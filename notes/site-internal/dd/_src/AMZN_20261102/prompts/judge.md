你是 stock-analyst **v20 判斷 agent**，標的 AMZN（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"AMZN","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMZN_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMZN_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":201.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿（SEC 8-K Ex.99.1）"},"note":"未取得 Q3 營收共識數字；AP 報導稱營收與獲利低於分析師預期"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income","value":null,"period":"Q3 FY2026","unit":"n/a","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026","citation":"Amazon 不公布 non-GAAP 營業利益，以 GAAP 為準，見下一項"},"note":"n/a","needs_sonnet":true},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":28.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD bn（利益率 13.9%，公司稱歷史最高）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿（SEC 8-K Ex.99.1）；28,076 百萬"},"note":"未取得數字；AP 稱低於預期"},{"id":"f_kpi3_free_cash_flow_ttm_ttm","label":"Free cash flow（TTM，公司僅報 TTM）","value":-42.4,"period":"TTM 至 Q3 FY2026（公告於 2026-10-29）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"TTM 至 Q3 FY2026（公告於 2026-10-29）","citation":"公司新聞稿（SEC 8-K Ex.99.1）；OCF TTM 168.3bn +29%"},"note":"n/a"},{"id":"f_kpi5_guidance_q4_fy2026","label":"Guidance：Q4 FY2026","value":"營收 240.0–247.0bn（YoY +12%～+16%）；營業利益 28.5–33.5bn","period":"Q3 FY2026 公告（2026-10-29）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026 公告（2026-10-29）","citation":"公司新聞稿（SEC 8-K Ex.99.1）；全年現金資本支出約 220bn（重申）"},"note":"營收共識約 244.2bn（來源：AP 報導，經 web_search）；營收指引中點 243.5bn 略低於共識；財報後盤後股價跌逾 6%（AP）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_amzn_gross_margin_pct","label":"AMZN 毛利率","value":50.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_operating_margin_pct","label":"AMZN 營業利益率","value":12.36,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_fcf_margin_pct","label":"AMZN FCF 利潤率","value":-0.82,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wmt_gross_margin_pct","label":"WMT 毛利率","value":25.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMT.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wmt_operating_margin_pct","label":"WMT 營業利益率","value":4.39,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMT.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wmt_fcf_margin_pct","label":"WMT FCF 利潤率","value":1.84,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMT.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_shop_gross_margin_pct","label":"SHOP 毛利率","value":47.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SHOP.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_shop_operating_margin_pct","label":"SHOP 營業利益率","value":17.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SHOP.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_shop_fcf_margin_pct","label":"SHOP FCF 利潤率","value":17.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SHOP.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_msft_gross_margin_pct","label":"MSFT 毛利率","value":67.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_operating_margin_pct","label":"MSFT 營業利益率","value":47.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_fcf_margin_pct","label":"MSFT FCF 利潤率","value":17.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_gross_margin_pct","label":"GOOGL 毛利率","value":60.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_operating_margin_pct","label":"GOOGL 營業利益率","value":33.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_fcf_margin_pct","label":"GOOGL FCF 利潤率","value":4.19,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc","label":"SBC 占營業利益","value":19.3,"period":"Q3 FY2026（SBC 5.406bn ÷ 營業利益 28.076bn，自算；SBC 占營收 2.7%）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（SBC 5.406bn ÷ 營業利益 28.076bn，自算；SBC 占營收 2.7%）","citation":"公司新聞稿現金流量表（SEC 8-K Ex.99.1）"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":240.35,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-10.4,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":38.26,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":39.52,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.21 → 12.85）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":1.05,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.45 → 10.56）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.75,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.42 → 13.52）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":12.85,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":10.56,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":13.52,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":47.19,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 8.73 → 12.85（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":19.43,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.26,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝75.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":75.2,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.46,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝80.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":80.1,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":18.7,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 12.85，分子＝快照價 240.35","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":157723.0,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 271949.0、現金 114226.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":10813.14,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":2756660.82,"period":"2026-11-02","unit":"USD m","basis":"市值 2598937.82 ＋ 淨負債 157723.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":828995.22,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（47 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":949994.17,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（59 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.33,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 240.35 / W52 241.03 / W104 227.87 / W250 176.52 / W250 13週斜率 0.77%"},{"id":"f_ma_w52","label":"52 週均線","value":241.03,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":227.87,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":176.52,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.77,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：新進入者且資金充沛的競爭者持續增加，AI 與網路降低進入門檻，使新興／較小業者更易與 Amazon 競爭，Amazon 可能失去業務或被迫降價。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm","excerpt":"Competition continues to intensify, including with the development of new business models and the entry of new and well-funded competitors, and as our competitors enter into business combinations or alliances and established companies in other market segments expand to become competitive with our business.","as_of":"2026-02-06","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"聚合站估計：Amazon 美國線上零售份額約 38%（2025 為 40%），Walmart 升至第二；來源為低品質彙整，數字粗略。","source":"designrush／countly 等聚合站（搜尋摘要）","url":"https://countly.net/largest-ecommerce-websites-usa-2026-top-10-by-revenue","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Synergy Research：全球雲基礎設施份額 AWS 2025Q3 29%→2026Q1 28%，Azure 20%→21%，Google 13%→14%；AWS 緩慢流失份額（經搜尋摘要轉述，未核 Synergy 原文）。","source":"Synergy Research Group 經 technologychecker／tech-insider 轉述","url":"https://tech-insider.org/cloud-market-share-aws-azure-google-cloud-q3-2026-growth-gap-2026/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Q1 2026 財報電話會議：管理層稱 AWS backlog 分布均衡，未集中於一兩家客戶","source":"Amazon Q1 Earnings Call Transcript: Backlog Evenly Distributed Across Multiple Clients (iTiger)","url":"https://www.itiger.com/news/1154837130","excerpt":"Andy Jassy: Regarding the backlog, it stood at $364 billion in Q1, excluding the recently announced multi-hundred-billion-dollar agreement with Anthropic. The backlog is well-balanced and not concentrated with just one or two clients;","as_of":"2026-05-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Jassy 稱 AWS AI 算力 2027 年前持續受限，2026 產能已全數認購、2027 近乎售罄、2028 已有相當部分預鎖；電力是核心瓶頸，預計 2027 年底電力容量較 2025 翻倍。","source":"datacenterknowledge.com / latestly.com 等報導 Amazon Q3 2026 財報電話會","url":"https://datacenterknowledge.com/infrastructure/amazon-lifts-ai-infrastructure-spending-to-220b-as-demand-outpaces-capacity","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q3 2026：AWS 營收年增 39% 至 $46.0B；backlog $578B（三位數年增）；Jassy 預期 AWS 2027、2028 成長逾 40%；2026 capex 約 $220B，2027 將『meaningfully more』；市場視 capex 與 backlog 轉換為核心張力。","source":"Amazon Q3 2026 earnings call 報導（aiweekly.co、singjupost）","url":"https://aiweekly.co/alerts/amazons-aws-growth-hits-39-in-q3-as-capex-guide-jolts-stock","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H","valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"零售端：Forrester 2024 預測全球線上零售 2028 年達 $6.8T、年複合 8.9%；eMarketer 預期美國零售電商 2027 達 $1.72T；均為較舊預測，非 2026 共識。","source":"Forrester press release 2024-05-30","url":"https://www.forrester.com/press-newsroom/global-online-retail-sales-to-grow-to-6-8-trillion-by-2028","excerpt":null,"as_of":"2024-05-30","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Business Insider 報導（經搜尋摘要轉述）：Amazon 已收到 Nvidia 機櫃但場地未就緒，歸因電力短缺與施工延誤；另有文件顯示部分電商基礎設施因電力風險移出 Dublin。Amazon 未證實。","source":"cloudcomputing-news.net 轉述","url":"https://www.cloudcomputing-news.net/news/amazon-aws-workloads-power-constraints/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"AWS 容量 2027 近乎售罄","source":"latestly.com","url":"https://www.latestly.com/technology/amazon-ceo-andy-jassy-says-aws-capacity-sold-out-through-2027-7655371.html","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q3 2026 8-K 新聞稿","source":"SEC 8-K Ex 99.1","url":"https://www.sec.gov/Archives/edgar/data/0001018724/000101872426000038/amzn-20260930xex991.htm","excerpt":"Operating income was $28.1 billion and operating margin was 13.9%—Amazon’s highest operating margin ever AWS net sales increased 39.3%—its fastest growth in nearly five years—to a $184 billion annualized revenue run rate","as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因子載明公司正在訴訟多件指控價格操縱、壟斷及消費者保護的案件，含州檢察長與 FTC 提起者。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm","excerpt":"For example, we are litigating a number of matters alleging price fixing, monopolization, and consumer protection claims, including those brought by state attorneys general and the Federal Trade Commission.","as_of":"2026-02-06","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2025 年其他營業費用增至 46 億美元，主因 2025 Q3 與 FTC 的訴訟和解，另含義大利稅務爭議與資產減損。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm","excerpt":"The increase in 2025 was primarily related to the settlement of a lawsuit with the Federal Trade Commission (the “FTC”) in Q3 2025, and also included the resolution of tax disputes associated with our stores business in Italy, and physical stores and other asset impairments.","as_of":"2026-02-06","retrieved_at":"20261102","affects":["valuation","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"法官駁回 Amazon 延後 FTC 壟斷案審理的請求，審理維持 2027-03-29。","source":"MLex: Amazon's bid to delay US FTC monopolization trial rejected by judge","url":"https://www.mlex.com/mlex/articles/2536525","excerpt":"a trial in the US Federal Trade Commission's monopolization case against the company to June 2027. In an order, US District Judge John Chun wrote the he \"has been preparing for some time for the March 29, 2027, trial date in this matter.\" He said he did not \"see a good reason to disturb the current schedule.\"See attached order.","as_of":"2026-10-09","retrieved_at":"20261102","affects":["thesis.R","triggers","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K FY2025 風險因素：中國賣家占第三方賣家服務與廣告營收相當比重，中國供應商提供相當比重的零組件與成品，關稅政策變動與貿易爭端可能不利營運結果","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm","excerpt":"because China-based sellers account for significant portions of our third-party seller services and advertising revenues, and China-based suppliers provide significant portions of our components and finished goods, regulatory and trade restrictions, tariff policy changes and trade disputes, data protection and cybersecurity laws, economic factors, geopolitical events, security issues, or other factors negatively impacting China-based sellers and suppliers could adversely affect our operating results.","as_of":"2026-02-06","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K MD&A：全球關稅與貿易政策不可預測的變動對營運結果有難以預測與量化的影響，預期影響延續至2026Q1","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm","excerpt":"global economic and geopolitical developments, including unpredictable shifts in global tariff and trade policies, and the development and adoption of technologies and services, including artificial intelligence, have direct and indirect impacts on our results of operations that are difficult to predict, isolate, and quantify.","as_of":"2026-02-06","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"據轉述 Amazon 2025 年報的 PESTEL 分析：中國賣家對第三方賣家與廣告收入貢獻顯著，中國供應商提供零組件與成品；中美貿易限制或緊張可能對公司造成重大影響（二手分析，未核 10-K 原文）。","source":"thestrategystory.com PESTEL analysis of Amazon","url":"https://thestrategystory.com/blog/?p=25522","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Digitimes 報導 AWS 自研晶片 Trainium 3 的 AI 伺服器進入量產，台灣供應商參與散熱、組裝與滑軌。","source":"Digitimes","url":"https://www.digitimes.com/news/a20260623PD213.html","excerpt":null,"as_of":"2026-06-23","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 北美段營收年增 6% 至 $112.9B，營業利益 $8.7B（去年同期 $4.8B）；Prime Day 移至 Q2 壓低 Q3 零售增速，非同基期比較","source":"Amazon IR, Q3 2026 results","url":"https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Third-Quarter-Results/","excerpt":"North America segment sales increased 6% year-over-year to $112.9 billion.","as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 國際段營收年增 5% 至 $43.1B（不含匯率 +8%），營業利益 $1.6B（去年同期 $1.2B）","source":"Amazon IR, Q3 2026 results","url":"https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Third-Quarter-Results/","excerpt":"International segment sales increased 5% year-over-year to $43.1 billion, or increased 8% excluding changes in foreign exchange rates.","as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 AWS 營收年增 39% 至 $46.0B，營業利益 $17.8B（去年同期 $11.4B），近五年最快增速","source":"Amazon IR, Q3 2026 results","url":"https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Third-Quarter-Results/","excerpt":"AWS segment sales increased 39% year-over-year to $46.0 billion","as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H","moat_trend","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q4 2026 指引：淨銷售 $240.0–247.0B（年增 12–16%，匯率不利約 60bp）；營業利益 $28.5–33.5B；廣告預期年增高個位至十幾％（high teens）；2026 全年資本支出約 $220B","source":"Amazon 8-K Exhibit 99.1 FY2026 Q3 (SEC) / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001018724/000101872426000038/amzn-20260930xex991.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"eMarketer：2026 年亞馬遜佔美國市集型電商 63.3%（2022 見頂後下滑）；亞馬遜加沃爾瑪合計將佔美國零售電商逾半；二手來源稱亞馬遜佔美國零售電商約 40%","source":"eMarketer chart: Amazon's share of US marketplace ecommerce peaked 2022","url":"https://www.emarketer.com/chart/273567/amazons-share-of-us-marketplace-ecommerce-peaked-2022-will-slip-633-2026-billions-us-amazon-marketplace-sales-change-of-total-retail-marketplace-ecommerce-sales-2020-2027","excerpt":"Amazon's Share of US Marketplace Ecommerce Peaked in 2022 and Will Slip to 63.3% in 2026","as_of":"2025-10-01","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：公司在新技術（含自動化、AI、機器學習）的投資可能無法回收，失敗時投資價值可能被減記或沖銷。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm","excerpt":"Failure to realize the benefits of amounts we invest in new technologies, products, or services could result in the value of those investments being written down or written off.","as_of":"2026-02-06","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Forrester：OpenAI Instant Checkout 於 2026-03-04 停用，預期結帳經夥伴（含 Amazon）回流；Amazon 以 Alexa for Shopping 取代 Rufus，並封鎖外部 AI 代理爬蟲、起訴 Perplexity Comet。","source":"Forrester blog: Power Couple OpenAI + Amazon May Have Just Won Consumer Agentic Commerce","url":"https://www.forrester.com/blogs/power-couple-openai-amazon-may-have-just-won-consumer-agentic-commerce","excerpt":"Home > Featured Blogs > Power Couple OpenAI + Amazon May Have Just Won Consumer Agentic Commerce Power Couple OpenAI + Amazon May Have Just Won Consumer Agentic Commerce","as_of":"2026-03-17","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Amazon Trainium2 已成數十億美元業務；分析稱 Trainium 在 CUDA 生態成熟度落後、Google TPU 在規模效率上領先。","source":"TechCrunch: Andy Jassy says Amazon's Nvidia competitor chip is already a multi-billion dollar business","url":"https://techcrunch.com/2025/12/03/andy-jassy-says-amazons-nvidia-competitor-chip-is-already-a-multi-billion-dollar-business","excerpt":"As expected, the company revealed at the AWS re:Invent conference the next generation of its Nvidia-competitor AI chip, Trainium3, which is 4x faster yet uses less power than the current Trainium2.","as_of":"2025-12-03","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 列示競爭者包含搜尋引擎、比價網站、社群、虛擬助理等線上與 app 發現商品的管道，含透過人工智慧者；行銷成本隨流量來源競爭與通路組合變動。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm","excerpt":"web search engines, comparison shopping websites, social networks, web portals, virtual assistants, and other online and app-based means of discovering, using, or acquiring goods and services, either directly or in collaboration with other retailers, including through artificial intelligence","as_of":"2026-02-06","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"第三方賣家占付費銷量比重降至 60%（2024 Q4 為 62%），自營零售單位量成長快於第三方，第三方絕對量仍增加。","source":"Canopy Management 分析 Amazon Q1 2026 財報","url":"https://canopymanagement.com/?p=23580","excerpt":"third-party seller share of paid units dropped to 60%, down from 62% in Q4 2024","as_of":"2026-05-01","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"廣告服務營收 2026 Q1 為 172 億美元、年增 24%；2025 全年廣告營收 686 億美元。","source":"Canopy Management；PPC Land","url":"https://canopymanagement.com/?p=23580","excerpt":"advertising services revenue grew 24% year over year to $17.2 billion for the quarter","as_of":"2026-05-01","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Amazon 於 2026 年 5 月將 Rufus 併入並更名 Alexa for Shopping，整合進搜尋列與廣告變現體系；Q2 2026 財報電話會議稱其活躍用戶年增近一倍（搜尋摘要轉述，未取得原文）。","source":"WebSearch 摘要彙整（Modern Retail／Retail Dive／Forrester 等）","url":"https://retaildive.com/news/amazon-alexa-for-shopping-agentic-ai-adoption/826806/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 共識目標價均值 $323.26（59 位分析師），最高 $400、最低 $218，as-of 2026-09-04（Q3 財報前，非財報後）","source":"MarketBeat AMZN Forecast","url":"https://www.marketbeat.com/stocks/NASDAQ/AMZN/Forecast/","excerpt":null,"as_of":"2026-09-04","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"各聚合站目標價均值不一：Investing.com $319.90（2026-07-31）、tickflow $307.77（93 位分析師，2026-08-01）；個別目標價 Morgan Stanley $350（2026-10-19）、Wells Fargo $329（2026-10-12）","source":"tickflow.io AMZN forecast；搜尋摘要所列 Morgan Stanley / Wells Fargo 目標價","url":"https://tickflow.io/stock/AMZN/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司 Q3 2026 財報給 Q4 營業利益 guidance $28.5–33.5 億的區間（原文單位為十億美元：$28.5B–$33.5B，去年同期 $25.0B）；Q3 營業利益 $28.1B、營業利益率 13.9%；本次搜尋未找到 Q4 營業利益的市場共識數字，無法比較落差","source":"Amazon, Q3 2026 earnings report (aboutamazon.com)","url":"https://aboutamazon.com/news/company-news/amazon-earnings-q3-2026-report","excerpt":"Operating income was $28.1 billion and operating margin was 13.9%—Amazon’s highest operating margin ever","as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-04-13 簽署併購協議，以約 116 億美元收購衛星業者 Globalstar（現金每股 90 美元或 0.32 股 AMZN 股票，股票價值設上限），預計 2027 年完成，待監管核准。","source":"Bloomberg Law｜Amazon to Buy Satellite Company Globalstar for $11.6 Billion","url":"https://news.bloomberglaw.com/tech-and-telecom-law/amazon-to-buy-satellite-operator-globalstar-for-90-a-share","excerpt":"Amazon to Buy Satellite Company Globalstar for $11.6 Billion (3)","as_of":"2026-04-14","retrieved_at":"20261102","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"10-K FY2025：2020 年 3 月起私人原告、州檢察長與 FTC 在美、加、英提起反壟斷／消費者保護訴訟，求償數十億美元，仍在進行。","source":"SEC EDGAR 10-K FY2025 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm","excerpt":"Since March 2020, private litigants, state Attorneys General, and the Federal Trade Commission have filed cases in the U.S., Canada, and the United Kingdom alleging, among other things: price fixing arrangements between each of Amazon and its vendors and Amazon and its third-party sellers; abuse of dominance, monopolization, and attempted monopolization","as_of":"2026-02-06","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"Q4 2025 認列 24 億美元費用，其中 11 億美元為義大利稅務爭議和解與一項訴訟和解。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm","excerpt":"Of this total, $1.1 billion related to the resolution of tax disputes associated with our stores business in Italy, and the settlement of a lawsuit, recorded primarily in “Other operating expense (income), net” and “Fulfillment,” and primarily impacted our International segment.","as_of":"2026-02-06","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"FDA 於 2026-06-17 對 Amazon 發出警告信，指 FBA 銷售的三項產品屬未核准新藥。","source":"gmp-compliance.org｜FDA Warning Letter to Amazon: Unapproved New Drugs Sold via Online Marketplace","url":"https://gdp.gmp-compliance.org/about-gdp/news/news-details/fda-warning-letter-to-amazon-unapproved-new-drugs-sold-via-online-marketplace.html","excerpt":"FDA Warning Letter to Amazon: Unapproved New Drugs Sold via Online Marketplace","as_of":"2026-06-23","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"-","claim":"2026 年 CPSC 公告多起平台第三方賣家商品召回（如 ATOYUS 兒童玩具方塊），CPSC 頁面標示銷售於 Amazon。","source":"CPSC 2026 recalls","url":"https://www.cpsc.gov/Recalls/2026/ATOYUS-Childrens-Activity-Cubes-Recalled-Due-to-Risk-of-Serious-Injury-or-Death-from-Choking-Hazard-Violate-Small-Parts-Ban-and-Mandatory-Standard-for-Toys-Sold-on-Amazon-by-Melofaver-US","excerpt":"ATOYUS Childrens Activity Cubes Recalled Due to Risk of Serious Injury or Death from Choking Hazard Violate Small Parts Ban and Mandatory Standard for Toys Sold on Amazon by Melofaver US","as_of":"2026-03-01","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-04-13 簽署併購協議，以約 116 億美元收購 Globalstar，預計 2027 年完成，待監管核准。","source":"Bloomberg Law｜Amazon to Buy Satellite Company Globalstar for $11.6 Billion","url":"https://news.bloomberglaw.com/tech-and-telecom-law/amazon-to-buy-satellite-operator-globalstar-for-90-a-share","excerpt":"Amazon to Buy Satellite Company Globalstar for $11.6 Billion (3)","as_of":"2026-04-14","retrieved_at":"20261102","affects":["valuation","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"10-K FY2025：多起美加英反壟斷／消費者保護訴訟（含 FTC、州檢察長、私人集體訴訟）仍在進行，求償數十億美元。","source":"SEC EDGAR 10-K FY2025 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm","excerpt":"These complaints seek billions of dollars of alleged damages, treble damages, punitive damages, injunctive relief, structural relief, civil penalties, attorneys’ fees, and costs.","as_of":"2026-02-06","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Q4 2025 認列與訴訟和解及義大利稅務爭議相關費用 11 億美元。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm","excerpt":"Of this total, $1.1 billion related to the resolution of tax disputes associated with our stores business in Italy, and the settlement of a lawsuit","as_of":"2026-02-06","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"FDA 於 2026-06-17 對 Amazon 發出警告信，指 FBA 銷售的三項產品屬未核准新藥。","source":"gmp-compliance.org｜FDA Warning Letter to Amazon","url":"https://gdp.gmp-compliance.org/about-gdp/news/news-details/fda-warning-letter-to-amazon-unapproved-new-drugs-sold-via-online-marketplace.html","excerpt":"FDA Warning Letter to Amazon: Unapproved New Drugs Sold via Online Marketplace","as_of":"2026-06-23","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"product_recall_warning#1","axis":"product_recall_warning","section":"events","direction":"-","claim":"2026 年 CPSC 公告多起銷售於 Amazon 的第三方賣家商品召回。","source":"CPSC 2026 recalls","url":"https://www.cpsc.gov/Recalls/2026/ATOYUS-Childrens-Activity-Cubes-Recalled-Due-to-Risk-of-Serious-Injury-or-Death-from-Choking-Hazard-Violate-Small-Parts-Ban-and-Mandatory-Standard-for-Toys-Sold-on-Amazon-by-Melofaver-US","excerpt":"ATOYUS Childrens Activity Cubes Recalled Due to Risk of Serious Injury or Death from Choking Hazard Violate Small Parts Ban and Mandatory Standard for Toys Sold on Amazon by Melofaver US","as_of":"2026-03-01","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"AMZN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.01,"operating_margin_pct":12.36,"fcf_margin_pct":-0.82,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"WMT","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.23,"operating_margin_pct":4.39,"fcf_margin_pct":1.84,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMT","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SHOP","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":47.77,"operating_margin_pct":17.81,"fcf_margin_pct":17.73,"rd_intensity_pct":12.41},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SHOP","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MSFT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.66,"operating_margin_pct":47.1,"fcf_margin_pct":17.31,"rd_intensity_pct":10.52},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"GOOGL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.86,"operating_margin_pct":33.32,"fcf_margin_pct":4.19,"rd_intensity_pct":15.81},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"AMZN"},"financial_history":{"ticker":"AMZN","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":513983000000.0,"revenue_yoy_pct":null,"gross_margin_pct":43.81,"operating_margin_pct":2.38,"net_income":-2722000000.0,"diluted_eps":-0.27,"free_cash_flow":-16893000000.0,"fcf_margin_pct":-3.29,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":574785000000.0,"revenue_yoy_pct":11.83,"gross_margin_pct":46.98,"operating_margin_pct":6.41,"net_income":30425000000.0,"diluted_eps":2.9,"free_cash_flow":32217000000.0,"fcf_margin_pct":5.61,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":637959000000.0,"revenue_yoy_pct":10.99,"gross_margin_pct":48.85,"operating_margin_pct":10.75,"net_income":59248000000.0,"diluted_eps":5.53,"free_cash_flow":32878000000.0,"fcf_margin_pct":5.15,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":716924000000.0,"revenue_yoy_pct":12.38,"gross_margin_pct":50.29,"operating_margin_pct":11.16,"net_income":77670000000.0,"diluted_eps":7.17,"free_cash_flow":7695000000.0,"fcf_margin_pct":1.07,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/AMZN/AMZN_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Amazon.com, Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Thank you for standing by. Good day, everyone, and welcome to the Amazon.com Q3 2026 Financial Results Teleconference.
[Operator Instructions]
Today's call is being recorded.
For opening remarks, I'll be turning the call over to the Vice President of Investor Relations, Mr. Dave Fildes. Thank you, sir. Please go ahead.

**Dave Fildes** (Executives):
Hello, and welcome to our Q3 2026 financial results conference call. Joining us today to answer your questions is Andy Jassy, our CEO; and Brian Olsavsky, our CFO. As you listen to today's conference call, we encourage you to have our press release in front of you, which includes our financial results as well as metrics and commentary on the quarter. Please note, unless otherwise stated, all comparisons in this call will be against our results for the comparable period of 2025.
Our comments and responses to your questions reflect management's views as of today, October 29, 2026, only and will include forward-looking statements. Actual results may differ materially. Additional information about factors that could potentially impact our financial results is included in today's press release and our filings with the SEC, including our most recent annual report on Form 10-K and subsequent filings.
During this call, we may discuss certain non-GAAP financial measures. In our press release, slides accompanying this webcast and our filings with the SEC, each of which is posted on our IR website, you will find additional disclosures regarding these non-GAAP measures, including reconciliations of these measures with comparable GAAP measures. Our guidance incorporates the order trends that we've seen to date and what we believe today to be appropriate assumptions. Our results are inherently unpredictable and may be materially affected by many factors, including fluctuations in foreign exchange rates and energy prices, changes in global economic and geopolitical conditions, tariff and trade policies, resource and supply volatility, including for memory chips and customer demand and spending, including the impact of recessionary fears, inflation, interest rates, regional labor market constraints, world events, the rate of growth of the Internet, online commerce cloud services and new and emerging technologies and the various factors detailed in our filings with the SEC.
Our guidance assumes, among other things, that we don't conclude any additional business acquisitions, restructurings or legal settlements. It's not possible to accurately predict demand for our goods and services, and therefore, our actual results could differ materially from our guidance.
And now I'll turn the call over to Andy.

**Andrew Jassy** (Executives):
Thanks, Dave. We're reporting $201.9 billion in revenue, up 12% year-over-year. Operating income was $28.1 billion, up 61% year-over-year. Q3 was another strong quarter for Amazon. In AWS, our plan is working. Despite lapping a comparable year-over-year period where we added a lot of capacity, AWS grew 39.3% year-over-year, accelerating for the sixth straight quarter, our fastest growth in nearly 5 years. Backlog is $578 billion, growing triple digits year-over-year and well diversified. 
We're installing an AI accelerator about every 14 seconds and almost as fast as we install capacity, customers are gobbling it up. Our core compute and storage revenue grew at their fastest rates in several years. Our operating margins have long been strong on our core offering, but rapidly improving on the AI side, too, well ahead of where they were on core at a similar time of evolution.
Even with heightened component costs like memory and significant depreciation from the CapEx we're investing. We continue to accelerate our CapEx payback and have even more conviction than we already had that the investment we're making in AWS will yield a much larger revenue and free cash flow generating business than we would have imagined a couple of years ago with strong return on invested capital.
We have a compelling flywheel spinning in AWS. Borrowing from Jim Collins' flywheel definition Good to Great, where if you do A, you almost can't help but do B and if you do B, you almost can't help but do C and so on.
In AWS, having the leading functionality, security and operational performance can't help but drive customers to run their apps and store their data in AWS, which can't help but drive AWS AI demand because customers prefer their production inference to be near the rest of their data and apps, which can't help but drive core AWS demand because AI uses core for work like reinforcement learning, posttraining and tool usage, which can't help but drive reinvestment back into our broader AWS functionality.
This is a different model than primarily hosting GPUs or renting short-term data center capacity. This is a long-term platform strategy that broadly helps customers invent and evolve their customer experiences, operate stably and build a reliable partnership they can grow for many years. And it also yields very attractive long-term economics for us regardless of supply scarcity.
There are many examples that illustrate our progress in AWS, but I'll share a few. On the core side, it's important to remember that the vast majority of global IT spend, about 85% is still on-premises, and we're in a 10- to 20-year cycle where that equation will flip to the cloud. Conventional wisdom has been that linchpin workloads like mainframes or storage array networks would never move to the cloud. But these workloads are moving as AWS has built unique cloud substitutes and AI-driven migration capabilities to make this transition much easier. And enterprises get the benefits of less CapEx, lower operating costs, faster innovation, better developer productivity and data accessibility to more easily leverage AI.
Our core business has attractive margins because we've learned to run it very efficiently over the last 20 years. As our core business grows, we keep reinvesting in our core AI functionality. For example, as customers generate increasingly more data and seek to get value from it in analytics and AI, the complexity of moving data between data stores and analytics engines is onerous and expensive. With our acquisition of DuckLabs, DuckDB will become the universal SQL dialect of AWS storage and analytics, simplifying data processing with a modern analytics engine that is fast, simple to use and ubiquitous and where customers will be able to write SQL queries once and then execute using any AWS analytics service.
For the first time in analytics, customers will have 0 migration or portability costs between query engines. This is a big deal. And you can imagine how it will also help agents do efficient querying as well.
On the AI side, we continue to expand the capabilities of our inference service, Amazon Bedrock, and it's leading to remarkable growth with Fortune 500 companies spending nearly 7x more on Bedrock year-over-year and total Bedrock token volume growing nearly 17x year-over-year. Bedrock is the fastest growing multibillion-dollar service in AWS' history. We recently added OpenAI models to Bedrock and usage is growing quickly. We also just added Bedrock managed versions of Kimi, GLM and SpaceX models.
You can't have a conversation about AI today without talking about security. It's another reason customers keep choosing Bedrock. We've designed Bedrock so customers' data remains secure and private. Inputs and outputs are never shared with model providers or used to train based models. When customers tune a foundation model, we create a private copy specifically for their use, and data is fully encrypted both in transit and at rest.
As frontier models get more powerful, they're surfacing software vulnerabilities previously not found and at unprecedented rates. We built AWS Continuum to discover, prioritize, validate and remediate code vulnerabilities and machine speed. It's already being used by customers like Capital One, IBM, Infor, Luminate and Robinhood. In Q3, we announced that we'll integrate it into the tools where code's being written, Anthropic's Claude Code, OpenAI's Codex, and AWS's Kiro. The interest from customers exceeds anything we've ever seen for a new security service.
Agents continue to be deployed at accelerating rates, many of which are being built on Bedrock AgentCore's building blocks. Tens of thousands of customers currently use AgentCore, deploying 2x more agents with it in Q3 than the prior 3 quarters combined. In addition to building their own purpose-built agents, most companies will also use turnkey agentic services, and we offer several that customers love. Kiro for coding, Amazon Connect for contact center agents and Amazon Transform for migration. They're all iterating quickly and picking up customer momentum. As is Amazon Quick, our intelligent AI work companion, which is growing very rapidly as large enterprises like Mondelez, EchoStar, 3M, Southwest Airlines and DXC are choosing Quick because it's purpose-built for work with no compromises on customer data.
Finally, our chips business continues to grow triple-digit percentages year-over-year and revenue commitments for Graviton and Trainium have each increased more than 20x year-over-year. AI continues to be a tailwind for Graviton because posttraining reinforcement learning and agent tool use is mostly done on CPUs versus AI accelerators, and Graviton is the strongest CPU chip, offering up to 30% to 40% better price performance than alternatives.
Customers using our custom silicon saved more than $2 billion in Q3 alone, and we just open-sourced TorchNeuron so developers can run existing PyTorch code, which most already use on Trainium without rewriting a thing. As we launch new generations of chips, demand for prior generations remained strong. After our launch of Graviton5, backlog for prior generation Graviton instances still more than doubled quarter-over-quarter. And short-term capacity for prior generation Trainium instances sell at a premium compared to the first half of the year.
With Trainium demand so strong, customers continue encouraging us to make it available outside of AWS. We intend to do so late in 2027. Overall demand for AWS capacity remains exceptionally strong. Enterprises are still very early in using inference at scale, and yet inference already accounts for well over half of AWS' AI revenue and growing. And we have a lot of training revenue as well. We still expect 2026 cash CapEx of approximately $220 billion, the majority for AWS and expect to spend meaningfully more in 2027. And with a clear line of sight to attractive financial returns, as I laid out on our last call.
AWS is a $184 billion annualized revenue run rate business, and yet the opportunity remains extraordinary. With our continued pace of innovation, new core and AI functionality, enterprises wanting to run their core and AI workloads in AWS and the amount of capacity that we're adding each year, we believe that AWS can grow north of 40% in each of 2027 and in 2028, and be a $1 trillion revenue business in the next 5 to 10 years. We're in the very early days of this inflection, our strategy is working, and I expect it will for the foreseeable future.
In stores, I think some folks are sleeping a bit on how much progress that business has made and what it's become in the last few years. I'm not aware of another retail business approaching Amazon's revenue size, hundreds of billions of dollars, with double-digit operating margins inclusive of ads that's growing at this pace. Year-to-date, units have grown nearly 15% year-over-year, and that's on an enormous base having sold more than 30 billion items last year. In absolute dollar terms, we've added more than $90 billion in gross sales in the trailing 12 months. And we're growing meaningfully faster than other retail competitors, adding about double the gross sales per quarter than our next largest competitor in the U.S. and consistently taking retail market segment share.
Over the past few years, our North America and international segments have each expanded operating margins by nearly 10 percentage points, which enables us to reinvest in making the customer experience even better. Remember, it's still early. The significant majority of retail, nearly 80% currently occurs in physical stores. That will eventually flip to e-commerce over time. We're helping enable this shift by rapidly building out our efficient and speedy fulfillment network, providing delightful customer experiences while driving significant free cash flow and return on invested capital.
Each of our priorities from faster delivery, to cost to serve, to groceries and pharmacy, to AI shopping are force multipliers, and we're firing on all cylinders. Our delivery speeds keep getting faster as we invest in our same-day network as well as our Amazon Now and Amazon Prime Air ultrafast services. We had our fastest Q3 ever globally, and we delivered more than 1.5 billion items to Prime customers same-day or overnight in Q3. We're energized by the customer response to our rapid rollout of Amazon Now around the world, is now available in over 450 towns and cities, and the number of items ordered through Amazon Now is up 10x year-over-year.
We're on track to reduce cost to serve per unit for the fourth consecutive year, which enables us to continue meeting or beating competitors' prices and cost effectively deliver a broad selection of fresh groceries and everyday essentials. Increasing speed is fueling our grocery business, including perishables and everyday essentials and gross sales grew to nearly $250 billion in the trailing 12 months. In Q3, fresh groceries and everyday essentials grew about 3x faster than the rest of our store, representing about half of all units sold. Customers who shop perishables with same-day delivery buy nearly 7x more everyday essential units than those who don't. And active grocery customers shop nearly 4x more nongrocery categories like home and apparel and spend over 2x more on those categories compared to nongrocery customers.
Amazon Pharmacy is also growing fast. The number of customers using it is up over 60% year-over-year with growth accelerating each quarter through 2026, and repeat customers grew more than 50% year-over-year. J.D. Power recently ranked Amazon Pharmacy, the top mail-order pharmacy for the third year in a row, and we keep making it even better, now offering 3-hour prescription delivery in more than 350 cities.
Over 400 million customers have used Alexa For shopping, our agentic shopping assistant, in the last 12 months with customer interactions up 570% year-over-year. U.S. customers using Alexa for Shopping are spending 50% more per order than those who don't. It researches products, compares options, checks a full year of price history, gets personalized gift recommendations, and tracks deals and price drops on customers' behalf. Though we anticipate working with horizontal agents, we believe Alexa for Shopping is going to be the primary shopping agent customers use to shop Amazon.
Having a shopping assistant constantly by your side as you browse, get inspired, have questions on product detail pages and that you can simply ask to buy something based on your prior purchases that already has your history, your shipping address and payment info is uniquely helpful and convenient for customers.
Moving to Amazon Ads. We generated $19.6 billion of revenue in Q3, up 12% year-over-year. Though there were some timing anomalies in this past quarter, we continue to be pleased with the overall momentum across our ad offerings. I'll mention 3 items impacting the growth rates. First, we shifted Prime Day into Q2 for most countries, moving significant sales and ad revenue that were in Q3 '25 into Q2 '26, a tailwind to our Q2 2026 rate and a headwind to Q3 2026. For advertising, that was 850 basis points sequential impact to Q3 year-over-year growth.
Second, Q2 '26 included the first season of NBA on Prime, which last year's Q2 didn't have, while Q3 does not include any NBA, it starts in Q4. And third, in Q3 2025, we changed our search engine marketing programs to drive more traffic to search pages on Amazon. It's a better experience for customers, and we also monetize that traffic at a higher rate and helped accelerate advertising revenue growth starting a year ago, and we started lapping that in Q3. We expect year-over-year growth will return to the high teens in Q4.
A natural question is whether agentic shopping from external horizontal agents is meaningfully impacting Amazon Ads. And the answer is no. Few customers are doing much shopping this way yet, as the experience is still not great nor more convenient than coming to a retailer directly to research or one-click order there. Q3 was chock-full of innovation from our ads team that we expect to have impact in the coming months. Headlined by Amazon Ads Agent, which brings together our full advertising offering under a single AI-first platform, backed by trillions of shopping, browsing and streaming signals, it supports advertisers at every step with insights, answers and the ability to optimize and act on their behalf.
We also launched full funnel campaigns in Amazon Ads Agent, bringing sponsored ads, display, video and streaming TV into a single campaign. Advertisers provide initial inputs, including budget and duration and Amazon's AI plans, executes and continually optimizes the rest.
We're continuing to see momentum in several other areas. I'll mention just a few. Prime Video has emerged as a significant business with a revenue run rate in the tens of billions of dollars now profitable in its own right. We have momentum with hit shows like Carrie, The Summer I Turned Pretty, The Boys, Off Campus, Reacher and Fallout. And breakout movies like Project Hail Mary, along with compelling live sports, including Thursday Night Football off to its best start ever in 2026, NBA on Prime, NASCAR, The Masters and UEFA Champions League soccer.
We recently launched our most powerful devices lineup yet with 34 new products across Echo, Kindle, Alexa Tablets, Fire TV, Ring and Bee. It's early, but we're off to a very strong start and excited for more customers to get their hands on these as we head into the holidays. And finally, Amazon Leo remains on track to begin initial service this year.
We're heading into one of our most exciting stretches of the year with both re:Invent and the holidays, and I want to thank our teammates for their hard work and invention to make customers' lives better and easier every day. What we're building at Amazon is unlike anything that's ever been seen before. There has never been a business with $1 trillion of annual revenue. Amazon is on a path to have 2 of them in AWS and stores. It's rare, and we're energized by what's ahead.
Over to you, Brian.

**Brian Olsavsky** (Executives):
Thank you, Andy. Let's start with our top line financial results. Worldwide revenue was $201.9 billion, a 12% increase year-over-year and 13% increase year-over-year, excluding the impact of foreign exchange. Worldwide operating income was $28.1 billion, with an operating margin of 13.9%, which is our highest operating margin ever.
Starting with our North American and International segment results. First, let me remind you that Prime Day has shifted this year with the sales event occurring in Q2 for most of our largest countries, including the United States. In 2025, Prime Day was entirely in Q3. Excluding the impact of this Prime Day time change, third quarter 2026 year-over-year growth would be approximately 400 basis points higher. In Q3 we saw strong customer engagement and a continuation of trends from the first half of the year. In the North America segment, third quarter revenue was $112.9 billion, an increase of 6% year-over-year. International segment revenue was $43.1 billion, an increase of 8% year-over-year, excluding the impact of foreign exchange. Worldwide paid units grew 12% year-over-year.
Prime remains a key pillar of our business. Hundreds of millions of Prime members are responding to our combination of vast selection, low prices and record delivery speeds. Over the past year, monthly orders of fresh groceries placed by our Prime members for free same-day delivery have more than tripled.
Let's shift to profitability. North America segment operating income was $8.7 billion, with an operating margin of 7.7%. International segment operating income was $1.6 billion with an operating margin of 3.7%. In our fulfillment network, the team navigated higher transportation costs from fuel inflation and higher linehaul rates. Even with these headwinds, we still lowered our overall cost to serve in Q3 through better inventory placement, shorter shipping distances and package consolidation. Shipping costs increased 11% year-over-year versus a 12% increase in units. Excluding fuel and linehaul inflation, shipping costs grew 8% or approximately 400 basis points slower than unit growth.
Robotics and AI are delivering measurable gains through productivity and employee safety, which we'll expect to compound in the future. In 2026, we doubled our fleet of robotic arms like Cardinal and Sparrow. We're also developing robotics foundation models that enable faster programming and teach robots increasingly complex physical tasks with the goal of delivering useful robotics at scale. Looking ahead, we see meaningful opportunities to improve productivity across our global fulfillment network and lower our cost to serve while continuing to get products to customers faster. Our operating margin may fluctuate quarter-to-quarter, but we're focused on sustained long-term improvement in our cost to serve per unit.
Moving to our AWS segment. Revenue was $46 billion and grew 39.3% year-over-year driven by both core and AI services. We added $3.8 billion in quarter-over-quarter revenue. AWS now has an annualized revenue run rate of $184 billion. Customers continue to move to the cloud and scale their use of AWS core services. And increasingly, customers who want the full benefits of AI are accelerating their transition to the cloud.
We see a strong linkage between AI spend and growth in our revenue for core services. As customers invest in AI, we see a corresponding increase in core consumption, and we expect that relationship to strengthen as more AI workloads move into production and drive additional demand for compute, storage and networking. AWS operating income was $17.8 billion with an operating margin of 38.7%, reflecting strong growth and our focus on driving efficiencies. Our investments in custom chips and custom networking along with software and process improvements are helping us optimize capacity and build a more cost-efficient infrastructure. As we've long said, we expect AWS operating margins to fluctuate driven in part by the level of investment we're making at any point in time. Our AI offerings are gaining traction with customers with AI revenue growing triple digits year-over-year. Bedrock has been a significant growth driver.
Now turning to our cash CapEx, which was $75.9 billion in Q3. This primarily relates to AWS and AI as we invest to support strong customer demand. We continue to make significant investments, especially in AI as we believe it to be a massive opportunity with the potential to drive long-term revenue and free cash flow as well as return on invested capital.
I'll finish with our financial guidance for Q4. Q4 net sales were expected to be between $240 billion and $247 billion. We estimate the year-over-year impact of changes in foreign exchange rates based on current rates, which we expect to be a headwind of approximately 60 basis points in the quarter. Q4 operating income is expected to be between $28.5 billion and $33.5 billion. I'll mention one factor impacting our Q4 guidance.
Amazon Leo's commercial service is on track to begin initial service this year, and we expect to begin capitalizing certain costs in Q1 of next year, including production and launch costs. This is later than I've been predicting in earlier earnings calls. As a result, we will continue to expense the majority of Leo-related costs in Q4. We're ready to serve customers this holiday season and to support the millions of customers building with AWS.
I want to thank our teams across Amazon for their hard work and focus on customers. Our commitment to elevating the customer experience remains the only reliable way to create lasting value for our shareholders.
With that, let's move on to your questions.

**Operator** (Operator):
[Operator Instructions]
And our first question comes from the line of Justin Post with Bank of America.

**Justin Post** (Analysts):
Andy, continue to see the cloud business accelerate, which is really nice. But the quarter-over-quarter growth slowed, and I'm just wondering if there's any callouts there on the customer side or token costs or anything that kind of drove that? And how you're thinking about the capacity adds in Q4?
And then, Brian, maybe just any impact of fuel costs on your guidance in Q4.

**Andrew Jassy** (Executives):
Yes. I'll start with the growth question. We're really pleased with the growth, 39.3% on a business that's got $184 billion annual revenue run rate is quite unusual. Our fastest growth in about 5 years or 6 quarters consecutively of acceleration. And we're adding quite a bit of capacity. I think if you look at what's driving the growth right now, it's a combination of a few things. First, on the AI side, the unusual top-to-bottom stack functionality we have, whether you're building your own model with SageMaker AI, which is the easiest way to build your own model, or you want to leverage one of the leading frontier models with high security and very strong price performance, people can use Bedrock.
Whether you are building your own agents where we have capabilities like Strands and AgentCore to build and to run those securely and scalably, or are you going to use turnkey agents, which most companies do, if you just look across Kiro for coding and Connect for call center and Transform for migrations and Quick, which is growing incredibly fast as an AI companion at work. People are adopting those very quickly.
And then we add a lot of capacity every quarter. Now the amount that we add every quarter is not equal. And we're adding different amounts each quarter. But if I look at how much we've added this year and what we have planned over the next, call it, 8 quarters or so, which is about as far out as we get 8 to 10 quarters, we have a lot of capacity coming as well. And then I layer on top of that, too, just the impact of chips. We're very well positioned for what's happening in AI because increasingly, what you're finding right now is most customers, every customer that runs -- that uses AI at scale. But particularly enterprises now as they're starting to deploy more inference into production, they are very eager to save on price performance. And Trainium, with a meaningful advantage it has in price performance versus other alternatives is very compelling to people.
And then as more and more people are using AI in a very broad way, it drives a lot of the core in capabilities like reinforcement learning and posttraining and tool calling and we have the leading CPU chip in Graviton, which is about 30% to 40% more price performant than the other x86 providers. So it's -- those things are really driving very significant growth. The amount of capacity we add each quarter will vary, but we're -- I mean, at this scale, to be projecting growing over 40% year-over-year in each of 2027 and 2028 is pretty significant and the fact that we believe that this can be a $1 trillion revenue business in 5 to 10 years, it's an extraordinary, unusual opportunity that we're very excited to be pursuing.

**Brian Olsavsky** (Executives):
And Justin, on your question about fuel and linehaul inflation, I would say -- I'm not going to -- I don't have an exact number for you, but it is higher in Q4 than it was in Q3. If you remember, we instituted a fuel surcharge at the beginning of the year for FBA sellers that recovers some, but not all of the costs that we're seeing on fuel for those shipments and then the remaining part is on the retail inbound shipments and outbound shipments. So it's in there. It's a little bit higher than Q3.

**Operator** (Operator):
Our next question comes from the line of Brian Nowak with Morgan Stanley.

**Brian Nowak** (Analysts):
I have 2. Andy, your excitement about AWS is coming through the line. It's pretty rare you would make comments about $1 trillion of revenue 5 to 10 years from now. It's more than you usually give. So can you just maybe walk us through how you get to that $1 trillion of dollars? Is it top down? Is it bottoms up? So what gives you confidence that you're going to be able to put up that type of revenue growth and to get to that type of number in the next 5 to 10 years?
Then the second one is for either of you on the robotics side. As we look into '27, what are the key milestones you're both focused on, on the robotics side for the retail business?

**Andrew Jassy** (Executives):
Yes. On the AWS side, if you just look at the growth rates, Brian, look at the growth rates on the run rate and then look at what we're projecting in '27 and '28. And as I've said a few times, we will always -- despite how much capacity we're providing, we -- the big chunks of capacity that people take, the hundreds of megawatts or sometimes up to 1 gigawatt of capacity, those big chunks are reserved well in advance because you can't leave 1 gigawatt of capacity hanging around. And so we have very good visibility into '27 and '28 and some of '29, too, with respect to what customers want in those really big chunks of capacity.
We will always leave a fair bit of capacity available for on-demand on EC2 or in Bedrock, and we're working closely with our customers and they'll have plenty of capacity to be able to use in AWS. But we have very good visibility into the next few years on what AWS looks like, those types of growth rates when you do the math on the revenue and the revenue run rate we have get you pretty quickly to escalating numbers.
And then I'd say that on top of not believing that a lot of the usage we see today is going to attenuate anytime soon. We're still really early in enterprises using inference in their production applications in a pervasive way. It just -- it is just really early. And some of that is enterprises having enough people who know how to operate in AI and posttrain and fine-tune models for the right applications. Some of it is the cost of inference. I think if we all want enterprises to be able to use inference the way we all believe they will, we have to keep working on taking the cost of inference down. That is a huge mission for AWS. It's one of the significant reasons why we're building our own custom silicon in Trainium is that we just really believe it's incredibly important for customers to be able to use inference in a much more cost-effective way. That has come down a lot, the cost of inference over the last couple of years, and I think it will come down meaningfully more.
And so -- and then you just think about what you're seeing. If you think about security, as an example, just by itself, the models today are so advanced that the vulnerabilities that they're finding humans just haven't found. And if you've had access to these models, it leads to -- you're using these models to both find them and ultimately to help with patching them and deploying. And there are some people who think that the amount -- the total amount of tokens used over the next year or 2, 20% of it is some significant percent of it may end up being just security, and that's a relatively new use case on top of what we're seeing with coding and how that continues to grow on top of what we're seeing with the various, I'll call it, AI companions, both in the consumer space and in the workspace, like with Quick. And these are just the initial big use cases.
And you layer on top of that, what you're going to see with enterprises where I believe virtually every enterprise -- modern enterprise production application will be rewritten to be agentically capable because that's the way you're going to have to deploy if you want to move quickly or you want to actually guard in the right way against some of the security risk there is just so much AI coming. And so that's -- you can't predict with any certainty 5 to 10 years from now, especially these types of growth rates, but it's not a stretch for us to imagine that this could be over a $1 trillion business.
On the robotics side, what I would say is that it's pretty remarkable what's happening in robotics right now. I'll say in general, but particularly at Amazon. We have over 1 million robots now in our fulfillment network. And while they're having very significant impact on our cost structure and on our productivity and on safety, if you look at our safety numbers in our fulfillment network, there are at record low numbers. We've made huge progress over the last 4 to 5 years, and robotics has been a big piece of that.
And yet I would tell you, we're still so early with respect to both what we have deployed -- built and deployed and what we're working on. And I think that you'll see, we will always have a lot of teammates in our fulfillment centers. But I think a lot of the jobs that we have that are more repetitive that we have humans doing will be done by robots. I think we will -- we're investing in all sorts of additional robotics of all different form factors. I think we have the opportunity to also assist on some of the delivering of the last 100 yards to customer stores. We have a lot coming.
And so for us, the way we measure robotics are, does it lead to comparable or better productivity, safety, cost structure and time to delivery. And when we like that combination of economics, we will deploy it at scale in our fulfillment network. And if I look at the new designs that we have coming in our fulfillment network, they -- including our expansion of same-day facilities, they are very heavy on robotics. So we think it had a big impact, and we think it's small compared to what it's going to be in the next 5 years.

**Operator** (Operator):
Our next question comes from the line of Mark Mahaney with Evercore ISI.

**Mark Stephen Mahaney** (Analysts):
Two things, one -- first, thanks a lot for the forward comments on AWS growth. Could I ask you to draw out margins, too? I know that margins can move up and down quarter-to-quarter, but over the next 2 years, do you think the current margin structure is relatively stable? We kind of hold at these kind of high 30s, 40% operating margins for AWS.
And then on perishable checkout, I'm super excited about this opportunity just watching how it's rolled out in my neighborhood and in other areas. How much coverage do you have for perishable checkout? In other words, how many Prime households do you think you've covered with perishable checkout? And for those that have used it, how much of a boost do you think that is per Prime household? Like is this something that increases spend per Prime household by 20%, 50%, 100%? Just given how large the fresh grocery category is?

**Brian Olsavsky** (Executives):
Mark, let me start with the operating margin outlook for AWS. So we're not guiding out beyond -- we're not guiding at all on our margin for AWS. But I can tell you -- give you my color on it. So very -- it seems very strong op margin, 38.7% this quarter. And I would add that the profitability you've been seeing recently is really not a random output, it's a result of a lot of disciplined efficiency gains, capacity optimization, closely managing our fixed cost. And as Andy said, the inclusion of over time, more and more custom chips into our cost structure. However, there are other things bouncing around. In fact, the outsized growth of AI puts margin pressure on the business as a whole because the margins are lower there.
We are happy with the progression in both core and AI margins. And there -- as Andy said earlier, they're ahead of where the core was at a similar point in time, but they're still lower. So there's going to be that mix issue. There's also headwinds from component pricing that we've talked about. So cannot predict it, but there's going to be always a confluence of these multiple factors that we're working very hard on the cost side and the efficiency side in dealing with investments and new product margins as they start up and launch and reach scale.

**Andrew Jassy** (Executives):
On the perishables checkout, Mark, I share your enthusiasm about it. It's -- as you know, we've had a big grocery business for a while. And it's mostly been in the middle aisles of what you'd find in a grocery store, consumables, canned goods, pharmaceutical items, beauty products. And we've had this leading organic grocery store in Whole Foods Market, which also is growing faster than the rest of the grocery segment, both on the top line and the bottom line with a new format and Daily Shop in urban environments that's doing really well that we're in the process of rolling out over the next couple of years.
We've always known if we wanted to be able to serve customers the way we think they want to be served and the way we want to, we have to have a mass offering, it starts with perishables. And if you look at the total spend per household, when we look at the difference between the total amount of spend that we think our consumers and customers are spending on items that we could serve them on versus what they spent in us, the biggest difference is grocery. And a lot of your shops, a lot of grocery starts with perishables. And so we are -- we really are excited that we feel like we found something with shipping perishables out of our same-day facilities.
We've grown our everyday essentials to about 3x faster than the rest of our store. It represents about half of our units now if I look at all the everyday essentials. What we find is customers who shop perishables through our same-day delivery, they buy about 7x more everyday essential units than those that don't. So again, if you're trying to close that gap between what consumers spend overall and the items that we can provide versus what they spend with us, perishables has a huge impact on that.
We also see that our grocery customers shop about 4x more nongrocery categories, like home and apparel and a bunch of other categories and spent about 2x more on those categories compared to those who don't use us for grocery. So those are big differences, and we believe that the progress we're making on perishables and grocery is going to ultimately lead to more -- being more relevant to customers for more of their shopping missions.

**Operator** (Operator):
Our next question comes from the line of Eric Sheridan with Goldman Sachs.

**Eric Sheridan** (Analysts):
Maybe a 2-parter on market opportunities within AWS. First, with respect to Bedrock, what have been your key learnings about the market opportunity around Bedrock and how it might continue to scale in the years ahead? And then with respect to the decision to sell Trainium externally, how do you think about balancing the market opportunity of external sales relative to the need for compute for that opportunity relative to other opportunities broadly across both internal use cases and AWS?

**Andrew Jassy** (Executives):
Yes. On the Bedrock side, I would tell you, you've probably heard this from us multiple times over the last couple of years. But one of the lessons that we've learned, I'll say, for 20-plus years in offering technology to customers, is that there is not one tool to rule the world. People always assume that whatever is in the lead early on is going to be the only thing or things that people use, and it's never the case. It's not true in database. It hasn't been true in analytics. In the beginning of AI, everyone said the only framework people use is TensorFlow. It turns out PyTorch is much bigger now.
And so -- and it's not going to be true with models either. In -- I'll say in the next 2 to 3 years, I think they're going to be 6 to 8 models that are about as good as each other or at least good enough for 95-plus percent of the workloads. And some will be better at reasoning and some will be better at coding and some will be better at visual pieces and some will be lower latency and some will be lower cost. And most customers are going to use multiple models, and many will use multiple models in the same generative AI application.
And so what customers really want to do, and we see this validated over and over again when we talk to customers is they want a service that has really broad selection of those frontier models and that has very good price performance and it has very strong security and access control. And they want that service so that they can kind of decide what combination of models they want to use and to swap them back and forth as they leapfrog each other as different constraints of their applications require them. And that's what we see with Bedrock. People are very excited about it.
We have both closed models and models like Anthropic and OpenAI's models. We have open models with Kimi and GLM and others. I think the Western world is very hungry for additional open models that are Western open models. And so I believe that will happen over time as well. But I think that the size of the opportunity in Bedrock is gigantic. And it could be a service as large as EC2, which is a very large service today in AWS. So I think it's very large.
On the balance of chips and what you sell externally versus what you use inside your cloud, it's a very good question. And it's a question that we're continuing to evaluate as we speak. I would say that the number of companies who have a significant cloud business and a chip strong enough to sell externally is effectively 2. So there really aren't many customers that have to grapple with the same type of problem at this type of scale. And at this point, everybody is producing their advanced chips with the same provider. There's only so many chips that provider can provide each year. Everybody gets an allocation. And you have to decide with that allocation how much of it you want to sell externally and how much of it you want to use in your cloud.
And there's a trade-off. If you sell externally, you're able to realize more revenue in the short term because you get to recognize the revenue as soon as it leaves your inventory. And on the flip side, if you decide to use it inside your cloud in the form of EC2 instances or Bedrock, you actually will end up driving more absolute revenue and free cash flow from those chips because you get to use them over 5 to 6 years and drive revenue for a longer period of time. So it is -- you have to really think through what you want to do. To date, I would say that we've taken a different approach in how we've used our chips than the other provider who has the same type of balancing act going on.
And as I mentioned earlier, we believe we're going to have a very significant business selling chips externally, and we're going to start in late 2027. And we will be thinking through that balance, I think, probably every year. But they'll both be very significant. Our ability to create price performance, scalable chips is going to be a very significant strategic advantage for us at scale, both in our own cost structure as well as building a separate business and selling external chips and selling external chips really is a very different business than your cloud infrastructure business.

**Operator** (Operator):
Our next question comes from the line of Doug Anmuth with JPMorgan.

**Douglas Anmuth** (Analysts):
When you think about the 40% plus AWS revenue growth each of the next 2 years and then the multiyear path beyond that, can you just talk about the CapEx required to drive that kind of revenue over the next couple of years and beyond? And then also, Andy, any updates just to how you're thinking about the duration of returns on both servers and networking and then also data centers?

**Andrew Jassy** (Executives):
Yes. I'll take them in reverse order. So on the breakeven on our infrastructure, as I mentioned in my opening comments, we're continuing to move that left. We're continuing to make that shorter. There are a lot of -- core is a little bit different from AI is a little bit different from how you finance these things. And so it varies depending on which you're talking about, but we're continuing to make progress as we historically have been pretty good at doing, if you think about AWS, at finding ways to extend useful lives and to make the breakeven sooner, and we're making good progress there, too.
On the CapEx involved to grow the way we're talking about, it's meaningful. And I think that this -- the way we think about it, Doug, is that this is a once-in-a-lifetime opportunity. I think what we're seeing with AI, it's the biggest transformation in our lifetime. And if the idea of being able to grow 39% with $184 billion annual run rate and to grow 40% a year on top of that in each of the next 2 years and ultimately end up as $1 trillion-plus business, we're going to invest to continue being the leader. We are the leader today in the, I'll call it, the infrastructure and AI space. And would it be more convenient if this type of acceleration and opportunity happened over 25 years and you could spread the CapEx over 25 years? Yes, it might be more convenient, but that's not the world that we live in, and that's not the opportunity.
And we can fund this plan. And I think it will forever change the size of Amazon. It will ever -- forever change our revenue. It will forever change our free cash flow. And we're going to invest and we're going to pursue it to continue to be the significant leader like we are today.

**Operator** (Operator):
And our final question comes from the line of Ross Sandler with Barclays.

**Ross Sandler** (Analysts):
Great. Yes, I thought I'd double down on the Bedrock question. So the token marketplace on Bedrock seems to be one of the hottest services in AI right now. And our understanding is the majority of these workloads are running on Trainium. So as this becomes a bigger part of the overall AWS story, like you just mentioned, Andy, how might that impact both revenue growth, but especially margins at AWS as you kind of shift from selling bare metal to selling more inference as a service. Could you just talk about that?

**Andrew Jassy** (Executives):
Yes. Well, you're right that the majority and most of Bedrock today is being run on top of Trainium. And we do that in meaningful part because we really like the price performance that we're getting, and it allows us to keep -- to both keep prices as low as possible for customers as well as our ability -- we like the margins associated with it. If you think about margins in the cloud space and you're looking at different players and what their cost structure looks like, there are a few things to pay attention to. The first is for their data centers, how many of them are they actually buying or long leasing versus doing colo or neoclouds. I mean neoclouds are about 3,500 basis points worse in operating margin than if you long lease them.
So -- and then you look at what is the hardware on top of which they're running. And the -- if you're using the hardware that everybody else is using, you'll have a comparable cost structure to what everybody is doing. And if you have the ability to use hardware that's different, you'll have an advantage. And so I think when you look at what we're doing, most of our capacity is either owned or long leased which is -- enjoys better operating margins than what you'll find when people are mostly doing colo or neo or a big chunk doing colo or neo. And the fact that we're running on top of our own chip that's providing both advantaged price performance and it's more cost effective for ourselves because we own it, I think, gives us some structural cost advantages that I think are going to be very helpful to customers as we pass them back to customers and helpful to the overall economics of AWS.

**Dave Fildes** (Executives):
Thanks for joining us for the call today and for your questions. A replay will be available on our Investor Relations website for at least 3 months. We appreciate your interest in Amazon and look forward to speaking with you again next quarter.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AMZN_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO｜guidance：Q3 net sales guidance range（原話："Q3 net sales are expected to be between $197 billion and"）
- 2026-07-30｜CFO｜guidance：Q3 operating income guidance range（原話："expected to be between $22.5 billion and $26.5 billion."）
- 2026-07-30｜CFO｜guidance：Q3 guidance includes FX headwind（原話："unfavorable impact of approximately 80 basis points from the"）
- 2026-07-30｜CFO｜margin：Prime Day timing: 2025 event was entirely in Q3（原話："In 2025, Prime Day was entirely in Q3."）
- 2026-07-30｜CFO｜margin：Ex-Prime Day, Q3 growth would be ~400bp higher（原話："year-over-year growth would have been nearly 400 basis"）
- 2026-07-30｜CFO｜guidance：Stores trend into Q3 after Prime Day adjustment（原話："a continuation of the trends that we have"）
- 2026-07-30｜CFO｜margin：Q2 operating income included ~$1.2B of expense-reducing items（原話："reduced expenses by approximately $1.2 billion"）
- 2026-07-30｜CFO｜margin：Tariff refund of ~$600M in North America（原話："tariff-related refunds of approximately $600 million."）
- 2026-07-30｜CFO｜margin：~$600M energy-contract derivative fair-value gain, mainly AWS（原話："a separate benefit of approximately $600 million related to"）
- 2026-07-30｜CFO｜margin：AWS margin expansion YoY, with and without derivative gain（原話："we're up 650 basis points year-over-year."）
- 2026-07-30｜CFO｜margin：CFO says AWS margins will fluctuate（原話："We've said before, these margins will fluctuate."）
- 2026-07-30｜CEO｜margin：CEO on AI margin trajectory vs core（原話："we see the AI business following very much the same type of"）
- 2026-07-30｜CFO｜margin：International segment margin（原話："$1.7 billion with an operating margin of 4.1%."）
- 2026-07-30｜CFO｜margin：Fulfillment margin not linear（原話："progress may not always be linear"）
- 2026-07-30｜CFO｜margin：Transportation cost headwind（原話："heightened transportation costs driven by fuel inflation"）
- 2026-07-30｜CEO｜capital_allocation：2026 cash capex raised to ~$220B due to memory costs（原話："approximately $220 billion in cash CapEx in 2026, with the"）
- 2026-07-30｜CEO｜capital_allocation：Prior capex plan ~ $200B（原話："approximately $200 billion in cash CapEx in 2026"）
- 2026-07-30｜CFO｜capital_allocation：Q2 cash capex（原話："cash CapEx, which was $53.1 billion in Q2."）
- 2026-07-30｜CEO｜capital_allocation：Server break-even period（原話："a little less than 3 years to break even on that investment."）
- 2026-07-30｜CEO｜capital_allocation：Server spend is demand-triggered（原話："If the demand isn't there, we won't spend the capital."）
- 2026-07-30｜CEO｜capital_allocation：Server useful life（原話："currently have a useful life of at least 5 to 6 years"）
- 2026-07-30｜CFO｜capital_allocation：Funding sources: debt issued this year, nothing further to share（原話："You've seen us issue debt this year."）
- 2026-07-30｜CEO｜commitment：Capacity still short of demand in 2026 and expected 2027（原話："have enough capacity to meet all the demand we have in 2026"）
- 2026-07-30｜CEO｜commitment：Capacity doubling target by end-2027 reaffirmed（原話："power capacity by the end of '27 that we had in '25"）
- 2026-07-30｜CFO｜commitment：Robotic arms fleet to more than double in 2026（原話："double our fleet of robotic arms, like Cardinal and Sparrow"）
- 2026-07-30｜CEO｜commitment：Capacity already reserved for 2028（原話："capacity that's already been reserved for '28."）
- 2026-07-30｜CEO｜commitment：Pursuing own frontier model（原話："we are pursuing our own frontier model"）
- 2026-07-30｜CEO｜product：AWS revenue growth and acceleration（原話："Revenue growth of 36.7% year-over-year, accelerating for the"）
- 2026-07-30｜CEO｜product：AWS backlog（原話："our backlog stands at $496 billion, growing triple digits"）
- 2026-07-30｜CFO｜product：AWS operating income（原話："AWS operating income was $16.6 billion"）
- 2026-07-30｜CEO｜product：Chips run rate（原話："revenue run rate of over $25 billion, growing triple-digit"）
- 2026-07-30｜CEO｜product：Kiro usage growth（原話："tripled in usage quarter-over-quarter"）
- 2026-07-30｜CEO｜product：Amazon Ads revenue（原話："strong growth across our offerings, generating $19.8 billion"）
- 2026-07-30｜CEO｜competition：NVIDIA partnership and customer choice（原話："will run on NVIDIA for as long as we can foresee"）
- 2026-07-30｜CEO｜competition：No own frontier model needed for AWS success（原話："a wildly successful business without its own frontier model."）
- 2026-07-30｜CEO｜competition：Possible third-party Trainium sales（原話："I expect there's a real chance we'll do that in the future."）
- 2026-07-30｜CEO｜customer：Anthropic and OpenAI Trainium commitments（原話："multi-gigawatt commitments from the 2 largest AI labs"）
- 2026-07-30｜CEO｜customer：Alexa for Shopping usage（原話："Over 350 million customers have used it in the last 12"）
- 2026-07-30｜CEO｜customer：Amazon Leo status（原話："Amazon Leo is close to 400 satellites in orbit"）
- 2026-07-30｜CEO｜customer：AWS long-term revenue ambition raised vs prior few-hundred-billion view（原話："now believe it'll be at least double that"）
- 2026-07-30｜CEO｜customer：AWS long-term revenue possibility（原話："very possibly be $1 trillion annual revenue business"）
- 2026-07-30｜CEO｜risk：Component price inflation (memory, drives, SSD)（原話："there are inflated prices right now on some of the"）
- 2026-07-30｜CEO｜risk：Contract pricing fixed over duration of signed deals（原話："those will be the prices and those will be the"）

### 問答異常語氣（迴避／改口／保留）
- AMZN_Q2_2026_Earnings_Call_20260730.md｜問：Anmuth: sustainability of 39% AWS operating margin｜答法：CFO: margins 'will fluctuate' without giving a sustainability view; CEO pointed to core-margin trajectory
- AMZN_Q2_2026_Earnings_Call_20260730.md｜問：Post: H2 vs H1 gigawatts added and 2027 outlook｜答法：CEO reiterated earlier doubling-by-end-2027 target; gave no H1/H2 split or 2027 figure
- AMZN_Q2_2026_Earnings_Call_20260730.md｜問：Nowak: timing of third-party Trainium sales and ROIC｜答法：CEO said 'real chance' in the future; no timing or ROIC given
- AMZN_Q2_2026_Earnings_Call_20260730.md｜問：Sebastian: sources of capital for build-out｜答法：CFO: 'nothing to share today' after noting debt issued this year
- AMZN_Q2_2026_Earnings_Call_20260730.md｜問：Gawrelski: what RPO implies for 2028+ capacity｜答法：CEO said backlog is in capex projections; no 2028 capacity quantification

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
{"date":"20260731","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AWS 在 FY2026-27 維持 ≥30% 營收成長，且營運利益率守住 ≥35%——量與利同時成立，不接受「用利潤率換成長」或「用成長換利潤率」的任一單邊","columns":{"2Y 驗證點":"連 4 季營收 ≥ +30% 且利潤率 ≥ 35%","5Y 驗證點":"AWS 年化營收 ≥ $3,500 億","10Y 驗證點":"AWS 走在邁向 $1 兆年營收的軌道上","具體數字門檻":"Q2'26 實績 +36.7% ／ 39.3%（剔除衍生工具利益 37.9%）；年化 run rate $1,690 億；合約餘額 $4,960 億","信息來源":"公司 Q2 2026 法說（2026-07-30，Jassy 與 Olsavsky）","漂移觸發條件":"連 2 季 TTM 偏離 ≥ 5% → 削弱；連 3 季偏離 ≥ 10% → 反轉"}},{"id":"H2","text":"約 $2,200 億／年的資本支出在 FY2028 前把 TTM 自由現金流拉回正值，且折舊年限不再向下修正","columns":{"2Y 驗證點":"FY2027 TTM 自由現金流 ≥ $0","5Y 驗證點":"自由現金流率回到 ≥ 8%","10Y 驗證點":"投入資本報酬率回到 ≥ 15%","具體數字門檻":"現況 TTM 自由現金流 −$76 億（去年同期 +$182 億）、TTM 資本支出 $1,690 億。管理層框架：資料中心提前 2 年投入、30 年以上壽命；伺服器不到 3 年回本、5-6 年壽命；AI 產能多為 ≥5 年合約","信息來源":"公司 Q2 2026 法說；耐用年限沿革見 10-K 與 2025 年初的年限回調揭露","漂移觸發條件":"連 4 季 TTM 偏離 ≥ 5% → 削弱。加速條款：折舊年限自 5 年再縮短，或利息費用年增率連 2 季超過營運利益年增率 → 直接判削弱，不等四季"}},{"id":"H3","text":"零售兩段的營運利益率結構性上行：北美 7.9% → FY2028 ≥ 10%，國際 4.1% → ≥ 5.5%","columns":{"2Y 驗證點":"北美（剔除退款）連 4 季 ≥ 7.5%","5Y 驗證點":"北美 ≥ 10%、國際 ≥ 5.5%","10Y 驗證點":"零售段營運利益達 AWS 之半","具體數字門檻":"Q2'26 北美 $91 億／7.9%（含 $6 億關稅退款，剔除後 7.3%）、國際 $17 億／4.1%。驅動：機器手臂 Cardinal 與 Sparrow 機隊 2026 年翻倍以上、同日達網路擴至 2,300 城生鮮、廣告 $198 億／+26% 附著","信息來源":"公司 Q2 2026 法說；Profitero 第三方定價研究（Amazon 售價平均低於同業 14%）","漂移觸發條件":"連 2 季北美（剔除退款）&lt; 7.0% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"折舊牆：資本支出遞延 2-3 年後轉為折舊費用，同時 AI 伺服器實際經濟壽命短於帳列 5 年，迫使年限再度下修","columns":{"對應假設":"H2（並外溢 H1 的利潤率）","時間尺度":"🔥 中期（4-6 季）","監測指標":"合併折舊攤銷／營收；伺服器耐用年限（10-K）；AWS 增量營運利益率","警戒閾值":"折舊／營收 &gt; 11%（FY2025 為 9.2%）且合併營運利益率守不住 13%；或年限由 5 年下修"}},{"id":"R2","text":"前緣需求的份額稀釋：Google Cloud 本季 +82%、合約餘額 $5,140 億已反超 AWS 的 $4,960 億；Azure +43% 且年營收破 $1,000 億。AWS 佔三巨頭營收池比重由約 48.2% 降至約 44.4%（年減 3.8 個百分點）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"三巨頭季度營收絕對增額對比；Anthropic／OpenAI 運算分配比例","警戒閾值":"AWS 季度絕對營收增額連 2 季低於 Google Cloud（Q2'26：AWS 約 +$113 億 vs GCP 約 +$112 億，已幾乎持平）"}},{"id":"R3","text":"資金結構槓桿化：總負債由 2025 年底 $1,530 億升至最近一季 $2,355 億，2026 年至今發債逾 $890 億；自由現金流為負而資本支出續增，形成「借錢蓋、蓋完折舊、折舊壓利潤」的三段夾擊","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"淨負債／EBITDA；利息費用年增率 vs 營運利益年增率","警戒閾值":"淨負債／EBITDA &gt; 1.5 倍（現約 0.54 倍，兩季前約 0.21 倍）；或利息費用增速連 2 季超前營運利益增速"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"首階 1/2·逢回 $215-235 補足·加碼＝AWS ≥30% 連兩季且 TTM FCF 轉正","irr_base_pct":12.9,"ev5y_pct":70.3,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":5.3,"ev5y_pct":70.3,"irr_base_pct":12.9,"max_dd_pct":-55.0,"bull_5y_price":585.0,"bear_5y_price":172.5,"p_bull_pct":27.0,"p_bear_pct":28.0,"rearm_trigger":"首階 1/2·逢回 $215-235 補足·加碼＝AWS ≥30% 連兩季且 TTM FCF 轉正","price_at_dd":235.5,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMZN_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
