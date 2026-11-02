你是 stock-analyst **v20 判斷 agent**，標的 AMKR（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"AMKR","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMKR_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMKR_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":1991,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司 IR 新聞稿 ir.amkor.com Q3 2026 press release（8-K Ex.99.1）"},"note":"未查證"},{"id":"f_kpi1_gross_margin","label":"Gross margin","value":18.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司 IR 新聞稿 ir.amkor.com Q3 2026 press release"},"note":"未查證"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":224.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","unit":"百萬美元（利益率 11.3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司 IR 新聞稿 ir.amkor.com Q3 2026 press release"},"note":"未查證"},{"id":"f_kpi3_non_gaap_operating_incom","label":"Non-GAAP operating income","value":null,"period":"Q3 2026（公告於 2026-10-26）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（公告於 2026-10-26）","citation":"公司 IR 新聞稿：公司不揭露 non-GAAP 營業利益，僅揭露 EBITDA $435M（Q2 $400M、Q3 2025 $340M）"},"note":"n/a","needs_sonnet":true},{"id":"f_kpi4_diluted_eps_gaap","label":"Diluted EPS (GAAP)","value":0.76,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司 IR 新聞稿 ir.amkor.com Q3 2026 press release"},"note":"未查證"},{"id":"f_kpi6_management_guidance_q4_2","label":"Management guidance Q4 2026","value":"營收 $1.9–2.0B；毛利率 18.0–19.0%；淨利 $160–185M；EPS $0.65–0.75；營業費用約 $140M；全年 capex 約 $2.5B","period":"Q4 2026 指引（公告於 2026-10-26）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q4 2026 指引（公告於 2026-10-26）","citation":"公司 IR 新聞稿＋Q3 2026 法說會逐字稿"},"note":"FY1 EPS 共識 2.50（dd_numbers_extra consensus_revision，2026-10-31 快照）；Q4 單季共識未查證"},{"id":"f_kpi7_advanced_products","label":"Advanced products 營收","value":1632,"period":"Q3 2026（公告於 2026-10-26）","unit":"百萬美元（占 82.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（公告於 2026-10-26）","citation":"公司 IR 新聞稿 ir.amkor.com Q3 2026 press release"},"note":"n/a"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-26","period":"2026-10-26","unit":"date","basis":"距今 6 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-26"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_amkr_gross_margin_pct","label":"AMKR 毛利率","value":16.56,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMKR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amkr_operating_margin_pct","label":"AMKR 營業利益率","value":9.51,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMKR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amkr_fcf_margin_pct","label":"AMKR FCF 利潤率","value":-2.09,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMKR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_3711_tw_gross_margin_pct","label":"3711.TW 毛利率","value":20.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3711.TW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_3711_tw_operating_margin_pct","label":"3711.TW 營業利益率","value":11.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3711.TW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_3711_tw_fcf_margin_pct","label":"3711.TW FCF 利潤率","value":-11.29,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3711.TW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_6239_tw_gross_margin_pct","label":"6239.TW 毛利率","value":19.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6239.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6239_tw_operating_margin_pct","label":"6239.TW 營業利益率","value":12.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6239.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6239_tw_fcf_margin_pct","label":"6239.TW FCF 利潤率","value":-9.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6239.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2449_tw_gross_margin_pct","label":"2449.TW 毛利率","value":38.31,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2449.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2449_tw_operating_margin_pct","label":"2449.TW 營業利益率","value":26.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2449.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2449_tw_fcf_margin_pct","label":"2449.TW FCF 利潤率","value":-32.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2449.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_600584_ss_gross_margin_pct","label":"600584.SS 毛利率","value":15.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.600584.SS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_600584_ss_operating_margin_pct","label":"600584.SS 營業利益率","value":7.15,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.600584.SS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_600584_ss_fcf_margin_pct","label":"600584.SS FCF 利潤率","value":-13.54,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.600584.SS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_free_cash_flow_pp_e","label":"Free cash flow（前九個月，營業現金流減 PP&E 付款，自行計算）","value":-368.5,"period":"2026 年前九個月（截至 2026-09-30，公告於 2026-10-26）；公司未揭露單季 FCF","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"2026 年前九個月（截至 2026-09-30，公告於 2026-10-26）；公司未揭露單季 FCF","citation":"公司 IR 新聞稿現金流量表：營業現金流 $868.3M、PP&E 付款 $1,236.8M"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":38.25,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-45.95,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":35.67,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.5 → 2.5）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.78 → 2.78）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.26 → 3.26）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":2.5,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.78,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.26,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-2.72,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 2.57 → 2.5（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":15.42,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝35.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":35.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.27,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝54.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":54.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.32,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝53.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":53.9,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":15.3,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 2.5，分子＝快照價 38.24","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.878,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":336.08,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 2712.28、現金 2376.2（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":247.81,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":9812.34,"period":"2026-11-03","unit":"USD m","basis":"市值 9476.26 ＋ 淨負債 336.08","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":7528.43,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":8593.11,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（11 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.3,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 38.07 / W52 53.61 / W104 38.33 / W250 30.57 / W250 13週斜率 0.92%"},{"id":"f_ma_w52","label":"52 週均線","value":53.61,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":38.33,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":30.57,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.92,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 指出外包封測市場競爭激烈，地緣政治貿易緊張提高了中國業者（中國供中國）的競爭；主要對手為 ASE、JCET、Powertech，另有晶圓代工與 EMS 提供部分先進封裝，IDM 客戶亦評估自家產能。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":"The outsourced semiconductor packaging and test market is highly competitive, and geopolitical trade tensions have increased competition from Chinese firms supporting a China-for-China supply chain. We face competition from established packaging and test service providers primarily located in Asia, including ASE Technology, JCET Group and Powertech Technology.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：前十大客戶占 2025 年淨銷售 72%；亦可能面對受中國政府支持、資金成本較低的本地業者競爭，客戶可能轉用內部、晶圓代工或合約製造商。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":"Our ten largest customers accounted for, in the aggregate, 72% of our net sales for the year ended December 31, 2025.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Amkor 年度資本支出最高約 $30 億，並提及 TSMC 自建先進封裝、Amkor 與 TSMC 協議","source":"TheNextWeb: Amkor will spend up to $3bn this year","url":"https://thenextweb.com/news/amkor-q2-2026-record-revenue-capex-advanced-packaging","excerpt":"TSMC signed a ten year agreement in June covering advanced packaging in Arizona. Amkor’s Peoria plant separately received $407m under the CHIPS Act. The logic is geographic.","as_of":"2026-07-28","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Amkor Q2 2026 前十大客戶占淨銷售 66%，低於去年同期 72%","source":"Amkor Q2 2026 財報新聞稿","url":"https://amkortech.gcs-web.com/node/24566","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Apple 占 2025 年淨銷售 29.8%、Qualcomm 11.1%，前十大客戶合計 72%；IDM 客戶會拿 Amkor 服務與自家 in-house 能力比較。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":"Our ten largest customers accounted for 72% of our net sales in 2025. Direct sales to Apple and Qualcomm accounted for 29.8% and 11.1% of our net sales, respectively, for the year ended December 31, 2025.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因素載明 IDM 與晶圓代工客戶可能隨時把外包封測轉回自有產能。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":"IDMs and foundries may decide to shift some or all of their outsourced packaging and test services to internally sourced capacity.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 前十大客戶占淨銷售 72%；Apple 直接銷售占 29.8%、Qualcomm 11.1%。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":"Our ten largest customers accounted for 72% of our net sales in 2025. Direct sales to Apple and Qualcomm accounted for 29.8% and 11.1% of our net sales, respectively, for the year ended December 31, 2025.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"公司風險因子自述：失去大客戶、客戶合併、訂單或價格下降可能對業務、流動性與財務產生重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":"The loss of a significant customer, a business combination among our customers, a reduction in orders or decrease in price from a significant customer or disruption in any of our significant commercial arrangements may result in a decline in our sales and profitability and could have a material adverse effect on our business, liquidity, results of operations, financial condition and cash flows.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Omdia expects AI-driven constraints in making and packaging advanced chips to last until at least 2027, with packaging costs continuing to rise.","source":"Cyprus Mail citing Omdia, AI bottlenecks set to continue until 2027","url":"https://cyprus-mail.com/2026/08/10/ai-boom-drives-record-semiconductor-revenue-forecast","excerpt":null,"as_of":"2026-08-10","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"TrendForce: TSMC CoWoS supply-demand gap reportedly narrowing from ~20% to ~10% by end-2026 as capacity expands; further improvement likely in 2027.","source":"TrendForce News 2026-06-15","url":"https://www.trendforce.com/news/2026/06/15/news-tsmc-cowos-supply-demand-gap-reportedly-seen-narrowing-from-20-to-10-by-end-2026-as-capacity-expands","excerpt":null,"as_of":"2026-06-15","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Amkor management expects 2.5D and HDFO platforms to roughly triple in 2026; 2026 capex $2.5-3B; Q3 call described favorable pricing supported by limited advanced packaging capacity.","source":"Zacks/Nasdaq Amkor earnings call summaries","url":"https://www.zacks.com/stock/news/3015520/amkor-q3-earnings-call-highlights-ai-growth-and-capacity-expansion","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Amkor consumer/Android weakness: Android revenue declined 20% in Q2; Q3 outlook affected by SiP migration to Vietnam, memory supply constraints and customer build changes.","source":"Zacks/Nasdaq Amkor earnings call summaries","url":"https://www.nasdaq.com/articles/amkor-eyes-strong-second-half-2026-ai-hpc-packaging-demand-surges","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SEMI July 2026 mid-year forecast: equipment sales $165.9B in 2026 rising to record $229.5B in 2028; WSTS Spring 2026 forecast ~$1.9T chip market in 2027 (~27% growth).","source":"SEMI press release; telecomlead on WSTS","url":"https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-forecast-to-reach-a-record-229-billion-dollars-in-2028-semi-reports","excerpt":null,"as_of":"2026-07-14","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K FY2025 的政府法規章節指出，法規遵循成本目前對資本支出、營運結果與競爭地位不重大，且預期無重大合規支出；搜尋未發現 2026 年反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 1 Governmental Regulations","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":"Costs and accruals incurred to comply with these governmental regulations are presently not material to our capital expenditures, results of operations and competitive position.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因素列出出口管制（BIS 規則）限制對部分中國公司銷售，屬產業特定貿易監管。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":"These expanded export restrictions limit our ability to sell to certain Chinese companies and to third parties that do business with those companies.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：Amkor 在中國、日韓、馬來西亞、菲律賓、葡萄牙、新加坡、台灣、越南設廠，客戶與供應商多在美國境外；公司稱美中關係與貿易政策變動、關稅、出口管制已對並可能持續對業務造成不利影響；BIS 規則限制先進運算晶片與設備出口中國，部分非美國競爭對手可能豁免。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":"Certain of the Company’s competitors may be exempt from the BIS Regulations by virtue of being non-U.S. manufacturers.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 稱 2025 年美國多次宣布關稅與出口管制變動，多數後來暫停或修訂；公司無法預測後續行動，關稅可能影響終端需求而不利於公司。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":"We cannot predict what further actions may ultimately be taken by the U.S. with respect to tariffs, export restrictions or other trade measures, what products or entities may be subject to such actions, or what actions may be taken by other countries in response to these U.S. actions.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"MD&A：公司持續監控全球貿易政策，關稅影響取決於不確定的未來發展。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":"The degree to which such tariffs and other related actions impact our business, financial condition and results of operations will depend on future developments, which are uncertain.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 競爭段：地緣貿易緊張提高了支援中國在地供應鏈的中國同業競爭。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":"geopolitical trade tensions have increased competition from Chinese firms supporting a China-for-China supply chain.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Amkor 封測廠分布於中國、日本、韓國、馬來西亞、菲律賓、葡萄牙、新加坡、台灣、越南，亞洲為主；美國亞利桑那廠仍在興建中","source":"Amkor Form 10-Q (Q1 2026)","url":"https://www.sec.gov/Archives/edgar/data/0001047127/000104712726000020/amkr-20260331.htm","excerpt":"Amkor has significant packaging and test services and other operations in China, Japan, Korea, Malaysia, the Philippines, Portugal, Singapore, Taiwan and Vietnam, and the Arizona Facility is a new factory under construction in the United States.","as_of":"2026-03-31","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"10-Q 稱全球佈局可能讓 Amkor 將產能轉移至其他廠而無重大成本或延誤，但部分服務依賴僅一或少數據點的設備（單點風險）","source":"Amkor Form 10-Q (Q1 2026)，經搜尋摘要轉述","url":"https://www.sec.gov/Archives/edgar/data/0001047127/000104712726000020/amkr-20260331.htm","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 指出幾乎所有不動產、廠房與設備位於美國以外，並列示地緣緊張、保護主義導致出口限制與關稅","source":"Amkor Form 10-K FY2025（搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險因素：中國營運風險因美中關係與貿易政策而可能升高","source":"Amkor Form 10-K FY2023","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712724000019/amkr-20231231.htm","excerpt":null,"as_of":"2024-02-28","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 Computing 與 Automotive & Industrial 年增各 37% 創單季新高；Communications 年減 28%（SiP 專案由韓國轉越南時程）；Consumer 季增 10%；Q4 指引營收 $1.9–2.0B","source":"Amkor 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001047127/000104712726000052/amkr-20260930.htm","excerpt":"computing and automotive and industrial end markets both grew 37% for the three months ended September 30, 2026 compared to 2025, primarily due to strength in datacenter and ADAS applications. The communications end market decreased 28% for the three months ended September 30, 2026 compared to 2025, primarily driven by timing for transfer of SiP programs from our factories in Korea to Vietnam","as_of":"2026-10-26","retrieved_at":"20261103","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 財報新聞稿：Computing 與 Automotive & Industrial 創紀錄，Communications 疲弱；Q4 毛利率指引 18.0–19.0%","source":"Amkor 8-K Ex.99.1 Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0001047127/000104712726000049/amkr9302026erex-991.htm","excerpt":"“Amkor delivered a strong quarter, with record revenue in Computing and Automotive & Industrial end markets and continued margin expansion, despite expected weakness in Communications,” said Kevin Engel, Amkor’s president and chief executive officer.","as_of":"2026-10-26","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"法說會：預期 2027 年 Computing 營收成長超過 30%，兩個新 2.5D 專案（網通、資料中心）自 Q4 起","source":"Amkor Q3 2026 Earnings Call Transcript (Webull)","url":"https://www.webull.com/news/15818016757633024","excerpt":"Computing Growth Outlook -- 30% or more for 2027, driven by data center ramps and new 2.5D programs in networking. Top Ten Customer Concentration -- 66% of net sales, representing a decline from 73% in the third quarter of 2025.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Onto Innovation Q2 2026：2026 先進封裝成長展望上調至約 80%（原 50%），受 HBM 與 OSAT 量能帶動","source":"Nasdaq: ONTO Q2 Earnings Call Highlights Packaging Strength Into 2027","url":"https://www.nasdaq.com/articles/q2-earnings-call-highlights-packaging-strength-2027","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"Hudson Labs：客戶願接受漲價以抵銷成本通膨；風險含基板／先進矽材料成本壓力；ASE 規模較大、TSMC 自建封裝為競爭壓力","source":"Hudson Labs AMKR Q2 2026 Earnings Preview Memo","url":"https://www.hudson-labs.com/research/amkr-q2-2026-earnings","excerpt":">30% gross margin at scale (~$1B revenue run-rate per phase). On Supply Chain and Risks Supply constraints: Memory, advanced silicon, and substrate supply remain tight; management is prioritizing production where materials are available. Pricing: Constructive environment; customers showing willingness to accept price increases to offset cost inflation.","as_of":"2026-07-08","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"+","claim":"TSMC 報導擴大把 CoW 前段步驟外包給 OSAT，OSAT 參與度取決於 TSMC 立場","source":"TrendForce News 2026-08-05","url":"https://www.trendforce.com/news/2026/08/05/news-tsmc-reportedly-expands-outsourcing-of-key-cowos-front-end-step-to-osats-amid-rising-nvidia-asic-demand/","excerpt":"#Foundry #AI Server #HBM #FOPLP #CoWoS #NAND Flash #Automotive #MLCC #Server #Micro LED #IC Design About TrendForce News TrendForce News operates independently from our research team, curating key semiconductor and tech updates to support timely, informed decisions. Home News [News] TSMC Reportedly Expands Outsourcing of Key CoWoS Front-End Step to OSATs Amid Rising NVIDIA, ASIC Demand","as_of":"2026-08-05","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Amkor 主管稱玻璃基板（Intel 主導）三年內可商業化，Amkor 為 Intel 合作夥伴","source":"Wccftech","url":"https://wccftech.com/intel-backed-glass-substrates-tech-will-be-commercilization-ready-within-three-years/amp/","excerpt":"Intel-Backed “Glass Substrates” Tech Will Be Ready For Commercialization Within Three Years, Says Amkor Lead Hassan Mujtaba • Apr 28, 2026 at 11:20am EDT Add Wccftech on Google Comments Amkor says that Glass Substrates, a packaging technology replacement for CoWoS spearheaded by Intel, is set for commercialization within 3 years.","as_of":"2026-04-28","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Amkor 2026 投資人簡報稱客戶合作改為更早期設計參與、規劃期拉長為多年、客戶承諾提升能見度；Q1 2026 法說稱客戶出資協助對齊技術路線與擴產","source":"Amkor 2026 investor presentation (SEC 8-K ex-99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001047127/000104712726000036/ex-991amkorinvestorprese.htm","excerpt":"Strategy to Deliver Shareholder Value Partnerships evolving with earlier design engagement Planning horizons are becoming multi-year Commitments improve visibility and predictability An intentionally built footprint to support regional delivery Arizona facility increases","as_of":"2026-06-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"公司 Q4 2026 guidance：營收 $1.9–2.0B、毛利率 18.0–19.0%、淨利 $160–185M（EPS $0.65–0.75）","source":"Amkor 8-K Ex.99.1 Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001047127/000104712726000049/amkr9302026erex-991.htm","excerpt":"Net sales of $1.9 billion to $2.0 billion","as_of":"2026-10-26","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 2026 發布前市場共識約 Q3 $2.04B、Q4 $2.05B；Q4 guidance 區間 $1.9–2.0B 低於該共識（搜尋摘要轉述，未核原文）","source":"WebSearch 摘要（finviz/Business Wire 等）","url":null,"excerpt":null,"as_of":"2026-10-26","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 2026-07 平均評等 Moderate Buy、共識目標價 $69.25；其他聚合站 $76–82.5 不等，差異大（Walnut 範圍 $65–92，截至 2026-08）；皆為 Q3 財報前資料","source":"MarketBeat Q3 2026 guidance 文章；Walnut；Stockhub","url":"https://www.marketbeat.com/instant-alerts/amkor-technology-nasdaqamkr-issues-q3-2026-earnings-guidance-2026-07-27/","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"UBS 升評 Buy 目標價 $90（原 $80）；B. Riley 降至 $75 中立；Morgan Stanley 升至 $70 Equal Weight","source":"stockanalysis.com AMKR","url":"https://stockanalysis.com/quote/bmv/AMKR/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-05-05 發行 11.5 億美元 0.00% 2031 年到期可轉債（含 1.5 億美元超額配售），屬融資事件，非併購。","source":"SEC EDGAR 8-K Item 1.01（2026-05-05）","url":"https://www.sec.gov/Archives/edgar/data/1047127/000104712726000029/amkr-20260430.htm","excerpt":"On May 5, 2026, Amkor Technology, Inc. (the “Company”) issued $1,150,000,000 aggregate principal amount of its 0.00% Convertible Senior Notes due 2031 (the “Notes”).","as_of":"2026-05-05","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 12 份 8-K 中重大項目 4 份；清單內可見項目為可轉債（1.01/2.03/3.02/8.01）與董事／高管異動（5.02），清單未列 2.01 併購完成、4.02 重編。","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001047127&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 12 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"ASE 2026 為最積極的建廠年，全球六座新封測廠同時動工（美、馬、日、德、高雄）；資本支出報導自約20億美元升至2025年53億、2026年85億美元，2027年預期仍高。","source":"TrendForce News, ASE targets FOPLP mass production by end-2026, launches 15 expansion projects","url":"https://www.trendforce.com/news/2026/06/25/news-ase-targets-foplp-mass-production-by-end-2026-launches-15-expansion-projects-this-year-amid-ai-boom/","excerpt":null,"as_of":"2026-06-25","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Amkor 2026 capex 指引 25-30 億美元，65-70% 用於廠房擴建（含亞利桑那 Phase 1），其餘為 HDFO、測試等先進封裝產能；Q3 摘要稱全年收斂至約 25 億。","source":"Amkor Q4 2025 earnings call summary (Yahoo Finance) / Zacks Q3 call summary","url":"https://finance.yahoo.com/news/amkor-technology-q4-earnings-call-233617219.html","excerpt":null,"as_of":"2026-02-09","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Amkor 亞利桑那 Phase 1 預計 2027 年中完工、2028 年初量產；2027 年廠房擴建支出仍高（韓國建設 4-4.5 億美元、越南 0.5 億）。","source":"Amkor Technology Q3 2026 earnings call transcript (Webull) / Q1 2026 10-Q","url":"https://www.webull.com/news/15818016757633024","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["triggers","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"ASE 2026 capex 上調 20 億至約 105 億美元，設備 65 億中約 70% 用於先進製程","source":"eu.36kr.com","url":"https://eu.36kr.com/en/p/3899029791623044","excerpt":"of advanced packaging capacity driven by the demand for high-end CoWoS. A large number of OSAT manufacturers are also increasing their efforts in layout. According to industry insiders, ASE is currently in the largest factory expansion cycle in the company's history. CEO Wu Tianyu revealed that in 2026, six new packaging and testing plants of ASE around the world will start construction","as_of":"2026-07-17","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"ASE 據報於 2026-07 將先進封裝報價調升 20% 以上（產業消息，非官方聲明），OSAT 價格趨勢向上、產能吃緊","source":"Silicon Analysts: ASE Advanced Packaging Quotes Surge 20%+","url":"https://siliconanalysts.com/market/ase-advanced-packaging-quotes-surge-20-amid-ai-driven-demand-crunch-2026-07-02","excerpt":null,"as_of":"2026-07-02","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Amkor 帳上存貨 2026Q2 約 $560.7M，較 Q1 $494.6M 季增約 13%、年增約 49%（聚合站數據，未核對 10-Q）","source":"businessquant.com AMKR Inventory","url":"https://businessquant.com/metrics/amkr/inventory","excerpt":"Amkor Technology (AMKR) posted Inventory of $560.7 million for Q2 2026, up 13.36% sequentially from $494.6 million in Q1 2026.","as_of":"2026-07-28","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"廣發證券預期 ASE 2026Q3-Q4 FC/wirebond/QFN 價格上漲 10%–80%，CoWoS 相關 10–20%","source":"TechNews 2026-10-21","url":"https://finance.technews.tw/2026/10/21/we-are-optimistic-about-the-accelerated-growth-of-ase-technology-holdings-advanced-packaging-and-testing-business/","excerpt":"廣發證券預期，受惠於供給緊繃，日月光在2026年第三季至第四季間，FC/Wirebond/QFN封裝價格將上漲10%至80%，CoWoS價格亦有10%至20%的調漲空間。 日月光的先進封測（LEAP）業務正急劇升溫，主要驅動力來自超微（AMD）伺服器CPU（如Venice與Verano）全面導入CoWoS技術，加上主要競爭對手擴產速度慢於預期。","as_of":"2026-10-21","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"SOX 歷史 5 次回撤 30%~82% 含復原資料（部落格彙整，非權威）","source":"quantflowlab: Semiconductor cycle history showing 5 SOX drawdowns from 30% to 82%","url":"https://quantflowlab.com/?p=936","excerpt":"Fastest Recovery Mar 2020 low → Jun 2020 2.6 months Trough to prior peak Long-Run Sales Global semiconductor revenue $139B → $795.6B 2001 → 2025 revised, both actual (SIA) §1 — The Computed Record Seven Completed Drawdown Episodes","as_of":"2026-03-28","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Amkor Q3 2024 毛利率 14.6%（去年同期 15.5%），Q4 指引 13.5%~15.5%，股價跌 8.8%","source":"itiger: Stock Track | Amkor Technology Plunges 8.8% as Q4 Guidance Disappoints","url":"https://itiger.com/news/1190429689","excerpt":"Additionally, Amkor expects gross margin of 13.5% to 15.5% and net income of $70 million to $110 million, or $0.28 to $0.44 per diluted share, suggesting further declines in profitability compared to Q3 2024 and the year-ago period.","as_of":"2024-10-29","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"8-K 清單（2025-11-03至2026-11-03）未列 Item 2.01 併購完成項目；唯一協議類為可轉債 Item 1.01。","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001047127&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 12 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"AMKR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":16.56,"operating_margin_pct":9.51,"fcf_margin_pct":-2.09,"rd_intensity_pct":2.12},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMKR","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"3711.TW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":20.81,"operating_margin_pct":11.47,"fcf_margin_pct":-11.29,"rd_intensity_pct":5.04},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3711.TW","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"6239.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.12,"operating_margin_pct":12.9,"fcf_margin_pct":-9.7,"rd_intensity_pct":3.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6239.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"2449.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.31,"operating_margin_pct":26.86,"fcf_margin_pct":-32.27,"rd_intensity_pct":2.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2449.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"600584.SS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.83,"operating_margin_pct":7.15,"fcf_margin_pct":-13.54,"rd_intensity_pct":5.21},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.600584.SS","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"AMKR"},"financial_history":{"ticker":"AMKR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":7091585000.0,"revenue_yoy_pct":null,"gross_margin_pct":18.75,"operating_margin_pct":12.65,"net_income":765823000.0,"diluted_eps":3.11,"free_cash_flow":190462000.0,"fcf_margin_pct":2.69,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":6503065000.0,"revenue_yoy_pct":-8.3,"gross_margin_pct":14.5,"operating_margin_pct":7.23,"net_income":359813000.0,"diluted_eps":1.46,"free_cash_flow":520553000.0,"fcf_margin_pct":8.0,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":6317692000.0,"revenue_yoy_pct":-2.85,"gross_margin_pct":14.77,"operating_margin_pct":6.94,"net_income":354012000.0,"diluted_eps":1.43,"free_cash_flow":345072000.0,"fcf_margin_pct":5.46,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":6707981000.0,"revenue_yoy_pct":6.18,"gross_margin_pct":13.99,"operating_margin_pct":6.97,"net_income":373895000.0,"diluted_eps":1.5,"free_cash_flow":190992000.0,"fcf_margin_pct":2.85,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/AMKR/AMKR_Q3_2026_Earnings_Call_20261026.md）

# Q3 2026 Earnings Call
**Amkor Technology, Inc.** | Earnings Calls | 2026-10-26

**Operator** (Operator):
Good day, ladies and gentlemen, and welcome to the Amkor Technology Third Quarter 2026 Earnings Conference Call. My name is Diego, and I will be your conference facilitator today. [Operator Instructions] As a reminder, this conference is being recorded.
I would now like to turn the call over to Jennifer Jue, Head of Investor Relations. Ms. Jue, please go ahead.

**Jennifer Jue** (Executives):
Good afternoon, and welcome to Amkor's Third Quarter 2026 Earnings Conference Call. Joining me today are CEO, Kevin Engel; and CFO, Megan Faust. Our earnings press release was filed with the SEC this afternoon and is available on the Investor Relations page of our website, along with the presentation slides that accompany today's call.
During this presentation, we will use non-GAAP financial measures, and you can find reconciliation to the comparable GAAP financial measures in the slides. We will make forward-looking statements today based on our current beliefs, assumptions and expectations. Please refer to our press release for a disclaimer on forward-looking statements and our SEC filings for a discussion on the risk factors and uncertainties that may affect our future results.
I will now turn the call over to Kevin.

**Kevin Engel** (Executives):
Thank you, Jennifer. Good afternoon, everyone, and thanks for joining. Amkor delivered a strong third quarter with revenue of approximately $2 billion. For the second consecutive quarter, we achieved record revenue in both Computing and Automotive and Industrial end markets. Gross margins expanded to over 18% and operating margins increased to over 11%. These results reflect continued execution against our strategy and demonstrate the improving earnings power of our business. On a year-on-year basis, revenue in the third quarter continued to accelerate in Computing and Automotive and Industrial with both end markets growing 37%. In Computing, demand remained robust and our flagship HDFO CPU program ramped throughout the quarter. Automotive and Industrial continue to benefit from strong demand for advanced in-car computing applications such as ADAS and infotainment.
Now let me share an update on our 3 strategic pillars. First, enhancing strategic partnerships in key markets. Customers are engaging earlier, aligning technology road maps and making longer-term commitments as advanced packaging becomes increasingly critical to AI and high-performance computing. We continue to see a shift in how customers support capacity expansions. Customers are not only planning further ahead, but are also making long-term commitments and providing advance payments tied to future capacity requirements. This gives us confidence as we accelerate our capital spending above historical norms. We believe this reflects a broader change in our industry. These commitments reflect our customers' confidence in their long-term advanced packaging requirements and in Amkor's ability to support their product road maps. For Amkor, these agreements improve visibility, strengthen alignment with our customers and support disciplined investment in advanced packaging capacity as our global footprint increases, including Arizona and our Asia facilities.
The second pillar is elevating technology leadership. Customer engagements remain strong across our advanced packaging platforms and our pipeline continues to broaden. The progress we are making across our HDFO and 2.5D programs continues to reinforce positive outlook for the long-term growth opportunities in Computing. Our flagship HDFO CPU program is scaling. An additional HDFO CPU program for a hyperscaler began ramping in Q3 and 2 new 2.5D programs in networking and data center are expected to come online in Q4. Customer engagement is particularly strong in next-generation AI infrastructure with additional advanced packaging opportunities developing across traditional data center, PC applications and automotive. Advanced packaging is on the critical path of system performance.
As customers push for greater performance, higher bandwidth and improved power efficiency, packaging technology is playing a larger role in enabling product road maps. As a result, customer discussions today are broader than they were just a few years ago. We are increasingly engaged in architectural design, technology road maps and test strategy along with long-term capacity planning. Our turnkey model allows us to integrate advanced packaging and test capabilities, providing customers with more complete solutions. This strengthens our competitive position, deepens customer relationships and creates additional opportunities to deliver value across the product life cycle. Taken together, the breadth of customer engagements we see today affirms our view that advanced packaging will remain a meaningful growth driver for Amkor over the coming years.
Our third pillar is expanding our geographic footprint. In September, we announced Phase 2 of our Arizona advanced packaging and test campus, which is expected to break ground in late 2027 as Phase 1 construction nears completion. Together, both phases are planned to be over 90,000 square meters of clean room space and represent an estimated investment of $12 billion. When fully ramped, the campus is expected to support a workforce of over 3,500 employees, strengthening the U.S. semiconductor ecosystem and support our customers' long-term needs.
In Korea, we recently broke ground on 2 new buildings on our Gwangju campus. This additional space is being built to support the continued ramp of HDFO for our data center customers, including the recent announcement with NVIDIA. On our Songdo campus, the new assembly and test building remains on schedule for completion by year-end. The incremental space is planned to expand test capacity for automotive and data center customers and strengthen our regional turnkey capabilities. Following completion of these expansions in 2028, our Korea footprint is expected to increase by 40% from 2025. This cements Korea as a center of excellence for high-value advanced packaging.
Our Vietnam build-out is also progressing as planned with increasing scale and a continued focus on automation. Automation allows for optimal space planning, higher equipment utilization and quality assurance. Our vision is for Vietnam to become our SiP center of excellence. It's been exciting to see this facility ramp from a piece of undeveloped land in 2021 to a high-tech manufacturing operation today. As we migrate SiP from Korea to Vietnam, we are opening up needed clean room space in Korea for additional advanced packaging growth. The released space in Korea is being redeployed and quickly consumed by advanced packaging customers.
In closing, our third quarter results demonstrate strong execution and continued momentum across the business. We delivered record revenue in Computing and Automotive and Industrial, expanded margins and advanced key programs. Customer commitments continue to grow, giving us greater visibility as we expand advanced packaging capacity. We are well positioned to capture long-term growth opportunities ahead.
I will now turn the call over to Megan to provide more detail on our third quarter performance and near-term outlook.

**Megan Faust** (Executives):
Thank you, Kevin, and good afternoon, everyone. Amkor delivered third quarter revenue of $1.99 billion, an increase of 5% sequentially. Our Computing and Automotive and Industrial end markets each achieved record revenue. Revenue in the Communications end market declined 8% sequentially. The factors we discussed last quarter largely developed as expected. These included the strategic migration of SiP technology to Vietnam, memory supply constraints and changes in build patterns. Component shortages affecting premium tier smartphones and IoT wearable devices created an additional headwind during the quarter across both Communications and Consumer applications. We expect these conditions to continue in the fourth quarter and for Communications revenue to decline high single digits sequentially.
Revenue in the Computing end market increased 25% sequentially to a new record. During the quarter, we continued to scale our flagship HDFO CPU program and saw growth in other data center programs. Looking ahead to the fourth quarter, we expect revenue to increase low double digits sequentially, driven by ongoing scaling and new program ramps. Q4 is estimated to result in over 50% growth year-on-year and provides strong momentum heading into 2027. Revenue in the Automotive and Industrial end market reached a new record, increasing 7% sequentially. Growth was driven by both ADAS and industrial products across multiple customers.
In the fourth quarter, we expect continued strength with revenue growing low single digits sequentially. Consumer revenue increased 10% sequentially, driven by demand for IoT and home electronic products. Revenue was impacted by the same component shortages affecting premium tier smartphones. We expect these shortages to continue in the fourth quarter with Consumer revenue declining more than seasonal into the mid-teens percent sequentially. Gross margin for the quarter was 18.3%, an increase of 150 basis points sequentially and 400 basis points year-on-year. Gross profit was $364 million.
Gross margin expansion is primarily driven by a richer mix of high-value advanced packaging, reflecting strong growth in Computing and Automotive. During the quarter, gross margin was impacted by foreign currency headwinds and to a lesser extent, the impact of the July earthquake on our Kumamoto Japan facility. Together, these factors had an unfavorable impact of approximately 60 basis points sequentially. Our Japan facility returned to full operations within the quarter.
Third quarter operating expenses were $139 million. Operating income was $225 million, resulting in operating income margin of 11.3%. Net income was $191 million, resulting in earnings per share of $0.76. EBITDA was $435 million and EBITDA margin was 21.8%. Our balance sheet remains strong and provides significant flexibility as we continue to invest to support long-term growth. As of September 30, we held $2.4 billion in cash and short-term investments and total liquidity was $3.4 billion. Total debt was $2.5 billion, and our debt-to-EBITDA ratio was 1.7x.
Now turning to our fourth quarter outlook. Q4 revenue is expected to be between $1.9 billion and $2 billion. Gross margin is expected to be between 18% and 19%. We expect operating expenses of approximately $140 million. Our full year effective tax rate is expected to be in the high teens percent due to year-to-date discrete tax benefits. Net income is forecasted to be between $160 million and $185 million, resulting in earnings per share between $0.65 and $0.75. We are narrowing our estimated 2026 CapEx spend to around $2.5 billion, primarily reflecting the timing of construction payments for our Arizona campus. Phase 1 construction remains on schedule for completion by the end of 2027.
Looking ahead, we expect a step-up in CapEx in 2027, driven primarily by facility investment in Arizona, Korea and Vietnam as we expand capacity to support our long-term growth opportunities. We will provide specific 2027 CapEx guidance on our fourth quarter call in February. Customer advance payments are expected to provide significant funding support for these CapEx investments. Since 2025, Amkor has executed advance payment arrangements with a dozen customers, primarily supporting advanced packaging capacity across both Korea and Arizona, and there are several more customer agreements under discussion.
In closing, our third quarter results demonstrate the earnings power of our business. A richer mix of advanced packaging revenue and strong execution drove meaningful margin expansion. We remain focused on disciplined investment as we position the business for profitable long-term growth.
This concludes our prepared remarks. Operator, we will now open the call for questions.

**Operator** (Operator):
[Operator Instructions] And your first question comes from Ruplu Bhattacharya with Bank of America.

**Ruplu Bhattacharya** (Analysts):
First one for Megan. You're guiding to about 20 bps of sequential gross margin improvement for the fourth quarter. How should we think about the impact of the SiP migration to Vietnam as well as weakness in the Android smartphone market and any other factors like FX or if there's any lingering issues in Japan? Can you just help us parse how you're thinking about that sequential improvement? And I have a follow-up.

**Megan Faust** (Executives):
Sure. So correct, we are going to see some modest expansion in our gross margin in Q4. That's primarily due to favorable product mix as it relates to further growth in our compute. And then I would say, lower SiP, as you had mentioned before. We are also anticipating continued unfavorable FX. As it relates to the Communications market, we've indicated in Q4 that would be down sequentially. As it relates to the dynamics between, I would say, the iOS and the Android, we do see Android being down in Q4 compared to Q3. And we also see iOS down. So we see both ecosystems down.
And did you have a follow-up?

**Ruplu Bhattacharya** (Analysts):
Yes. I had a follow-up for Kevin. So with this new announced agreement with NVIDIA, it looks like total prepayments are now about $3 billion. Kevin, how should we think about the division of programs between South Korea and Arizona? And will the margin and capital return profiles differ materially between these 2 locations? And from a risk management standpoint, if any major AI program changes, how fungible is this advanced packaging equipment? So a couple of different parts, but if you can just talk about Korea versus Arizona, the margin and capital return profiles and how you're thinking about risk management.

**Kevin Engel** (Executives):
Yes. Thanks, Ruplu. So a few components there. So when we think about the mix between Korea versus Arizona, obviously, for Korea, we're ramping today. That's obviously very important for us to continue to accelerate that ramp. There's a lot going on there. I mean, to add a little bit of color because we talked about the expansions in these locations as well.
So in Korea, obviously, as we migrate the SiP from the Korea facility over to Vietnam, that opens up space in the Korea facility and that we're quickly filling with assets that we already have on order to continue that ramp profile, I would say, short term. Then when we get to midterm, we have the new building on the Songdo campus that will be opening at the end of this year that will start to ramp to continue that acceleration. And then that announcement is also contemplating these K4 or that's our Gwangju location, where we have 2 new buildings where we recently broke ground, and those will drive the acceleration into late '27 into '28. Those buildings will be completed for construction in late '27.
To give you an idea of scale there from a spend perspective, the construction in Korea will basically for 2027 be in the $400 million to $450 million range. And then we talked about, obviously, this expansion in Vietnam, where the SiP is going in. And that expansion facility-wise for 2027 is in the $50 million range. Obviously, for Arizona, that ramp is later. Again, the facility will be completed late this year. We'll start moving assets in. So for that customer, that will be more of a 2020 -- late 2028 type ramp profile. And then when we think about gross margins for both facilities, what we -- obviously, when we think about Arizona, we do expect the overall cost to be higher related to building depreciation, labor.
We're managing that through multiple ways. Number one is keeping the factory very heavily utilized. So it will be lower product mix, higher utilization. And the customers we have planned for that facility understand that we want to reduce the seasonality, preferentially load in Arizona and then obviously offload into Asia. So that allows us to really keep that factory running at a high level. And obviously, it will be our most advanced related to automation. So that will help us from a labor perspective. So long term, while there may be some slight deltas in the margin profile, we wouldn't expect a big delta between the 2.
So I think that's a positive outlook. When we think about risk, the CAP agreements really help us from a risk profile. There's obviously multiple terms in those agreements that build confidence for us in getting that profile built. The asset fungibility, we think about any high-density fan-out program, 2.5D, even wafer bumping type things, these assets are fungible up and down that stack. Obviously, the scale that we're working with this customer is hard to offset. But I'd say, regardless, the technology is very fungible to different customers.

**Operator** (Operator):
And your next question comes from Joe Moore with Morgan Stanley.

**Joseph Moore** (Analysts):
Great. You had good results in compute, up 25%. I think you had talked about up 30% when you reported last quarter. So can you just talk about -- I assume that's sort of more constraints on the supply side, but can you give us some indication of that trajectory and any nuance there?

**Kevin Engel** (Executives):
Yes. I wouldn't necessarily say supply side actually, Joe. It's more related to -- you have to kind of imagine this process flow for these HDFO parts. This is over 300 steps in the process. So to build out that pipeline, get the product in the right locations, I think we talk a lot about WIP loading to get that built into that whole chain with multiple steps takes time. So I'd say we were -- it took a little bit longer to really load the line to the level we wanted to. I wouldn't say anything related to supply constraints.

**Joseph Moore** (Analysts):
Okay. That's helpful. And then also on the end market mix, it looked like you had some strength in Automotive. Any sense of what you're seeing in that part of the market?

**Kevin Engel** (Executives):
Yes. Thanks for that question. I wasn't sure that was going to come up today. But I'd say Automotive and Industrial are actually very, very positive on that. There's a few things. For Automotive, the advanced products, again, think in-car computing, ADAS, all those applications are continuing to grow for us, and that's a really exciting area. If you think about how the automotive industry has changed over the few years, it used to take years to develop a product, get it into a car. That's really accelerating. And so the advancement of new technologies in cars is going much more aggressively than we've seen in the past, which benefits these advanced packages.
Think about Arizona in general, where we have a lot of autonomous cars, the amount of semiconductor content in these vehicles is really increasing as that continues to proliferate down into passenger cars. We obviously will continue to see semiconductor content per car growing. And then in addition to that, the mainstream legacy-type packages going into cars are also rebounding. I'd say our customers, it's nice to hear them talk about their positive outlooks, inventory being under control, where that's taken years to get to that level. So that's all boding well. And then I don't want to leave out Industrial. Industrial, we also see some pretty significant growth there. So all 3 of those areas, we've seen positive momentum.

**Operator** (Operator):
Your next question comes from Ben Reitzes with Melius Research.

**Jack Adair** (Analysts):
This is Jack Adair on for Ben. I wanted to dive deeper into the Computing segment. You had guided Computing to be up over 50% year-over-year in 4Q. Could you talk more about the momentum into 2027 with more capacity coming online in Korea and more data center engagements ramping? And if that pace can continue in 2027?

**Kevin Engel** (Executives):
Yes. Thanks for the question. Yes. I mean, so basically, with our guide, we're expecting over 30% growth in Computing from 2025 to 2026. Again, keep in mind, that encompasses PC as well as data center. PC is relatively soft, but data center has offset that, and that's really what's driving this over 30% growth. We would expect a similar growth rate to even higher growth rate into 2027, again, based on that space profile that I outlined already.

**Jack Adair** (Analysts):
That's helpful. And if I could ask one more about your Communications business. And with the new launch cadence at Apple, just if you could help us with more color on seasonality in '27 and if you expect content gains to be a factor there with new form factors in the mix.

**Kevin Engel** (Executives):
Okay. Yes. So comms is interesting. I think overall, it's a little early to tell what the full year profile will look like. But you're right, with the different launch profiles, which we tried to signal a little bit going back last quarter, that we would expect that to change our typical seasonality. But I think it's, again, a little too early to see how that's going to completely play out. You can imagine there's lots of different dynamics going on there between supply constraints, memory pricing affecting overall demand, the build cycles like you talked about. So there's lots of components there. But in general, related to the form factors, I don't see that there's a lot of impact related to that. Obviously, it's more about unit sales, the better these -- the phones sell, obviously, that bodes well to just increased demand overall.

**Operator** (Operator):
Your next question comes from Randy Abrams with UBS.

**Randy Abrams** (Analysts):
Yes. My first question, I wanted to expand on your Computing opportunities. You're having a nice ramp on the CPU program. Could you talk about your progress on the fan-out bridge, how that is progressing? And also, if you could talk about the scope. I think you mentioned a couple of other new projects such as networking ramping up, how you see those incremental activities for compute.

**Kevin Engel** (Executives):
Okay. Yes. Thanks, Randy. So yes, a few things there. So when we think about the bridge opportunity, I'd say that's progressing as expected. We talked about that being a late 2027 opportunity into '28. I think our time line still matches that. The discussions with the customer are ongoing. Obviously, there's a lot of interest again, to kind of secure capacity overall. Again, we kind of paint a little bit of a picture around capacity constraints in general across the industry.
When we think about Computing, obviously, early on, there's a lot of discussion around silicon availability, memory availability. I'd say those seem to be -- I mean, they're still there, but at least customers understand better what is available to them going into 2027. And I think that has highlighted even more that packaging is becoming one of the key bottlenecks. So customers are really working to make sure they secure capacity into '27 and even into 2028. So that's where you start to see a lot of these advance payment discussions.
And help me with the second question again, Randy?

**Randy Abrams** (Analysts):
Yes. The second part of that was the other projects. If you could talk a bit more about the scope, is compute concentrated with the core CPU or you're seeing good broadening out to these other projects, if you expect them to be meaningful?

**Kevin Engel** (Executives):
Yes. So I mean, meaningful. I think these core fundamental programs are scaling much, much faster. So I think I have to say that. But I think we have programs going on in the xPU, networking programs and things like switches. Those are 2.5D type programs. And then again, we talked about the CPU program for a hyperscaler. Again, all of those are on track, either ramping now or ramping in the next quarter or this quarter, late this quarter. But I think overall, the scale-wise, the big driver is the key programs we talked about.

**Randy Abrams** (Analysts):
Okay. Great. And my second question, I wanted to ask about the cost and also the pricing environment. We're seeing a lot of the substrate and material costs rise, but also tight capacity. I think your Taiwan peer has been raising price. How do you see both of those drivers? And if I could add just one offset. Would the SiP business rebound stronger next year to offset if you indeed could see some pricing improvement? Do you see any offsets from SiP?

**Kevin Engel** (Executives):
Okay. Yes. So yes, I mean, there's definitely cost pressure. I think we're managing that closely with our suppliers. And typically, we're passing those costs on to our customers. I think the pricing environment in general is still attractive related to being able to pass costs along and think about long-term investment and how we're managing that margin profile to make sure the return is there. And again, you think about the number of players that support these types of products or these types of packages, it's relatively limited. So that creates an environment where I think all of the players in this field are able to really drive an attractive cost structure and price structure just because of the overall constraints in the capacity in general.
Then when it comes to SiP, we definitely see that -- again, we talked about the short-term kind of headwinds related to the transfer and how you always have a little bit of a gap as you're moving assets across the oceans. But we definitely see with working with the customers that the rebound is there. There's a lot of pipeline built up for SiP. Pricing, I'd kind of go back with that related to passing on cost increases that we're seeing, maybe not so much related to really driving an overall margin acceleration related to that business part.

**Operator** (Operator):
Your next question comes from Steven Fox with Fox Advisors.

**Steven Fox** (Analysts):
I had 2 as well. I guess, first of all, you gave a lot of great clues on how CapEx could look like for next year. Can you talk about how some of the capacity expansion could impact gross margins in the coming calendar year? And also how much of a mix offset you could get roughly when we think about that? And I have a follow-up.

**Kevin Engel** (Executives):
Okay. Megan, can you take that one?

**Megan Faust** (Executives):
Sure. So just to reiterate, Steve, we did want to signal without -- we're not yet ready to provide full 2027 CapEx guidance, but that we are proceeding with some programs that Kevin outlined that are going to step up CapEx, specifically around facilities. So just to recap there, we have the Arizona facility, we gave a framework that '27 could be up to 15% of that $12 billion in '27. And then for Korea in the range of $400 million to $450 million. And then Vietnam, $50 million. So altogether, those are higher than $2 billion just around those programs.
So as it relates to margin impact, just as a reminder, the Arizona facility will not yet be completed until the end of '27. So that won't start being recognized in the income statement until that's completed. So we'll be capitalizing that over the course of the year, similarly with the other primary projects in Korea. As it relates to equipment, we do anticipate further expansion on the equipment side. We're going to see probably around a mid-teens percent increase in depreciation in '26.
I do expect that, that will increase somewhat in '27. It's still too early to tell yet what that impact on margin will be. However, as you just mentioned, we are executing on our strategic plan, which identified product mix as one of the primary areas for margin expansion. And with our plan around compute to grow similarly 30% or more in '27, we would anticipate having a benefit related to that in '27.

**Steven Fox** (Analysts):
Great. That's super helpful. And then just as a follow-up, I know you just covered pricing, but maybe just asking it a little differently on some of these agreements. Obviously, you've taken some of the -- a lot of the risk out in terms of planning for capacity with some of these new compute agreements and networking, et cetera. How do we think about just how you're creating pricing power within that? Is there any other thing -- anything else we should think about besides you mentioned sort of the predictability of the production in a specific plant?

**Kevin Engel** (Executives):
No. Again, I think if you look at all of the Computing customers, the environment and the pricing environment, they understand that these are very significant capital investments, and there needs to be a return on these capital investments. So I think the margin profile and the return is not a major issue. They are more focused on making sure they secure the capacity. So at this point, we feel very optimistic around the pricing environment related to these multiyear agreements.

**Operator** (Operator):
[Operator Instructions] Your next question comes from Steve Barger with KeyBanc Capital Markets.

**Steve Barger** (Analysts):
Megan, you talked about the dozen customers with prepayments, and it sounds like there could be some more coming. As you think about CapEx timing versus these payments arrangements, can you manage this build-out without incremental debt? Or is it too early to tell?

**Megan Faust** (Executives):
Thanks, Steve. So with what we have outlined, we are -- obviously, there's going to be significant support in '27. So that even pushes through '28, where there may not even need to be incremental debt at that point. So I would say it's still too early to tell whether we would need incremental debt within '28 and beyond. But I would say the balance sheet positioning is solid through 2027.

**Steve Barger** (Analysts):
Got it. And if consumer electronics in comms and compute remains soft for multiple quarters into next year, does it change the margin trajectory or the earnings trajectory as you think about the CapEx investments that you've talked about relative to the unit volume, potential losses from some of these consumer electronics programs? Or do you expect that the AI-related devices acceleration can mitigate that?

**Kevin Engel** (Executives):
Yes. So let me just start again with the overall picture. And I think we talked about this a good bit during the Investor Day. So when we think about what's our long-term vision, compute is going to continue to accelerate. And obviously, that's a very attractive margin profile. and become a larger portion of the business. We talked about the CAGRs we would expect there. Some of these opportunities that we've talked about in advance payments were already contemplated in those long-term targets. But I think -- and then when we look at Communications, we would expect it to continue to grow, maybe not at -- obviously not at the kind of growth rates we're talking about for Computing. So in general, we feel the assets, we will have troughs and things like that. But the assets overall, we don't think that utilization levels will change over time. They'll continue to rise and be an attractive profile for the overall Communications business.
And Megan, anything to add there?

**Megan Faust** (Executives):
Yes. I just wanted to mention that we do see having a diversified portfolio as a benefit. And so in times like this, where we are seeing weakness in Communications and Consumer, those changes in market dynamics are being cushioned by the strength in compute. And we've seen this before when we had Automotive significantly declining post COVID, and we had other markets such as Communications and Compute at the time. So I think having a diversified portfolio definitely helps smooth through dynamics such as what we're experiencing today.

**Kevin Engel** (Executives):
Yes. And again, just thinking about build cycle changes, we're optimistic that the first half, second half peaks will be different moving forward. We'll see if that cycle continues longer term. But I think that will also be pretty significant related to the Communications first half, second half dynamic.

**Operator** (Operator):
And your next question comes from Denis Pyatchanin with Needham & Company.

**Denis Pyatchanin** (Analysts):
My first one is for Kevin. Given persistently high memory prices over the last year, what are you seeing in terms of impact on PC and smartphone-related product volume? Would you be able to quantify the current impact for each? And could you maybe provide an outlook for these markets for the next year?

**Kevin Engel** (Executives):
Yes, that's a hard question. I'd say, obviously, memory pricing and then just availability in general has affected both markets. Definitely in Communications, and I think we tried to signal some of this before, we saw that Android maybe had a little bit harder time adjusting than iOS. And that may be related to overall pricing dynamics. I think the low-tier type phones had a harder time absorbing those cost changes than the premium tier. So I think that will continue.
And then when we think about the PC market, again, memory is a pretty sizable component to the overall PC cost. So we definitely saw impacts there. But I think the general trend that we've always highlighted about the migration to ARM from x86 is continuing, and that's helping to offset some of those challenges for us.

**Denis Pyatchanin** (Analysts):
And my second one is for Megan. So more recently, CapEx has come up to over 30% of sales, while historically, it has been in the low to mid-teens. Would you be able to provide a longer-term outlook for CapEx intensity? Any thoughts on whether it will ramp down more slowly or if there will be a more significant drop at some point 2 or 3 years out?

**Megan Faust** (Executives):
Sure. So we have indicated '27 will have a step-up in CapEx for -- specifically for the facility build-out. We've also at least shared a framework that our Arizona build-out will peak in '28 and '29. That's because we will be constructing Phase 2 at the same time that we're bringing on equipment for Phase 1. So I think the CapEx is going to stay elevated through those periods. And then from that perspective, from what we've shared so far, it will probably taper back down. As far as a long-term kind of normalized, we have not provided that level of detail.

**Operator** (Operator):
At this time, I'm showing no further questions. I would like to turn the call back over to Kevin for closing remarks.

**Kevin Engel** (Executives):
Okay. Thank you, everyone, for the questions. Let me close with 3 key messages. First, our financial performance continues to strengthen. Record Computing and Automotive and Industrial revenue and margin expansion demonstrates the improving earnings power of the business. Second, advanced packaging is driving significant growth opportunities. We continue to make progress across our HDFO and 2.5D programs with strong momentum in AI and high-performance Computing. And third, customers are making longer-term commitments to Amkor. This gives us greater visibility as we accelerate our global capacity expansions. Thank you for joining the call today.

**Operator** (Operator):
Ladies and gentlemen, this concludes today's conference call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AMKR_Q2_2026_Earnings_Call_20260727.md
- 2026-07-27｜CFO｜guidance：Q3 營收財測區間（原話："Q3 revenue is expected to"）
- 2026-07-27｜CFO｜guidance：Q3 毛利率財測 18.5%–19.5%（原話："Gross margin is projected to be between 18.5% and 19.5%,"）
- 2026-07-27｜CFO｜guidance：Q3 EPS 財測（原話："resulting in EPS between $0.72"）
- 2026-07-27｜CFO｜guidance：Q3 通訊營收預期季減高個位數，偏離季節性（原話："we expect Communications revenue to decline in the high single digits"）
- 2026-07-27｜CFO｜guidance：Q3 運算營收預期季增近 30%（原話："Computing growth is expected to accelerate to nearly 30% sequentially in Q3,"）
- 2026-07-27｜CFO｜guidance：2026 資本支出維持 25–30 億美元（原話："Our estimated 2026 CapEx spend remains between $2.5 billion and $3 billion."）
- 2026-07-27｜CFO｜margin：Q2 毛利率 16.8%，季增逾 250 bps（原話："Gross margin was 16.8%, expanding over 250 basis points sequentially."）
- 2026-07-27｜CFO｜margin：Q2 毛利率擴張拆解：三分之二稼動率/量，三分之一產品組合（原話："two-thirds of that expansion"）
- 2026-07-27｜CFO｜margin：Q3 毛利率擴張主要來自產品組合（原話："predominantly the impact on that gross margin expansion is related to product"）
- 2026-07-27｜CFO｜margin：Q2 營業費用含 2,100 萬美元不動產出售利得（原話："included a $21 million gain on the sale of real estate."）
- 2026-07-27｜CFO｜margin：Q2 稅率 14%，含 1,400 萬美元離散稅務利益（原話："14% due to $14 million in net discrete tax benefits."）
- 2026-07-27｜CEO｜margin：CEO 說明稼動率：Q1 在 70 幾%、Q2 在高 70 幾%（原話："In Q2, we"）
- 2026-07-27｜CEO｜margin：管理層確認 Arizona 製造負擔將在 2027 成為逆風（原話："we need to be thinking about"）
- 2026-07-27｜CFO｜margin：CFO 稱 2028 毛利率與營業利益率均含 Arizona 低稼動率拖累（原話："ramping underutilized Arizona"）
- 2026-07-27｜CEO｜customer：與 TSMC 簽 10 年先進封裝協議（原話："First, we announced a 10-year advanced packaging agreement with TSMC."）
- 2026-07-27｜CEO｜customer：與 NVIDIA 簽多年策略夥伴協議（原話："We also announced a multi-year strategic partnership"）
- 2026-07-27｜CEO｜customer：NVIDIA 協議為預付款，2027 收到並隨服務返還，期限 5–10 年（原話："this is a prepayment"）
- 2026-07-27｜CFO｜customer：Android 營收 Q2 季減 20%，歸因記憶體供給（原話："Android revenue declined 20% reflecting the impact of"）
- 2026-07-27｜CFO｜risk：Q3 通訊下滑三因素：SiP 移越南、記憶體供給限制、拉貨型態改變（原話："second, ongoing"）
- 2026-07-27｜CEO｜risk：CEO 稱 SiP 移轉造成的逆風不只一季，延續到 Q4 與明年上半年（原話："It's probably going to extend into Q4"）
- 2026-07-27｜CEO｜risk：CEO 稱 Q3 通訊下滑約 50% 為市場因素、50% 為 SiP 移轉（原話："The other 50% would be driven by, again, this SiP move"）
- 2026-07-27｜CEO｜risk：Q4 通訊不預期有一般下半年的明顯拉升（原話："we would expect that communications in general will"）
- 2026-07-27｜CEO｜product：最新資料中心 CPU 專案 Q2 開始放量，下半年持續擴大（原話："our newest data"）
- 2026-07-27｜CEO｜commitment：今年預計各有 4 個 2.5D 與 4 個 HDFO 產品量產（原話："4 2.5D, 4 HDFO products launching this year."）
- 2026-07-27｜CEO｜product：橋接類技術時程屬 2028 年（原話："that would be more of a 2028 type"）
- 2026-07-27｜CEO｜commitment：R&D 占比維持 3%–5%，NVIDIA 協議無階梯式增加（原話："I would expect that level to continue."）
- 2026-07-27｜CFO｜capital_allocation：5 月發行 11.5 億美元 0% 可轉債（原話："we issued $1.15 billion of 0% convertible debt,"）
- 2026-07-27｜CFO｜capital_allocation：6/30 現金 25 億、流動性 36 億、總負債 25 億、負債/EBITDA 1.8x（原話："total liquidity was $3.6 billion."）
- 2026-07-27｜CEO｜capital_allocation：Arizona Phase 1 已被預訂滿載（原話："Our projections now show Phase 1 as fully committed,"）
- 2026-07-27｜CEO｜competition：CEO 稱當前客戶可見度與以往產業週期明顯不同（原話："is meaningfully different"）

### AMKR_Analyst_Investor_Day_Amkor_Technology_Inc_20260521.md
- 2026-05-21｜Megan Faust｜guidance：CFO 給出 2028 年營收目標 90 億美元，±5 億。（原話："revenue to grow to $9 billion, plus or minus $500 million"）
- 2026-05-21｜Megan Faust｜margin：2028 年毛利率目標 17.5%（±100bp），2025 為 14%。（原話："Gross margins expand to 17.5%, plus"）
- 2026-05-21｜Megan Faust｜guidance：2028 年 EPS 目標 2.50 美元，±0.25。（原話："earnings per share of $2.50, plus or minus $0.25"）
- 2026-05-21｜Megan Faust｜guidance：2030 年目標：營收逾 110 億美元、毛利率逾 22%（EPS 逾 5 美元）。（原話："more than $11 billion in revenue, more than 22% gross margin"）
- 2026-05-21｜Megan Faust｜guidance：管理層對 2028/2030 目標的定位：預期執行並打算超越。（原話："we would plan to beat those."）
- 2026-05-21｜Kevin Engel｜risk：CEO 說明目標模型未內建強烈的景氣下行。（原話："strong cycle in the downward direction."）
- 2026-05-21｜Kevin Engel｜guidance：目標模型僅含亞利桑那第一期，第二期尚未納入。（原話："we didn't put Phase 2 in the model."）
- 2026-05-21｜Kevin Engel｜guidance：2028 年 90 億目標的設定口徑：選的是有把握、可達成的數字。（原話："was achievable, we were very comfortable with."）
- 2026-05-21｜Kevin Engel｜risk：CEO 提到擴產面臨規模化挑戰（含空間）。（原話："We see challenges on scaling."）
- 2026-05-21｜Megan Faust｜guidance：亞利桑那滿載時營收約 10 億美元、毛利率逾 30%。（原話："revenue of around $1 billion and gross margins exceeding"）
- 2026-05-21｜Megan Faust｜capital_allocation：亞利桑那兩期預估總投資 70 億美元。（原話："an estimated total investment of $7 billion."）
- 2026-05-21｜Megan Faust｜commitment：第一期量產時程：2028 年開始、2030 年完全建成。（原話："manufacturing for the first phase is targeted to begin"）
- 2026-05-21｜Megan Faust｜margin：亞利桑那對營業利益的稀釋：2027 年起 1%～2%，視完工與爬坡速度。（原話："We anticipate a 1% to 2% dilution to"）
- 2026-05-21｜Megan Faust｜guidance：亞利桑那預期 2029 年前後損益兩平。（原話："We expect Arizona to reach breakeven around 2029"）
- 2026-05-21｜Megan Faust｜margin：數字口徑：2027–2028 亞利桑那爬坡成本先入營業費用，通過驗證後轉入銷貨成本。（原話："there are initial ramp costs in 2027 and 2028 tied to"）
- 2026-05-21｜Megan Faust｜margin：數字口徑：爬坡成本認列在 OpEx（SG&A）中，與越南廠做法一致。（原話："costs begin in OpEx, specifically in SG&A."）
- 2026-05-21｜Megan Faust｜margin：回答毛利擴張來源：前期以產品組合為主、並帶動稼動率。（原話："more mix impact to margin followed by leverage"）
- 2026-05-21｜Megan Faust｜margin：投資爬坡期的口徑：獲利成長刻意慢於營收成長。（原話："earnings growth is muted relative to revenue growth"）
- 2026-05-21｜Megan Faust｜guidance：數字口徑：2030 目標模型未納入第二座亞利桑那廠。（原話："We have not yet included the second Arizona facility"）
- 2026-05-21｜Megan Faust｜capital_allocation：2026 年資本支出指引 25～30 億美元。（原話："for 2026, we guided $2.5 billion to"）
- 2026-05-21｜Megan Faust｜capital_allocation：資本密集度預期由歷來 12%～13% 升至中高十幾%。（原話："moving up into the mid-teens, maybe mid- to high-teens."）
- 2026-05-21｜Megan Faust｜capital_allocation：歷史資本密集度區間。（原話："We've been very consistent in that 12% to 13%."）
- 2026-05-21｜Megan Faust｜capital_allocation：槓桿現況：含 12 億美元可轉債後，總債務 26 億、總槓桿 2.1 倍。（原話："with $2.6 billion of total debt, our gross leverage is 2.1x."）
- 2026-05-21｜Megan Faust｜capital_allocation：5 月發行 12 億美元可轉債。（原話："$1.2 billion of convertible notes we issued"）
- 2026-05-21｜Megan Faust｜commitment：長期債務／EBITDA 目標 1.5 倍以下。（原話："EBITDA target of 1.5x or below"）
- 2026-05-21｜Megan Faust｜commitment：股東回饋目標：自由現金流的 40%～50%。（原話："Over time, we target a return of 40% to 50%"）
- 2026-05-21｜Megan Faust｜capital_allocation：庫藏股授權上限 3 億美元，可機動使用並抵銷股酬稀釋。（原話："repurchase authorization of up to $300 million"）
- 2026-05-21｜Megan Faust｜commitment：回答線上提問：未考慮暫停或停止股利。（原話："we have not considered pausing or stopping the dividend."）
- 2026-05-21｜Megan Faust｜capital_allocation：資金來源之一：已有客戶以預付款形式承諾。（原話："that were in the form of advanced payments"）
- 2026-05-21｜Doug Scott｜capital_allocation：擴產原則：依需求而非投機。（原話："demand, not speculation."）
- 2026-05-21｜Megan Faust｜risk：亞利桑那第一期的機台尚未全數下單，客戶仍在討論專案性質與規模。（原話："yet ordered all the tools for that first phase."）
- 2026-05-21｜Kevin Engel｜customer：第一期客戶結構多為合約性安排（含裝載協議或預付款）。（原話："them are contractually based structures."）
- 2026-05-21｜Megan Faust｜commitment：第二期時程：管理層表示是何時而非是否。（原話："see Phase 2 as a not if, it's just when."）
- 2026-05-21｜Kevin Engel｜product：先進封裝營收今年預期成長為三倍，且全在運算市場。（原話："a tripling of that advanced"）
- 2026-05-21｜Doug Scott｜product：2.5D 客戶接洽數量。（原話："We now have over a dozen 2.5D engagements."）
- 2026-05-21｜Doug Scott｜customer：首個高密度扇出橋接封裝預計明年為 AMD 量產。（原話："bridge package to ramp next year for our customer AMD."）
- 2026-05-21｜Doug Scott｜product：正在開發三個共封裝光學（CPO）案，合計為十億美元級機會。（原話："these projects are billion-dollar opportunities"）
- 2026-05-21｜Doug Scott｜product：CPO 投資時點的敘事：太早投入會使產線閒置。（原話："when we were first asked to invest in CPO 10 years ago"）
- 2026-05-21｜Doug Scott｜product：對 CoWoS 轉 CoWoP 的態度：定位為快速跟進者而非領頭試產。（原話："but certainly as a fast follower."）
- 2026-05-21｜Kevin Engel｜product：測試占營收目前低十幾%，2029–2030 預期升至中高十幾%。（原話："we're envisioning in the mid- to high-teens"）
- 2026-05-21｜Kevin Engel｜competition：最先進封裝產能緊，台灣以外僅 Amkor 韓國可選。（原話："outside of Taiwan is Amkor in Korea."）
- 2026-05-21｜Megan Faust｜competition：管理層自述為美國唯一擴產中的大規模先進封裝 OSAT。（原話："only scaled advanced packaging OSAT that is expanding"）
- 2026-05-21｜Farshad Haghighi｜customer：Apple COO 影片被用作客戶背書，並稱此模式正部署到美國製造點。（原話："Sabih Khan, the COO at Apple generously shared his vision"）
- 2026-05-21｜Kevin Engel｜customer：與超大規模雲端業者直接溝通增加。（原話："definitely more direct communication with the hyperscalers."）
- 2026-05-21｜Kevin Engel｜customer：汽車為第二快成長市場。（原話："at least today, our second fastest-growing market."）
- 2026-05-21｜Megan Faust｜customer：通訊市場整體成長放緩，靠端側 AI 與換機週期。（原話："continued growth will be driven by on-device AI and refresh"）
- 2026-05-21｜Kevin Engel｜customer：數字口徑：2025 年通訊占營收 46%，運算預期成長快於市場。（原話："In 2025, it represented 46% of our revenue."）
- 2026-05-21｜Farshad Haghighi｜product：高階智慧手機半導體價值預期自 225 美元升至 400 美元。（原話："from $225 today toward $400 over the next few years."）
- 2026-05-21｜Kevin Engel｜product：OSAT 可服務市場（TAM）的估算口徑：每吉瓦約 5 億美元，四至五年成長逾 3 倍。（原話："an increase in TAM of over 3x over the next four to five"）
- 2026-05-21｜Kevin Engel｜risk：管理層強調此為結構性轉變而非景氣循環。（原話："and it's not cyclical."）
- 2026-05-21｜Kevin Engel｜customer：與 Intel 合作 EMIB，預計年底在韓國具備能力。（原話："how we are supporting bringing that technology into Korea"）
- 2026-05-21｜Kevin Engel｜capital_allocation：被問聯邦政府入股：表示沒有相關討論。（原話："there's been no discussions around that."）

### 問答異常語氣（迴避／改口／保留）
- AMKR_Q2_2026_Earnings_Call_20260727.md｜問：Randy Abrams 問 SiP 移轉是否僅一季時間差｜答法：CEO 先答之後在後續回答改口：移轉逆風並非一季，延伸到 Q4 與明年上半年
- AMKR_Q2_2026_Earnings_Call_20260727.md｜問：Ben Reitzes 問 Q3 毛利率中 SiP 與稼動率的影響及 Q3 稼動率預期｜答法：CEO 談稼動率定性描述（Q1 70 幾%、Q2 高 70 幾%），未給 Q3 稼動率數字，也未量化 SiP 影響
- AMKR_Q2_2026_Earnings_Call_20260727.md｜問：Steve Barger 問 Q4 毛利率是否季節性上升及 2027 到 2028 目標節奏｜答法：未給 Q4 數字，答依組合與稼動率而定；2027 僅指出美國製造負擔為逆風，未給 2027 數字
- AMKR_Analyst_Investor_Day_Amkor_Technology_Inc_20260521.md｜問：訂單能見度是否超過兩年、可否量化？｜答法：Doug 只答 'It's over'，Kevin 明確表示 'We won't estimate' 並轉談光學與客戶採用速度，未給期間數字。
- AMKR_Analyst_Investor_Day_Amkor_Technology_Inc_20260521.md｜問：2028 年 90 億目標是否受產能所限（目前已年化約 80 億）？｜答法：Kevin 未直接回答是否產能受限，改談目標是 'achievable numbers'、另有更多機會與空間擴張挑戰。
- AMKR_Analyst_Investor_Day_Amkor_Technology_Inc_20260521.md｜問：亞利桑那第二期的客戶需求時點與資本支出規模？｜答法：Kevin 稱討論 'progressing pretty rapidly' 並說 'stay tuned'；Megan 談時程貼近專案，皆未給時點或資本支出數字。
- AMKR_Analyst_Investor_Day_Amkor_Technology_Inc_20260521.md｜問：2.5D、HDFO、橋接、覆晶與晶圓級中哪些受限、哪些低利用？｜答法：Doug 只說整體先進封裝高稼動並持續投資，未點名哪個領域閒置或受限。

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
{"date":"20260524","verdict":"B 衛星候選：thesis 完整（B 級護城河 7/10、AI 先進封裝超級週期、TSMC Arizona partnership unique、Q1 26 EPS Beat 50% 強訊號），但 (a) 估值 🟡 救援後合理但未達 🟢、(b) Pure MA ✅ 強勢但 5/18 shooting star + 連 3 日衝高回落 = 動能末段、(c) 短期 R:R 為負值（共識中位 $73 vs 現價 $65.75 上行有限）= 時機尚不到。等回測 W52 $38-55 區或 Fwd PE 24x $58 區 + Q2-Q3 26 報季 EPS guidance 兌現 + HDFO 首次具體營收揭露後分批進場 3-5% 衛星倉。FY26 capex $2.5-3B 高峰執行進度 + Apple 集中度演變是核心監測點。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 先進封裝超級週期持續，AMKR advanced products mix 持續往 90%+ 移動","columns":{"2Y 驗證點":"FY26-27 advanced products 占比突破 85%；HDFO 開始貢獻可揭露營收","5Y 驗證點":"FY28-30 advanced products 占比 90%+，HDFO 占 advanced products 20%+","10Y 驗證點":"FY32+ advanced products 95%+，傳統 packaging 完全 phase out","具體門檻":"FY26 advanced products ≥ 82%；FY27 ≥ 85%；HDFO H2 26 first revenue","來源":"Amkor IR + sell-side 估算 + 法說會揭露","漂移觸發條件":"連 2 季 advanced products mix 停滯 / 下降 → H1 削弱（QC-35 對齊）"}},{"id":"H2","text":"TSMC Arizona partnership 真實落地，2027-2029 帶來 incremental revenue $500M-$1B/年","columns":{"2Y 驗證點":"2027 Arizona phase 1 完工 + 首批 TSMC 客戶訂單揭露","5Y 驗證點":"2028-2030 Arizona phase 1 + phase 2 ramp，產能利用率達 80%+","10Y 驗證點":"Arizona 多 phase 共 $7B 投資全部完工，成為 AMKR 第二大基地","具體門檻":"2027 mid Arizona phase 1 mechanical completion；2028 中首批 TSMC 客戶訂單揭露","來源":"TSMC 法說會 + Amkor IR + CHIPS Act 補助到位進度","漂移觸發條件":"Arizona 完工延後超過 12 個月，且 TSMC partnership 無新進展 → H2 削弱"}},{"id":"H3","text":"Apple 客戶集中度從 30% 逐步降至 22-25%（不是因為 Apple 流失，而是其他客戶成長）","columns":{"2Y 驗證點":"FY26-27 Computing + Automotive 兩段營收占比合計提升至 35%+","5Y 驗證點":"FY28-30 Computing 段成為第一大段（取代 Communications）","10Y 驗證點":"FY32+ 客戶分布更平衡，no single 客戶 &gt; 25%","具體門檻":"FY26 Computing 占比 ≥ 12%（FY24 ~9%）；FY27 ≥ 18%；FY28 ≥ 25%","來源":"Amkor 10-K 分段揭露 + sell-side 模型","漂移觸發條件":"Apple 占比連 2 年仍 ≥ 30% 且 Computing 占比 &lt; 15% → H3 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Apple iPhone unit 同期見頂 + Apple C2/C3 modem 自研擴大 → Communications 段 quarterly revenue YoY 轉負","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Communications 段 quarterly YoY %","警戒閾值":"連 2 季 YoY &lt; 0% → 觸發減倉"}},{"id":"R2","text":"FY26 capex $2.5-3B 真實執行但 H2 26 / H1 27 需求疲軟 → FY26 / FY27 FCF 連年壓制 / 轉負 → 股利 + buyback 動用 net cash","columns":{"對應假設":"H1 / H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"FY26 全年 FCF + Net cash position","警戒閾值":"FY26 FCF &lt; -$300M 或 Net cash 轉 Net debt &gt; $0.5B → 嚴重 capital discipline 質疑"}},{"id":"R3","text":"2030 年代計算範式轉換（photonics / hybrid bonding 完全取代 2.5D / 3D）+ TSMC 收回 advanced packaging in-house → AMKR 結構性退至 traditional 商品 OSAT","columns":{"對應假設":"H1 / H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"TSMC 法說會關於 SoIC / advanced packaging capex 比例 + AMKR R&amp;D / Revenue 趨勢","警戒閾值":"需 ≥ 50% 機率才砍倉；當前機率 ~15-20%，列入觀察"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":65.75,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMKR_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
