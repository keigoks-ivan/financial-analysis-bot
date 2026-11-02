你是 stock-analyst **v20 判斷 agent**，標的 LLY（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"LLY","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LLY_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LLY_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":24397,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（investor.lilly.com/node/55191，同文 8-K：https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000104/q326lillysalesandearningsp.htm）"},"note":"未取得"},{"id":"f_kpi1_gaap","label":"GAAP 營業利益／利益率","value":8608,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"百萬美元（利益率 35.3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（investor.lilly.com/node/55191，同文 8-K：https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000104/q326lillysalesandearningsp.htm）；利益率為營業利益÷營收自行計算"},"note":"未取得"},{"id":"f_kpi2_non_gaap","label":"Non-GAAP 營業利益／利益率（推算）","value":9039,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"百萬美元（利益率約 37.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司未揭露此數；自行推算＝GAAP 營業利益 8,608＋無形資產攤銷 128＋資產減損／重組等 303（出處同 https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000104/q326lillysalesandearningsp.htm）"},"note":"未取得"},{"id":"f_kpi3_non_gaap_eps","label":"Non-GAAP EPS","value":7.48,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（investor.lilly.com/node/55191，同文 8-K：https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000104/q326lillysalesandearningsp.htm）"},"note":"未取得"},{"id":"f_kpi4_non_gaap","label":"Non-GAAP 毛利率","value":84.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（investor.lilly.com/node/55191，同文 8-K：https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000104/q326lillysalesandearningsp.htm）"},"note":"未取得"},{"id":"f_kpi5_mounjaro","label":"Mounjaro 全球營收","value":10723,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（investor.lilly.com/node/55191，同文 8-K：https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000104/q326lillysalesandearningsp.htm）"},"note":"未取得"},{"id":"f_kpi6_zepbound","label":"Zepbound 全球營收","value":5352,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（investor.lilly.com/node/55191，同文 8-K：https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000104/q326lillysalesandearningsp.htm）"},"note":"未取得"},{"id":"f_kpi7_2026","label":"全年 2026 指引","value":"營收 91.0–92.0 十億；non-GAAP EPS 35.00–36.00；performance margin 52.0–52.5%","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（investor.lilly.com/node/55191，同文 8-K：https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000104/q326lillysalesandearningsp.htm）"},"note":"EPS 共識 FY1 35.13（財報後 10-31 快照；來源 consensus_revision）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_lly_gross_margin_pct","label":"LLY 毛利率","value":83.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lly_operating_margin_pct","label":"LLY 營業利益率","value":51.25,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lly_fcf_margin_pct","label":"LLY FCF 利潤率","value":13.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nvo_gross_margin_pct","label":"NVO 毛利率","value":80.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvo_operating_margin_pct","label":"NVO 營業利益率","value":43.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvo_fcf_margin_pct","label":"NVO FCF 利潤率","value":14.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mrk_gross_margin_pct","label":"MRK 毛利率","value":71.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mrk_operating_margin_pct","label":"MRK 營業利益率","value":0.87,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mrk_fcf_margin_pct","label":"MRK FCF 利潤率","value":18.72,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abbv_gross_margin_pct","label":"ABBV 毛利率","value":71.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbv_operating_margin_pct","label":"ABBV 營業利益率","value":33.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbv_fcf_margin_pct","label":"ABBV FCF 利潤率","value":28.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_azn_gross_margin_pct","label":"AZN 毛利率","value":81.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AZN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_azn_operating_margin_pct","label":"AZN 營業利益率","value":22.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AZN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_azn_fcf_margin_pct","label":"AZN FCF 利潤率","value":9.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AZN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":1417.54,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":47.61,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":77.89,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":3.29,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（34.01 → 35.13）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":4.27,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（47.34 → 49.36）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":3.89,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（54.55 → 56.67）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":35.13,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":49.36,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":56.67,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.8,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 34.51 → 35.13（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":46.01,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":14.6,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝66.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":66.1,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":15.12,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝64.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":64.1,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":40.35,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 35.13，分子＝快照價 1417.54","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.472,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":44618.0,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 49503.0、現金 4885.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":890.75,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":1307284.78,"period":"2026-11-02","unit":"USD m","basis":"市值 1262666.78 ＋ 淨負債 44618.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":91654.78,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":104831.7,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（28 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":14.26,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 1417.54 / W52 1082.33 / W104 931.23 / W250 683.42 / W250 13週斜率 2.47%"},{"id":"f_ma_w52","label":"52 週均線","value":1082.33,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":931.23,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":683.42,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.47,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 稱面臨全球競爭加劇，包括來自中國等市場研發能力大幅擴張的對手，這些公司正向跨國藥廠授權產品並直接在主要市場競爭。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"We face intensifying competition worldwide, including from China and other markets that have significantly expanded and accelerated research and development capabilities.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"搜尋摘要引 CNBC 來源報導：Lilly 美國肥胖藥市佔 60.9%、Novo 38.8%（二手來源，未對 IQVIA 核實）。","source":"WebSearch 摘要（heygotrade 等聚合，引 CNBC 2026-08-06）","url":"https://heygotrade.com/en/blog/eli-lilly-lly-vs-novo-nordisk-nvo-2026-glp1/","excerpt":"Lilly leads the obesity drug market with a 60.9% U.S. share, driven by strong sales of Mounjaro and Zepbound.","as_of":"2026-08-06","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2026年5月報導指 Lilly 在美國以外 GLP-1 市場份額已超越 Novo。","source":"GXP News","url":"https://gxpnews.net/en/2026/05/eli-lilly-overtakes-novo-nordisk-in-glp-1-market-share-outside-us/","excerpt":"Eli Lilly overtakes Novo Nordisk in GLP-1 market share outside US","as_of":"2026-05-01","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"口服競爭：Novo 口服 Wegovy 於2025年12月先獲FDA核准；Lilly orforglipron(Foundayo)2026年4月獲准，晚三個多月；Pfizer(Metsera)目標2028首次核准，Amgen MariTide進行六項後期試驗。","source":"Reuters Factbox 經 AOL/MarketScreener 轉載（摘要）","url":"https://www.aol.com/articles/factbox-weight-loss-drug-developers-122138062.html","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K：McKesson、Cencora、Cardinal Health 三家美國批發商在 2023–2025 各占合併營收顯著比例，無其他客戶超過 10%；搜尋未見最大客戶導入第二供應商或自製的來源。","source":"Eli Lilly FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"In 2025, 2024, and 2023, three wholesale distributors in the U.S.—McKesson Corporation, Cencora, Inc., and Cardinal Health, Inc.—each accounted for a significant percentage of our consolidated revenue. No other customer accounted for more than 10 percent of our consolidated revenue in any of these years.","as_of":"2026-02-01","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"LLY FY2025 10-K 披露三大美國批發商(McKesson、Cencora、Cardinal Health)占合併營收比重，其他客戶均未超過10%","source":"SEC EDGAR LLY Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"In 2025, 2024, and 2023, three wholesale distributors in the U.S.—McKesson Corporation, Cencora, Inc., and Cardinal Health, Inc.—each accounted for a significant percentage of our consolidated revenue. No other customer accounted for more than 10 percent of our consolidated revenue in any of these years.","as_of":"2026-02-20","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Lilly CFO said in March 2026 Lilly is producing ahead of demand for the first time since Zepbound launch, with three-month buffer inventory (secondary source)","source":"glp1clinics.org - eli lilly zepbound manufacturing supply shortages easing","url":"https://www.glp1clinics.org/blog/eli-lilly-zepbound-manufacturing-supply-shortages-easing","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261102","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Lilly's $27B plan adds four new US plants (three API, one injectables) expected operational in about five years; Houston $6.5B plant groundbreaking reported Sept 2026; Alzey Germany injectable site expected operational start of 2027; RTP NC fully operational 2027","source":"Fierce Pharma / European Pharmaceutical Review / search summary","url":"https://www.fiercepharma.com/manufacturing/plan-build-4-more-plants-eli-lilly-doubles-down-literally-its-manufacturing-pledge","excerpt":null,"as_of":"2026-09-24","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Lilly raised 2026 revenue guidance to $85-87B (Q2, Aug 2026); Leerink projects 15% revenue CAGR and $125B 2030 revenue, citing Medicare/Medicaid access from early 2027; Q3 actuals not found","source":"BNN Bloomberg / S&P Global preview / Yahoo Finance Leerink","url":"https://www.bnnbloomberg.ca/business/company-news/2026/08/05/eli-lilly-raises-annual-revenue-forecast-as-glp-1-drugs-fuel-growth/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Obesity-market forecasts trimmed: Reuters Feb 2026 said 2030 outlook cut ~30% on lower US GLP-1 prices and competition; Goldman cites $105B global by 2030 (down from $130B); Morningstar flags Medicare negotiation 2027 and new entrants 2027-2029","source":"Reuters via AOL / Morningstar","url":"https://www.aol.com/articles/analysis-obesity-market-sales-potential-110742804.html","excerpt":null,"as_of":"2026-02-15","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 指出 FTC 與歐洲等競爭主管機關對產業併購的持續關注，可能延遲或增加 Lilly 商務發展（併購/授權）活動的成本與風險。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"Continued regulatory focus on business combinations in our industry, including by the Federal Trade Commission and competition authorities in Europe and other jurisdictions, and heightened competition for attractive targets has and could continue to delay, jeopardize, or increase the costs or risks of our business development activities.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2025年12月歐盟就藥品通則立法達成原則性協議，將以條件制縮短部分智財保護（資料保護期上限）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"an agreement-in-principle announced in December 2025 between the European Commission, Council and Parliament to revise the EU's general pharmaceutical legislation would make conditional the length of certain pharmaceutical intellectual property incentives, including by reductions in maximum data protection periods.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"佛州檢察長 2026-09 於 Miami-Dade 對 Lilly、Novo、Sanofi 及 PBM 提起 insulin/GLP-1 回扣反壟斷與不實交易訴訟。","source":"Bloomberg Government: Florida Sues Lilly, Sanofi, CVS in Insulin Antitrust Action","url":"https://news.bgov.com/litigation/florida-sues-eli-lilly-sanofi-cvs-in-insulin-antitrust-action","excerpt":"Florida Sues Lilly, Sanofi, CVS in Insulin Antitrust Action (3) Sept. 22, 2026, 10:51 PM UTC; Updated: Sept. 23, 2026, 4:49 PM UTC Alex Ebert Senior Correspondent","as_of":"2026-09-22","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"複方藥局 Strive 對 Lilly、Novo 提 GLP-1 反壟斷訴訟，德州聯邦法官認定未能主張可信的市場。","source":"Bloomberg Law: Eli Lilly, Novo Hit With Antitrust Suit From Drug Compounder","url":"https://news.bloomberglaw.com/ip-law/eli-lilly-novo-hit-with-antitrust-lawsuit-from-drug-compounder","excerpt":"Eli Lilly, Novo Hit With Antitrust Suit From Drug Compounder (1) Jan. 14, 2026, 10:03 PM UTC; Updated: Jan. 14, 2026, 11:44 PM UTC Nyah Phengsitthy Reporter","as_of":"2026-01-14","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Lilly 與美國政府的初步協議提供三年寬限期：Section 232 調查下的產品不課關稅，條件是達成美國製造投資承諾；定案協議仍在談判。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"The preliminary agreements also provide a three-year grace period during which time our products under a Section 232 investigation will not face tariffs, provided that we meet U.S. manufacturing investment commitments. We are currently in the process of negotiating definitive agreements to implement these arrangements.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Lilly 依賴中國供應商取得部分供應鏈（化學合成、試劑、起始原料），美方持續考慮限制對中依賴（含 BIOSECURE Act），替代供應商可能不可行或耗時。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"we, and the pharmaceutical industry generally, depend on China-based suppliers for portions of our supply chain, including integral chemical synthesis, reagents, starting materials, and ingredients. Finding alternative suppliers if and as necessary due to geopolitical developments or otherwise may not be feasible or could require significant time and expense","as_of":"2026-02-12","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"公司稱藥品目前豁免部分關稅但豁免可能終止；若未來加徵關稅，可能無法有意義地分擔成本。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"While pharmaceuticals are exempt from certain of these tariffs, such exemptions may be terminated or may not apply to any future tariffs.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Global Trade Alert：美國與 Lilly 的 MFN 定價協議含三年 Section 232 關稅豁免，實施日 2026-07-31。","source":"Global Trade Alert - Agreement with Eli Lilly on MFN drug pricing and tariff exemption","url":"https://globaltradealert.org/state-act/95136-united-states-of-america-agreement-with-eli-lilly-on-most-favored-nation-drug-pricing-and-tariff-exemption","excerpt":"United States of America: Agreement with Eli Lilly on Most-Favoured-Nation drug pricing and tariff exemption Announcement 06 Nov 2025","as_of":"2025-11-06","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-04-02 公告對專利藥及成分課 100% Section 232 關稅，有協議者20%、EU/日/韓/瑞士15%。","source":"Supply Chain Dive - Trump tariffs patented drug imports","url":"https://www.supplychaindive.com/news/trump-tariffs-patented-drug-imports/816550/","excerpt":"President Donald Trump is imposing a 100% tariff on patented pharmaceutical products and ingredients while also carving out reduced rates for certain goods and trade partners.","as_of":"2026-04-02","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Lilly FY2025 10-K 表示公司與整個製藥業依賴中國供應商提供部分供應鏈（化學合成、試劑、起始原料、成分）。","source":"Eli Lilly FY2025 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"depend on China-based suppliers for portions of our supply chain, including integral chemical synthesis, reagents, starting materials, and ingredients.","as_of":"2026-02-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"Lilly 在 FY2024 10-K 表示以庫存、備援廠區等手段維持供應。","source":"Eli Lilly FY2024 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947825000067/lly-20241231.htm","excerpt":"To maintain supply of our products, we use a variety of techniques, including comprehensive quality systems, inventory management, and back-up sites.","as_of":"2025-02-01","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Lilly 於中國投資累計近 60 億美元，含 30 億美元十年期 GLP-1 在地化製造與供應網路。","source":"Pharma Manufacturing","url":"https://www.pharmamanufacturing.com/quality-risk/supply-chain/article/55370318/eli-lilly-continues-to-invest-in-china-to-strengthen-local-production-of-glp-1-drugs","excerpt":"Lilly's total investment in China has reached nearly $6 billion, including $3 billion over the next decade to build a localized manufacturing and supply network for its GLP-1 drugs.","as_of":"2026-01-01","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Lilly 表示若 BIOSECURE Act 成為法律，可能影響製藥供應鏈部分環節。","source":"搜尋摘要（pharma 新聞引述 Lilly）","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"if the proposed BIOSECURE Act, which seeks to limit supply chain reliance on Chinese companies, becomes law in the U.S. it \"could affect elements of the pharmaceutical supply chain\"","as_of":"2026-02-01","retrieved_at":"20261102","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Lilly 非美國市場的產品供應多來自愛爾蘭；2024 年底愛爾蘭長期資產約 32 億美元。","source":"Nasdaq 分析文引述 Q1 2025 電話會議","url":"https://www.nasdaq.com/articles/heres-how-pharmaceutical-import-tariffs-could-affect-eli-lilly","excerpt":"most of his company's product sourcing outside the U.S. comes from Ireland","as_of":"2025-04-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收 $24.4B 年增 39%，量增 53%、實現價格下降約 15%；Mounjaro $10.7B(+65%，美國 $5.0B +41%，美國以外 $5.7B +93%)、Zepbound $5.35B(約+49%)","source":"Lilly Q3 2026 8-K 財報新聞稿 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000104/q326lillysalesandearningsp.htm","excerpt":"In Q3 2026, worldwide revenue was $24.4 billion, an increase of 39% compared with Q3 2025, driven by a 53% increase in volume, partially offset by a 15% decrease in realized prices. Key Products1 revenue grew to $17.1 billion in Q3 2026, led by Mounjaro and Zepbound.","as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 後 2026 全年營收指引上調至 $91–92B(前次 $85–87B)","source":"Zacks: LLY stock jumps as Q3 earnings beat estimates, 2026 sales view raised","url":"https://www.zacks.com/stock/news/3018734/lly-stock-jumps-as-q3-earnings-beat-estimates-2026-sales-view-raised","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"價格壓力：美國定價受 Zepbound/Mounjaro 影響，Mounjaro 納入中國 NRDL 壓低海外價格，Zepbound 現金自付價降低","source":"Lilly Q3 2026 8-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000104/q326lillysalesandearningsp.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"肥胖藥市場 2030 預測差異大(JPM GLP-1 類 >$100B、約 2,500 萬美國使用者；GS 基準約 $100B，近期更保守因價格侵蝕)","source":"J.P. Morgan Research: obesity drugs","url":"https://www.jpmorgan.com/insights/global-research/current-events/obesity-drugs","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 載明公私付費方鼓勵使用學名藥替代品牌藥，美國多數情況下藥師可（或須）替代；部分國家智財保護弱，須與上市後不久的學名版本競爭。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"Further, public and private payers typically encourage the use of generics as alternatives to branded products. Laws in the U.S. generally allow, and in many cases require, pharmacists to substitute generics that have been rated under government procedures to be essentially equivalent to a branded product.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子載明：AI 技術可能使競爭對手更快或更有效採用 AI 能力，且不保證 Lilly 的 AI 投資有效益。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"The rapid advancement of these technologies presents opportunities for us in research, manufacturing, commercialization, and other business endeavors but also entails risks, including that AI-generated content, 34 analyses, or recommendations we utilize could be inadequate, or that our competitors may more quickly or effectively adopt AI capabilities.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Novo 口服 Wegovy 於 2025 年 12 月獲 FDA 核准、2026 年 1 月上市；Pfizer 收購 Metsera（最高 110 億美元，月注射 GLP-1）；Amgen MariTide 中期試驗體重減輕最多約 20%；Viking 口服 VK2735 計畫 2026 Q3 進入 Phase III。Lilly 口服 orforglipron（Foundayo）為第二個獲批的口服減重藥。","source":"Reuters Factbox（經 TimesLive 轉載）Weight-loss drug developers line up to tap lucrative market as competition heats up","url":"https://www.timeslive.co.za/news/world/2026-04-01-weight-loss-drug-developers-line-up-to-tap-lucrative-market-as-competition-heats-up/","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Lilly 2025 年 4 月起控告遠距醫療業者販售複方（compounded）tirzepatide；2026-03-12 發出複方 tirzepatide 污染物警告；2026-06 與醫療中心就複方藥案提出撤銷訴訟。搜尋摘要稱 FDA 受理兩件 tirzepatide 學名藥 ANDA，來源品質低、未驗證。","source":"Mealey's：Lilly, Medical Centers File Stipulation Of Dismissal In Compounded Drug Row","url":"https://www.mealeys.com/mealeys/articles/2490487","excerpt":null,"as_of":"2026-06-16","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Lilly 口服 orforglipron（Foundayo）獲 FDA 核准，口服減重藥競爭展開","source":"DCAT Value Chain Insights","url":"https://www.dcatvci.org/features/oral-obesity-drug-battle-is-on-with-fda-ok-for-lillys-orforglipron/","excerpt":"Home » Oral Obesity Drug Battle Is On with FDA OK for Lilly’s Orforglipron Features Oral Obesity Drug Battle Is On with FDA OK for Lilly’s Orforglipron","as_of":"2026-04-02","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 稱近期表現受新增 incretin 通路與市場的需求與導入速度影響，且通路動態會對單期業績造成不成比例影響。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"as well as the demand and pace of uptake in new incretin channels and markets. More generally, incretin volume fluctuations due to channel dynamics or demand can have a disproportionate impact on our results of operations in any given period.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2026年1月 JPM 會議上 CEO Ricks 稱 LillyDirect 自推出以來服務約一百萬名客戶，並計畫推向全球（搜尋摘要轉述，未取得逐字原文）。","source":"Pharmaceutical Technology / PharmExec JPM26 coverage","url":"https://www.pharmaceutical-technology.com/newsletters/jpm26-eli-lilly-enters-2026-with-strong-momentum-given-pipeline-innovation","excerpt":null,"as_of":"2026-01-14","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Ricks 稱 LillyDirect 服務約一百萬客戶並計畫全球化","source":"PharmExec JP Morgan 2026 Eli Lilly","url":"https://www.pharmexec.com/view/jp-morgan-2026-eli-lilly-continuing-glp1-success","excerpt":"The conversation turned to the success of Lilly Direct, with Ricks explaining, “We scaled this direct platform (Lilly Direct) to consumers which has been a success. Basically a million people a month go online and buy GLP-1 medicine directly from a drug manufacturer.","as_of":"2026-01-14","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Lilly 於 2026-10-29 公布 Q3：營收年增 39% 至 $24.4B；全年營收 guidance 上調至 $91–92B（原 $85–87B），中點上調 $5.5B；non-GAAP EPS guidance 為 $35.00–36.00（搜尋摘要稱前次 $35.50–36.50，且含 Q3 $4.57/股 IPR&D 費用；來源間對 EPS 升降描述不一致）。","source":"Lilly Form 8-K Q3 2026 / chemxplore / Zacks 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000104/q326lillysalesandearningsp.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"財報前全年共識約營收 $88.7B、EPS $34.46（單一來源；Hudson Labs 列營收共識 $88,495M），新 guidance 營收區間高於財報前共識；Q3 營收共識約 $22.5B，Q3 營收含約 $900M 一次性利益（含 $410M Jardiance 里程碑）。","source":"搜尋摘要彙整（S&P Global preview / Hudson Labs / Zacks）","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/10/eli-lilly-earnings-preview-q3-2026","excerpt":null,"as_of":"2026-10-21","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布（財報前快照，非 Q3 後）：Benzinga 共識 Buy（29 位分析師）、平均目標價約 $1,237、最高 $1,600；Barchart 平均 $1,292.46、最高 $1,600（引用 7/28 Barclays $1,400）；RBC $1,500、UBS $1,425（2026-07）。頁面無明確日期，Q3 後修正未查到。","source":"Benzinga / Barchart / FN2 搜尋摘要","url":"https://www.barchart.com/story/news/3686486/eli-lilly-stock-analyst-estimates-ratings","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Zacks：Q3 財報優於預期、2026 銷售展望上調","source":"Zacks","url":"https://www.zacks.com/stock/news/3018734/lly-stock-jumps-as-q3-earnings-beat-estimates-2026-sales-view-raised","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Lilly raises 2026 guidance after Q3 revenue surge","source":"chemxplore","url":"https://chemxplore.com/news/lilly-q3-2026-financial-results-guidance","excerpt":"The company raised its 2026 full‑year revenue guidance to $91.0–$92.0 billion (up from $85–$87 billion), increasing the midpoint by $5.5 billion. Updated non‑GAAP EPS guidance is $35.00–$36.00.","as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Lilly 2026 年多筆併購，Bloomberg 報導截至 2026 年 5 月底已宣布併購總額逾 200 億美元，為公司單年最高；含 Ventyx（約 12 億美元現金）、三家疫苗公司（最高 38 億美元）。","source":"Bloomberg Law／New Star Tribune：Lilly Goes on $20 Billion Buying Spree as It Seeks Next Act","url":"https://www.newstribune.com/news/2026/may/27/lilly-goes-on-20-billion-buying-spree-as-company/","excerpt":null,"as_of":"2026-05-27","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-08-31 Lilly 同意以最高 28.75 億美元收購 Merida Biosciences（含里程碑付款），預期 Q4 交割。","source":"PYMNTS：Lilly to buy Merida for up to $2.9 billion","url":"https://www.pymnts.com/cpi-posts/lilly-to-buy-merida-for-up-to-2-9-billion/","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"FDA 於 2026-04-01 核准 orforglipron（品牌 Foundayo）用於成人肥胖／過重之慢性體重管理。","source":"Lilly Medical：Is Foundayo (orforglipron) approved and is it available","url":"https://medical.lilly.com/us/products/answers/is-foundayo-orforglipron-approved-and-is-it-available-309937","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261102","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"10-K 載明 Mounjaro／Trulicity／Zepbound 產品責任訴訟（含 GI 與 NAION 兩個聯邦 MDL，另有以色列與加拿大魁北克集體訴訟請願）、胰島素定價訴訟及 340B 集體訴訟持續進行。","source":"SEC EDGAR 10-K FY2025 Item 8 訴訟段落","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"Since August 2023, various plaintiffs have filed lawsuits against us, Novo Nordisk A/S, and other related entities, alleging injuries following purported use of incretin medicines, including Mounjaro, Trulicity, and Zepbound.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"SEC 8-K 近 12 個月 7 份，含重大項目者 1 份（2026-05-20 Item 8.01 為債券發行），無 4.02 重編項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000059478&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Lilly 2026 年多筆併購，Bloomberg 報導截至 2026 年 5 月底已宣布併購總額逾 200 億美元，為公司單年最高。","source":"Bloomberg Law／New Star Tribune：Lilly Goes on $20 Billion Buying Spree as It Seeks Next Act","url":"https://www.newstribune.com/news/2026/may/27/lilly-goes-on-20-billion-buying-spree-as-company/","excerpt":null,"as_of":"2026-05-27","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"2026-08-31 Lilly 同意以最高 28.75 億美元收購 Merida Biosciences，預期 Q4 交割。","source":"PYMNTS：Lilly to buy Merida for up to $2.9 billion","url":"https://www.pymnts.com/cpi-posts/lilly-to-buy-merida-for-up-to-2-9-billion/","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"10-K 載明 Mounjaro／Trulicity／Zepbound 產品責任訴訟（兩個聯邦 MDL，另有以色列、魁北克集體訴訟請願）與胰島素定價、340B 集體訴訟持續進行；搜尋未見 2026 年證券集體訴訟之已提起訴狀。","source":"SEC EDGAR 10-K FY2025 Item 8 訴訟段落","url":"https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm","excerpt":"In addition to the cases in the United States, there are two class action petitions in Israel, as well as a class action petition in Quebec, Canada.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"+","claim":"FDA 於 2026-04-01 核准 orforglipron（Foundayo）用於慢性體重管理，依據 ATTAIN 第三期計畫。","source":"Lilly Medical：Is Foundayo (orforglipron) approved and is it available","url":"https://medical.lilly.com/us/products/answers/is-foundayo-orforglipron-approved-and-is-it-available-309937","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261102","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"0","claim":"2026-03-12 Lilly 公開警告複方 tirzepatide 與維生素 B12 混合會產生化學雜質並呼籲回收複方產品；此為公司警示，非 FDA 對 Lilly 的行動，搜尋未見 2026 年針對 Lilly 自家產品的召回或 FDA warning letter。","source":"Boerse-Express 等報導（Eli Lilly Aktie 系列）","url":"https://www.boerse-express.com/news/articles/eli-lilly-aktie-branchenprognosen-aktuell-876933","excerpt":null,"as_of":"2026-03-12","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"經查 8-K 清單，近 12 個月 7 份 8-K 無 Item 4.02（財報不可信賴／重編）；唯一重大項目為 2026-05-20 債券發行 Item 8.01。搜尋亦未見近期 SEC 調查或重編。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000059478&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"LLY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":83.63,"operating_margin_pct":51.25,"fcf_margin_pct":13.52,"rd_intensity_pct":17.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"NVO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":80.65,"operating_margin_pct":43.13,"fcf_margin_pct":14.85,"rd_intensity_pct":17.64},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVO","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MRK","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.31,"operating_margin_pct":0.87,"fcf_margin_pct":18.72,"rd_intensity_pct":53.19},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"ABBV","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.48,"operating_margin_pct":33.94,"fcf_margin_pct":28.28,"rd_intensity_pct":15.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"AZN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":81.88,"operating_margin_pct":22.77,"fcf_margin_pct":9.85,"rd_intensity_pct":24.56},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AZN","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"LLY"},"financial_history":{"ticker":"LLY","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":28541400000.0,"revenue_yoy_pct":null,"gross_margin_pct":76.77,"operating_margin_pct":29.01,"net_income":6244800000.0,"diluted_eps":6.572215,"free_cash_flow":4600400000.0,"fcf_margin_pct":16.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":34124000000.0,"revenue_yoy_pct":19.56,"gross_margin_pct":79.25,"operating_margin_pct":30.26,"net_income":5240000000.0,"diluted_eps":5.8,"free_cash_flow":-3152000000.0,"fcf_margin_pct":-9.24,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":45043000000.0,"revenue_yoy_pct":32.0,"gross_margin_pct":81.31,"operating_margin_pct":37.83,"net_income":10590000000.0,"diluted_eps":11.71,"free_cash_flow":414000000.0,"fcf_margin_pct":0.92,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":65179000000.0,"revenue_yoy_pct":44.7,"gross_margin_pct":83.04,"operating_margin_pct":45.56,"net_income":20640000000.0,"diluted_eps":22.95,"free_cash_flow":5964000000.0,"fcf_margin_pct":9.15,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/LLY/LLY_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Eli Lilly and Company** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Ladies and gentlemen, thank you for standing by, and welcome to the Eli Lilly Third Quarter 2026 Earnings Conference Call. [Operator Instructions] I would now like to turn the conference over to your host, Mike Czapar, Senior Vice President of Investor Relations. Please go ahead.

**Mike Czapar** (Executives):
Good morning. Thank you for joining us for Eli Lilly and Company's Q3 2026 Earnings Call. I'm Mike Czapar, Senior Vice President of Investor Relations. Joining me on today's call are Dave Ricks, Lilly's Chair and CEO; Lucas Montarce, Chief Financial Officer; Dr. Dan Skovronsky, Chief Scientific and Product Officer; Adrienne Brown, President of Lilly Immunology; Dr. Carole Ho, President of Lilly Neuroscience; Ilya Yuffa, President of Lilly U.S.A. and Global Customer Capabilities; Jake Van Naarden, President of Lilly Oncology and Head of Business Development; Patrik Jonsson, President of Lilly International; and Ken Custer, President of Lilly Cardiometabolic Health.
During this call, we anticipate making projections and forward-looking statements based on our current expectations. Our actual results could differ materially due to several factors, including those listed on Slide 4. Additional information concerning factors that could cause actual results to differ is contained in our latest Form 10-K and subsequent filings with the SEC.
The information we provide about our products and pipeline is for the benefit of the investment community. It is not intended to be promotional or otherwise influence prescribing decisions. Our commentary will focus on our non-GAAP financial measures. Now I'll turn the call over to Dave.

**David Ricks** (Executives):
Thank you, Mike. Q3 was another quarter of solid execution. We delivered strong financial results, raised our full year financial guidance, advanced our pipeline and expanded our manufacturing footprint. Revenue grew nearly $7 billion compared to Q3 2025, and our key product revenue increased by over $6 billion. Within key products, revenue from our oncology, immunology and neuroscience portfolio doubled versus last year.
We continued the global rollout of Foundayo, launching in the U.K., Mexico and Saudi Arabia for people with obesity and in Mexico for people with type 2 diabetes. We achieved several key regulatory and pipeline milestones since our last call, including the U.S. approval of our new weekly insulin and new indications for Inluriyo, Jaypirca, and Mounjaro.
As part of the Medicare GLP-1 Bridge Program, we expanded access to obesity medicines in the U.S. for approximately 20 million seniors. Since the July 1 launch, more than 0.5 million people have filled a prescription for Lilly medicine through this program. We've heard positive feedback from patients and physicians about the initial implementation. Within the GLP-1 Bridge program, the Lilly portfolio is performing well. Among new Bridge patients, 7 out of 10 are starting on a Lilly obesity medicine. We're encouraged to see the strong uptake of the Bridge program and believe it has the potential to both improve outcomes for seniors and save costs for Medicare.
A recently published paper from the University of Southern California's Schaeffer Center for Health Policy & Economics estimated the expansion of anti-obesity medications in Medicare could deliver over $20 billion of cumulative savings over 10 years. This is an encouraging indicator of the magnitude of savings the GLP-1 Bridge program could generate.
We added to our pipeline through business development this quarter, acquiring AtaiBeckley and Merida Biosciences. We also progressed our manufacturing build-out to support our long-term growth outlook. We broke ground on 2 new manufacturing facilities, a $6.5 billion facility in Houston, Texas and a $5 billion facility in Richmond, Virginia.
We distributed $1.5 billion of dividends in the third quarter and executed $400 million in share repurchases. We launched the Lilly Change the Course Commitment. Through this new initiative, we set a new goal to reach as many people in resource-limited settings who have obesity and related diseases as in high-income countries prior to 2040.
Lastly, we announced Patrik Jonsson, President of Lilly International, will retire at the end of 2026. Ilya Yuffa will expand his responsibilities to include Lilly International as part of his -- as part of a newly created role called President of Lilly Global Markets. I want to thank Patrik for his many contributions over a successful 36-year career at Lilly.
And now I'll turn the call over to Lucas to review our Q3 results.

**Lucas Montarce** (Executives):
Thanks, Dave. As shown on Slide 7, Q3 was another quarter of industry-leading financial results. Revenue grew 39% compared to Q3 2025, driven by Mounjaro, Zepbound and a strong momentum across therapeutic areas and geographies. Gross margin as a percentage of revenue increased 80 basis points to 84.4% as favorable product mix and improved cost of production were partially offset by lower realized prices.
Marketing, selling and administrative expenses increased 14% as we invested in promotional activities to support current and planned product launches. R&D expenses increased 23%, driven by investment in our growing pipeline of early and late-stage programs and new molecules added through business development.
Our non-GAAP performance margin was 54.2%, an increase of 5.9 percentage points from Q3 2025, driven by revenue growth. Non-GAAP earnings per share were $7.48, including acquired IPR&D charges of $4.57. This compares to $7.02 in Q3 2025, which included $0.71 of acquired IPR&D charges.
On Slide 8, we quantify the effect of price, rate and volume on revenue growth. U.S. revenue increased 34% in Q3, primarily driven by volume growth from Zepbound and Mounjaro, partially offset by a 7% decline in price. U.S. price benefited from a favorable adjustment to estimates from rebates and discounts.
Excluding this adjustment, U.S. price declined 10%. Europe revenue grew 29% in constant currency, driven by sustained strong volume growth of Mounjaro. Growth also benefited from a $410 million onetime milestone payment related to Jardiance. No additional Jardiance milestone payment remains under our agreement with Boehringer Ingelheim.
In Japan, revenue grew 26% in constant currency, driven by Mounjaro and Kisunla. Mounjaro posted robust volume growth as share of new patient starts increased to over 50%. In China, revenue grew 62% in constant currency, driven by the uptake of Mounjaro. Mounjaro is the first medicine in China to exceed $1 billion of revenue during its first full year.
In Rest of the World, revenue grew 87% in constant currency, driven by Mounjaro, primarily in Korea, Turkey and Brazil. Q3 revenue was positively impacted by approximately $900 million of previously mentioned items, including milestones and changes to estimates for rebates and discounts.
On Slide 9, we provide an update on the performance of our key products. Within immunology, Ebglyss worldwide revenue grew 59% compared to Q3 2025. In the U.S., Ebglyss continued to gain share of new prescriptions in the specialty dermatology market and is the fastest-growing medicine in atopic dermatitis.
Oncology, Jaypirca had another strong quarter as worldwide revenue increased 59% compared to Q3 2025. In the U.S., Jaypirca was the fastest-growing BTK inhibitor as measured by total prescriptions. Inluriyo continued its impressive uptake in the metastatic breast cancer oral SERD market, exiting Q3 with more than 60% share of new U.S. prescriptions and 40% of U.S. total prescriptions.
In neuroscience, Kisunla revenue grew 175% compared to Q3 2025. Kisunla maintained its leadership position in U.S. amyloid targeting therapies. Diagnostic testing momentum continues to build and the number of p-tau217 blood tests more than doubled compared to Q3 2025, translating to more people being diagnosed with Alzheimer's disease and accessing treatment.
Finally, in cardiometabolic health, Mounjaro and Zepbound combined for more than $16 billion of revenue, contributing $6 billion of growth compared to Q3 2025.
As seen on Slide 10, total prescriptions in the U.S. incretin market grew 32% compared to Q3 2025. Oral GLP-1s and the Medicare GLP-1 Bridge program are expanding the number of people taking incretin therapy. In the U.S., total incretin prescriptions for obesity grew 82% in Q3.
Approximately 6 out of 10 total prescriptions and more than 7 out of 10 injectable prescriptions were for Lilly medicine. In the U.S., type 2 diabetes incretin total prescription grew 8% compared to Q3 2025. And the Lilly portfolio continues to lead here with more than 60% share of market. Outside the U.S., Lilly's portfolio again performed well. Slide 11 shows aggregate trends in international incretins, which have increased by 53% since the same period last year as measured by IQVIA gross sales.
Lilly strengthened its leadership position outside the U.S., gaining nearly 4 percentage points of share compared to Q2 2026 to reach approximately 58%.  Slide 12 provides an update on the Foundayo launch. In the U.S., total prescriptions and the share of new patients continue to rise.
Approximately 4 in 10 patients starting an oral obesity medicine choose Foundayo, and the number of new Foundayo patients in Q3 doubled from the previous quarter. We look forward to launching Foundayo in type 2 diabetes in the U.S. and expect regulatory action in Q4.
Outside the U.S., Foundayo has launched in 4 countries and is under regulatory review in more than 40 additional countries. We continue to expect a global rollout in all major markets in 2027. On Slide 13, we provide an update on year-to-date capital allocation. Moving to Slide 14 is our updated 2026 financial guidance. Based on a strong underlying performance across our portfolio, we now expect full year revenue to be between $91 billion and $92 billion. We saw strength in the U.S. driven by rapid uptake of the Medicare GLP-1 Bridge Program and outside of the U.S. from strong Mounjaro performance.
Given our updated revenue outlook, we now expect non-GAAP performance margin to be between 52% and 52.5%. We expect non-GAAP earnings per share of $35 to $36. This reflects an increase of $4.07 per share at the midpoint of the range before updates to the Q3 acquired IPR&D charges of $4.57 per share. We are pleased with our Q3 results and confident in our ability to deliver another year of industry-leading growth.
We will share our 2027 financial guidance on our Q4 call in January. However, I will share highlights on our initial thoughts regarding some of the pushes and pulls that we expect to impact our 2027 financial outlook. Beginning with the U.S. revenue, we expect sustained volume growth in the incretin market and the full year impact of the Medicare GLP-1 Bridge access and the launch of Foundayo in type 2 diabetes. Outside the U.S., we expect Mounjaro's leadership position to continue. We expect to launch Foundayo, which will drive additional market growth.
Consistent with prior years, we expect net realized price to be a headwind more than offset by volume growth. It is also worth noting that the 2026 revenue benefited from approximately $2 billion of onetime items primarily related to milestone payments and changes in estimates for rebates and discounts that we don't expect to recur.
Now I will turn the call over to Dan to provide an update on our pipeline.

**Daniel Skovronsky** (Executives):
Thanks, Lucas. Since our last earnings call, we've made progress across Lilly R&D. I'll begin in cardiometabolic health by recapping our most recent Phase III readout from our GIP, GLP-1 glucagon triple agonist, retatrutide. Just yesterday, we shared top line results from TRANSCEND-T2D-2, a head-to-head trial of retatrutide versus semaglutide in people with type 2 diabetes. As shown on Slide 15, retatrutide delivered greater A1c reduction and more than double the weight loss of 2 milligram semaglutide.
Retatrutide reduced A1c by 2.2% compared to 1.8% on 2 milligrams of semaglutide. These data demonstrate retatrutide can provide even more glycemic control than an approved diabetes medicine, provide a potential new treatment option. What's even more striking was the 20% to 21% weight loss achieved in people taking retatrutide compared to 9.4% weight loss in the semaglutide arm.
For people with type 2 diabetes who struggle to lose weight, retatrutide continues to demonstrate powerful weight loss alongside compelling glycemic control in this difficult-to-treat population.
Moving to another Lilly triple agonist, at last month's European Association for the Study of Diabetes meeting, we presented Phase II data for EloraTZP. EloraTZP is a combination of our selective amylin receptor agonist, eloralintide, and our GIP GLP-1 dual agonist, tirzepatide. As shown on Slide 16, EloraTZP delivered weight loss of 23.3% at 48 weeks for people with type 2 diabetes and obesity.
In a population that struggles to lose weight, this powerful combination delivered 57% more weight loss compared to tirzepatide, the world's most prescribed incretin. In addition, the highest dose combination of EloraTZP delivered A1c reduction of 2.9% at 48 weeks and more than 3 out of 4 patients achieved an A1c below 5.7%, a level associated with normal blood glucose.
Pending replication of these first-of-their-kind results in our Phase III trials, we believe this drug could meaningfully improve what is possible in the treatment of type 2 diabetes and obesity. And these data highlight the potential importance of treating with 3 physiologic hormones at once.
Moving to Slide 17. As one might expect, when rapidly escalating doses of a medicine with multiple mechanisms, the highest dose EloraTZP arm had a higher discontinuation rate due to adverse events. As we move into Phase III, of course, we will use a slower optimized dose escalation schedule, which we anticipate will improve tolerability.
Note that monotherapy eloralintide showed excellent tolerability with discontinuations due to adverse events lower than placebo. We look forward to beginning the Phase III trials of co-formulated EloraTZP imminently. We also presented results from ACHIEVE-4, the cardiovascular outcomes trial of orforglipron in people with type 2 diabetes and obesity with increased cardiovascular risk.
As shown on Slide 18, orforglipron met the primary endpoint of non-inferiority versus insulin glargine, reaffirming its cardiovascular safety profile. In additional prespecified analysis compared to insulin glargine, orforglipron showed a 16% lower risk of MACE-4. And for people fortunate enough to have been randomized to receive orforglipron in this trial, there was a 57% lower risk of all-cause death. These data complement the 6 previously presented Phase III trials for orforglipron and support the potential of orforglipron as a foundational daily oral treatment for people with obesity and people with type 2 diabetes.
Also in cardiometabolic health this quarter, in the U.S., we received 2 important FDA approvals. The FDA approved tirzepatide to reduce cardiovascular risk in adults with type 2 diabetes and the FDA approved our once-weekly basal insulin, insulin, insulin, efsitora alfa for adults with type 2 diabetes under the brand name Onswik.
Weekly basal insulin could significantly improve patient experience by reducing the number of injections compared to daily basal insulin.
Moving to oncology. The FDA approved pirtobrutinib for certain patients with previously untreated CLL or SLL based on the BRUIN CLL-313 Phase III trial. Pirtobrutinib reduced the risk of disease progression or death by 80% compared to bendamustine plus rituximab.
This approval underscores pirtobrutinib's versatility across the CLL continuum of care. It can now be used in the first-line setting for appropriate patients in addition to its valuable role in the relapsed or refractory post-covalent BTK Inhibitor set. The FDA also approved imlunestrant in combination with abemaciclib in ER-positive, HER2-negative ESR1 mutated advanced breast cancer.
The all-oral combination of imlunestrant and abemaciclib gives patients a treatment approach that targets the 2 central drivers of ER-positive breast cancer with an evidence-based treatment approach, an established tolerability profile and no new monitoring requirements.
We look forward to the results from EMBER-4, ongoing Phase III trial of imlunestrant in high-risk early breast cancer. Elsewhere in oncology, we initiated a Phase III trial with our PI 3-kinase alpha inhibitor, Tersolisib, in combination with a CDK4/6 inhibitor and endocrine therapy in advanced breast cancer.
Tersolisib is a mutant-selective PI3-kinase alpha inhibitor, intended to target the PI3-kinase mutations in breast cancer while sparing normal PI3-kinase in healthy tissue. We believe this profile could lead to efficacy in the first-line metastatic setting without as much of the toxicity as seen with other agents.
We now have 8 new oncology medicines or major new indications that are in Phase III trials or will start Phase III shortly.
Moving to neuroscience. We completed the acquisition of AtaiBeckley, adding a portfolio of neuroplastogens with potential to treat depression and other serious mental health conditions. We're pleased to welcome the AtaiBeckley team to Lilly and look forward to advancing multiple clinical programs together.
Moving to immunology. We shared positive Phase III results for lebrikizumab in people with moderate to severe atopic dermatitis of the hands and feet. Hand and foot atopic dermatitis is painful and difficult to treat, and these data show lebrikizumab can be a new option for patients without the need for topical treatments. We've submitted these data to the FDA for potential label update. We also shared 52-week results from Phase IIIb trials of ixekizumab and tirzepatide used together in people with psoriasis or psoriatic arthritis and obesity.
The ixekizumab and tirzepatide arm delivered greater improvements in skin and joint outcomes than ixekizumab alone, highlighting the importance of immunometabolic health. Earlier this month, we closed the acquisition of Merida Biosciences, which is developing MER511, a precision immunology therapy in Phase I for Graves' disease and thyroid eye disease.
This drug was designed to selectively degrade the disease-causing autoantibodies while preserving normal immune function. We're excited about the potential to help patients here, and we're pleased to welcome the Merida team to Lilly.
Slides 19 and 20 show pipeline movements since our last earnings call and the key events we expect in the remainder of 2026. We look forward to sharing more details about our pipeline at the upcoming Lilly Innovation Day on December 7. Although we won't have time to share everything we're working on, we'll do our best to curate a few examples that illustrate the depth and breadth of our capabilities and our pipeline at Lilly.
I'll now turn the call back to Dave for closing remarks.

**David Ricks** (Executives):
Dan. We're pleased with the progress in Q3 and throughout 2026. We delivered another quarter of strong financial results, advanced our pipeline through Lilly Research Labs and business development and started building 2 new manufacturing facilities in the U.S. to support our future growth.
While we continue to make excellent progress during a period of industry-leading growth, we remain focused on investing now to support our long-term vision to redefine how a pharmaceutical company can improve human health at a global scale. We've developed differentiated capabilities in R&D, manufacturing and commercial operations, where we're engaging directly with patients through platforms like Lilly Direct, changing the way people access health care.
Given the depth of our incretin pipeline, we expect our leadership position in cardiometabolic health and broad pipeline of next-generation obesity medicines to have an impact on global health for decades to come. And with 3/4 of our clinical pipeline focused on diseases outside of obesity, we're developing new medicines that has the potential to impact a broad range of disease to deliver diversified and durable growth for Lilly and our shareholders.
Q3 was another strong quarter and another step toward our long-term goals. Now I'll turn the call over to Mike to moderate the Q&A session.

**Mike Czapar** (Executives):
Great. Thank you, Dave. We'd like to take questions from as many callers as possible. So to that end, consistent with prior quarters. Please limit yourself to one question. Operator please provide the instructions for how to join the queue. And then we're ready for the first caller.

**Operator** (Operator):
[Operator Instructions] Our first question today is coming from Chris Schott with JPMorgan.

**Christopher Schott** (Analysts):
Congrats on all the progress. I guess a bigger picture one. You've raised guidance on the top line by roughly $10 billion year-to-date. I guess you reflect on what's happening here, just talk a little bit about what the biggest surprises have been as we think about U.S. versus OUS, cash pay versus commercial, et cetera. And probably as importantly, just when you think about these dynamics going forward, are we just seeing a fundamentally larger incretin opportunity than you anticipated? Or is this more of a pull forward of demand as we think about that kind of longer addressable TAM for the company?

**Mike Czapar** (Executives):
Thanks, Chris, for the question. Talk a bit about guidance and our outlook for incretins in the future, we'll go to Lucas.

**Lucas Montarce** (Executives):
Yes, Chris, thank you for your question. And I think the starting point, if you go back when we set up the guide at the beginning of the year, you may remember that we have that slide with, again, the opportunities and still events that we had in front of us for 2026. We talk about the launch of Foundayo in Q2.
We talked about starting the Medicare Bridge program. And then, of course, we talk about the variable of the growth all U.S., in particular, on the increase in out-of-pocket business and the runway of that growth. Again, what you see now in the latest guidance that we just shared today is actually a confirmation that we are tracking well across all of them, even better than what we anticipated.
So that's, I think, a positive confirmation of the strength and the solid performance that we continue to see. Going back to your second part of the question about the runway of that, is that pulling forward or not? We think about it, if you look at just the incretin business, we're still scratching the surface on the number of patients that we can reach.
You look at the U.S. and we're talking about 1 out of 10 patients that we are reaching nowadays. And even OUS, we are talking about 2 patients out of 100 patients. So it's actually a really low base. So the number seems really big, $16 billion this quarter of incretin business. The runway of opportunity of growth is still for many years to come from my perspective. And on top of that, we continue to expand the breadth across all the therapeutic areas. Super also happy to report the 100% growth on the rest of the key products across oncology, immunology and neuroscience. So that's just to give you some color about the short term and how we think about also long term.

**Operator** (Operator):
Our next question is coming from Geoff Meacham with Citi.

**Geoffrey Meacham** (Analysts):
I want to ask about what data you have on tirzepatide persistency in obesity just over the course of the past year or so? And importantly, when you look to next year, would you expect Foundayo and retatrutide to be different than that in terms of real-world experience?

**Mike Czapar** (Executives):
To talk about tirzepatide persistency in obesity and thoughts on the pipeline looking in the future, we'll go to Ilya.

**Ilya Yuffa** (Executives):
Geoff, thanks for the question. What we've seen in persistency and actually before we even launched Zepbound and we've had success with Trulicity in the past, and that was kind of the standard of what is possible for chronic medicine for adherence, which ended up becoming around 16 to 18 months of adherence. What we're seeing with Zepbound is that in the covered space, we continue to see the trajectory of being just as beneficial in terms of adherence as we've seen in Trulicity.
And even in the self-pay, we're seeing that close to the covered market. So the persistency actually for a chronic medication Zepbound is doing extraordinarily well. Now expectations for oral, it's still early. But as typical chronic medications as long as you take a look at orals, they typically are lower adherence overall relative to weekly injectable therapies, and that's what we expect to see.
One additional data point that I think will be important as we look at even the success of Bridge, early days in Bridge, having a low out-of-pocket helps with that friction point, and we're seeing improved adherence in Bridge. So that will all play out as part of the different friction points, both in terms of out-of-pocket as well as the benefits that people gain from these therapies.

**Operator** (Operator):
Our next question is coming from Seamus Fernandez with Guggenheim.

**Seamus Fernandez** (Analysts):
I'm going to do the non-obesity question. Kisunla is actually starting to show the prospect of becoming a blockbuster product and starting to grow faster, maybe a little bit faster overseas. But I was hoping, Dan, you might weigh in on the prospects for TB3, the prospects for success and how you see that program really evolving the treatment paradigm should it succeed, particularly in the context of some of the novel tau biomarkers that we're starting to see.
I think there are a lot of questions from investors that we get on what really is the market opportunity here given the Kisunla uptake, but it does seem like some of those behaviors are changing.

**Mike Czapar** (Executives):
Thanks, Seamus. Always welcome neuroscience questions. So we'll go to Carole to talk about our prospects for Kisunla and maybe even kind of the neuroscience space more broadly.

**Carole Ho** (Executives):
Yes. We're very excited to see the growth of Kisunla over the last year, and this growth is both driven by our confidence in this product with its convenient 30-minute infusion time, once monthly dosing and the opportunity for treat to clear in this patient population.
We've also seen a tremendous growth in the opportunity for diagnosis with blood-based biomarkers with p-Tau217 becoming available. And we see this becoming a diagnostic that enables access to early diagnosis potentially even in primary care offices in the future.
As we look at TRAILBLAZER-3, which is our study looking at prevention in cognitively unimpaired people looking at prevention of progression to early symptomatic Alzheimer's disease, these biomarkers will certainly also enable early diagnosis for people that have risk concerns about their cognition before loss of their cognition. So we're excited both about the growth in early symptomatic Alzheimer's disease, but also if TRAILBLAZER-3 reads out positively, really expanding this market to earlier stages of disease where we already have preliminary evidence from our early symptomatic Alzheimer's disease space that treating earlier will have a more significant impact on cognition.

**Operator** (Operator):
Our next question is coming from Evan Seigerman with BMO Capital Markets.

**Evan Seigerman** (Analysts):
Bigger picture one here. So clearly, the incretin franchise is becoming an enormous earnings driver, but also raises the question of what comes next. When you look beyond the cardiometabolic disease, where do you see the best opportunity to build Lilly's next multibillion-dollar growth pillar? Does recent BD activity suggest that neuroscience and immunology are emerging as higher strategic priorities?

**Mike Czapar** (Executives):
Thanks, Evan, for the question about the next big opportunity after incretins. We'll go to Dan to talk a bit about some of the pipeline opportunities he's excited about.

**Daniel Skovronsky** (Executives):
I would say that we're excited about all 3 of our other therapeutic areas, which are immunology, neuroscience and oncology. And the BD activity reflects not just our strategic intent to grow those areas, but the intersection of that strategic intent with assets that are actually out there and are attractive to us. 
Oncology is probably the space where we've made the most progress, and we highlighted 8 really important late-stage programs, several of which could be quite large in size. For example, the recent Kelonia acquisition, which targets myeloma, is a huge opportunity if the data continue to hold out the way we expect them to. Neuroscience, of course, is the area that has the largest unmet medical need and really the least progress in the pharmaceutical industry towards addressing that.
We're firmly committed to making a difference for patients in this space. And you can see our acquisitions in sleep and psychiatry, combined with our in-house expertise in neurodegeneration are aimed to really grow that market on behalf of patients.
And then finally, immunology, I think there's been a lot of crowding in immunology on a few probably important targets, but we also see a great opportunity actually to raise expectations in immunology with breakthrough therapies that I think can deliver efficacy that's never been seen before. And that's what we're trying to do with programs like the Merida acquisition or the Orna acquisition, which is aimed at immune reset. So lots of growth opportunities across those areas.

**Operator** (Operator):
Our next question is coming from Kerry Holford with Berenberg.

**Kerry Holford** (Analysts):
I wonder if you could speak a little more about Medicare Bridge. How does the split between injectable and pill in that channel differ from others? It seems like the majority of Medicare demand is injectable. I wonder if that surprised you with regard to your products in that space. And also, could you talk to what proportion of patients in that Medicare channel for the Bridge program specifically are naive versus existing patients transferring from other channels?

**Mike Czapar** (Executives):
We'll go to Ilya to talk a bit about Bridge, the injectable versus pill split as well as the naive versus switches.

**Ilya Yuffa** (Executives):
Yes. Thanks for the question. For Bridge-1, it's performed extraordinarily well. I think we knew that it was going to be a significant benefit for seniors. The program itself is simple in understanding the criteria and the low out-of-pocket. And so all of those things combined, we have seen about 3/4, 75% of people coming into Bridge going into injectable therapy, 7 out of 10 in total choosing Lilly medicine. And so we've performed really well across Bridge.
That is higher than maybe some of the self-pay segment. One of the components of that is the same low out-of-pocket and getting the greatest efficacy in the standard of care that's been established in obesity has favored Zepbound in particular. But we're seeing good growth and uptake of orals and Foundayo as well.
In terms of expanding the number of people actually being treated after the first bolus of people coming into Medicare, we're seeing now at about 80% of the people getting treatment under bridge are naive or have not been on incretin therapy in the past. And so we see this as a significant driver of access long term. And it's still early days. And while it's performing above our expectations, we see continued opportunity here to expand access and utilization and not only improve care of seniors, but as we shared earlier on independent study, also the potential of saving significant amount for Medicare overall.

**Operator** (Operator):
Our next question is coming from Asad Haider with Goldman Sachs.

**Asad Haider** (Analysts):
Congrats on all the progress. Maybe just back to Foundayo. Thanks for the comments earlier, and I know that's still very early in the trajectory. But just curious to hear any updated framing on how the launch is playing out both in the U.S. as well as internationally in the context of both competitive dynamics versus oral Wegovy and then your own internal expectations. And then on the titration schedule for Foundayo, the 2 lower doses still represent about 75% -- 75% to 80% of TRx in recent weeks. So where do you see that going at steady state?

**Mike Czapar** (Executives):
I think we'll start maybe with international and go to Patrik to talk a bit about some of the ex-U.S. launches and then maybe a couple of nuggets on the U.S. as well.

**Patrik Jonsson** (Executives):
Thank you very much. We have now launched in 4 markets outside the U.S. We started with UAE very late in Q2. In the second half of Q3, we launched in U.K., Saudi and Mexico. I would say that so far, the launch is very much in line with our expectations. There are a lot of similarities with the learnings from the U.S. in terms of orals are truly expanding the market, and we see a huge amount of patients actually being new to incretins. In Middle East, I think we have a geopolitical situation to take into account, but we are the market leader in UAE with competition from Wegovy. In Saudi, we have launched in both type 2 and chronic weight management, and we have a good uptake there.
U.K., we have been subject to the pre-vetting requirements by the MHRA. So we have actually not been able to fully promote until now in October, but the signs here are also that the orals are expanding the market. Mexico, week 6, a very good uptake and actually slightly above our expectations. But most importantly, I think we see that there is a lot of work to be done here, and we need to do all of the work that has been done in the U.S. as well.
We recently got the CHMP positive opinion that should hopefully result in a regulatory approval by year-end, and we are ready to launch across chronic weight management and type 2 diabetes in more than 40 markets next year. But the initial focus is going to be on cash pay and chronic weight management since type 2 reimbursement will take some time.

**Ilya Yuffa** (Executives):
Yes. And in the U.S., we've made significant progress since last quarter. We've seen over 0.5 million TRx in the quarter, but the fundamentals and some of the key indicators that we've been talking about as part of our initial launch have been moving in a really positive direction.
Consumer awareness and interest has improved with our investment in campaign with Martha Stewart. You're seeing also number of trialists have more than doubled since last quarter. And so we're seeing good progression of adoption from providers. And that's showing up in our share of market.
So our NBRx share market is approaching around 4 out of 10. And so good progress overall for the growth of Foundayo in the oral segment. And even in the sequential growth of orals within -- from Q2 to Q3, we're taking 45% of that growth with Foundayo. In terms of the titration, it's expected that it takes time to titrate to the maintenance doses.
But we've actually seen good progress on our maintenance doses. We have multiple maintenance doses. So about 25% of people are at one of our maintenance doses. That's actually higher than what you see on Wegovy pill. And so we're encouraged by that. Of course, that's something we continue to monitor, but the experience overall that we're seeing both from provider and consumer has been positive.

**David Ricks** (Executives):
I would just add, we're under review for type 2 diabetes, and we see that as an extraordinary opportunity for Foundayo as well. Remembering today in the U.S., roughly half the volume of GLP-1s is in diabetes. So that's a big market expansion. Of course, you need to access reimbursement when we get that, but that's very promising sort of another leg to the stool here for the Foundayo performance.

**Operator** (Operator):
Our next question is coming from Steve Scala with TD Cowen.

**Steve Scala** (Analysts):
This is a follow-up to Chris' earlier question. And with all due respect, Lilly's financial guidance hasn't been a good predictor on ultimate results. And I'm curious what is the most frequent source of the surprise? So specifically, has it tended to be positive unit developments? Or has it been lack of negatives on price? Or is it some desire to just lean incredibly cautiously on guidance? And if it's the latter, why is that? A key for investors, I think, is to determine when the surprise factor runs its course. So any color would be appreciated.

**Mike Czapar** (Executives):
Thanks, Steve, for the good direct question. We'll go to Lucas to maybe provide a little extra color on guidance. And David, if you want to add anything, feel free as well.

**Lucas Montarce** (Executives):
Yes, Steve, thank you for the question. I think in terms of the variables that I described on the first question, there are still, again, the variables that we had when we started the year that, of course, again, now with yesterday newspaper, you think about that, again, we are performing way much better than what we had initially guided to.
But if you look at the runway of that growth across the U.S. and OUS has been all the events we were public about again, that the unknowns associated with that. Starting with the Bridge program, when that was Bridge program will start, the uptake of that as well, the progression of OUS. markets, both in share and also penetration.
And those all played out better than what we anticipated. So still the drivers are those ones. Again, we continue to guide to what we forecast in our internal bottom-up approach that we have on our forecasting model and try to be as public as possible about how we see the projections and now we provided some perspective into 2027 as well.
So I think from my perspective, we continue to drive, again, a very thorough process every single quarter and be public about, again, the variables that could affect positively or negatively as well our guidance projections.

**David Ricks** (Executives):
Yes, Steve, I appreciate the question. You followed the company a long time. Our goal is to give as accurate projections as we can. But of course, there's asymmetry with missing on the downside. That's like everyone's impulse. But let's remember, like we're in the middle of the largest new category expansion in the history of the pharmaceutical industry and Lilly is leading that.
So there's a number of things that have never actually happened before that we're trying to project. And we prefer to a posture that investors can rely on versus one that is more speculative. And at the JPMorgan conference at the beginning of the year, I said there's like 2 big variables this year. If I knew the answer to you, we would have had a tighter range.
One was the uptake in Bridge, which we didn't really know. We weren't even sure about the start time of Bridge at that point. And the other was the depth of the consumer purchasing internationally and whether we were really just skimming very high net worth individuals in these out-of-pocket markets or if more middle-income households would be interested in improving their health and losing weight at scale.
And I think both of those this year turned out to be positive for us, thus the roughly $10 billion improvement over first-time guide. As time goes on, I suspect we'll have fewer and fewer of those never before done things and the guidance can become more predictable. So I appreciate the question, but that's sort of how I've seen it over the last 3 years.
And we're beating on the up, that's better than missing on the down. And I think that's good news mostly not because of the earnings beats, but because we're actually executing against a really scaled opportunity and performing well.

**Operator** (Operator):
Our next question is coming from Terence Flynn with Morgan Stanley.

**Terence Flynn** (Analysts):
Maybe one on the pipeline for Dan. There's been a growing focus on longer-acting incretins. You guys recently said you have 3 different programs in the clinic. So just wondering if we can expect any clinical data at the R&D Day on these programs or if you can tell us what the stages of development because I think that is probably the only hole you have in your incretin pipeline.

**Mike Czapar** (Executives):
We'll actually go to Ken to talk about the long-acting approach and if there's anything to share beyond what's been public.

**Kenneth Custer** (Executives):
Thanks for the question, Terence. So as we discussed previously, we do see an opportunity for longer-acting incretins, particularly in a category that's big with such a consumer emphasis. We're taking the same approach we usually do when we see an important square on the board that we want to fill, which is baking off several competing platforms to see which one provides the best product possible.
This is a space where we think the molecule properties are really going to matter. And so that's why we haven't signaled anything yet, but it is because we have multiple efforts in the clinic. Those are a range of different technological approaches, including existing time extension technologies as well as ones that could be part of the future. And then we have other efforts that we've disclosed in business development around formulation technologies. Again, we'll look at all these data and make an informed decision on which effort or efforts to advance to Phase III.

**Operator** (Operator):
Our next question is coming from Trung Huynh with RBC.

**Trung Huynh** (Analysts):
So as you look to '27, what are you seeing in terms of opt-in trends for GLP-1 coverage amongst the larger employers in the U.S.? And with those dynamics in mind and Bridge continuing to ramp, could your U.S. channel mix meaningfully evolve next year? So it potentially creates additional pricing pressure amongst the mid-teens decline that you've absorbed in '26? Or could we see pricing headwinds in the same range for '27?

**Mike Czapar** (Executives):
I'll go to Ilya to talk about 2027 early opt-in trends and maybe the broader access environment as well as we look into next year?

**Ilya Yuffa** (Executives):
Yes. Overall, obviously, there's been noise around a number of employers opting out of coverage. At the same time, we're having positive discussions for Employer Connect  and other channels on improving access there as well. Our expectation is that overall, access on the commercial side will maintain relatively stable through 2027.
Obviously, we continue to have conversations to improve on that. The main access improvements overall for '27 will more likely be predominantly growth of Medicare and Medicaid as opportunities for expanded coverage. That will have a segment mix more towards a lower price, lower net price, not about decreasing the price overall, but more just a segment mix.
That as well as some level of self-pay in the lower net price per TRx. And in terms of commercial overall pricing, I would expect a modest and disciplined approach around pricing and access to maintain. But overall, stable on the commercial and increased coverage in Medicare and Medicaid.

**Operator** (Operator):
Our next question is coming from Akash Tewari with Jefferies.

**Akash Tewari** (Analysts):
So your team has talked about generally predictable and consistent GLP-1 pricing declines in the U.S. out to the end of the decade. How does that look ex U.S.? Could we see more stability there than maybe investors expect? And how do you think about the net price per patient in the U.S. versus international markets ex China evolving over time? It currently seems quite similar.
And Dave, you mentioned something interesting. Can you talk a bit more about the size of this emerging middle-income cash pay international market opportunity relative to what we've seen in the U.S. so far?

**Mike Czapar** (Executives):
It sounds like the question is for Patrik. So talk a bit about pricing expectations kind of on the cadence from here, thinking about net price U.S. versus ex U.S. and anything about the emergence of a middle income cash pay market?

**Patrik Jonsson** (Executives):
Yes. Thank you very much. We have taken a very disciplined approach to pricing OUS. And I think we have seen that both providers, consumers and payers are willing to pay for a differentiated product. And we have seen that even after the launch of generics in India, Brazil and Canada, we are holding our shares and continue to grow. And that's a discipline that we will continue to apply.
In terms of the out-of-pocket willingness, we actually see quite a big willingness to pay out-of-pocket OUS as well. Of course, when markets are getting further penetrated and like the U.K., where we launched more than 2 years ago and where we have a penetration very much along the lines of the U.S., we see a lower growth as we expected. But I think overall, taking into account where we are penetration-wise, low single digit long term, we see a tremendous opportunity OUS for the incretins and we will continue our efforts as well to gain type 2 reimbursement, which is very important. And we made some progress in Q3 here now having 9 European markets covered, but we will continue those efforts and continue to take a disciplined approach in terms of pricing.

**David Ricks** (Executives):
Maybe just to comment on the ex U.S. versus U.S. I mean our goal because of the consumer nature of this is to put much tighter band of pricing on obesity medicines than maybe you've seen historically in other medicine categories.

**Operator** (Operator):
Our next question is coming from Umer Raffat with Evercore.

**Umer Raffat** (Analysts):
I wanted to spend a quick second on a potentially sizable opportunity in early breast cancer for imlunestrant. And I understand there's a planned interim for you guys, a competitor trial stopped on interim. A, how should we think about early stoppage odds for your trial? And perhaps more importantly, if you could put the effect size comparisons versus lidERA in perspective, knowing that the treatment setting for you is a little more real world with meaningful post-CDK4 penetration.

**Mike Czapar** (Executives):
We'll go to Jake to talk a bit about EMBER-4.

**Jacob Van Naarden** (Executives):
Yes. Super excited about Inluriyo, both in its current actual commercial performance, where it's doing great in helping lots of people with monotherapy and new combination with Verzenio. And as you mentioned, the real big opportunity is in the adjuvant setting with the EMBER-4 study. We've not talked about interim analysis on the study. We've been pretty consistent that we expect the study to read out in 2027 next year. So we're sticking with that. That is what we expect. I think you're raising a good point. The treatment setting that we're exploring is much more real world, I think, than what was examined in lidERA, both in the context of the prevalent population that exists that may want to switch from existing endocrine therapy to new oral SERD.
And a study run in the context of modern standard of care of CDK4/6 inhibitors like Verzenio, which our study had and there's didn't. So a bunch of differences. I think when our study does read out successfully, I hope it will be much more relevant to clinical practice and easy to understand how to slot it in. I don't want to comment on anticipated effect sizes because we just need the study to read out and see what it shows us, but excited to get to that point.

**Operator** (Operator):
Our next question is coming from Carter Gould with Cantor.

**Carter Gould** (Analysts):
Congrats on the quarter. Maybe just to go back to the Bridge program. Have you had conversations with the admin or the various Part D sponsors that give you confidence this program will either be extended or balance will be revisited in a different iteration, I guess, to the point, just your confidence that there won't be a disruption at the end of '27.

**Mike Czapar** (Executives):
I'll go to Dave to talk a bit about our discussions with the administration.

**David Ricks** (Executives):
Yes. Well, I think we're pretty optimistic about expansion, I think, for 3 reasons, Carter. One is the early uptake is strong, and I think you see both demand and appropriate on-label use of the medications. The administration did a fantastic job implementing the PA criteria in a way that was not kind of over-indexed or under-indexed. And I think if we look at the people using the medicines, relatively high BMI, comorbid people. And that leads to the second point, which is cost effectiveness.
And I think we highlight today that independent study from USC that estimates not just breakeven, but like massive cost savings for Medicare due to this program. The CMS will -- because it's being done as a pilot program, will do their own analysis. But I think all signals now point to a pretty successful cost effectiveness, which could yield either a legislative or a regulatory shift in the coverage permanently.
In the meantime, I think there's a lot of energy with the people running CMS at the current point to continue this and the right way to do that is put this into the Part D benefit. So I would expect and it's probably a good conversation to have on our Q1 call, this to then shift to working with the carriers for the '28 calendar year. And we'll certainly work with the administration and all our partners who supply Part D coverage to have good access across our portfolio and continue the success of the program so far.

**Mike Czapar** (Executives):
Thanks, Dave. We'll try to squeeze in 2 more if we could, please.

**Operator** (Operator):
Our next question is coming from Michael Yee with UBS Securities.

**Michael Yee** (Analysts):
Maybe just a long-term portfolio question around obesity and how you view a consumerism-driven market where people will gravitate towards differentiated or different options within your portfolio. So I'm thinking about retatrutide and amylin.
Can you maybe just put on your prediction hat about what that portfolio would look like and how consumers would choose between these different products given various competition and price declines?

**Mike Czapar** (Executives):
We'll go to Ken to talk about the breadth of the obesity portfolio and how to think about what patients each are for.

**Kenneth Custer** (Executives):
Yes. Thanks, Mike, for the question. I mean maybe let's start with the size of the problem we're confronting here is 110 million or so people living in the U.S. with obesity or overweight internationally. That number has a B at the start of it. That's why we're pursuing a portfolio approach knowing that many individuals will seek out and find over time what works best for them.
Each of the molecules in our growing portfolio, they have unique features and probably each of them can fill multiple roles. We talked about how Foundayo is a great on-ramp for patients earlier in the weight loss journey, but can be a great maintenance option as well. Tirzepatide, we see as sort of a cornerstone with a growing body of evidence to support it including SURMOUNT-MMO very soon.
And then as we focus on Reta, this is a medicine that looks like it could do a lot of jobs on the high end, delivering tremendous power, the lower end, delivering a lot of simplicity and really differentiated responses in some important subpopulations, including men and type 2 diabetics, where it's the first agent that's ever shown greater than 2% -- or excuse me, 20% weight lowering.
Beyond that, we have our selective amylin portfolio, which opens up a new pharmacological access that can offer incretin-like weight lowering with really more placebo-like GI tolerability. And then last but not least, EloraTZP, we see this as sort of the most physiological approach yet to weight loss that could also again play a lot of roles in this, including providing really differentiated HbA1c lowering in patients with type 2 diabetes. So again, all of these agents, we think they can play a lot of roles.
We probably can't a priority stipulate for any individual patient what's going to work best for them. But what's important to us is that we offer all of them, we offer choice. We put them on really a platform with a consistent appearance experience that allows patients to start, switch and step up to any Lilly medicine that works best for them. And overall, no matter which one they choose, they'll still be on a Lilly medicine.

**Mike Czapar** (Executives):
We'll go to the last question, please.

**Operator** (Operator):
Our final question is coming from Courtney Breen with Bernstein.

**Courtney Breen** (Analysts):
I know we've spoken a little bit about the pipeline, but I instead wanted to think about other sources of innovation and namely the M&A that you've been doing and licensing that you've been doing externally to support your pipeline.
Obviously, there's been a rapid pace for the first part of this year. Can you just help us understand where you believe you're at in terms of the risk/reward balance across your portfolio, the types of areas that might be of interest to continue adding and how you're kind of ensuring that you're keeping the bar high as you continue to take on and broaden this pipeline kind of beyond what we see in Phase II right now?

**Mike Czapar** (Executives):
Yes. We'll go to Jake to talk a bit about the kind of BD strategy, the process to assess different transactions and kind of the interest across the board.

**Jacob Van Naarden** (Executives):
Yes. Thanks for the question. It's funny. You mentioned risk reward. Risk is really our friend here. Risk allows us to actually create value. And one of the ways we can deploy that for the reasons we can is because we don't need revenue tomorrow. I think we have this opportunity while the incretin business and the rest of the commercial businesses are doing so well to plan for the next decade or 2 ahead, which allows us to take more risk in a calculated way.
And some of that is very early-stage dealmaking, which oftentimes are not really even press released by us. So some of those you don't maybe know as much about. And we've done a bunch of, I would say, clinical stage, but not super late-stage clinical deals this year where we see enough risk still within the program for us to create value, but enough derisking for us to feel confident that there's a real medicine or maybe more than one medicine there. And we can point to a handful of deals even on the year this year that fit that paradigm.
So I think you'll see more of both of those categories from us across all the therapeutic areas. We're not solving for any one given therapeutic area. We're just solving for great products, great science and great people that we can bring into the company and fuel growth into the decades to come.
I think that gives us a competitive advantage, frankly, in how we look for what we want to take inside relative to our peers. So we have a pretty rigorous process to stay disciplined on a deal-by-deal basis, and I'm excited about what we've done so far and what's to come.

**Mike Czapar** (Executives):
We'll go to Dave for a couple of closing comments.

**David Ricks** (Executives):
Okay. Excellent. Thanks for joining us for today's call. Obviously, a strong quarter for the company. I want to take a moment, though, to promote an upcoming event, which is our December 7 Investor Day. This will really be an R&D and pipeline-focused day. We'll have other sections in that as well. And I hope all of you can join us live or if not, remotely for that event.
I also want to take a minute just to again congratulate Patrik on a great career, and I think this will be your last earnings call with us. You played a big part in our success over the last 30 years of your career, but certainly the most recent 6 or 7. So thank you, Patrik, for everything. Please follow up with the IR team if you have additional questions we didn't get to and look forward to seeing everyone in early December.

**Operator** (Operator):
Thank you. This does conclude our conference for today. This conference will be made available for replay beginning at 1:00 p.m. today and running through 11/26/26  at midnight. You may access the replay system at any time by dialing (800) 332-6854 and entering the access code 938904.
International dialers can call (973) 528-0005. Again, those numbers are (800) 332-6854 and 973 528-0005 with the access code 938904. Thank you for your participation, and you may now disconnect your lines.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LLY_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜guidance：CFO說明上調2026全年營收財測區間（原話："between $85 billion and $87 billion."）
- 2026-08-05｜CFO｜guidance：CFO給出non-GAAP performance margin財測區間（原話："performance margin to be between 49% and 50.5%"）
- 2026-08-05｜CFO｜guidance：CFO給出non-GAAP EPS財測區間（原話："non-GAAP earnings per share of $35.50 to $36.50"）
- 2026-08-05｜CFO｜guidance：CFO回答下半年隱含減速問題時，稱Q2含一次性及前期回扣估計調整，下半年不預期延續（原話："Those, of course, we don't expect that will continue"）
- 2026-08-05｜CFO｜guidance：CFO指出下半年財測已納入歐洲Q3假期季節性（原話："We always have the seasonality in Europe in Q3"）
- 2026-08-05｜CFO｜margin：CFO報告Q2毛利率（原話："Gross margin as a percentage of revenue was 86.3% in Q2,"）
- 2026-08-05｜CFO｜margin：CFO報告Q2 non-GAAP performance margin（原話："performance margin was 54.8%"）
- 2026-08-05｜CFO｜margin：CFO說明行銷銷售管理費用年增25%（原話："administrative expenses increased 25%,"）
- 2026-08-05｜CFO｜margin：CFO說明Q2 EPS含收購IPR&D費用（原話："Non-GAAP earnings per share were $8.38"）
- 2026-08-05｜CFO｜margin：CFO拆解美國價格：Q2受回扣與折扣估計變動影響（原話："U.S. price benefited from a change to estimates for"）
- 2026-08-05｜CFO｜margin：CFO給出剔除估計調整後的美國價格變動（原話："adjustments, U.S. price declined by 9%."）
- 2026-08-05｜CFO｜margin：CFO表示價格將因CVS恢復納入而下降，已納入財測，並以量成長抵銷（原話："actually go down for sure because of this"）
- 2026-08-05｜CFO｜commitment：CFO承諾以銷量成長抵銷價格下降（原話："we are going to more than offset that with volume"）
- 2026-08-05｜CFO｜competition：CFO稱已確立市占領先，海外成長將靠市場擴張（原話："with market share leadership already established,"）
- 2026-08-05｜CFO｜competition：CFO稱Lilly為全球incretin市場領導者（原話："Lilly is the global market leader"）
- 2026-08-05｜President of Lilly International｜competition：國際長：印度、巴西學名semaglutide上市後Mounjaro處方仍成長（原話："we continue to see TRx growth for Mounjaro"）
- 2026-08-05｜President of Lilly International｜competition：國際長：觀察到學名藥廠供應受限（原話："generic companies actually having significant supply"）
- 2026-08-05｜President of Lilly International｜competition：國際長：UAE第二個口服藥進場後Lilly合併incretin市占持平（原話："Lilly's combined incretin share, held steady"）
- 2026-08-05｜CEO｜product：Foundayo美國糖尿病適應症申請已完成，預期年內有監管動作（原話："expect regulatory action later this year."）
- 2026-08-05｜President of Lilly USA｜product：美國區總裁稱Foundayo七月最後一週處方量接近一個月前的兩倍（原話："almost doubling the volume that we had just a month ago"）
- 2026-08-05｜President of Lilly USA｜product：美國區總裁更新Foundayo處方醫師數（原話："we talked about 8,000 prescribers."）
- 2026-08-05｜President of Lilly USA｜product：美國區總裁：處方醫師增至36,000（原話："now increased that to 36,000 prescribers."）
- 2026-08-05｜CSO｜product：首席科學長說明ACHIEVE-3為口服GLP-1首次頭對頭（原話："first head-to-head comparison of two oral GLP-1s"）
- 2026-08-05｜CEO｜product：CEO說明retatrutide BLA路徑的法院判決與訴訟狀態（原話："There was a mixed decision in the -- first decision"）
- 2026-08-05｜CEO｜product：CEO稱仍需補充CMC資料才能送件（原話："we do need to gather a little bit more on the CMC side"）
- 2026-08-05｜President of Lilly Cardiometabolic Health｜product：心代謝總裁：reta在膝關節炎疼痛的降幅（原話："reducing pain by unprecedented amount, 75%."）
- 2026-08-05｜CSO｜commitment：CSO表示retatrutide計畫在2027年Q1於美國送件（原話："plan to submit in the U.S. in quarter 1"）
- 2026-08-05｜CEO｜commitment：CEO重申retatrutide送件時程（原話："look forward to the submission by Q1 next year"）
- 2026-08-05｜President of Lilly International｜commitment：國際長稱Foundayo海外供應無閘控（原話："So there will be no gating of launches either"）
- 2026-08-05｜CFO｜commitment：CFO稱預期2027年全球主要市場推出Foundayo（原話："With more than 40 markets currently under regulatory review"）
- 2026-08-05｜CFO｜customer：CFO報告自費占Zepbound總處方比重（原話："accounted for approximately 45% of total Zepbound"）
- 2026-08-05｜President of Lilly USA｜customer：美國區總裁給出自費占Zepbound處方比重（原話："about 55% of overall prescriptions for Zepbound"）
- 2026-08-05｜President of Lilly USA｜customer：美國區總裁：Medicare Bridge患者約八成為注射劑型（原話："probably around 80% of people that are getting treatment"）
- 2026-08-05｜CEO｜customer：CEO說明Medicare Bridge自付額（原話："the low out-of-pocket price of $50 per month."）
- 2026-08-05｜CFO｜customer：CFO列示Zepbound直接給病患的價格區間（原話："the starting point at $299 all the way to $449."）
- 2026-08-05｜CFO｜customer：CFO報告美國incretin整體處方成長（原話："incretin analogs market grew 31%"）
- 2026-08-05｜President of Lilly Cardiometabolic Health｜customer：心代謝總裁談reta上市後病患轉向正品（原話："with their feet and embrace the newly guaranteed product"）
- 2026-08-05｜CEO｜capital_allocation：CEO報告Q2股利發放（原話："We distributed $1.5 billion in dividends"）
- 2026-08-05｜CSO｜capital_allocation：首席科學長稱將持續積極進行商業開發但維持紀律（原話："remain active in business development"）
- 2026-08-05｜President of Lilly Oncology｜capital_allocation：腫瘤總裁稱交易價格讓公司維持紀律（原話："at prices that allow us to remain"）
- 2026-08-05｜President of Lilly Oncology｜capital_allocation：腫瘤總裁拒絕對感染症與精神科後續併購前瞻（原話："I don't want to forward-look too much on that"）
- 2026-08-05｜CSO｜product：首席科學長宣布收購AtaiBeckley，進軍治療抗性憂鬱症（原話："we announced an agreement to acquire AtaiBeckley"）
- 2026-08-05｜President of Lilly Oncology｜competition：腫瘤總裁談乳癌後Verzenio時代全口服組合策略（原話："We think we have the best medicines for every single"）
- 2026-08-05｜President of Lilly Oncology｜product：腫瘤總裁稱tersolisib未來將與Inluriyo合併（原話："we envision absolutely combining with Inluriyo"）
- 2026-08-05｜President of Lilly International｜risk：國際長稱Foundayo海外早期資料雜訊多（原話："very early data, and there is a lot of noise in the data set"）
- 2026-08-05｜Analyst David Risinger｜risk：分析師指出UAE單季Foundayo銷售占美國近半（原話："the UAE were $31 million"）
- 2026-08-05｜President of Lilly International｜risk：國際長稱海外報銷需時，上市重點為慢性體重管理（原話："the focus at the time of launch will be on"）

### 問答異常語氣（迴避／改口／保留）
- LLY_Q2_2026_Earnings_Call_20260805.md｜問：Asad Haider (Goldman)：Foundayo美國上市曲線慢於預期，何時反轉；Novo口服藥在UAE三週取得50%市占｜答法：美國區總裁未回應『慢於預期』的前提，改談領先指標與七月末反轉；國際長未回應Novo 50%市占，改稱資料為sell-in且雜訊多
- LLY_Q2_2026_Earnings_Call_20260805.md｜問：Akash Tewari (Jefferies)：財測隱含下半年減速，是否保守、價格是否有未見因素｜答法：CFO未直接回答是否保守，改列一次性項目、2025下半年基期（海外Mounjaro集中上市）與季節性，稱以美元計仍會顯著成長，未給下半年數字
- LLY_Q2_2026_Earnings_Call_20260805.md｜問：Umer Raffat (Evercore)：Zepbound淨價約$580高於Wegovy約$380，醫療例外可否持續｜答法：CFO未給淨價數字，改談直接給病患價格區間、Bridge價格與處方包裝大小；承認價格將下降但稱已納入財測
- LLY_Q2_2026_Earnings_Call_20260805.md｜問：Geoff Meacham (Citi)：是否需要商業策略防範目前市場上已有的retatrutide（非正品）｜答法：心代謝總裁未談防範策略，改稱病患會轉向正品；同時Zepbound自費處方占比CFO(45%)與美國區總裁(約55%)口徑不同
- LLY_Q2_2026_Earnings_Call_20260805.md｜問：Courtney Breen (Bernstein)：retatrutide是否能被接受為BLA、里程碑為何｜答法：CEO承認法院判決為混合結果、訴訟進行中，稱仍需補CMC資料，未給具體FDA里程碑或結論，僅稱有溝通

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
{"date":"20260806","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"量的擴張持續超過淨價的下行（incretin 收入用降價換取十倍病人池）","columns":{"2Y 驗證點":"M+Z 合計季營收 YoY 續守 &gt; +40%，同期美國實現淨價跌幅不擴大","5Y 驗證點":"FY2031 incretin 收入 &gt; $75B，且合併營業利益率 &gt; 50%","10Y 驗證點":"美國肥胖治療滲透率由中個位數升至 20%+ 而毛利率仍 &gt; 80%","具體數字門檻":"Q2'26 實績：M+Z $14.87B（+73%）、美國價格 −9%（剔調整）、美國肥胖 incretin 處方 +78%","信息來源":"Lilly Q2 FY26 法說與新聞稿（2026-08-05）","漂移觸發條件":"連 2 季 TTM 偏離 ≥ 5% → 削弱；連 3 季 ≥ 10% → 反轉"}},{"id":"H2","text":"口服 Foundayo 成為第二成長曲線（小分子可規模化、拓開注射劑觸及不到的病人）","columns":{"2Y 驗證點":"Foundayo 全球季營收 2027 內站上 $500M；美國新病人啟動中口服佔比 &gt; 25%","5Y 驗證點":"口服佔 Lilly incretin 收入 &gt; 25%；40+ 國完成上市","10Y 驗證點":"口服成為初診首選，帶動開發中國家滲透","具體數字門檻":"Q2'26 實績：全球 $98M（美 $67M／UAE $31M），未達共識 ~$104M；處方醫師 8,000 → 36,000；管理層稱 7 月最後一週量較一個月前近乎翻倍、約 1/4 新啟動選口服","信息來源":"Lilly Q2 法說；GS 研究：orals 佔 2030 全球 TAM 約 40%（$46B）","漂移觸發條件":"連 4 季 TTM 偏離 ≥ 5% → 削弱（本假設已因 Q2 未達共識而處於警戒）"}},{"id":"H3","text":"2030 incretin TAM $95-200B 且 Lilly 維持約 60% 美國份額","columns":{"2Y 驗證點":"美國總處方份額續守 ≥ 55%；國際份額 ≥ 55%","5Y 驗證點":"FY2031 全球 incretin 市場 &gt; $95B，Lilly 份額 &gt; 50%","10Y 驗證點":"次世代（retatrutide／eloralintide）接棒維持份額而非僅守成","具體數字門檻":"Q2'26 實績：美國約 6/10 總處方、7/10 注射劑處方；國際 ~55%（+2pp QoQ）；GS 2030 全球 $95B（自 $130B 下修）、MS 2035 $190B","信息來源":"IQVIA（經公司投影片）；Goldman Sachs；Morgan Stanley","漂移觸發條件":"跨 2 年度持續偏離 → 削弱；跨 3 年度 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"給付端同向收縮：州級 Medicaid 給付肥胖 GLP-1 的州數 16→13（加州 2026-01-01 取消、賓州估省 $8.36 億、新罕布夏／南卡跟進；約八成成人 Medicaid 受益人無給付路徑，Stateline 2026-04-30）；雇主端 Cigna 自 2026-07-01 停止自家員工減重覆蓋，被報導為一波雇主縮減潮。與 Medicare Bridge 的擴張方向相反、且規模更難逆轉。","columns":{"對應假設":"H1／H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"州級給付州數；自付（self-pay）佔 Zepbound 處方比重（現 45% 總／55% 新）","警戒閾值":"給付州數 &lt; 10；或自付比重連 2 季上升而總處方成長同步放緩 → 減碼"}},{"id":"R2","text":"口服曲線時程後移：Foundayo Q2 全球 $98M 未達共識；Novo 口服 Wegovy 同季 ~$494M 亦未達其共識——口服類別轉換慢於雙方模型；且 GS 估 orals 佔 2030 TAM 約 40%，這是 Lilly 目前處於落後位置的一段。","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Foundayo 全球季 run-rate；美國新啟動中口服佔比","警戒閾值":"連 2 季 &lt; $300M → §6 成長評級降一級；連 4 季 → H2 反轉"}},{"id":"R3","text":"相對同業溢價收斂：FY+2 前瞻 PE 26.0x vs 大型藥廠中位 13.9x ＝溢價 87%。溢價由成長差撐住（LLY FY26 營收 +32% vs NVO −5~−13%、PFE −8%、AMGN +2~4%），一旦成長差收窄，倍數收斂的下行遠大於 EPS 下修本身。","columns":{"對應假設":"H1／H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"LLY 營收成長率 − 同業中位成長率的差距；FY+2 前瞻 PE","警戒閾值":"成長差由 &gt;25pp 收窄至 &lt;10pp → 倍數假設須重設；需 ≥ 50% 機率才觸發砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":8.5,"ev5y_pct":44.8,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A+","val":"🟢","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":3.2,"ev5y_pct":44.8,"irr_base_pct":8.5,"max_dd_pct":-52.0,"bull_5y_price":2726.0,"bear_5y_price":719.0,"p_bull_pct":28.0,"p_bear_pct":30.0,"rearm_trigger":null,"price_at_dd":1169.86,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LLY_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
