你是 stock-analyst **v20 判斷 agent**，標的 PWR（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"PWR","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PWR_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PWR_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":12014.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm"}},{"id":"f_kpi1_gaap","label":"GAAP 營業利益","value":1026.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益率","value":8.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm"}},{"id":"f_kpi3_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（公司未揭露 non-GAAP 營業利益，以此代）","value":1448.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm"}},{"id":"f_kpi6_2026","label":"全年 2026 指引（上修）","value":"營收 $41.3–41.6B；adj. EPS $17.90–18.30；adj. EBITDA $4.40–4.49B；FCF $2.50–3.00B；GAAP EPS $12.57–12.97","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm"}},{"id":"f_kpi7_backlog","label":"總 backlog","value":63731.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_pwr_gross_margin_pct","label":"PWR 毛利率","value":15.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_operating_margin_pct","label":"PWR 營業利益率","value":6.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_fcf_margin_pct","label":"PWR FCF 利潤率","value":8.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mtz_gross_margin_pct","label":"MTZ 毛利率","value":12.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTZ.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mtz_operating_margin_pct","label":"MTZ 營業利益率","value":4.85,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTZ.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mtz_fcf_margin_pct","label":"MTZ FCF 利潤率","value":2.34,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTZ.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eme_gross_margin_pct","label":"EME 毛利率","value":19.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eme_operating_margin_pct","label":"EME 營業利益率","value":9.88,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eme_fcf_margin_pct","label":"EME FCF 利潤率","value":7.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dy_gross_margin_pct","label":"DY 毛利率","value":20.53,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DY.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dy_operating_margin_pct","label":"DY 營業利益率","value":7.78,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DY.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dy_fcf_margin_pct","label":"DY FCF 利潤率","value":6.81,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DY.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_gross_margin_pct","label":"FIX 毛利率","value":25.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_operating_margin_pct","label":"FIX 營業利益率","value":16.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_fcf_margin_pct","label":"FIX FCF 利潤率","value":19.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_fcf","label":"自由現金流（FCF）","value":1199.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm"}},{"id":"f_kpi5_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":6.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":625.48,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-17.38,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":49.97,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":4.12,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.75 → 17.44）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":2.96,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.93 → 20.52）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":1.7,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.54 → 23.94）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":17.44,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":20.52,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":23.94,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":24.39,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 14.02 → 17.44（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":56.6,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝67.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":67.8,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":2.53,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.67,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":35.86,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 17.44，分子＝快照價 625.48","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.07,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":5196.63,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 7511.9、現金 2315.27（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":150.68,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":99442.17,"period":"2026-11-03","unit":"USD m","basis":"市值 94245.54 ＋ 淨負債 5196.63","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":41492.91,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":46363.8,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.4,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 619.18 / W52 591.63 / W104 468.64 / W250 303.87 / W250 13週斜率 2.7%"},{"id":"f_ma_w52","label":"52 週均線","value":591.63,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":468.64,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":303.87,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.7,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K：多數業務進入門檻低，任何有資金與技術者都可能成為競爭者；分包商可能發展能力直接競標主合約；公用事業客戶有自有內部團隊，可能增加內製。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"In addition, there are relatively few barriers to entry into some of the industries in which we operate and, as a result, organizations that have adequate financial resources and access to technical expertise may become a competitor.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K：公司自述近期在較小規模專案已遇到更競爭的定價。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"based on rapidly changing competition and market dynamics, we have recently experienced, and may in the future experience, more competitive pricing for smaller scale projects.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"CSIMarket：PWR 在其追蹤同業組合計營收占比上升，營收成長高於同業","source":"CSIMarket PWR Competitors","url":"https://csimarket.com/stocks/PWR-Competitors","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K：最大客戶占合併營收 8%、前十大客戶占 30%；公司稱客戶（主要為公用事業）有內部服務組織，目前仍外包大部分，但不保證未來不增加自製能力。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"For the year ended December 31, 2025, our largest customer accounted for 8% of our consolidated revenues and our ten largest customers accounted for 30% of our consolidated revenues.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因素：客戶的內部服務組織可自行施作，客戶可能被迫增加自行施作而減少外包給 PWR；MSA 下客戶無義務指派特定工作量。未找到具體客戶已導入第二供應商或自製的新聞。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"the in-house service organizations of our existing or prospective customers are capable of performing, or acquiring businesses that perform, the same types of services we provide, and these customers may also face pressure or be compelled by regulatory or other requirements to self-perform an increasing amount of the services we currently perform for them","as_of":"2026-02-19","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 最大客戶占合併營收 8%，前十大客戶占 30%。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"For the year ended December 31, 2025, our largest customer accounted for 8% of our consolidated revenues and our ten largest customers accounted for 30% of our consolidated revenues.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"2023–2025 年無單一客戶占營收或應收帳款 10% 以上。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"No customer represented 10% or more of Quanta’s consolidated revenues for the years ended December 31, 2025, 2024 or 2023, and no customer represented 10% or more of Quanta’s consolidated receivable position as of December 31, 2025 or 2024.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"風險因素揭露：大客戶可能減少業務、被併購或遭遇財務困難乃至破產，可能對公司造成重大不利影響（一般性揭露）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"A significant customer may also encounter financial constraints, based on cost of capital or other reasons, file for bankruptcy protection or cease operations, any of which could also result in reduced or discontinued business with us.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"PWR 10-Q 顯示 2026-06-30 backlog 為 $53.44B（RPO $33.55B）；Q1 2026 backlog 曾為 $48.5B","source":"Quanta Services Form 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001050915/000105091526000025/pwr-20260630.htm","excerpt":"•The expected recognition and realization of our remaining performance obligations or backlog; •Expectations regarding the outcome of pending or threatened legal proceedings;","as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Zacks/Nasdaq 文章：PWR 管理層稱需求可能維持十年以上，大型 765-kV 輸電計畫才剛進入 backlog","source":"Nasdaq/Zacks: Can Quanta's Record $48.5B Backlog Support Another Growth Leg in 2026?","url":"https://www.nasdaq.com/articles/can-quantas-record-485b-backlog-support-another-growth-leg-2026","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"歐洲 TSO 調查：超過 90% 營運商表示技能短缺已拖延專案；高壓輸電勞動力為瓶頸","source":"euroengineerjobs: High-Voltage Transmission Recruitment in 2026","url":"https://www.euroengineerjobs.com/article/1048/high-voltage-transmission-recruitment-in-2026-when-the-grid-becomes-the-labour-bottleneck","excerpt":"directly into a recruitment bottleneck because transmission projects cannot accelerate without specialist engineers. Workforce Shortages Are Now a Delivery Risk, Not a Staffing Issue Transmission system operators entered 2026 already understaffed. Industry surveys across European utilities late in 2025 showed that over 90 percent of grid operators reported skills shortages directly slowing","as_of":"2026-01-15","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"ECMWeb：2027 北美建築展望偏謹慎（2026 末放緩），2028 起多年回升","source":"ECMWeb: Navigating Construction Growth in 2027 Amid Economic Uncertainty","url":"https://www.ecmweb.com/construction/article/55411800/navigating-construction-growth-in-2027-amid-economic-uncertainty","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3 描述的法律程序均為一般營運性訴訟，未列反壟斷調查或拆分事項。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"We are from time to time party to various lawsuits, claims and other legal proceedings that arise in the ordinary course of business.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因素提到對併購的反壟斷審查加嚴（FTC/DOJ、HSR 法等），可能影響部分潛在收購的成本、時程或完成能力；屬一般性風險揭露，非針對 Quanta 的調查。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"Furthermore, the increased antitrust scrutiny of and compliance requirements for potential acquisitions, including by the Federal Trade Commission (FTC) and Department of Justice under the Hart-Scott Rodino Act, the Sherman Act, the Clayton Act (each as amended) or other applicable laws, could negatively impact the cost and timing of or our ability to complete certain potential acquisitions.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"野火事件：Quanta 營運公司曾收到辯護通知、文件保全要求與傳票，未來可能有更多相關求償（產業特定責任風險，非反壟斷）。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"From time to time, Quanta operating companies have received tenders of defense, demands for preservation of documents and indemnity and subpoenas during the course of investigations and reviews of wildfire events","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：關稅、關稅稅負或採購限制可能墊高客戶專案成本、影響專案時程；貿易政策已影響部分元件（如太陽能板）供應鏈。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"Any tariffs, duties, taxes, assessments, or other limitations on the availability or sourcing of materials or components for our customers’ projects can also increase costs for customers and create variability of project timing.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：EPC／固定價合約下負責採購銅、鋼、鋁、變壓器等材料，價格與可得性可能受關稅等全球貿易關係影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"Prices and availability could be materially impacted by, among other things, supply chain and other logistical challenges (including inability of manufacturers to timely meet demand), global trade relationships (e.g., tariffs, duties, taxes, assessments, sourcing restrictions)","as_of":"2026-02-19","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2025 年海外營收 20.0 億美元、佔 7.0%，絕大部分為加拿大與澳洲。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"For the year ended December 31, 2025, we derived $2.00 billion, or 7.0%, of our consolidated revenues from foreign operations, the substantial majority of which was related to Canada and Australia.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險揭露：電力變壓器可得性受製造商無法滿足需求影響，且需求預期持續上升","source":"Quanta Services Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"the availability of power transformers utilized in electric power projects has been negatively impacted by the inability of manufacturers to meet current market demand, which has increased, and is expected to continue to increase.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K：全球貿易關係（關稅、制裁性採購限制）與地緣衝突可能影響設備交付與價格","source":"Quanta Services Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"Global trade relationships (e.g., tariffs, duties, taxes, assessments, sourcing restrictions) and other general market and geopolitical conditions (e.g., inflation, market volatility, increased interest rates and geopolitical conflicts).","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"Quanta 規劃投入 5–7 億美元於電力變壓器製造以緩解交期風險，並可能降低對全球貿易關係變動的暴露","source":"Transformer Technology: Quanta Services commits $700 million to bolster transformer and supply chain infrastructure","url":"https://transformer-technology.com/quanta-services-commits-700-million-to-bolster-transformer-and-supply-chain-infrastructure/","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收 $12.01B，對比 Q3 2025 $7.63B；調整後 EPS $6.06 對 $3.33","source":"Quanta Services Q3 2026 results (8-K ex99.1 / finviz)","url":"https://finviz.com/news/411212/quanta-services-reports-third-quarter-2026-results","excerpt":"Revenues in the third quarter of 2026 were $12.01 billion compared to revenues of $7.63 billion in the third quarter of 2025","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 RPO $41.8B、總 backlog 創高 $63.7B","source":"Quanta Services Q3 2026 results","url":"https://finviz.com/news/411212/quanta-services-reports-third-quarter-2026-results","excerpt":"Remaining Performance Obligations (RPO) of $41.8 billion* and Total Backlog of $63.7 billion*","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"10-Q：Q3 兩個 Electric 營收段營收與營業利益皆較去年同期增加（搜尋摘要未顯示各段數字）","source":"Quanta Services Form 10-Q (period 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001050915/000105091526000041/pwr-20260930.htm","excerpt":"increased revenues and operating income in both our Electric segments","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 管理層：輸配電業務符合預期，較大型輸電、發電與公用事業計畫仍在早期；預期需求延續至 2030 年後","source":"Nasdaq/MarketBeat Quanta Q2 earnings call highlights; Chartmill","url":"https://www.marketbeat.com/instant-alerts/quanta-services-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"-","claim":"分析稱勞動力緊俏（尤其資料中心市場）為限制，另有許可延遲與供應鏈執行風險；E&C 毛利本質偏薄（TipRanks 空方論點）","source":"Nasdaq 分析文章 / TipRanks","url":"https://www.nasdaq.com/articles/can-quanta-turn-data-center-demand-trends-margin-upside","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K FY2025 Item 1 describes utility customers adding smart grid technologies and emerging technologies, plus undergrounding of critical infrastructure and new gas generation and battery storage, all as sources of continued infrastructure work for the company; no substitute technology for its services is identified in the excerpt.","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"in order to reliably and efficiently deliver power and in preparation for emerging technologies, utility customers are also integrating smart grid technologies into distribution systems to improve grid management and create efficiencies, and a number of utility customers continue to implement system upgrades and hardening programs in response to recurring severe weather events, including, among other things, initiatives to underground critical infrastructure.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"PwC analysis: AI, robotics and prefab reshaping engineering and construction; SMRs and modular battery storage moving from prototype to production.","source":"PwC, Building smarter: How prefab, AI, and intelligent supply chains are reshaping engineering and construction","url":"https://www.pwc.com/gx/en/1/ext/us_en_industries_industrial-products_library_engineering-and-construction-trends.rhs.html","excerpt":null,"as_of":"2025-11-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q4 2025 財報電話會議揭露：計畫未來數年投入 5～7 億美元擴充電力變壓器製造與垂直供應鏈（向製造／垂直整合延伸）。","source":"Quanta Services Q4 2025 earnings call（經 Transformer Technology 等轉述）","url":"https://transformer-technology.com/quanta-services-commits-700-million-to-bolster-transformer-and-supply-chain-infrastructure/","excerpt":"During its fourth-quarter 2025 earnings call, Quanta Services detailed a strategic plan to invest between $500 million and $700 million over the next several years into its power transformer manufacturing and vertical supply chain infrastructure.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 載明服務主要以 MSA 等合約提供；搜尋未見 MSA 談判方式或改為直接對資料中心營運商簽約的變動紀錄。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"Our services are typically provided pursuant to master service agreements (MSAs), repair and maintenance contracts and fixed price and non-fixed price construction and engineering contracts.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"管理層描述朝「total solutions」與長期 programmatic 合約轉移，並擴增離場製造／預製設施約 670 萬平方英尺。","source":"Quanta Q1 2026 Earnings Call Transcript (MarketBeat)","url":"https://www.marketbeat.com/earnings/reports/2026-4-30-quanta-services-inc-stock/","excerpt":"and nearly double off‑site fabrication to ~6.7 million sq ft — supporting its goal to more than double earnings power by 2030. Positive Sentiment: Backlog reached a record $48.5 billion with broad‑based bookings (book‑to‑bill ~1.6x), driven by utilities, large‑load projects and hyperscaler/data‑center demand and an increase in programmatic/negotiated work that boosts execution certainty.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-30 Q2 後 Quanta 上調 FY2026 指引至調整後 EPS $16.45–16.95、營收 $39.3–39.7B，高於 MarketBeat 所列財報前共識（EPS $13.78、營收 $35.0B）。","source":"MarketBeat: Quanta Services issues FY 2026 earnings guidance (2026-07-30)","url":"https://www.marketbeat.com/instant-alerts/quanta-services-nysepwr-issues-fy-2026-earnings-guidance-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Zacks 報導財報後 7 筆估計上修，Zacks 共識 EPS 由 $14.27 升至 $15.94，仍低於公司指引區間 $16.45–16.95；最新一筆估計 $16.64 落在區間內。","source":"Nasdaq/Zacks: Bull of the Day: Quanta Services (PWR)","url":"https://www.nasdaq.com/articles/bull-day-quanta-services-pwr-0","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價分布因來源而異（as-of 約 2026-08）：Walnut 平均 $762.08、中位 $790、區間 $410–$976（27 位）；Tickflow 平均 $691.86（8/1）；MarketBeat 平均 $745.55，共識 Moderate Buy；Investing.com 22 買/7 持有/1 賣。Guggenheim 7/31 升至買進、目標價 $800。","source":"Walnut Invest / Tickflow / MarketBeat / Investing.com / MarketBeat Guggenheim","url":"https://walnutinvest.com/stocks/pwr/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026 年未見指引下修；Q1（4月底）上調至營收 $34.7–35.2B、EPS $13.55–14.25，Q2 再上調；Q2 backlog 紀錄 $53B。","source":"Nasdaq/Zacks: Quanta Services boosts FY26 outlook, shares soar 13%","url":"https://www.nasdaq.com/articles/quanta-services-boosts-fy26-outlook-shares-soar-13-update","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Q3 2026 財報稿稱 2026 前九個月完成 5 件收購、2025 全年 8 件；為小型併購（tuck-in），搜尋未見公司本身被合併或大型合併案","source":"Quanta Services 8-K Ex.99（Q3 2026 earnings release，經搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"10-K Item 3：訴訟屬一般營運過程，未列特定重大訴訟","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"We are from time to time party to various lawsuits, claims and other legal proceedings that arise in the ordinary course of business.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共10份，重大項目3份（債券發行等），無 4.02 非依賴／重編項目","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001050915&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Quanta plans $500-700M to double transformer manufacturing capacity and expand off-site manufacturing/fabrication space to about 6.7M sq ft (peer capacity expansion, not discipline)","source":"Nasdaq/Zacks: Can Quanta's Record $48.5B Backlog Support Another Growth Leg in 2026?","url":"https://www.nasdaq.com/articles/can-quantas-record-485b-backlog-support-another-growth-leg-2026","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"MasTec vertical supply-chain investments incl. transformer manufacturing expansion and larger off-site fabrication footprint","source":"Nasdaq/Zacks: MasTec's Record Backlog: A Springboard for Double-Digit Growth Ahead?","url":"https://www.nasdaq.com/articles/mastecs-record-backlog-springboard-double-digit-growth-ahead","excerpt":null,"as_of":"2025-10-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"PWR 2026-09-30 存貨 $480.5M，對比 2025-12-31 的 $370.4M；2026-06-30 為 $469.9M、03-31 為 $446.9M，逐季上升（回補/增加方向）","source":"Quanta Services Form 10-Q (period ending 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001050915/000105091526000041/pwr-20260930.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"PWR Q3 2026 總 backlog 約 $63.7B，較去年同期 $39.17B 增約 62.7%；RPO $41.8B；公司第三度上調全年指引；分析指出供應鏈瓶頸可能限制 backlog 轉換速度","source":"Quanta Services Q3 2026 results (8-K ex99.1) / FinSee Q3 2026 review","url":"https://finsee.ai/earnings/pwr/2026/q3/en/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","triggers"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"Skanska 2026 春季報告：開關櫃與油浸式變壓器交期 60–100 週，2026 年電氣設備價格預期上漲 5–8%；S&P 稱銅線纜、電氣設備、變壓器漲幅最大，2026-06 更新顯示成本動能放緩但交期延長","source":"Skanska Spring 2026 Supply Chain; S&P Global Market Intelligence E&C costs June 2026","url":"https://interactive.usa.skanska.com/2026-spring-construction-market-trends","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"S&P Global E&C 成本指標 2026-06 持續上升但動能放緩（指標由 75.3 降至 67.8）","source":"S&P Global Market Intelligence","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/06/engineering-and-construction-costs-in-june-continue-to-rise-but-momentum-slows","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"Quanta 2009 (GFC downturn) revenue fell 12.2% to $3.32B and gross profit fell 6.5% to $593.5M, while gross margin rose to 17.9% from 16.8% in 2008 (16.1% in 2007); no margin trough found in that cycle.","source":"Quanta Services Form 10-K FY2009 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001050915/000095012310019204/h68032e10vk.htm","excerpt":"Gross profit decreased $41.4 million, or 6.5%, to $593.5 million for the year ended December 31, 2009","as_of":"2010-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Q3 2026 財報稿稱 2026 前九個月完成 5 件收購、2025 全年 8 件；皆為小型併購，未見大型合併","source":"Quanta Services 8-K Ex.99（Q3 2026 earnings release，經搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K Item 3 僅述一般營運過程訴訟，未列特定證券集體訴訟；搜尋亦僅見 2017 年以前律所調查公告","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm","excerpt":"We are from time to time party to various lawsuits, claims and other legal proceedings that arise in the ordinary course of business.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 共10份，重大項目僅3份，清單無 Item 4.02；搜尋僅見 2014–2016 已結案 SEC 詢問，無近期調查或重編","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001050915&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"PWR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.76,"operating_margin_pct":6.81,"fcf_margin_pct":8.46,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MTZ","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":12.74,"operating_margin_pct":4.85,"fcf_margin_pct":2.34,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTZ","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"EME","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.59,"operating_margin_pct":9.88,"fcf_margin_pct":7.47,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"DY","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":20.53,"operating_margin_pct":7.78,"fcf_margin_pct":6.81,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DY","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"FIX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.57,"operating_margin_pct":16.66,"fcf_margin_pct":19.46,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"PWR"},"financial_history":{"ticker":"PWR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":17073903000.0,"revenue_yoy_pct":null,"gross_margin_pct":14.81,"operating_margin_pct":4.91,"net_income":491189000.0,"diluted_eps":3.32,"free_cash_flow":702682000.0,"fcf_margin_pct":4.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":20882206000.0,"revenue_yoy_pct":22.3,"gross_margin_pct":14.07,"operating_margin_pct":5.23,"net_income":744689000.0,"diluted_eps":5.0,"free_cash_flow":1141149000.0,"fcf_margin_pct":5.46,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":23672795000.0,"revenue_yoy_pct":13.36,"gross_margin_pct":14.83,"operating_margin_pct":5.5,"net_income":904824000.0,"diluted_eps":6.03,"free_cash_flow":1477118000.0,"fcf_margin_pct":6.24,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":28479697000.0,"revenue_yoy_pct":20.31,"gross_margin_pct":15.01,"operating_margin_pct":5.57,"net_income":1028378000.0,"diluted_eps":6.8,"free_cash_flow":1620816000.0,"fcf_margin_pct":5.69,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/PWR/PWR_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Quanta Services, Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good morning, and welcome to the Quanta Services Third Quarter 2026 Earnings Call. [Operator Instructions] As a reminder, this conference is being recorded. If you have any objections, please disconnect at this time. 
I will now turn the call over to Kip Rupp, Vice President, Investor Relations, for introductory remarks.

**Kip Rupp** (Executives):
Thank you, and welcome, everyone, to the Quanta Services Third Quarter 2026 Earnings Conference Call. This morning, we issued a press release announcing our third quarter 2026 results, which can be found on the Investor Relations section of our website at quantaservices.com. This morning, we also posted our third quarter 2026 operational and financial commentary and our 2026 outlook expectation summary on Quanta's Investor Relations website. While management will make brief introductory remarks during this morning's call, the operational and financial commentary is intended to largely replace management's prepared remarks, allowing additional time for questions from the institutional investment community.
Please remember that information reported on this call speaks only as of today, October 29, 2026. And therefore, you're advised that any time-sensitive information may no longer be accurate as of any replay of this call. This call will include forward-looking statements intended to qualify under the safe harbor from liability established by the Private Securities Litigation Reform Act of 1995, including statements reflecting expectations, intentions, assumptions or beliefs about future events or financial performance. You should not place undue reliance on these statements as they involve certain risks, uncertainties and assumptions that are difficult to predict or beyond Quanta's control, and actual results may differ materially from those expressed or implied.
We will also present certain historical and forecasted non-GAAP financial measures. Reconciliations of these financial measures to their most directly comparable GAAP financial measures are included in our earnings release and operational and financial commentary. Please refer to these documents for additional information regarding our forward-looking statements and non-GAAP financial measures.
Lastly, please sign up for e-mail alerts through the Investor Relations section of quantaservices.com to receive notifications of news releases and other information and follow Quanta IR and Quanta Services on the social media channels listed on our website. 
With that, I will now turn the call over to Mr. Duke Austin, Quanta's President and CEO. Duke?

**Earl Austin** (Executives):
Thanks, Kip. Good morning, everyone, and welcome to the Quanta Services Third Quarter 2026 Earnings Conference Call. I want to begin by thanking our approximately 95,000 employees. Their commitment to safety, to our culture of absolute performance and to the certainty we deliver for our customers makes everything we will discuss this morning possible.
This morning, we reported third quarter results that meaningfully exceeded expectations with robust double-digit growth in revenues, adjusted EBITDA and adjusted earnings per share, healthy cash flow and record backlog of $64 billion. These results reflect broad-based strength across our segments, service lines and end markets and also the successful multiyear strategy we are executing and the investments we have made in it. Given this outperformance and the expected incremental strength in the fourth quarter, we are significantly increasing our full year 2026 financial expectations across all metrics.
This quarter again demonstrated the ability for our operating model to deliver with certainty at scale. The breadth of our portfolio, combined with the fungibility of our skilled workforce across multiple end markets, provides a significant competitive advantage. This flexibility allows us to strategically deploy resources where demand is strongest, mitigate exposure to individual market cycles and deliver more consistent, predictable outcomes for our customers and stockholders.
Quanta is embedded in the long-term planning of our industry-leading customers across the utility, power generation and large load markets, and inbound demand is accelerating. We stay in front of our markets by remaining deeply customer-focused. Our customers want a partner that can plan with them for years in advance, align craft labor and supply chain solutions to their capital programs and bring certainty to their projects and programs at a reasonable cost and in a way that delivers lasting economic benefits to the communities where these projects are built. Our reputation for delivering and our ability to mobilize people and supply chain quickly is driving the demand for our solutions.
That reputation was built in our utility business, which remains the foundation of Quanta. Utilities are being asked to double in size over time, and we believe the need to significantly expand and enhance the power grid for reliability, resiliency and load growth is visible and necessary. We expect additional opportunities, including high-voltage transmission, power generation, large load and technology, to stack on top of what we view as a long-duration compounding utility base, where we continue to extend our leadership position. These opportunities extend our visibility well beyond 2030.
We see large transmission programs across the country making positive progress from permitting and approvals to planning and engineering and moving closer to contract execution and backlog. Power generation opportunities are also active and in various stages, and we are encouraged by the stacking opportunity we see across our diverse markets building over the coming years. Technology is moving as fast as it can. Utilities are working to protect stakeholders, and Quanta sits at the nexus of facilitating both.
The proven success of our operating model on the utility side of the business is also why technology and large load customers are embracing it. The collaborative solution-based approach we have built over decades serving utilities is exactly what we bring to those customers. As evidenced by our results this year, the demand for our solution is significant and growing.
In this market environment, our scope and scale, the fungibility of our resources and the solutions they enable are valuable. So committing our resources to the best overall opportunities has never been more important. We prioritize high-quality, well-capitalized industry-leading customers that value our collaborative long-term approach and have multiyear infrastructure programs. We believe the power of our portfolio is that it does not overly rely on the pace of a single market, it builds on broad, diverse and resilient base and is supported by an increasingly flexible craft workforce.
Our self-perform model is designed to deliver on time and on budget at scale. None of this is possible without our craft labor, and you cannot buy craft, you have to build it. We are investing in curriculum and innovative training programs across our operations and creating industry-leading training environments, which allows us to attract and retain talent. We are growing our foreman and superintendent leadership, which we believe has a multiplier effect on our ability to enhance our craft and self-perform capabilities. Craft builds craft. We have invested heavily in our workforce for more than a decade. With a decade of strong double-digit compound earnings growth, the results speak for themselves. We are also investing in the expansion of our integrated fabrication solutions, which we believe is a workforce multiplier that increases speed and efficiency, quality and schedule certainty.
We apply the same absolute performance mindset to our capital deployment decisions. Each high-quality company that has joined Quanta is a relationship often cultivated over many years. We are patient in buying great companies, and we are disciplined around our strategy with culture and fit a primary criteria. Our recently completed acquisitions are great companies that strengthen our fabrication, engineering and supply chain capabilities and extend our ability to deliver integrated solutions for customers, and we welcome them to the Quanta family.
We are proud of the exceptional results our teams have delivered this year and the larger programs across the utility, generation and technology and load center markets are still in front of us. We are pacing ahead of the multiyear growth targets outlined at our 2026 Investor Day, and our conviction in Quanta's ability to compound profitable growth over the longer term continues to strengthen. We see the opportunity to deliver strong double-digit adjusted EPS growth again in 2027, supported by our record backlog and growing workforce. We remain focused on executing our customer success, deploying capital with discipline and compounding earnings and stockholder value over the longer term.
I will now turn the call over to Jayshree Desai, Quanta's CFO, to provide a few remarks about our results and 2026 guidance, and then we will take your questions. Jayshree?

**Jayshree Desai** (Executives):
Thanks, Duke, and good morning, everyone. The third quarter was an excellent one with record results across the board. Revenue was $12 billion, up 57% from $7.6 billion a year ago. Adjusted EBITDA was $1.4 billion, up 69% from the third quarter of last year, and our adjusted EBITDA margin expanded to 12.1%. Adjusted diluted earnings per share was $6.06, up 82% from $3.33 last year, and GAAP diluted earnings per share was $4.55, more than double last year's $2.24. Third quarter operating cash flow was $1.5 billion and free cash flow was $1.2 billion, both quarterly records.
Turning to 2026 guidance. We now expect revenue to range between $41.3 billion and $41.6 billion, up approximately $1.9 billion at the midpoint from our prior outlook. We expect adjusted EBITDA to range between $4.4 billion and $4.49 billion, an implied margin profile of 10.7% at the midpoint and adjusted EPS to range between $17.90 and $18.30. Regarding cash flow, after a historically strong first 9 months of the year, we now expect free cash flow to range between $2.5 billion to $3 billion, which would represent another annual record and reflect greater than 60% conversion of adjusted EBITDA at the midpoint.
During the quarter, we used our operating and financial strength to bolster our liquidity and financial flexibility, positioning Quanta to continue deploying capital in support of our growth strategies. In July, we upsized our revolving credit facility commitments to $2.98 billion and extended its maturity to July 2031. In August, we issued $2 billion of senior notes. And in September, we prepaid the remaining outstanding balance on our term loan. We ended the quarter with $2.3 billion of cash and had only $20 million drawn on our revolver. Total liquidity was $5.2 billion, and our bank-defined leverage ratio was approximately 1.3x, affording us ample capacity to support our strategic initiatives.
Regarding acquisitions, we continue to deploy capital with discipline. Subsequent to our second quarter earnings release, we completed 2 acquisitions for approximately $245 million of consideration, net of cash acquired. As Duke mentioned, these companies bring leadership and management team -- management talent and strengthen our front-end engineering fabrication and supply chain capabilities, enhancing our ability to self-perform more scope and deliver cost and schedule certainty for our customers. We believe our strategy is materializing into improved forward visibility. As of September 30, we had record backlog of approximately $64 billion, a $10 billion sequential increase from June 30, with backlog growth across each of our key markets.
To close, we delivered a record quarter, significantly raised our full year expectations and strengthened our balance sheet, all of which position us well to continue investing our resources from a position of strength. As Duke mentioned, our conviction in our ability to compound profitable growth over the long term continues to strengthen. Additional detail and commentary on our 2026 financial guidance can be found in our operational and financial commentary and outlook expectation summary, both available on our Investor Relations website. 
With that, we're happy to take your questions. Operator?

**Operator** (Operator):
[Operator Instructions] Our first question will come from Ameet Thakkar with BMO Capital Markets.

**Ameet Thakkar** (Analysts):
Congratulations and thanks for the update. Your electric continues to run well above, kind of, your long-term growth framework. Kind of, given what you're seeing in utility generation and kind of outpace load center demand, what are the biggest constraints to sustaining this level of growth in 2027? Is it, kind of, customer spending, labor or simply available to kind of execute? And then just on margins, how much of that strength kind of reflects favorable project execution versus kind of the mix or something more structural that we should think about as being sustainable?

**Earl Austin** (Executives):
I think the margin question, we had a great quarter. It's the third quarter. We've got some leverage as well. I do think that when you're thinking through it, if you think about the employee count, how much growth we had organically, you're growing 7,000 employees, 6,000 employees on both the previous quarter and this quarter and then, like, 25,000, 26,000 this year. It gives you some leverage with our training, and that's showing up. We've always said, look, we're pressing margins because of the training. But if we're getting that kind of leverage out of it, which I think is great, it's something that's certainly helping the margin profile of the company.
Look, we can operate the utility business 10% to 12%. We've said that all along. We're getting some leverage out of MEP in the business. You're able to do some off-site manufacturing, do a lot of different things to increase efficiency in the field. So we're super happy with what we're doing and where it's going. Has it fundamentally changed? Look, it's moved up. The UI is still down. I do think we can do much better there. We can get in the double digits. The profiles and things of that nature as old work burns off and we start to get into the newer business there, that should move up.
So look I like where we're going, I do think we can increase some margins, but it's not a margin story. I go back and say we're going to compound, kind of, the margin profile we've talked about. The utility business is still, call it, $20 billion or so of the electric segment. That's in the 10% to 12%, call it, 11%. And then you have the other businesses that we're getting efficiencies out of. I would turn to the ROIC, though, and look at that growth. To me, like, we watch that a lot of what we're doing with return on invested capital, and Jayshree can go through the numbers on that at some point. But I do think that's what's driving that.
As far as the growth and what's inhibiting the growth, I think the markets are there. We can't be everything for everybody. We continue to think that both the TAMs -- what gives me a lot of -- what I would consider optimism of the growth and us keeping that up is that we've done it for 12 years, well plus 20% growth. So I wouldn't bet against us on growth. And yes, big numbers, but it's been big numbers in my career. So we're just going to continue to compound those.
And when you think about the 2 TAMs, our utility business in the past, if you go back 5 years, we couldn't take advantage of the generation, the fossil generation, even the renewable generation, that wasn't us. We were in T&D. Now we have that whole addressable market. And I think it's a big deal and it goes unnoticed of how much TAM we have in the utility business. So if you look at that TAM, it's there and then you roll it over into what we're doing very early in our technology business, but the large -- the 5 largest technology companies will spend 3x the capital budget of the utility side. And we can perform the vast majority of that capital is in chips.
So I like our chances to grow. We talked about -- it's not just next year. We gave 5-year guidance, and we said 10% to 15%. If we can compound it would be 20% plus. We had a hell of a year. It's setting up. And I'm looking at '28, '29. I think we got growth out there as well. And we're not going to give guidance today, but I feel highly comfortable with, kind of, the 15%, 20%, and we'll compound that as well. But it's super early. I got 5 months. I'm going to take my time.

**Operator** (Operator):
Our next question will come from Justin Hauke with Baird.

**Justin Hauke** (Analysts):
That's with Baird, but that's okay. So obviously, a really strong quarter here. I think the thing that stands out the most is the sequential backlog gain. And there was a tiny bit of the contribution from M&A and you talked about the NiSource scope. But it looks like there was a lot more beyond that. And there wasn't anything like specifically quantified as a large project win. Just curious if there was anything chunky, any of the 765 lines you've talked about. I know there were some questions on some hearings on some of those in Texas that seemed like they went favorable. But anything you can comment on kind of the contribution makeup of the backlog?

**Earl Austin** (Executives):
Look, it was broad-based backlog growth. I mean our renewable business is fantastic. It went all the way across the segments. We did book the one NiSource, but that's a program. If you can listen to their capital and what they're doing, it's a larger program. I expect us to book more there against that. It was both T&D and the power plant that we had discussed. And I really like what we're doing with the largest customers in the industry. We're standing by them. They want to build fossil, we'll go build fossil. We're super happy to do it. We believe we have a good model to do that and derisk the customer -- the end customer as well as us.
And I think that's key for us in that business. And when we look at just straight up to -- our distribution business is growing nicely. Transmission business is growing nicely. So no -- nothing really pulled in. We haven't started really the 765 build. It's much bigger than Texas. You have the Ohio work. You have MISO work. There's a lot of work out there that is not in backlog yet. In many ways, it's just getting started.
We say it all the time, but I'm not seeing big projects. That's not what's making up the company today. And it's a heck of a growth underneath it without the stacking of those in here yet. So I believe you'll see -- in the future, you'll start to see the generation business come into the business as well as the large transmission, which is not in there today, but we talked about growth, that's growth, that's stacking growth that we'll see in the outward years.
So super happy where we sit. We think we've done a real good job. I think the business 10 years ago, 5 years ago, it was very transactional. And today, I think it's more transformational. And we're running a transformational business that compounds earnings over time, and that backlog is broad-based.

**Justin Hauke** (Analysts):
If I can just squeeze one more in for Jayshree, just on the cash flow. It looks like there was a decent amount of prepayments in the contract liabilities. Is that just -- maybe just -- is that favorable terms on the contracts? Or is that really a function maybe of some of the prepayments on some of the modular and the capital investments you've made on the supply chain? I'm just curious the contribution of that in the working capital.

**Jayshree Desai** (Executives):
Yes. Thanks, Justin. No, as you can see, our working capital is continuing to improve. That is more of a function of the contract terms we're getting on a significant part of our revenue, especially from our MEP, our EPC business as well as our renewable business. All of those are contributing to that favorable working capital profile you're seeing. Our DSOs continue to improve. So we're pleased at where our free cash flow is coming in. That's why we raised it for the year.
There are some things we're doing around our supply chain as well as the -- as Duke mentioned in his prepared remarks around the expansion around our OSM facilities that actually are a use of cash. So I would just say, in general, what we told you in March continues to be the right way to think about our cash flow profile around 55% to 60%. This year, we look to be at the high end of that, actually higher than that. And our expectation going forward will depend very much on the mix of work around those factors I talked about. But 55% to 60% is still the right way to think about it, Justin.

**Operator** (Operator):
Our next question will come from Julien Dumoulin-Smith with Jefferies.

**Julien Dumoulin-Smith** (Analysts):
Nicely done. I got to hand it to you guys seriously. I wanted to come back to a couple of things you said. First off, you said inbound interest is accelerating, I think, to quote you from the transcript. Yet at the same time, Duke, you've put up 2 quarters in a row, I mean, several quarters in a row, but more than the point, just really exceptional quarters. Is it conceivable that you accelerate on the cadence of backlog additions? I mean, if I'm hearing you right.
And then related to another point you made earlier here on ROIC, how do you think about the scope of possible here, economic ROIC here? I mean, you've been putting up a point or so every year or maybe even more than that of late. Trajectory-wise, do you think that's the right cadence here through the forecast in as much as you say you're focused on that ROIC metric? Just how do you think about what that trajectory could look like, if not margin expansion, just to use your economic term you're focused on?

**Earl Austin** (Executives):
I mean, look at better terms on our contracts. So I do think we're generating free cash at a faster pace. Jayshree is probably unwilling to go there in guidance yet. But I do think that's happening. We are leaning into some supply chain, Julien, which I'm worried about copper, I'm worried about other things. And so we will use that balance sheet to mitigate risk for our clients. And if they can't see it, I can. And so I get to see it broad-based. So we'll lean into some of those supply chain constraints to keep our people busy.
Margins are expanding. The use of capital in these lighter capital businesses that we have, such as inside, that's certainly a bigger portion of what we do. So it's going to expand the ROIC. And how fast? I'm not signing up for that quite yet, but it's certainly something that we're highly focused on and the cadence thereof.
As far as backlog expansion, look, I believe we'll set records and continue to set records. The timing on that, it gets lumpy for us. A lot of MSAs coming in, a lot of good things happening. So what I would say is, I mean, we've stayed true to -- it's not in backlog until it's signed. And so that for us, some of that, kind of, $1 billion beat over the last 2 quarters is because it's book-to-bill, we're moving building to building or job to job without ever -- without it ever hitting backlog. So I'm not sure how to classify that. GAAP says for us, at least not GAAP, but the way our SEC requirements and the way we think about it is it's signed. So that's just how we're going to go about it. And over time, we've been doing it that way 10 years. We're not changing now. So it's just going to be that way. And I think you're going to get some lumpiness in it. I would say, as far as what the outlook of the business and what we see, the inbounds coming in certainly is moving at a faster pace than it's ever moved in my career.

**Julien Dumoulin-Smith** (Analysts):
Got it. And just on the data center front, real quickly to ask about that. How do you think about the right to win and what this is going to look like? Is this a partnership like with NiSource example, where you have like multiple sites? Or how do you think about moving into that sector? I mean, obviously, there's stuff beneath the surface, you guys haven't released -- press release formally already cooking. But how do you think about that TAM and tackling it and what we'll see more visibly?

**Earl Austin** (Executives):
Yes. I just think we're doing it now. I mean we're providing behind-the-meter generation that's going to utility generation. So utility-scale generation today, I mean, and balance of plant and balance of facilities in multiple areas. So we're doing that today. We just -- we didn't press release, we didn't say anything about it. We don't need to. We just go up, put the numbers up. And I think that's the key.
But the clients and both from the technology side as well as our utility customers, we're in the middle of that building that whole thing out. When you look at it in a geographic area, if we're doing everything in that area with our people, which we self-perform 85%, we have a lot of control of certainty. And we don't have people jumping trucks. We don't have the issues that others have, the scale of the company, the growth of the company and what we're able to accomplish because we can perform all of it is certainly beneficial to the end user and to the ratepayer.
And I just think as we're able to do more, we can certainly help with labor on those sites, those big area, I mean you have 5,000, 6,000, 10,000 people. If we can control that environment, it's certainly helpful. It keeps the wage pressures down and things like that. So yes, I mean, the clients are coming to us. They see it on both sides. We're able to really give them something they want. They want certainty and they want speed. If that's the 2 things, the criteria, I like our chances. So -- and that's what we're seeing today out there. So I do think as we see it, we're in the right spot doing the right things, and you'll continue to see more and more.
We were about -- if you look at on a megawatt basis for MEP and say it's $15 million a meg, everybody has a different classification. So CEO math or whatever you want to call it, but it's $15 million a meg, say that the company was getting $3 million or $4 million a meg a year ago. We're able to expand that into $5 million to $7 million. And as it goes farther, that will be $7 million to $10 million. So you can see us just capturing more and more of what the spend is per location, and that's not counting generation or utilities behind it. So I just -- we're getting more and more as we move forward. We're creating more verticals in the business. I like our growth patterns. I like our strategies, and we're doing well. So thank you.

**Operator** (Operator):
Our next question will come from Nick Amicucci with Evercore.

**Nicholas Amicucci** (Analysts):
So Duke, I just wanted to see, it seems like you guys are, especially this year, kind of positioning for the higher end of that 15% to 20% EPS CAGR growth target through 2030. Just wanted to see, like, kind of, the probability seems in your favor that you're going to get to, kind of, that full stack scenario. So I would just say -- I would just ask how do you see the opportunities that would drive the full stack really coming together? And where do you see the company really going from here?

**Earl Austin** (Executives):
Yes. Look, we're performing well above expectations. If you add -- if you take the 20% onto this year, you're well -- you're already in the -- basically the low end of the plan. And so very close to it. And I just -- the acquisition profiles, the companies that we're able to acquire, what we see out there, what we see, and I'm not signaling that we're going to go make acquisitions -- but we have in the past, and I continue to see opportunities for us to deploy capital in the right places with the right businesses. If we see that and we continue down this path, sure, we're going to be well above plan and probably be talking about something different earlier than 5 years because we're going to have to.
I do think as we see it, the markets -- there's risk to the markets. There's things that are out there in these long plans. So that's why we give you a good CAGR basis, and we're ahead. We're certainly above 20%. But we've operated above 20% on a CAGR basis for 12 years. And I think it's one thing to say it, a lot of people go out and they talk about it, talk, talk, talk about what they've done. I just say, look at our past, look what we've done, and it's predictive of the future.

**Nicholas Amicucci** (Analysts):
Definitely fair. And then as we kind of think about the past, too, just you guys have always been very prudent on kind of the risk profile of contracts. And so I just wanted to make sure that kind of less than 15% of revenue that was tied to fixed-price contracts exceeding $300 million that you guys outlined at the Investor Day. Is that still representative just given the magnitude of the recent awards and your recent acquisitions?

**Earl Austin** (Executives):
Yes. I mean the way you define -- I would say our risk profile, whether how we define it because you can define it in what a fixed price, you can have UPIs or some measure that allowed it to be derisked. There's a lot of ways to derisk these things, the GMP profiles, all the different ways to contract. No matter what you call it, I look at every one of them. And I would say the risk profile of the company is in a better position than it's ever been.

**Operator** (Operator):
Our next question will come from Steven Fisher with UBS.

**Steven Fisher** (Analysts):
Just, Duke, you mentioned some of the larger transmission projects that you have in the pipeline here. How close do you think we are actually to getting those programs in backlog? And how should we think about in terms of maybe order of booking, Texas versus Ohio versus MISO? Those are the few that you mentioned.

**Earl Austin** (Executives):
Yes. I mean I think we have LNTPs and things like that on multiple projects. We have things that we're doing with AEP. So we've talked about that where we're supplying -- doing some supply agreements and doing some agreements with them. And you can see what they're doing and with their capital. I think the business is tripling and super happy to work with our clients. And I think I'm not rushing them to get them signed. We want to take our time, both sides need to. The environments are moving, and they have their own customers on the backside. I want to get it right.
But we'll be on 765 in '27 for sure. Some of that's not booked already. So it's hard for me to say. Some are booking earlier LNTPs. We need to order material in places and do some things like that. I think you'll see really good bookings, call it, first half of '27 and even some starts. I'm not sure the cadence on that. It's hard to say. We're probably farther along in, I don't know, Texas, Ohio, probably be the first 2 to go.

**Steven Fisher** (Analysts):
Terrific. And then, Duke, on your mission to provide certainty of delivery, do you think there's still some important big pieces that are missing? Or are you really at this point, kind of just filling in the more kind of strategic-focused but smaller pieces of it?

**Earl Austin** (Executives):
I mean we talked about it in length, I mean, poles, wire and transformers, and we thought that those would be the short items, and we're not wrong. So we've leaned into transformers, breakers. This quarter, we acquired a pole manufacturing facility and a company, a nice company that we've been talking to for over 5 years. And I think we see it, we see poles coming out of Mexico in various areas that we're waiting on material today. So we're going to solve those problems.
I mean it won't be -- our growth will be dependent on the OEMs. It will. It always has been. Everyone is worried about our labor constantly, and we grew 26,000 people this year. So I'm waiting on material. I'm hoping they hurry up. And if they don't, we will lean into it. We have to, to keep our customers moving, keep the supply chains moving. And we're not a manufacturer at heart, but if we need to be, we will be. And we're going to provide the solution to these clients when we see it. If we see issues out there, the company will lean into those issues with our clients and move it forward. It's the right thing for the ratepayer.

**Operator** (Operator):
Our next question will come from Jamie Cook with Truist Securities.

**Earl Austin** (Executives):
That's a good question.

**Operator** (Operator):
Our next question will come from Michael Dudas with Vertical Research Partners.

**Michael Dudas** (Analysts):
Duke, you highlighted -- maybe your thoughts on over the next several quarters, several years, what is the risk to the market or what your utility or hyperscalers are thinking about that might cause some delays or slowdowns? Or is it just the supply chain and the labor issues that you guys have gotten your handles around to provide that turnkey solution because sometimes the market seems like the risk to the end of the cycle is quite dramatic relative to what a peer's reality is?

**Earl Austin** (Executives):
Yes. I would just say our inbounds are accelerating as far as what our clients are telling us. I don't -- they're doing things in years, 2 years kind of time frames and the demand is there when you listen to calls, when we listen to them and they're asking us for solutions out to 20 -- well past 2030. So we're just basically positioning the company for what we're asked by the client. We're staying very close to the customer.
I do think when you think about it, if you think about demand that's out there, we're building factory in 10 states, something like that, that's going to create close to 1,000 jobs against all these markets. So I'm waiting on power hookups in 2 or 3 factories. And the people that are building it are the people that are building data centers. So the very fungibility of labor, what we see here, I don't think labor is going to be the issue. I think it will be supply chain, critical items in supply chain to always lean into these things. I mean, you can see what GE did yesterday or day before whenever they did that, the criticality of their supply chain. And we have to lean into it as well on the things that we do.
So I like what the manufacturers are doing. Almost every OEM is expanding. It certainly helps us. It makes me feel more comfortable with where the markets are going and our ability to be certain on the time frame. So as long as those things stay intact and the things that we're doing, the good that we're doing for the country out there with labor and communities and things like that, that I know the political rhetoric and all the rhetoric that's out there. But the reality is, it's a very good thing for people and for teachers and for communities. And it's much like the Industrial Revolution. We're doing great things. The industries are doing great things. We're super proud to be a part of it and we see growth.

**Operator** (Operator):
We'll go back to Jamie Cook with Truist Securities.

**Jamie Cook** (Analysts):
Can you hear me?

**Earl Austin** (Executives):
Yes, ma'am.

**Jamie Cook** (Analysts):
Perfect. Sorry about that. All right. Duke, so now you get a tough question because I screwed up on this. I guess my first question, understanding the growth that you're seeing in data centers and looking at the margins relative to some of your public peers, as data center is one of the higher growth markets and given where your margin -- the peers are of your margins, why wouldn't structurally Quanta's margins improve greater than the 10% to 11% that you target? Is there any like structural reason why your margins can't be where your public peers are?
And then my second question, I just want to understand how you're thinking about the M&A pipeline. Obviously, it's been focused on getting more in data centers. But I'm just wondering how -- if you want to move sort of out of power more so and consider other markets within your large load market that you talked about, like advanced manufacturing, infrastructure. Just wondering if we're going to start moving beyond power, whether it's besides utility data center, if that makes sense?

**Earl Austin** (Executives):
Yes. I got it. So for the margins, Jamie, I don't think anyone has a $20 billion utility business that we would be compared to. I don't know who it would be, maybe all of them put together. So that said, I mean, if you fundamentally, we're not going above 10% to 12% in there by design. We're going to stay there. The ratepayers, what we're pressing on, we're not doing it. So we'll compound it over time. It's been a great business for us. We're part of that industry, and we understand what it takes to be long there. What I would say is I see decades of growth for this company. We've done a nice job staying part of that fabric. And we're not going to get transactional. We're going to stay transformational and continue to compound. So that's going to be there in that business and continue to grow nicely in the utility business.
As far as MEP, we are getting some efficiencies with our advanced manufacturing. We're doing some good things there. It is pressing upward on those margins in that segment. And it's still only 20% of the business, give or take, probably 15% to 20%. And when we look at it, I think that's -- because the utility business is growing nicely, our renewable business is fantastic. And that's another issue. You got a real nice renewable business, $5 billion to $10 billion of renewables in there. So I think when you look at those 2 businesses and what we're doing from capital and return on invested capital, we're getting the right growth of return. And I think that's the key to it. But it's compounding. And it's not something that's going to have wildly margin increases.
We are enhancing the underground segment. I do think there's room there. We are improving there. We're getting efficiencies. You can see some leverage coming in. Our training now when you're looking at training, people get scared of heights. And instead of dropping out of programs, they can be a plumber, a boilermaker, electrician and stay on the ground. So we're creating craft and that creates efficiencies within that. So we're picking up some efficiencies there.
But as far as margins, I like what we're doing. We're derisking the company along the way, better cash flows, better returns. So I like where it's going. It's got the right trajectory. But as far as pure operating income margin expanding to some astronomical level, I don't see it. I just -- I think we'll compound it. We'll continue to increase a little bit, certainly have room in the UI. But we execute through a lot of different variables that go unnoticed. I mean, fuel is up, insurance is up. I'm sure someone will be talking about fuel somewhere. It's -- we run right through all that, never say a word, move along, compound earnings. And we make sure that we account for all those things and guidance and the things that we say. If we operate through all that and Canada becomes world-class like Lower 48, yes, margins are going to move up.
And as far as M&A, I do think like we're very cognizant of the hockey sticks on data center. We're not buying a pure data center company per se. Like I look at it constantly to say like the businesses that we acquired, if our data center business cut in half, what would it do to the company long term? And it's -- we're in a very good position. It does -- sure, it comes down a little bit, but it does not -- we don't fall off a cliff, and we continue to still see growth in the business. So we can still see growth without data center. Our pharmaceutical businesses are -- what we're doing in power plants, what we're doing across the board, you have 50% of this growth in the utility business is not data center, by the way, like -- so we have growth in the utility sector without data center. We haven't had that in 20 years. Our distribution business, all the things that we're doing, all the things that they're doing, it's fantastic, I mean, across the board. So super excited and it has -- we like the fact that data centers are there, but we're not acquiring against it for sure.

**Operator** (Operator):
[Operator Instructions] Our next question will come from Sherif El-Sabbahy with Bank of America.

**Sherif El-Sabbahy** (Analysts):
Duke, you've said you don't expect labor to be the restricting factor going forward and you talked about getting more productivity out of your existing labor base. But with demand the way it is, do you need to accelerate the rate of hiring from the 6,000 or 7,000 a quarter it's at now? And if so, where could that go? And what investments do you need to make in training?

**Earl Austin** (Executives):
I mean I think we'll continue to train. I mean it's an expense. So that's not going anywhere. We continue to invest in it. I don't think you'll invest any more than we already have and may actually go down some. But -- because we're getting some leverage. But look, I don't -- you've got seasonality, you've got quarters that you won't grow as fast as well. I mean the first quarter certainly wasn't like the second and the third. And so you'll come down in some seasonality. We're able to -- fungibility, you can see our fourth quarter kind of stays flat now to the third. And when you think about it, those -- the people in Northern climes are moving around our system and moving to other things. The first quarter still falls a bit, but it naturally does, it always has in seasonality. 
So I think you'll lose some headcount in the first a little bit. But they're moving around more. We're moving segment to segment. We're moving company to company. We're moving across our -- what I would consider verticals, which is good. So we're getting more efficiencies out of the labor that we're training, but we still -- I mean, I still see the company, kind of, in the, call it, 6,000 to 8,000 a year on the average and then you'll have outward years where you're growing like we did this year. Some of it's acquisition, but I still think the organic growth is around, call it, 12,000, so something like that of organic growth. And I would say the organic growth of the company, we heard a lot about that organic growth, organic growth. I hope everyone looks at the numbers of the organic growth of the business, and maybe we can stop talking about that now and talk about what we've done organically. That's because we invested in the labor.

**Operator** (Operator):
Our next question will come from Andy Kaplowitz with Citigroup.

**Andrew Kaplowitz** (Analysts):
Duke, I'm going to take your softball about asking about fuel in a different context. I think this is a quarter that everyone in industrials is concerned about inflation and price versus cost. But obviously, you delivered strong electric power margin, as you said. So obviously, there's some positive mix, but maybe it's your vertical integration that's helping you. But maybe you could talk about how much better positioned Quanta is to handle inflation versus a few years ago where it did kind of show up in your electric margins.

**Earl Austin** (Executives):
Yes. We've done a nice job with the supply chain as well as just in general, I think we've always had pass-throughs on labor escalations in our utility business just the way by design. So I think we've done a good job with labor and being able to really from a risk standpoint, mitigated. We've done that forever, and it doesn't show up much. The things that are like for us, like health care, insurance, just risk and insurance, things like that have escalated faster than other things. And we have seen inflationary things in the business. We've got a lot of efficiencies. We haven't passed all that -- had to pass all that through to the client, which is nice.
And so we're -- I think the good thing is, the industry is working together in a collaborative manner. And as we do that, if we can do that with them, we can off-site manufacture. We can do a lot of things that make tons of sense where we both don't have to add people and what I would consider supply chain initiatives, all kinds of different things that we can do together. If we do that and think about it as a solution, we can reduce cost for the client. And for us, it increases top line as well as our margin profiles in many ways on these solution-based approaches. So we've been able to do that, and that's why that inflationary piece hasn't came into the business because we've been able to absorb it. But I do think, look, scale matters. It matters in the utility business. It matters in every business. We continue to create scale within the business. And I wouldn't underestimate that. It means a lot for us, and it means a lot for the business for us to continue to scale it.

**Operator** (Operator):
Our next question will come from Liam Burke with B. Riley Securities.

**Liam Burke** (Analysts):
The Underground Infrastructure segment is seeing very steadily improving operating margins, both from the fourth quarter last year and then sequentially. Could you give us some color as to what's driving that improvement?

**Earl Austin** (Executives):
Thanks for noticing. Look, it's work mix, a lot of it and a lot of it is the risk profiles that we're willing to take on 2 different things. I think we've added our mechanical businesses in it. We have some of our civil business in it. It's on both sides of it. Those additions are certainly something that are pushing it up. We'll continue to grow our mechanical business faster than anything else. With some growth in our traditional business, not as much.
So we're -- what I see is the work mix is changing it such that you can get into double digits fairly quickly. And it's incrementally happening. You can see it throughout the quarters, the growth. And I think it's getting to sustain -- you'll have some seasonality in the first quarter. But I do think in the next year, you could see us in double digits and quarters and get on a run rate there in the next year. So exponentially getting that up into the double-digit range.

**Operator** (Operator):
Our next question will come from Philip Shen with ROTH Capital Partners.

**Philip Shen** (Analysts):
And congrats on your strong bookings in the quarter. I wanted to explore the data center outlook some more. I know inbounds have never been greater, and you've spoken very positively about this opportunity. That said, some of our checks suggest some data center work may be sliding or even going dark. Duke, can you give a little bit of color on some of this risk that projects could be sliding? And then what is the potential for maybe a slowdown or just some pushouts in '27 or '28? Or are you able to just backfill some of the things that are pushing out? So a little bit of color on some of the -- if you can lift the hood a bit so we can see, that would be great.

**Earl Austin** (Executives):
Yes. I mean I think for us, it's much like our renewable business. We said all along when the sky was falling there that we work for the top 10 best. And from a developer standpoint, I would say the same applies to the data centers. I mean we're working for the very best in the world at this and the most liquid balance sheets that you see in the world. And all I can say is, we can't even get to 25% to 30% of what they have in front of us, and we're having to basically look out 5 years and see how much we can take at this point.
All I can do is tell you the inbounds that we see -- and when we sign contracts, we put it in backlog. Our backlog is growing nicely, not only 12 months, but beyond 12. All the investments in -- that you see in engines from GE that are 3 years out, all the investments that you see in factories that are coming. It's creating businesses as well with pharma and things like that. We have fungibility of labor as well. So if they're not -- we're building chip plants or we're building pharmaceuticals or we're doing a lot of different things with that same workforce if we're not -- so we're able to move across segments and move across verticals. If something was to slow, I'm not concerned at this point.
But the data center demand is there. We see it. That's all -- all I can say is what we see on a daily basis, the inbounds that we get at the very highest level of everyone that we talk to. The cloud-based environment, just the cloud alone, which is the majority of what we do, that inference-based cloud-based business has been there for 10 years and has done nothing but go vertical. And I continue to believe that's the case. You may get some learning centers that slow a little bit. It's very little of our work today. And I just -- I'm not as concerned as the market may perceive it at this point.
We still see large projects, and we see the cloud-based business growing much like our MSA business in the utility side, and we continue to capture more of the spend as we move forward. So I don't -- I think we're early stages for us. We're creating something like we did in the utility side and that's coming from the technology side now. And if it was to slow, we -- the company will capture more of the spend anyway. So I don't know, it's growth on growth right now, and I don't see it stopping.

**Operator** (Operator):
Our next question will come from Alexa Breno with Goldman Sachs.

**Alexa Petrick** (Analysts):
Can you just talk a little bit about what the dialogue looks like on the hyperscaler side? Are you seeing them engage with you earlier in the development process similar to your utility relationships? And then how do we think about that in the context of the scope of the work that you could be doing?

**Earl Austin** (Executives):
Yes, they're engaging early. I think a couple of things, community-based engagement. We're seeing our labor, how do we collaborate on labor, how do we collaborate on hiring. So yes, it's early. We can help a lot with the dialogue of actually what's going on with the workforce and the community. So I think just being a part of the industry there, the company is moving in the right direction. We're having great conversations at very highest levels with that side as well. So we're working hard to create the same environment and the same trust that we have. It's a trust thing.
So I do think the company has a long track record on generationally in the utility business. And the same applies, I mean, Cupertino grew up with the industry. And their reputation is every bit as good as anyone in the world. They do a great job and very customer focused. So the whole company is customer focused. And as long as we stay like that, we'll continue to see inbounds from the very biggest in the world at the early stages of these projects where we can really make a difference in the community. And certainly, I feel like if we're able to do that, that's what creates us to be a part of that fabric as well and create the moat that we have in the utility side is make sure that we are enhancing our customers' ability to build and perform much like we are.

**Operator** (Operator):
Our next question will come from Alex Rygiel with Texas Capital Securities.

**Alexander Rygiel** (Analysts):
Duke, I was curious about your reference to increasingly flexible craft workforce. What do you mean by increasingly flexible? And what's, kind of, different today versus, say, 5 to 10 years ago? Because obviously, you've had a pretty tremendous training program in place for many, many years. But the comment of increasingly flexible, kind of, caught my ear.

**Earl Austin** (Executives):
Good. It was intended to. So thanks, Alex. I think what we're saying is we were really confined to the utility business. And if you can't climb, it's very difficult to stay in our craft. You can drive trucks, you can do other things. But now, like, a person that can't climb, but as intellect for math and the things that you need for -- on the electric side or even plumbing, we're able to put them in a different craft because of our expansions in the verticals inside electrical voltage, boilermakers, pipe fitters, plumbers. We've really expanded the company over the last 2 to 3 years of what craft we have and how big we are in each one of them as we moved in.
So I think the flexibility for us to take a person and say, where do you want to sit in this? Here's the wage profiles and here's where we can go across the country. As we recruit, we can move people all the way through and our recruitment goes way up because of the things that we can do. I just -- it's certainly there. And then when you get in the trade, I mean, you can -- an electrician can go from a power plant all the way through basically to a home, it doesn't matter where if you get in the high-voltage side, yes, they can come down and do some low-voltage work, but it's much -- it's just different. They usually don't. And so it's not as fungible.
So I think we've created the fungibility of a craftsman to move across the system. And if they don't want to be in the high-voltage arena, we can move them into low voltage or we can move them across. So I just -- we've done a nice job with that training and the way their curriculum craft and how we think about craft and how important they are to the heartbeat of this company. We value it. And I think people resonate with that, especially in the field that just resonate with our ability to create an environment for them that they can go as far as they want in this company, and we're going to continue to do that.

**Operator** (Operator):
Our next question will come from Dimple Gosai with Piper Sandler Companies.

**Dimple Gosai** (Analysts):
We've heard a lot of commentary just about large data centers that have spoken about risk of just getting physical gas pipelines to data centers today. How do you think about leveraging this opportunity to win some of the programmatic work that you could potentially benefit from?

**Earl Austin** (Executives):
Yes. Look, on the gas side, we're winning work. We're doing a nice job there. We're in the business. And I do think you're starting to see expansions. You're going to need gas pipe. It's going to expand. I think that market, if it's not -- I'm confident in '27, you're going to see expansion of pipe and things like that, that we're in that market, we're going to take advantage of it. We've got great clients there that we're supporting. Some of them are on the electric side now, building gas generation in places. So we're working for them there.
And we're not giving up on it. I just -- we're going to be cognizant of the risk. And I don't -- we don't want risk we can't control. I can't control the weather, I can't. And so I'm -- we're not going to go into businesses where I have to give you a weather report, not doing it. We haven't done it in 7, 8 years, and I couldn't stand it when we did it in the past. So we're really trying to derisk the company from weather and things we can't control. So if we can control it, we can execute against it. We have the very best craft in the world, I'm not concerned. But we got to be able to control it. So we'll be risk tolerant on those things, but the market is there going forward, and you're right about what you're saying in a systematic way, you've got to feed all this gas generation with pipe. It's got to be done.

**Operator** (Operator):
Our next question will come from Brian Brophy with Stifel.

**Brian Brophy** (Analysts):
Congrats on the very good quarter. A couple of quarters ago, you mentioned $500 million to $700 million of incremental manufacturing-related CapEx over the next few years. Just curious how your views have changed here given some of the supply chain constraints that you mentioned and any other opportunities you're seeing on that front?

**Earl Austin** (Executives):
Yes. I said it a minute ago, I think we have like 10 states that we're increasing our manufacturing capabilities, whether it be transformers, breakers, all across poles now that we acquired. So I don't think it's going to be a huge part of the business. We're certainly going to lean into where we need to, to make sure we stay in front of the demand. We're also having great conversations with the OEMs to be good partners and to try to go along on things that we need to with them and partner with them. I think that's really important as well. They're important to us. We value what they do.
So we're probably in the top 5 buyer of -- we are in the top 5 buyer of HV equipment. And so I think that's important that not only are we building and putting capital in, we're also partnering and doing some things with our OEM providers that allow us to be certain on projects. And that's going to be important going forward as we see constraints. And so we recognize those things, Brian, and we're staying in front of them as well as investing capital in them where we think we have good backstop, long-standing relationships that we're not just going to go out and build factories without the demand in front of them.
So we're trying to get long on those things. And we've been able to do that and primarily to keep the workforce busy and get exponential growth. It's -- the business itself is great, but what it can do for our overall business is 10x what the factory can do. So those expansions are meant to grow the business and a multiplying effect as we move to the field and EPC and all those things. That's really what it's about. It's our ability to go EPC with certainty.

**Operator** (Operator):
There are now no more questions at this time. I'd now like to turn the call back over to management for closing remarks.

**Earl Austin** (Executives):
We want to thank the men and women in the field. They make this possible. They are the very best in the world, and we want to thank our shareholders for participating in the conference call. We appreciate your questions and ongoing interest in Quanta Services. Thank you. This concludes our call.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### PWR_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO｜guidance：CFO 上調 2026 全年營收指引區間（原話："revenues to range between $39.3 billion and $39.7 billion"）
- 2026-07-30｜CFO｜guidance：CFO 給出全年調整後 EPS 指引區間（原話："adjusted EPS to range between $16.45 and $16.95"）
- 2026-07-30｜CFO｜guidance：新指引內含四家併購的營收貢獻（原話："$1.2 billion to $1.4 billion of revenues"）
- 2026-07-30｜CFO｜guidance：新指引內含四家併購的調整後 EBITDA 貢獻（原話："$120 million to $140 million of adjusted EBITDA"）
- 2026-07-30｜CFO｜capital_allocation：CFO 說明負債對 EBITDA 比率自 2025 年底 1.95 降至 1.7（原話："our debt-to-EBITDA ratio improved to 1.7,"）
- 2026-07-30｜CEO｜margin：CEO 表示下半年毛利率仍有上行空間，且指引採保守做法（原話："So yes, I think there's upside in the back."）
- 2026-07-30｜CEO｜margin：CEO 重申電力部門利潤率能力的口徑（10 至 12，12 為上限）（原話："the electric segment has the ability to operate 10 to 12"）
- 2026-07-30｜CEO｜margin：CEO 答覆地下與基礎建設部門利潤率可能追上電力部門，先求達雙位數（原話："let me get to double digits first"）
- 2026-07-30｜CEO｜margin：CEO 稱地下部門有機會與電力部門持平，取決於工作組合（原話："I do think we have opportunities to get at parity"）
- 2026-07-30｜CFO｜margin：CFO 答覆本季無一次性項目（回應 SunZia 結算問題）（原話："There was nothing onetime in our quarterly"）
- 2026-07-30｜CFO｜guidance：CFO 稱自由現金流轉換率口徑約 55%（Investor Day 提過 55% 至 60%），並認為今年可達區間高端（原話："rate of around 55%."）
- 2026-07-30｜CFO｜customer：CFO 稱合約條款對現金流與營運資金有利，且遍及各業務（原話："We are getting favorable contracting terms"）
- 2026-07-30｜CEO｜competition：CEO 回應部分公用事業自建燃氣發電的趨勢（原話："Yes, it sounds easy. It's not."）
- 2026-07-30｜CEO｜risk：CEO 說明對複循環與單循環燃氣機組 EPC 的風險立場（原話："not willing to take the risk on the combined cycle side"）
- 2026-07-30｜CEO｜commitment：CEO 稱 NiSource 相關工作大部分將於第三季進入在手訂單（原話："a significant amount of that will go into backlog"）
- 2026-07-30｜CEO｜commitment：CEO 預期第三季甚至第四季在手訂單續創新高（原話："record backlog into the third and probably even into"）
- 2026-07-30｜CEO｜customer：CEO 描述傳統輸配電業務成長口徑（原話："upper single-digit growth in the business as it sits"）
- 2026-07-30｜CEO｜customer：CEO 說明大型輸電專案預計進場施工的時間點（原話："second half of '27, you'll start to see us go to the field"）
- 2026-07-30｜CEO｜customer：CEO 給出科技業務占整體營收比重的口徑（原話："15% of the business is technology, call it, 15% to 20%"）
- 2026-07-30｜CFO｜risk：CFO 說明資料中心專案列入在手訂單的規則（原話："we tend to put in things that have only LNTPs"）
- 2026-07-30｜CEO｜risk：CEO 回應紐約州資料中心暫停令對公司影響（原話："having a moratorium in New York doesn't bother me at all"）
- 2026-07-30｜CEO｜customer：CEO 否認本季有訂單提前拉貨（原話："nothing pulled in at all that I'm aware of"）
- 2026-07-30｜CEO｜risk：CEO 稱產能充足、無人力吃緊（原話："we're nowhere near capacity"）
- 2026-07-30｜CEO｜competition：CEO 稱近期不會看到技術工人供給過剩（原話："we're not seeing any oversupply of craft-skilled"）
- 2026-07-30｜CEO｜capital_allocation：CEO 稱每年訓練支出約 2.5 億美元（原話："we spend about $250 million a year in training"）
- 2026-07-30｜CEO｜capital_allocation：CEO 說明併購節奏不均：上季 0 件、本季 4 件（原話："Last quarter, we did zero. This quarter, we did 4."）
- 2026-07-30｜CEO｜capital_allocation：CEO 表示不看 EBOS 類公司（原話："I'm not looking at EBOS companies"）
- 2026-07-30｜CEO｜capital_allocation：CEO 說明垂直供應鏈投資將選擇性進行（原話："We'll be selective in how we invest there."）
- 2026-07-30｜CEO｜product：CEO 說明預製與整合製造面積擴增（原話："talked about having 7 million square feet"）
- 2026-07-30｜CEO｜product：CEO 答覆 800 伏特架構相關招標尚未出現（原話："We haven't seen it show up."）
- 2026-07-30｜CEO｜guidance：CEO 說明管線業務預算內部設定的口徑，並稱已超過（原話："we kind of put $500 million in our head"）
- 2026-07-30｜CFO｜guidance：CFO 答覆併購貢獻約為半年份，可自行年化（原話："It's about 6, 7 months worth of what we gave you."）

### PWR_Analyst_Investor_Day_Quanta_Services_Inc_20260331.md
- 2026-03-31｜Jayshree Desai｜guidance：2030 目標：有機營收 CAGR 7%–10%（原話："grow organic revenue by 7% to 10% CAGR"）
- 2026-03-31｜Jayshree Desai｜guidance：2030 目標：調整後 EBITDA 利潤率 10%–11%（原話："the ability to generate 10% to 11% adjusted EBITDA margins"）
- 2026-03-31｜Jayshree Desai｜margin：利潤率擴張幅度相對 2026 財測高標的口徑（原話："an 80 basis point expansion against the high end"）
- 2026-03-31｜Jayshree Desai｜guidance：2030 調整後 EPS 目標區間（原話："targeting an EPS and adjusted EPS range of $21.60 to $26.75"）
- 2026-03-31｜Jayshree Desai｜guidance：EPS 複合成長率目標（含資本配置）（原話："grow 15% to 20% compound annual"）
- 2026-03-31｜Jayshree Desai｜guidance：管理層稱不含併購的有機 EPS 可達雙位數成長，未給具體有機 EPS 目標（原話："achieve a double-digit EPS growth organically"）
- 2026-03-31｜Jayshree Desai｜guidance：全部機會疊加時 EPS CAGR 可超過 20%（原話："we should see an adjusted EPS CAGR of north of 20%"）
- 2026-03-31｜Jayshree Desai｜guidance：2030 營收區間 440–490 億美元（原話："organic revenue CAGR, $44 billion to $49 billion"）
- 2026-03-31｜Jayshree Desai｜guidance：2030 ROIC 目標 12%–15%（原話："we now expect a 12% to 15% by the end of 2030"）
- 2026-03-31｜Jayshree Desai｜guidance：2030 自由現金流轉換率目標 55%–60%（原話："we will be able to achieve a 55% to 60% conversion ratio"）
- 2026-03-31｜Jayshree Desai｜risk：管理層提到製造擴張對自由現金流轉換率的壓力（原話："free cash flow conversion given the manufacturing expansion"）
- 2026-03-31｜Jayshree Desai｜guidance：五年累計自由現金流預期（原話："$10 billion to $12 billion of free cash flow in this time"）
- 2026-03-31｜Jayshree Desai｜capital_allocation：槓桿目標區間（原話："We're targeting a leverage ratio of 1.5 to 2x"）
- 2026-03-31｜Jayshree Desai｜capital_allocation：管理層稱不被槓桿區間綁住（原話："But we don't feel any pressure to force"）
- 2026-03-31｜Jayshree Desai｜capital_allocation：併購時槓桿可拉高的上限（Blattner 為例）（原話："You could see us pushing closer to 3"）
- 2026-03-31｜Jayshree Desai｜capital_allocation：併購與回購以報酬率高低擇優（原話："buy a great company versus buying our shares back"）
- 2026-03-31｜Jayshree Desai｜capital_allocation：過去四年併購金額相對自由現金流（原話："bought $6 billion worth of companies"）
- 2026-03-31｜Jayshree Desai｜commitment：股利承諾：持續成長（原話："We're going to continue to grow our dividend"）
- 2026-03-31｜Earl Austin｜commitment：CEO 稱這些數字對他是個人承諾（原話："I don't view it goes away today. I view it last."）
- 2026-03-31｜Earl Austin｜commitment：CEO 稱不會放上自己不相信的計畫（原話："we would not put a plan up here that we didn't believe in"）
- 2026-03-31｜Earl Austin｜guidance：CEO 稱財測屬審慎（原話："Our guidance is prudent."）
- 2026-03-31｜Jayshree Desai｜guidance：管理層稱規劃以約 80% 效率率計，預留專案遞延（原話："ourselves at an efficiency rate of around 80%"）
- 2026-03-31｜Earl Austin｜guidance：CEO 稱寬幅財測約 80% 會如期落實（原話："you can expect about 80% of it to be right"）
- 2026-03-31｜Jayshree Desai｜margin：管理層要求勿過度解讀分部數字（原話："directional, directional"）
- 2026-03-31｜Jayshree Desai｜margin：利潤率擴張來源之一：企業整體績效改善（原話："performance improvements across the enterprise"）
- 2026-03-31｜Jayshree Desai｜margin：CFO 承認部分營運未達預期（原話："We haven't performed as well as we'd like"）
- 2026-03-31｜Jayshree Desai｜margin：CFO 稱可能為長期可見度讓出部分利潤率（原話："there may be times when we will give up some margin"）
- 2026-03-31｜Earl Austin｜margin：預製化／AI 帶來的利潤率貢獻量級（原話："it gives you some margin expansion, albeit small"）
- 2026-03-31｜Earl Austin｜margin：技術端客戶若要更快或承擔風險，定價可含風險溢價（原話："if there's risk to it, yes, you can expect more margins"）
- 2026-03-31｜Earl Austin｜margin：受管制業務端定價預期（原話："on our regulated side of the business"）
- 2026-03-31｜Jayshree Desai｜risk：固定價格大型合約佔比（原話："less than 15% of our revenues comes from fixed"）
- 2026-03-31｜Earl Austin｜customer：資料中心／大型負載佔積壓訂單比重（原話："while we talk about this, it's only 10%"）
- 2026-03-31｜Jayshree Desai｜customer：技術與大型負載為最快成長市場（原話："That will be our fastest-growing market as we see it today."）
- 2026-03-31｜Jayshree Desai｜customer：電力生成與儲能 CAGR 中點約雙位數（原話："At the midpoint, we're seeing about double-digit growth"）
- 2026-03-31｜Earl Austin｜customer：總可及市場規模（原話："we think it's around $2.4 trillion"）
- 2026-03-31｜Earl Austin｜customer：資料中心可及範圍占比（原話："it's about 50% to 60% of that"）
- 2026-03-31｜Earl Austin｜customer：需求展望延伸至 2030 年後（原話："This business has not stopped at 2030."）
- 2026-03-31｜Earl Austin｜customer：NiSource 機會規模（原話："$5 billion to $7 billion type opportunity"）
- 2026-03-31｜Jayshree Desai｜customer：NiSource 已計入預測（原話："that is baked into our projections"）
- 2026-03-31｜Earl Austin｜customer：客戶詢案頻率（原話："there's not a week that goes by, something doesn't"）
- 2026-03-31｜Earl Austin｜product：變壓器投資金額（CEO 先說錯後更正）（原話："million to $700 million investment"）
- 2026-03-31｜Earl Austin｜product：765kV 變壓器廠擴產（原話："where that factory will double in"）
- 2026-03-31｜Earl Austin｜product：管理層稱不承擔大宗商品風險（原話："We don't take commodity risk."）
- 2026-03-31｜Karl Studer｜product：整合式預製廠面積目標（原話："looking to grow to over 5 million this year"）
- 2026-03-31｜Earl Austin｜product：機械（MEP）平台併購（原話："DSI was kind of a platform acquisition we made last year"）
- 2026-03-31｜Earl Austin｜product：人力與營收成長關係不宜放進財務模型（原話："something that you can put in a financial model"）
- 2026-03-31｜Earl Austin｜product：CEO 估計所需人力成長（原話："you need to grow 7,000 to 10,000 a year"）
- 2026-03-31｜Jayshree Desai｜product：CFO 要求勿把人力成長當建模依據（原話："I don't want you guys to take that as a modeling exercise."）
- 2026-03-31｜Earl Austin｜competition：多數工作為議價而非競標（原話："the negotiations are around 75%"）
- 2026-03-31｜Earl Austin｜competition：電信與大型管線缺乏規模（原話："we don't have scale there in places"）
- 2026-03-31｜Earl Austin｜competition：聯合循環電廠風險態度（原話："take that risk of a combined cycle as it stands today"）
- 2026-03-31｜Earl Austin｜competition：對同業承擔 CCGT 勞力風險的看法（原話："I'm unwilling to take those risks of the past"）
- 2026-03-31｜Earl Austin｜capital_allocation：不買押注單一題材的公司（原話："I'm really concerned with these hockey stick companies"）
- 2026-03-31｜Earl Austin｜capital_allocation：併購模型不內建綜效（原話："we don't build synergies in our models to"）
- 2026-03-31｜Earl Austin｜capital_allocation：併購估值壓力看法（原話："acquire great companies at this kind of framework"）
- 2026-03-31｜Earl Austin｜guidance：全疊加情境營收預期落在區間高端（原話："full stack will be at the high end of the range."）
- 2026-03-31｜Jayshree Desai｜guidance：大型機會時程尚未確定，不在目標內（原話："the timing of those things can be still a little bit"）
- 2026-03-31｜Jayshree Desai｜risk：管理層列舉監管與許可風險（原話："have to get through the regulatory process"）
- 2026-03-31｜Jayshree Desai｜risk：稅務抵減（48E）不確定性，管理層稱是風險（原話："that is out there and that is a risk"）
- 2026-03-31｜Jayshree Desai｜risk：管理層稱目前對電力生成成長無疑慮（原話："we do not see any concerns"）
- 2026-03-31｜Jayshree Desai｜commitment：管理層稱 2026 目標將超標（原話："We now expect to exceed our targets on"）
- 2026-03-31｜Jayshree Desai｜commitment：EPS 加倍承諾（原話："we can double that over the next 5 years"）

### 問答異常語氣（迴避／改口／保留）
- PWR_Q2_2026_Earnings_Call_20260730.md｜問：Steven Fisher (UBS) 問長期利潤率上行空間，管理層過去對利潤率上行訊息偏保守｜答法：CEO 說下半年有 room、指引 prudent，但未給具體利潤率數字或長期目標
- PWR_Q2_2026_Earnings_Call_20260730.md｜問：Chad Dillard (Bernstein) 問預製業務占 RFP 比重、5 年展望、勞動成本節省與價值定價｜答法：CEO 談面積與協作，未回答 RFP 占比、5 年展望，也未直接回答價值定價
- PWR_Q2_2026_Earnings_Call_20260730.md｜問：Chris Tsung (Wolfe) 問收購標的年化 EBITDA 與購買倍數｜答法：CFO 要求分析師自行計算，未給年化數字與倍數
- PWR_Analyst_Investor_Day_Quanta_Services_Inc_20260331.md｜問：Wolfe：電力生成 CAGR 內含多少 NiSource 類專案｜答法：CFO 答 NiSource 已計入；CEO 改談『若不是 NiSource 就會是別家』，未給專案數量
- PWR_Analyst_Investor_Day_Quanta_Services_Inc_20260331.md｜問：ROTH：48E 稅務抵減與 FEOC 指引延遲對再生能源業務的影響｜答法：CFO 稱『沒有疑慮』並承認是風險，未給具體曝險或數字
- PWR_Analyst_Investor_Day_Quanta_Services_Inc_20260331.md｜問：UBS：人力成長與 7–10% 有機成長的橋接｜答法：CEO 給 7,000–10,000 人/年，CFO 隨即說別當建模依據，口徑收回
- PWR_Analyst_Investor_Day_Quanta_Services_Inc_20260331.md｜問：Goldman：活躍市場機會是否含在財測內｜答法：CFO 以多種方式回答（可疊加亦可降低目標風險），未直接答含或不含，並稱時程仍不確定

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
{"date":"20260731","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"美國電網與發電資本支出超級週期在 2026-2031 不中斷，且規劃額能實際轉為核准與開工"},{"id":"H2","text":"craft 工班稀缺使 Quanta 保有工程選擇權與利益率結構——Electric 分部守在 10-12%、Underground 由 9.1% 升向雙位數"},{"id":"H3","text":"市場願意持續給 Quanta 26 倍以上的 FY+2 遠期本益比（現為 32.9x）"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"固定價格／EPC 專案成本超支。Primoris 於 2026 年 6 月因六個再生能源固定價格專案超支，全年淨利指引由 $2.23-2.34 億砍至 $0.71-1.01 億、營運長離職。Quanta 的 10-K 只把合約分成單價／成本加成／固定價格三類，未揭露固定價格佔營收比重（數據限制）。發電 EPC 與資料中心整體工程正是固定價格風險最集中的型態，而 Quanta 正在往這兩塊擴張。"},{"id":"R2","text":"費率端政治反彈使資本支出「規劃」無法轉「核准」。EEI／S&amp;P 的 $1.3-1.4 兆是規劃額；零售電價因資料中心負荷上升而走高已引發州級審查壓力，費率案審批放緩會直接拖慢那 95% 尚未進入在手訂單的大型專案。併網佇列改革（PJM 的 first-ready, first-served 群組研究）同向延後發電專案成熟時點。執行長本人反覆強調「公司高度專注於把成本壓低給費率支付者」——這正是議價權被封頂的機制。"},{"id":"R3","text":"資料中心州級禁令擴散 ＋ 再生能源稅負優惠限縮，同時壓縮技術／大負載與再生能源兩條腿。紐約州已通過全美首例：2026-06-04 州議會通過 Responsible Data Center Development Act、州長簽署行政命令暫停超大規模資料中心一年；2026 年共 11 州提出州級暫停法案，數十個地方政府已自行凍結。喬治亞州 S.B. 476 擬取消幾乎全部州級稅負抵免。技術業務目前佔 PWR 營收 15-20%（執行長 2026-07-30）。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"FY+2 遠期本益比回落至 26x（約 $520）；或管理層正式將 2030 adj EPS 目標重設至 ≥$29 並經一季驗證","irr_base_pct":5.6,"ev5y_pct":19.9,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.36,"ev5y_pct":19.9,"irr_base_pct":5.6,"max_dd_pct":-60.0,"bull_5y_price":1168.0,"bear_5y_price":324.0,"p_bull_pct":25.0,"p_bear_pct":28.0,"rearm_trigger":"FY+2 遠期本益比回落至 26x（約 $520）；或管理層正式將 2030 adj EPS 目標重設至 ≥$29 並經一季驗證","price_at_dd":657.98,"archetype":"循環/商品","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PWR_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
