你是 stock-analyst **v20 判斷 agent**，標的 MSTR（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MSTR","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSTR_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSTR_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":125.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001050446/000105044626000047/mstr-20261029x8kxex9912.htm"},"note":"共識約 128M（媒體報導，未經公司來源驗證）；營收未達"},{"id":"f_kpi1_gaap_operating_income","label":"GAAP operating income","value":20910,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 8-K Ex.99.1 新聞稿（同上）"},"note":"不適用（數字幾乎全為數位資產公允價值利得 20.91B）"},{"id":"f_kpi2_operating_result_excludi","label":"Operating result excluding digital asset gains","value":-2.6,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"依新聞稿毛利 89.6M 減不含數位資產的營業費用 92.2M 自行計算，公司未揭露（非公司 non-GAAP）"},"note":"無"},{"id":"f_kpi3_gross_profit_margin","label":"Gross profit / margin","value":71,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 8-K Ex.99.1 新聞稿（毛利 89.6M）"},"note":"無"},{"id":"f_kpi4_net_income_to_common_dil","label":"Net income to common / diluted EPS","value":44.75,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD per diluted share","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 8-K Ex.99.1 新聞稿（淨利 19.53B；歸普通股 19.12B，已扣特別股股利 419.6M）"},"note":"無（EPS 受 BTC 公允價值波動主導，無可比共識）"},{"id":"f_kpi5_btc_holdings","label":"BTC holdings","value":848517,"period":"截至 2026-10-25（Q3 FY2026 新聞稿，公告於 2026-10-29）","unit":"BTC","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"截至 2026-10-25（Q3 FY2026 新聞稿，公告於 2026-10-29）","citation":"公司 8-K Ex.99.1 新聞稿（成本 64.02B；9-30 約 847,666 BTC）"},"note":"無"},{"id":"f_kpi6_btc_yield_ytd","label":"BTC Yield (YTD)","value":-3.7,"period":"YTD 2026 至 Q3 FY2026（公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"YTD 2026 至 Q3 FY2026（公告於 2026-10-29）","citation":"公司 8-K Ex.99.1 新聞稿（單季值未揭露）"},"note":"無"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mstr_gross_margin_pct","label":"MSTR 毛利率","value":66.6,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSTR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mstr_operating_margin_pct","label":"MSTR 營業利益率","value":-10.96,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSTR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mstr_fcf_margin_pct","label":"MSTR FCF 利潤率","value":-4539.71,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSTR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_coin_gross_margin_pct","label":"COIN 毛利率","value":71.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_coin_operating_margin_pct","label":"COIN 營業利益率","value":5.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_coin_fcf_margin_pct","label":"COIN FCF 利潤率","value":68.4,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mara_gross_margin_pct","label":"MARA 毛利率","value":76.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MARA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mara_operating_margin_pct","label":"MARA 營業利益率","value":-126.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MARA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mara_fcf_margin_pct","label":"MARA FCF 利潤率","value":-154.08,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MARA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3350_t_gross_margin_pct","label":"3350.T 毛利率","value":99.45,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3350.T.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_3350_t_operating_margin_pct","label":"3350.T 營業利益率","value":69.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3350.T.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_glxy_gross_margin_pct","label":"GLXY 毛利率","value":-0.45,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GLXY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_glxy_operating_margin_pct","label":"GLXY 營業利益率","value":-0.28,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GLXY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_glxy_fcf_margin_pct","label":"GLXY FCF 利潤率","value":-7.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GLXY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":134.93,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-26.59,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":43.64,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（-17.44 → -17.44）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.67 → 23.67）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.77 → 23.77）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":-17.44,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":23.67,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":23.77,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":115.44,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝81.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":81.3,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":117.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝73.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":73.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":870.32,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 6776.23、現金 5905.91（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":423.57,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":58022.92,"period":"2026-11-03","unit":"USD m","basis":"市值 57152.6 ＋ 淨負債 870.32","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":500.56,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（7 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":515.49,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（11 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":115.92,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 132.65 / W52 141.15 / W104 244.56 / W250 139.73 / W250 13週斜率 1.03%"},{"id":"f_ma_w52","label":"52 週均線","value":141.15,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":244.56,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":139.73,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.03,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出企業分析軟體對手為 IBM、Microsoft、Oracle、Salesforce、SAP 等全球 ISV；AI 整合落後可能損害競爭力","source":"SEC EDGAR 10-K FY2025 Item 1 / 1A","url":"https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm","excerpt":"For enterprise analytics, Strategy competes with global ISVs, such as IBM, Microsoft, Oracle, Salesforce, and SAP.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 表示募資時與 ETP、礦商、其他持幣企業、傳統金融機構等競爭資金，競爭加劇可能提高融資成本","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm","excerpt":"we compete for capital with, among others, ETPs, bitcoin miners, digital assets exchanges, other digital assets service providers, other companies that hold bitcoin or other digital assets as treasury reserve assets","as_of":"2026-02-19","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"搜尋結果未找到 Strategy 在 BI 市場的具體份額數據；BI 市場以 Power BI、Tableau 領先，各來源估計差異大","source":"intuitionlabs.ai BI platforms / 6sense 聚合","url":"https://6sense.com/tech/business-intelligence-bi","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"STRC 成為 2026 年比特幣邊際需求的主要來源；約 80% 持有人為散戶（單一來源）","source":"inter.capital — STRC: The Preferred Stock That Became Bitcoin's Marginal Bid","url":"https://inter.capital/?p=44758","excerpt":"STRC: The Preferred Stock That Became Bitcoin’s Marginal Bid Bitcoin’s demand story in 2024 was dominated by ETF inflows. In 2025, corporate treasury buying arose along ETFs. In 2026, STRC or “Stretch” became the dominant source of marginal demand, a perpetual preferred stock issued by Strategy.","as_of":"2026-05-18","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"若 STRC 需求持續（價格 $99–$101），僅靠 STRC 收益每月可買逾 18,000 BTC 且不稀釋普通股","source":"BitcoinTreasuries.net — Behind the recent demand surge of Strategy's STRC","url":"https://bitcointreasuries.net/news/behind-the-recent-demand-surge-of-strategys-strc","excerpt":"If this demand for STRC persists, it could enable Strategy to purchase over 18,000 Bitcoin per month solely from STRC proceeds, without diluting common shareholders.","as_of":"2026-03-10","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Pepperstone：若 Strategy 無法再融資或展期票據，未來可轉債需求恐大減","source":"Pepperstone — Bitcoin Treasury Risk and Strategy's Balance Sheet","url":"https://pepperstone.com/en-au/analysis/navigating-markets/bitcoin-treasury-entity-risk-explained-why-strategy-mstr-matters-as-btc-slides/","excerpt":"in convertible notes and $8.39 billion in preference shares. Dividend and Refinancing Concerns The five tranches of preference shares pay quarterly dividends, and the sustainability of these payments has become a focal point for the market. In addition, the convertible notes mature between 2028 and 2032, with particular concern centred on the 2028 tranche. If Strategy were unable to refinance or","as_of":"2026-02-05","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"經查 FY2025 10-K Item 3，公司僅提及 Note 9 的股東訴訟，其他日常法律程序預期不會對財務有重大不利影響；未揭露反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 3. Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm","excerpt":"We are involved in various legal proceedings arising in the normal course of business. Although the outcomes of these legal proceedings are inherently difficult to predict, we do not expect the resolution of these legal proceedings to have a material adverse effect on our financial position, results of operations, or cash flows.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因素列出加密資產監管動向（SEC 成立 Crypto Task Force 等），屬產業特定監管不確定性，非針對公司的反壟斷案。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm","excerpt":"in January 2025, the SEC announced the formation of a “Crypto Task Force,” which is intended to provide clarity on the application of the federal securities laws to the crypto asset market and to recommend policy measures with respect to digital asset security status, registration and listing of digital asset-based investment vehicles, and digital asset custody, lending and staking;","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Rosen Law Firm 於 2026-06-24 對 Strategy 及 Saylor 展開證券調查（原告律所調查，非政府行動，未提起集體訴訟）；三項搜尋均未找到 DOJ/FTC/EU 反壟斷調查。","source":"Bitcoin.com, Law Firm Investigates Strategy as MSTR Drops 7% and STRC Crashes to $73","url":"https://news.bitcoin.com/law-firm-investigates-strategy-as-mstr-drops-7-and-strc-crashes-to-73/","excerpt":null,"as_of":"2026-06-24","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"MSTR 10-K FY2025 風險因素僅提及美國司法部資料安全計畫規則（2025-04-08 實施）對傳輸敏感個資至中國等『關注國家』施加類出口管制限制，及制裁／洗錢風險；未見針對關稅或實體清單的產品／供應鏈暴露揭露。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm","excerpt":"The rule effectively imposes export control-like restrictions on the transfer, sale, or sharing of sensitive data-including genomic, geolocation, biometric, health, financial, and other personal data-to or with entities in countries of concern, as well as entities and persons associated with those countries.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-Q 風險因子：比特幣有時可能集中由單一託管人保管，託管人保險為所有客戶共用","source":"Strategy Inc Form 10-Q (period 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001050446/000105044626000044/mstr-20260630.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 總營收 $125.4M，YoY -3%（Q3 2025 為 $128.7M）","source":"AMBCrypto: MSTR stock falls 6.8% in 2026 despite Strategy's $20.9B Q3 income","url":"https://ambcrypto.com/mstr-stock-falls-6-8-in-2026-despite-strategys-20-9b-q3-income-why/","excerpt":"Notably, the firm’s total revenue declined 3% year-over-year to $125.4 million, compared with $128.7 million in Q3 2025.","as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","moat_trend"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 訂閱服務營收 $62.9M，YoY +54%；總營收 $122.4M，+6.9%","source":"SEC Form FWP Strategy Inc","url":"https://www.sec.gov/Archives/edgar/data/0001050446/000119312526352145/d169243dfwp.htm","excerpt":"$122.4M, up 6.9% year over year. BTC annualized through July 27 32% Subscription services. $62.9M, up 54% year over year. 2-year windows beating BTC 64% Two segments.","as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：AI 驅動攻擊與量子運算可能使傳統密碼技術失效，構成對公司系統的新漏洞(技術面風險，非替代產品)。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm","excerpt":"Emerging technologies, such as AI-driven cyberattacks and the potential for quantum computing, could introduce new vulnerabilities in our systems, potentially rendering traditional cryptographic techniques less effective and exposing us to more sophisticated forms of cyberattacks.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Blockworks 指出 2026 年 Strategy 買幣較零星，ETF 資金流為更可靠的價格決定力量;Strategy 與現貨比特幣上市商品爭奪投資人資金。","source":"Blockworks: The Strategy playbook looks different in 2026","url":"https://blockworks.com/news/strategy-playbook-2026","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Strategy 10-K FY2025: 分析平台提供地端授權或雲端訂閱；自2025年1月起地端授權進入end-of-support週期，完整支援於2026-12-31結束；雲端訂閱通常36個月；通路夥伴持續為銷售與服務覆蓋。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm","excerpt":"We offer our analytics platform in the form of an on-premises product license or a cloud subscription; however, as of January 2025, Strategy on-premises product licenses have entered an end-of-support cycle, with full support for such licenses ending December 31, 2026. Subscriptions for cloud-based deployments typically are for 36 months and include standard support.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Strategy支援生命週期頁：地端主流支援至2026-12-31，延伸支援至2028-12-31。","source":"Strategy support lifecycle","url":"https://www.strategy.com/software/support/support-lifecycle","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"15 位分析師 12 個月目標價中位數 $233，區間 $125–$550（Ticker Nerd，頁面日期未明確，資料含 2026-09）","source":"Ticker Nerd MSTR forecast","url":"https://tickernerd.com/stock/mstr-forecast/","excerpt":"The 15 Wall Street analysts covering Strategy, Inc. have a median 12-month price target of $233.","as_of":"2026-09-15","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"StockAnalysis：平均目標價 $257.5、高 $550、共識 Strong Buy（S&P Global，15 位）","source":"StockAnalysis MSTR forecast","url":"https://www.stockanalysis.com/stocks/mstr/forecast/","excerpt":"Price Target: $257.5 (+171.45%) Analyst Consensus: Strong Buy.","as_of":"2026-09-15","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga：16 位分析師 15 Buy、1 Hold；Barclays 9/15 目標價由 $125 升至 $160，Canaccord 9/8 至 $179","source":"Benzinga MSTR analyst ratings","url":"https://jp.benzinga.com/quote/MSTR/analyst-ratings","excerpt":null,"as_of":"2026-09-15","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026 年 6–7 月多家調降目標價：TD Cowen 6/30 降至 $260、Citi 7/1 降至 $136、Mizuho 7/7 降至 $213，皆維持 Buy/Outperform；B. Riley 4/29 由 $188 升至 $200","source":"AnaChart / Placera","url":"https://anachart.com/analyst-moves/mizuho-downgrads-mstr-to-outperform-price-target-213-07-jul-2026/","excerpt":"Mizuho cuts MSTR target to $213, stays Outperform","as_of":"2026-07-07","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Ticker Nerd 修正追蹤：次一財年 EPS 90 天修正 -88.1%，0 位上修、1 位下修（單一分析師樣本）","source":"Ticker Nerd MSTR forecast","url":"https://tickernerd.com/stock/mstr-forecast/","excerpt":null,"as_of":"2026-09-15","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"未找到 FY2026 正式盈餘 guidance 的上修/下修；Benzinga 稱公司最後一次 guidance 為 2025-12-01（FY2025，下調 EPS 展望）；資本計畫 42/42 至 2027 年底 $84B 為募資目標非盈餘 guidance","source":"Benzinga earnings forecasts / Equibles","url":"https://www.benzinga.com/quote/MSTR/earnings-forecasts","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露一件進行中的 putative class action（Dodge Class Action），涉及 2025-07-07 STRK 特別股指定證書修正，董事會同為被告；公司稱不預期其他訴訟有重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A / Note 9","url":"https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm","excerpt":"We are subject to a putative class action lawsuit (related to the certificate of amendment we filed on July 7, 2025 with the Secretary of State of Delaware to the STRK Stock certificate of designations) in which our board of directors are also defendants (the “Dodge Class Action”).","as_of":"2026-02-19","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2025 年聯邦證券詐欺集體訴訟（E.D. Va. 25-cv-00861）原告於 2025-08-28 自願撤訴，案件結束（未對照法院檔案）。","source":"Kessler Topaz 案件頁（搜尋摘要）","url":"https://www.ktmc.com/?p=10298","excerpt":null,"as_of":"2025-08-28","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-03-23 8-K Item 1.01/1.02：增訂 STRC/STRK/普通股銷售協議附錄並終止舊 STRK 發行；STRC 授權股數由 70,435,353 增至 282,556,565。非併購。","source":"SEC EDGAR 8-K 2026-03-23","url":"https://www.sec.gov/Archives/edgar/data/1050446/000119312526118810/d93392d8k.htm","excerpt":"On March 23, 2026, the Company filed a Certificate of Increase of STRC Preferred Stock (the “Certificate of Increase”) to certify the authorization to increase the number of authorized shares of its STRC Preferred Stock from 70,435,353 to 282,556,565 shares.","as_of":"2026-03-23","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"financial_capital_credit_cycle#0","axis":"financial_capital_credit_cycle","section":"coverage","direction":"+","claim":"Strategy USD Reserve 為 $3.75B，約 2.1 年的優先股股息與債務利息覆蓋","source":"Strategy Q2 2026 Financial Results (press release)","url":"https://www.strategy.com/de/press/strategy-announces-second-quarter-2026-financial-results_07-30-2026","excerpt":"The Company has grown the USD Reserve to $3.75 billion, representing approximately 2.1 years of coverage reserved for preferred-stock dividend payments and interest on outstanding indebtedness.","as_of":"2026-07-30","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"financial_capital_credit_cycle#1","axis":"financial_capital_credit_cycle","section":"coverage","direction":"+","claim":"2026年5月以約$1.38B現金買回$1.5B 2029到期0%可轉債，可轉債本金由$8.21B降至$6.71B","source":"Strategy Q2 2026 Financial Results (press release)","url":"https://www.strategy.com/de/press/strategy-announces-second-quarter-2026-financial-results_07-30-2026","excerpt":"In May 2026, the Company repurchased $1.50 billion aggregate principal amount of its 0% Convertible Senior Notes due 2029 in negotiated transactions for approximately $1.38 billion in cash","as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"financial_capital_credit_cycle#2","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"Q2 2026 歸屬普通股淨損$8.62B（含$400.7M優先股股息）；今年已賣約$218.4M比特幣支付部分優先股股息；STRC低於面值100買回","source":"Strategy Q2 2026 Financial Results (press release)","url":"https://www.strategy.com/de/press/strategy-announces-second-quarter-2026-financial-results_07-30-2026","excerpt":"The Company has sold approximately $218.4 million of bitcoin year to date 2026 to fund a portion of our preferred stock dividends.","as_of":"2026-07-30","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"financial_capital_credit_cycle#3","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"軟體為2026槓桿貸款壓力主要來源：占市場13%卻占31%困境貸款；實際違約率仍低(TTM 0.93%，2026年7月)","source":"PitchBook / 搜尋彙整（Distressed & Defaults）","url":"https://pitchbook.com/tag/distressed-defaults","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#4","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"Morgan Stanley 預期私募信貸違約率因AI衝擊軟體業升至8%","source":"Bloomberg","url":"https://www.bloomberg.com/news/articles/2026-03-16/private-credit-default-rates-to-reach-8-morgan-stanley-says","excerpt":null,"as_of":"2026-03-16","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"financial_regulatory_capital_rules#none","axis":"financial_regulatory_capital_rules","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Dodge Class Action（Delaware Chancery，2025-07-21 提起）主張 STRK 修正案應經普通股股東投票，並訴董事會違反受託義務。","source":"SEC EDGAR 10-K FY2025 Note 9","url":"https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm","excerpt":"On July 21, 2025, David Dodge filed a purported class action lawsuit in the Court of Chancery of the State of Delaware against the Company and the Company’s Board alleging violations of the Delaware General Corporation Law","as_of":"2026-02-19","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"2025 年聯邦證券集體訴訟原告於 2025-08-28 自願撤訴。","source":"Kessler Topaz 案件頁（搜尋摘要）","url":"https://www.ktmc.com/?p=10298","excerpt":null,"as_of":"2025-08-28","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MSTR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":66.6,"operating_margin_pct":-10.96,"fcf_margin_pct":-4539.71,"rd_intensity_pct":19.08},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSTR","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"COIN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.01,"operating_margin_pct":5.68,"fcf_margin_pct":68.4,"rd_intensity_pct":34.52},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"MARA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":76.71,"operating_margin_pct":-126.11,"fcf_margin_pct":-154.08,"rd_intensity_pct":3.44},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MARA","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"3350.T","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":99.45,"operating_margin_pct":69.97,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3350.T","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"GLXY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":-0.45,"operating_margin_pct":-0.28,"fcf_margin_pct":-7.17,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GLXY","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"MSTR"},"financial_history":{"ticker":"MSTR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":499264000.0,"revenue_yoy_pct":null,"gross_margin_pct":79.37,"operating_margin_pct":2.11,"net_income":-1469797000.0,"diluted_eps":-12.983,"free_cash_flow":-287196000.0,"fcf_margin_pct":-57.52,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":496261000.0,"revenue_yoy_pct":-0.6,"gross_margin_pct":77.85,"operating_margin_pct":0.16,"net_income":429121000.0,"diluted_eps":2.642,"free_cash_flow":-1892525000.0,"fcf_margin_pct":-381.36,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":463456000.0,"revenue_yoy_pct":-6.61,"gross_margin_pct":72.06,"operating_margin_pct":-13.62,"net_income":-1166661000.0,"diluted_eps":-6.06,"free_cash_flow":-22139269000.0,"fcf_margin_pct":-4776.99,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":477233000.0,"revenue_yoy_pct":2.97,"gross_margin_pct":68.69,"operating_margin_pct":-8.57,"net_income":-3848152000.0,"diluted_eps":-15.23,"free_cash_flow":-22579536000.0,"fcf_margin_pct":-4731.34,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MSTR/MSTR_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Strategy Inc** | Earnings Calls | 2026-10-29

**Chaitanya Jain** (Executives):
Good afternoon, everyone, and thank you for joining us for Strategy's Third Quarter 2026 Earnings Webinar. I'm CJ, Head of Investor Relations at Strategy. Joining us today are Andrew Kang, Chief Financial Officer; Phong Lee, President and Chief Executive Officer; and Michael Saylor, Founder and Executive Chairman.
We'll begin with approximately 60 minutes of prepared remarks, starting with Andrew, followed by Phong and Michael. We'll then move to a 30-minute live Q&A.
Before we begin, I'll briefly cover our safe harbor statement. Some of the information we provide in this presentation regarding our future expectations, plans and prospects may constitute forward-looking statements. Actual results may differ materially from these forward-looking statements due to various important factors, including fluctuations in the price of Bitcoin and the risk factors discussed under the caption Risk Factors in Strategy's quarterly report on Form 10-Q filed with the SEC on August 3, 2026, and the risks described in other filings that Strategy may make with the SEC. Except as required by law, we assume no obligation to update these forward-looking statements, which speak only as of today.
With that, I will turn the call over to Andrew Kang, CFO of Strategy.

**Andrew Kang** (Executives):
Thank you, CJ. Q3 was an exceptionally strong quarter across all parts of our business. We now hold 848,517 Bitcoin and recorded a record $21 billion fair value gain on our Bitcoin holdings in Q3. MSTR share price increased 76% during the quarter, and our market cap rose to $62 billion as of October 23. STRC's 1-month volume-weighted average price was $99.27 as of the close of markets on October 23. And as we speak today, we are just $0.01 away from par. Our combined Bitcoin and dollar reserves represent 49 years of interest and dividend coverage, strengthening the credit quality of our digital credit platform.
Q3 marked our 25th consecutive quarter, more than 6 years of building a consistent and ongoing track record of adding more Bitcoin to our balance sheet. Since Q3 of 2020, our holdings have grown from approximately 38,000 Bitcoin to 848,517 Bitcoin, accounting for 4% of all Bitcoin that will ever exist. Strategy remains the largest institutional holder of Bitcoin in the world. Our Bitcoin holdings exceed that of Bit, that of the largest nation states, other ETFs and all other major DeFi institutions. We aim to actively manage our holdings along with our cash reserves to benefit both our long-term common stock shareholders and our digital credit investors.
The sheer scale of our reserves gives us a market-leading advantage to actively manage our strategy and goals through both bull and bear market cycles. Our treasury assets have grown from approximately $54 billion at the end of Q1 this year to $74 billion in this comparison. That makes strategy the seventh largest treasury among S&P 500 companies when we include all cash and Bitcoin on our balance sheet. As you know, the #21 has a great deal of significance for us. We all know that there will only ever be 21 million Bitcoin in existence. And this last quarter, we recorded an approximately $21 billion in fair value gain on our digital assets in the third quarter.
We started Q3 with about 846,000 Bitcoin valued at approximately $50 billion. And during the quarter, Bitcoin's price increased from approximately $58,700 to close around $83,600, adding $21 billion in value. We also added a net 1,666 Bitcoin during the quarter. And as a result of the recent rally in Bitcoin price at the end of Q3, we recorded a $20.9 billion fair value gain on digital assets and ended September with over 847,600 Bitcoin worth approximately $71 billion.
For the third quarter, we reported a record $20.9 billion of operating income, $19.1 billion of net income and $44.75 in diluted earnings per share. This was the highest operating and net income for any quarter in the history of the company. This milestone achievement for the company highlights the resilience and strength of our capital base and balance sheet, which allows us to weather the storm through bear markets, but also readies us for exponential growth in bull markets.
Bitcoin per share has grown from approximately 56,600 stats at the end of 2020 to over 187,700 stats as of October 23, reflecting a CAGR of approximately 23% over that same period. Year-to-date, Bitcoin per share is 3.7% lower as we effectively deployed and managed through our capital management framework with a focus on strengthening the underlying credit of our capital structure. As we enter the next stage of Bitcoin price appreciation, we will be further positioned with a stronger capital base and a more robust reserves to amplify BTC yield in the long term.
We raised approximately $5.4 billion of total capital during Q3, bringing the total year-to-date capital raise to $21.2 billion. We raised $22.6 billion of capital in 2024 and $25.3 billion in 2025, importantly, reflecting our effective and impactful access to the capital markets in both rising and falling Bitcoin cycles. During Q3, digital assets increased from $49.7 billion to $70.8 billion, reflecting Bitcoin price appreciation and the net addition of Bitcoin during the quarter.
Cash and short-term investments increased to just under $5.9 billion, including $5.8 billion of total USD assets at the end of Q3, which provides more than sufficient liquidity to meet our interest and dividend payments, strengthen our overall credit quality and provide liquidity for general Bitcoin treasury needs. Our preferred equity ended the quarter at $13.1 billion, down from the previous quarter with the execution of our stretch open market repurchase program.
Common equity increased to $55.4 billion, bringing total equity to $68.5 billion, up $23.2 billion or 51% during the quarter. Our treasury assets as of October 23 were approximately $74 billion, consisting of $68.9 billion of Bitcoin and $5.1 billion in USD assets. After taking into account $6.7 billion of convertible debt and $13.3 billion of preferred stock at their notional amounts, our net reserve is approximately $53.9 billion or approximately $67.3 billion net of the out-of-the-money converts.
Our NAV is currently 1.15x, amplification, 1.28x with a low net leverage of approximately 2.4% and our U.S. dollar assets provide 3.4 years of interest and dividends coverage at current payment obligations. We have approximately $6.7 billion of total convertible debt outstanding compared with $69 billion of Bitcoin and USD $5.1 billion of U.S. dollar assets, representing a BTC rating of 42x. 4 of the 6 converts are currently trading above par for the 2 that are at the moment below par, the earliest put date remains significantly in the future and not until March 2028.
We have substantial asset coverage and the staggered put maturity schedule gives us ample levers to effectively manage these obligations in the future. We now have 17 equity analysts covering us, all of which carry buy ratings, an average MSTR price target of approximately $248 and an average published Bitcoin target of approximately $111,000. I am pleased to announce that our shareholder proposal to move our preferred equity dividends to daily record and payment dates has been resoundingly approved by our shareholders.
The final vote reflects 99.3% of approvals of votes cast in support of the amendment. Daily dividends for stretch will begin on November 1 record date with a November 2 payment date. Strife, Strike and Stride are scheduled to follow with a January 1 record date and a January 4 payment date. Dividends will accrue on every calendar day, including weekends and holidays with payment on the next business day. The overall annual dividend amounts remain unchanged and are not impacted as a result of this enhancement. Smaller, more frequent payments are designed to reduce volatility, improve liquidity, broaden investor demand and get cash to investors sooner. Calendar day accruals also make stretch and our preps better suited to the future of tokenized products and increasingly around-the-clock markets. Thank you to everyone who voted in favor of this change.
And finally, as announced earlier today, I will be stepping down as Chief Financial Officer effective November 5 for personal reasons. It has been an honor to serve as Strategy's CFO for the past 4.5 years and to be part of such an extraordinary period of growth and innovation. I am extremely grateful to Michael, Phong and the Board for their trust and support. And to all of our employees, thank you for your hard work, perseverance and dedication. To the entire finance team, a special thank you. It has been a privilege to work alongside each of you, and I am incredibly proud of what we have accomplished together. To our shareholders, analysts and everyone who has joined us over these last 18 quarters, thank you for your time, your engagement and your support. It has meant a great deal to me.
And for the last time as CFO, I will turn the call over to Phong.

**Phong Le** (Executives):
Thank you, Andrew. We will miss you, and I do appreciate your 4.5 years of service to strategy. You've seen the company through great times and also through a couple of bear markets with a steady hand, and I wish you well in the future. The plan going forward throughout the course of 2026 is for myself to step back into the CFO and Principal Financial Officer role. Starting in January 2027, we'll split the CFO role between our software and our Bitcoin businesses, which are quite different.
Stepping into the Principal Financial Officer role covering our software business will be a long-time veteran of strategy, Reza Verosta, who currently runs operations reporting to me. and has previously been a part of the finance leadership team running FP&A. He knows our software business inside out and will do a great job overseeing that.
The Principal Financial Officer of our Bitcoin business will be myself, and also, I'll continue to be the CEO of the company. Looking forward to wearing those dual hats and looking forward to continuing to lead with strong folks in our Bitcoin business that you're all familiar with. CJ here, who runs Investor Relations and Product; and Shirish, who runs our Treasury will report to me directly. And I think for all intents and purposes, the transition will be seamless to our shareholders, our investors, our analysts and our employees. And I'm looking forward to a bright future for the company.
Speaking of bright futures, I will cover off on our digital equity strategy and our digital credit strategy with a recap of Q3 and 2026 year-to-date and why I believe we have a very bright next year ahead of us. And then I'll hand it over to Michael, who will cover our digital capital and Bitcoin overall outlook and just general strategy for the company.
So first, let's talk about digital equity. We had what I would consider to be and what Andrew mentioned, a very strong Q3. I'll start with MSTR, our common equity has amplified Bitcoin. We are built to outperform Bitcoin, and we did exactly that in the return to a bull market in Q3. Bitcoin increased 43% over the course of the quarter. MSTR increased 76% -- in addition, we added 176,000 Bitcoin since the beginning of the year. So through a bear market cycle, we were able to significantly increase our Bitcoin, and that's more than 3x the second largest Bitcoin treasury company in the world added all in the course of 3 quarters.
And it has allowed us to be the #7 ranked treasury in all of the S&P 500 peer set. As Andrew said, we raised $21 billion of capital year-to-date, another 21 number coincidentally. And we have the fourth largest issuer of capital in the U.S., again, in the Bitcoin bear market. We reduced our net leverage to 2.4%, down from 8.4% in Q2. And our downside is really now well protected where Bitcoin could fall 78% to $18,000 before we are 1x covered for our liabilities by our Bitcoin value -- asset value. And our objective still stands. We're going to double Bitcoin per share over the course of the next 7 years, and we think we are on our way to that.
So I feel very strong about MSTR and where we're able to go on a go-forward basis. As a reminder, digital equity, that's MSTR is a combination of 2 things: one, amplify Bitcoin. We're going to increase Bitcoin per share; and two, digital credit. And you've seen, Stretch, Stream, Strike, Stride and potential future innovation on top of that, for example, daily calendar day dividends. Our cap structure is really a volatility transformer, right? What do we do? We take digital capital, Bitcoin, which has a ball of 36. We reduced that ball in our digital credit stretch down to what is about 10% right now.
We believe we can reduce that further down to potentially even 5% with a 12% dividend rate. And all of that excess ball and the excess returns gets accreted to our digital equity MSTR. That's basically the formula of the company and what we're able to do with Bitcoin, which is such a rare capital asset. We're the most -- among the most liquid stocks relative to our size and amongst the most liquid stocks in the S&P 500 universe.
You'll see here, if we take a look at our options open interest as a percentage of our market cap, we're #2 in the S&P 500 universe and our daily traded volume as a percentage of market cap is also #2 in the S&P 500 universe. What does that mean? That means there's a lot of interest in what we are, which is an amplified Bitcoin company. And there still is a lot of interest in Bitcoin despite all of the attention that is growing towards AI and other related stocks.
If you take away the market cap and don't look at us as a percentage of market cap, but just on total value, we are the #17 options open interest company amongst the S&P 500 universe, and we're #18 in terms of daily traded volume. And that's a pretty big deal for a company like ours, which has grown from about $1 million to over $1 billion to over $70 billion of market cap in the course of 6 years.
Last year, we were the #1 equity issuer in the world. A year before, in 2024, we were the #2 equity issuer in the world. And this year, year-to-date, we're #4, raising $21 billion in the equity capital markets. Three AI companies are ahead of us, AI and space, SpaceX, AI and Search, Alphabet, AI and semiconductors, Intel. What does this tell you? It tells you that in any Bitcoin market, we're able to access the equity capital markets. And it also tells you that there is still significant interest in Bitcoin and digital assets, and we see a bright future for the category overall.
If you take a comparison to the 2023, 2024 bull market, in that market, we outperformed Bitcoin significantly. That's the last real bull market we saw. During that 2-year period from 2023 through 2024, Bitcoin returned 454%, MSTR returned 3.6x that, 1,897%. So as we believe we're entering another Bitcoin bull market, we believe because we're amplified Bitcoin, we have the potential to similarly outperform Bitcoin during the next year to 2 years. What's the difference between the previous bull market in 2023 and 2024 and what we expect to see in 2026, 2027 and beyond is we are a very different shaped company.
The last bull market, we had 132,500 Bitcoin, of which 37% were encumbered by Bitcoin-backed loans. Now we have 848,500 Bitcoin, nearly 7x what we had before, and 0% of that Bitcoin is encumbered by any of our debt or our preferreds. We added 18,000 Bitcoin in the last bull market. We have since added about 200,000 Bitcoin in this market. The Bitcoin floor in the previous market was $18,000. This time around is $17,000. Our BTC rating was 0.9x, which actually meant we had less than 1x coverage on our liabilities. This time, we have 4.6x coverage on our liabilities.
Our net leverage bottomed out at 110% in the past market, this time around 2.4%. And the USD duration that we had was 0. We didn't have any U.S. dollars on our balance sheet. And this time around, it's 3.4 years. So compared to the previous bear market to this bear market, we have strengthened the company significantly over the course of the last year. And what means as we exit the bear market into a bull market, we have a stronger balance sheet. And we think that creates even more opportunity for amplification and more opportunity for growth for our common equity over the course of the next couple of year bull run that we expect to see.
Our Bitcoin reserve, as I mentioned, was $132,000, now it's $848,000, $2.2 billion versus nearly $70 billion, $0 in U.S. assets versus $5.1 billion now, no digital credit versus $13.3 billion now and a net leverage of 108% versus 24%. So what have we been doing for the last year? We've been building a fortress balance sheet so that as we enter a full cycle, we think we can outperform the last full cycle that we went through. Since the Bitcoin all-time high, Bitcoin has fallen 35%, while our holdings of Bitcoin rose 33%.
So as Bitcoin price went down from $124,000 to $81,200, we've taken that opportunity to buy Bitcoin at a less expensive price and grow our Bitcoin holdings 33% to $849,000. So why do we think that there's an opportunity for MSTR to grow, not just because we believe that Bitcoin price is going to grow, but we think MSTR is a combination of 2 things, right? One is the net Bitcoin that we have on our balance sheet. And two, is the DTC dollar gain multiplied by whatever multiple you might attribute to that, which is really the functioning of our digital credit business.
So we can grow Bitcoin per share, and we can grow MSTR through 2 levers essentially. One is through increase of Bitcoin price amplified to our common equity and increase of our digital credit business, which increases the Bitcoin gain, which can be ascribed a multiple. And we think those -- both of those components will start to take effect over the course of the next couple of years. What else happens during a bull market? Well, what else happens during the bull market is we see MNAV start to expand, right? The 2021 bull market saw MNAV -- median daily MNAV at 2.28, 2023, 2.57; 2024, 2.60. We currently sit at 1.15, but we see the potential for that to also grow over the course of the bull cycle.
And as I mentioned before, ultimately, what is the goal? The goal is to double Bitcoin per share in 7 years through the use of digital credit. How does that work? And it's important to emphasize the interplay between digital credit and digital equity. If we can sell digital credit by selling stretch at $100 into the market, right, that generates amplification to the company, right? It means that we are able to buy Bitcoin and pay 12% on that digital credit and accrete all the benefits of a greater than 12% gain, which generates amplification.
The amplification increases Bitcoin per share and the increase in Bitcoin per share allows the common equity to outperform Bitcoin over time. What are the levers? Levers are lower cost of credit, which we look at very closely. The levers are higher digital credit sales, which we think we'll be able to turn on again soon. And third lever is a higher NAV. So let's talk about digital credit. I talked about MSTR, digital equity.
Now let's talk about digital credit and our 5 instruments that we have. The first, the ecosystem is scaling really fast. We're really still only 22 months into digital credit. We have 6 issuers, right, not just ourselves in a $16 billion market. Stretch is returning to health. It's trading between $99 and $100 per our commitment. And today, stretch closed at $99.99. We strengthened our U.S. dollar coverage. We've heard from our shareholders of our digital credit. That's important, grew the digital U.S. dollar assets from $2.5 billion to double to $5 billion.
And we're supporting our digital credit securities stretch. We repurchased $2 billion of stretch, and we have $957 million capacity remaining. And of course, yesterday, daily dividends were approved for stretch, which takes effect November 1 and Stripe, Strike and Stride, which should take effect January 1, and we're excited about that innovation. And we're continuing to improve our credit profile, which I'll talk through in a little bit.
So how do you think about digital credit? One thing to think about is digital credit is really a combination and alloy of Bitcoin in U.S. dollars. So much like when you take iron and you combine it with Chromium, we created an alloy stainless steel, which is stronger, which is lighter, which is better than the combination of the 2. Bitcoin with 46 years of coverage and dollars with 3.4 years of coverage creates a 60%, 40% alloy called digital credit. That's what digital credit is.
It's ultimately a better version for certain shareholders of Bitcoin and of U.S. dollars and the sum is stronger than the parts. This market, as I mentioned, scaled to $16 billion in 20 months, and it's still fairly nascent and early. It is a brand-new product never seen before in the history of capital markets, and we're pretty excited to see others come into the market. I'd mentioned our 5 IPOs that we did last year, and Strive has since IPO-ed Seta and recently SAS 2 great additional great products. MetaPlanet has announced that they plan to issue digital credit. BMNP, which is an Ethereum-based digital credit instrument was launched earlier this year.
Chad, which is the Solana-based digital credit instrument was also launched earlier this year. More was launched, and we'll see other products start to launch and Layer 2 products start to build on top of this. It is early, but it is very promising to see the digital credit ecosystem start to build out. And why is digital credit attractive? Well, if you look at the market today, there's been a lot of talk about AI private credit. The yields aren't bad at 10%, but they are opaque instruments, and they're not nearly comparable in terms of the yields that you can get on a tax equivalent basis with other forms of digital credit like the ones we've issued.
And of course, worse than private credit are junk bonds, bank preferreds, investment grade, mortgage-backed, et cetera, other instruments in terms of lower yields and different risk return profiles. As tax rates start to go up, both at the municipal level and the state level, you'll start to see that digital credit becomes even more attractive because it is a return of capital instrument. What does that mean? The return of capital means that the taxes on the dividends are tax deferred. So rather than paying taxes, it lowers the cost basis as long as you don't sell the underlying instrument.
And so you can have a tax deferred status for as long as 10 years. That compares to qualified dividends, which might pay a 20% to 35% tax. So $100 of dividends to stretch and digital credit stays at $100, $100 of dividends on a qualified dividend instrument becomes $65 to $80 and $100 of interest in earnings on a taxable interest instrument like a money market becomes half of that when taxes are taken out.
So this is one of the reasons that we think digital credit is a superior instrument. We spent a lot of time thinking about after the downturn of Q2 to stretch and some of our digital credit instruments and how to improve our digital credit. And we put a capital framework in place, and we spoke about that at length on our previous earnings call. We built up a U.S. dollar reserve that is a minimum of 1 year of dividends and interest and now is 3 years of dividends and interest.
We said that we would monetize Bitcoin for the purposes of funding the U.S. dollar reserve, servicing our debt and interest obligations and repurchasing securities. We sold a little bit of Bitcoin as a result of that, but a fraction of the Bitcoin we hold. We began a digital credit repurchase program, and we spent about $2 billion buying back stretch, and we have $957 million remaining authorized. We put in an MSTR repurchase program of $1 billion, of which we have used none of it so far. And we said we're going to keep the stretch dividend right around 12%.
We're not really going to increase it because we don't think that it will drive more demand for the product in a material way. And we don't think it's best for our common shareholders to increase the dividend obligations associated with stretch. The sixth pillar that we added over the course of the last quarter is we added USD cash, and we added 242 -- which is currently at about $242 million. So what's the point of the USD cash? I'll start with the point of the USD reserve. It is designed to support the preferred dividends and debt interest.
In fact, it is reserved and set aside explicitly for the purpose of paying dividends and interest. The U.S. dollar cash balance gives us a lot more flexibility, right? It gives us flexible liquidity so we can buy Bitcoin. We can buy back instruments like stretch, which we've been using it for and other general treasury purposes. So it's truly thought of like a cash balance that we can use for general corporate purposes to improve our Bitcoin business and ultimately to improve our digital credit, which ultimately improves our digital equity MSTR.
USD duration, this is the amount of USD that we have to cover our interest and dividend obligations rose nearly 7x from our May lows, right? So we had about half a year of USD duration previously. Now we have 3.5 years of USD duration. And we think that's quite important. USD strength is a new metric that we put in place and USD strength is the USD duration as a percentage of the blended Macaulay duration of our perpetual preferred instruments and our convertible instruments. And what you see there is the USD strength gives basically an estimate of how much USD we have to pay dividends over the Macaulay duration of our instruments, and that's increased from 6% to 40%.
So we think these are both very strong metrics, and it shows the strength of our credit and the investment attractiveness of our credit. What else have we done? We've paid dividends, 40 dividends over the last 2 years. We intend to continue to pay all of our dividends across all of our instruments. We think it's important to do so to drive confidence in the digital credit instruments, which ultimately drives confidence in digital equity and MSTR.
We introduced some of these metrics last quarter, and I want to reemphasize these metrics because they're quite important ones. And they're good ones to think about how does digital credit and digital equity interplay and how does Bitcoin ARR impact it. I'll first start with the hurdle ARR, 10.6%. You might say, why is it not 12% the same as the stretch dividend rate? Well, the hurdle ARR blends all of our instruments together. And as long as we see Bitcoin go up more than 10.6%, what that means that all of the accretion above the 10.6% goes to our equity, right?
And so that's what we saw happen in Q3 where Bitcoin went up significantly and the equity saw the accretion above and beyond the hurdle ARR. And that is one of the reasons we are able to produce amplified Bitcoin through our common equity. And then the second ARR is the breakeven ARR. This says that as long as we see 2.2% increase in Bitcoin price on an annual basis, we'll be able to satisfy our dividend and interest obligations. If we were to want to, just by selling the Bitcoin that we accrete the Bitcoin value we accrete the 2.2%.
And that means into eternity, we'll be able to continue to pay dividends and interest, which means that the digital credit works, but it may mean that the equity could underperform Bitcoin because we're not over our hurdle ARR. The last ARR is our floor ARR, 17.4% -- if we see Bitcoin going down at 17.4% a year, what that will mean is the ability to cover our credit and our debt goes down to 1x. And so at that point, the credit will get stressed below 17.4% ARR, and it means we may want to consider other different structures for the business.
So how do we think about these 2.2% breakeven ARR, 10.6% hurdle ARR, negative 17.4% Bitcoin floor ARR. If we look historically, and we look at every 4-year window back to 2015, Bitcoin has experienced a rolling 4-year ARR on average of 42.7%, which is pretty incredible, the returns of Bitcoin over the last 10 years. But more importantly, Bitcoin has beaten the 2.2% breakeven ARR in every single 4-year window during that period, right? So that breakeven ARR, our ability to pay our interest and dividends through Bitcoin increases historically has occurred every single day in that 4-year window.
And we put another metric in here, which is the expansion of the U.S. monetary supply, M2 supply, which has been 1.9% on a 4-year annualized growth basis. And it's interesting to see how Bitcoin 4-year ARR has moved roughly with that M2 monetary supply, as you might expect. We have 2 pages on our website that I thought would be useful to go through. If you ever go to strategy.com and go to the credit page, you can see these 2 analyses. And these are important analyses because what I would state is early on in the development of digital credit, people have a hard time understanding what is the risk, what are the credit spreads and how do these ARRs come into play.
And so let me explain the first page on our credit tab at our website, which really goes through the credit analysis of our different instruments, our convertible bonds and our preferred stock. So to analyze the credit, there are a couple of assumptions that we make, and you can change these assumptions on the page. First, we assume the current Bitcoin price right around $81,200 as of the end of last Friday. the U.S. dollar assets we have and then you enter 2 additional things, which is the Bitcoin volatility and the Bitcoin ARR.
Here, we decided to be conservative and put 10% in. Recently, JPMorgan released a study that ascribed a 10% Bitcoin ARR. So we thought that would be a reasonable input point and 40% Bitcoin volatility is what we've seen historically over the course of the last 4 years. When we enter those things in and we run the analysis, what are we looking for? First thing is we look at what is the BTC rating, right? What is the coverage that we have over the existing notional value of our preferred stock and our debt.
And if you go down to the most junior instrument Stride, it means we have 4.6x coverage of Bitcoin over our preferreds and our debt. right? So what is the risk that, that BTC rating goes to 1? What is the risk that we will only have Bitcoin, right, to cover 1x all of these instruments. And the risk that occurs at the end of the Macaulay duration for our most junior instrument is 6%. If you want to play around the model and put a 20% Bitcoin ARR in there, you'll see it's quite sensitive to that.
And that actually takes the risk, the BTC risk of an instrument like SRD down to roughly 1.5%, right? With that risk, we can impute then a credit spread for each of these instruments. And you'll see the most junior instrument Stride has a credit spread of 86, stretch has 54 basis points. In all of these cases, they're investment-grade instruments with that level of BTC credit. right? And the last thing we provide here is the BTC floor, right? And this one makes probably more common sense. We're at $17,662, that basically means that our Bitcoin stack will be valued at equal to our cumulative notional of all of our debt minus our U.S. dollar assets and our price.
But the big picture here is if you look at these instruments on a Bitcoin risk and credit basis, they are very low-risk instruments. Then we have another page says, well, how do you equate this to a price, right? And what is potentially a reasonable modeled price or a derived price for these instruments? And you'll very quickly understand that if you take a look at the effective yield of these instruments, right, and you look at something like Stretch, which has a 12% effective yield, Stride, which has a 14.35% effective yield.
You take out the risk-free yield, you'll see a market spread for these instruments that is much greater than the BTC credit spread that we were able to impede, right? And if you were to take that differential, you might be able to derive a much higher price for these instruments. What's the reason for showing this model? The reason for showing this model is, one, Bitcoin risk is not well understood and not well modeled today. So we thought it would be good to provide a transparent way to look at this.
And two, probably more importantly, is we are early in the world of digital credit. Early in digital credit. We're a couple of years into the products. It will probably take another year or 2 years for the market to understand, but we think there's a lot of opportunity in digital credit. And if you just take a step back, right, Stretch is a 12% now daily dividend instrument, which is 4 to 5x collateral covered. And we think it's a great option for folks out there. It has shown the ability to go through a Bitcoin bear cycle, and we're fairly bullish on this market going forward.
So let me deep dive into stretch and talk a little bit more about that. Highlights of stretch as of October 2026. I mentioned a 12.1% effective yield, $160 million of trading liquidity. It is still the most traded preferred in the entire global capital markets by a lot. The volatility is starting to come down to 10%. I believe we can get it below 10%, potentially approaching and below 5%. And I mentioned the U.S. dollar strength.
Even after buying back $2 billion of stretch, it's still $8.4 billion of notional, very large liquid perpetual preferred instrument. And the $8.4 billion of notional is backed by $5.1 billion of U.S. dollar assets, $69 billion Bitcoin reserve, 46 years of dividend and interest payments between our U.S. dollar assets and our Bitcoin reserve.
Look, we recognize that stretch had a pretty significant dislocation at the end of June. The price went down to about $75. What I'd say is the company is committed to taking actions and we took actions to get it back within its target range. Not only did we get it back within its target range, we've got it back to nearly par $99.99, and we're committed to continuing to drive the instrument to trade at a range that we think is equivalent to what we think the product is valued at.
What did we do? We introduced a new capital framework. We raised the dividend rate to 12%. We went to semi-monthly dividend payments now to daily dividend payments. And we increased the U.S. dollar assets, and we started buying some stretch back. Interestingly, we started to understand a little bit more the investor base behind stretch. In the past, we've talked about 80% retail, 20% institutional ownership as of 3/17/26.
But we realized that part of this retail looks a lot more like an institutional long-time holder than a retail potentially fast money investor. High net worth individuals, meaning folks with over $1 million in stretch represent 24% of the total stretch investment base. And what we've seen happen over the course of the last 6 months, institutional increased from 21% to 23%, nearly doubled their holdings. But probably more interesting is the high net worth individuals increased from 24% to 29% and more than doubling their holdings.
And it's important for us to look at that and it's important for us to understand that market because we think that's where potential growth is and very solid growth. Speaking of institutional holders, we are now the largest holding in the largest preferred ETF in the world by BlackRock. We represent 3.49% of PFF. If we look at BAX, the sixth largest preferred index in the world or ETF in the world, we're also the largest there and 7.58% of the weight of the total index. Mike will talk more about this. People are building on top of stretch. So the ecosystem are not just owners of stretch.
It's not just ETFs, but it's an entire ecosystem of companies in the DeFi space, stablecoins, in the tokenization space, funds and ETPs, cash and yield accounts and corporate treasuries who are building on top of stretch. And this is our market, right? The market obviously includes retail, but high net worth individuals, institutions like this are going to build products on top of stretch and will cause it to grow from $8.5 billion to tens of billions, if not hundreds of billions over time.
That's our objective. By growing a stretch, we'll be able to grow MSTR and the cycle, the virtuous cycle continues. As Andrew said, thank you to all of the folks who voted positively to move stretch to daily dividends. The calendar day accrual here is a pretty big deal, right? People will start to realize the benefits as digital credit and digital transformation of capital markets occurs. We think that's going to start happening this year, right?
Bitcoin already trades 24/7. We see equities moving in that direction. You're going to start seeing the NASDAQ move to 7-day trading towards the end of this year. Tokenization is going to accelerate that even faster, especially in the U.S. with innovation exemptions that have been put forth by the SEC. We expect that market to grow very fast, too. And what are you going to build on top of? What are your tokenized securities. Some of them may partner with or build on top of products like stretch.
Last thing I'll leave it with before I hand it over to Michael is Strategy World. 2027 is going to be back in Orlando next year, March 29 to April 1. And I invite everybody to join us there. We're going to have an awesome time. We'll run our Strategy Software Conference alongside our Bitcoin for Corporations Conference alongside the True North conference, and it will be a great time. So we'll speak to you before then at our 2026 Q4 earnings call. But go ahead and register, and I hope to see you all in person.
And with that, I will hand it over to Michael Saylor.

**Michael Saylor** (Executives):
Thank you, Phong. And I want to thank all of our shareholders for being with us today. I'm going to say a few words about Bitcoin and digital capital and the way the ecosystem is evolving. So we feel like we're entering a bull market. We bounced off the 200-week moving average. Bitcoin's dominance is growing. Institutional demand is back. The banks are embracing Bitcoin. We feel like digital credit and banking credit could absorb all the new supply. And strategy is leading on chain.
We're the most tokenized company in the digital assets ecosystem. This chart tells the story. Bitcoin has traded above a 21% premium for 78% of its history. So we look at the 200-week moving average as the base of support. And we've gone through about a 1-year bear market. We would think that we should see 2 or 3 years of a bull market at this point. We're only about less than 24 months, 18 months or so from the next halving. The halving will be a big deal, but there are a lot of other factors that are driving this.
One thing that's very auspicious for Bitcoin is that Bitcoin market cap dominance is growing consistently through the cycle. It's about 67% of the market cap of all the crypto capital assets in the world. And so Bitcoin is 2/3. Everything else is the last 1/3. It's pretty clear that Bitcoin is the digital capital network, the dominant digital capital network in the world. It will not be displaced. And that's an important thing we can build upon.
The structural catalyst for Bitcoin adoption, fiscal debasement, the money supply is going to expand, bank adoption, digital credit, capital flows from institutions, tokenization, the AI disruption, which ultimately is going to drive capital into Bitcoin. And as I mentioned, the Bitcoin halving coming up in 2028. Here, you can see the capital flows and capital returned to Bitcoin ETFs in Q3 to the tune of about $6.3 billion of inflows. We thought that was very auspicious.
This chart structurally tells a story. And the story it tells is that the government is running deficit financing. And that being the case, the money supply is going to have to expand sometime in the coming few years. There's no reasonable opportunity to do anything other than monetize the debt. So we have cheaper sovereign debt that's going to be refinanced at a higher interest rate. Either the interest rates have to come down or the balance sheet of the Fed has to expand. We don't know when this will happen or how it will happen, but this chart illustrates that it's going to need to happen.
In the aftermath of the stall of the clarity bill in D.C., we got favorable regulations and favorable guidance coming out of Treasury, the SEC and the CFTC. The treasury guidance was very positive for digital currency. The SEC guidance was very positive for digital securities and the CFTC guidance was very positive for digital derivatives and digital commodities and digital exchanges. So this is all very digital assets positive news, and it's all happened just this quarter. We track banking adoption very closely.
We look at all the major banks and the degree to which they custody crypto assets, the degree to which they extend credit, whether or not they deal with Bitcoin derivatives or wrap Bitcoin or the actual native Bitcoin and whether they underwrite it and also their stance on it. And the stance of the banks has just turned positive and has been consistently getting better. If you look at this chart, we can see we're at a 9% banking adoption December 2023. We are 24% in December of '25. We're now at 34%.
We'll continue to track this, but the banks have all the money. And this is a monetary revolution. And the most important thing for Bitcoin success is that it be legitimized as a capital asset by the financial institutions of the world and that we create credit on top of it. If we take a look at the major banks, we can see very positive moves by Morgan Stanley, Citigroup, Deutsche Bank, Standard Chartered, Banco Santander, lots of broader digital assets momentum across the board as it relates to stable coins, tokenized securities and the like.
This has the effect of derisking the asset class, accelerating institutional adoption of the asset class, sending a signal to conservative and traditional investors that it's okay to allocate to the asset class. And all of those things are just very positive for Bitcoin. So how much capital do we need in order to drive the Bitcoin price? Each week, there's about $256 million of natural Bitcoin produced by Bitcoin miners available for sale. It's 450 Bitcoin a day, we're up about $37 million a day. If you have $37 million, you can buy it all.
After the halving coming around April of 2028, that $37 million a day of supply will become $18 million of supply. That means that right now, $13 billion a year buys all the Bitcoin produced in a matter of less than 2 years, $6.7 billion would buy all the Bitcoin produced. So if you imagine the impact on the commodity price, if you knew that the production of oil was going to be cut in half or the production of gold was going to be cut in half or soybeans or natural gas or anything, that would create a price shock.
If you look at the amount of Bitcoin that's produced and you consider that number, $260 million a week. And then you consider that U.S. banks are creating $17 billion of credit in the same time period. The banks are creating incredible amounts of credit. Largely, this asset class has been unbanked for its history. And you can see that as it permeates the banking system, as the banks create credit, then that's the equivalent of buying that much or taking that much Bitcoin out of production.
And so ultimately, the creation of bank credit is what drives the prices of equities up. Bank credit drives the prices of real estate up. Bank credit drives the prices of sports team franchises up and trophy assets like paintings. If the bank will lend against it, the prices will appreciate. When you have to pay cash, that depresses prices. And so the main cycle driver here is going to be the creation of bank credit. And you can see the order of magnitude here. And it just doesn't take that much credit in order to absorb the entire natural supply, then the price has to move up in order to find a willing seller at a higher price.
As I've said, tokenization is accelerating. Strategy is the most tokenized company on chain. We didn't do anything for this to happen. This happened because we just happen to have securities that are ideal for tokenizing, right, either amplified Bitcoin or digital credit. Both of those are correlated to Bitcoin, but you can trade them one way or the other against the Bitcoin 24/7, 365. So these are very valuable in the DeFi ecosystem and the digital asset system. And of course, one thing that DeFi does very well is it creates leverage and it allows you to say, lever something 2x or 3x or 4x under very flexible credit terms.
The thing that you would want to lever would be a stable, highly liquid, low volatility, high-yielding instrument like digital credit. Levering tokenized money markets at the cost of tokenized money markets doesn't really provide you much of an effective yield. But if something pays 8%, 9%, 10%, 11%, 12% and you can borrow money at 4% and you start to put 1, 2, 3 or 4 turns on it, then you can create digital income. And so digital credit is a building block for digital income.
And by using anywhere from 2 to 4x leverage, and using stablecoins and the global marketplace, you can see how you could create a fund that pays 5%, 10%, 15% or 20% in yen, euros, pounds or dollars as you like and you can just program up and program it down. And so clearly, tokenization is interesting and the market is very innovative, and we expect to be participants in it. This gives you another snapshot and explains why tokenization is so powerful.
When you tokenize a security, it starts to trade 24/7, 365. It also starts to trade globally. It's trading in Singapore or Hong Kong or Asia or Africa or South America. It also becomes programmable. And so you can tranche it, slice it, amplify it, deamplify it. The settlement goes from T+1 to nearly instantaneous. You can apply your artificial intelligence, your agentic finance to it. Agents want to do 1,000 things in the weekend, whereas your bank doesn't want to do anything on the weekend. And generally, high-speed trading in a TradFi world is moving money around once or twice a week. And of course, in the tokenized world, that might be once or twice an hour. And who knows, it might become faster than that.
You can also -- it's also possible to compose very interesting different products. So product innovation accelerates. -- tranching risk, creating yield, converting currency, hedging, plugging into perpetuals, -- all of these things are interesting. And a lot of traditional finance markets, you can't innovate at all. It's just literally not allowed to create many of these financial products. In other cases, it would take 6 months to 3 years to get approval to issue the product.
And so TradFi markets are crippled and conventional and slow and inefficient -- and they're also beset with all sorts of capital controls that slow down the motion of money. In the tokenized markets, these -- to say this stuff happens 10x as fast is probably an understatement. Innovation can happen 100x to 1,000x as fast and the money can move 1,000x orders of magnitude quicker. And of course, what does this mean? It means the tokenized economy is delivering better financial products, like who in Japan is getting an offer of 15% yield in yen, nobody, right? You can deliver better financial products with different characteristics, orders of magnitude quicker and you can make them easier to deliver.
And so we actually think that the nexus of innovation is going to be in the tokenized economy. And we think a lot about how do we optimize our securities to be ideal for tokenizing. One obvious thing is you make it pay a daily dividend because people can actually take action every day of the year, including holidays in the tokenized economy, they can't in the TradFi economy. Why does on-chain Capital gravitate toward us? Well, stablecoins offer 0% yield. STRSC, right, has a par value of $100. It is targeted to be stable versus the dollar, and it is 12% dividend.
And of course, Bitcoin holders are seeking upside, but tokenized MSTRs amplify Bitcoin. A lot of people ask about AI. Anyone that's used it know that it's disruptive and transformational to just about everything in the world. It's eroding moats. So AI will erode moats. What moats? Well, clearly, it writes software faster. It delivers services better. It creates media. It's going to provide legal consultation, education services. It transforms services. It transforms operation. It transforms the products themselves. It makes the products better and more intelligent. It changes the nexus where you deliver products.
Lots of industries are affected. Some are extremely affected. On the other hand, what is it that the robots and the bots can't create -- they're not very good at creating land. They're not very good at creating an acre in Palm Beach. They're not very good at creating commodities, especially scarce commodities. And of course, the scarcest of all commodities is Bitcoin. Bitcoin is the greatest of commodities, and it is the great and the only digital scarcity. So as the market evolves and absorbs AI, what you can expect is lots of companies are going to get dematerialized and demonetized and degraded by AI.
Lots of products and services will be transformed. Many will go away. There will be magical products that will emerge, self-driving cars, intelligent robots, you will see web -- someone will probably figure out how to provide medical, legal, accounting, financial advice to 1 billion people for the -- a little bit more than the cost of the compute. So lots of things will transform, lots of wealth will be created, but that wealth has to flow somewhere. It's going to flow into trophy assets, trophy real estate, products that you can't manufacture with a robot or a bot.
And of course, if I do want to transfer and preserve capital, move it across time and space, then the best way to do it is with digital capital, and that's what Bitcoin is. So we see Bitcoin as the winner. We see lots of chaos and disruption everywhere else in the economy. But ultimately, the world will be wealthier. There will be explosion in productivity. And the quality of living of the consumer should increase over time. There'll just be massive disruption in careers, products, services, corporations as we get there. This chart really shows a very important idea. if you're buying semiconductors that provide intelligence, they're 650x cheaper this year than they were 3 years ago.
So there's a -- so semiconductors are a depreciating asset. We learned this in the Bitcoin mining business, where it turned out to be a much better idea to buy $1 billion of Bitcoin than $1 billion of Bitcoin mining rigs. And that's because there's a massive -- a very rapid depreciation cycle on hardware to provide any particular service, whether it's security or intelligence. So digital intelligence is going to increase abundance, but it's not going to increase the amount of Bitcoin. Bitcoin is scarce, lots of other things. Intelligent is not going to be scarce. Anything that you can create with intelligence is not going to be scarce. It's going to be quite abundant.
And so it makes sense to capitalize a company on Bitcoin, the appreciating asset, not the Bitcoin mining rig, the depreciated asset. It makes sense to capitalize on something scarce and not something which is depreciating. And so I think that the market will start to realize that. This is why, for example, digital credit backed by Bitcoin is a much better idea than private credit backed by high-performance compute data centers because you can see the hardware in the data center is depreciating. It's a very competitive market. It's going to continue to be competitive.
And on the other hand, Bitcoin is going to become less competitive. There's only 900,000 Bitcoin left to come in the next 100 years. And so even as we exponentially increase the availability of intelligence and everything related to it, we're going to exponentially decrease the availability of digital capital and everything related to it is just going to appreciate. People ask about quantum computing. Are we ready for it? Are we ready for AI hacks and the like? The answer is the industry takes all these things very seriously.
We have a Bitcoin security consortium. It has the major holders and the major businesses providing economics products and services related to Bitcoin in it, companies like Coinbase, like Anchorage, like Fidelity, like Galaxy, like Blockstream like Block, like BlackRock, like Arc. We meet regularly. We support Bitcoin-related security research. We coordinate. And our focus is on making sure that we contribute to the stability and the security of the overall protocol. We'll continue to do that. There have been dozens and dozens of things people have been concerned about with regard to the network over the past 15 years.
Over the coming 10 or 15 years, I'm sure there'll be another few dozen things that will pop up. as they pop up, some of them are real, some of them are just FUD. And as they evolve in consensus forms that it makes sense to address them, then we're ready and able to do so. And I think this is functioning in order to provide comfort to any Bitcoin investor that all the companies in this industry take security seriously, and we're engaged and coordinating.
Future outlook. Bitcoin is 10 basis points of the world's capital assets. You can see it's de minimis 0.1%. We expect over time that it will grow to be 1%, and then it may grow to be a few percent. But you can see Bitcoin only needs to be a few percent of the world's assets to be extraordinarily successful. And the thing that's going to drive that growth is institutional adoption, Bitcoin, the legitimization of the asset class, the creation of credit, the creation of equity and other instruments on top of Bitcoin, the applications of Bitcoin.
We're headed toward a $100 trillion industry. That's where we think we'll get to. And $100 trillion when we get there, may still only be single digits of global wealth. And so it will be a part of the capital structure of the world, but $100 trillion is a lot of money. What are the applications? Bitcoin is digital capital. Digital equity built on top of it is the second application. Digital credit instruments, as we've talked about, is a third application. Digital debt, debt instruments based on Bitcoin, a fourth application. Digital currency, stable digital assets that are backed by Bitcoin will be a fifth application.
Digital money, something that's a stable currency equivalent that's paying you yield is another major application. Digital derivatives, perpetual futures, crypto derivatives, all flavors of options and perpetual contracts, another application. And then digital collateral, the capital that we embed into our robots that we embed into our agents that we embed into exchanges that we use as financial infrastructure for all digital commerce. All of these are very compelling applications, and they all require digital capital and therefore, Bitcoin in order to function effectively.
I think it's reasonable to consider 2 other industries when we look at the way the Bitcoin industry will grow. If we start with oil, the oil industry had a first application. It was kerosene and people use kerosene for light. The original application of oil was reading lamps at night. And it provided a utilitarian value to the middle class such that they could afford light at night. because before that, you're looking at whale oil and whale oil was absenely expensive compared to kerosene. Eventually, though, that light application was displaced by electricity.
It was obsolesce and the oil industry moved on to gasoline and then fuel oil and then heating oil, jet fuels, of course. And of course, it fueled cars that didn't exist when it was invented. It fueled planes that didn't exist when we first discovered kerosene. And then we saw plastics and fertilizer and asphalt and then we had lubricants and synthetic and then we had fabrics, nylon and polyester and licra. And then it became a feedstock to pharmaceuticals and cosmetics and even food and coatings.
And so if you think about all the applications of oil, they're everywhere, all around us, and they all started with kerosene. And the entire industry was a bunch of very innovative companies that figure out how to crack a barrel of oil into all of those different things and sell it to all of those different downstream manufacturers or service providers. Now we take electricity, it's a similar story.
The first application was the electric light bulb that was the killer app. But eventually, electricity drove motors and factories and refrigerators and air conditioners and radio and television and telephones and computers and Internet, data centers, electric vehicles. And of course, now it's AI, things for us. And when they started with a light bulb, nobody ever thought that eventually we would have Starlink and the AI to be thinking for us. But it's a very logical evolution. And when we look at Bitcoin, the first application was peer-to-peer cash. okay, how do I buy a pizza with 10,000 Bitcoin or buy 2 pizzas with 10,000 Bitcoin.
But it's a mistake to think that the industry stays mired in that one first use case. That would be like electricity just sticking with light bulbs and oil sticking with kerosene, right? What we see evolving is digital capital, digital equity, digital credit, digital debt, digital currency, digital money. That creates digital income. You want 20% in yen, euros, pounds, dollars, pick your currency, digital derivatives, a 10x perpetual, right?
Digital collateral. How do I actually put this collateral into my prediction market exchange, into my commodities exchange? How do I -- it's an ideal collateral to fuel every financial application in the world. Digital identity. You can use Bitcoin to create digital identity with public-private keypairs. Digital authentication follows next and then digital commerce. And so Bitcoin is the basis of a whole set of digital applications, great ideas, outgrow their first use case. We won't be a $100 trillion industry based upon swapping Bitcoin for pizza.
We will become a $100 trillion industry based upon hundreds or thousands of products created by thousands of companies, all to solve a different problem in the world of digital finance and digital commerce. And we're very enthusiastic to be part of that, but we expect many other companies to follow in our footsteps. And that takes us to Bitcoin treasury companies. There are 4 issuers of digital credit right now. They've issued 13 securities that are all based on Bitcoin. Those BTC treasury companies like Strive, like MetapPlanet, like Smarter Web, those treasury companies have acquired 220,000 Bitcoin this year. That works out to 165% of all the Bitcoin mined this year.
So the BTC treasury companies are buying 1.6 Bitcoin for every Bitcoin created by a Bitcoin miner. You see a supply shock forming. It's right here in front of our eyes. As the BTC treasury industry grows, their demand for Bitcoin grows, that drives up the price of the Bitcoin, driving up the value of their reserves, improving their credit, improving their equity, allowing to raise more capital. buying more Bitcoin, growing the industry, allowing them to create new innovative products like SATA, like SaaS, like more, like Stretch Paying Daily.
There will be a continual set of new products. Those products will serve new investor bases. They will broaden the investor base that attracts liquidity, that legitimizes the industry that will legitimize digital credit, that will legitimize digital equity, that will legitimize digital capital. We're not competitors. We're cooperators. We're all cooperating in a virtuous cycle and a virtuous relationship in order to strengthen digital capital, digital credit, digital equity and every other digital product or service that is backed by Bitcoin.
And I laid out a dozen, there will be hundreds of thousands. We're very early on in this industry's development. You can see, if you look at this graph of issuers, multiple issuers just make the category more investable. There are a lot of investors they can only have up to 5% exposure in issue or 2% or 1%. So if there are 3 issuers, they'll have 15% exposure. But if there's one issuer, they'll have 5% exposure. So we need multiple companies in order to diversify the risk in order to allow all of the capital investors to comply with their mandates and manage risk per their risk models. And so issuers are critical to growing the industry, but also issuers create innovations.
The issuers -- like we're not in a position to create a digital credit instrument in pounds, but Smarter Web is. We weren't in a position to create a daily dividend, but Strive was. And so new issuers will be able to do different things. MetaPlanet is creating new innovative instruments for the Japanese market. We're not in a position to do that. So all of us are working together in order to grow the global market. And as securities begin to get tokenized, then that will make it easier for all of the global players to participate in other markets and to innovate in a more rapid fashion.
I see this as very auspicious for the space. We can expect that AI is going to continue to push the boundary. It's pushing the boundaries of mathematics. It's pushing the boundaries of physics. It will push the boundaries of finance. We have designed all of our major credit instruments using AI. AI is critical for investors to understand them. It's critical to the models for pricing them. It's critical to solving the product design, the securities, the legal issues, et cetera. I think that the growth of AI is very auspicious to the growth of digital finance, and we just see this as a big plus for the industry in general.
So at this point, we have instruments for every time horizon. What I would say is if you don't need your money for 4 years and you're an equity investor and you believe in digital credit or you want amplified Bitcoin exposure or you have to buy an equity instrument, you would buy digital equity like MSTR. If you don't need your money for 4 years and you want to invest in something without counterparty risk, you would buy digital capital, you'll buy the Bitcoin. If you're willing or you need to buy it in an exchange-traded wrapper, you'll buy an ETF like Bid. That's fine.
There are many people that are credit investors. And if you're a credit investor and you have a long time horizon, like more than 4 years, maybe you want to put a piece of credit in a retirement portfolio or a trust, a family trust and you want to hold it for 30 years. Well, then we have instruments like Strife, Stream, Strike, Stride, SATS. All of these are long-duration perpetual credit instruments. They'll pay you a fixed dividend at par, whatever that dividend is 10% or the like. And you can lock in that yield for a decade or 20 years or 30 years. And that makes total sense if you've got that time horizon and you don't need the money back in the next few months or few years.
You will probably absorb a bit more volatility in order to get that duration, but it's like holding a 20- or 30-year bond, a government bond as opposed to holding a 1-month or 3-month T-bill. And so those perpetual instruments meet a need in the market. If you don't -- if you have money to invest for 4 months to 4 years, -- we would say you're a treasury credit or a shorter duration digital credit investor and there are instruments like STRC, what we offer or SATA, what Strive offers. And that's for a shorter duration investor. If STRC falls off of par or breaks below par, then the company is going to use all of its capital and its best efforts to return it to par as soon as it can.
And I don't think we would ever represent, for example, that we could do it in 4 days or 4 weeks because that might be pushing the edge of the envelope. But you can see that here in 4 months, we've shown that we can -- and we think that it's a general reasonable expectation that the company will return STRC to par within 4 months if it were to lose or fall below par and out of our trading range. And we would do that by buying it back. We would do it by adjusting our cash balances.
We would do it by adjusting our capital structure, et cetera, whatever we needed to do that we thought was rational at the time. Now if you need your money back in the next 4 months, maybe you have money and you want to invest it to get some yield, but you need it back in 5 days. You're a money market investor, and we would recommend that you put your money in the money market. Right now, money markets pay SOFR or something like that. We don't have a digital credit product that is for people that want to invest money for 0 to 4 months.
But partners are generating and innovating. And in the digital asset space, people are creating digital money type instruments. And over time, I expect that Bitcoin treasury companies will create digital money type instruments that will meet this need. And so that's an opportunity for all of us that we're very enthusiastic about. What are we? Well, we are emerging as the Central Bank of the crypto economy. At this point, we're the best capitalized public entity in the crypto space. We have about $74 billion of capital right now. That would put us 56 against -- as the 56th largest central bank in the world.
And we're moving up these rankings at a rapid rate. We will continue to grow. And our job is to bridge the TradFi market with the DeFi market, the Bitcoin, the BTC market with the fiat USD type market. And so we will -- and we expect that we will bridge the gap between Bitcoin and stablecoins, between capital and credit, between TradFi and DeFi. And we will work to strip volatility from Bitcoin for people that don't want ball, and we will amplify volatility for derivatives traders or equity investors that want more ball. We will extract yield, we will manage risk.
And we will convert currencies, right, converting BTC into a USD instrument or a euro instrument or something similar. So it's a very powerful business. We think that if you want to do this, you need a tower of capital, in this case, $74 billion. We think it's a big -- it's a very defensible moat if someone wanted to invest $100 billion or $200 billion or maybe even more than that in order to compete with us, they would have to buy that much Bitcoin.
And if someone went into the market and tried to buy $200 billion of Bitcoin right now, it's quite likely that our credit spreads would compress, demand for our credit would explode, our equity premiums would expand, demand for our equity would explode. The price of Bitcoin would appreciate, our reserves would appreciate. And our overall company would grow faster than they could buy Bitcoin, probably much faster. So it's very difficult for anyone else to displace us in this position because we've established this large defensible Bitcoin holding.
We intend to use those reserves substantial BTC reserves and substantial USD reserves in order to create the digital credit, which bridges all the global markets, the global credit markets, all the currency markets with the crypto markets, with other forms of capital and with the traditional finance markets. We think it's a great business opportunity. It needs to be done. And you can already see based upon our success raising capital in the TradFi market and our success tokenizing our securities in the DeFi markets that we're making great progress toward this ultimate vision.
And with that, we're ready for Q&A, and we look forward to answering your questions. Thank you for staying with us.

**Chaitanya Jain** (Executives):
Thank you, Michael. I'd like to welcome all our Q&A guests and invite them to come on video. We look forward to hearing your questions. We go one at a time. I'll call your names and you can direct your questions to the management team. For the first question, I would like to invite Andrew Harte, Director and Fintech Analyst at BTIG.

**Andrew Harte** (Analysts):
Good work this quarter. So Slide 26 frames the stronger balance sheet today compared to the previous bull market. And Phong, you talked about the balance sheet enabling strategy to take better advantage of a bull market with increased optionality. So I would love to hear what exercising that optionality looks like? And what are the key differences in how you plan to manage the business in the next bull market versus the prior ones?

**Phong Le** (Executives):
Well, I can start, and I'm sure some others can join in. The big difference is, one, our Bitcoin balance is almost 7x larger is fully unencumbered. We have U.S. dollar balance and all of those things allow us to issue additional credit, which we weren't able to do before, right? Before, we were relying on primarily leverage through convertible bonds. We've talked at length why we think that it is inferior. One is there's just a limit to the size of the market of convertible notes. It's a less liquid market. It's over the counter, means retail can't participate.
Amplifying the company through perpetual preferreds is far superior, and now we're able to do that on the back of nearly $70 billion of value in Bitcoin, which means that if we wanted to, we could raise $10 billion, $20 billion, $30 billion through perpetual preferreds, which if we pay 10%, 11% out at and Bitcoin goes up 30%, 40%, that creates amplification for the company and it grows the equity. So that's the big difference is we're a much larger company, and we have now a new strategy, which is digital credit.
And Mike mentioned, that's just issuing digital credit ourselves, then there will be companies in the DeFi space and the TradFi space building products on top of digital credit. No one is building products on top of our convertible notes, right? Now we've got DeFi. We've got traditional finance companies that over time will issue stable coins. They'll produce returns, putting digital credit behind it. So I think the opportunity is pretty tremendous over the course of the next 1, 2, 3 years.

**Andrew Kang** (Executives):
Yes. The point I'd make is you need a lot of capital in order to create a lot of credit. And so if you have a lot of capital, like we could create $10 billion, $20 billion, $30 billion of digital credit right now with our existing capital structure without raising any more equity capital and without Bitcoin appreciating. So we have a lot of credit capacity on the balance sheet now. And of course, we can create different types of credit. Are you creating BTC 5-rated credit, BTC II rated credit, right? The amount of risk in the credit and the amount of volatility in the credit is important to various types of investors. So one type of credit we're very interested in is digital money. How do you create 0 volatility digital credit?
And of course, you need a lot of capital to create 0 volatility digital credit. You need a lot of capital to create of all 5. And so we think that we have -- we are using our capital as a very powerful asset, and we're positioned for the next bull run, but the company's optionality is quite powerful now because we don't have to rely upon Bitcoin to do the heavy lifting or the equity to do the lifting. We could use our balance sheet to do the heavy lifting right now.
And that means we can meet a certain credit obligation or we can sell a certain type of credit to a credit investor or we can create new forms of credit with different volatility and risk profiles and different liquidity profiles as well that will also tap in and activate new markets. And so we're excited about that.

**Chaitanya Jain** (Executives):
Thank you, Andrew. Next, I'd like to invite [ King Hoi ], Founder and CEO of Treasury.

**Unknown Analyst** (Analysts):
I have 2 questions, if I may, one about equity and one about credit. On the equity side, you sold more than $5 billion of equity this quarter through ATM and the majority of that went into raising the cash balance and into buying back STRC. And it's clearly needed to stabilize the capital structure, which you've done. Now that is the case, I would love to get maybe some guidance or ladder even about how you think about where the equity ATM is accretive so where you would really switch it on again to buy Bitcoin. And on the other hand, if the nNAV stays sort of where it is or lower, where at which point it would make sense to actually sell STRC, assuming it goes above par again to buy back actually MSCR itself?
And then on the credit side, if I may, clearly, you've done a great job over the quarter of stabilizing STRC, bringing back very close to par, below par. And actually, it surprised me a little bit why it hasn't been a bit stronger given the buybacks you've done, the cash you've raised. And I was wondering from your conversations with credit investors, institutional investors, what is it that would make them really buy this in size? Is it the coupon? Is it the cash balance? Is it some structural features? What would make it happen? And what would get us to $100 billion or $1 trillion kind of asset, right? Is there sort of a key feature that will allow it to happen from where we're sitting now?

**Phong Le** (Executives):
I can start, and you put like 5 questions in there, King, so I'll try to get to all of them. The first question, what takes Stretch to stabilize at par? And why didn't it happen faster? First, I'll say is stretch went from a $2.5 billion IPO to $10.5 billion in the course of about 8 months. You might be able to argue that we overcharged it, right? And we brought in some capital that wasn't the most healthy. And so I think it overcharged, dislocated from par went down to $75, money exited, money looking for accretive principal growth entered, and we had to go through a cycling of the instrument. And so it ended up taking from June to now about 4 months to do. I think we'll be at par as to get par pretty closely. But I don't think 4 months is unreasonable in an instrument that grew that fast. So that's one.
Two, how do we want to buy Bitcoin. The primary way to acquire Bitcoin is by issuing digital credit, STRC or other instruments that start to grow over time or other digital credit instruments. And when we raise $1 billion to $2 billion a month on a stretch, I think one thing we'll likely do this time is we'll put some of that into the U.S. dollar reserve, and we'll use the remaining to buy Bitcoin. And then the idea would be to issue equity above 1x NAV or greater to pay the dividends and interest on the digital credit, right?
But the primary way to buy Bitcoin is by issuing digital credit, put into Bitcoin, pay a 12% dividend and get the returns on Bitcoin of 30%, 40%. Will we use MSTR to -- will we issue MSTR to buy Bitcoin, Perhaps, right, if the mNAV starts to expand aggressively and we see an opportunity. But the primary way to accrete Bitcoin to the company to create amplification and increase Bitcoin per share is going to be through digital credit.

**Chaitanya Jain** (Executives):
Thank you, King. Next, I'd like to invite Alex Thorn, Managing Director and Head of Research at Galaxy.

**Unknown Analyst** (Analysts):
Thank you, Michael, Phong and Andrew for having me on here. I also wanted to ask about your digital credit instruments. STRC and STRF have traded back towards their face value. Certainly, to some extent, with the help from your buybacks and your cash forward, I think very prudent. But STRD and STRK are still trading around 70. And in Europe, STRE is below 80 and it barely trades at all. What are your plans for these other prefs that aren't trading back to face value? And for the one in Europe, are you planning to push to get it uplisted to a major exchange?

**Phong Le** (Executives):
We'd like them all to trade strong. The focus right now is getting stretched back to par. I think we're close to that. By the way, once it gets to par and maybe to add to my answer to King's question, I think that will create a lot of confidence in the instrument when they see something that dislocated and came back to par within 4 months and actually shows the resilience of the instrument on a go-forward basis. The other thing is I do think the calendar day daily dividends will help, right?
We've been told by some large institutions that want to invest large pools of capital that are currently undeployed where they might put it into a T-bill, earning 400 basis points, and they can put in something like this and earn 12%. I think all of those types of things will grow stretch, right? And so that's priority #1, get stretch to par, grow stretch so that we can buy Bitcoin, amplify the stock and accrete the common. So that's sort of priority one.
I do think as that happens, the stock goes up and as Bitcoin starts to grow again, that the other instruments that you're talking about, Stride, Strike will start to grow. Stream will start to grow, right? Those are ones that are more sensitive to Bitcoin price. Stretch is less sensitive to Bitcoin price. So we're not dismissing those products. We're focusing on stretch and then those other instruments will start to grow over time. And we have -- when you think about our buyback capability, it's not just limited to stretch, right?
We could consider if the price stays dislocated on those, looking at those too. And then Stream is -- the euro listed one is a little bit of a challenge, right, because it's currently on an unregulated exchange in Europe, which means that it can't trade with retail. And so we need to find a way to improve and correct that product over time. So we haven't forgotten about it. But the European regulatory environment, as many probably know in the capital markets is not nearly as easy to work with as the U.S. regulatory environment.

**Michael Saylor** (Executives):
I think there's one other point worth making, Alex, which is all of those instruments dislocated when STRC dislocated. So they all recovered to a pretty similar level. I think they were all up like about 30%. So the recovery of STRC actually was correlated or led or it either dragged or it was comparable to the recovery of Strife, Stride and Strike when it happened. So they all benefited from what we're doing. Right now, our focus is make sure that STRC trades well.
But then to Phong's point, we think we're entering a new regime. So once we get into a stable point of equilibrium and then we migrate them all to daily dividends, then I think that people will probably start to give all the other credit instruments a look or more of a look, and we're optimistic about their future. They do all represent optionality for us. And so -- and also, they all represent a good tokenizing opportunity for us. And so as they get tokenized and as the market becomes more fluid, we think that they could appreciate in value.

**Chaitanya Jain** (Executives):
Next, I'd like to invite Pete Christiansen, Director of Digital Assets and Fintech Services Research at Citi.

**Peter Christiansen** (Analysts):
Great to be on the call again. Michael, question is, as you scale -- as the business scales further, you're not just allocating capital into Bitcoin, but you're also increasingly creating new financial claims against Bitcoin. I'm just curious, how do you think about the risk that the strategy success accelerates the financialization of Bitcoin itself, introducing leverage, duration, counterparty exposure into an asset that historically has derived much of its appeal from having none of these characteristics. Just curious your views there.

**Michael Saylor** (Executives):
I think I ran an analysis on institutional adoption of Bitcoin, and it was like 12.2% or 12% or something between the Bitcoin treasury companies and the ETF issuers. And if you roll the clock back about 5 years, it was like 3% or 4%. So institutional adoption has moved from like 3% marched up to 12%. But that means 88% of this is still either retail or native crypto. I think it's derisking the industry to go toward greater institutional adoption because that legitimizes the asset. It's a good thing for the asset that BlackRock holds some of it.
And every time an institution becomes engaged, whether it's Morgan Stanley or Wells Fargo or Charles Schwab or any time there's a company like ours, I think that derisks the asset because those institutions are all regulated, compliant, public, audited -- they represent hundreds of millions of beneficiaries, right, rippling through every institution in the world. So the way I look at it is if 100% -- if 95% of the asset was retail, not in institutions, then you don't have a lot of strong institutional benefactors and patrons.
And of course, it's the institutions that represent Bitcoin in Washington, D.C., and they represent it in Brussels. And it's the institutions that actually solve the legal issues, the accounting issues. It's the institutions that finance the more difficult development and the institutions are financing all the security issues. It's the institutions that have access to the frontier models, and they can actually do cybersecurity checks with the frontier models, right? So I think actually, it's a good thing, right, for institutional growth to progress.
And so I don't see it representing a risk at all. If anything, it's expanding the capital in the ecosystem. It's creating a constant bid. By the way, it's damping ball. The volatility of the asset was about 80%, 85% when we got into this industry in 2020 and institutional adoption was 4%. And today, the volatility is 40%, institutional adoption is 12%. And it doesn't take a rocket scientist to figure out like how do you damp volatility? Well, one way you damp volatility is there's an entire options market that formed on bid like a $30 billion options market.
So if you want to go and damp the volatility and sell the volatility and strip the upside and then strip the downside, then you need mature derivatives markets. And so the mature derivatives markets only exist. They exist because Coinbase is bringing the crypto derivatives market to the U.S. as an advocate. They bought Deribit. They exist because BlackRock advocated for Bit and then all of the derivatives on top of Bit only exist because of BlackRock. And they exist because MSTR created a very large regulated derivatives market and MSTR stocks and its equity. So I think that the institutional actors, both the funds -- really, there's 3.
There's like 100 funds that are very important actors. There's Bitcoin treasury companies, 100 of us, but especially a dozen that are very active that are important actors. And then they're are all the digital exchanges, right? And the more digital exchanges that -- if Schwab trades Bitcoin, that's good for Bitcoin. If Coinbase gets bigger, that's good for Bitcoin, right? What you want is lots of big regulated public companies in every market, right? You want them in Japan, you want them in Europe, you want banks, exchanges, brokers, corporations and funds, all of them to be handling the asset, they all solve a different problem.
They create legitimacy, they solve the compliance issue. They solve -- there I'm an investor and I live in the U.K., and I have money in a retirement account, and the only way to buy Bitcoin is by buying MicroStrategy stock in the year 2020 because that's literally the only legal practical way to do it, right? So we're all creating bridges to Bitcoin in a very complicated world where there's a lot of capital that's stranded, and we're solving problems like the accounting problem. There are so many different issues that have to be solved. And there -- and no one company can do it all, but -- but a retail investor normally struggles to solve these problems.
And so I think the asset class is growing up, and it's a good thing. And what it means is the vol will fall, the capital and liquidity will increase. The price will go up. The size of the industry will go up and the number of beneficiaries will expand and the number of companies participate will expand and the products and services will expand. And those are all good things. That's what you want. It's going like saying, well, in the electricity business, I'm really concerned, Mr. Edison, that other companies also want to create electric motors or use electricity. I'm really concerned, Mr. Rockefeller that other people want to actually build petrochemical products that use oil.
Doesn't that bother you? We only want retail people to have barrels of oil in the backyard. And of course, no industry is going to grow until you have thousands of companies that are doing very intricate things to add value to the base product. The base product is Bitcoin. And it's like oil got financialized, electricity got financialized and Bitcoin is getting financialized and it's not a bad thing. It's a good thing. right? And it will turn out to be a great thing. So I look forward to that.

**Chaitanya Jain** (Executives):
Thank you. For the last question, I'd like to invite [ Scott Melker ], also known as the Wolf of Wall Street.

**Unknown Analyst** (Analysts):
Thanks, CJ. Thank you, everybody. So Michael, you made a very compelling case earlier for 24/7 global programmable instant settlement on MSTR, STRC via tokenization. But in your own slide that presented that, it basically said these tokens are issued by third parties and not by strategy. So there's also an irony, obviously, which is that effectively, none of these products right now are even available to Americans. They're generally only available offshore. And they don't actually pay the cash dividend like STRC does. They generally rebase or reinvest in the underlying assets.
And to continue on, today, it's being reported that NASDAQ is actually urging companies not to participate in tokenization. So with all that in mind and knowing that we have a constant pendulum swing of a regulatory environment, do you have plans for a strategy to issue its own tokenized MSCR and preferreds on chain open to U.S. investors with dividends paid on chain? And if so, what would allow you to do that and when?

**Michael Saylor** (Executives):
Well, it's an evolving industry. And I would say we're kind of like year 1 or year -- somewhere between year 0 and year 1, especially in the U.S. And we want to do everything we possibly can to support the industry. So it's -- we have been active participants in the offshore tokenization world, supporting companies like Apex and Saturn and cheering them on and enthusiastically watching what's happening there. In the U.S., that's an evolving situation where the protocols are evolving, the platforms are evolving, the compliance rules are evolving. It's not clear to me that every issue has been settled, right, as you rightly perceive.
So our view is there probably isn't a single path. There's not like a single token standard. There are going to be ecosystems that build on BNB, on Ethereum, on Solana, on various open chains like that. There are going to be systems that probably evolve around more proprietary networks or closed networks or compliant networks, and there'll be flavors of compliance that will have more KYC and less flexibility. And there will probably be some walled garden token systems where you can tokenize it, but you can't take custody of it and you can't move it outside of the system.
My view, of course, is that the promise of tokenization is creating a free market in credit and custody and collaboration and composition and a completely free market. But you and I both know, not everyone shares the same view of the benefits of a free market and where they draw the line on constraints. I think the short of it is you're going to have institutions like us, like BlackRock. Larry Fink has been a major advocate for tokenization, like he's literally been giving speeches every year for -- he's been on the forefront of this. There are going to be institutions like us and BlackRock, and we're going to be advocating for the most powerful progressive tokenization rules on a global basis and especially in the U.S.
I think that there's not going to be one particular platform or one particular approach. We're going to work with everybody as best we can. And then I think the market is going to pick a set of approaches it likes, but it will be a hybrid process where it will be a dialogue or a dance between the regulators. And you'll see TradFi. There's a TradFi view, which is more conservative. There is a digital assets view, which is more progressive. There are going to be progressive regulators in certain jurisdictions, and there are going to be less progressive or regressive regulators in other jurisdictions.
We're going to be enthusiastically working to polish our securities or to structure our securities to make them the best products we can possibly create. I can't tell you what kind of digital assets initiatives we'll take now before we take them. But I think you can be sure that we're studying the entire market in every way, and we're asking the question, what do we need to do? What kind of securities do we need to create that are optimal for to be tokenized? Can we change existing securities to make them better for being tokenized? How can we support digital exchanges and innovators. I mean there's a whole industry of innovators, right?
There are the people that are tranching risk, the people that are trading tokens, the people that are trading them, they are the exchanges of the custodians. We're talking to all of them, and we're trying to figure out how we can best be constructive and supportive in a responsible fashion. If I knew the answer, I would give it to you. But I think that as soon as we have concrete offerings for U.S. investors, you'll find out from us. And meanwhile, this is one of those things where you grind the AI really hard and you have to find what's the right legal solution, the right compliance solution, the right practical solution and the right economic solution.
And then you have to figure out how to do it without fragmenting liquidity or creating fragility or new types of risk, right, or layered risk, and that makes it complicated. So we're enthusiastic and we're optimistic. But I really think the elephant in the room here clearly is that the U.S. capital markets have not converged on a tokenizing standard and a set of norms yet. And the market participants are all working their way through that. But I would also say in the next 12 months, I think we'll probably see a set of standards evolve and a framework and a structure. And when it happens, it will happen pretty quickly.

**Chaitanya Jain** (Executives):
Thank you, Scott. That concludes the Q&A. I'd like to thank all the guests for the questions and all the attendees for joining in live. I believe we had over 50,000 people across various live streams. I'll now turn the call over to Phong for any closing remarks.

**Phong Le** (Executives):
Thank you, CJ. Thank you to the guests who joined us today with your thoughtful questions. Thank you, Andrew, for your service to the company over the last 4.5 years. And thank you to everyone that joined us this evening for our Q3 earnings call. I look forward to seeing everybody again in about 3 months, and take care.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MSTR_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Phong Le｜guidance：美元準備金目標存續期 2–3 年（原話："our target is to be somewhere between 2 and 3 years."）
- 2026-07-30｜Phong Le｜commitment：美元準備金最低維持 1 年股息利息覆蓋（原話："we're going to keep 1 year of minimum"）
- 2026-07-30｜Phong Le｜commitment：Phong 重申美元準備金最低 1 年（原話："our minimum will be 1 year."）
- 2026-07-30｜Phong Le｜guidance：STRC 股息率目前計畫維持 12%（原話："So our current plan is to keep the rate right at 12%."）
- 2026-07-30｜Phong Le｜commitment：不打算降 STRC 利率來拉回面值（原話："We're not planning on decreasing the Stretch rate"）
- 2026-07-30｜Phong Le｜guidance：公司目標讓 STRC 回到 $99–100（原話："It's for Stretch to trade at $99 to $100 over time."）
- 2026-07-30｜Phong Le｜risk：STRC 現價約 $89.50，低於目標區間（原話："Stretch is now trading at about $89.50."）
- 2026-07-30｜Michael Saylor｜guidance：Saylor 以 IPO 後 70 交易日到面值類比，推算時點約 9/8（原話："that would put us around September 8"）
- 2026-07-30｜Michael Saylor｜commitment：Saylor 表示確定會讓 STRC 回到面值（原話："We're certain that we will return STRC to par."）
- 2026-07-30｜Michael Saylor｜guidance：買回規模與速度仍在摸索（原話："We're currently in a discovery process"）
- 2026-07-30｜Michael Saylor｜risk：STRC 市值與面額約 $1.2B 缺口（原話："So there's about a $1.2 billion dislocation."）
- 2026-07-30｜Michael Saylor｜commitment：STRC 低於面值就不發行（原話："we can't sell it at par, we're not going to sell it at all"）
- 2026-07-30｜Michael Saylor｜capital_allocation：目前不發行 STRC（原話："we're not selling Stretch right now"）
- 2026-07-30｜Michael Saylor｜commitment：公司不會暫停股息（原話："The company is not going to suspend its dividends"）
- 2026-07-30｜Phong Le｜capital_allocation：比特幣貨幣化三用途（原話："Bitcoin monetization, selling Bitcoin for 3 purposes"）
- 2026-07-30｜Phong Le｜capital_allocation：首筆賣幣 32 BTC 的理由（原話："We did it to inoculate the market and test our processes."）
- 2026-07-30｜Andrew Kang｜capital_allocation：季後至 7/27 賣出 2,225 BTC（原話："we did sell 2,225 Bitcoin for approximately $135 million"）
- 2026-07-30｜Phong Le｜capital_allocation：年初至今買賣 BTC 數量（原話："We bought 174,895 Bitcoin year-to-date 2026."）
- 2026-07-30｜Phong Le｜capital_allocation：年初至今賣出 BTC 數量（原話："We sold 3,620 Bitcoin during that same period of time."）
- 2026-07-30｜Phong Le｜capital_allocation：STRC 買回授權至多 $1B（原話："ability to repurchase digital credit up to $1 billion"）
- 2026-07-30｜Phong Le｜capital_allocation：MSTR 買回條件：低於每股淨比特幣（原話："when it's trading at a discount to net Bitcoin per share"）
- 2026-07-30｜Andrew Kang｜capital_allocation：Q2 以折價回購可轉債 $1.5B（原話："the $1.5 billion repurchase of convertible debt"）
- 2026-07-30｜Phong Le｜capital_allocation：下次可轉債回售日（原話："next convertible debt put date is September of next year"）
- 2026-07-30｜Andrew Kang｜capital_allocation：可轉債處理無時程（原話："There is no set time line."）
- 2026-07-30｜Andrew Kang｜capital_allocation：可轉債處理有三種選項，優先順位為 STRC 回面值（原話："liability management options remain open"）
- 2026-07-30｜Phong Le｜capital_allocation：不排除調降 STRC 利率與調整 ATM 發行（原話："We could adjust the rate down from 12% to 11% to 10%"）
- 2026-07-30｜Phong Le｜capital_allocation：可管理 ATM 發行節奏（原話："We could manage the ATM issuance, right?"）
- 2026-07-30｜Michael Saylor｜capital_allocation：資產配置不再 100% BTC（原話："I don't think it will be 100% in the future."）
- 2026-07-30｜Phong Le｜capital_allocation：Phong 談左腦比特幣多頭的教訓（原話："we shouldn't let our left brain Bitcoin bull"）
- 2026-07-30｜Phong Le｜capital_allocation：Phong 表示高幣價時可考慮降息（原話："reducing the rate when we see a strong Bitcoin price"）
- 2026-07-30｜Phong Le｜capital_allocation：Q1 說法延伸：由單向發行轉主動資本管理（原話："We went from one-way capital issuance"）
- 2026-07-30｜Michael Saylor｜commitment：不採用比特幣質押借款（原話："it's not on the table right now"）
- 2026-07-30｜Michael Saylor｜commitment：避免保證金式負債（原話："avoid any kind of appearance of a margin debt"）
- 2026-07-30｜Michael Saylor｜commitment：現有債務為上限並逐步縮減（原話："the existing amount of debt to be the maximum we have"）
- 2026-07-30｜Michael Saylor｜commitment：不賣出波動率（選擇權）（原話："right now, that's not part of the plan"）
- 2026-07-30｜Michael Saylor｜commitment：對衍生品交易商承諾不競爭、不改凸性（原話："we won't compete with you, and we won't change the convexity"）
- 2026-07-30｜Michael Saylor｜guidance：每 $1 資本每年可賣 $0.10–0.20 信用（原話："we can sell $0.10 to $0.20 of credit per year"）
- 2026-07-30｜Phong Le｜guidance：目標七年內讓每股比特幣翻倍（原話："double Bitcoin per share in 7 years through digital credit"）
- 2026-07-30｜Phong Le｜guidance：7 月迄今普通股發行約 $1.3B（原話："we've issued about $1.3 billion of common equity"）
- 2026-07-30｜Andrew Kang｜margin：放大倍數口徑（原話："Amplification represents our total Bitcoin as a multiple"）
- 2026-07-30｜Andrew Kang｜margin：淨槓桿口徑（原話："a low net leverage of 5.4%"）
- 2026-07-30｜Andrew Kang｜margin：年初至今 BTC yield（原話："Year-to-date BTC yield is currently 4.5%"）
- 2026-07-30｜Andrew Kang｜margin：Q2 BTC yield 對 Q1（原話："BTC yield of 5% outperformed the Q1 BTC yield of 3.2%"）
- 2026-07-30｜Andrew Kang｜margin：Q2 EPS（原話："an EPS of negative $24.45 per share"）
- 2026-07-30｜Phong Le｜margin：每年股息與利息支出（原話："interest payments of $1.76 billion currently annually"）
- 2026-07-30｜Michael Saylor｜margin：hurdle rate 定義（原話："hurdle rate represents our blended current cost of credit"）
- 2026-07-30｜Michael Saylor｜margin：floor rate 定義（原話："rate the Bitcoin would have to fall on an annualized basis"）
- 2026-07-30｜Michael Saylor｜competition：STRC 對標私募信用、銀行特別股、垃圾債（原話："STRC as competing against private credit and bank"）
- 2026-07-30｜Michael Saylor｜competition：STRC 在三大特別股指數均為第一大持股（原話："STRC is now the #1 holding at all 3"）
- 2026-07-30｜Michael Saylor｜competition：只有兩家公司能賣數位信用（原話："There's only 2 companies in the world right now"）
- 2026-07-30｜Michael Saylor｜product：聚焦整併信用工具（原話："We're laser-focused on consolidation."）
- 2026-07-30｜Michael Saylor｜product：計畫逐步縮減 11 檔信用工具（原話："Our explicit plan is to whittle them down over time."）
- 2026-07-30｜Michael Saylor｜product：重來會只發行 STRC、不發債（原話："I would do no bonds, I would just sell STRC"）
- 2026-07-30｜Michael Saylor｜product：STRC 名目規模成長（原話："to $10.5 billion at the end of Q2"）
- 2026-07-30｜Michael Saylor｜product：官網新增 200 週均線指標（原話："we've also added the 200-week moving average"）
- 2026-07-30｜Michael Saylor｜product：新推銀行採用指數（原話："Bitcoin Banking Adoption Index"）
- 2026-07-30｜Michael Saylor｜risk：Saylor 列五項比特幣逆風（原話："We really think there are 5."）
- 2026-07-30｜Michael Saylor｜risk：Fed 理事投票主張升息（原話："governors actually voted to raise rates"）
- 2026-07-30｜Michael Saylor｜risk：STRC 跌至 70 的成因：二三階信用額度收回（原話："third order reflexive contraction in credit in the system"）
- 2026-07-30｜Michael Saylor｜risk：Saylor 否認為 DeFi 清算（原話："so it wasn't DeFi, by the way."）
- 2026-07-30｜Phong Le｜risk：2026 最大教訓：持有流動美元（原話："the importance of holding liquid U.S. dollars"）
- 2026-07-30｜Phong Le｜risk：2022 教訓：避免有契約與保證金的債（原話："was don't do either of those"）
- 2026-07-30｜Michael Saylor｜customer：STRC 機構持有比重上升（原話："holdings had grown from $1.1 billion to $3.1 billion"）
- 2026-07-30｜Michael Saylor｜customer：STRC 持有人結構（原話："78% of STRC was held by retail and 22% by institutional"）
- 2026-07-30｜Andrew Kang｜customer：新增兩家分析師覆蓋（原話："We added 2 new covering analysts from Barclays and Siebert"）
- 2026-07-30｜Andrew Kang｜customer：分析師平均 MSTR 目標價（原話："The average MSTR price target is approximately $296"）

### 問答異常語氣（迴避／改口／保留）
- MSTR_Q2_2026_Earnings_Call_20260730.md｜問：Barclays：是否將美元準備金最低門檻由 12 個月提高到 18–24 個月｜答法：Phong 先說會考慮，隨即改口一年是好的位置，轉談實際準備金金額與使用承諾，未給是否調高的結論
- MSTR_Q2_2026_Earnings_Call_20260730.md｜問：Mark Palmer：是否以比特幣質押借款補美元準備金｜答法：Phong 說曾與多家對手方洽談，又說沒有認真研究過；Saylor 接著說目前不在檯面上但保留未來選項
- MSTR_Q2_2026_Earnings_Call_20260730.md｜問：Lance Vitanza：哪些原則是基礎、哪些隨市況調整｜答法：Saylor 只談 STRC 不低於面值，未回答如何區分基礎原則與可變原則
- MSTR_Q2_2026_Earnings_Call_20260730.md｜問：STRC 回面值需要多少資金與時間｜答法：Saylor 表示無法保證需要多少美元或多少天，只給 $1B 授權、9/8 類比時點與「花多少都花」的說法

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
{"date":"20260819","verdict":"迴避","role":"不持有","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"權益mNAV連續8週≥1.15x 且 BTC/股連2季QoQ回正 且 2028 put wall（$67.1億六檔轉債本金，2027-09至2028-06陸續到期）完成再融資且淨稀釋<15% 且 MSCI未將MSTR排除出現有指數 → 由迴避重審至觀望","irr_base_pct":15.9,"ev5y_pct":145.1,"drift_watch_prior":{"dca_verdict":"迴避","dca_role":"不持有","signal":"X","val":"🟠","ma":"❌","trap":"🔴","moat_trend":"↓","runway_post_y5":"🟡","asym_ratio":4.52,"ev5y_pct":145.1,"irr_base_pct":15.9,"max_dd_pct":-93.0,"bull_5y_price":625.0,"bear_5y_price":9.41,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"權益mNAV連續8週≥1.15x 且 BTC/股連2季QoQ回正 且 2028 put wall（$67.1億六檔轉債本金，2027-09至2028-06陸續到期）完成再融資且淨稀釋<15% 且 MSCI未將MSTR排除出現有指數 → 由迴避重審至觀望","price_at_dd":105.31,"archetype":"金融","cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名中除程式欄以外的每一個**（程式稍後才會算的 p_bull_pct／p_bear_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；`asym_ratio`／`ev5y_pct`／`irr_base_pct`／`bull_5y_price`／`bear_5y_price` 的漂移歸因同樣由程式生成條目（程式用本次情境、依先換情境後換股價的順序拆量），你不要為它們開條目；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

**給讀者看的文字欄不准出現內部代號**：`thesis.H[]`／`thesis.R[]` 的各欄（信息來源／漂移觸發條件等）、`triggers[].text`、`counter_evidence.contradictions[]` 各欄、`answers.*.verdict`／`answers.*.reasoning` 這類文字，一律不得出現事實表 id（`f_` 開頭，如 `f_consensus_rev_3m_fy1_pct`）或軸／finding id（`軸名#n`，如 `competitive_share_entrants#0`）——這些是程式內部代號，不是給讀者的話。要引用哪個事實或哪個軸，寫進對應的 `fact_refs[]`／`evidence_refs[]` 陣列，文字欄本身只寫人話。

---

## 尾段：scenario_inputs 形狀與回覆格式

**本檔 FY1 共識 EPS ≤ 0（虧損），程式已把估值口徑定為 `sales_multiple`：情境樹用營收路徑 × 終端 EV/S，不用 EPS × 本益比。** 口徑由程式決定，你填什麼 `valuation_basis` 都會被覆寫。`scenario_inputs` 的鍵名與形狀必須完全照下面這份（不得增刪改名；程式據此產生 `dd_scenario.py` 的輸入檔，寫錯鍵名就是整段判斷失效）：

```json
{
  "valuation_basis": "sales_multiple",
  "terminal_label": "FY20XXE",
  "start": {"rev": <FY+1 共識營收，百萬，報告幣別；抄事實表 f_rev_consensus_fy1_m>, "ev_s": <目前 EV/S（EV÷FY+1 共識營收）；抄事實表 f_ev_s_fwd>, "basis": "<起點口徑一句話：營收取哪一年、EV/S 的分母是哪一年，須與終端 EV/S 分母同口徑>"},
  "rev": {"bull": [<Y1>, <Y2>, <Y3>, <Y4>, <Y5>], "base": [五個數], "bear": [五個數]},
  "ev_s": {"bull": <終端 EV/S>, "base": <倍數>, "bear": <倍數>},
  "net_debt_y5": {"bull": <終端年淨負債，百萬，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "shares_y5": {"bull": <終端年稀釋股數，百萬股，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "p": {"bull": <機率整數>, "base": <整數>, "bear": <整數>},
  "yield_pct": {"dividend": <股息殖利率 %>, "net_buyback": <淨回購殖利率 %>},
  "max_dd": {"lo": <負數 %>, "hi": <負數 %>, "basis": "<範圍怎麼推出來的，見判斷卡③情境樹假設段>", "trigger_time": null},
  "basis": {"bull": "<這支路徑的假設一句>", "base": "…", "bear": "…"},
  "endo_ceiling_exceeded": <true|false，共識 CAGR 是否超過 §5.R 內生天花板>
}
```

（**不要**填 `eps`、`pe`、`second_stage`、`peer_max_fpe`；`eps_meta` 仍照常寫共識三年 EPS。現價、目前淨負債（`f_net_debt_m`）、目前股數（`f_shares_diluted_m`）由程式從事實表帶進 `scenario.json`。）

**終端每股價＝max(0, (終端營收 × 終端 EV/S − 終端淨負債) ÷ 終端股數)**，股權價值為負就是 0（Bear 情境債務吃光股權時，要如實寫出讓它歸零，不要為了好看調高倍數）。`net_debt_y5` 要反映該情境下的現金流與融資（虧損公司的淨負債通常會變大，不是沿用目前值）；`shares_y5` 要反映該情境下的增資與稀釋；兩者填 null 才是沿用目前值，不是預設答案。`ev_s` 是終端年 EV ÷ 終端年營收，須與 `start.ev_s` 同口徑（前瞻 vs trailing 不可混）。

`dd_scenario.py` 會擋：`rev` 各路徑長度 ≠ 5、終端營收非 Bear＜Base＜Bull、三機率加總 ≠ 100、`p.bear` ＜ 20、`endo_ceiling_exceeded=true` 且 `p.bear` ＜ 30、`p.base` ＞ 50。另有機械閘：Bull 前兩年營收不得與 Base 相同（情境退化）、`|max_dd.lo|` 不得小於任一情境終點跌幅。機率與路徑是你的判斷，算術（IRR／倍數貢獻／AR）全由腳本算，不要自己填結果欄。

**回覆全文即 `judgment.json` 內容**：緊湊 JSON（`json.dumps(obj, separators=(",", ":"))` 等效格式），陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）。不寫 `scenario.json`（程式從 `scenario_inputs` 產生）。不填不歸你的欄（`decision_inputs` 的機械欄、`reasoning`／`plain` 頂層、`moat.spread_table`／`competitors`、`contradictions`／`triggers` 等舊形狀頂層欄）——填了機械閘會擋。`decision_inputs.asym_ratio`／`irr_base_pct`／`ev5y_pct` 一律填 `null`，由腳本從 scenario 機械算回。

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSTR_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
