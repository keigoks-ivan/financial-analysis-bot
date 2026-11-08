你是 stock-analyst **v20 判斷 agent**，標的 ABNB（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ABNB","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABNB_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABNB_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":4869,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm"}},{"id":"f_kpi1_adjusted_ebitda_airbnb_n","label":"Adjusted EBITDA（Airbnb 不報 Non-GAAP 營業利益，以此代）","value":2509,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益","value":2021,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm"}},{"id":"f_kpi5_q4_2026","label":"下一季指引：Q4 2026 營收","value":"3,220–3,280","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"百萬美元（指引區間）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm"}},{"id":"f_kpi6_nights_and_seats_booked","label":"Nights and Seats Booked","value":155.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm"}},{"id":"f_kpi7_gross_booking_value_gbv","label":"Gross Booking Value（GBV）","value":27.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"十億美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm"}},{"id":"f_kpi8_adr","label":"ADR","value":178.83,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_abnb_gross_margin_pct","label":"ABNB 毛利率","value":82.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABNB.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abnb_operating_margin_pct","label":"ABNB 營業利益率","value":20.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABNB.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abnb_fcf_margin_pct","label":"ABNB FCF 利潤率","value":36.93,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABNB.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bkng_operating_margin_pct","label":"BKNG 營業利益率","value":32.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BKNG.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bkng_fcf_margin_pct","label":"BKNG FCF 利潤率","value":32.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BKNG.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_expe_gross_margin_pct","label":"EXPE 毛利率","value":90.48,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EXPE.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_expe_operating_margin_pct","label":"EXPE 營業利益率","value":18.39,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EXPE.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_expe_fcf_margin_pct","label":"EXPE FCF 利潤率","value":23.09,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EXPE.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mar_gross_margin_pct","label":"MAR 毛利率","value":19.87,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mar_operating_margin_pct","label":"MAR 營業利益率","value":15.93,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mar_fcf_margin_pct","label":"MAR FCF 利潤率","value":12.71,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hlt_gross_margin_pct","label":"HLT 毛利率","value":30.13,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hlt_operating_margin_pct","label":"HLT 營業利益率","value":24.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hlt_fcf_margin_pct","label":"HLT FCF 利潤率","value":14.49,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":1426,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm"}},{"id":"f_kpi4_sbc","label":"股權激勵費用 SBC","value":462,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":189.99,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":34.28,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":66.21,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.3 → 5.3）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.21 → 6.21）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.38 → 7.38）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.3,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.21,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":7.38,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.19,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 5.29 → 5.3（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":35.65,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝15.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":15.3,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":8.14,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝59.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":59.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":7.41,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝45.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":45.7,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":35.85,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 5.3，分子＝快照價 189.99","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-10075.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 2515.0、現金 12590.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":596.74,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":103300.05,"period":"2026-11-08","unit":"USD m","basis":"市值 113375.05 ＋ 淨負債 -10075.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":14384.32,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（38 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":16101.96,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（41 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":7.18,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 189.99 / W52 144.48 / W104 137.21 / W250 132.7 / W250 13週斜率 0.14%"},{"id":"f_ma_w52","label":"52 週均線","value":144.48,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":137.21,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":132.7,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.14,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出競爭者含 OTA、搜尋引擎、meta-search、連鎖飯店、物業管理公司與體驗平台；並提到擁有既有消費者關係的對手可能打造「super-apps」進入旅遊市場，可能推高獲客成本；部分物業管理者鼓勵直訂繞過平台。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm","excerpt":"Competitors with established consumer relationships may leverage these to enter the travel market, creating “super-apps” that integrate multiple services, potentially increasing our customer acquisition costs and affecting our competitive position.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 稱 Airbnb 在吸引房東與房客上面臨高度競爭，房東常跨平台刊登。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm","excerpt":"Hosts have numerous options for listing their spaces, experiences, and services, both online and offline, and often cross-list their offerings.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"KeyData Q2 2026：Airbnb 在美國專業管理租屋預約占 51%、營收占 43%，高於一年前的 47%／36%；Vrbo 超過 40% 預訂來自房東出資促銷","source":"Red Awning, vacation rental channel mix 2026","url":"https://www.redawning.com/vacation-rentals/pm/post/vacation-rental-channel-mix-2026","excerpt":"According to KeyData's Q2 2026 marketplace share data for professionally managed short-term rentals, Airbnb now delivers 51% of reservations and 43% of revenue, up from 47% and 36% a year earlier.","as_of":"2026-08-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ABNB Q3 2026 Nights and Seats Booked +16% YoY to 155.0M, fastest growth in four years (Q2 2026 was +10%); GBV $27.7B +21%; full-year 2026 revenue growth outlook raised to high teens. No 2027 guidance found.","source":"247WallSt: Airbnb Q3 2026: Bookings Surge 16%, Full-Year Outlook Raised","url":"https://247wallst.com/cards/airbnb-q3-2026-earnings-abnb-01m6preqjfxp9989tfpqgtmzd5","excerpt":"growth of Nights and Seats Booked during Q3 2026 compared to Q3 2025—the highest growth we've seen in four years","as_of":"2026-11-06","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"AirDNA July 2026 midyear outlook: US short-term rental available listings growth cut from 4.6% (Dec 2025 forecast) to 2.7% for 2026, matching demand growth +2.7%, occupancy 57.4%. Local oversupply concentrated in fast-supply-growth markets (Florida beach). Source did not frame structural vs cyclical.","source":"AirDNA Midyear Outlook (July 8, 2026), via search summary","url":null,"excerpt":null,"as_of":"2026-07-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"UK short-term rental supply kept growing YoY through June 2026 while nights reserved (5.8M) were broadly flat vs 2025 and below 2024.","source":"VisitBritain / Lighthouse short-term rental report","url":"https://www.visitbritain.org/media/6058/download","excerpt":"In June 2026, 5.8 million nights were reserved in short-term rental properties, broadly in line with 2025 level but remaining below 2024.","as_of":"2026-06-30","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3 says Airbnb is party to legal proceedings and government investigations incl. competition matters, but management believes resolution of all pending matters will not have a material adverse effect; no specific antitrust case or breakup is named.","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm","excerpt":"While it is not possible to determine the outcomes, we believe based on our current knowledge that the resolution of all such pending matters will not, either individually or in the aggregate, have a material adverse effect on our business, results of operations, cash flows, or financial condition.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2025 10-K risk factors: European Commission is conducting investigations into preferential tax treatments that may change how foreign operations are taxed; could raise effective tax rate.","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm","excerpt":"The European Commission is also conducting investigations into preferential tax treatments, which may lead to changes in how our foreign operations are taxed.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"European Commission proposed Affordable Housing Act giving local authorities a clear legal basis to restrict Airbnb and other short-term rentals; needs approval of member states and Parliament.","source":"Foster Garvey, Duff on Hospitality Law: Europe moves to rein in short-term rentals","url":"https://www.foster.com/newsroom/blog/duff-on-hospitality-law/europe-moves-to-rein-in-short-term-rentals/","excerpt":"to help cities crack down on short-term rentals in stressed housing markets, and the FTC extends its comment period on personalized pricing enforcement. EU Unveils Rules to Help Cities Crack Down on Airbnbs: The European Commission has proposed the Affordable Housing Act, a new legislative framework that would give local authorities a clear legal basis for restricting Airbnb and other","as_of":"2026-09-16","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Hungarian competition authority opened proceeding against Airbnb Ireland over suspected misleading consumer information.","source":"Portfolio.hu: Hungarian competition watchdog launches investigation into Airbnb","url":"https://www.portfolio.hu/en/business/20250807/hungarian-competition-watchdog-launches-investigation-into-airbnb-778769","excerpt":"(GVH) has initiated an investigation into Airbnb Ireland over suspected unfair commercial practices and misleading information provided to Hungarian consumers on its platform. The GVH suspects that Airbnb does not properly inform and may mislead Hungarian users. As a result, the authority has launched a competition supervision proceeding against the Irish-registered company that","as_of":"2025-08-07","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"ABNB 10-K FY2025 將關稅列為影響消費者可選支出（休閒旅遊）的宏觀風險；MD&A 稱至今對業務無重大影響，未來不確定。","source":"SEC EDGAR 10-K FY2025 Item 1A / Item 7","url":"https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm","excerpt":"To date, these conditions have not had a material impact on our business, results of operations, cash flows, and financial condition; however, the impact in the future of these macroeconomic and geopolitical conditions on our business, results of operations, cash flows, and financial condition is uncertain and will depend on future developments that we may not be able to accurately predict.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"ABNB 10-K 載明須遵守 OFAC 等制裁法規，未來在主要業務地區的制裁可能對業務造成重大影響（制裁，非商品出口管制）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm","excerpt":"Future sanctions in key business areas could materially impact our business, results of operations, and financial condition.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Airbnb 以 AWS 為主要平台代管與交付基礎設施（單一雲端供應商依賴）","source":"Airbnb FY2025 10-K","url":"https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm","excerpt":"We rely primarily on Amazon Web Services in the United States and abroad to host and deliver our platform.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Airbnb 揭露系統未具完整資料儲存／處理／支付處理備援","source":"Airbnb FY2024 10-K","url":"https://www.sec.gov/Archives/edgar/data/1559720/000155972025000010/abnb-20241231.htm","excerpt":"systems currently do not provide complete redundancy of data storage or processing or payment processing","as_of":"2025-02-13","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026 Q1 財報：伊朗相關戰事壓低 EMEA 與亞太需求，預期拖累 Q2 夜數成長約 1 個百分點","source":"MarketScreener 'Airbnb flags Middle East war impact on second quarter growth'","url":"https://www.marketscreener.com/news/airbnb-flags-middle-east-war-impact-on-second-quarter-growth-ce7f5bdadb8efe25","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Nights and Seats Booked +16% YoY; GBV $27.7B +21%; ADR $179, +4%","source":"Airbnb Q3 2026 shareholder letter (8-K Ex 99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm","excerpt":"In Q3 2026, GBV was $27.7 billion and increased 21% year-over-year","as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Regional Q3 nights growth: North America low-double digit, EMEA mid-teens, APAC and LatAm over 20%","source":"Airbnb Q3 2026 shareholder letter (8-K Ex 99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm","excerpt":"In North America, we saw low-double digit growth of Nights and Seats Booked during Q3 2026 compared to Q3 2025","as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q4 2026 revenue guided $3.22-3.28B (+16-18%); FY2026 growth now high teens","source":"Airbnb Q3 2026 shareholder letter (8-K Ex 99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm","excerpt":"For full-year 2026, we now expect year-over-year revenue growth in the high teens","as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Skift Research: Airbnb platform share of online lodging rising from 26% in 2019 to 42% in 2026","source":"Skift","url":"https://newsletters.skift.com/p/bull-case-for-airbnb","excerpt":"Airbnb’s dominance as a platform is accelerating, with market share rising from 26% in 2019 to 42% in 2026, Skift Research found. The landscape is consolidating, making direct channel competition difficult for independent players.","as_of":"2026-08-25","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：Airbnb 使用第三方授權的 AI/ML 技術，其規模化採用取決於第三方軟體、基礎設施或 AI 模型的取得，公司無法控制其品質、可得性與定價；若不可用或條款不利，產品吸引力可能下降。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm","excerpt":"In addition to our proprietary technologies, we use AI and ML Technologies licensed from third parties. Our ability to continue to adopt, integrate, and use such technologies at the scale we may need may be dependent on access to specific third-party software, and infrastructure, such as processing hardware or third-party AI models, and we cannot control the quality, availability, or pricing of such third-party software and infrastructure, especially in a highly competitive environment.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Skift：Chesky 稱 ChatGPT 可作為旅遊分銷管道，但要完全繞過 OTA 『非常困難』。","source":"Skift - Airbnb's Brian Chesky: ChatGPT Can Distribute Travel, But Cutting Out OTAs Is 'Very Difficult'","url":"https://skift.com/?p=779582","excerpt":"Airbnb’s Brian Chesky: ChatGPT Can Distribute Travel, But Cutting Out OTAs Is ‘Very Difficult’ Dennis Schaal October 22nd, 2025 at 10:50 AM EDT Photo Credit: Airbnb CEO Brian Chesky Airbnb","as_of":"2025-10-22","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Skift 引 Bernstein：Airbnb 在 OTA 中最有條件應對 AI 衝擊，因直接流量占比高。","source":"Skift - Airbnb Is the 'Best-Placed' Online Travel Agency to Fend Off AI Disruption: Bernstein Report","url":"https://skift.com/2025/08/27/airbnb-is-the-best-placed-online-travel-agency-to-fend-off-ai-disruption-bernstein-report/","excerpt":"Airbnb Is the ‘Best-Placed’ Online Travel Agency to Fend Off AI Disruption: Bernstein Report Dennis Schaal August 27th, 2025 at 5:39 PM EDT Photo Credit: IPhone apps for OYO, Airbnb Trivago, Booking.com, Expedia, Agoda, Hotels.com and Hostelworld.","as_of":"2025-08-27","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Airbnb 2026 Summer Release 擴充 Services（雜貨配送、租車、機場接送、行李寄放）並新增獨立精品飯店，朝一站式旅遊平台轉型","source":"eCommerceNews: Airbnb adds car hires, hotels, World Cup experiences","url":"https://e-commerce.news/story/airbnb-adds-car-hires-hotels-world-cup-experiences","excerpt":"Airbnb has added car rentals, grocery delivery, airport pick-ups, luggage storage, boutique hotels and new app tools to its platform. The expansion also includes exclusive FIFA World Cup 2026 experiences.","as_of":"2026-05-22","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Chesky 稱 Airbnb 自有 AI 平台是對抗去中介化的最強防禦，並批評對手聊天機器人","source":"Skift: Chesky Disses Rivals' Chatbots","url":"https://skift.com/2026/02/12/chesky-disses-rivals-chatbots-calls-airbnbs-ai-impossible-to-replicate/","excerpt":"intelligence, arguing that its “intentional path” toward a native AI platform is “our strongest defense against disintermediation.” Chesky was addressing the fear AI platforms threaten Airbnb and other booking sites. And he criticized competitors who rushed to market with AI chatbots.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q1 2026 revenue guidance $2.59B–$2.63B was above ~$2.54B consensus; FY2026 guided at least low double-digit revenue growth (Feb 2026 report).","source":"TipRanks/The Fly, Airbnb sees Q4 revenue / Q1 guidance coverage (search summary)","url":"https://www.stockopedia.com/share-prices/airbnb-NSQ:ABNB/news/airbnb-apos-s-q4-revenue-rises-12-driven-by-strong-demand-019e6a0c-44c0-7390-b5c0-66cb608306b0/","excerpt":null,"as_of":"2026-02-12","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 (reported 2026-11-05): revenue $4.87B up 18.9% vs $4.75B consensus; Q4 guide revenue $3.22B–$3.28B (16–18% growth); FY2026 revenue growth outlook raised to high teens.","source":"247wallst Airbnb Q3 2026: Bookings Surge 16%, Full-Year Outlook Raised","url":"https://247wallst.com/cards/airbnb-q3-2026-earnings-abnb-01m6preqjfxp9989tfpqgtmzd5","excerpt":"Gross Booking Value jumped 21% to $27.70 billion, and that broad momentum prompted management to lift the full-year 2026 revenue growth outlook to the high teens. Revenue came in at $4.87 billion, up 18.9% year over year and ahead of the $4.75 billion consensus estimate by 2.52%.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","thesis.H","triggers"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Analyst targets: Citigroup raised ABNB target to $175 (2026-05-08); other May 2026 raises (Susquehanna $170).","source":"MarketBeat Citigroup raises Airbnb price target to $175","url":"https://www.marketbeat.com/instant-alerts/citigroup-raises-airbnb-nasdaqabnb-price-target-to-17500-2026-05-08/","excerpt":null,"as_of":"2026-05-08","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Street mean target ~$156, high $181, ratings 19 buy/4 outperform/18 hold/2 sell as of June 2026.","source":"TIKR Airbnb Stock at $135 With a $156 Street Target","url":"https://www.tikr.com/blog/airbnb-stock-at-135-with-a-156-street-target-heres-what-the-q1-beat-changes-for-investors","excerpt":"Airbnb Stock at $135 With a $156 Street Target: Here’s What the Q1 Beat Changes for Investors Gian Estrada • 7 minute read Reviewed by: David Hanson Last updated Jun 9, 2026 TIKR Key Stats for AirbnbStock 52-Week Range: $111 to $147 Current Price: $134 Street Mean Target: $156 Street High Target: $181 Analyst Consensus: 19 Buys / 4 Outperforms / 18 Holds / 2 Sells","as_of":"2026-06-09","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月8-K共7份，僅1份含重大項目（2026-03-16 Item 1.01，為25億美元優先債發行），無併購、重編、下市等項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001559720&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"10-K FY2025 Item 3：公司稱所有未決事項的結果預期不會對業務、經營結果、現金流或財務狀況造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm","excerpt":"While it is not possible to determine the outcomes, we believe based on our current knowledge that the resolution of all such pending matters will not, either individually or in the aggregate, have a material adverse effect on our business, results of operations, cash flows, or financial condition.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K清單無 Item 2.01 等併購項目；搜尋結果僅見少數股權投資（WeRoad約10%）與出售Tiqets（賣方，Expedia於2025-12-10同意收購），未見Airbnb併購公告。","source":"SEC EDGAR 8-K 申報清單；搜尋摘要（pulse.bot）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001559720&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"Heritage Foundation 等保守派股東就股東提案排除提起之訴（D. Del. 1:25-cv-00676）2026-02部分駁回，2026-07-24 Law360報導原告撤訴；非證券集體訴訟。","source":"Law360: 2 Conservative Airbnb Investors Drop Proxy Bias Suit","url":"https://www.law360.ca/real-estate-authority/residential/articles/2505552/2-conservative-airbnb-investors-drop-proxy-bias-suit","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K Item 3 稱未決訴訟合計預期無重大不利影響；風險因素僅假設性提及證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm","excerpt":"While it is not possible to determine the outcomes, we believe based on our current knowledge that the resolution of all such pending matters will not, either individually or in the aggregate, have a material adverse effect on our business, results of operations, cash flows, or financial condition.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K清單無 Item 4.02（財報不可信賴/重編）項目；搜尋亦未見SEC調查報導。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001559720&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ABNB","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":82.9,"operating_margin_pct":20.81,"fcf_margin_pct":36.93,"rd_intensity_pct":18.89},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABNB","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"BKNG","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":32.78,"fcf_margin_pct":32.84,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BKNG","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"EXPE","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":90.48,"operating_margin_pct":18.39,"fcf_margin_pct":23.09,"rd_intensity_pct":8.04},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EXPE","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"MAR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.87,"operating_margin_pct":15.93,"fcf_margin_pct":12.71,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HLT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":30.13,"operating_margin_pct":24.01,"fcf_margin_pct":14.49,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"ABNB"},"financial_history":{"ticker":"ABNB","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":8399000000.0,"revenue_yoy_pct":null,"gross_margin_pct":82.15,"operating_margin_pct":22.51,"net_income":1893000000.0,"diluted_eps":2.79,"free_cash_flow":3405000000.0,"fcf_margin_pct":40.54,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":9917000000.0,"revenue_yoy_pct":18.07,"gross_margin_pct":82.83,"operating_margin_pct":15.31,"net_income":4792000000.0,"diluted_eps":7.24,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":11102000000.0,"revenue_yoy_pct":11.95,"gross_margin_pct":83.08,"operating_margin_pct":23.0,"net_income":2648000000.0,"diluted_eps":4.11,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":12241000000.0,"revenue_yoy_pct":10.26,"gross_margin_pct":82.96,"operating_margin_pct":20.78,"net_income":2511000000.0,"diluted_eps":1.03,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ABNB/ABNB_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**Airbnb, Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Good afternoon, and thank you for joining Airbnb's Earnings Conference Call for the Third Quarter of 2026. As a reminder, this conference call is being recorded and will be available for replay from the Investor Relations section of Airbnb's website following this call.
I will now hand the call over to Andrew Slabin, Vice President of Investor Relations. Please go ahead.

**Andrew Slabin** (Executives):
Good afternoon, and welcome to Airbnb's Third Quarter of 2026 Earnings Call. Thank you for joining us today. On the call with us, we have Airbnb's Co-Founder and CEO, Brian Chesky, and our Chief Financial Officer, Ellie Mertz. Earlier today, we issued a shareholder letter with our financial results and commentary for our third quarter of 2026. These items were also posted on the Investor Relations section of Airbnb's website. During the call, we will make brief opening remarks and then spend the remainder of time on Q&A.
Before I turn it over to Brian, I'd like to remind everyone that we will be making forward-looking statements on this call that involve a number of risks and uncertainties. Actual results may differ materially from those expressed or implied in the forward-looking statements due to a variety of factors. These factors are described under forward-looking statements in our shareholder letter and in our most recent filings with the Securities and Exchange Commission.
That being said, we urge you to consider these factors and remind you that we undertake no obligation to update the information contained on this call to reflect subsequent events or circumstances. You should be aware that these statements should be considered estimates only and are not a guarantee of future performance.
Also, during this call, we will discuss some non-GAAP financial measures. We've provided reconciliations to the most directly comparable GAAP financial measures in the shareholder letter posted to our Investor Relations website. These non-GAAP measures are not intended to be a substitute for our GAAP results.
And with that, I will turn the call over to Brian.

**Brian Chesky** (Executives):
All right. Hey, everyone. Thanks for joining. When you look back at our results, over the last several quarters, there is a clear story emerging. Airbnb is back in growth mode. It's rare for a marketplace of our size to reaccelerate growth, but that's exactly what we're doing. Q3 was our fastest revenue growth in more than 3 years. Revenue grew 19% year-over-year to $4.9 billion. Gross booking value grew 21% to $27.7 billion, and Nights and Seats Booked grew 16% to 155 million.
We've also exceeded our outlook across every key metric, and we're seeing the acceleration across the business. In Q3, every region delivered double-digit nights growth. Growth accelerated in all 5 of our core markets: U.S., France, U.K., Canada and Australia, nearly all of our expansion markets. In North America, nights booked grew at our fastest pace in 4 years.
We're also seeing more guests return to Airbnb and more people try it for the first time. First-time booker growth accelerated to 13%. Now this is the highest it's been since early 2022, and the fastest-growing segment is Gen Z. Our nights booked in our app grew 29%, and now 66% of our total nights booked are in our app.
Now, I want to start by explaining what's driving this growth. This did not happen overnight. Airbnb grew incredibly fast when we started. But eventually, our technology and the way we operate couldn't keep up. So, a number of years ago, we started by rebuilding the foundation. This was immediately after our IPO. We spent years rebuilding our technology platform. We redesigned the app. We improved our core experience. And a lot of this was pretty thankless at the time because we had to trade in some near-term growth to make these very important investments. We did this for the long-term growth of the company.
And technology alone was not enough. We also had to fundamentally change how the company operates. So we organized Airbnb around a single road map, we brought all these teams together, and we focused small teams on very specific problems. Then we developed an entirely new way to build products and it was inspired by the original early days of Airbnb, my co-founders. And Project Hawaii, what I've talked about in prior earnings calls, was our first big proof point. I took a very small team. I worked with them very nearly daily. We had 1 job, make it easier to find and book a home. And this team, they worked relentlessly, and they shipped hundreds of improvements that generated hundreds of millions of dollars of revenue. And so we're like, "Wow, that works." Let's take this approach and we start applying it to other teams.
So we took this and we applied it to the pricing team, and they were able to deliver hundreds of millions of dollars in incremental revenue. Then we took it to international expansion, and we gave them more autonomy to move really quickly. And we're seeing results of that team as well. For example, in Q3, nights booked by guests in our expansion markets grew at their fastest pace in nearly 3 years. Brazil grew more than 30%, and India grew more than 60%. We also began building new businesses, including hotels and services, and we brought in experienced leaders to help scale them.
And then AI changed the speed of everything. We spent years laying the groundwork, but now AI is helping us build, test and improve products faster than we've ever done before. In Q3 alone, we shipped more than 50 products and features, nearly 70% more than a year ago because of AI. So, when you put it all together, that's what's driving our growth. We spent years changing how Airbnb operates. And now we're seeing the results.
Now, let me share a few updates in the quarter, starting with our fall update. When people book a trip, they don't just care about the home, they care about where it's located. In fact, 75% of our guests use Airbnb maps when deciding where to stay. That's why we introduced Neighborhood pages, which help guests get a better feel for an area before booking, including the best restaurants, activities, and more. Now we started these Neighborhoods pages in Paris, where we saw a really big meaningful increase in bookings. So now what we're doing is we're bringing the Neighborhood pages to over 1,500 neighborhoods around the world on Airbnb by the end of the year.
Now, this is going to be massive because when you stay in an Airbnb, you're often staying in a neighborhood and how do you get that information, it's really hard to find on Google. This is going to be really useful. We're also helping guests plan trips with recommendations from friends and family. We expanded Connections, so guests can see where people they know stayed and what they recommend. And our new travel map brings those trips and recommendations together in one place.
Now, for hosts, we designed our multi-listing calendar. It makes it easy to manage multiple listings, update pricing, and fill open nights. In its first month of early access, nearly 1 in 4 eligible hosts opted in. We're also bringing in world-class leaders to help drive our next phase of growth. In September, Pepijn Rijvers joined us as Chief Business Officer. Now, Pepijn was one of the key leaders behind Booking.com's growth. He ran its entire accommodations business, including hotels and homes and led one of the largest performance marketing operations in the world. He now leads Airbnb's homes and hotels businesses as well as our international expansion.
Now, one of the biggest opportunities ahead of us is hotels. And we started small with a pilot in just 4 cities. Today, we have thousands of boutique and independent hotels on Airbnb across more than 60 top destinations. And hotel bookings accelerated again in Q3. Now, what's even more exciting is that hotels are bringing new guests to Airbnb. In fact, approximately 35% of guests whose first booking is a hotel, they come back and they book a home within a year. The hotels aren't just a new business for Airbnb. They're also helping us grow our homes business. Services are also becoming a bigger part of Airbnb. We launched car rentals this summer, and they've quickly become one of our fastest growing services.
In Q3, we announced new services, including meal delivery, laundry, baby gear, and we also have local offerings like ski gear if you're going skiing or boat rentals, if you're near an ocean or lake. And one of our biggest untapped growth opportunities is actually partnerships. Because for nearly 18 years, partnerships really weren't a major part of how we grew. It was mostly just organic. That's changing because we partner with airlines like Delta, Qantas and TAP Air to reach millions of travelers through companies they already use.
And in October, we launched our biggest partnership ever, an exclusive partnership with American Express, bringing more than 1 million Airbnb listings to Amex Travel. Now, it's still early, but we're seeing thousands of bookings through Amex Travel with nearly 1/4 of them coming from guests who are new to Airbnb. And we're seeing higher share of Luxe bookings than we typically see on Airbnb. So of course, they're bringing in a really high-end segment of travelers that we haven't typically had as much access to.
Now I want to spend a few minutes talking about AI. I believe AI is one of the best things to ever happen to Airbnb. And I want to give you a few examples of what we're doing with it. In Q3, we brought AI into more of the guest and host experience. For guests, we introduced AI search, so they can describe what they're looking for in their own words and find the right home, service, experiences for the trip. So, if you want to see AI search, just go to our app or a website and you see at the very top of the page, there's a toggle. If you open the -- you turn the toggle on, you can basically type entire sentences like natural language, and then it will basically select all the filters. It's working really well. It's especially popular with Gen Z, and younger travelers are very AI native.
AI can also suggest relevant social search filters. It can summarize important details of homes and help guests compare places they're saving. For hosts, we're using AI to make it easier to create 3D floor plans. These are really cool. They can help you price your homes competitively and understand how the listings are performing.
Now, we're also using AI to transform customer support. Our AI assistant is now available in more than 50 languages, and this next stat is really key. In Q3, approximately 40% of all customer support issues were resolved without a human agent. And this is up from 1/3 in Q2. So this has been huge for us. And we're expanding our assistant to voice support in the U.S., so guests and hosts can help -- get faster help over the phone. What this means is that customer support cost per booking has declined more than 17% year-over-year, driven in large part by improvements to our AI assistant.
And if you're wondering, customer service NPS is as high as it's ever been. But these improvements are just the beginning. There's a lot of discussion about whether people will eventually use one AI agent to do everything. And if they do, what does that mean for Airbnb? Are we going to be cut out? Well, I don't think people are going to use one AI agent for everything. You see today's AI agents like Muse and Instinct are good at simple routine tasks like making a restaurant reservation or scheduling an appointment. But planning a trip is different. Travel is aspirational. Discovering where to go and where to stay is part of the experience.
In fact, 80% of travelers say they enjoy spending time researching trips. People want to look at photos. They want to compare homes. They want to make decisions with people they're traveling with. And I don't think the general purpose agents are the best to do that. So that is why we are building our own AI agent. And we have 3 distinct advantages when we build our own agent. First, we understand the Airbnb marketplace better than anyone. For nearly 20 years, we've helped guest or host -- and host find places to stay with -- we help guests find places to stay with millions of hosts. Every home is different. Guests care about the home, the location, the reviews and the person hosting them. And we spent years learning how guests make the decision and how hosts operate. So the understanding gives us a significant advantage in building the AI agent to help people find and book the right place to stay.
Second, we are part of the reservation itself. Now, this is important because we know that travel doesn't end with the booking. In fact, that's when it starts. Because Airbnb handles reservations, payments and customer support, our agent is able to help guests throughout their trip. This means we can manage reservations, we can help you make changes to your plans and accessing Airbnb support and protection when you need them. These are things an outside agent cannot do easily on their own.
And third, and perhaps most importantly, we're building a new interface specifically for travel. We don't think the traditional chatbot is the right way to plan travel. It's the wrong interface. So what we are doing is developing a custom-designed, AI native experience to respond to what guests are looking for. So instead of relying on traditional chat alone, which is very tech heavy, which again is definitely not the way you should plan travel, our agent draws from a library of hundreds of travel-specific interface components, maps, photos, comparisons, calendars, itineraries and compose them in real time to match what they're looking for.
This is going to feel a little bit like generative UI in the sense that it's going to offer up the right interface at the right time for your specific travel needs. Now, it's going to help guests explore options, make decisions with people they're traveling with and take action directly on Airbnb. And over time, we want our agent to help guests plan their entire trip on Airbnb all in one place. We're going to start rolling it out to guests in the first half of next year.
So, I'm going to end where I started. Airbnb is back in growth mode. We're excited about what we're building. And with the momentum we're seeing across the business, we're raising our full year outlook.
With that, I'm going to turn it over to Ellie.

**Ellie Mertz** (Executives):
Thanks, Brian, and good afternoon, everyone. I'll start with Q3 results and then cover our outlook for Q4 and the full year 2026. As Brian shared, Q3 was a strong quarter with a meaningful acceleration across the business. Gross booking value was nearly $28 billion, up 21% year-over-year, a 5 percentage point acceleration from Q2. This was driven by strong growth in Nights and Seats booked and a moderate increase in ADR. Nights and Seats booked grew 16% year-over-year, accelerating significantly from Q2, with strength across all major regions and market types.
Q3 nights benefited from a 3% net lift from the expansion of Reserve Now, Pay Later. So, excluding the impact of RNPL, Nights and Seats booked growth was approximately 13%, still accelerating from Q2. ADR was up 4% year-over-year or 5% excluding FX. It was up across all regions with notable strength in North America and Europe. On a regional basis, we saw low double-digit growth in North America, mid-teens growth in EMEA, over 20% growth in both Latin America and Asia Pacific. These results were an acceleration across all 4 regions relative to Q2.
Turning to our Q3 financial results. Revenue grew 19% year-over-year to $4.9 billion or 16% excluding FX, significantly exceeding the high end of our outlook. Net income was $1.9 billion, a 39% net income margin. Net income benefited from a $135 million reduction in our provision for income taxes as the prior year included a $213 million valuation allowance related to CAMT credits.
Adjusted EBITDA grew 22% year-over-year to $2.5 billion, representing an adjusted EBITDA margin of 52%, up from 50% in Q3 of last year. Margin expansion in Q3 was driven by strong revenue growth and cost discipline, including operating leverage from AI-driven efficiencies and customer support as well as the shifting of certain marketing expenses to Q4.
Let me take a moment on monetization and take rates. Our implied take rate was 17.6% in the quarter, down slightly year-over-year. That was primarily due to the expansion and strength of Reserve Now, Pay Later, where guests book further in advance, increasing GBV before we recognize the associated revenue and to a lesser extent, higher incentives and credits related to new business initiatives. Partially offsetting these pressures to implied take rate are guest travel insurance and our migration to the single service fee. Guest travel insurance continues to build momentum. Revenue grew nearly 70% year-over-year with higher attach rates in every region.
Lastly, in October, we completed the final phase of our fee simplification initiative, whereby nearly all of our remaining hosts have now moved to a single 15.5% service fee. We've already seen that the single service fee helps hosts price more competitively and creates greater transparency for our guests.
Next, our balance sheet and cash flow. We continue to benefit from our efficient and capital-light business model delivering $1.4 billion of free cash flow in Q3, up modestly year-over-year. We expect that free cash flow would have grown more in Q3 absent the impact of Reserve Now, Pay Later bookings on working capital. RNPL defers guest payments from the time of booking closer to the date of stay impacting the seasonality of unearned fees. Free cash flow during Q3 was also impacted by a $75 million increase in purchases of property and equipment driven by our new office building in New York City. Over the trailing 12 months, we generated $4.9 billion of free cash flow, a 35% free cash flow margin.
Finally, during Q3, we repurchased $700 million of our common stock enabled by our strong balance sheet and significant cash flow generation, leaving $2.7 billion remaining under our existing authorization. And today, we're pleased to announce Board approval of a new $12 billion share repurchase program on top of this existing authorization. This reflects the continued confidence in our business performance, our ability to generate strong free cash flow as well as our commitment to returning capital to shareholders, which remains a core component of our capital allocation strategy.
Now let's turn to Q4 and full year 2026 outlook. We're encouraged by the meaningful acceleration we've delivered as well as the momentum we're seeing into year-end. Although we're closely monitoring ongoing developments in Europe, underlying global travel demand remains healthy and our faster pace of product innovation continues to drive results and our Q4 outlook reflects it. For Q4, we expect revenue of $3.22 billion to $3.28 billion, representing year-over-year growth of 16% to 18%. This includes an approximate 2 percentage point FX tailwind after factoring in our hedging program.
We expect our implied take rate to be up slightly year-over-year. We expect GBV growth in the mid-teens, driven by at least low double-digit growth in Nights and Seats booked and a modest increase in ADR.
In Q4, we are not assuming a material persistent impact related to the unrest in Europe, specifically France or the conflict in the Middle East, but are closely monitoring trends in both regions. On profitability, we expect adjusted EBITDA to increase year-over-year and adjusted EBITDA margin to be slightly down compared to Q4 2025, partially due to the timing of marketing spend noted earlier.
Now for the full year, once again, we're raising our revenue and adjusted EBITDA margin outlook despite facing more difficult comparisons as we head into Q4. We now expect year-over-year revenue growth in the high teens up from at least mid-teens last quarter and our expectation at the beginning of the year of low double-digit growth. And we now expect full year adjusted EBITDA margin of approximately 36%, up from at least 35.5% last quarter.
During 2026, due to the expansion of Reserve Now, Pay Later and its impact on the timing of working capital, we expect full year adjusted EBITDA margin to be modestly above our free cash flow margin. To close, Q3 demonstrates that the product and business changes we've made are translating into real financial outcomes, faster growth and expanding margins. We're encouraged by the progress we've made so far and the durability of our results. Lastly, our product road map is robust and gives us a clear path to driving growth into the future.
With that, I will open it up to Q&A.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Richard Clarke from Bernstein.

**Richard Clarke** (Analysts):
I guess, firstly, on dynamic pricing. I guess in Q2, Brian, you said you thought dynamic pricing was a bigger opportunity than Reserve Now, Pay Later. You've been out with that product for about a month now, just early learnings, what's the sign-up you're getting from hosts? And do you still stick with that? And just very quickly, Ellie, I think you said take rate up in Q4, why the reversal there? Is that because you're now lapping Reserve Now, Pay Later? Or is there any other initiatives that are adding to the take rate in the fourth quarter?

**Brian Chesky** (Executives):
Richard, so, I'll take the first part. So yes, I think -- well, I think generally, pricing is probably one of the biggest levers we have, certainly dynamic pricing. Just to give you a quick anecdote. A couple of months ago, we hired Pepijn Rijvers from Booking. He's our new Chief Booking (sic) [ Business ] Officer. And he was really instrumental in the early days of Booking. And one of the things he said when he joined, he said, if you think Reserve Now, Pay Later is big. Wait till you see what we can do with pricing. It's many Reserve Now, Pay Laters. And it actually kind of makes sense. If you sell a product, customers care about 2 things: how good is the product and what is the cost? So it's really 50% of the buying equation and affordability is just a fortunate point for Airbnb because we have a lot of young travelers. It's much more economic to stay in a home. We're very much Gen Z based. We don't have any data to share today about dynamic pricing, but the adoption is really great.
I think one of the things we've noticed, this is a really key point is that, there is this win-win where dynamic pricing can generally lower prices across the marketplace. It still allows hosts to make more money. So some nights, they make more money, other nights they make less. What we were really able to find these sensitivities where if you just charge like $10 less, you'll make enough more bookings that you'll actually make a lot more in the long run because your occupancy is much higher and that is like not an intuitive thing and it's good for the guests because it makes them a little more affordable.
And so it's a really huge lever. It's extremely early. This is something that like AI is really good at tuning. And the thing about AI is like you need to tune it and get more data. So I think in the coming quarters, we should be able to have some more results. But again, I'll just kind of summarize by saying pricing is a massive lever and actually dynamic pricing is one of many things we're doing around pricing.

**Ellie Mertz** (Executives):
Great. And Richard, to answer your take rate question, I guess, about Q4, just to double click on Q3 to explain the changing dynamic from quarter to quarter, in Q3, we got an outsized impact of Reserve Now, Pay Later on the gross booking value in quarter, whereas, obviously, the revenue from those bookings is delayed. And so in Q3, you see the impact of Reserve Now, Pay Later increases the denominator, bringing down the implied take rate. That's somewhat reversed, versus in Q4, you should expect a modest increase in implied take rate.
More broadly, I would say from quarter-to-quarter, there are some small timing movements that do impact take rate. But I wanted to call out that the single service fee, as well as guest insurance, should provide over a longer time period, a modest increase in terms of the overall take rate.

**Operator** (Operator):
Your next question comes from the line of Lloyd Walmsley from Mizuho.

**Lloyd Walmsley** (Analysts):
A couple, if I can. First, just on the hotel effort. Can you kind of give us an update of how growth here is performing relative to the core, maybe or any other helpful quantification? And sort of where do you think this could be over the next few years as a tailwind?
And then second one, I appreciate all the color about agents in the shareholder letter. Very helpful. Curious, Brian, do you sort of see a path to your agent helping customers with travel sort of beyond the walls of Airbnb? Or do you think it's more limited to taking action and sort of managing services that you all provide yourself? Like how do you see that evolving over time? I know it's early, but curious to get your vision on that as well.

**Brian Chesky** (Executives):
Yes. Okay. So hotels and agents beyond the walls of Airbnb. Hotels are growing markedly faster than our core business. That's not to say our core business is growing slow. It's just hotels are a $900 billion market off of a very, very tiny base. I certainly don't want to put any like projections out there or forecast. But it's undoubtable that we will do multiple billions of dollars in revenue in hotels in the coming years. And we don't even need to like win this market to be a significant player and make billions of dollars.
And part of the reason why is we have a huge amount of traffic. Most people come to Airbnb are looking for a place to stay. If somebody doesn't find a place on Airbnb, they're probably going to another app or a website booking a hotel. So, we don't have to win. We just have to get the people in our store to buy something before they leave. And they know -- we know they want something, they're in the store in the first place.
And the other thing is we're seeing -- this next thing was very surprising to me. Airbnb, when we started Airbnb, I was a little ideologically like not -- I was kind of against hotels. Let's be honest. My first tagline was forget hotels. And so, we had a little animosity with the hotel industry, like in 2010, 2011, 2012, over the last 6, 7 years, I really changed my tune and approach. I'd like to think of this as growing up a little bit and being practical. And our guests told us, "Hey, we love hotels. We booked hotels right before the pandemic." But we really decided to get serious about hotels a couple of years ago. And basically, one of the things we learned is that actually most people like staying in homes and hotels, it just depends on the type of trip. And that we don't have a campaign about why people stay in a home, but if you're booking last minute for business travel, one night, hotels are really great. So we expect people to want to book hotels.
The thing I wasn't expecting was the reception from the hotel industry. And it was a complete 180. And I think hotels suddenly saw Airbnb as a major ally. They really love the way they were merchandised. They love the fact that we were entirely new audience. We were disproportionately Gen Z. We are not just really affordable travel. We're actually really high-end travel because we have really big villas. We are a much more global audience and they just liked the fact that there was this whole another channel.
So all that is to say, when we got really serious about hotels, it's not the only reason I hired Pepijn Rijvers, but it was definitely a big thing. I told Pepijn, this is a major opportunity for Airbnb. And it is going to be huge. And by the way, Pepijn Rijvers ran the largest marketing organization ever at Booking.com. Now, I don't think performance marketing is a very important part of our core business, but I think with hotels, it's a commodity.
I think we're going to be able to do performance really efficiently because hotels are so high ADR, Booking.com shows it's very profitable. But the best thing is we don't need to do a lot of it because we have so much organic traffic already coming in. So all of which to say it's going to generate many billions of dollars of revenue. I don't know what the time line is, but it's a huge opportunity.
With regard to agents going outside the wall of Airbnb, yes, of course. We are going to be -- that will be through MCPs. We're going to be integrating a number of MCPs with our trip agent in the first half next year. I won't give away too much more. We like to do these product launches. We don't want to build a general agent. Just to double click for 1 second. The problem -- if I just want to double click for a second, 1 problem with a general agent is you have to create like a general interface because the agent has to be able to do everything. So the general interface generally becomes almost entirely text based, right? Because you can ask about travel, medical information, deliveries. You can't know what they're going to ask.
As you get more specialized, you can develop a really custom interface that is perfectly bespoke for that type of use case. So with travel, we're able to design these really custom components. If you want a car rental, the agent generates this little UI of a car and it's like beautifully in like a custom-generated interface. If you want to invite co-travelers, the agent helps you.
So there's going to be, I think, an incredible user interface experience that what I would describe as a kind of post-chat-based interface. It's going to have a chat element to it. And so that's what we're going to be doing. It will be able to go outside the walls, certainly, but it's going to stay within travel and expect in the first half of next year.

**Operator** (Operator):
Your next question comes from the line of Ken Gawrelski from Wells Fargo.

**Kenneth Gawrelski** (Analysts):
I appreciate it. Brian, I appreciate the commentary and the prepared remarks in the shareholder letter around the agent launch. Could you talk a little bit more -- and you just kind of elaborated that it actually could leave the walls of Airbnb, can you talk about -- are you talking about actually direct -- maybe direct integrations with airlines and et cetera, to kind of complete the full trip?
Because I guess the question is for a vertical agent, if you don't have all supply, you don't have all attractions, you don't have all hotels, how do you think about the trade-offs for the customer between that horizontal general purpose agent, which may not be ideal for travel, but at least it sees everything? That's question one. 
And two, the second one, please. if you don't mind, could you just -- and I apologize if I may have missed some of this. But could you talk a little bit just about the -- what you're seeing with RNPL as you continue to expand there? Could you give us some confidence around cancellation rates and anything new you might be seeing there?

**Brian Chesky** (Executives):
All right. Yes, I'll do the AI agent, and I'll hand over to Ellie for Reserve Now, Pay Later. So the short answer is, yes, we are going to do integrations with a lot of providers. I don't want to give away too much again about our kind of product road map but I think it's safe to say we're going to do every part of travel. There's not 1 part of travel that we're not eventually going to do.
And every part of travel will have MCPs. We will have APIs. And eventually, we do anticipate all bookings going through the app for every vertical in travel. I don't want to put a time line on it. Just to give you an example, like say car rental. Right now, car rentals is done through a partnership called CarTrawler and it's what we call link-off. So it's an API that says a link-off. The next phase is to do the reservation booking directly on Airbnb. And so that's what we're doing with a number of these partnerships. So the kind of way we're going to do a lot of these partnerships is to get mass scale. We're kind of doing like link-off. The link-offs appear to feel like Airbnb.
So it's really in a -- like a web view that's designed in our custom interface with groceries. This is with luggage storage. This is a car rental. And over time, we're going to develop a much more native booking integration. And obviously, the good of that is it's a little more seamless. You take a little bit greater part of the revenue, but you also have to handle customer service. So you got to be sure you're ready for that.
Now, the great thing about the link-off is we can kind of decide and test what things we want to integrate when. But the end game is yes. The end game is eventually, we'd like all travel to be able to book natively through the app of Airbnb, but we're not going to put a time line on it. And then the other part of your question was general versus horizontal, right? Okay. So with regards to general versus horizontal and trade-offs, I mean, listen, there is going to be a reason for general agents. I'm not saying that there won't be general agents, but I want to just give my view. 
I don't think -- I think a lot of people are looking at general chat agents like and they're trying to connect it to Google. Like there was 1 home page of the Internet. It was called Google and you went there and everything started at Google. This is just my opinion. I do not think that's going to happen with chatbots. I don't think there will be 1 chatbot that's like Google in the front page, and it is the orchestra conductor for every other app. I'll tell you a couple of reasons why that I don't think that will happen.
The first problem is if that were to exist, I think it would have to exist at the operating system level or exist at the Android operating system level, at the Mac iOS operating system level. The operating system is the right substrate to control your apps because one app was the home page. You're really saying an app is going to control all the other apps.
By the way, do you really think Apple is going to allow an app to control their entire computer? So we're considering all the potential issues for privacy and security and that they can actually cut out of their own like user experience. I'm actually quite skeptical of that. So I do think that general chat agents are going to be successful and popular. I just don't think they're going to be able to do everything.
And the burden of a general chat agent doing everything is they basically almost become an operating system. That is a lot to put into an app, and I just don't think that's going to happen. So I do think general chat agents will be popular for single everyday things. I think as they get really, really complicated, specialization is going to win. Now, the chat agent can hand over to a specialized agent, but a lot of people are going to go direct to the specialized agent, just like they discover Airbnb on Google, and they come back direct. They don't just keep going through Google. That is generally my thought.
Now, a general agent does have a bunch of data because you use the general agent more frequently, right? At the same time, we can connect MCPs of Gmail and Google Calendar. If you connect an MCP of Google Calendar and Gmail or other MCPs, we can actually pull in what the users consent to, and a ton of other data. So actually, there's many ways we can get as much data or nearly as much data as a chat agent uses every day. And this is just through basic MCP handoffs.
So I think basically, the way to think about it is in order for specialization to win, it must not be 20% better. It must be like 2, 3, 5x better than a general agent at its task because you do have the inertia and the switching costs. So our job isn't to be 20% better, it's to be multiples better. And that's the bar I'm holding the team to. We'll see if we can get there, but I'm pretty confident.

**Ellie Mertz** (Executives):
Great. Ken, let me tell you just a little bit more about what we're seeing on Reserve Now, Pay Later. Just as a reminder, Reserve Now, Pay Later, we began to launch a year ago in the U.S. We expanded amongst our flexible or moderate cancellation policy listings at the beginning of the year to rest of world. And then most recently, at the beginning of Q3, we expanded eligibility of Reserve Now, Pay Later to limited and firm cancellation policies.
In doing so, it obviously grew materially the total eligibility of GBV on the platform for this product. As of Q3, it was over 40% of GBV was eligible to use RNPL. In doing that expansion, we've seen a couple of things. First is a material lift to bookings. In particular, in Q3, we saw a full 3 points of net night lift associated with both the expansion and the [indiscernible] eligibility offering. This was an incremental point or more relative to the impact we saw in Q2. Candidly, that the expansion in the summer was even better than we had tested in terms of the reception for consumers. I think, it's probably pretty obvious, but this product make traveling more affordable, no need to pay upfront. And what we see is that people not only book more, they book earlier, so our lead times have expanded and they book more expensive listings, which is one of the reasons that ADR is up. Specific to your question, cancellation rates in aggregate are up 200 to 300 basis points from a year ago. And this is -- if you think about the nominal levels a year ago, our cancellation rates were order of magnitude about 16%. They're now about 19%, which we think is very healthy in the travel space.
The final comment I will make, and I'm sure we'll get questions on it later, is impact of RNPL in Q4. I just want to remind everyone that we had called out last quarter that Q3 would be the peak in terms of net impact of RNPL on our numbers. That's because we get the growth benefit in terms of the lift of bookings before we see the full cancellations. And so the net impact to nights booked will come down sequentially in Q4.

**Operator** (Operator):
Your next question comes from the line of Justin Post from Bank of America.

**Justin Post** (Analysts):
Maybe one for Brian and a quick one for Ellie. Can you remind us what percent of your inventory is really proprietary for Airbnb? And how have you thought about using that as an asset, maybe with agent negotiations? How do you really take advantage of that. And then Ellie, just quick on the insurance. Can you give us anything on what the penetration is of bookings? Or how much is contributing to take rates?

**Brian Chesky** (Executives):
Yes. Over 60% of our inventory, we believe, is exclusive to Airbnb. And -- so that's the first part of the question. What's the other part of your question? It's the penetration of insurance products?

**Ellie Mertz** (Executives):
Yes. Insurance products are growing quite nicely. It's a single-digit percent of bookings that have an attach that is up materially from a year ago. I think what's exciting on our insurance products is not only the growth, but also the opportunity to provide more insurance products. We're looking across a host of offerings that we could provide both guests and hosts and I should note that the margins are great on the attach insurance product.

**Brian Chesky** (Executives):
Sorry, Justin, you said how does that factor into agent negotiations, exclusive inventory. Can you elaborate on that?

**Justin Post** (Analysts):
Yes. How are you thinking about that as an asset, either for your own internal agents or maybe in negotiations with external agents getting good financial terms? Or any strategic advantages there? Yes.

**Brian Chesky** (Executives):
I'm not sure yet. I mean I think it's really -- I think as far as speculating what the relationship is between unique inventory and like potentially leverage, negotiating with like other partners. I think it's really early. I don't know. But let me just tell you my philosophy on unique inventory. I don't pay a lot of attention looking at what percent of our inventory is unique anymore. It's helpful. The more unique to better. There's no question.
The most important thing is as we go into categories, we are -- our philosophy is it's okay to have commodities, like hotels. It's okay to have some cross-listed home as long as there are a lot of unique things that you can't get anywhere else. And I think the percentage is not as important. It's the absolute amount, right? So like if there -- imagine there are 2 stores, they all have the same products except 1 store has a bunch of other stuff that other store doesn't have.
The percentage of unique stuff in that store doesn't matter, just how many things, the items are unique in that store, the other store didn't have. And so as a theoretical mental model, imagine there's 2 stores and one, they have almost all the same inventory, but 1 has just some more unique stuff. If you have 10% more unique stuff, you might get more than 10% more traffic because suddenly, it's a major difference. So we don't really look at the percent mix. I mean it's good to know. 
Of course, we track it, but we are growing really, really quickly. by process of inventory and getting that really competitive nice. And actually, one of the things you notice about Reserve Now, Pay Later, is it helped us become way more competitive like getting those nights than the host-only fee has been really competitive with us keeping more competitive prices. And so why I say this is just to finish off this point.
With services, a bunch of our inventory is commodity inventory, like car rentals. You can get those cars elsewhere. But then we have a bunch of inventory you can't find anywhere else, like masseuses, chefs and photographers. With experiences, we're now offering ticket. You can get bunch of those tickets on their website, but we also have exclusive experiences. So kind of category by category, we'll get a bunch of the commodities. We always want to make sure that we have a unique stuff. And we have unique plus commodities, then we become the one-stop shop. You don't need to go anywhere else.

**Operator** (Operator):
Your next question comes from the line of Benjamin Black from Deutsche Bank.

**Benjamin Black** (Analysts):
Great. So Brian, it seems that you're increasingly adding social and travel discovery elements through Connections, through Travel Map, through Neighborhood pages, even personalized recommendations. So how do these features change the role you guys play before guest has actually chose the destination or before they're ready to book? And could greater discovery eventually lead -- discovery element eventually lead to sort of a more natural opportunity for sponsored listings? And then secondly, as you add hotels, you expand a number of experiences, you add services, how does that change your thinking around loyalty more broadly?

**Brian Chesky** (Executives):
Two good questions. So social and travel discovery, let me just like before I answer the question, let me back up. So I remember like 22 years ago when Facebook first came out, it came out in 2004. I couldn't use it right away because I just missed it. I just graduated from college right before Facebook launched in my college, I had to wait 2 years before they open up to everyone. So I remember Facebook would used to be a social network. And with basically your friends and you can keep in touch with people and you can message them and see what they were doing. And that was around 2004 to 2006, 2007, 2008, let's call that the golden age of social networking.
And at some point, social networking morphed into social media. And our friends became our followers, and we stopped connecting and we started performing. And a very bizarre phenomenon happened where the social network in a sense was invented in kind of for a large part of the world, uninvented, like I no longer have a social graph. I no longer know whose birthdays my friends are unless they're close friends. I no longer know when somebody -- like something happens in someone's life, I no longer know how to keep a touch with people, except I just got to message them in WebChat or my messaging platform.
So there really aren't social graphs anymore. I mean, LinkedIn is kind of a resume graph, but really, there's no social grafts anymore. And we thought what if we brought back the social graph, but instead of being an online social graph, it was a social graph in the real world of the people you travel with and the people you meet along the way of your travels. And we thought this could be really interesting.
So we started building these social travel features this year. We launched them in May. We launched a travel map and we started realizing this might be the beginning of something massive. And we are going to be launching a lot more social features and social connected features next year. I think this is maybe one of the single most underestimated parts of our business.
I mean, it might be because we don't talk about them much. But that's okay. I don't want to give away too much of the road map, but I can just say a couple of things. Number one, it's a great proxy for trust. If I were a host, and I were to get a reservation for somebody, I don't know them, but I can see how they're connected to me, how many degrees away, that would be a really good proxy for trust. And as you build this social graph, you increase trust, as you increase trust you potentially go into a lot of the businesses. I'll let your imagination run wild what's possible.
You can also see where your friends have traveled and stayed. So you can see like my friends stayed in Paris, now I can message them and ask what's good to do in Paris. I can eventually -- we can eventually bring that into search results. Right now, that's on the profile tab, but we eventually are going to bring that into search results. So when you see the map, you'll be able to see where your friends have traveled in search results in map. You'll be able to see listings your friends have stayed. You'll be able to see who's been traveling there recently and where they're going. So there's going to be a lot of these features.
These features are going to, a, make things more sticky; b, it's going to make group travel much more collaborative; c, it's going to make it much easier to get great recommendations that's going to increase trust in the platform. And the other thing I'll just say the last thing is, I've been doing -- I occasionally do these roundtables and -- with customers. And I recently did a Gen Z roundtable, basically kids that are like college age. And they were kind of like a little younger than the age I was when I started Airbnb. And I heard 2 things from Gen Z. And again, I'd just say Gen Z is like the fastest-growing segment, and it's the prime advertising segment.
They basically said 2 things. One, they want to save money. Young people always want to save money, but in age of rising cost of living, with a lot of college debt, with tuition going up, and the ladder being pulled up a little bit with AI, a lot of entry-level jobs are harder to come by because AI can do them more than ever, they're looking for affordability.
But even more so, we're hearing a lot of college and recent grads saying they want to meet people. And a lot of people, they meet people at work, in school, church, bowling alleys. Well, a lot of these things aren't around as much anymore. And a lot of kids if they don't have a job, they're not going to meet someone at work. So we're starting to see that a lot of these social features are going to be especially popular with Gen Z. 
But surprisingly, we're also seeing like on the other barbell empty nester. Kids are out of the house. They want to travel. They want to meet people. So there's a lot of opportunities here with the social features. With regards to sponsor listing, the relationship between them, I don't know. I think the thing I'll say about sponsor listings in particular is we are developing our AI agent, and we wanted -- we are developing sponsor listings, but they'll be developed in the context of the AI agent. So we first need to launch the AI agent. We need to refine it, and then we figure out how ads work in that new world.
By the way, everyone's figuring this out. ChatGPT is figuring this out. So I don't think it's a clear -- it's not clear what the implementation is. But I think if anyone can figure out, I think our design team could. With regards to a loyalty program, I mean, I don't -- again, I want to not break any news, but we are absolutely looking at a loyalty program.
We've been looking at it for a long time. I think I've said for a long time, the best loyalty program is plus customers loving your product. Disney and Apple for years. Well, Apple doesn't have a loyalty program. People love their products. But at the same time, we're like the only travel -- major traveler in the world that doesn't have one.
And I think we have been at a disadvantage because we don't have a loyalty program. A lot of people who want to use Airbnb say, "I want to use you, but you don't have a program. So I almost feel like I can't use you." So we are absolutely looking at a loyalty program. I don't have anything to announce, but I can say that as we add more verticals, we just have a lot more to work with. So adding verticals make loyalty program more compelling.

**Operator** (Operator):
Your next question comes from the line of Jed Kelly from Oppenheimer.

**Jed Kelly** (Analysts):
Just looking at the guidance, it looks like your EBITDA margins are going to be in that 36% range, so above 35%. But if I look at your growth, you're growing 12%. I think, Brian, knowing you, you like faster growth. So can you just talk about how we should think about threading the needle between double-digit room night growth and maintaining margins above 35%, 36%?

**Ellie Mertz** (Executives):
Jed, are you talking about Q4 or '27, what's the reference?

**Jed Kelly** (Analysts):
Just balancing profit versus growth given that you're seeing accelerating growth and what your preference is?

**Ellie Mertz** (Executives):
Yes. Yes. I mean I think Brian and I have been very clear over the last 2 years that we have very been prioritizing growth focused on driving growth in this business. And I think the results in the last couple of quarters show that we have been able to deliver that growth. Behind that, we continue to invest in growth. But at the same time, in the last couple of years, what you've seen is that we've been capable of reinvesting upside in order to continue the momentum.
We're obviously in the '27 planning right now. And the prioritization around continuing this momentum continues to be the top priority. The good news is that this business is extremely profitable, has incredible cash flow dynamics that give us a lot of room to invest within a very strong profitability envelope.

**Operator** (Operator):
Your next question comes from the line of Matthew Cost from Morgan Stanley.

**Matthew Cost** (Analysts):
I guess, firstly, on the hotels and the people that are using the hotel product, are they generally new to Airbnb and bringing in incremental bookings? Are they a high-end or low-end consumer? How are they retaining? I guess, tell us a little bit more about the behavior of those people that are booking hotels.
And then secondly, Brian, I was wondering if you could just respond to some of the data that's out there about early adoption of these agents that's showing agents like Muse and Instinct that's showing that a lot of commercial activity happening there is travel related. Is that something you think strengthen the mix over time? Or how does that gel with your overall view of how people will use these horizontal tools?

**Brian Chesky** (Executives):
Maybe I'll start with the second one and just what's top of mind and then Ellie, you can go to the first one. So we're not seeing a lot of traffic in even fewer bookings from Muse and Instinct, yet. We do have nearly 0.5 million bookings a day and a very nonmaterial number of bookings happen on Muse and Instinct. So we're talking very low numbers. So we're not seeing a lot of traffic today and it's not really increased over the last 4 weeks.
So it kind of peaked in early October. It's kind of been stable in the last 4 weeks. So we're kind of watching it. My general philosophy on agents are, I'm generally excited about them. I don't see them as a threat. I see them kind of like Google as an opportunity for more people to discover Airbnb. So I think they'll be great handoff to us. There will be people that will want to book a one-off flight or something directly on an agent.
So I'm not saying that will never happen. But travel is -- maybe this is like just a framework to think about. There's item-based retailers and project-based retailers. So just as an analogy, you go to Walgreens. You don't go -- you don't like plan to go to Walgreens. You need to get something, you go to Walgreens. You go to IKEA or Home Depot, that's a project-based retailer, right? You have a whole project. You don't go to those places to get one item.
Airbnb, we're really long term, we want to be in the midst of the entire trip. That's entire project. It involves where to stay, what to do, how to get there all in one place. It's highly logistical. Our guests typically travel in groups of 3 or more. 90% of people message the host. The host wants to know who's in their home, so they want to have a connection. They don't want to offload it to an agent. If I'm hosting somebody, I want to talk to the person, not the agent on behalf of the person. It's very visual.
People typically look at multiple -- dozen listings or more. They look at 25 photos per listing often. So it's very visual. It's very collaborative. It's a very complicated experience. And the other thing I mentioned this in my opening remarks, is there's a lot of studies that show people enjoy anticipating travel more than actually traveling.
Here's a fun fact. Most of our traffic happens during 9 to 5 hours. These people are supposed to be working. And they're not. We have evidence. People are actually secretly using Airbnb. Maybe they're trying to skip their job. But the idea is that it's highly aspirational. So I don't think a lot of people want to offload all that to an agent. I think they want to offload things they don't enjoy not the things they do enjoy. So it's small.
We're watching it, but we are definitely open to working with these agents. But I also just think they'll be really helpful handoffs to us. But I think that to do -- I'm not saying agents can't do travel, I just think it to focus on travel, and that's what we're going to do. We're going to focus on travel. And anyone who focus on travel can probably solve it, but a general agent trying to solve travel and solve 50 other things. That's really hard.

**Ellie Mertz** (Executives):
Turning to the hotel questions, I'll be quick, I know we're running on time. In terms of the mix of new bookers versus past bookers, it's actually very consistent with our overall platform. We're seeing great demand from both segments. And just to underscore why like that is consistent with our strategy. We're eager to get more travel share from our past guests and hotel spoken up new use cases that even our most loyal guests may be choosing hotels off the platform.
Similarly, on the first-time booker front, hotels part of the strategy was to onboard those guests that haven't yet tried us for a home by offering them something they are familiar with, and we're seeing that as well. So great hotel demand on both sides of the marketplace.

**Operator** (Operator):
And we have reached the end of our question-and-answer period. I will now turn the call back over to Brian Chesky for some final closing remarks.

**Brian Chesky** (Executives):
All right. Well, thank you, everyone, for joining. I just want to end where I started. Airbnb is back in growth mode and it's here to stay. This is a result of years of hard work to make Airbnb better. And as we build Airbnb to become an AI native company, I actually think the opportunity ahead of us is actually even bigger. I want to end most importantly, by thanking our incredible team. I get to -- we get to take the credit when we have good calls, but it's only because of the great work of the people.
And I think one of the superpowers of Airbnb, maybe the Superpower, this is old cliche, it's all about the people. But it really is, especially in Silicon Valley and tech because you're only as good as your most recent innovations, and that's only as good as our team. Our team tirelessly. They've been really, really burning the midnight oil a lot of times this year.
And so I'm asked why are we growing so fast. I often say things like execution. Well, execution only happens from people, teams. And I think that what these results really are beyond AI, beyond all these products, is this is a team that's really starting to get into flow. They're doing great. So thank you all, team Airbnb. And thank you all for dialing in today. We are just getting started, back in growth mode. Thank you.

**Operator** (Operator):
This concludes today's conference call. Thank you for your participation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ABNB_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：Q3 營收財測區間（原話："revenue of $4.69 billion to $4.77 billion"）
- 2026-08-06｜CFO｜guidance：Q3 營收含約 3 個百分點匯率順風（原話："approximate 3 percentage point foreign exchange tailwind"）
- 2026-08-06｜CFO｜guidance：Q3 GBV 年增預期為中段十幾%（原話："We expect year-over-year GBV growth to be in the mid-teens"）
- 2026-08-06｜CFO｜guidance：Q3 財測未假設中東衝突有重大影響（原話："not assuming any significant impact related to the conflict"）
- 2026-08-06｜CFO｜guidance：Q3 調整後 EBITDA 利潤率預期略低於去年同期（原話："margin to be down slightly compared to Q3 2025"）
- 2026-08-06｜CFO｜guidance：全年營收成長上修至至少中段十幾%（原話："revenue growth to improve to at least mid-teens"）
- 2026-08-06｜CFO｜guidance：全年調整後 EBITDA 利潤率上修至至少 35.5%（原話："adjusted EBITDA margin to be at least 35.5%, up from 35%."）
- 2026-08-06｜CFO｜guidance：全年隱含 take rate 預期與 2025 大致持平（原話："our implied take rate to be relatively flat compared to 2025"）
- 2026-08-06｜CFO｜guidance：管理層說若無新業務客戶誘因 take rate 會略高（原話："our implied take rate to be slightly higher during the year"）
- 2026-08-06｜CFO｜guidance：管理層強調下半年較高基期下仍上修全年財測（原話："Even against tougher comps in the back half of the year"）
- 2026-08-06｜CFO｜margin：Q2 調整後 EBITDA 利潤率 35%（原話："an adjusted EBITDA margin of 35%"）
- 2026-08-06｜CFO｜margin：利潤率擴張來源之一：營運支援與產品開發效率（原話："cost efficiencies in operations and support"）
- 2026-08-06｜CFO｜margin：Q2 淨利含 $77 百萬稅務利益（原話："million tax benefit recorded in the current period"）
- 2026-08-06｜CFO｜margin：更新後財測假設全年 AI 支出大幅增加，同時利潤率擴張（原話："increase in terms of the AI spend over the course"）
- 2026-08-06｜CFO｜margin：CFO 稱在吸收 AI 成本下仍擴張利潤率（原話："expanding margins while absorbing that increased cost."）
- 2026-08-06｜CEO｜margin：客服每筆訂單成本年減約 16%（原話："support cost per booking declined about 16% year-over-year"）
- 2026-08-06｜CFO｜margin：CFO 稱不需像過去般增加人力（原話："need to grow our headcount at levels that we did in the past"）
- 2026-08-06｜CFO｜margin：FCF 數字口徑：近 12 個月 $4.8B（原話："generated $4.8 billion of free cash flow"）
- 2026-08-06｜CFO｜margin：未攤銷費用受 Reserve Now Pay Later 遞延影響的口徑（原話："unearned fees would have grown year-over-year in Q2"）
- 2026-08-06｜CFO｜margin：Reserve Now Pay Later 占 Q2 GBV 逾 20%（原話："over 20% of our total"）
- 2026-08-06｜CFO｜commitment：不給 2027 年以後的具體財測（原話："not going to give you a specific guide for '27 and beyond."）
- 2026-08-06｜CFO｜commitment：CFO 稱未來會尋求同樣的成長加利潤率擴張（原話："As we look forward, we're going to seek to do the same."）
- 2026-08-06｜CFO｜commitment：CFO 稱利潤率有相對下限、有機會就加碼投資（原話："floor in our ability to continue to invest against that."）
- 2026-08-06｜CFO｜commitment：單一服務費預計年底前完成推廣（原話："which we expect to be completed by year-end"）
- 2026-08-06｜CEO｜commitment：CEO 稱 AI 搜尋本月開始小流量測試（原話："We are beginning to put it in test this month."）
- 2026-08-06｜CEO｜commitment：AI 語音客服今年稍後推出（原話："Later this year, we will begin introducing AI voice support"）
- 2026-08-06｜CEO｜commitment：CEO 稱未來 1.5 年內可用 Airbnb 規劃完整行程（原話："you will absolutely be able to get to Airbnb"）
- 2026-08-06｜CEO｜commitment：CEO 稱對飯店要加大投入（原話："stepping on the gas given the reception"）
- 2026-08-06｜CEO｜commitment：CEO 稱未來一年聚焦旅遊一站式（原話："focused on the travel phase"）
- 2026-08-06｜CFO｜capital_allocation：Q2 回購 $1.1B（原話："we purchased $1.1 billion of our common stock"）
- 2026-08-06｜CFO｜capital_allocation：回購是資本配置核心之一（原話："Returning capital to shareholders remains a core component"）
- 2026-08-06｜CEO｜capital_allocation：併購策略維持機會主義，偏好自建（原話："our bias is always to grow organically"）
- 2026-08-06｜CEO｜capital_allocation：CEO 稱不需大額資本支出，推論成本相對 ROI 很小（原話："kind of de minimis relative to the ROI"）
- 2026-08-06｜CEO｜capital_allocation：CEO 稱不做 token maxing（原話："token maxing"）
- 2026-08-06｜CEO｜competition：CEO 稱表現優於最大同業（原話："we're outperforming our largest peers in travel"）
- 2026-08-06｜CEO｜competition：CEO 稱 CarTrawler 被 Expedia 收購不影響合作與併購策略（原話："I do not think this has"）
- 2026-08-06｜CEO｜competition：CEO 稱不做白標業務（原話："the white label business"）
- 2026-08-06｜CEO｜risk：CEO 稱 AI 是公司唯一的生存風險（原話："was the only existential risk to this company"）
- 2026-08-06｜CEO｜risk：CEO 稱政策是風險但非生存風險（原話："Now policy is a risk, but it's not an existential risk."）
- 2026-08-06｜CFO｜risk：CFO 稱中東衝突對業務影響低於預期（原話："from the conflict was less than we had anticipated"）
- 2026-08-06｜CEO｜product：CEO 稱飯店進展顯著優於預期（原話："going significantly better than I expected"）
- 2026-08-06｜CEO｜product：飯店夜數成長約為住宅 3 倍（原話："growing approximately 3x faster than our homes business."）
- 2026-08-06｜CEO｜product：首次訂飯店客人約 35% 回來訂住宅（原話："Roughly 35% of first-time hotel guests returned to Airbnb"）
- 2026-08-06｜CFO｜product：飯店供給擴至前 20 城並強調選擇性（原話："supply acquisition efforts to a top 20 number of cities"）
- 2026-08-06｜CFO｜product：飯店篩選標準：增益而非與住宅競爭（原話："inventory that can be accretive to the platform"）
- 2026-08-06｜CEO｜product：AI 搜尋預設仍是原搜尋，需數月重新訓練用戶（原話："months and months to retrain the customer"）
- 2026-08-06｜CEO｜product：CEO 稱定價是最大成長槓桿之一，遠大於 RNPL（原話："one of the biggest single levers for growth that we have"）
- 2026-08-06｜CEO｜product：CEO 稱體驗業務擴到數千市場不是今年（原話："and that's not this year"）
- 2026-08-06｜CEO｜product：CEO 稱租車會是最大的服務品類（原話："car rentals is going to be the biggest one by far"）
- 2026-08-06｜CEO｜product：服務多為夥伴模式，管理層稱成本不高（原話："there'll be much cost because they're partnerships"）
- 2026-08-06｜CEO｜product：CEO 稱 AI 是 Airbnb 發生過最好的事（原話："AI is the best thing to ever happen to Airbnb."）
- 2026-08-06｜CEO｜product：概念到上線時間最多縮短 60%（原話："reduced the time from concept to launch by as much as 60%"）
- 2026-08-06｜CFO｜product：CFO 稱 ADR 中臥室夜數成長是可持續的組成（原話："that component of ADR appreciation that is durable"）
- 2026-08-06｜CEO｜customer：首次訂房者成長加速至 11%（原話："growth among our first-time bookers accelerated to 11%"）
- 2026-08-06｜CEO｜customer：App 訂房夜數年增 23%（原話："Nights booked on our app grew 23% year-over-year"）
- 2026-08-06｜CEO｜customer：美法英澳核心市場成長加速（原話："the U.S., France, U.K. and Australia, all"）
- 2026-08-06｜CEO｜customer：AI 客服約 45% 問題無需真人（原話："Nearly 45% of issues that start with our AI assistant"）
- 2026-08-06｜CEO｜customer：CEO 稱成長可持續而非一次性（原話："This is durable growth."）
- 2026-08-06｜CEO｜customer：CEO 稱動能將延續到未來幾季（原話："we believe that momentum will continue through the"）
- 2026-08-06｜CFO｜competition：CFO 稱單一服務費對價格有下壓效果以維持競爭力（原話："has a kind of downward pressure on pricing"）

### 問答異常語氣（迴避／改口／保留）
- ABNB_Q2_2026_Earnings_Call_20260806.md｜問：Jed Kelly：單一服務費是否推廣到所有房東｜答法：CFO 答覆說年底前整個供給基礎都會用單一服務費；與稿中準備發言「大多數剩餘房東」口徑不同
- ABNB_Q2_2026_Earnings_Call_20260806.md｜問：Eric Sheridan：長期增量利潤率與再投資比例｜答法：CFO 明講不給 2027 年以後財測，改談過往紀錄與「相對下限」，未給數字
- ABNB_Q2_2026_Earnings_Call_20260806.md｜問：Lloyd Walmsley／Justin Post：飯店在哪些市場轉換率改善、規模與時間表｜答法：管理層以「單位數占比、成長 3 倍」等定性回答，未提供轉換率或市場別數字

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
{"date":"20260703","verdict":"進場","role":"條件式核心持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"核心 STR 市集成長維持雙位數、市佔續穩／擴大（網路效應不逆轉）","columns":{"2Y 驗證點":"Nights YoY ≥7%、GBV YoY ≥12%","5Y 驗證點":"營收 CAGR ≥12%、全球 STR 市佔 ≥44%","10Y 驗證點":"核心 GBV 仍為公司主體、市佔未被 Booking 反超","數字門檻":"Nights ≥7% YoY；全球 STR 市佔 ≥44%","來源":"公司 Q1'26 股東信、AirDNA/Yahoo Finance 市佔","漂移觸發":"Nights 連 2 季 &lt;5% → 削弱"}},{"id":"H2","text":"AI-native 直訂 app 抵禦 agentic AI 分發，take rate 不被結構性侵蝕","columns":{"2Y 驗證點":"Direct/app 訂房占比不降、take rate ≥12.5%","5Y 驗證點":"take rate ≥13%、ABNB 為旅客旅宿搜尋的獨立入口而非被比價後端","10Y 驗證點":"Airbnb 在 agentic 時代仍是「品牌直達」而非通用分發下游","數字門檻":"take rate ≥12.5%；直訂占比不連 2 季降","來源":"Chesky 法說（AI-native 策略）、Skift、OpenAI 撤 Buy Now（2026-03）","漂移觸發":"take rate 連 4 季 &lt;12.5% → 削弱（5Y 假設）"}},{"id":"H3","text":"Services＋Experiences 第二曲線兌現，佔營收由 ~1–2% 升至 ~10%","columns":{"2Y 驗證點":"Services/Experiences 顯性化為財報揭露項、flywheel 續存","5Y 驗證點":"Services＋Experiences 營收 ≥$2.5B（FY30）、佔比 ~10%","10Y 驗證點":"第二曲線成為第二成長引擎、Adj EBITDA margin 維持 ≥35%","數字門檻":"FY27 ≥$500M；FY30 ≥$2.5B；EBITDA margin ≥35%","來源":"2026 Summer Release、公司揭露（1/3 experience bookers 90 天內訂住宿）","漂移觸發":"跨 2 年度營收佔比停滯 &lt;3% → 反轉（10Y 假設）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"短租監管系統性擴散：EU Reg 2024/1028（2026-05-20 全歐生效）＋ 各州登記/資料揭露常態化，抽走頂級城市高 ADR 供給","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"都會區合規房源數、都會 GBV 占比、被下架房源規模","警戒閾值":"都會 GBV 占比連 2 年下滑 ＋ 供給淨減"}},{"id":"R2","text":"agentic AI 分發繞道：Google AI Mode partner 名單排除 ABNB，旅遊搜尋預設導向 6 家對手，直訂流量被抽","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4–6 季）","監測指標":"Direct/app 訂房占比、take rate、付費行銷占營收比","警戒閾值":"直訂占比連 2 季降 ＋ 行銷/營收比升 &gt;2pp"}},{"id":"R3","text":"第二曲線擴不起來：Services/Experiences 重蹈 2019 覆轍，佔比長期卡在個位數，24.6x fwd PE 的期權價值蒸發","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Services＋Experiences 營收與佔比、flywheel（experience→stay 轉換）","警戒閾值":"跨 2 年度營收佔比停滯 &lt;3%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":9.2,"ev5y_pct":55.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"條件式核心持倉","signal":"B","val":"🟡","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":5.0,"ev5y_pct":55.0,"irr_base_pct":9.2,"max_dd_pct":-55.0,"bull_5y_price":335.0,"bear_5y_price":104.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":null,"price_at_dd":148.93,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABNB_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
