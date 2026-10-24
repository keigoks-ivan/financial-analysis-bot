你是 stock-analyst **v20 判斷 agent**，標的 ROP（20261024）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ROP","date":"2026-10-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROP_20261024/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROP_20261024/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_revenue","label":"GAAP revenue","value":2171.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）","citation":"Roper Q3 2026 earnings release（8-K Ex.99）"},"note":"未查得"},{"id":"f_kpi1_gaap_operating_income_ma","label":"GAAP operating income / margin","value":28.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）","citation":"Roper Q3 2026 earnings release；營業利益 623.2M，利益率為 623.2/2171.8 自算"},"note":"未查得"},{"id":"f_kpi2_adjusted_ebitda_margin","label":"Adjusted EBITDA / margin","value":39.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）","citation":"Roper Q3 2026 earnings release；adj. EBITDA 864M，+7% YoY"},"note":"未查得"},{"id":"f_kpi3_adjusted_diluted_eps","label":"Adjusted diluted EPS","value":5.89,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）","citation":"Roper Q3 2026 earnings release（經 web search 摘要；GAAP DEPS 4.88）"},"note":"未查得（管理層稱優於其預期）"},{"id":"f_kpi4_free_cash_flow_ocf_capex","label":"Free cash flow（前九個月，OCF − capex − 資本化軟體，自算）","value":1800.0,"period":"9M FY2026（截至 2026-09-30，公告於 2026-10-22）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"9M FY2026（截至 2026-09-30，公告於 2026-10-22）","citation":"Roper Q3 2026 earnings release 現金流量表：OCF 1,882.2M、capex 35.4M、資本化軟體 46.8M；新聞稿未直接列 FCF"},"note":"未查得"},{"id":"f_kpi5_stock_based_compensation","label":"Stock-based compensation（前九個月）","value":163.9,"period":"9M FY2026（截至 2026-09-30，公告於 2026-10-22）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"9M FY2026（截至 2026-09-30，公告於 2026-10-22）","citation":"Roper Q3 2026 earnings release 現金流量表 non-cash stock compensation"},"note":"不適用"},{"id":"f_kpi6_guidance_fy2026_adjusted","label":"Guidance：FY2026 adjusted DEPS","value":"22.35–22.40","period":"Q3 FY2026 公告（2026-10-22）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026 公告（2026-10-22）","citation":"Roper Q3 2026 earnings release"},"note":"上調自 22.15–22.30；最新快照共識 FY1 22.34（consensus_revision）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-22","period":"2026-10-22","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-22"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_rop_gross_margin_pct","label":"ROP 毛利率","value":69.53,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROP.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rop_operating_margin_pct","label":"ROP 營業利益率","value":27.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROP.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rop_fcf_margin_pct","label":"ROP FCF 利潤率","value":30.93,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROP.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_csu_to_gross_margin_pct","label":"CSU.TO 毛利率","value":37.26,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSU.TO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_csu_to_operating_margin_pct","label":"CSU.TO 營業利益率","value":17.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSU.TO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_csu_to_fcf_margin_pct","label":"CSU.TO FCF 利潤率","value":21.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSU.TO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tyl_gross_margin_pct","label":"TYL 毛利率","value":47.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TYL.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tyl_operating_margin_pct","label":"TYL 營業利益率","value":15.14,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TYL.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tyl_fcf_margin_pct","label":"TYL FCF 利潤率","value":29.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TYL.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_jkhy_gross_margin_pct","label":"JKHY 毛利率","value":43.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JKHY.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_jkhy_operating_margin_pct","label":"JKHY 營業利益率","value":24.96,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JKHY.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_jkhy_fcf_margin_pct","label":"JKHY FCF 利潤率","value":19.91,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JKHY.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ame_gross_margin_pct","label":"AME 毛利率","value":36.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AME.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ame_operating_margin_pct","label":"AME 營業利益率","value":25.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AME.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ame_fcf_margin_pct","label":"AME FCF 利潤率","value":23.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AME.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":438.14,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":24.6,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_rsi14","label":"RSI(14)","value":80.65,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.45,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（22.24 → 22.34）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.74,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（24.39 → 24.57）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.57,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（26.24 → 26.39）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":22.34,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":24.57,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":26.39,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":19.61,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 22.34，分子＝快照價 438.14","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.831,"period":"2026-10-24","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-24"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-10-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 438.14 / W52 379.55 / W104 459.77 / W250 464.0 / W250 13週斜率 -0.26%"},{"id":"f_ma_w52","label":"52 週均線","value":379.55,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":459.77,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":464.0,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-0.26,"period":"2026-10-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 自述在多數利基市場為領導者或領導者的替代選擇，且無單一公司在大量產品線上與其競爭；未揭露份額數字或消長方向。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/882835/000088283526000009/rop-20251231.htm","excerpt":"We believe that we are a leader in most of our markets, and no single company competes with us over a significant number of product lines.","as_of":"2026-02-24","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子指出可能出現新競爭者，產品線可能受包含 AI 在內的新技術威脅；AI 能力可能快速商品化。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/882835/000088283526000009/rop-20251231.htm","excerpt":"In addition, new competitors may emerge, and product lines may be threatened by new technologies, including AI, or market trends that reduce the value of these product lines.","as_of":"2026-02-24","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q1 2026 財報電話會議：AI 與 AI 影響的訂單占新業務 75%，管理層稱法律與醫療無預算蠶食。","source":"VectorShift Roper Q1 2026 earnings transcript","url":"https://vectorshift.ai/research/companies/roper/earnings/2026-q1.html","excerpt":null,"as_of":"2026-04-23","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 載明 2025 年沒有任何客戶占任一事業部或公司總營收 10% 以上。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/882835/000088283526000009/rop-20251231.htm","excerpt":"Customers During 2025, no customer accounted for 10% or more of any segment or total Company net revenues.","as_of":"2026-02-24","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q2 2026 有機成長5%、軟體有機經常性收入+7%、企業客戶總留存率維持90%中段；全年有機成長指引5–6%，不含 Deltek GovCon 與 DAT 貨運復甦","source":"vectorshift.ai Roper Q2 2026 call in brief","url":"https://vectorshift.ai/research/companies/roper/earnings/2026-q2","excerpt":"Enterprise gross retention stayed in the mid-90s and organic recurring revenue across the software segments grew 7%, consistent with Q1 and expected to inflect higher in the second half.","as_of":"2026-07-23","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"AI／agentic 產品2026年尚非重大營收，變現預期為2027年議題；分析師7月將合理價自694降至550，理由為 AI 衝擊財務模型耐久性的疑慮","source":"Simply Wall St narrative update for Roper Technologies","url":"https://www.simplywall.st/narratives/0xz66nw8-update-for-roper-technologies","excerpt":"Fair Value US$550 Share price15 Jul US$438.1420.3% undervalued intrinsic discount Loading 1Y-8.49% 7D14.48% Share Like votes Follow Fair Value 1","as_of":"2026-01-07","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因素指出，併購成長需取得監管核准（含美國 Hart-Scott-Rodino 與海外反壟斷許可），列為併購執行風險；未見針對公司的現行反壟斷調查揭露。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/882835/000088283526000009/rop-20251231.htm","excerpt":"receive the necessary regulatory approvals (including clearance under the Hart-Scott-Rodino Act in the U.S. and similar antitrust regulations in foreign countries)","as_of":"2026-02-24","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"子公司 PowerPlan 與 Lucasys 反壟斷訴訟 2025 年 1 月以 2,400 萬美元和解並結案","source":"SEC EDGAR 10-Q 2025-06-30","url":"https://www.sec.gov/Archives/edgar/data/882835/000088283525000036/rop-20250630.htm","excerpt":"by former PowerPlan employees, alleged PowerPlan had engaged in, among other things, anticompetitive practices in violation of federal antitrust law which impacted the plaintiff’s ability to commercialize its software and services offerings. In January 2025, PowerPlan and the plaintiff agreed to settle the matter and such was fully concluded and cash settled in January 2025 for $24.0 on a","as_of":"2025-08-01","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 載明銷售須遵守 EAR、ITAR、OFAC 制裁，並可能受新增、擴大或報復性關稅影響","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/882835/000088283526000009/rop-20251231.htm","excerpt":"Our businesses may also be impacted by additional domestic or foreign trade regulations, including trade restrictions, trade agreements, tariffs (including new, expanded, or retaliatory tariffs), and sanctions.","as_of":"2026-02-24","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2025 美國以外客戶佔淨營收 13%，風險因子列出關稅與進出口要求不確定性","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/882835/000088283526000009/rop-20251231.htm","excerpt":"For the year ended December 31, 2025, 13% of our net revenues were generated from customers outside of the U.S. and 9% of our long-lived assets, excluding goodwill and other intangibles, were attributable to operations outside of the U.S.","as_of":"2026-02-24","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"TD Cowen 升評 ROP，稱關稅風險可忽略（美國曝險 85%），發布日不明","source":"TipRanks/The Fly: TD Cowen upgrades Roper Technologies on negligible tariff risk","url":"https://www.tipranks.com/news/the-fly/td-cowen-upgrades-roper-technologies-on-negligible-tariff-risk","excerpt":null,"as_of":"2025-05-01","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2019 10-K 稱多數材料來源充足，但部分零組件與次組件僅來自有限數量供應商；缺料曾造成出貨延遲但未對營收造成重大不利影響","source":"Roper Technologies 10-K FY2019","url":"https://www.sec.gov/Archives/edgar/data/882835/000088283520000006/a201910-kdoc.htm","excerpt":null,"as_of":"2020-02-28","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"第三方彙整稱 Roper 近期申報提示美國對中國、加拿大、墨西哥、英國等的新增或報復性關稅風險，並有單一來源供應商與少數雲端平台依賴","source":"policyrisk.com ROP","url":"https://policyrisk.com/world/company/ROP","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收 +8% 至 $21.7 億（內生 +7%、併購約 +1 點），調整後 EPS +15% 至 $5.89，並上調全年調整後 EPS 指引；Q3 分部數字未取得","source":"SEC 8-K Roper Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000882835/000088283526000042/a2026q3earningsrelease.htm","excerpt":null,"as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 分部：Application Software $11.8 億 +8%（內生 5%）；Network Software & Systems $4.309 億 +12%（內生 4%）；Technology Enabled Products $4.972 億 +7%（內生 7%）","source":"Zacks 對 Roper Q2 2026 財報報導（經搜尋摘要）","url":"https://www.easternprogress.com/roper-q2-earnings-top-estimates-application-software-sales-up-y-y/article_326e4c69-9b43-5a0d-b932-2b1fea865f70.html","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 全年指引：內生營收成長上調至約 6%、總營收成長 8%+，調整後 DEPS $22.15–$22.30","source":"Roper Q2 2026 earnings release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0000882835/000088283526000031/a2026q2earningsrelease.htm","excerpt":"The Company increased its full year total revenue growth outlook to 8%+, compared to a previous outlook of ~8%, and increased its organic revenue growth outlook to ~6%.","as_of":"2026-07-23","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"Deltek 政府承包企業業務 Q1 仍疲弱（聯邦採購中斷、機關重組、預算不確定）；管理層 2026 指引未預設 Neptune 復甦","source":"Roper Q1/Q2 2026 call 摘要（Quartr／vectorshift）","url":"https://vectorshift.ai/research/companies/roper/earnings/2026-q1","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子明列：若出現競爭或替代技術，商譽（$21,341.2，約占總資產 62%）可能減損；收購風險評估亦提及「來自 AI 的市場顛覆」易感性。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/882835/000088283526000009/rop-20251231.htm","excerpt":"If future operating performance at one or more of our business units were to fall significantly below current or expected levels, if competing or alternative technologies emerge, if discount rates rise, or if business valuations decline, we could incur a non-cash charge to operating income.","as_of":"2026-02-24","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 揭露其 AI 產品依賴第三方 LLM 供應商（OpenAI、Anthropic、Google、Microsoft），供應商可能漲價且 Roper 未必能轉嫁給客戶。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/882835/000088283526000009/rop-20251231.htm","excerpt":"As AI becomes more central to our offerings, our exposure to pricing changes from these providers increases, and we may not be able to pass such cost increases on to our customers.","as_of":"2026-02-24","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Seeking Alpha 2026-01 文章稱股價自高點下跌近 40%，歸因於 AI 引發的軟體股拋售。","source":"Seeking Alpha 'Roper Technologies: At A Crossroad'","url":"https://seekingalpha.com/article/4863674-roper-technologies-at-a-crossroad","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K 描述銷售通路主要為直銷辦公室、製造商代表、經銷商與配銷商；10-K 該節未載明通路結構性轉變。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/882835/000088283526000009/rop-20251231.htm","excerpt":"Distribution and sales occur primarily through direct sales offices, manufacturers’ representatives, resellers, and distributors.","as_of":"2026-02-24","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Piper Sandler 會議摘要：Roper 設有 25–30 人 AI accelerator 團隊協助各事業開發 agentic 產品；CentralReach 以 freemium 模式帶動快速採用。","source":"Quartr, Piper Sandler 5th Annual Growth Frontiers Conference summary","url":"https://quartr.com/events/roper-technologies-inc-rop-piper-sandler-5th-annual-growth-frontiers-conference_3sEdianz","excerpt":"CentralReach led AI adoption, using a freemium model to drive rapid uptake and ROI in autism therapy workflow. Applied learnings from CentralReach to other businesses like Vertafore, accelerating AI product rollout and adoption. AI accelerator team of 25–30 helps businesses develop agentic products, sharing expertise","as_of":"2026-09-15","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司 2026-10-22 將全年調整後 DEPS 指引上調至 $22.35–$22.40（前次 $22.15–$22.30），Q4 指引 $5.95–$6.00；Q3 調整後 DEPS 優於公司預期","source":"Roper 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000882835/000088283526000042/a2026q3earningsrelease.htm","excerpt":"Roper now expects full year 2026 adjusted DEPS of $22.35 - $22.40, compared to previous guidance of $22.15 - $22.30.","as_of":"2026-10-22","retrieved_at":"20261024","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Investing.com 彙整（2026-10）：16 位分析師平均目標價約 $445.92，區間約 $350–$550；評等 9 Buy／9 Hold／2 Sell；BMO 2026-10-07 以 Hold、目標價 $393","source":"Investing.com ROP consensus estimates","url":"https://uk.investing.com/equities/roper-industries-consensus-estimates","excerpt":null,"as_of":"2026-10-07","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Barchart（2026 年 7–8 月）：19 位分析師共識「Moderate Buy」，平均目標價 $438.80，最高 $550","source":"Barchart: What are Wall Street analysts' target price for Roper Technologies stock","url":"https://www.barchart.com/story/news/3947281/what-are-wall-street-analysts-target-price-for-roper-technologies-stock?.tsrc=rss","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月（2025-10-24至2026-10-24）共8份8-K，僅1份含重大項目（2026-04-01 Item 1.01/1.02/2.03，新5年期35億美元無擔保信用額度取代2022年舊額度）；清單無併購完成(2.01)、重編(4.02)等項目","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000882835&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["triggers","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-04-01 8-K Item 1.01：Roper於2026-03-30簽署新5年期35億美元無擔保循環信用額度，取代2022-07-21舊額度（再融資，非併購）","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/882835/000119312526138072/d124209d8k.htm","excerpt":"The new facility comprises a five-year $3.50 billion revolving credit facility, which includes availability of up to $150.0 million for letters of credit, of which $60.0 million shall be committed.","as_of":"2026-04-01","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K清單無2.01（完成併購）項目；唯一重大項目為信用額度再融資","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000882835&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K清單無Item 4.02（財報不可信賴/重編）項目；搜尋亦未見SEC調查","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000882835&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["triggers","decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ROP","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":69.53,"operating_margin_pct":27.97,"fcf_margin_pct":30.93,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROP","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CSU.TO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.26,"operating_margin_pct":17.86,"fcf_margin_pct":21.92,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSU.TO","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TYL","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":47.21,"operating_margin_pct":15.14,"fcf_margin_pct":29.05,"rd_intensity_pct":9.4},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TYL","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"JKHY","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":43.65,"operating_margin_pct":24.96,"fcf_margin_pct":19.91,"rd_intensity_pct":6.93},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JKHY","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"AME","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.36,"operating_margin_pct":25.9,"fcf_margin_pct":23.21,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AME","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"ROP"},"financial_history":{"ticker":"ROP","currency":null,"method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":5371800000.0,"revenue_yoy_pct":null,"gross_margin_pct":69.86,"operating_margin_pct":28.38,"net_income":4544700000.0,"diluted_eps":42.55,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":6177800000.0,"revenue_yoy_pct":15.0,"gross_margin_pct":69.72,"operating_margin_pct":28.25,"net_income":1384200000.0,"diluted_eps":12.89,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":7039200000.0,"revenue_yoy_pct":13.94,"gross_margin_pct":69.3,"operating_margin_pct":28.37,"net_income":1549300000.0,"diluted_eps":14.35,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":7902500000.0,"revenue_yoy_pct":12.26,"gross_margin_pct":69.24,"operating_margin_pct":28.29,"net_income":1536300000.0,"diluted_eps":14.2,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ROP/ROP_Q3_2026_Earnings_Call_20261022.md）

# Q3 2026 Earnings Call
**Roper Technologies, Inc.** | Earnings Calls | 2026-10-22

**Operator** (Operator):
Good morning. The Roper Technologies Conference Call will now begin. Today's call is being recorded. [Operator Instructions] I would now like to turn the call over to Zack Moxcey, Vice President, Investor Relations. Please go ahead.

**Zack Moxcey** (Executives):
Good morning, and thank you all for joining us as we discuss the third quarter 2026 financial results for Roper Technologies. Joining me on the call this morning are Neil Hunn, President and Chief Executive Officer; Jason Conley, Executive Vice President and Chief Financial Officer; Brandon Cross, Vice President and Chief Accounting Officer; and Shannon O'Callaghan, Senior Vice President of Finance. 
Earlier this morning, we issued a press release announcing our financial results. The press release also includes replay information for today's call. We have prepared slides to accompany today's call, which are available through the webcast and are also available on our website.
Now if you please turn to Page 2. We begin with our safe harbor statement. During the course of today's call, we will make forward-looking statements, which are subject to risks and uncertainties as described on this page in our press release and in our SEC filings.
You should listen to today's call in the context of that information. And now please turn to Page 3. Today, we will discuss our results primarily on an adjusted non-GAAP basis. For the third quarter, the difference between our GAAP results and adjusted results consists of the following items: amortization of acquisition-related intangible assets, transaction-related expenses associated with completed acquisitions, financial impacts associated with our minority investment in Indicor; and lastly, cash collected on Outgo's beneficial interest, which is the residual amount owed to Outgo after it sells receivables to a third party and is classified within cash flows from investing activities.
Reconciliations can be found in our press release and in the appendix of this presentation on our website. And now if you please turn to Page 4, I'll hand the call over to Neil. After our prepared remarks, we'll take questions from our telephone participants. Neil?

**Neil Hunn** (Executives):
Thank you, Zack, and thanks to everyone for joining us this morning. You can see our agenda on Page 4, so let's get into it. Next slide, please. As we turn to Page 5, I want to highlight 3 takeaways.
First, we delivered solid third quarter results, including 7% organic revenue growth and increased DEPS guidance for the year. Second, AI momentum continues to build, and we're pleased with the progress in the quarter.
Our businesses are bringing new products to market, and we're increasingly encouraged by the breadth of that progress and what these products will do for our customers. And third, we're active again on the acquisition front, completing three bolt-ons with our long-standing capital allocation discipline.
Starting with our results. Total revenue grew 8%, organic revenue grew 7%, EBITDA grew 7% and DEPS grew 15%. At a high level, we had a strong quarter, and to spike out a few of our larger businesses, we had another encouraging quarter for Deltek, although we continue to take a wait-and-see approach.
We continue to see nice supply side recovery at DAT. And unfortunately, Neptune continues to face subdued meter market conditions. Based on these results, we're also increasing our full year DEPS guidance.
It was a solid quarter, and Jason will walk you through the financial details in a moment. Turning to AI. Since our last call, our businesses have introduced a broad range of products that apply AI to the specialized tasks and workflows our customers manage every day.
Let me share a few examples. First, Vertafore launched agents for submission processing, benefit plans and document research and has now added 2 agents that automate policy processing for independent agencies. Since the beginning of the year, Vertafore has developed and launched 12 workflow automation agents with many, many more in development.
At Aderant, 7 AI agents are now in early access to help law firms bill more accurately and collect cash faster. The appeals agent helps draft billing appeals, the collection agent prioritizes overdue accounts and the time agent improves billing descriptions.
These are practical uses of AI to reduce administrative work and help law firms run more efficiently. Another example is PowerPlan, where our new intelligent unitization product tackles a significant industry challenge, more than $180 billion of capital investments awaiting detailed asset classification across the U.S. electric utilities.
Our purpose-built AI capability analyzes project and accounting data and recommends how cost should be allocated to individual assets. By accelerating that process, it helps utilities recover their capital investments and earn returns sooner, bringing forward revenue, earnings and cash flow and the productivity gains are substantial.
Customers are completing this work in minutes that previously took days or weeks. This is another powerful example of our focus across Roper, putting AI to work to help our customers grow, perform better and operate more efficiently.
Great work by Rafi and the team at PowerPlan. At Strata, financial decision intelligence helps health care finance teams identify what needs attention and understand what is driving performance. In a few minutes, I'm going to double-click on this specifically.
At CentralReach, ReportDraftAI is designed to improve provider productivity and economics. Clinical reauthorization reports typically take 9 to 12 hours per learner, much of which is nonbillable. By automating data gathering and preparing a draft for clinician input and review, the product frees up substantial capacity for billable care, creating opportunities for providers to serve more learners, supporting revenue growth and improving operational efficiency with their existing clinical teams. 
And Foundry introduced new AI capabilities for visual effects, while Subsplash launched work management products that bring AI and automation into Church operations. What is encouraging is both the breadth of this activity and how specific these products are to the markets we serve.
They address work our customers know well, work that takes time, require specialized knowledge and matters how their organizations operate. We continue to see a substantial opportunity to help customers do work more efficiently and effectively, and we're excited to partner with our customers across the enterprise to realize the promise of AI.
Our confidence and opportunity is grounded in the same advantages that have always made our vertical market software businesses strong, deep domain expertise, embedded workflows, unique data assets, trusted customer relationships and scaled distribution. 
Our businesses know their customers' workflows and where AI can save time and improve decisions. Each business develops products close to its customers, while our AI accelerator team helps speed development and share reasonable approaches across the portfolio. We're still early in commercialization and are starting to see adoption and monetization of our AI solutions.
Importantly, our products change how customers do work, so adoption will develop over time. As customers use our products, that experience will help our businesses refine the products and expand their capability remit. There's more work ahead, but we love the progress. We have new products reaching customers across a broad range of markets and a meaningful opportunity to build from here.
And third, we continue to execute our disciplined capital allocation strategy and are encouraged that we're able to execute three bolt-on acquisitions during the quarter. Specifically, we deployed $436 million towards bolt-on acquisitions for iPipeline, Procare and Strata. The common theme is expanding the capabilities and reach of our existing businesses, adding complementary products, expertise and customer relationships in markets we know well.
Each acquisition builds on our existing domain expertise and distribution, creating more opportunities to serve customers and drive long-term organic growth. Our approach remains consistent, evaluate each opportunity carefully and deploy capital where we see attractive long-term returns.
So a solid quarter with another impactful step on our AI journey. With that, let me turn the call over to Jason to walk through our financial results, capital allocation activity and balance sheet position. Jason?

**Jason Conley** (Executives):
Thanks, Neil, and good morning, everyone. Please turn with me to Slide 6 to review our financial performance. Our third quarter was highlighted by solid organic revenue growth and strong DEPS growth. We delivered revenue of $2.2 billion, which is up 8% over prior year, underpinned by organic growth of 7%.
Digging deeper here, organic recurring revenue grew [ 8% ] across our 2 software segments. Our enterprise software gross retention remains very high, consistently in the mid-90s. And further, core enterprise bookings were up mid-single digits on a TTM basis. EBITDA of $864 million was up 7% and converted to EBITDA margin of 39.8%. Core EBITDA margin was down 30 basis points with our software segment in aggregate slightly expanding, while our TEP segment was down 90 basis points.
Our Neptune business delivered more mechanical meters in the quarter, which has a dilutive impact on revenue dollars and margin. Over a longer arc, we expect a continued migration to ultrasonic meters, which drives higher lifetime value for customers and Neptune. DEPS of $5.89 was up 15% over prior year and above our guided range of $5.75 to $5.80 on better margin performance.
Free cash flow of $805 million represents 37% of revenue, but was down 4% versus prior year, given we had timing of interest coupon payments on bonds issued in 2025, and we had a temporary lag in collections at our Illumia business as they move through an ERP implementation.
For the year, we expect free cash flow to be 30% more revenue and with our share repurchase activity, free cash flow per share is expected to grow in the double digits area. Now if you turn with me to Slide 7, I'll walk through our financial position and capital deployment. Enabled by seasonally strong free cash flow and proceeds from the divestiture of Indicor's instrumentation businesses, we reduced our net debt to EBITDA by 0.5 turn within the quarter to land at 2.9x, all while simultaneously deploying $436 million towards acquisitions.
We finished with over $300 million of cash and $1.3 billion drawn on our $3.5 billion revolver. In the quarter, Indicor announced the sale of the remaining flow controls businesses to Xylem. We expect around $600 million of pretax proceeds sometime in Q4 as the transaction moves through regulatory clearance.
Also in the quarter, we acquired 3 tuck-in businesses for iPipeline, Procare and Strata. Consistent with our acquisition criteria, these tuck-ins play directly into the strategy of increasing organic growth where we have the highest right to win.
All 3 tuck-ins are growing faster than their acquiring platforms and coupled with synergies are expected to generate very attractive returns. Looking ahead, we now have more than $6 billion of capacity for capital deployment over the next 12 months, given strong free cash flow, which will be enhanced by proceeds from Indicor's sale of its flow controls businesses.
In summary, we remain well positioned to deploy capital towards the highest risk-adjusted return opportunities through a disciplined and analytical process and approach. Neil, with that, I'll turn the call back over to you.

**Neil Hunn** (Executives):
Thanks, Jason. As we turn to Page 9, let's review our Application Software segment. Revenue grew 7% in total with organic growth of 6%. EBITDA margins were 43.7%, up 30 basis points year-over-year.
Looking across the segment, AI momentum continues to build with more of our businesses bringing new solutions to market. We also continue to see solid progress on cloud conversions, including encouraging signals at Deltek. Turning to the business highlights. Aderant had another excellent quarter.
The team continued to expand its AI agent platform, as previously mentioned, with capabilities across rates, compliance and general ledger forecasting. Vertafore delivered growth across its agency, MGA and carrier businesses and launched 6 new AI agents, along with its value-based credit model.
This value-based pricing model is a key enabler of product-led growth as customers will utilize credits towards any current and future agentic solutions on the Velocity platform. As we discussed last quarter, Vertafore strategy starts with high-volume labor-intensive work, embedding agents directly into the systems customers already use.
The latest launches expand the work those agents can do and build on the foundation established with Velocity. Deltek had another encouraging quarter with continued strength in its private sector solutions. Government contracting bookings have been solid over the last couple of quarters, although the broader market remains uncertainty. Against that backdrop, customers are showing increased interest in moving from perpetual license to our cloud-based offerings. 
As we discussed earlier, we also saw new AI solution launches at CentralReach with ReportDraftAI and PowerPlan with intelligent unitization. Finally, we completed 2 bolt-on acquisitions. At Procare, we added Playground, which helps child care centers manage enrollment, billing and daily operations.
Playground has exceptional product market fit and is highly complementary to the existing Procare product set. We're excited about the growth opportunity from pairing that product with Procare's distribution and payment infrastructure. 
And at Strata, we added c. myers, which helps banks and credit unions plan for growth and manage financial risk. This quarter, I spent a full day with the Strata team and finance leaders from 9 of our health system customers at a codesign workshop for Financial Decision Intelligence, or FDI, Strata's new AI capability for health care finance. FDI became generally available on September 1.
FDI helps finance teams diagnose what is changing in their business and where to intervene to improve performance. For example, when joint replacement margins declined despite rising procedure volumes, FDI automatically explores the underlying drivers from payer mix and reimbursement to labor and implant costs to identify the source of margin pressure and focus management's response. 
FDI brings together 3 advantages we see from across the portfolio. First, proprietary data and ontologies. Every health system has its own accounting procedures and definitions. Two hospitals can both report their margin on joint replacements and mean very different things.
Strata spent decades mapping thousands of provider general ledgers into a specific common structure supported by health care cost accounting down to the individual patient encounter. That makes meaningful benchmarking possible and gives FDI its foundation. Its calculations use the same governed measures customers rely on to close their books with consistent repeatable results that are traceable to the source.
You cannot prompt your way to that. It is earned one customer implementation at a time over years. Second, turning insights into action. FDI operates inside the Strata platform, delivering answers in seconds and connecting those insights directly to the workflows where customers manage costs, improve margins and allocate resources.
And third, real customer trust. Health care finance leaders need confidence in the tools they use to make consequential decisions. Strata has earned that confidence through long customer relationships. Trust is critical to AI adoption and is very hard to replicate. Throughout the workshop, the customer request was simple and consistent, productivity, less time assembling and reconciling analysis and more time working with operating leaders to improve performance.
One CFO described analysis that took several people hours to being nearly instant and FDI doing a more comprehensive and grounded analysis. This frees finance teams to focus on improving profitability and supporting higher quality care. 
Strata is selling FDI as an add-on subscription, creating an opportunity to grow recurring revenue. This is just the beginning for FDI. I'm excited about the road map ahead. I'm proud of the Strata team's development speed and close customer collaboration and pleased with its partnership with our Roper AI accelerator team. Deep vertical data and domain expertise within each business paired with central AI capabilities. That is the model we're scaling across Roper.
Now turning to our outlook. We expect to see application software organic growth in the fourth quarter to be similar to that of the third quarter in the mid-single-digit plus range. Please turn us to Page 10. Total revenue in our Network Software segment grew 8% with organic growth of 5%. EBITDA margins were 52.4%, down 130 basis points year-over-year. Core margins were essentially flat to the prior year. Turning to the business highlights. DAT was strong in the quarter and accelerated growth, supported by expansion of its network, higher average revenue per user and continued adoption of its digital freight marketplace solutions.
We continue to see encouraging signs in the freight market with the supply side recovery progressing. As we've discussed, we would still like to see stronger load volume before calling a broader recovery. We also completed the Origo bolt-on acquisition for iPipeline. Origo connects U.K. pension providers, investment platforms and financial advisers, automating wealth transfers, enabling secure data exchange.
It complements iPipeline solutions for selling and administering financial products and expands its presence in the U.K. wealth and retirement market. Foundry also continued to grow and reached a record level of ARR. SoftWriters grew as adoption of its AI order entry solution continued to expand.
As I shared last quarter, following my visit to LI Script, this solution addresses a meaningful customer need, reducing the time spent on manual order entry so pharmacy teams can focus more of their capacity on clinical review, customer service and patient care.
Order entry is a starting point, and the team now has additional AI products in beta. Subsplash is tracking in line with our year one target and continues to advance the AI offerings, including enhanced workflow automation. 
Turning to our outlook. We expect network software organic growth in the fourth quarter to be a touch higher than Q3 and be in mid-single-digit plus range is based on strength at DAT and Subsplash becoming organic in Q4.
Now please turn to Page 11, and let's review our TEP segment. Total revenue and organic revenue both grew 10% in the quarter with exceptional growth in NDI and strong performance at Verathon. EBITDA margins were 34.3%, down 90 basis points year-over-year. Starting with NDI, the business had another excellent quarter, delivering exceptional growth driven by continued demand for its precision measurement solutions.
Verathon also delivered a very solid quarter with strength across its BFlex, GlideScope and BladderScan product families. In addition, we're encouraged by the positive customer response to the CFlex single-use cystoscope launch, which further expands Verathon's single-use portfolio.
Neptune had a softer Q3 following a better-than-expected first half. We now see second-half revenue slightly down versus our prior outlook for modest growth. Q3 mix skewed towards mechanical meters, putting pressure on both revenue and margins. That mix is likely to continue into Q4.
We view this as temporary as the long-term secular demand for static meters remains fully intact. Finally, I want to recognize the teams at CIVCO, FMI, Inovonics and rf IDEAS, each delivered strong execution and growth in the quarter.
Turning to our TEP outlook. We expect organic growth in the fourth quarter to be in the mid-single-digit range. With that, please turn with us to Page 13. On this page, let's walk through our increased full year adjusted DEPS guidance as well as our Q4 outlook. For the full year, we're raising and narrowing adjusted DEPS guidance to a range of $22.35 to $22.40. That represents a $0.15 increase at the midpoint of our prior guide and a $0.95 increase from our original guide.
Our full year revenue expectations continue to have total revenue growth north of 8% and organic revenue growth in the 6% area.
For Q4, we're establishing our DEPS guidance -- adjusted DEPS guidance of $5.95 to $6, expect our tax rate to be in the 20% to 21% ZIP code. Now please turn to Page 14, and then we'll open it up to your questions. 
We conclude with the same 3 points with which we started. First, we delivered solid third quarter results. Revenue grew 8%, organic revenue grew 7%, EBITDA grew 7% and adjusted DEPS grew 15%. We're raising our full year earnings outlook again, reflecting the strength of our year-to-date performance.
Second, AI momentum continues to build across Roper. Our businesses launched several new agentic solutions this quarter, expanding the work we can help our customers accomplish. The Strata workshop brought that opportunity to life.
Our ability to deliver that kind of value rests on advantages built over many years, deep domain expertise, proprietary data, embedded workflows and customer trust. Those advantages are unique to our businesses and central to how our businesses are developing and deploying AI. We're still early, but the opportunity is substantial. As our software takes on more valuable customer work, we have the opportunity to expand our addressable markets and earn a greater share of the value we create.
Finally, our capital allocation discipline remains unchanged. This quarter, we deployed $436 million into bolt-on acquisitions for iPipeline, Procare and Strata, adding capabilities to established businesses in markets we know well.
As you heard Jason mention, our leverage now sits at 2.9x, and we have over $6 billion of capital deployment capacity over the next 12 months. With that, we're pleased to be putting capital back to work through M&A, and we look to 2027 with cautious optimism about compelling opportunities to deploy capital and accelerate long-term cash flow per share compounding.
As always, our standard for deploying capital remains the same. We'll pursue the opportunities that offer the most attractive, durable and long-term cash flow per share compounding whether through acquisitions or opportunistic share repurchases. 
Looking ahead, our focus is straightforward: help our customers accomplish more, expand the work our businesses can do for them and invest the cash we generate where we can compound it most effectively. 
That is how we will build an even stronger Roper and deliver durable long-term growth in cash flow per share. As we wrap up, I'd also like to welcome Abhijit Dubey to our Board of Directors, who is the CEO and Chief AI Officer at NTT DATA. We're delighted to have him join us and look forward to his perspective and contributions as we continue to execute our strategy, broadly deploy AI across our product sets and our enterprise and create long-term value for our shareholders. So with that, let's open up to your questions.

**Operator** (Operator):
[Operator Instructions] Your first question is from Joe Giordano from TD Cowen.

**Joseph Giordano** (Analysts):
Maybe one just like on a specific company, but like I'm sure you saw like the Journal article the other day on autism care hours, particularly at PE-owned facilities. And I'm just -- maybe it's for the wrong reasons that these hours are going up in some of these places, but I'm just curious like what that means for the rollout of stuff like CentralReach. Like it seems like almost requirement to have technology like that if you're going to push the hours to the extent that this seems to be happening.

**Neil Hunn** (Executives):
I think -- I appreciate the question. So I think the thing that is great about CentralReach's Solutions is that it's all about appropriate care that is auditable that's to the standards and there was an article or there's a flare-up on this about a year ago when we looked across the CentralReach customer base, and it was like the most compliant set of customers.
I think it was in Minnesota, I forget where it was a year or so ago on some fraud claims. And it was -- the automation with CentralReach was the cleanest set of providers in the jurisdiction.
So same thing here. I mean it's just a good audit sort of backbone when you sort of use the CentralReach or automated systems here.

**Joseph Giordano** (Analysts):
If I think about the fourth quarter guidance, I'm just curious, like I know it's early for '27, but like are these exit rates fair starting points for us to think about moving forward? Like I'm curious like something like Neptune, right? Like that's a project-centric business. It's hard for us to kind of contextualize. So like if that's -- what are the prospects like kind of into next year?

**Neil Hunn** (Executives):
I would say for the '27 sort of setup, first, it's super important that we're just starting basically next week the planning process.
So this is -- we have to go through all the process with all 29 companies and understand the puts and takes and all the nuances. So we always have to caveat that. But we'd say it's generally a constructive setup. The recurring sort of revenue, sort of exit run rate is encouraging. Certainly, the velocity of the product development on the AI side is encouraging. Now caveat there is we're now into the commercialization phase, and we've got to drive the bookings and adoption and consumption.
So that's sort of where we are in that. I'm sure there'll be questions on that in today's call. And then if you sort of go segment by segment, Deltek has had a couple of good quarters. We -- as I mentioned, we're still in a wait and see. We want to see that continue.
And then the other thing about Deltek is the business is definitively turning more recurring, more SaaS. So we have to overlap the perpetual in that business. And then just a reminder, CentralReach, we get a full year of organic.
In network, certainly, what we're seeing at DAT is encouraging, but it's supply driven. So it'd be more -- it'd be healthier if it was demand driven, but it's definitely a better setup coming into next year versus coming into this year at DAT.
And then remind you, Subsplash is fully organic or organic for the full year. And then TEP, Neptune is really to be determined. And it has a wider range of outcomes. It had a wider range of outcomes this year than we anticipated that we're experiencing.
And so that's the -- that's to be determined. We'll have to really sort of spend a lot of time with the management team and understand the industry trends heading in next year. And then NDI, which has been awesome for us this year will be more normalized next year. So -- but the setup is generally constructive.

**Operator** (Operator):
Your next question is from Brent Thill from Jefferies.

**Ria Naidu** (Analysts):
This is Ria on for Brent. On Deltek last quarter, you mentioned that you wanted to see consistent conversion of the GovCon pipeline before being able to call this an inflection from OBBB. I'm just curious, did this quarter give you that and I recognize it's early, but maybe just to elaborate on that last question. How are you thinking about Deltek for 2027?

**Jason Conley** (Executives):
Yes. I think it was a very good quarter for Deltek. What we are seeing, thankfully, is that more customers are starting to move to the cloud. So the bookings were quite strong. That doesn't obviously materialize in revenue immediately like perpetual. It's an uncertain market.
I think what Deltek is doing is, and we mentioned this last quarter is announced the end of support for the Costpoint on-prem solution in the first quarter of '28. So that's creating a catalyst for them to go back to the base and start to do that migration. So despite a sort of uncertain market, they're sort of making growth happen. So we'll see one more quarter before we get into next year, but momentum is good there.

**Ria Naidu** (Analysts):
Got it. And then just curious on any incremental updates on the M&A environment since last quarter. I think you mentioned $436 million deployed towards bolt-ons, but I think I'm wondering more so on the larger deal side of things that you're seeing. So any color you're able to provide there would be helpful.

**Neil Hunn** (Executives):
Yes. I would say, as I mentioned in the prepared remarks, we look to next year with sort of cautious optimism. Janet and her team continues to be very busy.
I would say the pipeline tilts more proprietary and proactive outreaches than large-scale processes sort of very bespoke. We just had a couple of weeks ago, our second annual CEO conference where we had 20 or so target CEOs together for a day, 1.5 days going through Roper and getting to know the businesses.
So that was well attended and very high-quality targets at that business -- at that summit. And it's -- we're cautiously optimistic. I mean all the pressures that have been on the private equity firms for now going on 3 years continue to exist, LP credit, DPI pressure and sort of just coming to grips with where public companies are valued.
It takes there's a little bit of -- there's a lot of psychology in that, and that psychology appears to be coming into reality.

**Operator** (Operator):
Your next question is from Brian Peterson from Raymond James.

**Brian Peterson** (Analysts):
Thanks guys [Technical Difficulty].

**Neil Hunn** (Executives):
Thank you, Brian. We've lost you.

**Operator** (Operator):
Your next question is from Terry Tillman from Truist Securities.

**Terrell Tillman** (Analysts):
On Vertafore, I care a lot about the insurtech space. I'm curious how is the -- you called out the ARR growth. How is that faring versus the overall app software growth? And then it's still the first question, it's a multiparter of the first one. This idea of the value-based credits, will that just take some time for that revenue stream to ramp? And then I had a follow-up on Deltek.

**Neil Hunn** (Executives):
Yes, I'll take the value-based credit and Jason can take the first.

**Jason Conley** (Executives):
Yes, Terry, they're in line with the segment in terms of the ARR growth.

**Neil Hunn** (Executives):
And on the value-based credits, just to remind everybody, this is a -- these contracts are being structured as recurring. So you're buying a fixed amount. Those are -- have to be consumed in a specific period of time.
As a result, the revenue recognition treatment is recurring, not reoccurring. So it will look and feel like subscription revenue. Now, obviously, it's very important for Vertafore, sort of, if you will, forward-deployed teams, the customer support implementation teams, to make sure there's wide-scale adoption and utilization.
So you get the upgrades, the uplifts, the additional sort of credit purchases and the renewals. And that's where we are right now. It's where I think the Velocity platform was GA within the last 60 or 90 days.
I mean the full GA release has been very recent, and we're in the early adoption phase.

**Terrell Tillman** (Analysts):
Good to know on recurring versus reoccurring. I'm glad I asked that in terms of Deltek. I don't know if this is kind of a change in tone here, but I forgot where you last gave an update on the SaaS versus on-prem for Deltek, but it sounds like maybe things are picking up. So is kind of the real takeaway that the license part of total revenue could be like an incremental headwind in '27, but then you're going to have right behind it this kind of acceleration in recurring. Just anything more you can share on kind of what you're talking about here because it sounds like maybe it is picking up steam.

**Jason Conley** (Executives):
Yes. And I think that -- as you can appreciate, Terry, the timing of getting to the cloud is a little harder because it's a different value prop. So there's -- that's sort of what we're managing through.
But certainly, it's our biggest maintenance base at Roper. And so the timing of getting that to the cloud is certainly would outstrip perpetual. It's just kind of how that phases over the next few years is a question. So -- but we do feel good about the momentum as we sit here today.

**Operator** (Operator):
Your next question is from Brian Peterson from Raymond James.

**Brian Peterson** (Analysts):
Can you hear me? Sorry about that. I just wanted to ask on the appetite for AI and the adoption curve. I'm curious what products are you seeing that ramp a little bit faster than expected? And also just on the customer appetite in the packaging, has that been any challenges? Or is it more about change management? Just kind of curious what the customer appetite is at this point?

**Neil Hunn** (Executives):
So the -- I'll try to be comprehensive in my answer, and I don't -- we can certainly take this offline as well. So let me just follow the bouncing ball of this. So it was really a year ago, the models and the capability of AI, we really could do agentic work. So the first question is, can we think of the ideas, the customer magic, if you will, sort of put us into the product stack. 
That question is absolutely, without question, yes. I think it's 18 -- 17 or 18 of the 21 software businesses have agentic solutions in the market. So that's the first question. So first, can we think of the idea. The second one, can we build them? So that's yes. And that's led us to where we have the majority -- the vast majority of the companies having these products in the market.
Now the question is, can we drive early adoption, convert sort of, if you will, the beta customers to early adopters. The answer to that has been yes. Just go back to the remarks I said in the call about Strata and FDI or last quarter of SoftWriters with pharmacy automation.
The answer to that has been yes. Now it's about can we get -- we need to get to broad scale across -- into the go-to-market teams across all these businesses and get it broadly distributed into our customer bases and drive adoption.
So the customer interest has been very, very positive. And probably the most positive I've seen in my career in tech because we're literally delivering a bot that does magic things. So that's the good part. Now what we -- I think all companies, and we're not alone in this, is now you're facing budget cycles, AI committees, all the safeguards and governance of data.
And so we're just going through the go-to-market processes. The early indications are positive, but we said this year was going to be largely a year of commercialization learnings and adaptations and again, progressing well, but it's still to be proven.
And then I think the first part of your question, where is some of the better customer reaction, certainly CentralReach, certainly Aderant, certainly SoftWriters as in pharmacy automation, the early adopters at Vertafore, the early adopters at Strata. I mean there's really not -- I'm just going through the list in my mind, there's not really been really a flat launch.
I mean it's -- again, it's early days, and we will not bet a thousand across all these products, across all the companies, but we haven't had any abject out-of-the-box failures, if you will.

**Jason Conley** (Executives):
I think one of the interesting changes with AI, obviously, is when you launch a product, you can iterate -- continue to iterate. So you'll have some immediate customer feedback. So we've seen some times when something wasn't quite right, but then we've been able to iterate quickly based on feedback from the customer. So that's been helpful.

**Brian Peterson** (Analysts):
I appreciate the color, guys. Maybe just one added element there. As we're thinking about use of kind of frontier models versus some of the lighter weight models, how are you guys thinking about that balance? And does that change any views on how we're thinking about AI-oriented margins over the near to medium term?

**Neil Hunn** (Executives):
Yes. The punchline is our gross margins on these agentic tools are very positive, sort of at our software gross margins. Our philosophy on this at the moment, and this is obviously subject to change, and this is well informed by our leadership team and our central accelerator -- AI accelerator team, is we are 100% optimizing speed of development and deployment.
And so we're working with a lot of the models that are on the frontier. We don't need the most frontier model. Let's be very clear about that. We don't need 5, 6 Astra or Fable 5.1 or 2 or whatever the current release is. But we're going to use sort of the cheaper, downscaled models from the frontier.
But the harnesses that come with them, you can just get moving much, much faster on the product side. Now over time, every one of the products, 100% of the products have the model routers. And so we can sort of -- we have multiple sort of models underneath each product in case when you call Anthropic or OpenAI, they're not answering the phone and with the latency you need, you immediately flip over to another model. That architecture allows us to switch the models either into small language or open source models over time to manage the cost. But right now, we're optimizing for speed of development.

**Operator** (Operator):
Your next question is from Faith Brunner from William Blair.

**Faith Brunner** (Analysts):
Congrats on the quarter. Maybe to pull on a prior thread, you talked about you're seeing that encouraging engagement around adoption and now the focus is scaling that.
So as you kind of work through the early process of that, what have you learned? What challenges are still there? And how are you kind of adjusting your go-to-market strategy to address these new challenges? And how do we get to a more clear monetization path, if that makes sense? And then I have a quick follow-up.

**Neil Hunn** (Executives):
Yes. I mean this is -- keep asking this question because we'll just share our learnings as we go. I mean, obviously, we've had to figure out how to price all of these and not -- there's not a one pricing size fits all. It's different per company and per -- I wouldn't say per product, but per company based on where their customers are and the existing economic relationships we have with our customers.
So we generally -- we think we figured that out across the board. Then it's how do you sell this in addition to versus in lieu of everything else that we're selling because there's still a strong demand for, if you will, the legacy software stack.
So how we make sure this is on top of in addition to. And then it's like, like I said, like in health care, in particular, acute care hospitals have sort of an AI governance overlay.
And that was a new learning from the Strata team, for instance. It's like it's -- it has a traditional sales cycle and then another piece of it. So it's not a barrier. It's just maybe it slows things down a little bit. And those are the sorts of things that we're learning right now.

**Faith Brunner** (Analysts):
Okay. That makes sense. And then maybe as we get more cautiously optimistic about M&A, how are you thinking about -- how does AI change your whole thought process on what makes an attractive target, right? So is there different growth considerations, different competitive considerations that you now have to consider? And how are you guys working through that?

**Neil Hunn** (Executives):
For sure. So the first thing, and we've been doing this since -- over the last couple, 3 years since AI, since the ChatGPT moment, if you will, we need to certainly make sure and do the diligence that the end customer of the software company we're looking at is a viable long-term customer.
The customer is viable. So look at what we did last year, it was autism therapy, so people providing therapy to youth and then people going to church. So the end customer is highly viable and will not be sort of disintermediated by AI, if you will.
Then it comes down to what we see in our portfolio. Do you have sort of the defensive moats and offensive moats to be a winner in the AI world, right? So do you have sort of the right amount of data and the data rights and proprietary nature of the data? Do you have network effects? Do you have sort of configuration lock-in? So -- and et cetera, et cetera. I won't go through the full moat framework here.
So then do you have the preconditions to be successful in AI. That's where we are now. Fast forward a year or 2 or 3 from now, it becomes, I think the discernment becomes even easier because you have taken -- targets will have taken those advantages, and will either have proven or not proven that they're winning in the AI, would be able to develop products, bring them to the market, monetize the products, drive additional customer value. And so the companies that we're looking at now are in the earlier stages of that.

**Operator** (Operator):
Your next question is from George Kurosawa from Citi.

**George Michael Kurosawa** (Analysts):
A couple of quick ones for me. It looks like buyback activity was paused in the quarter. I think it's something you've kind of messaged you were doing as you're preparing for the M&A environment to potentially warm up. Just maybe how you're thinking about buybacks going forward?

**Jason Conley** (Executives):
Yes. Thanks, George. I think it's the same as we've always talked about, which is the relative sort of risk-adjusted returns for us. And for us, obviously, the buyback is attractive, but the option value on the M&A, given all the dynamics we've talked about in TEP and that everybody really knows about is worth the deleverage and preparing our balance sheet for that event.
Now if we fast forward a couple of quarters from now, we still have that option available to us. We still have quite a bit on the authorization. So that's still a viable alternative if the M&A markets don't cooperate.

**George Michael Kurosawa** (Analysts):
Okay. Great color. And you referenced on the free cash flow side, some impact from collections timing, the ERP implementation at Illumia. Maybe if you could quantify the magnitude of that and then ERP implementations have a habit of maybe extending beyond initial time lines. Is that ERP -- are those collections issues now addressed? Or is there any potential that could extend into Q4?

**Jason Conley** (Executives):
Yes, certainly a lot of focus by the team there, and I know they're going to do a great job. They're just powering through some order-to-cash challenges. They actually went live in January, but the big renewal season is in the summer and fall. So we expect to see some improvement in the fourth quarter. Some of that might spill into the first quarter of next year.
But when you kind of take a step back for the year, we expect free cash flow per share to be in line with DEPS growth, maybe even a little bit better. We'll see how it plays out. So that should all sort of normalize as we close out the year.

**Operator** (Operator):
Your next question is from Daniel Jester from BMO Capital Markets.

**Daniel Jester** (Analysts):
So I wanted to make sure I caught this right, but I think you said earlier in the call that a majority of your businesses now have an AI solution in the market.
And I guess, given the sort of urgency and the sort of moment in time that we're in and the past comments you've made about the ability to sort of speed your development, I guess, what's the time line to get to 100% in terms of your businesses and software having an AI tool? And are there any sort of commonalities in terms of limiting factors to get there?

**Neil Hunn** (Executives):
Yes, I appreciate the question. So when you look at the portfolio, sort of there's basically 3 companies that don't have an AI tool.
One is not a true software company. It's a group purchasing organization. So they don't really have like an agentic software front that reports -- MHA reported in the network segment. They're using all sorts of AI inside the business to drive productivity. But -- so that one, set that aside. 
Then you have 2 businesses that are in clinical diagnostics, DI and Clinisys. They have early AI tools, but this is a -- what laboratory software does and this sort of -- this remit is it's nearly a fully solved technical problem. There's not like -- this is how you run laboratories and route samples to analyzers and take results of analyzers and report that.
And so it's basically already fully automated process. And so there's not a large agentic remit to do here. Now, they're adding some AI tools around it, but it's not like these processes are already fully automated.
So essentially, a long-winded way of saying the companies that have AI remit, 100% of those companies have AI tools today.

**Daniel Jester** (Analysts):
That's super helpful. And then I guess I'll pull on the AI monetization thread as well for my follow-up. I guess as you think about next year, I guess, how diverse across the portfolio do you think that the monetization will be? Do you think that some parts of the business are going to have one type of way of monetization and other parts of the business, a very different one.
I guess maybe at an enterprise level, how should we be thinking about monetization? And maybe any color you can provide about the diversity at which parts of the business maybe will come sooner and which parts maybe will be coming a little bit later?

**Neil Hunn** (Executives):
Happy to do it. All right. So on the diversity of pricing models and AI, it comes in 3 general flavors. The first flavor we already talked about, I'll call it like this, this tokenized fixed budget, use it over a period of time where you take it as recurring. That appears to be the predominant, the majority of what Vertafore, Aderant, CentralReach, I mean, that's the predominant chunk, maybe less CentralReach, but that's the predominant way that our companies are going to monetize early.
So it's a consumption-based thing, but you buy a fixed amount of consumption, it is use it or lose it. As you consume that, you buy additional sort of chunks. There's -- the other model is straight consumption. It's a minority of what we're doing, but where we have straight consumption, it's where our customers already buy from us largely on a consumption basis.
So in pharmacy automation, a lot of the tools are already paid on a per script basis. So we monetize on a per script basis with AI tools there, or at DAT, we monetize what we do at Convoy and DAT on a per-load basis. So AI there will be on a per-load basis.
The third way is going to is -- and this is like, for example, at Deltek, where their software remit is ERP for government contractors. And so how do you automate like the accounting close is one of the products that -- one of the product features they're delivering right now. That's going to be basically delivered in the cloud as an add-on.
So you're going to see, if you will, accelerated move from ground to cloud at a higher price point once you get to the cloud. So those are the 3 models. To your point about which ones will show up first, I think it will sort of go in sort of the first 2 models, the consumption, if you will -- sorry, the subscription model where you have consumption embedded in that and the straight consumption, those will be the ones that show up earlier.
And then -- and then the lift and shift to the cloud will take a little bit more time, I would anticipate.

**Operator** (Operator):
Your next question is from Ken Wong from Oppenheimer.

**Hoi-Fung Wong** (Analysts):
I just wanted to circle back to TEP growth. Decel from the double digits that you guys reported this quarter. How much of that is divestiture? How much of that is you guys, I think, had called out some Neptune softness? Any color you can provide there?

**Jason Conley** (Executives):
Yes. Ken, so second half, we said it was going to be high single digits and it being a little bit higher in the third quarter. And so that did play out.
And so we've got mid-singles for the fourth. I would just say broadly, it has been the Neptune softness, and that's -- it's really a market sort of dynamic. And it's specifically for us, volume was okay, but we actually had more mechanical meters, has a lower ASP, and lower margin. So that was sort of the driver of the second half.
And we didn't have -- our divestiture -- we did divest the industrial businesses a few years ago, and we're getting the proceeds from that, but there's no sort of near-term divestiture activity in that segment.

**Hoi-Fung Wong** (Analysts):
Okay. Perfect. And then on the EPS guide or DEPS guide, any impact from the bolt-ons that you guys just picked up?

**Jason Conley** (Executives):
No. I mean the impact for us will be more next year. The current quarter, it's actually a little bit dilutive as we've got some synergies that will roll through next year. But it's actually -- for the fourth quarter, it's a little bit dilutive, few pennies.

**Operator** (Operator):
Your next question is from Josh Tilton from Wolfe Research.

**Joshua Tilton** (Analysts):
Maybe for my first question, I feel like there's been like a lot of hypotheticals and what if and how do we see the path of adoption play out around AI and just the monetization framework. And I understand why everyone is asking the questions. But unless I misunderstood, I thought you guys called out in the prepared remarks that you are seeing monetization from AI today. So I kind of like to focus on that comment, like where are you seeing the monetization today? How are you seeing it? And if we're already seeing it in some places today, like is that where we should expect it to be the most meaningful next year?

**Neil Hunn** (Executives):
Yes. I appreciate the question, Josh. So yes, I mean, this is -- I think the question is more on the -- how do we scale this. And obviously, this is new, not just for us, but for the economy at large.
And so we're all trying to figure that out. Where we're seeing early AI sort of monetization is where the product stacks were first to market, so CentralReach. For instance, CentralReach, I'll have Jason to make sure I sort of keep me honest here.
But 75% of their bookings are either AI-related, AI-specific or AI-related bookings in that range, for instance. Aderant, the number is like 25% of their bookings are either AI or AI related.
The anticipation for what's now back behind sort of the -- they were, I don't know, a year ahead of the portfolio.
Now the portfolio is catching up, 25% to 75% is a wide range, but it would be nice to see that as we sort of scale across a dozen of our companies, but it's too early to sort of say it's going to be 10%, 25%, 50% of bookings over time are going to be AI related.
Fast forward 3 or 4 years, like everything is AI. Like this whole thing, what's AI, what's not AI, it's going to be indistinguishable. So I think we're at a moment in time in that regard.

**Joshua Tilton** (Analysts):
Makes sense. And then maybe just my follow-up. Neptune sounds like, and again, I could be a little bit wrong here, but it sounds like second half is a little bit less favorable. There's a mix dynamic. We believe in this view of moving towards the ultrasonic meters over time, better pricing.
I understand all that. I guess, is there -- was the mix dynamic unexpected? And I ask it in the sense that is there a correction that can be made into next year where we can go back to maybe a better-than-expected Neptune outcome after we saw what happened this quarter, we step back, we make an adjustment and we go back to being a little bit better? Or do you expect kind of whatever you're seeing pressure the business today sort of last beyond this quarter, maybe into next year?

**Jason Conley** (Executives):
Yes, I appreciate the question. I mean I think it's -- the static pipeline from Neptune, customer by customer is strong. So there is definitely a market demand for it. It's just -- we just had pushes on the pipeline.
So we do think coming into next year, it's going to be more favorable for us. Timing is going to be uncertain in terms of kind of the quarterly cadence. But yes, that secular demand is there. So we feel good about that.

**Operator** (Operator):
Your next question is from Brett Linzey from Mizuho.

**Unknown Analyst** (Analysts):
Ryan on here for Brett. Yes, I wanted to just ask -- get a little bit more color on Neptune. Maybe just help us understand the market conditions, the main puts and takes that you guys are watching? And then maybe kind of how you expect the mix dynamic to play out over the coming quarters?

**Neil Hunn** (Executives):
Yes, I'll take another crack at this. So just to remind everybody, the macro, what's happening in the water meter -- the North American water meter end market, just to set that first, then we'll get into like the specific quarter and our best look at the outlook.
So what's happening is during COVID, especially in the Northeast, where the water meters are in people's basements, they cannot be sort of maintained or replaced.
So then post-COVID, '22, '23, there was a surge, there was a catch-up. Now on the backside of this, last year -- this year, for sure, we're having to sort of comp over that surge.
And so there's a -- in the industry, there are fewer meters that are being installed last year and this year versus the years before. You're kind of going from peak to trough. This isn't like a macroeconomic cycle. It's still like a COVID super cycle dynamic that the industry at large is digesting.
We talked about that in the past, but just sort of level set you and the team and everybody on that. So inside, so we're just sort of on the -- we believe we're on the tail end of that sort of reset getting into more of a normalized sort of meter market.
Now what's also happened inside of that is this mix from mechanical to static. Static meters are a better technology. They last longer. They measure -- they perfectly measure the flow of water over the life of the meter where mechanical degrades slowly over time.
So it's a better value proposition to the customer. That's why the market is generally going there because it's higher value, it carries a higher price. And so you've had this positive mix that's happened in the industry, in particular in Neptune that helped offset some of the meter declines -- macro meter declines in the market.
In the quarter, as Jason just said, there are projects, large projects, the static meter projects that pushed, which had this -- the total number of meters that Neptune sold in the quarter is actually pretty close to the expectation, but it was a dramatic mix towards mechanical, which had both a revenue implication and a margin implication.
As you just said, that likely sort of has a -- probability that normalizes in the next year. But that's sort of the setup of the mix dynamic, both the macro and the mix dynamic.
We believe over the long arc, not -- this is not a call for next year. It's like this is -- has been over our ownership, like a mid-single-digit growth business, and we think those dynamics are intact over the long arc.

**Operator** (Operator):
This concludes our question-and-answer session. I will now hand the call back to Zack Moxcey for any closing remarks.

**Zack Moxcey** (Executives):
Thanks, everyone, for joining us today, and we look forward to speaking with you during our next earnings call.

**Operator** (Operator):
Thank you. The conference has now concluded. Thank you for attending today's presentation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ROP_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜Neil Hunn｜guidance：全年調整後 DEPS 指引第二度上調，區間 22.15–22.30 美元（原話："second time this year to a range of $22.15 to $22.30."）
- 2026-07-23｜Neil Hunn｜guidance：全年營收成長指引上調：總營收 8% 以上、有機約 6%（有機數字在同句後段）（原話："guidance to north of 8%, with organic revenue growth"）
- 2026-07-23｜Neil Hunn｜guidance：Q3 調整後 DEPS 指引 5.75–5.80 美元（原話："we're establishing adjusted DEPS guidance of $5.75 to $5.80."）
- 2026-07-23｜Neil Hunn｜guidance：指引不含 Indicor 出售儀器業務的收益（原話："excludes any proceeds from Indicor's divestiture of its"）
- 2026-07-23｜Neil Hunn｜guidance：應用軟體下半年有機成長預期為中個位數偏上（原話："to be in the mid-single-digit plus range."）
- 2026-07-23｜Neil Hunn｜guidance：TEP 下半年有機成長預期為高個位數，Q3 較強（原話："high singles range and be a bit stronger in Q3."）
- 2026-07-23｜Jason Conley｜guidance：有機經常性營收成長預期於下半年走高（原話："organic recurring revenue growth to inflect higher"）
- 2026-07-23｜Neil Hunn｜guidance：管理層說明上調主要來自上半年已實現的表現與下半年機械性因素，仍保留審慎區間（原話："it was a lot of the increase is sort of in the bank."）
- 2026-07-23｜Jason Conley｜guidance：指引未計入 AI 帶來的實質貢獻，AI 變現屬 2027 規劃（原話："we haven't really baked in anything meaningful for AI"）
- 2026-07-23｜Jason Conley｜margin：核心 EBITDA 利潤率下滑 70bp，主因 TEP；軟體部門僅降 10bp 且含 AI 團隊投資（原話："Core EBITDA margin was down 70 basis points."）
- 2026-07-23｜Neil Hunn｜margin：TEP 利潤率下滑來自 Neptune 青銅錠投入成本通膨，以及 NDI/Verathon 耗材組合偏移（原話："Input cost pressure at Neptune, principally bronze ingot"）
- 2026-07-23｜Jason Conley｜margin：管理層預期下半年 Neptune 利潤率改善且比較基期較易（原話："we expect margin improvement at"）
- 2026-07-23｜Neil Hunn｜margin：網路軟體 EBITDA 利潤率年減 370bp 與核心利潤率微增 30bp 的落差，歸因於 Subsplash 收購與 DAT/Convoy 投資（原話："The gap reflects 2 dynamics: the acquisition of Subsplash"）
- 2026-07-23｜Jason Conley｜margin：AI 團隊人力投資約完成一半，支出占比因先聘資深人員而更高，多數已在 Q2 基期內（原話："a lot of that is already in our second quarter base"）
- 2026-07-23｜Jason Conley｜margin：公司 AI 工具/token 支出年化已為 1 月的約 3 倍，預期年底前再上升（原話："annualized basis, about 3x since January."）
- 2026-07-23｜Neil Hunn｜customer：企業軟體毛留存率維持在 90 中段，核心訂單 TTM 成長中個位數以上（原話："retention remained strong consistently in the mid-90s."）
- 2026-07-23｜Neil Hunn｜customer：Deltek 政府承包市場：有鼓舞跡象但尚不上調展望，要看管線連續數季轉換（原話："we'd like to see the sales pipeline convert consistently"）
- 2026-07-23｜Jason Conley｜customer：Deltek Q2 受惠於一筆未納入指引的大型授權案（原話："We had mentioned a large license deal that we had not put"）
- 2026-07-23｜Neil Hunn｜customer：DAT 貨運市場出現多項改善指標，但貨量尚未回升（原話："We still need to see load volumes improve before becoming"）
- 2026-07-23｜Jason Conley｜customer：DAT 2026 年僅預期小幅受益，重點放在 2027（原話："not baking in a massive inflection up"）
- 2026-07-23｜Neil Hunn｜customer：Neptune 營收小幅年減但優於預期；表計業務預計下半年回到成長（原話："remains on track to return to growth in the second half."）
- 2026-07-23｜Jason Conley｜customer：網路軟體中 MHA 與 iPipeline 的重複性/非經常性營收偏弱，MHA 因大客戶單位經濟較低（原話："more large customers with lower unit economics, and"）
- 2026-07-23｜Neil Hunn｜customer：Procare 被形容為仍需調整的業務，正補強核心產品、市場執行與導入能力（原話："Procare remains a work in progress."）
- 2026-07-23｜Neil Hunn｜product：AI/agentic 產品發布節奏加速，管理層稱商業化曲線仍早期（原話："we're still early in the commercialization curve"）
- 2026-07-23｜Neil Hunn｜product：Vertafore 發布 Velocity 平台，首批 6 個 agentic SKU（原話："released its AI velocity platform with 6 agentic SKUs"）
- 2026-07-23｜Neil Hunn｜product：Vertafore agentic 在 5 個領域的 TAM 擴張估計約為現有市場的兩倍，6 個 SKU 僅占一小部分（原話："It's a doubling-ish of the"）
- 2026-07-23｜Neil Hunn｜product：管理層自承 TAM 數字為推測（原話："And by the way, these are informed"）
- 2026-07-23｜Neil Hunn｜product：SoftWriters AI 訂單輸入把處理時間由約 90 秒降到約 18 秒，採交易計價（原話："SoftWriters prices the solution transactionally,"）
- 2026-07-23｜Neil Hunn｜product：Procare 首個 agentic 功能（未變現）上線 4 小時內約 20% 客戶使用（原話："within 4 hours of release, I think 20% of the customer base"）
- 2026-07-23｜Neil Hunn｜product：AI 變現主要採訂閱制 agent 層加階梯式用量層級，非純用量計費；Deltek 靠上雲加價、DAT/SoftWriters 交易計價（原話："Imagine it's going to be stair step consumption."）
- 2026-07-23｜Jason Conley｜product：地面轉雲端遷移持續推進；Deltek Costpoint 宣告停止支援舊版（原話："they actually just end of life on"）
- 2026-07-23｜Neil Hunn｜risk：客戶採用速度是最大未知數，近期變現規模無法具體說明（原話："pace of adoption at the customer level? That's the unknown."）
- 2026-07-23｜Neil Hunn｜risk：AI 產品 2026 年下半年不會形成實質營收（原話："So will it be material revenue in the"）
- 2026-07-23｜Neil Hunn｜risk：開發策略由方法化低風險轉向高速、容許部分失敗（原話："if we miss on a few, that's okay"）
- 2026-07-23｜Neil Hunn｜competition：管理層主張垂直軟體護城河：領域專長、嵌入式工作流、獨有資料、信任與配銷（原話："deep domain expertise, embedded customer workflows, unique"）
- 2026-07-23｜Neil Hunn｜competition：Aderant 定位為法律「事務所營運」(ERP/計費)，而非 Harvey 等「執業」AI；市占由 35% 升至 65%（原話："Aderant is all about the business of law."）
- 2026-07-23｜Neil Hunn｜competition：法律計費模式轉向固定費用的採用度目前仍偏低（原話："relatively low uptake across the industry."）
- 2026-07-23｜Neil Hunn｜competition：管理層稱自家 AI 產品進度領先私募買家持有的標的，但對方在追趕（原話："we're ahead on the product side versus the sponsors"）
- 2026-07-23｜Jason Conley｜capital_allocation：Q2 以約 12 億美元、均價約 341 美元回購 360 萬股，8 個月累計 32 億美元（原話："3.6 million of shares for $1.2 billion"）
- 2026-07-23｜Jason Conley｜capital_allocation：淨負債/EBITDA 由 3.1x 升至 3.4x，循環信貸已動用 29 億美元（原話："We exited the second quarter at 3.4x net debt to EBITDA"）
- 2026-07-23｜Jason Conley｜capital_allocation：Indicor 儀器業務出售予 AMETEK，預估稅前約 14 億、稅後約 12 億美元，下半年close（原話："approximately $1.4 billion or an estimated $1.2 billion"）
- 2026-07-23｜Jason Conley｜capital_allocation：年化資本部署能力超過 50 億美元（原話："more than $5 billion of annualized capacity for capital"）
- 2026-07-23｜Neil Hunn｜capital_allocation：管理層稱過去 8 個月因股價水準回購轉為顯著較有吸引力，此前數學一向偏向 M&A（原話："the capital allocation mathematically always favored"）
- 2026-07-23｜Neil Hunn｜capital_allocation：上半年除回購外僅兩筆小型併購，合計約 5,000 萬美元（原話："Well, outside the buyback, there are 2 small bolt-ons."）
- 2026-07-23｜Neil Hunn｜capital_allocation：併購策略：買贏家，不做買進後修復（原話："We're going to buy the winners and make them better."）
- 2026-07-23｜Neil Hunn｜capital_allocation：賣方（私募）估值預期鬆動，管理層看到自營機會增加，但預期不會短期內大爆發（原話："the new 15 is yesterday's 25"）
- 2026-07-23｜Neil Hunn｜commitment：未來 12–18 個月審慎樂觀部署 50 億美元以上於併購（原話："cautiously optimistic about deploying $5 billion"）
- 2026-07-23｜Neil Hunn｜commitment：近期資本部署偏向去槓桿而非機會性回購（敘事由前兩季大量回購轉向）（原話："near-term capital deployment will favor deleveraging over"）
- 2026-07-23｜Jason Conley｜commitment：預期 M&A 活動於今年稍後及 2027 年啟動，並先整備資產負債表（原話："We expect M&A activity to break loose later this year"）
- 2026-07-23｜Neil Hunn｜commitment：資本配置框架不變，以每股現金流長期複利為目標（原話："our capital allocation framework remains unchanged."）

### 問答異常語氣（迴避／改口／保留）
- ROP_Q2_2026_Earnings_Call_20260723.md｜問：Tillman：這些 agentic 產品何時能進入大規模生產工作負載（下半年？）｜答法：未給時點，改談學習曲線與組織動能；僅明確表示今年不會有實質營收，採用速度為「大未知數」
- ROP_Q2_2026_Earnings_Call_20260723.md｜問：Jester：2027 年 AI 變現上行空間有多大｜答法：明言不給 2027 變現金額，稱在客戶採用訊號更清楚前「unfortunately vague」
- ROP_Q2_2026_Earnings_Call_20260723.md｜問：Tilton：指引中還剩多少保守成分｜答法：未量化，僅稱仍有結果區間，要保持審慎以便全年強勢收尾

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
{"date":"20260710","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"VMS 護城河（工作流鎖定+合規+專有資料）抵禦 AI 通用化，組織不被侵蝕","columns":{"2Y 驗證點":"合併有機成長維持 5-6%、旗艦淨留存 ≥93%","5Y 驗證點":"留存 ≥90%、無旗艦垂直被 AI-native 對手系統性搶客","10Y 驗證點":"核心垂直仍為該行標準系統，AI 為加值層非替代","數字門檻":"旗艦淨留存 ≥90%;合併有機 ≥5%","來源":"公司法說（Q1 2026）+ 產業（Gartner 垂直 AI）","漂移觸發":"連 2 季 TTM 有機 &lt;4% → 削弱"}},{"id":"H2","text":"M&A 飛輪持續：大型 Tier-1 交易 cash-on-cash 維持約雙位數，不向 WACC 崩塌","columns":{"2Y 驗證點":"年度部署 ~$2-4B，揭露交易 ROIIC ≥ WACC","5Y 驗證點":"累積 M&A 增量 NOPAT/投入 ≥ 10-12%","10Y 驗證點":"飛輪未被「越來越貴的下一筆」吃掉；槓桿 ≤3x","數字門檻":"大型交易 ROIIC ≥ ~10%;ND/EBITDA ≤3x","來源":"公司揭露 + 賣方（PE 出價競爭）","漂移觸發":"年度 ≥2 筆大型交易出價落敗，或揭露 ROIIC &lt; WACC → 削弱"}},{"id":"H3","text":"市場對「高品質軟體 vs 中速槓桿 rollup」的重定性部分修復（15x → ~17-18x fwd）","columns":{"2Y 驗證點":"Fwd P/E 回升至 ≥16x","5Y 驗證點":"倍數穩定於 17-19x（peer/自身歷史下緣）","10Y 驗證點":"不再被永久打「conglomerate 折價」","數字門檻":"Fwd P/E ≥16x 且 EPS 兌現","來源":"賣方目標價（median $456）+ 同業（CSU 17.5x）","漂移觸發":"Fwd P/E 至 2027 仍困 &lt;13x → 反轉（永久重定性）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI-native 垂直軟體挑戰者（Onit/Applied Systems/新創潮）在旗艦垂直搶客 → 留存/定價侵蝕","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"旗艦淨留存、法律/保險垂直份額","警戒閾值":"任一旗艦淨留存 &lt;90% 或公開丟標竿客戶"}},{"id":"R2","text":"Deltek/GovCon 結構性永久降速（DOGE、聯邦採購凍結）+ DAT 貨運長弱","columns":{"對應假設":"H1","時間尺度":"🔥 中期（已跨 2025-26）","監測指標":"Deltek/DAT 有機成長、聯邦撥款能見度","警戒閾值":"Deltek 有機至 FY2026 底仍為負且無回穩"}},{"id":"R3","text":"大型 Tier-1 M&A 被 PE dry powder 抬價 → cash-on-cash 向 WACC 收斂；槓桿見頂限制飛輪","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"交易 ROIIC、ND/EBITDA、出價落敗次數","警戒閾值":"年度 ≥2 筆大交易落敗，或揭露 ROIIC &lt; WACC，或 ND/EBITDA &gt;3.5x"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼觸發：站回 W104（~$483）或連 2 季有機成長 ≥5% 且 Deltek/DAT 回穩→加碼；跌至 ~$310 且留存率/毛利未損→逢低加碼。","irr_base_pct":11.5,"ev5y_pct":70.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"B","val":"🟡","ma":"❌","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":6.4,"ev5y_pct":70.0,"irr_base_pct":11.5,"max_dd_pct":-42.0,"bull_5y_price":886.0,"bear_5y_price":270.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"加碼觸發：站回 W104（~$483）或連 2 季有機成長 ≥5% 且 Deltek/DAT 回穩→加碼；跌至 ~$310 且留存率/毛利未損→逢低加碼。","price_at_dd":355.94,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROP_20261024/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
