你是 stock-analyst **v20 判斷 agent**，標的 RCL（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"RCL","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RCL_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RCL_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":5591,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm"},"note":"Benzinga 報導營收低於共識（未取得精確數字）"},{"id":"f_kpi1_operating_income_gaap","label":"Operating income (GAAP)","value":1871,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm"}},{"id":"f_kpi2_operating_margin_gaap","label":"Operating margin (GAAP, 計算值)","value":33.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm"}},{"id":"f_kpi3_adjusted_ebitda","label":"Adjusted EBITDA","value":2539,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm"}},{"id":"f_kpi4_adjusted_eps","label":"Adjusted EPS","value":6.57,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm"},"note":"高於公司自家指引（共識數字未核實）"},{"id":"f_kpi6_share_based_compensation","label":"Share-based compensation YTD","value":94,"period":"9M FY2026（至 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"9M FY2026（至 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm"}},{"id":"f_kpi7_load_factor","label":"Load factor","value":112,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm"}},{"id":"f_kpi8_guidance_fy2026_adjusted","label":"Guidance: FY2026 Adjusted EPS","value":"17.85～17.95","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm"},"note":"上調；yfinance/快照 FY1 共識 17.90"},{"id":"f_kpi9_guidance_q4_2026_adjuste","label":"Guidance: Q4 2026 Adjusted EPS","value":"3.48～3.58","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm"}},{"id":"f_kpi10_guidance_fy2026_net_yiel","label":"Guidance: FY2026 Net Yields (as-reported)","value":2.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%（約）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm"}},{"id":"f_kpi11_guidance_fy2026_ncc_ex_f","label":"Guidance: FY2026 NCC ex fuel per APCD (as-reported)","value":0.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%（約）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_rcl_gross_margin_pct","label":"RCL 毛利率","value":49.06,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RCL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rcl_operating_margin_pct","label":"RCL 營業利益率","value":27.56,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RCL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rcl_fcf_margin_pct","label":"RCL FCF 利潤率","value":7.89,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RCL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vik_gross_margin_pct","label":"VIK 毛利率","value":43.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VIK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vik_operating_margin_pct","label":"VIK 營業利益率","value":23.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VIK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vik_fcf_margin_pct","label":"VIK FCF 利潤率","value":16.56,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VIK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nclh_gross_margin_pct","label":"NCLH 毛利率","value":40.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NCLH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nclh_operating_margin_pct","label":"NCLH 營業利益率","value":10.85,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NCLH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nclh_fcf_margin_pct","label":"NCLH FCF 利潤率","value":-6.36,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NCLH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ccl_gross_margin_pct","label":"CCL 毛利率","value":39.47,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CCL.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ccl_operating_margin_pct","label":"CCL 營業利益率","value":15.99,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CCL.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ccl_fcf_margin_pct","label":"CCL FCF 利潤率","value":11.51,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CCL.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_free_cash_flow_ytd_5_274","label":"Free cash flow YTD (計算值: 營運現金流 5,274 − 資本支出 3,880)","value":1394,"period":"9M FY2026（至 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"9M FY2026（至 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm（公司未報 FCF，為自行計算）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":322.3,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":25.65,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":72.74,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.06,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（17.89 → 17.9）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.05,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.44 → 20.43）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.38 → 23.38）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":17.9,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":20.43,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":23.38,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.02,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 17.72 → 17.9（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":19.07,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝51.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":51.8,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.51,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.67,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":18.01,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 17.9，分子＝快照價 322.32","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.706,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":22319.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 23170.0、現金 851.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":267.47,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":108530.23,"period":"2026-11-03","unit":"USD m","basis":"市值 86211.23 ＋ 淨負債 22319.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":19558.01,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":20991.68,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（25 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":5.55,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 320.04 / W52 282.4 / W104 272.37 / W250 167.87 / W250 13週斜率 2.12%"},{"id":"f_ma_w52","label":"52 週均線","value":282.4,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":272.37,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":167.87,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.12,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列示主要郵輪對手：Carnival、Disney、MSC、Norwegian Cruise Line Holdings、Viking、Virgin Voyages；公司自稱在逾兆美元全球度假市場中占比小","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/884887/000088488726000007/rcl-20251231.htm","excerpt":"Our principal cruise competitors are Carnival Corporation & plc, which owns, among other brands, Aida Cruises, Carnival Cruise Line, Costa Cruises, Cunard Line, Holland America Line, P&O Cruises, Princess Cruises and Seabourn; Disney Cruise Line; MSC Cruises; Norwegian Cruise Line Holdings Ltd, which owns Norwegian Cruise Line, Oceania Cruises, and Regent Seven Seas Cruises; Viking, and Virgin Voyages.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：公司依賴旅行顧問訂位，若佣金不具競爭力，顧問可能轉賣對手郵輪","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/884887/000088488726000007/rcl-20251231.htm","excerpt":"If we fail to offer competitive compensation packages or fail to maintain our relationships, these agencies may be incentivized to sell cruises offered by our competitors, which could adversely impact our operating results.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"2026 加勒比海運力：RCI 占約 30%、Carnival 25%；RCL 加勒比運力年增 9%，NCLH 增 55%、MSC 增 23%","source":"Cruise Industry News: Caribbean Continues to Claim Lion's Share of Market","url":"https://cruiseindustrynews.com/cruise-news/2026/05/caribbean-continues-to-claim-lions-share-of-market/","excerpt":"deployed in the Caribbean. MSC Cruises is third largest with a 10 percent market share and 37 percent of its capacity, followed by Norwegian Cruise line also with a 10 percent market share and 53 percent of its capacity deployed. Norwegian Cruise Line has the highest year-over-year capacity increase with 55 percent; MSC has a 23 percent increase from 2025; Royal Caribbean, 9 percent;","as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Port Economics 2026：Big-4 占部署船隊 78.9%，Virgin Voyages 1.4%","source":"Port Economics Management: Market Share of Main Cruise Lines, 2026","url":"https://porteconomicsmanagement.org/market-share-main-cruise-lines/","excerpt":"629,433 berths, representing a deployed capacity of 30.30 million passengers, or 78.9% share of the total deployed fleet. Disney Cruises, with a 2.9% share of the deployed capacity, tops the list of the other cruise lines. In comparison, the comparatively recently established Virgin Voyages holds a notable 1.4% of the deployed market capacity.","as_of":"2020-02-04","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"客戶為個人消費者；FY2020 10-K 揭露美國占 2020 年乘客船票營收 67%（2018 年 61%），其他單一國家均未超過 10%。屬地理集中而非單一大客戶集中。","source":"RCL Form 10-K FY2020","url":"https://www.sec.gov/Archives/edgar/data/884887/000088488721000006/rcl-20201231.htm","excerpt":null,"as_of":"2021-02-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"S&P 將 RCL 由 BBB- 升至 BBB（頁面未標日期）","source":"bondblox","url":"https://bondblox.com/news/royal-caribbean-upgraded-to-bbb-by-sp-2","excerpt":"Royal Caribbean Upgraded to BBB by S&P February 3, 2026 Corporates Credit Ratings Royal Caribbean Cruises was upgraded to BBB from BBB- by S&P.","as_of":"2026-02-03","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"RCL 2027 預訂量高個位數至十幾%成長：Q3 2026 財報後，管理層稱自上次財報電話會議以來預訂量中段十幾%成長、2027 航次預訂高十幾%成長，節奏領先歷史水準（來源為搜尋摘要轉述，未核原文）","source":"Seatrade Cruise / Royal Caribbean Q3 2026 earnings release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"RCL 自家運力成長指引：2026 年 6.7%、2027 年 4%、2028 年 6%、2029 年 7%（Q1 2026 財報稿）","source":"Royal Caribbean Q1 2026 earnings release, SEC 8-K","url":"https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000024/a2026q1earningsrelease.htm","excerpt":null,"as_of":"2026-04-28","retrieved_at":"20261103","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"業界新船訂單簿：2026-03 約 78 艘、逾 206,600 床位；2027 年交付 15 艘、2028 年 13 艘（約 30,770 床位）；2026-04 更新為 93 艘、約 229,500 床位","source":"Cruise Industry News orderbook updates (2026-03, 2026-04, 2026-07)","url":"https://cruiseindustrynews.com/cruise-news/2026/03/orderbook-update-more-ships-and-continued-push-over-200000-new-berths/","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"CLIA 稱大型船訂單簿實質上排滿至 2036，整體 89 艘、約 $99.8B，交付延伸至 2039（造船廠產能約束新增供給）","source":"Shipuniverse citing CLIA","url":"https://www.shipuniverse.com/?p=24506","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Carnival 稱 2027 年約半數已訂、入住率與價格創紀錄；NCLH 預期 2027 上半年需求仍弱、下半年才改善（需求面同業分歧）","source":"Baird Maritime (Carnival); Asianet News (NCLH)","url":"https://www.bairdmaritime.com/passenger/cruise/record-2027-bookings-lift-carnivals-annual-profit-outlook","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"CLIA 預測 2027 全球乘客約 40.3M，2028、2029 年成長約 2%","source":"Forbes España citing CLIA","url":"https://forbes.es/economia/906978/el-sector-mundial-de-cruceros-alcanzo-un-maximo-historico-de-372-millones-de-pasajeros-en-2025-segun-clia/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K FY2025 Item 3 僅列 Helms-Burton Act 的 Havana Docks 訴訟（美國最高法院 2025-10-03 准予調卷），其餘為產業常見索賠、多數有保險；未列反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/884887/000088488726000007/rcl-20251231.htm","excerpt":"The plaintiff petitioned the United States Supreme Court for a writ of certiorari, which was granted on October 3, 2025.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋未找到 2026 年 RCL 的反壟斷、DOJ 或 FTC 行動；結果僅有 2002 年購併審查與 2014 年義大利消費者罰款等舊事。","source":"WebSearch 結果摘要","url":null,"excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"RCL 10-K 風險因素稱供應鏈可能受關稅與貿易制裁等新法規影響；美國對特定國家進口品加徵關稅帶來不確定性，重大貿易關係變動可能對業務、財務與經營成績產生重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/884887/000088488726000007/rcl-20251231.htm","excerpt":"Our supply chain can also be impacted by new laws and regulations, such as tariffs and trade sanctions.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"中國自 2025-10-14 對美國關聯船舶收港口費；Royal Caribbean 以上海為母港的 Spectrum of the Seas 據報可豁免（中國母港船與中國建造船豁免），他牌 Oceania 等受衝擊。2026 年無更新查得。","source":"cruisemapper / cruisepassenger 報導（搜尋摘要）","url":"https://www.cruisemapper.com/news/15440-global-cruise-itineraries-disrupted","excerpt":null,"as_of":"2025-10-16","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"RCL 2026年營收成長指引由10%下調至約9%，理由是長期地緣緊張對部分航程造成小幅訂位衝擊；歐洲航程最受影響","source":"Hotel-Online/Reuters: Royal Caribbean Trims Revenue Forecast on Booking Hit from Geopolitical Tensions","url":"https://www.hotel-online.com/news/royal-caribbean-trims-revenue-forecast-on-booking-hit-from-geopolitical-tensions","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"RCL新船集中於Meyer Turku（芬蘭）與Chantiers de l'Atlantique（法國）兩家船廠，在建船約165億美元，約49.9%成本暴露於歐元匯率","source":"RCL 10-Q (2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000044/rcl-20260930.htm","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中東衝突壓抑RCL歐洲航程需求","source":"Cruise Industry News","url":"https://cruiseindustrynews.com/cruise-news/2026/07/middle-east-conflicts-weighs-on-royal-caribbeans-europe-program/","excerpt":"than anticipated, influencing consumer destination preferences and resulting in more modest yield growth for Europe sailings this summer,” he said. Liberty told Wall Street Analysts that Europe had been “off to an incredible start at the beginning of the year,” before geopolitical activity and its effect on fuel curtailed demand.”","as_of":"2026-07-28","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"RCL 2026年Q3營收約56億美元、年增9%；淨收益率(net yield)報告值+0.9%、固定匯率+0.6%，載客率112%；歐洲與加勒比海近期訂位帶動。全年調整後EPS指引上調至17.85–17.95美元。","source":"Baird Maritime／Seatrade Cruise，Royal Caribbean Q3 2026 results","url":"https://www.bairdmaritime.com/passenger/cruise/royal-caribbean-raises-earnings-outlook","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"管理層稱2027年訂位進度高於歷史水準且價格較高，仍預期達成2027年調整後EPS 20美元級的Perfecta目標；Sandals/Beaches合作預計2027年初交割後納入指引。","source":"Seatrade Cruise，Royal Caribbean's Q3 outperforms, 2026 outlook rises","url":"https://www.seatrade-cruise.com/finance-legal-regulatory/royal-caribbean-s-q3-outperforms-2026-outlook-rises","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"部分歐洲航線訂位因地緣政治活動受輕微影響，已反映於指引；2026全年淨收益率指引曾兩度收窄至1.75%–2.25%；有分析師質疑船上消費強勢能否轉為2027年船票價格。","source":"Cruise Industry News／Zacks 報導，RCL 2027 pricing","url":"https://cruiseindustrynews.com/cruise-news/2026/10/royal-caribbean-sees-record-rates-as-2027-bookings-climb/","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"CLIA預測全球海洋郵輪旅客由2026年3,830萬增至2027年4,030萬，2026–2029為個位數年增、新船交付減緩後增速放慢；2027年約15艘新船、約27,860床位交付。","source":"Ship Universe / Cruise Industry News，2027 Cruise Industry Outlook","url":"https://www.shipuniverse.com/cruise/2027-cruise-industry-outlook-growth-is-strong-but-the-easy-recovery-is-over/","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261103","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026財報新聞稿(SEC 8-K)：營收、淨收益率與2027訂位細節","source":"SEC EDGAR 8-K","url":"https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm","excerpt":"Load factor in the third quarter was 112%. •Gross Margin Yields decreased 0.8% as-reported. Net Yields increased 0.9% as-reported and 0.6% in Constant Currency, driven by better-than-expected close-in demand in Europe and the Caribbean.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：若公司跟不上技術發展，營運或競爭地位可能受損；使用 AI 等新興技術帶來業務、合規與聲譽風險。未點名具體取代性技術。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/884887/000088488726000007/rcl-20251231.htm","excerpt":"If we are unable to keep pace with developments, design, and implementation in technology, our operations or competitive position could become impaired. Our use of emerging technologies, including artificial intelligence, may present business, compliance and reputational risks.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 指出具備建造/維修能力的船廠數量有限，供應鏈中斷因替代選項少而衝擊業務（替代供應商面向，非替代產品）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/884887/000088488726000007/rcl-20251231.htm","excerpt":"There are a limited number of shipyards with the capability and capacity to build, repair, maintain and/or upgrade our ships. As such, any disruptions affecting the shipyard supply chain will adversely impact our business as there are limited substitutes.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"RCL Q3 2026 財報電話會：公司擁有大量土地、逾100個目的地專案，並規劃約30億美元取得 Sandals and Beaches Resorts 50% 股權（陸上度假替代品的因應）。","source":"Cruise Industry News: Royal Caribbean hints at untapped global land holdings","url":"https://cruiseindustrynews.com/cruise-news/2026/10/royal-caribbean-hints-at-untapped-global-land-holdings/","excerpt":"“By the way, we also sit on a lot of land around the world, which we don’t talk a lot about,” he said. Liberty did not elaborate on where the holdings are located or how much land is involved. The comment came as he discussed the company’s planned $3 billion investment for a 50 percent stake in Sandals and Beaches Resorts.","as_of":"2026-10-30","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"產業觀點：郵輪業調整產品以對抗陸上度假村與主題樂園，預期2026成長放緩。","source":"Maritime Executive: global cruise outlook new challenges","url":"https://maritime-executive.com/article/global-cruise-outlook-new-challenges","excerpt":"The industry has adjusted its product to compete with land-based resorts and theme parks, adding more short cruises in the broad, mass-market segment known as contemporary cruising as well as in the premium segment.","as_of":"2026-04-10","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 稱旅行顧問仍是重要銷售通路，公司維持有競爭力的佣金與激勵，同時投資自家網站、App 與電商，讓賓客可端到端預訂；描述為並行投資、非通路結構性替換。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/884887/000088488726000007/rcl-20251231.htm","excerpt":"Travel advisors continue to be a significant sourcing channel of revenues for our ships. We believe in the value of this distribution channel and invest in maintaining strong relationships with our travel partners.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Royal Caribbean 計畫 2028 年前將私人目的地由3個增至8個，並於2027年進入河輪市場（平台化/業務擴張）。","source":"Cruise Industry News: Royal Caribbean Group Invests in Private Destination Strategy","url":"https://cruiseindustrynews.com/cruise-news/2025/10/royal-caribbean-group-invests-in-private-destination-strategy/","excerpt":"and, together with the Royal Beach Club, Paradise Island, Perfect Day Mexico and others, we expect to increase our exclusive land-based destination portfolio from two to eight by 2028.” Royal Caribbean’s private destinations currently include:","as_of":"2025-10-01","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-28 公司上調 FY2026 EPS 指引至 $17.73–$17.87，高於當時共識 $17.32；營收指引約 $195 億，略低於共識 $196 億","source":"MarketBeat 2026-07-28 Royal Caribbean releases FY 2026 earnings guidance（經搜尋摘要轉述）","url":"https://www.marketbeat.com/instant-alerts/royal-caribbean-cruises-nysercl-releases-fy-2026-earnings-guidance-2026-07-28/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-10-27 公司再上調 FY2026 EPS 指引至 $17.85–$17.95（前次 $17.73–$17.87），歸因歐洲與加勒比海近期需求優於預期；Chartmill 2026-10-17 FY2026 EPS 共識 $18.00（32 位分析師），指引區間上緣低於該共識","source":"Seatrade Cruise: Royal Caribbean's Q3 outperforms, 2026 outlook rises；Chartmill RCL estimates","url":"https://www.seatrade-cruise.com/finance-legal-regulatory/royal-caribbean-s-q3-outperforms-2026-outlook-rises","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026 年指引歷程：1/29 初始 $17.70–$18.10；4/30 因燃油成本下調至 $17.10–$17.50（淨收益率區間由 1.5–3.5% 降至 1.5–2.5%）；7/28 上調；10/27 再上調","source":"Yahoo Finance: Royal Caribbean cuts 2026 profit forecast as fuel costs surge；Seatrade Cruise","url":"https://finance.yahoo.com/markets/stocks/articles/royal-caribbean-cuts-2026-profit-122136403.html","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價分布：Investing.com 平均約 $349、高 $425、低 $262（20 買進、1 賣出）；Tickflow（2026-07-31）平均約 $345（29 位）；FN2 10 月下旬評等 27 看多/19 中性/6 看空（52 位）。Q3 後 Barclays 目標價 $358→$342、BofA $355→$325","source":"Investing.com；Tickflow RCL forecast；FN2 analysts；TheFly via TipRanks（經搜尋摘要轉述）","url":"https://fn2.ai/earnings/rcl/analysts","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026-07-31 Freedom Capital 將 RCL 由 strong buy 降至 hold；Stifel 目標價 $415、BMO $370；Susquehanna $355、Wells Fargo $358、Jefferies $330（10 月）","source":"MarketBeat 2026-07-31 Freedom Capital downgrade；FN2","url":"https://www.marketbeat.com/instant-alerts/royal-caribbean-cruises-nysercl-downgraded-by-freedom-capital-to-hold-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-09-23 公司宣布以約 30 億美元取得 Sandals Resorts 50% 股權（隱含估值約 60 億美元），Morgan Stanley 提供承諾債務融資，預計 2027 年初交割、待監管核准。","source":"Hargreaves Lansdown／Maritime Executive 等報導：Royal Caribbean takes 50% stake in Sandals for $3bn","url":"https://www.hl.co.uk/shares/stock-market-news/company--news/royal-caribbean-takes-50-stake-in-sandals-for-$3bn","excerpt":null,"as_of":"2026-09-23","retrieved_at":"20261103","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"Havana Docks 訴訟（Helms-Burton）：11th Circuit 於 2024-10-22 推翻約 1.12 億美元判決；原告 cert 申請於 2025-10-03 獲最高法院受理，結果未定。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/884887/000088488726000007/rcl-20251231.htm","excerpt":"The plaintiff petitioned the United States Supreme Court for a writ of certiorari, which was granted on October 3, 2025.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 8-K 共 13 份，其中 1.01 皆為票據發行（2026-02 兩筆 4.750% 2033／5.250% 2038 各 12.5 億美元；2026-08 5.550% 2034 12.5 億美元，用於償還浮動利率定期貸款），無 M&A 類 8-K 項目。","source":"SEC EDGAR 8-K 申報清單／8-K 2026-08-20","url":"https://www.sec.gov/Archives/edgar/data/884887/000110465926099245/tm2623517d1_8k.htm","excerpt":"which it intends to use to repay a portion of the outstanding borrowings under its floating rate term loan facilities and any remaining net proceeds to repay or refinance other existing indebtedness.","as_of":"2026-08-20","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-09-23 公司宣布以約 30 億美元取得 Sandals Resorts 50% 股權（隱含估值約 60 億美元），Morgan Stanley 提供承諾債務融資，預計 2027 年初交割。","source":"Hargreaves Lansdown：Royal Caribbean takes 50% stake in Sandals for $3bn","url":"https://www.hl.co.uk/shares/stock-market-news/company--news/royal-caribbean-takes-50-stake-in-sandals-for-$3bn","excerpt":null,"as_of":"2026-09-23","retrieved_at":"20261103","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Havana Docks 訴訟：最高法院 2025-10-03 受理 cert，原判決約 1.12 億美元已被 11th Circuit 推翻，結果未定；搜尋未見近 12 個月證券集體訴訟（僅 2011、2020 舊案）。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/884887/000088488726000007/rcl-20251231.htm","excerpt":"The plaintiff petitioned the United States Supreme Court for a writ of certiorari, which was granted on October 3, 2025.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"RCL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.06,"operating_margin_pct":27.56,"fcf_margin_pct":7.89,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RCL","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"VIK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":43.21,"operating_margin_pct":23.27,"fcf_margin_pct":16.56,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VIK","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"NCLH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":40.57,"operating_margin_pct":10.85,"fcf_margin_pct":-6.36,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NCLH","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CCL","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":39.47,"operating_margin_pct":15.99,"fcf_margin_pct":11.51,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CCL","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"RCL"},"financial_history":{"ticker":"RCL","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":8840000000.0,"revenue_yoy_pct":null,"gross_margin_pct":25.16,"operating_margin_pct":-8.67,"net_income":-2156000000.0,"diluted_eps":-8.45,"free_cash_flow":-2229000000.0,"fcf_margin_pct":-25.21,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":13900000000.0,"revenue_yoy_pct":57.24,"gross_margin_pct":44.06,"operating_margin_pct":20.71,"net_income":1697000000.0,"diluted_eps":6.31,"free_cash_flow":580000000.0,"fcf_margin_pct":4.17,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":16485000000.0,"revenue_yoy_pct":18.6,"gross_margin_pct":47.52,"operating_margin_pct":24.92,"net_income":2877000000.0,"diluted_eps":11.0,"free_cash_flow":1997000000.0,"fcf_margin_pct":12.11,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":17934000000.0,"revenue_yoy_pct":8.79,"gross_margin_pct":49.35,"operating_margin_pct":27.38,"net_income":4268000000.0,"diluted_eps":15.61,"free_cash_flow":1236000000.0,"fcf_margin_pct":6.89,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/RCL/RCL_Q3_2026_Earnings_Call_20261027.md）

# Q3 2026 Earnings Call
**Royal Caribbean Cruises Ltd.** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Good morning. My name is Morgan, and I'll be your conference operator today. At this time, I would like to welcome everyone to the Royal Caribbean Group Third Quarter 2026 Earnings Call. [Operator Instructions] I would now like to introduce Mr. Blake Vanier, Vice President of Investor Relations. Mr. Vanier, the floor is yours.

**Blake Vanier** (Executives):
Good morning, everyone, and thank you for joining us today for our third quarter 2026 earnings call. Joining me here in Miami are Jason Liberty, our Chairman and Chief Executive Officer; Naftali Holtz, EVP and Chief Financial Officer; and Michael Bayley, President and CEO of the Royal Caribbean brand.
Before we get started, I'd like to note that we will be making forward-looking statements during this call. These statements are based on management's current expectations and are subject to risks and uncertainties. A number of factors could cause actual results to differ materially from our current expectations. Please refer to our earnings release issued this morning as well as our filings with the SEC for a description of these factors. We do not undertake to update any forward-looking statements as circumstances change.
Also, we will be discussing certain non-GAAP financial measures, which are adjusted as defined, and a reconciliation of all non-GAAP items can be found on our investor website and in our earnings release. Unless we state otherwise, all metrics are on a constant currency adjusted basis.
Jason will begin the call by providing a strategic overview and update on the business. Naftali will follow with a recap of our third quarter the current booking environment and our outlook for 2026. We will then open the call for your questions. With that, I'm pleased to turn the call over to Jason.

**Jason Liberty** (Executives):
Thank you, Blake, and good morning, everyone. I'm very happy to share the results of another outstanding quarter that exceeded our expectations and drove an increase to full year guidance as demand for our leading vacation brands continues to accelerate. Before we get into the results and outlook, I want to talk about our recent announced partnership to buy a 50% stake in Sandals and Beaches Resorts. Our strategy is to turn the vacation of a lifetime into a lifetime of vacations.
Our mid-70s Net Promoter Scores are a testament to our unwavering commitment to delivering the best vacation experiences responsibly. At the same time, we are building a connected vacation platform that brings guests back more frequently across more occasions and captures a greater share of a growing $2 trillion-plus global vacation market.
In recent years, we have strengthened our connected vacation ecosystem by investing in technology, loyalty and commercial capabilities. Everything starts and ends with the customer. We're building a portfolio that serves more of their needs across more occasions. A guest might choose Royal Caribbean for a multigenerational vacation, Sandals for a romantic getaway, Celebrity for a premium couples Galapagos adventure and Silversea for an Antarctica expedition.
We have also broadened how guests can vacation with us through Celebrity River Cruises and our growing portfolio of differentiated destinations and experiences. Connecting these opportunities through loyalty, data and technology, all while obsessing about delivering the best vacation experiences gives high-value guests more reasons to remain within our family of brands.
This, in turn, enables us to deepen engagement, increase frequency and expand lifetime value. That brings me to Sandals and Beaches Resorts. The business has 2 leading and complementary brands in the fast-growing and high potential all-inclusive resort segment. Sandals is the leading adult-only all-inclusive resort brand in the Caribbean, and Beaches leads in serving families and multigenerational all-inclusive resort travelers. It is also a strong strategic fit that builds on the strength and growth potential of our cruise businesses.
Today, we capture only 20% to 25% of our guest annual vacation spend. About 30% of our guests have vacations in a Caribbean all-inclusive resort in the last 2 years. By adding all-inclusive resorts to our ecosystem, we expand our reach to roughly 50% of the vacation wallet. This investment lets us serve guests that are already spending in all-inclusive resorts while also attracting new guests to our ecosystem and building on our Caribbean footprint and North American sourcing, all while reinforcing our core cruise business.
Caribbean all-inclusive is an attractive $16 billion market, growing 11% a year and Sandals and Beaches Resorts is a leading owner operator with strong brand awareness and financial profile. Financially, our approximately $3 billion investment for a 50% stake at 10x forward EBITDA is expected to be immediately accretive to our earnings, while keeping us within our leverage targets.
We are very excited about the value that's going to be brought to our customers, to our shareholders, to our employees, to the communities that we serve with this partnership for Sandals and Beaches. I will elaborate more about this opportunity a bit later. But now let me turn to our results.
This morning, we reported third quarter results that exceeded our expectations and resulted in an increase to our full year guidance. Third quarter revenue grew 9% year-over-year, while earnings came in 4% above our guidance. In the third quarter, we delivered 2.7 million incredible vacations at industry-leading guest satisfaction scores. Capacity increased 8% year-over-year and net yields were up 0.6%, which was about 60 basis points higher than our guidance. The beat was driven by better-than-expected close-in demand, along with strong onboard revenue, primarily for Europe and Caribbean products. Costs also came in favorably due to timing and as a result, adjusted EPS was $0.26 higher than our guidance. Naftali will elaborate on our results and outlook in a few minutes.
Turning to the demand environment, we continue to see accelerated momentum as consumers prioritize our vacations and experiences. Travel remains the #1 leisure category where consumers intend to increase spending. Traveling more is a top priority for a 1/3 of Americans and consumers see cruising as a good value due to high-quality onboard amenities, pricing that includes meals, accommodations and entertainment and the ability to visit multiple destinations in one trip. That confidence is reflected in our booking activity.
Since the last earnings call, booking volumes have increased in the mid-teens year-over-year and bookings for 2027 sailings up in the high teens, demonstrating strong demand as we continue to build a strong base of business for 2027. Our book position for both 2026 and 2027 is ahead of prior year at record rates. We are also seeing our relationship with our guests deepen. This year, close to half of our guests were repeat customers with the balance experiencing our brands for the first time. These new-to-brand guests are becoming loyal repeat cruisers and returning more frequently as the average time between cruises continues to decrease.
Our differentiated brands, Net Promoter Scores in the mid-70s, expanding portfolio and growing loyalty and technology capabilities gives us more ways to engage with guests and more opportunities to capture a greater share of their vacation spend.
Moving to the outlook for the remainder of the year. Our capacity in the fourth quarter is up 5% year-over-year, and we expect to grow yields 4.2% to 4.7%, which is in line with our prior expectations. As we discussed last quarter, the increase in expected fourth quarter yields reflects a more favorable year-over-year comparison, deployment mix and timing of drydocks.
Full year net yields is expected to grow approximately 2.1%. Full year adjusted EPS is now expected to be in the range of $17.85 to $17.95, representing 14% year-over-year growth. Our proven formula of moderate capacity growth, moderate yield growth and strong cost discipline is driving significant earnings growth, continued margin expansion and robust cash flow generation. This allows us to invest in high returning and strategic growth opportunities while also returning capital to our shareholders through dividends and share repurchases. 2027 is the final year of our Perfecta Program, and the business is performing well ahead of expectations.
In fact, at the spot fuel rate when we announced the program, we would exceed our 2027 earnings target by about a $1 per share. Despite the significant increase in fuel rates this year, we remain on track to achieve our 20% adjusted earnings per share CAGR target based on the current forward fuel price curve for a $20 handle in 2027.
Separately, we have already achieved our ROIC target. As I mentioned on our last call, we have a great partnership with local communities and the government of Mexico, where we deliver close to 1 million vacations a year. While I know there is great interest in our efforts in Mahahual, we will share further progress and updates at the appropriate time or as they become available.
Stepping back, our goal is straightforward. Keep guests vacationing with us again and again, whatever the occasion and whichever brand fits best. We are pursuing that through an integrated vacation ecosystem in which loyalty, technology and data reinforce one another to drive repeat travel and grow the long-term value of each guest.
Loyalty is the foundation of the platform. Status Match carries guests' loyalty status across our brands, while Points Choice and Royal ONE let them earn and redeem rewards across the ecosystem. These capabilities are already driving greater cross brand engagement and repeat travel. In fact, this year, 40% of our guests are loyalty customers.
Loyalty share has increased across nearly all tiers over the last few years with the strongest growth concentrated among entry-level members. This suggests more guests are engaging with the loyalty ecosystem earlier in their journey, expanding the pipeline of future repeat rates and deepening longer-term customer relationships. That deeper engagement is paying off in spend as well. Since we launched Status Match earlier this year, guests who sail across brands have higher APDs than guests who only sail on one brand.
Sandals and Beaches Resorts is where we are putting some additional capital as a TSR accelerator to our strategy. It extends our platform into the attractive all-inclusive category with loyalty benefits flowing in both directions. The roughly 30% category overlap gives us a natural way to introduce Sandals and Beaches to our guests and to welcome their guests into our brands.
Over time, that means more vacation occasions, greater frequency and higher lifetime value for both the Royal Caribbean Group and Sandals and Beaches Resorts. Just as important, this is a business with significant room to grow. The portfolio today has 18 high-quality all-inclusive resorts on some of the most attractive beachfront sites in the Caribbean.
The Stewart family has invested significantly in modernizing the resorts and elevating the guest experience, which is reflected in the quality of the product, guest loyalty, strong pricing and compelling financial performance. The portfolio also includes more than a 1,000 acres of undeveloped Caribbean real estate, much of it adjacent to existing resorts.
Together with Sandals and Beaches proven track record, this scarce hard-to-replicate land portfolio provides a strong foundation for growth. Funded by the business' own cash flow generation, the development plan includes 3 new beach resorts and significant room expansions across the existing portfolio with substantial opportunity to further expand the plan over time as we capture more of the attractive and growing all-inclusive resort market.
Beyond room and hotel expansion, the same capabilities that power our platform are what will drive value from this partnership. We bring decades of experience in revenue management, digital engagement, distribution, procurement, technology and data. Together, we see tangible opportunities to grow revenue, enhance customer acquisition and leverage our global scale while preserving the identity, Caribbean character and differentiated guest experiences of Sandals and Beaches.
All in, we see several hundred million dollars of synergy opportunities over time and every guest we connect across the 2 businesses, strengthens the broader ecosystem. We look forward to sharing more detail once the transaction closes, and we are excited about the value this partnership will create for our shareholders and our customers.
In summary, demand remains strong, and we are encouraged by the strength we are seeing for 2027 and beyond. At the same time, we continue to expand the opportunities in front of us. Our investments in new ships and destinations, Celebrity River Cruises, Sandals and Beaches Resorts, loyalty, digital and technology and broadening our vacation platform and creating more ways for our guests to interact and vacation with us.
We are executing from a position of strength with a growing base of loyal guests, an expanding portfolio of differentiated vacation experiences and significant opportunities ahead. With that, I will turn the call over to Naftali. Naf?

**Naftali Holtz** (Executives):
Thank you, Jason, and good morning, everyone. I will start by reviewing third quarter results. Adjusted earnings per share were $6.57, $0.26 higher than the midpoint of our guidance. Growth in both yields and capacity drove a 9% increase in total revenue for the quarter. Yields for the quarter were 60 basis points above our guidance driven by stronger close-in demand compared to our expectations in July, particularly in Europe and the Caribbean.
Net cruise costs per APCD, excluding fuel, decreased 1.8% year-over-year, approximately 40 basis points better than expected or $0.05 due to timing of costs shifting into the fourth quarter. Adjusted EBITDA was $2.5 billion, margin was 45% and operating cash flow was $1.6 billion.
As Jason noted, booking activity accelerated during the quarter, and our booked position for '26 and '27 is ahead of prior years at record rates. As I discussed last quarter, a more favorable year-over-year comparison, deployment mix and the timing of drydocks provide an approximately 200 basis point benefit to fourth quarter yields in 2026 following a similar headwind in the third quarter.
Capacity is expected to grow 6.6% this year. The Caribbean represents 57% of our capacity and 44% in the fourth quarter. We remain well-positioned in the Caribbean, where our ships, destinations and onboard experiences set us apart, driving positive net yield this year even with the elevated capacity in the region.
Europe will account for 15% of capacity for the year and 10% of capacity in the fourth quarter. Our Europe season has been very successful even with the geopolitical events this year. Lastly, Alaska is expected to account for 5% of total capacity for the year and immaterial for the fourth quarter.
Now let me talk about our updated guidance for 2026. For the full year, net yields are expected to grow approximately 2.1% in constant currency. The increase in yield guidance is driven by out-performance in the third quarter and expectations for fourth quarter yields that are in line with our July guidance. Together with capacity growth of 6.6%, total revenue is expected to grow 9%.
Net cruise costs, excluding fuel, are expected to be approximately flat in constant currency, consistent with our prior guidance. This reflects ongoing efficiency improvements while continuing to invest in the guest experience. We now expect full year fuel expense of approximately $1.35 billion, fourth quarter consumption is 58% hedged and we have continued to opportunistically add hedges for future years.
Based on current fuel prices, currency exchange rates and interest expense, we expect full year adjusted earnings per share to be $17.85 to $17.95. This brings us in line with our initial earnings expectations in January reflecting the strength of the underlying business despite the significant fuel and exchange rates headwinds and the impact we experienced during the year from geopolitical events.
Our higher earnings outlook also reflects stronger-than-expected third quarter results, partially offset by higher projected fuel costs and unfavorable currency movements. We expect continued cash flow to grow to support margin expansion, investment in our strategic initiatives, solid investment grade balance sheet metrics and continued capital returns to shareholders.
Now let me discuss our fourth quarter guidance. In the fourth quarter, capacity is expected to increase 5% year-over-year, and net yields are expected to grow between 4.2% and 4.7% in constant currency in line with our July expectations. As we discussed last quarter, yield growth in the fourth quarter reflects strong demand, a more favorable year-over-year comparison, deployment mix and the timing of drydocks.
Net cruise costs, excluding fuel, are expected to decrease between 0.9% and 1.4% in constant currency. We expect fourth quarter fuel expense of approximately $379 million based on current at the pump prices, net of hedging and forecasted consumption of approximately 463,000 metric tons. Taking all of this into account, we expect adjusted earnings per share for the fourth quarter to be between $3.48 and $3.58.
Looking ahead to 2027, we expect capacity growth of 4.5%, driven by new hardware and fewer drydock capacity days. 2027 deployment mix will be similar to 2026 with 56% in the Caribbean, 16% in Europe, 11% in Asia Pacific and 5% in Alaska. We are also very excited to welcome Hero of the Seas to the fleet in 2027 as well as beginning operating Celebrity River. With Hero of the Seas launching on the 7-night Miami program, Icon of the Seas will move to Galveston, our first Icon class ship in this home port.
We expect yield growth to be weighted towards the second half of the year as the first quarter faces approximately 200 basis points of structural headwinds, including timing of drydocks.
Turning to our balance sheet. We ended the quarter with $7.4 billion in liquidity and leverage below 3x, consistent with our goal of solid investment-grade metrics. During the quarter, we issued $1.25 billion of approximately 5.5% senior unsecured notes due 2034 with the proceeds used to repay a portion of our floating rate term loans and debt maturing in 2027.
In October, we also entered into a $400 million delayed-draw term loan with Export Development Canada, a new source of capital for us and increased our revolving credit facility by $50 million to $6.65 billion. We continue to maintain strong access to diverse sources of capital that support our liquidity, strategic growth initiatives and shareholder returns. I want to provide a few additional details on our investment in Sandals and Beaches Resorts.
We expect to account for the investment as an unconsolidated equity method investment, with results reported on a 1 quarter lag. We expect the transaction to close in early 2027 and for the investment to be immediately accretive to our financial metrics and grow over time.
The contribution to 2027 earnings will be immaterial and depend on when the transaction closes. As Jason mentioned, the business has significant growth ahead of it, including room expansion, new resorts and potential acquisitions. With strong cash flow generation and leverage below 1x, the company can self-fund the ambitious development plan while leaving room for distributions.
At this point, we do not expect to make any more contributions into the joint venture beyond the initial purchase price. The equity income will be included in our financial guidance following the close of the transaction, and we expect to provide more detail then.
In closing, we remain committed and focused on our mission to deliver the best vacation experiences responsibly as we work to deliver another year of strong results. With that, I will ask our operator to open the call for a question-and-answer session.

**Operator** (Operator):
[Operator Instructions] Your first question comes from Matthew Boss with JPMorgan.

**Matthew Boss** (Analysts):
So Jason, as you approach the end of your Perfecta plan, underlying earnings growth as you cited, is pacing to exceed the 20% earnings growth CAGR, if you exclude the impact from the additional fuel. So as we think multiyear, do you see any moderation in the way you're thinking about multiyear prospects for cruise? And any change in confidence around larger picture market share opportunities in that $2 trillion plus total vacation market?

**Jason Liberty** (Executives):
Well, Matt, thanks for the question. I'll start off with the short answer, which is, no, I do not. What we see is, obviously, whether it's our business, or in the general cruise space, we are a sliver of this growing $2 trillion plus travel space.
And quite frankly, that space is predicted to expand at a faster rate than we're going to grow and the cruise industry is going to grow. So I see really strong high-quality demand for the vacation experiences that our different brands are delivering. They are the leaders in their segments.
They're doing that through this incredible innovation on the ships that we build. The vacation experiences that we're delivering on those ships by our incredible crew and of course, the destinations, which we continue to bring on online here, which is elevating guest satisfaction.
Collectively, those things drive a NPS score in the low to mid-70s. So trust is high, expectations are that we're going to deliver the best vacation experience and doing that in a responsible way. And that's resulting in us getting more reps. You combine that with adding River and you're adding all-inclusive resorts further deepens our relationship with our customers, and we're getting more and more reps and which we're clearly showing in the numbers.
So we're very excited, obviously, about the performance this year. We're very encouraged by all the signals we're getting for next year and beyond. And Matt, that's a long way of me saying, we feel really confident in the future.
And we -- with the trust that we've built as well as the technology platforms, whether it's with AI or digital and the connectivity we're bringing across our brands, we feel very confident that we're going to get a greater share of our guests and our customers' vacation wallet. And that vacation wallet is -- we take that very seriously to make sure we're delivering high-quality vacations and they're getting high value for that. But also that share is typically coming because we're able to curate and identify these high-value customers. It's resulting in higher margin and higher lifetime value for that customer.

**Operator** (Operator):
Your next question comes from Steve Wieczynski with Stifel.

**Steven Wieczynski** (Analysts):
Congratulations on the strong results here. So Jason, I want to ask another question about 2027. As we think about getting to your $20 handle next year, I would assume like you're not ready to give exact yield and cost guidance for next -- for 2027, but I would assume it's going to fall under your company tagline of moderate capacity and yield growth and disciplined cost control.
Having said that, I would assume getting to that $20 plus in earnings next year does not include any type of help from things like Sandals, buybacks, debt refis, and I would also assume that if oil prices stay status quo, that's probably embedded in there as well. Just want to make sure that as we think about next year, some of the potential upside to that $20 number.
And then if I can ask a second question as well, Jason. As we think about the 1,000 acres of undeveloped land that Sandals has -- can you just help us think about maybe what some of the potential development opportunities could be there over time as well?

**Jason Liberty** (Executives):
Sure. So I think first to your first point, Steve. One, we don't know exactly when the Sandals transaction is going to close. Our expectations will be end of this year, early next year, but we don't know exactly when it's going to close. And it's also going to be on a quarter lag.
So to answer your first question, whether it is Sandals, whether it is share buybacks, debt refinancings, et cetera, that is stuff that is not in consideration to our statement around next year. And as Naf said in his comments, as we close at that point in time, we'll know -- the timing of that, we'll know what the forecast is based off of the lag. And at that point, we will update guidance. But regardless, we expect the impact for next year to be immaterial to our business. Sorry, you have another...

**Naftali Holtz** (Executives):
Steve, just on the second question on the land. So the purchase price that we paid and we've agreed to includes that 1,000 acres. This is beachfront key locations. We're very excited about continuing to have the company develop that. They have a very, very strong track record of development and enhancements and growing their existing footprint.
Lots of these lands are actually adjacent to existing properties. So these are just building on the current infrastructure they have and they'll just be room expansions in existing locations, and they have -- and there's also a couple of opportunities to do greenfield development in really attractive locations and markets.
Today, they have 18 resorts and 3 of them are being built. So lots of room to grow, expand the keys -- and we, of course, as you know, are very focused in making sure that consistent with our core business, those are developed, of course, to guest satisfaction scores, but also accretive financial results.

**Jason Liberty** (Executives):
Yes. And Steve, I just -- I think it's important to be clear, because I know there's been lots of questions that we've gotten about are we going to show up at Sandals St. Vincent with a cruise ship and tender people into that beautiful resort. The answer to that is no. Sandals needs to be Sandals. Beaches needs to be Beaches.
And there is this massive land bank. And of course, we will collectively be reevaluating on how we or evaluating how we grow this business and also where there might be adjacencies or opportunities, pre-post, et cetera, with our other cruise brands.
But we're trying -- these are additional vacations our guests are taking and we want to make sure they're taking that additional vacation with us. And I think we are very keen. And ultimately, as I made in my comment, we think that -- and not just we think this, but also our partner in this feels very confident that what we have been able to build with technology, with AI, the connected loyalty, obviously, our huge supply chain footprint, et cetera, that there's an opportunity for us to just bring greater scale and synergy to the business, which will not only help elevate the current performance, but it's also going to provide a lot of tailwinds to grow this business.
And as Naf said, the growth of this business is self-contained because this business generates a tremendous amount of cash flow, including the opportunities for dividends. And so we're very excited about this. The last thing I'll say is, this land, when you see it, it's -- I mean, yes, it's adjacent. There are other greenfield opportunities on other parcels of land that are inside this land bank. But it's -- this is not stuff that you can just go buy off the shelf. This has been curated, I mean, brilliantly by the Stewart family.

**Operator** (Operator):
Your next question comes from Trey Bowers with Wells Fargo.

**Raymond Bowers** (Analysts):
I was just going to ask about the '27 commentary where you guys mentioned being up high teens for next year. It's a little bit different language than you guys sometimes use when discussing the book position. I mean it's obviously a really impressive number. I just want to make sure I understand what that represents in terms of is it year-over-year? Or is it quarter-over-quarter? And in terms of the pricing dynamics underlying that are those up again next year?

**Jason Liberty** (Executives):
Yes. I would read that we're just trying to give you a measurement on how we've seen demand elevate for future periods. And of course, we're booked. Our book position is at a higher place and at higher rates.
And I think -- and of course, we're always and you've heard me say this before in the past, we're looking to optimize always our revenue performance.
We have, I think, leading world-class tools that are helping us determine what our best book position and best rate should be at any given point, which I think is why we're seeing the level of performance that we've now seen for several years come out of this. But I would take the commentary as customers are willing to pay us more in the future and today than they did yesterday. And I think that is -- and of course, we're also getting more reps out of our existing customers because our brands, our crew are delivering the very best vacation experiences, which are clearly seen in Net Promoter Scores, which create huge advocacy for us that are in the low to mid-70s.

**Operator** (Operator):
Your next question comes from Ben Chaiken with Mizuho.

**Benjamin Chaiken** (Analysts):
There was an interesting comment in the release this morning Jason, it says 30% of Royal Caribbean guests take all-inclusive vacations and a similar percentage of Sandals Beaches, guests also cruise, maybe in broad strokes, what is the penetration of that today, meaning 30% take all-inclusive, but how many or what percentage are Sandals versus elsewhere, and then vice versa for the percentage of Sandals that are showing up at Royal in broad strokes.

**Naftali Holtz** (Executives):
Hey, it's Naf. It's a good portion, but there's definitely room to grow, and we see that in the results. And when we say they take Sandals, guests take a cruise, they definitely cruise on some of our competitors. And as Jason said before, like, we are very much focused on loyalty. We see our loyalty continuing to grow. We see repeat rates are growing. And so we definitely feel that there is a significant opportunity to capture that and keep them in our ecosystem. That's really our strategy. That's our goal.

**Jason Liberty** (Executives):
Yes. And Ben, I always like to put things in a simple format, which is like today, if a Royal Caribbean customer goes on a competitive cruise brand, I think that's a fail. We offer I think the very best vacation experiences in the key segments, and we go to well over 1,000 different destinations.
And so having connected loyalty and delivering these incredible experiences should keep our customer inside of our ecosystem. Today, that customer might exit our ecosystem to go into River. But into the future, right, as we get into next year, if a customer is not traveling on Celebrity River across our ecosystem, that's a fail.
And then you take that one step further with all-inclusive. People go to a lot of different all-inclusive resorts for many different reasons. But we feel very confident in the level of experience that Sandals and Beaches is producing that when our customers go into all-inclusive resorts in the Caribbean, they should be going to Sandals and Beaches. And collectively, we want to keep that customer in our ecosystem, as I said, because we get better margin -- and we ensure that customer gets the vacation experience that they really desire to go and then we get the repeat rate out of that as well.

**Naftali Holtz** (Executives):
Yes. Just one other thing to note. Similar to what we've seen in River, where the occasion was incremental, not a substitution. The same trend we saw -- we see here as well with all-inclusive. And so the occasion is different, maybe the way you travel or the guest is traveling or the occasion itself. And so that incrementality is really encouraging to us, and we're very excited about making sure that, that comes to us.

**Operator** (Operator):
Your next question comes from Meredith Jensen with HSBC.

**Meredith Prichard Jensen** (Analysts):
I was hoping you might speak a little bit more about opportunities outside the Caribbean. Further out, I think there's going to be unique for El Cielo. Rhapsody will be in Europe, year-round and also thinking about while early days, the terminal in Japan, what this kind of says about what you're seeing, not only in Europe for year-round and winter opportunities. But in Asia and what you're thinking about potential returns there as well.

**Jason Liberty** (Executives):
Yes. Well, I mean, 46% of our business is not in the Caribbean. And obviously, we listen very closely to what our customers are looking to do, their vacation experiences as well as the build-out of other markets like Southeast Asia and Australia, New Zealand and Japan and China.
As we kind of think about that Asia-Pac corridor, we see a lot of opportunities to enhance the vacation offering as well as generate high-quality demand similar as we see in Europe, which is, to me, a vacation playground for our guests.
We see high demand, Alaska, et cetera. So all of our different segments continue to grow. All of our markets continue to grow. And our products continue to grow. They're always competing on where is the most optimal place for our fleet to be. And you're seeing us very -- I would say, on an aggressive basis, build out -- we have well over 100 different destination projects in some form or fashion going on and we're building that out so that it's not just about going to a location.
It's about making sure that the vacation experience when they go to that location, has them walking away with a great experience, memories and stories.

**Michael Bayley** (Executives):
Meredith, it's Michael. Just to add to Jason's point, in 2 weeks, we have the groundbreaking ceremony for the Royal Beach Club in Lelepa, and already that product is very attractive in the Australian market. We have got 4 ships operating out of Australia in '28, 3 in '27. And if you look at our deployment for '27, '28, you'll see that we have moved more capacity into Asia Pacific.

**Operator** (Operator):
Your next question comes from Robin Farley with UBS.

**Robin Farley** (Analysts):
Great. Kind of a 2-part question, if I could, on Sandals. You talked about the benefit and the synergies -- do you see opportunity or interest in land based outside of the Caribbean, there's all-inclusive resorts in other parts of the world. So is this something that Royal might be looking into elsewhere?
And then also any sort of ref -- you made a reference to kind of hundreds of millions in synergies. Is that mostly coming from increasing the reps on the revenue side? Or would some of that be expense? And then I don't know if you have any thoughts about going from 50% to higher ownership of Sandals, if there are sort of provisions for that in the agreement.

**Jason Liberty** (Executives):
Okay. The last one, we're focused on this great partnership we have with the Stewart family. So I won't get into I think is the future ownership outside to say that we're -- I think we're very happy to be able to partner with an incredible operator.  And who's led this business for a very long time. So we're very excited about that. The answer to outside the Caribbean, the answer is yes.
By the way, we also sit on a lot of land around the world, which we don't talk a lot about. But yes, the answer is we think the Sandals brand, we've tested this. The Beaches brand have great legs to it around the world. We are focused, I would say, today on really growing the footprint inside the Caribbean. And we think that is certainly -- well, that's all kind of within our full control. And so I think we're very excited about that.
As it relates to the timing of synergies come in over time, and I think it comes -- this will come in many, many different ways. It will certainly come on the revenue side, whether it's yield management, whether it's the connectivity of our loyalty systems, whether it's -- it's what we've built around data. I mean, we sit on a mountain range of high-quality consolidated, well-tuned data with great analytical layers and capabilities that are on top of that -- and then there's the -- on the cost side, there's always -- it's a very well-run business.
And so the cost side here is about how do we bring scale and to things like purchasing as an example while also balancing the importance of the communities that support the business. So it's just like the Sandals team, we're very community-focused. We're about enhancing benefits for all. But there's going to be opportunities for us to do things at a different level.

**Operator** (Operator):
Your next question comes from Brandt Montour with Barclays.

**Brandt Montour** (Analysts):
So the commentary on 2027 sounds really good. And yet the story of maybe the cruise industry midyear '26 seems to be just really strong sort of close-in demand and consumers booking closer in.
And so I'm curious if there's a bit of a bifurcation under the surface going on, whereby the contemporary brands and/or some of the lower-price itineraries within the spectrum is seeing consumers just maybe temporarily or permanently booking closer in? And if you think that that's a behavioral shift that will last or if that's maybe the signs of a consumer that's on their sort of their last leg and they're sort of spending with what the economy is doing or any sort of thoughts around those dynamics?

**Jason Liberty** (Executives):
Sure. Well, I think, first of all, Brandt, I think if we just look back over time here. I mean, if you look back at the past 3 or 4 years, I think it's pretty -- there's been many -- I think almost every quarter, we've talked about being somewhat surprised to the upside on close-in demand.
And I think that's the reality of the consumer. And it's also a reality of the products that we're offering. So we've made shifts to where we have more -- weekend getaways, we have -- where we have just shorter itineraries. And that's -- and also the incredible ships that we bring online are just attracting more people into that space.
And the shorter products tend to be a closer in booking kind of product. So some of it's product. The second is half of our guests are millennial and younger and so weekend getaways, they take more trips. They basically spend as much as they would on a short trip as they would on a 6 or 7 night type itinerary. And we have more of those guests in the mix.
I think the other thing that I would just -- just to kind of give you the -- another, I think, important data point is onboard spend has been much stronger than we thought it was going to be. Not that we didn't think it was not -- people weren't going to pay more than they did yesterday, but they're paying even more than we had anticipated.
And so I understand there's a lot of noise. There's been a lot of noise in the market this year. There's a lot of geopolitical stuff. But I look at our business, our initial guide for this year had a midpoint of $17.90. And we expect to have -- we have a midpoint on our guidance here of $17.90.
And I think that really talks to the resilience of the business, the resilience of the consumer and how they value effectively the vacation experience that we deliver, which is not only resulting in them paying more, but also them coming back for more.

**Operator** (Operator):
Your next question comes from Conor Cunningham with Melius Research.

**Conor Cunningham** (Analysts):
Good stuff today. Just I wanted to talk a little bit about the spread to land base for a second. You have Disney out there raising prices for park passes. Hilton this morning is talking about RevPAR growing 3% to 4%. I think it could set up a pretty healthy environment for you all.
But on the flip side, you have a competitor that's talking about a decel into 1Q just based on some deployment mixes. I just would think it would be super helpful if you could just talk high level, like any obvious moving parts to net yields next year. I mean, as deployments kind of shift around a smidge here? Just any thoughts there would be helpful.

**Jason Liberty** (Executives):
Yes. Well, I think first, we tend to, I think, lag a little bit to land based. I don't think -- I mean -- I mean our yields over the past several years have grown 35%, still behind where land-based had elevated to. And so when we see land rise, that's typically a good sign, but we tend to lag a little bit behind that increase. It's not a point of view on yield for next year. It's just understanding what has kind of historically occurred. And so that's positive signs that the consumer is willing to spend more on travel.
And because of the value differential, that tends to be great tailwinds for us. I run my cruise line and not others. So I'm not going to really comment there, outside to say that I think us and others have seen different trends. And we're focused -- when we think about our competitive set on vacation experiences, land-based vacation, that's what our customer -- our customers are not really trading us for other cruise lines. They're looking for -- are they doing other vacation experiences that are typically on land.

**Operator** (Operator):
Your next question comes from Vince Ciepiel with Cleveland Research.

**Vince Ciepiel** (Analysts):
You mentioned Icon going to Galveston. I was wondering if you could just talk about how you think that ship is being received in that market? And maybe just thoughts on the Western Caribbean in general over the next couple of years. I know it's somewhat tied to developments in Mexico. But when you think about coming up with deployment and itineraries, how you're thinking for planning around that, which is somewhat up in the air.

**Michael Bayley** (Executives):
Vince, it's Michael. I think Icon is going to be received exceptionally well. It's the best product entering into Texas from the cruise industry in the history of time. So -- it's an exciting product. We've already got a lot of great response from our travel partners and we think it's going to be a huge success.
And of course, it sets the table really for the future as it relates to those itineraries, particularly when we work our way through everything with Mahahual and Cozumel. So we're very optimistic about how Icon is going to perform. As Jason mentioned earlier, these ships are generating Net Promoter Scores in the 80s. And you can tell that if we're filling these ships with 7,600 people with a load factor of 133%, and people are rating it in the 80s, it means that they're having an exceptional time and they're happy to pay a good price for that experience. So we're pretty switched on for Icon.

**Operator** (Operator):
Your next question comes from David Katz with Jefferies.

**David Katz** (Analysts):
I just want to clarify some of the earlier commentary around Sandals, right? Naf referenced it as immaterial as we stand today. My sense is that, that is a comment that's before any synergies, and we can't really have an intelligent conversation about synergies until such time as it closes, right? Is that the right way to characterize that?

**Jason Liberty** (Executives):
Yes. I wouldn't characterize that. This obviously depends on the timing. And so we'll -- we expect this to be closing early in 2027. We'll see -- we're hoping to keep that date. We're working very hard, but it really depends on the timing. And then the synergies, of course, will come over time, not everything will come day one, right? There's a lot of work to do, but we're very excited about what this means to our customers, to their customers as well as to the financial results.

**Operator** (Operator):
That concludes our Q&A session. I will now turn the conference back over to Naftali Holtz, CFO, for any closing remarks.

**Naftali Holtz** (Executives):
We thank you all for your participation and interest in the company. Blake will be available for any follow-ups. We wish you all a great day.

**Operator** (Operator):
Ladies and gentlemen, this concludes today's conference call. Thank you for your participation. You may now disconnect, and have a wonderful rest of your day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### RCL_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CEO｜guidance：全年淨收益率成長財測（原話："We expect net yield growth of 1.75% to 2.25% for the"）
- 2026-07-28｜CEO｜guidance：全年調整後EPS財測（原話："grow 14% and be in the range of $17.73 to $17.87"）
- 2026-07-28｜CFO｜guidance：第三季淨收益率財測（原話："net yields are expected to be roughly flat"）
- 2026-07-28｜CFO｜guidance：第三季運力成長（原話："capacity is expected to be up 8.5%"）
- 2026-07-28｜CFO｜guidance：第四季收益率預期重新加速（原話："we anticipate yield growth during the fourth quarter"）
- 2026-07-28｜CFO｜guidance：第四季約2點有利、第三季同等不利（原話："this provides a 2-point benefit to fourth quarter yields"）
- 2026-07-28｜CFO｜guidance：全年不含燃油淨郵輪成本大致持平（原話："expected to be approximately flat, consistent with"）
- 2026-07-28｜CFO｜guidance：第三季不含燃油淨郵輪成本財測（原話："expected to decrease in the range of 1.1% to 1.6%"）
- 2026-07-28｜CFO｜guidance：第三季EPS財測（原話："between $6.26 and $6.36, a double-digit year-over-year"）
- 2026-07-28｜CFO｜guidance：燃油避險比例（原話："58% hedged at significantly below market rates"）
- 2026-07-28｜CFO｜guidance：為2027年加碼避險（原話："we opportunistically hedged more for 2027"）
- 2026-07-28｜CFO｜guidance：EPS財測受合資事業與財務費用面支撐（原話："benefited from an improved outlook from our joint ventures"）
- 2026-07-28｜CFO｜guidance：佈署組合對收益率的輕微逆風（原話："mix this year creates slight headwinds to yields"）
- 2026-07-28｜CFO｜guidance：CFO說第三季約200基點逆風、第四季類似順風（原話："around 200 basis points headwind to the third quarter"）
- 2026-07-28｜CEO｜guidance：2027年收益率幅度現在談為時過早（原話："exactly what the yield handle will be for next year"）
- 2026-07-28｜CEO｜guidance：載客率目標區間（原話："we're happy with being a couple of"）
- 2026-07-28｜CEO｜guidance：2027年預訂進度與價格（原話："book position is in line with prior years at record pricing"）
- 2026-07-28｜CFO｜margin：Q2 EBITDA 利潤率（原話："EBITDA margin was 38%"）
- 2026-07-28｜CFO｜margin：Q2成本較預期低因時點（原話："timing of our costs shifting to the second half of the year"）
- 2026-07-28｜CEO｜margin：致力擴張利潤率（原話："We also remain committed to expanding margins by"）
- 2026-07-28｜CFO｜margin：Q2收益率較財測高100基點（原話："were 100 basis points above our guidance"）
- 2026-07-28｜CFO｜margin：Q2 EPS超財測中點（原話："$0.33 higher than the midpoint of our guidance"）
- 2026-07-28｜CEO｜risk：中東衝突持續比預期長（原話："the conflict has persisted longer than anticipated"）
- 2026-07-28｜CEO｜risk：歐洲收益率低於預期；管理層稱否則會上調下半年（原話："to the point, we would have raised the"）
- 2026-07-28｜CEO｜risk：歐洲收益率未下降但低於預期（原話："Now that's not to say that European yields are down."）
- 2026-07-28｜CEO｜risk：Mahahual時程受影響（原話："is expected to affect our previously planned time line"）
- 2026-07-28｜CEO｜risk：消費者更審慎支出（原話："Consumers are becoming more deliberate about their spending"）
- 2026-07-28｜CEO｜risk：消費者偏好較近目的地（原話："preferring closer destinations over international trips"）
- 2026-07-28｜CFO｜competition：加勒比海競爭定位（原話："competitive position in the region is strong"）
- 2026-07-28｜CFO｜competition：業界運力偏高下仍成長收益率（原話："with elevated industry capacity in the region"）
- 2026-07-28｜CEO｜competition：對同業促銷的回應（原話："less insulated from what our competitors are doing"）
- 2026-07-28｜CEO｜competition：Celebrity River定價高於同業（原話："higher than what we see in the competitive set for River"）
- 2026-07-28｜CEO｜capital_allocation：Q2回饋股東（原話："we returned over $600 million of capital to investors"）
- 2026-07-28｜CFO｜capital_allocation：股利與回購（原話："we paid $404 million of dividends and repurchased"）
- 2026-07-28｜CFO｜capital_allocation：剩餘回購額度（原話："$805 million remaining under our current share repurchase"）
- 2026-07-28｜CFO｜capital_allocation：流動性與槓桿（原話："$6.9 billion in liquidity and leverage below 3x"）
- 2026-07-28｜CEO｜customer：Royal ONE持卡人重複出航（原話："they are twice as likely to sail"）
- 2026-07-28｜CEO｜customer：年輕客群偏好較短假期（原話："they like to take shorter vacations, like to do"）
- 2026-07-28｜CEO｜customer：重複客消費多20-25%（原話："those repeat guests spend 20% to 25% more"）
- 2026-07-28｜CEO｜customer：近期預訂定價能力（原話："we would typically have to discount for close-in demand"）
- 2026-07-28｜CEO｜commitment：2027年達成Perfecta（原話："reaching Perfecta by the end of next year"）
- 2026-07-28｜CEO｜commitment：App個人化功能明年初推出（原話："you'll start to see in early next year"）
- 2026-07-28｜CEO｜commitment：不為完美做規劃（原話："we don't plan for perfection"）
- 2026-07-28｜CEO｜commitment：以溫和收益率成長加成本控制創造價值（原話："tremendous shareholder value with moderate yield growth"）
- 2026-07-28｜CEO｜product：西加勒比佈署可能邊際調整（原話："That's not our expectation today, but there might be."）
- 2026-07-28｜CEO｜product：Mahahual狀態不評論（原話："we're not really in a place to comment on the status of that"）

### 問答異常語氣（迴避／改口／保留）
- RCL_Q2_2026_Earnings_Call_20260728.md｜問：Farley：2027在手訂單的載客率與價格是否較去年同期高｜答法：CFO只答「booked very well and at higher prices」；CEO說載客率「more or less in line」，未給具體數字
- RCL_Q2_2026_Earnings_Call_20260728.md｜問：Dove：2027是否可能是高於長期算法的一年｜答法：CEO反駁「comps are easy」，說明年收益率幅度太早，未給方向或數字
- RCL_Q2_2026_Earnings_Call_20260728.md｜問：Montour：Mahahual延後是否影響2028-29年東西加勒比50-50目標｜答法：CEO答「we'll see」，表示不評論開發狀態，僅稱部署可能邊際調整
- RCL_Q2_2026_Earnings_Call_20260728.md｜問：Rollo：第三季載客率是否降、預訂載客率是否因晚訂單轉弱｜答法：CEO談價格紀律與管理最適載客率，未直接回答第三季或未來載客率是否下降
- RCL_Q2_2026_Earnings_Call_20260728.md｜問：Cunningham：第四季隱含收益率走升的驅動｜答法：CFO稱「not guiding to it」，只給約200基點時點性順逆風，未談需求面

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
{"date":"20260729","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"供給端結構性受限使郵輪業具備長期定價地板——全球船廠年交付上限 14-16 艘、RCL 已鎖定 Meyer Turku 檔期至 2036，供給無法對需求上升快速反應"},{"id":"H2","text":"Perfecta 兌現且其後仍有 10%+ 的內生成長——2027 年調整後 EPS 達到相對 2024 的 20% CAGR（$20.4）、ROIC 17%+，且 2028-2031 靠運力 +5%／收益率 +2%／利息下降／回購維持雙位數 EPS 成長"},{"id":"H3","text":"市場對這門生意的估值框架不再下移——退出倍數維持在 Fwd P/E 14-16x 的成熟複利區間，而非回到 pre-COVID 郵輪業的 11-13x 週期股區間"}],"extra_text":"# | 具體數字門檻（floor） | 信息來源 | 漂移觸發條件\nH1 | FY2027 RCL 運力成長 ≤ +5%；FY2027 淨收益率 CC ≥ +2.5%；全球船廠年交付 ≤ 16 艘 | 船廠產能上限與六家主要船廠集中度：Hope Research Group《Cruise Capacity Growth 2026-2028》（2026）；Meyer Turku 長約鎖至 2036、Icon 6/7 訂單：Royal Caribbean Group 新聞稿（2026-05）；RCL 自身 2027-2029 運力 +4%／+6%／+7%：產業運力預測（2026） | 連 4 季淨收益率 CC 低於 +1.5%（5Y 假設，季節性過濾後）→ 削弱；連 6 季低於 0% → 反轉。單季地緣造成的波動不觸發。\nH2 | FY2026 調整後 EPS ≥ $17.73（指引下緣）；FY2027 ≥ $20.0；FY2031 ≥ $32；單船增量 ROIC ≥ 13% | FY2026 指引 $17.73-17.87：RCL Q2 2026 財報新聞稿（2026-07-28）；FY2027 共識 $20.01（n=28）、FY2028 $22.76：Koyfin/Excel 共識快照 2026-07-16 ＋ yfinance earnings_estimate（2026-07-29）；Perfecta 目標定義：RCL 新聞稿（2025-03） | FY2027 共識連 4 季累計下修 &gt; 5%（5Y 假設）→ 削弱；共識跌破 $18.5 → 反轉（Perfecta 結構性失敗）。\nH3 | Fwd P/E（FY+2）≥ 13x；EV/EBITDA ≥ 11x | 本報告自算之後疫情期（2023-01 起）Fwd P/E（FY+2 口徑）分布：低 4.72x／中位 11.05x／p75 14.47x／高 20.06x，現值 16.12x（§11.1）；EV/EBITDA 5 年均 13.36x、2025-12 峰 15.4x：GuruFocus／valueinvesting.io（2026） | 連 4 季 Fwd P/E（FY+2）低於 11x → 削弱（市場重新以週期股框架定價）；連 6 季低於 9x → 反轉。"},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"地緣事件持續壓抑地中海與近端國際航線。中東衝突已持續超出管理層預期，改變了消費者的目的地偏好（因機票成本轉向近程）。歐洲占 Q3 運力 28%，單季曝險遠高於全年 14%。"},{"id":"R2","text":"加勒比海運力集中投放引發系統性降價。加勒比海占全球郵輪運力 42%、占 RCL FY26 運力 57%；2026 年加勒比海部署較 2025 年增加 12%，2027-2029 產業運力續增 +4%／+6%／+7%。同業已在加速促銷。"},{"id":"R3","text":"目的地資產的政治與監管風險系統化。Mahahual 時程已受影響；墨西哥 DNR 稅三年 4.2 倍；EU ETS 自 2026-01 起 100% 涵蓋且擴及甲烷與氧化亞氮；美國 Section 883 免稅地位（RCL 有效稅率僅 1.9%）長期存在政策檢討風險。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd P/E(FY2027E) ≤ 14.5x（約 $290）；或 FY27 共識上修使該倍數自然回落至 14.5x 以下","irr_base_pct":9.4,"ev5y_pct":30.6,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.8,"ev5y_pct":30.6,"irr_base_pct":9.4,"max_dd_pct":-60.0,"bull_5y_price":646.0,"bear_5y_price":170.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd P/E(FY2027E) ≤ 14.5x（約 $290）；或 FY27 共識上修使該倍數自然回落至 14.5x 以下","price_at_dd":322.5,"archetype":"品質複利成長","cycle_position":"晚循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RCL_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
