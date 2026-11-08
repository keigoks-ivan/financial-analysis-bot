你是 stock-analyst **v20 判斷 agent**，標的 QCOM（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"QCOM","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/QCOM_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/QCOM_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"GAAP 營收","value":10322,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營收","value":10442,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm"},"note":"公司指引 9.7–10.5B 高端（共識數字未查）"},{"id":"f_kpi2_non_gaap","label":"Non-GAAP 營業利益／利益率","value":2769,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","unit":"USD M（利益率 26.5%，÷non-GAAP 營收 10,442）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm"}},{"id":"f_kpi3_gaap","label":"GAAP 營業利益／利益率","value":1356,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","unit":"USD M（利益率 13.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm"}},{"id":"f_kpi6_qct","label":"QCT 手機營收","value":5137,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm"}},{"id":"f_kpi7_qct","label":"QCT 車用營收","value":1990,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm"}},{"id":"f_kpi8_qct_iot","label":"QCT IoT 營收","value":1888,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm"}},{"id":"f_kpi9_qtl","label":"QTL 授權營收","value":1304,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm"}},{"id":"f_kpi10_q1_fy2027","label":"指引：Q1 FY2027","value":null,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","unit":"營收 10.4–11.2B；QCT 9.0–9.6B；QTL 1.3–1.5B；GAAP EPS 1.03–1.23；non-GAAP EPS 2.15–2.35","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm"},"needs_sonnet":true},{"id":"f_kpi11_fy2027","label":"指引：FY2027 全年定性","value":null,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","unit":"非手機營收 YoY >60%；資料中心營收目標 5B；定價調整效益於 FY27 下半年反映在 QCT 毛利率","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm"},"needs_sonnet":true},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_qcom_gross_margin_pct","label":"QCOM 毛利率","value":53.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_qcom_operating_margin_pct","label":"QCOM 營業利益率","value":20.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_qcom_fcf_margin_pct","label":"QCOM FCF 利潤率","value":20.06,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_2454_tw_gross_margin_pct","label":"2454.TW 毛利率","value":46.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2454.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2454_tw_operating_margin_pct","label":"2454.TW 營業利益率","value":15.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2454.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2454_tw_fcf_margin_pct","label":"2454.TW FCF 利潤率","value":13.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2454.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_gross_margin_pct","label":"NVDA 毛利率","value":74.67,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_operating_margin_pct","label":"NVDA 營業利益率","value":65.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_fcf_margin_pct","label":"NVDA FCF 利潤率","value":41.92,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nxpi_gross_margin_pct","label":"NXPI 毛利率","value":56.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NXPI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nxpi_operating_margin_pct","label":"NXPI 營業利益率","value":28.55,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NXPI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nxpi_fcf_margin_pct","label":"NXPI FCF 利潤率","value":24.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NXPI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_q4","label":"自由現金流（Q4 單季，推算）","value":1824,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm（稿內無單季現金流欄；Q4＝全年減前九個月，其中前九個月取自 Q3 稿 https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000085/qcom062826erex991.htm；自行推算）"}},{"id":"f_kpi5_sbc_non_gaap","label":"SBC 占 non-GAAP 營業利益","value":31.5,"period":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","unit":"%（SBC 873M ÷ 2,769M；占 GAAP 營收 8.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）","citation":"公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":165.41,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-23.81,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":44.31,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.16 → 10.16）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.85 → 12.85）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（17.84 → 17.84）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":10.16,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":12.85,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":17.84,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-3.51,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 10.53 → 10.16（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":13.02,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.1,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝58.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":58.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.3,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝59.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":59.4,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":16.28,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 10.16，分子＝快照價 165.41","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.189,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":8311.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 15992.0、現金 7681.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1070.0,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":185299.7,"period":"2026-11-08","unit":"USD m","basis":"市值 176988.7 ＋ 淨負債 8311.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":45419.02,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":52466.94,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（29 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.08,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 165.41 / W52 168.97 / W104 160.8 / W250 144.06 / W250 13週斜率 0.09%"},{"id":"f_ma_w52","label":"52 週均線","value":168.97,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":160.8,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":144.06,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.09,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Counterpoint：Qualcomm 智慧手機晶片出貨份額 Q1 2026 為 23%，較 2025Q1 的 27% 下滑；MediaTek 32%（前年 38%），Apple 19%（前年 15%）。","source":"Counterpoint Research 數據，經 Malaysian Wireless 報導 (MediaTek leads smartphone chipset market Q1 2026)","url":"https://www.malaysianwireless.com/2026/06/mediatek-leads-smartphone-chipset-market-q1-2026/","excerpt":"Qualcomm remained the second-largest smartphone chipset vendor with 23% market share in Q1 2026, down from 27% a year earlier. Apple ranked third with 19% market share in Q1 2026, up from 15% in Q1 2025.","as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Apple 自研 C1 數據機已上市，Reuters 報導 Qualcomm 在 Apple 數據機的份額預期從 100% 降至最低約 20%。","source":"Reuters 經 Telecoms Tech News (iPhone C1 modem chip to cut Apple's Qualcomm reliance by 80%)","url":"https://www.telecomstechnews.com/news/iphone-c1-modem-chip-to-cut-apples-qualcomm-reliance-by-80/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"資料中心：搜尋僅見 Humain 為 AI200 唯一具名客戶（約 200MW）；Meta 為 CPU 協議；Qualcomm 2026-06-24 投資人日目標資料中心營收由 FY26 $0.3B 增至 FY29 逾 $15B；對手為 Nvidia、AMD。","source":"Crypto Briefing / YourStory 報導 Qualcomm 投資人日與 AI200","url":"https://cryptobriefing.com/qualcomm-investor-day-2026-data-center-revenue-target/","excerpt":null,"as_of":"2026-06-24","retrieved_at":"20261108","affects":["thesis.H","triggers"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因子：Apple 歷來為 QCOM 最大客戶之一，但公司預期 Apple 今後將主要使用自家內部開發的 modem，而非 QCOM 產品。","source":"SEC EDGAR QCOM 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm","excerpt":"For example, Apple has historically purchased our modem products for use in its devices and has historically been one of our largest customers, but we expect that Apple will primarily use its own internally developed modem products, rather than our products, in its devices going forward.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K：部分最大客戶過去、現在及未來可能使用競爭對手晶片，且已開發或正開發自家積體電路產品（實質成為競爭者）；中國客戶亦有自研或改用競品。","source":"SEC EDGAR QCOM 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm","excerpt":"Certain of our largest customers have in the past used, currently use and may in the future use our competitors’ integrated circuit products in some or all of their devices, rather than our products. Further, certain of those customers have developed, are developing or may develop their own integrated circuit products (effectively making them competitors)","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 10-K：Apple 與 Samsung 各占合併營收 10% 以上；少數客戶/授權對象歷來占營收大部分。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm","excerpt":"A small number of customers/licensees historically have accounted for a significant portion of our consolidated revenues. In fiscal 2026, revenues from Apple and Samsung each comprised 10% or more of our consolidated revenues.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"10-K 風險因子：公司預期 Apple 未來主要使用自研數據機，對 QCT 營收、損益與現金流有重大負面影響；Samsung、小米亦自研晶片。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm","excerpt":"we expect that Apple will primarily use its own internally developed modem products, rather than our products, in its devices going forward, which will have a significant negative impact on our QCT revenues, results of operations and cash flows.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Moody's 確認 Qualcomm A2 發行人與優先無擔保債評等、展望穩定（發布日未核）。","source":"Moody's Ratings via researchpool","url":"https://app.researchpool.com/provider/moodys-investors-service/qualcomm-inc-qcom-moodys-ratings-affirms-qualcomms-a2-rating-outlook-stable-DaHDvpOtNq","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Counterpoint 預測 2026 智慧型手機出貨 −13.9% 至 10.8 億支、史上最大年減，復甦要到 2027 年底新增記憶體產能上線；IDC 預測 −12.9%。","source":"Counterpoint／IDC（經 thestar.com.my、91mobiles 等轉載）","url":"https://www.thestar.com.my/tech/tech-news/2026/09/16/smaller-phone-and-laptop-makers-dig-in-for-years-of-memory-scarcity","excerpt":"Counterpoint forecast smartphone shipments would fall 13.9 per cent this year to 1.08 billion units, the steepest annual decline on record.","as_of":"2026-09-16","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"三星稱 2027 年供需缺口可能比 2026 更大；SK hynix 預期記憶體緊缺 2027 見頂、延續至 2030；新產能多自 2028 起（來源含轉載，數字不一）。","source":"Tom's Hardware／PhoneArena 報導 Samsung、SK hynix 說法","url":"https://www.tomshardware.com/tech-industry/artificial-intelligence/samsung-and-sk-hynix-warn-ai-driven-memory-shortages-could-last-until-2027-and-beyond-as-hbm-demand-explodes-customers-already-reserving-supply-years-ahead-while-the-wider-dram-market-begins-to-tighten","excerpt":"Samsung and SK Hynix warn AI-driven memory shortages could last until 2027 and beyond as HBM demand explodes","as_of":"2026-06-03","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"高通 FY26 Q1 財報（2026-02）：Q2 營收指引 102–110 億美元低於共識；管理層指記憶體短缺與漲價將影響手機市場整個財年，並可能延到 2027；中國 OEM 削減機型生產與通路庫存。","source":"Qualcomm FY26 Q1 業績（經 The Star／Yahoo Finance 報導）","url":"https://www.thestar.com.my/tech/tech-news/2026/02/05/qualcomm-arm-bear-brunt-of-memory-shortage-as-smartphone-chip-sales-disappoint","excerpt":"Qualcomm, Arm bear brunt of memory shortage as smartphone chip sales disappoint","as_of":"2026-02-05","retrieved_at":"20261108","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"WSTS 2026 春季預測：2026 全球半導體市場約 1.51 兆美元、2027 約 1.9 兆美元（+約 27%），記憶體為主要驅動（2027 約 1.06 兆）。","source":"TelecomLead 報導 WSTS 預測","url":"https://telecomlead.com/semiconductor/wsts-raises-semiconductor-forecast-market-to-reach-1-51-trillion-in-2026-grow-to-1-9-trillion-in-2027-126102?noamp=mobile","excerpt":"WSTS Raises Semiconductor Forecast: Market to Reach $1.51 Trillion in 2026, Grow to $1.9 Trillion in 2027","as_of":"2026-06-02","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"MITRE：晶圓廠從動工到量產約 2.5 年，2026 起新增成熟製程產能有限。","source":"MITRE","url":"https://www.mitre.org/news-insights/publication/current-and-future-state-legacy-semiconductor-manufacturing-capacity","excerpt":null,"as_of":"2024-05-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"QCOM 10-K FY2026 風險因素：公司過去及目前仍受多項政府調查／法律程序，不利結果可能導致降低權利金率、授權晶片商、修改商業做法等補救，且單一國家的處分效力可能延伸至境外。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm","excerpt":"We have been in the past and currently are subject to various governmental investigations and/or legal proceedings.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 載明專利授權做法的調查或訴訟可能迫使公司未來改變授權做法。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm","excerpt":"Governmental investigations and/or legal proceedings could require us to change our patent licensing practices in the future","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"2026 年搜尋結果中，反壟斷行動的對象是 Arm 而非 QCOM：Qualcomm 向全球監管機關對 Arm 發動反壟斷行動（Bloomberg 報導），FTC 於 2026-05 對 Arm 授權做法展開調查。搜尋未見 2026 年 DOJ／FTC／EU 對 QCOM 本身的新行動。","source":"WebSearch 摘要（Reuters 2026-05-15 報導轉述；Bloomberg）","url":"https://stocktwits.com/news-articles/markets/equity/qualcomm-reportedly-takes-antitrust-battle-against-arm-to-regulators/chJGyX8Rb3i","excerpt":"Qualcomm has launched a global antitrust campaign against Arm","as_of":"2026-05-15","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"QCOM 10-K FY2026 風險因素：美中貿易保護與實體清單等政策已經、目前並可能限制或阻止與中國客戶／供應商交易；因對中國營收集中，進一步限制或中國關稅可能對業務、營運結果、現金流造成重大損害。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm","excerpt":"Given our revenue concentration in China, if, due to actual, threatened or potential U.S. or Chinese government actions or policies: we were further limited in, or prohibited from, selling our integrated circuit products to Chinese or Chinese-affiliated customers;","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K MD&A：公司持續監控關稅，影響取決於不確定的後續發展，可能衝擊需求、定價與成本，並導致呆滯庫存或準備金認列。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm","excerpt":"Changes to global trade policies may negatively impact demand, pricing and cost for our products and technologies, and contribute to the inherent uncertainties in estimating future customer demand, which may result in increased excess or obsolete inventory or reserve charges, negatively impacting our results of operations and cash flows.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-01 美國 Section 232 公告對符合特定性能門檻的先進半導體課 25% 關稅（2026-01-15 生效），搜尋結果未點名 QCOM 產品；後續可能擴大。","source":"EY Tax News: US Section 232 proclamation imposes 25 percent tariff on certain semiconductors","url":"https://taxnews.ey.com/news/2026-0209-us-section-232-proclamation-imposes-25-percent-tariff-on-certain-semiconductors","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Section 232 半導體 25% 關稅適用範圍為特定先進晶片（如 H200、MI325X），QCOM 未被點名","source":"GHY: U.S. Imposes 25% Tariff on Semiconductors Under Section 232","url":"https://www.ghy.com/trade-compliance/us-25-percent-tariff-semiconductors-section-232/","excerpt":"Imposes 25% Tariff on Semiconductors Under Section 232 Trade Update • Jan. 15, 2026 Key Points 25% ad valorem tariff on certain advanced semiconductors and derivative products takes effect January 15, 2026.","as_of":"2026-01-15","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K 風險因素：關鍵晶圓代工與封測夥伴集中在台灣與韓國，RF 製造在中國、德國、新加坡；中台嚴重或長期衝突可能切斷台灣晶片供應，對業務有重大不利影響（依搜尋摘要轉述，未核全文）","source":"SEC EDGAR QUALCOMM Form 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000128/qcom-20260927.htm","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 中國占營收 46%（依客戶總部，Nikkei 經 TrendForce 轉述）；Qualcomm 10-Q 載明美國撤銷對華為出口許可，不再預期華為產品營收，並提及中國資本流動規則可能延遲客戶付款","source":"TrendForce News 2026-06-25 / SEC 10-Q 2026-06-28","url":"https://www.trendforce.com/news/2026/06/25/news-qualcomm-reportedly-plans-china-ai-chip-push-with-export-control-compliant-custom-chips/","excerpt":null,"as_of":"2026-06-25","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"FY2026 Q4（季末2026-09-27）手機營收約$5.137B、年減26%；車用$1.99B（年增89%）；IoT$1.888B（年增4%）；車用＋IoT合計年增36%。來源為搜尋摘要彙整，未逐字核對","source":"xenospectrum / 247wallst 搜尋摘要","url":"https://xenospectrum.com/en/qualcomm-fy2026-q4-nonhandset-gap/","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"2026年7月：CEO稱Apple相關營收自FY Q4起下滑，下一代iPhone的高通份額遠低於先前估計的20%；專利授權至少收到2027年3月","source":"iClarified / MacRumors 報導","url":"https://www.iclarified.com/101624/qualcomm-says-apple-modem-revenue-will-fall-faster-than-expected","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"WSTS 2026春季預測：2026全球半導體約$1.51兆（+89.9%），2027約$1.9兆（+27%），記憶體為主因","source":"WSTS FC Release 2026 May / TelecomLead","url":"https://telecomlead.com/?p=126102","excerpt":null,"as_of":"2026-06-02","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"FY2026 Q4分部營收：手機$5.137B、車用$1.99B、IoT$1.888B","source":"Qualcomm 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000128/qcom-20260927.htm","excerpt":"The decrease in QCT revenues in fiscal 2026 was primarily due to: - lower handsets revenues, primarily due to lower chipset shipments to certain major OEMs (primarily driven by customers adjusting build plans to reduce their inventory levels as a result of the negative effects of recent memory supply constraints and related price increases)","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"WSTS 2027預測$1.9兆、+27%","source":"WSTS FC Release 2026 May","url":"https://www.wsts.org/esraCMS/extension/media/f/WST/7618/WSTS_FC-Release-2026-May.pdf","excerpt":null,"as_of":"2026-06-02","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 稱 QCT 面臨客戶內部自研產品的競爭（含最大客戶），並將客戶垂直整合列為風險因子；也與替代通訊技術競爭。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm","excerpt":"QCT also faces competition, which may intensify in the future, from products internally developed by our customers, including some of our largest customers.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子列出「客戶垂直整合（自行開發積體電路產品）可能損害半導體業務」。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm","excerpt":"Our business, particularly our semiconductor business, may suffer as a result of our customers vertically integrating (i.e., developing their own integrated circuit products).","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Apple 自研 C1 系列數據機已用於 iPhone 16e、iPhone Air、iPad Pro，取代高通晶片；高通稱非 Apple QCT 營收成長 18%。","source":"MacRumors: Qualcomm Now Relies on Android as Apple Modems Roll Out","url":"https://www.macrumors.com/2025/11/06/qualcomm-now-relies-on-android/","excerpt":"(QCT), apparently recorded strong year-over-year growth in the fourth quarter of fiscal 2025, led by rising Android device sales and increasing chip content per device. DigiTimes cited remarks from President and CEO Cristiano Amon, who said that non-Apple QCT revenue rose by 18% during the quarter.","as_of":"2025-11-06","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 10-K 將「配銷通路的成長與擴展」列為 QCT 的主要競爭因素之一；文件該段未描述通路或商業模式的結構性轉變。","source":"SEC EDGAR 10-K FY2026 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm","excerpt":"We believe that the principal competitive factors for our products include performance, level of integration, quality, compliance with industry standards, price, time-to-market, system cost, design, engineering and supply chain capabilities, new product innovation, growth and scaling of distribution channels","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"高通收購 Arduino（獨立子公司運作），取得創客與早期機器人公司的直接接觸管道","source":"Yahoo Finance: Qualcomm to acquire Arduino amid edge computing push","url":"https://finance.yahoo.com/news/qualcomm-to-acquire-arduino-amid-edge-computing-push-130012919.html","excerpt":null,"as_of":"2025-10-07","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"FY26 Q4（2026-11-04 公布）Q1 FY27 指引：營收 $10.4B–$11.2B、non-GAAP EPS $2.15–$2.35；QCT $9.0–9.6B、QTL $1.3–1.5B；資料中心併入 QCT 指引，使 Q1 QCT EBT 利潤率指引減 3 個百分點；公司重申 FY27 資料中心 $5B 目標。","source":"Qualcomm FY2026 4th Quarter Earnings Release / SEC 8-K","url":"https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"二手報導：財報後盤後股價跌約 6%，因手機晶片營收年減 26%（記憶體成本壓力）、前瞻指引偏弱；單一來源未證實。分析師共識與此指引的落差數字本次搜尋未查到。","source":"AI Weekly: Qualcomm Q4 Revenue Drops 8% to $10.3B, Guides $5B Data-Center Revenue in Fiscal 2027","url":"https://aiweekly.co/alerts/qualcomm-q4-revenue-drops-8-to-103b-guides-5b-data-center-revenue-in-fiscal-2027","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價共識為 Hold；Tickflow 頁面（約 2026-08-01）56 位分析師平均目標價 $216；MarketBeat 經 Capital.com 引用 2026-07-21 為 $219.76（38 位）；Barchart 財報前為 $215.50；MarketBeat 另頁 $184.29（34 位，區間 $120–$300，日期不明）。各來源口徑與日期不一，均早於 11-04 財報，無財報後共識。","source":"Tickflow / Capital.com / Barchart / MarketBeat 搜尋摘要","url":"https://www.tickflow.io/stock/QCOM/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Argus 2026-05-01 目標價由 $180 調至 $220，維持 Buy。","source":"Placera/Telegram: Argus Adjusts Price Target on QUALCOMM to $220 From $180","url":"https://www.placera.se/telegram/argus-adjusts-price-target-on-qualcomm-to-220-from-180-maintains-buy-rating-20260501","excerpt":"Argus Adjusts Price Target on QUALCOMM to $220 From $180, Maintains Buy Rating MT Newswires 1 maj, 15:00 Dela","as_of":"2026-05-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06-21 Qualcomm 簽約收購 Modular Inc；以 17,826,566 股普通股作價，2026-07-31 提交轉售招股補充說明書。","source":"SEC EDGAR 8-K Item 8.01 (2026-07-31)","url":"https://www.sec.gov/Archives/edgar/data/804328/000110465926089234/tm2621612d2_8k.htm","excerpt":"As previously announced, on June 21, 2026, the Company entered into a definitive agreement to acquire Modular Inc (“Modular”). The Company issued such 17,826,566 Shares as consideration for the acquisition of Modular in a private placement","as_of":"2026-07-31","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 11 份 8-K 中僅 1 份含重大項目（即 Modular 相關 8.01），無 4.02 重編類項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000804328&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-06-21 簽約收購 Modular Inc，以 17,826,566 股普通股作價。","source":"SEC EDGAR 8-K Item 8.01 (2026-07-31)","url":"https://www.sec.gov/Archives/edgar/data/804328/000110465926089234/tm2621612d2_8k.htm","excerpt":"As previously announced, on June 21, 2026, the Company entered into a definitive agreement to acquire Modular Inc (“Modular”). The Company issued such 17,826,566 Shares as consideration for the acquisition of Modular in a private placement","as_of":"2026-07-31","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單無 Item 4.02（財報不可信賴）；唯一重大項目為 Modular 相關 8.01。搜尋亦只見 2016 年已和解的 FCPA 案。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000804328&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"QCOM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":53.1,"operating_margin_pct":20.08,"fcf_margin_pct":20.06,"rd_intensity_pct":23.67},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"2454.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":46.28,"operating_margin_pct":15.13,"fcf_margin_pct":13.34,"rd_intensity_pct":25.83},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2454.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"NVDA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.67,"operating_margin_pct":65.21,"fcf_margin_pct":41.92,"rd_intensity_pct":7.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"NXPI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.43,"operating_margin_pct":28.55,"fcf_margin_pct":24.16,"rd_intensity_pct":17.92},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NXPI","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"QCOM"},"financial_history":{"ticker":"QCOM","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-09-30","revenue":35820000000.0,"revenue_yoy_pct":null,"gross_margin_pct":55.7,"operating_margin_pct":24.15,"net_income":7232000000.0,"diluted_eps":6.42,"free_cash_flow":9849000000.0,"fcf_margin_pct":27.5,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-09-30","revenue":38962000000.0,"revenue_yoy_pct":8.77,"gross_margin_pct":56.21,"operating_margin_pct":25.85,"net_income":10142000000.0,"diluted_eps":8.97,"free_cash_flow":11161000000.0,"fcf_margin_pct":28.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-09-30","revenue":44284000000.0,"revenue_yoy_pct":13.66,"gross_margin_pct":55.43,"operating_margin_pct":27.9,"net_income":5541000000.0,"diluted_eps":5.01,"free_cash_flow":12820000000.0,"fcf_margin_pct":28.95,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-09-30","revenue":43120000000.0,"revenue_yoy_pct":-2.63,"gross_margin_pct":53.1,"operating_margin_pct":20.08,"net_income":13628000000.0,"diluted_eps":12.7,"free_cash_flow":8651000000.0,"fcf_margin_pct":20.06,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/QCOM/QCOM_Q4_2026_Earnings_Call_20261104.md）

# Q4 2026 Earnings Call
**QUALCOMM Incorporated** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Ladies and gentlemen, thank you for standing by. Welcome to the Qualcomm Fourth Quarter Fiscal 2026 Earnings Conference Call. [Operator Instructions] As a reminder, this conference is being recorded November 4, 2026. The playback number for today's call is (877) 660-6853. International callers, please dial (201) 612-7415. The playback reservation number is 13762625.
I would now like to turn the call over to Brett Simpson, Senior Vice President of Investor Relations. Mr. Simpson, please go ahead.

**Brett Simpson** (Executives):
Thank you, and good afternoon, everyone. Today's call will include prepared remarks by Cristiano Amon and Akash Palkhiwala. In addition, Alex Rogers will join the question-and-answer session. You can access our earnings release and a slide presentation that accompany this call on our Investor Relations website. In addition, this call is being webcast on qualcomm.com, and a replay will be available on our website later today.
During the call today, we will use non-GAAP financial measures as defined in Regulation G, and you can find the related reconciliations to GAAP on our website. We will also make forward-looking statements, including projections and estimates of future events, business or industry trends or business or financial results. Actual events or results could differ materially from those projected in our forward-looking statements. Please refer to our SEC filings, including our most recent 10-K, which contain important factors that could cause actual results to differ materially from the forward-looking statements.
And now to comments from Qualcomm's President and Chief Executive Officer, Cristiano Amon.

**Cristiano Amon** (Executives):
Thank you, Brett, and good afternoon, everyone. In fiscal Q4, we delivered non-GAAP revenues of $10.4 billion and non-GAAP earnings per share of $2.17. QCT revenues of $9 billion, up 6% sequentially, were at the high end of our guidance. Licensing business revenues were $1.3 billion. For fiscal '26, we reported non-GAAP revenues of $43.2 billion and QCT revenues of $37.2 billion, highlighted by year-over-year revenue growth of 24% across combined automotive and IoT.
We closed fiscal '26 with many of the uncertainties that have been weighing on our business now behind us, specifically QTL license renewals, the loss of Apple as a customer and the negative impact of memory pricing on the size of the mobile industry. Regarding the latter, the June quarter marked the low point for our China Android business, and we have seen sequential growth this quarter. Going forward, our plan assumes global handset units will remain flat to down in calendar '27. The timing and shape of the Apple modem transition is fully incorporated in how we're planning the business and is well understood at this point. We also renew important QTL licensing agreements, including Apple and Huawei.
Now we enter fiscal '27 as a broader, more diversified Qualcomm with strong momentum and significant opportunities ahead. First, non-handset revenues in QCT will grow by more than 60% year-over-year. Second, our data center business begins its ramp with revenues expected to exceed $650 million in the December quarter. Third, automotive revenues reached an $8 billion annualized run rate exiting fiscal '26, $1 billion ahead of expectations. Fourth, we established a solid foundation in how agentic AI transforms the edge and leads to new product categories for Qualcomm. And finally, we reached a landmark agreement with SpaceX to power their nationwide terrestrial 5G network in the U.S.
Our technology investments are aligned with the direction the industry is moving. We've made key acquisitions to build on our hardware and software capabilities as we evolve into a full stack semiconductor company. We announced strategic agreements with industry leaders, including Meta, Amazon, BMW and Stellantis with more to come, and our design win pipeline across the company grew 70% year-over-year. This is the backdrop that positions Qualcomm to deliver on our fiscal '29 targets of $40 billion in non-handset revenues with over $15 billion coming from data center.
Now I will focus on the areas that are top of mind for investors. Let me start with licensing, where we reached a milestone this quarter. We're extremely pleased with our renewals with Apple, Huawei and Transsion. These agreements provide stability for QTL as we move to the 6G era. They also demonstrate the enduring value of our IP and patent portfolio. And just as in every prior generation, we expect our inventions to be foundational to 6G. Importantly, our QTL revenue run rate remains unchanged. The next renewal cycle begins in fiscal 2030 and runs through fiscal 2033. Licensing gives Qualcomm a durable, highly profitable foundation as we scale our next set of growth opportunities.
Data center is another area where we made considerable progress this quarter. It's one of our top strategic priorities and a major focus of my own time as we build this business around long-term customer relationships, a broad product portfolio and an open software ecosystem. AWS is a good example. Our agreement spans multiple product generations across custom silicon for AI inference and optical connectivity. Custom accelerators began shipping in October and our connectivity solutions with AWS ramp later this month. We also secured a second optical connectivity customer. With Qualcomm High Bandwidth Compute, our AI250 silicon is exceeding our expectations for power efficiency and bandwidth and early yields are on track. These results are generating significant interest from AI customers and memory partners, and we added 2 major prospects in the quarter.
Our Dragonfly C1000 CPU remains on track to ship to Meta as scheduled, and we engage with a large new potential customer. We're optimistic about the opportunities we have today with our high-speed connectivity solutions such as optical DSPs, and we are investing in bringing optics directly alongside our XPUs and custom silicon as we demonstrated with Lumentum and Corning at ECOC 2026. In software, our full stack integration with Modular is progressing well. Modular is delivering impressive performance as an open multi-vendor stack running on NVIDIA and AMD GPUs, Amazon Trainium and Google TPU. Optimization for Qualcomm accelerators is also underway. Last month, Modular made the full MAX source code available, and this builds on open sourcing the Mojo language in August. We're also excited that Modular Cloud went live during the September quarter and is already processing tens of trillions of tokens per month. We'll share more details soon about how our ecosystem partners are using Modular Cloud.
Our data center business is off to a strong start. We are reiterating our $5 billion revenue target for fiscal '27 with healthy order coverage supporting continued revenue growth in fiscal '28. In automotive, we exit fiscal '26 at an annualized revenue run rate of approximately $8 billion, well above the $7 billion expectations we provided last quarter. Additionally, fiscal fourth quarter automotive revenue grew nearly 90% year-over-year. Commercial shipments of our fifth-generation Snapdragon Digital Chassis began in the September quarter and will continue to ramp in fiscal 2027. As a reminder, this platform is our most advanced to date, delivering a significant increase in performance and represents our largest generation-to-generation content increase in Qualcomm's history.
Our products also evolve from SoCs to integrated compute modules. Customer demand remains strong across our portfolio, and Qualcomm is positioned to become one of the largest automotive semiconductor suppliers by revenue in fiscal 2027. In robotics, our premium tier Dragonwing IQ10 processor is set to begin its commercial ramp and continues to generate strong customer momentum. During the quarter, ecosystem partners demonstrated AI models of up to 80 billion parameters running directly on IQ10. In fiscal 2027, we will continue to expand the technologies and capabilities across our robotics platforms. As we anticipated, the proliferation and capability of AI agents is increasing rapidly, and we're seeing growing consumer adoption as a result. A prime example is Meta Muse, which reached over 10 million downloads in just 40 days.
We're also seeing more companies designing experiences and devices around agents. This includes agentic smartphones, smart glasses and other new personal AI form factors. Meta's Audio AI glasses, Muse Charm, Gemini eyewear and Alibaba's Qwen AI glasses are recent examples of intelligent wearables with more to come over the next year. The smartphone is an essential device for agentic experiences as it's the device that knows people best. It's always with them and has their context, preferences and permissions. The device is also evolving to simultaneously support what the user is doing and what agents are doing on the user's behalf. Delivering these experiences will require greater computing performance, power efficiency and connectivity, which play directly to Qualcomm's strengths. More of our customers are already building agentic features into their flagship devices, and we're pleased to share that the world's first agentic smartphones were launched on Snapdragon.
Heading into fiscal 2027, we're pleased with our premium tier Android share position, and we expect it to strengthen as the transition to agentic smartphones drive an increase in computing content per device. For perspective, leading AI companies are targeting smartphones by 2028, capable of running 100 billion parameter models locally with an all-day battery life. Reaching this goal will require a step function change in on-device compute performance. Finally, I'm very proud to share that SpaceX selected Qualcomm to power Starlink Mobile's nationwide terrestrial 5G network in the U.S.
Starlink is building one of the most ambitious new cellular networks in the country, and our Dragonwing infrastructure platforms will bring together advanced massive MIMO purpose-built RAN processing and commercial-grade Layer 1 software. Under a multiyear agreement, deployment begins in 2027 and is expected to be one of the largest 5G deployments in the United States. Together, we have an opportunity to advance United States wireless leadership, starting with 5G and the convergence of satellite and terrestrial connectivity. This new architecture establishes a foundation for next-generation connectivity and network intelligence. This is a significant win for our infrastructure business and the beginning of a strategic relationship with tremendous potential.
Before I close, I would like to briefly address our litigation with Arm. We're gratified that the jury found Arm breached its long-standing Architectural License Agreement, ALA, with Qualcomm, failed to honor its commitments, intentionally acted to disrupt Qualcomm's business and engage in unfair competition, both as a supplier and a competitor. Together with Qualcomm's prior court victory, this outcome further exposes Arm's intentions to harm Qualcomm and its ecosystem. This outcome is a victory for innovation and competition, and we remain focused on developing and delivering industry-leading semiconductor products, including our Oryon CPUs to customers and consumers worldwide from mobile to data center.
In summary, we enter fiscal 2027 having made important progress against the ambitious growth plan we outlined at Investor Day. Since then, we've signed major strategic agreements and positioned our data center business to ramp at scale. We remain focused on execution as we build the next chapter for Qualcomm, and we're confident in delivering on our fiscal 2029 targets.
With that, I will turn it over to Akash.

**Akash Palkhiwala** (Executives):
Thank you, Cristiano, and good afternoon, everyone. Let me begin with our results for the fourth fiscal quarter. We delivered non-GAAP revenues of $10.4 billion and EPS of $2.17 with revenues at the high end of our guidance. QTL revenues of $1.3 billion and EBT margin of 70% were in line with our expectations. QCT revenues of $9 billion were at the high end of our guidance and EBT margin of 24% was in line with expectations. QCT handset revenues of $5.1 billion reflected the impact of industry-wide memory dynamics on the global smartphone market.
In QCT Automotive, we delivered our first $2 billion revenue quarter with 89% year-over-year growth, driven by the growing adoption of integrated module products for our fifth-generation compute platforms. QCT IoT revenues of $1.9 billion were up 4% year-over-year, led by our industrial, networking and robotics category of products, which grew 20% versus the year ago period, offset by the impact of memory constraints on consumer products. Total non-handset revenues in QCT, including Automotive and IoT, grew 36% year-over-year, underscoring the continued execution of our growth initiatives. Lastly, we returned $2 billion to stockholders, including $1 billion each in share repurchases and dividends.
Before turning to guidance, I'd like to provide an update on a couple of factors reflected in our financial performance. First, in QTL, we have now completed long-term license agreements with Apple, Huawei and Transsion and do not have any upcoming license renewals with major handset OEMs for the next several years. Following these agreements, QTL revenue run rate and long-term revenue forecast remains unchanged. Second, as we outlined last quarter, we are implementing price increases across our products to reflect the higher semiconductor input costs. We expect the full benefit of these actions to be reflected in QCT gross margins in the second half of fiscal '27. Finally, we're excited that fiscal '27 marks an important milestone for our data center business as we transition from customer engagements to revenue generation.
Our first fiscal quarter guidance reflects the commencement of shipments to 2 hyperscaler customers for custom silicon engagement. As we have discussed previously, we expect these custom silicon engagements to be accretive to QCT operating margins but dilutive to gross margins. These factors are reflected in our fourth quarter performance and first quarter outlook. I'll now provide our guidance for the first fiscal quarter. We are forecasting revenues of $10.4 billion to $11.2 billion and non-GAAP EPS of $2.15 to $2.35. In QTL, we estimate revenues of $1.3 billion to $1.5 billion and EBT margins of 72% to 76%, reflecting normal seasonal trends. In QCT, we expect revenues of $9 billion to $9.6 billion and EBT margins of 20% to 22%. Please note that QCT EBT margin guidance includes an impact of 3 percentage points due to the addition of Data Center in the QCT segment starting in fiscal '27 and reflects investments for AI accelerator and CPU platform ahead of revenue ramp.
Importantly, this segmentation change has no impact on total company guidance or on our long-term QCT EBT margin target of 30%. We forecast QCT handset revenues to decline by a mid-single-digit percentage sequentially as growth in Android revenues is offset by the continued ramp down in Apple product revenue. In QCT Data Center, we expect revenues of greater than $650 million, driven by commencements of shipments to custom silicon customers. We expect combined QCT Automotive and IoT revenues to be approximately flat sequentially. Lastly, we anticipate non-GAAP operating expenses to be approximately $2.8 billion in the quarter.
Before I conclude my prepared remarks, I'd like to outline the progress in the execution of our growth strategy. In fiscal '27, we expect to achieve 2 key milestones for revenue diversification. First, non-handset revenues in QCT across Automotive, IoT and data center will grow by greater than 60% on a year-over-year basis starting in the first fiscal quarter. Second, non-handset revenues will represent more than 50% of QCT revenues in the fiscal year. In data center, we're executing to the revenue targets we outlined at Investor Day, including $5 billion in fiscal '27 and $15 billion in fiscal '29. We expect Data Center revenues to scale throughout fiscal '27, exiting the year at a $7 billion run rate. We're also expanding our customer engagement pipeline across additional global hyperscalers, including the long-term strategic agreement with Amazon Web Services with a potential revenue opportunity of up to $60 billion over the next 10 years.
During the quarter, we also successfully validated our high-bandwidth compute technology in lab trials, marking a key milestone in delivering an innovative AI inference accelerator solution designed to address the memory bandwidth challenge in data centers. We are also well positioned to lead other key industry trends, including the transition to agentic AI in consumer devices and the adoption of physical AI across automotive, industrial and robotics. Finally, we would like to thank our employees for their exceptional execution and innovation throughout fiscal '26. Their commitment enables us to deliver industry-leading products to customers around the world.
This concludes our prepared remarks. Back to you, Brett.

**Brett Simpson** (Executives):
Thank you, Akash. Operator, we are now ready for questions.

**Operator** (Operator):
[Operator Instructions] The first question comes from the line of Joshua Buchalter with TD Cowen.

**Joshua Buchalter** (Analysts):
Maybe to start, I mean, last quarter, you guys kind of telegraphed the gross margin step down that was expected from the ASIC business starting to ramp. How should we think about it through the rest of the year, though? Because just the simple math of having to get to your $7 billion run rate exiting the year implies the data center business should grow close to 3x. Like should we expect gross margins to continue to trend down through the year as a result of the larger data center business and this being the year where custom silicon is ramping aggressively?

**Akash Palkhiwala** (Executives):
Josh, it's Akash. So let me kind of frame the overall gross margin framework for the company. As you know, we mentioned this last quarter, we are implementing price increases to reflect the higher semiconductor cost across the industry. And so we start realizing the benefit of that in our second fiscal quarter, and we'll see the full benefit of that show up in second half of '27. So the way it plays out is as these price increases come into effect, our baseline gross margin goes back to our historical range of 48% to 50% at the low end of that range.
And then separately, on your question on data center, we -- as we said previously, we expect that to be something that is accretive to our operating margins, but dilutive to gross margins. And so that calibrates the gross margin down from the framework I just outlined. So that's no different than what we told you last quarter, and we're executing on the plan.

**Joshua Buchalter** (Analysts):
And then maybe for my follow-up, it's good to see the HBC demos that you outlined earlier this week. Can you maybe speak to what type of workloads you're seeing the most traction for your accelerator parts initially? And then any updates on the commercial traction as we think about that? I think I believe that's supposed to start contributing and ramping in the fiscal second half of this year, which is kind of only a couple of quarters away at this point.

**Cristiano Amon** (Executives):
Thanks, Josh. This is Cristiano. Look, we're very happy with the progress we're making on HBC. We're actually doing better than what we said on Investor Day. We had a target on the design to about 0.5 picojoules per bit. We're doing better in the lab. We're doing about 0.3. Yield is exceeding our expectations. So we're very happy with the technology progress. The main workloads that we're getting a lot of traction, it's incredibly efficient for decode. So decode, it's where we're getting a lot of the positive feedback.
We are engaged with customers. It changes the conversation when you have a PowerPoint to where you have silicon. And I think that continues to build confidence in the projections we have, not only for our custom ASIC, but for our merchant solutions coming up as we think about 2029 targets. What is also interesting, it's now became part of the conversation of custom silicon with HBC, combining our HBC with some of our custom accelerators. So I would just say customer engagement is very positive.

**Operator** (Operator):
The next question is from the line of Joseph Cardoso with JPMorgan.

**Joseph Cardoso** (Analysts):
Maybe just wanted to start off first with happy for you guys to give us the disclosure around how to think about the Data Center revenue ramp through the year. Maybe can you just provide a little bit more color on how you're thinking about your customers and how they get paced into that revenue ramp through the year itself? And then maybe the second aspect there, too, is, I think in the past, you've talked about 2 customers. So can you provide any color on the third customer here that's mentioned in the slide deck and how you're thinking about that getting intertwined in the guidance that you provided for this year? Or does the third customer ramp at another point? And then I do have a follow-up.

**Akash Palkhiwala** (Executives):
Okay. Joseph, this is Akash. Let me address the financials and then Cristiano will comment on top -- on customer ramp. So for fiscal '27, we are looking at $5 billion revenue forecast that we've previously provided. We're guiding greater than $650 million in the first quarter, and we expect this revenue to ramp throughout the year as we go through the quarters and we'll exit the year at approximately a $7 billion exit rate going into '28. And so very happy with that. We will -- we're very well positioned from a supply perspective to execute on the $5 billion target. And really, we expect to be constrained by supply rather than demand for upsides beyond the $5 billion.
When you look at fiscal '28, we are looking at a $7 billion starting point. And then the customers that we have in '27 will extend to '28 as well, and it gives us really strong design win coverage to deliver very strong year-over-year growth in fiscal '28 as well. And then as you know, we have set a target of $15 billion for '29, which the customer engagements that Cristiano will outline right after this will position us very well to have a very high coverage of that number as well.

**Cristiano Amon** (Executives):
Just real quick, Joseph, on the customer. The majority of the $5 billion in fiscal '27 comes from the 2 hyperscaler customers, so one of them being Amazon. I think the details of those were made public on the custom silicon plus connectivity. We do have another customer on the accelerator and an advanced discussion also on subsequent custom silicon that is part of the ramp towards '28 and '29. And we had said in the script, I think we have new prospects, especially on the CPU as well, I think, beyond Meta, and we're working with the customers.

**Joseph Cardoso** (Analysts):
Got it. I appreciate the color there. And then maybe just wanted to double-click on how you guys are framing handset revenue kind of exiting the year and into next year. Specifically, how are you guys thinking about the growth here in terms of pricing layering on? I know it sounds like you're not expecting that to be in the period or to kind of tranche here over the subsequent quarters. But any more color you can help us think about how that pricing ends up influencing kind of the numbers here and the magnitude that we should be thinking about?
And then as a second question, just bigger picture. Obviously, when we look at the market data points on the handset market, it does seem like a contraction on kind of the memory prices has been something we've been witnessing through this year. Just any early thoughts on how you're thinking about the health of the market going into next year? I would appreciate it.

**Akash Palkhiwala** (Executives):
Yes. Joseph, when you look at the overall handset market, '25 to '26, as -- like other industry analysts, we are projecting a low teens to mid-teens decline in the market. And then as we go into '27, we're thinking flat to slightly down for the handset market. And that's how we've always projected our business based on that assumption, and it's playing out consistent with expectations. Specifically for QCT handset revenue in Android, as you'll recall, we called the June quarter the bottom for QCT handset revenues and Android in China. What has happened since is we've seen revenue grow into September and December quarter. And so we are encouraged to see that. We've been conservative in our planning, and it's playing out exactly as we'd expected.

**Operator** (Operator):
The next question is from the line of Joe Moore with Morgan Stanley.

**Joseph Moore** (Analysts):
In terms of the royalty rate, you sort of said that the revenue run rate of QTL is unchanged. Is that the rate per device kind of similar as you look at these new contracts that you signed? Is there any change there? I assume that's right, but I just want to make sure.

**Akash Palkhiwala** (Executives):
Yes, Joe, you should -- we obviously don't specifically talk about the details of the contract. They're confidential, but we are indicating that the revenue run rate remains the same, which you should take it as we were able to hold the rates and the royalties as we renewed the contracts.

**Joseph Moore** (Analysts):
Great. That's helpful. And then separately, on the Amazon deal, the warrant structure that you have there, do you view that as kind of the model for approaching other customers? Do you expect to have those types of warrant arrangements? Or is that unique to that specific relationship?

**Akash Palkhiwala** (Executives):
Well, if you look at our general set of engagements across data center, the engagements are very traditional, normal kind of customer engagements in the semiconductor industry. The Amazon warrant structure is the exception. And as you know, the warrants that we issued were at-the-money warrants. So that's the only exception that we have at this point. And I think as we consider data center engagements going forward, we'll look at other structures on a deal-by-deal basis, but you should think of our framework as being aligned with the traditional semiconductor model.

**Operator** (Operator):
The next question is from the line of Timothy Arcuri with UBS.

**Timothy Arcuri** (Analysts):
Akash, I was wondering if you can provide a little bit of maybe outlook into March. I know that you don't want to guide March. But I think last call, you thought that revenue would be up a little bit in March. You have easy comps for Apple into March. Android should be a little better. So can you just give us kind of just a sense on March would be great.

**Akash Palkhiwala** (Executives):
Yes. Tim, you're right. We are not guiding March at this point. But let me make a few comments on the year that I hope are helpful. The first is, typically in previous years, December has been our strongest quarter in the year. Now with Apple product revenue ramp down, we do not expect December to be the high quarter for us. When you look at Data Center revenue, we've talked about kind of greater than $650 million in the first quarter, but we expect that to ramp as we go through the year. So that kind of defines our quarterly profile to some extent.
The third is when you look at '26 to '27, we expect auto IoT plus Data Center kind of non-handset revenue to grow by greater than 60%. So this revenue would more than offset the decline in Apple product revenue. And then finally, I think if you look at to fiscal '27, we expect handset now to be less than 50% of our total revenue. And so obviously, that's a key milestone for our diversification plan, and so we are happy to achieve that this year.

**Timothy Arcuri** (Analysts):
Got it. So you don't want to -- I just asked because last call, you did sort of say that March would be up. I guess you don't want to commit to that now.

**Akash Palkhiwala** (Executives):
Yes. I think it's the reasonable framework that I think the way people have been looking at the business is a reasonable way of looking at it.

**Operator** (Operator):
Our next question is from the line of Stacy Rasgon with Bernstein Research.

**Stacy Rasgon** (Analysts):
I wanted to dig into your handset market outlook a little bit. I'm a little surprised still with the outlook for flat, especially given where we seem to be running at the end of the year, we're probably down more than 20% year-over-year increase here and things don't look better, don't look all that great in Q4. You also said your own China Android revenues were actually starting to grow in, I guess, June or September and December. You're also doing price increases. Like how do you know in the context of everything that's going on that, that's just not prebuys in front of the price increases in Android? I'm just struggling a little bit with the handset outlook. Any further color you could give on that would be super helpful for me.

**Akash Palkhiwala** (Executives):
Sure, Stacy. So let me break it down into 2 parts. Let's talk about the market and then separately talk about QCT product revenue within Android. Overall market, as I said earlier, our view is that '25 to '26, it's down low to mid-teens. And then '26 to '27, we are projecting flat to down for the total market. So we think that's a prudent assumption as we plan given the uncertainty overall in the environment.
Specifically on QCT revenue, as you'll recall, the impact we saw in '26 was not just from the change in the market, but also channel inventory drawdown by OEMs. And we don't expect that impact in '27 because we've been following channel inventory. As you know, we get QTL information as well that we can check against. And so the channel inventory continues to be thin. And so we expect kind of QCT revenue really to be aligned with the overall market, and that's how we are projecting it going forward.

**Cristiano Amon** (Executives):
Maybe, Stacy -- it's Cristiano, just to add another thing. One of the things we had said before. And that's kind of because of our long-term partnerships that we have with our customers. A lot of the price increases, the reason that they have a delta versus the cost increase, and we talk about prices become more effective in the numbers in the second half, we kind of been pricing newer platforms, new phones. So less subject to prebuying effect. And as Akash said, I think based on the data we're seeing in the market, June remains, I think, the bottom, I think, for China Android.

**Stacy Rasgon** (Analysts):
If I could ask one follow-up, please. You talked about Samsung market share framework, 75%. Is that still the framework share you have in mind for their -- your share with them in their next-generation platform that ramps in '27?

**Cristiano Amon** (Executives):
Yes, absolutely. So here's how we think about the Samsung business. And here's a simple way to do it. We have -- we -- if you think about our business in the past, the baseline was 50%. This baseline is no longer 50%. It's north of 70% as we have been doing. When you think about future generations of Galaxy, this is how we plan our business, and I encourage all of you to plan the same way. That's the new baseline with Samsung. The other thing with Samsung is we're expanding the business. So traditionally, we were not the main supplier of all of their wearables and other devices, and you started to see that associated with the premium Galaxy design as well.

**Operator** (Operator):
Our next question is from the line of Ben Reitzes with Melius Research.

**Benjamin Reitzes** (Analysts):
I'm switching my question because Stacy just asked on the Samsung. So I wanted to ask about automotive with regard to the beat in the quarter versus expectations. I know you're talking about IoT, automotive and data center all growing 60% for the year. But specifically in automotive, it was particularly strong versus expectations, and you are increasing some prices that you mentioned. Is there a chance that there was prebuying there in the automotive segment? Or do you feel like this kind of performance is sustainable throughout the year? And then I have a follow-up.

**Cristiano Amon** (Executives):
No, very good. Thank you for the question. Look, we have been saying -- I believe we have said that in last quarter about the transition of our fifth generation platform. Just to give an idea, for cars that you see now on the road that with our third-generation platform, the silicon content increase versus the fifth generation is 8x. There's a lot of more -- there's a lot more compute content into the automotive. And most of our automotive growth is really share where the design win pipeline translate into revenue. That's where we started to see step function increases on the SoC revenue, and that will continue.

**Benjamin Reitzes** (Analysts):
Okay. And then, Akash, with regard to the EBIT margins, the EBT margins for QCT, how is that going to progress throughout the year from the 20% to 22% that you guided for given the mix shift towards data center? I was a little unclear there. How should we model that as we go throughout the year?

**Akash Palkhiwala** (Executives):
Yes, Ben, so maybe it's a good opportunity to clarify that one of the changes we have made in the way we segment the business is QCT now includes Data Center. In '26, it was outside the QCT segment. And just that change kind of reduces QCT gross margin -- operating margin by 3% as, of course, we are investing ahead of revenue in a couple of product lines. It doesn't change the overall Qualcomm numbers. It's just a change within segments that is included now in the QCT numbers. We're, of course, not guiding specific quarters or years for operating margins, but you should think of it as our operating margin target for QCT doesn't change. We are still looking at a target of 30%. And as revenue starts scaling across the next 2 to 3 years, we are confident in our ability to achieve it.

**Operator** (Operator):
The next question is from the line of Vivek Arya with Bank of America.

**Liam Pharr** (Analysts):
This is Liam Pharr on for Vivek. On networking interconnects, you mentioned the AWS optical ramp and a second optical connectivity customer. Could you help us size how large connectivity is today and how you see it growing into fiscal '27 and '28 as you move to 224 gig and 1.6T? And does the ongoing consolidation in the optical interconnect space impact you in any way? Do you see any natural synergies between interconnects and lasers from an ownership standpoint?

**Cristiano Amon** (Executives):
Very good. Actually, thank you so much for the question. I really appreciate that. So we're not breaking that down, but you should assume that there is interconnect connectivity revenue within the $15 billion that we talk about it and some of the $5 billion that we talked about in data center, $5 billion '27, $15 billion '29 . We have been very optimistic about this. We have been investing. This asset came to Qualcomm as part of the Alphawave acquisition. I think Qualcomm is probably a natural place for comms and we have been investing into this.
We have very interesting technology demonstration or progress with optical and co-packaged optics in the quarter in the 2026 ECOC in Europe, we actually did the demonstration with Lumentum. And you bring a good point. I think the structure of the industry is going to change. My analogy is what happened on RF front end, and that creates opportunities. So we have been engaged in very interesting conversations with some of the laser companies, especially as different forms of partnerships and strategic partnerships are going to be formed. This is actually a very exciting opportunity for Qualcomm. And you're going to see over time a lot more products from Qualcomm on optics. And we have been working on the road map that we outlined in 400 gig, 800 and 1.6 tera.

**Liam Pharr** (Analysts):
And then on the Dragonfly CPU, you mentioned new prospects beyond Meta. How should we think about the relative upside in CPUs relative to custom accelerators? And with the Arm remedies phase still pending, does the outcome have any implications for your CPU road map or cost structure?

**Cristiano Amon** (Executives):
So let me break that question into 2. No implications on our CPU road map. I think we've been very clear about where we are with the Arm trial. We're actually very happy and with our ability to continue to develop and ship Oryon products. I will look at that as probably upside in the projections that we made on $5 billion and $15 billion, we just had Meta as a customer. Any new customer above that is an upside to the revenue target.

**Operator** (Operator):
The next questions are from the line of Jim Schneider with Goldman Sachs.

**James Schneider** (Analysts):
I was wondering if you can maybe just kind of clarify relative to the 3 distinct hyperscale customers that you're ramping through fiscal '27, will all 3 of those be at some kind of revenue materiality exiting the year? Or will it just be maybe 2 of them and 1 will kind of fall outside the year?

**Akash Palkhiwala** (Executives):
Yes. You should think of 2 of those customers at a very significant scale, making up that $5 billion, and they will extend into fiscal '28 and then '29 as well. So it's -- think of it as a long-term multi-generation multi-product relationship and both the relationships are at scale.

**James Schneider** (Analysts):
And then as we model fiscal '27, you provided some helpful overall EBIT margin commentary in terms of the profile of the year. But is there any way to think about OpEx? And specifically, is there any kind of material OpEx step-up that we should be thinking about during the course of fiscal '27?

**Akash Palkhiwala** (Executives):
Yes. I think you should just think of our OpEx approach as consistent over the last year. We're guiding $2.8 billion for the September quarter. And the focus on OpEx is really kind of bringing in new skills that don't exist in the company as we diversify, especially within Data Center, and that will continue to be the focus area for us going forward. Just maybe one timing thing is just we typically have calendar year employee-related expenses reset when we get to January. So that will happen, but that's kind of consistent with previous years that you've seen.

**Operator** (Operator):
Our final question is from the line of Chris Caso with Wolfe Research.

**Christopher Caso** (Analysts):
Yes. I guess first question is with regard to the Starlink announcement you made this morning. Could you give some more color on that in terms of timing, magnitude and what Qualcomm is providing into that venture?

**Cristiano Amon** (Executives):
Yes. Thanks for the question, Chris. So timing, I think we talk about '27, you should think about from a financial standpoint, it will start to appear as we exit fiscal '27. It's more of a fiscal '28 from a revenue standpoint. Magnitude, I think that what we can say at this point, and I think it's probably how we both articulated into the announcement is a nationwide network in the United States and probably one of the largest build-outs of a network. It's terrestrial network.
We provide silicon content for radio, including massive MIMO as well as the accelerator for the digital unit, and we provide software on the Layer 1. It's a very -- it's a great partnership with SpaceX for next generation, I think, infrastructure. The industry has been running on dedicated equipment. I think we have seen a lot of trends of technology ranging from Open RAN to AI native as an opportunity to innovate in this space. And as we talk about it, it's a multiyear agreement and including how we're going to be thinking about the next generation of wireless as well. We're very proud of this announcement. I think it's great also from the United States technology leadership standpoint, and we're going to be executing on it.

**Christopher Caso** (Analysts):
Great. As a follow-up question, I wonder if you could give some color. And I know you talked a bit about this in the Analyst Day, but in terms of what product categories are in the Data Center revenue in the $5 billion in fiscal '27 and when other products layer in? And obviously, for near term for this year, is it all connectivity revenue? Is there -- assuming that there's no accelerator revenue in the numbers for the $5 billion that comes in '27?

**Akash Palkhiwala** (Executives):
Chris, so for the $5 billion in '27, most of that revenue is actually custom silicon engagement for the main AI accelerator at our 2 hyperscaler customers. The next category that's material in the $5 billion in fiscal '27 is the connectivity revenue. So you should think of those as driving the FY '27 revenue ramp. When you think about the $15 billion revenue in '29, that will be inclusive of the custom silicon engagement, expansion in connectivity, but then we'll also have CPU and AI accelerator both coming in. And that's why we feel confident about achieving the $15 billion and really going beyond that as we execute on the product road map given how good our technology is looking and the interest that we're seeing from various hyperscalers.

**Operator** (Operator):
That concludes today's question-and-answer session. Mr. Amon, do you have anything further to add before adjourning the call?

**Cristiano Amon** (Executives):
No, I just wanted to thank our employees and our partners. As I said in my prepared remarks, this is an important, I think, close of a fiscal year for Qualcomm. And it really positions us to start fiscal '27 with all of the things that are within our control and now focus on growing in a much more diversified company. We're very excited about that. We have a lot of things we're doing in parallel, but I guess we develop that capability as we diversify the company, and we're excited about our future. Thank you.

**Operator** (Operator):
Thank you. Ladies and gentlemen, this concludes today's conference call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### QCOM_Q3_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：CFO 給 FQ4 總營收與非GAAP EPS 財測區間（原話："We are forecasting revenues of $9.7 billion to $10.5 billion"）
- 2026-07-29｜CFO｜guidance：FQ4 QCT 營收與 EBT margin 財測（原話："In QCT, we expect revenues of $8.4 billion to $9 billion and"）
- 2026-07-29｜CFO｜guidance：FQ4 QTL 營收與 EBT margin 財測（原話："In QTL, we estimate revenues of $1.2 billion to $1.4"）
- 2026-07-29｜CFO｜guidance：FQ4 非GAAP 營業費用財測，含 Modular 併入與資料中心投資（原話："we anticipate non-GAAP operating expenses to be"）
- 2026-07-29｜CFO｜guidance：FQ4 車用預期年增約 60%（原話："In QCT automotive, we expect another record quarter with"）
- 2026-07-29｜CFO｜guidance：FQ1 不正式給財測，但定性說 QCT 營收季增小幅，Apple 約減半（原話："we expect it to be slightly up on a sequential basis."）
- 2026-07-29｜CFO｜guidance：FQ1 Apple 營收預期自 9 月季到 12 月季下滑約 50%（原話："we are forecasting approximately 50% decline from September"）
- 2026-07-29｜CFO｜guidance：季節性改變：預期 12 月季到 3 月季營收成長（原話："So we actually expect revenues to grow when we go from the"）
- 2026-07-29｜CFO｜guidance：FY27 非手機營收成長率由 FY26 的 24% 加速至逾 60%（原話："accelerate from 24% in fiscal '26 to greater than 60% in"）
- 2026-07-29｜CFO｜guidance：FY27 手機市場預期年減低十位數，Android 營收年減 20%、EPS 影響逾 1.5 美元（原話："the market will be down low teens relative to '25 to '26."）
- 2026-07-29｜CEO｜guidance：FY27 預期整體營收成長（原話："we expect top line growth for Qualcomm in fiscal '27"）
- 2026-07-29｜CFO｜guidance：FY27 與 FY29 資料中心營收目標及非手機占 QCT 比重（原話："data center revenue growth to $5 billion in fiscal '27 and"）
- 2026-07-29｜CEO｜guidance：車用年化營收出場速率目標由 60 億上調至約 70 億美元（原話："now expect annualized sales of approximately $7 billion"）
- 2026-07-29｜CFO｜guidance：OpEx 走勢：無變動，成長主要來自資料中心投資（原話："no change to the guidance we provided at Investor Day."）
- 2026-07-29｜CFO｜margin：管理層拆解 QCT 毛利率壓力的兩個成因之一：高階產品組合偏弱（原話："the first is a little bit of a weaker mix within premium"）
- 2026-07-29｜CFO｜margin：毛利率壓力第二個成因為供應鏈投入成本上升，漲價將在未來幾季反映（原話："we expect this benefit to show up in our gross margins over"）
- 2026-07-29｜CEO｜margin：CEO 稱 QCT 毛利率短期略低於歷史區間（原話："QCT gross margins, which will be slightly below our"）
- 2026-07-29｜CFO｜margin：基線毛利率區間 48%-50%；資料中心初期以客製晶片為主，對 QCT 加權毛利率拖累 1.5-2 個百分點（原話："that will be a drag of 1.5% to 2% on the weighted average"）
- 2026-07-29｜CFO｜margin：漲價幅度為雙位數，涵蓋多個終端市場，受合約與產品週期影響逐步生效（原話："the scale of the increase that we're looking at is double"）
- 2026-07-29｜CFO｜margin：QTL 版稅有 ASP 上限，價格在上限以下上漲才有部分受惠（原話："there is a cap on the total royalties based on the device"）
- 2026-07-29｜CFO｜competition：管理層稱漲價與同業一致（原話："it's no different than what a lot of the peers in our"）
- 2026-07-29｜CEO｜competition：三星旗艦機約 70% 採用 Snapdragon（原話："Snapdragon powering approximately 70% of their"）
- 2026-07-29｜CFO｜risk：Apple 敘事變化：因供應限制，新機份額預期遠低於先前估的 20%，Apple 營收下滑提前（原話："materially lower than our prior estimate of 20%."）
- 2026-07-29｜CFO｜customer：FY27 Apple 產品營收將低於先前指引的略高於 20 億美元（原話："less than the previous guidance we had given, which was a"）
- 2026-07-29｜CEO｜risk：記憶體價格與投入成本、供應短缺造成手機及消費電子營收下滑（原話："the entire industry continues to be impacted by"）
- 2026-07-29｜CEO｜risk：CEO 承認投資人想看資料中心執行的更多證明（原話："investors want to see more proof points that we can"）
- 2026-07-29｜CEO｜risk：供應鏈全面滿載，CEO 稱有供應執行計畫但沒人真正寬裕（原話："Everything is at 100% utilization, everything."）
- 2026-07-29｜CEO｜risk：美中限制：目前客戶合作不受限（原話："For the engagements we have today, we're not restricted."）
- 2026-07-29｜CFO｜customer：中國 OEM 營收預期 FQ3 為底部，FQ4 回到雙位數季增（原話："reached a bottom in the third fiscal quarter and will return"）
- 2026-07-29｜CFO｜customer：中國 OEM 先前消化通路庫存，現通路庫存已薄，營收回歸市場實際規模（原話："the channel inventory has thinned down that they can't draw"）
- 2026-07-29｜CEO｜customer：與 BMW 簽署擴大協議，成為次世代 ADAS 與數位座艙主要算力矽供應商（原話："lead compute silicon provider for their next-generation ADAS"）
- 2026-07-29｜CEO｜customer：車廠由逐 socket 設計贏單轉向多世代平台合作（原話："Customers are shifting from socket-by-socket design awards"）
- 2026-07-29｜CFO｜customer：兩個客製晶片客戶皆為全球級超大規模雲端業者，已有 PO 並開始投片（原話："we do have POs from these engagements, and so we've already"）
- 2026-07-29｜CEO｜product：HBC Gen 1 已完成 tape-out，首款 HBC 方案預計 2027 年中推出（原話："we have completed the tape-out of HBC Gen 1"）
- 2026-07-29｜CEO｜product：資料中心產品線時程：連接 FY26、客製矽與 AI 加速器 FY27、伺服器 CPU FY28（原話："custom silicon and AI accelerators in fiscal '27 and"）
- 2026-07-29｜CEO｜product：完成收購 Modular，強化資料中心與邊緣 AI 軟體堆疊（原話："we have closed our acquisition of Modular Inc., and"）
- 2026-07-29｜CEO｜product：CEO 稱 HBC 與 CPU 客戶想先看到矽片，晶片實測是下一個里程碑（原話："we needed to see silicon and see how it performs before we"）
- 2026-07-29｜CFO｜product：FQ3 車用營收 16 億美元、年增 61%；非手機 QCT 年增 28%（原話："record quarter with revenues of $1.6 billion, with 61% year-"）
- 2026-07-29｜CEO｜product：工業設計贏單管線逾 70 億美元，本財年已取得逾 35 億美元（原話："our industrial design win pipeline exceeds $7 billion with"）
- 2026-07-29｜CFO｜capital_allocation：FQ3 資本回饋 23 億美元（買回 14 億、股利 9.73 億）（原話："we returned $2.3 billion to stockholders"）
- 2026-07-29｜CFO｜capital_allocation：OpEx 規模納入 Alphawave 與 Modular 收購並持續投資資料中心（原話："it will reflect both obviously Alphawave and now Modular in"）
- 2026-07-29｜CEO｜commitment：CEO 承諾漲價生效後毛利率回到營運模型（原話："as they take effect, we expect to see gross margins realign"）
- 2026-07-29｜CEO｜commitment：兩個近期客製矽案於 12 月季開始貢獻營收（原話："Our 2 near-term custom silicon wins will be revenue"）
- 2026-07-29｜CFO｜commitment：FY27 非手機成長預期取代 FY26 全部 Apple 產品營收（原話："We expect this growth from non-handset revenues in fiscal"）
- 2026-07-29｜CEO｜commitment：FY29 非手機營收目標由 220 億上調至 400 億美元（原話："bringing our total non-handset revenue outlook to $40"）

### QCOM_Analyst_Investor_Day_QUALCOMM_Incorporated_20260624.md
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 給資料中心 FY27 營收目標 50 億美元。（原話："We're targeting $5 billion of revenue in fiscal '27."）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 給資料中心 FY29 營收目標 150 億美元。（原話："We are targeting $15 billion of revenue in data center"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 把 FY29 非手機營收目標由 18 個月前的 220 億上調為 400 億美元。（原話："Our fiscal '29 revenue target is now $40 billion."）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 給 FY29 EPS 目標高於 18 美元。（原話："Our EPS target is of greater than $18"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 說長期有機會把營收規模拉到 1000 億美元。（原話："our revenue to $100 billion"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 給車用 FY29 營收目標 100 億美元，並說這是第二次把進度再提前兩年。（原話："We will hit $10 billion of revenue in fiscal '29."）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 給個人 AI 與運算（PC 等）加工業網通與機器人合計 IoT 目標。（原話："We're going to be over $14 billion across these markets"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 給工業網通與機器人 FY29 營收目標 80 億美元。（原話："We are targeting $8 billion in '29 for this business"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 預期安卓手機營收溫和成長 5%，並列出前提是記憶體環境不大變、也不含 agentic AI 帶來的升級。（原話："This assumes that the current memory environment"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 說 FY29 手機占營收約三分之一（FY27 低於一半）。（原話："handset will be 1/3 of our revenues in '29"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 說資料中心長期可及市場約 1 兆美元，目標 5 到 7 年內市占率超過 5%。（原話："we are targeting greater than 5% share in 5 to 7 years"）
- 2026-06-24｜Nakul Duggal｜guidance：車用業務主管說 FY26 結束時年化營收達 60 億美元。（原話："We will exit FY '26 at $6 billion in annualized revenue"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 對資料中心 FY27 內容的拆解：兩家超大型雲端客戶各自超過 10 億美元，客製化晶片占最大宗。（原話："who will each be greater than $1 billion"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 在簡報中對同一批兩家超大型客戶的 FY27 貢獻說法（年內至少 10 億）。（原話："2 hyperscaler customers that are at global scale"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜margin：CFO 說 QCT（含資料中心）長期營業利益率目標 30%，與先前目標不變。（原話："to be at 30% in the long term"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜margin：CFO 說 QTL 營業利益率維持 70%。（原話："expect QTL to continue to be at 70%"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜margin：CFO 說客製化晶片毛利率會略低於公司整體毛利率。（原話："custom silicon gross margin to be slightly below our"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜margin：CFO 說客製化晶片在營業利益率層級是加分的。（原話："be accretive at the operating margin level"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜margin：CFO 說過去五年營運費用占營收比由 31% 降到 23%。（原話："OpEx as a percent of revenue came down from 31% to 23%"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜margin：CFO 預期營運費用占營收比進一步降到 19% 至 20%。（原話："we expect that to decline further to 19% to 20%"）
- 2026-06-24｜Antonios Pialis｜commitment：資料中心負責人承諾 FY27 起交出數十億美元營收。（原話："we will deliver multiple billions of revenue starting fiscal"）
- 2026-06-24｜Antonios Pialis｜commitment：資料中心負責人宣布贏得兩家超大型雲端客製化晶片案，年底起貢獻營收。（原話："hyperscaler deals that will contribute meaningful revenue"）
- 2026-06-24｜Nakul Duggal｜commitment：車用業務主管表示不打算讓連續兩位數成長中斷。（原話："We don't expect to let you down anytime"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜commitment：CFO 說營收與 EPS 成長速度會比先前告訴投資人的快。（原話："going to grow much faster than what we had told you before"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜capital_allocation：CFO 說資本配置策略不變。（原話："Our capital allocation strategy really is unchanged."）
- 2026-06-24｜Akash Palkhiwala (CFO)｜capital_allocation：CFO 說股息會以中低個位數幅度持續調升。（原話："We're going to keep increasing dividends in mid- to"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜capital_allocation：CFO 說大部分自由現金流會還給股東。（原話："we'll return most of our free cash flow to shareholders"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜capital_allocation：CFO 說過去十年已註銷 30% 股數。（原話："Over the last 10 years, we've retired 30% of our shares"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜capital_allocation：CFO 說過去五年完成 35 筆併購。（原話："we've done 35 acquisitions over the last 5 years"）
- 2026-06-24｜Mark Zuckerberg｜customer：Meta CEO 宣布與高通簽訂多世代合作，由高通供應資料中心 CPU。（原話："we've entered a multigenerational collaboration"）
- 2026-06-24｜Satya Nadella｜customer：微軟 CEO 表示對高通的資料中心高頻寬運算（HBC）創新感到期待。（原話："we are excited about your innovation in the data center"）
- 2026-06-24｜Antonios Pialis｜customer：高通介紹 HUMAIN 為其第一個資料中心客戶。（原話："our first data center customer"）
- 2026-06-24｜Antonios Pialis｜customer：資料中心負責人說連接晶片產品今年通過第一家主要超大型雲端客戶認證。（原話："we are qualified in our first leading major hyperscaler"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜customer：CFO 說資料中心營收來源並不集中。（原話："This is not a concentrated revenue stream."）
- 2026-06-24｜Nakul Duggal｜customer：車用業務主管說車用設計案儲備金額 650 億美元。（原話："We have built a $65 billion design win pipeline."）
- 2026-06-24｜Nakul Duggal｜customer：車用業務主管說 ADAS 客戶已達 25 家車廠。（原話："We are now at 25 OEMs."）
- 2026-06-24｜Cristiano Amon｜customer：CEO 說在中國每家做 agent 的基礎模型公司也成了客戶，傳統手機客戶界線模糊。（原話："I don't know who the mobile customers"）
- 2026-06-24｜Antonios Pialis｜product：資料中心負責人給出第一個 HBC 產品（AI250）上市時點。（原話："of our first HBC product in the middle of 2027"）
- 2026-06-24｜Antonios Pialis｜product：資料中心負責人給出 Oryon 伺服器級 CPU 推出時點（2028 年中）。（原話："the industry's first Oryon server class compute solution"）
- 2026-06-24｜Antonios Pialis｜product：資料中心負責人說 2027 年推出第三代 AI 加速器。（原話："Then in 2027, we are launching our third generation"）
- 2026-06-24｜Antonios Pialis｜product：資料中心負責人引述 C1000 CPU 時脈高於 5GHz、比競品快 30% 以上。（原話："30% faster than any of the competition"）
- 2026-06-24｜Antonios Pialis｜product：資料中心負責人引述 HBC 每瓦頻寬相對 HBM 方案的倍數。（原話："With HBC, we deliver 6x the bandwidth per watt versus"）
- 2026-06-24｜Cristiano Amon｜product：CEO 回顧資料中心營收時點從 FY28 逐步提前到 FY27、FY26 的說法。（原話："we get more traction, we move it to fiscal '27"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜product：CFO 描述公司定位轉變：從裝置公司變成雲端加裝置公司。（原話："being a devices company to being a cloud and device company"）
- 2026-06-24｜Cristiano Amon｜competition：CEO 回應「進資料中心是否太晚」。（原話："Never too late for Qualcomm."）
- 2026-06-24｜Cristiano Amon｜competition：CEO 說推論市場的護城河不如訓練市場強。（原話："not as strong as it has been for training"）
- 2026-06-24｜Tim Davis｜competition：Modular 共同創辦人把自家軟體定位為 NVIDIA 軟體堆疊的可攜替代方案。（原話："NVIDIA's software stack designed from day 1"）
- 2026-06-24｜Cristiano Amon｜risk：CEO 說手機市場正面對記憶體供應狀況的不確定性。（原話："uncertainty of the memory situation"）
- 2026-06-24｜Cristiano Amon｜risk：CEO 說 FY27 的 50 億美元已鎖定產能。（原話："For that revenue, we have secured capacity as well"）
- 2026-06-24｜Cristiano Amon｜risk：CEO 說 FY27 的 50 億美元已備妥晶圓與記憶體。（原話："we have wafers and we have memory"）

### 問答異常語氣（迴避／改口／保留）
- QCOM_Q3_2026_Earnings_Call_20260729.md｜問：Rasgon 問是否刻意「餓死」Apple、把矽片轉供他處｜答法：CFO 否認該說法，歸因部分為供應限制、部分為與 Apple 討論結果，未量化份額（只說「materially less than 20%」），亦未給確切 FY27 Apple 金額
- QCOM_Q3_2026_Earnings_Call_20260729.md｜問：Reitzes 問資料中心除兩客戶外是否有更多客戶、管線如何擴張｜答法：CEO 未直接確認第三家客戶，改談現有客戶線路與「客戶要先看到矽片」的里程碑
- QCOM_Q3_2026_Earnings_Call_20260729.md｜問：Cardoso 問漲價幅度及在需求已受壓的手機市場如何推行｜答法：CFO 只給「雙位數」不拆各市場；CEO 補充以記憶體 BOM 比較，稱不預期高階量有根本改變
- QCOM_Q3_2026_Earnings_Call_20260729.md｜問：Buchalter 問毛利率回到先前水準的時間點｜答法：CFO 只說「未來幾季」、逐步因合約與產品週期，不給具體時點或數字
- QCOM_Analyst_Investor_Day_QUALCOMM_Incorporated_20260624.md｜問：Goldman Sachs 的 Jim Schneider 問 FY27 的 50 億美元是否都已有訂單、以及用現有客戶能否達成 FY29 目標。｜答法：CFO 回答「high confidence in our forecast, and so I'll leave it at that」，未回答訂單是否涵蓋，也未回答現有客戶能否達成 FY29；資料中心負責人補充「幾個吉瓦可達 FY29 數字」，同樣沒給客戶或訂單數字。
- QCOM_Analyst_Investor_Day_QUALCOMM_Incorporated_20260624.md｜問：Wolfe 的 Chris Caso 問 FY27 指引內含哪些產品，以及兩家客戶是不是已公布的 HUMAIN 與微軟。｜答法：CFO 說明產品組合（客製化晶片最大、AI 加速器年底、連接產品），並說兩家客戶是超大型雲端、HUMAIN 是連接產品的重要部分；未直接確認或否認兩家客戶是否為微軟，也未點名。

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
{"date":"20260730","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"非手機引擎（Auto ＋ IoT ＋ 資料中心）FY27 營收成長 &gt; 60% 至約 $210 億，完整取代 FY26 約 $72 億的 Apple 產品營收；FY29 達 $400 億、佔 QCT 約三分之二。"},{"id":"H2","text":"雙位數漲價落地後 QCT 毛利率回到 48-50% 歷史區間，且資料中心客製矽（毛利率約 35%）對加權毛利率的 1.5-2pp 拖累不使其結構性掉出區間。—— 這是本報告新增的假設，取代上一份報告的 H2（QTL 維持），因為法說揭露的毛利率結構問題已經超越授權風險成為第一順位。"},{"id":"H3","text":"QTL 維持約 $54-56 億／年、EBT 率 ≥ 68%，不被裝置 ASP 上限、OEM 拒付、監管處置或華為未續約結構性壓縮。"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"資料中心從「已下 PO 的兩個客製矽案子」擴不出去：HBC 加速器與 Dragonfly C1000 拿不到商品矽插槽，$50 億（FY27）→ $150 億（FY29）的斜坡斷在第一階。結構原因有三個且互相獨立：① Arm 自製 AGI CPU 已於 2026-03 出貨、Meta 首發、FY27-28 需求逾 $20 億，而 C1000 要 2028 才上市（晚兩年、且付 Arm 授權金）；② hyperscaler 客製矽是多源策略，Broadcom／Marvell／聯發科都在同一張桌上；③ Cristiano 自己說「很多客戶要看到矽才決定」——也就是說目前的 pipeline 大部分還沒轉單。"},{"id":"R2","text":"QCT 毛利率結構性下移：漲價落地慢於組合稀釋，QCT 從 48-50% 的新常態變成 45-47%。四季軌跡已經在走：分部 EBT 率 31%（Q1 FY26）→ 27%（Q2）→ 26%（Q3）→ 指引 23-25%（Q4）。三個壓力來源疊加：台積 &lt;5nm 節點 2026 起漲價 5-10%（2nm 單片 &gt;$30,000、較前代 ＋50%）、OSAT 封測附加費 8-20%、資料中心客製矽稀釋 1.5-2pp。而 premium tier 內部降階（OEM 為了消化記憶體成本改用前代或較低階晶片）是需求側的自主降級——漲價治不了它。"},{"id":"R3","text":"QTL 的三重慢性壓縮同時發作：裝置 ASP 上限使記憶體驅動的手機漲價完全不入袋（Akash 明講上限以上「沒有差別」）＋ 華為授權到期未續且談判無果 ＋ 中國 SAMR 裁決附帶授權行為救濟。QTL 是全公司唯一的 69-72% EBT 率年金，它每流失 $1 都是接近純利。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"starter 1/3·帽 3%·加碼＝QCT 毛利率回 48%＋（Q1 FY27 法說）或資料中心單季營收 ≥ $1.0B","irr_base_pct":14.4,"ev5y_pct":76.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":6.0,"ev5y_pct":76.7,"irr_base_pct":14.4,"max_dd_pct":-45.0,"bull_5y_price":387.0,"bear_5y_price":100.0,"p_bull_pct":22.0,"p_bear_pct":32.0,"rearm_trigger":"starter 1/3·帽 3%·加碼＝QCT 毛利率回 48%＋（Q1 FY27 法說）或資料中心單季營收 ≥ $1.0B","price_at_dd":148.4,"archetype":"品質複利成長","cycle_position":"早循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/QCOM_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
