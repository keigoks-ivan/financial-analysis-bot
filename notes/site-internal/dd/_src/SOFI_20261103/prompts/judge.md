你是 stock-analyst **v20 判斷 agent**，標的 SOFI（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"SOFI","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SOFI_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SOFI_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_total_net_revenue","label":"GAAP total net revenue","value":1385.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿 EX-99.1（SEC 8-K）"},"note":"adjusted net revenue 1,371.1m vs 共識約 1,260m（來源：tikr.com 報導，媒體轉述，未經 IR 稿佐證）"},{"id":"f_kpi1_adjusted_net_revenue","label":"Adjusted net revenue","value":1371.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿 EX-99.1"},"note":"共識約 1,260m（tikr.com，媒體轉述）"},{"id":"f_kpi2_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA／利益率（Non-GAAP 獲利口徑；SoFi 為銀行控股公司，不揭露營業利益）","value":469.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m（利益率 34%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿 EX-99.1"},"note":"新聞稿稱優於 FactSet 共識但未列數字"},{"id":"f_kpi3_gaap_net_income_sofi_gaa","label":"GAAP net income（SoFi 無 GAAP 營業利益，以稅前／淨利替代）","value":241.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m（淨利率 17%；稅前 317.8m）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿 EX-99.1"},"note":"GAAP／調整後 diluted EPS 0.18 vs 共識 0.17（tikr.com）"},{"id":"f_kpi5_fy2026_guidance","label":"FY2026 guidance（上修）","value":5040,"period":"Q3 FY2026（公告於 2026-10-27）","unit":"USD m adjusted net revenue（約 +40% YoY）；adjusted EBITDA 約 1,660m（33%）；淨利約 840m（17%）；adjusted EPS 約 0.61；會員成長至少 30%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿 EX-99.1"},"note":"新聞稿稱高於共識；先前指引營收 4.75–4.85B（tikr.com）"},{"id":"f_kpi6_fy2027_outlook","label":"FY2027 outlook（首度提供）","value":6400,"period":"Q3 FY2026（公告於 2026-10-27）","unit":"USD m adjusted net revenue（約 +27%）；adjusted EBITDA 約 2,240m（35%）；淨利約 1,280m（20%）；adjusted EPS 約 0.90","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿 EX-99.1"},"note":"consensus_revision 快照 FY2 EPS 0.89（dd_numbers_extra.py）"},{"id":"f_kpi7_members","label":"Members","value":17.07,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿 EX-99.1"},"note":"n/a"},{"id":"f_kpi8_total_products","label":"Total products","value":26.67,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿 EX-99.1"},"note":"n/a"},{"id":"f_kpi9_tangible_book_value_rotc","label":"Tangible book value／ROTCE","value":9705,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m（每股 7.48；ROTCE 約 10%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿 EX-99.1"},"note":"n/a"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_sofi_fcf_margin_pct","label":"SOFI FCF 利潤率","value":-222.21,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SOFI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cof_fcf_margin_pct","label":"COF FCF 利潤率","value":45.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COF.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ally_fcf_margin_pct","label":"ALLY FCF 利潤率","value":14.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALLY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hood_gross_margin_pct","label":"HOOD 毛利率","value":81.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hood_operating_margin_pct","label":"HOOD 營業利益率","value":45.65,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hood_fcf_margin_pct","label":"HOOD FCF 利潤率","value":58.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_share_based_expense_sbc","label":"Share-based expense（SBC）","value":70.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m（占調整後淨收入約 5.2%，占 adjusted EBITDA 約 15.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿 EX-99.1；占比為本表自算"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":17.38,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":7.16,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":60.75,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（0.61 → 0.61）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（0.89 → 0.89）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.14 → 1.14）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":0.61,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":0.89,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":1.14,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.67,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 0.6 → 0.61（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":31.58,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"2 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.81,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝31.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":31.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.06,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝7.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":7.3,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":28.48,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 0.61，分子＝快照價 17.37","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1169.83,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 3979.41、現金 2809.58（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1296.62,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":23691.94,"period":"2026-11-03","unit":"USD m","basis":"市值 22522.11 ＋ 淨負債 1169.83","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":5054.63,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":6393.89,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.69,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 16.9 / W52 19.46 / W104 18.81 / W250 12.09 / W250 13週斜率 0.21%"},{"id":"f_ma_w52","label":"52 週均線","value":19.46,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":18.81,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":12.09,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.21,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 自述各業務面對多元競爭者：優質貸款市場高度分散、有銀行／信用合作社／科技型放款人；存款端有更大的銀行與擁有大量客群的科技／零售公司；科技平台端有大型機構可能壓價。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm","excerpt":"Competition to fund prime loans. The prime lending market is highly fragmented and competitive. We face competition from a diverse landscape of consumer lenders, including other banks, credit unions and specialty finance lenders, as well as alternative technology-enabled lenders.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：新進入者與現有業者可能壓低定價，進而影響市占；公司未揭露具體市占數字。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm","excerpt":"Additionally, when new competitors seek to enter our markets, or when existing market participants seek to increase their market share, these competitors sometimes undercut, or otherwise exert pressure on, the pricing terms prevalent in that market, which could adversely affect our market share and/or our ability to capitalize on market opportunities.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Zacks 2026 報導：Upstart 為 SoFi 科技型消費放款直接對手，2026 Q2 Upstart 放款 42 億美元年增 50%；SoFi Q2 放款 148 億美元，其中個人貸款 107 億美元。","source":"Zacks: SoFi Technologies loan boom: can record originations keep climbing","url":"https://www.zacks.com/stock/news/2977081/sofi-technologies-loan-boom:-can-record-originations-keep-climbing","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SoFi Q3 2026 新增會員紀錄 120 萬，總會員 1,710 萬，年增 35%","source":"SoFi Q3 2026 earnings release (8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000065/a2026q3earningsrelease.htm","excerpt":"SoFi grew members 35% year-over-year to 17.1 million, adding a record 1.2 million members during the quarter, while products increased 44% to 26.7 million, including a record 2.2 million products added.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SoFi Q2 2026 總originations $14.8B 創高，個人貸款 $10.7B，含 Loan Platform Business $3.1B；Sixth Street 最高 $10 億個人貸款投資協議","source":"SoFi Q2 2026 earnings release (8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000050/a2026q2earningsrelease.htm","excerpt":"SoFi delivered its best quarter ever for total loan originations at $14.8 billion, up more than $2.6 billion from the prior quarter, including record originations across Personal Loans, Student Loans and Home Loans. Personal Loan originations totaled $10.7 billion which included Loan Platform Business originations of $3.1 billion reflecting strong demand from Loan Platform Business","as_of":"2026-07-29","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"SoFi 10-K（FY2025）揭露其受 2019 年 FTC Consent Order 約束，禁止在無可靠證據下向消費者誤述節省金額；並稱可能受政府機關審查、調查與裁罰。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm","excerpt":"Under the FTC Consent Order, we are prohibited from misrepresenting to consumers how much money they would save by using our products, unless the claims are backed up by reliable evidence.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：美中、歐盟等貿易與國際投資政策變動近年已對金融市場造成負面影響；貿易戰升級可能引發關稅等報復措施，屬間接（市場／總經）暴露，非產品或供應鏈直接暴露。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm","excerpt":"changes, or proposed changes, to certain U.S. trade and international investment policies, particularly with important trading partners (including China and the European Union (the “EU”)) have in recent years negatively impacted financial markets.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：貿易限制、制裁可能限制特定市場的全球匯款服務。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm","excerpt":"Political instability, trade restrictions, current or new tax laws, or economic sanctions imposed on certain countries may further restrict our ability to provide global remittance services in specific markets.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025 年 4 月 Morgan Stanley 分析師認為關稅影響對 SoFi 難以忽視（總經／消費者信貸管道），並下調目標價；為分析師意見，非公司量化。","source":"TipRanks／Globe and Mail：Morgan Stanley analyst says tariffs impact difficult to ignore for SoFi","url":"https://www.tipranks.com/news/morgan-stanley-analyst-says-tariffs-impact-difficult-to-ignore-for-sofi-stock-sofi","excerpt":"Morgan Stanley (MS) analyst Jeffrey Adelson argues that the impact of these tariffs is \"difficult to ignore\" for companies like SoFi.","as_of":"2025-04-08","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險因子提及依賴第三方雲端供應商（如 AWS）與 co-location 設施，及供應商可能再外包，未指名單一資料中心供應商","source":"SoFi Technologies Form 10-K FY2024","url":"https://www.sec.gov/Archives/edgar/data/1818874/000181887425000016/sofi-20241231.htm","excerpt":null,"as_of":"2025-02-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Lending 調整後淨營收約 $807.4M，年增 68%，由個人貸款需求與較高發放費用驅動","source":"SoFi 8-K Q3 2026 earnings release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000065/a2026q3earningsrelease.htm","excerpt":"The company's lending segment generated $807.4 million in adjusted net revenue, up 68% year over year, driven by strong demand for personal loans and higher origination fees.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Financial Services 淨營收 $525.1M 年增 25%；淨利息收入年增 38%、非利息收入年增 13%","source":"SoFi 8-K Q3 2026 earnings release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000065/a2026q3earningsrelease.htm","excerpt":"For the third quarter of 2026, Financial Services segment net revenue of $525.1 million increased 25% from the prior year period.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 Technology Platform 營收年減 24% 至 $87.4M（大客戶 2025 年完成遷出）；排除該影響年增 18%","source":"SoFi 8-K Q3 2026 earnings release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000065/a2026q3earningsrelease.htm","excerpt":"Technology Platform segment revenue declined 24% year over year to $87.4 million, reflecting the departure of a large client that completed its transition off the platform in 2025. Excluding that impact, segment revenue increased 18% from a year earlier.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 調整後淨營收指引上調至 $5.04B（+40%）；2027 初步指引約 $6.4B（約 +27%）","source":"SoFi Q3 2026 earnings (Zacks/Benzinga 彙整)","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000065/a2026q3earningsrelease.htm","excerpt":"The 2027 outlook represents approximately 27% adjusted net revenue growth and a net income margin of approximately 20%.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 會員 17.1M（+35%）、產品 26.7M（+44%）；管理層稱未見會員借貸/消費/儲蓄/投資放緩","source":"SoFi Q3 2026 earnings / TIKR","url":"https://www.tikr.com/blog/sofi-ceo-planned-for-two-rate-cuts-he-got-a-hike-then-raised-his-outlook-anyway","excerpt":"We are not seeing evidence of a slowdown in how many members borrow, spend… save, or invest.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"Lending 佔調整後淨營收 59%（去年同期 51%），收入結構向貸款集中；TD Cowen 分析師質疑個人貸款高速成長可持續性","source":"SoFi Q3 2026 earnings call (Zacks)","url":"https://www.zacks.com/stock/news/3017458/sofi-q3-earnings-call-highlights-raised-outlook-growth-plans","excerpt":"Lending made up 59% of adjusted net revenue in the third quarter, up from 51% a year earlier.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"Dolphin Research 估計 SoFi 個人貸款市佔由 2023 年約 6.8% 升至 2025 年底約 12%（LPB 驅動）；Truist 另有 >25% 估計，口徑不同、日期不明","source":"Dolphin Research (longportapp)","url":"https://longportapp.cn/topics/42280033","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K 列出的競爭者含「技術導向的替代放款業者」，但未點名具體取代性技術。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm","excerpt":"We face competition from a diverse landscape of consumer lenders, including other banks, credit unions and specialty finance lenders, as well as alternative technology-enabled lenders.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Galileo 一個重要客戶近期轉向競爭對手，且客戶集中。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm","excerpt":"Galileo and Technisys revenue from clients is highly concentrated and a significant Galileo client recently moved to a competitor.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子承認若未維持或改善技術與流程，解決方案競爭力會下降。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm","excerpt":"A failure to maintain and/or improve current technology and business processes could cause disruptions in our operations or cause our solution to be less competitive, all of which could have a material adverse effect on our business.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"SoFi 2026 年 Q1 loan platform fees 為 $138.3M，對應 $3.0B 為第三方發起的個人貸款；Q2 LPB 貢獻調整後淨收入 $143.3M，並擴及 SMB 貸款與房屋淨值貸款，屬輕資本、收費型的第三方發起/分銷通路。","source":"SoFi Q2 2026 earnings release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000050/a2026q2earningsrelease.htm","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2026-03-26 SoFi 宣布與多家新夥伴簽署 LPB 協議，預期交付逾 $3.6B 個人貸款，SoFi 賺取發起費並保留服務權。","source":"SoFi IR / Business Wire: SoFi Expands Loan Platform Business with Multiple New Agreements Totaling Over $3.6 Billion","url":"https://investors.sofi.com/news/news-details/2026/SoFi-Expands-Loan-Platform-Business-with-Multiple-New-Agreements-Totaling-Over-3-6-Billion/default.aspx","excerpt":null,"as_of":"2026-03-26","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"Technology Platform 分部 Q1 2026 營收年減 27%，公司歸因於大型客戶於 2025 年底前完全移出平台；Q2 營收 $84.5M 年減 23%。","source":"SoFi Form 10-Q Q1 2026 / Q2 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000037/sofi-20260331.htm","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 財報上修全年指引：調整後淨營收 $5.04B（前次 $4.75–4.85B）、EPS $0.61（前次 $0.60），並首度給 2027 指引（營收約 $6.4B、EPS $0.90）；Q3 調整後 EPS $0.18 vs 共識 $0.17","source":"SoFi 8-K Q3 2026 earnings release（SEC）；搜尋摘要彙整","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000065/a2026q3earningsrelease.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 財報（2026-07-29）後營收指引 $4.8–4.9B 高於約 $4.7B 共識，EPS 指引 $0.60 僅略高於 $0.59 共識；股價創 52 週新低 $14.88","source":"MarketBeat: SoFi updates FY 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/sofi-technologies-nasdaqsofi-updates-fy-2026-earnings-guidance-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師共識為 Hold；一聚合站（約 2026-08）21 位分析師平均目標價 $21.40；各來源目標價 $21–22.5 不一，日期與資料商不一致","source":"搜尋摘要彙整（TIKR/MarketBeat/TipRanks 等）","url":"https://www.tikr.com/blog/sofi-technologies-stock-dropped-40-in-2026-as-ebitda-rose-62-to-a-record-high-heres-what-analysts-say","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q1 後目標價下修：Truist $17（原 $20，Hold）、Morgan Stanley $16（原 $18，Sell）、Citi $30（原 $37，Buy）、Mizuho $29（原 $38）、Stephens $25（原 $26）","source":"搜尋摘要（Truist/Morgan Stanley/Citi/Mizuho/Stephens 動態）","url":"https://www.placera.se/telegram/sofi-technologies-morgan-stanley-lowers-price-target-on-sofi-technologies-to-16-from-18-keeps-underweight-rating-20260430","excerpt":"Morgan Stanley analyst Jeffrey Adelson lowered his price target to $16 from $18 and kept a Sell rating.","as_of":"2026-05-12","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026 年 Q2 SoFi 收購 Peach Finance 與 Composer Securities（10-Q 載明），另報導 5 月同意買 PrimaryBid 大部分資產（未經一手確認）。","source":"SEC EDGAR 10-Q（截至 2026-06-30）；Seeking Alpha 報導","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000054/sofi-20260630.htm","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026-03-17 Muddy Waters 發布放空報告質疑 SoFi 貸款會計與公允價值評價；SoFi 同日回應稱報告不實並考慮法律行動；CEO Noto 買進 28,900 股。","source":"SoFi 新聞稿 SoFi Responds to Inaccurate Short Seller Report","url":"https://www.businesswire.com/news/home/20260317128099/en","excerpt":null,"as_of":"2026-03-17","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2026-05-04 律所 Block & Leviton 公告調查 SoFi 是否違反證券法（律所徵求，非法院起訴）；搜尋未見已提起證券集體訴訟。","source":"Block & Leviton 新聞稿（Newsfile）","url":"https://www2.newsfilecorp.com/release/295852/SoFi-Technologies-Inc.-ALERT-Securities-Fraud-Investigation-by-Block-Leviton-Could-Allow-Investors-to-Recover-Losses","excerpt":null,"as_of":"2026-05-04","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"2025-12 公開增發 54,545,454 股、每股 27.50 美元，2026-01-05 行使超額配售後共售 57,754,660 股（資本事件，非 M&A/訴訟）。","source":"SEC EDGAR 8-K Item 8.01（2026-01-05）","url":"https://www.sec.gov/Archives/edgar/data/1818874/000181887426000003/sofi-20260102.htm","excerpt":"bringing the total aggregate number of shares sold in the Offering (including the Option) to 57,754,660.","as_of":"2026-01-05","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"financial_capital_credit_cycle#0","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"TransUnion Q2 2026：無擔保個人貸款借款人層級 60+ DPD 為 3.81%，高於去年同期 3.37%（產業層面信用略轉弱）","source":"TransUnion Q2 2026 data via search summary (consumer credit trends)","url":"https://newsroom.transunion.com/2026-consumer-credit-forecast/","excerpt":"Borrower-Level Delinquency Rate (60+ DPD) | 3.81% | 3.37% | 3.38% | 3.62%","as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#1","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"TransUnion Q2 2026：消費者層級 90+ DPD 升至 2.26%，主因次級人口增加","source":"TransUnion Q2 2026 consumer credit data via search summary","url":"https://newsroom.transunion.com/2026-consumer-credit-forecast/","excerpt":"Consumer-level delinquencies edged higher in Q2 2026, with consumers 90+ DPD rising to 2.26%. A growing subprime population largely drove the increase","as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"financial_capital_credit_cycle#2","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"Equifax：個人貸款逾期年減改善，但 2024 次級個人貸款 vintage 惡化","source":"Equifax April 2026 Consumer Pulse","url":"https://www.equifax.com/newsroom/all-news/-/story/april-2026-consumer-pulse-the-latest-consumer-credit-trends/","excerpt":"Credit risk dynamics are shifting as improvements in personal loans and private label delinquency are being countered by a rise in severe mortgage delinquency, alongside a worsening in subprime vintages for both Bankcard and unsecured personal loans through 2024.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"financial_capital_credit_cycle#3","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"Fed 信用卡 NCO：Q2 2026 3.70%（Q1 3.66%），與疫情前相近","source":"Creditors Bar: Q2 2026 Credit Card Charge-Offs Tick Higher","url":"https://www.creditorsbar.org/news/q2-2026-credit-card-charge-offs-tick-higher","excerpt":"The charge-off rate on credit card loans increased from 3.66% to 3.70%. The charge-off rate continues to be at a level similar to the pre-pandemic period.","as_of":"2026-08-15","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"financial_capital_credit_cycle#4","axis":"financial_capital_credit_cycle","section":"coverage","direction":"+","claim":"SoFi Q2 2026 個人貸款報告 NCO 2.62%（Q1 3.03%），調整出售逾期貸款後約 3.7%；維持累計淨損 7%-8% 指引","source":"SoFi Q2 2026 earnings release / 10-Q","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000050/a2026q2earningsrelease.htm","excerpt":"The personal loan annualized charge-off rate decreased 21 basis points year-over-year to 2.62%, which includes the impact of asset sales, new originations and delinquency sales in the quarter. The annualized charge-off rate decreased from 3.03% in the prior quarter.","as_of":"2026-07-28","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"financial_capital_credit_cycle#5","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"SoFi Q2 2026 備抵增加 $5.5M，主因信用卡餘額成長，部分被信用品質持續強勁抵銷","source":"SoFi Q2 2026 10-Q","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000054/sofi-20260630.htm","excerpt":"of $9.2 million and an allowance increase of $4.5 million. Net charge-offs of $9.2 million increased $2.7 million compared to the three months ended June 30, 2025, driven by higher average credit card balances. The allowance increase of $4.5 million primarily reflected growth in the credit card portfolio balances, partially offset by continued strength in credit quality of the portfolio.","as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"financial_regulatory_capital_rules#0","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"-","claim":"SoFi 合併 CET1 比率 2026-09-30 為 16.9%（要求下限 7.0%，含 2.5% 資本保全緩衝），自 2025 年底 22.8%、2026-06-30 18.7% 持續下降；搜尋未見最低要求本身在 2026 有變動","source":"SoFi Q3 2026 earnings release 8-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000065/a2026q3earningsrelease.htm","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_regulatory_capital_rules#1","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"SoFi Bank 層級 CET1 2026-06-30 為 15.2%，對應 7.0% 要求下限與 6.5% well-capitalized 門檻","source":"SoFi 10-Q for period ended 2026-06-30 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000054/sofi-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"financial_regulatory_capital_rules#2","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"2026-03-19 Fed/FDIC/OCC 撤回 2023 年 Basel III endgame 提案並重新提出較輕版本；意見期於 2026-06-18 截止，未見最終規則；參議院銀行委員會 2026-06 來函要求撤回提案","source":"Simpson Thacher: Basel III Endgame Evolution — Banking Agencies Propose Major Capital Overhaul Again","url":"https://www.stblaw.com/about-us/publications/view/2026/03/20/basel-iii-endgame-evolution-banking-agencies-propose-major-capital-overhaul-again","excerpt":null,"as_of":"2026-03-20","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026 年 Q2 SoFi 收購 Peach Finance 與 Composer Securities（10-Q 載明）；另有 PrimaryBid 資產收購報導（5/11，未經一手確認）。條款未披露。","source":"SEC EDGAR 10-Q（截至 2026-06-30）；Seeking Alpha","url":"https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000054/sofi-20260630.htm","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026-05-04 律所 Block & Leviton 公告調查潛在證券法違反（連結 3/17 Muddy Waters 報告與 4/29 財報後跌逾 13%）；未見已提起證券集體訴訟。","source":"Block & Leviton 新聞稿（Newsfile）","url":"https://www2.newsfilecorp.com/release/295852/SoFi-Technologies-Inc.-ALERT-Securities-Fraud-Investigation-by-Block-Leviton-Could-Allow-Investors-to-Recover-Losses","excerpt":null,"as_of":"2026-05-04","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"SOFI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":-222.21,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SOFI","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"COF","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":45.04,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COF","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ALLY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":14.38,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALLY","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"LC","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LC"},"note":"quarterly_income_stmt 無資料"},{"name":"HOOD","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":81.44,"operating_margin_pct":45.65,"fcf_margin_pct":58.44,"rd_intensity_pct":19.34},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"SOFI"},"financial_history":{"ticker":"SOFI","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":1573535000.0,"revenue_yoy_pct":null,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":-320407000.0,"diluted_eps":-0.4,"free_cash_flow":-7359591000.0,"fcf_margin_pct":-467.71,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":2108215000.0,"revenue_yoy_pct":33.98,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":-300742000.0,"diluted_eps":-0.36,"free_cash_flow":-7348331000.0,"fcf_margin_pct":-348.56,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2612342000.0,"revenue_yoy_pct":23.91,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":498665000.0,"diluted_eps":0.39,"free_cash_flow":-1283424000.0,"fcf_margin_pct":-49.13,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":3613354000.0,"revenue_yoy_pct":38.32,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":481320000.0,"diluted_eps":0.39,"free_cash_flow":-3993575000.0,"fcf_margin_pct":-110.52,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/SOFI/SOFI_Q3_2026_Earnings_Call_20261027.md）

# Q3 2026 Earnings Call
**SoFi Technologies, Inc.** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Good morning. My name is Hillary, and I will be your conference operator today. At this time, I would like to welcome everyone to the SoFi Technologies Third Quarter 2026 Earnings Conference Call. [Operator Instructions] And with that, we may begin your conference.

**Unknown Executive** (Executives):
Thank you, and good morning. Welcome to SoFi's Third Quarter 2026 Earnings Conference Call. Joining me today to talk about our results and recent events are Anthony Noto, CEO; and Chris Lapointe, CFO. You can find the presentation accompanying our earnings release on the Investor Relations section of our website.
Unless otherwise stated, we'll be referring to adjusted results for the third quarter of 2026 versus the third quarter of 2025. Our remarks today will include forward-looking statements that are based on our current expectations and forecasts and involve risks and uncertainties. These statements include, but are not limited to, our competitive advantage and strategy, macroeconomic conditions and outlook, future products and services and future business and financial performance.
Our GAAP consolidated income statement and all reconciliations can be found in today's earnings release and the subsequent 10-Q filing, which will be made available next month.
Our actual results may differ materially from those contemplated by these forward-looking statements. Factors that could cause these results to differ materially are described in today's press release and our subsequent filings made with the SEC, including our upcoming Form 10-Q. 
Any forward-looking statements that we may make on this call are based on assumptions as of today. We undertake no obligation to update these statements as a result of new information or future events. And now I'd like to turn the call over to Anthony.

**Anthony Noto** (Executives):
Good morning, everyone. SoFi delivered an exceptional third quarter by any measure. We achieved 35% growth in members and 44% growth in products, leading to another quarter of accelerating revenue growth, reaching $1.4 billion, up 44% versus Q3 2025 and adjusted EPS of $0.18.
These are strong results in any environment, but they're even more remarkable when considering how 2026 has turned out. Nine months into the year, the environment looks different than what we expected in January. Our original 2026 guidance assumed 2 rate cuts. Instead, we've already had one rate hike. And today, we are positioned for 2 more rate hikes this year.
The good news is we are executing as well as we ever have. In fact, I now have as much confidence in our ability to drive durable growth in a high rate environment as I do in a low rate environment. Given the momentum in the business and our ability to execute in a higher rate environment, we are raising our full year 2026 guidance to reflect our Q3 outperformance and higher expectations for Q4.
We now expect 2026 adjusted net revenue of $5.04 billion, up 40% year-over-year and higher than our prior guidance range of $4.75 billion to $4.85 billion, adjusted EBITDA of $1.66 billion, which implies a 33% margin versus $1.6 billion previously; adjusted net income of $840 million and a 17% margin versus $825 million previously; and adjusted EPS of $0.61 versus $0.60 previously. This guidance implies Q4 revenue of approximately $1.375 billion, which equates to year-over-year growth of 36%, adjusted EBITDA of $492 million, adjusted net income of $276 million, which is a 20% net income margin and adjusted EPS of $0.19. Momentum across the business is broad-based and visibility remains strong, giving us confidence to provide preliminary 2027 guidance above our previous outlook.
After exceeding our 2026 original revenue guidance by $385 million, we now expect to achieve $6.4 billion in 2027 adjusted net revenue, which is 27% year-over-year growth. We also expect to deliver continued strong improvement in profitability with EBITDA margin increasing to approximately 35%, resulting in $2.240 billion of adjusted EBITDA.
We expect adjusted net income of $1.28 billion, reflecting a net income margin of approximately 20% and earnings per share of $0.90. And as Chris will walk you through, our plan is funded by our organic capital generation without the need for raising additional capital.
With expected 2026 revenue of $5 billion, we have reached sufficient scale and revenue and diversification across the individual businesses that only requires someone to understand the trends in our member growth, product growth and revenue per product to assess and forecast the business.
Importantly, we allocate our resources to these 3 measurements to grow our business and execute our strategy. Clearly, each business has unique drivers of its respective revenue per product, but the trend over the last 2-plus years illustrates a modest range and strong durability for these metrics.
Our focus is simple: more members, more products and more optimized revenue per product to create the most value for our shareholders over the long term. Starting this quarter and going forward, we're going to consistently talk about our business through the lens of these 3 drivers that matter most to our long-term value. How many members we serve, how many products each member uses and thus total products and how much revenue we generate per product.
Growth in members and products per member reflects the strength of our financial services productivity loop and the compounding effect it has on growth. It is also a critical reason we have achieved greater than the Rule of 40 for 20 consecutive quarters. Revenue per product reflects how well we monetize each relationship, which includes many variables, the most important of which are NIM and credit and lending, deposits and spending in SoFi Money, balances and spending in credit card and return on assets and invest.
Together, they drive durable revenue growth, lifetime value and our path to 20% to 30% returns on tangible common equity, and we'll report on them consistently every quarter. Now on to our results. Member activity remains very strong. We continue to track above-average earners while spending, saving and investing trends remain positive. Credit performance once again improved and remains firmly in line with our expectations with all-in personal loan net charge-offs of 3.4%.
We are not seeing evidence of a slowdown in how many members borrow, spend, save or invest. The third quarter demonstrated the continued strength of our strategy, achieving a Rule of 40 score of 79 when combining revenue growth of 44% and an EBITDA margin of 34%, marking the 20th consecutive quarter of exceeding the Rule of 40.
We grew members 35% year-over-year to 17.1 million. Total products increased approximately 44% year-over-year to 26.7 million. 51% of new products in the quarter were once again opened by existing members. Products continue to grow faster than members and products per member increased to approximately 1.56 compared to 1.47 a year ago. This reflects deeper engagement with our platform, continued growth of products per member across our cohorts and the increasing strength of our financial services productivity loop strategy.
Adjusted EBITDA reached a record $470 million, up 70% year-over-year and a record margin of 34%, while adjusted net income reached $243 million, up 74% versus the prior year period and at a record adjusted margin of 18%. Adjusted earnings per share were $0.18, up 64% year-over-year and 50% sequentially.
Our revenue mix continues to diversify toward our long-term goal of generating 50% of revenue from fee-oriented businesses. Total Q3 fee-based revenue was $571 million, representing 42% of total revenue compared to 39% in the second quarter.
The Lending segment generated approximately $807 million of adjusted net revenue. Lending net interest income was $607 million, reflecting a strong consolidated net interest margin of 6.14%, which was up 16 basis points sequentially. This also reflects the continued benefit of loan growth, higher returns from interest collected as cash payments on our loans than our fair value marks with lower-than-expected losses in our deposit funded balance sheet.
We generated a record $16.9 billion of total loan originations. Loan platform business originations reached approximately $3.8 billion, up $704 million from the second quarter, providing additional capacity to serve member demand while expanding our capital-light fee-based revenue opportunity.
Lending product growth remains strong and broad-based. Total lending products increased approximately 39% year-over-year to 3.4 million. Personal loan products grew 45% year-over-year. Student loan products grew 22% year-over-year and home loan products grew 50% year-over-year.
Lending revenue grew faster than lending products, reflecting the increasing monetization of our lending relationships. Using period-end products, annualized lending revenue per product increased to approximately $942 in Q3 compared with $782 in the third quarter of 2025. Financial Services revenue reached approximately $525 million, up 25% year-over-year. Financial Services products grew 44% year-over-year to 23.2 million. Within our Financial Services segment, Money and Relay continue to drive the greatest absolute growth with both reaching over 8 million products. Year-over-year, they grew 34% and 45%, respectively.
We are achieving attractive growth rates in other products as well. Invest grew 37% year-over-year, reaching over 4 million products. Credit card products increased 67% year-over-year to approximately 656,000 with a high percentage of primary card users and strong credit performance.
We also ended the quarter with over 500,000 crypto products and approximately 275,000 SoFi Plus subscribers. The breadth of products gives us multiple ways to acquire members, deepen engagement and create additional monetization opportunities.
Using period-end products as a simple proxy, annualized financial services revenue per product increased to approximately $90 in Q3 compared with $88 in the second quarter, with credit card and crypto seeing the greatest increase in monetization.
The improvement reflects the continued monetization of our member activity through deposits, spending, brokerage, lending referrals, subscriptions, effective interest rate on credit card balances and other fee-based services. As our products season, we see additional opportunities to increase revenue per product through higher balances, greater transaction activity, increased assets under management and additional cross-buy. SoFi Plus is the ultimate example of this model.
Not only does the product create a recurring revenue stream of $120 per product per year, but it also increases engagement across Money, Invest, Relay and Lending.
In fact, approximately 83% of SoFi Plus members were existing SoFi members and 25% of those members added another product after subscribing to SoFi Plus. There is no better example of the financial services productivity loop at work than SoFi Plus, and we remain confident that we can scale SoFi Plus to more than 1 million members as we continue to add to the value proposition and increase awareness among existing members.
Our Financial Services segment revenue growth is, therefore, coming from both volume and monetization. We're adding more members, increasing the number of products each member uses and expanding the revenue generated by those products. This creates a powerful flywheel. Broadly used financial services products help us acquire members efficiently.
Deeper engagement creates additional product adoption. Lending and fee-based products then allow us to monetize those relationships through both recurring net interest income and capital-light revenue streams. Our product growth reflects our ability to drive continuous innovation via our technology platform and brand building.
Importantly, our technology platform not only supports our product growth and member services, it's also an attractive business in its own right. Technology Platform segment revenue totaled $87 million in the quarter, down 24% year-over-year, primarily due to the previously disclosed transition of a large client.
Excluding revenue from that client in both periods, Technology platform revenue grew 18% year-over-year. We remain confident in our ability to return to 25% revenue growth in a steady state for the technology platform business.
We remain focused on increasing monetization of existing relationships and expanding the platform across issue processing, financial and banking cores and ledgers, payments and risk and fraud. As we approach the end of 2026, our conviction has never been greater. The results we're reporting today and the increased optimism we have for the future reflect the strength of SoFi's model. We've proven that as our member base scales, our product ecosystem becomes broader, engagement increases and the opportunity to generate revenue from each relationship expands.
That compounding dynamic is strengthening the durability of our success and increasing the lifetime value of our members, allowing us to achieve significant growth, improving profitability and returns in both rising rate and declining rate environments. Let's not forget how far we've come in less than a decade.
In 2018, we were largely a single product company built around student loan refinancing with roughly 650,000 members, a tiny fraction of the 17.1 million members we serve today.
Since then, we have completely transformed SoFi's culture, business and impact on members. Our team has been relentlessly focused on our Everything financial app strategy and has built fully scaled businesses in Money, Invest, Relay, credit card and the loan platform business in just a few years.
We became a nationally chartered bank, and we significantly scaled our lending franchise across personal loans, home loans and in-school loans. And in the last year, we have funded a new batch of start-up businesses in SoFi Crypto, SoFi Plus, small, medium business lending, Big Business Banking, SoFi Pay and SoFiUSD.
And because of that unwavering focus, we now serve 26.7 million products and no single product defines us. In fact, 87% of our products are financial service products, not lending.
Each of our businesses is built to grow on its own and make every other business stronger. Not too long ago, achieving $100 million in annual revenue was the milestone companies needed to achieve to go public. SoFi now has 8 distinct businesses that each have more than $100 million in annualized revenue and are still growing at over 30% year-over-year in almost all cases.
Specifically, we have one business with more than $2 billion in annualized revenue. We have one business with more than $1 billion in annualized revenue. We have 3 businesses with more than $300 million in revenue and 3 businesses with more than $100 million in revenue. That is 8 proven scale businesses that will drive our growth for decades to come, not to mention the new start-up businesses that I mentioned, which are not yet part of the Great 8, but have higher growth in earlier-stage revenue such as SoFiUSD, Big Business Banking, SMB, SoFi Plus and Crypto.
The ambitions we had for SoFi were bold in 2018, and our ambitions for the future of SoFi and the impact we can have in the lives of our members and clients are even bolder today.
Not everything we do will be successful but our unwavering focus and execution have been critical in beating the 1% odds that a business can reach $100 million in revenue, not just once but 8 times. Today, less than a decade later, we see a clear path to achieving 100 million products by the end of 2030, which is a 4x increase from where we stand today.
Our plan to reach that 100 million products by 2030 also includes having 5 of our businesses generating $1 billion in revenue or more, 5 more businesses generating at least $500 million in revenue and another 5 generating at least $100 million in revenue.
Achieving our bold objectives will require our team to challenge not only the norms of the industry, but even the norms we have created over the last 8 years by continuously innovating to create unmatched value for our members. I hope this provides a more tangible and quantitative perspective on what the future holds for SoFi and the clear path to these bold ambitions.
Our improved outlook is rooted in 3 primary drivers: more members using more products, generating more revenue per product. That is the engine behind our durable growth and our path to 20% to 30% returns on tangible common equity. We've had unprecedented performance thus far in 2026 and have great visibility for continuing to 2027 and beyond. With 17.1 million members, we are still early in a very large long-term opportunity. With that, I'll turn it over to Chris.

**Chris Lapointe** (Executives):
Thank you, Anthony. Before I walk through the numbers, I want to address 2 things: how we are putting our balance sheet and excess capital to work and how our business model performed in a rate environment very different from the one we planned for.
First, balance sheet and capital. Member demand for our loans continues to be strong, and our strategy of how we split the mix of balance sheet loans versus LPB continues to deliver attractive returns. With strong credit and risk-adjusted margins, loans on the balance sheet continue to deliver durable and recurring net interest income that compounds over time.
In fact, in the third quarter, we generated $1.4 billion of cash revenue, including $927 million from net interest income, our fourth straight quarter above $1 billion of cash revenue. This built-in recurring cash revenue gives us better visibility into future revenue. The investments we made in Q1 and Q2 are now delivering 34% EBITDA margins and 18% net income margins and provide sufficient organic capital generation to fund our lending business in 2027 and beyond.
We are doing this from a position of strength. Our total capital ratio of 17% remains well above the regulatory minimum of 10.5% and our internal stress buffer, giving us significant excess capital to keep investing in high-returning growth. We are now at the point where our current capital position, in addition to our organic capital generation is sufficient to fund our business and our planned growth in 2027.
For clarity, our 2027 guidance does not require raising additional capital and no capital raise is assumed or needed in what Anthony laid out. We are confident we can execute that plan organically given the balance sheet we have built, the capital we will generate organically from the business and the position we are in today. Second, on the current macro environment. Despite the unexpected rate environment we confronted this year, we delivered our third consecutive quarter of more than 40% revenue growth are raising our full year guidance and giving 2027 guidance 1 quarter earlier than usual.
As Anthony mentioned, we now have as much confidence in delivering strong growth in a high rate environment as we do in a low rate environment. Our hedges were highly effective in a volatile rate environment. We had over $800 million of fair value losses, which were largely offset by about $734 million of hedge gains. This is clear evidence the program worked as intended as the hedge gain offset the move in benchmark rates, while the remainder of the fair value impact was driven by other inputs, which our hedges are not designed to cover.
Our exceptional growth year-to-date and high confidence and visibility on future performance demonstrate that our business model is resilient to rate volatility. That's because of our model and our consistent focus on the 3 drivers that create the most long-term value for shareholders, delivering more members, more products per member and higher revenue per product. Q3 demonstrated strength on all 3.
So let me start with members. Member growth is the foundation of our financial results, driving both future revenue and our low-cost deposit funding. For the third quarter, we ended with 17.1 million members, up 35% year-over-year, and we added a record 1.2 million members.
As members deepen their relationship with SoFi, product growth continues to outpace member growth. Over time, that lowers our acquisition cost per product and raises the lifetime value of each member. For the third quarter, total products grew 44% year-over-year to 26.7 million. We added a record 2.2 million products. Products per member rose to 1.56 from 1.54 last quarter and 1.47 a year ago. Approximately 51% of new products came from existing members and 37% of members now use 2 or more products, up from 33% a year ago.
Revenue per product shows how well we monetize those relationships and it increased in both financial services and lending this quarter. We calculate revenue per product as annualized quarterly segment revenue divided by period-end products. Financial services annualized revenue per product was approximately $90, up from $88 last quarter. This was driven by interchange, credit card and SoFi Plus subscription revenue.
Lending annualized revenue per product was approximately $942, up from $920 last quarter. This was driven by growth in net interest income and loan origination fees. Together, more members, more products per member and higher revenue per product drove our 44% adjusted net revenue growth this quarter.
Turning now to our segment performance, starting with lending. For Q3, these strong results were driven by growth in net interest income, which increased 57% year-over-year to $670 million. The balance of our growth came primarily from loan origination fees, which were $271 million, up 2.6x year-over-year.
During the quarter, we saw continued record member demand for our lending products. Personal loan originations were a record $12.6 billion, of which $9 billion was originated for the balance sheet. Our core personal loan product generated a roughly 7.6% risk-adjusted margin in Q3.
This consisted of a weighted average coupon of 12.8%, and origination fee yield of 1.4%, funding costs of 3.1% and annualized losses of 3.4%. Our ability to generate loans with attractive risk and reward profiles supports our strong revenue growth through both balance sheet lending and our loan platform business. Student loan originations were $2.9 billion, up 96% from the same period last year. And home loan originations were $1.4 billion, up 44% from the prior year. Turning to Financial Services.
For the third quarter, net interest income for this segment was $281 million, up 38% year-over-year, which was primarily driven by growth in member deposits. Noninterest income grew 13% year-over-year to $244 million for the quarter. During the quarter, we achieved record interchange fee revenue in our Financial Services segment of $52 million, which was up 77% year-over-year and driven by $31 billion in total annualized spend across money and credit card.
We also achieved strong brokerage fee revenue of $18 million, which was up 47% year-over-year. Credit card, in particular, has been a bright spot, and we believe we've cracked the code on profitable customer acquisition and growth. This is evidenced by credit card revenue almost doubling from last quarter.
In Q3, we originated approximately $3.8 billion of personal loans, home equity loans and small business loans on behalf of our LPB partners. That, combined with our referral fees and servicing resulted in $153 million of total LPB revenue, up from $3.1 billion in originations and $143 million in revenue last quarter.
We also took a significant step forward with LPB by transferring our first SMB and home equity loans through the platform. LPB monetization is driven by several factors, including mix of assets transferred, excess supply and demand as well as timing and structure of new partnerships and extensions.
This is a great product for us as it allows us to serve more members in a capital-light manner, and our overall goal is to maximize variable profit. As a result, monetization will fluctuate from time to time. Shifting to our Tech Platform segment. For the quarter, Tech Platform revenue was approximately $87 million, down 24% year-over-year from the transition of a large client. Excluding revenue from that client, revenue grew 18% year-over-year.
Revenue growth was driven by further monetization of existing clients as well as contributions from new clients. Year-to-date, we've added 9 clients, which will continue to grow over time. Turning to our balance sheet. In the third quarter, total assets grew by $6.8 billion. This was driven primarily by $5.8 billion of loan growth and roughly $1 billion of growth in cash, cash equivalents and investment securities.
Total company-wide cash at quarter end was $3.6 billion. At the end of the third quarter, our personal loans were marked at 103.3%, down approximately 140 basis points from the prior quarter. Our student loans were marked at 101.9%, down approximately 240 basis points from the prior quarter. And our home loans were marked at 101.5%, down approximately 330 basis points from the prior quarter.
In each case, the decline was primarily driven by a higher discount rate. Collectively, there was over an $800 million negative impact from fair value marks, which was primarily offset by hedge gains during the quarter. On the liability side, total deposits grew by $5.8 billion to $51.3 billion, which included strong growth in member deposits.
Member deposit growth reflects more members choosing SoFi as their primary bank, and that funding base lets us grow higher returning assets across our lending products. Our net interest margin was 6.14% for the quarter, up 16 basis points sequentially. This included a 22 basis point increase in average asset yields, partially offset by a 1 basis point increase in cost of funds.
We continue to expect a healthy net interest margin above 5% for the foreseeable future. Tangible book value grew $2.5 billion year-over-year to $9.7 billion. The tangible book value per share at quarter end is $7.48, up from $5.97 a year ago, a 25% increase.
This quarter, we generated a return on tangible common equity of approximately 10%. We're reaching that level while still holding significant excess capital and growing the top line over 40%, and we see a clear path to higher returns as we put that capital to work as our business scales. Turning to credit performance. Consistent with Anthony's comments on the overall health of the consumer, our credit performance remains very strong overall, performing in line with expectations and driving attractive risk-adjusted returns across all loan types.
For personal loans, we saw a very strong credit performance for the quarter. Excluding the impact of delinquent loan sales, the estimated all-in annualized net charge-off rate was 3.4%, down approximately 80 basis points year-over-year and 30 basis points sequentially.
This was driven by an improvement in the underlying credit performance as well as growth in average loans on the balance sheet. The on-balance sheet 90-day delinquency rate was 42 basis points, in line with the last quarter and the third quarter of 2025. For student loans, the annualized charge-off rate was 63 basis points, down 6 basis points from the prior year and up 2 basis points sequentially.
The on-balance sheet 90-day delinquency rate was just 13 basis points, in line with last quarter and the third quarter of 2025. In terms of our regulatory capital ratios, we're very well capitalized. Our total capital ratio of 17% at quarter end is well above the regulatory minimum of 10.5% as well as our additional internal stress buffer.
Similar to last quarter, we continue to deploy excess capital into high-returning loans, bringing our total capital ratio down by 180 basis points sequentially as we normalize toward the low to mid-teens while remaining well above regulatory minimums. Let me finish with some additional color on our 2026 and 2027 guidance. 
For Q4 2026, on a segment level, we expect approximately $785 million of revenue in Lending, $550 million of revenue in Financial Services, $90 million of revenue in Technology Platform and corporate revenue in line with the third quarter for total adjusted net revenue of approximately $1.375 billion.
For 2027, our preliminary outlook assumes 2 rate hikes in the year and a 24% effective tax rate. Overall, Q3 was a strong quarter, and we continue to have strong momentum in our business, more members, more products and rising revenue per product showing up in revenue, margins and returns. Let's now begin the Q&A.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of John Hecht from Jefferies.

**John Hecht** (Analysts):
SMB lending, it's a relatively new category for you guys. It seems like it's got a lot of momentum and a decent amount of strategic focus. Maybe take us Anthony, through what is the specific target market within SMB and the characteristics of the borrowers? And how do we think about, call it, the prioritization of that as we go into 2027?

**Anthony Noto** (Executives):
Thank you, John. First thing I'd say is the SMB business is at a very nascent stage. We have driven revenue over the last, call it, 5 years from lead referrals in the small and medium business.
It really started when we hit COVID and the government was providing PPP loans for SMB companies, and we were having a lot of people come to SoFi looking for those loans, which we didn't provide at the time. We quickly stood up an HTML page for people to apply for the PPP application, and we realized there was a big opportunity in our existing consumer customer base to also provide SMB loans to them as many were small business owners.
Over that 5-year period, we've kind of incrementally invested at a very low rate. Think of it as a seed investment to see if we could grow the business. It reached the scale in 2025 that it was clear to us, it was time to become a principal in the business. And that's not just lending, but it will also be other products and services outside of lending, including checking and savings, et cetera.
And so we launched that business as a principal in 2026. I don't want anyone to think it's one of the Great 8. It's not one of the 8 businesses that are generating annual revenue of over $100 million. It's still a start-up business. But as you mentioned, it has great prospects and one we'll invest in over time and we'll continue to grow.
But getting the credit right is important, building relationships and the unit economics are important. Why? Because these are high repeat customers. Businesses need capital to grow. When they take out a loan, it helps them grow. That gives them motivation and economic incentive to take out another loan and then another loan.
And just like the largest corporations in our country, that capital fuels the growth. And so we want to make sure we build relationships, first and foremost, achieve the right unit economics, and we continue to expand that over and over on a nice linear line. So we're really pleased with where we are, but it's nowhere near where it will be in the future.

**Operator** (Operator):
Your next question comes from the line of Kyle Joseph from Stephens.

**Kyle Joseph** (Analysts):
Just want to hone in on the '27 outlook a little more. If you could walk us through some of your high-level assumptions in terms of how you're thinking about each segment contributing to those -- to that outlook?

**Anthony Noto** (Executives):
Before Chris gives you the particulars, I just want to add a couple of points. This is a change in behavior for those that have been following us as a public company. We didn't change our behavior because we had the same visibility we've had in the past.
We changed our behavior because of the visibility that we have. We made a concerted effort throughout this year to invest in long-term durability of growth. You hear us reference it's exceeding the Rule of 40 for 20 consecutive quarters.
At the end of 2025, when we looked at the incredible growth opportunities we had in front of us that weren't currently funded in 2026, we made a conscious decision to accelerate our investment in those start-up businesses that are not in the Great 8. We needed to drive revenue that would cover those expenses and still deliver the earnings that we had previously given an outlook for in 2026 and beyond.
We sit here now in 2026 with $1.4 billion reported in Q3 of revenue. That's -- we also generated $1.4 billion of cash revenue in the quarter, which means we've built a sustainable top line revenue number that can allow us to continue to invest into the future and not just invest in the future in the new businesses, but deliver to the investors greater profitability.
Our net income margins for 2027 are 20%. We will still be growing significantly faster than any other financial services company and many technology companies in 2027 when hitting the low bound range of our long-term net income margins and the mid-range of our long-term EBITDA margins.
And so we're going to continue to deliver both revenue growth and good profitability growth with expanding margins. And most importantly, we'll continue to move up towards our goal of return on tangible common equity of 20% to 30%. There's been no point in the company's history that we're at right now where we control our own destiny more than we have in the past and our conviction on our business and the visibility of our business is as strong as it is to give you guidance at the end of the third quarter of '26 for all of 2027. Chris, let's go through the segment.

**Chris Lapointe** (Executives):
Yes. In terms of the overall '27 guidance as it relates to the segments, we're expecting lending to grow 25% year-over-year. We're expecting Tech Platform to return to growth of 25% year-over-year, and we're expecting our Financial Services segment to grow 35% year-over-year.
And from a margin perspective, we're expecting a margin profile generally in line with where we are from a segment perspective right now.

**Operator** (Operator):
Your next question comes from the line of Andrew Jeffrey from William Blair.

**Andrew Jeffrey** (Analysts):
I like the focus on the ARPU KPI and obviously, member growth has been fantastic. Anthony, can you sort of dimensionalize TAM for us? I think you've talked about 40 million to 50 million potential members. Where does ARPU go? I mean, can we think about this ultimately is somewhere in the neighborhood of a $30 billion TAM? How are you guys thinking about that over the next several years?

**Anthony Noto** (Executives):
Yes. And I don't mean to correct you, but I just want to make sure people understand the difference. Typically, when the word ARPU is used as an acronym, it's average revenue per user.
Our monetization metric that we referenced in the earnings call, and we've referenced in the past is revenue per product, not per user. And obviously, a member is our user definition and the products per member are greater than 1 and their revenue per product is on an individual product basis.
What I'd say is this, you have to look at 2 different levels. One, we shared with you the annualized revenue per product rates for lending and the annual revenue per product for non-lending FIS businesses. And so there's a lot of upside in many of our individual businesses, and I'll kind of walk through them.
On the financial services side, we have significant upside in revenue per product in invest. The ratio of the revenue that we generate relative to our assets there is well below benchmarks. That will increase based on a number of factors: one, increased assets in that account; two, more products and services, which will also bring in more assets that involve fees.
So certain retirement accounts and trust accounts are very attractive from a revenue relative to AUM standpoint. In addition to that, we'll continue to benefit from more activity across the products in each individual account. So obviously, options and margin create more revenue per asset than the rest of the revenue streams.
And those are products that people don't use when they first open an account. Many of our investors are new and novice investors, but they quickly become very talented investors and very astute to the different ways to drive returns.
And so that's on the invest side. The credit card side, we're just getting started. The monetization of the credit card business is really kicking in. We've developed a very good playbook, which I won't go into detail because I don't want anyone to copy in the credit card business, but we're building our credit card business in a responsible way, and we feel like we've now the ability to leverage the financial services productivity loop to not just acquire new card members, but for those card members to become -- to use our card as Apple Wallet from a primacy standpoint and our effective interest rate there is going up by the day because we're not utilizing the very costly [ 0% ] balance transfer initiatives to do that.
So a lot of upside in credit card as that effective interest rate goes, but also as balances increase. In SoFi Money, as deposits grow, our monetization within SoFi Money increases, and we continue to see increasing deposits on a per account basis as it relates to that. Someone mentioned or John asked a question about the SMB business, significant monetization opportunity as it relates to that.
Our LPB business, the monetization is going to be relatively range bound. So I wouldn't put a lot of expectations around that. SoFi Plus, great monetizing business. We will add more products and services to that over time. Today, it's $10 per month. You could see us adding some premium services that have average revenue per product on top of that.
As you think about the lending businesses, I would say they generally are pretty stable. Personal loans, student loans, in-school loans and home loans are all relatively stable as it relates to revenue per product. There's a lot that goes into that. Obviously, the average loan size, the weighted average cost of capital -- the weighted average coupon that we charge, the loss rates that we have and our cost of funds impact all of that.
But they're relatively stable and an easier way to kind of forecast the revenue that we generate off of the assets on our balance sheet as it relates to loans. But I do want to make the broader point. The weighted average revenue per product will likely come down over the time period of 2026 to 2030 because the mix of the lower revenue per product businesses is going to grow faster and increase relative to the higher revenue per product businesses in lending. That's not a bad thing. It's not a bad thing because that's more than offset by the growth in products of those financial services businesses versus the growth of the products in the lending business.
In totality, we believe we have a competitive advantage with the highest lifetime value, which allows us to deliver the best rates on loans, the best rates on checking and savings, the best products and services you can get outside of the products with free certified financial planners and other things are great value in SoFi Plus.
So I would think about the products growing, as we mentioned, to $100 million. I would think about the members growing to a point of at least getting to 2 products per member. And then in addition to that, you can keep average revenue per product flat to slightly down. Our own individual forecast has it down, but it's going to depend on the mix.

**Operator** (Operator):
Your next question comes from the line of Dan Dolev from Mizuho.

**Dan Dolev** (Analysts):
Excellent results today. Congrats. Maybe, Chris, can you expand a little bit more on the ability to fund 2027 growth organically?

**Chris Lapointe** (Executives):
Sure. Thanks, Dan. So Anthony made this point on the call, and I reiterated it, but our 2027 outlook is going to be funded organically through 2 levers.
First is utilization of existing excess capacity. And the second is through organic capital creation through our expanded earnings that we outlined. So in terms of that first lever, today, we have about $9.6 billion of equity capital that's Tier 1 plus Tier 2 capital, and that translates to about $71 billion of risk-weighted asset capacity, and that's assuming a 13.5% risk-based capital ratio.
And that's $15 billion above where we are today at $56 billion of risk-weighted assets. In terms of the second lever, organic capital creation, we just guided to approximately $270 million of net income in the fourth quarter and $1.28 billion of full year 2027 net income.
And that earnings plus stock-based compensation translates to approximately another $14 billion of incremental risk-weighted asset capacity at that same risk-based capital ratio of 13.5%. So between the 2 levers that we have, we have about $29 billion of risk-weighted asset capacity, which is not planned for nor required to meet our 2027 guidance.
As we look beyond 2027, our continued expansion in ROEs as well as organic capital creation is what's going to bind and support our overall growth.

**Operator** (Operator):
Your next question comes from the line of Devin Ryan from Citizens Bank.

**Devin Ryan** (Analysts):
A question on interest rates and implications on the model. Obviously, this year has developed differently than you thought a few months ago even and going back to the beginning of the year as well with rates continuing to kind of bounce around here. 
But you're still performing quite well on that front. And so as we think about a world where rates potentially shift again and potentially lower, how should we think about the other side of that equation? The hedge portfolio seems like it's working quite well. Would lower interest rates or abrupt change from here still be a tailwind to the model? Or are there other offsets just based on how you guys are set up?

**Anthony Noto** (Executives):
So I'd say 2 things. First, the last time rates went up prior to this, I would say, last 18-month time period, we actually slowed our growth because I was concerned about the macroeconomic environment and higher for longer.
Part of that decision was also based on what the state of our other businesses were outside of lending and what our capital position was. We had a very unique opportunity in 2026 to test our ability to grow through a higher rate environment and how the business would perform. What afforded us that opportunity is that we had a lot more capital on our balance sheet.
Our business was a lot more diverse, and we can lean into it to see if we had the ability to raise the weighted average coupon that we charge relative to the higher benchmark rates to offset that and keep our unit economics where they were, in addition to also hedging the business.
And what I said in my comments is exactly how I feel. I think we can operate just as well in a high rate environment as we can in a low rate environment. You never know what you can truly do until you get there, but the results are very clear. Growing revenue at 44% faster than we did in the prior 2 quarters of the year with rates being the most volatile that they have been is a true testament to the demand for our products and our ability to meet that demand very well.
So in a lower rate environment, there are businesses that do better than others. The housing market will pick up meaningfully. That is a low capital business. So in some ways, it becomes a better margin business with less capital because those are agency mortgages that we don't have to hold on our balance sheet. That said, they don't contribute to the visibility of earnings the way the personal loans do or student loans given the duration of those loans relative to the home loans going off the balance sheet.
So there will be gives and takes, but our outlook that we've provided is one that we can deliver if rates stay where they are and go higher and we can deliver if rates go lower. And I'll let Chris add in any particulars.

**Chris Lapointe** (Executives):
Nothing else to add.

**Operator** (Operator):
Your next question comes from the line of Patrick Moley from Piper Sandler.

**Patrick Moley** (Analysts):
Chris, maybe just following up on the segment framework you laid out. If I take the 2026 guide at the 4Q segment level and then apply the growth rates that you gave there for 2027, I guess something like $6.7 billion, which is about $300 million above the guide. So maybe could you just help me square that difference? Is that just a step-up in the corporate line? Or is it conservatism that you baked into that number?

**Chris Lapointe** (Executives):
Yes. Yes. There's a slight uptick in the corporate line is the direct and straightforward answer.

**Operator** (Operator):
Your next question comes from the line of Kyle Peterson from Needham.

**Kyle Peterson** (Analysts):
Nice results. I wanted to ask on the loan platform business. Nice to see the volumes this quarter kind of pushing back up and were above expectations. So maybe if you could speak a little more to what the demand environment looks like there, both from existing and potential new partners. Just any color there would be great.

**Chris Lapointe** (Executives):
Yes. Overall demand remains really robust and strong. We just had record originations that we did on behalf of others of $3.8 billion and really strong revenue at $153 million.
Overall demand that we're seeing remains extremely strong across all asset types. So our traditional unsecured personal loan demand from existing partners as well as new partners continues to grow. We just signed up 2 new partners in this quarter, and we're in several other discussions with others.
We talked about during our last quarterly earnings call that we signed a partnership with BasePoint for $3 billion over 3 years of SMB loans. So there's really strong demand from capital markets participants there. And as Anthony mentioned, it's a relatively small part of the business today, but we're legging into it and we'll continue to expand.
We started issuing our first closed-end seconds through the platform as well, and there's sufficient demand to continue growing well beyond where we are today. So where you're going to see the growth is going to continue to be sustained momentum in our unsecured personal loans but more importantly, increasing demand from closed-end seconds as well as other asset types. We're already pacing ahead this quarter ahead of our $3.8 billion of originations that we did in Q3 and overall take rates are strong in this quarter.

**Operator** (Operator):
Your next question comes from the line of Lance Jessurun from Scotiabank.

**Lance Jessurun** (Analysts):
On the tech platform, you've guided the segment to 25% growth next year. Can you help us kind of discuss how much of that comes from third-party clients versus your own products running on the platform? And then the 9 clients this year, how does that kind of ramp into that number?

**Anthony Noto** (Executives):
Yes. What I'd say is I don't look at the business that way. We're building a technology platform that serves SoFi. We have the most complex needs of any fintech company given we have the broadest array of products available solely on a digital platform.
We built a technology platform set of businesses because those were things that SoFi would need over time, but it also turns out that the industry needs them as well. And so given the product superior of what we're building, our issue processing is world-class.
We have the most modern core in the cloud now that SoFi is now onboarding new members to. Not only do we have a core that we're using for checking and savings, but business banking was built on the back of the core, not only that, but we were able to launch crypto buy, sell and hold on the back of the core. And you'll see our product evolution and launches be faster and faster because we own our own core and it's the most modern in the cloud.
In addition to that, we've built out Payments as a Service or payment hub, which, again, we don't have to rely on other people to provide. And then last, the fourth growth pillar is fraud and risk, which clearly at our scale of 17 million members, $1.4 billion of revenue this quarter and 27 million products, we are getting attacked constantly but doing a great job of defending our members' assets as well as our shareholders' business.
And so when we build products for SoFi, we are building them and selling them to other people, and we'll generate revenue from both of those assets. Because we're a Fed bank holding company, and we're a national OCC bank, the relationship between SoFi Technology Solutions and the bank is one that has to be at arm's length. They actually have to negotiate arm's length negotiations and rates and fees on those services.
And so the way I think about it is that revenue that the SoFi businesses are paying SoFi Technology Solutions is cost we would otherwise have going outside the system. But instead, they're in the system and they're being allocated to the assets that are being built appropriately. I couldn't even tell you what the SoFi revenue number is in the SoFi Technology platform.
I know where to look it up if I want to look at it, but it's not something I think about. Why do I not think about it? Because we're building a business that can grow products to 100 million members by 2030, that can grow members to support that of about 50 million. That's going to require great technology scaling and great innovation as we start to enter an entirely new era of 2 technology super cycles with AI and blockchain, which we're capturing faster than any other fintech in the United States and quite frankly, faster than any large bank.
We are the only national bank that has issued a payment stablecoin and tokenized deposits. We're the only national bank that has all of its products available on a digital platform and no need to speak to anyone to use those products. That requires great technology in a world that is fraught with people that are trying to attack us at the same time, ensuring we have reliability 24/7, 365 for our members. So it's an incredible strategic asset for us that manifests in value creation across internal businesses and external businesses, and we have an obligation to quantify that value given we are a regulated bank.

**Operator** (Operator):
Your next question comes from the line of Moshe Orenbuch from TD Cowen.

**Moshe Orenbuch** (Analysts):
Chris, one of the areas of pushback that I get from some investors is just the sheer kind of amount of personal loan originations and how much that's grown. And it appears we don't have the industry data yet, but it's grown faster than the industry. Can you talk a little bit about what the -- your forecast is going into '27 on that? Like how do you think about the ability to originate either at these levels higher or where are you thinking?

**Chris Lapointe** (Executives):
Yes, absolutely. So we do expect continued momentum in the PL business. But where you're going to see the growth in 2027 is going to be coming from other asset types like our home loans business as well as SLR.
So you're not going to see the same type of magnitude in overall originations in the PL business. But at the end of the day, what we're focused on is delivering the best risk-adjusted returns that we can for our shareholders, and we're delivering really strong returns through our personal loans business.
Right now, our risk-adjusted margin for PL is north of 7.5%, and that's increased by over 100 basis points year-over-year, primarily as a function of an increase in origination fees, which are up 2.5x year-over-year, but also from improving losses. So net-net, we're focused on risk-adjusted returns at the end of the day.
We do expect continued momentum in the PL business, just given the overall market opportunity that we have today, but you are going to see a little bit of a mix from personal loans towards home loans and student loan refinancing.

**Operator** (Operator):
Your next question comes from the line of Will Nance from Goldman Sachs.

**William Nance** (Analysts):
I wanted to ask a question on the pricing environment in the personal loan business. It looks like the weighted average coupons have been ticking down for the last couple of quarters. And obviously, it's great to see things like net interest margin holding in despite higher funding costs.
But I was wondering if you could provide some color on just how pricing has evolved in personal loans and how you're thinking about kind of the moving pieces there between coupon rates and spread and how much of that maybe is being made up on the origination fee side?

**Chris Lapointe** (Executives):
Yes. And I think you hit on it with the origination fees. But we're continuing to price originations to deliver really attractive risk-adjusted returns.
And it's important to note that we're not optimizing for any single variable in isolation in that equation. Historically, weighted average coupon was the primary pricing lever for us, but increasingly, origination fees are an important part of the overall economics.
Today, more than 50% of all new PL originations include these origination fees, and we generated approximately $270 million of origination fee revenue in Q3, like I just said, up 2.5x year-over-year and 36% sequentially with the vast majority coming from personal loan borrowers.
So if you look at WACC plus our current origination fee yield, it was generally flat sequentially. And then after you incorporate lower losses and funding costs, our overall risk-adjusted return increased by about 100 basis points year-over-year.
I think the other thing I would note is the overall power of origination fees and what it does to the return profile of these assets. And it's why we're leaning in so heavily into driving that mix and giving our members better selection. If you look at an asset or a borrower who pays an origination fee, the overall CPR is about 600 to 700 basis points better than someone who takes out a loan without an origination fee, which thereby extends the overall life of the asset.
In addition to that, the CDR that we've observed on borrowers with an origination fee is about 40 to 50 basis points better than those without. So net-net, you're seeing about 200 to 300 basis points of ROE improvement from assets that have origination fees versus those that don't.
So we're looking at the overall mosaic focus on risk-adjusted margins at the end of the day, but origination fees are playing a much more important piece of the puzzle.

**Operator** (Operator):
Your next question comes from the line of Don Fandetti from Wells Fargo.

**Donald Fandetti** (Analysts):
Can you talk a little bit about your bank funding and kind of the confidence in your ability to grow checking as a percentage of deposits relative to online savings and just lower the overall funding cost of the company?

**Anthony Noto** (Executives):
What I'd say is I would not look at our APY on our products that we give consumers the way you would look at a traditional bank. One, we're not just a bank. We use technology to deliver our services. We're a fintech. And part of being a fintech means we don't have a physical presence for people to walk by and stop in and open an account.
Everything we do is delivered digitally. We don't do outbound calls to acquire people either. So our presence is driven by the digital distribution that we have. One element of digital distribution is what's your value prop. One element of the value prop is what's the leading interest rate.
So we use the interest rate for customer acquisition to replace the cost of physical locations to replace the cost of human beings, and it's a great return for us. So we think about that interest rate not just in aggregating deposits, but we also think about it aggregating new members and those new members then take out more products and the more products they take out against the revenue per product, we drive more returns, and it drives the flywheel.
SoFi Money is the tip of the sword. It is the best product that leads to cross-buy. It also gives us a lot of data on our member. It gives us information on what they're paying on their mortgage. It gives us information that they may have loans. It gives us information they may have credit card debt.
It gives us information that they may have excess cash sitting there that's not being invested. We're not earning interest. And so it's a strategic product that you can't just look at as a cost of funds. Chris will explain this in more detail in a second. It's actually cheaper for us to use broker deposits to fund our business than SoFi Money deposits.
We will use a mix of them to do it. We're managing to an overall return basis. And when we think about an overall return basis, it starts with our net income margin. And we've said that we can have a net income margin of 20% to 30%. We're forecasting for 2027 a 30% incremental net income margin, and that should become our long-term margin over time, where we've given a range of 20% to 30%. We'll actually be at 20% net income margin next year and still growing incredibly fast.
And so we're looking at what is our net income margin. And then what is our revenue to equity ratio. And as our mix moves from 42% of fee-based revenue to 50% fee-based revenue or higher, the revenue per equity ratio will approach 1, and that will get us to a return of 20% to 30%. So I'll let Chris give you the particulars on how we think about cost of funds overall and the role of broker deposits and retail deposits.

**Chris Lapointe** (Executives):
Yes, absolutely. So overall, we have a full set of tools to fund our originations, including member deposits, brokered CDs, warehouse facilities and then capital markets activities through securitizations and whole loan sales.
So when you see periods of a lot of rate volatility like we've experienced over the course of the last few quarters, we're going to leverage things like brokered CDs and wholesale funding more heavily.
However, the decision is not simply whether wholesale funding is cheaper than deposits in isolation, but rather the marginal cost of funding incremental asset growth versus repricing the broader member deposit base. So we use a mix that provides the best combination to Anthony's point, of cost, liquidity, duration and risk-adjusted returns. Our member deposits remain the long-term foundation for funding our assets with 80% to 90% deposit funding, and that's expected to be the case over time.

**Anthony Noto** (Executives):
The last point I'd make, I'm super excited about this, because no one's asked about AI. And most people think about AI being -- and they're calling it -- the government is now calling SI for super intelligence.
So I'm going to use SI from now on because I want to make sure we're aligned with all of our regulators. So a lot of people see SI as a risk to the deposit business. I don't see SI as a risk to the deposit business. I think it's going to add a tailwind to what we do. Why? It will provide more transparency of what rates are available.
One of the things that I say all the time to the team is we have great product market fit. As we increase our absolute dollars literally of marketing, we're not seeing an escalating rate in our customer acquisition cost, which means the #1 gating factor of our noncapital-related businesses is awareness. The more awareness we have, the more products we drive. We're driving a lot of that awareness through our marketing today.
But imagine a world in which there's not just search engines to see what rates are out there, but there's actually agents that do searches. And not only are those agents doing searches on what rates are available, but delineating between the rates, what's hidden fees, what's the requirement, what's the minimum deposits, what's the limits? And they're doing a great job with that, but it's nowhere near where it can be in a world in which there's 100% transparency, SoFi wins every time. Why do we win every time? We have the highest lifetime value, which allows us to give you better rates on loans, better rates on deposits, better products and services.
So I love what SI is going to do for the world as it relates to transparency and awareness. In that world, we think we win every time. And we'll continue to build the network effects and the competitive advantages that allow us to maintain that lifetime value superiority. Let's take the next question.

**Operator** (Operator):
Your next question comes from the line of Reggie Smith from Loop Capital.

**Reginald Lawrence Smith** (Analysts):
I guess great performance on the member growth and deposit growth this quarter. I was somewhat surprised at SoFi Plus. You guys had great momentum last quarter. It looks like you didn't add as many SoFi Plus members this quarter. I think I just saw an add in my app for like 4.4% APY. What's going on there? Are you surprised at the uptake there? And are you still targeting 1 million SoFi Plus members by the end of next year?

**Anthony Noto** (Executives):
We are targeting 1 million SoFi Plus members by the end of next year. In fact, I'm holding the team accountable to achieving 1 million SoFi Plus members before the end of next year.
I said previously, I'd be disappointed if we didn't get to 1 million SoFi Plus members by an earlier date than next year, and I'm challenging the team to get there. In the quarter, in Q3, our SoFi Plus growth was below what we expected. It was primarily due to us making sure that we had the right elements in place as we make offers and as members and nonmembers sign up for the product.
Bottom line is the growth wasn't where we anticipated it would be, but it was fundamentally due to some of the various factors. And so we had to change some things which impacted the growth. That said, those things are fixed. We're in Q4, the growth is reaccelerating again.
And I think the product that you see today will evolve every month. I am pushing the team incredibly hard at putting more value into SoFi Plus. Think of it as Prime for Amazon. When Amazon first launched Prime, I think it was $99 -- it's a long time ago, $99 for free shipping.
And I was thinking to myself as a research analyst, why are people going to pay $99? They don't order enough books, music and video to get a return on that $99. They'll just pay the shipping. And then Amazon started to put other things of value into Amazon Prime like free music and free video.
We will continue to put more value into SoFi Plus beyond just delivering the best of SoFi and the other product. So when you use SoFi Plus, we want to give you a better money product, i.e., higher APY. We want to give you a better and best product, i.e., higher matches for transfers.
We want to give you a better credit card product, i.e., higher rewards, lower interest. We want to give you better home loans. In addition to that, we will have SoFi Plus first product. So we're working on subscription cancellation. There are other companies that charge $9.99 just for subscription cancellation. It will be free as part of SoFi Plus, not an incremental fee.
We bought a company Composer, which is AI-generated portfolios. You'll get 1 or 2 of those for free when you use it outside of SoFi Plus. But if you use SoFi Plus, you'll get as many as you want for that price.
So SoFi Plus will continue to evolve. It is not going to be static. We're challenging the team every day to increase the value there. Why are we so focused on that? Because it is literally the best example of the financial services productivity. 85% of the SoFi Plus members are existing members. 25% of them take out another product. They were already our members. Why didn't they take out that product before SoFi Plus because they weren't aware of it, but the value prop wasn't strong enough.
And so it creates a great flywheel that we want to keep spinning and spinning faster and faster to drive more members, more products, more revenue per product. It just keeps feeding on itself. And if we don't get to 1 million by our deadline, so what? We'll get there eventually. There's 17 million members. You can't tell me we can't get at least 1 million of them for SoFi Plus. I think it should be several million, but one step at a time.

**Operator** (Operator):
Your next question comes from the line of Craig Maurer from FT Partners.

**Craig Maurer** (Analysts):
Curious on the mix between LPB and balance sheet going forward. It was weighted a little bit more toward balance sheet this quarter, and we're getting a lot of questions on how you intend to shape that moving forward.

**Chris Lapointe** (Executives):
Sure. So overall, we feel really good about the loan demand that we have, and we expect healthy origination volumes through the balance of the year and into 2027.
As we've said on prior calls and previously, we're not managing to a predetermined split between loans that we retain on our balance sheet and loans that we distribute through our loan platform business. One of the strengths of our model is that we have multiple ways to monetize that demand, and we're going to continue to allocate originations based on where we see the best risk-adjusted returns and long-term durable revenue profile.
Today, we have a really strong capital position and the flexibility to retain more loans than and that creates the greatest long-term value for our shareholders. At the same time, demand from our LPB partners remains really robust. We're starting to expand into new asset types, and we're seeing really good momentum from existing partners. And we view LPB as an attractive, profitable and capital-efficient business. So I wouldn't expect us to think about this as an either/or decision. We expect both the balance sheet and LPB to continue to grow with the mix determined by capital allocation opportunities, market conditions and partner demand rather than a fixed target.

**Operator** (Operator):
Your next question comes from the line of Gus Gala from MCH.

**Gustavo Gala** (Analysts):
As we think about banks and fintechs adding more and more products and we think about the financial services group, right, -- how has the moat and the sustainability changed? I mean we go back a few years, I think the deposit funding and the charter were big items.
This is something that more and more people are pursuing. Clearly you're standing out in terms of the cross-sell and your cost to serve. Just help us think of that going forward, more of a strategic question. And I just want to clarify on the calendar 30. we -- are we kind of seeing, hey, we're at that 50% fee mark? And then are we in that 20% to 30% return on total capital range?

**Anthony Noto** (Executives):
I'll take your first question and then Chris can answer the second one. So this is going to be somewhat of a long answer, but stay with me for a minute. When we -- when I got to the company in 2018 and kind of laid out the strategy, which is exactly what we've done since then and the mission, one of the things that you would have seen on the presentation I gave to the Board when I was interviewing for the final interview with the Board in December 27 is a focus on unit economics.
And so companies have done incredibly well with big moves around their business generally when they're low-cost operators. We're not necessarily trying to be a low-cost operator. We're trying to be a profit maximizer for unit economics.
And so each of our products, when the team is building out their initial business plan, we look at where can the long-term unit economics be? What's the amount of variable profit that we'll generate on that particular product over the long term. You can imagine when we start that product, the unit economics are not attractive. In fact, credit cards is a good example. We have lost a lot of money in the credit card business to get to where we're at.
But the unit economics in the long term are super attractive and it justifies. So each one of our products, we're trying to actually have superior unit economics relative to everyone else. In addition to that, we have a breadth of products and services.
So we have an opportunity to actually have more products per member than anyone else. The combination of having more products than anyone else per member and each of those products having superior unit economics gives us the highest lifetime value. It's the combination of both of those things.
And as long as we have the highest lifetime value, it's like being Walmart or Amazon and being a low-cost operator. They can give their consumers the best prices in the store on the same like-for-like products as anyone else. They can give better services in the store than anyone else because they have lower cost and therefore, more margin to give away. And that drives the retail productivity loop, which is a concept I made a long time ago and stole -- I mentioned a long time ago and stole from a great investor, Steve Mandel from Lone Pine Capital.
I apply the same thing to the entertainment industry for the entertainment productivity loop. Well, that now applies to the financial services productivity loop for SoFi, but it actually starts with unit economics across each of our products that are superior and then having more products to offer and having more products per member than everyone else and better unit economics on those products.
That also is important that we are indifferent with what product you use first. If we have the best unit economics in that product and it can survive on its own, which it must, then we're indifferent to what you use, and we can acquire more people, one, because we have the product; and two, we don't necessarily want to shy away from that product. There are many of our products banks don't even offer, which is a huge win for us. There are other products that are no-brainer products.
Your federal student loans are at 8%, we're giving them to it at 6%. We still make a great return on that product. Your credit card debts at 25%. We're giving you a personal loan at 12%, again, a no-brainer product. Deposits, checking and savings a little bit harder, credit card a little bit harder, but they're all designed to have superior economics. So when they add together, we have the highest lifetime value. And that's what builds our moat on top of one product at a time. Chris, why don't you talk about where we'll be in 2030 on mix and ROTCE?

**Chris Lapointe** (Executives):
Yes. So I think your specific question was in 2027, but I'll hit on both. So right now, where we are is at 10% ROTCE. As a reminder, ROE is the product of net income margin multiplied by revenue to equity.
Today, we're forecasting that our net income margin for next year is going to be 20% with an incremental net income margin of 32%. As we continue to hit our incremental net income margins, that becomes a steady-state long-term margin.
So we're going to get to, we expect 30-plus percent net income margins in the long-range outlook. And then it's about increasing our overall revenue to equity. Today, we're at about 57%. That's up from 55% last quarter and 50% the quarter before that.
So we're continuing to expand that multiple as well, and that's a function of growth in fee-based revenue, which will continue to grow over the course of the next several years.

**Anthony Noto** (Executives):
The other thing that will drive that is a greater mix of technology platform revenue, which we gave you an outlook for growth on. But obviously, that business doesn't require capital and the faster it grows and the bigger it gets, the more it will drive that revenue to equity ratio to where we need it to be.
With that, operator, I just want to share some closing remarks and thank all of those that have dialed into the call today. The third quarter was excellent by any measure, but the opportunity ahead of SoFi is still massive.
We approached 2027 with the clearest conviction in our mission and the deepest confidence in our strategy. Thanks to the tenacious execution of our team, we've proven SoFi's resilience in rising and declining rate environments. Leading our team is a privilege, especially this year as we've methodically delivered results that directly refute many of the prognostications of the haters of the great business we've built to help Americans achieve their dreams.
I love where we stand today. We have reached the financial scale and capital position where we can fund our planned growth in 2027 organically and control our own destiny. It's clearer than ever as SoFi's member base scales, our product ecosystem becomes broader, engagement increases and the opportunity to generate revenue from each relationship expands.
The model is working. It's why we're confident that by 2030, we can reach 100 million products, up 4x from today. It doesn't take much imagination to see how that can drive 4x in earnings. Don't get me wrong, that is a very ambitious goal and even achieving 3x from where we stand today in products and earnings would be an incredible achievement from where we stood in 2018 and where our stock is valued today.
But it's an achievable goal given where we stand today with the right leadership and execution of our proven strategy. Rest assured that we will continue working every hour of every day to deliver value to our members, clients and shareholders. Thank you, and see you next quarter.

**Operator** (Operator):
Goodbye. This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SOFI_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：FY2026 調整後淨營收財測上調（原話："$4.75 billion to $4.85 billion, which equates to"）
- 2026-07-29｜CFO｜guidance：FY2026 調整後 EBITDA 財測維持約 $1.6B（原話："to deliver adjusted EBITDA of approximately $1.6 billion"）
- 2026-07-29｜CFO｜guidance：EPS 財測內含 22% 稅率（原話："Our EPS guidance now includes a tax rate of 22%"）
- 2026-07-29｜CFO｜margin：以原先中位十幾% 稅率計算 EPS 為 $0.65 而非 $0.60（原話："would have actually been $0.65 in EPS"）
- 2026-07-29｜CFO｜guidance：利率假設改為與 Fed funds futures 一致，2026 升息 1–2 次（原為降息 2 次）（原話："consistent with the Fed funds futures and 1 to 2"）
- 2026-07-29｜CFO｜guidance：NIM 預期維持 5% 以上（原話："a healthy net interest margin above 5%"）
- 2026-07-29｜CFO｜margin：Q2 調整後 EPS 受稅率高於預期的影響（原話："due to higher-than-expected tax rate"）
- 2026-07-29｜CFO｜margin：管理層定義：現金營收的口徑（原話："Cash is defined and accounted for the same universally"）
- 2026-07-29｜CEO｜margin：Q2 增量 EBITDA 利潤率 31%（原話："Our incremental EBITDA margin was 31%"）
- 2026-07-29｜CFO｜margin：Tech Platform 分部貢獻利潤 $12M（原話："Contribution profit was $12 million"）
- 2026-07-29｜CFO｜margin：核心個人貸款風險調整後利差約 6.1%（原話："our core personal loan product generated a roughly 6.1%"）
- 2026-07-29｜CFO｜margin：ROTCE 的拆解口徑：淨利率 ×營收/權益（原話："ROTCE is the product of net income margin"）
- 2026-07-29｜CFO｜margin：增量淨利率已約 30%（營收成長逾 35%）（原話："has already been approximately 30% while growing revenue"）
- 2026-07-29｜CFO｜margin：管理層稱達 25–30% 淨利率路徑「highly probable」（原話："we believe the path to a 25% to 30% net income margin"）
- 2026-07-29｜CFO｜margin：個人貸款淨沖銷率（不含逾期貸款出售）（原話："estimated all-in annualized net charge-off rate was 3.7%"）
- 2026-07-29｜CFO｜risk：個人貸款公允價值 mark 較上季下降 71bp（原話："our personal loans were marked at 104.7%"）
- 2026-07-29｜CEO｜risk：房貸買房與再融資市場仍疲弱（原話："as purchase and refinance remain muted in"）
- 2026-07-29｜CEO｜commitment：Noto 設定 SoFi Plus 一年後 100 萬付費會員目標（原話："I'd be disappointed if we are not at 1 million SoFi Plus"）
- 2026-07-29｜CFO｜commitment：長期 ROTCE 目標 20–30%（原話："we are on a path to generating returns on"）
- 2026-07-29｜CEO｜commitment：Financial Services 與 Tech Platform 營收占比未來超過 50%（原話："to be more than 50% of our revenue"）
- 2026-07-29｜CFO｜capital_allocation：過剩資本中期內將讓風險資本比率回落至低到中十幾%（原話："normalize toward the low to mid-teens"）
- 2026-07-29｜CFO｜capital_allocation：現行營運計畫下不需增資（原話："comfortably within our target capital range"）
- 2026-07-29｜CFO｜capital_allocation：LPB 與資本消耗：財測期自行供資（原話："we're self-funded through our guidance period"）
- 2026-07-29｜CEO｜capital_allocation：資產負債表與 LPB 並行以取得未來數季 NII 能見度（原話："next 6 to 8 quarters"）
- 2026-07-29｜CEO｜capital_allocation：資產負債表放貸使 2027 營收能見度高（原話："we have very strong visibility into our revenue for 2027"）
- 2026-07-29｜CEO｜capital_allocation：累計現金 NII 對非現金溢價的倍數（原話："is 2.7x the cumulative noncash premium on our balance sheet"）
- 2026-07-29｜CFO｜guidance：EBITDA 未上調的理由：多餘營收用於投資（原話："just too many large attractive growth areas"）
- 2026-07-29｜CEO｜guidance：不想為 EPS/EBITDA 過度最佳化（原話："we don't want to over-optimize for the actual EPS"）
- 2026-07-29｜CEO｜guidance：若利率不升，底線有上行空間（原話："we probably have upside to the bottom line"）
- 2026-07-29｜CEO｜commitment：今年推出多項原 2026 計畫外的新業務（原話："things that were never in our 2026 plan"）
- 2026-07-29｜CEO｜competition：非貸款業務競爭環境（原話："Outside the loan business, the competition is very benign"）
- 2026-07-29｜CEO｜competition：貸款產品競爭較強（原話："The lending products are definitely more competitive"）
- 2026-07-29｜CEO｜competition：SMB 放貸對手利率偏高，SoFi 稱可低約 10 點（原話："most SMB lenders are charging exorbitant rates of over 30%"）
- 2026-07-29｜CEO｜customer：會員新增 110 萬（原話："We added a record 1.1 million new members in"）
- 2026-07-29｜CEO｜customer：新產品中既有會員交叉購買比例升至 51%（原話："accelerate with 51% of new products opened by"）
- 2026-07-29｜CEO｜customer：CAC 大致維持不變（原話："over 40% growth in products and really keeping CAC constant"）
- 2026-07-29｜CEO｜customer：SoFi Plus 付費訂閱戶逾 20 萬（原話："we surpassed 200,000 paid subscribers"）
- 2026-07-29｜CEO｜product：SoFi Coach 於 6 月推出（原話："SoFi Coach, which launched in June"）
- 2026-07-29｜CEO｜product：信用卡：稱已摸索出有效獲客方式（原話："We think we've cracked the code on efficiently"）
- 2026-07-29｜CEO｜product：SoFi Money 開始遷移到 STS 自建核心（原話："begun onboarding SoFi Money to our new"）
- 2026-07-29｜CEO｜product：併購 Peach Finance（原話："During the quarter, we acquired Peach"）
- 2026-07-29｜CEO｜product：Mastercard 卡將以 SoFi USD 結算（原話："will begin settling in SoFi USD with Mastercard"）
- 2026-07-29｜CFO｜product：LPB 新增 Basepoint 3 年 $3B SMB 協議（原話："a 3-year $3 billion agreement with Basepoint Capital"）
- 2026-07-29｜CFO｜product：LPB 需求逾 SoFi 願意滿足的量，合約承諾皆已履行（原話："we did fill all demand from our contractual commitments"）
- 2026-07-29｜CEO｜capital_allocation：結語：管理層自述買進股票（原話："when, not if the market can connect the dots"）

### 問答異常語氣（迴避／改口／保留）
- SOFI_Q2_2026_Earnings_Call_20260729.md｜問：Dolev（Mizuho）：為何不上調 EBITDA？｜答法：未給 EBITDA 上調數字，改談營收上調 $100–200M 與投資新成長領域；Noto 補充稱財測內有緩衝
- SOFI_Q2_2026_Earnings_Call_20260729.md｜問：Peterson（Needham）：LPB 連兩季未滿足上調需求，個人貸款面是否持續？｜答法：未回答未來個人貸款 LPB 量是否持續受限，改談其他資產類別成長與資本自給
- SOFI_Q2_2026_Earnings_Call_20260729.md｜問：Coad（Truist）：超額資本消耗的節奏｜答法：Noto 轉交 CFO；CFO 重申 18.8% 與低到中十幾%目標，未給時程或消耗速度

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
{"date":"20260730","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"資本輕費收引擎撐起報酬率目標的分子與分母：Financial Services ＋ Technology Platform 由調整後淨營收的 45.7% 破 50%，且該增量不消耗權益，使營收／有形權益比由 0.503 轉向 1.00"},{"id":"H2","text":"消費飛輪續轉且獲客成本不惡化：交叉購買佔新開產品比續升、每會員產品數續升、獲客成本持平，使追加產品的邊際獲客成本維持趨近零"},{"id":"H3","text":"信用穿越一次完整循環而不破承保容忍上限：無擔保消費簿在家庭債務創紀錄、聯準會轉為升息的環境下，年化淨壞帳率不突破使風險調整後利差歸零的水位"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"資本輕費收引擎失效：平台段持續萎縮、Financial Services 段 contribution margin 由 52% 降至 46% 的趨勢延續，費收佔比卡在 46% 上不去 → 報酬率目標的分母腿永遠修不好，估值框架被迫切換到消費放款銀行"},{"id":"R2","text":"口徑與查核風險：公允價值計量的認列時點爭議在年度查核程序中具體化（關鍵查核事項、重述、或監理問詢），或放空方持續施壓使折價常態化"},{"id":"R3","text":"消費信貸循環在晚期轉向：家庭債務 $18.19 兆創紀錄 ＋ 聯準會由降息轉升息 1-2 次 ＋ K 型分化下次級族群持續受壓 → 無擔保簿損失率上行，同時擠壓利差與資本"},{"id":"R4","text":"競爭結構下移：Chime 往上市場（Chime Prime）＋ 大型銀行奪回客戶成長 ＋ 存款端須維持 4.5% 年化利率才能留住存款"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"平台段 YoY 轉正或段 margin ≥25%，且營收／有形權益比首度回升至 ≥0.55（現 0.503）；技術路徑另計＝站回 W104 $17.70 滿 4 週","irr_base_pct":10.4,"ev5y_pct":58.3,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟢","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":4.4,"ev5y_pct":58.3,"irr_base_pct":10.4,"max_dd_pct":-55.0,"bull_5y_price":36.0,"bear_5y_price":10.3,"p_bull_pct":28.0,"p_bear_pct":27.0,"rearm_trigger":"平台段 YoY 轉正或段 margin ≥25%，且營收／有形權益比首度回升至 ≥0.55（現 0.503）；技術路徑另計＝站回 W104 $17.70 滿 4 週","price_at_dd":15.25,"archetype":"金融","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SOFI_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
