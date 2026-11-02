你是 stock-analyst **v20 判斷 agent**，標的 H（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"H","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/H_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/H_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_total_revenues","label":"營收（GAAP total revenues）","value":1743,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）"}},{"id":"f_kpi1_adjusted_ebitda_recast","label":"Adjusted EBITDA（recast 口徑）","value":295,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）"}},{"id":"f_kpi2_gross_fees","label":"總費用收入 Gross fees","value":327,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）"}},{"id":"f_kpi3_gaap_hyatt","label":"GAAP 淨利（歸屬 Hyatt）","value":58,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）"}},{"id":"f_kpi5_comparable_system_wide_r","label":"Comparable system-wide RevPAR 成長","value":7.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）"}},{"id":"f_kpi6_pipeline","label":"淨客房成長與 pipeline","value":158000,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"間（pipeline）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）"}},{"id":"f_kpi7_fy2026","label":"管理層指引 FY2026","value":null,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）"},"needs_sonnet":true},{"id":"f_kpi8","label":"資本回饋","value":147,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"US$M（Q3 買回）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_h_gross_margin_pct","label":"H 毛利率","value":20.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.H.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_h_operating_margin_pct","label":"H 營業利益率","value":7.21,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.H.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_h_fcf_margin_pct","label":"H FCF 利潤率","value":6.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.H.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mar_gross_margin_pct","label":"MAR 毛利率","value":19.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mar_operating_margin_pct","label":"MAR 營業利益率","value":15.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mar_fcf_margin_pct","label":"MAR FCF 利潤率","value":11.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hlt_gross_margin_pct","label":"HLT 毛利率","value":30.13,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hlt_operating_margin_pct","label":"HLT 營業利益率","value":24.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hlt_fcf_margin_pct","label":"HLT FCF 利潤率","value":14.49,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_chh_gross_margin_pct","label":"CHH 毛利率","value":50.59,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHH.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_chh_operating_margin_pct","label":"CHH 營業利益率","value":25.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHH.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_chh_fcf_margin_pct","label":"CHH FCF 利潤率","value":7.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHH.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wh_operating_margin_pct","label":"WH 營業利益率","value":36.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wh_fcf_margin_pct","label":"WH FCF 利潤率","value":30.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc","label":"SBC（占營收）","value":0.63,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":187.89,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":18.28,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":70.01,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":6.13,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.59 → 3.81）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.82,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.86 → 4.9）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.5,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.06 → 6.09）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.81,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":4.9,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":6.09,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.67,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 3.64 → 3.81（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":97.86,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.67,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":49.31,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 3.81，分子＝快照價 187.89","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.319,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":4153.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 4648.0、現金 495.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":93.39,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":21700.06,"period":"2026-11-03","unit":"USD m","basis":"市值 17547.06 ＋ 淨負債 4153.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":7143.17,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":7722.09,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.04,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 186.55 / W52 168.63 / W104 154.53 / W250 130.94 / W250 13週斜率 1.06%"},{"id":"f_ma_w52","label":"52 週均線","value":168.63,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":154.53,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":130.94,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.06,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出的競爭來源包含新分銷管道（潛在 AI 平台）、Alibaba、Google、信用卡發行商及 Airbnb/Vrbo 等短租，並指出部分對手規模與會員數大於 Hyatt。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"We also compete against smaller hotel chains and independent and local owners and operators and face competition from new distribution channels in the travel industry, including potential AI platforms.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素提及產業整併，若競爭對手整併可能使 Hyatt 失去份額或難以吸引業主與加盟商。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"If we lose market share or are not able to successfully attract third-party owners and franchisees to our brands as a result of this consolidation, our results of operations, cash flow, business, and overall financial condition could be materially adversely affected.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Hyatt 管理層稱 Q2 2026 全組合獲取份額，luxury 與 lifestyle 上半年 RevPAR index 提升近三點。","source":"Hyatt Q2 2026 earnings call (equibles)","url":"https://equibles.com/stocks/h/calls/2026-q2","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Hyatt 10-K FY2025 states no single customer is material to its business; customers are diversified corporate, association, specialty, travel agency and individual consumer accounts.","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"No single customer is material to our business.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"CoStar/Tourism Economics 2026年8月預測：美國飯店 2027 RevPAR 約 +2.1%（2026 為 +4.4%），供給成長約 0.6%，STR 稱在建量為 12 年來最低。","source":"CoStar/Hospitalitynet U.S. Hotel Forecast Assumptions – August 2026","url":"https://www.hospitalitynet.org/news/4133888/us-hotel-forecast-assumptions-august-2026","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Lodging Econometrics Q3 2026 報告：美國 2027 供給成長預估 1.3%（668 間、72,667 房），2026 為 1.2%；在建專案較去年同期減 4.9%。","source":"Lodging Econometrics via Hotel Dive Q3 2026 pipeline","url":"https://www.hoteldive.com/news/hotel-construction-pipeline-q3-2026/872849/","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Hyatt Q3 2026 將全年系統 RevPAR 成長上修至 5%-5.5%（美國 5%-6%）；管理層稱世足賽與猶太節日時點不會重複；All-inclusive 淨套餐 RevPAR -2.5%，中東 -3%；淨房數成長降至 3.9%。","source":"Hyatt Q3 2026 earnings call (MarketBeat transcript highlights)","url":"https://www.marketbeat.com/instant-alerts/transcript-hyatt-hotels-q3-earnings-call-highlights-2026-10-30/","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Colliers 2026 展望引 Green Street：2026 美國前 50 市場住宿需求成長 1.3%，低於 2006-2019 年均 2%。","source":"Colliers 2026 U.S. Hospitality Outlook via Hotel Management","url":"https://www.hotelmanagement.net/construction/le-predicts-14-us-hotel-supply-growth-2026","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：公司稱各項訴訟與程序的最終結果預期對合併財務狀況、經營成果或流動性不致有重大影響；未列出反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"We currently believe that the ultimate outcome of such lawsuits and proceedings will not, individually or in the aggregate, have a material effect on our consolidated financial position, results of operations, or liquidity.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"加盟業務受 FTC 規範及各州／各國加盟關係法約束；違規可能導致罰款與民事判決（產業特定監管框架，屬既有風險揭露）。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"Our franchising business is subject to various laws, as well as to regulations enacted by the Federal Trade Commission (\"FTC\"). The FTC also regulates the manner and substance of our disclosures to prospective franchisees.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Hyatt 與 Hilton 等被控透過 IDeaS 收益軟體交換價格資訊的民事反托拉斯集體訴訟，法院先行駁回（私人訴訟，非政府調查）。","source":"Law360 Hyatt, Hilton Beat Room Price-Fixing Antitrust Suit, For Now","url":"https://www.law360.com/articles/2366842","excerpt":"Hyatt, Hilton Beat Room Price-Fixing Antitrust Suit, For Now","as_of":"2025-07-18","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Hyatt 10-K 風險因素列出國際營運風險包括進出口許可要求與未預期的法規變動，含關稅、禁運、出口管制與其他貿易限制（一般性風險揭露，未量化）","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"import and export licensing requirements and regulations, as well as unforeseen changes in regulatory requirements, including the imposition of tariffs or embargoes, export regulations, controls, and other trade restrictions;","as_of":"2026-02-13","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K 載明營運受 OFAC 與商務部貿易制裁約束，且 2025 年無需依 ITRSHR Act 揭露的活動","source":"SEC EDGAR 10-K FY2025 Item 1 International Operations","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"We did not identify any 2025 activities required to be disclosed.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Skift 報導 2026 年 2 月全球關稅政策急變讓部分飯店營運商及其供應商感到混亂（產業層級，非 Hyatt 專屬）","source":"Skift, Hoteliers Scramble to Price U.S. Tariff Risk","url":"https://skift.com/2026/02/23/hoteliers-scramble-to-price-u-s-tariff-risk/","excerpt":"President Trump announced a 10% global tariff Friday and said Saturday he planned to raise it to 15%. The sudden shifts created confusion among some hotel operators and their suppliers.","as_of":"2026-02-23","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Q2 2026：中東衝突使系統整體 RevPAR 成長少 1.1 個百分點（原為 +5.9%）；CFO 預期中東酒店收入明顯低於去年，全年費用收入約減 $10 百萬","source":"eGlobalTravelMedia / panabee 轉述 Hyatt Q2 2026 業績","url":"https://eglobaltravelmedia.com.au/2026/08/03/hyatts-revpar-climbs-5-9-as-global-room-growth-hits-delays/","excerpt":"We continue to expect hotel revenues in the Middle East to remain significantly below last year, which we estimate will reduce full-year fees by about $10 million","as_of":"2026-08-03","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Hyatt 2026 前瞻聲明列出中東軍事衝突與墨西哥安全問題為影響旅遊的因素，風險因素亦提及貿易政策與關稅","source":"Hyatt Form S-3ASR 2026","url":"https://www.sec.gov/Archives/edgar/data/0001468174/000110465926103248/tm2623937-1_s3asr.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K：核心營運依賴第三方或雲端供應商的 IT 服務，並可能受軟體供應鏈事件影響","source":"Hyatt FY2025 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"Our success depends on the efficient and uninterrupted operation of our information technology systems and technology services delivered to Hyatt by third-party or cloud providers.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 comparable system-wide hotels RevPAR +7.2% YoY; gross fees +15.2% to $327M; 美國 RevPAR +8.2%（含 FIFA 世界盃與猶太節日時點）","source":"Hyatt Q3 2026 earnings release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm","excerpt":"comparable system-wide hotels RevPAR increased 7.2%, compared to the third quarter of 2025","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"全包式度假村（Distribution 段）Net Package RevPAR -2.5%，主因墨西哥需求下滑；颶風 Melissa 關閉牙買加飯店，Distribution 段 Adjusted EBITDA 下滑；預期 Q4 Net Package RevPAR 回正","source":"Hyatt Q3 2026 earnings release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm","excerpt":"Net Package RevPAR decreased 2.5%, compared to the third quarter of 2025, primarily reflecting lower demand for travel to certain destinations in Mexico, partially offset by growth in the Caribbean and Europe.","as_of":"2026-10-29","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Hyatt 將 2026 全年 comparable system-wide RevPAR 成長指引上調至 5%–5.5%（7 月為 3.5%–4.5%，Q1 初始 2%–4%）；美國 RevPAR 預期 +5%–6%","source":"Skift, Hyatt Raises Outlook, but Its All-Inclusives Lag","url":"https://skift.com/2026/10/29/hyatt-raises-outlook-but-its-all-inclusives-lag/","excerpt":"The company raised its full-year forecast for RevPAR, and now expects it to grow 5% to 5.5% in 2026, up from the 3.5% to 4.5% range it gave in July.","as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 美國 RevPAR +8.2%，約 50bp 來自世界盃；管理層歸因於高端旅客韌性；Q2 中東衝突拖累 RevPAR 約 110bp；Q3 中東與非洲 -0.7%","source":"Skift / Pulse2 / trade reports","url":"https://skift.com/2026/10/29/hyatt-raises-outlook-but-its-all-inclusives-lag/","excerpt":"Executives attributed the performance to the resilience of \"premium travelers.\"","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 豪華飯店帶動成長；市占與定價無直接數據，僅有產業『分化』評論（高端優於平價）","source":"Hotel Dive, Hyatt Q3 2026 earnings","url":"https://www.hoteldive.com/news/hyatt-q3-2026-earnings/873205/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Hyatt 10-K 風險因子：生成式 AI 工具與 LLM（ChatGPT、Claude、Gemini 等）決定提供何種資訊的方式，可能使 Hyatt 物業獲得的關注減少；資訊不準確也可能損及品牌聲譽。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"The manner in which these AI tools decide what information to provide in response to a given user query may also result in our properties receiving less attention by users of these tools.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Hyatt 10-K：自家 AI 部分依賴第三方授權 AI 技術，無法控制其可得性與定價；若不相容或不可用，其方案吸引力下降。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"We cannot control the availability or pricing of such third-party AI technologies, especially in a highly competitive environment, and we may be unable to negotiate favorable economic terms with the applicable providers.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"ZentrumHub 報告：預估到 2027 年底，OTA 訂房中 5–8% 可能由 AI 代理完成（廠商新聞稿，產業層面，非 Hyatt 專屬）。","source":"PR Newswire / ZentrumHub 報告","url":"https://tools.prnewswire.com/en-us/live/20813/release/20260617EN84821","excerpt":"New ZentrumHub Report: AI Agents Are Starting to Book Hotel Rooms -- Is the Travel Industry Ready? Free 2026 report based on 1.5 million+ real bookings shows how AI is changing who sells the hotel room.","as_of":"2026-06-17","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 列新分銷通路（含潛在 AI 平台）為競爭風險，並稱自家數位平台是主要分銷通路。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"Our digital platforms are our primary distribution channels providing guests, customers, and members with an efficient source of information about our hotels, distinct brand experiences, and a seamless booking experience.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"10-K 明列新分銷通路（含潛在 AI 平台）可能對業務造成負面影響。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"new distribution channels, including potential AI platforms, alternatives to traditional hotels, and industry consolidation among our competitors may negatively impact our business.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"Distribution 分部 2025 年營收 $946M，較 2024 年 $1,023M 下降 7.5%。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"Distribution revenues (1) $ 946 $ 1,023 $ (77) (7.5) %","as_of":"2026-02-13","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Hyatt 於 Q4 2025 財報電話會議稱已完全轉為輕資產，2026 年輕資產盈餘預計 90%（搜尋摘要轉述）。","source":"Hotel Dive, Hyatt Q4 2025 earnings","url":"https://www.hoteldive.com/news/hyatt-earnings-q4-2025/812093/","excerpt":null,"as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#4","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Hyatt 推 AI 搜尋與管理工具以提高直訂，並對部分 Amex 持卡人提供 $75 直訂優惠（搜尋摘要轉述，未核原文）。","source":"Stockti: Hyatt accelerates AI rollout to boost direct bookings","url":"https://stockti.com/hyatt-accelerates-ai-rollout-to-boost-direct-bookings-amex-offer-targets-loyalty","excerpt":null,"as_of":"2026-03-25","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 共識目標價 $198.29（Moderate Buy，9 Buy／6 Hold）；Tickflow 共識 $194.92（26 位分析師，Buy）；高端約 $221（Mizuho 5/29 由 219 升至 221）。as_of 為 2026 年 7 月底至 8 月初。","source":"MarketBeat / Tickflow（搜尋摘要）","url":"https://www.tickflow.io/stock/H/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Bullstory 列平均目標價 $196.83（24 位分析師），高 $221、低 $165，記錄價 $158.48，資料日 2026-09-27。","source":"Bullstory 預測頁（搜尋摘要）","url":"https://bullstory.io/en/stocks/h/forecast/upside","excerpt":null,"as_of":"2026-09-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司指引逐季上調：2月原指引系統 RevPAR +1.0%~3.0%；Q2（7/30）上調為 +3.5%~4.5%、淨增房數約 6%；Q3（10/29）再上調為 +5.0%~5.5%，Distribution 分部 EBITDA 預期降約 $30M（較前次再降 $5M，墨西哥需求弱）。","source":"Hyatt Q3 2026 earnings release (SEC 8-K) / Pulse2","url":"https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 後多家券商下調目標價（Morgan Stanley、Barclays、Baird、Deutsche Bank，據 StockAnalysis）。","source":"StockAnalysis（搜尋摘要）","url":"https://stockanalysis.com/stocks/H","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 財報上調全年 RevPAR 指引至 5.0%~5.5%","source":"Hyatt Q3 2026 earnings release","url":"https://newsroom.hyatt.com/Q3-2026-Earnings-Results","excerpt":"Franchise and other fees increased 16.8%, driven by non-RevPAR fee contributions, RevPAR growth in the United States, and new hotel openings. Owned and leased segment Adjusted EBITDA declined 1%, compared to the third quarter of 2025, after adjusting for 2025 asset sales. Distribution segment Adjusted EBITDA declined, compared to the third quarter of 2025, primarily due to","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Hyatt 於 2025-12-30 完成出售 Playa 持有飯店與不動產的子公司（Asset Sale），現金對價約 $2.0 billion，Hyatt 另提供 $200 million 優先股投資給買方。","source":"SEC EDGAR 8-K Item 2.01（2025-12-30）","url":"https://www.sec.gov/Archives/edgar/data/1468174/000110465925125229/tm2534420d1_8k.htm","excerpt":"On December 30, 2025, the Asset Sale Transaction closed for an all-cash purchase price of $1,977.5 billion. Buyer financed the acquisition with equity financing from an affiliate of KSL Capital Partners, LLC and Rodina, committed debt financing from third party sources, and a $200 million preferred equity investment provided by Hyatt.","as_of":"2025-12-30","retrieved_at":"20261103","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：公司稱現有訴訟與程序的最終結果預期不會對合併財務狀況、經營成果或流動性造成重大影響。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"We currently believe that the ultimate outcome of such lawsuits and proceedings will not, individually or in the aggregate, have a material effect on our consolidated financial position, results of operations, or liquidity.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 13 份 8-K 中重大項目僅 3 份（2025-11-26 Item 1.01 發債、2025-12-30 Item 2.01 出售、2026-05-28 Item 8.01 回購授權）；無 4.02（重編）或 3.01 項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001468174&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"法國業界媒體報導 Hyatt 完成收購 Two Roads Hospitality（Alila、Destination、Joie de Vivre、Thompson、tommie 五個生活風格品牌）；價格由 $480 million 降至 $405 million。僅單一法文來源，未讀原文。","source":"Tendance Hôtellerie（2026-07-15 頁面）","url":"https://www.tendancehotellerie.fr/articles-breves/communique-de-presse/10625-article/hyatt-finalise-l-acquisition-de-two-roads-hospitality","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Hyatt 於 2025-12-30 完成出售 Playa 持有飯店與不動產的子公司（現金約 $2.0 billion），並提供 $200 million 優先股投資。","source":"SEC EDGAR 8-K Item 2.01（2025-12-30）","url":"https://www.sec.gov/Archives/edgar/data/1468174/000110465925125229/tm2534420d1_8k.htm","excerpt":"On December 30, 2025, the Asset Sale Transaction closed for an all-cash purchase price of $1,977.5 billion. Buyer financed the acquisition with equity financing from an affiliate of KSL Capital Partners, LLC and Rodina, committed debt financing from third party sources, and a $200 million preferred equity investment provided by Hyatt.","as_of":"2025-12-30","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"法國業界媒體報導 Hyatt 完成收購 Two Roads Hospitality，價格由 $480 million 降至 $405 million（單一法文來源，未核原文）。","source":"Tendance Hôtellerie（2026-07-15）","url":"https://www.tendancehotellerie.fr/articles-breves/communique-de-presse/10625-article/hyatt-finalise-l-acquisition-de-two-roads-hospitality","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K Item 3：公司認為現有訴訟最終結果不會對財務狀況、經營成果或流動性造成重大影響；搜尋未見 2025–2026 證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm","excerpt":"We currently believe that the ultimate outcome of such lawsuits and proceedings will not, individually or in the aggregate, have a material effect on our consolidated financial position, results of operations, or liquidity.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 13 份 8-K 中無 Item 4.02（財報不可信賴／重編）項目；重大項目僅 3 份（發債、出售、回購授權）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001468174&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"H","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":20.11,"operating_margin_pct":7.21,"fcf_margin_pct":6.35,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.H","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MAR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.81,"operating_margin_pct":15.73,"fcf_margin_pct":11.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MAR","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HLT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":30.13,"operating_margin_pct":24.01,"fcf_margin_pct":14.49,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HLT","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CHH","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.59,"operating_margin_pct":25.52,"fcf_margin_pct":7.09,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHH","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"WH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":36.38,"fcf_margin_pct":30.57,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WH","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"H"},"financial_history":{"ticker":"H","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":5891000000.0,"revenue_yoy_pct":null,"gross_margin_pct":21.86,"operating_margin_pct":7.25,"net_income":455000000.0,"diluted_eps":4.09,"free_cash_flow":473000000.0,"fcf_margin_pct":8.03,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":6667000000.0,"revenue_yoy_pct":13.17,"gross_margin_pct":19.59,"operating_margin_pct":5.22,"net_income":220000000.0,"diluted_eps":2.05,"free_cash_flow":602000000.0,"fcf_margin_pct":9.03,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":6648000000.0,"revenue_yoy_pct":-0.28,"gross_margin_pct":19.51,"operating_margin_pct":6.27,"net_income":1296000000.0,"diluted_eps":12.65,"free_cash_flow":463000000.0,"fcf_margin_pct":6.96,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":7101000000.0,"revenue_yoy_pct":6.81,"gross_margin_pct":19.73,"operating_margin_pct":6.75,"net_income":-52000000.0,"diluted_eps":-0.55,"free_cash_flow":159000000.0,"fcf_margin_pct":2.24,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/H/H_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Hyatt Hotels Corporation** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good morning, and welcome to Hyatt's Third Quarter 2026 Earnings Conference Call. [Operator Instructions] 
As a reminder, this conference call is being recorded. I would now like to turn the call over to Ryan Nuckols, Vice President of Investor Relations and Corporate Strategy. Please go ahead.

**Ryan Nuckols** (Executives):
Thank you, and welcome to Hyatt's Third Quarter 2026 Earnings Conference Call. Joining me on today's call are Mark Hoplamazian, Hyatt's Chairman, President and Chief Executive Officer; and Joan Bottarini, Hyatt's Chief Financial Officer. Before we start, I would like to remind everyone that our comments today will include forward-looking statements under federal securities laws.
These statements are subject to numerous risks and uncertainties as described in our annual report on Form 10-K, quarterly reports on Form 10-Q and other SEC filings. These risks could cause our actual results to be materially different from those expressed in or implied by our comments. Forward-looking statements in the earnings release that we issued today, along with the comments on this call, are made only as of today and will not be updated as actual events unfold.
In addition, you can find a reconciliation of non-GAAP financial measures referred to in today's remarks under the financials section of our Investor Relations website and in this morning's earnings release. An archive of this call will be available on our website for 90 days. Additionally, we posted an investor presentation on our Investor Relations website this morning containing supplemental information.
Please note, unless otherwise stated, references to occupancy, average daily rate and RevPAR reflect comparable system-wide hotels on a constant currency basis and closed hotels in Jamaica are excluded from comparable metrics in 2026. Percentage changes disclosed during the call are on a year-over-year basis unless otherwise noted. 
With that, I will turn the call over to Mark.

**Mark Hoplamazian** (Executives):
Thank you, Ryan, and good morning, everyone. We appreciate you joining us today. I'm extremely proud of our teams and the exceptional results they helped deliver in the third quarter. Hyatt continues to demonstrate the strength of our asset-light business model and our insights-led brand-focused strategy, supported by the talent and commitment of our colleagues. 
Our teams are focused on delivering on-property experiences that truly resonate with our guests, deepen loyalty, drive durable fee growth, increase free cash flow and generate attractive long-term returns.
Our third quarter results provide another compelling example of our strategy in action. We delivered strong RevPAR, fee and adjusted EBITDA growth, expanded World of Hyatt membership and grew our development pipeline to record levels, even as certain subregions experienced temporary softness in demand. Our diversified global portfolio, focus on high-end experience-focused travelers and strong commercial platform continue to drive performance and strengthen Hyatt's position as a preferred choice among guests, owners and developers. 
Together, these advantages support high-quality operational execution and growth, driving higher fee earnings and free cash flow.
Turning to our operating results. Third quarter system-wide RevPAR grew 7.2%, exceeding our expectations. Performance was driven by durable demand from high-end travelers and continued strength across our luxury portfolio with some benefit from the FIFA World Cup in July and the timing of the Jewish holidays in September. 
RevPAR growth in the United States also exceeded our expectations, while most international markets delivered strong growth. Average rates grew in all brand categories, driving nearly 80% of our RevPAR growth.
Our focus on driving high-quality RevPAR growth is intentional as it supports higher cash flow for owners, and it also results in higher fees and fees per room for Hyatt. RevPAR increased across all customer segments, business, group and especially leisure travel. 
Year-to-date, we have gained 100 basis points of market share across our portfolio, driven by gains in average rate index, highlighting that our strong RevPAR gains are much more than just favorable industry trends. Together, these results highlight the benefits of Hyatt's differentiated strategy, premium brands that resonate with travelers and win in their competitive set, supported by a commercial engine that drives superior results for our owners.
Business transient RevPAR grew approximately 1% during the quarter with growth accelerating to more than 4% in September, a sign of renewed momentum after the summer with strong results in our select service brands in the U.S. 
Group RevPAR increased a strong 8% in the quarter compared to last year, with some of that growth coming from the FIFA World Cup and the shift in the timing of the Jewish holidays. The strength and resilience of leisure traveler drove leisure transient RevPAR growth of approximately 10%, once again led by our luxury hotels. Demand for high-quality experiences remains strong, with performance at our resorts in the Americas, offsetting temporarily softer demand at our all-inclusive resorts in Cancun.
Looking ahead, we see continued momentum across all customer segments and the pickup in bookings into Cancun is very encouraging. World of Hyatt continues to fuel increased performance across our brands and continues to grow at an exceptional rate with more than 72 million members, up 19% from a year ago. 
But it is not just about scale. World of Hyatt is central to our insights-led and brand-focused approach, and its continued growth reflects the appeal of our brand and the value the program delivers to members and ultimately, to owners. The way we connect and engage with our members differentiates their experience and provides us with valuable insights into what matters most throughout their travel journey.
We see this reflected through the deeper and more frequent engagement with our members. Since 2022, we have seen members with over 100 qualifying stays per year increase by nearly 40%. Our recently announced long-term loyalty collaboration with Delta Air Lines is a great example of connecting with our members beyond their hotel stay experience. 
Our collaboration brings together 2 brands with a shared commitment to thoughtful premium experiences that put members first. Together, Delta and Hyatt aim to make travel more connected and rewarding through exclusive benefits and experiences that extend throughout their travel journey. We're excited about this collaboration and look forward to sharing more as the program develops.
Together, our differentiated brands, commercial platform and growing base of highly engaged World of Hyatt members strengthen our value proposition for guests, owners and developers. This drives demand for Hyatt Hotels and supports attractive owner returns, underpinning our quality growth strategy. Hyatt's value proposition continues to resonate with owners and developers as reflected in our exceptionally strong development activity during the third quarter. We ended the quarter with a record development pipeline of approximately 158,000 rooms, up 12% from a year ago. Year-to-date, we have signed 70% more deals compared to last year, and our construction starts are up over 40%.
The performance of our luxury, lifestyle and inclusive collection brands continue to generate strong owner interest and signings, while our Essentials brands are building continued momentum and expanding Hyatt's reach. In fact, during the quarter, over half of the signings for our Essentials brands in the United States were in markets new to Hyatt. 
Third quarter net rooms growth was 3.9%, excluding rooms from the Playa Hotels acquisition that were removed from Hyatt's room count in the fourth quarter of 2025. Notable openings included the Thompson Seville, our second Thompson Hotels property in Spain and Hyatt Vivid Punta Cana.
Our expansion into upper mid-scale continues to gain momentum with 14 hotel openings in this segment during the quarter. As we look ahead, we expect over half of our openings for the year to occur in the fourth quarter. Approximately 2/3 of our anticipated fourth quarter openings are hotels in the final stages of preopening. The remainder of our anticipated growth is largely comprised of multi-property conversions that, in some cases, have taken longer to finalize than anticipated and strategic partner hotel additions. We've built a strong and rapidly expanding international pipeline that we believe will deliver accretive fees per room.
We also see significant opportunities to expand our brand presence in the United States. Together, these opportunities give me confidence in our ability to deliver the net rooms growth targets and most importantly, the fee growth that we outlined at our Investor Day in May. 
Now turning to transactions. We continue to make progress to sell the Hyatt Grand Central New York and are also advancing discussions to sell several additional properties. We will continue to provide updates as we make progress on these sales. Throughout these sales, our disciplined approach remains consistent with our track record of pursuing transactions that achieve attractive values while securing long-term management or franchise agreements, supporting continued fee growth and shareholder value.
We continue to sharpen our brand focus, invest in our talent and leverage technology to deliver high-quality experiences and operate more effectively. The appointment of Amar Lalvani as Hyatt's first Chief Creative Officer reflects that commitment. He's helping bring our brand strategy to life across the company and equipping colleagues to deliver it. 
We believe these capabilities strengthen Hyatt's competitive advantages and support long-term value creation. As we shared at Investor Day, we have built a powerful flywheel that creates value for guests, owners, colleagues and shareholders.
Our third quarter results reinforce the strength of our strategy and our confidence in Hyatt's long-term potential. Our opportunity is reflected in the strong development pipeline and the significant activity behind it. But this is not about growth for the sake of growth. 
We are and will remain intentional about where and how we grow, focusing on openings that strengthen our network, further drive owner returns that will result in high-quality, durable and compounding fee growth into the future. I'll now turn the call over to Joan to provide more details on the quarter. Joan, over to you.

**Joan Bottarini** (Executives):
Thank you, Mark, and good morning, everyone. Our third quarter results provide another proof point of the strength of premium leisure travel globally and healthy group demand. As Mark mentioned, RevPAR exceeded our expectations, increasing 7.2% compared to last year, driven by resilient demand from premium travelers and incremental demand from the FIFA World Cup. 
In the United States, RevPAR increased a strong 8.2% compared to last year, driven by robust leisure travel and healthy group demand with the FIFA World Cup contributing approximately 50 basis points to growth.
Our select service hotels also performed well with RevPAR increasing 6.8%, reflecting strong business transient demand and easier comparisons to last year. Outside the United States, RevPAR increased nearly 6% in the third quarter. Outbound travel from the U.S. to our international hotels was up over 10%, reflecting robust international travel demand and continued strength in the higher-end U.S. traveler. 
Asia Pacific, excluding Greater China, delivered robust RevPAR growth of more than 10%, driven by healthy inbound travel and demand in key markets where Hyatt has strong brand representation.
Greater China RevPAR increased 2.1% compared to last year, supported by leisure transient demand and strong average rate growth. Europe generated RevPAR growth of 4.3%, driven by healthy domestic leisure demand and continuing growth of international inbound travel. 
In the Middle East, RevPAR declined by only 3% compared to last year as strong domestic travel helped to offset a 40% decline in international inbound travel. In the Americas, excluding the United States, RevPAR increased 9.2%, benefiting from strong resort performance in the Caribbean, highlighting the exceptionally strong demand for high-end leisure travel experiences.
Net package RevPAR in our all-inclusive portfolio declined only 2.5% compared to last year. Strong demand for travel in the Caribbean and other parts of Mexico largely offset the more than 10% decline in Cancun. 
Despite these demand pressures, I'm very pleased to share that our all-inclusive resorts in Cancun have gained 400 basis points of market share this year, reflecting the strength of our brands in the markets in which we operate. Turning to our financial results. Our core fee business continued to perform well, supported by strong top line performance, healthy hotel level profitability, increasing scale and the quality of our portfolio.
Gross fees increased 15.2% to $327 million, ahead of our expectations, driven by strong performance across our managed portfolio, contributions from newly opened hotels, the new management agreements from the Playa portfolio and the quarterly timing of non-RevPAR fees. 
Our strong fee growth highlights the benefits of our broad, diversified and differentiated portfolio and our ability to deliver growth even as certain geographies face demand pressure. Distribution segment adjusted EBITDA declined compared to last year and was below our expectations as softer demand in Mexico and the reduction in flight capacity was more pronounced than anticipated.
Results continue to be impacted by lower demand for 4-star properties, and we expect a gradual recovery when flight capacity increases and travel spending improves among this consumer segment. Overall, third quarter adjusted EBITDA was up over 19% year-over-year, adjusted for asset sales, reflecting the strength of our core fee business. 
As of September 30, we had total liquidity of approximately $1.8 billion, including $1.3 billion of available capacity on our revolving credit facility. During the quarter, we also returned approximately $161 million to shareholders through share repurchases and dividends, bringing our year-to-date returns to $336 million.
We ended the quarter with approximately $1.4 billion remaining under our share repurchase authorization. Our balance sheet is strong, and we remain committed to maintaining our investment-grade profile. Looking ahead to the fourth quarter of 2026, while travel demand continues to vary across regions, we remain confident in our full year outlook, supported by the strength of our brands. 
Let me start with the 2 regions that are experiencing demand pressure this year. In the Middle East, while RevPAR declined by only 3% in the third quarter, we expect fourth quarter performance to be below those levels due to the seasonality of the business and the ongoing geopolitical conflict.
We continue to anticipate an approximate $10 million impact to full year fees. In Mexico, booking trends at our all-inclusive resorts are improving sequentially, but have not recovered to the extent we expected for the fourth quarter. Despite the headwinds in Mexico throughout the year, our teams have delivered exceptional results, managing to mitigate the impact to a $20 million decline in fees for the year, which equates to about 1.5% of our total annual gross fees. 
Looking ahead to the first quarter of 2027, forward booking trends are encouraging with first quarter bookings at our Americas all-inclusive resorts up in the high single digits and air capacity showing signs of improvement from lower levels.
The continued strength of our core business reinforces our confidence in its underlying fundamentals even as we navigate temporary regional challenges. In the United States, forward booking trends remain strong for the balance of 2026, with fourth quarter group pace for our U.S. full-service hotels up in the mid-single digits. We expect fourth quarter U.S. RevPAR growth to moderate relative to the second and third quarters, reflecting more difficult year-over-year comparisons and the impact of the November midterm elections. Outside the United States, we expect continued strong performance in Asia Pacific through the balance of 2026.
Reflecting these trends, we are increasing our full year system-wide RevPAR growth outlook to between 5% and 5.5%. We now expect full year RevPAR growth in the United States of between 5% and 6%. We expect RevPAR growth in international markets to be slightly lower than the United States for the full year. We continue to expect full year net rooms growth of approximately 6% with momentum in conversions, including within our new brands, driving another year of strong organic growth. As Mark mentioned earlier, we expect more than half of our openings for the year to occur in the fourth quarter.
The strong development activity we are seeing reinforces our confidence in achieving the long-term growth expectations that we laid out at our Investor Day. We expect full year gross fees to grow between 10% to 11% in the range of $1.32 billion to $1.335 billion, reflecting continued growth across our asset-light platform. 
Importantly, we are delivering this strong growth despite the temporary hotel closures in Jamaica and softer demand in Mexico and the Middle East, reinforcing my confidence in the strength of our fee business and long-term fee growth.
We expect our full year adjusted EBITDA to grow at a strong rate of 14% to 17% in the range of $1.17 billion to $1.20 billion. This outlook reflects strong fee performance, slightly lower adjusted G&A and an approximately $30 million year-over-year decline in our Distribution segment compared to 2025. We are maintaining our adjusted free cash flow outlook for the full year in the range of $580 million to $630 million, an increase of between 20% to 30% and adjusted EBITDA to adjusted free cash flow conversion of at least 50%. Finally, we are raising our full year outlook for capital returns to shareholders to between $375 million and $425 million.
In closing, our third quarter results demonstrate the continued strength of Hyatt's asset-light earnings model. As we highlighted during Investor Day, our strategy is designed to generate high-quality, durable fee growth and increasing cash flow over time, and our results this quarter are another demonstration of the successful execution of our strategy. This concludes our prepared remarks, and we're now pleased to answer your questions.

**Operator** (Operator):
[Operator Instructions] 
Your first question comes from the line of Conor Cunningham with Melius Research.

**Conor Cunningham** (Analysts):
Just -- you have a competitor out there that's talking about 3% to 4% RevPAR growth next year. Joan, you just listed a lot of headwinds that you had this year that shouldn't necessarily repeat next year. So just trying to understand the context of how you view RevPAR or RevPAR right now, just given where you sit on the demand commentary. 
And then maybe if I could just sneak a little one on top of that, just bringing it back to fees, like what gives you confidence in the [ NRG ] performance next year? I mean, obviously, this year has been a little lumpy. So just any thoughts on the 6% to 8% you laid out at Investor Day would be helpful.

**Joan Bottarini** (Executives):
Sure. Maybe I'll just start on 2027. We're in the middle of our planning process, and we will absolutely update you at Q4 with more specifics around guidance for 2027. But right now, it's setting up really nicely. Trends are strong across leisure, as we mentioned many times in our prepared remarks, and we have every reason to believe that those will continue. 
As we're looking into Q4, we're seeing that continue into Q4. So expect that to continue into the first part and throughout 2027. Group is also setting up nicely for next year. We are lapping some outsized group performance from the World Cup. But even despite that, we've got good group pace on the books for next year.
And we also have the disruptions from this year, which are temporary, are going to help us next year as we go into -- early in the first part of the year, we already mentioned that the pace into our all-inclusive segment is up in the high single digits. So as we think about leisure, we've got visibility into those RevPAR -- net package RevPAR numbers that they will be improving. 
So we feel good about next year's setup, and there's several tailwinds that are going to help us into next year, including, I'll just mention the hotels reopening in Jamaica as well. So there's several items, and we'll unpack all of that for you in the fourth quarter when we give guidance for next year. And that also just reaffirms what we said at Investor Day as far as our expectations around RevPAR growth and fee growth going into next year. And so maybe Mark will cover NRG.

**Mark Hoplamazian** (Executives):
Yes. I'll just add one thing to what Joan just said to support and substantiate the pace that we see in our all-inclusive business airlift into Cancun is improving as we speak serially. And we see that continuing into planned scheduled carrier activity in the first quarter and second quarter of next year. 
Jamaica is significant growth in airlift. Of course, the year-over-year numbers are stratospheric because they got cut back so severely in '26, but it is a restoration -- a very quick ramp to restoration of lift into Jamaica. And the Dominican Republic, which has had an absolutely stellar year is holding its own with respect to airlift, so should be able to support continued strong demand there.
The second dimension of this that I just wanted to touch on, which is really meaningful for us is that if you look at the component pieces of group, by far, the largest growth is coming from corporates. And if we look into what corporate looks like for the full year this year, it looks like it could be up in the range of 7% or thereabouts. And if you look into next year, corporate pace is up almost 10%. 
Now corporate makes -- first of all, we serve a relatively higher rated corporate base. And secondly, when corporate bookings are that strong, other revenue streams, catering, banqueting, F&B come along with it. So that's probably the thing that I'm tracking the closest. This year, of course, we had a massive growth in sports and SMERF business that had to do with FIFA. But even if you sort of ignore the FIFA impact there, the corporate forward bookings look really strong.
As to NRG, there's no question that we expect NRG to be more even over the course of the year in '27. We have -- if you just look at the pipeline itself without any -- without regard to any now unforeseen in the year for the year opportunities that come up between now and the end of the year or into the first quarter, we will be solidly in above 6% -- in the 6% to 7% range in the first quarter is our current outlook with respect to openings year-over-year increase.
So I think we're on our way back to restoring a more regular pace. You heard that the increase in the number of pipeline hotels under construction is up 40%. That's contributing to that. But we also are expecting some carryover of some of the portfolio deals and other conversions that we are working on today into the first quarter. 
We still stand by our annual outlook for '26. It just means that we may end up starting with an extra boost from early openings in '27. So that's our outlook in the near term for NRG. And firmly, I just reaffirm what we said at Investor Day for the '26 to '28 time period, we still feel very confident about 6% to 8%.

**Operator** (Operator):
Your next question comes from the line of Brandt Montour with Barclays.

**Brandt Montour** (Analysts):
Maybe just following on that, Mark, I want you -- I want to hear from you regarding the new development solutions that you rolled out in early October relating to conversions. What sort of prompted that? How sort of linked was that to some of the -- I guess, the sort of lowered revision on NRG last quarter. Do you think that, that sort of improved any sort of slowdown or sort of slow steps that you had in the process in terms of how we should think about next year?

**Mark Hoplamazian** (Executives):
Yes. I think there are several things that have happened over the course of this year. It's not just that which has happened in the last month or 2. But a couple of things. First, the utilization of AI to facilitate and accelerate how we approach property improvement plans for conversions. The turnaround time has been reduced from several weeks to a day. And that's already paid dividends in Asia Pacific, which is where -- that's the region that sort of led the way in terms of honing the best approach to making sure that we're taking structural considerations into account plus brand standards and brand codes. 
So we feel like we've got an extra arrow in the quiver at the moment to be able to go faster, be more definitive and even assist our developers in costing what the conversions might cost.
Secondly, we've been working on and we still -- we continue to work on an end-to-end AI platform from the time that a deal is pitched through the time that the hotel is around. So it's a full continuum. I'm not going to go into further details because of competitive reasons, but we are starting to see some real benefits from that. 
I think the -- some of the time lines that it has taken in the past, especially in and around systems conversions require -- there's the old adage, if you can't untie the Gordian Knot, you sometimes have to cut it. Well, we're cutting it because going in sort of traditional ways to reduce cycle time for systems conversion is painful and arduous. So we are actually developing some tools to be able to actually work around that and be able to make conversions -- have conversions go live faster and ramp the hotel faster by virtue of plugging in World of Hyatt.
So those are the kinds of changes. I believe that we will be largely complete with the end-to-end product that we are working on now in the first quarter of next year. And I think it will continue to benefit us because conversions remain a significant proportion of our total NRG.

**Operator** (Operator):
Your next question comes from the line of Shaun Kelley with Bank of America.

**Shaun Kelley** (Analysts):
I think you tackled a lot of what we had to ask, Mark. It might be helpful. We've seen a lot of developments on the agentic AI front in the last few months, specifically really since early September. And I know you are having a lot of conversations. You're pretty thoughtful on this subject. So just would love your view on how do agents specifically impact a little bit the booking journey? And how is Hyatt able to sort of directly steer those agents to your direct channels as opposed to other aggregators that are out there? What are you kind of seeing on that distribution funnel?

**Mark Hoplamazian** (Executives):
Yes. So thank you, Shaun. First, I would say that just to level set, the actual bookings that are being completed that originate through LLM platforms is very, very small. So we are still early, early in the days of agentic -- direct agentic booking. It's coming, and it will grow fast. I mean I think the pace of growth in AI-related tools and technology has proven to be extremely high. And I think we will see the same thing in agentic distribution.
We are absolutely focused on being available in the right ways to all purveyors. So across Gemini, OpenAI,  [indiscernible] you name it, we will have presence we are going to remain relatively agnostic. When I say relatively, I don't mean we have some biases. 
I am saying that the capabilities within these LLM frames are different. They're not all the same, and they don't all present your product the same way. Our learnings from being very early in representing Hyatt directly in the apps that you can find through ChatGPT's platform have taught us a lot. 
We have a much better handle on the people who are coming through those channels. They are younger and spending a lot more on travel. But the booking actually, the booking activity where it terminates or concludes rather in that environment is still very low.
So I would say I'm a believer that agentic booking will be a significant portion of our total distribution picture. over the next couple of years, I think we'll see that expand. The key is that our strategy is really focused on elevating our brands and being brand focused. 
And the clearer and sharper you can define your brands and the experiences that people can expect to have and also the total experience with respect to the booking, prebooking into stay and post stay makes it clear when a personal agent is searching for a particular trip. So we believe that for our clientele, I would not say that this matters in economy, for example, our budget hotels. It matters a lot in resorts. It matters a lot in luxury and lifestyle. It matters a lot in some full-service hotels. 
So I would say in the categories that we play in, that is the bulk of our system, it matters a lot. And that's why we are so hyper focused on really elevating our brands and making them sharper, more defined, more findable and more precise.
And so we are actively engaged. By the way, I think you'll hear this from everybody. This is not the time to sort of narrow the focus. It's a time to experiment and continuously test and learn, and that's what we're doing.

**Operator** (Operator):
Your next question comes from the line of Ben Chaiken with Mizuho.

**Benjamin Chaiken** (Analysts):
We've covered a lot of important topics. Just one for me. There was a number of impacts this year. Joan, you alluded to this, and maybe we can take it offline if you prefer. But to the extent we can kind of quickly review the impacts in '26 as they sound like most, if not all, will help in '27. I believe, Joan, you said $20 million Mexico impact, $10 million from Middle East. 
I guess, was that the total impact? Or is that strictly within the kind of managed and franchised hotel business as opposed to destination? And then part 2, could you remind us the total Jamaica impact in round numbers and then as well as the destination business? And if I'm missing anything else?

**Joan Bottarini** (Executives):
Sure. So I'll just reiterate for you, Ben, our outlook that we have, the 10% to 11% of fee growth for the full year and the 14% to 17% of EBITDA growth for the full year, which has been raised in this release this morning, reflects the impacts that we've experienced across the course of the year. So really [Technical Difficulty] and EBITDA. And the -- with respect to your question, just to summarize it for you, the fee impacts in Mexico and the Middle East for the year relative to our Q4 original guidance is about $30 million. 
And that's just slightly higher in our latest outlook relative to our Q2 outlook for Mexico. So $30 million in total for the year embedded within our full year guidance for fees, again, that 10% to 11%. So stronger RevPAR that we've been experiencing, stronger demand, including significant rates across the world has offset that $30 million.
For EBITDA, the impact when you include the fees plus the distribution business, it's a total of $60 million. So that is just wrapping it up into the aggregate numbers, again, from the beginning of the year until now. And we are remaining with this 14% to 17% EBITDA growth outlook, which is very, very strong and very consistent with our algorithms embedded within -- with respect to RevPAR growth and the flow-through. So very good results, and that's the summary of the impact for the year. Again, temporarily -- we believe these are temporary as we've seen now improving sequential [Technical Difficulty] dynamics that have impacted us, particularly in Mexico, which is the vast majority of that number, we're seeing improve. And that is a really good sign for us as we look ahead into 2027.
For Jamaica, we announced that in our original guidance, which was a $15 million headwind. As we look ahead into next year, they -- our owners are very focused on opening up these hotels. So our current estimate right now is late Q1, early Q2 for reopening of those hotels in Jamaica. So we'll get some of that -- some of that tailwind into next year and then into 2028 as well.

**Mark Hoplamazian** (Executives):
So Ben, I would just add one thing, and that is that we're tracking, obviously, how things are starting off in the fourth quarter. There are 2 areas that I just wanted to make mention of in passing. One is there's been a lot of disruption on the streets in France. That has not had an impact on our business to date. 
We're running ahead of where we thought we would be and pace for the quarter looks good. Actually, group pace has actually increased. And then the U.S. continues to hold up very well. 2 areas, business transient within our upscale hotels and luxury leisure which has just remained the juggernaut of growth for us and great stability, durability of demand.
So those are the things that are encouraging us to set up well going into next year. I think -- so Joan covered it completely, and that's how we have mapped out the year to date. I guess what I would say is while I'm not -- we are not taking any early indicators in October to the bank at this point because we shouldn't. The world is a very volatile place, and we have midterms coming up. One thing we can say is that things are not falling off -- falling through cracks or falling off the table at this point.

**Operator** (Operator):
Your next question comes from the line of David Katz with Jefferies.

**David Katz** (Analysts):
You've covered a ton of territory. I wanted to ask about the growth for Hyatt into the more moderate or limited service areas of the business. Understanding the strategic importance of having that as part of your portfolio, what I observe is that many of the other larger hotel platforms are trying to increase the economic intensity, right, of fees per room of each new unit, right, added to [ NRG ].
And on the surface, that may appear to decrease in economic intensity. But I presume that it has other economic benefits across the entirety of the platform that you consider, not just necessarily each contract on the surface of it. Can you maybe help us just understand those economic benefits and how that adds to the totality of Hyatt, which is such a strongly growing enterprise?

**Mark Hoplamazian** (Executives):
Absolutely. Thanks, David, for the question. First, across the new upper mid-scale brands that we have launched, Studios Select -- Hyatt Studios, Hyatt Select and Unscripted by Hyatt. We have currently 150 -- over 150 hotels in the pipeline. And the signings that we have made, over half of the signings are in brand-new markets to Hyatt, where we literally have 0 representation whatsoever. 
We did an enormous amount of research in 2023 and '24, looking at travel patterns for our members, and we discovered exactly where they -- when they were staying out of system, where they were staying -- in which markets they were staying out of system, and we looked and evaluated those markets where our competitors had product in the mid-scale or upper mid-scale and we didn't, we were absent.
And so that's been our target, and we are fulfilling that as we speak. The -- I think it's something like close to 70% of our openings in these brands have been in markets that we had identified as part of that research. So we are absolutely on strategy for covering new markets where our members were already traveling but staying outside of our system. And so the purpose of it is to do -- is twofold. One, to make sure that Hyatt in a very high-quality representation because we want Hyatt Select -- Hyatt Studios, Hyatt Select and Unscripted by Hyatt to be at the high end of their competitive sets. We want them to have a quality experience in the upper mid-scale in those markets that can be affordable for developers to build and very profitable for them, but also create a good guest experience for our guests.
And that so far is proving to be true. It is, by definition, true that when you have a hotel that's got a leading rate of $100 as opposed to $200, your total fee base and the room size is much smaller, the fee base is going to be lower. So that's just math. It is not an -- it is not an acute issue right now, meaning we don't expect -- as we forecast and look at our total pipeline, including these 150 hotels, our fees per key in the pipeline is actually accretive. 
It's higher than our current fees per key in our open and operating hotels. So it will take years for that to start to show up in terms of our total mix because the hotels that we are opening in the full-service luxury and resort areas are very high rated and our fee base continues to grow at a pretty good pace.
So I'm not worried about it from a system perspective, and you shouldn't be either. I think the key is being present where our travelers are traveling and being there with a high-quality representation. That was the rationale. That is what we're fulfilling right now. 
It is true that new construction starts in the U.S. have been low. That's partly why you see great results across pretty much all chain scales right now. And I think that, that will -- yes, and borrowing costs have gone up, but I think that more and more developers will understand that in either new markets for Hyatt or markets in which we are very underrepresented, there are new opportunities to still earn a great return because underlying performance is so high, and it really helps our network effects significantly.

**Operator** (Operator):
Your next question comes from the line of Duane Pfennigwerth with Evercore ISI.

**Duane Pfennigwerth** (Analysts):
I was hoping you could expand a little bit on the recent announcement with Delta this past quarter. Any unique aspects of that partnership maybe versus past relationships? And what future steps or opportunities in how you might work together?

**Mark Hoplamazian** (Executives):
Yes. The one thing I can say is what we've already announced, and that is that the arrangement that we've made is a dual earning relationship. So when you fly Delta or stay at Hyatt, you earn on both sides. That was a feature that is new to our partnerships, our airline partnership that wasn't true in our prior one in recent years.
So that's the one attribute that we did talk about. We will tell you a lot more in the first quarter. So when we announce fourth quarter earnings, we will unpack how we are approaching this partnership. I would say that the teams are working extraordinarily well together. The customer base overlap is -- that is the demographic overlap between our core customer base is very high, but the member opportunity in terms of expanding member utilization of -- Hyatt member utilization of Delta and Delta SkyMiles participants utilization of Hyatt, both have big opportunities. 
That's why both companies saw there to be significant opportunity for us to actually make this a very strong win-win situation. And it's really important to us as we continue to hyperfocus on elevating our brands, that we really continuously deepen our relationship with the premium customer with a high household income customer. And that's what we feel like we are gaining with the partnership with Delta.

**Operator** (Operator):
Your next question comes from the line of Lizzie Dove with Goldman Sachs.

**Elizabeth Dove** (Analysts):
Could you maybe just talk about generally what you're seeing in the environment for key money overall? I guess in the near term, I think you raised EBITDA but lowered CapEx guidance and maintained free cash flow. So I wasn't sure if that was kind of related to key money or something else, but curious just kind of over the long term as well.

**Mark Hoplamazian** (Executives):
Yes. First of all, key money is actually a reduction of free cash flow. So it's included in how we report free cash flow. I don't know how other companies do it, but that's how we report. The fact is that there's a lot of key money flying around development deals these days. I think the intensity of it varies by type of project or chain scale. 
I think the thing that we have focused on most of all is being super clear and quite deliberate and precise about what the actual needs are for a developer. And oftentimes, what happens is the allure of an upfront check tends to take hold in some cases. But when you actually think about it, it's actually a very small proportion of the total earnings that the owner developer can expect over a 20-year lifetime of a contract.
And so in a number of cases, in the last quarter, and I'm close to this because I've been directly engaged in several of these conversations with developers, the dialogue has been, look, you're presenting us with an ask with respect to a higher amount of key money. 
We're presenting you with a higher expected return over the next 20 years. And by the way, your actual need is not a onetime injection at the beginning. It's actually a piece of capital in your cap stack that you can benefit from and actually get -- still maintain your ability to do the transaction. 
And what we get is a return of capital. So we've been doing more by way of, I would say, innovative ways to support development, that are not necessarily as key money intensive, they still are capital -- they still deploy capital, but maybe in a different way. And so we have, I guess, both the track record and capability internally to do it. And so that's what we've been practicing. We actually laid out that we would be spending $150 million to $170 million a year in key money. 
And I expect that over the next 3 to 4 years, that number will be in and around that range. It might be higher in 1 year and lower in another year. But my guess is that, that range is still a good range for you to be thinking about as you look into the future.

**Operator** (Operator):
Your next question comes from the line of Rose Smedes (sic) [ Smedes Rose  ] with Citi.

**Bennett Rose** (Analysts):
I wanted to ask you just 2 quick ones. I guess the first one, just going back to Mexico for a moment. You said that it was weaker than expected than your expectations in the third quarter. And I was just wondering what sort of points were you looking at going into the third quarter that turned out to be maybe not so predictive or accurate? 
And just kind of what gives you confidence now that we're in the fourth quarter that we're not just seeing sort of another head fake or maybe there's something competitive going on the ground in Cancun that's not necessarily related to the political disruption we saw earlier this year?

**Joan Bottarini** (Executives):
Yes, Smedes, we actually saw some demand weakness in September, particularly in the third quarter. So it was slightly worse than our expectations. And we actually thought that flight capacity would be improving as we were looking at this Q2. It's been a little slower, but we're seeing it sequentially improve, as both Mark and I mentioned.
So as we head into Q4 and the first quarter, second quarter of next year, it's sequentially improving. My comment about market share in my prepared remarks is really remarkable. And our owners are pleased despite what's happening in the competitive environment that we are delivering and our commercial and operations teams are delivering market share gains. And that's what we need to be doing in this environment. And as we see the recovery continue from here, we'll be able to just drive more top line and cash flow for owners into the future.

**Mark Hoplamazian** (Executives):
I think it's -- if you think about the level of disruption in the Riviera Maya area because that's really where it's been concentrated. The Pacific Coast of Mexico, Dominican Republic, Costa Rica, they've been fine. In fact, they've been -- Dominican Republic has had probably its best year ever. So yes, it's significant. It's a bit over 1/3 of our total all-inclusive business. 
But all in all, if you think about the severity of the disruption to gain 400 basis points of market share and only have a fee degradation of 1.5% of our total fee base. I think, just demonstrates that the diversity even within our inclusive business, let alone our total business is proving that we are not highly subject to mass volatility as a result of what's going on in Mexico in a given area.
Joan mentioned, in case you didn't pick this up, it's an extraordinary number. Americas ex U.S. is up 9% in the third quarter. That's extraordinary. And a lot of that is in the Caribbean in our other resorts. So all I'm saying is that the health of the luxury leisure traveler is very, very good, and we are capturing that in different ways. 
And we do have some headwinds that are specific, and part of that has to do with the Sargassum, the seaweed problem that abates it's seasonal. So the first and second quarter are the best times, and they are also the biggest quarters for us in terms of total revenue. The times that it gets worse are in the weaker third quarter.
So that's some more color. I would say what Joan mentioned in passing is absolutely true. We did expect lift to improve more than it actually did into Cancun in the third quarter, especially in September, and that did not come through. So those -- that hopefully rounds out and contextualizes for you how we see our business there.

**Bennett Rose** (Analysts):
It does. I appreciate that. And then I just wanted to ask you quickly, you mentioned what looks like a really good pace of corporate group for '27. What sort of percentage is corporate group of your overall kind of group segment usually?

**Mark Hoplamazian** (Executives):
Corporate usually is about -- it typically goes something like 40-40-20, where we have 40% corporate, 40% associations and 20% other. Other would be sports and SMERF and so forth, local and also social. I will say that, that -- those proportions changed in 2026, where sports and social were much higher as a proportion of the total. And that was very much...

**Bennett Rose** (Analysts):
[indiscernible] FIFA, right?

**Mark Hoplamazian** (Executives):
Yes, exactly. It's all FIFA.

**Bennett Rose** (Analysts):
I mean, are you able just to provide or characterize the pace of group bookings just overall for '27? I was it like mid-single digits or maybe.

**Mark Hoplamazian** (Executives):
If you remove FIFA, it's mid-single digits right now. And I think the year is young. The corporate -- the corporate demand is very encouraging. And I think that's really what we -- it's not just corporate, by the way, in group. But if you look at our negotiated business, we were up 5%, 4.8%, something like that in the third quarter for corporate negotiated business across our full-service hotels. That's significant. So I think that we're seeing health among the -- significant health among the larger corporations -- and so they're traveling. They're out -- they're supporting business travel generally and group is a particular standout in terms of rate of growth into '27.

**Bennett Rose** (Analysts):
We'll see now that's why Hyatt isn't on Citi's travel portal. If you're doing too well.

**Operator** (Operator):
Our last question comes from the line of Dan Politzer with JPMorgan.

**Daniel Politzer** (Analysts):
I just wanted to follow up on the distribution business, kind of how you're thinking about the recovery into next year and the path to getting back to that 2025 EBITDA levels for that business? And then similarly, can you maybe talk about your attitude or willingness and how you're thinking about keeping or selling this business and if this is something you have inbounds on?

**Joan Bottarini** (Executives):
Sure, Dan. As we look into -- again, we're in the early cycles of planning for next year, but we do see this airlift capacity will have a direct impact for the distribution business and sequentially improving into next year. So that is absolutely what we're seeing in the data. And half of the business, and we've reported this before, is in the 4-star category. 
So as that consumer and their spending improves over time, and we're seeing some of that in our lower chain scales in the U.S. So as that improves, we'll see that business improve into those markets as well. And finally, with Jamaica reopening, that's a nice tailwind for the distribution business as they have more inventory to sell into next year. So do you want to comment on the other question Dan has?

**Mark Hoplamazian** (Executives):
I think the answer is we really don't have any further update on how we're thinking about strengthening that business. It still remains a very important distribution channel for us, and it's certainly helped us significantly in the gain of market share that we have seen because we're able to track where lift is coming from and where demand is coming from, primarily because we have a platform, a booking platform in use by over 175,000 travel advisers and travel agents. So we have a pulse on the market, and that allows us to be responsive to what we're seeing come through the system.
Admittedly, the vast majority of that, which we are focused on is 5-star. That's really our core. But with now Bahia Principe and some other activities that we've got going under the Alua brand, we will see more 4-star activity over time. So I think the value of the platform is not diminished in value. In fact, it's probably grown in value during tough times and the ability to improve our competitive positioning remains ahead of us.
So -- but nothing more specific to share with you at this point. So thank you all for joining us. I really appreciate the time that you've taken out of your busy days to listen. And stay tuned for really what will be another active quarter ahead. And we have, as you've heard from us, a very constructive positive outlook for the future. So thank you again, and have a good day ahead.

**Operator** (Operator):
This concludes today's conference call. Thank you for participating, and have a wonderful day. You may all disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### H_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Joan Bottarini｜guidance：全年系統 RevPAR 成長財測上調至 3.5%–4.5%（原話："increasing our full year system-wide RevPAR growth outlook"）
- 2026-07-30｜Joan Bottarini｜guidance：全年美國 RevPAR 成長預期 3%–4%（原話："RevPAR growth in the United States of between 3% and 4%."）
- 2026-07-30｜Joan Bottarini｜guidance：全年 gross fees 財測維持，成長 9%–11%、1.305–1.335 十億美元（原話："grow between 9% to 11% in the range of $1.305 billion"）
- 2026-07-30｜Joan Bottarini｜guidance：全年調整後 EBITDA 財測維持，成長 13%–18%、1.155–1.205 十億美元（原話："13% to 18% in the range of $1.155 billion to $1.205 billion"）
- 2026-07-30｜Joan Bottarini｜guidance：調整後自由現金流財測維持，EBITDA 轉換至少 50%（原話："adjusted free cash flow of at least 50% for the full year"）
- 2026-07-30｜Joan Bottarini｜capital_allocation：全年股東回報（回購加股息）預期 3.25–3.75 億美元（原話："$325 million and $375 million of capital to shareholders"）
- 2026-07-30｜Joan Bottarini｜guidance：第三季全球 RevPAR 預期落在全年區間低端（原話："global RevPAR growth towards the low end of our full year"）
- 2026-07-30｜Joan Bottarini｜guidance：第三季 net package RevPAR 預期略低於去年（原話："net package RevPAR to be moderately below last year."）
- 2026-07-30｜Joan Bottarini｜guidance：全年淨增房數約 6%，轉換案帶動（原話："approximately 6% for the full year, with momentum in"）
- 2026-07-30｜Mark Hoplamazian｜guidance：全年淨增房數區間下調，Q4 開幕部分可能延到 2027（原話："quarter openings, some of which could slip into 2027."）
- 2026-07-30｜Mark Hoplamazian｜commitment：管理層表示對 Investor Day 所述有機成長的信心很高（原話："I want to be clear, our confidence in delivering on"）
- 2026-07-30｜Mark Hoplamazian｜capital_allocation：Hyatt Grand Central New York 出售預期不會在 2026 年完成（原話："we no longer expect the transaction to"）
- 2026-07-30｜Mark Hoplamazian｜capital_allocation：持續洽談出售部分自有資產（原話："assets to unlock additional value from our owned portfolio."）
- 2026-07-30｜Joan Bottarini｜risk：中東飯店營收明顯低於去年，估計全年費用減少約 1,000 萬美元（原話："will reduce full year fees by approximately $10 million."）
- 2026-07-30｜Joan Bottarini｜risk：墨西哥 all-inclusive 訂房復甦不如預期，對費用影響約 1,500 萬美元（原話："resulting in an approximately $15 million impact to fees"）
- 2026-07-30｜Joan Bottarini｜risk：中東 RevPAR 年減 36%（原話："RevPAR in the Middle East declined by 36%"）
- 2026-07-30｜Joan Bottarini｜margin：世界盃對美國 RevPAR 成長的貢獻約 70 個基點（原話："contributed approximately 70 basis points of RevPAR growth"）
- 2026-07-30｜Joan Bottarini｜margin：第二季 gross fees 年增 8% 至 3.24 億美元（原話："Gross fees increased 8% to $324 million"）
- 2026-07-30｜Joan Bottarini｜margin：自有及租賃部門調整後 EBITDA 還原資產出售後成長 16%（原話："owned and leased segment adjusted EBITDA increased by 16%"）
- 2026-07-30｜Joan Bottarini｜margin：第二季調整後 EBITDA 還原資產出售後年增約 9%（原話："approximately 9% year-over-year after adjusting for"）
- 2026-07-30｜Joan Bottarini｜risk：分銷部門受 4 星級客群需求偏弱影響（原話："lower demand for 4-star properties"）
- 2026-07-30｜Joan Bottarini｜margin：分銷部門全年 EBITDA 預期較 2025 年減少約 2,500 萬美元（原話："$25 million year-over-year decline in our Distribution"）
- 2026-07-30｜Joan Bottarini｜margin：成長數字已調整 JV 按比例 EBITDA 的新定義，口徑為扣除 1,300 萬美元（原話："$13 million of pro rata JV EBITDA removed under our updated"）
- 2026-07-30｜Joan Bottarini｜capital_allocation：年初至今以回購與股息回報約 1.75 億美元（原話："we've returned approximately $175 million to"）
- 2026-07-30｜Joan Bottarini｜capital_allocation：回購授權餘額約 15 億美元（原話："approximately $1.5 billion remaining under our"）
- 2026-07-30｜Joan Bottarini｜commitment：重申維持投資等級信用（原話："We remain committed to our investment-grade profile"）
- 2026-07-30｜Joan Bottarini｜capital_allocation：Q2 回購金額偏低，原因為 Investor Day 期間的禁止交易期（原話："we were locked out for Investor Day for a period of time"）
- 2026-07-30｜Mark Hoplamazian｜risk：部分轉換案因 PIP 比原先模型更重而延後（原話："turned out to be heavier than we initially had modeled"）
- 2026-07-30｜Mark Hoplamazian｜risk：已見到開幕從 Q2 延到 Q3、Q3 延到 Q4（原話："we've seen slippage from Q2 to Q3 and Q3 to Q4 already."）
- 2026-07-30｜Mark Hoplamazian｜risk：約半數管線開幕集中在第四季（原話："our pipeline openings are in the fourth quarter."）
- 2026-07-30｜Mark Hoplamazian｜commitment：管理層稱淨增房數不是價值驅動，淨費用成長才是（原話："You can't take net rooms growth to the bank."）
- 2026-07-30｜Mark Hoplamazian｜product：與 Hall Financial 設立 5 億美元融資工具，Hyatt 提供部分信用支持（原話："We provided some credit support in that facility."）
- 2026-07-30｜Mark Hoplamazian｜commitment：對 Investor Day 提出的 6%–8% 淨增房數區間表示有信心（原話："the 6% to 8% range that we gave during Investor Day"）
- 2026-07-30｜Joan Bottarini｜commitment：管理層預期 9%–11% 的費用複合成長率（原話："the 9% to 11% compounded rate over the next couple of years"）
- 2026-07-30｜Joan Bottarini｜margin：新品牌每房費用較低，對費用有稀釋作用（原話："will be dilutive because of the fees per room"）
- 2026-07-30｜Mark Hoplamazian｜customer：團體訂房窗口沒有明顯改變（原話："booking window with respect to group hasn't really changed."）
- 2026-07-30｜Joan Bottarini｜guidance：美國全服務飯店下半年團體預訂 pace 為中個位數成長（原話："U.S. full-service hotels up in the mid-single"）
- 2026-07-30｜Joan Bottarini｜guidance：2027 年第一季該區域 pace 為高個位數成長（原話："the Q1 pace is up in the high"）
- 2026-07-30｜Joan Bottarini｜customer：2027 Q1 多明尼加 pace 成長逾 20%（原話："The Dominican in particular, is up over 20%."）
- 2026-07-30｜Joan Bottarini｜customer：Cancun 復甦程度不如預期（原話："improving, but not as much as we had anticipated."）
- 2026-07-30｜Joan Bottarini｜risk：全包式飯店 net package RevPAR 第二季年減 1.2%（原話："RevPAR in our all-inclusive portfolio declined 1.2%"）
- 2026-07-30｜Joan Bottarini｜guidance：下半年 EBITDA 預期有強勁假設，Q4 加速（原話："But there is a strong back half EBITDA assumption there."）
- 2026-07-30｜Joan Bottarini｜guidance：下半年美國財測對休閒與商務能見度較低，可能有保守成分（原話："probably some conservatism there"）
- 2026-07-30｜Mark Hoplamazian｜customer：奢華與休閒在各區域持續領先（原話："Luxury was the highest RevPAR growth with the highest ADR"）
- 2026-07-30｜Mark Hoplamazian｜customer：中國奢華飯店 RevPAR 本季成長 11%（原話："China luxury properties were up 11% this past quarter"）
- 2026-07-30｜Mark Hoplamazian｜competition：奢華與生活風格飯店上半年 RevPAR 指數提升近 3 點（原話："lifestyle portfolios increased RevPAR index by nearly 3"）
- 2026-07-30｜Mark Hoplamazian｜customer：World of Hyatt 會員約 6,900 萬、年增 17%（原話："approximately 69 million members, an increase of 17%"）
- 2026-07-30｜Mark Hoplamazian｜product：開發管線創紀錄，約 15.4 萬間、年增 10%（原話："development pipeline of approximately 154,000 rooms, up 10%"）
- 2026-07-30｜Mark Hoplamazian｜customer：休閒 transient RevPAR 年增約 7%（原話："transient RevPAR increasing approximately 7%"）
- 2026-07-30｜Mark Hoplamazian｜customer：商務 transient RevPAR 年增約 2%（原話："business transient RevPAR increasing approximately 2%"）
- 2026-07-30｜Mark Hoplamazian｜competition：管理層稱系統成本與最大對手相比具競爭力（原話："highly competitive, if not at a cost advantage to our"）
- 2026-07-30｜Mark Hoplamazian｜product：PMS 每房成本對業主下降 40%（原話："our PMS cost to owners has been reduced by 40%"）
- 2026-07-30｜Mark Hoplamazian｜commitment：已取消所有新開幕飯店的 IT 實施費（原話："we've removed IT implementation fees for all new"）
- 2026-07-30｜Mark Hoplamazian｜product：開發大型 AI 平台為團體業務評分（原話："a large-scale AI platform to actually score and"）
- 2026-07-30｜Mark Hoplamazian｜product：與 Dossen 簽署 Hyatt Select 中國大陸 master franchise 協議（原話："a master franchise agreement with Dossen Group"）
- 2026-07-30｜Mark Hoplamazian｜risk：UrCove 組合有部分飯店租約到期造成流失，租約約 10 年（原話："These lease deals tend to be 10 years in length."）
- 2026-07-30｜Mark Hoplamazian｜competition：交易市場焦點在高進入門檻市場的優質物業（原話："to-entry markets is what is garnering the most attention"）
- 2026-07-30｜Mark Hoplamazian｜guidance：特許加盟占比預期未來兩年不會顯著上升，五年後才明顯（原話："we will see franchise increase as a percentage of the total"）
- 2026-07-30｜Mark Hoplamazian｜customer：美國下半年比較基期受去年 Liberation Day 影響（原話："Liberation Day hit at the very beginning of the second"）

### H_Analyst_Investor_Day_Hyatt_Hotels_Corporation_20260528.md
- 2026-05-28｜CFO｜guidance：CFO 給 2025–2028 全球系統 RevPAR 複合成長區間 2%–4%（原話："RevPAR could grow at a compounded rate of between 2% and 4%"）
- 2026-05-28｜CFO｜guidance：淨房數成長 2028 前年複合 6%–8%（原話："rooms to grow at a compounded rate of 6% to 8%"）
- 2026-05-28｜CFO｜guidance：2025–2028 總費用（gross fees）三年複合成長 9%–13%（原話："a very strong 3-year compounded growth rate of between 9%"）
- 2026-05-28｜CFO｜guidance：調整後 EBITDA 2028 前三年複合成長 11%–16%（原話："3-year compounded rate of 11% to 16% through 2028"）
- 2026-05-28｜CFO｜guidance：調整後自由現金流複合成長 14%–18%（原話："compounded rate of between 14% to 18%"）
- 2026-05-28｜CFO｜margin：調整後 EBITDA 轉自由現金流轉換率約 55%，與 2022–2025 平均一致（原話："conversion of 55%, consistent with what we have delivered"）
- 2026-05-28｜CFO｜guidance：調整後 G&A 三年複合成長 2%–3%（原話："adjusted G&A to grow at a 3-year rate of between 2% to 3%"）
- 2026-05-28｜CFO｜guidance：Distribution 分部調整後 EBITDA 較 2025 年複合成長 2%–4%（原話："we expect adjusted EBITDA to grow between 2% and 4%"）
- 2026-05-28｜CFO｜guidance：key money 年均 1.5–1.7 億美元（原話："key money to average around $150 million to $170 million"）
- 2026-05-28｜CFO｜guidance：CapEx 年均 1.35–1.4 億美元，並預期之後下降（原話："CapEx to be between $135 million and $140 million per year"）
- 2026-05-28｜CFO｜guidance：有效稅率 27%–30%（原話："effective tax rate to be between 27% and 30%"）
- 2026-05-28｜CFO｜guidance：2026–2028 累計自由現金流 20–22 億美元（原話："between $2 billion and $2.2 billion of free cash flow"）
- 2026-05-28｜CFO｜capital_allocation：2028 年底前可增加 2–5 億美元負債並維持投資級（原話："capacity to increase our debt in the range of $200"）
- 2026-05-28｜CFO｜commitment：承諾維持投資級信用輪廓（原話："We remain committed to an investment-grade profile."）
- 2026-05-28｜CFO｜commitment：資產輕型盈餘占比 2028 年底可達 95%（原話："with the potential to increase to 95% by the end of 2028"）
- 2026-05-28｜CFO｜capital_allocation：董事會當天宣布庫藏股授權增加 10 億美元（原話："Board has authorized a $1 billion increase in our share"）
- 2026-05-28｜CFO｜capital_allocation：2022 年以來現金運用，回饋股東占比逾九成（原話："we've returned $2.1 billion or over 90% of"）
- 2026-05-28｜CFO｜capital_allocation：多餘現金優先走庫藏股（原話："we're going to return it through share repurchases"）
- 2026-05-28｜CFO｜capital_allocation：自有／租賃資產組合估值 22–25 億美元（原話："portfolio is valued between $2.2 billion and $2.5 billion"）
- 2026-05-28｜CFO｜capital_allocation：估值倍數 18–20 倍 2025 調整後 EBITDA（原話："multiple of 18x to 20x 2025 adjusted EBITDA"）
- 2026-05-28｜CFO｜commitment：持續評估減持自有飯店，無必持有之店（原話："there are no hotels we must own"）
- 2026-05-28｜CFO｜capital_allocation：三項特殊投資約 7 億美元，不含在 2028 展望內（原話："valued at about $700 million"）
- 2026-05-28｜CFO｜guidance：展望前提：總經成長穩定（原話："growth remains stable and consistent between now and 2028"）
- 2026-05-28｜CFO｜guidance：費用結構假設：九成獎勵費來自美國以外（原話："Today, 90% of our incentive fees are"）
- 2026-05-28｜CFO｜risk：CFO 稱 2026 年 Distribution 的干擾（颶風、墨西哥）屬暫時（原話："The disruptions in 2026, we believe are temporary."）
- 2026-05-28｜CEO｜commitment：CEO 稱展望 100% 以有機成長為基礎，併購為額外加成（原話："is all based on organic growth, period, end of story"）
- 2026-05-28｜CEO｜capital_allocation：併購不是第一優先（原話："nor is it our #1 priority"）
- 2026-05-28｜CEO｜guidance：展望內含的有機成長中，轉換型占約 35%–40%（原話："35% and 40% per year of conversions"）
- 2026-05-28｜CEO｜risk：新建案開幕過去較為遲緩（原話："new-build openings have been relatively more sluggish"）
- 2026-05-28｜CEO｜capital_allocation：正尋找銀行以外的非銀行融資管道（原話："we're looking for non-bank financial institutions"）
- 2026-05-28｜CEO｜risk：資本形成仍是問題，故轉換案是 6–8% 區間的關鍵（原話："capital formation remains an issue"）
- 2026-05-28｜CEO｜guidance：CEO 對 8% 高標不給保證，路徑取決於轉換加速（原話："we know for sure we're going to hit 8%"）
- 2026-05-28｜Laurie Blair｜commitment：擴大信用卡：未來 12–24 個月推出多張國際聯名卡（原話："several co-branded cards internationally"）
- 2026-05-28｜Laurie Blair｜guidance：信用卡與第三方費用 EBITDA 貢獻明年增逾一倍（原話："than double the EBITDA contribution from our credit card"）
- 2026-05-28｜CFO｜guidance：CFO：新卡擴張不在展望內，屬上行空間（原話："that will be upside to our outlook"）
- 2026-05-28｜CEO｜margin：CEO：資產輕型模式使利潤率擴張（原話："our asset-light model will enable margin expansion"）
- 2026-05-28｜CEO｜margin：CEO 對忠誠度滲透率口徑：滲透率高但利潤差「是愚蠢」（原話："with worse margins is idiotic"）
- 2026-05-28｜CEO｜margin：管理層改以淨房價實現率與利潤率為重點指標（原話："we are increasingly focused on net room realization"）
- 2026-05-28｜CEO｜margin：強調費用（美元）而非淨房數成長（原話："Net rooms growth doesn't create dollars."）
- 2026-05-28｜CEO｜competition：暗指同業部分淨房數成長是空熱量（原話："net rooms growth that's being reported is empty calories"）
- 2026-05-28｜Chief Commercial Officer｜competition：滲透率計算口徑與同業不同，不願同口徑比較（原話："we think about penetration through the owner lens"）
- 2026-05-28｜Chief Commercial Officer｜competition：Vondrasek 稱同口徑下差距遠小於近 50%（原話："we're a heck of a lot closer than"）
- 2026-05-28｜CEO｜competition：不進入輕經濟型與經濟型級距（原話："We're not in the lower mid-scale economy"）
- 2026-05-28｜CEO｜customer：約 70% 房晚經由 Hyatt 直銷管道（原話："70% of our room nights are booked through Hyatt's direct"）
- 2026-05-28｜Laurie Blair｜customer：自上次投資人日以來會員基數成長 78%（原話："our membership base has grown by 78%"）
- 2026-05-28｜CEO｜customer：Hyatt 客人每住一次花費高於同業 25%（原話："Hyatt guests spend over 25% more per stay"）
- 2026-05-28｜CEO｜risk：美國旅遊需求在不同收入層近期變異加大（原話："U.S. travel demand has recently shown more variability"）
- 2026-05-28｜CEO｜customer：科技業客戶迄今未見下滑（原話："We haven't seen a decline from that area to date."）
- 2026-05-28｜CEO｜product：Hyatt Select 首批物業在宣布後 8 個月開業（原話："first properties opened only 8 months after announcing"）
- 2026-05-28｜CEO｜product：Essentials 簽約量近期年增約 80%（原話："for essentials rooms were up approximately 80%"）
- 2026-05-28｜CEO｜customer：Essentials 簽約中 85% 為新業主（原話："85% of those signings are with new owners"）
- 2026-05-28｜CEO｜guidance：自 2017 年以來有機淨房數年均成長 7%（原話："Our organic net rooms growth was 7%"）
- 2026-05-28｜Chief Commercial Officer｜product：自 IDeaS 營收管理系統的營收提升（原話："has already delivered a 1.4%"）
- 2026-05-28｜Chief Commercial Officer｜product：意圖式搜尋轉換率提升 23%（原話："a 23% lift in conversion of intent-based search"）
- 2026-05-28｜Chief Commercial Officer｜product：ChatGPT 整合目前量體不大（原話："there is not a ton of volume here yet"）
- 2026-05-28｜Chief Commercial Officer｜competition：預期未來分銷轉向代理式 AI，直連意圖與訂房（原話："there won't be funnel, it will be a direct connect"）
- 2026-05-28｜CEO｜margin：AI 客服中心已省下數百萬美元並讓利給業主（原話："We took millions of dollars out of the"）
- 2026-05-28｜CEO｜commitment：AI 投資不會加到系統基金（原話："investments that we've been making in AI are not additive"）
- 2026-05-28｜Amar Lalvani｜product：Lifestyle 模式不需要增加人力或資本（原話："does not require additional headcount or additional capital"）
- 2026-05-28｜Javier Aguila｜customer：全包式渠道自有管道占 60% 銷售（原話："60% of our sales come from our internal channels"）
- 2026-05-28｜Javier Aguila｜competition：Inclusive 為該區隔最大營運商（原話："we are the largest in the segment"）
- 2026-05-28｜Javier Aguila｜risk：中東拓展須待地緣政治穩定（原話："we need to wait until the geopolitical situation stabilizes"）
- 2026-05-28｜CEO｜product：2.3 百萬間的全球可拓展房數（原話："We've identified approximately 2.3 million"）

### 問答異常語氣（迴避／改口／保留）
- H_Q2_2026_Earnings_Call_20260730.md｜問：Chaiken：Q4 開幕集中，是否已預先把部分房數移到 2027｜答法：先談兩年累計與 8 年有機成長、改強調費用成長而非房數，之後才說部分開幕可能延到 Q1
- H_Q2_2026_Earnings_Call_20260730.md｜問：Politzer：2027 淨增房數是否至少落在 6%–8% 區間中點或以上｜答法：回答 yes 後轉向歷史數據與管線，未給 2027 具體數字
- H_Q2_2026_Earnings_Call_20260730.md｜問：Montour：美國全年 3%–4% 隱含下半年明顯放緩，多少為保守｜答法：承認有保守成分，但未量化
- H_Q2_2026_Earnings_Call_20260730.md｜問：Duane：Q4 EBITDA 加速的驅動因素｜答法：列舉質化因素（颶風基期、G&A、Playa 季節性），未給金額
- H_Q2_2026_Earnings_Call_20260730.md｜問：Grambling：Dossen 與 Home Inns 協議的版稅率比較、UrCove 流失是否一次性｜答法：說明模式與租約年限，未回答版稅率，亦未明確回答是否為一次性，被時間打斷
- H_Analyst_Investor_Day_Hyatt_Hotels_Corporation_20260528.md｜問：Barclays：6–8% 再加速中，Essentials、轉換、新建各占多少｜答法：回答只給轉換案占 35–40%，未拆 Essentials 比重數字，改談區域差異與新建融資管道
- H_Analyst_Investor_Day_Hyatt_Hotels_Corporation_20260528.md｜問：JPMorgan：忠誠度滲透率約 49–50% 對比同業 65–70%，如何追上｜答法：質疑同業計算口徑，稱同口徑下「遠較接近」但不給調整後數字，並改談淨房價與利潤率
- H_Analyst_Investor_Day_Hyatt_Hotels_Corporation_20260528.md｜問：Baird：key money 1.5–1.7 億如何得出，新建與轉換、新增與防守各占多少｜答法：只答以現有合約加緩衝與小幅成長，未拆分新建／轉換或防守占比
- H_Analyst_Investor_Day_Hyatt_Hotels_Corporation_20260528.md｜問：Morgan Stanley：代理式 AI 對分銷、忠誠度成本及系統基金（同業降低提撥）影響｜答法：談分銷趨勢與免收啟動費用，未回答系統基金提撥率是否調降，僅稱 AI 投資不另加系統基金
- H_Analyst_Investor_Day_Hyatt_Hotels_Corporation_20260528.md｜問：Deutsche：Distribution 2–4% 為何不能回到 2024 水準｜答法：回答回到 2025 水準並略高，未直接回應 2024 水準，稱可能有上行

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
{"date":"20260520","verdict":"B（觀望偏進場；品質 A + asset-light 90% + 66M loyalty +18% + Pipeline 151K 新高，但 Fwd PE 34.8x 已 priced in 完整復甦，5Y PEG 2.05 接近警示；建議等 Fwd PE&lt;28x 或股價回測 W52 $151）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Lodging cycle 不在 2026-27 反轉，RevPAR 維持 +2-5% YoY","columns":{"2Y 驗證點":"2026 全年 RevPAR YoY +2-4% 達標 + 2027 H1 RevPAR YoY 仍 &gt; 0","5Y 驗證點":"2028-2030 跨完整 cycle 平均 RevPAR YoY +2-3%","10Y 驗證點":"2030+ 跨多次 cycle 全週期 RevPAR CAGR &gt; +2%","具體數字門檻":"FY26 guide 2-4%；下方 floor 連 2 季 YoY &lt; -2% → 反轉","信息來源":"Q1 26 8-K + FY26 mgmt guidance + STR Lodging report","漂移觸發":"連 2 季 RevPAR YoY &lt; 0 → 削弱；連 3 季 &lt; -2% → 反轉"}},{"id":"H2","text":"Loyalty + Pipeline 飛輪持續加速，Active Members &gt; 100M by FY28","columns":{"2Y 驗證點":"2026-27 World of Hyatt 會員 YoY +15%+；US Pipeline signings 連 4 季 +20%+","5Y 驗證點":"FY30 會員達 110M+；Pipeline 200K+ rooms","10Y 驗證點":"FY35 會員 150M+；luxury portfolio 全球 dominant","具體數字門檻":"Q1 26 66M 會員 +18%；下方 floor 連 2 季 YoY +10%","信息來源":"Q1 26 earnings release + Investor Day 2024-25","漂移觸發":"會員 QoQ 增量首次轉負 → 削弱；連 2 季 &lt; +10% → 反轉"}},{"id":"H3","text":"Asset-light 達 90%+ by 2026 完成；FY28 fee revenue 占 EBITDA 90%","columns":{"2Y 驗證點":"FY26 Q4 asset-light 80%+ → 90% transition；Playa 持續管理合約 $60-65M 增量 EBITDA","5Y 驗證點":"FY28 fee revenue 占 EBITDA 90%+","10Y 驗證點":"FY30 Hyatt 完全轉型為「hospitality brand manager」","具體數字門檻":"FY26 guide 90% asset-light；下方 floor 88%","信息來源":"Skift 2026/02 報導 + Q1 26 supplementary","漂移觸發":"asset-light 占比連 2 季 &lt; 85% → 削弱；&lt; 80% → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"消費衰退觸發 — RevPAR YoY 轉負，corporate travel demand 下降","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"STR US Lodging RevPAR YoY、Conference Board CCI、ISM Services PMI","警戒閾值":"連 2 季 RevPAR YoY 轉負；CCI &lt; 90；ISM Services &lt; 50"}},{"id":"R2","text":"Margin gap 擴大 — Marriott / Hilton 規模 + technology spending 拉大領先","columns":{"對應假設":"H2 + H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"MAR/HLT vs H Adj EBITDA margin gap; H technology spending / Rev","警戒閾值":"Adj EBITDA margin gap 從當前 5pp 擴大至 &gt; 8pp 連 2 年"}},{"id":"R3","text":"估值倍數結構性壓縮 — 市場對 asset-light premium 重設預期","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Forward PE multiple vs MAR/HLT；EV/EBITDA multiple convergence","警戒閾值":"Fwd PE 跌至 25x（-28% 倍數壓縮）or EV/EBITDA &lt; 18x"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":164.4,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/H_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
