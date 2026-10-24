你是 stock-analyst **v20 判斷 agent**，標的 LRCX（20261024）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"LRCX","date":"2026-10-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LRCX_20261024/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LRCX_20261024/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":8219.4,"period":"季末 2026-09-27 季度（公告 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"季末 2026-09-27 季度（公告 2026-10-21）","citation":"公司新聞稿 newsroom.lamresearch.com 2026-10-21"},"note":"上季指引 8.1B±0.4B，實績高於中點；共識數字未查"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益率","value":40.2,"period":"季末 2026-09-27 季度（公告 2026-10-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"季末 2026-09-27 季度（公告 2026-10-21）","citation":"公司新聞稿 newsroom.lamresearch.com 2026-10-21"},"note":"未查"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益率","value":40.0,"period":"季末 2026-09-27 季度（公告 2026-10-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"季末 2026-09-27 季度（公告 2026-10-21）","citation":"公司新聞稿 newsroom.lamresearch.com 2026-10-21"},"note":"未查"},{"id":"f_kpi5_2026_12","label":"下一季指引（2026-12 季）：營收","value":"8,600±400 百萬美元","period":"季末 2026-09-27 季度公告（2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"季末 2026-09-27 季度公告（2026-10-21）","citation":"公司新聞稿 newsroom.lamresearch.com 2026-10-21"},"note":"未查"},{"id":"f_kpi6_eps","label":"下一季指引：毛利率／營業利益率／EPS","value":"毛利率 52.5%±1%；營業利益率 40.5%±1%；EPS $2.33±0.15（GAAP 與 non-GAAP 同）","period":"季末 2026-09-27 季度公告（2026-10-21）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"季末 2026-09-27 季度公告（2026-10-21）","citation":"公司新聞稿 newsroom.lamresearch.com 2026-10-21"},"note":"未查"},{"id":"f_kpi7","label":"遞延收入","value":2660,"period":"季末 2026-09-27（公告 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"季末 2026-09-27（公告 2026-10-21）","citation":"公司新聞稿；不含日本客戶出貨"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-21","period":"2026-10-21","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-21"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_lrcx_gross_margin_pct","label":"LRCX 毛利率","value":50.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LRCX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lrcx_operating_margin_pct","label":"LRCX 營業利益率","value":35.29,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LRCX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lrcx_fcf_margin_pct","label":"LRCX FCF 利潤率","value":21.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LRCX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_asml_gross_margin_pct","label":"ASML 毛利率","value":52.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_asml_operating_margin_pct","label":"ASML 營業利益率","value":35.42,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_asml_fcf_margin_pct","label":"ASML FCF 利潤率","value":24.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amat_gross_margin_pct","label":"AMAT 毛利率","value":49.4,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amat_operating_margin_pct","label":"AMAT 營業利益率","value":31.09,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amat_fcf_margin_pct","label":"AMAT FCF 利潤率","value":18.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_klac_gross_margin_pct","label":"KLAC 毛利率","value":61.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_klac_operating_margin_pct","label":"KLAC 營業利益率","value":41.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_klac_fcf_margin_pct","label":"KLAC FCF 利潤率","value":27.74,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3","label":"自由現金流（營業現金流減資本支出，自算；公司未報）","value":3240.0,"period":"季末 2026-09-27 季度（公告 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"季末 2026-09-27 季度（公告 2026-10-21）","citation":"公司新聞稿現金流量表：營業現金流 3,497.7、資本支出含無形資產 257.7；FCF 為自算"},"note":"未查"},{"id":"f_kpi4_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":3.5,"period":"季末 2026-09-27 季度（公告 2026-10-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"季末 2026-09-27 季度（公告 2026-10-21）","citation":"新聞稿 equity-based compensation 114.7 百萬美元 ÷ GAAP 營業利益 3,283.7（自算）；占營收 1.4%"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":230.1,"period":"2026-10-23（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-13.92,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":24.56,"period":"2026-10-23（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.63 → 9.63）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.33,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.11 → 12.15）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.21,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（14.41 → 14.44）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":9.63,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":12.15,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":14.44,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":16.87,"period":"2026-07-30 → 2026-10-24","unit":"%","basis":"FY1 共識 EPS 8.24 → 9.63（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":34.29,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝37.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":37.8,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":11.02,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝44.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":44.1,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":10.88,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝43.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":43.4,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":23.89,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 9.63，分子＝快照價 230.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.482,"period":"2026-10-24","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-24"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-3701.94,"period":"2026-10-24","unit":"USD m","basis":"yfinance 最新一季：總債務 3735.44、現金 7437.38（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1251.42,"period":"2026-10-24","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":284250.82,"period":"2026-10-24","unit":"USD m","basis":"市值 287952.76 ＋ 淨負債 -3701.94","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":35389.96,"period":"2026-10-24","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（29 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":42680.21,"period":"2026-10-24","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（28 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":8.03,"period":"2026-10-24","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟢","period":"2026-10-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 230.1 / W52 258.49 / W104 173.62 / W250 108.7 / W250 13週斜率 3.42%"},{"id":"f_ma_w52","label":"52 週均線","value":258.49,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":173.62,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":108.7,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":3.42,"period":"2026-10-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列示主要對手：沉積為 Applied Materials；ALD/PECVD 另有 ASM International、Wonik IPS；蝕刻為 Applied、Hitachi、Tokyo Electron；濕洗為 Screen、Semes、Tokyo Electron。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"Our primary competitor in the dielectric and metals deposition market is Applied Materials, Inc. For ALD and PECVD, we also compete against ASM International and Wonik IPS. In the etch market, our primary competitors are Applied Materials, Inc.; Hitachi, Ltd.; and Tokyo Electron, Ltd.","as_of":"2026-08-07","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 指出中國本土設備商可能因在地化政策加劇競爭，且美國出口管制使不受限的國際對手取得優勢。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"Government and other initiatives to encourage local semiconductor manufacturing and supply chain in countries outside of the U.S., including China, could increase competition from domestic equipment and spare parts manufacturers in those countries.","as_of":"2026-08-07","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：若無法跟上 AI 需求擴產，可能流失市占。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"If we are unable to effectively scale our business to meet our customers’ requirements in response to AI-driven demand, we may lose market share","as_of":"2026-08-07","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Lam 管理層稱 2025 年 SAM 占 WFE 達 mid-thirties%，朝 high-thirties 目標前進；出貨占比年增逾 1 個百分點。","source":"Lam Research Q2 2026 (Dec-quarter 2025) earnings call transcript, AOL","url":"https://www.aol.com/articles/lam-research-lrcx-q2-2026-233812445.html","excerpt":null,"as_of":"2026-01-28","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"NAURA 2025 年全球設備銷售排名升至第五，中國本土蝕刻/沉積業者擴張。","source":"China Daily via SSE: Three Chinese firms enter world semiconductor industry top 20","url":"https://english.sse.com.cn/news/newsrelease/voice/c/c_20260204_10808424.shtml","excerpt":"top 20 by sales for the first time in 2025, according to data from Japanese research firm Global Net. This marks a rise from just one company in the pre-US-government-restriction era of 2022, underscoring accelerated progress in bolstering the domestic supply chain. The sales ranking reveals a big climb for State-backed Naura Technology Group, which jumped from eighth place in 2022 to fifth","as_of":"2026-02-04","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因素：Lam 銷售集中於少數大客戶，大客戶可能談判降價、增加成本、壓低毛利並限制技術分享；未見客戶導入第二供應商或自製的具體披露。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"Sales to a limited number of large customers constitute a significant portion of our overall shipments, revenue, cash flows, and profitability.","as_of":"2026-08-07","retrieved_at":"20261024","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 四家客戶分別占總營收約16%、15%、12%、12%；FY2025 兩家約17%、15%；FY2024 一家約17%。","source":"SEC EDGAR LRCX 10-K FY2026 Item 8","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"In fiscal year 2026, four customers accounted for approximately 16%, 15%, 12%, and 12% of total revenues, respectively. In fiscal year 2025, two customer accounted for approximately 17% and 15% of total revenues. In fiscal year 2024, one customer accounted for approximately 17% of total revenues, respectively.","as_of":"2026-08-07","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2026-06-28 應收帳款五家客戶分別占約20%、16%、15%、11%、10%；呆帳備抵金額不重大。","source":"SEC EDGAR LRCX 10-K FY2026 Item 8","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"As of June 28, 2026, five customers accounted for approximately 20%, 16%, 15%, 11%, and 10% of accounts receivable, respectively.","as_of":"2026-08-07","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"主要客戶為 Micron、Samsung、SK hynix、TSMC。","source":"SEC EDGAR LRCX 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"Our most significant customers during the fiscal years ending June 28, 2026, June 29, 2025, and June 30, 2024 included Micron Technology, Inc., Samsung Electronics Company, Ltd., SK hynix Inc., and Taiwan Semiconductor Manufacturing Company.","as_of":"2026-08-07","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"中國區占營收約34%（FY2026）、34%（FY2025）、42%（FY2024），受出口管制影響。","source":"SEC EDGAR LRCX 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"Revenue in China, which includes global customers and domestic Chinese customers with manufacturing facilities in China, represented approximately 34%, 34%, and 42% of our total revenue for fiscal years 2026, 2025, and 2024, respectively.","as_of":"2026-08-07","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SEMI 2026 年中預測：設備銷售 2026 年 1659 億美元（+23.2%），2028 年達 2295 億美元；WFE 2027 年 +21.8%、2028 年 +14.1%，上修主因 AI 基建、HBM 相關 DRAM 投資與先進邏輯。","source":"SEMI press release (mid-year forecast)","url":"https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-forecast-to-reach-a-record-229-billion-dollars-in-2028-semi-reports","excerpt":null,"as_of":"2026-07-14","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce：DRAM 實質產出多在 2027 下半年爬升、2028 才放量；NAND 2H27 隨新產能放鬆。","source":"TrendForce press center 2026-07-30","url":"https://www.trendforce.com/presscenter/news/20260730-13158.html","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Lam 將 2026 WFE 看法上修至 1500 億美元出頭；CEO 稱 2027 為 WFE 成長的「extraordinary setup」，DRAM 領先。","source":"TIKR: What Lam Research's Q4 Earnings Call Reveals About the 2027 Setup","url":"https://www.tikr.com/blog/what-lam-research-q4-earnings-call-reveals-about-the-2027-setup","excerpt":"$400M, implying over 20% sequential growth, while raising its 2026 WFE outlook to the low $150B range from $140B. Memory Mix Flips: NAND revenue doubled sequentially, pushing memory to 46% of systems revenue from 39% in March. Archer Calls 2027 Setup Extraordinary: CEO Tim Archer said the company sees “an extraordinary setup for WFE growth” heading into 2027, with DRAM leading growth again","as_of":"2026-07-30","retrieved_at":"20261024","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Korea Herald：下一輪記憶體週期由供給而非需求決定。","source":"Korea Herald","url":"https://www.koreaherald.com/article/10805993","excerpt":"Supply, not demand, will define next memory cycle, analysts say A construction site at the Yongin Semiconductor Cluster industrial complex in Yongin, Gyeonggi Province (Yonhap)","as_of":"2026-07-12","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Korea Times：設備取得成為韓國晶片擴產的新變數。","source":"Korea Times 2026-10-17","url":"https://www.koreatimes.co.kr/business/companies/20261017/securing-equipment-emerges-as-new-variable-for-koreas-chip-expansion-plans","excerpt":null,"as_of":"2026-10-17","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2026 10-K 風險因素僅將反壟斷法規列為一般適用法規之一，未載明具體反壟斷調查；三次搜尋亦查無 2026 年針對 Lam 的 DOJ／FTC／EU 反壟斷案。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"We are subject to the laws of multiple jurisdictions and the rules and regulations of various governing bodies, including, but not limited to, those related to import and export controls and other trade restrictions, national and economic security (including receipt or use of designated technologies), intellectual property rights, taxes, financial and other disclosures, corporate governance, data protection, privacy, anti-corruption, such as the Foreign Corrupt Practices Act and other local laws prohibiting corrupt payments to governmental officials, anti-boycott compliance, conflict minerals or other social responsibility legislation, immigration or travel regulations, antitrust regulations,","as_of":"2026-08-07","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2026 10-K：中國區營收約占總營收 34%（FY2026）、34%（FY2025）、42%（FY2024）；出口許可要求擴大已限制市場、影響營收，未來可能更嚴重。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"Revenue in China, which includes global customers and domestic Chinese customers with manufacturing facilities in China, represented approximately 34%, 34%, and 42% of our total revenue for fiscal years 2026, 2025, and 2024, respectively.","as_of":"2026-08-07","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2026 10-K：美國對鋼、鋁進口課關稅推高 FY2026 製造成本，壓低毛利；部分國際銷售依賴取得出口許可。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"For example, our business requires steel and aluminum to manufacture our products, and the imposition of tariffs on steel and aluminum imports into the United States increased our manufacturing costs in fiscal year 2026, which adversely impacted our margins.","as_of":"2026-08-07","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2026 10-K：客戶及下游業者亦可能受關稅、出口管制影響，進而衝擊對公司產品的需求。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"Our customers (and their customers and other downstream parties) may also be adversely affected by the tariffs, export controls, and other trade issues described above.","as_of":"2026-08-07","retrieved_at":"20261024","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026 年 4 月美國國會推進 MATCH Act，擬收緊對中國晶片廠的先進蝕刻／沉積設備出口管制，Lam 被點名於討論中。","source":"Simply Wall St 轉述","url":"https://simplywall.st/stocks/us/semiconductors/nasdaq-lrcx/lam-research/news/potential-us-china-chip-talks-reframe-lam-research-risk-and","excerpt":"On the flip side, if talks stall or result in only narrow exemptions, Lam would still be operating with the same licensing uncertainty around advanced etch and deposition tools.","as_of":"2026-05-18","retrieved_at":"20261024","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2015 10-K 揭露：部分元件與次組件僅能向單一或少數供應商採購（歷史揭露，非最新）","source":"Lam Research Form 10-K FY2015 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000707549/000119312515290023/d937085d10k.htm","excerpt":"In some cases, the requirements of our business mandate that we obtain certain components and sub-assemblies included in our products from a single supplier or a limited group of suppliers.","as_of":"2015-08-01","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中國相關營收約占 34%，美國出口許可限制已影響營收並加劇外國競爭","source":"Lam Research Form 10-Q (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000707549/000070754926000054/lrcx-20260927.htm","excerpt":"or technology transfers for which export licenses are required, has limited and could in the future further limit the market for our products and services and our ability to carry out R&D activities globally, which has had and could in the future have an adverse impact on our revenues. As is discussed below under the heading “Our Sales to Customers in China, a Significant Region for Us, Have","as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"公司預期 2026 年中國占比降至 30% 以下，因新增對部分中國客戶出貨限制","source":"Zacks","url":"https://www.zacks.com/stock/news/2817050/will-lrcxs-china-revenue-drop-below-30-hurt-2026-growth-outlook","excerpt":null,"as_of":"2026-01-30","retrieved_at":"20261024","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"6月季（FY26Q4）營收 $6.72B，QoQ +15%、YoY +30%；FY 營收 +26% 至 $23.23B。系統營收組合：Foundry 44%（前季 54%）、NAND 23%（前季 12%，NAND 營收季增逾一倍）、DRAM 23%（前季 27%，金額與 3 月紀錄持平）。9月季指引 $8.1B ±$0.4B；客戶支援業務 YoY +43% 至 $2.47B。","source":"MarketBeat, Lam Research Q4 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/lam-research-q4-earnings-call-highlights-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Lam 初步預估 CY27 晶圓製造設備（WFE）逾 $200B，CY26 約 $150B，由 DRAM、NAND、晶圓代工/邏輯驅動；2027 成長由 DRAM 領先，其次先進邏輯與 NAND。此數字僅單一來源（Newsquawk），須對照法說逐字稿。","source":"Newsquawk, earnings call: Lam preliminary CY27 WFE outlook exceeds USD 200bln","url":"https://www.newsquawk.com/headlines/earnings-call-lam-research-lrcx-says-its-preliminary-cy27-wafer-fabrication-equipment-outlook-exceeds-usd-200bln-exp-cy26-usd-150bln-driven-by-dram-nand-and-foundrylogic-demand","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Lam 稱其 SAM 占 WFE 比重 2025 年擴至 mid-30s%，目標 high-30s；出貨份額年增逾 1 個百分點；中國營收占比預期下降（2026 中國 WFE 持平）。Lam 為蝕刻龍頭、沉積第二（Pitchbook/Morningstar 說法）；Komo 稱乾蝕刻約 55%（未獨立證實）。","source":"Lam Research Q2 FY2026 earnings call transcript (AOL); Pitchbook profile","url":"https://www.aol.com/articles/lam-research-lrcx-q2-2026-233812445.html","excerpt":null,"as_of":"2026-01-28","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"SEMI 年中預測：2026 全球半導體設備（OEM）銷售 $165.9B，YoY +23.2%，2028 達 $229.5B；WFE 2027 +21.8%、2028 +14.1%，達 $200B；測試設備 2026 $15.3B（+31.0%），封裝設備 $6.7B（+9.6%）。","source":"SEMI Mid-Year Total Semiconductor Equipment Forecast – OEM Perspective","url":"https://semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Lam 10-K 列出技術快速變遷為風險：公司須持續開發新產品以因應製程技術變化，產品若在市場失敗或不及競品改良版，可能損失市占；10-K 未點名具體替代技術。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"Rapid technological changes in semiconductor manufacturing processes subject us to increased pressure to develop technological advances that enable those processes.","as_of":"2026-08-07","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 產品集中風險項下列有「技術變化我們無法因應」與「競爭對手改良版產品」等情境。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"an improved version of products being offered by a competitor in the markets in which we participate; •increased pressure from competitors that offer broader product lines; •increased pressure from regional competitors; •technological changes that we are unable to address with our products;","as_of":"2026-08-07","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"FQ4 2026 (Jun 2026 季) 指引營收約 $6.60B±$0.40B、non-GAAP EPS 約 $1.65±$0.15；7/22 財報前預覽的共識為營收 $6.66B、EPS $1.68，略高於指引中點。","source":"MarketBeat / iTiger 財報預覽搜尋摘要（Erste Group 2026-06-30 一文及 itiger 預覽）","url":"https://www.itiger.com/news/1106995403","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ4 2026 實際營收約 $6.72B；公司指引 9 月季營收 $8.10B±$0.4B、non-GAAP EPS $2.15±$0.15，毛利率 52%（Benzinga 報導）；RBC 上調 FY2026/FY2027 EPS 至 $5.65/$7.72。","source":"stock3 / placera（RBC）搜尋摘要","url":"https://stock3.com/news/lam-research-guidance-fuer-81-mrd-usd-ein-neues-niveau-17212540","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261024","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 彙整（2026 年 8 月底）：22 位分析師 21 買 1 持有，平均目標價 $342；Mizuho 8/25 目標價 $370→$365，Morgan Stanley 7/30 $404→$367。目標價已由年初約 $280 升至約 $340。","source":"Benzinga LRCX price targets","url":"https://kr.benzinga.com/quote/LRCX/price-targets","excerpt":null,"as_of":"2026-08-25","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ3 2026（2026-04-22 公布）營收 $5.84B 高於共識約 $5.70–5.74B，EPS $1.47 高於共識 $1.36，指引亦高於共識。","source":"搜尋摘要（低品質鏡像站，待核）","url":null,"excerpt":null,"as_of":"2026-04-22","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"8-K 顯示 FQ1 2027（Dec 2026 季）指引營收 $8.60B±$0.4B","source":"SEC 8-K Exhibit 99.1 Q1 FY2027","url":"https://www.sec.gov/Archives/edgar/data/0000707549/000070754926000052/lrcx_exhibitx991xq1x2027.htm","excerpt":"For the quarter ending December 27, 2026, Lam is providing the following guidance: U.S. GAAP Reconciling Items Non-GAAP Revenue $8.60 Billion +/- $400 Million — $8.60 Billion +/- $400 Million","as_of":"2026-10-22","retrieved_at":"20261024","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"SEC EDGAR 8-K 清單：2025-10-24 至 2026-10-24 共 8 份 8-K，含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000707549&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"SEMI 3Q26 300mm Fab Outlook：2026 全球 300mm 晶圓廠設備支出約 1490 億美元（年增 31%），2029 年達 2270 億美元；2026 年 20 座新廠／產線動工、2027 年 18 座；完工投產由 2026 年 13 座增至 2027 年 23 座。","source":"SEMI press release / The Star 2026-10-14 (secondary summary)","url":"https://www.semi.org/en/semi-press-release/global-300mm-fab-equipment-spending-to-reach-227-billion-in-2029-as-buildout-accelerates-semi-projects","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Lam 年報稱公司過去四年製造產能幾乎翻倍；另宣布未來五年投入逾 30 億美元擴 R&D 實驗室網絡（實驗產能增逾 50%），及 15 億美元 Tualatin 奧勒岡園區擴建（大樓 2028 年啟用）。","source":"Lam Research Form ARS FY2026 (SEC); PRNewswire via quantisnow 2026-08-13; sentisense 2026-08-27","url":"https://www.sec.gov/Archives/edgar/data/0000707549/000114036126037568/ef20082688_ars.pdf","excerpt":null,"as_of":"2026-08-27","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"同業 Applied Materials CFO 稱目標 2028 年前將季度半導體系統產出倍增，並規劃進一步擴產以支應至 2030 年需求；Tokyo Electron 2026 年 1 月報導 FY26 資本支出上調 48% 創高。搜尋未找到任何明示『供給紀律』的陳述。","source":"Dow Jones via iTiger; TrendForce News","url":"https://www.itiger.com/news/2659939721","excerpt":null,"as_of":"2026-01-31","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Tokyo Electron FY26 資本支出上調 48%","source":"TrendForce News","url":"https://www.trendforce.com/news/?p=51413","excerpt":"[News] Tokyo Electron Reportedly Raises FY26 CapEx 48% to Record High, Bets on DRAM Etching Demand 2026-01-09 Semiconductors editor Rising memory prices are expected to lift production and drive stronger demand for chipmaking equipment.","as_of":"2026-01-09","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Lam Research FY2026 Q2 財報電話會議：存貨週轉 2.7 次，高於前一季 2.6 次","source":"AOL, Lam Research LRCX Q2 2026 Earnings Call Transcript","url":"https://www.aol.com/articles/lam-research-lrcx-q2-2026-233812445.html","excerpt":null,"as_of":"2026-01-28","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Lam Research FY2026 10-K：日本客戶出貨在驗收前以成本列為存貨，預估未來營收約 4.902 億美元","source":"SEC, Lam Research Form 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0000707549/000070754926000037/lrcx-20260628.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"SEMI：2001 年全球設備出貨額 281 億美元，較 2000 年 477 億美元下滑約 41%","source":"SEMI: Worldwide equipment market dropped $28 billion in 2001 (Semiconductor Digest)","url":"https://sst.semiconductor-digest.com/?p=26003","excerpt":"worldwide billings totaled $28.1 billion in 2001, compared with $47.7 billion posted in 2000.","as_of":"2002-03-01","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Lam 2023 年 3 月季 GAAP 毛利率 41.5%（去年同期 44.7%），為該輪下行低點；FY2023 全年 44.6%，FY2022 45.7%","source":"Motley Fool 2023-04-25；Lam 10-K FY2023","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754923000102/lrcx-20230625.htm","excerpt":"Percent of revenue 44.6% 45.7% 46.5%","as_of":"2023-08-15","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"TechInsights（Hutcheson）：1963 年以來 14 次衰退期，約每 4.4 年一次，設備平均衰退約 20%，半導體約 8%；循環變頻繁但幅度趨緩","source":"TechInsights, The Chip Insider – Cyclical History of the Semiconductor Industry","url":"https://www.techinsights.com/blog/chip-insiderr-cyclical-history-semiconductor-industry","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Lam 出貨量 2000 年 12 月至 2001 年 12 月下滑 80%；設備營收 1998-2002 峰谷下滑 67%","source":"Machine Design, Semicon West show conditions much worse than 2001","url":"https://www.machinedesign.com/news/semicon-west-show-conditions-much-worse-2001","excerpt":null,"as_of":"2001-07-01","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K無併購相關項目（1.01／2.01）；搜尋亦無2025–2026併購。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000707549&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2026 10-K 風險因素僅以假設語氣提及證券集體訴訟（「If we are sued」），未揭露實際案件。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm","excerpt":"If we are sued in a securities class action, we could incur substantial costs, and it could divert management’s attention and resources and have an unfavorable impact on our financial performance and the price for our Common Stock.","as_of":"2026-08-07","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K清單無Item 4.02（財報不可信賴）項目；搜尋僅見2007–2008選擇權重編舊事件。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000707549&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"LRCX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.47,"operating_margin_pct":35.29,"fcf_margin_pct":21.05,"rd_intensity_pct":10.23},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LRCX","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"ASML","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":52.73,"operating_margin_pct":35.42,"fcf_margin_pct":24.27,"rd_intensity_pct":13.68},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"AMAT","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.4,"operating_margin_pct":31.09,"fcf_margin_pct":18.23,"rd_intensity_pct":12.88},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"KLAC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":61.3,"operating_margin_pct":41.69,"fcf_margin_pct":27.74,"rd_intensity_pct":11.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLAC","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"8035.T","period":"TTM ending 2026-06-30（2季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.8035.T","as_of":"TTM ending 2026-06-30（2季加總）"},"note":"Total Revenue 缺失，無法算利潤率；僅 2 季可得，非完整 TTM"}],"subject":"LRCX"},"financial_history":{"ticker":"LRCX","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":17428516000.0,"revenue_yoy_pct":null,"gross_margin_pct":44.62,"operating_margin_pct":29.93,"net_income":4510931000.0,"diluted_eps":3.321,"free_cash_flow":4677370000.0,"fcf_margin_pct":26.84,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":14905386000.0,"revenue_yoy_pct":-14.48,"gross_margin_pct":47.32,"operating_margin_pct":28.73,"net_income":3827772000.0,"diluted_eps":2.9,"free_cash_flow":4255599000.0,"fcf_margin_pct":28.55,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":18435591000.0,"revenue_yoy_pct":23.68,"gross_margin_pct":48.71,"operating_margin_pct":32.01,"net_income":5358217000.0,"diluted_eps":4.15,"free_cash_flow":5414078000.0,"fcf_margin_pct":29.37,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":23232690000.0,"revenue_yoy_pct":26.02,"gross_margin_pct":50.47,"operating_margin_pct":35.29,"net_income":7265396000.0,"diluted_eps":5.76,"free_cash_flow":4891252000.0,"fcf_margin_pct":21.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/LRCX/LRCX_Q1_2027_Earnings_Call_20261021.md）

# Q1 2027 Earnings Call
**Lam Research Corporation** | Earnings Calls | 2026-10-21

**Operator** (Operator):
Good day, and welcome to the Lam Research Corporation September 2026 Earnings Conference Call. [Operator Instructions] After today's presentation, there will be an opportunity to ask questions. [Operator Instructions]. Please also note, today's event is being recorded. I would now like to turn the conference over to Ram Ganesh, Vice President, Investor Relations. Please go ahead.

**Ram Ganesh** (Executives):
Thank you, and good afternoon, everyone. Welcome to the Lam Research Quarterly Earnings Conference Call. With me today are Tim Archer, President and Chief Executive Officer; and Doug Bettinger, Executive Vice President and Chief Financial Officer.
During today's call, we will share our overview on the business environment, and we'll review our financial results for the September 2026 quarter and our outlook for the December 2026 quarter. The press release detailing our financial results was distributed a little after 1:00 p.m. Pacific Time. The release and the accompanying presentation slides for today's call can be also found on the Investors section of the company's website. 
Today's presentation and Q&A include forward-looking statements based on our current beliefs, expectations and assumptions. These statements are subject to risks and uncertainties, and actual results could differ materially from those expressed or implied in such statements. 
For a discussion of factors that could cause actual results to differ materially, please refer to the risk factors in our most recently filed periodic reports on Form 10-K and Form 10-Q and subsequent filings with the SEC and the cautionary statement in the accompanying presentation slides. 
Today's discussion of our financial results will be presented on a non-GAAP financial basis unless otherwise specified. A detailed reconciliation between GAAP and non-GAAP results can be found in the accompanying presentation slides. This call is scheduled to last until 3:00 p.m. Pacific Time. A replay of this call will be made available later this afternoon on our website. 
And with that, I'll hand the call over to Tim.

**Timothy Archer** (Executives):
Thanks, Ram, and thank you to everyone joining us today. In the September quarter, Lam again delivered record revenue and profitability. Gross margin, operating margin and EPS all reached new highs with operating margin topping 40% for the first time. Our performance throughout the year reflects the broad strength of our product portfolio and a relentless focus on operational execution as AI continues to drive unprecedented semiconductor demand and increasing device complexity. Including the midpoint of our December quarter guidance, we expect calendar year 2026 systems revenue to grow well over 40% year-on-year. Rising deposition and etch intensity across all device types and advanced packaging solutions is continuing to drive greater opportunity for Lam. 
Over the past few years, increasing device complexity and a push towards greater 3D scaling have driven a 4-point expansion of our Served Available Market, or SAM, as a percentage of WFE. When combined with share gains from products addressing this growing SAM, we expect 2026 to mark our third consecutive year of WFE outperformance. 
For calendar year 2026, we expect WFE in the mid-$150 billion range. Our preliminary 2027 WFE outlook is for more than $200 billion of spending with percentage growth led by DRAM, followed by leading-edge foundry/logic and NAND. 
As we move into calendar year 2027, we see clean room space availability and supply chain constraints for certain components continuing to limit chip makers and equipment companies' ability to fully meet end demand. We are actively working with our suppliers to accelerate their capacity expansion plans and are confident Lam is well positioned to deliver on the strong demand we see ahead. 
Underpinning our outlook for WFE growth is the continued rapid adoption of AI by enterprises and consumers. It is reported that average weekly token usage is up roughly 250-fold in the past 18 months. As AI moves increasingly towards autonomous agentic workflows, demand for compute, memory and storage solutions continues to expand. 
For example, in NAND, AI performance and economics are driving demand for multiple tiers of storage, each optimized for different workloads. QLC today provides cost-effective storage for rapidly growing AI data volumes. TLC storage is used as a high-bandwidth tier for context memory and KV cache workloads. And SLC-class NAND is emerging for low latency, high-speed access in agentic AI. We believe adoption of an SLC storage tier could become a meaningful driver of NAND wafer capacity. Converting from TLC to SLC-class devices reduces bits per device by roughly 3x. Said differently, for each percentage point mix shift of NAND bits to SLC-class devices, approximately 2% more installed wafer capacity will be needed to support the same bit demand. Incremental growth in bit demand would further amplify wafer capacity requirements. 
We expect all 3 storage tiers to grow, increasing the value and strategic importance of NAND. We believe Lam is best positioned to benefit from this inflection. We have the industry's largest installed base of NAND systems and a comprehensive product portfolio spanning all critical deposition and etch steps. Any increase in NAND bit demand, whether satisfied through installed base upgrades or capacity additions, will generate additional need for Lam's tools and technology. Foundry/logic and DRAM are seeing a similar device level evolution to satisfy AI's emerging performance requirements. From advanced patterning and backside power to next-generation packaging, we see billions of dollars of potential SAM expansion and share gain opportunities for Lam in the years ahead. 
We are seeing the impact of our targeted investments in foundry/logic and DRAM products in our calendar year 2026 results. These 2 market segments have accounted for approximately 80% of Lam's systems revenue growth year-to-date. A good example is our focus on advanced patterning requirements for foundry/logic and DRAM. With each technology node bringing more stringent EUV pattern fidelity and defectivity requirements, Lam's Akara etch -- conductor etch and Aether dry resist tools are being paired to deliver unprecedented scaling capability. 
Importantly, these tools are also helping improve the productivity of DRAM scaling at a time when maximizing fab output is a critical priority for our customers. Multiple chip makers are adopting Akara for its ability to etch very high aspect ratio features with exceptional profile control, while at the same time, delivering up to a 50% reduction in wafer-to-wafer and lot-to-lot variability and up to a 50% gain in wafer output per fab footprint. 
Similarly, Lam's Aether dry resist solution has demonstrated sub-10-nanometer resolution at the highest pattern density and fidelity with high NA EUV. It helps achieve this result while requiring 10% lower exposure dose, improving scanner productivity and reducing patterning cost per wafer. Aether solutions are already ramping in HBM high-volume manufacturing with low NA EUV, and we see additional insertion opportunities ahead across both DRAM and foundry/logic customers. 
As a result, we now expect cumulative Aether-related revenue to reach approximately $2.5 billion by the end of the decade, roughly $1 billion above our prior expectations. Backside power is another example of where Lam's strength in deposition and etch is evident. Separating power and signal routing allows for thicker backside metallization to reduce resistance and improve power efficiency. Implementation increases process complexity, driving the need for more deposition, plating and etch steps. As customers ramp backside power at 2-nanometer and below, our production-proven VECTOR, SABRE and Flex tools are well suited to the task. VECTOR provides industry-leading footprint density and wafer-to-wafer repeatability with its unique quad architecture. 
SABRE is the global industry benchmark for electroplating due to its high productivity and superior on-wafer performance. Flex delivers high throughput dielectric etch with low defect levels leveraging its differentiated small volume chamber design and confined plasma. New materials such as molybdenum are also being introduced to enable more efficient electrical connections between the backside and frontside of the wafer. 
For this emerging application, our Halo tool is gaining traction by enabling both plasma and thermal processes within a single chamber while delivering industry-leading productivity. We are gaining share in this expanding backside power SAM opportunity and recently secured tool of record wins for all 4 products at a leading customer. 
In advanced packaging, our market-leading Syndion product is winning advanced logic and HBM TSV applications. Syndion's differentiated hardware design enables rapid process switching to deliver highly uniform TSV profiles, smooth sidewalls and high-volume productivity. Recently, we attained 4 new positions across multiple customers. 
Our Striker ALD product also achieved multiple TSV liner wins due to the film's superior step coverage and low etch rate. Beyond TSV applications, we secured additional VECTOR and TEOS 3D wins for high-energy bonding films and inter-die gap fill applications by delivering lower defectivity for thick film deposition. With its high deposition and etch intensity, advanced packaging has become a major growth driver for Lam.
For next-generation AI and high-performance computing devices, customers are increasingly turning their sights towards panel-level packaging to scale manufacturing. Our panel-level packaging portfolio continues to gain momentum across fan-out packaging, glass core substrates and emerging substrate and interposer architectures. 
To date, we have shipped panel plating systems to more than 20 customers worldwide across panel sizes ranging from 300 x 300 millimeter to 600 x 600 millimeter. Customers continue to select our Kallisto platform for its differentiated coplanarity and plating uniformity performance across bumps, pillars and redistribution layers. 
Kallisto is also well positioned to benefit from increasing adoption of glass-core substrates through emerging through glass via applications. Given our customer engagement, installed base growth and technology leadership, we expect to achieve panel-level packaging market share that surpasses the strong position we already hold in current wafer-level packaging. And finally, turning to CSBG, we are set to exit calendar year 2026 with solid momentum with annual revenue expected to grow more than 30% year-over-year. This is more than twice the rate of our long-term target set at our last Analyst Day. 
Growth is broad-based across upgrades, spares and services supported by high fab utilization and customers' continued focus on installed base efficiency. The value we are delivering with Equipment Intelligence and Dextro cobots recently helped us secure performance-based service contracts with multiple memory manufacturers. We expect CSBG momentum to continue in calendar year 2027 with revenue growing over 15% year-over-year. 
So to wrap up, we believe the industry is in the early stages of a multiyear investment cycle with customer visibility extending through 2028. Increasing manufacturing complexity, new materials integration and advanced packaging are driving higher deposition and etch intensity across device segments. Our technology leadership, growing installed base and strategic investments in product innovation and manufacturing capacity position Lam to capitalize on these inflections and drive sustained outperformance. Thank you, and here is Doug.

**Douglas Bettinger** (Executives):
Great. Thank you, Tim. Good afternoon, everyone, and thank you for joining our call today during what I know is a very busy earnings season. We were pleased with our continued strong execution in the September quarter, resulting in our fifth consecutive quarter of record revenue as well as record gross margin, operating margin and earnings per share. September quarter revenue was $8.22 billion, which was up 22% sequentially and up 54% from the same period in 2025. 
The deferred revenue balance at quarter end was $2.66 billion, which was an increase of $227 million from the June quarter. This grew primarily due to increased sales volume and it was partially offset by a decrease in customer down payments. From a market segment perspective, September quarter systems revenue in memory was 46%, which was consistent with the prior quarter. 
On a dollar basis, this represented a record level for memory, and it was up 120% from the same period in 2025. Within memory, nonvolatile memory accounted for 26% of our systems revenue, up from the June quarter's level of 23%. On a dollar basis, NAND revenue increased approximately 40% sequentially as the industry continued spending on conversions to 256-layer and above class devices. 
We are seeing initial spending on 384-layer class devices. DRAM revenue reached a record, growing sequentially on a dollar basis, but down a little bit on a percentage basis from 23% of systems revenue in the June quarter to 20% in the September quarter. DRAM spending remained focused on technology additions and upgrades across the 1-alpha, 1-beta and 1-gamma nodes that is enabling DDR5, LPDDR5 and more importantly, high-bandwidth memory. 
Foundry also achieved record revenue. Its strength -- excuse me, its share of systems revenue increased to 46% from 44% in the June quarter. Strength in the quarter was driven by investment in leading-edge nodes, including advanced packaging as well as mature node spending in China. And finally, Logic and Other were 8% of our systems revenue in the September quarter, slightly down from the prior quarter's level of 10%. Most of the spending here was targeted at leading-edge process nodes. 
Let me now discuss the regional composition of our total revenue. China contributed 35% of revenue, up from the June quarter level of 26%. We saw strong investments here by both domestic and multinational customers. In the December quarter, we expect China will represent a significantly lower percentage of our total revenue compared with the September quarter. Korea's contribution to revenue in the September quarter remained unchanged from the June quarter level at 20%. 
The Taiwan region contributed 18% of revenue, down from the June quarter at 27%. The Customer Support Business Group generated a fourth consecutive quarter of record revenues at nearly $2.5 billion in the September quarter. This was up slightly from the June quarter and 40% higher than the same period in 2025. Each component of CSBG remained strong with the prior quarter. 
Turning to the gross margin performance, the September quarter came in at an all-time record of 52.4%, improving from the June quarter level of 52% due to favorable customer and product mix. Additionally, we continue to balance our cost and pricing postures. Operating expenses for the June (sic) [ September ] quarter were $1 billion, up from the prior quarter amount of $916 million. The increase was primarily driven by higher incentive compensation due to our increased profitability levels. 
We are also investing incremental resources to support growing programs like Akara, Halo, panel form factors and Dextro. R&D accounted for nearly -- or excuse me, approximately 2/3 of our total operating expenses. Operating margin for the September quarter was another record at 40.2% compared to the June quarter level of 38.4%. This improvement reflected stronger gross margins and continuing operating leverage as our business scales. 
The non-GAAP tax rate was 16.5% for the quarter compared to 11% in the June quarter and in line with our expectations. The increase was primarily driven by a higher U.S. tax rate on foreign earnings as well as expected shifts in the geographic mix of income. We expect the tax rate to remain in this range for the December quarter and likely beyond. 
I'd encourage everyone to make sure they have their earnings models updated to this higher tax rate. Other income and expense for the September quarter was approximately $16 million in income compared with $19 million in expense in the June quarter. The improvement in OI&E was due to foreign exchange fluctuations, higher interest income as well as favorability in our venture portfolio. 
And as we've talked about in the past, you should expect to see some variability in OI&E quarter-to-quarter dictated by market factors. For the September quarter, diluted earnings per share were a record at $2.20. The diluted share count was roughly 1.26 billion shares, which was relatively unchanged with the June quarter. 
Let me pivot to capital return. We allocated approximately $1 billion to share repurchases, and we paid $325 million in dividends in the September quarter. During the quarter, we entered into an accelerated share repurchase structure that will continue to execute in the December quarter. We returned approximately 41% of free cash flow in the quarter and 59% in the calendar year-to-date. 
I would point out that we also used $750 million to pay down maturing debt during the year. Our long-term plans remain to return 85% of free cash flow to shareholders. We have $3 billion remaining on our Board-authorized share repurchase program. Our cash and short-term investments totaled $7.5 billion at the end of the September quarter, which was up from $5.6 billion at the end of the June quarter. 
The factors behind the increase were cash from operating activities partly offset by our capital return activities as well as capital expenditure. The September quarter was also a record for our free cash flow, coming in at $3.24 billion in the quarter. And as I mentioned last quarter, we've been increasing our cash levels a little bit to support growing business volumes as well as capital investments in this growing demand environment. 
Day sales outstanding were 63 days in the September quarter, a decrease from 72 days in the June quarter. Inventory at the September quarter end totaled $4.6 billion, which was an increase of $274 million from the June quarter as we're building inventory to meet the expected future demand for our products. 
Nonetheless, inventory turns continued to strengthen to 3.4x versus 3x in the prior quarter. I would just mention this was the highest level of inventory turns in nearly 7 years. Our noncash expenses for the September quarter included approximately $115 million in equity compensation, $106 million in depreciation and $16 million for amortization. 
Capital expenditures in the September quarter were $258 million, which was up from the June quarter at $189 million. Capital spending grew as we continue to increase our lab infrastructure and expand our manufacturing facilities globally. We ended the September quarter with approximately 24,300 regular full-time employees, which was a growth of approximately 1,900 people from the prior quarter. Headcount increased primarily in our factory and field teams to support expanding manufacturing activities and growing tool installations. We also added headcount in R&D. 
Now let's turn to our non-GAAP guidance for the December 2026 quarter. We're expecting revenue of $8.6 billion, plus or minus $400 million. I would mention that this revenue guide would have been a bit higher, if not for some near-term supply chain constraints that we are actively managing. 
We're expecting gross margin of 52.5% plus or minus 1 percentage point. This is improving a little bit in spite of headwinds related to customer mix. We're expecting gross -- operating margin of 40.5%, plus or minus 1 percentage point; and finally, earnings per share of $2.33, plus or minus $0.15, based on a share count of approximately 1.253 billion shares. 
So let me wrap up. We continue to execute our strategy for outperformance delivering another quarter of record revenue and profitability. Operating margin exceeded 40% for the first time in our history, and we're guiding for this to expand slightly. We're increasing R&D investment to strengthen the already strong product portfolio that we have. We're also investing in the infrastructure needed to support the growing demand we expect in the future. These activities continue to deliver a return on invested capital level that is comfortably above the competition. 
Operator, that concludes our prepared remarks. Tim and I would like to open up the call for questions.

**Operator** (Operator):
[Operator Instructions] Today's first question comes from Timothy Arcuri at UBS.

**Timothy Arcuri** (Analysts):
Doug, I don't think I've ever seen a quarter where you grew systems 35% Q-on-Q. So kudos on that. You did talk about the near-term constraints. I guess you can see that from payables. I think payables were up like $1.3 billion. So can you just give us a sense? Is it fair to say this is costing you like $300 million to $400 million? Is that like a reasonable number to assume that, that's costing you in the guidance for December? And do you get that back in March? So do you get back on this sort of 10% plus or minus systems growth in March, does that actually -- do you actually get that back?

**Douglas Bettinger** (Executives):
Yes, Tim, that's a good question. I'm not going to put a specific number on it. In the script, I said it would have been a little bit higher. So it would have been a little bit higher. And yes, Tim, to the extent that it's something we would have shipped in December because of timing, we will ship that in the March quarter.

**Timothy Arcuri** (Analysts):
Okay, Doug. And then can you just talk about -- there was a call hosted by a big memory company today, and they were talking about 4F squared. And they were saying that they're going to prioritize 3D DRAM rather than 4F squared and your stock traded down, which was a little bit odd to me. It seems that people don't really understand what your position is there. So Tim, I wonder if maybe you can talk about that. Can you talk about how you do for -- in like a 3D world versus like a 4F squared world? And sort of what you're seeing in terms of your customers' DRAM road maps?

**Timothy Archer** (Executives):
Sure. Obviously, we don't know exactly what the reaction was or why people would have reacted in that way because we've said for a long time that as all device architectures go 3D, etch and deposition intensity rises. Now I would say that in some ways, interestingly, the longer it takes to get there, the more we're seeing momentum for some of our other scaling activities. 
And so we focused on this -- even in this call, advanced patterning, if you want to extend the current architecture in which devices are getting -- patterns are getting even smaller. That's why we're starting to see this uptick in processes like Aether, processes like Akara for conductor etch, the processes that are needed to etch and create those smaller structures. So I would say in the short term, etch and dep intensity are rising. And if really, we're making a leap right from 6F squared to 3D DRAM, then etch and dep intensity is going to rise even faster even sooner than we would have thought, and that's a great thing.

**Operator** (Operator):
And our next question today comes from Melissa Weathers at Deutsche Bank.

**Melissa Weathers** (Analysts):
I wanted to also ask on the supply constraints. I think you said you're working with your supply chain to make sure some of those bottlenecks get resolved. Can you just give a little more color on what actions you're taking? Could you consider any co-investments or help on the capital side of those guys, just what needs to happen to relax those constraints?

**Douglas Bettinger** (Executives):
Listen, Melissa. Yes, I mean we're always working with our supply chain to make sure they're ready for the demand environment that we see. But given how strong things have been, we're seeing a little bit of tightness. I'm not going to get into specifically where it is, except I would tell you that what we're managing, just like we always do, we'll continue to do that, but it just got a little bit tight in the quarter. 
I have every expectation we'll effectively manage this as well as anybody in the industry will. And yes, if we needed to make some level of investments, we'd be open to that. But frankly, a lot of our suppliers are well capitalized and can manage this on their own from a financial standpoint. I don't know, Tim, would you add anything?

**Timothy Archer** (Executives):
No, I think that's correct. I mean for those of us who were around during the COVID shortages, this is nothing like that. We learned a lot of lessons during that period. And in fact, just in the last 2 months, we've hosted a couple of big events with our global suppliers to really lay out what we have in terms of expectations for growth into the next couple of years. 
And you know where you can run into problems is within our own products, as we talked about etch and deposition intensity increasing in certain parts of our business, like we talked about advanced packaging, for instance, really being a major driver of growth for Lam. You can find certain suppliers that are seeing percentage growth of our demand to them rising even much faster than Lam itself is growing. 
And so yes, I think we have been very clearly communicating that to those suppliers and really asking for transparency to the help they need to keep up with the pace that we're driving in the industry. And I think we'll be caught up very shortly.

**Melissa Weathers** (Analysts):
And then on the NAND spending cycle and that upgrade opportunity that you guys have been talking about, you pulled it in last quarter. And then it's nice to hear about the 384-layer devices that I think are starting to -- you guys are shipping to. So can you update us on where you -- like what inning you think we're at in that NAND upgrade cycle? What trends are you seeing? And yes, maybe any forward-looking comments on the SLC and some of those new opportunities.

**Timothy Archer** (Executives):
Yes. I think in terms -- there's still room to go on the upgrade cycle. And in fact, when you're in a period of high demand actually taking tools offline to do the upgrade, sometimes it's also a scheduling challenge for customers and for us. But I'd say that we're working our way through that, and we said that we would be finishing that in 2027. And so -- but we also pointed out that then you just roll to sort of the next upgrade cycle. And so remember, that upgrade was from the 128-layer to kind of into the 200-layer class devices. 
And as you just mentioned, people are already moving into the 300 and 400-layer devices, we've been engaged on those in R&D for quite some time. But I think the real thing we wanted to point out today is that while we used to just talk about layer counts as the driver for Lam equipment demand and wafer capacity needs. Now you're really seeing this separation of storage tiers and each of the devices within NAND starting to be more specialized to different workloads within AI.
And that actually, just like it did in DRAM with HBM and the impact on bits that could be manufactured per wafer, you're starting to see the performance needs of AI start to create a need for higher performance, low-latency devices. And I think we've just had a customer talk in some detail about that opportunity. I think that's going to drive NAND wafer capacity demand and intensity for Lam's equipment.

**Operator** (Operator):
And our next question today comes from Krish Sankar with TD Cowen.

**Sreekrishnan Sankarnarayanan** (Analysts):
I have 2 of them, Doug or Tim, when I look at your Q4 guide, I understand you're talking about mid-$150 billion WFE, but the implied WFE for Q4 is like it was $180 billion or so. I'm just wondering, are there any episodic revenues in Q4? Or is some of the price increases that the semi -- front-end semi equipment companies are doing impacting Q4 and kind of making the WFE number larger? And then I have a quick follow-up.

**Douglas Bettinger** (Executives):
Yes, Krish. No, there's nothing unique or one-off or episodic, to use your word, in the December quarter. It's just consistent with customer demand, frankly. And like I alluded to, it would have been a little bit higher, if not for some of the supply chain constraints, but there's not anything one-off.

**Sreekrishnan Sankarnarayanan** (Analysts):
Got it, Doug. And then I had just a quick follow-up. I think in your prepared comments, you mentioned China would be significantly lower in December versus September, kind of wondering, can you quantify that? How will the mix look like? Because it seems like September quarter was a surprise on the upside with both multinationals and domestics coming in.

**Douglas Bettinger** (Executives):
Yes, Krish, it wasn't a surprise. It was exactly as expected. And yes, I mean the domestic customers in September were strong, but so were the global multinationals. I expect it in December will be meaningfully down driven by the domestic customers in China. I expect in the December quarter, the multinationals in China likely continue to be reasonably strong, but the percent of revenue in China will be meaningfully down in the December quarter.

**Operator** (Operator):
Our next question today comes from Harlan Sur at JPMorgan.

**Harlan Sur** (Analysts):
On CSBG, 36% growth, first 9 months of this year, full year outlook greater than 30%, very, very strong. The growth tailwinds, I assume higher spares as customer utilizations are at record levels, higher sales of higher dollar value upgrades for NAND and maybe strength in Reliant, right, as the mature sectors of the markets start to come back. 
And of course, you have your intelligent services offerings. Can you guys just rank order these growth drivers? And more importantly, on a year-over-year basis, how much higher are CSBG operating margins? I'm just wondering if mix and volume dynamics within CSBG are contributing to the strong overall operating margin profile?

**Timothy Archer** (Executives):
Yes. I'll let Doug talk about the rank order in terms of financial impact in the short term. But if I were to rank order them in terms of my excitement, clearly, as we've talked about, we see Equipment Intelligence, the cobot-driven maintenance, the performance-based service contracts we talked about as really kind of the new part of our CSBG business that's really catching on. 
And we're in an environment right now where just as there was an earlier question about if people are trying to shrink devices even faster to get more bits or more performance out, that creates an intolerance to variability in the process, whether that's in the process control or the maintenance. 
And that's exactly where Equipment Intelligence and cobots come into play. So we're seeing strong pull for that element, and that's something new for our CSBG business. And so I'm very excited about that becoming a bigger growth driver for us than it has been in the past. And I'll let Doug talk about upgrade spares and everything else.

**Douglas Bettinger** (Executives):
Yes, Harlan, we don't specifically give you hard numbers on each of the individual sub-components. What I would tell you relative to strength of each of them, though, given how strong utilization in the industry is, spares and service are just humming along as you would expect. I've always said spares is the biggest individual component, and that continues to be true. But I'm not going to be specific on the other ones. What you alluded to is right, given where we're at in the NAND conversion/upgrade cycle, that portion of the business continues to be strong. 
And yes, Reliant did quite nicely last quarter, given the strength of investment in mature node spending. And I expect you'll see all of these trends continue into next year.

**Harlan Sur** (Analysts):
Yes. I appreciate that. And then as a follow-up, the supply tightness in leading-edge foundry/logic is creating tightness in mature and specialty nodes, analog, power microcontroller, foundry supply here is tightening very rapidly, right? It's like mature foundry suppliers, internal IDM factories, they're kind of all increasing capacity. You just said that this is reflected in your Reliant business. But if I exclude China, are you anticipating this segment of your customer base to grow this year?

**Douglas Bettinger** (Executives):
Probably not in a meaningful way this year, Harlan. I do expect as we get into next year that mature node spending outside of China will be strong because of the dynamics you were just referring to. I'm not sure that it's really sticking out quite yet in 2026.

**Operator** (Operator):
Our next question today comes from Srini Pajjuri with RBC Capital Markets.

**Srinivas Pajjuri** (Analysts):
Thank you. Tim, I'm looking at your systems business growth. I think last year, you were up 40%. And then this year, you're probably going to grow 45%, both well above the WFE growth. So looking out to next year, given your $200 billion-plus outlook, roughly 30%, let's say, I suspect you expect to outgrow that market next year as well. Can you talk about what are the drivers? Is it driven by any particular end market like NAND or DRAM or any product line? Or anything else you can comment on would be helpful.

**Timothy Archer** (Executives):
Yes. I guess I would -- at a very general level, I would say it's driven by the increase in deposition and etch intensity across all devices. And if there are a few things I'd point out just as maybe obvious trends in the market. Lam's exposure in the advanced packaging space is extremely high. 
And I think advanced packaging continues to play an even more vital role in just about every device that's feeding into AI today. And so that's, I think, a great position where we will see outperformance. And we talked even about that extending in the panel level. But it really is in every device. I mean you see NAND layers growing, you see new architectures coming to NAND. 
You see -- we talked a little bit about the emergence of SLC-class NAND. You're starting to hear from our customers. Foundry/logic, we've talked about success in gate-all-around. We invested 4 or 5 years ago in an entire set of products focused on improving our position in foundry/logic and DRAM. And I commented on the fact that today, those products are driving a significant portion of our growth here in the years in which foundry/logic and DRAM are leading the charge on growth. And so we're extremely happy with that. 
NAND is yet to emerge as to its full potential from our perspective. And I think you're starting to hear about it and the strategic role that can play in AI. And so I don't know, it's hard to project exactly. We'd love to see all the devices grow, but I think the single greatest theme is regardless of which device we're talking about, deposition and etch will play a greater role in 2027. 
And if you think about -- we had this model, which was the $100 billion of AI CapEx being about $10 billion in WFE, but the important thing is that $10 billion next year, Lam's opportunity in that $10 billion would be even greater than it is this year because of the device evolution. And so I think that's -- that dep and etch intensity is just the way to think about Lam's opportunity.

**Srinivas Pajjuri** (Analysts):
Right. And then maybe on the gross margins, Doug, you're guiding actually a slight increase despite you highlighted some customer mix headwinds. I'm suspecting that's related to China. So I guess, on a normalized basis, as we look out to the next few quarters, once China normalizes, how should we think about gross margins? I mean, in the past, you did talk about some pricing actions. And of course, you have the cost and efficiency improvements as well. So just curious as to how we should think about gross margins as we go into next year?

**Douglas Bettinger** (Executives):
Yes. Listen, in the near term, Srini, I think you're going to be plus or minus the level that we're at. We did suggest over the next several years, we see an opportunity to expand gross margin in the mid-50s. So kind of triangulate yourself between these 2 points. But in the near term, it will bounce around generally where it is. And yes, the things that contributed to our very strong gross margin as well as our expectation of how we're going to drive improvement into the future are new product introductions, right?
We've got some very nice technically differentiated new products like Akara and Aether. We're excited about where that's all going to trend from a profitability standpoint. We've talked about our close to customer strategy relative to how we're manufacturing closer to where the fabs are and that's contributed and still have a little bit of juice left to squeeze there. And then we've also talked about the fact that we're working on pricing. All of those things have contributed to getting us to the all-time record level that we printed in the September quarter and levers we're going to keep trying to pull as we go into the future to get to that mid-50s that we've said we are going to drive towards.

**Operator** (Operator):
Our next question today comes from Vivek Arya with Bank of America Securities.

**Vivek Arya** (Analysts):
For the first one, if I look at last year, you were able to kind of consistently expand your WFE expectations, I think you started the year at mid-130s. Now it's like mid-150s. So I'm curious what helped you increase WFE expectations last year? And then what are the constraints next year that you think can be resolved to help do better than the 30% or so industry growth. I know you mentioned some constraints in the near term. I'm curious if they are the same constraints that limit industry growth for next year or they are different. Just what can help you do better than this 30% industry WFE growth?

**Douglas Bettinger** (Executives):
Yes, Vivek, I'll start, and then I'll let Tim add. As we walk through this year, you're absolutely right. We started mid-130s, and then we went to a little bit more than $140 billion and then a little more than $150 billion and then we just took it to mid-150s. Basically, what we saw happening across all aspects of our customer base is everybody squeezed a little more out of the clean rooms that they had and/or pulled projects in a little bit quicker than maybe they originally intended. 
That's generally what happened. And frankly, we did exactly the same thing. And with the more than $200 billion number, we're giving you our initial starting point more than $200 billion. We normally don't give you this much specificity this early in the year, and we'll give you a sharper pencil on that when we get to the earnings call next quarter.

**Vivek Arya** (Analysts):
Got it. And for my follow-up, Doug, you mentioned something about an accelerated repurchase plan. I think you can all guess what that is due to, but would help to hear from you also and if you could help give some sense of what the magnitude is, how long you plan to continue it? I know you mentioned you have $3 billion left in the buyback. But just how much is the ASR component, how long it continues?

**Douglas Bettinger** (Executives):
Yes. I mean, Vivek, the way these accelerated share repurchase structures work is, you enter into them, you get some shares up front, and then they execute over time depending on where the share price is and volatility and things like that. I'm not going to disclose actually the start or end date because there's ranges around it. I don't like people to know what we do and how we do it, except I will reinforce for you. It's going to continue to execute in December.
And then we will likely be doing other things in the market relative to the buyback, right? Our medium long-term goals remained unchanged, which is to return 85% of free cash flow to shareholders.

**Operator** (Operator):
And our next question today comes from Atif Malik with Citi.

**Atif Malik** (Analysts):
The first one for Tim. Tim, I thought your panel-level packaging comments are extremely bullish, you're talking about a share that will exceed the wafer-level packaging. Can you just kind of double click in terms of the industry ramp on panel level packaging and your products? Are the products the same as wafer level like SABRE that will drive this growth?

**Timothy Archer** (Executives):
Yes. I mean at a fundamental level, they're similar. I mean, I think part of our optimism in this space is, one, it makes sense. I mean, obviously, we talked on the last -- I think, on the last earnings call about how packages themselves are getting larger, which, in many cases, is they're too big for wafer-level packaging. 
And so panels make sense as you try to assemble bigger and bigger system-level solutions. So we saw that quite a while ago, and we've been investing in panel for several years. And I would say we're still, though in the very, very early stages. I mean it's wafer level packaging is the predominant method. But as we talked about the shipments to more than 20 customers, you can think of those as really the planting the seeds for an industry that I think is going to ultimately assume a fair bit of the packaging work for the industry. The processes that we talked about, we don't call it SABRE in this case, I mean, but there's a plating aspect of this and some other processes that I think we'll do extremely well within panel level.

**Atif Malik** (Analysts):
Great. And then Doug, on the $200 billion plus wafer fab equipment outlook for next year, your rank orders DRAM, foundry/logic and NAND, which is the same as 90 days ago. But has the gap between DRAM and foundry/logic expectations narrowed given some of the announcements on the new logic fabs from foundry and Terafab, like?

**Douglas Bettinger** (Executives):
No, Atif they really haven't. And as you might expect, all of these projects perhaps that people are now publicly hearing about, we knew about in advance of that. So it really hasn't changed much.

**Operator** (Operator):
Our next question today comes from Jim Schneider at Goldman Sachs.

**James Schneider** (Analysts):
I was wondering as you look into 2027, can you maybe frame for us some of the moving pieces that could adjust the WFE outlook higher or lower? How much of it really is your customers' individual spending plans for the different technology or product areas versus just the general availability of clean room space overall?

**Douglas Bettinger** (Executives):
Yes, Jim, I'll start, and then I'll let Tim add. When we look into next year, we see 10 new Tier 1 fabs coming online between the beginning of the year and the end of the year and they will layer in over time. So obviously, that's a contributor. This year has been primarily clean room constrained. And then we begin to see, like we said, some emerging supply chain constraints that we're confident we're going to be able to work through effectively, but the whole industry is going to have to work through very similar things.
And so all this at the end of the day has to get balanced. Every equipment company needs to be able to supply things. Clean rooms need to come on, on schedule. People need to hire and train to make sure they're all ready. The industry is good at doing this, and we're great at doing it. But all of those things have to come into play when you're thinking about what the next year is going to look like.

**Timothy Archer** (Executives):
Yes. And I think in my prepared remarks, I talked about the fact that we have visibility through 2028. That's really from the demand side. And so I think that where we're saying it might just be a little bit early to give such a precise number on WFE is simply because we think by the January call, which is the normal time we would get that level of detail. We'll have a better view of clean room schedules and supply chain constraints and really be able to hone in on that. But it's -- those are the things we're looking at. And just this year, we were able to work through those. And I think as we get closer, we'll get a better sense for how the industry is responding.

**Operator** (Operator):
Our next question today comes from Stacy Rasgon with Bernstein Research.

**Stacy Rasgon** (Analysts):
The first one, I understand that this more than $200 billion WFE next year is a constrained number. Do you guys have a point of view on what that number would be if it was not constrained, if clean rooms were available, supply chain was not as tight as it is? Where do you think -- I guess what I'm asking is where do you think the demand for WFE is in 2027 versus the supply number that you've given?

**Douglas Bettinger** (Executives):
Listen, Stacy, you always ask these interesting questions. You know we're not going to answer. But I love the questions nonetheless. Listen, things are going to continue to be constrained, we think, in the next year by the things that we described. I'm not going to put a number on what the unconstrained demand would be. We probably -- not probably, it would be higher. But I'm not going to give you a precise number. And like I said, we'll fine-tune what we think the number is and give you a little more specificity on the next quarter call also.

**Stacy Rasgon** (Analysts):
Okay. That's helpful. For my follow-up, I just wanted to focus on the NAND upgrades relative to the services. It sounded like upgrades were strong. I don't know if that meant that they grew sequentially or not. I assume they did because the NAND revenues grew a bunch, but the CSBG revenues were kind of flattish, and I thought the upgrades were in CSBG. So if that's the case, I guess what I'm asking is, did upgrades drive the NAND growth? And if they did, what else was going on in CSBG to absorb the growth such that the overall was flat.

**Douglas Bettinger** (Executives):
Yes. Listen, Stacy. Upgrades are a part of NAND, also CSBG, but NAND also, when you go through these conversions, you need to buy new equipment also. So obviously, there was a contribution in the NAND spending from new equipment also.

**Stacy Rasgon** (Analysts):
Was it bigger than the upgrade piece? It sounds like it was.

**Douglas Bettinger** (Executives):
Both were meaningful contributors.

**Operator** (Operator):
And our next question today comes from Blayne Curtis at Jefferies.

**Blayne Curtis** (Analysts):
I actually want to ask on the NAND side. You mentioned SLC. That could be a big transition. Is that something you're seeing from customers? Or is that still a potential transition?

**Timothy Archer** (Executives):
I think it's something that you're starting to hear customers talk about. I mean, fundamentally, this idea of customizing memory and storage hierarchy to the different workloads, I think, is now pretty well understood. And so I think that this is emerging as one of the potential solutions for low latency NAND access. 
And so I think if you go look just in the last -- recent days and weeks, there's been discussion with SLC-class NAND emerging as part of that stack. A little bit longer. I mean for a little bit longer time, there's been discussion also things like high bandwidth flash and the role it can play. 
And so we're really starting to see NAND move from sort of a singular application we've always thought of to now one in which perhaps the device performances themselves will need to be customized. And that will have implications for us, but it will also -- from a process perspective, really, what we were highlighting here was the impact it would have on wafer capacity needs and therefore, perhaps an uptick in NAND equipment demand.

**Blayne Curtis** (Analysts):
And then I want to ask on advanced packaging. I think you said last time it would grow over 70% for the calendar year. I was curious what the update is. And then when you look at, it's probably the smaller end, so you didn't mention it, but in terms of that $200 billion outlook, like any thoughts on advanced packaging growth next year?

**Douglas Bettinger** (Executives):
Yes. Blayne, 70% for this year is still the right number, and I would be stunned if advanced packaging didn't grow nicely next year.

**Operator** (Operator):
And our next question comes from Shane Brett at Morgan Stanley.

**Shane Brett** (Analysts):
So my first question is on foundry/logic. At your 2025 Investor Day, you talked about your foundry/logic SAM per wafer increasing 2x. Just how far are we towards that 2x with the shift from 3-nanometer to 2-nanometer or if I rephrase that, how high did our SAM grow from 3-nanometer to 2-nanometer? And do you think your share gains would accelerate with the transition to 1.4?

**Timothy Archer** (Executives):
Yes. That was a -- that 2x was a multigenerational shift. And so it's a little bit hard to put exactly where we are in that, maybe halfway through, if I thought about that road map that we gave there. But really, it's -- as we've moved forward, though, we've seen just new emerging applications. I talked about a couple of them today. 
Clearly, advanced patterning itself is becoming ever more critical. We talked about the growth in Aether. We talked about the use of Akara for conductor etch. Backside power really starting to get a lot more attention being a very etch and deposition intensive application. We just see a number of elements of that improvement. And then I commented about how excited I was about advanced packaging. I mean it's -- advanced packaging is playing a huge role within foundry/logic and our exposure to the WFE there. And so I just think foundry/logic is turning into a good story. 
The thing we've highlighted over the last couple of calls, though, just to remind you, is the role we play in gate-all-around, our strength in ALD and our strength in surface treatment. Those are areas where I think even at the Investor Day, we might not have realized just how strong the uptake would be for things like the Argos surface treatment tool. So I feel like the story just kind of keeps getting better and better, the more complex the devices get across all 3 device types, foundry/logic, DRAM and NAND.

**Shane Brett** (Analysts):
Got it. And for my follow-up, it will be on advanced packaging. So at SEMICON West, one of your colleagues had a great presentation on breaking the integration wall in advanced packaging for the AI Era with one of the highlights being key challenges to hybrid bonding adoption at scale. Just how does Lam enable hybrid bonding? And is more hybrid bonding better or worse for our advanced packaging share?

**Timothy Archer** (Executives):
Well, I think that the -- we participate in the elements of the process that help enable hybrid bonding. And so obviously, as a deposition and etch company, we don't do the bonding ourselves, but we talked about a number of films, whether it's in the dielectric space or in the metal space that ultimately play an important role in achieving successful hybrid bonding. 
And so there is an opportunity for Lam through that transition. But I think that overall, look, the reality is success in advanced packaging, whatever version it is, will lead to greater adoption of advanced packaging. And ultimately, given our very high share position, that's a good thing for us. Hybrid bonding, you know it's a very etch and deposition intensive process compared to other parts of the semiconductor manufacturing process itself.

**Operator** (Operator):
And our next question today comes from Vijay Rakesh with Mizuho.

**Vijay Rakesh** (Analysts):
So Tim and Doug, you had some interesting comments on the NAND side. You mentioned every 1% move to SLC drives about -- requires about 2% increase in wafer capacity. So as you look at next year, with the move to SLC and potentially some HBF, any thoughts on how you think what percent of the market moves to SLC?Is it like 5%? Or how would you see that?

**Timothy Archer** (Executives):
I think it's too early for us to make any comment on that. And it would be probably something our customers should actually be commenting on. But what you can rest assured is that the -- in that sense, the intensity of Lam equipment in manufacturing those devices and those wafers would go up.

**Vijay Rakesh** (Analysts):
Got it. And then a quick follow-up. On the advanced packaging side, you mentioned, obviously, you have -- there's a whole CoWoS and EMIB-T coming and I guess, Lam has huge opportunities on the metallization, preclean TSV, et cetera. Just wondering if there's a way to size that opportunity as you have done before for every 100,000 wafers of EMIB-T or CoWoS, like how would you size that opportunity for Lam?

**Timothy Archer** (Executives):
Yes. I think maybe we'll take that as an action for some work to still be done. We're not prepared to do that today.

**Douglas Bettinger** (Executives):
Operator, we're going to take one more question.

**Operator** (Operator):
Absolutely. And our final question today comes from Brian Chin at Stifel.

**Brian Chin** (Analysts):
A few quick questions here. Maybe, Doug, firstly, days of inventory kind of running a little bit over maybe a quarter at the moment, clearly has drawn down. You said the turns have been really strong. Ideally, where would you want that to be?

**Douglas Bettinger** (Executives):
Yes. Listen, we're super comfortable where it is right now. As the company scales up, you do get some level of efficiency. Offsetting that, though, right now, we are trying to build inventory in anticipation of the growing demand we see into the next year. But I think we collectively feel pretty good about where we're at 3.4x.

**Brian Chin** (Analysts):
Okay. Great. Maybe just the last question here. Is the $1 billion increase in your dry resist revenue outlook reflective more of adding logic and DRAM customers in terms of the adoption of that platform? Or is it more towards existing customers pulling forward introduction of the timing of dry resist?

**Timothy Archer** (Executives):
I think it's a little bit of both. I mean there have been some additional customer adoptions, but really, it is -- as you really become PTOR for something like we mentioned, HBM manufacturing and the volumes are growing there. The number of tools and therefore, the business just continues to expand. And so we feel like we're positioned in production for some of the fast-growing parts of the market, and that's why we were able to take the number up.

**Douglas Bettinger** (Executives):
Thanks, Brian. Listen, thanks, everybody, for joining the call today. We're really excited about where the business is performing. We're really excited about what things look like into the next year. And I think we're probably the most excited about a third consecutive year of outperformance and an expectation that we're going to continue to drive those things into the next calendar year. So I know we'll see a lot of you guys in NDRs and conferences in the coming quarter, and we look forward to seeing you. Thanks for joining the call.

**Operator** (Operator):
Thank you. That concludes today's conference call. We thank you all for attending today's presentation. You may now disconnect your lines, and have a wonderful day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LRCX_Q4_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：9月季營收財測 81 億美元，區間正負 4 億（原話："$8.1 billion, plus or minus $400 million"）
- 2026-07-29｜CFO｜guidance：9月季毛利率財測 52%（正負 1 個百分點）（原話："gross margin of 52%, plus or minus 1 percentage point"）
- 2026-07-29｜CFO｜guidance：9月季營業利益率財測 39.5%（原話："operating margins of 39.5%, plus or minus 1 percentage point"）
- 2026-07-29｜CFO｜guidance：9月季 EPS 財測 2.15 美元（原話："earnings per share of $2.15, plus or minus $0.15"）
- 2026-07-29｜CFO｜guidance：9月季費用成長速度低於營收成長（原話："albeit at a much slower rate than the growth in revenue"）
- 2026-07-29｜CEO｜guidance：2026 年 WFE 展望為 1,500 億美元出頭（原話："WFE, to be in the low $150 billion range"）
- 2026-07-29｜CEO｜guidance：澄清：本季 WFE 展望未再說有上檔偏向（原話："We didn't say upside bias for this current outlook."）
- 2026-07-29｜CFO｜guidance：2027 年不給數字，只說看起來是很好的一年（原話："quantification around what '27 is going to be."）
- 2026-07-29｜CEO｜guidance：2027 年成長動能排序：DRAM、先進邏輯、NAND（原話："we still see DRAM being the fastest grower"）
- 2026-07-29｜CEO｜guidance：先進封裝 2026 年成長預期超過 70%（原話："deliver greater than 70% year-on-year growth"）
- 2026-07-29｜CFO｜guidance：稅率預期 9 月季升至中段十幾個百分點（原話："rate will be in the mid-teens in the September quarter"）
- 2026-07-29｜CFO｜guidance：服務事業下季輪廓與本季相近，不給數字（原話："similar profile of what we saw this quarter"）
- 2026-07-29｜CFO｜margin：FY2026 營收 232 億美元創高（原話："record revenue of $23.2 billion"）
- 2026-07-29｜CFO｜margin：本季毛利率超出財測上緣，原因含調價（原話："a myriad of factors, including pricing actions"）
- 2026-07-29｜CFO｜margin：管理層稱近期毛利率可維持 51%–52%（原話："we're in that 51%, 52% range right now"）
- 2026-07-29｜CFO｜margin：長期目標：毛利率中 50% 水準（原話："we intend to drive gross margins to the mid-50% level"）
- 2026-07-29｜CFO｜margin：達成中 50% 毛利率需數年（原話："take several years, I think, to get to those levels"）
- 2026-07-29｜CFO｜margin：SAM 占 WFE 比重今年約 36%–36.5%（原話："36%, 36.5% this year, something like that"）
- 2026-07-29｜CEO｜product：SAM 比 2025 投資人日設定的時程更快接近高 30%（原話："faster than what we had outlined at our 2025 Investor Day"）
- 2026-07-29｜CEO｜product：NAND 每片晶圓 SAM 由 128 層到 500 層以上將倍增（原話："SAM per wafer in NAND to double from the 128-layer node"）
- 2026-07-29｜CEO｜product：Akara 裝機量逐年倍增（原話："Akara's installed base has doubled every year"）
- 2026-07-29｜CEO｜product：VECTOR 硬遮罩方案對客戶成本節省（原話："offers over 20% cost savings to customers"）
- 2026-07-29｜CEO｜product：今年將出貨首台 310x310 毫米面板設備（原話："we will also ship our first 310x310-millimeter panel tool"）
- 2026-07-29｜CFO｜customer：NAND 營收季增超過一倍（原話："NAND revenue dollars more than doubled sequentially"）
- 2026-07-29｜CFO｜customer：遞延收入增加主因是客戶預付款（原話："the largest of which was customer downpayments"）
- 2026-07-29｜CFO｜customer：中國整體 WFE 持平到微升（原話："China overall WFE is flat to slightly up"）
- 2026-07-29｜CEO｜customer：美國新邏輯客戶：僅表示有接洽（原話："we're engaged"）
- 2026-07-29｜CEO｜customer：客戶已在談 2027 年以後的設備訂位（原話："the discussions are now out in the '27 and beyond"）
- 2026-07-29｜CEO｜risk：交期具挑戰性（原話："lead times are challenging"）
- 2026-07-29｜CEO｜risk：NAND 2028 年展望：認為現在談還太早（原話："I think it's a little early on 2028"）
- 2026-07-29｜CFO｜risk：產業供給仍不足，延續到明年（原話："the industry is undersupplied this year"）
- 2026-07-29｜CFO｜competition：資料中心資本支出對應 WFE 的比率比先前估計高（原話："trending, I don't know, $1 billion or $2 billion higher"）
- 2026-07-29｜CEO｜competition：清潔設備：不回答是否為第一（原話："I don't know about the #1 player"）
- 2026-07-29｜CFO｜capital_allocation：資本支出管理在營收 4%–5%（原話："manage the company to 4% to 5% of revenue"）
- 2026-07-29｜CFO｜capital_allocation：股東回饋承諾：至少 85% 自由現金流（原話："plans remain to return at least 85% of free"）
- 2026-07-29｜CEO｜commitment：連續第三年優於 WFE（原話："third consecutive year of relative outperformance to WFE"）
- 2026-07-29｜CFO｜commitment：不提供逐季指引（原話："not going to guide you quarter by quarter through next year"）

### 問答異常語氣（迴避／改口／保留）
- LRCX_Q4_2026_Earnings_Call_20260729.md｜問：Malik：NAND 明年是否有供過於求跡象｜答法：未直接回答是否供過於求，改談 2028 還早、Lam 不只靠 NAND
- LRCX_Q4_2026_Earnings_Call_20260729.md｜問：Rasgon：產能不受限下 2027 能否給數字／逐季成長｜答法：兩次都拒絕給數字，只說每季都感覺更好
- LRCX_Q4_2026_Earnings_Call_20260729.md｜問：Blayne Curtis／Schneider：同類產品的調價狀況｜答法：不談同類比較的價格，只重述調價是多項因素之一
- LRCX_Q4_2026_Earnings_Call_20260729.md｜問：Pajjuri：WFE 1,500 億是否有上檔偏向｜答法：修正自己準備稿的說法：本季未再說上檔偏向

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
{"date":"20260730","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 驅動的晶圓廠設備支出上行延續至 CY2027，且 DRAM 與 NAND 需分開承保——DRAM 結構性緊、NAND 有轉鬆風險"},{"id":"H2","text":"Lam 的可服務市場占產業設備支出比重持續上升，第三／第四年連續跑贏產業——蝕刻與沉積強度隨 3D 化結構性上行"},{"id":"H3","text":"倍數正常化「部分完成」，但未完成——盈餘成長須跑贏仍在進行中的估值下修"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"NAND 供需 2027 轉鬆，帶動記憶體設備支出見頂——TrendForce 於 2026-07-27 明確預估 2027 NAND 轉向寬鬆、價格承壓，主因新產能上線疊加超高層數轉換，而終端消費需求疲弱。Lam 本季 NAND 系統營收季增逾一倍、占系統營收 23%（自 12%），正是最曝險的一段。"},{"id":"R2","text":"中國出口管制在 Lam 自己的品項上收緊——50% 關聯方規則（2025-09-29 實施）已實證造成 2025 年 12 月季約 $200M 營收衝擊，其一年暫緩約於 2026-10-30 到期；MATCH Act 2026 修訂針對低溫蝕刻設備（Lam 核心品項），現收窄為五家具名中國實體。同時中國國產設備在成熟節點持續替代：中微被稱全球第二大蝕刻商，中國廠商合計占全球設備市場自 2024 年 5.6% 升至 2025 年 6.5%。"},{"id":"R3","text":"倍數繼續向中樞回歸而盈餘未同步成長——30.85x 相對長窗中位 19.1x 溢價 61%（近五年中位 16.9x，溢價 83%）。若 2027 設備支出僅持平而非成長，倍數與盈餘同時修正即為戴維斯雙殺。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼待兩約束同時解除：10月法說CY2027 WFE≥$180B且NAND合約價未連2季跌；且關聯方規則到期處置明朗（衝擊<$150M/季）。獨立分支：價格≤$200且R1未觸發","irr_base_pct":7.4,"ev5y_pct":32.9,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":2.0,"ev5y_pct":32.9,"irr_base_pct":7.4,"max_dd_pct":-60.0,"bull_5y_price":553.5,"bear_5y_price":119.0,"p_bull_pct":26.0,"p_bear_pct":30.0,"rearm_trigger":"加碼待兩約束同時解除：10月法說CY2027 WFE≥$180B且NAND合約價未連2季跌；且關聯方規則到期處置明朗（衝擊<$150M/季）。獨立分支：價格≤$200且R1未觸發","price_at_dd":252.35,"archetype":"循環/商品","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LRCX_20261024/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
