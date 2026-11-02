你是 stock-analyst **v20 判斷 agent**，標的 BWA（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"BWA","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWA_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWA_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":3487,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 borgwarner.com Q3 2026 press release（2026-10-29）"},"note":"未能以一手來源驗證；二手來源稱營收低於共識（約 $3.56–3.58B，未驗證）"},{"id":"f_kpi1_adjusted_operating_incom","label":"Adjusted operating income / margin","value":10.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 borgwarner.com Q3 2026 press release"},"note":"未驗證"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":8.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 borgwarner.com Q3 2026 press release"},"note":"n/a"},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":195,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 borgwarner.com Q3 2026 press release（營運現金流 $320m）"},"note":"n/a"},{"id":"f_kpi4_adjusted_diluted_eps","label":"Adjusted diluted EPS","value":1.39,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 borgwarner.com Q3 2026 press release"},"note":"財報前共識約 $1.24（二手來源，7 位分析師，未以一手驗證）"},{"id":"f_kpi5_fy2026_guidance","label":"FY2026 guidance（管理層指引）","value":"營收 $14.0–14.2B；調整後營業利益率 10.7–10.9%；調整後 EPS $5.20–5.35；GAAP EPS $4.65–4.84；營運現金流 $1.6–1.7B；FCF $0.9–1.1B","period":"Q3 2026（公告於 2026-10-29）","unit":"mixed","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（公告於 2026-10-29）","citation":"公司 IR 新聞稿 borgwarner.com Q3 2026 press release"},"note":"調整後 EPS 指引上調自 $5.05–5.30；上調原因為庫藏股與較低有效稅率；FCF 指引不變；營收區間自 $14.0–14.3B 收窄；假設電池事業銷售約減 $250m、匯率約增 $250m"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_bwa_gross_margin_pct","label":"BWA 毛利率","value":19.8,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWA.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bwa_operating_margin_pct","label":"BWA 營業利益率","value":10.2,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWA.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bwa_fcf_margin_pct","label":"BWA FCF 利潤率","value":9.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWA.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aptv_gross_margin_pct","label":"APTV 毛利率","value":19.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APTV.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aptv_operating_margin_pct","label":"APTV 營業利益率","value":9.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APTV.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aptv_fcf_margin_pct","label":"APTV FCF 利潤率","value":3.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APTV.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lea_gross_margin_pct","label":"LEA 毛利率","value":6.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lea_operating_margin_pct","label":"LEA 營業利益率","value":3.67,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lea_fcf_margin_pct","label":"LEA FCF 利潤率","value":3.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mga_gross_margin_pct","label":"MGA 毛利率","value":14.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mga_operating_margin_pct","label":"MGA 營業利益率","value":5.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mga_fcf_margin_pct","label":"MGA FCF 利潤率","value":7.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":52.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-6.77,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":27.7,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.96,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.21 → 5.26）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.17,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.91 → 5.9）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.45,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.63 → 6.66）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.26,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":5.9,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":6.66,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.54,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 5.18 → 5.26（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":22.11,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝48.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":48.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.74,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.85,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝71.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":71.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":9.92,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 5.26，分子＝快照價 52.19","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.303,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1616.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 3199.0、現金 1583.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":200.81,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":12096.49,"period":"2026-11-03","unit":"USD m","basis":"市值 10480.49 ＋ 淨負債 1616.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":14099.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（13 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":14675.45,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.86,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 51.94 / W52 57.39 / W104 45.78 / W250 39.13 / W250 13週斜率 0.64%"},{"id":"f_ma_w52","label":"52 週均線","value":57.39,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":45.78,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":39.13,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.64,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K列出主要非OEM對手（Bosch、Denso、Garrett、Hitachi、Magna、Valeo、Schaeffler、CATL）並指出亦與電動化新創競爭","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm","excerpt":"The Company’s major non-OEM competitors are Robert Bosch GmbH, Denso Corporation, Garrett Motion, Hitachi, Ltd., Magna Powertrain (an operating unit of Magna International Inc.), Valeo, Schaeffler Group and Contemporary Amperex Technology Co., Limited. The Company also competes with certain start-ups in electrification.","as_of":"2026-02-11","retrieved_at":"2026-11-03","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K風險因素：中國本土OEM擴大市占並增加自製原由Tier 1供應之零件；多家主要OEM表示將內製部分零件","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm","excerpt":"Domestic Chinese OEMs continue to expand their market share in and outside of China, and are increasingly insourcing certain components once sourced from Tier 1 suppliers.","as_of":"2026-02-11","retrieved_at":"2026-11-03","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2026Q2公布7項新訂單，含中國OEM全尺寸SUV分動箱（2026Q4量產）與歐洲OEM eTurbo（2029量產）；有機營收年減約1.2%，未稱跑贏市場","source":"BorgWarner Q2 2026 press release","url":"https://www.borgwarner.com/newsroom/press-releases/2026/08/05/borgwarner-reports-strong-second-quarter-2026-results--increases-2026-adjusted-eps-guidance-and-share-repurchase-authorization-by--1-billion--announces-7-awards-across-portfolio-to-support-long-term-profitable-growth","excerpt":"Torque-on-demand with mechanical lock transfer case award with a Chinese OEM for a newly developed, full-size SUV. Production is expected to begin in the fourth quarter of 2026.","as_of":"2026-08-05","retrieved_at":"2026-11-03","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因素：競爭對手包含主要 OEM 客戶的垂直整合單位；多家主要 OEM 客戶已表明有意將公司生產的部分零組件自製（insource），OEM 已選擇且可能再選擇自製取代現有供應。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm","excerpt":"Although many OEMs have indicated that they will continue to rely on outside suppliers, a number of major OEM customers have indicated their intent to insource certain components that we produce, and many do manufacture products for their own uses that directly compete with our products.","as_of":"2026-02-11","retrieved_at":"2026-11-03","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K：公司自身採購端使用 dual sourcing 等手段（屬供應端，非客戶對 BWA 導入第二供應商）。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm","excerpt":"the Company uses long-term contracts, cost sharing arrangements, design changes, dual sourcing, customer buy programs and limited financial instruments to help control costs.","as_of":"2026-02-11","retrieved_at":"2026-11-03","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K：Volkswagen 占營收 13%（2024 年 10%、2023 年 11%），Ford 12%（13%、14%）；無其他單一客戶超過 10%。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm","excerpt":"Volkswagen 13 % 10 % 11 % Ford 12 % 13 % 14 % No other single customer accounted for more than 10% of the Company’s consolidated net sales in any of the years presented. Sales to the Company’s top ten customers represented 71% of sales for the year ended December 31, 2025.","as_of":"2026-02-11","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"10-K 風險因子：前十大客戶占 2025 年營收 71%，供貨合約多為需求合約，失去主要客戶或其車款大幅減產會對業務造成不成比例的重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A. Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm","excerpt":"Sales to the Company’s top ten customers represented 71% of sales for the year ended December 31, 2025. Changes in our business relationships with any of our major customers or in the timing, size and continuation of their various programs could have a disproportionately material adverse impact on our business.","as_of":"2026-02-11","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Volkswagen 集團評等頁：Moody's 2025-03 由 A3 降至 Baa1，之後展望轉負；S&P BBB+ 展望負面。","source":"Volkswagen Group Annual Report 2025 - Ratings","url":"https://annualreport2025.volkswagen-group.com/group-management-report/shares-and-bonds/ratings.html","excerpt":"agency Standard & Poor’s confirmed its short-term and long-term ratings for Volkswagen AG of A–2 and BBB+ respectively. However, the outlook was revised down from “stable” to “negative”. In March 2025, Moody’s Investors Service downgraded the long-term rating by one notch, from A3 to Baa1.","as_of":"2026-03-01","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Ford 2026 Q2 後上調全年調整後 EBIT 指引至 100-110 億美元、自由現金流 60-70 億美元。","source":"Teleborsa: Ford alza la guidance 2026","url":"https://www.teleborsa.it/DettaglioNews/201_2026-07-29_TLB/Ford-alza-la-guidance-2026-dopo-utili-secondo-trimestre-oltre-le-attese.html","excerpt":"Per l'intero 2026 La società ha alzato le previsioni di EBIT rettificato a 10-11 miliardi (da 8,5-10,5 miliardi) e del flusso di cassa libero rettificato a 6-7 miliardi (da 5-6 miliardi di dollari).","as_of":"2026-07-29","retrieved_at":"2026-11-03","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"BorgWarner Q3 2026 call：2026 加權終端市場下滑1~2%，含約170bp來自北美無補貼與歐洲需求弱導致電池事業銷售下滑；輕型車eProduct銷售Q3年增33%至$630M（主要歐洲）；管理層預期新案支撐2027年小幅優於市場成長","source":"BorgWarner Q3 2026 earnings call highlights (MarketBeat) / 10-Q 2026-09-30","url":"https://www.marketbeat.com/instant-alerts/transcript-borgwarner-q3-earnings-call-highlights-2026-10-29/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"2026-11-03","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Ken Research（2026年1月）稱汽車供應商產業面臨獲利結構性重置而非週期性放緩，快速擴產與中國供應商積極定價壓低全球價格底部","source":"Ken Research - Automotive Suppliers Profitability Reset Global","url":"https://www.kenresearch.com/articles/automotive-suppliers-profitability-reset-global","excerpt":"The global automotive supplier industry is no longer facing a cyclical slowdown but a structural reset in profitability.","as_of":"2026-01-15","retrieved_at":"2026-11-03","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"BCG 2026年3月供應商研究：供應商已脫離急性危機但未回常態，預估至2027年平均年成長約2~3%，頂尾分化擴大","source":"BCG 2026 Global Automotive Supplier Study","url":"https://web-assets.bcg.com/1a/ec/fe8b5f8a494b8557ef0c3bbbe632/2026-global-automotive-supplier-study-march2026.pdf","excerpt":"The automotive supplier industry has exited the acute crisis years, but it has not returned to normal.","as_of":"2026-03-01","retrieved_at":"2026-11-03","affects":["valuation","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"BorgWarner 持續追討被推翻之 IEEPA 關稅退款，已開始收到部分退款，但金額與時點仍不確定，截至 2026-09-30 尚未認列退款應收款","source":"SEC EDGAR 10-Q (period ending 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0000908255/000090825526000062/bwa-20260930.htm","excerpt":"actively pursue the refund recovery of certain tariffs paid to the U.S. government, which were levied under the International Emergency Economic Powers Act and subsequently invalidated by the United States (“U.S.”) Supreme Court on February 20, 2026. Following this ruling, the Company has submitted tariff recovery claims through the U.S. Customs and Border Protection (“CBP”) portal.","as_of":"2026-10-30","retrieved_at":"2026-11-03","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 關稅對成本與營收的影響：客戶回收關稅使銷售增加約 $80M；關稅費用使銷貨成本年增約 $108M。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm","excerpt":"Customer recoveries relating to tariffs increased sales by approximately $80 million.\n\n•Tariff expense resulted in a year-over-year increase in cost of sales of approximately $108 million.","as_of":"2026-02-11","retrieved_at":"2026-11-03","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：2025 年美國對歐盟、加拿大、墨西哥、中國等課徵關稅，已推高原料與零件成本，並引發中國等報復性關稅；USMCA 2026 年待更新，中國供應鏈整合帶來特有風險。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm","excerpt":"the United States-Mexico-Canada Agreement (\"USMCA\") is subject to renewal in 2026. There can be no assurance that the USMCA will be renewed or, if renewed, any newly negotiated terms in the USMCA will not adversely affect our business.","as_of":"2026-02-11","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"公司以採購區域調整、長約、成本分攤、設計變更、雙源、客戶 buy program 等手段緩解關稅與出口禁令影響，2026 年起沿用。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm","excerpt":"The Company uses long-term contracts, cost sharing arrangements, design changes, dual sourcing, customer buy programs and limited financial instruments to help control costs. The Company intends to use similar measures in 2026 and beyond.","as_of":"2026-02-11","retrieved_at":"2026-11-03","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"BorgWarner 10-Q（2026 Q2）稱已收到約 $35M IEEPA 關稅退款，但因金額與時點不確定未認列退款應收；2025 年對 EU、加拿大、墨西哥、中國進口加徵關稅推高原料與零組件成本。","source":"BorgWarner 10-Q 2026-06-30 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000908255/000090825526000051/bwa-20260630.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"高盛分析師稱 BorgWarner 約 20% 營收來自中國，其中約 75% 與中國本土 OEM 相關，中國 eProduct 約 90% 與本土 OEM 相關；進口美國比重低於平均。","source":"Benzinga/Webull 轉述 Goldman Sachs","url":"https://webull.ca/news-detail/12623274394698752","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"風險彙整站稱 FY2025 約 84% 淨銷售來自美國以外，中國、墨西哥、德國、波蘭、南韓、匈牙利各逾 5%。","source":"policyrisk.com BWA","url":"https://policyrisk.com/world/company/BWA","excerpt":null,"as_of":"2026-03-01","retrieved_at":"2026-11-03","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 Turbos & Thermal Technologies 銷售 $1,372M，較去年同期 $1,437M 下滑；分部調整後營業利益率 14.7%（去年 15.2%）","source":"BorgWarner 10-Q (period 2026-09-30), SEC","url":"https://www.sec.gov/Archives/edgar/data/0000908255/000090825526000062/bwa-20260930.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"2026-11-03","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 總營收 $3,487M，年減約 2.9%；有機營收年減 3.1%；2026 營收指引收窄至 $14.0–14.2B，部分因電池業務銷售偏弱；調整後 EPS 指引上調至 $5.20–5.35","source":"BorgWarner 8-K Q3 2026 press release, SEC","url":"https://www.sec.gov/Archives/edgar/data/0000908255/000090825526000060/a20260930ex991pressrelease.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"2026-11-03","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"管理層預期 2026 加權終端市場下滑 1%–2%（前次預期持平至下滑 3%）；電池銷售拖累約 170bp，原因為北美缺乏補貼與歐洲需求偏弱；輕型車 eProducts Q3 銷售年增 33% 至 $630M，以歐洲需求為主","source":"MarketBeat, BorgWarner Q3 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-borgwarner-q3-earnings-call-highlights-2026-10-29/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"2026-11-03","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"BWA 2026Q3 10-Q：eProduct 營收約 7.08 億美元、占總營收 20%；前九個月約 19.68 億美元、占 18%；策略為涵蓋電動、油電混合與燃燒車的技術型產品組合。","source":"SEC EDGAR 10-Q（截至 2026-09-30）","url":"https://www.sec.gov/Archives/edgar/data/0000908255/000090825526000062/bwa-20260930.htm","excerpt":"The Company’s current strategy is to focus on profitable growth across its technology-focused product portfolio that supports electric, hybrid and combustion vehicles.","as_of":"2026-10-30","retrieved_at":"2026-11-03","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Pitchgrade 研究文章指燃燒相關產品（如渦輪增壓器）替代風險最高，且 OEM 垂直整合（如 Tesla 自製馬達與逆變器）為成長中威脅（二手意見）。","source":"Pitchgrade：borgwarner ai margin pressure","url":"https://pitchgrade.com/research/borgwarner-ai-margin-pressure","excerpt":"turbocharger plants spread over fewer units as ICE production declines. On the investment side, competing in eProducts requires sustained R&D in power electronics, motor design, and software-defined drivetrain management — areas where BorgWarner competes against specialized EV component companies and OEM vertical integration. OEM vertical integration is a significant AI-amplified threat. Tesla","as_of":"2026-02-15","retrieved_at":"2026-11-03","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：汽車產品一般直接賣給 OEM，依年度合約或長期供應協議，直接從工廠出貨；未見通路／商業模式結構性轉變（訂閱、D2C）描述。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm","excerpt":"The Company’s automotive products are generally sold directly to OEMs, substantially pursuant to negotiated annual contracts, long-term supply agreements or terms and conditions as may be modified by the parties. Deliveries are subject to periodic authorizations based upon OEM production schedules. The Company typically ships its products directly from its plants to the OEMs.","as_of":"2026-02-11","retrieved_at":"2026-11-03","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 2026 (2026-08-05)：公司上調全年調整後EPS指引至$5.05–5.30（原$5.00–5.20），銷售$14.0–14.3B不變；新中點約$5.18，與賣方共識（約$5.19 EPS／$14.2B 營收，MarketBeat）大致持平。","source":"Benzinga financials / MarketBeat FY2026 guidance alert","url":"https://www.marketbeat.com/instant-alerts/borgwarner-nysebwa-issues-fy-2026-earnings-guidance-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-11-03","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價分布（2026-08 下旬）：Bullstory 列15位分析師平均$79.67、高$95、低$62；Walnut 平均$78.87、中位$79、10 買5 持有；MarketBeat 2026-10-10 註記平均$78.57、共識 Moderate Buy。對照 2026-03 初 MarketBeat 平均$59.14。","source":"Bullstory / Walnut / MarketBeat (2026-10-10)","url":"https://www.marketbeat.com/instant-alerts/analyst-borgwarner-nyse-bwa-upgraded-at-wall-street-zen-2026-10-10/","excerpt":null,"as_of":"2026-10-10","retrieved_at":"2026-11-03","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2後目標價調整：JPMorgan $75→$85、Barclays $83→$85、Baird $70→$79、Deutsche Bank $81→$80。","source":"Yahoo Finance / 搜尋結果彙整","url":"https://finance.yahoo.com/markets/stocks/articles/td-cowen-raises-price-target-231243287.html","excerpt":null,"as_of":"2026-08-06","retrieved_at":"2026-11-03","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026（約10-29）：單一來源稱調整後EPS $1.39 優於共識約$1.24–1.25，營收$3.49B略低於預期、年減2.9%；同來源提及部分2026展望下調，但未給新數字，需核對Q3新聞稿。","source":"搜尋摘要（單一來源，未讀頁面）；SEC 8-K 2026-09-30 press release 列表","url":"https://www.sec.gov/Archives/edgar/data/0000908255/000090825526000060/a20260930ex991pressrelease.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"2026-11-03","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2025-10-15 BorgWarner 與 PHINIA 簽和解協議，PHINIA 付 $78 百萬，了結 VAT 退稅訴訟；BorgWarner 2025 年認列淨費用 $40 百萬","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm","excerpt":"On October 15, 2025, the Company entered into a settlement agreement (the “Settlement Agreement”) with PHINIA, pursuant to which PHINIA agreed to pay the Company $78 million, resolving the lawsuit and certain other matters relating to the spin-off.","as_of":"2026-02-11","retrieved_at":"2026-11-03","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2025-11-03 至 2026-11-03 共 11 份 8-K，含重大項目者 0 份（無併購、重編、下市等）","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000908255&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"2026-11-03","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Magna 計畫將原訂 2026 capex 下修 $200M，capex/sales 低於 4%；報導日期疑為 2024，未核","source":"Crain's Detroit - EV delays, changing plans take a financial toll on auto industry's suppliers","url":"https://prod.crainsdetroit.com/node/904781","excerpt":null,"as_of":"2024-10-01","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"BorgWarner 於資料中心／工業市場已裝 2GW 渦輪發電機產能，年內決定是否擴產","source":"Nasdaq - BorgWarner Q1 earnings call highlights","url":"https://www.nasdaq.com/articles/borgwarner-q1-earnings-call-highlights","excerpt":null,"as_of":"2026-05-01","retrieved_at":"2026-11-03","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"BorgWarner 2026-09-30 存貨 $1,299M，對比欄 $1,207M（比較日期待核）","source":"BorgWarner 8-K Q3 2026 press release","url":"https://www.sec.gov/Archives/edgar/data/0000908255/000090825526000060/a20260930ex991pressrelease.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"BWA 調整後月價自2008年5月約$18.67跌至2009年1月約$6.18，2009年12月回到約$12.16（約8個月跌約67%，約11個月後回升近一倍）","source":"digrin BWA Price History","url":"https://www.digrin.com/stocks/detail/BWA/price","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-11-03","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2009年Q2 BWA 排除一次性項目營業利益僅$0.8M（占銷售0.1%），去年同期為8.2%；銷售$916.2M，年減39.6%","source":"BorgWarner Q2 2009 results (SEC EX-99.1 / AftermarketNews)","url":"https://www.aftermarketnews.com/?p=61629","excerpt":null,"as_of":"2009-07-30","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2020 COVID：H1銷售$3,705M年減28%；Q2 Adjusted EBIT $28M（去年同期$249M）；Drivetrain Q2 Adjusted EBIT margin 0.2%（去年10.2%）；全年毛利率18.8% vs 2019年20.7%","source":"BorgWarner 10-Q Q2 2020 / 10-K FY2020","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825521000008/bwa-20201231.htm","excerpt":null,"as_of":"2021-02-17","retrieved_at":"2026-11-03","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2008-09產業：輕型車產量2009年約降40%至約800萬輛；零組件出貨2008年-14%、2009年再-24%；北美產量2012年回到約1,600萬輛（V型）","source":"US Dept of Commerce Auto Parts Industry report 2012 / industry reviews","url":"https://legacy.trade.gov/td/otm/assets/auto/AutoParts2012.pdf","excerpt":"Parts shipments fell 14 percent from 2007 to 2008 and an additional 24 percent from 2008 to 2009.","as_of":"2012-01-01","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K無併購類重大項目（1.01/2.01等）","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000908255&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"與 PHINIA 的 VAT 退稅訴訟於 2025-10-15 以 PHINIA 付 $78 百萬和解","source":"SEC EDGAR 10-K FY2025 Item 3/7","url":"https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm","excerpt":"On October 15, 2025, the Company entered into a settlement agreement (the “Settlement Agreement”) with PHINIA, pursuant to which PHINIA agreed to pay the Company $78 million, resolving the lawsuit and certain other matters relating to the spin-off.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"BWA","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.8,"operating_margin_pct":10.2,"fcf_margin_pct":9.16,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWA","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"APTV","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.63,"operating_margin_pct":9.75,"fcf_margin_pct":3.65,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APTV","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"LEA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":6.86,"operating_margin_pct":3.67,"fcf_margin_pct":3.58,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MGA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":14.71,"operating_margin_pct":5.48,"fcf_margin_pct":7.52,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"BWA"},"financial_history":{"ticker":"BWA","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":12635000000.0,"revenue_yoy_pct":null,"gross_margin_pct":18.75,"operating_margin_pct":8.57,"net_income":944000000.0,"diluted_eps":3.99,"free_cash_flow":558000000.0,"fcf_margin_pct":4.42,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":14198000000.0,"revenue_yoy_pct":12.37,"gross_margin_pct":18.09,"operating_margin_pct":8.9,"net_income":625000000.0,"diluted_eps":2.67,"free_cash_flow":565000000.0,"fcf_margin_pct":3.98,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":14086000000.0,"revenue_yoy_pct":-0.79,"gross_margin_pct":18.8,"operating_margin_pct":9.25,"net_income":338000000.0,"diluted_eps":1.5,"free_cash_flow":729000000.0,"fcf_margin_pct":5.18,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":14316000000.0,"revenue_yoy_pct":1.63,"gross_margin_pct":18.68,"operating_margin_pct":9.24,"net_income":277000000.0,"diluted_eps":1.28,"free_cash_flow":1208000000.0,"fcf_margin_pct":8.44,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/BWA/BWA_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**BorgWarner Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good morning. My name is Nick, and I will be your conference specialist. At this time, I would like to welcome everyone to the BorgWarner 2026 Third Quarter Results Conference Call. [Operator Instructions] 
I would now like to turn the conference over to Patrick Nolan, Vice President of Investor Relations. Mr. Nolan, you may begin your conference.

**Patrick Nolan** (Executives):
Thank you, Nick. Good morning, everyone, and thank you for joining us today. We issued our earnings release earlier this morning. It's posted on our website, borgwarner.com, both on our home page and our Investor Relations home page. 
With regard to our Investor Relations calendar, we will be attending multiple investor conferences between now and our next earnings release. Please see the Events section of our Investor Relations homepage for a full list. 
Before we begin, I need to inform you that during this call, we may make forward-looking statements, which involve risks and uncertainties as detailed in our 10-K. Our actual results may differ significantly from the matters discussed today. 
During today's presentation, we will highlight certain non-GAAP measures in order to provide a clearer picture of how the core business performed and for comparison purposes with prior periods. 
When you hear us say adjusted, that means excluding non-comparable items. When you hear us say organic, that means excluding the impact of FX. We will also refer to our incremental margin performance. Our incremental margin is defined as the organic change in our adjusted operating income divided by the organic change in our sales. We will also refer to our growth compared to our market. When you hear us say market, that means the change in light vehicle production weighted for our geographic exposure. 
Please note that we've posted today's earnings call presentation to the IR page of our website. We encourage you to follow along with these slides during our discussion. 
With that, I'm happy to turn the call over to Joe.

**Joseph Fadool** (Executives):
Thank you, Pat, and good morning, everyone. I'm pleased to share our results for the third quarter of 2026 and provide an overall company update, starting on Slide 5. 
I want to begin by thanking our employees, customers and suppliers for all of their trust, efforts and continued support. In the quarter, we achieved sales of just under $3.5 billion. Excluding the decline in our Battery Energy Systems segment, our organic net sales were down modestly year-over-year or roughly in line with the decline in global market production. 
Importantly, our light vehicle eProduct sales were up 33%, primarily due to European growth. Our adjusted operating margin and adjusted earnings per share performance was strong in the quarter. The company continued to operate at a very high level and delivered 20 basis points of adjusted margin expansion and 12% adjusted earnings per share growth, despite a declining production environment. This solid result was once again driven by our focus on cost controls across our business. 
I'm excited to report that our strong award activity continued into the third quarter. Today, I'll highlight 9 new business awards across our Foundational and eProduct portfolios. These wins represent only a portion of the awards secured during the quarter and highlight the strength of our Foundational and eProduct portfolio and the need for our products across combustion, hybrid and electrified architectures. Additionally, I believe the sustained level of award activity that we've seen over the last several quarters underscores the strength of our technology-focused portfolio and our deep customer relationships. 
Equally exciting is the progress we made in the quarter in taking meaningful steps to advance our product readiness and accelerate our quoting activity across our data center and other industrial markets portfolio. I will share a more detailed update in a few moments. 
Lastly, we remain focused on the efficient deployment of capital to drive shareholder value. In the quarter, we returned approximately $210 million or over 100% of our third quarter free cash flow to shareholders through share repurchases and the payment of our quarterly cash dividend. Including our currently planned fourth quarter repurchases, we expect to return over $700 million to shareholders in 2026. 
Looking back on our year-to-date performance, I'm very proud of our team and our results. Once again, we executed at a very high level, which I believe positions us well to achieve our full year sales, margin, free cash flow and increased EPS guidance. 
Next, I'd like to highlight 9 product awards that demonstrate both the competitiveness of our technology and our ability to support our customers' powertrain needs in key markets. 
First, BorgWarner will supply engine control modules for a new internal combustion engine pickup truck platform for one of our long-standing global OEM customers. The new high-volume contract extends the company's existing customer relationship. Securing the strategic ECU program maintains BorgWarner's electronics leadership and extends our engagement with this long-time partner through 2034. 
Next, BorgWarner has secured 3 separate conquest business awards with a global powertrain technology leader, including 1 contract for our variable turbine geometry turbocharger and 2 contracts for our wastegate turbocharger. The technologies will be used on the customer's light vehicle gasoline platforms in both South America and Europe. I believe these awards reflect the strength of our offering, including our competitive solutions and technical expertise. 
Next, BorgWarner has secured its first business award for its new aluminum wire eMotor technology from a major Chinese OEM, marking the technology's introduction to the market. This product will be used in hybrid vehicles across multiple applications, including generator and traction motors for auxiliary drive applications. The technology combines aluminum conductors with BorgWarner's hairpin winding expertise to deliver significant weight and cost benefits. 
Compared with a conventional copper wire motor, the aluminum wire solution maintains peak torque and peak power, while reducing wire weight by more than 60% and reducing wire cost by more than 80%. We are proud to introduce BorgWarner's aluminum wire eMotor technology to the market and to further strengthen our long-standing relationship with this customer. 
Next, BorgWarner has secured 3 eMotor business awards in China for a range of electrified and hybrid vehicle programs. The new business broadens the company's customer base and expands the application of its eMotor technologies in the Chinese market. I believe that the breadth of these programs demonstrates our ability to address diverse application requirements through strong product performance, cost optimization and localized manufacturing. 
And lastly, BorgWarner has secured a next-generation high-voltage inverter award for future battery electric vehicle programs with a global OEM. The award builds on an existing electrification partnership and further strengthens BorgWarner's position as a leading provider of advanced power electronic solutions for electric vehicles. I believe this business reflects the confidence customers place in BorgWarner's power electronics expertise and our ability to deliver innovative, high-performance electrification solutions. 
Next, on Slide 7, I would like to discuss how we are improving our product readiness and accelerating our quoting activity across our data center and other industrial markets portfolio. 
Let's start with an update on our turbine generator launch progress. I'm very pleased with the advancements we've made over the past quarter. Our partner is planning to expand external demonstrations of the turbine generator system during the fourth quarter due to strong customer interest. 
Our UL compliance process continues to progress well. The UL certification process of the subsystems is now largely complete and system UL certification is underway. The construction of the final assembly plant in North Carolina has now been completed and manufacturing floor and capital installation are expected in December. As a result, we expect to begin production trials by year-end. 
Overall, I'm very excited and pleased with the team's progress, which will position us well to meet the strong customer interest that we continue to see, including multiple hyperscalers. 
Turning next to our battery energy storage system. Our energy storage solutions are intended to support a range of use cases in data center and other industrial environments, and we continue to assess new potential applications. Customer validation and our UL compliance processes are advancing well. In addition, we are getting solid engagement with multiple customers across both NMC and LFP cell applications. We continue to expect that we will be production ready in 2027. 
Now turning to our microgrid inverter offerings. We have now shipped BorgWarner samples to 7 customers and engagements with other potential customers are underway. We expect to complete UL certification of our microgrid inverter in early 2027. Customer reaction has continued to remain very positive. For example, our inverter system efficiency testing is ahead of peers based on customer feedback. Customers believe we have the right value proposition, including U.S. manufacturing. 
Additionally, our high-voltage and power dense liquid cooled power electronics expertise is seen as a competitive advantage as we continue to advance our product readiness. We are also continuing to expand our power electronics portfolio for both data center and industrial applications. 
We've developed an 800-volt Power Supply Unit or PSU and showcased it at the recent Data Center World Power industry event in Dallas, Texas, in the third quarter. 
Lastly, I'm proud to report that we have begun the initial quoting process with our first major customer for our microgrid inverter. Overall, I view all of these steps as great signs of increased customer engagement and our right to win in this high-growth market. 
To summarize, I believe there are 4 key takeaways from today's call. First, BorgWarner's third quarter results were strong. Our light vehicle eProduct sales increased 33%. Our adjusted operating margin expanded 20 basis points and adjusted EPS grew 12% compared with the third quarter of 2025. Additionally, we increased our full year EPS guidance, reflecting our continued focus on growing the earnings power of the company. 
Second, we announced 9 new business awards across our portfolio in the quarter, which we believe further demonstrates our focus on product leadership and the need for our highly engineered solutions across combustion, hybrid, and BEV architectures. 
Third, we further improved our product readiness across our data center and other industrial markets portfolio. At the same time, we saw accelerating quoting activity. I continue to believe that our mechanical and electronic core competencies will enable us to successfully capture multiple growth vectors outside of our core automotive market. 
And finally, we took meaningful steps to return capital to shareholders during the third quarter with approximately $210 million returned through our cash dividend and share repurchases. Overall, I believe our year-to-date results illustrate the strength of our team, our product portfolio and the long-term earnings power of our business. I'm excited to continue our positive momentum as we close out the year and look ahead to 2027. 
With that, I'll turn the call over to Craig.

**Craig Aaron** (Executives):
Thank you, Joe, and good morning, everyone. I'm excited to share the details of our third quarter financials by turning to Slide 8 for a look at our year-over-year sales. Last year's Q3 sales were just under $3.6 billion. In the third quarter, stronger foreign currencies drove a year-over-year increase in sales of $8 million. Then you can see the sales headwind from our battery business, which drove a year-over-year decrease in sales of $54 million. The remaining organic sales decrease of $58 million or 1.6% was roughly in line with the decline in light vehicle market production for the quarter. 
Importantly, our light vehicle eProduct sales were $630 million in the quarter or a 33% increase compared with a year ago, primarily due to strength in Europe. Sum of these items resulted in under $3.5 billion of net sales in the third quarter. 
Turning to Slide 9. You can see our earnings and cash flow performance for the quarter. Our third quarter adjusted operating income was $381 million, equating to a strong 10.9% adjusted operating margin. That compares to adjusted operating income of $385 million or a 10.7% adjusted operating margin from a year ago. Excluding FX impacts, adjusted operating income decreased $6 million on $112 million of lower sales. This strong year-over-year performance benefited from ongoing cost reduction actions that our teams continue to take across our business. 
Our adjusted EPS was up $0.15 or 12% compared with a year ago from lower taxes and the impact of approximately $725 million in share repurchases or approximately 6% of the company's current market capitalization over the past 4 quarters. 
And finally, we generated free cash flow of $195 million in the third quarter, which helped support $175 million in share repurchases and $35 million in dividend payments. I believe this once again demonstrates our focus on creating value with our consistent and our strong free cash flow. 
Now let's turn to Slide 10 and take a look at our full year 2026 outlook. We are modestly adjusting the high end of our full year sales outlook based on a narrowing of our industry production expectations. However, we are maintaining our full year adjusted operating margin range despite a lower production environment based on our strong year-to-date results. Additionally, we are increasing our adjusted EPS guidance due to the impact of our third quarter and planned fourth quarter share repurchases and a lower full year effective tax rate outlook. We currently project total 2026 sales in the range of $14.0 billion to $14.2 billion compared with our previous guidance of $14.0 billion to $14.3 billion. 
Starting with foreign currencies, our guidance now assumes an expected full year sales benefit of $250 million compared with 2025 due to the strengthening of the euro and the renminbi versus the U.S. dollar. This benefit is modestly higher than our previous guidance. 
We expect our weighted end markets to be down 1% to 2% for the year, which is a narrower range than our previous flat to down 3% assumption. We expect our light vehicle business, which comprises over 80% of our sales to perform broadly in line with our weighted light vehicle market, consistent with our performance through the first 3 quarters of 2026. 
However, we expect a sales decline in our battery business due to the lack of North American incentives and weaker European demand. We expect this decline to represent roughly a 170 basis point headwind to our year-over-year sales growth. Based on these assumptions, we expect our 2026 organic sales change to be down 4% to down 2.5% year-over-year. 
Now, let's switch to margin. We continue to expect our full year adjusted operating margin to be in the range of 10.7% to 10.9% compared with our 2025 adjusted operating margin of 10.7%. At the midpoint of this guidance, we expect to expand margins on a year-over-year basis, despite a lower production environment, sales headwinds from our battery business and a $10 million to $15 million industrial R&D investment to support our long-term profitable growth. I believe this performance shows our commitment to driving superior short-term business performance, while also ensuring we position the company for profitable growth for years to come. 
Based on this sales and margin outlook, we are increasing our expected full year adjusted EPS in the range of $5.20 to $5.35 per diluted share from our previous guidance of $5.05 to $5.30 per diluted share. This $0.10 per share increase at the midpoint of our guidance is driven by our third quarter and currently planned fourth quarter share repurchases and a decline in our full year effective tax rate. The midpoint of this adjusted EPS guidance represents approximately a 7% increase over our 2025 adjusted EPS and once again demonstrates our focus on consistently driving the earnings power of the company, despite lower industry production. 
And finally, we continue to expect full year free cash flow to be in the range of $900 million to $1.1 billion, building off a strong 2025. With that, that's our 2026 outlook. 
So let me summarize my financial remarks. Overall, we were very pleased with our third quarter results. Our light vehicle sales performance was roughly in line with industry production. However, our light vehicle eProduct sales were $630 million in the quarter or a 33% increase compared with a year ago. We achieved a 20 basis points adjusted operating margin improvement and a 12% increase to adjusted earnings per share on relatively flat reported sales. And our strong free cash flow supported a cash return of approximately $210 million to our shareholders during the quarter. 
Q3 performance once again demonstrated the BorgWarner team's ability to deliver strong financial results in a declining production environment. As we look to the balance of 2026, we intend to remain focused on expanding the earnings power of the company. At the midpoint of our 2026 guidance, we expect another year of adjusted operating margin expansion and adjusted earnings per share growth despite our expectation that market volumes and battery sales will decline and an incremental $10 million to $15 million investment in industrial R&D to accelerate our long-term sales growth. 
Finally, with another year of anticipated strong free cash flow of $1 billion at the midpoint of our guidance, we expect to continue to deploy capital in a balanced manner that rewards shareholders and deliver on our 2026 financial commitments. 
And I'm equally excited by our efforts to grow our technology-focused portfolio in automotive and other adjacent markets. By continuing to focus on near-term execution, growing the long-term earnings power of the company through organic and inorganic investments, and following a disciplined and balanced approach to deploying capital, we believe BorgWarner will create significant shareholder value for many years to come. 
With that, I'd like to turn the call back over to Pat.

**Patrick Nolan** (Executives):
Thank you, Craig. Nick, we're ready to open it up for questions.

**Operator** (Operator):
[Operator Instructions] The first question will come from Chris McNally with Evercore.

**Chris McNally** (Analysts):
So look, congrats on another good quarter in tough times and really do appreciate the continued color on progress of all the industrial initiatives. Maybe if I could play the buy-side voice for just a second. There's clearly lots of excitement around where these 3 industrial businesses can grow in the coming years. It's going to take some time, 2030 for round numbers to get to some of the bigger numbers that we've all sort of projected out. 
And the direction of travel, I think your comments, the interest, the quoting, the engagement all moving forward. I wanted to see if you could maybe give us some idea about when we'd have more clarity of sort of the shape of that travel, the $300 million in 2027 rev, what that could become in '28, for example. Is that the type of certainty you think will come over the next 6 months? Or is that too hard to say at this point because there's too many moving pieces?

**Joseph Fadool** (Executives):
Yes. Chris, this is Joe. So first of all, I would say we're really pleased with the progress we're making in the quarter. I mentioned some of the highlights. One additional thing, our hiring to support the start of production is also in line with expectations. So I'm really pleased with the progress. We continue to see the backlog and demand for this turbine generator to be very strong. We won't be giving you any kind of color until we get into early 2027. We'll do our best to provide you a little bit more shape of the curve, as you call it, but a little bit too early for that.

**Chris McNally** (Analysts):
Okay. Perfect. And then my follow-up is basically around the sort of the second derivative of your customers within power gen. Any comments if you're seeing any issues from your data center partners around any of the sort of industry timing permitting delays that we're kind of broadly hearing about within data center build-outs across the U.S. Is that in any way affecting negotiations? Or is that something that's not an issue for you guys?

**Joseph Fadool** (Executives):
Yes. So as we stated, the quoting activity is very strong. We generally see some of the current political environment is possibly slowing the finalization of some of the program awards or program agreements. But overall, the activity is there and the workup on these final agreements remains really high. So we see this as probably a very short-term issue. We're looking beyond the midterm. Long term, we don't see any change in the demand.

**Operator** (Operator):
The next question will come from Dan Levy with Barclays.

**Dan Levy** (Analysts):
Maybe we could just start with just the near term and the trend revenue outlook. And maybe we could just project that into 2027. I believe your prior commentary was for some outgrowth or some modest outgrowth on the core automotive business as you have all of this business launching. I want to confirm that's still the case. So guidance this year and then just on the launch of the backlog next year.

**Craig Aaron** (Executives):
Yes. So maybe I'll talk about Q4 and then we can touch on 2027. So when you look at Q4, and I'll walk it from our average for Q1 through Q3. Revenue Q1 through Q3 on average was about $3.55 billion. As we look at Q4, we see it being closer to $3.43 billion. So down about $123 million. That's really a reflection of industry production in the quarter. From a margin perspective, we expect a decrement in the mid-teens on that lower revenue. And then, we have $10 million industrial R&D in the fourth quarter. So that's how you get to the midpoint of our guide. 
As we think about 2027 and the top line, I'd say right now, as we sit here today, we do see some industry headwinds. A couple of those are just higher interest rate environment, vehicle affordability are things that we're watching. With that said, our goals for BorgWarner remain the same. What we expect as we move into 2027 from a top line perspective is we expect to see modest growth over market as it relates to our automotive business. 
We won a lot of awards over the last 2 years, and we expect to see some of those wins in our P&L as we move to 2027. And then we expect to see $300 million of turbine generator revenue. So excited to get to 2027 and see an upswing in our top line for BorgWarner.

**Dan Levy** (Analysts):
Great. My second question is on the microgrid inverter where I think you put out a couple of updates here on, you're starting quoting and you're shipping more testing samples to additional customers. And I think this maybe also pairs with, we saw some news about entering into a multiyear supply agreement with one of the silicon carbide suppliers. And we know that your core inverter technology, there's a significant technology move. So maybe you can just help us understand how large the potential opportunity here and the technology moat that you have? And maybe just weave in how much the silicon carbide is sort of an unlock of that, if at all?

**Joseph Fadool** (Executives):
So great question. We're, first of all, really excited about the fast progress our team is making on these inverter products. If you think about a year ago, we weren't even talking about these products. So to see where that business is poised right now is really exciting. It is true that we're leveraging heavily the light vehicle technology. So in light vehicles, as a reminder, we use both silicon and silicon carbide technology and some of the more advanced EVs are using 800-volt as the, let's just call it, the architecture across the car. This is exactly what we are leveraging to bring more efficiency, more competitiveness into these microgrid inverters. 
So the fit is very strong between light vehicle and industrial. And if you step back a little bit, if you look at the 3 product family offerings: power gen, power conversion, energy storage, this is a family of products that can play on their own, but there's also a lot of system synergy between them. 
The name of the game with the speed to compute is making it more efficient, lower carbon and the more efficient it is, that means less power is lost and can be used for compute. So we're excited about how we're leveraging that into the space. And yes, we're going to reuse many of the automotive suppliers, including the folks that supply silicon and silicon carbide.

**Operator** (Operator):
The next question will come from Joseph Spak with UBS.

**Joseph Spak** (Analysts):
Thanks for some of that preliminary color for '27. I guess, I wanted to maybe pick up a little bit there and really not on '27 specifically, but just over the midterm because you used to really talk about how you've immunized the portfolio against powertrain a lot. And you still mentioned it, right, but it's been a little bit quieter on that front, I'd say, over the past year. But now we've obviously seen some acceleration in electrified powertrains, particularly in Europe. 
And you did highlight eProduct growth in Europe this quarter, but -- and you also sort of mentioned some Foundational product clients in China. So I guess maybe you could just sort of refresh us your thinking about how you see that balance between Foundational and eProduct mix impacting BorgWarner's auto business over the coming years? And maybe if you even could talk about it by Europe versus China.

**Joseph Fadool** (Executives):
Sure. Thanks, Joe. So let me start with our portfolio, which is highly resilient. When you look across the portfolio, we're a market leader in all of our foundational products. We have a fast-growing and scaling eProduct business. Really pleased with the 33% increase year-over-year in eProduct sales, which is really evidence of all the hard work our teams have been putting in and those business awards are starting to pull through. 
Now as Craig mentioned, that's primarily in Europe, which kind of makes sense. If you look at the increased penetration of hybrids and EVs in Europe, that is where the growth is at the moment. So we're starting to see that play through our P&L. A couple of other good examples. You've probably noticed a lot of eMotor awards over the last 12 months, including some of the new technology like aluminum-wire motors. This is just clear evidence that BorgWarner is a leader in this space. 
Many of those are in China where the music has been playing for quite some time on both hybrids and EVs. So from our standpoint, our portfolio is positioned well. The regions are playing out a little bit differently when it comes to adoption of EVs. But as you see EVs accelerate, you can see that it's driving some increased sales in the eProducts sales side.

**Joseph Spak** (Analysts):
Okay. So it sounds like your big picture view is that, that sort of balance between the two is still sort of -- you're sort of indifferent from -- at least from a sales perspective as to sort of how that will play out. You think the portfolio properly protects you?

**Joseph Fadool** (Executives):
That's true. Not only in the portfolio. Just as a reminder, we have probably the most diverse customer portfolio of anybody in the powertrain space. So we think that positions us well. Even as some of the Chinese OEMs have been growing, we've been seeing some benefit from that as they export more to other markets like in Europe because a lot of those vehicles have more technology riding along. So yes, we think we're in a great position to capitalize on the growth as it comes.

**Joseph Spak** (Analysts):
Okay. On the Power Gen side, I know you mentioned sort of multiple hyperscaler engagements. And then to the earlier question, you sort of talked about some maybe like near-term noise on some of the politicalization, if you will. There's also sort of been industry noise around NeoClouds and their ability to fund and capital. And I'm curious if you could sort of just talk about that subset of opportunity, whether there's been any interest shift there or you would sort of classify it as similar to sort of how you classify the hyperscaler engagement?

**Joseph Fadool** (Executives):
Yes. I wouldn't say we see any specific challenge with some of the issues that we hear around the NeoCloud players. I mean, as many people know, the NeoClouds are strictly focused on AI data centers versus our products, they serve all types of data centers. So edge data centers, co-locators, in addition to the hyperscaler data centers, some of which are handled on their own, some of which go through NeoCloud players. But there's many players out there. And if I step back, I don't see any change in the demand for our products. If anything, we continue to see an increase in a lot of the quoting activity. So pretty optimistic about the future here.

**Operator** (Operator):
The next question will come from Emmanuel Rosner with Wolfe Research.

**Emmanuel Rosner** (Analysts):
Just a quick follow-up on your Q4 math there. Not looking to nitpick just sort of to better understand the framework, but I think you were talking about $140 million lower revenue versus the first 3 quarters of the year rate at 15% decremental. But then there's also $10 million in higher R&D. Now in recent past, past couple of years or so you've sort of prided yourself a lot to being able to incorporate all these investments within sort of like the regular incremental and decremental. Is there anything -- is the framework changing? Or is there anything in particular about the investments needed in the fourth quarter that sort of like make you call it out?

**Craig Aaron** (Executives):
No, nothing is changing. So when you go back to our July discussion and guide, I'd say the second half is playing out as we expected, came in a little bit better in Q3. We -- due to recoveries in Q4, we were being impacted by some industrial and R&D. But I would say, overall, the second half is playing out just like we expected. 
Just to refine some of your numbers, Emmanuel, $120 million is the revenue decline versus our Q1 through Q3 average to Q4, so down, call it, 4-ish percent. Again, you're right, we expect a decrement in the mid-teens. And as we talked about in our July call, we expected $10 million to $15 million in incremental industrial R&D in the back half of the year. We saw $5 million of that in Q3. We expect $10 million in Q4, and it's to support the quoting activity that Joe spoke about. We're really bullish about that business, and we're happy to support it with some incremental R&D.

**Emmanuel Rosner** (Analysts):
Okay. Understood. And then turning to some of your non-auto business. Could you provide us a framework on how to think about the size of the inverter opportunity, just either what are sort of like the average content per vehicle that you're starting to quote or what is like a normal or range of sizes of business. So it feels like for the other 2 projects, we have actually a little bit of a framework around what capacity installed is or what available battery capacity is. For this one, it's a little bit earlier stages. So curious if you can help us there.

**Joseph Fadool** (Executives):
Sure. So it is earlier stage and what we're really focused on right now is our first and second business awards upon which we'd be happy to provide you more color on the TAM for those products. I think what's exciting this quarter, what we announced is a new product that we're developing this power supply unit, which actually goes inside of the data center. The microgrid is outside, which they call the grid space, and the PSU is inside, typically right next to the computer servers. So we're excited about that expanded TAM, and we'll provide you more color after we win our first few awards.

**Operator** (Operator):
The next question will come from Tom Narayan with RBC.

**Gautam Narayan** (Analysts):
I note that you said we're going to get more detail on the $300 million launch year turbine generator system sales. Just curious if we could get any color on -- are these like active discussions kind of potentially signed contracts? Just in terms of the progress there, I know you talked about hiring, but anything more concrete on how those discussions are faring? And then I have a follow-up.

**Joseph Fadool** (Executives):
So we -- if I go back a little bit, we do have a signed agreement with Endeavour. They are our go-to-market partner on this. And their role in this beyond some of the IP they carry is mainly the customer intimacy and serving the customers directly. So as we stated, the backlog and the quoting activity is an open book. 
Our teams operate as more or less one team here so that we can see the activity. They're the ones that coordinate the on-site visits from the hyperscalers, and that continues. So we're really, I would say, encouraged by the continued support here. So from our standpoint, we're probably more bullish now than we were 3 months ago because we're making progress against our plan. But as we stated, we'll be able to give you a little more color as we get into early next year.

**Gautam Narayan** (Analysts):
Got it. And thanks for the commentary on Europe and the EV growth and how that's impacting. Just curious if you're seeing a benefit on the hybrid side in the U.S. that's picking up a lot of growth there. And then if I could just sneak in how you think about debt paydown versus buybacks, and you guys did a big paydown in Q3 and your gross leverage around, I think, 2x. Just curious what your target leverage is and how you think about debt pay down.

**Joseph Fadool** (Executives):
Sure. I can take the hybrid question. So the immediate hybrid growth you see in the market, mainly from the Japanese players, where BorgWarner is strong is on these advanced hybrids. So plug-ins, for example, range extenders, which are some of the awards we've won, but haven't come to market yet in North America.

**Craig Aaron** (Executives):
Sure. I can take the tender one. Really pleased with the execution of our debt tender in the third quarter. Our gross net leverage target is 2.0x. Right now, we're at 1.5x. But when you think about the debt tender, it was EPS accretive, it was NPV positive. We're using every lever at our disposal to grow the earnings power of the company, and this is a great example of that. As you think about share repurchases, really pleased with our execution in the third quarter, $175 million in shares repurchased. We expect the same level in Q4. And when you take a big step back, we're excited about $1 billion of free cash flow generated again in 2026, and we're on target to distribute 70% of that to shareholders between share repurchases and dividends. But the balance of the discipline that the team is executing against, and we're excited to wrap up the year.

**Operator** (Operator):
The next question will come from James Picariello with BNP Paribas.

**James Picariello** (Analysts):
Just to focus on the PowerDrive segment, the EBIT loss was only $5 million on very strong growth, which was called out already. But did the quarter have any onetime recovery benefit at all? Or are we getting close to a breakeven run rate here at $700 million plus in quarterly sales? Because I assume the $5 million of additional R&D commitment hit the PowerDrive segment as well. If you could confirm.

**Craig Aaron** (Executives):
Yes. So thanks, James. I'll start with the top line. As we both mentioned, really pleased with the growth in that business unit quarter-over-quarter. It was about 20% on a reported basis. But when you look at light vehicle eProducts growth, again, primarily in Europe, it was 32%. So outstanding growth. We were able to capitalize that, convert at an incremental conversion of about $0.24 on the dollar. So that was great to see. There was a volume recovery in that Q3 figure. And if you go back to last year, we had a volume recovery in Q4. So just another data point between Q3 and Q4. 
As we look forward for that business, we expect to see about 20% growth this year, coming off 30% growth last year. So we really like the trajectory of that business, and we're excited to get into 2027 and continue to capitalize on that. Our objective for that business unit remains the same, convert in the mid-teens on a year-over-year basis, and we're on track to do that this year.

**James Picariello** (Analysts):
Got it. That's helpful. And then my follow-on -- my two quick follow-ons. As we think about the company's microgrid inverter development, I know it's early, but you guys are actively quoting the product. Any sense for what the margin profile could be similar to the confidence in turbine generators immediately contributing at a mid-teens margin profile? Are there any parameters to think about a future microgrid inverter award? 
And can you help us clarify the U.S. ban of foreign-sourced equipment for the electric grid? Because it sounds as though the products listed within the executive order cover all 3 product categories that you're trying to enter. So just curious if you have -- I'm just wondering if you have any thoughts to share on what the implications and timing might look like for that ban.

**Joseph Fadool** (Executives):
Yes. This is Joe. Maybe I can start with the executive orders. So it is true there were some orders issued and some of the scope of those orders has grown throughout the year. We're still getting clarification on those orders. From us, it doesn't matter if those orders are there or not. It would provide a nice tailwind since we're a U.S.-based company, we're going to produce these electronics in the U.S. But besides the FEOC executive order, our products are still extremely innovative, competitive and provide a lot of value to our customers based on the feedback we're getting from the 7 customers. 
I'll let Craig answer the margin profile.

**Craig Aaron** (Executives):
Yes. So James, I mean, we're obviously in the quoting phase. But I think the way to think about the microgrid is very similar to the TG. What we said for next year is we expect mid-teens conversion on that first year of launch. We expect some inefficiency in the process as we get -- as we build out that plant, as we get -- as we gain supply chain savings and higher OEE coming off our lines. So I would expect the same thing as we get to year 1 launch of the microgrid, but we believe that there's upside potential as we move forward off of that mid-teens incremental base.

**Operator** (Operator):
The next question will come from Mark Delaney with Goldman Sachs.

**Mark Delaney** (Analysts):
The input cost environment has been very challenging for several companies in the automotive industry so far this quarter. Recognize the good margins that BorgWarner was able to put up and guide to for this year. But can you talk a little bit more on what you're seeing in terms of input costs? And as you start to look into 2027, I'm not sure if you're starting to see input costs rising to an extent that maybe you haven't seen yet in '26, but may become more problematic in '27 and perhaps could create more challenging incrementals as you try and deal with that next year.

**Craig Aaron** (Executives):
Got it. Thanks, Mark. We are seeing some inflation, especially on the electronics side of our business in 2026. The good news is the teams are doing a fantastic job, and we think we can manage it within our incremental conversion for this year. As we go into next year, we're going to watch it really closely to the extent that we do experience those higher costs, we're going to manage them just like we have in the past, whether it's been previous inflationary environment, tariffs, et cetera. We're not going to get caught in between our supplier and our customers, and we'll manage it appropriately. But right now, we are seeing a bit higher inflation costs on the electronics side of our business.

**Mark Delaney** (Analysts):
Understood. My other question was on capital allocation and a fair amount of discussion already around the free cash flow generation of the business and your plans around how much you want to return to shareholders. Could you also touch on the potential for M&A? I know the company has previously articulated several key criteria any deal would need to meet. Any update around the funnel and the likelihood of deals being completed over the near to medium term?

**Joseph Fadool** (Executives):
Mark, we still remain active seeing M&A as a lever for us to expand the earnings power of the company. As we've stated in the past, you can count on Craig and I for a very disciplined approach. And those 3 criteria as a reminder, we want to leverage our core. So what are we really good at? It needs to make industrial logic. 
The second is we're looking for near-term accretion to any asset. And then finally, we don't want to overpay. We want to value the asset properly. It's these criteria that sets quite a high bar for us. But I would say we've opened our aperture. We're looking inside automotive. We're looking outside automotive. What I'm really pleased about is we're applying the same discipline that we have in our operational business to our M&A side of the business. And sometimes the best decisions are the assets you don't purchase. So I'm pleased with the pipeline. But of course, we will move on something that fits those 3 criteria.

**Operator** (Operator):
The next question will come from Andrew Percoco with Morgan Stanley.

**Andrew Percoco** (Analysts):
Maybe just to come back to the turbine generator. I know a lot has already been discussed, but it's clear that based on your discussions and your presentation that the customer interest has definitely picked up, which obviously makes sense given the environment that we're in. But I'm just curious if you could just maybe provide a little bit more insight into -- or information into what the dialogue is with those customers? What are they asking you? What do they want to see? Obviously, like the power shortfall is very well advertised. But when they're looking at your technology specifically, I'm just curious if you could provide a little bit of insight in terms of what they are asking most frequently? Is it efficiency? Is it durability? If you could just kind of bring us into those conversations a little bit, I think that would be really helpful.

**Joseph Fadool** (Executives):
Andrew, a little bit of color on the TG first, and maybe I can even touch on some of the other products. So many of the visits we received at our Arden R&D facility, especially the hyperscalers, these are engineer-to-engineer discussions. So the customers are focused on, first, are we able to meet the requirements that we've set for ourselves and that they may have. How are we managing the tolerances and the built-in quality and robustness? Uptime is a big topic, of course, for any kind of stationary power. So reliability is important. 
And then, of course, they want to understand the efficiency and emission profile of these. What's really important to hyperscalers is a sustainable solution that puts out lower carbon than diesel and other solutions. So these are typically the dialogues that we are having with them, and they're very deep and we're pouring over drawing specifications. 
More recently, we're looking at test results. We're seeing the units perform, including at some third-party sites, which Endeavor organizes those visits. As we look beyond TG, we talk about battery and inverter. For battery, we have a really built-in advantage with this capacity that's installed. So we're not using all that capacity for the CV and eBUS market. So we're able to get to market quickly with that because there are some constraints on energy storage in the market. 
And then on the inverter, it has a lot to do with the technology and the conversion efficiency. This is a big deal because the more efficient that inverter is, the less power they need to drive the data center. 
I would say the last thing which applies to all 3 speed to market is everything right now. And we know that having this automotive mindset where we can stand up manufacturing, leverage our supply base, we can get to market in 18 to 24 months, typically, which is about half the time of some of the industrial competitors.

**Andrew Percoco** (Analysts):
That's super helpful. I appreciate that. And maybe just a follow-up on energy storage. One of your competitors who reported recently on energy storage, there was a pretty significant kind of about-face in terms of what they're thinking on pricing or just the pricing environment that they're seeing within data centers being a much more lucrative or higher margin than maybe expected a few months ago. I know you're just maybe an earlier stage kind of quoting or negotiations there. But can you corroborate that? Are you seeing a more favorable maybe pricing environment on the energy storage side than you maybe anticipated a few months ago?

**Joseph Fadool** (Executives):
Yes. I don't know if we are ready to comment on that. What I would say is, there is very strong demand for energy storage, and we're focused on leveraging the capacity we have. So I think our team is focused on our first win and making sure we can bring that to the market. We can probably provide you a little more color next year as we get into 2027.

**Operator** (Operator):
The next question will come from Alex Perry with Bank of America.

**Alexander Perry** (Analysts):
So I just wanted to follow up on some of the key bridge items for next year that we should be thinking about on the cost side. Are there specific initiatives that you have in place that could help offset some of these cost pressures and the commodity headwinds that you're seeing? And then the incremental industrial R&D investment that you incurred this year, is that something we should be thinking about continuing going forward?

**Craig Aaron** (Executives):
Yes. Alex, I would say this year is a great example of what BorgWarner can do in a down production environment. We're expanding margins year-over-year, inclusive of that industrial R&D and things like supply chain savings and productivity in our plants are great examples of what the teams have been executing to achieve that result. 
As we move into next year, we're going to continue to focus on those same things, and our goals remain the same. We'd like to see growth over market in our automotive business, at least modest growth over market. We'd like to see $300 million in future revenue, and we'd like to see mid-teens conversion of extra growth. So we're really excited to move from a no-growth environment to a growth environment and really see what we can accomplish as a company.

**Alexander Perry** (Analysts):
Really helpful. And then my follow-up is just on China. Could you talk through your outlook for the region a bit more? It looks like you took your production outlook down there a bit. How are you positioned with some of the OEMs that are having higher export volumes? And any signs of the China market improving?

**Joseph Fadool** (Executives):
Yes. So I'll take that one. In China, we expect the overall market to be down between 6% and 8% this year, although we do see higher export volumes despite that. So from our book-of-business in China, we've been there over 30 years. We have a great mix of customers there. 70% of our China OEM business there, in fact, is with the leading 6 or 7 OEs and most of them are the export champions. So we're feeling pretty good about where we're positioned there and including as they start to move to localize in some of these other markets, you talk about Europe, you talk about South America, we're highly engaged with them to support some of their localization efforts. So we see it as a win in the short term and also a win in the long term.

**Operator** (Operator):
We have time for one final question, and that question comes from Rajat Gupta with JPMorgan.

**Rajat Gupta** (Analysts):
Just wanted to follow up from the last question. The recent news around restricting exports from China on hybrids, a quota system. I'm curious, like, how does that net out for Borg? Presumably, I would -- it would seem like it would be a net positive, protecting some of your legacy European customers on the content there. But curious to get your thoughts on if that actually plays out, how it would impact your growth profile in those regions? And I have a quick follow-up.

**Joseph Fadool** (Executives):
Raj, so our customer diversity is one of our strengths. So what we tend to see is when one customer loses another customer wins, and you really hear us talk about customer mix on the call for that reason. So we'll have to see how it plays out, but I don't anticipate this is something we're going to be highlighting in the future.

**Rajat Gupta** (Analysts):
But if I look at just like content on your exports from China to Europe versus just the hybrid content in Europe, is there a material difference there that we should think about if this turns out to be a more long-term move to restrict exports?

**Joseph Fadool** (Executives):
Yes, I would say on comparable vehicles, there's no difference.

**Rajat Gupta** (Analysts):
Understood. And just quickly on commercial, not a lot of talk about that on the call. We've seen some of your peers report see pretty healthy growth in their commercial business and kind of offsetting some of the light vehicle industry weakness. Just any update on that would be helpful in any preliminary view on '27 on that end market.

**Joseph Fadool** (Executives):
Sure. So from a market perspective, there is some growth globally, about 3% in CV overall. Most of that is led out of North America with about 11% growth. Ex battery business, we do see about mid-single-digit sales growth there. It's a little bit too early to comment in 2027, but we'll be able to give you some more color when we get there.

**Patrick Nolan** (Executives):
With that, I'd like to thank you all for your questions today. If you have any follow-ups, feel free to reach out to me or my team. With that, Nick, you can go ahead and conclude today's call.

**Operator** (Operator):
Thank you. This concludes the BorgWarner 2026 Third Quarter Results Conference Call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### BWA_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO Craig Aaron｜guidance：CFO 說明全年銷售、調整後營業利益率與自由現金流財測維持不變。（原話："adjusted operating margin and free cash flow guidance"）
- 2026-08-05｜CFO Craig Aaron｜guidance：全年調整後 EPS 財測上調為 $5.05 至 $5.30（原為 $5 至 $5.20）。（原話："$5.05 to $5.30 per diluted share"）
- 2026-08-05｜CFO Craig Aaron｜guidance：2026 全年銷售財測區間 $14.0B 至 $14.3B，維持不變。（原話："sales in the range of $14.0 billion to $14.3 billion"）
- 2026-08-05｜CFO Craig Aaron｜guidance：全年調整後營業利益率財測 10.7% 至 10.9%。（原話："range of 10.7% to 10.9% compared to our 2025"）
- 2026-08-05｜CFO Craig Aaron｜guidance：全年有機銷售變動財測為下滑 3.5% 至下滑 1.5%，與先前展望一致。（原話："sales change to be down 3.5% to down 1.5% year-over-year"）
- 2026-08-05｜CFO Craig Aaron｜guidance：全年自由現金流財測 $900M 至 $1.1B，維持不變。（原話："range of $900 million to $1.1 billion"）
- 2026-08-05｜CFO Craig Aaron｜risk：電池業務因北美缺乏誘因與歐洲需求偏弱而下滑，估計拖累全年銷售成長約 170 bp。（原話："this decline to represent roughly a 170 basis point"）
- 2026-08-05｜CFO Craig Aaron｜margin：利潤率財測低端所隱含的全年 decremental conversion 假設。（原話："a full year decremental conversion in the low double digits"）
- 2026-08-05｜CFO Craig Aaron｜margin：利潤率財測高端的假設：以進一步成本控制大致抵銷有機銷售下滑。（原話："At the high end, our outlook assumes we largely offset"）
- 2026-08-05｜CFO Craig Aaron｜margin：Q2 利潤率年增 100bp 的拆解：基礎業務 60bp。（原話："60 basis points came from strong performance"）
- 2026-08-05｜CFO Craig Aaron｜margin：Q2 利潤率拆解：BES 重組與退出充電業務貢獻 20bp。（原話："We had 20 basis points of enhancement through BES"）
- 2026-08-05｜CFO Craig Aaron｜margin：Q2 利潤率拆解：成本控制貢獻最後 20bp。（原話："And the final 20 basis points came from"）
- 2026-08-05｜VP IR Patrick Nolan｜margin：管理層對 incremental margin 的定義（有機調整後營業利益變動除以有機銷售變動）。（原話："Our incremental margin is defined as the organic change in"）
- 2026-08-05｜VP IR Patrick Nolan｜margin：管理層對 market 的定義：依地理曝險加權的輕型車產量變動。（原話："that means the change in light vehicle"）
- 2026-08-05｜CFO Craig Aaron｜margin：Q2 有機銷售增加 $18M（0.5%），略優於輕型車產量下滑。（原話："organic sales increase of $18 million, 0.5%"）
- 2026-08-05｜CFO Craig Aaron｜margin：CFO 說明排除充電業務退出與匯率後的 Q2 營業利益變動口徑。（原話："Excluding this benefit and FX impacts"）
- 2026-08-05｜CFO Craig Aaron｜margin：下半年銷售橋接：較低營收下的 decremental 約中段十幾 %。（原話："On those lower revenues, we're decrementing at"）
- 2026-08-05｜CFO Craig Aaron｜margin：下半年利潤率：不含工業 R&D 增加為 10.8%。（原話："our margin would be at 10.8%"）
- 2026-08-05｜CFO Craig Aaron｜margin：下半年利潤率：含工業 R&D 中點為 10.6%。（原話："industrial R&D at the midpoint, we're at 10.6%"）
- 2026-08-05｜CFO Craig Aaron｜commitment：下半年工業 R&D 增加 $10M 至 $15M，同時維持全年利潤率財測。（原話："investing an incremental $10 million to $15 million"）
- 2026-08-05｜CFO Craig Aaron｜commitment：管理層承諾在增加 R&D 的同時維持全年利潤率財測。（原話："while maintaining our full year margin guidance"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：CEO 回答增加的 R&D 是否持續時表示開發開始後會有一定程度的持續支出。（原話："you can expect to have some level of"）
- 2026-08-05｜CEO Joseph Fadool｜capital_allocation：董事會將庫藏股授權增加 $1B。（原話："approved a $1 billion increase to our current share"）
- 2026-08-05｜CFO Craig Aaron｜capital_allocation：合併原授權剩餘 $350M 後，可回購總額達 $1.35B，約市值 10% 以上。（原話："$1.35 billion of the company's outstanding shares"）
- 2026-08-05｜CFO Craig Aaron｜capital_allocation：過去四季回購約 $650M，原授權剩餘 $350M。（原話："$650 million and leaves $350 million remaining"）
- 2026-08-05｜CEO Joseph Fadool｜capital_allocation：CEO 表示將優先進行有機投資（R&D 與 CapEx）。（原話："we will always prioritize these organic investments"）
- 2026-08-05｜CEO Joseph Fadool｜capital_allocation：M&A 維持三項準則（核心競爭力、近期增益、不多付）。（原話："we're sticking to the 3 criteria"）
- 2026-08-05｜CEO Joseph Fadool｜capital_allocation：CEO 表示 M&A 門檻已經提高。（原話："we've really raised the hurdle in terms of any decision"）
- 2026-08-05｜CEO Joseph Fadool｜product：渦輪發電機測試已達 CARB 等級排放標準。（原話："we have achieved CARB-level emission standards"）
- 2026-08-05｜CEO Joseph Fadool｜product：UL 零組件認證預計 9 月開始。（原話："certification is expected to start in September"）
- 2026-08-05｜CEO Joseph Fadool｜product：渦輪發電機組裝廠設備預計第三季開始安裝。（原話："capital equipment installation to begin in the third quarter"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：電池儲能系統預計 2027 年量產就緒。（原話："we expect to be production ready in 2027"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：CEO 表示預期今年會有部分電池儲能訂單。（原話："We do expect to see some battery awards this year"）
- 2026-08-05｜CEO Joseph Fadool｜product：微電網逆變器已有四家客戶取得樣品。（原話："Four customers now have BorgWarner samples"）
- 2026-08-05｜CEO Joseph Fadool｜guidance：渦輪發電機產能：宣布安裝 2 吉瓦產能。（原話："we're installing 2 gigawatts of capacity"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：CEO 對明年約 $300M 工業營收表示有信心。（原話："which we're very comfortable with next year"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：渦輪發電機產能是否追加，管理層預計下半年做決定，尚未定案。（原話："So no decisions made yet"）
- 2026-08-05｜CEO Joseph Fadool｜product：渦輪發電機使用情境與早先預期相反：近 12 個月轉為以主電源（prime）為主。（原話："that's flopped, and we see more of them in prime use"）
- 2026-08-05｜CEO Joseph Fadool｜customer：針對 Koch 可能出售 Edged 股權的報導，管理層表示協議中無控制權變更觸發條款。（原話："nothing in our agreement that triggers change in control"）
- 2026-08-05｜CEO Joseph Fadool｜risk：對 Endeavour 夥伴 Koch 的新聞，管理層認為不會實質改變雙方關係。（原話："we don't think it materially changes anything"）
- 2026-08-05｜CEO Joseph Fadool｜competition：VCT 在中國取得 1.5L 渦輪汽油引擎新案，取代原有供應商。（原話："replacing the previous incumbent supplier"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：CEO 預期新訂單將支持 2027 年 outgrowth 的改善。（原話："improvement in our objective in outgrowth across portfolio in 2027"）
- 2026-08-05｜CEO Joseph Fadool｜competition：CEO 公開表示對目前 outgrowth 表現不滿意，並稱因此調整了策略。（原話："Craig and I are not pleased with the current outgrowth"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：CEO 表示預期這些訂單會改善公司 outgrowth。（原話："we're clearly expecting that they're going to improve the outgrowth"）
- 2026-08-05｜CEO Joseph Fadool｜customer：中國占全球銷售約 20%。（原話："China is about 20% of BorgWarner's global sales"）
- 2026-08-05｜CEO Joseph Fadool｜risk：管理層對中國產量的預期區間：下滑 4% 至 7%。（原話："China, likely to be down 4% to 7%"）

### 問答異常語氣（迴避／改口／保留）
- BWA_Q2_2026_Earnings_Call_20260805.md｜問：Spak：EBIT 較預期高近 $40M、R&D 只增 $10–15M，其餘 $25–30M 是否為較高成本？｜答法：CFO 未直接回答差額去向，改談上下半年營收橋接與利潤率（10.8% vs 10.6%）。
- BWA_Q2_2026_Earnings_Call_20260805.md｜問：Picariello：BES 上半年虧損僅 $4M，遠優於 mid-teens decremental，下半年如何橋接？｜答法：CFO 以重組與充電業務退出帶過，未解釋差距，僅重申下半年管理在 mid-teens decremental。
- BWA_Q2_2026_Earnings_Call_20260805.md｜問：Percoco：渦輪發電機訂單到交貨是否少於 6 個月？｜答法：CEO 表示未揭露交期且不打算談，改稱目前重點在 2026 年的產品上線。
- BWA_Q2_2026_Earnings_Call_20260805.md｜問：Perry：電力產品營收可擴大到多少、EBIT 貢獻如何估算？｜答法：CEO 只重申明年 $300M，未給 EBIT 或營收對產能比，稱可能未來再分享。
- BWA_Q2_2026_Earnings_Call_20260805.md｜問：McNally：電池儲能典型合約規模有無經驗法則？｜答法：CEO 稱沒有經驗法則、每案客製，僅說任何超大規模客戶訂單都會相當可觀，不給數字。
- BWA_Q2_2026_Earnings_Call_20260805.md｜問：Rosner：逆變器的產能與投資規模？｜答法：CEO 表示未宣布產能計畫，待年底報價後再評估，2027 年才可能分享。

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

## ⑥ 條件附卡（archetype_hint='循環/商品' 命中）：judge_addendum_cyclical.md

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
{"date":"20260524","verdict":"B｜衛星候選｜等 W52 拉回 $46-50 後分批進場；近 4 月 +60% 短期 stretched，估值燈 🟡 不急建倉","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"eProducts 達成 25% revenue mix（2027 target）+ margin ≥ 8%","columns":{"2Y 驗證":"FY 27 eProducts revenue ≥ $4.3B + OPM ≥ 8%","5Y 驗證":"FY 30 eProducts revenue ≥ $6B + OPM ≥ 10%","10Y 驗證":"2035 eProducts ≥ 40% mix + OPM 等同集團","數字門檻":"FY 27 eProducts $4.3B（公司公開 target）+ implied margin ≥ 8%","信息來源":"公司 2025 投資人日 + Capital Markets Day 2024-06","漂移觸發":"連 2 季 eProducts revenue YoY &lt; +15% → 削弱（2Y 假設）"}},{"id":"H2","text":"Adj OPM 結構維持 10-11% mid-cycle","columns":{"2Y 驗證":"FY 26 Adj OPM 10.7-10.9% （公司 guidance）","5Y 驗證":"5Y 平均 Adj OPM ≥ 10.5%","10Y 驗證":"無 mean reversion 至 9% 以下","數字門檻":"FY 26 ≥ 10.7% / FY 27 ≥ 10.7% / FY 28 ≥ 11%","信息來源":"2026-02 公司 guidance","漂移觸發":"連 4 季 OPM &lt; 9.5% → 削弱（5Y 假設）"}},{"id":"H3","text":"Data Center turbine generator scale up + free option value 兌現","columns":{"2Y 驗證":"2027 Y1 訂單 ≥ $300M + 2 GW capacity 達標","5Y 驗證":"FY 30 Data Center revenue ≥ $1B（mix &gt; 5%）","10Y 驗證":"2035 Data Center 為第三大業務線（mix ≥ 10%）","數字門檻":"Y1 $300M（公司公開）/ Y3 $800M / Y5 $1.5B","信息來源":"2026-02-11 BWA press release","漂移觸發":"連 2 季訂單 announcements &lt; $50M → 削弱（2Y）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"eProducts margin 永遠卡 6-7%（vs 集團 10.7%）","columns":{"對應假設":"H1 / H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 Adj OPM + 業務段 margin disclosure","警戒閾值":"連 4 季 集團 OPM &lt; 9.5%"}},{"id":"R2","text":"Vitesco-Schaeffler 合併 + 中國 EV 本土化 pricing war","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"eProducts 季度 ASP/W trend + 中國 OEM 自製率","警戒閾值":"跨 2 個年度 eProducts revenue YoY 連續 &lt; +10%"}},{"id":"R3","text":"ICE turbo 加速結構下行（BEV 強滲透）","columns":{"對應假設":"H1 / H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Air Management 業務 organic + BEV 滲透率","警戒閾值":"連 4 季 Air Management organic &lt; -7%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟡","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":65.82,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWA_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
