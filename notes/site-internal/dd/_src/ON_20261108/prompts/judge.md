你是 stock-analyst **v20 判斷 agent**，標的 ON（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ON","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ON_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ON_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1722.3,"period":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","citation":"onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益","value":399.8,"period":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","citation":"onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）"}},{"id":"f_kpi2_non_gaap","label":"Non-GAAP 營業利益率","value":23.2,"period":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","citation":"onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）"}},{"id":"f_kpi3_gaap","label":"GAAP 營業利益","value":378.3,"period":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","citation":"onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）"}},{"id":"f_kpi4_gaap","label":"GAAP 營業利益率","value":22.0,"period":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","citation":"onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）"}},{"id":"f_kpi7_q4_2026","label":"Q4 2026 指引：營收","value":null,"period":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","citation":"onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）"},"needs_sonnet":true},{"id":"f_kpi8_cogs_91","label":"存貨天數（自算：期末存貨÷季 COGS×91）","value":187,"period":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","unit":"天","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","citation":"onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-02","period":"2026-11-02","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-02"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_on_gross_margin_pct","label":"ON 毛利率","value":38.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ON.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_on_operating_margin_pct","label":"ON 營業利益率","value":19.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ON.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_on_fcf_margin_pct","label":"ON FCF 利潤率","value":25.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ON.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_txn_gross_margin_pct","label":"TXN 毛利率","value":60.24,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_txn_operating_margin_pct","label":"TXN 營業利益率","value":41.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_txn_fcf_margin_pct","label":"TXN FCF 利潤率","value":35.24,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nxpi_gross_margin_pct","label":"NXPI 毛利率","value":56.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NXPI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nxpi_operating_margin_pct","label":"NXPI 營業利益率","value":28.55,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NXPI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nxpi_fcf_margin_pct","label":"NXPI FCF 利潤率","value":24.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NXPI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mchp_gross_margin_pct","label":"MCHP 毛利率","value":60.19,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCHP.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mchp_operating_margin_pct","label":"MCHP 營業利益率","value":16.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCHP.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mchp_fcf_margin_pct","label":"MCHP FCF 利潤率","value":21.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCHP.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_stm_gross_margin_pct","label":"STM 毛利率","value":33.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_stm_operating_margin_pct","label":"STM 營業利益率","value":6.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_stm_fcf_margin_pct","label":"STM FCF 利潤率","value":3.22,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_fcf","label":"自由現金流（FCF）","value":488.6,"period":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","citation":"onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）"}},{"id":"f_kpi6_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":9.8,"period":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-10-02，公告於 2026-11-02）","citation":"onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":63.31,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-38.65,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":34.16,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.28 → 3.28）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.71 → 4.71）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.08 → 6.08）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.28,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":4.71,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":6.08,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":2.5,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 3.2 → 3.28（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":37.02,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝12.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":12.3,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.87,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝68.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":68.9,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.92,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝65.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":65.4,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":19.3,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 3.28，分子＝快照價 63.31","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":340.1,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 4707.8、現金 4367.7（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":389.28,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":24985.7,"period":"2026-11-08","unit":"USD m","basis":"市值 24645.6 ＋ 淨負債 340.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6607.47,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（28 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":7593.65,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（28 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.78,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 63.31 / W52 76.51 / W104 63.96 / W250 69.17 / W250 13週斜率 0.15%"},{"id":"f_ma_w52","label":"52 週均線","value":76.51,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":63.96,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":69.17,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.15,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列出 PSG 主要對手為 Infineon、STMicroelectronics、Wolfspeed、ROHM、Nexperia；AMG 對手含 TI、ADI、Infineon、ST、Renesas、MPS、NXP。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"PSG’s primary competitors include: Infineon Technologies AG (\"Infineon\"), STMicroelectronics N.V. (\"STMicroelectronics\"), Wolfspeed Inc., ROHM Semiconductor and Nexperia BV.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：公司承認 AI 資料中心電源可能無法如預期取得份額，失敗將導致市占流失；且無法保證贏得 design win。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"Our failure to commercialize new technologies that can power AI data centers in a timely manner or at all could result in a loss of market share, unanticipated costs and inventory obsolescence, which could adversely affect our financial results.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：部分對手獲政府補貼，若公司拿不到相同補助可能影響市占。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"In addition, some of our competitors may receive governmental subsidies or other incentives that give them a competitive advantage over us.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"TrendForce 報導 onsemi 傳擬在捷克廠裁員最多 300 人，因中國低價 SiC 競爭加劇。","source":"TrendForce News 2026-06-08","url":"https://www.trendforce.com/news/2026/06/08/news-onsemi-reportedly-plans-up-to-300-job-cuts-in-czech-plant-as-low-cost-chinese-sic-competition-intensifies/","excerpt":"[News] Onsemi Reportedly Plans Up to 300 Job Cuts in Czech Plant as Low-cost Chinese SiC Competition Intensifies 2026-06-08 Semiconductors editor","as_of":"2026-06-08","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"onsemi 與 NVIDIA 合作加速 800 VDC 電源架構轉換（AI 資料中心）。","source":"onsemi IR news release","url":"https://investor.onsemi.com/news-releases/news-release-details/onsemi-collaborates-nvidia-accelerate-transition-800-vdc-power","excerpt":null,"as_of":"2025-07-29","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"onsemi 10-K 將「自行開發 IC 的客戶」列為競爭來源之一（一般性風險揭露），未點名特定最大客戶導入第二供應商或自製。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"Because some of our components include functionality that in some cases may be integrated into more complex ICs, we also face competition from manufacturers of ICs, ASICs and fully-customized ICs, as well as customers who develop their own IC products.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 僅一家客戶（經銷商）占營收約11%（2024年約10%），橫跨所有報告部門；公司稱不依賴單一客戶。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"We had one customer, a distributor, whose revenue accounted for approximately 11% and 10% of the total revenue for the years ended 2025 and 2024, respectively, across all reportable segments. Although we are not dependent on any single customer, a significant disruption in key customer relationships could adversely affect our business.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"該經銷商占應收帳款約10%（2025年底），2024年底為13%；2023年無客戶超過10%。經銷商整體占營收54%。","source":"SEC EDGAR 10-K FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"One customer, a distributor, accounted for approximately 10% and 13% of the Company's accounts receivable balance as of December 31, 2025 and 2024, respectively.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Wolfe Research 的 Chris Caso 2026-07 認為本輪上行週期需要新建廠房、耗時長，2028 前很難出現供過於求（泛半導體，非專指 ON）","source":"247wallst: Top Chip Analyst: Semiconductor Oversupply Is Nearly Impossible Before 2028","url":"https://247wallst.com/investing/2026/07/30/top-chip-analyst-semiconductor-oversupply-is-nearly-impossible-before-2028-why-hes-bullish-on-memory/?.tsrc=rss","excerpt":"Top Chip Analyst: Semiconductor Oversupply Is Nearly Impossible Before 2028. Why He’s Bullish on Memory","as_of":"2026-07-30","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"8 吋晶圓代工價格 2026 上半年已漲 5-15%，TrendForce 稱第三輪漲價正討論於 2026 末至 2027 初（成熟製程類比／功率相關）","source":"DEV Community: Silicon wafer capacity is tightening in 2026","url":"https://dev.to/anypcba_official/silicon-wafer-capacity-is-tightening-in-2026-heres-what-hardware-engineers-need-to-know-37nc","excerpt":"foundry prices for 8‑inch have already risen 5‑15% in the first half of 2026. And TrendForce reports that a third round of price hikes is already being discussed for late 2026 and early 2027.","as_of":"2026-06-30","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"IBS Electronics 研究註記：2026 最可能是分段市場而非全面過剩，中國成熟製程新產能可能使部分品類交期正常化","source":"IBS Electronics: China's mature node chip expansion in 2026","url":"https://www.ibselectronics.in/resources/news/china’s-mature-node-chip-expansion-in-2026-market-impact-risk/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"ON 管理層稱需求已穩定、庫存去化多已結束，預期客戶補庫存，並預期 2027 恢復成長；分析師仍預期 SiC 面臨中國競爭與 EV 銷售低於預期","source":"allmind.ai ON Q1 2026 Earnings Call / 搜尋摘要","url":"https://allmind.ai/earnings/event/bt_ON_2026_Q1","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K FY2025 Item 3 未列出反壟斷調查；法律程序僅指向 Note 13，環境類程序採 $1 million 揭露門檻。","source":"SEC EDGAR 10-K FY2025 Item 3. Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"The Company has elected to use a $1 million threshold for disclosing certain proceedings arising under federal, state or local environmental laws when a governmental authority is a party.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Capitol Forum 報導 onsemi 擬收購 Synaptics（約 $7B）可能受中國市場監管機關嚴格審查","source":"The Capitol Forum","url":"https://thecapitolforum.com/?p=6139","excerpt":"Onsemi/Synaptics: Buyout Creating Physical AI Powerhouse Critical to Chinese Industries Likely to Face Intense SAMR Review U.S.","as_of":"2026-07-09","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"中國商務部對美國類比晶片（含 onsemi）發起反傾銷調查","source":"SemiMedia","url":"https://www.semimedia.cc/china-launches-anti-dumping-probe-into-us-analog-chipmakers-including-ti-adi-broadcom-and-onsemi/","excerpt":"Home › MarketWatch › China launches anti-dumping probe into US analog chipmakers including TI, ADI, Broadcom and onsemi 0 China launches anti-dumping probe into US analog chipmakers including TI, ADI, Broadcom and onsemi","as_of":"2025-09-22","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"onsemi 10-K 揭露：樂山（中國，持股80%）組裝測試廠可能因美中緊張面臨成本增加或貿易限制；商務部實體清單擴大可能要求對中國客戶申請額外出口許可，且不保證取得；進口零組件關稅可能衝擊獲利。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"our assembly and test operations facility located in Leshan, China, which is owned by Leshan-Phoenix Semiconductor Company Limited, a joint venture company in which we own 80% of the outstanding equity interests, may be subjected to increased costs or additional trade restrictions stemming from the geopolitical tension between the United States and China.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"onsemi 10-K 稱 FY2025 貿易法規遵循成本不重大，預期現行法規成本不會有重大不利影響，但未來政策變動可能造成重大成本。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"The costs we incurred in complying with applicable trade regulations for the year ended December 31, 2025 were not material, and we do not currently expect the cost of complying with existing trade laws and regulations to have a material adverse effect on our capital expenditures or earnings or on our competitive position in any one year.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-01-14 總統公告依 Section 232 對符合特定技術門檻的先進半導體課 25% 關稅，範圍狹窄；搜尋結果未見針對 onsemi 的專屬說明。","source":"White & Case: President Trump orders narrowly targeted 25% Section 232 tariff on certain advanced semiconductor articles","url":"https://www.whitecase.com/insight-alert/president-trump-orders-narrowly-targeted-25-section-232-tariff-certain-advanced","excerpt":null,"as_of":"2026-01-14","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"ON 10-Q 稱地緣與總經因素帶來挑戰，持續優化並縮減製造足跡（2025 製造重整計畫）","source":"ON Semiconductor Form 10-Q (quarter ending 2025-10-03) via MarketScreener","url":"https://in.marketscreener.com/news/on-semiconductor-quarterly-report-for-quarter-ending-october-3-2025-form-10-q-ce7d5cd9de8fff2c","excerpt":"Despite the current challenges posed by geopolitical and macroeconomic factors, we continue to optimize and right-size our manufacturing footprint","as_of":"2025-11-03","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"CEO 警告所有地區的地緣不確定性持續造成波動（Benzinga 標題）","source":"Benzinga: auto slowdown hits ON Semiconductor in Q4, Q1 outlook also dim","url":"https://benzinga.com/general/market-summary/25/02/43614897/auto-slowdown-hits-on-semiconductor-in-q4-q1-outlook-also-dim-ceo-warns-of-persisting-volatility-due-to-the-geopolitical-uncertainty","excerpt":"CEO warns of persisting volatility due to the geopolitical uncertainty","as_of":"2025-02-10","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026-06 報導 onsemi 捷克 SiC 廠擬裁最多 300 人，起因為中國低價 SiC 競爭；TrendForce 稱中國 SICC、天科合達占 2025 N 型基板銷售約 21.5%、20.1%","source":"TrendForce News 2026-06-08","url":"https://www.trendforce.com/news/2026/06/08/news-onsemi-reportedly-plans-up-to-300-job-cuts-in-czech-plant-as-low-cost-chinese-sic-competition-intensifies/","excerpt":null,"as_of":"2026-06-08","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"China 約占 onsemi 營收 30%，並標示地緣與關稅風險","source":"Finterra via Observer-Reporter","url":"https://stocks.observer-reporter.com/observerreporter/article/finterra-2026-3-6-powering-the-recovery-a-deep-dive-into-onsemi-on-and-the-future-of-silicon-carbide","excerpt":"China Exposure: onsemi derives approximately 30% of its revenue from China. While it has design wins in 60% of Chinese EV models, geopolitical tensions and potential trade tariffs remain a primary risk.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"捷克 Rožnov 廠 2026-06 擬裁 200–300 人，與中國 SiC 低價競爭有關；捷克新廠補貼約 €450M","source":"Evertiq 2026-06-09","url":"https://evertiq.com/design/2026-06-09-onsemi-reportedly-plans-up-to-300-job-cuts-at-czech-facility","excerpt":"at Czech facility Dennis Dahlgren US semiconductor manufacturer Onsemi is reportedly planning to cut between 200 and 300 jobs at its plant in Rožnov pod Radhoštěm in the Czech Republic, according to Czech media outlet e15. The cuts follow an earlier round of approximately 170 layoffs at the same facility in 2025. The restructuring reportedly affects specialists working on silicon carbide","as_of":"2026-06-09","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 營收 $1.72B，季增 7%、年增 11%；車用約 $777M，季減 1%、年減 1%，管理層稱因把受限產能轉向 AI 資料中心與工業，預期 2027 Q1 車用供給與營收恢復正常。","source":"stockstory/marketbeat Q3 2026 call summaries (search summary)","url":"https://stockstory.org/us/stocks/nasdaq/on/news/earnings-call/on-q3-deep-dive-ai-data-center-and-industrial-gains-offset-automotive-supply-shifts","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 工業營收 $467M，季增 10%、年增 9%，來自能源基礎建設與工廠自動化；AI 資料中心 $180M，季增 39%、年增 175%，2026 全年預期約 $620M，2030 目標上調至逾 $30 億。","source":"marketbeat Q3 2026 earnings call highlights (search summary)","url":"https://www.marketbeat.com/instant-alerts/transcript-onsemi-q3-earnings-call-highlights-2026-11-02/","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Q4 2026 指引營收 $1.715B–$1.815B；預期工業低雙位數成長、車用下滑高個位數百分比。","source":"stockstory/marketbeat Q3 2026 call summaries (search summary)","url":"https://stockstory.org/us/stocks/nasdaq/on/news/earnings-call/on-q3-deep-dive-ai-data-center-and-industrial-gains-offset-automotive-supply-shifts","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["triggers","thesis.R"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"SiC 市佔：onsemi 稱 Q1 2026 call 中 2026 北京車展新車型 SiC 份額約 55%、預期 2026 在其市場近 60%（公司自述）；他來源稱 ST 為 SiC 領導者；定價資料未查到可靠來源，僅有中國競爭者壓低非車用價格的未證實說法。","source":"Q1 2026 earnings call coverage / 247wallst (search summary)","url":"https://247wallst.com/technology-3/2026/05/11/onsemi-is-facing-a-continued-slowdown-in-sic-and-greater-competition-in-cis-from-sony/","excerpt":null,"as_of":"2026-05-11","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"WSTS 2026 春季預測：全球半導體市場 2026 約 $1.51 兆（+89.9%），2027 再成長約 27% 至約 $1.9 兆，成長主要由記憶體驅動。","source":"WSTS Spring 2026 forecast / telecomlead","url":"https://telecomlead.com/semiconductor/wsts-raises-semiconductor-forecast-market-to-reach-1-51-trillion-in-2026-grow-to-1-9-trillion-in-2027-126102?noamp=mobile","excerpt":null,"as_of":"2026-06-02","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"0","claim":"onsemi 8-K Q3 2026 新聞稿（官方營收數字）","source":"SEC 8-K ex99-1","url":"https://www.sec.gov/Archives/edgar/data/0001097864/000114036126041580/ef20084671_ex99-1.htm","excerpt":"onsemi (Nasdaq: ON) delivers intelligent power and sensing technologies that enable electrification, energy efficiency, safety, and automation across automotive, industrial, and AI data center end-markets.","as_of":"2026-11-02","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子載明：產品常被技術更先進的替代品取代，競爭對手的產品或技術可能使公司產品過時或失去競爭力。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"Products are often replaced by more technologically advanced substitutes and, as demand for older technology falls, the price at which such products can be sold drops.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 載明：競爭對手開發的產品或技術可能使公司產品或技術過時或不具競爭力；競爭壓力可能限制提價能力。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"Products or technologies developed by competitors may render our products or technologies obsolete or noncompetitive.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"TrendForce 報導 onsemi 因中國低價 SiC 競爭加劇，擬於捷克廠裁員最多約 300 人。","source":"TrendForce News 2026-06-08","url":"https://www.trendforce.com/news/2026/06/08/news-onsemi-reportedly-plans-up-to-300-job-cuts-in-czech-plant-as-low-cost-chinese-sic-competition-intensifies/","excerpt":"[News] Onsemi Reportedly Plans Up to 300 Job Cuts in Czech Plant as Low-cost Chinese SiC Competition Intensifies 2026-06-08 Semiconductors editor","as_of":"2026-06-08","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"SiC vs GaN 2026 分析：所有 800V 牽引逆變器使用 SiC，尚無車廠宣布量產 GaN 牽引逆變器。","source":"PCIM Magazine: SiC vs GaN in 2026 and beyond","url":"https://news.pcim.mesago.com/sic-vs-gan-in-2026-and-beyond-a-947d5edd20f5b5a7f22b8fbecd6f9ec3/","excerpt":"SIC VS GAN SiC vs GaN in 2026 and beyond 2026-07-29 From Luke James 5 min Reading Time Related Vendors MRS Electronic GmbH & Co. KG Diotec Semiconductor AG CISSOID S.A. Silicon carbide went into 1.17 million EV traction inverters in Q1 2026, or 17.2% of everything shipped, according to TrendForce, and Yole Group","as_of":"2026-07-29","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"經銷商銷售占營收比重 2023–2025 為 52%→53%→54%，小幅上升；單一經銷商占 2025 營收約 11%（2024 約 10%）；經銷商透過退貨與庫存輪調條款轉售給 OEM／EMS。未見訂閱化／D2C／平台化轉型的一手紀錄。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"Sales to distributors accounted for approximately 54%, 53% and 52% of our revenue in 2025, 2024 and 2023, respectively. We had one distributor whose revenue accounted for approximately 11% and 10% of the total revenue for the years ended December 31, 2025 and 2024, respectively.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"onsemi 於 2026-11-02 公布 Q3 2026 營收 17.2 億美元（年增約 11%），Q4 2026 營收指引 17.15–18.15 億美元，中點約高於分析師預期 1.6%；非 GAAP EPS 指引 0.95–1.07 美元（來自摘要，需核對原文）","source":"SEC 8-K Ex.99-1 / Stocktwits / capital.com 摘要","url":"https://www.sec.gov/Archives/edgar/data/0001097864/000114036126041580/ef20084671_ex99-1.htm","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 2026-06-21 報導分析師 12 個月目標價平均 94.68 美元；StockAnalysis 頁面顯示 25 位分析師平均目標價約 89.17 美元（as-of 未標示）；24/7 Wall St 2026-08-05 引用共識目標價約 113.12 美元。各聚合站數字差異大，分布不一致","source":"MarketBeat 2026-06-21；StockAnalysis；24/7 Wall St 2026-08-05","url":"https://www.marketbeat.com/instant-alerts/onsemi-nasdaqon-given-consensus-rating-of-moderate-buy-by-analysts-2026-06-21/","excerpt":null,"as_of":"2026-06-21","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-03 公司更新 Q3 2026 指引：EPS 0.81–0.93、營收 17–18 億美元，對照共識 EPS 約 0.83、營收約 17 億美元（指引中點略高於共識）","source":"MarketBeat 2026-08-03","url":"https://www.marketbeat.com/instant-alerts/onsemi-nasdaqon-updates-q3-2026-earnings-guidance-2026-08-03/","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-08-05 摘要稱 BofA 維持買進、目標價由 138 降至 120 美元，同時調升 2026／2027 EPS 預估 3%／7%（二手 AI 摘要，待核）","source":"Yonhap 摘要經搜尋結果引述","url":null,"excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 結果與 Q4 指引（含營收 1,715–1,815 百萬美元）","source":"finviz onsemi Q3 2026 results","url":"https://finviz.com/news/413565/onsemi-reports-third-quarter-2026-results","excerpt":"FOURTH QUARTER 2026 OUTLOOK The following table outlines onsemi’s projected fourth quarter of 2026 GAAP and non-GAAP outlook. Total onsemi GAAP Special Items ** Total onsemi Non-GAAP*** Revenue $1,715 to $1,815 million -","as_of":"2026-11-02","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-01 onsemi 與 Synaptics 簽訂修訂後合併協議（原 2026-06-25 協議全面改寫），因 Synaptics 收到第三方（Party A）主動收購提案。","source":"SEC EDGAR 8-K Item 1.01 (2026-10-01)","url":"https://www.sec.gov/Archives/edgar/data/1097864/000114036126038294/ef20083030_8k.htm","excerpt":"On October 1, 2026, onsemi, Synaptics and Merger Sub entered into an Amended and Restated Agreement and Plan of Merger (the “Amended Merger Agreement”). The Amended Merger Agreement amends and restates in its entirety the Agreement and Plan of Reorganization.","as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.R","valuation","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-11-02 onsemi 子公司簽約以 6 億美元現金併購 Ferric, Inc.。","source":"SEC EDGAR 8-K Item 1.01 (2026-11-02)","url":"https://www.sec.gov/Archives/edgar/data/1097864/000119312526443681/d185557d8k.htm","excerpt":"eligible securityholders of Ferric will be entitled to receive their applicable share of aggregate consideration of $600.0 million in cash, subject to customary purchase price adjustments for Ferric’s cash, indebtedness, transaction costs and working capital.","as_of":"2026-11-02","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"SiC 業務證券集體訴訟（Hubacek v. On Semiconductor）仍在審理中，申訴指控 SiC 業務誤導性陳述。","source":"SEC EDGAR 10-K FY2025 財報附註 Legal Matters","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"On December 13, 2023, a putative class action captioned Hubacek v. On Semiconductor Corp., et al., Case No. 1:23-cv-01429 (D. Del.), was filed by an alleged stockholder of the Company in the U.S. District Court for the District of Delaware against the Company and certain of its officers.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2025-11-13 管理層核准 2–3 億美元非現金減損與加速折舊（製造資產），8-K Item 2.06 於 2025-11-17 申報。","source":"SEC EDGAR 8-K Item 2.06 (2025-11-17)","url":"https://www.sec.gov/Archives/edgar/data/1097864/000114036125042498/ef20059530_8k.htm","excerpt":"on November 13, 2025, management approved the recognition of additional pre-tax non-cash impairment and accelerated depreciation charges of between $200 million and $300 million.","as_of":"2025-11-17","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"TI(類比同業)確認 2026 資本支出大幅降至 US$2–3 billion(2025 約 4.6 billion),來源解讀為資本紀律","source":"XTB, Investing or discipline? Texas Instruments seeks balance","url":"https://www.xtb.com/en/market-analysis/news-and-research/investing-or-discipline-texas-instruments-seeks-balance","excerpt":"The reduction in 2026 CapEx signals that Texas Instruments is prioritizing capital discipline","as_of":"2026-02-24","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"產業層面：2026 半導體資本支出約 2,000 億美元、年增 20%,但 IDM 資本支出再降 9%","source":"Bits&Chips, Semiconductor capex to jump 20 percent in 2026","url":"https://bits-chips.com/article/semiconductor-capex-to-jump-20-percent-in-2026/","excerpt":"integrated device manufacturers continue to pull back, with capex expected to decline another 9 percent in 2026 after a steep drop in 2025.","as_of":"2025-12-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"onsemi 完成捷克 Rožnov 20 億美元垂直整合 SiC 廠擴建，歐盟核准 4.5 億歐元補助","source":"Mammothtimes/TokenRing, High-voltage revolution onsemi SiC","url":"https://business.mammothtimes.com/mammothtimes/article/tokenring-2025-12-29-the-high-voltage-revolution-how-on-semiconductors-sic-dominance-is-powering-the-2026-ev-surge","excerpt":"In late 2025, the EU approved a €450 million grant to support onsemi's $2 billion vertically integrated SiC plant in Roznov, Czech Republic.","as_of":"2025-12-29","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Power SiC 面臨產能過剩下行，稼動率約 50%(上游)/70%(元件製程),中國為最大資本支出占比","source":"DQ India, Power SiC faces overcapacity downturn","url":"https://www.dqindia.com/esdm/power-sic-faces-overcapacity-downturn-while-china-accelerates-domestic-equipment-ambitions-10930636","excerpt":"of falling utilization rates, excess capacity, and reduced investment is raising concerns among industry players. Yet, despite the slowdown, SiC remains central to the electrification roadmap, with device revenue forecast to reach nearly US$10 billion by 2030. The industry’s first major investment cycle, driven by the 2019-2024 CapEx boom, created significant upstream overcapacity.","as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"SiC 晶圓產能將於 2026 陸續釋出(TrendForce),Silan 預計 2026 滿產","source":"LEDinside/TrendForce, Wafer Capacity Set to Surge: New Phase for SiC in 2026","url":"https://www.ledinside.com/node/35905","excerpt":"Silan Microelectronics: Utilization Rising, Full Capacity Expected in 2026 The SiC chip line operated by a subsidiary of Silan Microelectronics has seen steadily increasing output since the second half of 2025.","as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"Microchip 報導庫存去化接近尾聲（類比/MCU 同業週期位置訊號）","source":"MarketBeat: Microchip Technology Says Inventory Slump Is Nearing End as Data Center Wins Build","url":"https://www.marketbeat.com/instant-alerts/microchip-technology-says-inventory-slump-is-nearing-end-as-data-center-wins-build-2026-05-30/","excerpt":"Microchip Technology Says Inventory Slump Is Nearing End as Data Center Wins Build","as_of":"2026-05-30","retrieved_at":"20261108","affects":["thesis.H","triggers"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"onsemi 存貨天數(DIO)：Q4'25 185天(前季193)；Q1'26 200天(高於五年均值33天)；Q2'26 189天(高於五年均值18天)，Q2 改善。未找到通路庫存直接數字","source":"Barchart/StockStory: onsemi (NASDAQ:ON) Surprises With Q2 Sales, Inventory Levels Improve","url":"https://www.barchart.com/story/news/3621434/onsemi-nasdaqon-surprises-with-q2-sales-inventory-levels-improve","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"onsemi Q1 電話會議：經銷通路 mass market 營收年增35%，受惠針對性庫存投資與產品供應擴大","source":"Barchart: onsemi Q1 deep dive","url":"https://www.barchart.com/story/news/1702856/on-q1-deep-dive-ai-data-center-and-automotive-momentum-drive-revenue-beat-amid-inventory-build","excerpt":null,"as_of":"2026-05-04","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"記憶體合約價2026年Q1-Q2大漲（TrendForce 2Q26 行動DRAM合約價續漲）；屬記憶體非類比/功率，價格方向對 ON 僅旁證","source":"TrendForce via iconnect007: Mobile DRAM Contract Prices Continue Rising in 2Q26","url":"https://iconnect007.com/article/150033/mobile-dram-contract-prices-continue-rising-in-2q26-productio/150030/ein","excerpt":"Mobile DRAM Contract Prices Continue Rising in 2Q26, Pressuring Smartphone Production","as_of":"2026-04-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"ON 52週高點108.09(2023年7月)；2025年10月報價的52週區間為31.04–76.06；2025 Q1毛利率年減590bp至約40%，後續季度non-GAAP毛利率37.6%，主因降價與稼動率下滑造成固定成本未吸收（跨來源區間，非單一谷底季）","source":"MarketBeat / Barchart / Tiger 等搜尋摘要","url":"https://www.marketbeat.com/originals/onsemi-stock-signs-point-to-a-powerful-rebound","excerpt":null,"as_of":"2025-10-31","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"SOX 網路泡沫崩盤 2000/03–2002/10 下跌82%，約2.5年；2004–2026 間七次完成的≥20%回落，幅度約−25%至約−69%","source":"quantflowlab: Semiconductor cycle history","url":"https://quantflowlab.com/?p=936","excerpt":"Dot-Com Bust (2000–02) Mar 2000 → Oct 2002 −82% ~2.5 years Never (pre-GFC)","as_of":"2026-10-31","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"產業歷史平均週期約52個月；Regions稱谷底通常在高點後5–6個月，平均高低回落約30%","source":"ECIA Semiconductor Cycle Outlook July 2019 / Regions Asset Management","url":"https://ecia.memberclicks.net/assets/docs/Stats/Trends/ECIA%20Executive%20Analysis%20-%20Semiconductor%20Cycle%20Outlook%20July%202019%20Final.pdf","excerpt":"The average cycle length for previous cycles has been 52 months.","as_of":"2019-07-01","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-10-01 onsemi 與 Synaptics 簽訂修訂後合併協議（原 2026-06-25 協議全面改寫）。","source":"SEC EDGAR 8-K Item 1.01 (2026-10-01)","url":"https://www.sec.gov/Archives/edgar/data/1097864/000114036126038294/ef20083030_8k.htm","excerpt":"On October 1, 2026, onsemi, Synaptics and Merger Sub entered into an Amended and Restated Agreement and Plan of Merger (the “Amended Merger Agreement”). The Amended Merger Agreement amends and restates in its entirety the Agreement and Plan of Reorganization.","as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.R","valuation","triggers"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"2026-11-02 以 6 億美元現金併購 Ferric, Inc.。","source":"SEC EDGAR 8-K Item 1.01 (2026-11-02)","url":"https://www.sec.gov/Archives/edgar/data/1097864/000119312526443681/d185557d8k.htm","excerpt":"eligible securityholders of Ferric will be entitled to receive their applicable share of aggregate consideration of $600.0 million in cash, subject to customary purchase price adjustments for Ferric’s cash, indebtedness, transaction costs and working capital.","as_of":"2026-11-02","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Hubacek v. On Semiconductor 證券集體訴訟（指控 SiC 業務誤導性陳述，§10(b)/20(a)）仍未結案。","source":"SEC EDGAR 10-K FY2025 財報附註 Legal Matters","url":"https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm","excerpt":"The amended complaint again asserts claims for alleged violations of Sections 10(b) and 20(a) of the Securities Exchange Act of 1934. The plaintiff seeks a ruling that this case may proceed as a class action, and seeks damages, attorneys’ fees and costs.","as_of":"2026-02-09","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ON","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.68,"operating_margin_pct":19.12,"fcf_margin_pct":25.38,"rd_intensity_pct":8.85},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ON","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"TXN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.24,"operating_margin_pct":41.12,"fcf_margin_pct":35.24,"rd_intensity_pct":10.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"NXPI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.43,"operating_margin_pct":28.55,"fcf_margin_pct":24.16,"rd_intensity_pct":17.92},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NXPI","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"MCHP","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.19,"operating_margin_pct":16.23,"fcf_margin_pct":21.69,"rd_intensity_pct":22.24},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCHP","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"STM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":33.84,"operating_margin_pct":6.64,"fcf_margin_pct":3.22,"rd_intensity_pct":14.56},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STM","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"ON"},"financial_history":{"ticker":"ON","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":8326200000.0,"revenue_yoy_pct":null,"gross_margin_pct":48.97,"operating_margin_pct":33.2,"net_income":1902200000.0,"diluted_eps":4.24,"free_cash_flow":1597100000.0,"fcf_margin_pct":19.18,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":8253000000.0,"revenue_yoy_pct":-0.88,"gross_margin_pct":47.06,"operating_margin_pct":31.67,"net_income":2183700000.0,"diluted_eps":4.89,"free_cash_flow":438400000.0,"fcf_margin_pct":5.31,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":7082300000.0,"revenue_yoy_pct":-14.19,"gross_margin_pct":45.41,"operating_margin_pct":26.85,"net_income":1572800000.0,"diluted_eps":3.63,"free_cash_flow":1212400000.0,"fcf_margin_pct":17.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":5995400000.0,"revenue_yoy_pct":-15.35,"gross_margin_pct":33.09,"operating_margin_pct":12.53,"net_income":121000000.0,"diluted_eps":0.29,"free_cash_flow":1418600000.0,"fcf_margin_pct":23.66,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ON/ON_Q3_2026_Earnings_Call_20261102.md）

# Q3 2026 Earnings Call
**ON Semiconductor Corporation** | Earnings Calls | 2026-11-02

**Operator** (Operator):
Good day, and thank you for standing by. Welcome to the onsemi Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please be advised that today's conference is being recorded. I would now like to hand the conference over to your speaker today, Parag Agarwal, Vice President of Corporate Development and Investor Relations. Please go ahead.

**Parag Agarwal** (Executives):
Thank you, Daniel. Good afternoon, and thank you for joining onsemi's third quarter results conference call. I'm joined today by Hassane El-Khoury, our President and CEO; and Thad Trent, our CFO. This call is being webcast on the Investor Relations section of our website at www.onsemi.com. A replay of this webcast, along with our third quarter earnings release, will be available on our website approximately 1 hour following this conference call, and the recorded webcast will be available for approximately 30 days following this conference call.
Additional information is posted on the Investor Relations section of our website. Our earnings release and this presentation include certain non-GAAP financial measures. Reconciliation of these non-GAAP financial measures to the most directly comparable GAAP financial measures and a discussion of certain limitations when using non-GAAP financial measures are included in our earnings release, which is posted separately on our website in the Investor Relations section.
During the course of this conference call, we will make projections or other forward-looking statements regarding the future events or the future financial performance of the company. We wish to caution that such statements are subject to risks and uncertainties that could cause actual events or results to differ materially from projections.
Important factors that can affect our business, including factors that could cause actual results to differ materially from our forward-looking statements, are described in our most recent Form 10-K, Form 10-Qs and other filings with the Securities and Exchange Commission and in our earnings release for the third quarter.
Our estimates or other forward-looking statements might change, and the company assumes no obligation to update forward-looking statements to reflect actual results, changed assumptions or other events that may occur except as required by law. Now let me turn it over to Hassane. Hassane?

**Hassane El-Khoury** (Executives):
Thank you, Parag, and thank you all for joining us this afternoon. Our third quarter results reflect continued strength in our business and the momentum we are building across our strategic growth markets with growth above seasonal trends, continued acceleration in AI data center and improving demand in industrial. We see particularly strong demand where power density is becoming the key differentiator, from AI data centers and the grid infrastructure supporting them to energy storage and next-generation vehicle architectures.
These are strategic markets where we focused our investments and are now seeing that strategy translate into revenue growth, margin expansion, share gains and new customer wins. AI data center continues to be our fastest-growing market, scaling more rapidly than we anticipated entering the year with new wins that started to ramp. In automotive, we continue to gain content and secure new platform wins in every region, while industrial demand continues to improve, led by power infrastructure and energy applications.
In Q3, we delivered $1.72 billion of revenue, non-GAAP gross margin of approximately 41.2% and non-GAAP diluted earnings per share of $0.90, all above the midpoint of our guidance. The combination of stronger demand, improved mix and disciplined execution is driving meaningful operating leverage in our model with earnings growth significantly outpacing revenue growth.
We remain supply-limited in certain technology segments of our business, and we made the short-term decision in the third quarter and into the fourth quarter to allocate to markets where we see strong end demand like AI data center, industrial, which came in much stronger than we originally planned. In automotive, we are supporting all deliveries for end demand, but we are not supporting inventory replenishment backlog. As we balance supply and demand, we expect 2027 automotive growth to be in line with our long-term target.
In AI data center, our revenue covers the complete power tree from power supply units or PSUs to low-voltage smart power stages near the processor, where increasing compute is driving greater power density requirements and higher semiconductor content. In the third quarter, our AI data center revenue grew 39% sequentially to $180 million, and we now expect to deliver approximately $620 million of revenue in 2026, an increase of 140% year-over-year.
For 2027, we still expect our AI data center revenue to double over 2026 as we continue to ship with new product ramps. In the third quarter, we began volume shipments into multiple marquee platforms, including Google with both silicon carbide and silicon MOSFETs for PSUs and 54-volt to 12-volt applications. The transition to 800-volt architectures creates the next content opportunity for onsemi, moving AI data center power directly into our strength.
Our comprehensive low-to high-voltage power portfolio spanning silicon, silicon carbide and vertical GaN remains a competitive advantage, allowing us to address direct conversion from 800 volts to the 54-volt, 12-volt and 6-volt rails required across the AI rack. As power systems become more complex, customers increasingly need solutions that go beyond individual components.
At last month's OCP Summit, we showcased our 800-volt to 6-volt solution using our differentiated vertical GaN technology alongside our gate driver and MOSFETs to deliver industry-leading efficiency and world-leading power density for one of the most challenging conversions in the AI rack. The move to 800-volt high-voltage DC also accelerates the transition from mechanical to solid-state power disconnects for fast turn-off from solid-state transformers and circuit breakers to hot-swap applications.
Our silicon carbide JFET portfolio delivers superior thermal performance and is already designed in and contributing to our data center revenue. At Investor Day, we talked about the investments we are making to build differentiated capabilities ahead of the inflection points in our markets, and we continue to do that as power density becomes increasingly critical across AI data center, automotive and industrial. One example is EPP, our embedded power platform introduced at Investor Day.
EPP uses the silicon wafer itself as the package to solve electrical, thermal and mechanical constraints simultaneously. We are pleased with the customer interest in the platform since the announcement, reinforcing our conviction that power density is becoming an increasingly important differentiator across automotive, AI data center and industrial applications. EPP is already sampling to alpha customers across these markets and is manufactured using our 12-inch silicon process at East Fishkill.
Today, we are also excited to announce the acquisition of Ferric, which further extends our capabilities into integrated voltage regulators or IVR and puts us in the leadership position for power delivery to the next-generation AI processors. As power requirements of AI processors continue to increase, IVR incorporates the complete power regulator, including controller, power switches, capacitors and magnetics in one thin package and places it closer to the GPU, reducing power losses and solving the power density problem at the core.
Ferric offers the most compelling IVR solution in the industry with its industry-leading efficiency and transient response performance in an exceptionally compact footprint with best-in-class z-height. We expect Ferric to increase our market share in the Vcore stage of the AI data center power tree. While this is a multiyear opportunity for onsemi well beyond 2030, we are raising our 2030 AI data center revenue target by $500 million to greater than $3 billion.
Moving on to our industrial business. The AI halo effect is driving momentum beyond the data center itself. We expanded hybrid EliteSiC and IGBT module wins with multiple lead customers, including Sungrow and Sineng, driven by the 99.3% efficiency platform we introduced last quarter. Also in our industrial business, we see increasing momentum in robotics and physical AI, an area where our capabilities in power and sensing are highly complementary to Synaptics.
Demand from first-person view or FPV drones is driving increased shipments of our 2-megapixel and 8-megapixel Hyperlux image sensors, and we are engaged with more than 10 leading drone manufacturers. We continue to diversify across the robotics market and have secured multiple new design wins with leading U.S. humanoid makers across power, connectivity and sensing.
For sensing, we are advancing our indirect time-of-flight or iToF technology to deliver world-class depth resolution of 1 millimeter up to 10x better than competing solutions, enabling the precise depth perception critical for robots to interact with the physical world. As physical AI scales, these applications bring together many of our core capabilities across power and sensing, creating a significant new content opportunity for onsemi.
Turning to automotive. We continue to win new customer designs across all regions. As the industry moves toward electrification, higher level of autonomy and software-defined vehicles, the investments we have made in new products continue to expand our content per vehicle up to $2,000 as architectures evolve. These transitions create multiple vectors of content growth for onsemi even in a relatively flat SAAR.
We continue to gain share in the North American EV market across traction inverter designs and new onboard charger platform wins in addition to the Treo-based 10BASE-T1S ramp we already started. Across European OEMs, we expanded our design wins across our power portfolio as they also started the transition to 48-volt zonal.
In China, we continue to expand our leading position in high-end OEMs for their 900-volt electric vehicles with new 1,200-volt silicon carbide traction inverter wins at NIO for their flagship sedan and Geely Zeekr's rapidly expanding export model. As we look ahead, we are increasingly confident in the trajectory of the business. AI data center continues to scale rapidly, while improving demand in automotive and industrial, content gains and new platform wins create multiple vectors of growth.
All these trends are converging around the areas where onsemi is differentiated in intelligent power and sensing and our disciplined execution positions us to translate that growth into stronger earnings and cash generation. I want to thank our employees around the world for their continued focus and execution. Their work is what enables us to deliver for our customers and create shareholder value. Now let me turn it over to Thad to provide more details on our results and guidance for the fourth quarter.

**Thad Trent** (Executives):
Thanks, Hassane. We believe the recovery is gaining momentum, and we are in a fundamentally stronger position than in prior quarters. We have more content, a broader market opportunity and substantially greater earnings power. With much of the heavy lifting and investments behind us, we are positioned to convert revenue growth into earnings and free cash flow growth. In the third quarter, we continue to see this benefit in our financial results.
Q3 revenue was $1.72 billion, above the midpoint of our guidance and up 7% sequentially. Non-GAAP gross margin expanded by 190 basis points quarter-over-quarter to 41.2% and non-GAAP earnings per share was $0.90, growing 4x faster than revenue growth year-over-year. During our Investor Day, we discussed having consistently invested ahead of major market inflection points, building capabilities organically and supplementing them through strategic M&A to accelerate time to market. AI data center is a clear example.
As architectures evolve, we are continuing to strengthen our capabilities across the power tree to position onsemi to capture more of that opportunity. Today, we announced the acquisition of Ferric for $600 million, plus up to $175 million in earn-outs tied to the achievement of revenue milestones. As Hassane mentioned, Ferric puts us in a leadership position in power delivery for next-generation AI processors. We expect Ferric to be accretive to our growth and gross margin targets with EPS accretion at scale and no meaningful near-term financial impact.
This is a multi-year opportunity, raising our AI data center revenue target by 20% to more than $3 billion in 2030 and continues to accelerate thereafter. We expect the transaction to close in the fourth quarter, subject to customary closing conditions. Additional details on the acquisition are available on our Investor Relations website. Turning to revenue for the third quarter. Q3 revenue was $1.72 billion, up 7% sequentially and 11% year-over-year.
Revenue was $22 million above the midpoint of our guidance with growth in industrial and AI data center. Automotive revenue was $777 million, down 1% sequentially and year-over-year. The sequential decrease is primarily due to the reallocation of supply to the AI data center and industrial end markets. We expect automotive revenue to decrease high single-digit percentage points in the fourth quarter, reflecting continued supply reallocation as well as timing and phasing of customer deliveries.
Q1 is expected to return to normalized levels as supply comes online. Industrial revenue was $467 million, up 10% sequentially and 9% year-over-year. We saw strength in energy infrastructure, factory automation and the broader industrial market. We expect industrial revenue to increase low double-digit percentage points in the fourth quarter. AI data center revenue was $180 million, up 39% sequentially and 175% year-over-year.
Demand continues to accelerate, and we now expect our AI data center revenue to reach approximately $620 million in 2026, increasing mid-teens percentage points in the fourth quarter. In 2027, we expect this to double off a higher base. Please note, beginning this quarter, we are enhancing our disclosures by separately reporting AI data center revenue as a fourth market segment to provide greater transparency into this important growth driver for onsemi.
You will see this in our supplemental materials on our Investor Relations website and in our 10-Q. Revenue for the other end market segment, now excluding AI Data Center, was $299 million, up 11% sequentially and 10% year-over-year due to normal seasonality in the Wireless segment. We expect our other revenue segment to increase high teens percentage points in the fourth quarter.
Looking at the split between business units, revenue for the Power Solutions Group, or PSG, was $890 million, an increase of 7% quarter-over-quarter and 21% year-over-year. Revenue for the Analog and Mixed Signal Group, or AMG, was $597 million, an increase of 9% quarter-over-quarter and 2% year-over-year. Revenue for the Intelligent Sensing Group, or ISG, was $235 million, an increase of 3% quarter-over-quarter and 2% year-over-year.
Moving to gross margin. GAAP gross margin was 41.4%, and non-GAAP gross margin expanded for the fifth consecutive quarter to 41.2% due to utilization improvements earlier in the year and favorable mix to new products. Utilization remained flat at 83%. We expect similar levels in Q4 with utilization increasing as we move into 2027 in response to improving demand signals. Our Fab Right strategy remains an important contributor to the long-term margin opportunity.
In Q3, we closed the previously announced divestiture of a back-end facility in the Philippines, and we remain on track to close our divestiture of the Mountain Top fab exiting 2027. We are operating with a more focused and efficient footprint, creating additional opportunity for gross margin expansion over time. GAAP operating expenses were $335 million. Non-GAAP operating expenses were approximately $310 million. GAAP operating income was $378 million or 22% of revenue.
Non-GAAP operating income was $400 million or 23% of revenue. GAAP net income was $314 million and non-GAAP income was approximately $354 million. Our GAAP tax rate was 21%, and our non-GAAP tax rate was 15%. GAAP share count was approximately 397 million shares, resulting in GAAP earnings per share of $0.79. Non-GAAP share count was approximately 392 million shares, resulting in non-GAAP earnings per share of $0.90.
Turning to the balance sheet. Cash and short-term investments were approximately $4.4 billion at quarter end. Total liquidity was $5.9 billion, including $1.5 billion undrawn on our revolver. Cash from operations was $516 million and free cash flow was $489 million or 28% of revenue. Capital expenditures were $28 million or 1.6% of revenue, and we expect full-year capital expenditure to be approximately 2% of revenue. Inventory increased $22 million sequentially but declined on a days basis by 6 days to 186 days.
Strategic inventory continues to drain, declining 7 days in Q3 and base inventory increased by 1 day as we continue to support higher demand. Distribution weeks of inventory declined to 9.9 weeks from 10.1 weeks in Q2 with sell-through continuing to support a healthy channel and mass market growth. We repurchased $20 million of shares in Q3 with activity limited by trading restrictions related to the Synaptics acquisition and renegotiations.
Looking forward, let me provide the key elements of our non-GAAP guidance for the fourth quarter. As a reminder, today's press release contains a table detailing our GAAP and non-GAAP guidance. We anticipate Q4 revenue will be in the range of $1.715 billion to $1.815 billion, representing above seasonal growth of 2.5% sequentially at the midpoint. We expect non-GAAP gross margin to be between 41.5% and 43.5% and include approximately $8 million in stock-based compensation.
At the midpoint, this represents 130 basis points of sequential expansion. Non-GAAP operating expenses are expected to be between $303 million and $318 million. This includes approximately $34 million in stock-based compensation. We anticipate non-GAAP other income to be approximately $27 million, favorable. We expect our non-GAAP tax rate to remain at 15% and our non-GAAP diluted share count to be approximately 392 million shares.
This results in non-GAAP earnings per share in the range of $0.95 to $1.07, and we expect capital expenditures in the range of $40 million to $50 million. The fourth quarter outlook reflects continued demand momentum and another step forward in our model. Based on our current visibility, we expect this momentum to continue into 2027 with continued revenue growth and gross margin expansion as we scale our differentiated products and realize the benefits of our more efficient operating model.
As we look ahead, the opportunity is about more than a recovery in demand. We have built a stronger business with significantly greater earnings and cash flow potential. Our portfolio is more focused; our manufacturing footprint is more efficient and our path to growth is capital efficient.
As we exit the year, our priorities are clear: execute on the demand in front of us, scale our differentiated platforms and capture the large market opportunities ahead. We believe we are well positioned to deliver sustained growth and expand margins, creating long-term value for our shareholders. With that, I'll turn the call back over to Daniel to open up the call for questions.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Vivek Arya with Bank of America Securities.

**Vivek Arya** (Analysts):
Hassane, you have been sort of, I guess, rightly deemphasizing automotive in Q2 and Q3, and I think even in Q4 with this signaling of, I think, high single digit from what I heard. But then you suggested that next year, auto would go back to growing per your long-term target, which I think is up whatever, 9% or 10%. So I'm curious, does underserving that market have any market share implications longer term? And then where does the extra supply come from to start regrowing in that market from next year?

**Hassane El-Khoury** (Executives):
Yes. So just one thing I want to correct the words you used. We're not deemphasizing the automotive market. Automotive remains strategic as an end market. And even in our 5-year outlook that we highlighted in Investor Day, automotive still is the largest market, and that's not going to change. What you're seeing today or this quarter and next quarter, what we've hinted at is short term in nature and it's supply-driven, not strategically driven.
What I mean by that is we're not losing share because we're working closely with the OEMs, as I mentioned in my prepared remarks, we are supporting all of their end demand needs. What we are holding back, again, with conversations with them and alignment with them is their replenishment that they would have liked to see this -- during the quarters. We will resume shipment in Q1 as the supply comes online. The supply -- we've always had the supply coming online or increasing supplies in the technologies we've been constrained on.
But you saw the results from industrial and AI data center even beat our guidance and our expectations. So in the short term, we decided to shift the mix a little bit, but that is not a strategic decision. Our strategy remains the same as we've highlighted at Investor Day. That's why we're reiterating 2027 resuming the growth, which tells you there's no share loss. It is purely a replenishment, not an end demand, and it's short term in nature.

**Vivek Arya** (Analysts):
Got it. And for my follow-up, maybe, Thad, if you could walk us through the puts and takes of gross margins Q3 to Q4 volume, mix, utilization. And then let's say, conceptually next year, if your auto industrial businesses grow according to the long-term growth rates you set out and data center can potentially double, how should we think about the potential for gross margin expansion for 2027?

**Thad Trent** (Executives):
Yes, Vivek, our gross margin bridge doesn't change, right? It's -- the biggest driver in the gross margin expansion here in Q4 is utilization improvement. Now keep in mind, this is utilization improvement from 2 quarters ago, right? So you'll start to see that. You also start to see a little bit of the pricing impact that we've had where we've already had the headwind on the input costs hitting us, and so we'll start to see some of that pricing impact coming in as well.
But the math of every point of utilization being 25 basis points to 30 basis points of gross margin improvement still holds. And that will be true as we go into 2027 as well. So as I mentioned in my prepared remarks, we expect further growth. We expect further utilization improvement as we go into '27, which then will continue to give us margin expansion throughout the year. Obviously, as we have revenue growth, that will help as well. And then the other piece that really starts to drive is the new products.
So we get favorable mix, and we're already seeing that here in Q3 as the new products start to ramp at favorable margins. So we'll start to see that as a nice tailwind going in there, too. And then there's a little bit of the Fab Right with one of the divestitures that we've announced on the back-end facility. We'll see a little bit of that in '27. We'll see more of it in '28 from the Mountain Top facility, but that's a nice tailwind as we go forward as well.

**Operator** (Operator):
Our next question comes from Blayne Curtis with Jefferies.

**Blayne Curtis** (Analysts):
I just wanted to follow up on the last one. So I'm assuming auto would have been up in December and it's down high single digits. So I'm just trying to understand the level of restocking that might have already happened in the December quarter. And I'm just kind of curious whether you see those trends increasing.

**Hassane El-Khoury** (Executives):
Yes. I mean the trend is increasing. So there will be like -- think about it as there will be a catch-up because it's restocking, it's not really the end demand. The end demand, we are supporting. So there's no change to that. So you can assume some seasonality on top of it. But from a replenishment, the demand is not perishable. So we will -- you'll see that resuming in the first quarter as supply comes online. So it's purely a -- you can think about it as a quarterly timing.
We're not guiding Q1. But once we get to Q1, you can see that some of it would have been in Q4 if you normalize it. I've always said in automotive or even in multiple markets that we service, I don't look at the quarter-on-quarter, and I don't read anything into it. I look at it from a trend perspective and the decisions we are making. So I'm not -- I have 0 concerns about the decisions we're making in automotive.
They are the right decision for us to make as a company for -- to service the increased demand that we've delivered in industrial and AI data center in Q3 and looking out in Q4. And then we will resume to normalized supply and demand starting here in '27. And for the rest of '27, you'll see us deliver the long-term target again.

**Blayne Curtis** (Analysts):
And then data center business doubling again in '27 is pretty impressive. Just wondering if you had any broad strokes you could walk through in terms of the drivers of that.

**Hassane El-Khoury** (Executives):
Yes. I mean, look, it's a lot of the broad strokes as far as across the power tree, which I've been saying for a few quarters that we've been doing design wins across the power tree from the high voltage all the way to the core. Those have started to come online and generate revenue. So we've already transitioned from design-in to design wins and now revenue. And then the breadth of customers, we've highlighted some customers in the past. Some customers, you can kind of draw a line to who they are.
And it's across the power tree, meaning directly with the compute vendors when we're sitting on the board, but also with the supply chain when it comes from PSUs and so on, and we've highlighted those throughout the last few calls. All of these are starting to get maturity. We're ramping up -- we ramped up a few more in the third quarter here. We hinted at it at Investor Day as well.
So that came in. So it's really execution, execution, execution, but more importantly, new products that we have been introducing over the last couple of years are starting now to deliver. And that ramp is what's going to continue in 2027 on top of the new stuff that we're going to ramp into revenue in '27 that we're doing design wins on now. And just to highlight, the doubling in '27, again, is off of the higher base that we just talked about today. So it's -- '27 is higher than what we expected even 90 days ago.

**Operator** (Operator):
Our next question comes from Joe Quatrochi with Wells Fargo.

**Joseph Quatrochi** (Analysts):
Maybe just to follow up on that. The $500 million that you're increasing for your 2030 revenue target, is that all from the acquisition? Or is that also from just the base increasing from 90 days ago?

**Hassane El-Khoury** (Executives):
This is tied to the acquisition.

**Joseph Quatrochi** (Analysts):
Okay. And then as a follow-up, as we think about just the cash outlay that's kind of in front of you in terms of this acquisition and then also Synaptics and you're raising some debt for that as well. But how do we think about just the use of free cash flow and capital returns in that vein?

**Thad Trent** (Executives):
Yes, Joe. So we'll be using cash off the balance sheet from the Ferric acquisition. As we close the Synaptics acquisition, we will be focused on delevering. That will be our top priority. That's obviously after investing in the business as well. But we'll focus there, and we'll be opportunistic on buying back shares over time. But the intent here is to delever quickly.

**Operator** (Operator):
Our next question comes from Tom O'Malley with Barclays.

**Thomas O'Malley** (Analysts):
My first is on industrial. It looks like it's well above seasonal in September. And then when you go into December, it looks like some very strong results again. Any sort of vertical that you would call out in industrial that's doing a bit better? Those are some impressive numbers in the back half. Just want to start there.

**Hassane El-Khoury** (Executives):
Yes. I think I would call out the AI halo that we talk about, anything from energy. Think about it from the grid to the AI data center. So everything outside the walls of the AI data center has been very strong. It came in better than we expected. A little bit on the PMIs are improving, so the broad industrial. But if you ask me what is the beat and the outlook tied to is really the AI halo that we highlighted at our Investor Day is coming in as we expected and in the short term higher, which is the reason I mentioned servicing that ahead of some other markets.

**Thad Trent** (Executives):
Yes. And the broader industrial is about 40% of the total industrial bucket, and we're seeing strength there as well. I think just as you're seeing PMIs improve.

**Thomas O'Malley** (Analysts):
Got you. And then Thad, second one for you is just you talked about the automotive revenue just being a bit lighter because of supply reallocation, timing, phasing of customer deliveries. But it looks like the utilization is flat. So are you short external components? Because I would expect if you're not able to get more supply, like the utilization would continue to move up. You're saying kind of that's more next year. Maybe just describe the dynamic, like where are you seeing the constraints?

**Thad Trent** (Executives):
Yes. Keep in mind that what you're seeing come out of the line today was utilization from 2 quarters ago when we were running at 77%. We ran at 83% last quarter. We're running at 83% going into Q4. So this is us catching up to that supply as you get cycle time through the fab in the back end.
So that's where we have supply coming online. The supply constraints are in specific lines in certain areas. So it's not across the board or obviously, we'd be taking utilization up further. But as we look into next year and we see demand continuing to strengthen across all the end markets, we will be taking utilization up.

**Operator** (Operator):
Our next question comes from Gary Mobley with StoneX.

**Gaurav Saini** (Analysts):
Gaurav Saini here on behalf of Gary Mobley at StoneX. So I just wanted to ask specifically about the utilization lever in the gross margin bridge. About half of the path to that 53% gross margin target you guys set out comes from utilization. So just given the restructuring and also the changes to depreciation, how should we sort of think about the incremental gross margin on each dollar of revenue from here on out?

**Thad Trent** (Executives):
Well, look, the way you should think about the Q3 results is there's about 450 basis points of underutilization charges. Now again, you got to go back to the Q1 utilization of 77% for that. So if you take that, getting up to what is kind of peaking out for us, 92%, 93% somewhere in there, you can do that math on that 25 basis points to 30 basis points and you get to that 450 basis points. So to do the walk for everybody, getting from here to the 53%, you've got about 450 basis points of utilization improvement.
You've got 225 basis points of Fab Right. I talked about the activities we're taking there. You've got another 400 basis points of mix and the new products kicking in, and I've already kind of talked about we're starting to see that hit the P&L, and we'll start to see a lot more of it next year. And then the last component is we've been raising pricing, but we haven't seen that necessarily fully hit the P&L. So there's a little bit of tailwind from there. So if you start to add all that up, you're getting right around that 53% long-term target.

**Gaurav Saini** (Analysts):
Got it. Okay. And you guys also talked a bit about just now the new product ramp in '27. I kind of wanted to double-click on that and the contribution we'll see in the fiscal year for next year. How should we sort of think about the revenue from vertical GaN, EPP and Treo as these new sort of layers of revenue that really didn't preexist before?

**Hassane El-Khoury** (Executives):
Yes. So what you're going to start seeing is obviously, Treo will continue to ramp. Treo is already contributing to revenue this year. We already talked about vertical GaN contributing revenue in '27. And then you layer on top of that towards the end, EPP. But those are -- other than Treo that started to ramp last year. And obviously, we've been more than 2x'ing as you kind of move forward from a smaller base.
The other ones will start to ramp and will follow such a trajectory. So you can think about the base for 2027 as new products that we've had in '25 and '26 that will start contributing meaningfully, while the new products, we've introduced like EPP and vertical GaN to start in '27 and continue forward, all leading up to a more mature mix of new products towards that 2030 time line depending on auto or industrial.

**Operator** (Operator):
Our next question comes from Chris Caso with Wolfe Research.

**Christopher Caso** (Analysts):
The first question is with regard to the Ferric acquisition. Can you talk to us a little bit about where that acquisition stands with regard to revenue and design wins and realizing you used that to take up your 2030 target? But as we look into sort of '27, '28, what can we expect from that business?

**Hassane El-Khoury** (Executives):
No. Look, I'm not going to give a guide to revenue as far as the acquisition or '27 at this point. But I will tell you, during the diligence that we've had, obviously, we all know from a market, ourselves and all of you know the trajectory that IVR has taken that it is the solution for higher and higher power of AI processing. That's point number one. We know integration, power density and the criticality of the z-height is important.
And Ferric has been engaged with all of the hyperscalers from a design and platform architecture perspective. That's from the technology and the capabilities that they bring. We bring the scale, manufacturability and, of course, the breadth of our reach within the hyperscalers, but also the compute platforms.
That's the combination that makes this strategic. But from an engagement perspective, they are engaged and in a very good position with all of the hyperscalers based on our touch point, on the diligence that we've done with the team. And of course, it brings in a high-caliber, talented team that complements our own internal efforts, and that's the win-win.

**Christopher Caso** (Analysts):
Got it. As a follow-up, I've got a question on CapEx and capacity as you go into next year. And correct me if I'm wrong on this one, but it sounds like some of the supply constraints you're facing now is just a function of not having started the wafers earlier in the year. And so now you're catching up.
So I guess if that's the case, where do you stand with regard to capacity as you go into next year? Do you think you have the capacity to be able to meet what you see for the market next year? And then from that, what sort of CapEx should we be expecting as you head into next year?

**Thad Trent** (Executives):
Yes, Chris, I think that's a fair characteristic that this is a catch-up, right? And that's why Hassane talked about this as being temporary. We'll catch up in Q1. So we do have the capacity that we need based on the outlook that we have today and even some upside to that outlook. So I don't think we're going to be anywhere near capping out our capacity as we go into 2027. This year, our CapEx intensity is about 2% of revenue.
I expect it to be about 5%, in line with our long-term model next year. That will give us the ability to bring in not only maintenance capital, but a little bit of capacity where we need it on certain lines where we can get higher throughput. But we believe we're in a really good spot for a market that's going to grow in 2027 and even beyond that in terms of just the capacity we have online.

**Hassane El-Khoury** (Executives):
Yes. And the capacity that we talk about that will contribute to catching up in Q1, you can think about this as the capacity was -- is already behind us and the investment is behind us. It will just come online and deliver in -- think about it in 2027. So it's not something that we're looking forward. It's something that we've done, and we're just going to get the benefit just from the latency perspective.

**Operator** (Operator):
Our next question comes from Jim Schneider with Goldman Sachs.

**James Schneider** (Analysts):
Hassane, I was wondering if you could maybe characterize the OEM customers' behavior in terms of their willingness or interest in restocking. I think you referred in your prepared comments to automotive customers are not supporting restocking but only supporting increases in end demand. Can you maybe sort of broadly describe what's happening with those customers and then the broader OEM customer set with respect to taking on more inventory in the balance sheet?

**Hassane El-Khoury** (Executives):
Yes. So I'll -- first, I'll characterize it as specific to OEMs. It's not all OEMs are behaving the same way. So I can only reference the ones that we've been engaging with that have demand. And they're looking at it as they see the writing on the wall. AI and industrial is recovering, and they're trying to place demand, so they're not caught in traffic as far as capacity and capacity constraint because they see it across the board, not just on power semis that we see, but across analog, compute and of course, the memory.
So they're looking at their 2027 plans, and they want to think about it as have a what I would call a business continuity plan or BCP as known in the industry. Those are strategic plans that we do with our strategic OEMs where we sit down and figure out kind of their capacity and their pull rate, and we build ahead of that. Normal standard procedure as far as replenishment ahead of the ramp.
That's why we're having these conversations as far as we're not going to build it all in Q3 and Q4, which we made that decision. We will continue to ship demand, knowing that the backlog is now on the books and we'll service that, and that's what we've built the new capacity model towards. That's why it's a temporary in nature, it's short term, and we'll catch up in the '27.

**James Schneider** (Analysts):
And then maybe just as a follow-up, your remaining other subcategory seems to be actually growing very, very well even when you take away the data center, re-bucket it into its own category. Can you maybe talk about some of the -- what's driving the other category that remains? And what -- can you kind of extend that growth rate into 2027 or why or why not?

**Thad Trent** (Executives):
Yes. The other bucket for us, we play opportunistically, right? In the prepared remarks, we talked about Q3 as being seasonal with the wireless end market that's in that bucket as well. When we look into Q4, we have a large customer ramping program. So it's a little lumpy. I think that's why Q4 is up to mid- to high teens. As we go into next year, no, I wouldn't expect it to grow at that.
I think you're going to see the AI data center and the automotive and industrial grow at a much faster rate and that to be a little bit more in line with normal historical rates there as we focus on the other markets. And by the way, the Q4 ramp that I'm talking about is manufactured externally. So you're not seeing an impact of that. That's why we're able to support that.

**Operator** (Operator):
[Operator Instructions] Our next question comes from Tristan Gerra with Baird.

**Tyler Bomba** (Analysts):
This is Tyler Bomba on for Tristan. Is there any inventory replenishment embedded in the strength in industrial? You talked about not allowing replenishment in auto, but curious what you're seeing in industrial.

**Hassane El-Khoury** (Executives):
No. So the strength in industrial is really coming from the AI halo, as I mentioned in a prior answer. And the AI halo, we see end product going out in the market. So we can see the sell-through, not just the sell-through from us to customer, but the sell-through from customers to their end customers. If you look at the large industrial names that do kind of grid to data center, they have all had really good quarters for the ones that announced so far.
And we see that as well as far as what they're building. So that's why we're allocating when I say it's going to truly end demand, which is stuff getting deployed on sites. So that's not an inventory replenishment. It is purely an increase in demand that is getting installed as fast as possible in end sites.

**Tyler Bomba** (Analysts):
Great. For my follow-up, how should we think about the geographic mix of silicon carbide growth in '27 and the underlying contribution from new platforms and content gains versus just a recovery in the underlying EV production?

**Hassane El-Khoury** (Executives):
I think it's very broad in nature. Of course, from an EV perspective, China remains a strong pull for silicon carbide. But also a big growth in new products on silicon carbide is coming from North America with AI data centers. And of course, JFET specifically that I called out in my prepared remarks, that primarily is going into AI data center. So I would say since the EV diversification we've had geographically and end customer, we are adding now a very broad AI diversified market for silicon carbide, both by application, customer and geography.

**Operator** (Operator):
Our next question comes from Tore Svanberg with Stifel.

**Tore Svanberg** (Analysts):
Yes. Hassane, I wanted to go back to what you mentioned about the business continuity plans. I mean we all know that the capacity, especially for AI data centers has been tight for a while, right? So I'm just curious what's driving the auto OEMs to be willing to restock right now? And it must be a sign that their demand is really starting to accelerate? Or do I get that wrong?

**Hassane El-Khoury** (Executives):
No. I mean I don't know about accelerate, but I think there is demand that they are working on. Remember, for us, it's not just the SAAR, it's the content. So as you heard in my prepared remarks, Europe is moving into the 48-volt and zonal, that creates a higher demand opportunity from a content perspective, not necessarily vehicle units. Mix of EVs is higher, which is more content.
So you can think about it, demand that I refer to from our side is content. So when we talk about resuming to our long-term model, which is high single digit over SAAR, that's the one I'm referring to. That's what the OEMs place orders for. It's -- they see their content growth in their new platforms that they are introducing, not necessarily a SAAR or unit. So that's what I want to be very clear. Inventory for us is content in the car.

**Tore Svanberg** (Analysts):
Yes. That's very helpful. And as my follow-up on Ferric, so I think there's a lot of companies positioning in IVR right now. And I was just hoping you could share with us a little bit what's the uniqueness that Ferric brings? I know in your presentation, you talked about better magnetics, smaller footprint and so on and so forth. But yes, anything else that you could share with us why their technology is sort of the winning formula versus what we've seen from other companies?

**Hassane El-Khoury** (Executives):
Yes. So if you think about what the solution -- what the end solution needs in order for it to be viable from an IVR perspective, there's a thermal, a mechanical and an electrical. From an electrical perspective, we know Ferric has a superior transient performance than anything else in the market. So that covers the electrical. That's important because of the dynamic load that high-end processors are driving, where you got a lot of transient and the voltages have to regulate or respond to it.
So that provides a superior electrical performance versus peers or competitors. Then you have the mechanical side of it, which is the power density, where there are other solutions that are not necessarily magnetic. There are other innovative solutions out there, but the solution from Ferric with electro and magnetic components of it with the controller, that gives you the most dense from an area and the most compact from a z-height. The -- you can think about everybody's z-height is in the 2.5 millimeter.
Ferric blows that away. So that is extremely important when you're talking about truly integrated or IVR specifically, not outside of the package and so on. So that's key. And then the last one is the thermal. With the efficiency that the first 2 provide, the thermal becomes a lesser of a problem to resolve with the GPU or the compute vendors. Those 3 components, the Venn diagram, if you put all of them together, Ferric is the one in the middle. That's why we like it. That's why we wanted that asset rather than comparing to everything else.

**Operator** (Operator):
This concludes the question-and-answer session. I would now like to turn it back to Hassane El-Khoury, President and CEO, for closing remarks.

**Hassane El-Khoury** (Executives):
Thank you for your questions. We are focused on the areas where the challenges are getting harder and where our differentiation matters most. Power density is becoming critical across AI data center, automotive and industrial, and our investments in high-voltage technologies, Treo-based solutions and EPP enable us to solve those challenges at the device, platform and system level. Combined with the leverage in our operating model, we believe that positions us to drive profitable growth, stronger cash generation and long-term shareholder value. Thank you for joining us today.

**Operator** (Operator):
This concludes today's conference call. Thank you for participating. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ON_Q2_2026_Earnings_Call_20260803.md
- 2026-08-03｜CFO Thad Trent｜guidance：Q3 營收財測區間（原話："in the range of $1.65 billion to $1.75 billion"）
- 2026-08-03｜CFO Thad Trent｜guidance：Q3 non-GAAP 毛利率財測區間（原話："is expected to be between 40% and 42%"）
- 2026-08-03｜CFO Thad Trent｜guidance：Q3 non-GAAP EPS 財測區間（原話："earnings per share in the range of $0.81 to $0.93."）
- 2026-08-03｜CFO Thad Trent｜guidance：Q3 分部財測：車用小增、工業持平、其他（含 AI 資料中心）高十位數增（原話："we expect auto to be up low single digits"）
- 2026-08-03｜CEO Hassane El-Khoury｜guidance：2026 AI 資料中心營收預期由「翻倍」上調為「超過翻倍」（原話："AI data center revenue to more than double in 2026"）
- 2026-08-03｜CEO Hassane El-Khoury｜guidance：2026 AI 資料中心碳化矽營收預期成長近 60%（原話："AI data center applications to grow nearly 60%"）
- 2026-08-03｜CEO Hassane El-Khoury｜guidance：2026 ESS 營收預期成長約 40%（原話："We expect our ESS revenue to grow approximately 40%"）
- 2026-08-03｜CEO Hassane El-Khoury｜guidance：中國車用碳化矽營收預期成長 60% 至 70%（原話："revenue in that market to increase between 60% and 70%"）
- 2026-08-03｜CFO Thad Trent｜guidance：2026 資本支出占營收預期低於 5%（原話："expenditure for the year to be below 5% of revenue."）
- 2026-08-03｜CFO Thad Trent｜margin：Q2 non-GAAP 毛利率季增 80 bps（原話："Non-GAAP gross margin expanded 80 basis points"）
- 2026-08-03｜CFO Thad Trent｜margin：Q2 毛利率改善來源為製造表現與有利產品組合；稼動率升至 83%（原話："Utilization increased to 83%"）
- 2026-08-03｜CFO Thad Trent｜margin：稼動率每提高一點對應毛利率改善 25 至 30 bps 的口徑（原話："The math is 25 basis points to 30 basis points"）
- 2026-08-03｜CFO Thad Trent｜margin：管理層表示 Q2 漲價對毛利率沒有明顯貢獻（被投入成本抵銷）（原話："wasn't much of a margin impact at all from pricing"）
- 2026-08-03｜CFO Thad Trent｜margin：稼動率約兩季後反映在損益表，Q4 稼動率下滑是 Q2 的逆風（原話："there's about 2 quarter for utilization to hit the P&L"）
- 2026-08-03｜CFO Thad Trent｜margin：Fab Right 出售兩座廠預計貢獻約 50 bps 的 200 bps 毛利率改善（原話："approximately 50 basis points of the 200 basis points"）
- 2026-08-03｜CFO Thad Trent｜margin：出售 Mountain Top 與菲律賓廠年化節省金額（原話："approximately $35 million of annualized savings"）
- 2026-08-03｜CFO Thad Trent｜margin：管理層表示因折舊已進入穩定狀態，且產能已下線約 12%（原話："we took capacity offline about 12%"）
- 2026-08-03｜CFO Thad Trent｜margin：管理層說明稼動率約 92% 至 93% 視為滿載，之後轉往外部代工（原話："in that low 90% with 92%, 93% is fully utilized"）
- 2026-08-03｜CFO Thad Trent｜commitment：管理層承諾營運費用成長慢於營收（原話："increase at a slower pace than revenue"）
- 2026-08-03｜CEO Hassane El-Khoury｜commitment：Synaptics 收購預計 2027 年中完成（原話："We expect the transaction to close in mid-"）
- 2026-08-03｜CFO Thad Trent｜commitment：截至年初累計回饋股東約 105% 的自由現金流（原話："we have returned approximately 105% of free cash flow."）
- 2026-08-03｜CFO Thad Trent｜capital_allocation：Q2 股票回購金額（原話："returned $332 million to shareholders"）
- 2026-08-03｜CFO Thad Trent｜capital_allocation：中期資本支出目標為營收的中個位數百分比（原話："kind of in that mid-single-digit percentage range"）
- 2026-08-03｜CEO Hassane El-Khoury｜commitment：管理層承諾 2026 年將樣品出貨產品數量加倍（原話："We remain on track to double the number of products sampling"）
- 2026-08-03｜CFO Thad Trent｜commitment：非核心營收退出已完成，不再於未來財測中討論（原話："The exits are done. So the $35 million was the Q2 impact."）
- 2026-08-03｜CEO Hassane El-Khoury｜customer：中國車用營收上半年成長 13%（原話："our automotive revenue increased 13% in the first half"）
- 2026-08-03｜CEO Hassane El-Khoury｜customer：擴大在 NVIDIA MGX 生態系角色（原話："We have expanded our role in the NVIDIA MGX ecosystem"）
- 2026-08-03｜CEO Hassane El-Khoury｜customer：取得 Great Wall 兩個電源平台設計案（原話："we secured 2 power supply platform wins with Great Wall"）
- 2026-08-03｜CEO Hassane El-Khoury｜customer：AWS 電源與備援電池設計案（原話："design wins supporting AWS power supply and battery backup"）
- 2026-08-03｜CEO Hassane El-Khoury｜customer：Rivian R2 平台內容（原話："some customers ordering out into '28, trying to lock up supp"）
- 2026-08-03｜CFO Thad Trent｜customer：部分客戶下單至 2028 年以鎖定供給（原話："we prioritized shipments to AI data center"）
- 2026-08-03｜CFO Thad Trent｜customer：AI 資料中心需求排擠車用與工業出貨（敘事新增）（原話："we prioritized shipments to AI data center over"）
- 2026-08-03｜CFO Thad Trent｜customer：通路庫存週數下降，大眾市場營收季增（原話："Rivian's R2 platform"）
- 2026-08-03｜CEO Hassane El-Khoury｜competition：管理層自稱為涵蓋完整 AI 電力樹的唯一美國寬頻功率半導體供應商（原話："the only broad-based U.S. power semiconductor supplier"）
- 2026-08-03｜CEO Hassane El-Khoury｜competition：管理層表示不做多供應商產品，因毛利不吸引（原話："you can imagine the margin is not as exciting"）
- 2026-08-03｜CFO Thad Trent｜competition：管理層拒絕與競爭對手比較稼動率（原話："I don't want to comment about our competitors."）
- 2026-08-03｜CEO Hassane El-Khoury｜product：800V DC 機櫃預期 2027 年底至 2028 年初開始放量（原話："end of '27, beginning of '28, give or take a quarter"）
- 2026-08-03｜CEO Hassane El-Khoury｜product：每機櫃含量高壓成長約 10 倍，中低壓約 5 至 6 倍（原話："one is going up 10x, one is going up like 5x to 6x"）
- 2026-08-03｜CEO Hassane El-Khoury｜product：AI 資料中心 TAM 以 2030 年為基準（原話："the number we're anchoring on is 2030."）
- 2026-08-03｜CEO Hassane El-Khoury｜risk：供應商成本上漲，管理層不預期 2027 年定價轉軟（原話："I'm not expecting a softer pricing environment in '27"）
- 2026-08-03｜CFO Thad Trent｜risk：前置時間由約 27 週拉長（原話："lead times stretched out from about 27 weeks to"）
- 2026-08-03｜CFO Thad Trent｜risk：簽單出貨比數季以來顯著高於 1（原話："book-to-bill ratio has been significantly above 1"）
- 2026-08-03｜CFO Thad Trent｜risk：營收仍有約 25% 至 30% 的成長空間才會碰到產能上限（原話："revenue is still 25%, 30% higher than the run rate today"）
- 2026-08-03｜CFO Thad Trent｜guidance：9 月 16 日將於紐約舉行分析師日（原話："Analyst Day in New York on September 16."）

### ON_Analyst_Investor_Day_ON_Semiconductor_Corporation_20260916.md
- 2026-09-16｜Thad Trent｜guidance：2030 長期營收成長率模型 12–14%，高於前一版模型（原話："you get to about a 12% to 14% growth rate for the company"）
- 2026-09-16｜Thad Trent｜guidance：前一版長期成長模型為 10–12%，本次上調，主因 AI 資料中心（原話："Previous model was 10% to 12%, so we're taking that up"）
- 2026-09-16｜Thad Trent｜guidance：以 2026 年 Street 共識為基礎，2030 年營收略低於 110 億美元（原話："just under $11 billion of revenue in 2030"）
- 2026-09-16｜Thad Trent｜guidance：數字口徑：模型的 2026 基期是 Street 共識，不是公司自己的預估（原話："It's not our estimates, it's actually your estimates."）
- 2026-09-16｜Thad Trent｜guidance：數字口徑：長期模型假設 SAAR 持平，SAAR 上升為額外順風（原話："we're assuming a 0 SAAR"）
- 2026-09-16｜Achyut Shah｜guidance：AI 資料中心 2030 年目標：長期成長至少高於市場 10 個百分點（原話："we are going to grow at least 10% above the market"）
- 2026-09-16｜Achyut Shah｜guidance：舉例：市場 CAGR 40% 時，AIDC 營收由 2026 年 5 億美元基期成長至 2030 年逾 25 億美元（原話："we will deliver over $2.5 billion of revenue just in 2030"）
- 2026-09-16｜Achyut Shah｜guidance：2026 年 AI 資料中心業務預計成長逾一倍（原話："more than double the AI data center part of our business"）
- 2026-09-16｜Achyut Shah｜guidance：對 2027 年 AI 資料中心業務再翻倍表示有能見度（原話："this business is going to double again"）
- 2026-09-16｜Sudhir Gopalswamy｜guidance：車用 2026–2030 年營收成長約 9%/年，假設 SAAR 持平（原話："we'll grow our automotive revenue at about 9% a year"）
- 2026-09-16｜Sudhir Gopalswamy｜guidance：工業市場長期成長目標 10%（原話："allow us to grow by 10% in the industrial market"）
- 2026-09-16｜Thad Trent｜guidance：自由現金流率目標由 25–30% 上調至 30–35%（原話："Our target is going to 30% to 35%."）
- 2026-09-16｜Thad Trent｜guidance：2026 年 Street 共識自由現金流約 16 億美元（原話："about $1.6 billion in free cash flow for 2026"）
- 2026-09-16｜Thad Trent｜guidance：Synaptics 獨立計畫：成長率高於 15%，毛利率高於 55%（原話："We're looking at margins higher than 55%"）
- 2026-09-16｜Thad Trent｜guidance：Synaptics 前 18 個月協同效益 2 億美元，已含股權報酬（原話："$200 million of synergies in this number"）
- 2026-09-16｜Thad Trent｜guidance：數字口徑：長期模型為 onsemi 獨立數字，不含 Synaptics；預期明年完成交易（原話："It has nothing to do with Synaptics."）
- 2026-09-16｜Thad Trent｜margin：毛利率目標維持 53%，未上調（原話："our target remains 53%"）
- 2026-09-16｜Thad Trent｜margin：管理層把 53% 定位為里程碑，達成後再談更高（原話："The 53% is a milestone. It's not a destination."）
- 2026-09-16｜Thad Trent｜margin：毛利率拆解：稼動率貢獻 650 bp（原話："you've got utilization, 650 basis points."）
- 2026-09-16｜Thad Trent｜margin：稼動率口徑：去年底 68%，2026 Q2 約 83%（原話："exited last year at 68%. We're roughly around 83% in Q2"）
- 2026-09-16｜Thad Trent｜margin：毛利率拆解：Fab Right 貢獻 225 bp，比以往說法更高，納入已宣布的出售（原話："On the Fab Right, 225 basis points."）
- 2026-09-16｜Thad Trent｜margin：Fab Right 225 bp 中已有 50 bp 確定，其餘約 18–24 個月內認列（原話："Now 50 of that is already in the bag."）
- 2026-09-16｜Thad Trent｜margin：營收成長 12–14% 搭配 53% 毛利率下，毛利金額成長 22%（原話："gross profit dollars are going to grow by 22%"）
- 2026-09-16｜Thad Trent｜margin：營業利益成長速度為營收的兩倍（原話："Operating income is going to grow 2x revenue."）
- 2026-09-16｜Thad Trent｜margin：2030 模型營業利益率 38%（原話："You get to an operating margin of 38%"）
- 2026-09-16｜Thad Trent｜margin：漲價進入第二輪，用來抵銷已發生的投入成本（原話："We're raising pricing with our customers"）
- 2026-09-16｜Thad Trent｜margin：投入成本逆風已先出現在毛利率，漲價效益尚未跟上（原話："headwind of the input cost hitting the margin line already"）
- 2026-09-16｜Thad Trent｜margin：答分析師：毛利率路徑建議以線性建模，市場快則可更快（原話："I would think about a pretty linear progression."）
- 2026-09-16｜Thad Trent｜margin：與歷史相比，現有晶圓廠成本結構在同稼動下低 17%（原話："the current cost structure is 17% lower"）
- 2026-09-16｜Thad Trent｜capital_allocation：資本支出強度維持約 5%，擴產在既有廠區內（原話："We can do this at about a 5% capital intensity."）
- 2026-09-16｜Thad Trent｜capital_allocation：2023–2026 買回 42 億美元股票，占自由現金流 92%（原話："we bought back $4.2 billion of shares while investing"）
- 2026-09-16｜Thad Trent｜capital_allocation：上述期間股數減少 12%（原話："we've reduced our share count by 12% during that time"）
- 2026-09-16｜Thad Trent｜capital_allocation：現有買回授權尚餘 53 億美元（原話："We've got $5.3 billion left on our existing authorization."）
- 2026-09-16｜Thad Trent｜capital_allocation：股東回饋計畫：扣除其他投資後，自由現金流 100% 回饋股東（原話："100% free cash flow back to shareholders"）
- 2026-09-16｜Thad Trent｜capital_allocation：過去 5 年投入 87 億美元，換得約 810 億美元 TAM 擴張（原話："$8.7 billion for an $81 billion TAM expansion"）
- 2026-09-16｜Thad Trent｜capital_allocation：約 65% 產品仍由外部代工，晶圓廠網路已整併（原話："we'll be manufacturing about 65% externally"）
- 2026-09-16｜Thad Trent｜commitment：承諾預測期間不再增加 brownfield 產能投資（原話："there won't be additional brownfield investment"）
- 2026-09-16｜Thad Trent｜commitment：9 億美元非核心業務退出已全部完成（原話："the exits are now done and behind us"）
- 2026-09-16｜Hassane El-Khoury｜commitment：EPP 量產無須增加資本支出，併入 5% 基線（原話："there is no incremental investment."）
- 2026-09-16｜Sudhir Gopalswamy｜commitment：車用 SiC 下一代將於約兩個月內發表，性能每代提升 25% 以上（原話："increase by 25% or even more by generation"）
- 2026-09-16｜Sudhir Gopalswamy｜commitment：管理層表示打算與客戶分享所創造的價值（原話："we intend to share that value that we create"）
- 2026-09-16｜Achyut Shah｜product：宣布今年贏得主要 Vcore 插槽，營收 2026 年底起認列（原話："we won a major Vcore socket this year"）
- 2026-09-16｜Achyut Shah｜product：每機櫃 onsemi 內容價值由約 1.5 萬美元提升至逾 11.5 萬美元（原話："about $15,000 a rack to over $115,000"）
- 2026-09-16｜Achyut Shah｜product：sidecar 架構 800V 機櫃預計約 12–18 個月內（2027 年底）開始放量（原話："start ramping in the next 12 to 18 months"）
- 2026-09-16｜Achyut Shah｜product：固態變壓器世代預計 2028 年底至 2029 年初開始（原話："sometime in the end of '28, early '29"）
- 2026-09-16｜Hassane El-Khoury｜product：車用乙太網路 10BASE-T1S 區域架構首個車用新客戶量產預計今年底開始（原話："ramp starting actually at the end of this year"）
- 2026-09-16｜Sudhir Gopalswamy｜product：車用每車 onsemi 內容機會最高 2,000 美元（原話："up to $2,000 of onsemi content per vehicle"）
- 2026-09-16｜Sudhir Gopalswamy｜product：實體 AI（不含車用）2030 年對公司 TAM 約 60 億美元（原話："represents a $6 billion TAM for us by 2030"）
- 2026-09-16｜Achyut Shah｜competition：AI 電力樹由格點到核心全覆蓋者只剩兩家（原話："left with just 2 companies onsemi and one more"）
- 2026-09-16｜Achyut Shah｜competition：高壓中段（SiC／GaN）具備規模的競爭者僅 3–4 家（原話："there's just a handful, 3 or 4 competitors"）
- 2026-09-16｜Hassane El-Khoury｜competition：管理層稱垂直 GaN 領先最接近的競爭者約五年（原話："half a decade ahead from the closest competitor"）
- 2026-09-16｜Hassane El-Khoury｜competition：管理層稱 EPP 的優勢是熱與機構面，不只是電氣面（原話："is not electrical. It's thermal and mechanical."）
- 2026-09-16｜Achyut Shah｜competition：管理層承認在 Vcore 較晚進入市場，稱已追上（原話："we came a little later to the market"）
- 2026-09-16｜Achyut Shah｜risk：800V 新架構轉換時程：管理層承認一直存在疑慮，稱與客戶有對應方案（原話："there is always a concern when it comes to a new market"）
- 2026-09-16｜Hassane El-Khoury｜risk：答分析師：800V 滲透不會一次到位，影響成長曲線時間（原話："The 800-volt is not going to go flip the switch"）
- 2026-09-16｜Thad Trent｜customer：無單一 10% 客戶，前 20 大客戶占營收 35%（原話："No 10% customer and our top 20 customers are 35% of revenue."）
- 2026-09-16｜Thad Trent｜customer：客戶總數約 9,000 家（原話："We have 9,000 customers around the globe."）
- 2026-09-16｜Achyut Shah｜customer：管理層稱與所有主要資料中心客戶深度綁定（原話："we are deeply embedded with all of these customers"）

### 問答異常語氣（迴避／改口／保留）
- ON_Q2_2026_Earnings_Call_20260803.md｜問：Quinn Bolton 追問 AI 資料中心營收是否明顯高於上季提到的 5 億美元｜答法：CEO 回答「I'll let you run the numbers」並表示不再進一步拆分，未給數字
- ON_Q2_2026_Earnings_Call_20260803.md｜問：Joe Moore 問稼動率與競爭對手相比及能否搶市占｜答法：CFO 表示不評論競爭對手，改談自身稼動率與彈性
- ON_Q2_2026_Earnings_Call_20260803.md｜問：Jim Schneider 問 2027 年供應商投入成本與定價把握度｜答法：CEO 只給方向（不會下降）與「有可見度」，未給幅度或數字
- ON_Analyst_Investor_Day_ON_Semiconductor_Corporation_20260916.md｜問：Vivek Arya (BofA)：AI 資料中心 2027 年約 10 億美元、2030 年 25 億美元以上，成長明顯減速，是保守嗎？｜答法：Achyut Shah 與 Hassane 皆未直接說明是否保守，改稱數字只反映分析師 4 年預估基線、會高於市場 10 個百分點，並指 800V 滲透需時間；未給 2030 年自家預測

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
{"date":"20260620","verdict":"B 衛星候選/觀望（深度週期股剛Q1'26 inflect +5%YoY，股價自52W低$44.56已近3倍且跑過分析師均標$106；SiC#2+CIS#1+FCF韌性真實，但EV放緩是SiC結構逆風+Sony CIS競爭+估值🟠+MA🟡觀察池後谷底火箭極伸展；機率加權合理價$71/-42%下行不對稱；等大幅回檔$70-85+SiC/EV復甦確認，長期信心僅中）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"週期谷底反轉確立 + SiC/汽車復甦（EV 放緩不致命）","columns":{"2Y 驗證點":"FY26-27 營收持續 YoY 正成長、SiC 回正","5Y 驗證點":"FY28-30 營收回 $8B+（前峰）、SiC 重拾成長","10Y 驗證點":"SiC 滲透 EV/工業長坡兌現","數字門檻":"FY27 營收 &gt; $7B","來源":"ON 法說 / SiC 市場報告","漂移觸發":"SiC 連 2 季 YoY 仍負 + PSG QoQ 轉負 → 反轉（2Y，QC-35）"}},{"id":"H2","text":"AI 資料中心電源成新引擎","columns":{"2Y 驗證點":"2026 資料中心營收翻倍（&gt;$500M）","5Y 驗證點":"FY28-30 資料中心成 ON 第三大支柱","10Y 驗證點":"AI 電源結構性需求持續","數字門檻":"2026 資料中心 &gt;$500M","來源":"ON Q1'26 guide（翻倍）","漂移觸發":"資料中心 QoQ 增速明顯放緩 → 削弱（2Y）"}},{"id":"H3","text":"fab-right → 結構性 margin 提升","columns":{"2Y 驗證點":"FY27 非 GAAP GM 回 42%+","5Y 驗證點":"FY30 GM 朝高 40%/50%（前峰 49%）","10Y 驗證點":"fab-right 成本結構固化","數字門檻":"FY27 非 GAAP GM ≥ 42%","來源":"ON 法說 / fab-right 進度","漂移觸發":"GM 連 4 季 &lt; 39% → 削弱（5Y）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"EV 放緩使 SiC 復甦落空（結構性需求逆風）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"SiC/汽車營收 YoY、EV 銷量、PSG QoQ","警戒閾值":"SiC 連 2 季 YoY 負 + PSG QoQ 轉負 → 減倉"}},{"id":"R2","text":"Sony CIS 競爭侵蝕 ISG（汽車影像感測）","columns":{"對應假設":"—","時間尺度":"🔥 中期（4-6 季）","監測指標":"ISG 段營收、汽車 CIS 份額","警戒閾值":"ISG 連 2 季衰退 + 份額流失 → 重評"}},{"id":"R3","text":"股價已跑過共識 → 反轉行情退潮","columns":{"對應假設":"H1/估值","時間尺度":"⚡ 短期（1-2 季）","監測指標":"股價 vs 分析師均標 $106、動能","警戒閾值":"股價維持 &gt; 均標 20% + 動能轉弱 → 等回檔"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"🟡","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":121.62,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ON_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
