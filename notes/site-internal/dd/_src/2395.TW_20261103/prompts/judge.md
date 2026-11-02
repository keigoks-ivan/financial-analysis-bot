你是 stock-analyst **v20 判斷 agent**，標的 2395.TW（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"2395.TW","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2395.TW_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2395.TW_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP，合併）","value":32.44,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"十億 NT$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.advantech.com/en/resources/news/advantech-reports-3q26-eps-of-nt715"},"note":"未查得"},{"id":"f_kpi1_gaap_non_gaap","label":"營業利益／利益率（GAAP；研華不另報 Non-GAAP）","value":6.795,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"十億 NT$（利益率約 20.9%，自新聞稿數字推算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.advantech.com/en/resources/news/advantech-reports-3q26-eps-of-nt715"},"note":"未查得"},{"id":"f_kpi2","label":"毛利／毛利率","value":36.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%（毛利 11.896 十億 NT$，推算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.advantech.com/en/resources/news/advantech-reports-3q26-eps-of-nt715"},"note":"未查得"},{"id":"f_kpi3_eps","label":"稅後淨利／EPS","value":7.15,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"NT$ EPS（淨利 6.218 十億 NT$）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.advantech.com/en/resources/news/advantech-reports-3q26-eps-of-nt715"},"note":"未查得"},{"id":"f_kpi4_b_b_ratio","label":"訂單出貨比（B/B ratio）","value":1.64,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"x","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.advantech.com/en/resources/news/advantech-reports-3q26-eps-of-nt715"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_2395_tw_gross_margin_pct","label":"2395.TW 毛利率","value":39.0,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2395.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2395_tw_operating_margin_pct","label":"2395.TW 營業利益率","value":17.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2395.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2395_tw_fcf_margin_pct","label":"2395.TW FCF 利潤率","value":1.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2395.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6414_tw_gross_margin_pct","label":"6414.TW 毛利率","value":20.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6414.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6414_tw_operating_margin_pct","label":"6414.TW 營業利益率","value":5.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6414.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6414_tw_fcf_margin_pct","label":"6414.TW FCF 利潤率","value":4.29,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6414.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6166_tw_gross_margin_pct","label":"6166.TW 毛利率","value":35.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6166.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6166_tw_operating_margin_pct","label":"6166.TW 營業利益率","value":9.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6166.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6166_tw_fcf_margin_pct","label":"6166.TW FCF 利潤率","value":6.66,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6166.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3088_two_gross_margin_pct","label":"3088.TWO 毛利率","value":33.62,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3088.TWO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3088_two_operating_margin_pct","label":"3088.TWO 營業利益率","value":11.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3088.TWO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3088_two_fcf_margin_pct","label":"3088.TWO FCF 利潤率","value":3.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3088.TWO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2397_tw_gross_margin_pct","label":"2397.TW 毛利率","value":25.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2397.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2397_tw_operating_margin_pct","label":"2397.TW 營業利益率","value":6.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2397.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2397_tw_fcf_margin_pct","label":"2397.TW FCF 利潤率","value":-1.44,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2397.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":655.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"TWD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":93.22,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^TWII","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":45.25,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.87 → 19.87）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_tw_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.77 → 23.77）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_tw_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（28.01 → 28.01）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_tw_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":19.87,"period":"2026-10-31","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_tw_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":23.77,"period":"2026-10-31","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_tw_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":28.01,"period":"2026-10-31","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_tw_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":41.69,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.9,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.78,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":34.22,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 19.87，分子＝快照價 680.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.704,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-10921.35,"period":"2026-11-03","unit":"TWD m","basis":"yfinance 最新一季：總債務 7168.83、現金 18090.18（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":872.08,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":560292.06,"period":"2026-11-03","unit":"TWD m","basis":"市值 571213.41 ＋ 淨負債 -10921.35","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":103736.7,"period":"2026-11-03","unit":"TWD m","basis":"yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":123165.87,"period":"2026-11-03","unit":"TWD m","basis":"yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":5.4,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 680.0 / W52 448.02 / W104 391.86 / W250 343.79 / W250 13週斜率 1.78%"},{"id":"f_ma_w52","label":"52 週均線","value":448.02,"period":"2026-11-03","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":391.86,"period":"2026-11-03","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":343.79,"period":"2026-11-03","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.78,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Morningstar 公司報告稱研華在全球工業電腦市場市占逾 40%（靜態數字，無 2026 消長方向）","source":"Morningstar Advantech Co Ltd 2395","url":"https://www.morningstar.com/quotes/0P0000C217","excerpt":"The company owns more than 40% share of the global industrial personal computer market and is a leading supplier of embedded boards.","as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"研華總經理稱較成熟、商品化市場的客戶對漲價較難接受，後續可能影響接單","source":"經濟日報 研華法說報導","url":"https://www.ctee.com.tw/news/20260806701105-430201","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"114年年報「主要銷貨客戶」表：113年與114年皆無單一客戶占銷貨淨額10%以上，全部列為「其他」，各占100%（114年銷貨淨額70,882,362仟元、113年59,786,293仟元），與發行人無關係。","source":"公開資訊觀測站電子書件 114年股東會年報 主要銷貨客戶表（PDF第127頁）","url":"https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id=2395&year=115&seamon=&mtype=F&dtype=","excerpt":"1  其他(註) 59,786,293  100.00  無  其他(註) 70,882,362  100.00  無","as_of":"2026-05-08","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026/8/5 法說：研華預期第三季營收優於第二季、年增季增雙成長，全年AI相關營收占比目標突破30%；第二季B/B值1.44","source":"中央社 AI需求推升動能 研華估第3季營收雙增、毛利率持穩","url":"https://www.cna.com.tw/news/afe/202608050294.aspx","excerpt":"AI需求推升動能 研華估第3季營收雙增、毛利率持穩","as_of":"2026-08-05","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"研華北美區前8月B/B約2.15（整體約1.4），北美廠區產能滿載、供不應求，預期延續至2027年下半年","source":"鉅亨網轉載/uanalyze 研華北美市場BB值逾2 產能供不應求爆滿到明年下半年","url":"https://uanalyze.com.tw/articles/9291755901","excerpt":"研華北美市場BB值逾2 產能供不應求爆滿到明年下半年","as_of":"2026-09-30","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"法說提及DDR4與SSD等零組件漲幅劇烈，預估第三季毛利率與營業利益率維持第二季水準；零售業務因客戶對漲價敏感放慢換機而持平","source":"中央社 2026-08-05 法說報導（搜尋摘要）","url":"https://www.cna.com.tw/news/afe/202608050294.aspx","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"公平會處分書及決議書資料庫以「研華」全文搜尋 0 筆，無任何處分或決議提及。","source":"公平交易委員會 處分書及決議書全文搜尋","url":"https://www.ftc.gov.tw/internet/main/decision/decisionList.aspx?mid=11","excerpt":"以關鍵字「研華」全文搜尋（查詢日 2026-11-03）共 0 筆。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"證交所 ESG 揭露：研華報告年度 114 因反競爭行為法律訴訟造成的金錢損失為 0。","source":"證交所 OpenAPI t187ap46_L_20","url":"https://openapi.twse.com.tw/v1/opendata/t187ap46_L_20","excerpt":"報告年度 114，因與反競爭行為條例相關的法律訴訟而造成的金錢損失總額(仟元)＝0.000。","as_of":"2026-11-02","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"研華財務長表示原則上將關稅成本轉嫁客戶，出貨屬資通訊產品仍在對等關稅豁免清單，232半導體調查結果尚未出爐難評估影響","source":"中央社 研華：匯率與關稅風險可控 邊緣AI占比今年拚2成","url":"https://www.cna.com.tw/news/afe/202508060211.aspx","excerpt":"（中央社記者吳家豪台北6日電）工業電腦廠研華今天召開法人說明會，財務長暨綜合經營管理總經理陳清熙表示，下半年匯率應該會趨於穩定，關稅有點不確定性，原則上會以轉嫁成本給客戶為主、少數協商，匯率與關稅兩項因素大致上可控；他預估，邊緣AI應用營收占比今年底將突破20%。 陳清熙表示，雖然美國232條款半導體調查結果還沒出爐，難以評估影響，但研華出貨屬於資通訊產品，目前仍在對等關稅豁免清單上。","as_of":"2025-08-06","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"研華與美國客戶討論關稅轉嫁機制及價格調整，並以空運分批出貨因應","source":"中央社 2025-04-07","url":"https://www.cna.com.tw/news/afe/202504070303.aspx","excerpt":"為因應川普對等關稅影響，工業電腦廠研華持續與美國客戶溝通，討論關稅轉嫁機制及價格調整。圖為研華內湖總部。（中央社檔案照片） （中央社記者吳家豪台北7日電）工業電腦大廠研華整體營運表現回升，今天公布3月合併營收新台幣63.23億元，月增19.42%，年增25.61%，為近2年單月新高；第1季合併營收173.51億元，年增25.02%。研華正與美國客戶討論關稅轉嫁機制及價格調整，且有少量產品改用空運搶時效。","as_of":"2025-04-07","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"研華三大製造中心位於台灣林口、中國昆山、日本福岡","source":"研華2023 ESG報告書 ch2","url":"https://advcloudfiles.advantech.com/csr/Report/2023ESG_ch2.pdf","excerpt":"三大生產製造中心位於台灣林口、中國昆 山及日本福岡，並建構四大運籌管理物流中心及 21 個 在地服務中心，以完整的服務體系提供全球客戶即時、 全方位之整合服務。 研華及關係企業專注工業電腦相關產品製造、組裝、 銷售及售後服務（詳 2.1.2 組織圖），主要事業群包 含：工業物聯網事業群、嵌入式物聯網平台事業群、","as_of":"2024-06-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"研華2026-2030全球擴張計畫，擴建美國、日本、台灣製造基地，合計投資逾82億元","source":"TechNews 財經","url":"https://finance.technews.tw/2026/09/11/advantech-nt-8-2-billion-expansion/","excerpt":"疫情期間，研華曾被大客戶催促赴墨西哥設廠，卻在評估後，決定資源投注需求最強的美國，以及鄰近台積電的日本福岡。化被動為主動的全球布局，成為它追求高速成長的籌碼。 工業電腦龍頭研華，正在規畫五年內全球事業版圖。 今年5月，研華董事長劉克振宣布啟動2026~2030年全球擴張計畫，同步擴建美國、日本、台灣三地的製造基地，合計投資超過82億元，金額明顯高於研華過去兩年平均約12億至15億元資本支出，堪稱近十年來規模最大的擴產布局。 三大製造基地各自肩負不同任務，美國加州塔斯汀（Tustin）新園區，將成為研華深入北美市場的支點，10月啟用；日本福岡直方市的新製造大樓2028年完工，將分配到板卡、系統與組裝產線，兼具服務日本客戶與台灣產線備援角色。 最大筆投資則留在台灣，斥資40億元的華亞製造中心最快明年落成，屆時產能將是現有林口廠的兩倍，是研華研發與製造能力的核心。","as_of":"2026-09-11","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"財務長提到中東地緣政治、原物料成本與供應鏈不確定性挑戰","source":"中時新聞網","url":"https://wantrich.chinatimes.com/news/20260407900498-420101","excerpt":null,"as_of":"2026-04-07","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年9月營收107.49億元，年增73.1%，累計前9月789.52億元年增49.1%","source":"TechNews 研華9月營收","url":"https://finance.technews.tw/2026/10/08/acl-2395-202609-financial-report/","excerpt":"研華(2395)今(7)日公布 9 月營收，達 107.49 億元，較 8 月成長 3.2%,較去年同期成長 73.1%,累計前 9 月營收為 789.52 億元，年增 32.2%。","as_of":"2026-10-08","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年8月營收104.19億元，年增87.5%，累計前8月年增45.9%","source":"TechNews 研華8月營收","url":"https://finance.technews.tw/2026/09/07/acl-2395-202608-financial-report/","excerpt":"研華(2395)今(7)日公布 8 月營收，達 104.19 億元，較 7 月成長 -7.6%,較去年同期成長 87.5%,累計前 8 月營收為 682.03 億元，年增 45.9%。","as_of":"2026-09-07","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年6月營收101.23億元年增73.4%，上半年累計465.12億元年增32.2%","source":"TechNews 研華6月營收","url":"https://finance.technews.tw/2026/07/07/acl-2395-202606-financial-report/","excerpt":"研華(2395)今(7)日公布 6 月營收，達 101.23 億元，較 5 月成長 30.9%,較去年同期成長 73.4%,累計前 6 月營收為 465.12 億元，年增 32.2%。","as_of":"2026-07-07","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年3月營收76.99億元年增21.8%，Q1累計203.85億元年增17.5%","source":"TechNews 研華3月營收","url":"https://finance.technews.tw/2026/04/07/acl-2395-202603-financial-report/","excerpt":"研華(2395)今(7)日公布 3 月營收，達 76.99 億元，較 2 月成長 36.8%,較去年同期成長 21.8%,累計前 3 月營收為 203.85 億元，年增 17.5%。","as_of":"2026-04-07","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"3月4日法說：1~2月BB值達1.8，Q1營收預估5.9~6.1億美元，毛利率38~40%","source":"搜尋摘要整理（法說會報導，鉅亨網／udn）","url":"https://udn.com/news/story/7252/9359019","excerpt":null,"as_of":"2026-03-04","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2營收261.3億元季增28%年增46%；崑山廠產能利用率104%~106%；B/B值由Q1 1.77降至Q2 1.44","source":"uanalyze 研華Q2營收獲利創新高","url":"https://uanalyze.com.tw/articles/3630752922","excerpt":"2026年08月06日（優分析／產業數據中心報導）⸺ 研華(2395-TW)2026 年第 2 季營收達 261.3 億元，季增 28%、年增 46%，營收與獲利同步創下歷史新高。 28% 的季增幅已經相當亮眼，但如果深入了解，就會發現目前的營收成長，其實已經受到供應鏈與產能限制。 研華第 2 季崑山廠產能利用率已達 104%～106%，台灣廠與日本北九州廠約 94%～95%；","as_of":"2026-08-06","retrieved_at":"20261103","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"天下雜誌報導：研華在中國沒有大份量對手，未聽說中國要對其進口替代（屬進口替代風險，非技術替代）","source":"天下雜誌 cw.com.tw/article/5130056","url":"https://www.cw.com.tw/article/5130056","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"研華設立 WWBO（Worldwide Business Operation）作為全球八大區域營運總部，並建置以 Cross-Docking 與 AI 自主營運為核心的端到端供應鏈；目標 E2E／Cross-Docking 覆蓋率逾 80%、庫存周轉效率提升約 30%、生產週期縮短 50%（為目標非成果）","source":"Advantech 官網新聞稿 Advantech establishes WWBO global operating model and develops an AI-driven autonomous end-to-end supply chain","url":"https://www.advantech.com/en/resources/news/advantech-establishes-wwbo-global-operating-model-and-develops-an-ai-driven-autonomous-end-to-end-supply-chain","excerpt":null,"as_of":"2026-05-29","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"研華 2026 年品牌策略為 Edge Computing & AI-Powered WISE Solutions，持續深化軟硬整合；8 月公布 IWS（Integrated WISE Solution & Station）平台策略，涵蓋 IoT 管理、AI 模型部署與 AI agent 編排；2026 上半年營收 NT$465.12 億、年增 32%","source":"Advantech 官網新聞稿 Advantech drives industrial AI opportunities with Integrated WISE Solution & Station (IWS) platform strategy","url":"https://www.advantech.com/ja-jp/resources/news/advantech-drives-industrial-ai-opportunities-with-integrated-wise-solution--station-iws-platform-strategy","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026 年 COMPUTEX 期間研華首度將全球合作夥伴大會（WPC）與展覽整合，強化全球 Edge AI 生態系","source":"聯合新聞網 研華搶攻邊緣 AI 商機 COMPUTEX 首度整合全球夥伴大會","url":"https://udn.com/news/amp/story/7240/9502676","excerpt":null,"as_of":"2026-05-14","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"法說會提及研華未來將以策略合作與小型併購為主，補強攝影機、無線通訊、感測器等邊緣 AI 技術；另因記憶體缺料，板類產品漲價約 4%、系統產品約 8%，自 2026 Q1 反映","source":"搜尋摘要（鉅亨網／中時等法說報導，未逐篇核對）","url":"https://news.cnyes.com/news/id/6220578","excerpt":null,"as_of":"2026-03-02","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026年8月法說會後外資目標價700-750元、本土法人上看800元，Q2獲利大幅優於市場預期","source":"工商時報 ctee","url":"https://www.ctee.com.tw/news/20260806701105-430201","excerpt":"《電週邊》研華創高價後翻黑 法人全調價至700以上 最高上看8字頭 《電週邊》研華創高價後翻黑 法人全調價至700以上 最高上看8字頭 2026.08.06 12:29 時報資訊 研華 邊緣AI 工業電腦 半導體設備 法說會 切換文字大小 複製文章連結 分享至臉書 以Line分享 加入Google來源 參與討論 友善列印 已將目前網頁的網址複製到您的剪貼簿！ 【時報記者葉時安台北報導】研華(2395)法說會後，土洋法人看法正面，目標價均上修至700元以上，三家外資目標價給予700-750元，本土法人更上看800元大關，即使缺貨漲價因素，但工業電腦景氣處於上升階段，下半年營運可望高檔不墜，研華更可望受到半導體設備需求延續，2027年持續成長可期","as_of":"2026-08-06","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2營收與營益率優於財測、毛利率低於財測（原物料價格波動），上半年EPS 9.05元","source":"工商時報 ctee","url":"https://www.ctee.com.tw/news/20260731701464-430201","excerpt":"《電週邊》研華Q2、H1獲利續創同期高 但毛利率承壓 《電週邊》研華Q2、H1獲利續創同期高 但毛利率承壓 2026.07.31 15:11 時報資訊 研華 EdgeAI 法人說明會 營收 獲利 切換文字大小 複製文章連結 分享至臉書 以Line分享 加入Google來源 參與討論 友善列印 已將目前網頁的網址複製到您的剪貼簿！ 【時報記者葉時安台北報導】研華（2395）115年第二季暨上半年法人說明會將於下周三(8月5日)召開，研華周五舉行董事會，率先公布2026年第二季暨上半年合併財務報告。研華今年第二季營收及獲利均創同期新高，營收、營益率雙雙突破財測，然毛利率受短期關鍵原物料價格波動影響，較去年同期下滑，低於財測。研華上半年每股稅後盈餘升至9.05元，同步創高，展望下半年，加速Edge AI應用普及，為長期營運成長注入動能。","as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026年5月法說：Q1毛利率39.1%，Q2財測毛利率38%~40%、營益率16%~18%","source":"工商時報 ctee","url":"https://www.ctee.com.tw/news/20260506702000-430201","excerpt":null,"as_of":"2026-05-06","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FactSet調查：16位分析師2026年EPS中位數由15.75元上修至16.13元，預估目標價550元（日期未註明）","source":"鉅亨速報 cnyes","url":"https://news.cnyes.com/news/id/6561566","excerpt":"鉅亨速報 - Factset 最新調查：研華(2395-TW)EPS預估上修至16.13元，預估目標價為550元 鉅亨網新聞中心2026-08-06 08:10 根據FactSet最新調查，共16位分析師，對研華(2395-TW)做出2026年EPS預估：中位數由15.75元上修至16.13元，其中最高估值20.75元，最低估值14.1元，預估目標價為550元。","as_of":"2026-08-06","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026年5月法說後美系外資目標價調升至405元、日系外資自350元上修至480元、本土法人多在500元以上","source":"中時 wantrich","url":"https://wantrich.chinatimes.com/news/20260507900322-420101","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"公開資訊觀測站近12個月42則重大訊息中，標題含關鍵字者僅3則，皆為處分（子公司Advantech Europe B.V.股權集團內部架構調整、日本淺草不動產處分），無訴訟、裁罰、重編、停工類標題","source":"公開資訊觀測站 歷史重大訊息清單（近12個月）","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2395","excerpt":"2025-11-03 至 2026-11-03 共 42 則；標題含關鍵字（併購、合併、收購、處分、訴訟、仲裁、停工、工安、裁罰、重編、異常、更正等）者 3 則，未含者 39 則。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"子公司Advantech Europe Holding B.V.處分Advantech Europe B.V.100%股權予關聯企業，交易總金額新台幣1,421,476仟元，屬集團投資架構調整","source":"公開資訊觀測站 重大訊息全文（2026-07-31）","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2395","excerpt":"主旨：代子公司Advantech Europe Holding B.V.公告處分Advantech Europe B.V.100%股權","as_of":"2026-07-31","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"日本子公司AJP處分東京淺草土地及建物予非關係人Sekisui House Real Estate，預計交易總金額日圓1,810,000,000元（約NTD363,810,000元）","source":"公開資訊觀測站 重大訊息全文（2026-06-30）","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2395","excerpt":"預計交易總金額日圓1,810,000,000元(約NTD363,810,000元)","as_of":"2026-06-30","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"研華董事長劉克振宣布2026~2030年全球擴張計畫，同步擴建美、日、台三地製造基地，合計投資超過82億元，高於過去兩年約12億至15億元的平均資本支出","source":"TechNews 研華82億元擴張","url":"https://finance.technews.tw/2026/09/11/advantech-nt-8-2-billion-expansion/","excerpt":null,"as_of":"2026-09-11","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"新產能時程：台灣華亞新製造中心預計2028年第1季完工；日本福岡直方新製造大樓預計2028年完工；美國Tustin新園區預計2026年10月20日開幕。目前崑山廠Q2產能利用率104%~106%，預估Q3崑山與台灣廠105%~110%","source":"商業周刊/財經媒體彙整 研華啟動82億擴張","url":"https://www.businesstoday.com.tw/article/category/183015/post/202609090005/","excerpt":null,"as_of":"2026-09-09","retrieved_at":"20261103","affects":["thesis.R","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"研華8月法說會稼動率與產能說明：崑山廠106%~110%、台灣廠105%~110%、日本廠95%~100%，可透過加班或外包調配","source":"經濟日報 ctee","url":"https://www.ctee.com.tw/news/20260806701105-430201","excerpt":"展望第三季，研華單季營收可望雙增再創新高，觀察各廠稼動率，崑山廠預估達106%~110%、台灣廠105%~110%、日本廠95%~100%，產能可透過加班或外包調配。法人預估，研華2026年全年營收可望首度突破千億關卡，全年EPS大幅上修，挑戰兩個股本水準。 在產品線表現方面，高階邊緣伺服器與雲端基礎設施業務表現最為亮眼，年成長率衝破100%；","as_of":"2026-08-06","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"研華2025年10月初將主板與系統級產品價格分別調升約4%與8%，因記憶體等零組件成本上升，效益預期2026Q1起反映","source":"中央社 2025-11-05","url":"https://www.cna.com.tw/news/afe/202511050372.aspx","excerpt":"研華已於十月初將主板及系統級產品的價格分別調升4%和8%","as_of":"2025-11-05","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"外資認為2026下半年成本壓力可能自記憶體擴及CPU與PCB，但研華可望轉嫁絕大部分新增成本；未查到2026年降價資料","source":"經濟日報／工商時報 2026-08-06","url":"https://www.ctee.com.tw/news/20260806701105-430201","excerpt":"研華可望能轉嫁絕大部分的新增成本","as_of":"2026-08-06","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"TrendForce：2026Q1 DRAM合約價季增約90~95%，Q2預估季增58~63%、NAND 70~75%；4月報告稱PC DRAM合約價續漲但動能放緩，現貨市場趨穩","source":"TrendForce DRAM Contract Price Apr. 2026","url":"https://www.trendforce.com/research/download/RP260430QO","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"研華2026Q2營收261.26億元年增46%，毛利率受關鍵原物料價格波動影響較去年同期下滑","source":"經濟日報 2026-07-31","url":"https://www.ctee.com.tw/news/20260731701464-430201","excerpt":"但毛利率承壓 《電週邊》研華Q2、H1獲利續創同期高 但毛利率承壓 2026.07.31 15:11 時報資訊 研華 EdgeAI 法人說明會 營收 獲利 切換文字大小 複製文章連結 分享至臉書 以Line分享 加入Google來源 參與討論 友善列印 已將目前網頁的網址複製到您的剪貼簿！ 【時報記者葉時安台北報導】研華（2395）115年第二季暨上半年法人說明會將於下周三(8月5日)召開，研華周五舉行董事會，率先公布2026年第二季暨上半年合併財務報告。研華今年第二季營收及獲利均創同期新高，營收、營益率雙雙突破財測，然毛利率受短期關鍵原物料價格波動影響，較去年同期下滑，低於財測。研華上半年每股稅後盈餘升至9.05元，同步創高，展望下半年，加速Edge AI應用普及，為長期營運成長注入動能。 在單季營運部分，研華2026年第二季合併營收達新台幣261.26億元，年增46%","as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"2023年營收645.67億元年減6.07%，毛利率40.5%；Q3營收年減19.4%但毛利率40.1%，上輪庫存調整期毛利率未下探","source":"鉅亨網 研華法說/財報報導","url":"https://news.cnyes.com/news/id/4924972","excerpt":null,"as_of":"2024-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2023年Q2毛利率36.7%低於預期，原因為零組件缺料漲價與調價時間差","source":"鉅亨網 研華法說報導","url":"https://news.cnyes.com/news/id/4760774","excerpt":null,"as_of":"2023-08-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2023年Q3營收150.06億元年減19.4%，三大區接單不佳","source":"鉅亨網 研華法說報導","url":"https://news.cnyes.com/news/id/4691048","excerpt":null,"as_of":"2023-11-02","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月無對外併購；僅有子公司股權處分（Advantech Europe B.V.100%股權，集團內部架構調整，對象為關聯企業）","source":"公開資訊觀測站 重大訊息全文（2026-07-31）","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2395","excerpt":"(1)交易相對人：Advantech Automation Corporation B.V.\n(2)與公司之關係：Advantech Europe Holding B.V.之關聯企業","as_of":"2026-07-31","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"2395.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":39.0,"operating_margin_pct":17.97,"fcf_margin_pct":1.21,"rd_intensity_pct":7.43},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2395.TW","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"6414.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":20.33,"operating_margin_pct":5.78,"fcf_margin_pct":4.29,"rd_intensity_pct":6.38},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6414.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"6166.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.49,"operating_margin_pct":9.78,"fcf_margin_pct":6.66,"rd_intensity_pct":11.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6166.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"3088.TWO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":33.62,"operating_margin_pct":11.46,"fcf_margin_pct":3.3,"rd_intensity_pct":8.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3088.TWO","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"2397.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.57,"operating_margin_pct":6.38,"fcf_margin_pct":-1.44,"rd_intensity_pct":5.26},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2397.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"2395.TW"},"financial_history":{"ticker":"2395.TW","currency":"TWD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":68744701000.0,"revenue_yoy_pct":null,"gross_margin_pct":37.99,"operating_margin_pct":18.3,"net_income":10757077000.0,"diluted_eps":12.46,"free_cash_flow":8253809000.0,"fcf_margin_pct":12.01,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":64567697000.0,"revenue_yoy_pct":-6.08,"gross_margin_pct":40.52,"operating_margin_pct":18.83,"net_income":10837530000.0,"diluted_eps":12.52,"free_cash_flow":8376922000.0,"fcf_margin_pct":12.97,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":59786293000.0,"revenue_yoy_pct":-7.41,"gross_margin_pct":40.77,"operating_margin_pct":15.21,"net_income":9005037000.0,"diluted_eps":10.38,"free_cash_flow":8873191000.0,"fcf_margin_pct":14.84,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":70882362000.0,"revenue_yoy_pct":18.56,"gross_margin_pct":39.78,"operating_margin_pct":16.29,"net_income":10592508000.0,"diluted_eps":12.14,"free_cash_flow":6889452000.0,"fcf_margin_pct":9.72,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/2395.TW/2395.TW_Q1_2026_Earnings_Call_20260506.md）

# Q1 2026 Earnings Call
**Advantech Co., Ltd.** | Earnings Calls | 2026-05-06

**Ally Chen** (Analysts):
Okay. Good afternoon, and good morning, everyone. Welcome to Advantech's First Quarter '26 Earnings Call hosted by UBS. This is Ally Chen, covering the industrial sector at UBS. It's our pleasure to have Advantech's management team joining the call today. 
On the line, we have Eric Chen, President of GM, CFO; Linda Tsai, President of Intelligent Systems Sector; and Grace Liao, the IR Manager. So for today's meeting, we will start with Grace's presentation and open up for Q&A later. So now let me pass to Grace.

**Grace Liao** (Executives):
Thank you, Ally. Good morning, and good afternoon, ladies and gentlemen. Thank you for your time today. This is Grace Liao, the Senior IR Manager of Advantech. Regarding our Q1 2026 financial results, Q1's revenue reached TWD 20.4 billion, increased 17% year-on-year, 14% quarter-on-quarter. 
Gross margin rate reached 39.1%, slightly lower on both quarterly and annual basis, mainly due to component cost. Operating profit reached TWD 3.7 billion, increased 28% year-on-year. Operating profit rate reached 18.3%, which greatly improved from 15.7% in Q4 '25. Q1 effective tax rate was 18.4%. 
Net income reached TWD 3.3 billion, increased 22% year-on-year. Earnings per share in Q1 '26 was TWD 3.85. Q1 '26, both top line and bottom line reached a record high and also beat the company guidance. For regional performance, in terms of U.S. dollars, Q1 '26 revenue reached USD 644 million, increased 22% year-on-year. 
For regional performance, all regions reported double-digit growth. Major 3 markets continue to contribute 70% of our total sales with slightly shift in regional mix. North America increased 13% year-on-year, driven by semiconductor equipment and data center projects. 
Europe market increased 19% year-on-year due to strong medical equipment and channel sales. China market increased 38% year-on-year, benefit from channel sales, semi equipment and transportation projects. Korean market showed a 44% increase rebound from low base last year, and Taiwan market enjoyed 75% year-on-year growth driven by semiconductor and automation projects. 
For sector mix, perspective, all sectors enjoyed positive growth year-on-year. Both IoT automation and Intelligent System increased 19% year-on-year, driven by semiconductor, energy and transportation projects. Embedded sector increased 15% year-on-year, benefit from strong growth of medical equipment in North America, Europe, Middle East and Africa. 
Intelligent Service increased 3% year-on-year, driven by health care in Europe and the Middle East and Africa market. However, retail in North America slowed down due to component shortage. For balance sheet, this is also my last page, inventory accounts for 18% of total assets, while inventory turnover days slightly improved to 97 days, reflecting improvements in readiness of future shipments. Cash conversion cycle, CCC, maintained 84 days within a healthy range. 
Now I'm handing over the time to President, Eric, to share overall business outlook. Thank you.

**Eric Chen** (Executives):
Thank you, Grace. Good morning, and good afternoon, everyone. Thank you for joining today's meeting. This is Eric. Let me start with a few comments on the first quarter results. In the first quarter, our top line and operating profit exceeds our expectations. Our gross margin was in line with our guidance. Top line performance was mainly driven by strong demand from the semiconductor and the medical sector, also the transportation sector as well. 
In addition, higher DDR4 and SSD price promote customers to press orders early and push the faster delivery. In the first quarter, our OpEx ratio declined by 3.1% year-over-year and operating profit improved by 1.4 percentage points with operating profit up 27% year-on-year. 
With a stable tax expenses, we achieved a record high first quarter results with earnings per share of TWD 3.85. In terms of regional performance, China, Taiwan and emerging markets delivered significant growth of 38%, 75% and 24%, respectively. 
Demand in China was mainly driven by the distribution channels, transportation and energy sector. Taiwan delivered the strongest result driven by the semiconductor and factory automation sectors. From a sector perspective, the iAutomation and iSystems segments performed well, benefiting from strong demand in semiconductors, energy and transportation sectors. 
The Embedded sector benefited from increased shipment of medical equipment in North America, Europe and the Middle East and Africa. iService YoY increased by 3% only driven by growth in health care projects in Europe and Middle East, partially offset the weakness in North American retail business. 
So this concludes my comments on the first quarter. Next page, thank you. Let's look at the B/B ratio trend across regions as shown on this page. The first quarter B/B ratio rose to 1.77. In the U.S., the B/B ratio was 2.37 mainly because key account placed order aggressively to secure product allocation and rising DDR4 and SSD prices. 
The B/B ratios in Europe and China were 1.76 and 1.30, respectively. It is also worth noting that both B/B, bookings and shipments increased by 48% and 11.6%, respectively, compared with the fourth quarter of 2025. 
Next page. Looking ahead to the second quarter, we expect revenue to range between USD 650 million and USD 670 million based on an exchange rate of USD 1 to TWD 31.5. In terms of margin, we anticipate second quarter gross margin of 38% to 40% and operating margin of 16% to 18%. 
Next page. I also highlight then upcoming event that COMPUTEX. We have arranged a series of activities designed to engage different target audience. On the afternoon on June 1, we will host an Edge AI conference at Hua Nan International Center. 
The conference will cover 3 key themes: regional leadership in the era of Edge AI, real-world AI impact across industry and acceleration of WISE platforms and ecosystems. Day 2 will include an on-site visit to Advantech events at the COMPUTEX exhibitions. 
For investors, we will arrange more than 10 rounds of product briefings and booth tours. Day 3, will focus on our Annual World Partner Conference. It will be held at our Linkou campus with business matchmaking and the sector forum as key activities. 
So we would like to honor to have you join us for the day 1 or day 2 events. Many investors have already reserved a spot for the day 2 on-site tours with Grace. So please feel free to reach out to her to register. This concludes my guidance for the second quarter, and thank you for your attention.

**Grace Liao** (Executives):
Thank you, Eric. So I will hand over the time to Ally. Thank you.

**Ally Chen** (Analysts):
Okay. Thank you, Eric. Thank you, Grace. So now let's move on to the Q&A session. We will start with questions we collected from investors before the call and then open up the floor later. So now on the first one about financial and outlook. What is the expected sales mix target in 2026 and '27? And what's the demand for non-Edge AI project expectation?

**Eric Chen** (Executives):
Let me try to answer the question. We expect Systems and iAutomation to have a stronger growth momentum than Embedded and iService in 2026. Demand from semiconductors factory automation and energies remain promising and products such as Sky servers, IPC, box PC and industrial communication solutions should benefit. 
Embedded should benefit from demand in medical equipment and robotics, but we expect this growth momentum to be lower than in semiconductors. In robotics, AMR and AGV demand is stable, while humanoid robotics will take time to move from engineering sample to mass production, even though we currently have around 130 pipeline on hand with total revenue of TWD 120 million. 
iService is facing key chip allocation constraints, which may put some pressures on order fulfillment in the first half. So regarding the demand for non-Edge AI projects because Edge AI project accounts for about 20% of our first quarter revenues, most revenue is still generated from our edge computing and devices. At this moment, we do not expect demand from Edge AI product or project to be negatively impacted by Edge AI requirement. So this is my answer to the first question.

**Ally Chen** (Analysts):
Thank you, Eric. The second question is about -- so I think the first part, what is the sales mix for Edge AI project in first quarter? You just answered that it's 20%. And I think another question is about which verticals are driving Edge AI-related orders?

**Eric Chen** (Executives):
Okay. Edge AI revenue in the first quarter was USD 132 million, accounting for 20.5% of total revenues. We classify Edge AI revenue into 2 categories: Edge AI products and Edge AI components. We always have 2 categories to calculate Edge AI performance. 
In the first quarter, Edge AI product revenue grew 67% to TWD 123 million, while Edge AI component revenue grew 58% to TWD 9 million. Here, we define the Edge AI component as a pure buy and sell model with no value added to Advantech products. That accounts for only 6.8% of our Edge AI revenues. 
For the sectors, for the demand from the sectors, Edge AI related demand mainly come from the factory automation, robotics, smart city and transportation sectors. By geographies, the U.S., Europe and China accounts for a large portion of these orders. This is my answer.

**Ally Chen** (Analysts):
Okay. The third question is about regarding the B/B ratio. What percentage of order backlog is for delivery in second half 2026 or 2027?

**Eric Chen** (Executives):
Okay. Based on our ordering system, we have a central ERP system called SAP system. We have a central data. The percentage of our first quarter order with delivery days more than 6 months out was 37% in January, 57% in February and 47% in March. 
Overall, delivery schedule for more than six months of this year represent 47% of the total quarter 1 bookings. Advantech -- normally at Advantech, a customer order fulfillment generally fall into two categories: We have standard product and DMS or tailor-made products. 
For standard products, the lead time from order to shipments is typically under three months. For DMS and the tailor-made products, lead time depends heavily on customer requirements. In most cases, the shipping occurs within six months. For the quarter 1 bookings, the overall is 70% -- 47% delivery days more than 6 months. This is my answer.

**Ally Chen** (Analysts):
Thank you, Eric. Next question is about material cost impact and the reactions. In terms of profitability, what extent can the increased cost be passed on to customers in terms of different kinds of projects? Any signals that higher project pricing is hurting order intake?

**Eric Chen** (Executives):
Okay. Thanks for the questions. Advantech go-to-market sales strategy have three priorities. Key accounts, a channel partner and general account. For general accounts, we have full pricing power for key account and DMS business. 
When our design products represent a relative small portions of the customer total system cost. Here, I just give you an example. We provide a high reliability Embedded board, Edge AI system were used in the medical device such as surgical robotics or MRI systems, or in a semiconductor equipment such as front-end modules or wafer sorters. 
We are more likely to pass a cost increase through our customers. Because, again, our offering is just a small portion of the whole systems. This type of project represent around 70% of our design-in business. However, in the other side, for projects serving the retail market, for example, the kiosk or POS systems, customer tend to more cost sensitive. 
Free passing through a cost increase is not always practical, but in this case, we negotiate with customer to agree on proper pricing adjustments. At this stage, we don't see the higher project pricings materially affect order intake in some semiconductor customers. They tend to place an order cover the next 18 months to secure further allocation and capacity to Advantech. We don't see any order intake. This is my answer.

**Ally Chen** (Analysts):
Okay. Thank you, Eric. Next question is about the progress of replacing DDR4 with DDR5, and what has the price increase so far? Has the price momentum eased?

**Linda Tsai** (Executives):
This is Linda. On the migration from DDR4 to DDR5 in Embedded and industrial customer is still ongoing, and typically takes 15 to 8 (sic) months and depending on applications. In quarter 1 and quarter 2, 2026, memory price still remain an upward trend, especially on DDR5. 
It's roughly like 30% to 50% QoQ driven by strong AI demand. But in DDR4, stay at a more moderate level, but the ongoing supply is still very tight because the industry continue to face our legacy product. Thank you.

**Ally Chen** (Analysts):
Okay, thank you. For the price increase, for other components such as CPU and other passive components, what's the extent of the price increase, and what is the inventory level of these critical components? Is there any sourcing issue?

**Linda Tsai** (Executives):
From early-to-mid-2026, in addition to memory and SSD, we are seeing the pricing pressure on CPU, especially from Intel and AMD. It's around 10% to 20% price increase, depends on the SKU. Again, it's driven by strong AI demand and limited supply. 
In addition to CPU, we also see that AI-driven demand contribute a higher PCB cost, also a longer lead time. Overall, the component availability remain tighter than historical level, and the sourcing condition are becoming more competitive as the lead time extended across more component.
We are also putting the long-term PO vis-a-vis to our supplier. We continue to manage this through diversified sourcing with different strategic partner and the long-term purchase commitment with our upstream supplier, and the closer engagement to support and make sure the supply continuity. Thank you.

**Ally Chen** (Analysts):
Okay. Thank you. Thank you, Linda. And then next question is about regional and sector performance. What are key order drivers by each sector and by different market in second quarter 2026? How is first quarter 2026 new project design win progressing versus fourth quarter last year?

**Eric Chen** (Executives):
Okay. The key orders drives by sector and by market are as below. For the factory automation, including vision inspections, warehouse management and safety, restrict launch detections is mainly for factory automation. 
For robotics, including AMR and AGVs, we are also receive many RFQ for humanoid robot. As mentioned earlier, we have a lot of pipeline with more than TWD 120 million total revenues. Smart city and transportation, including video surveillance, such as railways, heavy duty vehicles, traffic management and roadside video surveillances. 
Factory automation demand is primary in Asia. For robotics, demand is primary from the U.S., Europe and China, with a small portion from Korea. Smart city and transportation demands mainly from the U.S., China, Asia and Europe.
For the healthcare, demand is mainly from the U.S., Europe and Korea. For the indicator design in indicators, compare with last quarters, below some data for your reference. In first quarter 2025, secured 46 design win with an estimate annual revenue of TWD 67 million.
In this quarter -- in first quarter this year, secured 53 design win with an estimate annual revenue of TWD 158 million. Compare with last quarter, the design win count increased by 7, but the EAR means estimate annual revenues, increased by 2.3x. 
This is the data. Please note that design in activities can be affected by customer demand cycle. Therefore, a 6 months review window provide a more accurate and meaningful compare with just a single quarter. This is my answer.

**Ally Chen** (Analysts):
Okay. Thank you, Eric. Next question is about what are the possible impacts from Middle East uncertainties on Advantech, and what's the company strategy to mitigate risks?

**Linda Tsai** (Executives):
The impact of Middle East crisis has been primarily on smart city infrastructure project, especially in transportation sector, where the implementation plan time line has been experiencing delay. 
Overall, the affected business portion remain relatively limited. However, most of business are actually facing indirect impact, including the 1 we shared previously on the increasing cost and the extended lead time for the key component. Thank you.

**Ally Chen** (Analysts):
Okay. Thank you, Linda. Next question is about what would be the highlights of Advantech's COMPUTEX exhibition?

**Grace Liao** (Executives):
Well, as Eric mentioned earlier, I think, we do have a full series of three days of events during COMPUTEX, including our Edge AI conference in Hua Nan International Conference Center in June 1. During the COMPUTEX exhibition, we do have lots of application and the physical AI showcases in the Nangang center -- exhibition centers in June 2. 
In June 3, we do host WPC World Partner Conference in our Linkou Campus with our grand keynote and also sector forums in different partners -- global partners and the customers in the Linkou Campus to have a further cooperation and to build the ecosystem in the future. I think, for investors, we'll welcome the investors and also the media to join us in the June 1 and June 2 event.

**Eric Chen** (Executives):
We also have a keynote speech by Miller and Richard, right, in June 2 or June 4.

**Grace Liao** (Executives):
Afternoon of the June 4.

**Ally Chen** (Analysts):
I think we've finished the questions we have on hand. Now we will open up the floor to allow participant to raise questions. [Operator Instructions]. I think while we are waiting for questions from the participants, maybe let me start with a follow-up on B/B ratio. The B/B ratio was like 1.77 as of end of first quarter. Is there any updates like B/B ratio as of most recent ones? Thank you.

**Grace Liao** (Executives):
I think the aggressive B/B ratio in Q1 2026 indicating 2 parts. First of all, I think we do see very strong demand in the market sides from the enterprise customer, especially in robotic and also automation and the semiconductor equipments. 
That is real demands from the end markets. However, with the balance of the supply chain and also continuously cost up in the component side, I think most of the customer is prompted to place their orders within 18 months, which means, I think, they are quite aggressive in their order behavior to secure the sourcing allocation from us.

**Ally Chen** (Analysts):
Okay. I often get asked by investors about how to calculate the B/B ratio. In terms of shipment, is that defined as the quarterly shipment, or can the management team elaborate a little bit on how to calculate B/B ratio?

**Eric Chen** (Executives):
Let me try to answer these questions. For the B/B ratio is called bill-to-bookings. The ratio compares the shipment versus the order. Just mentioned earlier, we have a central ERP system. We call it SAP HANA. When the new order pass, we will keep the order as an order date. 
The booking means, for example, for the April, all the new order came in from April, we keep as the booking. The order date cannot be revised by the manuals. They create by the system automatically. This is, we so-call the bookings. For the shipment as invoice date, as you know, we will generate invoice after the finished goods ship out from Taiwan or from China, Kunshan.
B/B ratio, the B, booking means the order entry in a certain period, especially we calculate by monthly base. For another B, it's called billings, as it's about how many invoice we generate and send out to our customers. This is we call the B/B ratio.

**Ally Chen** (Analysts):
Understand. Understand. Thank you. Actually, so if our revenue is already growing very strong, and B/B ratio is increasing, which means our order backlog is also increasing a lot.

**Eric Chen** (Executives):
Yes, exactly. Yes, exactly. But pay attention for, because the fulfillment time is -- normally, we get a certain order. We have huge amount of certain order, but the delivery, that means the business might be happens in the coming 2 to 3 months for the standard products. For the design product, it really depends on customer required date. Normally, I just mentioned earlier, it will be shipment within 6 months.

**Ally Chen** (Analysts):
Understand. Okay, thank you. And then separately on the gross margin front, last earning -- last analyst meeting, we understand that we should be able to -- Advantech should be able to pass over most of the cost increase. Meaning that the input cost difference between the signing of the agreement and the delivery day, the cost, the price gap can be largely passed over to our customer. Is this still the practice now?

**Grace Liao** (Executives):
Yes. As we mentioned in the previous investor conference, actually we take more aggressive pricing policy to our customer. First of all, we do have overall ASP hike in October 2025. That is the first wave of ASP hike with the hiking range of 4% to 8%. 
From beginning of this year, we take more aggressive pricing policy with bi-weekly adjustment -- pricing adjustment to our system level product and monthly adjustment to the board level products. We are able to transpass most of the pressure to pricing pressure to our customer.
As Eric mentioned before that, actually, the IPC and also the overall purchasement cost of in customer points of view, it is a small portion. It's quite limited to their overall CapEx. Therefore, I think there is a lower sensitive to the -- in the cost of pricing sensitivity. 
Going forward, I think we're still facing the upward pressure from the component side. As Linda mentioned that, besides memory, we do have several items that is still under pressure. we will be more cautious to review our overall cost structure and if necessary, we will continue to pass the pricing pressure to the customer. This is a continued theme of the whole year.

**Ally Chen** (Analysts):
Okay. Thank you.

**Eric Chen** (Executives):
And all [indiscernible], there's a time gap -- a time lag, how to say that -- the time lag between the new order, also the existing order. We will compensate a little bit for the time lag. If the component is still going higher, then we need to a little bit time to adjust our price.

**Grace Liao** (Executives):
Usually the time gap is, roughly 1 to 2 quarter.

**Eric Chen** (Executives):
Yes.

**Ally Chen** (Analysts):
Okay. Okay. Thank you. [Operator Instructions]. We have Meryl on hand. Meryl, please go ahead.

**Meryl Kao** (Analysts):
Hello, management team. Can you hear me?

**Grace Liao** (Executives):
Yes, please.

**Eric Chen** (Executives):
Yes.

**Meryl Kao** (Analysts):
Okay. Hi, management team. Thanks for having me. I'm Meryl from the Taipei Times. I believe last time -- like in our news conference last time, we talked about we have this forecast for our Edge AI percentage to account for about 30% of our total revenue this year, which it was 20% last year. 
According to what you just said, I believe we can have a more positive outlook for our Edge AI products this year, right? I would like to ask if we have a new prediction on the specific proportion of Edge AI percentage of our total revenue. This is my first question. 
My second question is that, because I think Advantech has been releasing positive outlooks on our robotics sectors as well. I would like to ask, because I think it's either Eric or Miller, like you guys said, we have been cooperating with about 20 robotic clients last year. 
I would like to ask if the number has been increasing, like did we cut into new robot clients or we are sticking to the 20 clients that we had last year, and we are still sticking to them, instead of like developing into new customers. Thank you.

**Grace Liao** (Executives):
Thank you, Meryl. I'll try to answer your questions. First of all is the Edge AI revenue contribution target this year. I think our target is still maintain a 30% by end of this year. I think right now the progress is on track and slightly beat the expectation. 
Q1 is 20.5% of a total revenue contribution from Edge AI. According to Eric, that Edge AI revenue is actually in first quarter has reached USD 132 million. I think we are quite positive for the Edge AI progress this year because both the Edge AI products and Edge AI components seems very -- it grows very aggressively.
I think right now we do see a very positive feedback from customer side in the factory automation, robotic and the smart city transportation sectors, especially in U.S., Europe and also China market, which is our major three markets. 
I think the first question, right now is on track and I think we are quite positive with the progress right now. The second question is about the robotic clients globally. Last year, around 20 customers, and we are still stick with those key accounts and the major players globally. However, I think robotics still is a early stage for the global.
I think the real contribution is gradually coming up rather than a rapid growth in the short time. I think right now Advantech do have a very good positioning with, we do have a fully product offering for the building block for the robotic applications, including all the sensing technology, all the calculation for sensors and also the modules. However, I think the real contribution right now is still very limited in the first half of this year. I think we will continued to co-work with those key accounts globally.

**Eric Chen** (Executives):
Just 1 appendix from my side. We have endorsed the robotics engagement, just not only for Embedded sector, but also for the Intelligent System sector. I think that Linda can update a little bit about the progress for the robotics.

**Linda Tsai** (Executives):
Yes. for robotic, some of customer design using Embedded board, some of them in the box. As you may know that, last year NVIDIA released Jetson Thor, and they also have 1 is called Jetson Thor IGX. That product's especially targeting AI robotics. 
Either it's human robotics or robotics wheel arm. With this new platform, we also have some of the good customer we are working on the designing. The new platform for this year is that Intel also launched Panther Lake. 
This is also the one with the several application they focus. One of the important is on the robotic as well. At the beginning, since quarter -- end of last year, this year, we are working with some of the customer, especially in USA., on that the new platform from NVIDIA Jetson Thor IGX, and also on Intel Panther Lake.

**Ally Chen** (Analysts):
[Operator Instructions]. I also have one follow-up question on the demand front. How will we view the demand? Where it come from? Is it more of a top-down upcycle in terms of automation, in terms of CapEx cycle, or do you see an uneven demand coming from a different subsector? And if this is all about a cycle, where are we in the cycle? Are we just at the beginning, and how long would you expect?

**Grace Liao** (Executives):
I think because Advantech's business is quite diversified, so we cover quite different sectors. Therefore, I think both of the drivers do have a positive effect to our business. For example, I think we do have a policy-driven related sector. 
For example, like automation or even like semiconductor kind of subsidized by the government, especially for U.S. or even China markets, I think policy-driven is one of the angle here, including semiconductor high tech...

**Eric Chen** (Executives):
In that nature.

**Grace Liao** (Executives):
High tech and also like, for example, like energy or infrastructure related. For second, we do see lots of emerging sectors, for example, like robotic and also like maybe like AI embedded technology, especially in the healthcare, for example. Emerging technology or emerging sector is one of the driver here. Maybe Linda can add on more information about this question. Thank you.

**Linda Tsai** (Executives):
Yes. I think I will see that on some of the vertical market on the demand cycle, especially on semicon, energy infrastructure and the data center. On semicon, of course, everything is driven by AI demand. This is still at the, I would say, the beginning of cycle because our target customer are the semicon equipment builder, no matter is the front end or the back end, the customer globally. 
We still see a very strong demand from our customer where we are already designing. And recently, there are more design requests from our customers. I think on the semicon equipment builder, they are still at the early design cycle, and they are demand from all the fab, one of the very important from Taiwan and others.
On energy side, there are two perspective because the power is very critical for all the data center. We're targeting that, that's already is Advantech that focus market, energy sector, smart grid. 
We see the demand for smart grid that we provide the smart substation and virtualization, also the connectivity. That's also the demanding. And I would say still at the beginning because that's all fulfillment for the data center, how they're going to build out their smart grid infrastructure.
Lastly, about this data center. We are not doing business with data center, but with our automation product and customer. In the data center, in addition to the energy, they need a lot of gateway and automation control. 
That's also flowing in the right data center through our automation customer. On semicon energy, especially on the infra side, on smart grid and on the data center also is on infrastructure wise, it's benefit to us. I think it's at the beginning of the increasing cycle demand. This is my answer.

**Ally Chen** (Analysts):
Okay. Thank you, Linda, and the team. checking if anyone have any question.

**Grace Liao** (Executives):
While we are waiting for further questions, I would like to recap the key points that we deliver in -- during the last investor conference. Because we, this year -- beginning of this year, approved by the board, actually, Advantech do have majority changes in our new dividend policy. 
I would like to take a few minutes to recap the key points for that. We do have a new dividend policy beginning of this year to realize more, the profit sharing to the shareholders and also try to optimize the ROE and the value creation of the company. The key point for the new policy would be including three parts.
First of all, dividends, format shifting from stock dividends plus cash dividends. Right now, shifting to 100% cash dividend base. Second, we increase cash payout ratio, raising from 70% to 75%, up to 70% to 80%. This a kind of a range. 
The third part is, we also announced the special cash dividends for the next three years, for additional TWD 2 per a share annually, sourcing from our capital reserves. And this is for the next three years, a period from 2026 to 2028. 
Therefore, with the new dividend policy take, the year 2025, for example, that our total EPS last year is about TWD 12.25. With 75% cash payout ratio, that would be TWD 9.2 per share, plus TWD 2 special cash dividend additionally. That was a total TWD 11.2. 
Therefore, The overall cash dividend payout is TWD 11.2 out of TWD 12.25. I think the total cash payout ratio would be 91.4%. That is higher than the historical range in the historical. So therefore, I think this is again, the new dividend policy from the management team and also approved by the board. This is a try to realize the profit sharing to every shareholders and allowing me to recap this key points to the investors. Thank you.

**Ally Chen** (Analysts):
Okay. Thank you, Grace. I saw we have two questions. First from Rohit. Rohit, Please unmute yourself. Yes, please.

**Unknown Analyst** (Analysts):
Thanks for the opportunity. If you could give us some more color on what exactly are the kind of products going into semiconductor equipment customers and into data centers, if you could provide some flavor. Second is, both put together, what will be the sales contribution from this?

**Grace Liao** (Executives):
Okay, thank you, Rohit. Maybe Linda can share.

**Linda Tsai** (Executives):
Yes. For semicon equipment builders that we sell, our product is on edge computing. And from the front-end tool of the semicon equipment tool, they need that server grade of that computing over there. That's all their engine. 
In addition to that, some of our semicon customer, they also require the IO, DIO, AIO and some connectivity where Advantech can provide that bundle selling together. That's for semicon. Some of semicon customer, they also, like, require the rack integration. 
There's also new emerging business that we're incubating instead of just providing a rack server used on the semicon tool, also the full rack integration. Data center, we are not selling server to data center, but data center-wise, on the infrastructure, they are the energy need to be monitoring. 
Those requiring the gateway, again, also with some of the IO connectivity. That's why we work with our OEM customer for data center. Some of the OEM customer, they are the automation OEM, and we work with them closely, and with them, they sell to data center. I hope that answered your question.

**Unknown Analyst** (Analysts):
Got it. That's very helpful. Both put together semicon equipment customers and the business for data centers, what would that be as a percentage of sales for one quarter, just to get a sense?

**Linda Tsai** (Executives):
The big portion of the revenue should be on semicon tool. The portion, because we are the -- I mean, the Advantech business -- Most of the semicon business -- I mean, semicon equipment builder, semicon tool, the front end, back end, mostly it come from Intelligent System team. 
From Intelligent System team, quarter 1, we have like 234, I would say like 30% to 40% because this quarter 1, one of the growing driver is semicon from U.S., Taiwan, Japan and Korea. I would say that 30% to 35% minimum is from semicon, or could be higher. 
Could be higher. Yes, could be higher. On the other hand, data center, because we are selling gateway, the ASP is much lower. The gateway is not a high performance server used on the tool, so data center is more like we're selling the gateway, could be the ARM-base. That revenue portion is not that big. It's more on the quantity-wise. Those are mainly from automation product line -- IoT automation product line.

**Unknown Analyst** (Analysts):
That's helpful. Just one follow-up on the memory side. How are you kind of -- how is Advantech securing memory supplies for the next, say, you know, few quarters? Are we directly speaking to the memory companies and signing long-term contracts, or are we relying on the spot market, in case there is a shortage?

**Linda Tsai** (Executives):
On the memory side, no, we do not talk to Micron, Hynix and Samsung directly. We work with the module house in Taiwan. And module house, several of them in Taiwan, they have the long-term agreement with Samsung, Hynix and Micron. 
Between Advantech and module house, we have the long-term agreement with them that, that whole year, the long-term agreement, and we show them our forecast. That's how we can guarantee the allocation. But really in case if our demand is out of our forecast, then we will still work with our module house because they have the inventory, and then we have the buffer, even though our demand is higher than our long-term agreement, LTA.

**Ally Chen** (Analysts):
Okay, thank you. Next question comes from Lorraine. Lorraine, please unmute yourself.

**Unknown Analyst** (Analysts):
Thank you for taking my questions. The first question is about your order backlog as of the first quarter or as of the April. And then can you share the percentage of your total backlog that will be delivered for the next 6 months? One more follow-up on this question is that would you foresee any factors that will prevent you from deliver this product within 6 months schedule, likely maybe CPU or memory shortages?

**Grace Liao** (Executives):
For the B/B ratio, as Eric mentioned during the previous session, that overall this year, the order schedule delivered in the second half of this year, which means more than 6 months deliveries, around 47% of total Q1's booking. And I think this is based on the component situation in the current moment. 
For IPC, I think the preparation and it is more of -- usually take maybe around 6 to 8 weeks, more than 6 to 8 weeks. So I think this is probably is quite fixed in the whole year. I think under the supply chain situation right now, there is unlikely to push the delivery before the schedule right now. 
So I think for the booking situation this year, considering the pricing -- the component pricing still went up for the following quarters, I think our B/B ratio could be in the high range for the following quarters. That is from B/B ratio points of view. Maybe Eric can share.

**Eric Chen** (Executives):
I can share the backlog situations. We do not disclose these numbers. But just for your reference, from now till December, the B/B ratio -- or the backlog, I mean the backlog is over TWD 1.3 billion, and for the second quarter, at over TWD 700 million. 
But due to the shortage on DDR4 or SSD, we have more conservatives. Our guidance is below -- a little bit below the backlog. Here the backlog, it's most come from our customers. But the reality is sometimes, we will encounter the material supply issue. So we just give a certain discounts, then give you the guidance. The backlog actually is over TWD 700 million, just for -- this is just the beginning of the [indiscernible]. We will gradually increase the backlog till the second quarter. Just for your reference.

**Unknown Analyst** (Analysts):
I have one more follow-up. Could you also share on the current bill of material for memory and CPU on your component and system level product?

**Grace Liao** (Executives):
Sorry, can you repeat your question again, Lorraine?

**Unknown Analyst** (Analysts):
Sorry. The BOM cost as of the first quarter 2026 on memory and CPU on your system and component level products.

**Grace Liao** (Executives):
In BOM cost, structure points of view, actually we don't disclose the detail as a usual basis. Roughly...

**Eric Chen** (Executives):
It very depends, yes.

**Linda Tsai** (Executives):
It very depends because we have like Embedded board or the memory chip down, and we could have the edge computing with the memory module, and we have the server. With the RDIMM is very expensive. In terms of the memory cost, over of bill of material, the percentage really very depends on different product line. Some of the boards on the system, it depends on what the chip set.

**Grace Liao** (Executives):
So Lorraine, which means we are not able to disclose more detail in the BOM cost points of view. I'm sorry.

**Unknown Analyst** (Analysts):
That's okay. Thank you.

**Grace Liao** (Executives):
Thank you. Probably due to all the limits of the time, maybe we can take one last questions. Any inquiry from the investors or from Ally's side?

**Ally Chen** (Analysts):
No? Okay. I think, we are all good here. Any final remarks from the management team before we conclude the call?

**Eric Chen** (Executives):
Not exactly. I just welcome you to join us on the COMPUTEX event, especially for day 2. We already arranged more than 10 rounds of product briefings, also the booth tour. So it's our honor to invite you to join our COMPUTEX event. Thank you.

**Ally Chen** (Analysts):
Okay. UBS also host a COMPUTEX tour, so if you want to join, please register with us. Okay? All right. Thank you, management team. Thank you, everyone, for joining the call. Let's conclude the call today here. Thank you. Bye.

**Eric Chen** (Executives):
Thank you. Bye-bye.

**Linda Tsai** (Executives):
Thank you. Bye.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 2395.TW_Q3_2025_Earnings_Call_20251105.md
- 2025-11-05｜Eric Chen｜guidance：Q4 2025 營收指引 5.5 億至 5.7 億美元（匯率 30.4）（原話："revenue to be between USD 550 million and USD 570 million"）
- 2025-11-05｜Eric Chen｜guidance：Q4 2025 毛利率指引 38%–40%（原話："our fourth quarter gross margin will be between 38% and 40%"）
- 2025-11-05｜Eric Chen｜guidance：Q4 2025 營業利益率指引 15%–17%（原話："we procured the operating margin to be between 15% and 17%"）
- 2025-11-05｜Eric Chen｜guidance：2026 年公司目標為有機成長雙位數（原話："to achieve double-digit organic growth next year"）
- 2025-11-05｜Eric Chen｜guidance：正式財測仍逐季提供，2026 各產品線與地區數字預計 11 月底更精確（原話："we will provide official guidance unless every quarter"）
- 2025-11-05｜Miller Chang｜guidance：Miller 表示北美、歐洲、中國三大區 2026 預期雙位數成長（原話："expect to have a double-digit growth continuously"）
- 2025-11-05｜Eric Chen｜guidance：Eric 預期 2026 年 Edge AI 占總營收至少 25%（2025Q3 為 17%）（原話："account for at least 25% of our total revenue"）
- 2025-11-05｜Miller Chang｜guidance：Q4 部門趨勢預期與前三季相似（原話："will be very similar as the first 3 quarters"）
- 2025-11-05｜Grace Liao｜margin：Q3 毛利率 38.9%，略低於財測區間，管理層歸因材料成本（原話："slightly lower than guidance range"）
- 2025-11-05｜Eric Chen｜margin：管理層量化 DDR4/SSD 漲價對 Q3 毛利率的拖累約 1 個百分點（原話："reduced our gross margin by around 1 percentage point"）
- 2025-11-05｜Eric Chen｜margin：若價格續漲，Q4 對毛利的衝擊會大於 Q3（原話："the GP impact for the fourth quarter will be greater"）
- 2025-11-05｜Grace Liao｜margin：營業費用年增 11%，扣除 AURES 與日本大阪辦公室一次性費用後有機成長 5%（原話："expenses organically increased 5% year-on-year"）
- 2025-11-05｜Eric Chen｜margin：產品成本約 90% 為材料，人工與製費僅約 10%（板卡 6–7%）（原話："90% of the product cost came from material costs"）
- 2025-11-05｜Eric Chen｜margin：管理層說明靠營運效率與採購降本把毛利率維持在約 40%（原話："we can keep our margin at around 40% for a long run"）
- 2025-11-05｜Eric Chen｜margin：AGS（Advantech Global Services）毛利率約 28%，口徑為 CPU／記憶體／硬碟計入 AGS，機殼與主機板計入自動化系統（原話："So the margin is around 28%"）
- 2025-11-05｜Eric Chen｜margin：Edge AI 產品毛利：自動化與 iService 高於公司平均 4 個百分點（原話："iService is 4% above the corporate average"）
- 2025-11-05｜Eric Chen｜margin：對 2026 Edge AI 毛利貢獻，管理層稱現在預測還太早（原話："it's still too early to make the predictions"）
- 2025-11-05｜Eric Chen｜margin：有機成長口徑：AURES 占合併營收 4.7%，扣除後前三季為 20.3%（原話："AURES accounts for 4.7% of our consolidated revenue"）
- 2025-11-05｜Eric Chen｜customer：Q3 B/B 值由 Q2 的 1.08 降至 1.01（原話："decreased from 1.08 in the second quarter to 1.01 only"）
- 2025-11-05｜Eric Chen｜customer：北美 Q3 B/B 由 Q2 1.19 降至 0.88，管理層歸因設計與專案週期（原話："softened to 0.88 in the third quarter"）
- 2025-11-05｜Eric Chen｜customer：10 月整體 B/B 回升至 1.19（歐洲 1.23、中國 1.20、美國 1.19）（原話："the B/B ratio was very aggressive rebounding to 1.19"）
- 2025-11-05｜Eric Chen｜customer：管理層稱美國 design win 管線可支撐未來 2–3 年業務（原話："it will secure our business for the coming 2 to 3 years"）
- 2025-11-05｜Eric Chen｜customer：韓國市場年減 6%，歸因政治因素（原話："Korean market declined 6%, largely due to political issue"）
- 2025-11-05｜Miller Chang｜customer：疲弱部門為零售與部分地區博弈，歸因消費者支出縮減（原話："such as retail and also gaming sector in some regions"）
- 2025-11-05｜Eric Chen｜risk：美國銷往美國產品 93% 自台灣出貨，目前享關稅豁免、多數產品稅率為 0（原話："93% import from Taiwan, only 6% from China"）
- 2025-11-05｜Eric Chen｜risk：若台灣面臨高關稅的三項對策：卡車直送、美國當地組裝、依貿易條件調價（原話："we will implement 3 key initiatives"）
- 2025-11-05｜Eric Chen｜risk：管理層擔心因關稅漲價導致 2026 年需求下滑（原話："price increase may lead to a decline in demand"）
- 2025-11-05｜Eric Chen｜risk：DDR4／SSD 供應緊張與價格不穩預期持續到明年中（原話："unstable price into the middle of next year"）
- 2025-11-05｜Eric Chen｜risk：因主要供應商控管現貨與配貨，公司要求客戶預付款項才備料（原話："ask customers to make advanced payments"）
- 2025-11-05｜Eric Chen｜risk：DDR4 庫存水位偏低，補貨跟不上需求（原話："our inventory level remained low"）
- 2025-11-05｜Eric Chen｜risk：醫療客製設計產品轉換 DDR5 較慢，因需客戶認證（原話："customer design products transition are mutually slower"）
- 2025-11-05｜Eric Chen｜commitment：10 月已發出調價通知：板卡漲 4%、系統漲 8%（原話："increase of 4% of board products and 8% for system products"）
- 2025-11-05｜Eric Chen｜commitment：管理層預期調價對新訂單與標準品的正面影響於 2026 Q1 呈現（原話："price adjustment to positively impact new orders"）
- 2025-11-05｜Eric Chen｜commitment：少數大客戶要求時，原則上可吸收 30% 關稅，但附條件（原話："we might absorb 30% of tariff as a matter of principles"）
- 2025-11-05｜Eric Chen｜commitment：結語承諾確保交貨並主動管理 ASP 以保護獲利（原話："actively manage our ASP to safeguard our profitabilities"）
- 2025-11-05｜Eric Chen｜commitment：結語承諾確保對客戶穩定交貨（原話："committed to ensure reliable delivery to our customers"）
- 2025-11-05｜Miller Chang｜commitment：ACE R 系列（機器人）與 ACE i 系列（工業）預計 2026 年中開始上市（原話："release the product to the market by middle of 2026"）
- 2025-11-05｜Eric Chen｜product：Edge AI 占營收由 2024 年 9.4% 升至 Q3 的 17%（原話："increased from 9.4% to 17% in the third quarter"）
- 2025-11-05｜Miller Chang｜product：機器人產品設計中專案管線超過 2 億（原文如此）（原話："more than 200 million projects in design pipeline"）
- 2025-11-05｜Miller Chang｜product：Edge AI 專案約 50% 營收來自硬體以外的模組、元件與軟體整合，傳統則約 90% 為硬體（原話："Edge AI project, 50% is not only hardware"）
- 2025-11-05｜Eric Chen｜competition：中國本土同業降價競爭，公司自述 2022/2023 年以來在中國售價下降約 2%（原話："our selling price dropped about 2% compared with year 2022"）
- 2025-11-05｜Miller Chang｜competition：Miller 稱中國本土競爭加劇，公司以長期服務與品質回應（原話："the local competition is even higher"）
- 2025-11-05｜Miller Chang｜competition：Edge AI 純硬體面超過 50% 的競爭來自台灣供應商（原話："more than 50% of the competition is from Taiwan"）
- 2025-11-05｜Grace Liao｜capital_allocation：Q3 現金占總資產 21%，低於上季，因第三季發放現金股利（原話："lower than the previous quarter due to cash dividend payment"）
- 2025-11-05｜Grace Liao｜capital_allocation：現金轉換週期 84 天，管理層視 99 天以下為舒適水位（原話："CCC, is reported 84 days"）

### 問答異常語氣（迴避／改口／保留）
- 2395.TW_Q3_2025_Earnings_Call_20251105.md｜問：DDR5 是否也供應吃緊／DDR4 轉 DDR5 進度｜答法：談轉換進度後，對 DDR 是否缺貨的原因明確表示不評論
- 2395.TW_Q3_2025_Earnings_Call_20251105.md｜問：DRAM 占總元件成本的比重｜答法：稱手邊沒有數字、內部不計算，改口稍後再提供，未給數字
- 2395.TW_Q3_2025_Earnings_Call_20251105.md｜問：Q4 各區 B/B 與出貨動能｜答法：先稱 Q4 預測還太早，但同時提供 10 月 B/B 1.19 單月數字

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
{"date":"20261011","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回到最近四季 EPS 的 30 倍以下，且最近一季接單出貨比仍 ≥1.0；觸發後先重跑研究，不直接建倉","irr_base_pct":3.9,"ev5y_pct":26.1,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.2,"ev5y_pct":26.1,"irr_base_pct":3.9,"max_dd_pct":-60,"bull_5y_price":1610.0,"bear_5y_price":390.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價回到最近四季 EPS 的 30 倍以下，且最近一季接單出貨比仍 ≥1.0；觸發後先重跑研究，不直接建倉","price_at_dd":727.0,"archetype":"循環/商品","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2395.TW_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
