你是 stock-analyst **v20 判斷 agent**，標的 CRS（20261025）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CRS","date":"2026-10-25","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRS_20261025/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRS_20261025/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":798.2,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q1 FY27 新聞稿（8-K 附件）"},"note":"未取得"},{"id":"f_kpi1_adjusted_operating_margi","label":"Adjusted operating margin excl. surcharge","value":30.9,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q1 FY27 新聞稿；公司只揭露此利益率，未揭露 Non-GAAP 營業利益金額"},"note":"未取得"},{"id":"f_kpi2_gaap_operating_income","label":"GAAP operating income","value":196.4,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"USD M（營業利益率 24.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q1 FY27 新聞稿"},"note":"未取得"},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":-24.8,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q1 FY27 新聞稿（營運現金流 52.8，資本支出 77.7，主因 brownfield 擴產）"},"note":"未取得"},{"id":"f_kpi5_guidance_q2_fy27_operati","label":"Guidance: Q2 FY27 operating income","value":"192–197","period":"Q1 FY2027 新聞稿（公告於 2026-10-22）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q1 FY2027 新聞稿（公告於 2026-10-22）","citation":"公司 Q1 FY27 新聞稿"},"note":"未取得"},{"id":"f_kpi6_guidance_fy27_operating_","label":"Guidance: FY27 operating income","value":"850–880","period":"Q1 FY2027 新聞稿（公告於 2026-10-22）","unit":"USD M（較 FY26 的 702.0 成長 21–25%，維持不變）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q1 FY2027 新聞稿（公告於 2026-10-22）","citation":"公司 Q1 FY27 新聞稿；FY29 營業利益目標 1,200–1,300"},"note":"未取得"},{"id":"f_kpi7_sao_segment_operating_ma","label":"SAO segment operating margin / adj. margin excl. surcharge","value":29.6,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"%（adj. excl. surcharge 37.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q1 FY27 新聞稿；SAO 營收 730.4、營業利益 216.3"},"note":"未取得"},{"id":"f_kpi8_aerospace_defense_end_ma","label":"Aerospace & Defense end-market sales","value":425.4,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q1 FY27 新聞稿；商用航太結構件／通路訂單 QoQ +23%、YoY +49%"},"note":"未取得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-22","period":"2026-10-22","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-22"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_crs_gross_margin_pct","label":"CRS 毛利率","value":30.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crs_operating_margin_pct","label":"CRS 營業利益率","value":22.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crs_fcf_margin_pct","label":"CRS FCF 利潤率","value":11.6,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hwm_gross_margin_pct","label":"HWM 毛利率","value":36.03,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hwm_operating_margin_pct","label":"HWM 營業利益率","value":27.31,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hwm_fcf_margin_pct","label":"HWM FCF 利潤率","value":19.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ati_gross_margin_pct","label":"ATI 毛利率","value":23.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ati_operating_margin_pct","label":"ATI 營業利益率","value":15.19,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ati_fcf_margin_pct","label":"ATI FCF 利潤率","value":11.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mtrn_gross_margin_pct","label":"MTRN 毛利率","value":16.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTRN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mtrn_operating_margin_pct","label":"MTRN 營業利益率","value":6.35,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTRN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mtrn_fcf_margin_pct","label":"MTRN FCF 利潤率","value":1.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTRN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rs_gross_margin_pct","label":"RS 毛利率","value":28.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rs_operating_margin_pct","label":"RS 營業利益率","value":7.76,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rs_fcf_margin_pct","label":"RS FCF 利潤率","value":3.41,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc","label":"SBC","value":6.4,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"USD M（占 GAAP 營業利益 3.3%，占營收 0.8%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q1 FY27 新聞稿；占比為 6.4÷196.4、6.4÷798.2 自算"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":284.66,"period":"2026-10-23（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-33.32,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":11.08,"period":"2026-10-23（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.59,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.46 → 13.38）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（15.96 → 15.96）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.42,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.12 → 19.2）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":13.38,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":15.96,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":19.2,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":26.47,"period":"2026-07-30 → 2026-10-24","unit":"%","basis":"FY1 共識 EPS 10.58 → 13.38（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":25.1,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.42,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝39.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":39.5,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.59,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝39.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":39.2,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":21.28,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 13.38，分子＝快照價 284.66","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.281,"period":"2026-10-25","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-25"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":539.8,"period":"2026-10-25","unit":"USD m","basis":"yfinance 最新一季：總債務 699.3、現金 159.5（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-25"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":49.54,"period":"2026-10-25","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-25"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":14642.06,"period":"2026-10-25","unit":"USD m","basis":"市值 14102.26 ＋ 淨負債 539.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-25"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":3435.36,"period":"2026-10-25","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（6 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-25"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":3790.28,"period":"2026-10-25","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（6 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-25"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.26,"period":"2026-10-25","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-25"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-10-25","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 284.66 / W52 418.01 / W104 317.22 / W250 168.26 / W250 13週斜率 3.24%"},{"id":"f_ma_w52","label":"52 週均線","value":418.01,"period":"2026-10-25","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":317.22,"period":"2026-10-25","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":168.26,"period":"2026-10-25","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":3.24,"period":"2026-10-25","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"10-K 自述：高價值產品的主要競爭對手不到十家；產品多需通過客戶資格認證，公司的技術與研發構成對現有及潛在競爭者的進入障礙。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm","excerpt":"There are less than ten companies producing one or more similar products that we consider our major competitors for our high-value products used in demanding applications. Many of our products are generally required to meet complex customer product specifications and often require the materials to be qualified prior to supplying the customer.","as_of":"2026-08-12","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"社群敘事提到競爭對手（如 ATI）增加產能投資，長期可能帶來較大價格壓力。","source":"Simply Wall St community narrative","url":"https://simplywall.st/community/narratives/us/materials/nyse-crs/carpenter-technology/g2ja5i47-aerospace-demand-and-brownfield-expansion-will-open-new-markets-h7ag","excerpt":null,"as_of":"2026-08-15","retrieved_at":"20261025","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2026 10-K：合併基礎下不依賴單一或極少數客戶；FY2026/2025/2024 無單一客戶占淨銷售 10% 以上","source":"Carpenter Technology Form 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0000017843/000001784326000034/crs-20260630.htm","excerpt":"On a consolidated basis, we are not dependent upon a single customer, or very few customers, such that the loss of any one or more particular customers would have a materially adverse effect on our consolidated statement of operations. No single customer accounted for 10 percent or more of total net sales for the years ended June 30, 2026, June 30, 2025 and June 30,","as_of":"2026-08-01","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"FY2024–FY2026 皆無單一客戶占淨銷售 10% 以上，6/30/2026 與 2025 應收帳款亦無單一客戶占 10% 以上；公司以客戶信用評估與客戶分散降低應收風險。","source":"SEC EDGAR 10-K FY2026 Item 8","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm","excerpt":"During fiscal years 2026, 2025 and 2024, no single customer accounted for 10 percent or more of total net sales. No single customer accounted for 10 percent or more of the accounts receivable outstanding at June 30, 2026 and 2025.","as_of":"2026-08-12","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q4 FY2026 call：FY2027 營業利益指引 $850–880M（+21–25%），FY2029 目標 $1.2–1.3B；管理層稱 FY2027 為潛在底部；棕地擴產按期於 FY2028 初完工，約 FY2030 年增營業利益約 $150M；部分結構件客戶下單低於預期需求。","source":"Zacks／MarketBeat／MyChesCo, Carpenter Q4 FY2026 earnings call coverage","url":"https://www.zacks.com/stock/news/2965759/crs-q4-earnings-call-highlights-strong-growth-outlook","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261025","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q2 FY2026 簡報：管理層稱航太與國防需求加速將超過供給、FY2027 不是高峰、全球合格鎳基超合金生產商很少；2019 年以來除內部生產力提升外無實質產能新增；棕地擴產約加 9,000 噸（約 2019 出貨量 7%）；完成三份航太長約並大幅調價。","source":"Carpenter 8-K Q2 FY2026 earnings presentation（經搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000005/a2q26earningspresentatio.htm","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261025","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"United Performance Metals 主管預期廠端產能 2026 下半年至 2027 轉緊；最難取得品項為鍛造鈦、特殊鎳棒、鈷合金；GMI 報告稱新航太級供應商資格認證需 18–36 個月（單一廠商報告，未獨立驗證）。","source":"UPM blog／Global Market Insights（搜尋摘要）","url":"https://www.upmet.com/resources/blog/supply-chain-outlook-conversation-katie-bland-director-product-management","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261025","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"鈦醫療經銷客戶需求疲弱拖累 Performance Engineered Products（Q2 FY2026），管理層稱 1 月訂單為 2025 年最高。","source":"MarketBeat Q2 FY2026 call highlights（搜尋摘要）","url":"https://www.marketbeat.com/instant-alerts/carpenter-technology-q2-earnings-call-highlights-2026-01-29/","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261025","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ATI 因航太與國防需求上調 2026 獲利指引，噴射引擎材料、國防合金最強","source":"metalnomist ATI coverage","url":"https://www.metalnomist.com/2026/07/ati-aerospace-and-defense-demand-lifts.html","excerpt":"ATI Aerospace and Defense Demand Lifts 2026 Guidance ATI raises 2026 guidance as aerospace, defence and jet engine material demand strengthens. By The Metalnomist on 7/30/2026 0","as_of":"2026-07-30","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2026 10-K 法律程序章節：僅環境整治（PRP/Superfund）與例行訴訟，未揭露反壟斷調查；公司預期已知或有事項不致對財務有重大不利影響。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm","excerpt":"Based on information currently available, the ultimate resolution of our known contingencies, individually or in the aggregate and including the matters described in Note 12 to the consolidated financial statements in this Form 10-K, is not expected to have a material adverse effect on our financial position, cash flows or results of operations.","as_of":"2026-08-12","retrieved_at":"20261025","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"公司透過附加費機制把關稅造成的原料成本轉嫁客戶，管理層認為目前關稅與中東衝突對公司無重大影響。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm","excerpt":"We have in the past used and plan to continue using these surcharge mechanisms to pass through the impact of any incremental tariffs on our raw material costs to our customers. As such, at this time and based on current information, we believe these items will not have a material impact on the Company.","as_of":"2026-08-12","retrieved_at":"20261025","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"風險因子列示關稅、配額、出口管制與貿易政策變動為國際營運風險，可能對業務重大不利。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm","excerpt":"These changes, including any implementation of or changes in trade sanctions, tariffs and embargoes, could materially adversely impact our business or require us to make changes to our current business practices or supply chain.","as_of":"2026-08-12","retrieved_at":"20261025","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險因子：部分關鍵原料向政經情勢可能不穩的國家的供應商採購，且供應商漲價或無法供貨時可能沒有替代來源；未點名國家，也未揭露特定單一來源供應商","source":"Carpenter Technology FY2024 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784324000014/crs-20240630.htm","excerpt":"In some cases, these critical raw materials and supplies are purchased from suppliers operating in countries that may be subject to unstable political and economic conditions.","as_of":"2024-08-15","retrieved_at":"20261025","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險因子：供應商漲價或不願／無法滿足需求時，公司可能沒有替代供應來源","source":"Carpenter Technology FY2024 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784324000014/crs-20240630.htm","excerpt":"If suppliers increase the price of critical raw materials or are unwilling or unable to meet our demand, we may not have alternative sources of supply.","as_of":"2024-08-15","retrieved_at":"20261025","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"3Q26 財報簡報前瞻聲明風險因子：取得能源或原料的能力，特別是來自政經情勢可能不穩國家的供應商，以及關稅與勞資糾紛","source":"Carpenter Technology 3Q26 Earnings Presentation","url":"https://s21.q4cdn.com/563831349/files/doc_financials/2026/q3/3Q26-Earnings-Presentation-FINAL.pdf","excerpt":"(3) the ability to recoup increases in the cost of energy, raw materials, freight or other factors; (4) domestic and foreign excess manufacturing capacity for certain metals; (5) fluctuations in currency exchange and interest rates; (6) the effect of government trade actions, including tariffs;","as_of":"2026-04-23","retrieved_at":"20261025","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"FY2026 航太國防淨銷售（不含附加費）年增15%；醫療約-21%、運輸約-11%","source":"Panabee FY26 results","url":"https://www.panabee.com/news/carpenter-earnings-2026-annual","excerpt":"income of $702 million and adjusted EPS of $10.76, primarily driven by 15% growth in the Aerospace and Defense segment which comprises 65% of sales. Management's new $1 billion share repurchase authorization signals confidence in long-term cash generation despite noted revenue declines in the Medical (-21%) and Transportation (-11%) segments.","as_of":"2026-08-12","retrieved_at":"20261025","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"三份航太長約已談成且價格大幅上調，非長約定價仍強；航太建造率目標較2025增約50%；FY27不是高峰","source":"Carpenter Q2 FY26 earnings presentation 8-K","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000005/a2q26earningspresentatio.htm","excerpt":"portfolio Completed negotiations on three aerospace LTAs with significant pricing increases • Aerospace supply chain remains confident in long-term demand • Customers focused on surety of supply Addressing frequently asked questions in Q2 FY26 Accelerating demand for nickel-based superalloys • Increasing supply chain confidence as build rates ramp • Aerospace industry targeting build rate","as_of":"2026-01-29","retrieved_at":"20261025","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2027營業利益指引$850–880M（+21–25%），FY2029目標$1.2–1.3B","source":"MyChesCo","url":"https://www.mychesco.com/?p=675472","excerpt":"The specialty alloys producer expects fiscal 2027 operating income of $850 million to $880 million, representing growth of 21% to 25% from fiscal 2026. Adjusted free cash flow is projected at $400 million to $430 million. Carpenter also established a fiscal 2029 operating income target of $1.2 billion to $1.3 billion, reflecting expected contributions from capacity expansion,","as_of":"2026-08-05","retrieved_at":"20261025","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"公司 10-K 揭露：部分不同產品在某些情況下可替代其成品。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm","excerpt":"Furthermore, a number of different products may, in certain instances, be substituted for our finished products.","as_of":"2026-08-12","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"公司 10-K 風險因子：較低成本替代材料持續可得，客戶可能轉用較低成本替代品，造成業績大幅波動。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm","excerpt":"In addition, continued availability of lower cost, substitute materials may cause significant fluctuations in future results as our customers opt for a lower cost alternative.","as_of":"2026-08-12","retrieved_at":"20261025","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 10-K 描述銷售仍經自家工廠、自有配銷網路與獨立經銷商，並維持自有全球服務／配銷中心與 JIT 備貨；文件未見通路或商業模式結構轉變的描述。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm","excerpt":"Our sales are distributed directly from our production plants and distribution network as well as through independent distributors. Unlike many other specialty steel producers, we operate our own worldwide network of service and distribution centers.","as_of":"2026-08-12","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"Latrobe Distribution 報告單位因客戶下單型態下滑，FY2024 Q3 認列 $14.1M 商譽減損（全數商譽），為舊事件，非 2026 通路轉型。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm","excerpt":"We determined the goodwill associated with the Latrobe Distribution reporting unit was impaired and recorded an impairment charge of $14.1 million during the third quarter of fiscal year 2024","as_of":"2026-08-12","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 FY2026 報告（2026-04-29）公司將 FY2026 營業利益 guidance 上調至 $700–705M（至少較 FY2025 +33%），調整後自由現金流約 $350M；Q2（2026-01-29）曾調至 $680–700M；搜尋未見下調。","source":"SEC 8-K / Carpenter Q3 FY2026 results (Seeking Alpha PR)","url":"https://seekingalpha.com/pr/20492339","excerpt":null,"as_of":"2026-04-29","retrieved_at":"20261025","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Tickflow 彙整（2026-08-01）：15 位分析師共識評級 Buy，共識目標價 $465.80，其引用價 $520.92，目標價低於當時價約 16.4%。","source":"Tickflow CRS forecast","url":"https://tickflow.io/stock/CRS/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261025","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"個別目標價分布：JPMorgan $700（Buy，2026-07-31）、KeyBanc $608（Buy，2026-08-03）、Wells Fargo $540（Hold）；Simply Wall St 敘事（2026-08）稱共識 $625.88、區間 $540–$700。各聚合站共識數字不一致。","source":"Investing.com CRS; Simply Wall St narrative","url":"https://www.investing.com/equities/carpenter-technology-corp","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261025","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"FY2026 10-K Item 3：僅有環保 PRP 與例行訴訟，管理層預期無重大不利影響；未列集體訴訟或 SEC 調查。","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm","excerpt":"Based on information currently available, the ultimate resolution of our known contingencies, individually or in the aggregate and including the matters described in Note 12 to the consolidated financial statements in this Form 10-K, is not expected to have a material adverse effect on our financial position, cash flows or results of operations.","as_of":"2026-08-12","retrieved_at":"20261025","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月18份8-K中僅1份含重大項目：2025-11-20 發行$700M 5.625%優先票據（Item 1.01），屬融資而非併購。","source":"SEC EDGAR 8-K 2025-11-20 Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/17843/000110465925114628/tm2531768d1_8k.htm","excerpt":"Carpenter Technology Corporation (the “Company”) completed its previously announced offer and sale of $700.0 million aggregate principal amount of 5.625% senior notes due 2034 (the “Notes”).","as_of":"2025-11-20","retrieved_at":"20261025","affects":["valuation"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K Item 3 僅載環保與例行訴訟，預期無重大影響；搜尋未見集體訴訟。","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm","excerpt":"Based on information currently available, the ultimate resolution of our known contingencies, individually or in the aggregate and including the matters described in Note 12 to the consolidated financial statements in this Form 10-K, is not expected to have a material adverse effect on our financial position, cash flows or results of operations.","as_of":"2026-08-12","retrieved_at":"20261025","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"CRS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":30.58,"operating_margin_pct":22.47,"fcf_margin_pct":11.6,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HWM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.03,"operating_margin_pct":27.31,"fcf_margin_pct":19.64,"rd_intensity_pct":0.41},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ATI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.36,"operating_margin_pct":15.19,"fcf_margin_pct":11.16,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MTRN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":16.01,"operating_margin_pct":6.35,"fcf_margin_pct":1.55,"rd_intensity_pct":1.23},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTRN","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"RS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":28.21,"operating_margin_pct":7.76,"fcf_margin_pct":3.41,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RS","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"CRS"},"financial_history":{"ticker":"CRS","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":2550300000.0,"revenue_yoy_pct":null,"gross_margin_pct":13.23,"operating_margin_pct":5.22,"net_income":56400000.0,"diluted_eps":1.14,"free_cash_flow":-67600000.0,"fcf_margin_pct":-2.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":2759700000.0,"revenue_yoy_pct":8.21,"gross_margin_pct":21.17,"operating_margin_pct":12.83,"net_income":186500000.0,"diluted_eps":3.7,"free_cash_flow":178300000.0,"fcf_margin_pct":6.46,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":2877100000.0,"revenue_yoy_pct":4.25,"gross_margin_pct":26.71,"operating_margin_pct":18.26,"net_income":376000000.0,"diluted_eps":7.42,"free_cash_flow":286100000.0,"fcf_margin_pct":9.94,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":3124200000.0,"revenue_yoy_pct":8.59,"gross_margin_pct":30.58,"operating_margin_pct":22.47,"net_income":529800000.0,"diluted_eps":10.52,"free_cash_flow":362300000.0,"fcf_margin_pct":11.6,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CRS/CRS_Q1_2027_Earnings_Call_20261022.md）

# Q1 2027 Earnings Call
**Carpenter Technology Corporation** | Earnings Calls | 2026-10-22

**Operator** (Operator):
Hello, everyone. Thank you for joining us, and welcome to the Carpenter Technology's First Quarter Full Year '27 Earnings Call. [Operator Instructions] I will now hand the conference over to John Huyette, Vice President, Investor Relations. Please go ahead.

**John Huyette** (Executives):
Thank you, operator. Good morning, everyone, and welcome to the Carpenter Technology Earnings Conference Call for the Fiscal 2027 First Quarter ended September 30, 2026. This call is also being broadcast over the Internet along with presentation slides. 
For those of you listening by phone, you may experience a time delay in slide movement. Speakers on the call today are Tony Thene, Chairman and Chief Executive Officer; and Tim Lain, Senior Vice President and Chief Financial Officer. Statements made by management during this earnings presentation that are forward-looking statements are based on current expectations. Risk factors that could cause actual results to differ materially from these forward-looking statements can be found in Carpenter Technology's most recent SEC filings, including the company's report on Form 10-K for the year ended June 30, 2026, and the exhibits attached to that filing. 
Please also note that in the following discussion, unless otherwise noted, when management discusses the sales or revenue, that reference excludes surcharge. When referring to operating margins, that is based on adjusted operating income, excluding special items and sales, excluding surcharge. 
I will now turn the call over to Tony.

**Tony Thene** (Executives):
Thank you, John, and good morning to everyone. I will start on Slide 4 with a review of our safety performance. We ended the first quarter with a total case incident rate of 1.7. We continue to invest in programs for employees with a focus on identifying potential risks and minimizing the severity of injuries. With our focus on leading indicators, we expect to see continued progress on our ultimate goal, a 0 injury workplace. 
Let's turn to Slide 5 for an overview of our first quarter performance. Our first quarter performance was a solid start to fiscal year 2027. The quarter's primary talking points fit into a tight simple narrative: one, record first quarter operating income, up 28% over the first quarter of last year. 
The record results were driven by productivity improvement, disciplined mix management and continued realization of pricing actions. 
Two, SAO segment adjusted operating margin matched the record from last quarter at 37.7%. This is an impressive feat with fewer operating days and increased preventive maintenance activity versus last quarter. 
And to be clear, we do not view this margin level as the peak as we expect strengthening demand, productivity and pricing actions to drive us to higher levels. 
Three, bookings continue to increase. Specifically, our bookings for customers in the commercial aerospace supply chain were up again sequentially and up 25% year-over-year. Importantly, the most talked about aerospace sub-markets, distribution and structural, were up 23% sequentially and 49% year-over-year. 
And aerospace engine bookings continue to increase sequentially. It's important to note that we and many others believe the industry is just at the beginning of this super cycle with even stronger demand anticipated in the coming quarters of fiscal year 2027 and beyond. 
As an extra data point, we have numerous customers who have confirmed that they are ordering at a level that doesn't even support current aerospace OEM build rates, let alone the projected future build rate increases the industry is planning for. This is an important point because it supports the fact that bookings will need to continue to increase significantly in the near future to support demand. 
Four, pricing continues to be a tailwind. With strengthening demand and an expanding supply-demand gap for nickel super alloys, our pricing for both LTA and non-LTA business remains elevated and consistently increasing. 
And five, strong financial targets for fiscal year 2027 and 2029 that we are focused on overachieving. More on that on my closing slide. That is the summary of the quarter's performance and current state of the business. All 5 primary areas of interest for our shareholders are currently flashing green and exhibit clear positive signals. 
Consistent record operating income performance, strong operating margins with levers to expand further, accelerating demand across key end-use markets, continuing benefit from pricing actions and an industry-leading financial outlook with opportunity to overachieve. 
Let me turn to Slide 6 and a closer look at first quarter sales and market conditions. In the first quarter of fiscal year 2027, our total sales, excluding raw material surcharge, were down 7% sequentially and up 5% year-over-year. As expected, the sequential sales decline was driven by the planned maintenance outages we discussed on the last earnings call. 
I will focus my comments today on the aerospace and defense end-use market as it accounts for the majority of our sales. Sales in the aerospace and defense end-use market were down 5% sequentially and up 10% year-over-year. Again, this sequential decline was expected and reflects the impact of our planned maintenance outages. 
For more submarket sales detail, I will share the following: Aero engine sales sequential change was a bit better than the overall aerospace and defense average. Aerospace fasteners was a bit worse, although it was the second highest sales quarter on record, second only to the previous quarter. 
Aerospace structural and distribution sub-markets was roughly flat to a strong previous quarter. And the defense submarket was down sequentially due primarily to lack of clear funding. I will talk more about this a bit later. It is important to note that at a time when the aerospace market is still only in the early stages of a large ramp and during a quarter where we had significant planned outages, we posted our second highest quarter of commercial aerospace sales on record and delivered a record first quarter operating income. 
As we build on this strong quarterly performance, let me provide you with some color on how we see the near-term future unfolding, how current bookings are taking shape and what our customers are telling us right now. 
Some have worried that macro events like the Iran conflict, increasing jet fuel prices and rising ticket prices will dampen travel demand and thus, the overall aerospace industry. But to date, the industry has been resilient as airlines are still reporting strong demand and air traffic is up 14% quarter-over-quarter. 
MRO activity is expected to continue to grow due to the overall demand environment, along with a large number of engines approaching their first shop visits. Airbus and Boeing continue to ramp production with backlogs now over 16,000 planes. That's more than 10 years of production. The industry is projecting approximately 1,400 to 1,500 new airplane builds in calendar year 2026, and they want to go higher with target rates above 2,100. 
That's a 50% increase above the current year rate, repeat, a 50% increase above the current year rate. So clearly, we are still in the early stages of this ramp with significant growth ahead of us. We do not have any customers talking to us about slowing down or about concerns over aerospace market growth in the future. 
Discussions are only about what pace of growth they will realize. A key development this week was the FAA approving the Boeing 737 MAX 10. This model is strategically important since it is the largest 737 variant and roughly 30% of Boeing's backlog. This provides another positive accelerant to the demand signal for the aerospace supply chain as production of this model ramps. Our quarterly bookings or order intake rate is an important indicator of the expanding growth. As I mentioned earlier, the aerospace distribution and structural submarket bookings were up 23% sequentially and 49% year-over-year. 
Our aerospace distribution customers in general are reporting that their backlogs are growing with incoming bookings exceeding billings. Their confidence is growing, and they see solid double-digit growth in calendar year 2027 and even higher growth rates in calendar year 2028.
Our aerospace engine bookings continue to increase, up 10% sequentially and 22% year-over-year. Our aerospace engine customers remain very busy and their demand outlooks for calendar years 2027 and 2028 continue to strengthen as OEMs increase ordering activity. 
In addition, we are receiving emergency orders in this submarket, and we expect those to increase as the supply chain ramps and the need for reliable material supply becomes even more critical. Aerospace fastener bookings were down sequentially as it is normal for quarterly bookings to be inconsistent in this sub-market. Our aerospace fastener customers continue to tell us that their activity has not yet fully caught up to current aircraft build rates, supporting further growth as ordering catches up with underlying demand. 
Turning last to the defense sub-market, where we see a stark contrast between end demand and our direct customer behavior. Bookings were down on a sequential and year-over-year basis. The disconnect between demand and supply chain activity is driven by funding challenges as our direct customers are not seeing the flow of funds required to place orders aligned with the Department of War needs. 
Given our position as a critical supplier across multiple defense programs such as the next-generation fixed-wing, rotary craft and missiles and munitions platforms, we have seen a significant uptick in direct engagement from the Department of War and OEMs as customers prepare for future needs. 
As an example, over the last quarter, the Navy selected Boeing to build its next-generation  F/A-XX fighter. We are already engaged with the supply chain on the design of critical elements for this fighter, and Carpenter Technology will support critical applications and have meaningful material content on this platform. 
Overall, the message is crystal clear. The defense industry will need significantly more material to support their goals. We, along with the industry, anticipate greater clarity post the midterm elections. Once budgets can be clarified, we anticipate a rush for material with significant emergency orders, driving significant growth in this submarket. 
It is clear from my comments that the key demand indicators, including higher bookings, growing customer backlogs and increasing urgency for material, all point toward continued demand acceleration across our highest value end-use markets. 
And in this accelerating demand environment, we remain focused on execution to realize the high-margin, high-growth profit opportunity ahead of us. I will take a closer look at our outlook on the last slide. But first, I will turn it over to Tim for a review of the financials.

**Timothy Lain** (Executives):
Thanks, Tony. Good morning, everyone. Starting with the income statement summary on Slide 8. Net sales, excluding surcharge, increased 5% year-over-year and declined 7% sequentially. The sequential decline primarily reflected planned first quarter downtime for preventative maintenance as we discussed last quarter. 
Improved productivity, product mix optimization efforts and pricing actions partially offset the impact of reduced operating time. Gross profit was $256.3 million, up 18% year-over-year and down 5% sequentially. Selling, general and administrative or SG&A expenses were $59.9 million, down $3.2 million year-over-year and down 2.1% sequentially, primarily due to lower variable compensation accruals. 
SG&A includes corporate costs of $26.1 million compared with $28.5 million in the fourth quarter of fiscal year 2026 and $26.6 million in the first quarter of fiscal year 2026. We expect second quarter fiscal year 2027 corporate costs of approximately $28 million to $29 million. 
Operating income was $196.4 million, up 28% year-over-year and down 5% sequentially. As Tony noted, this was a first quarter record and provides a strong foundation for the rest of fiscal year 2027. Our effective tax rate was 15.5%, similar to the first quarter of fiscal 2026, reflecting tax benefits associated with the vesting of certain equity awards. 
For fiscal year 2027, we expect the effective tax rate will be near the low end of our previously provided range of 20% to 22%. Diluted earnings per share for the first quarter were $3.25. Turning to our segment results, starting with SAO on Slide 9. First quarter net sales, excluding surcharge, were $573.5 million. 
Sales increased 7% year-over-year and declined 6% sequentially. The sequential decline reflected planned preventative maintenance downtime across our facilities, partially offset by mix management and pricing benefits. SAO's adjusted operating margin was 37.7%, consistent with the prior quarter's record. 
This is an impressive result given the lower available operating time that we typically see in our first fiscal quarter as a result of maintenance activities. From a trend perspective, we expect further margin expansion from productivity, mix and pricing. That said, margin may vary quarter-by-quarter depending on the mix of products that we ship in any given quarter. 
SAO reported first quarter operating income of $216.3 million. For the second quarter of fiscal 2027, we expect SAO operating income of $214 million to $218 million, in line with the first quarter. Our outlook reflects reduced production time during the holidays. 
As in prior years, we expect improved productivity and product mix optimization to partially offset the reduction in operating time. Turning to PEP on Slide 10. First quarter fiscal year 2027 net sales, excluding surcharge, were $83 million, down 5% year-over-year and 15% sequentially. 
Operating income was $7.3 million, slightly above our guidance compared with $7.1 million in the fourth quarter of fiscal year 2026 and $9.4 million a year ago. The year-over-year decline primarily reflected lower titanium sales into the medical end-use market, offset by strength in our additive business. 
We expect second quarter PEP operating income to be similar to the first quarter. Before turning to cash flow, let me summarize our second quarter fiscal year 2027 operating income outlook. We expect total operating income of $192 million to $197 million, which is largely in line with our strong first quarter results and implies growth of 24% to 27% compared to last year's second fiscal quarter. 
The total operating income estimate is comprised of SAO operating income of $214 million to $218 million, PEP operating income of approximately $7 million and corporate costs of approximately $28 million to $29 million. 
Turning to Slide 11 and our cash generation and capital allocation priorities. In the first quarter of fiscal year 2027, we generated $52.8 million of cash from operations and spent $77.7 million in capital expenditures that resulted in negative free cash flow for the quarter of $24.8 million. 
Significant cash generation is an important element of our ongoing growth story. We continue to focus our efforts on ensuring cash generation from increasing profitability as well as focused discipline on working capital management. As expected, capital spending remains elevated as we continue to fund our brownfield capacity expansion project. 
A brief update on our brownfield project. The expansion project remains on budget and on schedule for completion by the start of fiscal year 2028. Site activities are progressing well with major equipment installation underway. The project team remains focused on safely completing construction and equipment installation while preparing for a successful operational start-up. As we move through this year, we continue to anticipate generating between $400 million and $430 million of free cash flow in fiscal year 2027, which is an impressive outlook given that includes the elevated capital spending related to our capacity expansion investments. 
The cash generation enables our balanced capital allocation approach that combines investing in attractive accretive growth projects, including the brownfield capacity expansion with returning cash to shareholders. That is demonstrated by the $133.9 million of share repurchases during the quarter. 
As announced in August, these repurchases completed the prior $400 million authorization as well as purchases under the newly authorized additional $1 billion program. We also continued paying our long-standing quarterly dividend. Our strong balance sheet and liquidity support our capital allocation priorities. 
At quarter end, total liquidity was $658.6 million, comprised of $159.5 million in cash and $499.1 million in available borrowings under our credit facility. Our credit metrics remain very strong with net debt-to-EBITDA of 0.6x, and our capital structure is well positioned to allow significant flexibility with no debt maturities until 2034. 
Again, we believe our strong balance sheet, solid capital structure and outlook for significant cash generation positions us well to continue to invest in future growth as well as return significant cash to shareholders. With that, I'll turn the call back to Tony.

**Tony Thene** (Executives):
Thanks, Tim. As I mentioned in my earlier comments, the quarterly performance can be summarized into a tight positive narrative. Consistent record operating income performance, strong operating margins with levers to expand further, accelerating demand across key end-use markets and continuing benefit from pricing actions. 
I also noted an industry-leading financial outlook. For fiscal year 2027, we communicated strong financial targets just last quarter, but we are clearly focused on overachieving and are developing action plans to make that a reality. 
In fiscal year 2028, our brownfield capacity expansion project comes online, providing an additional accelerator to our earnings growth profile. And by fiscal year 2029, we expect operating income to reach approximately $1.2 billion to $1.3 billion. That's a 20%-plus CAGR over 3 years, a rate that we believe exceeds most in the industry. 
But again, our goal is to overachieve. And we do not view fiscal year 2029 as the peak of our earnings power. Altogether, we believe Carpenter Technology offers a uniquely attractive long-term investment opportunity. We are operating in an accelerating demand environment across many of the most attractive end-use markets in the world. 
And not only is demand accelerating, but the platforms that serve that demand, airplanes, medical implants, power generation, semiconductor fabrication, none of them can be built without Carpenter Technology. As a result, we have a clear path to significant earnings growth in the years ahead. 
Our strong and growing margin profile reflects the fact that our portfolio consists of highly specialized solutions, serving critical applications where performance matters, qualification cycles are long and the barriers to entry are significant. And our strong balance sheet and growing cash flow generation provide us with the flexibility to maintain a balanced and disciplined approach to capital allocation, investing in profitable growth opportunities and returning cash to shareholders. 
We remain committed to creating a meaningful long-term value for shareholders through disciplined execution, continuous improvement and profitable growth. Thank you for your time and continued confidence in Carpenter Technology.

**Operator** (Operator):
[Operator Instructions] Your first question from Andre Madrid with U.S. Bancorp BTIG.

**Andre Madrid** (Analysts):
Looking at -- you mentioned maintenance as being maybe one of the reasons that 1Q is a little weaker, but it seemed like some of that was already contemplated in your 1Q outlook. So I'm just trying to better understand maybe what are some of the other puts and takes that might have driven the miss.

**Tony Thene** (Executives):
Well, I think there are no other puts and takes. I mean the result was about 98% to 99% of the guidance that we gave. So you're only talking about a couple of million dollars, Andre, and that could come down to one customer unable to arrange a truck to be shipped on the last day of the quarter. That's how small this is what you're talking about. So I don't have a long list of items. We effectively came in at our guidance.

**Operator** (Operator):
Your next question from Gautam Khanna with TD Cowen.

**Gautam Khanna** (Analysts):
And I apologize, I missed the front of the call to the earnings day. But Tony, I just -- it sounded like nothing has changed in the demand environment, nothing has changed in the pricing environment and that your conviction in the '27 through '29 outlook is unchanged, right? I just want to make sure that was...

**Tony Thene** (Executives):
It has changed. I mean, it's stronger. My outlook on demand is stronger than it was a quarter ago. My outlook on pricing is stronger than it was a quarter ago. And my confidence in 2027 and 2029 is stronger than it was a quarter ago. So it has changed to the positive.

**Gautam Khanna** (Analysts):
Okay. And -- can you talk a little bit about productivity and kind of -- I know we don't have the tonnage disclosures, which is fine. I just I'm curious like anything directionally on capacity unlock, the ability to drive more throughput in the first quarter and then as we move through the year, like what you guys are expecting in terms of the ability to unlock because you're 24/7 all out at this point. I'm just curious what on that...

**Tony Thene** (Executives):
That's a good question. It's probably one of the most important questions. It's across the board. So there's not 1 item. I can't just work on 1 item. We're working on multiple areas of the plant. And as you well know, when you unlock one bottleneck, by definition, that creates another one that you go work, right? And you try to link them all together. So it was across the board. I mean, for SAO, to do 1/10 percentage point less than the record last quarter with less operating days and significantly more maintenance activity, you have to have that increased productivity to be able to maintain that. I mean that's actually an unbelievable level to be at that 37.7% in a month like we had. 
So very happy with what's going on, on the shop floor, but not satisfied. Of course, there's a next level and a level after that we can get to. And I would just say this, as you look and you get into Q3 and Q4, the demand signals that are out there, that's going to be even more tailwinds to push this margin percentage up. 
You're going to have significantly more volume coming across the assets and the price is going to continue to increase quarter-over-quarter.

**Gautam Khanna** (Analysts):
That's very helpful. Tony, also just if you could remind us on seasonal maintenance. You guys have been very proactive on doing -- pulling in maintenance throughout. But obviously, the September quarter has just a heavier load on that front. Is that unique to the quarter? And then just as we move forward, is there any perturbations you can call out now that we should be aware of, whether it's maintenance or other things? Yes.

**Tony Thene** (Executives):
Yes, the key is it's nothing special about the first quarter. That's just when we usually set up our maintenance schedules. And it usually Gautam isn't one large piece of equipment out for a long period of time. You just can't afford that in today's demand environment. So what you have are a lot of smaller maintenance projects all hooked together, and that's what you saw in the first quarter. 
You're going to continue to see that type of preventive maintenance throughout the year. My guess right now is none of those events will be as large as the one you saw in Q1.

**Gautam Khanna** (Analysts):
That makes sense. And just given the stock is acting kind of odd as many aerospace stocks these days, how do you prioritize capital allocation from here? Obviously, you guys have been doing buybacks. Just how do you think the Board will respond to those?

**Tony Thene** (Executives):
Well, without being too exact, I agree with you. I think right now, there's a major negative sentiment that's emerged over the last couple of months in the aerospace market. I can't really speak to that, Gautam, because I've not found 1 person that can explain exactly to me what they're negative on. 
And my guess is you probably wouldn't be able to explain that to me either. But I think my prepared remarks set out a pretty strong near-term future, let alone FY '27, near-term positive future. With that said, to specifically answer your question, we're going to continue to fund the brownfield. And certainly, at these levels, we'll remain active in the repurchase program.

**Operator** (Operator):
Your next question from Scott Deuschle with Deutsche Bank.

**Scott Deuschle** (Analysts):
Tony, can you provide an update on where the backlog stands today relative to the start of the calendar year?

**Tony Thene** (Executives):
Without giving a specific number, Scott, it is continuing to increase across all of our end-use markets.

**Scott Deuschle** (Analysts):
And then have you placed much of the brownfield capacity on contract at this point? Or are you still waiting to contract that out?

**Tony Thene** (Executives):
Well, we don't contract out specific pieces of equipment. So if you look at the demand profile going forward, that volume will be absorbed immediately as it comes online.

**Scott Deuschle** (Analysts):
Okay. And then lastly...

**Tony Thene** (Executives):
It will be absorbed by our current -- sorry, it will be absorbed by our current LTAs, right? All of our LTAs, they'll be wanting more material. So that's not -- I don't contract out specific equipment to specific customers.

**Scott Deuschle** (Analysts):
Right. Okay. And then I guess maybe on that point, can you comment on the share position that you've been securing on new aerospace LTAs and how that share position is or is not changing relative to the contracts that they are replacing and renewing?

**Tony Thene** (Executives):
Well, I can tell you this, all of them are higher. Every 1 of the customers that we're dealing with, and we just completed 2 aerospace -- significant aerospace LTAs this past quarter, the first quarter. And every customer to a T wants more material.

**Scott Deuschle** (Analysts):
Is the share percentage higher? Or is the volume commitment is higher?

**Tony Thene** (Executives):
Well, I don't know which one comes first, right? I mean the volume is higher, right? There's only a couple of players in the market, and they're going to need all that material. So I mean, the volume is significantly higher. The shares are probably going to remain pretty well the same. There's not a share gain battle going on.

**Operator** (Operator):
Your next question from the line of Josh Sullivan with JonesTrading.

**Joshua Sullivan** (Analysts):
The structural distribution market, what's your sense of their inventory levels? Are there any metrics you can share with us relative to current or projected build rates? Just trying to get a sense of as you see this order flow, what their restocking cycle kind of looks like from your perspective here?

**Tony Thene** (Executives):
Well, Josh, I will tell you this that the majority, if not all of the customers in that submarket are reporting decreasing inventories. And that aligns them very -- now all of them will be at different points in time. I'm not suggesting that every customer is the same. But they're, for the most part, all reporting decreasing inventories, and that is the direct correlation to seeing the increased bookings. 
I think the good news is that those bookings are going to have to continue to increase significantly, as I said in my remarks. There is no choice when it comes to that. So I think going forward over the next couple of quarters, a very positive outlook when it comes to those 2 sub-markets.

**Joshua Sullivan** (Analysts):
And I guess another sub-market on the defense market, just given the impetus to restock various inventories, and I think you had talked a little bit about emerging demand, but what does that more urgent order flow look like near term?

**Tony Thene** (Executives):
Well, I was not being -- I was not exaggerating when I said that I thought there would be a rush of material orders once there's some type of clarity around the budget. And I say that because of the discussions that we have with the Department of War, whether that be with the Navy, the Air Force, the Army, that demand is significant. 
The real issue is that the Department of War doesn't place orders. There's multiple companies in the supply chain that place those orders, and they don't have that funds flow to be able to do it. There's not one person in the defense supply chain that doesn't believe they should be placing orders right now. 
But the way that the budget works, that's just not possible for them to do right now. Once that clears up, I think saying that there will be a rush on orders will be an understatement.

**Operator** (Operator):
Your next question from the line of Bennett Moore with JPMorgan.

**Bennett Moore** (Analysts):
I wanted to -- it's great to see the bookings continue to move in the right direction. I appreciate your comment around incremental confidence in the '27 guide. But I'm just hoping you could frame looking specifically at structural activity and some of the dislocation on the defense side, how do these compare relative to the assumptions you have in that '27 guide?

**Tony Thene** (Executives):
Yes, Ben, I will say it this way. Based on that FY '27 guide, I believe that there is upside in volume, productivity and pricing versus the assumptions that we used when we gave that guidance 3 months ago.

**Bennett Moore** (Analysts):
All right. Understood. And then a quick housekeeping, if I could. Just on the working capital, the use was a bit bigger than we expected. I see the guide for free cash flow was maintained. So just wondering if this is largely a function of the planned outage or if there's anything else we should consider looking ahead?

**Timothy Lain** (Executives):
Yes. Ben, this is Tim Lain. I think it's more of a function of timing. So we did build some inventory in Q1. As we progress through the year, we've got more available days in the back half of the year. It's a historical trend. We'll burn that inventory off. So as we progress through the year, we should see cash flow continue to accelerate. 
CapEx might be a little bit higher in the second half as we ramp up and trying to finish the project later this year. But in general, based on the guidance we gave, the cash has to accelerate here in Q2 and then even more in the second half.

**Operator** (Operator):
Your next question from the line of David Strauss with Wells Fargo.

**David Strauss** (Analysts):
Tony, any comment kind of the volume versus price algorithm that came through in the Q1 revenue for -- kind of in total and more specifically on the aero side?

**Tony Thene** (Executives):
Well, I can tell you that price continues to increase quarter-over-quarter. The LTAs that we just signed higher price. We've got one that sits right now agreement in principle, higher price. We're working on a couple of other major ones as we speak. Both will be higher priced than before. 
I think it's -- David, it's illogical to think that the price would be lower. I mean demand is accelerating, not declining, and there's no more capacity coming online other than our brownfield and a couple of others that there's no way that we'll keep up with that. So the pricing story seems pretty straightforward to me.

**David Strauss** (Analysts):
Okay. Yes. I mean I was just looking if you kind of took the overall kind of revenue growth ex surcharge, was it 2/3 volume, 1/3 price or any -- in terms of the upside year-over-year there, any sort of color there?

**Tony Thene** (Executives):
No, no. I see what you're saying. I mean, obviously, we stopped giving volume this quarter. So I'm not going to then start giving it on the Q&A. But obviously, you think that you got a Q1 with less operating days, right? Versus Q4, which is usually your biggest one. 
But I don't have a volume problem or a volume challenge. I mean we're running, in many cases, the majority of our equipment as full as we can. So I don't have a volume problem. Now the issue that you have, David, is that volume isn't generic and it's not 100% fungible, right? So there are different products that use different pieces of the plant capacity. Having defense be a bit light, maybe the word a bit light isn't the right word, being light, that causes some challenges for us because we have to move some things around. That's some -- that's volume from the defense side that we would have run. 
Now we're not, right? So we moved some things around. So that can be some give and take based on what we decide to run there. But in totality, the volume is going to be there. And it's even going to be stronger as we get out over the next couple of quarters.

**David Strauss** (Analysts):
Okay. And maybe any comments on medical and energy, those end markets, I think you had talked last call, it seemed like you were a bit optimistic that we would start to see improvement kind of in those categories. What's the -- kind of what did you see in Q1? And how are you thinking about those 2 end markets from here?

**Tony Thene** (Executives):
Yes. I mean thanks for the question. Sometimes we forget about that. Medical is going to continue to perform for us. I mean, I should say not continue to perform, continue to increase. It's really one specific subset inside of medical that has lagged a bit. Procedures are up. We make products that provide our customers a solution that they can't get anywhere else. 
So I think that's -- we will see that continue to increase over the next couple of quarters. I'm not overly worried with medical, and it's not driving down my overall performance. Energy, interesting, small piece of my overall revenue, but certainly on the IGT side has been very strong. 
And I would anticipate that to remain strong going forward. We have a very small oil and gas business even, David, that's been relatively weak, I would say, that we see coming back a little bit here now in this quarter and the next couple of quarters. So overall, for those 2 markets in total, again, much smaller than aerospace, but both, I would say, with some positive tailwinds.

**Operator** (Operator):
[Operator Instructions] Your next question from the line of Andre Madrid with U.S. Bancorp BTIG.

**Andre Madrid** (Analysts):
I don't know what happened there, but I appreciate the response to the first question. I guess I want to follow up on that by maybe asking a bit more about LTA mix. I know it seems like you guys might have re-signed some new ones recently. Just should we be expecting the LTA mix to kind of start trending upward again, locking in some favorable pricing? Or how should we be thinking about that?

**Tony Thene** (Executives):
Let me make sure I understand your question. What do you mean by when you say the LTA trending upward?

**Andre Madrid** (Analysts):
Like the mix of business that's driven through LTAs, do you expect that to continue to grow through the end of the decade? Are you guys like starting to kind of lock in some more favorable pricing? Or is it going to kind of stay where it's at for the time being?

**Tony Thene** (Executives):
Yes. So a couple of questions in there. Of course, the pricing is going to be higher, Andre. As I said earlier, it would be illogical for it not to be in the current environment. But from a total percent of our total portfolio, I would say it's going to be relatively the same, right? Volume is increasing. And the LTAs that we are renewing are primarily with existing customers. The majority of our aerospace business is under LTA now.

**Andre Madrid** (Analysts):
Yes. Yes. No, that's clear. No, I appreciate that. And then I guess if I could just squeeze one more in. I mean, looking specifically at the engine aftermarket, I know you talked about it already a little bit, but there has been some concern, broadly speaking, across commercial aero on the effect of maybe higher fuel prices. 
It doesn't seem like some of your peers and downstream customers have been seeing it affecting demand yet. It seems to be the same case for you. But I guess just what specifically are you seeing in engine aftermarket that might inspire some more confidence that demand will persist?

**Tony Thene** (Executives):
Well, we've never seen the dropoff of it. So I understand some of that negative sentiment out there. We have not seen it, and we have not heard that from any of our customers.

**Operator** (Operator):
Your next question from Chuck Minervino with Susquehanna.

**Charles Minervino** (Analysts):
I was wondering if you could elaborate a little bit on your comments that you have some actions and projects you're working on that could exceed the operating income targets for fiscal '27 and 2029. So I was just wondering if you could provide a little bit more detail on some of the levers you could pull there to maybe unlock some of that.

**Tony Thene** (Executives):
Well, welcome, Chuck. Think about the 3 big buckets. Number one, volume, I think, has the opportunity to be higher than what we thought it would be a quarter ago, just because of the ordering patterns. We just talked about the pent-up demand in defense. That is a balloon that is ready to burst, right? I mean the demand is increasing and increasing and the orders aren't there. 
So I think that's going to be a significant -- or could be a significant tailwind from a volume standpoint. And then across the rest of the aerospace supply chain, we know customers have told us they are ordering today at a rate that doesn't even support the current build rates for Boeing and Airbus. So we know that's going to have to come back, and we sense that, that will be in the near term. 
So I think volume can be an upside. What we've seen with our current work now in LTAs, the pricing potentially can be an upside as well. And then on productivity, yes, there's multiple areas that we continue to drive productivity through our use of AI in many cases that we've been able to unlock faster and I would say, in a greater quantity than we had originally planned. 
So all 3 of those buckets, Chuck, are going to contribute to us potentially beating that FY '27 guidance. And remember, I mean, it doesn't take a huge percentage increase, for example, in price or in volume to exceed that guidance. So it's all -- it's not easy, but it's all doable.

**Charles Minervino** (Analysts):
Got it. And if I could just ask one more. Could you talk a little bit about your kind of outlook on margins in SAO, maybe this year, but also kind of beyond this year and where some of the levers may be to expand margins in that segment?

**Tony Thene** (Executives):
Yes, it's a good question. And it's almost -- I can give you the same answer I gave to you about how do you increase -- overachieve on FY '27, right? The margins are going to be driven by increased volume, pricing, we believe, is a tailwind and then also productivity. So we'll be working all 3 of those, right? As you're able to run your plant at higher and higher utilization levels and find more and more output available to you, that's a direct uplift to the margin. 
So we have to be careful. Everybody, obviously, a lot of concern over going down 0.1 percentage point in SAO in a quarter that they have significant preventive maintenance and less operating days. I'll have a hard time understanding that one. So you will have some of that variability quarter-to-quarter. But if you look over the long term, certainly, the opportunity for us to continue to increase SAO margins is clearly there.

**Operator** (Operator):
This concludes our Q&A session. I will now turn the call back to John Huyette for closing remarks.

**John Huyette** (Executives):
Thank you, operator, and thank you, everyone, for joining us today for our fiscal year 2027 first quarter conference call. Have a great rest of your day.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CRS_Q4_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO｜guidance：FY27 Q1 總營業利益財測 1.95–2.00 億美元（原話："operating income of $195 million to $200 million."）
- 2026-07-30｜CFO｜guidance：SAO 部門 FY27 Q1 營業利益財測（原話："income in the range of $218 million to $222 million."）
- 2026-07-30｜CEO｜guidance：FY27 全年營業利益財測（原話："we expect between $850 million"）
- 2026-07-30｜CEO｜guidance：FY29 營業利益目標區間（原話："approximately $1.2 billion to $1.3 billion"）
- 2026-07-30｜CEO｜guidance：FY27 調整後自由現金流財測（原話："we anticipate between $400 million and $430 million of"）
- 2026-07-30｜CFO｜guidance：FY27 Q1 公司費用預期約 2,900 萬（原話："corporate costs of approximately $29 million."）
- 2026-07-30｜CEO｜guidance：管理層對訂定目標的原則（原話："We believe in setting targets"）
- 2026-07-30｜CEO｜guidance：CEO 表示 FY27 財測可視為下限（原話："if you want to consider FY '27 to floor, you won't"）
- 2026-07-30｜CEO｜guidance：CEO 稱 FY29 不是獲利高點（原話："do not believe fiscal year 2029 represents the peak"）
- 2026-07-30｜CEO｜guidance：CEO 預期 FY27 航太明顯更高（原話："we see aerospace being meaningfully higher in FY '27."）
- 2026-07-30｜CFO｜margin：SAO 調整後營業利益率連續第 18 季上升至 37.8%（原話："consecutive quarter to a new record level of 37.8%."）
- 2026-07-30｜CFO｜margin：管理層說明每磅均價受產品組合影響（原話："is highly dependent on the mix of products."）
- 2026-07-30｜CFO｜margin：低價產品毛利水準相當（原話："the lower-priced products often come with comparable"）
- 2026-07-30｜CEO｜margin：CEO 稱 SAO 利潤率不會停在此處（原話："I can tell you now, this isn't the floor for us."）
- 2026-07-30｜CFO｜margin：Q4 有效稅率較低來自一次性稅務利益（原話："discrete tax benefits associated with certain equity awards."）
- 2026-07-30｜CFO｜commitment：擴產案進度與預算（原話："expansion remains on budget and on schedule to be completed"）
- 2026-07-30｜CFO｜commitment：擴產案預計 2030 年增量營業利益約 1.5 億（原話："roughly $150 million of incremental OI."）
- 2026-07-30｜CFO｜commitment：管理層對 1.5 億數字信心提高但維持不變（原話："it's fair to say that we are more confident in those"）
- 2026-07-30｜CEO｜commitment：CEO 解釋不調高 1.5 億的理由（原話："we're not 100% sure of the exact mix of those products."）
- 2026-07-30｜CEO｜commitment：CEO 回任，非過渡，不外找新任 CEO（原話："this is not an interim assignment, and we are not launching"）
- 2026-07-30｜CFO｜capital_allocation：回購累計額度使用情形（原話："the total to $281 million spent to date against the"）
- 2026-07-30｜CEO｜capital_allocation：資本配置哲學不變（原話："allocation philosophy remains unchanged."）
- 2026-07-30｜CEO｜capital_allocation：併購並非排除但排序較低（原話："That's not a no, but it's just a tough one"）
- 2026-07-30｜CEO｜capital_allocation：回購與股息持續（原話："We're always going to have the dividend."）
- 2026-07-30｜CFO｜capital_allocation：資本支出節奏全年平均（原話："it would be fairly ratable throughout the year."）
- 2026-07-30｜CFO｜capital_allocation：自由現金流轉換率 85–90%（原話："we can hit that 85% to 90% type conversion ratio"）
- 2026-07-30｜CEO｜customer：波音預期月產率 47 架（原話："Boeing stated that they expect to achieve rate 47 per month"）
- 2026-07-30｜CEO｜customer：部分結構件客戶下單仍謹慎（原話："structural customers remain cautious in their ordering"）
- 2026-07-30｜CEO｜customer：引擎客戶稱產能比需求更受關注（原話："than the capacity needed to meet that demand."）
- 2026-07-30｜CEO｜customer：結構件成長可能領先（原話："the growth in structural will lead the pack"）
- 2026-07-30｜CEO｜customer：航太緊固件銷售成長（原話："They were up 10% sequentially, 12% year-over-year."）
- 2026-07-30｜CEO｜customer：航太新合約客戶要求更多材料（原話："they ask for more and more material. Not less."）
- 2026-07-30｜CEO｜customer：交期大致穩定，部分產品拉長（原話："lead times are relatively consistent quarter-over-quarter."）
- 2026-07-30｜CEO｜customer：長約將有重大合約待續約（原話："there are a couple of very significant contracts that will"）
- 2026-07-30｜CEO｜customer：仍有疫情前條款長約（原話："yes, there's still 1, maybe 2 that's pre-COVID."）
- 2026-07-30｜CEO｜product：醫療終端本財年首度季增（原話："medical end-use market sales were up sequentially."）
- 2026-07-30｜CEO｜product：IGT 能源銷售季間波動（原話："sales for IGT material will fluctuate due to order timing"）
- 2026-07-30｜CEO｜product：工業消費由半導體帶動（原話："demand from the semiconductor industry, where our"）
- 2026-07-30｜CEO｜product：Dynamet 占比小但視為策略資產（原話："SAO is 95% plus of our segment"）
- 2026-07-30｜CEO｜competition：太空需求可能與航空引擎合金爭用產能（原話："space could potentially compete with aero engine alloys."）
- 2026-07-30｜CEO｜risk：結構件客戶謹慎、低於預期需求下單（原話："structural customers remain cautious in their ordering"）

### 問答異常語氣（迴避／改口／保留）
- CRS_Q4_2026_Earnings_Call_20260730.md｜問：Deutsche Bank 問為何 FY27 財測隱含 EBIT 成長放緩｜答法：CEO 不反駁，改說財測可視為下限，未解釋放緩原因
- CRS_Q4_2026_Earnings_Call_20260730.md｜問：Wells Fargo 問 SAO 增量利潤率｜答法：CEO 拒絕預測季度利潤率，僅稱非下限、等數季後再看，未給數字
- CRS_Q4_2026_Earnings_Call_20260730.md｜問：BTIG 問 FY29 目標隱含的利潤率高點｜答法：CEO 以玩笑帶過，不給模型利潤率
- CRS_Q4_2026_Earnings_Call_20260730.md｜問：TD Cowen 問長約續約占比｜答法：CEO 明言不給確切百分比，只說有幾個大型合約
- CRS_Q4_2026_Earnings_Call_20260730.md｜問：Deutsche Bank 問 2030 年 1.5 億是否偏低｜答法：CFO 稱信心提高、可能更高，但仍維持 1.5 億，未給新數字

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
{"date":"20260901","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"SAO 調整後營益率維持 ≥33% 為結構性新常態（非景氣頂峰）","columns":{"2Y 驗證點":"FY27-28 TTM 維持 34-38%","5Y 驗證點":"FY31 Athens 全貢獻後仍 ≥32%","10Y 驗證點":"FY35 跨週期均值 ≥26%","數字門檻":"連 2 季 TTM &lt;33%＝削弱；連 4 季 &lt;30%＝反轉","來源":"Q4 FY26 法說（2026-07-30）；連 18 季擴張紀錄","漂移觸發":"連 2 季 TTM &lt;33%"}},{"id":"H2","text":"航太 A&amp;D 需求動能持續至少到 FY28-29（16,000 架積壓訂單支撐）","columns":{"2Y 驗證點":"Boeing 737 MAX 達 47/月並邁向 52/月；Airbus A320neo 邁向 70-75/月","5Y 驗證點":"FY31 A&amp;D 占營收仍 ≥65%，訂單金額維持正成長","10Y 驗證點":"2035 前窄體機積壓不低於 8,000 架","數字門檻":"連 2 季訂單轉負＝削弱；連 3 季負成長＝反轉","來源":"Q4 FY26 法說；Boeing/Airbus 公開產能指引","漂移觸發":"連 2 季訂單轉負"}},{"id":"H3","text":"Athens AL 擴產（$400M，+9,000噸／+7%）如期於 FY2028 初商轉，且 2030 貢獻增量營益 $150M+","columns":{"2Y 驗證點":"FY27 法說持續確認 on schedule/on budget","5Y 驗證點":"FY30 增量營益達成或超過 $150M 目標","10Y 驗證點":"2030+ 新產能在下一輪週期谷底仍守 ≥60% 稼動率","數字門檻":"延後 &gt;6 個月＝削弱；成本超支 &gt;20%＝削弱","來源":"Q4 FY26 法說：「12 個月後上線」，capex $242.7M FY26 已投入","漂移觸發":"延後 &gt;6 個月"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Boeing 新一輪品質/FAA 介入事件，737 MAX 月產無法邁向 47→52 目標","columns":{"對應假設":"H2","時間尺度":"⚡ 短期","監測指標":"Boeing 月度交付數據＋FAA 公告","警戒閾值":"連 2 季月產 &lt;38 架削弱；連 3 季 &lt;35 架或再遭限產反轉"}},{"id":"R2","text":"ATI Bakers South VIM（2027H2 投產，9,000 噸、80% 已鎖 LTA）上線後產業提價紀律鬆動，CRS 續約 LTA 提價幅度縮小","columns":{"對應假設":"H1","時間尺度":"🔥 中期","監測指標":"CRS 逐年 LTA 續約提價幅度、SAO 定價事件帳","警戒閾值":"續約提價降至個位數且連 2 次＝削弱；出現折價續約＝反轉"}},{"id":"R3","text":"下一輪航太週期反轉（歷史前例 FY22-23，GAAP 曾轉虧），疊加 Athens 產能適逢景氣谷底上線稀釋利潤率","columns":{"對應假設":"H1+H2","時間尺度":"🐢 長期","監測指標":"全球商用機積壓訂單總量、Boeing/Airbus 訂單淨額","警戒閾值":"積壓訂單/交付比從 ~10 年降至 &lt;6 年開始減倉；&lt;4 年大幅減倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已進場核心角色，無rearm觸發；加碼觸發見§13b","irr_base_pct":8.4,"ev5y_pct":34.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.7,"ev5y_pct":34.7,"irr_base_pct":8.4,"max_dd_pct":-68.0,"bull_5y_price":1056.0,"bear_5y_price":187.5,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"已進場核心角色，無rearm觸發；加碼觸發見§13b","price_at_dd":476.42,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRS_20261025/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
