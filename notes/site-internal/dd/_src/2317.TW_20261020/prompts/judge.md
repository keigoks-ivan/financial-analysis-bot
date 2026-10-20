你是 stock-analyst **v20 判斷 agent**，標的 2317.TW（20261020）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"2317.TW","date":"2026-10-20","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2317.TW_20261020/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2317.TW_20261020/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP 合併）","value":2525.9,"period":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","unit":"十億 TWD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","citation":"鴻海 2026Q2 法說會（公司 IR https://www.honhai.com/zh-tw/investor-relations ；具體新聞稿頁未直接取得，數字經 https://blog.fugle.tw/post/earnings-call-2317-2026-08-12 轉述並與 yfinance quarterly_income_stmt 核對）；yfinance quarterly 報表（2026-06-30 欄）"},"note":"未取得單季共識"},{"id":"f_kpi1_gaap","label":"毛利率（GAAP）","value":6.12,"period":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","citation":"鴻海 2026Q2 法說會（公司 IR https://www.honhai.com/zh-tw/investor-relations ；具體新聞稿頁未直接取得，數字經 https://blog.fugle.tw/post/earnings-call-2317-2026-08-12 轉述並與 yfinance quarterly_income_stmt 核對）"},"note":"未取得"},{"id":"f_kpi2_gaap_non_gaap","label":"營業利益／營業利益率（GAAP；公司不另報 Non-GAAP）","value":3.75,"period":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","unit":"%（營業利益 948.0 億 TWD，YoY +68%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","citation":"鴻海 2026Q2 法說會（公司 IR https://www.honhai.com/zh-tw/investor-relations ；具體新聞稿頁未直接取得，數字經 https://blog.fugle.tw/post/earnings-call-2317-2026-08-12 轉述並與 yfinance quarterly_income_stmt 核對）；yfinance quarterly 報表（2026-06-30 欄）"},"note":"未取得"},{"id":"f_kpi3_eps","label":"稅後純益（歸屬母公司）／EPS","value":4.27,"period":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","unit":"TWD／股（純益 599.7 億 TWD，YoY +35%，QoQ +20%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","citation":"鴻海 2026Q2 法說會（公司 IR https://www.honhai.com/zh-tw/investor-relations ；具體新聞稿頁未直接取得，數字經 https://blog.fugle.tw/post/earnings-call-2317-2026-08-12 轉述並與 yfinance quarterly_income_stmt 核對）；yfinance 稀釋 EPS 4.24"},"note":"未取得"},{"id":"f_kpi6","label":"管理層指引","value":"Q3 營收較 Q2『顯著成長』、YoY『強勁成長』；全年『強勁成長』；全年營益率高於 2025 的 3.2%；AI 機櫃 Q3 出貨 QoQ 高雙位數成長；2026 資本支出 YoY +30% 以上","period":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","unit":"定性（公司未給數字區間）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","citation":"鴻海 2026Q2 法說會（公司 IR https://www.honhai.com/zh-tw/investor-relations ；具體新聞稿頁未直接取得，數字經 https://blog.fugle.tw/post/earnings-call-2317-2026-08-12 轉述並與 yfinance quarterly_income_stmt 核對）"},"note":"FY1 共識營收 10.87 兆 TWD（capital_structure）"},{"id":"f_kpi7_ai","label":"雲端網路產品占營收（AI 伺服器為主）","value":51,"period":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","citation":"鴻海 2026Q2 法說會（公司 IR https://www.honhai.com/zh-tw/investor-relations ；具體新聞稿頁未直接取得，數字經 https://blog.fugle.tw/post/earnings-call-2317-2026-08-12 轉述並與 yfinance quarterly_income_stmt 核對）"},"note":"不適用"},{"id":"f_kpi8","label":"淨現金","value":219.8,"period":"2026-06-30","unit":"十億 TWD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"2026-06-30","citation":"鴻海 2026Q2 法說會（公司 IR https://www.honhai.com/zh-tw/investor-relations ；具體新聞稿頁未直接取得，數字經 https://blog.fugle.tw/post/earnings-call-2317-2026-08-12 轉述並與 yfinance quarterly_income_stmt 核對）"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-12","period":"2026-08-12","unit":"date","basis":"距今 49 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-12"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_2317_tw_gross_margin_pct","label":"2317.TW 毛利率","value":6.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2317.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2317_tw_operating_margin_pct","label":"2317.TW 營業利益率","value":3.51,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2317.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2317_tw_fcf_margin_pct","label":"2317.TW FCF 利潤率","value":-0.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2317.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2382_tw_gross_margin_pct","label":"2382.TW 毛利率","value":5.54,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2382.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2382_tw_operating_margin_pct","label":"2382.TW 營業利益率","value":3.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2382.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2382_tw_fcf_margin_pct","label":"2382.TW FCF 利潤率","value":-1.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2382.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3231_tw_gross_margin_pct","label":"3231.TW 毛利率","value":5.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3231.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3231_tw_operating_margin_pct","label":"3231.TW 營業利益率","value":3.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3231.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3231_tw_fcf_margin_pct","label":"3231.TW FCF 利潤率","value":-8.93,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3231.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_jbl_gross_margin_pct","label":"JBL 毛利率","value":9.23,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.gross_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_jbl_operating_margin_pct","label":"JBL 營業利益率","value":5.03,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.operating_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_jbl_fcf_margin_pct","label":"JBL FCF 利潤率","value":3.89,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.fcf_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_cls_gross_margin_pct","label":"CLS 毛利率","value":11.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cls_operating_margin_pct","label":"CLS 營業利益率","value":8.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cls_fcf_margin_pct","label":"CLS FCF 利潤率","value":3.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_fcf","label":"自由現金流（FCF）","value":-117.7,"period":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","unit":"十億 TWD（營業現金流 -72.3、資本支出 -45.4）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","citation":"yfinance quarterly 報表（2026-06-30 欄）；上半年 FCF 約 -1,500 億 TWD 與法說轉述一致"},"note":"不適用"},{"id":"f_kpi5_sbc","label":"SBC 占營業利益","value":0.78,"period":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","unit":"%（SBC 7.4 億 TWD）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"2026Q2（季末 2026-06-30，法說／公告於 2026-08-12）","citation":"yfinance quarterly 報表（2026-06-30 欄）（Stock Based Compensation）"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":242.5,"period":"2026-10-20（RTH 收盤，UTC）","unit":"TWD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-20（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":18.35,"period":"2026-10-20（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^TWII","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-20（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":43.9,"period":"2026-10-20（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-20（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.49,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（18.38 → 18.47）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.48,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.14 → 23.25）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.48,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（27.26 → 27.39）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":18.47,"period":"2026-10-08","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.8483 @ 2026-10-08)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":23.25,"period":"2026-10-08","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.8483 @ 2026-10-08)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":27.39,"period":"2026-10-08","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.8483 @ 2026-10-08)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.23,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 17.72 → 18.47（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":16.42,"period":"2026-10-20（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝95.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-20（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":95.3,"period":"2026-10-20（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-20（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.37,"period":"2026-10-20（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝88.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-20（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":88.8,"period":"2026-10-20（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-20（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.35,"period":"2026-10-20（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝68.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-20（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":68.7,"period":"2026-10-20（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-20（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":13.48,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 18.47，分子＝快照價 249.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.957,"period":"2026-10-20","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-20"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-166925.05,"period":"2026-10-20","unit":"TWD m","basis":"yfinance 最新一季：總債務 1357777.99、現金 1524703.04（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-20"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":14074.26,"period":"2026-10-20","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-20"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":3246083.92,"period":"2026-10-20","unit":"TWD m","basis":"市值 3413008.97 ＋ 淨負債 -166925.05","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-20"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":10872980.57,"period":"2026-10-20","unit":"TWD m","basis":"yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-20"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":13988541.4,"period":"2026-10-20","unit":"TWD m","basis":"yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-20"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.3,"period":"2026-10-20","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-20"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-20","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-20","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 242.5 / W52 233.05 / W104 202.57 / W250 147.64 / W250 13週斜率 1.76%"},{"id":"f_ma_w52","label":"52 週均線","value":233.05,"period":"2026-10-20","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-20","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":202.57,"period":"2026-10-20","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-20","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":147.64,"period":"2026-10-20","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-20","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.76,"period":"2026-10-20","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-20","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"搜尋摘要稱鴻海在 ASIC 伺服器市占率超過四成，並目標 2026 年底 AI 伺服器機櫃週產能由約 1,000 個提升至 2,000 多個（摘要轉述，未讀原頁，原文與確切日期未驗證）","source":"搜尋結果彙整（鴻海 對手 擴產 OR 殺價 2026）；富果研究 hon-hai-precision-analysis","url":"https://blog.fugle.tw/post/hon-hai-precision-analysis","excerpt":null,"as_of":"2026-08-10","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"搜尋摘要稱廣達追加百億資本支出擴產、緯創台美加碼擴產，且有評析指 AI 伺服器打破 ODM「完全競爭」、緯創新客戶下半年加入（摘要轉述，未讀原頁，日期為約略）","source":"搜尋結果彙整（鴻海 對手 擴產 OR 殺價 2026）；moneyweekly／cnyes 等","url":"https://www.moneyweekly.com.tw/_Article?AID=241297","excerpt":null,"as_of":"2026-08-10","retrieved_at":"2026-10-19","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"鴻海 2026Q1 財報報導提及，部分雲端與網通產品（特別是 ASIC 伺服器）轉向指定零件（consignment）下單模式，由客戶自行提供關鍵零組件；屬接單模式改變，非轉單給其他代工廠（搜尋摘要轉述，未逐字取得原文）","source":"優分析 uanalyze 鴻海2026年第一季財報報導","url":"https://uanalyze.com.tw/articles/6131751512","excerpt":null,"as_of":"2026-05-14","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"彭博研究認為鴻海 2026 年底前仍為 iPhone 組裝龍頭，未來兩年組裝占有率約 55%–60%；立訊為第二大組裝業者，預估約負責 30% iPhone 訂單（搜尋摘要轉述；文章確切發布日未取得）","source":"世界日報／彭博：即便iPhone供應鏈轉移 鴻海仍將穩居組裝龍頭","url":"https://www.worldjournal.com/wj/story/121477/9229960","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-19","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"+","claim":"鴻海 2026 年 3 月法說會表示，液冷 CDU、Bussbar、連接器等自製零組件已導入主要客戶產品並量產出貨，自製比率將提高，部分零組件仍外購（搜尋摘要轉述；來源頁面未確認）","source":"鴻海2026年3月法說會報導（搜尋摘要）","url":null,"excerpt":null,"as_of":"2026-03-01","retrieved_at":"2026-10-19","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"鴻海114年度年報（母公司個別表）主要銷貨客戶僅列匿名「戊客戶」一家：113年占銷貨淨額54.03%（3,706,464百萬元），114年占44.11%（3,574,256百萬元），與發行人無關係。","source":"公開資訊觀測站電子書件 114年股東會年報 主要銷貨客戶表（PDF第125頁）","url":"https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id=2317&year=115&seamon=&mtype=F&dtype=","excerpt":"1 戊客戶  3,706,464  54.03%  無  戊客戶  3,574,256  44.11%  無","as_of":"2026-05-19","retrieved_at":"20261020","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026年第二季法說（8月）輪值CEO表示需求能見度較5月法說進一步改善，AI需求強勁，並正向看待明年","source":"uanalyze〈鴻海法說〉Q3、全年營收強勁成長 AI需求續旺明年展望正向","url":"https://uanalyze.com.tw/articles/3108153280","excerpt":"目前需求能見度比5月法說時進一步改善；在AI需求持續強勁下，正向看待明年","as_of":"2026-08-12","retrieved_at":"2026-10-19","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"法說稱雲端服務商持續增加資本支出、AI伺服器機櫃持續放量","source":"uanalyze 鴻海法說報導","url":"https://uanalyze.com.tw/articles/3108153280","excerpt":"雲端服務商(CSP)客戶持續增加資本支出，AI伺服器機櫃持續放量","as_of":"2026-08-12","retrieved_at":"2026-10-19","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"公司稱獲利成長高於擴產支出增幅，2027年續加碼擴產、無股權籌資計畫","source":"DIGITIMES 鴻海營運獲利成長高於擴產支出增幅 2027年續加碼、無股權籌資計畫","url":"https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=764980","excerpt":"鴻海營運獲利成長高於擴產支出增幅 2027年續加碼、無股權籌資計畫","as_of":"2026-08-12","retrieved_at":"2026-10-19","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"董事長2026年3月稱今年AI伺服器每週產能2,000櫃不是問題（公司目標，非已達成）；2025年11月時為每週1,000櫃","source":"鴻海 GTC 秀人型機器人，在美建最大 AI 伺服器產能（technews）／鴻海科技日報導","url":"https://technews.tw/?p=1526841","excerpt":"劉揚偉預期，今年鴻海集團AI伺服器每週產能2,000櫃不是問題，在美國打造最大AI伺服器生產基地。","as_of":"2026-03-17","retrieved_at":"2026-10-19","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"美系外資通路調查：2026年4月鴻海機櫃出貨約3,700櫃、市占逾44%；同月全球GB200/GB300機櫃總產量環比微降3%，原因為世代交替與零組件供貨節奏","source":"technews AI 伺服器出貨鴻海領先廣達、緯創","url":"https://finance.technews.tw/2026/05/12/foxconn-leads-quanta-and-wistron-in-ai-server-shipments/","excerpt":"AI 伺服器出貨鴻海領先廣達、緯創，外資看好 2026 年產業鏈獲利全面釋放","as_of":"2026-05-12","retrieved_at":"2026-10-19","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Citi認為新一代VR AI機櫃預計第三季量產、第四季加速出貨，有望2027年成為主流產品（外資預估，非公司承諾）","source":"uanalyze 鴻海AI需求續強 法說會後美系、日系外資齊升目標價","url":"https://uanalyze.com.tw/articles/1037253322","excerpt":"鴻海AI需求續強 法說會後美系、日系外資齊升目標價4字頭起跳","as_of":"2026-08-14","retrieved_at":"2026-10-19","affects":["valuation","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"公平會處分書及決議書資料庫以「鴻海精密工業」全文搜尋共 10 筆，命中僅代表文件提及該名稱，並非鴻海被處分；列出的命中為 2015 年電容聯合行為案（他廠被處分）僅文內提及。","source":"公平交易委員會｜處分書及決議書全文搜尋「鴻海精密工業」","url":"https://www.ftc.gov.tw/internet/main/decision/decisionList.aspx?mid=11","excerpt":"【程式統計】公平會「處分書及決議書」資料庫（ftc.gov.tw 決定書查詢），以關鍵字「鴻海精密工業」全文搜尋（查詢日 2026-10-20）共 10 筆。命中只代表處分書或決議書全文提到該名稱，不代表該公司被處分","as_of":"2026-10-20","retrieved_at":"20261020","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"證交所 ESG 揭露：鴻海報告年度 114 因反競爭行為相關法律訴訟造成的金錢損失為 0。","source":"證交所 OpenAPI t187ap46_L_20 反競爭行為法律訴訟","url":"https://openapi.twse.com.tw/v1/opendata/t187ap46_L_20","excerpt":"證交所 OpenAPI t187ap46_L_20（鴻海）「企業ESG資訊揭露彙總資料—反競爭行為法律訴訟」：報告年度 114，因與反競爭行為條例相關的法律訴訟而造成的金錢損失總額(仟元)＝0.000。","as_of":"2026-10-20","retrieved_at":"20261020","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"美國 ITC 就 Vicor 專利主張對鴻海及工業富聯啟動 337 調查（專利，非反壟斷）。","source":"uanalyze 鴻海及子公司遭美國337調查","url":"https://uanalyze.com.tw/articles/2787256851","excerpt":"鴻海及子公司遭美國337調查 強調營運出貨正常、已組團隊釐清因應 2026年10月11日 17:06 - 優分析產業數據中心 圖片來源：由鉅亨網提供 美國國際貿易委員會（USITC）於美國時間2026年10月9日，就美國電源供應模組廠商Vicor Corporation提出的專利侵權主張，正式啟動337調查（調查編號：337-TA-1526），包括台達電(2308-TW)、鴻海(2317-TW)、廣達(2382-TW)等多家台廠及其關係企業被列為被調查方。","as_of":"2026-10-11","retrieved_at":"20261020","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"鴻海旗下工業富聯兩家子公司（天津富聯精密電子、南寧富聯富桂精密工業）於2023年12月被美國列入未經核實清單；該清單不等同實體清單，通過檢查可移除","source":"中央社 cna.com.tw（2023-12-21 報導）","url":"https://www.cna.com.tw/news/afe/202312210231.aspx","excerpt":"名單包括天津富聯精密電子與南寧富聯富桂精密工業","as_of":"2023-12-21","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"金融時報報導（2025年2月），北京對工程師與設備離境施加限制，使鴻海難以把設備與技術主管移往印度","source":"technews.tw 轉述金融時報","url":"https://technews.tw/2025/02/17/china-tightens-grip-on-tech-minerals-and-engineers-as-trade-war-spirals/","excerpt":null,"as_of":"2025-02-17","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"鴻海表示代工模式下關稅影響主要落在客戶；董事長劉揚偉稱關稅影響存在但因較早布局而較輕；鴻海在越南、印度、美國、墨西哥已有量產規模。報導為2025年4月對等關稅時期，非2026年最新資料","source":"工商時報 ctee.com.tw（2025-04-07）及搜尋彙整","url":"https://www.ctee.com.tw/news/20250407700076-439901","excerpt":null,"as_of":"2025-04-07","retrieved_at":"2026-10-19","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026年5月底美方公告對台灣部分汽車零件、木材製品232關稅上限15%並自5月1日追溯適用；搜尋結果未量化對鴻海的直接影響","source":"KPMG / CBP 通告","url":"https://kpmg.com/us/en/taxnewsflash/news/2026/05/united-states-modifies-tariffs-products-taiwan.html","excerpt":null,"as_of":"2026-05-28","retrieved_at":"2026-10-19","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"優分析資料稱鴻海中國產能約占70%、非中國產能約30%（含美國、墨西哥、印度、台灣、越南）；來源未註明確切日期，年代不明","source":"優分析 uanalyze 產業資料庫","url":"https://uanalyze.com.tw/articles/1665513360","excerpt":"產能佔比：鴻海在中國的產能占70%,非中國產能占30%,包括美國、墨西哥、印度、台灣、越南等地。","as_of":"2022-10-10","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"2026年報導稱鴻海以美國與墨西哥為AI伺服器主要量產基地；墨西哥契瓦瓦州2026年5月增資1.29億美元；2025年資本支出1,738億元，2026年預計增逾30%","source":"優分析 uanalyze 台灣五大ODM重構AI伺服器供應鏈 北美在地製造進入加速期","url":"https://uanalyze.com.tw/articles/6235255398","excerpt":null,"as_of":"2026-09-01","retrieved_at":"2026-10-19","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"鴻海非中國產能比重曾由30%降至25%（劉揚偉於法說會坦言）；越南為東南亞最大生產基地，大於印度","source":"工商時報／uanalyze 引述","url":"https://ec.ltn.com.tw/article/paper/1225183","excerpt":"去年8月時鴻海非中產能為30%,劉揚偉在本次法說會則坦言已降到25%。","as_of":"2021-01-01","retrieved_at":"2026-10-19","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2020年疫情期間中國當局不同意鴻海深圳、鄭州廠區如期復工，顯示單一地區廠區停工風險（歷史事件）","source":"TechNews 引述日經亞洲評論","url":"https://technews.tw/?p=565699","excerpt":"由於 2019 新型冠狀病毒(2019-nCoV,武漢肺炎)疫情蔓延，中國當局不同意鴻海集團的深圳、鄭州廠區在 2 月 10 日復工。","as_of":"2020-02-07","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"鴻海2026年9月營收單月首度突破1.15兆元，第三季營收約3.02兆元、年增47.12%，前9月累計7.67兆元、年增39.53%","source":"優分析／鉅亨網報導 鴻海9月營收1.15兆元月增25% 單月首度破兆創新高","url":"https://uanalyze.com.tw/articles/4830556496","excerpt":"鴻海(2317-TW)今(5)日公告9月營收1.15兆元，單月營收首度突破兆元大關","as_of":"2026-10-05","retrieved_at":"2026-10-19","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"凱基證券預估鴻海雲端業務營收占比由2025年40%升至2026年55%、2027年62%（券商估計，非公司公布）","source":"KGI Hon Hai Precision 2317 TT 報告 20260810","url":"https://www.kgi.com.hk/zh-cn/-/media/files/kgishk/research-reports/tw-reports/hon-hai-precision-2317-tt20260810en.pdf","excerpt":"預期公司雲端業務營收占比將由2025年的40%提升至2026年的55%，並進一步於2027年達62%","as_of":"2026-08-10","retrieved_at":"2026-10-19","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"公司指引：AI機櫃今年出貨估倍增，800G以上交換器出貨可望倍增","source":"鴻海營收／展望相關報導（搜尋摘要）","url":"https://www.ctee.com.tw/news/20260805701610-430201","excerpt":"AI機櫃今年出貨估達倍增，AI多種解決方案出貨可望逐季增，800G以上的交換器出貨亦可望倍增","as_of":"2026-08-05","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年7月營收：雲端網路與電腦終端均較6月強勁成長","source":"鴻海第2季營收攀歷年同期新高 第3季可望季增年增／7月營收報導","url":"https://www.ctee.com.tw/news/20260805701610-430201","excerpt":"雲端網路產品受惠AI產品拉貨動能強勁、電腦終端產品受惠拉貨動能轉強，7月營收均較6月強勁成長","as_of":"2026-08-05","retrieved_at":"2026-10-19","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"第四季展望：AI相關業務續成長，ICT產品處於下半年傳統旺季","source":"鴻海9月營收公告報導","url":"https://uanalyze.com.tw/articles/4830556496","excerpt":"AI相關業務將持續成長，加上ICT產品仍處於下半年傳統旺季","as_of":"2026-10-05","retrieved_at":"2026-10-19","affects":["moat_trend","triggers"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"0","claim":"2026年5月營收：消費智能強勁成長，雲端網路約略持平，電腦終端與元件略衰退","source":"鴻海5月營收報導（搜尋摘要）","url":"https://money.udn.com/money/amp/story/5607/9548246","excerpt":"「雲端網路產品類別」約略持平，AI持續拉貨；「電腦終端產品類別」與「元件及其他產品類別」則略為衰退","as_of":"2026-06-05","retrieved_at":"2026-10-19","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"富果研究 2Q26 法說摘要指出：ASIC 伺服器興起後，鴻海已取得多家雲端業者機櫃訂單，預期 2027 年新增一家 ASIC 機櫃出貨客戶（搜尋摘要轉述，未讀頁面原文）","source":"富果研究 鴻海(2317) 2026年第二季法說分析","url":"https://blog.fugle.tw/post/earnings-call-2317-2026-08-12","excerpt":null,"as_of":"2026-08-12","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2026-05-14 法說會：管理層指出 AI 客戶變多元後集團產品結構會更平衡，首季獲利創同期新高，歸因於產品組合優化與營運效率；雲端網路產品占比已近五成（來自搜尋摘要轉述，未讀原頁）","source":"中國時報 旺得富 2026-05-14 法說報導","url":"https://wantrich.chinatimes.com/news/20260514900610-420101","excerpt":null,"as_of":"2026-05-14","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2025Q4 財報：雲端網路產品營收占比 42%，首度超越消費智能產品的 39%（搜尋摘要轉述，未讀原頁）","source":"中文財經媒體法說報導（鉅亨網／經濟日報系搜尋結果）","url":"https://news.cnyes.com/news/id/4815573","excerpt":null,"as_of":"2026-03-01","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"電動車以 BOL（構建、營運、在地化）模式與泰國國家石油公司合資建立生態系；董事長劉揚偉以「3+3+3」策略推動轉型（媒體轉述，非公司一手文件）","source":"uanalyze 鴻海轉型有成 董座劉揚偉獲選2026全球百大製造業領袖第7名","url":"https://uanalyze.com.tw/articles/1857656130","excerpt":null,"as_of":"2026-09-01","retrieved_at":"2026-10-19","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"KGI 2026-08-10 報告預期鴻海 8/12 法說會公布 2Q26 財報與展望，預估 2Q26 毛利率與營益率穩健、季增；此為券商預估，非公司 guidance。","source":"KGI 鴻海 2317 TT 研究報告 (hon-hai-precision-2317-tt20260810en.pdf)","url":"https://www.kgi.com.hk/zh-cn/-/media/files/kgishk/research-reports/tw-reports/hon-hai-precision-2317-tt20260810en.pdf","excerpt":null,"as_of":"2026-08-10","retrieved_at":"2026-10-19","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026 年 Q1 法說前，本土法人維持買進並將目標價由 305 元調升至 330 元，預估 2026 全年 EPS 18.41 元、營收約 10.03 兆元（日期為 2026 年 Q1 法說前後，確切發布日搜尋摘要未顯示）。","source":"鉅亨網「鴻海法說下午登場關注四大焦點 本土法人暖場喊買調升目標價」","url":"https://news.cnyes.com/news/id/6457768","excerpt":"鴻海法說下午登場關注四大焦點 本土法人暖場喊買調升目標價","as_of":"2026-05-01","retrieved_at":"2026-10-19","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"高盛上調鴻海目標價至 400 元，為搜尋結果中內外資最高；大摩目標價 317 元（優於大盤），樂觀情境上看 444 元。發布日期摘要未顯示（as_of 為估計，約 2025 年底至 2026 年初）。","source":"經濟日報「高盛上調鴻海目標價至400元 預估第4季營收達2.8兆元創高」；「鴻海目標價 喊到444」","url":"https://money.udn.com/money/amp/story/5607/9123167","excerpt":"高盛上調鴻海目標價至400元 預估第4季營收達2.8兆元創高","as_of":"2025-12-01","retrieved_at":"2026-10-19","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-01 月營收 5,387 億元，年增約 3%、月減 17%；2025 全年營收 8.09 兆元年增 18%。搜尋未取得 2026 年 9 月以後月營收。","source":"Yahoo 股市「AI伺服器出貨助創同期次高!鴻海元月營收5,387億 年增3%、月減17%」","url":"https://tw.stock.yahoo.com/news/ai%E4%BC%BA%E6%9C%8D%E5%99%A8%E5%87%BA%E8%B2%A8%E5%8A%A9%E5%89%B5%E5%90%8C%E6%9C%9F%E6%AC%A1%E9%AB%98%EF%BC%81%E9%B4%BB%E6%B5%B7%E5%85%83%E6%9C%88%E7%87%9F%E6%94%B65387%E5%84%84-%E5%B9%B4%E5%A2%9E3%E3%80%81%E6%9C%88%E6%B8%9B17-084055891.html","excerpt":"AI伺服器出貨助創同期次高!鴻海元月營收5,387億 年增3%、月減17%","as_of":"2026-02-05","retrieved_at":"2026-10-19","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"鴻海公告子公司 Foxconn (Far East) Limited 對 Maxnerva Technology Services Limited 發動公開要約收購，事實發生日 2026-07-27（交易金額與進度搜尋摘要未載）","source":"公開資訊觀測站重大訊息（經搜尋摘要轉述）","url":"https://wantrich.chinatimes.com/news/20260805900497-420101","excerpt":null,"as_of":"2026-07-27","retrieved_at":"2026-10-19","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"美國國際貿易委員會依 Vicor 專利侵權主張啟動 337 調查，鴻海及子公司列為被調查方；鴻海稱案件在立案初期，產品、生產營運及出貨未受影響","source":"technews 財經 337 Vicor 報導 / uanalyze","url":"https://finance.technews.tw/2026/10/11/337-usa-victor/","excerpt":null,"as_of":"2026-10-11","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ems_utilization_capex_cycle#0","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"+","claim":"鴻海日本8吋晶圓廠稼動率突破90%（僅見標題，內文未讀）","source":"DIGITIMES 鴻海EV、機器人與半導體齊步推進 日本8吋晶圓廠稼動率破90%","url":"https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=764963","excerpt":"鴻海EV、機器人與半導體齊步推進 日本8吋晶圓廠稼動率破90%","as_of":"2026-08-12","retrieved_at":"2026-10-19","affects":["moat_trend"],"status":"ok"},{"id":"ems_utilization_capex_cycle#1","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"0","claim":"2026年資本支出預期年增3成以上；2025年約1738億元，2026上半年約809億元，用於AI伺服器、機櫃、液冷產能及台灣、美國、墨西哥、越南等地擴產（金額與用途為搜尋摘要轉述，無逐字原文）","source":"Focus Taiwan Hon Hai's 2026 capex to focus on AI expansion","url":"https://focustaiwan.tw/business/202608120019","excerpt":"Hon Hai's 2026 capex to focus on AI expansion","as_of":"2026-08-12","retrieved_at":"2026-10-19","affects":["valuation","thesis.R"],"status":"ok"},{"id":"ems_utilization_capex_cycle#2","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"0","claim":"鴻海法說：今年資本支出估增3成，前期投入已逐步反映在營運成果","source":"優分析 〈鴻海法說〉今年資本支出估增3成 前期投入已逐步反映在營運成果","url":"https://uanalyze.com.tw/articles/7326553299","excerpt":"〈鴻海法說〉今年資本支出估增3成 前期投入已逐步反映在營運成果","as_of":"2026-08-12","retrieved_at":"2026-10-19","affects":["valuation"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#none","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"鴻海公告子公司 Foxconn (Far East) Limited 對 Maxnerva Technology Services Limited 發動公開要約收購，事實發生日 2026-07-27","source":"公開資訊觀測站重大訊息（經搜尋摘要轉述）","url":"https://wantrich.chinatimes.com/news/20260805900497-420101","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261020","affects":["valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"美國 ITC 啟動 337 調查（Vicor 專利侵權主張），鴻海及子公司列為被調查方；鴻海稱未影響出貨","source":"technews 財經 337 Vicor 報導","url":"https://finance.technews.tw/2026/10/11/337-usa-victor/","excerpt":null,"as_of":"2026-10-11","retrieved_at":"20261020","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"2317.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":6.12,"operating_margin_pct":3.51,"fcf_margin_pct":-0.46,"rd_intensity_pct":1.31},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2317.TW","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"2382.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":5.54,"operating_margin_pct":3.34,"fcf_margin_pct":-1.2,"rd_intensity_pct":1.29},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2382.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"3231.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":5.85,"operating_margin_pct":3.8,"fcf_margin_pct":-8.93,"rd_intensity_pct":1.15},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3231.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"JBL","period":"TTM ending 2026-05-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.23,"operating_margin_pct":5.03,"fcf_margin_pct":3.89,"rd_intensity_pct":0.08},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL","as_of":"TTM ending 2026-05-31（4季加總）"}},{"name":"CLS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":11.95,"operating_margin_pct":8.85,"fcf_margin_pct":3.33,"rd_intensity_pct":0.99},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"2317.TW"},"financial_history":{"ticker":"2317.TW","currency":"TWD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":6626996750000.0,"revenue_yoy_pct":null,"gross_margin_pct":6.04,"operating_margin_pct":2.62,"net_income":141482714000.0,"diluted_eps":10.06,"free_cash_flow":8048616000.0,"fcf_margin_pct":0.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":6162221359000.0,"revenue_yoy_pct":-7.01,"gross_margin_pct":6.3,"operating_margin_pct":2.7,"net_income":142098208000.0,"diluted_eps":10.07,"free_cash_flow":326602147000.0,"fcf_margin_pct":5.3,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":6859615493000.0,"revenue_yoy_pct":11.32,"gross_margin_pct":6.25,"operating_margin_pct":2.92,"net_income":152705066000.0,"diluted_eps":10.79,"free_cash_flow":21987450000.0,"fcf_margin_pct":0.32,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":8103104763000.0,"revenue_yoy_pct":18.13,"gross_margin_pct":6.15,"operating_margin_pct":3.2,"net_income":189353852000.0,"diluted_eps":13.4,"free_cash_flow":51339512000.0,"fcf_margin_pct":0.63,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/2317.TW/2317.TW_Q1_2020_Earnings_Call_20200515.md）

# Q1 2020 Earnings Call
2020-05-15

Q1 2020 Earnings Call
Hon Hai Precision Industry Co., Ltd. | Earnings Calls | 2020-05-15
Operator (Operator)
Ladies and gentlemen, thank you for your patience, and welcome to the Hon Hai 2020 First Quarter
Investor Conference Call. The presenters for today's conference are the Chairman Yang-Wei; the CFO,
David Huang; and IR Director, Alex Yang. [Operator Instructions]
I will now hand the conference over to Mr. Alex Yang, the IR Director. And Mr. Yang, please go ahead.
Alex Yang (Executives)
Good morning and good afternoon, ladies and gentlemen. Welcome to the Hon Hai Precision Industry
2020 First Quarter Financial Results Conference Call. This is Alex Yang, Hon Hai IR Director. We have
posted the presentation file of today's call on the Hon Hai corporate website, www.foxconn.com. Please
download them as your reference.
Before we start the call, I would like to remind you of the safe harbor notice on the second page. Hon
Hai Chairman, Yang Liu; and the CFO, David Huang, will present on today's call. On the third page,
there will be 4 sections of the presentation today, including first quarter financial results, second
quarter business outlook and a recap of recent major statements. After that, we will open up for
questions.
Now I will pass this to the CFO, David Huang.
Teh-Tsai Huang (Executives)
Good morning and afternoon, everyone. I'm David Huang, Chief Financial Officer of Hon Hai. I would
like to first direct you to Page 5 of today's briefing. According to past conventions, we will first
introduce several important company valued subsidiaries of Hon Hai Precision group as a percentage
of Hon Hai's overall consolidated revenue. Please see next page.
In the income statement, revenue for the first quarter was TWD 929.1 billion. After the outbreak in late
January of this year, a lot of the total working hours of the group fell by more than 20% compared with
the same period last year. With the concerted efforts of all employees, final revenue declined by only
12% compared with the same period last year.
Secondly, due to the decrease in revenue, the increase in the proportion of fixed cost amortization,
changes in product mix and increase in pandemic protection and prevention cost, gross profit
decreased by TWD 16.5 billion, a 28% decline from the same period last year and the gross profit
margin was 4.5%.
Third, EBITDA and prevention cost was estimated over TWD 10 billion due to COVID-19. As Chairman
Yang Liu mentioned on March 3 in the last investor conference, our company has requested our clients
and the local governments to share the costs together, thus, most of which will take effect afterwards.
Therefore without taking the epidemic into consideration, our operating profit would have been better
than the same period last year.

The operating profit for the first quarter was TWD 4.5 billion, which decreased by TWD 11.6 billion
compared to the same period last year. In this severe time, despite the increase in epidemic prevention
costs, Hon Hai is committed to controlling operating expenses. Therefore, operating expenses in the
first quarter has decreased by TWD 4.9 billion compared with last year for an operating profit margin
of 0.49%.
As for nonoperating income and expenses, due to high volatility in the financial markets during Q1 and
TWD 7.4 billion decrease on valuation of investment securities, a TWD 3.1 billion decrease on
investment income recognized under equity method compared with the same period last year. In
addition, net currency exchange loss in the first quarter has a little impact compared with the same
period last year. Based on above, Q1 net profit margin was 0.22% and the EPS was TWD 0.15.
Turning to the balance sheet on Page 7. The most obvious change in Hon Hai's balance sheet in the
fourth quarter was a year-on-year increase in cash by 14% and the net cash increased by 37%. At the
same time, due to proper inventory control, the cash cycle was reduced by 2 days compared with the
same period last year. With a high degree of uncertainty in the overall environment, Hon Hai is able to
maintain strategic responsibility by retaining a sufficient cash.
Please continue to the cash flow statement on the next page. Our cash inflow from operating activities
continued to increase and the capital expenditures continued to decrease. Free cash flow in the first
quarter reached TWD 117.4 billion from TWD 108.5 billion, a TWD 8.9 billion increase compared with
the same period last year.
Please continue to the next page. After review of Hon Hai first quarter financial statements, let's review
the performance of the 3 major consolidated subsidiaries in the first quarter. FI Q1 revenue was flat
year-on-year. Profit declined by 35% year-on-year. FIH Q1 revenues declined by 41% year-on-year. The
loss continued to converge year-on-year. FIT Q1 revenue declined by 7% year-on-year. Profit declined
by 94% year-on-year.
Looking back on revenue guidance we provided during the March 3 investor conference, at the same
time, we predict that managed mainline production would resume at the end of March, but in fact, we
achieved this goal ahead of expectations. Therefore, the outlook for the 4 product categories missed
expectations quarter-on-quarter. As for the year-to-year comparison, we are better than originally
expected.
Next, Hon Hai Chairman, Yang Liu, will present our outlook for the second quarter.
Yang-Wei Liu (Executives)
Thank you, David. Good morning and afternoon, everyone. I'm Yang Liu, Chairman of Hon Hai. I'll
now present to you our outlook for the second quarter of this year.
We estimate that the Q2 revenue should grow by over 15% compared with the first quarter. Compared
with the same period last year, it is estimated that there will be a single-digit decline. Overall, due to the
rapid spread of the epidemic, many countries have implemented restrictions, coupled with high
unemployment rates which has impacted consumer demand significantly. However, remote working,
online entertainment and new lifestyles have given us some new growth drivers.
From the perspective of the 4 major product categories, consumer products will have a single-digit Q-o-
Q decline or an over 15% decline Y-o-Y. But as for the rest of the 3 product categories, we show growth
trend for both Q-o-Q and Y-o-Y.

Since the onset of the epidemic, both enterprises and governments have implemented policies such as
work-from-home and learn-from-home, further driving the demand for home office and online
education. Therefore, enterprise products will grow more than 15% Q-o-Q and more than 10% Y-o-Y.
Computing products will also benefit from the increase in demand for home office and online
entertainment. Q2 Q-o-Q and Y-o-Y growth will exceed 15%.
Finally, in the Components & Other Product category, due to the increase in shipments of optical lens
modules, there will be more than 15% growth on quarter-to-quarter in Q2 and more than 10% growth
Y-o-Y.
Next, I would like to review with you the progress of several important investments from our last
investor conference today. First of all, our strategy of new products is not affected by COVID-19
pandemic. Hon Hai, with Yulong and HAITEC, officially signed a joint venture agreement on March 6.
Subsequent preparations for the new joint venture company as well as the R&D projects will proceed as
planned.
Secondly, we mentioned our responsibility as a green energy supplier at our investment conference last
June. Therefore, we invested in Shandong Chengshang Energy in April to strengthen our efforts on
clean energy. At present, our solar power has accumulated a total of 253 megawatts. In the next 2 years,
we expect to generate an additional 210 megawatts. This is all a part of our commitment on
environmental sustainability efforts.
Third, following Hon Hai Group's Foxconn 3.0 strategy. Each subsidiary also has its own plan in their
respective areas of expertise. FIH announced the capital increase in its subsidiary, Mobile Drive
Technology Co. on April 29, for the extension of its in-circuit infotainment and connected system,
including hardware, software and service platform.
Please see the following page. Finally, I further update the impact of the epidemic. At the end of
January, upon the outbreak of COVID-19, I issued the highest principle at our internal epidemic
prevention meeting. That is, first, the employee safety is the highest priority. Second, the operation of
the plant must be legal and compliant with all regulations. As for each individual factories, all major
factories in Mainland China have resumed normal operations. For India, the Indian government
announced restriction will be gradually lifted beginning May 17, and company will apply for resumption
of operations in accordance with local government regulations. Production in most of our Mexico
factories are classified as essential goods for people's livelihood, thus remain in operation. The Vietnam
factory is still operating as normal. Northeast Asia, Southeast Asia, Europe and North America are all
under normal operations. A small number of offices are working from home in response to government
regulations.
Above is all my presentation for today. Thank you for listening.
Alex Yang (Executives)
Operator, now we start to taking questions.
Operator (Operator)
[Operator Instructions] And our first question is coming from Gokul Hariharan of JPMorgan.
Gokul Hariharan (Analysts)

My first question is regarding supply chain changes and relocation. Are we seeing more activity from
your customers in terms of looking to diversify the supply chain a little bit more away from China?
Obviously, last year, we talked about trade war being a risk and being -- prepare for that. But now I
think some of the companies are even talking about diversification because of resiliency reasons. Are
we seeing an accelerated move?
And added question to that is, if we are seeing that kind of a move during this period, do we think that
Hon Hai CapEx is likely to be higher? Or are we still going to be able to manage with a similar kind of
CapEx?
And lastly, given this year, revenue outlook seems to be less certain, do we think that the 2020 CapEx
could be lower than 2019 CapEx?
Yang-Wei Liu (Executives)
In terms of the relocation, I think before the epidemic starts, we actually started the -- some of the
relocation, okay, based on the customers' demand. So after the break -- outbreak of the epidemic, we
don't see any specific requests of our customers for us to expedite the relocation. But no matter how the
political situation changes, Hon Hai will always focus on customers' needs first, okay? Well, that will be
the answer for your first question.
Okay, so the second question is about the CapEx. The CapEx, we don't see too big a change because the
relocation doesn't really happen after the epidemic, okay?
Gokul Hariharan (Analysts)
Okay, okay. Understood. Second question on margins. How should we think about margins in Q2 as
well as how should we think about second half once we are largely over this issue? Do we get back to
that 1% gross margin expansion sales target in second half of this year or do we have to wait for next
year for that to start kicking in?
Yang-Wei Liu (Executives)
Yes, we believe that Q2 gross margin, operating margin will return back to the previous levels of the
same period last year. Now due to the fourth quarter, we have some special situation, as our CFO
mentioned. Only about -- we have lost about 20% of our manpower -- manhours, okay? So margin-
wise, we would think Q2 will return to its previous level. But in terms of Q3 and Q4, so far, it's still
unclear for us what is going to happen.
Gokul Hariharan (Analysts)
Okay. Do you feel that -- do you feel more pricing power -- or pricing pressure from customers, given
that demand is a little bit weaker now compared to previously? Should we expect then that could push
back some of this margin expansion that we were expecting previously?
Yang-Wei Liu (Executives)
Yes, we don't see any pricing pressure at the moment. I think the pressure is on how we deliver the
product on time, so far.
Operator (Operator)

Next, we'll have Rob Cheng of Bank of America Securities for questions.
Robert Cheng (Analysts)
Okay. Chairman Liu, this is Rob. Yes, All I'm asking is a question that is probably more on the virus
impact. I think the whole world is changed as the virus [indiscernible]. I guess from your point of view,
because you guys are probably biggest EMS company, and at the same time, you probably see how the
consumer, their behavior is almost change, even in the political environment or even in the business
environment. I don't know, from your point of view, like, will you start doing some kind of strategy
change on your business plan or some adjustment after the virus? I mean, this is probably more long-
term strategy kind of question.
Yang-Wei Liu (Executives)
I think if you are familiar with our Foxconn 1.0, 2.0 and 3.0 strategy. Our long-term plan has always
been to diversify our business into a new industry. So that has not changed. And will the consumer
behavior change after the epidemic? We believe so, okay, it will change. But to what degree and to what
scale is yet to be seen. Okay?
Robert Cheng (Analysts)
Okay, okay. Understand. Probably another one and a follow up is on probably on the CapEx side.
Because of -- I mean we know Hon Hai has production facility globally. But right now, especially the
biggest [indiscernible] or the biggest production and the final assembly place in Wuxi is in China. I
mean, have you started thinking about, like, for example, building the assembly side, for example, in
U.S.? I mean -- because I know you guys already had some facility before in India, even in Vietnam or
in Europe. But probably not really -- I know in U.S., you guys have some R&D center and the stuff over
there, but mostly it's on small side. I mean, so how is your view on this?
Yang-Wei Liu (Executives)
I think in terms of assembly sites in the U.S. area, in the North American area, we have 3 big
production sites in Mexico. And to do production inside of the U.S., we had to pick the right products to
do, okay? And we already have some products being made over there. It's mostly maybe server-related
products. Due to the situation, the cost consideration in the U.S., only limited number of products can
be made in the U.S. Okay?
Robert Cheng (Analysts)
Okay. So yes, so can we say that the possibility is to have, for example, like a smartphone or the other
consumer products made in the U.S. going forward, can we say -- probably in the coming 2 to 3 years,
can we say here, I mean, very unlikely?
Yang-Wei Liu (Executives)
My personal opinion is that it's going to be difficult for the mobile devices to be produced in the U.S.
because it requires a lot of labor.
Robert Cheng (Analysts)

Yes. Understand. Probably my follow-up question is on margin side. Based on David, the CFO,
mentioned something like a lot of the cost coming out is in first quarter. Can we say it's more like a one-
off costs? And basically, a lot of this kind of additional costs, I mean, going forward, either with
government or clients, some of them that were coming back will pay back. So can we have, for example,
looking at not only normal, probably a sign in upside opportunity for second half? And even for next 2
years -- because I know company has been talking about -- like you mentioned 1.0, 2.0 is kind of long-
term plan. And one of big, I would say, important indicator for us is probably in the operating margin
or gross margins, you guys talking about 10% is kind of a target. I mean I don't know I haven't heard
this kind of hierarchy. Have you see and maintained the same kind of target?
Yang-Wei Liu (Executives)
Okay. For the margin for this year, the first quarter is very special due to the virus, coronavirus. And as
we mentioned in the past that we're getting some help from the local government and our customers,
but the help will not be realized, okay, in Q1. Most of them will be realized in Q2 and Q3, and some of
them will be realized in Q4. So because of that, we think, overall, the margin for the whole year will be
about the same. Okay? So in terms of the 10% margin goal, we still think that's still in our plan, okay?
And we are not changing it.
Operator (Operator)
[Operator Instructions] The next question is coming from Kylie Huang of Daiwa.
Kylie Huang (Analysts)
Chairman Liu and David, this is Kylie from Daiwa. I have a couple of question. The first question I want
to follow up. I just heard about you mentioned about the margin for this year is about 10%. I just want
to clarify, you mean the whole year gross margin is similar to last year?
Yang-Wei Liu (Executives)
That's correct. That's correct.
Kylie Huang (Analysts)
Okay. The second question, actually, I want to check about your progress in Wisconsin. I know -- I just
want to know because COVID-19, do you have any new plan for this site? Or could you give us some
update about when we see the panel will be ramped up later this year? And what kind of product are
you aiming for that site?
Yang-Wei Liu (Executives)
Our investment in Wisconsin is currently proceeding according to the plan, okay? The mix of planned
locally manufactured products continue to grow. Now that includes networking equipment and
network security products and some server products. And in terms of the panel products, that plan has
changed.
Kylie Huang (Analysts)
Okay. So I just want to follow up. So it means in the future, Wisconsin site won't focus on the display
product anymore, but more of like networking enterprise, these kind of products?

Yang-Wei Liu (Executives)
We're in the process of negotiating with the local government. So we will let you know once it is
confirmed. Okay, because the product we are producing at the moment, they are networking-related
and server-related products.
Kylie Huang (Analysts)
Okay. Understood. And from the news I see you guys actually already missed some requirement. So
potentially, we will get a subsidy from the U.S. government is that something potentially will factor in,
in like the second half this year?
Yang-Wei Liu (Executives)
Well, as I mentioned, that we are working with the local government. Okay. And I think due to the
epidemic impact, I think the plan -- the flexibility of the plan is understood by the local government,
but it takes time for us to communicate with the government officials.
Kylie Huang (Analysts)
Okay. Understood. My last question actually is about your cash dividend. I think a lot of long-term
investors really care about that part. We see last year, our cash dividend actually increased to $4.2. For
this year, I understand the situation may be quite challenging because of the overall economy
uncertainty. But I was wondering, this company have some intention of -- in the future, what's your
policy in terms of cash dividend? Will we maintain a certain amount of cash dividend or we want to
maintain a certain percentage of a cash payout ratio?
Yang-Wei Liu (Executives)
As far as now, we're going to stick with our percentage commitment. It's still at least 40% of the net
profit.
Kylie Huang (Analysts)
Okay. So no one speaks percentage rather than absolute dollar payout?
Yang-Wei Liu (Executives)
Yes.
Operator (Operator)
[Operator Instructions] And the next question is coming from Gokul Hariharan of JPMorgan.
Gokul Hariharan (Analysts)
Yes, Chairman Liu. A couple of -- one follow-up to Robert's question. Post the virus outbreak and the
feedback from the customers, et cetera, given the challenges that we have had in terms of the staffing of
the factories initially and then kind of bringing it back on, are you thinking about potential long-term
changes in terms of how assembly as well as other parts of the process is likely to work? Is there any
meaningful changes that you think that could happen in the industry that you could bring about? And
are there any implications from a cost or a customer perspective to that?

My second question is, obviously, there's been a lot of focus on health care-related products, and Hon
Hai group has also pitched in with some of expeditating some of these kind of products. I think you've
talked about digital health among one of the 3 key growth areas. Could we talk about anything that's
changing? I mean you've talked about some of the progress that you've made previously in some of the
medical instruments, et cetera. Are we seeing that accelerate as a result of a bigger focus on some of
these areas? And could we talk about what is the kind of 2- to 3-year plan for that vertical?
And my last question would be, I think there's a lot of press reports about competition and one of your
customers talking about bringing in China competition, et cetera. I think I just wanted to understand
what is Hon Hai's view on the core business? I think, obviously, competition has always been there, but
is this kind of a competition going to be different from the Taiwanese peers you've faced? Or you feel
that it's going to be fairly similar kind of dynamics compared to what you've seen over the last several
years?
Yang-Wei Liu (Executives)
Gokul, you're testing my memory.
Gokul Hariharan (Analysts)
Okay. Sorry, I'll ask one by one then.
Yang-Wei Liu (Executives)
To answer it as I can recall, the first question was about the...
Gokul Hariharan (Analysts)
Any change in the assembly plan or any -- like, long term, do you see that there is going to be change in
how you do things because of this...
Yang-Wei Liu (Executives)
Of course, the lighthouse manufacturing will be the way to go. Okay. We put a lot of efforts in
lighthouse manufacturing, okay, or smart manufacturing, okay? We think that will be the way to go,
okay? And the lighthouse manufacturing will be based on that to build-up our digital transformation
for the whole company. So that's what we are going to do. Okay. And your second question, the new
products that we're going to do?
Gokul Hariharan (Analysts)
Yes. Is on digital health, I think what are the new engagements you have? And how should we think
about it, given there is a lot of focus on the digital health side, obviously, recently?
Yang-Wei Liu (Executives)
Okay. Yes. On a digital health front, we have partnered with a global consulting company on several
projects, such as medical imaging, AI-related products, the DNA sequencing products and some
advanced x-ray equipment. Those are the 3 areas that we are looking -- we're looking into. And we
already have some collaboration with some company in Israel on the new generation of x-ray machines.
We also are working on some MBI equipments for imaging of the breast cancers, okay? Those are the
areas that we have been working on in the digital health area.

Gokul Hariharan (Analysts)
Okay. And my last question was about competition.
Yang-Wei Liu (Executives)
About competition, we always face a lot of potential competitor in the past. And we think these
challenges are always there. We'll leverage our best talents and resources in our existing industry to
provide global manufacturing services to our customers in order to fulfill their needs. But in the long
run, we are into 3 new future industries, as we mentioned in our Foxconn 3.0. That includes EV, digital
health and robotics. That's how we're going to outrun our competitors.
Operator (Operator)
And the next question is coming from Jordan Pong of Franklin Templeton.
Jordan Pong;Franklin Templeton Investments;Analyst (Analysts)
Dear Chairman, just a follow-up question on relocation. And actually, recently, there's an article talking
about your big customer, who asked to shift around 20% of the capacity to India from China. So I just
wonder that would be the -- actually the further request on your group? And what would be the CapEx
yearly incurred going forward? And would that change your pipeline? I understand that you already
have the capacity in India, but I mean under such a new development, would this speed up such
relocation and incur extra cost on the CapEx?
Yang-Wei Liu (Executives)
First of all, I think that's a rumor. I don't know what's going on with that, where the information comes
from. That's my first answer. But in terms of the plan for our specific customers and with their specific
products, I'm not the right person to comment on this -- on other specific customers and products. So
sorry.
Operator (Operator)
[Operator Instructions] And next we'll have Kylie Huang of Daiwa for questions.
Kylie Huang (Analysts)
Chairman Liu, this is Kylie, again. I have a question regarding your progress on the company
transformation for Foxconn 1.0, 2.0 to 3.0. I'm just wondering, because this year, I think a lot of
delivery on margin maybe deteriorate because of virus. But if we take a look about your internal efforts
to fall under Foxconn 1.0 and 2.0, can we expect to see some margin improvement from, let's say, next
year, maybe some, like, 1% to 2% digit point you're talking about?
Yang-Wei Liu (Executives)
We're quite optimistic about the progress of our Foxconn 1.0 and 1.2 projects. In terms of the margin
improvement for this year and next year, we'll do our best. So far, we're not able to predict how big the
impact will be because it's quite complicated due to the virus situation. But we think the progress of
these 2, Foxconn 1.0 and 2.0, we're quite happy about it. And we think it will have some impact, but in
terms of how big, just can't tell at the moment.

Kylie Huang (Analysts)
Okay. May I follow on next part, could I say, because I think originally, we are talking about 10% gross
margin within the 5 years view. I say because this year, we might be impacted by the COVID-19, so it's
more like delay for 1 year. Of course, let's assume the impact from the virus is over next year, so it's
more like a delay in the process. But actually, a lot of effort we're already making, but the overall
progress is actually on track to our original plan.
Yang-Wei Liu (Executives)
Yes, we don't see any change in terms of our 2025 target, okay. Even with the -- with the coronavirus
situation, the progress towards the 2025 is quite promising. That's what we see. The impact of the
pandemic is mostly on our current business. And if you look at the whole year performance, if nothing
goes too wrong in the next second half, our estimate is the margins will go back to what it was a year
ago.
Operator (Operator)
And the next question is coming from Henry Kuai of Orient Securities.
Jian Kuai (Analysts)
Just now you mentioned about the lighthouse is the direction you're going to be. And can you maybe
elaborate more about the program of the lighthouse and digital transformation? And maybe, what is
the impact of the digital transformation or maybe we call the industrial Internet to the top line of the
company?
Yang-Wei Liu (Executives)
Okay in terms of lighthouse project. Our goal was to transform about 10 of our factories into lighthouse
factories this year, we're still working on it, and the progress were still made according to the plan. That
will be the foundation, as I mentioned, for the digital transformation because we are a manufacturing
company, our -- the digital transformation will help to improve our factories. Unlike a lot of different
kind of industries, companies in different type of industries, when they do digital transformation, they
mean something else. But for us, as a manufacturing company, factories will be the foundation of the
company. So the majority of the efforts for our digital transformation will be to transform our factories
to a digital -- digitized factory. That is, from our point of view, lighthouse factories will be the target for
us.
And with the lighthouse production, lighthouse factories, the intention of that is to increase of --
increase our efficiency, the OEE. So with that, we think it will increase our bottom line, not the top line,
okay? The top line increase will be for the new business and the new industry. Okay? That's how we
look at it.
Jian Kuai (Analysts)
Okay. Got it. Because some of our factories are very huge and some are relatively small, may we know
roughly in terms of revenue or maybe manpower, how big are these 10 factories this year?
Yang-Wei Liu (Executives)

Our factory, the physical size of the factory is mostly about 160-meter times 60 meter. So it's about a
10,000 square meters with about 4 stories. That's our typical factories, typical size of the factories. Ten
factories that we're going to turn them into the lighthouse will be something in that size. Okay? And it
depends on the kind of production that they're doing. It could be, we call, the Level 5, Level 6 or Level
10. With Level 10, you -- in that kind of factories, it will go as much as like 4,000 to 5,000 people at the
moment. For Level 6, it's around 1,000 -- 1,000 to 2,000. For Level 5, it's lower than maybe about
1,000. So with lighthouse factories, we will turn that into hundreds for Level 5 and Level 6. For the
Level 10 final system assemblies, the reduction of the labor could be less. Less, by that I mean, maybe
30% less of its original labor.
Operator (Operator)
[Operator Instructions] And the next question is coming from Jordan Pong of Franklin Templeton.
Jordan Pong;Franklin Templeton Investments;Analyst (Analysts)
Dear Chairman, actually, another question is regarding your major customer. Do you think that there's
any chance that the new product would be delayed in terms of the product launch in the second half
this year? And when you are saying that if anything will go to normal in the second half of this year,
then the margin or everything will go to normal level. Would that assume that this kind of new products
would be launched on time?
Yang-Wei Liu (Executives)
Jordan, sorry, I cannot comment on any specific customer product or factory stuff related to our
specific customers.
Operator (Operator)
And the next question is coming from Robert Cheng of Bank of America Securities.
Robert Cheng (Analysts)
Chairman, yes. This is Robert Cheng, again. Because of -- I know you talked about big labor decreasing
on the lighthouse and -- but I have one of your -- I mean your peers in China been keep talking about
SiP, system-in-a-package. Basically, a lot of things become more and more small and -- I mean, need to
put a rather small component and into a small package because probably this is also one of the other
way to -- in terms of decreasing labor, increasing automation efficiency. I don't know do you -- I mean -
- because of -- I think probably from the angle that you're talking about, like, from the Level 5, Level 6,
it's probably more from mechanical. But from the SiP point of view, somewhere, I think on more
semiconductor and probably also from SMT side, I don't know, because you have experience in both
semi and in EMS, so I want to get the U.S. dollar on it.
Yang-Wei Liu (Executives)
I think the advanced packaging capabilities definitely will change the way we produce our products, not
only SiP package but also advanced 3D or the panel packaging. This -- I think this is the trend, but it
will not change the system-level product, okay?
So in terms of the -- for the system-level production, that may be, I would say the function or the way to
do the system-level products will be about the same. The impact maybe for the -- is on the Level 6.

Okay? The Level 6 may transform into a combination of SiP and the SMT. That's what we see. Okay?
Because some of the components will be in a bigger package will be further integrated into the new
packaging technology, but that package will still be assembled onto the board with typical SMT process.
So SMT will still be there.
Robert Cheng (Analysts)
Yes. So especially is -- from the SMT and some of the packaging technology, can we say this is actually
more in the component, especially in other semi, in other component level to put together. Probably, I
also want to know about what is the -- I mean...
Yang-Wei Liu (Executives)
Hello, are you there?
Robert Cheng (Analysts)
Sorry, yes. Sorry, because of phone coming. I also want to know how the Hon Hai's progress in SiP and
over advanced packaging in this area.
Yang-Wei Liu (Executives)
Yes. We already have the SiP capability right now. We have a company by the name of SST, I think.
They are already capable of doing some SiP products. So SiP is not new to Foxconn.
In terms of advanced packaging, we -- if you remember that we have some activity in Qingdao that we
are going to build some advanced packaging capability in Qingdao. And we will be targeted to have that
kind of packaging products in a couple of years in 2021 -- approximately 2021 -- at the end of 2021 to
2022.
Alex Yang (Executives)
Well, ladies and gentlemen, our time is up. So thank you all today for attending the call, and we will
conclude the call now. Thank you.
Operator (Operator)
Yes. Thank you, Chairman Liu. And ladies and gentlemen, this concludes today's conference call. We
thank you for your participation. You may now disconnect. Goodbye.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 2317.TW_Special_Call_Stellantis_N_V_20210518.md
- 2021-05-18｜Yves Bonnefont｜capital_allocation：Foxconn 與 Stellantis 合資公司採 50-50 表決權，雙方各投入最佳 IP（原話："The JV will be a 50-50 voting rights company"）
- 2021-05-18｜Yang-Wei Liu｜capital_allocation：Foxconn 及其子公司 FIH 先與 Stellantis 合作開發資訊娛樂軟硬體（原話："Foxconn and our subsidiary company, FIH, will initially work"）
- 2021-05-18｜Carlos Tavares｜commitment：Tavares 表示本合資是長期策略計畫的一塊，完整計畫年底發表（原話："we will present to you by the end of this year."）
- 2021-05-18｜Yang-Wei Liu｜customer：Mobile Drive 不獨家供應 Stellantis，也將供應其他公司（原話："Mobile Drive will not be exclusive to Stellantis."）
- 2021-05-18｜Yves Bonnefont｜competition：合資公司須與其他供應商以公平交易條件競爭 Stellantis 的業務（原話："It also has to compete for Stellantis' business"）
- 2021-05-18｜Yves Bonnefont｜product：合資公司承接約 250 名已組好的軟體工程師（原話："software engineers preassembled, organized."）
- 2021-05-18｜Yves Bonnefont｜customer：Stellantis 稱全球有 1,200 萬輛活躍連網車（原話："Today, Stellantis has 12 million active connected vehicles"）
- 2021-05-18｜Yves Bonnefont｜product：軟體策略目標之一：打造持續更新的車與服務（原話："we want this strategy to create forever up-to-date vehicle"）
- 2021-05-18｜Yves Bonnefont｜margin：永遠最新策略伴隨新商業模式與變現方式（原話："a new business model, a new monetization approach"）
- 2021-05-18｜Yves Bonnefont｜margin：被問收入分成時，稱分成方式依地區而定，JV 角色為技術提供者（原話："the way we will work on the revenue will also depend"）
- 2021-05-18｜Calvin Chih｜commitment：Calvin 稱執行重點為速度、品質與具競爭力成本（原話："execute with speed, quality and competitive cost."）
- 2021-05-18｜Calvin Chih｜margin：Calvin 稱個人化與區域服務是無縫體驗與經常性收入的關鍵（原話："experience and the recurring revenue generation."）
- 2021-05-18｜Yves Bonnefont｜customer：Stellantis 車款價格帶涵蓋 1.5 萬至 15 萬歐元，座艙需可擴充（原話："vehicles ranging from EUR 15,000, up to EUR 150,000."）
- 2021-05-18｜Yves Bonnefont｜customer：JV 技術預計服務 Stellantis 全產品組合而非單一品牌（原話："serve the full portfolio of Stellantis and not specifically"）
- 2021-05-18｜Yves Bonnefont｜product：JV 將開發應用層與部分座艙中介層（原話："layer as well as some of the cockpit middleware."）
- 2021-05-18｜Yves Bonnefont｜product：JV 初期聚焦座艙與連網服務（原話："the JV is in the first stage extremely focused on cockpit"）
- 2021-05-18｜Calvin Chih｜competition：Calvin 區分 Mobile Drive 與 MIH：前者逐車開發，非平台概念（原話："It's not a platform concept."）
- 2021-05-18｜Calvin Chih｜competition：Calvin 回應 Tesla／VW 自研：多數現行車款使用多供應商，整合耗時（原話："cars selling today are using multiple suppliers."）
- 2021-05-18｜Calvin Chih｜product：工程師執行主要在亞洲（台北），歐洲設需求與專案管理據點（原話："execution, the engineer in Asia, particularly in Taipei."）
- 2021-05-18｜Yves Bonnefont｜product：不阻止用戶使用 Android Auto／CarPlay 投影模式（原話："prevent people who prefer projected mode from using"）
- 2021-05-18｜Calvin Chih｜risk：Calvin 表示網路安全將是主要重點（原話："Cybersecurity will also be our primary focus."）
- 2021-05-18｜Carlos Tavares｜commitment：Tavares 稱此破壞式轉型對 Stellantis 長期策略是必要（原話："We believe that this disruption is a must for Stellantis."）
- 2021-05-18｜Calvin Chih｜guidance：Mobile Drive 無市占目標，稱剛成立（原話："No, we don't have that yet."）

### 2317.TW_Special_Call_Hon_Hai_Precision_Industry_Co_Ltd_20241008.md
- 2024-10-08｜Yang-Wei Liu｜commitment：董事長稱鴻海將是首批出貨 GB200 相關超級晶片的廠商。（原話："Foxconn will be the first to ship these super chips."）
- 2024-10-08｜Yang-Wei Liu｜customer：董事長轉述客戶要求更多自動化。（原話："Our customers told us they want to see more automation."）
- 2024-10-08｜Benjamin Ting｜product：Ting 稱正在興建全球最大的 GB200 生產設施。（原話："the largest GB200 production facility on the planet."）
- 2024-10-08｜Benjamin Ting｜customer：Ting 提到大家都在要 Blackwell。（原話："asking for Blackwell, so it's hard"）
- 2024-10-08｜Benjamin Ting｜commitment：Ting 表示已承諾建成後為台灣最強超級電腦（自建 Blackwell 資料中心）。（原話："So we have committed, when it is done, it is going to be"）
- 2024-10-08｜Benjamin Ting｜capital_allocation：Ting 重申董事長宣布要自建 Blackwell 超算資料中心。（原話："our own Blackwell supercomputing data center."）
- 2024-10-08｜Annemarie Grosse Frie｜product：Siemens 稱與鴻海合作產線的週期時間與產出變化數字。（原話："reduced by 25%, while throughput has increased by 20%."）
- 2024-10-08｜Jeff Walters｜product：BCG 稱鴻海營運逾一萬台射出成形機，為 Genesis 平台用例。（原話："Foxconn operates over 10,000 injection molding machines"）
- 2024-10-08｜Jesse Chao｜product：Foxconn 低軌衛星：前一年發射兩顆 Pearl CubeSats。（原話："launching our 2 Pearl CubeSats into low-earth orbit."）
- 2024-10-08｜Jerry Hsiao｜capital_allocation：Hsiao 稱鴻海已投入逾 100 億美元（原文接 3+3 策略下的永續脈絡）。（原話："Foxconn has invested over USD 10 billion"）
- 2024-10-08｜Jun Seki｜product：Seki 說明 EV 策略加入設計服務 CDMS。（原話："That is the CDMS; D for Design."）
- 2024-10-08｜Jun Seki｜capital_allocation：Seki 稱與 ZF 合資公司於 5 月 1 日成立。（原話："Actually, we did. As you see, May 1st, we newly established"）
- 2024-10-08｜Eike Dorff｜guidance：ZF Foxconn 合資 CEO 稱營收目標由 40 億歐元增至 80 億歐元，不含鴻海車款機會。（原話："from EUR 4 billion to EUR 8 billion over the next years."）
- 2024-10-08｜Andy Lee｜customer：Foxtron CEO 稱 Model C 在台灣成為暢銷電動車之一。（原話："one of the best-selling electric car in Taiwan."）
- 2024-10-08｜Andy Lee｜product：Model C 美國版預計 2025 年底上市。（原話："launching at the end of 2025."）
- 2024-10-08｜Emma Lee｜product：Model U 迷你巴士最大續航 275 公里。（原話："offers a maximum range of 275 kilometers"）
- 2024-10-08｜Tais Chuu｜product：Model D 充電 10 分鐘可增加 350 公里。（原話："350 kilometers in just 10 minutes"）
- 2024-10-08｜Tais Chuu｜product：Foxtron 定位為 EV 平台供應商。（原話："we are an EV platform provider first."）

### 問答異常語氣（迴避／改口／保留）
- 2317.TW_Special_Call_Stellantis_N_V_20210518.md｜問：Briana Noble：Stellantis 客戶何時開始受惠？｜答法：稱無法揭露首款座艙日期，改談已有明確專案、品牌之後再宣布
- 2317.TW_Special_Call_Stellantis_N_V_20210518.md｜問：José Asumendi：軟體更新收入如何分成？｜答法：未給分成比例，改稱依地區而定、JV 是技術提供者
- 2317.TW_Special_Call_Stellantis_N_V_20210518.md｜問：Lauly Lee：Mobile Drive 是否有市占目標與時程？｜答法：未給目標，稱剛成立尚無

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

## ⑥ 條件附卡（archetype_hint='EMS/ODM' 命中）：judge_addendum_cyclical.md

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
{"date":"20260601","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 伺服器需求結構性向上，鴻海維持 ~40% 機櫃市占並隨 GB300/Rubin/ASIC 放量","columns":{"2Y 驗證點":"2026 機櫃出貨翻倍兌現；雲端網通段佔比 ≥ 48%","5Y 驗證點":"AI 伺服器佔集團營收 ≥ 55%，市占維持 ≥ 35%","10Y 驗證點":"AI infra 進入更新週期，鴻海仍為前二大 ODM","具體數字門檻":"2026 AI 機櫃出貨 YoY ≥ +80%；JPM 估 AI server 營收 +63%","來源":"公司法說（5/14）/ JPMorgan / DIGITIMES","漂移觸發":"連 2 季 AI 機櫃出貨 TTM 偏離指引 ≥ 10% → 削弱"}},{"id":"H2","text":"成長轉化為 EPS：mix 向 AI/系統整合傾斜 + 寄售改善現金轉換，毛利美元與 EPS 同步成長","columns":{"2Y 驗證點":"2026E EPS 17.58（+31%）兌現；雲端網通段 OPM 不被稀釋","5Y 驗證點":"集團 OPM 由 3.2% 升向 4%+；FCF/NI 回升 ≥ 0.4","10Y 驗證點":"EPS 維持雙位數 CAGR，現金轉換結構性改善","具體數字門檻":"FY26 EPS ≥ 17；雲端網通段 OPM YoY 持平或升","來源":"yfinance/Refinitiv 共識；公司寄售指引","漂移觸發":"連 2 季 TTM EPS 偏離共識 ≥ 10% → 削弱"}},{"id":"H3","text":"估值維持「AI 系統整合商」再評價，PE 不回落至 pre-AI 組裝廠倍數","columns":{"2Y 驗證點":"Fwd PE 維持 ≥ 12x（FY+2）","5Y 驗證點":"PE 區間穩定於 12–16x（非回到 8–11x）","10Y 驗證點":"市場長期認可系統整合溢價","具體數字門檻":"FY+2 PE 不破 11x（pre-AI 中樞）","來源":"歷史 PE 河流圖（Goodinfo / statementdog）","漂移觸發":"連 4 季 TTM PE 中樞下移破 11x → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI 伺服器組裝商品化 / 價格戰，毛利美元被壓","columns":{"對應假設":"H1/H2","時間尺度":"🔥 中期（4–6 季）","監測指標":"雲端網通段 OPM；GB 機櫃 ASP 趨勢","警戒閾值":"該段 OPM 連 2 季 YoY −0.5pp"}},{"id":"R2","text":"FCF 轉換持續落後（高營運資金 + capex +30%），現金流陷阱","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1–2 季可現）","監測指標":"FCF/NI（TTM）；寄售佔伺服器營收比","警戒閾值":"FCF/NI 連 2 季 TTM &lt; 0.3 且寄售佔比未升"}},{"id":"R3","text":"AI 資本支出週期見頂 + 客戶內部化/在地化稀釋台廠紅利","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"hyperscaler capex 指引；客戶自製/白牌比例","警戒閾值":"Top 4 hyperscaler capex YoY 連 3 季 &lt; +10%（≥ 50% 機率才砍倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":289.0,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2317.TW_20261020/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
