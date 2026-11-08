你是 stock-analyst **v20 判斷 agent**，標的 BKNG（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"BKNG","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BKNG_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BKNG_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"GAAP 營收","value":8893,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm"}},{"id":"f_kpi1_adjusted_non_gaap_ftc","label":"Adjusted 營收（non-GAAP，加回 FTC 沖減）","value":9793,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm"}},{"id":"f_kpi2_adjusted_ebitda","label":"Adjusted EBITDA","value":4607,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm"}},{"id":"f_kpi3_gaap","label":"GAAP 營業利益","value":3418,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm"}},{"id":"f_kpi4_gaap","label":"GAAP 營業利益率","value":38.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm"}},{"id":"f_kpi7_adjusted_eps","label":"Adjusted EPS","value":4.66,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm"}},{"id":"f_kpi8_room_nights","label":"間夜數（room nights）","value":345,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm"}},{"id":"f_kpi9_gross_bookings","label":"總預訂額（gross bookings）","value":54.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm"}},{"id":"f_kpi10_q4_2026","label":"管理層指引：Q4 2026","value":"room nights +1%~+3%；gross bookings +2%~+4%（固定匯率 +4%~+6%）；adjusted 營收 0%~+2%（固定匯率 +2%~+4%）；adjusted EBITDA 約持平 YoY","period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"YoY","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm"},"note":"未查"},{"id":"f_kpi11_2026","label":"管理層指引：全年 2026","value":"gross bookings、adjusted 營收、adjusted EBITDA 皆高個位數成長；adjusted EPS 低至中十位數成長（表格排版未能清楚區分 Q4 與全年，需人工確認）","period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"YoY","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_bkng_operating_margin_pct","label":"BKNG 營業利益率","value":32.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BKNG.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bkng_fcf_margin_pct","label":"BKNG FCF 利潤率","value":32.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BKNG.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_expe_gross_margin_pct","label":"EXPE 毛利率","value":90.48,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EXPE.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_expe_operating_margin_pct","label":"EXPE 營業利益率","value":18.39,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EXPE.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_expe_fcf_margin_pct","label":"EXPE FCF 利潤率","value":23.09,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EXPE.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_tcom_gross_margin_pct","label":"TCOM 毛利率","value":80.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TCOM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tcom_operating_margin_pct","label":"TCOM 營業利益率","value":18.19,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TCOM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_trip_gross_margin_pct","label":"TRIP 毛利率","value":91.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TRIP.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_trip_operating_margin_pct","label":"TRIP 營業利益率","value":3.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TRIP.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_trip_fcf_margin_pct","label":"TRIP FCF 利潤率","value":-1.18,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TRIP.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_abnb_gross_margin_pct","label":"ABNB 毛利率","value":82.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABNB.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abnb_operating_margin_pct","label":"ABNB 營業利益率","value":20.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABNB.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abnb_fcf_margin_pct","label":"ABNB FCF 利潤率","value":36.93,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABNB.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_fcf_non_gaap","label":"自由現金流（FCF，non-GAAP）","value":1069,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm"}},{"id":"f_kpi6_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":4.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":160.66,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-2.69,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":49.93,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.48,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.46 → 10.41）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.49,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.35 → 12.29）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.62,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（14.44 → 14.35）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":10.41,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":12.29,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":14.35,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-0.38,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 10.45 → 10.41（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":17.43,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.25,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.44,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":15.43,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 10.41，分子＝快照價 160.66","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.023,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":5505.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 21319.0、現金 15814.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":743.7,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":124991.76,"period":"2026-11-08","unit":"USD m","basis":"市值 119486.76 ＋ 淨負債 5505.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":28620.09,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（26 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":31547.68,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（35 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.37,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 160.66 / W52 181.26 / W104 192.51 / W250 145.38 / W250 13週斜率 0.7%"},{"id":"f_ma_w52","label":"52 週均線","value":181.26,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":192.51,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":145.38,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.7,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：Google 將旅遊搜尋整合進 Maps 與 Gemini，其他大型科技平台與 AI 原生業者正開發可直接搜尋、比價、訂位的 Gen AI 助理，可能減少直接流量並使 OTC 被繞過；Gen AI 亦降低進入門檻。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm","excerpt":"Other large technology platforms and AI-native competitors are developing Gen AI-powered assistants and agents that can search, compare, recommend, and facilitate travel and dining reservations directly within their search engines, operating systems, messaging platforms, or \"super-apps.\"","as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K：部分對手願意零利潤或虧損以搶份額，亞洲尤其盛行折扣與優惠券，折扣會壓低 ADR 與營收占訂單比。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm","excerpt":"In some cases, our competitors are willing to make little or no profit on a transaction or offer travel services at a loss in order to gain market share.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"2026-09 下旬 Meta 個人 AI 代理 Muse 被報導可直接與航空公司或飯店完成訂位，Booking 股價當日跌約 5%，Expedia 跌 7%、Airbnb 跌 6%。","source":"24/7 Wall St. 報導 Muse","url":"https://247wallst.com/investing/2026/09/23/travel-booking-stocks-tumble-as-muse-threatens-to-bypass-them-expedia-falls-7-airbnb-drops-6-booking-holdings-sinks-5/","excerpt":"Travel Booking Stocks Tumble as Muse Threatens to Bypass Them: Expedia Falls 7%, Airbnb Drops 6%, Booking Holdings Sinks 5%","as_of":"2026-09-23","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"MarketScreener 評論稱 Booking 自行處理旅客付款的訂單占比 12 個月內由 63% 升至 70%，並據此論述其在取得份額。","source":"MarketScreener, Booking: guilty until proven innocent","url":"https://www.marketscreener.com/news/booking-guilty-until-proven-innocent-ce7e5fded089f727","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"BKNG 全年展望假設高機票價、部分航線運力受限與長程國際需求偏弱會持續（Q2 2026 報導）","source":"Booking Holdings Q2 2026 coverage (finviz)","url":"https://finviz.com/news/377349/booking-holdings-tops-second-quarter-forecasts-as-travel-demand-stays-resilient","excerpt":"The outlook is based on the assumption that high airfares, limited capacity on certain routes and weaker long-haul international demand will persist.","as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"BKNG 10-Q：中東衝突直接影響已大致正常化，但機票價格偏高的間接影響仍壓抑長程國際需求","source":"Booking Holdings 10-Q FY2026 (Q3)","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000045/bkng-20260930.htm","excerpt":"The direct impacts of the conflict in the Middle East on travel demand had largely normalized, but indirect impacts, including elevated flight ticket prices, continued to weigh on long-haul international travel demand.","as_of":"2026-10-30","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q3 2026 間夜 345M、年增 7%（Q2 為 5%、Q1 為 6%）；Q4 間夜指引僅 1%–3%","source":"BKNG Q3 2026 earnings coverage (search summary of 8-K/transcript)","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261108","affects":["thesis.H","triggers"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"美國飯店供給成長低：STR 預估 2026 年 0.4%、2027 年 0.6%；Lodging Econometrics 預估 2027 年 1.4%；全球在建管線創高","source":"Hotel Management / Lodging Econometrics via travelextra","url":"https://www.travelextra.ie/global-hotel-construction-pipeline-reaches-record-16000-projects/","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Phocuswright 預估全球旅遊訂房額年增 5.2% 至 2027、約 1.8 兆美元；WTTC 預估未來十年旅遊 GDP 年增 3.6%","source":"Phocuswright / WTTC via tripinfo, tourexpi","url":"https://www.tripinfo.com/itm/articles/from-1-6t-to-1-8t-how-global-travel-will-grow-shift-go-digital-by-2027","excerpt":null,"as_of":"2025-10-29","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"BKNG Q3 2026 間夜年增 7%，Q4 指引 1–3%","source":"BKNG Q3 2026 Earnings Release","url":"https://s25.q4cdn.com/383369491/files/content_files/BKNG-Q3-2026-Earnings-Release.pdf","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261108","affects":["thesis.H","triggers"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K FY2025 揭露 Booking.com 受各國競爭主管機關調查（合約平價、定價工具、排名標準），已以承諾改變平價、排名資訊與價格顯示做法了結部分案件；並因 DMA gatekeeper／DSA VLOP 指定而受額外規範，已依 DMA 取消歐洲經濟區平價條款","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm","excerpt":"We have been the subject of investigations or inquiries by national competition authorities (\"Competition Authorities\") and other governmental authorities regarding competition law matters, consumer protection issues, and other areas.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2026 年 7 月 FTC 幕僚告知 Priceline 擬建議提起訴訟（揭露、費用、帳單等不公平或欺騙性做法，屬消費者保護而非反壟斷）；公司於 Q3 2026 認列營收減項 9 億美元及應計損失 1 億美元，尚未和解","source":"Booking Holdings 10-Q（2026-09-30）經搜尋摘要引述","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000045/bkng-20260930.htm","excerpt":"FTC staff informed Priceline that they intend to recommend that the FTC files a complaint against Priceline and a business-to-business affiliate partner of Priceline asserting unfair or deceptive business practices related to disclosures, fees, customer support, and billing practices.","as_of":"2026-09-30","retrieved_at":"20261108","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"西班牙 CNMC 2024 年裁罰並限制平價條款與排名標準；公司已入帳負債 4.76 億美元，西班牙國家法院裁定上訴期間暫停執行","source":"Booking Holdings 10-Q（2026-09-30）經搜尋摘要引述","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000045/bkng-20260930.htm","excerpt":"In 2024, the CNMC imposed a fine and restricted certain of Booking.com's business practices such as those relating to contractual parity provisions and the ranking criteria; it recorded a liability for this matter with $ 476million.","as_of":"2026-09-30","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"義大利 AGCM 2026 年 4 月對 Booking.com 啟動調查（付費能見度／偏好夥伴排名）；瑞士 2025 年命令降低佣金、上訴中；希臘 2025 年 6 月啟動正式調查","source":"Booking Holdings 10-Q（2026-09-30）經搜尋摘要引述","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000045/bkng-20260930.htm","excerpt":"In April 2026, the Italian Competition and Consumer Authority opened an investigation into whether certain Booking.com business practices adversely affect consumers.","as_of":"2026-09-30","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#4","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"經查搜尋結果未見美國 DOJ／FTC 對 Booking 的反壟斷（非消費者保護）案件；一手 10-K Item 3 摘錄無具體條文","source":"WebSearch 結果（無美國反壟斷案）","url":null,"excerpt":null,"as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#5","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"希臘競爭委員會就 Booking 濫用優勢地位案，異議聲明與救濟措施聽證（12/28）","source":"MLex","url":"https://www.mlex.com/mlex/articles/2543881","excerpt":"Booking’s proposed remedies set for Greek antitrust hearing ( October 29, 2026, 12:05 GMT | Official Statement) -- MLex Summary: Accommodation platform Booking’s proposed commitments to address suspected abuse of dominance in Greece will be examined on Dec. 28, alongside a Statement of Objections published on Thursday.","as_of":"2026-10-29","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"regulatory_antitrust#6","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"歐盟執委會調查 Booking.com 詐欺防制（德文報導，未核實）","source":"goldesel.de","url":"https://goldesel.de/aktien/news/booking-holdings-aktie-eu-ermittelt-wegen-moglicher-verbraucherschutzverstosse","excerpt":"EU untersucht Betrugsprävention und Anzeigenkennzeichnung Die Europäische Kommission prüft, ob Booking.com Risiken durch betrügerische Unterkunftsangebote und Phishing ausreichend bewertet und wirksam eingedämmt hat.","as_of":"2026-10-21","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"BKNG 10-K FY2025 將出口管制列為多司法管轄區合規風險之一；隨支付處理業務擴展至新地區，須遵守金融服務與出口管制法規，增加合規成本。僅屬一般性風險揭露，未點名具體關稅或管制事件。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm","excerpt":"as our payment processing activities develop or expand into different geographies, we are subject to additional regulations, including financial services and export controls regulations, which would result in increased compliance costs and complexities","as_of":"2026-02-18","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Q1 2026 10-Q：中東衝突造成全球地緣與總經擾動，直接衝擊中東及歐亞等旅遊走廊，取消增加、新訂單成長放緩。","source":"Booking Holdings 10-Q Q1 FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000025/bkng-20260331.htm","excerpt":"The conflict in the Middle East has resulted in worldwide geopolitical and macroeconomic disruption, directly impacting travel trends in the Middle East and in other travel corridors such as Europe and Asia. Following the onset of the conflict, we experienced increased cancellations and slower growth in new bookings.","as_of":"2026-05-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Q2 2026 10-Q：區域直接影響於 6 月大致正常化，但仍有間接影響（機票價格高、國際航線運能減少、長程需求下降）；Q3 10-Q 指長程需求疲弱仍壓低間夜成長。","source":"Booking Holdings 10-Q Q2 FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000037/bkng-20260630.htm","excerpt":"Direct regional impacts largely normalized during June, there were continued indirect impacts, including elevated flight ticket prices, reduced flight capacity on certain international routes, and decreased long-haul international travel demand.","as_of":"2026-07-31","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險因素：硬體放在全球託管設施，災難復原計畫未必涵蓋所有區域；第三方服務商合約通常不提供服務中斷追索權。搜尋未見「單點失效」字樣或具名雲端供應商。","source":"Booking Holdings 10-K FY2023 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1075531/000107553124000014/bkng-20231231.htm","excerpt":null,"as_of":"2024-02-23","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 room nights 345M, +7% YoY; gross bookings $54.5B, +10%; reported revenue $8.9B, -1% (FTC-related revenue reduction), adjusted revenue $9.8B, +9%","source":"Booking Holdings Q3 2026 earnings release (8-K), 2026-11-03","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"Q4 2026 guidance: room nights +1% to +3%, gross bookings +2% to +4% (4%-6% constant currency); management cited Middle East disruption, higher airfares, localized European unrest and softer international travel late in Q3, assumed to persist through year-end","source":"Booking Holdings Q3 2026 earnings release (8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Room night growth trend 2026: Q1 +6% (Middle East conflict est. ~2pp drag), Q2 +5%, Q3 +7%; 2025 full-year +8% driven by Europe and Asia","source":"Booking Holdings Q1/Q2 2026 earnings releases via search summary","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000036/q2-26bkngearningsrelease.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Skift (May 2026) reported Booking lost ~6M room nights to the Iran war, grew room nights 6% vs 8% projected, and noted U.S. market share gain likely at Expedia's expense (secondary aggregator summary)","source":"Pulse.bot summary of Skift report","url":"https://www.pulse.bot/proptech/news/booking-ceo-touts-ties-with-independent-hotels-as-agentic-ai-and-airbnb-seek-gains-be94ca5e-4de8-4efa-887b-22b77a146528","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"2026-09-23 Meta 推出可不經 OTA 直接訂機票/飯店的個人 AI agent，BKNG 當日跌約 5%，Goldman 警告此類 agent 可能衝擊仲介型業務。","source":"247WallSt｜Travel booking stocks tumble as Muse threatens to bypass them","url":"https://247wallst.com/investing/2026/09/23/travel-booking-stocks-tumble-as-muse-threatens-to-bypass-them-expedia-falls-7-airbnb-drops-6-booking-holdings-sinks-5/","excerpt":"Meta's new AI agent can book a flight or hotel room without ever visiting Expedia, Airbnb, or Booking Holdings","as_of":"2026-09-23","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"2026-08 報導 OpenAI 縮減 ChatGPT 直接結帳計畫、改以第三方 app 為主；Bernstein 認為降低去中介風險。","source":"搜尋摘要彙整（Bernstein 分析師 Richard Clarke 評論）","url":"https://daytraders.com/news/2026/02/23/booking-expedia-2026-analysis-price-target-ai-disruption","excerpt":"This means that Booking and Expedia can continue to get in front of consumers on AI-platforms, lowering the risk of disintermediation","as_of":"2026-08-17","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"BKNG CFO 表示去中介不是真正風險，較實際的風險是損失部分直接流量；2025 直接流量約中 60% 段。","source":"Yahoo Finance via newsquantified｜Booking CFO: The AI Threat Isn't 'Really a Risk at All'","url":"https://www.newsquantified.com/bkng/stock-report/booking-holdings-inc-cfo-ai-threat-isnt-really-0fp1td","excerpt":"I don't think disintermediation is really a risk at all.","as_of":"2026-02-28","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"2026-02 Marriott、Wyndham 的 agentic 計畫被視為可繞過 OTA；BTIG 認為疑慮過度，因多數飯店為獨立業者。","source":"Skift｜Wyndham and Marriott's Agentic Plans Put Pressure on Booking","url":"https://skift.com/2026/02/20/wyndham-and-marriotts-agentic-plans-put-pressure-on-booking-are-the-concerns-justified/","excerpt":"the vast majority of the world's hotels are independents and less able to break away from OTAs.","as_of":"2026-02-20","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FY2025 10-K：直接來自自家平台的間夜占比為五十%中段且年增，改善行銷效率；排除聯盟（B2B）後更高。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm","excerpt":"The mix of total room nights booked by consumers coming directly to our platforms was a mid-fifties percentage in 2025, and was higher if we exclude the room nights booked through affiliate programs (i.e., business-to-business). The mix of total room nights booked by consumers coming directly to our platforms increased year-over-year, which benefited our marketing efficiency for 2025.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"FY2025 10-K：2025年平均績效行銷ROI小幅下滑，原因為付費流量組合變化與社群媒體支出增加。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm","excerpt":"In 2025, our average ROI was down slightly year-over-year driven by changes in paid traffic mix and increased social media spend.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q3 2026 10-Q：商家模式占總訂房額 75%，去年同期 72%，因 Booking.com 由代理轉商家模式","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000045/bkng-20260930.htm","excerpt":"These merchant services allow us to facilitate payments from travelers and offer secure, flexible transaction terms, such as varied payment forms, currencies, and timing. The mix of our total gross bookings generated on a merchant basis across the Company was 75% in the third quarter of 2026, an increase from 72% in the third quarter of 2025 due to the ongoing shift from agency to merchant","as_of":"2026-10-30","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 2026（2026-11-03 公布）：room nights +7%、gross bookings +10%，報告營收 -1%（FTC 相關約 $9 億營收減項）；Q4 指引 room nights +1%~3%、調整後 EBITDA 約持平，管理層稱季末旅遊需求略降溫；全年指引大致不變。（搜尋摘要轉述，未核原文）","source":"Finviz/247wallst/Booking Q3-26 earnings release 搜尋摘要","url":"https://finviz.com/news/415433/booking-holdings-shares-little-changed-as-revenue-miss-and-weaker-q4-outlook-offset-earnings-beat","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.R","valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師共識目標價約 $232–234（Benzinga 34 位分析師均值 $234、評級 Buy；Investing.com 均值 231.98，31 Buy/7 Hold）；已反映股票分割後價位，舊頁面 $4,000–6,000 為分割前。最新目標價動作為 2026-08 的 BTIG $250、Evercore $270，as-of 非 Q3 後，Q3 後修正未查到。（搜尋摘要轉述，未核原文）","source":"Benzinga sentiment / Investing.com consensus estimates","url":"https://uk.investing.com/equities/priceline.com-inc-consensus-estimates","excerpt":null,"as_of":"2026-08-27","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3-26 8-K 財報新聞稿：Q4 與全年指引原文","source":"SEC 8-K Q3-26 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm","excerpt":"● Net income declined 1% compared to the third quarter of 2025, while Adjusted Net income and Adjusted EBITDA grew 8% and 9%, respectively. ● GAAP EPS and Adjusted EPS grew 7% and 17%, respectively, compared to the third quarter of 2025. Q3 2026 (#) (Δ Y/Y) Room Nights 345M 7% Gross Bookings $54.5B 10% Revenue $8.9B (1%) Adjusted Revenue $9.8B 9% GAAP Net Income $2.7B (1%)","as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"OpenTable（Booking 旗下）於 2026-04-20 宣布收購加拿大訂位平台 Libro，Libro 維持獨立品牌。","source":"GlobeNewswire 經 researchpool：OpenTable acquires Canadian reservation platform Libro","url":"https://app.researchpool.com/provider/globenewswire/booking-holdings-inc-bkng-opentable-acquires-canadian-reservation-platform-libro-expanding-prese-pIWWnSbmF9","excerpt":null,"as_of":"2026-04-20","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"Booking.com 於 2026-04 確認訂房資料遭未授權第三方存取（姓名、聯絡方式、訂房細節），稱未涉及付款資料、已重設訂位 PIN。","source":"BleepingComputer：New Booking.com data breach forces reservation PIN resets","url":"https://bleepingcomputer.com/news/security/new-bookingcom-data-breach-forces-reservation-pin-resets","excerpt":null,"as_of":"2026-04-13","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"Q3 2026 10-Q 揭露：2026-10 歐盟執委會對 Booking.com 啟動 DSA 調查；2026-07 FTC 員工告知 Priceline 擬建議提起訴訟；2026-04 義大利競爭暨消費者局啟動調查；西班牙 CNMC 罰款上訴中、已認列約 4.72 億美元負債。","source":"SEC EDGAR 10-Q（2026-09-30）及 10-Q（2026-06-30）","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000045/bkng-20260930.htm","excerpt":null,"as_of":"2026-10-31","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"+","claim":"2026-02 公司作為原告與對方達成和解，預計 2026 Q1 取得約 9,000 萬美元收益。","source":"SEC EDGAR 10-K FY2025 附註","url":"https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm","excerpt":"In February 2026, the Company entered into favorable settlement agreements to resolve litigation matters in which it was a plaintiff, for which it expects to receive a benefit of approximately $90 million in the first quarter of 2026, upon completion of various conditions.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"2026-02-18 宣布 25 比 1 股票分割，2026-04-06 起以分割後基準交易。","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1075531/000107553126000008/bkng-20260218.htm","excerpt":"On February 18, 2026, the Company announced a twenty-five-for-one forward stock split of the Company's common stock.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"OpenTable 於 2026-04-20 宣布收購加拿大 Libro（小型併購）；未見大型併購。","source":"GlobeNewswire 經 researchpool：OpenTable acquires Libro","url":"https://app.researchpool.com/provider/globenewswire/booking-holdings-inc-bkng-opentable-acquires-canadian-reservation-platform-libro-expanding-prese-pIWWnSbmF9","excerpt":null,"as_of":"2026-04-20","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K 風險因素：過去曾為證券集體訴訟被告；另有多個司法管轄區就旅遊交易稅對 OTC（含公司）提告。搜尋未見 2026 年證券詐欺集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm","excerpt":"In the past, we have been a defendant in securities class action litigation.","as_of":"2026-02-18","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026 Q1 10-Q：兩個荷蘭基金會代表歐洲飯店與消費者提出競爭法／消費者索賠；Booking 表示將抗辯。","source":"SEC EDGAR 10-Q（2026-03-31）","url":"https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000025/bkng-20260331.htm","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"無實體產品召回；2026-04 Booking.com 資料外洩事件，公司重設訂位 PIN。","source":"BleepingComputer：New Booking.com data breach forces reservation PIN resets","url":"https://bleepingcomputer.com/news/security/new-bookingcom-data-breach-forces-reservation-pin-resets","excerpt":null,"as_of":"2026-04-13","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 清單無 Item 4.02（財報不可信賴）；搜尋未見 SEC 執法或重編。監管案為歐盟 DSA、FTC、義大利、西班牙 CNMC（消費者／競爭機關，非 SEC）。","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001075531&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"BKNG","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":32.78,"fcf_margin_pct":32.84,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BKNG","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"EXPE","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":90.48,"operating_margin_pct":18.39,"fcf_margin_pct":23.09,"rd_intensity_pct":8.04},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EXPE","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"TCOM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":80.05,"operating_margin_pct":18.19,"fcf_margin_pct":null,"rd_intensity_pct":24.33},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TCOM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"TRIP","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":91.86,"operating_margin_pct":3.1,"fcf_margin_pct":-1.18,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TRIP","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ABNB","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":82.9,"operating_margin_pct":20.81,"fcf_margin_pct":36.93,"rd_intensity_pct":18.89},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABNB","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"BKNG"},"financial_history":{"ticker":"BKNG","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":17090000000.0,"revenue_yoy_pct":null,"gross_margin_pct":null,"operating_margin_pct":29.85,"net_income":3058000000.0,"diluted_eps":3.054,"free_cash_flow":6186000000.0,"fcf_margin_pct":36.2,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":21365000000.0,"revenue_yoy_pct":25.01,"gross_margin_pct":null,"operating_margin_pct":27.31,"net_income":4289000000.0,"diluted_eps":4.696,"free_cash_flow":6999000000.0,"fcf_margin_pct":32.76,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":23739000000.0,"revenue_yoy_pct":11.11,"gross_margin_pct":null,"operating_margin_pct":31.83,"net_income":5882000000.0,"diluted_eps":6.9076,"free_cash_flow":7894000000.0,"fcf_margin_pct":33.25,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":26917000000.0,"revenue_yoy_pct":13.39,"gross_margin_pct":null,"operating_margin_pct":34.48,"net_income":5404000000.0,"diluted_eps":6.6228,"free_cash_flow":9087000000.0,"fcf_margin_pct":33.76,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/BKNG/BKNG_Q3_2026_Earnings_Call_20261103.md）

# Q3 2026 Earnings Call
**Booking Holdings Inc.** | Earnings Calls | 2026-11-03

**Operator** (Operator):
Hello, and welcome to Booking Holdings Third Quarter 2026 Conference Call. Booking Holdings would like to remind everyone that this call may contain forward-looking statements, which are made pursuant to the safe harbor provisions of the Private Securities Litigation Reform Act of 1995. These forward-looking statements are not guarantees of future performance and are subject to risks, uncertainties and assumptions that are difficult to predict.
Therefore, actual results may differ materially from those expressed, implied or forecasted in any such forward-looking statements. Expressions of future goals or expectations and similar expressions reflecting something other than historical facts are intended to identify forward-looking statements.
For a list of factors that could cause Booking Holdings' actual results to differ materially from those described in the forward-looking statements, please refer to the safe harbor statement in the Booking Holdings' earnings press release as well as the Booking Holdings' most recent filings with the Securities and Exchange Commission.
Unless required by law, Booking Holdings undertakes no obligation to update publicly any forward-looking statements, whether as a result of new information, future events or otherwise. A copy of Booking Holdings' earnings press release is available in the Investors section of Booking Holdings' website at www.bookingholdings.com.
Booking Holdings intends to use the Investor Relations page of its website, ir.bookingholdings.com, to disclose material information for purposes of the SEC's Regulation Fair Disclosure. Booking Holdings encourages investors to monitor this website in addition to other public announcements and SEC filings as information posted on that page could be deemed to be material information.
[Operator Instructions] And now I'd like to introduce Booking Holdings speakers for this afternoon, Glenn Fogel and Ewout Steenbergen. Go ahead, gentlemen.

**Glenn Fogel** (Executives):
Good afternoon, and thank you for joining us today. I am pleased to report that our teams delivered another quarter of strong operating performance with results exceeding the high end of our guidance across each of our key financial metrics. These results reflect the resilience of travel demand and the work our teams have done to strengthen our products and services.
While travel trends can fluctuate in the near term, we remain focused on making travel easier, more connected and more personalized. This quarter, we continued to advance several priorities that support that goal. Let me begin with AI, which is creating significant opportunities to better serve travelers and partners while strengthening our business. We believe this is the most transformational time for industries since the dawn of the Industrial Revolution.
Particularly in travel distribution, AI is opening up new ways for people to discover, plan, book and manage travel. The technologies and the way people use them are evolving quickly. We are actively testing AI across the traveler journey, learning from real-world usage and scaling the capabilities that create the most value for travelers and partners. We have made tangible progress across our brands over the last several months.
For example, at Booking.com, we're expanding AI tools that help travelers explore destinations in greater detail at the top of the funnel. We also continue to advance our agentic capabilities, enabling customers to cancel a booking or get answers about their stay without having to contact customer service. Early testing is showing encouraging customer satisfaction results and fewer escalations to our service teams.
Agoda launched its new AI assistant, which is now live across 21 markets and helps travelers move from an initial idea to a bookable trip using Agoda's live selection of accommodations, flights and activities. At Priceline, we continue to develop Penny, its AI travel assistant, and bring more of Penny's capabilities into the main Priceline experience so more customers can benefit from them.
These experiences show the difference between recommending a trip and actually enabling someone to book it seamlessly. Whether it's comparing locations, photos, room choices and prices, we can combine the ease of an AI assistant with the information, live inventory, booking capabilities and service of our platforms. We're also excited to see the birth of new AI-native experiences beyond our existing brands.
In September, we launched Lola, which helps people access unique travel, dining and event inventory across platforms beyond our company through a conversational experience and a membership model. A few weeks later, we launched Vayo, a proactive AI travel agent designed to help travelers from initial planning through booking and beyond.
It can bring existing reservations from a traveler's email history into one place and use that history to create more personalized offers and suggest ways to fill gaps in an itinerary. Vayo also continuously monitors prices and stays engaged after booking, alerting travelers to changes and helping them adjust their plans along the way. These platforms are testing grounds where we can explore new AI capabilities, iterate quickly and apply what we learn across Booking Holdings.
Our established brands give us the scale to bring successful capabilities to our partner and customer bases. This combination allows us to pursue several approaches and direct resources toward the experiences that prove most useful to travelers and partners. Alongside these investments, our partnerships give us additional ways to reach travelers wherever they choose to engage. We continue to work with leading technology and AI companies, including Meta, OpenAI, Google, Anthropic and Amazon.
OpenTable's native integration with OpenAI has become one of the brand's fastest growing channels, from a small base, and OpenTable recently debuted as the first dining partner with Meta's Muse personal agent. And Agoda is live on Muse as a launch partner in Asia, connecting Muse directly with Agoda's new AI assistant. Finally, AI is helping us operate more efficiently. We use it to help customer service teams handle routine requests, accelerate product development and improve our internal processes.
As an example, in the third quarter, customer service costs declined despite higher booking volumes while satisfaction remained high. We are also seeing higher engineering productivity while the cost per merge request continues to decline. These are real efficiency gains we are seeing today, and we believe AI can deliver more over time. 
Now, let me turn to the value we provide to our supplier partners, as the benefits of these AI improvements that we are bringing to our traveler customers have been built on the foundational relationships we have developed with our suppliers over many years. Independent hotels and alternative accommodation partners generate the vast majority of our room nights at Booking.com.
Another way to look at this is the ten largest global hotel chains account for only a low double-digit percentage of room nights at Booking.com. So many of our partners do not have significant resources. The value we provide to them is to improve their business by enabling them to have incremental travelers from around the world at lower cost, and by providing services and expertise they may not be able to develop on their own.
For example, small and even medium-sized accommodation providers are generally not able to efficiently market themselves globally. Our brand and marketing reach, supported by years of investment in machine learning and AI, helps connect partners' offers with travelers across markets and channels. Partners benefit from that reach without upfront marketing costs, paying us only when they earn revenue for a room night that might otherwise have gone empty.
To help our partners, we provide them with sophisticated data and tools to better understand travel demand patterns and improve their performance. And we provide different products, like Genius, that offer them opportunities to be more competitive. Our value goes beyond just showing a property to a traveler with advice on how to display it to improve conversion. We provide payment services. We provide customer service in over 40 languages, with both AI agents and people available around the clock.
Our dedicated Partner Services teams are on the ground, across the world, working directly with properties to help them improve their operations. Local knowledge matters. Traveler preferences, payment methods and regulations vary widely from one market to another. Payments are a good example. Travelers want to use methods they know and trust, even when those methods are unfamiliar to the property where they are staying. Today, we can process more than 100 payment methods in over 50 currencies.
That helps properties welcome guests from around the world without having to manage that complexity themselves or lose bookings because they cannot accept a traveler's preferred payment method. This combination of global reach and local expertise supports our growth in markets where we see significant opportunity. The U.S. and Asia are two such important priorities.
In the U.S., we have mentioned in the past seeing significant room to grow over the long term. We have invested in product, supply, brand, marketing and technology to build a stronger offering over the past several years. And our progress is clear. We have outperformed the broader market in terms of room night growth for the last 3 years as we have deepened direct engagement and more travelers have chosen to book multiple parts of their trip on our platform.
These results reflect the consistent execution of our strategic priorities and reinforce my confidence in the opportunity ahead. Asia is another important area of growth. Its many distinct markets call for local execution, and we believe Booking.com's global reach and Agoda's local expertise position us well to deliver it. Across the region, we continue to invest in products, payments, marketing, distribution and supply relationships that reflect how people travel in each market.
As we discussed last quarter, that can mean adapting payment options, working with local properties or reaching customers through the social and messaging platforms that they use every day. These investments help us better serve travelers and partners while supporting our long-term growth in the region.
Across all of our markets, we are focused on building relationships that extend beyond a single booking. We want to help travelers with more of their trip and give them more reasons to choose us again for the next one. Our Connected Trip efforts and Genius loyalty program are central to that goal. Travel can be fragmented. A trip may involve accommodations, flights, ground transportation and attractions, often with different providers.
By bringing these pieces together, we can engage travelers earlier, help with more of their trip, and seek to build a stronger relationship over time. Genius adds value for travelers and encourages them to return to Booking.com. And we are seeing progress on both. Connected Trip transactions, where a traveler books more than one travel vertical with us for the same trip, grew three times faster than Booking.com's overall transactions, from a relatively smaller base.
Those travelers also tend to return more frequently. Higher-tier Genius members plan further ahead, return more consistently and book directly at a higher rate than non-Genius travelers. Over the last 12 months, Level 2 and Level 3 members represented more than 30% of Booking.com's active customer base and accounted for a high-50% share of room nights, up from a year ago.
In closing, our teams executed well in the third quarter, delivering solid results while advancing the priorities I discussed today. I want to thank them for that work. The pace of change in technology is accelerating, and therefore the pace of change in travel is also accelerating. AI is creating new ways for people to discover and plan trips, compare various travel options, and do it all in an easier way. And we are building quickly to continue to help shape that future.
Through it all, though, our mission remains the same, to make it easier for everyone to experience the world. We have spent years building the brands, partner relationships and services that help us deliver on that mission. We help travelers turn ideas into trips that they can book with confidence, and our services help our partners welcome customers from around the world.
However a traveler begins their travel inspiration and planning, we see opportunities to make the whole travel process better, easier, with less frustration and anxiety. In the end, it comes down to providing more value to both sides of the travel marketplace. That is the work our teams are focused on. It is why I am confident in the future of Booking Holdings. With that, I'll turn the call over to Ewout to discuss our financial results and outlook.

**Ewout Steenbergen** (Executives):
Thank you, Glenn, and good afternoon, everyone. I will now review our results for the third quarter and provide our current thoughts for the fourth quarter and full year. All growth rates are on a year-over-year basis, and the reconciliation of non-GAAP to GAAP financials can be found in our earnings release. I'm pleased to report that room nights, gross bookings, adjusted revenue and adjusted EBITDA all exceeded the high end of our guidance for the third quarter.
We delivered profitable growth in a complex macro and travel environment, while investing in our long-term priorities. Our results reflect the fundamental strength of our global business and the continued focus and discipline of our teams. Travel demand was resilient in the quarter, although we saw some moderation towards the end of the period. Prices increased as we saw constant currency ADRs up approximately 3% year-over-year, primarily driven by Europe but also by the U.S. and Asia.
We saw a slight expansion in the booking window in Europe and at the global level, while the booking window in the U.S. modestly contracted. Average length of stay increased year-over-year for our business outside Asia, as Asia domestic travel outpaced international travel by the widest margin of any region.
Now let's turn to our third quarter results. Room nights grew 7%, up from the 5% in the second quarter, driven by an improvement in international travel from bookers in Europe and Asia, while domestic room night growth was stable at a higher level. Globally, domestic room nights grew high single digits, and international room nights grew mid-single digits. We continued to navigate the indirect impacts of the conflict in the Middle East, with elevated airfares and reduced capacity on certain routes weighing on long-haul travel demand.
Looking at room night growth by booker region, Europe grew high single digits, with domestic room nights up high single digits. Asia grew high single digits, with domestic room nights up low double digits. The U.S. grew mid-single digits, driven by domestic room night growth. We were pleased to see another consecutive quarter of direct channel growth in the U.S. Rest of World grew mid-single digits, which was stable from the second quarter as we continued to see growth from bookers in the Middle East.
Over the past four quarters, our B2C direct mix remained stable in the mid-60% range as room nights booked through the direct channel continued to grow in line with the rest of the business, while the mix of room nights coming from direct visits to our websites and mobile apps increased year-over-year. LLM referrals have accelerated over the last several weeks but still account for significantly less than 1% of Booking.com's room nights.
Organic referrals increased following the release of the latest ChatGPT models, which improved citation rates and drove more traffic to our platforms. Paid referrals are also growing as we continue to partner with OpenAI by expanding into additional markets, and testing and refining our approach. The mobile app mix of total room nights over the past four quarters was in the high-50% range, up from the mid-50% range a year ago, and the mix of Booking.com room nights booked by travelers in Genius Levels 2 and 3 was in the high-50% range, which also increased from a year ago.
What is particularly encouraging is the behavior of travelers who engage with Booking.com across all three dimensions: booking directly, using our mobile app, and participating in Genius Levels 2 and 3. Room nights booked by this cohort grew meaningfully faster than those booked by other travelers, both in the third quarter and year-to-date. These trends reinforce our confidence in the investments we are making to deepen our direct relationships with travelers.
And we believe our broader selection of accommodations, flights and attractions, together with progress in payments, the Connected Trip and more personalized and proactive AI-powered experiences will give travelers even more reasons to choose us and return for future trips. Alternative accommodations represented approximately 37% of Booking.com's room nights, up about 1 percentage point from the third quarter of 2025, with room night growth of 7%, improving from 4% growth in the second quarter as we saw an acceleration across all of our major regions.
We also saw alternative accommodation listings growth accelerate to 9%, which is an encouraging signal for our future growth in this category. In our other travel verticals, flight tickets increased 19% year-over-year, a strong acceleration from the second quarter and ahead of the broader market, despite continued pressure from elevated ticket prices and reduced capacity on certain routes. Attraction tickets grew 24% year-over-year, also an acceleration from the second quarter.
Importantly, Connected Trip transactions' growth accelerated to almost 20% year-over-year, and represented a low double-digit mix of Booking.com's total transactions. This share has increased substantially over the past few years as we have expanded our supply across travel verticals beyond accommodations. We expect further increases as we deliver more personalized and GenAI-powered experiences and bring these offerings together more seamlessly through our Genius loyalty program.
Our data shows that travelers who book with us across multiple travel verticals return more frequently, reinforcing our confidence in the Connected Trip opportunity. Our total merchant gross bookings represented approximately 75% of total gross bookings, up about 3 percentage points year-over year.
Our merchant payments platform is a key enabler of our Connected Trip vision, providing travelers with a more seamless and flexible booking experience, helping partners accept customers' preferred payment methods, and generating incremental contribution margin dollars for our business. Total gross bookings increased 10% year-over-year, or approximately 11% on a constant currency basis.
Constant currency gross bookings growth was approximately 4 percentage points higher than room night growth, primarily reflecting the higher constant currency ADRs and the contribution from flights and other verticals. Adjusted revenue increased 9% year-over-year, or approximately 10% on a constant currency basis. Adjusted revenue as a percentage of gross bookings was about 15 basis points lower year-over-year due to a higher mix of flight bookings and the timing of bookings versus travel, partially offset by higher revenues from facilitating payments.
Marketing expenses increased 11% year-over-year, slightly faster than gross bookings, driven primarily by faster growth in B2B affiliate marketing expenses. Excluding our B2B affiliate business, our B2C business had marketing leverage in the quarter as we continue to aim to grow our topline metrics faster than marketing investments. Adjusted sales and other expenses were 2.0% of gross bookings and were a source of leverage.
Efficiencies in third-party customer service, supported by AI-enabled tools, more than offset higher payment expenses associated with our increasing merchant mix. Disciplined cost management continued to support operating leverage in the quarter. Adjusted fixed operating expenses increased 6% year-over-year, reflecting actions we have taken to manage our cost base.
As our use of generative AI scales, we are applying the same cost discipline, including price caps on higher-cost models and model routing simpler tasks to more cost-effective models. For example, at Agoda, our blended cost per million AI tokens declined by more than 25% between June and September. For the company overall, developer productivity continued to improve, while cost per merge request declined double digits.
These gains are helping us deliver new capabilities faster, including several Glenn highlighted in his opening remarks. Adjusted EBITDA of approximately $4.6 billion grew 9% year-over-year. We delivered 9% adjusted revenue growth while expanding our adjusted EBITDA margin slightly to 47.0%, including stock-based compensation as an expense, a powerful combination of growth and profitability that underscores the strength of our business model and disciplined execution.
Adjusted EPS of $4.66 per share increased 17% year-over-year, faster than adjusted EBITDA growth, helped by a 7.5% reduction in our average share count. We continue to execute on our Transformation Program and remain on track to achieve the full $650 million in annual run-rate savings in 2027. We incurred approximately $23 million of transformation costs in the third quarter, the majority of which were excluded from our adjusted results.
Now on to our cash and liquidity position. Our third quarter ending cash and investments balance was $16.2 billion, compared to $17.7 billion at the end of the second quarter. During the quarter, we generated free cash flow of $1.1 billion, which was impacted by a working capital decrease driven by a $3.6 billion seasonal unwind of deferred merchant bookings. We also returned $2.4 billion to shareholders, including $2.1 billion of share repurchases.
During the first nine months of 2026, we returned $10.5 billion of capital to shareholders, including $9.5 billion of share repurchases. We remain committed to a disciplined capital allocation framework, investing behind the highest return growth opportunities across our business while also actively returning capital to shareholders and maintaining a strong balance sheet. 
Moving to our thoughts for the fourth quarter, the travel environment is mixed. As I mentioned earlier, we saw some moderation in global demand trends toward the end of the third quarter, driven by international travel. Domestic travel continues to hold up as we are seeing travelers take shorter trips and choose destinations closer to home.
In October, a number of external factors have also affected demand, including disruptions to travel to and from the Middle East, the conflict's broader indirect effects such as elevated airfares, and localized unrest in certain European cities. Our guidance reflects these near-term disruptions and assumes that both the direct and indirect impacts of the Middle East conflict on travel persist through the end of the year.
Our guidance also assumes recent FX rates for the remainder of the year, including the Euro-U.S. Dollar exchange rate at $1.12. We estimate changes in FX will negatively impact our fourth quarter reported U.S. Dollar growth rates by about 2 percentage points. For the full year, we estimate changes in FX will positively impact reported growth rates by about 1 percentage point for gross bookings and about 0.5 percentage point for adjusted revenue.
We currently expect fourth quarter room nights to increase between 1% and 3%, reflecting the toughest prior-year comparison of 2026 and the uncertainty around the impact of recent events on travel demand. We currently expect gross bookings to increase between 2% and 4%, or between 4% and 6% on a constant currency basis, which is higher than room night growth due to higher constant currency ADRs and flight ticket growth.
We currently expect adjusted revenue to increase between 0% and 2%, or between 2% and 4% on a constant currency basis, slower than gross bookings due to flight bookings mix and differences in the timing of bookings versus travel, partially offset by higher revenue from payments.
We currently expect adjusted EBITDA to be about flat year-over-year, or up about 2% on a constant currency basis, and to be impacted by increased planned investments behind our long-term strategic priorities, including expanding capabilities across non-accommodation verticals such as flights, attractions, and dining; advancing our AI capabilities; and enhancing our underlying technology infrastructure and platforms. We expect these investments to be partially offset by marketing leverage.
For the full year, on a reported basis, we continue to expect gross bookings, adjusted revenue, and adjusted EBITDA to be up high single digits, and adjusted EPS to be up low to mid-teens. At the high end, this outlook is broadly in line with our long-term constant currency growth ambition of at least 8% for gross bookings and adjusted revenue, and 15% for adjusted EPS.
In conclusion, our third quarter results demonstrated the resilience of our global platform and the disciplined execution of our teams in a dynamic environment. We continue to focus on key areas that we believe can further strengthen our long-term growth outlook, including expansion in key markets, deepening traveler relationships through Connected Trip and Genius, creating greater value for our partners, and advancing our approach to AI.
As agentic AI evolves, we're taking a multi-pronged approach. First, building our own AI-agent powered experiences; second, participating in new distribution channels that bring incremental demand at attractive economics; and third, using AI to improve customer service, developer productivity and operating efficiency. We believe Booking Holdings is well positioned to win as the landscape evolves.
Our confidence is grounded in the capabilities that matter when inspiration turns into an actual trip: extensive supply, real-time price and availability, trusted brands, attractive loyalty programs, payments and service capabilities, and longstanding relationships with travelers and partners. We believe these will create economic value both within our own platforms and through emerging channels, supporting sustained growth and attractive returns over time.
With that, we'll now take your questions. Operator, will you please open the lines?

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Doug Anmuth with JPMorgan.

**Douglas Anmuth** (Analysts):
I have 2. Just first on the tangible AI progress that you're seeing in brands. Obviously, good to see the customer service cost efficiencies. Is there anything that you can share in terms of some of the top line benefits perhaps that you're seeing around either conversion rates or frequencies or just other ways to quantify? And then on those accelerating AI referrals in recent weeks, are you seeing any differences in some of the newer agents like Muse and Grok Bot relative to what you saw previously with kind of the other LLMs?

**Ewout Steenbergen** (Executives):
Doug, this is Ewout. First, on some of the tangible AI progress. There are 4 key categories where we see some positive early indicators. So let me explain that and give a couple of examples around that. First, we're seeing higher engagement. So examples here are Booking.com's daily AI search visitors are up 10x with trip search in the third quarter compared to the second quarter.
And second example here is our new Vayo platform users are connecting their e-mail, and we're seeing strong conversational engagement with Vayo at the moment. Second area is higher conversion. So a couple of examples, again, Priceline's Penny and Agoda's AI Assistant users have converted at approximately twice the rate of non-users. Third area, higher booking value. We see Agoda's AI Assistant users have an average booking value of approximately 20% higher than non-users. And the fourth category is incrementality.
So -- again, some examples. OpenTable's native integration with OpenAI has become one of the brand's fast-growing channels and had in September 190,000 seated covers and then OpenTable's agentic interactions with Muse and other horizontal agents have brought a significant number of completely new customers to our platform. So 4 key areas where we see improvements and really positive indicators, higher engagement, higher conversion, higher booking value and incrementality.
It's early days, but we're encouraged by the momentum, and we really think these are really nice positive uplifts on these metrics. In terms of your question around referrals from LLMs versus the newer horizontal agents, what we are seeing that this traffic is still very small in aggregate. So nothing is really jumping out there in terms of one that is growing faster than another.
So it's still very small. Yes, we have seen some acceleration in the recent weeks, but it's still significantly below 1%. I also would like to point out that the vast majority of that traffic is coming to us, and that is based on third-party data sources. So we're not missing out on the traffic, but it's still really small.

**Operator** (Operator):
Your next question comes from the line of Mark Mahaney with Evercore ISI.

**Mark Stephen Mahaney** (Analysts):
Two questions, please. I know you've got this partnership with Muse and with Agoda in Asia. And just what's the -- just talk a little bit about the strategy of -- you've got 3 sort of global brands. Why work with Muse with Agoda versus one of the others? And then the marketing deleverage in B2B. And I think that's been the case for a quarter or 2 or 3. I think you're leaning into this as a channel. Could you talk about any signs of traction, success, more momentum you're getting just in the B2B segment?

**Glenn Fogel** (Executives):
Mark, why don't I take the first one, and I'll let Ewout take the second one. So it's interesting which agreements with whom we get done first and priorities, et cetera. Look, I think the important thing to recognize is that we are working with everybody all the time. Some things are going to happen faster than others. Some things get completed faster than others.
But you should not think just because we have Agoda getting the launch in Singapore is somehow more important than what we end up in the U.S. with Muse or anyone else. Please don't misinterpret that. And I have confidence that we'll have great relationships with all the players and not just the ones that you know of now because we know there are a lot more coming down the road.

**Ewout Steenbergen** (Executives):
Mark, with respect to your second question, with respect to B2B marketing deleverage, so let me point out the following. So we are pleased, of course, with third quarter marketing leverage for B2C and also, of course, pleased with the growth of our B2B business volumes. So specifically, your question about B2B, yes, that is a business that is getting more focus and attention internally. I think you know about our plans that we're launching on January 1, a combined B2B business.
So you will also see then more details about the numbers because most likely, we will break that out going forward. What is happening there is if the business is growing and they are reporting more revenues, usually the commission structures are based on a rev share. So therefore, also the rev share and the commissions are going up, and that is flowing through the marketing line. But that's for a good reason because if that is going up, it means that from an economics perspective, it's also very healthy for the company.

**Operator** (Operator):
Your next question comes from the line of Matt Cost with Morgan Stanley.

**Matthew Cost** (Analysts):
I'm sure you've seen data out there showing that a lot of the commercial activity that's happening on these early agents is skewing towards travel. And I guess to the extent that you're seeing that come to your brands, should we view that as something that is just a convenience for people who are going to book travel already? Or is there an aspect here where by removing friction from a very complex purchase process, there may actually be incremental demand that's engendered by these tools?

**Glenn Fogel** (Executives):
So that is an interesting thing. And we are seeing the data you're mentioning, lots of people using these personal agents or any form of AI to do travel discovery. It's easy. It's interesting. People like to do travel discovery throughout all the time. It doesn't end up with a lot of bookings as we -- Ewout mentioned, we're getting -- the referral numbers are pretty darn small, and we believe we're getting a good number of the total number out there. So what does it mean for us, though?
Over time, it may end up being another perhaps significant way that we get business the way we've gotten business in the past from other people who had a front door of discovery. It may be making it easier for people, less friction to try and learn what they need to do. So perhaps we end up with things that are actually going to convert at a higher rate. We believe it's important enough that we're coming out with things like Vayo, like Lola and all our brands coming out with things, too. So people can come to us first.
And look, what I really want to do is complete our connected trip using AI to make it easier, provide more value to the consumer so that when they are thinking of travel, they always want to come to us first. And we know we're not going to get everyone. But we absolutely believe that we should, with the technology capabilities that we have, with the capital we have, with the resource we have, with the relationships with the suppliers, so we can help provide more value to the consumer.
And of course, that customer service that is so important, being able to make people able to trust that when they come to us, they're going to be able to have the best experience in their travel. Those types of things are really important. I believe this is actually a wonderful thing that there could be much more of a fragmentation of the way people are beginning their discovery that enables us to actually be able to obtain customers at a lower cost. We could see that happen. Ewout, anything you want to add to that?

**Ewout Steenbergen** (Executives):
Just to say one more thing is strategically, of course, these new channels are important for us because it gives us an opportunity for diversification of third-party channels, and that ultimately will drive an economic advantage to us. We have been talking about that in the past, but I think that is already really showing up in practice because clearly, there are many AI platforms now, many AI tools, agentic tools out there.
They're still figuring out their economic model. They haven't really come to a conclusion there because the competition is very high. And we get the vast majority of the traffic because they like to connect to aggregators, that is much better for them, and that is good for us. But from an economics perspective, the diversification looks like it's going to be a positive for us at the end.

**Operator** (Operator):
Your next question comes from the line of -- I'm sorry, of Alex Brignall with Redburn Atlantic.

**Alex Brignall** (Analysts):
I'll ask a follow-on on that previous question. It's something I've asked in the past about fragmentation. You're obviously seeing some B2C leverage. If you could talk about the components of that, that would be very helpful. And then sat over here in Europe, we have obviously and specifically Continental Europe, seen the DMA impact on Google's search results, which have thrown a bit of a spanner on what they can display when people search for travel. I wonder if you could give us some thoughts on that and how it might affect your numbers.

**Ewout Steenbergen** (Executives):
Alex, with respect to our B2C leverage, nothing is different than what we have always done. We're managing that in a disciplined way. We see 2 advantages there flowing through. One is we're always trying to drive up higher ROIs in our paid channels. And then also what we are seeing is that the direct traffic is up at the same time.
So both in combination are helping us to achieve B2C marketing leverage in the third quarter. And also, we are looking at the possibility to deliver on marketing leverage in the fourth quarter as well. So this is always our standard, what we are going after. Glenn, do you want to take the question about Europe, the DMA and Google?

**Glenn Fogel** (Executives):
Yes, I'll talk a little bit about that. We -- right now, we don't see any great advantage from this change. Obviously, it's early, et cetera. We haven't seen anything in terms of numbers change. I know some people have been talking about that, oh, it's going to be such an advantage for the OTAs. I hope it is. I haven't seen it yet. We'll see. What's interesting, though, since you mentioned DMA, it gives me an opportunity to talk about something that I don't see a lot of people writing about.
And that talks about the regulatory framework in many parts of the world, particularly in Europe and how these personal -- these horizontal personal agents are going to be able to do things or not. What sort of access they're going to be allowed to have in terms of personal information, what sort of requirements are going to be, what's going to be allowed in being a commerce platform along with being an advertising platform. It's very complex.
There's a lot of regulatory stuff out there, whether it be the DMA or the EU AIA or the DSA or the VLOP laws or you get into the U.K., and I saw something that one of the senior executives, I think it was out of the treasury. It was regarding the FCA, I think, in terms of being able to allow to do monetary things in Muse or not. I think there's parts of the world where the adoption of these horizontal personal agents may be much slower than is anticipated. And we'll see what that may mean. For ourselves, we don't know, but it is interesting that I don't see a lot of people talking about that.

**Operator** (Operator):
Your next question comes from the line of Justin Post with Bank of America.

**Justin Post** (Analysts):
A couple on agentic. I think in addition to economics, one of the concerns is they might be preferencing direct sites versus OTAs. Are you seeing any evidence of that? And what can you do to really improve your relevance in AI results? And then second, just thinking about the cost increases in Q4. I think there's some questions on how you're thinking about investment in '27 and what that could do to your algorithm. Any help with that would be very helpful.

**Glenn Fogel** (Executives):
So I'll talk a little bit about the first question. I'll let Ewout talk about investments going forward. So it's interesting you say that because I haven't -- I've heard some of that, but I see other things, too, where the OTAs are actually getting a greater advantage right now. Here's the end -- the real story is, and this is the way we believe we need to play it is, you got to provide more value, whether it be to a human traveler or to the agent, such that the agent, we want that agent or that person to be using us, looking at our stuff, going through us, transacting with us.
If we are able to do that, in the long run, we will have a competitive advantage. And that's really the way it is. Now one of the things that we provide is to the small independents, and Ewout mentioned a little bit about that, how a very small percentage of our business comes from the big hotels. And so much of it is the small, medium-sized ones who don't have the resources, who absolutely are afraid that in the new world, they won't be seen at all.
But that's okay because we're there to provide them what they need. That's what we've been doing for the -- almost 27 years I've been at this company is providing value to our partners, being able for them to get incremental travelers because they could not, whether it was 20 years ago, go online and have a website or then they don't have an app or now it's how do I show up in an LLM? How is an agentic horizontal going to find me, see me or whatever.
We are there to provide it for them, and we do it at a risk-free rate. Essentially, they don't have to pay anything unless they get a head in the bed, and that's what we are able to do for them. So I absolutely believe that we have an advantage. So this is a great time for us now being able to use our technology, all these things to be able to provide even more value to both the travelers and the partners, and I see the future is very bright. So Ewout, do you want to talk about investments needed to achieve all this?

**Ewout Steenbergen** (Executives):
Yes, Justin, let me give some commentary about the fourth quarter, and you also asked about 2027. So first, about the fourth quarter. Our philosophy is to make disciplined investments for the long term of the company while also protecting profitability in the near term. So from a big picture perspective, I think everyone knows that we have already industry-leading EBITDA and EBITDA margins, and that is on a fully loaded basis. So we're not capitalizing a lot.
We have a fully loaded expense base, including stock-based compensation. We don't understand how people are pulling that out. That's a real cost of running your business. At the same time, we also have strong execution and discipline regarding the delivery on our productivity programs, efficiency targets, operating leverage. And that is then offset by increased investments in strategic initiatives, and those were planned in the fourth quarter at a higher level.
But obviously, we have attractive business cases underneath. I also would like to point out that our full year EBITDA margins, we expect to be stable. So with respect to 2027, it's a bit too early to provide commentary. We'll do that in February with our fourth quarter results. But what I can say is that we remain confident with respect to our long-term growth outlook, and we will stay disciplined how we are planning to invest in the business also next year and in the future.
Maybe one thing to throw out for 2027, and this is not related to cost, but more on the commercial side. It's a very early directional indicator. So it's still subject to change, like cancellations and others. But if you look at our on-the-book statistics for the first half of 2027, that actually looks healthy. So that gives us confidence in the outlook for next year.

**Operator** (Operator):
Your next question comes from the line of Ron Josey with Citi.

**Ronald Josey** (Analysts):
Glenn, I wanted to go back to your comments on just applying the learnings from Lola and Vayo and sort of using Booking's platforms as a testing ground. Just talk to us about the metrics insights you're looking for from those tools and the other AI tools that you have before applying the learnings. And then we sort of just talked about it, but I'd love to hear your thoughts on just the value of the supply that Booking has as agents become a larger part or potentially a larger part or a new front door for the internet overall. So just the value of Booking supply.

**Glenn Fogel** (Executives):
Ron, so in terms of what we use in terms of learnings and why we started up 2 greenfield operations to be able to come up with a new agentic way to do our travel business in 2 different ways, 2 different companies doing different -- I mean, they're not the same, you're probably reading about what they're doing. The way we do this is seeing what customers like, what is converting well, what people are signing up for, whether or not, for example, they -- will they take an e-mail?
Will they have the whole e-mail history in the thing or not? Well, we've learned that actually, yes, most will, which is really good to know. And that's how we do it. Now in terms of the actual specific metrics, I'm not going to go around and get into the details of how we're going to do it. But obviously, when we see things that are working, that is such a value to bring to the much bigger companies, Booking, Agoda, Priceline and being able to transfer that so that they can then take the advantage of doing that.
It really is a wonderful place to be when you have the capabilities, the capital, the resources, the number of people that you can afford to do this type of agile creating new things and being able to test it out and then test bed type stuff, come bring it back when it's working or don't bother. And it didn't hurt you because you tried it on a much bigger platform and it wasn't working. So that's on that one. In terms of supply, what is the value -- I make sure I got you right, Ron, if you're asking, what value do we provide to the supplier in a new AI world? Is that -- was that the question?

**Ronald Josey** (Analysts):
More like the other way around. So in other words, when we do our searches on Muse, we see Booking show up, whether we're looking for a hotel in Panama City, Panama or in Paris, for example. And so Booking inherently is always there. And I think that's because of the supply, but I wanted to get your thoughts there.

**Glenn Fogel** (Executives):
Yes. Why are we showing up more there than others or that? That's a hard thing to say. I think we have a lot of theories about why the models are choosing us. We believe it has a lot to do with the level of the content, the reliability of it, the value that the way the models go look through and see what value this content provides. Truth is, though, there is no handbook on how do you show up more in an LLM, how do you show up more in a personal agent or not. In the end, what we really want is what I said earlier, though, and this is being able to provide the more value.
So the agents, when agent to agent, our agent is talking to the personal agent, the horizontal and really being instantly giving all the reasons, it's better -- and it's not just price, of course, all the elements that we've talked about over the last 40 minutes or so about what we provide to the traveler and to the partner, that is the best place to do this travel in such a way that the horizontal agent recognizes it and is recommending or saying, do it here because this is best. That's what we want to achieve.

**Ewout Steenbergen** (Executives):
If I can add a few elements there, Ron. I think brand credibility is a very important element. So I think that's why those horizontal agents want to work with us because it gives them instant credibility being associated with our brand. As I said before, they like to partner with aggregators.
It's going to be very expensive for them to connect to 4.7 million properties directly and get all the information about real-time data, pricing, availability, so they can get that through us and immediately have also the possibility in the future of a potential monetization model with us. So those are a couple of reasons why we think that we are showing so much up on those platforms.

**Glenn Fogel** (Executives):
And just to add to Ewout's point, if these horizontal agents do go down the route of some type of monetization that is not dissimilar to what we have been doing over the last 2 decades, we will be even in a better position.

**Operator** (Operator):
Your next question comes from the line of Benjamin Black with Deutsche Bank.

**Benjamin Black** (Analysts):
So Genius has become a much larger part of your transaction mix. So can you dig into how you're thinking about the next evolution of the program and how you can deepen loyalty without maybe becoming more reliant on supplier-funded discounts? And then maybe a follow-up on the 8-8-15 framework.
As AI begins to drive real efficiencies across customer service, across engineering, across other parts of the cost base, does 15% still seem like the right long-term sort of EPS algorithm? Or is there a scenario where AI-driven operating leverage allows you to outperform that framework without even driving faster top line growth?

**Glenn Fogel** (Executives):
Thanks, Benjamin. I'll take the first and I'll let Ewout take the second there. It's -- to be fair, repeat that first one again, gives me a little more time to think exactly how I want to answer it.

**Benjamin Black** (Analysts):
Yes, it's really about Genius and how you're thinking about evolving it from here. It's already become a much larger part of your transaction mix.

**Glenn Fogel** (Executives):
Yes. All right. So here's, I guess. And I've kind of teased this out a little bit in the past. I just want to be very careful what I say. We are going to improve Genius. It's going to be an even better program down the road. I absolutely believe, and as I said earlier, I said it several times now, the issue, the importance of providing value, providing value to that traveler and it's also value to the partner. Genius works right now very well because the partner is funding a lot of it and is getting a good ROI out of that.
And of course, the traveler is getting a great deal, too, because they get a lower cost for their holiday. So it works both ways. But there are a lot of other ways we can improve upon that tremendously. There are other things that travelers want and maybe the partner will be willing to give it up either at no cost because there's very little marginal cost to them or perhaps, they'd be willing to do it at a lesser cost that we can help work with.
These are ways we have to think about down the road is how do we continue to make sure that we are giving more value and in a way that travelers who use us get even more value because they use us loyalty, spend more with us, stay with us more, do things more with us, get more benefit, continue to do that in a way that it creates a flywheel effect and continues to grow.
Now, not going to give away when we're going to bring out what or what they're actually going to be, but I absolutely recognize the importance of continuing to come up with a differentiating value that enables us to continue to show up as the better way for the traveler to use us and for the partner to participate. And Ewout, I think the question about the algo is yours.

**Ewout Steenbergen** (Executives):
Yes, Ben, with respect to the 8-8-15 and the benefit from AI that might flow into that. I think it is a little bit too early to tell you exactly how we will see that changing our long-term algorithm. But what I can say is that we're already moving from experimentation to measurable operating value across the company coming from AI. So in a couple of areas.
First, we are fundamentally improving the travel experience for our traveler customers, think about engagement, think about conversion, think about booking value, think about incrementality and some of the examples that I gave earlier during this call. Then we have been speaking before about the benefits, for example, in customer service, where the average cost per booking are coming down and the customer satisfaction remains high and also in our engineering groups where the average cost per merge request are coming down in a significant way.
And then the third area is our headcount growth has been very minimal over the last 2 years, and that has been mostly in lower-cost locations like our center of excellence in India, where we also can find great talent. So we're pleased that we're already seeing some tangible results, but it is a little bit too early to exactly determine in which way that will impact our long-term algorithm.

**Operator** (Operator):
We have time for one last question, and that question comes from the line of Meredith Jensen with HSBC.

**Meredith Prichard Jensen** (Analysts):
I just had one question, a little bit related to the last, but potentially a smaller piece of the pie. But if you might talk about a little bit of the changes in the distribution landscape and how it might open some new doors for Booking and hotel suppliers and ways that they could collaborate, particularly around loyalty programs and guest recognition. So if you could -- I know, Glenn, you've spoken a little bit about this in the past in interviews, and I would just love some updated thoughts.

**Glenn Fogel** (Executives):
So Meredith, so I make sure I understand your question. You'd like to know a little bit more about how in terms of recognition for the suppliers in the process? Or are you talking more for the travelers?

**Meredith Prichard Jensen** (Analysts):
Just if there's -- the loyalty program connectivity between some of the hotel programs to, if they book through Muse and Booking is the connector, how that kind of could play out over time because everything is moving so quickly.

**Glenn Fogel** (Executives):
It is. It absolutely is. And that's one of those interesting questions in terms of networks and how do you create a loyalty program, so you have more and more people who want to participate in it gives more value. We all know the value of a network and the more nodes you have, the exponential increase in the value of that network.
So absolutely talking with hoteliers, talking with every travel player and non-hotelier players, non-travel players, people outside the travel ecosystem and figure out ways, again, in these types of loyalty programs, you can actually though give more value to both the person who is participating, the traveler, and anyone who's on the other side supplying some type of service or product.
We absolutely believe that's an important part of helping build out and ensure that the Genius program remains one of the most valuable programs there is and the reason people will want to come. And again, I don't want to give away too much of what we're building down the road, but we absolutely understand the need to continue to provide more value to both sides of that network. Is that helpful?

**Meredith Prichard Jensen** (Analysts):
Yes.

**Glenn Fogel** (Executives):
Well, I guess that was our last question. So let me conclude. First, as always, I want to thank our employees for their dedication and strong execution. I want to thank our shareholders for their continued support. And of course, I've got to thank the travelers and the partners who place their trust in us every day. I and we, together, we are so excited about the role AI is going to play in travel, and I'm absolutely encouraged by the progress we are making across our strategic priorities.
Look, we're going to continue to navigate this near-term uncertainty with the discipline that we've always had, and we're going to be investing thoughtfully in the opportunities ahead. Our people and the capabilities we continue to develop gives us the confidence in our ability to continue to play a leading role in shaping the future of travel and delivering lasting value for our shareholders. Thank you very much, and good night.

**Operator** (Operator):
Ladies and gentlemen, this does conclude today's conference call. Thank you for your participation, and you may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### BKNG_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜Ewout Steenbergen｜guidance：Q3 guidance: room nights +3% to 5%; gross bookings, revenue, adj. EBITDA each +4% to 6%.（原話："expect third quarter room nights to increase between 3% and"）
- 2026-08-04｜Ewout Steenbergen｜guidance：Full-year reported guidance: GB, revenue, adj. EBITDA each up high single digits.（原話："to each be up high single digits and for adjusted EPS"）
- 2026-08-04｜Ewout Steenbergen｜guidance：Adj. EPS full-year guidance is low to mid-teens growth; GB expectation lowered vs prior.（原話："Our expectation for gross bookings is lower than our prior"）
- 2026-08-04｜Ewout Steenbergen｜guidance：GB cut is attributed to flight ticket growth; accommodation outlook unchanged.（原話："primarily due to lower flight ticket growth"）
- 2026-08-04｜Ewout Steenbergen｜guidance：FX assumed to add to full-year reported growth.（原話："we estimate changes in FX will positively impact full year"）
- 2026-08-04｜Ewout Steenbergen｜guidance：Guidance assumes stable travel environment.（原話："Our guidance assumes stability in the broader travel"）
- 2026-08-04｜Ewout Steenbergen｜guidance：Full-year guidance in line with long-term algorithm, assuming 7 of 12 months Middle East impact.（原話："that is still in line with our long-term algorithm"）
- 2026-08-04｜Ewout Steenbergen｜risk：Guidance assumes 7 of 12 months of Middle East impact.（原話："we have 7 out of 12 months impact of the Middle East"）
- 2026-08-04｜Ewout Steenbergen｜risk：Q2 Middle East impact was said to be a bit higher than Q1's ~2 point impact.（原話："the impact was actually a bit higher"）
- 2026-08-04｜Ewout Steenbergen｜risk：Q3 Middle East impact expected a bit smaller than Q2 on normalization.（原話："we expect that there will be a little bit less of an impact"）
- 2026-08-04｜Glenn Fogel｜risk：Long-haul international travel pressured by airline prices and capacity.（原話："international travel remained pressured by elevated airline"）
- 2026-08-04｜Ewout Steenbergen｜risk：Booking window and length of stay contracted globally in Q2.（原話："we saw a modest contraction in booking window and length"）
- 2026-08-04｜Ewout Steenbergen｜margin：Adj. EBITDA margin expansion in Q2.（原話："Adjusted EBITDA margin expanded nearly 40 basis points"）
- 2026-08-04｜Ewout Steenbergen｜margin：Marketing expense grew faster than gross bookings.（原話："Marketing expense increased 11% year-over-year, modestly"）
- 2026-08-04｜Ewout Steenbergen｜margin：Revenue growth below GB growth, explained by March cancellations.（原話："Revenue growth was lower than gross bookings growth"）
- 2026-08-04｜Ewout Steenbergen｜margin：Adj. EPS growth outpaced EBITDA growth with lower share count.（原話："Adjusted EPS of $2.54 per share increased 15%"）
- 2026-08-04｜Ewout Steenbergen｜margin：Transformation savings target raised from $550M to $650M.（原話："increasing our expected annual run rate savings from"）
- 2026-08-04｜Ewout Steenbergen｜margin：Additional $100M savings mostly from procurement, existing categories.（原話："mostly came from the procurement work stream"）
- 2026-08-04｜Ewout Steenbergen｜capital_allocation：Q2 debt raised and repaid.（原話："raised $3 billion of debt, paid down $1 billion of debt"）
- 2026-08-04｜Ewout Steenbergen｜capital_allocation：H1 2026 buybacks of $7.4B.（原話："repurchased $7.4 billion of our common stock"）
- 2026-08-04｜Ewout Steenbergen｜capital_allocation：Capital allocation framework stated.（原話："We remain committed to a disciplined capital allocation"）
- 2026-08-04｜Glenn Fogel｜commitment：Management says it does not want surprise AI spending; return or stop.（原話："What we do not want is any surprise"）
- 2026-08-04｜Ewout Steenbergen｜commitment：Management states AI ROI already positive.（原話："already seeing an ROI that is positive on our AI investments"）
- 2026-08-04｜Glenn Fogel｜customer：Genius level 2/3 share of room nights.（原話："accounted for a high 50% share of room nights"）
- 2026-08-04｜Glenn Fogel｜customer：U.S. room nights growth in Q2.（原話："U.S. room nights grew in the high single digits"）
- 2026-08-04｜Ewout Steenbergen｜customer：Connected Trip transactions growth.（原話："Connected Trip transactions grew low double digits"）
- 2026-08-04｜Ewout Steenbergen｜customer：Merchant share of gross bookings.（原話："approximately 73% of total gross bookings"）
- 2026-08-04｜Ewout Steenbergen｜customer：Flight tickets growth in Q2.（原話："flight tickets increased 4% year-over-year"）
- 2026-08-04｜Glenn Fogel｜customer：Alt accommodation growth; wants higher especially in U.S.（原話："4% growth in alternative accommodations, well, I'd like that"）
- 2026-08-04｜Ewout Steenbergen｜competition：SEO described as small component under pressure.（原話："SEO remains a small component of our overall room"）
- 2026-08-04｜Glenn Fogel｜competition：Google AI overview pressured SEO.（原話："Putting in that AI overview probably has done it."）
- 2026-08-04｜Ewout Steenbergen｜competition：LLM traffic share of room nights.（原話："of our room nights. And that hasn't moved so much recently."）
- 2026-08-04｜Ewout Steenbergen｜competition：Booking is in OpenAI CPC test group.（原話："part of the test group of OpenAI for CPC."）
- 2026-08-04｜Glenn Fogel｜competition：Google agentic booking launch with Booking among first.（原話："of our room nights. And that hasn't moved so much recently."）
- 2026-08-04｜Glenn Fogel｜competition：Google moved toward performance marketing ad platform.（原話："performance marketing advertising platform"）
- 2026-08-04｜Glenn Fogel｜competition：Asia described as dynamic competitive environment.（原話："Despite a dynamic competitive"）
- 2026-08-04｜Glenn Fogel｜product：AI referrals described as small contributor.（原話："performance marketing advertising platform"）
- 2026-08-04｜Glenn Fogel｜product：Penny usage still very small; no metrics.（原話："it's still very small, and we're not at a stage"）
- 2026-08-04｜Glenn Fogel｜product：Customer service cost per booking decreasing at double-digit rate.（原話："per booking continues to decrease at a double-digit rate"）
- 2026-08-04｜Ewout Steenbergen｜product：AI costs a low single-digit share of tech spend.（原話："low single-digit level of our overall technology spend."）
- 2026-08-04｜Glenn Fogel｜product：B2B units being merged into one.（原話："let's put it together as one unit."）
- 2026-08-04｜Ewout Steenbergen｜product：B2B incrementality discipline vs B2C cannibalization.（原話："cannibalizing your existing B2C business"）

### 問答異常語氣（迴避／改口／保留）
- BKNG_Q2_2026_Earnings_Call_20260804.md｜問：Mahaney: quantitative evidence AI/Penny improved conversion or bookings per customer?｜答法：Declined to give percentages or CSAT numbers; said still very small.
- BKNG_Q2_2026_Earnings_Call_20260804.md｜問：Kopelman: where did the assumed 300bp Middle East headwind for Q2 end up, and Q3 assumption?｜答法：No bp figure; said Q2 'a bit higher' than Q1 and Q3 'a little bit less'.
- BKNG_Q2_2026_Earnings_Call_20260804.md｜問：Post: why air decelerated and rental cars were down, what it means for Connected Trip｜答法：Answered air only, framed as exogenous; rental cars not addressed.
- BKNG_Q2_2026_Earnings_Call_20260804.md｜問：Walmsley: SEO pressure not called out before; AI search shift or SEM favoring? Traffic going direct to hotels?｜答法：Fogel said 'I don't know, they don't tell me' on hotels; Ewout corrected that SEO was discussed last quarter.
- BKNG_Q2_2026_Earnings_Call_20260804.md｜問：Kopelman: extent of AI discovery testing on Booking.com and learnings｜答法：Said no data yet, gave only impressions.

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
{"date":"20260805","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Connected Trip 由敘事變成經濟：跨垂直交易的附著率持續推進，機票／租車／景點由「留客工具」變成自身有利潤的垂直，讓 BKNG 由住宿 OTA 進化為全旅程平台"},{"id":"H2","text":"Agentic commerce 穿過 OTA 而非繞過 OTA：AI 平台把發現層拿走，但結帳與 merchant of record 留在 BKNG，因此 take rate 不被結構性抽稅"},{"id":"H3","text":"低至中雙位數 EPS 複利可維持 5 年：約 7–8% 固定匯率營收成長 × 每年約 40 個基點 EBITDA 利潤率擴張 × 每年約 4% 淨股數縮減"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"發現層通路稅結構化：AI 平台與搜尋引擎把「被看見」變成永久性收費項目。已在動的三條線——Google AI 概覽壓縮自然搜尋（管理層本季正面承認）、OpenAI CPC 廣告位（BKNG 已在測試群）、以及旅館連鎖自有 AI 訂房工具（Hilton「AI Planner」2026-03 上線、Marriott「Ask Bonvoy」2026-06 上線涵蓋約 10,000 家物業／146 國、IHG 2026-07 起可在自家 AI 對話內以點數／現金／混合方式搜尋並訂房）。最後這條是 BKNG 結構上無法對稱回應的——它沒有忠誠度貨幣。"},{"id":"R2","text":"歐洲法律與監理堆疊的追溯性賠償階段：比價條款之爭已由「禁止未來使用」進入「追溯賠償」。柏林第二地方法院於 2025-12-16 判定 1,099 家德國旅館可就 2013–2024 年的窄式最惠條款求償（金額待後續程序認定）；HOTREC 主導的集體訴訟在阿姆斯特丹審理，參與旅館由 2026-01 的 3,087 家增至 2026-07 底的 10,783 家，預計 2026 秋季達約 18,000 家，求償框架約 €8B、涵蓋 2004–2024 年；西班牙 CNMC 的 €413M 罰款雖獲暫緩執行，BKNG 已提存全額財務擔保；瑞士 COMCO 於 2026-04-30 對旅遊業「品牌關鍵字競價互不出價」開啟調查（歐盟執委會有平行調查）。這不是近期盈餘風險，而是把多年法務成本與和解風險制度化，並永久拿掉 BKNG 用契約手段守住 take rate 的工具。"},{"id":"R3","text":"中東衝突再升溫或蔓延：現行指引假設「情況穩定、間接影響持續至第三季末」。若衝突延長至 2027 或蔓延至紅海航運／台海，全球入境流量可再降 10–15%，全年營收成長可能跌至 +3–5%，營運槓桿反轉。聯合國世界旅遊組織已將 2026 年國際入境成長由原估 3–4% 下修 1–2 個百分點；中東入境 2026 年預估下滑 11–27%。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"starter 1/3 已可建；加碼待 TTM take rate 守住 14.0% 且室夜連 2 季 ≥ +4%，或回落 $180 以下","irr_base_pct":13.5,"ev5y_pct":66.1,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":3.9,"ev5y_pct":66.1,"irr_base_pct":13.5,"max_dd_pct":-52.0,"bull_5y_price":463.0,"bear_5y_price":126.5,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"starter 1/3 已可建；加碼待 TTM take rate 守住 14.0% 且室夜連 2 季 ≥ +4%，或回落 $180 以下","price_at_dd":194.27,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BKNG_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
