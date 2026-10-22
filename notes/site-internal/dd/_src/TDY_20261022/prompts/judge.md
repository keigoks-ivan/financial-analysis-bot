你是 stock-analyst **v20 判斷 agent**，標的 TDY（20261022）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TDY","date":"2026-10-22","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TDY_20261022/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TDY_20261022/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1684.9,"period":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","citation":"公司 Q3 2026 earnings release（8-K 附件，IR 新聞稿全文）https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":402.6,"period":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","citation":"公司 Q3 2026 earnings release（8-K 附件，IR 新聞稿全文）https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":347.2,"period":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","citation":"公司 Q3 2026 earnings release（8-K 附件，IR 新聞稿全文）https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm"}},{"id":"f_kpi6_q4_2026_non_gaap_eps","label":"管理層指引：Q4 2026 non-GAAP EPS","value":"6.60–6.70","period":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","citation":"公司 Q3 2026 earnings release（8-K 附件，IR 新聞稿全文）https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm"}},{"id":"f_kpi7_2026_non_gaap_eps","label":"管理層指引：全年 2026 non-GAAP EPS","value":"25.40–25.50","period":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","citation":"公司 Q3 2026 earnings release（8-K 附件，IR 新聞稿全文）https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm"}},{"id":"f_kpi8_digital_imaging","label":"Digital Imaging 分部營收","value":903.0,"period":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","citation":"公司 Q3 2026 earnings release（8-K 附件，IR 新聞稿全文）https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm"}},{"id":"f_kpi9_funded_backlog","label":"Funded backlog","value":"近 5,300","period":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","citation":"公司 Q3 2026 earnings release（8-K 附件，IR 新聞稿全文）https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-21","period":"2026-10-21","unit":"date","basis":"距今 1 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-21"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_tdy_gross_margin_pct","label":"TDY 毛利率","value":43.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDY.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tdy_operating_margin_pct","label":"TDY 營業利益率","value":19.45,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDY.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tdy_fcf_margin_pct","label":"TDY FCF 利潤率","value":17.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDY.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ame_gross_margin_pct","label":"AME 毛利率","value":36.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AME.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ame_operating_margin_pct","label":"AME 營業利益率","value":25.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AME.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ame_fcf_margin_pct","label":"AME FCF 利潤率","value":23.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AME.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_keys_gross_margin_pct","label":"KEYS 毛利率","value":64.69,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KEYS.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_keys_operating_margin_pct","label":"KEYS 營業利益率","value":20.25,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KEYS.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_keys_fcf_margin_pct","label":"KEYS FCF 利潤率","value":22.32,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KEYS.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_ftv_gross_margin_pct","label":"FTV 毛利率","value":63.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FTV.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ftv_operating_margin_pct","label":"FTV 營業利益率","value":18.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FTV.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ftv_fcf_margin_pct","label":"FTV FCF 利潤率","value":24.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FTV.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":319.5,"period":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","citation":"公司 Q3 2026 earnings release（8-K 附件，IR 新聞稿全文）https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm"}},{"id":"f_kpi4_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":3.5,"period":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","citation":"公司 Q3 2026 earnings release（8-K 附件，IR 新聞稿全文）https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm"}},{"id":"f_kpi5_non_gaap_eps","label":"Non-GAAP 稀釋 EPS","value":6.72,"period":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-27 前後，公告於 2026-10-21）","citation":"公司 Q3 2026 earnings release（8-K 附件，IR 新聞稿全文）https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":630.1,"period":"2026-10-21（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-1.65,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":61.93,"period":"2026-10-21（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（24.74 → 24.74）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.04,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（26.79 → 26.8）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.03,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（28.94 → 28.93）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":24.74,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":26.8,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":28.93,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":2.36,"period":"2026-07-16 → 2026-10-21","unit":"%","basis":"FY1 共識 EPS 24.17 → 24.74（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":30.48,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.58,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.85,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":25.47,"period":"2026-10-21","unit":"x","basis":"分母＝FY1 EPS 24.74，分子＝快照價 630.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-21"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1686.9,"period":"2026-10-22","unit":"USD m","basis":"yfinance 最新一季：總債務 2027.0、現金 340.1（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":46.36,"period":"2026-10-22","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":30895.61,"period":"2026-10-22","unit":"USD m","basis":"市值 29208.71 ＋ 淨負債 1686.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6557.75,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（7 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":6929.3,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（10 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.71,"period":"2026-10-22","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-22","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 630.1 / W52 606.84 / W104 556.34 / W250 470.95 / W250 13週斜率 0.66%"},{"id":"f_ma_w52","label":"52 週均線","value":606.84,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":556.34,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":470.95,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.66,"period":"2026-10-22","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：部分客戶正開發競品或垂直整合以自有產品取代 TDY 產品；部分專利已到期或將到期，可能開放更多競爭；中國等國的競爭者可能受國家補貼而低價競爭。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"Furthermore, some of our patents have expired or are expiring, which could open up further competition. Additionally, some of our customers have been developing competing products or electing to vertically integrate and replace our products with their own.","as_of":"2026-02-20","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：中國、印度、沙烏地等國強化在地供應商與在地製造規定，已對 TDY 儀器、商用航太、海洋與數位影像營收造成負面影響；歐洲國防採購漸要求歐盟境內產線，TDY 若無法因應可能失去標案給歐盟業者。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"Many countries, including China, India and Saudi Arabia, have bolstered laws or regulations requiring the use of local suppliers, personnel and in-country manufacturing, which has had a negative impact on Teledyne’s revenues of instrumentation, commercial aerospace, marine and digital imaging products, as we currently have limited manufacturing operations in these countries.","as_of":"2026-02-20","retrieved_at":"20261022","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 競爭段：TDY 認為競爭者眾多且無單一對手提供相同產品線或涵蓋所有市場；各市場高度競爭，許多對手規模、裝機量與資源更大。公司未揭露份額數字。","source":"SEC EDGAR 10-K FY2025 Item 1 Business - Competition","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"we encounter a wide variety of competitors, none of which we believe offer the same product and service lines or serve all of the same markets as we do.","as_of":"2026-02-20","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因素揭露：部分客戶已在開發競品或選擇垂直整合，以自家產品取代 Teledyne 產品；國防電子一旦設計導入，客戶要求冗長資格測試才能換供應商。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"Additionally, some of our customers have been developing competing products or electing to vertically integrate and replace our products with their own.","as_of":"2026-02-20","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"投資人簡報摘要稱無單一客戶或國際目的地占銷售超過 5%","source":"Quartr Teledyne investor presentation summary","url":"https://quartr.com/events/teledyne-technologies-incorporated-tdy-investor-presentation_3PBpkih5","excerpt":"No single customer or international destination accounts for more than 5% of sales, reducing concentration risk.","as_of":"2026-09-04","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"FY2025 無任何商業客戶占任一部門或全公司淨銷售超過10%；美國政府占25.5%，主要客戶美國戰爭部（原國防部）銷售$1,203.6M","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"No commercial customer in 2025 or 2024 accounted for more than 10% of net sales for any of our segments or for the total Company.","as_of":"2026-02-20","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"中國客戶約占營收4%，無單一境外國家超過10%","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"Our net sales to China-based customers represented approximately 4% of total revenues in 2025 and 2024, respectively.","as_of":"2026-02-20","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TDY 2026 Q2 摘要：創單季營收與營業利益紀錄，紅外線成像、無人系統、國防電子帶動；5 億美元級以上之 $5 billion 已資金到位積壓訂單，book-to-bill 連續十季高於 1；全年財測連兩季上修。","source":"fn2.ai TDY FY2026 Q2 earnings summary","url":"https://fn2.ai/earnings/tdy/2026-q2","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"同類摘要指毛利擴張部分來自關稅相關效益（分析師存疑），鍺與稀土磁鐵供給可能限制生產；另有評論指有機成長落後於併購成長、國防銷售高峰可能回歸常態。","source":"fn2.ai TDY earnings page; AlphaStreet","url":"https://fn2.ai/earnings/tdy","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Freedonia 預測美國分析儀器需求至 2028 年名目年增 3.1%，由研發支出與製造業出貨支撐（產業層級，非 TDY 專屬）。","source":"Freedonia Group press release","url":"https://www.freedoniagroup.com/press-releases/r-d-spending,-manufacturing-to-drive-increase-in-us-analytical-instrument-demand","excerpt":null,"as_of":"2024-10-01","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因素稱併購能力取決於取得監管核准，包含日趨嚴格的合併管制與外國直接投資法規；搜尋未見 2026 年針對 TDY 的美國 DOJ／FTC 或歐盟反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"Our ability to make acquisitions depends on a number of factors, including the availability of potential acquisition candidates at reasonable prices, competition from other bidders, the ability to obtain regulatory approvals, including under increasingly stringent merger control and foreign direct investment laws, and the availability of debt and equity financing, among other factors.","as_of":"2026-02-20","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"中國商務部 2025-04-04 對 Varex 啟動反傾銷調查並延長至 2026-10-03；兩位競爭法律師認為不太影響 SAMR 對 Teledyne 收購 Varex 的合併審查。","source":"ION Analytics Mergermarket 分析","url":"https://ionanalytics.com/insights/mergermarket/parr/beyond-supply-considerations-varex-teledyne-faces-limited-competition-concerns-in-china-analysis/","excerpt":"(MOFCOM) initiated an anti-dumping investigation involving Varex on 4 April 2025 and subsequently extended the investigation through 3 October 2026. Under the relevant rules, the investigation is expected to conclude shortly and cannot be extended further. Two competition lawyers told this news service that the anti-dumping investigation is unlikely to affect SAMR’s merger review.","as_of":"2026-10-07","retrieved_at":"20261022","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：中國將包含兩家 Teledyne 法人實體列入不可靠實體清單或出口管制清單，並限制鎵、鍺等材料出口，已影響部分數位影像與航太國防產品的生產與定價。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"In response, China has unveiled restrictions on exports from China of certain materials and components, including gallium and germanium and which are used in semiconductor manufacturing and permanent magnets and which have impacted 9 Table of Contents the production and pricing of some of our digital imaging and aerospace and defense products. China has also increased sanctions on certain specific U.S. companies, including two Teledyne legal entities, by adding them to its Unreliable Entity List or Export Control List","as_of":"2026-02-20","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K MD&A：關稅仍有效，中國限制稀土出口；公司稱製造據點分散於多國可緩解部分關稅衝擊，並可能以調價因應。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"Our manufacturing facilities span across many countries which helps us mitigate the impact of certain tariffs and trade restrictions. Also, consistent with our strategy, we continually optimize our operations and take measures to contain costs to reduce the impact from tariffs. We may also implement additional pricing actions to mitigate the impact of these tariffs.","as_of":"2026-02-20","retrieved_at":"20261022","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：公司曾就 Teledyne FLIR 自非美國轄區出貨、de minimis 計算方式錯誤導致未取得許可，向美國國務院與商務部 BIS 自願揭露。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"We have made other voluntary disclosures to the U.S. Department of State and the U.S. Department of Commerce, including to the Bureau of Industry and Security (“BIS”) with respect to Teledyne FLIR shipments of products from non-U.S. jurisdictions which were not licensed due to incorrect de minimis calculation methodology under the Export Administration Regulations.","as_of":"2026-02-20","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Q2 2026 財報電話會議：關稅退款使利潤率受惠，淨一次性效益約 $10M，主要在 Digital Imaging；管理層並提及關稅變動、鍺與稀土磁鐵供應疑慮。","source":"MarketBeat Teledyne Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/teledyne-technologies-q2-earnings-call-highlights-2026-07-22/","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"中國商務部 2025-10-09 將 Teledyne FLIR 等 14 家外國實體列入不可靠實體清單。","source":"Bloomberg Law: China Adds More Foreign Entities to Unreliable Entity List","url":"https://news.bloomberglaw.com/ip-law/china-adds-more-foreign-entities-to-unreliable-entity-list-1","excerpt":null,"as_of":"2025-10-09","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 稱中國與台灣若爆發軍事衝突，將對在該地區的銷售與供應鏈造成重大不利影響","source":"Teledyne FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"A military conflict between China and Taiwan would likely have a material adverse impact on our ability to sell products to customers in these areas and on our supply chain.","as_of":"2025-12-28","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2025 與 2024 年對中國客戶銷售約占總營收 4%","source":"Teledyne FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"Our net sales to China-based customers represented approximately 4% of total revenues in 2025 and 2024, respectively.","as_of":"2025-12-28","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中國、印度、沙烏地要求在地供應商與在地製造，公司在這些國家製造有限，已損及數條產品線營收","source":"Teledyne FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"Many countries, including China, India and Saudi Arabia, have bolstered laws or regulations requiring the use of local suppliers, personnel and in-country manufacturing","as_of":"2025-12-28","retrieved_at":"20261022","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"歐洲國防採購愈來愈要求歐盟境內生產設施，無法滿足則可能無法投標新專案","source":"Teledyne FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"requirements to have production facilities in the EU are becoming more common to win contracts. If we are unable to respond to these requirements, we may be unable to bid on new programs","as_of":"2025-12-28","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"PolicyRisk 摘要：公司揭露中國軸風險含稀土與永磁限制、關稅、出口管制收緊","source":"PolicyRisk.com TDY company page","url":"https://policyrisk.com/world/company/TDY","excerpt":"On the China axis it flagged Beijing's restrictions on rare earth minerals and permanent magnets used in its products, new and proposed tariffs, tightening export controls","as_of":"2026-02-01","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Digital Imaging 銷售 $903.0M，年增 15.0%，主因紅外線偵測器、國防與商用元件／子系統、海事產品等","source":"Teledyne Q3 2026 earnings release (8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm","excerpt":"The Digital Imaging segment's third quarter 2026 net sales were $903.0 million compared with $785.4 million, an increase of 15.0%.","as_of":"2026-10-22","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 Instrumentation 銷售 $370.5M，年增 1.9%；環境儀器增加（含 $6.2M 併購貢獻）、海事儀器增加，電子測試與量測減少 $4.8M","source":"Teledyne Q3 2026 earnings release (8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm","excerpt":"The Instrumentation segment's third quarter 2026 net sales were $370.5 million compared with $363.6 million, an increase of 1.9%.","as_of":"2026-10-22","retrieved_at":"20261022","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Aerospace and Defense Electronics 銷售 $287.4M，年增 4.3%；國防電子 +$16.5M、航空電子 −$4.6M","source":"Teledyne Q3 2026 earnings release (8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm","excerpt":"$287.4 million compared with $275.5 million, an increase of 4.3%.","as_of":"2026-10-22","retrieved_at":"20261022","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Engineered Systems 銷售 $124.0M，年增 7.8%，主因工程產品","source":"Teledyne Q3 2026 earnings release (8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm","excerpt":"The Engineered Systems segment's third quarter 2026 net sales were $124.0 million compared with $115.0 million, an increase of 7.8%.","as_of":"2026-10-22","retrieved_at":"20261022","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 電話會議：國防需求加速、飛彈彈藥年化約 $200–250M、無人系統營收約 $575M、水下國防儀器約 +20%","source":"Motley Fool Q2 2026 earnings call transcript","url":"https://www.fool.com/earnings/call-transcripts/2026/07/22/teledyne-tdy-q2-2026-earnings-call-transcript/","excerpt":"defense and munitions programs. Management clarified that approximately 65% of the company's total portfolio remains commercial, providing geographic and market balance across the United States and international markets. Executive Chairman Mehrabian highlighted the success of the Black Hornet 4 nano drone, which is contributing to the 12% projected revenue growth in total unmanned systems for","as_of":"2026-07-23","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素揭露：競爭對手在導入 AI 與其他顛覆性技術上可能比 Teledyne 更快或更成功，會削弱其競爭力；未點名具體替代技術。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"Our competitors may be faster or more successful than we are in incorporating AI and other disruptive technology into their offerings, which would impair our ability to compete successfully.","as_of":"2026-02-20","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026（2026-10-21 公布）公司把全年非GAAP EPS 指引上調至 $25.40–$25.50（7 月為 $24.45–$24.65），Q4 非GAAP EPS 指引 $6.60–$6.70；未提供營收指引。","source":"Teledyne 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000055/q3-2026earningsrelease.htm","excerpt":"full year 2026 non-GAAP diluted earnings per share will be in the range of $25.40 to $25.50.","as_of":"2026-10-21","retrieved_at":"20261022","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 非GAAP EPS $6.72，高於公司 7 月自家指引 $6.05–$6.15 與當時市場共識 $5.98；營收 $1,684.9M，年增 9.4%。","source":"Teledyne Q3 2026 earnings release（經搜尋摘要）／MarketBeat 2026-07-22","url":"https://www.marketbeat.com/instant-alerts/teledyne-technologies-nysetdy-issues-q3-2026-earnings-guidance-2026-07-22/","excerpt":null,"as_of":"2026-10-21","retrieved_at":"20261022","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布因來源而異：Benzinga 2026-08-31 共識 Buy（9 位分析師，8 Buy／1 Hold），平均目標價 $631；Morgan Stanley 8/13 升至 $715、Barclays 7/24 升至 $640；FN2 8/1 列 Jefferies $830、Stifel $775、Needham $750；MarketBeat 平均 $694.14。均為 Q3 公布前的快照。","source":"Benzinga／FN2／MarketBeat 聚合頁（搜尋摘要）","url":"https://kr.benzinga.com/quote/TDY/price-targets","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共13份，其中含重大項目者3份；無併購完成（2.01）、重編（4.02）類項目，唯一 1.01 為信貸協議修訂（取消 SOFR 調整 10bp）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001094285&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-10-22","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"10-K 稱未發生重大石棉訴訟負債，其他訴訟預期不致對財務狀況造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"While the outcome of litigation cannot be predicted with certainty, and some of these lawsuits, claims or proceedings may be determined adversely to the Company, management does not believe that the disposition of any such pending matters is likely to have a material adverse effect on the Company’s financial condition.","as_of":"2026-02-20","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026上半年完成一件併購（DD-Scientific，英國氣體感測，歸 Instrumentation 部門），上半年併購支出約5340萬美元；2025年完成四件小型併購。","source":"SEC 10-Q FY2026 Q2（經搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/0001094285/000109428526000043/tdy-20260628.htm","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["valuation","moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K 揭露僅有石棉等一般訴訟，未曾發生重大負債；搜尋未見證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm","excerpt":"To date, we have not incurred material liabilities in connection with these lawsuits.","as_of":"2026-02-20","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單無 Item 4.02（重編）；搜尋未見 SEC 調查。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001094285&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-10-22","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"TDY","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":43.34,"operating_margin_pct":19.45,"fcf_margin_pct":17.92,"rd_intensity_pct":5.26},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDY","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"AME","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.36,"operating_margin_pct":25.9,"fcf_margin_pct":23.21,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AME","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"KEYS","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.69,"operating_margin_pct":20.25,"fcf_margin_pct":22.32,"rd_intensity_pct":18.13},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KEYS","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"FTV","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":63.23,"operating_margin_pct":18.23,"fcf_margin_pct":24.36,"rd_intensity_pct":6.07},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FTV","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"TDY"},"financial_history":{"ticker":"TDY","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":5458600000.0,"revenue_yoy_pct":null,"gross_margin_pct":42.69,"operating_margin_pct":17.81,"net_income":788600000.0,"diluted_eps":16.53,"free_cash_flow":394200000.0,"fcf_margin_pct":7.22,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":5635500000.0,"revenue_yoy_pct":3.24,"gross_margin_pct":43.29,"operating_margin_pct":18.36,"net_income":885700000.0,"diluted_eps":18.49,"free_cash_flow":721200000.0,"fcf_margin_pct":12.8,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":5670000000.0,"revenue_yoy_pct":0.61,"gross_margin_pct":42.94,"operating_margin_pct":18.37,"net_income":819200000.0,"diluted_eps":17.21,"free_cash_flow":1108200000.0,"fcf_margin_pct":19.54,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":6115400000.0,"revenue_yoy_pct":7.86,"gross_margin_pct":42.76,"operating_margin_pct":18.8,"net_income":894800000.0,"diluted_eps":18.88,"free_cash_flow":1074000000.0,"fcf_margin_pct":17.56,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TDY/TDY_Q3_2026_Earnings_Call_20261021.md）

# Q3 2026 Earnings Call
**Teledyne Technologies Incorporated** | Earnings Calls | 2026-10-21

**Operator** (Operator):
Welcome to Teledyne's Third Quarter Earnings Call. Here's our first speaker, Mr. Jason VanWees.

**Jason VanWees** (Executives):
Good morning, everyone. Thanks for joining us. This is Jason VanWees, Vice Chairman of Teledyne, and I'd like to welcome everyone to Teledyne's Third Quarter 2026 Earnings Release Conference Call. We released our earnings earlier this morning before the market opened. Joining me today are Teledyne's Executive Chairman, Robert Mehrabian; President and CEO, George Bobb; EVP and CFO, Steve Blackwood; and Melanie Cibik, EVP, General Counsel, Chief Compliance Officer and Secretary. After remarks by Robert, George and Steve, we will answer your questions.
However, our attorneys have reminded me that before we get started, all forward-looking statements this morning are subject to various assumptions, risks and caveats as noted in the earnings release and our periodic SEC filings, and of course, actual results may differ materially. In order to avoid potential selective disclosures, this call is simultaneously being webcast, and a replay via webcast and dial-in will be available for approximately 1 month. Here is Robert.

**Robert Mehrabian** (Executives):
Thank you, Jason, and good morning, everyone. Our third quarter sales and operating earnings were the strongest in Teledyne's history. For the third quarter in a row, we're raising our full year 2026 sales and earnings guidance. In January, we forecasted revenue of $6.37 billion, a 4.2% increase from 2025, and non-GAAP earnings of $23.65 per share. Today, our outlook for 2026 sales is $6.625 billion, a year-over-year increase of 8.3% and nearly double the growth rate projected in January.
And earnings of $25.45 per share, which is $1.80 per share or almost 8% higher than forecast in January, and it's a 16% increase compared to last year. For all of Teledyne, orders have exceeded sales for 12 consecutive quarters, and funded backlog is now approximately $5.3 billion. In the third quarter, organic growth accelerated in our Digital Imaging segment and was led by sales of infrared detectors and subsystems for space and unmanned applications. 
Furthermore, each of our major commercial imaging businesses, such as industrial vision sensors and systems as well as healthcare, increased year-over-year. Our third quarter performance reflected not only the strong execution of the backlog that we've been building for 3 years, but also the strength of our business portfolio and what Teledyne is today, a company with a broad set of sensors and vertically integrated platforms from space to deep sea.
We also continue to enjoy robust free cash flow and recently made $224.6 million of opportunistic stock repurchases at a weighted average price of approximately $607 per share. We did the same in 2025 and 2024 when we felt Teledyne was undervalued. During the past 3 years, we've deployed nearly $980 million to buy back shares of our company at a total weighted average price of $479 per share.
Regarding the pending acquisition of Varex, we were following the company for more than 6 years. As healthcare and life sciences markets began to recover earlier this year, we felt the timing was finally right for us to pursue and then announce this highly complementary acquisition in the third quarter. The regulatory process is underway, and Varex's special stockholder meeting is scheduled for October 28. We continue to anticipate closing early in 2027. 
Notwithstanding the stock repurchases and the pending acquisition, current leverage remains at the lowest level in 6 years, and we have more than ample flexibility to continue compounding earnings growth for years to come. 
George will now comment on the performance of our 4 business segments.

**George Bobb** (Executives):
Thank you, Robert. In the Digital Imaging segment, third quarter sales increased 15% and 14.3% organically due to well-balanced growth among our defense and commercial businesses. Sales of infrared detectors for space-based imaging increased more than 25%, as did revenue from infrared subsystems and cameras for our customers' unmanned air systems and unmanned maritime surface vehicles. In addition, segment sales increased in each of our larger commercial end markets. That is, sensors and cameras for industrial and scientific vision applications, X-ray products for healthcare, commercial thermography cameras, electronics for maritime navigation, geospatial sensors and software and microelectromechanical systems, or MEMS. Finally, non-GAAP operating margin in the segment increased 376 basis points to 25.4%.
In the Instrumentation segment, which consists of our marine, environmental and test and measurement businesses, third quarter sales increased 1.9% versus last year. Overall sales of marine instruments increased 2%, primarily due to strong defense-related sales of interconnects for U.S. Virginia and Columbia submarines as well as continued growth in the offshore energy exploration and production market.
Sales of environmental instruments increased 7.1% due to increased sales of gas monitoring instrumentation, along with more modest growth in sales of laboratory and life sciences instruments. Sales of electronic test and measurement systems decreased 6.3% due in part to the timing of orders, which increased 18% year-over-year for a record book-to-bill ratio of 1.23. Instrumentation non-GAAP operating margin in the third quarter decreased modestly due to product mix but was sequentially higher for the second consecutive quarter.
In the Aerospace and Defense Electronics segment, third quarter sales increased 4.3%. Growth in Defense Electronics of 7.4% was partially offset by lower sales in commercial aerospace. However, third quarter bookings were very strong in both the defense and aerospace markets, with a segment book-to-bill ratio of 1.29. Non-GAAP segment margin increased 86 basis points year-over-year, even though there was a greater mix of Defense Electronics, which, as a whole, have a lower operating margin compared with commercial avionics. 
For the Engineered Systems segment, third quarter revenue increased 7.8%, driven primarily by greater sales of marine and other manufacturing programs. Segment operating margin was largely flat with last year. 
I will now pass the call back to Robert.

**Robert Mehrabian** (Executives):
Thank you very much, George. To conclude, right now, virtually all of our businesses are moving in a positive direction simultaneously, and our growth remains balanced across many end markets and geographies and not due to any singular, potentially fleeting market driver. Given our backlog, the pending acquisition of Varex, our strong balance sheet and outstanding operating discipline, I'm already looking forward to 2027. 
I will now turn the call over to Steve.

**Stephen Blackwood** (Executives):
Thank you, Robert, and good morning. I will first discuss some additional financials for the quarter not covered by Robert, and then I will discuss our fourth quarter and full year 2026 outlook. 
In the third quarter, cash flow from operating activities was $352.5 million compared with $343.1 million in 2025. Free cash flow, that is, cash flow from operating activities less capital expenditures, was $319.5 million, a third quarter record, compared with $313.9 million in 2025. Cash flow increased due to favorable operating results in the third quarter of 2026 compared with 2025, partially offset by higher inventory purchases. Capital expenditures were $33 million in the third quarter of 2026 compared with $29.2 million in 2025. Depreciation and amortization expense was $84.7 million in the third quarter of 2026 compared with $84.5 million in 2025. We ended the quarter with $1.47 billion of net debt, that is, approximately $2.03 billion of debt less cash of $562.4 million.
Now turning to our outlook. Management currently believes that GAAP earnings per share in the fourth quarter of 2026 will be in the range of $5.68 to $5.83, with non-GAAP earnings per share in the range of $6.60 to $6.70. And for the full year 2026, we believe that GAAP earnings per share will be in the range of $21.71 to $21.87 and non-GAAP earnings per share in the range of $25.40 to $25.50. 
I will now pass the call back to Robert.

**Robert Mehrabian** (Executives):
Thank you, Steve. We would now like to take your questions. Rob, if you're ready to proceed with the questions and answers, please go ahead.

**Operator** (Operator):
[Operator Instructions] And the first question today comes from the line of Zachary Walljasper with UBS.

**Zachary Walljasper** (Analysts):
My first question is around backlog. So total company backlog has grown sequentially every quarter so far this year. So with the trends you're seeing in unmanned, space, can you just talk about the visibility that the team is building on from a top line perspective heading into 2027? Because based on the awards you're winning now, I would assume they'll be delivered next year. 
And then my second question is around instrumentation. It sounds like, from the prepared remarks, there's a bit of a mistiming or a bit of a timing in orders. Was that just for test and measurement or for the whole segment?

**Robert Mehrabian** (Executives):
Thank you, Zach. Let me take the backlog question first. I want to just take it on a larger scale. As we mentioned, the backlog right now stands at $5.3 billion. Of that, about 72% will be available for us to -- as a revenue in the last -- next 12 months. To put that in perspective, that number is about half of the revenue that we enjoy for 2026. Now the backlog in other areas, it varies. But basically, a lot of our longer-term defense and other areas, the backlog is for the full 18 months and 9 months of it being, as I mentioned. 
And overall, we think, if you look at the different segments, even in instruments that George talked about and you just mentioned, our book-to-bill is 1.07. So we feel pretty good about it. Even though the revenue may have been down in certain parts of that, overall, the pickup in our orders in Q3 points to a very favorable future.

**Operator** (Operator):
Our next questions are from the line of Andrew Buscaglia with BNP Paribas.

**Andrew Buscaglia** (Analysts):
I wanted to touch on Digital Imaging. Just it seems like things have really accelerated, and it seems really broad-based. But what changed intra-quarter that made you exceed your expectations by so much? Was it on the defense side? Or is it more kind of commercial infrared stuff that really picked up?

**Robert Mehrabian** (Executives):
Yes. I think, Andrew, obviously, we anticipated, based on the orders we had, that we would do better than we initially thought. But obviously, everything depends on execution. I think, when you look at our Digital Imaging and you look at it both as what we call our historical Digital Imaging, which would be our Teledyne DALSA, e2v, our imaging systems here, what we call Teledyne Scientific & Imaging, those grew very nicely, primarily due to space. As you know, we do a lot of work in space with our infrared image sensors, and the whole missile warning and tracking system has been a really good domain for us. So that picked up. 
The other area, of course, is the unmanned systems, and that did very well, better than we thought. And then lastly, in the commercial domain, which is machine vision, healthcare, microelectromechanical systems, if you add them all up, they all did very well. And Digital Imaging book-to-bill as a whole, both what we call our legacy and FLIR, had a book-to-bill of about 1.22x. So things worked out across the board very well.

**Andrew Buscaglia** (Analysts):
Okay. Yes. And maybe the next question on Digital Imaging margins. Can you talk about expectations around gross margin going forward, given price/cost dynamics? And then it looks like R&D and SG&A are growing quite fast. I thought, last year, you guys were -- you took out some costs, but those -- so presumably, those wouldn't be growing that way. But can you talk a little bit more about, on the OpEx side, what you expect from here?

**Robert Mehrabian** (Executives):
Well, I'll let George talk about the cost structure because that's been a significant undertaking in the whole Digital Imaging domain, especially in what we call our historical Digital Imaging. All along, we've said that FLIR is going to do better year-over-year, quarter-over-quarter, and it's finally arrived at a point where we feel very comfortable with the growth, both in revenue as well as earnings. Overall, we're projecting robust growth in FLIR year-over-year of 12% and in defense as well as commercial domain. 
In terms of the cost structure, I'll let George, as I said, answer it. But I think what we're aiming for is to continuously improve our margins. And we started the year -- just broadly, we started the year by saying Digital Imaging margins would grow about 150 basis points in Q2. Today, we've added another 61 basis points. So we're projecting for the whole year margins to grow 225 basis points. So with that, I'll pass this to George to talk about the cost structure.

**George Bobb** (Executives):
Sure. So we did take cost out in 2025. We're getting the benefit of that, as evidenced by the margins that we had here in Q3, up 180 basis points. And gross margins are up year-over-year, at least in the neighborhood of 100 basis points. Beyond that, R&D really wasn't up materially in the quarter. And I think the rest of the cost structure is fine. So I think we're getting the benefit of the cost we took out and obviously, the volume growth that we have.

**Robert Mehrabian** (Executives):
That's about -- I hope that answers your question.

**Operator** (Operator):
The next question is from the line of Sheila Kahyaoglu with Jefferies.

**Adam Samuelson** (Analysts):
It's Adam Samuelson on for Sheila. Maybe the first question is on Instrumentation. I know you talked about test and measurement kind of bookings improving and that giving you confidence on the outlook for the top line as you go into the fourth quarter. But I'm wondering if you could comment on kind of the margin outlook there. Is that -- as we think about that mix maybe flipping more favorably within the segment, should we think about that segment returning to year-on-year margin expansion in the fourth quarter? And I mean, is there any way you think about the margin trajectory for that business as we move into 2027?

**Robert Mehrabian** (Executives):
Thank you, Adam. I'll pass this one back to George again.

**George Bobb** (Executives):
Yes. I think, largely, we continue to see sequential margin improvement as we go through the year. Quarter-over-quarter, I don't think we'll quite get back to 2025 margins in Q4. Having said that, based on the outlook for 2027, we feel good about the direction we're headed.

**Adam Samuelson** (Analysts):
Got it. And then, maybe just switching gears, if I could sneak one more in. Back in Digital Imaging on the unmanned side, any way to differentiate the demand for infrared subsystems for customer platforms versus your own? And any thoughts on kind of -- is there any need for incremental capacity to support some of the demand growth that you're seeing there?

**Robert Mehrabian** (Executives):
Yes. First of all, our subsystems have been the strongest of all of our defense programs. In the infrared and visible domain, our sensors, as you said, we supply to our own as well as other people, and that has grown substantially year-over-year. There are good reasons for that. One of them is, obviously, as the demand is growing, the ability to meet the demand and the confidence that the customers have in a demand environment that you will be supplying and not get offline becomes very, very important.
And the second thing is, of course, we're improving our product continuously. We have 12-micron, which -- detectors that we've been shipping. Now we have announced 8-micron plus software additions, et cetera. On the bigger system, which would be our total defense system, we're looking at about a 10% growth, whereas in the subsystems, we're looking at multiple of that.

**Operator** (Operator):
The next questions are from the line of Jonathan Siegmann with Stifel.

**Jonathan Siegmann** (Analysts):
Congratulations on the nice, balanced growth across the portfolio again. A question on the budget environment. Teledyne has some terrific exposure both in space and in drones and counter-drone applications. Those are disproportionately funded by some of the reconciliation money, which there is some worries out there may be stalled out in the months ahead in Congress. As a supplier, what impact does that have on your business? What are your prime customers saying in terms of any impact on this powerful growth you're seeing?

**Robert Mehrabian** (Executives):
That's a very good question. There's -- right now, as you mentioned, there's uncertainty in the budget. On the other hand, because of our longer-term programs that we've won, including the most recent one in the Golden Dome, we don't see an issue for us in 2027. Having said that, there's other things that are happening that may change the outlook in '28 and '29, we don't know. On the other hand, right now, sitting where I am and where George is, we think we're okay in 2027 with all the uncertainties surrounding the budget as well as everything else that's going on in Europe and the Middle East.

**Jonathan Siegmann** (Analysts):
And if I could just slip one in on Varex, given we're used to looking at businesses that fly and blow up. Just can you -- I understand you've looked at Varex for quite some time. Maybe could you talk a little bit about what attracted you to that business and maybe comment on some of the declines in revenue that business saw and why you're excited about it? I'd appreciate it.

**Robert Mehrabian** (Executives):
That's a very good question. First of all, we've been looking at that business for a long time, at least in the last 6 years, pretty actively. We wanted to buy pieces of that business before. We were not able to. But what happened is, recently, as the whole arena of healthcare and products that they make began to recover, we thought it was an appropriate time for us to approach them, and that would be obviously in the recovery after the post-COVID era. And we were able to approach them. We were able to go through the process. They had a lot of other potential buyers that they were dealing with. And that's, by the way, detailed in their merger proxy. And in the end, we ended up with a friendly transaction. 
Why Varex? Very simple. We have healthcare products. We have X-ray detectors, but nothing like they do. We primarily focus on ceramic metal-oxide detectors which are small in size, cannot tolerate high energy, high X-ray energy levels like you have in oncology. They have a bunch of other detectors led by amorphous silicon that are uniquely designed for high-energy oncology X-rays. Also, they have really different complementary products to us. And I'll end up with one thing that they have that's exciting to us, and that's their photon detectors, which can detect X-rays without having to go through an intermediate layer called scintillation. And that's very attractive to us because we've always wanted to get into that field, and they're already in it, have advanced in it. 
And we think while the revenue has been relatively flat, we think, for us, the opportunity is to improve margins like we've done in all of our acquisitions. I'll give you one example, FLIR. We bought it at a multiple of 16.7x to EBITDA. If you look at it today, in just 4 years, that's down to 13.7x. And broadly, Teledyne has improved almost every acquisition that we've made and improved the margins. I would say, on the average, we've paid 13.5x EBITDA. And today, they're less than 8x. So that's the other driver, is we think we can improve it with our 80-20 programs, with not having the public costs associated with a smaller public company. So that kind of sums up the best answer I can give you at this time.

**Jonathan Siegmann** (Analysts):
Great. Congratulations on it, and a nice final one for Jason to have his contributions on. Good luck with it.

**Operator** (Operator):
The next question is from the line of Guy Hardwick with Barclays.

**Guy Drummond Hardwick** (Analysts):
Robert, considering your pretty upbeat comments on the backlog, are you willing to give us kind of an early look as to what revenue growth potential could be in 2027, excluding the Varex acquisition? And just as -- and I'll ask my follow-up now. Did Digital Imaging margins in Q3 benefit from any tariff reversals or refunds?

**Robert Mehrabian** (Executives):
No. The refunds were really taken up in Q2. So it doesn't affect Q3. Let me start there. It's a little early for us to talk about '27. Matter of fact, we had our first cut of half of our businesses that George went through with our Board. I think our momentum is there. I think we will improve next year again, whether it be at the level we did this year or projecting to do this year, I don't know, it's a little early. Improve? We will. That I can tell you.

**Operator** (Operator):
The next question is from the line of Joe Giordano with TD Cowen.

**Joseph Giordano** (Analysts):
So on the orders there, I mean, again, at the consolidated level, really strong. It's pretty similar number to what you had in dollars last quarter. I'm just curious if there is any parts of that where you feel like are customers ordering earlier or excessively because of worries about a budget or anything like that? I mean, I know your products are not like stocked in inventory typically or anything like that. But just curious if there's any parts of the business where you feel like there is a little bit of different order patterns for whatever reason?

**Robert Mehrabian** (Executives):
Yes. Joe, I don't think so. We haven't seen anything unusual. The kind of -- the backlog, the orders are broad-based across our products. We're not looking at any huge movements because of data centers or other things. So we feel comfortable about that. So that's the best answer I can give. We haven't noticed anything unusual across our portfolio.

**Joseph Giordano** (Analysts):
Okay. And then on Varex, like I think I cut -- my phone cut out a little bit. You may have gotten into this a little bit on the last question. But on the growth side of Varex, I mean, you guys have showed the ability to cut costs out. And so I think people would expect that on the margin side. But growth, you mentioned it's been flattish. Like, what do you do there? Is that just the market dynamic? I know you're probably not wanting to buy something that's wildly dilutive to the total growth profile of Teledyne. So what do you do there to stimulate that?

**Robert Mehrabian** (Executives):
Yes. I think, first, we're going to apply -- like we do in our own -- all of our businesses every single quarter, every single month, we're going to apply our 80-20 principles to Varex. What do we mean by that? We haven't done detailed analysis because, obviously, we're going through the process now. So the first thing in 80-20 is that's probably going to shrink revenue somewhat because we look at the 80% of the revenue that is substantially available for us to improve margins. And there's 20% that goes to smaller customers that are dilutive to earnings. 
And we do that across Teledyne. If you looked at Teledyne today versus 4, 5 years ago, we've reduced the number of SKUs that we have by 50%. So we're going to do that first. So that might actually reduce our revenue a little bit at the beginning. But then we think after that, we think we'll get back to midsized -- mid-single-digit growth like we do under normal circumstances across our own portfolio. And we'd obviously look for synergies where we can sell similar but different products to the same customer. So I think, initially, revenue down a little bit, margins up, gross margins up in almost the first year accretive. And then as we go forward, grow the business like we've done every other acquisition that we've made.

**Joseph Giordano** (Analysts):
If I could just sneak one more in. Do you foresee Varex like the go-to-market strategy? Is there -- are they going to work independently from the offerings you already have? Is it 2 separate sales teams? Or is this going to be like one face of Teledyne going to these same customers?

**Robert Mehrabian** (Executives):
I think it's going to be one face. That is very important because George really was the architect of what we call One Teledyne, and it's not just across healthcare, but across all of our products. So when a market representative, a sales representative approaches a company, whether it's a defense company or a commercial company, they have the visibility of all of our products. And so somebody in defense might mention some of the products we have in the commercial domain. We're going to do the same thing with Varex. It's not going to be separate. It's going to be One Teledyne approach.

**Operator** (Operator):
The next questions are from the line of Ron Epstein with Bank of America.

**Ronald Epstein** (Analysts):
So yes, just quickly, I didn't hear much discussion around how are supply chains holding up for you? When we've gone to some of the recent trade shows, we've heard that there's shortages on things like printed circuit boards and some basic electronic components given all the, I'm going to say it, capacity that's being thrown to the hyperscalers and the AI build-out that they're kind of like sucking up everything. How is that impacting you guys? And how are you managing it?

**Robert Mehrabian** (Executives):
Well, that's a very good question. Obviously, there's a lot of shortages. We have a dedicated team that works with our businesses, that ensures that we get what we need to produce our products. The only problem that we see because of the shortages, the inflation, specific inflation to the different areas you mentioned is higher than normal. But we try and make up for that with price increases. This year, we've been successful in enjoying probably one of our better price increases across our portfolio. 
So it's an annoyance from an inflation perspective. And sometimes you have a hard time getting specifically what you need, but we're very aggressively planning ahead with our suppliers, recognizing that some of the shortages would probably not last, let's put it that way.

**Operator** (Operator):
The next question is from the line of Noah Poponak with Goldman Sachs.

**Noah Poponak** (Analysts):
Jason, congrats on your announcement, and thanks for all the time you spent with us over the years, always super helpful.

**Jason VanWees** (Executives):
Thanks, Noah. I'll see you in December, so I'm still here for now.

**Noah Poponak** (Analysts):
Yes, appreciate that. Robert, given the diversification of your business as well as you guys have done over the years, there aren't that many quarters in any of the businesses that look like the last 2 growth rates in Digital Imaging. I guess it leaves me wondering how sustainable is that? Because what's happening in the defense verticals you feed into right now is pretty unique and at least for now, seems fairly enduring. And I guess you kind of have that happening at the same time that your commercial side is picking up, that has a little bit more of a cyclical element to it. Can we -- do you see these growth rates sustaining for a period of time? Or is this more the early pickup on easy compares?

**Robert Mehrabian** (Executives):
Thank you, Noah. Very good question as usual. Difficult one to answer. Let me just say, short term and short term 2027, we think that we're going to do better than we have historically. This year, as you know, we're looking at about 8.3%, 8.4% growth, that's organic, which is higher -- the organic, sorry, it's about 7.5% (sic) [ 10% ], but still, it's higher than what we've enjoyed the last 15 years or so.
I think that's going to sustain, maybe not exactly at that level, but it's going to be better than low single digits, which we've been stuck on for a while. Mid- to higher single digits is what we're anticipating. It's hard to say, but Noah, we have a balanced portfolio. We've intentionally worked very hard to balance our portfolio so that when things get tough, we survive and do well, and when things are going well, some parts of our portfolio outshine like they are this year. So I feel comfortable that we're going to do better than our historical, maybe not as aggressive as this year, but pretty close to it.

**Noah Poponak** (Analysts):
Okay. And then I also wanted to ask about the margin in that segment. When it was under some pressure, you would project when you expected it to be back to the level it's at now. I guess now that it's here, and it maybe has growth ahead of it, but also pieces moving around under the hood. Is there a framework for how to think about the 3 to 5 year out or just the longer-term profitability potential of Digital Imaging?

**Robert Mehrabian** (Executives):
Yes. In Digital Imaging, obviously, we've enjoyed significant margin improvement this year over last year. By the end of the year, we expect the total margin to go up 225 basis points. Our target for every year across our portfolio is at least 50 basis points. This year, we're going to enjoy closer to 90 basis points. And that improvement really we just announced this quarter. Last quarter, we were closer to 50 -- 55. So I think our target is to stay on that 50 and do what we can year-over-year to improve our margins. And that goes to the heart of what George talked about. When necessary, cut costs. When things improve, don't put it back.

**Noah Poponak** (Analysts):
Okay. One last one. Just what's the implied fourth quarter total company organic revenue growth that's embedded in your revised guidance? I realize you raised the bottom line considerably, but it seems like it would require organic growth that maybe looks a little conservative, given you still have the easy compares.

**Robert Mehrabian** (Executives):
Yes, I think 7% to 8% is the number we have in mind at the present time. It may be a little higher, but 7% to 8% for Q4. As we get into Q4, which we are now, things are looking pretty well. We just have to execute. Execution, as you well know, is everything in our portfolio. So 8% is a good number.

**Operator** (Operator):
The next question is from the line of Robert Jamieson with Needham & Company.

**Robert Jamieson** (Analysts):
Just back on the 4Q guide as well, just with everything and the positive commentary around order books and book-to-bills. And then just looking historically, I got to go back to like 2015, 2016 to see sequentially when EPS was kind of like similar in 3Q to 4Q. So just wondering what's kind of embedded in your outlook and any puts and takes in the broader macro that you're considering that might be just keeping you a little bit more cautious here on your guidance?

**Robert Mehrabian** (Executives):
Yes. I think if you kind of look back at those years, and by the way, we do all the time, what happened is in -- by the end of fourth quarter of 2025 (sic) [ 2015 ], we started seeing some tax benefits, which, by the way, we're not enjoying today. So we're very hard at work, making sure that we get those tax credits, but they play an important role, obviously, especially if we can move the IRS to do what it's supposed to do, make decisions. If we can do that, we might enjoy some tax benefits on top of everything else.
But if you look back at what we call coming out of the hard years, simply what happened is we cut costs, as I mentioned before, George did, let's say, in marine and other domains. But when markets turned up, we didn't put all that cost back. We had very good discipline. If we can do that again, that would sustain us for a while and our EPS will grow just like it did subsequent to the tough years that we had in the mid-2015 and 2016. So that's the best I can do in my answers. George, do you have anything you want to add?

**George Bobb** (Executives):
No.

**Robert Mehrabian** (Executives):
No, I guess not.

**Robert Jamieson** (Analysts):
No. That's helpful. And then just can you update us on the unmanned outlook? Just how much you expect to generate just on dollar growth for this year? I know you guys kind of bumped that up the last couple of quarters. So just curious where that stands today.

**Robert Mehrabian** (Executives):
Yes. Broadly, 15% year-over-year. 25% to 26%, just on unmanned. If you put everything else in, with space, electronic warfare, missiles and of course, underwater, if you do all of that, it's still double digits. It's 11.3%, 11.5%. So while unmanned is doing really great, everything else in the portfolio seems to be moving up in double digits in that domain.

**Operator** (Operator):
The next question is from the line of John Godyn with Citigroup.

**Bradley Eyster** (Analysts):
This is Bradley Eyster on for John Godyn. So I just want to follow up on Noah's question about the growth trajectory for Digital Imaging. I mean, 2Q, 3Q have been strong. But I'm just trying to think for the potential outlook here, given that you called programs such as space sensors, missile detection. These programs still seem to be in their infancy. So I'm just trying to think what the size and shape of this segment looks like over the fullness of time. Any color you can give here would be appreciated.

**Robert Mehrabian** (Executives):
Let me just say, right now, from where we sit, George and I, we're looking at mid-single digits, maybe a little higher than that, 5% to 8%. It's too early right now. Right now, we're working on 2027, and I've never been one to project beyond the year. I know some people would tell you, 3 to 5 years, everything is going to be great, but that's not us because we don't see that far into the future.
But I think single digits on the high side, we'd be comfortable with that. And as we execute and as we compete with new programs, with things like our new drones, loitering drones that are armed, with our new nano drones that you can release 3 of them simultaneously from a single platform and recover them, with our ability to have an environment where all of our drones, whether it's ground-based or air, talk to one another, I think we feel comfortable with the, let's say, higher single-digit growth.

**Operator** (Operator):
The next question is from the line of Joe Giordano with TD Cowen.

**Joseph Giordano** (Analysts):
Just wanted to clarify something I may have heard wrong. Robert, I thought you said for DI for the year, you were thinking like 8-point-something percent. Is that a fourth quarter number? Or is that a full year number? Because if it's a full year number, I'm guessing it's not, then it would mean like fourth quarter organic is barely up. I just wanted to clarify that.

**Robert Mehrabian** (Executives):
Yes. I think, for the year, it's higher than that. It's -- organic is 10%. With 0.6% of acquisition, it's 10.6%, closer to 11%. So if I said that, I may have misspoken. We're talking about the revenue for Digital Imaging around $3.5 billion.

**Joseph Giordano** (Analysts):
That makes much more sense.

**Operator** (Operator):
Thank you. At this time, we've reached the end of our question-and-answer session. And I'll hand the floor back to management for any closing comments.

**Robert Mehrabian** (Executives):
Thank you, Rob. I will now ask Jason to conclude our conference call.

**Jason VanWees** (Executives):
Thanks, Robert. And again, thank you, Rob, for hosting the call. And if any of you have follow-up questions, please feel free to call me at the number in the earnings release or you have my e-mail. So thanks, everyone. Bye.

**Operator** (Operator):
This will conclude today's conference. You may disconnect your lines at this time. We thank you for your participation. Have a wonderful day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TDY_Q2_2026_Earnings_Call_20260722.md
- 2026-07-22｜Robert Mehrabian｜guidance：全年非 GAAP EPS 展望上調 $0.55（中點）（原話："raising our full year non-GAAP earnings outlook by $0.55"）
- 2026-07-22｜Robert Mehrabian｜guidance：全年營收預期比 4 月預測多約 1.2 億美元（原話："$120 million greater than our forecast in April"）
- 2026-07-22｜CFO｜guidance：CFO 給出全年非 GAAP EPS 區間 24.45–24.65（原話："in the range of $24.45 to $24.65"）
- 2026-07-22｜CFO｜guidance：CFO 給出 Q3 非 GAAP EPS 區間上緣 6.15（下緣 6.05）（原話："$6.05 to $6.15"）
- 2026-07-22｜Robert Mehrabian｜guidance：短週期業務原預測持平至低個位數成長（4 月說法）（原話："forecast flat to low single-digit growth"）
- 2026-07-22｜Robert Mehrabian｜guidance：全年國防銷售預期高個位數成長（原話："2026 defense sales should increase at the high single-digit"）
- 2026-07-22｜Robert Mehrabian｜guidance：Digital Imaging 全年成長預期 7.5%（原話："We're right now thinking about 7.5% for the year"）
- 2026-07-22｜Robert Mehrabian｜guidance：太空業務年底規模預估 4 億至 4.5 億美元（原話："over $400 million, maybe $450 million"）
- 2026-07-22｜Robert Mehrabian｜guidance：無人系統今年營收預估約 5.75 億美元（原話："more like $575 million"）
- 2026-07-22｜George Bobb｜guidance：測試量測全年成長預期約 3%（原話："the full year is perhaps kind of around 3% overall"）
- 2026-07-22｜George Bobb｜guidance：醫療（X 光偵測器）全年仍預期低個位數成長（原話："low single-digit growth for the full year at this point"）
- 2026-07-22｜George Bobb｜guidance：工業與科學視覺全年預期約 5% 成長（原話："a solid mid-single-digit growth on the order of 5%"）
- 2026-07-22｜Robert Mehrabian｜guidance：管理層稱 Q4 面臨 Digital Imaging 去年同期基期較高（原話："have a little tough comps with last year's Q4"）
- 2026-07-22｜Robert Mehrabian｜guidance：管理層提到各業務可能有 3,000 萬至 4,000 萬美元上行空間（原話："$40 million in various businesses. We're counting on it."）
- 2026-07-22｜Robert Mehrabian｜margin：全年利潤率預期改善 56 bps，未隨營收上調而調整（原話："2026 versus 2025 of 56 basis points"）
- 2026-07-22｜Robert Mehrabian｜margin：管理層對全年利潤率維持與先前預測相同（原話："We think the margins will stay the same as"）
- 2026-07-22｜George Bobb｜margin：Q2 關稅淨利益（扣除其他一次性項目）約 1,000 萬美元，主要在 Digital Imaging（原話："tariff benefit, net of some other onetime items"）
- 2026-07-22｜George Bobb｜margin：關稅貢獻 Digital Imaging 353 bps 利潤率改善中的約 120 bps（原話："the tariffs contributed a little more than 100 basis points"）
- 2026-07-22｜George Bobb｜margin：Instrumentation 利潤率下降歸因於產品組合（原話："quarter decreased primarily due to product mix."）
- 2026-07-22｜George Bobb｜margin：Digital Imaging 利潤率受關稅退款支撐，但被 R&D、庫存準備金等增加抵銷（原話："While tariff refunds contributed to the strong margin, the"）
- 2026-07-22｜Robert Mehrabian｜customer：Q2 book-to-bill 1.23，Digital Imaging 更高（原話："Overall, our book-to-bill was 1.23, led by Digital Imaging"）
- 2026-07-22｜Robert Mehrabian｜customer：訂單連續第 11 季超過銷售（原話："exceeded sales for the 11th consecutive quarter"）
- 2026-07-22｜Robert Mehrabian｜customer：飛彈與彈藥相關營收年化約 2–2.5 億美元（原話："and $250 million of our revenue on a run rate basis"）
- 2026-07-22｜Robert Mehrabian｜customer：國防占公司銷售約 30%–35%（原話："about 30% to 35% of the company's sales that go into defense"）
- 2026-07-22｜Robert Mehrabian｜customer：政府對製造擴產提供逾 3,000 萬美元承諾（原話："we had over $30 million commitment to increase"）
- 2026-07-22｜Robert Mehrabian｜customer：稱為 Golden Dome 幾乎所有參與者的主要供應商（原話："the primary supplier to just about everybody in the Golden"）
- 2026-07-22｜Robert Mehrabian｜product：Black Hornet 4 奈米無人機已在銷售（原話："Black Hornet 4, which is now being sold, is very successful"）
- 2026-07-22｜Robert Mehrabian｜product：Qioptiq 第二季有機成長 20%（原話："It's grown 20% organically in Q2"）
- 2026-07-22｜George Bobb｜product：Protocol 業務上半年偏慢，管理層對下半年回升表示樂觀（原話："I'm kind of optimistic that in the second half"）
- 2026-07-22｜Robert Mehrabian｜risk：逾 10 億美元營收依賴鍺供應與稀土磁鐵（原話："germanium supply and rare earth magnets"）
- 2026-07-22｜Robert Mehrabian｜risk：油價波動列為保守原因之一（原話："the oil prices keep jumping up and down"）
- 2026-07-22｜Robert Mehrabian｜risk：生命科學相關業務相對持平（原話："life science businesses that we're in are relatively flat"）
- 2026-07-22｜Robert Mehrabian｜risk：Q2 季末提前出貨影響很小（原話："I would say a little bit of pull-in, very little."）
- 2026-07-22｜Robert Mehrabian｜capital_allocation：淨槓桿 1.1 倍（原話："net leverage was 1.1"）
- 2026-07-22｜Robert Mehrabian｜capital_allocation：有 12 億美元未動用信貸額度（原話："We have a $1.2 billion of untouched credit"）
- 2026-07-22｜Robert Mehrabian｜capital_allocation：管理層不願以市場上過高價格併購（原話："pay some of the crazy prices that we see out there"）
- 2026-07-22｜George Bobb｜capital_allocation：今年 CapEx 較去年增加約 30%（原話："investing more CapEx this year than we did last year"）
- 2026-07-22｜CFO｜capital_allocation：CFO 報告第二季自由現金流（原話："less capital expenditures, was $284.7 million"）
- 2026-07-22｜Robert Mehrabian｜commitment：管理層表示將繼續透過收購複利成長獲利與現金流（原話："compound earnings and cash flow through acquisitions"）
- 2026-07-22｜Robert Mehrabian｜commitment：管理層說明槓桿為六年最低，有彈性部署資本（原話："leverage at its lowest level in 6 years"）

### TDY_Shareholder_Analyst_Call_Teledyne_Technologies_Incorporated_20260422.md
- 2026-04-22｜Melanie Cibik｜capital_allocation：股東會通過修訂重述的2014年激勵獎勵計畫（治理／薪酬事項，非資本配置數字），贊成逾93%（原話："over 93% of the shares present in person or by proxy"）
- 2026-04-22｜Melanie Cibik｜risk：股東獲得召集特別股東會之權利的章程修正案通過，贊成逾87%流通股（治理事項）（原話："Over 87% of the outstanding shares have been voted in favor"）
- 2026-04-22｜Robert Mehrabian｜commitment：主席表示股東提問將於會後回覆，會中無業務或財測討論（原話："We will answer questions submitted by you after the meeting."）

### 問答異常語氣（迴避／改口／保留）
- TDY_Q2_2026_Earnings_Call_20260722.md｜問：TD Cowen（Giordano）：Q4 即使取全年高端也幾乎沒有年增，是否過於保守？｜答法：先以玩笑回應「你要我少保守一點」，再列 Q4 基期、供應鏈（鍺／稀土）、油價與新關稅等保守理由，未直接給 Q4 隱含數字；僅稱可能有 3,000–4,000 萬美元上行
- TDY_Q2_2026_Earnings_Call_20260722.md｜問：UBS：訂單中短期出貨與多年期各占多少？對明年有何初步框架？｜答法：答稱手邊沒有短期／多年期拆分數字，交由 IR 事後提供；未回應明年框架
- TDY_Q2_2026_Earnings_Call_20260722.md｜問：BNP Paribas：槓桿低且本季回購不積極，管線與偏好產業為何？｜答法：回答槓桿、信貸額度與併購活躍度，未回應回購問題，也未點名偏好或不碰的產業

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
{"date":"20260723","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"國防順風持續 + backlog 轉收入（FLIR Defense／無人機／太空紅外／反無人機）","columns":{"2Y 驗證點":"b:b &gt;1.0、A&D 高個位數~雙位數成長","5Y 驗證點":"國防營收年化持續成長，無人機 $575M→規模化、太空 &gt;$450M","10Y 驗證點":"FLIR 成西方戰術 ISR 與太空紅外偵測器標準供應商","具體數字門檻":"Q2'26 backlog $5.0B、b:b 1.23（11 季連 &gt;1.0）、太空 $400-450M、無人機 $575M（+12-15%）","信息來源":"公司法說 + 美國國防預算立法","漂移觸發":"b:b 連 2 季 &lt;1.0 → 削弱"}},{"id":"H2","text":"紀律 M&A 複利持續（ROIIC ≥ WACC）","columns":{"2Y 驗證點":"每年 bolt-on，無過價大案","5Y 驗證點":"累計 M&A ROIIC &gt; WACC，整合無減損","10Y 驗證點":"25 年複利機器持續，無價值毀滅大案","具體數字門檻":"FCF ~$1.1B、槓桿 1.1x（6 年最低）、$4B 火力已備；近 2 年 &gt;$1B 併購（DD-Scientific $53M、Excelitas/Qioptiq $710M、Micropac $51M）","信息來源":"公司資本配置揭露 + 10-K","漂移觸發":"大型 M&A ROIIC &lt; WACC，或商譽減損 → 削弱"}},{"id":"H3","text":"估值維持 quality-industrial 溢價（本份核心：等估值修正）","columns":{"2Y 驗證點":"Non-GAAP Fwd PE 維持 22-26x","5Y 驗證點":"倍數正常化但不崩（PE &gt;20x）","10Y 驗證點":"EPS 複利 + 倍數企穩，5Y IRR 為正","具體數字門檻":"現 Fwd PE FY26 26.5x／FY27 24.9x vs 同業（AME/FTV/ROP/KEYS）；GF Value $491（−31% 高估）","信息來源":"同業估值 + GuruFocus","漂移觸發":"PE 跌破 18x（週期/預算衝擊）→ Bear；或現價不動＝預期報酬持續被估值壓"}}],"extra_text":"假設 | 24 天前判定 | 本次判定 | 短窗漂移 | vs Inception 累積漂移 | 結論\nH1 國防順風 | 🟢 兌現（backlog $4.6B、b:b 1.16） | 🟢 兌現++（backlog $5.0B、b:b 1.23，太空/無人機加速） | 強化（Q2 創高證實） | 強化（Inception 以來能見度上台階） | 持續\nH2 紀律 M&A | 🟢 兌現（bolt-on 節奏、無過價） | 🟢 兌現（槓桿 6 年最低、$4B 火力、明確拒絕過價 30-33%） | 持平偏強（火力再備但飛輪未點火） | 持平 | 持續\nH3 估值 | 🟡 削弱（$635、Fwd PE 24-26x 近高、5Y IRR 3.7%） | 🟡 削弱（$650 更滿、Fwd PE ~26x、5Y IRR ~5%） | 削弱（股價 +2.4% 使估值更滿） | 削弱（等估值的理由未變、若有更強） | 警戒（binding constraint）"},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"國防預算 CR 凍結/sequestration + 工業短週期二次下行（backlog 轉收入延遲、margin 壓力）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"b:b、organic growth、國防預算進度","警戒閾值":"b:b 連 2 季 &lt;1.0 或 organic 連 2 季 &lt;3%"}},{"id":"R2","text":"紀律 M&A 破壞：牛市追高一筆大案，capital deployment ROIC &lt; WACC（火力 $4B 已備＝雙面刃）","columns":{"對應假設":"H2","時間尺度":"🐢 長期慢變數（但單一事件可觸發）","監測指標":"大型 M&A 出價倍數、首年稀釋、ROIIC","警戒閾值":"EV/EBITDA &gt;20x 且 ROIIC &lt; WACC"}},{"id":"R3","text":"估值正常化：付滿水位倍數 → 從 ~26x 壓至 18-20x（即使 EPS 兌現，報酬平）","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Non-GAAP Fwd PE 分位、同業倍數","警戒閾值":"EPS 達標但 PE &lt;20x（成長對、報酬平）"}},{"id":"R4（新增本份）","text":"鍺／稀土磁材供應中斷：&gt;$1B 營收曝險，中國管制加嚴致交付延遲或替代成本上升","columns":{"對應假設":"H1（margin/交付）","時間尺度":"⚡🔥 短-中期（政策事件驅動）","監測指標":"季度 GM、原料替代進度、2026-11 停火到期","警戒閾值":"季度 GM 因原料受壓 &gt;1pp，或關鍵料源中斷"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE≤21-22x（約 $540-570）或國防+無人機+太空營收能見度再上台階；月度追蹤估值分位","irr_base_pct":5.1,"ev5y_pct":20.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.8,"ev5y_pct":20.0,"irr_base_pct":5.1,"max_dd_pct":-45.0,"bull_5y_price":1105.0,"bear_5y_price":436.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE≤21-22x（約 $540-570）或國防+無人機+太空營收能見度再上台階；月度追蹤估值分位","price_at_dd":650.5,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TDY_20261022/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
