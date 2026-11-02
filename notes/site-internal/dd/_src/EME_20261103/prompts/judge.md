你是 stock-analyst **v20 判斷 agent**，標的 EME（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"EME","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EME_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EME_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":5540,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"EMCOR Q3 2026 press release (8-K Ex.99.1) https://www.sec.gov/Archives/edgar/data/0000105634/000010563426000132/eme-ex991_2026930xq3.htm"},"note":"未取得"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":10.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"% (營業利益 $579.8m)","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"EMCOR Q3 2026 press release (8-K Ex.99.1)；排除 $34.0m 美國建築服務無形資產減損"},"note":"未取得"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":9.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"% (營業利益 $545.8m)","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"EMCOR Q3 2026 press release (8-K Ex.99.1)"},"note":"未取得"},{"id":"f_kpi3_diluted_eps_non_gaap","label":"Diluted EPS (non-GAAP)","value":9.6,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"EMCOR Q3 2026 press release (8-K Ex.99.1)"},"note":"未取得"},{"id":"f_kpi4_free_cash_flow_q3","label":"Free cash flow (Q3 單季，推算)","value":759.6,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"推算：9M 營運現金流 $1,086.6m − 上半年 $289.9m = $796.7m；9M capex $97.0m − 上半年 $59.9m = $37.1m（Q3 與 Q2 8-K Ex.99.1；非公司直接申報）"},"note":"未取得"},{"id":"f_kpi6_full_year_2026_guidance_","label":"Full-year 2026 guidance（10-29 上調）","value":"營收 $20.6–21.0B；non-GAAP 營業利益率約 10%；non-GAAP EPS $34.50–35.50","period":"Q3 FY2026（公告於 2026-10-29）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（公告於 2026-10-29）","citation":"EMCOR Q3 2026 press release (8-K Ex.99.1)"},"note":"共識 FY1 EPS 34.29（2026-10-31 快照，來源：dd_numbers_extra.py consensus_revision）；yfinance FY1 營收共識 $20,703m"},{"id":"f_kpi7_remaining_performance_ob","label":"Remaining performance obligations (RPO)","value":18570,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"EMCOR Q3 2026 press release (8-K Ex.99.1)"},"note":"未取得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_eme_gross_margin_pct","label":"EME 毛利率","value":19.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eme_operating_margin_pct","label":"EME 營業利益率","value":9.88,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eme_fcf_margin_pct","label":"EME FCF 利潤率","value":7.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_gross_margin_pct","label":"FIX 毛利率","value":25.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_operating_margin_pct","label":"FIX 營業利益率","value":16.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_fcf_margin_pct","label":"FIX FCF 利潤率","value":19.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_gross_margin_pct","label":"PWR 毛利率","value":15.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_operating_margin_pct","label":"PWR 營業利益率","value":6.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_fcf_margin_pct","label":"PWR FCF 利潤率","value":8.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mtz_gross_margin_pct","label":"MTZ 毛利率","value":12.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTZ.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mtz_operating_margin_pct","label":"MTZ 營業利益率","value":4.85,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTZ.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mtz_fcf_margin_pct","label":"MTZ FCF 利潤率","value":2.34,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTZ.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_strl_gross_margin_pct","label":"STRL 毛利率","value":23.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STRL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_strl_operating_margin_pct","label":"STRL 營業利益率","value":18.62,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STRL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_strl_fcf_margin_pct","label":"STRL FCF 利潤率","value":10.93,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STRL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc_non_gaap","label":"SBC 占 non-GAAP 營業利益","value":0.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"推算：9M SBC $19.7m − H1 $15.0m = Q3 約 $4.7m，÷ non-GAAP 營業利益 $579.8m（Q3 與 Q2 8-K Ex.99.1）"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":692.67,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-23.82,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":42.78,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":2.42,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（33.48 → 34.29）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":3.03,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（37.95 → 39.1）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":1.08,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（44.54 → 45.02）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":34.29,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":39.1,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":45.02,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":16.83,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 29.35 → 34.29（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":20.03,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝61.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":61.8,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.53,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝84.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":84.3,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.52,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝85.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":85.7,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":20.2,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 34.29，分子＝快照價 692.67","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.231,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-208.24,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 566.51、現金 774.75（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":43.78,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":30118.24,"period":"2026-11-03","unit":"USD m","basis":"市值 30326.48 ＋ 淨負債 -208.24","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":20702.87,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":23328.76,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（11 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.45,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 686.88 / W52 748.63 / W104 631.66 / W250 388.18 / W250 13週斜率 2.37%"},{"id":"f_ma_w52","label":"52 週均線","value":748.63,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":631.66,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":388.18,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.37,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 自述：產業高度分散，進入障礙低，任何具足夠財力與技術的組織都可能成為競爭者；部分對手管理費用較低、報價較低，競標壓力可能壓低價格與利潤率。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"In addition, relatively few barriers exist to prevent entry into most of the industries in which we operate. As a result, any organization that has adequate financial resources, and access to technical expertise, may become a competitor.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列出電氣／機械承包主要對手：APi、Comfort Systems、Dycom、Everus、IES、MasTec、MYR、Quanta、Tutor Perini；多數營收來自競標案，邀標常以過往經驗、技術能力與財務實力為條件。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"A majority of our revenues are derived from projects requiring competitive bids; however, an invitation to bid is often conditioned upon prior experience, technical capability, and financial strength.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 指出收購競爭：其他潛在收購方可能資源更多或條件更優，可能限制 EME 的併購機會。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"We may also face increased competition from other potential acquirers, including those who may have greater financial resources available to them or who may be in a position to offer more favorable terms to the target company.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Zacks/Nasdaq：EMCOR 預期 2026 年成長再度優於美國非住宅營建，並提到創紀錄積壓訂單與持續贏得份額。","source":"Nasdaq/Zacks: Can EMCOR Outgrow Nonresidential Construction Again in 2026?","url":"https://www.nasdaq.com/articles/can-emcor-outgrow-nonresidential-construction-again-2026","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"CSIMarket：同業 Comfort Systems 2026 Q2 營收成長 50.26%，市占上升。","source":"CSIMarket FIX Competitors","url":"https://csimarket.com/stocks/FIX-Competitors","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"EMCOR 10-K 風險因素揭露：可能面臨現有或潛在客戶自有 in-house 服務組織的競爭（尤其 building services），不確定客戶未來會否繼續外包。屬一般性風險，未指名最大客戶導入第二供應商。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"We may also face competition from the in-house service organizations of existing or prospective customers, particularly with respect to building services. Many of our customers employ personnel who perform some of the same types of building services that we do.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"10-K FY2025 風險因素：客戶可隨時單方面減少、不續約或終止合約，失去重要客戶可能有重大不利影響；未揭露單一客戶占營收百分比。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"Although we provide services to a diverse portfolio of end markets and have long-standing relationships with many of our significant customers, our customers may unilaterally reduce, fail to renew, or terminate their contracts with us at any time.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"FY2025 營收來源分散：97% 美國、72% 營建、21% 建築服務、7% 工業服務；<$10M 專案占電機機械營建營收約 42%。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"We derive revenues from many different customers in numerous industries, which have operations in several different geographical areas.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2024 年曾因特定客戶破產提列 $11.0M 準備，影響美國建築服務部門利潤率 30bp。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"The results of this segment for the year ended December 31, 2024 included an $11.0 million reserve for a specific customer bankruptcy within its commercial site-based services division, which negatively impacted the segment’s operating margin by 30 basis points in such prior year period.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"EMCOR Q3 2026 RPO 創高 $18.57B（年增 47.2%），資料中心 RPO $8.74B、年增逾一倍、季增 13%，約占總額近半；FY2026 營收指引上調至 $20.6–21.0B。管理層稱客戶以大型 hyperscaler 為主，非 neocloud；通話中分析師提及 Loudoun 暫停與紐約暫停令。","source":"EMCOR Form 8-K Q3 2026 earnings release / MarketBeat call highlights","url":"https://www.sec.gov/Archives/edgar/data/0000105634/000010563426000132/eme-ex991_2026930xq3.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"電工缺口：Industrial Info Resources 預期失衡於 2027 年達高峰（缺約 107,000 名電工）；AIA 共識預測資料中心支出 2026 年 +26.3%、2027 年 +16.5%；NEMA 預期資料中心與電網建設成長持續至 2027；JLL 稱 57% 北美資料中心專案延誤三個月以上；德州州長暫停新資料中心核准屬需求風險。","source":"WebSearch 彙整：IIR、AIA、NEMA（ewweb.com）、JLL、Construction Dive","url":"https://www.ewweb.com/news/project-watch/article/55338440/nema-outlook-forecasts-more-solid-growth-in-data-center-grid-construction-through-2027","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 一般法規風險揭露，未點名特定反壟斷調查","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"•the impact of legal proceedings, claims, lawsuits, or governmental investigations; •unfavorable developments in the mix of our business; and •other factors discussed elsewhere in this report.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K FY2025 風險因子：EMCOR 暴露於銅、鋼等原物料價格與保護主義貿易措施；依賴第三方供應商供料；部分合約無法調價，關稅變動可能損及獲利與流動性","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"Changes in U.S. foreign trade policies could lead to the imposition of additional trade barriers and tariffs. We cannot predict the full extent of new, extended, or changed trade policies, including tariffs, that may be made by the current or a future presidential administration or Congress","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K 提及對中美貿易爭端相關制裁的合規風險；搜尋未見 EMCOR 被列入出口管制或實體清單的來源","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"sanctions against foreign persons and entities have increased in recent years, especially in connection with the war in Ukraine and ongoing trade and diplomatic disputes between the U.S. and China.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K：EMCOR 倚賴第三方供應商取得材料與設備，曾遇供應鏈延遲、部分材料設備交期長、材料與燃料價格上升；關稅可能使客戶減少使用其服務","source":"EMCOR FY2025 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"in the future be impacted by the rescission of electric vehicle tax credits, tariffs imposed on the import of vehicles to the United States, and other disruptions to the global supply of vehicles generally; (e) regulations and requirements that restrict or prohibit our ability to impose requirements on third-party contractors;","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"2025-12-01 EMCOR 出售英國建築服務部門（EMCOR (UK) Limited 與 EMCOR Group (UK) plc），海外地緣曝險下降；風險因素僅泛列國內外政治事件與關稅","source":"EMCOR Form 10-Q (2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0000105634/000010563426000130/eme-20260930.htm","excerpt":"On December 1, 2025, we sold EMCOR (UK) Limited and EMCOR Group (UK) plc, which collectively represented our United Kingdom building services segment (collectively, “EMCOR UK”).","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收創單季新高 $5.54B，年增 28.8%，有機成長 25.5%","source":"EMCOR 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000105634/000010563426000132/eme-ex991_2026930xq3.htm","excerpt":"revenues totaled a quarterly record of $5.54 billion, an increase of 28.8%, compared to revenues of $4.30 billion for the third quarter of 2025. On an organic basis... third quarter revenues increased by 25.5%.","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Electrical Construction 營收年增 44.3% 至 $1.85B，Mechanical Construction 年增 43.1% 至 $2.55B；工業服務與去年同期大致持平（法說會）","source":"MarketBeat Q3 2026 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/transcript-emcor-group-q3-earnings-call-highlights-2026-10-29/","excerpt":"Electrical Construction revenue increased 44.3% to $1.85 billion, while Mechanical Construction revenue climbed 43.1% to $2.55 billion.","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"資料中心 RPO $8.74B，較去年同期逾倍增、季增 13%；總 RPO 創高 $18.57B；美國建築服務段認列 $34.0M 減損","source":"EMCOR Q3 2026 earnings release / call summary","url":"https://www.sec.gov/Archives/edgar/data/0000105634/000010563426000132/eme-ex991_2026930xq3.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 RPO $17.14B 年增 44%，管理層稱網通（含資料中心）需求極強，全年營收指引上調至 $20–20.5B","source":"MarketBeat Q2 2026 call highlights","url":"https://www.marketbeat.com/instant-alerts/emcor-group-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 10-Q 各報告段營收成長","source":"EMCOR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0000105634/000010563426000130/eme-20260930.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"EME 10-K FY2025 風險因素未列出取代其核心服務的替代技術；技術面只提及自身使用 AI 工具可能有故障、安全漏洞、演算法瑕疵，以及 AI 生成內容智財歸屬法規未定的侵權風險。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"We may also utilize new information technology tools, including AI tools, in certain business functions, and such tools could be subject to malfunction, security vulnerabilities, or algorithmic flaws (including AI generation of false or biased information).","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Simply Wall St 社群敘事（投資人意見，非公司揭露）主張預製／模組化營建在業界擴大，可能降低現場安裝與維護的長期需求；同敘事亦指 EME 持續擴大預製、VDC、BIM 能力。","source":"Simply Wall St community narrative: rising automation and tightening regulations will erode margins (EME)","url":"https://simplywall.st/community/narratives/us/capital-goods/nyse-eme/emcor-group/ts7dtyqk-rising-automation-and-tightening-regulations-will-erode-margins-lfqc","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"產業趨勢文章稱模組化營建是短中期最具顛覆潛力的趨勢（可將最多 80% 現場工作移入工廠）；Autodesk 頁面指電力基礎建設規模將推動營建團隊走向預製與更佳協調。屬顧問／廠商部落格，數字未追溯至一手資料。","source":"Bancolombia 營建創新趨勢；Autodesk 2026 Construction Trends","url":"https://www.autodesk.com/blogs/construction/?p=20904","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"模組化營建被視為最具顛覆潛力的趨勢，可將最多 80% 現場工作移入工廠","source":"Bancolombia 營建創新趨勢","url":"https://www.bancolombia.com/empresas/capital-inteligente/tendencias/innovacion/nuevas-tendencias-sector-constructor-innovacion","excerpt":"técnica de ABC Arquitectura Modular lo sintetiza así: son producidos en \"módulos\" que, al unirse en su emplazamiento, replican fielmente el diseño y las especificaciones iniciales de la infraestructura. El mercado de construcción modular en Colombia alcanzó un valor estimado de USD517,75 millones en 2025 y se proyecta que crecerá a una tasa compuesta anual del 6,80 % hasta 2035, cuando podría","as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-30 Q2 後公司第二次上調 FY2026 guidance：稀釋 EPS 32.00–33.25（前 28.25–29.75）、營收 20.0–20.5B（前 18.5–19.25B）、營業利益率 9.5–9.8%（前 9.0–9.4%）；原始 guidance（2026-02-26）營收 17.75–18.50B、利益率 9.0–9.4%。未見下修。","source":"EMCOR Q2 2026 8-K ex99.1 / 搜尋摘要整理（Nasdaq、Benzinga、SEC）","url":"https://www.sec.gov/Archives/edgar/data/0000105634/000010563426000112/eme-ex991_2026630xq2.htm","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 財報前 FY2026 EPS 共識約 29.31、營收約 19.0B；新 guidance 高於財報前共識。Q2 實際 EPS 9.06 vs 共識 7.23，營收 5.15B vs 約 4.71B。","source":"MarketBeat：EMCOR Group posts quarterly earnings results","url":"https://www.marketbeat.com/instant-alerts/emcor-group-nyseeme-posts-quarterly-earnings-results-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Chartmill 顯示 FY2026 EPS 最新共識 33.19（12 位分析師，2026-10-17），位於新 guidance 區間 32.00–33.25 的上緣；Q3 EPS 預期 8.44、營收 5.24B。尚未查到 Q3 實際結果。","source":"Chartmill EME estimates","url":"https://www.chartmill.com/stock/quote/EME/estimates","excerpt":"Latest recorded estimate: 33.19 USD · Oct 17, 2026 · 12 analysts","as_of":"2026-10-17","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"目標價分布（2026-07/08 快照）：Investing.com 平均 1,044.14、中位 1,065、區間 885–1,200（7 Buy／3 Hold）；Tickflow 平均 987.67（6 位，2026-08-02）；valueinvesting.io 平均 969.79（14 位）；Wallstreetzen 平均 958（5 位，808–1,123）；Benzinga 平均 930（8 位）；各站樣本與日期不一。UBS 1,065（07-31）、Oppenheimer 1,200 上調。","source":"Investing.com／Walnut／Tickflow／valueinvesting.io／Wallstreetzen／Benzinga（搜尋摘要）","url":"https://walnutinvest.com/stocks/eme/forecast","excerpt":"Average target $1044.14, median $1065.00, target range $885.00 to $1200.00, 7 buy and 3 hold","as_of":"2026-08-02","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026 上半年 EMCOR 收購四家公司，upfront 對價 $99.8 百萬（Q2 2026 10-Q 所述，經搜尋摘要轉述，未逐字核對原文）。","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0000105634/000010563426000110/eme-20260630.htm","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"PEMEX Deer Park 煉油廠 2024-10-10 化學外洩，子公司 Repcon 與 EIS 被列為多起訴訟被告，公司預期保險涵蓋大部分或全部賠付。","source":"SEC EDGAR 10-K FY2025 Item 8 附註","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"Repcon, Inc. (“Repcon”) and EMCOR Industrial Services, Inc. (“EIS”), indirect subsidiaries of the Company, have been named in several of the lawsuits, and Repcon has also been subject to contractual indemnification claims.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 8-K 共 6 份，含重大項目者 0 份。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000105634&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026 上半年 EMCOR 收購四家公司，upfront 對價 $99.8 百萬；屬小型併購（搜尋摘要轉述）。","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0000105634/000010563426000110/eme-20260630.htm","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"近 12 個月 8-K 無 1.01／2.01 等重大併購項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000105634&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"PEMEX Deer Park 外洩案：Repcon 與 EIS 被列為多起合併訴訟（MDL）被告，公司預期保險涵蓋。","source":"SEC EDGAR 10-K FY2025 Item 8 附註","url":"https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm","excerpt":"Based on currently available information, we believe insurance will cover much or all of any amounts required to be paid by Repcon or EIS in connection with these claims.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 含 4.02（不可信賴先前財報）等重大項目者 0 份，搜尋亦無 SEC 調查或重編。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000105634&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"EME","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.59,"operating_margin_pct":9.88,"fcf_margin_pct":7.47,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"FIX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.57,"operating_margin_pct":16.66,"fcf_margin_pct":19.46,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PWR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.76,"operating_margin_pct":6.81,"fcf_margin_pct":8.46,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MTZ","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":12.74,"operating_margin_pct":4.85,"fcf_margin_pct":2.34,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTZ","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"STRL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.78,"operating_margin_pct":18.62,"fcf_margin_pct":10.93,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STRL","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"EME"},"financial_history":{"ticker":"EME","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":11076120000.0,"revenue_yoy_pct":null,"gross_margin_pct":14.48,"operating_margin_pct":5.1,"net_income":406122000.0,"diluted_eps":8.1,"free_cash_flow":448644000.0,"fcf_margin_pct":4.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":12582873000.0,"revenue_yoy_pct":13.6,"gross_margin_pct":16.6,"operating_margin_pct":6.98,"net_income":632994000.0,"diluted_eps":13.31,"free_cash_flow":821251000.0,"fcf_margin_pct":6.53,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":14566116000.0,"revenue_yoy_pct":15.76,"gross_margin_pct":18.98,"operating_margin_pct":9.23,"net_income":1007145000.0,"diluted_eps":21.52,"free_cash_flow":1332944000.0,"fcf_margin_pct":9.15,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":16986422000.0,"revenue_yoy_pct":16.62,"gross_margin_pct":19.33,"operating_margin_pct":9.23,"net_income":1272817000.0,"diluted_eps":28.19,"free_cash_flow":1189313000.0,"fcf_margin_pct":7.0,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/EME/EME_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**EMCOR Group, Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good morning. My name is Dave, and I will be your conference operator today. At this time, I would like to welcome everyone to the EMCOR Group Third Quarter 2026 Earnings Conference Call. [Operator Instructions]
I will now turn the call over to Lucas Sullivan, Director, Financial Planning & Analysis. Mr. Sullivan, you may begin.

**Lucas Sullivan** (Executives):
Thanks, Dave. Good morning, everyone, and welcome to EMCOR's Third Quarter 2026 Earnings Conference Call. For those of you joining us by webcast, we are at the beginning of our slide presentation that will accompany our remarks today. This presentation will be archived in the Investor Relations section of our website at emcorgroup.com.
With me today are Tony Guzzi, our Chairman, President and Chief Executive Officer; Jason Nalbandian, Senior Vice President and EMCOR's Chief Financial Officer; and Maxine Mauricio, Executive Vice President, Chief Administrative Officer and General Counsel.
For today's call, Tony will provide comments on our third quarter 2026 and discuss our RPOs. Jason will then review the third quarter numbers and then turn it back to Tony to discuss our guidance before we open it up for Q&A. Before we begin, a quick reminder that this presentation and discussion contains certain forward-looking statements and may contain certain non-GAAP financial information.
Slide 2 of our presentation describes in detail these forward-looking statements and the non-GAAP financial information disclosures. I encourage everyone to review both disclosures in conjunction with our discussion and accompanying slides.
And finally, as a reminder, all financial information discussed during this morning's call is included in our consolidated financial statements within both our earnings press release issued this morning and in our Form 10-Q filed with the Securities and Exchange Commission.
And with that, let me turn the call over to Tony.

**Anthony Guzzi** (Executives):
Yes. Thanks, Lucas, and good morning, and thank you for joining us. I'm going to begin here on Slide 4. EMCOR delivered another quarter of exceptional growth, margin performance, operating cash flow and capital allocation. Revenue increased 28.8% or 25.5% organically. This growth, coupled with strong field execution and improved SG&A leverage, resulted in meaningful expansion of our operating margin. Operating cash flow in the quarter was $797 million, and remaining performance obligations reached a record $18.57 billion, up 47% year-over-year, 40% from year-end 2025 and 8.3% sequentially despite the strong revenue growth we had in the quarter.
Most of the RPO growth was organic, reinforcing the depth of demand across multiple end markets. On an adjusted basis, our third quarter operating margin was 10.5%, reflecting the strength of our execution and operating model. And we earned $9.60 in adjusted diluted earnings per share, a 46% increase versus the year ago period.
Our Construction segments continue to deliver outstanding performance. Both our Electrical and Mechanical segments grew revenues by more than 40%, with approximately 75% of such growth being generated organically.
Our Electrical Construction segment delivered a 13.3% operating margin. And Mechanical Construction delivered a 12.1% operating margin, resulting in combined margin expansion of 40 basis points.
Demand remains broad-based with particular strength in the Network & Communications, which is data centers for the most part, Healthcare, Manufacturing & Industrial, Water & Wastewater and Institutional sectors. We continue to outgrow the broader nonresidential construction markets.
Building Services also posted a strong quarter. Revenue grew nearly 5%, operating income increased 11.5% and operating margin expanded 50 basis points, driven by a favorable revenue mix and improved SG&A leverage.
Industrial Services performed as expected and relatively in line with the third quarter of 2025. Importantly, we saw expanding opportunities in LNG maintenance and petrochemical work, which supports our continued broadening of the markets that we will serve with this segment. As I previously mentioned, and this will be on Slide 5 now. As I previously mentioned, our RPO position strengthened considerably during the quarter, reaching a record $18.57 billion. This growth reflects strong demand across the majority of our market sectors, led by Network & Communications or data centers as well as continued strength in Healthcare, Water & Wastewater, Institutional, Manufacturing & Industrial and I'm going to take a deeper look at each of these sectors.
Data center RPOs totaled a record $8.74 billion, more than double the year ago level and an increase of 13% sequentially. This growth demonstrates our broad capabilities in this sector, which includes electrical, mechanical and fire life safety construction and service. Healthcare RPOs totaled $1.71 billion, an increase of 31% year-over-year, reflecting the strength of this long-standing core market for EMCOR. Water & Wastewater RPOs totaled $1.42 billion, an increase of 38% year-over-year, as we continue to capitalize on opportunities throughout Florida. Institutional RPOs totaled $1.72 billion, an increase of 25% year-over-year, driven by strong demand for many of our education customers, especially at the higher level education. And finally, Manufacturing & Industrial RPOs totaled $1.18 billion, an increase of 10% year-over-year and nearly 27% sequentially as we are benefiting from a broad range of investments across this sector. The size, quality and diversity of our RPOs remains very strong.
Before I turn the call over to Jason, I want to underscore what these results demonstrate. Our field leaders continue to exhibit discipline and precision as they execute some of the industry's largest and most technically complex projects for our highly sophisticated and very demanding customers. That execution is translating into strong margins, cash generation, record RPOs and growth well above the underlying market.
With that, I'll turn it over to Jason.

**Jason Nalbandian** (Executives):
Thank you, Tony, and good morning, everyone. Starting on Slide 6, I will cover the results for each of our segments as well as some of the key financial data for the third quarter of 2026 as compared to the third quarter of 2025. Revenues of $5.54 billion established a new quarterly record for EMCOR, increasing 28.8% or 25.5% on an organic basis.
Revenues of Electrical Construction were $1.85 billion, increasing 44.3%. While the largest increase was driven by greater demand for data center construction projects within the Network & Communications market sector, where revenues increased by 68%, this segment also saw notable growth within Institutional, which was up 78%; Healthcare, which was up 31%; and Manufacturing & Industrial, which increased by 28%. Additionally, contributing to the growth of our Electrical segment was $140.1 million of incremental revenues resulting from the acquisitions we previously announced, including Connelly and Schmidt, which closed in early August.
Mechanical Construction revenues were $2.55 billion, an increase of 43.1%. Greater demand for data center construction projects, including expanded scope associated with increased cooling requirements, led to significant growth within the Network & Communications market sector, where revenues increased by nearly 130%. Beyond data centers, Mechanical Construction benefited from greater opportunities within several other sectors, including Institutional, which was up 56%; Commercial, which increased by 23%, really driven by warehousing, distribution and logistics projects; Manufacturing & Industrial, which includes food processing and was up 17%; Healthcare, which grew by 29%; and Water & Wastewater, which increased by 32%. Driven by the Danforth acquisition in Q4 of last year, this segment generated $173.2 million of incremental revenues within the quarter.
On a combined basis, our Construction segments had revenues of $4.4 billion, establishing new quarterly revenue records for both segments.
We often discuss the diversity of demand that we have across our business. And with double-digit revenue increases across a number of sectors, I think the performance of our Construction segments this quarter really highlights that fact.
If we move to Building Services, revenues of $852.4 million increased by 4.7% and like our Construction segments, represents a quarterly record. We continue to see strength within Mechanical Services, which experienced growth across each of its service lines, including service, repair and maintenance, building automation and controls and retrofit projects.
In addition, given greater project volume, the award of new facilities maintenance contracts and scope or site expansion with existing customers, this segment's site-based business grew revenues by 6.5%, continuing the trend we saw last quarter.
Industrial Services revenues were $287.5 million, generally in line with the prior year. However, on a year-to-date basis, revenues of this segment are up 10.4% as a result of greater refinery turnaround activity, higher petrochemical project volume, new opportunities for LNG plant maintenance and progress made on a large solar project.
Let's turn to Slide 7 for operating income. On a GAAP basis, we generated operating income of $545.8 million or 9.8% of revenues. Our third quarter results included a $34 million noncash intangible asset impairment charge associated with the prior acquisition within our Building Services segment. This business, which accounts for less than 1% of the segment's revenues, provides energy efficiency contracting outside of traditional mechanical services and our site-based offerings and has been affected by disruption in the performance contracting market. When excluding this impairment, our operating income was $579.8 million, and our operating margin was 10.5%. This represents a 43% increase in operating income and reflects 110 basis points of operating margin expansion.
Looking at each of our segments. Operating income of Electrical Construction increased by just over 70% to $247 million, due to the revenue growth I previously mentioned, coupled with 200 basis points of operating margin expansion. While the segment did benefit from a 50 basis point reduction in SG&A margin, the overwhelming majority of the increase in operating margin was a result of greater gross profit margin, given an improved execution and a more favorable project mix.
Mechanical Construction had operating income of $308.2 million, which represents a 34.4% increase. Similar to the first half of the year and as we anticipated, the 80 basis point reduction in operating margin of this segment resulted from a change in mix that included a greater percentage of revenues from projects where we are acting as either the construction manager or prime contractor, and which inherently carry a lower-than-average gross profit margin due to reduced markups on materials, equipment and subcontractor costs as well as an increase in the number of GMP and cost-plus contracts. Despite the year-over-year decrease, operating margin of 12.1% continues to reflect strong execution by our operating companies across a vast number of projects, and we remain pleased with this performance.
Together, our Construction segments grew operating income by nearly 50%, establishing new quarterly operating income records for each segment and earning a combined operating margin of 12.6%, an increase of 40 basis points.
Operating income of Building Services was $66.2 million, an increase of 11.5% and operating margin was a quarterly record of 7.8%, a 50 basis point improvement over Q3 2025. A more favorable mix, coupled with better project execution, resulted in a 30 basis point improvement in gross margin and due in part to the restructuring we completed within our site-based business last year, SG&A margin decreased by 20 basis points.
Operating income for Industrial Services was $5.1 million compared to $6.3 million a year ago. A 120 basis point improvement in gross profit margin was more than offset by an increase in SG&A of the segment.
If we move to Slide 8, I'll cover a few additional items regarding the quarter. As you can see on this page, the increase in our operating margin reflects both outstanding execution by our field teams as well as meaningful operating leverage resulting from the growth we've experienced. Specifically, gross profit of $1.11 billion increased 32.7% while gross profit margin expanded by 60 basis points to 20%. And SG&A was $528.4 million or 9.5% of revenues compared to $429.6 million or 10% of revenues in last year's quarter.
Moving down our P&L. Diluted earnings per share was $9.04, but when you adjust for the intangible asset impairment charge, diluted earnings per share was $9.60, which represents an increase of 46.1% compared to the $6.57 earned in last year's third quarter.
If we briefly turn to Slide 9, you can see our performance year-to-date. Revenues have grown by 22.9% or 20.8% organically. Our gross profit margin has increased by 30 basis points, and we successfully leveraged our cost structure, reducing SG&A margin by 40 basis points.
In a few slides, Tony will provide our updated guidance for 2026. Underlying that guidance is strong fourth quarter performance and the expectation that our full year adjusted operating margin will at least be equivalent to the unprecedented 10% that we have earned through the first 9 months of the year.
I'm going to close on Slide 10, which is our balance sheet. With $775 million of cash on hand and $1.03 billion of working capital, we continue to have significant financial flexibility. This allows us to invest in organic growth, execute on strategic M&A opportunities and return capital to our shareholders. Although not shown on the slide, we generated $796.7 million of operating cash flow in the quarter. And on a year-to-date basis, operating cash flow is now $1.1 billion.
We remain committed to our philosophy of balanced and disciplined capital allocation, which is demonstrated by our year-to-date activity as well as this morning's announcement that our Board of Directors has authorized an additional $500 million for the repurchase of our common stock. Through September 30, we have invested nearly $800 million in acquisitions and returned $510 million to our shareholders through both share repurchases and dividends. These actions reflect our confidence in the long-term prospects of our business.
And with that, I'll turn the call back over to Tony.

**Anthony Guzzi** (Executives):
Thanks, Jason. I'm going to finish on Slide 11 and 12 and go to the capital allocation point before I jump in. You can see all that on Slide 12. Given our year-to-date performance and the visibility of our record RPOs, we are again raising our full year 2026 guidance. We now expect to earn revenue of between $20.6 billion and $21 billion and adjusted diluted earnings per share of between $34.50 and $35.50. This increase reflects sustained demand across multiple sectors, our continued success in winning and executing large-scale projects and our confidence in our operating teams.
Although our acquisitions enhance long-term earnings, near-term earnings per share and operating income contribution is moderated by acquisition-related backlog amortization. Our integrations remain on track, and we are pleased with the strategic fit, build capabilities and the teams we have added.
Our outlook assumes continued strong execution and demand across our core end markets. We will remain disciplined on pricing, contract terms, project selection and resource allocation. Our performance rests on 4 durable operating fundamentals that support growth, margins and cash generation, and they really do serve as our long-term foundation for our compounding success.
First, we invest in training and innovation, workforce development, prefabrication, virtual design and construction, or we refer to as VDC, and enhanced project delivery methods to increase productivity, expand capacity, which ultimately strengthens our execution. We are supporting these capabilities with investments in our recruitment, development, software enhancements, leadership training and new and expanded facilities.
Second, we exercise disciplined contract and risk management. Our teams always balance customer service with rigorous project selection and execution, particularly on large and complex opportunities.
Third, we believe our field leadership is a structural competitive advantage. The expertise of our foremen, general foremen, superintendents, project managers and operating leaders drive safe, reliable execution and that supports repeat business with our customers.
And finally, our balanced capital allocation strategy has supported long-term value creation. We are investing in organic growth, pursuing strategic acquisitions and returning cash to shareholders while preserving the financial flexibility to act on attractive opportunities. During the quarter, we did close on our acquisition of Schmidt Electric headquartered in Austin, Texas, and Connelly Electric serving the Chicagoland area. We are very excited that they are part of our team.
We do recognize the macro environment remains uncertain, including geopolitical conflict, supply chain disruptions and policy and regulatory changes. Our approach is consistent: serve our customers well, protect our contractual rights, manage overall risk and execute through changing and challenging conditions. And we have done that very well over a very long period of time.
And I'm going to close, like I always do, by thanking my EMCOR teammates. Their commitment to our culture of mission first, people always, is the foundation of that success.
With that, I will take questions and turn the call over to Dave to queue you up.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Adam Thalhimer with Thompson, Davis.

**Adam Thalhimer** (Analysts):
Great quarter. I wanted to start on the RPOs for Network & Communications. You said $8.74 billion. Based upon what you're seeing, the trends you're seeing, what are the expectations for growth there?

**Anthony Guzzi** (Executives):
I mean we're going to keep growing. And I always remind you, and I know, Adam, you know this, and this is no particular comment, growth can come in lumpy, but we see great opportunities across the country in all the markets we serve in the data center market. We're seeing it electrically, mechanically and through fire life safety. We've seen no abatement of that demand despite all the noise out in the market right now, preelection. And we continue to work for the right people. The people that have long-term prospects, the big hyperscalers and those that are serving the bigger hyperscalers is who we work for. We're not very much into the neocloud market and sort of the speculative of building data centers. So good market, will continue to be good. We are working off a larger number. So I think eventually, you run in the large -- law of large numbers. But I said that last year, too, and we doubled our growth.

**Jason Nalbandian** (Executives):
Yes. And I think the acquisitions we made give us additional opportunities in additional geographies where maybe they weren't as exposed at the time of acquisition, and that gives us some play into the future.

**Adam Thalhimer** (Analysts):
Okay. And just as we think about the margin performance in the quarter and how we should think about that going forward as a comp, were there any headwinds from gasoline prices or diesel prices or other inflation in Q3?

**Anthony Guzzi** (Executives):
At one time, that would -- with the size we were 5, 8 years ago, it would have mattered a lot more. I think the headwind from that is de minimis because we also are very good at going out and adjusting our bill rates, mainly in Mechanical Service, which is where the majority of the gasoline is used. So was it a headwind? I would say marginally, Jason.

**Jason Nalbandian** (Executives):
Yes. I think on an annual basis, round numbers, we use 20 million gallons of gasoline and diesel. So the way I think about it is every dollar increase is a $20 million impact to us, if we don't pass those costs along. But to Tony's point, we're doing a good job passing it along. So I would say at least 50% of the increase is getting passed on to customers.

**Anthony Guzzi** (Executives):
Yes. I mean the ones that don't are then being captured really in project pricing through the project managers and then form it back into the jobs or in some general condition on a job. So we're pretty good, like Jason said, 50% to 75% getting on. You never get it all back. But the flip side, you don't reduce your prices immediately. So it catches on the other side when prices come down for a little bit.

**Adam Thalhimer** (Analysts):
And then, Jason, just any quick thoughts on cash from ops in Q4? You've still got a lot of -- you still have a lot of accounts receivable that could flip in Q4.

**Jason Nalbandian** (Executives):
I think for us, nothing has changed in terms of the way we view long-term cash generation, right? So somewhere between net income and up to 80% to 85% of operating income on a full year basis. So for this year, that puts you somewhere around $1.5 billion to $1.7 billion of operating cash flow for the full year.

**Operator** (Operator):
And the next question comes from Brent Thielman with Oppenheimer.

**Brent Thielman** (Analysts):
Congrats. Tony, this massive growth in data center RPO, is it fair to say it's all happening still within your kind of your core markets? Is any of this kind of a product of you moving maybe what we call a little further from the home markets into untraditional areas?

**Anthony Guzzi** (Executives):
I think 75% of it is still in our core markets. But we are expanding. We are expanding in Texas. Even pre-Schmidt acquisition, mechanically, we've expanded in Texas. We are serving mechanically some of the more rural markets in Texas. That's part of this. But in general, it's our core markets growing and building out and/or within 30 to 40 miles of our core markets.

**Brent Thielman** (Analysts):
Okay. And then look, as this gets towards -- the data centers get toward looks like 50% of your combined Construction segment revenue here pretty quickly. I guess I want to get your view whether there's a balance in terms of mix of markets and customers you want to maintain? Or is it simply move the teams to go after the best returning opportunities for the business right now?

**Anthony Guzzi** (Executives):
I think it's both, Brent, the reality, right? We have built in a diversity of demand because not all our end markets, not all our geographic markets have data center capability. We still have a fairly significant business in California. And really the data center business in California is de minimis. We have a fairly significant business across all New York State and New England. The data center business across New York State, none there right now because of the moratorium. But the data center business in New England, New York State and even New Jersey is de minimis.
So we have built-in diversity. But even within markets where we have strong data center demand, we are very cognizant that we still need to serve, especially our core Healthcare customers and some of our Institutional customers and our Manufacturing customers. So we are very cognizant of having the ability to spread across all. And quite fortunately, we've been able to do very creative things with our workforce to make that happen to include things like they will work on those sites 4 or 5 days a week. And if they want to pick up overtime, they can come over on a scope of work and work on the data center site on the weekend to pick up extra hours.
But it's -- there is no magic number to any of this. I think it starts with -- we have long-term customers. We have built-in diversity. We have long-term customers in markets that have data center demand. We're going to continue to serve. But then on balance, we're going to make the right mix management opportunity because we are contractors over the next 1- to 3-year period about how we'll serve the market and how we'll maximize return for our shareholders.

**Jason Nalbandian** (Executives):
And if you're asking about the data center space, in particular, if we have a concentration risk there, I would say we're not tied to 1 or 2 customers. It's fairly diverse. And if you look year-to-date, data centers are about 1/3 of our revenues, and that 1/3 of our revenues is split up amongst numerous customers.

**Anthony Guzzi** (Executives):
Yes. But even there, Brent, in the data center market, Jason makes a good point. One, we have diversity, not only of trade, but end geographies and end customers. But the other thing that we have also is we have more people that want to work with us. I don't say people are just like we can do what we want. We have more data center constructors that want to work with us than we can serve.
So we do have the ability to be selective about who we'll work for, what kind of work we'll do. It's always important when you think about data centers. Still the majority of our mix still tilts towards cloud storage data centers and cloud computing data centers. And I think it's going to be that way for at least the next year, 1.5 years.

**Brent Thielman** (Analysts):
Okay. Excellent. Maybe just last one. Tony, a lot of your peers talk about sort of developing physical capacity in MEP, whether you call it prefab or whether you call it modular. You've been doing a lot of that for a long time. Maybe you could just talk about what your plans are within your business on that side? Are you doing expansions? Are you building that out? Maybe just to clarify what it is you do there as well?

**Anthony Guzzi** (Executives):
Yes, 100% we're expanding. The way we think about it is what demand do we have to support that? Typically, we're building for ourselves. We are -- we do have the opportunity with a couple of the hyperscalers to build modules. And the difference between us and one of our peers is we're not building buildings and then putting them on tractor trailers and moving them out. We're building piping modules, piping racks, HVAC units, things like that. We typically have done it for ourselves. We have done it for them to have other people install. I think that's going to become more of what we do. It won't ever be a significant amount of our revenue, but we will service that market.
I think pragmatically, once we are doing that on a job, they will then ask us to expand and do the installation. So that will actually grow geographic areas, too. But no, we're expanding. We're expanding some of our traditional shops and traditional locations. But we'll add over the next 2 quarters, a couple of fab shops that will be fab-only serving multiple EMCOR companies and also the external market.
And then the other thing to always think about with us, one of the reasons people sell their companies to us is a lot of times they have good fab capability. Others don't have great fab capability. And as a result of that, we help them with best practice learning and build the right fab shop for them to grow in the future.

**Operator** (Operator):
And the next question comes from Justin Hauke with Baird.

**Justin Hauke** (Analysts):
Great. So yes, I wanted to ask -- I feel like this has been a question on kind of across the space. But on the cash flow, the net contract liabilities balance went up a pretty decent amount, I guess, on some of the advanced billings on some of these earlier-stage projects. But I guess, Jason, maybe you could just talk about the sustainability of that, given that you've had such rapid growth, and that's obviously a very favorable working capital dynamic. But to the extent that growth, I don't know, moderates or maybe just doesn't grow at the same pace, how that would potentially reverse itself?

**Jason Nalbandian** (Executives):
Sure. Sure. So I mean, you're right. Some of the growth that we saw this quarter in contract liabilities just goes hand-in-hand with the growth we've seen in backlog or RPO. And that's typical. The flip side, though, is we still do have a significant investment in working capital in the form of unbilled and accounts receivable. And so if growth were to slow, you are going to see that start to liquidate and you're going to see that turn into cash flow. And to some extent, that's part of what drove this quarter's cash flow in Industrial, right? We had fairly strong growth last quarter in Industrial. We were up nearly 30%. This quarter, revenues were relatively flat. You saw the flip of that favorably impacting cash flow. So in a period where growth slows for us, we've historically spit off a lot of cash, and I think that would happen again.

**Anthony Guzzi** (Executives):
Yes. And it's always important to know, billings in advance doesn't mean we're getting all cash in advance.

**Jason Nalbandian** (Executives):
Some of that is offset by the increase in AR. Some of it is just advanced billings that haven't been collected yet. Some of it is deposits. So it's a combination of both, right?

**Justin Hauke** (Analysts):
Sure. All right. No, that makes sense. And then I guess maybe my second one here would just -- and obviously, margins were really good this quarter and the outlook is higher. On the Mechanical side, you talked about the mix impacts. I think you guys have been talking about that for a while. But just curious if you could quantify how much maybe that's weighing on the margins? And also, to what extent does that continue? When do we get to a point -- I mean, I guess it can change all the time. But assuming the mix stays at the same level, when does that kind of...

**Jason Nalbandian** (Executives):
I think the level we're running at today is where we're going to be running for probably the next 12 months or so, right? So there's been a year-over-year decline in Mechanical margin because of the mix shift. I think as we enter '27, that decline goes away. I think the margins are around this level. Again, if you look at a rolling 12- to 24-month average for Mechanical, that puts you in the 12% to 12.5% margin range. I think that's where we're going to be for some time.

**Anthony Guzzi** (Executives):
Yes, because I think the more AI data centers become part of the mechanical mix, the designs on those are so much more dynamic. And also that's sort of the contracting method of choice for one of the big customers we work with. And that's not going to change. We're not going to seek to change it because it is so dynamic. These are still really good gross margin jobs. They're really good jobs. And they contribute pretty significant margin dollars, which is really -- and you've heard me say this before, the margins we're operating in now, we're much more in the quest for margin dollars than margin percentages.

**Operator** (Operator):
And the next question comes from Brian Brophy with Stifel.

**Brian Brophy** (Analysts):
Great quarter. Just following up your answer to Brent's question, it sounds like you're leaning more into fab-only capacity here relative to what you've talked about in the past. So I guess I'm just curious as to what changed. Is this a reflection of the demand environment or something else? And how you're thinking about managing risk given the incremental fixed costs?

**Anthony Guzzi** (Executives):
The incremental -- so for us, think about fixed costs, we lease the facilities. We have the capital in it. And these are long-term, I would say, geographically advantaged locations we're going to. So if there is a fixed cost turnabout, we will get out of less productive facilities long term and go to these.
Secondarily, nothing has really changed in how we think about it. It's just we have 1 or 2 customers who like what we've done on the work that we do and see the fabrication that we do. And in places where we don't have installation capability, they'd like us to support them on how they are going to build out longer term.
Like I said, we're not going to be looking to build buildings and put them on trailers with a bunch of other people's equipment and ship them to job sites. That's not what we do. What we do is take the capability we have, whether it be on some of the substation packages we do or even things like that and also some of the work we do on piping packages and then serve the market more broadly, which also allows us to absorb the fixed cost in the facilities we have. So not a shift in what we do, responding to our customers and being supportive of them.

**Jason Nalbandian** (Executives):
And I think even if we made some larger investments in that space, CapEx for us is still going to be 1% or less of revenue, still in terms of investment, not significantly...

**Anthony Guzzi** (Executives):
It's really tied to the revenue growth.

**Brian Brophy** (Analysts):
Understood. That's really helpful. And then you touched on some of the SG&A leverage you're seeing. Curious how much runway is left there. And part of the reason I'm curious is that it's been less of a margin driver for you guys in the past despite some of the really healthy top line growth we've seen over the past, call it, 5 years. I guess I'm just curious if something has structurally changed there and how you're managing costs on that line.

**Anthony Guzzi** (Executives):
Not really. We are getting some efficiencies, right, with favorable mix. Large projects -- and because we're shifting more to large project mix, we do absorb more SG&A doing that. Also, nothing structural, it'd be probably small into this. But the positive of GMP contracts is you can absorb more through general conditions of your SG&A overhead into those contracts than you may get right on a fixed price contract.
Nothing very much structurally. I just think it's the mix of large project work, coupled with us -- because it's large projects, you don't have to hire 5 project managers, you can have 2 versus when you're doing the smaller work, you still need more people to do that.

**Jason Nalbandian** (Executives):
And then the other factor is just field incentive compensation is variable. A lot of that runs through SG&A. And so in the last few years where we've had a pretty sizable expansion of gross profit margins, you're going to have greater field incentive comp, which will drive SG&A margins up as well. This year where that incremental gross profit margin hasn't been as large, you're going to see the benefit in SG&A because the field compensation doesn't increase to the same extent.

**Operator** (Operator):
And the next question comes from Avi Jaroslawicz with UBS.

**Avinatan Jaroslawicz** (Analysts):
Just on the high-tech manufacturing vertical, still seeing that not really accelerating yet, but it does look like it's nearing an inflection point. Just wondering how you're thinking about growth within that specific market sector.

**Anthony Guzzi** (Executives):
We remain pretty excited about growth in that market sector. The first phase usually comes in a lump and then thereafter, it gets awarded in smaller packages. But clearly, there's a couple of sites that we're pretty excited about. We are participating in. One of those companies is expanding to another geography and they want us to be part of it. And we'll balance that specific market sector against other markets and opportunities in that market, specifically data centers at times. And whether there's a big data center build, we'll balance between the 2 of them over a 2-year period. We have the capability. We're good at it. But it's not always the best use of our resources in a given 1- or 2-year period.

**Jason Nalbandian** (Executives):
And I also think you can see it starting to flip in our favor now. If you look combined construction year-to-date, that sector is down $162 million, but in the quarter, the decrease was only $6 million. So I think this is the first quarter in a while where we actually saw the semiconductor revenues increase. It's just being offset by a bit of a decline in some of the EV work that we do. So for the second quarter, relatively flat, if you will, in high tech, we're starting to see semis come back.

**Anthony Guzzi** (Executives):
But the bottom line, it's another job in another sector, and we balance it against everything else.

**Avinatan Jaroslawicz** (Analysts):
Right. Okay. That makes sense. And I guess touching your -- continuing on that thread and similar to what you mentioned before. I know not every operating unit that you guys have is working on data centers. So just if we were to see a broader reacceleration in nonres spending, how should we think about how that could impact your business? How much of the business has kind of more room to grow with better end markets?

**Anthony Guzzi** (Executives):
I mean we've grown -- if you go look at our RPOs and you look at the growth in those RPOs outside of data centers, it's pretty stunning, right? Healthcare RPO is up 31% year-over-year; Water & Wastewater up 38% year-over-year; Institutional RPO is up 25% year-over-year; Manufacturing & Industrial RPO is up 10% year-over-year. Really, the only -- and I think Commercial is down 1%, 2%.
We've had pretty good success with RPOs. And that is the precursor for growth in subsequent periods. And we'll serve those markets, especially in the nondata center markets. But a lot of times, when you look at especially at the Healthcare, specifically in Manufacturing & Industrial, we're balancing that in a lot of cases in some markets against data centers. And so I don't want to -- and we haven't really seen a deceleration for the most part in those markets that we serve. So will we benefit from it? I think if you're going to see nonres grow more broadly based on what we've seen in our business, that will likely come in traditional commercial. That will be more so in warehousing and then just more commercial aftermarket with building restacks, energy efficiency and things like that.

**Operator** (Operator):
And the next question comes from Tim Mulrooney with William Blair.

**Timothy Mulrooney** (Analysts):
I know you highlighted some regions where you're doing a lot of work that has nothing to do with data centers. But I'm curious with all the political rhetoric around data center moratoriums and other regulations around data center construction, I'm curious if you've seen any change in project schedules or pushouts of the pipelines in the regions where you are very large and dense in data center work.

**Anthony Guzzi** (Executives):
No. But I think -- so no, because I think most of what's going to get built in the next 2 or 3 years aren't subject to that rhetoric. That rhetoric, they're permitting things and trying to develop things for 18 to 24 or 36 months out. But also, I think a lot of that rhetoric wasn't grounded in fact. And as facts become more aware and people -- the people wanting to build and permit things become more engaged in the local communities and start talking about the benefits. I think the rhetoric will die down and there'll be -- I think there'll be a lot of rhetoric that will die down magically between November 3 and November 30 post election. I think it's just reality.

**Timothy Mulrooney** (Analysts):
Magically. Got it. Okay. That's very clear. Thank you for walking me through that. And then on the data center stuff, sticking with that, you said -- I thought I heard you say in the prepared remarks, I want to make sure I heard that right, that the majority of work you're doing today is still on cloud-based data centers, presumably contrasted with the large liquid cooled AI data centers. I just want to make sure I heard you correctly. And if so, as you -- I did. Okay. So as you look into the backlog, what do you think that mix will look like a year or 2 from now? I still don't have a good sense for that.

**Anthony Guzzi** (Executives):
It's hard for us to do because as they get bigger, I think the distinction starts to go away a little bit. We definitely know when we're building an AI training model data center. We know that. I mean we know what's going on there. We know what it's connected to. When you get to the mixed-use ones, we're less clear. I think 2 things will be true. Even the cloud storage is getting bigger and more resource intensive. And it's pretty clear when it's an AI training module one. The question is the sort of the ones that cope between both of them. But I think, look, because they're so much larger and the contracts are bigger, I would say today, we're probably 65% to 70% cloud and 30% AI. That will probably get to more 50-50 in the future. And where you really see that is Mechanical. That's where we know the difference and see the difference.

**Jason Nalbandian** (Executives):
Yes. The AI is definitely driving a bigger piece of the growth right now in mechanical, hence, the 130% year-over-year increase in data center revenues from mechanical, but still, on balance, more of our revenues are coming from cloud.

**Anthony Guzzi** (Executives):
Yes. And that's even shifted more in Electrical, I agree that comes from cloud.

**Timothy Mulrooney** (Analysts):
Okay. Okay. Really helpful. Congrats on a nice quarter.

**Anthony Guzzi** (Executives):
Tim, just one follow-up on that, though, right? You've noted the political discussion and all the stuff has been around AI data centers is very targeted, right? And I'm not sure people really understand all the things we just talked about.

**Timothy Mulrooney** (Analysts):
Yes. That's why I was asking, Tony, because I see the proposed moratoriums by some of these candidates are like for the large data centers, not the cloud-based ones. So I was curious about that as well. But it sounds like broadly you expect a lot of this to die down after November 4.

**Anthony Guzzi** (Executives):
Well, especially one of them, they can do all the moratoriums they want, but they're one senator of 100 regardless of what they want.

**Operator** (Operator):
And the next question comes from Manish Somaiya with Cantor.

**Manish Somaiya** (Analysts):
Congrats on a strong quarter. I wanted to ask on the margins that are embedded in new awards. Obviously, we see mechanical. And I think, Jason, you kind of went through the math that, that should improve with the current contract structure shifting. But more specifically, I wanted to know about the Electrical, if that 13% is sustainable and how we should sort of think about that going forward?

**Anthony Guzzi** (Executives):
So to be very clear, we didn't say that we thought mechanical margins would vary much from where they are today in the future because...

**Jason Nalbandian** (Executives):
The comps get easier. The comps get easier.

**Anthony Guzzi** (Executives):
The margins stay somewhere in this band. But the reality is the best way to start to see our margins is what we've always said, look back 4 to 8 quarters and you get a pretty good view of what's happening in the market.

**Jason Nalbandian** (Executives):
And so for Electrical, that's somewhere between 12% and 13%, maybe skewing up to 12.5% to 13%. And for Mechanical, that's 12% to 12.5%.

**Anthony Guzzi** (Executives):
Yes. Any contractor that tells you with conviction that they know that this is a baseline for their margins going forward and they only improve from there must be running 1 project. It must be a 1 project or 2 project contractor. Because with 12,000 projects, we couldn't possibly do that. So over a long period of time, we've been very clear with all of our analytical community and our buy side.
Margins move in bands. We are in a very good band structurally. We continue to execute very well. We don't -- we are very much now focused on margin dollars. Could we expand from here? Yes, we could get more SG&A leverage a little bit. Could we have a couple of quarters where we have closeouts that are more favorable? Sure, we could. We can also have quarters where we're starting up more difficult work, and they seem a little more depressed because we haven't released contingency. So I think any responsible contractor talks about margins in bands and talks about growth the same way. And I think that's why we have so much credibility over a very long period of time when we address this subject.

**Manish Somaiya** (Analysts):
That's helpful. And then, Tony, obviously, you gave really good color on the end markets and the diversity of growth coming from those markets. As we think about backlog and RPOs, I mean, it sounds to me like it may not be the best indicator of all the work that you have ahead of you because obviously, orders tend to be lumpy, et cetera. So what are some of the other measures we should look at in understanding the true potential of EMCOR or any other company for that matter?

**Anthony Guzzi** (Executives):
Yes. I think you always have to be careful, right? We've always been very rigorous in how we talk about forward-looking, right? We've always done RPOs. When it all converted about 7, 8 years ago, it was a very easy walk over to us from backlog to RPOs. We don't make up backlog and say it's only contracted work. It's only the noncancelable portion of service agreements. It's only approved change orders. We don't say, well, we know we've done with this customer, this oil and gas customer. We know that we've done this work forever and the turnaround is projected at that. We also know it's all T&M work and that scope can change. We don't say, "Hey, we're on 1 site. They promise us buildings 2 and 3. It has the same scope." So therefore, we're going to give you an RPO number, which is accounting based.
But here's what our real backlog of future opportunity looks like. I think backlog is a pretty good indicator of future awards. What it doesn't capture, and I think you correctly pointed out is what's the potential for us to grow on some of these sites? And I'm always just been careful, right? We have very little work that's canceled. We actually have very little work that we're promised that gets delayed. But I think we sort of had this construct for a while of how we communicate, and it's worked very well for us because it's all in the known. And I think we'll keep it that way.
I think when you think about future demand, the way I think about it is if these end markets continue to grow like they have, we expect to grow in excess of those end markets. We are the largest specialty subcontractor doing data center work. Could it approach 50% of our construction revenue? Sure, it could for a period of time. That's not by design, that's not holding people up. That's literally mix managing over probably 17 or 20 different discrete and geographic markets. And then looking for the best opportunities while continuing to serve our core customers that we've had for a long time.
So I think if you believe in the data center growth and you look at nonres, I think a great construct is what we've said before to the market. If nonres grows x, we're going to grow probably most times 600 basis points above that as a company overall, and our construction business could be somewhere between 700 and 900 basis points above that. And that's, I think, the best contract to think about it because that captures everything. And that's pretty healthy growth. And I think probably the last couple of years, we would even skew a little higher above the nonres growth, but we're giving you a 5-year look at the world, not just a 2-year look at the world.

**Manish Somaiya** (Analysts):
Okay. Super helpful, Tony. And then just lastly, obviously, you've had a number of acquisitions this year, which will entail some purchase accounting, backlog amortization, et cetera, in '27. But I guess what I wanted to gather was, how should we think about EBITDA accretion becoming EPS accretion when it comes to these acquisitions? I mean what's the time frame? And I guess, what are the indicators, et cetera, that we should think about?

**Jason Nalbandian** (Executives):
I guess the best thing to think about for the newly acquired businesses, particularly Schmidt and Connelly, is that the backlog that we acquired, that amortization period is roughly 16 to 17 months. So that's with us really through the end of '27. And so I think probably what's helpful for everyone on the call, just to give you a sense of what we expect for amortization, both in Q4 and then into '27. So you can obviously see what our amortization is year-to-date in our 10-Q. But if you look at Q4, our expectation is $35.3 million of amortization. It's about $20.1 million in Electrical, $7.7 million in Mechanical, $4.4 million in Building and $3 million in Industrial. And then in 2027, our estimate is about $128 million. It's about $76 million in Electrical, $25 million in Mechanical, $17 million in Building and $10 million in Industrial. And I think if you look at those numbers relative to the year-to-date '26 plus the estimate I just gave you for fourth quarter, you'll be able to see what the impact in '27 is from the incremental amortization.

**Anthony Guzzi** (Executives):
That's just from acquisitions that we've...

**Jason Nalbandian** (Executives):
That's the one that we've announced and we have today, yes.

**Anthony Guzzi** (Executives):
And I think, Manish, you're right to think about EBITDA also. I mean, I think my perfect world, that would be a GAAP number because there's no c*** usually in that. But EBITDA and then we do GAAP earnings, we figure you're smart enough to figure out the benefit. Of course, everything always comes out in cash. And I think across the sector for a very long period of time, we've been the leading cash generator as a percentage of net income or over percentage of net income. And I think that's where the rubber really hits the road, right?

**Operator** (Operator):
The next question comes from Sangita Jain with KeyBanc Capital Markets.

**Sangita Jain** (Analysts):
I just have one. And I know this was related to earlier on semi-fab. It looks like a lot of activity is upcoming in the quarters ahead. And I just want to see how you guys see allocating resources to that end market versus you did in the first cycle of the build-out because you're in a very different place now with all the data center-led demand.

**Anthony Guzzi** (Executives):
We will participate. Where we have real capability is broadly, we have real capability with fire life safety. We will participate broadly with fire life safety. Electrical, really across it a little less so, maybe a little bit in one of the states, Arizona, but outside of -- and maybe Oregon a little bit. But outside of that, less so. Mechanically, Arizona, potentially upstate New York and potentially with one of the customers moving into Texas, we'll participate there. These are all right, you win or you don't. And we're positioned to continue winning well on a couple of these sites.
And then we're putting together good estimates and good potential to maybe participate in the others or get a carve out of scope of the work we want to do. We'll sure know this time next year, we'll know how successful or whether we diverted resources in other places based on pricing.

**Operator** (Operator):
And the next question comes from Adam Bubes with Goldman Sachs.

**Adam Bubes** (Analysts):
I know we're only at Q3 here, but with backlog up 47% year-over-year, can you just talk about visibility you have on growth in 2027, how you're thinking about range of outcomes? And what's your current assessment of your ability to grow head count over the next 12 months to meet the demand that's in your backlog?

**Anthony Guzzi** (Executives):
So I'll start there. We wouldn't have taken the job if we didn't think we could put the resources from field supervision through craft labor on those jobs. We put a manpower plan together with our -- whenever we even estimate work to figure out how -- what slot in with what we have available and what we're going to be able to recruit.
As far as '27, I mean, look, I think you go back to the long-term trends that Jason talked about. And I talked about today about our ability to outgrow nonres. I think that's the best we'll give you on '27. We've been pretty rigorous about not providing forward-looking guidance on the year ahead. You guys are pretty smart to figure it out.

**Adam Bubes** (Analysts):
And then I wanted to talk about your Virginia exposure. I think it's your top market. We've seen some slowdown in announcements in that market and Loudoun County recently enacted a pause on data centers. How are you thinking about the trajectory of incremental awards in Virginia? And just more broadly, how you think through your regional mix evolving over the next year or 2?

**Anthony Guzzi** (Executives):
Look, we're bullish on Virginia. Loudoun County is one county, and I fully expect by the middle of next year. We'll be continuing to see new awards in Loudoun County. I think the reality of Loudoun County was it's booked for the next 2 or 3 years anyway. And so I think it was probably a pause to say, "Okay, where else are we going to build in the county?" They probably were waiting for some power to be provided anyway. Virginia will remain a great market for us. Texas will remain a great market for us. Ohio will remain a great market for us. Iowa will remain a great market for us. I'm just -- Georgia will remain a great market for us. Oklahoma, I'm only providing a few. We're in many, many more markets than that.
But I'm just hitting some of the hot buttons where people have talked about this openly. Pennsylvania will be involved also. I think some of it actually made a lot of sense in a way I've talked about it to the team, and I think collectively, if you put our top 100 data center people in a room, they would agree. Some of it actually will elongate the cycle. And that will be a good thing. And some of it wasn't -- I think some of the thought behind some of the executive orders have made a lot of sense. I think there was a fair amount of phantom demand in Texas, and it wasn't phantom demand with us because of who we serve. But there are other things that people wanted to get involved with. It would be like that's not going to be real anytime soon or you really don't have a plan there. You're just trying to sort of put a stake in the ground.
So I think some of it has been thoughtful. And of course, the whole thing has been full of misinformation. I venture to say this. I think if you put -- so the tax benefits that's happening as a result of these data centers and put 100 school superintendents in a market with the local people, I think when they understood what's available to them and how it can really allow them to build the schools, pay the teachers and the cops and the firefighters and build out world-class facilities like they've done in Loudoun County and like they've done in Louisiana, like they've done in other markets we serve. I think you'll find that these things will get built. They won't get built everywhere. But I think we'll build the capacity. And in being EMCOR, we're well positioned anywhere that matters that they're going to build them.

**Operator** (Operator):
This concludes our question-and-answer session. I would like to turn the conference back over to Tony Guzzi for any closing remarks.

**Anthony Guzzi** (Executives):
Thank you all very much. Thanks for your interest. Thanks for the preparation. I guess we won't talk again until we'll see some of you when we're out and about talking to your buy-side people. But in general, won't see you. Have a great holiday season, and I hope you all stay healthy, and we'll talk to you again in February collectively. Thanks. Bye.

**Operator** (Operator):
The conference has concluded. Thank you for attending today's presentation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### EME_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜CEO｜guidance：CEO 公布上修後的 2026 全年營收與 EPS 財測區間（原話："revenue of between $20 billion and $20.5 billion"）
- 2026-07-30｜CFO｜guidance：財測假設五家併購下半年貢獻 2.5–2.75 億美元營收（原話："$250 million and $275 million of revenue contribution"）
- 2026-07-30｜CFO｜guidance：CFO 說明財測低／中／高端對應的下半年利潤率隱含，且不含 10.6% 重現（原話："the back half of this year looks like the first half"）
- 2026-07-30｜CFO｜guidance：CFO 表示財測中並未假設 Q2 的 10.6% 利潤率重複（原話："not baked into our guidance is that the 10.6% margin repeat"）
- 2026-07-30｜CFO｜guidance：CFO 解釋上修利潤率的理由：營收加速帶來間接成本吸收與 SG&A 槓桿（原話："this is really going to be a revenue story for us"）
- 2026-07-30｜CEO｜guidance：CEO 指出中東情勢使下半年煉油廠停工檢修減少，預期影響第四季利潤率（原話："that's a small impact on margins but it's likely to"）
- 2026-07-30｜CFO｜guidance：CFO 稱併購的 EPS 影響在今年餘下時間有限，因無形資產攤銷與淨利息收入減少（原話："the impact to diluted earnings per share will be limited"）
- 2026-07-30｜CEO｜margin：Q2 營收、營業利益與營業利益率數字（原話："Operating income reached $547 million"）
- 2026-07-30｜CFO｜margin：CFO 拆解 Electrical 利潤率擴張來源：主要是毛利率而非 SG&A（原話："the vast majority of the increase in operating margin"）
- 2026-07-30｜CFO｜margin：CFO 解釋 Mechanical 利潤率下滑 110bp 來自專案組合（CM／prime、GMP／cost-plus 比重上升）（原話："an increase in the number of GMP or cost-plus contracts"）
- 2026-07-30｜CEO｜margin：CEO 稱利潤率以區間管理，Electrical 目前位於區間中點（原話："We always talk about margins in bands"）
- 2026-07-30｜CEO｜margin：CEO 量化合約組合轉向 GMP 的幅度，並指出轉變來自 AI 資料中心（原話："It probably shifted to mechanical 9% to 10%"）
- 2026-07-30｜CEO｜margin：CEO 說明 Q2 有季節性因素（Building Services 強、Industrial 較強）不利後續利潤率（原話："The second quarter is always a strong building"）
- 2026-07-30｜CFO｜margin：Building Services 利潤率擴張 130bp，拆為毛利率 +70bp、SG&A −60bp（site-based 重組）（原話："SG&A margin decreased by 60 basis points"）
- 2026-07-30｜CFO｜margin：CFO 稱 Mechanical 利潤率壓力與 Q1 所述一致，且不代表經營哲學改變（原話："I don't think it's an"）
- 2026-07-30｜CEO｜customer：RPO 創高 171.4 億美元，年增 44%，95% 為有機（原話："total RPOs reached a record $17.14 billion, an increase of"）
- 2026-07-30｜CFO｜customer：Electrical 營收成長主要來自資料中心（網通 sector 營收成長 45%）（原話："where revenues increased by 45%"）
- 2026-07-30｜CEO｜customer：被問及資料中心需求輪廓是否有變，CEO 直接回答沒有（原話："Short answer, none. The demand profile remains the same."）
- 2026-07-30｜CFO｜customer：CFO 列出資料中心 RPO 以維吉尼亞州最多，德州第二、喬治亞緊隨（原話："Texas is the second for us and followed closely by Georgia"）
- 2026-07-30｜CEO｜customer：CEO 描述資料中心規模放大與 AI 專案的乘數（原話："we get a multiplier of 1.5 to 2 on AI data center"）
- 2026-07-30｜CFO｜customer：半導體領域 RPO 年初至今與季增均約 7%，CFO 預期稍後出現成長（原話："RPOs are up in that space about 7%"）
- 2026-07-30｜CFO｜customer：CFO 說明年初需另行簽約並完成的營收比例已大幅下降（本年約 40%）（原話："I think this year, it was 40% of the"）
- 2026-07-30｜CFO｜customer：CFO 稱 RPO 12 個月內轉化比例由歷史約 85% 降至 75–76%，原因含水務組合與簽約量（原話："it's more like 75% or 76%"）
- 2026-07-30｜CFO｜customer：CFO 說明 RPO 成長快於營收財測，部分為動員時點（原話："Some of that is just the timing of mobilization"）
- 2026-07-30｜CEO｜competition：被問與透過併購進入市場的競爭者比較，CEO 稱各工種專業壁壘高、不會因做場地工程而獲得機電標案（原話："These trades are very"）
- 2026-07-30｜CEO｜competition：CEO 說明併購篩選標準未變：先看現場執行力（原話："can they execute in the field"）
- 2026-07-30｜CEO｜competition：CEO 稱機電綑綁投標很少見（原話："very rarely combine a bid"）
- 2026-07-30｜CFO｜capital_allocation：CFO 說明五家併購的 TTM 營收與 EBITDA（原話："collectively generated $625 million of revenues and $105"）
- 2026-07-30｜CFO｜capital_allocation：CFO 說明併購以現金及必要時信貸額度支應（原話："a combination of cash on hand and to the extent"）
- 2026-07-30｜CFO｜capital_allocation：CFO 披露其中兩筆交易最高 9,000 萬美元的 earn-out（原話："up to $90 million in earnouts for 2 of the deals"）
- 2026-07-30｜CFO｜capital_allocation：CFO 表示 2026 資本配置比例將與 2025 相近，M&A 占比上升（原話："as the percentage deployed towards M&A increases"）
- 2026-07-30｜CEO｜capital_allocation：CEO 稱併購管線強，聚焦機電工程與機械服務，不投資不熟悉領域（原話："The pipeline is strong."）
- 2026-07-30｜CEO｜capital_allocation：CEO 對單一市場、客戶或地理的公司持謹慎態度（原話："But we want to pay a fair price."）
- 2026-07-30｜CFO｜capital_allocation：CFO 描述現金流經驗法則（營運現金流至少等於淨利，約為營業利益 80–85%）並預期 2026 與前兩年相似（原話："We see no reason why the operating cash flow in '26"）
- 2026-07-30｜CFO｜commitment：CFO 預期併購的 EPS 貢獻在攤銷退場後逐步增加（原話："these acquisitions will provide further"）
- 2026-07-30｜CEO｜commitment：CEO 預告 Schmidt 與 Connelly 於第三季完成交割（原話："we look forward to closing"）
- 2026-07-30｜CFO｜commitment：CFO 對 2027 不予評論（原話："we won't comment on '27 at this point"）
- 2026-07-30｜CEO｜product：CEO 稱被併購公司可轉向資料中心，並會派員協助現場、前端估價與合約談判（原話："do we implant a couple of our folks"）
- 2026-07-30｜CEO｜product：Mechanical 資料中心可大量預製，減少鄉村市場現場人力（原話："you can have a large"）
- 2026-07-30｜CEO｜risk：CEO 提及宏觀風險（地緣衝突、商品成本、設備交期）（原話："geopolitical conflicts, commodity"）
- 2026-07-30｜CEO｜risk：CEO 談資料中心禁令與州級提案，稱屬局部且業主會找到建置地點（原話："It's sort of laughable that New York put a data center ban"）
- 2026-07-30｜CEO｜risk：CEO 說明勞動力調度方式，含在偏遠市場可能使用非工會營運（原話："there are opportunities for some nonunion operations"）

### 問答異常語氣（迴避／改口／保留）
- EME_Q2_2026_Earnings_Call_20260730.md｜問：UBS 問 Electrical 高利潤率是否有特殊因素，以及下半年是否可能維持 10% 以上｜答法：CEO 否認「everything went right」、改談 ebb and flow 與區間；CFO 不直接答可否維持 10%+，改以財測低／中／高端的隱含說法，並明言 10.6% 不在財測內
- EME_Q2_2026_Earnings_Call_20260730.md｜問：Cantor 問 2027 現金轉換率展望｜答法：CFO 明確拒絕給 2027 評論，改述 2026 的經驗法則與前兩年相似
- EME_Q2_2026_Earnings_Call_20260730.md｜問：Baird 問在 Mechanical 拖累與攤銷下為何仍上修利潤率財測｜答法：CFO 以營收加速帶來的吸收與 SG&A 槓桿回答，未給出攤銷或 Mechanical 拖累的量化數字

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
{"date":"20260518","verdict":"觀望","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 資料中心 capex 結構性 5-10 年週期，EME 是 M&E 落地核心","columns":{"2Y 驗證點":"Hyperscaler 四家加總 2027 capex guidance ≥ 0B（即 vs 2026 0B 持平或上升）；EME RPO 2027 末 ≥ B","5Y 驗證點":"2031 全美 data center 容量達 100+ GW（vs 2025 50 GW）；EME data center 相關 revenue / total ≥ 35%","10Y 驗證點":"2036 AI 工作負載成熟，data center 從 hyperscale build-out 轉 maintenance + retrofit；EME building services 佔比擴大至 30%","驗證指標":"RPO 絕對額、data center exposure %、hyperscaler capex guidance","資料來源":"2Y: §6 RPO + §11；5Y: §8.A Runway；10Y: §8.A 路線圖 + §9 護城河趨勢"}},{"id":"H2","text":"勞工結構性短缺 + EMCOR 規模優勢轉化為持續定價權","columns":{"2Y 驗證點":"FY26-27 Gross margin 維持 18%+；OPM 維持 8%+","5Y 驗證點":"2031 GM 維持 17-19%，OPM 7-9%（cycle 平均上移）","10Y 驗證點":"2036 union labor 短缺問題尚未解決（美國技術職業教育投入仍跟不上需求）","驗證指標":"Gross Margin、OPM、員工數成長 vs 營收成長","資料來源":"§9 護城河、§10 財務、§11 議價權"}},{"id":"H3","text":"市場給予 EME 中等 PE 溢價（vs FIX 折價 ~40%），thesis 兌現後溢價收斂","columns":{"2Y 驗證點":"FY27 Forward PE 維持 22-28x（即不大幅 derate 至 &lt; 18x）；分析師上修 EPS 至 FY27 .50+","5Y 驗證點":"2031 EPS 達 .00+，PE 即使壓回 20x 仍給 .00 股價（+10% 5Y CAGR）","10Y 驗證點":"10Y EPS .00+，PE 18-22x，股價區間 ,300-1,600（年化 +6% CAGR）","驗證指標":"Forward PE、PEG、分析師目標價中位、FY+2 EPS 共識","資料來源":"§13.1 / §13.5 / §6 共識追蹤"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Hyperscaler capex cycle peak — 任一家 (AWS/MSFT/GOOG/META) 大幅下修 2027 capex","columns":{"對應假設":"H1","時間尺度":"短期（12 月內）⚡","監測指標":"四家加總 2027 capex guidance；EME RPO QoQ 動能","警戒閾值":"四家加總 2027 capex guidance &lt; 0B（即 vs 2026 0B 下修 8%+）；或 EME RPO 連續 2 季 QoQ 轉負且絕對額下降 — 削弱閾值"}},{"id":"R2","text":"Margin cycle peak — FY25 OPM 8.7% 為 10 年新高，回歸 cycle 均值 ~6%","columns":{"對應假設":"H2","時間尺度":"中期（2-3 年）🔥","監測指標":"Gross Margin / OPM 趨勢；勞工通膨 vs 議價權","警戒閾值":"Gross margin 連 2 季 YoY 下滑 &gt; 1.5pp；或 OPM FY27 跌破 7% — 削弱閾值；FY27 OPM &lt; 6% — 反轉閾值（H2 thesis 部分失效）"}},{"id":"R3","text":"整合失敗 — Miller Electric M 收購若 integration charge 或 culture clash","columns":{"對應假設":"H1 / H2","時間尺度":"短期（12 月內）⚡","監測指標":"Miller Electric segment 貢獻；無預期 integration cost","警戒閾值":"FY26-27 Miller Electric segment 公布 impairment 或 segment EBITDA 低於 acquisition deck 50%；或管理層淡化「accretive」承諾 — 削弱閾值"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":913.11,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EME_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
