你是 stock-analyst **v20 判斷 agent**，標的 3665.TW（20261012）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"3665.TW","date":"2026-10-12","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3665.TW_20261012/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3665.TW_20261012/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_ifrs","label":"營收（IFRS 合併）","value":232.81,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-21）","unit":"億 TWD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-21）","citation":"uanalyze.com.tw/articles/1343453844（轉載鉅亨網）；Quartr 交叉一致；非公司 IR 原稿"},"note":"查無"},{"id":"f_kpi1","label":"毛利率","value":30.73,"period":"Q2 2026（公告於 2026-08-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 2026（公告於 2026-08-21）","citation":"uanalyze.com.tw/articles/1343453844；Quartr"},"note":"查無"},{"id":"f_kpi2_ifrs_gaap","label":"營業利益率（IFRS，等同 GAAP）","value":17.22,"period":"Q2 2026（公告於 2026-08-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 2026（公告於 2026-08-21）","citation":"uanalyze.com.tw/articles/1343453844；Quartr"},"note":"查無"},{"id":"f_kpi3_ifrs","label":"營業利益（IFRS）","value":40.1,"period":"Q2 2026（公告於 2026-08-21）","unit":"億 TWD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 2026（公告於 2026-08-21）","citation":"Quartr 頁面列 NT$4.01B；與營收×營益率推算一致"},"note":"查無"},{"id":"f_kpi4_eps","label":"稅後純益（歸屬母公司）／EPS","value":15.28,"period":"Q2 2026（公告於 2026-08-21）","unit":"TWD/股（純益 29.82 億，QoQ +31.13%，YoY +47.29%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 2026（公告於 2026-08-21）","citation":"uanalyze.com.tw/articles/1343453844；Quartr"},"note":"查無"},{"id":"f_kpi5","label":"管理層展望（無數字指引）","value":"定性","period":"Q2 2026（公告於 2026-08-21）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 2026（公告於 2026-08-21）","citation":"Quartr 摘要、uanalyze；非公司原稿"},"note":"無數字區間可比"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-25","period":"2026-08-25","unit":"date","basis":"距今 34 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-25"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_3665_tw_gross_margin_pct","label":"3665.TW 毛利率","value":31.08,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3665.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3665_tw_operating_margin_pct","label":"3665.TW 營業利益率","value":17.44,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3665.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3665_tw_fcf_margin_pct","label":"3665.TW FCF 利潤率","value":5.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3665.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_aph_gross_margin_pct","label":"APH 毛利率","value":37.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APH.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aph_operating_margin_pct","label":"APH 營業利益率","value":26.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APH.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aph_fcf_margin_pct","label":"APH FCF 利潤率","value":17.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APH.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tel_gross_margin_pct","label":"TEL 毛利率","value":36.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TEL.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tel_operating_margin_pct","label":"TEL 營業利益率","value":20.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TEL.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tel_fcf_margin_pct","label":"TEL FCF 利潤率","value":17.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TEL.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3023_tw_gross_margin_pct","label":"3023.TW 毛利率","value":24.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3023.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3023_tw_operating_margin_pct","label":"3023.TW 營業利益率","value":10.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3023.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3023_tw_fcf_margin_pct","label":"3023.TW FCF 利潤率","value":4.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3023.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":2355.0,"period":"2026-10-12（RTH 收盤，UTC）","unit":"TWD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":6.77,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^TWII","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":54.54,"period":"2026-10-12（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":69.25,"period":"2026-10-09","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-09","citation":"DD_tw_EPS_estimates_20261009.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":127.97,"period":"2026-10-09","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-09","citation":"DD_tw_EPS_estimates_20261009.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":164.67,"period":"2026-10-09","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-09","citation":"DD_tw_EPS_estimates_20261009.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":43.31,"period":"2026-10-12（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-12（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.58,"period":"2026-10-12（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-12（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.56,"period":"2026-10-12（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-12（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":34.08,"period":"2026-10-09","unit":"x","basis":"分母＝FY1 EPS 69.25，分子＝快照價 2360.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-09"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.655,"period":"2026-10-12","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-12"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2026 年 8 月合併營收 88.92 億元，年增 54.0%；前 8 月累計 626.33 億元，年增 40.0%（營收動能間接資料，非直接份額數據）","source":"TechNews 貿聯-KY 8 月營收","url":"https://finance.technews.tw/2026/09/04/bhi-bizlink-3665-202608-financial-report/","excerpt":"貿聯-KY(3665)公布 8 月合併營收 88.92 億元，較上(7)月成長 -7.7%,與去年同期相比為年增 54.0%;累計其今年前 8 月營收為 626.33 億元，較去年同期增加 40.0%。","as_of":"2026-09-04","retrieved_at":"20261012","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"貿聯於 Computex 2026 展示支援 448Gbps/lane、PCIe Gen6/7 及 Co-Packaged Copper 的高速銅纜方案，並屬 NVIDIA MGX 生態系（公司自述）","source":"BizLink 新聞稿 Computex 2026","url":"https://www.bizlinktech.com/news/bizlink-showcases-ai-infrastructure-interconnect-solutions-supporting-the-nvidia-mgx-ecosystem-at-computex-2026","excerpt":null,"as_of":"2026-06-02","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Digitimes 2026 年 4 月標題指貿聯認為 CPO 放量時程不確定（細節未讀到）","source":"Digitimes BizLink tag page","url":"https://www.digitimes.com/tag/bizlink/0019083.html","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261012","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"2025年初農曆年前，傳出大客戶Credo引進第二個AEC供應商，貿聯股價一度跌停；董事長梁華哲稱雙方合作六年、貿聯仍是Credo獨家供應商（搜尋摘要轉述，未逐字取得）。","source":"工商時報／經濟日報等報導（ctee 20250220700247-439901）","url":"https://www.ctee.com.tw/news/20250220700247-439901","excerpt":null,"as_of":"2025-02-20","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R","moat_trend"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"2025年12月報導：市場再傳AEC大客戶Credo引進第二供應商，壓抑貿聯股價；未見公司或Credo正式確認，亦無第二供應商出貨規模資料。","source":"中時 wantrich 20251205900555-420101","url":"https://wantrich.chinatimes.com/news/20251205900555-420101","excerpt":null,"as_of":"2025-12-05","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"2026年1月報導：輝達CES表示Rubin伺服器將採「無線纜」設計，線束大廠貿聯首當其衝（潛在設計面衝擊，非確認輝達自製線束）。","source":"中時 wantrich 20260114900129-420101","url":"https://wantrich.chinatimes.com/news/20260114900129-420101","excerpt":null,"as_of":"2026-01-14","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#3","axis":"customer_second_source","section":"coverage","direction":"+","claim":"2026年中歐系外資表示貿聯仍是Credo AEC與ALC產品主要供應商；6月美系外資認為2027上半年主要由AEC帶動。","source":"technews 貿聯-KY 掌握高壓供電、CPO 技術，法人重申買進","url":"https://technews.tw/2026/06/08/investor-see-bizlink/","excerpt":null,"as_of":"2026-06-08","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"董事長梁華哲 2026 年 2 月表示 AI 基礎建設仍在加速期、短期看不到泡沫跡象，預期全年營收有機會再創新高、逼近千億元（公司談話，非財報）","source":"uanalyze 貿聯董座：AI需求仍在加速期 今年營收估延續強勁成長上看千億元","url":"https://uanalyze.com.tw/articles/2312448089","excerpt":null,"as_of":"2026-02-25","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026 年 6 月自結合併營收 85.18 億元、年增 63.79%；上半年累計營收 441.11 億元、年增 33.97%","source":"工商時報 2026/07/28","url":"https://www.ctee.com.tw/news/20260728701005-430201","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261012","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"併入 Interplex 資料通訊業務後，外資預估 HPC 營收占比 2026、2027 年可達 53%、75%（外資預估）","source":"經濟日報/UDN 併購 Interplex 添動能 法人調高貿聯獲利預估值及目標價","url":"https://money.udn.com/money/story/5607/9783283","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Vera Rubin NVLink scale-up 背板仍用被動銅纜，估約 5,184 條，設計大致沿用 GB300（大摩關聯分析，經台灣部落格轉述）","source":"cnyes 大摩輝達 Rubin BOM 出來了：光電視角的四個判斷","url":"https://hao.cnyes.com/post/249153","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"供應鏈報告稱 Nvidia Kyber 官方仍目標 2H27 量產，但延後至 2H28 機率上升；若延後，Rubin Ultra 可能沿用 Oberon NVL72x2 機櫃（機櫃內銅背板）。另稱 TE 在 GB300 cable backplane 份額低於預期的 30%","source":"cnyes hao 供應鏈報告（passive-components.eu 同期市場週報亦有 copper intra-rack 論述）","url":"https://hao.cnyes.com/post/248772","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美國於2026年7月23日依Section 301對中國課徵12.5%關稅，另有7.5%產能過剩關稅討論中；2026年2月最高法院裁定IEEPA無權直接課徵廣泛關稅後，美方改以301與232為主要工具。屬總體背景，未點名貿聯。","source":"理財周刊 moneyweekly.com.tw AID=244673","url":"https://www.moneyweekly.com.tw/_Article?AID=244673","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"彭博報導美國新的產能過剩關稅預計延到習近平與川普會面之後才宣布；未點名貿聯。","source":"TechNews 2026-09-18","url":"https://finance.technews.tw/2026/09/18/us-said-to-hold-off-on-tariffs-until-after-xi-trump-summit/","excerpt":null,"as_of":"2026-09-18","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#none","axis":"geo_supply_chain","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年9月合併營收93.32億元，年增39.2%；前9月累計719.65億元，年增39.9%（公司整體，非分段）","source":"TechNews 貿聯-KY 9月營收","url":"https://finance.technews.tw/2026/10/05/bhi-bizlink-3665-202609-financial-report/","excerpt":"貿聯-KY(3665)公布 9 月合併營收 93.32 億元，較上(8)月成長 5.0%,與去年同期相比為年增 39.2%;累計其今年前 9 月營收為 719.65 億元，較去年同期增加 39.9%。","as_of":"2026-10-05","retrieved_at":"20261012","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"法人預估併入Interplex後，HPC營收占整體比重2026、2027年分別可達53%、75%；自9月23日起併入","source":"經濟日報/UDN 併購 Interplex 添動能 法人調高貿聯獲利預估值及目標價","url":"https://money.udn.com/money/amp/story/5607/9783283","excerpt":"貿聯 自9月23日起正式併入Interplex,法人預估 2026、2027年整體營收占比分別可達53%、75%","as_of":"2026-10-01","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"永豐投顧估計HPC相關營收今年與2027年分別年增91%與40%；CPO與800V HVDC方案預期2027-2028進入全面爆發期","source":"UDN/財經媒體摘要（搜尋結果彙整）","url":"https://money.udn.com/money/amp/story/5607/9783283","excerpt":"永豐投顧估計 今年至2027年HPC相關營收分別年增91%與40%,並認為 CPO 與 800V HVDC 方案將在 2027 至 2028 年進入全面爆發期","as_of":"2026-10-01","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年6月宣布以8.5億美元現金收購Interplex Datacom（過去12個月營收約3.92億美元，產品含AI伺服器機架機構件），預計2026下半年完成","source":"BizLink 官網新聞/Pulse2","url":"https://www.bizlinktech.com/news/bizlink-expands-global-market-presence-and-deepens-customer-partnerships-by-acquiring-interplex-datacom","excerpt":"Interplex Datacom generated revenue of approximately US$392 million, for the twelve months ended on March 31, 2026.","as_of":"2026-06-11","retrieved_at":"20261012","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"HPC相關營收占比由2024年18%升至2025年35%（分析估計）；HPC電源產品占比由2025年17%升至2026年24%（口徑不同）","source":"搜尋摘要彙整（uanalyze/UDN）","url":"https://uanalyze.com.tw/articles/8715825507","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261012","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"CRU 預期銅雙絞線（twinax）成長延續到本十年末，但 2020 年代後期至 2030 年代初隨光學替代擴大而放緩","source":"CRU Group, The outlook of copper based data cables in AI data centres","url":"https://www.crugroup.com/en/communities/thought-leadership/2026/the-outlook-of-copper-based-data-cables-in-ai-data-centres/","excerpt":"Copper twinax is likely to continue growing through the end of the decade... However, growth is expected to slow in the late 2020s to early 2030s as optical substitution broadens","as_of":"2026-01-01","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"NVIDIA 表示 CPO 交換器 2026 下半年小規模部署，超大規模雲端 2026–2028 仍以可插拔光模組為主","source":"搜尋摘要（聚合來源 itiger／相關轉述），Copper vs. Optical in AI Data Centers","url":"https://www.itiger.com/news/1124823421","excerpt":"NVIDIA has explicitly stated that its CPO switches will see small-scale deployment in the second half of 2026... hyperscale cloud providers will still primarily rely on pluggable optical modules between 2026 and 2028.","as_of":"2026-01-01","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Gartner（2026 年 2 月）預期 CPO 約三年內成為主流，銅在 224Gbps/lane 遇到極限，買方焦點轉向 scale-up 互連","source":"Gartner Insights Abstract","url":"https://www.gartner.com/en/documents/7421462","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"貿聯 2025-10 OCP 發表 224Gbps/lane 共封裝銅纜（CPC）並提供 CPO-ready 設計，銅與光並列為互補方案（公司新聞稿，未揭露營收占比）","source":"BizLink, Showcasing Complete AI and HPC Rack Solutions at OCP Global Summit 2025","url":"https://www.bizlinktech.com/news/bizlink-showcasing-complete-ai-and-hpc-rack-solutions-at-ocp-global-summit-2025","excerpt":null,"as_of":"2025-10-01","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Investing.com 彙整：14 位分析師皆買入，12 個月平均目標價約 NT$3,203，高 3,870、低 2,450（頁面快照 as_of 不明，以 Simply Wall St 引用之 2026-09-18 近似）","source":"Investing.com BizLink consensus estimates","url":"https://www.investing.com/equities/bizlink-consensus-estimates","excerpt":"14 buy ratings, no holds or sells, and an average target of NT$3,202.86, with a high of NT$3,870 and a low of NT$2,450.","as_of":"2026-09-18","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"個別券商目標價：CLSA 2026-04-28 升評 3,870；JPMorgan 2026-07-15 首次覆蓋 3,100；Nomura/Instinet 2026-08-24 3,270","source":"Investing.com / 搜尋彙整","url":"https://www.investing.com/equities/bizlink-consensus-estimates","excerpt":"Nomura/Instinet's August 24, 2026 note carried a NT$3,270 target, and JPMorgan initiated coverage on July 15, 2026 with a NT$3,100 target. CLSA's April 28 upgrade set NT$3,870.","as_of":"2026-08-24","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"美系外資 2026-08 維持買進，認為 Q3 營收優於市場預期（媒體轉述；目標價數字與股票代號相同，原文待核）","source":"工商時報 ctee 2026-08-06","url":"https://www.ctee.com.tw/news/20260806700941-430201","excerpt":"美系外資最新報告維持貿聯-KY「建議買進」評等，目標價3665元，該報告也認為 2026年第3季營收表現優於市場預期。","as_of":"2026-08-06","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司月營收 9 月 93.32 億，年增 39.2%，前 9 月累計年增 39.9%","source":"科技新報 technews 2026-10-05","url":"https://finance.technews.tw/2026/10/05/bhi-bizlink-3665-202609-financial-report/","excerpt":"貿聯-KY(3665)公布 9 月合併營收 93.32 億元，較上(8)月成長 5.0%,與去年同期相比為年增 39.2%;累計其今年前 9 月營收為 719.65 億元，較去年同期增加 39.9%。","as_of":"2026-10-05","retrieved_at":"20261012","affects":["thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"貿聯董事會決議以現金向 Blackstone 旗下基金收購 Interplex 集團資料通訊業務 Interplex Datacom，企業價值 8.5 億美元，另有最高 5000 萬美元或有價金；原預計下半年交割。","source":"NOWnews 重訊報導","url":"https://www.nownews.com/news/6845272","excerpt":"董事會以現金方式收購高精密機械產品供應商Interplex集團旗下資料通訊業務Interplex Datacom，價值8.5億美元，預計在完成合約約定交割條件後，於下半年完成交割。","as_of":"2026-06-10","retrieved_at":"20261012","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"搜尋摘要稱貿聯於 9 月 23 日公告已完成 Interplex Datacom 收購並納入合併報表（來源為摘要彙整，未見官方公告原文；日期待核）。","source":"uanalyze 貿聯完成收購新加坡Interplex Datacom業務","url":"https://uanalyze.com.tw/articles/8733155904","excerpt":"貿聯完成收購新加坡Interplex Datacom業務 強化資料中心基礎設施布局","as_of":"2026-09-23","retrieved_at":"20261012","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"歐系外資報告指貿聯擬發行 GDR 與 ECB，預估稀釋每股盈餘約 6%~7%（摘要轉述，無逐字原文）。","source":"工商時報 wantrich 外資報導","url":"https://wantrich.chinatimes.com/news/20260709900212-420101","excerpt":null,"as_of":"2026-07-09","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"貿聯以現金收購 Interplex Datacom，企業價值 8.5 億美元（另最高 5000 萬美元或有價金）。","source":"NOWnews 重訊報導","url":"https://www.nownews.com/news/6845272","excerpt":"董事會以現金方式收購高精密機械產品供應商Interplex集團旗下資料通訊業務Interplex Datacom，價值8.5億美元，預計在完成合約約定交割條件後，於下半年完成交割。","as_of":"2026-06-10","retrieved_at":"20261012","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"摘要稱已於 9 月 23 日完成交割並納入合併報表（日期待核）。","source":"uanalyze 貿聯完成收購新加坡Interplex Datacom業務","url":"https://uanalyze.com.tw/articles/8733155904","excerpt":"貿聯完成收購新加坡Interplex Datacom業務 強化資料中心基礎設施布局","as_of":"2026-09-23","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"3665.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":31.08,"operating_margin_pct":17.44,"fcf_margin_pct":5.38,"rd_intensity_pct":2.46},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3665.TW","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"APH","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.63,"operating_margin_pct":26.77,"fcf_margin_pct":17.34,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APH","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TEL","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.12,"operating_margin_pct":20.49,"fcf_margin_pct":17.16,"rd_intensity_pct":4.76},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TEL","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"3023.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":24.36,"operating_margin_pct":10.63,"fcf_margin_pct":4.1,"rd_intensity_pct":4.37},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3023.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"3665.TW"},"financial_history":{"ticker":"3665.TW","currency":"TWD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":53757171000.0,"revenue_yoy_pct":null,"gross_margin_pct":25.65,"operating_margin_pct":10.46,"net_income":3838380000.0,"diluted_eps":22.844217,"free_cash_flow":530808000.0,"fcf_margin_pct":0.99,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":51051791000.0,"revenue_yoy_pct":-5.03,"gross_margin_pct":24.65,"operating_margin_pct":8.39,"net_income":2317355000.0,"diluted_eps":13.645137,"free_cash_flow":4210563000.0,"fcf_margin_pct":8.25,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":54080481000.0,"revenue_yoy_pct":5.93,"gross_margin_pct":28.2,"operating_margin_pct":12.07,"net_income":4396138000.0,"diluted_eps":23.59,"free_cash_flow":3448886000.0,"fcf_margin_pct":6.38,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":71247272000.0,"revenue_yoy_pct":31.74,"gross_margin_pct":31.73,"operating_margin_pct":17.52,"net_income":9005366000.0,"diluted_eps":46.33,"free_cash_flow":4875152000.0,"fcf_margin_pct":6.84,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/3665.TW/3665.TW_Q2_2026_Earnings_Call_20260821.md）

# Q2 2026 Earnings Call
**BizLink Holding Inc.** | Earnings Calls | 2026-08-21

**Ally Chen** (Analysts):
Okay. Good afternoon, and good morning. Welcome to join BizLink's Second Quarter Earnings Call hosted by UBS. I am Ally Chen, covering BizLink and the industrial sector in Taiwan. It's our honor to host BizLink management today. Now let me hand over the call to Mike Wang, the Senior IR Manager. Mike, please?

**Mike Wang** (Executives):
Thank you, Ally, for the intro. And once again, thank you to UBS for hosting our results call now. Good afternoon, everyone, and welcome to BizLink's Second Quarter 2026 Earnings Conference Call. My name is Mike Wang, Senior IR Manager. Joining me today are Roger Liang, our Chairman; Felix Teng, our CEO; and Charles Tsai, our CFO. Our earnings results were released earlier today and are available on our IR website, where you can download the latest earnings materials and access the call through MOPS. 
Today's call will begin with Felix, who will share strategic updates. Charles will then conclude with our financial highlights before we move to the Q&A session. You may submit your questions at any time through the public or private chat function, and we will address as many as time permits. Before we begin, please note that today's discussion may contain forward-looking statements based on our current expectations and are subject to risks and uncertainties. Actual results may differ materially. Please refer to the safe harbor notice in our earnings materials for further details. 
This call is being recorded and will be available on our IR website within 24 hours. With that, I would now like to turn the call over to Felix.

**Chien-Hua Teng** (Executives):
All right. Thank you, Mike. Good afternoon, everyone, and thank you for joining us. Before Charles discuss our second quarter financial performance, I would like to spend some time on how we see our markets evolving, what is changing in our customers' requirements and how BizLink is positioning itself for these changes. Over the past several years, BizLink has changed significantly. Connectors, cables and interconnect products remain important parts of our business, but they no longer fully describe where our business is heading. 
The more important question today is what engineering problems our customers need us to solve and whether we have the capabilities to solve them. AI infrastructure is entering a new phase. The first phase of this investment cycle was heavily focused on securing compute. That remains important, but the challenge is increasingly shifting towards deploying that compute at scale. As compute density rises, the infrastructure surrounding it has to keep pace. More power has to be delivered safely and efficiently. More data has to be -- have to move at higher speeds. 
Thermal and mechanical requirements are becoming more demanding. And increasingly, these systems need to be designed, manufactured and deployed together. This is why we continue to emphasize deployment first. The demand for compute is substantial, but compute only creates economic value after it is deployed and operating. The ability to deploy therefore depends not only on GPUs or accelerators, but on the availability and readiness of power, networking, cooling, mechanical infrastructure, facilities and utilities. 
As AI factories become larger, synchronization across the infrastructure layers become increasingly important. This also means deployment will not always be linear, thus, different points in the cycle, the constraints can shift from compute to networking, from networking to power or from equipment availability to facilities and utilities. This can create variability in procurement and deployment schedules even when the underlying requirement for this infrastructure remains strong. 
We believe this distinction between underlying demand and deployment timing is increasingly important. For BizLink, it also extends the opportunity. As performance requirements increase and systems become more complex, customers need suppliers that can address a broader range of engineering and manufacturing requirements. We have been building BizLink around that direction for several years. Well, how we frame the business. We do not view our strategy as building a collection of individual products. We view it as expanding the capability we can bring to customers. 
What began with traditional interconnect solutions has evolved to include power delivery, high-speed data connectivities, optical connectivities, engineering, new product introductions, advanced manufacturing and increasing broader system level integration. The value of this capability increases when they work together. Engineering allows us to engage earlier in the customers' deployment process. NPI converts engineering solution into products that can be qualified and manufactured reliably. 
Manufacturing allows those products to scale and system integration allows us to address a larger part of the customers' requirement. This is the direction in which we have been moving. We are already seeing this evolution across several business. In capital equipment, our scope has expanded from components towards higher-level assemblies and system integrations. Our engineering involvement is also increasingly -- increasing as customers engage us earlier in the development process. 
In HPC, we have expanded from traditional connectivity into higher-speed data solutions and increasingly sophisticated power solutions. Across the company, the common denominator is that our customers are asking us to do more. This is important strategically. The more capabilities we have, the more problems we can potentially solve. Earlier participation give us a better understanding of the customers' system requirements. 
And when we execute successfully, that creates opportunities to participate in more programs and more content over time. It also makes our business less dependent on the success of any single product or architecture. Individual products will change. Technology architectures will change. Customer requirements will change. Our objective is to build capabilities that remain relevant through those changes. This is one reason we have continued to expand both the depth of our products and the breadth of our capabilities. Greater product depth allow us to participate in more parts of our customers' system. Broader capabilities allow us to respond as the technology mix change. 
We do not need to predict every technology transition correctly. We need the engineering and manufacturing capabilities to remain relevant as those transitions occur. This is also why NPI has become increasingly important to BizLink. Engineering creates an opportunity, but engineering alone does not create revenue. The solution still has to be validated, qualified, industrialized and produced reliably at scale. 
NPI connects those stages. As our NPI capabilities strengthen, we can work with customers earlier, improve manufacturability, shorten the transition into volume production and build the operating knowledge required to support the program over its life cycle. This makes the relationship deeper than supplying an individual component. And as the system becomes more complex, customers increasingly value suppliers that can take on a broader part of that responsibility. 
This does not mean one supplier needs to do everything. It means the value of having suppliers with broader engineering, manufacturing and integration capabilities is increasing. That is where we want BizLink to compete. So what is changing? AI infrastructure provides the clearest example of the evolution today. Power requirements are rising rapidly as compute density increases. This is changing how power needs to be generated, transmitted and delivered all the way to the rack. 
At the rack level, the industry is evaluating multiple approaches, including higher temperature and higher voltage. We do not believe there will be one solution for every customer or every data center. Existing infrastructure matters, deployment schedules matters, reliability matters. The transition will, therefore, involve multiple power architecture operating at the same time. For BizLink, this is important because we are not dependent on one architecture winning. Our power capabilities span cables, busbars and increasingly higher power solutions. 
As customer requirements evolve, our objective is to support those requirements across different architectures. The direction is clear, more compute requires more power and higher power requirements create more engineering challenges throughout the infrastructure. These changes will also extend beyond the data center. The growth in AI-related electricity demand is accelerating investments across power generation, grid infrastructures and electrical equipment. 
As those systems become increasingly electrified, capabilities developed around power delivery, power management and higher density electrical systems can also become relevant to industrial automation, capital equipment and other end markets over time. Data connectivity is evolving in parallel. As compute clusters become larger, more data needs to move within and between those systems at higher speed. 
Copper continue to play an important role, particularly where distance and system architecture allow it. At the same time, optical connectivity becomes increasingly important as bandwidth requirements and transmission distances increase. We have capabilities in both. Our position in copper connectivity continues to evolve with higher-speed architectures, while XFS has materially expanded our optical capabilities. We do not see this as a simple transition from copper to optics. Different systems architectures will require different combinations of both, and those requirements will continue to evolve. 
For BizLink, the strategic point is straightforward. We can participate across power, copper and optics. This gives us more than additional content opportunities. It gives us greater flexibility as customer architectures evolve. If content shifts between technologies, our objective is to participate in the transition rather than depend on one technology outcome. As these infrastructure layers become more closely connected, that breadth becomes increasingly valuable. And importantly, we do not expect the industry to change every part of the infrastructure at the same time. 
Customers need to deploy. New technologies, therefore, have to coexist with existing infrastructure and architecture transitions will occur at different speeds, depending on the customers and applications. This reinforces our view of deployment first. The winning solution is not necessarily the newest architecture in isolation. It is a solution that allows customers to bring reliable compute capability capacity online at the scale and timing they require. 
Our execution strategy follows directly from these changes if customers' requirements are becoming broader, our capability needs to become broader as well. We continue to invest organically in engineering and NPI. We are expanding manufacturing capabilities and -- capacity and capabilities where customer demand supports those investments. We are increasing the level of system integrations we can provide, and we continue to evaluate strategic investments where acquiring an established capability can accelerate our progress. 
Our global footprint is an important part of this strategy. Customers increasingly require suppliers that can support them across multiple regions while maintaining consistent engineering, quality and manufacturing standards. We, therefore, continue to invest in our manufacturing network where we see sustained customer requirements. But strong demand does not mean we need to pursue every available opportunity. We remain selective in how we allocate capacity and capital. 
We prioritize programs where our capabilities, customers relationship and expected returns justify the resources required. This is particularly important in the current environment. We do not intend to build capacity simply because demand expectations are high. Capacity expansion needs to be supported by customers' requirements and attractive long-term economics. We also actively manage how existing capacity is used. 
As our business mix evolves, we can reallocate manufacturing space, equipment and organizational resources toward opportunities where we see stronger growth, greater strategic value or better returns. In some cases, this may mean allowing more mature business to roll off rather than adding capacity simply to preserve revenue. Our objective is, therefore, not to maximize revenues at any cost. It is to allocate our resources towards the opportunities where BizLink can create the greatest long-term value. This discipline is important because capacity decisions made during periods of very strong demand can affect returns for many years. 
We want to participate fully in the growth opportunities ahead of us without building the company around the assumption that every demand signal will continue, indefinitely. At the same time, we are seeing increasing opportunities to participate earlier in customer projects. Earlier engagements allow us to contribute more engineering value and give us a better understanding of how the complete system is evolving. 
The progression we are pursuing is clear. Earlier engineering engagement, stronger NPI, scalable manufacturing and broader system integration. This is also how we approach M&A. We evaluate acquisitions based on more than their immediate revenue contribution. We look for capabilities, technologies, customer relationships, geographic reach and other strategic strengths that can make BizLink more competitive over time. 
Increasingly, we also think about M&A through the durability of the capabilities we acquire. Individual products can have relatively short technology cycle. A strong engineering design or manufacturing capabilities can potentially remain relevant across multiple product generations, customers and end markets. That matters to how we allocate capital. We prefer strategic assets that strengthen what BizLink is capable of doing rather than simply adding exposure to a product that is attractive at one point in the cycle. 
The contemplated acquisition of Interplex Datacom fits our broader capability expansion framework. It should not be viewed as a change in BizLink's strategic direction, but rather as another step along the path we have been following for many years. Interplex Datacom's capability in mechanical engineering, precision manufacturing and design would implement BizLink's existing -- complement BizLink's existing strengths across electrical, optical, power and manufacturing engineering. 
Following closing, we believe this complementary capabilities will broaden the engineering and manufacturing capabilities available across the BizLink platform, particularly where mechanical and electrical requirements increasingly intersect. Because the transaction has not yet closed, Interplex Datacom remains a separate business, and we will, therefore, remain disciplined about what we discussed before closing. 
Our broader acquisition philosophy remains unchanged. We will continue to develop capabilities organically where that is the best approach. We will consider acquisitions when they can accelerate our strategy, and we will remain selective. The objective is not simply to make BizLink larger. The objective is to make BizLink more capable. 
So what this means going forward? Looking forward, we see a larger opportunity set for BizLink than we had several years ago. AI infrastructure is creating new requirements across power, data connectivity, thermal and mechanical systems. Semiconductor production equipment is becoming more complex and creating opportunities for greater engineering and system integration content. Industrial automation, transportation, health care and other markets continue to evolve towards higher level of electrification and automation. 
This market will not grow at the same rate every quarter. We also do not expect the current AI investment cycle to move in a straight line. The scale and pace of investment across AI infrastructure today are significant. We remain constructive on the structural opportunity, but investment cycle of this magnitude will include periods of acceleration and period of digestion. Our responsibility is not to predict every turn in that cycle. It is to ensure that BizLink is positioned to capture the upside while remaining resilient if conditions change. 
Our strategy is increasingly designed around that flexibility. We are building depth across products so that we can participate as customers' requirements move between technologies. We are building broader capabilities that can remain relevant across multiple products and markets. We are selective about the demand and capacity we pursue, and we continue to diversify the earnings base of the company. 
We do not need perfect visibility into every technology transition or every point in the investment cycle. We need the ability to adapt as those conditions change. We are not building our strategy on the assumption that today's rate of investment continue indefinitely. We are building the company so that we can capture the structural opportunities through different parts of the cycle. 
Across BizLink, our strategy remains consistent. We want to participate earlier. We want to solve more complex problems. We want to increase our content and value to customers, and we want to convert those capabilities into sustainable long-term growth. Our opportunity is no longer defined by any single product. It is increasingly defined by the range of problems BizLink is capable of solving. 
With that, I will turn the call over to Charles.

**Tse-Shen Tsai** (Executives):
Thank you, Felix, and good afternoon, everyone. Felix has discussed how our opportunity set and capability are evolving. And I will focus on what that evolution means financially. Our second quarter performance, the economic of the business as we scale, the breadth of our growth drivers and how we're managing our capital structure following the recent fundraising. 
So for the second quarter of 2026, consolidated revenue was TWD 23.28 billion, representing a 37% year-over-year growth and 12% sequential growth. Gross profit was TWD 7.15 billion with gross margin of 30.73% compared with 28.77% in the first quarter. Operating profit was TWD 4.01 billion with operating margin of 17% compared with 14.9% in the first quarter. Net income attributable to shareholders was TWD 2.98 billion and EPS was TWD 15.28. Net income and EPS reached a new quarterly high. 
The second quarter showed a clear improvement from the first quarter. Revenue increased sequentially, utilization improved and the operational issues that affect our first quarter profitability began to normalize. Last quarter, we explained that gross margin was affected by several factors occurring at the same time, including product transition, customer deployment schedule, foreign exchange and business mix. 
During the second quarter, we focused on the areas that we can control. The first is cost efficiency. As volume improved, utilization improved with them, we continue working on manufacturing efficiency, material cost, productivity, execution across our operations. The second is operating expense efficiency. We continue to invest where necessary to support growth, but the organization also needs to become more efficient as the revenue base expands. 
Importantly, the improvement in the second quarter was not simply a function of higher volume. We also made progress in addressing the operational issues that affected the first quarter while continuing to improve manufacturing efficiency, material cost productivity and operating efficiency across the organization. The result this quarter show progress in both areas. We should also be clear about how we manage the business. Our objective is not to maximize gross margin in a particular quarter. 
Our business model is to deliver strong scale growth at healthy and sustainable margins. Margin will move from quarter-to-quarter because of product mix, customer mix, utilization, foreign exchange and program timing. We expect that. What matters is whether we can maintain reasonable profitability while expanding the absolute earnings and cash generation capacity of the company. 
The second quarter is a strong demonstration of that model. So BizLink today is materially larger than it was several years ago. For several years, we focused on improving the quality of the business. We improved gross margin. We improve operating efficiency. We maintain discipline around operating expenses. We improved cash generation, and we became more selective about where we deploy capital. Those priorities remain. 
But the next stage of BizLink's development is not about maximizing any one financial ratio. It's about maintaining healthy economics while continuing to scale. A healthy margin on the larger revenue base generates greater operating profit, greater net income and greater cash flow. That increased earning capacity give us more resources to invest in customer program, technology, capacity, people and strategic opportunities. 
The important point is that scale and profitability have to work together. Growth without adequate return does not create sustainable value. But maximizing margin by walking away from attractive growth opportunity is also not how we intend to manage that company. Our objective is to capture growth where we have a competitive advantage while maintaining disciplined profitability and returns. 
This is increasingly relevant because the composition of BizLink's business is changing. Our growth business are becoming larger. Our engineering content is increasing. Our system integration capability are expanding. And in several businesses, we are moving closer to the customer and participating in more of the value chain. This create opportunity to increase both the size and the quality of our earnings base. We're already seeing that financial impact of that evolution. We can see this change in how we engage with customers. 
Across several of our higher growth businesses, our participation is moving beyond individual components toward broader assembly subsystem and engineering solutions. We're also becoming involved earlier in customer development cycle and supporting more complex programs. This increased the value that we can provide to customers and expand the opportunity available to BizLink with each program. 
So what is changing? The source of the growth across BizLink are becoming broader. AI infrastructure remains one of our strongest structural growth drivers. The underlying demand for compute is -- remains strong. And as Felix discussed, the infrastructure required to deploy the compute is expanding across power, connectivity and other areas. 
Another important characteristic of this business is that we are participating across multiple technology generations at the same time. While today's generation is already contributing to our revenue and profit growth, our engineering team are working with customers on future platforms. In some areas, that work already extend beyond the next generation into N+2 solutions. So this matter because each generation is becoming more demanding. 
Power density is increasing, data speed are rising and system requirements are becoming more integrated. Early participation allow us to accumulate engineering knowledge, qualification, experience and customer trust that can carry forward into subsequent generations. As a result, the capabilities supporting today's earnings also help position us for future opportunities. 
At the same time, we do not assume that the current pace of AI infrastructure investment will continue in a straight line. Large investment cycle inevitably include changes in deployment timing, capacity digestion and shift in where capital is being directed. We do not need to predict exactly when those changes will occur. We need to manage BizLink so that we can continue creating value through them. That's start with the quality of the demand we choose to support. 
We do not need to address every unit of incoming demand. When demand is strong, it can be tempting to add capacity simply to capture additional revenue. We do not believe that is always the right decision. We evaluate the capital required, the expected return, the strategic importance of the program and whether existing resource can be redeployed before committing incremental capacity. This allows to participate in attractive growth without automatically converting every increase in demand into higher capital intensity. 
Over time, we intend to keep capital expenditure discipline relative to the scale of the business and broadly consistent with the way we have historically managed capital intensity. There may be periods where strategic investment justify higher spending, but the principle is clear. We will not build capacity simply because demand expectations are high. Capital has to be supported by customer requirements and expected returns. 
Product and capability depth provide another form of resilience as Felix discussed, broader participation across technologies give us greater flexibility as architecture evolves. From a financial perspective, that matter because our growth does not have to depend on one product or one technology outcome. The same principle apply to strategic investment. When we invest in capability that can support multiple product, customer or end market, we create more ways to generate return from that investment over time. 
We believe this is a more durable approach that -- than concentrating capital around narrow product opportunities simply because the demand is strong today. Capital equipment has become another important structural growth engine. AI is increasingly -- is increasing manufacturing complexity across advanced logic, memory and packaging, supporting continued investment in increasingly sophisticated semiconductor equipment. 
Our role in this market has expanded from component toward high-level assembly and system integration with deeper engineering engagement and participation in more complex, higher-value programs. This is already translating into accelerating growth with quarterly sales reaching a new level. Today, we have reasonable order visibility extending into the second half of 2027, while discussions with customers are already beginning to extend into 2028. We are preparing for the next stage of growth by deepening our engineering engagement and expanding our subsystem capabilities. 
We also see a gradual recovery across our broader industrial businesses. The recovery is not uniform and different end markets are moving at different speed, but the direction has improved. This gives us multiple source of growth rather than requiring one business to carry the entire company. Our diversification is, therefore, not simply defensive. It allows us to participate in multiple structural growth opportunity while giving us greater flexibility in where we allocate capital and capacity. 
So how we're executing. This brings me to a capital allocation and capital structure. Following our recent fundraising, I want to be clear about how we think about both. We manage our balance sheet against a clear internal financial framework. This framework is our North Star for how much leverage and liquidity we believe are appropriate for BizLink. We do not need the balance sheet to remain at exactly the same position at every point in time. 
Working capital changes, we invest in capacity. We pursue strategic opportunity, and there may therefore be a period where the balance sheet moves away from our preferred position. But we operate within defined guardrails. If the balance sheet moves outside of this guardrail, we will take the necessary steps to bring it back to our preferred position. That discipline does not change with market sentiment. This is how we intend to manage the company through different part of the cycle. 
Our recent financing reflects this philosophy. We had alternatives, including relying more heavily on debt financing. We chose not to do that. We believe maintaining a stable balance sheet is the right approach for BizLink, particularly as the size of our customer program and investment opportunity continue to increase. This is also why we chose to support our growth through a combination of equity and equity-linked capital. We believe that when capital is deployed well, it should create long-term value for our customers, our BizLinkers and the community where we operate as well as our shareholders. 
Over the years, as we execute our strategy, the value of BizLink has grown substantially and the market's recognition of that strategy has grown with it. Our responsibility is to continue earning that recognition by converting the capital entrusted to us into greater capability, stronger earnings and sustainable long-term value. Greater financial capacity expands our choices. It does not change our financial discipline or lower our return requirement. 
Our capital allocation priorities remain consistent. We first invest in the existing business where customer demand and expected return justify the investment. That includes working capital, engineering, technology, capacity, automation and NPI. But before adding capacity, we also evaluate whether existing resource can be used more effectively. As our business mix changes, we can shift resource away from more mature programs toward opportunity where we see stronger growth, greater strategic importance or better economics. 
This is how we manage capital intensity. We do not measure success by how much capacity we have, but by what the capacity allows the company to earn. Not every incremental dollar of revenue deserve the same amount of capital. We will remain selective and prioritize opportunities where customer importance, strategic fits and expected returns justify the resource required. We can see the result of this discipline in our returns as BizLink has grown, both our return on equity and return on investment capital have improved meaningfully over the past several years. We view this as an important measure of the quality of our growth. 
Our objective is not simply to make the company larger, but to deploy capital in ways that generate attractive return over time. Following our recent financing, that responsibility become even more important. We can now have greater financial capacity and our job is to convert that capital into capability and earnings while maintaining disciplined return. Capital allocation also extends beyond physical capacity. As BizLink grows, we need more than factory and equipment. We need engineers who can solve increasingly complex customer problems. 
NPI team, they can convert those solutions into scalable production, leaders capable of managing larger and more geographically diverse operations and digital system and processes that allow our team to operate efficiently across the global company. This investment may not produce immediate revenue, but they are necessary to support sustainable earnings growth. 
We also evaluate strategic opportunities through M&A. Our approach is increasingly capability led. We look for engineering, design, manufacturing, technology, customer or geographic capability that can strengthen the broader company. We prefer capability that can remain valuable across multiple product customers and technology cycles rather than building our strategy around any single product opportunity. 
The contemplated Interplex Datacom acquisition is one example of how we may deploy capital when we identify a strategic opportunity that meet our long-term objective and return criteria. As the transaction has not yet closed, Interplex Datacom remains a separate business and has not contributed to our reported results. Strategic opportunity do not necessarily appear when internally generated cash is most abundant. This is another reason we value maintaining financial flexibility. BizLink itself is becoming larger. 
Our customer programs are becoming larger and the investment required to support those opportunities are also increasing. A strong balance sheet give us the ability to act when an opportunity meet our strategic and return requirement without compromising the operating needs of the rest of the company. That is the purpose of financial capacity, not to spend more, but to ensure that capital availability does not become a constraint when the right opportunity appear. 
So looking forward, we believe BizLink is entering the next stage of its development from a much stronger position. The earning base is larger, our structural growth drivers are broader, our product and capability depth are greater, our engineering and manufacturing capability are deeper. Our customer relationship increasingly span more product, program, geography and our financial capacity has increased. Our responsibility is to convert those advantage into sustainable value. 
The process is straightforward. We need to convert customer opportunity into earnings. We need to convert earnings into cash. We need to allocate that capital with discipline, and we need to reinvest where we see attractive long-term returns. As we do that, we will maintain several discipline. We will remain selective about the demand we pursue. We will manage capital intensity rather than automatically adding capacity. We will continue reallocating resources as our business mix evolves. 
We will favor capability that can remain relevant as product and technology change, and we will manage the balance sheet against financial guardrails that we have established. This discipline becomes more important when markets are strong. The scale of investment occurring across AI infrastructure today is significant, and we remain constructive on the long-term opportunity, but we're not managing BizLink on the assumption that today's demand environment continue indefinitely. 
There will be a period of acceleration. There will be a period of digestion. Technology will change, and there will be changes in where the bottleneck sit. We do not need to predict each one. We need a business model that can adapt to them. This is why product and capability depth matter. This is why diversification matters. This is why capital discipline matter, and this is why we maintain financial guardrails. 
The second quarter give us greater confidence in this model. We have returned to sequential growth. Profitability has improved from the first quarter and our absolute earnings continue to demonstrate the benefit of greater scale. Looking further ahead, we remain constructive on AI infrastructure. We remain constructive on capital equipment. We're seeing improving conditions near across all parts of our industrial portfolio, and we continue to see opportunity to expand our content and capability across the customer end market we serve. 
We do not need every business to grow at the same rate every quarter. We need each business to create value over time, and we need to allocate capital toward the opportunity where BizLink has strongest competitive position and the most attractive returns. Our objective is clear: grow the earnings base, maintain healthy profitability, allocate capital selectively and preserve the strategic and financial flexibility required to keep investing through the cycle. This is how we intend to create sustainable long-term value for our shareholders. Thank you. 
So now let me turn the call over to Mike.

**Mike Wang** (Executives):
Thank you, Felix and Charles. This concludes our prepared statement section. Now let us begin the Q&A section. [Operator Instructions] I want to remind everyone that there will be no forward-looking quantitive comments. Looking at some of the questions, I think the one that we want to address first is the one on our competitive position. 
And this one to kind of give you an idea what sort of a summary of what's being asked, as competitors broaden their AI infrastructure portfolios, how do you think about BizLink's competitive position and ability to maintain or increase content? So for this one, I'd like to hand over to Roger to provide a little color on that.

**Hwa-Tse Liang** (Executives):
All right. Thank you, Mike. We are seeing more competitors span across data connectivity, power and optics. Our strategy is not to pursue price for its own sake, but to build deeper positions where performance requirements are high, qualification is difficult and customer value reliability and the types of market. High-speed copper is a good example. Multiple generation of developers and qualification have built engineering know-how, manufacturing experience and customer relationships. That position has helped us accelerate into power and capability and the system level knowledge we build in power that support our development in optics. 
We therefore see copper, power and optics increasingly reinforcing one another. Being early matter because this market do not reset with every each generation. An incumbent supplier enter a next architecture with qualification history, customer relationship and manufacturing experience. Later entrants need to catch up while the technology itself continues moving forward. The increasing complexity of AI infrastructure made these steps more valuable. Higher data rates, higher power density and the liquid cooling increasingly require electrical, mechanical, thermal and manufacturing capability to work together. 
Customers need suppliers that can solve engineering problem, qualified solution and scale them reliably. We can also use targeted M&A to add complementary capability when that is faster or more effectively building everything organic. Combined with organic development, this can shorten our strategic road map. So we believe our advantage can compound over time. Being ahead today can help us enter the next generation early, move faster and potentially widen that lead as AI infrastructure becomes more complex.

**Mike Wang** (Executives):
Thank you, Roger, as well as thank you to those who put the question on competition. There seems a lot of interest on optics. So this is the next question. Can you update us on the progress of the optics business and how you see the opportunity developing over the next several years? So for this one, I'd like to hand it over to Felix.

**Chien-Hua Teng** (Executives):
Okay. Thank you, Mike. Yes. So we see optics as a structural extension of our data connectivity business. So yes, as AI clusters become larger and more complex, bandwidth requirements continue to increase. But the opportunity is about more than successive transitions from 800G to 1.6T and naturally higher speed. So yes, density becoming increasingly important. The opportunity is also broadening as optics move closer to system level through architectures such as optical circuit switching and NPO CPO, which is very -- I mean, many people have heard about that. 
And so this technology may develop on different time lines. But collectively, they point towards greater optical complexity. So importantly, we see both greenfield and also installed base opportunities. The new AI will be designed with greater optical content from the beginning. And I mean, however, the current existing hyperscaler infrastructure can be upgraded or evolved with the network's architecture change. 
So with the environment, we see -- actually, we see more and more the demands and also inquiries about our solution, optical solutions. And XFS gives BizLink an established position in fiber assemblies, harnesses and also related optical connectivity solutions. So we are, therefore, not trying to predict exactly which optical architecture wins or when each transition occurs, but almost every task towards larger and denser AI infrastructure requires more sophisticated optical connectivities. And indeed, XFS give us a meaningful platform from which to participate in that evolution.

**Mike Wang** (Executives):
Thank you, Felix. Of course, thank you to those who post those questions on optics. Now let me turn to some financial questions. Everybody is asking about what we see about margin trajectory, the second quarter that we just reported, and of course, what we see going forward. So for this one, second quarter profitability improved sequentially. How should we think about margin trajectory into the second half, particularly seeing the change in business mix and new platform ramps? Which is perfect question for our CFO, Charles.

**Tse-Shen Tsai** (Executives):
Okay. Thank you, Mike, and thank you, everyone. I think the first point I would like to make is that the second quarter showed the improvement that we expected from the first quarter. Revenue increased sequentially, operating condition improved and some of the factors that affected first quarter profitability began to normalize. So we also continue working on the areas we can control, particularly in the manufacturing, efficiencies, material cost productivity and operating expense efficiency. 
So looking into the second half, I think we remain constructive. But I would not suggest modeling gross margin as a straight line upward every quarter as we discussed before, the product transition, customer deployment cycle, foreign exchange, business mix, they can all create quarter-to-quarter fluctuation. So we're managing business for a stable and reasonable margin while growing that earnings base. 
Also, I think it's the more important is what is happening underneath the margin. The higher growth business are becoming larger. So our engineering content is increasing. And in several areas, we're moving closer to customer and participating in more value chain. So at the same time, some of our more mature business are also beginning to recover. So we're increasing both scale and mix that's working for us. 
So that does not mean that margin will increase -- will increase indefinitely. So what it means is that if we can maintain a healthy margin while growing the revenue base and improving operating efficiency, the absolute earnings and cash generating capacity of the company can continue to increase. So that is the financial model that we're trying to build. So I hope that answers your question.

**Mike Wang** (Executives):
Thank you, Charles, and thank you to those who posted the questions on margins. So we have one. We can do one more question. So yes, we will address some of these questions offline. There's -- we're still through some of these questions, but I think something else to tie off this is also financial-wise, continued questions around our spending, CapEx, right, I would say it in the slide on that. So for this one, the last question for this call, with demand remaining strong across HPC and other growth businesses, how are we thinking about capacity expansion and capital intensity over the next 1 to 2 years? So again, a financial question, I hand this over to Charles.

**Tse-Shen Tsai** (Executives):
Okay. Thank you, Mike. I think the first thing is that we will definitely continue to invest because the opportunity set in front of us is expanding. So -- but our approach to capacity has not changed. We do not believe that every dollar incoming demand should automatically result in another dollar of capacity. So we look at our priority. We have priority. We have strategic fit. We have return requirement. We have durability of the opportunity and whether the existing resources can be first used to be more effective. 
So our business mix changes, we can reallocate resources, capacity supporting more mature programs can sometimes be redirected to faster growing or higher value opportunities. So automation and productivity improvement can also generate additional output without requiring the same level of incremental physical capacity. So CapEx is only one part of how we support growth. So where do we invest? The requirement is increasingly broader than factory space and equipment. We're investing in engineering. We're investing in technology. We're investing in qualification, automation. We're investing in manufacturing capability, also in people, in system, in organizational infrastructure that require to support a larger company. 
So we therefore intend to manage capital intensity with the discipline and remain mindful of historical experience rather than building capacity simply against higher possible demand scenario. We are willing to leave some business on the table if the economic and strategic value and durability of that demand do not justify the capital required. So at the same time, we will maintain a clear internal financial framework around our balance sheet. We don't need the balance sheet to remain just exactly the same. 
So if we move away from our preferred position, we will just take necessary steps to bring it back to other position. So I think the important thing is that greater financial capacity also give us choices. So it does not really -- but it does not really lower our hurdle rate. So I hope that address your question.

**Mike Wang** (Executives):
Thank you, Charles. And thank you for those who posted questions on that. And finally, thank you, Roger, Felix and Charles. This concludes our Q&A session. A replay of the conference call today will be available on our IR website within 24 hours from now. If you have any further questions, feel free to reach out to BizLink's Investor Relations, so it will be me or Jimmy. We thank you very much for joining today's call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 3665.TW_Q1_2026_Earnings_Call_20260512.md
- 2026-05-12｜Mike Wang｜guidance：主持人聲明本場不提供前瞻性量化評論（原話："there will be no forward-looking quantitative comments"）
- 2026-05-12｜Charles Tsai (CFO)｜margin：CFO 將毛利/營運槓桿壓力歸因於世代轉換：舊品下滑、新世代爬坡初期、產能利用率與產品組合尚未到位（原話："our legacy solution are declining as expected, while next-generation programs are still in early stage of ramp"）
- 2026-05-12｜Charles Tsai (CFO)｜margin：CFO 列出重疊期的三項壓力來源：舊品價格正常化、新案爬坡低效率、多世代並行的營運複雜度（原話："legacy pricing normalization, early-stage ramp inefficiency for newer programs and elevated operational complexity"）
- 2026-05-12｜Charles Tsai (CFO)｜margin：CFO 稱目前毛利狀況屬轉換與重疊階段，並非長期軌跡改變（原話："the current margin profile is best understood as part of the transition and overlap phases"）
- 2026-05-12｜Charles Tsai (CFO)｜margin：CFO 稱長期營運槓桿不變但逐季未必線性，並提到本季營業利益層級顯示費用控管（原話："it still show that we have strong OpEx discipline"）
- 2026-05-12｜Charles Tsai (CFO)｜margin：CFO 描述新平台初期的成本結構：量小、前期工程與營運成本高（原話："newer platform typically begin with lower initial volume and higher upfront engineering and operational costs"）
- 2026-05-12｜Charles Tsai (CFO)｜risk：銅與 PVC 原料成本持續上升，引發部分供應鏈的價格討論，公司選擇性調價（原話："We are selectively adjusting pricing where appropriate while continuing to support customer ramp requirements."）
- 2026-05-12｜Charles Tsai (CFO)｜risk：供應鏈緩衝庫存與急單減少，部署時程差異在近期更為明顯（原話："which means timing difference are more visible in the near term"）
- 2026-05-12｜Charles Tsai (CFO)｜risk：擴產與營運整備可能暫時影響近期效率（原話："this effort may temporarily impact near-term efficiency"）
- 2026-05-12｜Charles Tsai (CFO)｜competition：家電業務在部分品類因產業產能過剩與客戶競爭而仍具競爭性壓力（原話："electrical appliances remain competitive across selected product categories due to industry overcapacity"）
- 2026-05-12｜Charles Tsai (CFO)｜customer：工業與車用狀況逐步改善，來自特定客戶活動與試產案（原話："industrial and automotive conditions continue improving gradually"）
- 2026-05-12｜Charles Tsai (CFO)｜customer：半導體設備端近期投資節奏較為溫和，但能見度仍屬健康（原話："a more measured near-term investment cadence in certain areas of semiconductor ecosystem"）
- 2026-05-12｜Florian Hettich (COO)｜risk：COO 稱檳城的主要挑戰在營運擴張與勞動力能力培養，而非需求（原話："our primary challenge remains operational scaling and labor capability development rather than demand generation"）
- 2026-05-12｜Florian Hettich (COO)｜product：COO 稱 AI 基礎設施趨向機櫃層級設計（原話："One of the clearest shifts is that AI infrastructure is becoming rack-centric."）
- 2026-05-12｜Hwa-Tse Liang (Chairman)｜product：HPC 布局涵蓋銅互連、光連接與電源傳輸三層（原話："copper interconnect, optical connectivity and power delivery"）
- 2026-05-12｜Hwa-Tse Liang (Chairman)｜competition：董事長稱公司策略不依賴單一架構結果，多種電源／光／互連路線將並存多年（原話："our strategy is not dependent on any single architecture outcome"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜product：CEO 說明鑫福盛（XFS）自 1 月初併入，Q1 反映與 2025 大致一致的基線（原話："we consolidated the business starting early January"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜product：CEO 指出 4 月活動明顯回升，但仍定性為早期階段（原話："particularly into April, is a meaningful pickup in activities"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜commitment：CEO 表示需再觀察數季穩定表現才對 XFS 軌跡下結論（原話："we would prefer to see a few more quarters of consistency before drawing firm conclusions on the trajectory"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜guidance：XFS 近期營收貢獻取決於客戶部署步調與時程（原話："near-term revenue contribution will still depend on the pace and timing of customer deployments"）
- 2026-05-12｜Florian Hettich (COO)｜competition：COO 回應銅 vs 光：不視為二元取代，兩者並存（原話："we do not view this as a binary transition where one technology is just replaced by another"）
- 2026-05-12｜Charles Tsai (CFO)｜capital_allocation：CFO 說明資本支出採能見度驅動、紀律式節奏，擴產地點含 Batam、Tainan、Penang、Johor、Vietnam（原話："disciplined and visibility driven rather than speculating"）
- 2026-05-12｜Charles Tsai (CFO)｜commitment：CFO 稱投資步調對應客戶專案能見度與營運成熟度，而非短期需求波動（原話："pacing investment alongside customer program visibility and operational maturity"）
- 2026-05-12｜Hwa-Tse Liang (Chairman)｜capital_allocation：董事長稱長期併購策略不變，採能力導向、選擇性，並維持估值與整合紀律（原話："long-term M&A strategy remains the same, unchanged"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜commitment：CEO 稱目標不在單純加快成長，而是建立可跨週期擴展的長期能力（原話："our objective is not simply to grow faster"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜guidance：CEO 稱處於 AI 基礎設施投資週期的非常早期階段；季度部署時程仍會變動（原話："we are, again, in a very early stage of the AI total development investment cycle"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜guidance：CEO 稱季度部署時程仍可能因客戶排程而變動，但整體建置呈多年累積性質（原話："quarterly deployment timing can still vary depending on customer schedules"）
- 2026-05-12｜Florian Hettich (COO)｜product：COO 稱電壓提升由物理與效率驅動，客戶仍在評估不同 HVDC 與機櫃配電方案，預期多路徑並存（原話："we are therefore, expect multiple pathways to coexist"）

### 問答異常語氣（迴避／改口／保留）
- 3665.TW_Q1_2026_Earnings_Call_20260512.md｜問：毛利低於預期的具體原因與復原路徑（Morgan Stanley、BofA 等）｜答法：管理層以世代轉換／產業結構論述作答，未給出毛利數字、各項壓力的量化拆解或復原時點；僅稱「隨新案放量自然抵銷」
- 3665.TW_Q1_2026_Earnings_Call_20260512.md｜問：光學／XFS 的商機與放量軌跡｜答法：未給 XFS 營收或放量數字；稱 Q1 為與 2025 一致的基線、4 月回升，並表示需數季一致表現才下結論
- 3665.TW_Q1_2026_Earnings_Call_20260512.md｜問：營運槓桿與長期獲利力（含工程密集度與光學投資）｜答法：僅稱長期槓桿「intact」、路徑逐季不線性，未給時點或幅度
- 3665.TW_Q1_2026_Earnings_Call_20260512.md｜問：CapEx 與製造擴張規模；HPC 能見度；48/54V 與 800V HVDC 母排 ASP 差距｜答法：CapEx 與能見度問題未給金額或訂單量；ASP 提升幅度的提問未被直接回答，改談物理與架構

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
{"status":"no_prior_dd"}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3665.TW_20261012/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
