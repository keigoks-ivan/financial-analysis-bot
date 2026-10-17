你是 stock-analyst **v20 判斷 agent**，標的 IBKR（20261018）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"IBKR","date":"2026-10-18","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBKR_20261018/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBKR_20261018/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_yoy_15_6","label":"GAAP 淨營收（YoY +15.6%）","value":1914,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"},{"id":"f_kpi1_fx","label":"調整後淨營收（排除貨幣避險與 FX 影響）","value":1870,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"百萬美元（約）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"},{"id":"f_kpi2_gaap","label":"GAAP 稅前利益","value":1496,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"},{"id":"f_kpi3_gaap","label":"稅前利益率（GAAP 與調整後皆）","value":78,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"},{"id":"f_kpi4","label":"淨利（含非控制權益）","value":1348,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"},{"id":"f_kpi6_yoy_19","label":"淨利息收入（YoY +19%）","value":1154,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"},{"id":"f_kpi7_yoy_12","label":"佣金收入（YoY +12%）","value":602,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"},{"id":"f_kpi8","label":"客戶帳戶數","value":5.576,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"},{"id":"f_kpi9","label":"客戶權益","value":964.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"十億美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"},{"id":"f_kpi10_darts","label":"客戶 DARTs","value":4.273,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"},{"id":"f_kpi11","label":"客戶保證金貸款餘額","value":105.2,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"十億美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-15","period":"2026-10-15","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-15"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ibkr_gross_margin_pct","label":"IBKR 毛利率","value":90.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBKR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ibkr_operating_margin_pct","label":"IBKR 營業利益率","value":86.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBKR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ibkr_fcf_margin_pct","label":"IBKR FCF 利潤率","value":142.84,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBKR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_schw_fcf_margin_pct","label":"SCHW FCF 利潤率","value":41.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SCHW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hood_gross_margin_pct","label":"HOOD 毛利率","value":81.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hood_operating_margin_pct","label":"HOOD 營業利益率","value":46.03,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hood_fcf_margin_pct","label":"HOOD FCF 利潤率","value":3.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_eps_gaap","label":"稀釋 EPS（GAAP／調整後）","value":"0.69 / 0.67","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"},{"id":"f_kpi12_0_0875","label":"季股息（由 0.0875 調升）","value":0.15,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","unit":"美元／股","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[12]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）","citation":"公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm"},"note":"查無共識數字（未採集）"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":82.69,"period":"2026-10-16（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":1.39,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":37.61,"period":"2026-10-16（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.37,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.71 → 2.7）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":1.87,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.2 → 3.26）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":2.49,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.62 → 3.71）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":2.7,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.26,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.71,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.25,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 2.59 → 2.7（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":31.56,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":19.96,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.54,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":32.54,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 2.7，分子＝快照價 87.87","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.406,"period":"2026-10-18","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-18"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-94763.0,"period":"2026-10-18","unit":"USD m","basis":"yfinance 最新一季：總債務 35230.0、現金 129993.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1703.82,"period":"2026-10-18","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":46125.51,"period":"2026-10-18","unit":"USD m","basis":"市值 140888.51 ＋ 淨負債 -94763.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":7438.69,"period":"2026-10-18","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":8916.38,"period":"2026-10-18","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（9 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":6.2,"period":"2026-10-18","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"IBKR 2026年6月客戶 DARTs 526.9萬，年增53%、月增6%；客戶帳戶約518–519萬，年增約34%","source":"Finance Magnates / ChartMill, Interactive Brokers June 2026 DARTs","url":"https://www.financemagnates.com/forex/interactive-brokers-reports-53-million-darts-in-june-client-growth-continues/","excerpt":"Total client DARTs in June were 5,269,000, representing a 53% increase from June 2025 and a 6% rise from May 2026.","as_of":"2026-07-01","retrieved_at":"20261018","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"IBKR 2026年7月客戶帳戶達531.7萬，年增34%；DARTs 442.6萬，年增27%、月減16%","source":"FX News Group, Interactive Brokers registers 27% Y/Y increase in DARTs in July 2026","url":"https://fxnewsgroup.com/forex-news/retail-forex/interactive-brokers-registers-27-y-y-increase-in-darts-in-july-2026/","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261018","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"IBKR FY2025 10-K 稱預期直接市場接取經紀業務競爭將持續加劇，競爭者含自建電子交易工具的 prime broker 及線上股票、選擇權／期貨經紀商","source":"IBKR Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1381197/000138119726000062/ibkr-20251231.htm","excerpt":"We expect competition to continue and intensify in the future.","as_of":"2026-02-27","retrieved_at":"20261018","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Motley Fool 評論：威脅屬漸進；大型既有業者價格競爭，零售平台簡化開戶；若用戶改重 AI 洞察與介面，競爭焦點可能轉向使用者體驗；未指出特定新進入者","source":"Motley Fool, Can Interactive Brokers Maintain Its Edge in a Changing Brokerage Industry?","url":"https://www.fool.com/investing/2026/02/28/can-interactive-brokers-maintain-its-edge-in-a-cha/","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261018","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 稱截至 2025-12-31 無營業常規以外的重大信用風險集中；信用曝險按單一交易對手及相似屬性群組衡量並設限額。未找到單一客戶營收占比揭露。","source":"Interactive Brokers Group, Inc. Form 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1381197/000138119726000062/ibkr-20251231.htm","excerpt":"To reduce the potential for risk concentration, credit limits are established and exposure is monitored.","as_of":"2025-12-31","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q3 2026：客戶帳戶年增35%至558萬、客戶權益年增27%至9,647億美元、保證金貸款年增36%至1,052億美元；總DARTs 427萬，年增18%但較Q2下降11%","source":"IBKR Form 8-K Ex.99.1 (Q3 2026 results)","url":"https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261018","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"2026年7月帳戶531.7萬（年增34%）、單月淨增131,800；DARTs 6月高峰526.9萬（年增53%）、7月回落至442.6萬（年增27%、月減16%）；管理層將Q2 DART成長歸因於客戶參與度與市場波動，並提及中國大陸對Tiger、Futu等同業的監管行動帶來券商轉入","source":"fxnewsgroup / Zacks / Q2 2026 earnings call coverage","url":"https://fxnewsgroup.com/?p=45732","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"共識預估IBKR 2026與2027年EPS分別年增22.8%與18%","source":"Zacks 月度指標報導","url":"https://www.zacks.com/stock/news/2972080/whats-driving-interactive-brokers-solid-monthly-performance-numbers","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261018","affects":["valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"IBKR FY2025 10-K 表示公司每年接受大量監管詢問與例行檢查，絕大多數不導致罰款或後續行動；並稱監管趨嚴推高合規成本。","source":"Interactive Brokers Group, Inc. Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1381197/000138119726000062/ibkr-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"2021 年 GameStop 軋空相關私人集體訴訟曾含反壟斷主張（MDL，佛州南區）；公司後續公告已不再是其中一案的被告。屬私人訴訟，非政府反壟斷調查，且為舊事。","source":"fxnewsgroup: Interactive Brokers confirms it is no longer defendant in “short squeeze” lawsuit","url":"https://fxnewsgroup.com/forex-news/retail-forex/interactive-brokers-confirms-it-is-no-longer-defendant-in-short-squeeze-lawsuit/","excerpt":null,"as_of":"2021-01-01","retrieved_at":"20261018","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"二手來源稱 Interactive Brokers LLC 2025 年 7 月與 OFAC 以約 1,183 萬美元和解制裁違規（2016–2024）；來源為次級網站，未對照 OFAC 原文。","source":"policyrisk.com IBKR 公司頁 / brokerchooser 監管頁","url":"https://policyrisk.com/world/company/IBKR","excerpt":null,"as_of":"2025-07-01","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"IBKR 2026 Q1 10-Q 將關稅政策列為可影響交易量與市場波動的不確定因素（間接，非直接成本）；搜尋摘要未提供逐字原文，需回 10-Q 風險因素核對","source":"SEC EDGAR, Interactive Brokers Group 10-Q (quarter ended 2026-03-31)","url":"https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000093/ibkr-20260331.htm","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"搜尋中無 2026 年任何出口管制或實體清單點名 IBKR；唯一相關為 2025-07 OFAC 約 1,180 萬美元裁罰（對制裁地區人士提供經紀服務，含交易中國軍工複合體相關證券）","source":"搜尋結果彙整（OFAC 2025-07 penalty，未取得原始頁面）","url":null,"excerpt":null,"as_of":"2025-07-01","retrieved_at":"20261018","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子列有「宏觀、地緣與其他挑戰與不確定性」及國際營運曝險（政治或經濟不穩、監管與央行政策變動），稱可能對業務、財務與經營結果造成重大不利影響；搜尋未見資料中心集中度或實體生產地的具體描述","source":"SEC EDGAR, Interactive Brokers Group Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1381197/000138119726000062/ibkr-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2020-12 IBKR 發生多段服務中斷，公司稱起因為第三方供應商提供的「高可用性」資料儲存系統故障，並將系統模組改接備援復原中心；匿名消息稱硬體故障位於 Equinix NY5（公司未證實）。為歷史事件，非現況單點認定","source":"Bloomberg Law, Interactive Brokers Says Vendor Issue Tangled Trading; Bloomberg 2020-12-08","url":"https://news.bloomberglaw.com/securities-law/interactive-brokers-hit-by-significant-failure-on-system-1","excerpt":null,"as_of":"2020-12-08","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年Q3 佣金收入年增12%至6.02億美元，DARTs年增18%，部分受轉嫁客戶的監管費用推升；淨利息收入年增19%至11.5億美元。","source":"Interactive Brokers Group 2026Q3 results, SEC Form 8-K Ex.99.1","url":"https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm","excerpt":"Commission revenue increased 12% to $602 million on 18% higher DARTs and higher regulatory fees, which are passed through to customers.","as_of":"2026-10-15","retrieved_at":"20261018","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"2026年Q3 客戶交易量：期貨+13%，股票-24%，選擇權-1%。","source":"Interactive Brokers Group 2026Q3 results, SEC Form 8-K Ex.99.1","url":"https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm","excerpt":"Customer trading volume in futures increased 13%, while stocks and options volumes decreased 24% and 1%, respectively.","as_of":"2026-10-15","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年9月 DARTs 411.1萬筆，年增6%；客戶帳戶557.6萬戶，年增35%。","source":"FX News Group, Interactive Brokers Sep 2026 metrics","url":"https://fxnewsgroup.com/forex-news/retail-forex/interactive-brokers-registers-6-y-y-increase-in-darts-in-sep-2026/","excerpt":"4.111 million Daily Average Revenue Trades (DARTs) in September 2026, 6% higher than in September 2025; 5.576 million client accounts, 35% higher than prior year","as_of":"2026-10-01","retrieved_at":"20261018","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年Q2 淨利息收入年增23%至10.6億美元；客戶保證金貸款1,085億美元，年增67%。","source":"Quartr / Webull Q2 2026 earnings coverage","url":"https://quartr.com/events/interactive-brokers-group-inc-ibkr-q2-2026_3PCCsyg3","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261018","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"-","claim":"利率敏感度：10-Q 估計美元利率上升0.25%將使年化淨利息收入增加約8,100萬美元（反向降息則對淨利息收入不利）。","source":"IBKR Form 10-Q for period ended 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000147/ibkr-20260630.htm","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Coinbase 正申請 SEC 核准代幣化股票，對零售券商形成競爭壓力；IBKR 已讓部分美國客戶以穩定幣入金（與 tastytrade 同用 ZeroHash 基礎設施）","source":"Stocktwits: Interactive Brokers Turns to Stablecoins To Compete With Robinhood, Schwab, Coinbase","url":"https://stocktwits.com/news-articles/markets/equity/interactive-brokers-turns-to-stablecoins-to-compete-with-robinhood-schwab-coinbase/cLICVxmREFz","excerpt":"Both tastytrade and Interactive Brokers rely on ZeroHash for underlying infrastructure.","as_of":"2026-08-30","retrieved_at":"20261018","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Motley Fool 評論：IBKR 已有全球券商平台、清算、保證金與機構網路，穩定幣與代幣化對其是增量服務而非全新商業模式","source":"Motley Fool: interactive brokers advantage coinbase robinhood","url":"https://www.fool.com/investing/2026/05/27/interactive-brokers-advantage-coinbase-robinhood/","excerpt":"Unlike many crypto-native companies, Interactive already operates a large global brokerage platform, clearing system, margin platform, and institutional trading network. Stablecoins and tokenization become incremental services layered onto an existing business rather than entirely new business models.","as_of":"2026-05-27","retrieved_at":"20261018","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"零佣金交易使定價壓力成為結構性，IBKR 雖未以免費為品牌仍處於此環境","source":"Motley Fool: Can Interactive Brokers Maintain Its Edge in a Changing Brokerage Industry?","url":"https://www.fool.com/investing/2026/02/28/can-interactive-brokers-maintain-its-edge-in-a-cha/","excerpt":"Even though Interactive Brokers never built its brand on being \"free,\" it still operates in an environment where pricing pressure is structural.","as_of":"2026-02-28","retrieved_at":"20261018","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"IBKR 與韓國 Daol Investment & Securities 宣布策略合作，讓韓國投資人經 Daol 平台接觸全球股票；新聞稿將 IBKR 定位為全球 introducing brokers 的券商技術與 white-label 供應商。","source":"Interactive Brokers 新聞稿：Strategic Collaboration with Daol Investment & Securities","url":"https://www.interactivebrokers.com.sg/en/general/about/mediaRelations/8-26-26.php","excerpt":null,"as_of":"2026-08-26","retrieved_at":"20261018","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q2 2026 財報電話會議：管理層稱 introducing broker（IB）管線強勁、持續導入多家新 IB，並為大型 IB 提供客製化方案。","source":"Full Transcript: Interactive Brokers Group Q2 2026 Earnings Call (Webull)","url":"https://www.webull.com/news/15267423912862720","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261018","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 情緒頁（2026 年 10 月初）：16 位分析師共識為買進，平均目標價約 $80，高 $116、低 $25；UBS 中立目標 $101、Barclays 加碼目標 $115（均 2026-10-07）。","source":"Benzinga IBKR sentiment","url":"https://www.benzinga.com/quote/IBKR/sentiment","excerpt":"Avg Consensus PT $80, -7.7%; Highest Price Target $116; Lowest Price Target $25","as_of":"2026-10-07","retrieved_at":"20261018","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 分析師評等頁（2026 年 9 月）：12 位分析師平均目標價約 $110（9 買進、3 持有）；Goldman 9/2 下調目標至 $113，UBS 9/1 以中立、$102 開始coverage。與 10 月頁的 $80 平均差異大，來源未解釋（分析師集合不同或資料誤差）。","source":"Benzinga IBKR analyst-ratings","url":"https://www.benzinga.com/quote/IBKR/analyst-ratings","excerpt":null,"as_of":"2026-09-02","retrieved_at":"20261018","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"IBKR 2026-10-15 公布 Q3：GAAP 稀釋 EPS $0.69、調整後 EPS $0.67，調整後淨收入 $1.87B，淨利息收入年增 19% 至 $1.15B，佣金收入年增 12% 至 $602M，季股利由 $0.0875 提高至 $0.15。事前 S&P/Visible Alpha 預估營收 $1.85B、NII $1.12B（+15%）；Benzinga 預估 EPS $0.69、營收 $1.89B。未找到公司前瞻性 guidance。","source":"SEC 8-K Ex.99.1 (Q3 2026); S&P Global Market Intelligence 2026-10-14","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/10/interactive-brokers-forecast-to-report-12-yoy-increase-in-q3-revenue","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261018","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 年報揭露：OFAC 制裁案於 2025 年 7 月結案，罰款 1,180 萬美元","source":"Interactive Brokers Group Form ARS FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1381197/000114036126009035/ny20056593x4_ars.pdf","excerpt":null,"as_of":"2025-07-31","retrieved_at":"20261018","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 年報揭露：關於平倉部位的集體訴訟，和解協議於 2026 年 1 月簽署，公平聽證訂 2026-06-17（聽證結果未查到）","source":"Interactive Brokers Group Form ARS FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1381197/000114036126009035/ny20056593x4_ars.pdf","excerpt":null,"as_of":"2026-01-31","retrieved_at":"20261018","affects":["decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#0","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"IBKR 客戶應收款備抵信用損失於 2026 年 6 月底為 2,600 萬美元，2025 年底為 1,800 萬美元，增速快於應收款本身（二手分析，非 10-Q 原文）","source":"finhacker.cz《Interactive Brokers v polovině roku 2026》","url":"https://www.finhacker.cz/interactive-brokers-v-polovine-roku-2026-co-ukazuji-nejnovejsi-cisla/","excerpt":"Interactive Brokers LLC evidoval ke konci června u klientských pohledávek allowance for credit losses ve výši 26 milionů USD (účetní odhad), oproti 18 milionům na konci roku 2025. Opravná položka tak vzrostla rychleji než samotné pohledávky.","as_of":"2026-06-30","retrieved_at":"20261018","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"financial_capital_credit_cycle#1","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"FINRA 客戶保證金餘額 2026 年 7 月降至 1.417 兆美元，自 6 月紀錄高點 1.502 兆美元回落，為有紀錄以來最大單月降幅（二手轉載）","source":"cryptobriefing《US margin debt drops $85B in July, largest monthly decline on record》","url":"https://cryptobriefing.com/us-margin-debt-record-decline-july/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#2","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"IBKR 2026 年 6 月底客戶保證金貸款約 1,089 億美元（各來源數字不一，10-Q 摘要為 108.9B）；Q2 10-Q 已在 SEC EDGAR，未讀全文，NPL/NCO 未取得","source":"autobound.ai 10-Q 摘要；SEC EDGAR ibkr-20260630 10-Q","url":"https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000147/ibkr-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261018","affects":["thesis.R","valuation"],"status":"ok"},{"id":"financial_regulatory_capital_rules#0","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"+","claim":"IBKR 2026-06-30 10-Q：各營運子公司合計超額監管資本 $14.2B（淨資本/合格權益 $17,790M，要求 $3,597M，超額 $14,193M）；IB LLC 淨資本 $10,533M、要求 $2,108M、超額 $8,425M。受 SEC Rule 15c3-1 與 CFTC Reg 1.17 約束，非 Basel CET1 框架。","source":"Interactive Brokers Group, Form 10-Q (period ended 2026-06-30), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000147/ibkr-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261018","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"financial_regulatory_capital_rules#1","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"前一季（2026-03-31）合計超額監管資本 $13.9B（要求 $2,816M），到 6 月要求升至 $3,597M；第三方捷克文分析稱 H1 2026 IB LLC 保證金貸款增約 18.5%、淨資本大致持平（次級來源）。","source":"Interactive Brokers Group, Form 10-Q (period ended 2026-03-31), SEC EDGAR; finhacker.cz","url":"https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000093/ibkr-20260331.htm","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261018","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"financial_regulatory_capital_rules#2","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"美國聯準會/OCC/FDIC 於 2026 年 3 月發布 Basel III endgame 重新提案；ISDA 稱市場風險部分標準法下資本約增 89%（全組合），依現行內部模型核准混合約增 30%。提案適用大型銀行，搜尋未顯示對 IBKR（券商，適用淨資本規則）有直接適用；最終規則時程未確認。","source":"ISDA, US Basel III Endgame: Trading and Capital Markets Impact 2026 Update","url":"https://www.isda.org/?p=1246761","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261018","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"平倉部位集體訴訟於 2026 年 1 月簽署和解協議，公平聽證訂 2026-06-17","source":"Interactive Brokers Group Form ARS FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1381197/000114036126009035/ny20056593x4_ars.pdf","excerpt":null,"as_of":"2026-01-31","retrieved_at":"20261018","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"IBKR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":90.18,"operating_margin_pct":86.5,"fcf_margin_pct":142.84,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBKR","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SCHW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":41.46,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SCHW","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HOOD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":81.49,"operating_margin_pct":46.03,"fcf_margin_pct":3.61,"rd_intensity_pct":19.59},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"IBKR"},"financial_history":{"ticker":"IBKR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":4192000000.0,"revenue_yoy_pct":null,"gross_margin_pct":81.44,"operating_margin_pct":74.57,"net_income":380000000.0,"diluted_eps":0.9375,"free_cash_flow":3899000000.0,"fcf_margin_pct":93.01,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":7787000000.0,"revenue_yoy_pct":85.76,"gross_margin_pct":88.28,"operating_margin_pct":83.77,"net_income":600000000.0,"diluted_eps":1.4175,"free_cash_flow":4495000000.0,"fcf_margin_pct":57.72,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":9316000000.0,"revenue_yoy_pct":19.64,"gross_margin_pct":89.04,"operating_margin_pct":84.17,"net_income":755000000.0,"diluted_eps":1.7325,"free_cash_flow":8675000000.0,"fcf_margin_pct":93.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":10222000000.0,"revenue_yoy_pct":9.73,"gross_margin_pct":89.77,"operating_margin_pct":85.98,"net_income":984000000.0,"diluted_eps":2.22,"free_cash_flow":15744000000.0,"fcf_margin_pct":154.02,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/IBKR/IBKR_Q3_2026_Earnings_Call_20261015.md）

# Q3 2026 Earnings Call
**Interactive Brokers Group, Inc.** | Earnings Calls | 2026-10-15

**Operator** (Operator):
Hello, and welcome to the Interactive Brokers Group Third Quarter 2026 Earnings Call. [Operator Instructions]
I would now like to turn the conference over to Nancy Stuebe, Director of Investor Relations. You may begin.

**Nancy Stuebe** (Executives):
Thank you. Good afternoon, and thank you for joining us for our third quarter 2026 earnings call. Joining us today are Thomas Peterffy, our Founder and Chairman; Milan Galik, our President and CEO; and Paul Brody, our CFO. I will be presenting Milan's comments on the business, and all 3 will be available at our Q&A.
As a reminder, today's call may include forward-looking statements, which represent the company's belief regarding future events, which, by their nature, are not certain and are outside of the company's control. Our actual results and financial condition may differ, possibly materially, from what is indicated in these forward-looking statements. We ask that you refer to the disclaimers in our press release. You should also review a description of risk factors contained in our financial reports filed with the SEC.
The S&P 500 was up 2% this quarter after rising nearly 15% last quarter, maintaining its resilience even as interest rates moved higher due to enthusiasm for both large technology companies and artificial intelligence. However, this performance masked somewhat narrow market breadth as large technology names represented the majority of the S&P 500's gains this quarter. The 10 largest U.S. technology stocks now represent nearly 40% of the total value of the index, which has become more concentrated over the course of the year. The most actively traded names on our platform this quarter continued to be global technology names. Their growth and business traction appeal to investors around the world, who want the ability to invest directly and gain ownership in them and convert their currency inexpensively into USD to do so.
Investors hold these stocks across accounts in hedge funds, in their personal accounts and in their retirement accounts. The flexibility with which they can do so regardless of account type is a major reason for the success of our platform. As can be seen in our over 30% account growth, strong interest continues in opening and funding accounts. We are seeing growth from both institutional and individual investors and in all regions. Pretax profit was a record, and our 78% pretax margin marked the eighth consecutive quarter with margins above 70%. In recognition of this and as a sign of confidence in the strength of our business model, its growth potential and of our capital base, we revisited how we allocate our capital and decided to increase the amount of dividend we pay to $0.60 a year.
We introduced multiple new products and initiatives this quarter. We added access to multiple new exchanges, the Bucharest Stock Exchange, one of the top-performing markets over the past decade, the Texas Stock Exchange, where we are already seeing average daily volume of about 2.5 million shares, and a new options exchange that aims to improve liquidity for larger, particularly institutional options orders. In Brazil, we launched trading of B3 futures on financial indexes, cryptocurrencies and commodities, expanding our Latin America access. We began a limited rollout of cryptocurrency staking, giving our clients a means to earn a return on their coins. In Japan, we now can offer several new ways for clients to enhance their returns, starting with margin lending.
We can also offer our fully paid securities lending program as well as Gaika+, our proprietary offering that enables Japanese clients to earn interest on the eligible non-Japanese yen cash balances in their brokerage accounts. For prediction markets, we introduced trading in short duration event contracts with hourly and 15-minute expirations in crypto, metals and energy. These give clients a way to gain intraday exposure to price outcomes and have increased platform engagement by our clients. Our AI connector remains one of the fastest adopted features we have ever introduced. This quarter, we added Perplexity as an official partner and expanded connectivity to support any AI tool that uses the Model Context Protocol, or MCP, including the coding and desktop assistants preferred by many of our active clients.
We also enhanced the connector with account level P&L, alert management and watch lists and expanded its trading capabilities to include 2-leg option strategies. We also launched autonomous AI trading, which allows eligible clients to connect the AI agent of their choice to their IBKR account and authorize it to trade autonomously. It works with any compatible MCP client or AI platform. Clients can create and fund a dedicated partition for autonomous AI trading within their existing account in a single session without opening a new account. The rollout is underway with autonomous AI trading now available to eligible clients in several countries with additional countries to follow. Clients can trade global stocks and options using a variety of order types and trading sessions, including day, overnight and overnight plus day.
Turning to some of our customer segments. For registered investment advisers, we now offer tax-aware long/short strategies to their customers. Given that our platform is designed for active, sophisticated clients and that we have a long-standing prime brokerage offering, tax-aware accounts that use margin, short selling and securities lending are a good fit for us. We are seeing increased interest in our offering, particularly as other brokers impose limits on these strategies. We have 3 tax-aware strategy providers onboarded now with additional ones coming by year-end and more early next year, offering RIAs a broad range of options. We have been able to utilize our extensive programming expertise to customize the offering for different clients based on their needs.
Our introducing broker pipeline once again was strong, similar to what we saw last quarter, a growing substantial pool of prospects and the continued onboarding of a number of new introducing brokers as well as the growth of existing ones. This quarter, DAOL Investment & Securities, a publicly traded South Korean brokerage firm, launched a global securities trading platform powered by IBKR's technology and trading infrastructure. AI continues to be adopted internally. We are implementing and rolling out AI-assisted tools to our client service team that can retrieve data across multiple internal systems, begin analysis of a simple or a multipart request and present findings to the representative, helping our team serve clients faster and more efficiently.
New account onboarding, compliance and surveillance are all incorporating AI and machine learning to help us scale as we ramp up the flow of new clients and global exchanges. Finally, despite somewhat slower overall trading activity versus the second quarter, our overnight trading volumes continue to rise, increasingly showing how important it is for international investors who want to trade during their waking hours in active liquid markets. Overnight trading rose from 3.5 million trades in the third quarter last year to over 10 million trades this year. We have much planned for the quarters ahead and look forward to sharing further updates in the coming quarters.
With that, I will turn the call over to Paul Brody. Paul?

**Paul Brody** (Executives):
Thank you, Nancy, and thanks, everyone, for joining the call today. And we'll start with our revenue items on Page 3 of the release. We are pleased once again with our financial results this quarter as we again produced near-record adjusted net revenues and record pretax income. Commissions rose 12% versus last year's third quarter to $602 million, the third consecutive quarter our commission revenue has exceeded $600 million. Net interest income rose 19% year-on-year to over $1.1 billion, driven primarily by higher balances. Robust growth in margin borrowing reflected an investing environment that grew more risk-on as the quarter progressed.
Our segregated cash portfolio grew with new accounts. Though as our clients put more funds to work in the market during the quarter, interest on segregated cash was about even with the prior quarter. The interest we paid on our customers' cash balances, which offsets the interest revenue somewhat, also expanded with account growth. Other fees and services generated $88 million, up 33%, primarily driven by higher risk exposure fees in a more risk-on environment than last year, higher market data fees and strong options volumes, which led to higher payments from options exchange-mandated order flow programs. Other income includes gains and losses on our investments, our currency diversification strategy and principal transactions. Note that many of these noncore items are excluded in our adjusted earnings. Without these excluded items, other income was $28 million for the quarter.
Turning to expenses. Execution, clearing and distribution costs were $134 million in the quarter, up $42 million or 46% over the year ago quarter, primarily from the reinitiation of SEC regulatory fees. These fees were 0 in last year's third quarter and $30 million this year -- this quarter. Because they're largely passed through, these fees increased both our commission revenue and execution costs and do not impact profits. Execution and clearing costs were 17% of commission revenue in the third quarter for a gross transactional profit margin of 83%. We calculate this by excluding from execution, clearing and distribution, $28 million of nontransaction-based costs, predominantly market data fees, which do not have a direct commission revenue component.
Compensation and benefits expense was $167 million for the quarter for a ratio of compensation expense to adjusted net revenues of 9%, similar to last year. Our head count at September 30 was 3,286. G&A expenses were $78 million, up from the year ago quarter, with continued expansion of advertising, the predominant factor. Our pretax margin was 78% for the quarter as reported and as adjusted. Income taxes of $148 million reflects the sum of the public company's $60 million and the operating company's $88 million. This quarter, the public company's effective tax rate was 16%, within its usual range.
Moving to our balance sheet on Page 5 of the release. The consistent strength of our business and our healthy balance sheet support our raising the dividend from $0.35 to $0.60 per year, returning capital to shareholders while still maintaining an ample capital base for the current business and future opportunities. Our total assets were 21% higher than the prior year at $243 billion, with growth driven by higher margin lending and segregated cash and securities balances. New account growth also helped drive our record customer credit balances. We continue to have no long-term debt. Profit growth drove our firm equity up 19% to $23.3 billion. We maintain a balance sheet geared towards supporting growth in our existing business and helping us win new business by demonstrating our strength to prospective clients and partners while also considering overall capital allocation.
Turning to the operating data. Customer activity was strongest in futures contracts, up 13% over the prior year with more muted activity in options and stocks. Options volumes were down slightly. Stock share volumes were down 24% versus last year, primarily driven by low-priced stocks where share volume is high relative to notional value. Generally, clients gravitated to larger, higher-quality names where returns far exceeded the rise in most major market indices. On Page 7, you can see that total customer DARTs were 4.3 million trades per day in the quarter, up 18% from the prior year. Commission per cleared commissionable order of $2.59 was down 4% from last year on smaller order sizes across product types.
Turning to net interest margin. Page 8 shows the NIM numbers. Total GAAP net interest income was just over $1.1 billion for the quarter, up 19% on the year ago quarter, and our NIM table net interest income was $1.2 billion, also up 19%. We include for NIM purposes certain income that is more appropriately considered interest, but that for GAAP purposes is classified as other fees and services or as other income. Our NII reflects strong annual increases in balances, along with a mixed bag of policy rate changes across central banks worldwide. Several central banks raised rates in September, providing a minor tailwind to net interest income in the third quarter and further benefit going forward. Together, these factors drove a rise in interest income on margin loans and customer segregated cash, partially offset by higher interest expense on customer cash balances.
Year-on-year, the average U.S. Fed funds rate fell 63 basis points or by 15%. Despite this decline, our margin loan interest was up 36%, and our segregated cash interest was up 4%, both bolstered by higher balances. The average duration of our investment portfolio remained at less than 30 days. Because of the timing of the Fed rate hikes in mid-September, most of their impact will be realized in the fourth quarter. The U.S. dollar yield curve is generally positive in the short to medium term, and we have responded by pushing our duration out a bit while still maintaining a relatively tight maturity match between our assets and liabilities.
Reported securities lending net interest trailed last year's unusually strong result, though both quarters had a few very popular hard-to-borrow names. However, an all-encompassing view of securities lending paints a different picture. A portion of what we earned from securities lending is classified as interest earned on segregated cash. We estimate that if the additional interest earned and paid on cash collateral were included under securities borrowed and loaned, then total net revenue related to securities lending would have been $426 million this quarter, up 36% over the prior year quarter. Fully rate-sensitive customer balances ended the current quarter at $27.8 billion versus $25 billion in the year ago quarter.
Now for our estimates of the impact of changes in rates, given some uncertainty over the direction of U.S. interest rates and the divergent actions of central banks around the world, we look at potential effects of rate moves in either direction. We estimate the effect of a 25 basis point increase or decrease in the benchmark Fed funds rate to be $83 million higher or lower, respectively, in annual net interest income. Note that our starting point for this estimate is September 30, with the Fed funds effective rate at 3.88% and balances as of that date. Any growth in our balance sheet and interest-earning assets would increase these impacts.
About 30% of our customer interest-sensitive balances is not in U.S. dollars. So estimates of the U.S. rate change exclude those currencies. We estimate the effect of a 25 basis point increase or decrease in all the relevant non-USD benchmark rates would increase or decrease annual net interest income, respectively, by $35 million. In conclusion, this was another financially strong quarter, reflecting our continued ability to grow our customer base and deliver on our core value proposition to customers while simultaneously scaling the business. Our business strategy continues to be effective, automating as much of the brokerage business as possible, continuously improving while expanding through new product introductions, what we offer while minimizing what we charge.
And with that, we'd like to open up the line for questions.

**Operator** (Operator):
[Operator Instructions] Our first question comes from the line of Patrick Moley with Piper Sandler.

**Patrick Moley** (Analysts):
So I had one on the dividend, pretty big step-up to $0.15. Could you just walk us through the Board's thinking around sizing that and whether this signals any sort of new payout framework, whether it's a target ratio or a certain level of excess capital that you think is appropriate?

**Thomas Peterffy** (Executives):
We have generally been following the guideline of paying dividends between half and 1% of the market value, and we have fallen somewhat behind. So we are trying to catch up here. And we are going to continue to follow that guideline of paying between half of 1% and 1% of the market value.

**Patrick Moley** (Analysts):
Okay. Great. And then just as a follow-up, Paul, you called out advertising as the predominant driver of the G&A increase. And I know in September, it's only been about a month, but you joined the X Cashtags program and you're offering $100 funding credit there. So could you maybe just give us an early read on what that channel is producing? And should we read the ad spend step-up and the X partnership as maybe a signal that you guys are leaning more into the digital customer acquisition strategy?

**Thomas Peterffy** (Executives):
Yes, we are. That is a correct assumption, and that is exactly what we're trying to spend more money on, but it will take some time to get it correctly lined up.

**Patrick Moley** (Analysts):
Great. Any sort of early read you can give us on how successful it's been or what the customer accounts that are coming over look like?

**Thomas Peterffy** (Executives):
It's been mixed. So while the customers we have been getting lately are higher-value customers, we're getting a smaller number of them.

**Operator** (Operator):
Our next question comes from the line of James Yaro with Goldman Sachs.

**James Yaro** (Analysts):
I wanted to touch on across your key geographies, where you believe Interactive Brokers has the greatest account market share gain opportunity? And as a corollary, where you believe IBKR is still underpenetrated?

**Milan Galik** (Executives):
Well, I wouldn't single out one particular geography. We believe that we have plenty of room to grow in both established and new markets. See, one of our strengths is that we operate a single global platform that is highly automated and can be easily adapted to local regulations and needs without having to build a separate business in each country. So a huge plus. Now the opportunities are not necessarily the same everywhere. In some markets, we see more interest from individual investors, in others from institutions or intermediaries. But that's the advantage of our model. We can serve different types of clients across different markets, and we can expand without significantly increasing our cost.

**James Yaro** (Analysts):
Great. I hope that you might be able to speak to the scale of your tax-aware long/short product for RIAs thus far, perhaps in terms of assets. But -- and then more broadly, just your aspirations for this product from here.

**Milan Galik** (Executives):
Well, in terms of assets by the end of the quarter, it was approximately $300 million. We have only recently started really attracting this client segment. We have very high hopes. We work with 3 or 4 different providers, including AQR, a very well-known name in the space. And we are looking to add more. We are seeing RIAs signing up, although the process is moving more slowly than we would like.
This product, we believe we are particularly well-positioned for. These strategies require margin financing, short selling, securities lending, all of which we have been doing a very good job at for many, many years. We have low financing costs, access to a large pool of lendable securities and the automation to handle these strategies efficiently at scale. And on top of that, other brokers are placing restrictions, which creates additional opportunity for us. So we're very focused on this business, and we think that it has considerable room to grow for us.

**Operator** (Operator):
[Operator Instructions] Our next question comes from the line of Daniel Fannon with Jefferies.

**Daniel Fannon** (Analysts):
You've seen some moderation in client activity in terms of trading. Curious at a high level, if you see anything at a customer or geographic region where you anticipate, maybe some -- a continued slowdown or anything underneath that's a little -- that would be concerning in terms of looking ahead around growth or anything else?

**Milan Galik** (Executives):
Nothing really concerning. As you know, the trading activity is not always the same. In the previous quarter, we probably benefited from some activity that was related to the IPO. There were some IPOs that were supposed to come online this quarter. They have been delayed. The -- we expect the volatility to somewhat increase as we approach the mid-term elections. As the volatility increases, our traders and clients tend to trade more. So no concerns whatsoever.

**Daniel Fannon** (Analysts):
Great. That's helpful. And then you did -- you highlighted a few product rollouts within Japan, I think, around margin, and you mentioned another one. Curious just about the uptake and how to think about the potential contribution from those changes.

**Milan Galik** (Executives):
Our current aim is to migrate the accounts that we have accumulated on behalf of the Japanese residents in our U.S. affiliate to Japanese affiliate. So that is what we're focusing on. That is what we have been in discussions with the regulators about. But at the same time, we have put a very significant effort into offering margin in Japan in a regulatorily compliant way. We have very recently finished the rollout of the so-called passkey, which is another type of second-factor authentication methodology, which is supposed to be resistant to phishing attacks. And right now, we are focusing on making the client account onboarding faster, making the KYC verifications fully digital to the extent that is possible.
So there is still some amount of work left in Japan. But then we believe that we will have everything we need to significantly compete. Now what the headwind that we will be facing is it's difficult to do business in Japan. That is what we have learned over the last couple of years that we have put some significant effort into that country. The -- Japan is culturally very different, very homogeneous. Hopefully, the younger investors will be looking more favorably towards foreign brokers like ours. So we remain optimistic.

**Operator** (Operator):
Our next question comes from the line of Ben Budish with Barclays.

**Benjamin Budish** (Analysts):
Maybe a follow-up on the earlier question on the tax-aware strategy. And maybe you could talk a bit more about the current state of your RIA business. I'm curious, can you maybe remind us what types of RIAs are on the platform today? What types are you sort of attracting that may have been new to Interactive Brokers? Do you think there are opportunities to sort of consolidate a little bit of market share for RIAs that may be using multiple custodians? And just your kind of broader thoughts on this is a kind of an RIA-specific strategy or strategy with appeal to that channel versus something that has appeal to your more kind of higher net worth and active trader customers?

**Milan Galik** (Executives):
So the tax-aware products, they're mainly carried by the financial advisers. These products are suitable for bigger accounts. Those are the types of accounts that the financial advisers carry. As I said, very high hopes for the segment for the various reasons I mentioned. Aside from focusing on the tax-aware portfolios, we are putting some work into making the onboarding of the RIAs easier and smoother, not just those that are interested in these products. So there are some programming projects currently in progress. And we are also looking into significantly enhancing our integrations with the multi-custodial platforms with the hope that the financial advisers that are already custodying with some of our competitors will be more open to bring some of their business to our platform.

**Benjamin Budish** (Analysts):
Got it. That's very helpful. Maybe just a separate follow-up on some new trading product opportunities. I think there wasn't as much discussion, at least this call on things like binary options and single-stock futures. And I think Cboe just very recently got approval for the single-stock KPIs. So just maybe curious your thoughts on some of these newer products. Any expectations for what uptake may look like, that would be helpful.

**Milan Galik** (Executives):
So the Cboe announcement, I think it was either made yesterday or a couple of days ago, very exciting, obviously. I think the prediction markets will welcome the addition of these KPIs on single stocks. We do not yet know when the product will go live. I think Cboe may try to go live by the end of this month. We are working on the project. Our aim is to offer them to our clients a very interesting product. We're very excited about it.

**Operator** (Operator):
Our next question comes from the line of Steven Chubak with Wolfe Research.

**Steven Chubak** (Analysts):
So to start, I wanted to inquire about some recent developments at a large brokerage competitor in the RIA space. They recently introduced a minimum asset threshold of $100 million for RIAs on their platform. It goes into effect sometime in the middle of next year. But many people believe that this could bring more small RIAs in motion. That certainly plays to your firm's strengths. And I was curious if you're hearing this from other RIAs in the industry. Is this driving any uptick in interest in terms of the pipelines and how you believe you're positioned to potentially consolidate share as some of your larger competitors maybe deemphasize some of the smaller firms?

**Milan Galik** (Executives):
So as you said, this is supposed to happen sometime in the middle of next year. The competitor was Fidelity, I believe, and anybody under $100 million is supposed to find a new home. I completely agree with you. We are one of the obvious choices, if not the obvious choice. That is why -- that is part of the reason why some of the work that I mentioned earlier is so relevant and so beneficial. So we have 9 months between now and maybe a little more when this is supposed to happen. So we're going to be working very hard to show a welcoming home to the financial advisers that need to find one.

**Steven Chubak** (Analysts):
That's great color. And for my follow-up, I wanted to just ask about the -- since you mentioned a large introducing broker relationship on the platform, whether you could speak to the pipeline, how that compares to what you were seeing in the IB pipeline, whether it was 6 or 12 months ago, just so we can check at least how the momentum there is trending.

**Milan Galik** (Executives):
I think I would say that it looks pretty much the same as it did the last couple of quarters. A lot of integrations in the pipeline or in the progress. Some of them have gone online. The business continues to attract firms looking to expand their offering and grow their business. Here, one of our key advantages is that we provide a complete solution from the account opening and front-end trading platforms to execution, corporate actions, clearing, custody, along with, I would say, unmatched global multi-asset offering. So that's a very key advantage.
Another big advantage is that the investments that we make in our direct brokerage business also benefit our IBroker clients. As we expand into new markets or asset classes or add new capabilities, these capabilities become available almost immediately to our IBroker clients as well. So we continue to be extremely well positioned to benefit from anyone who wants to become an IBroker.

**Operator** (Operator):
Our next question comes from the line of Dan Welden with Wells Fargo.

**Daniel F. Welden** (Analysts):
You mentioned the rollout of autonomous AI trading. And I wonder what percentage of your customer base do you think will be eligible? And then relatedly, do you think that AI tools are going to help people gain more comfort trading new types of instruments and cause a material step-up in trades per account over the long term?

**Milan Galik** (Executives):
So we started a very limited rollout of the autonomous trading. We had only invited clients who had previously used our human-in-the-loop AI connector. We are planning to expand the eligibility to more clients over the next few weeks. As to the expected activity, so to give you the rough numbers, approximately 3,000 clients of ours were invited over the last several days. Obviously, this number is going to greatly increase. As far as the expected activity, we expect -- as the clients become more comfortable with AI in general, we expect them to become more comfortable with AI making trading decisions on their behalf. The good investors will become much more productive because they will be able to consume and process significantly higher amount of information. They will be able to follow more companies. They will be able to implement trading strategies more easily. So these are the reasons why we expect higher trading volumes related to AI adoption over time.

**Daniel F. Welden** (Analysts):
And then for a follow-up, you're now routing to more venues for prediction markets. How do you feel about the progression and adoption through that channel?

**Milan Galik** (Executives):
So we have added Kalshi and CME and along with ForecastEx we now cover 3 different platforms. We are working on integrating with Polymarket. The integrations are delivering the results that we were hoping for. We have increased the overall volume. Our clients benefit from increased range of products, deeper liquidity, better execution prices.

**Operator** (Operator):
Our next question comes from the line of Brennan Hawken with BMO.

**Brennan Hawken** (Analysts):
I'd like to follow up on the question around dividend. So if you're thinking about a yield basically on market cap, does that mean that if we see a drawdown in market cap where the yield gets pushed above the range that you would consider cutting the dividend? Or is that just something you'd ride out until the market cap recovers? Like how would you think about those parameters?

**Thomas Peterffy** (Executives):
I don't think that we will ever cut the dividend, at least not in any situation that I can imagine sitting here right now.

**Brennan Hawken** (Analysts):
Excellent. Thomas, that's very clear. And then on the more mundane side, so the yield on margin balances ticked up pretty nicely versus last quarter. You referenced a mixed bag of policy rate movements. So could you talk about how much that increase in rates came down to base rate changes versus a mix shift? And how sustainable you think that yield pickup is?

**Paul Brody** (Executives):
Well, it's always a combination of those factors, especially what currencies is coming in and what those central banks are doing. We did see more of a contribution from the non-U.S. dollars during this quarter than in prior, but it all feeds in. The primary driver was the size of the increase in the balances themselves, up 47% on the year and another 8% on the quarter.

**Operator** (Operator):
[Operator Instructions] Our next question comes from the line of Brian Bedell with Deutsche Bank.

**Brian Bedell** (Analysts):
Maybe just one more on the tax-aware strategy. In terms of the economics of that, is it -- should we be thinking of that as simply as you grow margin loans and securities lending is used and obviously, the credits that support that would be the same economics that you are currently getting on those line items? Or would there be a different set of economics for these strategies for RIAs in those areas?

**Milan Galik** (Executives):
The economics would be similar to the rates that we offer to large balances and large accounts today.

**Brian Bedell** (Analysts):
Okay. Great. Great. And then just on -- going back to prediction markets and company KPIs. And as you're connecting to more markets, and obviously, Cboe would be one of them as well, I would think. Is there -- are there any plans to change the user interface for -- to accommodate those different, say, company KPIs? Or would you just be leveraging the same user interface as you are now?

**Milan Galik** (Executives):
That's an interesting question. And I'll go a little bit into the weeds. So the prediction market interface that we offer to our clients today is covering the products that ForecastEx offers, Kalshi offers, CME offers. These are swaps regulated by CFTC. The KPI contracts that are going to be offered by Cboe are classified as binary options. The end result is the same in terms of the payout, but they are actually structured as call and put options that you can both buy and sell. And the calls and puts are not tied together. The call price and the put price together may be larger or larger than $1, which is not possible in the CFTC-regulated markets. So we are going to tie them together. We are going to present them on the user interface that our prediction market traders are used to, but they will also be available on the regular option screens, just like the currently available Cboe binary options on indexes are.

**Operator** (Operator):
Our next question comes from the line of Chris Allen with KBW.

**Christopher Allen** (Analysts):
I wanted to circle back a little bit on the more subdued trading activity in the quarter. Trading activity per account dipped to the lowest level in quite some time. Just wondering if you could provide any color on different customer segments, whether it was kind of broad-based that all customer segments pulled back or there was pullback in certain customer segments more so than others?

**Milan Galik** (Executives):
Broad-based.

**Christopher Allen** (Analysts):
Understood. And then maybe just on the announcements around Japan offering margin and the securities paid lending program, are there any other countries where there's a similar opportunity to expand your offerings there in terms of a major marketplace?

**Milan Galik** (Executives):
There are, but we would rather not discuss them so as not to show the blueprint to some of our competitors that are probably listening to us. As we do the work and as we have products that we can deliver, we will announce those.

**Operator** (Operator):
Thank you. Ladies and gentlemen, I'm showing no further questions in the queue. I would now like to turn the call back over to Nancy for closing remarks.

**Nancy Stuebe** (Executives):
Thank you, everyone, for participating today. And as a reminder, this call will be available for replay on our website, and we will be posting a clean version of the transcript on the site tomorrow. Thanks again, and we will talk to you next quarter end.

**Operator** (Operator):
That concludes today's call. You may now disconnect. Thank you for your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### IBKR_Q2_2026_Earnings_Call_20260721.md
- 2026-07-21｜Paul Brody｜guidance：CFO 給出利率敏感度：Fed funds 升降 25bp 對年化淨利息收入影響各 8,100 萬美元（以 6/30 餘額為基準）（原話："$81 million increase in annual net interest income"）
- 2026-07-21｜Paul Brody｜guidance：非美元基準利率升降 25bp 對年化淨利息收入影響 3,800 萬美元（原話："by $38 million"）
- 2026-07-21｜Nancy Stuebe｜margin：稅前利潤率 77%，連續第七季高於 70%（原話："marking the seventh"）
- 2026-07-21｜Paul Brody｜margin：CFO 的毛交易利潤率口徑：執行清算成本佔佣金 17%，扣除 2,900 萬非交易成本（主要市場資料費）後算出 83%（原話："for a gross"）
- 2026-07-21｜Paul Brody｜margin：SEC 規費重啟使執行清算費用增加 1,900 萬至 3,400 萬，扣除後成長 7%；因轉嫁而不影響利潤（原話："do not impact profits"）
- 2026-07-21｜Paul Brody｜margin：薪酬佔調整後淨收入 10%，去年為 11%；員工 3,265 人（原話："Our head count at June 30 was 3,265."）
- 2026-07-21｜Paul Brody｜margin：G&A 成長，廣告擴張為因素之一（原話："continued expansion of advertising a contributing factor"）
- 2026-07-21｜Paul Brody｜margin：母公司調整後有效稅率 14.7%，低於常態區間，因股價上漲對員工股權計畫的稅務效果（原話："adjusted effective tax rate was 14.7%"）
- 2026-07-21｜Paul Brody｜margin：Fed funds 均值年減 70bp，但融資利息收入仍增 39%、隔離現金利息增 7%，皆由餘額支撐（原話："our margin loan"）
- 2026-07-21｜Paul Brody｜margin：證券借貸全口徑淨收入 3.43 億美元，年增 37%（含隔離現金中的證券借貸利息）（原話："would have been $343 million this quarter, up 37%"）
- 2026-07-21｜Paul Brody｜margin：NIM 表淨利息 11 億美元（年增 28%），與 GAAP 淨利息差在部分歸類於其他費用或其他收入的項目（原話："We include for NIM purposes, certain income"）
- 2026-07-21｜Paul Brody｜margin：投資組合存續期維持 30 天以內，因美元殖利率曲線短中段轉正而略拉長（原話："pushing out our duration a bit"）
- 2026-07-21｜Nancy Stuebe｜customer：新帳戶成長 34%，客戶閒置現金年增 27% 至創紀錄 1,820 億美元（原話："34% growth in new"）
- 2026-07-21｜Nancy Stuebe｜customer：客戶權益年增 40% 至 9,300 億美元（原話："Client equity rose 40% to $930 billion."）
- 2026-07-21｜Paul Brody｜customer：客戶 DARTs 為 480 萬筆／日，年增 36%；每筆可清算佣金訂單 2.64 美元，略低於去年（原話："up 36% from the prior year"）
- 2026-07-21｜Milan Galik｜customer：介紹經紀商管道：連續第四或五季有兩位數整合上線，進行中與已承諾整合數都多於上季；新進機構類型轉向既有業務公司（原話："The type of institutions we have been onboarding"）
- 2026-07-21｜Milan Galik｜customer：中國監管整頓 Tiger 與 Futu 後，IBKR 收到的轉戶帳戶與資產明顯增加，多為既有帳戶搬移資產；是否持續難說（原話："Hard to say whether"）
- 2026-07-21｜Milan Galik｜customer：管理層說明新帳戶成長下 DARTs 與每單佣金未稀釋，部分來自強勢環境，另受大型對沖基金與小帳戶介紹經紀商組合波動影響（原話："partially due to the strong environment."）
- 2026-07-21｜Milan Galik｜customer：被問帳戶成長區域，答覆為全球、全帳戶類型皆成長，未拆分韓國貢獻（原話："We are growing everywhere globally, all the regions"）
- 2026-07-21｜Nancy Stuebe｜product：IBKR 為首家開放韓國交易所與 Nextrade 的線上券商；韓國記憶體晶片股受客戶追捧（原話："We became the first e-broker to offer trading in Korea"）
- 2026-07-21｜Nancy Stuebe｜product：與 Anthropic、OpenAI、xAI 合作推出 IBKR Connector，客戶可將 AI 聊天機器人連接帳戶（原話："we released IBKR Connector in"）
- 2026-07-21｜Milan Galik｜product：AI 下單採 human-in-the-loop，客戶須核准後才成為可執行訂單（原話："we utilize the so-called human-in-the-loop"）
- 2026-07-21｜Milan Galik｜commitment：管理層表示未來某時點會提供完全自主的代理式交易，並設護欄與客戶測試，無時程（原話："We are going to be offering at some"）
- 2026-07-21｜Nancy Stuebe｜product：推出 IBKR Prediction Markets，整合 ForecastEx、CME 與 Kalshi，訂單路由至最佳淨價（原話："unified destination for trading event contracts"）
- 2026-07-21｜Milan Galik｜product：預測市場仍不提供體育與娛樂合約，專注於可能影響客戶投組的事件（原話："we still do not offer sports"）
- 2026-07-21｜Thomas Peterffy｜product：ForecastEx 將持續聚焦天氣類合約，正加入颶風登陸合約（原話："continue to concentrate on weather-related contracts"）
- 2026-07-21｜Milan Galik｜product：加密貨幣永續合約約佔加密貨幣交易量三分之一（原話："roughly 1/3 of the trading that we see is now coming"）
- 2026-07-21｜Nancy Stuebe｜product：夜盤交易量年增近三倍，由 380 萬筆增至 1,090 萬筆（原話："Overnight trading volumes nearly tripled year-over-year"）
- 2026-07-21｜Nancy Stuebe｜commitment：取得 OCC 對全國信託銀行執照的初步有條件核准，計畫年底前完成並上線（原話："We plan to have"）
- 2026-07-21｜Milan Galik｜capital_allocation：扣除各項緩衝後超額資本約 103 億美元，較上季增加約 11 億（原話："is around $10.3"）
- 2026-07-21｜Milan Galik｜capital_allocation：併購：投行寄來的標的信件大增，但目前沒有值得追求者（原話："nothing so far stood out as worthy pursuing it"）
- 2026-07-21｜Paul Brody｜capital_allocation：無長期債務；資產負債表設計為支持成長並考量整體資本配置（原話："We continue to"）
- 2026-07-21｜Thomas Peterffy｜competition：行銷支出提高後報酬率與以往大致相同，並未更高（原話："It is roughly the same."）
- 2026-07-21｜Thomas Peterffy｜risk：被問融資餘額快速成長是否有過度承險，答覆持續監控、對現有水準感到安心，未給數字（原話："we feel"）
- 2026-07-21｜Nancy Stuebe｜risk：客戶承擔更多風險（融資或衍生品部位），交易量成長（原話："clients taking on more risk through either"）
- 2026-07-21｜Milan Galik｜risk：對中國大陸監管：IBKR 不在大陸廣告，並檢查帳戶須證明居住地在大陸以外（原話："We do not"）
- 2026-07-21｜Thomas Peterffy｜commitment：管理層對帳戶成長率拒絕承諾，回憶過去給出 30% 目標後成長率反降至 20%（原話："we don't like to promise"）

### 問答異常語氣（迴避／改口／保留）
- IBKR_Q2_2026_Earnings_Call_20260721.md｜問：Chubak：行銷策略演進是否支持帳戶成長結構性高於 20% 常態｜答法：Peterffy 先稱行銷報酬率與以往大致相同，再答「Yes, but we don't like to promise」，拒絕給成長率數字
- IBKR_Q2_2026_Earnings_Call_20260721.md｜問：Chubak：融資餘額高速成長是否有過度承險跡象｜答法：Peterffy 僅答持續監控與「comfortable」，未提供任何指標或數字
- IBKR_Q2_2026_Earnings_Call_20260721.md｜問：Budish：證券借貸強勁中 SpaceX 佔多少、對 Q3/Q4 的意涵｜答法：Brody 稱難以預測，未拆分 SpaceX 貢獻，改談借貸驅動因素與 stock yield enhancement
- IBKR_Q2_2026_Earnings_Call_20260721.md｜問：Fannon：帳戶成長的區域來源、韓國是否為主要貢獻｜答法：Galik 答「全球皆成長」，未拆分區域或韓國貢獻
- IBKR_Q2_2026_Earnings_Call_20260721.md｜問：Hawken：韓國開放交易的量化影響｜答法：Galik 稱不提供按地區的交易量細節，僅定性描述「a line that goes straight up」

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

## ⑥ 條件附卡（archetype_hint='金融' 命中）：judge_addendum_archetype.md

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
{"date":"20260722","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"結構性帳戶複利延續：全球專業/散戶結構性增長 + B2B IB 通路上移 + 跨資產平台化，帳戶維持 >25% 成長、驅動 EPS 從 FY26 $2.60 至 FY28 $3.39","columns":{"2Y 驗證點":"帳戶 YoY 維持 >25%；客戶權益 YoY >20%","5Y 驗證點":"帳戶基數擴大後 YoY 自然放緩至 15-20% 但客戶權益複利延續","10Y 驗證點":"全球電子券商滲透續升、trust charter 託管 + 新資產類別擴 TAM","數字門檻":"帳戶 YoY >25% / 客戶權益 YoY >20% / FY28 EPS ≥ $3.3","來源":"Q2 26 帳戶 +34%、客戶權益 $930B +40%、Peterffy 重申 >30%（駁 20% 常態說）","漂移觸發":"帳戶 YoY 連 2 季"}},{"id":"H2","text":"NII 韌性：即使 Fed 降息，客戶餘額量增（margin loan、cash）抵消 rate 壓縮，NII 不結構性萎縮","columns":{"2Y 驗證點":"降息週期中季度 NII 不連 2 季 QoQ 下滑；margin loan/cash 餘額續增","5Y 驗證點":"NII 隨資產基數擴大而長期成長，rate 只是週期波動","10Y 驗證點":"NII 與 commission 雙引擎穿越 rate 週期皆成長","數字門檻":"NII QoQ 不連 2 季負；每 25bp −$81M 由量增抵消","來源":"Q2 26 NII $1.0B +23% YoY（avg funds −70bp 下仍增，量增抵）；sensitivity $81M/25bp USD","漂移觸發":"降息中 NII 連 2 季 QoQ 下滑（量增未抵）→ 削弱"}},{"id":"H3","text":"估值：市場為 34% 帳戶成長 + 77% 利潤的品質付 30x+，且此溢價可維持（不 de-rate）","columns":{"2Y 驗證點":"Fwd PE 維持 28x+（不跌破 5Y 中上緣）","5Y 驗證點":"倍數隨成長放緩自然回落至 5Y 中位 ~22x（re-rate 為報酬拖累）","10Y 驗證點":"成熟後倍數收斂至優質金融 18-22x","數字門檻":"Fwd PE ≥ 28x（樂觀維持）；本報告 Base 假設回 22x","來源":"賣方共識目標 ~$95-100（≈現價，無安全邊際）；5Y 分位 ~85%","漂移觸發":"共識 EPS 下修 + PE 跌破 22x → H3 反轉（進場窗開）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"NII 週期反轉：Fed 2026H2–2027 加速降息（−100~150bp）壓 NII（−$320~480M 年化），若交易量同步退潮（無量增對沖）→ EPS 增速降、倍數重設","columns":{"對應假設":"H2/H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Fed funds 路徑、季度 NII QoQ、margin loan/cash 餘額增速、管理層 sensitivity 表","警戒閾值":"降息中 NII 連 2 季 QoQ 下滑 → 削弱；EPS 共識連 2 季下修 → 立即重評倍數"}},{"id":"R2","text":"估值均值回歸：Fwd PE 自 85 分位 / 31x 下修回 5Y 中位 ~22x（即使 EPS 續增，倍數壓縮吞報酬）","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Fwd PE 5Y 分位、共識 EPS 修正方向、賣方目標 vs 現價","警戒閾值":"PE 跌破 25x 且 EPS 未同步上修 → de-rating 進行中"}},{"id":"R3","text":"交易量週期 + 成長品質：DARTs 目前受市場熱度（波動、SpaceX IPO）拉高，退潮則走平；marketing yield 未隨支出提升（成長非來自行銷效率）→ 帳戶增速若減，複利敘事鬆動；China 資產轉入（Tiger/Futu）durability 管理層自認「難說」","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"DARTs、commission/order、帳戶淨增、marketing yield","警戒閾值":"DARTs 連 2 季下滑 + 帳戶 YoY"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE 回 22-25x（~$65-75）或 NII 經降息週期證明韌性（量增抵消，如 Q2 margin loan +39% 抵 −70bp avg funds）；或回測 Bollinger 中軌 ~$82","irr_base_pct":7.0,"ev5y_pct":39.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.0,"ev5y_pct":39.0,"irr_base_pct":7.0,"max_dd_pct":-45.0,"bull_5y_price":175.0,"bear_5y_price":58.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"Fwd PE 回 22-25x（~$65-75）或 NII 經降息週期證明韌性（量增抵消，如 Q2 margin loan +39% 抵 −70bp avg funds）；或回測 Bollinger 中軌 ~$82","price_at_dd":94.42,"archetype":"金融","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBKR_20261018/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
