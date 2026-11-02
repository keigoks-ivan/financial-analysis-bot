你是 stock-analyst **v20 判斷 agent**，標的 COIN（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"COIN","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COIN_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COIN_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenue_gaap","label":"Total revenue (GAAP)","value":1215.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（YoY -35%，QoQ -0.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）"},"note":"無共識數據（未查）"},{"id":"f_kpi1_net_revenue","label":"Net revenue","value":1160.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（YoY -34%，QoQ +1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）"},"note":"無共識數據（未查）"},{"id":"f_kpi2_gaap_operating_income","label":"GAAP operating income","value":61.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）"},"note":"無共識數據（未查）"},{"id":"f_kpi3_gaap_operating_margin","label":"GAAP operating margin","value":5.1,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%（對 total revenue 61.7/1215.6）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）"},"note":"無共識數據（未查）"},{"id":"f_kpi4_net_income_gaap","label":"Net income (GAAP)","value":718.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（diluted EPS 2.51；含約715M 持有加密資產評價利益，該數字來自第三方未驗證）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）"},"note":"無共識數據（未查）"},{"id":"f_kpi5_adjusted_ebitda","label":"Adjusted EBITDA","value":332.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）"},"note":"無共識數據（未查）"},{"id":"f_kpi6_stock_based_compensation","label":"Stock-based compensation","value":233.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（占 GAAP 營業利益約 378%；占營收 19.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）"},"note":"無共識數據（未查）"},{"id":"f_kpi7_subscription_services_re","label":"Subscription & services revenue","value":570.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（QoQ +3%，YoY -20%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）"},"note":"無共識數據（未查）"},{"id":"f_kpi8_transaction_revenue","label":"Transaction revenue","value":590.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（QoQ -1%，YoY -44%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）"},"note":"無共識數據（未查）"},{"id":"f_kpi9_assets_on_platform","label":"Assets on platform","value":377,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD B（QoQ +53%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）"},"note":"無共識數據（未查）"},{"id":"f_kpi10_guidance_q4_2026","label":"Guidance Q4 2026","value":"550-630","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"subscription & services rev 550–630M；Adjusted Expenses 1,007–1,157M；SBC 約240M；Q4 transaction rev QTD至10-25約165M（公司提醒勿外推）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）"},"note":"無共識數據（未查）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_coin_gross_margin_pct","label":"COIN 毛利率","value":71.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_coin_operating_margin_pct","label":"COIN 營業利益率","value":5.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_coin_fcf_margin_pct","label":"COIN FCF 利潤率","value":68.4,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hood_gross_margin_pct","label":"HOOD 毛利率","value":81.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hood_operating_margin_pct","label":"HOOD 營業利益率","value":45.65,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hood_fcf_margin_pct","label":"HOOD FCF 利潤率","value":58.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ibkr_gross_margin_pct","label":"IBKR 毛利率","value":89.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBKR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ibkr_operating_margin_pct","label":"IBKR 營業利益率","value":86.25,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBKR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ibkr_fcf_margin_pct","label":"IBKR FCF 利潤率","value":135.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBKR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_schw_fcf_margin_pct","label":"SCHW FCF 利潤率","value":52.27,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SCHW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cme_gross_margin_pct","label":"CME 毛利率","value":86.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CME.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cme_operating_margin_pct","label":"CME 營業利益率","value":65.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CME.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cme_fcf_margin_pct","label":"CME FCF 利潤率","value":62.15,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CME.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":140.39,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-30.78,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":30.69,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（-1.69 → -1.69）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.02 → 3.02）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.83 → 4.83）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":-1.69,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.02,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":4.83,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":238.0,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS -0.5 → -1.69（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.83,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝43.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":43.9,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.47,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝45.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":45.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":128.79,"period":"2026-07-16","unit":"x","basis":"分母＝FY1 EPS 1.22，分子＝快照價 157.12","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-07-16"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-1935.19,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 6885.69、現金 8820.88（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":264.76,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":35227.0,"period":"2026-11-03","unit":"USD m","basis":"市值 37162.19 ＋ 淨負債 -1935.19","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":5235.02,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（32 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":6654.33,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（32 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":6.73,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 140.14 / W52 190.25 / W104 237.62 / W250 170.29 / W250 13週斜率 -0.67%"},{"id":"f_ma_w52","label":"52 週均線","value":190.25,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":237.62,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":170.29,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-0.67,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K FY2025 列出競爭類別含傳統券商/fintech、加密原生、機構點狀方案、DEX、非USDC穩定幣；因新增股票與預測市場，競爭集合擴大，並預期美國監管明朗後來自美國公司的競爭增加。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm","excerpt":"With the expansion in our product offerings in 2025 to include stocks, prediction markets and more, our competitive set in this category has broadened","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：DEX 交易量多次媲美自家平台，預期競爭加劇。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm","excerpt":"We have seen increased interest in certain decentralized platforms with transaction volumes rivaling our own platform on multiple occasions, and expect interest in decentralized and noncustodial platforms to grow further as the industry develops.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"TokenInsight資料：Binance Q2 2026總市佔由32.77%升至35.34%，為最大增幅。","source":"Landbase blog","url":"https://www.landbase.com/blog/fastest-growing-crypto-exchange-companies-startups","excerpt":"Q2 2026 market share: 35.34%, up 2.57 percentage points Market-Share and Multi-Asset Growth Binance processed approximately $5.85 trillion in Q2 2026 trading volume. Its total market share increased from 32.77% to 35.34%, the largest quarterly gain among the exchanges tracked by TokenInsight.","as_of":"2024-05-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Bernstein估計Coinbase掌握美國市場66%；Morgan Stanley稱Robinhood可能搶份額。","source":"DL News","url":"https://www.dlnews.com/articles/markets/coinbase-stock-seen-surging-on-these-drivers-bernstein-says","excerpt":"player and controls 66% of the US market, according to Bernstein. The Securities and Exchange Commission has also agreed in principle to drop its case against Coinbase. Growing competition To be sure, Coinbase is not the only one to benefit from Trump tailwinds. The SEC has also dropped or paused cases against Coinbase rivals like Kraken, Gemini and Robinhood.","as_of":"2025-03-18","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Coinbase Q2 2026 8-K: crypto trading volume market share 10.3% (record), up from 9.1% in Q1; average USDC held in products $20B, >30% of USDC in circulation; Subscription & Services 48% of net revenue; consumer trading volume fell to $25.8B from $41.5B y/y (cyclical weakness in spot).","source":"Coinbase Form 8-K Q2 2026 earnings deck (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000087/q226earningsdeck_sec.htm","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["moat_trend","thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"William Blair cut estimates; expects Coinbase total trading volume to fall ~44% in 2026 to $669B, then rebound >32% in 2027; earnings trough 2H26 and recover 2027.","source":"Crypto Briefing: William Blair sees Coinbase and Circle benefiting from crypto recovery despite slashing estimates","url":"https://cryptobriefing.com/william-blair-coinbase-circle-crypto-recovery/","excerpt":"The firm projects total trading volume on the platform will fall roughly 44% in 2026 to $669 billion, before bouncing back over 32% in 2027. Advertisement","as_of":"2026-09-22","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Analysts cut Coinbase 2026/2027 estimates; Barclays Underweight expects forecasts to fall unless trading rebounds; Moderate Buy consensus.","source":"BrokerChooser: Analysts See Opportunity in Coinbase's Slide, Despite Slashed Forecasts","url":"https://brokerchooser.com/news/analysts-see-opportunity-in-coinbases-slide-despite-slashed-forecasts--b304751c","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Cantor argues prediction markets could drive up to 30% of COIN gross profit by 2028.","source":"Coinbase analyst coverage (prediction market expansion)","url":"https://durslt.du.ac.in/first-dry/Coinbase-Global-Inc-COIN-Prediction-Market-Expansion-and-Product-Diversification-Drive-Bullish-Analyst-Sentiment-11-2638","excerpt":null,"as_of":"2026-04-29","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露：Coinbase 已收到多個州機關與檢察長、各監管機構的調查傳票與要求函，涉及上架流程、資產分類、質押計畫、穩定幣與收益產品；公司表示將配合。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm","excerpt":"we have received investigative subpoenas and demand letters from various regulators for documents and information, including about certain customer programs, operations, and existing and intended future products, including our processes for listing assets, the classification of certain listed assets, our staking programs, and our stablecoin and yield-generating products.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"2026-04 Bloomberg 報導：CFTC 表示因 Coinbase 與 Gemini 相關行動而起訴紐約州（州與聯邦監管權限之爭）。細節未讀到。","source":"Newsquawk 引述 Bloomberg","url":"https://newsquawk.com/headlines/cftc-says-it-has-sued-new-york-in-response-to-coinbase-coin-and-gemini-actions-bloomberg-reports-24-04-2026","excerpt":"CFTC says it has sued New York in response to Coinbase (COIN) and Gemini actions, Bloomberg reports.","as_of":"2026-04-24","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋未見 2026 年 DOJ／FTC 對 Coinbase 的反壟斷調查；僅見私人反壟斷訴訟（BiT Global 10 億美元案，2025-05 法官傾向駁回）。","source":"Law360, Coinbase May Avoid BiT Global's $1B Antitrust Suit, For Now","url":"https://www.law360.com/articles/2340882","excerpt":"A California federal judge indicated Thursday she'll likely toss a $1 billion antitrust case against Coinbase claiming the cryptocurrency exchange delisted BiT Global after launching a competing","as_of":"2025-05-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K FY2025 載明 Coinbase 須遵守美國商務部 BIS 等管轄的出口管制法規與 OFAC 制裁規定；屬合規義務，未見關稅或實體清單對其產品或供應鏈的具體衝擊描述。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm","excerpt":"We are also required to comply with export control laws and regulations administered by the United States and other applicable jurisdictions, including those administered by the U.S. Department of Commerce’s Bureau of Industry and Security.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K FY2025 風險因子指出，隨國際擴張，公司可能面臨涉及制裁、出口管制與反洗錢的調查或執法。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm","excerpt":"we may be subject to inquiries, investigations, and enforcement actions by U.S. and non-U.S. regulators and governmental authorities, including those related to sanctions, export control, and anti-money laundering.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026-05-07 AWS US-EAST-1 資料中心過熱導致 Coinbase 交易中斷逾兩小時；主交易系統為降延遲跑在單一可用區，備援未如預期運作；為約七個月內第二次 AWS 相關中斷（前次 2025-10）","source":"paymentexpert.com / thenextweb.com 報導（搜尋摘要）","url":"https://paymentexpert.com/2026/05/11/coinbase-aws-outage-infrastructure/","excerpt":null,"as_of":"2026-05-11","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露依賴第三方支付、金融機構及雲端運算與資料中心服務，且不直接營運這些供應商設施，面臨停電、人為錯誤、天災等中斷風險","source":"Coinbase FY2025 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Coinbase 2026-05 AWS 中斷，主系統單一可用區","source":"The Next Web","url":"https://thenextweb.com/news/coinbase-aws-outage-layoffs-worst-week","excerpt":"Coinbase said the issue originated in a single AWS availability zone, use1-az4, in the US-EAST-1 region, but that failures spread across multiple zones, overwhelming the resilience mechanisms designed to handle a single-zone loss.","as_of":"2026-05-08","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 交易營收 $590.2M，年減 44%，機構現貨成交量年減 53%","source":"Coinbase 10-Q (period 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000122/coin-20260930.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 訂閱與服務營收 $570.2M，年減 20%、季增 3%，占淨營收 49%；Q4 指引 $550–630M","source":"Coinbase 10-Q / Q3 earnings deck; Finviz","url":"https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Coinbase 自報加密貨幣成交量市占 2026 Q2 達紀錄 10.3%（Q1 9.1%）；第三方 CryptoRank 4 月 CEX 現貨市占 5.3%（第四），CEX 現貨量創 25 個月低 $951.8B","source":"Coinbase Q2 2026 earnings deck; CryptoRank April 2026 CEX spot volume recap","url":"https://cryptorank.io/insights/reports/april-2026-cex-spot-volume-recap","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"William Blair 預估 Coinbase 平台 2026 成交量年減約 44% 至 $669B，2027 反彈逾 32%","source":"CryptoBriefing: William Blair sees Coinbase and Circle benefiting from crypto recovery","url":"https://cryptobriefing.com/william-blair-coinbase-circle-crypto-recovery/","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Coinbase 10-K FY2025 risk factors say new services/technologies (decentralized networks, generative AI) may be superior to or render obsolete its current products and may fundamentally alter use of its services in unpredictable ways.","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm","excerpt":"We expect new services and technologies to continue to emerge and evolve, which may be superior to, or render obsolete, the products and services that we currently provide. For example, decentralized networks and other disruptive technologies such as generative AI may fundamentally alter the use of our products or services in unpredictable ways.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Artemis data cited in early Feb 2026: on-chain perp exchange Hyperliquid processed ~$2.6T notional volume in 2025 vs ~$1.4T for Coinbase.","source":"Whale Alert, Hyperliquid processes $2.6T in 2025 notional volume—surpasses Coinbase","url":"https://whale-alert.io/stories/9b87014f208437/Hyperliquid-processes-26T-in-2025-notional-volumesurpasses-Coinbase-as-onchain-perpetuals-drive-user-and-TVL-growth","excerpt":"According to Artemis data released in early February 2026, Hyperliquid processed approximately $2.6 trillion in notional trading volume during 2025. Over the same period, Coinbase recorded about $1.4 trillion.","as_of":"2026-02-10","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Coinbase 10-K FY2025：Coinbase One 訂閱制 2025 新增 Basic 檔，共三個會員層級，並推出 Coinbase One 信用卡；訂閱產生經常性收入並深化用戶參與。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm","excerpt":"In 2025, we launched an additional subscription tier, Coinbase One Basic, offering consumers essential benefits for a lower subscription fee. There are now three membership tiers under Coinbase One: Basic, Preferred, and Premium.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"搜尋摘要：Coinbase 2026 策略為「Everything Exchange」，Q1 2026 訂閱與服務占淨收入 44%，納入預測市場、零售衍生品、代幣化股票與商品永續合約（二手彙整，未核一手）。","source":"WebSearch 彙整（Coinbase Q4 25 Earnings Call 等）","url":"https://www.webull.ca/news-detail/14134214718931968","excerpt":null,"as_of":"2026-05-13","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Coinbase 2026 roadmap：成為 everything exchange（股票、預測市場、商品）、擴大 USDC 支付、建 Base 超級應用","source":"BlockEden coinbase everything exchange 2026 roadmap","url":"https://blockeden.xyz/blog/2026/03/11/coinbase-everything-exchange-2026-roadmap-equities-base-super-app/","excerpt":"Coinbase's 'Everything Exchange' Gambit: From Crypto Platform to Global Financial Super-App March 11, 2026 · 8 min read Dora Noda Software Engineer Your browser does not support the audio element.","as_of":"2026-03-11","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"TIKR：共識目標價約 $212，較一年前約 $380 下修，8 月低點 $195","source":"TIKR Coinbase Stock at $158 Against a $309 Target","url":"https://www.tikr.com/blog/coinbase-stock-at-158-against-a-309-target-the-ebitda-recovery-path-and-what-has-to-hold","excerpt":null,"as_of":"2026-10-08","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Citizens JMP 目標價由 $325 降至 $280，維持 Market Outperform","source":"TIKR Coinbase Has Lost 56% in a Year","url":"https://www.tikr.com/blog/coinbase-has-lost-56-in-a-year-citizens-jmp-sees-63-upside","excerpt":"9, 2026, Citizens JMP cut its price target to $280 from $325 while keeping its Market Outperform rating, a call that implies 63% upside. Analysts’ consensus target has fallen from $380 to $212 over the same year, even as Buy ratings rose from 12 to 19.","as_of":"2026-10-09","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Zacks：Q2 後 FY2026 共識 EPS 大幅下修至約 -$0.05","source":"Nasdaq/Zacks Bear of the Day: Coinbase Global","url":"https://www.nasdaq.com/articles/bear-day-coinbase-global-coin","excerpt":null,"as_of":"2026-08-15","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 訂閱與服務營收指引 $500M–$580M","source":"247wallst Coinbase Q3 Earnings Preview","url":"https://247wallst.com/investing/2026/10/25/coinbase-q3-earnings-preview-can-cryptos-rebound-save-coin-from-a-fourth-consecutive-miss-oct-29/","excerpt":"Subscription and services revenue is the buffer. Guidance calls for $500M-$580M, compared with $555M last quarter.","as_of":"2026-10-25","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2026-05-05 8-K Item 2.05：宣布重組，裁員約 700 人（約 14%），預估重組費用 $50–60 百萬，多數於 2026Q2 認列。","source":"SEC EDGAR 8-K Item 2.05 (2026-05-05)","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978826000049/coin-20260505.htm","excerpt":"The Plan involves a reduction of the Company’s workforce by approximately 700 employees, representing approximately 14% of the Company’s global workforce as of May 1, 2026.","as_of":"2026-05-05","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2025-12-15 公司註冊地由德拉瓦遷至德州（8-K Item 8.01）。","source":"SEC EDGAR 8-K Item 8.01 (2025-12-16)","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978825000247/coin-20251215.htm","excerpt":"the reincorporation of the Company from the State of Delaware to the State of Texas (the “Reincorporation”) became effective on December 15, 2025, at 5:00 p.m. Eastern Time","as_of":"2025-12-16","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K：公司收到多個州機關與監管機關的調查傳票與要求函，涉及上架流程、質押、穩定幣與收益產品；管理層認為無其他重大不利訴訟。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm","excerpt":"we have received investigative subpoenas and demand letters from various regulators for documents and information, including about certain customer programs, operations, and existing and intended future products, including our processes for listing assets, the classification of certain listed assets, our staking programs, and our stablecoin and yield-generating products.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#0","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"COIN 10-Q（2026-06-30）揭露現金多置於高信用品質金融機構、未曾發生損失；搜尋結果未見 NPL/NCO/撥備數字","source":"Coinbase 10-Q for period ended 2026-06-30 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000088/coin-20260630.htm","excerpt":"The Company has not experienced losses on these accounts.","as_of":"2026-08-01","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#1","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"摩根士丹利 2026 信用循環展望：2026 信用循環先熱後退（總體層級，非 COIN 或交易所產業專屬）","source":"Morgan Stanley Thoughts on the Market, Andrew Sheets, credit cycle 2026","url":"https://www.morganstanley.com/insights/podcasts/thoughts-on-the-market/credit-cycle-2026-andrew-sheets","excerpt":null,"as_of":"2025-12-15","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"financial_regulatory_capital_rules#0","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"COIN 2026Q3 10-Q: 子公司符合資本要求；CB Inc. 淨資本$2,928M vs 要求$1,185M（盈餘$1,743M）；CB Inc. 要求自6月底$988M升至$1,185M；NYDFS 協議要求最低淨資本。","source":"Coinbase Form 10-Q (quarter ended 2026-09-30), SEC","url":"https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000122/coin-20260930.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_regulatory_capital_rules#1","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"2026年3月世界交易所聯合會(WFE)呼籲巴塞爾委員會修訂銀行加密資產曝險審慎標準；未查到已定案的2026修訂或針對交易所的規則變動。","source":"FOW: WFE urges Basel rethink on crypto capital rules","url":"https://www.fow.com/insights/wfe-urges-basel-rethink-on-crypto-capital-rules","excerpt":null,"as_of":"2026-03-14","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"程式統計：近12個月 12 份 8-K 中，重大項目（含 2.01 併購完成）者僅 2 份（2.05、8.01），無 1.01／2.01 併購類 8-K。搜尋摘要提及 2025-11 Vector、2025-12 The Clearing Company 小型收購，未取得可逐字原文。","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001679788&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 12 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"FY2025 10-K 披露 Underwood 等集體訴訟等重大訴訟（Note 21）；公司稱曾、現正面臨集體訴訟，結果無法確定。另搜尋顯示 D.N.J. 證券集體訴訟（2021 直接上市相關，AP7 為首席原告）法院駁回第三次駁回動議，裁定日期未見。","source":"SEC EDGAR 10-K FY2025 Item 1A / Note 21；Kessler Topaz 案件頁","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm","excerpt":"We have been, currently are, and may from time to time become subject to claims, arbitrations, individual and class action lawsuits with respect to a variety of matters, including employment, consumer protection, intellectual property, privacy, information security, data protection, advertising, and securities.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"-","claim":"FY2025 10-K 披露收到多個州與聯邦監管機關調查傳票；未見重編財報（8-K 清單無 Item 4.02）。2025-05 另有 SEC 調查過往用戶數揭露（早於12個月窗口）。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm","excerpt":"We intend to cooperate fully with such investigations.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"COIN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.01,"operating_margin_pct":5.68,"fcf_margin_pct":68.4,"rd_intensity_pct":34.52},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"HOOD","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":81.44,"operating_margin_pct":45.65,"fcf_margin_pct":58.44,"rd_intensity_pct":19.34},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"IBKR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":89.97,"operating_margin_pct":86.25,"fcf_margin_pct":135.66,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBKR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SCHW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":52.27,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SCHW","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CME","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":86.63,"operating_margin_pct":65.66,"fcf_margin_pct":62.15,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CME","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"COIN"},"financial_history":{"ticker":"COIN","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":3194208000.0,"revenue_yoy_pct":null,"gross_margin_pct":80.28,"operating_margin_pct":-60.96,"net_income":-2624949000.0,"diluted_eps":-11.83,"free_cash_flow":-1649390000.0,"fcf_margin_pct":-51.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":3108383000.0,"revenue_yoy_pct":-2.69,"gross_margin_pct":63.47,"operating_margin_pct":-1.73,"net_income":94871000.0,"diluted_eps":0.37,"free_cash_flow":610174000.0,"fcf_margin_pct":19.63,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":6564028000.0,"revenue_yoy_pct":111.17,"gross_margin_pct":74.78,"operating_margin_pct":34.06,"net_income":2579066000.0,"diluted_eps":9.48,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":7181325000.0,"revenue_yoy_pct":9.4,"gross_margin_pct":74.64,"operating_margin_pct":20.28,"net_income":1260327000.0,"diluted_eps":4.45,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/COIN/COIN_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Coinbase Global, Inc.** | Earnings Calls | 2026-10-29

**Shan Aggarwal** (Executives):
Our discussion today includes forward-looking statements, which may vary materially from our actual results. Please refer to our SEC filings and earnings presentation for information concerning risks, uncertainties and other factors that could cause these results to differ. In addition, our discussion today includes certain non-GAAP financial measures. Reconciliations to the most directly comparable GAAP financial measures are provided in the earnings presentation on our Investor Relations website.

**Alesia Haas** (Executives):
Hi, everyone. Thanks for joining us live on X. I'm Alesia Haas, CFO of Coinbase, and I'm here with our Co-Founder and CEO, Brian Armstrong; and a few independent and institutional research analysts. If you haven't already, please head over to our IR website to watch the videos we posted of Brian and I discussing our quarterly results. But in this session, right now, we are excited to directly connect with you, our customers, our community, our shareholders and we want to talk about our quarter and answer questions. So just as a friendly reminder, we're not going to answer any questions on when, X,Y,Z token. We have a robust asset listing process that we follow. And we're not going to talk about any customer support cases. But besides from those simple ground rules, it is open question time.
So first up, I'd like to introduce Andrew.

**Andrew Jeffrey** (Analysts):
Thank you very much. Alesia and Brian, it's a pleasure to be here. Appreciate the opportunity. I thought maybe I'd start with a big picture macro question. And I think you touched on it in the quarterly results. It does feel like crypto sentiment has shifted and we've seen Bitcoin rally a lot off of its lows. But it still trades like a risk asset, even after market today with tech trading off. Do you feel like the case for Bitcoin ownership broadly has evolved? It does seem to me like that Base is certainly making the case that Bitcoin can be a global -- can really be global digital collateral in DeFi marketplaces. But can you maybe just comment on how you think sort of the raison d'être may have shifted?

**Alesia Haas** (Executives):
And before you answer, Brian, I just wanted to apologize. Andrew, I should have given you a more robust introduction. With us folks is Andrew Jeffrey, who is an institutional research analyst with William Blair. And with that, Brian, over to you. What is the BTC value proposition today in 2026?

**Brian Armstrong** (Executives):
Yes. So I think it's evolving. You're right. It's obviously still a store of value. We're super bullish on Bitcoin. I think we just purchased our 18,000th Bitcoin actually on Coinbase balance sheet. Alesia has a Bitcoin pillow.

**Alesia Haas** (Executives):
Happy birthday.

**Brian Armstrong** (Executives):
Yes, it's Bitcoin's birthday coming up too. And then I think what you're getting at is correct, which is now that you can use Bitcoin as collateral, it actually improves liquidity when -- for trading, right? So that's improving DEX trading, for instance, with Bitcoin. A lot of our customers who were early in Bitcoin, they don't want to ever sell their Bitcoin but they do want to use it as collateral. And Base for instance, has done really well recently by growing its financing product. So you can use that Bitcoin as collateral, get financing, go and do more trading. It's pretty synergistic. And I think that's definitely a big trend that's happening right now. So -- and then just broadly, I'd say like in this cycle that we're in, I mean, it's always difficult to call these things exactly but we are seeing volumes rebounding and more institutions coming and onboarding. And so yes, I think it's a exciting road ahead for Bitcoin.

**Alesia Haas** (Executives):
Yes. I would just comment that we saw significant ETF inflows into Bitcoin specifically this quarter as people recognized that the price has stabilized. And one, Bitcoin is still a critical asset to us but we are Bitcoin and, people can now trade a lot of things and we've seen volatility come down in Bitcoin with the institutional adoption of this as an asset class. And I think that, that is providing it to be an important diversification in a lot of people's investment portfolios.

**Andrew Jeffrey** (Analysts):
Thank you. Mine included. I guess I'm not vain enough to have introduced myself. I probably should promote myself better. I actually think the comment on diversification and thinking about your business, in particular, is really a good segue. Terrific sequential growth in prediction markets revenue. One of the questions we get a lot is sort of trends in consumer transaction revenue and take rate. I'm sure you hear this a lot, too. Could you help us parse a little bit how much -- it certainly looks like Prediction Markets cushioned consumer transaction revenue in the quarter. But can you help us sort of unpack that a little bit and tell us maybe how we can think about that going forward?

**Alesia Haas** (Executives):
Absolutely. So prediction markets is one of our fastest-growing new revenue products. We just launched it in February this year. And during the third quarter, it crossed $200 million of annualized run rate revenue. And what's great about that is this is a market where overall spot crypto trading was actually down. We saw overall crypto spot trading volume down 10% quarter-over-quarter. And so the growth in prediction markets offset the decline in overall spot trading. And we delivered flat revenue quarter-over-quarter. The mix shifted considerably. And when we look at the mix of our overall revenue, it's really interesting to look at this quarter. Predictions plus derivatives, so those 2 combined were about 25% of our total transaction revenue.
And if I look at then our total revenue, subscription services was roughly 49% of total net revenues. So we are seeing the investments that we've made over the past few years to really diversify our revenue really come to our benefit as I love what Brian said, there's always a market somewhere. And so people are shifting their trading behavior to the asset that's most interesting and most excited in the markets that they want to trade in. And what we saw right now in this quarter, a lot of that was around predictions. But I also want to share with you, this isn't cannibalizing our spot trading. What we're seeing is, this is all incremental. And when we look at our trading profile, people are still continuing to trade, spot just maybe at a lesser level than they did in past quarters and they're putting incremental dollars to trade in prediction markets and derivatives. So really, these are additive to our product offering right now.

**Andrew Jeffrey** (Analysts):
Which really goes a long way, I think, toward debunking the idea that Bitcoin is the tail that wags the dog, although I think that still seems to inform stock prices at least in the short term. There's a ton to talk about. I did want to spend a little time on stablecoins moving away from transaction. Could you just elaborate for us a bit on your Circle relationship? To me, it seems very much like a coopetition situation. Both companies, whereas USDC is still primary to your stablecoin efforts, it does seem like both companies are building similar stablecoin movement infrastructure. Can you talk about perhaps where your efforts overlap with Circle's and where your efforts are distinct?

**Alesia Haas** (Executives):
Brian, do you want me to start here and then you can add on?

**Brian Armstrong** (Executives):
Yes, go for it.

**Alesia Haas** (Executives):
All right. Well, we are proud to be a co-founder of USDC and we are very committed to growing USDC. And we also want to support other high-quality regulated stablecoins. And so you saw that we also partnered with, as an example, with OUSD. We also have PYUSD on our platform. We will be supporting our customers in whatever asset they want to trade and whatever asset they want to transact with in crypto. So we think about ourselves asset agnostic that way. But because of our commercial relationship with Circle, where we have a strong economic interest to grow USDC, we are active in supporting this overall USDC ecosystem. Coinbase focuses on distribution, the customer relationships, the infrastructure and really deeply integrating USDC and opportunities to use stablecoins in transaction flows within our products.
This means that we are using this collateral with our derivatives exchange as an example. This means that we are looking to put -- we put USDC on Base to really augment our payments with our Coinbase Developer  product. And as a result, we've seen all-time highs in USDC use on our platform. So we capture about 50% of the overall economics. We hold about 30% of total USDC in circulation as assets on our platform. And we've seen the total assets on our platform grow for 5 sequential quarters, or it's just been growing more than that now. It's just been significantly growing on our platform for now many, many quarters. Where we compete is we're both building stablecoin payment infrastructure. And so we will compete in some areas but we are both incentivized to grow total USDC market cap and deeply embedded in the overall network of stablecoin usage around the world.

**Brian Armstrong** (Executives):
Yes. I guess I'd just add that we really enjoy our partnership with Circle. There are many times where we work together on certain efforts. You're right that we are both building infrastructure. It's going to take a lot of work from lots of companies to go update the financial system. And so I think that, that's great what they're doing and we're going to keep doing our piece of it as well. And overall, what we want to see is just stablecoins be a larger and larger percentage of global GDP for payments in -- everywhere -- used in every country of the world. So we're going to keep working with them on that.

**Alesia Haas** (Executives):
All right. Let's go to our next guest. We have Jon Ma from Artemis with us. Jon, over to you. Ready for your questions too.

**Jonathan Ma** (Analysts):
Happy early 18th birthday for Bitcoin. That's very exciting.

**Alesia Haas** (Executives):
I think someone out there is going to have a Halloween Bitcoin costume. I'll start looking for that on social.

**Jonathan Ma** (Analysts):
Yes. That's my Halloween outfit. Thanks for the idea, Alesia. I'm really excited to talk about Coinbase agents and getting your thoughts. So one of our engineers, Crystal she built onbase.dev. She's one of -- a big Base developer. We recently integrated Coinbase MCP trading agents into Artemis. And she said, of all the brokerages she worked with, it was the easiest. And so my question is, what could go right for Coinbase agents because it's the only MCP that includes x402 in prediction markets, equities and crypto. Like what could go right from here?

**Brian Armstrong** (Executives):
Yes. Well, thanks for using our MCP. We launched this product called Coinbase for Agents a little while back. And it's basically an easy way to connect any third-party agent to your Coinbase account. And we really want to make Coinbase the most AI-enabled financial account out there for trading and payments and borrowing. So we've been putting a lot of work into that MCP API. And honestly, it's been really exciting. I mean the agentic trading volume is growing something like 20% week-over-week right now, which is just shocking. I mean these numbers...

**Jonathan Ma** (Analysts):
Wow.

**Alesia Haas** (Executives):
Early days. Early days. But like them, yes.

**Brian Armstrong** (Executives):
Yes, there's still -- the numbers in the grand scheme of things are still relatively small compared to our other trading volume. But to me, it's a clear indication of where things are going. And I'm just like -- I'm just incredibly excited about the TAM for what the agentic economy could be. I mean you asked what could go right. I think probably like you, we're seeing this trend and thinking, okay, there's going to be more and more agents in the economy getting work done on our behalf. They are going to have to pay for things and goods and services to get work done or go shopping for us. They're going to have to -- in a business context, they're going to have to pay for vendors and services to not get stuck at these paywalls, just like you would give an expense account to an employee or a budget to a certain team.
This is very clear to us that they're going to need their own financial infrastructure and they're going to do it for trading, too. It's not just payments. And so what does this mean? I mean they're going to need to have accounts with good controls and permissions to make sure you're managing their spending and all that. And I think that it's hard to imagine a world where there's not more AI agents than humans at some point in this economy. So the agentic economy is going to be massive. And I think it's just one of these opportunities where, frankly, we see the legacy players being a little bit hesitant about this and saying, I don't know, this is scary, any  -- what if these rogue agents do something unexpected.
We're not going to let any of these things touch our accounts. I kind of feel the opposite. It's an opportunity. If we can lean in and build this in a very safe and trusted way, which is what Coinbase is known for using these frontier technologies, AI and crypto, which by the way, they go really well together, that's just a huge opportunity for us to capture more and more market share as -- like as the most AI-enabled financial account. So we're all in on this. It's what I wake up thinking about a lot these days.

**Jonathan Ma** (Analysts):
Yes. Brian, it gets me really excited because right -- like right before the earnings call, I was using the Coinbase MCP to sell some Polkadot. I bought some ServiceNow stock. I sold down some USDC to buy another stock. And it was like the only product where everything is all in one place. And so something I'd be curious about is Coinbase is already #1 in crypto market share for spot in the U.S., how do we go from here to #1 across all assets, Everything Exchange, because this does feel very unique. Like maybe there's a world where every retail, every user just uses Coinbase for all their different assets because it's the only place where their agent can access all these different assets in one place.

**Brian Armstrong** (Executives):
Yes. I mean I think you're right. It gets to what Alesia was saying earlier about diversification. A lot of these new bets that we made as part of the Everything Exchange investment over the past year have really started to bear fruit now, prediction markets, derivatives. Because historically, we've been overweight on spot crypto trading, which was down quarter-over-quarter. I don't think that this is widely understood yet. And the facts on the ground are actually looking a lot better than it's showing up maybe in the overall numbers, which are more flattish. But yes, it makes sense to me that if you have an account where you can do all these things in one place, trading, payments, lending because many of these are synergistic, right? Like you might want to have a margin account to do more trading or you might -- as a business, you might want to do FX trading as you're receiving payments.
So we believe that all of these things are going to need to work in one account. We did this with crypto. We can now do it with AI. I think this could be a massive source of new demand for our products. So yes, that's definitely a very exciting moment. And I'll tell you one other fun anecdote, which is -- so in Coinbase for Agents, we -- initially, we were going around talking to customers and just say, hey, what would you like to see in it and building some of those features. One of the engineers on our team, they put an endpoint into the Coinbase MCP that is like a /feedback endpoint. And so now all day long, as agents are using it, the agents are actually sending us feedback. And I -- so we're like hundreds of messages are just coming into Slack every day that are like different things that they want to see. And a lot of those get turned into pull requests and now they're live back in production like a day later.
So it's starting to get to that kind of recursive self-improvement type feeling. And since that pattern was so successful, we're going to think about putting some of that for our internal APIs as well just so that -- because we're using lots of agents internally as well. So yes, every API needs to be agentified, so to speak.

**Jonathan Ma** (Analysts):
Yes, Brian, I think folks were wondering, I think Jesse mentioned that you and Jesse were like shipping like 44 PRs over a day and maybe you were responding to the agents that were giving feedback about the agent MCP.

**Brian Armstrong** (Executives):
That's been part of it. Yes. I mean I've definitely been getting excited to go back and write some code. I mean it's really the agents writing most of it. But starting my career as an engineer, it's been -- you get a little rusty in the code, the more CEO stuff you do. But yes, it's definitely a fun moment. I think we're living through this kind of golden age and AI is changing lots of things but it's now starting to really change financial services. And that's been the biggest opportunity for us. And the level of productivity, I think code quality can actually go up as the velocity goes up. We're seeing that as well on the cyber front and the amount of -- the number of bugs and incidences -- incidents and reliability can get better.
So it's massively up-leveling our internal systems and then we can go build this infrastructure and provide it for all of our customers. To me, this is the future of financial services. And then, yes, I mean, I still -- we sort of we want to bring frontier technologies like crypto and AI to financial services. And I think we're one of -- we're the best company in the world that's set to do that.

**Jonathan Ma** (Analysts):
Love that.

**Alesia Haas** (Executives):
All right. Well, thank you, Jon, for this question. And thank you for feedback on the products as well. We love it when people give us feedback.
So next up, we'd like to introduce Lorenzo Valente from Arc and hand it over to you to ask some questions, Lorenzo.

**Lorenzo Valente** (Analysts):
Excited to do this. Maybe I'll start with the -- just a question on security and custody in general. There's growing concern out there that AI could discover new algos that break cryptography and ECDSA in general. How does that change the security and custody setup? And are you accelerating the post-quantum road map? So just like a question in terms of custody and security in general and how you guys are thinking about that?

**Brian Armstrong** (Executives):
Yes, sure. Okay. So I think there's really 2 separate things to look at. One is the AI, the trends that we're seeing of them coming out with new math proofs and security things. Then there's the quantum question. So these are actually pretty different. I think that when it comes to ECDSA and this elliptic curve cryptography, I'm actually not too worried about AI creating a risk there. There's been something like a 40-year track record actually of people attempting new algorithms to try to make this easier to break and they've basically made 0 progress. And it's -- you have to -- it requires this brute forcing of 256-bit number. So it's not one of these problems that -- I don't think AI is going to be able to chip away at it.
Now, quantum is a different story. I think quantum, it requires a new type of computer to be built and actually to do it at scale, not just like a theoretical one with a couple of qubits. And so I think that's more of a matter of when, not if. Like I think eventually, a big enough quantum computer will get made that starts to make this stuff a real issue. So the quantum one, I think, is the more serious one to look at here. And to get ready for this, I mean, we're doing a handful of things. One is, we have begun the work to upgrade our custody to be post-quantum. So that's important. Now, of course, we also need the blockchains themselves to be upgraded and to be quantum resistant. And I know lots of the different blockchains are all working on this. Some of them have published their road map.
One thing we've been participating as best we can on the Bitcoin side, there's an advisory council for Bitcoin around post-quantum that had a really good meeting that we attended a few months ago at Stanford with -- Dan Boneh was leading that along with a number of other folks. And that was a really great conversation that just got a lot of the people together in the room. And I know that the community has put out some of these Bitcoin improvement proposals like BIP-360 and there's others. And so yes, I mean, my hope is that the Bitcoin community will essentially find a path over the coming couple of quarters to start to coalesce around some of these proposals that are out there. And that one, I think, it's not like -- it's not imminent. I don't think it's going to happen imminently but I do think we -- just -- it's always good to be proactive and start to get ahead of these things.

**Alesia Haas** (Executives):
I just wanted to add on and share that in 2022, we acquired a team of some of the foremost cryptography experts. And this is a space, both on the quantum and on the AI side that we are monitoring very carefully internally and being really vigilant in investing resources to harden both our own ecosystem as well as work in partnership with the community, as Brian shared.

**Lorenzo Valente** (Analysts):
Perfect. Shifting to the tokenized stocks on Base. I know it's still very early, obviously. Is the Base sequencer fee the main revenue driver going forward? Or are you looking at other monetization plans? And just to add to that, we're seeing just a lot of different equities tokenized by several exchanges. How do you see that fragmentation going forward? And how do you think about that?

**Alesia Haas** (Executives):
Great questions, Lorenzo. So yes, sequencer fees are the most direct monetization point for tokenized equities today. And our main opportunity then is the utility of the assets once they're tokenized. And as we kind of expand out and build this network and build liquidity, we can explore different ways to monetize. But network effect is key. Liquidity is key. And that is the answer to your question on we're seeing a lot of places tokenized equities. We see a lot of stablecoins. But what is hard -- it is easy actually to tokenize something. And I don't mean that the wrong way but the -- getting the tokenized asset is not the complicated part. Building depth of liquidity, building network effect, that is the hard part.
And we're really proud that we're one of the firms with partnership with Circle that has really built that with the USDC ecosystem as an example. And so we feel like we have the skills, we have the tools to build liquid deep markets around these tokenized equities and that is what we're doing. We've already seen $3 billion, for example, tokenized Coinbase in tokenized equity trading volume since launch of that product for our non-U.S. customers. We're just getting started here but the key is building network effect. And I do think that what we'll see then over time is things will coalesce and you'll see more and more market share gained by the best pricing and the best network effect and liquidity offered in these exchanges.

**Brian Armstrong** (Executives):
Yes. The only thing I'll add to that is that we took the time to really do this in a thoughtful way, which means that these tokenized equities that we put out there, they're real deal securities. You can get the upside from dividends. We're implementing voting rights, things like that. So there are other things out there in the market that are more like synthetics or derivatives that give you exposure to it but we thought it was important to do it in a way that it's a real security, it can be redeemed for the underlying asset, et cetera. And I think just as the largest custodian in crypto, the most trusted brand in crypto, this is actually something that we're uniquely good at and have a right to win. So yes, I'm excited about tokenized equities.

**Alesia Haas** (Executives):
All right. Thanks, Lorenzo. We're going to go to our last analyst today and I'd like to introduce Ansem, who is the host of Market Bubble, to ask us any questions.

**Zion Thomas** (Analysts):
Yes, so, this is cool. Actually, I bought my first Bitcoin on Coinbase back in 2017. So this is crazy for me. But I know you guys are trying to verticalize a lot of the stack as a financial application from spot trading, prediction markets, Fibcoin interest and also institutional trading. But there are also a lot of other companies that are trying to do the same thing. How do you guys differentiate in those plans from your competitors?

**Brian Armstrong** (Executives):
Yes. It's a great question. So I do think you're right. There are more and more people coming together around this Everything Exchange idea. I think it depends which competitor you're talking about, right? So there's going to be some folks that I think they're not going to lean into this kind of frontier technology, whether it's crypto or AI or perps and prediction markets. And so they're not -- some of the more traditional players are probably not going to have all of these on one platform with a good, let's say, agentic trading interface. I think if you look at some of the more tech-forward ones, it depends -- I think you have to look at -- on the surface, they might look similar but Coinbase is trying to do something a little different than I think the others, which is we're not trying to just bring a bunch of people to Wall Street or something. We're trying to make a new decentralized financial system that doesn't need Wall Street, right and can reach the billions of people that the old system didn't really serve.
So I think there's many -- there's going to be strengths and weaknesses of each of the players, including us. I think that some of the areas where we're going to be a little stronger are on the crypto infrastructure side because that more is in line with our mission, right? And so things like Base have just a really large developer and on-chain ecosystem around it. We cofounded USDC. We created the x402 protocol for agentic commerce. We have really good decentralized exchange integrations. And I'd say one other advantage that Coinbase has is, we actually serve not just consumers but we also serve institutions. We have a developer infrastructure that -- a product that we sell. And so I think it's a little easier to run a business that has just one customer but it's actually a lot more powerful if you can build the right platform to serve multiple customer types, which we've been investing in that platform for a number of years now.
And I think it's really starting to give us leverage and to amortize -- we build something once in an excellent way, we can now launch it across multiple customer segments and we can actually bring all of these customers to a new, let's say, a new asset or market on our exchange. And it's retail, it's institutional, it's businesses, it's developers from like third parties are now all plugging into that. So those are some of the things we're focused on. Actually, if I could put in one more real quick, I'd say that still the majority of financial services is running on the traditional financial system. It's probably 90%, 95%, depends how you estimate it.
And like all fintech companies combined are probably, say, 5% to 10% of the financial services revenue, which is a massive, massive percentage of GDP. And so the real opportunity, I think, is for the tech-enabled fintechs to keep growing and capture that other 90% or 95% of the market and create net new demand from these new categories like agentic finance. So that's really our opportunity. And we're going to do our best to compete but we're also going to create new markets and go capture share from TradFi.

**Zion Thomas** (Analysts):
Awesome. I love the points about the decentralized financial system. I know you guys recently acquired Deribit with your focus more on the institutional investor side of things. Have you seen the growth of that product, the perpetual futures and the options? And how has your plans with that shifted with the recent shift in more of a positive regulatory environment in the U.S.?

**Brian Armstrong** (Executives):
Yes. So we acquired Deribit, which was the largest crypto options trading platform out there and we've made really good progress now integrating it into our existing products. So we've got now this unified regulated global exchange that processes everything, perps, options, futures. We're making Deribit now available to both U.S. and ex U.S. So I think we're one of the only companies that can unify the global liquidity. Historically, this was fragmented across all the offshore stuff, non-U.S. and then in the U.S. had a different world. We're now unifying much of this.
And so it's been a huge benefit for us acquiring Deribit. We're -- we said publicly, we're going to actually relaunch our advanced trader platform under the Coinbase Pro brand. So Coinbase Pro is coming back. And you're right, the regulatory front has gotten a lot better as well. I think we're seeing really tailwinds from that, not just with the GENIUS Act that became law but the -- this SEC and CFTC have been very forward thinking and collaborative between the 2 agencies to get more of this stuff available in the U.S. because they want to see the U.S. win and so do we.

**Zion Thomas** (Analysts):
Yes. As far as the Coinbase Pro, actually used to use when it was GDAX back in the day. So it's going to be cool, that come back. I know you got to focus a lot on like the regulatory stuff in D.C. but I feel like you guys haven't done as much on like the consumer retail marketing side. I know it seems like a lot of the exchanges that did focus heavily on that turned out to be not having the best practices behind the scenes. But I'm curious if you guys have plans to do more marketing along that front to kind of target a different consumer or a different customer segment.

**Brian Armstrong** (Executives):
Yes. So I know this perception is out there sometimes that we're almost like more focused on D.C. than on traders or something like that. I think in the wake of Sam Bankman-Fried kind of blowing up and FTX, I remember there was this really kind of critical moment where I felt like I had to go represent the industry there because nobody else was doing it. And in many ways, I feel like that helped the crypto industry. And it could have -- people forget, like it could have gone really poorly under Gensler. I mean the industry could have effectively been banned in the U.S. and like we had to sue him and push back and we won that case. And there's another version of history that looks a lot worse.
And so in many ways, I'm glad that we did that. Now this doesn't mean -- it's not a zero-sum game. Like we've got to -- we can go build products, we can go talk to our customers and help push the regulatory ball forward. So I'll still be in D.C. periodically but my -- more and more of my focus now is shifting to really just talking to our customers, improving our products. That's going to be my focus much more in 2027. So yes, I think I'd leave it at that.

**Alesia Haas** (Executives):
Well, that's a perfect place to end. We're going to focus on our customers.
Thank you all for joining us for our Q&A for our Q3 2026 earnings. If you haven't already, please go check out our presentation that Brian and I posted to our IR website where we discuss our quarterly results. And we will see you next quarter. Thank you all.

**Brian Armstrong** (Executives):
Thanks all.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### COIN_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Brian Armstrong｜risk：CEO 表示若 CLARITY 法案未過，對 Coinbase 而言大致照常營運，受損的是美國消費者（原話："I think Coinbase would be fine."）
- 2026-07-30｜Brian Armstrong｜risk：CEO 稱法案通過仍較佳，因其提供跨政府任期的持久性（原話："So we still think on margin, it's better if the CLARITY Act passes."）
- 2026-07-30｜Alesia Haas｜competition：CFO 稱與 Circle 的合約續約條件已達成，將以相同條款續約（原話："we have already met the conditions for the Circle contract to renew"）
- 2026-07-30｜Brian Armstrong｜competition：CEO 說明加入 Open USD 的理由是多穩定幣平台定位（原話："the short reason is that we're a multi-stablecoin platform."）
- 2026-07-30｜Brian Armstrong｜risk：CEO 被問及多位高階主管離職，稱策略沒有改變（原話："There's nothing that's changing about the strategy."）
- 2026-07-30｜Alesia Haas｜risk：CFO 稱高階主管異動皆為個別決定（原話："these were all individual decisions."）
- 2026-07-30｜Brian Armstrong｜customer：CEO 回應 AI agent 無品牌忠誠度的問題，稱信任在 agent 時代仍重要（原話："I think trust will continue to be important in that world."）
- 2026-07-30｜Brian Armstrong｜product：CEO 引述 Base 的費用與結算速度作為對 agent 的價格競爭力（原話："actually delivers like sub $0.01 and sub 1-second settlement."）
- 2026-07-30｜Alesia Haas｜margin：CFO 說明成長行銷回收期的基準與近期表現（原話："seeing a 1-year payback on growth marketing efforts, but recently, we've outperformed this benchmark."）
- 2026-07-30｜Alesia Haas｜product：CFO 稱新產品（如預測市場）早期訊號顯示帶動額外現貨交易量而非互相蠶食（原話："These early days are actually indicating that we're seeing incremental trading coming"）
- 2026-07-30｜Brian Armstrong｜customer：CEO 說明以資產存放量階層誘因（Coinbase One Card 回饋率）鼓勵客戶存放更多資產（原話："you can get a higher rate on Coinbase One Card, the more that"）
- 2026-07-30｜Alesia Haas｜customer：CFO 稱本季付費 Coinbase One 訂閱戶創歷史新高，且發生在交易量下滑的市場（原話："we saw an all-time high in paid"）
- 2026-07-30｜Brian Armstrong｜product：CEO 談比特幣相關交易占比下降，並稱比特幣會回來（原話："And I think Bitcoin will come back in a big way, too, by the way."）
- 2026-07-30｜Brian Armstrong｜guidance：CEO 表示 agentic finance 目前不提供具體數字或預測（原話："have any specific numbers or forecast to share on that at the moment."）
- 2026-07-30｜Brian Armstrong｜commitment：CEO 稱預先 IPO 永續合約開放美國客戶在路線圖上，將持續推動（原話："In terms of U.S. access, that is on the road map, and we'll keep pushing on that."）
- 2026-07-30｜Brian Armstrong｜competition：CEO 預期 Robinhood、Stripe 等自建區塊鏈後，區塊鏈也會出現類似穩定幣的整併（原話："So my guess is we're going to see something similar happen with blockchains."）
- 2026-07-30｜Brian Armstrong｜commitment：CEO 承諾持續投資 Base 並開放給所有人建置（原話："to continue to invest in Base. We're going to make sure everyone can build on top of it."）
- 2026-07-30｜Alesia Haas｜capital_allocation：CFO 對 Hyperliquid 合作表示願意分享 USDC 經濟利益以推動網路效應（原話："we're happy to share economics to drive this network effect."）
- 2026-07-30｜Brian Armstrong｜commitment：CEO 承諾持續投資 USDC 成長（原話："we're going to keep investing in USDC to keep growing it."）
- 2026-07-30｜Alesia Haas｜margin：CFO 被問 Coinbase One 單位交易收益是否壓縮，稱整體淨單位經濟為正，但收入會在損益表間轉移（原話："So I think overall, this will be more net unit economic positive to us."）
- 2026-07-30｜Alesia Haas｜margin：CFO 稱若會員普及，收入將在損益表各項目間轉移（原話："But you will see the revenue shift through the P&L if we"）

### 問答異常語氣（迴避／改口／保留）
- COIN_Q2_2026_Earnings_Call_20260730.md｜問：Coinbase One 會員每交易一美元的營收是高於或低於非會員（增益或 take rate 壓縮）｜答法：CFO 自稱給「不令人滿意的答案」，未給出每單位營收數字，只稱平均單位經濟較高、邊緣有例外
- COIN_Q2_2026_Earnings_Call_20260730.md｜問：多位高階主管本季離職，策略為何｜答法：CEO 與 CFO 皆以人才深度與接班規劃回應，未說明離職原因，稱皆為個別決定
- COIN_Q2_2026_Earnings_Call_20260730.md｜問：Hyperliquid 合作顯示第三方持有足夠 USDC 即可取得多數 USDC 經濟利益，如何保護長期經濟利益｜答法：CFO 與 CEO 談網路效應與願意分享經濟利益，未回應如何保護長期經濟利益或給出分潤比例
- COIN_Q2_2026_Earnings_Call_20260730.md｜問：agentic commerce 的營收規模與規劃｜答法：CEO 稱仍很早期，不提供具體數字或預測

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
{"date":"20260525","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Take rate 壓縮可被 transaction volume 成長與 mix 升級（衍生品）抵銷，blended transaction revenue 維持 5-15% CAGR","columns":{"2Y 驗證點":"FY26-27 transaction revenue YoY 從 -25% 回升至 ≥ +10%（FY27）","5Y 驗證點":"FY28-30 transaction revenue 累計成長 ≥ 60%（Deribit 整合 + cycle peak）","10Y 驗證點":"FY35 transaction revenue $5B+（vs FY25 ~$3.5B）","具體數字門檻":"2Y：FY27 transaction rev ≥ $3.8B（Q1 26 是 $755.8M，年化 ≥ $3.0B 為下限）；5Y：accumulated transaction rev FY28-30 ≥ $13B","信息來源":"Q1 2026 8-K + FY24 10-K + Deribit 整合披露","漂移觸發條件":"連 2 季 TTM transaction rev YoY 偏離 -10%（相對 baseline）→ 削弱；連 4 季 → 反轉"}},{"id":"H2","text":"USDC + Base + Subscription 形成「平台基礎設施第二曲線」，subscription revenue 維持 25%+ CAGR 並在 FY28 占比 ≥ 45%","columns":{"2Y 驗證點":"FY26 subscription revenue YoY ≥ +5%（Q1 26 已 $583.5M，年化 ~$2.4B）","5Y 驗證點":"FY28 subscription revenue ≥ $3.5B（含 USDC 50%+ + Base sequencer + Coinbase One + staking）","10Y 驗證點":"FY30 subscription revenue ≥ $5B","具體數字門檻":"2Y：FY27 subscription rev ≥ $2.6B；USDC on-platform AUM ≥ $30B；5Y：subscription / total revenue ratio ≥ 45%","信息來源":"Q1 2026 8-K 揭露 $305M stablecoin rev + Q4 2025 $19M Base sequencer rev + Coinbase 法說會","漂移觸發條件":"連 2 季 USDC AUM YoY 偏離 -15%（vs +35% baseline）→ 削弱；連 4 季 → 反轉"}},{"id":"H3","text":"監管環境（GENIUS Act 規則化 + SEC 訴訟和解）走向「Coinbase 規範性護城河強化」而非「intermediary loyalty rewards 被禁」","columns":{"2Y 驗證點":"FY26-27 Treasury 對 GENIUS Act 的 implementation guidance 不擴大解釋「intermediary」","5Y 驗證點":"FY28-30 SEC 訴訟和解，Coinbase 在 staking / DeFi 等業務獲明確 safe harbor","10Y 驗證點":"FY30+ US 成為全球 crypto 監管 gold standard，Coinbase 為主要規範性 fiat-crypto 介面","具體數字門檻":"2Y：Treasury Final Rule 不擴大解釋 intermediary loyalty rewards 為 stablecoin issuer 行為；5Y：SEC 訴訟和解或勝訴；無新 enforcement action 重大事件","信息來源":"Coinbase 2025-11 Treasury ANPRM 回應 + GENIUS Act 法條原文","漂移觸發條件":"單一監管事件即足以削弱（不需連續）：Treasury 廣義解釋 OR 新 SEC charges → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"BTC 進入新一輪結構性熊市（cycle 30-50% drawdown），平台交易量崩盤","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Spot trading volume YoY；BTC price 6 個月 drawdown","警戒閾值":"連 2 季 spot volume YoY -30%+ AND BTC drawdown -40% → 減倉 1/3"}},{"id":"R2","text":"GENIUS Act Treasury Final Rule 廣義禁止 intermediary loyalty rewards，USDC 收益分潤模式被擊穿","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Treasury rule draft 公告；Coinbase 法律部對外發言調性","警戒閾值":"Final Rule 廣義解釋 → 立即 reduce thesis confidence + thesis 重估"}},{"id":"R3","text":"DEX 主流化（Hyperliquid + Uniswap）+ HOOD 零佣 + Binance.US restructure 三面夾擊，blended take rate 加速壓縮","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Blended transaction take rate（季度）；CEX 整體 spot market share；DEX 占 spot 比例","警戒閾值":"連 4 季 blended take rate YoY -10%+ AND CEX spot 比例下降 → 護城河重估，可能砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":184.99,"archetype":null,"cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名中除程式欄以外的每一個**（程式稍後才會算的 p_bull_pct／p_bear_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；`asym_ratio`／`ev5y_pct`／`irr_base_pct`／`bull_5y_price`／`bear_5y_price` 的漂移歸因同樣由程式生成條目（程式用本次情境、依先換情境後換股價的順序拆量），你不要為它們開條目；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

**給讀者看的文字欄不准出現內部代號**：`thesis.H[]`／`thesis.R[]` 的各欄（信息來源／漂移觸發條件等）、`triggers[].text`、`counter_evidence.contradictions[]` 各欄、`answers.*.verdict`／`answers.*.reasoning` 這類文字，一律不得出現事實表 id（`f_` 開頭，如 `f_consensus_rev_3m_fy1_pct`）或軸／finding id（`軸名#n`，如 `competitive_share_entrants#0`）——這些是程式內部代號，不是給讀者的話。要引用哪個事實或哪個軸，寫進對應的 `fact_refs[]`／`evidence_refs[]` 陣列，文字欄本身只寫人話。

---

## 尾段：scenario_inputs 形狀與回覆格式

**本檔 FY1 共識 EPS ≤ 0（虧損），程式已把估值口徑定為 `sales_multiple`：情境樹用營收路徑 × 終端 EV/S，不用 EPS × 本益比。** 口徑由程式決定，你填什麼 `valuation_basis` 都會被覆寫。`scenario_inputs` 的鍵名與形狀必須完全照下面這份（不得增刪改名；程式據此產生 `dd_scenario.py` 的輸入檔，寫錯鍵名就是整段判斷失效）：

```json
{
  "valuation_basis": "sales_multiple",
  "terminal_label": "FY20XXE",
  "start": {"rev": <FY+1 共識營收，百萬，報告幣別；抄事實表 f_rev_consensus_fy1_m>, "ev_s": <目前 EV/S（EV÷FY+1 共識營收）；抄事實表 f_ev_s_fwd>, "basis": "<起點口徑一句話：營收取哪一年、EV/S 的分母是哪一年，須與終端 EV/S 分母同口徑>"},
  "rev": {"bull": [<Y1>, <Y2>, <Y3>, <Y4>, <Y5>], "base": [五個數], "bear": [五個數]},
  "ev_s": {"bull": <終端 EV/S>, "base": <倍數>, "bear": <倍數>},
  "net_debt_y5": {"bull": <終端年淨負債，百萬，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "shares_y5": {"bull": <終端年稀釋股數，百萬股，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "p": {"bull": <機率整數>, "base": <整數>, "bear": <整數>},
  "yield_pct": {"dividend": <股息殖利率 %>, "net_buyback": <淨回購殖利率 %>},
  "max_dd": {"lo": <負數 %>, "hi": <負數 %>, "basis": "<範圍怎麼推出來的，見判斷卡③情境樹假設段>", "trigger_time": null},
  "basis": {"bull": "<這支路徑的假設一句>", "base": "…", "bear": "…"},
  "endo_ceiling_exceeded": <true|false，共識 CAGR 是否超過 §5.R 內生天花板>
}
```

（**不要**填 `eps`、`pe`、`second_stage`、`peer_max_fpe`；`eps_meta` 仍照常寫共識三年 EPS。現價、目前淨負債（`f_net_debt_m`）、目前股數（`f_shares_diluted_m`）由程式從事實表帶進 `scenario.json`。）

**終端每股價＝max(0, (終端營收 × 終端 EV/S − 終端淨負債) ÷ 終端股數)**，股權價值為負就是 0（Bear 情境債務吃光股權時，要如實寫出讓它歸零，不要為了好看調高倍數）。`net_debt_y5` 要反映該情境下的現金流與融資（虧損公司的淨負債通常會變大，不是沿用目前值）；`shares_y5` 要反映該情境下的增資與稀釋；兩者填 null 才是沿用目前值，不是預設答案。`ev_s` 是終端年 EV ÷ 終端年營收，須與 `start.ev_s` 同口徑（前瞻 vs trailing 不可混）。

`dd_scenario.py` 會擋：`rev` 各路徑長度 ≠ 5、終端營收非 Bear＜Base＜Bull、三機率加總 ≠ 100、`p.bear` ＜ 20、`endo_ceiling_exceeded=true` 且 `p.bear` ＜ 30、`p.base` ＞ 50。另有機械閘：Bull 前兩年營收不得與 Base 相同（情境退化）、`|max_dd.lo|` 不得小於任一情境終點跌幅。機率與路徑是你的判斷，算術（IRR／倍數貢獻／AR）全由腳本算，不要自己填結果欄。

**回覆全文即 `judgment.json` 內容**：緊湊 JSON（`json.dumps(obj, separators=(",", ":"))` 等效格式），陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）。不寫 `scenario.json`（程式從 `scenario_inputs` 產生）。不填不歸你的欄（`decision_inputs` 的機械欄、`reasoning`／`plain` 頂層、`moat.spread_table`／`competitors`、`contradictions`／`triggers` 等舊形狀頂層欄）——填了機械閘會擋。`decision_inputs.asym_ratio`／`irr_base_pct`／`ev5y_pct` 一律填 `null`，由腳本從 scenario 機械算回。

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COIN_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
