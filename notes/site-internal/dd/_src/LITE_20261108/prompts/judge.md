你是 stock-analyst **v20 判斷 agent**，標的 LITE（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"LITE","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LITE_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LITE_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_revenue_gaap","label":"Net revenue (GAAP)","value":1262.6,"period":"Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）","citation":"公司新聞稿 investor.lumentum.com Q1 FY27 press release"},"note":"未查證"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":42.3,"period":"Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）","citation":"公司新聞稿 investor.lumentum.com Q1 FY27 press release"},"note":"未查證"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":28.5,"period":"Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）","citation":"公司新聞稿 investor.lumentum.com Q1 FY27 press release"},"note":"未查證"},{"id":"f_kpi4_guidance_q2_fy2027","label":"Guidance: Q2 FY2027","value":"營收 $1.575B–$1.625B；non-GAAP 營業利益率 45.0%–46.0%；non-GAAP EPS $5.90–$6.20","period":"Q1 FY2027 新聞稿（2026-11-02）對 Q2 FY2027 指引","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q1 FY2027 新聞稿（2026-11-02）對 Q2 FY2027 指引","citation":"公司新聞稿 investor.lumentum.com Q1 FY27 press release"},"note":"未查證"},{"id":"f_kpi5_gaap_gross_margin","label":"GAAP gross margin","value":51.0,"period":"Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）","citation":"公司新聞稿 investor.lumentum.com Q1 FY27 press release"},"note":"n/a"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-02","period":"2026-11-02","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-02"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_lite_gross_margin_pct","label":"LITE 毛利率","value":45.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lite_operating_margin_pct","label":"LITE 營業利益率","value":23.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lite_fcf_margin_pct","label":"LITE FCF 利潤率","value":9.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cohr_gross_margin_pct","label":"COHR 毛利率","value":38.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cohr_operating_margin_pct","label":"COHR 營業利益率","value":14.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cohr_fcf_margin_pct","label":"COHR FCF 利潤率","value":-23.28,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cien_gross_margin_pct","label":"CIEN 毛利率","value":44.07,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CIEN.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_cien_operating_margin_pct","label":"CIEN 營業利益率","value":14.12,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CIEN.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_cien_fcf_margin_pct","label":"CIEN FCF 利潤率","value":13.53,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CIEN.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_aaoi_gross_margin_pct","label":"AAOI 毛利率","value":28.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAOI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_aaoi_operating_margin_pct","label":"AAOI 營業利益率","value":-10.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAOI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_aaoi_fcf_margin_pct","label":"AAOI FCF 利潤率","value":-100.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAOI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mtsi_gross_margin_pct","label":"MTSI 毛利率","value":57.13,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mtsi_operating_margin_pct","label":"MTSI 營業利益率","value":18.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mtsi_fcf_margin_pct","label":"MTSI FCF 利潤率","value":9.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_sbc_and_related_payroll_","label":"SBC and related payroll taxes","value":146.7,"period":"Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）","citation":"公司新聞稿 investor.lumentum.com Q1 FY27 press release（含高管退休股權修改 $89.4M、薪資稅 $14.2M；占營收約 11.6%、占 GAAP 營業利益約 40.8%，為本檔換算）"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":538.59,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-40.41,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":29.51,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（24.83 → 24.83）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（39.01 → 39.01）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（54.41 → 54.41）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":24.83,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":39.01,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":54.41,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":14.85,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 21.62 → 24.83（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":13.05,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝68.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":68.7,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":12.9,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝65.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":65.9,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":21.69,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 24.83，分子＝快照價 538.59","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-549.4,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 1430.2、現金 1979.6（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":90.68,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":48292.59,"period":"2026-11-08","unit":"USD m","basis":"市值 48841.99 ＋ 淨負債 -549.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6690.42,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":10473.31,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（22 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":7.22,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟢","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 538.59 / W52 708.13 / W104 404.67 / W250 203.96 / W250 13週斜率 5.25%"},{"id":"f_ma_w52","label":"52 週均線","value":708.13,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":404.67,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":203.96,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":5.25,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：光通訊市場已成熟、日益商品化；既有對手與以亞洲為主的新進入者近年加劇競爭，造成價格壓力。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"Both legacy competitors as well as new entrants, predominantly Asia-based competitors, have intensified market competition in recent years leading to pricing pressure.","as_of":"2026-08-17","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：競爭對手可能以新品或激進低價取得或保住份額，且公司自稱對手中許多資源較大；若供給跟不上需求，可能流失份額。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"Our competitors may continue to enter markets or gain or retain market share through introduction of new or improved products or with aggressive low pricing strategies that may impact the efficacy of our approach.","as_of":"2026-08-17","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"10-K 自述依營收與市占為光子產業領先供應商（公司自述，未附具體份額數字）。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"an industry-leading provider of optical and photonic products based on revenue and market share","as_of":"2026-08-17","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"TrendForce：EML/CW-DFB 雷射供應集中，Lumentum、Broadcom 等合計高占比","source":"LEDinside/TrendForce","url":"https://www.ledinside.com/intelligence/2026/06/2026_06_04_07","excerpt":"Given the high technical barriers, the top three suppliers—Lumentum, Broadcom, and Mitsubishi Electric—collectively hold approximately 72% market share.","as_of":"2026-06-04","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"HyperLight 薄膜鈮酸鋰調變器新進入者，威脅限於調變器而非 InP 雷射","source":"marketanalysis.com","url":"https://marketanalysis.com/the-hyperlight-threat-to-coherent-and-lumentum-ends-where-indium-phosphide-begins/","excerpt":"TFLN takes the modulator, not the engine A transceiver is a light source, a modulator, a detector, and the packaging that holds them together. HyperLight’s chiplet contests one of those four functions. It modulates light it does not generate. The laser still comes from indium phosphide, and that is the function Coherent and Lumentum spent","as_of":"2026-06-19","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2026 10-K 風險因子：客戶的廠商選擇、採購行為變動曾導致對該等客戶銷售下滑或訂單延遲／取消，並可能持續；競爭者可能以低價策略搶市占。未見明確指出最大客戶導入第二供應商或自製的揭露。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"changes in the business requirements, vendor selection, project prioritization, financial prospects, capital resources, and expenditures, or purchasing behavior (including product mix purchased or timing of purchases) of our key customers, or any real or perceived quality issues related to the products that we sell to such customers, have led to decreased sales to such customers or delays or cancellations of planned purchases of our products or services","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2026 10-K：兩大未具名客戶占營收 26.6% 與 15.0%（前一年 15.4%、16.0%）","source":"SEC EDGAR 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0001633978/000162828026057358/lite-20260627.htm","excerpt":"Customer A 26.6 % 15.4 % 18.9 % Customer B 15.0 % 16.0 % 11.4 % International Operations","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 10-K：單一終端客戶 Customer A 占營收 26.6%（FY2025 15.4%、FY2024 18.9%），Customer B 15.0%（FY2025 16.0%、FY2024 11.4%）；兩大客戶合計約 41.6%。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"Customer A 26.6 % 15.4 % 18.9 % Customer B 15.0 % 16.0 % 11.4 %","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"風險因子：公司長期依賴少數客戶，預期集中度持續；多數客戶以採購單下單、無數量或長期承諾，可能無預警改變採購。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"We have consistently relied on a small number of customers for a significant portion of our sales. We expect that this customer concentration will continue in the future","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"應收帳款集中：2026-06-27 兩家客戶分別占應收帳款毛額 30% 與 11%（前一年 13%、11%）。","source":"SEC EDGAR 10-K FY2026 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"As of June 27, 2026, our accounts receivable from a single customer, which represented 10% or greater of the total accounts receivable, was concentrated with two customers, which represented 30% and 11% of gross accounts receivable, respectively.","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"搜尋未找到主要客戶信用評等下調、破產或財務壓力的來源；10-K 客戶名稱匿名，客戶身分僅來自二手媒體推測。","source":"WebSearch 結果彙整（無客戶信用惡化來源）","url":null,"excerpt":null,"as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TrendForce 報導 InP 短缺成為 AI 光互連瓶頸（InP 為鋅冶煉副產品，供給難獨立擴張）","source":"TrendForce News: InP Shortage Emerges as AI Optical Interconnect Bottleneck","url":"https://trendforce.com/news/2026/08/06/news-inp-shortage-emerges-as-ai-optical-interconnect-bottleneck/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce：供應商 2026 年 EML＋CW-DFB 雷射月產能約倍增至 50.7M 顆；Broadcom、Lumentum、Sumitomo 合計約 55% 市占（二手聚合站轉述）","source":"TrendForce press center 2026-06-03","url":"https://www.trendforce.com/presscenter/news/20260603-13077.html","excerpt":null,"as_of":"2026-06-03","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Lumentum CEO 稱 InP 供需缺口已超過 DRAM/NAND","source":"Tom's Hardware","url":"https://www.tomshardware.com/tech-industry/semiconductors/lumentum-ceo-says-the-indium-phosphide-shortage-will-become-worse-than-memory","excerpt":"Lumentum CEO Michael Hurlston told an audience at the RAISE Summit in Paris earlier this month that indium phosphide, the compound semiconductor behind every laser in an AI data center, is heading into a supply squeeze worse than what we've already seen with DRAM / NAND, and that Nvidia's decision to fund Lumentum and its biggest competitor at the same time was a response to","as_of":"2026-07-31","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Lumentum 產能經長約配置至 2027、出貨低於需求約25-30%","source":"Marketbeat Q2 2026 earnings call transcript","url":"https://www.marketbeat.com/earnings/reports/2026-2-3-lumentum-holdings-inc-stock/","excerpt":null,"as_of":"2026-02-03","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"公司 2024-08 收到 BIS 行政傳票與 DOJ 相關傳票，要求提供對華為業務的紀錄；公司持續配合，屬出口管制調查而非反壟斷；未履行出口管制可能面臨罰款、出口權限被拒與政府合約除名。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"In August 2024, we received an administrative subpoena from BIS requesting the production of records in connection with our business with Huawei. We also received a related subpoena from the U.S. Department of Justice (“DOJ”) that also requested information regarding our business with Huawei. We have been, and will continue to, cooperate with BIS and DOJ in responding to the subpoenas and their ongoing reviews.","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因素揭露美國關稅、出口管制與制裁法規可能限制對中國等地區銷售並增加成本；232 條款半導體調查可能帶來新關稅。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"U.S. regulatory activity, such as tariffs, export controls, and economic sanctions laws have in the past, and may in the future, materially limit our ability to make sales to customers in certain regions of the world, including China, and which have in the past, and may in the future, increase our costs and harm our results of operations and financial condition.","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"三次搜尋未發現 2026 年 DOJ/FTC/EU 對 Lumentum 的反壟斷調查或拆分風險；10-K 僅一般性提及反壟斷法可能限制併購。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"In addition, applicable antitrust laws and other regulations may limit our ability to acquire targets or force us to divest all or a portion of our business or an acquired business.","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"因 BIS 對華為的出口限制，公司自 2024 年初起停止對華為（曾為中國最大網通客戶）的所有出貨","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"As a result, we stopped all of our product shipments to Huawei, historically our largest networking customer in China, in the beginning of calendar year 2024.","as_of":"2026-08-17","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"中國對稀土及關鍵礦物實施出口管制，限制公司取得這些材料；中國對日本出口限制亦影響其基板供應鏈","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"China imposed new export control measures affecting exports of rare earth metals and other critical minerals, limiting our ability to access these materials,","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"美國商務部 2025-04-14 依 232 條款啟動調查，可能對半導體等產品課新關稅，對公司影響不確定","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"on April 14, 2025, the Secretary of Commerce initiated an investigation under Section 232 of the Trade Expansion Act of 1962","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"公司部分供應商位於中國，暴露於中美出口管制、關稅與報復措施風險","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"Further, certain of our suppliers are located in China, which exposes us to risks associated with Chinese laws and regulations and U.S. laws, regulations and policies with respect to China,","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"關稅與出口管制可能推高銷貨成本，若無法轉嫁則壓縮毛利率","source":"SEC EDGAR 10-K FY2026 Item 1 / MD&A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"The imposition of tariffs on certain imported goods and materials and export controls on critical components may increase our costs and place upward pressure on the cost of goods sold, which, in turn, may reduce our gross margins if we are unable to pass these costs onto customers through price increases.","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"InP 供需缺口已超過 DRAM/NAND；Lumentum 雖有多座 InP 晶圓廠仍面臨供給短缺（2026 年 8 月報導）","source":"TrendForce News: InP Shortage Emerges as AI Optical Interconnect Bottleneck","url":"https://www.ledinside.com/news/2026/08/2026_08_06_01","excerpt":"Despite operating multiple InP wafer fabrication facilities, Lumentum continues to face widening supply shortages.","as_of":"2026-08-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2023 10-K：自有廠在美、泰、中、英、斯洛維尼亞、日，代工主要在泰、台、馬（搜尋摘要轉述，非逐字）","source":"Lumentum FY2023 10-K","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828023030374/lite-20230701.htm","excerpt":null,"as_of":"2023-08-15","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2022 10-K：製造集中亞洲，且 FY22 Q3 因疫情政府規定中國工廠暫時關閉（搜尋摘要轉述，非逐字）","source":"Lumentum FY2022 10-K","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828022023617/lite-20220702.htm","excerpt":null,"as_of":"2022-08-15","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY26 Q1 (Sep 2025季) 營收 $533.8M、年增58%；Components $379.2M 年增63.9%、Systems $154.6M 年增46.5%；公司已改單一報導部門，雲端與AI基礎設施占營收逾60%；Q2指引 $630–670M","source":"TipRanks/itiger 報導 Lumentum Q1 FY2026","url":"https://www.itiger.com/news/2581761566","excerpt":null,"as_of":"2025-11-04","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"管理層稱EML市占約70-80%，產能依長約（多為三年）到2027曆年已被認購；預期2026年12月季EML出貨量年增逾50%；EML供不應求預期延續至2027；價格上行","source":"Briefing.com Story Stocks: Lumentum lighting it up (FY27 setup)","url":"https://www.briefing.com/story-stocks/archive/2026/8/12/lumentum-lighting-it-up-as-record-margins-and-strong-optical-demand-lift-fy27-setup-(lite)","excerpt":null,"as_of":"2026-08-12","retrieved_at":"20261108","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"FY26 Q4 營收年增約90%，AI資料中心光學帶動創紀錄季度","source":"Converge Digest: Lumentum revenue soars 90% as AI data center optics drive record quarter","url":"https://convergedigest.com/lumentum-revenue-soars-90-as-ai-data-center-optics-drive-record-quarter/?amp=1","excerpt":"Lumentum Revenue Soars 90% as AI Data Center Optics Drive Record Quarter","as_of":"2026-05-06","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"FY2026 10-K 風險因子：市場技術變化快、新品頻繁推出；光通訊產品已成熟並日趨商品化，傳統對手與亞洲新進者加劇價格壓力，公司需持續開發差異化高階產品。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"The market for optical communications products in particular has matured over time and these products have increasingly become subject to commoditization. Both legacy competitors as well as new entrants, predominantly Asia-based competitors, have intensified market competition in recent years leading to pricing pressure.","as_of":"2026-08-17","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"2026-06-09 Mizuho 會議 CEO 稱近封裝光學（NPO）可能比 CPO 更大；CPO 較大規模出貨預計 2027 年底。","source":"TIKR blog: Lumentum CEO new opportunity bigger than co-packaged optics","url":"https://tikr.com/blog/lumentum-ceo-just-revealed-a-new-opportunity-that-could-be-bigger-than-co-packaged-optics-heres-what-it-means-for-lite-stock","excerpt":"demand, how a new technology called near-packaged optics is being pulled forward faster than anyone expected, and why his previously stated $8 billion fiscal 2028 revenue target may end up conservative. What Hurlston Said and Why It Matters Now The most important disclosure from the conference was Hurlston’s characterization of near packaged optics, or NPO, as a potentially larger opportunity","as_of":"2026-06-10","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Simply Wall St 敘事指出整合/矽光子對手與快速創新週期為風險（意見文，非公司揭露）。","source":"Simply Wall St narrative: photonics risks and cloud consolidation will erode margins","url":"https://simplywall.st/community/narratives/us/tech/nasdaq-lite/lumentum-holdings/t622mvni-photonics-risks-and-cloud-consolidation-will-erode-margins","excerpt":null,"as_of":"2025-08-15","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Lumentum 稱關鍵元件實質售罄，正爭取長期協議以抵銷資本支出；FY2026 Q4 已簽多份泵浦雷射長約；談判可含預付、take-or-pay、漲價。","source":"MarketBeat, Lumentum Q3 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/lumentum-q3-earnings-call-highlights-2026-05-05/","excerpt":"These components [narrow-linewidth laser assemblies and pump lasers] remain effectively sold out for the foreseeable future, and we are actively working to secure long-term agreements that will help offset anticipated capital expenditures","as_of":"2026-05-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"8/11 公司給 FQ1'27 EPS 指引 4.05–4.35，高於當時共識 3.55","source":"Benzinga（經搜尋摘要）","url":"https://www.benzinga.com/quote/LITE/earnings-forecasts","excerpt":"The company guided earnings per share in the range of $4.05 - $4.35, compared to a consensus EPS estimate of $3.55.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ1'27 實際營收 $1.26B、non-GAAP EPS $4.57，高於指引區間上緣 4.35；FQ2 營業利益率預期 >45%","source":"Lumentum 投資人關係新聞稿 FQ1 FY2027","url":"https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-First-Quarter-of-Fiscal-Year-2027-Financial-Results/default.aspx","excerpt":"Non-GAAP net income for the first quarter of fiscal year 2027 was $461.1 million, or $4.57 per diluted share.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill：FY2027 EPS 共識 22.05（33 位分析師），3 個月上修 20.2%","source":"Chartmill LITE estimates","url":"https://www.chartmill.com/stock/quote/LITE/estimates","excerpt":"EPS: 1.07% over 1 month; 20.20% over 3 months.","as_of":"2026-10-24","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga：14 位分析師 Buy 共識，平均目標價約 $830（1 強買/10 買/3 持有）；Barclays 7/20 升 Overweight 目標 $1,000，TD Cowen 7/13 目標由 $995 降至 $800；頁面日期不明確","source":"Benzinga LITE price targets","url":"https://kr.benzinga.com/quote/LITE/price-targets","excerpt":null,"as_of":"2026-07-20","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 7月：共識評級 Moderate Buy、共識目標價 $1,012.67；4月時為 $592.88","source":"MarketBeat（經搜尋摘要）","url":"https://www.marketbeat.com/instant-alerts/lumentum-nasdaqlite-shares-up-94-still-a-buy-2026-07-21/","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"FQ1'27 財報後 FQ2 營收指引與是否上修","source":"rallies.ai","url":"https://rallies.ai/news/lumentum-raises-q2-revenue-outlook-62-to-650m-unveils-150w-ultrafast-lasers","excerpt":"Lumentum Raises Q2 Revenue Outlook 62% to $650M, Unveils 150W Ultrafast Lasers - LITE News | Rallies","as_of":"2026-01-16","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-11-01 Lumentum 與 Marvell 簽署合併協議（兩段式合併，Lumentum 成為 Marvell 全資子公司）；搜尋摘要稱全股票交易、換股比 4.5 Marvell 股/LITE 股，約 $115B，預期 2028 上半年完成（聚合報導，未讀原文）","source":"SEC EDGAR 8-K Item 1.01 (2026-11-02)","url":"https://www.sec.gov/Archives/edgar/data/1633978/000119312526442758/d163169d8k.htm","excerpt":"On November 1, 2026, Lumentum Holdings Inc., a Delaware corporation (“Lumentum” or the “Company”), entered into an Agreement and Plan of Merger (the “Merger Agreement”) with Marvell Technology, Inc., a Delaware corporation (“Marvell”)","as_of":"2026-11-02","retrieved_at":"20261108","affects":["valuation","triggers","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"BIS 與 DOJ 對 Lumentum 對華為出貨的傳票調查仍在進行，公司配合中、未見和解或處罰","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"In August 2024, we received an administrative subpoena from BIS requesting the production of records in connection with our business with Huawei. We also received a related subpoena from the U.S. Department of Justice (“DOJ”) that also requested information regarding our business with Huawei.","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 8-K 共 13 份，含重大項目者 2 份（2025-12-22 信貸協議、2026-11-02 合併協議）","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001633978&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-11-01 與 Marvell 簽署合併協議，Lumentum 將成 Marvell 全資子公司","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1633978/000119312526442758/d163169d8k.htm","excerpt":"On November 1, 2026, Lumentum Holdings Inc., a Delaware corporation (“Lumentum” or the “Company”), entered into an Agreement and Plan of Merger (the “Merger Agreement”) with Marvell Technology, Inc., a Delaware corporation (“Marvell”)","as_of":"2026-11-02","retrieved_at":"20261108","affects":["valuation","triggers","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"-","claim":"無 SEC 調查或重編；但有 BIS/DOJ 對華為出貨的出口管制調查（非 SEC），仍在進行","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm","excerpt":"We have been, and will continue to, cooperate with BIS and DOJ in responding to the subpoenas and their ongoing reviews.","as_of":"2026-08-17","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"LITE","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.91,"operating_margin_pct":23.35,"fcf_margin_pct":9.52,"rd_intensity_pct":12.47},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"COHR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.16,"operating_margin_pct":14.11,"fcf_margin_pct":-23.28,"rd_intensity_pct":10.18},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"CIEN","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":44.07,"operating_margin_pct":14.12,"fcf_margin_pct":13.53,"rd_intensity_pct":15.36},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CIEN","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AAOI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":28.92,"operating_margin_pct":-10.58,"fcf_margin_pct":-100.9,"rd_intensity_pct":18.06},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAOI","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MTSI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.13,"operating_margin_pct":18.97,"fcf_margin_pct":9.44,"rd_intensity_pct":23.23},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTSI","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"LITE"},"financial_history":{"ticker":"LITE","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":1767000000.0,"revenue_yoy_pct":null,"gross_margin_pct":32.2,"operating_margin_pct":-4.96,"net_income":-131600000.0,"diluted_eps":-1.93,"free_cash_flow":51300000.0,"fcf_margin_pct":2.9,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":1359200000.0,"revenue_yoy_pct":-23.08,"gross_margin_pct":18.5,"operating_margin_pct":-26.59,"net_income":-546500000.0,"diluted_eps":-8.12,"free_cash_flow":-112300000.0,"fcf_margin_pct":-8.26,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":1645000000.0,"revenue_yoy_pct":21.03,"gross_margin_pct":27.96,"operating_margin_pct":-11.68,"net_income":25900000.0,"diluted_eps":0.37,"free_cash_flow":-104700000.0,"fcf_margin_pct":-6.36,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":3014000000.0,"revenue_yoy_pct":83.22,"gross_margin_pct":41.67,"operating_margin_pct":17.79,"net_income":-6935100000.0,"diluted_eps":-92.96,"free_cash_flow":300100000.0,"fcf_margin_pct":9.96,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/LITE/LITE_Q4_2026_Earnings_Call_20260811.md）

# Q4 2026 Earnings Call
2026-08-11

Q4 2026 Earnings Call
Lumentum Holdings Inc. | Earnings Calls | 2026-08-11
Operator (Operator)
Good day, everyone, and welcome to the Lumentum Holdings Fourth Quarter and Fiscal Year 2026
Earnings Call. [Operator Instructions] Please also note, today's event is being recorded for replay
purposes. [Operator Instructions].
At this time, I would like to turn the conference call over to Kathy Ta, Vice President of Investor
Relations. Ms. Ta, please go ahead.
Kathryn Ta (Executives)
Thank you, Matthew, and welcome to Lumentum's Fiscal Fourth Quarter and Full Year 2026 Earnings
Call. This is Kathy Ta, Lumentum's Vice President of Investor Relations. Joining me today are Michael
Hurlston, President and Chief Executive Officer; Wajid Ali, Executive Vice President and Chief
Financial Officer; and Wupen Yuen, President, Global Business Units.
Today's call will include forward-looking statements, including, without limitation, statements
regarding our future operating results, strategies, trends and expectations for our products and
technologies, that are being made under the safe harbor of the Securities Litigation Reform Act of 1995.
These statements are subject to risks and uncertainties that could cause actual results to differ
materially from our current expectations. We encourage you to review our most recent filings with the
SEC, particularly the risks described under Risk Factors and elsewhere in our 10-Q for the fiscal quarter
ended March 28, 2026, and in our most recent 10-K for the fiscal year ended June 27, 2026, to be filed
by Lumentum with the SEC.
The forward-looking statements provided during this call are based on Lumentum's reasonable beliefs
and expectations as of today. Lumentum undertakes no obligation to update or revise these statements,
except as required by applicable law. Please also note that unless otherwise stated, all financial results
and projections discussed in this call are non-GAAP. Non-GAAP financials have inherent limitations
and are not to be considered in isolation form or as a substitute for or superior to financials prepared in
accordance with GAAP. You can find a reconciliation between non-GAAP and GAAP measures and
information about our use of non-GAAP measures and factors that could impact our financial results in
our press release and our filings with the SEC. Lumentum's press release with the fiscal fourth quarter
and full year 2026 results and accompanying supplemental slides are available on our website at
investor.lumentum.com. We encourage you to review these materials carefully.
With that, I'll turn the call over to Michael.
Michael E. Hurlston (Executives)
Thank you, Kathy, and good afternoon, everyone. Lumentum is positioned at the heart of a secular
industry shift. As AI compute workloads increased in both speed and bandwidth, data center architects
are turning to optical links as a primary means of connectivity. Our fourth quarter results reflect the
early stages of this transition, driven by broad-based momentum across our scale-out and sell across

product lines. Revenue surged 109% year-over-year to $1.01 billion, marking our eighth consecutive
quarter of top line growth.
Additionally, we are maintaining revenue velocity as we saw our third consecutive quarter of greater
than 20% sequential growth notable as the compare point is getting ever larger. While we experienced
broad-based success, some of our previously highlighted growth drivers are just starting to layer in.
Notably, in cloud transceivers, we achieved record 800 gig shipments, while initiating production of
our next-generation 1.6T modules. In OCS, we successfully navigated supply chain constraints to meet
steep customer demand, ramping internal manufacturing shipments according to plan.
In addition to strong top line performance, non-GAAP gross margin crossed 50%. We had originally
targeted this threshold at a $2 billion quarterly run rate. So this milestone came quite a bit sooner than
expectations. We expect gross margin expansion to continue driven by product mix and tight
operational execution. Non-GAAP operating margins expanded by more than 2,150 basis points year-
over-year. These results prove 2 things: Our differentiated technology commands premium value and
our operating model delivers outsized leverage. Driven by sharp acceleration in AI revenue, the
midpoint of our Q1 revenue guidance reaches our $1.25 billion target more than 1 quarter ahead of
schedule. Additionally, our Q1 non-GAAP operating margin guidance exceeds the high end of our target
model that we associated with this revenue level.
I'd like to address some recent market noise around co-packaged and near-packaged optics. First, our
lead CPO customers' production plans remain very much on track and their demand signal has
increased since our last update. Our visibility into the timing of CPO scale-up deployments is also
sharpened. We remain confident in a demand ramp for our ultra high-power laser chips in the second
half of calendar 2027 ahead of customer scale up deployments in calendar 2028. Because the first
phase of scale-up optical connections will span across compute racks within the cluster, this demand
ramp applies to any topology larger than one rack. Adding to our confidence, we have recently given
our first external line source or ELS module purchase for delivery by the second half of calendar 2027.
Second, the rest of our customer base is currently prioritizing near-packaged architectures as an
intermediate step to the eventual adoption of CPO. The NPO opportunity is completely additive for us,
significantly increasing optical TAM. We're seeing strong NPO momentum across multiple high-
velocity engagements using our differentiated laser chips. Even our largest CPO customer is looking at
NPO for specific new use cases further increasing the optical TAM at that account. These architectural
shifts represent a major market inflection that plays directly to our core strengths as a premier laser
chip manufacturer, benefiting us as optics begin to penetrate the copper domain.
NPO offers a faster time-to-market option by placing optical engines on the board right next to the XPO
accelerator, training power and costs for simplicity and optical scale-up applications. Customers are
evaluating 2 types of laser chips for NPO. In mid-power laser integrated directly with the optical engine
and a high-power laser used in an external light source module. Our mid-power lasers inherent the
reliability and engineering of our flagship high-power platform. Our family of NPO and CPO lasers
utilizes common design and process know-how to achieve industry-leading efficiency across 120
milliwatt, 150-milliwatt and 400-milliwatt output levels. Looking ahead, CPO continues to be viewed as
the natural end state on the technology road map, placing optics directly on the substrate or interposer
for maximum power efficiency through foundry-level advanced packaging.

Now let's look closer at the metrics to define our fourth quarter, starting with the components product
category. Components revenue for the fourth quarter was $649 million, reflecting 22% sequential and
103% year-over-year growth increases. Our laser portfolio continues to demonstrate strong momentum
across every vector. Shipments of our narrow linewidth laser assemblies grew sequentially for the tenth
consecutive quarter, and we were up over 130% year-over-year. Pump laser shipments surged more
than 80% year-over-year, and we will remain effectively sold out for the foreseeable future despite our
rapid capacity expansion.
Expanding, inferencing and training applications are driving full rate connectivity between data
centers, while political and regulatory constraints favor smaller, more modular builds. These 2 factors
among others are substantially increasing the demand for our pump laser solutions. To put this in
perspective, for one major hyperscaler, the network capacity connecting just 2 AI data center sites
could double the total global backbone capacity they built over the entirety of the last decade. To
support the growth and scale across deployments, we have secured multiple long-term customer
agreements that helped offset our planned capital expenditures. We continue to expect a fourfold
increase in our pump laser shipments over the next several quarters to meet this escalating demand.
Turning to laser chips. We delivered another record-breaking quarter for EMLs, primarily driven by
strong demand for 100-gig per lane devices. Momentum for our 200-gig EMLs is also accelerating
rapidly, now accounting for over 25% of total EML revenue. Simultaneously, we are expanding our
laser chip strategy to capture broader market opportunities in ways that aligned with our financial
model. A key example is our CW laser chip for 200 gig per lane applications, which delivers high yield,
proven reliability and industry-leading performance in a compact form factor to a multitude of
customers.
Internal deployment of these lasers reinforces what our customers regularly confirm. We have a
distinctive ability to deliver at scale to a very tight set of specifications, which enables superior yields in
transceiver manufacturing. Importantly, these new CW laser products will deliver margins that are
accretive to our long-term financial targets. Looking ahead, we expect demand for both EML and CW
lasers to grow significantly through the second half of calendar '26 and into 2027. To capture the
coming 200-gig and 300-gig lane speed opportunities, we are expanding capacity across our 2 indium
phosphide wafer fabs in Japan, qualifying both CW and EML process flows on our newest tools as they
come online. Even as we allocate additional capacity to CW lasers, we remain on track to deliver over
50% EML unit growth by December 2026 quarter compared to the year ago quarter. Wrapping up our
components commentary, we have visibility to an expanding set of 3D sensing applications. These new
opportunities are expected to drive growth in upcoming product cycles with our primary customer.
Now I will move to our systems product category. Systems fourth quarter revenue reached $357
million, representing a 30% sequential and 123% year-over-year increase. Both cloud transceivers and
OCS were major drivers of the revenue growth quarter-over-quarter. While pockets of supply chain
tightness for certain components capped shipments below total market demand, our factories executed
to our aggressive plan for both product lines. The bulk of our cloud transceiver shipments in the
quarter were at 800 gig speeds, and we began shipping 1.6T transceivers as planned.
Meanwhile, profitability across our transceiver lines continues to improve, driven by gains in both yield
and capacity utilization as well as the initial rollout of higher ASP 1.6T transceivers. Our visibility into
future cloud transceiver demand is clearer than ever. In fact, we expect the 1.6T transceiver uptake to

intensify starting in fiscal Q1 and sustain through calendar 2027. This momentum is anchored by our
lead Tier 1 hyperscale customers whose strong rollouts of custom AI clusters are driving a rapid
transition from 800 gig to 1.6T technology. Through the use of improved design engineering
techniques, we appear to be first to market in many instances ahead of larger competitors, giving us a
market share advantage that we should be able to maintain through the cycle. The degree of difficulty
with 1.6T designs, again, is playing to our strengths as our Signal Integrity team is widely acknowledged
as the best in a competitive field.
Turning to OCS. Our internal manufacturing expansion is progressing smoothly. After doubling
shipments from fiscal Q3 to Q4, our guidance includes our first triple-digit OCS revenue quarter. The
demand signal for 2027 continues to be incredibly strong, and we have started the initial work to add
capacity with contract manufacturers as well as continuing to increase output in our internal factories.
Since our last call, the road map for OCS has also come into better view. We are now planning higher
and lower port count products, including specialized in-tray offerings. Rounding out our systems
category performance in industrial lasers and cable access strengthened quarter-over-quarter. Within
industrial lasers, we are seeing increased adoption of our ultrafast lasers targeting high-density PCB via
drilling that supports advanced AI XPU boards and 1.6T optical modules.
Looking ahead to Q1. We expect to set another quarterly record and as stated earlier, reach our $1.25
billion revenue target more than one quarter ahead of the plan outlined at the last OFC. We anticipate
that approximately half of the sequential growth will stem for our components portfolio driven by
continued expansion in scale-out and scale-across applications. The other half will be powered by the
ongoing ramp of our systems portfolio of about 1.6T transceivers and accelerating OCS deliveries.
Now I'll hand the call over to Wajid. Mr. Ali?
Wajid Ali (Executives)
Thank you, Michael. Fourth quarter revenue of $1.01 billion was at the high end of our guidance range
and non-GAAP EPS of $3.23 was well above our prior expected range, demonstrating the leverage of
our business model. GAAP gross margin for the fourth quarter was 47.4% and GAAP operating margin
was 27.8%. Both metrics exemplify the company's exceptional performance. As disclosed previously, in
the fourth quarter, we proactively equitized a portion of our convertible notes, which were in the money
following the appreciation of our stock over the past year. This action reduces our debt by $1.1 billion or
approximately 35% of our outstanding convertible debt. This transaction resulted in a one-time non-
cash GAAP charge of $7.8 billion, bringing our fourth quarter GAAP net loss to $7.2 billion.
Turning to our non-GAAP results. Fourth quarter gross margin was 50.4%, which was up 250 basis
points sequentially and up 1,260 basis points year-on-year due to better manufacturing utilization,
favorable mix and increased pricing on select products. Fourth quarter non-GAAP operating margin
was 36.6%, which was up 440 basis points sequentially and up 2,160 basis points year-on-year. We
continue to invest in critical R&D programs serving cloud and AI customers while maintaining the
rigorous cost controls necessary to optimize our business model. Fourth quarter non-GAAP operating
profit was $368.8 million and adjusted EBITDA was $406.4 million. Fourth quarter non-GAAP
operating expenses totaled $138.1 million or 13.7% revenue, an increase of $11.9 million from the third
quarter and an increase of $28.8 million from the same quarter last year in support of expanding cloud
and AI opportunities.

Q4 non-GAAP SG&A expenses were $50.6 million. Non-GAAP R&D expenses were $87.5 million. Total
interest and other income net was $22 million on a non-GAAP basis. Fourth quarter non-GAAP net
income was $326.3 million and non-GAAP net income per share was $3.23. Our diluted weighted
shares for the fourth quarter were 101.1 million on a non-GAAP basis. I will now turn to the balance
sheet.
During the fourth quarter, our cash and short-term investments decreased by $0.43 billion to $2.74
billion, with the decrease primarily driven by convertible debt conversions. Our inventory levels
increased by $59 million sequentially to support the expected growth in our cloud and AI related
revenue. In Q4, we spent $167 million in CapEx, primarily focused on manufacturing capacity to
support cloud and AI customers. Turning to revenue details. Components revenue of $649.4 million
increased 22% sequentially in Q4 and 103% year-on-year. Systems revenue of $356.9 million increased
30% sequentially in Q4 and 123% year-on-year.
Now let me move to our guidance for the first quarter of fiscal year '27, which is on a non-GAAP basis
and is based on our assumptions as of today. We anticipate net revenue for the first quarter of fiscal
year '27 to be in the range of $1.225 billion to $1.275 billion. The $1.25 billion midpoint reflects more
than 130% year-over-year growth, setting yet another all-time quarterly revenue record for Lumentum.
We project first quarter non-GAAP operating margin to be in the range of 39.5% to 40.5% and diluted
net income per share to be in the range of $4.05 to $4.35. At the midpoint, this operating margin
represents an expansion of more than 2,100 basis points year-over-year. Our non-GAAP EPS guidance
is based on a non-GAAP and annual effective tax rate of 16.5%. These projections assume shares used
for non-GAAP diluted earnings of approximately 102 million.
With that, I'll turn the call back to Kathy to start the Q&A session. Kathy?
Kathryn Ta (Executives)
Thank you, Wajid. [Operator Instructions]
Operator (Operator)
[Operator Instructions] Your first question comes from the line of Joseph Cardoso with JPMorgan.
Joseph Cardoso (Analysts)
Maybe for the first one, obviously, you highlighted you're tracking to hit the $1.25 billion revenue target
a quarter early and are already running well ahead of your high end of margin targets here. Just given
both the stronger demand and maybe the more favorable mix, how should we be thinking about the
read-through to the next set of financial targets, particularly given what looks like incremental
opportunities forming relative to the framework, including ELS, NPO engagements. And I think you
even mentioned scale up OCS as well. Just curious in terms of how we should be thinking about the
next set at this here?
Michael E. Hurlston (Executives)
Joe, this is Michael. Firstly, thanks for your continued support. Look, we'll come out with some new
financial targets, probably at the next OFC. We're obviously running well ahead on almost every metric
on revenue, on margin, on operating margin. We seem to be doing quite a bit better. And you're right.
Look, I think there are some new things that we didn't factor into our discussion at OFS. NPO, we spent

a bit of time on the -- in the prepared remarks on NPO. CW lasers, we think that that's an incremental
opportunity for us that we would probably not spend a lot of time on before.
And you're right, OCS, I think, as we've discussed, but it seems to be doing a bit better than expected.
So we feel like we're executing. We're trying to keep our head down and run and obviously adding
nearly $250 million incrementally into the guide is pretty impressive, and we think we have the
opportunity to do that more as we look out in future quarters.
Joseph Cardoso (Analysts)
Got it. Fair. And then maybe just a follow-up and specifically on the NPO. Curious if you could provide
any further details there, specifically how you're thinking about the time here, just given that it does
sound like some of these opportunities are forming a little bit earlier than expected. And I know you
talked about the different form factors or the different kind of content opportunities as it relates to the
laser opportunities there. But any way to kind of flesh out like where you guys are seeing maybe the
architecture of choice by your customers and is that biased in any direction? And how we should think
about content as it at least relates to maybe your large customer on the CPO side relative to the ultra
high power laser.
Michael E. Hurlston (Executives)
Yes. I'm going to say a couple of things and then actually ask Wupen to comment a little bit on the
differentiation in mid-power. Certainly, the timing of these opportunities is plus or minus what we have
talked about for our lead CPO customer. Our lead CPO customer, we just said in the prepared remarks,
we would expect to start shipping in high volume for scale-up. We're already, of course, shipping for
scale-out. For scale-up, we expect to be shipping in the second half of calendar '27 for their deliveries in
'28.
Our leading customers on NPO, plus or minus, probably maybe minus a quarter, are in that ZIP code.
The first couple of those are more -- is the same kind of ELS high-powered laser and then maybe
followed by a couple that are integrated where the optical engine of a mid-power laser is integrated
inside the optical engine, and it's all one unit. So I would say that the ones that we have the best line of
sight on and that are sooner are more of the high-powered laser type, very consistent with what we've
been talking about for our largest CPO customer.
With that said, I wanted Wupen, maybe to give a few seconds of color because I think there's a little bit
of a mischaracterization. We think that these mid-power lasers that are going inside the OE, lot of
things going on there in terms of differentiation. Do you want to give 2 seconds on that?
Wupen Yuen (Executives)
Yes, definitely. Thanks, Michael. So definitely, the -- it is the -- to do the kind of the NPO optical engine,
imagine these NPOs set at about 6.4T of bandwidth, which is really equivalent to 4x that of a local CC
module. The level of integration and the power density that's required and efficiency required to fit
everything to a small optical engine is immense. Therefore, you need really the best laser technology
and the best efficiencies in order to really fit everything in a small package.
So Lumentum's advantage here really is to leverage our 400-milliwatt kind of design principle and
leverage the high efficiencies of the intrinsic design process and scale it to an application, right, around
150, 200-milliwatt range, that enables that application. This is actually based on our ultra-high power

technology that we uniquely positioned to address this market, and we believe that by late 2027-2028
timeframe, that NPO will hit the market to enable optical scale-up, and this becomes an interesting
opportunity for us to increase our laser business.
Operator (Operator)
Your next question comes from the line of Simon Leopold with Raymond James.
Simon Leopold (Analysts)
First thing I wanted to try to ask is, to what extent we're able to reprice backlog with your customers?
And how did that affect this quarter's gross margin as well as your gross margin outlook? And then I've
got a quick follow-up.
Michael E. Hurlston (Executives)
Yes. Thanks, Simon. Look, we did reprice a little bit. I think most of our sort of LTAs are more forward-
looking in terms of the price impact. We saw some benefit, as Wajid said in his prepared remarks, on
the gross margin line on pricing. We think that, that still has some room to play through. But I'd say the
long pole this quarter was more on mix, right, where we were shipping a lot more of our high mix
components and I think as we said, we'd expect that to continue to play through as well. So we think we
have some room to run on gross margin line side.
Simon Leopold (Analysts)
Great. Appreciate that. And the other thing I've been hoping to ask you about is we've been hearing
more about Chinese-based companies coming to market with new indium phosphide fabs. What's your
take on this developing and future competition?
Michael E. Hurlston (Executives)
Yes. Look, I mean, I think we're hearing the same thing. We obviously haven't seen any impact on our
numbers as yet, and I don't expect there to be any impact. We think we have differentiation, obviously,
on EMLs. We were very strong there. And these high and mid power lasers that are necessary for NPO
and CPO, again, very strong differentiation there. And then even in CW, we've been surprised at our
ability to price up given what we said in the prepared remarks that customers are seeing far better
yields given our ability to deliver consistent performance on our lasers.
They just simply don't deviate. The width of the spec is very narrow, and that results in far better
transceiver yields for the customers that we've actually started shipping CW lasers to. And so as a
result, we are able to command a nice price premium that we'd expect to sustain as these Chinese -- if
these Chinese guys come online. I caution people also -- I think people are -- some of these Chinese
laser suppliers are not delivering in the market today. So they have very -- there's no recourse when
they throw out these big numbers. We have not seen anything like that to date in terms of their output.
Operator (Operator)
Your next question comes from the line of Mike Genovese with Rosenblatt Securities.
Michael Genovese (Analysts)

Really good to see the guide for a triple-digit OCS revenue quarter, I think, in the current quarter, I
think is what you said. So could you just confirm that? But also the question is, any comment on when
we could expect to see that happen for ultra high-powered CW scale-out lasers where we'd get triple-
digit quarter?
Michael E. Hurlston (Executives)
Yes, Mike, again, first, I want to thank you for the support of the company and really following our
details really well. Yes, you've got it right. So in the guide, which is the first quarter, we expect our first
triple-digit OCS revenue quarter, we'd expect to be meaningfully above the 3-digit mark. We're
executing well on OCS, as I said.
And then for ultra-power lasers, we have said, hey, we expect by the end of the year to be sort of in the
$50 million mark. I think the third quarter is when you'd see the first triple digit quarter for ultra-high
powered lasers. So we are executing. We're shipping today. We had a good shipments in this -- in the
reported quarter, Q4. We'd expect that to build somewhere in the $50 million range by the end of the
calendar year, and then to really meaningful impact in fiscal Q3.
Michael Genovese (Analysts)
Great. Perfect. And then finally, for Greensboro. Just any -- is there any update on the expectation for
sort of half of the capacity of Greensboro being there in calendar '28, the other half in calendar '29? Is
that still the schedule? And I know it's early, but any kind of color you could give us on the progress
there would be great.
Michael E. Hurlston (Executives)
Yes. Look, progressing super well. I'm actually very pleased that the team that we got in Greensboro is
first rate. As you know, we inherited a fully functioning fab. So the switch that we need to throw is to
convert it from gallium arsenide indium phosphide. That is well underway. Some of the long haul
items, reactors and things like that, our team has gotten out in front of. I think we continue to say
revenue -- first revenue out of that in early 2028 and ramping through calendar 2028 into kind of a full
pitch by the end of '28 and into '29. So really no change in that, Mike.
Operator (Operator)
Your next question comes from the line of Papa Sylla with Citi.
Papa Sylla (Analysts)
Congrats on the strong results as well. Michael, I was kind of double clicking on the OCS. I was hoping
perhaps you can refresh us. I know this quarter, you mentioned it hit triple digits, but if you can refresh
us on the $400 million plus OCS guide for the second half of 2026. Are you running well ahead of it or
just any update on that side? And perhaps tied to that, how should we think about your key OCS
customers build versus buying from you calculus? Do you expect Lumentum to eventually absorb most
of their internal programs? If so, any timeline in mind?
Michael E. Hurlston (Executives)
Yes, Papa, look, what I'd say is we're definitely tracking to the $400 million. I would not say tracking
ahead. I mean, we definitely, as you know, had some problems early on in the ramp with supply chain.

We're out of that now. I think we're executing, as I said, to plan. We are plus or minus about where I
would have expected to be for the guide, right? So that contributes -- takes a dent out of the $400
million and that leaves us some room to run in the fourth quarter -- fourth calendar quarter. Relative to
one customer that apparently has an internal source of supply, we are, I think, executing extremely
well. I don't think we -- I think they'll continue to use an internal version.
But I think as they ship more and more OCSs, we will absorb the vast majority of that. So I would
expect sometime in early '27 that we cross over and be the #1 supplier and actually have momentum
from there in terms of our OCS shipments. So we definitely, I think we surprised the customers. We are
continuing to ship to a number of different customers. Our execution back on track, but most
importantly, like on software and things like that, where I had expected us to have more difficulty,
Papa, we've done well. So I think our customers, in general, if you talk to them, would say, we've been
an incredibly, incredibly strong supplier.
Papa Sylla (Analysts)
No, that's great to hear. And Michael, for my follow-up, just curious on the -- any update on the
supply/demand kind of imbalance? I believe last quarter you mentioned 30% plus. Where are we now?
And how do you see that improving? Or how do you see that going into fiscal '27 and beyond?
Michael E. Hurlston (Executives)
Yes. So I would say on EML, probably no change, right? So I don't think that it's gone up, but it hasn't
come down. We're still shipping behind customer demand on EML. I think what surprised us is high-
powered lasers, right? High-powered lasers, again, there's been a lot of noise in the system on what's
happening on various co-packaged and near-packaged opportunities. We are way behind. Our
shipments, unfortunately, on high-powered lasers. So we -- if one vector has really changed since the
last time you and I talked, I'd say it's your high-powered lasers, and we are very much further behind.
The demand signals increased and we are very much further behind relative to our ability to supply.
Wupen Yuen (Executives)
Yes. I think just to clarify -- yes, just to clarify, our execution of the ramp is on track, right? We're
further behind because our -- the demand has accelerated. That, as Michael said in the prepared script.
Operator (Operator)
Your next question comes from the line of Christopher Rolland with Susquehanna.
Christopher Rolland (Analysts)
My question, in your press release, it sounds like you were selling not just ELS lasers, perhaps ELS
modules as well. And I was wondering if you could speak a little bit more about that opportunity and
what the economics look like beyond just lasers and for the full module?
Michael E. Hurlston (Executives)
Yes, Chris. Yes. No, we -- again, first, appreciate how much time you're spending on the company. Yes,
we've got our first ELS module order right? Which from an ASP standpoint is meaningfully higher than
the set of lasers that we ship in. So we're very excited about the revenue opportunity, small to start,
right? And we said that we'd be shipping sometime midyear, early second half of '27 to be honest, a

little bit later. We felt like we'd see more opportunity on sort of scale-out applications than we have to
date. But we're very pleased to be participating in the early phases of scale up with both lasers and now
with the ELS module.
As I said a minute ago, the ELS module meaningfully higher from an ASP standpoint, but the margins
are not quite as good. Above corporate average, but not quite as good as the lasers. So we're trading a
little bit of margin to get some revenue bump. We think -- I think Simon asked earlier in the call, we
think we have enough drivers on the margin side that we can keep the margin vector moving, but help
our revenue acceleration.
Wupen Yuen (Executives)
Also just a bit to add, right? If you recall that we've positioned our ELS module to be really enabling the
customers who don't want to deal with individual laser chips. So this is really a very first step for us to
take to ship to one customer and then go from there, we enable other end users to use the ELS, enable
their CPO and NPO systems.
Christopher Rolland (Analysts)
Excellent. Maybe as a follow-on, I think, Michael, you've talked about, I think it's the 1.6T cycle or 200
gig per lane and perhaps CW and SiPHo working into the supply chain maybe earlier and being a larger
part of transceiver shipments ultimately. I guess, first of all, where are we on that? Is this on the SiPHo
CW side accelerated even faster than you originally spoke about. And can you kind of describe the
difference in economics for you between CW lasers and EMLs, which would be, I think, larger because
they contain the modulators as well. That will be great.
Michael E. Hurlston (Executives)
Okay, Chris, yes, good question, and I'll give some commentary, and then have Wupen comment as
well. So one, no slowdown in our EML demand. I mean we are -- I think it was Papa that asked a
minute ago, we see still a significant supply/demand imbalance on CW or EMLs. As Kathy put in the
prepared remarks, we're still very much on track to increase our EML output year-over-year. But even
at the end of the year, we'd expect to be significantly behind demand. So no slowdown at all in the
demand that we're seeing from EML.
We acknowledge and we've said this before, that we would expect and are seeing CW lasers take a
significant portion of transceiver output. Silicon photonics is a viable solution at 1.6T. Of course, we've
also said, and it also seems to be bearing out that as we think about 3.2T, silicon photonics loses some
of its advantages, and we'd expect to see EMLs come back in a meaningful way. What I comment is, a
little bit of a shift in stance is that we are allocating some of our output now because we're actually
doing quite a bit better in Japan than we expected in terms of output. And so what we're doing is part of
that is allocating some of this excess output to CW lasers and we're now shipping CW lasers in a
relatively meaningful way in this 200-gig per lane silicon photonics opportunity. What's also changed
for us is we have significantly reduced the die size of our CW laser.
So before when you and I talked, we said, hey, probably from a margin standpoint, EML is better. Now
we brought things much more in line. CW lasers are smaller. They're better performing. We are
commanding a significant price premium, as I said in a previous question, against what we view as the
market price because of the performance of these lasers. And as such, the margin opportunity is still

better EMLs, but that gap has closed considerably, I think since the last time we talked. Wupen, do you
want to talk a little bit about the dynamic that you're seeing on CW and EML?
Wupen Yuen (Executives)
Yes, Michael, I think I hope we're accurate, right? Just a couple of things to add to that. Number one, if
you look at the application today, there's a lot of 200 G per lane volume that's on 800 gig. And then in
that, we actually see a much higher EML share versus CW laser share. So Michael, talked about
dynamics. I think this will continue. EML will remain a very important player in 200 G per lane. But as
1.6T ramps up, I think we will see more CW lasers as Michael talked about, our new design of 200 G
CW laser is much more efficient, therefore smaller. It gave us a much better gross margin profile.
Another thing also of note, really, dynamics here is that in a constrained environment, we'll also see
customers' behavior as wherever they can get the laser source, they will use that solution to support
their build-out. So the dynamics of EML/CW lasers is not only a technical one, but also a supply versus
demand situation.
Operator (Operator)
Your next question comes from the line of Vijay Rakesh with Mizuho.
Vijay Rakesh (Analysts)
A good quarter and guide here. Just a quick question on the 200 gig per lane EML and CW, it looks like
that's ramping very nicely. Is it fair to assume both the 200 gig EML and CW laser should be accretive
to your margins? And when do you see this 1.6T crossover, it looks like it's already greater than 25%
revenues. But when do you see that crossing over with the [ 800 G ], I guess, and a follow-up.
Michael E. Hurlston (Executives)
Yes. Mr. Rakesh. Good to hear from you, my friend. Look, no change really in the forecast on the
crossover. What we said is -- and I think you're referring to 200 gig per lane lasers. We have said that
for us, we'd expect 200 gig EMLs to be the majority volume shipments by the middle of 2027. We just
said in the prepared remarks that now 200 gig per lane EMLs are 25% of our mix. We'd expect it to be
50% or more of volume by midyear of 2027. So we seem to be tracking to that. No real change in that. I
think generally speaking, yes, you're right, lasers are one of our better businesses, and the lasers are
more than -- our corporate accretive, the CW or EML. And as I said to Chris a minute ago, we've closed
the margin gap quite considerably since our last call, on EMLs versus CW by shrinking the die size of
the CW laser. So EMLs are still better, but we've closed the margin gap quite considerably.
Vijay Rakesh (Analysts)
Got it. Very helpful. And then on the operating leverage side, Wajid, it looks like solid improvement
there year-on-year, you already at your 40% target. How should we look at -- how should we think
about it as you go through fiscal '27?
Wajid Ali (Executives)
Yes. Thanks, Vijay. So the guideline that we have given at $2 billion of revenue was 38% to 42%, like
Michael said in his prepared remarks. We're already at the midpoint of that at much lower revenue
levels. And so with gross margins improving as we approach $2 billion, we'll see some improvement on

the operating margin line as well that corresponds to those gross margin improvement. So think of the
42% outlier more as a midpoint with the range, probably moving up 100 to 200 basis points versus
what we showed at OFC.
Operator (Operator)
Your next question comes from the line of George Notter with Wolfe Research.
George Notter (Analysts)
Congrats on all the success here. I guess I wanted to ask about indium phosphide substrate supply. I
was really intrigued by the deal you guys signed in the quarter with AXT. Because I think a quarter ago,
you actually said that you were doing pretty well on indium phosphide substrate. And so it feels like
there's a bit of a change here. I guess I'm wondering like what you guys are seeing longer term here in
terms of your need for more indium phosphide substrate. And as I extrapolate that kind of look at
Greensboro, are you making more progress towards filling the rest of that facility looking forward?
Michael E. Hurlston (Executives)
George, yes, look, I would agree. I mean I think what we tried to hint to in a previous question is the
ultra-high-powered laser demand has surprised us, and that cuts across a couple of customers. So what
we're trying to do, I think really in the last 3 months is secured even more substrate supply. We were
doing well. We felt like we had given the baseline of demand that we were seeing from ultra-high-
powered and then, of course, the EMLs, the CW lasers that go into our scale-out products. We felt
pretty good, right, as you said. But I think we've seen a pretty big surge in demand, as we said. And in
order to respond to that, we went out and we found additional substrate help from AXTI. They are a
great partner. Wupen has worked with them for a good number of years. And we think we're going to
need their help just given the surge in demand.
So that's what drove that deal. If this vector continues, we're probably going to need to look for more
help on substrate. We feel we're good at this moment. We're probably pretty comfortable just given our
lead in arrangement with the Japanese supplier and now of the announced deal with AXTI. But given
the rate of change in the demand vector that we're seeing, that may not be true a quarter or 2 from now
either.
George Notter (Analysts)
Got it. And then do you think it's likely that we could see you sign some LTAs for more of the capacity in
Greensboro. Is that a possibility?
Michael E. Hurlston (Executives)
Yes. Look, we're looking to do that. I think we've sort of reported consistently that we have capacity in
Greensboro. We have room there and Wupen has been out talking to a number of customers about
helping them with their laser demands, which are, again, changing minute by minute is that everybody
starts to look to adopt near-packaged or co-packaged solutions. And so I would expect that we have
some things to talk about over the next couple of quarters relative to new arrangements in Greensboro
that speak to more of this capacity we have there.
Operator (Operator)

Your next question comes from the line of Tom O'Malley with Barclays.
Thomas O'Malley (Analysts)
My first is on the NPO side where you spend a little more time on the preamble talking about the
technology. I was curious, when you look at ASIC and GPU road maps, when you see the intersection of
NPO, does that need to be with a new generation of silicon or can you intersect an existing ramp. If you
were to see a big customer today ramping in the beginning of next year, were you able to ship NPO
solutions where they originally started off as electrical-only solutions just for the timing aspect of your
ramp, that would be super helpful.
Michael E. Hurlston (Executives)
Yes. Tom, super to speak to you again. We really appreciate this chat, as always, Tom, as always. Look, I
think what we're seeing now is an inflection in the ASICs and in the SerDes speed, and that's driving the
need for NPO and CPO. I don't know, and Wupen can comment a little bit on this. I don't think there
are existing TPUs, XPUs, GPUs that are shipping that have a fast enough SerDes speed that we could
suddenly plop in an NPO or CPO solution, which I think is what you're asking. But as these new
generations come online, really seeing silicon in mid-'27 toward the end of '27 and early '28 all those
new silicon solutions, again, GPUs, XPUs, TPUs all seem to be driving SerDes speeds that are
consistent with the adoption of NPO or CPO.
Wupen, any color you can add for Tom?
Wupen Yuen (Executives)
Thank you, Michael. I think that's very accurate. Really, I don't think, Tom, we are not seeing kind of
the retrofit of NPO onto the current XPUs. We're seeing really, like as Michael talk about, there is a
broad momentum towards the '28, kind of '28 ramp of NPO and CPO and really driven by optical scale-
up. So it's not -- this is beyond just the XPU itself. This also goes into a rack-based multi-rack system
that requires optical scale-up, right? Therefore, we believe this is going to be new processor, new racks
and there's 2028 event for optical scale-up from the industry's evolution point of view.
Thomas O'Malley (Analysts)
Super helpful. And then on the other side of things on OCS, you talked about in-tray OCS. I was
curious, is the competitive dynamic there similar for you guys? In terms of the timing, is that in your
current TAM? Or would that be additive to the TAM? And when do you see that intersecting in terms of
that technology hitting the market?
Michael E. Hurlston (Executives)
Tom, additive, right? So anything that Kathy's presented at OFC, it's above and beyond that. It's a very
new set of opportunities. We've come to find out there are a number of different folks that are looking
at this kind of approach, and it's all very additive. It would hit for us '28 timeframe, Tom. It's not
something that's super imminent, but it's imminent enough that we're working on it aggressively. It
requires a lot of redesign on our -- from our engineers. But look, we're the only guy shipping.
I mean I know a lot of people are talking about OCS a lot of start-ups for us to be now at $100 million
and beyond types of quarters, we're the only ones that have a track record outside of a contract

manufacturing relationship with a large OCS users. So we're really the only merchant supplier today of
OCS. And by virtue of that, we're going to get every single call and have the first look, I think, in every
single opportunity out there.
Kathryn Ta (Executives)
And Matthew, it looks like we have time for just 1 more question.
Operator (Operator)
Great. Your next and final question will come from the line of Ruben Roy with Stifel.
Ruben Roy (Analysts)
Great. Thanks for sticking me in here. Michael, maybe just to drill into the Pump Laser commentary a
bit, growing quite nicely. I think you said 80% year-over-year for the second consecutive quarter and
fourfold increase coming still effectively sold out. Can you talk a little bit about where you are in the
Rose Orchard ramp and what exit capacity looks like. And then you talked about some long-term
supply agreements that you're putting into place for scale across. Can you characterize maybe high
level, what the structure of those agreements are and the duration?
Michael E. Hurlston (Executives)
Yes, Ruben, best for last. We really always appreciate your questions. I think this is an area of incredible
strength for us, right, which really I think is underappreciated. We have a very large market share here.
And what we've done is really worked hard with, for example, a lot of the NEMs, the network
equipment manufacturers to form strategic partners. And we're super pleased with how people have
come to work with us on helping offset some of the CapEx, and it's considerable that we have to put out
to ramp in Rose Orchard. You got it right, and to then bring that into our Thailand manufacturing for
packaging and tests.
We formed a series of arrangements that for the most part, our 3-year arrangements. And those
arrangements -- as our normal arrangements, have pricing built into them, there are pricing levers that
we can exercise if certain conditions are met. So we think we have some room there on the price line.
But these are giving us a lot of surety in terms of that demand not evaporating. And in most instances, I
think they're take-or-pay, Wupen, comment since you have been the middle of that. But we feel really,
really good about where we're sitting, Ruben, on the pumps. Again, rough order, we're somewhere
between 70%, 80% share. And we believe we have a technology road map that our customers want to
engage in that will afford us the opportunity to work on price to further increase output. But this is a
darn exciting area for us.
Wupen, any additional color?
Wupen Yuen (Executives)
No, thank you.
Ruben Roy (Analysts)
That's really helpful. For the last 30 seconds here, a lot of discussion on NPO. My quick follow-up on
that is, are the discussions, engagements, that type of thing associated with some of the open or
standards-based NPO kind of, yes, I guess the standard-based NPO versus custom. And I'm asking, I'm

just wondering if there's a better alternative for you given your technology and positioning. Does that
matter...
Michael E. Hurlston (Executives)
Look, I'll have Wupen to comment just in the interest of time. I mean there are OCI, like different
standards that are coming out that are talking about the way the interface between the ASIC and the
optical engine, for example, that's great for us because that opens up switch opportunities, for example,
that may not be open to us before. So the standards-based approach is -- opens up optical TAM. But we
are engaged to be honest with you on both, right? There are a lot of custom, very specific types of
implementations that our customers are driving to. And we are -- that's really going to be our first wave
of NPO engagement moment, Ruben. Any color?
Wupen Yuen (Executives)
Maybe a little bit of color. I think just the -- to the extent what Michael just talked about, right, there is
actually 2 things. One is that today, right, the physical level, the optical level, they're all so called fast
narrow, 200 gig per lane, massive lanes. And the next generation, right, as Michael talked about will be
like OCI/MSA based, right? So that's on the optical side.
But on the form factor side, it is very much proprietary, right? Everybody has a different design. Again,
we talked about earlier, matched to their rack design, their system design, and that actually is different
from customer to customer, right? So again, optically, they are kind of standard based, but then on the
competition side, they're different between different customers.
Operator (Operator)
Thank you for your questions. I will now turn the call back to Kathy for closing remarks.
Kathryn Ta (Executives)
Thank you, Matthew. That is all the time we have for questions, and we look forward to connecting with
you at upcoming investor conferences and meetings throughout the quarter. With that, I'd like to thank
you for joining us today.
Operator (Operator)
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LITE_Q3_2026_Earnings_Call_20260505.md
- 2026-05-05｜Wajid Ali｜guidance：CFO 給 FQ4 營收指引區間 9.6 億至 10.1 億美元（原話："in the range of $960 million to"）
- 2026-05-05｜Wajid Ali｜guidance：FQ4 非 GAAP 營業利益率指引 35%–36%，EPS 2.85–3.05 美元（原話："operating margin to be in the range of 35% to 36%"）
- 2026-05-05｜Wajid Ali｜guidance：FQ4 EPS 指引假設稅率 16.5%、稀釋股數約 1.02 億（原話："effective tax rate of 16.5%"）
- 2026-05-05｜Michael E. Hurlston｜guidance：CEO 說 FQ4 成長一半以上來自元件，其餘來自系統（高速收發器與 OCS）（原話："over half of the sequential growth will stem from"）
- 2026-05-05｜Michael E. Hurlston｜guidance：管理層稱有信心達成 OFC 活動所提的單季 20 億美元營收目標（原話："very much on track to reach our $2 billion quarterly"）
- 2026-05-05｜Michael E. Hurlston｜guidance：OCS 下半年可出貨約 4 億美元，並稱 2027 年該數字續升（原話："We've outlined this sort"）
- 2026-05-05｜Wajid Ali｜margin：非 GAAP 毛利率 47.9%，季增 540bp，並列出三項驅動因素（原話："better manufacturing utilization across the majority of our"）
- 2026-05-05｜Wajid Ali｜margin：非 GAAP 營業利益率 32.2%，季增 700bp，歸因於元件營收成長（原話："primarily driven by revenue growth in components products."）
- 2026-05-05｜Michael E. Hurlston｜margin：CEO 拆解毛利率改善：工廠吸收、砍低毛利產品線、漲價（原話："we made some"）
- 2026-05-05｜Michael E. Hurlston｜margin：CEO 承認收發器毛利率落後同業（原話："I think we are underperforming peers."）
- 2026-05-05｜Michael E. Hurlston｜margin：CEO 稱 1.6T 結構上毛利率優於 800G，預期收發器毛利率墊高（原話："1.6T is definitely better. Structurally from a margin"）
- 2026-05-05｜Michael E. Hurlston｜margin：FQ4 約 20% 模組將用自家 CW 雷射，並稱此為毛利導向（原話："it would be about 20% of our"）
- 2026-05-05｜Michael E. Hurlston｜margin：CEO 稱委外代工可提升毛利，早期階段（原話："we can actually improve our margins."）
- 2026-05-05｜Michael E. Hurlston｜margin：CEO 稱部分晶圓廠（含英國廠）仍未滿載，有利用率改善空間（原話："We've historically been underutilized."）
- 2026-05-05｜Michael E. Hurlston｜risk：收發器出貨遠低於客戶需求，受關鍵零組件供給限制（原話："supply constraints on critical components keep our shipments"）
- 2026-05-05｜Michael E. Hurlston｜risk：EML 供需缺口擴大為大於 30%，前次為 25–30%（原話："The supply-demand imbalance is probably even"）
- 2026-05-05｜Michael E. Hurlston｜risk：泵浦雷射限制為突發、先前幾季未提，缺口超過 30%，需取捨分配客戶（原話："It's hit us relatively suddenly."）
- 2026-05-05｜Michael E. Hurlston｜risk：OCS 是目前最大的執行風險，且 OCS 受供應鏈限制（原話："the biggest single tight rope that we're walking"）
- 2026-05-05｜Michael E. Hurlston｜risk：被問超額供給風險，CEO 認為低，理由是客戶仍在洽談延長長約（原話："I mean, I feel it's low."）
- 2026-05-05｜Michael E. Hurlston｜risk：雷射供給近期主要靠自己，但基板 2027 年仍需持續處理（原話："as we head into 2027, we're going to continue to"）
- 2026-05-05｜Michael E. Hurlston｜competition：CEO 稱 OCS 領先地位不會永遠，但未來一年難有人出貨類似方案（原話："That's not going to last forever, right? We know that."）
- 2026-05-05｜Michael E. Hurlston｜competition：CEO 稱正在降成本、簡化 OCS 以因應中國競爭者的創新方案（原話："We are working on cost reducing."）
- 2026-05-05｜Michael E. Hurlston｜competition：稱有定價彈性，供需失衡短期不會解決（原話："We definitely have some pricing"）
- 2026-05-05｜Michael E. Hurlston｜product：本次法說新增強調 scale-across 產品組合對毛利率的貢獻（原話："it is important to outline the considerable role"）
- 2026-05-05｜Michael E. Hurlston｜product：元件營收 5.33 億、季增 20%；窄線寬雷射出貨年增逾 120%、泵浦雷射年增 80%（原話："while pump laser shipments grew 80% year-over-year."）
- 2026-05-05｜Michael E. Hurlston｜product：雲端收發器季增逾 40%，1.6T 預計 FQ4 放量（原話："we are poised to ramp 1.6T speed transceiver shipments"）
- 2026-05-05｜Michael E. Hurlston｜product：CEO 稱 scale-up CPO 仍在初期，是最大單一成長動能，scale-out CPO 與 OCS 貢獻仍小（原話："scale-up CPO is still very much in its infancy."）
- 2026-05-05｜Michael E. Hurlston｜product：自家 CW 雷射供貨時程改口：原訂日曆 Q2 導入後退後，現因外部 CW 供應吃緊而加速（原話："we backed off just seeing so much tension on the EML line."）
- 2026-05-05｜Michael E. Hurlston｜product：Q3 超高功率雷射(CPO)季增，預計 12 月季產生有意義營收，並履行 2027 上半年數億美元訂單（原話："fulfill the multihundred million dollar purchase order"）
- 2026-05-05｜Michael E. Hurlston｜product：CEO 稱 ELS 垂直整合是非主要客戶的切入點，比單供雷射更短的上市路徑（原話："a more convincing and shorter path to"）
- 2026-05-05｜Michael E. Hurlston｜customer：OCS 仍與三家客戶合作，其中兩家占大部分量體；更多訂單尚未能公布（原話："Two of"）
- 2026-05-05｜Michael E. Hurlston｜customer：CEO 稱 Google 是最大客戶之一，並驅動大量需求（原話："They're certainly one"）
- 2026-05-05｜Michael E. Hurlston｜customer：CEO 稱 v7 與 v8 的 OCS 拉貨差異小、屬增量（原話："It's incremental. It's not that big"）
- 2026-05-05｜Wajid Ali｜capital_allocation：Q3 資本支出 1.25 億美元，聚焦雲端與 AI 產能（原話："In Q3, we spent $125 million in CapEx"）
- 2026-05-05｜Wajid Ali｜capital_allocation：現金及短期投資增至 31.7 億，主因 NVIDIA 直接投資（原話："primarily driven by NVIDIA's direct investment in Lumentum."）
- 2026-05-05｜Michael E. Hurlston｜capital_allocation：購入第五座磷化銦廠（北卡 Greensboro）（原話："we expect to take advantage of a significant number"）
- 2026-05-05｜Michael E. Hurlston｜capital_allocation：Greensboro 產能不在現有數字內，2028 年才上線，約 6 季後才有顯著貢獻（原話："the Greensboro fab is not going to come online until 2028."）
- 2026-05-05｜Michael E. Hurlston｜capital_allocation：泵浦雷射 CapEx 與客戶討論預付款、照付不議或漲價分擔（原話："That can entail prepayment, that can"）
- 2026-05-05｜Michael E. Hurlston｜commitment：承諾 2026 年 12 月季 EML 單位數較去年同期成長逾 50%（原話："on track to achieve more than 50% growth in EML"）
- 2026-05-05｜Michael E. Hurlston｜commitment：正爭取長期協議以抵銷預期資本支出（原話："we are actively working to"）
- 2026-05-05｜Michael E. Hurlston｜commitment：泵浦雷射計畫未來四季在美國 Rose Orchard 廠擴產（原話："We have a plan to ramp capacity"）
- 2026-05-05｜Michael E. Hurlston｜commitment：CEO 對長期毛利率目標表示很有信心，且認為還有上升空間（原話："We feel very comfortable with that."）
- 2026-05-05｜Michael E. Hurlston｜commitment：CEO 稱 scale-up CPO 若執行得當可增加逾 50 億美元增量營收（原話："somewhere greater than $5 billion of incremental revenue"）

### LITE_Deutsche_Bank_2026_Technology_Conference_20260827.md
- 2026-08-27｜CEO Michael Hurlston｜guidance：CEO 表示公司提出新的 2028 財年每股盈餘能力目標 $40。（原話："in 2028, we figured that we can now deliver $40 of earnings power"）
- 2026-08-27｜CEO Michael Hurlston｜customer：CEO 稱最大客戶自上次財報後大幅增加 OCS 訂單。（原話："huge uptick in our order book and the order rate"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 認為先前公布的 OCS 80 億美元 TAM 被低估。（原話："the TAM now looks like it's significantly undercalled"）
- 2026-08-27｜CEO Michael Hurlston｜customer：CEO 承認目前 OCS 主要綁定單一客戶。（原話："we're predominantly today, I'd say, tied to one customer"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 稱 CPO 與 NPO 對光學產業是加成而非互相取代。（原話："completely additive to the numbers that we see today"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 稱 CPO／NPO 目前尚未反映在公司營收數字中。（原話："nothing is showing up in our number"）
- 2026-08-27｜CEO Michael Hurlston｜margin：CEO 稱 scale across 業務毛利率高且成長快但較少人討論。（原話："Our scale across business is quite high margin."）
- 2026-08-27｜CEO Michael Hurlston｜margin：CEO 說明 EML 由 100G 升到 200G 的價格倍數。（原話："you're seeing about a 2x uplift in price"）
- 2026-08-27｜CEO Michael Hurlston｜competition：CEO 稱 200G EML 目前競爭少、近期也無新進者。（原話："We don't see a lot of competitive threats on the horizon either"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 預期 1.6T 時 EML 型收發器占比降至市場的 40%～50%（800G 約 70%～80%），絕對數量仍增加。（原話："40% to 50% of the market at 1.6T"）
- 2026-08-27｜CEO Michael Hurlston｜competition：CEO 稱目前未見中國雷射供給造成影響。（原話："we see no impact from any Chinese laser supply"）
- 2026-08-27｜CEO Michael Hurlston｜competition：CEO 認為中國雷射業者趕上所需時間比外界認為的長。（原話："I think it's going to take longer than people think."）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 稱 NPO 機會近期比 CPO 更大。（原話："actually larger than the CPO opportunity, at least in the near term"）
- 2026-08-27｜CEO Michael Hurlston｜capital_allocation：CEO 說明 Greensboro 晶圓廠於 2026 初收購、2028 初才投產。（原話："it's not operational until early calendar 2028"）
- 2026-08-27｜CEO Michael Hurlston｜commitment：CEO 表示新增產能投資前需看到類似 NVIDIA 的客戶承諾。（原話："I would definitely need to see a similar type of commitment"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 稱 NPO 放量時點由原先預期的 2028 底／2029 初提前。（原話："it's a late 2027 into early 2028 event"）
- 2026-08-27｜CEO Michael Hurlston｜risk：CEO 稱 NPO 需求將對 Greensboro 晶圓廠產能造成壓力。（原話："it's going to put a lot of pressure, a lot of pressure on that Greensboro fab"）
- 2026-08-27｜CEO Michael Hurlston｜risk：CEO 稱產能最大限制是時間（認證週期長）。（原話："the headline is just time"）
- 2026-08-27｜CEO Michael Hurlston｜risk：CEO 稱基板供給緊，已在日本供應商之外再與 AXT 簽約。（原話："we went out and did another deal with AXTI"）
- 2026-08-27｜CEO Michael Hurlston｜customer：CEO 說明在 NVIDIA 的產品認證耗時一年。（原話："it was a year cycle for us to get qualified at NVIDIA"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 稱系統（模組）業務單季營收規模。（原話："running well over $200 million a quarter in that business"）
- 2026-08-27｜CEO Michael Hurlston｜margin：CEO 承認模組業務毛利率尚未改善。（原話："We've yet to fix the gross margin."）
- 2026-08-27｜CEO Michael Hurlston｜margin：CEO 承認模組毛利表現不及頂尖競爭者。（原話："We don't perform as well as the top competitors."）
- 2026-08-27｜CEO Michael Hurlston｜commitment：CEO 稱 2027 年起將著手改善製造以提升毛利。（原話："how do we fix the manufacturing?"）
- 2026-08-27｜CEO Michael Hurlston｜risk：CEO 回顧 Cloud Light 過去的品質問題。（原話："a lot of quality problems coming out of Cloud Light"）
- 2026-08-27｜CEO Michael Hurlston｜competition：CEO 不視異質整合為威脅。（原話："I don't see it as a threat"）
- 2026-08-27｜CEO Michael Hurlston｜risk：CEO 稱公司被視為美國禁中國收發器的淨受益者。（原話："We are viewed, probably correctly so as a net beneficiary"）
- 2026-08-27｜CEO Michael Hurlston｜risk：CEO 指出中國收發器廠商在美國市場的占比。（原話："make 70% of the transceivers in the U.S. market"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 指出未來 12～18 個月要觀察的重點是 scale-in（託盤內光互連）。（原話："that's the thing to watch over the next 12 to 18 months"）

### LITE_Citi_s_2026_Global_TMT_Conference_20260909.md
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜guidance：CFO 說因 OCS 能見度提高，首度提出 FY28 EPS $40 指引（原話："putting out a fiscal year '28 guidance on EPS of $40"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜customer：OCS 上行來自最大客戶，原因是需出貨更多單位（原話："that OCS upside is coming from our largest customer"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜guidance：FY28 $40 EPS 涵蓋所有季度，OCS 貢獻隨季度線性疊加（原話："layering in linearly and increasing as we move through"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜commitment：CFO 表示對達成 $40 有信心，並指出賣方模型（含主持人）EPS 較低（原話："we have all the confidence that we'll be able to meet"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜guidance：被問 $40 隱含的毛利率等，CFO 不拆解，僅提及賣方模型偏低（原話："I'm hesitating to say that because we did see the sell-side"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜risk：管理層稱供需缺口仍在擴大，雷射、EML、CPO 雷射皆短缺，2027 不會緩解（原話："we don't see the shortage going away in '27"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜margin：管理層稱新交易定價等於或高於先前已上調的價格，並依價格與加急費分配產能（原話："All the deals we're making today are equal or higher pricing"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜product：CPO 時程不變但需求量提高，先用於 scale-out 交換器，2027 下半年用於 scale-up（原話："No change in timing, but intensity is actually increasing"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜product：對 scale-up 市場的看法改變：由單一客戶故事變成全產業，CPO 與 NPO 約各半（原話："CPO will be half of the market. NPO is the other half"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜product：管理層稱 NPO 是機會的淨增加（先前只想到 CPO）（原話："the NPO is a net addition to our opportunity"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜competition：高功率雷射只看到 Coherent 一家競爭者（NVIDIA 也與其簽 LTA）（原話："We see one competitor, right, who is Coherent"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜competition：管理層稱中國 CW 雷射供應主要針對可插拔市場，NPO/CPO 需 120-150mW 以上高功率（原話："targeted today to serve the pluggable market"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜capital_allocation：UHP 雷射三波擴產：San Jose、英國 2Q27 起、Greensboro 2Q28 或 mid-28 起（原話："We will start to ramp in second quarter 2028 or mid-'28"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜risk：擴產時程最大變數為客戶認證（PCN）時間（原話："change the schedule is the qualification timing"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜capital_allocation：新產能採新增而非取代現有產品線，含 6 吋產能（原話："So by and large, we don't sacrifice, we add."）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜product：首個 ELS 勝利來自現有 CPO 客戶，預計 2027 下半年出貨，估計取得其 15-20% 份額（原話："maybe 15% to 20% of their fleet is about the right amount"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜commitment：CFO 預告未來數個月內可能公布首位 NPO 客戶，目前尚無 NPO 勝利公告（原話："we can expect to see something in the next handful"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜product：1.6T/200G 每通道已超過 EML 出貨組合 25%，100G EML 仍為主力（原話："we exceed 25% of the mix"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜competition：EML 未見中國新進入者作為合約競爭者，EML 定價維持有利（原話："our EML pricing remains very favorable"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜competition：管理層認為 400G/lane 時 InP 有機會重拿 100G 世代的份額，矽光與薄膜鈮酸鋰各有限制（原話："indium phosphide has a good chance of regaining the share"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜margin：CW 雷射良率已高於 EML、價格相近，毛利輪廓不及 EML 但接近（原話："our laser yield has climbed up to be higher than EMLs"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜product：OCS 每顆 XPU 搭載率仍約 1.5:1，新拓撲互有增減後大致持平（原話："it still ends up roughly 1.5:1"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜product：OCS 先前 $8B TAM 估計看到上行（動態叢集、容錯網路應用），約 2028 底至 2029 初可見（原話："So that probably puts upside to that $8 billion number."）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜competition：Coherent 追上高功率雷射的時程管理層表示不知道，稱客戶需要第二來源（原話："We frankly don't know, right?"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜customer：scale-across 帶動泵浦雷射，預期未來約 5 季量增 4 倍，並與主要網通設備商簽多年 LTA 且價格較高（原話："a 4x multiplier on our volume of pump lasers"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜commitment：管理層聲稱公司定位將涵蓋 scale across 到 scale in（原話："Lumentum's best days are yet to come"）

### LITE_Lumentum_Holdings_Inc_Marvell_Technology_Inc_M_A_Call_20261102.md
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜capital_allocation：Marvell 宣布與 Lumentum 合併（收購），Lumentum CEO 與另兩位董事將在交割後進入 Marvell 董事會（原話："Michael and 2 other members of the Lumentum Board will join"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜guidance：合併後 2030 年合計 TAM 估 5500 億美元，增量主要來自 NPO 與 CPO（原話："a combined TAM of $550 billion in 2030"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜customer：Lumentum CEO 宣布第二個大型 NPO／CPO 訂單，預期帶來逾 50 億美元營收（原話："our second major NPO and CPO win"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜competition：Lumentum CEO 說明考慮過獨立發展與自行收購等替代方案後選擇與 Marvell 合併（原話："continuing to execute as a stand-alone company"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜product：Lumentum CEO 描述銅牆外移，scale-up 光學頻寬比 scale-out 再高 10 倍（原話："optics which carry another 10x increase in bandwidth"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜commitment：雙方承諾維持既有 go-to-market 模式，繼續供應元件與系統給整個生態系（原話："we plan to maintain our existing go-to-market model"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜product：Lumentum 的 MEMS 光路交換器（OCS）被客戶越來越多採用，與網路交換器預期並存（原話："optical circuit switching are expected to coexist"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜capital_allocation：Marvell 說將與供應鏈夥伴投入數十億美元確保產能（原話："investing multiple billions of dollars"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜capital_allocation：Lumentum 稱磷化銦晶圓廠為皇冠上的寶石，正積極擴產（原話："we are investing aggressively to expand our capacity"）
- 2026-11-02｜CFO (Marvell, Daniel Durn)｜guidance：CFO 預期交易使非 GAAP 毛利率與營業利益率增益，含逾 10 億美元年化協同效益，主要來自 COGS（原話："run rate synergies we primarily see from COGS"）
- 2026-11-02｜CFO (Marvell, Daniel Durn)｜guidance：CFO 預期交易於交割後第 1 年起對非 GAAP EPS 增益（原話："accretive to non-GAAP EPS starting in year 1 post close"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜margin：CEO 引用備考數字：年化營收 177 億美元、非 GAAP 營業利益率 39%（依 Marvell 當季指引與 Lumentum 當日財報）（原話："$17.7 billion in annualized revenue"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜guidance：合併 Lumentum 下一財季指引與 Marvell 共識，備考年化營收逾 210 億美元、營業利益率低 40% 區間（原話："pro forma annualized revenue of over $21 billion"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜guidance：增量 TAM 約 600 億美元，近期協同一部分反映在 COGS，另有營收協同（原話："incremental of $60 billion"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜customer：管理層稱關鍵客戶在交易傳出後與週末皆表達強力支持（原話："there's just tremendous support for the combination"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜competition：Lumentum 雷射供應給幾乎所有（競爭）模組廠，生態系為 co-opetition（原話："we supply our lasers to almost all of our competitors"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜commitment：Marvell 稱元件供應策略不變，首要任務仍是 DSP 等領先與供應雷射（原話："That strategy is not going to change."）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜risk：分析師問及雷射供需；Marvell 稱供給吃緊非此時交易的原因，磷化銦與記憶體同屬供給受限（原話："tight supply is not the reason we're wanting to enter"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜risk：Marvell CEO 承認 Marvell 自身亦有供給短缺，並稱 Lumentum 情況無不同（原話："Marvell's got supply shortages. I mean we're behind."）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜guidance：Lumentum CEO 稱去年營收翻倍，多數人預期明年再翻倍，管理層未見改變（原話："Most people have us doubling again next year"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜capital_allocation：Lumentum CEO 說明出售動機：放棄控制權，因認為合併 #1 優於收購多家 #2～#4（原話："why would we go out and buy a string of pearls"）
- 2026-11-02｜CFO (Marvell, Daniel Durn)｜guidance：CFO 稱 Analyst Day 的獨立目標（800 億美元營收）仍成立，本交易為增量（原話："everything we put forward at the Analyst Day"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜product：Marvell 稱增量 TAM 多在 scale-up，後期在 scale-in，結合 Lumentum micro-VCSEL 與 Marvell EIC（原話："best-in-class micro-VCSEL technology"）

### 問答異常語氣（迴避／改口／保留）
- LITE_Q3_2026_Earnings_Call_20260505.md｜問：Michael Mani：若滿足所有需求，收發器可有多大；缺口相對 30%？｜答法：未給收發器缺口數字，稱「沒算過」，僅說在同一量級(ZIP code)；並澄清 30% 僅指 EML
- LITE_Q3_2026_Earnings_Call_20260505.md｜問：Ryan Koontz：scale-across 市場規模、多軌放大機會多大？｜答法：兩位主管均未量化，稱「之後適當時機再給」，僅用 huge、significant 形容
- LITE_Q3_2026_Earnings_Call_20260505.md｜問：Sahej Singh：毛利率 waterfall 拆解(mix/CapEx/量價)｜答法：未給各因素占比，只列舉 mix、利用率、價格，並重申長期目標「很有信心」
- LITE_Q3_2026_Earnings_Call_20260505.md｜問：Samik Chatterjee：OCS 新增訂單進度與規模｜答法：稱「too early to call」不給時程，僅說規模 quite sizable
- LITE_Q3_2026_Earnings_Call_20260505.md｜問：Vijay Rakesh：Google v8 對 OCS 2027–28 的影響｜答法：拒評特定客戶與架構，僅說 v7→v8 拉貨差異屬增量
- LITE_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：FY28 $40 EPS 隱含的毛利率或其他損益項目為何？｜答法：未提供任何隱含數字，改談賣方模型偏低與對 $40 的信心
- LITE_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：Coherent 追上高功率雷射需要 12 或 18 個月？｜答法：不給時程，稱不知道，改談客戶需要第二來源
- LITE_Lumentum_Holdings_Inc_Marvell_Technology_Inc_M_A_Call_20261102.md｜問：Tom O'Malley（Barclays）請 CFO 給出 10 億美元協同中 COGS 占比（90%？95%？）及主要來源拆解｜答法：CFO 未給百分比或分項金額，改談結合後營收規模、毛利率與長期可擴大協同
- LITE_Lumentum_Holdings_Inc_Marvell_Technology_Inc_M_A_Call_20261102.md｜問：Tore Svanberg（Stifel）問 Analyst Day 的互連營收成長（60–70%、375 億美元）在合併後如何調整｜答法：Murphy 稱「our numbers, we haven't provided them」，未給更新數字，只說仍在軌道上、TAM 更大
- LITE_Lumentum_Holdings_Inc_Marvell_Technology_Inc_M_A_Call_20261102.md｜問：Vivek Arya（BofA）問是否競價流程、是否可能有其他出價者，以及是否買在短缺高峰（隱含約 1 倍 2030 TAM）｜答法：兩位管理層均未回答是否有競爭出價者；估值問題以供需、設計定案與資料可見度回應，未談價格倍數

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
{"date":"20260812","verdict":"觀望","role":"候選/追蹤池","H":{"status":"ok","format":"table","rows":[{"id":"H1（2Y）","text":"200G/lane EML 供需缺口持續，LITE 為唯一量產供應商，GM 維持 40%+以上","columns":{"驗證指標":"季度 GM 軌跡","2026-06-27→2026-08-12 邊際變化":"🟢 強化：GM 44.2%→50.4%，超越假設上緣"}},{"id":"H2（2Y）","text":"FY27 EPS 較 FY26 成長 &gt;100%","columns":{"驗證指標":"共識 FY27 EPS","2026-06-27→2026-08-12 邊際變化":"🟢 強化：共識 $18.13→$18.73，且 Q1 guide 中值 $4.20 遠超共識 $3.63，年化路徑上修"}},{"id":"H3（5Y）","text":"OCS/CPO 第二引擎能撐起 EML 缺貨紅利消退後的估值","columns":{"驗證指標":"OCS營收guide兌現率、CPO 首批出貨時程","2026-06-27→2026-08-12 邊際變化":"🟢 強化：Q1FY27 guide已內含首個三位數（$100M+）營收季（原判仍待驗證的「一整季軌跡」已提前在guide中出現），OCS出貨量Q3→Q4已翻倍，管理層預期2027年初超車成該大客戶OCS第一供應商；仍待實際兌現驗證"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE(FY27基礎，隨最新共識滾動重算)回落至≤32x或5Y分位<70%；或GM連續4季維持>48%；生意面前提：COHR 200G/lane EML於任一top hyperscaler/NVIDIA完成客戶認證前，估值觸發不因股價波動單獨視為安全邊際打開","irr_base_pct":7.5,"ev5y_pct":39.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"候選/追蹤池","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.3,"ev5y_pct":39.0,"irr_base_pct":7.5,"max_dd_pct":-58.0,"bull_5y_price":1948.8,"bear_5y_price":411.9,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE(FY27基礎，隨最新共識滾動重算)回落至≤32x或5Y分位<70%；或GM連續4季維持>48%；生意面前提：COHR 200G/lane EML於任一top hyperscaler/NVIDIA完成客戶認證前，估值觸發不因股價波動單獨視為安全邊際打開","price_at_dd":820.59,"archetype":"品質複利成長","cycle_position":"晚循環/過熱頂部"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LITE_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
