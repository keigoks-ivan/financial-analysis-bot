你是 stock-analyst **v20 判斷 agent**，標的 CLS（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CLS","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CLS_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CLS_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":5829.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）"}},{"id":"f_kpi1_non_gaap_adjusted_operat","label":"Non-GAAP 營業利益率（adjusted operating margin）","value":8.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":460.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","unit":"百萬美元（利益率 7.9%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）"}},{"id":"f_kpi5_q4_2026","label":"Q4 2026 指引","value":"營收 6,275–6,575 百萬美元；adjusted EPS $3.37–3.57；adjusted 營業利益率中位數 8.7%","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）"}},{"id":"f_kpi6_2026","label":"全年 2026 指引（上調）","value":"營收 21.0B（前 20.5B）；adjusted EPS 11.55（前 11.30）；adjusted 營業利益率 8.4%（不變）；FCF 460 百萬美元（前 600，下調）","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","unit":"全年","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）"}},{"id":"f_kpi7_2027","label":"全年 2027 首次指引","value":"營收 40.0B；adjusted EPS 21.50；adjusted 營業利益率 9.0%；capex 1.5–2.0B","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","unit":"全年","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）"},"note":"consensus FY2 EPS 22.31（來源：numbers_extra.json consensus_revision，2026-10-31 快照）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-26","period":"2026-10-26","unit":"date","basis":"距今 6 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-26"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_cls_gross_margin_pct","label":"CLS 毛利率","value":11.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cls_operating_margin_pct","label":"CLS 營業利益率","value":8.29,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cls_fcf_margin_pct","label":"CLS FCF 利潤率","value":2.99,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_flex_gross_margin_pct","label":"FLEX 毛利率","value":9.5,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_flex_operating_margin_pct","label":"FLEX 營業利益率","value":5.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_flex_fcf_margin_pct","label":"FLEX FCF 利潤率","value":3.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jbl_gross_margin_pct","label":"JBL 毛利率","value":9.23,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_jbl_operating_margin_pct","label":"JBL 營業利益率","value":5.11,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_jbl_fcf_margin_pct","label":"JBL FCF 利潤率","value":3.82,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_sanm_gross_margin_pct","label":"SANM 毛利率","value":9.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sanm_operating_margin_pct","label":"SANM 營業利益率","value":5.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sanm_fcf_margin_pct","label":"SANM FCF 利潤率","value":4.66,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2317_tw_gross_margin_pct","label":"2317.TW 毛利率","value":6.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2317.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2317_tw_operating_margin_pct","label":"2317.TW 營業利益率","value":3.51,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2317.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2317_tw_fcf_margin_pct","label":"2317.TW FCF 利潤率","value":-0.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2317.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_non_gaap_fcf","label":"自由現金流（non-GAAP FCF）","value":127.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）；營業現金流 389.7、資本支出淨額 262.2"}},{"id":"f_kpi4_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":4.6,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）","citation":"公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）；員工 SBC 21.3 百萬美元／GAAP 營業利益 460.0 百萬美元（本 agent 換算；占營收約 0.4%）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":259.12,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-38.41,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":36.66,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.26,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.56 → 11.59）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.45,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（22.21 → 22.31）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":1.94,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（31.38 → 31.99）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":11.59,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":22.31,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":31.99,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.85,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 11.38 → 11.59（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":24.45,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝45.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":45.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.79,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝60.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":60.5,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.63,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝53.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":53.1,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":22.36,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 11.59，分子＝快照價 259.12","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-2932.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 1031.1、現金 3963.1（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":126.11,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":29746.09,"period":"2026-11-03","unit":"USD m","basis":"市值 32678.09 ＋ 淨負債 -2932.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":21039.53,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":40193.48,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.41,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟢","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 254.56 / W52 322.92 / W104 236.11 / W250 113.03 / W250 13週斜率 3.82%"},{"id":"f_ma_w52","label":"52 週均線","value":322.92,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":236.11,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":113.03,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":3.82,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K FY2025 指出 CCS 競爭仍非常激烈，資料中心支出集中於大型雲端/AI 客戶，導致 EMS 積極競標、ODM 加強搶份額。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"resulting in aggressive bidding from EMS providers and increased competition from ODMs as they attempt to gain greater share in this market.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列名競爭對手含 EMS（Benchmark、Flex、Hon Hai、Jabil、Plexus、Sanmina）、ODM（Quanta、Wiwynn、Accton）及 OEM（Arista、Cisco）。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"Our ODM competitors provide product design capabilities and manufacturing services and include Quanta Computer Inc., Wiwynn Corporation, and Accton Technology Corp.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Celestica 8-K 宣布取得第三家超大規模客戶的 1.6T 交換器平台設計與製造案，2027 開始放量。","source":"Celestica 8-K（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000006/cls-20251231prcondensedfs.htm","excerpt":"Celestica has been awarded the program for the design and manufacturing of the 1.6 terabyte switching platform with a third hyperscaler customer. The HPS program is expected to begin ramping production in 2027.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q2 2026 財報摘要稱客戶因 Celestica 複雜產品爬坡能力而將生產移回，並有十個 1.6T 專案進行中（二手部落格，未核原文）。","source":"deltasheets substack CLS FY2026 Q2","url":"https://deltasheets.substack.com/p/cls-fy2026-q2","excerpt":"remain resilient — Continued 400G and 800G growth is overlapping with the 1.6T launch, which may produce a longer and less disruptive upgrade cycle than investors expect. ✅Competitor execution problems are creating share gains — Customers are reportedly moving production back to Celestica because of its ability to ramp complex products reliably, providing growth beyond the expansion of the","as_of":"2026-07-28","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因素：客戶過去與未來可能把業務轉給競爭者、實施 in-source 與 second-source 計畫，或調整供應商集中度。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"Customers have and may also shift business to our competitors, implement in-source and second-source programs, or adjust the concentration of their supplier base.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K：關稅下客戶可能以 insourcing 或轉移給其他供應商來規避成本，影響可能重大。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"whether our customers will continue to bear the cost of the tariffs and/or avoid such costs by insourcing or shifting business to other providers, their impact on the demand for our services, our operations and results for future periods cannot be currently quantified, but may be material.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Q2 2026 10-Q：三位客戶（皆屬 CCS）各占營收 10% 以上，為 32%、17%、14%。","source":"SEC EDGAR 10-Q Q2 2026（經搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000044/cls-20260630.htm","excerpt":"Three customers (all in our CCS segment) individually represented 10% or more of total revenue in Q2 2026 ( 32%, 17%, 14%).","as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#3","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Q4 2025 財報電話會議：管理層稱 Google TPU 專案 Celestica 並非唯一來源，超大型客戶通常保留第二供應商，Celestica 仍為主要來源（搜尋摘要轉述，未逐字）。","source":"MarketBeat Celestica Q4 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/celestica-q4-earnings-call-highlights-2026-01-29/","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 前十大客戶占營收79%（2024 73%、2023 64%）；三家客戶各占10%以上（32%、14%、12%），均在CCS部門。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"We depend on a small number of customers for a substantial portion of our revenue. In the aggregate, our top 10 customers represented 79% of total revenue for 2025, 73% for 2024 and 64% for 2023. In 2025, three customers (all in our CCS segment) individually represented 10% or more of total revenue (32%, 14% and 12%).","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"10-K風險因素：失去任一重要客戶可能對營運結果造成重大不利影響；無法保證降低客戶集中度的努力成功；CCS占2025合併營收74%。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"A decline in revenue from, or the loss of, any significant customer could have a material adverse effect on our operating results, financial position and cash flows, and may increase the variability of our operating results from period to period.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025年Enterprise終端市場營收年減19%，原因為一家超大規模客戶AI/ML運算專案的技術轉換，顯示單一客戶專案轉換已造成實際營收波動。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"Enterprise end market revenue for 2025 decreased $481.7 million (19%) compared to 2024, driven by the technology transition in an AI/ML compute program with one of our hyperscaler customers.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Q2 2026前三大客戶合計占營收63%，最大客戶占32%；集中度與存貨風險上升。","source":"Panabee Celestica Q2 2026 earnings summary","url":"https://www.panabee.com/news/celestica-earnings-q2-2026-report","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Celestica 管理層指引 2027 營收約 400 億美元，約為上調後 2026 年約 210 億美元的兩倍；2028 客戶需求（僅計已award專案）預期較 2027 更高。來源間 2026 指引數字不一（20.5 vs 21.0 十億）。","source":"247wallst: Celestica Q3 2026: $40 Billion Revenue Target Set for 2027","url":"https://247wallst.com/cards/celestica-q3-2026-earnings-cls-01m5wye16dkezbw1zs666n1v2m","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Celestica 稱零組件供應是主要限制，但認為 2026 承諾與 2027 展望已適當避險。","source":"MarketBeat: Celestica Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/celestica-q2-earnings-call-highlights-2026-07-28/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce 2026 年 10 月報導：記憶體供給可能緊到 2028 年後，新產能主要自 2028 起逐步開出。","source":"TrendForce News","url":"https://www.trendforce.com/news/?p=64868","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Global Electronics Association 2026 年 8 月調查：64% 製造商表示零組件僅限量供應或交期延長；多家來源稱緊缺屬結構性、延續至 2027 年底以上，Utmel 則稱非全面短缺而是結構性分化；搜尋未見過剩情境。","source":"Distribution Strategy: electronics supply chain tightens as component shortages lead times worsen","url":"https://distributionstrategy.com/2026/08/electronics-supply-chain-tightens-as-component-shortages-lead-times-worsen/","excerpt":null,"as_of":"2026-08-26","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"被動元件廠 Holy Stone 稱高階被動元件短缺 2027 年可能更明顯，並預期產能今年增 20–30%、2027 年再增 30–40%。","source":"搜尋結果（Holy Stone 引述，未取得原始網址）","url":null,"excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：管理層認為所有未決事項的最終結果不會對合併財務狀況或經營成果造成重大不利影響；經查一手紀錄未列反壟斷訴訟，僅提及稅務事項。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"In the opinion of management, the ultimate resolutions of all such currently pending matters will not have a material adverse effect on our consolidated financial position or results of operations.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因素僅泛稱未來可能出現涉及反壟斷等的法律或監管事項，未揭露具體反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"Additional legal claims or regulatory matters may arise in the future and could involve matters relating to commercial disputes, government regulation and compliance, IP, antitrust, tax, employment or shareholder issues","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：美中貿易爭端已造成關稅上升；Capital Equipment 業務與 CCS 部門過去且可能持續受美國對中國等國的技術/資料出口管制負面影響","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"In addition, international trade disputes with China have resulted in increased tariffs and other measures that have, and may continue to, adversely affect the Company's business. Our Capital Equipment business and our CCS segment have been in prior periods and may continue to be negatively impacted by U.S. technology/data export controls, including controls on cross-border technology/data access, with respect to China and other countries","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：美國對特定先進運算半導體晶片的出口管制已對並持續對 Capital Equipment 與 CCS 造成不利影響；未來衝擊可能重大","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"These actions have adversely impacted and continue to adversely impact our Capital Equipment business and our CCS segment. The future adverse impact of these and/or other actions taken by the governments of either the U.S. or China, or both, or other governments (including in response to continuing tensions), could be material.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：關稅影響無法量化但可能重大，取決於客戶是否持續吸收關稅或轉單","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"Given the uncertainty regarding the scope and duration of these (or further) trade and export actions, whether trade tensions will escalate further, and whether our customers will continue to bear the cost of the tariffs and/or avoid such costs by insourcing or shifting business to other providers, their impact on the demand for our services, our operations and results for future periods cannot be currently quantified, but may be material.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"搜尋未發現 2026 年 Celestica 被列入 Entity List 或遭出口管制執法的來源（僅見例行合規職缺）","source":"WebSearch 結果摘要（無相關來源）","url":null,"excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"公司 8-K（Q2 2026 新聞稿）重申展望假設關稅相較基準日無重大變動","source":"Celestica 8-K 2026-07 新聞稿","url":"https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000043/cls-20260630prcondensedfs.htm","excerpt":"no material changes to tariffs, trade restrictions, customs administration, or related refund or recovery processes, including developments relating to duties imposed under the International Emergency Economic Powers Act of 1977 and any replacement, continuing or retaliatory tariff measures, compared to what are in effect as of July 27, 2026;","as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Celestica 10-Q 風險因素點名美中緊張、中台緊張、俄烏與中東衝突及關稅政策為地緣曝險；據來源摘要，營運據點分布北美、亞洲、歐洲，未見分國產能占比。","source":"SEC Form 10-Q (period ended 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000050/cls-20260930.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026 展望已計入客製矽、記憶體、高層數 PCB 的交期拉長；10-Q 警告短缺可能導致無法及時交貨或須以較差條件向第三方採購。未查到單一來源料件明細。","source":"Celestica 2026 outlook / 10-Q 風險因素（經 itiger、Motley Fool Canada 轉述）","url":"https://www.itiger.com/news/2630092586","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"cmgm.net 稱 Celestica 在泰國（Laem Chabang）、馬來西亞、墨西哥擴產，墨西哥自 2026-01-01 對非 FTA 商品課最高 50% 關稅（第三方產業文章，未核實）。","source":"cmgm.net","url":"https://www.cmgm.net/?p=6684","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收約 $5.83B、年增 83%；CCS 約 $4.9B 年增 102%（占 84%）、ATS $957M 年增 23%；Q4 指引 CCS 約 +110%、ATS 約 +10%（來源間 ATS 指引數字有出入，為二手轉述未對照公司新聞稿）","source":"What Celestica (CLS) Said on Its Q3 Earnings Call (tickerreport)","url":"https://www.tickerreport.com/?p=13643408","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 call：2026 營收指引上調至 $20.5B，預期 2027 成長高於 2026；驅動為超大規模 AI/ML、AMD 機櫃、OpenAI 客製機櫃；800G 2027 續增、1.6T 加速；受限於材料供應","source":"MarketBeat, Celestica Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/celestica-q2-earnings-call-highlights-2026-07-28/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 CCS/ATS 分段營收與 Q4 指引","source":"Circuits Assembly: Celestica Q3 revenue surges 28% YoY","url":"https://circuitsassembly.com/ca/editorial/menu-news/42711-celestica-q3-revenue-surges-28-yoy.html","excerpt":"The company’s Connectivity & Cloud Solutions (CCS) segment led growth, surging 43% to $2.41 billion as customers ramped investment in AI-driven data center infrastructure. Hardware platform solutions within CCS saw a 79% year-over-year jump. The Advanced Technology Solutions (ATS) segment generated $780 million in revenue, down 4% from last","as_of":"2025-10-30","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子列出客戶面臨技術快速變化（含 AI 演進）、替代品出現、低成本與開源 AI 模型競爭，可能限制客戶 AI 相關產品定價；屬一般性風險揭露，未點名特定替代技術取代 CLS 產品。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"Factors that may adversely affect our customers include: rapid changes in technology (including evolving AI technologies); evolving industry standards; seasonal demand; their failure to successfully market, and/or a lack of widespread commercial acceptance of, their products and services; supply chain issues; the emergence of substitutes for products and services;","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"10-K 稱 CLS 投資前瞻產品路線圖與設計能力，與生態夥伴合作定義未來路線，提供機櫃級平台方案。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"We continue to invest in leading-edge product roadmaps and design capabilities aligned with both market standards and emerging technologies.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"CLS 獲得超大規模客戶 CPO（共封裝光學）乙太網路交換器設計與製造專案，採 1.6T 交換晶片，預計 2027 年開始量產爬坡。","source":"Celestica 8-K（2026Q1 新聞稿）","url":"https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000030/cls-20260331prcondensedfs.htm","excerpt":"The switch, optimized for AI scale out networks, will utilize 1.6 Terabit switch silicon, leveraging co-packaged optical interconnects, and liquid cooling technology. The HPS program is expected to begin ramping production in 2027.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q1 2026 財報電話會議摘要稱，1.6T 網通與 CPO 轉換驗證 Celestica 向價值鏈上游、成為先進超大規模客戶共同設計夥伴的方向","source":"Yahoo Finance, Celestica Q1 2026 earnings summary 'Strategic Performance Drivers'","url":"https://finance.yahoo.com/markets/stocks/articles/celestica-inc-q1-2026-earnings-123000989.html","excerpt":"validates Celestica's move up the value chain as a sophisticated co-design partner for advanced hyperscalers","as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2026年3月 Celestica 與 AMD 宣布合作，將 Helios 機櫃級 AI 平台推向市場（平台化/共同設計）","source":"WebSearch result (Celestica/AMD announcement)","url":"https://letsdatascience.com/news/celestica-shifts-toward-ai-infrastructure-co-design-posts-st-8d0a4fa4","excerpt":"announced a strategic collaboration to bring the new \"Helios\" rack-scale AI platform to market","as_of":"2026-03-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"第三方評論稱 Celestica 由 EMS 轉向 ODM（評論性來源、未經公司文件證實；查無正式 go-to-market 或通路重組公告）","source":"Seeking Alpha / 聚合評論（搜尋摘要）","url":"https://seekingalpha.com/article/4859162-celestica-when-engineering-becomes-the-moat","excerpt":"transitioning its business model from that of an EMS company to that of an Original Design Manufacturer, or ODM","as_of":"2026-06-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 報告（2026-07-27）公司將全年指引上調至營收約 $20.5B、調整後 EPS $11.30，高於當時共識約 $19.2B／$10.13；Q3 指引 EPS $2.88–3.08 高於共識 $2.65（MarketBeat 數字）","source":"MarketBeat: Celestica releases FY 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/celestica-nysecls-releases-fy-2026-earnings-guidance-2026-07-27/","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"4 月 Q1 報告將 2026 指引上調至營收 $19.0B、調整後 EPS $10.15（原營收 $17.0B）；報告後股價跌約 16%，RBC 指出超預期幅度小於近期趨勢","source":"Celestica 8-K Q1 2026 / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000030/cls-20260331prcondensedfs.htm","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"StockAnalysis 彙整（含 2026-10-27 動作）：22 位分析師共識 Strong Buy，平均目標價 $466.34，區間 $375–$550；MarketBeat 另示 23 位平均 $437、高 $510、低 $300（各源 as-of 不同）","source":"StockAnalysis CLS forecast","url":"https://stockanalysis.com/stocks/CLS/forecast/","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill 顯示 FY2026 EPS 最新共識估計 $11.35（19 位分析師，記錄於 2026-10-24），貼近公司指引 $11.30；下一季營收估計 3 個月內上修 9.58%","source":"Chartmill CLS estimates","url":"https://www.chartmill.com/stock/quote/CLS/estimates","excerpt":null,"as_of":"2026-10-24","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：無重大訴訟，管理層認為待決事項不致對財務有重大不利影響","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"In the opinion of management, the ultimate resolutions of all such currently pending matters will not have a material adverse effect on our consolidated financial position or results of operations.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-08-05 公開增發 9,677,419 股，每股 $310，淨額約 $33.9 億（股權融資事件，非 M&A）","source":"SEC EDGAR 8-K Item 1.01 (2026-08-07)","url":"https://www.sec.gov/Archives/edgar/data/1030894/000110465926092676/tm2621135d2_8k.htm","excerpt":"the offering, issuance and sale by the Company of 9,677,419 common shares, without par value, of the Company (the “Common Shares”), at an offering price of $310.00 per Common Share (the “Offering”).","as_of":"2026-08-07","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-04-27 修訂信用協議：循環額度由 $7.5 億增至 $17.5 億，到期延至 2031 年 4 月","source":"SEC EDGAR 8-K Item 1.01 (2026-04-28)","url":"https://www.sec.gov/Archives/edgar/data/1030894/000110465926049818/tm2612871d1_8k.htm","excerpt":"increase the commitments under the Company’s revolving credit facility (“Revolver”) from $750.0 million to $1,750.0 million","as_of":"2026-04-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"ems_utilization_capex_cycle#0","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"-","claim":"Celestica 2026 capex 預期約 $1 億美元級的 $10 億（約營收 6%），2025 為 $2.01 億；新產能 2026–2027 陸續開出，含德州 Richardson 擴建與 Fort Worth 新廠（2027 上線）、泰國擴建","source":"Celestica Q4 2025 earnings call highlights / 8-K (search summary)","url":"https://finance.yahoo.com/news/celestica-q4-earnings-call-highlights-023916385.html","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ems_utilization_capex_cycle#1","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"0","claim":"Celestica 宣布在 Fort Worth AllianceTexas 興建逾 100 萬平方呎園區，預計創造約 1,700 個全職職位","source":"Evertiq: Celestica to build one million square foot campus in Fort Worth","url":"https://evertiq.com/news/2026-06-03-celestica-to-build-one-million-square-foot-campus-in-fort-worth","excerpt":null,"as_of":"2026-06-03","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"ems_utilization_capex_cycle#2","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"0","claim":"Richardson 新增 343,000 平方呎租約，約 2 年內資本投資約 $3 億","source":"Community Impact: Celestica expanding Richardson footprint to 1 million sq ft","url":"https://communityimpact.com/dallas-fort-worth/richardson/business/2026/06/17/tech-company-celestica-expanding-richardson-footprint-to-1-million-square-feet/","excerpt":null,"as_of":"2026-06-17","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"ems_utilization_capex_cycle#3","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"0","claim":"Motley Fool Canada 稱長交期矽料訂單多為不可取消不可退款；毛利擴張取決於高毛利專案放量與產能利用","source":"Motley Fool Canada: Real revenue, real margins inside Celestica's AI hardware boom","url":"https://www.fool.ca/2026/08/24/real-revenue-real-margins-inside-celesticas-ai-hardware-boom/","excerpt":null,"as_of":"2026-08-24","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#0","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"+","claim":"Celestica 2026 招股補充文件揭露 non-GAAP adjusted ROIC 46.5%（LTM，平均淨投入資本 $2,659.7M）；未調整營業利益基礎 ROIC 51.5%","source":"SEC Form 424B5 Celestica 2026","url":"https://www.sec.gov/Archives/edgar/data/0001030894/000110465926091994/tm2621135d3_424b5.htm","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#1","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"+","claim":"Celestica 2026 Q2 現金循環天數 47 天，較去年同期改善 19 天、較上季改善 8 天（來源為法說會逐字稿）","source":"Celestica Q2 2026 earnings call transcript (earningswhispers)","url":"https://earningswhispers.com/transcript/CLS/Q22026","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#2","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"0","claim":"EETimes 2026-03-31 文章估計大中型 EMS 公司 ROIC 約 20%（超過 S&P Industrials 一倍以上），20 家 EMS 綜合現金循環 33 天；底層分析師未明（單一摘要來源）","source":"EE Times","url":"https://www.eetimes.com/?p=1124845","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#3","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"+","claim":"OpenCapital 聚合站列資產週轉率：Celestica Q1 2026 約 2x，Flex 1.4x、Jabil 1.6x（無日期單一快照；TipRanks 另列 1.61、ROIC 16.10%，定義不一）","source":"OpenCapital CLS asset turnover","url":"https://www.opencapital.sh/stocks/cls/metrics/asset_turnover","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K 稱過往證券集體訴訟與股東衍生訴訟已和解或駁回；Item 3 無重大訴訟","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm","excerpt":"including securities class action and shareholder derivative lawsuits which have been settled or dismissed","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 12 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"CLS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":11.46,"operating_margin_pct":8.29,"fcf_margin_pct":2.99,"rd_intensity_pct":0.93},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"FLEX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.5,"operating_margin_pct":5.44,"fcf_margin_pct":3.32,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"JBL","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.23,"operating_margin_pct":5.11,"fcf_margin_pct":3.82,"rd_intensity_pct":0.08},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL","as_of":"TTM ending 2026-08-31（4季加總）"}},{"name":"SANM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.01,"operating_margin_pct":5.49,"fcf_margin_pct":4.66,"rd_intensity_pct":0.26},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"2317.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":6.12,"operating_margin_pct":3.51,"fcf_margin_pct":-0.46,"rd_intensity_pct":1.31},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2317.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"CLS"},"financial_history":{"ticker":"CLS","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":7250000000.0,"revenue_yoy_pct":null,"gross_margin_pct":8.96,"operating_margin_pct":4.08,"net_income":180100000.0,"diluted_eps":1.18,"free_cash_flow":102100000.0,"fcf_margin_pct":1.41,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":7961000000.0,"revenue_yoy_pct":9.81,"gross_margin_pct":9.47,"operating_margin_pct":4.4,"net_income":244400000.0,"diluted_eps":2.03,"free_cash_flow":201100000.0,"fcf_margin_pct":2.53,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":9646000000.0,"revenue_yoy_pct":21.17,"gross_margin_pct":10.72,"operating_margin_pct":6.41,"net_income":428000000.0,"diluted_eps":3.61,"free_cash_flow":303000000.0,"fcf_margin_pct":3.14,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":12390900000.0,"revenue_yoy_pct":28.46,"gross_margin_pct":12.06,"operating_margin_pct":8.64,"net_income":832500000.0,"diluted_eps":7.16,"free_cash_flow":458300000.0,"fcf_margin_pct":3.7,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CLS/CLS_Q2_2026_Earnings_Call_20260728.md）

# Q2 2026 Earnings Call
2026-07-28

Q2 2026 Earnings Call
Celestica Inc. | Earnings Calls | 2026-07-28
Operator (Operator)
Hello, everyone. Thank you for joining us, and welcome to the Celestica Second Quarter 2026 Financial
Results and Conference Call. [Operator Instructions]
I will now hand the conference over to Matthew Pallotta, Head of Investor Relations. Please go ahead.
Matthew Pallotta (Executives)
Good morning, and thank you for joining us on Celestica's Q2 2026 Financial Results Conference Call.
On the call today, we have Rob Mionis, Chair of the Board and Chief Executive Officer; and Mandeep
Chawla, Chief Financial Officer. Please note that during the course of this call, we will make forward-
looking statements, including statements relating to the future performance of Celestica, our business
outlook, guidance for the third quarter of 2026, our 2026 annual outlook and anticipated trends in our
industry and their anticipated impact on our business.
These are based on management's current expectations, forecasts and assumptions as of July 27. These
forward-looking statements are subject to risks and uncertainties that could cause actual results to
differ materially from our expectations and their potential impact on our results cannot be reliably
predicted at this time. For identification and discussion of the material assumptions, risks and
uncertainties, please refer to our public filings with the SEC and on SEDAR+ as well as the Investor
Relations section on our website.
We undertake no obligation to update these forward-looking statements unless expressly required to do
so by law. In addition, during this call, we will refer to various non-GAAP financial measures. We have
included in our earnings release found in the Investor Relations section of our website, a discussion of
those non-GAAP financial measures and a reconciliation to the most comparable GAAP measures.
Unless otherwise specified, all references to dollars on this call are to U.S. dollars, all per share
information is based on diluted shares outstanding and all references to comparative figures are a year-
over-year comparison.
With that, I will now turn the call over to Rob.
Robert Mionis (Executives)
Thank you, Matt, and good morning, everyone, and thank you for joining us on today's call. As we cross
the midyear mark, we continue to see sustained and accelerating momentum across our portfolio. In
the second quarter, we delivered revenue of $4.7 billion and adjusted EPS of $2.54, both exceeding the
high end of our guidance ranges. This performance was backed by an adjusted operating margin of
8.2%, a new high for the company. These results reflect strong operational execution across both
segments alongside record demand from our CCS customers. Within CCS, we continue to expand with
leading hyperscale customers through close alignment on multiyear capacity road maps.
Rapid progression in technology upgrade cycles in networking and AI compute are driving broad
demand, and we are in the process of ramping a number of significant new programs expected to

launch in the second half of the year and into 2027. At the same time, our ATS segment continues to see
strong profitability improvements alongside solid revenue growth during the quarter.
Before I provide an update on our longer-term business outlook, I would like to turn the call over to
Mandeep, who will take us through our Q2 results and Q3 guidance. Mandeep, over to you.
Mandeep Chawla (Executives)
Thank you, Rob, and good morning, everyone. Revenue in the second quarter was $4.70 billion, up
62% and above the high end of our guidance range as strong demand and solid operational execution
led to higher-than-expected revenue in our ATS segment and both of our CCS end markets. Our non-
GAAP operating margin was 8.2%, up a robust 80 basis points with solid margin expansion in both
segments, resulting primarily from improved operating leverage. Our adjusted earnings per share was
$2.54, exceeding the high end of our guidance range and an increase of $1.15 or 83%.
Moving on to some additional metrics. Adjusted gross margin was 11.5%, down 20 basis points, largely
due to mix in our CCS segment. Our second quarter adjusted effective tax rate was 20%. Lastly, our
strong earnings growth and disciplined working capital management led to adjusted ROIC of
approximately 55%, higher by 20 percentage points compared to the prior year. Turning now to our
segment performance. Revenue in our CCS segment was $3.81 billion, up 84% compared to the prior
year period, driven by very strong growth in both our communications and enterprise end markets. In
the second quarter, the CCS segment accounted for 81% of total company revenue.
Our communications end market revenue was up 62%, higher than our outlook of approximately 50%,
primarily driven by growth in our 800G networking switch programs, complemented by continued
strong demand in our 400G programs. Revenue in our enterprise end market was up by 167%, well
above our outlook of approximately 130%, driven by the accelerated ramp of an AI/ML compute
program with a hyperscaler customer and supported by stronger-than-expected demand in storage
programs. In our HPS business, revenue was $1.9 billion in the second quarter, representing growth of
58%, driven by ramping 800G switch programs across multiple hyperscaler customers.
Our HPS business accounted for 41% of total company revenue in the second quarter. ATS revenue for
the quarter was $888 million, higher by 8% and above our outlook of a mid-single-digit percentage
increase. The solid performance was driven by revenue growth in each of our businesses. Our ATS
segment accounted for 19% of total company revenue in the second quarter. Moving on to segment
margins. Our CCS segment margin was 8.7% in the second quarter, an improvement of 40 basis points,
driven by strong operating leverage from significantly higher volumes.
Our ATS segment margin was 6.3%, up 100 basis points year-to-year, driven by operating leverage and
higher engineering-driven product mix. In the second quarter, 3 customers each accounted for 10% or
more of total revenue, accounting for 32%, 17% and 14%, respectively. Turning to working capital. At
the end of the second quarter, our inventory balance was $3.4 billion, a sequential increase of $0.7
billion and higher by $1.5 billion compared to the prior year, driven by continued scaling to support
significant growth and upcoming program ramps in our CCS segment as anticipated.
Cash cycle days for the quarter were 47, representing a 19-day improvement over the prior year and an
8-day improvement sequentially. Moving on to cash flows. We generated $147 million of free cash flow
in the second quarter and $285 million year-to-date. Our capital expenditures were $264 million or
approximately 5.6% of revenue compared to 1.1% of revenue in the prior year quarter. Consistent with

our prior outlook, our full year 2026 capital expenditure guidance remains unchanged at approximately
$1 billion.
Our capital expenditure investments are intended to support the significant anticipated growth from
currently ramping and awarded programs. They are underpinned by strong demand visibility and close
alignment on multiyear capacity planning with our key customers. At the end of the second quarter, our
cash balance was $536 million, while our gross debt was $740 million, resulting in a net debt position
of $204 million. We had no draw outstanding on our revolver at the end of the quarter. Our gross debt
to non-GAAP trailing 12-month adjusted EBITDA leverage ratio was 0.5 turns, an improvement of 0.1
turns sequentially and 0.4 turns versus prior year. Our cash balance, in combination with our recently
upsized revolver provides us with approximately $2.3 billion of available liquidity.
As of June 30, we were in compliance with all financial covenants under our credit agreement. We did
not repurchase shares for cancellation during the second quarter. While we continue to approach share
repurchases on an opportunistic basis, our highest priority at this time is to reinvest in our business to
support the unprecedented growth we anticipate over the coming years. We maintain a disciplined
approach to capital allocation, deploying to the highest return opportunities in order to drive long-term
shareholder value. Now moving on to our guidance for the third quarter. Third quarter revenue is
projected to be between $5.25 billion and $5.55 billion, representing growth of 69% at the midpoint.
Adjusted earnings per share is anticipated to be between $2.88 and $3.08, representing an increase of
$1.40 at the midpoint or 89% growth compared to the prior year. Assuming the achievement of the
midpoint of our revenue and adjusted EPS guidance ranges, our adjusted operating margin is expected
to be 8.4%, which would represent an increase of 80 basis points. We anticipate our adjusted effective
tax rate for the third quarter to be approximately 20%. Finally, let's review our revenue outlook for each
of our end markets. In our CCS segment, we expect revenue in our communications end market to grow
approximately 60%, driven primarily by hyperscaler-led growth in 800G programs as well as the
commencement of mass production ramps in our first 1.6 terabit programs.
In our enterprise end market, we expect growth of approximately 190%, driven in large part by the
continued ramp in hyperscaler AI/ML compute as well as improved demand in storage. In our ATS
segment, we anticipate revenue to be up in the mid-teens percentage range, driven primarily by strong
demand in our capital equipment business as well as by new program ramps in our other businesses.
With that, I will now turn the call back over to Rob to provide an update on our 2026 annual financial
outlook and additional color on the latest developments in our business.
Robert Mionis (Executives)
Thank you, Mandeep. We are once again raising our full year 2026 annual outlook, driven by our strong
first half performance and strengthening second half customer forecast supported by improved
component supply. Our revenue outlook increases from $19 billion to $20.5 billion, representing very
strong growth of 65%. We are also raising our adjusted EPS outlook to $11.30, up from $10.15,
representing growth of 87% Reflected in our outlook is full year adjusted operating margin of 8.4%,
higher than our previous outlook of 8.1%. Finally, we are increasing our free cash flow outlook for 2026
from $500 million to $600 million, which includes approximately $1 billion in planned CapEx.
Our outlook maintains a prudent view on component availability and the timing of new program
ramps. Looking beyond 2026, our visibility is very strong. This is driven by multiyear global capacity

alignment with our key customers, along with improved component supply planning to effectively
manage extended component lead times. For 2027, as a result of exceptionally strong customer
demand and new program wins, we expect our revenue growth rate to accelerate as compared to the
65% growth expected in our 2026 annual outlook. Furthermore, as we continue expanding our adjusted
operating margins, we anticipate our adjusted EPS growth rate to outpace our revenue growth. We look
forward to providing a detailed full year outlook for 2027 later this year.
Now moving on to discuss the business outlook for our segments and beginning with CCS. Based on our
updated 2026 annual outlook, we now anticipate CCS revenue to grow by approximately 85%. In
Communications, we expect strong momentum to continue through the rest of the year, driven by
continued growth in 800G Ethernet switch programs alongside the launch of mass production for 1.6T
programs with 2 hyperscaler customers beginning in the third quarter. In 2027, we expect that the
combination of continued growth in 800G volumes alongside the acceleration of 1.6T ramps across our
customer base will drive very strong growth. Within our enterprise end market, our outlook for the
second half of 2026 remains exceptionally robust as we see strengthening demand in our AI compute
portfolio.
We expect to continue this strong growth into 2027, driven by the ramp of multiple compute programs.
Additionally, later this year, we expect to commence initial deliveries of custom racks for a digital
native customer, whom we are pleased to share is OpenAI. In our role as a strategic systems partner,
Celestica will collaborate with OpenAI and Broadcom in support of their multigenerational custom
accelerator road maps, beginning with the Jalapeño accelerator with mass production planned in 2027.
As OpenAI's custom accelerator road maps advance towards future generations, Celestica will continue
to provide its expertise to support their multi-gigawatt scale deployments. Now moving on to our ATS
segment. We are updating our full year outlook, which now calls for revenue growth of approximately
10% Growth is accelerating in the second half of the year, largely driven by sequential growth in our
capital equipment business, where stronger wafer fab equipment demand tailwinds are anticipated to
continue into 2027. This momentum will be complemented by continued growth across the rest of our
portfolio, supported by new program ramps.
We also remain positive on the trajectory of strengthening ATS segment margins. We anticipate that
this momentum will continue as the portfolio benefits from both improving mix and leverage from
returning revenue growth. Looking ahead, our demand pipeline remains at record levels. Across key
customer programs, we continue to see improving multiyear visibility into AI infrastructure
investments, which reinforces our confidence in our growth trajectory through the remainder of 2026
and into 2027. Combined with strong operational execution and disciplined capital allocation, we
believe we are well positioned to expand margins, deliver EPS growth and return strong long-term
value for our shareholders.
With that, I will now turn the call over to the operator to open the line for questions.
Operator (Operator)
[Operator Instructions] Your first question comes from the line of Tim Long with Barclays.
Timothy Long (Analysts)
Yes, one question, and then I'll have a follow-up after. Maybe I know you don't want to get too into the
2027, but the acceleration of growth is obviously pretty meaningful. So we're looking at, I don't know,

$13 billion or so of incremental revenues. Could you just maybe at a high level, talk about how much
those new programs are contributing? I think there's the OpenAI that you mentioned in 2 others, AMD
and the 1.6T CPO switch. So if you could just give us a little bit of color on kind of new versus existing?
And then I'll have a follow-up right after that.
Robert Mionis (Executives)
Sure, Tim. What we're seeing in 2027, first as we see scaling of 800G programs. and also the scaling of
the 1.6T switch programs. And this is complemented on top of very strong growth or I should say,
continued growth of 400G. So 400G, as we go from '26 to '27 is remarkably resilient. Then on top of
that, after 2027, we have ramps of next-generation AI/ML compute programs. And then to your
question, we have our new custom rack deployments with OpenAI and AMD.
Both are several billion-dollar opportunities that we see in 2027, specifically on the AMD Helios scale-
up platform, the pipeline on that program continues to grow. And again, that's a multibillion-dollar
program in 2027. On top of that, ATS is also really coming into its own. Its margins are improving and
the growth fueled by capital equipment is really adding fuel to the fire for 2027.
Timothy Long (Analysts)
Okay. Great. Great. And if I could just follow up on gross margin. It seems like a solid performance in
the quarter. Maybe just a little bit how we should think of that as the complexion of the business
changes. A lot of these newer programs are pretty scale and some of them, I think they're mostly HPS.
So just a high level on profitability and how HPS can impact that over the next year?
Mandeep Chawla (Executives)
Yes. Tim, it's Mandeep here. So we're pleased with where gross margin is coming in at right now, up a
little bit sequentially. And we do believe that we should be able to maintain being around the mid-11s as
we go through 2026. As we look into 2027, still dialing in some of the specifics, to your point, we do
have some positive benefits coming through. We're going to be seeing accelerated growth in HPS the
ramping of network switches, which are primarily HPS. And so that definitely helps us. We're still
working through the mix impacts as we look at the rest of the portfolio. But what I'll point you back to
then is operating profit. We have a lot of confidence right now that we will see operating profit
expansion for yet another year as we go into next year.
Operator (Operator)
[Operator Instructions]
Your next question comes from the line of Joseph Cardoso with JPMorgan.
Joseph Cardoso (Analysts)
Maybe as a follow-up to the revenue guidance, it's great to see the increase here for this year and next
year as well. But maybe just given the context of the broader supply constraints we're seeing in the
industry, both perhaps direct and indirect, can you maybe talk to how those have tracked through the
quarter or the quarter-to-date? And to what extent are they acting or still acting as limiters to the
guidance? Are you seeing it kind of materialize worser? Or are you seeing it more easier to navigate?
Robert Mionis (Executives)

Thanks, Joe. Yes, we performed better than we expected this quarter. The team has really been
outstanding in navigating a very tight supply chain. Demand across the AI data center infrastructure
continues to outpace the global component supply. However, in our '26 commitments and our '27
outlook, we are appropriately hedged. And frankly, we find it manageable. We're continuing to work
closely with our customers and our suppliers to secure even improved capacity as we move into 2027.
And it's an ongoing process.
But ultimately, the positive side of this is that the supply tightness that we're seeing really reflects the
strength and the multiyear durability of the underlying demand pipeline that we see. And frankly, the
unprecedented levels of demand visibility is enabled by extended lead times. So this supply chain
constraint is really helping us do a better job of planning with our suppliers and with our customers,
and it's giving us confidence in our longer-term outlook.
Mandeep Chawla (Executives)
Just one thing to maybe add to that would be, if you just look at it holistically through '26 and through
'27, we have the capacity in place to execute the demand that's there for 2026. We have the capacity
plans in place to execute the demand in 2027. However, the constraint is really around materials. And
so we've taken that into our -- into consideration when providing the figures that we're providing, but
the demand does exceed the revenue figures that we've been sharing.
Operator (Operator)
Your next question comes from the line of Ruben Roy with Stifel.
Ruben Roy (Analysts)
Rob, to start with, could you maybe spend a minute on how you're thinking about 1.6T ramps? There's
been a lot of discussion about pace of those ramps, et cetera. Obviously, 800 gig is continuing to do well
for you guys, and you're talking about continued expansion into '27. So I'm just wondering if you could
maybe talk about what customers are thinking in terms of 1.6T ramps and if you think there's a
crossover coming in '27? Or if not, if you can give us how you're thinking about the mix, that would be
helpful.
Robert Mionis (Executives)
Sure. So 1.6T really starts ramping coming into its own in the back half of '26 and really surging in
2027. Again, we have 10 active 1.6T programs in the mix, and they'll start really picking up in 2027 on
top of some very strong growth, year-over-year growth in 800G. On top of that, the pipeline for 1.6T in
terms of sales pipeline is continuing to grow, and we're probably will end up booking some additional
awards here in the coming quarters. And there's some programs still in development that will also start
kicking in, in the latter half of 2027.
Ruben Roy (Analysts)
I know I only have one question, but if you could maybe just comment on CPO as well. I know you have
the one win. Is that sort of on track with the way you're thinking about timing? And any additional
customer discussions around CPO? That's all I have.
Robert Mionis (Executives)

The samples for that CPO win will come out in the first half of '27, and mass production for that
program will start in the second half of 2027. And we continue to work with that customer on next-
generation technologies to kind of further their technology road map.
Operator (Operator)
Your next question comes from the line of Michael Ng with Goldman Sachs.
Michael Ng (Analysts)
I just wanted to ask for a few more details on the 2027 revenue growth guidance improvement. Could
you just talk a little bit about what changed most significantly to raise the growth outlook? Was it more
on the communications side or the enterprise side? Any specific programs or deals that kind of give you
that confidence and visibility to increase the outlook at this stage of the year?
Robert Mionis (Executives)
Sure. So just some 90 days ago, our AI/ML compute demand has significantly increased for 2026 and
also leading into 2027. That has given us confidence. The demand pipeline for the next-generation
racks for AMD next-generation racks also continue to increase. And then our base demand across
networking for our 800G programs has also just dramatically increased for 2027. As Mandeep
mentioned earlier, we do have the capacity to support that demand, and hence, we raised our outlook
for 2027.
Mandeep Chawla (Executives)
Michael, maybe I'll just add on to Rob's comments. We've talked about this a little bit over the last 6
months or so, but the capacity planning discussions we're having are allowing us to have some very
forward-looking conversations with our customers. We're having demand conversations in 2027 for
2028 and in some cases, even for 2029. And to Rob's point, the demand is continuing to strengthen.
The forecast visibility in many cases is widening. But really, what's changed in the last 3 to 6 months is
you got to start ordering the materials. And with extended lead times now with some products being
well above 52 weeks, we really needed to solidify the demand outlook for next year. And so with those
orders now in place, it gave us just that one extra level of confidence to be able to share the numbers
that we did.
Operator (Operator)
[Operator Instructions]
Your next question comes from the line of Ruplu Bhattacharya with Bank of America.
Ruplu Bhattacharya (Analysts)
I have one question, but as you may have guessed, it's going to be in 2 parts. The first question is, Rob,
you're guiding very strong growth for fiscal '27, much stronger than we had expected. What are some of
the -- what are 2 or 3 of the key assumptions that are embedded in this outlook that investors should
monitor over the next 6 months or so? I'm trying to get at what are some of the risk factors that
investors should keep in mind? And the follow-up for Mandeep, because of all the geopolitical
uncertainty, are you getting requests for more regional manufacturing? And do you see this as an
opportunity to expand in North America versus in Southeast Asia and other places?

Robert Mionis (Executives)
Sure. In terms of the risk factors, they always continue to be the same. It's largely at this stage of the
game around continued material supply and continuity of supply. That being said, as Mandeep
mentioned earlier, the lead times for components are quite long. And our suppliers -- I mean, our
customers have placed noncancelable, nonrefundable orders for long lead silicon, which gives us
confidence for that. We've also have supply agreements on hard to find components such as memory
and PWBs and things along those lines.
So we think we've effectively managed the risk on the downside. In terms of the upside, just
unprecedented demand increases across the board, specifically in AI/ML compute and also in
networking. We feel like we're gaining share across the board, driven by our ability to execute and
execute well at scale, and that's also enabling us to provide a solid 2027 guidance. Again, for 2027, we
feel that it's continuing to unfold, and we're refining it. So we're not placing a ceiling on the upside at
this time, but the guidance that we gave, we feel very comfortable at this stage.
Mandeep Chawla (Executives)
And Ruplu, just to also address your question around the operational footprint. And I'll tie back to
dollars as well because I'm sure that this is top of mind as well. We still think the $1 billion of CapEx for
this year is the right number. It may move around a little bit just based on the timing of payments. We
think the $1.5 billion is a good placeholder still for next year. We'll give a number in October because if
that number is to go up and it may, it will really be reflective of the demand that we're seeing in 2028.
So then when you look at where that capacity is being deployed, it really is quite global in nature.
We are adding capacity in Thailand, which is one of our flagship locations, supporting a number of the
highest growth customers, just a fantastic execution track record in Thailand. But we're making
expansions in Japan at the request of our customers as well and moving some switching business
Japan. But we're making significant investments in the United States. In particular, in Richardson,
Texas, we're expanding our existing footprint. In Fort Worth, Texas, we are already bringing online
some new capacity and more capacity will come online next year as well. And so we're finding that our
customers right now are looking for an equal amount of growth in Asia as well as in the United States.
Operator (Operator)
Your next question comes from the line of David Vogt with UBS.
David Vogt (Analysts)
I have more of a thematic philosophical question for you guys. When you think about the demand that
you're seeing that I think you called out, Rob, as unprecedented demand over the next several years,
can you help us understand -- I understand all the programs that are ramping 800, 1.6 CPO, but are the
bands wider in terms of what you're hearing from your customers? And what I mean by that is, are you
seeing sort of a wider range of potential outcomes from your customers given the supply chain
uncertainty? And outside of CapEx, maybe Mandeep, what kind of capital support or working capital
support are your customers asking for at this part of the cycle, given how strong demand is and
potentially some limitations on capital at some of your potential customers going forward?
Robert Mionis (Executives)

I would say earlier in the year, as the demand started picking up, our customers' demand signals are
very, very dynamic. Just to use an analogy, I think all our customers threw a bunch of spaghetti on the
wall and they try to figure out what would stick or not. And then after the supply chain, the broad
supply chain try to understand its true capacity and what it could scale, the demand signals then
normalized and strengthened around the theory of constraints, if you will.
So right now, what we're really just seeing is a very constant and growing set of demand signals from
our customers. And hence, we've been working methodically with our suppliers to expand it. So I think
the noise has calmed down quite a bit. Our customers, again, continue to want more than the supply
chain could supply, but that is, again, not perishable demand. It's just giving us more visibility into the
future when we're able to responsibly scale to achieve it.
Mandeep Chawla (Executives)
And David, to your question around the engagement with our customers, look, we're servicing the best
customers in the world right now. We have very open and detailed conversations around balance sheet
strength on both sides, ensuring that the commitments that we're making are supported by strong
credit to be very kind of blunt about it. To be equally blunt, we're not a bank. So we don't go and fund
our customers' ability to grow. And so we feel comfortable that when we're signing up for programs that
we have the right contractual terms in place to protect both sides.
We do work very collaboratively with our customers, long-term forecasting and increasing levels of
visibility is where it really starts. In some cases, we have binding forecasts that go out 12 to 18 months
in order to secure the materials. We do work with our customers on specialized equipment or
nonrecurring expenses to be covered by them, and we'll cover the majority of the rest of it. But really,
we take a dynamic approach by customer based on their individual situations, but we have no concerns
across our customer base at this time.
Operator (Operator)
Your next question comes from the line of Thanos Moschopoulos with BMO Capital Markets.
Thanos Moschopoulos (Analysts)
On AMD Helios, there's obviously been a lot of programs announced. Could you give us some color in
terms of at this point, how many you're involved in, what may represent potential opportunities? And
to what extent you would expect some Helios revenue to start kicking in later this year?
Robert Mionis (Executives)
Sure, Thanos. So again, for the AMD Helios, we're the R&D design and manufacturing partner for the
scale-up networking switch. And this switch forms the interconnect backbone for the entire rack. We
are shipping samples towards the end of 2026, and the ramp begins in earnest in the first half of 2027.
Again, this rack has interest and demand and orders from several customers and the pipeline is
growing. At this stage of the game in 2027, we view this as a multibillion-dollar pipeline and growing.
Thanos Moschopoulos (Analysts)
And should we assume that you're involved in most of those programs? Or is it up to hyperscaler to
determine the configuration of the [ rack ]?

Robert Mionis (Executives)
No, we're involved in all of these programs.
Operator (Operator)
Your next question comes from the line of Robert Young with Canaccord Genuity.
Robert Young (Analysts)
I just wanted to dig deeper on the CCS margin outlook. It looks like the non-HPS elements of that
business are tracking at margins approaching HPS. I was curious what the driver is. And if you could
also discuss the margin profile for [ 400 ], which is remaining at higher levels of demand than you
expected and then what it looks like in 800 and 1.6 terabyte going forward? Is it a similar margin
profile? Or is there something to understand there?
Mandeep Chawla (Executives)
Rob, to Look, the CCS business is performing very well from a margin perspective, record margins in
the last quarter, and we think that there continues to be an opportunity to see expansion there. You're
hitting on a couple of different points, but how I would maybe bring it up a level is, are we growing in
HPS or are we not? And the vast majority of our switching programs are HPS, meaning a lot of our
designs incorporated in there, a lot of our know-how, and that does allow us to have that reflected in
price. And so as we see an acceleration of networking growth next year, that will clearly be a benefit.
We're still working through mix impacts. Non-HPS business is not as margin-rich as HPS products. So
we're working through that piece right now. But then the other area that we have very clear line of sight
to is the operating leverage. We will continue to be very disciplined on our OpEx spend, and we do
believe that we're going to see another year of very good operating leverage coming through on the back
of really double-digit productivity across the majority of our sites.
And so CCS is performing very well. Just lastly, I'll talk about [ ATS ]. ATS is really benefiting us as well.
We're really happy to see that the business has returned to growth. We see that growth accelerating in
the back end of this year. We see growth next year as well. But from a margin perspective as well, ATS
just has highest margins in its history at 6.3%. And we think that based on the mix of our portfolio, that
there's an opportunity for expansion there as well as we go into next year. So really multiple
contributors right now to the margin story.
Operator (Operator)
Your next question comes from the line of George Notter with Wolfe Research.
Unknown Analyst (Analysts)
This is [indiscernible] on for George. Can you talk a little bit more about what you're seeing in the scale-
up landscape? Like are there any other scale-up program opportunities beyond Helios? What you guys
are seeing over the next couple of years?
Robert Mionis (Executives)
Yes. On scale up, obviously, there is Helios, but there's also the OpenAI [ rack ] that we're doing with
respect to OpenAI timing. We're starting to deliver samples in 2026. And then that program will ramp

in 2027, well into 2028 as well. We view this revenue opportunity as again, as a multibillion dollar
revenue opportunity from this. Regarding broader scale-up opportunities. Broadly speaking, we have
numerous engagements and discussions with folks to go into scale up. Scale up for us really started
with 1.6T. And as we continue to win awards for integrated [ rack ] systems, we expect this to be a huge
opportunity for us.
Mandeep Chawla (Executives)
Yes. And to add from a customer logo perspective, to Rob's point, we're going to be seeing a lot of scale-
up demand with OpenAI as well as AMD. But we're also winning a number of networking programs
from one of our largest customers that is also in scale up. And so we find this to be really encouraging.
The TAM is expected to grow in scale up between now and the next 3 years quite substantially. And
that's tracking for us because we're seeing it come through in the wins that we have.
Operator (Operator)
Your next question comes from the line of John Shao with TD Cowen.
John Shao (Analysts)
I just wanted to ask about the turnkey versus consignment consideration, especially for new programs
in 2027. So any changes on how you recognize the revenue given some of your peers are choosing more
consignment? And any implications when it comes to OpenAI program given that it's more end-to-end?
Mandeep Chawla (Executives)
John, so the answer is -- maybe I'll start with OpenAI. I think it's fair to assume right now that, that will
have the dynamics of a consigned program. And so therefore, the material costs will not be flowing
through our revenue. As you know, the vast majority of our networking has the silicon included. And
the vast majority of our compute does not have the silicon included. And those dynamics are really
holding as we go into next year. So no big change in the accounting side that's impacting our revenue.
Operator (Operator)
[Operator Instructions]
Your next question comes from the line of [indiscernible] with SIG.
Unknown Analyst (Analysts)
I guess my question is on the fiscal year '26 outlook. You've raised both revenues and margin outlook
for the year. When I look at the incremental margins on that $1.5 billion revenue, I get about 12% of
operating margin. of incremental. And I was wondering, how should we think about the drivers behind
that margin improvement? Is that your cost of component supply that is improving? Or are you able to
capture more value at those customers? And as a follow-up, if you were to have more supply unlock,
how should we think about the incremental margins on this upside?
Mandeep Chawla (Executives)
[ Betsy ], nice to talk to you. I'm going to try and answer that at a little bit of a higher level, which is we
are seeing margin expansion quarter-to-quarter, and it's being driven by 2 main things. The first one is
that CCS margins are accretive to the company. And CCS is growing at a record rate this year. CCS is

going to be growing close to 85% year-over-year. And then we're going to see a similar level of growth
next year. Just naturally, as CCS becomes a bigger part of the pie, margins do have that benefit.
Within CCS, it's the 2 things that I had talked about. One is we're seeing an increasing level of HPS or
ODM content that allows strong pricing because of the value add that we're bringing. But then we're
seeing operating leverage. Our factories right now are running at a high level of utilization, and it is not
by accident. It's intentional because we know that you can drive very strong productivity in that type of
an environment. And so we are seeing the benefits of operating leverage. To your point on if revenue
was to continue to accelerate, well, we don't expect to add an SG&A dollar for every revenue dollar. So I
would say the operating leverage flow-through should be there. The rest of it would really be mix
dependent.
Operator (Operator)
Your next question comes from the line of Paul Treiber with RBC Capital Markets.
Paul Treiber (Analysts)
You mentioned that you're gaining market share across the board. Can you elaborate further on market
share momentum within both enterprise and communications? And then specifically with programs
becoming larger and larger, are you seeing the competitive intensity of those programs increasing and
how you're working to retain share going forward?
Robert Mionis (Executives)
Yes. Sure, Paul. So broadly speaking, our customers are valuing continuity and surety of supply. One of
the things that we do very, very well is that we are able to deliver high complex products to our
customers reliably at scale. So in many cases, where products were dual sourced, and that's very
common in our industry as products get awarded initially, we're usually the ramp partner. And then as
they get mature, sometimes they get offloaded a second source for us to ramp the next generation.
In many cases, what we're seeing is our customers are asking us to pick up -- take back some share that
was potentially awarded to other providers because we can more reliably produce those products at
scale, if you will. So we're seeing that across the board. And why we're able to rise to the occasion is that
material is already pipelined. So we don't have to get back in line. We're actually able to pick up that
supply chain and just put it through our proven manufacturing processes. And we're seeing that
certainly in enterprise and also in communications.
Mandeep Chawla (Executives)
One thing I would add to that, Paul, is one of the things that we're hearing from our customers is the
amount of value that is placed on the transition from designing a program to ramping a program. It is
not easy. One of the differentiators we think that Celestica has is we have a very sizable design
engineering organization, which we've been investing in for over a decade. That organization will be
close to 2,000 engineers by the end of this year. And so being able to design the product in
collaboration with our customer and then being able to work very collaboratively with the
manufacturing side of the business to ramp it successfully, we believe, add to Rob's point, has led to
some market share gains.
Robert Mionis (Executives)

Some people do design, some people do manufacturing. We do both, and that's part of our secret sauce.
Operator (Operator)
There are no further questions at this time. I will now turn the call back to Rob Mionis, CEO, for closing
remarks.
Robert Mionis (Executives)
Thank you. Our strong second quarter performance and momentum carrying us into the second half of
the year gives us confidence to raise our full year 2026 outlook and continued exceptionally strong
customer demand and strategic investments in our infrastructure are enabling us to accelerate our
2027 revenue growth past the 2026, 65% mark. Again, thank you for your support, and we are looking
forward to update you next quarter.
Operator (Operator)
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CLS_Q1_2026_Earnings_Call_20260428.md
- 2026-04-28｜CFO｜guidance：CFO 給 Q2 營收區間 41.5～44.5 億美元（原話："be between $4.15 billion and $4.45 billion"）
- 2026-04-28｜CFO｜margin：Q2 non-GAAP 營業利益率以中點計預期 8.0%（原話："8.0%, which would represent an increase of 60 basis points"）
- 2026-04-28｜CEO｜guidance：CEO 將 2026 全年營收展望由 170 億上調至 190 億美元（原話："raising our revenue outlook from $17 billion to $19 billion"）
- 2026-04-28｜CEO｜guidance：全年調整後 EPS 展望上調至 10.15 美元（原 8.75）（原話："our outlook for adjusted EPS and from $8.75 to $10.15"）
- 2026-04-28｜CEO｜margin：全年調整後營業利益率展望 8.1%，高於先前 7.8%（原話："an adjusted operating margin outlook of 8.1%"）
- 2026-04-28｜CEO｜guidance：自由現金流展望維持 5 億美元，已含 10 億資本支出（原話："we are reaffirming our free cash flow outlook of $500"）
- 2026-04-28｜CEO｜commitment：CEO 稱 2026 展望為高信心觀點（原話："This outlook represents our high confidence view for 2026"）
- 2026-04-28｜CEO｜guidance：2027 營收成長預期顯著高於 2026 的 65 億美元增量，未給具體數字（原話："grow revenue significantly more than this in 2027"）
- 2026-04-28｜CFO｜guidance：CFO 說明 2027 營收下限約 255 億美元，且實際看到更高（原話："would be somewhere around $25.5 billion"）
- 2026-04-28｜CEO｜guidance：CCS 全年營收成長預期約 70%（原話："we now anticipate approximately 70% revenue growth"）
- 2026-04-28｜CEO｜guidance：ATS 全年營收展望上調為中至高個位數成長（原話："mid- to high single-digit percentage growth"）
- 2026-04-28｜CFO｜margin：Q1 CCS 分部利益率 8.6%，歸因於產品組合與營運槓桿（原話："CCS segment margin in the first quarter was 8.6%"）
- 2026-04-28｜CFO｜margin：Q1 ATS 分部利益率 6.0%，歸因於組合優化（原話："ATS segment margin was 6.0%, up 100 basis points"）
- 2026-04-28｜CFO｜margin：Q1 調整後毛利率 11.3%（原話："Adjusted gross margin was 11.3%, up 30 basis points"）
- 2026-04-28｜CFO｜margin：CFO 表示毛利率目標為維持或提升，並承認長期有輸入成本逆風（原話："we definitely are looking to maintain, if not grow"）
- 2026-04-28｜CFO｜margin：CFO 指出記憶體與矽等輸入成本大幅上升，構成毛利率逆風（原話："some input costs that are going up materially"）
- 2026-04-28｜CEO｜risk：CEO 稱元件短缺較 90 天前更嚴重（原話："more component shortages now than 90 days ago."）
- 2026-04-28｜CEO｜risk：CEO 點名受配給的物料為客製矽與記憶體（原話："on allocation are custom silicon and memory."）
- 2026-04-28｜CFO｜risk：Q1 企業端營收略低於展望，原因為部分元件限制（原話："gated by select component constraints"）
- 2026-04-28｜CEO｜risk：CEO 表示 Q1 AI/ML 運算專案問題屬物料供應而非需求（原話："It was actually a material supply issue."）
- 2026-04-28｜CEO｜risk：供應端緊俏被描述為正在「節制」成長速度（原話："environment, effectively pacing our growth"）
- 2026-04-28｜CEO｜commitment：CEO 稱已與供應商取得支撐展望的供貨承諾（原話："we have commitments from all our suppliers"）
- 2026-04-28｜CEO｜commitment：CEO 稱與客戶的訂單多為 NCNR，提供合約保護（原話："supported by our customers are NCNR"）
- 2026-04-28｜CEO｜customer：CEO 稱已在接 2028 年出貨的訂單（原話："actually booking awards right now"）
- 2026-04-28｜CFO｜customer：Q1 有三家客戶各占營收至少 10%（35%、15%、15%）（原話："three customers that each accounted for at least 10%"）
- 2026-04-28｜CEO｜customer：CPO 交換器訂單來自既有客戶（原話："it's an existing customer"）
- 2026-04-28｜CEO｜commitment：CPO 交換器量產時間為 2027 下半年（原話："this will be second half of 2027"）
- 2026-04-28｜CEO｜product：CEO 稱此為首個使用 Broadcom 方案的大規模 CPO 量產部署（原話："production scale deployment of co-packaged optics"）
- 2026-04-28｜CEO｜margin：CEO 稱 CPO 專案利益率落在公司一般水準的高端（原話："on the higher end of what we typically do"）
- 2026-04-28｜CEO｜product：CEO 自述已上移價值鏈成為共同設計夥伴（原話："a sophisticated codesign partner"）
- 2026-04-28｜CEO｜product：1.6T 有 10 個進行中專案，2027 大量放量（原話："in terms of 1.6T we have 10 active programs"）
- 2026-04-28｜CEO｜product：與 AMD 合作的 Helios 交換器預計年底有初期樣品（原話："we expect initial units to be"）
- 2026-04-28｜CEO｜product：Helios 2027 年營收可能受矽供應而非需求所限（原話："silicon availability than by end market demand"）
- 2026-04-28｜CEO｜commitment：數位原生機櫃專案樣品今年出貨，2027 Q1 末量產（原話："We're shipping sample systems this year"）
- 2026-04-28｜CFO｜product：ATS 資本設備被描述為進入新循環（原話："now is entering into a very nice cycle"）
- 2026-04-28｜CEO｜competition：CEO 回答市占：未見重大變化（原話："We haven't seen a significant change in market share shifts"）
- 2026-04-28｜CEO｜competition：CEO 稱供應緊俏環境下的搶市占機會目前尚未出現（原話："We haven't necessarily seen that as of yet"）
- 2026-04-28｜CFO｜product：設計工程師約 1,350 人，年底將更多，R&D 支撐 HPS（原話："We have about 1,350 design engineers right now."）
- 2026-04-28｜CFO｜capital_allocation：2026 資本支出指引約 10 億美元不變（原話："guidance remains unchanged at approximately $1 billion"）
- 2026-04-28｜CFO｜capital_allocation：2027 資本支出以約 15 億美元作暫定佔位數字（原話："number of $1.5 billion as a placeholder for now"）
- 2026-04-28｜CFO｜capital_allocation：若成長需要額外資金，管理層不會猶豫（原話："we have no hesitation to do that."）
- 2026-04-28｜CFO｜capital_allocation：Q1 回購約 7.3 萬股、2,000 萬美元，態度為機會性（原話："We continue to be opportunistic with respect to share"）
- 2026-04-28｜CFO｜capital_allocation：財報後修訂信貸，循環額度增加 10 億美元至 17.5 億（原話："we amended our credit facility, increasing our revolver"）

### CLS_Shareholder_Analyst_Call_Celestica_Inc_20260519.md
- 2026-05-19｜CEO｜guidance：CEO 提到 Q1 業績後表示年初表現很強。本場無具體財測數字。（原話："we've had a very strong start to the year and"）
- 2026-05-19｜CEO｜commitment：CEO 表示對公司前景維持信心（無量化目標）。（原話："remain confident in our trajectory."）
- 2026-05-19｜CEO｜customer：CEO 稱 CCS 部門因支援超大型雲端客戶而取得顯著成長。（原話："we are capturing significant growth as we"）
- 2026-05-19｜CEO｜customer：CCS 成長來源描述為支援 hyperscaler 建置下一代資料中心基礎設施。（原話："support hyperscalers building next generation of data center"）
- 2026-05-19｜CEO｜competition：CEO 自稱為 400G／800G 乙太網路交換器的公認市場領導者。（原話："recognized market leader in 400G and 800G Ethernet switches"）
- 2026-05-19｜CEO｜product：CEO 表示正交付下一代 1.6T 交換方案。（原話："generation of 1.6T switching solutions"）
- 2026-05-19｜CEO｜customer：CEO 提及先前季度已公告的重大新專案獲標。（原話："significant new program wins we've announced"）
- 2026-05-19｜CEO｜capital_allocation：ATS 策略為工程導向，投資於專業化市場團隊與全球設計中心。（原話："investing in specialized market-focused teams and global"）
- 2026-05-19｜CEO｜commitment：CEO 結語稱成長機會仍在前方。（原話："we are just getting started"）

### CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：CFO 給 2027 全年營收展望 400 億美元。（原話："We anticipate revenue of $40 billion"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2027 全年 non-GAAP 營業利益率展望 9.0%。（原話："non-GAAP operating margin is expected to be 9.0%"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2027 調整後 EPS 展望 21.50 美元。（原話："We anticipate non-GAAP adjusted EPS of $21.50, up 86%"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：Q4 營收財測區間。（原話："between $6.275 billion and $6.575 billion"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：Q4 調整後 EPS 財測區間。（原話："between $3.37 and $3.57"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2026 全年營收展望由 205 億上調至 210 億美元。（原話："increases from $20.5 billion to $21 billion"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2026 自由現金流展望為 4.6 億美元（原 6 億）。（原話："free cash flow outlook for 2026 is $460 million"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2027 營收下半年顯著高於上半年。（原話："meaningfully higher revenue in the second half"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2027 資本支出區間。（原話："in the range of $1.5 billion to $2.0 billion"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：Q4 Compute & Storage 終端市場成長預期約 160%。（原話："we expect growth of approximately 160%"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2027 營收財測的口徑：已把斜坡、零組件供應與執行風險納入。（原話："took into consideration the risk around the ramps"）
- 2026-10-27｜Todd Ankenmann (CFO)｜margin：Q3 調整後營業利益率與年增幅度。（原話："Our non-GAAP operating margin was 8.5%, up 90 basis points"）
- 2026-10-27｜Todd Ankenmann (CFO)｜margin：Q3 調整後毛利率下降，管理層歸因於 CCS 產品組合。（原話："Adjusted gross margin was 11.2%, down 50 basis points"）
- 2026-10-27｜Todd Ankenmann (CFO)｜margin：2027 毛利率預期維持 11% 出頭，取決於網通與運算的組合。（原話："our margins will continue in '27 in the low 11s"）
- 2026-10-27｜Todd Ankenmann (CFO)｜margin：CFO 稱網通仍對毛利率有增益。（原話："networking being accretive from a margin perspective"）
- 2026-10-27｜Todd Ankenmann (CFO)｜margin：回答 H1/H2 毛利率是否不同：CFO 稱兩半年無不同動態，取決於各季組合。（原話："different gross margin dynamics in '27 between the 2 halves"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜margin：Mandeep 說明產能與電力投資使其拿下競爭對手拿不到的專案，並帶來較好的定價與毛利。（原話："allowing us to capture program wins that many of our competitors"）
- 2026-10-27｜Todd Ankenmann (CFO)｜commitment：CFO 表示以現有看法，目標 2028 年自由現金流轉正。（原話："target to return to positive cash flow in '28"）
- 2026-10-27｜Todd Ankenmann (CFO)｜commitment：CFO 稱 2027 會出現淨現金使用（自由現金流為負）。（原話："will result in a net use of cash in 2027"）
- 2026-10-27｜Todd Ankenmann (CFO)｜commitment：管理層稱僅依已獲專案推算的 2028 客戶需求預測高於 2027 營收展望。（原話："customer demand forecasts based solely on awarded programs"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜commitment：Mandeep 預期 2027 維持高稼動率。（原話："we do expect high utilization in 2027"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜commitment：CCS 預計 2027 研發投入超過 3 億美元。（原話："expect to invest over $300 million in 2027"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜commitment：HPS 工程師預計明年增至 2,000 人以上。（原話："grow to over 2,000 engineers by next year"）
- 2026-10-27｜Todd Ankenmann (CFO)｜commitment：管理層稱 2027 資本支出對應已獲專案，並承諾持續重新評估產能需求。（原話："we feel we've got the capacity needed with the investments"）
- 2026-10-27｜Todd Ankenmann (CFO)｜capital_allocation：資本配置優先順序：有機成長優先，勝過回購。（原話："the priority and focus of our capital is on the organic growth"）
- 2026-10-27｜Todd Ankenmann (CFO)｜capital_allocation：CFO 解釋更新 NCIB 的原因為加拿大每年需更新之規定。（原話："requirement to renew the program on an annual basis"）
- 2026-10-27｜Todd Ankenmann (CFO)｜capital_allocation：對股東回報的態度：看時機的機會主義。（原話："opportunistic in our approach towards returning capital"）
- 2026-10-27｜Todd Ankenmann (CFO)｜capital_allocation：8 月完成股權增資，CFO 稱足以應付需求。（原話："we did raise $3.5 billion of equity in August"）
- 2026-10-27｜Todd Ankenmann (CFO)｜capital_allocation：2027 約 200 億美元增量營收下，管理層投入營運資金。（原話："we are investing meaningfully in working capital"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜capital_allocation：M&A 有主動漏斗，以能力為導向。（原話："we do have an active funnel"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜competition：Mandeep 稱 1.6T/800G 專案面對的競爭者較前幾代減少。（原話："there are fewer competitors today that we are going up against"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜competition：Dorwart 承認成功會招來競爭、已有新增競爭者。（原話："it's going to invite competition"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜competition：Mandeep 對整櫃整合市場的競爭者去留說法。（原話："not all competitors will stay for the journey"）
- 2026-10-27｜Robert Mionis (CEO) / Steven Dorwart｜competition：引用第三方研究：客製乙太網路交換器營收市占率。（原話："58% share of total custom Ethernet switch revenue"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜competition：Dorwart 稱公司不必像商品化市場那樣定期爭奪份額，但份額會與客戶定期協商，客戶可能把舊產品移出。（原話："we're not in a situation of having to compete for share"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜product：預期 1.6T 營收明年超過 800G。（原話："1.6T revenue will surpass 800G revenue next year"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜product：已宣布的 10 個 1.6T 專案中，scale-up 與 scale-out 的拆分。（原話："4 of them are scale up and 6 of them are scale out"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜product：與超大規模客戶共同設計的 CPO 機櫃交換器專案，預定 2027 年底量產。（原話："production scheduled to ramp in late 2027"）
- 2026-10-27｜Gavin Cato (SVP, CCS Engineering)｜product：Gavin 稱 1.6T 世代可插拔光模組仍佔多數，CPO 要到 3.2T/400G SerDes 才更普遍。（原話："you're going to see pluggables remain in the 1.6 time frame"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜product：DS6010（AMD Helios scale-up 交換器）預計年底開始量產爬坡。（原話："We expect to begin ramping by the end of the year."）
- 2026-10-27｜Steven Dorwart (President, CCS)｜product：OpenAI 客製 ASIC 系統預計 2027 開始量產爬坡。（原話："It is expected to begin ramping production in 2027."）
- 2026-10-27｜Todd Ankenmann (CFO)｜customer：Q3 三家 10% 以上客戶占營收 35%、17%、14%。（原話："accounting for 35%, 17% and 14%, respectively"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜customer：2027 運算成長的兩個主要動力為 Google TPU 與 OpenAI。（原話："relationship with Google in support of their TPU platform"）
- 2026-10-27｜Todd Ankenmann (CFO)｜customer：CFO 稱客戶資金充裕、無財務困難跡象。（原話："We see no financial distress across our portfolio."）
- 2026-10-27｜Steven Dorwart (President, CCS)｜customer：Dorwart 描述漏斗主要來自既有核心客戶，並以籃子比喻客戶集中。（原話："it's not always good to have all your eggs in one basket"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜customer：Dorwart 稱商機漏斗處於歷史高位，且主要來自既有客戶。（原話："I would say it's at a historic high level"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜customer：2023–2026 超大規模客戶營收預計成長約 5 倍。（原話："grow by approximately 5x, expanding at a 71% CAGR"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜risk：Dorwart 指出可能壓低數字的限制多在土地、電力與地緣政治。（原話："more in the areas of land and power"）
- 2026-10-27｜Todd Ankenmann (CFO)｜risk：Q3 存貨較上季增加 11 億美元、年增 25 億美元。（原話："a sequential increase of $1.1 billion"）

### 問答異常語氣（迴避／改口／保留）
- CLS_Q1_2026_Earnings_Call_20260428.md｜問：Goldman Sachs Michael Ng 問 2027 CCS 營收成長相對上次指引的預期，並請拆分各專案貢獻｜答法：回答「顯著更多」與 2026 年增量下限推算，未給 CCS 2027 成長率與各專案貢獻，稱之後再提供更具體數字
- CLS_Q1_2026_Earnings_Call_20260428.md｜問：BNP Paribas Karl Ackerman 請拆分新交換器專案與 AI 伺服器的成長驅動，及對利潤率走勢的影響｜答法：列舉各專案名稱與時程，明說暫不提供細節（「more to come」），未回答利潤率軌跡
- CLS_Q1_2026_Earnings_Call_20260428.md｜問：Susquehanna Mehdi Hosseini 請量化 Helios 未來 18 個月機會及已含入 2026 目標的部分｜答法：僅稱整體市場為數十億美元級，未回答 Celestica 自身金額，也未說明是否已含入 2026 目標
- CLS_Q1_2026_Earnings_Call_20260428.md｜問：BofA Ruplu Bhattacharya 問 2027 自由現金流與營運資金，以及 scale-up 與 scale-out 對 65 億以上增量的拆分｜答法：CFO 重申 2026 FCF 與資本紀律，未給 2027 FCF 或營運資金數字；CEO 僅確認兩類專案屬性，未拆分金額
- CLS_Q1_2026_Earnings_Call_20260428.md｜問：Wolfe George Notter 問 CPO 訂單規模，以及是否蠶食既有營收｜答法：回答既有客戶、不蠶食及量產在 2027 下半年，未回答訂單規模
- CLS_Q1_2026_Earnings_Call_20260428.md｜問：JPMorgan Samik Chatterjee 問 CPO 交換器的內容價值與利潤率｜答法：未給單機內容價值數字，利潤率只稱位於一般水準高端
- CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md｜問：JPMorgan（Cardoso）要求給 2027 淨現金使用的範圍與現金週期天數｜答法：CFO 未給範圍或週期天數，改談 2026 FCF 下修、8 月增資足夠、2028 年目標轉正。
- CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md｜問：BNP（Ackerman）問交換器複雜度提升對毛利率的貢獻，以及伺服器/L11 毛利率能否改善｜答法：Dorwart 只答公司能選擇專案、毛利為考量因素，話說到一半被 CFO 接手；CFO 改談毛利率 11% 出頭與營業槓桿，未直接回答伺服器或 L11 毛利。
- CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md｜問：BofA（Bhattacharya）問現有廠區能支撐多少營收｜答法：CFO 明確表示不給與產能掛鉤的營收數字，只說 2027 投資足以支撐 2027 與 2028 需求。
- CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md｜問：BofA（Bhattacharya）問回購是否主要用來抵銷股權激勵，或可能成為有意義的資本回報｜答法：CFO 未直接回答抵銷股權激勵與否，只說時機看機會、優先有機成長、更新 NCIB 是加拿大年度規定。
- CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md｜問：Canaccord（Young）問稼動率相關歷史量化數字與維持高稼動率對達成 9% 營益率的重要性｜答法：Mandeep 未給任何量化稼動率數字，只說高稼動率是刻意經營，並說 2027 預期高稼動率。
- CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md｜問：RBC（Treiber）問供應可得性是否比設計能力更重要，以及完整機櫃方案的競爭者是否變少｜答法：Dorwart 未直接回答兩者何者較重，承認有新增競爭者；Mandeep 補充稱 1.6T/800G 競爭者較少，但舉例仍以性質描述為主。

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
{"date":"20260711","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 機架級「設計+製造」是結構性能力，非純週期需求；hyperscaler 不會在 36 個月內大規模自建或全面切換 ODM","columns":{"2Y 驗證點":"1.6T 兩家 hyperscaler 2H2026 量產如期；custom switch 份額守住 ~55%","5Y 驗證點":"CCS 段仍為多數 hyperscaler 網路/運算平台的量產夥伴","10Y 驗證點":"設計含量 mix 不逆轉，HPS 毛利率不被商品化","數字門檻 + 來源":"custom Ethernet switch 市佔 ≥50%（Dell'Oro 2025）；1.6T 已中標 ≥2 家 hyperscaler（公司法說）；Top 3 客戶 ≥10% 揭露（10-K）","漂移觸發":"某 &gt;10% 客戶單季占比掉 &gt;5pp，或 CCS 毛利率連 2 季 −100bps → 削弱（TTM 季節性過濾）"}},{"id":"H2","text":"2026 capex ramp（約 $1B、5% 營收）為「擴產換訂單」的合理投入，2027 起 FCF/NI 回升","columns":{"2Y 驗證點":"2027 H1/H2 FCF/NI 回到 ≥0.6","5Y 驗證點":"capex/rev 回落 &lt;4%，owner earnings 轉正常化","10Y 驗證點":"資本輕結構不因基建投資變重","數字門檻 + 來源":"FY25 FCF/NI 0.55（GAAP）；2026 capex/rev guide ~5%；AllianceTexas $876M（Bisnow 2025-04）","漂移觸發":"2027 H2 FCF/NI 連 2 季 &lt;0.5 且 capex/rev &gt;6% → 隱性資本密集確認"}},{"id":"H3","text":"35.5x Fwd PE 不會崩至 15x（估值體系不崩壞）；前提是 EPS 維持 +30%+ 且 ROIC &gt;25%","columns":{"2Y 驗證點":"Fwd PE FY1 維持 25-40x 區間，EPS 上修延續","5Y 驗證點":"倍數隨成長放緩溫和壓縮至 ~20x（非崩塌）","10Y 驗證點":"不落入 EMS 均值回歸至 15-18x 的地板","數字門檻 + 來源":"Fwd PE FY1 現 35.5x（5Y 分位 ~78%）；同業 JBL 22x／SANM 17x；EPS 3Y CAGR 45.6%（Excel snapshot 2026-06-23）","漂移觸發":"Fwd PE FY1 分位連 4 季 &gt;90% + 同業溢價連 4 季 &gt;80% → mean reversion 機率升；或 EPS YoY 連 2 季下修 → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"hyperscaler 2026 H2 / 2027 capex 大幅修正（2007/2015 式），AI 資本週期拐頭","columns":{"對應假設":"H1+H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Meta/GOOGL/AMZN/MSFT 合計 capex guidance YoY","警戒閾值":"合計 capex YoY 從 +77% 降至 &lt;+15%（連 1 季）"}},{"id":"R2","text":"大客戶 AI 伺服器/交換機組裝二供或 in-house 擴散（Google TPU 已現，蔓延至網路交換機/其他客戶）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"Inventec/Foxconn AI 伺服器出貨份額；季度個別客戶占比；CCS 毛利率","警戒閾值":"某 &gt;10% 客戶占比單季 −5pp；或 CCS 毛利率連 2 季 −100bps"}},{"id":"R3","text":"倍數均值回歸——35.5x 峰值 Fwd PE 隨成長放緩壓縮至 EMS 地板 15-18x，即使 EPS 兌現股價仍跌（SMCI/JBL 式 re-rate 頂）","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"Fwd PE FY1 分位、同業（JBL/SANM）相對倍數","警戒閾值":"Fwd PE FY1 分位連 4 季 &gt;90%；同業本益比連 2 季同步壓縮 &gt;20%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"集中度回落<58% 或 Google 二供對 CCS 營收衝擊量化明朗、且證券詐欺調查結案；估值面 Fwd PE FY1≤28x（約 $285）補安全邊際","irr_base_pct":8.4,"ev5y_pct":35.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.8,"ev5y_pct":35.0,"irr_base_pct":8.4,"max_dd_pct":-58.0,"bull_5y_price":768.0,"bear_5y_price":143.0,"p_bull_pct":28.0,"p_bear_pct":30.0,"rearm_trigger":"集中度回落<58% 或 Google 二供對 CCS 營收衝擊量化明朗、且證券詐欺調查結案；估值面 Fwd PE FY1≤28x（約 $285）補安全邊際","price_at_dd":359.85,"archetype":"EMS/ODM（資本輕·低毛利·需求週期·代工服務）","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CLS_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
