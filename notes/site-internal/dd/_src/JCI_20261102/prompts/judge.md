你是 stock-analyst **v20 判斷 agent**，標的 JCI（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"JCI","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JCI_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JCI_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":7113,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm"}},{"id":"f_kpi1_adjusted_ebit","label":"調整後營業利益（Adjusted EBIT）","value":1299,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm"}},{"id":"f_kpi2_segment_ebita","label":"調整後 Segment EBITA 利益率","value":20.6,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm"}},{"id":"f_kpi3_gaap_consolidated_ebit","label":"GAAP 營業利益（Consolidated EBIT）","value":1145,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm"}},{"id":"f_kpi6_eps","label":"調整後 EPS","value":1.66,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm"}},{"id":"f_kpi7_organic_orders_yoy","label":"訂單（Organic orders YoY）","value":44,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm"}},{"id":"f_kpi8_backlog","label":"Backlog","value":23.0,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm"}},{"id":"f_kpi9_q1_fy2027","label":"指引：Q1 FY2027","value":null,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm"},"needs_sonnet":true},{"id":"f_kpi10_fy2027","label":"指引：FY2027 全年","value":null,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm"},"needs_sonnet":true},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_jci_gross_margin_pct","label":"JCI 毛利率","value":36.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jci_operating_margin_pct","label":"JCI 營業利益率","value":14.45,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jci_fcf_margin_pct","label":"JCI FCF 利潤率","value":6.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tt_gross_margin_pct","label":"TT 毛利率","value":34.99,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tt_operating_margin_pct","label":"TT 營業利益率","value":17.92,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tt_fcf_margin_pct","label":"TT FCF 利潤率","value":16.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_carr_gross_margin_pct","label":"CARR 毛利率","value":24.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CARR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_carr_operating_margin_pct","label":"CARR 營業利益率","value":8.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CARR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_carr_fcf_margin_pct","label":"CARR FCF 利潤率","value":10.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CARR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lii_gross_margin_pct","label":"LII 毛利率","value":33.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LII.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lii_operating_margin_pct","label":"LII 營業利益率","value":19.94,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LII.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lii_fcf_margin_pct","label":"LII FCF 利潤率","value":15.34,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LII.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hon_gross_margin_pct","label":"HON 毛利率","value":38.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hon_operating_margin_pct","label":"HON 營業利益率","value":16.2,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hon_fcf_margin_pct","label":"HON FCF 利潤率","value":4.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_fcf","label":"自由現金流（FCF）","value":1078,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm"}},{"id":"f_kpi5_sbc_equity_based_compens","label":"SBC（equity-based compensation）","value":29,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":149.03,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":3.3,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":48.4,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.32 → 6.32）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.4 → 7.4）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.49 → 8.49）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":6.32,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":7.4,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":8.49,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":27.16,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 4.97 → 6.32（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":31.57,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.52,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.85,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":23.58,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 6.32，分子＝快照價 149.03","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.805,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":8659.0,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 9277.0、現金 618.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":605.74,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":98932.64,"period":"2026-11-02","unit":"USD m","basis":"市值 90273.64 ＋ 淨負債 8659.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":28330.51,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":30680.49,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.49,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 149.03 / W52 135.46 / W104 114.01 / W250 81.54 / W250 13週斜率 1.53%"},{"id":"f_ma_w52","label":"52 週均線","value":135.46,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":114.01,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":81.54,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.53,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"FY2025 10-K 列示主要對手（Honeywell、Siemens、Schneider、Carrier、Trane、Vertiv、API Group、Daikin），並指出數位服務、SaaS、IoT 領域有新創與新進入者競爭；稱失去任一合約或客戶不會有重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"Larger competitors include Honeywell International, Inc.; Siemens Smart Infrastructure, an operating group of Siemens AG; Schneider Electric SA; Carrier Global Corporation; Trane Technologies plc; Vertiv Holdings Co., API Group and Daikin Industries, Ltd.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子指出 AI 技術快速演進，若未跟上，競爭地位與經營結果可能受損。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"If we fail to keep pace with rapidly evolving technological developments in AI, our competitive position and business results may suffer.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"CSIMarket 稱 JCI 以營收計之整體市占改善至約 2.87%（營收代理指標，非產業份額）","source":"CSIMarket JCI Competitors","url":"https://csimarket.com/stocks/JCI-Competitors","excerpt":"sales growth, net income, profitability, valuation and market share, plus each peer's market capitalization, revenue, income and employees. Free below: the top 5 peers. Subscriber access adds the full competitor list and CSV downloads. Peer Data As of Q2 2026 Competitors 32 Named by the company Peer Group Market Share 2.87 %","as_of":"2026-07-31","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K：FY2023-2025 無單一客戶占合併淨銷售超過 10%","source":"JCI Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"In fiscal 2025, 2024 and 2023, no customer exceeded 10% of consolidated net sales. Geographic Areas Financial information relating to the Company’s operations by geographic area is as follows (in millions):","as_of":"2025-11-05","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"JCI 10-K（FY2024）揭露 FY2024/2023/2022 無單一客戶占合併淨銷售超過 10%；FY2025 該附註未在搜尋結果中確認","source":"SEC 10-K FY2024 jci-20240930.htm","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344424000064/jci-20240930.htm","excerpt":null,"as_of":"2024-11-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"JCI 截至 2026-06-30 10-Q：S&P BBB+、Moody's Baa1，展望皆穩定，遵守所有契約；搜尋未見 2026 年降評或下修指引（指引為上調）","source":"SEC 10-Q 期間 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000087/jci-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Carrier 2026 call: commercial HVAC, controls and aftermarket set up well for 2027; residential replacement unit demand expected to recover gradually toward ~9M from ~6.5M in 2026 (同業 Carrier，非 JCI)","source":"financialfilings.com Carrier Global call transcript 2026","url":"https://financialfilings.com/filings/carrier-global-corp/call-transcript/2026/48479265/","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"JCI FY2026 Q4: backlog $17.8B up 54% YoY (organic/FX-adjusted), driven by sustained data center demand","source":"JCI Q4 FY26 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm","excerpt":"Excluding acquisitions and divestitures and adjusted for foreign currency, orders increased 58% year-over-year and backlog of $17.8 billion increased 54% year-over-year. The increase in orders and backlog was supported by sustained demand for data centers and our differentiated technology and capabilities.","as_of":"2026-11-01","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"JCI expects data centers to become about one-third of its business over next 3-5 years, from high teens % of FY2026 sales","source":"Webull news: Johnson Controls Sees Data Centers Becoming One-Third Of Its Business","url":"https://www.webull.com/news/15311425061086208","excerpt":"Johnson Controls Sees Data Centers Becoming One-Third Of Its Business Benzinga · 07/29 16:01","as_of":"2026-09-01","retrieved_at":"20261102","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3 列示的訴訟為 Gumm v. Molinaroli（2016 年 Tyco 合併股東集體訴訟），2025-03-28 遭法院全案駁回，原告已上訴；Item 3 未列反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"On March 28, 2025, the Court dismissed the complaint in its entirety. Plaintiffs have appealed the decision, though the timing of the decision by the court is currently unknown.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因素提到跨國營運受反壟斷、出口管制、關稅等複雜法規約束，並稱無法保證持續被認定合規。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"No assurances can be made that we will continue to be found to be operating in compliance with, or be able to detect violations of, any such laws or regulations.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"香港競爭事務委員會對 Johnson Controls Hong Kong、其母公司及一名前員工提起第二宗競爭審裁處程序，指控 2015-12 至 2018-06 空調工程定價、分割市場及圍標，違反第一行為守則，涉案工程逾 HK$3 billion。","source":"The Standard (HK) - Poon company in hot water again over alleged cartel","url":"https://www.thestandard.com.hk/section-news/section/11/252737/Poon-company-in-hot-water-again-over-alleged-cartel","excerpt":"The Competition Commission has commenced another set of proceedings against a company owned by Otto Poon Lok-to, husband of former secretary for justice Teresa Cheng Yeuk-wah, for alleged price-fixing, market-sharing and bid-rigging.","as_of":"2023-05-24","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K：關稅與對等關稅推升原物料成本，公司至今大致能抵銷已實施關稅的影響；若新增關稅，可能因銷量下降與銷貨成本上升而衝擊營收成長與利潤率。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"Although the Company has been largely able to mitigate the impact of tariffs that have been enacted to date, if additional tariffs and reciprocal tariffs are implemented (whether as currently proposed or otherwise), such actions could negatively impact the Company's revenue growth and margins in future periods through decreased sales and increased cost of goods sold","as_of":"2025-11-14","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2025 10-K MD&A：公司以區域製造、本地採購、加速漲價與變更單主張合約權利等方式緩解關稅，但未來成效不確定。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"The Company is taking actions to mitigate the actual and anticipated impact of these events, including strengthening the Company's in region, for region manufacturing strategy, pivoting to local sourcing in its supply chain, accelerating pricing actions and asserting contractual rights through change orders.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2025 10-K風險因素：公司受美國BIS出口管制、OFAC等法規約束，並不保證持續合規。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"the system of laws and regulations to which we are subject is complex and includes regulations issued by the U.S. Customs and Border Protection, the U.S. Department of Commerce's Bureau of Industry and Security, the U.S. Treasury Department's Office of Foreign Assets Control","as_of":"2025-11-14","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2026 Q2 10-Q（截至2026-03-31）：公司稱已實施關稅對財務表現無重大影響，並正評估IEEPA關稅退款程序（搜尋摘要轉述，未取得原文）。","source":"SEC EDGAR 10-Q 2026-03-31","url":"https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000050/jci-20260331.htm","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261102","affects":["valuation","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"JCI 2026年3月季報稱其強化「區域內生產供應區域內」製造策略並轉向在地採購；關稅已大致可抵銷、尚無重大財務影響；中東衝突擾動能源與供應鏈。","source":"JCI Form 10-Q (period ended 2026-03-31), SEC","url":"https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000050/jci-20260331.htm","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"JCI 10-K風險因素：關鍵零件（半導體、含稀土零件）來自單一或少數供應商，另有關稅涵蓋中國、墨西哥等","source":"JCI Form 10-K FY2025, SEC","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"We use a wide range of materials (primarily steel, copper and aluminum) and components (including semiconductors, electronic components, and components utilizing rare earth minerals) in the global production of our products, which come from numerous suppliers around the world.","as_of":"2025-11-05","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q4 FY26: total sales +10% to $7.1B, organic +12%; Americas $4,930M +14% (organic +14%); EMEA $1,312M -2% (organic +3%); APAC $871M +12%; backlog $23B up 43% organically; orders +44% organic, Americas orders +58%; Q1 FY27 guide organic sales +12% to 14%","source":"Johnson Controls Q4 FY26 earnings release (SEC 8-K exhibit 99.1)","url":"https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm","excerpt":"Americas EMEA APAC Total Net sales - 2025 $ 4,325 $ 1,337 $ 780 $ 6,442 Base year adjustments Divestitures and other — (42) (13) (55) Foreign currency (2) (16) 7 (11)","as_of":"2026-10-30","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 FY26 call: organic orders +27%, backlog $21.0B (+32% organic), Americas orders +37%, Applied HVAC growth high-teens driven by data centers; data centers expected high-teens % of FY26 sales","source":"MarketBeat, JCI Q3 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/johnson-controls-international-q3-earnings-call-highlights-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Mixed demand outside data centers and concern about durability of data-center cooling boom and new competitors","source":"Nasdaq, JCI Q3 earnings call highlights","url":"https://www.nasdaq.com/articles/johnson-controls-international-q3-earnings-call-highlights","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"JCI 10-K 風險因子：若無法敏捷回應新產品/技術（能效、液冷、AI/ML）的顛覆，業務與財務可能受不利影響","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"If we are unable to be agile and responsive to disruption in the development of new products, services and technologies, including capabilities such as energy efficiency, cooling technology (including liquid 11 cooling), artificial intelligence and machine learning, our business, financial condition, results of operations and cash flows could be adversely affected.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Nvidia CEO 於 2026 年 1 月稱次世代晶片可能大幅降低資料中心冷卻需求；資料中心占 JCI 銷售比重有限","source":"Webull news","url":"https://www.webull.com/news/15378059250328576","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：JCI 商用 HVAC、控制、保全、消防設備與系統主要經由全球直銷通路銷售，另有第三方經銷商通路貢獻大量銷售；10-K 未描述通路結構性轉變。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"The Company sells and installs its commercial HVAC equipment and systems, control systems, security systems, fire-detection and fire suppression systems, equipment and services primarily through its extensive direct channel, consisting of a global 4 network of sales and service offices. Significant sales are also generated through global third-party channels, such as distributors of air-conditioning, controls, security and fire-detection and suppression products.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"DEF 14A 提及新董事長/CEO 分離與以 80/20、Lean 建立新營運系統（非通路轉型，僅營運方向）","source":"SEC DEF 14A FY2026","url":"https://www.sec.gov/Archives/edgar/data/833444/000110465926004565/tm2524665-5_def14a.htm","excerpt":"At the same time, the Company is developing and implementing its new proprietary business system — rooted in proven methodologies like 80/20 and Lean, and augmented with the promise of digitization and artificial intelligence.","as_of":"2026-01-01","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY2026 調整後 EPS 指引於 Q3（2026-07-29）由約 $4.85 上調至約 $5.05，有機成長由約 6% 上調至約 8%（Q2 時已由約 $4.70 上調至 $4.85）；上調主因為資料中心與關鍵任務設施需求。","source":"Security Systems News / SentiSense：Johnson Controls raises FY2026 guidance following strong third quarter performance","url":"https://www.securitysystemsnews.com/article/johnson-controls-raises-fy2026-guidance-following-strong-third-quarter-performance","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q4 FY26 調整後 EPS $1.66，高於公司指引約 $1.55 與共識 $1.52；單一二手來源稱全年 FY26 調整後 EPS $5.16（高於 $5.05 指引，未對照 Q4 財報原文）。","source":"SEC 8-K Q4 FY26 earnings release / Earnings Whispers","url":"https://www.earningswhispers.com/article/JCI/r413","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY2027 指引：有機成長 11%–12%、調整後 EPS $6.15–$6.30；Goldesel 標題稱 FY27 EPS 展望顯著高於市場共識（摘要未給共識數字）。","source":"Earnings Whispers；Goldesel：FY27-EPS-Ausblick liegt deutlich über Konsens","url":"https://goldesel.de/aktien/news/johnson-controls-international-aktie-fy27-eps-ausblick-liegt-deutlich-uber-konsens","excerpt":"FY27-EPS-Ausblick liegt deutlich über Konsens","as_of":"2026-11-02","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價分布（各聚合站日期不一）：StockAnalysis 約 20 位分析師共識 Buy、平均 $162.05；Tickflow（資料 2026-08-01）20 位 Hold、平均 $156.40；MarketBeat 23 位平均 $152.85、高 $180、低 $120；Investing.com 平均 $144.86、區間 $109–$173。價差比較須引用 numbers.price_at_dd。","source":"StockAnalysis / Tickflow / MarketBeat / Investing.com","url":"https://stockanalysis.com/stocks/JCI","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"個別券商：RBC Sector Perform 目標價 $161（由 $154 上調，2026-07-30）；UBS 目標價 $180（由 $170 上調，Buy）；Wolfe 2026-04 目標價降至 $160。","source":"MarketBeat：Johnson Controls stock price expected to rise, RBC analyst says","url":"https://www.marketbeat.com/instant-alerts/johnson-controls-international-nysejci-stock-price-expected-to-rise-royal-bank-of-canada-analyst-says-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Gumm v. Molinaroli（2016 JCI-Tyco 合併相關股東集體訴訟）2025-03-28 遭法院全案駁回，原告上訴，裁決時程未定","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"On March 28, 2025, the Court dismissed the complaint in its entirety. Plaintiffs have appealed the decision, though the timing of the decision by the court is currently unknown.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"AFFF（消防泡沫）PFAS 訴訟：Chemguard 與 Tyco Fire Products 被列為 49 件待審聯邦集體訴訟被告，另有 7 件加拿大集體訴訟","source":"SEC EDGAR 10-K FY2025 Note 20","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"Chemguard and Tyco Fire Products are named in 49 pending putative class actions in federal courts originating from 20 states and territories.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 11 份 8-K 無重大項目（1.01／2.01／4.02 等）","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000833444&type=8-K","excerpt":"2025-11-02 至 2026-11-02 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"2025-07-31 完成住宅與輕商用 HVAC 業務出售給 Bosch；2026-02-18 宣布、2026-05-13 完成收購 Alloy Enterprises（資料中心散熱技術，金額未揭露，單一二手來源）","source":"搜尋摘要（goldesel.de 報導；10-K FY2025）","url":"https://goldesel.de/aktien/news/johnson-controls-schliesst-alloy-ubernahme-baut-warmepumpen-werk-in-danemark-aus-was-anleger-jetzt-wissen-sollten","excerpt":null,"as_of":"2026-05-13","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-02-18 宣布、2026-05-13 完成收購 Alloy Enterprises，金額未揭露（單一二手來源）；2025-07-31 完成住宅及輕商用 HVAC 出售給 Bosch","source":"goldesel.de 報導；10-K FY2025","url":"https://goldesel.de/aktien/news/johnson-controls-schliesst-alloy-ubernahme-baut-warmepumpen-werk-in-danemark-aus-was-anleger-jetzt-wissen-sollten","excerpt":null,"as_of":"2026-05-13","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"Gumm v. Molinaroli 2025-03-28 遭駁回，原告上訴中","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"On March 28, 2025, the Court dismissed the complaint in its entirety. Plaintiffs have appealed the decision, though the timing of the decision by the court is currently unknown.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"AFFF PFAS 集體訴訟 49 件待審（美）＋7 件加拿大","source":"SEC EDGAR 10-K FY2025 Note 20","url":"https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm","excerpt":"Chemguard and Tyco Fire Products are named in 49 pending putative class actions in federal courts originating from 20 states and territories.","as_of":"2025-11-14","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 無 Item 4.02（財報不可信賴）等重大項目；搜尋僅見 2005-06 重編與 2016 FCPA 和解等舊事","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000833444&type=8-K","excerpt":"2025-11-02 至 2026-11-02 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"JCI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.65,"operating_margin_pct":14.45,"fcf_margin_pct":6.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":34.99,"operating_margin_pct":17.92,"fcf_margin_pct":16.43,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CARR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":24.64,"operating_margin_pct":8.05,"fcf_margin_pct":10.43,"rd_intensity_pct":2.65},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CARR","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"LII","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":33.1,"operating_margin_pct":19.94,"fcf_margin_pct":15.34,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LII","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HON","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.04,"operating_margin_pct":16.2,"fcf_margin_pct":4.95,"rd_intensity_pct":5.37},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"JCI"},"financial_history":{"ticker":"JCI","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-09-30","revenue":20637000000.0,"revenue_yoy_pct":null,"gross_margin_pct":34.36,"operating_margin_pct":9.75,"net_income":1532000000.0,"diluted_eps":2.19,"free_cash_flow":1503000000.0,"fcf_margin_pct":7.28,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-09-30","revenue":22331000000.0,"revenue_yoy_pct":8.21,"gross_margin_pct":34.95,"operating_margin_pct":10.82,"net_income":1849000000.0,"diluted_eps":2.69,"free_cash_flow":1775000000.0,"fcf_margin_pct":7.95,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-09-30","revenue":22952000000.0,"revenue_yoy_pct":2.78,"gross_margin_pct":35.19,"operating_margin_pct":10.53,"net_income":1705000000.0,"diluted_eps":2.52,"free_cash_flow":1604000000.0,"fcf_margin_pct":6.99,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-09-30","revenue":23596000000.0,"revenue_yoy_pct":2.81,"gross_margin_pct":36.41,"operating_margin_pct":11.99,"net_income":3291000000.0,"diluted_eps":5.03,"free_cash_flow":965000000.0,"fcf_margin_pct":4.09,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/JCI/JCI_Q4_2026_Earnings_Call_20261027.md）

# Q4 2026 Earnings Call
**Johnson Controls International plc** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Hello, everyone, and welcome to the Johnson Controls Q4 2026 Earnings Conference Call. My name is Ryan, and I'll be coordinating the call today. [Operator Instructions] I will now hand the call over to Eric Swanson, VP, Investor Relations, to begin. Eric, please go ahead.

**Eric Swanson** (Executives):
Good morning, and thank you for joining Johnson Controls Fiscal Fourth Quarter 2026 Earnings Conference Call. Joining me on the call today are Johnson Controls Chief Executive Officer, Joakim Weidemanis; and Marc Vandiepenbeeck, our Chief Financial Officer. 
As a reminder, today's discussion will include forward-looking statements that are subject to risks and uncertainties that could cause actual results to differ materially. Please refer to our SEC filings for additional information. We will also reference non-GAAP measures. Reconciliations are included in our earnings release and presentation appendix available on our Investor Relations website. I will now turn the call over to Joakim.

**Joakim Weidemanis** (Executives):
Thanks, Eric, and good morning, everyone. This is Eric's first earnings call since joining our Investor Relations team last month, and we're excited to have him on board. I want to start by recognizing Johnson Controls colleagues around the world. Over the last 18 months, we've made significant progress toward becoming a more focused thermal technology company, growing at a faster rate with more investment capacity and higher profitability. At the end of the day, it's our people who bring those strategies to life, combining our technology and deep field and manufacturing expertise to deliver for customers. Their commitment to customers and disciplined execution is reflected in the consistency of our performance.
Fiscal 2026 was an important proof point for the framework we introduced at our Going to Gemba Day in June. Our differentiated technological capabilities, unmatched field presence, global manufacturing strength and proprietary business system are helping us move with speed, win with customers and strengthen performance. For the full year, we exceeded both our initial fiscal 2026 guidance and the raised outlook we provided during the year. Organic revenue increased more than 8%. Adjusted EPS increased 37%, and adjusted free cash flow conversion was 103%. 
We enter fiscal 2027 with momentum and confidence in our ability to continue creating value for customers and shareholders. That confidence is grounded in a business model built around 3 reinforcing elements. Our strategic pillars focus resources on the most attractive opportunities, including AI and data centers, mission-critical environments and decarbonization. Our proprietary business system empowers frontline teams, accelerates problem-solving and drives continuous improvement everywhere in our company. And our economic engine converts those advantages into differentiated customer value, innovation, manufacturing scale and frontline productivity.
The result is a powerful value creation engine that helps our colleagues win and deliver for our customers and grow profitably and compound value over time. These capabilities are increasingly relevant as our priority customers are investing in some of the world's most demanding operating environments to deliver the outcomes they aspire to. This is especially evident across AI and data centers, advanced manufacturing and biopharma. 
As customers scale capacity in these verticals, the environments supporting their operations are more heat and energy intensive, need to be controlled within tighter tolerances and are less tolerant of disruption. Our portfolio brings together integrated thermal management and controls with liquid cooling technologies, including cooling distribution units and cold plates for data centers. We combine subsystem technology developed in-house with the ability to design, deliver and service the broader architecture across the thermal chain, including controls.
As data center architectures continue to evolve, we see additional opportunity in modular data centers. We believe our differentiated capabilities position us well in this emerging segment, and we are investing to win and building a stronger partner ecosystem. Our collaboration with Armada is one example. As announced at the NVIDIA GTC in Berlin, together, we plan to build 500 megawatts of distributed edge compute capacity in 2027, bringing together our thermal management technology, engineering capabilities and global manufacturing scale to bring capacity online faster.
Our advantage comes from bringing together 5 areas of expertise: a focused portfolio oriented toward high-growth, mission-critical verticals; proprietary technologies built over the last 150 years; an unmatched global field presence of approximately 50,000 sales solution architects and highly skilled technicians; an emerging manufacturing advantage focused on quality, capacity and delivery; and our proprietary business system. These 5 areas of expertise allow us to solve complex customer challenges with greater speed, create differentiated value and support sustained profitable growth. We are a global thermal technology leader that is built for this time. With that context, Marc will take you through the financial results in more detail.

**Marc Vandiepenbeeck** (Executives):
Thanks, Joakim, and good morning, everyone. We finished the year with strong fourth quarter results. Organic revenue increased 12%, led by strong double-digit growth in Americas and APAC. Systems grew 13%, reflecting continued strength in data centers, while service continues to deliver with a solid 8% growth. That top line growth, combined with continued productivity, contributed to margin expansion across all 3 regions.
Americas adjusted segment EBITA margin expanded 210 basis points to 22%. EMEA expanded 80 basis points to 16.4%, and APAC expanded 110 basis points to 19%. Strong operating performance, combined with lower corporate expense, drove significant adjusted EBIT margin expansion of 300 basis points to 18%, aligning our operating leverage well within range despite much higher growth. 
Adjusted EPS increased 32% to $1.66. The demand environment also accelerated as we exited the year. Orders increased 44%, driven by continued data center demand, along with strong growth across other mission-critical verticals, including battery and semiconductor manufacturing and large research universities. Backlog grew 43% to a record $23 billion, reflecting sustained demand for our differentiated technology and capabilities.
Our operating performance translated to strong cash flow generation, supported by the disciplined execution and working capital focus embedded in our business system. For the full year, adjusted free cash flow was $3.2 billion, representing 103% conversion. We ended the year with $600 million of cash, while net debt declined to 1.8x below our long-term target range. And we returned $2.5 billion to shareholders through share repurchases and dividends.
This performance provides capacity to invest for growth, maintain our investment-grade credit profile and return capital to shareholders. With customer demand extending well beyond fiscal year 2027 and requirements continuing to scale, customers need a partner with the capabilities and willingness to invest alongside them. Joakim will now discuss how we are investing to meet the demand.

**Joakim Weidemanis** (Executives):
As Marc said, we see customer demand translating into record backlog, a strong pipeline and increasing visibility into longer-term demand with our largest customers. We're acting decisively on that opportunity, investing ahead to expand capacity and capture a larger portion of the growth in our highest growth markets while simplifying Johnson Controls to reduce complexity, move faster and increase earnings power. Both are integral to our value creation plan and reflect a consistent and disciplined approach to capital allocation, investing where we see the greatest opportunities for growth while building a simpler, more productive company. 
We expect approximately $900 million of capital expenditures in fiscal 2027. This investment puts us in a strong position to capture a larger portion of the growth. It is anchored in the demand we see across our backlog and pipeline as well as the longer-term requirements we are planning for with our largest customers, particularly in our highest growth markets. This capital will strengthen our ability to win new business and capture the significant opportunity ahead. It will also expand capacity, improve lead times, delivery and quality, enable us to serve customers as their requirements scale.
Our business system is enabling us to add that capacity more efficiently. Without the productivity and capital efficiency we are driving across the company, we estimate the capital requirement would have been more than 2x higher. We are applying that same discipline to our restructuring actions, reallocating resources and capacity toward the areas where we see the strongest opportunities for growth. 
While our growth investment is focused on thermal technology, our restructuring actions are concentrated primarily in other parts of our portfolio outside our most technology-differentiated mission-critical verticals. There, we are optimizing our manufacturing and warehouse footprint, streamlining the functions that support those operations and moving accountability closer to customers. We anticipate approximately $400 million of restructuring expense over fiscal 2027 and fiscal 2028 and expect approximately $600 million of gross annualized savings by fiscal 2029. 
These actions will position us to support the growth we see today and the opportunities ahead. Additional capacity positions us to capture increasing demand, simplification improves speed and accountability, and productivity creates room to reinvest, expand margins and increase earnings power. Marc will now review our fiscal 2027 guidance.

**Marc Vandiepenbeeck** (Executives):
The investments and actions Joakim just outlined position Johnson Controls to accelerate growth while maintaining our margin expansion trajectory. Our fiscal year 2027 outlook reflects the strength of the demand environment, the visibility provided by our backlog and continued improvement in execution. For the first quarter, we expect organic revenue growth of 12% to 14%, operating leverage of 30% to 35% and adjusted EPS of $1.15 to $1.20. 
For the full year, we expect organic revenue growth of 11% to 12%, ahead of the high single-digit growth in our long-term algorithm. We expect operating leverage of greater than 30% and adjusted EPS of $6.15 to $6.30. At the midpoint, that represents 21% EPS growth from fiscal 2026. As we meaningfully increase capital expenditure to support growth, we expect an adjusted free cash flow conversion of approximately 95%. 
Our ability to maintain such a strong cash flow conversion while increasing investment, investing in restructuring and increasing manufacturing capacity demonstrate the strength and quality of our earnings and disciplined capital allocation. Operator, we are now ready for questions.

**Operator** (Operator):
[Operator Instructions] Our first question will come from Amit Mehrotra with UBS.

**Amit Mehrotra** (Analysts):
Appreciate the question. Maybe we can start with backlog and growth, obviously both extremely strong. Maybe you can just talk about your ability to sort of keep growing the backlog as the revenue growth picks up. Do you still expect to sort of convert 70%, 80% of that over the next 12 months? And I noticed F&S growth sort of perked up in the Americas, which is encouraging to see. Maybe you can just talk about sort of the expectations there as well.

**Joakim Weidemanis** (Executives):
Amit, we had very healthy order entry in the quarter, coming off of a prior quarter where the order entry also was very strong. So our backlog continues to grow while our ability to execute and deliver through our manufacturing operations, but also our field teams, continues to improve. Our pipelines, Amit, continue to grow. They're very healthy in multiple verticals. Of course, data centers was very strong, but we also have a number of other mission-critical verticals that continue to grow here from both pipeline and orders point of view. So we're very confident with the guide that we've given here.

**Amit Mehrotra** (Analysts):
And I guess, Marc, just as a follow-up on the incremental margin of 30% plus, and that's obviously consistent with the long-term framework. I understand that obviously there's a need for capacity. But at Investor Day, we talked a lot about this opportunity to create synthetic capacity. And so maybe you can just balance those 2 and is there maybe an opportunity to sort of exceed the long-term framework in '27, just given how early we are in the journey of the productivity initiatives?

**Marc Vandiepenbeeck** (Executives):
Yes. So we're already exceeding the long-term algo on the top line, right? We guided that 30-plus percent incremental on a high single-digit long-term algo, which we're seeing a much faster growth now, going into fiscal year '27, and yet are maintaining that operating leverage well above 30%. The underlying question is how much headwinds do we see as we build that capacity into the factory? There's an opportunity to accelerate growth and potentially create higher operating leverage in the back end of the year as the ramp-up stabilize a little bit and we get to a better run rate from the infrastructure we've built. 
And of course, the business system continues to drive enormous opportunities for us to create that soft or synthetic capacity within the factory, allowing us to really create more output with much, much less capital. As Joakim laid it out in his opening remarks, we think we would have probably -- have needed about twice as much capital as we were going to need over the next year or so, to be able to invest in the growth we are seeing and that continues to increase from our customers.

**Joakim Weidemanis** (Executives):
And the $900 million, Amit, investment in capacity here is obviously in manufacturing, but it's also in innovation as well as investing in digital and AI approaches to continue to -- which is part of our proprietary business system, to continue to drive more productivity and better execution capabilities in our field operations.

**Operator** (Operator):
Our next question will come from Nigel Coe with Wolfe Research.

**Nigel Coe** (Analysts):
Not a bad FY '26. Congratulations on wrapping that up. Just I want to go back to the orders and obviously, standard strength in the Americas, good traction elsewhere. But just curious if there's any change in the kind of the contours of the orders. Is this still largely a chiller story? Or are we starting to see a bigger mix of, I don't know, modular or CDUs? Just wondering if there's any change in the mix of orders.

**Joakim Weidemanis** (Executives):
Yes. So what we've been working on, in particular, in the data center area is to increase our TAM. And as you've heard over the last couple of quarters, we've increased our offering, added CDUs, acquired a cold plate company that we're now making good progress with several major customers. And in modular data centers, that is not a new product line for us, but with a little bit increased focus here and a little bit more innovation work. You've been able to read about some of the progress that we've been making here more recently. So chillers is the largest part of our portfolio still, but a good part of our growth is starting to come from these efforts that we -- I outlined here to increase our TAM. So we're very encouraged about what we're seeing here.

**Nigel Coe** (Analysts):
No question. And then just coming back to the -- it looks like it's a new restructuring program, Marc, the $400 million of expense to yield $600 million of savings by FY '29. Number one, I just want to make sure this is a new program on top of the existing program. And maybe just bring us up to speed in terms of where we are right now on the current program and the sort of savings you expect to realize on the current program.

**Marc Vandiepenbeeck** (Executives):
Yes. So if you look at the existing program that really came from the divestiture of our residential light commercial, a lot of that program had to do with fixing how we organize and the base cost and the support infrastructure that drives solutions and functional support for customers. And we're very pleased with how that came about. So we had announced about $400 million of expense for $500 million of savings. And we've spent about 85% of that $400 million. And you can see as it translates into the earnings here this year, the run rate savings is probably $100 million to $150 million above that original $500 million target. So the outcome and the speed at which we generate the savings ended up, a, being much faster on the old program, but also being much higher. 
As we looked at more opportunity to simplify the portfolio, we clearly saw the opportunity to simplify the part of the portfolio that is less geared toward the mission critical and data center, and simplify a little bit our logistics and manufacturing footprint, which hasn't been touched as part of the original program. And so that new program we expect will have maybe a little bit longer lead time than the original program, less low-hanging fruits. But I think it will bear probably as good of a level of return as the first program did. And we are very excited about the opportunity to further simplify our infrastructure.

**Operator** (Operator):
Our next question will come from Steve Tusa with Wells Fargo.

**Charles Stephen Tusa** (Analysts):
Just on the earnings bridge for '27. I think you break out mix and things like that. You mentioned the savings this year. Can you maybe give us a little bit of color on mix, price/cost and then any kind of savings you have flowing through just to help decompose a little bit the margin?

**Marc Vandiepenbeeck** (Executives):
Yes. The -- so I'll get past the divestiture item that we put on that bridge. But clearly the year was really supported by the accelerated growth that we saw mostly in system, and that's our chiller output revenue that came about. Because of the efforts we did from a business system standpoint, we saw a lot of productivity. The mix uplift we saw really had to do with the different mixes of businesses that generated that incremental revenue. 
So less the traditional fire and security business and more of the higher-end-margin chiller where we differentiate more and we have the ability to really deploy our technological advantage, and that created a gross margin lift. Now transparently, service was a slight drag into that internal mix, but if you net all of that out, it's really focusing and orienting our growth opportunity against end market where we can differentiate and provide solution for the customer that they're willing to pay for.

**Charles Stephen Tusa** (Analysts):
Okay. And you're price/cost positive?

**Marc Vandiepenbeeck** (Executives):
We are price/cost positive for the year. There was a lot of inflation on both material and a little bit on raw. You can see that while we maintain price/cost positivity, the incremental price we got on top of inflation does not fully translate into the same margin rate. Said differently, we don't get exactly the 37% gross margin rate we have on our recovery on inflation, but we're absolutely price/cost positive. It's just slightly margin dilutive for the year.

**Operator** (Operator):
Our next question will come from Scott Davis with Melius Research.

**Scott Davis** (Analysts):
Congrats on a great year. Just quick to clarify on Steve's question, are you -- do you need more price in '27 to be price/cost positive?

**Marc Vandiepenbeeck** (Executives):
No, we are price/cost positive in '26, and we will be price/cost positive in '27. We don't need more relative price. My point, Scott, was if you get 100 points of price and you have a cost increase of 80, you're price/cost positive by 20. But that 20 is less than your normal 37% in our case, gross margin rate. And so, yes, ideally, I'd always love more price, but we want to remain competitive in the way we play in the market. 
And so we'll continue to act as good guardian of our shareholders' money and price way higher than what we see in inflation. But our ability to maintain from an inflationary standpoint, the entirety of the gross margin rate of the enterprise at time will become challenged.

**Scott Davis** (Analysts):
Okay. That's helpful. And then are you guys done with 80/20 in fire and security? And I don't mean that -- well, growth reaccelerated, so are we kind of -- have you anniversaried the tougher kind of comps there on 80/20 or was growth itself just that much stronger?

**Joakim Weidemanis** (Executives):
Well, when it comes to the business system that we have built and are deploying, that's a multiyear journey. So to some respect, and it's the good news, that you're never done because there's always more opportunity. I think what we're seeing is, to go back to the performance of some of those businesses, is that as a result of leveraging our business system, but also as a result of some org changes we made a couple of quarters ago, where we have decentralized decision-making and empowered frontline general managers with a broader scope of responsibility, think being able to influence the customer end-to-end. I think we're starting to see the early benefits of that. So I'm very encouraged and expect to see more here going forward.

**Scott Davis** (Analysts):
Congrats again, guys.

**Operator** (Operator):
Our next question will come from Joe Ritchie with Goldman Sachs.

**Joseph Ritchie** (Analysts):
I echo everybody's congratulations on a great year. The first question I have is really just around the backlog conversion. So your guidance implies call it roughly around $3 billion in incremental revenue in FY '27 versus FY '26. Obviously, backlog is up $8 billion. What I'm trying to understand is just -- is it just the nature of the projects that you're booking, and when those projects are expected to deliver? And is there potential upside to Amit's question from earlier around like synthetic capacity to be able to deliver more of your backlog in FY '27 than what's implied in your guidance?

**Marc Vandiepenbeeck** (Executives):
Yes. No, fair question, Joe. The $23 billion backlog we've now accumulated over the past year, that really provides us very clear visibility into the growth for '27 and is fully embedded in how we've outlooked the 11% to 12% organic revenue growth for the year. We still anticipate 70% to 80% of that backlog to convert into revenue over the next 12 months. That's not something that has changed.
And the remainder of that balance that extend beyond fiscal year '27. The primary constraint really is not demand. The demand continues to accumulate, and the mix of project is not materially changing. But in some case, we see customer that continues to face power and some electrical infrastructure limitation. That influences their commitment on when they want to take delivery and the project timing and simply the schedule of how that will all unfold. But we are very confident that we are going to continue to build a backlog and continue to build capacity to accelerate growth.

**Joseph Ritchie** (Analysts):
That's great, Marc. And then I guess just my follow-on question, maybe just on that capacity. You guys talked about this ability to create synthetic capacity. I'm just curious, just given the demand environment remains so strong, is there a point where this capital-efficient approach that you guys have maybe requires additional hard CapEx? Or do you feel like you've got good line of sight for the next couple of years?

**Joakim Weidemanis** (Executives):
I think we have pretty good line of sight for the next couple of years. And I will back that up with what many of you who participated in our Going to Gemba Day in June, where we showed an example of how we had taken a part of a factory and quadrupled the capacity without adding head count, capital and actually had reduced the number of space needed. So there are still many opportunities like that available to us. So our capacity expansion going forward is going to continue to be less capital-intensive than in the past.

**Operator** (Operator):
Our next question will come from Andrew Obin with Bank of America.

**Andrew Obin** (Analysts):
Can you just talk about what's happening in just HVAC supply chain? Specifically, I'm thinking Silent-Aire. A lot of headlines, a lot of concerns. You seem to have been able to deal with it well. Where are we? What does it look like into next quarter? And what are your assumptions into next year? And how are you managing it?

**Joakim Weidemanis** (Executives):
Well, so first of all, thanks for that question. So first of all, as you heard also from -- at the Going to Gemba Day, and those materials, for those of you who weren't there, are on our website. So our vertical integration here is really a significant advantage in a high-demand environment that we're living in right now. And you'll recall we talked about for chillers, for example, a chiller is really 5 key subsystems, and we own not just the proprietary technological know-how, but also control the COGS.
So we manufacture the 5 subsystems and are quite vertically integrated. And we, of course -- but we're not vertically integrated on everything, so we continue to look at what would make sense economically to do it more in-house to reduce the dependency on potential shortages from a variety of vendors. And included in that is also looking at potential acquisitions of -- I think of them more as surgical acquisitions, bolt-on acquisitions to help protect our supply chain here. But so far, our teams are executing very well. So even though there are the odd issues, which there always are in manufacturing, we're able to execute pretty well here, as you see from the results.

**Andrew Obin** (Analysts):
And then just maybe a more technical question. Given your relationship with Armada, how does the modular product flow through your P&L? How should we think about it? Because you sort of get very excited about capacity additions. Do we just assume all of this revenue flows through the P&L and margin? Or how should we think about modeling it?

**Marc Vandiepenbeeck** (Executives):
Yes. So the way that flows through is our Silent-Aire. So relationship with Armada is we are really the infrastructure provider of those containerized modular edge compute sovereign AI pods. As you know, we are very proud of having been now qualified for the new NVIDIA program, and we announced that plan to ramp up 500 megawatt with them. Armada has the entirety of the software layer and distributed application that goes through that compute, and we take care and revenue in our P&L over the next 12, 18 months. 
Everything that has to do with the equipment and those containerized modular data center. And so we're very excited about that opportunity, the growth it represent. We think that market will continue to evolve, and it will continue to evolve to the positive, as some of the political environment and the uncertainty around logistic and location and the need to accelerate the speed to compute will continue to be a critical item for our customers.

**Joakim Weidemanis** (Executives):
And our TAM, our dollars per megawatt, if you will, is higher in this kind of business than in most other parts of the data center business that we're in. I'm talking about per megawatt now. And so you should think about those modular data centers as having pretty much everything we develop and own included in it.

**Operator** (Operator):
Our next question will come from Nicole DeBlase with Deutsche Bank.

**Nicole DeBlase** (Analysts):
Can we just talk a little bit about what you're seeing with respect to the Middle East and what you've baked in for the Middle East within the EMEA outlook for 2027?

**Joakim Weidemanis** (Executives):
So the Middle East was challenged in 2026. But over the last couple of quarters, it would seem like some customers have figured out how to live with the uncertainty of the environment. And therefore, we are projecting a slight improvement in what we expect from that region. But of course, there's still a lot of uncertainty around what's going to happen there. So we're not back to where we were before the uncertainties.

**Nicole DeBlase** (Analysts):
Okay. Understood. And then with respect to the Global Intrusion announcement yesterday, is it possible to size that business in terms of the total divestitures that you guys were -- have been considering that you've disclosed? And any update on the progress for -- or the time line for additional divestitures?

**Marc Vandiepenbeeck** (Executives):
Yes. So first, that intrusion business, if you remember, it's a residential, very light commercial type of business. As you know, those are 2 end market that we've really decided were noncore for what JCI does and really not aligned with our mission-critical approach. We anticipate to close that transaction towards the end of the second quarter of '27. That transaction will be slightly dilutive. Think about $0.15 on an annualized basis once it closes. So for the balance of fiscal year '27, it won't be highly material as we look into it. But depending on the timing, we'll keep you posted. The annual revenue of that business is right around $0.5 billion.

**Joakim Weidemanis** (Executives):
And then, Nicole, we continue to work on our overall portfolio, and the overarching goal here is, of course, to create shareholder value. And so there is more work going on, and we'll keep you posted. But meanwhile, of course, we're -- as per the other question that was asked, we're making sure that we continue to execute better across the portfolio.

**Operator** (Operator):
Our next question will come from Noah Kaye with Oppenheimer.

**Noah Kaye** (Analysts):
Yes. So your comment earlier about the productivity of the CapEx you're adding and how it would have been twice as high were it not for the business system. I wonder if we could put some additional parameters around that. Is there a way to think about the revenue capacity that this investment is bringing? Because I think it would be a good measure of kind of your capital efficiency here, and obviously help us understand some of the longer-term growth possibilities.

**Marc Vandiepenbeeck** (Executives):
The goal is to keep up with the demand as we see it coming from the mission-critical vertical like data center, meaning the goal is to keep up for a longer period of time with double-digit growth demand in terms of revenue opportunity. Doesn't mean we'll be a double-digit growth company forever, but it means that the objective of the buildup of our infrastructure in '27 and in '28 is to maintain that double-digit trajectory and capture as much as we can of the opportunity as we see it and maintain that leadership position in those critical domain that JCI has been operating in.

**Joakim Weidemanis** (Executives):
And keep in mind, again, the $900 million, of course, manufacturing is an important part of that. But as I've mentioned before, there's an important part of innovation investments in there as well to accelerate the rate -- the speed and rate of innovation to further our competitive advantage, capitalize on 150 years of know-how -- technological know-how that we built up. And then there's also a chunk of investment related to, basically think of it as productivity in the field that will enable our -- with AI and digital approaches and tools, enable our field to serve and win more customers.

**Noah Kaye** (Analysts):
A question on some of the regional orders dynamics. I think it's striking that Americas was so robust this quarter. When we look at the pipelines and where we're seeing inflection in pipeline growth, one could argue that EMEA and APAC are perhaps seeing more accel at this point. I'm curious to know if you see that in your pipelines as well, and how you think about the implications for orders growth from here moving into the next several quarters.

**Joakim Weidemanis** (Executives):
So our pipelines continue to grow at a nice rate in all 3 regions. Now having said that, the some of the secular drivers around data centers, semicon, those 2 verticals that really are related to the world's desire and need for more compute. The drivers are much stronger in the United States and Asia Pacific. And by the way, in Asia Pacific, they have strengthened in a very nice way here over the last couple of quarters. 
Europe is just simply a little bit earlier in its journey when it comes to all things compute, but we expect that to hopefully change here over the next year. Beyond those verticals, there are healthy pipeline growth in, for example, biopharma, but also defense for the obvious reasons. You can read in the paper every day what's going on in the world, right? So -- and so the mix of what's happening in the pipeline is a little bit different by region here. But generally, pipelines are growing very nicely in every region.

**Operator** (Operator):
Our next question will come from Jeffrey Sprague with Vertical Research.

**Jeffrey Sprague** (Analysts):
Just coming back to backlog and conversion. I know there's been a couple of questions on this, but the fundamental principle of the backlog you share with us, I believe, is backlog that you can deliver within the next 12 months. Obviously, what you can deliver and what the customer can accept are maybe 2 different things, which gets us to maybe that 70% to 80%. But wanted to confirm that's fundamentally correct. The backlog is technically deliverable within 12 months. 
And then -- so maybe you could -- if that's so, then the numbers do suggest fairly significant revenue upside relative to your guide, and it obviously is an initial guide, we get that. But maybe just kind of talk about maybe those customer bottlenecks. Are they getting more significant? What role you could maybe play in helping untangle some of this stuff? And just any other perspective on that sort of broader question.

**Marc Vandiepenbeeck** (Executives):
Yes. So as I mentioned earlier, the primary constraint is really not demand. And yes, the definition, as you laid it out, is exactly what it is. We -- unconstrained supply, unconstrained demand, we could deliver the entirety of that backlog in the next 12 months. It doesn't mean that our customer will be able to. And in some cases, the customer continue to face the same problem as they have historically. I wouldn't say not at a faster pace. So dynamically, the market isn't changing. The location, maybe in some of those data center, is moving a little bit around. 
But we don't see really a slowdown or more difficulty from a customer standpoint to accept the orders. But your point stands, if some of those constraints simplify or loosen up a little bit over the next 12 months, our ability to unfold more of the backlog quicker is absolutely an opportunity. And as you said, 11% to 12% is where we see the year coming in. Should the market evolve a little bit differently, we could be -- potentially do better.

**Jeffrey Sprague** (Analysts):
And then maybe since we're near the tail end of the call and we've covered a lot of ground, I'll just throw a modeling nit at you, Marc. Just kind of the movement in corp and amort looks a little odd dropping down the way it did in Q4 and then back up in Q1. Can you just provide a little color on what's going on there?

**Marc Vandiepenbeeck** (Executives):
Yes, the amort coming down was just part of the normal amortization schedule, and when you see it coming back up, it's associated with the transaction we did on Alloy, that increased in the quarter, the amortization expense. As you know, new acquisition, especially technology capability acquisition, will come sometimes with a little bit more amort than you normally do. But those are for the good reason, and we're really excited about the opportunity that Alloy brings from a heat exchanger differentiation as well as our entry into the cold plate market and differentiated CDU opportunities.

**Operator** (Operator):
Our next question will come from Varun Govindaraj with Bernstein.

**Varun Govindaraj** (Analysts):
Every few months, there's always this scare that, hey, chillers are going away. At GTC in Berlin, NVIDIA put out another video showing that. Clearly, it's not reflecting in your strong order numbers, but are you hearing anything at all from customers indicating a shift away from chillers? And just as you plan for this over the longer run, how are you thinking of managing that risk away?

**Joakim Weidemanis** (Executives):
Thank you for the question. I think lots have been written on that topic by many on this call. I think there will be some situations over time where on the margin, perhaps 1 or 2 fewer chillers will be needed. But by and large, customers are designing data centers with redundancy and designing them for operating at certain peak conditions, which even though you would think you may be able to reduce the number of chillers, in practice, in reality, that's not how they're being designed, at least not -- yes, with less chillers, that is. 
Now regardless of that, as I mentioned before, our strategy in the data center market is to continue to increase our TAM per megawatt, and we're doing that through a number of ways. But if I talk about 2 approaches. One is, and we've talked about this before. One is simply approaching -- our strategy is to win in the overall thermal architecture of the entire data center to be able to reduce the amount of energy used for even higher capacity and more rapid response cooling. And we're doing that by adding -- have been adding capabilities in CDUs, in cold plates and in controls. And there's more to come, and we'll be announcing more here in the next couple of quarters. 
And so that's one way to increase the TAM and help our customers basically design and operate much more efficient data centers. And then the second thing, which we talked about earlier on this call, is really the modular segment that we have been in for a number of years, but that we've decided to double down on because we think the opportunity is very, very compelling here in the near and medium term. And there, again, as I alluded to, our TAM per megawatt is even higher than in the larger gigawatt data centers.

**Varun Govindaraj** (Analysts):
Got it. And then as a quick chiller-related follow-up, are you seeing anything happen in the mix between air-cooled and water-cooled units just with this whole narrative around water conservation? Whatever you can share qualitatively?

**Joakim Weidemanis** (Executives):
The mix has not changed materially recently. And as you know, almost all of the data centers that are being built today have closed-loop water cooling systems and consume less than -- much, much less than your local golf course. And so I think this water consumption point is something many of our customers are addressing now with the general public through their ramping PR agencies here. It's quite frankly old news and not the way data centers have been designed for a long time.

**Operator** (Operator):
Our next question will come from Brett Linzey with Mizuho.

**Brett Linzey** (Analysts):
I wanted to follow up on the pipeline, the CDU, and then the incremental business on cold plates. I guess as we look at that $1 billion pipeline, how much of that is already converted into orders -- firm orders here? And then, thinking about as that new capacity comes online, how much is effectively spoken for versus really dependent on future order conversion?

**Marc Vandiepenbeeck** (Executives):
Only a small portion of that $1 billion-plus pipeline is converting to date. So there's a lot of upside opportunity, and we continue to see that pipeline growing. We are ramping up capacity for CDU in all 3 regions. That capacity is mostly spoken for as we look at it. But part of the investment we're making, the $900 million of CapEx, has to do with ramping up that capacity at speed to reduce our lead time and have the opportunity to accelerate the order rate for a very differentiated CDU product offering.

**Joakim Weidemanis** (Executives):
And then in general on capacity, let me share a little bit the types of discussions I'm having with some of our larger customers, which basically is along the following lines. We have, over the last year, staffed up with an incredibly strong manufacturing and operations team, which is why, and they're helping us deploy the business system to create capacity through lean manufacturing. But they're also very strong and experienced at standing up new capacity as we continue to do, and we've talked about on this call. 
We're able to, for many of our product lines, stand up new plant -- physical plant capacity within 12 months. And with the lean manufacturing, the business system, we're able to create meaningful capacity within quarters in addition to what we get for the -- with the hard capacity that we create.
Many of our customers take more than a year to build the data center, right? So they are ordering, in some cases, up to a year ahead of when they need the actual equipment. So we're trying to create a situation here, and I think we're there, where we can -- we have flexibility on creating capacity faster than the demand requires it. And so we're trying to create a bit of a business model change, which we believe is going to be part of our -- many aspects of our differentiation.

**Brett Linzey** (Analysts):
Yes. I appreciate that. And then just a quick follow-up on service and specifically the attachment rates. So very strong growth in systems, service, obviously, strong. But the rate of growth not the same level. What really explains that? I guess, is it duration? Or is there resource allocation? Maybe just talk about the uptick in your attachment rate trends.

**Joakim Weidemanis** (Executives):
Well, so we're in many different service businesses, right? You've got HVAC, you have fire, you have security. And within those businesses, there are different service games, right? So it's -- you can't really generalize. We've spoken about in prior quarters where the growth has been more subdued, in particular in our security part of the portfolio, the service and the security portfolio, where we have done work to look at what kind of contracts we want to be involved in, the growth run rate and the profitability of those. 
And as we're repositioning a little bit in the service side of the -- security service side of the business, we're still seeing a little bit of subdued growth there, but it's starting to pick up. But as we've said in prior quarters, we still probably have another 1 or 2 quarters ahead before we're on the other side of that. So the security service business is the one that is -- has the biggest opportunity here.

**Operator** (Operator):
Our next question will come from Toby Okwara from Morgan Stanley.

**Tobenna Okwara** (Analysts):
Congrats on the great quarter. I just wanted to follow up on some of the service questions and specifically in data center. I guess was this -- as the business mix is more towards data center, does that change the service opportunity long term at all? Or how do you kind of think about that?

**Joakim Weidemanis** (Executives):
Yes, it will. And obviously, the systems growth is very, very healthy, and the attachment rates in the data center world are higher than fleet average. So over time, that will benefit us. And we believe that our field footprint is one of the industry's largest. And as we're deploying our business system, and as many of you who visited us on the Going to Gemba Day could see, we're not just improving our ability to productize and sell services, but we're also improving our ability to execute on those services more productively. So we believe there's both a, over time, a top line acceleration opportunity, but also a very nice margin opportunity here.

**Tobenna Okwara** (Analysts):
And then following up on some of the international questions. I guess outside of Middle East, how did the growth look in Europe there? And what would you need to see in the market to see acceleration and the catch-up to the growth that we've seen in Americas and APAC?

**Joakim Weidemanis** (Executives):
Yes. So first of all, I think it's important to understand that our business mix is quite different in Europe than the other 2 regions. So we're much heavier on fire and security in Europe. And -- but building our presence on thermal management, meaning HVAC and control. So -- and that's where the investments are going in Europe. As you heard, the market in Europe for data centers and semicon is in earlier stages than it is in the United States and Asia Pac, but I think that over the next few years, we're going to see a significant pickup in that, and we're positioning ourselves to be ready for that.

**Operator** (Operator):
This concludes our Q&A session. I will now hand the call back to Joakim Weidemanis for any closing comments.

**Joakim Weidemanis** (Executives):
Thank you all for joining us today. So we exit fiscal 2026 with great momentum, record backlog and clear visibility into the year ahead. Our differentiated technological capabilities, our unmatched field presence and proprietary business system positions us to support customers as their requirements continue to scale and to create increasing value for our shareholders. I want to thank our more than 90,000 colleagues around the world for their commitment to our customers and for continuing to raise the standard of execution across Johnson Controls. Thank you for joining us today.

**Operator** (Operator):
This now concludes today's call. Thank you all for joining. You may now disconnect your lines.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### JCI_Q3_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：FY26 有機營收成長財測由約 6% 上調至約 8%（原話："expect organic revenue growth of approximately 8%, up from"）
- 2026-07-29｜CFO｜guidance：Q4 財測：有機營收成長與營運槓桿區間（原話："organic revenue growth of 9% to 10%, operating leverage of"）
- 2026-07-29｜CFO｜guidance：FY26 調整後 EPS 財測上調（原話："raising our adjusted EPS guidance to approximately $5.05"）
- 2026-07-29｜CFO｜guidance：FY26 自由現金流轉換率維持約 100%（原話："adjusted free cash flow conversion of approximately 100%"）
- 2026-07-29｜CFO｜guidance：FY27 具體財測留待下次法說（原話："too early to provide real specific fiscal year '27 guidance"）
- 2026-07-29｜CFO｜guidance：Q4 EMEA 預期極低個位數至持平（原話："EMEA land in very low single digit to flat in Q4"）
- 2026-07-29｜CEO｜guidance：中東假設近幾季情況無重大改變（原話："we can't predict the Middle East any better than you can"）
- 2026-07-29｜CFO｜margin：Q3 調整後 EBIT margin 擴張 260bp（原話："while adjusted EBIT margin expanded 260"）
- 2026-07-29｜CFO｜margin：管理層說明營運槓桿未來 12–24 個月仍高於 30%（原話："higher than 30% operating leverage over the next 12 to 18"）
- 2026-07-29｜CFO｜margin：資料中心系統占比提高造成設備組合 margin 小幅逆風（原話："a smaller equipment mix margin, a small headwind"）
- 2026-07-29｜CFO｜commitment：重申長期算式：營收高個位數成長、增量至少 30%（原話："top line growth and at least 30% of incremental"）
- 2026-07-29｜CEO｜commitment：Gemba Day 長期算式含營運槓桿、EPS 與 FCF 轉換（原話："operating leverage of more than 30%, double-digit adjusted"）
- 2026-07-29｜CFO｜commitment：資料中心營收占比 3–5 年內成為公司三分之一（原話："becoming 1/3 of the company from a revenue standpoint"）
- 2026-07-29｜CFO｜commitment：服務目標回到中至高個位數成長（原話："returning to mid- to higher single-digit growth is the focus"）
- 2026-07-29｜CEO｜commitment：Armada 相關機會預告未來幾季再談（原話："within the next couple of quarters, we'll be able to talk"）
- 2026-07-29｜CEO｜customer：訂單與積壓訂單：動能超過 25%、積壓創高（原話："backlog grew more than 30% to a record $21 billion"）
- 2026-07-29｜CFO｜customer：系統訂單成長 40%（原話："Systems order grew 40%"）
- 2026-07-29｜CFO｜customer：FY26 資料中心占營收比重預估（原話："land in the high teens as a mix of percentage of revenue"）
- 2026-07-29｜CEO｜customer：對 AI 需求可持續性的看法（原話："the output of the data centers is going to continue to grow"）
- 2026-07-29｜CEO｜customer：資料中心客戶未見需求受新聞影響（原話："seen any impact on demand at all from what you see in"）
- 2026-07-29｜CFO｜product：CDU 預計本季開始出貨（原話："We are going to start shipping actually this quarter."）
- 2026-07-29｜CFO｜product：CDU 商機 pipeline 達 10 億美元（原話："has now reached $1 billion"）
- 2026-07-29｜CEO｜product：取得 NVIDIA 認證（原話："we had the recent NVIDIA certification as well"）
- 2026-07-29｜CEO｜product：吸收式冷卻機參考設計可降低冷卻用電約 44%（原話："reduce cooling electrical demand by approximately 44%"）
- 2026-07-29｜CEO｜product：持續提高每百萬瓦的營收含量（原話："continue to work on increasing our dollars per megawatt"）
- 2026-07-29｜CEO｜product：管理層看法：冷水機需求下降之說影響極小（原話："going to be a very, very nominal impact, if any"）
- 2026-07-29｜CEO｜competition：稱在其聚焦類別中正在取得市占（原話："We think we are for the categories that we focus on."）
- 2026-07-29｜CEO｜competition：大型資料中心客戶很少只選單一夥伴（原話："rarely just pick one partner that they design in with"）
- 2026-07-29｜CFO｜competition：安全業務差異化較低，出現競爭性量壓力（原話："a little bit less differentiated than, for example, our HVAC"）
- 2026-07-29｜CFO｜competition：安全業務競爭性量壓力（原話："created a little bit of a competitive volume pressure"）
- 2026-07-29｜CFO｜risk：美洲服務積壓訂單下滑歸因於安全業務定價與轉向成長（原話："pivoting towards growth and the dynamic of price"）
- 2026-07-29｜CFO｜risk：Fire & Security 市場被描述為非高成長市場（原話："a high single-digit or double-digit growth market"）
- 2026-07-29｜CEO｜risk：供應鏈偶有瓶頸、仰賴外部供應商（原話："we depend on external vendors as well"）
- 2026-07-29｜CEO｜risk：產能：Applied HVAC 爬坡略快於預期，仍需新增實體產能（原話："we're also going to have to add some new physical"）
- 2026-07-29｜CFO｜capital_allocation：淨負債比降至 1.9x，低於長期目標區間（原話："Net debt declined to 1.9x, below our long-term target range"）
- 2026-07-29｜CFO｜capital_allocation：現金狀況使公司更能投資業務（原話："We are now better positioned to invest in the business"）
- 2026-07-29｜CEO｜capital_allocation：電力端可能以夥伴或外科手術式併購擴充（原話："surgically expand our capabilities there"）
- 2026-07-29｜CEO｜capital_allocation：策略檢討進展但無時程（原話："we continue to make progress, and we will keep you posted"）
- 2026-07-29｜CFO｜capital_allocation：持續出售住宅訂閱業務（原話："we have a few more to go"）

### JCI_Shareholder_Analyst_Call_Johnson_Controls_International_plc_20260601.md
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：長期有機成長目標由中個位數提高到高個位數（原話："a clear path to a high single-digit organic growth overall"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：舊長期算式的有機成長口徑為中個位數（原話："pegged around mid-single digit"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：營運槓桿（增量利潤率）長期口徑為 30% 以上（原話："leverage at 30-plus percent from where we were"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：未來 12–18 個月增量利潤率預期高於 30%（原話："the next 12 or 18 months, where we will do better than 30%"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：CFO 對分析師提出的 50% 增量利潤率說難以辯護（原話："50% is going to be hard to defend at this stage"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：資料中心 2025 年約占營收 12%（原話："Data center last year in 2025 was about 12% of our revenue"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：預期五年內資料中心約占公司三分之一（原話："it will be about 1/3 of the company within the next 5 years"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：服務業務過去中至高個位數成長，目標提高到更高的個位數（原話："through a better productization of our service offering"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜commitment：仍承諾 EPS 雙位數成長（原話："double-digit growth in our EPS"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜commitment：維持 95%–100% 自由現金流轉換率（原話："performing between 95% and 100% free cash flow conversion"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜commitment：承諾將 100% 自由現金流還給股東（原話："we are committed to returning 100% of our free cash flow"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜capital_allocation：管理層稱已讓資本支出與營收成長脫鉤（原話："we have decoupled the need for capital expenditure"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜capital_allocation：管理層稱未來某時點仍需要實體（hard）產能（原話："at some point, hard capacity will be needed"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜capital_allocation：併購管線健康（原話："We have a very healthy pipeline of M&A opportunities"）
- 2026-06-01｜CEO Joakim Weidemanis｜capital_allocation：補齊熱管理鏈不需大筆資本投入，可能有收購（原話："we don't need any major capital deployment"）
- 2026-06-01｜CEO Joakim Weidemanis｜capital_allocation：投資組合無新說法，維持股東導向評估（原話："we don't have any new news versus what we've spoken about"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜margin：服務利潤率有機會從 40% 多再往上（原話："from a 40s percent margin to something greater over time"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜margin：庫存改善帶來的利潤與現金效益（原話："overall, it's hundreds of basis points"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜margin：ACE 工廠準時交貨率由 43% 到 100%（原話："43% on-time delivery 4 months ago, 100% on-time delivery"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜margin：ACE 工廠改善所需資本支出很少（原話："very little CapEx required to achieve that"）
- 2026-06-01｜CEO Joakim Weidemanis｜margin：ACE 工廠產能提升至四倍（原話："we're now able to quadruple the capacity of that"）
- 2026-06-01｜CEO Joakim Weidemanis｜margin：管理層稱不需要 44 座工廠（原話："probably not going to need 44 plants in the future"）
- 2026-06-01｜CEO Joakim Weidemanis｜margin：銷售與服務端仍會增員，G&A 不增（原話："We'll continue to add people in some functions"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜margin：現場業務賣方與客戶相處時間倍增（原話："we managed to double the time those sellers are able"）
- 2026-06-01｜CEO Joakim Weidemanis｜customer：訂單與積壓訂單創新高（原話："Our backlog is at record levels"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜customer：資料中心客戶週期汰換速度較快（原話："churn time of a data center customer is about 60% faster"）
- 2026-06-01｜CEO Joakim Weidemanis｜customer：資料中心服務合約初始附加率高於產業平均（原話："the initial attach rate of service contracts is much"）
- 2026-06-01｜CEO Joakim Weidemanis｜customer：主要資料中心客戶每週派工程師共同創新（原話："we have a major data center customer, hyperscaler or colo"）
- 2026-06-01｜CEO Joakim Weidemanis｜customer：目前沒有客戶從晶片端整套採購熱管理（原話："I couldn't think of a single example where somebody"）
- 2026-06-01｜CEO Joakim Weidemanis｜product：Alloy 技術將用於差異化 CDU，預計一年內上市（原話："That will happen within the next year in terms of when it"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜product：每台冷卻器能耗與客戶成本的下降幅度（原話："chiller that provide 50% less consumption, that are 25%"）
- 2026-06-01｜CEO Joakim Weidemanis｜product：液冷資料中心仍加裝更多空氣處理設備（原話："there are even more air handling"）
- 2026-06-01｜CEO Joakim Weidemanis｜competition：現場團隊規模為多數競爭對手兩倍以上（原話："twice the field footprint than many of the other people"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜competition：風冷與水冷冷卻器市場結構與18個月前預期不同（原話："people anticipated water to grow as a bigger share"）
- 2026-06-01｜CEO Joakim Weidemanis｜risk：全面導入需時，不能六個月內複製到各處（原話："can't copy paste and do everything in 6 months"）
- 2026-06-01｜CEO Joakim Weidemanis｜risk：CEO 自認過去未能快速釋放潛力（原話："have we really unlocked that at speed over the last years?"）
- 2026-06-01｜CEO Joakim Weidemanis｜risk：全公司約十萬人，轉型需時（原話："if you have 100,000 people, it takes a little while"）
- 2026-06-01｜CEO Joakim Weidemanis｜risk：CEO 稱成果已開始反映在損益表（原話："results are already starting to show up in the P&L"）

### 問答異常語氣（迴避／改口／保留）
- JCI_Q3_2026_Earnings_Call_20260729.md｜問：Ritchie：FY27 已有多少積壓訂單確定會在 FY27 出貨｜答法：CFO 回答資料中心占比與長期占比，未給 FY27 出貨比例數字
- JCI_Q3_2026_Earnings_Call_20260729.md｜問：Obin：Armada 模組產品的 TAM 與是否墊高 margin｜答法：CEO 稱 TAM 形成中而不給數字，未回答 margin 是否增厚
- JCI_Q3_2026_Earnings_Call_20260729.md｜問：Obin：策略檢討的時程｜答法：CEO 只說持續進展、會再通知，未給時程
- JCI_Q3_2026_Earnings_Call_20260729.md｜問：Mehrotra：Applied HVAC 能否進一步加速｜答法：CEO 談 pipeline 與產能，未直接給成長數字
- JCI_Q3_2026_Earnings_Call_20260729.md｜問：Snyder：冷水機、空氣處理、CDU 各自含量變動幅度｜答法：CEO 談方向，未提供各項幅度數字
- JCI_Shareholder_Analyst_Call_Johnson_Controls_International_plc_20260601.md｜問：Julian Mitchell：高個位數有機成長是否意味不需大型divest｜答法：回覆「沒有新消息」，改談投資組合像運動隊各有角色，未正面回答
- JCI_Shareholder_Analyst_Call_Johnson_Controls_International_plc_20260601.md｜問：Julian Mitchell：液冷如何影響設備汰換率｜答法：CEO 稱需要再想想，反問分析師看法，未給答案
- JCI_Shareholder_Analyst_Call_Johnson_Controls_International_plc_20260601.md｜問：Amit Mehrotra：增量利潤率30%是否保守｜答法：未給新數字，稱長期算式有「+」，近12–18個月會更好，未量化
- JCI_Shareholder_Analyst_Call_Johnson_Controls_International_plc_20260601.md｜問：Joe Ritchie：訂單轉成長的能見度｜答法：回覆訂單與積壓創新高、整體看好，未給轉換節奏或數字

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
{"date":"20260518","verdict":"A 觀望偏進場·thesis 完整但短 R:R 0.5x 偏緊，建議分批 / 等 BB 中軌 $132 或 Fwd PE 24x ~$135 回測","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Data Center thermal chain attach rate 結構性上升 + JCI share gain","columns":{"2Y 驗證點":"FY27 backlog 仍 > $22B + Applied HVAC 業務段 organic +15%/年","5Y 驗證點":"FY29 Adj EPS > $7.5（5Y CAGR 14%+）；ROIC 站回 10%+","10Y 驗證點":"FY35 Adj EPS > $14；ROIC stably > 13%","具體數字門檻":"Applied HVAC 業務段 organic growth ≥ 15%/年 至 FY27；Data Center 在 Applied HVAC 占比逐季提升","信息來源":"JCI 法說會 Q2/Q3 FY26 + Goldman Sachs Industrial 研究 ($154 PT，2026 Mar)","漂移觸發條件":"連 2 季 Applied HVAC organic"}},{"id":"H2","text":"Weidemanis 重整兌現：3 段式 operating model 重組釋放 efficiency","columns":{"2Y 驗證點":"FY27 Operating Margin > 13.5%（FY25 12.0% → FY26 estimate 13.0%）","5Y 驗證點":"FY29 ROIC > 10%；Adj FCF conversion > 100% sustained","10Y 驗證點":"FY35 ROIC > 13%（Danaher track 對標）","具體數字門檻":"FY26 Operating Margin guidance ≥ 13%；FY27 ROIC ≥ 8.5%","信息來源":"FY26 Q2 法說會 Weidemanis 重整進度 + Danaher 過去 5 年 track（10-K）","漂移觸發條件":"FY27 ROIC"}},{"id":"H3","text":"估值維持 5Y 中位區間（Fwd PE 24-28x），不被市場壓縮回 peer 19x","columns":{"2Y 驗證點":"NTM Fwd PE 在 24-30x 區間 sustained（不下破 23x）","5Y 驗證點":"5Y Fwd PE 中位仍 ≥ 25x","10Y 驗證點":"—（10Y 估值難以預測）","具體數字門檻":"NTM Fwd PE 不破 23x（vs peer 中位 19x，溢價 ≥ 20%）","信息來源":"Macrotrends 5Y PE 歷史 + Trefis 同業比較研究（2026 Feb）","漂移觸發條件":"連 2 季 Fwd PE"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Data Center capex cycle 提前見頂（GPU 供應飽和、power 約束限制新建、AI 投資 ROI 質疑）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"Hyperscaler capex 季度 YoY、JCI 訂單 Applied HVAC 業務段 organic growth","警戒閾值":"JCI Applied HVAC organic"}},{"id":"R2","text":"Weidemanis 三段式重整卡關（中層抵制、文化錯位、執行延期）","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"季度 Adj EPS Beat/Miss、Operating Margin 軌跡、ROIC 滾動值","警戒閾值":"FY27 Operating Margin"}},{"id":"R3","text":"估值溢價收斂回 peer 中位（同業 TT/CARR 也搶 AI 順風股，JCI 失去獨特性）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"JCI vs TT/CARR Fwd PE 差距、買方 sell-side downgrade 數量","警戒閾值":"JCI Fwd PE 跌至 22x 以下 + sell-side downgrade ≥ 3 家"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":143.08,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JCI_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
