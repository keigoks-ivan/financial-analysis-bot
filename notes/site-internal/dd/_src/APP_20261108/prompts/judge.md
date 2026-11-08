你是 stock-analyst **v20 判斷 agent**，標的 APP（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"APP","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/APP_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/APP_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":2184.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD mn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001751008/000175100826000068/exhibit991-3q26earningspre.htm"},"note":"高於公司自身指引上緣約 $100mn（Q3 指引 $2,055–2,085mn，來源：Q2 新聞稿）；外部共識未取得"},{"id":"f_kpi1_gaap_operating_income","label":"GAAP operating income","value":1709.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD mn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001751008/000175100826000068/exhibit991-3q26earningspre.htm"},"note":"未取得"},{"id":"f_kpi2_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（公司未報 non-GAAP 營業利益，以此代）","value":1842.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD mn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001751008/000175100826000068/exhibit991-3q26earningspre.htm"},"note":"未取得；Q4 前 Q3 指引 $1,710–1,740mn"},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":1418.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD mn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001751008/000175100826000068/exhibit991-3q26earningspre.htm"},"note":"未取得"},{"id":"f_kpi5_guidance_q4_2026_revenue","label":"Guidance Q4 2026 revenue","value":"2,365–2,395","period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD mn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001751008/000175100826000068/exhibit991-3q26earningspre.htm"},"note":"未取得"},{"id":"f_kpi6_guidance_q4_2026_adjuste","label":"Guidance Q4 2026 Adjusted EBITDA","value":"1,995–2,025","period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD mn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001751008/000175100826000068/exhibit991-3q26earningspre.htm"},"note":"未取得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_app_gross_margin_pct","label":"APP 毛利率","value":88.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APP.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_app_operating_margin_pct","label":"APP 營業利益率","value":77.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APP.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_app_fcf_margin_pct","label":"APP FCF 利潤率","value":64.07,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APP.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_meta_gross_margin_pct","label":"META 毛利率","value":81.03,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_meta_operating_margin_pct","label":"META 營業利益率","value":32.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_meta_fcf_margin_pct","label":"META FCF 利潤率","value":11.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_gross_margin_pct","label":"GOOGL 毛利率","value":60.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_operating_margin_pct","label":"GOOGL 營業利益率","value":33.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_fcf_margin_pct","label":"GOOGL FCF 利潤率","value":4.19,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ttd_gross_margin_pct","label":"TTD 毛利率","value":76.87,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ttd_operating_margin_pct","label":"TTD 營業利益率","value":19.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ttd_fcf_margin_pct","label":"TTD FCF 利潤率","value":28.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_u_gross_margin_pct","label":"U 毛利率","value":61.96,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.U.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_u_operating_margin_pct","label":"U 營業利益率","value":-31.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.U.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_u_fcf_margin_pct","label":"U FCF 利潤率","value":24.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.U.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc","label":"SBC","value":84.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD mn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001751008/000175100826000068/exhibit991-3q26earningspre.htm"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":391.22,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-16.5,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":76.31,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.65 → 16.65）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.01 → 20.01）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（24.27 → 24.27）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":16.65,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":20.01,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":24.27,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.85,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 16.51 → 16.65（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":26.34,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":17.04,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝42.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":42.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":17.08,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝40.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":40.9,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":23.5,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 16.65，分子＝快照價 391.22","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":342.41,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 3516.14、現金 3173.73（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":331.32,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":129962.2,"period":"2026-11-08","unit":"USD m","basis":"市值 129619.79 ＋ 淨負債 342.41","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":8337.19,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":10431.08,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（32 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":15.59,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 391.22 / W52 451.12 / W104 425.32 / W250 205.15 / W250 13週斜率 1.63%"},{"id":"f_ma_w52","label":"52 週均線","value":451.12,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":425.32,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":205.15,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.63,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K FY2025 列示競爭者包含 Meta、Google、Amazon、Unity，部分同時是合作夥伴與客戶，客戶可能自建產品取代 AppLovin。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1751008/000175100826000010/app-20251231.htm","excerpt":"These companies vary in size and include Meta, Google, Amazon, and Unity Software as well as various private companies, several of which are also our partners and clients. Clients who are also competitors may decide to invest in their own offerings rather than continue to use our advertising solutions.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"JPMorgan 估 MAX 在手遊中介市占 >70%、DSP >40%；Q1 app-install 廣告份額 QoQ 與 YoY 上升","source":"Webull 報導（JPMorgan）","url":"https://www.webull.com.au/news-detail/15401856595731456","excerpt":"JPMorgan estimates AppLovin’s MAX mediation platform holds more than 70% of the mobile gaming mediation market. Its AppLovin Ads demand-side platform has more than 40% share.","as_of":"2026-05-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"新進入者 CloudX 推出 SDK-less AI 廣告產品，APP 當日股價下跌","source":"Marketbeat/Nasdaq 文章","url":"https://www.marketbeat.com/articles/applovin-after-46-fall-in-2026-key-reasons-for-optimsm-remain/","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"AppLovin 10-Q 風險因素：廣告解決方案主要在行動 app 生態（特別是手遊），且大量營收經由數個第三方發行平台；管理層稱自 2024 起擴展至網頁電商廣告主（客群分散中）。搜尋未找到任何點名最大客戶導入第二供應商或自製的揭露。","source":"AppLovin Form 10-Q (period 2026-09-30), SEC","url":"https://www.sec.gov/Archives/edgar/data/0001751008/000175100826000069/app-20260930.htm","excerpt":"We face concentration risk in that our advertising solutions primarily operate in the mobile app ecosystem and specifically mobile gaming. Further, a significant amount of our total revenue is derived through mobile applications subject to a limited number of third-party distribution platforms","as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"FY2025 10-K：2025、2024、2023 年無單一客戶占總營收 10% 以上，2025 與 2024 年底也無單一客戶占應收帳款淨額 10% 以上；公司不要求擔保品。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1751008/000175100826000010/app-20251231.htm","excerpt":"No individual customer represented 10% or more of the Company’s accounts receivable, net as of December 31, 2025 or 2024. No individual customer represented 10% or more of the Company’s total revenue during the years ended December 31, 2025, 2024, or 2023.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Fitch 將 AppLovin 長期發行人評等由 BBB 升至 BBB+（聚合站摘要，約 2026-06）。","source":"Investing.com：AppLovin upgraded to 'BBB' by Fitch on strong performance","url":"https://ng.investing.com/news/stock-market-news/applovin-upgraded-to-bbb-by-fitch-on-strong-performance-93CH-2208378","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q2 2026 指引不如預期被歸因於 AXON 模型改進比預期慢，而非廣告主需求下滑；Q3 2026 營收指引 $2.055–2.085B","source":"commonthreadco.com — AppLovin Q2 2026: What the AI Model Pause and Record Ecommerce Spending Mean for Your Campaigns","url":"https://commonthreadco.com/blogs/coachs-corner/applovin-q2-2026-earnings-ecommerce-advertisers","excerpt":"The guidance miss came from AXON model improvements moving slower than projected, not from any drop in advertiser demand or platform effectiveness.","as_of":"2026-08-15","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"消費者（電商）垂直快速成長，3 月較 1 月約 +25%，4 月創單月紀錄、高於任一 Q4 高峰","source":"Hudson Labs — AppLovin Q2 2026 earnings preview","url":"https://www.hudson-labs.com/research/applovin-q2-2026-earnings-preview-app-revenue-guidance-key","excerpt":"The consumer vertical (formerly e-commerce) is scaling rapidly, with March 2026 up ~25% vs. January and April reaching a record month, higher than any Q4 peak.","as_of":"2026-07-30","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"FUNDA 8 月預覽：成長仍健康但對比基期較高而趨緩，遊戲客戶成長略降、電商客戶表現佳","source":"FUNDA substack — previewapp 2q26 e-commerce growth","url":"https://fundaai.substack.com/p/previewapp-2q26-e-commerce-growth","excerpt":"Gaming-client growth eased modestly this quarter, while e-commerce clients performed well.","as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"in-app 廣告市場預測 2025–2028 為 $390.64B、$426.25B、$462.29B、$498.20B（Oberlo 圖表）","source":"Oberlo — In-App Advertising Revenue (2017–2028)","url":"https://oberlo.com/statistics/in-app-advertising-revenue","excerpt":null,"as_of":"2025-01-01","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K FY2025 Item 3 列示的法律程序為證券集體訴訟（class period 2024-11-07 至 2025-03-27），未列反壟斷案件；風險因子僅泛稱反壟斷法可能限制併購。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1751008/000175100826000010/app-20251231.htm","excerpt":"Beginning in early March 2025, certain alleged stockholders filed putative class action complaints against the Company, Adam Foroughi, Matthew Stumpf, and/or Herald Chen asserting claims for alleged violations of Sections 10(b) and 20(a) of the Securities Exchange Act of 1934","as_of":"2026-02-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"SEC 調查仍在進行（Bloomberg 2026-02 報導），範圍未公開、未對公司或高管提出指控；起因報導為違反平台夥伴服務協議以推送更多定向廣告。屬證券／資料收集監管，非反壟斷。","source":"The Star（Bloomberg 轉載）SEC probe involving AppLovin still active","url":"https://www.thestar.com.my/tech/tech-news/2026/02/21/sec-probe-involving-applovin-still-active-bloomberg-news-reports","excerpt":null,"as_of":"2026-02-21","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"報導稱 FTC 調查 AppLovin 的用戶資料收集方式（隱私，非反壟斷）","source":"Game World Observer","url":"https://gameworldobserver.com/2025/10/07/report-ftc-has-launched-an-investigation-into-applovin-over-its-user-data-collection-practices","excerpt":"Report: FTC has launched an investigation into AppLovin over its user data collection practices Published by admin Tags: AppLovin, FTC The U.S. Federal Trade Commission (FTC) has decided to investigate the activities of AppLovin, Bloomberg sources report.","as_of":"2025-10-07","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：公司在中國有營運，美中緊張可能影響業務；美國對部分產品／技術輸往中國要求出口許可，但公司目前產品不受這些管制限制；中國政府曾對美國關稅與出口管制報復，可能間接影響公司。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1751008/000175100826000010/app-20251231.htm","excerpt":"Further, we have operations in China and the continuing tension between the U.S. and China may impact our business and results of operations in the future. The U.S. government has restricted the ability to send certain products and technology to China without an export license. In many cases, these licenses are subject to a policy of denial and will not be issued. While our current products are not restricted by these controls, such controls or future restrictions could impact our business in the future.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K 指出關稅等總經因素可能影響廣告主支出或公司成本；廣告方案可能適用 EAR 出口管制，公司以 IP 封鎖與受制裁對象篩查因應。無實體硬體供應鏈關稅敘述。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1751008/000175100826000010/app-20251231.htm","excerpt":"Economic and political relations between the U.S. and other countries continue to evolve rapidly, including with respect to tariff and other policies, and changing policies may adversely affect our business by harming advertising spending or increasing our costs.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-Q（2026-09 期）稱大量營收透過有限數量第三方發行平台（Apple App Store、Google Play、Meta）","source":"AppLovin 10-Q FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001751008/000175100826000069/app-20260930.htm","excerpt":"Further, a significant amount of our total revenue is derived through mobile applications subject to a limited number of third-party distribution platforms, such as the Apple App Store, the Google Play Store, and Meta.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"風險追蹤站稱 AppLovin 在中國與以色列有營運/員工，受美中緊張與中東衝突成本影響","source":"policyrisk.com APP","url":"https://policyrisk.com/world/company/APP","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收約 21.8 億美元、年增 55%（10-Q）；公司已出售 apps 業務，不再分段揭露營收；成長主要來自核心行動遊戲（模型改進）","source":"AppLovin 10-Q (period 2026-09-30) / stockanalysis.com","url":"https://stockanalysis.com/news/applovin-q3-2026-earnings/","excerpt":"primarily to the core mobile gaming business due to model improvements during the quarter","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q4 2026 營收指引 23.65–23.95 億美元，年增 43%–44%（較 Q3 的 55% 放緩）","source":"AppLovin Q3 2026 earnings release (8-K ex99.1) via search summary","url":"https://www.sec.gov/Archives/edgar/data/0001751008/000175100826000068/exhibit991-3q26earningspre.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"電商／非遊戲廣告主：Needham 將 2026 電商營收預估自 10.5 億上調至 14.5 億美元；自助 AppLovin Ads 於 2026 年 6 月底對所有廣告主開放；管理層稱非遊戲消費廣告業務年增三位數（二手摘要，未核原文）","source":"rallies.ai (Needham) / commonthreadco.com","url":"https://rallies.ai/news/needham-raises-applovin-price-target-to-700-lifts-2026-e-commerce-forecast","excerpt":null,"as_of":"2026-07-02","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"市佔：JPMorgan 估 MAX 中介平台占行動遊戲中介 >70%、AppLovin Ads DSP >40%；威脅為 Unity Vector 與潛在 Meta 競爭；Q1 2026 業界查核稱 APP 安裝份額季增、年增（賣方／通路查核，非稽核數據）","source":"search summary of sell-side notes (fundaai substack / Dolphin Research)","url":"https://fundaai.substack.com/p/previewapp-1q26-no-meta-impact-observed","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收 21.8 億、年增 55%，淨利增 72%","source":"mobilegamer.biz","url":"https://mobilegamer.biz/applovin-posts-record-revenue-of-2-2bn-in-q3-up-55/","excerpt":"AppLovin posts record revenue of $2.2bn in Q3 – up 55% By Vikki Blake / 5th November 2026 AppLovin’s revenue grew 55% year-on-year to a record $2.2bn in Q3 2026.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"AppLovin 10-K FY2025 風險因素稱廣告生態技術變動快，競爭對手可能更快或更有效採用新興技術或商業模式，做出技術上更優越的產品；並提到需因應 AI 對廣告生態的影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1751008/000175100826000010/app-20251231.htm","excerpt":"Further, our competitors may adopt an emerging technology or business model more quickly or effectively than we do, creating products that are technologically superior to ours or attract more users than ours.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"CloudX 以 SDK-less 模式上市，被視為對 AppLovin 護城河的潛在技術威脅，APP 當日股價大跌；創辦人稱定位為補充而非搶客。","source":"Motley Fool: Why AppLovin fell double digits this week","url":"https://www.fool.com/investing/2026/02/06/why-applovin-fell-double-digits-this-week","excerpt":"CloudX can innovate digital ad auctions at scale, increasing trust and speed. Image source: Getty Images. Analysts defend Applovin in the wake In response to the sell-off, some Wall Street analysts weighed in on the new potential threats. Gaming analysts at Wedbush were skeptical that CloudX would be as threatening to Applovin, citing past attempts by Google and others to participate in SDK-le","as_of":"2026-02-06","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"CloudX 推出後 APP 股價下跌，散戶稱可忽略雜訊。","source":"Asianet Newsable: APP stock falls following CloudX launch","url":"https://newsable.asianetnews.com/markets/app-stock-falls-13-following-cloudx-launch-retail-says-ignore-the-noise-articleshow-38fhw5b","excerpt":"APP Stock Falls 13% Following CloudX Launch: Retail Says 'Ignore The Noise' APP Stock Falls 13% Following CloudX Launch: Retail Says 'Ignore The Noise'","as_of":"2026-02-04","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"AppLovin 於 2025-10 將廣告平台改名 Axon，Ads Manager 先以推薦碼制（referral-only）上線，管理層表示 2026 年將全球開放。","source":"Modern Retail：AppLovin rebrands its ad platform as Axon, launches Ads Manager on referral-only basis","url":"https://www.modernretail.co/marketing/applovin-rebrands-its-ad-platform-as-axon-launches-ads-manager-on-referral-only-basis/","excerpt":null,"as_of":"2025-10-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"單一代理商部落格（非公司公告）稱 AppLovin Ads 自助平台已於 2026 年中對所有廣告主開放、不需推薦碼；未見公司一手公告佐證。","source":"Common Thread Collective：AppLovin Ads Is Now Open to All Advertisers","url":"https://commonthreadco.com/blogs/coachs-corner/applovin-ads-now-open-all-advertisers-ecommerce-2026","excerpt":null,"as_of":"2026-07-02","retrieved_at":"20261108","affects":["moat_trend","thesis.H","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026（2026-11-04 公布）營收約 $2.18B vs 分析師共識 $2.07B；調整後 EBITDA $1.84B vs 共識 $1.73B；兩者皆高於公司自身 Q3 指引上緣（營收 $2,055–2,085M、EBITDA $1,710–1,740M）。","source":"StockStory: AppLovin delivers strong Q3 2026 numbers; stockanalysis.com Q3 2026 earnings","url":"https://stockstory.org/us/stocks/nasdaq/app/news/earnings/applovin-nasdaqapp-delivers-strong-q3-2026-numbers-stock-jumps-249percent","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q4 2026 指引營收 $2,365–2,395M、調整後 EBITDA $1,995–2,025M；中點高於共識（營收共識約 $2.25B、EBITDA 共識約 $1.88B，後者僅單一來源）。","source":"StockStory; CoinCentral（Q4 營收共識）","url":"https://stockstory.org/us/stocks/nasdaq/app/news/earnings/applovin-nasdaqapp-delivers-strong-q3-2026-numbers-stock-jumps-249percent","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"財報後盤後股價報導上漲約 24–25%。","source":"StockStory; CoinCentral","url":"https://stockstory.org/us/stocks/nasdaq/app/news/earnings/applovin-nasdaqapp-delivers-strong-q3-2026-numbers-stock-jumps-249percent","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布（Investing.com UK 頁，日期不明、最新條目約 2026-02）：26 位分析師平均 12 個月目標價 714，區間 458–860；為舊於 Q3 2026 財報的數字，非財報後共識。","source":"Investing.com UK Applovin consensus estimates","url":"https://uk.investing.com/equities/applovin-consensus-estimates","excerpt":null,"as_of":"2026-02-12","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"證券集體訴訟（10b-5）自 2025-03 起在加州北區提起，修正訴狀列 Foroughi、Stumpf、Chen、Shikin 為被告，集體期間 2024-11-07 至 2025-03-27，仍在進行（FY2025 10-K）。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1751008/000175100826000010/app-20251231.htm","excerpt":"The Amended Complaint alleges a putative class period running from November 7, 2024 through March 27, 2025.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"Bloomberg 報導 SEC 調查 AppLovin 資料蒐集／廣告做法（2025-10，股價單日約 -14%）；搜尋結果未見 2026 年結案或執法進展。","source":"StreetInsider/Reuters: AppLovin probed by US SEC over data-collection practices, Bloomberg News reports","url":"https://www.streetinsider.com/Reuters/AppLovin+probed+by+US+SEC+over+data-collection+practices%2C+Bloomberg+News+reports/25424385.html","excerpt":null,"as_of":"2025-10-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月（2025-11-08至2026-11-08）8-K 共6份，含重大項目（1.01/1.02/1.03/2.01/2.05/2.06/3.01/4.02/5.01/8.01）者0份，無併購、重編等8-K事件。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001751008&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K無含2.01/1.01等重大項目者；搜尋未見2026年併購。2025-05 出售手遊工作室組合予 Tripledot（約$800m，窗外）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001751008&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"證券集體訴訟進行中，集體期間 2024-11-07 至 2025-03-27。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1751008/000175100826000010/app-20251231.htm","excerpt":"The Amended Complaint alleges a putative class period running from November 7, 2024 through March 27, 2025.","as_of":"2026-02-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"-","claim":"Bloomberg 報導 SEC 調查資料蒐集做法（2025-10）；未見2026年進展，近12個月8-K無Item 4.02重編。","source":"StreetInsider/Reuters: AppLovin probed by US SEC over data-collection practices, Bloomberg News reports","url":"https://www.streetinsider.com/Reuters/AppLovin+probed+by+US+SEC+over+data-collection+practices%2C+Bloomberg+News+reports/25424385.html","excerpt":null,"as_of":"2025-10-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"APP","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":88.78,"operating_margin_pct":77.78,"fcf_margin_pct":64.07,"rd_intensity_pct":4.97},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APP","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"META","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":81.03,"operating_margin_pct":32.86,"fcf_margin_pct":11.86,"rd_intensity_pct":31.68},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"GOOGL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.86,"operating_margin_pct":33.32,"fcf_margin_pct":4.19,"rd_intensity_pct":15.81},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"TTD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":76.87,"operating_margin_pct":19.61,"fcf_margin_pct":28.38,"rd_intensity_pct":18.12},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTD","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"U","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":61.96,"operating_margin_pct":-31.46,"fcf_margin_pct":24.66,"rd_intensity_pct":50.23},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.U","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"APP"},"financial_history":{"ticker":"APP","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":2817058000.0,"revenue_yoy_pct":null,"gross_margin_pct":55.41,"operating_margin_pct":-1.7,"net_income":-192746000.0,"diluted_eps":-0.52,"free_cash_flow":412111000.0,"fcf_margin_pct":14.63,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":1841762000.0,"revenue_yoy_pct":-34.62,"gross_margin_pct":80.64,"operating_margin_pct":41.94,"net_income":357211000.0,"diluted_eps":0.98,"free_cash_flow":997611000.0,"fcf_margin_pct":54.17,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":3224058000.0,"revenue_yoy_pct":75.05,"gross_margin_pct":83.85,"operating_margin_pct":59.27,"net_income":1579790000.0,"diluted_eps":4.53,"free_cash_flow":2073458000.0,"fcf_margin_pct":64.31,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":5480717000.0,"revenue_yoy_pct":69.99,"gross_margin_pct":87.86,"operating_margin_pct":75.75,"net_income":3333764000.0,"diluted_eps":9.75,"free_cash_flow":3942776000.0,"fcf_margin_pct":71.94,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/APP/APP_Q3_2026_Earnings_Call_20261104.md）

# Q3 2026 Earnings Call
**AppLovin Corporation** | Earnings Calls | 2026-11-04

**David Hsiao** (Executives):
Welcome to AppLovin's Earnings Call for the Third Quarter ended September 30, 2026. I'm David Hsiao, Head of Investor Relations. Joining me today to discuss our results are Adam Foroughi, our Co-Founder and CEO; and Matt Stumpf, our CFO. Please note, our SEC filings to date as well as our financial data and press release discussing our third quarter performance are available at investors.applovin.com.
During today's call, we will be making forward-looking statements, including, but not limited to, the future development and reach of our platform, our expected growth opportunities, the expected future financial performance of the company and other future events. These statements are based on our current assumptions and beliefs, and we assume no obligation to update them except as required by law. Our actual results may differ materially from the results predicted. We encourage you to review the risk factors in our most recently filed Form 10-Q for the fiscal quarter ended June 30, 2026. Additional information may also be found in our quarterly report on Form 10-Q for the fiscal quarter ended September 30, 2026, which will be filed today.
We will also be discussing non-GAAP financial measures. These non-GAAP measures are not intended to be superior to or a substitute for our GAAP results. Please be sure to review the GAAP results and the reconciliations of our GAAP and non-GAAP financial measures in our earnings release and financial update available on our Investor Relations site. This conference call is being recorded and a replay and transcript will be available for a period of time on our IR website.
Now I'll turn it over to Adam and Matt for some opening remarks, then we'll have the moderator take us through Q&A.

**Adam Foroughi** (Executives):
Thanks, everyone, for joining us today. We delivered a record quarter revenue of $2.18 billion, up 55% year-over-year, the largest sequential dollar step-up in revenue with well over $200 million more than last quarter. Both revenue and EBITDA came in well above the high end of our guidance. That's the standard we've always run this business by outperforming our expectations. That result belongs to our team. They're carrying out a model transition as significant as AXON 2.0, while running the business at full speed, and they delivered both in the same quarter. I want to thank them.
Here's what drove it. During the quarter, we partially rolled out the next generation of our models built on the architectural changes I described last quarter. Performance was strong advertisers saw more spend deploying profitably at their target return on ad spend goals and budgets stepped up. And our gaming business grew nearly 50% year-over-year, reaccelerating right alongside the rollout. Here's the part I want you to sit with. This was a partial rollout. The transition is still in front of us, and the new generation gives us meaningfully more room to optimize in the architecture it replaces. It also improves performance most where data is sparser, newer advertisers, smaller advertisers, newer categories, exactly where our consumer vertical lives.
As always, model gains won't land on a perfect quarterly schedule and we won't promise the cadence, but the headroom is real, and we're still very early. Just as important, we did it with discipline. While part of the team trained the new models, our engineers optimized how we serve them. So even as training investment increased, data center costs declined as a percentage of revenue. Every dollar of this investment is gated on return. In this quarter, you saw both halves of that, the return in revenue and the discipline in margin. Consumer had another strong quarter and with Q4 now underway, the seasonal peak for these advertisers Consumer is set up very well heading into the biggest spending season of the year.
On the long term, nothing has changed. We run 1 auction across multiple advertiser categories. Gaming keeps improving. Consumer keeps adding runway. And we believe this business can compound at roughly 30% annually over the long term. And as this year shows, we intend to run well ahead of that whenever we can. Our focus heading into next year is consistent. Complete the model transition and optimize on top of it, expand spend from our current customers while really ramping up the rate of acquiring new customers, keep improving our creative tools and ad formats and start expanding our efforts on CTV. Let me close with this. A quarter ago, we stood here answering questions about a miss. We told you what had happened that it was fixed and that the business was reaccelerating. And everything we told you showed up in this quarter's numbers. That's how we'll keep operating, build for the long term, be transparent about challenges and opportunities and compound through the noise.
With that, I'll turn it over to Matt to walk through the financials.

**Matt Stumpf** (Executives):
Thanks, Adam, and thanks to everyone for joining us today. AppLovin posted record third quarter earnings. Net income grew 72% year-over-year to $1.44 billion on record revenue of $2.18 billion up 55% year-over-year with an industry-leading 66% net income margin and 84% adjusted EBITDA margin. Revenue grew 14% sequentially and exceeded the high end of our guidance by approximately $100 million, primarily driven by the core mobile gaming business due to model improvements during the quarter with continued scaling in the consumer vertical.
Consumer advertiser spend continues to have healthy growth with spend up double digits quarter-over-quarter and growing triple digits from the same quarter last year. Adjusted EBITDA was $1.84 billion, up 59% year-over-year. and also above the high end of our guidance range at an 84% margin, up approximately 190 basis points from the same period last year. Quarter-over-quarter flow-through to adjusted EBITDA was 87%. Operating leverage remains strong. Our data center costs declined as a percentage of revenue due to optimizations rolled out by our infrastructure team, even as we invested in an additional compute for training our existing models and for new model development. We manage this business to EBITDA dollars and free cash flow rather than to a margin percentage, and we'll continue to deploy dollars when we see an opportunity to produce more revenue.
Free cash flow for the quarter was $1.4 billion or 77% of adjusted EBITDA, up from 53% in the second quarter. As I mentioned on last quarter's call, second quarter conversion was depressed by the timing of cash tax payments. We still expect full year free cash flow conversion of roughly 70% to 75% of adjusted EBITDA. To put our results in context, this earnings season, the largest platforms in digital advertising reported third quarter revenue growth between roughly 10% and the mid-20s year-over-year. We grew 55%, several times faster than the market. And we did it at margins well above all of our peers across the advertising space. The contrast is even sharper on cash. This quarter, our asset-light model converted roughly 65% of revenue into free cash flow. We ended the quarter with $3.17 billion of cash against $3.5 billion of long-term debt which puts net leverage below 0.1x adjusted EBITDA, comfortably below the roughly 1x net leverage where we expect to operate over the long term.
During the third quarter, we repurchased and withhold a total of 4.1 million shares for $1.4 billion, a meaningful step-up from the second quarter and ended the -- quarter with 331 million shares outstanding. Given our continued confidence in the company's future, our Board of Directors increased our share repurchase authorization by an incremental $3.2 billion, bringing our total current authorization to $3.6 billion as of the end of October.
Since we began the program, we have repurchased and withheld a total of 104 million shares for $9.4 billion at an average price of $90 per share, returning 85% of our free cash flow over that period and reducing our share count materially. Our weighted average diluted share count has now declined for 8 consecutive quarters and is down approximately 2% from a year ago, even as we invest in the business. That combination, 55% growth with a shrinking share count is one very few companies can match.
Turning to our outlook for the fourth quarter of 2026. We expect revenue between $2.365 billion and $2.395 billion, representing approximately 43% to 44% year-over-year growth or 8% to 10% sequentially. We expect adjusted EBITDA between $1.995 billion and $2.025 billion, representing approximately 43% to 45% year-over-year growth. At the midpoint, this guidance implies full year 2026 revenue and adjusted EBITDA growth of more than 50%. That outlook reflects normal seasonality, further scaling in our consumer vertical, significant model improvements that are already live and performing and continued investment in training compute for new model development.
To close, we exceeded the high end of our guidance on both revenue and adjusted EBITDA, grew revenue 55% year-over-year, expanded margins, generated $1.4 billion of free cash flow and returned $1.4 billion to shareholders. Our fourth quarter outlook reflects that same trajectory.
With that, let's move to Q&A.

**Operator** (Operator):
[Operator Instructions]. Our first question will come from James Heaney.

**James Heaney** (Analysts):
Yes. Great. Just a couple for me. I'll start with Adam. Could you just talk about these new generations of models that you're rolling out? Just curious what's the biggest improvement that you see as compared to AXON 2? And then anything around just timing of the full rollout? And then I'll ask one to Matt.

**Adam Foroughi** (Executives):
James, we talked about it last quarter, but one of our objectives was try to get to a place where we could build bigger models, use more compute and try to train a model that has better output. And so I foreshadowed it for you last quarter. We're now starting to roll those out. We've seen good results. We can't tell you or commit to when we can actually see a full rollout or how the progression of these models will go. But what I said in the talk track is these models have a lot more room to optimize them than the old generation that we were on. So we're really excited about the future.

**James Heaney** (Analysts):
Great. And then one for Matt. Just on the surface, it feels like the Q4 revenue guide of the 8% to 10% sequential growth seems a get a bit more conservative versus the 14% in Q3 when you layer in the strength of e-commerce in the quarter for Q4? Just how would you frame up that sequential deceleration?

**Matt Stumpf** (Executives):
Yes. I mean our guidance philosophy remains the same from what we've done over the past few quarters. We're guiding to what we know at that point in time. So we're guiding to include the points that I said in my script, which are normal seasonality within the quarter, the model updates that we've already launched and are live and performing and then obviously, the increase in the data center costs. So nothing there has really changed from previous quarters.

**Operator** (Operator):
Your next question comes from Jason Bazinet with Citi.

**Jason Bazinet** (Analysts):
Just 1 question. I think last quarter, you guys talked about leaning into the referral program a bit more. I was just wondering if you could give us an update on whether you're pleased or not with the progress you're making with those partners.

**Adam Foroughi** (Executives):
Yes. Jason, still work in progress. Obviously, this is going to be multi-quarter, multiyear trajectory on this business. We're early in doing partnerships. But as you've seen, even in the rate of Pixel accounts that I think you're publishing is that we've been getting more and more customers coming on and the rate is accelerating. That's only going to compound over time because not only you're going to have more partnership deals, we'll start running more ad campaigns, but you're just going to have more positive sentiment on the product in the market as more customers start getting a good experience and doing it over time because the other thing you got to realize is we've got customers that come on. They have to get campaigns that are scaled and optimized on our platform, they have to run an incrementality study. They have to prove that it works and then they really scale for the long term. So -- and we expect this stuff will just keep compounding over time.

**Operator** (Operator):
Our next question will come from Matthew Cost with Morgan Stanley.

**Matthew Cost** (Analysts):
Great. I guess, does the experience that you've had with this new model that just rolled out does that change your expectations for how much runway there still is ahead to improve gaming ad revenue? Because you've been relatively specific over the course of this year about a 20% to 30% growth expectation and sort of law of large numbers weighing on gaming. Would you reiterate all that at this point? Or is there potentially more headroom than you would have otherwise expected based on how it's gone so far?

**Adam Foroughi** (Executives):
So I mean what we've been specific on the last 2 quarters that we're committed to is an expectation that we can grow this business 30% year-over-year for the long term. And we are a platform that's a unified auction. So let's say, in some world, we grew consumer 1,000% in the next quarter. Well, that's going to create more competition, right? So like you can't look at it verticalized as this consumer business is now growing more and more. It's very hard to judge a vertical by itself in a silo.
Now that said, this model is, for sure, more accurate than the old model, and it has a lot more room to optimize going forward. So if we're able to do that, of course, we would expect that gaming could continue to grow at higher rates for the long term. It's just not something that we need, though, in order to hit that 30% if we have both parts of the business growing pretty quickly. And as we touched on in the talk track, the other side of the business, the consumer side is growing triple digits. So when you have a business like that, that now isn't immaterial in our business, growing at that rate with a lot of opportunity to grow in the future as we go get more customer penetration, it gives us a lot of headroom on future growth opportunity.

**Matthew Cost** (Analysts):
Got it. And then I noticed you mentioned CTV in the prepared remarks. I think it's been a little while since that's something you chose to highlight. I guess, how prominently does that feature into your product road map right now relative to 6 months ago?

**Adam Foroughi** (Executives):
Yes, we're making more progress there. I mean if people watch anything on connected television, you'll start seeing some of our ads and we've got pilot campaigns going now. The product is actually looking very promising. It's early. It's a whole new market. So I wouldn't bank on it at all for being accretive to numbers anytime soon. But it's something that the team is actually gaining a lot of confidence in with where they're at in the product road map. And so if we get to the point where it actually starts showing really good result, for customers, we'll talk about it more. Internally, we're now very excited about it.

**Operator** (Operator):
Next, we'll go to Benjamin Black with Deutsche Bank.

**Benjamin Black** (Analysts):
Adam, you've spoken in the past the need to collect more data on the consumer side to refine the model and to improve performance and then the flywheel around that. And now with the new architecture, do you have sort of line of sight to potentially getting that flywheel to reach sort of a tipping point to where you were with gaming a few years back? And if not, which incremental investments do you think are required?

**Adam Foroughi** (Executives):
No, look, these 2 things go hand in hand, right? Every day that we stay in business, we get customers that come into the platform, they share data with us so we get more data density. So as you fast forward that quarters, years, you then need to pair it with model architecture that can actually process more data and generate better output. So you write a bigger model, more complex model, you train it on a larger compute cluster, and you end up with better output.
And what this new architecture allows us to do on the gaming side and on the consumer side, is just train bigger models. So we're going to be starved for data. The more data we get into the system quicker, the better the output of our predictions model is going to become. And so we're never going to stop looking to go get data, whether it's promoting ourselves through referrals and advertising as we just touched on for new customers or potentially some sort of data acquisition we're going to be looking for ways to get data into this model because we've seen every single time we add more data, we're able to write a more complex model, we're able to train a bigger model and just get a better output on the other side.

**Benjamin Black** (Analysts):
Great. And I guess, how are consumer advertiser budget is shaping up for the holiday shopping season relative to last year. And if you think advertisers see strong returns this quarter, how much of that spend could ultimately prove sticky into '27? Or should we expect a seasonal reset as usual in Q1?

**Adam Foroughi** (Executives):
I think it just follows the normal patterns. I mean, look, we're still early in the curve. It's not even into the holiday season. So that stuff takes form really over the next couple of weeks. But that seasonal reset, I mean, that's consistent in e-com. Now we do have the benefit that so long as we're growing this business at this rate and we're pretty early in its evolution, we still have rate of customer acquisition, allowing us to grow the business even in more traditionally seasonally difficult quarters like the Q1 versus Q4 comp.
With that said, like the same advertiser like-for-like will have a huge Q4 and followed it up with a weak Q1. That's just the reality of the e-commerce business. There, we -- traditionally, if you looked at the business growth sequentially in our business, our Q1s have been pretty strong because gaming has a phenomenon called Q5. We're going into Q1, they know that there's not as much competition. And so the models whether just selecting gaming more often because return on ad spend is compelling or the customers being willing to take bigger risk because they're coming off of a very high-priced Q4 into this post Q4 season. They end up spending very competitively. So we've been more insulated than other advertising companies. But as we get more deep into e-commerce, we should see bigger Q4 is followed by tougher Q1.

**Operator** (Operator):
For our next question, we'll go to Stephen Ju with UBS.

**Stephen Ju** (Analysts):
Right. So I think I was talking to some of the advertisers on your platform and they said something curious. They were anticipating that the pricing on the auction is going to start getting inflated because you're going to have incremental bidders from e-commerce coming in and taking up the prices. So they were preemptively taking some of the budgets to some of your competitors in anticipation of what might be compression of ROI. So which kind of seemed like a strange thing to do, but it did make me worry about, I guess, the amount of inventory, which I think you've addressed in prior periods of this being, I guess, a demand-constrained industry as opposed to supply constrained industry. So can you talk about how your thinking might have evolved or things have changed at all in terms of AppLovin's ability to absorb all this incremental ad spend without having some of the ROI get compressed for some of your incumbent customers.

**Adam Foroughi** (Executives):
Yes. I mean if you look at our business over the last 3 years, we've gotten a lot more competitive. The business is much, much bigger. The ROI or return on ad spend for customers is stronger than it was 3 years ago because the spend is materially larger, right? So the better these models get at taking an impression and predicting an outcome, the more accurate they can price.
Our step-up this quarter in net revenue dollars against the last quarter I don't know how much of our competition that's publicly reporting has in terms of scale to directly compare to that. But I think it's a lot of their annual reported revenue that we just put up in 1 quarter of growth. So I think these industry checks tend to end up being flawed because you're looking at a small subsegment of the ecosystem and the customers that are taking time talking to you all probably aren't working that hard. The ones that are working hard and succeeding probably aren't talking to you all. So I would say we're a pretty good indicator on the market and our technology has proven to be great at getting better pricing for customers. That doesn't mean that just looking at a CPM, the price is not going up. In fact, if we get better targeted so that our conversion rate goes up, the CPM will go up. but the down funnel effect of a better prediction is that the return on ad spend is going up, and that's why we're able to grow so quickly.

**Operator** (Operator):
For our next question, we'll hear from Robert Coolbrith with Evercore.

**Robert Coolbrith** (Analysts):
Just wanted to ask a little bit more about the architecture. Is that something as it becomes larger or allows for more data models get bigger. Is that something that also becomes more generalizable. I know in the past, you talked about keeping the consumer and the gaming model separate, but is that something that -- something where in the models become sort of more generalizable across media types, across client types over time.

**Adam Foroughi** (Executives):
Yes, it's possible -- sorry to interrupt on the second question. But you're right, it is possible that we will eventually be able to take, this architecture in that direction.

**Robert Coolbrith** (Analysts):
Okay. Got it. And then just I wanted to ask a little bit about the brand performance, if you will. We heard from more brands maybe because of the issues in mobile web, both in terms of inventory supply, but also iOS 26 focus more on mobile app inventory. Do you see that as an opportunity that's potentially attractive interesting for AppLovin going forward?

**Adam Foroughi** (Executives):
I mean, certainly, if it's a performance marketer, so I would split up performance brand into true performance where they're optimizing the incremental ROAS or like a down funnel purchase transaction. then you've got performance brand that still is looking for audience reach. A lot of the mobile web advertising and a lot of what's called, I guess, traditionally open web is more of the latter. They're just trying to buy audience and trying to price effectively as cheap as possible to reach that audience. we try to price the discovery all the way to the point of transaction. So that's what they care about, and they're able to track it all on digital, then yes, we think a lot of those dollars will shift into the app space. It clearly performs really well. it's much, much bigger.
I mean if you -- I said this, I think, on the All-In Pod at the All-In Summit, the scale of this space is getting very, very large. We have -- I mean, you can back into the gross spend numbers that we have and they're pretty substantial. And if you then gross that up for the whole space, this is one of the largest advertising opportunities that there are outside of social and search, maybe the largest outside of social and search. So we fully expect more dollars will follow given the performance is there.

**Operator** (Operator):
Our next question comes from Clark Lampen with BTIG.

**William Lampen** (Analysts):
I have 2, if I may. I guess, Adam, I sort of wanted to pull out this model thread. And based on everything that I understand about where you guys are going right now, I think one of the bigger derivative benefits of success would be opening up a lot more inventory or available inventory, I guess, within the same sort of base of games and supply that you have right now, which probably should get filled because of auction dynamics by non-gaming advertisers. Is that right, I guess, just sort of number one, as we think about like the second order benefit beyond just sort of more ads per 100 that you're buying right now translating to revenue-generating customers for a commerce or gaming developer. And if so, I guess, is there a way to frame for us just how significant, I guess, this sort of available or effective supply expansion could be?

**Adam Foroughi** (Executives):
Yes. I mean, look, I think the challenge with supply expansion is that the MAX market or the gaming advertising market is a lot bigger than people realize. So when you've got this market that's in the tens of billions, we can go get new supply. And in fact, this model that we're now on and that consumer vertical growing gives us a lot of opportunity to go get more supply. But there aren't that many supply sources that are sort of open to third parties that could be a huge needle mover in one shot. So then you need to compound it over time.
The reason CTV is compelling to us is there's not a true top of funnel to bottom of funnel performance offering on connected TV. If we can figure that out and be the first to market with something that's scalable there, there's a lot of available inventory that's under monetized there. It's sort of what mobile looked like to us 10, 15 years ago when we started the business. So something like that could be impactful.
Anything else not so much. But that's why we've always talked about this conversion rate. We're still very low on what we think is the possible conversion rate inside this gaming ecosystem. What consumer gives us is a chance to diversify the ads that someone is seeing. So we are showing the same user 20 gaming ads in a week. We might show them 15 product ads and 5 gaming ads. That doesn't mean that the gaming customers lost 75%. It just means that the model can get much more targeted. So those same 5 impressions that would have driven the conversion are still going to sit there. And now all of a sudden, you have all these product ads. So that's really the focus area. That's the largest needle mover in the short, medium term, but long term, for sure, supply expansion is something that we're going to be focused on.

**William Lampen** (Analysts):
Okay. That makes sense. And for Matt, I guess, just sort of net of what I think we were seeing just a moment ago in terms of after-hour share price reaction, your stock is still down ballpark 40% year-to-date, and it's only retraced most of the sort of post 2Q earnings step down, does the buyback give you flexibility or the added authorization that you guys just layered on give you flexibility to be more aggressive, I guess, and opportunistic. If you think that the share is -- or the share price is meaningfully disconnected from intrinsic value? Or is this mostly going to be programmatic going forward?

**Matt Stumpf** (Executives):
No. I mean you saw within the quarter as well, Clark, though, we did a meaningful step up. And so that was directly as a result of what you're referring to, right? That was us opportunistically ramping up. the buyback because we saw this dislocation in the stock price versus the actual intrinsic value of the company. So we have the ability to do that going forward as well.

**Operator** (Operator):
Next, we'll go to Martin Yang with OpCo.

**Martin Yang** (Analysts):
A question for Adam. At the industry conference, you referenced a dynamic product ad for e-commerce, sometimes it can work better than video. So I want to get your thoughts on the longer term, do you think a more diversified ad format is the ultimate goal to make e-commerce more effective? Are you still just waiting on Gen AI video creation to make volume and the quality of video ads higher, and this dynamic product ad is just an intermittent step for your advertisers to get volume to in front of customers?

**Adam Foroughi** (Executives):
Look, I'd say it's both. I mean, as the large language models that are applied to creative continuously improve and there's a lot of companies in this ecosystem building ads now out of the box, you're going to see better advertiser performance. we're also going to create more ad formats that can service the advertisers in hopefully better ways. What we want is diversity of what the consumer sees. When you serve as many ads a day as we do, that diversity of content can create an uplift. And so that's why in my talk track, that was one of the bullets. It's an area of focus for us. This product is still really new. So I mean I know we're a couple of years in, but it's a really new product. the ad format hasn't evolved that much yet. I would fully expect it to evolve a lot more over the next couple of years.

**Martin Yang** (Analysts):
Got it. A follow-up on e-comm, if I may. When you compare this year going into the holiday season versus last year. How would you say the learning budget or learning time is for e-comm customers? How has that improved, if any?

**Adam Foroughi** (Executives):
Yes. I mean, look, learning is two-sided. So our model has gotten better. And this new model architecture also, as I said in the talk track, is faster when there's less data. On the other hand, customers are risk averse going into a new relationship. So when they buy on us, even if the result looks better, they still need to validate it. So in this category, if you talk to the customers, not only do they want to see spend and return on ad spend, they need to run incrementality studies, too.
So there is a slow ramp-up. It's just a fact of the industry, but our product is getting better. Every quarter that we go on and we have a new release part of the space is getting it better is just improving it for current customers. The other space of getting it better is that so a customer now clicks in, they don't have much data on our system. How quickly can you show them a good result because that's how you lower your churn rates.

**Operator** (Operator):
Our next question will come from Rob Sanderson with Loop Capital.

**Robert Sanderson** (Analysts):
A couple of questions on consumer as well, growing triple digits, obviously, good trajectory here. Any commentary on sort of conversion of new leads coming through self-service or through your referral partners or any specifics on customer outcomes. I'm just kind of wondering, there is still a bit of hit and miss kind of depending on sophistication of the advertisers. Are we still seeing sort of similar trends or anything you can comment on sort of how the go-to-market is progressing?

**Adam Foroughi** (Executives):
Yes. I mean look, we're still early in the product. So like if a customer goes through our team, much higher likelihood to succeed than they just go through self-service channel and they're on their own. Now if they go through self-service and they're on their own and they're sophisticated, they absolutely can have success. If they're a very small business, something that is just what you would classify as complete SMB, that's still further into the future for us.
So there is a road map on this thing where the more data you get into the system, the more predictive you can be in the absence of data, and we're not at the point yet where somebody can just plug in tiny business, selling jewelry. We've never seen them before, very little data, very little GMV, and it just plugs in and then they go.
But 5 years from now, if we've got a lot of scale of data and the model has time to get evolved to the point of 5 years from now, you're going to have much better outcomes across the board. So this is a road map. I mean, we got to build this product out over time to tackle every single circumstance, it is working really well for the customers that we either handhold or they come in and are sophisticated.

**Robert Sanderson** (Analysts):
Is ad creative still a primary barrier? Like that was a lot of the points of failure, a lot of things that weren't working it's kind of stalled out at the ad creative. Is that still kind of the primary sticking point? And if we kind of asked this question a year ago, I mean, did you expect the industry to be a little further ahead on Gen AI tools by this point, 1 year ago? It seems like to me at least, maybe things are a little bit slower than we would have thought?

**Adam Foroughi** (Executives):
Yes. I mean, look, on the latter, the large language model companies in the West are focused on something else. And so you have less R&D outside of us on this problem, right? On the former -- I wouldn't call it a barrier, but it is an opportunity cost or opportunity loss for customers that don't invest in creative. If you talk to customers that buy on Meta, they buy on TikTok, they buy on us. There's a constant like point that they make that you need to put more creatives into AppLovin to have success on our platform. So the ones that know that have more success than the ones that don't know that. The ones that don't might be smaller, they may -- it's probably not a barrier to working at all but they're missing a point of scale. And the challenge is that our ads are just much longer and they are seen.
And when you go into another platform and you load 10 ads, they're not seen that long and a lot of them aren't seen. Load 10 ads into our platform, on average, you're getting over 35 seconds of watch time, you just can't do anything else on the screen. It's a full screen ad. And so they are being seen with 100% certainty. So ad count and quality of ad combination is what creates scale in our platform. Some customers know it, they're able to become our large spenders. The others have to learn it.

**Robert Sanderson** (Analysts):
I'm going to try to sneak one more in. So you're talking about significantly larger models, right, step function in scale. Are you generating enough data organically to feed the models? You did talk a little bit, Adam, about maybe opportunities to acquire data. I'm assuming you'd be looking for customer data, transaction data. What types of data to be most helpful? Does it need to be evergreen? Do you need it even are you generating enough organically?

**Adam Foroughi** (Executives):
I mean, look, like obviously, this quarter, we had a fantastic quarter, best we've ever had with the data that we had. So there was no incremental data into the system, right? So there's, on the one hand, just processing the data you have available to you in smarter ways, can create uplifts.
On the other hand, like these models just need more data. I mean there's -- that's consistent across any company in a modeling space. And so getting more data into the system is important for us. We're not rush. The business is doing really well. Every customer we get live is a data relationship on top of a business revenue relationship. But long term, if we can add ways to get data into our system quicker, the business is going to have much more runway in the short term.

**Operator** (Operator):
Next, we'll go to Shweta Khajuria with Wolfe.

**Shweta Khajuria** (Analysts):
Okay. I have a high-level question. Some of my questions were asked. As an ad tech company for investors who are questioning the visibility of your business model and how much confidence you have in the durability of your top line growth. Is there something else incremental that you would consider sharing that give more confidence in terms of the way your product works, the visibility you can offer and the moat that you're building?

**Adam Foroughi** (Executives):
Yes. I mean, look, I think over the last -- I don't know, it's been 16 quarters or something. We've had 15 phenomenal quarters. Our growth rate has been higher than almost any tech company in the world that's public at the scale that we operate at and our margins are probably second to none. And so you've got a business that, while is unpredictable in the future, and we can't really give KPIs to predict something that isn't there, a lot of it is tied to actually us being able to improve our technology. And then a lot of it is tied to new customer growth, but we're so early in that consumer segment, that there's nothing that's material there yet that can be predictive in the future.
You sort of have to make your own guesses. I said this, I think I don't know, maybe 12 quarters ago, early in AXON 2. I said, when human beings tend to think about predicting something, everyone gets negative on the future. In our business, they can be negative and positive. But almost all those quarters, I mean, I think it's been 14 out of 16 that we've beaten the high end of our guidance and not by an immaterial amount, we've been consistently outperforming what anyone would have expected. So I think a lot of this is over time.
People have to go, this is a bigger ad tech company that's sort of independent ad tech without a first-party site, bigger than anything we've ever seen before. We're a very large business at this point. We create a lot of cash flow and we're delivering to our customers in a very large amount of scale, return on ad spend, tens of billions of dollars of revenue on the other side of the ad spend that they put into our platform in any given year. So we're a very large economic force at this point. That ad spend is creating GDP. It's creating new transactions that otherwise wouldn't have been there. So as a very large business, we're growing quickly. We can't give those KPIs that you're looking for because we're just not at that point of stability. But we have something that is a catalyst that is also very valuable. Our engineers improving our models and more data into the system is not predictable, but it can create very high upside.

**Operator** (Operator):
Next, we'll go to Ralph Schackart with William Blair.

**Ralph Schackart** (Analysts):
Adam, on the talk track, you talked about a reference this model step-change is as big as AXON 2.0, I think you said. I'm just curious, is it fair to think of this as a AXON 3.0. Just really trying to frame this model update because when the model transition to AXON 2.0, you had a fairly significant inflection point. Obviously, the business is a lot larger now. But just if you could help conceptualize how impactful this new model will be once it's fully rolled out and impact on the business would be great.

**Adam Foroughi** (Executives):
Yes. I'd put it from a technology standpoint in terms of technical complexity on that level in terms of business. Look, this is the next generation of the model. We're not a direct-to-consumer AI company. And so we don't increment the model. But the reality is this gives us a lot bigger path in the future in terms of processing more data and spinning up bigger clusters and hopefully getting better output. Team is really excited about what it means. We're still in partial rollout. So it has to roll through all of our models. There's still a lot of complex R&D work there. But it gives us a much longer road map than the old models would have given us. So that gets the team really excited.

**Ralph Schackart** (Analysts):
Great. One follow-up. Obviously, the results and I might speak for themselves. But after last quarter, there was a ton of competitive concern. Maybe just give us an update on the market and the competition as you see it today.

**Adam Foroughi** (Executives):
Yes. I mean, look, like the industry checks out there show you all. Other companies are performing really well in the market. We've said since we went public, this isn't zero-sum. Our prediction, the impression, what we price for a customer is going to be different than any other model. What makes this category great is that the sum total of all the models improving, give these customers better businesses. So it's never been the case that other companies growing should squeeze us. I said on the last earnings call, that was not something that actually happened and it was our own footfall. That now shows true to you all. In the face of other companies doing well and it's not just one, it's multiple all at the same time, we put up a massive quarter.

**Operator** (Operator):
For our next question, we'll hear from Bryan Smilek with JPMorgan.

**Bryan Smilek** (Analysts):
I guess, just really curious, Adam, you had mentioned that the All-In Summit, I believe that gross spend flowing through AppLovin's ecosystem was approaching like $20 billion annualized. Can you just talk about going forward in order to achieve that 30% long-term growth algorithm overall? How much of that growth will be from greater realized achievements through this new model versus incrementally adding new customers, both on the gaming and consumer side.
And then, I guess, Matt, more near term, obviously, good to see that performance in 3Q implied 8% to 10% sequential totally appreciate greater consumer seasonality into year-end. But just curious like what's embedded there from a gaming perspective as you continue to roll out the new model?

**Adam Foroughi** (Executives):
Yes, look, long-term growth for us like the components of are hard to predict. Of course, new customers coming on is now going to be a component, not in gaming. We have every mobile gaming company live probably. But in consumer, we're really early. The data in the system will improve the model architecture now gives us a long runway to improve it. So we don't know.
It's also interesting that every quarter, it can be different. If you verticalize the business, we could have a lift on the gaming side that doesn't apply to the consumer side, and that takes off 1 quarter and the next quarter flips. What gets us really excited is that consumer is growing very quickly and it's starting to become more and more a part of our business. That on its own has much longer runway because we're so lightly penetrated into the market of customers. as each quarter goes on, more customers find out about us, that business is going to grow really quickly.

**Matt Stumpf** (Executives):
Yes. On the guide, Bryan, we don't break out, obviously, between gaming and consumer. I won't give you the specific splits. But what we've assumed for gaming and for consumer is consistent. I mean, there's seasonality, right, as we look into Q4, obviously, both are strong for different reasons. You have the consumer period, right, of Black Friday, Cyber Monday and then the holidays, you also have on the gaming side of the business, there's seasonality as well, and Q4 is always strong. So we've assumed that within the guide and then obviously, the model improvements that we've had thus far, those are reflected in the 8% to 10% as well.

**Operator** (Operator):
Next, we'll go to Alex Brondolo with Wells Fargo.

**Alec Brondolo** (Analysts):
Appreciate the question. Maybe 2 for me. I think, first, you mentioned in response to a question about e-commerce or web advertising, the idea of a data acquisition. And I think that there's this kind of idea percolating that there could be tuck-in M&A leverage to kind of accelerate the capabilities in e-commerce. And so perhaps if you could talk about what's the ideal acquisition candidate or what the ideal data you're looking for is that would help people kind of frame that opportunity?
And then secondly, you mentioned the Pixel data, so I guess it's fair game. Clearly, APAC, most of the inflection in the Pixel data, it seems like most of the inflection in e-commerce customer growth is coming from APAC. Why do you think that region is finding kind of stronger product market fit first relative to the U.S. and Europe?

**Adam Foroughi** (Executives):
Okay. I want to take the second first. We've got sales teams on both North America, I guess, EMEA as well. But APAC and the North America team are the 2 biggest. We've always traditionally been focused on both those 2 markets, which are big ones on the Western advertising side. The APAC customers because they're tapping into the Asian supply chain. A lot of times, they spin up sites that are specific to certain type of products that aren't buying elsewhere. So for them, if they go spend $1,000 on us. They either make money or they lose money, but it's very easy because there's no attribution complexity.
So sometimes these Pixel sites are brand-new sites that just didn't exist that are spun up specifically for our channel. North American customers are bigger enterprises. They're not going to go spin up the next version of Wayfair, right? It's one domain. And so you -- it doesn't -- I wouldn't read into the counts as I'm seeing more Pixel counts out of APAC, so they're getting more penetration into the customer base over there. It might be just one is creating a lot because they don't have the same attribution complexity that some of the Western companies do because they're just longer-standing brands.
On the acquiring data, point. The M&A that we did in the past that maybe is our best is when we bought MoPub. We were already succeeding with MAX, so it's a great product. And at the time, no one understood it. This crazy company bought a company and put it out of business. I mean we put it out of business in 90 days. But we got all the customers over to our platform because we just build great products. And by doing that, we ended up with what MAX is today, which everyone knows is a really valuable business. That transaction has paid for itself many times over now.
What we would look for is can we buy data relationships, customer relationships that are valuable for us. We're going to get all these customers over the next decade anyways. But if we could buy it and get the shot in the arm to bring all these customers onto our platform quickly and get all that data into our platform quickly, it will accelerate this business to get through what could be a decade's worth of work in a much shorter amount of time. Same sort of structure is that kind of deal is what we would look for.

**Operator** (Operator):
Our next question comes from Omar Dessouky with BofA.

**Omar Dessouky** (Analysts):
In your old models, you used to continuously retrain on live impression data and that resulted in a steady 3% to 5% self-learning growth. and that's distinct from engineer directed model uplifts. You didn't address it specifically on the last conference call. So can you tell us if you see that same 3% to 5% tailwind from self-learning and intra-quarter model retraining off of live impression data. Did you see it in Q3? Is it assumed in your Q4 guidance? And kind of looking forward, how much visibility do you have as to that component of growth? Or are you just wholly reliant on engineer-directed model enhancements going forward?

**Adam Foroughi** (Executives):
Look, in all these models, you have this sort of reinforcement that happens. You get a prediction, you get data that comes into the system and they get smarter. This is true in any sort of category of companies that are writing these deep learning models at this point. So you don't actually know is it 3%? Is it 3.2%? Is it 4%? You can't really track what the model is improving on its own. But there is always going to be this self-learning notion that exists in a company that's running a model, creating a prediction, reassessing its own prediction and hopefully getting smarter as it goes forward. that's what these models are built to do, right? Like they're structured similar to the human brain. We, as humans, learn from our memories and get smarter as we go forward. These models do the same exact thing. So we just wouldn't split it up into this is a growth driver. Let's plug this number in here. And then on top of it, let's put a model enhancement because we talked about back in the day also we'd have one big one a year. Well, probably over the last 16 quarters, we've had multiple AV test lifts pretty much every single one of those quarters, except the last one that contributed to very outsized growth for the business. The stuff is not all that predictable nor is it able to be dissected down to a specific percentage, but it all compounds into the business that we have today.

**Operator** (Operator):
Next, we'll go to Jim Callahan with Piper Sandler.

**James Callahan** (Analysts):
Adam, I think last year, you mentioned supply growth across MAX growing double digits. Any comment on what that looks like this year or to 2027.

**Adam Foroughi** (Executives):
Yes. I mean, look, it's still strong double digits. I think last quarter, we told you in a single quarter, it grew double digits. So it's a very fast-growing space in the advertising ecosystem, where I think like most ad spaces in terms of the supply growth and value of that supply aren't growing all that fast, probably like very low double digits to possibly single digits, this MAX market is growing at very strong double-digit growth rate every year.

**James Callahan** (Analysts):
Great. And then anything on the cost of supply acquisition. We've kind of heard this come up in checks a little bit that the cost of impression broadly has gone up. Any way to frame how that looks today and kind of how that could look into next year as well?

**Adam Foroughi** (Executives):
Yes. I mean, look, there's 2 drivers to MAX growth, more supply and the cost going up. So cost effectively, company is getting better at monetizing the impressions. The value of the auction goes up, the publisher makes more.
Now on the other side of that, we're either going to have to pay out more for publisher inventory or improve our own technology at that same rate or improve our own technology more than that rate to grow our business even faster than that market. And so a lot of the innovation that we've had over the last 4 years has been the latter. We've been improving our technology better than the market, and therefore, our business is growing much faster than the market is growing.

**Operator** (Operator):
For our next question, we'll go to Vasily Karasyov with Cannonball.

**Vasily Karasyov** (Analysts):
Adam, I wanted to ask you to comment on the take rate directionally maybe compared to last quarter and maybe year-on-year, whatever is easier? And then the question I had with this model, separate models for consumer and gaming, is there -- would there be a reason why the take rate fluctuation on one would be greater than the other. Can you help us like frame it for us, how to think about it?

**Adam Foroughi** (Executives):
Yes. I mean, look, we don't talk about take rate in the business. And frankly, it happens after the fact -- when you have a conversion rate that's a little bit over 1%. If we were buying on 1,000 impressions, somewhere around like 987 of them we're losing money on. So there's no take rate, we lost everything.
On the other ones, you have almost an infinite take rate because you're making a ton of revenue with a very small amount of outlay. So it's just not a function that we optimize to. And it really does tie to the point that I made earlier. If our engineers created a massive uplift in the next 2 weeks, we'd be able to take more because we out-innovated to everyone else in the market. If we innovate at the rate of the market, the market pricing stays consistent, we're sort of where we always are, which is pretty consistent.
And then if we fall way behind, we just disappear for 5 years, our take rate will contract because the market pricing will get better than the rate of improvement on our technology. Now what you've seen with our team and the opportunity that we put in front of us with these different business lines and where we are in them, is that we're really good at executing. We've been able to execute better than others in the ecosystem for a very long amount of time now, our team is very seasoned on improving these technologies. And when they have R&D breakthroughs like we just had, usually those end up being before everyone else. So before anyone else even understands how to have a technological breakthrough like that, we're many quarters or years ahead.

**Vasily Karasyov** (Analysts):
And is there something inherent to consumer versus gaming that would drive different...

**Adam Foroughi** (Executives):
It will be consistently, again, like similar. So I mean the way -- this is why I always say it's like one auction. Let's say, gaming has a predictive value of $20 CPM, so $0.02 for the impression. And a consumer comes in and wins that impression at $21. It's so close to each other. You're paying out to the publisher. And if the model is very predictively accurate, you're not going to have like one bid at $50 and the other one bid at $20, they're pretty competitive to each other.

**Operator** (Operator):
Next, we'll go to Tim Nollen with SSR.

**Timothy Nollen** (Analysts):
I have a question about data and it's about data provenance versus data processing. Question is really who owns the data in your transactions? Is it your mediation platform that processes the data? Or is it like the original game developer or the monetization platform that handled the transaction?

**Adam Foroughi** (Executives):
What data are you talking about? Just mediation data? I don't -- we have a lot of data in our system. So I didn't follow exactly...

**Timothy Nollen** (Analysts):
Yes. Well, the data -- the data originates through transactions. However, whoever processes them, but your mediation platform kind of creates these packages and you have the sort of new package data. So I guess my question is, who owns that data? Is it...

**Adam Foroughi** (Executives):
What is packaged data? If you just give me an example of like an ad served, it will help me answer it for you.

**Timothy Nollen** (Analysts):
So if an ad is served and you process the transaction versus somebody else processes the transaction, you can see the data that is going through these transactions. You incorporate these data into your media -- into your mediation platform. So I guess my question is, is the data -- does the data belong to the original game developer or ad tech company that processes the transaction or through the mediation platform, do you gain providence over that data? Does that make sense?

**Adam Foroughi** (Executives):
I think there's not really because I think there's a disconnect on what you think we have access to mediation. When we have a mediation auction run, there's -- every company bids into the auction. The only data that's available. So to the MAX system, of course, we see all the bids. We don't know what people bid for. But the only data that's available to our AXON models or our system are did we win the ad? Or did we not win the ad? What was the price for the winning auction? And then everyone who loses gets the price for the losing auction.
That's it. No one should have access to what other people serve. We don't have visibility into an auction cleared, someone else want it. They serve exactly X. That exact X is the ownership of the advertising company. The company that wrote a model that created that process a ton of data has a relationship with customers and consumers to show an advertisement. That's their data. It's an output of their models that remains with them. And so there's nothing that like gives us magical data access from the mediation. In fact, when we built MAX, what we did was we commoditized it all. We said everyone is going to have the same access to data as we will as a bidder into MAX because what we wanted was a fair marketplace. The reason MAX out monetizes the rest of the world of mobile gaming is because we made it fair, and that fairness is what drove the price of every single impression to be the highest possible. Does that answer your question?

**Timothy Nollen** (Analysts):
That answers it. Thanks very much, Adam.

**Operator** (Operator):
We'll take our last question from Matthew Swanson with RBC.

**Matthew Swanson** (Analysts):
Great. Congratulations on the quarter. I guess, on the consumer side, Adam, you mentioned there's some handholding in terms of like the initial on-ramp, if you're not a more sophisticated customer. I guess, a 2-parter there. One, how much of it is like on you versus them in terms of improving that initial performance? Is it still about the models? Is it about them learning how to kind of better optimize their usage of the platform. And then secondarily, when you're kind of targeting customers, it seems like these real sophisticated users are more likely to generate revenue immediately. Is that more the priority? Or are you looking for kind of the best long-term partners for AppLovin?

**Adam Foroughi** (Executives):
Yes. And so I mean, I think a lot of this is a learning curve. We're new platform. So a lot of these customers have not bought in games. They're not used to an ad that actually gets watched, and certainly not used to an ad that's watched for that much time. And if you have a shop, I mean, like think about like when I -- sometimes I think about like we're asking the customer to create 60 seconds of content to showcase a shop. I mean, what do you even show in that ad? It's like shops aren't that exciting.
On the gaming side, they're creating mini games, so someone's playing a preview of their game. It's straightforward. So this is just -- there's a learning process here that has to happen. So that the media buyers really understand the framework. And then once they do and more and more media buyers understand it and more agencies are trained, then it will become standardized. There will be playbooks for our platform. but it's not dissimilar to buying on social 10 years ago. It was brand new. The scale was way smaller. People didn't know what to do. Now everyone knows what to do because if you don't, you're probably not scaling your business. And on the priority of the type of customers we go for, we are looking for the more sophisticated ones. That's why these partnership deals make a lot of sense rather than just run AppLovin ads everywhere through strategic partnership deals, we can get real customers coming on.

**Operator** (Operator):
And that concludes the question-and-answer session for this quarter. We thank you all for joining us today. Have a good afternoon.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### APP_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜Matt Stumpf｜guidance：Q3 營收指引 20.55–20.85 億美元，年增 46–48%、季增 7–8%（原話："We expect revenue between $2.055 billion and $2.085 billion"）
- 2026-08-05｜Matt Stumpf｜guidance：Q3 調整後 EBITDA 指引 17.1–17.4 億美元，利潤率約 83%（原話："adjusted EBITDA margin of approximately 83%"）
- 2026-08-05｜Matt Stumpf｜guidance：Q3 指引不含尚未部署的新模型釋出（原話："It does not assume additional"）
- 2026-08-05｜Matt Stumpf｜guidance：本季指引納入已上線模型改善與已增加的算力成本，與過去指引哲學的差異（原話："we've guided inclusive of the model"）
- 2026-08-05｜Matt Stumpf｜guidance：全年自由現金流轉換率預期正常化至調整後 EBITDA 約 75%，Q3 改善（原話："normalize to roughly 75% of adjusted"）
- 2026-08-05｜Adam Foroughi｜guidance：CEO 稱長期可年複合成長約 30%（原話："this business can compound at roughly 30%"）
- 2026-08-05｜Adam Foroughi｜guidance：CEO 承認 Q2 營收略低於指引中點、EBITDA 略低於區間（原話："And this quarter, we fell short of that standard."）
- 2026-08-05｜Matt Stumpf｜margin：Q2 營收 19.2 億美元，年增 53%、季增 4%（原話："second quarter revenue of $1.92 billion, growing"）
- 2026-08-05｜Matt Stumpf｜margin：Q2 調整後 EBITDA 16.1 億美元，年增 58%，利潤率較去年同期擴張約 300bp（原話："Adjusted EBITDA was $1.61 billion, up 58% year-over-year"）
- 2026-08-05｜Matt Stumpf｜margin：季增成本上升主因為訓練與新模型開發的算力；管理層以 EBITDA 金額與自由現金流而非利潤率管理（原話："We manage this business to EBITDA dollars and free cash flow rather than"）
- 2026-08-05｜Matt Stumpf｜margin：Q2 季對季增量營收轉 EBITDA 的流入率 70%（原話："Quarter-over-quarter flow-through to adjusted"）
- 2026-08-05｜Matt Stumpf｜margin：算力口徑：每增加一美元營收約花 0.10 美元於算力，預期維持，長期可能有波動（原話："of the incremental dollar in revenue, we're spending about $0.10 on"）
- 2026-08-05｜Matt Stumpf｜margin：長期仍高度有信心 EBITDA 利潤率維持在低 80% 區間，並預告短期可能波動（原話："kind of that 80, the low 80% EBITDA margin."）
- 2026-08-05｜Matt Stumpf｜margin：Q2 自由現金流 8.63 億美元，低於正常轉換率，歸因於國際現金稅與利息支付時點（原話："Free cash flow for the quarter was $863 million."）
- 2026-08-05｜Adam Foroughi｜risk：Q2 失誤歸因於模型改善步伐低於正常，下一次升級在季末後才落地；稱無需求或競爭變化（原話："nothing we saw suggested weakening advertiser demand or a change in the competitive"）
- 2026-08-05｜Adam Foroughi｜risk：管理層承認模型提升屬研發性質，無法保證每季都有提升（原話："there's no guarantee that we're"）
- 2026-08-05｜Matt Stumpf｜risk：SEC 查詢已結束，無建議採取行動（原話："concluded its inquiry with no recommended action."）
- 2026-08-05｜Adam Foroughi｜competition：MAX 發行商收益季增雙位數，瀑布流份額維持一致（原話："MAX publisher earnings grew double digits quarter-over-quarter"）
- 2026-08-05｜Adam Foroughi｜competition：回應 Android 份額問題：Android 較競爭，因 Google 為大型競爭者（原話："the Android platform is more competitive because there's a very big competitor"）
- 2026-08-05｜Adam Foroughi｜competition：管理層稱遊戲買量並非零和市場（原話："we've proven the space is not zero-sum"）
- 2026-08-05｜Adam Foroughi｜competition：回應手遊生態健康度質疑（下載下滑、CPI 上升）：稱 CPI 上升不代表價值下降，且資料遺漏站外內購（原話："So as the cost goes"）
- 2026-08-05｜Adam Foroughi｜customer：電商/消費端廣告主支出創新高，較 Q4 2025 高 28%（原話："finishing 28% above Q4 2025 levels"）
- 2026-08-05｜Adam Foroughi｜customer：消費端目前是少數廣告主貢獻較多，焦點為中型市場品牌（原話："that few advertisers contributing more today."）
- 2026-08-05｜Adam Foroughi｜customer：消費端廣告主尚未達到支出天花板，平台被視為測試類預算（原話："We're deemed a new bucket, so a testing"）
- 2026-08-05｜Adam Foroughi｜customer：新客首年總支出 7 萬美元的指標，預期隨夥伴與中型市場策略而上升（原話："It will likely go up as we do partnership deals and target mid-market."）
- 2026-08-05｜Matt Stumpf｜customer：美國 vs 國際營收：國際近乎持平，管理層稱無重大特別原因（原話："No, nothing material."）
- 2026-08-05｜Adam Foroughi｜product：平台以原名 AppLovin Ads Manager 對外公開，並先從中型市場廣告主切入，靠夥伴關係推進（原話："AppLovin Ads Manager."）
- 2026-08-05｜Adam Foroughi｜product：創意仍是最大障礙；30–60 秒高品質影片尚無法開箱即用產出（原話："The creative is the biggest hurdle"）
- 2026-08-05｜Adam Foroughi｜product：潛在客戶開發（lead gen）業務仍在測試，無新進展（原話："Lead gen business is still work in progress."）
- 2026-08-05｜Adam Foroughi｜product：供給擴張路徑：先到非遊戲 App，再開放網路，最後 CTV；目前不具備執行條件（原話："We're just not at the point yet where we can go execute on it."）
- 2026-08-05｜Adam Foroughi｜product：合作夥伴策略：透過電商分析公司等第三方，以更精準方式引入廣告主（原話："it's a more targeted way to get the"）
- 2026-08-05｜Matt Stumpf｜capital_allocation：Q2 回購與扣繳約 114 萬股、5.51 億美元，剩餘授權約 18 億美元（原話："approximately 1.14 million shares"）
- 2026-08-05｜Matt Stumpf｜capital_allocation：回購步調較 Q1 約 10 億美元放緩，歸因於現金流較低，稱非信念改變（原話："does not indicate a change in"）
- 2026-08-05｜Matt Stumpf｜capital_allocation：期末現金 30.5 億美元、總債務 37 億美元，淨槓桿約 0.1 倍，長期預期營運於約 1 倍（原話："puts net"）
- 2026-08-05｜Adam Foroughi｜commitment：只要額外算力帶來顯著更多營收，管理層承諾繼續投入（原話："that's a trade we'll make every day."）
- 2026-08-05｜Adam Foroughi｜commitment：管理層稱 Q3 開局強勁、業務回到預期軌道並重新加速（原話："Q3 is off to a strong start, and the business is back on the"）
- 2026-08-05｜Matt Stumpf｜commitment：管理層稱只在看到增量營收時才增加支出，並說明未來若算力占比增加會溝通原因（原話："we'll communicate that and the reasons behind why we've increased compute"）
- 2026-08-05｜Adam Foroughi｜commitment：管理層不給消費端廣告主擴張到全市場的時間表（原話："We can't tell you"）

### 問答異常語氣（迴避／改口／保留）
- APP_Q2_2026_Earnings_Call_20260805.md｜問：Ralph Schackart：為何沒拿到預期的模型提升、能否診斷？｜答法：回答以「這是研發、無保證」為主，未給出具體原因診斷，也未量化 Q3 提升幅度
- APP_Q2_2026_Earnings_Call_20260805.md｜問：Omar Dessouky：開放平台約 6 週的廣告主導入表現是否符合預期、數量趨勢｜答法：未提供廣告主數量，改談中型市場焦點與長期過程，並稱無法預測何時擴大
- APP_Q2_2026_Earnings_Call_20260805.md｜問：Aaron Lee：Q3 之後算力投入是否維持墊高、能見度多高｜答法：重申每增量一美元營收約 0.10 美元算力，未給 Q3 後的具體數字，保留「長期可能有變動」

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
{"date":"20260710","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AXON 的 ROAS 優勢是合法的 AI 護城河（源自規模 + 模型飛輪），且能通過 SEC 檢驗","columns":{"2Y 驗證點":"SEC 無重大處分結案／和解；AXON 廣告 rev YoY 維持 ≥40%","5Y 驗證點":"後 ATT 世界 AXON 仍為圍牆外成效標竿","10Y 驗證點":"模型飛輪隨資料量自我強化，不依賴單一夥伴資料","具體數字門檻":"SEC 調查無 Wells Notice；AXON 廣告 rev YoY ≥40%（Q4'25 +90%、Q1'26 +59%）","信息來源":"APP Q1'26 法說（2026-05-06）；SEC 對 Bloomberg 確認 active（2026）","漂移觸發":"SEC 發 Wells Notice 單事件即觸發即時重評；AXON rev YoY 連 2 季 &lt;25%（TTM）"}},{"id":"H2","text":"e-commerce/consumer 第二曲線兌現（AXON 走出手遊）","columns":{"2Y 驗證點":"self-serve 年化 ARR ≥ $1.45B；go-live 轉換率升破 65%","5Y 驗證點":"非遊戲廣告成為營收主力之一","10Y 驗證點":"AXON 成為圍牆外電商投放預設層","具體數字門檻":"FY2026 consumer vertical 年化 ARR ≥ $1.45B；self-serve 2026-06 全球 GA（已達成）；go-live 轉換率由 ~57% 升","信息來源":"Q1'26 法說；BofA 估 e-com Q1'26 net rev ~$90M（run-rate $360M+）；管理層揭露 57% qualified→go-live","漂移觸發":"ARR 連 2 季 &lt;$300M 年化，或 go-live 轉換率連 2 季不升破 65%（新增閘，回應轉換瓶頸）"}},{"id":"H3","text":"市場在 FY2027 EPS 兌現 + SEC 陰霾散去後重新定價","columns":{"2Y 驗證點":"Fwd PE FY+2 分位回到 &gt;60%（現 ~35%）","5Y 驗證點":"估值回到與成長相稱的 25-30x","10Y 驗證點":"——","具體數字門檻":"FY2027E EPS 共識 ≥ $21.9（現 $21.93）；分析師中位目標價 $647（高 $860／低 $340，n≈36）","信息來源":"Excel buy-side snapshot 2026-06-23；yfinance 共識；MarketBeat／S&amp;P Global","漂移觸發":"FY+2 EPS 共識連 4 季偏離下修 ≥10%，或 SEC 惡化使 de-rating 固化"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"SEC 認定資料實務越界 / App Store 協議判違約——GM 88% 被重估為越界紅利","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"SEC docket、8-K 監管往來揭露、App Store 政策","警戒閾值":"Wells Notice 發出 → 連 2 季不需，單事件即減倉"}},{"id":"R2","text":"e-com 擴張因 go-live 轉換瓶頸（~57%）與競爭（Meta/Amazon/Shopify Ads）而不如預期","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"self-serve ARR、go-live 轉換率、GenAI 創意工具滲透","警戒閾值":"ARR 連 2 季 &lt;$300M 年化 或 轉換率連 2 季不升破 65%"}},{"id":"R3","text":"行動廣告 + 手遊需求週期性下行（2025 全球手遊廣告投放僅 +3%／$25B），拉低整體量能","columns":{"對應假設":"H1/H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"APP 自身 gaming 廣告 YoY、iOS 廣告收入份額（Q1'26 ~39%）","警戒閾值":"gaming 廣告 YoY 轉負且非季節性，連 3 季 → 重評 §6 成長假設"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"SEC 資料實務調查無重大處分結案／和解，或 e-com self-serve 年化 ARR 站上 $1.45B 且 go-live 轉換率升破 70%；回檔 $430-460 分批加碼","irr_base_pct":9.7,"ev5y_pct":55.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"🟢","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":4.3,"ev5y_pct":55.0,"irr_base_pct":9.7,"max_dd_pct":-60.0,"bull_5y_price":1170.0,"bear_5y_price":336.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"SEC 資料實務調查無重大處分結案／和解，或 e-com self-serve 年化 ARR 站上 $1.45B 且 go-live 轉換率升破 70%；回檔 $430-460 分批加碼","price_at_dd":520.43,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/APP_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
