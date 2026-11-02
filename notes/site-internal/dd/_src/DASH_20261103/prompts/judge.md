你是 stock-analyst **v20 判斷 agent**，標的 DASH（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"DASH","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DASH_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DASH_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":4616,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results"},"note":"未查得可靠共識數字，不填"},{"id":"f_kpi1_gaap","label":"GAAP 營業利益 / 利益率","value":442,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（利益率 9.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results"},"note":"未查得，不填"},{"id":"f_kpi2_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（公司未報 Non-GAAP 營業利益，以此替代）","value":1060,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（占 GOV 3.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results"},"note":"未查得，不填"},{"id":"f_kpi5_q4_2026_marketplace_gov","label":"Q4 2026 指引：Marketplace GOV","value":"35.4–36.4","period":"Q3 FY2026 財報（公告於 2026-10-29）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026 財報（公告於 2026-10-29）","citation":"公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results"},"note":"未查得，不填"},{"id":"f_kpi6_q4_2026_adjusted_ebitda","label":"Q4 2026 指引：Adjusted EBITDA","value":"900–1,100","period":"Q3 FY2026 財報（公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026 財報（公告於 2026-10-29）","citation":"公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results"},"note":"未查得，不填"},{"id":"f_kpi7","label":"總訂單數","value":993,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results"},"note":"未查得，不填"},{"id":"f_kpi8_marketplace_gov","label":"Marketplace GOV","value":33.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results"},"note":"未查得，不填"},{"id":"f_kpi9_net_revenue_margin_take_","label":"Net Revenue Margin（take rate）","value":13.6,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_dash_gross_margin_pct","label":"DASH 毛利率","value":51.51,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DASH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_dash_operating_margin_pct","label":"DASH 營業利益率","value":4.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DASH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_dash_fcf_margin_pct","label":"DASH FCF 利潤率","value":11.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DASH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_uber_gross_margin_pct","label":"UBER 毛利率","value":42.31,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UBER.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_uber_operating_margin_pct","label":"UBER 營業利益率","value":12.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UBER.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_uber_fcf_margin_pct","label":"UBER FCF 利潤率","value":18.32,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UBER.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cart_gross_margin_pct","label":"CART 毛利率","value":72.23,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CART.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cart_operating_margin_pct","label":"CART 營業利益率","value":13.88,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CART.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cart_fcf_margin_pct","label":"CART FCF 利潤率","value":29.6,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CART.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":787,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（占營收約 17.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results"},"note":"未查得，不填"},{"id":"f_kpi4_sbc_gaap","label":"SBC（含部分薪資稅）占營收 / 占 GAAP 營業利益","value":269,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（占營收 5.8%；占 GAAP 營業利益約 61%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 Adjusted EBITDA 調節表（數字含部分薪資稅，非純 SBC；占比為本 agent 以 269/4616、269/442 換算）"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":189.32,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":9.67,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":52.29,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-1.36,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.87 → 5.79）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-1.94,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.25 → 8.09）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-1.88,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.12 → 9.93）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.79,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":8.09,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":9.93,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":3.95,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 5.57 → 5.79（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":78.56,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"2 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.84,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝49.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":49.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.68,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝48.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":48.9,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":32.7,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 5.79，分子＝快照價 189.32","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-2684.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 3298.0、現金 5982.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":435.98,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":79857.22,"period":"2026-11-03","unit":"USD m","basis":"市值 82541.22 ＋ 淨負債 -2684.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":17950.57,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（37 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":21692.94,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（42 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.45,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 189.08 / W52 188.7 / W104 200.5 / W250 135.39 / W250 13週斜率 0.62%"},{"id":"f_ma_w52","label":"52 週均線","value":188.7,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":200.5,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":135.39,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.62,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列示的競爭對手為 Amazon、Uber Eats、Prosus、Delivery Hero 與在地業者；本地外送業務分散且競爭激烈。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm","excerpt":"Globally, we compete with other local on-demand delivery companies, including Amazon, Uber Eats, Prosus, Delivery Hero, and other local incumbents.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：切換成本低，消費者與商家可多平台並用；競爭壓力已迫使公司調整佣金、費用與促銷，對財務表現造成負面影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm","excerpt":"It is relatively easy to switch between offerings in our industry. Consumers have a propensity to shift based on cost, quality, and selection and could use more than one local commerce platform","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：他業公司正開發自動化／無人機配送技術，可能以此與公司競爭，對手可能先於公司規模化。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm","excerpt":"companies operating in different industries are developing and have begun implementing autonomous technologies, and we believe that they may use these technologies to compete with us in the delivery or logistics industries.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q1 2026 財報摘要稱 DoorDash 在幾乎所有市場獲得份額（第三方分析，非公司申報）。","source":"AlphaSense DoorDash Earnings Q1 2026 Analysis","url":"https://www.alpha-sense.com/earnings/dash/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"DoorDash 擬以約 170 億美元收購 Instacart，AELP 要求監管機關阻止（掌握近 60% 第三方雜貨外送市場）。","source":"Local news: DoorDash is buying Instacart for $17 billion","url":"https://www.ktnv.com/business/company-news/doordash-is-buying-instacart-for-17-billion-creating-a-food-delivery-giant","excerpt":"But there’s already opposition to the deal, with the American Economic Liberties Project (AELP), an anti-monopoly advocacy group, pushing regulators to block the deal because it would control nearly 60% of the third-party grocery delivery market.","as_of":"2026-10-29","retrieved_at":"20261103","affects":["moat_trend","triggers"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K：2023–2025 年無任何客戶占營收 10% 以上；應收帳款中單一實體占比 2024 年底 13%、2025 年底 12%。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm","excerpt":"As of December 31, 2024, one entity individually accounted for 13% of accounts receivable, net. As of December 31, 2025, one entity individually accounted for 12% of accounts receivable, net. No customer accounted for 10% or more of revenue for the years ended December 31, 2023, 2024, and 2025.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"10-Q 2026-06-30：遵守信貸協議 covenant，無循環借款，信用狀 $117M；6/30 後全面修訂重述協議。","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0001792789/000179278926000050/dash-20260630.htm","excerpt":"Agreement with certain lenders, which, as previously amended and restated on April 26, 2024, provided for an $800 million unsecured revolving credit facility maturing on April 26, 2029, with a sublimit for the issuance of letters of credit in an aggregate face amount of up to $600 million. As of June 30, 2026, we were in compliance with the covenants under the Existing Credit Agreement.","as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"DoorDash Q1 2026 beat; Q2 2026 GOV guidance $32.4B-$33.4B vs ~$31.8B analyst expectation; CFO said demand patterns good; analyst view cites demand durability across grocery and retail. Risk: ~$50M/quarter fuel reimbursement drag.","source":"Invezz, DoorDash stock jumps 11% after earnings beat and strong delivery demand","url":"https://invezz.com/ca/news/2026/05/07/doordash-stock-jumps-11percent-after-earnings-beat-and-strong-delivery-demand/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"US online food delivery market estimated ~$34.88B in 2025; Ken Research projects $58.30B by 2031 (~8.9% CAGR); no single 2027-2028 consensus found.","source":"Ken Research, USA Online Food Delivery Market","url":"https://www.kenresearch.com/industry-reports/usa-online-food-delivery-market.md","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 揭露：2025年2月 Uber 在加州州法院提告，指控 DoorDash 部分商業做法違反競爭法；部分轄區競爭主管機關曾詢問或調查其定價條款，個別轄區已有決定。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm","excerpt":"For example, in February 2025, Uber filed a lawsuit in California state court alleging that certain of our business practices are anticompetitive. In addition, competition authorities in some of the jurisdictions in which we operate have made queries regarding, or investigated, our pricing-related terms or other practices","as_of":"2026-02-18","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 揭露：加州 EDD 就薪資稅審計並於2023年1月發出不利評定，公司提出上訴並已提列應計；另有多個轄區的政府調查與詢問。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm","excerpt":"we are currently under audit by the Employment Development Department of the State of California (the \"CA EDD\") for payroll tax liabilities. In January 2023, the CA EDD issued a negative assessment in connection with such audit.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"MLex：DoorDash 約170億美元收購 Instacart 可能遭美國聯邦與州反壟斷機關深度調查","source":"MLex","url":"https://www.mlex.com/mlex/articles/2544720/doordash-instacart-likely-to-get-in-depth-us-state-federal-antitrust-reviews","excerpt":"Antitrust Artificial Intelligence Data Privacy and Security DealRisk® Energy Financial Crime Financial Services Intellectual Property Mergers and Acquisitions State Aid Technology Trade GDPR Enforcement Tracker TAKE A FREE TRIAL Toggle Dropdown Advanced Search DoorDash, Instacart likely to get in-depth US state, federal reviews","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"DoorDash 若因反壟斷障礙無法完成併購，須付 Instacart 12.5億美元終止費","source":"DoorDash 10-Q (2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001792789/000179278926000070/dash-20260930.htm","excerpt":"The transaction is expected to close in the end of 2027 or the first half of 2028, subject to approval by Instacart stockholders, the expiration or termination of the waiting period under the Hart-Scott-Rodino Antitrust Improvements Act of 1976, other regulatory approvals, including in Canada and Israel, and other customary","as_of":"2026-11-01","retrieved_at":"20261103","affects":["thesis.R","valuation","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"DoorDash 10-K（FY2025）風險因子僅一般性提及國際擴張涉及出口管制與貿易制裁（OFAC、歐盟）合規風險，未點名關稅或實體清單對其產品／供應鏈的具體暴露。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm","excerpt":"international expansion may subject our business to broader economic, political, and other international risks, including economic volatility, security risks, and geopolitical conflicts, and may increase our risks in complying with various laws and standards, including with respect to anti-corruption, anti-bribery, export controls, and trade and economic sanctions, such as U.S. Office of Foreign Assets Control sanctions and similar European Union (\"EU\") sanctions.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"分析師文章（非公司揭露）稱 2026 年主要逆風為全球關稅，美國有效關稅率 13-17%，壓抑可自由支配支出。","source":"Finterra／FinancialContent：The New Era of Local Commerce: A Deep Dive into DoorDash (DASH) and the Global Tariff Shock","url":"https://markets.financialcontent.com/stocks/article/finterra-2026-2-24-the-new-era-of-local-commerce-a-deep-dive-into-doordash-dash-and-the-global-tariff-shock","excerpt":"The primary headwind in 2026 is the impact of global tariffs. With effective US tariff rates reaching 13-17% following recent trade disputes, the \"discretionary dollar\" is under pressure.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露：部分營運地區鄰近俄羅斯，增加遵循貿易與制裁規範的難度（地緣風險屬法遵面，非實體供應鏈）","source":"DoorDash FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm","excerpt":"operations in jurisdictions that are in close proximity to Russia increase the difficulty in complying with trade and economic sanction regimes","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2022 10-K 舉例：哈薩克動亂迫使子公司 Wolt 暫停當地營運","source":"DoorDash FY2022 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1792789/000162828023005131/dash-20221231.htm","excerpt":"civil unrest in Kazakhstan required Wolt to temporally suspend its business operations in the country","as_of":"2023-02-17","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"DoorDash 自研送貨機器人 Dot，發表時公司表示仍在評估製造地與零組件來源，未揭露生產地","source":"TechSpot / 搜尋摘要：DoorDash expands autonomous delivery with four-wheeled Dot robot","url":"https://www.techspot.com/news/109696-doordash-expands-autonomous-delivery-four-wheeled-dot-robot.html","excerpt":"is still evaluating where the robots will be manufactured and how components will be sourced","as_of":"2025-10-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026（2026-10-29 公布）：總訂單 9.93 億筆、年增 28%（排除 Deliveroo 為 17%）；Marketplace GOV 約 339 億美元、年增 36%（排除 Deliveroo 為 23%）；營收約 46 億美元、年增 34%（排除 Deliveroo 約 23%）；Deliveroo 貢獻營收 3.65 億美元。自 2026 Q4 起不再揭露排除 Deliveroo 的數字。","source":"DoorDash Q3 2026 earnings press release / SEC 8-K ex99.1（經搜尋摘要轉述，未讀原頁）","url":"https://www.sec.gov/Archives/edgar/data/0001792789/000179278926000062/proddashex991-pressrelease.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Consumer Edge 刷卡資料：DoorDash 在主要外送 app 的消費占比由 2021 Q2 的 44% 升至 2026 Q3 的 59%；Uber Eats 16%→18%；Instacart 26%→18%（含全部外送品類）。","source":"AP 報導（WAFB 轉載）DoorDash to buy Instacart for $17 billion","url":"https://www.wafb.com/2026/10/29/doordash-buy-instacart-17-billion-big-consolidation-grocery-delivery/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"DoorDash 宣布以 170 億美元收購 Instacart（AP，2026-10-29），Instacart 客戶將可使用 DoorDash 另外涵蓋的 50,000 家店。","source":"AP 報導（WAFB）DoorDash to buy Instacart for $17 billion","url":"https://www.wafb.com/2026/10/29/doordash-buy-instacart-17-billion-big-consolidation-grocery-delivery/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["moat_trend","thesis.R","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"公司指引：2026 Q4 調整後 EBITDA/Marketplace GOV 將季減，主因季節性 Dasher 成本、年度保險費用與全球投資增加（含 Deliveroo，並提示整合風險）；未找到公司 2027 展望。","source":"DoorDash 8-K ex99.1 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001792789/000179278926000048/proddashex991-pressrelease.htm","excerpt":"In H2 2026, we expect Adjusted EBITDA as a percentage of Marketplace GOV to follow a similar pattern to H2 2025, with a Q/Q increase in Q3 2026 followed by a Q/Q decline in Q4 2026.","as_of":"2026-08-05","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 earnings press release：訂單、GOV、營收年增與排除 Deliveroo 數字","source":"DoorDash IR Q3 2026 Earnings Press Release","url":"https://s22.q4cdn.com/280253921/files/content_files/Q3-2026-Earnings-Press-Release.pdf","excerpt":"as a % of Marketplace GOV Weighted-average diluted shares outstanding $ 3,955 13.8 % $ 1,689 27 % $ 31,604 39 % 27 % Net Revenue Margin GAAP gross profit 32 % $ 29,683 6.8 % $ 1,780 5.0 % $ 0.6 % 754 $ 2.4 % 442 200 5.2 % $ 466 0.6 % 1.4 % 914 $ 1,060 2.8 % 3.1 % 439 440 1 Operational Update In Q3 2026, we grew Total Orders 28% Y/Y (17% Y/Y excluding the impact of Deliveroo), Marketplace","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：資源更多的競爭者可能更快回應新興技術與偏好變化，使 DoorDash 平台吸引力下降或過時；並提及消費者可能採用新出現的替代方案，使市場發展不如預期。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm","excerpt":"Greater financial resources and product development capabilities may allow these competitors to respond more quickly and efficiently to new or emerging technologies and changes in merchant, consumer, and Dasher preferences that may render our platform less attractive or obsolete.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"DoorDash 表示 Dasher 仍將是物流骨幹，同時增加地面與空中機器人投資；Dot 預期年底在最大測試市場占高個位數百分比訂單；DoorDash Air 預計2026秋季開始商業配送。","source":"DoorDash 8-K 新聞稿 / Pulse 2.0","url":"https://pulse2.com/doordash-dot-robots-could-handle-a-high-single-digit-share-of-orders-in-largest-test-market-by-year-end/","excerpt":"We expect Dashers to remain the backbone of our logistics network for a very long time, but we are increasing our levels of investment in both our land and air based robots and are optimistic we can continue to make steady progress.”","as_of":"2026-08-16","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"DoorDash 推出 Apple Messages 文字下單 AI 代理；CEO Tony Xu 稱 AI 代理可能處理前幾步，但 DoorDash 能協調整個配送。","source":"The Star: DoorDash debuts text-to-order AI agent that works in Apple Messages","url":"https://www.thestar.com.my/tech/tech-news/2026/10/01/doordash-debuts-text-to-order-ai-agent-that-works-in-applemessages","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"DoorDash CEO 論述不懼 AI 購物代理。","source":"Restaurant Business: why DoorDash isn't afraid of AI shopping agents","url":"https://www.restaurantbusinessonline.com/technology/why-doordash-isnt-afraid-ai-shopping-agents","excerpt":"DoorDash co-founder and CEO Tony Xu tackled that question head-on during an earnings call this week. AI agents, he said, may be able to handle the first few steps of the food delivery process, but DoorDash can orchestrate the whole thing.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 describes two offerings: Marketplaces (DoorDash/Wolt/Deliveroo, with DashPass/Wolt+/Deliveroo Plus memberships, 35M+ members at 2025-12-31) and a Commerce Platform (Drive white-label delivery, online ordering, branded apps) that helps merchants sell on their own channels.","source":"SEC EDGAR 10-K FY2025, Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm","excerpt":"In addition to our Marketplaces, we offer our Commerce Platform, which is a suite of services that help empower merchants to build, operate, and grow their businesses on their own channels. Within our Commerce Platform, we offer white-label delivery fulfillment services (\"Drive\")","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025: substantial majority of revenue still comes from Marketplace orders (commissions and consumer fees); Drive earns per-order fees for fulfilling demand from merchants' own channels. Marketplace remains the main revenue base.","source":"SEC EDGAR 10-K FY2025, Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm","excerpt":"We generate a substantial majority of our revenue from orders completed through our Marketplaces and the related commissions charged to partner merchants and fees charged to consumers.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q2 2026 8-K press release: strategy framed as marketplaces plus services helping merchants sell via their own channels; digital ordering used by 150,000+ merchants with revenue growth over 40% y/y.","source":"SEC 8-K Q2 2026 earnings press release","url":"https://www.sec.gov/Archives/edgar/data/0001792789/000179278926000048/proddashex991-pressrelease.htm","excerpt":"In Q2 2026, we grew new signed venues at SevenRooms by over 100% Y/Y and grew revenue from our digital ordering service, which is being used by over 150,000 merchants, by over 40% Y/Y.","as_of":"2026-08-05","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Bullstory 2026-09-02 資料：42 位分析師平均目標價 $252.30，區間 $172–$350，共識 Buy（該站當日價 $226.15，現價請引 numbers.price_at_dd）","source":"Bullstory DASH price target forecast","url":"https://bullstory.io/en/stocks/dash/forecast/price-target","excerpt":null,"as_of":"2026-09-02","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Tickflow 2026-07-31：36 位分析師共識目標價 $251.71，Buy；MarketBeat 頁面 36 位平均 $256.08、高 $350、低 $185（頁面日期未標示）","source":"Tickflow DASH forecast; MarketBeat DASH price target","url":"https://tickflow.io/stock/DASH/forecast","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"公司 Q3 2026 指引：Marketplace GOV $33.0–34.0B、調整後 EBITDA $950M–1.1B；稱上半年表現優於公司預期；年底商戶付款時點使 2026 FCF 減少 $700–800M；SBC 指引下修至約 $1.2–1.3B（原 $1.3–1.4B）；Deliveroo 2026 約貢獻 $200M EBITDA","source":"DoorDash 8-K 新聞稿 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0001792789/000179278926000048/proddashex991-pressrelease.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 2026 指引 GOV $32.4–33.4B、EBITDA $770–870M；指引 GOV 區間高於部分來源共識（TIKR 共識 $31.8B），EBITDA 中點 $820M 低於約 $825.9M 分析師估值（來源間共識數字不一致）","source":"TIKR / Barchart Q1 2026 摘要","url":"https://www.tikr.com/blog/doordash-stock-analysis-record-membership-grocery-volume-lead-and-a-820-tikr-target","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 實績：EPS $0.46 低於 Zacks 共識 $0.50，營收 $4.45B 高於共識 3.08%；Chartmill 顯示 FY2026 EPS 共識 2.63 美元（45 位分析師，2026-10-24），Q3 營收預估近 3 個月上修 1.88%","source":"Chartmill DASH Q2 earnings / estimates","url":"https://www.chartmill.com/news/external/110247/doordash-inc-dash-q2-earnings-miss-estimates","excerpt":null,"as_of":"2026-10-24","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 2026 指引 GOV $32.4–33.4B、EBITDA $770–870M 與 Dasher gas relief 成本 >$50M","source":"DoorDash 8-K Q1 2026 新聞稿","url":"https://www.sec.gov/Archives/edgar/data/0001792789/000179278926000036/proddashex991-pressrelease.htm","excerpt":"$32.4 billion - $33.4 billion $770 million - $870 million","as_of":"2026-05-06","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-28 DoorDash 與 Instacart（Maplebear）簽署合併協議，每股 Instacart 可選 $65.00 現金或 0.3372 股 DoorDash A 類股（含按比例分配）；媒體報導總值約 $170 億，需 HSR 及加拿大、以色列核准。","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1792789/000114036126041111/ef20084547_8k.htm","excerpt":"On October 28, 2026, DoorDash, Inc., a Nevada corporation (“DoorDash” or the “Company”), entered into an Agreement and Plan of Merger (the “Merger Agreement”) with Maplebear Inc., a Delaware corporation (“Instacart”), and Ibiza Merger Sub, Inc.","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","thesis.R","valuation","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-09-18 DoorDash 完成由 Delaware 改設 Nevada 的重新註冊，業務、管理層不變。","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1792789/000114036126037109/ef20081998_8k.htm","excerpt":"the reincorporation of the Company from the State of Delaware to the State of Nevada (the “Nevada Reincorporation”) became effective on September 18, 2026, at 12:02 a.m. Pacific Time","as_of":"2026-09-18","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-10-28 簽署收購 Instacart 的合併協議（現金 $65.00 或 0.3372 股，可選擇並按比例分配）；預期需 HSR 與加拿大、以色列反壟斷核准，報導預計 2027 年底至 2028 上半年完成。","source":"SEC EDGAR 8-K Item 1.01（2026-10-29）","url":"https://www.sec.gov/Archives/edgar/data/1792789/000114036126041111/ef20084547_8k.htm","excerpt":"each share of common stock, par value $0.0001 per share, of Instacart (the “Instacart Common Stock”) issued and outstanding (other than Excluded Shares and Appraisal Shares (as defined in the Merger Agreement)) will be converted into the right to receive, at the election of the holder thereof and subject to proration as described below, (i) $65.00 in cash, without interest","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","thesis.R","valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"FY2025 10-K 揭露持續面臨 Dasher 獨立承包商分類等訴訟、仲裁與政府調查（含集體訴訟）；搜尋未見證券集體訴訟，僅見消費者／隱私類案件（如 2025-11 資料外洩集體訴訟，未核原文）。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm","excerpt":"We are currently involved in, and may in the future be involved in, legal proceedings, claims, regulatory inquiries, audits, and governmental investigations (collectively, “Legal Proceedings”) in the ordinary course of business, including suits by merchants, consumers, Dashers, or other third parties (individually or as class actions).","as_of":"2026-02-18","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 10 份 8-K 中無 Item 4.02（財報不可依賴）項目；搜尋亦未見 SEC 調查或重編。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001792789&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"DASH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":51.51,"operating_margin_pct":4.05,"fcf_margin_pct":11.38,"rd_intensity_pct":10.86},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DASH","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"UBER","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":42.31,"operating_margin_pct":12.13,"fcf_margin_pct":18.32,"rd_intensity_pct":6.77},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UBER","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"CART","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.23,"operating_margin_pct":13.88,"fcf_margin_pct":29.6,"rd_intensity_pct":17.58},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CART","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"DHER.DE","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DHER.DE"},"note":"quarterly_income_stmt 無資料"}],"subject":"DASH"},"financial_history":{"ticker":"DASH","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":6583000000.0,"revenue_yoy_pct":null,"gross_margin_pct":45.5,"operating_margin_pct":-15.68,"net_income":-1365000000.0,"diluted_eps":-3.68,"free_cash_flow":21000000.0,"fcf_margin_pct":0.32,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":8635000000.0,"revenue_yoy_pct":31.17,"gross_margin_pct":46.86,"operating_margin_pct":-6.68,"net_income":-558000000.0,"diluted_eps":-1.42,"free_cash_flow":1349000000.0,"fcf_margin_pct":15.62,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":10722000000.0,"revenue_yoy_pct":24.17,"gross_margin_pct":48.31,"operating_margin_pct":-0.35,"net_income":123000000.0,"diluted_eps":0.3,"free_cash_flow":1802000000.0,"fcf_margin_pct":16.81,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":13717000000.0,"revenue_yoy_pct":27.93,"gross_margin_pct":50.88,"operating_margin_pct":5.29,"net_income":935000000.0,"diluted_eps":2.13,"free_cash_flow":1826000000.0,"fcf_margin_pct":13.31,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/DASH/DASH_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**DoorDash, Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Hello, everyone, and thank you for joining us, and welcome to the DoorDash Third Quarter 2026 Earnings Call. [Operator Instructions] 
I will now hand the call over to Weston Twigg. Please go ahead.

**Weston Twigg** (Executives):
All right. Thank you, Dustin. Good afternoon, everyone, and thanks for joining us for our Q3 2026 earnings call. I'm pleased to be joined today by Co-Founder, Chair and CEO, Tony Xu; and CFO, Ravi Inukonda. 
We'll be making forward-looking statements during today's call, including, without limitation, our expectations for our business, financial position, operating performance, profitability, our guidance, strategies, capital allocation approach and the broader economic environment. When we -- we will also be making forward-looking statements about our pending acquisition of Instacart, including, without limitation, the expected timing and likelihood of completion of the acquisition and our plans, objectives, intentions and expectations with respect to the acquisition and the combined company. 
Forward-looking statements are subject to risks and uncertainties that could cause actual results to differ materially from those described. Many of these uncertainties are described in our SEC filings, including our most recent Form 10-K and 10-Q. You should not rely on our forward-looking statements as predictions of future events or performance. We disclaim any obligation to update any forward-looking statements, except as required by law. 
During this call, we will discuss certain non-GAAP financial measures. Information regarding our non-GAAP financial measures, including a reconciliation of such non-GAAP measures to the most directly comparable GAAP financial measures may be found in our earnings release, which is available on our Investor Relations website at ir.doordash.com. These non-GAAP measures should be considered in addition to our GAAP results and are not intended to be a substitute for our GAAP results.
Finally, this call is being audio webcasted on our Investor Relations website. An audio replay of the call will be available on our website shortly after the call ends. Operator, I'll pass it back to you, and we can take our first question.

**Operator** (Operator):
[Operator Instructions] And your first question comes from the line of Andrew Boone with Citizens Bank.

**Andrew Boone** (Analysts):
Tony, you laid out a pretty compelling case in terms of adding additional demand to DashMarts. Can you just flesh that out, help us understand what your vision is for DashMarts and how Instacart plays into that?

**Tony Xu** (Executives):
Yes. I mean if you think about where grocery delivery is, it really is just a fraction of what its potential could be. And I think the reason I said this quite a lot in the past that the product really isn't there yet. Customers today are still being asked to pay a premium for imperfect delivery. So the question is, how can we actually ensure that we offer perfect deliveries at the most affordable prices? And the way I think about this is it really is a sequencing road map. And our journey really started 5 years ago when we began our own work in new verticals, and it's been a very successful endeavor. As part of that journey, we recognized that in order to offer the best possible service at the most affordable prices, we really needed to manage the inventory because stockouts were a key issue. 
And when you look at, for example, the deliveries that we fulfill from DashMarts versus the delivery that we do third party, even though we have best-in-class logistics operations quality in the third-party stores, we are near perfect in our deliveries with DashMarts, but we're only in the low 90s in terms of our accuracy through the third-party stores. So there's a meaningful gap, but we've been able to prove demonstrably that we can close it both first by holding our own inventory and now actually managing thousands of items for fantastic retail partners like Giant Eagle or Albertsons and many others. 
But when you think about this business, it's a fixed-cost business when you're managing inventory. So scale is really helpful. And when I think about today's news in partnering with Instacart and the fact that they have unique demand or orders that are unique to our network, that not only helps certainly, on a day 1 scenario post-close, where the added density in the last-mile network brings fulfillment efficiencies to offer faster delivery as well as lower cost throughout the system, but it allows us to continue to invest on our end state journey of building what we believe will be the best-in-class product for all retailers to be able to compete against the world's biggest companies. 
And that will enable faster delivery and that will enable more affordable prices, which in turn will generate more sales for every grocer and retailer and more earnings opportunity for every shopper.

**Operator** (Operator):
Our next question comes from the line of Shweta Khajuria from Wolfe.

**Shweta Khajuria** (Analysts):
Okay. Let me try two, please. One is you talked in your release and letter that you expect multiyear path to $500 million or more in annual synergies net of investments. Could you please talk about where those synergies will be coming from? And where do you expect to invest? In year 1, over 100% of total synergies will be invested. So could you please talk about how do you see that play out? 
And then second, on DoorDash's core business, U.S. marketplace GOV accelerated on tougher comps, which is impressive. And I guess you talked to rise in frequency as well as new consumers ordering. Could you please talk to that a little bit more? How do you see demand trend? And what going forward will drive organic U.S. market -- restaurant marketplace growth?

**Ravi Inukonda** (Executives):
Shweta, it's Ravi. Look, I mean, I'll take both of them, and Tony, feel free to chime in. Look, I mean, I think there's an opportunity, Shweta, for us to build a really large and attractive business, right? If you think about synergies, which is the part of your question, there's a number of big blocks that you could think about. 
Let's start with the growth ones first. Look, there's an opportunity for us to cross-list merchants. For example, there's categories that are not available on both platforms. There's a clear opportunity for us to be able to cross-list them, which drives growth. One of the clearest examples is we are going to be able to list our restaurants platform on Instacart, which is going to drive top line growth. 
Second, I would talk about is just purely ads. CPG advertisers will now have more consumers to reach, which will not only drive quality, but also higher ad spend, which will in turn drive more ROAS. The third one that I would think about is there is an opportunity for us to cross-sell products. Instacart has built a really strong first-party software infrastructure, which we can now cross-sell to grocers on our platform as well as Tony touched on DashMart Fulfillment Services. It's going to be an opportunity for us to make that available to more customers across both platforms. 
Look, I mean, on the efficiency side, Dasher density, shopper density is going to be pretty critical. As you increase the volume, that's going to drive efficiency in the fulfillment network. And finally, if you look up and down the P&L, there's a number of opportunities, whether it's opportunities on sales and marketing opportunities on support. There's many opportunities that we could jointly work on together. And we thought about the opportunities that can jointly arise from combining both platforms. 
One thing that's pretty clear is putting both platforms together will actually rise to leading in growth as well as increasing in overall profit dollar production. The key for us, however, is how do you take some of the profit dollars and reinvest that back in the business to ultimately build a better product for consumers as well as grocers. Look, that's historically what we've done. 
And to the second point in your question, which is what's driving the growth in the core marketplace. Largely because of the reinvestment back in the product, our playbook is going to be very similar here. You can see examples from that in our acquisition of Deliveroo as well, where we've reinvested back in the product to ultimately drive the growth that you're seeing in the business. In fact, when I look at the new verticals platform, our core business is doing really well. That's growing quite nicely. We've become volume share leaders. We've continued to improve the customer outcomes, whether it's increase in order rate, increase in order frequency, the basket sizes are growing. 
So the way we think about this is this is actually an accelerant to our core business, which continues to do well. And the other side, which is the core business continues to do well, which gives us, a, the conviction and the capacity to be able to do more. So if you're thinking about it from a modeling perspective, the way I would think about the model is year 1 is going to be the investments that we'll make to build a better product. Year 2, we'll make progress. And finally, in year 3, my expectation is we'll drive $500 million of incremental synergies to the bottom line that is net of the investments that we plan to make. 
On the second one, look, I mean, you're right. I mean, the core business is doing really well. It's firing on all cylinders, right? If you look at the growth that we're seeing in the business, Q3, our restaurant business actually accelerated from Q2 to Q3. In fact, when you look at the sequential growth rate in Q3, it's the fastest we've seen in the last 5-plus years. New verticals continues to grow, both Wolt as well as Deliveroo, they also accelerated from Q2 to Q3. But more broadly, when you look at our overall U.S. restaurant growth, it's been stable actually for the last 4 years. A lot of that has got to do with the underlying improvements in the product. 
We've invested back in selection. We've made subscription better. Overall paid subscribers continue to set all-time records. The combination of the work that we've done in improving the product while continuing to drive subscription is what you're seeing in terms of the growth that you're seeing in the business. And again, the growth is coming from sustainable levers, which is user growth, subscription growth. And the way at least I think about it from a mental model perspective is these are compounding growth that will come in the future, which gives us a lot more confidence as we look ahead into what we can drive in terms of both growth as well as profit dollar production for the next several years.

**Operator** (Operator):
Our next question comes from the line of Deepak Mathivanan from Cantor Fitzgerald.

**Deepak Mathivanan** (Analysts):
Great. Tony, so on the acquisition of Instacart, can you talk about why now is the right time? I mean your grocery business is strong, and you have most of the retail partners, too. DashMart is offering a very differentiated value prop to retailers. Can you talk about why now is the right time? 
And then also a second one, a high-level strategy question on AI agents. How much of the agentic experience, specifically for food use case, be it grocery delivery or food delivery or maybe meal planning and others, do you want Dash to kind of directly power for consumers with ceding some of that to more generic agents like Muse. Or maybe asked another way, should we expect Dash to have its own set of personal agents, specifically catered for food use cases for consumers? How should we think about that?

**Tony Xu** (Executives):
Yes. Deepak, I'll take both of those. On the first question about why now. I mean, it's a great question because M&A is very, very hard to do successfully. And so we always take these decisions extremely seriously. I would say the first thing is our core business is doing really, really, really well. Ravi touched upon a bit of this. And as you can see in the results that we just published this morning on the quarter, I mean, record highs in top line, bottom line, accelerating growth in the U.S. restaurants business, continued fast growth on new verticals, accelerating growth in our international properties. 
You continue to see product innovation from us. For example, our most recent Dash Forward event with the announcements of DoorDash Air, DashOS and merchant software as well as, speaking of AI agents, updates to our own AI agents. So the core business is truly firing on all cylinders. 
I would say the second thing is our big projects for the year are on track. Obviously, the year is not over. But if you look at the projects around building a single tech stack, if you look at the projects around integrating Deliveroo and the -- some of the results kind of speak for themselves. We're seeing customer benefits already from the single tech stack work, whether it's faster onboarding of merchants, better conversion from improved search, better SLAs for support across all audiences. These are just some of the ones that come top of mind. 
If you look at the ROO side, we grew in Q3 at twice the rate that we did a year ago before we acquired the business. So all of the big projects we had for the year were projects that are doing really, really well. And so from a management bandwidth perspective and a sequencing perspective, we felt like we had the space to do something offensive. And this is a space we understand really well, the grocery marketplace space, both because we built our own grocery marketplace very successfully to your -- to the premise of your question, as well as the fact that we've integrated other marketplaces very successfully into the DoorDash family, whether it's Wolt, whether it's Deliveroo, whether it's actually even thinking about how we've reinvested over the years back into product innovation and driving durable growth for our own U.S. restaurant marketplace. 
I think those would be all 3 demonstrable examples of our understanding of how to run a marketplace at scale, both driving top line growth durably, but also generating long-term total profit dollars. And that's what we intend to do here and play offense. 
When I think about Instacart, I talked a little bit about how it feeds us on the journey towards building this end state, which is being able to manage inventory on behalf of every retailer of every size. But when I think about this, this really is about giving every retailer of every size the ability to compete in a world where technology is only accelerating faster, disruption is happening more quickly and the world's biggest companies are becoming larger. 
And when I think about the capabilities that the combined companies will have, we will have best-in-class software to help each one of these grocers. That's something that Instacart has done a fantastic job building over a decade in helping grocers build their first-party online channels. You combine that with our first-party logistics capabilities, which we pioneered with DoorDash Drive also over a decade ago, and you can offer merchants the ability to build the best-in-class first-party experience for fast delivery, their own loyalty programs, their own data, their own customers. Then you look at the third-party side of the house, the combined marketplace and the combined reach gives every grocer higher quality orders, faster delivery, which is going to generate more sales. And so I think it was just the time to play offense. And you're right. I mean, everything is going great with the core business. This only adds to it. 
Your second question was around AI agents. I would say that this is something that is still a very dynamic area. And my take on all things technology is you never want to fight gravity. But at the same time, you don't want to be delusional. What I mean by that is if you look at where AI agents are today, we're seeing maybe several hundred orders in total from some of these third-party agents, some of which you've cited in terms of whether or not customers are placing orders. And I think it's because they still largely view these third-party assistants, not necessarily for what I call these easier tasks, whether it's ordering food, like you said. The predominant use case of that is actually through our app. 
And what we've been doing is actually in learning with some of these third parties what are the features that actually drive incremental orders, in which case we can build a very healthy partnership with some of these third-party assistants. But then what are the features that actually just make the DoorDash app and our own AI agents, whether it's DoorDash Ask (sic) [Ask DoorDash], the Text DoorDash which is something that we released recently, our MCP that we've been giving to third parties to use for things like corporate lunch orders, things like this to just make our app easier to use. 
And I think that is the win-win of what we've been able to see where the volumes are very low, as I kind of cited. But I do believe there's a path in which you can get incremental orders and allow customers to order the way that they want to order, especially for long-consideration purchases or purchases they're not even thinking about that might be proactively made on their behalf. But for -- the everyday ordering, what we see is people come to DoorDash and they come back to DoorDash. It's easy to use. We're making it easier to use, and we expect to continue to do so.

**Ravi Inukonda** (Executives):
Deepak, going back to your first question, right, I'll just reiterate one point. Look, I mean, you're absolutely right. Our core business on new verticals is doing really well, right? Look, we've been operating this business for the last 5 years, a lot of performance that we've demonstrated over the last 5 years. If you look at the performance of that business, that business is growing really fast. When I look at the cohorts, MAUs are increasing, basket size is increasing, people are using us for different use cases. We actually think the combination is truly going to be an accelerant for us. We talked about efficiency. A couple of calls ago, I mentioned that the overall new vertical portfolio is going to be gross profit positive by the end of the year. We're pretty close to doing that. We're pretty close to being breakeven on a gross profit level. So the combination of both Instacart and us actually adds to that vision. So we're doing it from a position of strength, the way we think about it.

**Operator** (Operator):
Our next question comes from the line of Nikhil Devnani from Bernstein.

**Nikhil Devnani** (Analysts):
Maybe just a follow-up to what you were just talking about, Ravi. I guess, have you found the organic effort in the category to be harder than you initially expected when it comes to building wallet share or recurring habitual behavior around grocery? I appreciate that the growth has been quite strong, but I'm just wondering the extent to which you feel Instacart might help with some of the more challenging aspects of the build-out.
And then maybe a related question on the deal is just given the replatforming and integration exercise you're going through this year for the other assets, how does that help your overall integration ability and sort of the speed at which you can move with this deal once it eventually closes?

**Ravi Inukonda** (Executives):
Yes. Nikhil, I'll take the first one. Look, I mean, I think quite the contrary, right? Like actually, in my answer to Deepak's question, I talked about what we're seeing from an underlying cohort perspective, right? The way at least we run the business is ultimately, it's a cohort business. I look at the historic cohorts to see what the behavior of the future cohorts is going to be. 
When I look at mature cohorts, the behavior that we're seeing is people are using us more, more of those cohorts are coming back, which tells me that the product has gotten better, people are getting habituated to the product. Their basket sizes are increasing. Their engagement on the platform is increasing. And that is now starting to translate into newer cohorts as well, where we're seeing similar signs of strength in the newer cohorts. That to me truly is what we think is actually going to happen in the overall business as well as you continue to add more and more newer cohorts. 
Our goal has been, how do you continue to improve the product? Whether it's adding more selection. Look, we just added Costco on the platform, which is off to a great start. We've increased the quality of the platform. Overall, more number of DashPass subscribers are continuing to use categories outside of the core restaurants, and that number continues to grow. All of this gives us confidence that people are using the product more. They're engaging with us even more, which is also driving some of the efficiencies that I talked about, right? As we continue to scale that platform, we're seeing efficiency gains also come back and benefit the overall platform, which we are reinvesting back in the business. 
To us, the combination of both Instacart and us is actually going to accelerate this vision. And the simple mental model that we have is, look, when you put both companies together, there's an obvious opportunity in driving both higher top line growth as well as higher profit dollar production. On top of that, we're going to have synergies. Our goal is how do you take a portion of that, reinvest that back in the business historically, like we've done with Deliveroo, like we've done with our core restaurant business, which is what's driving the stable growth, and use that to ultimately drive a better product, which, in fact, will drive more growth over the longer term as well as get the customers to adopt a better product.

**Tony Xu** (Executives):
Nikhil, I'll just add a little bit to that before I talk about your question on the integration of the tech stacks. To get, I guess, one level deeper, a lot of what I think about here is actually how can we actually help improve the Instacart business as well as how can they help improve ours. And it's -- actually, I think that because of the success we've seen in running our marketplace as well as the marketplaces, as I've mentioned, of the ones we've integrated as well as how we've reinvested back into the U.S. restaurants marketplace and some of the things we've learned on how to do that, I think we'll actually be able to reaccelerate the Instacart marketplace. And I actually think that they'll help us grow a lot of the first-party software products for grocers and retailers, something that they started ahead of us, whereas we kind of focused on first-party on the restaurant front. 
And so I actually think that it's quite a nice mutual combination here where you're bringing the best of both, where on the DoorDash side, the best-in-class understanding of logistics operations, how to manage the marketplace to total profit dollars, how to generate product innovation in a continuous way. And then on the Instacart side, the best-in-class tools for -- software tools for grocers and their own online channels. 
Your second question was around tech stack. I'm glad you asked it. So I mean, this is a huge endeavor for us, and I actually don't even think most people appreciate how big of a deal it is because we're not only trying to get all of our features into one tech stack, which means that we ship, once we ship, everywhere. But we're actually building new infrastructure, like actually new infrastructure to run core DoorDash, which will make any future integration much easier to run because it will just kind of work out of the box. So it will actually speed things up quite a bit. And that's why we decided to undertake such a large investment, both in terms of dollars as well as people, I mean, literally rebuilding this airplane as we're flying it part by part, engine by engine. And so it will actually speed things up in the future.

**Operator** (Operator):
Our next question comes from the line of Michael Morton from MoffettNathanson.

**Michael Morton** (Analysts):
One for Tony and then one for Ravi. Tony, I was curious to how you expect this deal to be perceived by your grocery customers. Will it land with them that DoorDash is becoming at similar scale to Amazon and Walmart and going to help them in that competition? Or will it raise concerns that they have now one concentrated service provider because those grocers are obviously powerful with the kind of local regulatory bodies? 
And then my next question for Ravi is just I was curious as to why you're using your shares. Historically, you've been very disciplined with repurchasing shares and it's trading at a level where you have been active repurchasing. So just trying to get a better understanding to why you see it as an opportunity to use your currency at these prices and not just more cash.

**Tony Xu** (Executives):
Michael, I'll take the first one. We expect a very positive response from grocers. And a lot of what we talk about with grocers is just how are -- how can we together help them compete against the largest companies in the world, online or offline? And how do we actually help them build the capabilities of great technology, a modern tech stack as well as fast delivery? You really need all of these component parts to have a fighting chance. I mean if you -- I mean, if you've seen what has happened in the grocery industry, in particular, I mean, the largest companies are only getting larger and eating more of the pie. And the question is how do you give everybody else a fair fighting shot? 
And I think the grocers view things very similarly. I mean these are conversations about what's happening in the industry in terms of the biggest companies eating more of the pie. I mean, that conversation has been happening for the past decade.  And it's only kind of gone in that direction of travel. So the question is how do we give everybody else the capabilities to have a level playing field? And that's what we see in this potential partnership, which is we're going to give you the tools, we're going to give you the business with added density, which will help with faster delivery times, more affordable prices for everyone. Greater earning opportunities for shoppers. 
And we think it really puts together the best possible chance where you have a modern tech stack that we're only going to continue investing and innovating more and new fulfillment models, which we are inventing as we speak. And certainly, reinvestment, which has been the philosophy all along the way at DoorDash and how we've built our own marketplace.

**Ravi Inukonda** (Executives):
Mike, look, I mean, on the second point, look, I mean, I think you're absolutely right. We value our stock very highly. Look, we are focused on dilution. It was important for Instacart to have some stock in the deal, as overall, they wanted to participate in the upside in the business. Look, we believe there's upside in the business. We are happy with the consideration between cash and stock. 
What I will tell you is, look, our philosophy on buyback has not changed, right, to the second part of your question. We've been conservative. We're going to be opportunistic. We're happy with the buybacks that we've done so far, which has generated a strong IRR. And in the future, if we see there's a good opportunity to buy back, we are happy to do that as long as it's a good return on the overall investment.

**Operator** (Operator):
Our next question comes from the line of Josh Beck from Raymond James.

**Josh Beck** (Analysts):
I wanted to ask just a little bit about the ambitions on DashMart. I think in the shareholder letter, you mentioned thousands of items from some of the big, well-known grocers. And if you look at maybe someone like Instacart, they've spoken to selection of millions or tens of millions of items. So is there an ambition to have probably not a similar selection, but maybe some fraction of that available via DashMart? And kind of what -- how should we think about the investment angle behind DashMart? Is this something where we need a much bigger fulfillment footprint and we should be thinking more warehouses, more employees? Just like to hear a little bit about how we should frame that up.

**Tony Xu** (Executives):
Yes. Josh, I'll take that one. I mean if you look at the next decade of work, I mean, it really is about making sure that we can build the local infrastructure for all things last-mile delivery for everything inside your city. That's what DoorDash is working on, right? So that's about merchant software. That's about building new fulfillment models, so some of the warehousing that you're discussing. And of course, it's always about making sure that we have the highest quality and most affordable logistics network. It's why we're investing deeply into autonomy, both land vehicles and drones.
And you're right, there is going to be an investment. But the way to think about this is a lot of the real estate though, that we're talking about, in many ways, has already been designed for us. There are hundreds of thousands of grocery stores available that carry these millions of items that you're already talking about. The real question is whether or not all of that square footage and all of that shelf space is being utilized in the most productive way. None of these stores, as you probably know, are built for delivery. I mean they were effectively built for browsing. 
And in a world where delivery and convenience are a much bigger part of consumer expectations and a growing trend, something has to change in order to offer a cost structure as well as a price point that consumers expect to see so that they will continue growing their relationships with each one of these grocers. And that's really what we believe we can build with Instacart. But this is a sequencing process. This is not something -- when you're talking about all things physical and not just pure digital, you can't just hit a button and then magically, everything changes. You have to understand that it's a marriage of technology, operations and people. 
I mean a lot of these fantastic businesses of these grocers have been built over many decades, and their processes have been built over many decades. And the question is how do we allow those stores to shine as the showrooms? And how do we actually build the correct square footage as the warehouse or the back-of-house infrastructure such that we can offer fast delivery at attractive prices to compete against the world's biggest companies? That is the vision of DashMart, but it's a sequencing process. 
Step one, day 1 after close, it's how do we actually take the combined network where you have added density and DoorDash understands well how to reinvest that added density and give back value to everybody, every audience, consumers, grocers, shoppers. How do we then take that added scale to then drive down further costs as we think about managing warehouses, which is a fixed cost business? How do we then do that with more types of SKUs and items so that we can bring more of the store? Then how do we bring every single store and ultimately everything inside your city to you in minutes?

**Operator** (Operator):
Our next question comes from the line of Bernie McTernan from Needham & Company.

**Bernard McTernan** (Analysts):
Maybe just a follow-up on some of the maybe more eloquently said regulatory questions. Tony, is there anything else to add in terms of what got you comfortable in order to get this deal past regulatory? And then second, any additional plans on the go-to-market? It seems like the plan is to keep the Instacart brand, but just wanted to see from a consumer perspective, what we should expect.

**Tony Xu** (Executives):
Yes. I mean, the first thing I'll say is that -- the first question I always ask is like, what is something fair? And what is it that we actually want to see in the world? And what I believe is fair and something that we want to see in the world is a world in which every business locally of every size has a fair chance at competing. That is the mission of DoorDash. I mean, that's really why I created DoorDash. And if that were to happen, then GDP grows locally, which is the best possible way of GDP growth, not just for jobs, but also for the safety and health of communities and really the lifestyle of why we pick the different neighborhoods and cities in which we live. 
And when I think about it from that perspective, and you just look at what's happening in the grocery industry, for example, over the past decade or even 2 decades, what you see is the largest companies are only eating more and more of the pie. Why is that? It's because they've invested aggressively into capabilities like a modern technology stack, like fast delivery, like new fulfillment models. And that's been very difficult when you're a smaller player to invest in on your own. That's what this combination is really about, where DoorDash and Instacart can give every retailer a fighting chance of competing in the modern-day era. And I believe that if we can do that, that's great for every community. 
So when I think about it from that perspective, that's how I get comfortable, a, knowing it's the right thing to do whenever you're doing the right thing, that usually is the right narrative for anyone. The second comment around go-to-market, we won't say too much about this for now. But you're right. I mean, I think Instacart has built a great brand, and it's a very unique brand where their audience is very, very loyal to that brand. And so we certainly will support it. We certainly will bring value to consumers. For instance, for the same price that you pay for DashPass today, you'll get access to 2 subscription programs, the Instacart membership program as well as the DoorDash membership program. 
And we have some other ideas, too. But a lot of the value in this partnership is really going to come in all things, what I see almost like not visible to the consumer. They'll see the benefits in the form of faster delivery, lower prices, greater selection, higher quality and accuracy of orders. Grocers will see the value in terms of extra sales. Shoppers will see the value in terms of greater earning opportunities. And communities will see the value in greater GDP.

**Operator** (Operator):
Moving forward, our next question comes from the line of Youssef Squali from Truist.

**Youssef Squali** (Analysts):
I just have one question. Ravi, can you maybe just talk a little bit about where you guys are within -- with regards to your replatforming? How much of it has been completed so far? Are you on track? Are you ahead on budget? And then I guess, as part of that question, as Instacart comes into the fold, I guess, starting in 2028, is it fair to assume that effectively, the replatforming becomes like work in progress that extends way beyond next year as well as you try to integrate Instacart and hopefully generate the type of synergies you're talking about?

**Ravi Inukonda** (Executives):
Youssef, let me take that one. Look, I mean, I think on the overall tech platform, it is on track, both from a cost as well as a time line perspective compared to what I talked about like a few quarters ago. In fact, we have been working on it in a very modular fashion. We have several modules that are already live on the new tech stack. We're already starting to see traffic flow through it. We're fully seeing customer benefits, too. In places where we've already deployed our new tech stack, merchants are getting onboarded faster. Customer support is starting to get better. We already started to see early signs of benefit. 
In terms of the overall time line, look, I expect that to be done by the first half of 2027, which is what we had originally expected. So overall, we feel very good about both time line as well as cost. 
And your second point around integration of Instacart onto the overall new tech stack, look, I mean, one of the core features as we thought about the new tech stack was the ability to add more future acquisitions and future platforms onto the tech stack. We've done some work around this. We think there's some investment needed. But overall, we don't think it's a massive investment to be able to operate both tech stacks on the replatformed tech stack on a go-forward basis.

**Tony Xu** (Executives):
Yes, Youssef, the one thing I'll add is something I said, I think, on an earlier question, which is, one of the biggest parts and why this current work on building a single tech stack is so expensive is we're actually literally building new infrastructure, which is why you have a lot of different copies of compute instances and you're overprovisioning things and you're doing all of these things so that you literally have a much faster capability to build any new thing in the future. That includes, obviously, building organically, but also what Ravi said, integrating new products or new technologies or new services. And so it makes us ready for any modern work we want to do with AI agents. It makes us ready for any new acquisitions.

**Operator** (Operator):
Our next question comes from the line of Dominic Ball from Rothschild & Co Redburn.

**Dominic Ball** (Analysts):
Congrats on the news. I just want to go back to another question around consumer AI agents. So acquiring Instacart strengthens your position in the physical world. Advertising is a meaningful contributor to DoorDash's EBITDA. How do you see that business evolving as consumers over time shop through AI agents? And could there be a revenue-sharing agreement with these consumer agents going forward?

**Tony Xu** (Executives):
Dominic, I don't know if you were able to catch the top of the call. We discussed some of this, which is, right now, AI agents are generating several hundred orders across the time that they've been up and running. So it's been a fairly low use case. And I believe that there will be opportunities in which we can generate win-win opportunities with third-party agents. My general philosophy when it comes to technology is you never want to fight gravity. And if -- and that includes how consumers want to use technology. If consumers want to use technology to shop in certain ways, we're going to find a way to make that a win-win partnership. 
And I do believe there are a lot of incremental possible use cases, whether it be helping with long consideration purchases, whether it be doing work on your behalf proactively in the background. But when it comes to a task that's as simple as ordering food, we tend to see that come directly to DoorDash. Not to mention, we're building our own AI agents to make the shopping process a lot easier. 
But you also have to remember one thing, which is it's not just about ordering food. That's actually not the hard part of the entire process or ordering groceries. The hard part is making sure that they actually show up and show up in the order in the way that you expected and the condition that you want. That end-to-end journey and making sure all of that is going to happen appropriately, especially when things go awry, we found that to be true living in our product. 
That said, I actually think that there will be advertising opportunities even within some of these AI agents. But I think first and foremost, we have to find ways to bring value to consumers. Right now, with the low volumes that I kind of -- I'm telling you about, there isn't yet that value. But as hopefully, that grows, we'll find a way to make that work.

**Operator** (Operator):
Our last question comes from the line of Justin Post from Bank of America.

**Justin Post** (Analysts):
Can you give us any idea of the scale of their grocery business relative to yours? And then acquisitions in the grocery space have been somewhat difficult in the past. As you think about talking to the regulators, what are some of the points you would think about as far as share and how this really benefits grocers?

**Ravi Inukonda** (Executives):
Justin, let me take this one. Look, I mean, I think on your first question on share of grocery, look, we -- it's public information. We're not going to talk about -- disclose anything about Instacart. 
To your second point around the value to grocers, look, I mean, ultimately, we talked about some of this, right? Like the goal is how do you take the combination of both capabilities that both companies have and how do you build a better platform, right? We have a highly sophisticated logistics engine. We have a demand generation engine. We've build DashMart Fulfillment Services for some merchants that we talked about. Instacart has done a really good job of being able to build a very large enterprise storefront platform in addition to their own demand generation engine. And I think the combination of both of this will actually help increase the number of products that we can co-sell to both sets for merchants. 
In addition to that, I think there's an opportunity where we can actually invest back in the product to build a better product, not just for grocers, right, for consumers as well. We actually think the combination of both is a win-win for consumers, grocers as well as overall shoppers in the ecosystem.

**Operator** (Operator):
That concludes our question-and-answer session. This concludes today's call as well. Thank you all for attending, and you may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### DASH_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜commitment：CFO 重申新垂直業務預計下半年毛利轉正（原話："We're on track for that in the second half of the year."）
- 2026-08-05｜CFO｜guidance：CFO 表示下半年利潤率預期落在先前給的 Q3 財測區間內（原話："I would expect us to land inside the range of"）
- 2026-08-05｜CFO｜guidance：CFO 對 take rate 的建模指引：Q3 與 Q2 持平、Q4 較低（原話："so flattish from Q2 to Q3, and lower in Q4."）
- 2026-08-05｜CFO｜margin：CFO 說明 Q2 EBITDA 超標來得晚，沒時間再投資（原話："we just don't have enough time to reinvest back in the"）
- 2026-08-05｜CFO｜margin：CFO 點出單位經濟超預期的兩個來源（原話："Ads was one of them, subtotal was the other one."）
- 2026-08-05｜CFO｜margin：CFO 說明 Deliveroo 在 Q2 貢獻利潤為正（原話："ROO's contribution profit positive"）
- 2026-08-05｜CFO｜margin：CFO 表示不追求單季最後一塊錢的最佳化（原話："We're not trying to optimize the last dollar"）
- 2026-08-05｜CFO｜margin：CFO 解釋 Q1 到 Q2 take rate 上升來自 Dasher 成本季節性（原話："Dasher costs are seasonal for us."）
- 2026-08-05｜CFO｜commitment：CFO 對 Deliveroo 的利潤目標表態（原話："meet the profitability targets that we set out in the last"）
- 2026-08-05｜CFO｜commitment：CFO 稱自主配送、技術堆疊統一、商家服務投資均在預算與計畫內（原話："They're all going on budget and on"）
- 2026-08-05｜CFO｜capital_allocation：CFO 描述效率持續改善、再投資的原則（原話："We're consistently trying to improve efficiency."）
- 2026-08-05｜CFO｜capital_allocation：CFO 說明 AI 支出管控：設上限（原話："We've put caps in place."）
- 2026-08-05｜CEO｜product：CEO 稱單一技術堆疊的更多效益預期在明年初之後（原話："we expect to see even more benefits as time goes on."）
- 2026-08-05｜CEO｜product：CEO 談自動配送：先做到位再擴張（原話："you really have to nail something before you scale it"）
- 2026-08-05｜CEO｜product：CEO 談 DashMart Fulfillment Services 的錯誤率（原話："we're also seeing 10x better error rates"）
- 2026-08-05｜CEO｜product：CEO 介紹下單代理 DoorDash Ask（原話："DoorDash Ask, which is an ordering agent"）
- 2026-08-05｜CEO｜product：CEO 談商家端數位業務規模（原話："that business serves over 150,000 businesses"）
- 2026-08-05｜CFO｜customer：CFO 稱 DashPass 去年新增訂閱者多於前兩年（原話："We added more number of DashPass subscribers in the last"）
- 2026-08-05｜CEO｜customer：CEO 稱代理式流量目前很低（原話："quite low, I think, from some of the agentic partners"）
- 2026-08-05｜CFO｜customer：CFO 談新增距離費對損益影響（原話："I wouldn't expect it to be a massive impact"）
- 2026-08-05｜CEO｜competition：CEO 說國際市場是最小可行規模的生意（原話："And that's because it is a minimum viable scale"）
- 2026-08-05｜CEO｜competition：CEO 稱前十大海外市場為領先者或強勢第二（原話："we are the leader or we are a very strong #2"）
- 2026-08-05｜CFO｜competition：CFO 稱英國市場 Deliveroo 持續搶市占（原話："We're one of the fastest growing in that"）
- 2026-08-05｜CEO｜risk：CEO 對下一步自動配送擴張城市不給時程（原話："We'll share certainly more as time comes"）

### 問答異常語氣（迴避／改口／保留）
- DASH_Q2_2026_Earnings_Call_20260805.md｜問：Morton 問部分雜貨商是否近乎零抽成、能否重新定價｜答法：CEO 稱不評論特定對象，改談成長與多個改善槓桿
- DASH_Q2_2026_Earnings_Call_20260805.md｜問：Helfstein 問 Dot 單位經濟與最新 AOV 數字｜答法：CEO 談願景與營運複雜度未給單位經濟數字；CFO 談籃子變大未給 AOV 數字
- DASH_Q2_2026_Earnings_Call_20260805.md｜問：Youssef Squali 問 2026 年不含 Deliveroo 的 EBITDA 利潤率是否仍高於去年、有無投資遞延｜答法：CFO 只答下半年落在 Q3 財測區間內，未直接答全年年增與遞延
- DASH_Q2_2026_Earnings_Call_20260805.md｜問：Beck 問 Dot 單市場個位數高段滲透的特徵與自動配送占比上限｜答法：CEO 先稱問題太多，改談 Phoenix 與執行力，未給占比上限
- DASH_Q2_2026_Earnings_Call_20260805.md｜問：Sandler 問 Dot 擴到其他城市的速度｜答法：CEO 稱有擴張計畫但之後再說，未給時程
- DASH_Q2_2026_Earnings_Call_20260805.md｜問：Nowak 問新技術堆疊模組可量化的投資報酬｜答法：CEO 以比喻回應並給定性例子（搜尋轉換、客服自動化），未給量化數字

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
{"date":"20260518","verdict":"衛星候選 — US local commerce 平台龍頭 thesis 完整但 Pure MA 修正期；估值合理 (Adj Fwd PE 28x / PEG 0.94)；等 MA 回測 W104 $185 站穩 4 週或 Q2 26 Adj EBITDA $820M+ 兌現後分批進場","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"US local commerce flywheel 持續加深：DashPass 訂閱數、orders/MAU、cross-vertical attach rate 三軸同步擴張，US 市佔 56% 至少維持或微升"},{"id":"H2","text":"Operating leverage 兌現 + Adj EBITDA margin 從 19% (FY25) 擴張至 22-25% (FY28E)：投資週期完成後，core platform OPM 應大幅擴張"},{"id":"H3","text":"估值 multiple 修復 + EPS兌現：當前 Adj PE 28x 對 30% CAGR 屬合理偏便宜；2H 2026 投資週期過後，PE 應修復至 32-35x peer-aligned；GAAP EPS Path 從 -$0.04（FY24 normalized）至 FY27 $4.39 = profitability story 兌現"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"投資週期失控（Capex 持續 ramp + Dot autonomous + 國際整合三軸 + merchant SaaS）→ Adj EBITDA margin 不擴張甚至壓縮"},{"id":"R2","text":"監管全面化（Seattle 模式擴展至 NYC / CA / Chicago / DC）→ Dasher 結構成本 +20-30%，contribution profit per order 結構性壓縮"},{"id":"R3","text":"UBER One $4.99 全面殺價 + Amazon Prime/ Walmart+ 跨平台訂閱競爭 → DashPass 增速放緩或被迫降價"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟠","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":159.2,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DASH_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
