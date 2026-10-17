你是 stock-analyst **v20 判斷 agent**，標的 ASML（20261017）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ASML","date":"2026-10-17","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ASML_20261017/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ASML_20261017/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_net_sales","label":"Total net sales","value":11662,"period":"Q3 2026（公告於 2026-10-14）","unit":"€百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（公告於 2026-10-14）","citation":"ASML Q3 2026 新聞稿（6-K）"},"note":"未查得"},{"id":"f_kpi1_gross_margin","label":"Gross margin","value":57.5,"period":"Q3 2026（公告於 2026-10-14）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（公告於 2026-10-14）","citation":"ASML Q3 2026 新聞稿（6-K）"},"note":"未查得"},{"id":"f_kpi2_net_income","label":"Net income","value":4960,"period":"Q3 2026（公告於 2026-10-14）","unit":"€百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（公告於 2026-10-14）","citation":"ASML Q3 2026 新聞稿（6-K）"},"note":"未查得"},{"id":"f_kpi3_installed_base_managemen","label":"Installed Base Management sales","value":3289,"period":"Q3 2026（公告於 2026-10-14）","unit":"€百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（公告於 2026-10-14）","citation":"ASML Q3 2026 新聞稿（6-K）"},"note":"高於公司自家指引約 €400 百萬（CEO 說法，見搜尋摘要，未逐字核對）"},{"id":"f_kpi4_guidance_q4_2026","label":"Guidance Q4 2026","value":"net sales €14.2–15.2bn；gross margin 約 57%；R&D 約 €1.2bn；SG&A 約 €0.4bn","period":"Q3 2026（公告於 2026-10-14）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（公告於 2026-10-14）","citation":"ASML Q3 2026 新聞稿（6-K）"},"note":"未查得"},{"id":"f_kpi5_guidance_fy2026","label":"Guidance FY2026","value":"net sales €44–45bn；gross margin 約 56%","period":"Q3 2026（公告於 2026-10-14）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（公告於 2026-10-14）","citation":"ASML Q3 2026 新聞稿（6-K）；搜尋摘要稱 7 月指引為 €43–45bn、毛利率 54–56%（未逐字核對）"},"note":"未查得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-14","period":"2026-10-14","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-14"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_asml_gross_margin_pct","label":"ASML 毛利率","value":52.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_asml_operating_margin_pct","label":"ASML 營業利益率","value":35.42,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_asml_fcf_margin_pct","label":"ASML FCF 利潤率","value":24.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2330_tw_gross_margin_pct","label":"2330.TW 毛利率","value":64.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2330_tw_operating_margin_pct","label":"2330.TW 營業利益率","value":56.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2330_tw_fcf_margin_pct","label":"2330.TW FCF 利潤率","value":25.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvda_gross_margin_pct","label":"NVDA 毛利率","value":74.67,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_operating_margin_pct","label":"NVDA 營業利益率","value":65.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_fcf_margin_pct","label":"NVDA FCF 利潤率","value":41.92,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_onto_gross_margin_pct","label":"ONTO 毛利率","value":50.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONTO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_onto_operating_margin_pct","label":"ONTO 營業利益率","value":13.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONTO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_onto_fcf_margin_pct","label":"ONTO FCF 利潤率","value":22.54,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONTO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":1641.52,"period":"2026-10-16（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":12.84,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":37.67,"period":"2026-10-16（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-1.69,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（43.68 → 42.94）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-1.39,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（58.95 → 58.13）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-1.32,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（77.48 → 76.46）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":42.94,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":58.13,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":76.46,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":11.33,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 38.57 → 42.94（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":40.39,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝51.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":51.9,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":16.03,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":15.75,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":41.46,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 42.94，分子＝快照價 1780.34","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.552,"period":"2026-10-17","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-17"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-10772.1,"period":"2026-10-17","unit":"EUR m","basis":"yfinance 最新一季：總債務 1963.0、現金 12735.1（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-17"},"note":"財報幣別 EUR ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 EUR，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":385.42,"period":"2026-10-17","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-17"},"note":"財報幣別 EUR ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 EUR，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":44468.86,"period":"2026-10-17","unit":"EUR m","basis":"yfinance revenue_estimate 0y 平均（34 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-17"},"note":"財報幣別 EUR ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 EUR，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":57214.82,"period":"2026-10-17","unit":"EUR m","basis":"yfinance revenue_estimate +1y 平均（38 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-17"},"note":"財報幣別 EUR ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 EUR，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"ASML 2026 年指引二度上調至營收 €43–45B；Q2 營收年增 21% 至 €9.33B；中國占比降至 14%、台灣升至 30%。搜尋未顯示光刻市占本身有變動證據。","source":"TrendForce News: ASML raises 2026 guidance for second time this year, Taiwan sales share climbs to 30%","url":"https://www.trendforce.com/news/2026/07/15/news-asml-raises-2026-guidance-for-second-time-this-year-taiwan-sales-share-climbs-to-30/","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261017","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"今夏有報導稱中國光刻機廠（上海某公司）今年出貨 5 台 DUV、2027 年暫定 20 台，ASML 股價兩個交易日跌約 10%；其為 DUV 非 EUV，被評為距 EUV 多年，機台未經驗證。","source":"Barchart/Nasdaq: Everyone's focused on China but that's not ASML's biggest risk","url":"https://www.nasdaq.com/articles/everyones-focused-china-thats-not-asmls-biggest-risk","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Musk 的 Terafab 被指為潛在客戶亦為潛在 EUV 對手（自由電子雷射光源路線），FEL-EUV 尚未量產就緒，未宣布設備訂單。","source":"Dealroom: ASML faces a double-edged Terafab: prospective customer and potential EUV rival","url":"https://dealroom.co/news/143828-asml-faces-a-double-edged-terafab-prospective-customer-and-potential-euv/","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"2026 年 6 月報導稱 Nikon 與美亞大型晶片廠進行進階洽談、數案接近正式採購單（未證實）；Canon 奈米壓印僅用於 3D NAND 等特定應用，尚不構成對 ASML 的威脅。","source":"IPS News: Competitor Challenges ASML in the Evolving Global Semiconductor Lithography Landscape","url":"https://ipsnews.net/business/2026/06/10/competitor-challenges-asml-in-the-evolving-global-semiconductor-lithography-landscape/","excerpt":null,"as_of":"2026-06-10","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Bloomberg 報導 TSMC 認為 ASML 最新設備過貴；TSMC 將在 2029 年前不把最先進（High-NA）機台用於量產以節省成本（搜尋摘要轉述，非逐字）","source":"Bloomberg video, 'TSMC says ASML's latest chipmaking gear is too pricey', 2026-04-23","url":"https://www.bloomberg.com/news/videos/2026-04-23/tsmc-says-asml-s-latest-chipmaking-gear-is-too-pricey-video","excerpt":null,"as_of":"2026-04-23","retrieved_at":"20261017","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"美國支持的新創 xLight 以自由電子雷射作為 EUV 光源替代方案，據報正洽募資 3.5 億美元，原型目標 2028 年；ASML 執行長稱正與 xLight 合作技術展示。Substrate（Thiel 支持）發展 X-ray 微影。目前無客戶改採第二供應商或自製微影機的證據","source":"The Next Web, xLight EUV $350M ASML Euclyd, 2026-06-24","url":"https://thenextweb.com/news/xlight-euv-350m-asml-euclyd","excerpt":null,"as_of":"2026-06-24","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"ASML FY2025 20-F 風險因子標題載明「淨銷售額高比例來自少數客戶」；本次搜尋未取得 FY2025 最大客戶占比數字","source":"SEC EDGAR ASML Form 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/0000937966/000162828026011378/asml-20251231.htm","excerpt":"A high percentage of net sales is derived from a few customers","as_of":"2026-02-01","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"歷史揭露：FY2021 最大客戶占淨銷售約37.0%，前兩大客戶合計66.3%（FY2020 為31.4%、FY2019 為39.7%）","source":"SEC EDGAR ASML Form 20-F FY2021 / FY2020","url":"https://www.sec.gov/Archives/edgar/data/937966/000093796622000013/asml-20211231.htm","excerpt":null,"as_of":"2022-02-01","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Mizuho 下調 ASML 至中立，理由含對台積電的客戶集中度上升；預期 Samsung、Intel 2026 上行有限（為訂單面，非信用面）","source":"itiger: ASML cut to Neutral at Mizuho on downside risk to 2026 business outlook","url":"https://www.itiger.com/news/2524617419","excerpt":"higher customer concentration to TSMC","as_of":"2026-07-01","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2026 Q1 韓國占系統銷售由22%升至45%（Samsung、SK Hynix 記憶體擴產），記憶體機台占比由30%升至51%；為地區別數據，未拆單一客戶","source":"TrendForce News: ASML raises 2026 sales outlook","url":"https://www.trendforce.com/news/2026/04/15/news-asml-raises-2026-sales-outlook-to-e36b-e40b-on-memory-and-logic-client-demand-south-korea-share-hits-45/","excerpt":"The sales share in South Korea rose from 22% to 45%","as_of":"2026-04-15","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ASML 在 Q3 2026 財報表示，現行 2027 與 2028 供給計畫仍無法完全滿足客戶需求","source":"ASML Form 6-K Q3 2026 press release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000937966/000162828026065813/pressreleasefinancialresul.htm","excerpt":"With such strong visibility and an order book momentum that continues to increase quarter on quarter this year, we now expect that our supply as currently planned for both 2027 and 2028 will not fully meet the demand of our customers.","as_of":"2026-10-15","retrieved_at":"20261017","affects":["thesis.H","moat_trend","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ASML 已規劃 2027 年低 NA EUV 與 DUV 浸潤式產能較 2026 增 30%，並研究 2028 年超過 30% 的擴產","source":"ASML Q3 2026 results (secondary summary)","url":"https://evertiq.com/design/2026-10-15-asml-expects-demand-to-outstrip-supply-in-2027-and-2028","excerpt":"investigating ways to increase capacity for 2028 beyond the 30% increase we previously communicated","as_of":"2026-10-15","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"部分客戶有意下 2029、2030 年訂單；有分析提醒其中部分可能是保留產能行為而非確定訂單","source":"ASML Q3 2026 results (secondary summary)","url":"https://evertiq.com/design/2026-10-15-asml-expects-demand-to-outstrip-supply-in-2027-and-2028","excerpt":"some customers are expressing an interest in placing orders with us for 2029 and even 2030","as_of":"2026-10-15","retrieved_at":"20261017","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q3 2026 淨銷售創高 €11.7bn；Q4 指引 €14.2–15.2bn，全年 2026 預期 €44–45bn","source":"ASML Q3 2026 results (secondary summary)","url":"https://investinglive.com/stocks/asml-says-2027-and-2028-supply-will-fall-short-of-demand-as-q3-sales-hit-a-record/","excerpt":"Q4 guidance is sales of €14.2bn to €15.2bn with a gross margin around 57%. Full-year 2026 sales are now seen at €44bn to €45bn, with a margin around 56%","as_of":"2026-10-15","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SEMI 2025 年底預測設備總銷售 2027 年達 $156bn（2026 年 $145bn），WFE 2027 年 $135.2bn；中國銷售預期自 2026 起逐步下滑（該預測非 2026 年更新版）","source":"SEMI press release 2025-12-16","url":"https://semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports","excerpt":null,"as_of":"2025-12-16","retrieved_at":"20261017","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"記憶體端：SK Hynix 約 $38bn 新廠 M17 第一座無塵室最早 2028 年 12 月開出，Micron 稱 2027、2028 年需求仍超過供給；另有 Silicon Motion 觀點認為 DRAM 自 2027 下半年新大廠量產後可望緩解（各家說法不一，二手彙整，日期未標）","source":"Webull 'SK Hynix Approved $38 Billion of New Memory Fabs That Won't Produce a Chip Before December 2028'","url":"https://www.webull.com/news/15408108739732480","excerpt":"In calendar 2027 as well as 2028, we see demand exceeding supply.","as_of":"2026-07-11","retrieved_at":"20261017","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"美國商務部長 Lutnick 據報向 ASML 高層詢問是否有 EUV 機台違反美方主導管制流入中國；ASML 表示全力遵守所有適用法規。Commerce 未對是否掌握出貨證據置評，消息來源未提出佐證（單一媒體報導）。","source":"NL Times: US commerce secretary raises concerns over reports ASML machine reached China","url":"https://nltimes.nl/2026/06/19/us-commerce-secretary-raises-concerns-reports-asml-machine-reached-china","excerpt":"fully committed to complying with all applicable regulations","as_of":"2026-06-19","retrieved_at":"20261017","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026年6月報導：美國商務部長 Lutnick 據稱向 ASML 提出疑慮，認為有一台 EUV 設備可能流入中國；ASML 否認，稱從未向中國出貨 EUV 或其專用零件。報導時屬未證實的審查，非確認違規。","source":"China Global South: ASML Denies Selling EUV Chipmaking Tool to China After Report of U.S. Concern","url":"https://chinaglobalsouth.com/2026/06/19/asml-rejects-claims-euv-chip-tool-reached-china/","excerpt":null,"as_of":"2026-06-19","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025年7月 ASML 因川普關稅不確定性收窄全年財測，執行長稱仍規劃 2026 年成長但無法確認；搜尋未找到 2026 年 Section 232 半導體關稅是否實施及對 ASML 影響的報導。","source":"iTiger: ASML Narrows Guidance Amid Tariff Uncertainty, Warns On 2026 Growth","url":"https://www.itiger.com/news/2551112649","excerpt":null,"as_of":"2025-07-16","retrieved_at":"20261017","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"ASML 20-F 披露 Carl Zeiss SMT 為其光學元件唯一供應商；Zeiss 產能可能限制系統產量，若關係終止或光學供應長期中斷，ASML 實質上無法營運（該 20-F 為 FY2020 版，現況可能已變）。","source":"ASML Holding NV Form 20-F FY2020 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/937966/000093796621000007/asml-20201231.htm","excerpt":null,"as_of":"2021-02-10","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026 年 Q1 中國大陸占 ASML 銷售 19%（前季 36%）；公司預期 2026 年中國約占 20%；2025 全年中國占 33%。","source":"Caixin Global: ASML's China sales slump as export curbs bite","url":"https://www.caixinglobal.com/2026-04-16/asmls-china-sales-slump-as-export-curbs-bite-102434749.html","excerpt":null,"as_of":"2026-04-16","retrieved_at":"20261017","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026 年 4 月美國議員提出 MATCH Act，擬將 EUV 禁令延伸至 DUV 浸潤式設備；若美國立法且荷蘭執行，將是自 2024 年 9 月以來首度新增對 ASML 的限制；分析師估影響為營收個位數百分比，另有估 EPS 最多降 10%。","source":"MarketScreener: ASML shares fall on US Congress plan to further restrict China exports","url":"https://www.marketscreener.com/news/asml-shares-fall-on-us-congress-plan-to-further-restrict-china-exports-ce7e51d3dc8eff21","excerpt":null,"as_of":"2026-04-16","retrieved_at":"20261017","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"有報導稱 ASML 評估在東南亞設廠以降低中國相關曝險，但屬未證實、來源可信度低。","source":"Globe and Mail / 聚合報導（ASML chipmakers 2026 growth US tariff）","url":"https://www.theglobeandmail.com/business/article-asml-chipmakers-2026-growth-us-tariff","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261017","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"ASML Q3 2026（2026-10-14 公布）淨銷售€11.66B、毛利率57.5%、淨利€4.96B；系統銷售€8.373B（EUV約€4.1B，含1台High-NA）、裝機管理€3.289B；Q4指引€14.2–15.2B","source":"ASML Form 6-K Q3 2026 / Quartr Q3 2026 earnings summary","url":"https://www.sec.gov/Archives/edgar/data/0000937966/000162828026065813/pressreleasefinancialresul.htm","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"2026全年指引上調並收窄至€44–45B（7月為€43–45B；4月為€36–40B）；分段成長：EUV >45%、非EUV系統約20%、裝機管理約50%；邏輯系統銷售約+10%、記憶體約+75%（來源未單獨拆DUV）","source":"ASML Q3 2026 results coverage (SEC 6-K / Quartr / Trivano)","url":"https://www.trivano.com/persbericht/asml-reports-eur117-billion-total-net-sales-and-eur50-billion-net-income-in-q3-2026-767037.html","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3後說法：AI需求增強，2027–2028規劃產能可能不足以滿足客戶需求，未設新的2027–2028產出目標","source":"Quartr ASML Q3 2026 investor call summary","url":"https://quartr.com/events/asml-holding-n-v-asml-q3-2026-investor-call_3YH2Nyl8","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261017","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026（2026-07-15）：管理層稱客戶能見度延伸數年；2027低數值孔徑EUV產能較2026約65台增加30%、2028再研究增加30%；DUV浸潤式產能自約130台增加30%；中國約占集團銷售20%","source":"Investing.com / MarketBeat / Arkolith Q2 2026 coverage","url":"https://arkolith.com/news/news-asml-ai-demand-capacity","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261017","affects":["thesis.H","triggers"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"Morgan Stanley估2027年EUV出貨約80台（創紀錄），其中約52台給邏輯/晶圓代工；該估計早於Q2財報；並提醒2028成長高度不確定","source":"Morgan Stanley via itiger: ASML's Peak Moment","url":"https://www-web.itiger.com/news/1166060522","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261017","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"市佔：EUV唯一供應商，整體光刻市佔約90%，Nikon與Canon落後（2026年1月投資摘要）","source":"itiger: ASML Stock Price Forecast 2026","url":"https://www.itiger.com/news/2652232986","excerpt":"ASML holds a 90% share of the global lithography market and is the only supplier of EUV technology","as_of":"2026-01-01","retrieved_at":"20261017","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"0","claim":"價格：TrendForce報導ASML尋求漲價、TSMC據報抵制，成熟DUV可能漲約10%，TSMC因High-NA單價約US$400M而延後採用；Q2電話會稱漲價受長訂單週期限制，不會立即生效","source":"TrendForce News 2026-07-16","url":"https://www.trendforce.com/news/2026/07/16/news-asml-reportedly-seeks-higher-tool-prices-as-tsmc-pushes-back-mature-duv-tools-could-see-10-hike/","excerpt":"ASML is also seeking higher prices for its chipmaking equipment, a move TSMC is said to be resisting.","as_of":"2026-07-16","retrieved_at":"20261017","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"+","claim":"SEMI 2026年中預測：全球設備銷售2026年US$165.9B（+23.2%），2028年US$229.5B；WFE 2026年US$143.9B，2027年+21.8%、2028年+14.1%至約US$200B；主因AI帶動HBM DRAM與先進邏輯投資","source":"SEMI mid-year 2026 forecast via iconnect007","url":"https://iconnect007.com/article/150797/global-semiconductor-equipment-sales-forecast-to-reach-a-record-229-billion-in-2028/150794/ein","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"ASML 自家 20-F 風險因子載明：若競爭者的替代技術更有效，或客戶轉向較不依賴微影的新架構，業務將受損。","source":"ASML Holding NV Form 20-F FY2019 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000937966/000093796620000011/a2019integratedreportb.htm","excerpt":"Our business will suffer if the technologies that we pursue to assist our customers in producing smaller and more energy-efficient chips are not as effective as those developed by competitors, or if our customers adopt new technological architectures that are less focused on lithography products.","as_of":"2020-02-01","retrieved_at":"20261017","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"2026-07 評論指出 EUV 層級對手仍遠遠落後；中國 SMEE 報導已交付早期 28nm ArF 浸潤式 DUV，尚未產品化，被稱為原型階段。","source":"Takshashila, ASML's Blowout Quarter Is a Geopolitical Signal (2026-07-17)","url":"https://takshashila.org.in/content/blogs/20260717-asml-geopolitical-signal.html","excerpt":null,"as_of":"2026-07-17","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Yonhap 報導之分析：即使中國取得 20 台 ArF 浸潤式微影機，對 ASML 2027 年營收影響約 14 億歐元，占整體約 2.4%。","source":"Yonhap-reported analysis via Nasdaq/search summary","url":"https://www.nasdaq.com/articles/asml-new-chinese-competitor-major-threat-nasdaq-asml","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261017","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"新創 Substrate 於 2025 年底宣稱 X 光微影可媲美 EUV；Bernstein 分析師稱該技術早年已被提出但未能推進，EUV 成熟後被放棄。","source":"Finviz: Is ASML's Leadership Threatened After Substrate's Recent Better Technology Claims?","url":"https://finviz.com/news/230513/is-asmls-asml-leadership-threatened-after-substrates-recent-better-technology-claims","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"-","claim":"MATCH Act 正於美國國會審議，將禁止對中國銷售新 DUV 並含既有設備維修服務。","source":"Search summary of commentary (nasdaq.com 'everyones focused china thats not asmls biggest risk')","url":"https://www.nasdaq.com/articles/everyones-focused-china-thats-not-asmls-biggest-risk","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"未找到通路或商業模式的正式轉變；可查到的是安裝基礎管理（IBM，服務與現場選配）營收在 2026 Q2 約 28 億歐元，高於指引約 3 億歐元，主要來自升級業務，管理層預期 2026 年 IBM 成長逾 30%。","source":"ASML Q2 2026 investor call transcript (2026-07-15)","url":"https://ourbrand.asml.com/asset/1fd3908a-0381-47b5-9b69-a3094f656651/2026_07_15-ASML-Transcript-investor-call-Q2-2026.pdf","excerpt":"Installed Base Management sales for the quarter came in at 2.8 billion euros, almost 300 million euros above our guidance, a result driven primarily by additional upgrade business.","as_of":"2026-07-15","retrieved_at":"20261017","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"IBM 預期 2026 年成長逾 30%，驅動來自擴大中的 EUV 安裝基礎之服務營收與客戶對效能／產能升級的需求。","source":"ASML Q2 2026 earnings call (MarketBeat highlights)","url":"https://www.marketbeat.com/instant-alerts/asml-q2-earnings-call-highlights-2026-07-15/","excerpt":"Installed Base Management sales are expected to grow more than 30%, driven by service revenue from the expanding EUV installed base and customer demand for performance and productivity upgrades.","as_of":"2026-07-15","retrieved_at":"20261017","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"ASML 2026 年 7 月將全年 2026 營收指引上調至 €430–450 億、毛利率 54–56%（前次 51–53%）；Q3 營收指引 €110–120 億。搜尋結果未見任何 2026 年下修。","source":"SEC EDGAR ASML Form 6-K FY2026；Investing.com 'ASML gains after Q2 beat, raises 2026 outlook on AI chip demand'（二手摘要）","url":"https://www.investing.com/news/earnings/asml-q2-outlook-tops-on-ai-chip-demand-lifts-fullyear-forecast-4792148","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026 年 4 月（Q1）ASML 將全年銷售指引由 €340–390 億上調至 €360–400 億、毛利率 51–53%；Q2 指引中位 €87 億低於共識 €91 億。","source":"Chartmill / tikr 等二手報導 Q1 2026 業績","url":"https://www.chartmill.com/news/ASML.AS/Chartmill-45349-ASML-HOLDING-NV-AMSASML-Shares-Drop-Despite-Q1-2026-Earnings-Beat-on-Cautious-Guidance","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"MarketBeat 彙總 2026 年 7 月底共識評級 Moderate Buy、平均目標價約 $1,970.33；JPMorgan 7/16 目標價 $2,200→$2,400（overweight）、Bernstein $1,971→$2,623（outperform）、RBC 7/14 $1,700→$2,000（outperform）。各聚合站數字不一致（TickerLeague 4 位分析師共識 $2,305.75，區間 $2,000–$2,623；Benzinga 頁 $1,710 疑過時）。","source":"MarketBeat 'ASML stock price expected to rise, JPMorgan analyst says' 2026-07-16；TickerLeague ASML estimates","url":"https://www.marketbeat.com/instant-alerts/asml-nasdaqasml-stock-price-expected-to-rise-jpmorgan-chase-co-analyst-says-2026-07-16/","excerpt":"JPMorgan Chase & Co. lifted their price target on ASML from $2,200.00 to $2,400.00 and gave the company an \"overweight\" rating in a research note on Thursday, July 16th.","as_of":"2026-07-16","retrieved_at":"20261017","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Erste Group 2026-07-31 將 ASML FY2026 EPS 預估由 $36.94 上調至 $44.50，高於共識 $43.60（估計上修的一例）。","source":"MarketBeat 'FY2026 earnings estimate for ASML issued by Erste Group Bank' 2026-07-31","url":"https://www.marketbeat.com/instant-alerts/fy2026-earnings-estimate-for-asml-issued-by-erste-group-bank-2026-07-31/","excerpt":"Erste Group Bank raised ASML's FY2026 EPS estimate to $44.50 from $36.94, above the $43.60 consensus.","as_of":"2026-07-31","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"美國 SDNY 有針對 ASML 與三名高管的證券集體訴訟（Case 24-cv-08664），集體期間 2024-01-24 至 2024-10-15，主張 10(b)/20(a)；來源為律所新聞稿，指控未經裁定，搜尋結果未見判決或和解。此案提起於 12 個月視窗之前，是否仍在進行未查明。","source":"Pomerantz／KTMC 律所公告（SDxCentral、ktmc.com）","url":"https://ktmc.com/new-cases/asml-holding-nv","excerpt":"Class Period January 24, 2024 through October 15, 2024","as_of":"2024-11-01","retrieved_at":"20261017","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"SDNY 證券集體訴訟 City of Hollywood Firefighters' Pension Fund v. ASML Holding N.V.（24-cv-08664），集體期間 2024-01-24 至 2024-10-15；指控未經裁定；未見判決或和解。提起日在 12 個月視窗之前。","source":"KTMC 律所公告 ASML Holding N.V. Securities Fraud Class Action","url":"https://ktmc.com/new-cases/asml-holding-nv","excerpt":"Class Period January 24, 2024 through October 15, 2024","as_of":"2024-11-01","retrieved_at":"20261017","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ASML","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":52.73,"operating_margin_pct":35.42,"fcf_margin_pct":24.27,"rd_intensity_pct":13.68},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"2330.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.23,"operating_margin_pct":56.1,"fcf_margin_pct":25.33,"rd_intensity_pct":6.07},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"NVDA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.67,"operating_margin_pct":65.21,"fcf_margin_pct":41.92,"rd_intensity_pct":7.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"ONTO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.36,"operating_margin_pct":13.81,"fcf_margin_pct":22.54,"rd_intensity_pct":12.73},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONTO","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"ASML"},"financial_history":{"ticker":"ASML","currency":"EUR","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":21173400000.0,"revenue_yoy_pct":null,"gross_margin_pct":50.54,"operating_margin_pct":30.7,"net_income":5624200000.0,"diluted_eps":16.07,"free_cash_flow":7167500000.0,"fcf_margin_pct":33.85,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":27558500000.0,"revenue_yoy_pct":30.16,"gross_margin_pct":51.29,"operating_margin_pct":32.81,"net_income":7839000000.0,"diluted_eps":20.59,"free_cash_flow":3247200000.0,"fcf_margin_pct":11.78,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":28262900000.0,"revenue_yoy_pct":2.56,"gross_margin_pct":51.28,"operating_margin_pct":31.92,"net_income":7571600000.0,"diluted_eps":19.24,"free_cash_flow":9083100000.0,"fcf_margin_pct":32.14,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":32667300000.0,"revenue_yoy_pct":15.58,"gross_margin_pct":52.83,"operating_margin_pct":34.6,"net_income":9609400000.0,"diluted_eps":24.71,"free_cash_flow":11027300000.0,"fcf_margin_pct":33.76,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ASML/ASML_Q3_2026_Earnings_Call_20261014.md）

# Q3 2026 Earnings Call
**ASML Holding N.V.** | Earnings Calls | 2026-10-14

**Operator** (Operator):
Good day, and thank you for standing by. Welcome to the ASML 2026 Third Quarter Financial Results Conference Call on October 14, 2026. [Operator Instructions] Please be advised that today's conference is being recorded. I would now like to hand the conference call over to Mr. Jim Kavanagh. Please go ahead.

**Jim Kavanagh** (Executives):
Thank you, operator. Welcome, everyone. This is Jim Kavanagh, Head of Investor Relations at ASML. Joining me today on the call are ASML's CEO, Christophe Fouquet; and our CFO, Roger Dassen. The subject of today's call is ASML's 2026 third quarter results. The length of the call will be 60 minutes, and questions will be taken in the order that they are received. This call is also being broadcast live over the Internet at www.asml.com. A transcript of management's opening remarks and a replay of the call will be available on our website shortly following the conclusion of this call. 
Before we begin, I would like to caution listeners that comments made by management during this conference call will include forward-looking statements within the meaning of the federal securities laws. These forward-looking statements involve material risks and uncertainties. For a discussion of risk factors, I encourage you to review the safe harbor statement obtained -- contained in today's press release and presentation found on our website at www.asml.com and in ASML's annual report on Form 20-F and other documents as filed with the Securities and Exchange Commission. 
With that, I would like to turn the call over to Christophe Fouquet for a brief introduction.

**Christophe Fouquet** (Executives):
Thank you, Jim. Welcome, everyone, and thank you for joining us for our third quarter 2026 results conference call. Before we begin the Q&A session, Roger and I would like to provide an overview and some commentary on the third quarter 2026 results as well as provide some additional comments on the current business environment and on our future business outlook. Roger?

**R.J.M. Dassen** (Executives):
Thank you, Christophe, and welcome, everyone. I will first review the third quarter 2026 financial accomplishments and then provide guidance on the fourth quarter and the full year of 2026. Let me start with our third quarter accomplishments. Total net sales in the third quarter of 2026 were a record at EUR 11.7 billion, towards the high end of our guidance and reflecting strong execution of our capacity ramp. Net system sales were EUR 8.4 billion, which includes EUR 4.1 billion from EUV system sales, including the sale of 1 High NA EUV system and EUR 4.3 billion from non-EUV system sales.
Net system sales were split between Logic at 54% and Memory at 46%. Installed Base Management sales for the quarter were EUR 3.3 billion, exceeding our guidance by almost EUR 0.4 billion, primarily due to the strong demand for our productivity upgrade products in both EUV and DUV. Gross margin for the quarter was above guidance at 57.5%, primarily due to the contribution of very high-margin components within our Installed Base Management business. Our operating expenses were as guided with R&D expenses at around EUR 1.2 billion and SG&A expenses at around EUR 0.4 billion. The effective tax rate for Q3 was 16.1%. 
For the full year 2026, the expected annualized effective tax rate is around 17%. Net income in Q3 was EUR 5 billion, which includes around EUR 0.5 billion as a result of an increase in the valuation of our initial investment in Mistral AI, representing 42.5% of total net sales and resulting in earnings per share of EUR 12.95.
Turning to the balance sheet. We ended the third quarter with cash, cash equivalents and short-term investments at a level of EUR 12.7 billion. Our free cash flow in Q3 was EUR 11.4 billion, underpinning the strong order momentum of our customers and the related down payments. 
Moving to the cash return to our shareholders. In Q3, ASML paid the first interim dividend over 2026 of EUR 1.88 per ordinary share. Further, we purchased in Q3 around EUR 4.1 billion worth of shares under the current 2026-2028 share buyback program. The second quarterly interim dividend over 2026 will be EUR 1.88 per ordinary share and will be made payable on November 4, 2026. 
With that, I would like to turn to our expectations for the fourth quarter and the full year 2026. We expect Q4 total net sales to be between EUR 14.2 billion and EUR 15.2 billion with a gross margin of around 57%. We expect our Q4 Installed Base Management sales to be around EUR 3.7 billion. The expected R&D expenses for Q4 are around EUR 1.2 billion and SG&A is expected to be around EUR 0.4 billion. 
Regarding our full year expectations, we expect our full year 2026 total net sales to be between EUR 44 billion and EUR 45 billion with a gross margin of around 56%. This anticipated year-over-year total net sales increase of around 36% reflects our expectation of over 45% growth in EUV, around 20% growth in non-EUV-related system sales and around 50% growth in Installed Base Management sales. 
Turning to end use. This year, we expect Logic net system sales to grow around 10% and Memory net system sales to grow around 75%. The growth in Memory is driven by the combination of capacity expansion of our customers and the increasing adoption of EUV on advanced DRAM nodes. As previously mentioned, we continue to expect the China region to account for around 20% of our total net sales this year. 
In summary, the third quarter was a record for both total net sales and gross margin, and we expect our business to continue to accelerate in the fourth quarter as we execute against a backdrop of very strong customer demand for all our products and services. 
With that, I would like to turn the call back over to Christophe.

**Christophe Fouquet** (Executives):
Thank you, Roger. If we take a step back to look at the market environment, we see that the pace of the AI build-out continues to be very robust. Supply shortages across advanced Logic and Memory nodes continue to increase in size and in time horizon. Against this backdrop, we had very constructive discussions with our customers throughout the quarter and the demand signals we have received have continued to strengthen. 
Our leading edge high-volume customers are sharing very good visibility as a result of the increasing number of long-term commitments they are securing with their customers. This extended visibility has led them to conclude that demand for their product will outpace supply through at least 2028. As a result, customers are accelerating capacity build-out plans and preparing for further expansion beyond 2028 in order to better meet the anticipated level of demand. 
For us, their drive to add capacity is translating into not only greater short-term demand across our entire Holistic Lithography portfolio, but also improved longer-term visibility and demand, especially for our EUV products. As customers shift focus to their needs beyond 2027, our order momentum continues to build. We are increasingly receiving orders for 2028 and customers are also expressing interest in placing orders for 2029 and even 2030. 
As our customers are preparing to meet rising demand, we, in turn, continue our focus on adding capacity to support their needs. Roger will now share further details on our latest plans on providing our customers additional capacity. Roger?

**R.J.M. Dassen** (Executives):
Thank you, Christophe. We have been very successful in ramping capacity this year. For Low NA EUV, we anticipate output of roughly 65 systems for 2026, which is nearly 50% more than the 44 systems that we shipped last year. For deep UV immersion systems, while our initial output target for these systems was well below the prior year, we now expect we will deliver a similar quantity in 2026 as we did in 2025. 
Looking further ahead, we shared our intent last quarter to increase our capacity in 2027 by 30% for both Low NA EUV and deep UV immersion systems as well as to investigate adding a further 30% in 2028. However, given the dynamics of this quarter, we now anticipate that our current planned levels of output in '27 and '28 will not fully meet the demand of our customers. Therefore, we continue to strengthen our efforts to produce more systems, especially beyond '27, and with that goal in mind, are now looking into expanding our 2028 capacity even above the 30% year-on-year growth target that was under investigation last quarter for both Low NA EUV and immersion systems.
In addition to shipping new systems, we support customer needs for more wafer capacity through productivity upgrades across our EUV and deep UV installed base as well as with the introduction of new products. The ability to enable an increase in capacity through upgrades on the same footprint is very compelling for our customers as the effect is an immediate increase in output capability. We will continue to work on this important value driver, expanding the upgrade portfolio offering, new productivity options to our customers in the coming years. 
The introduction of new products is the other lever that we have to support increased wafer capacity. We plan to introduce our next-generation Low NA EUV system, the NXE:3800F, starting in small quantities at the beginning of 2027. This system is specified at a throughput of 260 wafers per hour compared to the 230 wafers per hour capability of the NXE:3800E system. We also plan to introduce the next-generation critical deep UV immersion running at 330 wafers per hour. These new products will provide incrementally more wafer capacity to the industry as they ramp in the coming years. 
With that, I will hand it back over to Christophe for a technology update.

**Christophe Fouquet** (Executives):
Thank you, Roger. This quarter, we saw meaningful momentum around High NA EUV with several industry announcements providing evidence of the technology's progress from development towards production. Intel announced that it has exposed more than 1 million wafers using its High NA EUV systems with performance that meets or exceeds comparable layers pattern using Low NA EUV.
Additionally, Samsung and TSMC announced plans to introduce High NA EUV into high-volume manufacturing in 2028 and 2030, respectively. With availability across the existing High NA EUV fleet approaching 90%, we now expect to see adoption increase node on node moving forward. To further ensure chipmakers can fully leverage the advantage of High NA EUV, we also, in collaboration with TSMC, began an industry-wide initiative to develop larger format EUV photomasks. This collaborative effort aims to establish a 12-inch mask pilot line by 2031 and enter production in 2033. 
The broad support for this transition reflects customer interest in maximizing the value of High NA EUV and in investing in the next generation of this technology. In closing, the combination of very strong demand fundamentals, improved visibility and rising litho intensity reinforce our confidence in the trajectory of our business. Our focus continues to be on supporting our customers as they ramp their Logic and Memory nodes by continuing to expand our capacity over a multiyear horizon, while also delivering enhanced productivity by executing our technology road map. 
In Q3, we have also shipped the first YieldStar 550B metrology system. This overlay measurement system is designed with improved accuracy and precision to support the tighter process control requirements of the 14-angstrom node in Logic and the 1D node in DRAM. The system is designed to deliver more than 60% greater productivity over the previous generation YieldStar, allowing customers to measure more wafers and therefore, more quickly drive yield improvement in their processes. This latest generation system continue to support major adoption of YieldStar at customers with a demand that is expected to more than double for the coming years versus 2025.
Finally, the transition of High NA EUV into high-volume manufacturing creates a compelling opportunity for customers to enhance the economics of their future road map, and we remain fully committed to helping them execute a successful insertion. 
With that, we would like -- we will be happy to take your questions.

**Jim Kavanagh** (Executives):
Thank you, Roger, and thank you, Christophe. The operator will instruct you momentarily on the protocol for the Q&A session. Before I would like to ask you to kindly limit yourself to 1 question with 1 short follow-up, if necessary. This will allow us to get through as many callers as possible. Now operator, could we have your final instructions and then the first question, please?

**Operator** (Operator):
[Operator Instructions] And your first question today comes from the line of Joe Quatrochi from Wells Fargo.

**Joseph Quatrochi** (Analysts):
I was wondering if you could provide maybe just a little additional color on the capacity expansion that you need beyond the 30% previously talked about? And just what do you think you can do in 2027 relative to that kind of mid-80s that we talked about last quarter?

**Christophe Fouquet** (Executives):
Well, I think that we are basically working very hard to increase capacity. And I think this is true now, as Roger explained, we have done a lot of that this quarter. That's going to be true next year, and that's going to be true in 2028. And the reason for that, as we explained, is we continue to see customers asking for more tools. Now if we look at some of the opportunity we see, of course, it's a bit easier for us to enable those opportunities later, so mostly in 2028 rather than on the shorter term. So this is what we are focusing on. I won't give new numbers for '27 or '28 because it's far too early to give those numbers as we continue to basically do everything we can to get extra capacity.

**Joseph Quatrochi** (Analysts):
And then as a follow-up, you talked about in the prepared remarks or in the transcript, value-based pricing impacting more 2027, 2028. Can you share any just a few more additional details on that, how to think about just kind of the trajectory of gross margin from here?

**R.J.M. Dassen** (Executives):
Yes. So those are 2 questions, right? So first, on the pricing. As we mentioned in July, we -- at that point, we were entering into conversations with customers on price increases. Those conversations have been completed and have indeed led to pricing increase for what we call the most critical products for our customers. So that has been done. We also -- and you made reference to it, as we said in the prepared remarks, this is not going to have an impact on '26. You will see some impact on '27, but I would say that the full impact of that is really going to start in '28. So from '28 onwards, you're going to see a sustained impact of that, but you will see -- in the course of '27, you will see that starting to manifest itself in a positive way in both our revenue and the ASPs and in the gross margin. 
Your second question on gross margin is obviously a much broader question, but let me take that one then. So what are the puts and takes on the gross margin? So as you have seen, gross margin this quarter, very, very strong and stronger than we anticipated, I would say, primarily as a result of the EUR 400 million more upgrade business that we have. But we should also not forget that if you look at the total year at 56%, it's not just the upgrade business, right? It's also higher volume. It's also the fact that we had a very strong Low NA EUV business in there, very strong immersion business in there. So those are all things that help. 
And then obviously, the question is how will that develop into the years beyond this year, right? So what's the implication for '27 and beyond. And of course, we're not going to give you a gross margin percentage for '27, that will come in January of 2027. But if you look at the key drivers of the gross margin this year, you have to ask yourself how much of that can be sustained into 2027. So first off, volume with everything that Christophe just told you on the 30% increase in 2027, of course, volume should help, right? And volume, as long as we're able to control the cost of the increase in capacity, volume should give you better fixed cost coverage. So that should be a positive in that regard. 
The second element is mix. And there, too, again, key drivers of the volume are the 30% extra in immersion and Low NA EUV. Both of them are obviously very positive from a gross margin perspective. Of course, there will be quite some dry business that we continue to increase this year, but also next year. But I would say that also mix with the strength in EUV demand and immersion demand, that should help. Then to your point, we have the price increase, which, as I mentioned, will have some effect in '27, the larger effect you will see in '28, but it will have some effect in '27. So that's going to be helpful. 
And then finally, in the positive sense, I would probably call out the mix effect within the EUV, right, where the mix effect next year is going to be better than this year because this year, we still have quite some D models in the mix. That won't materially be the case anymore next year. And we will have a few Fs in there as well. So that's going to be helpful in the total EUV mix. So those are key elements. And then what are the things that we need to watch out for? Well, one, as I mentioned, is the ramp cost, right? So how much cost are we incurring to ramp not just for '27, but also for beyond? So that's one thing that we simply need to manage those costs well.
And then there is the swing factor of the upgrades, right? Because as we mentioned, the upgrades are very, very strong this year. So that really begs the question, how sustainable is the upgrade business? And if you look into that, the sustainability of the upgrade business, there's a few elements to bear in mind there. First off, we still see as of today that there is quite some addressable market for us on the upgrade business. So if you look at the upgrade -- the number of upgrades that we have performed in the field, it's quite a few tools, but there are still quite a few tools out there that have not yet been upgraded. So that gives you good potential for the coming quarter, but also for the year thereafter. 
Second, as we mentioned on the video, we're also aggressively pushing upgrade products. So we will bring new upgrade products to the market. And of course, that will open an entirely new addressable market for us in the installed base. So that's helpful. And then, of course, there is a question how will the market continue? In the current market environment, with the demand that is out there, as we just said, there is a lot of appetite for these upgrades. So I would say upgrades is an important swing factor for us in the gross margin development as we see in '27 and beyond, very strong this year. But I think we're, at least from our side, doing whatever we can to create as much opportunity for upgrade business on a go-forward basis as we can.

**Operator** (Operator):
Your next question today comes from the line of Krish Sankar from TD Cowen.

**Sreekrishnan Sankarnarayanan** (Analysts):
Christophe or Roger, my first one, I understand you don't want to give exact capacity numbers. I'm just wondering, under the strong demand environment, is there a natural ceiling on your EUV output either due to space at BIC or Carl Zeiss capacity? Or in other words, if the demand is there, can you do 140 or 150 units in 2028? And along the same line, do you worry that customers are pulling in orders or giving you bigger forecast just to secure a slot? I have a quick follow-up after that.

**Christophe Fouquet** (Executives):
Yes. So maybe let me try to answer both questions. So first on maybe what we are doing to increase the capacity. So I think I mentioned that before, this is a task really started several months ago. And I think there are really 3 elements to it. The first one is to optimize the footprint we have here in order to basically build our machines. We have, as you know, a pretty important footprint, and we started to make sure that most of that footprint can be used for output. And that's true for Low NA EUV. That's also true, by the way, for DUV, including immersion. And this creates already some opportunity that we can use and build up again this year, next year and in 2028. 
The second one, which I think is a very big opportunity and still a major parameter is the cycle time, meaning the time we spend in our factory with a certain given machine. And as we gain in maturity, for example, on the NXE:3800E, we are capable to shorten the cycle time for a certain given sequence, but we are also capable to further optimize the sequence, meaning there are things that we needed to do initially in order to qualify a tool, which over time, in agreement with our customer, we believe we don't have to do anymore. And I would say that this approach, we can take pretty far moving forward. And this is one of the really key opportunities we see basically moving forward.
And as I mentioned before, as we go over time, the opportunities continue to materialize, which give us some more hope and opportunity. On the supply chain, of course, I mean, indirectly, your question is or your remark is that we have to supply the supply chain. This is something that we take into account, starting with Zeiss. So we do not see Zeiss today as a bottleneck for the capacity expansion we are discussing even beyond the 30% we mentioned for 2028. And we have done in the recent years, many, many work with all the supply chain to make sure that the supply chain will not be an issue for us. 
So we continue, of course, to watch that very carefully. You understand that every time you add capacity, of course, we create more challenges there. So we do that. And the last thing I will say is that we have time. I mean if you look at the progress we have done this year, I think they are very significant. We are feeling pretty good about next year. And the time we have, again, for next year, for 2028 is still significant for us to continue to be very creative on all those fronts. So that's, I will say, the first -- the answer to your first question. 
On the second one, I think I mentioned in the introduction, we have very good conversations with our customers. And the conversation is not only about how many tools they need. It's also about exactly when those tools will be hitting the ground in their factories. And when it comes to the demand we are referring to, the increased demand we are referring to, I think we are very much capable to validate that demand with some more detailed plans our customers are sharing with us in terms of fab construction, release, et cetera, et cetera. So I think that we -- when we talk about demand, when we refer to demand in those discussions, we really refer to demand we believe is real and not inflated by any potential buying behavior from our customers.

**Sreekrishnan Sankarnarayanan** (Analysts):
Got you. That's super helpful, Christophe. And then a quick follow-up for Roger. On the value pricing, is this across the board? Is it for systems, services, spare parts, everything? And I'm guessing based on your commentary, you're not repricing the backlog. Can you just clarify that?

**R.J.M. Dassen** (Executives):
Yes. Exactly how we do it, Krish, I'm not going to share. But as I mentioned, we are increasing prices for what we call the most critical products, those products that bring most value to our customers. So these are the high-range, high-volume manufacturing products. Those are the ones that provide most value to customers in the current environment, and those are the ones that we put the pricing increases on it. And you will also understand that upgrade prices are closely associated with the prices of the tools. So that's -- they will also follow -- upgrade prices will also follow this pattern. That's how we do it and exactly how we do it, when we do it, et cetera, I don't want to go into any detail. But the bottom line is that you will start to see the effect on that in the course of 2027, but the full effect you will start to see from '28 and onwards.

**Operator** (Operator):
Your next question today comes from the line of Sandeep Deshpande from JPMorgan.

**Sandeep Deshpande** (Analysts):
My question is back again to the question of your indication that you are looking at adding more capacity than the 30% into 2028. There are multiple components that you need to be able to add capacity and some of these suppliers of ASML will need to add physical capacity to be able to supply you with this kind of huge volume increases given that there's already a 30% increase in 2027. Have these discussions started with customers? Does ASML need to make any substantial payments to these suppliers in terms of adding this capacity? And are there any particular impediments? And given that you yourself do not have any additional physical capacity until 2029, how is this whole supply chain being managed to be able to produce more capacity in 2028? And I have a quick follow-up after that.

**Christophe Fouquet** (Executives):
So I will try to add a bit to what I said before. I think that the only real challenge we have with the supply chain is to make sure they can ramp. I think that there is not question on their side on the, say, the strength of the demand, on the strength of the ramp. I think that the main challenge with all our suppliers, because in this case, with all the suppliers is make sure that they can go up 30% every year. 
Now Roger mentioned it before in the introduction, we went up this year by 50% on EUV, which is the sign basically that these are the kind of things we are capable to do with the suppliers. And as you can imagine, that's a discussion that we have with them on a very regular basis. And us mentioning 30% growth in '27, more than 30% growth in '28 is the result of the confidence we have that this entire supply chain can, of course, follow our own demand, both on EUV and deep UV. That exercise, I will say, of course, could be expanded as far as needed because we are continuing also to add, I will say, suppliers. So we are continuing to make sure also that we have more and more people who can produce some of our parts, especially the noncritical one. And when it comes to the very critical one, Zeiss comes to mind again, we are absolutely strategically aligned on the trajectory of the industry and therefore, the trajectory of the demand. So these are very, very detailed intense discussion. But again, every number we share with you is the result of us having validated that the supply chain can, of course, follow those numbers.

**Sandeep Deshpande** (Analysts):
Quickly, Roger, on the gross margin, your guidance on gross margin in the fourth quarter is down from the current quarter, even though your revenues are going up significantly. And then, I mean, just again, regarding the response you made earlier about the value-based pricing, should we assume that most of the value-based pricing-related increases will go straight down to the gross margin line? Or is there a margin number on the increases that you will be putting through?

**R.J.M. Dassen** (Executives):
So on the first one, the gross margin in Q4, a little bit lower from Q3. That is primarily related to the fact that we are seeing some ramp costs, right? So we're ramping up for the increases that Christophe was just talking about. That has a bit of a bearing on the gross margin expectation. And that's why the fixed cost coverage that you would expect to benefit from the higher volume is a little bit compensated and a bit more compensated by the extra cost that we incur in the ramp as we see it now in Q4. So that's the main reason that we have there. 
In terms of the price increase and to what extent is the price increase completely accretive to the gross margin, of course, there, the same applies, right? I mean one of the arguments that we had also in our conversations with our customers is that we are incurring costs in order to ramp, right? So ramp costs will give you some additional costs. So it will definitely be accretive to the gross margin. But again, you will see some ramp costs that we are incurring in 2027 in order to get to the elevated number that Christophe was just talking about. And this is both for ourselves, but also into the supply chain for the reasons that Sandeep, you just mentioned, right? We need to make sure that the supply chain is completely attuned to what we're looking for. And of course, that also means that in some places, there is some help needed to get that done. So there is some portion of the increase -- of the price increase that we need to cover for the extraordinary ramp that we're going through. But I would say that still a significant part of it is directly accretive to the gross margin.

**Operator** (Operator):
Our next question today comes from the line of Francois Bouvignies from UBS.

**Francois-Xavier Bouvignies** (Analysts):
So I just wanted to follow up a bit on this shortage situation. Obviously, we are in a very unprecedented time with this capacity constraint for your customers. But also today, you are claiming that on your side as well, the demand will be higher than supply. So I mean, the behavior usually is that people order as much as they can, especially if you start seeing some ramp to make sure they have the tools. 
And we see in other industries, some long-term agreements, some prepayment, try to get a more true sense of the demand. I was wondering if you were considering any change of the way you want to contract with your customers in those times, for example, increasing the prepayments or also adding like more the firm orders earlier to make sure you know that your customers are committed.

**R.J.M. Dassen** (Executives):
Yes, Francois. So if we take that, and we said it before, if you put an order with ASML, that's not a frivolous piece of paper that you put your name under. It comes with 2 serious commitments. One serious commitment is a commitment to make a down payment. And as I qualified it before, it's a down payment that is enough to hurt, right? So that's one element. And secondly, a PO is a real commitment on both sides of the equation. And it also means that it's -- if you want to get rid of that commitment, that's not going to be easy, right? It's -- that comes at a price, not just the down payment, but more than that. So therefore, before customers sign a PO with ASML, they've made up their mind and they're not doing this frivolously. 
In terms of will you accept orders early on? Well, as Christophe mentioned, we are getting the request of customers to accept -- for us to accept their orders, their POs already for 2029 and 2030. And the only reason why Christophe worded it in that way that customers are requesting us, and therefore, we have not yet accepted those is that we want to make sure that we have a good picture of what the overall demand in '29 and 2030 looks like that customers are currently signaling and mirror that against the capacity expansion as we see it at that point in time.
And we want to do that because we don't want now to accept orders from customer A, B and C and then to tell customer D who hasn't given orders yet for '29 and 2030, sorry, we're sold out. I mean that would be totally inappropriate for customers that have been business partners for us for a very long period of time. So we're now really using this period of time to mirror, to get a good understanding what is the total demand that our customers are signaling for the '29, 2030 time frame. What does that look like? What is for us a reasonable expectation of capacity as we see it in the '29, 2030 time frame. And once we have that picture ready, then we are ready to accept orders and also accept the commitment from our side to execute on those orders. 
So we -- the only hesitation we have at this stage is that we really want to do our homework, be very diligent on the acceptance of the orders that customers are offering us to make sure that no single customer feels left out.

**Francois-Xavier Bouvignies** (Analysts):
Very good answer, detailed. The second one is on the High NA news flow. I mean, Christophe, you mentioned this high-volume manufacturing in '28 with the Memory guys and also TSMC in 2030. And if I look at the past Low NA when we started this high-volume manufacturing, I mean, we saw a significant step-up in shipments during those years. So I was wondering if we should think about High NA shipments in '28 to increase significantly on the back of it and potentially a double-digit number of High NA shipments to -- as we go forward?

**Christophe Fouquet** (Executives):
Well, I think it's -- we're still looking at the very initial ramps. I think that you are going indeed to see that every year, our customers are going to need more tools as they validate in manufacturing that they like High NA and that most probably they plan over time more layers. I think the announcement and the drive of TSMC first on the 12-inch reticle is very interesting there because the first signal it gives is that in the mind of the customer, there will be more and more use of High NA. Because if it was not the case, I mean, no one will really bother to go to 12-inch mask on High NA. So the 12-inch mask drive and very wide adoption by customer in the consortium is just a sign that anyone has in mind over time to develop basically more and more adoption of High NA. 
So with that, it's always difficult to say exactly how this will basically manifest itself. We also have, of course, a very big ramp. So there's a lot of focus on building up capacity, which sometimes can have a positive or negative impact on the High NA rollout, depending if customers see High NA as additional capacity or potentially a bit of a slowdown. But the number will grow for sure year after year. And again, the message, I think all our customers have given this quarter with their participation into the 12-inch consortium is that they believe, over time, this will become a very important technology and the number of layers will grow over time for sure.

**Operator** (Operator):
Your next question today comes from the line of Lee Simpson from Morgan Stanley.

**Lee Simpson** (Analysts):
Maybe just a follow-up to the last answer set. I thought it was quite interesting that if you look at the noncurrent liabilities, there's quite a material jump Q-on-Q. We're of the order of about EUR 5 billion. And typically, the bulk of that is down payment. So can we make a read-through to a relative size of big order intake in Q3? That's question number one. And I think maybe alongside that, it did seem to infer, Christophe, in your answer to last question that it's perhaps new customers that are bringing you to sort of thinking about the '29 and '30 sort of framework. And as you say, you still want to keep your marginal buyers still in the mix here. Are we right in saying that most of this is coming from new customers as a result?

**R.J.M. Dassen** (Executives):
Yes. So on the first one, the noncurrent liabilities, does that include down payments? Yes, it does, right? So in that way, it is an interesting gauge of how order intake is developing. I should say it's a bit of a lagging indicator because typically, the down payment and the receipt of the money lags a little bit the actual signing of the PO. So it is a bit of a lagging indicator. But for lack of any PO numbers that you get from ASML, it's a nice proxy. Yes.

**Christophe Fouquet** (Executives):
Yes. I'm not sure I've fully understood the second question. So...

**R.J.M. Dassen** (Executives):
I think the second question, I think, was on the customers in '29, '30 that expressed an interest to do that. I think your question is, Lee, is that a totally new customer that might potentially start with a T. And might this be that this customer is in that way, sort of locking out existing customers?

**Christophe Fouquet** (Executives):
You put it better than I would.

**R.J.M. Dassen** (Executives):
And I guess the answer is that the interest that is being expressed is much broader. Much broader. This is not linked to one specific customer. There is a far broader interest in customers to have -- to place POs for that time period.

**Christophe Fouquet** (Executives):
Yes. And maybe to add to that because you mentioned a new customer indirectly. I think what's interesting on Low NA EUV, we've talked about increased adoption of EUV. We continue to see, in fact, new customer on Low NA EUV, especially when it comes to DRAM. And I would say this goes a bit beyond the T customers. So that's another interesting dynamic that we have to indeed take into account for 2028, '29, 2030. That's another, of course, challenge when it comes to the capacity discussion we're having. But I think it's a great news when it comes to the validation of how EUV will be used moving forward. And the last thing I will say is that we see a similar trend on High NA. So that's, I think, also a very good set of news we get from our potentially new customers.

**Operator** (Operator):
Our next question today comes from the line of Alexander Duval from Goldman Sachs.

**Alexander Duval** (Analysts):
Just wanted to pivot a bit and talk about immersion DUV. You talked today about how you'll reach a throughput of 330 wafers per hour. So I wondered what that could directionally mean for pricing in '28 and whether we should be thinking about the kind of ASP step-ups we saw historically on EUV tools when we think about the innovation you're delivering on immersion. And then I would like to think also secondarily as a follow-up on Logic versus Memory. I wondered if it's fair to say that in the prior quarter, the incremental demand seemed to be very much related to Memory. But now you seem to be seeing quite a strong balance across both Logic and Memory. So curious to what extent you'd agree with that statement and what is driving this, whether it might be across drivers like Agentic AI or it could be progress either with existing customers or new customers?

**Christophe Fouquet** (Executives):
Yes, I can start. So I appreciate the question on the 330 wafers per hour because this is one of the I would say, the very short-term action we have taken to increase capacity. We're going to bring the different immersion product to 330 wafers per hour. You know that we have a slightly different version of our immersion tool depending on the overlay requirement of our customer. But all of them at the beginning of next year will go to 330 wafers per hour. 
And when it comes to value and therefore, to pricing, as we discussed many times for EUV, the price, the value scale basically with the throughput. And I think what's true for EUV will be true also for deep UV. So this is both an opportunity on value, margin, pricing. It's also, of course, very helpful when it comes to capacity because you look at, of course, providing the same capacity with potentially less tool. It doesn't mean that we need less tool. It means that we get more capacity for our customers, of course. So that's another, I would say, creative move we have made on our portfolio to get more capacity out. And we expect, again, the value to come to us in the same way it has always come with productivity. That's for deep UV. 
On the second question, I think that Roger gave some number. If you look at the increase compared to last year, Memory has gone up very much. We're still on a trend where Memory become more and more important, 75% increase, which is, of course, significant. So you start to see the results of this huge Memory investment that, by the way, is mostly DRAM to be clear. And we continue to see that moving forward. And I think we have said in the past that the ratio between Logic and Memory will most probably increase towards Memory. Still, I will say that Logic is also very strong. So to be able to predict exactly where this is going to land is difficult because I'd like to stress that we see also a very strong demand on the Logic side because, of course, as you know, the 2 are very much coupled when it comes to delivering AI capacity to the market.

**R.J.M. Dassen** (Executives):
Yes. And just to give you one more data point there. So indeed, as I mentioned, Logic went up 10%, around 10%. But the advanced Logic piece included in there is far bigger, right? So that grew over 25%, is expected to grow over 25% in this year. So you're right, Memory is getting closer to Logic, but Logic remains very, very important. And when we look at 2027, Memory comes close, but I still believe that Logic will outweigh Memory in the total book of business for next year.

**Operator** (Operator):
The next question today comes from the line of Chris Caso from Wolfe Research.

**Christopher Caso** (Analysts):
My question is with regard to your customer clean room constraints. And perhaps you could discuss that with respect to your decisions to expand capacity into '28. Do you expect that clean room is still a constraint on your customers' ability to add tools and add capacity? And then what does that mean as you go into potentially 2029?

**Christophe Fouquet** (Executives):
Well, I think there's still some, what I would call, tactical constraints that one system will move from the end of a quarter to the beginning of another one. We don't see too much of that, to be honest, but that's still possible because our customers have been ramping their clean room facility extremely fast. If we look at the longer term, as I said before, beyond those little move or those tactical moves, we have confirmed that the numbers our customers are giving us are really lined up with their plans. In fact, in many cases, when the supply is tight, we make sure before we fully allocate a tool to a customer that the space will be there. The facility also will be there so that we don't ship a tool that will be waiting for weeks for a customer to use it because, of course, other customers will be very disappointed with that. So we do a lot of work to make sure that in all the plans we have at ASML, we don't have a delay of more than a few days or weeks, I will say, in shipping our products. So short answer is, I think, no. We don't see our customer clean room constraint being a major factor on our demand.

**R.J.M. Dassen** (Executives):
But to your point, Christophe, it's very clear that with everything that is being built today, it is such a massive scale. So on the one hand, that opens significant opportunities. But it also means that our customers have to manage the execution of all that construction in '27, '28 very diligently, right? So they're looking at a huge expansion of their footprint. But of course, that requires very diligent execution. And that's obviously something that we need to monitor very, very carefully. So in that way, conceptually, a lot of opportunity and not a constraint. But in reality, we need to make sure that they execute well such that it doesn't become a constraint.

**Christopher Caso** (Analysts):
As a follow-up question is with regard to China, and you talked about that at 20% of your systems revenue this year. What should we expect going forward with respect to China? Do you expect it to maintain those levels as you go into next year?

**R.J.M. Dassen** (Executives):
I think the intrinsic demand in China is strong, right? If you look at what China needs in terms of mainstream Logic, in terms of Memory, there is very strong demand in China for their domestic consumption. If you look at the fabs that are being built in China, that is -- there is a lot coming online there. And therefore, we would expect the demand in China to be strong. This year, 20%. And I would argue that also for 2027 and beyond based on the intrinsic drivers, it seems that the demand situation in China remains very strong.

**Operator** (Operator):
Our next question today comes from the line of Tammy Qiu from Berenberg.

**Tammy Qiu** (Analysts):
So firstly, it's on your value-based pricing. So this year, you are increasing pricing. Going forward, let's say, this tightness in the industry continues, do you think you'll be able to negotiate price increase every single year?

**R.J.M. Dassen** (Executives):
Well, Tammy, that wasn't the plan, to be honest.

**Christophe Fouquet** (Executives):
We were smiling.

**R.J.M. Dassen** (Executives):
We were smiling.

**Christophe Fouquet** (Executives):
Customers are listening.

**R.J.M. Dassen** (Executives):
Yes, exactly. That wasn't the plan. So we've had these conversations with customers that given everything that the ecosystem is going through and given the efforts that we're all going through to meet the ramp requirements, we thought that we were entitled to a higher percentage, and we were able to get there with customers, and we would see that as something that is possible within our value-based pricing model, but we would not be looking at repeating this every year or so. That is not the plan.

**Christophe Fouquet** (Executives):
I would add to, Roger, it's still -- I think mostly, this is mostly one of the very first times we have this discussion with customers. If you go back many, many years back, this is something we never did. And Roger mentioned in the introduction, the construction -- the discussions were constructive. I think they were more than constructive, meaning there was a clear acceptance that maybe the overall value in the ecosystem is shifting. And that's triggered by, of course, AI to some extent. And I would say we will see what the future brings, but at least we have been able to have a very good, very mature discussion, which I think is very important. So something we never did before. We don't want to do that every year because that's not the purpose. But I think that it's very good that in principle, at least we have the ability mostly once a while to discuss again what's the real value of lithography in the entire ecosystem.

**R.J.M. Dassen** (Executives):
Absolutely. And Tammy, as you know, one of the key objectives for us in the pricing conversation is to make sure that we never depart from the concept of value-based pricing because we don't want to be in a position that if the market goes down, that we're actually having discussions with customers on price decreases. I mean -- and that is very well understood in the conversations with our customers as we've had it. So to Christophe's point, these have been conversations on fairness. 
But the premise that we are able to capture value of the next generation of tools. And that as a result of that, we're able to continue to increase the pricing commensurate with the value that it brings. That is a principle that we want to sustain even if the market goes backward a bit. So that's the reason why we're not opportunistically pricing, why we're not opportunistically seizing the opportunity and why we're executing along the lines of what Christophe just described.

**Tammy Qiu** (Analysts):
Okay. That's really clear. And secondly, regarding your exposure in China. So I understand that China will never be able to compete with you from a technology perspective. But going to, let's say, 2029-ish, when you work out, let's say, a low-end version of immersion tool, do you think that will decrease your potential to price at a premium versus the Chinese local players or your potential margin in Chinese market may need to come lower?

**Christophe Fouquet** (Executives):
Well, I think there's a lot of, of course, speculation in the question. But where we are today, I think, with our Chinese customers is that they all want to work with us. I think this is very clear. I won't give any market share number, but you can imagine it's extremely high, especially on immersion. And therefore, as long as we have a good market access, as long as our customer can trust they can work with us, I think that the likelihood of a major competition in China is still pretty low. That's the first thing I will say. 
The second is, of course, if they were to not have access to some of our tools, then you get a lot more motivation. But it's still a very, very long way to go. And I think that we have been having this discussion about China having a tool to compete with us for the last 25 years. And every other year, we get the news that this is coming. If you stick to fact, I think the facts this year are not different from the fact a year ago or even 5 years ago. So I think that the progress is not very strong. The motivation is not strong at all. And I think that as long -- again, as we preserve market access in reasonable means, we should be fine.

**Jim Kavanagh** (Executives):
Okay. I just wanted to remind we've got time for one last question. So Sharon, can I ask you to ask the final question, please? And then if there are follow-on questions, please contact ASML Investor Relations, and we'll do our best to follow up. So operator, can we have that last question, please?

**Operator** (Operator):
Your final question today comes from the line of Stephane from ODDO BHF.

**Stephane Houri** (Analysts):
Actually, my question was on China initially. But just to understand the discussions that you have on 2029 and 2030, if it is more -- because you seem to be very positive at the moment on Memory, if it's very balanced between Memory and Logic or if it's still Memory manufacturers who are giving you some visibility on 2028 -- 2029, sorry, and 2030?

**Christophe Fouquet** (Executives):
Well, I think you need both Memory and Logic to get from AI chips. I think we have a big discussion with both customers because they get the same message from their own customers. I think today, DRAM is a bit more aggressive on the buildup of those capacities. But yes, we have discussions with both. So I think we see equal interest, equal, I would say, demand trajectory for both DRAM and Logic because we need both basically to get the products out.

**Stephane Houri** (Analysts):
And DRAM, is it at the same time, the U.S., Korea and even China? Or is it more concentrated from a geographic standpoint?

**Christophe Fouquet** (Executives):
No, I think that we're mostly talking about EUV in this case. So this excludes China.

**Jim Kavanagh** (Executives):
Okay. Thank you, everyone. On behalf of ASML, I'd like to thank you for joining the call today. Operator, if you could formally conclude the call, that would be very much appreciated. Thank you.

**Operator** (Operator):
Thank you. This concludes the ASML 2026 Third Quarter Financial Results Conference Call. Thank you for participating. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ASML_Q2_2026_Earnings_Call_20260715.md
- 2026-07-15｜CFO｜guidance：Q2 總淨銷售 93 億歐元，高於財測上緣，因安裝基礎管理銷售高於預期（原話："billion, which is above the high end of our guidance"）
- 2026-07-15｜CFO｜margin：Q2 毛利率 54%，高於財測（原話："Gross margin for the quarter was above our guidance at 54%,"）
- 2026-07-15｜CFO｜margin：Q2 營業費用高於財測，原因為技術與 IT 轉型的估計成本認列（主要在 R&D）（原話："were higher than guided due to the recognition"）
- 2026-07-15｜CFO｜margin：Q2 EUV 系統銷售 38 億歐元（原話："which included EUR 3.8 billion from EUV system sales,"）
- 2026-07-15｜CFO｜customer：Q2 系統銷售邏輯 51%、記憶體 49%（原話："almost equally split between logic at 51% and memory at 49%."）
- 2026-07-15｜CFO｜margin：Q2 安裝基礎管理銷售 28 億歐元，比財測高近 3 億，主要來自升級業務（原話："almost EUR 300 million above our guidance"）
- 2026-07-15｜CFO｜capital_allocation：Q2 自由現金流 13 億歐元（原話："Our free cash flow in Q2 was EUR 1.3 billion."）
- 2026-07-15｜CFO｜capital_allocation：Q2 依 2026–2028 庫藏股計畫買回約 11 億歐元（原話："billion worth of shares under the current 2026-2028 share"）
- 2026-07-15｜CFO｜capital_allocation：2026 首季中期股息每股 1.88 歐元（原話："interim dividend over 2026 will be EUR 1.88 per ordinary"）
- 2026-07-15｜CFO｜guidance：全年有效稅率預期約 17%（原話："expect that annualized effective tax rate is around 17%."）
- 2026-07-15｜CFO｜guidance：Q3 毛利率財測 55%–57%（原話："Gross margin for Q3 is expected to be between 55% and 57%."）
- 2026-07-15｜CFO｜guidance：Q3 R&D 費用預期約 12 億歐元（原話："The expected R&D expenses for Q3 are around EUR 1.2 billion"）
- 2026-07-15｜CFO｜guidance：上調 2026 全年財測（原話："Driven by continued strong demand, we are updating our full"）
- 2026-07-15｜CFO｜guidance：全年淨銷售 430–450 億歐元、毛利率 54%–56%（原話："total net sales between EUR 43 billion and EUR 45 billion"）
- 2026-07-15｜CEO｜customer：多家客戶上調資本支出計畫（原話："A number of our customers have revised their capital"）
- 2026-07-15｜CEO｜customer：邏輯與 DRAM 客戶皆與其客戶簽長期協議，提供能見度（原話："Our customers in both segments are entering into long-term"）
- 2026-07-15｜CEO｜product：邏輯端微影強度上升（原話："driving both an increase in litho intensity and greater"）
- 2026-07-15｜CEO｜guidance：先進邏輯／晶圓代工相關系統銷售今年成長逾 25%（原話："now expect advanced logic/foundry-related net system sales"）
- 2026-07-15｜CEO｜guidance：記憶體相關系統銷售今年成長逾 75%（原話："to grow by over 75% this year."）
- 2026-07-15｜CEO｜customer：DRAM 量、HBM 與 1c／1b 節點 EUV 層數增加並存，CEO 稱 DRAM 對 ASML 是「perfect storm」（原話："creates a bit the perfect storm for ASML on DRAM"）
- 2026-07-15｜CFO｜guidance：今年預計出貨約 65 台 Low-NA EUV（原話："We now expect to ship around 65 Low-NA"）
- 2026-07-15｜CFO｜guidance：EUV 系統銷售年增逾 45%（原話："year-over-year EUV net system sales growth of over 45%."）
- 2026-07-15｜CFO｜guidance：浸潤式 DUV 今年約 130 台（原話："For immersion deep UV, we expect about 130 shipments"）
- 2026-07-15｜CFO｜guidance：非 EUV 系統銷售預期成長約 25%（原話："we expect growth in non-EUV net system sales of around 25%"）
- 2026-07-15｜CFO｜guidance：安裝基礎管理銷售今年成長逾 30%（原話："Management sales are expected to grow over 30% this year"）
- 2026-07-15｜CFO｜guidance：中國占全年淨銷售仍約 20%（原話："We continue to expect this to make up around 20%"）
- 2026-07-15｜CFO｜commitment：2027 年 Low-NA EUV 訂單接近全額覆蓋（原話："close to being fully covered with orders for Low-NA EUV"）
- 2026-07-15｜CFO｜commitment：計畫 2027 年 Low-NA EUV 產能增加約 30%（原話："increase our Low-NA EUV capacity by around 30%."）
- 2026-07-15｜CFO｜guidance：2028 年已收到大量 Low-NA EUV 訂單（原話："significant number of Low-NA EUV orders."）
- 2026-07-15｜CFO｜guidance：正在研究 2028 年再增 30% 產能（尚為「investigate」）（原話："investigate a further 30% capacity increase for that year."）
- 2026-07-15｜CFO｜commitment：浸潤式系統 2027 年產能增 30%（原話："intend to increase capacity by 30% in 2027"）
- 2026-07-15｜CEO｜product：Intel Foundry 在 Intel 18A 以 High-NA EUV 生產部分 Core Ultra Series 3（原話："to produce a subset of its Intel Core Ultra Series 3"）
- 2026-07-15｜CEO｜product：High-NA 平台成熟度持續改善（原話："improving towards the level required for insertion"）
- 2026-07-15｜CFO｜guidance：2026 年 High-NA 認列維持 4 至 5 台（原話："Yes, 4 to 5 is still our view for this year."）
- 2026-07-15｜CEO｜commitment：下次資本市場日訂於 2027 年 6 月 10 日更新長期展望（原話："Capital Markets Day, which will be held on June 10, 2027"）
- 2026-07-15｜CEO｜competition：CEO 稱 High-NA 要勝過 Low-NA 加浸潤多重曝光的成本，關鍵在平台成熟度（原話："to beat the cost of Low-NA plus immersion multi-patterning"）
- 2026-07-15｜CEO｜product：CEO 認為不需要比較兩種機台價格（原話："there is no real need to maybe look at one tool price"）
- 2026-07-15｜CFO｜guidance：CFO 同意當前環境給定價更大彈性（原話："to beat the cost of Low-NA plus immersion multi"）
- 2026-07-15｜CFO｜guidance：CFO 稱已在執行定價，但受長交期影響不會立即反映（原話："And of course, we're executing on that as well."）
- 2026-07-15｜CFO｜guidance：CFO 稱可望取得更大價值份額，帶來更好定價能力（原話："gives you better pricing power."）
- 2026-07-15｜CFO｜commitment：與客戶討論如何就額外價值獲得回報（原話："conversations with customers on how we get rewarded"）
- 2026-07-15｜CEO｜commitment：產能擴充皆基於現有廠房（原話："there is no real need to maybe look at one tool"）
- 2026-07-15｜CFO｜guidance：CFO 稱 2027 約 85 台為目前供需平衡點（原話："we think the 85 is a nice representation of"）
- 2026-07-15｜CFO｜margin：CFO 說明 2027 年 EUV 機台組合 E／F，晶圓產能增幅約 45% 而非 30%（原話："not 30% improvement of wafer capacity that we're adding, but"）
- 2026-07-15｜CFO｜product：D 型機台今年售完，2027 年改出 E、F（原話："we're simply sold out when it comes to D models"）
- 2026-07-15｜CFO｜margin：CFO 稱明年 E、F 組合有較佳 ASP（原話："that mix will come with a better ASP than the mix"）
- 2026-07-15｜CFO｜margin：CFO 拆解下半年毛利率：浸潤式出貨大增（原話："not 30% improvement of wafer capacity that we're"）
- 2026-07-15｜CFO｜margin：CFO 以財測中點推算下半年毛利率約 56%（原話："second half at a gross margin of 56% approximately"）
- 2026-07-15｜CFO｜risk：2025 年曾請 ZEISS 準備較低的浸潤式數量，致上半年偏弱（原話："ZEISS prep for a substantially lower immersion number"）
- 2026-07-15｜CEO｜risk：CEO 稱 2027、2028 需求尚未進入穩定狀態（原話："a stable state on what the demand will be for '27"）
- 2026-07-15｜CFO｜guidance：CFO 稱 2028 產能研究先於客戶正式下單（原話："So we're not waiting. We're preempting."）
- 2026-07-15｜CEO｜customer：升級需求強勁，客戶要求加速並開發新升級產品（2027、2028）（原話："So this creates really strong condition for system upgrade."）
- 2026-07-15｜CEO｜product：E 與 F：客戶兩者都要；F 將用於 1.4nm（原話："the F will certainly be used for 1.4-nanometer"）
- 2026-07-15｜CEO｜product：DRAM 與邏輯客戶同時驗證 High-NA（原話："are qualifying equally High-NA today."）
- 2026-07-15｜CFO｜commitment：CFO 稱 R&D 與 SG&A 持續控管，營運槓桿未來會更好（原話："I think all the capacity increases, either planned or"）
- 2026-07-15｜CFO｜capital_allocation：預計今年動工新園區，但屬 2028 年之後（原話："We expect to break ground this year on a new campus"）

### 問答異常語氣（迴避／改口／保留）
- ASML_Q2_2026_Earnings_Call_20260715.md｜問：Bouvignies（UBS）問 Low-NA 是否有調價空間、何時反映｜答法：CEO 先轉談 High-NA 成熟度；CFO 承認有彈性但不給時間表，只說視訂單與交期而定
- ASML_Q2_2026_Earnings_Call_20260715.md｜問：Houri（ODDO）問 2028 年 110 台已覆蓋多少｜答法：CFO 稱不提供訂單或覆蓋率數字，改談客戶訊號強
- ASML_Q2_2026_Earnings_Call_20260715.md｜問：Houri 問 75% 記憶體成長中 HBM 與量的比例｜答法：CEO 稱難以知道確切比例，改談量與層數
- ASML_Q2_2026_Earnings_Call_20260715.md｜問：Tammy Qiu（Berenberg）問能否優於 WFE 成長｜答法：CFO 稱從不評論 WFE，只談自家計畫
- ASML_Q2_2026_Earnings_Call_20260715.md｜問：Nigel van Putten（MS）問 45% 產能是否為 EUV 營收下限｜答法：CFO 稱不對明年營收給任何指引
- ASML_Q2_2026_Earnings_Call_20260715.md｜問：Muse（Cantor）問 60% 增量營業利益率是否為目標｜答法：CFO 稱不量化，僅說營運槓桿將變好
- ASML_Q2_2026_Earnings_Call_20260715.md｜問：Scemama（BofA）問 2027 毛利率是否高於 2026 出口率｜答法：CFO 稱不給 2027 毛利率指引，只列定性驅動因素

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
{"date":"20260716","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"WFE/EUV 需求超級週期延續，AI 驅動 capex 兌現","columns":{"2Y 驗證點":"2026 €43–45B（二度上修）、2027 再成長且訂單近乎全滿","5Y 驗證點":"2030 €44–60B（投資者日模型）","10Y 驗證點":"EUV 為 sub-2nm 物理必需，多代延續","具體數字門檻":"2026 指引 €43–45B（上緣）；2027 EUV 產能 84 台；WFE 2027 $135B（SEMI，+7.3%）；設備銷售 2027 創高 $156B","信息來源":"ASML 2026-07-15 法說 + SEMI 2026 forecast","漂移觸發":"2026 指引下修 或 WFE 連 2 季降速 或 2027 訂單連 2 季軟化 → 削弱"}},{"id":"H2","text":"High-NA EUV（0.55NA）鞏固下一代壟斷——由 Intel 首度高量產驗證（前次「延後/集中」已部分解除）","columns":{"2Y 驗證點":"Intel Panther Lake on 18A 選擇性層 High-NA 高量產（2026-07-15 ASML 證實特定層別雙資格認證、良率與 NXE 相當；「85%」為 KeyBanc 推估）；SK Hynix 2 台、Samsung EXE:5200B（SF2/HBM4）","5Y 驗證點":"EXE:5200 大量商業部署 2028–29；TSMC 仍缺席至 ~2029（A14 用 0.33NA）","10Y 驗證點":"High-NA 成 sub-1.4nm 主流","具體數字門檻":"2026 出貨 10 台 High-NA（~$380M/台）；60+ 台總 EUV；2027 EUV 產能 +~30%（~78–84 台，來源分歧）；Intel 14A 風險量產 2027、量產 2028","信息來源":"ASML 2026-07-15；Intel Foundry roadmap；TrendForce","漂移觸發":"Intel 14A 取消 或 High-NA 出貨連 2 季 miss → 削弱"}},{"id":"H3","text":"估值 de-rate 至壟斷成熟區 30–35x FY27（de-rating＝進場條件，非賣出條件）——本份已透過 EPS 成長兌現","columns":{"2Y 驗證點":"FY27 fwd PE ≤ 34–35x（後上修共識 ~$52 → $1,815 = 33–35x）","5Y 驗證點":"持有期內倍數維持 28–35x 壟斷成熟區","10Y 驗證點":"—","具體數字門檻":"後上修 FY27 EPS ~$52（凍結 Excel 快照仍 $47.87 = 37.9x，見 §11 lag 註記）","信息來源":"§11.1 歷史分位 + Q2 二度上修 + 共識上修軌跡","漂移觸發":"FY27 fwd PE 反升 &gt; 45x → 追高風險、暫停加碼"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"出口管制升級：MATCH Act（2026-04-22 通眾院外委會，把管制自 EUV 擴及 DUV、150 天窗施壓荷/日否則 FDPR）；BIS/Lutnick 自 2026-04 質問 ASML 高管 EUV 零件是否違規流入中國（AMAT 2026-02 因經韓轉 SMIC 遭罰 $252.5M 為先例）。兩情境：溫和管制＝壓縮 China ~20% TAM；MATCH Act 若過關擴及 DUV＝近乎清零 China 業務（China 現幾乎全靠 DUV+服務）——後者機率較低但衝擊大一個量級","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1–2 季可觸發）","監測指標":"MATCH Act 立法進度、BIS 立案、China 營收占比","警戒閾值":"MATCH Act 院會表決 或 BIS 正式立案；China 營收連 2 季 YoY &lt;−30%（JPM 估 EPS −10%）"}},{"id":"R2","text":"High-NA 採用邊際化：TSMC 跳過至 ~2029、High-NA 經濟性（~$380M/台）使非 Intel 客戶採用緩慢；Intel 14A 若找不到外部客戶而暫停 → H2「鞏固下一代壟斷」右移","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4–6 季）","監測指標":"High-NA 季度出貨、Intel 14A 外部客戶確認、TSMC High-NA roadmap","警戒閾值":"High-NA 連 2 季出貨 miss 或 Intel 14A 確認暫停"}},{"id":"R3","text":"AI capex 週期見頂 + 估值倍數壓縮：hyperscaler 2026 FCF 已惡化（Amazon 已轉負——2026 Q1 −$18.2B、FY 估 −$17~28B；四大合計 capex ~$725B、+77% YoY，BofA 估已吃掉 ~94% 股利回購後營運現金流）→ 若 2027 capex 增速見頂 → 訂單能見度被折價 + 倍數壓向中樞——最高機率、不需基本面惡化","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期慢變數（可被 R1 加速）","監測指標":"hyperscaler capex 修訂、WFE 增速、FY27 fwd PE 分位","警戒閾值":"hyperscaler 2027 capex guidance 下修 或 WFE 連 2 季負成長"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼觸發：回檔至 $1,650（FY27 ≈32x）分批，或 2027 指引/訂單再上修、Intel 14A 外部客戶落地","irr_base_pct":7.0,"ev5y_pct":37.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":3.6,"ev5y_pct":37.0,"irr_base_pct":7.0,"max_dd_pct":-55.0,"bull_5y_price":3449.0,"bear_5y_price":1271.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"加碼觸發：回檔至 $1,650（FY27 ≈32x）分批，或 2027 指引/訂單再上修、Intel 14A 外部客戶落地","price_at_dd":1815.27,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ASML_20261017/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
