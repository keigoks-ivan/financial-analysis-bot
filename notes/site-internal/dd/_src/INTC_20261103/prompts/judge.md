你是 stock-analyst **v20 判斷 agent**，標的 INTC（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"INTC","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INTC_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INTC_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":16.513,"period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results"},"note":"未查得"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益率","value":19.6,"period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results"},"note":"未查得"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益率","value":15.3,"period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results"},"note":"未查得"},{"id":"f_kpi5_q4_fy2026","label":"Q4 FY2026 指引","value":"營收 $15.0–16.0B；non-GAAP 毛利率 38.0%（GAAP 37.1%）；non-GAAP EPS $0.25（GAAP $0.10）","period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results"},"note":"未查得"},{"id":"f_kpi6_dcai_foundry_ccpg","label":"分部營收 DCAI／Foundry／CCPG","value":"DCAI $7.3B（YoY +78%）；Foundry $6.7B（+58%）；CCPG $8.1B（-5%）","period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results"},"note":"未查得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_intc_gross_margin_pct","label":"INTC 毛利率","value":38.73,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INTC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_intc_operating_margin_pct","label":"INTC 營業利益率","value":7.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INTC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_intc_fcf_margin_pct","label":"INTC FCF 利潤率","value":6.25,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INTC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amd_gross_margin_pct","label":"AMD 毛利率","value":53.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amd_operating_margin_pct","label":"AMD 營業利益率","value":15.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amd_fcf_margin_pct","label":"AMD FCF 利潤率","value":20.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2330_tw_gross_margin_pct","label":"2330.TW 毛利率","value":65.85,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_2330_tw_operating_margin_pct","label":"2330.TW 營業利益率","value":57.98,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_2330_tw_fcf_margin_pct","label":"2330.TW FCF 利潤率","value":29.58,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_005930_ks_gross_margin_pct","label":"005930.KS 毛利率","value":57.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_operating_margin_pct","label":"005930.KS 營業利益率","value":36.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_fcf_margin_pct","label":"005930.KS FCF 利潤率","value":28.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_gfs_gross_margin_pct","label":"GFS 毛利率","value":27.14,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GFS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_gfs_operating_margin_pct","label":"GFS 營業利益率","value":11.59,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GFS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_gfs_fcf_margin_pct","label":"GFS FCF 利潤率","value":11.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GFS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_adjusted_fcf","label":"調整後自由現金流（Adjusted FCF）","value":1.639,"period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results"},"note":"未查得"},{"id":"f_kpi4_sbc_non_gaap","label":"SBC 占 Non-GAAP 營業利益","value":18.1,"period":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results（SBC $586M；占比為自算 586/3,234；占營收 3.5%）"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":62.9,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-34.32,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":23.99,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-3.9,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.54 → 1.48）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-3.67,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.18 → 2.1）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.2 → 3.2）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.48,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.1,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.2,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-2.63,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 1.52 → 1.48（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.58,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.52,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":42.5,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 1.48，分子＝快照價 62.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-3871.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 50134.0、現金 54005.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":5315.0,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":330415.91,"period":"2026-11-03","unit":"USD m","basis":"市值 334286.91 ＋ 淨負債 -3871.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":61848.8,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（45 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":69350.92,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（46 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":5.34,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 61.26 / W52 77.25 / W104 50.62 / W250 40.7 / W250 13週斜率 1.06%"},{"id":"f_ma_w52","label":"52 週均線","value":77.25,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":50.62,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":40.7,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.06,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Mercury Research Q2 2026: Intel x86 share fell below 70% (~69.3%) for the first time since 1995; AMD record ~30.7%; AMD server share 34.5% ex-IoT (Intel 65.5%).","source":"Mercury Research via CPU Market Share Q2 2026 (basic-tutorials.com)","url":"https://basic-tutorials.com/news/cpu-market-share-q2-2026-amd-breaks-the-30-percent-mark-intel-loses-ground-across-the-board/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Q1 2026: AMD EPYC took 46.2% of server x86 revenue; Intel server unit share 66.8% vs 72.8% a year earlier; ARM server unit share 17.7% vs 11.5% (UBS).","source":"Tom's Hardware: AMD reaches 46% of server x86 CPU revenue","url":"https://www.tomshardware.com/pc-components/cpus/amd-reaches-46-percent-of-server-x86-cpu-revenue-intel-still-controls-70-percent-of-the-consumer-pc-market-share","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Tesla is the only officially confirmed 14A customer (TeraFab, April 2026); other reported foundry wins (AMD, NVIDIA, Marvell, Microsoft, Micron, OpenAI) are unconfirmed per KeyBanc/FactSet-cited report; 14A risk production 2028, volume 2029.","source":"WCCFtech: Intel 14A wins Tesla, major customers","url":"https://wccftech.com/intel-foundry-snags-amd-nvidia-openai-as-design-wins-on-18a-14a-nodes/","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261103","affects":["thesis.H","triggers"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"ByteDance 報導正開發自家 Arm 與 RISC-V 伺服器 CPU，理由含 Intel/AMD 漲價與交期變長（早期階段）","source":"aiweekly.co - ByteDance designs custom Arm and RISC-V server CPUs","url":"https://aiweekly.co/alerts/bytedance-designs-custom-arm-and-risc-v-server-cpus","excerpt":"ByteDance designs custom Arm and RISC-V server CPUs By Alexis Dufresne · Published May 29, 2026 at 06:35 UTC · Updated May 29, 2026 at 06:40 UTC ByteDance Chips China AI china-ai semiconductors chip-independence Key insights Intel and AMD raised server CPU prices 10-35% quarter-on-quarter while lead times for Chinese buyers stretched to six months.","as_of":"2026-05-29","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"Counterpoint：NVIDIA 評估以 Intel Foundry 為部分產品的 second source（最早 2029）；Apple 可能尋求第二來源，Intel 14A-E 為潛在夥伴（分析師推測，非確認合約）","source":"Counterpoint Research - Foundry Monthly Intelligence Report February 2026","url":"https://counterpointresearch.com/jp/reports/Foundry-Monthly-Intelligence-Report-February-2026","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"INTC 三大客戶合計占 2025 淨營收 43%（2024 為 45%、2023 為 40%）；預期少數客戶仍將占大宗。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm","excerpt":"Collectively, our three largest customers accounted for 43% of our net revenue in 2025, 45% of our net revenue in 2024 and 40% of our net revenue in 2023.","as_of":"2026-01-23","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"三大客戶應收帳款占比 47%（2025-12-27 與 2024-12-28），公司認為不構成重大信用風險。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm","excerpt":"We believe the net accounts receivable balances from our three largest customers (47% as of December 27, 2025 and December 28, 2024) do not represent a significant credit risk, based on cash flow forecasts, balance sheet analysis and past collection experience.","as_of":"2026-01-23","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Intel Q3 2026 10-Q：資料中心產品需求維持強勁（AI 基建投資），公司預期強勁需求延續到 2026 Q4 及以後。","source":"Intel Form 10-Q (period ended 2026-09-26), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0000050863/000005086326000191/intc-20260926.htm","excerpt":"In Q3 2026 and YTD 2026, demand for our data center products remained strong amid continued investments in AI infrastructure. We expect strong demand to continue into Q4 2026 and beyond.","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Intel Q2 2026 10-Q：市場需求超過可供應產品，受自家晶圓廠產能及產業供給限制所致（供給為瓶頸）。","source":"Intel Form 10-Q (period ended 2026-06-27), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0000050863/000005086326000157/intc-20260627.htm","excerpt":"market demand exceeded our available product supply due to capacity constraints at our factories and industry-wide supply constraints","as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Wolfe Research 的 Chris Caso 認為半導體供過於求最早 2028 年才可能出現，因新廠需數年建置。","source":"24/7 Wall St., Top Chip Analyst: Semiconductor Oversupply Is Nearly Impossible Before 2028","url":"https://247wallst.com/investing/2026/07/30/top-chip-analyst-semiconductor-oversupply-is-nearly-impossible-before-2028-why-hes-bullish-on-memory/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"TrendForce 預估 NAND 2026 供給短缺 4–5%，2027 下半年供給位元成長將超過需求成長。","source":"thefpsreview, New Report Suggests That NAND Supply Growth Could Once Again Exceed Demand in 2027（引 TrendForce）","url":"https://www.thefpsreview.com/2026/07/21/new-report-suggests-that-nand-supply-growth-could-once-again-exceed-demand-in-2027/","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Gartner：2Q26 晶片庫存指數進入中度短缺，預期持續至 2027。","source":"Gartner Insights Abstract","url":"https://www.gartner.com/en/documents/8208429","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261103","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Trefis：PC 市場 2026 預期下滑低雙位數 %，Intel 產能轉向資料中心 CPU。","source":"Trefis, Intel Stock's Real Opportunity Is Demand It Cannot Yet Ship","url":"https://www.trefis.com/articles/611546/intel-stocks-real-opportunity-is-demand-it-cannot-yet-ship/2026-08-14","excerpt":"The obvious objection is the PC market, which Intel expects to be down low double-digit percent for calendar 2026. For a manufacturer already sold out, that is less of a headwind than it looks. Client and server parts come off the same factory network, and management has said it will pivot as much production as it can toward data center CPUs.","as_of":"2026-08-14","retrieved_at":"20261103","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"MLex 報導（2026-03-03）：Intel 就歐盟長期處理器案再度向歐盟最高法院上訴；去年12月判決已將罰款由3.76億歐元降至2.37億歐元，歐盟執委會未再挑戰該判決（付費牆，未讀全文）。","source":"MLex 報導（搜尋摘要轉述）","url":"https://www.mlex.com/mlex/articles/2448033","excerpt":null,"as_of":"2026-03-03","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2026年3月美國跨黨派議員對 Intel 測試 ACM Research 晶片設備（該公司與中國及受制裁實體有關）提出國安疑慮；Intel 稱僅為測試用途、尚未量產（二手轉述）。","source":"TradingKey, market movers INTC 2026-03-06","url":"https://www.tradingkey.com/news/stocks/261656031-market-movers-intc-20260306","excerpt":null,"as_of":"2026-03-06","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"三次搜尋未發現2026年 DOJ／FTC 對 Intel 的新反壟斷調查或拆分案；搜尋到的 FTC 相關資料均屬2010年前後舊案。中國對 Intel 反壟斷調查僅有2025-02傳聞，未見確認展開。","source":"WebSearch 三次查詢結果彙總","url":null,"excerpt":null,"as_of":"2026-03-06","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-01-14 公告（No. 11002）對特定先進晶片課 25% Section 232 關稅，2026-01-15 生效，範圍限於達技術門檻之晶片，美國資料中心、研發、消費電子等有豁免；搜尋結果未見 Intel 公司自述財務影響。","source":"Thomson Reuters OneSource, Trump administration imposes tariffs on advanced AI chips under Section 232 authority","url":"https://www.thomsonreuters.com/en-us/help/onesource-global-trade/regulatory-insights/2026/january-15th/trump-administration-imposes-tariffs-on-advanced-a","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"BIS 撤銷 Intel、Samsung、SK Hynix 向中國晶圓廠出口美製設備的授權，自 2026-01-01 起不得再供應新機台。","source":"heise, Intel, Samsung, SK Hynix: No more US exports for Chinese fabs","url":"https://heise.de/-10626911","excerpt":null,"as_of":"2025-08-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Intel 於 2025-04 告知中國客戶部分 AI 晶片（Gaudi 等）出口需許可證；搜尋結果未說明 2026 年是否仍有效。","source":"silicon.co.uk, Intel Tells Chinese Clients Some AI Chips To Require Licence","url":"https://www.silicon.co.uk/cloud/ai/intel-china-ai-609032","excerpt":null,"as_of":"2025-04-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Intel 10-K/ARS 揭露：中國與台灣緊張升高、戰事風險上升，且許多產品依賴台灣供應商提供關鍵零組件（含各類 compute die）","source":"Intel FY2025 Form 10-K / ARS (SEC)","url":"https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm","excerpt":null,"as_of":"2026-01-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Intel 2026 年 10-Q 風險因素新增中東衝突、俄烏戰爭，以及含外部晶圓代工的複雜全球供應鏈","source":"Intel Form 10-Q (quarter ended 2026-09-26, SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000050863/000005086326000191/intc-20260926.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Intel 10-K：美中緊張導致關稅與出口管制，中國為最大市場之一；2025 年美國管制擴大導致額外銷售減少","source":"Intel FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm","excerpt":null,"as_of":"2026-01-30","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Moody's：先進製造集中於少數地區與少數公司，上游特化化學品與基板供應商冗餘低","source":"Moody's, Semiconductors in 2026: why supply chains are a major bottleneck","url":"https://www.moodys.com/web/en/us/insights/corporations/semiconductors-in-2026-why-supply-chains-are-a-major-bottleneck.html","excerpt":"Semiconductor production is highly specialized, with advanced manufacturing concentrated in a handful of regions and dominated by a small group of firms.","as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Intel Q3 2026：DCAI 營收年增 78% 至 73 億美元（15 年來最強），營業利益約 30 億美元；CCPG 營收年減 5% 至 81 億美元，仍營業虧損；總營收 165 億美元年增 21%；Q4 指引 150–160 億美元；CFO 稱 PC 市場低迷至少延續到 2027 上半年","source":"servethehome / thestar 等二手報導 Intel Q3 2026 財報","url":"https://www.servethehome.com/intel-q3-2026-earnings-data-center-foundry-client/","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"報導稱 Intel 計畫 2026-10 約 10% 調漲 PC CPU 價格（自 2025 底第三次）；Q2 2026 伺服器 CPU ASP 年增約 48%；DigiTimes 稱目的為毛利而非市佔；Mercury 2025Q4 x86 出貨 Intel 70.8%／AMD 29.2%；AMD 2026Q1 伺服器市佔約 33%（+6pp）；PC 出貨預估 2027 由 2.6 億降至約 2.5 億台。部分為未經 Intel 證實之報導，且伺服器市佔來自 BofA 分析","source":"cryptobriefing / yicaiglobal / aiweekly 等二手報導","url":"https://www2.yicaiglobal.com/news/intel-hikes-cpu-prices-adding-to-pc-industrys-cost-pressures","excerpt":null,"as_of":"2026-10-05","retrieved_at":"20261103","affects":["moat_trend","valuation","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"WSTS 2026 春季預測：2026 全球半導體約 1.51 兆美元，2027 再成長約 27% 至約 1.9 兆美元，主要由記憶體驅動（2026 記憶體 8039 億美元）；H1 2026 市場 7020 億美元年增 102%（WSTS Q2 release）","source":"WSTS Spring 2026 forecast / WSTS Q2 Release 2026-08-06","url":"https://telecomlead.com/semiconductor/wsts-raises-semiconductor-forecast-market-to-reach-1-51-trillion-in-2026-grow-to-1-9-trillion-in-2027-126102?noamp=mobile","excerpt":null,"as_of":"2026-06-02","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"WSTS Q2 2026 release 半導體市場數據","source":"WSTS Q2 Release 2026-08-06","url":"https://www.wsts.org/esraCMS/extension/media/f/WST/7734/WSTS-Q2-Release-2026-08-06.pdf","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"NoobFeed 報導（引 GF Securities 分析師預期）稱 Nvidia 以 Arm 架構 Vera CPU 切入企業 CPU，直接挑戰 Intel/AMD 的 x86；若成為次世代 AI 系統首選 CPU 夥伴，x86 長期壓力將加速。屬部落格級來源。","source":"NoobFeed: NVIDIA Vera CPUs Signal a Massive Threat to Intel and AMD's x86 Dominance","url":"https://www.noobfeed.com/hardware/nvidia-vera-cpus-threat-intel-amd-x86","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Borecraft 報導：Intel 14A 後續路線取決於能否取得外部晶圓代工客戶；據稱 Intel 曾告知投資人，若無重要外部客戶與里程碑達成，可能暫停或終止 14A 及後續先進節點；14A 首次量產導入 High-NA EUV。","source":"Borecraft: Intel's post-18A roadmap hangs on landing 14A foundry customers","url":"https://borecraft.com/2026/06/17/intels-post-18a-roadmap-hangs-on-landing-14a-foundry-customers/","excerpt":null,"as_of":"2026-06-17","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Intel FY2026 年報信：18A 良率持續改善；客戶預計 2026 下半年至 2027 上半年做 14A 決定。","source":"Intel Form ARS FY2026","url":"https://www.sec.gov/Archives/edgar/data/50863/000005086326000060/intc014890-arsa.pdf","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261103","affects":["triggers","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Intel 14A 改為先取得客戶承諾再擴產（脫離「蓋廠客戶自然來」模式），客戶決定落在 2026 下半年至 2027 上半年","source":"TechNews 台灣 2026-01-27 Intel 14A 能否贏得大客戶訂單","url":"https://technews.tw/2026/01/27/whether-intel-14a-can-win-orders-from-major-customers-2026-will-be-a-pivotal-year-for-intels-transformation/","excerpt":null,"as_of":"2026-01-27","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 7/27：49 家券商共識為 Hold（29 Hold、15 Buy、2 Strong Buy、3 Sell），12 個月平均目標價約 $107.67；Q2 EPS 0.42 vs 共識 0.21，營收 $16.13B vs $14.43B。","source":"MarketBeat, Intel Corporation (NASDAQ:INTC) Given Consensus Rating of Hold by Analysts","url":"https://www.marketbeat.com/instant-alerts/intel-corporation-nasdaqintc-given-consensus-rating-of-hold-by-analysts-2026-07-27/","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 指引（7/23 發布）：EPS 0.38 vs 共識約 0.37；營收指引 $15.8B–$16.8B vs 共識 $16.40B（Benzinga 日文頁，來源間數字不完全一致）。","source":"Benzinga INTC earnings-forecasts","url":"https://www.benzinga.com/quote/INTC/earnings-forecasts","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布因來源與日期而異：Tickflow（資料 8/1）54 位分析師 Hold、均值 $91.80；Walnut（7月）41 位、均值 $115.27、中位 $110、區間 $74–$200；TipRanks 財報前均值 $113.72。","source":"Tickflow / Walnut / TipRanks (via search summary)","url":"https://www.tickflow.io/stock/INTC/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026年7月多家調升目標價：KeyBanc $110→$155、UBS $83→$121、Susquehanna $80→$115、BofA $160、Baird $125（Neutral）、Citi Buy $130；Rosenblatt Sell $65。","source":"Search summary (daytraders.com / Walnut / MarketBeat)","url":"https://daytraders.com/news/2026/07/23/intel-earnings-are-imminent-these-most-accurate-analysts-revise-forecasts-ahead-of-earnings-call-7","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"報導稱 Intel 2026-10-29 提供 Q4 指引營收 $15–16B、non-GAAP EPS 0.25、毛利率 38%，低於分析師預期約 $17.07B／0.43，盤後股價大跌（未核實）。","source":"tech-insider.org, Intel plunges 25% Q4 guidance $15-16 billion PC slump 2026","url":"https://tech-insider.org/intel-plunges-25-q4-guidance-15-16-billion-pc-slump-2026/","excerpt":"Intel guided to US$15 billion to US$16 billion in fourth-quarter revenue and US$0.25 per share in adjusted earnings. Analysts had pencilled in roughly US$17.1 billion and US$0.43.","as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-04-08 Intel 以 142 億美元向 Apollo 基金買回 Fab 34（愛爾蘭）合資 49% 權益，資金為現金加 65 億美元過橋貸款，買回後持有 100%。","source":"SEC EDGAR 8-K Item 8.01（2026-04-08）","url":"https://www.sec.gov/Archives/edgar/data/50863/000005086326000072/intc-20260408.htm","excerpt":"On April 8, 2026, Intel Corporation (“Intel”) repurchased from Apollo-managed funds and affiliates their 49% equity interest in the parties’ joint venture related to Intel’s Fab 34 in Ireland. The $14.2 billion repurchase price was financed by Intel with cash on hand and a bridge loan of $6.5 billion, which Intel intends to refinance, subject to market conditions.","as_of":"2026-04-08","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露：2024 年 5 月於北加州聯邦法院提起的證券集體訴訟（涉及分部報告與內部代工模式），2025 年 7 月第二次修正訴狀被駁回並判被告勝訴，原告已上訴。","source":"SEC EDGAR 10-K FY2025 財報附註（申報 2026-01-23）","url":"https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm","excerpt":"The court granted plaintiffs leave to amend, but in July 2025 dismissed plaintiffs' second amended complaint and entered judgment in defendants' favor, again finding that plaintiffs failed to plead any false or misleading statements. Plaintiffs have appealed.","as_of":"2026-01-23","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"Intel 於 2026-10 簽署definitive agreement 收購 Classiq Technologies 100%（金額標題不一致）","source":"Newsquawk headline","url":"https://www.newsquawk.com/headlines/intel-intc-says-it-entered-into-a-definitive-agreement-in-october-2026-to-acquire-100-of-classiq-technologies-for-approximately-usd-19bln-according-to-a-filing","excerpt":"Intel (INTC) says it entered into a definitive agreement in October 2026 to acquire 100% of Classiq Technologies for approximately USD 1.9bln, according to a filing","as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"turnaround_catalyst_timeline#0","axis":"turnaround_catalyst_timeline","section":"coverage","direction":"0","claim":"Q3 2026 10-Q：2025 重整計畫大部分已於 2025 完成、餘下預計 2026 完成；2024 計畫預計 2026 完成；應計重整餘額 $182M（2026-09-26）；前九個月商譽減損 $3.9B","source":"Intel Form 10-Q (period ended 2026-09-26)","url":"https://www.sec.gov/Archives/edgar/data/0000050863/000005086326000191/intc-20260926.htm","excerpt":"in YTD 2026, primarily relating to the 2025 Restructuring Plan, compared to $146 million in Q3 2025 and $1.8 billion in YTD 2025. Charges in Q3 2025 and YTD 2025 primarily related to the 2025 Restructuring Plan, with the remaining charges relating to the 2024 Restructuring Plan. Asset impairment charges in YTD 2026 included non-cash goodwill impairment charges of $3.9 billion.","as_of":"2026-10-30","retrieved_at":"20261103","affects":["triggers","thesis.H"],"status":"ok"},{"id":"turnaround_catalyst_timeline#1","axis":"turnaround_catalyst_timeline","section":"coverage","direction":"+","claim":"Altera 51% 股權出售給 Silver Lake 已於 9/12 完成，稅前利得 $5.6B","source":"Intel Form ARS FY2026","url":"https://www.sec.gov/Archives/edgar/data/50863/000005086326000060/intc014890-arsa.pdf","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"turnaround_catalyst_timeline#2","axis":"turnaround_catalyst_timeline","section":"coverage","direction":"0","claim":"Intel 規劃發債並動用現金回購 Apollo 持有的 Fab 34 49% 股權（約 $14.2B，新債約 $6.5B）","source":"Bloomberg Law: Intel Plans Multi-Billion Dollar Bond Sale Tied to Apollo Deal","url":"https://news.bloomberglaw.com/private-equity/intel-plans-multi-billion-dollar-bond-sale-tied-to-apollo-deal","excerpt":"Intel Plans Multi-Billion Dollar Bond Sale Tied to Apollo Deal April 24, 2026, 9:23 PM UTC Brian Smith Bloomberg News Kevin Kingsbury Bloomberg Editorial","as_of":"2026-04-24","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"turnaround_liquidation_floor#0","axis":"turnaround_liquidation_floor","section":"coverage","direction":"-","claim":"Intel Q3 2026 10-Q：2026 年前九個月資產減損為 39 億美元非現金商譽減損（Q1 認列，與 Mobileye 相關）","source":"SEC Form 10-Q FY2026 (period ending 2026-09-26)","url":"https://www.sec.gov/Archives/edgar/data/0000050863/000005086326000191/intc-20260926.htm","excerpt":"Asset impairment charges incurred in the first nine months of 2026 were related to non-cash goodwill impairment charges of $ 3.9billion.","as_of":"2026-09-26","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"turnaround_liquidation_floor#1","axis":"turnaround_liquidation_floor","section":"coverage","direction":"0","claim":"FY2025 年報資產負債表：總資產 2,114 億美元（含商譽 239 億美元），長期債約 441 億美元；商譽仍佔帳面資產一定比重","source":"Intel Form ARS FY2025 balance sheet (Dec 27, 2025)","url":"https://www.sec.gov/Archives/edgar/data/50863/000005086326000060/intc014890-arsa.pdf","excerpt":"Total assets $ 211,429 $ 196,485","as_of":"2025-12-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"turnaround_liquidation_floor#2","axis":"turnaround_liquidation_floor","section":"coverage","direction":"0","claim":"Q3 2026 10-Q：稅務應收款 74 億美元（2025 年底 76 億）；Q2 10-Q 指因美國境內估值備抵，2026 上半年虧損無法取得稅務利益","source":"SEC Form 10-Q FY2026 Q3 / Q2","url":"https://www.sec.gov/Archives/edgar/data/0000050863/000005086326000191/intc-20260926.htm","excerpt":"Additionally, our Consolidated Condensed Balance Sheets as of September 26, 2026 and December 27, 2025 contain certain tax receivables of $ 7.4billion and $ 7.6billion.","as_of":"2026-09-26","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-04-08 Intel 以 142 億美元買回 Apollo 持有的 Fab 34 合資 49% 權益（回購少數股權，非外部併購）。","source":"SEC EDGAR 8-K Item 8.01（2026-04-08）","url":"https://www.sec.gov/Archives/edgar/data/50863/000005086326000072/intc-20260408.htm","excerpt":"The $14.2 billion repurchase price was financed by Intel with cash on hand and a bridge loan of $6.5 billion, which Intel intends to refinance, subject to market conditions. Intel owns 100% of the joint venture following the repurchase.","as_of":"2026-04-08","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"證券集體訴訟（2024 年 5 月，分部報告／內部代工模式）已被駁回並判被告勝訴，原告上訴中。","source":"SEC EDGAR 10-K FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm","excerpt":"In March 2025, the court dismissed plaintiffs' amended consolidated complaint, finding that plaintiffs failed to plead any false or misleading statements by defendants. The court granted plaintiffs leave to amend, but in July 2025 dismissed plaintiffs' second amended complaint and entered judgment in defendants' favor, again finding that plaintiffs failed to plead any false or misleading statements. Plaintiffs have appealed.","as_of":"2026-01-23","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Spectre／Meltdown／Downfall 消費者集體訴訟在美加仍在進行。","source":"SEC EDGAR 10-K FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm","excerpt":"Consumer class action lawsuits are pending against us in the U.S. and Canada. The plaintiffs, who purport to represent various classes of purchasers of our products, generally claim to have been harmed by our actions and/or omissions in connection with Spectre, Meltdown, and other variants of this class of security vulnerabilities that have been identified since 2018","as_of":"2026-01-23","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"INTC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.73,"operating_margin_pct":7.95,"fcf_margin_pct":6.25,"rd_intensity_pct":22.97},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INTC","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"AMD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":53.2,"operating_margin_pct":15.71,"fcf_margin_pct":20.34,"rd_intensity_pct":22.74},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"2330.TW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":65.85,"operating_margin_pct":57.98,"fcf_margin_pct":29.58,"rd_intensity_pct":5.96},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"005930.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.48,"operating_margin_pct":36.88,"fcf_margin_pct":28.95,"rd_intensity_pct":9.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"GFS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":27.14,"operating_margin_pct":11.59,"fcf_margin_pct":11.47,"rd_intensity_pct":8.11},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GFS","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"INTC"},"financial_history":{"ticker":"INTC","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":63054000000.0,"revenue_yoy_pct":null,"gross_margin_pct":42.61,"operating_margin_pct":3.7,"net_income":8014000000.0,"diluted_eps":1.94,"free_cash_flow":-9411000000.0,"fcf_margin_pct":-14.93,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":54228000000.0,"revenue_yoy_pct":-14.0,"gross_margin_pct":40.04,"operating_margin_pct":0.06,"net_income":1689000000.0,"diluted_eps":0.4,"free_cash_flow":-14279000000.0,"fcf_margin_pct":-26.33,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":53101000000.0,"revenue_yoy_pct":-2.08,"gross_margin_pct":32.66,"operating_margin_pct":-8.87,"net_income":-18756000000.0,"diluted_eps":-4.38,"free_cash_flow":-15656000000.0,"fcf_margin_pct":-29.48,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":52853000000.0,"revenue_yoy_pct":-0.47,"gross_margin_pct":34.77,"operating_margin_pct":-0.04,"net_income":-267000000.0,"diluted_eps":-0.06,"free_cash_flow":-4949000000.0,"fcf_margin_pct":-9.36,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/INTC/INTC_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Intel Corporation** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Thank you for standing by, and welcome to the Intel Corporation's Third Quarter 2026 Earnings Conference Call. [Operator Instructions] As a reminder, today's program is being recorded.
And now I'd like to introduce your host for today's program, Mr. John Pitzer, Corporate Vice President of Investor Relations. Please go ahead, sir.

**John Pitzer** (Executives):
Thank you, Jonathan, and good afternoon to everyone joining us today. By now, you should have received a copy of the Q3 earnings release and presentation. Both are available on our Investor Relations website, intc.com. For those joining us online today, the presentation is also available in our webcast window.
I'm joined today by our CEO, Lip-Bu Tan; and our CFO, Dave Zinsner. Lip-Bu will open on comments on third quarter results and progress on our strategic priorities. Dave will then discuss overall financial results, including fourth quarter guidance, before we transition to answer your questions.
Before we begin, please note that today's presentation does contain forward-looking statements based on the environment as we currently see it. As such, they are subject to various risks and uncertainties. It also contains references to non-GAAP financial measures that we believe provide useful information to our investors. Our earnings release, most recent annual report on Form 10-K and other filings with the SEC provide more information on specific risk factors that could cause the actual results to differ materially from our expectations. They also provide additional information on our non-GAAP financial measures, including reconciliation, where appropriate, to our corresponding GAAP financial measures.
With that, let me turn it over to Lip-Bu.

**Lip-Bu Tan** (Executives):
Good afternoon, and thank you for joining us. The demand environment in Q3 was more balanced than previous quarters. Strong momentum in DCAI drove upside and enabled the strongest revenue growth for the segment in 15 years. This was partially offset by weakness in CCPG driven by the industry-wide impacts from higher memory prices and limited IT budgets.
The industry continues to navigate one of the most significant supply shortages in the history, driven by the unprecedented demand for Super Intelligence. Against this backdrop, I am pleased by the progress we made growing our server supply in Q3. I'm mindful about the ongoing challenges we face in the future quarters to keep pace with the server demand.
The successful completion of our equity offering in August provided us with the necessary financial resources to capture the growth ahead. I'm very pleased to add new sovereign funds and long-term growth investors in addition to our existing shareholders. We are deploying this capital quickly and prudently. We expect CapEx and purchase commitments for key components to increase significantly over the next several quarters. I want to thank our substrate, memory, foundry, equipment suppliers for their strong partnership and collaboration as we work together to expand supply and support growing demand.
Turning to business units. First, DCAI. Within our server business, we are making steady progress on our road map. Granite Rapids on Intel 3 has become one of the fastest ramping server products. Clearwater Forest, our first Intel 18A server product, is shipping for revenue, and demand for 2027 is significant, especially in CPU-dense agentic rack-scale infrastructure.
Diamond Rapids, our first Intel 18A-P server product is sampling and on track to ramp in 2027, with strong interest for inference and agentic workloads. We were pleased to recently announce an agreement with Oracle Cloud Infrastructure to deploy our latest generation CPUs to support their AI build-out.
I also want to acknowledge headwinds limiting our progress to meet this extremely high AI-driven demand. First, Intel 3 yield and cycle time continue to improve, but I am demanding significant execution from the team. Second, even as our Intel 3 wafer output ramps quickly, an industry-wide shortage of advanced organic substrates for our EMIB packaging is also impacting our ability to scale output.
Finally, early this month, an unfortunate and tragic accident led to an extended shutdown in our Israel factory. While the teams have worked quickly to address the situation, it will impact our Q4 10-nanometer server shipments.
Purpose-built silicon remains our fastest-growing business segment, tripling over the last 3 years, and poised to triple again over the next few years. We see further growth opportunity with both existing and new potential customers, including AI labs, and expanding our IP portfolio to meet the needs of a wider array of customers.
Lastly, we recently unveiled our Crescent Island inference-optimized GPU. Early feedback is encouraging, performance is tracking well. This is a new market for us, and it will take time to scale, but customer engagements are progressing towards firm commitments.
Turning to our client business. In recent weeks, our customers began signaling a PC slowdown based on the memory prices and availability. Year-to-date system endpoint prices have increased significantly placing additional pressure on already limited IT budgets. The pace of this PC correction has accelerated over the last 2 months, as our OEM partners are aggressively managing inventory to match the softer sell-through. We expect the current environment to persist until memory availability and prices begin to normalize.
While the next few quarters will be challenging for the PC market, our road map continues to strengthen and our long-term outlook remains positive. We have successfully ramped Panther Lake on Intel 18A and demand for the Wildcat Lake is outstripping supply. Nova Lake, our first Intel 18A-P client product, is tracking ahead of schedule, with design wins expected to be twice those of Panther Lake at launch. We look forward to sharing more at CES in January. As the market normalizes, we expect this portfolio drives meaningful share gains.
Intel Foundry execution continues to improve consistently. During the quarter, Intel 3 and Intel 18A yields both increased again, with Intel 18A improving at a double-digit rate. Wafer output on both nodes exceeded expectations. Intel 18A-P remains on track for launch by year-end across our internal product portfolio, and external customer engagement continues to build. We are engaged with a couple of highly strategic customers, and I'm increasingly confident that our Intel 18A-P will be an attractive node for external foundry customers.
Intel 14A also remains on track. In October, as committed, we released our industry standard 0.9 PDK to select customers. It is our highest-quality 0.9 PDK, meeting industry standard yield and performance criteria at release. As is standard practice in the foundry business, I have consistently maintained that we will not disclose customer details. That being said, I remain highly encouraged by the progress we are making with multiple potential customers on 14A.
On advanced packaging, we are pleased by the progress we are making with EMIB and EMIB-T for our internal products. Both continue to see significant external customer traction as well. We continue to improve on execution, working with our supply chain to secure the capacity to meet the needs of our advanced packaging customers. We are also seeing robust progress in the readiness of HBI, which is an enabler of 3D chip stacking for our upcoming server products.
Across our manufacturing network, additional capacity continues to come online. Intel 3 tool installation is progressing well in Ireland, as is the ramp of the 18A in both Oregon and Arizona, including Fab 62, our second high-volume 18A fab. In New Mexico and Malaysia, we are adding capacity to support strong customer ramps for advanced packaging next year.
In New Albany, Ohio, the team recently achieved important construction milestone with installation of the first major structural truss, and we continue to evaluate unique and highly differentiated opportunities to accelerate our Ohio build-out, and I hope to share more on this in the near future.
Looking to the future, I have always emphasized that rebuilding Intel is going to be a multiyear journey, and I remain firmly committed to making it happen. We are only 1.5 years into this journey. We have made enormous strides in these 18 months, including a dramatic resizing of our workforce, eliminating middle management and bureaucracy, streamlining our executive ranks and establishing an almost entirely new leadership team. We have installed once again an engineering-centric culture, streamlining our product portfolio and put in place a more competitive road map for Intel Products and Intel Foundry. We still have much more to do.
The resurgence in demand for CPU is a meaningful tailwind for us along our transformation journey. Increasingly, energy efficiency is becoming the most important metric for the AI infrastructure build-out. While GPUs are great at thinking tasks, deterministic CPUs are far more efficient at finding tasks. While a GPU reasoning query can run as high as multiple watt-hours of energy, a single CPU query could cost only joules of energy.
Applying even conservative estimates to the total number of digital agents, and agents serviced per CPU, it is easy to anticipate a massive dollar and unit TAM for CPUs over the coming 5 years. By our estimates, server CPU TAM, largely driven by agentic workloads, could increase as much as 5x from where it is today, from $40 billion to more than $200 billion over 5 years. This makes the opportunity for Intel enormous.
We're, of course, mindful of fierce competition underway as nearly every fabless company races to meet this unprecedented demand with their own offering. But Intel is uniquely positioned to benefit from this demand in 3 ways.
First, as a custodian of x86, the most widely deployed ISA in the world, we are doubling down on x86 innovation and have an exciting tick-tock road map of CPU innovations in the pipeline. In addition, for the first time, we are making fully modular, verified instances of our x86 CPUs, optimized for the custom workloads available to our customers.
Second, as 1 of the just 3 advanced node semiconductor foundries in the world, and the only one domiciled in the United States, we are well positioned to support not only our own demand, but also the demand of wider fabless industry. We are also open to building any CPUs at scale for our customers, fully agnostic to underlying ISA.
Third, as modern computing platforms increasingly become complex systems in a package, our leadership in advanced packaging offers highly differentiated solutions, especially to meet the requirements of the massive AI infrastructure build-out underway. This is why I remain optimistic on the opportunities ahead for Intel even as we have work to do.
Lastly, while we remain focused on executing against our near-term priorities, we cannot lose sight of what comes next. Intel has a deep portfolio of technology and IP that positions us to drive the next wave of computing. We continue to invest in breakthrough technologies, including silicon photonics, neuromorphic computing, advanced materials and quantum computing that we believe can unlock the important new opportunities over time. This week, we announced our intent to acquire Classiq, an Israel-based quantum software provider, moving our quantum efforts from foundational research towards commercialization. Classiq's overarching hardware agnostic software platform layer provides a gateway for more consumers to explore quantum computing and it is a wonderful complement to our already strong internal quantum hardware and software stacks and enables us to further extend our compute platform offering to include QPUs, in addition to CPUs, GPUs and ASICs. Postacquisition, Intel will become a full-stack revenue-generating quantum computing company.
In summary, while we did well in Q3, there is clearly more work to do. I'm disappointed that we were not able to meet strong customer demand in this quarter. We face near-term challenges, including manufacturing supply shortages, the unprecedented memory crunch, and the resulting softness in PC demand. But I remain confident in our path forward.
We need to address these challenges with urgency without losing sight of the massive opportunity in front of us. I want to thank our employees, partners and suppliers for their tireless efforts in this quarter.
With that, I will turn the call over to Dave for additional details.

**David Zinsner** (Executives):
Thank you, Lip-Bu. We delivered a strong quarter, exceeding our guidance for revenue, gross margin and earnings per share. This marks the eighth consecutive quarter of exceeding our financial expectations. Our Q3 results reinforce the essential role our server CPUs play in the build-out of Super Intelligence or AI infrastructure. Results also demonstrate our improving execution as we grow supply to capture the strong demand for AI compute.
Third quarter revenue was $16.5 billion, led by record year-over-year growth in DCAI. Strong execution across our factory network and external supply chain drove better-than-expected server CPU output. This strength was partially offset by weakness in client where industry-wide PC consumption is being impacted by memory shortages and limited IT budgets.
Third quarter non-GAAP gross margin was 44.1%, approximately 200 basis points higher than Q2 and our guidance. The sequential improvement was driven by improved costs on Intel 3 and Intel 18A and a more favorable product mix. 
Third quarter non-GAAP EPS was $0.52, compared with our guidance of $0.38. The upside was driven by higher revenue, stronger gross margin and disciplined spending, which together produced better-than-expected operating leverage.
Operating cash flow was $5.1 billion. We ended the quarter with approximately $54 billion in cash and short-term investments, in addition to $15 billion of borrowing capacity under our new, extended revolvers, up from $10 billion previously.
In early August, we further strengthened our balance sheet through a $23 billion equity offering. The incremental interest income associated with the offering contributed approximately $0.01 to Q3 EPS that was not contemplated in our original guidance.
Now moving to segment results. DCAI revenue was $7.3 billion, up 17% sequentially and nearly 80% year-over-year. Revenue was meaningfully ahead of our expectations as our factory network and external suppliers supported higher output. The work our teams have done to increase supply is having a tangible impact. Based on our current outlook, DCAI revenue is on track to finish 2026 nearly $10 billion above expectations entering the year.
Q3 growth was broad-based across hyperscale, enterprise and neo-cloud customers. We also continued to see strong momentum in purpose-built silicon with revenue increasing more than 50% sequentially and more than doubling year-over-year. Despite our progress to increase capacity, demand for DCAI products continues to meaningfully exceed available supply.
DCAI operating profit was $3 billion, representing 42% of revenue and increasing approximately $600 million sequentially. The improvement was driven by higher revenue and lower operating expenses. Granite Rapids is now the largest product family in our server portfolio as we continue to increase output from our Ireland facility.
Earlier this month, at the Open Compute Project Global Summit, we demonstrated select Clearwater Forest configurations that scale beyond 46,000 cores per rack at approximately 133 kilowatts of total rack power, delivering best-in-class performance per watt. We also introduced the Intel GPU D-series, formerly code-named Crescent Island, which is designed to improve the economics of sustained, memory-intensive AI inference. Customer interest in both product families is running ahead of our initial expectations.
CCPG revenue was $8.1 billion, down 9% sequentially and below our expectations. We previously noted that memory shortages could pressure the second half PC TAM. That pressure intensified during Q3, particularly late in the quarter, and resulted in a meaningful adjustment in customer purchasing patterns. Despite the near-term weakness, we saw several positive developments. Our AI PC revenue grew 35% year-over-year, even as total CCPG revenue declined 5%. Our client products on Intel 18A continued to ramp well. Wildcat Lake, our cost-optimized Intel 18A client CPU increased units by approximately 70% sequentially and is sold out. Lastly, our edge business was more resilient, supported by continued momentum in edge and physical AI design wins.
CCPG operating profit was $2.3 billion, representing 28% of revenue and approximately flat sequentially, primarily due to lower inventory charges.
Turning to Intel Foundry. Intel Foundry revenue was $6.7 billion, up 16% sequentially, driven by better-than-expected growth on Intel 3 and Intel 18A. External Foundry revenue was $411 million, an increase of $118 million sequentially, primarily due to a nonrecurring customer program.
Intel Foundry reported an operating loss of $1.9 billion, an improvement of $236 million sequentially, even as we continued to invest aggressively to prepare Intel 14A for risk production next year. Higher yields, better cycle times and increased factory utilization continued to reduce wafer costs. Intel 3 costs improved approximately 15% from Q1 levels, while volumes increased in the mid-teens sequentially. Intel 18A costs have declined approximately 40% since Q1, reflecting continued yield and cycle time improvements.
Intel 18A yields continued their upward trajectory to industry standard levels, ahead of our internal projections. Since Q1, Intel 18A client CPUs have grown from less than 5% of revenue to now nearly 1/3 of client CPU revenue. These results represent meaningful progress, although we still have considerable work ahead of us to deliver a sustainably profitable Foundry business.
Now turning to outlook. Demand signals from our data center customers continue to strengthen. We expect the industry to remain supply-constrained throughout 2027 and into 2028. As Lip-Bu discussed, the adoption of agentic AI is broadening the role of CPU compute. AI workloads are moving beyond prompt-based responses toward multistep reasoning, orchestration, and autonomous persistent action. Our CPUs play a central role in enabling these workloads.
As a result, we continue to see strong demand for our DCAI products. We now expect industry server CPU units to grow more than 30% in both 2026 and 2027. Growth would be higher in both years if additional industry supply were available. At the same time, the PC market is weakening after remaining resilient during the first half of 2026. We expect the 2026 PC unit TAM to decline approximately 12%, with second half units down more than 20%. We do not expect a sustained recovery until memory availability improves and pricing begins to normalize. For 2027, we're planning for the PC unit TAM to decline roughly 10%. We expect year-over-year declines to be more pronounced during the first half, with the potential for improvement in the second half against an easier comparison.
Our longer-term view of the PC market remains unchanged. Traditional PCs will play an important role in enabling AI applications and driving strong returns on AI infrastructure spending. In addition, we're just now seeing new agentic systems in the market. We also continue to see attractive longer-term opportunities in edge and physical AI as agentic applications spread across the economy.
Taking these factors together, we're guiding Q4 revenue to a range of $15 billion to $16 billion. At the midpoint of $15.5 billion, we expect a gross margin of 38%, a tax rate of 11% and EPS of $0.25, all on a non-GAAP basis. Our guidance includes an impact of roughly $300 million to revenue and 200 basis points to gross margin based on our early assessment of the incident at Fab 28. 
By segment, we expect DCAI revenue to grow mid-teens percent sequentially, with purpose-built silicon growing faster than DCAI overall. Please note almost all of the $300 million impact from Fab 28 is related to 10-nanometer server products.
We expect CCPG revenue to decline greater than 20% sequentially as customers move quickly to reduce weeks of inventory and align purchases with their expectations for 2027 consumption. The sequential decline in Q4 gross margin primarily reflects lower overall revenue against our fixed cost base as we adjust client wafer starts to current demand conditions. In addition, revenue mix, especially the strong growth expected in purpose-built silicon, is creating difficult quarter-on-quarter comparison. These headwinds will be partially offset by continued yield and cost improvements on Intel 3 and 18A.
We expect non-GAAP operating expenses of approximately $4.4 billion in Q4 and approximately $16.3 billion for the full year. We expect noncontrolling interest, or NCI, to be approximately $250 million in Q4, and we currently expect NCI of approximately $1.1 billion in both 2027 and 2028. Lastly, we expect Q4 fully diluted share count of 5.44 billion, representing a full quarter of shares issued for our August equity offering.
Moving to CapEx. Our 2026 gross capital expenditures remains on track to be $20 billion, and we expect 2027 gross capital spending to be up strongly. We have made good progress securing the equipment required to support our growth plans, with firm purchase orders to equipment suppliers increasing nearly 40% sequentially. We're also accelerating clean-room build-outs, including Fab 62 in Arizona, and exploring opportunities to accelerate in Ohio. Despite this increase in capital spending and working capital, we remain committed to deleveraging in 2027.
We will remain disciplined as we invest, and we will not spend $1 of capital unless we have confidence in the health of our products and process technologies and clear evidence of customer demand. Our confidence in all 3 is improving.
In closing, I want to offer a few words outlining the opportunity we see ahead. Our core server CPU market is growing faster than ever, and edge and physical AI represent meaningful incremental opportunities for client-class CPUs even as we navigate the current market conditions.
Importantly, as we improve our product execution and road map, we have opportunities to regain share and grow even faster than our underlying markets. Beyond our core x86 franchise, we are investing in 3 large opportunities where we have meaningful momentum but relatively modest revenue today: purpose-built silicon, advanced packaging and external wafer foundry. Each represents tens of billions of dollars of new markets where our technology, manufacturing assets and customer relationships provide us a differentiated opportunity to participate.
Taken together, we have line of sight to long-term double-digit revenue growth with meaningful leverage and improving margins. We have significant work ahead of us. However, the combination of stronger markets and the cultural changes set into motion by Lip-Bu to improve execution, transparency and discipline gives us increasing confidence in Intel's long-term earnings power and free cash flow growth, a solid foundation for building sustainable shareholder value.
With that, I'll turn it over to John to begin the Q&A.

**John Pitzer** (Executives):
Thank you, Dave. [Operator Instructions] With that, Jonathan, can we take the first question?

**Operator** (Operator):
Certainly. And our first question comes from the line of Timothy Arcuri from UBS.

**Timothy Arcuri** (Analysts):
Dave, I'm wondering with all the puts and takes and what's going on in PC, I'm wondering if you can give us maybe some guardrails maybe you could say it next year. I mean it seems like DCAI could grow $10 billion to $15 billion year-over-year, but PC, I'm guessing, is maybe down a touch. So can you just maybe give us guardrails for the year and sort of how to think about the shape of the year?

**David Zinsner** (Executives):
Yes, thanks, Tim. Yes, I'm not obviously going to guide next year, but maybe I'll give you some qualitative information. I would say at a high level, we see next year as a growth year. We feel like the momentum that we saw in data center this quarter, and taking away the impact from Israel, that momentum would have continued into the fourth quarter, we see that continuing next year. The only little nuance is the first half of the year, we are still a bit constrained. We've talked about putting 40% more capacity in substrates, but a lot of that doesn't hit until the back half of the year.
In addition, we are still constrained on Intel 3, and we're going to work towards moving, as Lip-Bu said, some of our supply into Oregon, but it's going to take a while before that comes out of the fab and gets into products. But we're very optimistic and enthusiastic about the opportunities for us next year in terms of growth on the data center business.
In addition, we talked about within DCAI, we also have purpose-built silicon. That business has been growing at a 3x rate over the last 3 years. We see that growing at a 3x rate in the next 3 years. And so we're really bullish about that throughout 2027.
Obviously, the client is going to be the most difficult to call. As I talked about, we see TAM declining in '26 by about 12% on a unit basis. We think that's going to be about 10% next year on a unit basis. So that will be one dynamic. Then there's going to be this kind of inventory correction. We're in the throes of that right now. We felt a little bit of it in the third quarter, we're going to feel a lot of it in the fourth quarter. We think it extends at least out into the first quarter. After that, I think you'll start to see like the inventory correction part of this start to kind of wane and we'll be back into more of like what's going to go on, on the TAM side, which, as I said, we're thinking about 10% down.
The one added piece of this is we come into next year with Nova Lake as our product offering. And we think this is the best set of products we've had in a very long time. We think it covers the gamut of what's required to participate in client. We're very excited about it. We think next year and in the future years, we're in a kind of a market share gain type of environment for our clients. So obviously, unfortunate that we run into this challenge on the memory side and its impact on client, but we are very enthusiastic about the product side.
And I just -- you didn't ask this question, but I'll just extend it out beyond this year. We do think that the PC is going to go through a renaissance despite this. And we think that as AI workloads start to shift around, there's going to be a lot of workload required in the client space, either as a PC or a some kind of agentic box. And so we do see this market as being pretty interesting. It's got to obviously get through this bit of challenge that we have. But longer term, feel really good about the market.

**John Pitzer** (Executives):
Tim, do you have a quick follow-up question?

**Timothy Arcuri** (Analysts):
I do. Yes. So Dave, you did say that CapEx is going to be up a lot next year. I think a lot of us are thinking kind of like $30 billion. But I guess the real question is, are you committed to generating free cash flow next year? Or do you think because of the CapEx burden that, that will be hard?

**David Zinsner** (Executives):
Yes, it's a good question. Yes, we haven't exactly locked into the number. We don't do that until we get towards the end of this year. But we have kind of a directional understanding of what's likely to happen. And we have been putting POs in place with equipment vendors given the lead time. So we have some sense of what's going to happen.
I think next year is an investment year for us as we look at the year. Probably not a dynamic where we're going to have positive free cash flow next year. But it's because we see this as a tremendous opportunity to invest into the growth. And one thing that we have seen is you make the right investments, you ramp the node in the right way, you see profitability and you see return on invested capital. And we talked about this as we were doing the equity offering at the beginning of August, that we think we should be getting at least 20% ROI on all of these nodes as we invest in them.
But this -- next year is going to be one of those years where there's a couple of things going on at the same time. We're ramping 18A, we're ramping Intel 3 to some extent, and we're making the appropriate investments to position 14A to begin production in '28. That's a lot of investment all kind of hitting us in one year. So I don't think that this will be a year in which we see positive cash flow.
And by the way, that is why we raised the money that we did at the beginning of August, was to get ourselves positioned to do this. Longer term though, these businesses generate lots of cash flow. And if you look at Intel 7 today, kind of 10-nanometer 7, that's already a profitable node to us. Intel 3 is going to be profitable next year for us. So we know we can make these businesses profitable. We know we can generate good cash flow from them. We know we can get 20% return. We just got to get through what is basically a knothole here in '27 to go realize that.

**Operator** (Operator):
Our next question comes from the line of Ben Reitzes from Melius.

**Benjamin Reitzes** (Analysts):
I wanted to ask about some of the issues that you noted for 4Q and that may linger into 1Q and see if you can kind of size them versus prior expectations and then when they get better. You cited execution, obviously, the Israel situation, which is $300 million. Wondering what that's going to be in the quarters after that and when that is solved. And sorry that happened, by the way. And then the client. And in the context that the guide is about $1.8 billion below the Street, maybe you can kind of go through those 3 things, how big they are to the cut of $1.8 billion and when they get better, that would be great.

**David Zinsner** (Executives):
Yes. What was the -- so Israel, the client, what was the third one?

**John Pitzer** (Executives):
Just relative to the guide in the Street.

**David Zinsner** (Executives):
Yes. Okay. So...

**Benjamin Reitzes** (Analysts):
The execution, Dave. There was an extra comment around execution, and Lip-Bu made some comments. I'm wondering how big that was in terms of the guidance cut.

**David Zinsner** (Executives):
Okay. Well, on Israel, we've been shut down for about 2 weeks. We feel like we're going to be starting up production here by the end of this week. While we're doing that, we're trying to assess all the wafers that are in the line and what's usable and what's not usable from those materials. So this is somewhat of an early assessment, both really of 4Q and 1Q. But I think the current thinking is that we'll have about a $300 million impact to the fourth quarter. That's likely to be similar in the first quarter.
We think most of the write-offs of wafers or scrapping of wafers is likely to all kind of happen in the fourth quarter. That's kind of what's driving the 200 basis point. But I wouldn't expect to see additional scrapping going on in the first quarter. But just keep in mind, it's early. We're going through all of that as we speak, and we'll, of course, update you as we go along.
I think on the client side, obviously, it's going to kind of reset to this level, and we're going to have -- I think, usually, you have a very similar inventory correction quarter-to-quarter. So I would expect it to generally be similar other than there will be more -- you will have a seasonality effect in Q1 on client as well. So the likelihood is that whatever the level that we're talking about for the fourth quarter, we'll see somewhat of a seasonal decline next quarter.
Beyond that, I think from an execution perspective, I have to think about some of the negative things, but a lot of the execution has been really positive. I mean Lip-Bu has -- and the team have done a very good job driving Intel 3 yields, driving 18A yields and working with the substrate vendors. Lip-Bu was in Japan talking to many of the substrate vendors, to make sure that we were getting allocated the appropriate supply. So I think we're as positioned -- or as well positioned as anyone out there in terms of delivering supply. It's tight. It's going to be tight this next quarter. It's going to be tight into the first half. But I think we've positioned ourselves well that, beyond that, we should start to see some pretty healthy growth in the data center business.

**John Pitzer** (Executives):
Ben, do you have a quick follow-up?

**Benjamin Reitzes** (Analysts):
Yes. Then just with regard to the server velocity, there's shortages and whatnot. But do you have an idea for when you think you can ramp and grow in line with the market that's going on that $200 billion plus? Is that more second half next year based on your commentary?

**Lip-Bu Tan** (Executives):
Yes. Good question. I think, Ben, first of all, I think the server, the biggest revenue for us is the Granite Rapids, that's on the Intel 3. Clearly, we are continuing to drive efficiency in terms of yield. And then secondly, we also try to expand the capacity. And I think Dave mentioned about Oregon, we are planning to have that Intel 3 in the second half of next year to be in the production so that we can supply some of the demand from the customer.
And so I think overall, I think we'll be good to address the Intel 3. And then clearly, we have the Clearwater Forest coming up, and we are in the shipping in revenue that's on 18A, we should have capacity for that. And then Diamond Rapids, that will be 2027, we have 18A-P, we'll be ready for that. And of course, the Coral Rapids coming up in 2028, that will be on the 14A. So those, I think, will be in pretty good shape.

**Operator** (Operator):
Our next question comes from the line of Joseph Moore from Morgan Stanley.

**Joseph Moore** (Analysts):
Yes. I mean along the same lines, does the PC weakness give you the opportunity to reallocate wafers and sort of address some of this and accelerate that transition?

**David Zinsner** (Executives):
The answer is yes. We had -- what we're taking offline to put Intel 3 into Oregon is 18A wafers, which we're generally going to build Panther Lake products. So we see the opportunity with some of that capacity freed up to go produce more data center wafers.
Just keep in mind that we're not only constrained on the wafer side, we're also constrained on the substrate side. So it's important we get the substrate piece of this ramped up to be able to meet the demand.

**John Pitzer** (Executives):
Joe, do you have a follow-up question?

**Joseph Moore** (Analysts):
Yes, I do. How do you see server market share next year? I think you talked about 30% unit growth. AMD has guided to 70% revenue growth. The ARM camp seems to be growing quite quickly. Just -- I understand you're constrained, but how do you sort of see market share playing out?

**Lip-Bu Tan** (Executives):
Sure. I think that's a good question. So clearly, we have a road map. We like what we have. In terms of Coral Rapids, we will be competitive to AMD. And the next-generation product, the tick-tock, we'll be ahead of the AMD on that. So I think stay tuned, we'll continue to drive leadership. CPU is really our franchise. We are determined to drive success there. And then I think that's a good opportunity for us to really drive that.

**David Zinsner** (Executives):
I'd say maybe one other addition is I really see market share next year being a function of supply. And so the more we can improve our supply on a relative basis, the better we'll do in terms of market share.

**Operator** (Operator):
Our next question comes from the line of Stacy Rasgon from Bernstein Research.

**Stacy Rasgon** (Analysts):
I wanted to dig into gross margins a little bit. So I get that the 38% guidance, I guess, would have been 40% without the unfortunate situation in Israel. But as I'm looking into next year, how do I think about the overall drivers? I've got a -- clearly, I have a client flush and maybe utilization issue, which is a negative. I've got depreciation probably going up from CapEx, which is a negative. 
And then maybe like as 18A and 3 ramp, I get the yields are getting better, but I guess you can tell us if the gross margins on those parts are still below [ 10 7 ]. I wonder if that mix shift is a headwind plus ASICs and packaging and everything.
And maybe on the other side though, maybe mix towards servers as a positive, maybe pricing helps. I'm just trying to get a feeling of the gross margin evolution in this kind of an environment given all of those puts and takes. It just seems like there's a lot of them. I'm hoping you could help with that a little bit.

**David Zinsner** (Executives):
That's a good question, Stacy. There are definitely a lot of moving pieces. I think from a margin perspective, the Israel piece, it's probably on a margin basis is going to be really more of a Q4 event. I don't expect a significant amount in Q1 in terms of scrapping. Usually, if we can identify it, we'll scrap it in the quarter. We have Xeon demand remains really strong. And I think I mentioned Granite Rapids is now margin accretive for us. So growth in Granite Rapids is helpful to gross margins. And we will also continue to be focused on both Intel 3 and 18A.
Their structural cost is what we can focus on more, as well as yields, throughput, all of those. We did very well in Q3, we expect to do better in Q4. And the goal is to continue to drive that through the year.
You're right on 18A, the loading isn't going to be where we want it. We're fixing a little bit of that with putting Intel 3 in Oregon. But nevertheless, there will be a little bit of a underloading scenario for 18A that's going to be a little bit of a headwind.
The other headwind for us, which is, I think, a positive viewed the right way, is our purpose-built silicon business, and it's kind of in its early stages, its margins are below the corporate average. But we see tremendous growth there. And Lip-Bu and I really decided to focus on driving the gross profit. And so we're just going to grow the gross profit. That will grow the earnings. It may put a little pressure on the operating margin percentage through next year, but I think it will be goodness at the bottom line. 
I think when you put all that together, and it's so many puts and takes, it's hard to quantify, I still lean towards the 40% to 60% fall-through. That's probably what we're shooting for. So if we have a growth year next year, we should see gross margin expansion given that kind of rule of thumb. It may not work out every quarter that way. But I think when you look at it on a year-over-year basis, it's going to be in that kind of range.

**John Pitzer** (Executives):
Stacy, do you have a follow-up question?

**Stacy Rasgon** (Analysts):
I do, yes. I guess I wanted to ask about PC. So I mean, Q3 was probably the worst Q3 I've seen for PCs in at least 20 years, maybe more, sequentially. So it does sound like customers probably built inventory in Q2. I guess can you confirm that? And then it sounds like that they're flushing out a bunch in Q4. I'm trying to get -- and maybe even in Q1. It sounds like you think things get better in the second half as, I suppose, memory supply. What gives you confidence that memory supply is actually going to improve? If you listen to memory guys, they seem to be suggesting that it won't.

**David Zinsner** (Executives):
Yes, let me clear. I mean -- yes, it's a good question. Stacy, let me be clear. We think that when -- you're dead-on that Q4, Q1 are going to be likely the 2 quarters in which there's most of the inventory correction, and that impacts us more than the TAM declines. So we will see that in the first, call it, Q4, Q1, maybe stretching a little bit into Q2. 
After that, it does recover back to where, theoretically, where billings to us are somewhat equivalent to consumption. So we get a little bit of a recovery from that. But make no mistake, we are not optimistic about next year in terms of memory. We think that it is going to impact the TAM. We think TAM will be down 10% on a unit basis next year. And then we'll have to see in '28 whether things improve. But our expectation is that it does not improve in '27.

**Operator** (Operator):
Our next question comes from the line of Vivek Arya from Bank of America Securities.

**Vivek Arya** (Analysts):
For the first one, if I take your, I think, implied DC guidance for Q4, that puts it at about $8.5 billion or so. And if I annualize that, that's like mid-30s billion in terms of a conceptual target for next year. So I'm curious, is that a doable floor? Can you do better? Is there kind of ASP expansion, just given demand is outstripping supply? Or are there other factors we should keep in mind as we think about how large your data center business could be in '27?

**David Zinsner** (Executives):
Yes. I think that's a good starting point. I think that's the right way to think about it. What we would characterize is that the first half of '27 is likely to be tighter in terms of wafers and substrates. But we've put a lot of work in place, both in terms of as I talked about increasing our wafer output of Intel 3, improving yields as a freeway to get more product, and the investments we've made in the substrates with vendors unlock that capacity in the back half of the year. So we do expect it to be big growth.
I mean keep in mind also that we roll our purpose-built silicon, our ASIC business in under that business unit. So that's part of what's driving a lot of the growth in the fourth quarter. And again, we expect that to continue in '27.

**John Pitzer** (Executives):
Vivek, do you have a follow-up?

**Vivek Arya** (Analysts):
Yes. I was hoping to get an update on engagements with external customers in your foundry both on the packaging side. And then also more importantly, Lip-Bu, on the kind of the wafer processing side. Are you expecting external customers for 18A-P? Or should we assume that all the engagements will be on 14A? And when do you think Intel gets the confidence to move them from sort of the evaluation to the tape-out or tangible revenue column? So we're all kind of set in terms of when we should start modeling external revenue for Intel over the next few years.

**Lip-Bu Tan** (Executives):
Good. Vivek, thank you so much for the question. So I think clearly the first question you have is about the packaging. Our EMIB-T making great progress. We have been very focused on capacity in the substrate, making sure that we can secure the capacity we need and also the yield profile for the capacity from substrate for material.
Secondly, we focus on the yield, and we are improving substantially. And then thirdly, it's the cycle time. And then so far, under the leadership of Seok-Hee Lee, he used to be the CEO of SK Hynix, expert in the process integration. He's done fabulous job, very dedicated. I think we get a lot of capacity in the next 2 years in terms of the substrate material. And we're also improving the yield as the day go by.
And then overall, I think we're going to have some -- stay tuned, we're going to have a couple of customers ready to announce in the next 2 quarters. And then, so clearly, we always want to wait for the customer. If they want to announce, we will respond to that.
And then secondly, on the 18A-P, we're making great progress in volume production from Panther Lake, and then clearly on the Wildcat Lake. And so I think those, I think, internally, we've been using. The yield, we are quite happy with the performance. And right now, we also have inbound interest from the external customer, and we are intensively working with them, and they are very pleased with the yield. And right now, we are focused on the die size, make sure that we can deliver to them and also make sure that IP ready for that. So I think 18A-P, stay tuned. We have some good progress on that. 
On the 14A, we made tremendous progress. I think we announced the 0.9 PDK. We already released to our select customers. They already responded very actively working with us. And then the other part is also, I think, in terms of performance, yield, all the metrics and defect density and the variation, we are making daily improvement on that. So far, we are very pleased. We should be able to do the 1 PDK by Q1 next year, and we can start engaging with customers with products they like to use our fab. And so I think stay tuned again, we will have time to announce some of the customers when they are ready.

**Operator** (Operator):
Our next question comes from the line of Harlan Sur from JPMorgan.

**Harlan Sur** (Analysts):
Commencing second half of this year, there's a number of new GPU and XPU platform launches. Most of these new launches are going to continue to ramp through the first half of next year. Given the strong CPU attach to these platforms and many of them are Intel x86 CPU-based platforms. And then additionally, in addition to the overall sort of supply dynamics, which remain tight, but the team is bringing on more capacity, yields are improving, as you mentioned. Given all of this, should we anticipate continued sequential growth in DCAI in the first quarter?

**David Zinsner** (Executives):
Yes. I mean I would avoid guiding too much the quarter. I think your overall premise is right. There's going to be a strong driver of demand for CPUs. We see that continuing all through next year. We're working on the supply side of the equation to make sure that we can meet what customers need. We will likely not fully meet what they require. But I think we're going to be in a more challenging situation in the first half of the year than we are in the second half. So maybe that's one added data point I'd just make sure that you're using when you're modeling. Outside of that, I'd prefer to wait for another quarter and see how things kind of play out before we guide Q1's data center.

**Lip-Bu Tan** (Executives):
Harlan, just to add on that. I think clearly you saw our announcement with Oracle Cloud. And we also have multiple customers, they are all interested to sign up the LTA agreement with us. So that make sure that we can secure the CPU rollout for them. So I think those are encouraging signs that CPU is high demand.

**John Pitzer** (Executives):
Harlan, do you have a follow-up question?

**Harlan Sur** (Analysts):
Yes. On the factors that the team has control over and as a reflection of the continued yield, reliability, manufacturability improvements, I think back in Q2, both Panther Lake and Granite Rapids gross margins were below corporate average. But as Intel 3 and 18A saw further yield improvements in the third quarter, you did mention Xeon 6 Granite Rapids on Intel 3 accretive to gross margins in Q3. Did the team also drive Core Series 3 Panther Lake gross margins above the low/mid-40% level in Q3 as well?

**David Zinsner** (Executives):
So we have definitely made meaningful improvement on the gross margins of Panther Lake. It's not yet at or above the corporate average, but we have made huge strides. And this is just a matter of grinding it out on yields and throughput and driving the right scale and so forth. And these will be accretive gross margins over time. It's just not quite there yet.

**Operator** (Operator):
Then our final question for today comes from the line of C.J. Muse from Cantor Fitzgerald.

**Christopher Muse** (Analysts):
I guess first question, going back to CapEx, you talked up significantly. Curious how you're thinking about spending on WFE versus buildings. I think in the past, you've talked about majority of the incremental spend on buildings. I wanted to confirm that that's still kind of the direction that we're going.

**David Zinsner** (Executives):
Yes. So we have, I think, a significant ramp in equipment spend this quarter, and it's expected to be even more significant next quarter. So a lot of what we're spending on now is really equipment. We have made the investments. I would call it, putting -- in a lot of cases, putting the finishing touches on some of the space and just -- and most of the spend is going towards equipment, with the only exception we're still in the heavy construction phase of Ohio. But outside of that, it's really about equipment.

**John Pitzer** (Executives):
C.J., do you have a quick follow-up?

**Christopher Muse** (Analysts):
Yes, I do. On the PC side, I know you've talked about units down 10% next year for the industry. Curious if you could comment on how you're thinking about your mix shift and what impact that might have on your pricing?

**David Zinsner** (Executives):
Mix shift in terms of like low end versus high end and so forth? Is that what you mean?

**Christopher Muse** (Analysts):
Yes, exactly.

**David Zinsner** (Executives):
Yes. I mean we have -- I would say we have seen strong demand in Panther Lake on a relative basis. Obviously, the whole market is coming off, but Panther Lake is holding its own. We also put a lot of effort into a product called Wildcat Lake, which is a cost-optimized part. We've seen significant growth in Wildcat Lake. It's coming exactly at the right time because it's cost-optimized and we're seeing a lot of focus in that regard.
As we go into next year, we'll have Nova Lake. And I think the important aspect of Nova Lake is we've had a bit of a hole in our portfolio for high-end desktop, and Nova Lake filled in that gap. So I would expect us to do pretty well on a mix basis because we should see better traction on the high-end desktop as well. So we'll see how it goes. We do feel like we go into the year as a market share gainer with our Nova Lake portfolio. And obviously, we'll kind of monitor the market and see how things kind of play out.

**Lip-Bu Tan** (Executives):
With that, I want to thank everyone for joining us today. We made good progress this quarter on our journey to transform Intel, but we still have a lot to work ahead of us. I'm looking forward to seeing many of you throughout the quarter and providing another update in January.

**Operator** (Operator):
Thank you, ladies and gentlemen, for your participation in today's conference. This does conclude the program. You may now disconnect. Good day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### INTC_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜CFO｜guidance：Q3 營收財測區間（原話："we're guiding Q3 revenue to a range of $15.8 billion"）
- 2026-07-23｜CFO｜guidance：Q3 財測中點毛利率與稅率（non-GAAP）（原話："we forecast gross margin of 42%, a tax rate of 11%"）
- 2026-07-23｜CFO｜guidance：2026 全年 PC 消費預期（原話："down low double digits percent for all of 2026"）
- 2026-07-23｜CFO｜guidance：伺服器 CPU 產業單位成長預期（原話："strong double-digit unit growth for the industry"）
- 2026-07-23｜CFO｜guidance：全年 non-GAAP 營業費用目標（原話："non-GAAP operating expenses to roughly $16.5 billion"）
- 2026-07-23｜CFO｜guidance：下季 CCPG 與 client 營收展望（原話："it's going to be kind of flattish for us"）
- 2026-07-23｜CFO｜guidance：伺服器供給線性偏向 Q3 末與 Q4（原話："near-term linearity of our supply growth is more skewed"）
- 2026-07-23｜CFO｜guidance：Q4 仍追不上需求（原話："We will be behind in the fourth quarter"）
- 2026-07-23｜CFO｜capital_allocation：2026 資本支出上調（原話："expect our CapEx to be more than $20 billion"）
- 2026-07-23｜CFO｜capital_allocation：2027 資本支出將顯著高於 2026（原話："expenditures to be significantly above the 2026 levels"）
- 2026-07-23｜CFO｜capital_allocation：2027 資本支出數字尚未定案（原話："I purposely didn't mention the number for 2027"）
- 2026-07-23｜CFO｜capital_allocation：2026 設備支出增幅（原話："We'll increase tooling in '26 by 40% relative to '25"）
- 2026-07-23｜CFO｜capital_allocation：投資稅額抵減比例（原話："getting $0.35 on the dollar back from the investment"）
- 2026-07-23｜CFO｜capital_allocation：約 100 億美元非核心資產可變現（原話："$10 billion of what I call noncore assets"）
- 2026-07-23｜CFO｜capital_allocation：可能需要資本市場融資（原話："we may need to tap the capital markets to drive some more"）
- 2026-07-23｜CFO｜capital_allocation：客戶願意共同投資（原話："our customers willing to invest with us"）
- 2026-07-23｜CFO｜commitment：14A 風險試產與 2028 量產承諾（原話："committed high-volume ramps in 2028"）
- 2026-07-23｜CEO｜commitment：14A PDK 0.9 時程（原話："0.9 for 14A is on track for October"）
- 2026-07-23｜CFO｜commitment：資本支出與客戶需求配合（原話："matching our expenditures with customer demand"）
- 2026-07-23｜CEO｜commitment：資本支出前提條件（良率、IP、客戶參與）（原話："I don't put CapEx unless I see the yield"）
- 2026-07-23｜CFO｜commitment：每季毛利率維持在 40% 以上（原話："comfortably into the 40s in every quarter"）
- 2026-07-23｜CFO｜commitment：不在客戶承諾前下注（原話："careful around making bets ahead of customer commitments"）
- 2026-07-23｜CFO｜margin：Q2 毛利率超標原因（原話："better yields, and higher ASPs due to mix and pricing"）
- 2026-07-23｜CFO｜margin：CCPG 庫存減損說明（原話："stranded inventory, we wrote that down"）
- 2026-07-23｜CFO｜margin：新產品毛利仍低於公司平均（原話："they're still below the corporate average"）
- 2026-07-23｜CFO｜margin：毛利增量落差（fall-through）區間（原話："we'd expect that to be somewhat the fall-through"）
- 2026-07-23｜CFO｜margin：Panther Lake 成本下降（原話："driven down the cost of our primary Panther"）
- 2026-07-23｜CFO｜margin：CCPG 營業利益率（原話："CCPG was $2.3 billion, 26% of revenue"）
- 2026-07-23｜CFO｜margin：晶圓代工營業虧損（原話："operating loss in Q2 was $2.1 billion and $348 million"）
- 2026-07-23｜CFO｜margin：外部晶圓代工營收（原話："External foundry revenue was $293 million in the quarter"）
- 2026-07-23｜CFO｜margin：Client 營收強勁主因為 ASP（原話："I would say it was largely ASP"）
- 2026-07-23｜CFO｜customer：AI 相關業務成長（原話："our AI-driven businesses grew greater than 70%"）
- 2026-07-23｜CEO｜customer：新增策略客戶與長期合約（原話："outlook with the additional strategic customer wins"）
- 2026-07-23｜CFO｜product：18A 產出高於目標（原話："output approximately 25% above target and up more than"）
- 2026-07-23｜CEO｜product：14A 良率與缺陷密度進度（原話："the yield for 256 SRAM and the defect density"）
- 2026-07-23｜CEO｜product：伺服器年增率（原話："year-over-year server growth was the strongest on record"）
- 2026-07-23｜CFO｜product：ASIC／客製晶片營收規模（原話："at least approaching a $2 billion run rate"）
- 2026-07-23｜CFO｜product：ASIC 營收目標規模（原話："we'll be at a $4 billion run rate for that business"）
- 2026-07-23｜CFO｜product：伺服器營收成長預期（原話："double-digit CAGR for us in terms of growth rate"）
- 2026-07-23｜CFO｜competition：CPU 對 GPU 比例（原話："we're almost in parity at this point"）
- 2026-07-23｜CEO｜competition：競爭地位自述（原話："Some areas we are still behind, but we are catching up"）
- 2026-07-23｜CFO｜risk：封裝材料與記憶體為供給瓶頸（原話："procuring all of that is also a bit of a choke point"）
- 2026-07-23｜CFO｜risk：後端投資可能拖累明年現金流（原話："That could be a drag to gross -- to cash flow next year"）

### 問答異常語氣（迴避／改口／保留）
- INTC_Q2_2026_Earnings_Call_20260723.md｜問：Rasgon：庫存減損多大？剔除後 Q3 毛利率指引是否實質下滑｜答法：先反問對方指的哪項庫存，說明為 match set 未完成而減損，未給金額，僅稱指引持平
- INTC_Q2_2026_Earnings_Call_20260723.md｜問：Arcuri：Q4 是否因產能上線而大幅成長｜答法：以只給一季指引回應，僅說供給改善會帶來提升但仍落後需求，未給數字
- INTC_Q2_2026_Earnings_Call_20260723.md｜問：Arya：外部晶圓代工客戶何時公告；明年資本支出增幅｜答法：未回答客戶公告時點；資本支出稱 2027 數字還需一到兩季才定案，只說會上升
- INTC_Q2_2026_Earnings_Call_20260723.md｜問：Moore：伺服器市占率與對 AMD、ARM 的奪回前景｜答法：未談市占數字，轉談需求強與供給限制及產品路線圖，承認部分領域仍落後
- INTC_Q2_2026_Earnings_Call_20260723.md｜問：Reitzes：競爭對手提出 2030 CPU TAM 2,200 億美元，是否認同｜答法：表明不給數字，稱無人能精準預測，只說市場會顯著成長
- INTC_Q2_2026_Earnings_Call_20260723.md｜問：Rakers：ASIC 業務年化約 12 億美元之後的成長與毛利率結構｜答法：CFO 回覆目前接近 20 億美元年化、未來 40 億美元，未回答毛利率部分

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

## ⑥ 條件附卡（archetype_hint='轉機/特殊情境' 命中）：judge_addendum_archetype.md

<!-- source: .claude/skills/stock-analyst/references/archetype-gatesets.md sha256:d173785f92087f36 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary ∈ {金融，未獲利高成長，轉機/特殊情境，受監管公用/穩定內需} -->

# archetype 換尺 gate-set 附卡（QC-44/45/46）

## QC-44 金融（bank／insurer／broker）
archetype=金融時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：ROTCE(替FCF Margin) >15%穿越循環｜ROE且>COE~10%(替ROIC) ROE>12-15%｜跨信用循環ROTCE穩定含2008/2020壓力年(替10Y ROIC穩定) 壓力年仍正/不破底｜NIM趨勢+效率比cost/income(替毛利率定價) 效率比<~60%｜Capex/Rev不適用→operating leverage/效率比改善｜EPS+TBVPS複合+股息總回報(替EPS CAGR>20%) ~10-12%即優｜P/TBV vs ROTCE(替PEG)：Warranted P/TBV=(ROTCE−g)/(COE−g)，實際P/TBV≤warranted｜CET1 ratio(替D/E<0.7) >監管要求+緩衝(~11-13%)｜NPL/NCO趨勢+撥備覆蓋+CET1緩衝(替負債安全性)：信用品質穩、撥備足。[§QC-44]
§10估值主錨：P/TBV分位+P/E，用Warranted P/TBV判貴賤；EV/EBITDA拿掉。QC-31 signal：X改ROTCE跨循環<COE／CET1跌破監管／NPL·NCO結構惡化／重大舞弊，移除FCF·NI、EV-EBITDA、Capex觸發。§6跑道：放款·存款·AUM成長+費收業務+市佔，非TAM滲透。[§QC-44]
子型：bank＝CET1/NIM/效率比/NPL·NCO/ROTCE/P-TBV｜insurer(注意US掛牌ALV=Autoliv汽車安全件循環工業，非保險，勿誤歸)＝combined ratio<100%/float/Solvency II ratio/book value/ROE，不看NIM/CET1｜broker·交易所＝ARPU/AUC/take rate/活躍戶，常與未獲利高成長blend｜支付網絡不歸金融，走品質複利。[§子型]
batch補搜：`[ticker] CET1 ratio NIM efficiency ratio ROTCE`(bank)／`[ticker] combined ratio Solvency II book value`(insurer)；yfinance .info 給不出 CET1/NIM/效率比/NPL/ROTCE/TBV。[§batch]

## QC-45 未獲利高成長
archetype=未獲利高成長時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：Rule-of-40(營收成長%+FCF margin%，替EPS CAGR>20%) ≥40｜EV/S÷營收成長growth-adjusted或EV/gross-profit(替PEG<2)｜NRR+毛利率+增量OI margin改善軌跡(替ROIC>15%，GAAP負無意義) NRR>110%/GM>65-70%｜FCF margin+轉正軌跡(替FCF Margin>15%；已正看margin升，未正看跑道+轉正路徑)｜NI負時FCF/NI比無意義→改看FCF margin絕對值+淨現金+跑道，FCF正或跑道>12個月。[§QC-45]
§10估值主錨：EV/S(+EV/gross-profit)+Rule-of-40-adjusted，轉正後接forward P/E；trailing PE/PEG拿掉。**情境樹同步改走EV/S（2026-10-12）**：FY1共識EPS≤0時程式自動切`valuation_basis=sales_multiple`，`scenario_inputs`填營收路徑×終端EV/S×終端淨負債×終端股數（形狀見尾段），不再用EPS×本益比；負債重者(淨負債/EV>30%)Bear的`net_debt_y5`須如實反映融資缺口，股權價值為負即歸零。QC-31 signal：不因GAAP NI負觸發X；X改NRR跌破100%／Rule-of-40<20連2季／毛利結構崩／現金跑道<12個月無轉正路徑／SBC稀釋失控(股數>10%/yr無營收槓桿)。§6跑道：NRR+淨增客戶+TAM滲透+SBC-adjusted轉正時程。blend：fintech broker常＝金融×未獲利，兩套都跑、標背離。[§QC-45]

## QC-46 轉機／受監管公用（輕量尺，不展開大表）
轉機/特殊情境：§4/§10主錨→資產重估/SOTP/normalized earning power/P-TBV，非成長外推；EPS-CAGR/PEG不適用。Single Thing→轉機觸發(債務重組完成/出售虧損部門/新管理層/catalyst里程碑)，非「moat擴張」。§6/§5→「為何現在會轉」catalyst+下行保護(資產底/清算價值)。QC-31 X→流動性危機(跑道<12個月+無再融資)/重整失敗/治理舞弊。[§QC-46轉機]
受監管公用/穩定內需：§4/§10主錨→DDM/殖利率+股息成長/regulated ROE(rate base×allowed ROE)/P/B；PEG/高成長門檻不適用。§6成長→rate base成長+費率案(rate case)+准許ROE，非TAM滲透。§5護城河→監管特許/天然獨佔(single-axis)。QC-31 X→准許ROE結構下調/費率案連敗/監管轉敵/過度槓桿(利率敏感)。[§QC-46受監管]
此兩類不強制長表，但換尺與catalyst/下行保護須sourced。[§QC-46]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260724","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Intel Foundry 成為可外賣的外部代工業務（外部營收占比實質上升、至少 1 個 tier-1 14A design win 轉 commitment）","columns":{"2Y 驗證點":"FY27 外部 foundry 營收占比 ≥ 10%；≥1 個具名 tier-1（Apple/QCOM/AMD/NVDA/MSFT）公開 commit 14A wafer","5Y 驗證點":"FY28-29 14A 外部營收 ≥ $5B；≥2 個 tier-1 公開 commit","10Y 驗證點":"FY30+ 外部營收 ≥ $15B（≈ TSMC 10% 規模）","具體數字門檻":"外部占比 ≥ 10% FY27；14A ≥ 2 tier-1 FY28-29","信息來源":"Q2'26 法說（外部 $293M）+ BofA + 8-K","漂移觸發":"連 2 季外部占比未升 / 1H27 仍零具名"}},{"id":"H2","text":"財務結構性轉正（foundry breakeven、FCF 由負轉正）","columns":{"2Y 驗證點":"Foundry exit-2027 breakeven 如期；FY27 GAAP NI &gt; 0","5Y 驗證點":"FY28-29 FCF margin &gt; 8%；GAAP ROIC &gt; WACC","10Y 驗證點":"FY30+ FCF margin &gt; 15%；ROIC 穩定 &gt; WACC ~10%","具體數字門檻":"Foundry breakeven 2027；FCF 轉正 2028","信息來源":"Q2'26 法說（foundry −$2.1B 收斂）+ BofA（exit-2027）","漂移觸發":"breakeven 滑出 2027 / FCF 連 2 季無改善"}},{"id":"H3","text":"當前估值（P/B 5.5x 五年頂、Fwd PE FY26 90x）由轉機兌現支撐、不崩","columns":{"2Y 驗證點":"P/B 維持 &gt; 4x 需外部客戶落地佐證","5Y 驗證點":"倍數由「optionality premium」轉為「earnings-backed」","10Y 驗證點":"normalized ROE 回到 12%+ 支撐 P/B","具體數字門檻":"不因單一利多回檔破 P/B 3x","信息來源":"GuruFocus P/B 五年區間 0.9-5.1x","漂移觸發":"FY1/FY2 EPS 共識連 2 月下修 ≥ 5%"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"外部 foundry 客戶始終不來：客戶「等成熟良率」的觀望被證明對，14A 2028 才量產給了他們等待理由","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"外部占比 / 具名 commitment 數","警戒閾值":"1H2027 前零具名 tier-1 → thesis 嚴重削弱"}},{"id":"R2","text":"伺服器份額續失於 AMD（ASP/mix 問題）：AMD 46.2% x86 伺服器營收份額 record，且 Diamond Rapids 砍 SMT、滑到 2027（Tan 自認「less competitive」）","columns":{"對應假設":"H1/H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"AMD 伺服器營收份額 / Intel 高 ASP mix","警戒閾值":"AMD &gt; 50% → DCAI 反彈為單季事件"}},{"id":"R3","text":"資本黑洞 + 治理干預：capex 再升需增資稀釋；Delaware 訴訟 + 國家股使資本配置受政治干預","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"FCF TTM / 增資動作 / 訴訟進展","警戒閾值":"被迫 tap 資本市場稀釋 / 訴訟判治理瑕疵"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"首個具名 tier-1 外部客戶 14A/18A 晶圓 commitment（把 >$15B pipeline 轉成經常性營收）；或 foundry 2027 exit breakeven 如期兌現且外部營收占 foundry 比 ≥ 10%","irr_base_pct":1.9,"ev5y_pct":9.5,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"C","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.3,"ev5y_pct":9.5,"irr_base_pct":1.9,"max_dd_pct":-65.0,"bull_5y_price":180.0,"bear_5y_price":50.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"首個具名 tier-1 外部客戶 14A/18A 晶圓 commitment（把 >$15B pipeline 轉成經常性營收）；或 foundry 2027 exit breakeven 如期兌現且外部營收占 foundry 比 ≥ 10%","price_at_dd":100.23,"archetype":"轉機/特殊情境","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INTC_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
