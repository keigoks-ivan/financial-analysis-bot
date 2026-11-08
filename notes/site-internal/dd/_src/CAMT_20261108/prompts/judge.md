你是 stock-analyst **v20 判斷 agent**，標的 CAMT（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CAMT","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAMT_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAMT_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":161.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html"}},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income","value":47.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html"}},{"id":"f_kpi2_non_gaap_operating_margi","label":"Non-GAAP operating margin","value":29.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html"}},{"id":"f_kpi3_gaap_operating_income","label":"GAAP operating income","value":39.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html"}},{"id":"f_kpi4_gaap_operating_margin","label":"GAAP operating margin","value":24.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html"}},{"id":"f_kpi5_operating_cash_flow","label":"Operating cash flow","value":71.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html"}},{"id":"f_kpi6_share_based_compensation","label":"Share-based compensation","value":5.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html"}},{"id":"f_kpi7_cash_deposits_marketable","label":"Cash, deposits & marketable securities","value":877.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html"}},{"id":"f_kpi8_gaap_gross_margin","label":"GAAP gross margin","value":50.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html"}},{"id":"f_kpi9_guidance_q4_2026_revenue","label":"Guidance: Q4 2026 revenue","value":180,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M（約數，~+40% YoY）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html"},"note":"FY2026 營收指引約 595 vs yfinance FY1 共識 596.38（dd_numbers_extra capital_structure）；FY2027 指引 >800 vs 共識 804.17"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_camt_gross_margin_pct","label":"CAMT 毛利率","value":50.03,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAMT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_camt_operating_margin_pct","label":"CAMT 營業利益率","value":23.15,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAMT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_onto_gross_margin_pct","label":"ONTO 毛利率","value":50.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONTO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_onto_operating_margin_pct","label":"ONTO 營業利益率","value":13.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONTO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_onto_fcf_margin_pct","label":"ONTO FCF 利潤率","value":22.54,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONTO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvmi_gross_margin_pct","label":"NVMI 毛利率","value":57.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVMI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nvmi_operating_margin_pct","label":"NVMI 營業利益率","value":30.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVMI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nvmi_fcf_margin_pct","label":"NVMI FCF 利潤率","value":25.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVMI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_klac_gross_margin_pct","label":"KLAC 毛利率","value":61.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_klac_operating_margin_pct","label":"KLAC 營業利益率","value":42.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_klac_fcf_margin_pct","label":"KLAC FCF 利潤率","value":27.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":97.05,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-52.78,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":30.21,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.63 → 3.63）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.09 → 5.09）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.92 → 5.92）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.63,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":5.09,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":5.92,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.55,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 3.61 → 3.63（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":36.48,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝23.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":23.3,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":8.33,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝59.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":59.7,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":8.12,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝51.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":51.6,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":26.74,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 3.63，分子＝快照價 97.05","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-117.34,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 489.18、現金 606.52（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":46.73,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":4417.34,"period":"2026-11-08","unit":"USD m","basis":"市值 4534.68 ＋ 淨負債 -117.34","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":596.38,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（10 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":804.17,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（10 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":7.41,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 97.05 / W52 147.54 / W104 115.43 / W250 77.86 / W250 13週斜率 1.56%"},{"id":"f_ma_w52","label":"52 週均線","value":147.54,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":115.43,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":77.86,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.56,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"20-F FY2025 風險因素：市場高度競爭，對手有些資源更多；市場成長可能吸引新進入者；另有本地小型競爭者主攻低階市場、以較低價格供貨；競爭可能壓低價格與毛利。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm","excerpt":"The continued growth of the markets in which we operate may attract and result in new market entrants and may also encourage existing competitors to expand their efforts and presence in these markets.","as_of":"2026-03-19","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"20-F 風險因素：另有本地小型競爭者鎖定低階市場並以較低價格供貨。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm","excerpt":"Other competitors are local smaller competitors in the markets we operate, which target the low-end market and may offer products at lower prices.","as_of":"2026-03-19","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q1 2026 財報電話會議：管理層稱維持 3D 凸塊量測領先並在 2D 檢測持續拿更多份額（公司自述）","source":"Camtek Q1 2026 Earnings Call Transcript (Insider Monkey)","url":"https://www.insidermonkey.com/blog/camtek-ltd-nasdaqcamt-q1-2026-earnings-call-transcript-1761058/","excerpt":null,"as_of":"2026-05-12","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q4 2025 財報電話會議：管理層稱未輸給對手份額（公司自述）","source":"Camtek Q4 2025 Earnings Call Transcript (MarketBeat)","url":"https://www.marketbeat.com/earnings/reports/2026-2-18-camtek-ltd-stock/","excerpt":null,"as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2024 20-F：三家客戶各占總營收 15%、10%、10%（客戶集中度資訊；未見第二供應商或自製的揭露）","source":"Camtek Form 20-F FY2024","url":"https://www.sec.gov/Archives/edgar/data/0001109138/000117891325000945/zk2532834.htm","excerpt":"In 2024, three customers accounted for 15%, 10% and 10% of total revenues, respectively.","as_of":"2025-03-31","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 僅一家客戶占營收 11%；2024 年三家客戶占 15%、10%、10%；2023 年一家占 15%。","source":"SEC EDGAR 20-F FY2025 Item 4","url":"https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm","excerpt":"In 2025, one customer accounted for 11% of total revenues. In 2024, three customers accounted for 15%, 10% and 10% of total revenues, respectively. In 2023, one customer accounted for 15% of total revenues.","as_of":"2026-03-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025 年亞太占營收約 91%，其中中國占 49%。","source":"SEC EDGAR 20-F FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm","excerpt":"In 2025, our sales in the Asia Pacific region (mainly China, Taiwan and South Korea) accounted for approximately 91% of our total revenues with sales to China being 49% of our total revenues.","as_of":"2026-03-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SEMI 2026年中預測：全球半導體製造設備OEM銷售2026年約1659億美元(+23.2%)，2028年達2295億美元，連續第五年成長；DRAM設備2027 +27.4%、2028 +15.0%","source":"SEMI press release via Korea JoongAng Daily","url":"https://www.koreajoongangdaily.com/business/global-semiconductor-equipment-sales-forecast-to-hit-record-high-in-2028-on-ai-infrastructure-investment/12783597","excerpt":"Global semiconductor equipment sales are expected to soar 23.2 percent on year to $165.9 billion this year before reaching an all-time high of $229.5 billion in 2028.","as_of":"2026-07-21","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Camtek Q1 2026 法說：兩家HBM客戶下單/預測，3D量測與2D檢測預期2026–2027營收逾2.6億美元，另有時程上行空間","source":"Camtek Q1 2026 earnings call (Insider Monkey transcript)","url":"https://www.insidermonkey.com/blog/camtek-ltd-nasdaqcamt-q1-2026-earnings-call-transcript-1761058/","excerpt":null,"as_of":"2026-05-12","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Camtek進階封裝營收高度依賴HPC及少數chiplet/HBM客戶，客戶減少資本支出或自製會造成衝擊（集中度風險）","source":"Simply Wall St community narrative on Camtek","url":"https://simplywall.st/community/narratives/us/semiconductors/nasdaq-camt/camtek/1jrcrz60-introduction-of-eagle-g5-and-hawk-will-expand-market-opportunities-in-hpc-segment-bfr5","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"20-F（FY2025）揭露：公司不是任何重大法律程序的當事人。","source":"SEC EDGAR 20-F FY2025 Item 8 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm","excerpt":"We are not a party to any material legal proceedings, and there are no material proceeding in which any director, any member of senior management, or any of our affiliates is either a party adverse to us or our subsidiaries or has a material interest adverse to us or our subsidiaries.","as_of":"2026-03-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"20-F 風險因素：公司受以色列經濟競爭法規範，併購或出售全部／實質全部資產時，可能需以色列競爭管理局核准；此為控制權變動的規範，非調查。","source":"SEC EDGAR 20-F FY2025 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm","excerpt":"we are subject to the Israeli Economic Competition Law, 1988 and the regulations promulgated thereunder (formerly known as the Israeli Antitrust Law, 1988), under which we may be required in certain circumstances to obtain the approval of the Israel Competition Authority","as_of":"2026-03-19","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Camtek 20-F 揭露：2025 年亞太區占營收約 91%，中國占 49%；出口管制（含 2022 年 10 月起、2025 年加強的美國商務部規則）可能間接壓低中國半導體設備需求；美國對進口（含中國）加徵關稅帶來不確定性並可能增加成本。","source":"SEC EDGAR 20-F FY2025 Item 3.D Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm","excerpt":"In 2025, our sales in the Asia Pacific region (mainly China, Taiwan and South Korea) accounted for approximately 91% of our total revenues with sales to China being 49% of our total revenues.","as_of":"2026-03-19","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"20-F 指出即使美國出口管制不直接適用，也可能影響需求；若有美國連結（含美國原產成分、美國受控技術），非美國公司亦可能受管制。","source":"SEC EDGAR 20-F FY2025 Item 3.D Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm","excerpt":"Even where U.S. and other global export controls do not apply to our products, they may impact the demand for our products.","as_of":"2026-03-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"搜尋未發現 Camtek 被列入 Entity List 或遭 BIS 執法的報導；Camtek 新聞稿的前瞻聲明列有 entity list 變動為風險項。","source":"WebSearch 摘要（Camtek Q1 2026 results 相關）","url":"https://www.daytraders.com/news/2026/05/12/camtek-announces-results-for-the-first-quarter-of-2026","excerpt":null,"as_of":"2026-05-12","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Q1 2026 財報電話會議報導：Camtek 以色列設施在中東局勢困難下照常運作，未曾錯過出貨；主要製造與研發在以色列 Migdal Haemek，並在歐洲擴充產能作為對沖","source":"MarketBeat, Camtek Q1 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/camtek-q1-earnings-call-highlights-2026-05-12/","excerpt":null,"as_of":"2026-05-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"20-F（FY2020 版，較舊）揭露依賴單一／有限來源供應商與分包商（Key Suppliers）提供關鍵零組件與子系統","source":"Camtek Form 20-F FY2020 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1109138/000117891321001065/camt20f1220.htm","excerpt":"Camtek relies on single source and limited source suppliers and subcontractors (\"Key Suppliers\") for a number of essential components and subsystems of its products.","as_of":"2021-03-31","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Q2 2026 財報電話會議摘要：管理層預期中國占 2026 年營收約 45%（前一年 49%）","source":"MarketBeat, Camtek Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/camtek-q2-earnings-call-highlights-2026-08-10/","excerpt":"Management said China business has remained stable over the past several years and expects revenue from China to account for roughly 45% of total revenue in 2026, compared with 49% in the prior year.","as_of":"2026-08-10","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Simply Wall St 敘事指亞洲市場與客戶集中帶來地緣風險","source":"Simply Wall St narrative","url":"https://simplywall.st/community/narratives/us/semiconductors/nasdaq-camt/camtek/expanding-high-performance-computing-demand-will-shape-future-success-in-generative-ai","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收指引 $158–160M（季增約 20%），管理層預期 2026 下半年較上半年成長逾 30%，2027 持續成長","source":"Camtek Q2 2026 results / earnings call summaries (MarketBeat, Quartr)","url":"https://www.marketbeat.com/instant-alerts/camtek-q2-earnings-call-highlights-2026-08-10/","excerpt":"Q3 2026 revenue guidance: $158–$160 million, a 20% sequential increase over Q2.","as_of":"2026-08-10","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 營收 $133.2M，年增 8%；兩家 HBM 客戶的 3D 量測與 2D 檢測訂單／預測，2026–2027 預期營收逾 $260M","source":"Camtek Form 6-K / Q2 2026 summaries","url":"https://www.sec.gov/Archives/edgar/data/0001109138/000117891326003975/zk2635905.htm","excerpt":null,"as_of":"2026-08-10","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 財報後指引：2026 全年營收約 $595M（約年增 20%），2027 初步展望逾 $800M；年初至今訂單逾 $800M，主要為 AI 先進封裝，客戶預訂交期至 2027","source":"Panabee: Camtek's $800 Million YTD Orders Propel 2027 Revenue Outlook","url":"https://www.panabee.com/news/camtek-earnings-q3-2026","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"先進封裝預計年底約占營收 80%；可服務市場 2027 年達 $2B 以上（較目前增約 $500M）；混合鍵合 2027 貢獻有限，2028 起較有意義；需求擴及化合物半導體、CIS、RF。此為二手摘要","source":"MarketBeat Camtek Q3 earnings call highlights (2026-11-04) / Q2 call summary","url":"https://www.marketbeat.com/instant-alerts/transcript-camtek-q3-earnings-call-highlights-2026-11-04/","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"SEMI 2026 年中預測：全球半導體設備 OEM 銷售 2026 年 $165.9B（年增 23.2%），2028 年 $229.5B；DRAM 設備 2026 年 +39.0%、2027 年 +27.4%（未直接驗證 SEMI 原稿）","source":"SEMI mid-year forecast (via search summary)","url":"https://semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Camtek 20-F 風險因素自述：市場技術變動快，若未能預測或跟上技術變化或競爭對手產品，營收可能受損；採用新技術也可能造成存貨沖銷。未點名特定替代技術。","source":"SEC EDGAR 20-F FY2025 Item 3.D Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm","excerpt":"If we fail to anticipate correctly, or if we are unable to keep pace with, technological changes, products offered by our competitors or emerging industry standards, our ability to generate revenues may be negatively affected. Adopting new technologies may also result in material inventory write-offs which would adversely affect our results of operations.","as_of":"2026-03-19","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"APCNDT 2026 摘要（Applied Materials）描述以 3D X-ray CT 與 laminography 檢查 hybrid bonding 界面、對位偏差與空洞，為光學檢測以外的技術路線","source":"APCNDT 2026 abstract (airdrive.eventsair.com)","url":"https://airdrive.eventsair.com/eventsairsthcusprod/production-asnt-public/3f130c65daf8432ba7f874e076dd232d","excerpt":"semiconductor industry. Keywords: X-Ray Computed Tomography, X-Ray Computed Laminography, Semiconductor, 3D Inspection INTRODUCTION The continued scaling of semiconductor packaging toward fine-pitch and three-dimensional integration architectures, such as hybrid bonding, chiplet integration, and advanced wafer-level packaging, has","as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Yole 2026 檢測量測報告：hybrid bonding 與 panel-level packaging 增加關鍵控制點，並朝多技術／混合量測轉移","source":"Yole Group Metrology & Inspection Equipment 2026","url":"https://www.yolegroup.com/product/report/metrology--inspection-equipment-2026/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Camtek 收購 Visual Layer，表示有機會建立 AI 軟體與分析產品，長期可能帶來額外的經常性收入來源","source":"iconnect007: Camtek acquires Visual Layer","url":"https://iconnect007.com/article/149701/camtek-acquires-visual-layer-to-strengthen-visual-ai-capabilities-in-inspection-and-metrology/149698/aep","excerpt":"We also see a meaningful opportunity and potential beyond our core business to build AI-driven software and analytics offerings that could, over time, open an additional and recurring revenue stream for Camtek.”","as_of":"2026-04-21","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 2026 法說會分析師詢問 Visual Layer AI 軟體包賣給裝機基礎，會認列為經常性訂閱收入還是一次性升級授權","source":"MarketBeat: Camtek Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/camtek-q2-earnings-call-highlights-2026-08-10/","excerpt":null,"as_of":"2026-08-10","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Camtek 2026-10-14 預告：Q3 營收高於指引區間，全年 2026 營收指引約 $595M、Q4 指引約 $180M、2027 初步展望 >$800M；搜尋摘要稱全年指引與共識（約 $594.3M）大致相符、Q4 略高於共識（約 $179.2M）","source":"PRNewswire / Webull：Camtek pre-announces record Q3 revenues above guidance","url":"https://www.prnewswire.com/il/news-releases/camtek-pre-announces-record-q3-revenues-above-guidance-provides-record-q4-guidance-and-initial-revenue-outlook-for-2027-302908515.html","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-10 Q3 指引上調至 $158–160M（前一區間 $129–131M 為 Q2 指引）；Benzinga 統計自 2022-11 起 17 次指引更新，13 次上調、2 次下調；2026 年未見下調","source":"搜尋摘要（Benzinga 統計，Camtek Q2 2026 結果）","url":"https://www.benzinga.com/quote/CAMT/earnings-forecasts","excerpt":null,"as_of":"2026-08-10","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價：Walnut Invest 2026-08 為 12 位分析師均值 $187.58、中位 $187.50、區間 $160–$220；TickFlow 2026-07-31 為 14 位均值 $178.56；MarketBeat 5 月均值約 $174.33、後續 $174.67（7 Buy / 7 Hold）；Benzinga 約 $157.21（14 位，高 $200 低 $80，日期不明）；各來源 as-of 與分析師數不一致","source":"Walnut Invest / TickFlow / MarketBeat / Benzinga 聚合頁","url":"https://walnutinvest.com/stocks/camt/forecast","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"賣方目標價有雙向調整：2026-05 Jefferies、Evercore 調升至 $200；2026-08-10 Stifel 調降至 $170（Q2 營收 $133.2M 後）；Stifel 4 月曾降至 Hold","source":"StreetInsider / Financial Modeling Prep","url":"https://site.financialmodelingprep.com/market-news/camtek-camt-q2-revenue-ai-driven-growth-price-target-update","excerpt":null,"as_of":"2026-08-10","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"某聚合頁列 FY2026 EPS 共識 $3.70（15 位分析師，2026-10-31）","source":"Benzinga earnings-forecasts 聚合頁","url":"https://www.benzinga.com/quote/CAMT/earnings-forecasts","excerpt":null,"as_of":"2026-10-31","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Camtek 2026-04-14 宣布簽署definitive agreement收購特拉維夫AI公司Visual Layer，金額未揭露，預計數週內交割；搜尋未見交割公告。","source":"iconnect007：Camtek Acquires Visual Layer to Strengthen Visual AI Capabilities in Inspection and Metrology","url":"https://iconnect007.com/article/149701/camtek-acquires-visual-layer-to-strengthen-visual-ai-capabilities-in-inspection-and-metrology/149698/design","excerpt":null,"as_of":"2026-04-14","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 20-F：公司非任何重大法律程序當事人。","source":"SEC EDGAR 20-F FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm","excerpt":"We are not a party to any material legal proceedings, and there are no material proceeding in which any director, any member of senior management, or any of our affiliates is either a party adverse to us or our subsidiaries or has a material interest adverse to us or our subsidiaries.","as_of":"2026-03-19","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Camtek 2026-04-14 宣布簽署definitive agreement收購特拉維夫AI公司Visual Layer，金額未揭露，預計數週內交割；搜尋未見交割公告。","source":"iconnect007：Camtek Acquires Visual Layer to Strengthen Visual AI Capabilities in Inspection and Metrology","url":"https://iconnect007.com/article/149701/camtek-acquires-visual-layer-to-strengthen-visual-ai-capabilities-in-inspection-and-metrology/149698/design","excerpt":null,"as_of":"2026-04-14","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 20-F：非任何重大法律程序當事人；過去曾有一起證券集體訴訟，已被駁回。","source":"SEC EDGAR 20-F FY2025 Item 8 / Item 3","url":"https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm","excerpt":"We are not a party to any material legal proceedings, and there are no material proceeding in which any director, any member of senior management, or any of our affiliates is either a party adverse to us or our subsidiaries or has a material interest adverse to us or our subsidiaries.","as_of":"2026-03-19","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"CAMT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.03,"operating_margin_pct":23.15,"fcf_margin_pct":null,"rd_intensity_pct":11.39},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAMT","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"ONTO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.36,"operating_margin_pct":13.81,"fcf_margin_pct":22.54,"rd_intensity_pct":12.73},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONTO","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"NVMI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.38,"operating_margin_pct":30.04,"fcf_margin_pct":25.44,"rd_intensity_pct":15.64},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVMI","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"KLAC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":61.47,"operating_margin_pct":42.64,"fcf_margin_pct":27.83,"rd_intensity_pct":10.8},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"CAMT"},"financial_history":{"ticker":"CAMT","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":320909000.0,"revenue_yoy_pct":null,"gross_margin_pct":49.81,"operating_margin_pct":25.4,"net_income":79949000.0,"diluted_eps":1.66,"free_cash_flow":49505000.0,"fcf_margin_pct":15.43,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":315375000.0,"revenue_yoy_pct":-1.72,"gross_margin_pct":46.81,"operating_margin_pct":20.74,"net_income":78632000.0,"diluted_eps":1.61,"free_cash_flow":71054000.0,"fcf_margin_pct":22.53,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":429234000.0,"revenue_yoy_pct":36.1,"gross_margin_pct":48.91,"operating_margin_pct":25.18,"net_income":118515000.0,"diluted_eps":2.42,"free_cash_flow":111876000.0,"fcf_margin_pct":26.06,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":496072000.0,"revenue_yoy_pct":15.57,"gross_margin_pct":50.46,"operating_margin_pct":25.84,"net_income":50722000.0,"diluted_eps":1.04,"free_cash_flow":127072000.0,"fcf_margin_pct":25.62,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CAMT/CAMT_Q3_2026_Earnings_Call_20261104.md）

# Q3 2026 Earnings Call
**Camtek Ltd.** | Earnings Calls | 2026-11-04

**Kenny Green** (Attendees):
Ladies and gentlemen, thank you for standing by. I would like to welcome all of you to Camtek's results Zoom webinar. My name is Kenny Green, and I'm part of the Investor Relations team at Camtek. [Operator Instructions] Following the formal presentation, I will provide some instructions for participating in the live question-and-answer session. I would like to remind everyone that this conference call is being recorded, and the recording will be available from the link in the earnings press release and on Camtek's website from tomorrow. You should have all received by now the company's press release. If not, please view it on the company's website. With me today on the call, we have Mr. Rafi Amit, CEO; Mr. Moshe Eisenberg, CFO; and Mr. Ramy Langer, COO.
Before we begin, I'd like to remind you that the statements made by management on this call will contain forward-looking statements within the meaning of the federal securities laws. Those statements are subject to a range of changes, risks and uncertainties that can cause actual results to vary materially. 
For more information regarding the risk factors that may impact Camtek's results, please review Camtek's earnings release and SEC filings and specifically the forward-looking statements and risk factors identified in the results press release issued earlier today and such other factors discussed in Camtek's most recent annual report on SEC Form 20-F. Camtek does not undertake the obligation to update these forward-looking statements in light of new information or future events. 
Today's discussion of the financial results will be presented on a non-GAAP financial basis unless otherwise specified. As a reminder, a detailed reconciliation between GAAP and non-GAAP financial results can be found in today's earnings release. 
And now I'd like to hand the call over to Mr. Rafi Amit, Camtek's CEO. Rafi, please go ahead.

**Rafi Amit** (Executives):
Hello, everyone, and thank you for joining us today. Just 3 weeks ago, many of you joined us at our investors and analyst breakfast event at SEMICON West, where we shared our growth strategy, technology road map and new financial targets. With that in mind, I will keep my remarks brief today. 
I will start with a review of our third quarter results, followed by a brief recap of the key messages from this event. 
The third quarter marked another record quarter for Camtek with revenue reaching $161.3 million, exceeding our guidance and representing 28% year-over-year growth and 21% sequential growth. Operating income also reached a record $47.5 million with operating margin expanding to 29.5% compared with 27% in second quarter. These results highlight the strong operating leverage of our business model as robust revenue growth translated into even greater growth in operating profitability. 
Approximately 80% of our revenue was generated from advanced packaging applications. The majority of which were driven by AI-related demand. Our new generation platform, the Eagle G5 and Hawk accounted for approximately 57% of our system's revenue, and we expect their contribution to continue growing as customer adoption expands. Order momentum remained exceptionally strong. As we shared at our recent investor and analyst breakfast event less than a month ago, we had received more than $800 million in order since the beginning of year until that date. And the strong order momentum has continued since then. Approximately 80% of this order were related to advanced packaging applications, nearly all of which are high-end applications driven by AI demand. 
OSATs accounted for slightly more than 50% of total orders, reflecting their increasingly important role in the advanced packaging ecosystem. Importantly, for the past several months, many of our customers have been securing delivery slots through 2027, providing us with strong visibility into sustained demand and continued growth. We have seen this trend in all territories, including China, and we expect this strength in all regions to continue in 2027. 
For the first time in Camtek history, we have visibility extending approximately 1 year ahead. This gives us greater confidence in our growth outlook. Looking ahead, we expect fourth quarter revenue of approximately $180 million, bringing our full year 2026 revenue to approximately $595 million. For 2027, we expect revenue to exceed $800 million, supported by our strong order backlog and sales pipeline. Moshe will provide more details on our financial outlook in a few minutes. 
Let us briefly recap the key messages from our Investor and Analyst Day. First, we operate in an exceptionally strong growth market, advanced packaging, which is our core business, this market is growing faster than the overall semiconductor industry, while high-end advanced packaging for AI application is growing at an even faster pace. Second, increasing complexity creates new opportunities for Camtek. AI as advanced packaging becomes more complex, it requires more inspection and metrology steps as well as new tools with more advanced capabilities. 
Third, we have a clear competitive advantages. Our advanced technology, combined with an installed base of approximately 4,000 systems and strong long-standing relationships with all leading customers put us in excellent position to continue gaining market share. Looking ahead to 2027, we plan to introduce new AI-based software products, creating an additional revenue stream for Camtek and further strengthening our competitive advantages. Fourth, we are ready to scale. Together with our manufacturing partner, who have already expanded their production capacity, we have strengthened our operational infrastructure to support significantly higher revenue level. 
In the near term, like the rest of the industry, we are experiencing certain supply chain challenges involving a limited number of suppliers. We are working closely with this supplier to address the challenges and expect to meet our customer delivery schedule. All of this supports our new long-term target to double our 2026 revenue and reach $1.2 billion in annual revenue within approximately 3 years. Importantly, this target is based on organic growth without factoring in new potential contribution from substantial M&A. We recognize that this is an ambitious target, but we believe we have the right strategy, strong market opportunities and the capability to achieve it, assuming the continued trend of our industry. We are fully committed to this goal and are working hard to turn it into reality. 
And now Moshe will review the financial results. Moshe?

**Moshe Eisenberg** (Executives):
Thanks, Rafi. In my financial summary, I will provide the results on a non-GAAP basis. A reconciliation between the GAAP results and the non-GAAP results appear in the table at the end of the press release issued earlier today. Third quarter revenues came in at a record level of $161.3 million, a 28% increase year-over-year and 21% increase compared with the second quarter of 2026. 
The geographic revenue split for the quarter was as follows: Asia accounted for 95% and the rest of the world, 5%. Gross profit for the quarter was $82.3 million. The gross margin for the quarter was 51.1%, similar to the 51.4% in the previous quarter. 
Gross margin came in a bit lower than our expectations. As Rafi mentioned, there is an industry-wide supply chain demand, which has not only created operational challenges, but also resulted in price pressure on parts, components and material used in our system, affecting our COGS. We have already started to increase our ASPs, and we expect this to positively impact our gross margin already in 2027. Further improvement is expected by higher share of our more advanced offering and by offering new software products. 
Operating expenses in the quarter were $34.8 million compared with $32.5 million in the previous quarter. Most of the increase in operating expenses was in selling and marketing, in line with the higher revenue level. Our operating profit in the quarter reached a record $47.5 million compared with $36 million in the second quarter and $37.6 million in the third quarter of last year. Operating margin was 29.5%, up from 27% in the second quarter, reflecting the leverage we have in our model. 
Financial income for the quarter was $7.1 million compared with $7 million in the previous quarter. Net income for the third quarter of 2026 was a record $50.3 million or $0.99 per diluted share. This is compared with net income of $39.4 million or $0.78 per diluted share in the previous quarter. The total diluted number of shares as of the end of the third quarter was $51.5 million. 
Turning to some high-level balance sheet and cash flow metrics. Cash and cash equivalents, including short and long-term deposits and marketable securities as of September 30, 2026, were $877.1 million. We generated $71.1 million in cash from operations in the quarter. Accounts receivable increased to $166.2 million compared to $153.9 million in the previous quarter. DSO remained at similar levels of around 90 days. 
Now to the outlook. For the fourth quarter of 2026, we expect revenues of approximately $180 million, up 40% year-over-year. This will bring our full year 2026 revenues to approximately $595 million, representing growth of about 20% over 2025. 
For 2027, based on our backlog pipeline and strong order momentum, our initial revenue outlook is more than $800 million. Let me briefly remind you of our new target model. We are targeting $1.2 billion of revenues within about 3 years, substantially organic with operating margin of 34% to 36%. And with that, Rafi, Ramy and I will be open to take your questions. Kenny?

**Kenny Green** (Attendees):
Thank you, Moshe. We'll now open the line for question and answers. [Operator Instructions] And we will take our first question from Matt Prisco of Cantor Fitzgerald.

**Matthew Prisco** (Analysts):
I guess first on gross margins. I'd just love to hear where we're tracking in 4Q. And then as we move into '27, can you perhaps walk us through the levers as we just think about those cost increases, the pricing increases, the new product mix, higher volumes, a lot of moving parts there. So can you help us just kind of walk through those?

**Moshe Eisenberg** (Executives):
Absolutely, Matt. So first of all, indeed, we were a bit disappointed by the gross margin level, although we did implement cost reduction initiatives during the quarter, which will benefit us in the future as well. On the same time, the product mix is also working in our benefit and our favor, and this will continue to favor us in the future as well. What happened this quarter was slightly higher parts and material costs that offset some of these benefits that will remain with us in the future. Now our plan is, obviously, and this is already in motion is to increase overall ASPs in the market. And with -- together with the software offering that brings to the table, and we plan to improve the gross margin already in 2027. 
Keep in mind also that over the last few quarters, the exchange rate also was not benefiting our business activities. The shekel got much stronger against the U.S. dollar, which was slightly an overhang on the COGS cost structure overall and also in the COGS level. So this is not something that this is definitely beyond our control, and we hope that next year, this will balance out. Did I answer your question, Matt?

**Matthew Prisco** (Analysts):
That's perfect. And then as a follow-up, just can you give us an update on where orders stand today? Any particular areas of strength across markets or systems you would highlight? And then as we think about that '27 outlook, how much of that is supported by backlog today? And how much upside is there given supply and component issues and all those things?

**Ramy Langer** (Executives):
So Matt, this is Ramy. So first of all, we are talking about an initial outlook of over $800 million and definitely, I think we cannot give more information at this stage. We said in our prepared notes and when we met in October that the backlog is significant. And I think this is as far as we can go. From the color, to give you some color on the backlog and what we see in those $800 million, definitely, we see a very strong, as we said, over 50% came from the OSATs, an area that we have a very strong position. About 80% is coming from advanced packaging. So all in all, our main segment is healthy, and we maintain a good market position. And I think all in all, all the trajectories are up, and we feel very comfortable with these numbers.

**Kenny Green** (Attendees):
Our next question will be from Brian Chin of Stifel.

**Brian Chin** (Analysts):
Maybe first, just a follow-up on the order commentary. I guess, one, to clarify, it seemed based on that last comment from Ramy, a little bit more of a skew towards AI logic relative to HBM in terms of the booking. And also, as you look into Q4 and really in the second half, based on sort of where lead times are for equipment, are you booking more towards maybe kind of midyear next year, maybe even second half '27?

**Ramy Langer** (Executives):
So first of all, we are booking already the second half. And as we said, we have a very good visibility 1 year ahead of us. So this is indeed the case. And I would say, as a follow-up from where our discussion, definitely, the business is strong across the different regions, including China.

**Brian Chin** (Analysts):
Okay. Great. I had a question about software. I know that was one of the interesting topics from the Analyst Day a few weeks ago. I believe you mentioned this revenue stream could increase from sort of tens of millions per year to well over $100 million in that kind of 3-year target model. A few questions there. When you think about your 35% initial revenue growth outlook for '27, do you attribute maybe a few percentage points of that growth to software in terms of some of these new products? And then just kind of thinking forward, is the idea here that you envision some of this AI-related and defect classification software to be effectively bundled with future shipments of Hawk or Gen 5 Eagles?

**Ramy Langer** (Executives):
So let me, first of all, correct you. When we talked about the figure, it included software and service. Service is growing very fast at a rate of about 35% a year and has been growing in this respect at this rate for the past few years, and we see it continuing to grow as a result of the much larger installed base and our customers requiring more and more support as the machines are becoming more and more complex. And this is one leg of the growth. 
The second growth will come from software. And I think we have said in the past and the acquisition of Visual Layer, which brought us a lot of capabilities on AI, but in parallel, it is a platform to develop products that we expect to start to sell in '27. And I hope that even we'll see initial revenues in the first quarter of '27. So definitely, combination of the software and the service is going to start to be significant already in '27, and we expect to reach the numbers, as we said, in the 3-year target.

**Kenny Green** (Attendees):
Our next question will be from Charles Shi of Needham.

**Charles Shi** (Analysts):
I want to follow up on the supply chain challenges. We obviously have seen some of that impact in the reported quarter gross margin. But can you provide a little bit of background on what specific components are in shortage and is it something more specific to, let's say, your tools, optics, light sources or maybe it's just some simple things like PCBs or even memory components, et cetera. So I want to get some thoughts on what exactly is in short right now and for us to get some sense on for how long do you think the shortage situation will last and when the supply can catch up and no longer being an issue going forward?

**Ramy Langer** (Executives):
So thank you, Charles. So let me try and elaborate a little bit more. So first of all, these are not specific parts that are made for Camtek. These are general wide industry components. I think you mentioned memories and CPUs that's definitely today in shortage and the prices are higher. This is not something new to anyone. And there are other general purpose components that are in shortage mainly on the handling part of the machine -- and we are working, one, with our vendors. In most cases, we have dual sources. So this is really a question how to balance between the different sources, make the first source less and bring in the second source. These are things that are in motion. And I expect these topics to be resolved, I would say, within 3 to 6 months, I think it will balance off. But this is really my feeling. We're not sure about it. But I think we said in the prepared notes that we will not miss any delivery schedules. We are doing every effort and working very closely with the vendors to keep our plan in place.

**Charles Shi** (Analysts):
Got it. Maybe a second question. Maybe more on the advanced packaging, especially AI-related advanced packaging outlook between 2.5D and the HBM. We know there are some unique situation on the 2.5D side, maybe just a '27 issue, maybe going to '28, not really an issue. But on the HBM side, what are you seeing today? Because since the SEMICON West event, a few of the packaging, especially the foundry companies reported at least there's one thermal compression bonding company saying they are seeing some TCB delays for HBM packaging build-out. Wondering what you're seeing there? Maybe you are seeing some offsetting factor, maybe that's not that good to read through to Camtek, but I wonder if you can address those issues that have been -- that has been discussed for a couple of weeks among the investment community.

**Ramy Langer** (Executives):
So we -- I'm trying to think about your question, but we do not see any change to our plans or predictions. I think we are on track with all the customers in the HBM area. So I cannot bring you any more information or anything new based on your question.

**Kenny Green** (Attendees):
Our next question will come from Michael Mani from Bank of America.

**Michael Mani** (Analysts):
To start, nice to see that Hawk and Eagle G5 are more than 55% of sales at this point of the year. If you were to kind of reflect back on the last couple of quarters, were there any areas where maybe your share gain or traction in those new categories progressed faster or better than expected? And what does that tell you about where -- about your confidence level in where you can potentially gain share next year in 2027 to deliver upside to that $800 million full view that you gave a couple of weeks ago?

**Ramy Langer** (Executives):
So first of all, indeed, the position in the market continues to be strong. Talking about share in '27 and gaining share, it's a little bit too early. As I said previously, it's really an initial outlook when we talk about '27. And I think it's too early to talk about gains. I think that we are performing very well with our customers as we see it. I think we will definitely maintain position. I also hope that we will gain share, but it's too early to say in which areas.

**Michael Mani** (Analysts):
Got it. And for my follow-up, I just wanted to ask about the OSAT market. I know this has come up repeatedly, but in the last few months, we've heard your peers become more vocal about being able to enter the space. Obviously, Camtek has had a very established position there for a long time and has seemed to defend that for the most part, pretty well. But when you were to look at each of the different players that are sort of like participating now, whether it is the local Chinese suppliers who are looking to displace incumbents to take share, whether it's the smaller process control peers in your ecosystem, whether it's KLA, what do you think is the Camtek value prop against each of those different competitors? Like why do you think your moat is intact from each of those players? 
And when you think about why more competition is coming to the space, do you think it's more of a fact that your customers are looking for multi-sourcing away from Camtek or is it more just secure a very sort of temporary shortage situation in that market because there simply isn't enough capacity out there to address all the demand?

**Ramy Langer** (Executives):
All right. So let me, first of all, address the competitive situation of many Chinese players. We do not see any competitive threat from those small competitors in China. We maintain a very strong position, and we expect -- if we talk about share gain, we definitely think that China is a place that we can continue and gain share. So this, I would say, about the lower end competition. And I think when you talk about from the other side that you see the bigger players that are trying to enter the market. And I think this is something that we have seen. I think the market is becoming lucrative and growing. So definitely, people are thinking of maybe we can get some share. This is natural. We never expect that it will be different. But I think when I look at our products, the competitiveness our responsiveness as a company. The products were designed for customization for the dynamic advanced packaging market that is very, very important. We hold a dominant position at the OSAT market, and I think will be very difficult for the larger players to enter. 
And I think what is very important is that we have a proven portfolio with dedicated solutions for the advanced packaging. This includes our metrology where we hold a phenomenal market share, includes things like flexible handling, fluorescence inspection, and we can continue and talk about it. And when you think about it, the larger players do not necessarily have all of these capabilities, and it takes a lot of time to develop it while we are developing new and other capabilities that are required. And all in all, when you talk about the larger players, I think we discussed it in previous meeting, they are bigger than us. But in the specific market that we play, we are significantly larger.

**Moshe Eisenberg** (Executives):
I just want to add one point, Michael, regarding the Chinese market and the potential domestic competition. I would say that in the last few months, we received -- we enjoyed a nice order momentum across the board and specifically in China. When I look today in our backlog for '27, China will represent a meaningful piece of our business, at least as high as this year. So I think that the competition in China does not play a major role in our business at the moment.

**Kenny Green** (Attendees):
Our next question will be from Jim Schneider of Goldman Sachs.

**James Schneider** (Analysts):
I just wonder if you could maybe, as we think about 2027, help us with how you see the linearity of 2027 playing out. Obviously, you have much better visibility into the first half than the second, as you mentioned. But should we think about sort of like sequential step-up in revenue in the first couple of quarters of the first half and then flattening out in the back half or maybe any help on that would be helpful.

**Ramy Langer** (Executives):
So trying to look at and as I said, it's really an initial outlook. And I think the business will be stable. We are starting to fill the shipments, the capacity as we speak. And as I said, we're already booking a lot of orders for the second half of '27. So at least when I look at it, I think it will be stable. But it's initially, I would say, balanced capacity growth over the fourth quarter. But definitely, we are in a very good situation, which we're actually seeing already slots in the second half.

**James Schneider** (Analysts):
And then can you maybe talk about the gross margin profile? I mean, obviously, you have mix in your favor. At the same time, you talked about the input cost headwinds. So can gross margins start to improve further as we get into the back half or is it too early to call on that?

**Moshe Eisenberg** (Executives):
Yes. So the expectation is that gross margin will gradually improve starting from the first quarter of '27. And again, as I said before, it's a combination of the cost reduction initiatives that are already in place, the favorable product mix that we have, as you saw, already 55% -- over 55% of our revenues are related to the high-end products, which carry higher gross margin. And I believe that this short-term supply chain constraints will be balanced out off. 
So starting from Q1, we will see a gradual improvement. Together, by the way, with the contribution of the software and the service business that is starting to pick up. And Ramy mentioned that we are already looking to see some initial software business in the first quarter. So gross margin bottom line is expected to gradually improve starting from Q1 '27.

**Kenny Green** (Attendees):
Our next question is from Ed Yang of Oppenheimer.

**Ed Yang** (Analysts):
The first one is, can you size the ASP increase you're contemplating? And maybe talk about the initial customer receptivity to that? And was that always embedded in your $800 million revenue view or is that incremental?

**Ramy Langer** (Executives):
So I don't think we can say now whether it will be incremental or included. It's really too early. But let me talk about resin prices. So there are 2 aspects here. First of all, we understand and I think our customers understand that due to the increase in prices of components, there will be some increase in the ASPs. So I think this is understood and this is starting -- we're starting to implement it. And this will, I think, will gain momentum in the next quarter. 
Second aspect is implementing new capabilities into our machines. And definitely, this is the area where we can explain to our customers and our customers are receptive to pay more for more capabilities on our machines. So we are working on both fronts, raising some due to the increase in prices, our own prices, but I think on a greater scale, adding the new capabilities, the new developments that we are implementing in our machines, a reason for additional price increase. And these are the 2 things that we are going to do during 2027. And actually, we've already started it this year, but it will gain momentum in 2027. And whether this will be in the 800 initial outlook or not, it's too early to say. I do hope that there is some upside to these numbers as we go more into next year, but this is something that still yet to be seen.

**Ed Yang** (Analysts):
Okay. And for my follow-up, we're starting to see some demand headwinds in consumer and non-AI electronics. And could you just remind us, do you have any exposure there? I know in the advanced packaging bucket of your business, there is a piece, primarily mobile, I think, that's not high-performance computing related. But are you seeing any similar softness in that line item?

**Ramy Langer** (Executives):
No, we do not see any softening. Yes, there is some piece when we talk about the conventional advanced packaging, which is anywhere in the range of, I would say, 15% in average per quarter. But no, no, we don't see any headwinds not at this stage.

**Kenny Green** (Attendees):
Our next question will be from Craig Ellis of B. Riley.

**Craig Ellis** (Analysts):
I wanted to ask a few to better understand what we're seeing in our calendar year 2027 outlook. I know at our analyst breakfast at SEMICON West, we talked a lot about hybrid bonding. The question, is hybrid bonding material in that $800 million outlook for '27 or is it really an opportunity that the company sees filling in 3 years down the road when we're looking for $1.2 billion?

**Ramy Langer** (Executives):
So the hybrid bonding, there is a lot of development today being done -- so yes, we are seeing some business, but really on a low magnitude at this stage. I believe that this is business that will start to materialize more in the '28 and onwards. I think in '27, I don't expect to see any substantial business coming from hybrid bonding. But as we said in the previous meeting, definitely, we have a road map to address this market, and we believe that this is an opportunity for us.

**Craig Ellis** (Analysts):
Got it. And sticking with what's potentially in '27 and where there's additional opportunity beyond the orders that you have in hand now, if we were to categorize potential incremental business as either A; custom ASICs or XPUs, B; work from semiconductor companies with specific GPU and similar programs or 3, HBM, where do you think there's the most opportunity from what you have in hand today to add to orders for next year?

**Ramy Langer** (Executives):
I think the main opportunity for us is to gain market share in 2D for additional steps. So this is not really specific that I can tell you whether it's a GPU or HBM or it's very hard for me from the top of my head to try and assess it. But definitely, I think that we discussed it, we have a strong portfolio for 2D inspection, but still, I think there is a lot more business that we can gain there, and we are putting a lot of focus in this area. And I believe if there is upside potential, it will probably come from this area.

**Craig Ellis** (Analysts):
And when do you think you might be able to convert that pipeline activity to orders? Is that something that you see progressing through the fourth quarter or are these longer-term engagements that might convert 1 half or midyear next year?

**Ramy Langer** (Executives):
So first of all, I think we said in the prepared notes, and Moshe also mentioned that the order momentum continues. So at this stage, what we are seeing from our customers are ordering and really securing deliveries next year. And I think this is -- if I would try to put some color on the kind of business that we are, it's really getting and securing slots in 2027. And I think this we will see until the end of this year. And I think new upsides, if there will be, I think this we will see in the first and second half of 2027.

**Kenny Green** (Attendees):
Our next question will be from Shane Brett of Morgan Stanley.

**Shane Brett** (Analysts):
My first question is on services. I want to ask Brian's early question on software in a different way. If I think about the bridge from your service revenue this year of about $40 million to your $140 million target in 3 years, just how much new software revenue are we adding into the model? And apologies if you've mentioned this previously, but how much software revenue do we have this year?

**Moshe Eisenberg** (Executives):
Let me start, Ramy. So our service business, as you indicated, is around $40 million this year. It's growing at a rate of 35% to 40% annually. So within 3 years, we will be able to reach around $100 million of service revenues from the existing business together with obviously with the installed base that will get bigger. Additional $40 million was assumed with new software offering. At this point, we have pretty much 0 software offerings. This will start in next year in 2027 already in the first quarter and should gain momentum. We believe that there is potential upside to the $40 million that we've mentioned.

**Ramy Langer** (Executives):
And I would like to add that we see the software business is going to already be significant next year and expecting double-digit revenues in 2027, and this business has the potential to grow. We have the platform, the capabilities. We already have some products in the pipeline that we started to introduce to customers, and I expect to gain momentum in this area starting in the first quarter of 2027.

**Shane Brett** (Analysts):
Got it. That's really encouraging to hear. For my follow-up, so your comments on your 3D bump metrology inspection, 3D bump metrology portfolio for HBM from your investor breakfast, is very convincing. But just could you help us quantify how much of your HPC revenue will be coming from HBM this year? And is that mix within HPC, sorry, HBM mix within HPC going to go higher or lower for you next year?

**Ramy Langer** (Executives):
I'm telling what the last numbers that we mentioned. I think at the time that we mentioned and it was 2 quarters ago that we said that we received $600 million in orders since the beginning of the year. And we said that the HBM was over 20%. So it's going to be significant, and we didn't continue to add it because the order flow on what we call the high-performance computing, OS and CoWoS-related applications, we -- they don't come together. It's different streams of orders. I expect that the HBM business, both for inspection and 3D metrology will be significant in 2027. I cannot comment at this stage on exactly the magnitude.

**Kenny Green** (Attendees):
Our next question will be from Vedvati Shrotre of Evercore.

**Vedvati Shrotre** (Analysts):
So the first one I had was, as we go into 2027, you're seeing the order momentum. But at the same time, you're seeing some of the component supply chain constraints creep in. Can you talk about the lead times and how the lead times for your tools have changed? Have they started to stretch now versus last quarter?

**Ramy Langer** (Executives):
I think these are 2 separate issues. First of all, the components issue, it's more, I would say, of a tactical issue that some of our vendors are just -- don't have enough capacity, and we need to use second sources and to overcome, and this is a short term. I expect this will be for 1 or 2 quarters, maybe it will be longer, but I'm expecting us to resolve this situation specifically. And I think Rafi said it in his prepared notes. And I think in general, because of the level of orders intake, definitely, our lead times are increasing. And typically, they are 3 to 6 months. But in some cases, customers are willing to give us today orders a year ahead. And this is not that they necessarily need the machines today. They just want to secure capacity on our floor for the time that there are clean rooms or whatever they need, they want to secure this capacity, and that's the reason that they are already placing orders today.

**Vedvati Shrotre** (Analysts):
Understand. And then for my second question, you mentioned Eagle and Hawk is more -- the Eagle G5 and Hawk is more than 55% of revenues this year. What happens next year? Does that become a majority? Like is that 80% and up? Is that a good estimate on the contribution from these tools next year?

**Ramy Langer** (Executives):
So definitely, this will be more than 55% next year. And whether it will reach 80%, it's a question that's very hard to answer. And the reason for us that certain customers do not want to change the machine in production if they have a very quick ramp and they don't want to qualify a new machine. So this is really something that is also related to customers. I do expect an increase in the percentage of these products and -- but I don't know if they will get to 80%. Eventually, they will, but I'm not sure that it will happen in '27.

**Kenny Green** (Attendees):
Thanks Vedvati. That brings us to the end of our question-and-answer session. I just would like to remind everybody that a recording of this call will be available from Camtek's Investor Relations website in the coming hours. Also the Zoom link will also have a link and I hand back to Rafi for his closing statement.

**Rafi Amit** (Executives):
Okay. I want to express my gratitude to all of you for your ongoing interest in our business. I look forward to our next conversation in the upcoming quarter. Thank you, and goodbye.

**Kenny Green** (Attendees):
That ends our call. You may disconnect. Thank you very much.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CAMT_Q2_2026_Earnings_Call_20260810.md
- 2026-08-10｜CEO｜guidance：CEO 給 Q3 營收區間 1.58～1.60 億美元（原話："range of $158 million to $160 million"）
- 2026-08-10｜CFO｜guidance：CFO 重述 Q3 財測，並說 Q4 季增雙位數、2027 持續成長（原話："sequential double-digit growth in Q4 and further growth into 2027."）
- 2026-08-10｜CEO｜guidance：CEO 說今年初至今累計訂單超過 6 億美元（原話："orders received year-to-date to more than $600 million"）
- 2026-08-10｜CEO｜guidance：CEO 預期下半年先進封裝業務較上半年成長約 45%（原話："expected to drive approximately 45% growth"）
- 2026-08-10｜CEO｜guidance：CEO 預期 Q4 先進封裝營收約比 Q1 高 70%（原話："approximately 70% higher than the first quarter"）
- 2026-08-10｜COO｜guidance：COO 說年底先進封裝約占營收 80%（原話："80% of our revenues will go towards Advanced Packaging"）
- 2026-08-10｜COO｜guidance：COO 被問全年先進封裝成長，答「成長 70%」（原文脈絡為今年）（原話："The Advanced Packaging will grow by 70%"）
- 2026-08-10｜CFO｜guidance：CFO 澄清 2025 到 2026 先進封裝與 AI 相關業務成長區間（原話："anywhere between 35% to 45% between the Advanced Packaging"）
- 2026-08-10｜CFO｜risk：CFO 提醒去年是紀錄年，今年基期高（原話："Bear in mind that last year was a record"）
- 2026-08-10｜CFO｜guidance：CFO 預期今年中國營收占比約 45%（去年 49%）（原話："China to be anywhere between 45 -- 45-ish kind of"）
- 2026-08-10｜CFO｜margin：CFO 給年底毛利率目標 52.5%～53%（Q2 為 51.4%）（原話："anywhere between 52.5% to 53% exiting the year"）
- 2026-08-10｜CFO｜margin：CFO 給年底營業利益率 30%～32%（Q2 為 27%）（原話："operating margin of between 30% to 32%"）
- 2026-08-10｜CFO｜margin：CFO 說獲利指標將隨產品組合與槓桿逐步改善（原話："improvement across all profitability metrics in the next few quarters"）
- 2026-08-10｜CFO｜commitment：CFO 說費用會增加，但幅度不會超過營收成長（原話："definitely plan to see some increase in our OpEx level"）
- 2026-08-10｜CFO｜commitment：CFO 說毛利率與營業利益率都計畫改善，營業利益率幅度更大（原話："but even more the operating margin levels"）
- 2026-08-10｜CEO｜margin：CEO 報 Q2 營收紀錄 1.33 億美元（原話："Second quarter revenue reached a record of $133 million"）
- 2026-08-10｜CEO｜product：CEO 說 Q2 系統營收約一半來自新一代平台 Eagle G5 與 Hawk（原話："approximately 50% of our systems revenue"）
- 2026-08-10｜COO｜product：COO 說客戶從 Eagle 轉換到 Gen5（原話："want to stay with the Eagle, switching over to the Gen5"）
- 2026-08-10｜COO｜product：COO 說 ASP 會隨產品組合改善，但無法拆解數字（原話："there is going to be an improvement in ASPs as we go along"）
- 2026-08-10｜CEO｜product：CEO 說 Hawk 搭配光學與 AI 技術，可切入更多製程步驟（含混合鍵合）（原話："enabling us to penetrate additional process steps"）
- 2026-08-10｜COO｜product：COO 說 NanoProf 目標擴大量測市場版圖（原話："significantly increase our footprint in the metrology area"）
- 2026-08-10｜CEO｜customer：CEO 拆解訂單：約 80% 為先進封裝（原話："80% of these orders are Advanced Packaging applications"）
- 2026-08-10｜CEO｜customer：CEO 說 OSAT 占訂單逾 50%（原話："OSATs accounted for more than 50% of our total order intake"）
- 2026-08-10｜COO｜customer：COO 說 6 億美元訂單中 HBM 廠商占逾 20%（原話："20% is from HBM players"）
- 2026-08-10｜COO｜customer：COO 說光子學占 6 億美元訂單 5%（原話："orders that we talked about, 5% is photonics."）
- 2026-08-10｜COO｜guidance：COO 預期 2027 光子學訂單占比高於 5%（原話："'27 will be more than the 5% I just mentioned"）
- 2026-08-10｜COO｜customer：COO 說非先進封裝業務穩定（原話："the business is stable"）
- 2026-08-10｜COO｜customer：COO 說有顯著的 CMOS 影像感測器訂單（原話："have some orders for CMOS Image Sensors that are significant"）
- 2026-08-10｜COO｜customer：COO 說中國業務過去幾年穩定（原話："our China business has been, I would say, stable"）
- 2026-08-10｜COO｜competition：COO 回應競爭者說法，稱在 OSAT 市場居主導地位（原話："dominant position in the OSATs market"）
- 2026-08-10｜COO｜competition：COO 說部分領域在搶市占（原話："I think we are gaining share in certain areas"）
- 2026-08-10｜COO｜competition：COO 說未來一年成長與 WFE 相當或更好（原話："I believe that we will be doing similar or better than the WFE"）
- 2026-08-10｜COO｜risk：COO 說 2027 預測尚早，完整輪廓需再 1～2 季（原話："at least 1 more quarter to 2 quarters"）
- 2026-08-10｜COO｜commitment：COO 說供應鏈與產能就緒，無阻礙（原話："we don't see any issues or obstacles when we discuss capacity"）
- 2026-08-10｜COO｜guidance：COO 說 2026 的新訂單很少，多數為 2027 交期（原話："'26, yes, but there are very few."）
- 2026-08-10｜CEO｜capital_allocation：CEO 說持續擴充製造產能（原話："expanding our manufacturing capacity"）
- 2026-08-10｜CFO｜capital_allocation：CFO 說 R&D 增加源於 Visual Layer 收購以強化 AI（原話："the Visual Layer acquisition in order to strengthen our AI offering"）
- 2026-08-10｜CFO｜capital_allocation：CFO 報現金與有價證券餘額（原話："June 30, 2026, were $815.8 million"）
- 2026-08-10｜CFO｜risk：CFO 報 DSO 升至 105 天（原話："DSO increased to 105 days"）
- 2026-08-10｜CFO｜capital_allocation：CFO 預期存貨將增加以支應營收成長（原話："grow in the coming quarters to support the forecasted"）

### CAMT_Analyst_Investor_Day_Camtek_Ltd_20261014.md
- 2026-10-14｜Rafi Amit｜guidance：Q3 營收預告區間（原話："Revenue expected in Q3 is $160 million to $161 million."）
- 2026-10-14｜Rafi Amit｜guidance：2027 營收展望超過 $800M，首次提前一年給（原話："Revenue outlook for 2027 is more than $800 million."）
- 2026-10-14｜Rafi Amit｜guidance：3 年內營收翻倍至 $1.2B，CAGR 約 26%（原話："reaching $1.2 billion representing a CAGR about 26%"）
- 2026-10-14｜Rafi Amit｜guidance：$1.2B 目標屬純有機成長（原話："this target is based on organic growth without factoring in"）
- 2026-10-14｜Moshe Eisenberg｜guidance：年初至今新增訂單累計超過 $800M，動能持續（原話："the order momentum continues"）
- 2026-10-14｜Moshe Eisenberg｜guidance：新增訂單中先進封裝占約 80%（原話："80% comes for advanced packaging"）
- 2026-10-14｜Moshe Eisenberg｜customer：訂單中 OSAT 占略超過五成（原話："a little over 50% came from OSATs"）
- 2026-10-14｜Moshe Eisenberg｜margin：營業利益率由 30% 到 $1.2B 時 34–36%（原話："the operating margin from 30% last year to 34% to 36%"）
- 2026-10-14｜Moshe Eisenberg｜margin：毛利率目標 55–56%（原話："Gross margin goes from 51% to 52% nowadays to 55% to 56%"）
- 2026-10-14｜Moshe Eisenberg｜margin：產品組合拆解：加 3.4 點毛利（原話："they will add around 3.4 points to the profitability"）
- 2026-10-14｜Moshe Eisenberg｜margin：SG&A 槓桿貢獻 2.4 點（原話："this will contribute around 2.4 points"）
- 2026-10-14｜Moshe Eisenberg｜margin：R&D 投入拿回略多於 1 點（原話："take back a little over 1 point from the profitability"）
- 2026-10-14｜Moshe Eisenberg｜margin：模型假設 R&D 約占營收 10%（原話："we assume that R&D will account for around 10% of the mix"）
- 2026-10-14｜Moshe Eisenberg｜guidance：成長三引擎：檢測與量測主業貢獻約 $380M（原話："will contribute around $380 million to the growth"）
- 2026-10-14｜Moshe Eisenberg｜guidance：軟體與服務由 $28M 增至 $140M 以上、占 12%（原話："to over $140 million, which will be 12% of the mix"）
- 2026-10-14｜Ramy Langer｜product：軟體產品 2027 起產生營收（原話："we plan to generate revenues from this product starting 2027"）
- 2026-10-14｜Moshe Eisenberg｜product：2025 年服務營收成長 40%（原話："we grew 40% the service revenue"）
- 2026-10-14｜Moshe Eisenberg｜commitment：管理層稱 3 年模型非明確承諾、為基準情境（原話："we didn't commit to specific 3 years"）
- 2026-10-14｜Eyal Segev｜guidance：IR 與分析師口徑：2027 為 outlook 非 guidance（原話："this is not a guidance. This is an outlook."）
- 2026-10-14｜Ramy Langer｜commitment：管理層稱歷來預測保守且未失手（原話："we ever missed one of our forecast in the last few years"）
- 2026-10-14｜Ramy Langer｜guidance：WFE 更強則難以現在調整數字（原話："it's too early now to give a different number"）
- 2026-10-14｜Moshe Eisenberg｜guidance：2027 中國預期不低於今年（原話："at least as strong as it is this year in 2027"）
- 2026-10-14｜Rafi Amit｜customer：中國約占營收 45%（原話："China is around 45% of our business"）
- 2026-10-14｜Rafi Amit｜risk：本地競爭者在中國增加（原話："competition more and more from the locals"）
- 2026-10-14｜Moshe Eisenberg｜risk：WFE 可能進入資本支出消化期（原話："the WFE will get into a CapEx digestion period"）
- 2026-10-14｜Ramy Langer｜competition：競爭對手宣布 OSAT 訂單，公司稱收到不遠小於的同客戶大單（原話："we have received a very significant order"）
- 2026-10-14｜Ramy Langer｜competition：預期 2028 年份額更大（原話："I'm expecting that our share in '28 will be larger."）
- 2026-10-14｜Ramy Langer｜competition：台灣 OSAT 份額預期至少 50%（原話："I expect that our share is at least 50%"）
- 2026-10-14｜Ramy Langer｜competition：否認客戶對 3D 凸塊量測有猶豫（原話："we do not see this hesitancy"）
- 2026-10-14｜Ramy Langer｜competition：大型對手進入 2D 檢測是競爭（原話："we will need to address and work very hard"）
- 2026-10-14｜Ramy Langer｜competition：2D 檢測占 2026 年出貨 85%（原話："85% of our tools were sold for inspection applications"）
- 2026-10-14｜Eyal Segev｜product：第 10 代凸塊高度感測器明年推出（原話："next-generation sensor, which will be released next year"）
- 2026-10-14｜Eyal Segev｜product：HBM5 仍沿用凸塊而非混合鍵合（敘事變化）（原話："It's going to continue to be based on bumps."）
- 2026-10-14｜Eyal Segev｜product：混合鍵合進度慢於預期（原話："it's ramping up slower than we expected"）
- 2026-10-14｜Ramy Langer｜product：2030 年 SAM 約 $6B（原話："an increased SAM of about $6 billion in 2030"）
- 2026-10-14｜Ramy Langer｜customer：訂單約 5% 來自光子（原話："about 5% are going to photonics"）
- 2026-10-14｜Ramy Langer｜customer：光子主要放量在 2028 年之後（原話："more of a '28 and onwards"）
- 2026-10-14｜Ramy Langer｜customer：2027 全年交貨檔期已在排（原話："we are getting to a slot for all of '27"）
- 2026-10-14｜Moshe Eisenberg｜capital_allocation：現金超過 $800M 用於成長與併購（原話："We have over $800 million to support the growth"）
- 2026-10-14｜Lior Aviram｜capital_allocation：過去 1.5 年看過逾百件併購機會（原話："we've looked at over 100 opportunities"）
- 2026-10-14｜Rafi Amit｜capital_allocation：併購不分散管理層對核心有機成長的注意力（原話："extremely careful not to divert management attention"）
- 2026-10-14｜Lior Aviram｜capital_allocation：Visual Layer 整合完成（原話："the PMI has already been completed"）
- 2026-10-14｜Ramy Langer｜risk：上調空間尚無法量化（原話："it's too early to size the upside"）
- 2026-10-14｜Rafi Amit｜commitment：產能不構成限制、可供應更多（原話："Our operational infrastructure will be able to supply more"）

### 問答異常語氣（迴避／改口／保留）
- CAMT_Q2_2026_Earnings_Call_20260810.md｜問：Brian Chin 問 Hawk/Gen5 占比提高下，下半年 30%+ 成長中 ASP 貢獻如何拆解｜答法：COO 稱事前沒算、無法給準確答案，只說 ASP 會改善
- CAMT_Q2_2026_Earnings_Call_20260810.md｜問：Matt Prisco 問 2027 能見度與成長是否可持續｜答法：COO 稱現在給預測太早，不給 2027 數字，只說客戶樂觀
- CAMT_Q2_2026_Earnings_Call_20260810.md｜問：Matt Prisco 問中國營收走勢與競爭環境｜答法：COO 只說穩定、持續投資，並稱「這大致是我現階段能評論的」，未答競爭
- CAMT_Q2_2026_Earnings_Call_20260810.md｜問：Shane Brett 追問全年先進封裝成長（約 30%）與 HPC 成長｜答法：COO 先答先進封裝今年成長 70%，經 CFO 追問後改為 35%～45%，數字前後不一致
- CAMT_Q2_2026_Earnings_Call_20260810.md｜問：Jim Schneider 問 DRAM／HBM 曝險與中國業者（如 CXMT）｜答法：COO 給 HBM 占訂單比例，但對 CXMT 等客戶名稱未回答，稱不能談客戶名
- CAMT_Analyst_Investor_Day_Camtek_Ltd_20261014.md｜問：Auguste Richard（Northland）：把 2027 年 $800M 依預測／訂單／預付三層拆分，並問交貨檔期｜答法：未給拆分數字，稱 backlog 為 meaningful number 但 We did not say the numbers，改談 pipeline 定義與公司歷來預測紀錄
- CAMT_Analyst_Investor_Day_Camtek_Ltd_20261014.md｜問：Blayne Curtis（Jefferies）：CPO 與 MPO 時程及公司在 PIC 的定位｜答法：只答訂單約 5% 為光子、放量在 2028 後，未直接談 MPO 或時程判斷
- CAMT_Analyst_Investor_Day_Camtek_Ltd_20261014.md｜問：Matt Prisco（Cantor）：若 2027 有上調空間，來源排序與能否供應｜答法：稱有 potential upside 但表示太早量化，要等 1–2 季，未給排序或數字
- CAMT_Analyst_Investor_Day_Camtek_Ltd_20261014.md｜問：Charles Shi（Needham）：客戶對專用 3D 凸塊量測有猶豫、HBM 降規格｜答法：直接否認看到猶豫並質疑資訊來源，同時承認 NVIDIA 等傾向降低單模組記憶體密度

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
{"date":"20260906","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤ $125（FY2027E 本益比約 25.5 倍、Base 五年年化 ≥ 12%）且 Q3 營收 ≥ $158M 兌現→首倉 1/3；或 FY2027 共識 EPS 上修 ≥ 10% 且股價未過 $165→重跑","irr_base_pct":8.7,"ev5y_pct":42.8,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"-","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.59,"ev5y_pct":42.8,"irr_base_pct":8.7,"max_dd_pct":-55,"bull_5y_price":330.0,"bear_5y_price":86.4,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價 ≤ $125（FY2027E 本益比約 25.5 倍、Base 五年年化 ≥ 12%）且 Q3 營收 ≥ $158M 兌現→首倉 1/3；或 FY2027 共識 EPS 上修 ≥ 10% 且股價未過 $165→重跑","price_at_dd":145.72,"archetype":"品質複利成長","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAMT_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
