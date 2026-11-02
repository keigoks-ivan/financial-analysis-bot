你是 stock-analyst **v20 判斷 agent**，標的 MGA（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MGA","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MGA_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MGA_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_sales","label":"Sales（營收）","value":10059,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"US$百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm"}},{"id":"f_kpi1_adjusted_ebit","label":"Adjusted EBIT","value":683,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"US$百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm"}},{"id":"f_kpi2_adjusted_ebit_margin","label":"Adjusted EBIT margin","value":6.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm"}},{"id":"f_kpi3_income_from_operations_b","label":"Income from operations before income taxes（稅前營業利益，GAAP 口徑；公司未單列 GAAP 營業利益率）","value":552,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"US$百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm"}},{"id":"f_kpi4_free_cash_flow","label":"Free Cash Flow","value":584,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"US$百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm"}},{"id":"f_kpi5_adjusted_eps","label":"Adjusted EPS","value":1.83,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"US$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm"}},{"id":"f_kpi6_diluted_eps_gaap","label":"Diluted EPS（GAAP）","value":1.44,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"US$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm"}},{"id":"f_kpi7_fy2026","label":"FY2026 指引（本次更新）","value":"Sales 41.2–42.0B；Adj EBIT margin 6.3–6.5%；Adj EPS 6.85–7.15（中點 7.00 不變）；FCF 1.85–1.90B","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","unit":"—","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm"},"note":"共識 FY1 EPS 7.04（dd_numbers_extra.py consensus_revision，2026-10-31 快照）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-30","period":"2026-10-30","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-30"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mga_gross_margin_pct","label":"MGA 毛利率","value":14.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mga_operating_margin_pct","label":"MGA 營業利益率","value":5.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mga_fcf_margin_pct","label":"MGA FCF 利潤率","value":7.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lea_gross_margin_pct","label":"LEA 毛利率","value":6.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lea_operating_margin_pct","label":"LEA 營業利益率","value":3.67,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lea_fcf_margin_pct","label":"LEA FCF 利潤率","value":3.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aptv_gross_margin_pct","label":"APTV 毛利率","value":19.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APTV.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aptv_operating_margin_pct","label":"APTV 營業利益率","value":9.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APTV.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aptv_fcf_margin_pct","label":"APTV FCF 利潤率","value":3.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APTV.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_6902_t_gross_margin_pct","label":"6902.T 毛利率","value":15.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6902.T.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_6902_t_operating_margin_pct","label":"6902.T 營業利益率","value":6.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6902.T.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_6902_t_fcf_margin_pct","label":"6902.T FCF 利潤率","value":1.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6902.T.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bwa_gross_margin_pct","label":"BWA 毛利率","value":19.8,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWA.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bwa_operating_margin_pct","label":"BWA 營業利益率","value":10.2,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWA.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bwa_fcf_margin_pct","label":"BWA FCF 利潤率","value":9.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWA.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":65.81,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":12.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":54.43,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.14,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.05 → 7.04）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.13,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.79 → 7.78）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.36,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.39 → 8.36）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":7.04,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":7.78,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":8.36,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":3.38,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 6.81 → 7.04（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":21.44,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝67.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":67.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝96.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":96.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.52,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":9.35,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 7.04，分子＝快照價 65.81","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.256,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":5039.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 6469.0、現金 1430.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":259.66,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":22127.01,"period":"2026-11-03","unit":"USD m","basis":"市值 17088.01 ＋ 淨負債 5039.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":41735.76,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":42283.86,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.53,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 65.96 / W52 60.29 / W104 49.69 / W250 48.96 / W250 13週斜率 -0.19%"},{"id":"f_ma_w52","label":"52 週均線","value":60.29,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":49.69,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":48.96,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-0.19,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Magna FY2025 annual filing says established electronics and semiconductor companies have entered or expanded presence in automotive, and disruptive innovators may offer solutions traditional suppliers cannot match","source":"SEC Form 40-F FY2025 (Magna)","url":"https://www.sec.gov/Archives/edgar/data/749098/000119312526128771/d20215dex991.htm","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Magna Q2 2026 call highlighted new awards: a driver/occupant monitoring system program with a European OEM and an 800-volt two-speed e-drive program with Chery","source":"MarketBeat, Magna Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/magna-international-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Competitor Lear acquired Kongsberg Interior Comfort Systems, IGB and Grupo Antolin seating business to strengthen seating vertical integration (Magna seating peer)","source":"Nasdaq/Zacks, Will Magna's Seating Segment Remain a Core Strength in 2026?","url":"https://www.nasdaq.com/articles/will-magnas-seating-segment-remain-core-strength-2026","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Magna CEO sees opportunity with Chinese automakers","source":"Plastics News","url":"https://www.plasticsnews.com/latest-news/cdb-magna-sees-chinese-automakers-opportunity-20260609/","excerpt":null,"as_of":"2026-06-09","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 40-F：Magna 六大客戶占 2025 年銷售 76%（2024 為 73%），最大客戶 GM 與 Mercedes-Benz 各約 15%；未找到任何客戶導入第二供應商的來源。","source":"Magna International Form 40-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/749098/000119312526128771/d20215dex991.htm","excerpt":"While we supply products and services to a large number of customers worldwide, sales to our six largest customers represented the following proportions of our consolidated sales in 2025 and 2024","as_of":"2026-03-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 40-F：新興 EV 客戶占總銷售低於 5%。","source":"Magna International Form 40-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/749098/000119312526128771/d20215dex991.htm","excerpt":"Sales to these customers represented less than 5% of the Company's total sales.","as_of":"2026-03-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Magna 以 40-F 申報（非 10-K）。FY2025 六大客戶占合併銷售約 76%：GM 15%、Mercedes-Benz 15%、Ford 12%、BMW 12%、Volkswagen 11%、Stellantis 11%（2024 年六大約 73%）。","source":"Magna Form 40-F FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/749098/000119312526128771/d20215dex991.htm","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2026 年 AIF 載明 Magna 供貨所有主要 OEM，但絕大多數銷售集中於六家客戶（GM、Mercedes-Benz、Ford、BMW、Volkswagen、Stellantis），並提示特定電動車型的內容集中風險。","source":"Magna 2026 Annual Information Form (SEC 40-F exhibit)","url":"https://www.sec.gov/Archives/edgar/data/749098/000119312526128771/d20215dex9911.pdf","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"2026 年 S&P 維持 A-、展望調為穩定；Moody's 維持 A3、展望改善為穩定；2026-06-30 評等機構口徑槓桿比 1.42x。搜尋未見降評。","source":"Magna 2026 6-K / earnings materials (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000749098/000110465926089231/tm2618646d2_ex99-3.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"2026 年摘要稱 Q2 上調全年 adjusted EBIT 利潤率、EPS 與自由現金流展望，Q3 再上調自由現金流展望並授權 10% 買回；搜尋未見 2026 年下修或新客戶破產。Fisker 破產相關應收回收仍不明（舊事件）。","source":"Panabee, Magna Q3 2026 earnings summary","url":"https://www.panabee.com/news/magna-earnings-q3-2026","excerpt":null,"as_of":"2026-11-01","retrieved_at":"20261103","affects":["thesis.H","triggers"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"ITR Economics 預測北美輕型車產量 2026 -0.2%、2027 -2.1%、2028 +4.6%，量體至 2028 年大致維持 15.0–15.6M 輛（搜尋摘要轉述，未讀原頁）","source":"HeatTreat: Automotive and Heavy-Duty Truck Forecasts Point to Two Different Paths Through 2028","url":"https://www.heattreat.net/news/automotive-and-heavy-duty-truck-forecasts-point-to-two-different-paths-through-2028","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Magna Q3 2026 更新：因中國預期產量下降與車型組合不利而下修銷售區間；調整後 EBIT margin 指引收窄至 6.3%–6.5%，EPS 中位數不變（搜尋摘要轉述）","source":"Magna Form 6-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120638/tm2628312d2_ex99-2.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"2027 全球輕型車產量預測：GlobalData（2026-08）下調 300k，主因中國；MarkLines 7 月版全球 2027 為 92.64M（2026 為 91.97M）。需求偏平、無緊缺或過剩的結構性證據","source":"MarkLines / GlobalData 經搜尋摘要","url":"https://www.marklines.com/en/report/forecastprod_202607","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Magna 揭露巴西 CADE 針對汽車門鎖供應商的反壟斷正式行政程序（2019 年 5 月啟動），為舊案、狀態待確認","source":"Magna Form 6-K FY2022 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/749098/000110465922052802/tm2212357d1_ex99-2.htm","excerpt":"with an ongoing antitrust investigation relating to suppliers of automotive door latches and related products [\"access mechanisms\"]. In May 2019, CADE informed the Company that it completed its preliminary investigation and, based on a review of the evidence, had commenced a formal administrative proceeding into alleged anticompetitive behaviour relating to access mechanisms involving the","as_of":"2022-05-06","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Q1 2026 電話會議：Magna 毛關稅曝險約 $160M（前為 $200M），約一半為 IEEPA；Q1 未認列 IEEPA 退款；客戶去年吸收約 80% 關稅成本（來自搜尋摘要轉述，原文未逐字取得）","source":"Magna Form 6-K Q1 2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000749098/000110465926054211/tm2612872d2_ex99-3.htm","excerpt":null,"as_of":"2026-05-04","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Q2 2026 電話會議：管理層稱美國提議的 50% 美國含量規則將對整個汽車產業有影響，未說明是否預期生效","source":"Magna Form 6-K Q2 2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000749098/000110465926089231/tm2618646d2_ex99-3.htm","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026-08 加美貿易談判中 Section 232 汽車關稅為主要爭點；美方據報提議降至 15%，加方認為過高","source":"Stockwatch 2026-08-17","url":"https://wwww.stockwatch.com/News/Item/Z-C!MG-3852793/C/MG","excerpt":null,"as_of":"2026-08-17","retrieved_at":"20261103","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Magna Steyr 代工小鵬 G6/G9；Magna 中國區總裁表示準備協助中國車廠進入加拿大市場","source":"Caixin Global 2026-04-14","url":"https://www.caixinglobal.com/2026-04-14/magna-ready-to-help-chinese-ev-makers-expand-into-canada-china-chief-says-102434024.html","excerpt":null,"as_of":"2026-04-14","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Magna 揭露其為 Nexperia 受影響零件的直接買方（中國出口限制阻擋成品出貨），並提及美國鋁板供應商火災（約占車用鋁板產能 40%）可能造成延長停產","source":"Magna 6-K（2025 Q3 相關檔）","url":"https://www.sec.gov/Archives/edgar/data/749098/000110465925104593/tm2526125d1_ex99-2.htm","excerpt":"The inability of affected OEMs to mitigate the disruption by sourcing aluminum sheets from alternative suppliers may cause extended production disruptions to programs on which we have content, which in turn could have an adverse effect on our profitability. · Potential Supply Chain Disruption: Nexperia, a global supplier of electronic components and semiconductor chips, is currently","as_of":"2025-11-06","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Magna 管理層估計年化關稅曝險約 2.5 億美元，主要為加拿大、墨西哥輸入美國工廠的零件，另有少量來自中國與歐洲","source":"Magna 6-K Q1 2025 財測電話會議","url":"https://www.sec.gov/Archives/edgar/data/749098/000110465925073101/tm2519795d2_ex99-3.htm","excerpt":"We continue to work closely with our customers to mitigate the impact of tariffs. Based on our actions taken and recent updates to tariff rates up to mid-July, we have lowered our estimated annualized tariff exposure to $200 million from $250 million when we reported in Q1.","as_of":"2025-05-02","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 銷售約 $10.06B，年減 4%（前年 $10.46B），主因 Lighting 與 Rooftop 出售、客戶價格讓步（net customer price concessions）、外幣走弱，新車型投產部分抵銷；前九個月銷售 $31.4B（+1%）；Adj. EBIT +11% 至 $683M。分部明細未取得。","source":"Magna Q3 2026 results 6-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","moat_trend"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Magna 2026 全年輕型車產量假設：北美 15.0M、歐洲 16.8M（皆未變），中國由 31.2M 下修至 30.4M；銷售展望因中國產量下修與產品組合下調；Adj. EPS 區間 $6.85–$7.15 中點維持，FCF 上調至 $1.85–1.90B，Adj. EBIT margin 收斂至 6.3%–6.5%。","source":"Magna Q3 2026 results 6-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Magna 自述部分產品組合預期長期衰退，包括手排變速箱、機械式全輪驅動系統","source":"Magna 40-F FY2025 exhibit 99.1 (annual information form)","url":"https://www.sec.gov/Archives/edgar/data/749098/000119312526128771/d20215dex991.htm","excerpt":"Some systems in our product portfolio are expected to decline over the long-term, including manual transmissions, mechanical all-wheel drive systems.","as_of":"2026-03-31","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Magna 風險因子提及部分產品技術過時風險升高","source":"Magna Form 6-K risk factors (SEC)","url":"https://www.sec.gov/Archives/edgar/data/749098/000110465926014610/tm2530886d15_ex99-1.htm","excerpt":"heightened risk of technological obsolescence of some of our products","as_of":"2026-02-15","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"區域式電子架構與軟體定義車市場中，Bosch、Continental、Aptiv、ZF 等供應商正投資整合式區域控制器，傳統控制單元供應商單車含量下降（產業層級，非特指 Magna）","source":"Meticulous Research, Automotive Zonal Controller Market (Aug 2026)","url":"https://meticulousresearch.com/product/automotive-zonal-controller-market-6842","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026年4月宣布出售照明與車頂系統業務，歐洲照明業務6月底已完成出售，其餘預計2026下半年交割（投資組合收斂，非通路轉變）","source":"just-auto: Magna to sell lighting, rooftop businesses","url":"https://www.just-auto.com/news/magna-sell-lighting-rooftop-businesses/","excerpt":null,"as_of":"2026-04-14","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 2026 法說：管理層表示正評估機器人、自動化與資料中心等車用以外機會（細節未見）","source":"Magna Q2 2026 earnings coverage (panabee / quartr)","url":"https://www.panabee.com/news/magna-earnings-q2-2026","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q2 2026 6-K：歐洲OEM獲獎，定位為跨車款架構的基礎平台級方案","source":"SEC 6-K ex99-3","url":"https://www.sec.gov/Archives/edgar/data/0000749098/000110465926089231/tm2618646d2_ex99-3.htm","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-31 Q2 後 Magna 將 2026 調整後 EPS 指引由 $6.25-7.25 上調至 $6.70-7.30（共識約 6.82）；營收指引 $41.3-42.5B（共識 $42.4B，MarketBeat 稱較前區間下修）；調整後 EBIT 利潤率 6.3%-6.6%（前 6%-6.6%）。","source":"MarketBeat: Magna International issues FY 2026 earnings guidance (2026-07-31)","url":"https://www.marketbeat.com/instant-alerts/magna-international-nysemga-issues-fy-2026-earnings-guidance-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 引述 FCF 指引上調至 $1.75-1.85B；各來源對營收指引前一區間說法不一（$41.5-43.1B vs $41.9-43.5B），方向未能釐清。","source":"Benzinga MGA earnings forecasts / search summary","url":"https://www.benzinga.com/quote/MGA/earnings-forecasts","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價共識分布：Tickflow（as of 2026-08-01）17 位分析師均值 $67.30、Hold；Walnut（2026-07）均值 $70.28、中位數 $72、區間 $52-80；Google Finance 均值 $67.60、區間 $55-76；Benzinga $61.59；各聚合站不一致。","source":"Tickflow / Walnut Invest / Google Finance / Benzinga","url":"https://www.tickflow.io/stock/MGA/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"個別券商：TD 2026-05-04 目標價 $76（自 $75）維持 Buy；RBC 2026-07-13 目標價 $66；Citi 2026-06 升至 $75（自 $58）；Goldman 2026-04 降至 $52（自 $60）；Scotiabank 7-24 將 FY2026 EPS 預估降至 $6.63（自 $6.83）、目標價 $74。","source":"Yahoo Finance TD Securities; MarketBeat Scotiabank (2026-07-24); Walnut Invest","url":"https://www.marketbeat.com/instant-alerts/scotiabank-has-pessimistic-outlook-of-mga-fy2026-earnings-2026-07-24/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Chartmill 顯示 FY2026 共識 EPS 7.26（20 位分析師，2026-10-24），高於指引區間上緣 7.30 附近；下一季營收預估 3 個月內下修 5.02%。與 MarketBeat 6.86 因日期不同無法對齊。","source":"Chartmill MGA estimates","url":"https://www.chartmill.com/stock/quote/MGA/estimates","excerpt":null,"as_of":"2026-10-24","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"經查 SEC EDGAR 8-K 清單，近 12 個月無 8-K，亦無含重大項目申報。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000749098&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 0 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Magna 簽署協議出售 Lighting（兩筆交易）與 Rooftop Systems 業務，三筆預計 2026 下半年完成；Q1 2026 認列待售資產損失 485（搜尋摘要轉述，未讀頁面原文）。","source":"Magna 6-K FY2026（SEC）／qz.com 報導","url":"https://www.sec.gov/Archives/edgar/data/0000749098/000110465926054211/tm2612872d2_ex99-1.htm","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"Magna Electronics 於 2025-09-03 向 NHTSA 申報召回 25E054（後視鏡頭可能顯示空白或倒置，涉 Ford、Chrysler 車款，聚合站稱約 250,292 輛）。","source":"NHTSA Campaign 25E054","url":"https://static.nhtsa.gov/odi/rcl/2025/RCAK-25E054-9753.pdf","excerpt":null,"as_of":"2025-09-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"MEMA/Deloitte Q2 2026：供應商收緊資本承諾核准標準；2026 新專案 capex 預計約 +5.2%，既有專案 capex 大致持平（搜尋摘要轉述）","source":"Deloitte Q2 2026 MEMA Barometer Commentary","url":"https://www.mema.org/system/files/Deloitte_Q2%202026_MEMA%20Barometer_Commentary_FINAL.pdf","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Magna 2026 資本支出指引下修至約 $15 億（原 $15–16 億）；Q2 2026 capex $2.69 億、占營收 2.4%；銷售展望下修至 $412–420 億，主因中國產量下降（搜尋摘要轉述）","source":"Magna 6-K / MarketBeat Q2 call highlights","url":"https://www.marketbeat.com/instant-alerts/magna-international-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"2026 年個別供應商仍有北美擴廠公告：Newman Technology 俄亥俄 $7,400 萬（2026-03）、DAS North America 蒙哥馬利 $7,760 萬（2026-02）、Auto Parts Manufacturing Mississippi $5,300 萬（2026-07）；均為小型、非 Magna 直接同業產能數據","source":"PlasticsToday / PlasticsNews / industrialinfo 搜尋結果","url":"https://www.plasticstoday.com/automotive-mobility/toyota-supplier-expands-mississippi-plastics-operations","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Zacks 2026年6月產業展望：汽車零件供應鏈庫存已見底，需數月才能補足，回補緩慢且不均（偏售後零售/供應鏈整體，非 Magna 專屬）","source":"Zacks Industry Outlook O'Reilly and Advance Auto Parts (Chartmill)","url":"https://www.chartmill.com/news/external/55863/zacks-industry-outlook-o-reilly-and-advance-auto-parts","excerpt":"Depleted inventories across the auto parts supply chain will take months to fully replenish.","as_of":"2026-06-15","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Magna 存貨 2026-09-30 為 $4,161M（2025 年底 $4,126M；6/30 $4,009M；3/31 $3,964M）；成品 $639M vs $661M","source":"Magna Form 6-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-2.htm","excerpt":"Raw materials and supplies $ 1,668 $ 1,647 Work-in-process 479 484 Finished goods 639 661 Tooling and engineering 1,375 1,334 $ 4,161 $ 4,126","as_of":"2026-10-31","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"美國 CPI 汽車零件與設備指數 2026-01 為 186.920，低於 2025-12 的 187.835","source":"FRED CUUR0000SETC","url":"https://fred.stlouisfed.org/series/CUUR0000SETC","excerpt":null,"as_of":"2026-02-15","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Magna 2022 Adjusted EBIT Margin expected ~4.3% per Jan 2023 update, below the 4.8%-5.0% range in Nov 2022 outlook (lower sales contribution, higher warranty, receivable provisions, higher engineering expense).","source":"TipRanks: Magna updates 2022 outlook to reflect preliminary full year 2022 results","url":"https://www.tipranks.com/news/press-releases/magna-updates-2022-outlook-to-reflect-preliminary-full-year-2022-results","excerpt":null,"as_of":"2023-01-19","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Magna Q4 2008 loss of $148M and grim 2009 forecast","source":"Manufacturing.net: Magna's 2009 Forecast Grim After $148M Q4 Loss","url":"https://www.manufacturing.net/supply-chain/news/13068266/magnas-2009-forecast-grim-after-148m-q4-loss","excerpt":null,"as_of":"2009-02-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Magna Q4 and full-year 2009 results (trough-cycle financials)","source":"Newswire.ca: Magna announces fourth quarter and 2009 results","url":"https://newswire.ca/news-releases/magna-announces-fourth-quarter-and-2009-results-539350001.html","excerpt":null,"as_of":"2010-03-01","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"US light vehicle sales peak-to-trough declines since 1950 (35%, 23%, 31%, 20%)","source":"Gabelli 2003 presentation: A New Kind of Industry Cycle","url":"https://media.corporate-ir.net/media_files/NYS/AN/presentations/gabelli_052003/tsld006.htm","excerpt":null,"as_of":"2003-05-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Magna 簽署協議出售 Lighting（兩筆）與 Rooftop Systems 業務，預計 2026 下半年完成；搜尋未見新收購。","source":"Magna 6-K FY2026（SEC）","url":"https://www.sec.gov/Archives/edgar/data/0000749098/000110465926054211/tm2612872d2_ex99-1.htm","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["valuation","moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"Magna Electronics 於 2025-09-03 向 NHTSA 申報召回 25E054（後視鏡頭畫面空白或倒置，聚合站稱約 250,292 輛）。","source":"NHTSA Campaign 25E054","url":"https://static.nhtsa.gov/odi/rcl/2025/RCAK-25E054-9753.pdf","excerpt":null,"as_of":"2025-09-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"MGA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":14.71,"operating_margin_pct":5.48,"fcf_margin_pct":7.52,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"LEA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":6.86,"operating_margin_pct":3.67,"fcf_margin_pct":3.58,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"APTV","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.63,"operating_margin_pct":9.75,"fcf_margin_pct":3.65,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APTV","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"6902.T","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.2,"operating_margin_pct":6.88,"fcf_margin_pct":1.95,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6902.T","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"BWA","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.8,"operating_margin_pct":10.2,"fcf_margin_pct":9.16,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWA","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"MGA"},"financial_history":{"ticker":"MGA","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":37840000000.0,"revenue_yoy_pct":null,"gross_margin_pct":12.29,"operating_margin_pct":4.16,"net_income":592000000.0,"diluted_eps":2.03,"free_cash_flow":414000000.0,"fcf_margin_pct":1.09,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":42797000000.0,"revenue_yoy_pct":13.1,"gross_margin_pct":13.11,"operating_margin_pct":4.76,"net_income":1213000000.0,"diluted_eps":4.23,"free_cash_flow":601000000.0,"fcf_margin_pct":1.4,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":42836000000.0,"revenue_yoy_pct":0.09,"gross_margin_pct":13.54,"operating_margin_pct":4.94,"net_income":1009000000.0,"diluted_eps":3.52,"free_cash_flow":1456000000.0,"fcf_margin_pct":3.4,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":42010000000.0,"revenue_yoy_pct":-1.93,"gross_margin_pct":14.26,"operating_margin_pct":5.02,"net_income":829000000.0,"diluted_eps":2.93,"free_cash_flow":2285000000.0,"fcf_margin_pct":5.44,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MGA/MGA_Q3_2026_Earnings_Call_20261030.md）

# Q3 2026 Earnings Call
**Magna International Inc.** | Earnings Calls | 2026-10-30

**Operator** (Operator):
Hello, everyone. Thank you for joining us, and welcome to Magna International Third Quarter Fiscal Year 2026 Financial Results Conference Call. [Operator Instructions] I will now hand the conference over to Louis Tonelli, Vice President of Investor Relations. Please go ahead.

**Louis Tonelli** (Executives):
Thanks, operator. Hello, everyone, and welcome to our conference call covering our Q3 2026 results. Joining me today are Swamy Kotagiri and Phil Fracassa. Yesterday, our Board of Directors met and approved our financial results for the third quarter of 2026 and our updated outlook. We issued a press release this morning outlining both of these. You'll find today's press release, conference call webcast, the slide presentation to go along with the call and our updated quarterly financial review all in the Investor Relations section of our website at magna.com. 
Before we get started, just as a reminder, the discussion today may contain forward-looking information or forward-looking statements within the meaning of applicable securities legislation. Such statements involve certain risks, assumptions and uncertainties, which may cause the company's actual or future results and performance to be materially different from those expressed or implied in these statements. Please refer to today's press release for a complete description of our safe harbor disclaimer. Please also refer to the reminder slide included in our presentation that relates to our commentary today. With that, I'll pass it over to Swamy.

**Seetarama Kotagiri** (Executives):
Thank you, Louis. Good morning, everyone, and thank you for joining us today. We appreciate your time and interest. Let's get started. I am pleased with our performance this quarter. We delivered another strong quarter with continued margin expansion, reflecting disciplined execution and progress across a number of areas. In the quarter, sales were down 4%, reflecting lower light vehicle production and our previously announced dispositions. However, weighted organic growth over market was positive. Adjusted EBIT was up 11%, while adjusted EBIT margin expanded 90 basis points to 6.8% and adjusted EPS rose 38% to $1.83. These results reflect continued progress in our operational excellence initiatives and success in resolving commercial items, including some pull forward from Q4. Most notably, we continue to see improvement in the underlying operating performance of the business. Our strong free cash flow is further evidence of the continued improvement in our operating performance and the cash-generating capability of the business. 
During the quarter, we generated $950 million in operating cash flow and $584 million in free cash flow. And we ended the quarter with leverage well within our targeted range and $1.4 billion in cash on hand, which provides continued financial flexibility. Supported by our strong year-to-date performance, we updated our full year 2026 outlook. We lowered our sales expectations to reflect reduced vehicle production in China and unfavorable program mix and narrowed our range for adjusted EBIT margin. However, we maintained the midpoint of our outlook range for adjusted EPS. In addition, we raised our outlook range for free cash flow, again, reflecting our year-to-date momentum and confidence in our cash flow trajectory. Together, these updates demonstrate our ability to absorb lower production and still deliver improved profitability and cash generation. We remain steadfast in executing our proven capital allocation framework. We continue to invest in our business to support further profitable organic growth while returning significant capital to shareholders. 
During the quarter, we returned $658 million to shareholders, including $529 million through share repurchases. We completed our existing buyback authorization in October, repurchasing the remaining 1.3 million shares, and our Board approved a new NCIB for 25.8 million shares. And lastly, we closed on the sales of our rooftop and North American lighting businesses in Q3 and expect to complete the remaining divestitures in the fourth quarter. 
I would like to take a moment to highlight our Complete Vehicle segment, which is ramping up business globally and demonstrating the value of our flexible vehicle manufacturing model. In Mesa, Arizona, we are launching and ramping up two new vehicle programs for Waymo in our existing upfitting facility. In Graz, Austria, we assembled six vehicles in total for XPENG and GAC. We are launching the G9L, our fourth model in Graz, supporting XPENG's European localization strategy. We also produced two GAC models, including the AION UT launched earlier this year. And in China, our joint venture is ramping up production of all-new Alpha T7, the fifth ARCFOX model produced by the joint venture. These programs demonstrate our ability to support new and established customers across regions through flexible state-of-the-art manufacturing. They are also generating discussions with additional customers and creating opportunities to bring more Magna systems content to new vehicle programs. 
We also continue to win new business across our core product areas. We were awarded a transfer case, rear-drive module and front drive unit for a North American-based global OEM. This new program, which launches in 2028, adds to our leading market position in 4-wheel drive. We were also awarded incremental actuator content for a SmartLatch system we currently supply to a North American-based global OEM. The global program launches in 2027, spans our three key markets and supports new global regulation requirements. The wins reinforce Magna's strong technology position in leading product areas. 
Lastly, our commitment to innovation continues to be recognized by the industry. Three of our technologies are finalists for Automotive News PACE Awards and two are finalists for PACEpilot Awards. Winners will be announced in November. These finalists span a number of our capabilities, demonstrating our strong position across our portfolio. With that, I'll turn the call over to Phil.

**Philip Fracassa** (Executives):
Thanks, Swamy, and good morning, everyone. I'm going to begin on Slide 15 with a summary of our strong third quarter results. Sales were $10.1 billion in the quarter, down approximately 4% from last year. Adjusted EBIT margin improved 90 basis points to 6.8%. Adjusted earnings increased 38% to $1.83 per share, and free cash flow was strong at $584 million. Each of these metrics exceeded our expectations and continues the momentum we saw in the first 6 months of the year. Now I'll take you through some of the details. Let's start with sales on Slide 16. As I mentioned, third quarter sales were down about 4% overall compared to last year. Excluding divestitures and foreign currency translation, sales declined 2.1% organically. By comparison, global light vehicle production declined about 3% in the quarter. On a Magna-weighted basis, we estimate light vehicle production was down 2.6%. This translates to positive growth over market for Magna of about 0.5% on a consolidated basis and 1% excluding Complete Vehicles. 
Looking at the sales walk, volumes, launches and other reduced sales by $150 million. The decrease mainly reflects lower light vehicle production, the end of production on certain programs, including the Ford Escape and normal course customer price concessions. These factors were offset partially by new program launches, including the Jeep Cherokee and the Mercedes-Benz GLB and GLC. Complete vehicle sales declined $74 million organically despite higher unit volumes. The higher volumes were driven by new programs, XPENG and GAC in Graz, where sales are recognized on a value-added basis. Volumes with other customers, where sales are generally recognized on a full cost basis declined year-over-year, including end of production for the BMW Z4 and Toyota Supra. This mix shift resulted in net lower assembly sales dollars but at higher margins. Engineering revenue was also lower, in line with our expectations. The rooftop systems and completed lighting divestitures reduced sales by $165 million in the quarter. And lastly, foreign currency translation reduced sales by $14 million, reflecting a net stronger U.S. dollar. 
Now let's move to EBIT on Slide 17. Third quarter adjusted EBIT was $683 million, an increase of $70 million or 11% versus last year. Adjusted EBIT margin was 6.8%, an improvement of 90 basis points. Operational volumes and other contributed about 120 basis points to margin in the quarter. The improvement mainly reflects net favorable commercial items and the impact of operational excellence initiatives, net of normal course customer price concessions. We also benefited from prior restructuring actions as well as the divestitures, which were running at margins below then the average. These factors were offset partially by lower earnings on reduced organic sales volumes, unfavorable net foreign exchange impacts and higher profit sharing and incentive compensation. In addition, lower net tariff costs contributed approximately 30 basis points to margins. Costs were slightly lower, and we're getting recoveries faster than we did last year. 
While the tariff situation continues to evolve, we currently expect that our full year net tariff headwind will be similar to what we experienced last year. Higher commodity costs reduced margins by about 50 basis points. As we have noted in prior quarters, we continue to experience inflation across several key commodities. While this was a headwind in the quarter, we do expect to substantially mitigate or recover these increased costs over time. And lower equity income reduced margins by around 10 basis points. This mainly reflects the impact of lower sales, unfavorable product mix and higher income tax expense at certain affiliates accounted for under the equity method. 
Looking below the EBIT line on Slide 18. Interest expense was $30 million lower than last year. The improvement was driven by some discrete interest expense last year that did not recur as well as reduced seasonal short-term borrowings, supported by our strong cash flow. Our third quarter adjusted tax rate was 22.4%, an improvement of 410 basis points versus last year and better than our expectations. For the full year, we now expect an adjusted tax rate of approximately 22% -- and third quarter adjusted EPS increased 38% to $1.83, reflecting the higher net income and a 6% reduction in diluted shares outstanding from share repurchases completed over the past 12 months. 
Next, let's take a brief look at our business segment performance, which is summarized on Slide 19. We were impacted by lower global light vehicle production across the business. In Power & Vision, reported sales also reflect the rooftop and completed lighting divestitures. Excluding divestitures and foreign currency translation, P&V sales increased approximately 2% organically in the quarter. In Seating, sales were negatively impacted by a major changeover at Ford's Louisville plant as well as retooling at BMW's Spartanburg plant for upcoming planned program launches. And in Complete Vehicles, sales declined 8% as expected despite higher unit volumes as lower sales on full cost programs and lower engineering revenue were only partially offset by new value-added programs at higher margins with Chinese OEMs in Graz. 
Turning to EBIT. Body Exteriors & Structures, Power & Vision and Complete Vehicles all posted notable year-over-year improvements in adjusted EBIT dollars and margins, reflecting strong operational execution. P&V also benefited on the margin line from the divestitures and Complete Vehicles benefited from favorable mix. And in Seating, margins were down as expected, mainly reflecting the decline in sales for the program changeovers I mentioned earlier. 
Now let's look at cash flow on Slide 20. In the third quarter, we generated $950 million in cash from operations, an increase of $38 million from last year, driven by higher earnings and improved working capital. Investment activities in the quarter included $307 million in CapEx and $75 million for investments, other assets and intangibles, offset partially by proceeds from normal course asset disposals. Netting everything out, we generated free cash flow of $584 million in the quarter, which was slightly above last year and ahead of our expectations. 
We continue to return cash to shareholders in the third quarter with $129 million in dividends, along with $529 million through share repurchases. During the quarter, we repurchased 7.9 million shares under our current NCIB buyback authorization, which left us with just over 1 million shares remaining at the end of September. As of today, we will have repurchased all remaining shares. That's a total of over 25 million shares over the past 12 months. And as Swamy mentioned, yesterday, our Board approved a new NCIB buyback authorization, which is expected to take effect in November. 
Turning to Slide 21. Our balance sheet and capital structure remains strong. At the end of September, we had close to $5 billion in total liquidity, including $1.4 billion of cash on hand. This is despite the significant return of capital during the first 9 months of the year. Looking at leverage. Our net debt to adjusted EBITDA was under 1x and our rating agency leverage was 1.4x at quarter end. These are both within our targeted ranges, which provides significant financial flexibility and puts Magna in a great position to continue investing in the business and returning capital to shareholders. Next, let me cover the macro assumptions underpinning our current outlook on Slide 22. Compared to our July outlook, we've reduced our China production estimate by 800,000 units. We also updated our foreign currency assumptions to reflect recent exchange rates. Our full year outlook now assumes a slightly stronger Canadian dollar, euro and Chinese yuan relative to the U.S. dollar. 
Moving to Slide 23. We are revising our full year sales outlook, primarily to reflect our assumption for lower vehicle production in China and unfavorable program mix compared to our previous outlook. Despite the lower sales outlook, we continue to expect strong year-over-year margin expansion. We are narrowing our outlook for adjusted EBIT margin to a range of between 6.3% and 6.5%. Our midpoint of 6.4% represents an improvement of 80 basis points from last year on slightly lower sales at the midpoint. We are also narrowing our adjusted EPS outlook to a range of between $6.85 and $7.15 per share. The midpoint, which is unchanged at $7 per share, represents an increase of 22% versus last year. And finally, we are raising our free cash flow outlook to between $1.85 billion and $1.9 billion, an increase of $75 million at the midpoint, mainly reflecting lower planned capital spending. The updated outlook represents free cash conversion of approximately 100% of adjusted net income. 
With respect to other key assumptions, we expect CapEx to be approximately $1.5 billion compared to our previous range of $1.5 billion to $1.6. We're planning for slightly lower interest expense, and we expect a lower adjusted tax rate of approximately 22% compared to 23% previously, reflecting a more favorable mix of earnings. And finally, our assumptions for equity income at the midpoint and diluted shares remain unchanged. That's it for the financial review. And now I'll turn it back to Swamy to wrap things up. Swamy?

**Seetarama Kotagiri** (Executives):
Thank you, Phil. Before we take your questions, let me summarize. We delivered a strong third quarter with meaningful growth in adjusted EBIT margin and adjusted EPS. Just as importantly, we generated strong free cash flow, reinforcing the quality and sustainability of our earnings. These results reflect the continued progress we are making through disciplined execution and operational excellence across the company. Looking ahead, our updated 2026 outlook reflects our confidence in Magna's ongoing operating performance. We remain focused on sustaining our momentum in margin expansion, earnings growth and free cash flow while continuing to execute our disciplined capital allocation strategy. 
We completed our previous share repurchase program, and the Board has approved a new authorization. This positions us to continue returning significant capital to shareholders while investing in the business. Overall, we believe Magna is well positioned to deliver continued margin expansion, EPS growth and attractive shareholder returns. We hope to see many of you in November at our investor event in New York City, where we will go into detail on our strategy, key initiatives and long-term financial outlook. Thanks for your attention. Now operator, let's open it up for questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of James Picariello from BNP Paribas. James, we will return momentarily. Your next question comes from the line of Dan Levy from Barclays.

**Dan Levy** (Analysts):
First, just wondering if you could unpack maybe some of the items within the quarter. You said there was timing of commercial recoveries. Maybe you could just outline a bit more the magnitude of those? And maybe just give us a little more sense if those were for commodities, if those are for vehicle programs? And then what's onetime versus maybe the right sort of on a run rate basis going forward, the right way to think of it?

**Seetarama Kotagiri** (Executives):
Yes. Dan, maybe I'll start off with the high level and Phil can jump in with some of the details. The commercial and tariff recoveries benefited Q3 and some favorable commercial items moved forward from Q4. But I would say that's not the full explanation of the full improvement. We delivered meaningful productivity and efficiency gains, operational excellence benefits and restructuring benefits, which helped absorb significant commodity pressures. So if I had to summarize it, I would say timing helped the quarter, but the underlying operating performance is what held the improvement and will serve as a trajectory going forward.

**Philip Fracassa** (Executives):
Yes. The only thing I would add there, Dan, is you're right, the operational volume and other bucket, if you will, added 120 basis points overall to margins. The 2 biggest positives would have been commercial and operational excellence. Swamy talked about the operational excellence. As we've said many times, we're still in the early innings there and expect that momentum to continue. On commercial, I would say it was in that particular bucket, it was probably a combination of volume-related commercial and some commodity-related commercial, although commodities was a net headwind in the quarter. We actually show that in the different buckets. 
It was mainly commercial related or volume-related commercial, some pull ahead from Q4. The only thing I would say is we still expect margins in Q4 despite the pull ahead into Q3, still expect margins in Q4 to step up from Q3 despite lower volume, despite commodity costs, despite actually commercial probably flipping negative on us in Q4. So we do believe the margin performance when you peel it all back, is sustainable. And as we've said before, we think the midpoint of the full year guide, when you look at 6.4% at the midpoint, we do believe that is a structural jumping off point as we head into 2027.

**Dan Levy** (Analysts):
And just to clarify, within that, the commodity cost that you said was a net headwind. The view, I assume over time is that you should get full recoveries to make it EBIT dollar neutral. And so it's just a matter of the timing. Is that correct?

**Philip Fracassa** (Executives):
Yes, that is correct. We signaled it probably last quarter was modest impact in Q2. It stepped up in Q3 to the 50 basis points that you see. We're expecting probably a comparable headwind, maybe even a little bit higher in Q4. And it is a timing issue. It really is across think of DRAM and related electronic components, you can think of resins and some aluminum that we buy in from Tier 2s and the like that's embedded in components, if you will. And that is where we -- it does take some time to get recoveries from customers. I would tell you, we've gotten some. The 50 bps you see is, sort of, the net headwind for the quarter. Conversations, I would say, are constructive. But what we don't recover this year, the plan would be to substantially mitigate or recover in 2027.

**Dan Levy** (Analysts):
Great. As a follow-up, one of the automakers mentioned on their call that for one of their new vehicles, they want to bring castings in-house. And we've heard this from others as well, this idea to do, sort of, gigacasting. So BES, obviously, you've got some big customer relationships there, and it's pretty chunky content. Maybe you could just talk about the trend by some of the automakers to bring some of the casting in-house and whether that's at all a risk to you?

**Seetarama Kotagiri** (Executives):
The simple answer, Dan, no. The reason I say that is as we continue to have conversations with various customers actually in all regions of the world, North America, Europe and China, if anything, we are continuing to see more interest in our capability and bringing forward some inventive or innovative ideas on doing castings on a pretty large scale, right, in the 6,000, 7,000 ton type machines. And some of the technologies we are bringing, which we got PACE Awards last time in terms of the alloy development in terms of joining technologies and so on. And we are able to show some solutions there where 2 or 3 castings, which bring together significant consolidation of parts, but at the same time, take into account repairability and maintenance and so on and so forth. So all in all, a lot of interest. We are not seeing any negative influence. We are actually pretty enthusiastic about that process and product.

**Operator** (Operator):
Your next question comes from the line of James Picariello from BNP Paribas.

**James Picariello** (Analysts):
Can you hear me? All right. Second time's a charm. Sorry about that. So I know we're going to get all the detail we want in just two weeks at the Investor Day. But as we think about free cash flow and consider the strength in Magna's free cash flow and buybacks commitment, can you confirm the amount of EV recoveries in the outlook in the free cash flow outlook for this year? And just high level, how you're thinking about the puts and takes for the trajectory into next year?

**Philip Fracassa** (Executives):
Yes, sure, James. I would -- we talked in the first quarter that we had a large EV recovery from a North American OEM, and we had talked at that time that it was north of $450 million. We got probably a little bit more in Q3. So, as we're sitting here today, I'd probably round the number to about $500 million in the year. And again, some of the -- and that would have been sort of cash received. We do have some go-forward impacts as well. But as we look at the free cash flow, it's been very strong on strong earnings, very good working capital management. And then obviously, CapEx coming in at the full year guide around kind of 3.6-ish percent of sales. So feel really good about the free cash flow, not only in 2026. 
I'll talk about go forward in a moment, but balance sheet is in great shape. So we ended the quarter with great liquidity. The balance sheet is in really good shape. We renewed the NCIB. So we feel really good about the cash generation of the business and the ability to continue returning significant capital to shareholders moving forward. And as you step forward to 2027, obviously, those recoveries won't repeat, but the combination of stronger earnings, again, continued focus on working capital and CapEx. We do believe the free cash flow of the business will remain strong, and we'll continue to be supportive of everything we want to do.

**James Picariello** (Analysts):
Got it. That's great to hear. And then on Power & Vision, the growth over market was a clear positive again this quarter with the full year guide implying another strong showing for the fourth. Can you speak to any key factors driving this improvement, either from a product or favorable customer mix perspective? Or is the growth mainly driven by new business backlog contribution? Just any color on the Power & Vision growth inflection would be helpful.

**Seetarama Kotagiri** (Executives):
James, I think you summarized the Power & Vision, as you saw, declined 2% in the sales side of things, including the divestiture effects. And the margin improved about 150 basis points and standing at 6.6%. The improvement in this case or in this segment definitely was less about commercial recoveries and more about strong operational execution. I would say it's continued traction from our operational excellence initiatives, and it's truly becoming foundational, and we are starting to see that. It's definitely a trajectory going forward. And I don't think there is any one particular product that stands out. Definitely, the launches of some of the programs that we've been working being a normal cadence and normal run rates definitely helps. And the discipline in engineering and launches is the other part. So all in all, I would sum it up as the different headings under the operational excellence is what's giving us the jump in the profitability.

**James Picariello** (Analysts):
Yes. No, it's great to see that low to mid-single-digit core growth.

**Operator** (Operator):
Your next question comes from the line of Tamy Chen from BMO Capital Markets.

**Tamy Chen** (Analysts):
First, I just want to start on the Seating side. Can you remind us again in North America, I think there's the fairly sizable replacement or refresh program that will come. When do you launch that? And when we think about overall Seating margins as we go towards that launch, like is this refresh or renewed program meaningful enough to potentially move those segment margins back to pre-pandemic? Is that how we could think about it?

**Seetarama Kotagiri** (Executives):
Yes, I think a couple of things, right? The program changeovers at Ford Louisville and BMW Spartanburg are the ones that are having impact. As they come back into -- come back online, you'll see the Seating come back to what I would call the normal cadence if you look at it from last year to how we've been progressing, we are satisfied and seeing what we expected there other than the program changeovers. And the October full year margin outlook is 3.1% to 3.3%, right? So if you take the midpoint, 3.2%, that's in line with what we've been talking about. And with the program launches coming in play and the one big program that you mentioned will be fully launched by this time next year. It started now and it's phasing, right? And we feel pretty confident in how the launch is going, how the economics are working out. And when all of this comes back, I would say I kind of go back to what I always said about Seating good returns business. We are seeing the trajectory we wanted. So this quarter seems a little bit off, but that's because of the changeovers. All in all, it's following the trajectory we had in plan.

**Philip Fracassa** (Executives):
Yes, Tamy, the only thing I would add is that we'll still feel more of the impact of the BMW because that's sort of launching kind of as we speak, but we'll feel it more in '27, whereas Ford Lou will be sort of mid next year. So that will be kind of a midyear ramp, if you will. But as Swamy said, the margins this quarter, while they were down year-over-year, were actually better than we anticipated coming into the quarter because obviously, that's a lot of volume to lose, albeit it's temporary, if you will. But the team did a great job on operational excellence and some commercial items to kind of protect margins. And moving forward, as Swamy said, with the new economics and the volumes coming back, we feel really good about the ability of Seating margins to get back where they were.

**Tamy Chen** (Analysts):
Okay. Good to hear. Got it. And my follow-up question is a bigger picture. I assume you'll talk more about it at the Investor Day as well. But curious if you can give any insights right now. Your overall operational excellence journey, if you had to describe what inning do you think we're at? What's still to come? I think one of the areas is your Factory of the Future, just continuing to roll out in more facilities. So if you can give any sort of numbers to help us assess how far along and how much more there is to come from there?

**Seetarama Kotagiri** (Executives):
At the Investor Day, you'll definitely hear from us about a little bit more detail on how our strategy is evolving. We'll talk about our growth over market priorities and definitely more color on the operational excellence initiatives. I won't put a number on it, but I would still say it's early innings. We are enthused about -- and you've seen the traction of what -- shout out to the Magna team, everybody on the shop floor, they're sticking to it, doing it. So with all gratitude towards them, we still feel pretty good about how we are doing. And then we'll also obviously touch on the medium- to long-term financial framework when we come to the Investor Day.

**Operator** (Operator):
Your next question comes from the line of Alex Perry from Bank of America.

**Alexander Perry** (Analysts):
I guess, first, I just wanted to ask a little bit more about the change in the guide for this year, specifically on China. Is there any visibility on China improving? How conservative would you say the outlook is at this point with the volatility and visibility you have in that region? And then maybe just walk us through how China sort of varies versus the other regions in terms of the visibility profile given some of the fragmentation there in the market?

**Seetarama Kotagiri** (Executives):
Alex, as you said, China is pretty dynamic in terms of local consumption versus exports, the dynamics between the Chinese OEMs and the Western OEMs and so on. From our perspective, China vehicle production declined 7% in Q3, and our impact was roughly about 10%. And if you peel that back a little bit, you'll see that the three German OEM group collectively declined approximately 28% in the quarter. 
So contextually, Magna, when we started, we had a much bigger share with the Western OEMs. But over the last decade, I would say we have grown at 10-plus percent CAGR in China. And today, we are about 65% business or revenue is with the Chinese OEMs in China. So we have evolved pretty well. We continue to grow in the long term pretty good. It's an important market for us. And from a financial metrics, I would say we are satisfied and continue to be good and accretive -- it's a little bit lumpy is how I would characterize it, but our focus remains on the right customers, platforms, products and definitely returns.

**Alexander Perry** (Analysts):
Really helpful. And then I wanted to ask a little bit about what you're doing with some of the AV players. So maybe help us think about in contextualizing the size of the Waymo business, what you're doing there. Could that become significant over time? And then are you targeting other robotaxi AV players that are trying to integrate a lot of pieces in the various tech stacks?

**Seetarama Kotagiri** (Executives):
Yes. I think generally, AV is -- first of all, I think from a component systems perspective, we have been pretty clear that our focus really is on, call it, the driver assist systems, right? And if there is alignment in terms of our product strategy where we can support the AV players in sensors and systems and so on, absolutely, yes, and we continue to explore that opportunity. Specifically with Waymo, it's our complete vehicle group that has brought value in terms of the upfitting for Waymo. And as we talked about, we are adding more models there. That model will continue to be explored in other areas, but -- or with other customers in the other regions. But again, it's going to be something long term, something that's more partnership and value driven. But we continue to look at it, but we are very highly disciplined and cautious in how we go about it.

**Operator** (Operator):
Your next question comes from the line of Tom Narayan from RBC Capital Markets.

**Gautam Narayan** (Analysts):
The first one is on European capacity. It looks like you took a charge in P&V $76 million in Q3. Just curious what was behind that? We know Jim Farley on the Ford call was saying that Europe has just too much capacity, and then this is coupled with Chinese exports coming into Europe. So curious if you expect to see more capacity cuts in Europe at P&V in Europe or perhaps in other segments? And then I have a follow-up.

**Seetarama Kotagiri** (Executives):
Tom, I think, like, we've been talking about, call it, consolidation, restructuring, closures, all of it over the last 4 years, and we've done that with 41-plus divisions. A significant portion of that was in Europe. My point being, it's been a continuous journey. So we have been flexing from the times when Europe saw like 21 million, 21.5 million units to the current 17 million-plus units. So we worked along with it. We still are very careful and continue to watch it. I feel pretty comfortable. Again, this is part of the operational excellence, right, being able to react quickly enough, be agile and be resilient. So there is a little bit more work, but nothing that I would call a heavy lift from Magna perspective for Europe.

**Gautam Narayan** (Analysts):
Okay. And then on the buyback plan, I think it is a 10% float through, I think, November next year. Your leverage is quite low. I know we'll hear more on the Investor Day on this, but the implication is potentially that you're maybe leaving some room for M&A and reinvesting in the business, perhaps in some nonautomotive areas. Again, I don't want to steal your thunder here, but is that a fair assumption to make that the buyback plan, which is big, but it is maybe potentially leaving some room for other things, too?

**Seetarama Kotagiri** (Executives):
So I think for us, the capital allocation principles were pretty straightforward. So I think focused really on the organic profitable growth that remains very disciplined in terms of going after programs and how we grow. As I said before, Tom, and I think it still holds, we are pretty happy with the portfolio the way we have it today. I don't really see a significant or transformative M&A. Could we see some small tuck-ins that would help our strategy? Yes. So it would be looking at externalities, the dynamics of their economic conditions and so on and so forth, maintain our financial flexibility and leverage ratios. And the rest, I think, would be share buybacks and dividends as we see it, as we have done in 2026.

**Philip Fracassa** (Executives):
Yes. And Tom, I would only add that I would probably look at it a little bit different. So we had 10% available to buy back this year, and we've bought back the entire 10%. We have been able to take leverage down. We have been working to bring our leverage down within our range. We're slightly below the top end of our targeted range. We don't feel a need to certainly delever from here. And I do think it puts us, if anything, puts us in great position as we look ahead to next year from a capital return standpoint. And as Swamy said, continue to invest in the business and then maybe a tuck-in here or there. But I do feel like the balance sheet capacity we have, we certainly intend to put it to use similar to what we did this year.

**Operator** (Operator):
Your next question comes from the line of Jonathan Goldman from Scotiabank.

**Jonathan Goldman** (Analysts):
Could you just remind us if you've updated your expectations for growth over market this year?

**Philip Fracassa** (Executives):
Yes. Great question, Jonathan. So given the updates to the volumes that we made in this current outlook, in the quarter, we were slightly above 1% growth over market, roughly 1%, excluding Complete Vehicles. Right now, for the full year, we're probably looking at closer to flattish all in and up 1%, excluding Complete Vehicles. So a little bit down from what we would have guided to last quarter, mainly as a result of the updated volume estimates. And then as we peel the onion back in terms of programs that we're on. Swamy talked about the dynamic in China. And then as well as we do -- we did have a customer in North America and a customer in Europe had some planned downtime in the fourth quarter where we do have quite a bit of content with those customers. 
So as we kind of pull it all together, it did bring it down. But if you take a step back, as we've said all along, really the downtime and some of the impacts in China. China is going to move around a little bit. The downtime is really temporary, if you will. We still feel really good about our ability to generate positive growth over market. We've talked about low to mid-single digits in the past. It's not going to be that number every quarter or every year, but really nothing has changed in terms of our long-term view on that.

**Jonathan Goldman** (Analysts):
Okay. That's helpful. And that's a good dovetail to my next question. Maybe by this point of the year, how would you describe the level of visibility on Q4 production? Do you have any early reads on light vehicle production in the environment in '27 based on some of the commentary you're talking about downtime and kind of that coming back and kind of the macro environment you're seeing in your various regions?

**Seetarama Kotagiri** (Executives):
Yes. I think as we go through the planning process that we're going through right now for '27, we consider, call it, the tribal knowledge of the programs that we have, obviously, discussions with the customers and looking at the outside kind of seems to be a little bit softer. We haven't gotten a final answer to that yet. We'll get through the planning process and know it. And that's how we are going into it planning. But we'll get back a little bit more detail, Jonathan, when we come into February, right? Right now, it would be premature to put numbers on it. But I would say our biggest focus is assuming a flattish market and how do we continue the momentum we have in our self-help or operational initiatives. And that's what I think will give us the confidence, right, of moving forward. So more color to come.

**Jonathan Goldman** (Analysts):
That's fair and definitely see the progress on the operational excellence is coming through. And I guess related to that, if I can squeeze one more in on free cash flow. I think it's going to be the second year in a row, you're doing close to $2 billion, maybe $1.875 billion, $1.9 billion. Is there anything that sticks out that's unusual in this year, last year? Or should this be kind of like the go-forward run rate of free cash flow and free cash flow conversion and maybe upside if you're able to squeeze more out on the operational excellence?

**Philip Fracassa** (Executives):
Yes. No, great question, Jonathan. So if you look at last year and this year, free cash flow, we're quite good in both years, over 100% conversion on adjusted net income last year and the midpoint of the guide would imply right around 100% conversion on adjusted net income this year. So really strong performance. We did have some recoveries last year related to some EV investments. We did have some recoveries, as I talked about earlier this year. But moving forward, as we've talked about, with earnings growth, strong working capital management and discipline around CapEx, we do expect the strong free cash flow to continue. It's a little early to talk about 2027. But even with those recoveries not recurring, we do expect to continue to generate strong conversion on net income, strong free cash flow, which should be very supportive of our capital allocation strategy.

**Operator** (Operator):
Your next question comes from the line of Rajat Gupta from JPMorgan.

**Rajat Gupta** (Analysts):
I just -- I wanted to follow up on the AV and robotaxi opportunity. We keep hearing a lot from both Western and Chinese OEMs about in-sourcing a lot of the work, particularly the higher value software layer, et cetera. I'm curious, as your conversations have progressed on the opportunity, what has changed versus what has been intact in terms of where you're playing across that ADAS stack? And are there any opportunities either from an M&A side that can help you enhance your stack in the future? Just curious what's the latest there? I have a quick follow-up.

**Seetarama Kotagiri** (Executives):
I think the way, again, I've said, we kind of look at domain as driver assist systems and call it, full autonomy. As you look into the story of the driver assist and depending on who you talk to, let's say, in generic terms, L3 or L3++ scenario, there's a lot of discussions, as you said, and it depends on the region and also depends on the type of the vehicle, whether you have sensors that have edge compute and that architecture, there are some which are talking about zonal architecture and then there are some which is complete central compute. 
If you sit back and look at it from the ability to provide either edge compute or sensors that support the central or zonal architecture, I would say we are pretty well positioned in being able to support that, not just giving them the pieces of it, but actually the integration of all of these systems put together and be able to provide a feature that our customers want and ultimately, the consumers want, I think we're in a decent place. 
We have to be a little disciplined, like you said, until there is a little bit of a clear path on which way it goes, and it's different by regions and what the chip strategies are. So I think they're a little bit cautious at this point in time. I would be focused on continuing to expand our strength rather than look at any inorganic activity at this point in time. We feel pretty good where we are. We'll stay disciplined and focused and be deliberate on the customers and programs we pick, and we're watching.

**Rajat Gupta** (Analysts):
Understood. That's helpful. And then just wanted to follow up on the commodities headwind. I'm curious versus the prior outlook, how much higher is the margin headwind from commodities? And within that, what parts are just indexed and easily recoverable versus what you might have to offset with more internal initiatives?

**Philip Fracassa** (Executives):
Yes, sure, Rajat. This is Phil. So I would say it definitely got worse since the last outlook. I don't have the exact number, but certainly got incrementally worse both in Q3 and Q4 versus the prior outlook. And obviously, we actually are doing a little bit better on operational excellence, which is helping to mitigate that a little bit. But when you take a step back, you look across key commodities, steel and aluminum were pretty well covered with resale programs with customers or index pass-throughs, if you will. We do have some exposure on aluminum from Tier 2s if it's embedded in components and the like. 
On resins, we've said we have about 40% that's protected through indexes, the rest we would have to negotiate commercially with the customer to get recoveries for. And then the bigger thing that really is continuing to escalate, probably the biggest driver behind what we saw in the second half has been the DRAM and the related electronic components, whether it's the boards and the like. We're seeing increases there as well. And on most of that, the vast majority of that is where we have to negotiate with our customers for recoveries. And as I said, that's ongoing. We've actually secured some already. The conversations have been real constructive. But the headwind we saw in Q3, we'd expect another headwind, I would say, of, call it, similar size in Q4 and then obviously work to recover or mitigate the impact of those items as we move into next year.

**Operator** (Operator):
Your next question comes from the line of Joe Spak from UBS.

**Joseph Spak** (Analysts):
Maybe, Phil, if we could just sort of recap. I mean, you sort of made the 6.4% sort of jumping off point. And look, we could all make our own volume assumptions. And then you talked about operational excellence, which is still in the early innings, but that -- some of that might get eaten away by the inflation headwinds. I guess the question is really on that operational excellence. I think you were targeting 35% to 40% this year. And Swamy, you still sort of said it's early innings. But isn't -- and correct me if I'm wrong, but isn't some of the like the new contracts rolling on versus the old ones rolling off like part of that operational excellence? And shouldn't we -- are we through most of that? Or is there still more -- just more favorable contracts that still continue to roll on that still support that operational excellence?

**Seetarama Kotagiri** (Executives):
Joe, I'll make a few points. No, it's not just the new economics. When we talk about operational excellence, this is on top of that. And I don't think it's the right way to characterize that whatever we do is being eaten away by inflation. I think some of the inflation is the recoveries and the economics that we talked about. On the other hand, what we talk about operational excellence is the self-help activities, right? So the best way -- at least the way we are looking at it is from last year to this year, about 1.5% less of revenue and about 80 basis points better in margin, right? So -- and that will continue. 
What I said was 35 to 40 basis points is what we said last time. We're, kind of, tracking more towards 50 this year from the margin benefit. And if you ask me, like Philip said, if you take the midpoint of 6.4% on a flattish production environment, I would venture to say it's very likely for us to look at another 35 to 40 basis points going into next year on operational excellence. Now you talked about externalities. That's anybody's guess, right? Production mix, interest rates, yes, that's industry driven. So we are really focused on what can we do that's in our control, and that's what I'm talking about.

**Joseph Spak** (Analysts):
Yes, absolutely. That's helpful. And then, Phil, maybe just one point on the NCIB. I think last year, when you renewed it, there was some commentary about a commitment to sort of fully execute it. Can we assume that again? Or is this a little bit play by ear as to, sort of, how much of that authorization you'll attack this year?

**Philip Fracassa** (Executives):
Yes. No, thanks, Joe. What I would say is you're right. Back in February, we did indicate our intention to exhaust the current NCIB, which we've done. We put the new one in place. It will take effect in a week or two. It's probably a little bit early to talk specifically about it. But as I said earlier, when we think about the strong free cash flow and our expectation for that to continue and the balance sheet being in great shape, I mean, we are in great position to continue to buy back a substantial amount of shares. And I would expect that we will have buybacks certainly in the fourth quarter that we'll be talking about next call, if you will. But in terms of being more specific in that, it's probably a little early and probably, I would say, more to come on that.

**Joseph Spak** (Analysts):
Okay. If I could squeeze one quick one in. Like just your fourth quarter at the midpoint of the range, right, we could all sort of calculate that. But it is still like plus or minus like 9% on either side, which with 2 months left seems a little bit wide. So any color commentary about just sort of how we should expect the year to finish up?

**Philip Fracassa** (Executives):
Yes. I mean, I think you're right, we narrowed the adjusted EBIT margin down to 6.3% to 6.5%, which probably 20 basis points on the full year with one quarter ago is maybe a little bit wide. But again, I think we feel -- I would say, feel very confident in our ability to land in that range. And I would focus -- I would probably focus mainly on the midpoint of that range, plus or minus. And yes, and I think when you think about the headwinds that got layered into the fourth quarter between volumes, between mix, between commodity costs, et cetera, I think we feel really confident in the full year guide. The midpoint would imply roughly 7.3% margins in Q4, which is a step-up from Q3 despite incremental headwinds and then down only 20 bps from last year. And you remember last year was a bit of a tough comp given the significant recoveries we got last year that we don't expect to recur.

**Operator** (Operator):
Your next question comes from the line of Brian Morrison from TD Cowen.

**Brian Morrison** (Analysts):
I appreciate all the answers today. I just have a couple of housekeeping. Phil or Swamy, can you just remind me what the complete vehicle assembly theoretical capacity is in Europe? I think it was like 150,000 units several years back. And what is the volume capacity in Arizona and Asia? And then second question, just quickly for housekeeping. Why the increase in the value of the euro in your updated guide? I realize that most of the year is over, but at $1.11 now, directionally, I'm a little bit surprised it went up.

**Seetarama Kotagiri** (Executives):
Brian, you're right about the approximately 150,000 units, right, in our Europe facility. The one in Arizona, it's not based on paint and body shop and so on. So it's flexible, I would say. So it's just based on a little bit of footprint, but we could be very agile. It's not as asset heavy or capital intensive. So that could flex pretty easily. So it's not constrained by anything.

**Philip Fracassa** (Executives):
And then on the currency, Brian, I would say -- I would just add, we generally tend to snap the line kind of at the end of the quarter, and that's kind of what we did this time around. Currency is going to move around. And you're right, the dollar-euro is sitting at probably $1.12 today, if you will. So a little bit weaker than what we had guided. But in my experience, I think we consistently like to snap the line at the end of the quarter, and that's kind of what we did in this case.

**Seetarama Kotagiri** (Executives):
And Brian, just to add one other thing in China, the complete vehicle assembly capacity is roughly about 180,000 just to complete the picture.

**Operator** (Operator):
Your next question comes from the line of Mark Delaney from Goldman Sachs.

**Mark Delaney** (Analysts):
Looking forward to seeing you soon at the Investor Day. I had another one on Complete Vehicles. I think EBIT for 2H '26 for your current guidance is relatively flat year-on-year. Given all the work Magna is doing in AV upfitting as well as the growing business you're speaking about with the Chinese OEMs, including in Europe, can you help contextualize what that all means for the ability to grow Complete Vehicles EBIT from here?

**Philip Fracassa** (Executives):
Yes, sure. Sure, Mark. So basically, what we're seeing in Complete Vehicles, obviously, this year has been impacted by lower engineering revenue has certainly been the negative. But on the positive side, the launches that we've seen with Chinese OEMs and Graz have gone very well. Those contracts are on a value-added basis. And that's really the model we're going to work going forward in Complete Vehicles is more on a value-added basis. So the margins will be higher. Revenue dollars will be a little bit lower. That's what's given you the dynamic of lower revenue, but higher margins, if you will. But moving forward, again, I do see -- we do see a path for continued growth in Complete Vehicles, whether it's in Graz, in Arizona with the AV business in Asia with some of the work we do there. And then again, with new programs coming in on value add, coupled with operational excellence and continuing to try to get better economics on programs that we launch, we do continue to see, I would say, upside on the margin in Complete Vehicles from here.

**Mark Delaney** (Analysts):
Helpful color, Phil. My other question was on the BES business. I just want -- you already mentioned the role Magna can play with castings and bringing innovative ideas there to OEMs. Could you also clarify whether you're seeing any change in how much stamping business may be available and how Magna can bring value to OEMs as one of the large European OEMs spoke about doing more in-house stampings on their earnings call this week.

**Seetarama Kotagiri** (Executives):
Mark, to be short and simple, we are not seeing anything significant. I think it's one of our core groups, long-standing, and we continue to have discussions and inquiries from customers. I would say if there is a big program or if there is any consolidation, if there is any issues, we typically see customers reach out to us. So I would say we definitely have a seat at the table. And we haven't seen, call it, any negative impact on the type of in-sourcing that if anything, we are one of the, if not the only one that can do some of the things that OEMs do and they depend and ask us to be partners with them. So I'm pretty comfortable and optimistic about continuing that.

**Operator** (Operator):
At this time, there are no further questions. I would like to turn the call back to Louis Tonelli for closing remarks.

**Louis Tonelli** (Executives):
Okay. Thanks, everyone, for listening in today. If you have any follow-up questions, please don't hesitate to reach out to me. Thank you for your interest in Magna, and have a great day.

**Operator** (Operator):
This concludes today's call. Thank you all for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MGA_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明 2026 全年調整後 EBIT margin 展望縮窄上調至 6.3%–6.6%，中點較前次高 15bp（原話："margin of between 6.3% and 6.6%, up 15 basis points at the"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明全年調整後 EPS 展望為 $6.70–$7.30，中點較前次增加 $0.25（原話："adjusted EPS to between $6.70 and $7.30 per share. At the"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明全年自由現金流展望中點上調至 $1.8B，較 5 月多 $100M（原話："cash flow outlook to $1.8 billion at the midpoint, up $100"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 給下半年 EPS 隱含值與 Q3／Q4 的 40-60 切分（原話："adjusted EPS of $3.76. We expect roughly a 40-60 split of"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說 Q3、Q4 的 margin 都預期年增（原話："margins to be up year-over-year in both the third and the"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：管理層給全年加權 growth over market（不含 Complete Vehicles）為 +1% 至 +3%（原話："expect positive growth over market for 2026 in the range of"）
- 2026-07-31｜CEO Swamy Kotagiri｜guidance：CEO 說合併口徑全年 growth over market 為 0% 至 2%（原話："0% to 2% positive growth over market for the full year."）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明全年調整後稅率維持 23%，下半年稅率將高於 23%（原話："expect an adjusted tax rate of 23%, which implies that our"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明 Q2 稅率較 23% 指引帶來 $0.09 EPS 好處，下半年會反轉（原話："tax line, we did have a $0.09 benefit in the quarter"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明下半年有機營收約小幅下滑，主要落在 Q3（原話："guidance at the midpoint would imply we're down kind of"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明下半年 P&V 因出售案減少的營收增為略逾 $400M（5 月為 $350M）（原話："about just over $400 million of revenue coming out of P&V"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：管理層下調中國、上調北美與歐洲產量假設（原話："units, respectively, while we reduced our China production"）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 拆解 Q2 margin 橋：營運表現、量與其他為最大正貢獻（約 75bp）（原話："The largest benefit came from operational performance"）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 說明 Q2 淨關稅成本年減貢獻約 25bp margin（原話："Lower net tariff costs year-over-year added around 25 basis"）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 說明 2026 全年淨關稅逆風與 2025 相近（原話："we currently expect that our net tariff headwind for full"）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 說明 IEEPA 關稅已付逾 $100M、約半數已退回（原話："we probably paid just over $100 million in IEEPA tariffs."）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 說明 IEEPA 退款預期有 80%–90% 回饋客戶（原話："pass backs to our customers and would expect customers to"）
- 2026-07-31｜CEO Swamy Kotagiri｜margin：CEO 說明營運卓越帶來的年度 margin 擴張節奏（35–40bp／年，’23 至 ’26 累計約 200bp）（原話："expansion. As we finished this year, we would add about 200"）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 說明 Q2 的 75bp 中營運卓越占大半，與 35–40bp 區間一致（原話："operational excellence is -- I would say a majority of that"）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 說明新合約經濟條件改善，ʼ27 起新專案預期有較佳經濟性（原話："We do expect better economics on those programs."）
- 2026-07-31｜CEO Swamy Kotagiri｜margin：CEO 說明首半年到下半年回收偏重下半年的節奏仍在，但斜率較去年趨緩（原話："continues, but the slope has softened this year."）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 表示不預期明年有 margin 拖累（回收項目）（原話："operational excellence momentum and the other things we're"）
- 2026-07-31｜CEO Swamy Kotagiri｜risk：CFO 說明下半年有小幅未回收成本逆風（DRAM／記憶體等）已納入展望（原話："unrecovered cost headwind in the second half, but we've"）
- 2026-07-31｜CEO Swamy Kotagiri｜risk：CEO 指出宏觀與地緣政治（中東、貿易政策）仍不確定（原話："macroeconomic and geopolitical conditions remain somewhat"）
- 2026-07-31｜CEO Swamy Kotagiri｜risk：CEO 對美國 50% 本地含量提案表示不評論貿易政策（原話："I think, Ty, I usually refrain from making comments on"）
- 2026-07-31｜CFO Philip Fracassa｜risk：CFO 說明 Complete Vehicles 銷售下滑，因全成本認列客戶量降低（原話："Sales in complete vehicles declined $96 million organically"）
- 2026-07-31｜CEO Swamy Kotagiri｜competition：CEO 說明中國營收約 65% 來自中國 OEM，西方 OEM 在中國失去份額短期會影響銷售（原話："China is about 65% with the Chinese OEMs."）
- 2026-07-31｜CEO Swamy Kotagiri｜competition：CEO 說明對中國 OEM 與供應商進歐洲的防禦論述：平台策略與製造整合能力為護城河（原話："And the technology and the manufacturing DNA and the"）
- 2026-07-31｜CEO Swamy Kotagiri｜product：CEO 公布與歐洲 OEM 的駕駛／乘員監控系統專案得標（原話："We were recently awarded a driver and occupant monitoring"）
- 2026-07-31｜CEO Swamy Kotagiri｜product：CEO 公布奇瑞 800V 二速 eDrive 專案得標（原話："Our recently awarded 800V 2-speed eDrive program with Chery"）
- 2026-07-31｜CEO Swamy Kotagiri｜customer：CEO 提及獲 GM 五項供應商獎（原話："Most recently, Magna earned 5 General Motors Supplier of"）
- 2026-07-31｜CEO Swamy Kotagiri｜customer：CEO 說 2028 年業務已訂單逾 90%（原話："Our business pipeline continues to grow with over 90% of"）
- 2026-07-31｜CFO Philip Fracassa｜capital_allocation：CFO 說明剩餘約 9M 股 NCIB 計畫於 11 月初到期前買完（原話："We are planning to repurchase the remaining shares"）
- 2026-07-31｜CFO Philip Fracassa｜capital_allocation：CFO 說明年度資本配置：提高股息、買完整個 NCIB（逾 $1.5B）（原話："$1.8 billion of free cash flow, we raised the dividend and"）
- 2026-07-31｜CFO Philip Fracassa｜capital_allocation：CFO 說明資本支出預期維持歷史區間（低 4% 水準）（原話："And then managing CapEx within that historical range of 4%"）
- 2026-07-31｜CEO Swamy Kotagiri｜capital_allocation：CEO 說明 Q2 末評等機構口徑槓桿為 1.4x（原話："we ended the quarter with a 1.4x rating agency leverage"）
- 2026-07-31｜CEO Swamy Kotagiri｜capital_allocation：CEO 說明非汽車領域擴張需符合報酬準則，並非為多角化而多角化（原話："The key point is that we are not pursuing diversification"）
- 2026-07-31｜CEO Swamy Kotagiri｜capital_allocation：CEO 回答產能時提及 40 餘座工廠已重組、關閉或縮編（原話："And you've heard me talk about 40-plus plants either"）
- 2026-07-31｜CFO Philip Fracassa｜commitment：CFO 預期未來自由現金流轉換率維持相近水準（原話："we do expect to convert a similar amount of earnings to"）
- 2026-07-31｜CEO Swamy Kotagiri｜commitment：CEO 承諾非汽車機會會在 11 月投資人日提供標準、專案與路徑細節（原話："incremental growth and high return value creation over"）
- 2026-07-31｜CEO Swamy Kotagiri｜commitment：CEO 表示非汽車領域將非常挑剔（原話："So all in all, I think we are going to be very selective."）
- 2026-07-31｜CFO Philip Fracassa｜commitment：CFO 說明 2027 年 growth over market 將重新加速（原話："sets us up well for growth over market to reaccelerate in"）

### 問答異常語氣（迴避／改口／保留）
- MGA_Q2_2026_Earnings_Call_20260731.md｜問：Mark Delaney (Goldman)：已贏得的非汽車業務，能否給出已訂單規模｜答法：CEO 拒絕給任何數字，說不想逐案談，只說是 meaningful wins，留待投資人日
- MGA_Q2_2026_Earnings_Call_20260731.md｜問：Dan Levy (Barclays)：非汽車業務能否對 $40B+ 營收基期形成實質成長｜答法：CEO 未給規模，說「decide what material means」，改約 11 月再談
- MGA_Q2_2026_Earnings_Call_20260731.md｜問：Tom Narayan (RBC)：2028 年已訂單的 margin 輪廓與中國 OEM 占比｜答法：CEO 明說不談各客戶或未來的 margin 輪廓，也未答中國 OEM 占比，留待投資人日
- MGA_Q2_2026_Earnings_Call_20260731.md｜問：Jack Joyce (BofA)：2027 年 growth over market 隱含值｜答法：CEO 說 too early，不給 2027 數字，改談 2026 全年
- MGA_Q2_2026_Earnings_Call_20260731.md｜問：Ty Collin (CIBC)：美國 50% 本地含量規則的影響｜答法：CEO 表示不評論貿易政策，只說需敏捷因應，未量化影響
- MGA_Q2_2026_Earnings_Call_20260731.md｜問：James Picariello (BNP)：Q2 關稅回收是否提前、有無一次性項目｜答法：CEO 稱淨關稅與商務回收較去年為負，CFO 則稱 Q2 關稅有 25bp 正貢獻、全年中性；兩人口徑不同，CFO 另補「Maybe we'll do a little better than that. I mean who knows.」

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
{"date":"20260524","verdict":"B 觀望偏進場（衛星候選）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Adj EBIT margin 結構性擴張至 6.0-6.5%（vs FY24 5.2%）","columns":{"2Y 驗證點":"FY26 全年 Adj EBIT margin ≥ 6.0%（guidance 中緣）","5Y 驗證點":"FY29 Adj EBIT margin ≥ 7.0%（操作槓桿全兌現）","10Y 驗證點":"FY35 EBIT margin 維持 7%+（不再回落至 5%）","具體數字門檻":"FY26 全年 Adj EBIT margin ≥ 6.0%；FY27 ≥ 6.5%","信息來源":"Q1 2026 法說會（已 reaffirm guidance）+ 公司 2026 outlook","漂移觸發條件":"連 2 季 TTM &lt; 5.5% → 削弱；連 4 季 &lt; 5.0% → 反轉"}},{"id":"H2","text":"FCF 持續 .6-2.0B/年，capex 從 .55B 峰值穩定下行","columns":{"2Y 驗證點":"FY26 FCF 達 .7B 中緣","5Y 驗證點":"FY29 累積 FCF .0-9.5B","10Y 驗證點":"FY35 capex/Revenue &lt; 4.5%（vs 高峰 6.0%）","具體數字門檻":"FY26 FCF ≥ .6B；capex/Rev &lt; 4.5%","信息來源":"公司 FY26 guidance + Q1 26 法說會 capex 路徑","漂移觸發條件":"連 2 季 FCF/EBITDA &lt; 50% → 削弱"}},{"id":"H3","text":"市場估值倍數均值回歸至 5Y 均（PE 11-14x）","columns":{"2Y 驗證點":"Fwd PE 12 月內回升至 10-11x","5Y 驗證點":"5Y 內 PE 至少觸及 14x（5Y 均 -25%）","10Y 驗證點":"10Y 區間 8-18x（不超過 5Y 高 25x）","具體數字門檻":"Fwd PE 24 月內 ≥ 11x（5Y 均下緣）","信息來源":"Macrotrends / GuruFocus 5Y PE 數據","漂移觸發條件":"連 2 季維持 &lt; 9x → 結構性 de-rating 持續"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"GM / Ford / Stellantis 工會罷工或新模型延後 → 北美營收 -10%、EBIT margin -150bps","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"UAW / Unifor 談判進度、OEM Q-on-Q production 量","警戒閾值":"單季 Adj EBIT margin &lt; 5.0%（連 2 季減倉）"}},{"id":"R2","text":"第 2 個 Fisker 級別 EV 客戶（如 Lucid / Rivian / VinFast / 中國新勢力）破產 → 認列 0M-0M 沖銷","columns":{"對應假設":"H1 + H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"EV 客戶 cash burn 月數、訂單 cancel 公告","警戒閾值":"單客戶沖銷 &gt; 5% 季度 EBIT → 連 4 季影響 → 大動作"}},{"id":"R3","text":"OEM 大規模 in-source 趨勢 + 中國新勢力擠壓 → MGA 全球市佔結構性流失","columns":{"對應假設":"H1 + H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"MGA 全球 organic growth vs 全球 LVP 差距；中國市場 design wins","警戒閾值":"連 8 季 organic growth underperform LVP &gt; 200bps → 結構性失去份額"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":64.58,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MGA_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
