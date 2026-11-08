你是 stock-analyst **v20 判斷 agent**，標的 TMDX（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TMDX","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TMDX_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TMDX_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenue_gaap","label":"Total revenue (GAAP)","value":203.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 新聞稿（8-K ex99.1）https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm"},"note":"未查"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":14.2,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"% (adj. op income $28.9M)","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 新聞稿（8-K ex99.1）https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm"},"note":"未查"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":13.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"% (op income $28.1M)","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 新聞稿（8-K ex99.1）https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm"},"note":"未查"},{"id":"f_kpi4_guidance_fy2026_revenue_","label":"Guidance FY2026 revenue (incl. PAD Aviation)","value":"764-774","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"$M（含 PAD；不含 PAD 750-760，上調自 737-757）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 新聞稿（8-K ex99.1）https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm"},"note":"未查"},{"id":"f_kpi5_gross_margin","label":"Gross margin","value":58.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 新聞稿（8-K ex99.1）https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_tmdx_gross_margin_pct","label":"TMDX 毛利率","value":58.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TMDX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tmdx_operating_margin_pct","label":"TMDX 營業利益率","value":12.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TMDX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tmdx_fcf_margin_pct","label":"TMDX FCF 利潤率","value":11.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TMDX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abt_gross_margin_pct","label":"ABT 毛利率","value":56.67,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abt_operating_margin_pct","label":"ABT 營業利益率","value":13.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abt_fcf_margin_pct","label":"ABT FCF 利潤率","value":13.37,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mdt_gross_margin_pct","label":"MDT 毛利率","value":65.01,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mdt_operating_margin_pct","label":"MDT 營業利益率","value":19.04,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mdt_fcf_margin_pct","label":"MDT FCF 利潤率","value":16.33,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_gkos_gross_margin_pct","label":"GKOS 毛利率","value":64.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GKOS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gkos_operating_margin_pct","label":"GKOS 營業利益率","value":-25.3,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GKOS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gkos_fcf_margin_pct","label":"GKOS FCF 利潤率","value":2.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GKOS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_podd_gross_margin_pct","label":"PODD 毛利率","value":71.88,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PODD.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_podd_operating_margin_pct","label":"PODD 營業利益率","value":18.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PODD.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_podd_fcf_margin_pct","label":"PODD FCF 利潤率","value":7.29,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PODD.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_sbc","label":"SBC","value":12.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"$M（約占營收 6.0%、占 GAAP 營業利益 43%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q3 2026 新聞稿（8-K ex99.1）https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm（10-Q 權益表列 $12.6M，口徑差異）"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":88.24,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":30.07,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":66.55,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.51 → 1.51）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.25 → 2.25）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.31 → 3.31）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.51,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.25,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.31,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-3.21,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 1.56 → 1.51（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":24.04,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"2 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.21,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.73,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":58.44,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 1.51，分子＝快照價 88.24","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":373.94,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 866.9、現金 492.96（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":34.73,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":3438.86,"period":"2026-11-08","unit":"USD m","basis":"市值 3064.92 ＋ 淨負債 373.94","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":769.07,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":895.08,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.47,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 88.24 / W52 100.08 / W104 98.73 / W250 84.35 / W250 13週斜率 1.09%"},{"id":"f_ma_w52","label":"52 週均線","value":100.08,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":98.73,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":84.35,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.09,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"10-K稱OCS是市場上唯一獲FDA核准的可攜式多器官溫灌注裝置；冷保存／冷灌注供應分散。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"Our Organ Care System is the only FDA approved portable, multi-organ, warm perfusion device on the market.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K風險因子承認他方可能開發更好、更便宜產品使OCS過時，且許多對手資源更大。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"Other companies may develop technologies and products that result in improved patient outcomes or are safer, easier to use, less expensive or more readily accepted than the OCS.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"XVIVO心臟冷灌注Heart Assist Transport預期2026年有機會獲FDA PMA核准，主要對手為TransMedics。","source":"briefglance: New Hope for Hearts: XVIVO Trial Boosts Organ Viability","url":"https://briefglance.com/articles/new-hope-for-hearts-xvivo-trial-boosts-organ-viability","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子揭露營收來自有限數量客戶，客戶可能改用其他器官保存方式（冷藏、常溫區域灌流）或減少業務；該段未提及任何客戶導入第二供應商或自製 OCS 的事件。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"We generate a significant amount of our revenue from a limited number of customers. However, our customers may not continue to utilize our products or services at current levels, pricing, or at all, and our revenue could fluctuate significantly due to changes in economic conditions, the use of other methods for organ preservation, such as cold storage or normothermic regional perfusion","as_of":"2026-02-24","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2023–FY2025 三年均無單一客戶占營收超過 10%，且 2024、2025 年底無客戶占應收帳款超過 10%。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"For the years ended December 31, 2025, 2024 and 2023 no customer accounted for more than 10% of revenue. As of December 31, 2025 and 2024, no customer accounted for more than 10% of accounts receivable.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"風險因素仍揭露營收來自有限數量客戶，失去或大幅減少主要客戶業務將對營收造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"We generate a significant amount of our revenue from a limited number of customers. However, our customers may not continue to utilize our products or services at current levels, pricing, or at all, and our revenue could fluctuate significantly","as_of":"2026-02-24","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026 review: growing graft demand, wider transplant criteria and rising organ disease leave a global shortage of transplantable grafts; US waitlist >104,000 in late 2024, ~7,000 die yearly before receiving an organ (shortage framed as persistent/structural)","source":"Transplant International 2026 review (Frontiers) / News-Medical Dec 2025","url":"https://www.frontierspartnerships.org/journals/transplant-international/articles/10.3389/ti.2026.16100/full","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TMDX reported 5,139 U.S. OCS cases in FY2025, +38% vs 3,735 in FY2024; Q2 2026 revenue +20.7% YoY to $189.9M and low end of 2026 guidance raised to $737-757M (ex-PAD)","source":"TransMedics 8-K / Q4 2025 and Q2 2026 results (via search summaries)","url":"https://www.sec.gov/Archives/edgar/data/0001756262/000119312526206347/tmdx-ex99_1.htm","excerpt":"Second-quarter 2026 revenues rose 20.7% year over year to $189.9 million.","as_of":"2026-07-30","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Management reaffirmed ~10,000 transplants/yr by 2028 on current heart/lung/liver platform (ex kidney); kidney and international drive 10,000->20,000 by 2030-2032; 2028 target $1.2B revenue and 30% op margin","source":"vectorshift TMDX 2026 Q2 earnings summary","url":"https://vectorshift.ai/research/companies/transmedics-group/earnings/2026-q2-summary","excerpt":"Reaffirmed ~10,000 transplants by 2028 on the current heart/lung/liver platform (excluding CHOPS and kidney); kidney and international drive 10,000->20,000 by 2030-2032.","as_of":"2026-07-30","retrieved_at":"20261108","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"2026 adjusted operating margin outlook cut to 12.5%-14% from ~16% mainly due to accelerated OCS Kidney investment; commentary frames it as capex/execution story","source":"Zacks-based article on TMDX Q2 2026","url":"https://www.panabee.com/news/transmedics-earnings-q1-2026","excerpt":"Management reduced its 2026 adjusted operating-margin outlook, excluding PAD Aviation, to 12.5%-14% from about 16%, mainly because of accelerated OCS Kidney investment.","as_of":"2026-07-30","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Visible Alpha consensus (S&P Global, Apr 2026): OCS Heart revenue ~$157M in 2026 (+25%), US heart volumes 909 (2025) to 1,124; US OCS Lung volumes nearly doubling to 194","source":"S&P Global Market Intelligence: TransMedics clinical pipeline to drive next phase of growth","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/03/transmedics-clinical-pipeline-to-drive-next-phase-of-growth","excerpt":"Visible Alpha consensus points to OCS Heart revenues reaching $157 million in 2026, an increase of 25% year-on-year, supported by US unit volumes rising to 1,124 from 909 in 2025.","as_of":"2026-04-01","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Competition/consolidation: Terumo acquired OrganOx for $1.5B (Aug 2025) per a single low-quality market report; no concrete 2026-27 competitor capacity announcements found","source":"Market research report (organ perfusion market)","url":"https://www.htfmarketintelligence.com/report/global-ex-vivo-organ-perfusion-technology-market","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K FY2025 Item 3 列出的法律程序為證券集體訴訟（Jewik／Collins 合併案，D. Mass.），未列反壟斷調查或拆分程序。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"On August 8, 2025, Lead Plaintiffs filed a consolidated amended complaint. Like the earlier-filed complaints, the amended complaint purports to assert claims pursuant to Sections 10(b) and 20(a) of the Exchange Act and Rule 10b-5","as_of":"2026-02-24","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因子指出歐盟等主管機關對醫療公司與醫療提供者互動的審查加強，調查可能增加成本；屬產業一般性監管風險，非針對 TMDX 的已知調查。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"Responding to investigations can be time-and resource-consuming and can divert management’s attention from the business.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"TMDX FY2025 10-K MD&A：進口少部分零組件的關稅使 2025 年營業成本小幅增加。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"For example, tariffs related to a small portion of components that we import moderately increased our cost of revenue in 2025.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：美國對中國及他國加徵關稅、貿易限制與出口管制，及他國報復，可能影響供應商與 OCS 產品／飛機零組件價格。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"Additional tariffs, trade restrictions and export controls imposed by the U.S. on a broader range of imports, or further retaliatory trade measures taken by China or other countries in response, may impact our suppliers and the price of our components for our OCS products or our aircraft.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Section 232 醫療器材調查（2025-09-02 開啟）截至 2026-10 更新仍未結案；搜尋結果未提及 TMDX。","source":"SPS Commerce, Section 232 Medical Device Tariffs: The Investigation That Never Closed","url":"https://www.spscommerce.com/community/articles/section-232-medical-device-tariffs-the-investigation-that-never-closed","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["triggers","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露 OCS Console 與 Perfusion Set 部分零件向單一來源、少數為唯一來源供應商採購；部分零件為客製、無現成替代，換供應商可能需 FDA 核准設計變更","source":"TransMedics FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":null,"as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Fresenius Kabi 為 OCS Lung 與 OCS Heart 之 OCS Solutions 單一來源供應商","source":"TransMedics FY2025/FY2023 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":null,"as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"OCS Console 與一次性 Perfusion Set 在麻州 Andover 單一廠區設計與組裝；滅菌依賴第三方；FY2025 10-K 稱新總部預計 2028 年 1 月遷入","source":"TransMedics FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":null,"as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"國家器官運送(NOP)依賴第三方私人飛機網絡，供給受美國私人飛機與合格飛行員數量限制，供應商未必優先配合其航班","source":"TransMedics FY2023 ARS (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312524091891/d72709dars.pdf","excerpt":null,"as_of":"2024-04-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收 $203.0M，年增 41%（有機 35%）；產品 $113.4M（+29%）、服務 $89.6M（+60%）；FY2026 指引上調至 $764–774M（含 PAD Aviation 約 $14M），前次 $737–757M 不含 PAD。","source":"TransMedics 8-K Ex.99.1 (Q3 2026 results, 2026-11-05)","url":"https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"2025 美國 OCS 移植 5,139 例（約占心／肺／肝移植 26%），肝 OCS 滲透率 36%；管理層目標 2030 年 2–3 萬例移植；腎臟平台預計 2027 年進入 FDA 試驗，時程曾有變動。","source":"TransMedics Q4 2025 earnings call summary (Yahoo Finance) / Baird conference transcript (Investing.com)","url":"https://finance.yahoo.com/news/transmedics-group-inc-q4-2025-173531840.html","excerpt":null,"as_of":"2026-02-25","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Terumo 收購 OrganOx；管理層視為市場驗證並主張以臨床結果為護城河（競爭者出現）。","source":"TransMedics Q4 2025 earnings call summary (Yahoo Finance)","url":"https://finance.yahoo.com/news/transmedics-group-inc-q4-2025-173531840.html","excerpt":null,"as_of":"2026-02-25","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：他方可能開發出結果更好、更安全、更易用或更便宜的技術，使 OCS 過時或失去競爭力；許多替代品供應商資源遠大於公司。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"Other companies may develop technologies and products that result in improved patient outcomes or are safer, easier to use, less expensive or more readily accepted than the OCS. These products or technologies could make the OCS obsolete or noncompetitive and reduce demand for our OCS products.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：公司須持續向外科醫師、移植中心與支付方證明 OCS 相對冷藏保存（cold storage）或新競爭技術的價值。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"We must continue to educate surgeons, transplant centers and private and public payors and demonstrate the merits of the OCS compared with cold storage or new competing technologies.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"搜尋彙整指出 XVIVO Perfusion 為另一家灌流保存器材競爭者；本次搜尋未找到具體 2026 年威脅 OCS 的替代產品上市紀錄。","source":"Simply Wall St 社群敘事 TMDX","url":"https://simplywall.st/community/narratives/us/healthcare/nasdaq-tmdx/transmedics-group/fp74bkfw-fda-trials-and-logistics-expansion-will-spark-mixed-outcomes-478q","excerpt":"XVIVO Perfusion (XVIVO.ST), which has also developed perfusion-based storage devices and services that extend organ viability and reduce complications.","as_of":"2026-07-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 描述商業模式以高比例經常性收入為特徵，來源為一次性 OCS 耗材組與 NOP 對移植中心提供的服務；FY2025 營收 $605.5M（+37.1%）。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"Our business model is characterized by a high level of recurring revenue, which is derived primarily from sales of our single-use, organ-specific disposable sets that are required for each transplant using the OCS as well as services provided to transplant centers by our NOP.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"搜尋摘要顯示公司正把 NOP 服務與物流模式複製到歐洲（義大利首個物流標案，並規劃義大利、荷蘭、比利時），未見訂閱制或通路去中介化的正式轉變。","source":"WebSearch 摘要（引 TMDX 10-Q/8-K，2026）","url":"https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449827/tmdx-20260930.htm","excerpt":null,"as_of":"2026-11-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 2026（8/4 公布）營收 $189.9M 年增 20.7%，高於共識 3.1%；調整後 EPS $0.44 低於 Zacks 共識 $0.50；FY2026 營收指引低標上調至 $737–757M（前為 $727–757M）。","source":"Zacks/Chartmill, TransMedics (TMDX) Q2 Earnings Lag Estimates; BioSpace, TransMedics Reports Second Quarter 2026 Financial Results","url":"https://www.chartmill.com/news/external/107600/transmedics-tmdx-q2-earnings-lag-estimates","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat：2026-06-02 共識評級 Hold，13 家券商平均目標價 $134.00（7 Hold／6 Buy）；5 月 MarketBeat 約 $135。其他聚合站（無明確日期）區間 $113–$128.92，低 $70–$85、高 $142–$178。","source":"MarketBeat, TransMedics Group given average rating of Hold by brokerages (2026-06-02); StockAnalysis; Benzinga","url":"https://www.marketbeat.com/instant-alerts/transmedics-group-inc-nasdaqtmdx-given-average-rating-of-hold-by-brokerages-2026-06-02/","excerpt":null,"as_of":"2026-06-02","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 財報後 Piper Sandler 維持 Overweight 但目標價由 $120 降至 $100；MarketBeat 8/5 標題為財報後股價跳空下跌；MarketBeat 後續共識目標價 $124.45（日期不一）。","source":"MarketBeat, TransMedics earns overweight rating from Piper Sandler (2026-08-05)","url":"https://www.marketbeat.com/instant-alerts/transmedics-group-nasdaqtmdx-earns-overweight-rating-from-piper-sandler-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"搜尋摘要指 2026-11-05 公司將 FY2026 營收指引上調至 $750–760M（不含 PAD Aviation；含則 $764–774M），前為 $737–757M；Zacks 稱同時下調調整後利潤率展望至 12.5%–14%（未獲一手來源確認）。8-K 內文未讀。","source":"SEC 8-K Ex.99.1 (TransMedics Q3 2026 results) via search summary; Webull","url":"https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 前 Zacks 預估修正趨勢不利，Zacks Rank #5（Strong Sell）；Zacks 共識 FY 營收 $733.24M／EPS $1.82，低於當時指引中點約 2%。Benzinga 顯示放空比例約 38.6% 流通股。","source":"Zacks via Nasdaq, Why Is TransMedics (TMDX) Up 10.2% Since Last Earnings Report?; Benzinga","url":"https://nasdaq.com/articles/why-transmedics-tmdx-102-last-earnings-report","excerpt":null,"as_of":"2026-09-04","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"證券集體訴訟 Jewik／Collins 已合併，2025-08-08 提出合併修正起訴書，被告 2025-10-07 聲請駁回，法院裁定時間未定（10-K 截至 2026-02-24）","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"On October 7, 2025, defendants filed a motion to dismiss the amended complaint for failure to state a claim. Lead Plaintiffs’ filed their response to the motion on November 21, 2025, and defendants’ filed a reply in further support of their motion on December 22, 2025. We cannot anticipate when the court will rule on that motion.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 9 份 8-K 中僅 1 份含重大項目（2026-01-12 總部租約 Item 1.01），無併購、重編等重大項目","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001756262&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"2026-01 與 2026-02 FDA 分別完整核准下一代 OCS Lung（DENOVO）與 Heart（ENHANCE）IDE；2026-04 發表 CHOPS 冷保存系統以支援對照組收案。尚無新器械上市核准","source":"搜尋摘要：Finviz／S&P Global Market Intelligence／Quantisnow","url":"https://finviz.com/news/311875/tmdx-wins-full-fda-ide-approval-for-next-gen-ocs-enhance-heart-trial","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"2026-04 簽訂投資德國 PAD Aviation 的definitive agreement，建置歐洲移植空運物流網；屬策略投資，非收購公司","source":"TransMedics 新聞稿／搜尋摘要","url":"https://rallies.ai/news/transmedics-invests-in-pad-aviation-to-build-european-organ-transplant-air-logistics-network","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月 8-K 無 2.01／1.02 等併購類項目；2026-04 僅有投資 PAD Aviation（策略投資）","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001756262&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Jewik v. TransMedics（D. Mass.）證券集體訴訟，class period 2023-02-28 至 2025-01-10；已與 Collins 合併，駁回聲請待裁","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"On February 14, 2025, a class action captioned Jewik v. TransMedics Group, Inc., et al., Case No. 1:25-cv-10385, was filed against the Company and certain of its current and former officers in the U.S. District Court for the District of Massachusetts.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"+","claim":"DENOVO Lung IDE 完整核准（2026-01）、ENHANCE Heart IDE 完整核准（2026-02）；兩試驗進行中，尚無結果","source":"Finviz／S&P Global 搜尋摘要","url":"https://finviz.com/news/311875/tmdx-wins-full-fda-ide-approval-for-next-gen-ocs-enhance-heart-trial","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"0","claim":"10-K 風險因子載明過去曾自願從臨床站點召回部分 OCS 產品；搜尋未見近12個月新召回或 FDA 警告信","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm","excerpt":"We have voluntarily recalled certain OCS products from clinical sites in the past and may need to take similar actions in the future, which may result in notices to regulatory agencies in other jurisdictions.","as_of":"2026-02-24","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"TMDX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":58.69,"operating_margin_pct":12.21,"fcf_margin_pct":11.82,"rd_intensity_pct":13.83},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TMDX","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"ABT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.67,"operating_margin_pct":13.9,"fcf_margin_pct":13.37,"rd_intensity_pct":6.8},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABT","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"MDT","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":65.01,"operating_margin_pct":19.04,"fcf_margin_pct":16.33,"rd_intensity_pct":7.77},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"GKOS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.78,"operating_margin_pct":-25.3,"fcf_margin_pct":2.81,"rd_intensity_pct":27.12},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GKOS","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"PODD","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.88,"operating_margin_pct":18.44,"fcf_margin_pct":7.29,"rd_intensity_pct":11.3},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PODD","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"TMDX"},"financial_history":{"ticker":"TMDX","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":93459000.0,"revenue_yoy_pct":null,"gross_margin_pct":69.84,"operating_margin_pct":-33.64,"net_income":-36231000.0,"diluted_eps":-1.23,"free_cash_flow":-57724000.0,"fcf_margin_pct":-61.76,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":241623000.0,"revenue_yoy_pct":158.53,"gross_margin_pct":63.77,"operating_margin_pct":-11.89,"net_income":-25028000.0,"diluted_eps":-0.77,"free_cash_flow":-192087000.0,"fcf_margin_pct":-79.5,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":441540000.0,"revenue_yoy_pct":82.74,"gross_margin_pct":59.36,"operating_margin_pct":8.49,"net_income":35464000.0,"diluted_eps":1.01,"free_cash_flow":-80941000.0,"fcf_margin_pct":-18.33,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":605494000.0,"revenue_yoy_pct":37.13,"gross_margin_pct":59.92,"operating_margin_pct":17.93,"net_income":190291000.0,"diluted_eps":4.87,"free_cash_flow":133589000.0,"fcf_margin_pct":22.06,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TMDX/TMDX_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**TransMedics Group, Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Good afternoon, and welcome to TransMedics Third Quarter 2026 Earnings Conference Call. [Operator Instructions] As a reminder, this call is being recorded for replay purposes.
I would now like to turn the call over to Hannah Jeffrey from The Gilmartin Group for a few introductory comments.

**Hannah Jeffrey** (Attendees):
Thanks, operator. Good afternoon, and welcome to TransMedics' Third Quarter 2026 Earnings Call. I'm joined by our President and CEO, Waleed Hassanein; and our CFO, Fernando Araujo.
During this call, we will make forward-looking statements, which are based on how we see things today and are subject to various assumptions. As described in our SEC filings, actual results may differ materially due to risks and uncertainties.
Our conference call remarks will also include both GAAP and non-GAAP financial results. Reconciliations between GAAP and non-GAAP measures, along with information regarding our use of forward-looking statements can be found in today's press release and in the presentation slides available on our website.
With that, I will hand the call over to Waleed.

**Waleed Hassanein** (Executives):
Thank you, Hannah. Good afternoon, everyone, and thank you for joining TransMedics third quarter 2026 earnings call. I'm delighted to be joined today by Fernando Araujo, our new Chief Financial Officer, who will review our third quarter financial results in detail later on, on this call.
TransMedics has built one-of-a-kind transplant business founded on 5 fundamental -- 5 foundational assets that are extremely difficult to replicate. At the core is our transformative OCS technology platform, amplified by our clinical organ procurement and donor screening services and enabled by our vertically integrated logistics network and NOP digital assets. Together, they form a single integrated platform with one purpose to increase the number of organ transplants and improve outcomes for patients worldwide. Our goal is crystal clear, to be the trusted partner to every stakeholder in organ transplantation committed to growing transplant volumes, maximizing efficiency and improving post-transplant clinical outcomes. We are very proud of what we've built, but we are not standing still. We firmly believe our best innings are still ahead, and this conviction is why we continue to invest in innovation-driven growth across technology, services and digital transformation of the transplant ecosystem. I will update you on the progress of these initiatives shortly.
Turning to 3Q results. The third quarter of 2026 was the strongest in TransMedics' history for both revenue and case volume. Third quarter highlights include: total revenue of approximately $203 million, up approximately 41% year-over-year; transplant product revenue of $113 million, up approximately 29% year-over-year and transplant service revenue of roughly $79 million, up approximately 44% year-over-year. Despite typical third quarter seasonality, OCS Liver and Heart case volume grew both year-over-year and sequentially, modestly surpassing the all-time high levels we set in the second quarter of 2026. As our near and midterm growth initiatives begin contributing to case volumes, we fully expect product revenue growth to accelerate further and converge with our service growth rates.
TransMedics transplant logistics generated approximately $41 million in revenue, up approximately 50% year-over-year. We supported approximately 86% of NOP missions requiring air transport using our own fleet. This is consistent with our second quarter performance and meeting our steady state goal of managing more than 80% of our NOP missions. We ended the quarter with approximately $493 million in cash and cash equivalents.
Looking at our third quarter results, we are especially proud of our record revenue performance, which was driven primarily by market share gains in Liver and Heart and strong clinical service revenue. Again, we delivered this growth despite typical third quarter seasonality and lower overall U.S. disease donor volume that was down 6% in 3Q 2026. Importantly, we achieved these results with no incremental contribution yet from ENHANCE Part B or DENOVO. We also drove product service margin expansion and generated approximately $20 million in cash.
Beyond this strong financial performance, we also successfully advanced several of our near and midterm growth initiatives. Let me start with the Heart, where we're working to further expand OCS adoption in the existing indication and expand into new indications in the United States. Our ENHANCE Heart Part A program was designed to demonstrate the safety and effectiveness of our OCS Heart 2.0 enhancements and a new proprietary perfusion solution within our current OCS Heart indications, which covers extended criteria DBD and DCD donor hearts. We completed enrollment of 175 patients in September. And in October, FDA approved a continued access protocol, or CAP, allowing us to enroll an additional 90 patients in the CAP protocol. We expect CAP enrollment to begin in late fourth quarter 2026 or early first quarter 2027.
ENHANCE Heart Part B is designed to open an entirely new indication for TransMedics, focusing on DBD donor hearts preserved within roughly 4 hours of preservation. This segment represented approximately 2,200 heart transplanted in 2025. In late October, FDA approved our IDE protocol amendment to include the TransMedics Controlled Hypothermic Organ Preservation System, or CHOPS, as the control arm. That gives us 2 shots on goal in this segment, OCS Heart and the TransMedics CHOPS with the potential to offer the market 2 distinct options at different price points. Part B is designed to enroll approximately 600 patients, 400 on OCS and 200 on CHOPS. Participating centers are now completing their internal IRB processes, and we expect Part B to be a major catalyst for our Heart business beginning in the first quarter of 2027.
Next is expanding adoption of OCS in the lung transplant market, which we believe could be a sleeping giant for TransMedics business. Our DENOVO Lung program leverages our Gen 2.0 OCS Lung enhancement and again, a new proprietary perfusion solution to generate data that we believe will catalyze a large untapped U.S. lung transplant market of approximately 3,500 transplants annually, the vast majority of which use no form of machine perfusion today. In late October, FDA also approved our IDE protocol amendment to include CHOPS as the DENOVO control arm. Together, OCS Lung and TransMedics CHOPS represent a significant opportunity to transform this market. DENOVO is designed to enroll approximately 450 patients, 300 in OCS and 150 on CHOPS. As with ENHANCE, centers are completing their IRB processes, and we expect DENOVO to be a major catalyst for our Lung business beginning in the first quarter of 2027.
Taken together, ENHANCE Heart and DENOVO Lung give us access to conservatively estimated 2,000 to 5,000 incremental U.S. heart and lung cases annually, materially expanding our U.S. addressable market. In addition, data from these programs will also help catalyze heart and lung transplant adoption internationally.
Beyond our clinical programs, we continue to make progress expanding OCS NOP and transplant logistics in Europe. Tamer and our European commercial team have made significant strides and are preparing to launch OCS NOP in Italy, Netherlands, Belgium -- and Belgium in H1 2027. We are also in active discussion with several additional European countries about expansion beyond these initial markets. This groundwork supported strong European performance in the third quarter of 2026.
Importantly, I'm delighted to report that in October, our PAD Aviation business won TransMedics' first European transplant logistics tender in Italy's Emilia-Romagna region. This is a strategic first step towards our vision of a dedicated pan-European transplant logistics network modeled on what we have built in the United States. With significant need and established budgets for transplant logistics across Europe, we see logistics as a powerful entry point for OCS NOP in the many countries where we are actively engaged. We expect OCS NOP and European transplant logistics together to become another growth catalyst for TransMedics in 2027.
Meanwhile, we remain laser-focused on OCS Kidney, our entry into the largest transplant market segment with what we believe will be the first portable normothermic oxygenated kidney perfusion system. In the U.S., approximately 21,000 diseased donor kidneys are transplanted each year and approximately 9,000 more go unused, in part due to prolonged ischemic time. This is the single largest addressable transplant segment available to us in the U.S. and globally. We are building OCS Kidney on our NextGen 3.0 platform, which is designed to add meaningful scale and operating leverage across our business. OCS Kidney development is progressing well, and we remain on track for the first in-man clinical experience in the second half of 2027. From there, we expect OCS Kidney to become another major growth catalyst for TransMedics beginning in late 2027 and into 2028.
And finally, turning to the U.S. transplant and OPO modernization initiatives led by HHS and CMS. On October 30, CMS released its final rule on OPO certification. The key highlights were: CMS affirmed the outcome-based 3-tier performance framework and that it will be applied on a DSA-by-DSA basis. CMS allowed for OPOs for the first time to hold multiple DSAs with CMS formalizing when a DSA opens for competition and how successor OPOs are selected. In addition, CMS removed the historical requirements that an organization must have operated as an OPO between 2002 and 2005 to qualify to become an OPO. This opens the door for new entities to become OPOs. However, CMS deferred finalization of a pathway for new OPOs to further rule-making process. CMS also stipulated that designation period may be shortened or extended and CMS may directly assign a DSA when time doesn't allow for a full competitive process.
Bottom line is, based on our review, we see nothing in the final rule that would prevent TransMedics business from progressing as planned as we do it every day. Meanwhile, we are actively collaborating with approximately 20 OPOs across the United States to help them improve donor organ utilization and meet CMS performance tier metrics. We remain committed to supporting every OPO in meeting or exceeding these metrics because doing so ultimately means saving more American lives.
Turning to guidance. Given our strong year-to-date performance and balance against the timing of our new program contributing to early 2027 rather than the fourth quarter, we are raising our full year 2026 revenue guidance to a range of $764 million to $774 million, inclusive of approximately $14 million from PAD Aviation, representing growth of approximately 26% to 28% over 2025. Importantly, this range assumes no meaningful incremental revenue from ENHANCE Part B or DENOVO in the fourth quarter. Fernando will detail the guidance update in his section of today's call.
In summary, over the past 4 years, TransMedics has consistently turned strategic investments into both rapid top line growth and strong bottom line performance. We are a growth company at our core, leading bold, far-reaching innovations across our OCS technology platform, our clinical and logistics services and the digital transformation of the entire transplant ecosystem. The progress we made on our growth initiatives in 2026 gives us the confidence that our best years are still ahead. TransMedics is once again well positioned to lead the next wave of innovation in organ transplant worldwide in 2027 and beyond.
With that, I will turn the call over to Fernando to review our third quarter financial results in detail. Fernando?

**Fernando Araujo** (Executives):
Thank you, Waleed. Good afternoon, everybody. As this is my first call with the company, I want to reiterate my excitement at joining TransMedics at such an important stage in the company's growth. What drew me here is our differentiated technology, strong market position and multiple growth catalysts, a combination that provides us with a significant opportunity to scale the business, expand operating leverage and drive long-term shareholder value. My focus will be on partnering with the team to execute these growth opportunities with financial discipline while advancing our mission to transform transplant care.
Now turning to TransMedics' third quarter performance. The third quarter delivered strong revenue growth and stable gross margin, reflecting the underlying strength of the business alongside planned strategic investments in R&D and infrastructure to support our next phase of growth. Total revenue was $203 million, up 41% year-over-year, including organic revenue of $194 million, up 35% year-over-year, making this the highest quarterly revenue in our history. U.S. transplant revenue was approximately $186 million, up 34% year-over-year and 1% sequentially.
By organ, liver contributed with approximately $150 million, heart approximately $33 million and lung approximately $2 million. International revenue was approximately $6.6 million, up 82% year-over-year, reflecting continued progress as we expand our presence in Europe.
Product revenue was $113 million, up 29% year-over-year and 2% sequentially, led by liver and heart. Despite typical third quarter transplant seasonality, liver and heart case volumes grew modestly both year-over-year and sequentially, building on the all-time high we set in the second quarter. We expect product revenue growth to accelerate as our near and midterm growth initiatives begin contributing to case volumes.
Service revenue was $90 million, up 60% year-over-year and 14% sequentially. Service revenue included $9.4 million of revenue generated from PAD Aviation charter services. Excluding PAD, service revenue was up approximately 43% year-over-year. The growth in service was driven by higher NOP adoption, primarily around liver and heart and continued improvements in logistics, market share gains and pricing adjustments to offset higher fuel costs.
The gross margin was 58.5%, down approximately 40 basis points year-over-year. It's important to note that the gross margin decrease reflects a channel mix shift in the quarter. Service revenue, which carries a lower margin than product revenue, rose to 44% of the total revenue and PAD Aviation diluted gross margin by 260 basis points. Excluding PAD, gross margin was 61.1%, up approximately 230 basis points year-over-year. As PAD is integrated into our business, we expect to see improved margins moving forward.
Looking at the margin drivers of our respective channels, product gross margin was 79.2%, up 50 basis points year-over-year. This improvement was driven by process improvements related to reduced scrap and cycle count. Service margins improved 440 basis points to 32.2%, driven by logistics efficiencies resulting from pricing improvements across both service and logistics operations, productivity gains from reduced supplemental lift utilization, lower ground transportation cost per mission and improved leverage of fixed operating costs as volume increased.
It is worth noting that we do expect some normalization in service margin in the fourth quarter while remaining above historical levels. We plan to keep working these same levers as part of our operational strategy, improving efficiency across NOP and in manufacturing, while next-generation OCS and OCS Kidney are designed to cost less to build and run.
Adjusted operating expenses were $89.8 million, up 47% year-over-year and 3% sequentially. The year-over-year increase was driven by planned investments in OCS Kidney, next-generation OCS and our ENHANCE and DENOVO clinical programs, as well as increased headcount to support our development activities, ongoing expansion plan and infrastructure investments, including our U.S. headquarters and the addition of PAD Aviation. The sequential increase was primarily related to the addition of PAD. Excluding these investments, operating expenses declined sequentially, demonstrating continued discipline across our cost base.
Adjusted R&D was $29.2 million, up 91% year-over-year, primarily reflecting investment in the strategic growth programs. Adjusted SG&A was $50.6 million, up 32% year-over-year and 9% sequentially. The year-over-year increase reflects planned investments in the NOP network, IT infrastructure, international expansion and in our Somerville headquarters.
Adjusted income from operations was $28.9 million, representing an adjusted operating margin of 14.2%, highlighting our strong top line results and our planned increase in strategic investments. Adjusted net income was $18.9 million and adjusted diluted earnings per share was $0.51.
Now for modeling purposes, interest expense was $7.3 million in the quarter, including approximately $3.9 million related to the finance lease for our new Somerville headquarters. For the full year, we expect total interest expense of approximately $29 million, including approximately $15.4 million related to our new headquarters, partially offset by approximately $11 million of interest income.
Our adjusted effective tax rate was 23.8% in the quarter, and we expect it to end at this level for the full year. Our diluted weighted average shares were approximately 40.8 million in third quarter, and we expect the share count to remain at the similar levels for the full year.
We ended the quarter with $493 million in cash and cash equivalents, an increase of $20 million sequentially. Approximately $18 million in restricted cash, primarily related to our headquarters lease is reported separately.
Now turning to our 2026 outlook. As Waleed noted, we're raising our full year 2026 revenue guidance from a range of $737 million to $757 million to a new range of $764 million to $774 million, representing growth of 26% to 28% compared to 2025. This revenue guidance is inclusive of approximately $14 million for the full year from PAD Aviation. Excluding the contributions from PAD Aviation, our updated revenue expectations of between $750 million to $760 million represents growth of 24% to 26% year-over-year.
In terms of operating margin, we remain confident in the previously communicated full year adjusted operating margin range of 12.5% to 14%. As a reminder, this range primarily reflects the accelerated investments in our OCS Kidney program, which is critical strategic growth driver for the business.
Looking ahead, we expect gross margin to remain around current levels in the near to midterm as we continue to invest in R&D and in the international expansion. At the same time, the operational improvements we are driving in manufacturing and across the NOP, along with disciplined management of our broader cost base give us the capacity to keep investing in R&D and new technology without losing sight of profitability. Over the long-term, we expect those investments to pay off. Greater scale and utilization across our international platform, together with the efficiencies designed into OCS Kidney and next-generation OCS should support a higher sustainable gross margin profile with potential to further improvement.
To close, on our capital allocation, priorities remain focused on long-term value creation, supporting innovation across our technology and clinical pipeline, strengthening our NOP and international platform and building the systems and infrastructure required to support scale.
With that, I'll turn the call over to Waleed for his closing remarks.

**Waleed Hassanein** (Executives):
Thank you, Fernando. In summary, the third quarter was the strongest in TransMedics' history, recorded revenue of approximately $203 million, up 41% year-over-year, recorded case volume -- record case volume and margin expansion in both of our product and service businesses, and we delivered all of this before any incremental contribution yet from ENHANCE Heart Part B and DENOVO Lung. We enter 2027 with strong momentum and a robust set of growth catalysts. ENHANCE Heart Part B and DENOVO Lung target large untapped heart and lung segments with 2 shots on goal in each through OCS and CHOPS. In Europe, we plan to launch OCS NOP in Italy, the Netherlands and Belgium, building on our first European transplant logistics win achieved in October of this year. And OCS Kidney remains on track for first-in-human clinical experience in the second half of 2027, our path into the largest transplant market.
Again, our strategy is crystal clear. Our execution is proven. Our conviction has never been stronger. We are building the global platform to transform organ transplantation, and we strongly believe our best years are still ahead.
With that, I will turn the call over to the operator for questions. Operator?

**Operator** (Operator):
[Operator Instructions] Your first question comes from Bill Plovanic with Canaccord.

**Zachary Day** (Analysts):
It's Zachary on for Bill. Congrats on the quarter. I want to start with expanding into Europe. Obviously, American investors might not have a lot of visibility into what those operations look like. Can you take a second and talk about the cadence of tenders you might get with the markets that you're going into moving forward? And just what maybe reimbursement and operations might look like, how NOP is different over there versus in the U.S.?

**Waleed Hassanein** (Executives):
Zach, that's a very important question, but it's a very complex and will require a significant amount of time to address it in detail. However, to highlight, all the geographies that we are actively engaged with had some level of reimbursement for the product and the service and definitely for the logistics. So reimbursement comes first before we engage in any of these geographies. We believe that the -- from a clinical demand, Europe, as we always said, is a mirror image of the U.S., which effectively nearly double our total addressable market, and it's a critical market for organ transplantation.
What's unique about Europe is transplant logistics is well established, budgets has been well established and the access to PAD Aviation enables us to compete and as we've proven successfully in these tenders. I'll leave it here. We are confident in the strategy. We see transplant logistics as a unique attributes of the European market entry strategy given the pre-existing budgets for logistics. But at the end of the day, it has to also be supported with revenue growth from OCS and NOP. And in all the geographies, we're actively engaged with OCS and NOP-type services are reimbursed.

**Operator** (Operator):
The next question is Ryan Daniels with William Blair.

**Matthew Mardula** (Analysts):
This is Matthew Mardula on for Ryan. Congrats on a really strong quarter. So regarding the strong organic revenue growth seen in the third quarter, why do you think TransMedics wasn't as impacted by the traditional seasonality seen this quarter? I know you discussed how industry volume was down and how you took market share. But just given the really strong organic revenue growth, what caused those market share gains, especially this quarter?
And then lastly, kind of given that Q3 performance, should we still think of seasonality in Q3 the same as before? Or do you have more of that ability to offset it now?

**Waleed Hassanein** (Executives):
Thank you for the question. I think what blunted the seasonality impact in this quarter is the healthy adoption and market share gains that we've gained in all market segments for heart and liver, both DBD and DCD. This is really a result of the experience, both experiencing the benefits of NOP, but also, in the case of the heart, the contribution of the ENHANCE Part A catalyzed that adoption. Also, the participation of the OPO program that we're supporting many OPOs in the country to help them salvage more organs and transplant more organs. So that's why we weathered the storm this quarter.
As far as going forward, I think with the success of Part B, ENHANCE Part B and DENOVO, we might be able to blunt the seasonality. The reality is, there was seasonality in Q3 in August this year. But the success of our team, NOP team and taking market share, both in DBD and DCD for heart and liver helped us blunt that. So I don't want to guess. I think the success of Part B, ENHANCE and DENOVO could help us blunt that going forward. But Q3, there is always seasonality during the summertime.

**Matthew Mardula** (Analysts):
Great. And I know you talked about the OPO final rule, and I might have missed this, but do you plan to apply to become an OPO? And if you do plan to apply, how does that kind of non-for-profit requirement for OPOs determine the ultimate structure? And then if you're not planning to apply kind of what's the reasoning behind that?

**Waleed Hassanein** (Executives):
This is all speculation. We can't apply to something when we don't know what the rules are. And CMS has not announced the rules yet, has not -- all they said -- all they stated is they will -- any new entity wishing to become an OPO will have to wait for a new rule-making process. We will have to wait for that rule-making statement, and we'll see what the conditions are before we decide whether or not it makes sense for us to apply or not.

**Operator** (Operator):
Your next question comes from Young Li with Jefferies.

**Young Li** (Analysts):
I wanted to follow up on the trials and CHOPS economics. Can you maybe just talk a little bit more about if you're charging for using CHOPS with the trials, the level that you might charge and how much of a premium it would be priced versus other code systems?

**Waleed Hassanein** (Executives):
Young, thank you for the question. We are focusing on the clinical impacts of these programs. We are not focusing on the commercial impact of these programs yet. Our top priority right now is to initiate these programs because of the significant potential value that the patients would experience using these programs. The bottom line is, we are not going to discuss any of the pricing or any of that. It's way too premature. We need to get the program started. We need to get the data flowing. And when CHOPS is 510(k) in the U.S., we can talk in detail about the commercial rollout of CHOPS. But until then, the priority is getting the clinical programs initiated, getting the clinical value to the transplant patient, utilizing more organs and gaining the confidence in the 2 options that are available for heart and lung transplants.

**Young Li** (Analysts):
Great. And I guess to follow up on the EU question. Are you able to size the tender that you won in Italy? How big could that be for you? Is it like a multiyear tender or just 1 year?

**Waleed Hassanein** (Executives):
It's a multiyear tender. Again, we are going through the process right now of finalizing that. Again, everything we are going to be involved with in Europe going forward is going to be a multiyear tendering process, especially in Italy, it's going to be region by region. The goal is the aggregate of these different regions will be several millions, if not tens of millions of dollars annually, but we just won the first, hopefully, out of many. So we're excited about this important first step. And the reason why we engaged is, it has the significant potential of growing our revenue in Italy. So we're excited about that. And hopefully, we will win additional tenders. There are several tenders coming up late in the fall and early in the winter.

**Operator** (Operator):
Your next question comes from Allen Gong with JPMorgan.

**Unknown Analyst** (Analysts):
This is Henry on for Allen. There are a couple of questions from us, and I'll ask them both upfront. So, obviously, a strong quarter, a good strong beat. But when we look at the guidance, it was raised a bit lower. Can you talk about any conservatism or just the philosophy behind the guide?
And then second question, we've seen a little bit of softness maybe in the fourth quarter October flight trends. Can you just talk about what you're seeing and any trends there from your side?

**Waleed Hassanein** (Executives):
On the first part of the question, our philosophy on guidance has always been to be conservative. Q4, obviously, we have the holiday season coming up, and we don't know what, if any, seasonality might happen. We're also being conservative and not factoring in any meaningful contribution from ENHANCE Part B or DENOVO. That's why our guidance is what it is.
On the second part -- on the second question, listen, again, as I've stated many times, the flight trend is an indicator. It's not the be-all, end-all. But yes, I mean, the flights are down in October. It's a fact, but we still have November and December, and we've seen similar trends in Q3. So it's difficult for me to predict the full quarter based on a couple of weeks' worth of softness in flights. Also, as you can see in Q3 results, we had more car transports in Q3 than aviation. So, again, we need to weigh all that into our guidance and not just read the tea leaves based on a couple of weeks of soft flights and conclude what the quarter would look like. And we believe we achieved that level -- that balance of conservatism in the guidance we stated.

**Operator** (Operator):
Your next question comes from Chris Pasquale with Barclays.

**Christopher Pasquale** (Analysts):
Waleed, I want to make sure that we understand how ENHANCE Part A impacted your results. 175-patient study, how much of that activity took place in the third quarter, and what percentage of those cases do you think are really incremental to the business versus procedures that TransMedics likely would have been involved in anyway?

**Waleed Hassanein** (Executives):
Chris, thank you for the question. We've always stated that ENHANCE Part A we don't consider as incremental because these are the indications we have. However, the excitement about the outcomes that were seen by the transplanting surgeons certainly helped increase our adoption in Q3. There's no equivocality about it. Many of the transplant programs are commenting anecdotally about how these hearts are coming out of the device looking better, recovering quicker, less edema, all the potential benefits that we had hoped that we would replicate in the clinic from what we've seen in the preclinical phase. So we have a high degree of confidence that, that Part A, albeit the same indication, helped drive deeper adoption in this indication because transplant programs were excited to see the enhancements in Part A.

**Christopher Pasquale** (Analysts):
And then maybe one for Fernando. Congratulations on the new role. I would love any directional commentary you can provide at this time on R&D spending and how that's going to trend as we get into '27. It stepped up a lot this year, and that's before Part B gets going. It's before DENOVO, before Kidney moves into first-in-human testing. And so, as we think about just sort of what the budget looks like for all the programs you guys have going on next year, does that need to move meaningfully higher? Or have you front-loaded some of that expense here this year?

**Fernando Araujo** (Executives):
Yes. No, thank you for the question. And like I said in the prepared remarks, we expect the R&D to be fairly stable at this level for the foreseeable future here, like meaning for the next few quarters. That said, we are in the middle of our budget process. And obviously, we're going to be able to refine the overview and provide better detail as we get through the fourth quarter earnings and provide full year guidance for 2027. But we expect that we are stable at this level that we are, at least for the next few quarters. And then we will see what is up next in terms of new technology that the team really wants to pursue. And we'll make sure that we have the financial capability to really support that while maintaining, which is very important, the profitability at the levels that we anticipate here.

**Operator** (Operator):
Your next question comes from Josh Jennings with TD Cowen.

**Joshua Jennings** (Analysts):
Waleed, hoping to just circle back on ENHANCE Part A and just wanted to get an update on just timing of filing and potential approval for the NextGen OCS Heart System for the current indication. And then you gave some positive feedback in your answer to Chris around heart transplant surgeons' feedback. I would love to hear your team's kind of response to that feedback and your optimism that this next-generation OCS Heart can enable day-only heart transplant surgeries.

**Waleed Hassanein** (Executives):
Thank you, Josh, for the question. I think, as always, it's a very loaded question, Josh. I want to be cautious. Until the final results of the trial are read out, everything I stated is anecdotes. I was trying to address Chris's question what -- how confident are we that the contribution of heart market share gain was from ENHANCE Part A, and that was what I was trying to address. However, I've always stated when a trial enrolls ahead of schedule, that gives us good signals. And this trial enrolled even faster. This portion of the trial enrolled even faster than the DCD heart enrolled with a much higher number of patients. So we are cautiously optimistic.
We need to wait for the follow-up period to be concluded, and the plan is to be filing the PMA amendment for the existing indication based on Part A sometime in '27. And obviously, it will be up to the FDA to review the material and issue their opinion on the matter. But we are cautiously optimistic, Josh, and we hope to be able to submit for a PMA indication in 2027.

**Joshua Jennings** (Analysts):
Maybe one follow-up just on CHOPS and any update on the 510(k) filing and clearance time line, and just remind us how you could launch CHOPS outside of ENHANCE Part B and DENOVO?

**Waleed Hassanein** (Executives):
Thank you, Josh. As we've always stated, our commitment to FDA was to ensure that CHOPS is 510(k) cleared independently of the trial. And we are going to deliver on that commitment to FDA. Right now, we believe the second half of '27 is the target time line where we may receive that 510(k) decision, given that we are prioritizing H1 to getting the device ready for the regulatory 510(k) review process. And we still are holding ourselves to that time line. So yes, the answer is yes.
There's a possibility that we will have CHOPS 510(k) approved in 2027 before ENHANCE Part B is completed. In fact, that's what FDA would love to see us deliver on. And depending on timing of filing the ENHANCE Part A PMA amendment or PMA supplement, we might have that as well before year-end of 2027. But we have to wait and see.

**Operator** (Operator):
Your next question comes from Samantha Munoz with Piper Sandler.

**Samantha Munoz** (Analysts):
Congrats on a great quarter. I guess, first, could you talk about what you're seeing competitively in the market? It looks like you gained a good amount of share in liver and heart this quarter. And then maybe could you just provide more color in terms of whether you're going deeper into accounts or is this gaining new accounts?

**Waleed Hassanein** (Executives):
Thank you, Sam, for the question. As I stated before, it's really difficult for me to comment on competition. I think that question should be saved for the competition. My focus is to make sure that every quarter our team is making progress, taking market share, and growing our top line. And I think Q3 met that expectation. And we're working hard on Q4 and into 2027. We need to -- as I stated before, we need to be extremely confident and comfortable to operate in a very, very crowded market today. And that's why we lead with innovation. And we're constantly challenging the status quo and any potential competitor based on innovation. And we were willing to put our innovation, our technology, and our services against anybody to continue to be in that leadership position. So, I guess, that's the answer on the status of the competition.

**Samantha Munoz** (Analysts):
And then just one more on CMS's recent final rule. It looks like they're placing greater scrutiny on transport-related adverse events. Could you talk kind of like what you see for those in the market and whether there's an opportunity for TransMedics to differentiate itself based on the reliability of its NOP network?

**Waleed Hassanein** (Executives):
Thank you, Sam. I think the examples that CMS are focusing on are the traditional examples that we've seen for many, many years. Some kidneys that are shipped on commercial flights, they might not make it on time or they might end up in the wrong aircraft, that kind of stuff. So for us, it is crystal clear, and CMS knows it and everybody in the field of organ transplant knows it, that having the vertical integration of transplant logistics gives us the highest degree of reliability that we can give back to the transplant community, whether it's an OPO or a transplant center, because we can track the organ from the minute it leaves the donor body until it arrives to the recipient. Not us tracking it, but also we developed the digital ecosystem to enable that full transplant tracking of the organ by the accepting transplant program and the OPO staff that were involved in that particular organ.
So there's no doubt in my mind that we deliver the best logistic -- transplant logistics service on planet Earth. The key for us is to continue to innovate, continue to drive more market share, and hopefully help many of the OPOs to deliver more organs and utilize more organs for transplantation.

**Operator** (Operator):
Your next question comes from Suraj Kalia with Oppenheimer.

**Suraj Kalia** (Analysts):
Waleed, can you hear me all right?

**Waleed Hassanein** (Executives):
I can hear you just fine, Suraj.

**Suraj Kalia** (Analysts):
Gentlemen, congrats on a great quarter. Waleed, a couple of quick questions, there are like a gazillion calls going on at the same time. As part of the IDE approval for ENHANCE B, were any protocol amendments mandated? That's part A.
And part B of my question, Waleed, I would love to get your comments on the RE-UP procedure. There's always something new that people keep bringing up. Any of your comments and thoughts on RE-UP versus NRP and how we should think about it moving forward would be greatly appreciated. Gentlemen, congrats again.

**Waleed Hassanein** (Executives):
Thank you, Suraj. We appreciate it. On the first part of the question, mandated protocol amendments by FDA? The answer is no. We made proposals to the protocol, the FDA reviewed it, and they allowed it. So there's no FDA-mandated protocol changes.
Related to RE-UP, I think our position on RE-UP, like many others, and I think Farhan gave a very data-driven presentation that actually raised a lot of questions about the validity of the RE-UP procedure. He did that in our symposium at the ISHLT. I'll leave it at that. And again, I point to our great results in Q3, where we took market share both in DBD and DCD heart. And I also remind the audience that RE-UP is only used in 1 center in the United States. But our position on RE-UP is well stated in a public presentation that was data-driven from Farhan, our Head of the Cardiothoracic team, at the ISHLT.

**Operator** (Operator):
Your next question comes from David Rescott with Baird.

**David Rescott** (Analysts):
Congrats on the results here. Just one from us. I guess it's a two-parter, so maybe you can count it as 2. I think you commented on this U.S. TMA, OPO modernization after -- that's going on. And we've seen some other things, I think, recently there's this new DCD rule I think that's coming into effect in November, and then on the kidney side, you had the National Care -- the Kidney Care National Plan that came out a couple of weeks ago. So curious as to what your thoughts are if at all on both of those. And then more of a high-level question on this topic, more related to how you see kind of the political landscape or just this broader policy environment playing out today versus what it kind of looked like a couple years ago, and where you foresee that going over the next couple of years, of course, as you continue to expand and drive data and adoption of the technology?

**Waleed Hassanein** (Executives):
Thank you, David. That's a very complex set of comments/questions. Let me start by the biggest and most impactful one, which is the HHS Kidney Care National Plan that was issued in October 2026. In that plan, HHS clearly stated that their goal is to increase kidney transplantation by approximately 2,000 kidneys per year, which they estimate in that report that we have an economic benefit per transplant of approximately $4.7 million per transplant. You multiply 2,000 kidneys by $4.7 million, you end up with $9.4 billion implied value for each year added to the transplant patient, or kidney added -- or 2,000 kidneys added for the transplant population, which amounts to $200 billion of projected economic benefits through 2040. That's based off of 2,000 kidneys added.
As I highlighted, and the data is crystal clear on it, last year there were about 9,000 kidneys discarded only for ischemic time. There's only 1 device that we're aware of that could reduce ischemic time and frankly eliminate ischemia during preservation, and making more kidneys available for transplant, which is the OCS Kidney when it becomes available. So we see these initiatives as highly complementary, highly focused on what OCS, and NOP, and TransMedics do well, which is maximize donor organ utilization for transplant, increase efficiency, and improve post-transplant clinical outcomes. We do all of the above.
The same thing applies for the DCD ruling. The DCD ruling pretty much we saw some cowboyish behavior that came into the system. What HRSA and CMS are trying to do is put protocols in place to maximize patient safety and maximize utilization of organs. Again, we stand by the utilization rate of OCS in the DCD and DBD population to be the highest ever recorded in the history of organ transplant, north of 94% or 95%. So we are not afraid of these initiatives. We're not afraid of the initiatives of even CMS final rule. We do not see any of these things as negative or detrimental. We see it all as complementary, and we see TransMedics' role is to be supportive to all stakeholders in the field, OPOs, transplant centers, and regulators, to ensure that we are delivering the best organ transplant care to American patients in the U.S. So we are inspired by what's going on.
I'm not going to comment on the political environment. The issue around organ transplantation has always been bipartisan from day 1. Both administrations, both types of political views, have supported organ transplantation. So we'll leave it at that.

**Operator** (Operator):
Your next question comes from Tom Stephan with Stifel.

**Thomas Stephan** (Analysts):
Apologies if this has been asked, just jumping between calls. But I wanted to ask a bit on trends and the base business guidance. If I look at October flights and then maybe take the typical November and December declines in the U.S. transplant market relative to October? You're getting to OCS vols maybe down sequentially in the fourth quarter versus the third quarter. Yet based on the core business guide for revenues and your service revenue commentary, it sounds like you do expect product revenue to be up sequentially in 4Q, correct me if I'm wrong there. So for that, I think it's roughly a $198 million midpoint guide for -- implied for 4Q on total revs in the base biz. I guess, Waleed, what gives you the confidence in hitting that number when it seems like trends in 4Q maybe are tracking down sequentially and not up?

**Waleed Hassanein** (Executives):
Tom, thank you for the question. I think your characterization that Q4 -- second half of Q4 usually goes down is -- I don't think it's accurate. I think the opposite is true. We see a significant up-ramp in the second half of Q4 for a variety of different reasons. So we expect to see the same here. Yes, October was clearly a soft month, but again, I'm not willing to give up on the quarter just off a couple of weeks of slowness in October. And from our track record, from our history, from our performance, usually the last 6 to 8 weeks -- 6 to 7 weeks in Q4 is usually a significant recovery for a variety of different reasons.
So what gives us the confidence is our track record. What gives us the confidence is we're living this day in and day out. And we're not just looking at trends in the rearview mirror, and also all the catalysts that are coming up in front of us in the remainder of Q4 and exiting the year.

**Fernando Araujo** (Executives):
Yes, and Tom, just maybe adding, I think you referenced that you were jumping calls, so you probably didn't hear Waleed answered a similar question before. But what is important to highlight on top of what he already highlighted here is the fact that just taking the flight data might not necessarily be all comprehensive. There is clear evidence that we're making really good progress on other forms of transportation as well, including ground. So just wanted to make sure you have confidence, we have done a pretty good job in making sure that we have confidence in this guidance. And we believe we are guiding to a degree conservatively in the way we're thinking about the sequential progress between third quarter and fourth quarter.

**Thomas Stephan** (Analysts):
I might have to check back on that OPTN data. But all makes sense. And then quick follow-up just on op margins next year in 2027. I think Street ex-PAD has been modeling positive year-over-year op margin expansion next year. So maybe talk about kind of your level of comfort in that with the base business posting operating margin accretion in '27, given all the initiatives that, I think, clearly have some nice momentum. And then as a tack-on, it'd be great if you can help us with what the PAD impact in '27 from a margin standpoint might look like, how will that business's op margin maybe compares to the base business?

**Fernando Araujo** (Executives):
Tom, first of all, a few of your questions that truly get into the '27 guidance, which I'm going to defer to our fourth quarter earnings, where I'm going to be able to provide a more detailed understanding of the business. So I'm not going to comment on the PAD performance in 2027. I'm going to wait for when we get to the call in the fourth quarter, like I said.
But what I would say to you is, to your question related to the margin, I think it's safe to say, and it was part of my prepared remarks, we feel very strong about the way the progression of the business is going from a gross margin standpoint. And we believe that with the productivity programs that we have in place, both for product and service, we'll be able to hit those numbers and continue to drive continued progress, which is what we're going to keep using for margin leverage as well as continuing to do a fairly good job in making sure that we fund the business on the R&D side of the house.
So hopefully it answers your question for today, and like I said, I'm looking forward to being able to refine the models which we're working through right now as it relates to the budget, and we'll guide at a more detailed level in February.

**Operator** (Operator):
Your next question comes from Mike Matson with Needham & Company.

**Michael Matson** (Analysts):
Yes. So I just want to ask one on the kidney trial. I don't know if you're able to talk about how you expect to design the trial, but my understanding is the standard of care there's hypothermic perfusion. So is that what you'd likely be using as your control? And then how do you sort of avoid the same issue you had with the heart and lung trials where the competitors didn't want you using their devices for the trial?

**Waleed Hassanein** (Executives):
Thanks, Mike. We are at least a year away from discussing the detail on the kidney trial design. So we still have a long way to go. It's way too premature to start talking about the kidney trial design. However, related to the control arm, the control arm is the standard of care, as you said. It's cold perfusion. It's been in the market for 25 years. We don't expect the same reaction, given that this technology is not in the hands of the transplant programs. It's in the hands of the organ procurement organizations. They manage it broadly. So we don't expect the same dynamic here as the highly concentrated call points for heart and lung that we've experienced with the controlled hypothermic storage. So -- but we have a long ways to go before we can share the detail of the design of the kidney trial, and obviously, we will do that in the first half of 2027.

**Operator** (Operator):
Your next question comes from Daniel Markowitz with Evercore ISI.

**Daniel Markowitz** (Analysts):
I wanted to know, following the final OPO rule, how are you thinking about timing of potential decertifications and transitions? Could those handovers create further near-term disruption to donor activity before we see the benefits of reform come through? I guess, overall, just wondering how you expect this dynamic to impact the more near-term, call it, 2027, and then in the longer term beyond '27 as well.

**Waleed Hassanein** (Executives):
Thank you, Daniel. It's very hard, obviously, nobody knows what the impact is, but from reading the CMS final rule, I think actually CMS is being very thoughtful about this and trying to minimize the disruption. They're extending the runway from a time line perspective. They're opening the door for many of the OPOs in Tier 2 to merge even before the decertification process takes place. They're giving a lot of runway for Tier 2s. So I -- my own perception is, this is going to be a lot more controlled, and we hope that it doesn't show -- it doesn't result in any disruption in the national volume, given that's already done. I mean, the final rule has come out. CMS is not changing their mind. Unless something happens during the challenge process, we don't expect much to change.

**Operator** (Operator):
That concludes our Q&A session. I will now turn the conference back over to Dr. Waleed Hassanein for any closing remarks.

**Waleed Hassanein** (Executives):
Thank you, operator. We thank you all very much for taking the time to be with us tonight, and we wish you all happy holidays. And we will meet again early next year. Thank you very much. Have a good evening.

**Operator** (Operator):
This concludes today's call. Thank you for participating. You may now disconnect, and have a wonderful rest of your day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TMDX_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜Waleed Hassanein｜guidance：CEO 提高 2026 全年營收財測下緣至 737–757M 美元、年增 22–25%（原話："$737 million to $757 million, representing 22% to 25%"）
- 2026-08-04｜Waleed Hassanein｜guidance：財測假設不含 PAD Aviation 營收，且不含 ENHANCE Part B／DENOVO 的實質增量營收（原話："assumes no revenue contribution from PAD Aviation"）
- 2026-08-04｜Gerardo Hernandez｜guidance：CFO 說明財測中點的下半年季增型態與過去兩年平均相近（原話："because at the midpoint, it reflects a second half"）
- 2026-08-04｜Gerardo Hernandez｜guidance：全年調整後營業利益率預期（不含 PAD）為 12.5%–14%，先前預期約 16%（原話："adjusted operating margin, excluding the impact of PAD"）
- 2026-08-04｜Gerardo Hernandez｜margin：管理層將營業利益率下修歸因於 OCS Kidney 投入提高（原話："prior expectation primarily reflects the higher planned"）
- 2026-08-04｜Gerardo Hernandez｜guidance：2026 下半年毛利率預期（不含 PAD）約 59%（原話："For the second half of 2026, we expect gross margin"）
- 2026-08-04｜Gerardo Hernandez｜margin：2026 年後毛利率（不含 PAD）預期未來 2–3 年維持現水準，長期約 60%（原話："Looking beyond 2026 and excluding PAD Aviation, we expect"）
- 2026-08-04｜Gerardo Hernandez｜margin：服務毛利率由 Q1 約 27% 升至 Q2 35%，歸因於機隊使用率與效率（原話："approximately 27% in the first quarter of 2026 to 35% in"）
- 2026-08-04｜Gerardo Hernandez｜margin：產品毛利率 77%，與上季大致持平（原話："Product gross margin was 77%, broadly stable sequentially."）
- 2026-08-04｜Gerardo Hernandez｜margin：管理層預期下半年服務毛利率回落但仍高於歷史水準（原話："normalization in service margin during the second half"）
- 2026-08-04｜Gerardo Hernandez｜margin：CFO 在問答中稱 Q3 量下降時服務毛利率無法維持 Q2 水準（原話："goes down, there is no way we can achieve those levels."）
- 2026-08-04｜Gerardo Hernandez｜margin：PAD 初期合併將稀釋毛利率與營業利益率，自第三季起（原話："gross margin and operating margin beginning in the third"）
- 2026-08-04｜Gerardo Hernandez｜margin：新計畫（OCS Kidney、次世代 OCS、ENHANCE／DENOVO）占調整後營業費用年增額約一半、約 1400 萬美元（原話："clinical programs accounted for approximately half of the"）
- 2026-08-04｜Gerardo Hernandez｜guidance：下半年既有業務的調整後營業費用預期與上半年相近，R&D 維持高檔（原話："with the first half, with R&D remaining elevated and SG&A"）
- 2026-08-04｜Waleed Hassanein｜capital_allocation：CEO 重申資本配置優先序：長期營收成長優先於短期營運槓桿（原話："durable top line growth ahead of near-term operating"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 表示營業利益率會隨投資節奏逐季波動（原話："margin will vary quarter-to-quarter with the pace of the"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 承諾每季回報各成長計畫進度（原話："are equally committed to delivering a strong operating"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 預期 CHOPS 納入 ENHANCE 的 IDE 補充於 Q3 末或 Q4 初核准（原話："submitted and is currently under FDA review. We expect it"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 設定 OCS Kidney 首次臨床使用時間為 2027 下半年（原話："targeting first clinical experience later in 2027"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 說 CHOPS 的 510(k) 現實時程為 2027 上半年（原話："I think realistically speaking, this is H1 2027 horizon for"）
- 2026-08-04｜Waleed Hassanein｜product：CEO 稱 ENHANCE Part B 與 DENOVO 啟動緩慢，目前僅少量病例（原話："We've done a handful of cases in each, nothing really to"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 以收案起算 12–18 個月作為試驗完成的關注基準（原話："And again, we're keeping our focus around 12 to 18 months"）
- 2026-08-04｜Waleed Hassanein｜product：CEO 預期心臟業務於 Q4 起隨 ENHANCE Part B 解鎖而加速（原話："And we expect heart to continue to accelerate in the fourth"）
- 2026-08-04｜Waleed Hassanein｜product：自 7/1 新增捐贈者與受贈者臨床篩選協調服務，已簽一家波士頓大型醫療體系做試點（原話："We signed up a major health care system in Boston."）
- 2026-08-04｜Waleed Hassanein｜customer：CEO 描述 Q3 開局強勁但保留，稱 7 月為史上最高航空月（原話："July was the highest aviation month for the business."）
- 2026-08-04｜Waleed Hassanein｜risk：CEO 對 Q3 維持謹慎樂觀，指出 8 月季節性疲弱（原話："So we are cautiously optimistic about"）
- 2026-08-04｜Waleed Hassanein｜competition：CEO 稱服務營收成長主要來自物流市占提升，並稱競爭對手失去大客戶轉到 TMDX（原話："And other vendors reported earlier today that they lost a"）
- 2026-08-04｜Waleed Hassanein｜margin：CEO 稱飛機雙班制改善了利潤率並帶來營運槓桿（原話："The double-shifting gave us significant operating leverage"）
- 2026-08-04｜Waleed Hassanein｜product：物流團隊 Q2 涵蓋需空運 NOP 任務約 86%，Q1 為 82%（原話："On average, we covered approximately 86% of NOP mission"）
- 2026-08-04｜Waleed Hassanein｜customer：CEO 先稱無乾跑增加，後答覆服務營收與產品營收差距可能來自乾跑（原話："potentially dry runs because our team gets deployed and we"）
- 2026-08-04｜Waleed Hassanein｜product：管理層將預期的長期目標寫為 2032 年約 30,000 例移植、年營收逾 20 億美元（原話："support approximately 30,000 transplants by 2032, driving"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 說明 2028 年 10,000 例目標以現有心肝肺平台計算，不含 CHOPS、腎臟或 ENHANCE Part B（原話："The 10,000 transplants is on the current platform, heart"）
- 2026-08-04｜Waleed Hassanein｜customer：CEO 在準備稿稱義大利已取得全國性補償（原話："where we have secured national reimbursement for machine"）
- 2026-08-04｜Waleed Hassanein｜customer：問答中 CEO 更正：只在義大利取得預算，並非全歐補償（原話："I said we secured a budget in Italy,"）
- 2026-08-04｜Waleed Hassanein｜risk：德國目前無補償且無 DCD 捐贈，CEO 不視為近期成長催化（原話："it's a complex market, and we are actively engaged there"）
- 2026-08-04｜Waleed Hassanein｜capital_allocation：CEO 稱 PAD 投資與 Summit 不同，需求證明前資本投入不會積極（原話："we are not going to be as bullish in capital deployment"）
- 2026-08-04｜Gerardo Hernandez｜guidance：CFO 未提供 PAD 的任何數字，預計 Q3 提供該年剩餘期間指引（原話："Not yet. I think, as we mentioned, we are not prepared just"）
- 2026-08-04｜Waleed Hassanein｜risk：CEO 表示成長計畫不含成為 OPO，因為該決定為二元結果（原話："everything we discussed today from a growth opportunities"）
- 2026-08-04｜Waleed Hassanein｜risk：CEO 稱 CMS 的 OPO 決定可能延後，且無新進展（原話："CMS may delay the decision point."）
- 2026-08-04｜Gerardo Hernandez｜guidance：CFO 對 2027 營業利益率不給方向，表示 Q4 提供 2027 指引（原話："certainly, in Q4, we will have a better view and"）
- 2026-08-04｜Gerardo Hernandez｜capital_allocation：CFO 稱臨床計畫延後使原 2026 的投資遞延至明年（原話："that those programs are delayed, that investment is going to"）

### 問答異常語氣（迴避／改口／保留）
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：JPMorgan 問服務營收強勁是否因乾跑增加及 Q3 動態｜答法：先否認曾討論乾跑增加並說到此為止；後續回答 David Rescott 時稱服務與產品差距可能是乾跑
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：Canaccord 問 FDA 對 ENHANCE／DENOVO IDE 的對話及延遲信心｜答法：拒絕評論 FDA 討論，稱 FDA 掌控時程，改談實際收案病例
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：William Blair 追問 ENHANCE／DENOVO 試驗完成度｜答法：口誤混用 Part A／Part B 後自行更正，未提供完成百分比，僅稱已做少量病例
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：William Blair 問義大利補償與歐洲成長是否優於預期｜答法：糾正提問者前提，稱只取得義大利預算而非全歐補償
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：Evercore 問 PAD 投資規模與對損益的近期影響｜答法：CFO 稱尚無法提供任何數字，延後至 Q3
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：Jefferies 問 OPO 壓力在 Q2 及下半年影響｜答法：稱無更新、不評論與自身無直接關係的動態，未量化影響
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：Stifel 追問 2027 營業利益率或 EPS 方向｜答法：CFO 未給數字或方向，只列三項驅動因素，稱 Q4 再給指引

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
{"date":"20260525","verdict":"B 衛星候選等修復 — thesis 完整但 Q1 EPS miss 引發 trap 🟡 + MA ❌→🟠 雙減半；等 Q2 26 EPS recovery + W250 站回 ~$80 連 4 週後可升 A","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Margin compression（Q1 26 OI margin 7.6% vs FY25 25%+）是 aviation fleet ramp 的 timing 問題不是結構性","columns":{"2Y 驗證":"Q4 26 OI margin 恢復至 ≥15%；FY26 全年 OI margin ≥ 15%","5Y 驗證":"FY28 OI margin ≥ 22%（回到 FY25 水平 + scale economy）","10Y 驗證":"FY30 OI margin ≥ 25%（aviation fleet 規模化後 leverage）","具體門檻":"Q3 26 OI margin ≥ 12% / Q4 ≥ 15% / FY28 ≥ 22%","來源":"Q1 26 earnings call mgmt commentary + Investor presentations","漂移觸發":"連 2 季 OI margin &lt; 10% → 削弱；連 4 季 &lt; 10% → 反轉"}},{"id":"H2","text":"US OCS liver 持續主驅動 + heart/lung 漸進 ramp + 歐洲 PAD Aviation 開出第二曲線","columns":{"2Y 驗證":"FY26 Revenue ≥ $727M（guide low）+ Liver YoY ≥ +25%","5Y 驗證":"FY30 Revenue ≥ $1.2B（含 EU contribution $150M+）","10Y 驗證":"FY35 Revenue ≥ $2B（全球三器官 + ADC ramp）","具體門檻":"FY26 ≥ $727M / FY27 ≥ $880M / FY28 ≥ $1.05B","來源":"FY26 公司 guide + sell-side consensus","漂移觸發":"連 2 季 Liver YoY &lt; +15% → 削弱；FY26 全年 &lt; $700M → 反轉"}},{"id":"H3","text":"OCS NMP 在 US 維持 first-and-only FDA 地位 — XVIVO/HOPE 不進入 US heart/liver 5 年內","columns":{"2Y 驗證":"FDA 觀察 — XVIVO 仍在 EU 階段 + HOPE 仍 limited use；OCS 在 NOP 服務內持續","5Y 驗證":"5 年後可能有 XVIVO 競爭但 OCS 已有 logistics moat（22 架 fleet）保護","10Y 驗證":"10 年後 NMP 平台可能多選但 OCS 仍佔 leadership 因 first-mover","具體門檻":"5 年內無 XVIVO US FDA approval for heart/liver","來源":"FDA 公告 / 競品 IPO/M&A 訊號","漂移觸發":"XVIVO 取得 US Heart/Liver FDA approval → 削弱；NRP guideline 推 OCS 取代 → 反轉 H3"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟠","trap":"🟡","moat_trend":"widening","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":68.94,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TMDX_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
