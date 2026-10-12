你是 stock-analyst **v20 判斷 agent**，標的 LEVI（20261012）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"LEVI","date":"2026-10-12","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEVI_20261012/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEVI_20261012/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_revenues_gaap","label":"Net revenues (GAAP)","value":1609.7,"period":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","unit":"US$M（YoY +4.3% 報告、+4.5% 有機；去年同期 1,543.4）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm"}},{"id":"f_kpi1_adjusted_ebit","label":"Adjusted EBIT","value":248.7,"period":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","unit":"US$M（利益率 15.5%，去年同期 11.8%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm"}},{"id":"f_kpi2_gaap_operating_income","label":"GAAP operating income","value":222.3,"period":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","unit":"US$M（利益率 13.8%，去年同期 10.8%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm"}},{"id":"f_kpi3_gross_margin","label":"Gross margin","value":66.2,"period":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","unit":"%（YoY +450bps，去年同期 61.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm"}},{"id":"f_kpi4_adjusted_diluted_eps","label":"Adjusted diluted EPS","value":0.48,"period":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","unit":"US$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm"},"note":"consensus 0.36（來源：EarningsWhispers，非 IR；僅供參考）"},{"id":"f_kpi5_adjusted_free_cash_flow","label":"Adjusted free cash flow","value":44.3,"period":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","unit":"US$M（去年同期 -39.4；年初至今 427.3）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm"}},{"id":"f_kpi6_stock_based_compensation","label":"Stock-based compensation（年初至今 9 個月）","value":58.8,"period":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","unit":"US$M（新聞稿未揭露單季，亦未直接給占營業利益％）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm"}},{"id":"f_kpi7_inventories","label":"Inventories","value":1253.6,"period":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","unit":"US$M（YoY -3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm"}},{"id":"f_kpi8_fy2026_guidance_2026_10_","label":"FY2026 guidance（2026-10-07 更新）","value":"報告營收 ~+7.0%；有機 ~+6.0%；毛利率 +130bps；adj EBIT margin ~12.1%；稅率 ~23%；adj EPS 1.54–1.56","period":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）","citation":"公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-07","period":"2026-10-07","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-07"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_levi_gross_margin_pct","label":"LEVI 毛利率","value":61.72,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEVI.gross_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_levi_operating_margin_pct","label":"LEVI 營業利益率","value":11.06,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEVI.operating_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_levi_fcf_margin_pct","label":"LEVI FCF 利潤率","value":8.46,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEVI.fcf_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ktb_gross_margin_pct","label":"KTB 毛利率","value":48.24,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KTB.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ktb_operating_margin_pct","label":"KTB 營業利益率","value":12.03,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KTB.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ktb_fcf_margin_pct","label":"KTB FCF 利潤率","value":13.6,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KTB.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pvh_gross_margin_pct","label":"PVH 毛利率","value":58.78,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PVH.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pvh_operating_margin_pct","label":"PVH 營業利益率","value":8.05,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PVH.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pvh_fcf_margin_pct","label":"PVH FCF 利潤率","value":8.01,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PVH.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gap_gross_margin_pct","label":"GAP 毛利率","value":43.26,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GAP.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gap_operating_margin_pct","label":"GAP 營業利益率","value":10.99,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GAP.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gap_fcf_margin_pct","label":"GAP FCF 利潤率","value":6.24,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GAP.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rl_gross_margin_pct","label":"RL 毛利率","value":70.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RL.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rl_operating_margin_pct","label":"RL 營業利益率","value":16.42,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RL.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rl_fcf_margin_pct","label":"RL FCF 利潤率","value":11.99,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RL.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":18.7,"period":"2026-10-09（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-16.76,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":30.69,"period":"2026-10-09（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.54 → 1.54）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.71 → 1.71）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.98 → 1.98）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.54,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":1.71,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":1.98,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 1.54 → 1.54（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":12.3,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝6.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":6.7,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.07,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝18.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":18.8,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.31,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝9.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":9.6,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":12.14,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 1.54，分子＝快照價 18.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":3.102,"period":"2026-10-12","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-12"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#none","axis":"competitive_share_entrants","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K：前十大批發客戶占淨營收 24%（FY2024 25%、FY2023 27%），占比逐年下降；未見最大客戶導入第二供應商或自製的揭露。","source":"Levi Strauss & Co Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/94845/000009484526000008/lvis-20251130.htm","excerpt":"Sales to our top ten wholesale customers accounted for 24%, 25% and 27% of our total net revenues in fiscal years 2025, 2024 and 2023, respectively.","as_of":"2026-01-31","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2024 10-K：公司已開始整併合約製造商數量（供應端集中度風險，非客戶端 second-source）。","source":"Levi Strauss & Co Form 10-K FY2024","url":"https://www.sec.gov/Archives/edgar/data/94845/000009484525000005/lvis-20241201.htm","excerpt":"it has begun consolidating the number of contract manufacturers from which we source our products","as_of":"2025-01-31","retrieved_at":"20261012","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2022 10-K：前十大批發客戶合計約占 2022 淨營收 31%（2021 年 32%、2020 年 29%），無單一客戶達 10%。","source":"LEVI STRAUSS & CO - Form 10-K - FY2022 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/94845/000009484523000006/lvis-20221127.htm","excerpt":"No single customer represented 10% or more of our net revenues in any of these years.","as_of":"2023-01-01","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2015 10-K 風險因素：與批發客戶無長期合約、採逐單採購；主要批發客戶破產或財務惡化可能造成營收重大損失。","source":"LEVI STRAUSS & CO - Form 10-K - FY2015 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0000094845/000009484516000047/a2015yeform10-k.htm","excerpt":"While we have long-standing relationships with our wholesale customers, we do not have long-term contracts with them. As a result, purchases generally occur on an order-by-order basis","as_of":"2016-01-01","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"LEVI FY2026 Q3（季末2026-08-30）淨營收約$16億，報告基準+4%、有機+5%；亞洲區域成長最強、美國報告基準-1%；DTC +2%，CEO稱DTC未達內部預期；公司上調全年獲利指引。","source":"FashionUnited: Levi Strauss reports Q3 net revenue growth of 4 percent, raises outlook","url":"https://fashionunited.com/news/business/levi-strauss-reports-q3-net-revenue-growth-of-4-percent-raises-outlook/2026100875090","excerpt":null,"as_of":"2026-10-08","retrieved_at":"20261012","affects":["moat_trend","thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"LEVI Q3 淨利$168.6M，含IEEPA關稅退款利益$78.6M；公司計畫$100M加速庫藏股，並將多數關稅退款利益再投入Q3/Q4業務。","source":"LEVI Form 8-K Exhibit 99.1 3Q2026 press release / RTTNews","url":"https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm","excerpt":null,"as_of":"2026-10-08","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"丹寧產業產能：印度丹寧產能擴張超越國內市場成長，形成約20–25%的暫時性過剩（來源文章未標日期，非2026數據）；另USTR於2026-03啟動Section 301「結構性過剩產能」調查（製造業整體，非丹寧專屬）。","source":"Retail4Growth: Denim makers face price, capacity pressure amidst continued glut；shenglufashion FASH455 (June 2026)","url":"https://retail4growth.com/news/denim-makers-face-price-capacity-pressure-amidst-continued-glut-806","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"全球丹寧市場2024年底約$867億，預估2030年達$1,217.6億；棉價世銀預期2027年再升至$1.8/kg（市調報告，非共識預測）。","source":"Modaes: denim market to grow 42% by 2030 with cotton on the rise","url":"https://www.modaes.com/global/markets/goodbye-leggings-hello-jeans-denim-market-to-grow-42-by-2030-with-cotton-on-the-rise","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"FY2026 10-Q：美國最高法院 2026-02-20 裁定 IEEPA 關稅無效；美國政府 2026-07-23 宣布依 Section 301 的新關稅；Q3 記錄 IEEPA 關稅退款 $78.6M。","source":"LEVI STRAUSS & CO Form 10-Q FY2026 (period ending 2026-08-30)","url":"https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000047/lvis-20260830.htm","excerpt":"On February 20, 2026 a U.S. Supreme Court ruling invalidated the tariffs imposed by the U.S. government under the International Emergency Economic Powers Act; the U.S. government announced on July 23, 2026, new tariffs under Section 301 of the Trade Act of 1974.","as_of":"2026-10-01","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-Q：多數產品產地（孟加拉、柬埔寨、巴基斯坦、越南）曾受被廢除的 IEEPA 關稅，且受新的預期關稅約束。","source":"LEVI STRAUSS & CO Form 10-Q FY2026","url":"https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000047/lvis-20260830.htm","excerpt":"many of our products are produced in countries, such as Bangladesh, Cambodia, Pakistan, and Vietnam, that were subject to the invalidated U.S. IEEPA tariffs, and are subject to the new prospective tariffs.","as_of":"2026-10-01","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Q3 營收約 +4%，關稅退款推升毛利率；全年調整後 EPS 預期上調，約 $60M 退款再投入業務。","source":"Hargreaves Lansdown / just-style: Levi Strauss lifts annual forecasts as strong demand cushions tariff hit","url":"https://www.hl.co.uk/news/levi-strauss-lifts-annual-forecasts-as-strong-demand-cushions-tariff-hit","excerpt":"The revised guidance factors in the impact of IEEPA tariff refunds, with approximately $60m set to be redeployed into the business.","as_of":"2026-10-01","retrieved_at":"20261012","affects":["valuation","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"中國占 Levi's 服裝產量約 1%（2018 年為 15%），主要產地為巴基斯坦、孟加拉、印尼等。","source":"Apparel Insider: Levi's to slash China sourcing amid trade war","url":"https://apparelinsider.com/levis-to-slash-china-sourcing-amid-trade-war/","excerpt":"It adjusted its set-up in response to the tariffs and the share that China now has of its garment production is approximately 1%.","as_of":"2025-01-01","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"產業面：2026-02 IEEPA 被推翻後改為暫時性 10% Section 122 關稅（至 2026-07-24），其後 Section 301 新關稅（10%–12.5%、逾 80 國）自 2026-07-24 起；單一倡議團體來源，需對照官方公告。","source":"Business & Human Rights Resource Centre: tracking the impact of forced labour tariffs on apparel footwear supply chains","url":"https://www.bhrrc.org/zh-hant/最新消息/tracking-the-impact-of-forced-labour-tariffs-on-apparel-footwear-supply-chains/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"LEVI FY2025 10-K：由約32國獨立代工廠供貨，單一國家占比不超過30%（無單一國家集中）","source":"LEVI STRAUSS & CO Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/94845/000009484526000008/lvis-20251130.htm","excerpt":"In fiscal year 2025, we sourced products from independent contract manufacturers located in approximately 32 countries around the world, with no more than 30% sourced from any single country.","as_of":"2025-11-30","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"二手來源稱 LEVI 對美進口直接來自中國僅約1%、墨西哥約5%（2025年1月高管說法），生產轉往越南、墨西哥等；屬二手轉述，未讀原文","source":"Yahoo Finance / Simply Wall St 轉載（搜尋摘要）","url":"https://finance.yahoo.com/news/levi-navigates-trump-tariffs-agile-141609234.html","excerpt":null,"as_of":"2025-01-31","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"二手來源稱主要供應商國家含孟加拉、柬埔寨、埃及、巴基斯坦、斯里蘭卡、越南，2025年4月受10–49%對等關稅；第三方估年化關稅成本$25–30M（非公司數字）","source":"Simply Wall St narrative（搜尋摘要）","url":"https://www.simplywall.st/narratives/ivd0ffpq-tariffs-and-global-risks-will-limit-margins-yet-spark-change","excerpt":null,"as_of":"2025-04-02","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"產業層：2026年7月24日起美國對孟加拉、印度、巴基斯坦、柬埔寨等適用10%、越南與中國12.5%（Section 301關稅，據textalks）；Dhaka Tribune 給出不同有效稅率（孟25.6%、中35.6%、越28.1%），兩源口徑不一；越南占美國服飾進口22.2%（2026前五月）","source":"textalks.com / Dhaka Tribune（搜尋摘要，貿易媒體）","url":"https://textalks.com/us-tariffs-give-bangladesh-a-new-apparel-edge-over-vietnam-and-china/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261012","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 FY2026（至2026-05-31）淨營收約$1.6B，報告+8%、有機+6%；Americas +9%（有機+7%，美國+5%）、Europe +4%（有機-1%，歸因配送中心轉換造成出貨時點移位）、Asia +10%（有機+12%）。","source":"Levi Strauss & Co. Reports Second Quarter Results (Business Wire)","url":"https://secure.businesswire.com/news/home/20260708278591/en/Levi-Strauss-Co.-Reports-Second-Quarter-Results","excerpt":null,"as_of":"2026-07-08","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 FY2026 通路：DTC 報告+11%、有機+8%，占淨營收51%；批發報告+5%、有機+3%。毛利率62.7%，來自較低產品成本與調價，關稅與匯率為逆風。","source":"Levi Strauss & Co. Reports Second Quarter Results (Business Wire)","url":"https://secure.businesswire.com/news/home/20260708278591/en/Levi-Strauss-Co.-Reports-Second-Quarter-Results","excerpt":null,"as_of":"2026-07-08","retrieved_at":"20261012","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"女裝Q2營收+11%，管理層稱男女裝市占皆擴大；高端丹寧（約$300 Blue Tab）CFO稱在高端丹寧類別市占僅0.4%；未找到女裝專屬市占數字。","source":"Levi Strauss Q2 2026 earnings call (earningswhispers transcript / textalks summary)","url":"https://textalks.com/?p=84329","excerpt":null,"as_of":"2026-07-09","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 營收成長指引上調至7%–7.5%（原5.5%–6.5%）；CEO稱類別預期至2030年每年中個位數成長。","source":"Levi Strauss raises 2026 outlook as premium denim and DTC sales lift growth (textalks)","url":"https://textalks.com/?p=84329","excerpt":null,"as_of":"2026-07-09","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"第三方丹寧市場規模預估分歧（全球2026約USD91.4B、CAGR 5.48%；另一來源USD103.16B），多數來源為低至中個位數成長；美國消費者為較弱環節。","source":"Research and Markets / Fortune Business Insights（搜尋摘要彙整）","url":"https://www.researchandmarkets.com/report/jeans","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#none","axis":"substitute_technology","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"FY2026 Q3：DTC 淨營收僅 +2%（報告與有機），占總營收 45%，管理層稱 DTC 低於內部預期，預期 Q4 中個位數成長；e-commerce +10%","source":"Levi Strauss & Co. Reports Third-Quarter Results (Business Wire/Morningstar, 2026-10-07)","url":"https://www.morningstar.com/news/business-wire/20261007513688/levi-strauss-co-reports-third-quarter-results","excerpt":"DTC net revenues increased 2% on a reported and organic basis. DTC comprised 45% of total net revenues in the third quarter.","as_of":"2026-10-07","retrieved_at":"20261012","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q1 FY2026：DTC 占總淨營收 52%，DTC 成長為成長引擎；同時批發也成長（Q2 10-Q 稱批發量增）","source":"FashionUnited, DTC surge drives Levi Strauss to raise annual guidance","url":"https://fashionunited.com/news/business/dtc-surge-drives-levi-strauss-to-raise-annual-guidance/2026040871618","excerpt":"DTC net revenues rose 16 percent on a reported basis, now accounting for 52 percent of total net revenues for the quarter.","as_of":"2026-04-08","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 FY2026 10-Q：批發淨營收在三個月與六個月期間皆成長（報告與有機），主因量增；歐洲量減係因上年德國 Dorsten 配送中心轉換後出貨正常化","source":"Levi Strauss 10-Q for quarter ended 2026-05-31","url":"https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000037/lvis-20260531.htm","excerpt":"net revenues in our wholesale channel increased for the three-month and six-month periods ended May 31, 2026 compared with the prior-year periods on a reported and organic net revenues basis primarily due to higher volumes","as_of":"2026-07-01","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-07 Q2 後 FY26 調整後 EPS 指引上調至 $1.46–$1.52（前 $1.42–$1.48），營收 $6.72–6.75B；中點 $1.49 略低於當時共識 $1.51","source":"Benzinga earnings forecasts（經搜尋摘要）","url":"https://www.benzinga.com/quote/LEVI/earnings-forecasts","excerpt":null,"as_of":"2026-07-08","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026 年已兩度上調指引（Q1 四月、Q2 七月），未見下調；兩次均假設美國對中國關稅 30%、其他地區 20%，且未計關稅減免/退款","source":"edgar.tools / FashionUnited / Yahoo Finance 摘要","url":"https://finance.yahoo.com/markets/stocks/articles/levi-strauss-raises-fy26-outlook-135221339.html","excerpt":null,"as_of":"2026-07-08","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價分布：StockAnalysis 15 位平均 $28.2；Investing.com 12 位平均 28.27、高 34 低 25；Benzinga 19 位平均 $26、高 $34、低 $14（Morgan Stanley）；來源間時點不一致","source":"StockAnalysis / Investing.com / Benzinga（搜尋摘要）","url":"https://stockanalysis.com/stocks/LEVI","excerpt":null,"as_of":"2026-09-11","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Wells Fargo 於 2026-07-28 降評至 Hold、目標價 $25；Barclays 目標價 $27（自 $26）維持 Overweight；JPMorgan Overweight（目標價 $33 或 $34，來源不一）","source":"Benzinga sentiment / StockAnalysis（搜尋摘要）","url":"https://www.benzinga.com/quote/LEVI/sentiment","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Levi's 出售 Dockers 品牌予 Authentic Brands Group：2025-05-20 宣布，初始 $311M、盈利支付最高 $391M；美加部分 2025 年完成，國際部分 2026-02-27 最終交割；約 $100M 淨收益用於加速股票回購。","source":"FashionUnited: Levi Strauss completes sale of Dockers brand to Authentic","url":"https://fashionunited.com/news/business/levi-strauss-completes-sale-of-dockers-brand-to-authentic/2026030971023","excerpt":"The final closing happened on February 27, 2026, following an agreement first announced on May 20, 2025","as_of":"2026-03-09","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Dockers 剝離予 Authentic Brands Group，2026-02-27 最終交割（Levi's 為賣方，非收購方）；初始 $311M，盈利支付最高 $391M。","source":"FashionUnited: Levi Strauss completes sale of Dockers brand to Authentic","url":"https://fashionunited.com/news/business/levi-strauss-completes-sale-of-dockers-brand-to-authentic/2026030971023","excerpt":"The final closing happened on February 27, 2026, following an agreement first announced on May 20, 2025","as_of":"2026-03-09","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"LEVI","period":"TTM ending 2026-05-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":61.72,"operating_margin_pct":11.06,"fcf_margin_pct":8.46,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEVI","as_of":"TTM ending 2026-05-31（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"KTB","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":48.24,"operating_margin_pct":12.03,"fcf_margin_pct":13.6,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KTB","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PVH","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":58.78,"operating_margin_pct":8.05,"fcf_margin_pct":8.01,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PVH","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"GAP","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":43.26,"operating_margin_pct":10.99,"fcf_margin_pct":6.24,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GAP","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"RL","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":70.27,"operating_margin_pct":16.42,"fcf_margin_pct":11.99,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RL","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"LEVI"},"financial_history":{"ticker":"LEVI","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-11-30","revenue":6168600000.0,"revenue_yoy_pct":null,"gross_margin_pct":57.53,"operating_margin_pct":10.82,"net_income":569100000.0,"diluted_eps":1.41,"free_cash_flow":-39000000.0,"fcf_margin_pct":-0.63,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-11-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-11-30","revenue":5842100000.0,"revenue_yoy_pct":-5.29,"gross_margin_pct":57.53,"operating_margin_pct":7.96,"net_income":249600000.0,"diluted_eps":0.62,"free_cash_flow":121900000.0,"fcf_margin_pct":2.09,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-11-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-11-30","revenue":6032000000.0,"revenue_yoy_pct":3.25,"gross_margin_pct":60.63,"operating_margin_pct":9.37,"net_income":210600000.0,"diluted_eps":0.52,"free_cash_flow":670900000.0,"fcf_margin_pct":11.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-11-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-11-30","revenue":6282000000.0,"revenue_yoy_pct":4.14,"gross_margin_pct":61.73,"operating_margin_pct":11.22,"net_income":578100000.0,"diluted_eps":1.45,"free_cash_flow":308200000.0,"fcf_margin_pct":4.91,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-11-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/LEVI/LEVI_Q3_2026_Earnings_Call_20261007.md）

# Q3 2026 Earnings Call
**Levi Strauss & Co.** | Earnings Calls | 2026-10-07

**Operator** (Operator):
Good day, ladies and gentlemen, and welcome to the Levi Strauss & Company Third Quarter Fiscal 2026 Earnings Conference Call for the period ending August 30, 2026. [Operator Instructions] This conference call is being recorded and may not be reproduced in whole or in part without written permission from the company. This conference call is being broadcast over the internet and a replay of the webcast will be accessible for one quarter on the company's website, levistrauss.com.  
I would now like to turn the call over to Aida Orphan, Vice President of Investor Relations at Levi Strauss & Co.

**Aida Orphan** (Executives):
Thank you for joining us on the call today to discuss the results for our third quarter of fiscal 2026. Joining me on today's call are Michelle Gass, our President and CEO; and Harmit Singh, our Chief Financial and Growth Officer.
We'd like to remind you that we will be making forward-looking statements based on current expectations, and those statements are subject to certain risks and uncertainties that could cause actual results to differ materially. These risks and uncertainties are detailed in our reports filed with the SEC. We assume no obligation to update any of these forward-looking statements.
Additionally, during this call, we will discuss certain non-GAAP financial measures, which are not intended to be a substitute for our GAAP results. Definitions of these measures and reconciliations to their most comparable GAAP measure are included in our earnings release available on the IR section of our website, investors.levistrauss.com.
Please note that Michelle and Harmit will be referencing organic net revenues or constant currency numbers, unless otherwise noted, and the information provided is based on continuing operations.
Finally, this call is being webcast on our IR website, and a replay of this call will be available on the website shortly. Today's call is scheduled for 1 hour, so please limit yourself to one question at a time to allow others to have their questions addressed.
And now I'd like to turn the call over to Michelle.

**Michelle Gass** (Executives):
Welcome, everyone, and thank you for joining us. Over the past several years, we have transformed Levi Strauss & Co. into a more diversified, higher-growth company. We have sharpened our focus on the areas where we see the greatest opportunities to win, expanded internationally, built a more balanced DTC and wholesale model and evolved Levi's from a denim bottoms business into a leading global denim lifestyle company.
While we delivered strong results across much of the business, our DTC performance fell short of our expectations during the quarter. As we'll discuss on the call, we have a clear understanding of what worked and what did not, and we have already taken targeted actions to improve performance.
Before I turn to our Q3 results, I'd like to take a moment to speak to the CFO appointment we announced last week. I'm delighted to share that we have named John Vandemore as the company's next CFO. John brings more than 2 decades of financial leadership experience across global consumer businesses, most recently serving as CFO of Skechers, where he helped support its growth into one of the world's largest footwear brands. He is a proven operator with deep financial expertise, a track record of driving profitable growth and margin expansion and strongly aligns with our strategy, brand and culture.
I also want to take this opportunity to thank Harmit for his leadership and dedication over the past 14 years. He has played an important role in transforming LS&Co. into a more direct-to-consumer, diversified and profitable company. Harmit has been a trusted partner to me and to our leadership team, and I'm grateful for his many contributions to the company.
Now turning to Q3. As a reminder, all numbers Harmit and I will reference are on an organic basis. The quarter again demonstrated the benefits of our diversified portfolio and reinforce our confidence that we have the right strategies in place to drive sustainable, long-term profitable growth. We delivered another quarter of mid-single-digit growth, up 5% on an organic basis. And year-to-date, our business is up 7% versus the prior year.
Our international business grew 8% this quarter, led by Asia, which has been a consistent source of strength throughout the year and delivered another quarter of double-digit growth, while profitability continues to improve as the business scales. Global Wholesale continued its strong momentum, up 6% with growth across all segments. And our strategy to expand beyond denim continues to deliver results.
Categories outside our Levi's denim bottoms business accounted for approximately 50% of our top line growth in the quarter, driven in part by accelerating momentum in tops, which grew 7%. That said, DTC performance in the quarter fell short of our expectations, driven primarily by softer traffic trends in both the U.S. and Europe.
In Europe, unseasonably warm weather across several key markets weighed on traffic for much of the quarter. As temperatures normalized, traffic and sales trends improved meaningfully, and those improvements continued into Q4 quarter-to-date.
In the U.S., while our marketing continued to generate strong consumer engagement and reinforce brand heat, we had fewer major brand-building moments than a year ago. In addition, our back-to-school campaign did not drive the level of traffic and demand we had anticipated.
Importantly, we moved quickly to address these U.S. traffic challenges and have a clear plan to improve performance. We are increasing investment behind areas of strong consumer demand, particularly low-rise fits and strengthening inventory positions accordingly. We are deepening our marketing investments, creating a stronger cadence of traffic-driving moments and placing greater emphasis on mid-funnel product marketing.
We are strengthening commercial execution across our stores and digital channels with a sharpened focus on conversion and other key productivity metrics. Since implementing these actions, we have seen positive trends in our U.S. direct-to-consumer business. Combined with the continued improvement in Europe, this gives us confidence that DTC will return to at least mid-single-digit growth in the fourth quarter and deliver high single-digit growth for the full year.
To support these efforts and fuel growth, we are redeploying a substantial majority of the tariff refunds we recorded in the third quarter back into the business across both Q3 and Q4. In addition to increased marketing investments, we are putting those funds to work behind sharper value for consumers during key holiday promotional moments and enhanced supply chain capabilities to strengthen our competitive position and support sustainable long-term growth.
I'll now walk you through the highlights from the quarter in the context of our strategies, starting with our first strategy to be brand-led. In Q3, we continued to reinforce Levi's position at the center of culture through impactful campaigns, premium experiences and iconic brand moments around the world.
A recent example of this was our partnership with one of our top European wholesale accounts, Zalando, for its fall/winter campaign that featured Lily Collins in head-to-toe Levi's and showcased the breadth of our denim lifestyle offering across Europe. And our debut at Paris Couture Week was another milestone in the elevation of the brand, bringing Levi's to one of fashion's most influential and prestigious global stages.
Looking ahead, we have a consistent drumbeat of brand activations and marketing moments planned through year-end with high-impact partnerships, including Shaboozey. And we are amplifying our strongest product franchises such as Loose, low-rise and Super Low through increased marketing support and compelling product storytelling.
For the holidays, we are as prepared as we've ever been with our most robust activation plan in years. From breakthrough brand moments and experiential pop-ups to elevate store experiences, personalized styling and curated gifting assortments, we are creating new ways for consumers to engage with Levi's throughout the holiday season. Combined with strong product newness and focused commercial execution, these efforts are designed to drive traffic, improve conversion and deepen consumer connection with the Levi's brand.
Now turning to product. The Levi's brand grew 4% with both men's and women's growing mid-single digits. While DTC pressure was most pronounced in our women's bottoms business, we have moved quickly to increase support behind winning trends and strengthen execution. Encouragingly, the DTC women's business accelerated in September, and we expect our total women's business to be up high single digits in Q4. 
In men's bottoms, newer iterations of our icons, including the 501 Loose and 501 Relaxed continue to gain traction, demonstrating our ability to drive growth through both heritage and innovation. In women's, we saw strong demand for wider leg silhouettes and the low-rise trend continued to fuel growth with our Low Loose and newer platforms like the Cinch Baggy delivering standout performance. These strong performing franchises give us confidence in our ability to further scale proven fits and drive future growth.
Importantly, growth in the quarter was balanced across both our core denim business and our expanding lifestyle assortment. Categories beyond bottoms contributed roughly half of our growth in the quarter, expanding our addressable market and building Levi's into a true denim lifestyle company.
Tops delivered a solid quarter of growth, led by women's tops, which increased 10%. Growth was broad-based across the assortment with strong momentum in blouses, wovens, sweaters, outerwear and tees. Blue Tab continues to exceed our expectations, delivering strong double-digit growth with broad-based strength across both men's and women's.
As we expand the assortment into more elevated products, including cashmere and premium knitwear, Blue Tab is extending the brand into higher price points, attracting new consumers and further premiumizing the Levi's brand in the marketplace.
Entering our fourth quarter, we are confident in our holiday assortment and the continued opportunity to build on the momentum we're seeing across our lifestyle categories. Sweaters will be a key focus, complemented by fresh denim innovation across both men's and women's.
Taken together, we are entering the holiday season with a stronger assortment, exciting newness across both lifestyle categories and denim and a compelling offering for consumers around the world.
Now shifting to our next strategy to be DTC-first. Our global direct-to-consumer business grew 2% in the quarter, with comp sales flat to last year, driven by the softer traffic in the U.S. and Europe, as I mentioned earlier.
Importantly, both businesses have returned to positive trends in recent weeks. Our DTC businesses in Latin America and Asia continued to deliver exceptional momentum. Latin America delivered broad-based growth across key markets, while in Asia, our DTC business achieved its seventh consecutive quarter of double-digit growth, driven by strong comp sales.
Both Asia and Latin America remain underpenetrated from a DTC perspective relative to the company average, providing a significant runway for continued growth. Our e-commerce channel delivered another quarter of double-digit growth. We continue to upgrade levi.com and recently improved the site with richer storytelling, more dynamic videos and inspirational styling content.
In the U.S., we launched our AI shopping assistant, which provides styling advice, helping consumers discover new styles and build complete outfits. While still early, we're seeing fans who engage with the tool adding to bag at roughly 3x our average rate. These efforts are part of our broader journey to build an entirely new digital flagship experience, including a complete redesign and platform migration of levi.com.
We are making great progress, and both efforts remain on track for a global launch next year. Once complete, levi.com will offer personalized experiences, dynamic outfit recommendations, immersive fit navigation and other unique capabilities that will convert more consumers into head-to-toe lifestyle shoppers.
We're seeing positive momentum in the business and continue to expect our DTC channel to grow at a high single-digit rate for the full year, including mid-single-digit growth in the fourth quarter. Global wholesale remained a source of strength in the quarter, increasing 6%, reflecting broad-based growth across segments, including in the U.S. The continued momentum reflects the health of our brand with key partners and improving sell-through trends.
Importantly, we are seeing strength across a broader range of categories beyond denim, reflecting increasing confidence from wholesale partners in the breadth of the Levi's offering. The consistent performance we have seen in wholesale throughout the year reinforces our conviction in our DTC first but not DTC-only strategy and demonstrates the complementary nature of our channels, allowing us to meet consumers wherever they choose to shop.
Now turning to our third strategy, powering the portfolio. This quarter, our international business grew 8%, led by Asia. The momentum in the region was further supported by our breakthrough partnership with ROSE and a series of pop-up experiences in Bangkok, Tokyo, Shanghai and Seoul.
The consumer response was extraordinary. And together, these activations generated more than 3 billion impressions and approximately $45 million in earned media value. We are also encouraged by the progress we're seeing in China, up 13%, where we continue to strengthen the brand and enhance execution.
While still early, we believe China represents one of the most significant long-term growth opportunities within our portfolio, and we are increasingly confident in our ability to unlock that potential over time. Signature plays an important role in our portfolio by extending the reach of the Levi's brand.
Signature grew 13% in the quarter, driven by strength in both core denim and our expanding lifestyle assortment. Denim tops and outerwear, looser silhouettes and new categories like maternity all contributed to the brand's strong performance.
Beyond Yoga was up 9%, driven by growth across both channels. Glowzone, our new performance collection, which launched in July, is generating positive early results and supports our strategy of expanding beyond yoga into more occasions like higher intensity workout activities.
As we approach closing out the year, we are more confident than ever in the long term. Over the last 3 years, we have built a larger, more diversified and more profitable Levi Strauss & Co., adding nearly $1 billion in revenue, significant margin expansion and stronger earnings while significantly strengthening our cash generation.
With this strong foundation, we see meaningful opportunities to drive sustainable top and bottom line growth across our channels and markets as we further build our position as the leading global denim lifestyle company.
And with that, I'll turn it over to Harmit. Harmit?

**Harmit Singh** (Executives):
Thank you, Michelle. Before we get into the quarter, I'd like to start by welcoming and congratulating John as the company's next CFO. John's deep financial expertise and strong track record, combined with the financial and growth foundation we have built as a world-class finance team, give me confidence that the company is well positioned to deliver sustainable, profitable growth.
While the third quarter had its challenges, our teams responded quickly. As Michelle mentioned, we saw improving trends emerge in September, particularly in DTC and women, which gives us confidence in the actions underway and our updated outlook. We entered the final quarter of the year with improving momentum, strong financial discipline and a clear focus on execution. Before I turn to the results, I want to address the impact of tariff refunds, which creates some unique dynamics in quarter 3 and Q4 results.
During the third quarter, we recorded approximately $80 million of tariff refunds, reflecting substantially all the refunds we expect to receive. We are redeploying roughly 3/4 of the benefit back into the business to support future growth. These investments are expected to be split approximately 60-40 between SG&A and COGS and are focused on the following 3 areas: incremental marketing to drive demand, enhanced supply chain capabilities to improve competitiveness over time and sharper value for consumers during key holiday promotional moments.
Approximately $25 million of these investments were redeployed during the third quarter with approximately $35 million expected to be invested in the fourth quarter. We believe this is the right approach. It allows us to strengthen the business, support our near-term momentum and still deliver on our annual growth algorithm. With that context, let me turn to our third quarter results.
Overall, we delivered mid-single-digit revenue growth with net revenues up 4% on a reported basis and 5% on an organic basis. Gross margin expanded 450 basis points to 66.2%. The benefit from tariff refund, net of redeployments contributed 370 basis points to gross margin.
Excluding that benefit, the remaining non-tariff-related gross margin expansion of 80 basis points was driven by lower product costs, partially offset by foreign exchange. Adjusted SG&A as a percentage of net revenues was 50.8%, which included approximately $6 million or 40 basis points of tariff benefit redeployment. Excluding that redeployment, adjusted SG&A increased 50 basis points versus the prior year, driven by higher distribution costs and deleverage from softer DTC revenue growth.
Distribution costs were higher than we expected this quarter and the path to realizing the full benefits of our network transformation has taken longer than we anticipated, reflecting both the complexity of the transition and a fire-related incident that impacted operations. That said, we are making progress. We closed our Hebron distribution center at the end of the third quarter and expect to begin realizing benefits from the closure in '27.
In Europe, where our distribution center transformation is complete, we're already seeing distribution cost leverage year-to-date. As we continue to scale and optimize the network, we expect service efficiency and productivity benefits to build over time.
Adjusted EBIT margin was 15.5%. The tariff refund benefit net of redeployment contributed 330 basis points to adjusted EBIT margin. The remaining non-tariff-related EBIT margin expansion of 40 basis points was largely driven by accelerating margins in Asia and growth in wholesale.
This is a good example of the power of the and in our model. Even in a dynamic environment, the strength of our diversified business helped us deliver both growth and margin expansion. Adjusted diluted EPS was $0.48, which included $0.11 benefit from tariff refunds, net of redeployment. Excluding this benefit, the remaining 9% growth versus Q3 '25 was driven by EBIT margin expansion and share buybacks.
Moving to the balance sheet. We ended the quarter with inventory down 3%, reflecting continued progress in improving the health and productivity of our inventory while maintaining the flexibility to support growth opportunities. We continue to strengthen the life cycle management of our inventory and expect to exit the year with inventory levels in line with our expected sales growth.
Turning to shareholder returns. We returned $62 million to shareholders in the form of dividends during the quarter, representing 11% increase versus last year. In addition, given our strong cash position and confidence in the business outlook, we intend to repurchase an additional $100 million of shares through an accelerated share repurchase program.
Now let's review the key highlights by segment. In the Americas, net revenues grew 2%. LatAm delivered another strong quarter with revenues up 10%, fueled by strength across channels and growth in every market in the region. Operating margin expanded 640 basis points to 29.9%, primarily due to the benefit of the tariff refund net of redeployments. And in quarter 4, we expect the U.S. to return to growth driven by improving DTC trends.
Europe net revenues grew 5% similar to the performance we saw in the first half of the year, driven by double-digit growth in wholesale. We saw strength in key markets, including the U.K., Germany and Italy as well as growth across categories. Operating margin increased 150 basis points to 22.8%, driven by gross margin strength.
As warmer weather moderated, DTC performance improved. And looking ahead, wholesale pre-bookings for spring/summer '27 are up high single digits, giving us confidence in the continued momentum of the business. Asia net revenues delivered its third consecutive quarter of double-digit growth, up 10%, fueled by strength across channels, categories and key markets, including Japan, India, Australia and China.
Strong gross margin expansion drove operating margin leverage of 220 basis points to 14.2%. Year-to-date, Asia EBIT margin is up 240 basis points to 16.7%, underscoring the improving margin profile of the segment and its growing contribution to overall company profitability. That sustained momentum gives us confidence to continue investing behind the segment with many of our nearly 60 net new system stores planned for Asia in the fourth quarter.
Now turning to guidance. Our updated outlook reflects both the benefit of the tariff refund and our decision to redeploy a significant portion of that benefit back into the business. We believe this balanced approach strengthens our competitive position, supports near-term growth and keeps us on track to deliver our annual algorithm of mid-single-digit revenue growth with a clear path to 15% operating margins over time.
Importantly, recent trends reinforce our confidence in the fourth quarter. We are seeing improved momentum in DTC and women's, including positive growth in U.S. DTC, and we are increasing marketing support and investment behind winning products as we prepare for the holiday season.
Overall, we are confident in our ability to lap this year's strong results, inclusive of the net tariff benefits as we set the business up for 2027. For the full year, we now expect reported net revenues growth to be approximately 7% versus our previous outlook of 7% to 7.5%, driven by the stronger U.S. dollar and we expect organic net revenues to be a little stronger at approximately 6%, which is at the high end of our previous expectation.
We now expect gross margin of approximately 63% for the full year, including approximately 80 basis points of net tariff refund benefit. Excluding this, gross margin is higher than our previous outlook, driven by the benefit of the lower tariff rate and lower product costs.
We now expect adjusted SG&A as a percentage of revenue to be approximately 51% compared with our prior outlook of 49.7% to 49.9% -- this includes approximately 50 basis points of redeployment of the tariff refund benefit.
Accordingly, we now expect adjusted EBIT margin to be slightly above the previous guidance at approximately 12.1%. This includes approximately 30 basis points of net tariff refund benefit. Excluding the net tariff refund benefit, adjusted EBIT margin would be up 40 basis points versus the prior year.
We now expect adjusted diluted earnings per share to be in the range of $1.54 to $1.56 for the full year, including a $0.04 net tariff refund benefit. For the fourth quarter, we expect reported net revenues to be approximately 3% and organic net revenues to be approximately 4%, with the difference reflecting the impact of foreign exchange. We expect gross margin of approximately 61.8%, up 100 basis points versus prior year, including $3 million or another 10 basis points of net tariff refund redeployment costs.
Adjusted SG&A for the fourth quarter includes approximately $30 million of tariff refund redeployment costs. And as a result, we expect adjusted EBIT margin of approximately 11.4% to 11.6% for the quarter, which includes 180 basis points of net tariff refund redeployment costs. This translates to adjusted diluted EPS of approximately $0.36 to $0.38, including $0.07 of net tariff refund redeployment.
While the third quarter highlighted a few areas of opportunity, the team responded with agility and urgency and the actions we have taken are already beginning to show results. Even more importantly, the quarter also reinforced the power of our strategy and the benefits of our increasingly diversified business model.
As I conclude, I want to say thank you to our employees, our fans, Michelle and the executive team, our Board, our shareholders, including the Levi's family and the buy-side and the sell-side analysts who follow us. Thank you for your support, your trust and your partnership throughout my tenure.
Over the past 14 years, I've had the privilege of being part of one of the most significant chapters in the company's history. Together, we strengthened the business, returned the company to the public markets, built a more diversified portfolio across channels, geographies and categories and significantly strengthened our balance sheet and financial foundation.
But what I'm most proud of is that as the business has grown, so have our people, especially my world-class finance growth and transformation team. I'm deeply grateful to have been part of the journey and to have grown as a leader alongside so many of my talented colleagues.
As I look ahead, I wish Michelle, John and the entire company my very best. I'm honored to say that this is my 56th and final earnings call at the company and my 67th as a CFO. And with that, operator, let's open the line for questions.

**Operator** (Operator):
[Operator Instructions] Our first question comes from the line of Laurent Vasilescu of BNP Paribas.

**Laurent Vasilescu** (Analysts):
Michelle, Harmit, I wanted to ask about your DTC trends in the U.S. I know, Michelle, you provided some color there about traffic trends. But could you maybe just unpack a little bit more what drove the underperformance in the third quarter? Like how did the quarter progress by month?
And then separately, Harmit, I think you mentioned that global DTC should grow mid-single digits in the fourth quarter, which is very encouraging. But should the U.S. and Europe both grow mid-single digits? And then I think you also mentioned that you've seen positive trends in the recent weeks.
But is that a comment in line with the fourth quarter commentary of mid-single digits?

**Michelle Gass** (Executives):
Thanks, Laurent, for the question. And I'll just take the whole one because it's all connected. So kind of back to what happened U.S. DTC, and I mentioned it in my remarks, I'll add a little more color.
So -- well, first, I will say the Levi's brand remains very strong, very healthy around the world, including in the U.S. And I know we spoke to what really drove the growth, whether that was global wholesale, up 6%, really strong growth international, up 8%, e-commerce double digit, et cetera. And it's worth mentioning in the U.S. that U.S. wholesale was also positive. So we really can isolate the DTC issue to Europe and the U.S.
In Europe, it was very clear this was a weather-related issue. I mean I think it's no secret that it was very warm and it impacted footfall for the industry, really. And so that impacted our business despite we had lots of great summer offerings, but the weather was at another level. When the temperature started cooling and weather moderated, weather moderated, we saw the trends come back. And so as we are in Europe right now, DTC quarter-to-date, the trends are very robust, very positive and robust. So you should feel good about that. The other thing worth mentioning in Europe is that we had an incredible wholesale business. So suffice it to say, like I said, the brand is very healthy there.
In the U.S., I'll say it again, brand is healthy. This really had to do with kind of a tactical move around back-to-school and how we showed up for that period. And we would say that our back-to-school campaign underdelivered our expectations. And then more specifically, our campaign was all around loose.
Loose is still an important business. It's a big volume driver for us, but the market in the U.S. had really shifted to talk about low, low rise was a lot of energy and a lot of competitiveness, frankly, around that. And we saw that softening sort of July and August. The good news is the team got after it very quickly, and we sharpened our focus.
We have the benefit of the tariff refunds. As we remarked earlier, we're reinvesting that back into demand generation, into marketing and into the consumer. And we pivoted into low. And so we're able to do that quite quickly. And so we are already seeing the benefit. So that started sort of very tail end of Q3, but more importantly, into Q4 into September, and we're seeing the results.
So to your question on what's happening in the U.S., the U.S. DTC is now back to positive. overall DTC is tracking right now quarter-to-date mid-single digits. We expect it, let's say, to be mid-single digits for the quarter and then to end the year in what we've been performing at sort of that high single digits. So we feel very good. I mean it's been a 360 approach across marketing, mid-funnel marketing, mid-funnel demand generation, in-store execution, et cetera.
And so yes, so like I said, I feel that gives us the confidence to share these numbers that we're talking about for the quarter ahead. I'd also say, as it relates to the U.S. consumer, the category is still strong, and we continue to gain market share with men and women, hold that #1 position between men, women and youth. So I feel like we've addressed it.

**Operator** (Operator):
Our next question comes from the line of Matthew Boss of JPMorgan.

**Matthew Boss** (Analysts):
Congrats on your next chapter, Harmit. So Michelle, maybe if we took a step back, can you speak to the health of the denim category? Has anything changed other than this intra-category trend change that you cited?
And can you elaborate on September maybe relative to that 4Q outlook for 4% organic revenue growth? And Harmit, just any operating margin considerations for next year for us to think about relative to the annual margin expansion algorithm that you would see at mid-single-digit revenues?

**Harmit Singh** (Executives):
Sure. So you want to go ahead?

**Michelle Gass** (Executives):
Yes. Yes, I'll start. So thanks for the question, Matt. So I would say that the denim category remains healthy, robust, and it's attractive, right? You see lots of companies, either if they're in denim being more assertive and competitive or even in some cases, new entrants into the category.
So there's a lot of energy in denim. I'd say as the category leader by a mile, like this is good for us, but it also is we got to continue to lead, lead with innovation, lead with fits, et cetera, et cetera. And so from that standpoint, while I alluded to that in hindsight, we would have done -- we would have approached Q3 or back-to-school differently knowing what we know today, but we've learned. And importantly, when you learn, you pivot, you're agile and the team moved. And we're already seeing results.
So I'll get to that in a minute. But as it relates to our relative position, in men's, and I'm speaking to the U.S. now, #1 continues in men's, and we actually gained share and further widened our lead against the #2 player. In women's, we've been solidly #1, again, strengthened our position there. Youth, even despite the level of competition, we've maintained our #1 position.
And I think importantly, we have a segmented strategy. So we have Red Tab, we've got Signature and then we've got Blue Tab, and we are gaining market share in that $100-plus segment. And as I mentioned on the call, our Blue Tab business, while small, is growing double digits, and we think that's going to be a meaningful growth driver in the future.
And the end of this is while leading in denim, categories still growing, we are, as you know, Matt, expanding beyond denim. And so our head-to-toe denim lifestyle strategy is working. Half of our growth -- so of our 5% organic growth, half was driven by categories like tops outside of denim bottoms. Tops accelerated this quarter with a robust 7% growth.
So I think all in, we're feeling good about the category, but we're very present of the fact that the competitive nature has intensified, hence, really taking some of that tariff refund money and deploying it back into driving demand and marketing so that we can make sure that we can break through.

**Harmit Singh** (Executives):
And Matt, to your question about the annual growth algorithm -- we had a big discussion and debate around this, especially given that the tariff refunds are incorporated in the results. And that's why we talked about the reported results and the underlying results.
Overall, our view is that the annual growth algorithm is intact, which is really a mid-single-digit growth company with growth in gross margins and growth in EBIT margins. So let me give you a little bit more color. The organic revenue guidance for the year, we have taken up to the high end of our range. And that's largely driven by wholesale being stronger.
So wholesale, I think last quarter, we said globally would be low to mid. We're now saying mid-single digit. And that is really -- I think all of you have asked us, why don't you grow wholesale, but this is the second year we're growing wholesale globally, and it's profitable.
Asia, which was underlevered because it wasn't growing and the margins were lower, also, we have up to low double digits, and that helps operating margin. We end the year at about 12.1% EBIT margins all in and which is 70 basis points versus a year ago. And all of you do a great job dissecting what is tariff and what is not.
Our view is all in, 12.1%, we will lap that going forward. So that's a new base. And so that's how we are thinking about it. So the way to think about it is we end the year on a reported number. We lap that for next year and then build the annual algorithm on it. Now how are we going to lap it? There are expenses that we are undertaking to drive the future growth of the business that won't repeat in 2027.
So if you do advertising as an example, as a percentage of sales, it will be higher this year than the 7%, but we don't have to spend at this pace next year. As an example, distribution, we have talked about, we are making the strategic transformation, but -- and it was a little expensive because we're running 2 parallel distribution centers. It won't be at that pace next year. That's why our view is that we can continue to grow margins and obviously, top line. I hope that helps you, Matt.

**Operator** (Operator):
Our next question comes from the line of Jay Sole of UBS.

**Jay Sole** (Analysts):
I want to follow up on the last question. You talked about -- you gave us great color on the DTC channel trends for U.S. and Europe. But does the wholesale business sell-through trend in the U.S. and Europe look like the DTC trend? Harmit, I think you mentioned that the European prebooks for next spring are up high single digits.
If you could just give us a little bit of context for how the sell-through is running in wholesale in the U.S. and EU and how that's impacting the order books in next year, that would be helpful.

**Harmit Singh** (Executives):
Well, Jay, I was wondering if you or somebody else would ask a question on wholesale. As I mentioned, channel has done globally performed really well. And it's the -- what I call the power of the 'and'. It's DTC and wholesale, which is important. Now you know wholesale does ebb and flow every quarter largely because you sell in, you set floors. -- timing is different by customer. But overall, wholesale has been performing well globally, including in the U.S. It's profitable, which is really good.
And it's across all categories. I mean women's is performing well, Men's is performing well. AURs are up and so is units. So overall, we are pleased with the performance. I mean, looking ahead and your question -- specific question, Jay, on sell-through, the sell-through is fairly good. We've seen good sell-through trends. It's healthy. The prebooks are strong. We get data on prebooks in Europe, so we reflected that.
I think quarter-over-quarter, especially in the U.S., it's pretty ebb and flow. So wholesale in quarter 4 will be a little weaker than the wholesale you saw in in quarter 3 in terms of growth year-over-year, but it is not because of weakening demand. I mean -- and let me just assure you. It's just when flow sets are set, when product goes to the customer. But generally speaking, we are seeing a healthy demand from our retailers across the world.

**Jay Sole** (Analysts):
Got it. Okay. Super helpful. Harmit, congratulations again and best of luck.

**Operator** (Operator):
Our next question comes from the line of Dana Telsey of Telsey Advisory Group.

**Dana Telsey** (Analysts):
Harmit, best of luck in your next chapter. Michelle, I think you mentioned some events in back-to-school not impactful enough. How do you -- what's your assessment? And what's changing for holiday? Is it the marketing? Anything with product? You mentioned low rise.
And also, you mentioned that the competitive environment intensified in price to intensify in price and style? Or what are you seeing in the competitive environment? And just lastly, as you look out to 2027, I think last year was the year of music. This year was the year of sports. How do you think of next year in terms of topical?

**Michelle Gass** (Executives):
All very good questions, Dana. Thank you for that. Yes. So let me add just a little bit more. And I will tell you, the teams here, as we saw the issues unfolding, they were all over it. I'd say just both here in the U.S. and globally, the consumer moves fast. And so we've got to just continue to be on top of it. And by and large, we are.
I'd say, but there are going to be moments like this. If you aren't quite there with the consumer, then you have an opportunity to react. And that is, frankly, the benefit of also getting all this data real time in your own channels so that you can impact not only DTC more broadly.
But as I've been talking about, as we took a step back, we felt like our campaign in this period of time was not as impactful as it could have been. And you see that in the numbers. Our traffic was soft. And so rather than continue to go with that same direction, we pivoted.
And our diagnostics would say that at a time when, hey, the loose business, and to be clear, it's still a very big business and it's growing, but there was just a lot of energy and excitement, whether that was online, offline around the rise getting lower. And we have plenty of it. It just wasn't our leading message.
So when the team understood that, they then quickly moved to pivot into low rise. And what that meant in practice was reshooting the campaign, getting that in stores, remerchandising the store. We have a whole a whole group of content creators in social media. We have let them loose. So all of that is happening as we speak. So we really put this in place right as we started September. So that was for women.
And then for men and men has been a pretty steady performer, but also took the opportunity as a big business for us to also reenergize the men's business. And we did that around our icons, 501. One of the top sellers right now is 501 Loose, so that baggy for men idea. And one of our influencers that also has worked well for us in the U.S. has been Shaboozey, who his star power has only grown over the last year. So we're leaning into a Shaboozey partnership with men. We're really going after this low rise through digital, social, in-store demand generation, like I mentioned, and then chase more product.
So leveraging our supply chain to make sure we have the inventory. And as I said, the indications are good. The U.S. trends in DTC quarter-to-date are positive. DTC globally overall is running mid-single digit, and we expect that to at least carry into the full quarter to be mid-single digit around the world.
Similarly, in Europe. Europe is back to mid-single digit, given its pivot out of this very warm weather. And then to your point on holiday, really excited about what's ahead. Being a DTC player now, it will feel very holiday. So we'll lean into the classic denim innovation, but we're also going to take a big position in tops, in sweaters.
We have a lot of innovation coming, fantastic store merchandising, some really innovative creative that you'll see soon. So our intent is to win the holiday, and I'm confident we will. And then you asked about what does this mean going forward? I mean we are upping our marketing game.
Again, the tariff refunds allowed us to redeploy right into investing in the consumer and telling our story. We expect that to be a tailwind as we start the next year. And then specifically, what's the big idea for next year? I'm not at liberty to share that with you yet, but I'd say we're taking all of our learnings over the last 2 years to make sure that we are showing up in an innovative and compelling way for our fans around the world.

**Operator** (Operator):
Our next question comes from the line of Rick Patel of Raymond James.

**Rakesh Patel** (Analysts):
Harmit, congrats on a remarkable career as well. A follow-up on the earlier margin question. So you're redeploying tariff refunds into marketing, supply chain and sharper value for the consumers. Is it safe to assume these factors are not limited to the back half of this year and they'll continue through the first half of next year as well?
I appreciate your long-term algo is for mid-single-digit revenue growth. But if these investments do continue, what's the minimum growth that you would need to see in order to achieve operating leverage going forward?

**Harmit Singh** (Executives):
Yes. I mean, Rick, obviously, this is not about guiding next year. I'm going to leave that to Michelle and John and the team -- but our view is the tariff refunds were timely. The business, as Michelle mentioned, softened, especially on DTC and women's, and we acted with agility and speed and utilize that largely against driving more focused marketing with a real product awareness, accelerate our product offer, especially things that are working and promotional -- we didn't take prices down.
Some retailers had. We took it up, but that's not something we decided to do because we do provide good price value. But we said, let's promote because market got a little promotional, especially during holiday events, let's promote so we're competitive. And so our view is it's not something that -- the expenses, incremental expenses don't sustain into 2027.
And so our view is a mid-single-digit growth does allow us to leverage to the P&L, and you'll see that flow through to EBIT. We're not running away, and Michelle is completely supportive of this and so is the executive team. We do want to get to 15% operating margins. And if you take the last 3 or 4 years, in '23, I think our operating margins were 9%, -- we'll end this year over 12%. And so we are on that path and that journey.
I hope that answers your question. I can't be more specific, Rick, unfortunately, because we haven't yet completed our financial plan, and John and Michelle would be the best to lay it out for you next year -- early next year.

**Operator** (Operator):
Our next question comes from the line of Bob Drbul of BTIG.

**Robert Drbul** (Analysts):
Harmit, 56 quarters. That's a lot of quarters.

**Harmit Singh** (Executives):
I'm not going to ask you, Bob, how many quarters you've covered, but as a CFO, thank you for that.

**Robert Drbul** (Analysts):
I guess the first question really for Michelle is when you think about Blue Tab, I think double-digit growth, like what have been your learnings thus far with that initiative? And I guess, sort of similarly, when you think about the brand heat, I would be interested in hearing sort of any of the successes you've had with collabs and sort of what we should be looking for in the next few months in this holiday season around collabs that you're really excited about?

**Michelle Gass** (Executives):
Yes, you bet. Thanks, Bob. Thanks for asking about Blue Tab. It's something we all have a lot of passion and belief for that this could be a real opportunity for us. As the denim leader, we have like less than a 1% market share of the super-premium jean category. And that should at least be commensurate with our market share overall.
So you can do the math and see the opportunity. And we -- because we have this leadership, we do have all of this innovation and knowledge about denim and the best denim. So for Blue Tab, I'd say the learnings, number one is it is always anchored, of course, in denim authority and denim leadership. So when we use denim in our Blue Tab, it will be that amazing Japanese selvedge denim.
I think the insight we have today versus when we've sold in the past, like denim bottoms of of Japanese denim is that this, with Blue Tab, is this can be an entire category head-to-toe, not unlike what we're doing for Red Tab. So we can use a beautiful Japanese denim in bottoms, in jackets, in dresses and skirts. And if you actually see online, you'll see representation of all of those products.
But we can also extend into tops categories, but they need to look -- feel different than our core Red Tab. So I think I said in my remarks that we're getting into really elevated fabrics like cashmere, like Silk, very premium blazers, denim trousers. So you can imagine this whole lifestyle presentation. And so it's going to be a big opportunity for us.
And one of our biggest insights is that is -- and we're still work in process is how to merchandise it in the store. And you can see a mixed approach in our stores today of some outstanding merchandising, Harajuku in Japan as an example, to where we're still experimenting. But we will figure this out because it's such an incredible opportunity with price points ranging from $200 to $500.
As it relates to collaborations, also a great way to elevate the brand. Right now, we just launched the Sacai collaboration. So you can actually see it on our site, although it's selling quickly, but that's a great example of us connecting with the highest levels of couture type of thing.
We have a few more in the pipeline that we have not talked about yet. But I think what you can expect from us and a recipe that has worked is a real balance between what I'd call more commercially oriented collabs to ones that have this very high-end Sacai. We did Valentino a couple of years ago, Miu Miu a few years ago, sort of that.
And the good news is, given the brand heat today, people are knocking on our doors. So we've already have the pipeline and the calendar for next year, I would say there's some really good ones in there. So you'll be hearing about that. I actually just got the Sacai jacket myself yesterday, but it is selling out.
So for those who are interested, you better get after it. And then I think the other piece on brand heat, one of our real exciting moment that's happening today is happening in Asia. So we did a global campaign with ROSE, launched at the Super Bowl. She was part of our Behind Every Original.
That has now manifested as a partnership in Asia, a collaboration. We're doing pop-ups. When you see these pop-ups happening, there are literally thousands of people in line to see ROSE. And it has been a tailwind to how we're getting the overall results of, like I said, Asia overall 10%, China up 13%. And our women's business in Asia is even higher than that, all driven by this ROSE momentum.
So stay tuned, lots to come.

**Operator** (Operator):
Our next question comes from the line of Kendall Toscano of Bank of America.

**Kendall Toscano** (Analysts):
Harmit, congrats on the retirement. Just wanted to ask about the -- well, you talked about greater-than-expected complexity in the U.S. distribution network transition in the U.S. And just curious, how should we think about this in light of what was supposed to be an immediate $5 million in cost savings per quarter as soon as you shut these parallel DCs down in 4Q.
It sounds like we now shouldn't expect to see any benefits until 2027, but any visibility on when in 2027 and what besides the fire that you called out has been more challenging than you anticipated?

**Michelle Gass** (Executives):
Sure, Kendall. I can take this one. I'll first say that we are disappointed more than anyone that this transition has taken as long as it has, and it's been more complex. And I think as we've kind of ramped this up with our partner, we do have a complex business given the number of SKUs we have, the number of channels, the number of customers. We will get there. It's just taking more time.
And we did mention the fire that happened towards the end of the quarter, which just was a big disruption in some of our most important weeks. And so it was what it was. The team recovered fine. So I guess we're just being patient and realistic in terms of when we will see the benefits. I do think a very important milestone that we achieved was closing our parallel Hebron facility. So we closed at the end of Q3.
With this behind us, we truly can begin to see the benefits in 2027 because we will not have that running. As it relates to Q4, I'd say, as Harmit was speaking to earlier, I mean, the good news is we do have a lot of demand from both channels. So we need to make sure that Groveport is set up to fulfill the demand.
And that's why we're making some investments along with our partner to ensure that we get the productivity, we get the service levels, we get the inventory right and then over time, get that cost efficiency.
So we believe we're confident we will begin to see that in 2027. We're not guiding 2027. We'll talk about that more. But we believe that 2026 let's call it, the peak of what has been our transition-related costs relative to this. And the last thing I would leave you on is that the proof point for us is we did complete a complex transition in Europe, and that took some time. That's now behind us, and you are seeing the EBIT performance and benefits of that. So that does give us confidence that we will get behind this.
I think 2027 is very reasonable and realistic to start seeing the benefits. And like I said, closing that Hebron facility was an important milestone to say we have the confidence that Groveport will fulfill our needs. Now we're working through the operational complexities there.

**Operator** (Operator):
Our next question comes from the line of Ike Boruchow of Wells Fargo.

**Irwin Boruchow** (Analysts):
Harmit, best of luck. We'll miss you, been a pleasure working with you. I'll ask just 2 questions. On the 4Q guide relative to 3 months ago, is there any change on the revenue guide? It looks like it's a little lower than the implied before, but I just want to check that to you guys.
And then on the reinvestment of the refund on gross margin, Harmit, can you just be a little bit more specific, what exactly are you guys doing? And why is that not a drag that we need to think about that potentially kind of lingers into 4Q or the first half of next year? Just more of the mechanics there.

**Harmit Singh** (Executives):
Yes. So I think, Ike, on the revenue, it is a little lower than the implied guide for Q4 because we guide the following quarter and the full year is largely driven by foreign exchange. So reported, I think consensus is about 4.1% and this implies, I think we're saying 3%. Foreign exchange is a 100 basis point drag from that perspective. So that's your question on revenue.
The question on what are we doing in gross margins is largely -- we're doing a couple of things. We're -- we could have taken pricing down. We could have. That was just one of the levers. When the tariffs happened, it was not the only lever in the U.S. There are a couple of other pieces. But as I said earlier, we looked at the price value. And I think our current prices sustain that long term. And given the environment is a little bit more promotional at this stage, we are really targeting promotions on key holiday moments.
I mean that's how we're thinking about it. Think Labor Day with Thanksgiving coming up with holiday, that's where we're thinking about it. To your point about why shouldn't this last? And also, I think Michelle said, we didn't have the right offer in the quarter. So we had to do this.
And so given the fact that we strongly believe working with our product teams and the marketing team that we do have a great offer for holiday. Michelle talked about sweaters and the like, and you will see that in our stores. I think that coupled with our execution, we believe the promotional aspect of our offers will probably not sustain itself. And I think Matt asked the question about gross margin. We feel good at this time, continue to grow gross margins in 2027.

**Operator** (Operator):
Our next question comes from the line of Brooke Roach of Goldman Sachs.

**Brooke Roach** (Analysts):
Harmit, you mentioned 3 areas of reinvestment of the tariff refund supply chain, marketing and sharper value on promotions. Can you quantify the proportion of investment that you're putting towards each bucket? And if any of these investments will lead to payoffs in the business in 2027 and beyond versus the investments that are just driving immediate impacts to your business?
And then maybe a follow-up for Michelle. Given the enhanced marketing as a percent of sales this year, how are you thinking philosophically about the opportunity to potentially reinvest at a higher marketing spend rate over the next several years, similar to what we've seen other companies do in the branded space?

**Harmit Singh** (Executives):
So to answer your question, Brooke, the simplistic way, let's say we spend -- we redeployed $60 million out of the $80-odd million for tariffs that we received. I would say 1/3 is marketing, 1/3 is distribution and logistics and 1/3 is promotional activities. A little bit, we did clear some inventory just to make sure we are clean and we have inventory for the holiday. That's the simplest way of looking at it.
In Q3, the majority was promotions, a little bit of advertising, a little bit of inventory clearance. In Q4, it's largely advertising, marketing, distribution and slight promotions, not to Ike's question, the activities that -- the promotional activities we ramped up in Q3 are going to be ramped down in Q4, largely because we've got better product and we've got better marketing.
Does that answer your question, Brooke?

**Brooke Roach** (Analysts):
Yes. Helpful.

**Michelle Gass** (Executives):
And Brooke, I can take part 2. So I think your question is to me, how should we think about our bridge between, say, Harmit mentioned it earlier, we're at 9% in 2023. We're at, call it, we've just guided around 12%, and we're still committed to the 15%. Our line of sight there is that we see opportunity in driving store 4-wall profitability. We see leverage opportunity based on the volume, how we think about corporate expense and the like.
We do see an opportunity for D&L improving over time. We can see it this year. We think it's the peak. So all of those things and a few more, we see as gross margin, another one. We expect to continue to elevate the brand and get gross margin gains. So those will all be tailwinds between now and put a date out there to get 15%.
Along the way, from a marketing standpoint, our intent is over time to invest more in the brand. Now we're at roughly 7%, a little bit more than that. I'm not going to put a precise number. But if we continue to get good returns on marketing, we'll find a way to fund that. So that's how we're thinking about it in the context of our commitment to all of you to get to that 15% EBIT. So we'll be obviously on our next call talking about how we're thinking about '27 in that context. So stay tuned.
And I think that was the last question. So thank you, everyone, for listening. I guess I want to make just one reiteration that as we think about our business heading into the fourth quarter, we've said it already. The trends are positive. DTC is running at least a mid-single-digit rate. We feel confident for the balance of the year and want to wish everyone a great holiday, and we'll see you in January. Thank you.

**Operator** (Operator):
Thank you. This concludes today's conference call. Thank you for your participation. Please disconnect your lines at this time.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LEVI_Q2_2026_Earnings_Call_20260708.md
- 2026-07-08｜CFO｜guidance：全年調整後稀釋 EPS 指引上調為約 1.46–1.52 美元（原 1.42–1.48）（原話："range of approximately $1.46 to $1.52, up from"）
- 2026-07-08｜CFO｜guidance：全年有機營收指引上調為 +5.5% 至 +6%（帳面 +7% 至 +7.5%）（原話："7% to 7.5% and organic net revenues to be up 5.5% to 6%."）
- 2026-07-08｜CFO｜guidance：Q3 營收指引：帳面與有機皆 +4% 至 +5%，無匯率助益（原話："organic net revenues to be up 4% to 5% for the quarter"）
- 2026-07-08｜CFO｜guidance：Q3 調整後 EPS 指引約 0.34–0.36 美元，含稅率與匯率對毛利率的 0.02–0.03 美元逆風（原話："approximately $0.34 to $0.36, which includes a"）
- 2026-07-08｜CFO｜guidance：全年調整後 EBIT 利潤率指引 12%（原話："We expect adjusted EBIT margin to be 12% for the full year"）
- 2026-07-08｜CFO｜margin：全年毛利率指引：預期擴張約 10 個基點（原話："now expected to expand approximately 10 basis points"）
- 2026-07-08｜CFO｜guidance：指引的關稅假設：中國 30%、其餘 20%（原話："U.S. tariffs on imports from China at a 30% rate"）
- 2026-07-08｜CFO｜guidance：指引未計入潛在關稅退款（原話："does not assume any benefit from potential tariff refunds"）
- 2026-07-08｜CFO｜guidance：CFO 承認下半年指引隱含的放緩屬保守設定（原話："it is prudent. It is conservatism and it's probably"）
- 2026-07-08｜CFO｜margin：H2 EBIT 利潤率擴張集中在 Q4，並列出四項驅動（關稅基期、匯率壓力、A&P 正常化、重複配送成本減少）（原話："more pronounced in Q4 as we begin to lap the full impact"）
- 2026-07-08｜CFO｜margin：CFO 以 Q4 約 14% EBIT 作為口徑說明（回到 2024 年基期）（原話："let's say, circa it's about 14% EBIT"）
- 2026-07-08｜CFO｜margin：CFO 稱 Q4 2024 是 Q4 2026 的良好參照，因去年關稅拖累約 100 個基點以上（原話："Q4 '24 is a good proxy for Q4 2026"）
- 2026-07-08｜CFO｜margin：Q2 毛利率擴張 10 個基點至 62.7%（原話："expanded 10 basis points to 62.7%"）
- 2026-07-08｜CFO｜margin：Q2 調整後 EBIT 利潤率擴張 70 個基點至 9%（原話："adjusted EBIT margin expanded 70 basis points to 9%"）
- 2026-07-08｜CFO｜margin：CFO 拆解 Q2 SG&A 增幅：三分之一來自匯率（原話："1/3 of the SG&A increase was contributed by"）
- 2026-07-08｜CFO｜margin：營收成長中單位數與均價（AUR）的拆解：Q2 為 2/3 對 1/3（原話："2/3 of the growth was contributed by units and 1/3 by AUR"）
- 2026-07-08｜CFO｜guidance：全年單位數與 AUR 的貢獻預期改為約各半（Q1 約各半、2025 為 2/3 對 1/3）（原話："Our expectation for the year is more 50-50."）
- 2026-07-08｜CFO｜margin：管理層將 AUR 提升歸因於減少促銷與全價銷售占比提高（原話："reduced promotional levels and cost efficiency"）
- 2026-07-08｜CFO｜risk：關稅退款約 8,000 萬美元已付，管理層稱金額可觀但尚未決定如何處理（原話："We are not incorporating it in our guidance, but it's"）
- 2026-07-08｜CFO｜risk：關稅降稅對成本的利益因庫存周轉約 2 次而遞延，Q2 邊際、Q3 少量（原話："Q2 was marginal. Q3 will be a little bit"）
- 2026-07-08｜CEO｜risk：CEO 提及仍留意外部環境（原話："While we remain mindful of the external environment, the"）
- 2026-07-08｜CFO｜commitment：長期目標重申：營收 100 億美元與 15% 營業利潤率（原話："path to $10 billion in revenue and 15% operating margin"）
- 2026-07-08｜CFO｜commitment：全年淨新開店 50–60 家，多數落在下半年（原話："50 to 60 net new doors this year"）
- 2026-07-08｜CFO｜commitment：全年存貨金額預期略高於去年但低於銷售成長（原話："slightly above last year but below expected sales growth"）
- 2026-07-08｜CFO｜commitment：美國 Hebron 配送中心移交 Maersk 預計於 Q4 初完成，進度較原計畫慢（原話："The transition has taken longer than planned as we"）
- 2026-07-08｜CFO｜commitment：CFO 說明延後 Hebron 關閉的額外成本僅數百萬美元（原話："The cost is a couple of millions"）
- 2026-07-08｜CFO｜commitment：全球 ERP 整合：歐洲與其餘拉美國家預計 2027 年中完成（原話："countries are on track for completion by mid-2027"）
- 2026-07-08｜CFO｜commitment：CFO 提到 ERP 完成後具備重新思考會計年度行事曆的基礎（原話："we have the foundation to get that to at least think through"）
- 2026-07-08｜CFO｜capital_allocation：資本配置架構：將自由現金流的 55%–65% 以上回饋股東（原話："at least 55% to 65% of free cash flow to shareholders"）
- 2026-07-08｜CFO｜capital_allocation：Q3 季度股利調升 0.02 美元至 0.16 美元（原話："quarterly dividend by $0.02 to $0.16 per share"）
- 2026-07-08｜CEO｜product：擴大後的可觸及市場（TAM）貢獻約三分之一營收成長（原話："roughly 1/3 of our top line growth in the quarter"）
- 2026-07-08｜CEO｜product：CEO 稱轉向全身丹寧生活風格使可觸及市場擴大 15 倍（原話："our addressable market by the tune of 15x."）
- 2026-07-08｜CEO｜product：CEO 引述丹寧品類預期成長速度（原話："grow mid-single digits annually through 2030"）
- 2026-07-08｜CEO｜product：Blue Tab 價位帶：下身 200–350 美元（原話："price points like in bottoms from $200 to $350"）
- 2026-07-08｜CEO｜product：CEO 稱 Blue Tab 長期規模可達 1–2 億美元以上（目前規模較小）（原話："there's no reason why this can't be $100 million, $200"）
- 2026-07-08｜CEO｜product：Beyond Yoga 開店處於早期，門市不到 20 家（原話："We have less than 20 stores"）
- 2026-07-08｜CEO｜customer：Signature 價值品牌 H2 預期加速至高個位數到低雙位數（原話："high single digits, low double digits"）
- 2026-07-08｜CFO｜customer：歐洲批發預訂單 H2 成長高個位數，用以支持全年歐洲中個位數成長（原話："high single-digit wholesale preorder growth for H2"）
- 2026-07-08｜CFO｜customer：歐洲 DTC H2（Q3、Q4）預期中到高個位數成長（原話："expect DTC to be mid- to high single digits"）
- 2026-07-08｜CEO｜customer：CEO 說明 Q2 超預期主要來自批發（原話："wholesale actually contributed more to the beat if you will"）
- 2026-07-08｜CEO｜customer：CEO 對中國市場的描述：回到成長的初步跡象（原話："we're encouraged by a return to growth and improving"）
- 2026-07-08｜CEO｜competition：CEO 針對促銷環境回應：Levi's 線上減少促銷、全價銷售增加（原話："more full-price selling"）

### 問答異常語氣（迴避／改口／保留）
- LEVI_Q2_2026_Earnings_Call_20260708.md｜問：Vasilescu 問 Signature 前季高十位數、本季僅低個位數，是否反映價值型消費者疲弱｜答法：CEO 改以上半年合計 +9% 與下半年預期回答，未直接說明 Q2 低個位數的原因；CFO 於後段稱「largely timing」
- LEVI_Q2_2026_Earnings_Call_20260708.md｜問：Boruchow 問營收超預期約 300 基點、營業利潤率僅達指引高端的流量轉換不足｜答法：CFO 回應轉向毛利率、SG&A 三分之一來自匯率與上半年調整後口徑，未直接量化流量轉換缺口
- LEVI_Q2_2026_Earnings_Call_20260708.md｜問：Toscano 問上季所述 3,500 萬美元關稅成本利益與 0.07 美元 EPS 是否已在 Q2 顯現、Q3 預期｜答法：CFO 稱 Q2 邊際、Q3 少量，未給數字；關稅退款 8,000 萬美元稱「substantial」但表示尚未決定如何處理
- LEVI_Q2_2026_Earnings_Call_20260708.md｜問：Kogan 追問季初至今（QTD）表現是接近 Q2 還是符合 Q3 指引 4%–5%｜答法：CFO 表示不提供季中更新，僅稱趨勢支持 Q3 與全年指引、無明顯需求變化，未給量化比較

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

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260522","verdict":"B（衛星候選，分批 + 等回測 Bollinger 中軌 $20.88 或 Fwd PE 13x ~$19.50）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"DTC 通路（含 e-commerce）持續擴張並成為主導通路 + ASP 結構性提升驅動 GM 維持在 60%+","columns":{"2Y 驗證點":"DTC channel 占比從 52% 升至 55% by FY27；DTC comp sales +5% YoY","5Y 驗證點":"DTC 占比達 60% by FY30；e-commerce 占 DTC 30%+","10Y 驗證點":"DTC + 直營實體 占 70%；批發降至 30%","具體數字門檻":"FY26 DTC: 52% → 55% (FY27) → 60% (FY30)；GM 維持 ≥ 60%","信息來源":"Q1 FY26 法說會 + 2024 Investor Day 公司公開目標","漂移觸發條件":"連 2 季 TTM DTC growth"}},{"id":"H2","text":"Beyond Yoga 成功放大成女裝 / athleisure 第二曲線，年化從 $170M 達 $500M by FY28","columns":{"2Y 驗證點":"Beyond Yoga 年化 ≥ $250M by FY27；organic growth ≥ +20% YoY","5Y 驗證點":"達 $500M-$700M by FY30；國際擴張啟動（歐洲 / 亞洲）","10Y 驗證點":"Beyond Yoga 為 $1B+ 獨立次品牌，貢獻集團 12-15% revenue","具體數字門檻":"當前年化 ~$170M（Q1 FY26 $43.3M × 4）→ $250M (FY27) → $500M (FY30)","信息來源":"Q1 FY26 earnings call + 公司分項披露","漂移觸發條件":"連 2 季 organic"}},{"id":"H3","text":"Project Fuel 重組 + 通路升級 + Dockers 出售後，集團 Adj EBIT margin 從 11.3% (FY24) 擴張至 13% (FY28) → 估值倍數從 14.5x → 17x","columns":{"2Y 驗證點":"FY26 Adj EBIT margin ≥ 12%（公司 guidance）；FY27 ≥ 12.5%","5Y 驗證點":"FY28-30 達 13-14%（peer-leading）","10Y 驗證點":"持續維持 13%+ 是 brand-led 的證明","具體數字門檻":"Adj EBIT margin: FY24 11.3% → FY26E 12% → FY28E 13%","信息來源":"FY26 raised guidance + Q1 法說會明確 path","漂移觸發條件":"連 2 季 Adj EBIT margin 年化"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Denim 品類降溫，athleisure / leggings 在 2027-2028 強勢回歸","columns":{"對應假設":"H1, H2","時間尺度標記":"🔥 中期（4-6 季）","監測指標":"Lululemon / Alo / Vuori 季 YoY 成長 vs LEVI 季 YoY；NPD 數據 denim share 走勢","警戒閾值":"連 4 季 LEVI vs Lulu growth spread > 15pp 不利"}},{"id":"R2","text":"Tariff 升級（China 60% / Vietnam 35% / Mexico 25%）超 FY26 guidance 假設","columns":{"對應假設":"H3","時間尺度標記":"⚡ 短期（1-2 季）","監測指標":"季度 GM trajectory；公司 tariff 註腳更新；川普 / 國會貿易政策進展","警戒閾值":"連 2 季 GM YoY 壓縮 > 200bp 且公司歸因 tariff"}},{"id":"R3","text":"Beyond Yoga 整合 / 擴張失敗，第二曲線失速","columns":{"對應假設":"H2","時間尺度標記":"🐢 長期（2+ 年）","監測指標":"Beyond Yoga 季 organic growth；DTC vs wholesale mix；公司是否將其 spin out","警戒閾值":"需 ≥ 50% 機率才砍倉；連 4 季 organic"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":21.75,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEVI_20261012/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
