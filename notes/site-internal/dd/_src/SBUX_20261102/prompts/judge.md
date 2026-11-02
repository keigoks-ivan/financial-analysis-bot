你是 stock-analyst **v20 判斷 agent**，標的 SBUX（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"SBUX","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SBUX_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SBUX_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":9141.2,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-10-29）","citation":"公司新聞稿 investor.starbucks.com Q4 FY26 press release／8-K Ex.99.1"},"note":"YoY -4.5%（去年同期 9,569.0）、QoQ -1.9%；略低於共識（Benzinga $9.24B、Yonhap 約低 $80m，聚合站口徑不一）；YoY 下滑主因中國合資交易"},{"id":"f_kpi1_non_gaap_operating_margi","label":"Non-GAAP operating margin","value":14.0,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-10-29）","citation":"公司新聞稿 Q4 FY26 press release"},"note":"Non-GAAP 營業利益 $1,276.9m；非 GAAP EPS $0.80 vs 共識 $0.70（Benzinga）"},{"id":"f_kpi2_gaap_operating_margin","label":"GAAP operating margin","value":10.8,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-10-29）","citation":"公司新聞稿 Q4 FY26 press release"},"note":"GAAP 營業利益 $991.8m；GAAP EPS $0.59"},{"id":"f_kpi4_stock_based_compensation","label":"Stock-based compensation（FY2026 全年）","value":368.6,"period":"FY2026（截至 2026-09-27，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"FY2026（截至 2026-09-27，公告於 2026-10-29）","citation":"公司新聞稿現金流量表；單季未揭露，占營業利益比未算（缺全年營業利益）"},"note":"無共識可比"},{"id":"f_kpi5_comparable_coffeehouse_s","label":"Comparable coffeehouse sales（全球）","value":7.2,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-10-29）","citation":"公司新聞稿 Q4 FY26 press release"},"note":"平均客單 +5.2%、交易數 +1.8%"},{"id":"f_kpi6_guidance_fy2027_53","label":"Guidance FY2027（53 週年度）","value":"Non-GAAP EPS $3.15–3.25；Non-GAAP 營業利益率 13.5%–14.0%；營收約 -1% YoY（含第 53 週約 $700m）；北美同店約 +4.0%；淨新店約 1,200","period":"FY2027 指引（公告於 2026-10-29）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"FY2027 指引（公告於 2026-10-29）","citation":"公司新聞稿 Q4 FY26 press release"},"note":"Non-GAAP EPS 共識約 $3.13（聚合站）；營收共識約 +1%，指引低於共識；GAAP EPS 指引 $3.07–3.17"}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_sbux_gross_margin_pct","label":"SBUX 毛利率","value":21.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SBUX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sbux_operating_margin_pct","label":"SBUX 營業利益率","value":10.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SBUX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_sbux_fcf_margin_pct","label":"SBUX FCF 利潤率","value":9.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SBUX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wing_gross_margin_pct","label":"WING 毛利率","value":49.37,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WING.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wing_operating_margin_pct","label":"WING 營業利益率","value":27.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WING.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wing_fcf_margin_pct","label":"WING FCF 利潤率","value":15.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WING.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mcd_gross_margin_pct","label":"MCD 毛利率","value":57.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mcd_operating_margin_pct","label":"MCD 營業利益率","value":45.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mcd_fcf_margin_pct","label":"MCD FCF 利潤率","value":28.02,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dpz_gross_margin_pct","label":"DPZ 毛利率","value":40.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DPZ.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dpz_operating_margin_pct","label":"DPZ 營業利益率","value":19.5,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DPZ.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dpz_fcf_margin_pct","label":"DPZ FCF 利潤率","value":12.55,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DPZ.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cmg_gross_margin_pct","label":"CMG 毛利率","value":23.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMG.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cmg_operating_margin_pct","label":"CMG 營業利益率","value":14.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMG.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cmg_fcf_margin_pct","label":"CMG FCF 利潤率","value":11.88,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMG.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_free_cash_flow_fy2026","label":"Free cash flow（FY2026 全年，新聞稿僅揭露年度現金流量）","value":3724.8,"period":"FY2026（截至 2026-09-27，公告於 2026-10-29）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"FY2026（截至 2026-09-27，公告於 2026-10-29）","citation":"公司新聞稿現金流量表自算：營運現金流 4,988.4 − 資本支出 1,263.6（非公司自報 FCF；單季未揭露）"},"note":"無共識可比"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":103.65,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-0.97,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":63.45,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":21.46,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.61 → 3.17）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":19.81,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.13 → 3.75）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":16.13,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.72 → 4.32）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.17,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.75,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":4.32,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":32.64,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 2.39 → 3.17（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":46.9,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝82.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":82.6,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.12,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.61,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":32.7,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 3.17，分子＝快照價 103.65","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.393,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":18549.4,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 22413.6、現金 3864.2（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1140.1,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":136720.76,"period":"2026-11-02","unit":"USD m","basis":"市值 118171.36 ＋ 淨負債 18549.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":37844.88,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（26 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":39423.64,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（26 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.61,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 103.65 / W52 96.28 / W104 92.79 / W250 88.27 / W250 13週斜率 0.01%"},{"id":"f_ma_w52","label":"52 週均線","value":96.28,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":92.79,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":88.27,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.01,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：Starbucks 承認並非每個細分市場都居領先，美國大型快餐業者可能壓低客流與客單，全球面臨既有品牌、新進入者與小型專業業者競爭，對手可能以同價或更低價搶份額。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm","excerpt":"We face increasing competition in all channels and markets and do not hold leadership positions in every segment. In the U.S., large quick-service competitors offering coffee, tea, and other competitive products may reduce customer traffic and transaction value. Globally, competition from established brands, new entrants, and smaller specialty operators may hinder growth and impact sales.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"AP/Technomic：星巴克占美國咖啡店消費支出份額由 2023 年 52% 降至 48%，Dutch Bros、Luckin 等連鎖競爭加劇","source":"AP via Fortune, Starbucks feels the heat as more chains compete for US coffee drinkers","url":"https://fortune.com/2026/01/31/starbucks-polyamorous-era-coffee-drinking-dunkin-dutch-bros-luckin/?rand=8593","excerpt":"it now stands at 48%, down from 52% in 2023, according to Technomic, a food industry consulting firm. Dunkin ‘, a perennial rival that just opened its 10,000th U.S. store, gained market share in both of those years. Starbucks has other challengers, like the fast-growing drive-thru chains 7 Brew, Scooter’s Coffee and Dutch Bros.","as_of":"2026-01-31","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Luckin 與 Cotti 進入美國市場，以 $2–3 價位低價切入","source":"eMarketer, Chinese coffee companies Luckin and Cotti plot US expansion","url":"https://www.emarketer.com/content/chinese-coffee-companies-luckin-cotti-plot-us-expansion","excerpt":null,"as_of":"2025-06-01","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SBUX FY2026 全年 global comparable sales +6.2%（comparable transactions +3.2%、average ticket +3.0%），合併淨營收 $37.9B；FY2027 outlook 搜尋未見。","source":"Starbucks 8-K FY2026 Q4 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000829224/000082922426000154/sbux-09272026xearningsrele.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"SBUX FY2026 計畫淨新增 600–650 店；FY26 Q3 末 41,304 店（該季淨增 175），維持全年區間。","source":"Nasdaq/Zacks: Starbucks Targets 600-650 New Stores in FY26","url":"https://www.nasdaq.com/articles/starbucks-targets-600-650-new-stores-fy26-execution-key","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"NRA 預測 2026 實質餐飲銷售 +0.8%（早先預測 1.3%），2027 預期成長轉強至 4.8%；Black Box 2027 預測為銷售小幅成長、客流大致持平。","source":"National Restaurant Association / Black Box Intelligence","url":"https://restaurant.org/research-and-media/research/restaurant-economic-insights/analysis-commentary/restaurants-remain-resilient-despite-challenging-business-conditions/","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"業界客流疲弱，評論認為 oversaturation（單位過多）為結構性原因之一，但該說法來自分析師評論與意見文，無單位數據佐證。","source":"Tagex Brands: Oversaturation in the Restaurant Industry","url":"https://www.tagexbrands.com/?p=1845","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"咖啡連鎖競爭者仍擴張：Dutch Bros 2026 Q1 末 1,177 店、計畫至少新開 185 店；7 Brew 朝 1,000 店；Luckin 約 36,000 店。","source":"Restaurant Dive 7Brew; 綜合咖啡連鎖擴張報導","url":"https://restaurantdive.com/news/7brew-on-pace-reach-1k-units-2026/822608/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K FY2025 風險因子：個資法規快速演變，FTC 與各州檢察長正將消費者保護法適用於線上資料作法，可能帶來罰款與訴訟（屬資料隱私監管，非反壟斷）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm","excerpt":"Regulatory scrutiny is intensifying, with agencies such as the Federal Trade Commission and state attorneys general applying consumer protection laws to online data practices.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋未見 2026 年 DOJ／FTC／歐盟對星巴克的反壟斷調查或拆分行動；歐盟對其稅務裁定的國家補貼調查已於 2024-11-28 結案（稅務案，非競爭案）。","source":"WebSearch 結果摘要（歐盟執委會競爭政策頁）","url":"https://competition-policy.ec.europa.eu/sectors/financial-services/latest-news_fi","excerpt":null,"as_of":"2024-11-28","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2026-10 有集體訴訟指星巴克八款「sugar-free」蛋白飲含 13–21 克糖，可能牴觸聯邦標示規範（私人訴訟，未見監管機關行動）。","source":"Simply Wall St 經 Webull 轉載","url":"https://www.webull.com/news/15700040195703808","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：關稅已影響、未來也可能影響咖啡採購成本；公司對咖啡價格上漲的避險能力有限，且供應給授權店的策略性產品（含咖啡）轉嫁成本能力有限。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm","excerpt":"Tariffs have also affected, and in the future may affect, our costs to procure coffee. Given coffee’s central role in our operations and our limited ability to fully hedge against price increases, rising costs or supply shortages could materially impact our profitability and ability to meet customer demand.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 列示貿易政策／關稅／進出口法規變動為風險，過去已對公司造成不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm","excerpt":"Changes in the import and export policies, including trade restrictions such as new, increased, threatened, or retaliatory tariffs or quotas, embargoes, sanctions and countersanctions, safeguards, or customs restrictions by the U.S. and foreign governments, have in the past required, and could in the future require, us to change the way we conduct business","as_of":"2025-11-14","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"MD&A：預期新關稅與咖啡價格波動的總體挑戰持續；關稅直接影響商品價格與可得性及營運結果。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm","excerpt":"The price and availability of these commodities, including impacts from volatility in green coffee prices and new tariffs, directly impact our results of operations, and we expect commodity prices, particularly coffee, to continue to impact future results of operations.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"CFO 預期咖啡價格與關稅壓力於 Q2 見頂、H2 2026 緩解","source":"Newsquawk, Starbucks CFO conference call","url":"https://www.newsquawk.com/headlines/starbucks-sbux-cfo-continues-to-expect-coffee-prices-and-tariff-pressures-to-peak-in-q2-and-find-some-relief-in-h2-26---conference-call","excerpt":"Starbucks (SBUX) CFO continues to expect coffee prices and tariff pressures to peak in Q2 and find some relief in H2 '26 - conference call Newsquawk Staff · 28 Jan 2026, 13:46 UTC","as_of":"2026-01-28","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露在 89 個市場營運，面對多元地緣政治環境；風險清單含關稅、制裁與地緣不穩造成的勞動中斷","source":"Starbucks Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm","excerpt":"Operating in 89 global markets, we face diverse cultural, regulatory, geopolitical, and economic environments.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2024 10-K 列出中國業務特有的資料隱私與網路安全風險","source":"Starbucks Form 10-K FY2024","url":"https://www.sec.gov/Archives/edgar/data/829224/000082922424000057/sbux-20240929.htm","excerpt":"data privacy and cybersecurity risks unique to the conduct of business in China","as_of":"2024-11-15","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Panjiva 資料顯示哥倫比亞占 Starbucks 進口約 29.5%（原產地集中）；巴西咖啡豆受關稅影響","source":"Panjiva: Colombia's Coffee Leadership May Slip as Starbucks Stockpiling Ends, Tariffs Bite","url":"https://es.panjiva.com/research/colombias-coffee-leadership-may-slip-as-starbucks-stockpiling-ends-tariffs-bite/19232","excerpt":"While underlying demand from buyers, led by Starbucks and Rothfos may be robust a reduction in stockpiling may rapidly cut demand. That would be particularly keenly felt in Colombia which accounted for 29.5% of Starbucks’s imports and 39.1% of Rothfos’s in the past 12 months.","as_of":"2025-09-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026 年 10 月報導美國眾議院中國委員會主席要求 Starbucks 關閉新疆兩家新店；中國外交部否認","source":"TIKR blog","url":"https://www.tikr.com/pt/blog/starbucks-xinjiang-stores-us-lawmaker-demands-closure","excerpt":"Legislador dos EUA Exige que Starbucks Feche Lojas no Xinjiang, China Aditya Raghunath • 4 minutos de leitura Avaliado por: David Hanson Última atualização Oct 5, 2026","as_of":"2026-10-05","retrieved_at":"20261102","affects":["thesis.R","triggers"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY26 Q4：北美可比銷售+7.9%（均單+5.0%、可比交易+2.7%），北美營收+6%至$7.33B；國際可比銷售+0.9%、交易-2.8%，國際營收-37%至$1.3B（中國零售轉授權合資）","source":"Starbucks Q4 FY2026 earnings release / 8-K","url":"https://investor.starbucks.com/news/financial-releases/news-details/2026/Starbucks-Reports-Q4-and-Full-Fiscal-Year-2026-Results/default.aspx","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"FY27 指引：營收約-1%、北美可比銷售約+4.0%、non-GAAP EPS $3.15–3.25","source":"Starbucks Q4 FY2026 earnings release (via search summary)","url":"https://investor.starbucks.com/news/financial-releases/news-details/2026/Starbucks-Reports-Q4-and-Full-Fiscal-Year-2026-Results/default.aspx","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Technomic 數據：星巴克美國咖啡店支出占比由2023年52%降至2024–25年約48%，外帶車道與低價競爭者擴張；USDA預估2026外食通膨4.6%","source":"StoneX - Starbucks losing share in US market despite firm demand","url":"https://www.stonex.com/en-gb/insights/starbucks-losing-share-in-us-market-despite-firm-demand/","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"NRA 2026預估美國餐飲業銷售約$1.55兆、實質成長1.3%；IBISWorld 美國咖啡簡餐店2026市場$75.5B、成長約0.2%","source":"NRA 2026 State of the Restaurant Industry; IBISWorld","url":"https://shop.restaurant.org/2026-State-of-the-Restaurant-Industry","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"中國咖啡市場分析師預估2025年$18.7B、至2030年年增近6%，競爭加劇","source":"Seeking Alpha - Coffee competition in China is heating up","url":"https://seekingalpha.com/news/4520399-coffee-competition-in-china-is-heating-up-these-are-the-major-players","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"機器人咖啡師(robotic barista)市場2026年約21.8億美元、2030年預計40.5億美元（促銷稿，未驗證）","source":"Daily Tribune press release: The $4 Billion Robotic Barista Boom","url":"https://www.daily-tribune.com/online_features/press_releases/the-4-billion-robotic-barista-boom-how-ai-coffee-kiosks-are-reshaping-global-retail-in/article_f8501c3a-d6d6-5942-9386-63f97c8a000e.html","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K: Channel Development was 5% of revenue; large portion runs on a licensed model via Nestlé Global Coffee Alliance; North America 74%, International 21%.","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm","excerpt":"Revenues from our reportable operating segments as a percentage of total net revenues for fiscal 2025 were as follows: North America (74%), International (21%), and Channel Development (5%).","as_of":"2025-11-14","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Starbucks and Boyu closed China JV on 2026-03-30; Boyu funds took 60%, Starbucks 40%; China company-operated stores moved to licensed model.","source":"Business Wire: Starbucks and Boyu Capital Finalize Joint Venture","url":"https://www.businesswire.com/news/home/20260330750110/en/Starbucks-and-Boyu-Capital-Finalize-Joint-Venture-to-Accelerate-Long-Term-Growth-in-China/","excerpt":null,"as_of":"2026-03-30","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-Q (quarter ended 2026-03-29): China JV stores transitioned to licensed operating model; equity-method accounting.","source":"SEC 10-Q FY2026 Q2","url":"https://www.sec.gov/Archives/edgar/data/0000829224/000082922426000080/sbux-20260329.htm","excerpt":"our share of income from the joint venture, recognized as income from equity investees under the equity method of accounting, and recording revenues related to product sales and royalties. The disposal group was deconsolidated from our financial statements and will be reported as part of our licensed portfolio in the third quarter of fiscal 2026.","as_of":"2026-05-01","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 FY26 (報告 2026-07-29)：公司把 FY2026 調整後 EPS 指引由 $2.25–2.45 上修至 $2.55–2.65；全球可比店銷 +7.9%，營收 -1% 至 $9.3B（中國 JV 轉型）；淨新增店 600–650 維持。","source":"Starbucks 8-K FY2026 Q3 earnings release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000829224/000082922426000129/sbux-06282026xearningsrele.htm","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Chartmill 2026-10-24 快照：FY2026 EPS 共識 2.67（41 位分析師），Q4 FY26 預期 EPS $0.73、營收約 $9.418B；EPS 共識近 1 個月 -0.08%、近 3 個月 +9.06%。共識略高於公司指引區間中點 $2.60，落在區間上緣之上。","source":"Chartmill SBUX estimates","url":"https://www.chartmill.com/stock/quote/SBUX/estimates","excerpt":null,"as_of":"2026-10-24","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布（Benzinga 情緒頁，日期未標）：平均 $107、高 $125、低 $90，30 位分析師共識 Outperform。TickerLeague 另列共識 $108.53（中位 $111，區間 $90–120，僅 2 位分析師）。皆為聚合站、as_of 不明。","source":"Benzinga SBUX sentiment; TickerLeague SBUX estimates","url":"https://jp.benzinga.com/quote/SBUX/sentiment","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 後個別目標價：Wells Fargo $125、Morgan Stanley $115、UBS 與 Citigroup $112、DA Davidson $110；MarketBeat 彙整平均約 $110–112，共識評等 Moderate Buy。Q3 調整後 EPS $0.85 vs 共識 $0.66。","source":"MarketBeat 2026-07-29/30 alerts","url":"https://www.marketbeat.com/instant-alerts/starbucks-nasdaqsbux-updates-fy-2026-earnings-guidance-2026-07-29/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 上修指引：EPS $2.55–2.65","source":"Nasdaq Q3 call highlights","url":"https://www.nasdaq.com/articles/starbucks-q3-earnings-call-highlights","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Starbucks 與 Boyu Capital 的中國合資案（Boyu 取得中國零售營運 60% 權益，估值約 40 億美元）2025-11 宣布，2026-04 完成交割；Starbucks 保留 40% 並授權品牌。","source":"New Straits Times 轉載 Reuters：Starbucks closes China deal with Boyu","url":"https://www.nst.com.my/amp/business/corporate/2026/04/1409285/starbucks-closes-china-deal-boyu-plans-expand-stores","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026-09-22 董事會核准「Back to Starbucks」進一步行動：關閉北美約 1% 門市，重組費用約 3 億美元（約 2 億現金、1 億非現金）；FY2026 淨新開店指引由 600–650 降至約 440。","source":"SEC EDGAR 8-K（2026-09-24，Item 2.05）","url":"https://www.sec.gov/Archives/edgar/data/829224/000082922426000145/sbux-20260922.htm","excerpt":"Of the approximately $300 million of restructuring charges to be incurred, the Company anticipates that approximately $200 million will be cash charges primarily related to lease exit costs and employee separation benefits.","as_of":"2026-09-24","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-05-13 董事會核准重組計畫：精簡國內外支援組織與非零售設施，並降低 Reserve／Roastery 門市營運複雜度。","source":"SEC EDGAR 8-K（2026-05-15，Item 2.05）","url":"https://www.sec.gov/Archives/edgar/data/829224/000082922426000088/sbux-20260513.htm","excerpt":"Under the approved restructuring plan, the Company plans to capture cost savings by further streamlining its domestic and international support organization and non-retail facilities.","as_of":"2026-05-15","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"中國業務與 Boyu Capital 合資：Boyu 取得 60% 權益（約 40 億美元），2026-04 報導已交割。","source":"New Straits Times 轉載 Reuters","url":"https://www.nst.com.my/amp/business/corporate/2026/04/1409285/starbucks-closes-china-deal-boyu-plans-expand-stores","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2024 年提起的證券集體訴訟（W.D. Wash.，class period 2023-11-02 至 2024-04-30，因 2024-04-30 下修財測股價單日跌逾15%）仍為主要訴訟；2026-01 另有律所宣布對董事／管理層受託責任的衍生訴訟調查。搜尋未見 2026 年和解或判決消息，現況未確認。","source":"Kirby McInerney / Business Wire：Securities Class Action on Behalf of Starbucks SBUX Investors（2024-09-27）；Johnson Fistel 2026-01 新聞稿","url":"https://www.businesswire.com/news/home/20240927561365/en/Kirby-McInerney-LLP-Announces-the-Filing-of-a-Securities-Class-Action-on-Behalf-of-Starbucks-Corporation-SBUX-Investors","excerpt":null,"as_of":"2024-09-27","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"比利時聯邦食品鏈安全局公告召回部分 Starbucks 品牌 ASIA 茶飲（丙二醇 E1520 含量過高），經香港食安中心轉載（2026-02-13）。屬歐洲授權品項，未見美國 2026 年召回。","source":"Hong Kong Centre for Food Safety 轉載比利時 AFSCA 公告","url":"https://www.cfs.gov.hk/english/rc/subject/files/20260213_1.pdf","excerpt":null,"as_of":"2026-02-13","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"SEC EDGAR 近12個月 12 份 8-K 中含重大項目者 3 份（2.05 兩份、8.01 一份），無 Item 4.02（重編）；搜尋僅見 2005 年租賃會計重編舊案，未見 SEC 調查。","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000829224&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 12 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 11 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"SBUX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":21.9,"operating_margin_pct":10.17,"fcf_margin_pct":9.44,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SBUX","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"WING","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.37,"operating_margin_pct":27.74,"fcf_margin_pct":15.97,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WING","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MCD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.38,"operating_margin_pct":45.71,"fcf_margin_pct":28.02,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCD","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"DPZ","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":40.04,"operating_margin_pct":19.5,"fcf_margin_pct":12.55,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DPZ","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CMG","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.84,"operating_margin_pct":14.95,"fcf_margin_pct":11.88,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMG","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"SBUX"},"financial_history":{"ticker":"SBUX","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-09-30","revenue":32250300000.0,"revenue_yoy_pct":null,"gross_margin_pct":25.96,"operating_margin_pct":13.74,"net_income":3281600000.0,"diluted_eps":2.83,"free_cash_flow":2556000000.0,"fcf_margin_pct":7.93,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-09-30","revenue":35975600000.0,"revenue_yoy_pct":11.55,"gross_margin_pct":27.37,"operating_margin_pct":15.3,"net_income":4124500000.0,"diluted_eps":3.58,"free_cash_flow":3675100000.0,"fcf_margin_pct":10.22,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-09-30","revenue":36176200000.0,"revenue_yoy_pct":0.56,"gross_margin_pct":26.84,"operating_margin_pct":14.12,"net_income":3760900000.0,"diluted_eps":3.31,"free_cash_flow":3318100000.0,"fcf_margin_pct":9.17,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-09-30","revenue":37184400000.0,"revenue_yoy_pct":2.79,"gross_margin_pct":22.77,"operating_margin_pct":9.63,"net_income":1856400000.0,"diluted_eps":1.63,"free_cash_flow":2442000000.0,"fcf_margin_pct":6.57,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/SBUX/SBUX_Q4_2026_Earnings_Call_20261029.md）

# Q4 2026 Earnings Call
**Starbucks Corporation** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good afternoon, and welcome to Starbucks' Fourth Quarter and Full Fiscal Year 2026 Earnings Call. [Operator Instructions].
I will now turn the call over to Catherine Park, Vice President of Investor Relations. Ms. Park, you may now begin your conference.

**Catherine Park** (Executives):
Good afternoon, and thank you for joining us today to discuss Starbucks' Fourth Quarter Fiscal Year 2026 results. Today's discussion will be led by Brian Niccol, Chairman and Chief Executive Officer; and Cathy Smith, Executive Vice President and Chief Financial Officer. 
This conference call will include forward-looking statements, which are subject to various risks and uncertainties that could cause actual results to differ from these statements. Any such statements should be considered in conjunction with cautionary statements in our earnings release and risk factors discussed in our filings with the SEC. Starbucks assumes no obligation to update any of these forward-looking statements or information. 
Certain metrics referenced on today's call are non-GAAP and measured in constant currency. Please refer to the earnings release on our website at investor.starbucks.com to find reconciliations of these non-GAAP measures to the corresponding GAAP measures and supplemental financial information. 
This conference call is being webcast, and an archive will be available on our website through Friday, December 11, 2026. And for your calendar planning purposes, please note that our first quarter fiscal '27 earnings conference call is tentatively scheduled for Wednesday, January 27, 2027.
I'll now turn the call over to Brian.

**Brian Niccol** (Executives):
Good afternoon, and thanks for joining. We closed fiscal 2026 with another terrific quarter and a much stronger Starbucks than we had a year ago. Back to Starbucks started as a turnaround plan and now Back to Starbucks is our growth plan. In Q4, our net revenues were $9.1 billion, down 3.9% year-over-year, reflecting the midyear transition of our China business to a licensed model.
Global comps were up 7.2%, marking our fifth consecutive quarter of comp growth and U.S. comps were up 7.7%. Consolidated operating margin expanded 450 basis points year-over-year to 14%, our third consecutive quarter of margin growth and earnings per share grew approximately 54% to $0.80. For the full year, consolidated net revenues grew $37.9 billion, up 2.1%. 
Global company-operated comps were up 6.2%, with U.S. comps up 6.5% and international comps up 3.7%. Consolidated operating margin expanded 200 basis points to 11.9% and earnings per share grew approximately 27% to $2.72, exceeding the high end of our guidance. These results reflect our relentless focus on executing our Back to Starbucks strategy. 
Two years ago, we committed to getting Back to Starbucks and delivering our brand promise more consistently. We put the customer at the center of every decision. We gave our partners more support. We got clear on what matters. We restored the third place, and we put Starbucks back on its front foot. Our plan is working. More customers are visiting us because the Starbucks experience is better. 
Our coffeehouses are coffeehouses again, our partners are creating more moments of connection. Our brand is more visible, relevant and loved. Our license and channel development businesses are extending our reach to more places and occasions. And more of our sales growth is translating into earnings.
For more than 50 years, we've grown by delivering on the Starbucks brand promise, exceptional coffee, human connection and a great customer experience in a true third place. It comes down to the fundamentals. When we execute them with excellence, we grow. That's what we saw in fiscal '26 and it's what gives me confidence in the durability of our performance for the future.
We had a great quarter and a great year, and it put us ahead of schedule on our fiscal '28 framework. And as we focus on growth in fiscal '27, we have even more opportunity ahead.
Let me walk you through some of the highlights for the quarter, starting in North America. Company-operated comps grew 7.9%, driven by double-digit comps in Canada and strong comps in the U.S. That momentum is being driven by great execution in our coffeehouses, a strong brand and a healthier portfolio.
First, our coffeehouses are coffeehouses again. We're operating with greater discipline and consistency anchored by Green Apron Service. In the quarter, more than 80% of our North America company-operated coffeehouses delivered positive comps, up from less than 50% a year ago.
Average service times remained on target, and we continue to refine Smart Queue and our operating routines to improve throughput and consistency across all access points. Inventory availability is at an all-time high with daily delivery now reaching close to 90% of our North America company-operated coffeehouses, and our new quarterly coffeehouse incentive program is driving greater discipline around staffing and product waste, while keeping teams focused on great customer service.
Our leadership pipeline is also getting stronger. We now have more than 3,000 coffeehouses coaches enrolled across our U.S. company-operated business, and they've all been hired from within the company. These positions improve leadership stability and execution, give our partners new pathways to grow and help build the next generation of leaders to support our future growth.
Second, customers are responding to a stronger, more relevant brand and menu. Starbucks brand affinity is at near record levels as our menu innovation, marketing and merchandise continue to create moments that drive culture and bring people into our coffeehouses. Espresso, Refreshers, Matcha and our artisanal bake case showed continued strength in the quarter. 
Our Unicorn launch in August United 34 markets for our first Global coffeehouse activation and delivered a record sales weekend for our North America company-operated business. We followed that with our strongest North America fall launch day and our global Peanuts collaboration demonstrated the power of great merch, delivering robust sales days around the world. 
Our U.S. company-operated comp growth remained balanced with contribution from both ticket and transactions. 90-day active Starbucks Rewards members reached a record 36 million, growing both year-over-year and sequentially from Q3. And sales growth remains broad-based across income levels, generations and dayparts.
Together, these results tell us the Starbucks Experience is resonating. Our coffeehouses feel more like Starbucks too. As of fiscal year-end, we surpassed our goal by completing more than 1,700 total uplifts across North America, bringing back warm, comfortable seating and the third place to our cafes. Uplifted coffeehouses continue to show transaction lift across access points, dayparts, formats and loyalty groups, giving us confidence to continue our pace of work.
Third, we're building a healthier coffeehouse portfolio. In North America, we closed coffeehouses that didn't show a path to delivering the experience or financial performance we expect. We also unveiled our smaller format coffeehouses in multiple markets, taking the concept we showcased at Investor Day from prototype to reality in less than a year.
Customer and partner feedback has been terrific, and we'll learn from these early openings to help shape how we build for the future. International is an important growth engine for Starbucks. Our diversified portfolio remained a key strength in Q4 with comp sales growth across the majority of our licensed and company-operated markets, led by the U.K., Philippines and Mexico.
Our increasingly licensed international model, which combines the power of Starbucks with the deep market expertise of local operators underpinned our unit growth. China exceeded its goals in fiscal 2026, we surpassed 6,000 coffeehouses in Asia Pacific, and we grew to more than 1,900 in Latin America and the Caribbean, bringing Starbucks premium coffee experience to nearly 500 new communities.
Our progress through fiscal '26 reinforces what we know. We know what makes Starbucks special. We know Back to Starbucks drives growth, and we know how to win. For fiscal '27, we will raise the bar. We entered the new fiscal year on stronger operational footing and with momentum. At a high level, for fiscal '27, we expect North America comps of approximately 4%, consolidated operating margin of 13.5% to 14% and EPS of $3.15 to $3.25. 
To deliver these results, 5 priorities will drive our work. First, win on the fundamentals in the coffeehouse through Green Apron Service. That means building capacity to deliver exceptional Green Apron Service to more customers. We see room to grow transaction across every daypart in our coffeehouses by extending our peak in the morning and creating a peak in the afternoon. 
To do this, we'll keep making Smart Queue smarter, we'll improve production flow behind the bar to unlock throughput while maintaining great craft. We'll also begin Mastrena 3 espresso machine test and exploring next-generation drive-through concepts to improve speed and connection. It means greater operating precision. 
We'll keep refining how we forecast and deploy labor and how we manage inventory and product waste and we'll raise growth performance expectations while keeping our leaders focused on operating behaviors that create a meaningful third place full of community and connection and drive consistent results. And it means continued investment in our partners. Fiscal '27 will be a major tech modernization year. We'll roll out new staffing and scheduling and point-of-sale systems through the year that simplify tasks, improve speed of service and allow partners to spend more time engaging with customers.
We're also transforming our supply chain with testing underway to improve demand forecasting, ordering accuracy and replenishment cycles. As this work scales, it will drive greater availability, less product waste and less work for our partners over time.
Second, make our branded menu even more relevant and loved. We'll drive mass reach through effective marketing to bring in new and lapsed customers while continuing to nurture our Starbucks Rewards members. We'll keep winning the morning and earning the afternoon with planful innovation, building scalable platforms that can grow with us.
These include functional and zero sugar beverages, new bakery items, more portable options, and protein forward choices that meet more customer needs and wants throughout the day. Great innovation strengthens the ritual and gives customers more reasons to choose Starbucks. In fiscal '27, we'll bring beverages, food and merchandise together in collections that create more compelling customer moments and drive greater attach. 
Merchandise remains a small part of our business today, but Q4 showed its potential. Both our Pink and Peanuts launches contributed to ticket growth in the quarter. We'll apply that same integrated approach to upcoming brand launches like holiday. We've learned a lot about what it takes to execute innovation well. In fiscal '27, we'll put even greater focus on operational readiness with thoughtful builds, better training and the right staffing to help our partners deliver with excellence.
Third, build the right experiences and capabilities for the future. Starbucks has built an exceptional digital experience in one of the world's most engaged customer communities. In the year ahead, we'll make our industry-leading Starbucks app even more intuitive for customers to order, customize and have frictionless access wherever they are. 
We'll update the menu experience and build more personalized touch points through relevant content and recommendations tailored to customer tastes and preferences. In Q2, we'll begin to integrate delivery directly into the Starbucks app and will extend the opportunity for customers to begin earning and redeeming Stars on delivery orders.
We are working on opportunities for AI to make search and discovery in the app more seamless with the potential to support conversational and agentic ordering over time. And we're exploring ways to make it easier for customers to place mobile orders from their cars and through emerging AI platforms.
We're also working to reimagine the drive-thru experience to make it faster, more convenient and more personal. Roughly half of our customers use the drive-thru, making it a significant opportunity. In fiscal '27, we'll begin testing background AI models and the drive-thru that help our baristas input orders more accurately and efficiently as they interact with customers.
The intent is to help our partners focus on connecting with customers while improving both throughput and speed of service. We're also exploring experiences that recognize participating customers as they arrive, present personalized digital menus and make payment more effortless. We're early in this work, and we'll test, learn and scale what works. 
Fourth, grow with discipline in the U.S. and around the world. We see significant long-term white space in North America with the opportunity to build around 5,000 additional coffeehouses over time. We're focused on making disciplined decisions today that set us up for stronger, more durable growth in the future. 
Rebuilding our development pipeline will take time, which means we expect fewer company-operated openings in fiscal '27 and a stronger, healthier pipeline beyond that. As we do this work, we'll continue investing in our uplift program. We expect to complete more than 2,000 uplifts in fiscal '27.
We'll also work to grow our North America license business, bringing the Starbucks Experience to even more customers. We expect International to lead our global unit growth this fiscal year with net new coffeehouse openings accelerating by nearly 50% compared to fiscal '26. That translates to about 3 new coffeehouses a day. 
Beyond fiscal '27, we see substantial room to grow our footprint outside North America from more than 23,000 international coffeehouses today to nearly 40,000 over the long term. That includes the potential to double our presence in China and India with meaningful growth across other regions. 
Fifth, create more opportunity for partners. Our hourly partner turnover rate remains well below the industry average, driven by what third-party studies confirm are industry-leading pay and benefits as well as improved staffing and flexible schedules that give partners the hours they want to work. And in fiscal '27, we'll expand coffeehouse coaches to more North American coffeehouses, giving experienced partners more opportunities for advancement while building a pipeline of talent to support future coffeehouse growth.
We'll pair that with more training and development opportunities and better tools for leaders to build and manage strong teams. Taken together, these priorities give us clear direction and confidence in the path ahead. Back to Starbucks started as a turnaround plan, and it put us back in a position of strength. 
Today, Back to Starbucks is our growth plan. To conclude, fiscal '26 was a tremendous year of progress and results, and it gives us confidence in our trajectory. We're ahead of schedule in relation to our fiscal '28 framework, and we see a clear path to consistent comp growth and stronger earnings in fiscal '27. 
To our partners around the world, thank you. The progress we've made reflects your focus, ownership and belief in our brand promise, I'm confident we'll keep building on what is working, raising the bar and bringing the best of Starbucks to even more customers around the world. 
With that, I'll turn it over to Cathy to take you through our results in more detail and our fiscal '27 guidance.

**Catherine Smith** (Executives):
Thank you, Brian, and thank you all for joining us today. In fiscal 2026, we strengthened the fundamentals of our business and that work is increasingly showing up in our financial performance.
I'd like to also thank our partners whose focus and dedication were critical to delivering our Back to Starbucks priorities. Now to our fourth quarter results and outlook. Fourth quarter consolidated net revenues were $9.1 billion, down 3.9% year-over-year, primarily reflecting Starbucks China's transition from company operated to a licensed joint venture.
Global comps grew 7.2%, our fifth consecutive positive quarter. North America net revenues grew 6.3% to $7.3 billion, led by strong company-operated comps in both the U.S. and Canada. U.S. comps grew 7.7%, with a healthy balance of transactions up 2.4% and ticket up 5.2%. 
Contribution from transactions moderated from Q3, particularly as we began to lap the growth from last year. On a 2-year basis, U.S. transaction comps improved sequentially from Q3, a sign that customers continue to choose us more often. 
And as Brian mentioned, we delivered growth across all dayparts, income levels and access points. Ticket growth continued to reflect balanced contribution from pricing, attach, mix and delivery growth with pricing and mix, including merchandise, driving most of the sequential improvement from Q3.
We've been very pleased with our delivery performance in the U.S., with revenues more than tripling over the past 5 years, and these transactions have been largely incremental, expanding delivery to more coffeehouses supported our growth in fiscal '26 and with delivery soon to be fully integrated into the Starbucks app, we see additional runway in fiscal '27.
We're also driving the engagement we want to see in our Starbucks Rewards program. 90-day active members reached a record 36 million in the quarter. More members are moving into higher frequency tiers and Starbucks Rewards members led our transaction and sales growth in the quarter. 
North America licensed revenues grew 2.6% in Q4, reflecting a third consecutive quarter of positive system-wide comps and strength across broader retail, travel and leisure. We ended the quarter with 18,176 coffeehouses in North America. This reflects 247 company-operated net closures primarily from last month's portfolio actions and partially offset by 52 net licensed openings.
Moving to International. The segment delivered Q4 net revenues of $1.3 billion and operating income of $261.3 million, with positive system-wide comps across our diversified portfolio. International company-operated comps, which are now largely comprised of Japan and the U.K. grew 0.9%. 
We had exceptional performance in the U.K., balanced by tougher comparisons in Japan. As a reminder, Starbucks China's retail operations are now deconsolidated from our financials and reported as a licensed business. With our 40% joint venture economics reported in income from equity investees. This transition will continue to be the driver of year-over-year changes in International through the first half of fiscal '27. 
International drove our unit growth in fiscal '26 ending Q4 with 23,431 coffeehouses, including 498 net new openings in the fourth quarter. This demonstrates our continued confidence in the long-term opportunity to grow our brand globally. 
In total, we ended fiscal '26 with 41,607 coffeehouses globally, with 617 net new openings for the full year, well ahead of our most recent expectations. In Channel Development, Q4 net revenues declined 8.9% to $494.4 million led by the Global Coffee Alliance and the absence of coffee price-related tailwinds we saw in the first 3 quarters.
Operating income was about flat year-over-year, despite the lower revenue base. With consumers remaining choiceful in their spending, we and our partners will continue to lean into innovation and marketing activations to maintain our #1 position in at-home and ready-to-drink coffee in North America and to build new occasions with offerings like Refreshers and protein.
Moving to margin. Q4 consolidated operating margin expanded 450 basis points to approximately 14%. This was our third consecutive quarter of margin expansion, with improvement across every segment. North America operating margin expanded 440 basis points to approximately 16%, driven primarily by sales leverage, disciplined execution and cost savings. We also lapped our Green Apron Service labor investments in August, which are now a part of our base. These benefits were partially offset by higher product and distribution costs mainly from product mix.
Coffee price impacts were roughly neutral in the quarter. Consolidated G&A declined approximately 20%, reflecting our cost savings efforts and China deconsolidation. Together, these results reflect stronger execution with more of our sales growth flowing to the bottom line. Interest and other income of $59.2 million benefited from net gains on certain investments in the fourth quarter.
And our effective tax rate was in line with our expectations at 24.7%. All in, fourth quarter EPS was $0.80, up approximately 54% year-over-year. Our fourth quarter and full year results showcase our focus on executing Back to Starbucks to strengthen the business and our earnings recovery is well underway. 
Turning to our outlook. In fiscal '27, we see multiple drivers of growth and a clear path to stronger earnings as we continue advancing our long-term priorities. As a reminder, fiscal '27 is a 53-week year. Our guidance includes the extra week, except for sales comps, which are on a comparable 52-week basis. 
Starting at the top of the P&L, we expect full year consolidated net revenues to decrease by approximately 1% year-over-year, including approximately $700 million of revenues related to the 53rd week. The expected decline is primarily driven by our International segment as we lap Starbucks China's retail operations, which were company operated in the first half of the year. 
Our revenue expectations also include modest coffee deflation and the impact of fewer new North America coffeehouse openings. We expect full year North America net revenue growth to slightly exceed comp growth driven by the impact of the 53rd week. During the first 3 quarters of the year, we expect North America net revenue growth will trail the segment's comp growth, reflecting the recent company-operated coffeehouse closures. 
In addition, we expect Channel Development net revenues to decline by approximately 10%, also heavily influenced by coffee price trends. In the U.S., consumers are increasingly prioritizing experiences that feel worth it. That reinforces our focus on quality, craft and connection and on delivering a consistently great customer experience.
We expect fiscal '27 North America comps to grow approximately 4%, led by beverage and food innovation, Green Apron Service, delivery and a small contribution from uplifts and sales transfer from coffeehouse closures. Any pricing will remain focused and well below CPI. 
We expect fiscal '27 cadence of U.S. comps to be more balanced across the quarters than fiscal '26. Specifically, we expect less variability between Q1 and the rest of the year. Also moving forward, we'll focus our annual comp guidance on our North America company-operated business. It is the primary driver of our underlying comp performance as our international portfolio is now predominantly licensed.
We expect fiscal '27 consolidated operating margin of 13.5% to 14%, up approximately 190 basis points at the midpoint. This is led by our North America business and supported by sales leverage and our focus on disciplined coffeehouse execution. In addition, we remain on track with our cost savings work which we expect to continue realizing through fiscal '28. 
And to date, we've realized roughly half of those gross savings, we expect benefits to operating margin to become more evident in fiscal '27 as we now have lapped our labor investments in Green Apron Service. In G&A, we continue to realize savings from actions we took last year and expect consolidated G&A dollars to be flat to slightly down year-over-year.
For international, we expect operating margin to begin the year at around 20% and improved slightly through the year, supported by sales leverage and our capital efficient licensed model. And in channel development, we expect operating margin to remain in the mid- to high 40% range over the longer term. 
For tax, we expect our effective tax rate will be roughly in line with or slightly below fiscal '26. Putting it all together, we expect EPS of $3.15 to $3.25, growing close to 18% year-over-year at the midpoint. Our guidance includes a benefit of slightly more than $0.10 related to the 53rd week. 
Finally, we expect approximately 1,200 net new coffeehouses globally in fiscal '27. International is expected to drive much of this growth at approximately 1,100 net new openings with China contributing about half. In North America, we expect 90 to 100 net new coffeehouses for the year, about half is expected to come from our licensed portfolio.
The balance is expected to come from our company-operated business as we rebuild the development pipeline Brian discussed. Fiscal '27 is an important step toward our fiscal '28 framework. We're tracking ahead of pace toward our 2028 goals and we remain focused on building from here. Our capital allocation priorities remain investing in the business with discipline, maintaining our investment-grade balance sheet and supporting a competitive dividend. We recently raised our quarterly dividend to $0.63 per share, our 16th consecutive annual increase. 
We also expect to deploy approximately $1 billion towards share repurchases, reflecting our confidence in the business and our plan. In fiscal '27, we expect capital expenditures to be approximately 5% of net revenues, primarily as we continue investing in uplifts and our Back to Starbucks priorities. 
To conclude, fiscal '26 demonstrated the meaningful progress we're making and gives us confidence in the path ahead. Back to Starbucks has moved us from turnaround to growth and our priorities are clear. We're focused on executing with discipline and delivering sustainable growth and long-term shareholder value. 
And with that, we are now ready to take your questions.

**Operator** (Operator):
[Operator Instructions].  And your first question comes from Brian Harbour with Morgan Stanley.

**Brian Harbour** (Analysts):
In guiding 4% same-store sales this year. I mean that is very specific. You had kind of the 3% plus algo. So should we think about that as being -- you essentially view this as an on-algo-year plus maybe some of the benefit from closures and uplifts that you stated. And I guess could you just comment on whether you're seeing something akin to that right now as we enter the fiscal first quarter.
And just, I guess, more broadly, what do you view as kind of the most important incremental layers as we go into this year?

**Brian Niccol** (Executives):
Yes. Look, thanks for the question. No, the way to think about it is our guidance for fiscal year '27 is really built on the strength of the fundamentals of the business, really driven by Green Apron Service, coupled with really strong rewards and digital program and then obviously the marketing menu innovation that we've got going on. 
So the way I look at it is we're probably a year ahead of schedule relative to the guidance we gave for fiscal year '28 and we do see strength in the business that gave us the confidence to commit to 4% comps. And obviously, I think our goal always is to continue to build on the strength that we have.
And the good news is that strength is coming through the fundamentals. I can't emphasize that enough. Hopefully, you heard that in my prepared remarks. The business is on really strong footing and it's driven by operational health.

**Operator** (Operator):
And your next question comes from Danilo Gargiulo with Bernstein.

**Danilo Gargiulo** (Analysts):
Great. I was wondering if you can comment on the evolution of margins in 2027. How should we think about the puts and takes? I heard you say expectations on deflationary coffee. And if you can also indulge us in maybe expanding on the $2 billion saving opportunities that you have identified in the past. So if you could give us some examples of incremental savings that you could be unlocking from here on, excluding the sales leverage that is coming with that. And congrats.

**Catherine Smith** (Executives):
Thanks, Danilo. And I appreciate the congrats. Thank you. So a little bit of color on 2027 margin. As we shared in the prepared remarks, it won't be quite as -- you won't see as much variation as you saw in '26. As you know, we had a lot of change moving through our P&L last year.
So going into 2027, it will be a little bit more balanced. I guess, all in, probably about a little bit better than 40% to 45% or so is in the first half, the remainder is in the back half. But it's fairly balanced throughout the course of the year. And then to really answer about savings, we're really pleased with our savings program. 
As we shared in the prepared remarks, we're over 50% of the $2 billion gross savings program achieved. And this year, more towards G&A, as we always shared, next would be OpEx and then cost of goods sold. Cost of goods sold is the one that we always said would be more into '27 and '28, and that's exactly what we're going to see as you're going to start to see it weight more there because of just the realities of getting new products online with new vendors.
Sometimes we have to let existing contracts finish. And so just getting that to pull through our business, the cost of goods sold start to show up in '27 and '28 more. But we're on track. We feel very, very good, still have a very robust pipeline. The team continues to add to that every day. And you're going to see a little bit more in cost of goods sold and then operating expenses. And then lastly would be G&A because you've seen the most of that this year. We'll have a little bit of benefit from the calendarization of the work we did this year.

**Brian Niccol** (Executives):
Yes. The only thing I would add to what Cathy said is, just if you remember at our Investor Day, we targeted the idea of 13.5% to 15% margins by fiscal year '28.  I think the fact that we are already believing we will achieve that low end of that guidance in fiscal year '27 speaks to, I think, the excellent work on the cost but also the fundamentals that are driving the top line and transactions.
So the fact that we're already hitting what we were guiding for '28 the low end in '27, I think, just speaks to the strength of the business and the operating discipline that we have on cost.

**Operator** (Operator):
Your next question comes from David Palmer with Evercore ISI.

**David Palmer** (Analysts):
I wanted to ask a question about the company unit growth in the United States, Americas. I think your comment was that net unit growth would be something south of 100, I think maybe closer to 40 to 50 this year. Could you speak to maybe the ramp that you see going into -- longer term going forward, I know there's capabilities that have to be added back. And if I could throw in one other thing, the technology test that you're talking about, it sounds like a lot of that is going to help the drive-thru and could you just give us a sense of timetable, if that works. And if it does work, what metrics you think that will affect sales or profitability and when that could hit?

**Brian Niccol** (Executives):
Yes. So I'll start on the first part of your question. Just in regard to new units in the U.S. specifically, we think it's going to be in that, call it, 100 net new range or a little below there. And that's really driven by the fact that we had to reset the pipeline. Obviously, we had to do some closures. But what I'm really excited about is how the pipeline is building for '28 and I think we showed you guys our prototype at Investor Day, and I'm happy to say that, that prototype is now up and running in a couple of markets.
And we're seeing great response both in the cost to build and then the way that our teams are able to operate. Our partners are providing great experiences for our customers. So the feedback on the new unit has been really positive. Obviously, it's early days on the performance, but they've all opened really well. 
And then as you look out into fiscal year '28, we want to get back into building new units north of 300 or so in the U.S. And we believe that is what gets us going towards that opportunity of 5,000 or more in North America. So lots of opportunity on the new unit side of things. It does take a little bit of time to reset the pipeline, but I believe we now have done all the hard work and now it's in the business of executing against the pipeline and getting the units built. 
On your question about drive-thru, we're just getting started in some of these ideas. And it will be exciting to see how these things test out. Once we have better understanding of the testing, our goal is, David, that will improve throughput and you know how this works. If you can improve throughput, a lot of good things happen from there, both on the top line and bottom line. 
So more to come, it'd be premature to get specific on this, but the whole rationale behind it is to give a better customer experience and also a better partner experience, which then results in more throughput that ultimately drives the top and bottom line.

**Operator** (Operator):
Your next question comes from Chris O'Cull with Baird.

**Christopher O'Cull** (Analysts):
Congrats to the team for the progress it's making. So I had a follow-up question about the North American margin. The profit flow-through was much better than we expected in the fourth quarter. Beyond higher sales, what were the biggest drivers of the leverage? 
And then looking ahead, what does guidance assume for the North American international operating margins next year? And are there any unusual items that could make the quarterly progression uneven?

**Catherine Smith** (Executives):
Thanks, Chris. So starting to Q4 2026's North America margin, as you just said, the biggest driver is always sales leverage. So the 7% comp we did in the U.S., that obviously helps a ton with the sales leverage. So that's the biggest driver of the margin expansion we saw. We also are rolling over our Green Apron Service investments we did last year, remember in August, mid-August time frame, so we get the benefit of rolling over those investments as well. 
And then a little bit of kind of a few other things. We had some pricing benefit, we had some supply chain savings come through, and all of that is helping with that margin expansion. I go back to where Brian was earlier, though, and it's all on the fundamentals. If you think about what we're doing to drive the durability of both the top line and the bottom line, it's -- everything we're talking about are going to help us to continue with that progress, which obviously then shows up in our guidance for this next year for fiscal '27.
Then maybe moving to fiscal '27. I'm going to knock on wood about onetimers or unusual things, I'm hoping not, we do know we've got some benefits of coffee should be helping us year-over-year. Obviously, we were a little bit higher in coffee prices this last year. It started to moderate throughout the course of the year. By the time it got to the fourth quarter, there was no impact. But that will help us with a little bit of a tailwind this next year. 
All of the fundamental work we've done around cost savings will continue to help. And the biggest driver of the profit this next year, again, will always be that comp guide that we just gave. That's always going to help with the leverage. So we're optimistic with the progress we're making, and that should be showing up in the guidance we just gave.

**Operator** (Operator):
Your next question comes from Sara Senatore with Bank of America.

**Sara Senatore** (Analysts):
Just, I guess, a question maybe about longer-term growth. Cathy, first, do you mind just sharing the benefits perhaps from sales transfer, store closures. Just trying to think about the balance between traffic and ticket over time. I think your check, obviously, a nice mix of attach and maybe a little bit of price. Next year, 4% comp, I think, would imply maybe less ticket, I'm assuming, a bit more of a balance with traffic. So just sort of the components there. 
And then I think, Brian, at one point, you had -- you've sort of -- it seems like you've kind of narrowed your expectations for how many stores the North America could support over time. Any changes or what has changed perhaps from maybe earlier commentary or maybe the number was a bit higher than the 5,000 you cited?

**Catherine Smith** (Executives):
Maybe I'll start, Sara. So I'll start with first Q4 comps to help break down the growth we saw. So as you said, you asked about store closures or transfers there. It's consistent with the previous quarter, about 200 basis points helped us there. Pricing and delivery were about half of the ticket, and then the attach and mix were the other half a ticket. So again, we had a 5.2% ticket in U.S. and that was about half pricing delivery and about half attach and mix. 
As we move into FY '27, we're going to weight a little bit more towards ticket than transaction as we continue to see the strength of all the work the team is doing in attach and mix. We continue to see really good progress both there and attach and mix. We'll see some price continue to come through. It will be below CPI. And then the remainder of that comp growth will be in transactions, continue to be led by our great operations.

**Brian Niccol** (Executives):
Yes. The only thing I would add to that is the thing that gives us a lot of confidence in kind of pushing the guidance up in '27 versus just a long-term guidance of 3% or better is the fact that we continue to have really good strength in transactions. So that's the foundational elements that are driving the business. 
And I think we've made great progress in food attach and mix, as Cathy mentioned. On your question around new units, the way I would describe it is we've got clear line of sight on the 5,000. Obviously, as we get closer down the road, I'm guessing there's going to be more upside to that number. 
But for now, we've kind of -- as we've done all the market planning, we feel really good about saying we see line of sight on the 5,000 additional units.

**Operator** (Operator):
Your next question comes from Andrew Charles with TD Cowen.

**Andrew Charles** (Analysts):
Just one quick clarification and then a question. Curious, what drive the expectation that 1Q in North America same-store sales to run pretty consistent with 2Q to 4Q, given that there's an easier comp in the first quarter? And my real question is, Brian, the proxy calls out a successful new platform launch in the U.S. by the end of the fiscal year. And I'm curious of the priorities laid out, what fits this criteria. You've spoken in the past about how you've won in the morning and the afternoon is going to be your bigger focus. So perhaps the revamped afternoon food platform is going to satisfy that criteria, but curious if you could expand some more on your thoughts.

**Catherine Smith** (Executives):
So I'll start, Andrew, on the cadence of our comp guidance throughout the course of the year. Yes, Q1 is the easiest lap if you just look at last year. But if you look at absolute transactions, we were actually fairly consistent through the year. One thing the team has done or a lot of work on is trying to take some of the seasonality out of our business. And so we have a strong product lineup that happens -- the cadence of it is less, in the past, we used to have, I think, a little bit more very distinct seasons. 
We've been trying to make sure that we smooth that out. You saw it a little bit last year, you'll see it a little bit more this year, but they worked really hard at pulling seasonality and then the other thing is, I just look at the absolute transaction volume per quarter, it's actually far more consistent throughout the year. And so that's what gives us the guidance that we did, which is fairly consistent through the year. Obviously, there'll be a little bit of variation.

**Brian Niccol** (Executives):
Yes. And then to your question of platforms, so like protein would be an example of the platform. Obviously, the Energy Refreshers is an example of a platform and then some of the work that we've done in -- on the food front, you'll be seeing some platforms roll out on the food side of things around our leveraging our bites business, moving that from just a morning idea to also an afternoon idea. 
And then there's still opportunities on health and wellness to go beyond just protein, so we feel really good about the initiatives we've got coming down the pike on, call it, platforms and then also the platforms that we've already gotten out the door. 
So you'll continue to see us have both, I would call, like, LTO ideas and then also platform ideas. And those working together are doing a nice job of driving transaction and sales.

**Operator** (Operator):
And your next question comes from John Ivankoe with JP Morgan Chase & Company.

**John Ivankoe** (Analysts):
I wanted to maybe talk about the implications of a 7-day a week delivery which I think is also going to have a 24-hour fulfillment if it doesn't already. So Brian or Cathy, can you talk about the implications specifically in the afternoon, but also the morning what that might mean for beverages, what might that mean for food, what that might mean to the grab-and-go case? In other words, how big of an unlock might we be just on the cusp of relative to the legacy Starbucks distribution platform into the stores back end?

**Brian Niccol** (Executives):
Yes. Look, it's a great question. And we do believe supply chain is going to be a nice advantage for us once we get the replenishment schedule there. We're getting closer on the daily deliveries. And we're going to continue to improve on the replenishment schedule. But yes, it helps in exactly those areas that you talked about. 
We'll kind of -- we have this mantra, we want to have the right product at the right place at the right time. And what this allows us to do is just that. Each of our coffeehouses behave differently on various elements of the business, whether it's food or beverage that's in the cold case that you can grab and go, whether it's the food platform that we heat up for people and give you that fresh food experience or the beverages that we make kind of by craft for everybody.
And to have the ability to get the daily deliveries within a signal for the replenishment within 24 hours is going to be a big advantage for us to make sure that we keep all of those things in stock at the right cadence for our customers and our partners to serve it. So we believe there's still a lot of upside to be had there, and the team is making great progress. We've made a lot of progress early on the daily deliveries, and we're going to be getting to the replenishment here in the next, call it, 6 to 12 months.

**Operator** (Operator):
Your next question comes from Lauren Silberman with Deutsche Bank.

**Lauren Silberman** (Analysts):
Congrats. So you guys have mentioned a couple of times that you're running ahead of schedule. I know approaching the low end of the fiscal '28 guide, what elements have been faster? Is it like sales, margins, cost savings, anything else that we don't necessarily see? And then can we interpret this as potential upside to fiscal '28 targets?

**Brian Niccol** (Executives):
Well, look, the good news is you kind of listed off all the things that are ahead of schedule, sales, margins and earnings. So that's why you see us guiding already to the low side of fiscal year '28. And look, the other thing I'd tell you is the guidance for fiscal year '28, I think we said this at Investor Day, it's just a point in time on our journey. Like we have no expectations that that's an end point. So our goal is, obviously, to always continue to figure how we grow the business smartly, and that's exactly what's happening. 
And we're doing it the right way through the fundamentals of operations and then obviously, surrounding it with, I think, the right innovation, whether it's digital, menu and then obviously, I think the creative solutions we're going to have in the asset, too. So I think we're hitting on all cylinders. And that's why you heard me say really Back to Starbucks as a strategy is switch gears from a turnaround plan to a growth plan. And I couldn't be more optimistic about where we're headed.

**Operator** (Operator):
And your next question comes from Sharon Zackfia with William Blair.

**Sharon Zackfia** (Analysts):
I'm curious whether you're seeing a continued correlation between the scorecard and individual unit comp performance. And if you look at those small percentage of locations that are comping negatively, is that typically related to scorecard deficiencies and things you can do operationally? Or are there more idiosyncratic issues?

**Brian Niccol** (Executives):
So yes, the good news is the Grow Scorecard continues to be a great indicator of performance. And I will tell you the stores that we're not comping, there are some idiosyncratic issues like the road is under construction or we might have been moving delivery around to make sure we allocate delivery to the right stores.
And then there are a handful of stores that we know we need to be operating better. Whether that means we need more stability in the team or we may have some issues with above store leadership. So there are opportunities. The good news is the scorecard gives us clear feedback. So we know where to spend our time on those stores. 
And I think our operators and Mike and the team are doing a great job of dialing that in going forward. So it's going to continue to be the tool that we use. Actually, just as an aside, I got a great e-mail just the other day from one of our coffeehouse leaders, her name is Maddie. She runs a store in Northern Idaho. She told me from when we started a Green Apron -- or I'm sorry, the Grow Scorecard with Green Apron Service, she was one of the stores that was like number 1,574. Her goal was to get into the top 5. 
She sent me an e-mail just this week to let me know that she's now #3 in the entire system. So of course, I had to call her and find out what she did. And you know what she told me? She focused on Green Apron Service, and she focused on that Grow Scorecard. And as a result, Mike and I are going to be heading out to go see her because I want to celebrate leadership like that. And we've got more of those stories every day at Starbucks. 
So it's a very powerful tool. It's a very effective tool, and it's also a tool that I think our coffeehouse leaders understand how to use and use it in a way that's very productive and enables them to lead correctly.

**Operator** (Operator):
Your next question comes from Jacob Aiken-Phillips with Melius Research.

**Jacob Aiken-Phillips** (Analysts):
So with CapEx at approximately 5% sales next year, development is expected to accelerate in the following year. How much of the spending is -- establishes capabilities that can kind of support the next phase of growth? And can the higher opening pace fit within the similar capital envelope or should we expect another step-up?

**Catherine Smith** (Executives):
Yes. So we're -- this next year, we're going to be -- as you would look at, I think when you see our full filings our CapEx was actually a lower percent of revenue this last year, really, I think, reflecting those -- the fewer new openings. 
As we move into this next year, we are ramping up our uplift. So we want to bring that great coffeehouse experience to more and more stores. As we said, we're going to continue to increase that. That's where some of the CapEx will go this next year and then obviously supporting the new store openings that we've communicated.
Going beyond that, though, into the following year, we still believe we should be in that 5% of revenue range, plus or minus, and we'll continue to use that as our guide. When you ask about what amount is going for new capabilities maybe for the future, it's actually fairly small. 
If you think about where our supply chain is, we don't need a lot of incremental capital, there's some, obviously, to continue to invest there, but it's not massive amounts traditionally our biggest capital goes into the support of our coffeehouses.

**Operator** (Operator):
Your next question comes from Jon Tower with Citi.

**Jon Tower** (Analysts):
Just curious, maybe, obviously, uplifts are a big part of the story or a bigger part of the story next year than they were in '26. Curious if you could kind of shed some light on what you're seeing with respect to absolute lifts on the stores so far. How it's actually showing up in the business? Are you seeing a nice balance between traffic and ticket? Or is one kind of over indexing?
And then just a second question, you'd mentioned the idea of being more asset light across the world outside of North America. So when thinking about the Japanese business, do you guys have any thoughts on if and when you do something with that and turn it into a license model?

**Brian Niccol** (Executives):
So -- well, I'll start with the first part of your question on the uplift. The uplift continue to do exactly what we want. It's brand building and it's transaction driving and it shows up in the total results for the business. So I'm really excited for the fact that we're going to get going and be able to do more than 2,000 in this coming fiscal year.
And so the feedback, and I don't know if you've had the opportunity to go into one of our coffeehouse that have gone through an uplift. But the feedback both from our partners and our customers is, this feels like Starbucks again, like thank you for bringing back my third place and so it does a lot for, I think, the brand. And then obviously, we love what we're seeing from the impact on transactions and then obviously, the total sales results. So that, by all accounts, is a winner for us, and we're going to keep driving that really hard. 
To your question on international, the thing I would tell you is we had another great year international. I think this is now 7 consecutive quarters of comp growth. If you exclude China, our revenue was up 5%. So really, the team did a tremendous job around the world, and I'm really excited about the growth opportunities that are in front of us. 
Specifically to Japan, I got to give the Japan team a lot of credit. They had another terrific year, and it's a really great business. And I think we've said this consistently. We always evaluate what is the right ownership strategy. And if and when the time comes where that should change, we'll share that with you. But I'm really proud of the way that the team delivered. And I'm really proud of how our international business is performing. And I'm really confident for the new unit growth that we've got coming down for this fiscal year and into the out years.

**Operator** (Operator):
And your next question comes from Peter Saleh with BTIG.

**Peter Saleh** (Analysts):
Congrats on the performance. I wanted to ask about the rewards program. You've had a couple of quarters now under your belt with the change in the rewards program. I know you mentioned 36 million active users. But can you give us a little bit more sense on how they're performing in terms of frequency, spend? Any more detail you can provide there would be great.

**Brian Niccol** (Executives):
Yes. Look, that is a one of those initiatives that continues to, I think, meet and exceed our expectations. The way we've done the new tiering with Green, Gold and Reserve, we're continuing to see people move up from Green to Gold and Gold to Reserve, and that's really driven by, first and foremost, frequency.
And then I think as we get better with our personalization, we're also going to see ticket continue to have an impact. But the early days, the first big moves we're seeing are in the frequency world. So not surprising, a lot of the new users that first come into Green start at a lower frequency level. 
And then as they spend more time in the program, we see their frequency levels increase. And then we see people moving up from Green to Gold and obviously, Gold to Reserve. So the program is working exactly the way we would hope. Customers are giving us feedback that they're enjoying the program. They love being able to redeem the stars at 60 stars for the $2 offer. 
And the team is doing a great job of figuring out how to take advantage of what is the next step in the evolution of that rewards program, which is going to be more around additional personalization.

**Operator** (Operator):
And your next question comes from Margaret May Binshtok with Wolfe Research.

**Margaret-May Binshtok** (Analysts):
Brian, I know you've talked about creating a second peak in the afternoon as a priority for fiscal '27. Can you talk a little bit about where the afternoon stands today perhaps versus a year ago? What you see the biggest drivers are from here on the afternoon? And any update on how Energy Refreshers have trended since you launched?

**Brian Niccol** (Executives):
Yes. Thanks for the question. This is something that I'm really excited about. We're kind of in the early days of a lot of our efforts. But one of the things that's been really great is with the upgrades that we've made to our food and our pastry case, the biggest place where we've seen an increase of attach has been in the afternoon, in the PM. So we've seen a nice little pickup in afternoon attach.
The refreshers program, the thing that's great is -- and we still have more work to do on this, but energy has actually skewed more towards the morning. But the fact now that you can get caffeine-free refreshers is driving some nice growth in the afternoon. And we've got some work coming down this fiscal year where you'll see us now highlight for people that there is a caffeine-free refresher program, which I think you're going to see play really well in the afternoon.
We also have some work around a tea platform where we're going to put some health and wellness into our teas, which I'm really excited about. And so we're making really great progress in the afternoon. TSDs are up versus a year ago. And I think you heard me say this in our earlier remarks, they're up all day and every daypart, but it's great to see that the morning is increasing, the afternoon is increasing and the initiatives that we've targeted to the afternoon are actually working the way we'd hope they would work.

**Catherine Smith** (Executives):
Maybe I'll just put a plug in as well for another favorite in the afternoon is our Matcha business and our Matcha platform. Our Matcha business is now over $1 billion platform, and it's growing tremendously year-over-year. What started as probably just a more simple Matcha beverage. We now -- almost everyone puts a cold foam on it, and it is sought after more often in the afternoon. So that's also been a great addition as we continue to evolve the Matcha business.

**Brian Niccol** (Executives):
Yes. Actually, as you mentioned, the other thing to think about too for the afternoon that's been great is our cold beverage innovation has really connected. And kind of to Cathy's point, those cold beverages, a lot of them have cold foam. So as we talk about the mix that we're seeing, the combination of customers moving to cold, which also results in usually a little bit bigger size.
And then the idea of modifying with cold foam, whether it's matcha, cold brew, iced coffee or iced Americanos, continues to see a really nice impact in the afternoon.

**Operator** (Operator):
And the last question comes from Brian Bittner with Oppenheimer & Co.

**Brian Bittner** (Analysts):
Question is now that the Green Apron Service investments really had been fully in the base for some time. Look, it clearly was the right strategy. That's obvious. But is there now potentially an opportunity, Brian, to go back and surgically reanalyze the footprint and potentially see if maybe there's pockets where you can find opportunities to perhaps get more efficient now that you've had time with all this learning? And if so, could this potentially be a lever for maybe additional operating leverage moving forward?

**Brian Niccol** (Executives):
Yes. Thanks for your question. And I couldn't agree more that the Green Apron Service labor investment was the absolute right thing for the business. The thing that's great to see is -- and I'm going to get a little technical with you here, but we've got right now a 3-hour peak in the morning. And the good news is the way we're seeing the business respond to being staffed deployed correctly in the morning, it's giving us confidence that, that 3-hour peak can actually become a 4-hour peak in the morning. 
And the reason why that's important is, obviously, we're earning our way into having additional labor to support more transactions at a peak type performance. And I think you're going to see the same thing happen in the afternoon. It will start out as an hour, and then we'll stretch it into 2 hours and then ideally, it will get to 3 hours. 
And if you look at Starbucks historically, way back when -- we actually had a 4-hour morning peak. So we are getting back to what we know we can do. And that is what I get excited about. And that's when you mentioned like getting surgical, that's what I think about getting surgical, which is driving and extending the peaks, so that we give customers better service and our partners are staffed and deployed to meet the demand that we know and see at those times of day. 
So we're going to continue to fine-tune it. But I really think we're fine-tuning it from the standpoint of driving more growth, more throughput and bigger peaks. So I think that was the last question?

**Operator** (Operator):
Yes, that was the last question. I'll turn it over to Brian Niccol for closing remarks.

**Brian Niccol** (Executives):
Okay. So look, thanks, everybody, for your time. I'd like to wrap up. And there's a couple of things I just want to leave you with. First, we had a terrific quarter and a great year, okay, because we got back to, I think, winning on the fundamentals. And as a result, our core business is stronger, we are ahead of schedule, and the improvements we've made are going to be lasting improvements because they're built on the fundamentals of the business.
The second thing is, Back to Starbucks, I mentioned this earlier, it started as a turnaround plan. It really is now our growth plan. We delivered 5 consecutive quarters of positive comps, 3 consecutive quarters of margin expansion. We're seeing the TSDs perform in the peaks, both in the morning, the afternoon and all day. So we're continuing to feel really confident in what our growth plan is all about.
And then the third thing is, I think it's really important as we look at fiscal year '27, we're focused on delivering consistent comp performance that's going to be driven by, I think, the fundamentals of the business with great innovation, both in menu, digital, and then obviously, across our assets. 
So we know when we get really good top line, we have the ability to expand the bottom line. And I think we demonstrated that as we closed out fiscal year '26. And I think that's what you're going to continue to see us do going forward. So we've got a clear strategy, really proud of our teams in every single coffeehouse. 
I think the Seattle Support Center is dialed in and focused on absolutely the right work. And we've got a growth plan that we're going to continue to execute and deliver durable results. So I'm super excited about what's ahead. 
The other thing I'll let you know too is, holiday kicks off next week. And I've got an insider's look at what our merchandising looks like for that, all the merchandise looks fabulous. I haven't been here that long, but I think it's the best I've ever seen. So I can't wait to get out in the stores next week. See the stores turn red, with the great holiday merchandise. And if you've never had a Tiramisu Latte, get ready to have a Tiramisu Latte from Starbucks because I think that's also fabulous. 
So hopefully, you can get out there, celebrate with your family and friends. I know I'll be out there celebrating with our partners as we launch holiday. So look forward to seeing everybody in a few months, and I'm sure we'll be talking soon. So thank you, and take care.

**Operator** (Operator):
This concludes Starbucks' Fourth Quarter and Full Fiscal Year 2026 Conference Call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SBUX_Q3_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：FY26 EPS 指引上調兩端至 $2.55–$2.65（原話："we are raising our EPS guidance at both ends of the range"）
- 2026-07-29｜CFO｜guidance：FY26 合併營業利益率指引上調至 >11%（原話："2026 consolidated margin guidance to greater than 11%."）
- 2026-07-29｜CFO｜guidance：FY26 合併營收預期持平至微增（原話："net revenues to be flat to slightly higher year-over-year"）
- 2026-07-29｜CFO｜guidance：Q4 美國同店成長預期 6.5% 或更好（原話："fourth quarter comp growth in the U.S. to be 6.5% or"）
- 2026-07-29｜CFO｜guidance：全年美國同店約略高於 6%（原話："U.S. comp growth of a little more than 6%"）
- 2026-07-29｜CFO｜guidance：Q4 有效稅率回到中 20% 區間（原話："returns to a more normal level in the mid-20s"）
- 2026-07-29｜CFO｜guidance：咖啡價格壓力 Q4 持續緩解（原話："we expect coffee price pressures to continue easing in Q4"）
- 2026-07-29｜CFO｜guidance：FY26 淨新增店數 600–650 不變（原話："approximately 600 to 650 net new"）
- 2026-07-29｜CFO｜guidance：北美可能出現關店，因對績效不佳門市有更深能見度（原話："we are gaining deeper visibility into some underperforming"）
- 2026-07-29｜CFO｜margin：Q3 關稅退款大致抵銷前三季關稅，管理層稱年初至今為較正常口徑（原話："The refunds we received in Q3 largely offset"）
- 2026-07-29｜CFO｜margin：Q3 產品與配送成本率之正常化參考為年初至今 32.3%（原話："the year-to-date metric of 32.3%"）
- 2026-07-29｜CFO｜margin：扣除關稅退款後北美利潤率仍成長逾 100 bp（原話："Q3 North America margin improved more than"）
- 2026-07-29｜CFO｜margin：Q3 合併 G&A 年減約 20%（原話："Consolidated G&A decreased by approximately 20% in the"）
- 2026-07-29｜CFO｜margin：7.9% 同店中約半數或略少來自關店、銷售轉移與外送（原話："about half of it or a little bit less"）
- 2026-07-29｜CFO｜margin：定價對客單成長貢獻不到 1 點（原話："Pricing contributed less than 1 point of ticket growth"）
- 2026-07-29｜CFO｜margin：Q3 中國營收 $53M，納入國際部門（原話："we reported $53 million of net revenues attributable to"）
- 2026-07-29｜CFO｜margin：管理層稱關稅退款已大致取得應得部分（原話："we've largely gotten the refunds we're entitled to"）
- 2026-07-29｜CEO｜margin：外送目前對利潤率無取捨（原話："there's no trade-off on margins"）
- 2026-07-29｜CFO｜commitment：$2B 成本節省計畫維持進度（原話："We remain on track with our $2 billion cost savings plan."）
- 2026-07-29｜CFO｜commitment：FY26 G&A 金額維持低於 FY23（原話："G&A dollars to run below fiscal 2023 levels"）
- 2026-07-29｜CEO｜commitment：門市 uplift 目標調升至 FY26 底至少 1,500 家（原話："completing at least 1,500 uplifts by fiscal year-end 2026"）
- 2026-07-29｜CEO｜commitment：FY27 uplift 將明顯加速（原話："meaningful step-up in '27"）
- 2026-07-29｜CEO｜commitment：管理層稱先拉營收、獲利隨後（原話："We said we would drive sales growth"）
- 2026-07-29｜CFO｜commitment：中國合資長期門市目標上看 20,000 家（原話："reach up to 20,000 coffeehouses over time"）
- 2026-07-29｜CFO｜capital_allocation：動用中國交易款償還約 $1.8B 債務（原話："repaid approximately $1.8 billion of our debt"）
- 2026-07-29｜CFO｜capital_allocation：uplift 平均單店投入約 $150,000（原話："a very low level of investment, as we've shared, $150,000 on"）
- 2026-07-29｜CEO｜capital_allocation：美國與國際新店組成可能演變，資源轉向 uplift（原話："the composition of U.S. and international new store growth"）
- 2026-07-29｜CEO｜capital_allocation：北美公司營新店淨成長 FY27 前可能偏低（原話："may remain modest through fiscal 2027"）
- 2026-07-29｜CEO｜capital_allocation：國際約 90% 已為授權結構（原話："about 90% of our international portfolio is"）
- 2026-07-29｜CEO｜capital_allocation：FY27 為科技系統現代化年（原話："fiscal 2027 will be an important"）
- 2026-07-29｜CEO｜capital_allocation：行銷費用約占營收 2% 多，不設上限（原話："we spend a little bit more than 2% of sales on marketing"）
- 2026-07-29｜CEO｜competition：Refreshers 定位：自稱原創者（原話："we're the original when it comes to refreshers"）
- 2026-07-29｜CEO｜competition：目標取得超過合理份額（原話："only our fair share, but more than our fair share."）
- 2026-07-29｜CEO｜competition：下午時段競爭升溫（原話："you see the competition really heating up in that space"）
- 2026-07-29｜CEO｜product：測試氣泡類飲品（原話："we'll begin testing sparkling beverages in select"）
- 2026-07-29｜CEO｜customer：90 天活躍會員 3,580 萬（原話："We now have 35.8 million 90-day active members in the U.S."）
- 2026-07-29｜CEO｜customer：成長涵蓋各世代與收入族群（原話："Sales growth in Q3 was broad-based across"）
- 2026-07-29｜CFO｜product：通路發展營收成長 22%，部分來自咖啡通膨（原話："helped by coffee inflation"）
- 2026-07-29｜CEO｜risk：美國消費者信心仍承壓（原話："the continued pressure on U.S. consumer sentiment"）
- 2026-07-29｜CFO｜risk：Q4 面臨去年同期客流基期與消費環境變動（原話："the continued variability in the broader consumer landscape"）
- 2026-07-29｜CFO｜risk：北美授權門市 Q3 淨關店 41 家（原話："41 net closures within our licensed portfolio"）
- 2026-07-29｜CEO｜risk：CEO 承認 2–3 年前開發策略不佳（原話："we did not have a great development strategy when"）
- 2026-07-29｜CEO｜product：24 小時重點在補貨而非門市營業，後者非目前焦點（原話："that's not a focus area"）
- 2026-07-29｜CEO｜product：下午時段仍有成長空間（原話："there still is a lot of room for growth"）

### SBUX_Analyst_Investor_Day_Starbucks_Corporation_20260129.md
- 2026-01-29｜CEO｜guidance：FY2028 目標：營業利益率區間與 EPS 區間（CEO 開場先給）（原話："between 13.5% and 15%, which means $3.35 to $4 in earnings"）
- 2026-01-29｜CEO｜guidance：FY2028 框架的前提：中國零售維持現況（原話："this framework assumes our China retail operations are a"）
- 2026-01-29｜CFO｜guidance：FY2026 全球可比銷售指引（原話："comparable sales to grow 3% or better, underpinned by a 3%"）
- 2026-01-29｜CFO｜guidance：FY2026 合併淨營收與可比銷售成長同步（原話："Our consolidated net revenues will be in line with our comp"）
- 2026-01-29｜CFO｜guidance：FY2026 營業利益率預期小幅改善，下半年起改善（原話："We expect consolidated operating margins to improve"）
- 2026-01-29｜CFO｜guidance：FY2026 EPS 指引區間（原話："$2.15 to $2.40 balances sustainable growth"）
- 2026-01-29｜CFO｜guidance：FY2027 起獲利成長快於營收（原話："Starting in fiscal 2027, earnings will outpace revenue"）
- 2026-01-29｜CFO｜guidance：中國改合資後 FY2028 EPS 約少 0.15 美元（現行指引未含）（原話："then the fiscal 2028 EPS would be approximately $0.15 less."）
- 2026-01-29｜CFO｜margin：中國合資對合併營業利益率的年化影響（CFO 數字口徑）（原話："it's about 40 basis points improvement in margin"）
- 2026-01-29｜CEO, Starbucks International｜margin：國際部門營業利益率預期因中國改授權而升至高十位數（原話："which we expect to climb to the high teens."）
- 2026-01-29｜CEO, Starbucks International｜margin：國際部門營業利益率 FY28 可能超過 20%（原話："exceed 20% by FY '28."）
- 2026-01-29｜CFO｜margin：FY2026 之後的利益率改善來源拆解：銷售槓桿與成本節省各半（原話："from equal part sales leverage and cost savings."）
- 2026-01-29｜CFO｜margin：目標性調價主要用來抵銷通膨（原話："pricing mostly to offset inflation."）
- 2026-01-29｜CFO｜margin：成本節省管線：90 項以上專案、分階段關卡（原話："current pipeline is comprised of over 90 initiatives"）
- 2026-01-29｜CEO｜margin：CEO 對成本節省規模的說法：約 20 億美元、2 年、其中 8 億較明確（原話："$2 billion over the next couple of years, 2 years, $800"）
- 2026-01-29｜CFO｜margin：CFO 更正節省規模與期間（20 億、2026–2028 三年）（原話："It's not $2 billion to $3 billion, $2 billion."）
- 2026-01-29｜CFO｜margin：CFO 更正節省期間為 2026、27、28 三年（原話："So it's 2026, '27 and '28. So think about it over the 3"）
- 2026-01-29｜CEO｜margin：CEO 稱成本節省與福利、薪資、勞動投資無關（原話："it doesn't really have anything to do with our benefits or"）
- 2026-01-29｜CFO｜margin：CFO 估計近期要 1% 至 2% 可比銷售才能覆蓋固定成本（原話："we probably need in that 1% to 2% comp range"）
- 2026-01-29｜CFO｜margin：CFO 稱公司歷史上每筆新增交易的流動率約 65%，目前尚未達到（原話："the company historically has seen around a 65-or-so"）
- 2026-01-29｜CEO｜margin：CEO 稱 2028 之後有能力回到 2019 年 17%–18% 利潤率（原話："2019, which is those 17%, 18% margins you're referencing."）
- 2026-01-29｜CFO｜commitment：CFO 對股東的財務承諾：穩定可比銷售成長（原話："consistent, reliable same-store sales growth year after year"）
- 2026-01-29｜CFO｜commitment：CFO 稱所有要素都在公司掌控內（原話："Every element is in our control."）
- 2026-01-29｜CEO｜commitment：CEO 稱進度超前（原話："Comps and transactions across our key markets are growing."）
- 2026-01-29｜CEO｜commitment：每日補貨目標：2026 曆年底前（原話："we're going to have daily replenishment by the end of"）
- 2026-01-29｜COO｜commitment：COO 供應鏈目標：美國 90% 門市每日補貨（原話："90% of our U.S. coffeehouses receiving daily replenishment."）
- 2026-01-29｜COO｜commitment：COO 的 Mastrena 3 推出時程與效益（原話："it will cut that 70 seconds in half"）
- 2026-01-29｜Global Chief Brand Officer｜commitment：忠誠計畫新版 3 月 10 日上線（原話："Our reimagined program, which launches on March 10"）
- 2026-01-29｜COO｜commitment：COO 承諾提拔零售領導職位（原話："commitment to promote 90% of retail leadership roles"）
- 2026-01-29｜CFO｜commitment：正式指引僅涵蓋至 FY2028（原話："we want to focus our formal guidance on the"）
- 2026-01-29｜CFO｜guidance：全球淨新增門市：FY2026 為 600–650 家，FY2028 逾 2,000 家（原話："accelerates from 600 to 650 in fiscal 2026 to"）
- 2026-01-29｜CFO｜guidance：FY2028 國際淨新增門市至少 1,500 家（原話："we expect international net new openings will be at least"）
- 2026-01-29｜CFO｜guidance：新店開發原則：單店建置成本降約 20%（原話："build cost by approximately 20%."）
- 2026-01-29｜CFO｜guidance：新店目標三年現金回收期（原話："yielding a 3-year cash-on-cash payback in the coming years."）
- 2026-01-29｜CFO｜capital_allocation：資本支出約占合併淨營收 5%（原話："our CapEx to be at a rate of about 5% on a consolidated net"）
- 2026-01-29｜CFO｜capital_allocation：近期優先降槓桿而非回購（原話："delevering our balance sheet over share repurchases"）
- 2026-01-29｜CFO｜capital_allocation：股利政策：逐步成長至約 50% 配息率（原話："time with measured increases until we reach approximately"）
- 2026-01-29｜CEO｜capital_allocation：美國店型：預期利潤率回到高水位後會想持有更多自營（原話："building, we're actually going to want to be owning."）
- 2026-01-29｜CEO｜capital_allocation：CEO 對日本、英國是否再授權：持續評估所有權結構（原話："we're always going to evaluate what the right ownership"）
- 2026-01-29｜CEO｜capital_allocation：國際策略定調為九成授權（原話："we're going to be 90% licensed."）
- 2026-01-29｜CEO, Starbucks International｜capital_allocation：中國 8,000 家門市由自營轉授權（原話："we're shifting our 8,000 coffeehouses from a"）
- 2026-01-29｜CEO, Starbucks International｜capital_allocation：國際授權比例由約 55% 升至 90%（原話："licensed to 90% licensed"）
- 2026-01-29｜CEO, Starbucks International｜capital_allocation：國際部門 pro forma 營收約 50 億美元（原約 80 億）（原話："approximately $5 billion. Yes, that's a little bit lower"）
- 2026-01-29｜COO｜capital_allocation：美國單店更新（Uplift）每店成本約 15 萬美元（原話："These uplift costs roughly $150,000, are completed mostly"）
- 2026-01-29｜COO｜capital_allocation：更新計畫進度與完成時間（原話："expect to surpass 1,000 by fiscal 2026 and finish the"）
- 2026-01-29｜COO｜capital_allocation：美國新店機會：看得到 5,000 家（原話："we see up to 5,000 new coffeehouse"）
- 2026-01-29｜COO｜capital_allocation：Green Apron Service 追加 5 億美元人力投資（原話："investing $500 million to ensure we have the right number"）
- 2026-01-29｜Global Chief Brand Officer｜customer：忠誠會員 90 天活躍數創高（原話："a new all-time high of over 35 million, 90-day active"）
- 2026-01-29｜Global Chief Brand Officer｜customer：Rewards 會員占美國自營營收近六成（原話："Rewards showed nearly 60% of U.S. company-operated revenue"）
- 2026-01-29｜Global Chief Brand Officer｜customer：新忠誠計畫的營收測算（原話："And we believe it has the power to deliver up to a"）
- 2026-01-29｜CEO｜customer：一季轉為交易量驅動的同店成長（原話："U.S., in every major market around the world, driven by"）
- 2026-01-29｜Global Chief Brand Officer｜customer：Rewards 與非 Rewards 交易量近 4 年首度同時成長（原話："we grew Rewards and non-rewards transactions for the first"）
- 2026-01-29｜Global Chief Brand Officer｜customer：消費者價格感受改善（原話："improvements in affordability perceptions driven by all age"）
- 2026-01-29｜CFO｜customer：CFO 稱可比銷售以交易量優先（原話："we always believe in transaction growth first"）
- 2026-01-29｜Global Chief Brand Officer｜customer：約三分之一消費者視星巴克為離家咖啡首選（原話："Starbucks is their first choice for coffee or tea away"）
- 2026-01-29｜CEO｜product：CEO 稱 2026 轉為進攻與創新（原話："we are shifting to playing offense and innovating."）
- 2026-01-29｜Global Chief Brand Officer｜product：能量 Refreshers 春季推出（原話："changing the game again with energy refreshers."）
- 2026-01-29｜CEO｜product：CEO 承認在能量飲品類別起步較晚（原話："we've been late to the game on some of these"）
- 2026-01-29｜Global Chief Brand Officer｜product：午後時段營收規模與第二高峰目標（原話："dayparts already generate $11 billion after 11:00 a.m."）
- 2026-01-29｜Global Chief Brand Officer｜product：創造午後第二高峰（原話："there's room to create a true second peak."）
- 2026-01-29｜COO｜product：Green Apron 試點店交易量領先（原話："650 pilot stores, pilot locations continue to outperform"）
- 2026-01-29｜COO｜product：尖峰服務時間不到 4 分鐘（原話："we achieved less than 4-minute"）
- 2026-01-29｜COO｜product：Grow 計畫：五星門市可比銷售為整體 3 倍（原話："5 Shot coffeehouses delivered 3x the same-store comp"）
- 2026-01-29｜COO｜competition：COO 稱完整體驗下競爭者難以撼動（原話："customers don't -- competitors do not move the needle."）
- 2026-01-29｜COO｜competition：COO 承認目前得來速並非最快（原話："in America. We do not today. It's good. It's competitive."）
- 2026-01-29｜CEO｜competition：CEO 稱約 1,000 個競品所在地點方圓一英里內沒有星巴克（原話："there's like 1,000 sites out there where there are"）
- 2026-01-29｜COO｜risk：COO 描述接手前的營運問題：決策過度集中（原話："too much centralized decision-making from Seattle"）
- 2026-01-29｜COO｜risk：COO 描述行動點單先前的問題（原話："orders created chaos instead of convenience."）
- 2026-01-29｜CEO｜risk：CEO 承認缺貨頻繁（原話："we were out of stock way too often."）
- 2026-01-29｜CFO｜risk：CFO 承認單一來源採購過多（原話："at our scale and maturity, we have too many of them."）
- 2026-01-29｜CFO｜risk：CFO 對中國合資後成長的保留說法（原話："But we don't want to get ahead of ourselves."）
- 2026-01-29｜CEO｜risk：中國年開店逾 1,000 家的時點（原話："It's not going to happen this year or next year,"）
- 2026-01-29｜CEO, Starbucks International｜risk：國際開店成長前緩後快（原話："Growth will be moderate through 2026, but it will then"）

### 問答異常語氣（迴避／改口／保留）
- SBUX_Q3_2026_Earnings_Call_20260729.md｜問：Bernstein：公司營與授權門市的同店與營運表現比較｜答法：Niccol 先確認問題後以定性回答（授權店也有好季、GROW 報告），未提供兩者數字差距
- SBUX_Q3_2026_Earnings_Call_20260729.md｜問：Wells Fargo：Q4 是否還有關稅退款、指引是否含入｜答法：Smith 未給 Q4 金額，改建議以年初至今口徑為錨，並稱已大致取得應得退款
- SBUX_Q3_2026_Earnings_Call_20260729.md｜問：JPMorgan：Green Apron 工時是否已到位、未來有無效率空間｜答法：Niccol 以營運者管理良好及成長空間回答，未給工時數字或方向
- SBUX_Analyst_Investor_Day_Starbucks_Corporation_20260129.md｜問：Eric Gonzalez：20–30 億節省是否多數流入獲利、與步調｜答法：CFO 先更正為 20 億、期間 2026–2028 三年，與 CEO 先前『2 年、其中 8 億』說法不同；對流入獲利比例只答『a little bit of both』，未給比例
- SBUX_Analyst_Investor_Day_Starbucks_Corporation_20260129.md｜問：Lauren Silberman：達成 3% 以上可比銷售能否到 EPS 高標｜答法：CEO 以『需要銷售與成本紀律』作答，未給槓桿數字
- SBUX_Analyst_Investor_Day_Starbucks_Corporation_20260129.md｜問：Dennis Geiger／Danilo Gargiulo：北美利潤率所需可比銷售門檻與邊際流動率｜答法：CFO 給 1%–2% 區間與歷史約 65% 流動率，稱『we're not there today』並請 6 個月後再問
- SBUX_Analyst_Investor_Day_Starbucks_Corporation_20260129.md｜問：Jeff Bernstein：2028 後 EPS 成長基準｜答法：CEO、CFO 皆只說獲利成長要快於營收，未給 2028 後 EPS 成長數字
- SBUX_Analyst_Investor_Day_Starbucks_Corporation_20260129.md｜問：Jacob Aiken-Phillips：利潤率擴張哪些部分有執行風險｜答法：CEO 以專案有負責人與期限、管線持續補充作答，未指出特定高風險部分
- SBUX_Analyst_Investor_Day_Starbucks_Corporation_20260129.md｜問：Andrew Charles：是否再授權日本、英國、加拿大及資金用途｜答法：CEO 稱『always going to evaluate』，未答資金用途與時程
- SBUX_Analyst_Investor_Day_Starbucks_Corporation_20260129.md｜問：Brian Bittner：3,550 萬會員在三層級的分布｜答法：Tressie 稱多數最佳客戶落在 Gold 與 Reserve，未給人數分布
- SBUX_Analyst_Investor_Day_Starbucks_Corporation_20260129.md｜問：未具名分析師：午後時段貢獻是否已含在 2028 展望，或屬上行｜答法：CEO 稱午後有『big incremental opportunity』，未回答是否已計入展望

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
{"date":"20260901","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"門市本體需求動能可持續（剝離關店移轉/外送/中國JV效應後，北美流量正且≥2.5%）","columns":{"2Y驗證點":"FY27美國comp≥+4%，門市本體≥+2.5%","5Y驗證點":"美國comp穩定+3%以上","10Y驗證點":"uplift全鋪設後生產力續升","具體數字門檻":"門市本體comp≥+2.5%連4季（Q3：總comp+7.9%、交易量+4.2pp）","信息來源":"Q3法說Cathy Smith：「約一半或略少於一半」來自關店/移轉/外送","漂移觸發條件":"連2季"}},{"id":"H2","text":"利潤率階梯可走完——非GAAP合併OM自FY25約10.2%走到FY26>11%、FY28 13.5-15%，sales leverage與$2B計畫「各半」貢獻真的落地","columns":{"2Y驗證點":"FY26>11.0%→FY27邁向12%+","5Y驗證點":"FY28 13.5-15%（Investor Day框架）","10Y驗證點":"邁向管理層長期願景17-18%（未正式guide）","具體數字門檻":"FY27全年OM≥12.0%；COGS率不YoY擴張>100bp","信息來源":"Investor Day財務框架＋Q2法說「一半top line、一半cost savings」","漂移觸發條件":"FY27全年OM"}},{"id":"H3","text":"倍數不下修到QSR水準——FY+2 Fwd P/E維持28-34x，正常化退坡至24-27x","columns":{"2Y驗證點":"Fwd P/E不連4季","5Y驗證點":"24-27x brand premium守住","10Y驗證點":"長期22-25x","具體數字門檻":"Fwd P/E不連4季","信息來源":"自算5年realized-NTM區間20.9x／32.1x／49.9x（§10.1）","漂移觸發條件":"共識EPS連4季下修+Fwd P/E"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"關店移轉順風退潮＋boycott實質流量損失——Q3 comp約一半來自關店/移轉/外送","columns":{"對應假設":"H1","時間尺度":"⚡短期","監測指標":"門市本體comp；boycott城市comp離散度","警戒閾值":"門市本體comp連2季"}},{"id":"R2","text":"SBWU全國合約鎖定永久性人力成本，boycott升高簽約壓力","columns":{"對應假設":"H2","時間尺度":"🔥中期","監測指標":"SBWU談判進度；boycott趨勢","警戒閾值":"合約鎖最低三人配置或$17底薪→opex+100-150bp"}},{"id":"R3","text":"Niccol依賴＋中國40%權益殘值折讓（JV僅運作3個月，Q3貢獻僅$5,300萬）","columns":{"對應假設":"H1+H2+H3","時間尺度":"🐢長期","監測指標":"Niccol/Smith留任；JV貢獻軌跡","警戒閾值":"Niccol離任（即時重跑）；JV貢獻連4季近零"}},{"id":"R4","text":"咖啡豆成本——ICE arabica庫存跌至26年低位，現貨~$3.40/lb，FY27對沖簿將重定價","columns":{"對應假設":"H2","時間尺度":"🔥中期","監測指標":"arabica現貨；COGS率","警戒閾值":"COGS率連2季YoY擴張>100bp；arabica連4週≥$3.60/lb"}},{"id":"R5","text":"相對QSR估值溢價擴大至+80.6%（前份+69%），復甦完成後收斂風險上升","columns":{"對應假設":"H3","時間尺度":"🐢長期","監測指標":"SBUX vs餐飲中位Fwd P/E差","警戒閾值":"溢價收斂50%至~40%→約$85"}},{"id":"R6","text":"GLP-1對含糖飲品與早餐時段的長期需求侵蝕（咖啡為受衝擊第二大品類，含糖飲料支出約−7%，高收入早餐客群占比高）","columns":{"對應假設":"H1","時間尺度":"🐢長期","監測指標":"含糖冷飲品項占比；早餐時段交易量YoY","警戒閾值":"兩指標連續下滑且無protein/低糖品項對沖跡象"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"starter 1/3·帽3%·加碼＝FY27 OM guidance（2026-10-29）≥12.5%或回檔至~$94（W52均線）；門市本體comp連2季<+2.5%則停止加碼","irr_base_pct":4.0,"ev5y_pct":10.3,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟠","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.05,"ev5y_pct":10.3,"irr_base_pct":4.0,"max_dd_pct":-60.0,"bull_5y_price":172.0,"bear_5y_price":54.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"starter 1/3·帽3%·加碼＝FY27 OM guidance（2026-10-29）≥12.5%或回檔至~$94（W52均線）；門市本體comp連2季<+2.5%則停止加碼","price_at_dd":106.25,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SBUX_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
