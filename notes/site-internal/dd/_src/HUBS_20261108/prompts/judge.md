你是 stock-analyst **v20 判斷 agent**，標的 HUBS（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"HUBS","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBS_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBS_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":947.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益","value":214.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm"}},{"id":"f_kpi2_non_gaap","label":"Non-GAAP 營業利益率","value":22.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm"}},{"id":"f_kpi3_gaap","label":"GAAP 營業利益","value":71.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm"}},{"id":"f_kpi4_gaap","label":"GAAP 營業利益率","value":7.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm"}},{"id":"f_kpi7","label":"客戶數","value":311704,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"家","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm"}},{"id":"f_kpi8_non_gaap","label":"訂閱毛利率（Non-GAAP）","value":85.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm"}},{"id":"f_kpi9_calculated_billings","label":"Calculated billings","value":924.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm"}},{"id":"f_kpi10_q4_2026","label":"指引：Q4 2026 營收","value":946.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M（區間 945.0–947.0）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm"}},{"id":"f_kpi11_fy2026","label":"指引：FY2026 營收","value":3686.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M（區間 3,685–3,687）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_hubs_gross_margin_pct","label":"HUBS 毛利率","value":83.02,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HUBS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hubs_operating_margin_pct","label":"HUBS 營業利益率","value":5.45,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HUBS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hubs_fcf_margin_pct","label":"HUBS FCF 利潤率","value":18.89,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HUBS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_crm_gross_margin_pct","label":"CRM 毛利率","value":77.28,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crm_operating_margin_pct","label":"CRM 營業利益率","value":21.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crm_fcf_margin_pct","label":"CRM FCF 利潤率","value":34.49,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_now_gross_margin_pct","label":"NOW 毛利率","value":73.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_now_operating_margin_pct","label":"NOW 營業利益率","value":9.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_now_fcf_margin_pct","label":"NOW FCF 利潤率","value":30.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_team_gross_margin_pct","label":"TEAM 毛利率","value":84.83,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TEAM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_team_operating_margin_pct","label":"TEAM 營業利益率","value":0.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TEAM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_team_fcf_margin_pct","label":"TEAM FCF 利潤率","value":20.07,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TEAM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mndy_gross_margin_pct","label":"MNDY 毛利率","value":88.74,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNDY.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mndy_operating_margin_pct","label":"MNDY 營業利益率","value":2.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNDY.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mndy_fcf_margin_pct","label":"MNDY FCF 利潤率","value":21.56,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNDY.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_non_gaap_fcf","label":"Non-GAAP 自由現金流（FCF）","value":188.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm"}},{"id":"f_kpi6_sbc","label":"SBC（股權報酬費用）","value":127.1,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":200.61,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":1.66,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":33.76,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.3 → 13.3）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.82 → 16.82）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.21 → 20.21）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":13.3,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":16.82,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":20.21,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.15,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 13.28 → 13.3（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":48.46,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"2 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":2.73,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.43,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":15.08,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 13.3，分子＝快照價 200.61","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-1072.72,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 224.04、現金 1296.76（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":48.84,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":8724.36,"period":"2026-11-08","unit":"USD m","basis":"市值 9797.08 ＋ 淨負債 -1072.72","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":3687.28,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（29 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":4108.03,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（31 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.37,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 200.61 / W52 256.6 / W104 425.37 / W250 445.12 / W250 13週斜率 -1.0%"},{"id":"f_ma_w52","label":"52 週均線","value":256.6,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":425.37,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":445.12,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-1.0,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"HubSpot 10-K FY2025 的競爭對手清單新增「AI agent 提供者」與「AI-native CRM 及工作流自動化新創」，並提到通用 LLM、vibe coding 等非專業方案可能搶單。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm","excerpt":"•data enrichment vendors; •AI agent and providers; •AI-native CRM and workflow automation startups; and •large-scale enterprise suites.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：公司可能面對依賴通用 LLM、生成式 AI 與通用 agent 的非專業方案競爭，需說服客戶其產品優於 vibe coding 等替代；對手可能以綑綁近零成本提供平台，迫使降價。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm","excerpt":"We may also face greater competition from non-specialist solutions relying on generic large language models (“LLMs”), generative AI and general-purpose agents to address a broad range of business needs.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"SaaStr 2026 摘要稱多數現今 YC 新創已不使用 Salesforce 或 HubSpot（新進入者／AI-native CRM 趨勢）。","source":"NextGenABM: key takeaways from SaaStr AI 2026","url":"https://www.nextgenabm.io/post/from-ai-inside-crm-crm-rebuilt-around-agents-key-takeaways-from-saastr-ai-2026","excerpt":"Salesforce and HubSpot are doing what incumbents do: layering agents across what they already have. Salesforce is buying its way there: Agentforce, plus recent acquisitions like Qualified (inbound agent) and Momentum (auto-transcribes every call into the CRM).","as_of":"2026-05-18","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Solutions Partners 及其轉介客戶約占 2025 年營收 49%（占客戶數約 25%），屬通路集中而非單一客戶集中。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm","excerpt":"Solutions Partners and customers referred to us by our Solutions Partners represented approximately 25% of our Customers as of December 31, 2025, and approximately 49% of our revenue for the year ended December 31, 2025.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"訂閱收入占 98%，多數訂閱期限一年或更短；10-K 信用風險集中段僅列現金、投資、應收帳款，未見單一客戶集中揭露。","source":"SEC EDGAR 10-K FY2025 Item 7 / Item 8","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm","excerpt":"Most of our Customers’ subscriptions are one year or less in duration.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"HubSpot Q3'26 營收年增17%；客戶數311,704、年增12%；客戶成長主要來自低價 Starter 產品需求，單客平均訂閱營收$12,038、年增4%。","source":"HubSpot 10-Q FY2026 (period 2026-09-30) / 8-K ex99.1","url":"https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447363/hubs-20260930.htm","excerpt":"the growth in Customers was primarily driven by increased demand for our lower-priced Starter products","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Q2'26 NRR 為102%，較去年同期降1個百分點；管理層預期全年 NRR 約與去年持平。Q2 淨新增客戶7,000，低於預期，原因為轉換率較弱與買方猶豫（來自第三方摘要）。","source":"HUBS 2Q26 AI Summary (platformaeronaut)","url":"https://transcripts.platformaeronaut.com/summaries/HUBS-2Q26-AI-Summary","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Gartner（轉述）：2030年前企業 SaaS 支出逾40%將脫離純席位計價；Bloomberg Intelligence 預期定價由席位轉向用量／成果計價。屬產業結構性轉變論述（二手轉述）。","source":"Bloomberg Intelligence Agentic AI Deep Dive; secondary coverage","url":"https://assets.bbhub.io/professional/sites/41/Bloomberg-Intelligence-Agentic-AI-Deep-Dive.pdf","excerpt":"will shift from seat-based subscriptions toward usage- and outcome-based structures","as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Ramp 2026-04 資料：已推出用量計價的傳統 SaaS 廠商，絕大多數支出仍為席位制，用量收入幾乎未增，席位侵蝕慢於言論。","source":"Ramp Leading Indicators, April 23 2026","url":"https://ramp.com/leading-indicators/death-of-saas-greatly-exaggerated","excerpt":null,"as_of":"2026-04-23","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因子僅泛稱反壟斷機關日益審查科技投資，可能阻擋、延遲或附條件於其投資組合交易；未述及針對 HubSpot 的調查。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm","excerpt":"We may also experience challenges from regulatory authorities in connection with our investments, including from antitrust authorities who are increasingly scrutinizing technology investments, and which may lead to unforeseen expenditures or which may block, delay or impose undesirable conditions on transactions involving our investment portfolio.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 指出 FTC 與各州檢察長適用隱私與消費者保護法；不合規可能導致執法、罰款；DPF 不合規可能遭 FTC 執法與民事罰款（隱私監管，非反壟斷）。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm","excerpt":"We may be subject to regulatory enforcement by the FTC if we are found to be noncompliant with any of the DPF principles, and this regulatory enforcement may lead to significant civil penalties.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"HubSpot 2026 年 10-Q 風險因子提及州級 AI 法規（加州、德州 2026 生效，Colorado 延至 2027-01-01）拼湊式立法。","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447363/hubs-20260930.htm","excerpt":"For example, AI laws in California and Texas took effect in 2026, and Colorado enacted a comprehensive AI law that was subsequently amended to narrow its scope and delay its effective date to January 1, 2027.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"HubSpot 10-K 風險因子列出關稅或其他貿易限制為國際營運風險之一，並指出其業務受美國 EAR 及 OFAC 出口管制與制裁法規約束；未見具體關稅金額影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm","excerpt":"Our business activities are subject to various restrictions under U.S. and other global export controls and trade and economic sanctions laws, including the U.S. Commerce Department’s Export Administration Regulations and economic and trade sanctions regulations maintained by the U.S. Treasury Department’s Office of Foreign Assets Control.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"MD&A 將關稅或其他貿易限制列為可能影響經營結果的總體經濟因素之一，未量化。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm","excerpt":"Our results of operations may be significantly influenced by general macroeconomic conditions, including, but not limited to, the impact of pandemics, geo-political conflicts, foreign currency fluctuations, interest rates, inflation, recession risks, tariffs or other trade restrictions","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"HubSpot 的平台主要功能由 AWS（北維吉尼亞、法蘭克福）與 Google Cloud（法蘭克福）第三方資料中心承載（FY2021 10-K 文字）","source":"HubSpot 10-K FY2021","url":"https://www.sec.gov/Archives/edgar/data/1404655/000095017022001221/hubs-20211231.htm","excerpt":"We currently serve the majority of our platform functions from third-party data center hosting facilities operated by Amazon Web Services located in northern Virginia and Frankfurt, Germany and Google Cloud Platform located in Frankfurt, Germany.","as_of":"2022-02-25","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2025-10-20 AWS us-east-1 大規模中斷影響 HubSpot 主要基礎設施所在區域，並在 HubSpot 內部任務處理系統引發連鎖問題；HubSpot 啟動可靠度改善計畫","source":"HubSpot Product blog: incident report for october 20 2025","url":"https://product.hubspot.com/blog/incident-report-for-october-20-2025","excerpt":"AWS experienced one of its most severe service disruptions in recent history, affecting numerous services in the us-east-1 region where HubSpot's primary infrastructure operates.","as_of":"2025-10-30","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 專業服務及其他營收 $17.3M、年減3%，因技術顧問服務減少、Payments 費用部分抵銷；總營收年增17%","source":"HubSpot 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447363/hubs-20260930.htm","excerpt":"Professional services and other revenue decreased during the three months ended September 30, 2026 compared to the same period in 2025 due to lower revenue from technical consulting services, partially offset by fees earned from Payments.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 客戶數 311,704（年增12%），單客訂閱營收 $12,038（年增4%，報告幣別）","source":"HubSpot Q3 2026 8-K ex99.1","url":"https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm","excerpt":"Grew Customers to 311,704 as of September 30, 2026, up 12%. Average Subscription Revenue Per Customer was $12,038 during the third quarter of 2026, up 4% on an as-reported basis.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Q4 2026 營收指引 $945.0–947.0M，年增12%（較 Q3 17% 減速）","source":"HubSpot Q3 2026 8-K ex99.1（搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"2026-04-14 Breeze Customer Agent 定價由每對話$1.00改為每解決對話$0.50（成果計價）；來源為次級網頁","source":"finder.techleap.nl 'HubSpot hits 18,000 agent activations, launches outcome-based AI pricing'","url":"https://finder.techleap.nl/news/feed/hubspot-hits-18-000-agent-activations-launches-outcome-based-ai-pricing","excerpt":null,"as_of":"2026-04-14","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"Gartner 3Q26 預測（次級轉述）：企業應用軟體2026年支出 $496.3B，2030年 $812.6B；跨功能代理式AI至2030年將侵蝕傳統應用軟體 $116B","source":"softwarestrategiesblog.com 引述 Gartner","url":"https://softwarestrategiesblog.com/2026/10/08/gartner-enterprise-application-software-forecast-812b-2030-crm-agentic-ai/","excerpt":null,"as_of":"2026-10-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"Gartner 2026年全球軟體支出約 $1.44兆、年增15.1%","source":"SaaStr 引述 Gartner","url":"https://www.saastr.com/gartner-software-spend-now-1-44-trillion-in-2026/","excerpt":"Gartner: Software Spend Now $1.44 Trillion in 2026, Revised Back Up to 15.1%. The Slowdown Never Came. Are You Grabbing That Budget? by Jason Lemkin | Blog Posts","as_of":"2026-04-27","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"HubSpot 10-K(FY2025)風險因子：承認競爭者可能以新AI技術使其產品失去競爭力或過時，並面對通用LLM、generative AI、通用agent及vibe coding自建軟體等非專業替代方案。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm","excerpt":"We may also face greater competition from non-specialist solutions relying on generic large language models (“LLMs”), generative AI and general-purpose agents to address a broad range of business needs.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"分析師(Seeking Alpha 2026-05)認為生成式AI與agent對HubSpot長期客戶成長影響有限，因自建CRM有安全與整合風險。","source":"Let's Data Science: Analyst Flags Limited Long-Term AI Disruption for HubSpot","url":"https://letsdatascience.com/news/analyst-flags-limited-long-term-ai-disruption-for-hubspot-a377781a","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 描述通路：直銷加 freemium 與 in-product cross-sell，另有 Solutions Partner 通路（以佣金轉介），並稱正與夥伴因應 AI 帶來的機會與挑戰、讓夥伴營收組合轉向經常性收入。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm","excerpt":"We are actively working with our partners to navigate the opportunities and challenges presented by AI advancement, ensuring they are equipped to deliver value in an evolving technological landscape.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"2026 年 HubSpot 將旗艦 Breeze AI agent 轉向結果導向計價（客戶在 agent 完成任務時付費），底層仍為席位加點數（credits）；第三方報導指出宣布 AI 計價變動後股價大跌。","source":"WebSearch 摘要（彙整 Search Engine Journal／第三方追蹤站；letsdatascience 等）","url":"https://letsdatascience.com/news/hubspot-announces-ai-pricing-changes-stock-falls-sharply-ac89c514","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"HubSpot 2026 年合作夥伴報告預估夥伴生態機會至 2030 年達 420 億美元，AI-first 夥伴營收占比由 2026 年 34.9% 升至 2030 年 43.2%；Kickoff 2026 推出產業別徽章；MarTech 解讀為夥伴計畫朝少數高度專精的公司集中。第三方 Panabee 稱夥伴通路帶動 49% 營收（未核對）。","source":"MarTech: Salesforce and HubSpot reshape partner programs for the AI era；MarketScale","url":"https://martech.org/salesforce-and-hubspot-reshape-partner-programs-for-the-ai-era/","excerpt":null,"as_of":"2026-03-09","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 2026 營收 9.117 億美元，被框為轉向可預測計價。","source":"digitalapplied HubSpot Q2 2026 AI pricing credits","url":"https://www.digitalapplied.com/blog/hubspot-q2-2026-ai-pricing-credits-agent-adoption","excerpt":null,"as_of":"2026-08-09","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026-08-05 Q3 指引：營收 $924–925M 低於共識 $941.2M；EPS $3.25–3.27 高於共識 $2.99；FY26 EPS 指引 $13.23–13.31（MarketBeat 所列共識 11.37，口徑不一）","source":"MarketBeat, HubSpot issues Q3 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/hubspot-nysehubs-issues-q3-2026-earnings-guidance-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 2026 營收 $912M 優於預期 $898M、調整後 EPS $3.26 對 $3.02；財報後股價當日大跌（報導稱約 21%）","source":"Motley Fool, Why HubSpot stock is plummeting today","url":"https://www.fool.com/investing/2026/08/06/why-hubspot-stock-is-plummeting-today/","excerpt":"Reporting Q2 2026 revenue of $912 million, HubSpot beat analysts' expectations of $898 million.","as_of":"2026-08-06","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"分析師目標價 2026-08 共識約 $274–285（Walnut/Yahoo：均值 $273.96、中位 $250、區間 $190–450、33 位；Tickflow 8/1：$285.14）；2月 MarketBeat 均值 $452.70，年內大幅下修；各源口徑與日期不一","source":"Walnut HUBS forecast / Tickflow / MarketBeat","url":"https://walnutinvest.com/stocks/hubs/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026 指引軌跡：5月上調 FY EPS 至 $13.04–13.12（前 $12.38–13.46 區間見來源）；8月Q2後指引偏弱並宣布裁員約660人；10/1 8-K 重申Q3與全年指引","source":"SEC 8-K 2026-10-01 / Webull / Placera (Morgan Stanley)","url":"https://www.sec.gov/Archives/edgar/data/0001404655/000119312526414965/d183135d8k.htm","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["triggers","thesis.R"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-04-03 以現金 1,910 萬美元（扣除取得現金後）收購 AI 媒體平台 Futurepedia，規模小","source":"HubSpot 10-Q（2026-03-31 季度）","url":"https://www.sec.gov/Archives/edgar/data/0001404655/000119312526212122/hubs-20260331.htm","excerpt":"On April 3, 2026, the Company acquired all outstanding membership interests of Futurepedia, LLC (\"Futurepedia\"), an AI-focused media platform, to expand HubSpot's media footprint. The total cash purchase price for the acquisition was $ 19.1 million, net of cash acquired.","as_of":"2026-05-07","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026-10-01 董事會核准重組計畫，裁減約 7% 員工（8-K Item 2.05）","source":"SEC EDGAR 8-K 2026-10-06 Item 2.05","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526414965/d183135d8k.htm","excerpt":"On October 1, 2026, the Board of Directors of the Company authorized the Plan that results in the elimination of certain roles, impacting approximately 7% of the Company's workforce.","as_of":"2026-10-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2026-08-05 Q2 財報下修指引後股價約跌 25%，多家律所（Block & Leviton、Johnson Fistel）宣布調查，但無已提起的集體訴訟、法院無認定","source":"Block & Leviton 案件頁／Johnson Fistel 新聞稿（2026-05-11、2026-08-18）","url":"https://www.blockleviton.com/cases/hubs","excerpt":null,"as_of":"2026-08-18","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"+","claim":"未發現 SEC 調查、重編財報、FDA 或產品召回/警告；2026-08-03 董事會授權最多 10 億美元回購（24 個月）","source":"SEC EDGAR 8-K 2026-08-05 Item 8.01 及搜尋結果","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526335148/hubs-20260803.htm","excerpt":"On August 3, 2026, the Company's Board authorized a share repurchase program for the repurchase of shares of the Company's common stock in an aggregate amount of up to $1.0 billion (the \"August 2026 Share Repurchase Program\") over a period of up to 24 months.","as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-04-03 以 1,910 萬美元現金收購 Futurepedia，規模小；無 HubSpot 被併購之確認消息","source":"HubSpot 10-Q（2026-03-31 季度）","url":"https://www.sec.gov/Archives/edgar/data/0001404655/000119312526212122/hubs-20260331.htm","excerpt":"On April 3, 2026, the Company acquired all outstanding membership interests of Futurepedia, LLC (\"Futurepedia\"), an AI-focused media platform, to expand HubSpot's media footprint. The total cash purchase price for the acquisition was $ 19.1 million, net of cash acquired.","as_of":"2026-05-07","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"律所宣布調查（Johnson Fistel 2026-05-11；Block & Leviton 2026-08-18），尚無已提起之證券集體訴訟；10-K 載明曾面臨 CIPA 追蹤器類集體訴訟/求償信","source":"Block & Leviton 案件頁；HubSpot 10-K FY2025 Item 1A","url":"https://www.blockleviton.com/cases/hubs","excerpt":null,"as_of":"2026-08-18","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"10-K 風險因素：公司曾遭受 CIPA 追蹤器類訴訟","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm","excerpt":"We have been subject to these actions and may become subject to additional such actions in the future.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"HUBS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":83.02,"operating_margin_pct":5.45,"fcf_margin_pct":18.89,"rd_intensity_pct":25.2},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HUBS","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"CRM","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":77.28,"operating_margin_pct":21.52,"fcf_margin_pct":34.49,"rd_intensity_pct":14.49},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"NOW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":73.08,"operating_margin_pct":9.68,"fcf_margin_pct":30.78,"rd_intensity_pct":22.47},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOW","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"TEAM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":84.83,"operating_margin_pct":0.16,"fcf_margin_pct":20.07,"rd_intensity_pct":49.74},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TEAM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MNDY","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":88.74,"operating_margin_pct":2.9,"fcf_margin_pct":21.56,"rd_intensity_pct":26.03},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MNDY","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"HUBS"},"financial_history":{"ticker":"HUBS","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":1730969000.0,"revenue_yoy_pct":null,"gross_margin_pct":82.21,"operating_margin_pct":-5.94,"net_income":-107347000.0,"diluted_eps":-2.35,"free_cash_flow":181403000.0,"fcf_margin_pct":10.48,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":2170230000.0,"revenue_yoy_pct":25.38,"gross_margin_pct":84.41,"operating_margin_pct":-4.8,"net_income":-164510000.0,"diluted_eps":-3.3,"free_cash_flow":250717000.0,"fcf_margin_pct":11.55,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2627543000.0,"revenue_yoy_pct":21.07,"gross_margin_pct":85.03,"operating_margin_pct":-2.42,"net_income":4628000.0,"diluted_eps":0.09,"free_cash_flow":469793000.0,"fcf_margin_pct":17.88,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":3131266000.0,"revenue_yoy_pct":19.17,"gross_margin_pct":83.76,"operating_margin_pct":0.36,"net_income":45911000.0,"diluted_eps":0.86,"free_cash_flow":576654000.0,"fcf_margin_pct":18.42,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HUBS/HUBS_Q3_2026_Earnings_Call_20261104.md）

# Q3 2026 Earnings Call
**HubSpot, Inc.** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Good day, everyone. My name is Ryan, and I will be your conference operator today. At this time, I would like to welcome you to HubSpot's Third Quarter 2026 Earnings Call. [Operator Instructions]
At this time, I would like to turn the call over to Vice President, Investor Relations, Geoff Koegler. Please go ahead.

**Geoff Koegler** (Executives):
Thanks, operator. Good afternoon, and welcome to HubSpot's Third Quarter 2026 Earnings Conference Call. Today, we'll be discussing the results announced in the press release we issued this afternoon.
With me on the call this afternoon is Yamini Rangan, our Chief Executive Officer; Dharmesh Shah, our Co-Founder and CTO; and Kate Bueker, our Chief Financial Officer.
Before we start, I'd like to draw your attention to the safe harbor statement included in today's press release. During this call, we'll make forward-looking statements within the meaning of the federal securities laws that are subject to risks and uncertainties including statements regarding our financial guidance for the fourth fiscal quarter and full year 2026, future financial performance, business outlook and strategy.
These statements reflect our views only as of today, and except as required by law, we undertake no obligation to update or revise them. Please refer to the cautionary language in today's press release our Form 10-Q and our other SEC filings for a discussion of the risks and uncertainties that could cause actual results to differ materially from expectations.
During the course of today's call, we'll refer to certain non-GAAP financial measures as defined by Regulation G. Reconciliations to the most directly comparable GAAP measures can be found in today's press release.
Now it's my pleasure to turn the call over to HubSpot's Chief Executive Officer, Yamini Rangan. Yamini.

**Yamini Rangan** (Executives):
Thank you, Geoff, and welcome, everyone. I'll start with our Q3 results, what drove our performance and how we are responding to the headwinds we are seeing in the market. Then I'll share our progress transforming HubSpot for the AI era.
Q3 revenue grew 17% year-over-year in constant currency. We delivered 3 points of non-GAAP operating margin expansion, bringing our operating margin to 23%. Our total customer count reached over 311,000 globally with 5,300 net additions in the quarter. We're still in the early stages of a massive shift with AI and Q3 reflected that reality. The headwinds we saw in Q2 continued and became more pronounced in Q3.
Let me unpack the 2 underlying trends, how we're responding and the early results we're seeing. First, customers are evaluating AI differently. They want to see AI work with their data in their environment. They want proof before they buy. We saw the shift early and leaned into it in Q2. We introduced free trials and pricing tied to value and outcomes. We knew this would extend buying cycles and create near-term headwinds, but we believe it's the right long-term trade-off.
We're seeing encouraging early results. Agent trials grew 64% quarter-over-quarter in Q3. But we're also learning that customers need hands-on support to turn AI trials into real outcomes. Our focus is on improving the trial experience and leveraging our partners and solution consultants to help more customers move from trials to paid adoption.
Second, we are seeing a shift in demand with increased budget sensitivity. AI is changing how customers discover HubSpot and how they make purchasing decisions. Inbound demand remains under pressure, and we are diversifying to new sources of demand through intent-based marketing, LLM connectors and AEO. At the same time, tighter budgets are making buying decisions more complex. Upmarket, we're seeing larger buying committees, more CEO, CTO and Board involvement and therefore, longer sales cycles. Down market, customers are more price-sensitive and focused on optimizing costs. We are adapting our playbooks to these new buying patterns.
We're engaging the C-Suite earlier, involving more stakeholders and bringing technical expertise into complex deals. We're seeing early evidence that this playbook works. Win rates are nearly 3x higher in deals with 5 or more buying committee members when we engage multiple stakeholders. We're also seeing higher close rates on larger deals with C-suite involvement.
Together, these early signs give us confidence that we have the right initiatives in place to address these headwinds, even though it will take some time for them to show up in our results. Despite the near-term headwinds, we continue to see clear momentum in AI and progress across our core and emerging growth drivers. Multi-hub adoption remains strong as customers consolidated their go-to-market tools on HubSpot. 62% of new Pro+ customers landed with multiple hubs, up 2 points year-over-year. Upmarket continues to be a growth driver with deals over 120,000 growing 19% year-over-year as larger customers turn to HubSpot to consolidate their data and build the context needed to drive AI outcomes.
More importantly, AI adoption is accelerating and credit is emerging growth driver. Monthly credit consumption is up nearly 2.5x since the beginning of the year, with usage diversifying across our agentic use cases. Active core seats grew 34% year-over-year. These trends reinforce our conviction in accelerating our AI transformation. At Analyst Day, we laid out how we are transforming HubSpot to lead in the outcomes era. AI is fundamentally changing software from tools that help people do work to agents that do the work and deliver outcomes.
We are moving with urgency to transform our product, pricing, go to market and how we operate to capture this opportunity. And in Q3, we made meaningful progress in all of these areas. We have transformed HubSpot into an agentic customer platform with 4 connected parts. HubSpot agents and custom agents deliver outcomes across marketing, sales and service. Breeze Assistant is now the gateway to the power of HubSpot, shifting the experience from how do I do it to do it for me. We believe this is the future of how people work, and we are investing heavily to make that experience exceptional.
Our headless strategy brings HubSpot into leading LLMs through connectors and enables agents to run HubSpot through APIs. And growth context makes it all work, giving AI the understanding of a business, its customers and its teams to take the right actions. Together, these 4 parts make HubSpot the platform where AI understands the business, does the work and delivers outcomes. We're making meaningful progress bringing this vision to life.
At UNBOUND, we doubled our portfolio of HubSpot agents. We launched Campaign Agent, Content Agent and Nurture Agent to help marketeers build campaigns, create content and personalized engagement at scale. We also enhanced Customer agent, Prospecting agent and Data agent to help businesses, resolve support issues, generate pipeline and enrich customer data. We're seeing strong growth in both reach and depth of adoption. 20% of Pro+ customers now use HubSpot agents, up 11 points since the start of the year.
Depth measured by the total number of monthly agentic actions across our Pro+ customer base has increased 5x since the start of the year. More importantly, agents are delivering measurable outcomes. Customer Agent resolved over 2 million support issues in Q3. Data Agent enriched 68% more contacts quarter-over-quarter and customers using prospecting agents are seeing 76% more qualified leads and 80% more meetings than those who don't.
We're also making it easy for customers and partners to build their own agents and workflows on HubSpot. In July, we launched Agent Builder and Agent Hub, allowing them to build, deploy and manage custom agents powered by HubSpot's growth context. Since launch, Pro+ customers have deployed over 5,600 custom agents and partners have deployed nearly 700 in Q3, more than doubling quarter-over-quarter and we're providing incentives to accelerate this motion. This is an important shift. Customers are building their own agents to solve problems specific to their businesses with partners helping scale that innovation.
Next is Breeze Assistant, which we believe will fundamentally change how customers work with HubSpot. At UNBOUND, we launched an all-new Breeze assistant that goes beyond answering questions to taking action. Customers simply describe what they want to accomplish and Breeze builds workflows, creates reports and gets work done for them. We're seeing rapid growth in adoption and customer satisfaction. 61% of Pro+ customers now use Breeze Assistant, up 24 points since the start of the year. And customer satisfaction has improved 15 points to 69% since the start of the year as well.
Take Kaplan Early Learning, a company with hundreds of employees. Their HubSpot admin previously relied on developers to build and update workflows, which could take weeks. With Breeze Assistant, he rebuilt key workflows himself in under 4 hours and now uses Breeze every day. We believe this is the future of work, a conversational experience powered by AI that understands your business and takes action. We're combining that experience with HubSpot's go-to-market domain expertise and growth context to make Breeze the gateway to our platform.
And to round it out, our headless strategy extends HubSpot, wherever customers choose to work with AI. We're building the best CRM connectors for leading LLMs like ChatGPT and Claude, and we are opening up our APIs and MCP capabilities so agents can run HubSpot. We were the first CRM to connect with all 4 leading frontier models. And today, we are the most popular CRM connector on both ChatGPT and Claude.
What is important is what happens when customers connect HubSpot to their preferred LLMs. They're not just pulling data out of HubSpot. They're doing more work in HubSpot. They're analyzing reports, managing pipelines, creating CRM records and taking action all through conversations. In Q3, customers created over 22 million CRM objects through connectors within HubSpot, up 157% quarter-over-quarter. And the more they work with HubSpot, the more value they get from it.
Customers using connectors have 13 points higher gross revenue retention and upgrade paid seats at 3x the rate of non-connector users. This reinforces our conviction that headless is additive to HubSpot. As customers use AI to analyze data, manage deals and take action, they're doing more in HubSpot. That deeper engagement creates more opportunities for seat expansion, stronger retention and long-term growth.
Now as we transform our product, we are also transforming our pricing to drive long-term growth. Our vision is simple, a hybrid model of seats and credits. We began simplifying pricing in 2024 by lowering seat prices, removing seat minimums and introducing core seats. While this initially lowered ASP, it has led to healthier customer cohorts with higher retention.
Now we're taking the next step to give customers greater flexibility and predictability in how they spend on AI. Our pricing pilot simplifies HubSpot in 3 ways. It provides access to all HubSpot capabilities through a go-to-market seat, removing hubs. It reduces the price jump from starter to Pro across marketing, content and data hubs and brings all usage-based features under a single credit mechanism.
Early results from our Nordics and Benelux pilots are encouraging. Compared to regions outside the pilot, credit usage is 2 to 3x higher. Pro+ customer volume is higher, while average selling price is lower. We're seeing early evidence that this is working. More customers, greater credit consumption and stronger new ARR. We've expanded the pilot across EMEA in Q4 for new customers, and we will use those results to determine the timing of the continued rollout. 
Our goal is to make HubSpot easier to buy and AI easier to adopt. We believe this is the time to remove friction, accelerate AI adoption and gain market share early in the AI platform shift.
Now let me just close out with a bigger picture. AI is reshaping our industry, and we're moving decisively to position HubSpot for the next era of growth. We recognize the near-term headwinds and we are taking actions to address them. Our core growth drivers remain intact, AI adoption and usage are accelerating and we are seeing evidence that our product and pricing transformations are beginning to work.
We're making deliberate trade-offs to build a stronger, faster growing and more profitable HubSpot for the longer term. We have a clear strategy. We're executing with urgency and we are confident in the opportunity ahead.
With that, I'll turn it over to Kate to walk through our financial and operating results. Kate?

**Kathryn Bueker** (Executives):
Thanks, Yamini. Let's turn to our third quarter and full year 2026 financial results. Q3 revenue grew 17% year-over-year in both constant currency and as reported. Q3 subscription revenue grew 18% year-over-year, while services and other revenue decreased by 3%, both on an as-reported basis. Domestic revenue grew 16% year-over-year in Q3. International revenue growth was 18% in both as reported and in constant currency, representing 49% of total revenue.
We added 5,300 net new customers in Q3, bringing our total customer count to over 311,000 growing 12% year-over-year. Our Q3 net additions reflect continued demand pressure and increased buyer hesitancy particularly down market. Average subscription revenue per customer was $12,000 in Q3, up 4 points year-over-year in both as reported and in constant currency.
Customer dollar retention remained stable and healthy in the high 80s. Net revenue retention was 101%, down about 1 point quarter-over-quarter driven by a step-up in budget sensitivity, which was also more pronounced down market. Q3 calculated billings were $925 million, growing 15% year-over-year in both constant currency and as reported.
Non-GAAP operating margin was 23% up 3 points compared to the year ago period. This expansion reflects our disciplined hiring approach, partially offset by AI costs. GAAP operating margin was 8% in Q3, up 6 points compared to the year ago period. This expansion reflects our non-GAAP operating income expansion and a more than 3-point reduction in stock-based compensation as a percentage of revenue. 
Non-GAAP net income was $189 million, and non-GAAP net income per diluted share was $3.81, up 35% and 43% year-over-year, respectively. GAAP net income was $83 million in Q3, and GAAP net income per diluted share was $1.67.
In the third quarter, the company generated $188 million of free cash flow or 20% of revenue. Our cash and marketable securities totaled $1.3 billion at the end of September. During the quarter, we bought back more than $237 million of stock under our share repurchase program, bringing our 2026 year-to-date repurchases to nearly $1 billion reflecting the continued confidence we have in our future growth opportunity.
Before we dive into guidance, let me share some perspective regarding the headwinds we experienced in Q3, the reorganization we announced in October and our expectations on the near-term performance of our KPIs. As Yamini shared, we are seeing shifts in demand and customer buying behavior, as customers navigate the AI transition. Upmarket, we're seeing more decision-makers and longer sales cycles. Down market, we're seeing greater price uncertainty and budget optimization.
Both headwinds emerged in Q2 and became more pronounced in Q3. Our Q4 and full year guidance reflects our expectation that these increased headwinds will persist throughout the remainder of the year and into 2027. Given the transition we are driving across product, pricing and go-to-market, we are prioritizing setting the business up for long-term growth rather than solving for short-term net adds. As a result, we are not providing a net adds estimate for Q4, but expect to be below the 5,000 level we achieved in Q3.
We expect low to mid-single-digit ASRPC growth in constant currency in Q4. We now expect full year 2026 net revenue retention to be down about 2 points year-over-year. We expect customer dollar retention will remain strong and stable in the high 80s, but continue to expect net upgrade rates to be pressured as a result of customer budget optimization. We now expect net new ARR to decline year-over-year in fiscal 2026.
On October 6, we announced a reorganization of our people around customer outcomes, which flattened the organization and created Agile teams with clear ownership. This leaner structure will allow us to operate faster and with more focus on our biggest opportunities and reinforce our commitment to profitability. We will invest a portion of the savings in employee retention, AI talent and platform. We remain confident in delivering our 2027 non-GAAP operating margin target of 23% to 24% and our long-term profitability targets we shared at our Analyst Day at UNBOUND.
With that, let's dive into our guidance for the fourth quarter and full year of 2026. For the fourth quarter, total as reported revenue is expected to be in the range of $945 million to $947 million, up 12% year-over-year on an as reported and constant currency basis.
Non-GAAP operating income is expected to be between $216 million and $217 million, representing a 23% margin. Non-GAAP diluted net income per share is expected to be between $3.85 and $3.87, representing growth of 25%. This assumes 48.9 million fully diluted shares outstanding.
And for the full year of 2026, total as reported revenue is now expected to be in the range of $3.685 billion to $3.687 billion, up 18% year-over-year on an as-reported basis and 16% in constant currency. We expect non-GAAP operating income to be in the range of $772 million to $773 million, representing a 21% margin.
Non-GAAP diluted net income per share is now expected to be between $13.59 and $13.61, representing growth of 40%. This assumes 50.4 million fully diluted shares outstanding.
As you adjust your models, please keep in mind the following: Q4 GAAP operating income will include an expected $60 million to $70 million charge for severance costs in connection with our October reorganization. We continue to expect CapEx as a percentage of revenue to be 5% to 6% for the full year of 2026 and now expect free cash flow to be about $720 million.
With that, I will turn the call back over to the operator for questions.

**Operator** (Operator):
[Operator Instructions] Your first question will come from the line of Samad Samana with Jefferies.

**Samad Samana** (Analysts):
I'm going to squeeze in a 2-parter here. I guess, first, maybe could you comment on like when you started to see trends get worse in 3Q? And I guess, maybe more specifically into 4Q, has that continued to deteriorate? Has it stabilized? And I guess, any early green shoots that we can hang our hat on?
And then maybe, Kate, for you, I would ask given the exit rate of 12% for 4Q, is that a good starting point for 2027? And I know the company doesn't normally give an early outlook into the forward year, but just given the slowdown. I was wondering if we can get some contours.

**Yamini Rangan** (Executives):
Samad, thank you so much. This is Yamini. Look, I'll talk about the trends that we saw in Q2, Q3 and what we are assuming for Q4. The simplest way to describe what we are seeing is that customers are navigating a major AI platform shift and that is changing how they evaluate software, how they discover HubSpot and how they make purchasing decisions. So that's what we've been seeing. So let me unpack each of those trends.
First, customers want to see AI work in their own environment with their own data. They want to see the proof of AI before they buy. And as we talked about it in the last earnings call, we recognized the shift early. We introduced trials, and we tied our pricing closer to the value and the outcomes that customers see. Now trials are growing. That's the green shield, 64% quarter-over-quarter growth, but they're converting requires handholding. You can't just like turn an agent on. Therefore, we are improving the trial experience. We're bringing partners and solution consultants to help the customers get the value faster.
So we believe this is the right long-term approach even though it extends the buying cycles in the near term.
Okay. The second big trend that we're seeing is the demand environment is changing with greater budget pressure. And it's a couple of different things here. So let me break it down. Inbound demand, which we've talked about for a number of quarters, it remains under pressure as AI changes how buyers discover software. And we've been diversifying through the top of the funnel through intent-based marketing. We're now doing LLM connectors as a source for sign-ups as well as leads as well as AEO, but these new channels are nascent and they don't really need the changes in the inbound demand.
Now at the same time, buying decisions are very complex. We've talked about this for a couple of quarters, upmarket. There are larger committees with more CEO, CTO, board involvement, and that's because it's no longer just a technology decision. This is a strategic choice. So we are responding by engaging senior decision-makers earlier were involving multiple stakeholders, and we are bringing partners and technical expertise earlier within the deal cycle.
Now again, the green shoot that we're seeing is that in deals with 5 or more buying committee members, win rate is nearly 3x higher when we engage multiple stakeholders. And we're also seeing higher win rate with C-suite involvement.
And finally, down market, customers are just more price sensitive because AI is a new line item and they are looking at controlling the spend across all the experiments and the tools that they're running. And we are leaning into it by simplifying our own pricing. We're lowering barriers to entry and making it easier to adopt AI.
Now, all of these trends we started seeing in Q2, which is when we shared all of those, it became more pronounced in Q3, and it is reflected within our Q4 outlook. So we're moving very quickly. Early indicators of our plays are encouraging, but this is going to take time for the changes to translate into stronger growth.

**Operator** (Operator):
Your next question...

**Kathryn Bueker** (Executives):
Yes. Thanks, Samad...

**Operator** (Operator):
Sorry, go ahead.

**Kathryn Bueker** (Executives):
Sorry, I will -- I'll follow on, Samad your specific question on the guidance and some of the factors that you should be considering as you think about next year. Unsurprisingly, I'm sure we are not -- like we are not providing formal 2027 guidance at this time.
As you know, we are early in Q4. Q4 is our most important quarter and we are focused on executing a very strong Q4. We are also still early in our 2027 planning process. That said, I will share a few of the dynamics that might be helpful as you start to think about your 2027 outlook.
The first is that, in Q3, our revenue grew at 70% in constant currency. It's down about 0.5 point from our constant currency revenue growth in Q2. And the decrease was a result of the pressure that we've seen this year, which became more pronounced in Q2. We also expect that these more pronounced headwinds will continue in Q4 and into 2027. 
Our Q4 guidance obviously implies a more significant step down in constant currency revenue growth, and the deceleration from Q3 reflects the impact of the more pronounced headwinds on our Q4 results. In addition, we shared that we now expect that net new ARR to decline year-over-year in 2026. And those are the factors that I would consider as you think ahead into next year.
Finally, I'll remind you that we took the same approach to guidance this quarter as we have always done. Our approach has not changed. We will obviously share 2027 guidance when we report our Q4 results in February. Until then, we're going to remain focused on executing a very strong Q4.

**Operator** (Operator):
Your next question will come from the line of Brian Peterson with Raymond James.

**Brian Peterson** (Analysts):
Yamini, I wanted to see if I can get more detail on some of your trial pricing and packaging. I know you said that maybe the upfront ASPs are down, but you're seeing some encouraging dynamics for customers that have ramped. Is there any color that you can share there? And maybe -- because I think that would give investors confidence that maybe that's good for HubSpot over the long-term.

**Yamini Rangan** (Executives):
Brian, thank you so much for the question. Yes. So let me break it down in terms of the pricing evolution, but also what we are seeing in terms of the pilot that we have in Nordics and Benelux.
Many of you who have followed us for a while know that in 2024, we took a set of steps to simplify pricing. And what we specifically did is that we lowered seat pricing. We've removed seat minimums for Sales hub and Service hub, and we introduced core seats. And that made it easier to buy and expand across our seat-based hubs. Initially, we saw the ASPs decline, but then we attracted more customers, and we saw stronger retention of those cohorts. And that was Phase 1.
Now we're doing Phase 2. We want to further simplify pricing with AI, and our vision is a hybrid model of seats and credits. Seat because it provides access to platform AI and data for anybody within a go-to-market team and credit because it scales with the AI value and the customer outcomes that we deliver. So that's the pricing evolution.
Now specifically for the pilot that we mentioned in Nordics and Benelux, we're doing 3 things. We're removing separate hub-based subscription. So customers can access HubSpot capabilities through a go-to-market seat, no hubs. And that is a simplicity that customers like. Second, we're actually reducing the price jump from starter to Pro for marketing, content and data hub. And this is going to lower ASPs initially, but it is going to do something really important. It's going to remove the friction in pricing, and it's going to lead to more Pro+ customer volume. And this is exactly what we are seeing within the Nordics and Benelux pilot. We're seeing ASPs go down, but we're seeing the number of Pro+ customers go up, which is encouraging.
And third, we're bringing all of the usage-based features into credit. And that means e-mail sent, tickets resolved, data-enriched, APIs, all in credits. And that means it's a simpler mechanism. It reduces the friction of adopting credits, and that simplification is something that customers like as well. In fact, we've seen 2x to 3x more credit consumption in the pilot cohorts that we just talked about.
Look, it's early days, but our focus is very clear. We want to remove pricing friction. We want to remove packaging friction, and we want to remove AI adoption friction as we go through this process. And as we do that, we have the confidence that over the long period of time, we're setting up for durable growth.

**Operator** (Operator):
Your next question will come from the line of Jackson Ader with KeyBanc Capital Markets.

**Jackson Ader** (Analysts):
To follow-up on the pricing, it's kind of -- its pricing and its AI adoption, Yamini. When you talk about trying to solve some of the AI adoption with lowering the friction and changing the pricing and packaging with this pilot program. But then on the other side, you're also talking about meeting more solution consultants and partners to be hands on in order to drive, again, more AI consumption and usage in your core customer base.
So I'm just curious, like, is it more about friction in the products in the pricing? Or is it more about people just not getting the value that you'd expect them to, the first time around when they see Breeze or when they see some of these agents that you're rolling out.

**Yamini Rangan** (Executives):
Jackson, thank you. I really appreciate the question. And the question is you're making changes in pricing packaging and then you're also putting more consultants and partners and what is the thing that you're actually trying to accomplish. And it really comes to the segmentation that we have.
So look, overall, if you really step back, people are trying to navigate a huge platform shift. And they need to have confidence that it is going to work in their environment. Second, they want to have the predictability in costs. But let me now unpack the dynamics in upmarket versus down market.
In upmarket, customers really want to drive the outcomes. They want to drive more pipeline with prospecting agent. They want to drive more tickets resolved through the customer support agents. And there, when we introduce the trials, it's not just enough, we want to be able to hold their hands, which is where our partner ecosystem comes in. We also are putting our solution consultants, and we've always deployed presales and post sales consultants in the upmarket segment. And what we are finding is that when we turn the trials on checking back in a week, making sure the outcomes are clear and being able to follow-up with some handholding is really important to drive that AI adoption and when we do that, we begin to see a lot more uptick.
There are tons of examples of those customers, but Eventus is an example that we talked about. They started with the data agent and prospecting agent. They did a trial. During the trial, their pipeline improved, but they actually put some help in order for them to get those value. And then as they've done that, they've continued to expand.
Now the dynamic is quite different down market, because down market, we're not going to put solution consultants, and that's not where our partners focus on. And so the biggest lever that we have in removing the friction is make the product [ live ] experience for trials really easy and simple. We've invested pretty heavily on agentic onboarding, which means you give your e-mail, you get your calendar and you start getting the outcomes as quickly as possible, and that's what we launched at UNBOUND for the down market segment.
The bigger problem there is that friction point in pricing that I talked about, Jackson, which is the jump between Starter and Pro for Marketing Hub and Content hub aside, which is what we're solving. And that solves it specifically for the down market segment when someone is looking to go from a starter addition to a pro edition and that's the set of changes that we're doing.
Look, if I step back, pricing transformation plus product transformation plus go-to-market, all of it is aimed to get our customers and the segment that we serve small and medium businesses really navigate a pretty big shift while being very clear in delivering the outcomes in the way that they want.

**Operator** (Operator):
Your next question will come from the line of Elizabeth Porter with Morgan Stanley.

**Elizabeth Elliott** (Analysts):
Great. Kate on profitability, just Q4 was a little bit light. I was wondering if you could help us understand what's driving the incremental spending or pressure on profitability. And following the October restructuring, where specifically are you choosing to reinvest those savings? And how should we think about the linearity of investments relative to the 23%, 24% margin target that you have for 2027.

**Kathryn Bueker** (Executives):
Yes. Thanks, Elizabeth. Let me just maybe start by taking you back to the conversation that we had at Analyst Day, which was very much around -- the transformation that we have been going through as an organization for a number of years now, right? We have been focused on becoming a more efficient and effective organization enabled by AI. And we have done that in such a way where you've seen us really invest in some places and pull back in other places.
And specific to your question on Q3. Our Q3 margins really benefited from that disciplined hiring approach that we have been deploying now for a number of years. If you look at our head count ending in Q3, it's actually down quarter-over-quarter. And that created some positive margin momentum going into Q3.
Now in terms of Q4, the head count reductions that we made as part of our October reorganization will benefit our Q4 operating profit, but we are reinvesting a significant portion of that in employee retention, along with selective hiring in AI and some AI product investments. So there's a bit of a seasonal shift in what we're seeing in profitability in 2026, but we continue to expect that we will deliver nearly 2.5 points of margin expansion this year.
You also asked about our 2027 and longer-term guardrails for operating profit margin, and we remain confident that we will deliver that 23% to 24% non-GAAP operating margin that we talked about at Analyst Day as well as our long-term profitability targets that we shared at UNBOUND.

**Operator** (Operator):
Your next question will come from the line of Billy Fitzsimmons with Piper Sandler.

**William Fitzsimmons** (Analysts):
So with net revenue retention at 101% and it was flanked that it was under a little bit of pressure from budget optimizations, how much of that NRR pressure reflects fewer upgrades versus customer churn? And are trends meaningfully different between smaller and larger customers or vertical to vertical.

**Kathryn Bueker** (Executives):
Yes. I appreciate the question. You're right, net revenue retention was down about 1 point quarter-over-quarter. The component trends are very much the same as the ones that we have been talking about for some time. They are just more pronounced in Q3 than what we've seen in the last couple of quarters. And just to reiterate, customer dollar retention, which is our gross churn remains very strong and stable in the high 80s.
And it's -- the net upgrade that remains under pressure. Specifically, though, we are seeing the core persona -- core seat and persona seat upgrades continue to be a tailwind to net revenue retention but they are now being more than offset by headwinds elsewhere, which includes cross-sell, contact tier upgrades, addition upgrades and other cost optimizations that we're seeing our customers do as they come up for renewal. We do expect that these trends will continue, which is why we have updated our view, our expectation for our net revenue retention for 2026 to be down approximately 2 points.
That said, and we talked about it explicitly in some of the pricing discussions that Yamini just had, the seats and credit model really does set us up for stronger net revenue retention over time by lowering the barrier to entry to get started and making it easier to grow AI use cases on HubSpot.

**Operator** (Operator):
Next up will be Tyler Radke with Citi.

**Tyler Radke** (Analysts):
My question is just on the timing of some of these changes you're making. As you think about the rollout that you saw in the Nordics and Benelux with the trade-off of lower ASPs. How long will -- are you expecting that to take to roll out and sort of the impact on the rest of the business? And how should we just think about that from a timing and revenue impact, thinking about 2027?

**Yamini Rangan** (Executives):
Tyler, let me take this, and I'll say that in terms specifically of the timing of the rollout Nordics pilot. We started in April. Benelux, we started in June, and those have been ongoing for new customers on this flexible seats and credit model. In Q4, we expanded it for all of EMEA for new customers only. So that is what is going on that's now 4 weeks into that process. And we will use the results to validate customer adoption, credit usage, retention and the impact on new ARR before we finalize the timing of the broader rollout.
As you can imagine, this is still early within Q4, and we want to see the pilot run through all of EMEA for our new customers before we decide the full timing. And as Kate mentioned, we'll come back and talk to you about 2027 when we finish out the year and start with the new year.

**Operator** (Operator):
Next question will come from Samik Chatterjee with JPMorgan.

**Samik Chatterjee** (Analysts):
Maybe on the visibility into the net ads, you're sort of talking about less than 5,000 customer add into Q4. I understand some of the industry-wide headwinds you're facing at this point. But when you think about sort of the lower visibility there, can you just flesh that out in terms of how the pipeline looks for new customers? What you're seeing in terms of engagement?
And is there a function in terms of maybe more of your resources being diverted towards upsell with the existing customers or the pilot programs where maybe you're sort of seeing with the pipeline on the new customer side at the same time? Any sort of more insights on what's going on with the lower sort of numbers there into Q4?

**Kathryn Bueker** (Executives):
Yes. I appreciate the question. Maybe I will try to first talk about what happened in the quarter, talk about the underlying drivers of net additions and then talk about the expectations and guidance that we put forward for Q4.
So I'll just start with Q3. We added 5,300 customers in the quarter, which was in line with the 5,000 to 6,000 range that we shared on our last call, but down from the 7,000 net adds we delivered in Q2. And this reflects the demand pressure and the pricing sensitivity that we're seeing down market.
I'll spend just a couple of minutes talking about the dynamics that drive net additions because I think it will help with the understanding of what really is going on under the hood. As we've talked about in the past, our net addition KPI is really disproportionately impacted by down market customers, down market customers specifically using our Starter and Pro tiers.
And the customer acquisition motion for this segment is an inbound product-led motion. And as demand shifts like Yamini has been talking about and customers become more price sensitive, it shows up in net adds in a really outsized way. We're making changes across product pricing and go-to-market to address the challenges that we are seeing down market. We relaunched our starter product with a self-updating CRM and agentic onboarding. We're continuing to diversify our sources of demand, including into social, LLM connectors into partnerships and also AEO.
And we're piloting our seats and credits pricing model to address some of that key pricing friction, especially in the down market segment. And we think these are the right steps to transform our down market business, but they're going to take time to impact the results.
In the meantime, we expect the level of uncertainty in the metric to be elevated, right? And so we're not providing a specific expectation for Q4. That said, we will provide Q4 actual results as part of our February earnings call. And we're going to make the right choices to drive long-term growth rather than solving for the short-term metric of net adds.

**Operator** (Operator):
Your next question will come from the line of Kirk Materne with Evercore.

**S. Kirk Materne** (Analysts):
Yamini, Just maybe a higher-level question for you, which is you guys have done a lot on product and packaging. Is there just more to be done in an AI world from a go-to-market perspective with you all? And I guess, how are you thinking about that going into '27 in terms of the need to handhold perhaps at the higher end of your customer base?

**Yamini Rangan** (Executives):
Kirk, thanks a lot. I think it's all of you about. Like this is a pretty massive shift and the way we've thought about it on the product side is product is all about delivering outcomes. And the way we have thought about it from the go-to-market side is putting the resources in the right roles with the right incentives to drive those outcomes. That is broadly how we have thought about it.
Now it shows up differently upmarket and downmarket. In upmarket, as one of the things we brought sales and CS together under one organization. And the reason is we want that handoff between starting your first trial to closing the first AI use case to expanding on top of it to be very, very seamless, and that is what that organization is focused on, and that's where we're putting the resources. The second is, I talked a little bit about the trial motion, that's a go-to-market change, right?
We are landing with trials, which means our reps need to be very focused on making sure that during the trial period, there is clear and fast outcome. During the same trial period, we got to bring the partners as well as some of the presales consultants in to deliver the value. And so there's just much more closer coordination that's happening from the go-to-market perspective.
And then expansion becomes very, very obvious in AI because once you land and once you start getting the value, the expansion becomes almost natural. So the kinds of things that we're doing in go-to-market is really tied to how do we land with smaller AI use cases how do we show value during the trial period, how do we show compounding returns as AI and agentic use cases begin to drive impact?
And how do we make pricing super simple and predictable for the segment that we are really focused on. So those are the sets of changes that we're doing in go-to-market.

**Operator** (Operator):
Your next question will come from Siti Panigrahi with Mizuho.

**Sitikantha Panigrahi** (Analysts):
Yamini, I think at a high level, what investors trying to figure out this transition seems like not a year or two, probably it will be a multiyear transition. How do you see this -- should we expect this growth to stay below this level as you transition? Or how should you think about as you try to roll it out new versus existing, how are you trying to balance growth and profitability.

**Yamini Rangan** (Executives):
Well, I think there are 2 parts of your question. The first part is it seems multiple quarters. How should we think about the growth trajectory of the company and what gives confidence. And then the second part is, as you do that, how do you like balance, growth as well as profitability.
So look, I think we've been very clear that this year, we are seeing headwinds and the headwinds are how are customers evaluating AI as well as how -- who is making the purchasing decision. And that has impacted both Q2 as well as Q3, and we are facing the same kind of headwinds in Q4. So the short answer is we expect the headwinds to continue into Q4.
Now the path for us back to stronger growth is transforming our product pricing go-to-market, which is what we are accelerating. We've done a number of deliberate choices to create near-term pressure that creates near-term pressure, but it's the right thing for the company and the right thing for our customers as they go through this. Trials as an example, the pilot of seats and credits that we just talked about as an example and a number of other things that where we are investing to help our customers grow.
Now we are seeing early evidence that the product transformation is working. And we've provided a framework for how you all should be evaluating our product transformation, which is first one is reach. What percentage of our customers are actually using our AI products and agents. 64% of Pro+ customers are using AI futures and 20% are using agents, and that's up quarter-over-quarter.
Second part of the framework is depth, how many actions are they taking? And are they doing it frequently. And Pro+ customers are taking 5x more actions than the beginning of the year. And that means credit consumption is up nearly 2.5x. So those are the early indicators that the product transformation is beginning to work. We would love to see that accelerate, but we're not satisfied with that. And we're also making sure all of the pricing friction is removed.
So look, the green shoots are there. We have a very clear strategy, but this is not going to be a single quarter or a 2-quarter transformation. We are going to take all of the right actions to set HubSpot up to be able to capture the broader opportunity that is ahead.
And then sorry, I want to make sure that I captured the second part of your question, which is you asked how it going to balance growth and profitability. The transformation is not just on the product and pricing side. We are transforming HubSpot internally, and that is what has given us the ability to increase our profitability. Kate just walked through the commitment for this year. She walked through the commitment for our operating margin for 2027 as well as the long-term target that we have. So we are very focused on balancing both as we go through this transformation.

**Operator** (Operator):
Your next question will come from Raimo Lenschow with Barclays.

**Unknown Analyst** (Analysts):
This is [ Damon Cogan ] on for Raimo. Just a quick one on the win rates comment, being 3x higher when you engage with 5 or more buying community members. Is there a sense of what share about market customers get that treatment today? And what does that multi-threaded playbook due to sales cost and payback period?

**Yamini Rangan** (Executives):
That's a good question. So first of all, when we talk about multiple stakeholders, we're talking about upmarket customers. And what we are noticing with upmarket customers is that -- they're not doing technology purchase. They're actually making a strategic choice for the AI platform that's ahead, which means they're bringing in CEOs, CTOs, sometimes even the Board for approval. So that is the shift that's happening within upmarket.
And the comment that I made about win rates is that our playbooks are changing to accommodate for how buyers are changing and who becomes the decision maker. And therefore, our sales teams are now really focused on making sure that any large deal that they're working on they are multithreading. They are talking to multiple stakeholders. They are involving our C-level executives and making sure that we have a complete buy-in from upmarket buyers for the decision that they're making.
And specifically, when they do that, we see the win rates improve, which means that the playbook that we have put in place for our upmarket is beginning to work. And we want to double and triple down on that during Q4, but also consistently do that as we go further ahead into next year.

**Operator** (Operator):
Next question will come from Terry Tillman with Truist.

**Giancarlo Valle** (Analysts):
Giancarlo on for Terry here. What AI products do your customers see the highest ROI from? And how quickly do you typically see that value?

**Yamini Rangan** (Executives):
Can you please repeat the question? I think I didn't get the first part of the question.

**Giancarlo Valle** (Analysts):
Yes. I guess what AI products do customers see the highest ROI from? And then how quickly do you typically see that value?

**Yamini Rangan** (Executives):
Great. Thank you for that question. And look, if we step back and go to market, the buyers really care about 4 outcomes. In marketing, they want to build demand. And in sales, they want to be able to win deals and close the pipeline that they have. In post sales, it is about delighting customers. And then overall, go-to-market is about driving efficiency by scaling growth. So if you think about the outcomes, those are the consistent set of outcomes.
Now in terms of the AI products where we are beginning to see a ton of traction. First is actually creating your TAM and the data agent and the combination of data agents and prospecting agent with intent signals is really high value. We've given a number of examples, but the easiest way to think about it is take your data in CRM, whether it is company data or contact data, enrich it so that you can prepare the right audiences for campaigns, enrich it, so you can drive the right prospecting conversations. And so the consistent one is really data agent plus intent plus prospecting. That is what is driving immediate value, and we begin to see that.
The other one, and we've had this as a long-standing one is customer agent. Customer agent resolve support tickets, and we are consistently seeing the quality of the resolution of the tickets is high. And if customers have knowledge base and they have very clear kind of documentation of the processes, it begins to work pretty immediately.
Now those are early. And we are continuing to -- one of the things that we have seen from Q2 to Q3 is the diversification across all of these agents. We now have a fleet of about 8 agents, and there is a diversification in terms of all of these agents, and that shows the value that many of them are beginning to deliver for our customers.

**Operator** (Operator):
Your next question will come from Keith Bachman with BMO.

**Keith Bachman** (Analysts):
I wanted to go back to go-to-market for a second. And the focus is really on trying to understand strategic decisions. What I mean by that is you're rolling out Nordics and Benelux and as Yamini, you indicated, you're going to make some evaluations as you roll broader Europe. When you think about the pricing to new customers, I'm trying to understand what would be the criteria to roll it out to existing customers or not?
And because of the implications, I think, on the duration of the transition are remarkably different. And so would it be possible to have 2-tier customer pricing, one to new customers, one to existing customers? Because if I'm a new customer, I see lower ASPs, I think I want that. But maybe just help me understand the decision-making criteria because, again, it would have meaningful implications, I think, on the duration of transition, but love to hear your feedback here.

**Yamini Rangan** (Executives):
Sure. Thanks a lot for that question, Keith. So just to simplify it, we want to be in a world where our growth drivers are credits and seats. That's it. And that is the future role that we want to be in. And there are multiple steps within the process. The first is, in Q4, all of EMEA is now in this new pilot for new customers. And we want to be able to see it. We want to see the impact in terms of adoption for new customers. We want to be able to look at the adoption of AI and how this is removing friction and based on the results for the new customers, the first step in the decision-making process is how quickly we will roll it out for the rest of the world. That's the first step in the process.
And we want to get a complete handle in terms of how this is removing friction for new customers before we get into the installed base of customers. And so the next step in the decision-making process wants to get high degree of comfort that this is driving AI adoption, it's removing friction. It's driving more Pro+ volume of customers. Once we do that and once we have the new customer rollout, then we'll actually think about the migration. At this point, we're not really focused.
And to your earlier question, yes, this is not one where there is a time line for migration. We don't need to have everybody in one in the longer duration of time, we want it to be in a hybrid model of seats and credits. And I understand the question, and we'll continue to be very transparent as we go through pilots and we learn from those pilots.

**Operator** (Operator):
Your next question will come from Ken Wong with Oppenheimer & Co.

**Hoi-Fung Wong** (Analysts):
I wanted to maybe dig in on what Keith was just asking. I realize there's no time line to push this out to the installed base. But based on what you guys have seen in the Nordics and -- do customers that utilize the new seats [ sold ]-- is there -- do you get a sense that there is a desire to maybe push that model down to the installed base -- what kind of feedback are you getting from customers in terms of that pricing dynamic?

**Yamini Rangan** (Executives):
Sure. Look, let me just explain the pricing dynamics and the feedback that we're getting from customers. The first thing is that we're just removing the seat lines, and you can just buy a go-to-market seat, which means if a customer is trying to figure out, do I need sales Hub Pro with the service sub enterprise, they don't need to do it. So the overall feedback from new customers is that they like the simplicity of just use HubSpot and just use it with a go-to-market seat.
Now that's completely different for our existing customers who've already bought hubs and who understand it. So the first part of it is actually much more beneficial for new customers who just want the simplicity of starting with all of HubSpot capabilities. I think the second one is really how do we reduce the friction of going from a low bundled product for starter to a very high pro for Marketing Hub, Content Hub and Data Hub.
And again, that is beneficial for new customers as they navigate their choices that are there. And what we are seeing is the volume of Pro+ customers is high, even though the ASP, as you can imagine, is initially lower, but the combination of that means that they will continue to upgrade over time.
And then there is a psychological thing that we're seeing, which is like if all of your add-ons is just in one usage-based mechanism, which is credit, then there's somehow an easier way in which customers are adopting. So credit does not become a friction point for new customers. They're just -- they understand what credits are. They're -- they understand it's for all usage-based mechanism, and therefore, they are adopting that more, which is why we see 2 to 3x more credit consumption.
Again, this has been tested with the new customers. It's in all of EMEA as we complete this fiscal year and come back to you in February, will share a lot more details about what we saw in EMEA and therefore, the timing of future rollouts.

**Operator** (Operator):
This concludes today's call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### HUBS_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜Kate Bueker (CFO)｜guidance：下半年每季淨新增客戶預期降至 5,000–6,000（同句並預期 ASRPC 固定匯率成長為低至中個位數）（原話："net additions to be approximately 5,000 to 6,000"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：2026 全年 net new ARR 成長預期低於固定匯率營收成長（原話："expect net new ARR growth to be below constant currency"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：全年 NRR 預期大致持平（原話："net revenue retention to be roughly flat year-over-year"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：Q2 逆風預期持續整個下半年（原話："headwinds we saw in Q2 will persist throughout the remainder"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：Q3 營收財測區間（原話："revenue is expected to be in the range of $924 million"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：全年營收財測（as reported）區間（原話："revenue is now expected to be in the range of $3.678"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：全年 non-GAAP 營業利益財測維持（原話："to be in the range of $762 million to $766 million"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：全年 non-GAAP 稀釋 EPS 財測區間（原話："$13.23 and $13.31"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：全年自由現金流預期約 7.5 億美元（原話："be about $750 million."）
- 2026-08-05｜Yamini Rangan (CEO)｜margin：CEO 說 2027 營業利益率擴張 2–3 點（原話："2 to 3 points of operating margin expansion in 2027"）
- 2026-08-05｜Kate Bueker (CFO)｜margin：CFO 說今年財測含 2 點 non-GAAP 營業利益率槓桿（原話："2 points of non-GAAP operating margin leverage this year"）
- 2026-08-05｜Kate Bueker (CFO)｜margin：non-GAAP 利益率擴張歸因於人力支出紀律、部分被 AI 成本抵銷（原話："disciplined approach to head count spend, partially offset"）
- 2026-08-05｜Kate Bueker (CFO)｜margin：GAAP 營業利益率擴張部分來自 SBC 占營收下降逾 4 點（原話："4-point reduction in stock-based compensation expense"）
- 2026-08-05｜Kate Bueker (CFO)｜commitment：承諾 SBC 占營收逐年下降（原話："we remain committed to driving stock-based compensation"）
- 2026-08-05｜Kate Bueker (CFO)｜commitment：將於 Analyst Day 提供 SBC 細節（原話："Analyst Day next month"）
- 2026-08-05｜Kate Bueker (CFO)｜capital_allocation：Q2 回購逾 5 億美元（原話："more than $500 million of stock under our current"）
- 2026-08-05｜Kate Bueker (CFO)｜capital_allocation：董事會再授權最多 10 億美元回購（原話："an additional share repurchase program of up to $1 billion"）
- 2026-08-05｜Kate Bueker (CFO)｜capital_allocation：資金用途含有機創新與機會型併購（原話："investing in organic innovation and opportunistic M&A"）
- 2026-08-05｜Kate Bueker (CFO)｜customer：Q2 淨新增客戶低於管理層原預期 9,000–10,000（原話："below our 9,000 to 10,000 expectation"）
- 2026-08-05｜Kate Bueker (CFO)｜customer：淨新增不如預期歸因於轉換率與購買猶豫（原話："conversion rates and increased buyer hesitancy"）
- 2026-08-05｜Kate Bueker (CFO)｜customer：Q2 NRR 為 102%（原話："net revenue retention was 102%"）
- 2026-08-05｜Kate Bueker (CFO)｜customer：續約客戶出現降級壓力（原話："seeing some downgrade pressure as they sort of optimize"）
- 2026-08-05｜Yamini Rangan (CEO)｜customer：大單（ARR >12 萬美元）年增 38%（原話："deals over $120,000 ARR grew 38% year-over-year"）
- 2026-08-05｜Yamini Rangan (CEO)｜risk：CEO 承認 4 月起步慢、季度不如預期（原話："April got off to a slow start"）
- 2026-08-05｜Yamini Rangan (CEO)｜risk：買方決策更慢，需高層與董事會核准（原話："leading to longer sales cycles"）
- 2026-08-05｜Yamini Rangan (CEO)｜risk：CEO 表示假設 Q2 情況延續整個下半年（原話："what we saw in Q2 is what we will see in the second half"）
- 2026-08-05｜Kate Bueker (CFO)｜risk：CFO 表示壓力持續到 7 月（原話："we did see it continue into July"）
- 2026-08-05｜Yamini Rangan (CEO)｜risk：CEO 無法給出預算壓力緩解的確切時點（原話："I can't tell you an exact month or a quarter"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：4 月起推出 agent／AEO 試用，管理層承認延長購買流程（原話："We knew this would create some near-term headwinds"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：引進試用讓客戶先體驗再購買（原話："we introduced trials so customers can turn on agents"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：定價改為結果導向並降低入門價（原話："introduced outcome-based pricing for several of"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：Data agent 啟用客戶逾 1.6 萬（原話："Data agent has over 16,000 customers"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：Breeze Assistant 週活躍使用量年初至今翻倍（原話："weekly active usage has doubled since the start of the year"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：每月 agentic actions 年初至今成長逾 3 倍（原話："has increased more than 3x this year"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：客服 agent 無人工介入解決率 72%（原話："Customer agent now resolved 72% of support"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：降價與改制後 Q2 總 credit 用量仍成長（原話："Total credit consumption grew in Q2 despite the"）
- 2026-08-05｜Yamini Rangan (CEO)｜competition：CEO 稱市場競爭激烈、非贏家全拿（原話："it's never a winner-take-all market"）
- 2026-08-05｜Yamini Rangan (CEO)｜competition：CEO 稱客戶不想要來自 10 家廠商的 10 個 agent（原話："They don't want like 10 agents from 10 different vendors"）

### HUBS_Analyst_Investor_Day_HubSpot_Inc_20260917.md
- 2026-09-17｜CFO Kathryn Bueker｜guidance：2026 non-GAAP營業利益率財測21%（較前一年+2點）（原話："our 2026 guidance for non-GAAP operating margin is 21%"）
- 2026-09-17｜CFO Kathryn Bueker｜guidance：2027 non-GAAP營業利益率財測23%–24%（原話："In 2027, we expect non-GAAP operating margin of 23% to 24%"）
- 2026-09-17｜CFO Kathryn Bueker｜guidance：2026自由現金流預期7.5億美元（原話："we expect to deliver $750 million in free cash flow"）
- 2026-09-17｜CFO Kathryn Bueker｜commitment：2030長期目標：non-GAAP營業利益率30%（原話："We expect to deliver non-GAAP operating margins of 30%"）
- 2026-09-17｜CFO Kathryn Bueker｜commitment：2030目標含GAAP營業利益率20%、SBC占營收10%（原話："stock-based compensation as a percentage of revenue of 10%"）
- 2026-09-17｜CFO Kathryn Bueker｜margin：管理層稱2027年COGS成長將快於營收成長（積極投資agent採用）（原話："COGS growth will outpace revenue growth in 2027"）
- 2026-09-17｜CFO Kathryn Bueker｜margin：毛利壓力以模型路由與OpEx槓桿抵銷（原話："balance gross margin pressure with OpEx leverage"）
- 2026-09-17｜CFO Kathryn Bueker｜margin：毛利率策略：先求品質再優化成本（原話："quality number one, and then optimize cost over time"）
- 2026-09-17｜CFO Kathryn Bueker｜margin：客服端已三年未淨增客服人員（原話："We have not added a net new support rep."）
- 2026-09-17｜CFO Kathryn Bueker｜capital_allocation：過去12個月回購逾10億美元（原話："repurchased more than $1 billion in shares"）
- 2026-09-17｜CFO Kathryn Bueker｜capital_allocation：FCF用途含有機/併購與機會性回購（原話："free cash flow for organic and inorganic opportunities"）
- 2026-09-17｜CEO Yamini Rangan｜commitment：管理層重申不在成長與獲利間二選一（原話："committed to driving both durable growth"）
- 2026-09-17｜CEO Yamini Rangan｜risk：上市場客戶買委會擴大、決策延長（原話："larger buying committees"）
- 2026-09-17｜CEO Yamini Rangan｜risk：管理層稱採購遲疑非單季現象（原話："I don't think this is a 1 quarter kind of an effect"）
- 2026-09-17｜CEO Yamini Rangan｜risk：管理層預期仍有定價敏感度（原話："we will see some level of pricing sensitivity"）
- 2026-09-17｜CFO Kathryn Bueker｜risk：淨營收留存率近期大致持平（原話："net revenue retention goes, which is largely flat"）
- 2026-09-17｜CEO Yamini Rangan｜risk：2027能見度：管理層稱現在說還太早（原話："It's pretty early to say what happens in 2027"）
- 2026-09-17｜CEO Yamini Rangan｜product：Breeze Assistant採用率（CEO稱逾55%，8月）（原話："over 55% of our Pro+ customers are using Breeze Assistant"）
- 2026-09-17｜CFO Kathryn Bueker｜product：Breeze Assistant採用率（CFO稱57%，8月）（原話："57% in August"）
- 2026-09-17｜Jon Dick｜product：HubSpot agents觸及19% Pro+客戶，較年初2倍（原話："19% of Pro+ customers are using HubSpot agents as of August"）
- 2026-09-17｜CFO Kathryn Bueker｜product：自訂agent自7月上線後部署逾3,000個（原話："Over 3,000 custom agents have already been deployed"）
- 2026-09-17｜Duncan Lennox｜product：Aviator採模型中立、依任務選模型（原話："Switzerland of AI approach"）
- 2026-09-17｜Duncan Lennox｜product：每週持續執行數千個evals（原話："thousands of these evals that we've built out"）
- 2026-09-17｜Duncan Lennox｜product：ChatGPT連接器週活躍用戶自6月成長250%（原話："weekly active users on ChatGPT up 250% since June"）
- 2026-09-17｜CEO Yamini Rangan｜customer：連接器用戶約35萬、留存提升12點（原話："nearly 350,000 users on connectors"）
- 2026-09-17｜CEO Yamini Rangan｜customer：使用連接器的客群留存改善12點（原話："12-point improvement in retention"）
- 2026-09-17｜Jon Dick｜customer：夥伴參與上市場交易：勝率與ASP較高（原話："nearly an 8-point higher win rate, 75% higher ASP"）
- 2026-09-17｜Jon Dick｜customer：$12萬以上ARR大單年增38%（原話："deals over $120,000 of ARR, up 38% year-over-year"）
- 2026-09-17｜CFO Kathryn Bueker｜customer：Starter客戶15萬，約占客戶數一半（原話："150,000 starter customers on HubSpot"）
- 2026-09-17｜Jon Dick｜customer：下市場客戶價格敏感且時間受限（原話："They're more price sensitive, they're time constrained"）
- 2026-09-17｜Jon Dick｜customer：Q4加碼促銷下市場（原話："we are ramping up our promotion in Q4"）
- 2026-09-17｜Duncan Lennox｜product：AI Growth Bundle：新客Starter與credits折扣65%（原話："65% off HubSpot Starter and HubSpot credits"）
- 2026-09-17｜CFO Kathryn Bueker｜product：付費席位自2024定價簡化後成長80%（原話："paid seats up 80% since our 2024 pricing simplification"）
- 2026-09-17｜CFO Kathryn Bueker｜product：2024簡化席位定價帶來NRR約2點效益（原話："approximately 2 points of benefit in net revenue retention"）
- 2026-09-17｜CFO Kathryn Bueker｜product：4月降agent價並轉結果導向定價，造成短期逆風（原話："which created a near-term headwind"）
- 2026-09-17｜CFO Kathryn Bueker｜commitment：預期席位與credits將成營收主要驅動（原話："seats and credits will be the primary drivers"）
- 2026-09-17｜CEO Yamini Rangan｜product：非綁定go-to-market人員的項目將改按credits計（原話："should just be based on credits"）
- 2026-09-17｜CFO Kathryn Bueker｜product：Nordics/Benelux試點：初始ASP較低、後續成長較大（原話："lower initial ASPs, but larger growth trajectory"）
- 2026-09-17｜CFO Kathryn Bueker｜product：試點擴大到EMEA新客，下月起（原話："we're moving into EMEA for new customers next month"）
- 2026-09-17｜Jon Dick｜competition：對自行開發CRM：起步易、規模化難（原話："scaling it is exceptionally hard"）
- 2026-09-17｜Jon Dick｜competition：對AI點解決方案：不認為有人要agent sprawl（原話："we don't think anybody will want agents sprawl"）
- 2026-09-17｜Duncan Lennox｜competition：headless策略質疑：分析師問為何對應用軟體公司有利（原話："why is headless good for an application software company?"）
- 2026-09-17｜Jackson Ader (KeyBanc)｜competition：headless策略質疑：分析師問為何對應用軟體公司有利（原話："why is headless good for an application software company?"）

### 問答異常語氣（迴避／改口／保留）
- HUBS_Q2_2026_Earnings_Call_20260805.md｜問：Samad Samana（Jefferies）問除已知的定價、銷售訓練、服務條款變更與回滾外，是否還有其他決策干擾結果、是否需更積極行動｜答法：回答聚焦試用與定價兩項刻意改變及需求環境，未回應服務條款變更與回滾，也未直接回答是否需要更積極動作
- HUBS_Q2_2026_Earnings_Call_20260805.md｜問：Eamon Coughlin（Barclays）問 credit 用量中付費 vs 內含／試用的占比｜答法：改談 reach、depth、quality 等領先指標，未提供付費與內含用量的比例
- HUBS_Q2_2026_Earnings_Call_20260805.md｜問：Gabriela Borges（Goldman）問環境何時好轉、是否為新常態｜答法：未給時間表，僅說假設 Q2 情況延續下半年並提供客戶信心措施
- HUBS_Q2_2026_Earnings_Call_20260805.md｜問：Jackson Ader（KeyBanc）問客戶把預算轉去哪裡、預算壓力何時緩解｜答法：表示沒有水晶球、無法指出確切月份或季度，改談 token maxing 與結果導向定價
- HUBS_Q2_2026_Earnings_Call_20260805.md｜問：Rishi Jaluria（RBC）問是否有 AI 原生新廠商造成市場雜訊與更高審查｜答法：以易用與平台優勢回應，未點名競爭者或說明新廠商是否造成影響
- HUBS_Q2_2026_Earnings_Call_20260805.md｜問：Q&A 中 CEO 引用 agent 客戶數｜答法：口頭說「Customer agent, 18,000 customers that grew by 80%」，與準備稿 customer agent 逾 10,000、data agent 啟用 1.6 萬且季增 80% 不一致，隨即自行更正 data agent 為 1.6 萬
- HUBS_Analyst_Investor_Day_HubSpot_Inc_20260917.md｜問：Piper Sandler問：第一方產品使用前沿模型vs開源模型比重、是否自建模型｜答法：Lennox未給比重，稱持續評估各模型；Bueker稱毛利處於『very early』、品質優先
- HUBS_Analyst_Investor_Day_HubSpot_Inc_20260917.md｜問：Citi問：定價變動與促銷對近期營收/ARR成長形狀的影響｜答法：Bueker/Rangan談定價實驗與降門檻，未給近期營收或ARR影響的數字
- HUBS_Analyst_Investor_Day_HubSpot_Inc_20260917.md｜問：Raymond James問：NRR長期是否上升及合理水準｜答法：Bueker僅稱近期大致持平、長期有順風，未給數字
- HUBS_Analyst_Investor_Day_HubSpot_Inc_20260917.md｜問：Needham問：2027年AI工作流能見度是否改善營運環境｜答法：Rangan稱『pretty early to say』，未對2027給判斷

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
{"date":"20260522","verdict":"B 觀望（thesis 偏 observation；估值 5Y 分位 3% 極便宜但 Pure MA ❌ 盲點 2 救援失敗 + 4 家券商 5/8 同步降評；等 Q2 FY26 8/6 Customer Agent ARR 揭露）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"ARR YoY growth 維持 ≥ 18% — HubSpot 業務動能未被 AI native + Microsoft 蠶食，SMB CRM 換代週期持續","columns":{"2Y 驗證點":"Q2-Q4 FY26 ARR YoY ≥ 18%（vs Q1 +23% 維持高水位）","5Y 驗證點":"FY29 ARR 達 $6-7B（從 FY26 ~$3.7B 起算 17-18% CAGR）","10Y 驗證點":"FY31 sub rev $8-10B（10Y 從 FY25 .13B 起算 13-15% CAGR）","具體數字門檻":"FY26 全年 ARR ≥ +18% YoY；FY27 guide ≥ +15%","信息來源":"HUBS Q1 FY26 8-K + 5/7 earnings call","漂移觸發條件":"連 2 季 ARR YoY &lt; 18% → 削弱（2Y 假設適用 QC-34/35）"}},{"id":"H2","text":"Non-GAAP Operating Margin 持續擴張至 22-24% — operational leverage 兌現，GTM 轉型不傷利潤","columns":{"2Y 驗證點":"FY26 退出 Non-GAAP OpMargin ≥ 19%（vs Q1 18%）","5Y 驗證點":"FY29 Non-GAAP OpMargin ≥ 22%","10Y 驗證點":"FY31 Non-GAAP OpMargin 達 24%+ steady state","具體數字門檻":"FY26 退出率 ≥ 19%；FY27 入場 guide ≥ 20%","信息來源":"HUBS Q1 FY26 8-K + 5/7 earnings call","漂移觸發條件":"連 2 季 Non-GAAP OpMargin YoY 下降 ≥ 100bp → 削弱"}},{"id":"H3","text":"Customer Agent + Prospecting Agent ARR 達 -500M FY27 — AI 戰略兌現，pricing power 護城河加深","columns":{"2Y 驗證點":"Q4 FY26 Customer Agent ARR 揭露 ≥ $50M","5Y 驗證點":"FY29 Customer Agent ARR ≥ -B（佔 sub rev ~15-20%）","10Y 驗證點":"Agent ARR 成為獨立 line item disclosure","具體數字門檻":"Q4 FY26 揭露 ≥ $50M；FY27 揭露 ≥ -500M","信息來源":"5/7 earnings call Yamini 開場語 + Spring Spotlight 2026/3","漂移觸發條件":"連 2 季 Customer Agent active customer 絕對下降 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Microsoft Copilot for Sales + AI-native CRM (Apollo/Clay/Attio) 從 mid-market 雙夾擊 HubSpot","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"Microsoft Copilot for Sales 公開搶單案例；HubSpot 新客戶 ACV YoY 趨勢；NRR 趨勢","警戒閾值":"Microsoft / Apollo / Clay 任一拿下 ≥ -10M ACV HubSpot 客戶 ≥ 2 件；NRR 連 2 季 &lt; 100%"}},{"id":"R2","text":"GTM 從 contact-tier 轉 seats+credits 執行失敗 — customer churn 加速、新客戶 net add 變慢","columns":{"對應假設":"H1 / H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Customer count quarterly net add；ARPU 趨勢；NRR","警戒閾值":"連 2 季 net add &lt; 10,000；NRR 連 2 季 &lt; 100%；Gross retention &lt; 88%"}},{"id":"R3","text":"SMB CRM 變 commodity / Google Workspace + Microsoft 365 內建 CRM 模組取代 standalone tier","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Google / Microsoft 是否公告內建 CRM；HubSpot Starter tier customer churn 加速","警戒閾值":"Google / Microsoft 任一公告免費 CRM 模組（≥ 50% 機率才砍倉）；Starter tier 客戶 YoY 連 4 季絕對下降"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"❌","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":198.37,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBS_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
