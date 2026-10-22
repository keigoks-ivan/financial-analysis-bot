你是 stock-analyst **v20 判斷 agent**，標的 NFLX（20261022）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"NFLX","date":"2026-10-22","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NFLX_20261022/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NFLX_20261022/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":12874.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"Netflix Q3'26 股東信／8-K Ex.99.1（Netflix IR 發布）"},"note":"未取得共識數；公司自家預測：營收略高於預測"},{"id":"f_kpi1_gaap","label":"GAAP 營業利益","value":4458.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"Netflix Q3'26 股東信／8-K Ex.99.1"},"note":"公司稱優於自家預測，主因費用認列時點（timing of expenses），非結構性"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益率","value":34.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"Netflix Q3'26 股東信／8-K Ex.99.1"},"note":"優於公司自家預測（費用時點）"},{"id":"f_kpi5_q4_2026","label":"管理層指引：Q4 2026","value":13442,"period":"Q3 2026 公告（2026-10-20）","unit":"USD million（營收，約 +12% YoY）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026 公告（2026-10-20）","citation":"Netflix Q3'26 股東信／8-K Ex.99.1"},"note":"未取得"},{"id":"f_kpi6_2026","label":"管理層指引：全年 2026","value":51100,"period":"Q3 2026 公告（2026-10-20）","unit":"USD million（營收點估計，+13% YoY）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026 公告（2026-10-20）","citation":"Netflix Q3'26 股東信／8-K Ex.99.1"},"note":"營收指引較前次區間中點低 0.2%"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-20","period":"2026-10-20","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-20"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_nflx_gross_margin_pct","label":"NFLX 毛利率","value":49.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NFLX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nflx_operating_margin_pct","label":"NFLX 營業利益率","value":29.68,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NFLX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nflx_fcf_margin_pct","label":"NFLX FCF 利潤率","value":23.06,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NFLX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_meta_gross_margin_pct","label":"META 毛利率","value":81.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_meta_operating_margin_pct","label":"META 營業利益率","value":38.08,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_meta_fcf_margin_pct","label":"META FCF 利潤率","value":17.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_googl_gross_margin_pct","label":"GOOGL 毛利率","value":60.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_googl_operating_margin_pct","label":"GOOGL 營業利益率","value":33.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_googl_fcf_margin_pct","label":"GOOGL FCF 利潤率","value":11.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pins_gross_margin_pct","label":"PINS 毛利率","value":79.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PINS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pins_operating_margin_pct","label":"PINS 營業利益率","value":6.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PINS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pins_fcf_margin_pct","label":"PINS FCF 利潤率","value":28.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PINS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_roku_gross_margin_pct","label":"ROKU 毛利率","value":45.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROKU.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_roku_operating_margin_pct","label":"ROKU 營業利益率","value":5.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROKU.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_roku_fcf_margin_pct","label":"ROKU FCF 利潤率","value":13.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROKU.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":2883.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"Netflix Q3'26 股東信／8-K Ex.99.1"},"note":"未取得"},{"id":"f_kpi4_sbc","label":"SBC 占營業利益","value":3.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"自算：SBC 133.7M ÷ GAAP 營業利益 4,458.6M（SBC 取自同份股東信）"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":65.04,"period":"2026-10-21（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-30.24,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":32.61,"period":"2026-10-21（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.28,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.58 → 3.59）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.8 → 3.8）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.56 → 4.56）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.59,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.8,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":4.56,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.56,"period":"2026-07-16 → 2026-10-21","unit":"%","basis":"FY1 共識 EPS 3.57 → 3.59（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":18.8,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.45,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝17.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":17.4,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.58,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝14.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":14.7,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":18.12,"period":"2026-10-21","unit":"x","basis":"分母＝FY1 EPS 3.59，分子＝快照價 65.04","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-21"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":6909.44,"period":"2026-10-22","unit":"USD m","basis":"yfinance 最新一季：總債務 15132.39、現金 8222.95（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":4163.94,"period":"2026-10-22","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":277732.08,"period":"2026-10-22","unit":"USD m","basis":"市值 270822.64 ＋ 淨負債 6909.44","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":51123.53,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（40 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":56665.35,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（45 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":5.43,"period":"2026-10-22","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-10-22","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 65.04 / W52 86.05 / W104 96.24 / W250 64.69 / W250 13週斜率 0.24%"},{"id":"f_ma_w52","label":"52 週均線","value":86.05,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":96.24,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":64.69,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.24,"period":"2026-10-22","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出競爭對手涵蓋線性電視、串流（含盜版）、遊戲、開放內容平台與社群媒體，並指新進入者可能以獨特服務進場。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm","excerpt":"New entrants may enter the market or existing providers may adjust their services with unique offerings or approaches to providing entertainment video.","as_of":"2026-01-23","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Nielsen Gauge（2026年8月報導）：Netflix 占美國電視觀看 7.9%，去年同期 8.3%；YouTube 13.5%（12.8%）、Prime Video 4.2%（3.6%）、Peacock 2.3%（1.5%）。","source":"MediaPost, Streaming Climbs To 48.5%, Per Last Lame Duck Edition Of Nielsen's 'Gauge'","url":"https://www.mediapost.com/publications/article/417308/streaming-climbs-to-485-finds-last-lame-duck-ed.html","excerpt":"The latest edition shows streaming platform YouTube rising to a 13.5% share (vs. 12.8% a year ago), and Prime Video climbing to 4.2% (vs. 3.6%); Roku Channel to 3.0% (from 2.5%); and Peacock to 2.3% from 1.5%. Netflix sank to 7.9% from 8.3%.","as_of":"2026-08-01","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"MoffettNathanson 預測 Netflix 2027 年廣告收入逾 60 億美元、2030 年近 100 億美元；廣告方案訂戶 2027 年 7650 萬","source":"MediaPost: Netflix To See Even Faster Ad Growth, To $6B In 2027: Analyst","url":"https://www.mediapost.com/publications/article/404240/netflix-to-see-even-faster-ad-growth-to-6b-in-20.html","excerpt":"Netflix could see even faster advertising growth than expected -- rising to $6 billion globally in 2027 and to nearly $10 billion in 2030, says MoffettNathanson Research.","as_of":"2025-10-01","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因素：2025 年 7 月美歐聯合聲明中，歐盟承諾不採行或維持網路使用費；但歐盟及其他司法管轄區仍有事實上義務的風險；2025 年 1 月美國聯邦上訴法院推翻 FCC 網路中立規則，規則不確定性可能影響公司成長。","source":"SEC EDGAR｜Netflix 10-K FY2025｜Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm","excerpt":"In July 2025, in an important joint statement with the United States, the EU committed not to adopt or maintain such network usage fees, although the risk of de facto obligations remains in the EU and in certain other jurisdictions.","as_of":"2026-01-23","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"DOJ 就 Netflix 收購 Warner Bros. 案發出民事調查要求，檢視 Clayton Act 第 7 條與 Sherman Act 第 2 條，並詢問 Netflix 對獨立製片與創作者的議價力。","source":"Bloomberg Law｜DOJ Probes Netflix's Power Over Filmmakers in Warner Deal Review","url":"https://news.bloomberglaw.com/antitrust/doj-probes-netflixs-power-over-filmmakers-in-warner-deal-review","excerpt":"is seeking to determine whether the deal “may substantially lessen competition or tend to create a monopoly in violation of Section 7 of the Clayton Act or Section 2 of the Sherman Act,” according to a copy of a civil investigative demand reviewed by Bloomberg News that was sent Friday.","as_of":"2026-02-21","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"倡議團體 Demand Progress 於 2026-07-07 發起「Netflix is a Monopoly」運動，要求 DOJ、FTC 調查（倡議，非官方行動）。","source":"MLex｜'Netflix is a Monopoly' campaign seeks US DOJ, FTC investigation","url":"https://www.mlex.com/mlex/amp/articles/2498138","excerpt":"'Netflix is a Monopoly' campaign seeks US DOJ, FTC investigation July 7, 2026, 5:39 PM GMT MLex Summary: Netflix's dominance of subscription video streaming merits an antitrust investigation, according to a campaign by advocacy group Demand Progress Education Fund that includes a \"Netflix is a Monopoly\" billboard...","as_of":"2026-07-07","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"川普於2025-09-29宣布對境外製作電影課100%關稅；法律依據不明，白宮稱尚未做最終決定；Netflix股價當日收跌1.9%。","source":"Reuters 經 Citizen Digital 轉載：Trump says US to impose 100% tariff on movies made outside the country","url":"https://citizen.digital/article/trump-says-us-to-impose-100-tariff-on-movies-made-outside-the-country-n370528","excerpt":null,"as_of":"2025-09-29","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Capstone DC 判斷 Section 232 調查是推動電影關稅最可能的途徑，但實務與法律障礙使政府難以落實；Netflix 列為受影響串流業者之一。","source":"Capstone DC: Trump's Movie Tariff Effort Faces Key Obstacles","url":"https://capstonedc.com/?p=50549","excerpt":null,"as_of":"2025-09-30","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Citigroup 估計最壞情境下電影關稅可使 Netflix EPS 約降20%","source":"Forbes Australia: Netflix stock dips as Trump wields 100% movie tariffs","url":"https://www.forbes.com.au/news/investing/netflix-stock-dips-as-trump-wields-100-movie-tariffs/","excerpt":null,"as_of":"2025-05-05","retrieved_at":"20261022","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Netflix FY2023 10-K 國際營運風險因子列有政治經濟不穩與全球敵對行動","source":"Netflix Form 10-K FY2023 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1065280/000106528024000030/nflx-20231231.htm","excerpt":null,"as_of":"2024-01-26","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Netflix Q3'26 區域營收：UCAN $5,628M 年增 11%（Q2'26 為 10%）；EMEA $4,107M 年增 11%（匯率中性 9%）；LATAM $1,603M（成長率未取得）；APAC 未取得。","source":"Netflix Form 8-K Q3 2026 shareholder letter (ex991_q326)","url":"https://www.sec.gov/Archives/edgar/data/0001065280/000106528026000290/ex991_q326.htm","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261022","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 年 3 月 Netflix 調漲美國全部方案：廣告方案 $7.99→$8.99、標準 $19.99、高級 $24.99→$26.99；TD Cowen 估 2026 年 UCAN ARM 年增約 6%；Netflix 2026 內容支出約 $20B（2025 為 $18B），2026 營收指引 $50.7–51.7B。","source":"Yahoo Finance / Reuters / CNBC 報導 Netflix raises US subscription prices","url":"https://finance.yahoo.com/markets/stocks/articles/netflix-raises-us-subscription-prices-131900704.html","excerpt":null,"as_of":"2026-03-26","retrieved_at":"20261022","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Omdia：2025 年底全球線上影音訂閱 22.4 億、年增 17.6%，預期 2026 年成長降至個位數；線上影音營收年增 13.5% 至 $1,760 億，付費電視營收年減 4% 至 $1,700 億（不含廣告）。","source":"senalnews, Omdia: online video subscriptions hit 2.24 billion, slowdown ahead in 2026","url":"https://senalnews.com/en/data/omdia-online-video-subscriptions-hit-224-billion-slowdown-ahead-in-2026","excerpt":null,"as_of":"2026-06-02","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Netflix 10-K 風險因素：娛樂影音有訂閱、廣告、盜版等多種模式可能搶走市場，且含生成式 AI 在內的新技術快速演進","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm","excerpt":"New entrants may enter the market or existing providers may adjust their services with unique offerings or approaches to providing entertainment video. In addition, new technological developments, including the development and use of generative AI, are rapidly evolving.","as_of":"2026-01-23","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"搜尋摘要：Netflix 成立 INKubator 生成式 AI 短內容動畫工作室，並推手機垂直影片動態，對標 YouTube／短影音平台","source":"Dataconomy / Interesting Engineering 報導","url":"https://dataconomy.com/2026/05/15/netflix-forms-ai-powered-studio-for-short-form-content/","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Netflix 廣告方案月活觀眾超過 2.5 億，並擴大直播體育（NFL 聖誕賽、WWE Raw 等）","source":"senalnews：Netflix nearly doubles 2026 upfront ad commitments","url":"https://senalnews.com/en/digital/netflix-nearly-doubles-2026-upfront-ad-commitments","excerpt":"The company continues to scale its advertising business following the announcement in May that its ad-supported tier surpassed 250 million monthly active viewers globally.","as_of":"2026-08-11","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Netflix 與法國 TF1 合作，2026 夏季起在自家 app 內提供 TF1 直播頻道與隨選內容","source":"NewscastStudio：Netflix to start offering France's TF1 linear feeds, on-demand content in 2026","url":"https://www.newscaststudio.com/2025/06/17/netflix-tf1-deal/","excerpt":null,"as_of":"2025-06-17","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"報導稱 Netflix 與 NBCUniversal、Fox early talks，考慮把 Peacock、Fox One 納入自家 app","source":"Sentisense：Netflix Explores New Streaming Store While Negotiating Fox and NBC Content Partnerships","url":"https://app.sentisense.ai/stories/netflix-explores-new-streaming-store-while-negotiating-fox-and-nbc-content-partn-08252026","excerpt":"Netflix Explores New Streaming Store While Negotiating Fox and NBC Content Partnerships SentiSense · Published Aug 25, 2026, 9:36 AM ET · Updated Aug 25, 2026, 5:37 PM ET Netflix is reportedly in early talks with NBCUniversal and Fox Corporation about bringing Peacock and Fox One into its own app, modeled on Amazon's Pr...","as_of":"2026-08-25","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Netflix 2026-07-16 Q3 指引（營收 $12.86B、EPS $0.82）低於市場共識（約 $13.0B／$0.84）；財報後股價開盤跌近 12%","source":"Capital.com Netflix stock forecast／Benzinga NFLX earnings（搜尋摘要）","url":"https://capital.com/en-gb/analysis/netflix-stock-forecast","excerpt":null,"as_of":"2026-07-16","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"FY2026 營業利益率指引 31.5%，比共識 32.7% 低 120bps（S&P Global 引述）；Q2 2026 營收 $12.56B 略低於共識 $12.58B，EPS $0.80 優於 $0.79","source":"S&P Global Market Intelligence, Netflix post-Q2 research","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/07/netflix-postq-slower-advertising-ramp-mask-profit-resilience-outlook-eases","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"FY2026 指引：2026-07-16 Q2 後營收 $51–51.4B（+13–14%）、營業利益率 31.5%、FCF 約 $12.5B；4 月 Q1 時維持 $50.7–51.7B 不變，未如市場期待上調","source":"Proactive Investors／TheWrap 報導（搜尋摘要）","url":"https://www.thewrap.com/industry-news/business/netflix-q1-2026-earnings-stock-reaction/","excerpt":null,"as_of":"2026-07-16","retrieved_at":"20261022","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價：2026-09-07 平均 $93.66；Benzinga 9 月 10 日 33 位分析師 27 Buy／6 Hold、共識目標 $103；6 月 TIKR 區間 $80–$151、均值 $114；Wolfe 8/25 升至 $95，Baird 7/22 降至 $90；BMO 街高 $135。各來源平均不一致","source":"247WallSt 2026-09-07／Benzinga NFLX price-targets／TIKR","url":"https://247wallst.com/investing/2026/09/07/netflix-has-momentum-despite-being-down-in-2026-one-analysts-price-target-implies-70-upside/","excerpt":null,"as_of":"2026-09-10","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"年初 Visible Alpha：2026 營收預估微升，營業利益預估下修近 3%、EPS 預估下修 3.7%（內容與廣告成本上升）","source":"S&P Global, Netflix post-earnings review Q4 2025 and outlook","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/01/netflix-post-earnings-review-q4-2025-and-outlook","excerpt":null,"as_of":"2026-01-25","retrieved_at":"20261022","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2025-12-04 Netflix 與 WBD 簽訂合併協議，收購 WBD 串流與影視工作室業務，每股 $27.75，股權價值約 $72.0B、企業價值約 $82.7B","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm","excerpt":"On December 4, 2025, we entered into a definitive agreement and plan of merger with WBD to acquire WBD's streaming and studios businesses, including its film and television studios, HBO Max and HBO","as_of":"2026-01-23","retrieved_at":"20261022","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-01-19 修訂合併協議，對價改為全現金 $27.75/股","source":"SEC EDGAR 8-K Item 1.01 (2026-01-20)","url":"https://www.sec.gov/Archives/edgar/data/1065280/000119312526015951/d37713d8k.htm","excerpt":"Netflix and WBD have agreed to revise the structure of their previously announced transaction to provide that the $27.75 per share merger consideration to be paid to WBD stockholders in the Merger (as defined below) will be paid entirely in cash, instead of a combination of cash and shares of Netflix common stock","as_of":"2026-01-20","retrieved_at":"20261022","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2025-12-19 簽 $5B 無擔保循環信貸，用於支付 WBD 交易現金對價與費用","source":"SEC EDGAR 8-K Item 1.01 (2025-12-22)","url":"https://www.sec.gov/Archives/edgar/data/1065280/000119312525327462/d82688d8k.htm","excerpt":"The Revolving Credit Agreement provides for a $5,000,000,000 unsecured revolving credit facility.","as_of":"2025-12-22","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"2026-02-27 8-K Item 1.02 終止重大協議；搜尋摘要顯示 WBD 終止 Netflix 合併協議改與 Paramount Skydance 簽約，Paramount 代付 $2.8B 終止費予 Netflix","source":"SEC EDGAR 8-K 清單；WBD 10-Q 搜尋摘要","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001065280&type=8-K","excerpt":"2026-02-27 8-K Items 1.02 Termination of a Material Definitive Agreement","as_of":"2026-02-27","retrieved_at":"20261022","affects":["valuation","thesis.H","triggers"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"+","claim":"Paramount 代 WBD 付 Netflix $2.8B 終止費","source":"WBD Form 10-Q FY2026 (Q2)","url":"https://www.sec.gov/Archives/edgar/data/0001437107/000143710726000075/wbd-20260630.htm","excerpt":"to the Netflix Merger Agreement, on February 27, 2026, in accordance with the terms of the Netflix Merger Agreement, the Company terminated the Netflix Merger Agreement in connection with entering into the PSKY Merger Agreement (as defined below). As a result of the termination of the Netflix Merger Agreement, PSKY, on behalf of the Company, paid Netflix a termination fee of $2.8 billion in","as_of":"2026-08-01","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2025-12-04 與 WBD 簽併購協議（約 $82.7B EV），2026-01 改全現金，2026-02-27 協議終止","source":"SEC EDGAR 8-K (2026-01-20)","url":"https://www.sec.gov/Archives/edgar/data/1065280/000119312526015951/d37713d8k.htm","excerpt":"will be paid entirely in cash, instead of a combination of cash and shares of Netflix common stock","as_of":"2026-01-20","retrieved_at":"20261022","affects":["valuation","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"NFLX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.12,"operating_margin_pct":29.68,"fcf_margin_pct":23.06,"rd_intensity_pct":7.67},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NFLX","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"META","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":81.75,"operating_margin_pct":38.08,"fcf_margin_pct":17.95,"rd_intensity_pct":31.38},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"GOOGL","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.9,"operating_margin_pct":33.11,"fcf_margin_pct":11.95,"rd_intensity_pct":15.47},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"PINS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":79.47,"operating_margin_pct":6.27,"fcf_margin_pct":28.11,"rd_intensity_pct":34.42},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PINS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ROKU","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.5,"operating_margin_pct":5.25,"fcf_margin_pct":13.63,"rd_intensity_pct":14.13},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROKU","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"NFLX"},"financial_history":{"ticker":"NFLX","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":31615550000.0,"revenue_yoy_pct":null,"gross_margin_pct":39.37,"operating_margin_pct":17.82,"net_income":4491924000.0,"diluted_eps":0.995,"free_cash_flow":1618528000.0,"fcf_margin_pct":5.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":33723297000.0,"revenue_yoy_pct":6.67,"gross_margin_pct":41.54,"operating_margin_pct":20.62,"net_income":5407990000.0,"diluted_eps":1.203,"free_cash_flow":6925749000.0,"fcf_margin_pct":20.54,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":39000966000.0,"revenue_yoy_pct":15.65,"gross_margin_pct":46.06,"operating_margin_pct":26.71,"net_income":8711631000.0,"diluted_eps":1.983,"free_cash_flow":6921826000.0,"fcf_margin_pct":17.75,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":45183036000.0,"revenue_yoy_pct":15.85,"gross_margin_pct":48.49,"operating_margin_pct":29.49,"net_income":10981201000.0,"diluted_eps":2.53,"free_cash_flow":9461053000.0,"fcf_margin_pct":20.94,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/NFLX/NFLX_Q3_2026_Earnings_Call_20261020.md）

# Q3 2026 Earnings Call
**Netflix, Inc.** | Earnings Calls | 2026-10-20

**Spencer Wang** (Executives):
Good afternoon, and welcome to the Netflix Q3 2026 Earnings Interview. I'm Spencer Wang, VP of Finance and Capital Markets. Joining me today are co-CEOs, Ted Sarandos and Greg Peters; and CFO, Spence Neumann. As a reminder, we will be taking forward-looking statements and actual results may vary. We'll now take questions submitted by the analyst community.

**Spencer Wang** (Executives):
Our first question comes from David Joyce of Seaport Research Partners. His question is: investors are looking for more clarity in what has typically been Netflix' industry-leading strategy. What role do live events or becoming a centralized streaming portal or offering short-form video, third-party or user-generated content play in how you see Netflix regaining a competitive edge that can help sentiment?

**Theodore Sarandos** (Executives):
I'll take that. And thank you, David, for the question. It gives us an opportunity to clarify, obviously. But our strategy is unchanged, and it's always been and it continues to be, to combine best-in-class entertainment with industry-leading discovery, global distribution and the best possible monetization. We want to be the must-have entertainment service, the first one members check for a great series or a great film and the last service they'd ever cancel.
Now the anchor of that strategy are the Netflix Originals, differentiated, exclusive, ambitious, professionally produced series and films and live events. Now we've oriented the market to expect something great and new to watch every week, so we have to deliver on quality and quantity always. And as for the live events, in a world of so much choice, we have titles like KPop and Wednesday and Bridgerton, and with all those things to choose from, live events like the Canelo-Crawford fight or the eventized sports that we do with the NFL and the MLB, these events break through. And they stand out. They drive new membership. They add fuel to our ad revenues. They please our existing members, and they just generally enhance the value of Netflix.
So we take all of that strategy, we pair that exclusive programming with kind of a broad offering of third-party programming, including second-run titles, deals we just did with Sony, Disney, Universal and others. And in addition to that, we look to new ways to bring third-party content onto the service as well to complement those originals, like we just did with TF1 in France, where you're ingesting a full network of programming.
Now all that said, it's really important to remember, roughly 95% of our spend and nearly all of our revenue is focused on that core, where we see a long runway for future growth. Now other areas that you mentioned, these are early-stage initiatives meant to explore future programming expansions, and we keep our focus and our investment in those areas very tight because the core is the critical growth engine.

**Spencer Wang** (Executives):
Great. Thank you, Ted. Our next question comes from Eric Sheridan of Goldman Sachs. How would you characterize recent engagement trends in the U.S. relative to other geographies? How would you frame any variables such as content, seasonality, competition, that might be driving any such divergences in engagement by region?

**Gregory Peters** (Executives):
I'll pick up this one and start with just overall engagement, which we think of as the sum total of actual value that we are delivering to members. So this is quality, quantity and variety of viewing. That remains healthy, and it drives our business model. And the best evidence that we've got that we're delivering that value is churn.
We've got healthy retention in every region. Q3 churn, both globally and in the United States, improved year-on-year. It was better than forecast. It's already industry leading. And the ultimate determinant are -- of are we delivering that value is the reaction to price changes. And those recent price changes that we did, including in the United States, have gone well. We've seen results that are consistent with past changes and our expectations. And consistent with all that performance, we do plan on delivering our full year guidance.
Now you talked about sort of specific engagement trends by geography, and as you saw from the letter, we had great results in APAC, Lat Am and EMEA. Our local titles from those regions are driving engagement and they're driving business growth. And you can see how our business model works here. We specifically highlighted India, which had a strong slate with a couple titles really, really performing. And as a result, view hours in Q3 in India grew 24% on an absolute basis. They were also up on a per member basis, all of which drives membership. It drove membership and nearly 20% year-over-year revenue growth. So that's a great example of how the core model works. We deliver on member value, and we get the business outcomes that we are looking for.
Turning to the U.S., the other region. Our engagement is solid, and it will allow us to continue to grow as we have for the last several years, but we know that we can do better. And that better is our upside. It's our goal to go from very good to great on the performance of that slate. But I just want to note that we are quite excited about what we've got coming. So coming from the U.S. in Q4, on series side, we're already off to a great start with limited series East of Eden. My whole social group is talking about that. We've got season 4 of The Diplomat, the best season yet of this show. Later this quarter, we've got The Body. We've got The Murder of JonBenét Ramsey. We've got the final season of Emily in Paris.
On the film side, we've got The Further Mis-Adventures of Cliff Booth with Brad Pitt, directed by David Fincher, written by Quentin Tarantino. You can't ask for a more star-studded lineup than that. We've got Bad Day with Cameron Diaz; and then we've got Steps, which is our new animated film featuring Ali Wong, Stephanie Hsu and Amanda Seyfried. In addition to all that, we've got our Christmas Day NFL games, and we'll now have the first Thanksgiving Eve game, which we are going to spice up with U2 as the halftime show. And U2 is just legendary, one of my favorites.
And then moving to 2027. Our slate includes Narnia. We've got Charlie and the Chocolate Factory (sic) [ Charlie vs. the Chocolate Factory ], Here Comes the Flood, Grown Ups 3, fifth season of Bridgerton, third season of Wednesday, Michael Fassbender starring in a new series about the Kennedys, God of the Woods, Rabbit, Rabbit just to name a few. We're going to have NFL games, one NFL game in the final week of the regular season. This is the first time we're doing that and of course, the Women's World Cup in the U.S. and Canada. So there is just a lot to look forward to.

**Spencer Wang** (Executives):
Thanks, Greg. That was an impressive overview of the slate in Q4, in 2027. I think you made Ted proud. But maybe to build on that, we do have a set of questions building off the theme of engagement to some of the executive changes. This next question comes from Rob Sanderson of Loop Capital. As Netflix is a massive and global content production operation, in what ways can a fresh perspective at the top influence the organization? What elements of success from his tenure at Disney are you most optimistic that Peter Rice can replicate at Netflix? Are there particular aspects you think the content org can perform better under new leadership?

**Theodore Sarandos** (Executives):
Rob, that's a great question. And first, let me start by taking this opportunity to thank Bela Bajaria for all of her incredible contributions to Netflix. Bela had an incredible decade-long run here. She put a lot of great hits on the board. She led the teams through a lot of expansions of new types of content. She also did the hard work of building this incredible international team who's been making local for local content around the world, which has become a great competitive differentiator for us over the last decade. So I just want to take that moment to thank Bela.
I'd also, calling back to that great list you just heard from Greg, there is a lot to be excited about, but I know that we could do better, and we want to build on that momentum. Now we've seen an opportunity to take our slate to the next level, especially in the U.S., where we can have an outsized impact when we create a big buzzy show that members love and talk about all over the world.
Now I'm incredibly thrilled to have Peter Rice joining as our new Chief Content Officer. Let me give you some history is I've known Peter for about 15 years, and I've got to tell you, the outpouring of excitement for -- about him coming to Netflix from across the industry and from the creative community has been nothing short of overwhelming. He's one of the really rare people in the industry who's led TV networks, movie studios, streaming services. His creative instinct and his business acumen are remarkable. He's really an at-scale, quality and volume operator, and he does it across every imaginable form of entertainment: network, prestige cable, streaming, theatrical and TV films and live sports.
So -- but most importantly, Rob, Peter Rice understands talent relations, and in a competitive market, creative talent have choices of where they want to work, and we want Netflix to always be the place that they love to do the best work of their life. Peter is the exact right person to lead those efforts in the U.S. and around the world. Now that's a key aspect of what I believe Peter can improve on looking forward.

**Spencer Wang** (Executives):
Thanks, Ted. We have a follow-up question that's on the same topic. This comes from Matt Condon of Citizens Bank. With Peter Rice stepping in as Chief Content Officer, what do you see as the biggest opportunities to evolve Netflix' content strategy under his leadership? Should we anticipate any meaningful changes in the types of content you prioritize, how you allocate content spending or your overall approach to driving engagement? Or is this more about improving execution within the existing strategy?

**Theodore Sarandos** (Executives):
Yes. Thanks, Matthew. Look, our business and our business flywheel are working. There is no need for a fundamental shift in the strategy. We do need better execution in the U.S. Our content around the world is largely working, as you heard a couple examples there from Greg. But we see titles across Latin America, EMEA, APAC driving engagement, subscriber growth, revenue and profit.
Now the U.S. is also working. It's just not growing as fast as it could or as fast as we'd like. So we had some really solid doubles and triples this year, but the other territories count on some of those titles being home runs so that they'll travel around the world. So we really have got to -- we're focusing on that execution.
And when we're talking about like success in APAC, India is a great example, but that success is also happening in Korea and Japan. And when you look to EMEA, we look to the Nordics, which is a very mature market for us, and that content slate is killing it there. And it's proof that when we have the right focus, make the right choices and deliver creatively, we can drive outsize impact on the business around the world.
Now Peter brings expertise in both art and commerce, television and film. It's kind of that exact balanced skill set that will help guide us through our next chapter. Now there's a ton to be excited about in our Q4 slate and a ton to be excited about in 2027. And I believe that Peter will actually be able to have an impact on that project -- those projects that are in the works, even in the short term. So we're very excited to have him join.

**Spencer Wang** (Executives):
Thanks, Ted. The next question comes from Dan Kurnos of StoneX. The question is: I wanted to touch on your recent head count reductions, which is the largest since 2022. He -- I recognize that you may not want to get into specifics, but how should we think about the thinking behind it?

**Gregory Peters** (Executives):
I can provide some color here. Go back to we've got a big and ambitious mission. We aspire to entertain literally the whole world. Now fulfilling on that big mission requires us to be incredibly disciplined about where we focus, where we invest, how our people work, where our resources go. And when you've driven considerable top line growth as we have over the last several years, and you're in a highly dynamic market that's constantly changing, I don't think it's unusual then to find that there are some areas that we built quickly and we ended up overinvested in or there are opportunities to adjust how we are operating to best drive the business through the next stage of growth.
Now we prefer to make these adjustments organically and iteratively. We -- that's the best way to do it. We think it's our mission basically to constantly be trying to tune and adjust. But sometimes the team needs a forcing function. The company needs a mandate that requires the whole organization to ask hard questions about where can we be more efficient, where can we make tough decisions about where we can trim or redirect how we're investing. We do not take these decisions lightly, but we also believe we have a responsibility to make hard trade-offs in service of our members, our partners, our employees, our investors, and ultimately our long-term growth. And that was the simple thinking behind it and what motivated these recent changes.

**Spencer Wang** (Executives):
Thanks, Greg. Building off of that, our next question comes from Doug Anmuth of JPMorgan. Can Netflix increase revenue growth at a double-digit pace in 2027? What are the key levers to get there? And is it sustainable?

**Spencer Neumann** (Executives):
Spencer, I'll take this one. Got to contribute a little bit to this call. So Doug, I appreciate the question. We're delivering strong growth in 2026 to start with, and that's because all 3 revenue levers that we have, they're working and they're contributing. That's member growth, pricing and ads. And we expect to deliver strong revenue growth into 2027 as well with those same 3 levers.
And we know there's questions about view hour growth. We've spoken about that. Greg and Ted talked about it just now. And to be clear, we want to grow view hours faster. We're not satisfied. We're working on it. But again, as both Greg and Ted articulated, that would be an accelerant to what is already underlying healthy revenue growth. We saw that in India. We just talked about that, strong slate, bump -- big bump in view hour growth, nearly 20% revenue growth, and that's just one of those multiple success stories across regions that Ted also mentioned. 
But even with modest view hour growth, the modest view hour growth that we're delivering, we're delivering that increasing value to our members across quality, quantity and variety of viewing with a steady drumbeat of big hits in most regions. And that's really the great thing about our model. It's that stability of our growth engine. We're not overly dependent on any kind of one title nor kind of outsized performance by any one region to deliver healthy growth.
So it's premature to issue full year 2027 guidance. We'll do that on our kind of next call or our Q4 call. But our financial objectives are unchanged. We look to sustain double-digit revenue growth. We look to expand margins, and we look to increase free cash flow.

**Spencer Wang** (Executives):
Thanks, Spence. The next question probably falls in your court as well. This one comes from Michael Morris of Guggenheim. The fourth quarter guidance includes about 120 basis points of cost tied to the head count reductions. What annual run rate savings do you expect? And how much of that should we assume is reinvested versus supporting operating margin expansion in 2027?

**Spencer Neumann** (Executives):
Well, I may disappoint again in terms of specific guidance. We're not going to specifically quantify the expense impact in 2027. But as we did note in our letter, that work, that hard work that Greg walked through, that prioritization ensures that we can continue to invest aggressively into the highest impact areas to improve our service, drive innovation, drive growth. So we're really focused on finishing this year strong. We'll provide 2027 guidance in January, including that margin guidance, but there's no change to our philosophy of obviously investing in our business to drive that growth in innovation and also steadily growing margin each year.

**Spencer Wang** (Executives):
Thanks, Spence. We have 2 questions that are somewhat related, so I'll bunch them together. The first version comes from Vikram Kesavabhotla of Baird. How has the integration with TF1 in France performed in its first few months? How has this experience impacted your perspective on distributing other services through Netflix? And what are the guidelines you are using to evaluate these types of partnerships going forward?
The related question comes from Matthew Condon of Citizens Bank. As you think about the evolution of the Netflix offering, what is your appetite for third-party content partnerships or add-on services that could be integrated into the Netflix experience? Do you see an opportunity to broaden the value of the platform through aggregation without necessarily owning or directly licensing all that content?

**Gregory Peters** (Executives):
Yes. Maybe to start with the answer to this one, just stepping back with a little context because I know these seem like new and novel techniques for us, or approaches, but they actually serve a goal that's been with us for as long -- going way back to when we started the streaming service. And that's been consistently expand the entertainment offering, provide more value to members. Our members consistently tell us that they want more from us. We see that in the preferences of how they use the service. So delivering on that desire over many, many years has been a goal, and I'd say it's been the primary driver of our industry-leading subscriber reach and retention.
So we are totally focused on that. We are always seeking new ways to expand our offering, new ways to provide more professionally produced film, TV, live events, more core entertainment value. And that means we do things like licensing. It also means like we look for new creative partnerships like we did with TF1.
And maybe one second on why partners are interested in working with us. We have broad distribution reach. We've got a top-of-class product experience, which is a good home for all the work that they do and the content that they create. We've got industry-leading monetization, and all of that makes us a great partner for studios, for networks, for creative talent. We can find new audiences. We can drive incremental revenue for them. That's why they want to partner with us.
So specifically to your question on TF1, we are very pleased with the early performance that we've seen in that integration. We have been able to enhance an already very compelling service for our French members with even more local popular French programming. We've seamlessly integrated the TF1 product experience in a way where it supports their brand, but it also keeps things distinct.
And we think this approach is advantageous for both them, supports their value proposition and us. It's good for the customer, too, because it signals what they're getting. And we are growing the TF1 viewing on our service every month. So we're constantly improving that product experience. We see a whole runway and line of improvement that we know we'll be able to fulfill from our previous history about being able to improve these things. 
Additionally, the early analysis and testing that we've done indicates that the TF1 engagement is incremental to our platform. So essentially, all things are working about that partnership. As for what to expect going forward, we certainly believe we can replicate similar positive results with other partners where this approach meets the needs of the partner as well. Those are opportunities that we're going to sequence, we'll prioritize with all the other growth opportunities we have. We have a lot going on that we're going after.
And then for the second question, add-on services, by which I believe that Matthew was asking about, which I think are like other subscription or hybrid ads subscription services that the customer could choose to add to their offering. Those would be yet another way to expand our entertainment offering. We think that the same core benefits to the partner, incremental reach, incremental monetization would apply in that model as well. We also think that there's much about the product experience that we built that works for -- that will work, that would work for that kind of service integration as well. So there's nothing to announce today, but you should expect that we are going to continue to find new ways to bring more core entertainment value to our members.

**Spencer Wang** (Executives):
Thanks, Greg. I'll follow up next with a couple questions on content from Sean Diffley of Morgan Stanley. Please discuss how you are approaching theatrical going forward. Believe you have released 30 movies in the box office. Excited for Cliff Booth with IMAX and Narnia next year. Do you see the potential to build more buzz by going to theaters first? Or is it very much a project-by-project decision? And what is the right amount of time with respect to the theatrical window?

**Theodore Sarandos** (Executives):
That's a great question. Great set of questions, I should say. But reminder, we are a streaming-first business. That is our core. But we consider every time we have a new film, the film itself, the audience for the film and the filmmaker when we're trying to come up with the release plan. And yes, we're going to release about 30 films theatrically this year, pretty much what we did last year. And each one of these have their own kind of bespoke release pattern.
So we start off by looking at the projects we have, asking ourselves, how do we best serve movie lovers, many of whom are our members, who want to see that movie in a theater and how do we do it without actually harming the view value to Netflix? So part of that is looking at specialty theatrical releasing. We've done that for the better part of a decade.
And at the other end of the spectrum are the big family movies that get a ton of rewatching as well as first-time streaming on Netflix. And we look at these 2 categories of film and treat them totally differently. So for specialty releases, we're doing a 47-day window platform theatrical release for La Bola Negra right now. It's this fantastic Spanish language film. And then we also upcoming have a theatrical release for Mosquito Bowl, a bit shorter. And we're partnering with IMAX to release the David Fincher film, The Further Adventures -- Mis-Adventures of Cliff Booth, worth repeating over and over again because it's so exciting for us, too. And in that one, we've done a deal with IMAX to put them on the biggest screens for a couple of weeks, 4 weeks before the Netflix release.
Now for those big family movies I talked about, we've already announced we have a 45-day window and a wide theatrical release for Greta Gerwig's new movie, Narnia: The Magician's Nephew; and for our animated feature, Charlie vs. the Chocolate Factory. Both films have big global IP and big global fandom. So we're very excited about how that will play out next year. So our theatrical strategy has evolved. It's evolved to include a traditional 45-day window for a handful of films, but the other one that's been important to folks is that we are also now reporting box office grosses for those releases when we do it. 
So that's new, and it looks like we picked a good title to start with, with La Bola Negra. We reported our first box office reporting this week for its opening weekend. It opened with more than $69,000 per screen average, which is the second highest per screen average ever for a non-English language film in the U.S., second only to Parasite, a film that went on to win the Oscar for Best Picture. So we're really excited about where we sit. Now of course, we have 1 week of public reporting of box office under our belt, and we're real happy about it, so let's check in again in about 6 months.

**Spencer Wang** (Executives):
Thanks, Ted. Sean also has a follow-up question. How would you describe the third-party licensing market? It seems the Disney deal for Ice Age and other content is a win-win and this follows renewing The Walking Dead and getting Power. How should we think about the mix of self-produced versus licensed content on a go-forward basis?

**Theodore Sarandos** (Executives):
Yes. Well, remember, original exclusive titles have always been the anchor of the service. We saw that value more than a decade ago when we got into the original production business. And it's why we continue to expand our original content investment across all different kinds of genres and all geographies.
But we're very happy to license second-run titles that complement our original exclusive offering. It's our broad distribution, our best-in-class technology. This makes us ideal partners for studios and networks and creative talent. As a result of those things, we have -- we continue to have strong access around the world to content.
I want to tell you about a -- those are great examples on The Walking Dead. That's an evergreen franchise with lots of episodes, and people love it. Power is a great show that was just under-distributed. And on Netflix, it will introduce a whole new wave of viewers to the Power universe. So that's really exciting.
But I really want to focus on 2 recent deals that we're very excited about. You mentioned the Disney deal we just launched in October. Now that deal brought all of the Ice Age films to Netflix, along with a bunch of other Disney films or Disney series and some upcoming films. And to your point, it is a win-win deal. And the reason it's a win-win deal is that we benefit by expanding the entertainment offering, for sure. Disney benefits from the revenue and from putting that content in front of our large global member base.
Now our members benefit, of course, because they get the addition of Disney content, and we already are seeing some of those benefits from the Ice Age movies. All 5 of them hit our top 10. That's really exciting. Now this benefits Disney because as they gear up to release their next Ice Age movie in the theaters in February, it's called Ice Age: The Boiling Point (sic) [ Ice Age: Boiling Point ], more people will be recent fans of the Ice Age franchise. And by the way, yes, Netflix just plugged a Disney movie on our earnings call. You're welcome, Josh.
Another deal to talk about is actually in Brazil. Last week, we and Globo announced our largest content license agreement between the 2 of us ever. Now this is the most meaningful licensing deal we've ever done in Brazil. We're excited to work with Globo. They are the leading series and film producer and distributor in that country. And they have also been a long holdout licensing content to us locally. We have, in the past, put a lot of Globo content on Netflix around Latin America and around the world, but just not in Brazil.
So we're excited to be -- this new stage of our business. We believe it's going to benefit both of us and our members in Brazil. It includes local titles from across all different genres. The Oscar-winning movie, I'm Still Here, is in there. The International Emmy-winning telenovela, India - A Love Story. And this deal spans a healthy mix of local, regional and global rights. So we're very excited about that, and this step forward with Globo in Brazil is a very exciting time in our existence together. 
Now the access to licensed content and which titles are available, this will always have some ebb and flow to it. But we expect to have opportunities throughout for the best series and the best films with all the suppliers. It's a little complicated because all of our suppliers are also our competitors. But our deals bring in much needed revenue. They certainly build awareness, and the benefit of that awareness transfers back to them because it helps grow the value of their IP. So these deals really are win-win. And as we sit here today, we're not really dependent on any single supplier, but we are thrilled to be in business with just about every supplier in the world.

**Spencer Wang** (Executives):
Thank you, Ted. I'll now move us on to the topic of advertising. We have several questions on advertising given the slight change in the outlook for this year. But we'll go with the question from Vikram Kesavabhotla of Baird. He asks, how is the advertising business progressing relative to your expectations this year? What are you observing with respect to the demand for your inventory and the breadth of advertisers on the platform? How are your recent technology investments influencing performance at this stage?

**Gregory Peters** (Executives):
So our ads business has delivered really impressive growth since we've launched, and we do see a long road of continued growth ahead of us. And then since that launch point, we've been committed to building an innovative advertising platform, a differentiated offering for our clients, bringing the best of digital advertising to the best of TV advertising, all while respecting our member privacy and ensuring that we also retain our first-party data advantage. So our integration models, our partner integration models, preserve that advantage while getting to the best targeting that we can.
We set big growth targets for our ads business this year. We established an aggressive product road map that was consistent with that strategy. And just note, I think that the build-out that we've been on is the fastest build-out of a comparable ad stack in our industry. But we are currently a bit behind our aggressive target for the year. We're still growing, just to set the context or put this in perspective. We're still growing our ads business over 80% this year. So excited about the rate that we're going on.
And I think noting that if you are sufficiently aggressive with your road map, you're going to occasionally be behind some milestones. And specifically, in this case, we've seen some delays in the rollout and partner integrations for some of those new ads products. So getting to the integration model that we want sometimes takes a bit more work with our partners, but we strongly believe that a modest short-term hit for a better long-term strategic position is a good ultimate trade-off. 
We also don't see this impacting our long-term gains. In fact, pushing for this barely achievable deliverables model tends to maximize our overall velocity. It's a strategy that we've used to good effect historically many, many times. We see the benefits when we continue to roll out other products like new ad formats, which help with our growth. So stepping back just to take a look, our priorities for this ad business are unchanged. We want to advance our full funnel optimization solutions. We want to deliver new ad formats, new ad products. 
We want to increase the availability of our first-party measurement and reporting. To the question specifically, general demand remains strong, breadth of advertisers continues to expand, and ultimately, advertisers want our new products and features, and that's a big mechanism of growth for us. So we are very focused on getting those out to them as quickly as we possibly can.

**Spencer Wang** (Executives):
Thanks, Greg. Another question on the advertising business. This is from Robert Fishman of MoffettNathanson. Ahead of launching ad tiers in 15 new countries next year, any update on the gap in average revenue per membership between the ad tier and the standard non-ad tier in the U.S. and other existing international markets?

**Gregory Peters** (Executives):
Yes. Super excited to do our first expansion of ads countries since we launched. But to answer the question, just start by noting that we manage the ads business for total revenue and growth. So we look at ARM and fill rates as a means to an end, not an end goal in and of itself. Now that said, there's still a gap between the combined ad tier ARM and then ARM for standard without ads. But that gap is narrowing, and that gap means under-realized revenue growth for us in the near term. It means we can -- it's an opportunity. We can improve our ads capabilities. We can close that gap over time.
And we've seen exactly that process happen over this last year. We've expanded demand sources. We continue to execute quickly on our own ad tech stack. We're adding more features, more ads products, more measurement. We're making it easier for folks to transact with us. All of those things drive demand. They drive competitiveness. Those yield increased fill rates. Those push ad ARM higher.
And of course, while we are doing that, we're also signing up more ads plan members. So that drives inventory up. That creates more room for us to grow into. So this dual growth phenomena where we're growing inventory and growing into our monetization on that inventory, I expect that that's going to persist for some time, likely with gradual closing of that ARM gap as we've seen because we're going to drive improved ad tech product, go-to-market capabilities, all which drive better unit performance and monetization for the next several years.

**Spencer Wang** (Executives):
Thanks, Greg. We'll take one last question. This one is from Sean Diffley of Morgan Stanley. What have you learned about churn and engagement following the most recent round of price increases compared with prior pricing cycles? As penetration increases in more mature markets, where do you see the largest remaining sources of membership and revenue growth? Is it pricing, advertising or international penetration, question mark?

**Gregory Peters** (Executives):
Okay. So on the first part of Sean's question, the price changes in '26 have gone well. So across all market types where we've done price changes, the member response, you mentioned churn engagement, engagement usually isn't really impacted by these things, but those -- that member response is consistent with prior price changes and our expectations. And again, we think that this is a strong indicator of the value that we're delivering to members as measured by the quality, the quantity, the variety of viewing that is healthy.
And maybe just one also, an external reference point for that value, take the U.S. as an example. Netflix subscribers are paying the least per hour of viewing compared to other SVOD offerings in the country. In some cases, they would have to pay more than double per hour for a competitive service. We think that that's a really good marker of how much value we are delivering per price. Also note that we saw continued healthy retention in every region, churn globally and the U.S. improved year-over-year, so better than forecast. Those are -- those things also reinforce the signs of that value and make us increasingly confident in that.
Okay. So to the second part of your question, we operate around the world, roughly 190 countries globally. These countries vary a lot. They vary by our penetration level there. They vary by market maturity, which means the presence of necessary or enabling market conditions. Think smart TVs, think good connectivity, payment methods, all the things that enable customers, consumers to sign up for our service and have a good experience. These countries vary also by whether we currently have an ads product. We're seeking to expand the number of countries there, but that's an important part of the mix. 
So as such, the drivers of business growth really have different weights across all those different countries and country types. So you can take our most mature markets, you think the U.S., U.K., Australia. We're more deeply penetrated, so our revenue growth drivers in those markets are going to skew towards ARM and advertising growth. And then in newer markets, think India, Indonesia, Colombia, we've got plenty of room to grow members. So we're going to continue to offer plans with accessible entry points. We expect member growth to be the most significant driver of overall revenue growth in those kinds of countries.
And then we got a lot of markets that are in the middle, where we believe we can get really a balanced combination of both member and ARM growth, and that includes ads countries like Mexico and Japan. We've got a lot more folks that we can sign up in those countries, and we can also deliver a lot more value into those -- to the offering in those countries, which drives ARM and ads monetization as well as countries without ads, like Philippines and Turkey, where the same -- both member growth and ARM growth opportunities, we believe, exist there as well.

**Spencer Wang** (Executives):
Thanks, Greg. And I want to thank everybody for joining us for our third quarter earnings call, and we look forward to speaking with you next quarter in January. Thanks.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NFLX_Q2_2026_Earnings_Call_20260716.md
- 2026-07-16｜Spencer Neumann｜guidance：CFO 重申 2026 全年營收成長指引為 13% 至 14%。（原話："13% to 14% top line growth for the full year"）
- 2026-07-16｜Spencer Neumann｜guidance：CFO 說明第三季指引為報價幣別成長 12%、匯率中性 11%。（原話："12% revenue growth in Q3 reported, 11% FX neutral"）
- 2026-07-16｜Spencer Neumann｜margin：CFO 以去年下半年權重較高解釋季間成長的波動，並稱公司以全年而非單季管理。（原話："a little bit of quarter-to-quarter choppiness in growth"）
- 2026-07-16｜Theodore Sarandos｜guidance：Ted 給出 2026 年內容費用預期成長約 10%。（原話："we're forecasting content expense up about 10% this year"）
- 2026-07-16｜Spencer Neumann｜customer：管理層稱全球可觸及家戶約 8 億戶。（原話："roughly 800 million addressable households"）
- 2026-07-16｜Gregory Peters｜margin：Greg 說明觀看時數與營收、利潤並非線性關係（數字口徑說明）。（原話："not a linear relationship between view hours and revenue"）
- 2026-07-16｜Gregory Peters｜product：Greg 給出直播佔內容預算與觀看時數的比重差異（預算 5%、時數 1%）。（原話："live, we expect will be 5% of our content budget this year"）
- 2026-07-16｜Gregory Peters｜customer：Greg 稱上半年觀看時數成長 2%，相較 2025 年的 1.5% 略為加快。（原話："slight acceleration compared to 1.5% growth in 2025"）
- 2026-07-16｜Gregory Peters｜margin：Greg 表示不揭露參與品質指標的細節，視為競爭優勢。（原話："We're not going to go into the details of that quality metrics"）
- 2026-07-16｜Theodore Sarandos｜product：Ted 稱第二季觀看整體無顯著變化，且今年第二季流失幅度略有改善。（原話："Our Season 2 falloff is actually slightly improved this year"）
- 2026-07-16｜Theodore Sarandos｜risk：Ted 承認大型直播帶來的訂戶可能有稍高的流失率，但稱符合模型預期。（原話："they can exhibit slightly higher churn"）
- 2026-07-16｜Theodore Sarandos｜commitment：Ted 表示會持續擴大全球直播賽事行事曆。（原話："build out that global live event calendar"）
- 2026-07-16｜Gregory Peters｜competition：Greg 稱對與 TF1 的整合表現滿意（合作僅約四週）。（原話："pleased with the performance we are seeing in that integration"）
- 2026-07-16｜Gregory Peters｜competition：Greg 稱免費方案在部分市場可能可行，並表示會持續考慮。（原話："free is something that we're going to continue to consider"）
- 2026-07-16｜Gregory Peters｜customer：Greg 確認正在多個國家測試針對新加入會員的免費試用。（原話："we're testing free trials for non-rejoining new members"）
- 2026-07-16｜Theodore Sarandos｜product：Ted 稱影音 podcast 的觀看是增量，且出現在非黃金時段。（原話："convinced us that this viewing is definitely incremental for us"）
- 2026-07-16｜Gregory Peters｜margin：Greg 稱廣告方案與無廣告標準方案的每會員營收差距正在縮小。（原話："that gap is narrowing"）
- 2026-07-16｜Gregory Peters｜customer：Greg 稱上半年美國、墨西哥、西班牙等市場的調價進展順利。（原話："markets like U.S., Mexico, Spain. They've gone well."）
- 2026-07-16｜Gregory Peters｜product：Greg 稱雲端遊戲月活躍玩家自去年 10 月以來成長 11 倍。（原話："monthly active players for cloud games have increased 11x"）
- 2026-07-16｜Gregory Peters｜capital_allocation：Greg 稱遊戲投資相對整體內容支出仍很小，會依表現調整。（原話："still very small relative to our overall content spend"）
- 2026-07-16｜Theodore Sarandos｜competition：Ted 稱產業整併已持續十年以上，公司專注於會員與健康成長。（原話："the industry has been consolidating for over 10"）
- 2026-07-16｜Theodore Sarandos｜product：Ted 稱生成式 AI 工作流程已用於約 300 部作品。（原話："gen AI workflows now have been used in roughly 300 of"）
- 2026-07-16｜Theodore Sarandos｜product：Ted 以《American Experiment》舉例，AI 強化片段製作速度與成本。（原話："produced twice as fast and at half the cost of previous options"）
- 2026-07-16｜Theodore Sarandos｜capital_allocation：Ted 稱 AI 省下的成本可能再投入更多內容。（原話："So the cost savings will likely be"）
- 2026-07-16｜Theodore Sarandos｜commitment：Ted 重申公司主要是建造者而非買家。（原話："we are primarily builders, not buyers"）
- 2026-07-16｜Theodore Sarandos｜commitment：Ted 稱進行大型併購的門檻很高。（原話："we have a very high bar to do any big M&A"）
- 2026-07-16｜Spencer Neumann｜capital_allocation：CFO 稱第二季買回 47 億美元股票，為單季歷史最大。（原話："we repurchased $4.7 billion of shares this"）

### 問答異常語氣（迴避／改口／保留）
- NFLX_Q2_2026_Earnings_Call_20260716.md｜問：參與度品質指標（Rob Sanderson）：哪些內部指標支撐「品質改善、時數軟化」的說法，成長放緩到何時會成為疑慮？｜答法：未回答疑慮門檻；表明不揭露品質指標細節，改談直播與動畫的時數差異及上半年時數 +2%。
- NFLX_Q2_2026_Earnings_Call_20260716.md｜問：AI 與 200 億美元現金內容預算（Sean Diffley）：成本節省會否降低預算，或再投入？｜答法：未給預算數字或方向，只說節省『可能再投入更多內容』，語氣為『likely』。
- NFLX_Q2_2026_Earnings_Call_20260716.md｜問：併購傳聞（Dan Kurnos）：Lionsgate、NBCUniversal 傳聞與大型併購的界線。｜答法：拒絕評論市場臆測，改重申資本配置原則與『builders, not buyers』。

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
{"date":"20260717","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"廣告＋定價雙引擎，在觀看時數僅 +2% 下仍撐住 11-13% 營收成長","columns":{"2Y 驗證點":"FY26 廣告約 $3B；FY27 營收 ≥+10%","5Y 驗證點":"FY30 廣告 ≥$8B；營收 CAGR ≥10%","10Y 驗證點":"營收 &gt;$90B","具體數字門檻":"FY26 廣告 ≥$2.6B（guide $3B）；廣告 CPM ≥$25（現約 $30，自 2022 上線的約 $65 下滑）；Q3'26 UCAN YoY ≥+9%","信息來源":"Netflix Q2'26 股東信（2026-07-16）；廣告產業 CPM 彙整（信心 med）","漂移觸發條件":"連 2 季 FX 中性營收 YoY &lt;+10% → 削弱；或 2 年期堆疊 YoY 跌破 27%（vs 2026 全年穩定約 29%）→ 基期歸因證偽"}},{"id":"H2","text":"營運槓桿把 OM 由 29.5% 推至 33%+（FY27），且不被體育版權通膨打斷","columns":{"2Y 驗證點":"FY26 OM 31.5%（7/16 已重申）；FY27 OM guide ≥33%","5Y 驗證點":"FY30 OM ≥35%","10Y 驗證點":"OM 穩定 35-38%","具體數字門檻":"FY26 OM 31.5%（明文重申）；增量 OM ≥45%（現 46.5-56.8%）；內容攤銷成長率 − 營收成長率 &lt;0（現 −3~−4pp）","信息來源":"Netflix Q2'26 股東信；本報告增量 OM 推導（§6.B③）","漂移觸發條件":"內容攤銷成長率 − 營收成長率 連 2 年 &gt;0 → 削弱"}},{"id":"H3","text":"市場不再進一步降檔——終端倍數守住 18x（成熟複利框架），不滑向 11-14x（成熟媒體框架）前份 H3「估值自 5Y 低檔 re-rate 至 23-25x」本次判定反轉，已自報酬引擎移除並改寫為此防禦型假設（§12.3）","columns":{"2Y 驗證點":"Fwd PE（FY+2）≥15x","5Y 驗證點":"FY31 終端 PE ≥18x","10Y 驗證點":"—","具體數字門檻":"Fwd PE（FY+2）≥15x（現 17.75x）；對照錨：Disney 約 17-18x 而 Netflix 的 ROIC 是它的約 3.7 倍","信息來源":"本報告 §11.4／§11.5；賣方目標價下修追蹤","漂移觸發條件":"Fwd PE（FY+2）連 2 季 &lt;15x 且 FY27 共識 EPS 未上修 → 降檔確認、H3 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"注意力份額結構性流失至 YouTube／短影音 — Netflix 佔美國電視觀看 9.0%（2026-01）→7.8%（2026-04），YouTube 12.7%→13.4% 連 11 個月居首、2026-04 領先第二名 4.0pp（該榜開辦以來最大）；Netflix 上半年觀看時數僅 +2%，而串流總份額創 47.6% 新高——餅在變大，Netflix 那塊沒有。攻擊者資本量級：YouTube 隸屬 Alphabet（市值約 Netflix 的 10 倍）且內容成本 ≈0。","columns":{"對應假設":"H1（傳導至定價力）＋H2（被迫加碼內容）","時間尺度":"🔥 中期（4-6 季）","監測指標":"Nielsen Media Distributor Gauge 之 Netflix 月份額","警戒閾值":"連 6 個月 &lt;8% → 護城河趨勢降 ↓＋停止加碼並減至 starter"}},{"id":"R2","text":"體育版權成本通膨打斷 OM 階梯 — 全球體育版權 2026 支出 $673.4 億（+9.6% YoY，S&amp;P Global）；FIFA 2030/34 美國轉播權傳出報價 $15-20 億 vs Fox 2026 屆 $4.85 億（CNBC, 2026-07）；NFL 2030 起重新競標、與世足爭同一批預算。Netflix 現階段直播僅佔內容支出「just over 5%」——一次得標就是 step change。","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"內容攤銷成長率 − 營收成長率（現 −3~−4pp）；體育標案結果","警戒閾值":"連 2 年 &gt;0 → H2 死；或單一體育合約 &gt;$15 億/屆 → 重算 §6.E"}},{"id":"R3","text":"廣告定向受監管限制壓縮 CPM — 德州檢察長 Ken Paxton 於 2026-05-11 對 Netflix 提告（未經適當同意違法蒐集用戶資料，含兒童）；另有廣告層隱私消費者集體訴訟。CPM 已自 2022 上線初期約 $65 降至約 $30（程序化 $20-30、直接 IO $45-65；第三方彙整，信心 med），主因供給擴張與 Prime Video 廣告開賣的競價壓力。","columns":{"對應假設":"H1（廣告腿）","時間尺度":"🐢 長期（2+ 年）","監測指標":"公司損益層閘（不預測監管結果）：FY 廣告營收 vs guide；第三方 CPM 追蹤","警戒閾值":"FY26 廣告 &lt;$2.6B，或 CPM &lt;$25 → H1 廣告腿削弱"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"starter 1%·帽 3%·加碼凍結至 Q3'26 財報（2026-10）；解凍條件＝UCAN YoY ≥+11%","irr_base_pct":12.5,"ev5y_pct":72.8,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟢","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":6.6,"ev5y_pct":72.8,"irr_base_pct":12.5,"max_dd_pct":-48.0,"bull_5y_price":180.4,"bear_5y_price":52.8,"p_bull_pct":25.0,"p_bear_pct":28.0,"rearm_trigger":"starter 1%·帽 3%·加碼凍結至 Q3'26 財報（2026-10）；解凍條件＝UCAN YoY ≥+11%","price_at_dd":67.97,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NFLX_20261022/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
