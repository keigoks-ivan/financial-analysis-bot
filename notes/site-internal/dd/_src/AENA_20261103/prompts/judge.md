你是 stock-analyst **v20 判斷 agent**，標的 AENA（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"AENA","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AENA_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AENA_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_consolidated_reven","label":"Total consolidated revenue (9M)","value":5283.9,"period":"9M 2026（截至 2026-09-30，公告於 2026-10-28）","unit":"EUR m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"9M 2026（截至 2026-09-30，公告於 2026-10-28）","citation":"Aena IR 新聞稿 https://www.aena.es/en/press/aena-earns-a-profit-of-1774.7-million-euros-in-the-first-nine-months-of---2026.html"},"note":"查無"},{"id":"f_kpi1_ebitda_9m","label":"EBITDA (9M)","value":3077.9,"period":"9M 2026（截至 2026-09-30，公告於 2026-10-28）","unit":"EUR m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"9M 2026（截至 2026-09-30，公告於 2026-10-28）","citation":"Aena IR 新聞稿（同上）"},"note":"查無"},{"id":"f_kpi2_net_profit_9m","label":"Net profit (9M)","value":1774.7,"period":"9M 2026（截至 2026-09-30，公告於 2026-10-28）","unit":"EUR m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"9M 2026（截至 2026-09-30，公告於 2026-10-28）","citation":"Aena IR 新聞稿（同上）"},"note":"查無"},{"id":"f_kpi3_net_operating_cash_flow_","label":"Net operating cash flow (9M)","value":2811.3,"period":"9M 2026（截至 2026-09-30，公告於 2026-10-28）","unit":"EUR m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"9M 2026（截至 2026-09-30，公告於 2026-10-28）","citation":"Aena IR 新聞稿（同上）"},"note":"查無"},{"id":"f_kpi4_investment_paid_capex_au","label":"Investment paid (capex, 含 Augusta 51% 股權 343.5)","value":1133.5,"period":"9M 2026（截至 2026-09-30，公告於 2026-10-28）","unit":"EUR m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"9M 2026（截至 2026-09-30，公告於 2026-10-28）","citation":"Aena IR 新聞稿（同上）"},"note":"查無"},{"id":"f_kpi5_net_financial_debt_net_d","label":"Net financial debt / Net debt-to-EBITDA","value":5845,"period":"2026-09-30，公告於 2026-10-28","unit":"EUR m（1.47x EBITDA）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"2026-09-30，公告於 2026-10-28","citation":"Aena IR 新聞稿（同上）"},"note":"查無"},{"id":"f_kpi6_passengers_group","label":"Passengers (Group)","value":309.9,"period":"9M 2026（截至 2026-09-30，公告於 2026-10-28）","unit":"m pax","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"9M 2026（截至 2026-09-30，公告於 2026-10-28）","citation":"Aena IR 新聞稿（同上）"},"note":"查無"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_aena_gross_margin_pct","label":"AENA 毛利率","value":74.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AENA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aena_operating_margin_pct","label":"AENA 營業利益率","value":47.51,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AENA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aena_fcf_margin_pct","label":"AENA FCF 利潤率","value":15.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AENA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_asr_gross_margin_pct","label":"ASR 毛利率","value":47.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_asr_operating_margin_pct","label":"ASR 營業利益率","value":40.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_asr_fcf_margin_pct","label":"ASR FCF 利潤率","value":23.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pac_gross_margin_pct","label":"PAC 毛利率","value":55.6,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PAC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pac_operating_margin_pct","label":"PAC 營業利益率","value":43.29,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PAC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pac_fcf_margin_pct","label":"PAC FCF 利潤率","value":14.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PAC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":27.6,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":21.16,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":68.52,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.57,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.75 → 1.74）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.82 → 1.82）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.53,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.87 → 1.88）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.74,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":1.82,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":1.88,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-4.4,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 1.82 → 1.74（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":13.73,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝14.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":14.7,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.08,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.87,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":15.56,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 1.74，分子＝快照價 27.08","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":3.949,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":5376.41,"period":"2026-11-03","unit":"EUR m","basis":"yfinance 最新一季：總債務 7933.87、現金 2557.46（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1500.0,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":46776.41,"period":"2026-11-03","unit":"EUR m","basis":"市值 41400.0 ＋ 淨負債 5376.41","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6903.97,"period":"2026-11-03","unit":"EUR m","basis":"yfinance revenue_estimate 0y 平均（16 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":7241.12,"period":"2026-11-03","unit":"EUR m","basis":"yfinance revenue_estimate +1y 平均（19 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":6.78,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 27.08 / W52 24.94 / W104 22.94 / W250 17.25 / W250 13週斜率 1.31%"},{"id":"f_ma_w52","label":"52 週均線","value":24.94,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":22.94,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":17.25,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.31,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Ryanair 因 Aena 2026 年機場費調漲（約 6.5%）宣布夏季 2026 再砍西班牙區域機場 120 萬座位；Valladolid 旅客 -59.5%（至7月）、Santiago -13.3%，Vigo +10.2%、Zaragoza +2.9% 部分抵銷（來源為 Idealista 報導，2025 年資料）","source":"Idealista - Ryanair Spain news: 1.2m seats cut as Aena row intensifies","url":"https://www.idealista.com/en/news/node/858605","excerpt":null,"as_of":"2025-09-15","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Aena 在 Rio de Janeiro-Galeão 招標最後階段與 Vinci、Zurich Airport 競標；巴西已管理約 20% 機場流量；另以 €309M 收購 Leeds Bradford 控股 51%（海外擴張，非西班牙國內新進入者）","source":"Moodie Davitt Report / 搜尋摘要彙整","url":"https://moodiedavittreport.com/aena-forecasts-commercial-revenues-to-exceed-2019-level-by-48-in-2026","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Aena 對 Ryanair 依賴高：西班牙媒體稱約每 10 位 Aena 機場旅客有 2 位搭 Ryanair；Ryanair 2025 年在 Aena 西班牙機場載客 13.3 百萬人（媒體報導，非 Aena 官方分航空公司揭露）。","source":"Vozpópuli, Ryanair dispara su dominio en los aeropuertos españoles","url":"https://www.vozpopuli.com/economia/empresas/ryanair-dispara-su-dominio-en-los-aeropuertos-espanoles-en-plena-guerra-contra-el-gobierno.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Ryanair 因費率爭議削減西班牙運力（報導稱取消 12 條航線、80 萬座位），Valladolid、Santiago 受衝擊最大；easyJet 等部分填補。","source":"Vozpópuli / Menorca.info 報導","url":"https://www.vozpopuli.com/economia/empresas/la-guerra-con-aena-fortalece-a-ryanair-gana-otros-tres-millones-de-pasajeros.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Moody's 於 2026-05-29 將 Aena 評等由 A2 升至 A1，展望穩定；Fitch 報導為 A+、展望穩定，預期 2026–2030 平均淨槓桿約 1.9x。未見降評。","source":"Moody's rating action via Aena IR","url":"https://airportcities.aena.es/documents/d/accionistas-e-inversores/rating_action-moodys-ratings-upgrades-aenas-29may2026-pr_523691","excerpt":null,"as_of":"2026-05-29","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Fitch 升 Aena 至 A+，穩定展望，DORA III 強化現金流能見度","source":"Democrata.es","url":"https://www.democrata.es/it/economia/fitch-migliora-il-rating-di-aena-per-il-traino-del-traffico-e-il-dora-iii-rafforza-la-visibilita-di-cassa/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Aena 將自 2027 夏季季起在馬德里 Barajas 與巴塞隆納 El Prat 依航廈管理容量，定位為 DORA III 投資投入使用前的過渡措施，限制將隨 2027–2031 投資執行逐步取消","source":"Aviation Week / Air Journal (2026-07)","url":"https://www.air-journal.fr/2026-07-07-aena-va-plafonner-la-croissance-a-madrid-et-barcelone-a-partir-de-2027-5276120.html","excerpt":null,"as_of":"2026-07-07","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"DORA III（2027–2031）總投資 128.88 億歐元，其中受管制部分 99.91 億歐元；2026-09-15 部長會議核准；巴塞隆納容量規劃由 5,500 萬升至 8,000 萬","source":"Aena 3Q26 results release / 搜尋摘要","url":"https://www.aena.es/doc/pressdetail/261028-aena-resultados-3rt-en.pdf","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Aena 維持 2026 西班牙網路客運成長 1.3% 預測（3.26 億人次），但 1H2026 實際成長 3.7%，CAPA 稱 Aena 低估需求；航空公司公會要求 DORA III 期間每年降價 4.9%","source":"CAPA centreforaviation 'ALA: Aena underestimates demand as traffic grows 3.7% in 1H2026'","url":"https://centreforaviation.com/news/ala-aena-underestimates-demand-as-traffic-grows-37-in-1h2026-1365987","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"CNMC 於 2026-06-02 建議 DORA III（2027-2031）機場費率每年下調 0.59%，Aena 原提案為每年上調 3.82%；WACC 由 9% 降至 7.4%，OPEX 減 741.5 百萬歐元；最終由部長會議決定。","source":"RTVC: La CNMC propone rebajar las tasas aeroportuarias hasta 2031","url":"https://rtvc.es/la-cnmc-propone-rebajar-las-tasas-aeroportuarias-hasta-2031-3-junio-2026/","excerpt":null,"as_of":"2026-06-03","retrieved_at":"20261103","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"CNMC 的 FBO 案（S/0014/25）中 Aena 是檢舉方而非被調查對象；未發現針對 Aena 的反壟斷調查或歐盟執委會行動。Ryanair 公開指責 Aena 壟斷，但搜尋未見監管機關調查。","source":"CNMC press release 2025-10-24 (sancionador FBO)","url":"https://www.cnmc.es/prensa/sancionador-fbo-20251024","excerpt":null,"as_of":"2025-10-24","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#none","axis":"reg_tariff_export","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Aena 為機場營運商、無製造據點；Middle East 衝突下管理層仍維持 2026 年西班牙機場 1.3% 客運成長預測（約 3.26 億旅客）","source":"The Corner: Despite geopolitical climate, Aena maintains forecast of 1.3% growth","url":"https://thecorner.eu/companies/despite-geopolitical-climate-aena-maintains-forecast-of-1-3-growth-across-network-of-airports-in-spain/124892/","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Q2 2026 摘要：2026 客運成長約 3%，H2 能見度有限，受地緣與經濟不確定、燃油避險到期、載客率轉弱影響","source":"Quartr: Aena SME Q2 2026 earnings summary","url":"https://quartr.com/events/aena-sme-sa-aena-q2-2026_3P4iBxKF","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"產業層級單點失效：2025年9月 Collins Aerospace 報到系統遭攻擊，單一供應商失效波及多個歐洲機場；OT-ISAC 2026年8月報告將第三方集中風險評為高。未找到 Aena 自身供應商集中揭露","source":"OT-ISAC report (Aug 2026)","url":"https://www.otisac.org/_files/ugd/5f2206_2a44f6c125144607af53aa7692de6fea.pdf","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"H1 2026 總營收 3,299.6 百萬歐元（+10.1%，不含 IFRIC 12 為 +8.3%）；西班牙機場 H1 旅客 156,246,234 人，年增 3.7%（2025 H1 為 +4.5%）；管理層預期西班牙 2026 年流量約 +3%","source":"Aena H1 2026 results press / travelextra.ie","url":"https://www.aena.es/en/press/aena-closes-the-first-half-of-2026-with-a-profit-of-1002-million-euros.html","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"H1 2026 分段：航空營收 +8.3%、商業營收 +7.1%（983.9 百萬歐元）、不動產 +15%；國際營收 +24.5%（Quartr）或 +27.9%（財報電話會議逐字稿），兩來源不一致；Leeds Bradford 自 2026-05-07 併入","source":"Quartr Aena Q2 2026 summary / earnings call transcript (roic.ai)","url":"https://quartr.com/events/aena-sme-s-a-aena-q2-2026_3P4iBxKF","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"DORA III（2027–2031）：Aena 提案平均每年每旅客 +0.43 歐元（約 3.8%/年）、投資 12.888 十億歐元；Aena 預測 2027–2031 流量年增 1.3%，CNMC 為 2.2%，航空公司為 3.6%；ALA 要求每年降價 4.9%","source":"thecorner.eu / aviacionaldia.com / Aena press release","url":"https://aviacionaldia.com/en/2026/02/aena-proposes-airport-fee-hikes-in-spain-triggering-strong-opposition-from-airlines.html","excerpt":null,"as_of":"2026-02-18","retrieved_at":"20261103","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"競爭主管機關 CNMC 呼籲政府確保 Aena 在 2031 年前降低機場收費（DORA III 監管不確定性）","source":"thecorner.eu","url":"https://thecorner.eu/companies/competition-authority-calls-on-government-to-ensure-aena-reduces-airport-charges-until-2031/125999/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Aena 西班牙 2026 H1 旅客 +3.7%、全年預期約 +3%","source":"Aena H1 2026 results PDF","url":"https://www.aena.es/doc/pressdetail/260729-aena-resultados-1s-en.pdf","excerpt":"have recorded a total of 156,246,234 passengers (3.7% more than in 2025), representing a lower growth rate than that recorded in the first half of 2025","as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"0","claim":"Aena 提案 DORA III 每旅客年均 +0.43 歐元","source":"Aena press release","url":"https://www.aena.es/en/press/aena-proposes-13-billion-euros-of-investment-for-all-airports-in-its-network---in-spain-and-an-average-annual-increase-of-43-cents-per-passenger-in---airport-charges.html","excerpt":null,"as_of":"2026-02-17","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"2026上半年西班牙鐵路故障使旅客回流航空：馬德里–馬拉加航空流量+23%、馬德里–塞維亞+18%、馬德里–瓦倫西亞+12%；高鐵在可靠時仍為馬德里–巴塞隆納、馬德里–馬拉加的強勢替代品（原文為搜尋摘要轉述，未讀頁面）","source":"rustourismnews.com: spains rail problems are sending travelers back to planes","url":"https://www.rustourismnews.com/2026/09/17/spains-rail-problems-are-sending-travelers-back-to-planes/","excerpt":null,"as_of":"2026-09-17","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Aena與UrbanV/Volocopter 2024年eVTOL可行性研究指出，示範飛行取決於資金、資源與飛行許可，地面基建、空域重設與商業模式仍有許多挑戰；示範時程已延後（搜尋摘要轉述）","source":"aviacionline: feasibility studies launch for eVTOL integration in Aena's airport network","url":"https://www.aviacionline.com/feasibility-studies-launch-for-evtol-integration-in-aenas-airport-network","excerpt":null,"as_of":"2024-06-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q1 2026 Aena 免稅收入下滑（Avolta 營運免稅 -0.7%），而餐飲與專賣店上升，屬商業組合內部變化","source":"TRBusiness: Aena in Q1: duty-free down, but F&B and speciality shops up","url":"https://www.trbusiness.com/regional-news/europe/aena-in-q1-duty-free-down-but-fb-and-speciality-shops-up/278254","excerpt":"Within the retail division, which delivered revenue of €263.07m/$308m*, the group saw another contraction in income from its Avolta-operated duty-free stores of -0.7% to €131.7m/$154.4m.","as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Jefferies 維持買進、目標價 €29.50，Q2 後預測大致不變；當日收盤 €26.82，2027 EPS 本益比 16.3x、股息率約 4.9%；下一批催化劑為 DORA III 確認、策略計畫更新、2027 費率設定","source":"Bolsamania: Jefferies reitera su recomendación de compra sobre Aena tras mantener intactas sus perspectivas financieras","url":"https://www.bolsamania.com/noticias/empresas/economia--jefferies-reitera-su-recomendacion-de-compra-sobre-aena-tras-mantener-intactas-sus-perspectivas-financieras--23176892.html","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 2026 集團 EBITDA €1,146m，低於分析師共識 0.8%；Bernstein 升至 Outperform 目標價 €30.80，BofA 買進目標價 €30.50；52 週高 €28.86","source":"Parqet Aena asset page","url":"https://app.parqet.com/pl/assets/aena-ES0105046009","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"TipRanks 平均 12 個月目標價 €27.56；Simply Wall St 共識公允價約 €25.94 上調至 €26.54，區間約 €20.54–€31.50（無明確日期）","source":"TipRanks ES:AENA; Simply Wall St AENA","url":"https://www.tipranks.com/stocks/ES:AENA","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q1 2026 營收年增 11.6% 高於共識 4.9%，EBIT 利潤率 31.0% 低於共識 33.5%；公司表示重新評估交通量預測、原 1.3% 預測可能調整（落差：未見正式 guidance 上/下修）","source":"The Corner: Aena net profit Q1 2026; Quartr Q1 2026 summary","url":"https://thecorner.eu/?p=125453","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Aena Q2 2026 業績摘要（guidance／展望）","source":"Quartr Aena Q2 2026","url":"https://quartr.com/events/aena-sme-sa-aena-q2-2026_3P4iBxKF","excerpt":"Outlook and guidance Traffic growth for 2026 estimated at around 3% year-on-year, with limited visibility for H2 due to geopolitical and economic uncertainties, expiring fuel hedges, and weakening load factors.","as_of":"2026-08-14","retrieved_at":"20261103","affects":["thesis.H","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Aena 子公司 2025-12-18 同意收購 Leeds Bradford 與 Newcastle 控股公司 51%，2026-05-07 完成（H1 2026 新聞稿）","source":"Aena 2026 H1 results press release; 搜尋摘要彙整 Aena 2025 年報新聞稿","url":"https://www.aena.es/en/press/aena-closes-the-first-half-of-2026-with-a-profit-of-1002-million-euros.html","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Aena 9M 2026 業績稱已於 2026-10-06 完成收購 Rio de Janeiro–Galeão 機場特許經營商 100% 股權","source":"Aena 9M 2026 results press release","url":"https://www.aena.es/doc/pressdetail/261028-aena-resultados-3rt-en.pdf","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"CNMC（競爭主管機關）調查數家企業涉嫌就 Aena 招標的 FBO 空間租賃圍標，屬初步檢查，Aena 非被調查對象（來源摘要）","source":"Bolsamanía / CNMC","url":"https://www.bolsamania.com/noticias/empresas/economia--la-cnmc-investiga-a-varias-empresas-por-un-posible-reparto-de-licitaciones-convocadas-por-aena--16891736.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulated_rate_case_roe#0","axis":"regulated_rate_case_roe","section":"coverage","direction":"-","claim":"CNMC 2026-06-02 報告建議 DORA III（2027–2031）WACC 由 Aena 主張的 9% 降至 7.44%，平均年費率 -0.59%（Aena 申請 +3.82%）；為建議非定案","source":"CNMC 新聞稿 informe DORA 2026-06-02（經搜尋摘要）","url":"https://www.cnmc.es/prensa/informe-dora-20260602?back=news","excerpt":"Reducir el coste de capital (WACC) del 9 % al 7,4 %, según criterios alineados con la regulación europea","as_of":"2026-06-02","retrieved_at":"20261103","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulated_rate_case_roe#1","axis":"regulated_rate_case_roe","section":"coverage","direction":"0","claim":"Aena 9M 2026 業績稿載明部長會議已於 2026-09-15 核准 DORA III（2027–2031）","source":"Aena press: Aena earns a profit of 1,774.7 million euros in the first nine months of 2026","url":"https://www.aena.es/en/press/aena-earns-a-profit-of-1774.7-million-euros-in-the-first-nine-months-of---2026.html","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["triggers","valuation"],"status":"ok"},{"id":"regulated_rate_case_roe#2","axis":"regulated_rate_case_roe","section":"coverage","direction":"0","claim":"DORA III 最終 WACC 8.32%、年均機場費 +0.33%，部長會議 9/15 核准","source":"Quartr Aena investor update summary","url":"https://quartr.com/events/aena-sme-s-a-aena-investor-update_3P4iyUxo","excerpt":"The WACC is set at 8.32%, and average annual airport charges will rise by 0.33%. Regulated OpEx is projected to grow from €1.929 billion in 2027 to €2.079 billion in 2031, reflecting inflation and regulatory demands.","as_of":"2026-09-21","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"收購 Leeds Bradford 與 Newcastle 控股公司 51%，2025-12-18 簽約、2026-05-07 完成","source":"Aena 2026 H1 results press release","url":"https://www.aena.es/en/press/aena-closes-the-first-half-of-2026-with-a-profit-of-1002-million-euros.html","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"2026-10-06 完成收購 Rio de Janeiro–Galeão 機場特許經營商 100% 股權","source":"Aena 9M 2026 results press release","url":"https://www.aena.es/doc/pressdetail/261028-aena-resultados-3rt-en.pdf","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 11 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"AENA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.65,"operating_margin_pct":47.51,"fcf_margin_pct":15.94,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AENA","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ADP.PA","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADP.PA"},"note":"quarterly_income_stmt 無資料"},{"name":"FHZN.SW","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FHZN.SW"},"note":"quarterly_income_stmt 無資料"},{"name":"ASR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":47.63,"operating_margin_pct":40.81,"fcf_margin_pct":23.32,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PAC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":55.6,"operating_margin_pct":43.29,"fcf_margin_pct":14.44,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PAC","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"AENA"},"financial_history":{"ticker":"AENA","currency":"EUR","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":4190195000.0,"revenue_yoy_pct":null,"gross_margin_pct":61.06,"operating_margin_pct":32.29,"net_income":901499000.0,"diluted_eps":0.601,"free_cash_flow":1135474000.0,"fcf_margin_pct":27.1,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":5047917000.0,"revenue_yoy_pct":20.47,"gross_margin_pct":65.89,"operating_margin_pct":41.72,"net_income":1630814000.0,"diluted_eps":1.087,"free_cash_flow":836877000.0,"fcf_margin_pct":16.58,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":5784328000.0,"revenue_yoy_pct":14.59,"gross_margin_pct":68.17,"operating_margin_pct":45.4,"net_income":1934224000.0,"diluted_eps":1.289,"free_cash_flow":1923938000.0,"fcf_margin_pct":33.26,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":6294312000.0,"revenue_yoy_pct":8.82,"gross_margin_pct":70.36,"operating_margin_pct":47.12,"net_income":2136676000.0,"diluted_eps":1.42,"free_cash_flow":1728176000.0,"fcf_margin_pct":27.46,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/AENA/AENA_Q1_2026_Earnings_Call_20260429.md）

# Q1 2026 Earnings Call
2026-04-29

Q1 2026 Earnings Call
Aena S.M.E., S.A. | Earnings Calls | 2026-04-29
Operator (Operator)
Hello, everyone, and thank you for joining us today for the Aena Q1 2026 Results Presentation. My
name is Sami, and I'll be coordinating your call today. [Operator Instructions] I'll now hand over to
your host, Carlos, Head of IR, to begin. Please go ahead, Carlos.
Carlos Gallego (Executives)
Good afternoon, everyone, and welcome to our Q1 2026 results presentation. This is Carlos Gallego
speaking, Head of IR. It's a pleasure to be with you today. Our CFO, Ignacio Castejon, will host the call
together with me. We are going to cover some of the main topics explained in the results presentation
that is already available in the CNC website, and we'll finish with a Q&A session. [Operator
Instructions] without further ado, I give the floor to Gasteol.
Ignacio Hernandez (Executives)
Thank you very much, Carlos. Hello, everyone. Good afternoon, and thank you for joining us today with
our Q1 2026 results presentation. I will start commenting some highlights. And afterwards, I give the
floor to Carlos. We'll have a Q&A session at the end of the call. Let me start on Slide 4 with some
comments on traffic trends. As you can see, traffic increased for the group 3.8% year-on-year, up to
81.3 million passengers. If we look at the Spanish network, the annual increase was 3.2%, and we
reached almost 65.6 million passengers. -- slightly ahead of our forecast for this quarter.
Please note that the traffic performance for this quarter has been positively affected by the timing of the
Easter break. Last year, the Easter break took place in April, and this year has been -- has happened
between March and April. And we have also experienced some positive shift from rail to air transport, I
would say, took place on an extraordinary basis. If we look at the short term from a traffic standpoint,
what I can share with you at this moment in time is that April so far is performing well.
Let's have a look at the financial performance. 2026 Q1 total revenues for the group accounted for EUR
1,479.9 million. That's an increase of EUR 154.3 million. EBITDA reached EUR 661 million, increasing
by EUR 17.4 million. And we look at net profit, profit after taxes, that was circa EUR 330 million, an
increase of 9.3%, circa an increase of EUR 30 million. The growth in revenues was driven by traffic
performance, traffic evolution, the increase in the Aero charges from March 1, the improvement in
commercial activity and the performance of our international assets. Please let me highlight that when
we look at the performance of the international assets, -- given the increase in the construction services,
I'm now looking at Slide 6. The explain -- they mostly explain that increase. The construction services
amounted to EUR 84.3 million in the first quarter of 2026 compared with only EUR 8 million in the
first quarter of 2025.
Basically, this reflects the progress that we are having in the Congonhas portfolio with the progress in
that specific airport in all the construction activities. If we exclude the IFRIC 12 construction revenues,
the underlying consolidated revenue growth for the group was 6% in this quarter. Let's have a look at
the performance by business lines. Aero revenues, they grew by 5.2%. commercial revenues, 5.5%.

Revenues from real estate, a very positive and high increase with a 16.8% and international revenues
increased by 57.7%, largely driven, as I was explaining earlier, by the construction revenues recognized
on the IFRIC 12. If we exclude this effect, the revenue grew -- growth, sorry, of our international
revenues would have been 8%. Let's have a look in more detail to Aero and commercial. Aero, just a
couple of comments. As you know, as you, I'm sure, have seen in the papers we have said with the
market, dilution in this quarter has been EUR 28.7 million.
That's much higher than the dilution that we have last year. And the main reason is the increase in
tariff. Last year, tariff was flat for the first quarter. And in this specific year, the tariff has been flat for
the first two months has increased in the third month, and we are taking into account the final tariff for
the whole year in order to calculate dilution. That's the rationale for -- the main rationale behind the
EUR 28 million of dilution that are not part of the revenues at this moment in time in this quarter, but
will be revenues for the group in a couple of years through the dilution factors to the K factor. If we look
at the commercial revenues, just a few comments. Sales keep going -- keep increasing, circa 5% in the
first quarter of 2026 and also a very important growth in all our activities that we manage in-house. I'm
referring to VIP services and parking. VIP services keep delivering growth rates higher than 30% and
parking revenues also performed very strongly. When we look at the retail activities, I would like to
share with you that we have an excellent results in the awards of the contracts in F&B and specialty
subs, as you can see in the information provided to the market. For example, in F&B, MAGs increased
by 30% when comparing MAGs for 2026. And if we look at the specialty subs, MAGs increased by 45%
when we compare the MAGs in 2026 to 2025.
So very good results from all the contracts award for retailing activities in this quarter. And let me
finish on commercial business with another topic. We have managed to reach agreement with a number
of tenants in relation to all the losses that the company had in -- through COVID because traffic losses.
This is -- as a result of these agreements, the company will have a cash inflow in the next months and
also income that you will be seeing in the next quarter when we present the results for the first half of
the year. The income that will come to -- that you will be able to see at that moment in time will be circa
EUR 30 million as part of our commercial income mainly. Let's have a look at cost.
So I would move into Slide 7. I've seen a number of notes on cost and operating cost this morning from
many of your notes. Basically, let me share some information, and we can exchange this later on the
Q&A. With respect to information, operating expenses, so that includes supplies, staff costs and other
operating expenses for the group. If you look and compare year-to-year, the increase is 17.8%, a total of
EUR 850 million. Please note that, that increase is taking into account the IFRIC 12. So if we remove
from that item, the IFRIC 12 impact, the increase in cost in OpEx would be circa 7% for the whole group
for the consolidated group. We have been -- for a number of years and especially in the last two calls
that we have had with all of you, we have been anticipating that we are seeing a trend with respect to
our OpEx in which that trend is provoking that the OpEx figures of the company go north. We have also
tried to be very transparent about the reasons of that change of that increase that is mainly explained
by more FTEs, higher traffic, regulation, quality levels, inflation.
So happy to provide more insight later, and I'm sure Carlos will spend some time explaining the other
operating expenses later on, but that's what we are seeing. So when we look at the Spanish network, the
total OpEx figure has increased by 7.9%, reaching EUR 644.3 million, with an increase in staff cost of
12.4% that -- and also a significant increase in other operating expenses. Let's have a look at EBITDA.
So I'm referring to Slide 8. Reported EBITDA for the first quarter of 2026 amounted to EUR 661.1

million. That's a growth of 2.7% year-on-year, and the reported EBITDA margin for the quarter was
44.7%. These figures on EBITDA growth, margin and number are impacted when we compare those
figures with the previous -- with the figures of the previous year or the quarter or first quarter of the
previous year.
And the main impacts are basically explained by the Luton situation in relation to the fire that the
parking and the reconstruction of that parking after the fire and insurance compensation, but also
IFRIC 12 impacting on the margin. So if we remove the impact of the extraordinary revenues that we
had in the first quarter of 2025 related to the fire compensation for the reconstruction of the parking,
the increase in the EBITDA of the group would have been higher than 5%, 5.1%, amounting to an
increase of EUR 32.1 million. If we remove from the margin calculations, this compensation, but also
the IFRIC 12, the margin of the group would stand this quarter 2026 at 47.4% compared with a margin
also in 2025 of 47.7%.
So a decrease, but a very slight decrease, I would say, a flattening of EBITDA margins when we remove
all these extraordinary items. Let's have a look at the net profit that is also in that slide. Net profit
amounted to EUR 329 million in the first quarter of 2026. That's an increase of 9.3% year-on-year.
That's a very strong growth that is explained by, of course, the business growth that we have been
explaining earlier, but also by the lower depreciation and amortization in this quarter compared to the
quarter of 2025 because of the adjustments in the useful lives that we explained last year, but also
because of the lower net financial expenses that were reduced by EUR 20 million when we compare
quarter-to-quarter, basically explained by the compensation of all the cash that we have in Brazil that
we have in order to be able to pay for the CapEx in the following months and the applicable exchange
rates for this quarter. Let me finish with some comments on EBITDA.
With respect to EBITDA, moving to Slide 9 by business segments. The EBITDA growth in the real
estate activities has amounted to sorry, the -- just give me a minute because I cannot see properly. Yes,
31%. Sorry, that was right. The EBITDA for the real estate business increased by 32%, mainly explained
by the increase in revenues that I was discussing earlier, 16%, but also by the cost control in that
specific business segment. And with respect to international activities, you will see in this Slide 9, a
decline of 3.5%, but it's also explained by all those extraordinary effects, mainly related to the
reconstruction of the parking facility and the insurance compensation related to that reconstruction. If
we were removing that impact, EBITDA for international activity would be going up by circa 16% in this
quarter, confirming the very strong underlying performance of all our assets in Brazil and the U.K., as
Carlos will explain further.
Let me finish with some further notes. Hopefully, in the next weeks, of this quarter, we will achieve the
financial close of the acquisition of a stake in a new holding company that will be owning 100% of Leeds
Bradford Airport and also Newcastle Airport as we anticipated before year-end. And with respect to the
announced transaction related to Rio de Janeiro Galeao International Airport a few weeks ago, the
initial steps in order to achieve financial close of that transaction are happening as we were expecting.
On regulatory and corporate matters, as you know, the company made their proposal for DORA last
February. That's progressing according to our plans. And the AGM that took place in mid-April
approved all the resolutions proposed to our shareholders.
and therefore, the distribution of the dividend approved at the AGM took place this week on Monday,
in which EUR 1.09 per share was paid to all our shareholders an incredible dividend for all our

shareholders. And that was all for me. I will let Carlos to go into further detail in a number of topics for
today's presentation. Thank you very much, Carlos. Thank you.
Carlos Gallego (Executives)
Thank you, Ignacio. Let me go you through some additional details with respect to traffic as
summarized on Slide 12. On traffic, Ignacio already covered traffic performance at the group level and
in Spain. So I'll give a quick overview of the traffic data for our international assets as disclosed in the
press release published on April 13. Luton Airport handled 3.7 million packs. That's an increase of 2.9%
compared to Q1 2025. In our Brazilian assets, ANB managed circa 4.7 million passengers, plus 11.5%
year-on-year. And BOAB recorded 7.2 million passengers, 5.0% higher than the same period of 2025.
Within the Spanish network, domestic traffic declined by 1.4% year-on-year, while international traffic
increased by 5.5%. This reflects a combination of supply and demand factors impacting the domestic
market. On Slide 13, traffic by regions. Europe, excluding Spain, grew by 4.9%, Luton by 8.3%, North
America by 9.5%, Africa by 14.9% and Asia by 36.8%, while the Middle East, minus 13.4% and Spain,
the aforementioned minus 1.4% were the only regions where traffic declined. By countries, traffic with
the United Kingdom increased by 4.9%, Germany declined by 1.2% and Italy increased by 5.3%. At
airport level, Alicante recorded passenger growth of 6.6%, Malaga grew by 6.3%, Madrid increased by
4.3% and Barcelona increased by 4.1%. By airline, Ryanair reduced passenger volumes by 3.4% year-
on-year with a market share of 19.6% of total traffic. Vueling increased passenger volumes by 4.3% with
a market share of 16%. And finally, Iberia increased passenger volumes by 0.9%, representing a market
share of 8.2%.
Let's analyze in more detail the commercial performance. So let's move to Slides 14 and 15. Total sales
increased by 4.9%, higher than the traffic growth.
And on a per passenger basis, the growth has been 1.7%. Revenue from fixed and variable rents
invoiced in the period increased by 8.3% compared to Q1 2025. Excluding the multiyear straight-line
and other adjustments, commercial and real estate revenue grew by 7.9% to about EUR 488 million
and the revenue on a per passenger basis grew by 3.0%, reaching EUR 7.6 per passenger. As Ignacio
mentioned earlier, total revenues from real estate services increased by 16.7% year-on-year. This
growth was mainly driven by two components. On the one hand, cargo business revenues increased by
16.4%, reflecting continued strength in air cargo activity. And on the other hand, revenues from real
estate operations increased by 32.1%, driven by higher income from leased assets and surface rights
linked to logistics and commercial developments. I think it's worth analyzing the information along
commercial business line to comment on specific details.
On Slide 15, I would like to start by stating that the sales of our tenants in our core retail activities,
duty-free, specialty subs and food and beverage grew in line or above traffic. In the case of duty-free
growth was 8% in the case of specialty subs, 3% and in the case of F&B, 7% Total revenue in duty-free
decreased 0.7% compared to Q1 2025, reaching EUR 131 million. But if we analyze duty-free revenue,
excluding straight lining and other adjustments and consider business revenue as the sum of both the
variable revenue invoice in the period and the MAGs, revenue has grown by 2.8%, which is virtually in
line with traffic growth. In addition, in the first quarter of 2025, the Canary Islands plot was the only
one that exceeded the minimum annual guarantee rents. Total revenue in Food and Beverage grew
year-on-year by 3.5% to EUR 86 million and specialty shops grew by 9.3%, reaching more than EUR 32
million.

The performance in both business lines can be explained by the new brands and tenants, the
improvement of the commercial mix and additional commercial service. Revenue from mobility
services, including car parks and car rentals, has grown by 6.2% to nearly EUR 110 million. Car park
revenue grew well above domestic traffic, 9.1% to EUR 52 million, while domestic traffic decreased by
1.4%. The main drivers behind the revenue growth are the optimization of the variable parking spaces
and the pricing policy, which has boosted the average ticket by 5.8%. Car rental sales grew by 1% and
total revenue by 3.7% to EUR 58 million. This growth is primarily due to a strong performance at major
airports and 1.2% increase in contracts, partially offset by the strong competition among the car rental
providers. Finally, as Ignacio mentioned earlier, Via services revenues continued to grow during the
quarter, plus 31.5% year-on-year in Q1 2026 to EUR 55 million with an income per passenger of EUR
0.84, plus 27% compared to Q1 2025.
Within this business line, VIP lunches is the main one, representing circa 88% of the revenue. Its
revenue grew by 25% because of the higher number of users, plus 15% and higher average price, 9%.
Slide 16 shows a high detail of the main items of the other operating expenses for the network in Spain,
both in million euros and on a per passenger basis. Other operating expenses in the Spanish network
rose to 7.1%, reaching EUR 442 million. This increase was driven by the increase in maintenance, 20%
security, plus 8.5%; PRM plus 23.5% professional services, plus 17.3% and VIP lunches plus 35%,
partially offset by electricity, minus 7.7% and taxes, minus 2.2% -- although OpEx growth was higher
than traffic growth, Aena clearly retains the leadership in the OpEx per passenger metric.
On Slide 17, net cash generated by operating activities amounted to circa EUR 909 million in the first
quarter of 2026, representing an increase of 10.7% year-on-year. Because of this cash generation and
overall financial management, net financial debt to EBITDA improved from 1.46x at year-end 2025 to
1.32x at the end of the first quarter of 2026, reflecting a continued strengthening of the balance sheet.
CapEx paid in the first quarter amounted to circa EUR 300 million. Most of this investment focused on
safety and security and improving the airport facilities. Fixed rate debt stood at 83% of our total debt
compared to 82% of 2025 and the average cost of our debt increased to 2.51% compared to 34% in
2025. I will off commenting on international assets, starting with Luton on Slide 18. In local currency,
revenue at London Luton Airport rows 8.3% to EUR 84.2 million -- sorry,GBP 84.2 million. EBITDA
reached GBP 32.1 million, minus 15.4% and the EBITDA margin was 38.2%, 48.8% in the first quarter
of 2025. The contribution of the group's EBITDA amounted to EUR 37 million. Excluding all the items
recorded in the first quarter of 2025 resulting from the car park fire, insurance compensation for the
rerostruction, loss profit and expenses arising from the car park fire, EBITDA for the first quarter of
2025 will be GBP 27 million, and the year-on-year change will reflect an increase of 18.9% and plus
GBP 5.1 million.
The EBITDA margin will be 35.7% in the first quarter of 2025. Let's move to the Brazilian assets, Slides
19 and 20. I would like to highlight the traffic growth, plus 11.5% in ANB and 5.0% in BOAB and the
very limited CapEx in ANB and the mandatory CapEx we have already started to deploy in BOAB. As
you know, EBITDA margins are affected by the accounting standard IFRIC 12. Excluding this impact,
the EBITDA margin and ANB stands at 65.7%, 65.0% in Q1 2025 and in BOAB at 65.0%, 63.3% in Q1
2025. The contribution of the Brazilian assets to the group EBITDA amounted to EUR 50 million. That
will be the end of my presentation. So Sami, if that's okay for you, we are ready to move to the Q&A
session. I can see that there are many of you who would like to clear up some doubts about this
presentation and to give everyone a chance to speak and to keep within the time limit of this

presentation, I will be grateful if you could limit your comments to a single question. As always, the
Investor Relations team is available to answer any further questions you may have. Thank you.
Operator (Operator)
[Operator Instructions] Our first question comes from Luis Prieto from Kepler Cheuvreux.
Luis Prieto (Analysts)
I'm going to limit myself to one. It's not going to be in the obvious OpEx front. It's going to be more
traffic oriented. So what I would like to come back to is the AGM statement by the Chairman that you
would be reassessing traffic performance in due course. I don't exactly know what reassessing means.
But what forces and tensions are you seeing in short-term traffic performance at the moment?
Ignacio Hernandez (Executives)
Thank you very much, Luis, for your question. This is Ignacio speaking. I think what the Chairman
referred at that moment in time at the AGM, I think it's the comment that all of us are making to
ourselves when the number for the traffic forecast for the traffic guidance of this year was internally
elaborated and built the information, the inputs that Aena had were completely different to the
information that we have in front of us at this moment in time. And we are seeing positive and negative
trends impacting the traffic performance and the trends are so different to the ones that were used at
that moment in time. That's why we, as a company, we were -- we wanted to be transparent about the
situation.
I think confirming a number or putting a number at this moment in time when we are seeing news
every single minute changing the situation, not only of the geopolitics, but also, in particular, the one
impacting our industry is something that all of us are watching and that could impact short term,
medium term and long term from many different fronts. So all that is what we would like to convey to
all of you. I think I've seen some notes Luis this morning, Aena is confirming. Aena is not confirming
the 1.3% -- what we are not confirming or we are not changing. What we are saying is that all the
information that was put together in order to estimate the 1.3% is being materially impacted, and it's
reasonable to expect that the traffic projects forecast for this year will change. But we are seeing Luis
things that are impacting positively and negatively.
And the ones that are impacting negatively could be things that could materially impact the whole
industry. And we are talking about Jet fuel, we are seeing news about flights being canceled, airlines
confirming flight tickets going up. So we are seeing many trend of negative news that is huge in that
regard. It's too early to put a number given that the uncertainty is, in my opinion, at the highest levels
that I have seen in my career. And what we are trying to gain is some more visibility before putting a
number in front of all of you. And that's what we are being totally transparent.
Operator (Operator)
Our next question comes from Tobias [indiscernible] from Bernstein.
Unknown Analyst (Analysts)
I will ask a question on OpEx. And I was wondering if you can help us square the that stands for OpEx.
I appreciate that excluding IFRIC 12, OpEx only grew by 8-ish percent year-over-year. But I would like

to focus on maintenance and security because those are the two cost elements that you had elaborated
on in your DORA 3 proposal as well. When I take the 20% growth in Q1 year-over-year for maintenance
and then I sort of add this up sort of apply that same growth rate over the next couple of quarters, I get
to EUR 311 million in 2026, and you had stated maintenance cost of EUR 300 million in 2027. I'm just
-- this is just an example. I don't want to sort of pinpoint necessarily just on that. But does that mean
OpEx growth for the rest of the year will be slower than in Q1? Is that something you can sort of
elaborate on a little bit?
Ignacio Hernandez (Executives)
Thank you very much for your question. I think with respect to the general trend on OpEx, and we can
discuss some of the items or the items that you have asked on maintenance or security or PRM. I think
the general trend that you will see in OpEx for this year is the one that we have been explaining to the
market for a while, increases that are comparable to increases that you have seen this quarter, the last
quarter of 2025, the third quarter of 2025.
Because the largest items on the other operating expenses of this company, I'm referring to
maintenance, security or PRM are being impacted in many fronts. And we are renewing some of our
contracts. And in those contracts, because of scope getting larger because of regulation, because of
more activities, because of assets that the warranties are terminating and therefore, we have to pay for
the maintenance of those assets because of many reasons, those -- all those costs are going up. You
were referring to maintenance that I think in this quarter, the figure is 20% I'm not expecting a 20%
through the whole year of growth, but it's not going to be materially different to the maintenance
increases to the increases that you have seen in the maintenance items in the previous year. This
quarter perhaps is a bit higher than other quarters. And therefore, you should expect a potential
reduction. But it's not going to be a reduction that changed the trend that we have been explaining to
everyone in our calls.
You have referred to security. Security, there is not a new contract. The contract was signed, I would
say, a couple of years ago, 1.5 years ago. And what you are seeing is an increase in the cost of security
related to CPI more activity that is part of the contract that we have for security. And that's the result of
that number. Don't expect a material change with respect to the performance of that item compared to
the one that you are seeing in this quarter. There could be some slight reduction because in this
quarter, you will remember that in the middle of 2025, we increased the cost in security in order to
have more security guards in our terminals.
And that's an impact that took place around the second half of this year of 2025. So those cost increases
that are impacting the comparison in the first half because we have those, but we didn't have those
costs in the first half of 2025. But through the year, given that we start incurring those increases in
2025 in June, July 2025, you will get some normalization, but it is a very small part of the cost item of
security.
Unknown Analyst (Analysts)
Okay. Great. Maybe just a very, very quick follow-up. So the numbers that you have in your DORA III
proposal, those are still valid and then this quarter has not changed anything regarding your
assumptions?

Ignacio Hernandez (Executives)
Of course, those numbers are still valid. What I would like to highlight is that all of us are seeing the
consequences of the inflation that everyone is anticipating related to the increases in the and inflation is
going to be another important topic in OpEx for the next months because it will depend on how all the
cost increases in oil will be translated or passed through to the economy. And that's something that we
didn't have at the moment in time that we put together the numbers for DORA.
Operator (Operator)
Our next question comes from Graham Hunt from Jefferies.
Graham Hunt (Analysts)
Maybe I'll stick on OpEx and just ask the sort of similar question on staff costs, specifically within Spain
that you're growing 12.5% in Q1. What's going into that number? And is that something we should be
carrying through for the rest of the year? Or is that some one-off impact in there? Just -- and then as we
think beyond, is that giving you capacity that means the outer year is a little bit slower? Just wondering
what's driving such a high increase in staff costs for this quarter.
Ignacio Hernandez (Executives)
Thank you very much. I'm happy to try to address your question. If I am not wrong, -- the increase in
staff cost for this quarter has been 12.5%. That's around EUR 17.6 million. If we look at the breakdown
behind that increase, we have increases in social security costs. That's around EUR 4 million, increases
in headcount. We have been adding people. And if you compare the headcount numbers of this quarter
with the quarter of '25, there is an increase of around 400 people. That's between EUR 3 million and
EUR 4 million of increase. We have some impacts coming because of the collective bargain -- the new
collective agreement that Aena signed last year, adjustments in relation to the variable remuneration
changes coming from the collective agreement, that's a couple of million euros, salary review for 2026
that is 2% that's public. So there are a number of reasons there that I would say are going to happen
through the year and are going to be recurring based on the breakdown and the explanations that I
have just shared with you.
I wouldn't be surprised, Grant, if the cost of staff cost, the increase through the year is double digit and
it's not far from the one that you have seen this quarter. So that's what I can share with you at this
moment in time.
Operator (Operator)
Our next question comes from Cristian Nedelcu from UBS.
Cristian Nedelcu (Analysts)
It's a 2-part question, if I may, and it's all related to kerosene. I guess the first part is in the context of
potential kerosene shortages, could you describe a little bit more about your supply chain in kerosene
and tell us a bit more about that? And also in relation with the higher kerosene prices, we had a French
regulator a few weeks ago published a large document acknowledging that the current disruption will
be considered in their traffic forecast in their WACC assumptions, in their inflation assumptions for the
next regulatory period in France. So my question here is, do you believe the CNMC and the DGAC will

also consider these changes when thinking about DORA III ? And how will the mechanism work?
Would you be expected to update your proposal, your DORA III proposal? Or what is the loss -- what
does the loss say in this situation?
Ignacio Hernandez (Executives)
Thank you. You completely reached the rule of 2 questions of 1 question per speaker. No problem at all.
I think with respect to your first question, the straightforward answer is that as far as we understand,
and there is a group that Aena is part of that is monitoring the supply chain with respect to Kerosene jet
fuel for the following weeks, supply has been confirmed in Spain. So that's the information that I can
share with you at this moment in time. Of course, everything is going to depend on the length of the war
and the length of the situation in the state of Hormuz. So let's see how things evolve. But the
information that I can say is the one that I was summarizing for the following weeks, given all the
information that we are receiving, supply is confirmed in Spain. With respect to your second question,
Cristian, I don't know -- the honest answer is I don't know what the French regulator stated or
proposed about all this.
What I certainly know is that this is confirming the situation, the level of risk of the industry, the level
of risk of any traffic forecast, the level of risk of financial risk that airport operators have that are
looking at the rates. So this is confirming that a crisis happened, that traffic is impacted, that returns
are impacted. And hopefully, given that all this is known by everyone, given that is in the public domain
and all of us are seeing decisions taken by airlines to land planes or how all the situation is impacting
market rates that all that is taken into account by the regulators because it's information that no one
can be get. But with respect to how it's going to be treated, how it's going to be taken into consideration.
I cannot answer you that in a specific manner, your question, Cristian. As you know, we made our
proposal in mid-Feb. And hopefully, we should hear back before summer that we would love in order to
mitigate as much as possible the length of time in which we are exposed to that decision. Thank you,
Cristian.
Operator (Operator)
Our next question comes from Andrew Lobbenberg from Barclays.
Andrew Lobbenberg (Analysts)
Can I just go to a different place of the P&L? And you mentioned a bit in your elaboration about the
change in the financial lines. Can you just explain it a bit more slowly and whether we should expect the
improved financial result to continue through the year or not? That's one, isn't it?
Ignacio Hernandez (Executives)
Thank you, Andrew. I was expecting your question on Luton.
Andrew Lobbenberg (Analysts)
I know. You can tell us about that as well if you want to make it, too. I mean it is flexible.
Ignacio Hernandez (Executives)
Okay. Happy to take it later. I think there is a significant part that is explained because of exchange rate
movements. The real has helped a lot with -- has a bit, sorry, with the appreciation. But I wouldn't

expect that this impact is a structural one through the whole year because of the 2 following reasons.
The cash position in Brazil will get reduced through the natural CapEx cycle of investment in
Congonhas. So that cash will be used for that purpose. And two, there was a loss -- a financial loss in
the first quarter of last year related to the exchange rate that perhaps doesn't happen in the next
quarters. So expect a reduction in that positive impact. And on Luton, we are working hard in order to
make progress for the potential agreement on the expansion on the airport and our role there.
Operator (Operator)
Our next question comes from Dario Maglione from BNP Paribas.
Dario Maglione (Analysts)
Just one question for me on the CNMC. So one of the parameters that they look at is the OpEx
allowance, so the euros per ATU per passenger, let's say. Any discussion on this point with the CNMC
for instance on how to account for OpEx inflation, how this allowance could move?
Ignacio Hernandez (Executives)
I couldn't follow your question completely. But if I understood you well, the answer is that there has not
been a real discussion, and we haven't received feedback from the CNMC yet on our proposal. So I
cannot help you with that one, unfortunately.
Dario Maglione (Analysts)
Okay. And do you maybe have any view on the OpEx allowance, how they could move in DORA 3 and
how likely is that the CNMC and the regulator will allow for some increase compared to...
Ignacio Hernandez (Executives)
Well, what I can share with you, Dario, is that the proposal that we have put on the table in mid-Feb
reflects our views on the OpEx expected performance of the company for the following years.
So talking about allowance or reactions to that figures would be just a speculation from my side at this
moment in time. So let's be hopeful that all the information, highly detailed information provided by
the company in order to explain the CapEx performance that we forecast is taken into account, and we
can operate on those basis.
Operator (Operator)
Our next question comes from Marcin Wojtal from Bank of America.
Marcin Wojtal (Analysts)
So just one question. I believe it was reported recently in Spanish press that you are working on a
business plan presentation that could happen towards the end of the year. Could you perhaps comment
on that very briefly? Is that indeed the intention? And when could that business plan presentation
actually happen?
Ignacio Hernandez (Executives)
Thank you very much for the question, Marcin. Yes, you know that we have a current strategic plan that
ends in 2026 that we updated 18 months ago. well, 24 months ago. Therefore, the current strategic plan

needs to be reassessed and needs to be replaced by a new one. So the company is looking at the next 5-
year period in order to put together what we think makes sense in all our businesses, in our
international strategy from many different perspectives. So given this situation that the current one is
going to end, what I can share with you is that we are working, of course, in order to be ready for the
next 5-year period. And the company has always shared with the market once that exercise has finished
our views for that new strategic period, and that would be our intention.
I cannot confirm Marcin to you when, how. But I think based on experience, please assume that, that
will be our approach. And that once we have more information and we are getting close to the end of
the year, we are likely to be ready in a position for that move.
Operator (Operator)
Thank you. Our next question comes from Jose -- as from Santander.
José Arroyas (Analysts)
I think you answered my question indirectly earlier, but I wanted to make sure I understood correctly.
Is it reasonable to expect that the DORA III will be completed by July this year instead of by
September? And if this is the right interpretation, when should we expect the report, the nonbinding
report from the CNMC?
Ignacio Hernandez (Executives)
Jose, thank you for the question. I would love to have a straightforward answer to your question. What
I can share with you is that we have worked hard in order to set our proposal with the regulator in mid-
Feb. We are aware that CNMC and the Civil Aviation Authority are working -- are also working very
hard -- and what we believe is that the sooner we have a resolution, the better in order to reduce
uncertainty from many perspectives. And that's what we are doing and has always been our intention in
this process. And what I can confirm to you is that the regulators are working -- are also working very
hard based on all the interactions that we have with them. So that's -- we would love to have that
resolution before summer. But it's given all the stakeholders that are involved is something that I
cannot confirm to you. But everyone is working in that direction. Thank you.
Operator (Operator)
We currently have no further time for any questions, I'm afraid. So I'd like to hand back to Carlos for
some closing remarks.
Carlos Gallego (Executives)
Thank you, Sami. As there are no further questions, we would like to conclude today's call. The Investor
Relations team remains at your disposal for any additional information or clarification you may
require. Thank you very much to all of you, and have a great afternoon. Thank you.
Operator (Operator)
This concludes today's call. We thank everyone for joining. You may now disconnect your lines.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AENA_2025_Earnings_Call_20260225.md
- 2026-02-25｜CEO｜guidance：CEO 說明 2026 年西班牙客流預估成長 1.3%，稱為自然預估。（原話："increase of 1.3% and to us, this is a natural estimate"）
- 2026-02-25｜CEO｜risk：CEO 說明部分機場接近技術上限，2026 年起特定日子會有容量限制。（原話："face constraints because the infrastructure"）
- 2026-02-25｜CEO｜guidance：CEO 說明政府須在 2026 年 9 月前核定最終 DORA III。（原話："a deadline in September 2026 to approve the definitive DORA III."）
- 2026-02-25｜CEO｜capital_allocation：CEO 說明 DORA III 下受管制資產基礎預計增加逾 55 億歐元。（原話："our regulated assets base in more than EUR 5.5 billion."）
- 2026-02-25｜CEO｜guidance：CEO 說明 DORA III 提案的平均費率每年上調約 0.43 歐元。（原話："is just EUR 0.43 every year."）
- 2026-02-25｜CEO｜commitment：CEO 承諾西班牙機場費率仍將是歐洲最具競爭力。（原話："and this is a commitment that we will"）
- 2026-02-25｜CFO｜margin：CFO 報告 2025 年 EBITDA 利潤率 59.3%，較 2024 年低 90 bp。（原話："EBITDA margin of 59.3%, 90 basis points lower than in 2024."）
- 2026-02-25｜CFO｜margin：CFO 說明排除 IFRIC 12 影響後，集團 EBITDA 利潤率為 61.4%，改善 50 bp。（原話："would have improved by 50 basis points to 61.4%."）
- 2026-02-25｜CFO｜margin：CFO 報告集團營運費用成長 11.1%。（原話："operating expenses at group level grew by 11.1%"）
- 2026-02-25｜CFO｜margin：CFO 說明排除巴西 IFRIC 12 後集團營運費用增幅為 4.9%。（原話："would be 4.9% for the whole group."）
- 2026-02-25｜CFO｜margin：CFO 說明人事費用成長，並表示將持續增加全職人力。（原話："adding more FTEs to the company in many different fronts"）
- 2026-02-25｜CFO｜guidance：CFO 表示人事費用的上升趨勢預期不會改變。（原話："we don't expect a different change in this trend"）
- 2026-02-25｜CFO｜competition：CFO 稱 Aena 每位旅客營運費用在可比機場業者中最低。（原話："we are the lowest by far."）
- 2026-02-25｜CFO｜guidance：CFO 表示營運費用項目將在近期持續受衝擊。（原話："will be impacted in the near future."）
- 2026-02-25｜CFO｜guidance：CFO 對 2026 年折舊攤銷的指引：水準與 2025 年相近。（原話："a very similar level of depreciation and amortization for 2026"）
- 2026-02-25｜CFO｜margin：CFO 說明資產耐用年限調整的折舊節省明年會較低、非經常性。（原話："next year will be a bit lower."）
- 2026-02-25｜CEO｜capital_allocation：CEO 說明 2025 年股利提案為每股 1.09 歐元（毛額）。（原話："payment of a gross dividend of EUR 1.09 per share."）
- 2026-02-25｜CFO｜capital_allocation：CFO 報告集團淨債務對 EBITDA 為 1.46。（原話："net debt to EBITDA ratio of the group stood at 1.46"）
- 2026-02-25｜CFO｜capital_allocation：CFO 說明若計入巴西短期存款，槓桿比率約 1.35–1.36。（原話："the ratio of 1.46 would be around 1.35, 1.36."）
- 2026-02-25｜CEO｜capital_allocation：CEO 提到 2025 年 12 月取得英國 Leeds 與 Newcastle 機場的重要持股。（原話："we acquired a significant participation in the U.K."）
- 2026-02-25｜CEO｜commitment：CEO 表示長期希望西班牙與國際業務有更均衡的結構。（原話："a better balance between Spain and the rest"）
- 2026-02-25｜CFO｜customer：CFO 說明 2025 年西班牙客流成長主要來自國際市場，內需小幅下降。（原話："International markets grow at circa 6%"）
- 2026-02-25｜CFO｜product：CFO 說明商業與不動產收入首度突破 20 億歐元。（原話："this is the first year in which we were able to exceed"）
- 2026-02-25｜CFO｜product：CFO 說明免稅有一個分區營收仍比最低保證租金（MAG）短少約 10%。（原話："And we were short by around 10% in"）
- 2026-02-25｜CFO｜product：CFO 報告 VIP 貴賓室服務總營收成長 31.5% 至 1.04 億歐元。（原話："by 31.5%, reaching to EUR 104 million."）
- 2026-02-25｜CEO｜guidance：管理層表示新廣告標案的財務影響要到 2028 年才反映。（原話："would really happen in 2028"）
- 2026-02-25｜CEO｜guidance：管理層表示巴塞隆納餐飲標案的財務影響將在 2026 年反映。（原話："will be seen in 2026 because of all the MAGs"）
- 2026-02-25｜CEO｜guidance：管理層對 2026 年免稅表現表示有信心，將反映帕爾馬新店開幕。（原話："We are confident that a duty-free line for 2026"）
- 2026-02-25｜CEO｜customer：管理層說明特許零售店受電商衝擊最大。（原話："because of disruption of e-commerce, et cetera."）
- 2026-02-25｜CEO｜margin：管理層說明免稅第四季表現較弱，部分來自年底 MAG 的會計調整。（原話："There might be some accounting adjustment"）
- 2026-02-25｜CFO｜margin：CFO 說明航空收入稀釋金額未來將回收。（原話："will be recovered in a couple of years"）
- 2026-02-25｜CFO｜capital_allocation：CFO 說明 Luton 目前承諾的資本支出以維護為主，限制有限。（原話："So limited CapEx on that front."）
- 2026-02-25｜CFO｜capital_allocation：CFO 說明是否參與 Luton 擴建尚未談定。（原話："it has not been resolved yet."）
- 2026-02-25｜CFO｜commitment：CFO 說明巴西 Congonhas 機場工程預定 2028 年 6 月完成。（原話："deliver all those construction works in June 2028"）
- 2026-02-25｜CEO｜risk：CEO 對政治干預風險表示有信心不會再發生。（原話："I'm very confident that this won't happen again"）
- 2026-02-25｜CFO｜risk：CFO 回答 AI 對客流影響時表示管理層會持續追蹤。（原話："it is something that as a company, we are following"）

### AENA_Shareholder_Analyst_Call_Aena_S_M_E_S_A_20260416.md
- 2026-04-16｜Maurici Betriu｜guidance：管理層重述西班牙網絡 2026 年客運量公開預測（原話："traffic increase in Spain is of 1.3% in terms of passengers"）
- 2026-04-16｜Maurici Betriu｜guidance：管理層表示地緣與經濟不確定性消退後須重新評估該預測（原話："we will need to reassess that forecast"）
- 2026-04-16｜Maurici Betriu｜guidance：管理層預期未來數年西班牙客運成長較近年和緩（原話："it is to be expected that there will be more moderate growth"）
- 2026-04-16｜Maurici Betriu｜guidance：DORA III 提案載明 2031 年西班牙機場客運量預測（原文數字如此）（原話："a focus of 1.69 billion passengers in"）
- 2026-04-16｜Maurici Betriu｜guidance：DORA III 提案營運費用年增率（原話："an increase of OpEx of 3.8% per"）
- 2026-04-16｜Maurici Betriu｜guidance：DORA III 提案 WACC（原話："Aena proposes a 9%."）
- 2026-04-16｜Maurici Betriu｜guidance：DORA III 提案每位旅客平均費率調升幅度（原話："increasing airport fees for on average by EUR 0.43"）
- 2026-04-16｜Maurici Betriu｜guidance：DORA III 尚待內閣核准，管理層預期會有修改（原話："which probably will undergo some modifications"）
- 2026-04-16｜Maurici Betriu｜guidance：2026 Q1 業績發布時點（原話："we will be presenting the results of the first quarter"）
- 2026-04-16｜Maurici Betriu｜margin：2025 合併 EBITDA margin 口徑：合併而非單體（原話："margin, not the stand-alone margin, was 59.3%"）
- 2026-04-16｜Maurici Betriu｜margin：2025 營運費用年增，列舉驅動項（原話："11% increase versus 2024, driven by personnel, services"）
- 2026-04-16｜Maurici Betriu｜margin：商業與不動產收入首度超過 20 億歐元（原話："Group exceeded EUR 2 billion, which is a significant figure"）
- 2026-04-16｜Maurici Betriu｜margin：不動產收入年增與驅動項（原話："revenues of 10.5%, driven by air cargo activity"）
- 2026-04-16｜Maurici Betriu｜margin：2025 淨利與年增幅（原話："almost EUR 2,136.7 million, 10.5% higher than in 2024"）
- 2026-04-16｜Maurici Betriu｜margin：國際業務占合併 EBITDA 比重（原話："international activity represented more than 10% of"）
- 2026-04-16｜Maurici Betriu｜margin：管理層說明 DORA III 營運費用增加的理由之一：新投資週期（原話："We need more human resources for the new investment cycle"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：DORA III 五年總投資規模（原話："a total investment of nearly EUR 13 billion"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：DORA III 受管制年投資相對 DORA I/II 法定上限的倍數（原話："4.4x the current legal maximum investment of DORA I"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：2025 淨財務負債對 EBITDA（原話："decreased to 1.31x in 2025"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：管理層稱財務體質為新投資週期起點（原話："starting point for the new investment cycle"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：建議 2025 年度股利與年增幅（原話："2025 earnings, 11.7% more than last year"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：發行 10 年期公司債（原話："successful issuance of a 10-year Aena bond in"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：巴西第二特許權債券融資（原話："debenture issue worth BRL 5.3 billion underwritten by"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：國際併購紀律：選擇性新增資產（原話："selective addition of new international assets based on"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：宣布收購 Leeds Bradford 與 Newcastle 持股公司（原話："acquisition of 51% stake in a new holding company that owns"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：取得里約 Galeão 特許權（原話："the award of the 13-year concession for"）
- 2026-04-16｜Maurici Betriu｜commitment：管理層承諾維持 80% 派息率（原話："payout ratio of 80% of net income"）
- 2026-04-16｜Maurici Betriu｜commitment：管理層希望在年底前的策略計畫中確認派息率（原話："we hope to be able to confirm this in the strategic plan"）
- 2026-04-16｜Maurici Betriu｜commitment：管理層對投資計畫與債務成本的信心表述（原話："I am confident that in the coming years, Aena will be able"）
- 2026-04-16｜Maurici Betriu｜commitment：光電計畫 2029 年目標及進度慢於先前說法（原話："produce renewable energy equivalent to 51% of Aena's 2019"）
- 2026-04-16｜Maurici Betriu｜competition：航空公司壓低機場費率的壓力；管理層稱之為不負責任（原話："the irresponsible pressure backed by"）
- 2026-04-16｜Maurici Betriu｜competition：費率修正案曾試圖凍結 DORA III 期間機場費（原話："sought to arbitrarily freeze airport fees"）
- 2026-04-16｜Maurici Betriu｜competition：管理層引用 2015–2025 實質費率降幅（原話："a 37% drop in airport fees in 11 years in real"）
- 2026-04-16｜Maurici Betriu｜customer：管理層引用 IATA 資料：歐洲航空公司每位旅客收入增幅（原話："increased by almost 27%, i.e., EUR 40 per person"）
- 2026-04-16｜Maurici Betriu｜customer：西班牙國內線客運 2025 年幾乎持平（原話："national traffic was virtually flat"）
- 2026-04-16｜Maurici Betriu｜risk：管理層表示部分自治區要求共管機場構成重大風險（原話："pose significant risks for the Spanish airport system"）
- 2026-04-16｜Maurici Betriu｜risk：巴斯克雙邊機場機構僅屬諮詢性質（管理層說法）（原話："is strictly consultative and not a"）
- 2026-04-16｜Maurici Betriu｜risk：西班牙客運成長受部分基礎設施容量限制（原話："constraints in some of Aena's infrastructure that could"）
- 2026-04-16｜Maurici Betriu｜risk：中東戰爭對航空的直接影響目前小（原話："the direct impact of the war in Iran and the Middle East"）
- 2026-04-16｜Maurici Betriu｜risk：DORA III 期間債務上升後對總經變動更敏感（原話："we will be more exposed in the future years to macroeconomic"）
- 2026-04-16｜Maurici Betriu｜risk：累計費率缺口（交通量風險由 Aena 承擔）（原話："Aena bears the so-called traffic risk"）
- 2026-04-16｜Maurici Betriu｜risk：累計收入缺口金額（原話："accumulated by and exceeds EUR 550 million"）
- 2026-04-16｜Maurici Betriu｜product：管理層首度提到 AI 可能聚焦 Aena 管理（原話："AI will focus on the management of Aena"）
- 2026-04-16｜Maurici Betriu｜product：光電計畫速度慢於兩年前說法，歸因外部因素（原話："we said that we would have wanted that"）

### AENA_2026_20260729.md
- 2026-07-29｜Executive Vice Chairman (Marin)｜guidance：2026 西班牙網絡旅客成長管理層估約 3%（原話："could be around 3% compared with 2025."）
- 2026-07-29｜Executive Vice Chairman (Marin)｜risk：管理層稱對 2026 冬季季無能見度（原話："we still don't have visibility on the 2026 winter season"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜risk：管理層稱載客率弱於座位運能成長（原話："we are observing weaker load factors"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜competition：荷莫茲危機後旅客轉向西班牙（原話："a diversion of traffic towards Spain has been observed as"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜margin：報告 EBITDA 利潤率 54.5% 對 56.5%（原話："The reported EBITDA margin was 54.5% compared with 56.5%"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜margin：排除 IFRIC 12 與 Luton 保險補償後可比 EBITDA 利潤率（原話："the comparable EBITDA margin would have been 56.9%"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜guidance：DORA III 最終由部長會議核准時程（原話："final DORA by the Council of Ministers by 30 September 2026"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜capital_allocation：Rio de Janeiro 機場收購金額（原話："equivalent to approximately EUR 490 million"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜product：首批機場酒店地面權授標（原話："first hotel developments within the Spanish airport network"）
- 2026-07-29｜CFO (Castejon)｜guidance：下半年成本增幅預期與上半年相近（原話："we don't see reasons to have cost increases materially"）
- 2026-07-29｜CFO (Castejon)｜margin：管理層拆解上半年母公司其他營運費用增項（原話："related to maintenance, 21.5% increase"）
- 2026-07-29｜CFO (Castejon)｜margin：商業總業務每旅客成長數字（原話："total business per pax of 5.4% this quarter and 4.7%"）
- 2026-07-29｜CFO (Castejon)｜customer：特許店新標 MAG 較 2025 增幅（原話："The award MAGs implied an increase versus 2025 of 82%"）
- 2026-07-29｜CFO (Castejon)｜customer：F&B 新標 MAG 增幅（原話："MAG increases of 11% for 2027 and 37% for 2028"）
- 2026-07-29｜CFO (Castejon)｜customer：免稅帳列收入大致持平（原話："reported duty-free revenue was broadly flat"）
- 2026-07-29｜CFO (Castejon)｜customer：僅加那利群島免稅標超過 MAG（原話："The one in Canary Islands is above."）
- 2026-07-29｜CFO (Castejon)｜customer：馬德里與加泰隆尼亞免稅仍遠離 MAG（原話："Madrid and Catalonia, we are still far from being able"）
- 2026-07-29｜CFO (Castejon)｜risk：出入境系統可能壓抑地中海沿岸免稅表現（原話："duty-free business might have been impacted"）
- 2026-07-29｜CFO (Castejon)｜customer：VIP 服務定價能力（原話："We still have pricing power in many fronts."）
- 2026-07-29｜CFO (Castejon)｜capital_allocation：非管制 CapEx 約 30 億主要用於停車場擴容（原話："those EUR 3 billion are mainly explained by car parks"）
- 2026-07-29｜CFO (Castejon)｜commitment：股利政策 80% 配息不偏離（原話："dividend policy of 80% of payout"）
- 2026-07-29｜CFO (Castejon)｜commitment：DORA 後才更新股利政策（原話："we'll have a whole new set of plans for the company."）
- 2026-07-29｜CFO (Castejon)｜commitment：不預期信用評級惡化（原話："we are not expecting a deterioration or deviation from the"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜commitment：策略計畫年底前完成（原話："we'll be done before the end of the year"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜guidance：K、P 因子將在策略計畫前公布（原話："you will know those figures before the strategic plan"）
- 2026-07-29｜CFO (Castejon)｜risk：P 因子不一定能 100% 轉嫁通膨（原話："we are not completely optimistic of being able to"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜capital_allocation：CapEx 計畫總額 130 億（原話："our CapEx program will be EUR 13 billion"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜risk：管制 CapEx 超支由 Aena 承擔（原話："if we increase that, it's on our side"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜risk：未投滿 100 億須退回 DORA IV（原話："we'll have to give that money back to"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜guidance：2027 起基期較高但長期成長率受限（原話："we'll start at a higher level in 2027"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜capital_allocation：目前不看新併購（原話："we are not looking at any operation"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜risk：巴塞隆納擴建的行政核准不由 Aena 掌控（原話："many approvals that do not depend on Aena"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜competition：對 Ryanair 公開批評（原話："They are never happy with airport charges."）
- 2026-07-29｜Executive Vice Chairman (Marin)｜competition：Barajas 環境許可容量（原話："to grow up to 120 operations per hour"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜competition：對 easyJet 可能被收購（原話："we are not concerned about that at this"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜risk：新冠 MAG 租金爭議（原話："It's not illegal what we are doing."）
- 2026-07-29｜CFO (Castejon)｜margin：Luton 利潤率下滑原因（原話："the end of the special force majeure"）
- 2026-07-29｜CFO (Castejon)｜margin：ANB 利潤率（原話："the EBITDA margin improved as well, from 58% to 60%"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜commitment：Congonhas 工程完工時程（原話："The completion, as I have said, for the Congonhas airport"）
- 2026-07-29｜CFO (Castejon)｜capital_allocation：淨負債/EBITDA 上升原因含股利（原話："EUR 1.6 billion going to our shareholders."）
- 2026-07-29｜Executive Vice Chairman (Marin)｜commitment：對 DGAC 不施壓（原話："we must not press the regulator in this process"）
- 2026-07-29｜CFO (Castejon)｜risk：商業營運商壞帳準備（原話："bad debt provisions that we have to"）

### AENA_Shareholder_Analyst_Call_Aena_S_M_E_S_A_20260921.md
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜guidance：DORA III（2027–2031）核定 WACC 為 2.32%（原話："has been finally set at 2.32%"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜guidance：DORA III 年均機場收費漲幅 0.33%（原話："the average annual airport charges increase will be 0.33%"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜guidance：DORA 假設西班牙機場網絡 2031 年旅客數達 3.63 億（原話："will reach 363 million passengers in 2031"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜capital_allocation：核定受管制投資計畫接近 100 億歐元（原話："regulated investment plan amounts to almost EUR 10 billion"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜capital_allocation：含非受管制商業投資，總投資接近 130 億歐元（原話："the total investment will reach almost EUR 13 billion"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜margin：DORA III 受管制成本以2026年固定價格計，2027年19.29億歐元升至2031年20.79億歐元（原話："from EUR 1,929 million in 2027 to EUR 2,079 million in 2031"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜margin：2025年受管制成本為16.5億歐元，DORA III起點重設至19.29億（原話："the figure was EUR 1,650 million"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜margin：管理層解釋成本重設原因：環保、安全、資安規範趨嚴與通膨、基本工資上調（原話："So doing the same costs more money"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜margin：受管制OpEx對ATU比率年增近2%（原話："the ratio of OpEx to ATUs will increase almost 2% annually"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜commitment：新策略計畫（2027–2031）將於年底前發布（原話："before the end of the year, our new strategic plan"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜commitment：董事長預告策略計畫中的財務目標企圖心偏高（原話："I can anticipate will be high in many of the financial targets"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜risk：管理層列出兩大優先事項：OpEx 與 CapEx 執行，並稱兩者與過往 DORA 明顯不同（原話："One is OpEx. Two is the CapEx execution."）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜risk：董事長形容本期 DORA 具挑戰性與高要求（原話："it is challenging, it is demanding"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜capital_allocation：董事長稱核定投資使受管制業務價值提高，但需達成各項要求才能實現（原話："Aena's value is higher after the approval of DORA III"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜capital_allocation：管理層表示投資增加將使債務大幅上升（原話："Our debt will increase significantly."）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜product：馬德里與巴塞隆納主要擴建多數在 DORA IV 交付，容量全面釋放在 DORA IV（原話："the whole capacity will be delivered in DORA IV"）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜commitment：管理層承諾投資不超過核定的 100 億歐元（原話："We are not going to invest more than it has been approved"）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜capital_allocation：彈性工具：各機場只需執行核定投資額的 80%（原話："to comply with 80% of the investment that has been approved"）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜risk：策略性投資占 CapEx 計畫 40%–50%，須依時程執行（原話："between 40% and 50% of the CapEx program"）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜risk：策略性投資未達標可能受罰，因此超支時先動非策略項目（原話："you can receive a penalty"）
- 2026-09-21｜CFO (Ignacio Castejón)｜risk：已發包的 CapEx 比例仍很低（原話："It's still very low, still very low."）
- 2026-09-21｜CFO (Ignacio Castejón)｜commitment：CFO稱公司工程招標一向要求固定價格（原話："with fixed prices in order to avoid last-minute surprises"）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜risk：Tenerife South 航廈標案無人投標，技術部指市場評估的風險高於預期（原話："the risk that the market has assessed in this project"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜risk：董事長承認 Tenerife 流標不是好消息，但稱因國家持股透明度才被公開（原話："it leaves you a bad taste in the mouth"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜risk：董事長稱 Tenerife 流標情況並不令人擔憂（原話："this is not worrying"）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜guidance：通膨保護沿用法規定義的 P 因子；過渡期 1% 上限已不適用（原話："Now those limitations do not apply at this moment."）
- 2026-09-21｜CFO (Ignacio Castejón)｜capital_allocation：非受管制 CapEx 的節奏請比照受管制 CapEx 建模，其餘留待策略計畫（原話："expect something similar to regulated CapEx"）
- 2026-09-21｜CFO (Ignacio Castejón)｜risk：CFO稱將檢視公司提交的OpEx假設與核定版差異，並指出有履約不及的高風險項目（原話："a high risk of not being able to perform"）
- 2026-09-21｜Carlos Gallego (IR)｜commitment：下次財報為10月底的2026前9個月業績（原話："at the end of October"）

### 問答異常語氣（迴避／改口／保留）
- AENA_2025_Earnings_Call_20260225.md｜問：JPMorgan 請管理層給出 2026 與 DORA III 期間 OpEx 增幅的量級與分項拆分。｜答法：CFO 回顧 2025 年人事與其他營運費用的成因，說趨勢會延續，但未給 2026 年或 DORA III 的 OpEx 增幅數字。
- AENA_2025_Earnings_Call_20260225.md｜問：BNP 追問 2026 年航空業務 D&A 預期。｜答法：CFO 先回答折舊節省『顯著低於 6,800 萬歐元』，被追問後才改說總 D&A 水準與 2025 年相近，首答與提問口徑不一致。
- AENA_2025_Earnings_Call_20260225.md｜問：UBS 問 DORA III 客流預測是否納入 AI 導致白領失業的風險，以及是否與監管機關討論。｜答法：管理層未直接回答預測是否納入，改談市場情緒，並稱與監管機關的討論保密，不透露細節。
- AENA_2025_Earnings_Call_20260225.md｜問：Santander 問免稅與特許零售店每位旅客營收放緩的趨勢。｜答法：管理層回應偏向解釋（會計調整、淡季、電商），未提供每位旅客營收的具體數字。
- AENA_2026_20260729.md｜問：Bank of America 問 2027 關稅 K 因子與 P 因子最佳估計｜答法：說有內部計算但因程序不能公布，不給數字
- AENA_2026_20260729.md｜問：UBS 問固定加變動股利及 Aena S.M.E 可接受的最高槓桿｜答法：不給槓桿上限數字，推到 DORA 後的策略計畫
- AENA_2026_20260729.md｜問：Santander 問 2028 P 因子是否反映今年約 10% 的西班牙 OpEx 通膨｜答法：表示不願斷言轉嫁，未給估計
- AENA_Shareholder_Analyst_Call_Aena_S_M_E_S_A_20260921.md｜問：Bernstein：最終核定成本比初始假設低約10%，是否意外、差異在哪、如何控制成本｜答法：CFO 只回答 CapEx 招標部分，OpEx 差異未給數字，延後到策略計畫（請「給我們幾週」）
- AENA_Shareholder_Analyst_Call_Aena_S_M_E_S_A_20260921.md｜問：Jefferies：非受管制 CapEx 的節奏與零售投資的價值上行時點｜答法：CFO 表示留待策略計畫，只給 CapEx 節奏類似受管制一句，未回答價值上行
- AENA_Shareholder_Analyst_Call_Aena_S_M_E_S_A_20260921.md｜問：Deutsche Bank：已發包 CapEx 佔比｜答法：只答「still very low」，未給百分比
- AENA_Shareholder_Analyst_Call_Aena_S_M_E_S_A_20260921.md｜問：BNP：標價高於預期時 100 億總額是否增加或順延至 DORA IV｜答法：回答不超投資，但同時承認價格、部分專案仍有不確定性，並稱可能將部分投資延至 DORA IV

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

## ⑥ 條件附卡（archetype_hint='受監管公用/穩定內需' 命中）：judge_addendum_archetype.md

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
{"date":"20260711","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"非監管商業 + 巴西驅動非受管制成長，抵消受監管關稅被壓的逆風","columns":{"2Y 驗證點":"商業 RPP > €6.5、巴西 EBITDA 貢獻起量","5Y 驗證點":"商業 RPP ≥ €7.5、巴西成集團 15%+ EBITDA","10Y 驗證點":"非監管收入占比由 ~35% 升至 45%+","具體數字門檻":"商業 RPP ≥ €6.5（FY2025 €6.07 起點）；巴西 2025-2028 capex 投產","信息來源":"AENA FY2025 年報（2026-02-25）；Q1 2026（2026-04-29）；Moodie Davitt 商業追蹤","漂移觸發條件":"連 2 季商業 RPP YoY"}},{"id":"H2","text":"DORA III 政府終裁不惡化到破壞回報——年化關稅路徑 ≥ 持平（非 CNMC 建議的 −0.59%/年）","columns":{"2Y 驗證點":"2026-09-30 部長會議終裁","5Y 驗證點":"2027-2031 IMAP 實際軌跡","10Y 驗證點":"DORA IV（2032+）延續可預測回報","具體數字門檻":"年化 IMAP ≥ 持平；紅線＝","信息來源":"CNMC 官方（cnmc.es）；AENA DORA III 新聞稿；部長會議紀錄","漂移觸發條件":"政府採 CNMC 降價路徑且 AENA/TCI 敗訴無救濟 → 反轉"}},{"id":"H3","text":"估值不進一步 de-rate——股息複利 + 個位數 EPS 成長維持 ~8% 總回報","columns":{"2Y 驗證點":"Fwd PE 守 16-17x、殖利率 4%+","5Y 驗證點":"股息年增 ~5-8%、payout ~70-80%","10Y 驗證點":"DDM 隱含價值隨 rate base 成長","具體數字門檻":"Fwd PE ≥ 15x 且殖利率 4-5%；股息不中止","信息來源":"yfinance 共識；JPM/BofA/Jefferies 評等；歷史殖利率區間","漂移觸發條件":"股息政策中止或 capex 排擠分紅 → 削弱 H3"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"歐元區/西班牙觀光需求衝擊（衰退、地緣、恐攻）→ 月度旅客急跌；疊加 overtourism 政策反制（Barcelona 旅遊稅 2026-04 翻倍至 €10-15/晚、短租 2028 前淘汰、Balearic 尖峰季 €15/晚），壓縮平價/長停旅客消費，直擊 H1 商業 RPP 引擎","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"西班牙月度旅客 YoY（INE + AENA 月報）；商業 RPP 環比","警戒閾值":"連 3 月旅客 YoY −5% → 監控部位；連 3 月 −10% → 減碼"}},{"id":"R2","text":"DORA III 政府終裁採 CNMC 降價路徑（或 PP 凍結案通過）——年化關稅","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"CNMC/部長會議公告；後續 Audiencia Nacional 訴訟 docket","警戒閾值":"年化裁定"}},{"id":"R3","text":"航空去碳化：EU ETS 2026 起航空全額拍賣碳權（免費配額歸零），航司 opex +4-6%，疊加關稅爭議放大航司對邊緣航線的取捨 → 長期歐洲 traffic CAGR 下修","columns":{"對應假設":"H1/H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"EU ETS 航空政策；IATA 長期 traffic 預測；SAF 成本","警戒閾值":"IATA 歐洲 10Y traffic CAGR 下修至"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"DORA III 政府終裁允許 ≥ 持平關稅路徑（2026-09-30 前）且訴訟風險釐清，或股價回落至 €24 以下（Fwd PE ≤15x）","irr_base_pct":8.0,"ev5y_pct":43.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":5.7,"ev5y_pct":43.0,"irr_base_pct":8.0,"max_dd_pct":-38.0,"bull_5y_price":49.8,"bear_5y_price":22.1,"p_bull_pct":32.0,"p_bear_pct":23.0,"rearm_trigger":"DORA III 政府終裁允許 ≥ 持平關稅路徑（2026-09-30 前）且訴訟風險釐清，或股價回落至 €24 以下（Fwd PE ≤15x）","price_at_dd":26.94,"archetype":"受監管公用/穩定內需","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AENA_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
