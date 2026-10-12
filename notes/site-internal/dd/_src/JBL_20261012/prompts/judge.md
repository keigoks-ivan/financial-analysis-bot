你是 stock-analyst **v20 判斷 agent**，標的 JBL（20261012）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
  *eps
    *bull[]: arr ≥1 num
    *base[]: arr ≥1 num
    *bear[]: arr ≥1 num
  *pe
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
{"meta":{"ticker":"JBL","date":"2026-10-12","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JBL_20261012/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JBL_20261012/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_revenue_gaap","label":"Net revenue (GAAP)","value":10616,"period":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","citation":"公司 8-K Ex.99.1 Q4 FY26 新聞稿（https://www.sec.gov/Archives/edgar/data/0000898293/000162828026063890/jbl-20260930ex991.htm；IR 頁 investors.jabil.com 同步發布）"},"note":"consensus 約 $9.7B（來源：媒體彙整，非 IR；web_search）"},{"id":"f_kpi1_core_non_gaap_operating_","label":"Core (non-GAAP) operating income","value":675,"period":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","citation":"公司 8-K Ex.99.1 Q4 FY26 新聞稿（https://www.sec.gov/Archives/edgar/data/0000898293/000162828026063890/jbl-20260930ex991.htm；IR 頁 investors.jabil.com 同步發布）"},"note":"未取得"},{"id":"f_kpi2_core_operating_margin","label":"Core operating margin","value":6.4,"period":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","citation":"公司 8-K Ex.99.1 Q4 FY26 新聞稿（https://www.sec.gov/Archives/edgar/data/0000898293/000162828026063890/jbl-20260930ex991.htm；IR 頁 investors.jabil.com 同步發布）"},"note":"未取得"},{"id":"f_kpi3_gaap_operating_income","label":"GAAP operating income","value":602,"period":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","citation":"公司 8-K Ex.99.1 Q4 FY26 新聞稿（https://www.sec.gov/Archives/edgar/data/0000898293/000162828026063890/jbl-20260930ex991.htm；IR 頁 investors.jabil.com 同步發布）"},"note":"未取得"},{"id":"f_kpi4_gaap_operating_margin","label":"GAAP operating margin","value":5.7,"period":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","citation":"公司 8-K Ex.99.1 Q4 FY26 新聞稿（https://www.sec.gov/Archives/edgar/data/0000898293/000162828026063890/jbl-20260930ex991.htm；IR 頁 investors.jabil.com 同步發布）"},"note":"未取得"},{"id":"f_kpi5_core_diluted_eps","label":"Core diluted EPS","value":4.4,"period":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","citation":"公司 8-K Ex.99.1 Q4 FY26 新聞稿（https://www.sec.gov/Archives/edgar/data/0000898293/000162828026063890/jbl-20260930ex991.htm；IR 頁 investors.jabil.com 同步發布）"},"note":"consensus $4.07（來源：媒體彙整，web_search）"},{"id":"f_kpi6_adjusted_free_cash_flow","label":"Adjusted free cash flow (全年)","value":1532,"period":"FY2026（年度至 2026-08-31，公告於 2026-09-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"FY2026（年度至 2026-08-31，公告於 2026-09-30）","citation":"公司 8-K Ex.99.1 Q4 FY26 新聞稿（https://www.sec.gov/Archives/edgar/data/0000898293/000162828026063890/jbl-20260930ex991.htm；IR 頁 investors.jabil.com 同步發布）；季度單季 FCF 新聞稿摘要未見"},"note":"未取得"},{"id":"f_kpi8_guidance_q1_fy2027","label":"Guidance：Q1 FY2027","value":"營收 $10.6B～$11.4B；GAAP 營業利益 $481M～$541M；core 營業利益 $592M～$652M；GAAP EPS $2.78～$3.18；core EPS $3.80～$4.20","period":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","citation":"公司 8-K Ex.99.1 Q4 FY26 新聞稿（https://www.sec.gov/Archives/edgar/data/0000898293/000162828026063890/jbl-20260930ex991.htm；IR 頁 investors.jabil.com 同步發布）"},"note":"未取得"},{"id":"f_kpi9_guidance_fy2027","label":"Guidance：FY2027 全年","value":"營收 $44.5B（+24%）；core 營業利益率 6.1%；core EPS $17.55（+34%）；adjusted FCF 約 $1.6B","period":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","citation":"公司 8-K Ex.99.1 Q4 FY26 新聞稿（https://www.sec.gov/Archives/edgar/data/0000898293/000162828026063890/jbl-20260930ex991.htm；IR 頁 investors.jabil.com 同步發布）"},"note":"未取得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-09-30","period":"2026-09-30","unit":"date","basis":"距今 8 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-09-30"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_jbl_gross_margin_pct","label":"JBL 毛利率","value":9.23,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.gross_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_jbl_operating_margin_pct","label":"JBL 營業利益率","value":5.03,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.operating_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_jbl_fcf_margin_pct","label":"JBL FCF 利潤率","value":3.89,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.fcf_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_cls_gross_margin_pct","label":"CLS 毛利率","value":11.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cls_operating_margin_pct","label":"CLS 營業利益率","value":8.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cls_fcf_margin_pct","label":"CLS FCF 利潤率","value":3.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_flex_gross_margin_pct","label":"FLEX 毛利率","value":9.35,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_flex_operating_margin_pct","label":"FLEX 營業利益率","value":5.29,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_flex_fcf_margin_pct","label":"FLEX FCF 利潤率","value":3.68,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sanm_gross_margin_pct","label":"SANM 毛利率","value":9.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sanm_operating_margin_pct","label":"SANM 營業利益率","value":5.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sanm_fcf_margin_pct","label":"SANM FCF 利潤率","value":4.66,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi7_sbc_core","label":"SBC 及相關費用占 core 營業利益","value":20.8,"period":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q4 FY2026（季末 2026-08-31，公告於 2026-09-30）","citation":"公司 8-K Ex.99.1 Q4 FY26 新聞稿（https://www.sec.gov/Archives/edgar/data/0000898293/000162828026063890/jbl-20260930ex991.htm；IR 頁 investors.jabil.com 同步發布）（SBC $25M ÷ core op income $675M，自算；全年 $140M ÷ $2,069M＝6.8%）"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":306.28,"period":"2026-10-09（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":2.31,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":49.41,"period":"2026-10-09（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":38.53,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.77 → 17.69）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":31.34,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.88 → 22.17）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":26.06,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.57 → 25.93）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":17.69,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":22.17,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":25.93,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":38.64,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 12.76 → 17.69（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":31.41,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝85.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":85.1,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.89,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.96,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":17.31,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 17.69，分子＝快照價 306.28","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.104,"period":"2026-10-12","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-12"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"CSI Market 追蹤同業組：Jabil 占同業合計營收約 19.7%，一年前為 22.2%；FQ3 2026 營收年增 11.8%，同業合計 30.3%。同業範圍未揭露，單一資料商。","source":"CSI Market, JBL Growth vs Peers","url":"https://csimarket.com/stocks/JBL-Growth-vs-Peers","excerpt":"Jabil Inc accounted for 19.7% of combined revenue among its tracked peer group, down from 22.2% a year earlier.","as_of":"2026-06-30","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Sacra 報告指 Bright Machines 的 Bright Factory 可能替超大規模雲端客戶營運產能，與 Jabil 等合約製造商直接重疊；Jabil 2024 年曾投資 Bright Machines。屬可能性描述，非已發生的奪單。","source":"Sacra, Jabil as Investor and Competitor","url":"https://sacra.com/chat/h/09126889-d363-400e-a066-653d749b4d98/","excerpt":"it may also operate capacity for hyperscalers","as_of":"2026-01-01","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-Q（截至 2026-05-31 的九個月）：前五大客戶約占淨營收 36%，78 家客戶約占 90%；未點名最大客戶，亦未揭露第二供應商或自製化進度。","source":"Jabil Form 10-Q FY2026 (quarter ended 2026-05-31)","url":"https://www.sec.gov/Archives/edgar/data/0000898293/000162828026046138/jbl-20260531.htm","excerpt":"During the nine months ended May 31, 2026, the Company's five largest customers accounted for approximately 36% of its net revenue","as_of":"2026-05-31","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"2026 年募股說明書風險揭露：Jabil 依賴少數客戶貢獻相當比例營收，且預期未來仍將如此。","source":"Jabil Form 424B5 FY2026","url":"https://www.sec.gov/Archives/edgar/data/898293/000119312526015418/d938204d424b5.htm","excerpt":"depends, and expects to continue to depend for the foreseeable future, upon a relatively small number of customers for a significant percentage of its net revenue","as_of":"2026-01-01","retrieved_at":"20261012","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"第三方（Finviz 託管文章，無日期）稱 Jabil 眾多現有與潛在客戶正在評估自製與外包的利弊；摘要被截斷，無法確認後續內容。","source":"Finviz-hosted article on JBL (undated)","url":"https://finviz.com/news/276090/if-you-invested-1000-in-jabil-a-decade-ago-this-is-how-much-itd-be-worth-now","excerpt":"Many of JBL's current and potential customers are assessing the merits of in-house manufacturing against the outsourcing option","as_of":"2026-01-01","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Apple 營收占比逐年下降：FY2021 22%、FY2022 19%、FY2023 17%、FY2024 11%（取自 10-K 財報表彙整）","source":"SEC EDGAR JBL 10-K FY2024 Financial_Report","url":"https://www.sec.gov/Archives/edgar/data/898293/000162828024043960/Financial_Report.xlsx","excerpt":null,"as_of":"2024-10-17","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"第三方彙整：FY2025 前五大客戶約占營收 36%，Customer A 占營收 16%、應收款 24%（未對照 10-K 原文）","source":"policyrisk.com JBL 彙整頁（搜尋摘要）","url":"https://policyrisk.com/world/company/JBL","excerpt":null,"as_of":"2025-10-01","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Moody's 稱 Jabil 單一客戶集中度相對同業偏高，但分散於多項產品","source":"Moody's Investors Service，經 policyrisk.com 引述","url":"https://policyrisk.com/world/company/JBL","excerpt":"Jabil's single customer concentration is high relative to peers, but this exposure is diversified across numerous products","as_of":"2025-10-01","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Panabee 整理 FY2026 Q2 財報：前五大客戶占淨營收 36%（二手來源）","source":"Panabee: Jabil Revenue Grows 18% YTD on AI Demand, Yet Inventory Divergence Persists","url":"https://www.panabee.com/news/jabil-earnings-q2-2026-report","excerpt":null,"as_of":"2026-03-20","retrieved_at":"20261012","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#4","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"FY2026 Q3 財報：全年指引上調至約 $350 億，AI 相關營收預期 $136 億；新增第三家 hyperscaler 客戶，預計 FY2027 貢獻數億美元；管理層提醒指引取決於零組件供應等。搜尋未見客戶被降評、倒閉或下修財測的報導","source":"Nasdaq: Jabil Q3 Earnings Call Highlights AI Growth and Margin Path","url":"https://www.nasdaq.com/articles/jabil-q3-earnings-call-highlights-ai-growth-and-margin-path","excerpt":null,"as_of":"2026-06-18","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Lincoln International Q2 2026 EMS review：產業呈兩極化；資料中心／AI 基礎建設為強項，工業與消費終端表現不一","source":"Lincoln International, 2026 Q2 EMS Quarterly Review","url":"https://www.lincolninternational.com/publications/ems-quarterly-review-q2-2026/","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Jabil FY2027 指引營收 445 億美元（約 +24%）、core EPS 17.55 美元；AI 相關營收由 144 億增至 221 億；雲端與資料中心基礎設施營收預計 +52% 至 175 億","source":"Jabil FY2026 Q4 results / Tiger news 'Jabil Projects 24% Revenue Growth in Fiscal 2027, AI-Related Revenue to Reach $22.1 Billion'","url":"https://www.itiger.com/news/1118646763","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Jabil 新增約 400 萬平方呎產能以支應 FY27 逾 80 億美元增量營收；管理層稱已承諾的客戶需求正填滿新增產能；預期六家 Intelligent Infrastructure 客戶各貢獻逾 10 億美元","source":"Jabil FY2026 Q4 earnings call (Webull transcript / Zacks summary)","url":"https://www.zacks.com/stock/news/2998924/jbl-q4-earnings-call-highlights-ai-led-fiscal-2027-growth","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261012","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Evertiq 2026-09 報導：超大規模業者的 AI 基礎建設投入規模超過全球 EMS 產業全年營收；未找到 FY27 以後的需求預測","source":"Evertiq, Evertiq Expo Gothenburg 2026: AI shortages and the EMS market in focus","url":"https://evertiq.com/news/2026-09-18-evertiq-expo-gothenburg-2026-ai-shortages-and-the-ems-market-in-focus","excerpt":null,"as_of":"2026-09-18","retrieved_at":"20261012","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Jabil 10-Q（FY2026 Q2，期末 2026-02-28）：最高法院推翻 IEEPA 關稅（含部分中國商品）；公司持續監控潛在退稅並評估影響，尚未認列任何退稅。","source":"SEC Form 10-Q, Jabil Inc, quarter ended 2026-02-28","url":"https://www.sec.gov/Archives/edgar/data/898293/000162828026024148/jbl-20260228.htm","excerpt":"The Supreme Court issued a ruling striking down tariffs imposed under the International Emergency Economic Powers Act Jabil continues to monitor the situation, including any potential refunds of such tariffs, and evaluate the impact on its results. No potential refunds have been recorded.","as_of":"2026-02-28","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Jabil 10-Q（期末 2026-05-31）：已開始收到先前繳納的 IEEPA 關稅退款，對經營結果無重大影響；全球關稅格局仍快速變動。","source":"SEC Form 10-Q, Jabil Inc, quarter ended 2026-05-31","url":"https://www.sec.gov/Archives/edgar/data/0000898293/000162828026046138/jbl-20260531.htm","excerpt":null,"as_of":"2026-05-31","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Jabil FY2025 10-K 風險因素：與中國的貿易爭端或政治分歧已經且可能造成關稅等措施，對公司業務產生不利影響。","source":"SEC Form 10-K, Jabil Inc, FY ended 2025-08-31","url":"https://www.sec.gov/Archives/edgar/data/898293/000162828025045293/jbl-20250831.htm","excerpt":null,"as_of":"2025-08-31","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-Q（期間至 2026-05-31）揭露：部分產品所需一項或多項零組件僅有單一來源供應。","source":"Jabil Form 10-Q FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000898293/000162828026046138/jbl-20260531.htm","excerpt":null,"as_of":"2026-05-31","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"10-Q 揭露前五大客戶約占淨營收 36%，78 家客戶約占 90%。","source":"Jabil Form 10-Q FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000898293/000162828026046138/jbl-20260531.htm","excerpt":null,"as_of":"2026-05-31","retrieved_at":"20261012","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"據 10-K（FY2025）摘要：據點含中國、馬來西亞、墨西哥、美國；國際營運面臨地緣動盪、法規與匯率風險；中國營運受貿易爭端及資金匯出限制；2025 年 2 月起美國關稅墊高零件成本；部分次級材料（鈀、氖氣）有衝突導致的短缺風險。為第三方摘要，非原文。","source":"Policy Risk summary of Jabil SEC disclosures","url":"https://policyrisk.com/world/company/JBL","excerpt":null,"as_of":"2025-10-31","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Zacks 類報導稱 Jabil 在地化生產以貼近區域 hyperscaler 需求、降低地緣與關稅不確定性，但擴大在地足跡推高成本、預期造成毛利擠壓。","source":"Zacks via TradingView: JBL gains from robust supply chain network","url":"https://tr.tradingview.com/news/zacks%3A7510bb390094b%3A0-jbl-gains-from-robust-supply-chain-network-will-it-drive-growth","excerpt":null,"as_of":"2025-10-31","retrieved_at":"20261012","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2027 指引：營收約 445 億美元（+24%）、核心營業利益率 6.1%、核心 EPS 17.55 美元；AI 相關營收約 221 億美元（+54%）","source":"Zacks／MarketBeat 轉載 Jabil FQ4 2026 財報電話會（2026-09-30）","url":"https://www.zacks.com/stock/news/2998924/jbl-q4-earnings-call-highlights-ai-led-fiscal-2027-growth","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Intelligent Infrastructure FY2027 預期約 256 億美元（+43%）；雲端與資料中心基礎設施約 175 億美元（+52%）；資本設備約 42 億美元（+40%）；六家 II 客戶各超過 10 億美元；新增約 400 萬平方英尺產能","source":"Zacks／MarketBeat 轉載 Jabil FQ4 2026 財報電話會（2026-09-30）","url":"https://www.marketbeat.com/instant-alerts/transcript-what-jabil-jbl-said-on-its-q4-earnings-call-2026-09-30/","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261012","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"FQ2 2026：Regulated Industries 約 30 億美元（約 +10% 年增），三大終端市場皆成長；Intelligent Infrastructure 約 40 億美元（+52%）；Connected Living & Digital Commerce 約 12 億美元（-8%，計畫性項目退場與客戶修剪）","source":"MarketBeat Jabil Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/jabil-q2-earnings-call-highlights-2026-03-18/","excerpt":null,"as_of":"2026-03-18","retrieved_at":"20261012","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"FQ4 2026 營收約 106 億美元（+29% 年增），FY2026 營收約 350 億美元；Intelligent Infrastructure 與 Regulated Industries 超出指引","source":"Jabil Q4 2026 財報電話會逐字稿（Webull）","url":"https://www.webull.com/news/15667757115769856","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261012","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"-","claim":"風險：半導體零組件供應、客戶決策與產能利用率被列為擴張風險；CEO 稱最終指引取決於零組件供應、組合與爬坡時點","source":"Zacks／MarketBeat 彙整 FQ4 2026 電話會","url":"https://www.zacks.com/stock/news/2998924/jbl-q4-earnings-call-highlights-ai-led-fiscal-2027-growth","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#none","axis":"substitute_technology","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY27 指引（2026-09-30 隨 Q4 FY26 公布）調整後 EPS 17.55 美元、營收 445 億美元，高於共識 EPS 16.92、營收 429.3 億；其他來源共識為 16.58～16.67／422～426 億，指引在各基準下皆高於共識","source":"Finviz news: Jabil shares fall 4% despite fourth quarter earnings beat and higher fiscal 2027 outlook","url":"https://finviz.com/news/397095/jabil-shares-fall-4-despite-fourth-quarter-earnings-beat-and-higher-fiscal-2027-outlook","excerpt":"Jabil expects adjusted earnings of $17.55 per share, above the Wall Street consensus estimate of $16.92.","as_of":"2026-09-30","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY27 核心營業利益率指引 6.1%（+30bp）、調整後自由現金流約 16 億美元、AI 相關營收 144 億→221 億美元（+54%）","source":"Jabil Projects 24% Revenue Growth in Fiscal 2027 (itiger)","url":"https://www.itiger.com/news/1118646763","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q1 FY27 指引 EPS 3.80～4.20、營收 106～114 億美元；當時共識 EPS 3.66、營收 99 億；公布後盤前股價約 -4%","source":"Finviz news (同上)","url":"https://finviz.com/news/397095/jabil-shares-fall-4-despite-fourth-quarter-earnings-beat-and-higher-fiscal-2027-outlook","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261012","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 彙整約 9 位分析師（1 強買、7 買、1 持有），平均目標價 377 美元；Goldman 目標價 2026-09-08 由 482 降至 375；UBS 2026-08-11 由中立升買進、目標價 430。頁面日期約 9 月底，確切 as-of 與現價未確認，不得與 numbers.price_at_dd 以外之價格比較","source":"Benzinga JBL price targets / analyst ratings","url":"https://kr.benzinga.com/quote/JBL/price-targets","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-06 Simply Wall St：8 位分析師 FY27 營收約 430 億、EPS 13.61（前值約 380 億、11.39）；平均目標價上調 27% 至 441 美元。與 9 月 Benzinga 平均 377 並存，來源間目標價分布不一致（Goldman 9 月降目標）","source":"Simply Wall St via Webull (2026-06-22)","url":"https://www.webull.hk/en/news/15100527365161984","excerpt":"Jabil Inc. (NYSE:JBL) shareholders will have a reason to smile today, with the analysts making substantial upgrades to next year's forecasts.","as_of":"2026-06-22","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Jabil 於 2026-01-02 以約 7.25 億美元現金完成收購資料中心電力公司 Hanley Energy Group","source":"搜尋摘要（新聞聚合）：Jabil completes Hanley Energy Group acquisition","url":null,"excerpt":"Jabil Inc. (NYSE: JBL) completed its acquisition of Hanley Energy Group on January 2 for approximately $725 million in cash.","as_of":"2026-01-02","retrieved_at":"20261012","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"FDA CDER 於 2026-08-27 對 Jabil 旗下 Pharmaceutics International（馬里蘭州 Cockeysville）發出 cGMP 警告函，檢查期間 2026-02-23 至 03-06","source":"FDA Warning Letter: Jabil Inc. 731037 (08/27/2026)","url":"https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/jabil-inc-731037-08272026","excerpt":null,"as_of":"2026-08-27","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"ems_utilization_capex_cycle#0","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"0","claim":"FY2027 資本支出指引：淨 capex 約佔營收 1.5%–2%","source":"Jabil Q4 FY2026 earnings call transcript (Webull)","url":"https://www.webull.com/news/15667757115769856","excerpt":"net capex in the range of 1.5% to 2% of revenue.","as_of":"2026-09-30","retrieved_at":"20261012","affects":["valuation","thesis.R"],"status":"ok"},{"id":"ems_utilization_capex_cycle#1","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"-","claim":"管理層稱全組織新增約 400 萬平方呎產能","source":"Jabil Q4 FY2026 earnings call transcript (Webull)","url":"https://www.webull.com/news/15667757115769856","excerpt":"we're growing capacity by about 4 million square feet.","as_of":"2026-09-30","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ems_utilization_capex_cycle#2","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"+","claim":"CFO 將新增產能與下半年更佳稼動率連結，作為利潤率擴張動能之一","source":"Jabil Q4 FY2026 earnings call transcript (Webull)","url":"https://www.webull.com/news/15667757115769856","excerpt":"better utilization of the capacity we've invested in","as_of":"2026-09-30","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"ems_utilization_capex_cycle#3","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"+","claim":"搜尋摘要稱稼動率由前一年約 75% 升至 Q2 FY26 財報會約 80%；FY25 Q3 曾稱 75%，低於正常 85–86%（為二手彙整，非逐字）","source":"Jabil Q2 FY2026 earnings call coverage (AOL) / Q3 FY25 call summary","url":"https://www.aol.com/articles/jabil-jbl-q2-2026-earnings-183643775.html","excerpt":null,"as_of":"2026-03-18","retrieved_at":"20261012","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#0","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"0","claim":"資產週轉率（聚合站 Q1 2026）：Jabil 約1.6x、Flex 約1.4x、Celestica 約2.0x、Sanmina 約1.5x（Fabrinet 對照表）；Jabil 介於 Flex 與 Celestica 之間，TipRanks 另示1.61、Value Research 示1.56 TTM。","source":"OpenCapital asset turnover pages (JBL/FLEX/CLS); TipRanks JBL statistics","url":"https://www.opencapital.sh/stocks/jbl/metrics/asset_turnover","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261012","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#1","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"0","claim":"ROIC 聚合站數字不一致：OpenCapital 示 Jabil 29.8%（Q4 2025）、Flex 19.2%、Celestica 39.5%；TipRanks 示 Jabil 16.06%，定義可能不同；Sanmina 未查到。","source":"OpenCapital JBL ROIC page; TipRanks JBL statistics","url":"https://www.opencapital.sh/stocks/jbl/metrics/roic","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261012","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#2","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"0","claim":"Lincoln International Q2 2026 EMS 季報（截至 2026-06-30）大型股毛利/營業/EBITDA 利潤率：Celestica 12.0/8.9/10.0%、Flex 9.5/5.4/7.3%、Jabil 9.2/5.1/7.1%、Sanmina 9.0/5.5/6.8%；僅為利潤率非 ROIC。","source":"Lincoln International, EMS Quarterly Review Q2 2026","url":"https://www.lincolninternational.com/publications/ems-quarterly-review-q2-2026/","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#3","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"0","claim":"Jabil FY26 Q3（截至2026-05-31）10-Q：sales cycle 5天（前季21、去年同期24）；存貨天數84（前75、74）；應付天數135（前102、96）；CCC縮短主因應付天數上升。","source":"Jabil Form 10-Q quarter ended May 31, 2026","url":"https://www.sec.gov/Archives/edgar/data/0000898293/000162828026046138/jbl-20260531.htm","excerpt":null,"as_of":"2026-05-31","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#4","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"-","claim":"Q3 FY26 財報會議：存貨天數84，扣除客戶存貨押金約68，高於目標區間55–60天，管理層預期Q4回歸正常；評論稱應付款+82%至144億美元、存貨+58%至74億美元，全年營收僅+21%。","source":"Panabee, Jabil Q3 2026 earnings coverage","url":"https://www.panabee.com/news/jabil-earnings-q3-2026","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Jabil 於 2026-01-02 以約 7.25 億美元現金完成收購 Hanley Energy Group；2026 年 7 月另收購 Rebound Electronics UK（聚合來源，未經一手確認）","source":"搜尋摘要（新聞聚合）：Jabil completes Hanley Energy Group acquisition","url":null,"excerpt":"Jabil Inc. (NYSE: JBL) completed its acquisition of Hanley Energy Group on January 2 for approximately $725 million in cash.","as_of":"2026-01-02","retrieved_at":"20261012","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"-","claim":"FDA CDER 於 2026-08-27 對 Pharmaceutics International（Jabil 旗下）發出 cGMP 警告函，涉成品藥製造違規","source":"FDA Warning Letter: Jabil Inc. 731037 (08/27/2026)","url":"https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/jabil-inc-731037-08272026","excerpt":null,"as_of":"2026-08-27","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"FDA 於 2026-08-27 發出警告函（cGMP，涉調查不明差異、批次失敗及 CAPA 不足）；搜尋未見產品召回通知","source":"GMP-Compliance.org: When 'Undetermined' is not an Answer","url":"https://www.gmp-compliance.org/gmp-news/when-undetermined-is-not-an-answer-what-two-fda-warning-letters-show-about-root-cause-analysis-and-capa","excerpt":null,"as_of":"2026-08-27","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"JBL","period":"TTM ending 2026-05-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.23,"operating_margin_pct":5.03,"fcf_margin_pct":3.89,"rd_intensity_pct":0.08},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL","as_of":"TTM ending 2026-05-31（4季加總）"},"is_subject":true},{"name":"CLS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":11.95,"operating_margin_pct":8.85,"fcf_margin_pct":3.33,"rd_intensity_pct":0.99},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"FLEX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.35,"operating_margin_pct":5.29,"fcf_margin_pct":3.68,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SANM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.01,"operating_margin_pct":5.49,"fcf_margin_pct":4.66,"rd_intensity_pct":0.26},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"JBL"},"financial_history":{"ticker":"JBL","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-08-31","revenue":33478000000.0,"revenue_yoy_pct":null,"gross_margin_pct":7.86,"operating_margin_pct":4.21,"net_income":996000000.0,"diluted_eps":6.9,"free_cash_flow":266000000.0,"fcf_margin_pct":0.79,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-08-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-08-31","revenue":34702000000.0,"revenue_yoy_pct":3.66,"gross_margin_pct":8.26,"operating_margin_pct":4.59,"net_income":818000000.0,"diluted_eps":6.02,"free_cash_flow":704000000.0,"fcf_margin_pct":2.03,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-08-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-08-31","revenue":28883000000.0,"revenue_yoy_pct":-16.77,"gross_margin_pct":9.26,"operating_margin_pct":4.98,"net_income":1388000000.0,"diluted_eps":11.17,"free_cash_flow":932000000.0,"fcf_margin_pct":3.23,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-08-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-08-31","revenue":29802000000.0,"revenue_yoy_pct":3.18,"gross_margin_pct":8.88,"operating_margin_pct":4.82,"net_income":657000000.0,"diluted_eps":5.92,"free_cash_flow":1172000000.0,"fcf_margin_pct":3.93,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-08-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/JBL/JBL_Q4_2026_Earnings_Call_20260930.md）

# Q4 2026 Earnings Call
**Jabil Inc.** | Earnings Calls | 2026-09-30

**Adam Berry** (Executives):
Good morning, and welcome to Jabil's Fourth Quarter Earnings Call and Ninth Annual Investor Briefing. My name is Adam Berry. I'm Senior Vice President of Investor Relations and Corporate Affairs. Thank you for joining us today.
Each September, this call is an opportunity for us to both report the quarter as well as give you a deeper look at our business and the opportunities that lie ahead. And as you'll hear throughout today's presentation, we have a lot to feel good about as the momentum we've seen in fiscal 2026 continues into fiscal 2027.
Before we begin, it's worth noting that today's presentation is being live streamed. The slides are available in the Investor Relations section of jabil.com, and a recording will be available after this event.
In addition, we will be making forward-looking statements during this presentation, including, among other things, those regarding the anticipated outlook for our business, such as our currently expected first quarter and full fiscal year 2027 net revenue and earnings. These statements are based on current expectations, forecasts and assumptions involving risks and uncertainties that could cause actual outcomes and results to differ materially. An extensive list of these risks and uncertainties is identified in our annual report on Form 10-K for the fiscal year ended August 31, 2025, and in other filings with the SEC. Jabil disclaims any intention or obligation to update or revise any forward-looking statements, whether as a result of new information, future events or otherwise.
Now let me set the stage for what we'll cover today. We'll begin with Greg Hebard, our Chief Financial Officer, who will review our fourth quarter and fiscal year results, cash flow and balance sheet, capital returns as well as our first quarter outlook. We will then move to Steve Borges, who will cover our Regulated Industries segment, including automotive and transportation, healthcare and renewable and energy infrastructure. Next, Matt Crowley will follow with Intelligent Infrastructure and how we're expanding our role across AI infrastructure as customer demand continues to accelerate. Following Matt will be Rafael Renno, who will discuss our newly renamed segment, Intelligent Devices and Robotics, or IDR, which will take the place of Connected Living & Digital Commerce. We feel this name change better reflects where the segment is heading in terms of automation and robotics capabilities as the mix of business continues to shift towards more highly complex engineered solutions.
Upon hearing from these 3 leaders, it will become further evident that the business remains strong and in good shape with growth coming in many key areas. In fact, when you put all of this diversified growth together, we're anticipating adding in excess of $8.5 billion of revenue in fiscal '27 after having added over $6 billion in fiscal '26. That's an unprecedented amount of growth for Jabil. Hence, we felt it was critically important for Frank McKay, our Chief Supply Chain Officer; and Andy Priestley, our Chief Operations Officer, to discuss how we're preparing to deliver this growth as well as our unique model for working with both customers and suppliers to secure the necessary components to ensure customer success. And finally, our CEO, Mike Dastoor, will bring it all together, starting with how Jabil has evolved as an engineering-led, supply chain-enabled manufacturing solutions company, followed by our fiscal 2027 outlook by end market, our capital allocation priorities and how we're thinking about the business beyond fiscal 2027. We'll then open the call for your questions.
As you will hear from the team, there are 3 key messages today. First, we're positioned for growth in fiscal '27. Our strong customer relationships and capabilities are expanding what we can deliver, while committed customer demand is filling the additional capacity we have added. Second, our commitment to product, end market and customer diversification continues to create meaningful value. AI remains strong with a broadening customer base, complemented by growth in automotive, defense and aerospace, healthcare, energy infrastructure and warehouse and retail automation. These businesses broaden our customer base and allow us to apply capabilities across markets. Finally, we're focused on converting this growth into earnings, cash flow and shareholder returns through disciplined execution, investment and capital allocation.
With that, let's get started. It's my pleasure to introduce Chief Financial Officer, Greg Hebard.

**Gregory Hebard** (Executives):
Thank you, Adam. Good morning, everyone, and thank you for joining us. I am very excited with our strong finish to fiscal '26.
Fourth quarter revenue and core earnings per share both exceeded the high end of our guidance, reflecting solid execution across the business. Revenue was approximately $10.6 billion, up 29% year-over-year and more than $1 billion above the midpoint of our June outlook. The upside was driven from Intelligent Infrastructure and Regulated Industries. I'll provide additional detail on both segments later in my remarks.
Turning to profitability. GAAP operating income was $602 million or 5.7% of revenue. Core operating income was $675 million, representing a core operating margin of 6.4%. GAAP diluted earnings per share were $3.76, while core diluted earnings per share were $4.40, up 34% year-over-year. Net interest expense for the quarter was $87 million.
Turning now to our performance by segment. Regulated Industries revenue was $3.4 billion, up 9% year-over-year and above our outlook for the quarter. Auto and transportation was the largest contributor to that upside with demand stronger than we expected. Renewable and energy infrastructure also finished ahead of our outlook. Together, those businesses more than offset lower-than-expected revenue in healthcare and packaging, where results were impacted by delays in automation equipment and the timing shift of a customer program. Core operating margin for the segment was 5.8%. In Intelligent Infrastructure, revenue was approximately $5.8 billion, up 56% year-over-year and roughly $900 million above our June outlook.
The upside was driven by 2 factors. First, AI-related demand remained very strong and continued to accelerate, exceeding the significant growth we had already incorporated in our June outlook. Second, capacity came online sooner than planned and customer ramps progressed better than anticipated, allowing us to support that higher level of demand. That growth was supported by the ramp of our second hyperscaler in Mexico and continued strength in our networking programs in India. Our power business also performed better than expected, contributing to the upside for the quarter. After being capacity constrained for much of the year, we're beginning to see our capacity investments drive growth. Core operating margin for the segment was 6.5%, up 60 basis points year-over-year, reflecting an improving mix, including the contribution of our margin-accretive Hanley Energy acquisition.
In Connected Living & Digital Commerce, revenue was approximately $1.4 billion, roughly flat year-over-year. Core operating margin was 7.1%. As Adam mentioned, we will refer to this business as Intelligent Devices & Robotics in our outlook.
Turning to cash flow and our balance sheet. Let me begin with inventory. We made solid progress in the fourth quarter, reducing net inventory days by approximately 4 days sequentially to 64, including inventory deposits. Gross inventory days ended the year at approximately 82. While net inventory days remain above our target range of 55 to 60 days, we expect continued improvement and a return to that range as we move through fiscal 2027. Cash from operations was $733 million in the quarter and approximately $2 billion for the full year. Net capital expenditures were $192 million in Q4 and $470 million for the year or 1.3% of revenue. As a result, strong adjusted free cash flow was $541 million in the quarter and more than $1.5 billion for the year, exceeding our initial FY '26 outlook of $1.3 billion plus.
Looking ahead, we continue to expect net capital expenditures of 1.5% to 2% of revenue. The asset-light nature of Intelligent Infrastructure enables us to support strong growth while continuing to invest across our diversified portfolio. We exited fiscal 2026 with a strong balance sheet with debt to core EBITDA of 1.3x and cash balances of approximately $1.7 billion.
Turning to our capital structure. We ended fiscal 2026 with approximately $6.1 billion of total available liquidity, including $4.4 billion of unused borrowing capacity. Balance sheet debt was approximately $3.4 billion. Our strong financial position provides the flexibility to support customer growth, continue returning capital to shareholders while maintaining our commitment to an investment-grade credit profile.
Turning to shareholder returns. We repurchased approximately $169 million of shares in the fourth quarter and approximately $1.1 billion for the full year. That builds on our consistent track record of returning capital to shareholders. Since fiscal 2013, we've reduced shares outstanding from approximately 203 million to approximately 104 million, a reduction of 49%. Over that period, we've repurchased shares at an average price of $58 and returned $8.8 billion to shareholders through repurchases and dividends. During the fourth quarter, we completed our prior repurchase authorization and began repurchasing shares under the new $1.5 billion program authorized by our Board in July. Approximately $1.4 billion remained available at year-end. Our long-term framework remains unchanged: return 80% or more of adjusted free cash flow to shareholders over time while continuing to invest for growth.
With that, let's turn to our first quarter guidance, beginning with revenue by segment. For Q1, we anticipate Regulated Industries revenue of approximately $3.5 billion, up about 12% year-over-year. The growth is expected to be led by auto and transportation, driven by programs in defense and aerospace and automotive, along with continued momentum in renewable and energy infrastructure. For Intelligent Infrastructure, we expect strong growth to continue, with revenue of approximately $6.3 billion, up about 63% year-over-year. AI-related demand remains very strong and continues to accelerate. We expect customer ramps and additional capacity coming online to support that growth. In Intelligent Devices & Robotics, we expect revenue of approximately $1.2 billion, down about 10% year-over-year.
Putting it all together at the enterprise level, total company revenue for Q1 is expected to be in the range of $10.6 billion to $11.4 billion. GAAP operating income is expected to be in the range of $481 million to $541 million. Core operating income is estimated to be in the range of $592 million to $652 million. GAAP diluted earnings per share is expected to be in the range of $2.78 to $3.18. Core diluted earnings per share is estimated to be in the range of $3.80 to $4.20. Net interest expense is estimated to be approximately $95 million for Q1 and in the range of $390 million to $400 million for the full year. Our core tax rate for Q1 and for the fiscal year is expected to be 20%.  
Let me close with our full year results and the longer-term progress shown on the next 2 slides. Since fiscal 2020, core operating margin has increased from 3.2% to 5.8%, and together with our share repurchase program has driven core earnings per share at a compound annual rate of approximately 29%. Our asset-light model has also enabled stronger cash generation with less capital, reducing net capital expenditures from 2.9% of revenue to 1.3%, while more than tripling annual free cash flow. That's a strong track record and one we are proud of.
Our business has evolved considerably over that period, but our focus has remained consistent: strengthening the portfolio, expanding margins and converting earnings into cash. We saw the value of that approach again this year. Intelligent Infrastructure led our growth; and automotive, energy infrastructure and digital commerce also contributed. The strength of our diversified portfolio gives us multiple opportunities to grow, and we'll continue to allocate capital toward the market and capabilities where we see the most attractive long-term returns.
We enter fiscal 2027 with strong momentum and broader participation across our end markets. Our focus remains on delivering that growth with the same financial discipline that has driven our progress to date. Our business leaders will now discuss those opportunities in more detail before Mike takes you through our strategy and full year outlook.
Steve, let me turn it over to you to begin with Regulated Industries.

**Steven Borges** (Executives):
Thanks, Greg. Good morning, everyone. I lead Jabil's Regulated Industries segment, which brings together automotive and transportation, defense and aerospace, healthcare and packaging and renewable energy infrastructure. These businesses share an important characteristic. They compete in markets where trust is earned over years, not quarters. Qualification cycles are lengthy, certification requirements are rigorous and customers depend on consistent execution throughout programs that often remain in production for a decade or longer. That creates durable customer relationships and gives us the opportunity to expand our role over time. We often begin by supporting a specific product, and as confidence and performance increase, we broaden our engagement into adjacent technologies, additional manufacturing processes and increasingly complex system-level solutions. Deepening these relationships remains one of the strongest drivers of value creation across the segment.
Looking ahead to fiscal 2027, we remain optimistic about the outlook across Regulated Industries. Automotive is benefiting from a more balanced technology mix. Defense and aerospace is gaining momentum as new programs move into production. Healthcare is expected to return to growth, while renewable and energy infrastructure is benefiting from improving market conditions and overall demand. Although we remain mindful of the broader demand environment, the long-term trends supporting these businesses remain compelling.
Let me start with automotive and transportation. This business returned to growth faster than we anticipated, driven by strong operational execution, improved win rates with strategic customers and disciplined portfolio management. Over the past several years, we have intentionally repositioned the automotive business towards higher-value opportunities, including software-defined vehicles, advanced driver assistance systems, vehicle compute and powertrain-agnostic technologies that support internal combustion, hybrid and battery electric platforms.
That strategy is working. We have reduced the share of electrification and powertrain programs in our portfolio from approximately 80% in fiscal 2023 to about 40% in fiscal 2026. Software-defined vehicle, compute and advanced driver assistance programs represent much of the balance. This more balanced mix positions us to perform across multiple technology pathways as the market evolves. While regional dynamics vary, we continue to see strong momentum across the board. In the U.S., our growth is increasingly tied to powertrain-agnostic technology. In Europe and in China, we are seeing increased adoption of advanced technologies across battery electric platforms. Our European pipeline continues to expand as existing customers extend these architectures across global vehicle platforms and respond to ongoing localization requirements. Approximately 90% of fiscal 2026 automotive revenue came directly from original equipment manufacturers. As OEMs rethink their strategies, outsourcing is becoming more prevalent.
Jabil is well positioned to benefit from these trends. Our customer relationships, engineering expertise, advanced manufacturing know-how and resilient global supply chain enable us to participate in the highest value, most complex areas of the autonomous, connected, electrified and software-defined vehicle market. Beyond automotive, we see attractive potential across the broader portfolio. Defense and aerospace is expected to become an increasingly meaningful contributor in fiscal 2027 as new programs move into production. Across both established industry leaders and emerging technology companies, customers need partners that can move complex products from design to high-volume production while meeting demanding quality, security and scale requirements.
This is where Jabil's breadth of capabilities becomes a competitive advantage. By bringing together engineering, systems integration and supply chain expertise from across Jabil, we can support increasingly complex products and expand our role from electronic assemblies to complete integrated systems. Our immediate focus is executing today's program ramps while preparing the business for its next phase of expansion.
Turning to healthcare. This remains a stable business with an attractive long-term growth profile. As I mentioned earlier, these customer relationships are built over many years, creating durable partnerships and strong visibility. We expect the business to return to growth in fiscal 2027 as customers launch new products and increasingly rely on Jabil for complex manufacturing solutions. Medical technology companies increasingly need partners that can integrate engineering, global supply chain expertise and regulated manufacturing at scale. That combination differentiates Jabil and enables us to capture additional share as outsourcing expands.
We are investing in high-value areas, including minimally invasive technologies, sterilization, medical device reprocessing and pharmaceutical solutions. These investments broaden our addressable market, deepen existing relationships and support long-term value creation with attractive margin opportunities. Drug delivery is a good example of that strategy in action. Across insulin delivery, biologics and weight loss therapies, customers need partners that can manufacture highly reliable devices at scale. We combine precision manufacturing with deep process expertise to help our customers bring these next-generation therapies to market efficiently.
To illustrate the scale of that opportunity, we expect to manufacture more than 700 million injectors and delivery pens in fiscal 2027. This reflects both the breadth of our participation in drug delivery market and our growing role in several of the fastest expanding therapeutic categories. Our pharmaceutical solutions business, which we expanded through the acquisition of Pii is a natural extension of that strategy. As we move through fiscal 2027, our focus is on executing customer product launches, expanding capacity where demand supports it and investing selectively in the technologies that will sustain growth in the years ahead.
Finally, let's turn to renewable and energy infrastructure, where market conditions improved throughout fiscal year 2026. We're seeing encouraging signs across our energy-related business with solar remaining an important part of the portfolio. More importantly, customer investment is broadening into energy storage, electrical infrastructure and thermal management solutions. Electricity demand continues to accelerate, driven by electrification, industrial expansion and the rapid growth of data centers. That demand is increasing investment across the energy value chain from power generation and storage to grid modernization, distribution equipment and power management.
While the pace of customer investment will vary by end market, our strategy is focused on the areas with the strongest long-term potential, energy storage, grid power solutions, HVAC and data center cooling, commercial power and the broader energy infrastructure. To strengthen our position, we are investing in engineering capabilities, vertical integration, strategic partnerships and targeted inorganic growth in power electronics and low-voltage switchgear.
In closing, trust remains the common thread across Regulated Industries. Long-standing customer relationships, differentiated technical expertise and disciplined investment provide a strong foundation for sustainable growth and attractive long-term returns.
I'll now turn it over to Matt to discuss Intelligent Infrastructure.

**Matt Crowley** (Executives):
Thanks, Steve. Good morning, everyone. I lead Jabil's Intelligent Infrastructure segment. We continue to feel very good about Intelligent Infrastructure. Demand for AI infrastructure remains strong and continues to accelerate. As customers expand their infrastructure, the systems they need are becoming more complex. That creates more opportunities for Jabil. Fiscal '26 reflected that. Segment revenue grew more than 40% and AI-related revenue was up 60% year-over-year. And we ended the year with 4 customers with AI-related revenue above $1 billion annually, up from one $1 billion customer 2 years ago. Additionally, we added a third hyperscale customer in the third quarter of this year, all proof points that our strategic focus on capability is resonating with customers and the market.
Behind those results is how we think about the data center. It's one complete system, and we've built the capabilities required across the entire system. Compute, storage and networking need to work with the power and cooling around them. A change in one area affects the others. A simple example of this is putting more compute and GPUs into a rack requires more power and generates more heat. This changes both the cooling design and the way power is delivered, while the network and optical connections have to keep pace.
Working through those choices with the customer is where our engineering is making a difference. We're investing in those capabilities and getting involved earlier, often before a program reaches the quotation stage. 4 of our 6 largest data center wins this year began that way as design engagements. That early involvement is what we mean by engineering-led and silicon to solutions. We can engage around the silicon, help design and integrate the rack and support the infrastructure around it.
With that strategic concept in mind, let me walk you through our 3 end markets in the order we report them. Capital equipment comes first because it's where we participate earliest in the investment cycle. AI complexity and custom silicon are raising the demands on semiconductor test, and wafer fab investment is creating opportunities in the tools that make chips. In both areas, we're taking on more of the tool, moving from components into modules and subsystems. This year, we brought a new site in Vietnam into production, and we're building complete subsystems for a new generation of memory testers using thermal control that came out of our data center work. Capital equipment revenue grew about 20% in fiscal '26, and we expect fiscal '27 to be an even stronger year with growth of 40% as the wafer fab equipment cycle recovers and ATE demand remains strong.
Cloud and data center infrastructure is our largest end market. Liquid cooling is a good example of how we grow there. A customer may come to us with a thermal problem. As we work through it, the discussion expands to the design and integration of the rack. We solve the initial problem, demonstrate what we can do and earn the opportunity to take on more. That's how our largest account developed, from a server and rack program into servers, racks, power, cooling and services. Our second hyperscale customer started with a single capability and has grown into a storage program above $1 billion in annual revenue. That expansion doesn't stop at the rack. The power and cooling infrastructure around it also has to be ready, and customers increasingly want that equipment built and tested before it reaches the site.
In Guadalajara and Salt Lake City, we're building modular data centers, power and cooling modules built and tested in the factory, so customers reach power months sooner. Prefabricated modules aren't tied to critical path at the construction site and customers can line up revenue much more closely with their costs.
Hanley takes that one step further. It adds power engineering, deployment and services to our manufacturing capabilities so we can help customers commission equipment and maintain it after installation. That services capability is the highest margin business in the segment. We're seeing the same pattern in networking, which is one of the opportunities we're most excited about. As AI workloads grow, more of the network is moving into dedicated racks with higher capacity systems to address more complex topologies for neural networks.
When a switch customer needed capacity for a new generation of AI switches, we brought production in India online at record pace. Those lines now build liquid-cooled network racks. Our photonics team supplies the silicon photonics transceivers that connect them and co-packaged optics move the optics onto the switch silicon. It also grows with how much AI is used, not with the size of any single model, but I'll come back to that.
Across all 3 markets, we've built the business around capabilities that work across different customer platforms. Customers can choose different silicon and networking architectures, and we can help them bring the system together. That's a deliberate choice. Others in the industry are building product companies around their own power and cooling platforms and asking customers to standardize on them. That's a legitimate model.
Ours is different. We help customers build the system they've designed with their silicon, their architecture and whichever suppliers they choose. And we bring our own technology where it fills a gap in cold plates, chillers and power distribution. That matters in 2 ways. It widens the programs we can win because we aren't competing with the customers' other choices and our position doesn't depend on any single product surviving the next architecture change. The engineering, integration and test carry forward.
Turning to fiscal '27. We expect Intelligent Infrastructure revenue to grow 43% year-over-year with all 3 end markets growing double digits. We expect AI-related revenue to grow 50-plus percent year-on-year and 5 customers with revenue above $1 billion. The business should also continue to be asset-light because the capacity we're adding is tied to programs already booked. That is central to our strategy, and it shows up in return on invested capital, which we believe is a clear advantage of our model over our competitors.
An outlook like that raises a fair question about volatility in the AI trade. So let me be direct about how we think about it. To me, it all starts with where our demand comes from. The AI spending that makes headlines is at the frontier, small number of labs training the most capable models on the largest clusters ever built. Most of our business is not there. It is in deployed AI models that already exist, running at scale for the world's largest cloud platforms and the enterprises they serve. That's inference. It grows with usage. It needs storage, networking, power and cooling as much as accelerators. And much of what we build is needed whether a customer is adding capacity or upgrading what's already installed.
I also said I'd come back to networking because it's the clearest example. Our direct exposure to frontier model developers is a small fraction of our AI-related revenue. And then something else worth highlighting is the diversification across the segment. Capital equipment follows the semiconductor cycle, while cloud infrastructure and networking follow data center deployment. Within the data center, racks, power and cooling, service and test have different buyers and different timing. And a large share of Jabil's revenue and operating profit sits outside this segment, where the same thermal, power and test capabilities are increasingly relevant as AI reaches energy, healthcare, automotive and automation. That helps to lower the volatility of our earnings and lets us keep investing through a downturn.
Our immediate focus is to turn that capacity into reliable production. We're working with operations and supply chain to have people, processes and materials ready as programs ramp. The combination of a broader role with customers and disciplined investment gives us confidence in the business we're building.
Rafael, I'll turn it over to you.

**Rafael Renno** (Executives):
Thank you, Matt. Good morning, everyone. My name is Rafael Renno, and I'm pleased to be here with you today. Over the past 21 years at Jabil, I've held a variety of leadership roles, building and managing strategic customer relationships across the company. Today, I lead Jabil's Intelligent Devices & Robotics segment. As Adam mentioned briefly, we renamed the segment to better reflect our strategy and the ongoing evolution of the business. Today, our portfolio spans intelligent devices, automation platforms and robotics that bring AI into the physical world from warehouses to industrial environments to public spaces and our homes.
Over the past several years, we've been reshaping the segment around opportunities that deliver stronger margins, better returns and deeper customer relationships. That strategy continues to guide both end markets, Connected Living and Commerce & Robotics. To accomplish the ongoing transition from consumer-based products to robotics and automation, we leverage our strong capabilities in optics, robotics and advanced precision mechanics to enable the design, industrialization and delivery of our customers' complex engineered products. This expertise also forms the foundation of our physical AI stack and will remain an important investment area.
Within Connected Living, we continue to prioritize profitability over volume, exiting or deemphasizing programs that did not meet our return requirements. As a result, the business is more focused, more disciplined and better positioned for long-term success. Today, Connected Living serves customers across public safety and vision systems, home automation and lifestyle devices as well as other complex consumer and commercial systems. We are increasingly concentrating the portfolio on higher-value products where engineering complexity, supply chain execution and regional manufacturing create meaningful differentiation.
Regional manufacturing has become especially important as customers respond to evolving geopolitical dynamics and new regulatory requirements, particularly for products such as foreign-produced drones and communication devices. Within Commerce & Robotics, we continue to evolve the portfolio with an even greater emphasis on robotics and automation and the physical AI stack across warehouses, retail environments, fulfillment networks and other industrial settings, customers are investing in automation to improve efficiency, address labor constraints and increase productivity. These are long-term secular trends that continue to gain momentum.
Jabil supports a broad range of automation platforms, including ASRS warehouse systems, mobile robots, retail technologies and autonomous last-mile delivery solutions. Our ability to help customers industrialize and scale complex products globally position us well to benefit from continued adoption. One of our customers described the value of this partnership well.

**Michael Trueblood** (Attendees):
Hello, my name is Michael Trueblood, Vice President of Procurement at Symbotic. Since 2023, Jabil has been a trusted partner in scaling Symbotic's bot production. Their engineering rigor, manufacturing expertise, global sourcing capabilities and commitment to world-class quality enable us to move quickly while maintaining disciplined execution. Since entering mass production in early 2024, we reached 10,000 bots in June of 2025 and are now approaching 20,000 in total. Jabil's collaborative approach helps us address challenges early, supporting our continued growth and next generation of innovation.

**Rafael Renno** (Executives):
That reflects exactly how we're building across this business, long-term customer relationships grounded in engineering depth, manufacturing excellence and disciplined operational execution. Those capabilities also give us the foundation to participate in emerging markets. For example, our experience in complex automation and high-volume manufacturing allow us to engage early with customers developing humanoid robots and the precision mechanical systems that enable them, including actuators and robotic hands. We help move these products from design into repeatable, reliable, high-volume manufacturing. Over time, we expect these capabilities to extend further into physical AI as more intelligence moves into machines, warehouses, retail environments, public spaces and industrial settings.
As we enter fiscal '27, we have a stronger business. Connected Living is more focused. Commerce & Robotics is a credible growth engine today. The capabilities we've built create additional avenues for expansion while physical AI represents a significant long-term opportunity as the market develops. That is how we intend to build the business behind the new name.
Andy will now explain how our global operations team prepares new programs for production and supports them as they scale.
Andy, over to you.

**Andy Priestley** (Executives):
Thanks, Rafael. Good morning, everyone. I lead Jabil's global operations across more than 120 facilities. We spent much of the past year preparing those factories for our customers' growth. We're now beginning to fill the additional capacity with the committed business. For our operations team, that means flawlessly bringing programs into production and increasing output all while maintaining the highest standards for safety, quality and delivery.
As production moves closer to the end customers, we're expanding our footprint across the United States in places like Mississippi and Virginia as well as internationally in India, Mexico, Brazil and Vietnam. Our expansion gives us more room to grow in the regions where our customers need us most. The equipment, people, processes and supply chain all have to come together before a facility can deliver at scale. That work becomes even more demanding as products become more complex. Liquid-cooled systems, for example, require specialized assembly and test capabilities alongside the space to build them. We're preparing our people and manufacturing processes around those requirements, so customer programs can move seamlessly into mass production.
To handle that combination of greater volume and greater complexity, we're continuing to invest in physical AI and automation. On the factory floor, we're expanding automation in areas such as material movement and inspection. These investments improve consistency and productivity while allowing our people to focus on the higher value work that requires their expertise. This is particularly important as we support customers closer to their end markets, including in the high-cost regions. We're also focused on making those investments more fungible. Flexible automation allows us to adapt and reuse equipment as products change, helping us respond faster to new customer requirements while improving returns on deployed capital.
Alongside that automation, we're investing in computer vision to support automated optical inspection with the goal of using what we learn to prevent defects before they occur. The opportunity also extends outside of the production line. AI tools that simplify workflows and automate transactions give our teams more time to resolve issues and support launches. All these capabilities help us ramp programs faster, identify issues earlier and use equipment more effectively and efficiently. Once a solution has proven effective, we want other sites and businesses to benefit from it. Our regulated customers in healthcare and automotive, for example, require validated processes, consistent quality and traceability.
Commerce & Robotics customers need help bringing complex large form factor automation products into production. The requirements often differ, but experiences developed in one part of Jabil can improve how we serve customers elsewhere. This is one practical benefit of our diversified portfolio and our focus for the coming years to put it to work as new programs ramp. We want customers to know that they can grow with Jabil. We want that growth to come with better productivity and disciplined investment. Material availability has to keep pace with that production, however. Frank and his team are working alongside us to make that happen.
Frank, over to you.

**Francis McKay** (Executives):
Thanks, Andy, and good morning, everyone. As Andy said, being ready to manufacture is only part of being ready to deliver. Customers also need confidence that components will be available when production needs them. That confidence starts with supply chain resilience, which for Jabil is an operating discipline that directly affects continuity, cost and growth for our customers. We're seeing real constraints today. Memory, in particular, is being reallocated towards AI and hyperscale demand, tightening supply across many of the diversified end markets that we serve. We view this as a structural shift in global capacity compounded by ongoing geopolitical disruption, and we work with customers and suppliers to understand where those pressures could affect a launch or production schedule so that we can act early.
Our supplier relationships are central to that work. We've identified about 120 strategic partners that we engage like customers. We share road maps and executive-level relationships. In constrained markets, allocation follows trust as much as order size does. That's where those relationships pay off directly for our customers, helping us work through allocation, qualify alternate sources and coordinate commitments needed to support a ramp. We bring Jabil's purchasing scale to those discussions alongside our customers' own procurement capabilities. In cloud and data center infrastructure, for example, large customers play a key role in securing supply and coordinating their requirements with our supplier relationships and production plans helps us get material to the factories where needed.
Structurally, what we do works in part because procurement reports into supply chain. Sourcing, execution and tailor-made customer supply chain architecture decisions are not made in silos. We're building on that foundation by improving visibility across suppliers and our logistic networks, evaluating regional production and nearshoring strategies and developing AI tools to identify constraints much earlier than we could have in the past. The goal is simple, know which customer programs are affected when demand shifts or a supplier falls behind and have options ready before issues reach the production line.
For the year ahead, our focus is on delivering reliably as customers scale, managing cost and keeping material commitments aligned with demand, helping customers maintain continuity while protecting the capital needed to fund their growth. As we do this, Jabil becomes a more strategic partner in an increasingly uncertain environment.
I'll now pass it off to Mike Dastoor. Thank you.

**Michael Meheryar Dastoor** (Executives):
Thanks, Frank. Good morning, everyone. Before I get into the outlook, I want to thank our teams around the world. We asked a great deal of them this year, bringing capacity online, supporting demanding customer ramps and delivering a much stronger finish than we expected in June. I'm extremely pleased with what they accomplished and grateful for their commitment to our customers and each other.
As you heard from Greg today, fiscal 2026 was yet another exceptional year for Jabil. Year-on-year, we grew revenue by 21%, expanded core operating margin by 40 bps, delivered 34% growth in core earnings per share and expanded free cash flow by more than $200 million. Our AI-related business drove much of that growth, but automotive, energy infrastructure and digital commerce performed very well, too. And we accomplished all of this while progressing extremely well on a number of customer ramps and bringing critical capacity online in Southeast Asia, the U.S., Mexico and India, which sets us up to deliver even more growth in fiscal 2027 and beyond.
But before we get to fiscal 2027, I want to spend a few minutes on how this company has evolved over the last several years because it explains why we're so confident in what comes next. Let's start with gross margin. The mix shift toward higher-value markets has lifted it more than 200 basis points since fiscal 2020 to 9.2%. We exited lower-margin business with the mobility divestiture and more of our revenue now comes from Regulated Industries, Intelligent Infrastructure and Digital Commerce, where the work is more complex and the relationships run deeper. Put simply, we're moving up the value chain, taking on more of the engineering, supply chain integration and complexity that increases our value proposition to customers. And we did that in a year when revenue grew 21%, and we were building out significant new capacity for the growth ahead.
At the same time, we've become structurally less capital intensive. Net CapEx is down to 1.3% of revenue from 2.9% in fiscal 2020. Our AI business is growing rapidly with lower capital intensity. We structure programs with customers so the investment matches the commitment, and we prioritize organic investment toward the higher returning parts of the portfolio. Last year, we supported $36 billion of revenue on about $470 million of net CapEx. Not everyone in our space can say that. And looking ahead, we expect that asset-light model to continue with net CapEx in the range of 1.5% to 2% of revenue. Higher margins and lower CapEx shows up in cash flow. Adjusted free cash flow has more than tripled since fiscal 2020 to $1.5 billion, and we converted approximately 110% of core net earnings into cash last year, even as revenue grew 21%. That cash gives us the flexibility to invest in the business and return capital to shareholders at the same time. And with the growth ahead, I expect it to keep building.
The higher margins and asset-light model and strong free cash flow has resulted in strong return on invested capital even as we continue to grow. Our core ROIC has nearly tripled since fiscal 2020 to 59%. I like that a lot. It tells me the quality of the business is improving, not just the size. Over the years, we've evolved from a contract manufacturer to an end-to-end complex manufacturing solutions service provider. We've been deliberate about building an engineering-led, supply chain-enabled manufacturing solutions company. That's more than a tagline. It says something important about what we are and what we are not. We are not a contract manufacturer competing with low-cost EMS companies, nor are we a product company competing with our customers. We build a diverse set of capabilities and deploy them in whatever combination the customer needs to deliver complex solutions for their products and services. That's why they trust us with their most important programs, and it's why our vision is to be the world's most technologically advanced and trusted manufacturing solutions service provider.
That vision rests on 3 core strands. Let me take each in turn. First, engineering. We have more than 9,000 engineers helping customers solve technical problems and develop products that can be built efficiently and at scale. Being engineering-led means we get involved earlier in the customer's decision cycle often before the product design is locked. That's where design for manufacturing matters most. Our engineers shape the design so it can be built reliably at the right cost and at volume, followed by industrialization, the work of taking a product from prototype to a stable scale production line, and we use value engineering to take cost out along the way. We do that faster than most, and it's one of the reasons customers bring us their most demanding ramps. Once we're embedded that early, we're very hard to displace. Design wins become long-term relationships, and we take on more of the customers' challenge from development through production.
Second, supply chain. This is a capability people tend to underestimate. We manage approximately $35 billion of global spend, 40,000 suppliers and 1 million parts with roughly 3,500 procurement and supply chain professionals. Our supply chain expertise is even more valuable in today's increasingly complex global environment where geopolitical uncertainty, regional conflicts and structural component constraints continue to challenge our customers. Our continued investment in supply chain capabilities, systems and long-term supplier relationships enables us to help customers mitigate risk, enhance resilience and maintain continuity.
Third, manufacturing, and this is where the diversity of our capabilities really shows up. While each customer has its own unique requirements, our advantage lies in combining the full breadth of Jabil's capabilities under one roof, enabling every customer to benefit from expertise developed across the enterprise. Thermal management developed for data centers helps in semiconductor test, automotive and energy storage. Precision manufacturing built for healthcare helps in other regulated markets. Very few manufacturing companies can bring that breadth to our customer, and I like that combination, deep domain expertise with the resources of the broader company behind it.
Behind those strengths is a leadership team with more than 200 years of Jabil tenure. They know our customers, they know our factories, and they've worked together through several up and down economic cycles. That continuity matters when you're ramping the kind of capacity we are. And this team runs a footprint of more than 120 sites in 30 countries around the world, which lets us build where our customers need us. The capacity we added this year in Southeast Asia, the U.S., Mexico and India is the latest example. It's worth highlighting that we now have more than 40 sites in the U.S. as we continue to support our customers' reshoring activities. Jabil manages a balanced portfolio of long-term strategic partnerships across 3 focus segments with many of the world's most respected companies. These aren't transactional relationships. Many of them go back a decade or more, and they've grown as our capabilities have grown.
Let me now walk through our fiscal 2027 outlook for each segment, beginning with Regulated Industries. The outlook for Regulated Industries has improved considerably from where we started fiscal 2026. We now have several end markets contributing to growth. In automotive and transport, we expect approximately $5 billion in revenue, up about 9%. We finished fiscal 2026 at approximately $4.6 billion in revenue and now expect another year of growth. Within automotive, we continue to feel very good about our position with some of the world's best makers of electric and ICE vehicles, and we broaden those relationships through vehicle compute, advanced driver assistance and the high-performance electronics behind increasing adoption of FSD and autonomous vehicles.
We believe defense and aerospace, which sits within this end market, will be an important growth driver in fiscal 2027 and beyond. Governments are modernizing platforms and replenishing inventories of critical systems, increasing the role played by Jabil, a U.S.-based ITAR-compliant manufacturing solutions provider. That's a market with real barriers to entry, registered facilities, security cleared personnel and a qualified quality system. We have all 3 in place. Our faster production lead times are critical here as efforts to replenish inventories gains momentum.
Healthcare is another end market I feel very good about. For healthcare and packaging, we expect approximately $5.6 billion in revenue, up about 6%. Outsourcing in healthcare continues to be relatively immature and customers are increasingly looking for a partner that brings engineering, supply chain scale and regulated manufacturing together. That plays directly to what we do. Our healthcare pipeline for FY '28, particularly looks robust with book business coming online towards the end of FY '27.
In renewable and energy infrastructure, we expect approximately $3 billion in revenue, up about 7%. Here, the business we're building has broadened beyond residential solar. Commercial projects and energy storage are increasingly important as data center power demand continues to create opportunity in this end market. Putting those markets together, we expect Regulated Industries revenue of approximately $13.6 billion in revenue, up about 7%. Defense and aerospace, automotive, healthcare and energy infrastructure each bring different customer programs and different growth drivers. That breadth is invaluable.
Turning to Intelligent Infrastructure. AI demand remains strong, and our outlook continues to accelerate. In fiscal 2026, the team delivered approximately $14.4 billion of AI-related revenue, up $5.4 billion year-over-year. In fiscal 2027, we expect that to grow to approximately $22.1 billion, up 54%. What is really impressive about this is that's another $7.7 billion at a higher growth rate on top of a much larger base, even from our expectations in June. As Matt said earlier, most of our AI business supports everyday AI usage rather than frontier model training, which makes our demand less exposed to swings in the AI spending boom. Our holistic approach of focusing on various engineering capabilities across semi-cap equipment and data center build-outs is clearly resonating with customers.
Starting with capital equipment. For fiscal 2027, we expect approximately $4.2 billion in revenue, up approximately 40%. Demand for automated test equipment remains strong as customers introduce more complex silicon and memory. At the same time, the wafer fabrication equipment market is inflecting higher, providing another driver of growth. I like both the improving demand outlook and the durable customer relationships we're building in this business.
In cloud and data center infrastructure, we expect approximately $17.5 billion in revenue, up approximately 52% as the capacity we've invested in throughout the year ramps. We're filling that capacity with committed business. We've expanded the relationships with our second hyperscaler by executing well and bringing them additional capabilities, and that ramp in Mexico is contributing to growth. I expect the second hyperscaler to be a 10% plus customer in FY '27. We also discussed our third hyperscaler win in June. We continue to expect modest contribution in fiscal 2027 with the greater opportunity beyond that. Our role is also broadening beyond the rack. Higher density systems need more sophisticated power distribution and liquid cooling. Our Hanley Energy acquisition adds modular power and energy management together with deployment and service expertise.
In networking and communications, in spite of a subdued 5G market, we expect to be up approximately 15% at approximately $3.9 billion in revenue with our advanced AI networking programs in India being a major contributor. The investments we made back in 2023 with the Intel acquisition, along with our investments in high-speed interconnects and optics position us well to support co-packaged optics and co-packaged copper technologies as they start to scale. For the Intelligent Infrastructure segment overall, we expect approximately $25.6 billion in revenue, up about 43%. Not only do we have a diverse set of capabilities, we have a diversified customer portfolio. In fiscal 2027, we expect 6 customers in this segment to each generate more than $1 billion of revenue. That breadth and the capabilities behind it is why I feel so good about this outlook.
Turning to Intelligent Devices & Robotics. The new name reflects where we're taking the business, led by Digital Commerce & Robotics, which we expect to generate approximately $3 billion in revenue, up approximately 11%. Retailers, warehouses and distribution centers continue to invest in automation, whether that's behind the scenes in the aisle or at checkout. We have the engineering, robotics and system integration capabilities to support those investments, and I continue to like the opportunity here. As early participants, we continue to make good headway in building out our engineering capabilities around physical AI. Our forecast for physical AI continues to be modest and conservative. I expect that to grow substantially in the mid- to longer term beyond FY '27.
In Connected Living, we expect revenue to decline about 15% to approximately $2.3 billion. Here, we remain committed to competing on capability, complexity and value creation, not on being the lowest cost provider. We also remain conservative around memory constraints in this market. The decline in Connected Living more than offsets the growth in Digital Commerce & Robotics, bringing our IDR outlook to approximately $5.3 billion in revenue, down about 2%.
So when I add up all 3 segments, we expect fiscal 2027 revenue of approximately $44.5 billion, up about 24%. AI is clearly our largest growth driver. At the same time, we expect robust growth in warehouse and retail automation, defense and aerospace, automotive, healthcare and energy infrastructure. Those areas serve different customers on different time lines. There's no single point of dependence, and I like that breadth.
So what does that growth mean for the bottom line? On that revenue base, we expect core operating margin of 6.1%, an improvement of 30 basis points and core diluted earnings per share of $17.55, up about 34%. The margin expansion comes from 3 areas: strong revenue growth, better utilization of the capacity we've invested in and an improving mix of business. As volumes scale, we leverage our fixed costs more effectively, and that's a more durable foundation for earnings and cash flow. We expect that earnings growth to support another year of strong adjusted free cash flow generation of approximately $1.6 billion.
On capital allocation, our priorities haven't changed. Our strong balance sheet and low leverage provides us with optionality. We'll invest organically where we see attractive returns, including AI infrastructure, healthcare and warehouse and retail automation. We have substantial opportunities within this business, and we intend to continue building out our capabilities with one eye on the rapid pace of technology evolution and another eye on line of sight capacity requirements while staying disciplined about returns. We'll also consider acquisitions that add capabilities that will enable us to offer end-to-end solutions to our customers. Mikros Technologies and Hanley Energy are good examples, specialized expertise in liquid cooling that we can apply in semi-cap equipment, networking, servers and racks and data center power that we can combine with our data center infrastructure business. And we remain committed to returning 80% or more of adjusted free cash flow to shareholders over time.
Share repurchases remain a top priority as is evidenced by our continued aggressive buybacks. We fully utilized the prior authorization in Q4 and have begun buying shares under the new $1.5 billion program our Board authorized in July. We'll do all of that while maintaining our investment-grade credit profile and the flexibility to support our customers. I feel good about our ability to invest for growth while returning substantial cash to shareholders.
For fiscal '28 and beyond, here's how I'm thinking about the business. I don't see AI growth slowing down anytime soon. Inference workloads keep expanding, and that drives demand for the infrastructure we build. And the capacity we're ramping for fiscal '27 means we exit the year at a meaningfully higher capacity, which sets us up well for FY '28. At the same time, the rest of the portfolio is growing, too, rising defense spending, data center power demand pulling through energy storage, a healthcare pipeline that includes Croatia. I also remain extremely bullish on the India data center build-out through our strategic alliance with the Adani Group. And I'm excited about the opportunity that co-packaged optics proliferation presents for us in networking, along with physical AI moving to the next stage of commercial deployment.
So while AI is leading the way, we expect all 3 segments to contribute. And as we continue to move up the value chain, we expect that mix to keep pushing core operating margin higher over time. When you put that kind of revenue growth and margin expansion together and add the buybacks on top of it, that's what gets core earnings per share growing well above revenue. And because we run an asset-light model with net CapEx in that 1.5% to 2% range, it also drives strong free cash flow. We continue to expect free cash flow conversion above 100% over time. That's what allows us to keep returning 80% or more of it to shareholders, primarily through buybacks while maintaining our investment-grade credit profile and sustaining strong returns on invested capital.
So when I step back, I'm confident in where Jabil sits today, strong customer demand across multiple end markets, committed business filling the capacity we've invested in, a model that turns that growth into strong returns and cash flows with further growth opportunities beyond FY '27. And we have the people to bring it all together. To our teams around the world, thank you for the integrity, ingenuity and inspiration you bring to our customers, our communities and each other every day. You are the foundation of this business and the reason we can look ahead with confidence.
With that, I'll turn it back to Adam.

**Adam Berry** (Executives):
Thanks, Mike. Before we open the call for questions, let me come back to the 3 messages we started with. First, we're entering fiscal 2027 with strong demand, committed customer business and added capacity. Second, diversification is creating value across AI infrastructure, defense and aerospace, automotive, healthcare, energy infrastructure and automation. In AI infrastructure alone, 5 customers are expected to exceed $1 billion in fiscal 2027. Finally, disciplined execution, capital allocation and Intelligent Infrastructure's asset-light model are helping convert this growth into earnings, cash flow and shareholder returns.
Thank you for joining us today. Operator, we're now ready for questions.

**Operator** (Operator):
[Operator Instructions] Today's first question is coming from Steven Fox of Fox Advisors.

**Steven Fox** (Analysts):
Thanks for all the great detail this morning. I guess for my first question, kind of big picture, Mike, but maybe you just gave a ton of detail on how you guys are executing. But as we think out to sort of this -- what have you done for us lately question now that you're looking at like $8.5 billion of growth. I guess, how do we think about the challenges to execute to that number in this year and how they're different from last year? And then along those lines, how that gets you to the 6.1% operating margin? In other words, how much is just sheer operating leverage from volume versus things that you control? And then I had a follow-up.

**Michael Meheryar Dastoor** (Executives):
Thanks, Steve. I actually feel really good about the 6.1% for the year. I think that's 30 bps up year-on-year. The $8.4 billion of revenue, I think we're growing capacity by about 4 million square feet, and that's quite a big task. Obviously, involves a lot of execution. We've been on that journey for a while. So it's not something we're doing now. I feel really good about the team executing to that $8.4 billion. There might be some upside on that as well if the execution comes in better than expected.
I think the capacity is something we always watch. We have a line of sight to all the capacity that we're adding. We have booked orders. We have customers ready to go. So it comes on through the year, and that's one of the reasons you'll find the revenue through the year is relatively well balanced. I think it's 45% to 55% first half to second half. The margins, though, are a little bit back-end loaded because of the initial ramp that you get when you put out that much capacity. And when I say ramp, it's not just revenue, it's yield, it's additional expenses, it's training. There's a whole bunch of things that go into bringing on capacity online. So feel really good about that. And it's 6.1% number there. We're going to try and outperform that as well.

**Steven Fox** (Analysts):
Great. That's helpful. And just as a follow-up, I'm sure there'll be a lot of other AI questions. I was wondering if you could focus on what could be an emerging market for you in terms of physical AI. You mentioned how you're using it internally and then obviously driving new customer wins. And it sounds like a longer-term benefit, but it's also driving some growth this year. So like how confident are you that these markets develop? And where is Jabil going to play, say, beyond this year and into next year and the year after?

**Michael Meheryar Dastoor** (Executives):
So Steve, I think if you look at physical AI, it's still very, very early commercialization stage. Real-world deployment is negligible, especially in the West. I think China might be ahead of us, but it's a cost issue and a complexity issue still the price points still haven't made it to that full adoption phase. But if you sit back and look at Jabil and what we do, so what are some of the devices and machines that are impacted with physical AI, you have your retail warehouse robots, you have drones, you have autonomous vehicles, you have robotics, humanoids, industrial automation systems, intelligent edge devices. All of that Jabil plays in.
So we're well positioned in all the devices and the peripherals that will come through those devices on physical AI. And then if you think of all the capabilities that we have, you think of sensors, think of onboard compute, connectivity, power, thermal solutions and liquid cooling, every humanoid is going to need liquid cooling there, your motion and actuated related systems. We've been doing that for a while now. So from a capability standpoint, we're really, really well positioned as well. So I can't wait for the adoption. I just -- at this stage, for FY '27, we haven't built in that much from a physical AI perspective. But hey, is this a '28 event? Is it a '29? Only time will tell. One thing you can definitely take away is that Jabil as an early participant and early adopter actually is probably the best positioned in this end market as of today.

**Operator** (Operator):
The next question is coming from Mark Delaney of Goldman Sachs.

**Mark Delaney** (Analysts):
I appreciate all the details in the presentation today. For either Mike or Matt, I'm hoping you can share more on what you're hearing from your conversations with customers and government officials on how potential regulations could impact both data center infrastructure and AI development. And to what extent you've seen any changes in where or when customers are looking to build out that data center capacity?

**Matt Crowley** (Executives):
Yes. Thanks, Mark. Obviously, we spend a lot of time working with the government, understanding where regulation is headed. What I would tell you is, at this point, we don't see any significant impact and/or disruption. I think, obviously, with the midterms ahead, there is potential inflection points depending on how that turns out. But even with that, it feels like there's nothing that is going to create a significant impact to '27 fiscal. And certainly, at this point, we also don't see anything hitting fiscal '28. But it's something we watch closely, and we'll continue to. And so as the midterms evolve, we'll have to see what comes out of that.

**Mark Delaney** (Analysts):
Understood. And my question was a follow-up on the linearity of the year. Mike, I heard the 45-55 weighting comment. I think if you take the 1Q revenue and annualize it, I mean, you're already at about $44 billion. So it does suggest a pretty more flattish year this year than some of the past years. And you did talk about some capacity coming online as the year progresses. So maybe talk about what some of the offsets are that are maybe leading to a more flattish trajectory in the fiscal '27 outlook.

**Michael Meheryar Dastoor** (Executives):
I think you'll see a little bit of a drop in Q2 just from a seasonality. If you go back to all our Q2s in the last 2 or 3 years, that's a seasonal event for us as you come off some of the holiday season spend, as you come off some of the seasonality that's built into our various end markets. I think from an income standpoint, you'll find even the revenue is 45-55, I think income is a little bit more back-end loaded. Like I said, on the ramp and bringing on capacity, the revenues are there. So it's not about revenues as much as it is about getting the yields up. It's about getting the cost through initially, the first 1 or 2 quarters in any ramp, the costs are going to be much higher as a result of which margins can be a little bit lower in the first half.
Having said that, if you look at Q1 of '27, it's actually year-on-year, we're up by 20 bps. So we're doing much better than in previous years. It's just the shape of the year is slightly different this time around because of the heavy ramp in capacity that we're bringing online.

**Mark Delaney** (Analysts):
And just -- I guess just lastly for me and then I'll pass it on, but the ability to get supply from a materials and semiconductor perspective to support that 2H ramp, your visibility into having enough to meet that ramp that you expect?

**Francis McKay** (Executives):
Mark, it's Frank McKay. Yes. So I wouldn't suggest that we're immune from everything that's going on from a constrained market out there, but I definitely feel that Jabil is really, really well positioned just because of -- this has been decades in the building around developing supplier relationships that are strong enough and that we have confidence in them. They're mature and there's a level of trust built in there. So while we'll navigate some bumps in the night through fiscal '27, I'm really confident that we've put a structure in place. We've developed and invested in the right tools. We've got the right team. And I think we've got the right relationship to see us through kind of whatever the world throws at us, but certainly through this constrained market.

**Operator** (Operator):
The next question is coming from Joseph Cardoso of JPMorgan.

**Joseph Cardoso** (Analysts):
Maybe just a follow-up on the seasonality question that you guys have talked to, but maybe in the context of the margin progression as we think of the year, just given the commentary that you made around some of the underutilization costs and the ramps around programs and manufacturing footprint, how should we think about margins stepping up as we kind of progress through the year and the exit run rate, particularly if we compare it to kind of the historical trends that you typically see first half versus second half? And then I do have a follow-up.

**Gregory Hebard** (Executives):
Joe, this is Greg. Yes. So again, as Mike mentioned, the shape of the year will be very similar to last year. Again, we're going to be a little bit lighter on the first half from a margin perspective and then ramping up as we fill capacity and the utilization of that in the back half. So we'll continue to see leverage on our SG&A, better mix as we go in the back half. And the key point is just the capacity we're bringing online, that will be better utilized as we go into the back half.

**Joseph Cardoso** (Analysts):
Got it. And then maybe just wanted to double-click on the networking and communications growth expectations of 15% for fiscal '27 below the other Intelligent Infrastructure end markets and just trying to understand the variance relative to the other markets and maybe broader commentary from OEMs in the space that anecdotally are highlighting very strong demand kind of entering at least calendar '27. So just trying to bridge your expectations maybe versus the interpretation around the underlying markets there? And should we just think about it as largely being correlated to 5G? Or is there other moving pieces there?

**Matt Crowley** (Executives):
Yes. Thanks for the question, Joe. So yes, that's exactly it. On the networking side, we're actually growing roughly 45% to 50%. And so what you're seeing pull-through in the 15% in that reporting line is really effectively some of the downside that we're seeing in the communications space. So we're actually very happy with where the networking business is, and we'll continue to manage through the bouncing around the bottom that comms continues to see. But at the end of the day, 45% to 50% growth in the networking space, we feel like is very much well in line with, if not ahead of the market.

**Operator** (Operator):
The next question is coming from Ruplu Bhattacharya of Bank of America.

**Ruplu Bhattacharya** (Analysts):
Mike, you mentioned asset-light model several times. You've guided for strong growth this year, fiscal '27 and also some comments on fiscal '28. Can you talk about how much total revenue your manufacturing footprint can support today? And where do you see incremental investments? If capital equipment is really going to grow 40% year-on-year and cloud data center 52%, can the model still remain asset-light? Or should investors expect higher CapEx or higher working capital? And would you need to come to the markets to raise funds for that?

**Michael Meheryar Dastoor** (Executives):
So I absolutely and categorically think we still have an asset-light model. Our CapEx requirements are going to be in that 1.5% to 2% range, almost closer to the 1.5% in my view. I'll let Greg answer on the capacity piece. But I think overall, the capitalization, the strong balance sheet that we have, there's no need to get any more funds like some of our competitors. But I feel asset-light model is probably one of the biggest differentiators that Jabil is now providing. I do believe the level of growth we're seeing, the level of returns that we're able to provide, the free cash flow generation that we're able to get is differentiated from some of the others.

**Gregory Hebard** (Executives):
Ruplu, just to add to Mike's comments, it's Greg. Again, we're -- as we mentioned, we're adding 4 million of square footage across the organization. So we feel really good of supporting incremental revenue above our guide. CapEx, absolutely 1.5% to 2%. And when we look at the Intelligent Infrastructure segment, that itself is really closer to 1% of revenue. So we really feel, again, asset-light on that. What I would say is working capital as we go into next year, with $8 billion plus of growth, we do see a dollar increase in just managing net working capital for the year, but we still feel really good about generating free cash flow of $1.6 billion. So again, feel really good of how we're positioned for the year on that.

**Ruplu Bhattacharya** (Analysts):
Okay. Thanks for the details there. Can I ask -- can you give us a little bit more update on the Croatia facility and your opportunity with GLP-1? It seems like that's been delayed a bit. Of the 6% year-on-year growth for the Healthcare segment fiscal '27, is there anything from that? And how is that impacting revenue margins today? And what is the opportunity set there?

**Steven Borges** (Executives):
Yes. Thanks, Ruplu. This is Steve. On Croatia, that remains as planned with the ramp continuing in fiscal year '27. And then as I've stated before, really moving into full production in fiscal year '28. And what I would say there is the bottom line is that, that continues to be on track.
Relating to growth, and I guess, related to GLP-1 question, there is a small element of growth kind of linked to GLP-1. But I'd tell you what has me excited in the healthcare part of the business is the growth is actually across all the subsegments of healthcare. We have new wins in auto-injectors, but that's across biologics, diabetes, insulin, GLP-1s, and that's requiring expansion in our North Carolina site. We have new wins in med devices and patient monitoring and continuous glucose monitoring devices. I'd tell you, we also have new wins in orthopedics as well as diagnostics that relate to advanced testing platforms. So we have a great foundation now to -- with the new wins of this past year and launching those as we move into '27 and beyond for a really good foundational business for that 5% to 7% growth of health care as we go forward.

**Ruplu Bhattacharya** (Analysts):
Got it. I'm going to try and sneak one quick one in, and this is another take on a prior question that's already been asked. But Mike, if I look at the guide for fiscal '27, revenue and EPS, you're guiding $1.6 billion, $0.70 above Street, right? But some investors might say, well, $1 billion and $0.40 of that is already in 1Q. I mean, should we really assume that this is a front-end loaded year? Or is there some conservatism in the guide?

**Michael Meheryar Dastoor** (Executives):
Look, we're always appropriately conservative. There's a whole bunch of geopolitics, inflation, supply chain constraints that we're always cognizant of. So we have estimated where our 6.1% margin for the year falls out. I think if you look at year-over-year, I do expect each of the quarters to outperform the year-on-year quarter comps. Overall, I think is there some upside? Sure, there might be some upside if we have a flawless execution. Like I said, we're bringing on 4 million square feet of capacity. All of that, if that comes together, and there's no major issues in supply chain, we could well have a higher margin profile there as well.

**Operator** (Operator):
The next question is coming from David Vogt of UBS.

**David Vogt** (Analysts):
I appreciate all the detail, very helpful. Maybe, Mike, I just want to pull together a lot of the comments on the call that were made and just maybe get a better sense how you're thinking about the longer-term outlook philosophically because I think Steve mentioned that healthcare is starting to improve this year. Matt talked about not seeing any sort of impact from the geopolitical on the data center side. And you talked about obviously adding 4 million square feet, which helps obviously the ramp in not just in '27, but clearly in '28 and beyond.
So how do we think about sort of the growth algorithm for the company given sort of where the CapEx profile is, where the square footage is and sort of the strength that you're seeing across some of the key markets, particularly across, obviously, within regulated getting better and obviously, data center remaining strong. Because I think you made a reference in the deck to exiting fiscal '27 at a higher Q4 exit run rate. So just trying to get a sense for how do we think about the growth algorithm for Jabil and what that ultimately means for margins given the volume leverage and the economies of scale that you're getting?

**Michael Meheryar Dastoor** (Executives):
So I won't provide FY '28 growth sort of numbers, but I do think you hit all the right spots. If you look at regulated, which was sort of in a recovery mode over the last 2 or 3 years. Actually, I'm really pleased with how regulated is turning out. And the expectation is for each of those end markets in regulated to start growing. I think Matt talked about Intelligent Infrastructure and how demand continues to be through the roof. Demand is way outweighing supply right now. So I think that's a long leg on data center infrastructure. And by the way, the capabilities that we're providing, the holistic approach that the team has taken in providing all these various capabilities is actually resonating with customers. So I think that is going really well.
And then in Rafael's business, if you think of warehouse and retail automation, robots, intelligent devices, all of that is doing well. The only one that I highlighted earlier in my prepared remarks was on the Connected Living side, where one of the things we're trying to do is compete on capability there. It's got to be complex. It's got to be a high level of capability required. We're not competing on low cost. So that might be -- and we factored that into our guide. I think if you look at the Connected Living piece, that's down 15%.
But overall, '27, I think year-on-year, if you look at '26 over '25, I think it was 21%. If you look at '27 over '26, it's 24%. Am I saying '28 will be similar? Maybe. I don't know at this stage. But all the -- everything is in place for us to be able to deliver a good FY '28 as well. I think, like I said, on a CapEx basis, the bulk of the growth is coming and the new capacity that we're adding is coming through the Intelligent Infrastructure space. The regulated and the warehouse automation piece is actually utilizing some of our surplus capacity. So overall, the company is well set for a decent period of growth going forward.

**David Vogt** (Analysts):
Great. Can I just ask a follow-up, Mike? So when you think about the demand signals across Intelligent Infrastructure, what do you need to see to get more aggressive in terms of adding capacity for that particular segment? I would imagine you still have plenty of capacity for healthcare and regulated given what's going on in Croatia. But how long of a lead time and what are the demand signals that you need to see to potentially add more capacity, maybe not in '27, but lining it up for, I guess, fiscal '28 and beyond?

**Matt Crowley** (Executives):
David, thanks for the question. Yes, I would say, one, we did spend a big part of '26, adding capacity in preparation for '27. So we feel really good about that. From an outlook on demand, currently, we feel good about what we see 12 to 24 months out. And certainly, we have felt that way for at least the last 2 quarters. So we really have been preparing for more of an 18-month horizon.
If we start to see some unanticipated demand coming from new customer wins that we don't currently have in the funnel, then it's something we'd look at. But again, if you think about our strategy, which is capability-based, it kind of depends on where the upside would potentially come from. In our data center infrastructure space, we can add capacity with lower power requirements at 2 to 4 megawatts at 1 million square feet relatively quickly inside 3 to 4 months. If the demand is coming from an increase in need for highly complex AI racks that are going to require 20 to 30 megawatts of power towards test infrastructure, then that's a different profile. But at this point, we've brought on the capacity that we think we're going to need, and we feel good about the next 12- to 18-month outlook.

**Operator** (Operator):
The next question is coming from Melissa Fairbanks of Raymond James.

**Melissa Dailey Fairbanks** (Analysts):
I actually had a question for Greg and Frank, and I apologize I've been bouncing around a bunch traveling. So I apologize if this has been addressed. I know, Frank, you gave us some pretty good views into the way that you're managing the supply chain. Mike kind of echoed that as well. We have seen days of inventory come up, and I have been asked about that quite a bit. I'm wondering how much of that is just rising input costs, meaning the inventory is more expensive or that your customers are asking you to preplace that inventory ahead of where their actual demand is?

**Gregory Hebard** (Executives):
Melissa, it's Greg. So let me start that and then hand it off to Frank. So yes, our net inventory days is 64. We're down 4 days from Q3, so progressing well there, but we are above our target range of 55 to 60 days. We have seen -- as our gross inventory has gone up, we have seen an incremental increase in our inventory deposits, which has helped support the market at this time. But there is some higher commodity pricing. We also have a higher weighting of our inventories in the cloud DCI space. And maybe I'll let Frank kind of add from there, any color.

**Francis McKay** (Executives):
Yes. Thanks for the question, Melissa. This is -- it's not -- this isn't kind of rocket science here. I mean this is just a lot of rolling up the sleeves and really hard work to try and keep the inventory as low as we possibly can. I do think we are going to normalize a little bit back to the range that Mike has been chatting about over the last couple of years and that kind of 55, 60-day range as long as we continue to get support from customers on the inventory deposits as well, which I believe we will.
And then just lock in hands with operations and making sure that we have the right tools and people in place to execute. And it's just blocking, tackling, rolling the sleeves up and working closely with each other. I mean it's really that simple. And I think the team is doing a really good job. And I think we're going to be able to continue to execute in a very, very challenging environment.

**Melissa Dailey Fairbanks** (Analysts):
For sure. Frank, I always have to call you and Greg out on every call.

**Francis McKay** (Executives):
Thank you. Appreciate it.

**Melissa Dailey Fairbanks** (Analysts):
Maybe just a follow-up on that. Have there been any issues in terms of moving that inventory into different regions as the demand is kind of shifting to different businesses and maybe within different facilities? Have there been any issues with getting that inventory to the right place?

**Francis McKay** (Executives):
We're really well there, Melissa, in terms of our logistics flow and the way we have that set up, and we're really good at moving programs and inventory from region to region where customers decide maybe their new strategy is going to be a little bit more of a near-shoring position as we continue to navigate through the ever-changing dynamics of legislation change. So I feel really good that wherever those moves are needed, we've got a process and a methodology to go execute really, really well.
So yes, not anything that's keeping me up at night. I think the thing that keeps me up at night is still getting access to supply. And as I mentioned in the prepared remarks and from the question earlier, I think it will be the right combination of relationships with suppliers. I think our customers are doing a really nice job getting in front of this for us and in combination, making sure that we are positioned in Jabil for success when we think about access to our unfair share in, again, what is a very, very constrained marketplace.

**Melissa Dailey Fairbanks** (Analysts):
Great. That's excellent to hear. I have to give Matt a little bit of a break. Appreciate the comments.

**Operator** (Operator):
Thank you. At this time, I'd like to turn the floor back over to Mr. Berry for closing comments.

**Adam Berry** (Executives):
Thank you very much. This concludes our call.

**Operator** (Operator):
Ladies and gentlemen, thank you for your participation. This concludes today's event. You may disconnect your lines or log off the webcast at this time, and enjoy the rest of your day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### JBL_Q3_2026_Earnings_Call_20260617.md
- 2026-06-17｜CFO Gregory Hebard｜guidance：CFO 報告 FY26 Q3 營收約 88 億美元、年增 12%，高於財測中點 2.5 億。（原話："revenue was approximately $8.8 billion, up 12% year-over-year, and $250 million above the midpoint"）
- 2026-06-17｜CFO Gregory Hebard｜margin：Q3 core EPS 3.16 美元、年增 24%（core 營業利益率 5.8%）。（原話："core diluted earnings per share was $3.16, up 24% year-over-year"）
- 2026-06-17｜CFO Gregory Hebard｜guidance：Q4 營收財測 92 億至 100 億美元，中點年增約 16%。（原話："billion to $10 billion or about 16% year-over-year growth at the midpoint."）
- 2026-06-17｜CFO Gregory Hebard｜guidance：Q4 core 營業利益財測區間 5.89 億至 6.49 億美元（中點 core 利益率約 6.4%）。（原話："income to be in the range of $589 million to $649 million"）
- 2026-06-17｜CFO Gregory Hebard｜guidance：Intelligent Infrastructure 部門 Q4 營收財測約 49 億美元、年增約 32%。（原話："approximately $4.9 billion, up about 32% year-over-year"）
- 2026-06-17｜CFO Gregory Hebard｜guidance：FY26 全年財測上調：營收約 350 億、core 利益率約 5.8%、core EPS 約 12.70 美元。（原話："approximately $35 billion, core operating margin of approximately 5.8%, core diluted earnings per"）
- 2026-06-17｜CFO Gregory Hebard｜guidance：FY26 調整後自由現金流財測由 13 億以上上調至 14 億以上。（原話："up from our prior outlook of more than $1.3 billion"）
- 2026-06-17｜CFO Gregory Hebard｜margin：管理層拆解存貨天數：扣除客戶存貨預收後約 68 天，高於目標區間，歸因於出貨時點。（原話："range of 55 to 60 days."）
- 2026-06-17｜CFO Gregory Hebard｜capital_allocation：10 億美元庫藏股授權已於 Q3 買回約 2.91 億，預計 Q4 全數完成。（原話："which we intend to fully complete in Q4"）
- 2026-06-17｜CEO Michael Dastoor｜guidance：FY26 AI 相關營收預期上調至約 136 億美元（3 月為 131 億）。（原話："be approximately $13.6 billion in fiscal 2026."）
- 2026-06-17｜CEO Michael Dastoor｜guidance：CEO 提前給出 FY27 AI 營收成長率的初步看法：百分比與 FY26 相近。（原話："percentage terms to be similar to FY '26"）
- 2026-06-17｜CEO Michael Dastoor｜commitment：CEO 表示有信心 FY27 core 營業利益率超過 6%。（原話："move core operating margin above 6% in fiscal 2027"）
- 2026-06-17｜CEO Michael Dastoor｜margin：回答分析師時強調 6% 後面要加「plus」，同時承認新產能爬坡有影響。（原話："I feel really confident about 6% plus margins"）
- 2026-06-17｜CFO Gregory Hebard｜margin：Q4 為全年利益率最高的季度，去年 Q4 為 6.3%，今年 Q4 財測 6.4%。（原話："Q4 is our highest margin quarter. Last year, we were at 6.3%."）
- 2026-06-17｜CEO Michael Dastoor｜margin：Hanley 收購標的利益率為雙位數，被列為 FY27 利益率改善來源之一。（原話："it's at double-digit margins"）
- 2026-06-17｜CEO Michael Dastoor｜customer：Q3 贏得第三家超大規模客戶。（原話："We also took an important step forward in Q3 by winning our third hyperscale customer."）
- 2026-06-17｜CEO Michael Dastoor｜customer：第三家超大規模客戶 FY27 營收預期約數億美元，FY28 擴至 10 億美元以上。（原話："couple of hundred million dollar range for '27, rapidly expanding to"）
- 2026-06-17｜CEO Michael Dastoor｜competition：回答「憑什麼勝出」：從單一能力切入、再擴展到整座資料中心的打法。（原話："go in through one channel or one capability"）
- 2026-06-17｜CEO Michael Dastoor｜capital_allocation：管理層維持 CapEx 占營收 1.5%–2% 的區間，即使加上新產能。（原話："I still feel comfortable with 1.5% to 2%."）
- 2026-06-17｜CFO Gregory Hebard｜capital_allocation：CFO 表示全球產能將增加約 10%，並相信足以支撐 FY27 AI 營收。（原話："Globally, we're adding an incremental 10% on our footprint."）
- 2026-06-17｜CEO Michael Dastoor｜product：Adani 合作：尚無定案架構，管理層稱 FY28 才是較實際的有意義貢獻起點。（原話："fiscal 2028 is the more realistic starting point for meaningful contributions"）
- 2026-06-17｜CEO Michael Dastoor｜risk：Adani 合作的結構與資本安排尚未確定。（原話："we do not have a definitive framework, so we haven't"）
- 2026-06-17｜CEO Michael Dastoor｜product：資本設備部門：測試設備需求強勁，WFE 出現復甦跡象。（原話："the test equipment demand is through the roof"）
- 2026-06-17｜CEO Michael Dastoor｜product：網通業務 FY27 需求預期與 FY26 相近或更好。（原話："will be similar or better next year to '26"）
- 2026-06-17｜CEO Michael Dastoor｜guidance：Intelligent Infrastructure Q4 財測拆解：Q3 遞延出貨約數億，另加約 3 億增量。（原話："couple of hundred million from Q3 extending into Q4"）
- 2026-06-17｜CEO Michael Dastoor｜risk：供應鏈：DDR4 及以下記憶體預期將有一定程度短缺。（原話："below, I think there will be some level of shortages"）
- 2026-06-17｜CEO Michael Dastoor｜risk：高階 HDI PCB 等零組件交期持續拉長。（原話："Lead times have been extending."）
- 2026-06-17｜CEO Michael Dastoor｜risk：CEO 談零組件短缺對 Intelligent Infrastructure 的影響程度。（原話："I don't lose that much sleep over it"）
- 2026-06-17｜CEO Michael Dastoor｜commitment：北卡羅來納廠時程不變，1 月起滿載，預期年化營收 10 億／20 億／30 億美元（未來 1/2/3 年）。（原話："I would expect run rates to be in that $1 billion,"）
- 2026-06-17｜CEO Michael Dastoor｜capital_allocation：北卡旁邊土地的規劃調整：改看現成可用的廠房，以免再花 12–18 個月興建。（原話："going through another 12, 18 months of build-out"）
- 2026-06-17｜CEO Michael Dastoor｜risk：FY27 Q1 仍處於產能爬坡期。（原話："of '27, we will be in a little bit of a ramp situation."）
- 2026-06-17｜CEO Michael Dastoor｜customer：汽車業 FY26 營收預期上調至約 44 億美元（3 月為 42 億）。（原話："auto revenue of approximately $4.4 billion in fiscal 2026"）
- 2026-06-17｜CEO Michael Dastoor｜risk：汽車業優於預期但管理層仍維持謹慎。（原話："cautious on the automotive market given continued demand volatility"）
- 2026-06-17｜CFO Gregory Hebard｜customer：Connected Living 表現優於財測所嵌入的保守假設。（原話："better than the cautious assumptions we had embedded in the guide."）
- 2026-06-17｜CEO Michael Dastoor｜customer：醫療業 FY26 預期下調 1 億美元，管理層稱不重大。（原話："we took it down by $100 million"）
- 2026-06-17｜CEO Michael Dastoor｜commitment：被問 FY27 總營收成長時，管理層不願延伸 AI 以外的數字，FY27 指引待 9 月提供。（原話："expanding revenue on an incremental basis"）

### 問答異常語氣（迴避／改口／保留）
- JBL_Q3_2026_Earnings_Call_20260617.md｜問：Stifel：Adani 多 GW 建置資本密集，如何與 CapEx 1.5%–2% 並存？是合資還是夥伴出資？｜答法：未回答結構或出資方式，稱尚無定案架構，改談製造能力已被驗證、仍對 1.5%–2% 感到 comfortable。
- JBL_Q3_2026_Earnings_Call_20260617.md｜問：JPMorgan：FY27 AI 持續成長，整體 FY27 營收成長是否至少與 FY26 持平或更高？｜答法：不確認整體營收，表示 AI 數字僅為提示，要求「不要被數字沖昏頭」，FY27 指引留待 9 月。
- JBL_Q3_2026_Earnings_Call_20260617.md｜問：Stifel：Q4 利益率約 6.4%、FY27 僅框為「6% 以上」，如何調和？｜答法：以 Q4 季節性回應，未給出 FY27 利益率的具體走勢，稱談全年形狀還太早。

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

`scenario_inputs`（EPS路徑五年、終端倍數、機率、yield、second_stage、Max DD範圍與依據）——你不寫`scenario.json`，那份由程式跑`dd_scenario.py`產生。Bear機率5Y不應<20%(多數25-30%；極強護城河+短期已兌現才壓15-20%)；Bull/Bear散布5Y應比1Y/2Y寬≥50%；Base機率不應>50%；bear機率須註明依據，sourced結構性durability仍硬套bear需說明「為何不採信」否則不得高於base [§3]。
- 內生天花板sanity check：Base情境EPS CAGR貢獻vs§5.R內生天花板(同組數字不重算)→天花板內✅/超出⚠(⚠→Bear機率強制≥30%)。成長熄火：3年後成長率降至15%/10%/5%三情境×Forward P/E壓縮→估值跌幅，作Bear PE錨。三分量拆解(≤80字，Base IRR多少來自EPS複利/re-rate/股息淨回購)：re-rate貢獻≥Base合計IRR的40%→標記「估值依賴型」(`decision_inputs.valuation_dependent=true`) [§3]。
- IRR落點：<8%/yr弱、8-12%中、>12%強、>15%罕見，不作跨檔排序依據。AR=`(P_bull×|Bull5Y%|)÷(P_bear×|Bear5Y%|)`，<2平庸/2-4偏正/≥4顯著，非放鬆機率防線理由。年期硬規則：①表頭終端年=主時距終端年②終端倍數EPS分母年期與現價倍數同源③終端倍數必附≥1個同業現值comp對照 [§3]。10Y二段延伸(`runway_post_y5`=🟢且終端倍數承重，或Base IRR實質來自Y5後)：Y5→Y10 EPS CAGR/10Y累積倍數/IRR。R:R數學假象：下行>15%正常使用；5-15%警示「已接近定價」；<5%失效標「數學假象」禁引用進場判定，改極端Bear(Bear PE×0.8+Bear EPS×0.85)重算(Bear EPS=FY+1 EPS×0.9；Bear PE=成長熄火「降至10%」情境) [§3]。

**Max DD**(`premortem.max_dd`)：填範圍`lo`/`hi`(禁單點，寬度≥10pp)+`path_risk`(🟢0～−30%/🟡−30～−50%/🔴<−50%)；推導依據須寫`reasoning.premortem`。硬接線：🔴且thesis脆弱(`moat.trend`↓或`runway_post_y5`🔴或估值依賴型)→倉位上限下修(6%→≤3%)；🔴但thesis完整→不因波動砍倉，註記「深回撤心理準備」[§2問六]。

**必答項**：`scenario_inputs`三支EPS路徑、終端倍數、Bear/Base/Bull機率、`premortem.max_dd.lo/hi`、`path_risk`。

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

## ⑥ 條件附卡（archetype_hint='EMS/ODM' 命中）：judge_addendum_cyclical.md

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
{"date":"20260703","verdict":"觀望","role":"條件式衛星持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Intelligent Infrastructure（AI/DCI）段持續高成長，把 blended 毛利/營業利益率結構性上移","columns":{"2Y／5Y／10Y 時間軸":"2Y：AI 營收 +40%/yr；5Y：II 段成 &gt;60% 營收；10Y：JBL 成 AI 基建代工結構性玩家","sourced floor（驗證門檻 + 來源）":"Q3 FY26：II 段 $4.2B（+21% YoY）、AI 營收 FY26 $13.6B（+50%、佔 39%）、core OM guide 5.8%→FY27 &gt;6%（Investing.com / Seeking Alpha 2026-06）","漂移觸發（削弱／反轉）":"削弱：AI 營收成長連 2 季 &lt; +25%；反轉：II 段連 2 季 YoY &lt; +10% 或 core OM 連 4 季不升"}},{"id":"H2","text":"hyperscaler AI 資本開支續強，JBL 的量增引擎不熄火","columns":{"2Y／5Y／10Y 時間軸":"2Y：四大 capex +20%+/yr；5Y：AI 基建 buildout 未見頂；10Y：AI 算力需求結構化","sourced floor（驗證門檻 + 來源）":"2026 四大 capex 產業級 +30%+；JBL 第三家 hyperscaler 進單（FY27 貢獻「數億」、FY28 &gt;$1B，Q3 call 2026-06）","漂移觸發（削弱／反轉）":"削弱：2027 四大 capex 指引 YoY &lt; +15%；反轉：hyperscaler 公開暫停/削減資料中心（如 MSFT 2026 H1 曾取消 ~2GW 的產業訊號蔓延）"}},{"id":"H3","text":"倍數維持在「credit AI mix」的高位（不回歸 EMS 歷史常態）","columns":{"2Y／5Y／10Y 時間軸":"2Y：NTM PE 維持 ~18-23x；5Y：不跌破 14x（歷史中位）","sourced floor（驗證門檻 + 來源）":"現 TTM PE ~46x（5Y 中位 14x、低 8.8x）、EV/EBITDA 15.7-16x 貼 13 年高（GuruFocus 2026-02）；NTM ~20-23x 近 10 年高（Simply Wall St）","漂移觸發（削弱／反轉）":"削弱：NTM PE 跌破 16x；反轉：跌破 14x（回歸 EMS 常態，re-rate 論點作廢）→ 這是 Bear 主路徑"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":5.2,"ev5y_pct":28.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"條件式衛星持倉","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.7,"ev5y_pct":28.0,"irr_base_pct":5.2,"max_dd_pct":-50.0,"bull_5y_price":640.0,"bear_5y_price":230.0,"p_bull_pct":30.0,"p_bear_pct":30.0,"rearm_trigger":null,"price_at_dd":341.3,"archetype":null,"cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名的每一個**（含程式稍後才會算的 asym_ratio／bull_5y_price／bear_5y_price／p_bull_pct／p_bear_pct／ev5y_pct／irr_base_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JBL_20261012/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
