你是 stock-analyst **v20 判斷 agent**，標的 HOOD（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"HOOD","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HOOD_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HOOD_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_total_net_revenues","label":"營收（GAAP total net revenues）","value":1424,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi1_gaap","label":"營業利益（GAAP，營收減總營業費用，衍生值）","value":685,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）；營業利益由營收1,424−opex 739衍生"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi2_gaap","label":"營業利益率（GAAP，衍生）","value":48.1,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）；衍生"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi3_adjusted_ebitda_gaap_non","label":"Adjusted EBITDA（非 GAAP，公司未報 non-GAAP 營業利益）","value":808,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi4_adjusted_ebitda_margin","label":"Adjusted EBITDA margin","value":57,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi5_gaap","label":"淨利（GAAP）","value":476,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi6_adjusted_eps_gaap_8_k_a","label":"Adjusted EPS（新揭露非 GAAP 指標，8-K/A 修訂版）","value":0.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi11_funded_customers","label":"Funded Customers","value":28.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi12_arpu","label":"ARPU（年化）","value":200,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[12]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi13_total_platform_assets","label":"Total Platform Assets","value":396,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[13]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi14_net_deposits","label":"Net Deposits","value":15.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[14]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_hood_gross_margin_pct","label":"HOOD 毛利率","value":81.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hood_operating_margin_pct","label":"HOOD 營業利益率","value":45.65,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hood_fcf_margin_pct","label":"HOOD FCF 利潤率","value":58.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_schw_fcf_margin_pct","label":"SCHW FCF 利潤率","value":52.27,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SCHW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ibkr_gross_margin_pct","label":"IBKR 毛利率","value":89.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBKR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ibkr_operating_margin_pct","label":"IBKR 營業利益率","value":86.25,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBKR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ibkr_fcf_margin_pct","label":"IBKR FCF 利潤率","value":135.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBKR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_coin_gross_margin_pct","label":"COIN 毛利率","value":71.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_coin_operating_margin_pct","label":"COIN 營業利益率","value":5.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_coin_fcf_margin_pct","label":"COIN FCF 利潤率","value":68.4,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi7_ocf_1_225_capex_21","label":"自由現金流（OCF 1,225 − capex 21，衍生，公司未報）","value":1204,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）；衍生"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi8_sbc","label":"SBC","value":80,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi9_sbc","label":"SBC 占營業利益（衍生）","value":11.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）；衍生"},"note":"未取得（無可靠共識來源，不填造）"},{"id":"f_kpi10_2026_adjusted_opex_sbc","label":"指引：2026 全年 Adjusted opex＋SBC","value":"2,675–2,750","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）；區間 2,675–2,750m（上緣下調 25m）；公司無 2026 營收／2027 指引"},"note":"未取得（無可靠共識來源，不填造）"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":86.27,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":12.66,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":31.48,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":2.11,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.37 → 2.42）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":3.35,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.28 → 3.39）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":4.55,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.18 → 4.37）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":2.42,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.39,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":4.37,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.76,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 2.31 → 2.42（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":39.74,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"2 個年度端點內的分位＝44.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":44.6,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":15.28,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝54.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":54.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":14.83,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝55.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":55.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":35.64,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 2.42，分子＝快照價 86.24","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-2277.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 22552.0、現金 24829.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":900.49,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":75367.86,"period":"2026-11-03","unit":"USD m","basis":"市值 77644.86 ＋ 淨負債 -2277.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":5317.03,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（27 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":6870.72,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（28 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":14.17,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 85.18 / W52 97.15 / W104 86.17 / W250 43.43 / W250 13週斜率 2.86%"},{"id":"f_ma_w52","label":"52 週均線","value":97.15,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":86.17,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":43.43,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.86,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列示競爭來源包括既有券商、金融科技、銀行、加密交易所與科技平台，多數對手營運歷史更長、資本更大；部分新興對手受較少監管。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm","excerpt":"Our current and potential future competition principally comes from incumbent brokerages, established financial technology companies, venture-backed financial technology firms, banks, cryptocurrency exchanges, asset management firms, financial institutions, consumer financial service providers and technology platforms.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q2 2026 Funded Customers 2,840 萬、年增 7%（含 WonderFi 約 30 萬）；管理層自述持續贏得市占，無獨立第三方市占數據。","source":"Robinhood Reports Second Quarter 2026 Results（搜尋摘要）","url":"https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-second-quarter-2026-results","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"預測市場領域競爭加劇：Interactive Brokers、Coinbase 等進入，Tenev 預期產業將整併；2026 年已有 10 家向 CFTC 申請 DCM。","source":"ingame.com: Robinhood CEO expect consolidation（搜尋摘要）","url":"https://www.ingame.com/robinhood-ceo-expect-consolidation/","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"LSEG 研究：散戶流量主要是週期性，但基準線永久性墊高（科技與溝通結構因素）。","source":"LSEG AIC research article: Retail volumes on higher baseline, show strong cyclical correlations","url":"https://www.lseaic.com/research-articles/retail-volumes-on-higher-baseline%2C-show-strong-cyclical-correlations","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"FM Intelligence：2026Q2 美國活躍散戶帳戶 739 萬，季減 0.4%、年增 30%；配對月成交量季減 7.3%，每帳戶成交量下降。","source":"Finance Magnates datalab: retail broker accounts hold at 7.4 million as volume per account falls 7%","url":"https://datalab.financemagnates.com/market-insights/retail-broker-accounts-hold-at-7-4-million-as-volume-per-account-falls-7","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"HOOD 2026Q3：淨入金 157 億美元（年化 17%），近 12 個月 710 億（21%）；資金客戶 2,870 萬（年增 7%）；平台資產 3,960 億（年增 19%）；Gold 訂閱 520 萬；10 月 MTD 淨入金逾 130 億含 60 億 Dell 一次性。","source":"Robinhood Reports Third Quarter 2026 Results (investors.robinhood.com)","url":"https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"加密營收 2026Q3 年減 55% 至 1.2 億美元、交易量年減 38%；預測市場合約 Q2 逾 136 億張、年增逾 10 倍，世界盃市場佔 Rothera 首月量約 93%（事件驅動）；Bernstein 預估預測市場 2028 年達 17 億美元。","source":"Analytics Insight / CoinMarketCap Academy (Bernstein) 報導","url":"https://www.analyticsinsight.net/amp/story/news/robinhood-crypto-revenue-drops-55-prediction-markets-surge","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：公司目前並預期未來持續受 DOJ、SEC、FINRA、CFTC、NFA、CFPB、州監管機關及英國 FCA 等國際監管機關的調查與檢查，可能導致禁令、罰款、和解。屬一般性揭露，未點名反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm","excerpt":"From time to time, we have been and currently are subject, and, given the highly regulated nature of the industries in which we operate, we expect that we will be subject in the future, to a number of legal and regulatory examinations and investigations arising out of our business practices and operations, conducted by the DOJ, SEC, FINRA, the CFTC and the NFA or other SROs or federal agencies","as_of":"2026-02-18","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋 DOJ／FTC／反壟斷相關結果僅回傳公司 SEC 申報（10-K、10-Q），未見反壟斷調查或拆分的第三方報導；監管風險集中在 PFOF／執行品質（紐約州檢察長自 2023-07 調查）與 Rule 605 新揭露規則（2026-08 起適用）。此為搜尋工具摘要，非逐字原文。","source":"SEC EDGAR 10-Q Q1 2026 / 10-K FY2025（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001783879/000178387926000062/hood-20260331.htm","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-Q 提及 Rule 605 修正案自 2026-08 起適用於 RHF/RHS，可能壓縮 PFOF 收入","source":"SEC EDGAR 10-Q Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0001783879/000178387926000167/hood-20260930.htm","excerpt":null,"as_of":"2026-10-31","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：關稅與貿易政策變動被列為影響市場波動、進而影響營運結果的外部因素（間接、屬市場情緒面），未見產品或供應鏈的直接關稅暴露。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm","excerpt":"financial market volatility (such as we previously experienced during the COVID-19 pandemic or have experienced and may experience in the future due to trade policy shifts and the imposition or escalation of tariffs implemented by the U.S. and other countries or blocs, including China, Canada, and the EU","as_of":"2026-02-18","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K 列出適用法規含制裁與出口管制（sanctions regimes and export controls）；公司依 OFAC 清單篩查客戶，違規存取制裁國家有執法風險。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm","excerpt":"Although our application includes features designed to block access to our services from sanctioned countries, if our services are accessed from a sanctioned country in violation of trade and economic sanctions, we could be subject to enforcement actions.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"新聞搜尋：2026年1月歐洲關稅消息日 HOOD 股價單日跌約1.6%；報導視關稅為總體情緒因素，未見針對公司自身成本或出口管制的描述。","source":"Barchart/Finviz 'Why Robinhood (HOOD) shares are trading lower today'","url":"https://www.barchart.com/story/news/37133665/why-robinhood-hood-shares-are-trading-lower-today","excerpt":null,"as_of":"2026-01-20","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 披露公司主要倚賴 AWS 提供平台服務（雲端單一主要供應商依賴）；無實體製造，無台灣/中國曝險之來源","source":"Robinhood Markets Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm","excerpt":"several cloud technology providers such as AWS (on which we primarily rely to deliver our services to customers on our platforms)","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險因子：倚賴第三方（清算系統、做市商、交易所系統等），這些供應商有營運、技術與資安弱點","source":"Robinhood Markets Form 10-K FY2021 (risk factor wording, reiterated in later 10-Ks)","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387922000044/hood-20211231.htm","excerpt":"We rely on third parties to perform some key functions... These providers are susceptible to operational, technological and security vulnerabilities","as_of":"2022-02-24","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"國際擴張帶來額外法規、經濟、營運與政治風險；業務涵蓋英國、歐盟、新加坡、杜拜（無亞洲製造/台灣中國曝險之來源，風險屬一般國際擴張語言）","source":"Robinhood Markets Form 10-Q Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0001783879/000178387926000167/hood-20260930.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 總營收年增 12% 至 $14.2 億；交易類營收年增 19% 至 $8.67 億（選擇權 $3.99 億 +31%、股票 $1.21 億 +41%、事件合約 $1.73 億、加密 $1.20 億 -55%）","source":"Robinhood Reports Third Quarter 2026 Results (investors.robinhood.com，2026-10-27)","url":"https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results","excerpt":"Total net revenues increased 12% year-over-year to $1.42 billion.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 淨利息收入年減 9% 至 $4.15 億，主因證券餘額下降；其他營收年增 61% 至 $1.42 億（Trump Account 服務與 Gold 訂閱）","source":"Robinhood Q3 2026 results (investors.robinhood.com)","url":"https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results","excerpt":"Net income decreased 14% year-over-year to $476 million, and diluted earnings per share (\"EPS\") decreased 16% to $0.51.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 管理層稱總平台資產年增 32% 至 $3,690 億，並持續在股票、選擇權、事件合約贏得市佔；未找到產業整體市佔百分比","source":"Robinhood Q2 2026 shareholder letter (investors.robinhood.com)，經搜尋摘要轉述","url":"https://investors.robinhood.com/static-files/0e3b7b58-a716-4bf6-a434-c8035af21a95","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Goldman Sachs 預估 Rothera（預測市場交易所）2027 年營收 $3.07 億；其預測市場預估高於共識 10%（2027）與 14%（2028）","source":"The Coin Republic，Robinhood stock price target raised to 142 on Rothera growth","url":"https://www.thecoinrepublic.com/2026/09/09/robinhood-stock-price-target-raised-to-142-on-rothera-growth/","excerpt":null,"as_of":"2026-09-09","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：新興科技公司不受同等監管，可能更快創新、承擔更多風險，使 HOOD 處於競爭劣勢；競爭者包含加密貨幣交易所與科技平台。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm","excerpt":"Some of our competitors, particularly new and emerging technology companies, are not subject to the same regulatory requirements or scrutiny to which we are subject, which could allow them to innovate more quickly or take more risks, placing us at a competitive disadvantage.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：HOOD 自述若跟不上快速演進的 AI 技術，競爭地位與經營結果可能受損。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm","excerpt":"If we fail to keep pace with rapidly evolving AI technological developments, especially in the financial technology sector, our competitive position and business results may suffer.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：金融服務業面臨快速技術變革（證券交易方式與加密貨幣的發展），HOOD 需推出包含事件合約等缺乏經驗的新技術產品。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm","excerpt":"Rapid and significant technological changes continue to confront the financial services industry, including developments in the methods in which securities are traded and developments in cryptocurrencies.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"分析師稱 Hyperliquid 等加密原生去中心化平台為 HOOD 商業模式的潛在威脅；亦有分析師認為零售客群為護城河。","source":"Stocktwits 新聞：HOOD Stock Drops Amid Market Sell-Off","url":"https://stocktwits.com/news-articles/markets/cryptocurrency/robinhood-hood-stock-falls-generational-company-hyperliquid-threat/cZmVxw4R7VG","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-Q 指競爭者可能放棄 PFOF，對 HOOD 的 PFOF 安排形成下行壓力。","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001783879/000178387926000167/hood-20260930.htm","excerpt":"In addition, our competitors might choose to forgo PFOF, which could create downward pressure on PFOF and make it more difficult for us to maintain our PFOF arrangements, which are a significant source of our revenue.","as_of":"2026-10-30","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q1 2026 Gold 訂閱用戶年增 36% 至創高 430 萬，訂閱營收年增 57% 至 8,500 萬美元，加密交易營收年減 47%","source":"Nasdaq: Robinhood Gold Hits Record Subscribers","url":"https://www.nasdaq.com/articles/robinhood-gold-hits-record-subscribers-bet-starting-pay","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Robinhood 預測市場原透過第三方交易所（主要 Kalshi）配送，正轉向自有交易所","source":"TIKR: Robinhood has lost 52% from its highs","url":"https://www.tikr.com/blog/robinhood-has-lost-52-from-its-highs-the-jpmorgan-tmc-conference-just-made-the-bull-case-harder-to-ignore?","excerpt":"Prediction markets became Robinhood’s fastest-growing revenue segment in 2025. The company traded 8.8 billion event contracts in Q1 2026 alone, a record. Until now, Robinhood routed those contracts through third-party exchanges, primarily Kalshi, absorbing distribution costs without capturing exchange-level economics.","as_of":"2026-05-25","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026 (10/27 公布)：公司將 2026 調整後營業費用＋SBC 指引由 $2.675–2.775B 收窄為 $2.675–2.75B（上緣降 $25M）；不提供 GAAP 總營業費用指引（監管費用不確定）。財報後盤後股價跌約 6%。","source":"Robinhood Q3 2026 results (investors.robinhood.com) / FXNewsGroup","url":"https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 EPS 與營收略低於市場預期：Decrypt 報導營收略低於約 $1.43B 預期，EPS $0.51 vs 預期 $0.55（各來源預期值不一致，另有來源稱 $0.55–0.64）。","source":"Decrypt: Robinhood misses Q3 earnings","url":"https://decrypt.co/382004/robinhood-misses-q3-earnings-crypto-prediction-markets?rand=52368","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"財報前分析師目標價分歧：BofA $156（10/5 自 $140 上調）、Truist $134（自 $130）、JPMorgan $115 Neutral（自 $103）、Wells Fargo $120 Equal Weight（10/14 自 $125 下調）；Koyfin 平均 $134.56（31 位）。查無財報後的目標價修正。","source":"Stocktwits / TIKR / 搜尋彙整","url":"https://stocktwits.com/news-articles/markets/equity/robinhood-gets-a-price-target-hike-from-truist-as-wall-street-s-earnings-outlook-improves/cZxBnkORBYg","excerpt":"Bank of America raised its target to $156 from $140 with a Buy rating on October 5, while Wells Fargo cut its target to $120 from $125 with an Equal Weight rating on October 14.","as_of":"2026-10-21","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"聚合站共識目標價分布大（as-of 不一）：MarketBeat 2026-07-20 約 $120（21 Buy/5 Hold）；TickerLeague $122.19（區間 $100–160）；TipRanks 平均 $144.29（高 $170、低 $68）。","source":"MarketBeat 2026-07-20 alert / TickerLeague / TipRanks","url":"https://www.marketbeat.com/instant-alerts/robinhood-markets-nasdaqhood-price-target-raised-to-16000-2026-07-20/","excerpt":null,"as_of":"2026-07-20","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06-16 宣布裁員約10%全職員工，預估現金重組費用約$20M、股權報酬約$8M","source":"SEC EDGAR 8-K Item 2.05","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387926000071/hood-20260616.htm","excerpt":"This reduction in force involves approximately 10% of the Company's full-time employees, and additionally involves the closure of a small number of open roles across the Company.","as_of":"2026-06-16","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06-25 完成$2.2B 0% 2029到期可轉換優先票據私募","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387926000077/hood-20260622.htm","excerpt":"The aggregate principal amount of the Notes sold in the offering was $2.2 billion, which includes $200 million in aggregate principal amount of Notes issued pursuant to the Initial Purchasers’ option to purchase additional Notes","as_of":"2026-06-25","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"Cash sweep 集體訴訟（Dey、Deeney）進行中，2025-04-28 法院部分駁回動議","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm","excerpt":"On April 28, 2025, the court granted in part and denied in part Robinhood’s motion to dismiss.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"financial_capital_credit_cycle#0","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"Q3 2026 總提列信用損失 $71M，去年同期 $26M（+173%）；信用卡相關 $23M→$61M，券商相關 $3M→$10M；前九個月 $163M vs $78M，部分被較低準備率抵銷。","source":"Robinhood Form 10-Q 期間 2026-09-30（SEC）","url":"https://www.sec.gov/Archives/edgar/data/0001783879/000178387926000167/hood-20260930.htm","excerpt":"Provision for credit losses 26 | 71 | 173%","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#1","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"財報稱因信用卡放款簿擴張，信用損失提列增加推高費用；公司不提供 2026 總營運費用展望，因提列與監管費用可能有重大影響。","source":"Robinhood Reports Third Quarter 2026 Results","url":"https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results","excerpt":"higher provisions for credit losses as we grow the credit card loan book","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"financial_capital_credit_cycle#2","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"二手來源稱信用卡 90 天以上逾期率自 2025 年底約 2% 升至 6%（未對照一手 10-Q，待核）。","source":"Panabee: Robinhood Earnings: Subscription Growth Meets Rising Credit Stress","url":"https://www.panabee.com/news/robinhood-markets-earnings-q3-2026-report","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_regulatory_capital_rules#0","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"+","claim":"HOOD 2026Q3 10-Q：券商子公司符合淨資本要求；RHS 淨資本 $4,212M 對要求 $491M，超額 $3,721M；RHD（FCM）$585M 對 $11M。","source":"Robinhood Markets Form 10-Q (quarter ended 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001783879/000178387926000167/hood-20260930.htm","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"financial_regulatory_capital_rules#1","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"SEC 交易與市場部 2026-02-19 發布 FAQ，說明支付型穩定幣在券商淨資本規則（Rule 15c3-1）下的處理；另 Rule 15c3-3 客戶保護修正合規日延至 2026-06-30。搜尋未發現專對線上券商的 2026 淨資本規則變動。","source":"Q1 2026 Regulatory and Compliance Update for Broker-Dealers (JD Supra)","url":"https://www.jdsupra.com/legalnews/q1-2026-regulatory-and-compliance-7145093/","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261103","affects":["thesis.R","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"+","claim":"完成收購加拿大 WonderFi，全現金每股C$0.36，約US$180M股權價值（2026-06-01）","source":"CTV News: Robinhood expands into Canada with acquisition of WonderFi","url":"https://www.ctvnews.ca/business/article/robinhood-expands-into-canada-with-acquisition-of-wonderfi/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Cash sweep 集體訴訟（Dey v. Robinhood、Deeney）進行中，求償金額未明","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm","excerpt":"In October 2024, RHM, RHF, and RHS were sued in a putative class action captioned Dey v. Robinhood Markets, Inc. et. al., in the U.S. District Court for the Northern District of California.","as_of":"2026-02-18","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"HOOD","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":81.44,"operating_margin_pct":45.65,"fcf_margin_pct":58.44,"rd_intensity_pct":19.34},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"SCHW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":52.27,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SCHW","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"IBKR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":89.97,"operating_margin_pct":86.25,"fcf_margin_pct":135.66,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IBKR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"COIN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.01,"operating_margin_pct":5.68,"fcf_margin_pct":68.4,"rd_intensity_pct":34.52},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"HOOD"},"financial_history":{"ticker":"HOOD","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":1358000000.0,"revenue_yoy_pct":null,"gross_margin_pct":56.7,"operating_margin_pct":-71.13,"net_income":-1028000000.0,"diluted_eps":-1.17,"free_cash_flow":-909000000.0,"fcf_margin_pct":-66.94,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":1865000000.0,"revenue_yoy_pct":37.33,"gross_margin_pct":92.17,"operating_margin_pct":-28.74,"net_income":-541000000.0,"diluted_eps":-0.61,"free_cash_flow":1160000000.0,"fcf_margin_pct":62.2,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2951000000.0,"revenue_yoy_pct":58.23,"gross_margin_pct":79.43,"operating_margin_pct":35.72,"net_income":1411000000.0,"diluted_eps":1.56,"free_cash_flow":-207000000.0,"fcf_margin_pct":-7.01,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":4473000000.0,"revenue_yoy_pct":51.58,"gross_margin_pct":83.34,"operating_margin_pct":46.81,"net_income":1883000000.0,"diluted_eps":2.05,"free_cash_flow":1584000000.0,"fcf_margin_pct":35.41,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HOOD/HOOD_Q3_2026_Earnings_Call_20261027.md）

# Q3 2026 Earnings Call
**Robinhood Markets, Inc.** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Thank you to everyone for joining Robinhood's Q3 2026 Earnings Call, whether you're tuning into the live stream or here with us in Menlo Park. With us today are Chairman and CEO, Vlad Tenev; CFO, Shiv Verma; and VP of Corporate Finance and Investor Relations, Chris Koegel. Vlad and Shiv will offer opening remarks and then open the call to Q&A. During the Q&A portion of the call, we'll answer questions from the audience, which includes institutional research analysts, finance content creators who may hold an ownership position in Robinhood and both institutional and retail shareholders.
As a reminder, today's call will contain forward-looking statements. Actual results could differ materially from our current expectations, and we may not provide updates unless legally required. Potential risk factors that could cause differences, including regulatory developments that we continue to monitor are described in the press release we issued today, the earnings presentation and our SEC filings, all of which can be found at investors.robinhood.com. Today's discussion will also include non-GAAP financial measures. Reconciliations to the GAAP measures we consider most directly comparable can be found in the earnings presentation.
With that, please welcome Vlad.

**Vladimir Tenev** (Executives):
All right. Thank you guys for coming. This is awesome, and it's great to see so many people in person. We're back at our headquarters in sunny Menlo Park. So thank you again for being on this journey with us and showing up in person and to everyone watching remotely.
So as you probably know, at Robinhood, we have a singular goal. We believe in ownership. We want to make everyone an owner. And we think that broad ownership is actually essential to a free, stable and prosperous society. So in order to execute on this vision, we have our three-part strategy. So to recap that, the first part, we want to build the #1 active trader platform. So we want to allow customers to own any tradable asset. And really an active trader should feel like they're at a disadvantage trading elsewhere. So we'll have more about that later. Second, strategic arc, #1 in wallet share for the next generation. So we want to build our customers' financial home and not just for them, but for their families as well.
Then the third, #1 global financial ecosystem. So take the ownership that we've been able to deliver and grow in the U.S. and expand it everywhere around the world. Q3, we made a lot of progress. So our product velocity continued across each of these three arcs, and we saw strong business and financial results. So for active traders, again, the idea is if you're an active trader, you're at a disadvantage trading elsewhere. 
So what have we done for active traders? Last month, we held our third annual HOOD Summit event in Houston, Texas. And we launched not 1, not 2, but 17 new products and new services to our customers. So I'll hit a couple of highlights. Agentic Trading, which is near and dear to my heart, literally, I'm wearing the vest right now. So our agentic offerings have really increased in scope over the course of the year. If you remember, we started with our MCP, which has grown quite well. And now we've got Agentic Trading directly in the app, so you no longer need to use your external tool like your Claude Code or Codex. You can do it within the app.
And we've also allowed customers to extend their MCP connectivity to Robinhood Legend. So Robinhood Legend is now in scope for our MCP connectors as well. So we're just continuing to make it easier for anyone to trade on our platform, whether it's you directly or your agent. And while we're still very early in the in-app capabilities and the harness tooling, we've been seeing really strong early adoption across the entire suite of agentic products. So customers have over 250 million in agentic accounts.
Remember, this is -- the account start at zero. So you have to make a choice to move money into them. And we look at the adoption curves, both across usage and trading, and they're sort of following an accelerating curve, which gets us very excited about the future of these products. And as we continue to add more asset classes, more features, those curves appear to be steepening.
Next, perpetual futures. So we became the first U.S. broker to offer what we call true perpetual futures. So these are perpetuals powered by our global derivatives exchange Bitstamp, and they settle continuously around the day. So 15-minute settlement. We're also working on adding earnings contracts to our prediction markets hub. I think this will be particularly relevant for this audience because they'll allow you to trade EPS and revenue on individual companies as well as KPIs that are company specific. And of course, something I've been very excited about for quite some time. We announced 24/7 equity trading that will be coming to Robinhood later this year. And again, this is something -- I think we'll be the first to offer this as well. And these are just a few of the many items we've shipped. So there's a lot more, and I encourage you all to check out the full keynote on YouTube or X if you haven't already.
So let's move to wallet share. A couple of things that I'd like to highlight here. Trump accounts achieved a really important milestone in Q3, auto enrollment. So as we said before, we've got nearly 70 million children in the U.S. under the age of 18 that are eligible for the Trump account. And now the U.S. Treasury has opened accounts for all of them, for all these children. And because of the generous gift from Michael and Susan Dell through their foundation, 25 million of those children already had $250 invested for them by the Dell Foundation. So we're excited about this initiative. It's one of those things where it's just been snowballing and we're doing more. So there's just a ton of road map ahead. One of the things I'm particularly excited about is I think it can become the default vehicle for philanthropic giving in this country, right? And we're already seeing the beginnings of that with the Dell's, but also the other donors. And we don't really have a great default option. I think Trump accounts can become that. So we're going to be doing more there in partnership with BNY and the U.S. government.
We're also continuing to make progress with Robinhood Gold, which today is one of the largest paid membership programs in consumer finance in the U.S. So a couple of years ago, we set out to actually completely revamp our Gold product. And what we wanted to do is put something in Gold for our mass market customer so that you didn't have to be an active trader to benefit from Gold. And I think we've been able to achieve that. So in this quarter, Robinhood Gold reached 5 million subscribers. okay? We see it really paying off. We see it paying off. We've got 5 million Gold subscribers. And that's up over 30% year-over-year, and it's a 4x increase from when we began the journey to revamp the Gold program just about 4 years ago. So that gets us to about an 18% overall Gold adoption rate when you look at our customer base, but 40% if you look at in quarter. So of the customers that joined Robinhood in quarter, much higher adoption. And that's really great to see because then we see a path as we continue to grow, Gold will just continue to increase. And I think there's actually much more room to grow.
Our big bets for growing the Gold value proposition are banking and credit. And those are still despite getting to large scale, not generally available yet. So there's still limited release. And we've been really investing in more integration points. So things like easy sign-up for banking and Gold Card if you're signing up for Robinhood, contextual upsells so that we detect when banking and credit is going to be appropriate for you when you're using the Robinhood app and kind of putting it there. So we think we've got plenty of room to run. These can become even more meaningful drivers of higher Gold adoption.
Finally, let me get to global financial ecosystem. So on July 1, just a few months ago, we launched the Robinhood Chain Mainnet. And in its first quarter, it's already a top 5 chain by volume and revenue. So far, we've seen over $100 billion in DEX volume. So it's $100 billion in decentralized exchange trading volume and over $50 million in chain fees. DeFi perpetuals, it's an interesting innovative product, have seen solid growth on the chain as well. So in recent weeks, we've been seeing DeFi perpetuals volume of over $1 billion per day on the chain. So it's clear customers have demand for these tokenized assets on chain.
And we think we not only believe we're building Robinhood Chain to be the best place to own and trade all of these tokenized assets, of course, starting with stock tokens and perpetuals, but expanding much broader from that. We're also expanding our brokerage infrastructure globally. And we're excited with that to announce that we received authorization from the Dubai Financial Services Authority to launch Robinhood in the region. This will broaden our international footprint even further. The product velocity that you've been seeing and the focus on the customer experience have led to really strong business results.
Market share continues to grow, up double digits year-over-year for each of the main assets, equities, options, crypto and margin as well. Revenues grew 12% year-over-year to a record $1.4 billion. Adjusted EBITDA, that's up 9%, record of over $800 million. And then net deposits, $16 billion in quarter. And with a strong start to Q4, which Shiv will talk more about, we have already exceeded our annual goal of 20% net deposit growth, and that's with 2 months left to go. So we're pleased with the strong results for our customers and for our business. We're pushing hard to make Robinhood your financial super app.
So with that, I'll ask Shiv to come up. How are you doing, sir?

**Shiv Verma** (Executives):
All right. All right. So thank you, Vlad. Before we get into the results, I just wanted to share 3 big takeaways from Q3. First, as Vlad said, the core business is firing on all cylinders. This led to our highest quarter ever for both revenue and adjusted EBITDA and really great to see platform assets were nearly $400 billion. And on top of that, we set new records for equities, options, event contracts and margin. So going well all around. Second, our product is driving a more diversified business. We're now up to 14 cylinders that have reached $100 million or more of annualized revenue as Rothera, our prediction markets exchange, hit this number in just its full -- first full quarter of operations. So really nice to see Rothera scaling well. And then finally, we drove another quarter of strong growth, profitability and scale. So we're a Rule of 80 company, but at our scale of over $5.5 billion of annualized revenue. So we remain disciplined on expenses even while investing for growth, which is fantastic to see.
So let's get to our Q3 results, and all of these will be compared to a year ago. So revenues were up 12% to a record $1.4 billion, and this was driven by strong growth in both new products and existing products as well. Transaction revenues were a record as trading volumes were new highs across equities, options and margin. Each of these was up around 50% year-over-year, and this was on market share gains. And the event contracts continue to scale really nicely. This was up 7x year-over-year. Additionally, the Robinhood Chain in its first quarter of adoption saw really strong usage, as Vlad mentioned before. So that was another driver of transaction revenue in the quarter.
And then on NIM or net interest revenues, really strong growth in margin, credit card book and Robinhood Banking, and these grew to new record balances. And our total interest-earning assets on the platform also hit new highs. So really nice to see both transaction revenue and the interest-earning assets do well. And then finally, in other revenues, as Vlad shared before, Gold subscribers reached a new all-time high of over 4 million subs, which is great to see. And then additionally, as we continue to build and expand the Trump accounts for customers, that generates some additional revenue as well. 
And so while revenues grew to a quarterly record, we also see discipline on costs. And so adjusted OpEx and SBC was managed to $664 million. This was managed within our prior outlook range. And again, as we're investing for growth, we're still being really, really disciplined on our expenses. And our productivity also continues to do really well. So in this quarter, we hit revenue per employee of nearly $2 million, which would be a new record. So we're shipping for customers, but we're also doing it in our lean and disciplined way. 
And then finally, as we look ahead to Q4, while we plan to continue making growth investments, in particular, in the Trump accounts, we're also controlling our expenses and have driven more efficiencies across our business. So as we do that, we're going to lower the top end of our prior outlook range by $25 million, and we now expect full year adjusted OpEx and SBC to be between $2.675 billion and $2.75 billion, and this is $13 million lower at the midpoint versus our prior outlook. So you put them together, really strong top line growth, expense discipline, and this led to a strong quarter of profitability. So adjusted EBITDA was a record $808 million. This is up 9% year-over-year, and adjusted EBITDA margin continues to be strong at 57% in Q3.
EPS for the quarter was $0.51. Now this includes a minus $0.07 of mark-to-market impact on investments that we hold. And so as we talk about EPS, we're continuing to expand our business into investments. One of them is such as Robinhood Ventures. And as we launch more and more of these products, we're now seeing some nonoperating movements on these investments. So we're introducing adjusted EPS, and this is to just better reflect our core operating profitability before any gains or losses on investments or some of these other nonoperating items. But at the same time, we're going to remain accountable for all of our regular ongoing costs. So we're still including normal course SBC in our adjusted EPS. As I've said before many times, share count and the denominator matters. And so you put it all together, in Q3, adjusted EPS was $0.60. And so moving forward, we hope that investors find this a useful measure of our core profitability in the business.
Another area I wanted to touch upon is prediction markets. We believe it's really early innings for the asset class, and we're investing to be a leader in the space. We're constantly improving the in-app experience. We now have a vertically integrated exchange with Rothera. And as I mentioned before, it's off to a great start. Additionally, we also announced a recent partnership with Crypto.com and OG.com. Now this is really exciting for both our customers, but also for our business and shareholders. It's really important for us that customers have a best-in-class selection with consistent pricing across exchanges and with these partnerships that now allows us to do that. But additionally, with no cash outlay, we received an initial 1% equity ownership stake in Crypto.com and OG.com. And we have the ability to earn up to 10% ownership depending on how much we partner together in the years to come.
So before we move to Q&A, I just wanted to give a little bit about how Q4 looks to start following a record Q3. October net deposits are over $13 billion in the month, great to see, and that includes $6 billion of the Dell family gift to Trump accounts, as Vlad mentioned earlier. And this brings our total year-to-date net deposits to over $68 billion. This is already a new annual record and north of our 20% growth target with just a few months -- with still a few months to go left in the year. And then compared to Q3, average daily volumes for equities, options and cryptos are off to a good start and are about 5% lighter relative to the really strong Q3. And then event contract ADVs are already up about 10% to start the quarter.
So stepping back, it was great to see another strong quarter in Q3, and we're really excited about our momentum entering Q4. And as we've shared before, our financial North Star remains the same, maximize earnings per share and free cash flow per share for shareholders over time.
All right. Chris, Vlad, should we take some questions?

**Chris Koegel** (Executives):
All right. Thank you, Shiv.

**Vladimir Tenev** (Executives):
Let's do it.

**Chris Koegel** (Executives):
For the Q&A session, we'll start by answering shareholder questions from Say Technologies. And after the Say questions, we'll turn to live questions from our audience and then go to the dial-in queue. 
So I'll kick it off with our first question from Say, which comes from Bo Shen. Okay. I think we've lost Bo. So Bo asked, how is the expansion into banking going? And when will features such as the Zelle replacement arrive?

**Vladimir Tenev** (Executives):
It's a great question. So I thought rather than talking about it, I'll actually just show you. I try not to launch new products during earnings, but I thought since we have a crowd here, I might as well give you a little bit more. By the way, before I get into it, I do want to say one thing about banking as it pertains to our super app vision. So one of the things we've been tracking for a really long time is what the top bank withdrawal destinations for our brokerage business have been. So this is the top institutions that people actually move money from brokerage into banking. And for the longest time, it's been kind of the expected big banks, not a huge surprise there. But as we've started to roll out Robinhood Banking, we've actually seen Robinhood Banking climbing up the list. And this quarter, for the first time, Robinhood Banking became the #1 withdrawal destination for Robinhood brokerage customers.
This is actually even before it's generally available. So it is the #1 bank that customers withdraw money to by dollars, which I think is quite amazing. And obviously, we love this because that money is not leaving the Robinhood ecosystem. It just stays in people's accounts. And I think it's one major proof point that customers are choosing Robinhood for their totality of their financial needs. They're coming in, they're direct depositing their paycheck. They have their checking and savings account. Of course, they move money to invest and trade. They do their spending with Gold and now Platinum. So increasingly, you don't really have to leave Robinhood because we offer best-in-class services kind of across the board.
Now one thing that people have been asking about is peer-to-peer payments. And of course, we didn't want to just do like a regular add-on bolt-on peer-to-peer payments feature. We wanted to make it really, really nice. So if you guys are ready, I can share my screen. So this is Robinhood Banking. So I've blurred out my balances. This is the new design, by the way. We've updated it to have the liquid glass UI. So there's this button on the bottom right, which is kind of your overall transaction action button. And if you open that, you see there's this new send money feature.
So, Matt, can I send you -- would you accept a few dollars for me?

**Unknown Executive** (Executives):
Sure. Yes, I don't know how much you like me based on how much you send.

**Vladimir Tenev** (Executives):
Okay, good. You know I like you a moderate amount. So it's just as simple as that. I'll send Matt, who's been doing a great job from our Investor Relations team, $5 from my joint checking account, okay? And you can put a little message here. Of course, this is my favorite one. And so check this out. So I'm going to send it via text. One of the really annoying things about peer-to-peer payments, I don't know if you guys have experienced this, but you want to use an app and the person you send money to doesn't have it, which creates this like moment of friction. I don't want them to have to install anything. And then they'll ask you, can you send it this way? Can you do it with one of the competitors? And then you have to install it. Anyway, we've gotten rid of all of that, Matt, if you -- did you get it?

**Unknown Executive** (Executives):
I got the text.

**Vladimir Tenev** (Executives):
Okay. If you want to show, so there it is, he just taps on it, and you can accept money with Apple Pay or Google Pay without even having a Robinhood Banking account, which is pretty awesome if you think about it. Of course, it gives us an opportunity to upsell Robinhood Banking, which is just a really clean experience for those of you that have tried it, but you don't have to have it. You can just get it right into your Apple Pay. So you don't have to worry about that friction of the recipient of the funds.
So right now, still in limited release. If Matt sends money to someone, they'll get it. But yes, you should expect to see us rolling this out much more broadly in the coming weeks. And just another reason why everything we think can be better on Robinhood if you do more and more of your -- if you run more of your financial life through us.

**Shiv Verma** (Executives):
Who needs Zelle, right?

**Vladimir Tenev** (Executives):
Yes. I mean legacy technology, I think we can do better if we build everything in an integrated fashion.

**Chris Koegel** (Executives):
All right. Great demo. All right. So the next question is from Marcus M, who asks, how is global expansion going? And what countries are next?

**Vladimir Tenev** (Executives):
Yes. So I'll field that one. So when Shiv and I were kind of coming up with our plan and we thought what can Robinhood be in 10 years, we called our third arc global financial ecosystem. And we -- our vision, and I think this is backed up by how big these markets are and also sort of like wealth accumulation, people outside the U.S. keep getting wealthier. Our vision is that over the long run, more than half of our business should be outside the U.S. And cut another way, more than half should be institutional. And what we didn't anticipate is products like Robinhood Chain, right?
And we said Robinhood Chain already in quarter got out of the gate really quick with $100 billion in DEX volume and $50 million of chain fees, right? And you think about how much -- and we're actually continuing to invest, frankly, the growth of the chain and associated ecosystem and the wallet surprised and sort of like -- was higher than our expectations. And so now we're spending a lot of time investing in how to make that even bigger, how to support the community. We know we've been hearing from a lot of builders that we could be doing more to support the community. And I think you should expect to see us really ramp that up because we want to make it the best developer ecosystem as well as the best sort of global on-chain community.
So yes, you should expect to see us ramping the investment because you just don't see growth of a new ecosystem like this. It's an uncommon thing. I mean a lot of chains have launched over the past few months that have just had not nearly like an incomparably small level of traction compared to this. So we're doubling down on that. And of course, as I mentioned earlier, we're expanding into MENA with our Dubai license, and we did get in principle approval from MAS to expand into Singapore, and that will be our Southeast Asia APAC hub, which we're very excited about. And by the way, we're continuing to get deeper in our more established markets of EU and U.K. U.K. now has crypto and brokerage in the same offering. So it's getting to parity. And you've seen us actually increasing our download share and getting more traction there.
So it's -- I would say, Shiv, I don't know if you would disagree, I think like for a while, our international business was sort of like a future -- very like far off into the future when we expected to see meaningful contributions. But we're starting to see that accelerate. And I'm seeing the most traction I have. So I feel probably the best that I've ever felt, and we're kind of accelerating so much in momentum there.

**Shiv Verma** (Executives):
No, I agree. We built a 10-year plan. It's nice to see the seeds coming. And also Canada, you forgot to mention that as well. We're now...

**Vladimir Tenev** (Executives):
Yes, Canada with the crypto business through the WonderFi acquisition there for sure. So pretty soon, we'll have Robinhood all over the world.

**Chris Koegel** (Executives):
All right. Our next question comes from a special guest. You may have seen him driving the Robinhood neon car during the last two NASCAR seasons, 3-time Cup Series race winner and driver of the #23 Toyota for 23XI racing, Bubba Wallace.

**Unknown Attendee** (Attendees):
Are there any new major product plans for 2027 that could increase Robinhood's revenue?

**Vladimir Tenev** (Executives):
No easy questions, Bubba. He's just getting right into it. Yes. And by the way, it was fun watching Bubba compete at the Las Vegas Motor Speedway a couple of weeks ago, hot, but I don't know how he does that for so long. So I would say one of the things that I think people find attractive about Robinhood as a business is that it's a financial compounder, right? Even if you look at the core business of equities, options, crypto, margin, we're continuing to gain in market share. We get more customers. Those customers get wealthier as they get older. The market appreciation adds to that. So all of this is leading to total platform assets this quarter of about $400 billion. And I don't think it will be long before we're talking over $0.5 trillion and, knock on wood, into the trillions, right? 
So just the core brokerage business and the crypto business has been remarkably strong. But we're not just like being complacent and seeing we have a strong core business. We're moving at incredible pace, not just adding all the products and features that our competitors have, but also, I think, just leading the industry across a couple of major domains. I mentioned Agentic Trading earlier. I think Agentic Trading, I don't think there's really another game in town in terms of financial companies that are really investing in Agentic Trading and making that a first-class experience. So I think we're at the very beginning there, and we're just continuing to invest in making the product experience really, really good. We've talked a lot about prediction markets. I'll also throw in perpetual futures. I mean we're super early to that, right? A lot of companies announce plans to offer these new assets, but we announce and then we ship and we roll out. We're seeing strong traction. That's another asset class where we expect to be the leader and gain market share.
On the wallet share front, you've heard me talk about Trump accounts. Robinhood Ventures is another one where it's just other companies aren't really doing this where they're trying to -- they're going after the vision of democratizing private markets for retail investors. So we have RVI, RVII shipped, and you should expect even more. I mean we are just -- we're really investing because we think it's important, and it's a big business opportunity, a new category that I think we can own. And then, of course, long term in the global financial ecosystem, tokenization and Robinhood Chain and Robinhood Wallet are unique products where it just really feels like we've got the tiger by the tail. So those are kind of several areas, not just one where we think we can surprise to the upside with the product bets that we're making.

**Chris Koegel** (Executives):
All right. Thank you, Vlad. That concludes our Say Technologies questions. And now I'd like to go to questions from our live audience. So if you'd like to ask a question, please raise your hand.

**Shiv Verma** (Executives):
[indiscernible] later stages of the pipeline and then [indiscernible].

**Chris Koegel** (Executives):
Can I get a mic over to Hayden? Over here.

**Unknown Analyst** (Analysts):
I know you've got active trading and you've got the strategy side of things. What are you doing to focus on the middle ground of customers who just kind of want to deposit and forget about it?

**Vladimir Tenev** (Executives):
Yes, that's a great question. Actually, that's one thing I forgot to mention. I think Robinhood strategies which is our passive digital advice product. So over $2 billion in assets. It's been growing really quickly year-over-year. I think it's a bit of a dark horse just because we launched so many things. And I think the active trading products tend to get a lot more attention and mind share, but we have all these amazing passive products, strategies being one of them that provides a best-in-class experience. So we've been continuing to add things to the product suite.
We have this tool, Smart Income, which is part of Robinhood Strategies, where you basically just like can just really easily with a slider, just slide your time horizon and risk tolerance, and it will tell you what the sort of like expected return for your investments would be. And then the idea is you just put money in there, you drop money into that account, and it's a complete set it and forget it product. And then I think we've got some things like that team has ambitious plans. There's a bunch of things that we're working on to make that even better. So suffice it to say, strategies isn't staying still. I think that's -- it's a dark horse product. I think it's one that could surprise people in the coming year.

**Chris Koegel** (Executives):
All right. Thank you, Vlad. Next, I think, Hayden, did you have your hand up? Yes. Get a mic to Hayden.

**Unknown Analyst** (Analysts):
We've been really impressed by the product velocity and traction at Robinhood, the 14 cylinders over $100 million. Can you speak to how many products your power users engage with versus your average user? And what would it mean for your business if you're able to convert the majority of your customers into power users?

**Vladimir Tenev** (Executives):
Yes. I mean that's a great question. We look at this internally quite a bit. And we sort of see that basically the more products that someone uses, once you get up to three or four products in the Robinhood ecosystem, the average revenue per user and the engagement just continues to increase with three or four products being really kind of the sweet spot. Also, we can cut it by asset classes. A lot of people come to us to trade equities or crypto first. But then if you look at the customers that trade equities, crypto options, futures and prediction markets, the revenue and the engagement with the platform really increases. And we've been making a lot of investments, maybe those of you that use Robinhood have been seeing our work there and just making the app more coherent and more discoverable. This is something I mentioned in the last earnings call. We have more work to do because we have all these products, how can we make sure that the app is coherent and that you kind of understand what we're about.
Well, I think you're starting to see some of that progress because our shared services, including social, search, home, I think we're doing a much better job in kind of surfacing relevant content to you. I think the focus has been on making sure prediction markets works really well because we're kind of doing a unique thing like combining this new asset class with other tools that are sort of like personal finance centered.
But I think you'll see us continue to invest in personalization and making it easy to discover things in subject to all the rules and regulations, being able to surface relevant content to customers. And I think that's another area where we're best-in-class and continuing to get better.

**Shiv Verma** (Executives):
If you want to look in terms of how big it could be, I think Gold is the best way to see it. So Gold, we don't view it as a subscription product. We view it as a loyalty product. And what you see is a customer comes for something. It doesn't matter whether it's an equity, an option, a crypto, an event contract. They discover Gold, they then use more products. They then deposit more, they engage more, they trade more. And so for how big it could be, it's great. We have 5 million customers. It's only an 18% attach rate. And about 40% plus adopt it when they first come in, but there's still a large runway ahead of that.

**Chris Koegel** (Executives):
All right. Thank you. Next question.

**Unknown Analyst** (Analysts):
What is Robinhood's strategy for educating customers about active trading products like perpetual futures or Agentic Trading?

**Vladimir Tenev** (Executives):
Yes. I think that what we really try to do is make the products themselves understandable and clear within the app. And I think with our various learning modules and tools, we've done a really good job at taking advantage of the limited real estate of the app and giving people the information they need at the time that they onboard without just like the -- too much of the fluff and filler.
Now as we expand into the agentic products, and actually, one of the reasons I'm excited about Agentic Trading and our investments there is that a lot of our customers are using that as an education tool because these AI agents are really good. If you just ask them, hey, explain this to me. What is a wheel strategy? What is an option -- like what are the typical options trades? You can say, hey, I have this like plan, this point of view, can you break down, give me like the top 3 ways to capitalize on that. So I think there is strong potential, and we're actually seeing a lot of customers doing this of just explaining things, not even just placing the trade or fully trading autonomously, although we're pushing ahead in that direction, too, but just taking some of this complexity and kind of breaking it down for the customer.
So yes, the plan is really each interface has somewhat different affordances. On mobile, it's really about how do you like clearly articulate what the functionality is, what it's for, how do you make it so that with as few taps as possible, you can actually do what you want to do as a customer. Web, I think you have a little bit more of like real estate to browse. And I think agentic lends itself to like a back and forth, which is difficult with all of the interfaces. But yes, I mean, we're making a ton of progress on all of these simultaneously.
And I think the other thing we recognize is we do -- I mean we do produce some first-party educational content, video and so forth. But we also want to make it easier for you to discover all the great content that's out there. So I mean, there's just so many content creators and influencers that are making YouTube videos and they're quite entertaining. So one of the things we've been trying to do is can we make it easier for you to get some of those things in the right way through the experience, too.

**Shiv Verma** (Executives):
You also have Robinhood Social as well, where you can learn from the community each other. So just another surface for customers to talk to each other.

**Vladimir Tenev** (Executives):
Yes. And that's a great point. I think I'm much more bullish on our ability to surface third-party user-generated content to you because we just have many more passionate people that can make it. So some of the content on Robinhood Social that we're seeing is actually like very deep investment analysis. And we've been working hard, giving people more tools to like share charts, share different data sources. And yes, I think we like what we're seeing there. So we're going to do even more.

**Chris Koegel** (Executives):
All right. Any other questions from the audience?

**Unknown Analyst** (Analysts):
Does Robinhood plan to get into like exchange funds like Cache and Titan? There's a lot of money that's locked in into other brokerages, which you don't want to sell. So having the ability to trade without selling can be a very big upside for Robinhood.

**Vladimir Tenev** (Executives):
Yes. And I talked a little bit about Robinhood strategies. And I think certainly, helping customers with concentrated positions to diversify and handle that in a tax-efficient way is something that we've been looking very carefully into. And the other thing is a lot of these products that are offered by the incumbents have really high minimum requirements. So of course, whenever we see that, we ask ourselves, is there an opportunity to create a really, really nice product and make it available to lots of people.

**Chris Koegel** (Executives):
All right. Any other questions from the audience? Okay. With that, let's move to the Zoom Q&A. So I think the first question we have today is from Devin Ryan from Citizens.

**Devin Ryan** (Analysts):
Question on Robinhood Chain. Obviously, great to see early traction there. Also appreciate it benefited from some congestion in late August and September, which helped gas fees. So maybe seeing some normalization in fees there. But volumes have been still pretty resilient.
So my question is really just how should we be thinking about the financial opportunity over time? And really, what we should be looking for to drive maybe that next real inflection in activity? I know you mentioned perpetual is gaining traction. So maybe that's one example. But is it just more products being developed? You mentioned Robinhood can do things to support the chain. I'd love to hear about that. And then just bigger picture, too, can monetization improve over time without making the chain less competitive?

**Vladimir Tenev** (Executives):
Yes. I mean I'll start. Maybe you can hit your thoughts on monetization. So another thing we look at for the chain that gets us so excited is developer activity. So I think last time I checked, we were #1 in on-chain developer activity. And so developers are actually coming to Robinhood Chain because they see the traction that we've had, and they're making a bet that this is kind of the ecosystem that they want to invest in for their activities.
And I think at the end of the day, the ecosystem is actually going to be driven by the developer activity. People haven't had very much time to build sophisticated on-chain applications yet. So that's why I think in the first instance, the applications that you've seen are relatively simple launch pads and linked pools and things of that nature. And people are working on really interesting things now that are more complex that connect stock tokens with crypto assets and technology. And just sort of imagine if you take a stock token and make it fully programmable, just like software, what can you do? I mean, can you have tokenized options contracts, for example? Can you have products that we haven't seen before? So that's why we want to invest in the developer ecosystem.
I think it's interesting, the whole fees and congestion and revenue. When Johann, who's our crypto GM and I talk about this, basically, we both agree that the most important thing to prioritize is a great experience for our users. So I don't really want to be in the business of like charging high fees for on-chain usage. What I'd rather do is gain the market share, make the developers choose us as the best chain, give them more products. And I think we have a pretty clear road map for what first-party products we need. Yes, the idea is anything that you can trade on Robinhood in the U.S. wherever possible should be made available on on-chain versions for our international customers. So it's more stock tokens, but then expanding to other asset classes and making sure that these things become like LEGO building blocks that developers can incorporate into their on-chain applications. And since we offer the primitives, one of the reasons stock tokens have been so successful is people know that Robinhood stands behind them, and that makes it much more likely that they trust them in their applications than just some third party.
So we're going to continue to execute on that. And I think the way we're tracking long-term sustainability is we obviously like to see DeFi TVL go up, but we're specifically looking at -- we're specifically looking at stock token TVL, making sure that's on a healthy trajectory, and we have a path there because I think our differentiator with the chain and what's been working well for us is real-world assets. So we should expect to see real-world assets adoption just continue to increase.

**Shiv Verma** (Executives):
On monetization, only piece I'll add is it's about $50 million in gross revenue in the quarter. We shared the schedule before. We shared some of it with Arbitrum. It's about 50%. So even on a net basis, about $25 million or $100 million annualized. We didn't call it a cylinder just yet. We want to give it more time to bake. You should expect in a normalized environment, it's probably a couple of basis points on notional values what we monetize. But as Vlad said, the team is not goaled on revenue at this point. It's growing TVL, making developers happy, growing stock tokens. If we do that, a couple of basis points can add up to a really large number over time.

**Vladimir Tenev** (Executives):
Yes. And I know for the developers out there, they -- we have a lot of passionate Robinhood Chain developers that are working on projects. Just be confident that we're talking about what we can do for the community. And I think you'll see -- since it caught us by surprise, we've had to like staff up a team here, I think you'll see a lot more for us supporting builders in the near future.

**Chris Koegel** (Executives):
Great. Thank you, Vlad and Shiv. Our next question is from Steven Chubak at Wolfe.

**Steven Chubak** (Analysts):
So I wanted to just ask on the net deposit growth, which I know seasonally 3Q tends to be a touch lighter. I'm really evaluating this KPI on a core basis. But as the denominator has grown larger, you've been getting -- running a little bit below that 20% target. And I just wanted to get a better sense as to -- as we unpack some of the building blocks, how much of that 20% is expected to come from new account growth or new store growth versus same-store growth? And specifically, I wanted to get a better sense as you continue to expand internationally, how those efforts could potentially help close the gap.

**Shiv Verma** (Executives):
Yes. I'm happy to start on this one.

**Vladimir Tenev** (Executives):
Yes, yes, go for it.

**Shiv Verma** (Executives):
So as we said before, we target 20% annualized, and we gave some October color on the call. We have already surpassed that. So we're just through October. We've already done over the $68 billion last year and surpassed our growth target.
Now as you mentioned, it will not be linear. There was some higher growth in Q2 and then it came down a little bit in Q3. But we've said over and over again, I don't over-index in any one month, any one week, any one quarter. But on an annualized basis, we are still seeing the business compound. The best driver of net deposits is just new products. And so as we keep shipping new product velocity, customers come, they adopt us more and they continue to deposit more. In terms of new store sales versus existing customers, it is both.
More recently, it's been a little bit more of the existing customers. We got a lot of customers very, very fast in the prior years. And now as we ship new products, we're gaining share of wallet and they're starting to trust us more. As we've said before, though, we are starting to turn the dial to try to accelerate net funded accounts again. And so Q3 was similar to Q1. Q2, we saw a nice bump up because of some market backdrop and there was a couple of IPOs in there as well. But big picture, our existing customers are still using us for more, and we think we have some great products next year that should also drive the top of funnel.

**Vladimir Tenev** (Executives):
Yes. And I'd also add to that, we've been pushing pretty hard on Trump accounts, making that a great product. You'll see this -- this isn't just an app. It's going to be increasingly an ecosystem. So we're plugging in employers, now employers will be able to fund Trump accounts on behalf of their employees. And then we're going to be plugging in donors. Donors are kind of done on a one-off basis now. But you can imagine if you're a corporate donor or a wealthy philanthropic individual, we'll make it really easy and delightful to go into the Trump accounts.
We're already seeing meaningful net deposit impact on that. And I think that it can be much, much bigger. Everyone -- a lot of people are aligned in having that be a bigger number. And we think that we have an opportunity, of course, if we continue to serve these customers very well as we expect to, for those to be compounding assets. What was the number, $70 million, $25 million funded by Michael and Susan Dell alone. I mean if we serve these customers well over time, I think a large portion should be Robinhood customers.

**Chris Koegel** (Executives):
All right. Thank you, Vlad and Shiv. So the next question is from Michael Cyprys at Morgan Stanley.

**Michael Cyprys** (Analysts):
I just wanted to ask about peer-to-peer payments that you just launched here on the call here. I was hoping you could expand on your vision for this new offering, how you see this contributing in the coming years, including perhaps a funnel for new client acquisition, maybe even revenue monetization. So hoping you could talk about your expectations there and how you see this ramping?

**Vladimir Tenev** (Executives):
Yes. I mean where we started was really just -- we had a lot of customers saying that they want to send money to their friends via the question asked about Zelle, but Zelle or other things, can we make that a little bit easier? And then we thought, well, what's the most simple, seamless thing we could do where you don't even have to enter anything. You could just send money via text. And I think we deliver that experience. It's just if you want to just -- literally sending money from Robinhood is as easy as texting someone.
So the first thing we're looking for as we roll this out is are our existing customers using it? Is it solving their problem. And I think once we've got that, by its very nature, the product should be viral, right? As they continue to send money to their friends, if they use it, then we have to make a compelling case for that recipient if they don't already have Robinhood to enter that ecosystem. But that gives us another opportunity, another potential touch point to get them as customers.

**Chris Koegel** (Executives):
All right. Thank you, Vlad. The next question is from Alex Markgraff at KeyBanc. All right. We may have lost Alex. The next question is from Ben Budish at Barclays.

**Benjamin Budish** (Analysts):
One for Shiv on the expenses. So the number for the quarter came in, I think, a bit lower than a lot were expecting. Your full year guide was lower just a little bit. Curious if you could talk about the moving parts. I know there's some timing of Trump expenses that are expected to come in, in the back half. And curious what you can share on the run rate into '27. I know you're not giving guidance there yet. Obviously, the Trump expenses may be nonrecurring. And you've kind of talked before about sort of like a lower single-digit growth rate for existing businesses, but on top of that, there are new initiatives. So curious if you could talk a bit about the near-term moving pieces and how we should think about the run rate going into next year.

**Shiv Verma** (Executives):
Yes. Great question. So what I'm really excited about is even with all the new products we're shipping, we're still staying lean and disciplined. As you mentioned, we lowered our outlook by $25 million at the top end. In Q4 specifically, there's a couple of things that we're rolling out that we're investing in. First, we're doing even more for the Trump account. So you should expect some more expenses there. Second is the credit card. We're continuing to scale the credit card, both Gold and Platinum. So there'll be some investments there. And then lastly, we're in the middle of annual planning right now, but there's a couple of items we're really excited for. And so we pulled those forward and we started to make a couple of investments there.
For Trump accounts specifically that you asked about, for the full year, I shared earlier that we expect it to be about $100 million investment. It's still roughly going to be in that range for the full year. And so there was some timing things throughout the quarter, but that's what I would expect. 
For next year, it is early, and we're going to finish our planning process, and we'll come back in January and February and share the full plan. So nothing to share on that yet. But as Vlad said, it is going really well. They're asking us to do more. And so I would expect that we'll be continuing to invest there.
And then in terms of our overall philosophy, very similar to prior years. As we go through planning, we're asking each of the teams to be more efficient in those core business. We take those efficiencies and then we reinvest it. We have so much more to do, as you've seen. And so it will be very, very similar to prior years.

**Chris Koegel** (Executives):
All right. Thank you, Shiv. The next question is from Patrick Moley at Piper Sandler.

**Patrick Moley** (Analysts):
I do have one on Crypto.com and OG.com. You now own equity in two prediction market venues while running your own exchange with Susquehanna. How do you reconcile the routing decisions between the different venues? And what is the strategic logic of holding stakes and competitors to Rothera?

**Vladimir Tenev** (Executives):
Yes. Maybe I can start. We want to give our customers the best prediction markets experience. And we want them to have choices, too. I don't think we can send all of our flow to one venue. So we think that the combination of Rothera and Crypto.com is just -- positions us well to actually serve our customers well, have great execution quality and have broad coverage of all of the assets that our customers want to trade. Maybe you can take the financials.

**Shiv Verma** (Executives):
Yes. As Vlad mentioned, it is good to have a resilient and a second exchange. What you should expect is Rothera will be our primary exchange and Crypto.com/OG.com will now be our main second exchange, and we'll be getting off most of our competitors. By the end of the year into early next year, you should expect the vast majority of our flow goes through both of those.
From the financial standpoint, what we're doing now is, in addition to sending them flow, we're also becoming owners. And so before we were sending our flow to other exchanges, and we weren't getting any financial incentives because of that. There is no conflicts to be clear. A product is listed on a particular exchange. It's depending on where you can get a product experience. So there's no routing like equities or options. They're not interlistable. You have to list it on either Rothera or either Crypto.com. But now in addition to getting a great customer experience, we can also provide a little bit of monetization for shareholders. So that's why we're super excited to both build and get a great product experience for customers, but now also having some financial upside for shareholders as well.

**Chris Koegel** (Executives):
All right. The next question is from Brian Bedell at Deutsche Bank.

**Brian Bedell** (Analysts):
If I can ask a two-parter. One, just the timing of company KPIs for launching those now that Cboe has final approval for that. 
And then secondly, Shiv, if you could just talk about a little bit more color or give a little bit more color on the October volumes to date. I think you said down 5% on equity assumptions in crypto. If you could just sort of maybe bifurcate between those areas? And any comments on take rate in crypto? I know that tends to move around a lot.

**Shiv Verma** (Executives):
You want to do the KPIs, and I'll do...

**Vladimir Tenev** (Executives):
Why don't you take them all?

**Shiv Verma** (Executives):
Sure. So on the KPIs, we were actually just talking with the GMs this morning, Steve Quirk and Johann. They're both coming very soon. And so the teams are hard at work on them. We're getting the final approvals. We announced them at HOOD Summit. So you should expect them in the near term, we're just waiting for kind of all the approvals to come through, but we're ready to go and excited for customers.
In terms of the October color, and so as a reminder, Q3 was a record quarter. So everything was our highest quarter ever for equities, options and margin. And so great to see in October for equities and options and crypto, they're within plus or minus 5%. And so I kind of group them all together, but they're all trending to similar levels and early in the quarter, call it, within 5% of the high watermark in Q3. And then I called out event contract specifically because that was a little bit different and up about 7x year-over-year. And so starting to see some more increase there.
On take rate, what we're seeing to start the quarter is that spreads are a little bit tighter. And so we'll see where the full quarter shakes out, but early indications are spreads are a little bit tighter, and we'll see how it plays out for the next 2 months.

**Chris Koegel** (Executives):
Great. All right. The next question is from Gav Blaxberg from WOLF Financial.

**Gav Blaxberg** (Analysts):
I'm going to go into an area that I don't think has been discussed too much yet, and that is Robinhood Social. I talked with you about this, Vlad. I've been power using the platform, love it, spending probably an hour plus a day on there. And I'm talking to more and more people and people are like, well, what are the plans for this? What's the goals? How does this create revenue? How does this drive things for the platform and create shareholder value? And I would just love to hear also how it's being prioritized and balanced with so many other things going on, building out a social media is no small undertaking. And so I wanted to hear some of the vision for this and how this is ultimately going to lead to revenue generation and increasing shareholder value.

**Vladimir Tenev** (Executives):
How have you been liking it? Have you -- any critical feedback, anything we could be doing better?

**Gav Blaxberg** (Analysts):
I've been chatting with Anna Tork and some others on the team and given a ton of pieces of feedback and also trying to talk to the other power users and connect with them and get pieces of feedback. I think it's continuing to progress really nicely. There's certainly -- listen, if you want a feedback session at some point, I'll give it to you, but I don't know if that's the best use of your time right now.

**Vladimir Tenev** (Executives):
Yes, that's good. Yes, you don't want to do that. It's too much at earnings. He's a tough customer. Yes, look, I think that the reason we get excited about Robinhood Social is because, yes, I mean, frankly, I believe that it's the best way to learn rather than which way am I most bullish on Robinhood producing all the content that teaches people how to invest and gives them all the tools? Or am I more bullish on 28 million customers and those customers using our product and bringing the best ideas that they find from everywhere in the world to us? So definitely the latter.
And yes, I think if done well, we can just surface really good content for our customers that they can use to learn new things. And we're already seeing kind of a community form around this. So I mean, we've got a lot to do. Just we've made it so that people can share things outside of the platform. And we've continued to also increase the type of content that you can share on social. It started out with just trades, but now you can share P&L, you can share charts -- you can do your portfolio. We have the creator offering. Also creators, a lot have been asking about creator monetization. So that's something we'll obviously want to look into. And I think at that point, yes, it becomes a business line for us.
But as of now, I think we're thinking about it in the context of the broad Robinhood experience. And we think that if we do a really, really good job, it just gives people one more reason to not just do the execution of the trade on Robinhood, but just stay in Robinhood for getting the idea and the context behind the trade.

**Chris Koegel** (Executives):
All right. Thank you, Vlad. The next question is from James Yaro at Goldman Sachs.

**James Yaro** (Analysts):
I was hoping you might be able to just update us on your Robinhood strategy -- your Rothera strategy at this point. How do you plan to generate market share gains? And maybe you could speak to the pricing strategy at this point. And then maybe finally, maybe just an update on how you're thinking about adding other FCMs to the platform beyond just the HOOD brokerage.

**Vladimir Tenev** (Executives):
Yes. That's a great question. And again, we don't -- we're a significant equity holder in Rothera, us and SIG, but we don't actually -- we're not actually operating Rothera ourselves. I mean, of course, hopefully, they like to -- Tom and team do listen to us occasionally on retail, but it's like an independent business. Yes. And so I don't want to speak too much about their strategy for getting FCMs, though I know they're highly motivated. And I think Rothera could become the default neutral gateway for FCMs because a lot of the other prediction market venues, they have their first-party offerings where they are trying to acquire customers while they're offering a service to others. And I think when we talk to a lot of other FCMs, they don't like the idea and the potential conflict of their provider also operating a first-party business. So I think the great thing about Rothera for any FCMs that want to connect to it is that it's purely working with FCMs. So you don't have to worry about your provider also competing with you in the marketplace.
And at least from our standpoint, we have been investing a lot in the non-sports contracts. You saw us announce KPI prediction markets. We've been seeing a lot of growth in the crypto contracts and commodities. And I think that over time, we see an opportunity in integrating these financial -- I think we can own the financial category because that's like a unique advantage we have. And Rothera can support just more sophisticated financial contracts and be a leader there because I think we're less excited about doing what everyone else is doing, which is just all sports all the time because I think that's rapidly going to get commoditized and is just, frankly, a little bit less differentiated from my standpoint.

**Shiv Verma** (Executives):
Yes. And the two things I'll add there. On the non-sports side, if you look in the quarter, it was actually about 30% was non-sports, and that was up from 15% the quarter before. So as Vlad said, we're starting to see adoption across some of these other asset classes, which is great to see. 
On the pricing side, we're really excited that our pricing is now official, but we lowered pricing for customers when we bought Rothera. And what we did is we made a dynamic pricing model. And so what we heard from customers was if you were trading something in the wing relative to the center, you actually paid a higher take rate. And so instead of just increasing monetization, what we decided to do is redo the pricing model. We made it dynamic. We listened to customers, but we didn't impact our take rate because we were able to share some with them and take some of that back. And then on top of that, we made it even better with Gold. We talked a lot about Gold. But now if you're a Robinhood customer and you're a Gold member, you also get even better pricing as well. So a couple of different things all going on there at the same time.

**Vladimir Tenev** (Executives):
Yes. And if you look at the experience, those of you that trade prediction markets on Robinhood, you can see we've really done a nice job just refining the experience, having like specific modules for different types of prediction markets. The midterms hub, in particular, I think, just looks amazing. So it's not just if you want to trade them, but just as a way to explore and find what's likely to happen through the midterms. I think we've done a really, really nice job. And the 15-minute up and down markets on crypto have been looking good. So yes, I think you can see the chiseling that's happening on the product to make it even more usable.

**Chris Koegel** (Executives):
All right. The next question comes from somebody right off a plane, Dan Dolev from Mizuho.

**Vladimir Tenev** (Executives):
Dan Dolev. Are you in the airport?

**Dan Dolev** (Analysts):
I'm in Munich. I just got back from Israel en route to New York, [ traveling both ] today. Great results, as always, we've done some work. I'm very interested in perpetual futures. It sounds like you guys are headed to something really big there. And I think we're getting a lot of questions on it. I just want to know like how big do you think this one could be? Because it sounds like it's a huge opportunity here. So I would love to get some more color on that.

**Vladimir Tenev** (Executives):
Yes. I mean I think that if you look at the sort of like leaders in perpetual futures, the perpetual futures is a huge market by volume with daily volumes in the billions. In fact, some of the platforms globally have tens of billions in daily perps volume. And then we saw even on Robinhood Chain, which again is just a couple of months old, we're seeing over USD 1 billion notional in on-chain perps. So I see no reason why our offering can't get to a similar, if not greater scale than the DeFi offering as time goes on.

**Chris Koegel** (Executives):
All right. The next question is from David Smith at Truist.

**David Smith** (Analysts):
Can you flesh out a little bit more about what you're seeing in terms of the drivers on take rates as 3Q came in lighter than what a lot of us were expecting. It sounded like that declines continued to start the fourth quarter. Sure, it differs across asset class, but is this a mix issue on the user front or on the sub-asset class front, trade sizes, volumes, other dynamics? What would you point to there?

**Shiv Verma** (Executives):
Yes, I'm happy to take this one. So on equities, it's usually a mix shift between single names and ETFs, and it also depends on what the spreads are. Options is also similar. It depends on what the vol is and also the spreads. And then is it -- are they trading more index options? Are they trading more single names? Is it more indices? That tends to be a bigger driver there.
On crypto, the main driver was our Robinhood Earn, our stablecoin product. So that product is doing great and now has over $500 million of assets there. But because it's stablecoin, we monetize it less than the normal platform. And so that's what drove it down. If you take out the stablecoin, it was basically similar to the quarter before in the same ZIP code. So that was the main driver there. 
And then ECs, as I mentioned, we updated our pricing. And so it will depend on what the customer is trading. Are they trading the money line? Are they trading at the wings? Are they using Robinhood Gold? And so that's why we saw it moving a little bit. So I would say each of them is a little bit different. And that what we're seeing in October is as a start, they're similar to what we saw and maybe a touch lighter as spreads are a little bit tighter. But again, it's about 3 weeks into the quarter, and so we'll see what the full quarter shakes out.

**Chris Koegel** (Executives):
Great. The next question is from Dr. Crossroads.

**Unknown Analyst** (Analysts):
Just wanted to ask, given that you've given us last year some information regarding the impact of rate hikes, and we're in a very different -- rate cuts, and we're in a very different situation with rate hikes. I'm wondering if it's going to be a similar impact on the ecosystem. I believe you guided for a negative $50 million impact for each rate cut on net interest income, especially now that banking is a part of your ecosystem and also credit cards are a meaningful part as well.

**Vladimir Tenev** (Executives):
You remember, by the way, a -- was it like a year ago, everyone was like, what's your business going to do? You've done so well in a high rate environment with all this interest income. How will you survive in a low rate environment? And now it's funny, every couple of years, it's like the question reverses, you've been doing so well with these declining rates. How are you -- now rates are going to go up again, but...

**Shiv Verma** (Executives):
I'm happy to take it. It is great. I mean, first...

**Vladimir Tenev** (Executives):
Good to see you, by the way. I hope you're doing well.

**Shiv Verma** (Executives):
The first thing we like, as Vlad said, is the business is diversified. So some products do well in a low rate environment, such as the trading products and others do better in a high interest rate environment, such as the NIM products. The actual math is for every 25 basis point hike or decline, it's about a 1.5% change to revenue. So all else being equal, if the Fed hikes another 25 basis points, that should be a lift. The really simple math is we have about $80 billion of interest-earning assets. About half of that $40 billion is interest-sensitive assets because the sweep program and a few other things aren't interest sensitive. So the DV01 $25 million -- 25 basis points and $40 billion is about $100 million of a change and then $100 million on about a $5.5 billion to $6 billion run rate gets you to about that 1.5%. So big picture, though, we like being diversified and a rate hike is a tailwind. But regardless of the rate environment, we've got a business that does well in both of them.

**Chris Koegel** (Executives):
Thank you, Shiv. The next question is from Adam Frisch from Evercore.

**Adam Frisch** (Analysts):
I wanted to follow up a little bit on net deposit growth and actually monthly actives as a percentage of fully funded. Both were a little weaker this quarter. So I would appreciate some color on what drove that in the quarter, if we should be aware of any new or incremental initiatives you're thinking about or acting already to reverse that? Or if it's just a 90-day period that isn't necessarily indicative of the overall trends and what you're seeing so far in 4Q?

**Shiv Verma** (Executives):
Yes. I would say it's more of the latter. We don't over-index in any 1 month or quarter. And the best way to see it is October. As we mentioned, October was already a record of over $13 billion of net deposits. And ADVs were very similar or just a touch lighter than what we saw in a record Q3. And so things are going to move around. There's timing of when we launch new products. There's timing of when promos happen. There is some seasonality. There's macro events. There's the IPO market. So all of those come together. But if you look at it on an annualized basis or if you just look at October alone, already seeing really healthy engagement across trading and net deposits.

**Chris Koegel** (Executives):
All right. Thank you, Shiv. The next question is from Ramsey El-Assal at Cantor.

**Ramsey El-Assal** (Analysts):
I wanted to ask if you could elaborate a little bit, Vlad, on the rationale for the Ripple partnership. How is that going to benefit you guys? I know there's a few different dimensions there, internal treasury operations, also external facing benefits for Bitstamp, et cetera. Where do you see the nearest-term opportunity, the greatest near-term opportunity? And just sort of if you could expand a little bit on the overall strategic rationale.

**Vladimir Tenev** (Executives):
Yes. I mean, yes, I think I like Brad and the team at Ripple. And I think that we were excited to do more business together. I think that there's a lot of ways in which we offer complementary things. And we're never afraid to get more integration into -- I think more integration, more products, more selection for the Robinhood ecosystem, both in the app and in chain is just strictly better. And I think we kind of bring complementary things to the table with their institutional business and our more retail-oriented business.
And in fact, today is another example of this, Ondo integrating into Robinhood Chain. Now Ondo also has tokenized products, but our thought is, well, we want our chain to be the best home of tokenized products. They don't need to be our own. And in fact, it's important for us to just make sure everyone has an equal opportunity to list on our chain and on our properties for our customers because that just leads to the best product. So of course, if we would like our own first-party products to always be used, but if they also have to be better than the competition.

**Chris Koegel** (Executives):
All right. Thank you, Vlad. The next question is from Ed Engel at Compass Point.

**Edward Engel** (Analysts):
I guess how are you thinking about bringing stock tokens onshore in the U.S. after the SEC's innovation exemption? And then is there anything regulatory-wise in your radar that might unlock private stock tokens that you announced last year?

**Vladimir Tenev** (Executives):
Yes, that's a great question, something we've been very passionate about. For private companies, we basically have two bets, one being Robinhood Ventures, which is in the form of fund products in the U.S. and then stock tokens overseas where we have the ability to tokenize individual companies. And in a sense, through our -- what we benefit from -- these two things help each other because with Robinhood Ventures, we have relationships with companies. We've been investing in a lot of companies. We have like an active pipeline. And a lot of those companies actually inquire about what tokenization is and can they join and we've been -- we have the relationships, and we've been a leader in this space. So I would say we have a path to doing it overseas. We know how to do it. We've demonstrated the technology and the capability. So it's just a question of getting all the regulatory stuff in place, but we do intend to launch these products overseas.
Now when it comes to in the U.S. for private stocks specifically, there's another layer to it, which is the accreditation requirements. And so we are working hard to find a path that satisfies the current accreditation requirements and also leads to a great customer experience. I think Robinhood Ventures is an example of this in the construct of funds. But of course, a lot of customers want exposure to individual names as well. And so we're working hard to do that within the constraints.
As far as the innovation exemption goes, I think it's a really positive step. We're supportive of it. We think that, obviously, the U.S. needs to be a leader in this new technology. I do think more needs to be done to give people a little bit of certainty because as we talk to customers, I think the uncertainty of what happens in 5 years is likely to be an impediment to like putting serious assets onto this technology. So I still think some rule-making or legislation is going to be necessary, even though, of course, it's a positive step, and we hope to have more to share on our own U.S. tokenization plans in the near future.

**Chris Koegel** (Executives):
All right. Thank you, Vlad. The next question is from John Todaro at Needham.

**John Todaro** (Analysts):
I was hoping we could just get some commentary on maybe the health of the retail trader within equities. In particular, AI stocks have come down quite a bit in the last several weeks, and many of those were traffic in quite a bit by retail. So just wondering if we can get any commentary there on engagement post the sell-off.

**Shiv Verma** (Executives):
Yes, I'm happy to take this one. Engagement continues to be really strong. I mean the best way to see that is through the ADVs and through net deposits, and both of those were incredibly strong in the start of October. And so as we said before, our customers, they tend to be younger. They tend to be techno-optimists. They tend to be technology forward. They use sell-offs as a buying opportunity. And so when you saw a sell-off in AI stocks or in chip makers or in semis, our customers leaned in and continue to buy more. On down days, we tend to see some of our strongest net buying. And so -- but the best metrics I would look at are just net deposits and ADVs, and both of those were really strong in the start of October.

**Chris Koegel** (Executives):
All right. Thank you, Shiv. The next question is from Andrew Harte from BTIG.

**Andrew Harte** (Analysts):
Shiv, you talked about turning up the dial a bit on top of funnel. Just wondering if you can share some details on the strategy there and any traction you've seen? And then a bit of a follow-up on the MAU question. I realize it's kind of just one period. But in the past year, we've been in that 13 million to 14 million user range on MAUs. Just curious, anything you can do there to try to drive that number higher as well?

**Shiv Verma** (Executives):
Yes. Could you repeat what was the first part of the question? Apologies, before the MAUs.

**Andrew Harte** (Analysts):
Anything on top of funnel that you're doing? And then similar question, but how to increase the MAU number as well?

**Shiv Verma** (Executives):
Yes. On the top of funnel, there's two things. First is product and the second is marketing. What we've been focusing on this year is primarily product. We've been testing a tiny bit on marketing, but we haven't done it yet. But if you look at a lot of the things that Vlad shared, whether it was P2P or banking or other products, we think those can be pretty meaningful drivers. So we're making some investments, and we pulled some of that forward to make them and develop them this year, and you'll see them launch in 2027. But the big drivers are generally just products and a little bit of marketing.
On MAUs, the honest answer is we don't goal on it. The teams are goaled on, are customers engaged? Are they using the platform? Are they trusting us? Are they depositing? All of those are incredibly healthy. MAUs is an output metric. It's going to move around a little bit with the market. As I mentioned before, it could be seasonal, it could be the macro, it's what they're doing. Everything we're seeing is customers are incredibly healthy. And if they're depositing more and they're engaging more, they're using more of our products, we call that a win and then MAUs are just going to move around.

**Vladimir Tenev** (Executives):
Yes. And I think longer term, we have some bets that we're working on. I think, obviously, having the opportunity to serve upwards of 70 million children with the Trump accounts and serving as the broker and -- the initial trustee of the program with BNY. I think it's a big opportunity for us to just be in front of the next generation there. We've also been thinking about how to invest. I mean, we have custodial accounts, which have been a nice addition to the platform, but how can we actually invest in getting customers as they're even younger and build an even better experience because we're starting to see some smoke there.
So yes, I think that in the next year, we're going to be making several bets that yes, I believe will not just increase top of funnel net funded account growth, but also MAU growth. I mean the two are sort of like high level interconnected. So you should see those move and that's outside of marketing and outside of, I think, the long-term opportunity of serving as the trustee of the Trump accounts initiative. You're muted.

**Andrew Harte** (Analysts):
I told you last quarter, my son was about to be born and I signed him up and I can confirm it was a very easy onboarding process for his Trump account. So well done there.

**Vladimir Tenev** (Executives):
Thank you. That warms my heart. Hopefully, you'll have many more.

**Shiv Verma** (Executives):
Also, you can see if your employer will match you now and get a little bit more for your son in there as well.

**Andrew Harte** (Analysts):
Yes. Good call.

**Chris Koegel** (Executives):
All right. The next question is from Alex Markgraff at KeyBanc.

**Alexander Markgraff** (Analysts):
It sounds like things are going quite well in banking. I certainly appreciate the withdrawal destination data point that you shared. What should we be looking for to determine when the product is in a state that warrants more sort of intentional marketing efforts or when you're ready to pour fuel on the fire, so to say?

**Vladimir Tenev** (Executives):
Yes, that's a good question. That's going to be tied with the general availability of the product. So right now, you kind of have to be a Robinhood brokerage customer to be eligible for banking, which essentially means there's no like independent onboarding -- sorry, my hair makes these tough. No independent onboarding yet in the banking app. Of course, we do intend to roll that out. And if -- once we have independent onboarding, then that unlocks the possibility of performance marketing, which will be a new capability of ours because now we're marketing multiple things.
So we're still early, but I think we're -- we've got a great team on the marketing side, and we're going to be investing more in the capability. But we do believe that banking will actually give growth to brokerage and not just the other way around. So this is just -- yes, just a greenfield opportunity for us, which will also impact net funded account growth and MAUs.

**Shiv Verma** (Executives):
And banking is a little different than the credit card. So credit card, we're rolling out more delivery because you have to get the unit economics right, you have to get the credit risk right. Banking is just like any of the other products that we launch. You make sure that customers like it, you fix their pain points once you find product market fit. So it will be much more akin to a regular software product relative to the credit card, which took a little bit longer to roll out.

**Vladimir Tenev** (Executives):
Yes. And I'd also add that it's a little bit more of a predictable compounder because the trading products, there is a dependence on the market and seasonality, but banking, people just receive their paychecks, they spend, they're in the ecosystem week in, week out, it's -- which counterbalances the trading business quite nicely.

**Chris Koegel** (Executives):
All right. And finishing strong here. Our next question is from Ken Worthington at JPMorgan.

**Kenneth Worthington** (Analysts):
Keeping it sort of high picture, ARPU doubled over the last 2 years to about [Audio Gap]. Road map of new products and new cross-selling, how do you see ARPU evolving from here? And if I pick an ARPU figure like $300, do you see this as feasible? And given all that you've got going on, what does Robinhood need to get right to get to a figure like that?

**Vladimir Tenev** (Executives):
Yes. I think that's an interesting question. I mean the reason I'm reluctant to just give you our ARPU goal is I think we also think there's a lot of opportunity to grow customers and grow down market. I mean if we get more younger customers, you could see, for example, ARPU decreasing, but the total size of the customer base increasing dramatically. I mean, particularly depending on how you count Robinhood Chain users and international customers as we continue to put our foot on the gas of the international expansion, which I think we're still in the relative early days. I mean we crossed 1 million international customers, but not hard to imagine that itself growing exponentially on the way to the majority of our customers being international over the long run.
So it's a complicated optimization of our existing customers continuing to get more valuable, get wealthier and their ARPU should be continuing to increase, but there's going to be a counterbalancing effect of us just getting plenty of more customers from international markets and who are younger.

**Shiv Verma** (Executives):
Yes. A couple of things I'll add there. ARPU is an output metric. So we actually don't go to teams on that. We grow them on market share and then ROI. And what we've said before is we believe Robinhood can 10x from here. And so you can take any metric you want, whether that's revenue, net deposits, et cetera. The highest predictor in correlation to revenue is just net deposits. So if we keep gaining that deposits, if the customers keep trusting us, whether it's new funded customers, whether that's an existing customer trusting us with more, that's how you grow the business, and that's how you grow revenue. ARPU is going to grow wherever it's going to go. But again, that's not what we go on. We just grow on market share and giving a great customer experience.

**Chris Koegel** (Executives):
All right. Well, that concludes the Q&A portion of the call. Vlad, would you like to make any closing comments?

**Vladimir Tenev** (Executives):
Yes. I just wanted to tell you guys, again, thank you for being here for those of you in person and also those of you watching remotely. We're building a community here, not just of customers, but also shareholders, investors, retail and institutional, had some content creators on the call. And you should know that we are far from done, and we are not complacent and the road map just continues to be incredibly full. So rolling out all the things from HOOD Summit and a bunch of other things in the hopper to make this your financial super app and to deliver the power of ownership to people worldwide. So thank you for being with us on the journey. And thank you for listening, bearing the heat.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### HOOD_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜Shiv Verma｜guidance：CFO 稱調降並收窄 2026 全年 adjusted OpEx 與 SBC 展望，區間 26.75 億至 27.75 億美元（原話："and SBC to a range of $2.675 billion to $2.775 billion."）
- 2026-07-29｜Shiv Verma｜guidance：CFO 給 7 月淨入金追蹤約 40 億美元，並說明尚未含 Trump Accounts 入金（原話："July net deposits are tracking towards the $4 billion area"）
- 2026-07-29｜Shiv Verma｜guidance：7 月股票、選擇權、預測市場日均量與 Q2 相近（原話："July, the ADVs for equities, options and prediction markets"）
- 2026-07-29｜Shiv Verma｜guidance：7 月加密貨幣交易量初步比 Q2 稍慢（原話："In terms of crypto, it's probably a little bit slower"）
- 2026-07-29｜Shiv Verma｜guidance：7 月 take rate 與 Q2 平均相近，建議以此為起點（原話："they're in a similar area to what we saw for the Q2 average"）
- 2026-07-29｜Shiv Verma｜margin：管理層對 take rate 的口徑：視為輸出指標，股票與選擇權受組合、波動度、合約類型影響（原話："take rates are an output"）
- 2026-07-29｜Shiv Verma｜margin：Q2 adjusted EBITDA 7.41 億美元，年增 35%，利潤率 57%（原話："adjusted EBITDA was $741 million, up 35% year-over-year"）
- 2026-07-29｜Shiv Verma｜margin：Q2 EPS 0.62 美元，年增 48%（原話："earnings per share was $0.62, up 48% year-over-year"）
- 2026-07-29｜Shiv Verma｜margin：Q2 adjusted OpEx 與 SBC 為 6.41 億美元，低於先前展望區間，且含兩項新業務成本（原話："adjusted OpEx and SBC was $641 million"）
- 2026-07-29｜Shiv Verma｜margin：管理層說明 Rothera 與 WonderFi 新增成本由內部效率自行吸收（原話："allowing us to both self-fund Rothera and WonderFi costs"）
- 2026-07-29｜Shiv Verma｜margin：回答費用三桶（新產品、核心、併購）演變時，稱節省來自三者，且新併購未納入原展望（原話："The short answer is the savings are coming from all of"）
- 2026-07-29｜Shiv Verma｜margin：新併購成本未納入原先費用展望，由公司自行吸收（原話："So we fully self-funded those."）
- 2026-07-29｜Shiv Verma｜margin：管理層新增的衡量口徑：Rule of 40，並稱已是 Rule of 80 公司（原話："more than a Rule of 80 company for the past few"）
- 2026-07-29｜Shiv Verma｜capital_allocation：6 月募資 22 億美元，稱零票息（原話："In June, we opportunistically raised $2.2"）
- 2026-07-29｜Shiv Verma｜capital_allocation：該筆融資條件：0% 票息、股價超過 300 美元前無淨稀釋（原話："with both a 0% coupon and no net dilution until"）
- 2026-07-29｜Shiv Verma｜capital_allocation：年初至今買回 750 萬股、6.64 億美元（原話："we've repurchased 7.5 million shares for $664 million"）
- 2026-07-29｜Shiv Verma｜commitment：重申財務北極星為最大化每股盈餘與每股自由現金流（原話："our financial North Star remains the same, maximize earnings"）
- 2026-07-29｜Shiv Verma｜commitment：計畫在未來一年增加更多年化營收 1 億美元級業務（目前 13 項）（原話："add even more $100 million ARR businesses"）
- 2026-07-29｜Shiv Verma｜commitment：CFO 提到有投資人反映難以判斷該看哪些成長指標，因此提出三項衡量指標（淨入金、Rule of 40、1 億美元 ARR 業務）（原話："we've also heard from some investors"）
- 2026-07-29｜Vladimir Tenev｜commitment：CEO 稱目標在本季底前將 Robinhood Social 開放給所有人（原話："The goal is to get it out to everyone"）
- 2026-07-29｜Shiv Verma｜commitment：CFO 稱未來十年業務規模可望擴大 10 倍（原話："10x the business over the next 10 years"）
- 2026-07-29｜Shiv Verma｜commitment：CFO 稱淨入金年化 20% 為目標，並表示不解讀單月波動（原話："So our goal, as we said, is 20% on an annualized basis."）
- 2026-07-29｜Shiv Verma｜commitment：CFO 稱累積幾季後會更細拆 Robinhood Chain 的變現（原話："quarters, we'll break it down more specifically."）
- 2026-07-29｜Shiv Verma｜customer：Q2 新增近 100 萬名資金帳戶客戶，為上市近 5 年來單季最多（原話："1 million funded customers, the most we've added"）
- 2026-07-29｜Shiv Verma｜customer：CFO 列舉新客成長來源之一：併購帶來數十萬帳戶（原話："which provided a couple of hundred thousand accounts"）
- 2026-07-29｜Shiv Verma｜customer：CFO 稱新客戶訂閱 Gold 比例約 40% 至 50%（原話："New customers still sign up for Gold about 40% to"）
- 2026-07-29｜Shiv Verma｜customer：預測市場使用者數由上次揭露的約 150 萬升至接近 200 萬（原話："number is now closer to 2 million"）
- 2026-07-29｜Shiv Verma｜customer：CFO 稱客戶於下跌日或下跌月傾向淨買進（原話："down days or down months, we tend to see really strong net"）
- 2026-07-29｜Shiv Verma｜customer：CFO 稱 PDT 規則取消使公司因客戶帳戶較小而受惠高於同業（原話："benefit relative to our peers given our customers"）
- 2026-07-29｜Shiv Verma｜customer：CFO 對 PDT 後續貢獻表示尚難量化（原話："it's too early to tell what's exactly going to be"）
- 2026-07-29｜Vladimir Tenev｜customer：Trump Accounts 已有 700 萬名兒童註冊（原話："So 7 million children have signed up."）
- 2026-07-29｜Vladimir Tenev｜customer：銀行帳戶直接存款的附掛情況：約 40% 客戶已設定（原話："we just give you 3.5% automatically on every account"）
- 2026-07-29｜Vladimir Tenev｜product：Gold Card 年化消費額超過 170 億美元（原話："driving over $17 billion in annualized purchase volume"）
- 2026-07-29｜Vladimir Tenev｜product：Robinhood Chain 上線後 DEX 交易量超過 120 億美元（原話："we saw over $12 billion in DEX volume"）
- 2026-07-29｜Vladimir Tenev｜product：Robinhood Earn 提供 7% APY，數週內入金超過 2 億美元（原話："now it allows customers to earn 7% APY"）
- 2026-07-29｜Vladimir Tenev｜product：Agentic Trading 已有逾 10 萬人整合並開立帳戶（原話："We've had over 100,000 people actually"）
- 2026-07-29｜Vladimir Tenev｜product：CEO 列出 Agentic 的使用摩擦之一：模型不熟悉被用於交易（原話："the models themselves aren't familiar with"）
- 2026-07-29｜Shiv Verma｜product：Robinhood Chain 變現口徑：每筆交易收數個基點，非按交易量（原話："per transaction, we make a few basis points"）
- 2026-07-29｜Shiv Verma｜product：Chain 收入約一半與 Arbitrum 分潤（原話："we do share approximately half of it with Arbitrum"）
- 2026-07-29｜Vladimir Tenev｜product：CEO 表示外國股票在產品路線圖上（原話："Obviously, it's on our road map."）
- 2026-07-29｜Vladimir Tenev｜product：新加坡等地擴張策略的說法：希望一次推出更多產品，而非逐項上線（原話："it's better to get more at once rather than"）
- 2026-07-29｜Shiv Verma｜competition：預測市場流量部分：預期近中期多數或相當部分走 Rothera（原話："a good portion will flow through Rothera"）
- 2026-07-29｜Vladimir Tenev｜competition：CEO 稱預測市場採多交易所連接，不依賴單一對手方（原話："and we're not reliant on any one individual counterparty."）
- 2026-07-29｜Vladimir Tenev｜competition：被問美國永續合約時，CEO 稱不提供具體時間表（原話："I just don't like giving time lines on earnings."）
- 2026-07-29｜Vladimir Tenev｜risk：CEO 談 Clarity Act：希望產業在美國有穩定的法規基礎（原話："the foundation of the industry in the U.S. to be durable"）
- 2026-07-29｜Vladimir Tenev｜risk：CEO 稱即使 Clarity Act 延後，公司認為仍會沒問題（原話："So we think we'll be good regardless."）

### HOOD_Shareholder_Analyst_Call_Robinhood_Markets_Inc_20260602.md
- 2026-06-02｜Vladimir Tenev｜product：CEO 稱 Trump Accounts 已有近 600 萬名兒童註冊，符合資格者逾 6000 萬（原話："Nearly 6 million American children are already signed up."）
- 2026-06-02｜Vladimir Tenev｜product：CEO 稱首檔 Robinhood Ventures 基金 RVI 3 月 IPO，市值已超過 10 億美元，並在籌備後續基金（原話："The response so far has been very strong."）
- 2026-06-02｜Vladimir Tenev｜capital_allocation：CEO 稱 RVI 已投資 OpenAI 7500 萬美元（原話："invested $75 million in OpenAI."）
- 2026-06-02｜Vladimir Tenev｜capital_allocation：CEO 表示在私募市場產品上大幅投入（原話："We're investing big here."）
- 2026-06-02｜Vladimir Tenev｜product：CEO 稱 Agentic Trading 上週推出，當時約推到一半客戶，目標本週底全面開放（原話："Trading is rolled out to about half of our customers"）
- 2026-06-02｜Vladimir Tenev｜commitment：CEO 表示 agentic finance 會定期更新、持續擴充（原話："you should expect to see regular updates."）
- 2026-06-02｜Vladimir Tenev｜product：CEO 給出預測市場年化營收數字（口徑：event contracts 年化營收）（原話："generating over $400 million in annualized revenues"）
- 2026-06-02｜Vladimir Tenev｜product：CEO 稱 2026 年迄今預測市場成交合約數已超過 150 億（2025 全年逾 120 億）（原話："more than $15 billion already traded in 2026"）
- 2026-06-02｜Vladimir Tenev｜product：CEO 介紹與 Susquehanna 合資的 Rothera（交易所與清算所）（原話："Rothera, which is our new joint venture with Susquehanna"）
- 2026-06-02｜Lucas Moskowitz｜risk：法務長對預測市場全面禁令的看法（原話："we think a categorical ban on prediction markets is unlikely"）
- 2026-06-02｜Lucas Moskowitz｜risk：法務長稱體育類合約是主要爭議點，公司與 CFTC 立場一致認為屬聯邦監管商品，結果待觀察（原話："that these are federally regulated products"）
- 2026-06-02｜Lucas Moskowitz｜risk：法務長稱正與監管者討論放寬散戶進入私募市場的規則（原話："productive discussions in Washington with regulators and"）
- 2026-06-02｜Vladimir Tenev｜customer：CEO 稱 Robinhood Banking 薪資直存附加率（口徑：直存客戶占有資金帳戶客戶）（原話："40% direct deposit attach rate"）
- 2026-06-02｜Vladimir Tenev｜customer：CEO 稱 Banking 自年底推出以來存款逾 25 億美元、有資金客戶逾 17 萬（原話："deposits from over 170,000 funded customers since launch"）
- 2026-06-02｜Vladimir Tenev｜commitment：CEO 對 Zelle 需求稱無具體資訊，但承諾之後會有更新（原話："rest assured, we hear the feedback"）
- 2026-06-02｜Vladimir Tenev｜commitment：CEO 稱股息追蹤功能目前內部測試中，預告即將推出（原話："is actually in internal testing now"）
- 2026-06-02｜Vladimir Tenev｜competition：CEO 談 Early Dividends 功能時對競爭對手的說法（原話："I'd be shocked if our competitors aren't scrambling"）
- 2026-06-02｜Vladimir Tenev｜competition：CEO 稱客戶可透 Robinhood 參與 SpaceX IPO，並與其他平台比較無最低帳戶門檻（原話："there's no minimum account size to do so"）
- 2026-06-02｜Vladimir Tenev｜product：CEO 稱國際客戶已突破 100 萬（原話："we now have crossed 1 million international customers"）
- 2026-06-02｜Vladimir Tenev｜capital_allocation：CEO 稱已完成 WonderFi 收購（進入加拿大）（原話："our acquisition of WonderFi"）
- 2026-06-02｜Vladimir Tenev｜commitment：CEO 稱預計年內完成印尼券商與加密貨幣收購（原話："planned brokerage and crypto acquisitions in Indonesia"）
- 2026-06-02｜Vladimir Tenev｜product：CEO 稱獲新加坡金管局原則性核准提供綜合券商服務（原話："in-principle approval from the Monetary Authority of"）
- 2026-06-02｜Vladimir Tenev｜product：CEO 陳述 Robinhood Chain 的目標定位（原話："make it the best chain to trade real-world assets."）
- 2026-06-02｜Vladimir Tenev｜margin：CEO 以營收規模口徑說明業務多元化：年營收達 1 億美元的業務線數量（原話："11 business lines generating $100 million in annual revenue"）
- 2026-06-02｜Vladimir Tenev｜customer：CEO 稱股票交易量前一日創歷史新高（會議前一日）（原話："yesterday was all-time record in equities trading"）
- 2026-06-02｜Vladimir Tenev｜commitment：CEO 稱 PDT 規則已改，下一個推動目標是合格投資人認證門檻（原話："now that the PDT rule has been has been improved"）
- 2026-06-02｜Vladimir Tenev｜product：CEO 重申三大策略支柱之二：下一代錢包份額第一（原話："number two, we want to be #1 in wallet share for the next"）

### 問答異常語氣（迴避／改口／保留）
- HOOD_Q2_2026_Earnings_Call_20260729.md｜問：Steven Chubak (Wolfe)：年初費用成長 18%（10% 新產品、5% 核心、3% 併購）的三桶如何隨新展望演變｜答法：CFO 稱節省來自三桶、強調自行吸收、仍是成長公司，但未給各桶新數字
- HOOD_Q2_2026_Earnings_Call_20260729.md｜問：Craig Maurer (FT Partners)：7 月淨入金約 40 億美元為今年最低，有何說明｜答法：CFO 改談年化 20% 目標與年初至今仍遠高於此，稱不解讀單月，未解釋 7 月數字下滑原因
- HOOD_Q2_2026_Earnings_Call_20260729.md｜問：James Yaro (Goldman) 與 Patrick Moley (Piper)：美國永續合約何時推出、為何不更積極｜答法：CEO 稱與 CFTC 溝通具建設性但不給具體時程，轉談其他產品路線圖，並說不喜歡在財報給時程
- HOOD_Q2_2026_Earnings_Call_20260729.md｜問：Brian Bedell (Deutsche)：Rothera 是否推出 Cboe 公司財務 KPI 合約，以及事件合約轉移 Rothera 的計畫｜答法：CEO 稱不確定 Rothera 是否近期推出；CFO 只說「多數或相當部分」將走 Rothera，未給比例或時程
- HOOD_Shareholder_Analyst_Call_Robinhood_Markets_Inc_20260602.md｜問：RVI 是否會投資 Anthropic？｜答法：未直接回答，稱無法具體說明正在看哪些公司，改談一般投資原則
- HOOD_Shareholder_Analyst_Call_Robinhood_Markets_Inc_20260602.md｜問：Robinhood Banking 會不會有 Zelle 與帳單支付？｜答法：先談存款與直存數字，Zelle 部分稱無具體資訊可分享，未給時程
- HOOD_Shareholder_Analyst_Call_Robinhood_Markets_Inc_20260602.md｜問：若預測市場因立法被迫下架，有何替代收入計畫？｜答法：未提供替代收入的數字或具體計畫；法務長談監管對話，CEO 轉而強調多元化與股票交易量創高

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

## ⑥ 條件附卡（archetype_hint='金融' 命中）：judge_addendum_archetype.md

<!-- source: .claude/skills/stock-analyst/references/archetype-gatesets.md sha256:d173785f92087f36 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary ∈ {金融，未獲利高成長，轉機/特殊情境，受監管公用/穩定內需} -->

# archetype 換尺 gate-set 附卡（QC-44/45/46）

## QC-44 金融（bank／insurer／broker）
archetype=金融時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：ROTCE(替FCF Margin) >15%穿越循環｜ROE且>COE~10%(替ROIC) ROE>12-15%｜跨信用循環ROTCE穩定含2008/2020壓力年(替10Y ROIC穩定) 壓力年仍正/不破底｜NIM趨勢+效率比cost/income(替毛利率定價) 效率比<~60%｜Capex/Rev不適用→operating leverage/效率比改善｜EPS+TBVPS複合+股息總回報(替EPS CAGR>20%) ~10-12%即優｜P/TBV vs ROTCE(替PEG)：Warranted P/TBV=(ROTCE−g)/(COE−g)，實際P/TBV≤warranted｜CET1 ratio(替D/E<0.7) >監管要求+緩衝(~11-13%)｜NPL/NCO趨勢+撥備覆蓋+CET1緩衝(替負債安全性)：信用品質穩、撥備足。[§QC-44]
§10估值主錨：P/TBV分位+P/E，用Warranted P/TBV判貴賤；EV/EBITDA拿掉。QC-31 signal：X改ROTCE跨循環<COE／CET1跌破監管／NPL·NCO結構惡化／重大舞弊，移除FCF·NI、EV-EBITDA、Capex觸發。§6跑道：放款·存款·AUM成長+費收業務+市佔，非TAM滲透。[§QC-44]
子型：bank＝CET1/NIM/效率比/NPL·NCO/ROTCE/P-TBV｜insurer(注意US掛牌ALV=Autoliv汽車安全件循環工業，非保險，勿誤歸)＝combined ratio<100%/float/Solvency II ratio/book value/ROE，不看NIM/CET1｜broker·交易所＝ARPU/AUC/take rate/活躍戶，常與未獲利高成長blend｜支付網絡不歸金融，走品質複利。[§子型]
batch補搜：`[ticker] CET1 ratio NIM efficiency ratio ROTCE`(bank)／`[ticker] combined ratio Solvency II book value`(insurer)；yfinance .info 給不出 CET1/NIM/效率比/NPL/ROTCE/TBV。[§batch]

## QC-45 未獲利高成長
archetype=未獲利高成長時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：Rule-of-40(營收成長%+FCF margin%，替EPS CAGR>20%) ≥40｜EV/S÷營收成長growth-adjusted或EV/gross-profit(替PEG<2)｜NRR+毛利率+增量OI margin改善軌跡(替ROIC>15%，GAAP負無意義) NRR>110%/GM>65-70%｜FCF margin+轉正軌跡(替FCF Margin>15%；已正看margin升，未正看跑道+轉正路徑)｜NI負時FCF/NI比無意義→改看FCF margin絕對值+淨現金+跑道，FCF正或跑道>12個月。[§QC-45]
§10估值主錨：EV/S(+EV/gross-profit)+Rule-of-40-adjusted，轉正後接forward P/E；trailing PE/PEG拿掉。**情境樹同步改走EV/S（2026-10-12）**：FY1共識EPS≤0時程式自動切`valuation_basis=sales_multiple`，`scenario_inputs`填營收路徑×終端EV/S×終端淨負債×終端股數（形狀見尾段），不再用EPS×本益比；負債重者(淨負債/EV>30%)Bear的`net_debt_y5`須如實反映融資缺口，股權價值為負即歸零。QC-31 signal：不因GAAP NI負觸發X；X改NRR跌破100%／Rule-of-40<20連2季／毛利結構崩／現金跑道<12個月無轉正路徑／SBC稀釋失控(股數>10%/yr無營收槓桿)。§6跑道：NRR+淨增客戶+TAM滲透+SBC-adjusted轉正時程。blend：fintech broker常＝金融×未獲利，兩套都跑、標背離。[§QC-45]

## QC-46 轉機／受監管公用（輕量尺，不展開大表）
轉機/特殊情境：§4/§10主錨→資產重估/SOTP/normalized earning power/P-TBV，非成長外推；EPS-CAGR/PEG不適用。Single Thing→轉機觸發(債務重組完成/出售虧損部門/新管理層/catalyst里程碑)，非「moat擴張」。§6/§5→「為何現在會轉」catalyst+下行保護(資產底/清算價值)。QC-31 X→流動性危機(跑道<12個月+無再融資)/重整失敗/治理舞弊。[§QC-46轉機]
受監管公用/穩定內需：§4/§10主錨→DDM/殖利率+股息成長/regulated ROE(rate base×allowed ROE)/P/B；PEG/高成長門檻不適用。§6成長→rate base成長+費率案(rate case)+准許ROE，非TAM滲透。§5護城河→監管特許/天然獨佔(single-axis)。QC-31 X→准許ROE結構下調/費率案連敗/監管轉敵/過度槓桿(利率敏感)。[§QC-46受監管]
此兩類不強制長表，但換尺與catalyst/下行保護須sourced。[§QC-46]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260714","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"加密收入在 FY26 觸底，正常化盈餘軌跡重建（非幣別引擎接棒）","columns":{"2Y 驗證點":"某季加密 −40% 而交易性總收入仍成長","5Y 驗證點":"FY28 非 GAAP EPS ≥ $3.60、加密收入占比降到","10Y 驗證點":"加密收入長期波動但均值 ~$300M+ 為 base","具體數字門檻":"Q2 非加密交易性收入 YoY >+20%；FY28 EPS ≥ $3.66（Excel 6/23）","來源":"公司月度營運數據 + Excel/共識","漂移觸發":"連 2 季非加密交易性收入 YoY"}},{"id":"H2","text":"有資金帳戶 + 淨存款持續複利（用戶資產飛輪）","columns":{"2Y 驗證點":"有資金帳戶 30M+（5 月 27.7M）","5Y 驗證點":"FY30 帳戶 40M+ + 平台資產 $500B+","10Y 驗證點":"成為「complete fintech super-app」，跨世代留存","具體數字門檻":"淨存款年化 +20%+（TTM 27%）；帳戶 YoY +6.7%（5 月 +1.76M）","來源":"2026-05 月度營運數據（sourced）","漂移觸發":"連 2 月淨存款年化"}},{"id":"H3","text":"M&A + 新線多元化 → 降低加密單引擎依賴","columns":{"2Y 驗證點":"事件合約收入 FY26E ~$586M（Bernstein，+286%）；WonderFi/Bitstamp/TradePMR 整合貢獻","5Y 驗證點":"FY30 財管/銀行/預測市場合計收入 ≥ 加密收入","10Y 驗證點":"多線使加密占比","具體數字門檻":"Q1 事件合約 other trading +320% 到 $147M；銀行 >$2B 淨存款、Gold 4.3M","來源":"Q1 FY26 財報 + 公司揭露","漂移觸發":"任一新線整合受挫（減損/高層離職）或事件合約遭監管禁令 → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"加密結構性 deflation：BTC/ETH 進入 multi-year 熊，加密收入與相關量能長期低迷，拖累交易活躍度與情緒","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"加密收入 YoY、BTC 價位、加密 ADV","警戒閾值":"連 2 季加密收入 YoY"}},{"id":"R2","text":"預測市場（事件合約）監管風險：多州訴訟（Wisconsin 等）+ CFTC 管轄權戰使這條 +320% 引擎被限縮或按州下架","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"訴訟程序里程碑、CFTC 表態、事件合約可用州數","警戒閾值":"集體禁令或關鍵州下架 → §3.F 觸發，重評 H3"}},{"id":"R3","text":"take rate / PFOF 壓縮 + 競爭：Coinbase/Kalshi/SoFi/Schwab 在各垂直分食，零佣金結構下 ARPU 天花板","columns":{"對應假設":"H2/H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"ARPU、各線 take rate、活躍戶留存","警戒閾值":"ARPU 連 4 季 YoY 走弱且無新線補 → 砍倉檢討"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Q2（7/29）確認非加密交易性收入不靠加密回補 且 事件合約監管未惡化（Wisconsin 等禁令未擴大），或回檔至 $90-95（Fwd PE≈30x）；則轉進場·衛星 starter","irr_base_pct":9.1,"ev5y_pct":47.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":2.8,"ev5y_pct":47.0,"irr_base_pct":9.1,"max_dd_pct":-60.0,"bull_5y_price":264.0,"bear_5y_price":64.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Q2（7/29）確認非加密交易性收入不靠加密回補 且 事件合約監管未惡化（Wisconsin 等禁令未擴大），或回檔至 $90-95（Fwd PE≈30x）；則轉進場·衛星 starter","price_at_dd":109.86,"archetype":"金融","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HOOD_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
