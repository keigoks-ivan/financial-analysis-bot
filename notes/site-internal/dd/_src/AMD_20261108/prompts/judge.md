你是 stock-analyst **v20 判斷 agent**，標的 AMD（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"AMD","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMD_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMD_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":11536,"period":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","citation":"公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results, https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results"},"note":"Street 共識約 $11.31B，實際 $11.536B（beat）（來源：web_search 彙整多家財經媒體引述 LSEG/Wall St. 共識，非公司原始揭露）"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":27,"period":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","citation":"公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results"},"note":"未查得明確 Street 共識營業利益率數字；EPS 端可比對：non-GAAP EPS $1.66 vs 共識 $1.62（beat，來源：web_search 多家財經媒體）"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":17,"period":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","citation":"公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results"},"note":"N/A（Street 通常僅追蹤 non-GAAP 口徑，未查得 GAAP 營業利益率共識）"},{"id":"f_kpi5_q3_fy2026_guidance","label":"管理層 Q3 FY2026 財測 guidance","value":"營收約 $13.0B ± $300M；non-GAAP 毛利率約 56%","period":"發布於 2026-08-04，指引對象為 Q3 FY2026","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"發布於 2026-08-04，指引對象為 Q3 FY2026","citation":"公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results"},"note":"公司指引中值 $13.0B 高於彼時 LSEG 共識 $12.52B（來源：web_search 財經媒體引述）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-03","period":"2026-11-03","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-03"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_amd_gross_margin_pct","label":"AMD 毛利率","value":53.72,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amd_operating_margin_pct","label":"AMD 營業利益率","value":17.72,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amd_fcf_margin_pct","label":"AMD FCF 利潤率","value":15.53,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nvda_gross_margin_pct","label":"NVDA 毛利率","value":74.67,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_operating_margin_pct","label":"NVDA 營業利益率","value":65.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_fcf_margin_pct","label":"NVDA FCF 利潤率","value":41.92,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_gross_margin_pct","label":"MRVL 毛利率","value":52.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_operating_margin_pct","label":"MRVL 營業利益率","value":16.81,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_fcf_margin_pct","label":"MRVL FCF 利潤率","value":18.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_3661_tw_gross_margin_pct","label":"3661.TW 毛利率","value":37.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3661_tw_operating_margin_pct","label":"3661.TW 營業利益率","value":24.0,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3661_tw_fcf_margin_pct","label":"3661.TW FCF 利潤率","value":-10.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":1558,"period":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","citation":"公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results"},"note":"未查得 Street FCF 共識數字"},{"id":"f_kpi4_sbc","label":"SBC 占營收 %","value":4.36,"period":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","citation":"公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results"},"note":"N/A（無此項共識追蹤）"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":449.04,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-1.35,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":38.41,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.12,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.06 → 8.07）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":3.13,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.27 → 16.78）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":4.71,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.56 → 24.67）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":8.07,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":16.78,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":24.67,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":6.75,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 7.56 → 8.07（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":95.95,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝10.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":10.7,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":16.21,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":16.06,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":55.64,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 8.07，分子＝快照價 449.04","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-6565.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 9211.0、現金 15776.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1640.09,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":729899.8,"period":"2026-11-08","unit":"USD m","basis":"市值 736464.8 ＋ 淨負債 -6565.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":52235.53,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（43 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":95706.77,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（49 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":13.97,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"✅","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 449.04 / W52 376.27 / W104 257.5 / W250 175.04 / W250 13週斜率 3.47%"},{"id":"f_ma_w52","label":"52 週均線","value":376.27,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":257.5,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":175.04,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":3.47,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMD reached a record 34.1% x86 CPU market share in Q2 2026 (Mercury Research data), up 4.7 percentage points YoY, with Intel losing share across every major client/server segment.","source":"digitalcitizen.life, \"AMD Reaches Record 34.1 Percent x86 CPU Share as Intel Loses Ground Across Every Major Segment\"","url":null,"excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMD's desktop x86 CPU unit share climbed to 34.9% in Q2 2026, up 1.8 percentage points quarter-over-quarter.","source":"The Register, \"AMD grabs more CPU share while pricier PCs punish desktop demand\"","url":null,"excerpt":null,"as_of":"2026-08-21","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMD's server CPU revenue share hit a record 46.2% in Q1 2026 while shipping roughly one-third of x86 server units; Intel still shipped ~66.8% of units but its revenue share fell to ~53.8%, reflecting AMD's higher-ASP premium EPYC configs.","source":"wccftech, \"AMD's EPYC Steamrolls the Server Market With Record 46.2% Revenue Share\"; TechPowerUp, \"Intel's Server Share Slips to 67%\"","url":null,"excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMD's EPYC CPUs were reported sold out in 2026, with delivery lead times stretching more than 30 weeks due to hyperscaler demand.","source":"io-fund, \"AMD, Nvidia, Arm, Intel: Inside the $120 Billion CPU Gold Rush\"","url":null,"excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","triggers"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"In AI accelerators, AMD's share has grown from under 1% to an estimated 5-7% (~$7-8B Instinct revenue), but Nvidia still holds roughly 80% of AI accelerator revenue share, meaning the absolute gap is widening even as AMD's relative share grows.","source":"siliconanalysts.com, \"AMD vs NVIDIA AI GPU Market Share 2026: MI350X vs B200 Competitive Analysis\"","url":null,"excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Custom ASIC silicon from hyperscalers (Broadcom AI ASIC revenue $20B+ in FY2025, Google TPU, AWS Trainium) is characterized as a larger and faster-growing competitive threat to Nvidia's AI accelerator dominance than AMD is, positioning custom silicon rather than AMD as the more significant new-entrant pressure in AI accelerators.","source":"SemiAnalysis, \"Can AMD break the CUDA Moat? AMD Advancing AI 2026\" (cited via siliconanalysts.com search summary)","url":null,"excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#6","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMD Instinct MI300X/MI350 accelerators have secured adoption from Microsoft Azure, Meta, Dell Technologies, HPE and Lenovo, including use by Microsoft Azure for Azure OpenAI services; MI350 began shipping to partners and hyperscale data centers in Q3 2025.","source":"AMD FY2025 Annual Report to Shareholders (Form ARS), SEC EDGAR filing","url":null,"excerpt":null,"as_of":"2025-12-27","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#7","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMD confirmed the Instinct MI400 series for 2026 with 432GB HBM4 memory, doubling MI355's throughput (40 PFLOPS FP4 / 20 PFLOPS FP8 vs 20/10), as part of AMD's plan to release a new data center GPU every year.","source":"VideoCardz, \"AMD launches Instinct MI350 series, confirms MI400 in 2026 with 432GB HBM4 memory\"","url":null,"excerpt":null,"as_of":"2025-06-12","retrieved_at":"20261108","affects":["moat_trend","thesis.H","triggers"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Meta（AMD 6GW Instinct GPU 合約的客戶）在簽下輝達與 AMD 大單數週後，宣布擴大自研 AI 晶片 MTIA（in-house）部署","source":"CNBC, \"Meta rolls out in-house AI chips weeks after massive Nvidia, AMD deals\", https://www.cnbc.com/2026/03/11/meta-ai-mtia-chip-data-center.html","url":null,"excerpt":null,"as_of":"2026-03-11","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Broadcom 被證實是 Google TPU、Meta MTIA、Microsoft Maia，以及 2026 年初起 OpenAI／Anthropic Titan 自研 AI 晶片專案的設計夥伴——顯示 AMD 多個大型 AI 客戶同時在推進自製晶片路線","source":"Tom's Hardware, \"The custom AI ASIC state of play (May 2026)\", https://www.tomshardware.com/tech-industry/semiconductors/custom-ai-asics-examined-from-broadcom-to-mtia","url":null,"excerpt":null,"as_of":"2026-05","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Microsoft 自研 AI 晶片 Maia 200 於 2026 年 1 月開始部署（台積電 3nm 製程），號稱比現有機隊每美元效能高 30%——微軟同時也是 AMD Instinct 的客戶之一","source":"Windows News, \"AI Compute Crunch: How Meta and Microsoft's Chip Deals Shape the 2026 Race\", https://windowsnews.ai/article/ai-compute-crunch-how-meta-and-microsofts-chip-deals-shape-the-2026-race.411832","url":null,"excerpt":null,"as_of":"2026-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"AMD 10-K (FY2025, filed 2026-02-04) discloses no single customer accounted for 10% or more of consolidated net revenue in fiscal 2025 or fiscal 2024, an improvement from FY2023 when one customer accounted for 18% of consolidated net revenue.","source":"AMD Form 10-K for fiscal year ended 2025-12-27, SEC EDGAR (amd-20251227.htm)","url":null,"excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear","triggers"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"AMD's forward customer base is concentrating around a small number of AI hyperscalers: AMD and Meta signed a 5-year, up-to-$60B, 6GW Instinct GPU supply agreement (with AMD issuing Meta a performance-based warrant for 160M shares), and combined with the OpenAI 6GW agreement AMD has ~12GW of committed deployments; these agreements are multi-year and milestone-based, meaning most of the associated revenue is not yet contracted, shipped, or paid.","source":"CNBC / Tom's Hardware / AMD IR press release on AMD-Meta strategic partnership","url":null,"excerpt":null,"as_of":"2026-02-24","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"OpenAI, a counterparty to AMD's Instinct GPU supply agreement, reported a Q1 2026 net loss of $21.3B, carries roughly $665B in long-term compute purchase commitments not reflected as balance-sheet debt, and faces a projected financing gap of about $130B over the next two years.","source":"TradingKey / IFR (International Financing Review) reporting on OpenAI Q1 2026 financials","url":null,"excerpt":null,"as_of":"2026-05","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Despite tripling its debt load in a single month (including $26B in debt financing from Blue Owl/PIMCO for a Louisiana AI data center), Moody's (2026-07-24) said Meta still retains one of the strongest corporate balance sheets and its investment-grade rating is not under imminent threat, even as Moody's flagged 'unprecedented' AI spending as a broader credit-quality risk across hyperscalers.","source":"CNBC, citing Moody's commentary","url":null,"excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#4","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"S&P Global downgraded Oracle's credit rating from BBB to BBB- (one notch above junk), explicitly naming OpenAI as a 'key credit risk' for Oracle due to Oracle's large compute-supply exposure to OpenAI — illustrating rating-agency concern about OpenAI's counterparty credit quality that is also relevant to AMD's own OpenAI compute agreement.","source":"the-decoder.com / TradingKey reporting on S&P Global Oracle downgrade","url":null,"excerpt":null,"as_of":"2026","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"記憶體晶片（DRAM/NAND，含 HBM 上游）短缺預期持續到 2027 年，SK海力士高層警告短缺可能延續到 2030 年之後，因 AI 資料中心需求排擠傳統記憶體供給","source":"CNBC, \"Memory chip shortage to last through 2027, semiconductor boss says\", https://www.cnbc.com/2026/01/26/memory-chip-shortage-synopsys-lenovo-ai-data-centers.html","url":null,"excerpt":null,"as_of":"2026-01-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Gartner 預測 2026 年全球半導體營收將突破 1.3 兆美元，反映 AI 相關晶片需求持續強勁","source":"Gartner 新聞稿，\"Gartner Forecasts Worldwide Semiconductor Revenue to Exceed $1.3 Trillion in 2026\", https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026","url":null,"excerpt":null,"as_of":"2026-04-08","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"NVIDIA 執行長黃仁勳在 GTC 大會上將公司 AI 晶片訂單預測倍增至 1 兆美元、預計 2027 年達成，理由是產業正進入由推論（inference）工作負載主導的新階段","source":"MLQ News, \"NVIDIA Doubles Its AI Chip Order Forecast to $1 Trillion by 2027, Citing Inference Demand Surge\", https://mlq.ai/news/nvidia-doubles-its-ai-chip-order-forecast-to-1-trillion-by-2027-citing-inference-demand-surge/","url":null,"excerpt":null,"as_of":"2026-03-17","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"AMD 在 AI 加速器市場的營收份額約 5-7%（NVIDIA 約 80%），但 AMD Instinct GPU 系列 2025 會計年度營收估計 $6-8B，較 2024 年最初約 $2B 的原始指引歷經四次上修至『超過 $5B』的實際成果","source":"Silicon Analysts, \"AMD vs NVIDIA AI GPU Market Share 2026: MI350X vs B200 Competitive Analysis\", https://siliconanalysts.com/analysis/amd-vs-nvidia-ai-gpu-market-share-2026","url":null,"excerpt":null,"as_of":"2026-04-13","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"美國商務部工業與安全局(BIS)於2026年1月13日發布最終規則、1月15日生效，將輝達H200與AMD MI325X等同等級先進AI晶片對中國(含澳門)出口的審查標準，從『推定拒絕』改為『逐案審查』；出口商須證明輸往中國/澳門的總處理效能(TPP)低於輸美客戶總量的50%。","source":"Mayer Brown, 'Administration Policies on Advanced AI Chips Codified' (引述BIS最終規則) https://www.mayerbrown.com/en/insights/publications/2026/01/administration-policies-on-advanced-ai-chips-codified","url":null,"excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"美國總統於2026年1月14日簽署行政公告，對輸往中國、非用於美國供應鏈之先進AI晶片(含AMD MI325X等級產品)課徵25%從價關稅，作為前述放行規則的配套限制。","source":"Mayer Brown, 'Administration Policies on Advanced AI Chips Codified' https://www.mayerbrown.com/en/insights/publications/2026/01/administration-policies-on-advanced-ai-chips-codified","url":null,"excerpt":null,"as_of":"2026-01-14","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"President Trump's Proclamation 11002 imposed a 25% Section 232 tariff on advanced semiconductors and derivative products effective January 15, 2026; AMD's Instinct MI325X is specifically named in the annex. Exemptions apply to products supporting US data centers, R&D, startups, repairs, and non-data-center consumer/industrial uses.","source":"President Trump Announces Section 232 Tariffs on Semiconductors and their Derivative Products, International Trade & Supply Chain Insights (internationaltradeinsights.com/2026/01/president-trump-announces-section-232-tariffs-on-semiconductors-and-their-derivative-products/)","url":null,"excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"BIS published a final rule on January 15, 2026 shifting export license review policy for NVIDIA H200 and AMD MI325X exports to China/Macau from 'presumption of denial' to 'case-by-case review', subject to a 25% tariff on those exports, a 50% volume cap, third-party testing, and KYC requirements.","source":"Revision to License Review Policy for Advanced Computing Commodities, Federal Register (federalregister.gov/documents/2026/01/15/2026-00789); BIS press release (bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china)","url":null,"excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"AMD CEO Lisa Su stated China represents roughly 20% of AMD's total revenue, and characterized China as a 'very important market' despite ongoing US export restrictions on advanced AI GPUs.","source":"AMD CEO Lisa Su says China still accounts for about 20% of revenue despite GPU export controls, cryptobriefing.com (cryptobriefing.com/amd-china-revenue-export-restrictions/)","url":null,"excerpt":null,"as_of":"2026-05-22","retrieved_at":"20261108","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"AMD planned to ship an additional $100 million of MI308 chips to China in the quarter ending March 2026, but was not counting on further China AI-chip revenue beyond that due to market/regulatory uncertainty.","source":"AMD 1Q Sales to Slip Despite $100M MI308 China Boost, Next-Gen AI Chips Set for 2H Ramp, TrendForce (trendforce.com/news/2026/02/04/news-amd-1q-sales-to-slip-despite-100m-mi308-china-boost-next-gen-ai-chips-set-for-2h-ramp/)","url":null,"excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"TSMC controls roughly 90% of the world's most advanced-node chip production (3nm/5nm) and is AMD's main foundry for leading-edge chiplet processors; this production is concentrated in Taiwan, ~100 miles from mainland China.","source":"Mapshock, \"TSMC Taiwan Geopolitical Risk: Concentration and Resilience Planning\" (mapshock.com); FourWeekMBA, \"AMD and TSMC: What a Reported Foundry Cost Rise Reveals About the Fabless Supply Layer\"","url":null,"excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"On 2026-01-14, the US administration signed a proclamation imposing a 25% duty/revenue-share on advanced computing chips (e.g. H200, MI325X) shipped to China, with mandatory third-party testing and a volume cap; AMD CEO Lisa Su stated China still accounts for about 20% of AMD's revenue despite export controls.","source":"Introl Blog, \"BIS Export Policy Shift\" (introl.com/blog/bis-export-policy-h200-mi325x-china-case-by-case-2026); Cryptobriefing, \"AMD CEO Lisa Su says China still accounts for about 20% of revenue despite GPU export controls\"","url":null,"excerpt":null,"as_of":"2026-01-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"AMD had previously forecast about $1.5 billion in 2025 revenue loss and taken an $800 million charge tied to halted AI-chip shipments to China (inventory write-downs, cancelled purchases) due to tightened US export restrictions.","source":"Astute Group, \"AMD Flags $1.5 Billion Revenue Blow from Tightened Export Curbs\"; Motley Fool, \"AMD Stock Declines as Earnings Drop 30% on Government Restricting Advanced AI Chip Sales to China\"","url":null,"excerpt":null,"as_of":"2025-08-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"TSMC's second Arizona fab (Fab 21 Phase 2, 3nm) is reportedly targeting 2H27 mass production, with all four announced US fabs said to be fully booked; AMD is among the AI chip designers allocated capacity at TSMC's advanced nodes including its overseas (non-Taiwan) fabs, offering AMD partial future geographic diversification, though no advanced-node output outside Taiwan is yet in volume production for AMD's chiplets.","source":"TrendForce, \"TSMC Reportedly Eyes 2H27 3nm Mass Production at Arizona Fab 2; Four U.S. Fabs Said to Be Fully Booked\" (trendforce.com/news/2026/03/24)","url":null,"excerpt":null,"as_of":"2026-03-24","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Data Center segment revenue $6.7B in Q2 2026, up 107% YoY, driven by EPYC CPU and Instinct GPU sales","source":"AMD Q2 2026 press release (ir.amd.com); CNBC https://www.cnbc.com/2026/08/04/amd-earnings-report-q2-2026.html","url":null,"excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"AMD guided Q3 2026 data center + embedded revenue to grow double-digit sequentially, and server CPU revenue to grow >80% YoY in H2 2026","source":"AMD Q2 2026 earnings slides via Investing.com https://www.investing.com/news/company-news/amd-q2-2026-slides-data-center-revenue-doubles-ai-partnerships-expand-93CH-4836256","url":null,"excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["thesis.H","triggers"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"AMD stated data center segment revenue should more than double in 2027, supported by ramp of Helios (MI400-series) platform","source":"AMD Q2 2026 earnings call/slides via Investing.com https://www.investing.com/news/company-news/amd-q2-2026-slides-data-center-revenue-doubles-ai-partnerships-expand-93CH-4836256","url":null,"excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"AMD data center revenue reached $5.8B in Q1 2026; company reiterated a long-term target of $120B server CPU-related revenue by 2030","source":"DataCenterDynamics https://www.datacenterdynamics.com/en/news/amd-posts-q1-2026-data-center-revenue-of-58bn-forecasts-120bn-server-cpu-income-by-2030/","url":null,"excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"AMD reached record 46.2% server x86 CPU revenue share in Q1 2026 (unit share ~30% of entire x86 CPU market)","source":"Wccftech https://wccftech.com/amd-posts-record-server-cpu-revenue-in-q1-2026-red-team-commands-30-percent-market/; Tom's Hardware https://www.tomshardware.com/pc-components/cpus/amd-reaches-46-percent-of-server-x86-cpu-revenue-intel-still-controls-70-percent-of-the-consumer-pc-market-share","url":null,"excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"NVIDIA holds an estimated 70-75% of data-center AI accelerator market revenue vs. AMD's estimated 6-8%; hyperscaler custom silicon collectively ~15-20%","source":"Silicon Analysts https://siliconanalysts.com/analysis/nvidia-ai-accelerator-market-share-2024-2026","url":null,"excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"AMD Instinct GPU line generated an estimated $7-8B in 2025 (~5-7% of AI accelerator revenue); MI400 series (CDNA5, 2nm, 432GB HBM4) launched July 2026 as first-to-market 2nm AI accelerator","source":"Silicon Analysts https://siliconanalysts.com/analysis/amd-vs-nvidia-ai-gpu-market-share-2026","url":null,"excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"+","claim":"Third-party analyst scenario projects AMD AI accelerator share could reach 15-20% by 2027 (vs. NVIDIA 75-80%), citing OpenAI 6GW compute commitment and Meta multi-year deals as catalysts; this is a market-analyst projection, not AMD guidance","source":"Silicon Analysts https://siliconanalysts.com/analysis/amd-vs-nvidia-ai-gpu-market-share-2026","url":null,"excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#8","axis":"end_markets","section":"coverage","direction":"+","claim":"AI data center GPU market projected to grow from $11.12B (2025) to $32.3B by 2030, a 23.8% CAGR","source":"GlobeNewswire market report https://www.globenewswire.com/news-release/2026/04/14/3273676/0/en/AI-Data-Center-Graphics-Processing-Units-GPUs-Market-Report-2026-32-3-Bn-Opportunities-Trends-Competitive-Landscape-Strategies-and-Forecasts-2020-2025-2025-2030F-2035F.html","url":null,"excerpt":null,"as_of":"2026-04-14","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#9","axis":"end_markets","section":"coverage","direction":"+","claim":"Client segment (PC CPU) unit market share reached 30.3% in Q2 2026 (first time above 30%), up from 29.6% in Q1 2026 and 24.1% a year earlier; Intel share fell to 69.7%","source":"XenoSpectrum https://xenospectrum.com/en/amd-x86-client-share-q2-2026/; pbxscience https://pbxscience.com/amds-x86-client-processor-share-tops-30-for-the-first-time-as-intels-lead-keeps-shrinking/","url":null,"excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#10","axis":"end_markets","section":"coverage","direction":"+","claim":"Client segment revenue was $3.1B in Q2 2026, up 23% YoY (from $2.5B); Q1 2026 client revenue was $2.9B, up 26% YoY, driven by Ryzen demand and share gains","source":"AMD Q1/Q2 2026 press releases (ir.amd.com)","url":null,"excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#11","axis":"end_markets","section":"coverage","direction":"-","claim":"Gaming segment revenue was $779M in Q2 2026, down 31% YoY, primarily due to lower semi-custom (console) revenue and higher component costs weighing on GPU demand at this late stage of the console cycle; AMD guided H2 2026 gaming revenue to be >20% lower than H1 2026","source":"Tom's Hardware https://www.tomshardware.com/tech-industry/amd-doubles-data-center-revenue-year-over-year-but-gaming-revenue-plunged-by-31-percent-ceo-lisa-su-says-prices-have-weighed-on-consumer-demand-but-is-optimistic-about-client-market","url":null,"excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#12","axis":"end_markets","section":"coverage","direction":"0","claim":"Gaming revenue was $720M in Q1 2026, up 11% YoY on higher Radeon GPU demand, partially offset by lower semi-custom revenue; customer demand for next-gen console platforms described as encouraging even as current-gen console sales decline late in the cycle","source":"TweakTown https://www.tweaktown.com/news/111459/amd-gaming-revenue-increased-in-q1-2026-thanks-to-solid-demand-for-radeon-gpus/index.html","url":null,"excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#13","axis":"end_markets","section":"coverage","direction":"+","claim":"Embedded segment revenue was $977M in Q2 2026, up 19% YoY (strongest embedded growth in 3+ years), with operating margin at 40% (up from 33% a year earlier); segment tracking toward a record year with over $18B in new design wins, following a prolonged industrial inventory correction","source":"AMD Q2 2026 press release (ir.amd.com)","url":null,"excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#14","axis":"end_markets","section":"coverage","direction":"+","claim":"Embedded segment revenue was $873M in Q1 2026, up 6% YoY, as industrial and edge demand began improving","source":"AMD Q1 2026 press release https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results","url":null,"excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"AMD 2026 SWOT 分析指出，AMD 部分大客戶正自行開發內部處理器與加速器（客製化晶片/ASIC），可能壓縮 AMD 的可觸及市場（addressable market）。","source":"AMD SWOT Analysis 2026 - The Strategy Story (https://thestrategystory.com/blog/amd-swot-analysis-2026/)","url":null,"excerpt":null,"as_of":"2026-09-21","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"AMD 於 2026-08-10 收購 AI 加速新創 Taalas（由 Tenstorrent 共同創辦人 Ljubisa Bajic 創立）。Taalas 技術將模型「硬編碼」進晶片（predefined logic tiles + mask-programmed ROM），宣稱推論階段 token 速率達最接近競品的 8 倍、耗電更低，屬於犧牲彈性換取速度的專用硬體路線，被視為對通用型 GPU（如 AMD 自家 MI455X）的替代/互補技術，AMD 藉收購提前佈局以防被此類專用晶片路線邊緣化。","source":"xpu.pub, \"Taalas Technology to Boost AMD AI Performance and Efficiency\" (https://xpu.pub/2026/08/10/amd-taalas-ai-acceleration/)","url":null,"excerpt":null,"as_of":"2026-08-10","retrieved_at":"20261108","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"AMD 10-K FY2025 稱其日益聚焦 VAR 通路（轉售 OEM 系統給中型與 SMB 市場）及全球系統整合商；銷售仍經直銷、OEM、獨立經銷商。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm","excerpt":"Large multi-nationals and regional accounts are the core of our OEM partners’ business; however, we are increasingly focused on the VAR channel, which resells OEM systems to the mid-market and the small and medium business (SMB) segments.","as_of":"2026-02-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"搜尋摘要稱 AMD 由單賣 GPU/CPU 轉向整機櫃（rack-scale）系統，Lisa Su 預期 2026 年 MI450 絕大多數以整機櫃方案銷售。","source":"letsdatascience 等聚合站報導（AMD Shifts To Rack-Scale Systems Strategy）","url":"https://letsdatascience.com/news/amd-shifts-to-rack-scale-systems-strategy-e34c4b3a","excerpt":"In 2026 it expects the \"vast majority\" of its MI450 series GPUs to be sold as \"rack scale solutions\"","as_of":"2026-02-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026 營收 guidance 約 $13B（±$300M）、毛利率約 56%，與市場共識（營收 $13,058M、毛利率 56.1%）幾乎一致，無明顯落差","source":"Hudson Labs, AMD Q3 2026 Earnings Preview","url":"https://www.hudson-labs.com/research/amd-q3-2026-earnings-preview-revenue-guidance-key-drivers","excerpt":"consensus of $13,058M revenue and 56.1% margin","as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價共識約 $508（MarketBeat，48 位分析師，區間 $320–$700，Moderate Buy），as-of 2026-07-29；另 MarketScreener 平均 $500.40（51 位）","source":"MarketBeat via search summary (2026-07-29); MarketScreener","url":"https://www.marketbeat.com/instant-alerts/advanced-micro-devices-inc-nasdaqamd-given-consensus-recommendation-of-moderate-buy-by-analysts-2026-04-07/","excerpt":"MarketScreener reported an average 12-month target price of $500.40 for AMD, based on 51 analyst estimates","as_of":"2026-07-29","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"高端目標價：Barclays $665（2026-06-01）、Wells Fargo 由 $505 升至 $615（2026-06-30）；TIKR 指出股價當時已超過共識均值 $508。現價請引 numbers.price_at_dd","source":"search summary of capital.com / TIKR","url":"https://www.tikr.com/blog/amd-stock-has-doubled-in-2026-can-the-120-billion-cpu-tam-revision-justify-a-target-above-2000","excerpt":"Wells Fargo raised its target to $615 from $505 on June 30, citing server CPU demand.","as_of":"2026-06-30","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-05 Q1 財報時 AMD 將 Q2 營收 guidance 上調至約 $11.2B±$300M；Benzinga 記錄 2022-11 至 2026-08 間 11 次上調、4 次下調","source":"Benzinga AMD guidance page / MarketBeat Q1 call highlights","url":"https://www.benzinga.com/quote/AMD/guidance","excerpt":"Advanced Micro Devices (AMD) raised its revenue guidance from a prior range of $9.50B - $10.10B to $10.90B - $11.50B for Q2 2026.","as_of":"2026-05-05","retrieved_at":"20261108","affects":["thesis.H","triggers"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"賣方 FY2026 EPS 預估持續上修：Erste 於 5 月自 $5.74 升至 $6.29、6 月升至 $6.35；Northland 則下修 Q2 EPS 至 $1.22（維持 Market Perform、目標價 $260，為低端離群）","source":"MarketBeat (Erste Group estimate, 2026-06-11); Northland estimate (2026-05-12)","url":"https://www.marketbeat.com/instant-alerts/what-is-erste-group-banks-estimate-for-amd-fy2026-earnings-2026-06-11/","excerpt":"Erste Group raised its FY2026 EPS estimate to $6.29 from $5.74 in May, then to $6.35 from $6.29 in June","as_of":"2026-06-11","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill 顯示最新 FY EPS 預估 7.72 USD（59 位分析師，2026-10-17），下一季營收預估 3 個月內上修 5.67%（單一聚合站，未交叉驗證）","source":"Chartmill AMD estimates","url":"https://www.chartmill.com/stock/quote/AMD/estimates","excerpt":"latest recorded estimate: 7.72 USD · Oct 17, 2026 · 59 analysts","as_of":"2026-10-17","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-02-23 AMD 向 Meta 發行績效型認股權證，最多 160 million 股、行使價 $0.01，連動 Meta 購買首批 1GW 的 Instinct GPU 的具約束力承諾。","source":"SEC EDGAR 8-K（Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/2488/000000248826000045/amd-20260223.htm","excerpt":"On February 23, 2026, in connection with a strategic arrangement between Advanced Micro Devices, Inc. (“AMD”) and Meta Platforms, Inc. (“Meta\") governing the purchase of AMD Instinct™ GPU products by Meta, AMD issued to Meta a performance-based warrant (the “Warrant”) to purchase up to an aggregate of 160 million shares of common stock of AMD (the “Warrant Shares”) at an exercise price of $0.01 per share.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-08-17 AMD 完成 47.5 億美元高級債券發行（2029/2031/2033/2036 四檔）。","source":"SEC EDGAR 8-K（Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/2488/000119312526354029/d142696d8k.htm","excerpt":"On August 17, 2026 (the “Closing Date”), Advanced Micro Devices, Inc. (the “Company”) closed its public offering (the “Offering”) of $4.75 billion aggregate principal amount of senior notes","as_of":"2026-08-17","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-05-14 AMD 簽訂 50 億美元五年期無擔保循環信貸，取代 2022 年舊協議。","source":"SEC EDGAR 8-K（Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/2488/000119312526226746/d118163d8k.htm","excerpt":"The Credit Agreement provides for a five-year, $5.0 billion unsecured revolving credit facility (the “Revolving Facility”) and replaces the Company’s existing Credit Agreement dated as of April 29, 2022","as_of":"2026-05-15","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 13 份 8-K 中含重大項目者 3 份；無 Item 4.02（重編）申報。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000002488&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"AMD 於 2026-09-28 宣布以約 82 億美元全股票收購 World Labs，預計 2026 年底前完成，需監管核准。","source":"PrivSource","url":"https://www.privsource.com/acquisitions/deal/amd-to-acquire-world-labs-for-8-2-billion-in-all-stock-deal-ane_IFKSplj863","excerpt":"AMD to Acquire World Labs for Approximately $8.2 Billion September 28, 2026 AMD agreed to acquire World Labs in an all-stock transaction valued at approximately $8.2 billion.","as_of":"2026-09-28","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-09-28 宣布以約 82 億美元全股票收購 World Labs（預計年底前完成、待監管核准）；2026-06-15 宣布收購 MEXT（條款未揭露）。僅搜尋摘要，未讀原文。","source":"PrivSource；StreetInsider","url":"https://www.privsource.com/acquisitions/deal/amd-to-acquire-world-labs-for-8-2-billion-in-all-stock-deal-ane_IFKSplj863","excerpt":null,"as_of":"2026-09-28","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 清單無 Item 4.02（非可靠財報重編）申報；程式統計 3 份重大項目均非重編。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000002488&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"AMD","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":53.72,"operating_margin_pct":17.72,"fcf_margin_pct":15.53,"rd_intensity_pct":22.14},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"NVDA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.67,"operating_margin_pct":65.21,"fcf_margin_pct":41.92,"rd_intensity_pct":7.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"MRVL","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":52.21,"operating_margin_pct":16.81,"fcf_margin_pct":18.23,"rd_intensity_pct":25.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"3661.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.2,"operating_margin_pct":24.0,"fcf_margin_pct":-10.46,"rd_intensity_pct":9.17},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"AMD"},"financial_history":{"ticker":"AMD","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":23601000000.0,"revenue_yoy_pct":null,"gross_margin_pct":44.93,"operating_margin_pct":5.36,"net_income":1320000000.0,"diluted_eps":0.84,"free_cash_flow":3115000000.0,"fcf_margin_pct":13.2,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":22680000000.0,"revenue_yoy_pct":-3.9,"gross_margin_pct":46.12,"operating_margin_pct":1.77,"net_income":854000000.0,"diluted_eps":0.53,"free_cash_flow":1121000000.0,"fcf_margin_pct":4.94,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":25785000000.0,"revenue_yoy_pct":13.69,"gross_margin_pct":49.35,"operating_margin_pct":8.09,"net_income":1641000000.0,"diluted_eps":1.0,"free_cash_flow":2405000000.0,"fcf_margin_pct":9.33,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":34639000000.0,"revenue_yoy_pct":34.34,"gross_margin_pct":49.52,"operating_margin_pct":10.66,"net_income":4335000000.0,"diluted_eps":2.65,"free_cash_flow":6735000000.0,"fcf_margin_pct":19.44,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/AMD/AMD_Q3_2026_Earnings_Call_20261103.md）

# Q3 2026 Earnings Call
**Advanced Micro Devices, Inc.** | Earnings Calls | 2026-11-03

**Operator** (Operator):
Greetings. Welcome to the AMD Third Quarter 2026 Conference Call. [Operator Instructions] And please note that this conference is being recorded.
I will now turn the conference over to Matt Ramsay, VP, Financial Strategy and IR. Thank you, Matt. You may begin.

**Matthew Ramsay** (Executives):
Thank you, and welcome to AMD's Third Quarter 2026 Financial Results Conference Call. By now, you should have had the opportunity to review a copy of our earnings press release and the accompanying slides. If you have not had the chance to review these materials, they can be found on the Investor Relations page of amd.com. We will refer primarily to non-GAAP financial measures during today's call. The full non-GAAP to GAAP reconciliations are available in today's press release and slides posted on our website.
Participants on today's conference call include Dr. Lisa Su, our Chair and CEO; and Jean Hu, Executive Vice President, CFO and Treasurer. This is a live call and will be replayed via webcast on our website.
Before we begin, I would like to note that AMD will participate in the following events with the financial community this quarter. The UBS Technology and AI Conference on Tuesday, December 1; and Barclays 24th Annual Global Technology Conference on Wednesday, December 9.
Today's discussion contains forward-looking statements based on our current beliefs, assumptions and expectations, including forward-looking statements regarding financial projections, business and industry trends that speak only as of today and as such, involve risks and uncertainties that could cause actual results to differ materially from our current expectations. Please refer to the cautionary statement in our press release for more information on the factors that could cause actual results to differ materially.
With that, I will hand the call over to Lisa.

**Lisa Su** (Executives):
Thank you, Matt, and good afternoon to all those listening today. The third quarter was the largest and most profitable in our history as we began ramping our next-generation data center products. Revenue increased 45% year-over-year to $13.4 billion, driven by record EPYC and Instinct sales and strong embedded growth. Earnings per share grew even faster, increasing 74% to $2.09. We executed very well in the quarter with Helios production ramping as planned and EPYC adoption expanding across cloud, enterprise and super intelligence workloads.
Data center revenue growth has accelerated sequentially every quarter this year, with the segment contributing 64% of total revenue in the third quarter, up from 47% just 1 year ago. We expect that acceleration to continue in the fourth quarter, driven by increased demand for inference and agentic workloads and the ramp of our newest products.
Turning to our segments. Data center revenue grew 97% year-over-year to a record $8.5 billion. In server, both cloud and enterprise sales more than doubled year-over-year. We significantly exceeded our previous outlook of more than 80% growth as we gained revenue share. Customers deploy EPYC across more applications with agentic workloads contributing significant growth. In cloud, hyperscalers deployed substantial volumes of EPYC servers in the quarter to run more internal services and expand their public cloud offerings. Turin is now the most widely deployed EPYC generation in the public cloud with more than 540 instance types available globally from the largest providers.
Cloud providers also added significant EPYC capacity in the quarter for personal and enterprise agents, which are quickly becoming the next killer app for CPUs in the cloud. Meta's Muse and OpenAI's Dots illustrate how quickly personal agents are growing with more than 10 million people activating Muse agents in the first 6 weeks.
Enterprises are moving fast as well, putting agents to work across software development, supply chain and IT operations. These agents work continuously and in parallel across applications and enterprise systems, adding to accelerator demand while creating a substantial increase in CPU demand.
Adoption is just starting, and we expect demand to grow sharply as agents are deployed more broadly and take on more complex work. In head nodes, we won major deployments with several of the largest model developers and cloud providers in the quarter, which will ramp over the coming quarters. EPYC's leadership performance and mature ecosystem proven at scale have made it the host CPU of choice for custom accelerators. As 1 example, OpenAI selected Turin EPYC processors as the host CPUs for its first custom accelerator platforms.
In enterprise, EPYC server sell-through was a record with strong demand from new and existing customers. We added dozens of first-time EPYC customers in the quarter, including large financial services, communications, retail and health care companies. Existing customers are also making EPYC their primary compute platform, extending adoption from specific workloads to a much larger share of their overall infrastructure.
We began revenue shipments of EPYC Venice processors in the third quarter, and the first OEM systems are on track for availability this quarter. Early demand is the strongest we have seen for any new EPYC generation. Our OEM and ODM partners have committed more than 240 Venice platforms, 20% more than Turin, and cloud providers are deploying Venice this quarter ahead of instance rollouts planned for early 2027.
We recently launched Helion, a Venice reference design that enables turnkey EPYC rack-scale systems for agentic infrastructure. Customers can configure Helion for their workloads from all CPU racks for hyperscalers to enterprise systems combining Venice and Instinct GPUs that can run agents and models together. In the all CPU configuration, a single Helion rack has up to 144 Venice processors with nearly 74,000 threads, delivering the highest agent density in the industry. Every major server OEM and ODM plans to offer Helion, with the first system shipping this quarter.
Looking more broadly, demand for server compute is accelerating across cloud, enterprise, agentic and super intelligence infrastructure. EPYC is the industry's broadest portfolio spanning all of these markets with per-socket leadership for cloud and agents, per core leadership for enterprise and head nodes and memory and I/O options tuned to each workload.
Venice builds on that leadership with significantly better performance per watt, performance per core and performance per dollar than any other x86 or ARM server CPU, positioning us to gain share and significantly grow our server business as the TAM grows to approximately $220 billion by 2030.
Turning to our data center AI business. Frontier labs, hyperscalers and cloud providers expanded Instinct deployments for inferencing and training driving record revenue. We started shipping MI455X in volume in the quarter, and lead customers, including Anthropic, Meta, Microsoft, OpenAI and Oracle, brought their first Helios racks online quickly.
Customers are now running their latest models and workloads on Helios, and we are seeing very strong performance with the initial deployments. We expect Helios deployments to increase substantially in the fourth quarter as production continues to ramp and HPE, Dell, Lenovo, Super Micro and other OEM and ODM partners begin shipping systems.
We are very pleased with the overall performance we are seeing at the rack level. MI455X leads in compute flops, memory capacity and scale-out bandwidth. And as Helios comes to market, it delivers an even larger lead in memory bandwidth and higher scale-up bandwidth than the competition. We are working closely with our manufacturing and OEM partners to scale production as customers expand their deployments.
In supercomputing, EuroHPC selected Instinct MI430X GPUs and 6th Gen EPYC processors for LUMI-AI, Europe's next flagship supercomputer planned to come online in the second half of 2027. MI430X delivers nearly 9x the double precision performance of the competition, which is critical for scientific simulations. As a result, MI430X has now been selected to power next-generation systems around the world, and we are well positioned to win additional designs as governments and research centers plan their next major investments.
In software, we launched ROCm 10 with major enhancements for production deployments at scale, including faster start-up across large GPU clusters and greater resilience for long-running workloads. ROCm 10 also adds agentic performance tuning with ROCm.AI, which profiles workloads, identifies bottlenecks and applies and validates improvements, turning weeks of engineering optimization into hours.
Customers are also using their own agents to optimize models on our open software stack. For example, Anthropic highlighted that 1 engineer used Claude to bring up their latest model on Instinct MI355X racks over a single weekend with strong performance.
Our work with frontier labs is already enabling their models to handle complex software development and performance tuning for Instinct. And as those capabilities continue to improve, the benefits extend to everyone in the AMD ecosystem. We announced 2 acquisitions in the quarter to strengthen our Super Intelligence portfolio. Taalas brings a highly experienced engineering team and specialized silicon built for low latency, efficient inference. We plan to integrate their technology across our solutions portfolio to address the growing demand for low latency super intelligence applications. World Labs, led by Co-Founder and CEO, Dr. Fei-Fei Li, brings a world-class research team with expertise in spatial intelligence and models that understand the physical world, giving us deeper insight into how frontier models and workloads are evolving.
Fei-Fei will join AMD as Chief Scientist, leading our model research and helping shape our future hardware, software and systems road maps. We expect both acquisitions to close by the end of the year.
Looking ahead, our focus is on execution at scale. The racks of Venice, the MI450 Series and Helios are still early, and all 3 are on track to grow significantly. We now expect data center segment revenue growth to accelerate in the fourth quarter and full-year segment revenue to more than double from 2025.
Our visibility into 2027 also continues to strengthen. Last quarter, we said we expected annual server revenue to grow more than 70% and data center segment revenue to more than double for the year. Since then, customers have expanded their EPYC and Instinct deployment plans, and we have secured more supply to support that growth.
We now expect server revenue to double year-over-year in 2027 and data center AI revenue to grow even faster than we projected 90 days ago. As a result, we expect data center to be more than 80% of our total revenue in 2027 and to drive the majority of our revenue and earnings growth.
Looking further out, customer engagements for MI500 continued to progress very well. Interest is very high as it is another significant leap forward in performance. We are working very closely with multiple frontier labs to optimize MI500 for their workloads as they plan multi-gigawatt deployments.
Turning to client and gaming. Segment revenue decreased 8% year-over-year to $3.7 billion. In client, revenue increased 7% year-over-year to $2.9 billion, driven by strong sales of our Ryzen mobile processors. Commercial is becoming a larger part of our client business as large enterprises adopt Ryzen PRO PCs across their employee base. 8 of the 10 largest banks in the world and 7 of the 10 largest health care and automotive companies now use Ryzen PRO PCs.
OEMs continue expanding their AMD-based commercial lineups from everyday business PCs to high-end workstations. HP, Lenovo and others launched the first commercial notebooks and small form factor desktops featuring our newest Ryzen AI Max PRO 400 series processors. These systems deliver workstation class performance and run super intelligence models with up to 300 billion parameters locally.
Looking at the market, PC sell-through slowed late in the quarter as higher memory and component costs weighed on demand. We are managing the business accordingly, aligning sell-in with sell-through to keep customer and channel inventory healthy. In 2027, we are planning for PC market unit shipments to decline by a double-digit percentage. In this environment, we expect to outperform the market as we deliver our Ryzen road map and grow our commercial footprint.
In gaming, revenue declined 40% year-over-year to $773 million, primarily due to lower semi-custom sales as expected at this stage of the console cycle. Gaming graphics revenue declined year-over-year, while Radeon GPU channel sell-through increased sequentially. Beyond gaming, Radeon AI Pro revenue grew significantly from the prior quarter as more developers choose AMD to run and fine-tune models locally. We expect strong growth for Radeon AI Pro to continue, driven by our leadership performance per dollar and an open software stack optimized for the latest open source models.
Turning to our Embedded segment. Revenue increased 29% year-over-year to $1.1 billion, the fourth consecutive quarter of accelerating growth. Demand was very strong across all of our end markets, led by strong growth with aerospace and defense, automotive, communications and industrial customers. Data center build-outs are also driving higher demand for our embedded CPUs and adaptive SoCs in control plane and optical networking applications. We remain on track to close more than $18 billion of design wins in 2026, our third consecutive record year. Adaptive design wins have increased every year since we acquired Xilinx with embedded x86 and semi-custom wins growing even faster. As these wins ramp over the next few years, we expect our embedded business to deliver strong double-digit annual revenue growth and continue outgrowing the market.
In summary, we delivered an excellent third quarter and expect an even stronger fourth quarter as data center and embedded segment growth more than offsets lower client CPU sales. We entered 2027 with the strongest product portfolio in our history and significant customer momentum. We have worked across our supply chain to secure the wafers, substrates, advanced packaging, memory and other key components needed to support much higher growth next year.
Based on our current visibility, we now expect revenue to grow more than 80% in 2027, which is more than twice the long-term financial model we outlined at our Financial Analyst Day last November. Data center will be the largest contributor, driven by expanding Helios deployments and continued EPYC share gains. We also expect embedded growth to accelerate next year driven by adoption of our adaptive and x86 solutions.
Beyond 2027, we are increasing R&D investment across our silicon, software and systems road maps and working closely with our largest customers to support their ambitious infrastructure plans for the next 3 to 5 years. We are also deepening our collaboration with our supply chain partners and investing alongside them to secure the long-term capacity our growth will require.
Taken together, these give us strong confidence in our ability to sustain exceptional revenue growth for years to come, with earnings growing even faster.
Now I will turn the call over to Jean to provide additional color on our third quarter results. Jean?

**Jean Hu** (Executives):
Thank you, Lisa, and good afternoon, everyone. I'll start with a review of our financial results and then provide our outlook for the fourth quarter of fiscal 2026.
We delivered an outstanding third quarter. Revenue increased 45% year-over-year to a record $13.4 billion, exceeding the high end of our guidance, driven by our data center segment, which nearly doubled year-over-year. Revenue increased 16% sequentially, driven by strong growth in the data center and embedded segments, partially offset by a decline in the client and gaming segment. Our data center segment accounted for approximately 64% of total revenue, up from 58% last quarter, underscoring the continued shift in our business mix and its increasing contribution to AMD's growth.
Gross margin was 56%, up 190 basis points year-over-year, reflecting a richer product mix. Operating expenses were $3.6 billion, an increase of 29% year-over-year as we continue to invest in R&D to expand our data center silicon systems and software capabilities. Operating income grew 75% year-over-year to a record $3.9 billion, significantly outpacing our revenue growth. Operating margin was 29%, expanding more than 5 percentage points year-over-year, underscoring the operating leverage in the business as we scale.
In the third quarter, we began recognizing the accounting impact of warrants issued under our previously announced customer agreement as we shipped MI450 Series GPUs. Our GAAP diluted earnings per share were $1.46, which included $1.1 billion noncash charge in other income and expense, primarily reflecting the increase in our share price and the changes in the estimated probability of meeting the warrant conditions.
Going forward, these quarterly noncash fair value adjustments are expected to increase as we and our customers progress under this agreement. The amount will vary each quarter based on AMD's stock price and other valuation assumptions. These noncash adjustments would not affect our non-GAAP results or free cash flow. Our non-GAAP diluted earnings per share were $2.09.
Now turning to our reportable segments, starting with the data center. Data center segment revenue was a record of $8.5 billion, up 97% year-over-year, driven by record server revenue and strong demand for our 5th generation EPYC processors and by record data center AI revenue, highlighted by the launch of our AMD Instinct MI450 Series GPUs.
On sequential basis, data center revenue increased 27%, primarily driven by initial MI450 Series sales and strong server revenue growth. The data center segment operating income was $2.9 billion, up 168% year-over-year. And the operating margin increased to 34% compared to 25% a year ago, demonstrating strong operating leverage of data center business.
Client and Gaming segment revenue was $3.7 billion, down 8% year-over-year due to lower semi-custom and graphics sales, partially offset by higher demand for the latest generation Ryzen mobile processors. In the client business, revenue was $2.9 billion, up 7% year-over-year, driven by higher sales of Ryzen mobile processors. Sequentially, client revenue was down 4% as higher memory cost weighed on PC unit demand, partially offset by a richer mix of high-end processors.
Gaming revenue was $773 million, down 40% year-over-year due to lower semi-custom revenue and lower graphics demand. Sequentially, gaming revenue was essentially flat. Client and Gaming segment operating income was $573 million or 15% of revenue, compared to $867 million or 21% a year ago.
Embedded segment revenue was $1.1 billion, up 29% year-over-year and 14% sequentially as demand strengthened across several end markets, led by growth in aerospace and defense, automotive, communication and industrial end markets. Embedded segment operating income was $453 million or 41% of revenue compared to $283 million or 33% a year ago.
Turning to balance sheet and cash flow. During the quarter, inventory increased approximately $3 billion sequentially to $11.5 billion to fulfill our strong data center demand. We generated $1.2 billion in cash from operating activities of continuing operations. Free cash flow was $554 million, reflecting increased working capital investment and ongoing capital expenditures to secure equipment and capacity for the rapid growth of our data center business, including back-end capacity dedicated to support our data center demand. We expect to continue to invest in inventory and capacity to support our strong growth in 2027.
At the end of the quarter, cash, cash equivalents and short-term investments were $15.8 billion. Our total debt was $7.1 billion, including $4.75 billion senior notes offering we completed in August.
Now turning to our fourth quarter 2026 outlook. We expect revenue to be approximately $17 billion, plus or minus 3%. The midpoint of our guidance represents approximately 66% year-over-year revenue growth, primarily driven by the acceleration of our data center segment. Sequentially, we expect revenue to grow by approximately 27%, driven by a sharp increase in our data center segment of approximately 50% growth, a decline in our client and the gaming segment of greater than 20% and a double-digit growth in our Embedded segment.
In addition, we expect fourth quarter non-GAAP gross margin to be approximately 55%, and we expect non-GAAP operating expenses to be approximately $3.75 billion. We expect non-GAAP net interest and other expense to be a gain of approximately $4 million. We expect our non-GAAP effective tax rate to be 13%, and diluted share count is expected to be approximately 1.67 billion shares, including the estimated impact of closing the Taalas and the World Labs acquisitions in the fourth quarter. We are not expecting our fourth quarter share count to be impacted by customer warrants.
In closing, the third quarter was an outstanding quarter for AMD with record revenue, significant operating margin expansion and earnings growth, reflecting disciplined execution across the business. As our data center business continues to scale, we are very well positioned to drive increased profitability and long-term shareholder value.
With that, I'll turn it back to Matt for the Q&A session.

**Operator** (Operator):
[Operator Instructions] And the first question comes from the line of Tom O'Malley with Barclays.

**Thomas O'Malley** (Analysts):
Congrats on the great results. I guess, Lisa, let's start off with the fact that you're giving some more color into 2027. It looks like revenue is growing 80%, but the data center component of that is growing much faster where data center is going to be a greater than 80% of your business. So maybe can you talk about, first and foremost, like is this backed up by supply, whether that be wafers, packaging, substrate, memory? And then if you look at the demand profile behind that, would demand outstrip that supply if you were able to get some more?

**Lisa Su** (Executives):
Yes. Sure, Tom. Thanks for the question. So look, we have a lot of momentum going into the fourth quarter and into 2027. We do see a situation where there is very strong demand. So we see demand across the data center business, across our CPU business as well as our data center AI business. And when you look at the rate and pace of that growth, we've been planning for it for the last several years. So we've absolutely spent a significant amount of time with our customers planning what their needs are in terms of their deployments and their deployment schedules and also with our supply chain partners to ensure that we have the wafers, the substrates, the advanced packaging, the memory, all of the other components that go along with it.
It is true that demand is higher than supply. So we continue to work with our supply chain partners to increase supply. And I do believe that there is a good opportunity for us to do that, just given the strong relationships we have throughout the ecosystem. But sitting where we are today to be able to say that the overall company will grow greater than 80%, especially the server business will approximately double from a fairly high point in 2026. And then the data center AI business, we continue to have strong visibility, and we see strong demand from our customers, and we continue to see also good follow-through on all of the other aspects of the infrastructure that are needed. So overall, we're very positive about the data center growth into 2027.

**Thomas O'Malley** (Analysts):
And then just as a follow-up on the client side, you're saying down greater than 20% in the fourth quarter. That's kind of in line with what we've heard from others so far in the market. But if you look at '27, I think something that's difficult that normally you see seasonality down in Q1 and then you wouldn't get a recovery kind of until Q2, Q3. So maybe talk about like what the longevity of this correction kind of looks like and why you've been able to kind of outperform a bit up until this point and how you see that kind of coming out of this trough into next year?

**Lisa Su** (Executives):
Yes. Sure, Tom. So talking a little bit about the PC market. The PC market continues to be an important market to us. I think we were signaling all along in the last couple of calls that we were expecting a subseasonal second half of the year, and that's how it's played out. Our view is this is one of those times when component prices go up, it affects overall system pricing. One would expect the consumer markets to be more sensitive to that. And so we have seen a bit of slowdown in the sell-through.
We're just managing the business very prudently, and we want to ensure that inventory stays healthy throughout the channel and throughout our customers. And so our planning assumption for 2027 is that the market will be double-digit percentage down. We will certainly focus on the segments where we can add the most value, places like enterprise, where we continue to be underrepresented, premium consumer, desktop channel. These are really good markets for us. But we are planning with the current environment for a down year for 2027. And we will work through that.
The good part about it is, our supply chain is quite fungible across our PC business and our data center business. And so that actually does afford us the ability to move supply around as we see these signals in the market. And overall, as I said earlier, we do have more demand than we have supply. And so we're continuing to work all of the aspects to increase supply as we go through the next few quarters.

**Operator** (Operator):
And the next question comes from the line of Vivek Arya with Bank of America Securities.

**Vivek Arya** (Analysts):
Lisa, there's a lot of market debate about the financing of data centers and availability of land, power and shell, et cetera. So kind of a 2-parter, what's the level of confidence, right, that AMD has that your anchor customers have the financing and the physical infrastructure to support, I think it's roughly 3 gigawatts or so of planned AMD deployments into '27?
And then, as we look beyond, many of your competitors are kind of investing in the ecosystem, providing residual value guarantees, and such. I'm saying there is a lot more fungibility of their products. So does that create kind of a competitive dynamic for AMD? So just curious to hear your perspective on '27 readiness and '28 competitive landscape?

**Lisa Su** (Executives):
Sure, Vivek. Thanks for the question. So as I said earlier, we're seeing very strong demand from our lead data center AI customers. I think you can see that there's a strong demand for more compute and MI455 is positioned extremely well. When we look at Venice, MI455, Helios, I think we feel extremely good about the competitiveness.
We have been planning for this ramp with our customers jointly. So we have good visibility into the 2027, as you said, land, power, shells, all of those, the data center infrastructure, and we are very much working hand-in-hand with our customers. So we know where the GPUs are going in terms of which data centers and which locations and all of that stuff.
Going into 2028 and beyond, I guess, what I would say is the following. Look, I think we are seeing very strong growth overall. I think we have a very strong business. We have a very strong balance sheet. And from that standpoint, our goal is, first and foremost, we're investing in our growth to support that, and that means investing in R&D, investing in supply chain and capacity, investing alongside our partners to ensure that we have the capacity for all of those things that we talked about earlier that are necessary for this type of ramp.
And then we are selectively investing with our lead partners where we see it's helpful to have, for example, the data center infrastructure identified way in advance, and that's multiple years in advance. And I think that's the right thing to do to ensure that we are jointly ensuring that there's the right infrastructure as our new chips become available. But we are being selective and strategic in how we do that with the first principle being investing in our growth.

**Vivek Arya** (Analysts):
And for my follow-up, Lisa, one more on the competitive landscape. Many of your Frontier lab customers have been working on their custom ASICs. And I'm curious, how do they conceptually make the choice between using ASICs versus AMD products? Like what determines their allocation? Is it cost per token, power efficiency, software flexibility, time to deployment? What are the puts and takes in that decision making? And are there workloads where using an AMD GPU works better than the alternatives that they have?

**Lisa Su** (Executives):
Sure, Vivek. So look, I think we feel extremely good about where we're positioned in terms of our performance and our total cost of ownership that we're delivering with Helios. That is fundamentally the most important factor when we think about sort of deployment scale and deployments going forward. I think there was a significant investment that we've made in the rack-scale systems and ensuring that Helios really ramped nicely. Third quarter was the first quarter that we shipped MI455 and Helios racks for revenue. I think this is a very major milestone. We have a big step up in Q4. We'll continue to ramp throughout 2027.
And the key is for us to continue to show that TCO advantage across workloads. It is true that from general purpose CPU standpoint, that we have more fungibility as you think about various workloads that occur. There has been also very strong codesign. So beyond the MI450 Series, we're working on MI500 and MI600 as well to ensure that our technology gets even more, let's call it, tuned to what the frontier labs need. So I think that's -- those are the key factors in terms of deployment choices.

**Operator** (Operator):
And the next question comes from the line of Joshua Buchalter with TD Cowen.

**Joshua Buchalter** (Analysts):
Congrats on the progress. I was wondering if you could give us insight into how we should be thinking about HBM costs impacting your model as the Instinct business ramps. I think investors have been asking how your revenue per gigawatt contribution in the last year or so, your outlook has been so consistent in that $15 billion to $20 billion per gigawatt range given what's going on with HBM pricing. Is that because early builds are fairly program-specific and pricing was agreed upon a long time ago? And again, as we think about that business longer term, do you have the ability to pass on these higher input costs even to your big 3 customers?

**Lisa Su** (Executives):
Sure, Josh. So the way to think about it is as we ramp, we have had, let's call it, long-term agreements with some of our suppliers as well as some of our customers. But given where the memory market is and not just the memory market, by the way, other component costs are also seeing some inflationary pressures in the sense of as there is more CapEx that's put into the overall supply chain environment. We are also working with our customers to include -- to ensure that those costs are shared as we go forward.
So from my perspective, back to the question that Vivek had, this is all about TCO and ensuring that from a tokens per dollar standpoint, that we continue to offer very strong advantages for choosing AMD Instinct in our overall Helios system. And even with some of the inflationary pressures that are out there, we certainly believe that we are offering a leading TCO for the AI workloads.

**Joshua Buchalter** (Analysts):
And maybe for Jean, it was good to see OpEx come in light in the third and fourth quarter. It's been a sticking point for investors for a little bit. But I guess given how steep the revenue growth is expected to be in 2027, we're flying a little blind given you're kind of more than 2x your target model. How should we think about OpEx growth in '27? And I guess while I'm in the neighborhood, do you think you can hold your target gross margin range sort of that 55% floor as we move through the year and Helios continues to ramp?

**Jean Hu** (Executives):
Yes. Josh, thank you for the question. On the OpEx, as you said, we have been investing aggressively. What you are seeing is the investments are translating to accelerating revenue growth we are seeing in 2026. We're actually quite pleased with the 2026, our operating leverage. We're expanding revenue much faster than OpEx growth, which is driving the operating margin increase. And if you think about the Q4 guide, we are guiding very significant revenue growth more than OpEx.
That dynamic, we believe, will carry into 2027, Lisa talked about is that we expect the whole company growing more than 80%. We should expect OpEx to grow less than the top line revenue growth rate -- less half -- less than half of the top line revenue growth rate. So that will drive a very significant operating margin expansion in 2027.
Going back to gross margin, we are actually very happy about where we are with our gross margin. In Q3, we are ramping MI450. Data center AI business is doing very well, actually better than our expectation when we got into the Q3 quarter. And in Q4, we are guiding sequentially revenue growing 50% for data center business. It's actually going to be the quarter data center AI business surpassed server business. So we all know their margin is a little bit dilutive to corporate average, but the gross margin dollars are increasing very significantly.
I think looking ahead of 2027, we actually think that our data center business will be more than 80% of the total company revenue. So the mix of data center business is going to drive the company's gross margin significantly. The way to think about this data center AI will continue to ramp through 2027, and the server business is expected to double. So quarter-over-quarter, there may be variations because the mix of those businesses will be a little bit different.
In addition, embedded business is strengthening in 2027, I think that will also help our gross margin. Overall, when you put the whole business model together, what you should expect us to do with significant top line revenue growth, significant gross profit expansion and OpEx growing less [indiscernible] and revenue growth, which will result in very significant operating margin expansion and profitability expansion.

**Operator** (Operator):
And the next question comes from the line of Timothy Arcuri with UBS.

**Timothy Arcuri** (Analysts):
Lisa, I'm wondering if you can break down a little bit how data center is going to look like next year. You did revise server CPU up from up 70% to more than 100%, but you're not being super specific about data center AI. So is the right way to think about it that the GPU business will still be bigger in dollars than the server CPU business, but not much? Is that the right way to think about the split? And then how to think about the shape of the year? I know that the GPU business is lumpy, but I imagine it's probably pretty ratable through the year. Is that kind of fair to think there?

**Lisa Su** (Executives):
Yes, Tim, maybe let me break down a couple of things. So first of all, we think 2027 is going to be a very strong momentum year for both the CPU business as well as the data center AI business. And when we gave you some of the markers, you should just consider them markers, right? So we've said the overall company will grow greater than 80%. And for the data center CPU business, we will about double; and for the data center AI business, it will significantly more than double. And from that standpoint, you should expect that the data center AI business continues to be, as Jean just said, Q4 is the first quarter where the data center AI business will cross over in terms of size compared to the CPU business. And we would expect both businesses to grow nicely throughout the year. So hopefully, that gives you a bit of shape as we go through the year.

**Timothy Arcuri** (Analysts):
And then, Jean, I guess, can you help us on the warrants? How are they going to layer in through the year? Any sort of like guardrails you can give us on sort of how to roll that into our model through the year and into 2027?

**Jean Hu** (Executives):
Yes. Thanks for the question. I think the simple way to think about it is there are 3 parts for the warrant. The first one is we report net revenue, the Q3 revenue, Q4 guide and whenever we talk about the revenue, it's always net revenue, which already incorporated the warrant revenue reduction piece, which is determined at the grant date of fair value. So that one you should not worry about it. It's always incorporated in our revenue whenever we talk about the revenue.
The second piece is probably you're asking is the share count. The way to think about this, the share count only comes into diluted shares once all the vesting conditions and the exercising conditions are met by our customers. That means the shipments need to be there and some commercial conditions that need to be met. We are going to provide the guidance in 2027 to give you clear guidance when we believe the share vesting and exercising conditions are met. That is something we'll provide transparency once we get into 2027.
The last piece is it's a noncash charge, quarterly noncash charge, which is a remeasurement of fair value, that actually does not impact our non-GAAP financial results and free cash flow. So on the share count, just wait for us to provide you a clear guidance when we get there.

**Operator** (Operator):
And the next question comes from the line of C.J. Muse with Cantor Fitzgerald.

**Christopher Muse** (Analysts):
I guess first question, on the server CPU side, you've obviously taken your outlook higher. I'm curious how we should be thinking about units versus mix, including higher core count as well as higher ASPs associated with Venice. Is there a way to break that down to help us understand that 100% growth?

**Lisa Su** (Executives):
Sure, C.J. So on the server CPU side, when we talk about 100% growth, you should imagine that we are definitely shipping significantly more units in that. Of course, some of those units have higher core counts as we go into Venice. But I would say the growth in revenue is mostly in units and core count and less so in ASPs, although there are some -- there's an ASP uplift as we increase core count.

**Christopher Muse** (Analysts):
And just as a follow-up, just to button down 1Q seasonality. Based on what you said tonight, I'm interpreting that we should see kind of normal client and gaming down seasonally in Q1 kind of ratable data center above December. And I guess as part of that, any sort of vision for how to think about embedded?

**Jean Hu** (Executives):
For the embedded business, typically, there is seasonality. We do see overall, when we look at the 2027 for the whole year, embedded business is actually going to grow significantly and also strengthening through the year. But typically, Q1, actually, there is some seasonality for embedded business.

**Operator** (Operator):
And the next question comes from the line of Stacy Rasgon with Bernstein Research.

**Stacy Rasgon** (Analysts):
I was wondering, I know you said that you had crossover for GPU versus CPU in Q4 within the context of that 50% guide. I was wondering if you could help us with the magnitude of that crossover? Is it just barely there? Or like is it like significantly higher? I'm just trying to get the sizing in my head in terms of the entrance rate in the next year?

**Jean Hu** (Executives):
Yes. Stacy, maybe I'll give you some color, right? Is the way to think about it is if you think about the MI450 ramp, it's a very significant step up sequentially from Q3 to Q4. And that really compared to server side, server is growing really nicely, strongly. But the ramp of data center AI, which surpassed the server in Q4. That is a very significant step up. I think the way server business, of course, is very strong, but the data center AI will be much higher than server business in Q4.

**Stacy Rasgon** (Analysts):
In terms of dollars?

**Jean Hu** (Executives):
Yes, in terms of dollars.

**Stacy Rasgon** (Analysts):
And for my follow-up, there were some questions earlier about gross margins next year. I wasn't exactly quite sure how to interpret your answer in terms of the gross margins next year relative, I guess, to the Q4 rate. Do you think you could give us some color or some highlights on like a good entrance rate and a good exit rate for gross margins in 2027, given that the ramps of the different products and everything that are happening?

**Jean Hu** (Executives):
Yes, Stacy, the reason we are not able to provide you quarter-over-quarter. It's really because -- when you think about the data center mix is the primary driver in 2027. When you have a data center business, revenue is more than 80% of the total company business. And then within data center, the interesting part is you have a data center AI business continue to ramp significantly. On the server side, we did mention, Lisa mentioned that we're going to double in 2027. Of course, we also know the supply constrained environment and Lisa also mentioned that we are working with our suppliers to ensure we get more supplies. So the mix between those 2 businesses actually determine what the company's gross margin will be. Right now, I actually don't have that visibility. I think we hope both businesses are going to do great. And we know they're going to both doing great.
Q4 actually, is a good benchmark to think about it is because Q4 data center AI business is much higher than CPU business. So I think that gives you some idea at that benchmark. Then in 2027, different quarter could be different. There could be variation there.

**Operator** (Operator):
And the next question comes from the line of Joe Moore with Morgan Stanley.

**Joseph Moore** (Analysts):
We've heard quite a bit of positive feedback on the Helion racks. And I wonder if you could talk a little bit about that. In the CPU-only version of that, what's different for sort of these agentic workloads versus a traditional rack? And then do you anticipate an attach rate of the GPU blade in a lot of these?

**Lisa Su** (Executives):
Sure, Joe. Yes, there is quite a bit of positive excitement around the Helion racks. And I think the main point there is these agentic racks, they really want to be optimized for the environment that they're in. So if they are in, let's call it, hyperscaler or large cloud racks, you're going to have them in all-CPU configurations. It's going to be quite dense. Venice is the -- from a performance per socket standpoint is the best in the industry. And so that will translate into a very strong agentic rack if you fully populate it with CPUs.
But in enterprise areas, you will also see the opportunity to mix CPUs and GPUs. And it just allows people to really optimize for the workloads that they're in. And it is -- we have contributed to OCP. So it's a fully open rack, and I think that is viewed as a positive. And from that standpoint, we've gotten very positive feedback from both OEMs and ODMs as well as customers.

**Joseph Moore** (Analysts):
And if I could follow up, the 100% growth in server, do you think you're meeting demand at that level? Or do you think you still have kind of a shortage condition through all of next year?

**Lisa Su** (Executives):
Well, Joe, for us to grow that amount, we're meeting a lot of demand. And when you look at -- when we talked about the TAM growing, let's call it, about 50% CAGR over the next 3 or 4 years, we saw growth in sort of 3 areas, right? So traditional cloud and enterprise, agentic, CPUs and agentic workloads and head nodes. We believe we're gaining share in each one of those segments as we give you that forecast of roughly 100%.
I do believe there's more demand, and we are actively working with our supply chain partners to satisfy additional demand. Obviously, we also have to make sure that the squared sets are there and DDR5 and all of the other components are there. But my view is we are taking a big step up in terms of the demand forecast from our customers. I'm excited about the fact that our demand is broad-based. So it is really virtually across every customer in terms of their expansion of their footprint with AMD. And so that's positive. And we're going to continue to work on increasing supply to meet additional demand as it comes to fruition.

**Matthew Ramsay** (Executives):
John, I'm actually going to ask you to have one more caller join us, please. I think we have time for one more question here.

**Operator** (Operator):
Our final question comes from the line of Harsh Kumar with BMO Capital Markets.

**Harsh Kumar** (Analysts):
Lisa, question is on Helios. So you're one of 2 companies shipping complete racks. Can I ask you about what your share aspiration is? And the reason why I'm asking is you've done a wonderful job in servers, taking share from basically a very difficult competitor. And also, the second part of that question is, do you have aspirations to address the enterprise market with this -- with the Helios rack in the setup? And then I have a follow-up.

**Lisa Su** (Executives):
Sure, Harsh. So look, we're very happy with the progress that we've made with Helios. I think this is a significant -- the rack-scale solutions are significant R&D efforts. I think Helios has ramped very nicely. We saw a very -- a good initial quarter in Q3. We're ramping nicely into Q4 and into 2027. Our aspirations are to be a very significant compute supplier to our largest customers, both frontier labs as well as hyperscalers. And from that standpoint, the focus on Helios MI450 ramp is very much on our minds for Q4 and 2027. But we're in very active dialogues with our largest customers on MI500 and MI600 and beyond. And our aspirations are to continue to have a larger and larger piece of their compute needs. And from everything that we see, demand continues to go up. So I think that's the overall view on Helios.
Was there another part of that question?

**Jean Hu** (Executives):
Enterprise.

**Lisa Su** (Executives):
Enterprise. Yes, certainly. I think we continue to see -- although enterprise is developing, let's call it, a little bit slower than the largest frontier labs and hyperscalers, we do believe that the enterprise business is quite important. We have made a lot of progress in enterprise CPUs. Many of our enterprise customers are actually asking for our advice as to how to deploy AI and how to ensure that they're deploying it as efficiently as possible when you think about both on-prem as well as cloud deployments. So we are expanding our portfolio. We've introduced some enterprise-specific GPUs, and that will be a place where we would like to grow our footprint to, again, be a very strategic supplier to our largest enterprise customers.

**Harsh Kumar** (Analysts):
And my follow-up is on the client side. Historically, you've done a great job managing this business through situations like this. What would be your share keep strategy if your chief competitor was to cut ASPs, would you try to match them? Or would you be -- would you have to just gauge the situation as it goes? Just be curious about how you're going to manage this.

**Lisa Su** (Executives):
Yes. I think, Harsh, our view is PCs are an important market for us in the standpoint of -- I'm a big believer in end-to-end AI deployment, so from cloud to edge to clients, and we have a unique portfolio in that fashion. That being the case, I think we're always quite disciplined in how we manage. Our focus has really been on the most -- the highest value and most profitable segments of the PC market. Enterprise, premium consumer, desktop channel. These are places that we do very well. We do recognize that there's a good amount of volatility in the low end of the market, and that's a place where we have the least exposure, frankly, to that portion of the market.

**Matthew Ramsay** (Executives):
All right. Thank you, John, for organizing the Q&A. Thank you, everybody, for joining our call. We really appreciate you spending some time with AMD and thank you very much for your questions and your attention. John, go ahead and close the call. Thank you very much.

**Operator** (Operator):
Thank you, Matt. And ladies and gentlemen, thank you for your participation. This does conclude today's teleconference. You may disconnect your lines at this time, and have a wonderful day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AMD_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜CFO Jean Hu｜guidance：CFO 給 Q3 營收指引約 130 億美元，上下 3 億（原話："We expect revenue to be approximately $13 billion plus"）
- 2026-08-04｜CFO Jean Hu｜margin：Q3 non-GAAP 毛利率指引約 56%（原話："third quarter non-GAAP gross margin to be approximately 56%"）
- 2026-08-04｜CFO Jean Hu｜guidance：Q3 non-GAAP 營業費用指引約 36.5 億美元（原話："operating expenses to be approximately $3.65 billion"）
- 2026-08-04｜CFO Jean Hu｜guidance：Q3 non-GAAP 有效稅率指引 13%（原話："Non-GAAP effective tax rate to be 13%"）
- 2026-08-04｜CEO Lisa Su｜guidance：CEO 上調伺服器 CPU 營收下半年年增幅度（高於 80%）（原話："more than 80% year-over-year in the second half of 2026"）
- 2026-08-04｜CEO Lisa Su｜guidance：CEO 表示 2027 年資料中心部門營收將年增逾一倍（原話："more than double year-over-year in 2027."）
- 2026-08-04｜CEO Lisa Su｜guidance：Q3 資料中心部門指引為季增雙位數，Q4 更高（原話："grow sequentially double digits"）
- 2026-08-04｜CEO Lisa Su｜guidance：Helios 放量節奏：Q3 起步、Q4 加大、Q1 再加大（原話："Q1 will be a further step up"）
- 2026-08-04｜CEO Lisa Su｜guidance：CEO 回應分析師：資料中心 AI 2027 年預期成長遠高於 100%（原話："the data center AI business is going to be well over"）
- 2026-08-04｜CEO Lisa Su｜guidance：CEO 對分析師估算的 2027 資料中心 AI 數字表示偏低（原話："number is probably too low."）
- 2026-08-04｜CEO Lisa Su｜guidance：CEO 將長期營收成長目標上調至高於先前 35%（原話："substantially above our prior target of greater than 35%"）
- 2026-08-04｜CEO Lisa Su｜guidance：CEO 表示將在策略期間內顯著超越 20 美元年度 EPS 目標（原話："significantly exceed our $20 annual EPS target"）
- 2026-08-04｜CEO Lisa Su｜guidance：CEO 上調 2030 資料中心 AI 加速器 TAM（年增逾 45%）（原話："accelerator market to grow more than 45% annually"）
- 2026-08-04｜CEO Lisa Su｜guidance：CEO 上調 2030 伺服器 CPU TAM（年增逾 50%）（原話："server CPU market to grow more than 50% annually"）
- 2026-08-04｜CFO Jean Hu｜margin：Q2 毛利率 56%，年增逾 200bp（原話："Gross margin for the quarter expanded to 56%"）
- 2026-08-04｜CFO Jean Hu｜margin：CFO 說明資料中心 AI 的毛利率略低於公司平均（逐字含原稿用字 copper）（原話："gross margin is slightly below copper average"）
- 2026-08-04｜CFO Jean Hu｜margin：CFO 表示 2027 毛利率由伺服器與資料中心 AI 的組合決定，伺服器為毛利率增益項（原話："Overall, I think they have a good offset in general overall."）
- 2026-08-04｜CFO Jean Hu｜margin：CFO 稱嵌入式業務復甦將在 2027 提供毛利率順風（原話："Embedded business is recovering significantly."）
- 2026-08-04｜CFO Jean Hu｜margin：資料中心部門營業利益 21 億美元、占營收 31%（原話："segment operating income was $2.1 billion or 31% of revenue"）
- 2026-08-04｜CFO Jean Hu｜margin：客戶端與遊戲部門營業利益率由去年同期 21% 降至 15%（原話："$582 million or 15% of revenue compared to $767 million"）
- 2026-08-04｜CEO Lisa Su｜margin：CEO 拆解 Q2 伺服器成長：單位數與 ASP 均雙位數成長，單位數成長較高（原話："ASPs, but it was actually more unit"）
- 2026-08-04｜CFO Jean Hu｜commitment：CFO 承諾營業費用成長低於營收成長以創造營運槓桿（原話："OpEx increase less than the top line revenue growth"）
- 2026-08-04｜CFO Jean Hu｜commitment：CFO 表示營收成長將快於 TAM（原話："we'll be growing faster than TAM"）
- 2026-08-04｜CEO Lisa Su｜commitment：CEO 表示公司計畫每年推出新一代機櫃級 AI 平台（原話："we plan to launch a new rack scale AI platform every year"）
- 2026-08-04｜CEO Lisa Su｜commitment：CEO 稱供應足以滿足已給的資料中心指引（原話："we have supply to more than meet the guidance"）
- 2026-08-04｜CEO Lisa Su｜commitment：CEO 表示看不到會讓公司對達標產生疑慮的因素，並指出範圍取決於產能到位時程（原話："I don't think we see anything that would give us pause"）
- 2026-08-04｜CEO Lisa Su｜commitment：CEO 稱 2027 伺服器供應狀況將優於 2026（原話："the 2027 server supply situation should be better than"）
- 2026-08-04｜CFO Jean Hu｜commitment：CFO 說 2027 毛利率更多細節待屆時再提供（原話："we'll give you more color when we get there to guide"）
- 2026-08-04｜CEO Lisa Su｜customer：新宣布 Anthropic 合作：最多 2GW 的 MI450 系列（原話："Anthropic will deploy up to 2 gigawatts of MI450 series"）
- 2026-08-04｜CEO Lisa Su｜customer：與 OpenAI、Meta 的多世代 GW 級部署（原話："gigawatt scale deployments with OpenAI and Meta"）
- 2026-08-04｜CEO Lisa Su｜customer：CEO 說 Helios 客戶拉貨強於原先預測（原話："tracking ahead of our initial forecast"）
- 2026-08-04｜CEO Lisa Su｜customer：CEO 說明每 GW 營收仍在雙位數十億美元範圍（原話："I think we've said double-digit billions"）
- 2026-08-04｜CEO Lisa Su｜product：Helios 已投產，初期出貨預計本季稍後開始（原話："initial shipments on track to begin later this quarter"）
- 2026-08-04｜CEO Lisa Su｜product：CEO 稱 Venice 客戶需求強於歷代 EPYC（原話："Customer demand for Venice is stronger than for any prior"）
- 2026-08-04｜CEO Lisa Su｜product：Cerebras 合作方案預計 Q4 起在 Cerebras 雲端提供（原話："start becoming available in Q4 in the Cerebras cloud"）
- 2026-08-04｜CEO Lisa Su｜product：嵌入式部門新設計案目標：年度逾 180 億美元（原話："more than $18 billion of new design wins"）
- 2026-08-04｜CEO Lisa Su｜competition：管理層宣稱 Helios 相對競品每美元可多產出 30% tokens（原話："up to 30% more tokens per dollar than the competition"）
- 2026-08-04｜CEO Lisa Su｜competition：管理層宣稱 Venice 每瓦效能對 ARM CPU 領先（原話："up to 3.3x the performance per watt of"）
- 2026-08-04｜CEO Lisa Su｜competition：管理層稱 Q2 伺服器 x86 營收市占年增提升（原話："exceeding the outlook we provided last quarter"）
- 2026-08-04｜CEO Lisa Su｜risk：CEO 表示 HBM 配置能見度佳，同時承認部分工作負載可能調整記憶體配置（原話："There is very good visibility into HBM allocation"）
- 2026-08-04｜CEO Lisa Su｜risk：CEO 稱中型模型工作負載對記憶體的效益較小時會調整記憶體配置（原話："we would address the memory footprint"）
- 2026-08-04｜CEO Lisa Su｜risk：管理層預期下半年 PC 市場偏軟，因記憶體及零組件成本上升（原話："we are planning for a softer PC market"）
- 2026-08-04｜CEO Lisa Su｜risk：CEO 稱 PC 市場走向取決於零組件成本（原話："The market itself will depend a bit on some of the"）
- 2026-08-04｜CEO Lisa Su｜risk：CEO 稱 2027 達標區間取決於產能能否及時到位（原話："the range will depend on the ability to bring on more"）
- 2026-08-04｜CEO Lisa Su｜risk：遊戲部門 Q2 營收年減 31%（半客製降）（原話："revenue declined 31% year-over-year to $779 million"）
- 2026-08-04｜CFO Jean Hu｜capital_allocation：Q2 營業費用年增 40%，管理層稱因持續投入 AI 研發（原話："Operating expenses were $3.4 billion, an increase of 40%"）
- 2026-08-04｜CFO Jean Hu｜capital_allocation：Q2 來自繼續營業的現金流 24 億美元（原話："we generated $2.4 billion in cash from continuing operations"）
- 2026-08-04｜CFO Jean Hu｜capital_allocation：存貨季增至約 85 億美元，管理層稱為支應資料中心需求（原話："Inventory increased sequentially to approximately $8.5"）

### 問答異常語氣（迴避／改口／保留）
- AMD_Q2_2026_Earnings_Call_20260804.md｜問：UBS Arcuri：Q3 資料中心季增中 CPU 與 GPU 哪個美元增量較大；H2 年增 80% 似乎暗示 Q4 伺服器 CPU 成長有限｜答法：CEO 未給 CPU／GPU 美元拆分，只說兩者 Q3、Q4 都會成長、Q4 高於 Q3，未回應分析師的數學疑問
- AMD_Q2_2026_Earnings_Call_20260804.md｜問：BofA Arya：2027 年 AMD 看得到多少 GW、每 GW 營收是否約 150 億美元以上｜答法：CEO 未確認 GW 數或 150 億美元每 GW，改談伺服器與資料中心 2027 年成長百分比，僅說每 GW『雙位數十億美元』
- AMD_Q2_2026_Earnings_Call_20260804.md｜問：BofA Arya：Helios 多 50% HBM 是否使 AMD 更暴露於記憶體成本通膨、如何維持毛利率｜答法：CEO 談 HBM 配置能見度與 TCO 優勢，未回應毛利率影響，也未給數字；提到必要時調整記憶體配置
- AMD_Q2_2026_Earnings_Call_20260804.md｜問：TD Cowen Buchalter：Helios 前一兩季毛利率相對後期如何，會否隨放量改善｜答法：CEO 只談良率隨放量改善，未提供毛利率數字或軌跡
- AMD_Q2_2026_Earnings_Call_20260804.md｜問：Bernstein Rasgon：新聞稿說資料中心下半年加速，但 Q3 指引成長在 80% 左右低於 Q2 的 107%，如何解讀｜答法：CFO 將『加速』界定為下半年對上半年比較，未直接回答 Q3 是否低於 Q2 年增率
- AMD_Q2_2026_Earnings_Call_20260804.md｜問：Cantor Muse：Instinct 2027 毛利率起點與年底落點｜答法：CFO 稱組合會逐季不同、整體有抵銷，未給 Instinct 毛利率數字，表示之後再提供 2027 指引
- AMD_Q2_2026_Earnings_Call_20260804.md｜問：Cantor Muse：2027 Instinct 收入約 300 億美元的隱含推算及上下半年節奏｜答法：CEO 未給數字，只說該數字『probably too low』、資料中心 AI 成長應視為遠高於 100%

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
{"date":"20260923","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回落到 490 美元以下（約 FY2027 共識 EPS 的 31 倍）且 FY2027 共識不低於 15 美元，才恢復分批加碼","irr_base_pct":6.7,"ev5y_pct":30.9,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":1.8,"ev5y_pct":30.9,"irr_base_pct":6.7,"max_dd_pct":-72,"bull_5y_price":1500.0,"bear_5y_price":280.0,"p_bull_pct":22,"p_bear_pct":32,"rearm_trigger":"股價回落到 490 美元以下（約 FY2027 共識 EPS 的 31 倍）且 FY2027 共識不低於 15 美元，才恢復分批加碼","price_at_dd":623.77,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMD_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
