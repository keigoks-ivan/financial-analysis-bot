你是 stock-analyst **v20 判斷 agent**，標的 DXCM（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"DXCM","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DXCM_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DXCM_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1344.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000193/dxcm09302026-exhibit991.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":339.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"US$M（利益率 25.3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000193/dxcm09302026-exhibit991.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":327.2,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"US$M（利益率 24.3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000193/dxcm09302026-exhibit991.htm"}},{"id":"f_kpi5_fy2026","label":"管理層全年指引（FY2026）","value":"營收 $5.20–5.25B（+12–13%）；Non-GAAP 毛利率約 64%（維持）；Non-GAAP 營業利益率約 24%（上調）；Adj. EBITDA 利益率約 32%（上調）","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000193/dxcm09302026-exhibit991.htm；Q4 隱含營收中點成長約 10%（CFO 法說稿）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_dxcm_gross_margin_pct","label":"DXCM 毛利率","value":63.42,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DXCM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_dxcm_operating_margin_pct","label":"DXCM 營業利益率","value":23.98,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DXCM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_dxcm_fcf_margin_pct","label":"DXCM FCF 利潤率","value":33.93,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DXCM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abt_gross_margin_pct","label":"ABT 毛利率","value":56.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abt_operating_margin_pct","label":"ABT 營業利益率","value":15.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abt_fcf_margin_pct","label":"ABT FCF 利潤率","value":15.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_podd_gross_margin_pct","label":"PODD 毛利率","value":71.08,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PODD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_podd_operating_margin_pct","label":"PODD 營業利益率","value":16.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PODD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_podd_fcf_margin_pct","label":"PODD FCF 利潤率","value":8.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PODD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mdt_gross_margin_pct","label":"MDT 毛利率","value":65.01,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mdt_operating_margin_pct","label":"MDT 營業利益率","value":19.04,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mdt_fcf_margin_pct","label":"MDT FCF 利潤率","value":16.33,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_tndm_gross_margin_pct","label":"TNDM 毛利率","value":56.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TNDM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tndm_operating_margin_pct","label":"TNDM 營業利益率","value":-4.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TNDM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tndm_fcf_margin_pct","label":"TNDM FCF 利潤率","value":-5.93,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TNDM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":906.2,"period":"前三季累計至 2026-09-30，10-Q 公告；新聞稿未單列 Q3 FCF","unit":"US$M（2026 年前三季累計＝營業現金流 1,120.4 − capex 214.2）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"前三季累計至 2026-09-30，10-Q 公告；新聞稿未單列 Q3 FCF","citation":"SEC 10-Q https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000195/dxcm-20260930.htm；法說稿稱前三季 FCF >$900M"}},{"id":"f_kpi4_sbc","label":"SBC 占比","value":2.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"% 營收（$36.8M；占 GAAP 營業利益 11.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000193/dxcm09302026-exhibit991.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":82.29,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":34.13,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":47.75,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":1.88,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.66 → 2.71）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.32,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.12 → 3.13）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.67 → 3.67）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":2.71,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.13,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.67,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":32.4,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.5,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.01,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝2.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":2.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.93,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.3,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":30.37,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 2.71，分子＝快照價 82.29","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-425.0,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 1392.9、現金 1817.9（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":372.95,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":30265.13,"period":"2026-11-02","unit":"USD m","basis":"市值 30690.13 ＋ 淨負債 -425.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":5227.38,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（27 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":5772.14,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（27 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":5.79,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 82.29 / W52 72.51 / W104 75.22 / W250 92.85 / W250 13週斜率 -0.75%"},{"id":"f_ma_w52","label":"52 週均線","value":72.51,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":75.22,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":92.85,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-0.75,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 點名 Abbott、MiniMed（Guardian Connect、Simplera）、Roche 等為直接對手；Stelo 的直接對手為 Abbott；並提到主要在中國的新興競爭者。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"In selling Stelo, we compete directly with the Diabetes Care division of Abbott Laboratories. Collectively with us, these companies currently account for the majority of the worldwide sales of self-monitored glucose testing systems. We are also aware of emerging competitors primarily located in China.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K：非傳統醫材業者（大型上市公司）正開發競品，且 FDA 2026-01-06 的一般健康器材指引可能使其受惠。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"We are also aware of companies outside the traditional medical device sector that are attempting to develop competitive products and services, including for the general health and wellness, or population health space.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"CMS 將 CGM 納入 DMEPOS 競標（2027 簽約、2028-01-01 起付款變更），預期約 10 份 CGM 合約，得標價取第 75 百分位，預期降低 Medicare 給付。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"CMS anticipates that ten (10) contracts will be awarded for CGMs.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["valuation","triggers","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q1 2026 DexCom 營收年增約 15%（美國 +11%、國際 +19%），Zacks 連結到份額增加；Abbott Libre Duo 擴張為競爭風險。","source":"Zacks: DXCM stock up nearly 35% YTD","url":"https://www.zacks.com/stock/news/2973841/dxcm-stock-up-nearly-35-ytd:-will-the-uptrend-continue-in-the-rest-of-2026","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Mordor 引述：2025 CGM 營收份額 Abbott 52.83%、DexCom 33.89%、Medtronic 10.10%。","source":"Kavout: Abbott dual analyte bet","url":"https://www.kavout.com/market-lens/abbott-s-dual-analyte-bet-positions-it-to-outpace-dexcom-in-the-expanding-cgm-market","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K FY2025 風險因子：DXCM 對單一來源零件難以快速建立替代供應商（供應端風險，非客戶端導入第二供應商）；搜尋未見最大客戶（經銷商）導入第二供應商或自製的來源。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"If there are regulatory delays or impediments impacting our suppliers or us for any reason, we may not be able to quickly establish additional or replacement suppliers, particularly for our single-source components, in part because of the custom nature of various parts we design.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Reuters 經 Stockopedia：DexCom 向 FDA 提交基於 Silicon Labs 晶片的申請，分析師解讀為在 Nordic Semiconductor 之外增加第二供應商（供應端雙源）","source":"Stockopedia/Reuters: Nordic Semi falls as DexCom filing raises dual-sourcing concerns","url":"https://www.stockopedia.com/share-prices/dex-com-NSQ:DXCM/news/nordic-semi-falls-as-dexcom-filing-raises-dual-sourcing-concerns-019e73fd-cdb7-7de7-9e68-a3a3b7a6c05e/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K：三家客戶（A/B/C，皆>10%）占營收比重分別 55%/35%/46%（2024 為 40%/35%/42%，2023 為 35%/30%/37%）；占應收帳款 24%/20%/24%。營收為扣除費用、折扣、回扣後淨額，回扣付給其他實體者排除，故合計可超過 100%。","source":"SEC EDGAR 10-K FY2025 附註 Concentration of Credit Risk and Significant Customers","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"Customer A 55 % 40 % 35 % 24 % 18 % Customer B 35 % 35 % 30 % 20 % 21 % Customer C 46 % 42 % 37 % 24 % 27 % * Total revenue for each customer is net of fees, cash discounts, and rebates directly allocable to that customer. Rebates paid to other entities are excluded; therefore, the combined value may exceed 100%.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"公司稱以歷史趨勢、客戶財務狀況與外部市場因素監控客戶信用。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"We monitor the creditworthiness of our customers based on historical trends, the financial condition of our customers, and external market factors.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2026 Q2 10-Q 顯示經銷商管道為主要營收來源（Q2 經銷商約 $1,102.4M vs 直銷 $206M）","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000143/dxcm-20260630.htm","excerpt":"We sell our CGM systems direct and to distributors. We also disaggregate our revenue by our two primary geographical markets, the United States and International, based on the geographic location of delivery.","as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"DexCom Q2 2026 revenue +13% YoY to $1.31B (US +11%, intl +19%), attributed to CGM demand, new-customer starts, expanded reimbursement and share gains","source":"MarketBeat, Dexcom Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/dexcom-q2-earnings-call-highlights-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Type 1 US CGM penetration ~60-65% (mature base); Type 2 non-insulin (~25M US patients) is the growth lever, all four largest commercial PBMs now cover; Medicare coverage still pending; 2026 guidance reportedly assumes no Type 2 coverage benefit","source":"Quartr Baird 2025 summary; MarketBeat Q2 2026; MedTech Dive","url":"https://www.marketbeat.com/instant-alerts/dexcom-q2-earnings-call-highlights-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.H","triggers"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Ireland (Athenry) plant construction completed 2026-03-30; ramp-up costs weigh on margin in first three quarters of 2026 per Benchmark; G6 discontinued 1 July 2026 with volume moving to G7 15 Day; adjusted GM guided 63-64% for 2026","source":"StreetInsider, Benchmark Buy rating; industrialinfo","url":"https://www.streetinsider.com/Investing/Dexcom+gets+a+new+Buy+rating+at+Benchmark+on+expected+margin+expansion/26473962.html","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Dexcom Q1 2026 growth 15% vs Abbott CGM 7.5%; both guiding ~11-13% FY2026 growth; no 2027-2028 consensus found","source":"Kavout MarketLens","url":"https://www.kavout.com/market-lens/abbott-s-dual-analyte-bet-positions-it-to-outpace-dexcom-in-the-expanding-cgm-market","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3 列示的法律程序為證券集體訴訟等；未列反壟斷調查。FTC 在 10-K 中僅以隱私與廣告消費者保護監管角色出現。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"Between August 21 and October 9, 2024, three substantially similar putative class action complaints were filed against us and certain of our executive officers in the United States District Court for the Southern District of California.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FTC 對一般非限制類器材（含 Dexcom）的廣告有管轄權，10-K 風險因素提示行銷內容可能遭 FDA/FTC 執法；屬產業監管框架，非已發生之調查。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"The FDA and the FTC share oversight of medical device promotion. The FDA has broad authority over device marketing (including assessment and oversight of safety and effectiveness) and over FDA-approved “promotional labeling,” while the FTC has authority over “advertising” for most medical devices (i.e., non-“restricted” devices, such as ours).","as_of":"2026-02-12","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FDA 於 2025-03 對 Dexcom 發出 warning letter，指聖地牙哥與 Mesa 廠製造及品質系統不符；G6/G7 感測器未經核准變更。","source":"MassDevice: Dexcom receives FDA warning letter","url":"https://www.massdevice.com/dexcom-receives-fda-warning-letter/","excerpt":null,"as_of":"2025-03-25","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K 列示關稅與貿易政策波動（含更高進口關稅、報復性關稅）與 OFAC／BIS 出口管制為國際營運風險因子；屬一般性風險揭露，未量化","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"fluctuations in trade policy and tariff regulations, including potential higher tariffs on imported goods and materials and renegotiation of free trade agreements and potential retaliatory tariffs imposed by foreign countries against U.S. goods","as_of":"2026-02-12","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026 年搜尋未見 DexCom 專屬的關稅或出口管制量化影響；2026 Q3 non-GAAP 毛利率 65.1%（去年同期 61.3%），全年指引約 64%","source":"DexCom 8-K Q3 2026 earnings release Exhibit 99.1","url":"https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000193/dxcm09302026-exhibit991.htm","excerpt":"Non-GAAP gross profit* totaled $875.3 million or 65.1% of reported revenue for the third quarter of 2026","as_of":"2026-10-30","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2023 10-K：DexCom 依賴單一或唯一來源供應商，例如發射器內的 ASIC 與生物介面膜用的特定聚合物","source":"DexCom Form 10-K FY2023 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355724000021/dxcm-20231231.htm","excerpt":"However, we also rely on single and/or sole sources for certain components and materials used in manufacturing, such as for the application-specific integrated circuit that is incorporated into the transmitter and certain polymers used to synthesize the polymeric biointerface membranes for our products.","as_of":"2024-02-15","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"風險摘要站稱 DexCom 製造集中於亞利桑那州梅薩與馬來西亞，聖地牙哥有限，替代產能難以快速建立（二手摘要，非 SEC 原文）","source":"policyrisk.com DXCM","url":"https://policyrisk.com/world/company/DXCM","excerpt":"Most manufacturing is concentrated in Mesa, Arizona and Malaysia (limited in San Diego), with replacement capacity hard to stand up quickly.","as_of":"2026-01-01","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"2025 Q1 電話會議 CFO 稱因多數產品在美國製造，關稅直接衝擊較小、預期無重大影響","source":"MDDI: Did Dexcom Return to Form with its 1Q25 Earnings?","url":"https://www.mddionline.com/diabetes/did-dexcom-return-to-form-with-its-1q25-earnings-","excerpt":null,"as_of":"2025-05-01","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"DXCM 2026 Q3 營收約 $1.344B，年增 11%；美國年增 14% 至約 $970M，國際年增 5% 至約 $375M；管理層稱國際受各國給付週期影響，預期明年初回到較高有機成長；全年財測上調，Q4 財測中點年增約 10%。","source":"SEC 8-K Exhibit 99.1 / securities.io / Drug Delivery Business（Q3 2026 結果）","url":"https://www.securities.io/dexcom-raises-2026-outlook-as-q3-revenue-grows-11-to-1-344-billion/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"美國 CGM 市佔 2025 年 GlobalData 模型：Abbott 48.5%、Dexcom 44.7%；歐洲/亞太/中東非洲 Dexcom 市佔遠低於 Abbott。Barclays 以 Abbott Libre 市佔壓力為由給 Underweight、目標價 $71。","source":"Kavout / Munich-startup insights（二手彙整）","url":"https://www.kavout.com/market-lens/abbott-s-dual-analyte-bet-positions-it-to-outpace-dexcom-in-the-expanding-cgm-market","excerpt":"Dexcom held a CGM market share of 44.7% in the US in 2025, second only to Abbott with a 48.5% share.","as_of":"2026-06-01","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Mordor Intelligence 指 Stelo 以 USD 89-99 上市及 Abbott 類似 OTC 策略，預期未來兩年感測器價格趨向 USD 60 以下（預測非現行價目）。","source":"Mordor Intelligence US CGM Market","url":"https://www.mordorintelligence.com/industry-reports/us-continuous-glucose-monitoring-market","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Dexcom 2026 年 9 月 Wells Fargo 會議摘要：兩項 CMS 申請審查中（全部第二型、使用降血糖藥者），CMS 決定預期 2027 年中；若通過可能使成長加速超過目前 10%+。","source":"Quartr Dexcom Wells Fargo 21st Healthcare Conference summary","url":"https://quartr.com/events/dexcom-inc-dxcm-wells-fargo-21st-annual-healthcare-conference_3PQtY9no","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261102","affects":["thesis.H","triggers"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"William Blair（2025-10）：即使採 T2 basal 採用曲線 75% 且使用率較低，2030 年仍為 $4B 市場；調查受訪者預期 T2 非胰島素 CGM 使用滲透率三年內由 25-30% 升至約 50%。","source":"William Blair Medical Technology CGM deep dive","url":"https://www.williamblair.com/-/media/downloads/eqr/2026/williamblair_medical-technology-cgm-deep-dive.pdf","excerpt":null,"as_of":"2025-10-01","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：競爭對手快速採用 AI 可能加速創新週期並加劇競爭壓力（未點名具體替代技術）","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"while competitor use of AI may accelerate innovation cycles and intensify competitive pressures.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"搜尋未找到足以取代 CGM 的非 CGM 替代技術（如非侵入式血糖）之報導；2026 來源描述的是 CGM 內部競爭（Abbott、Medtronic/MiniMed、Senseonics 365 天植入式 Eversense），消費科技業者（如 Apple）進入被列為長期變數但有法規門檻","source":"WebSearch 彙總（Zacks/MDDI 等 2026 報導）","url":null,"excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Abbott 推出 Libre Duo（葡萄糖＋酮體連續監測）；DexCom G7 15 Day 於 2026-07 獲加拿大衛生部授權","source":"Knowledge Sourcing CGM market press release","url":"https://www.knowledge-sourcing.com/resources/press-releases/continuous-glucose-monitoring-cgm-market","excerpt":"CGM functionality, Libre Duo broadens the role of wearable biosensors in diabetes management. The product could also influence competition as manufacturers explore multi-biomarker sensing, connected insulin delivery, and integrated digital health platforms. Recent Developments in the Continuous Glucose Monitoring Market July 2026: Dexcom received Health Canada authorization for G7 15","as_of":"2026-09-17","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Analysts 指出 Abbott 雙分析物（葡萄糖＋酮體）策略可能在 CGM 市場領先 DexCom","source":"Kavout market lens","url":"https://www.kavout.com/market-lens/abbott-s-dual-analyte-bet-positions-it-to-outpace-dexcom-in-the-expanding-cgm-market","excerpt":"Abbott's Dual-Analyte Bet Positions It to Outpace Dexcom in the Expanding CGM Market 4 months ago SHARE THIS ON: Save Exclusive Content for Pro Members","as_of":"2026-08-01","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K describes通路為北美及部分國際市場直銷團隊，輔以北美與數個國際市場的經銷安排；未描述結構性通路轉換。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"To complement our direct sales efforts, we have entered into distribution arrangements in North America and several international markets that allow distributors to sell our products.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"Q4 2025 財報電話會議摘要：管理層預期 Q1 2026 營收季減約 6-7%，部分歸因於逐步轉向藥局通路。","source":"MarketBeat, DexCom Q4 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/dexcom-q4-earnings-call-highlights-2026-02-12/?.tsrc=rss","excerpt":null,"as_of":"2026-02-12","retrieved_at":"20261102","affects":["valuation","moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 2026 call：Stelo 為針對非胰島素第 2 型糖尿病的 app 與平台；G7 15-Day 預計年底轉換約 50% 美國客戶。","source":"Webull, DexCom Q2 2026 Earnings Call Transcript","url":"https://www.webull.com/news/15319340244476928","excerpt":"DexCom Flex Launch -- introduced in Germany as a 15-day sensor targeting the type 2 basal and non-insulin markets. G8 System Development -- targeted for late 2027 or early 2028, featuring a multi-analyte platform and a footprint half the size of the G7.","as_of":"2026-07-30","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 release (2026-10-29) 全年指引：營收 $5.20–5.25B（約 +12–13%），non-GAAP 營業利益率約 24%、adj. EBITDA 率約 32%、毛利率約 64%；營收與兩項利潤率上調，毛利率維持。","source":"DexCom 8-K Exhibit 99.1 (Q3 2026 results)","url":"https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000193/dxcm09302026-exhibit991.htm","excerpt":"Revenue of $5.20 - $5.25 billion (approximately 12-13% growth)","as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026（07-30）指引：營收 $5.18–5.25B（前次 $5.16–5.25B），Benzinga 稱 2022-10 至 2026-07 共 29 次指引更新，上調 7 次、下調 4 次。","source":"Benzinga / search summary (DexCom guidance)","url":"https://www.benzinga.com/quote/DXCM/earnings-forecasts","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價分布（2026-07 擷取）：平均 $86.16、中位 $85、區間 $65–$112，25 位分析師；Tickflow 2026-08-01 平均 $83.80、33 位。Q3 後的目標價未查到。","source":"Walnut Invest DXCM forecast; Tickflow","url":"https://walnutinvest.com/stocks/dxcm/forecast","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"個別目標價：Truist $87（自 $80，2026-07-16）、Mizuho $90（自 $85，07-15）、Deutsche Bank 初評 Buy $86（06-23）；Barclays 2026-01 降評 Underweight 目標 $71。","source":"Search summary (price target tracker; Investing.com)","url":"https://kr.benzinga.com/quote/DXCM/price-targets","excerpt":null,"as_of":"2026-07-16","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 實際 EPS $0.70 對共識 $0.61；營收 $1.31B 對 $1.29B；FY2026 調整後 EPS 共識約 $2.64（Q2 前）。","source":"Benzinga earnings forecasts; Barchart","url":"https://www.benzinga.com/quote/DXCM/earnings-forecasts","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"證券集體訴訟（In re Dexcom Securities Litigation）持續中：2026-01-07 法院准許被告判決於訴狀（附修正許可），2026-02-06 原告提第二次修正訴狀","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"On January 7, 2026, the court granted defendants’ motion for judgment on the pleadings with leave to amend. On February 6, 2026, lead plaintiff filed a second amended consolidated complaint.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"G6/G7 使用者集體訴訟：2025-09-29 至 2026-01-08 共六件重疊的集體訴訟起訴","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"Between September 29, 2025, and January 8, 2026, various plaintiffs, purported users of G6 or G7 devices, filed six overlapping putative class action complaints against us.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"董事會 2026-10-29 授權最高 US$10 億庫藏股計畫，期限至 2027-12-31；2026-05-14 亦曾授權 US$10 億計畫並終止舊計畫","source":"SEC EDGAR 8-K 2026-10-29 Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000193/dxcm-20261029.htm","excerpt":"On October 29, 2026, Dexcom announced that its Board of Directors authorized and approved a share repurchase program of up to $1.0 billion of Dexcom’s outstanding common stock","as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06-04 簽約收購 Nutrisense（價格未揭露），管理層稱非 CGM 營收每年僅數百萬美元以下","source":"搜尋摘要彙整（drugdeliverybusiness/massdevice/gurufocus Q2 2026 call）","url":null,"excerpt":null,"as_of":"2026-06-04","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"+","claim":"FDA 清除 Stelo 非處方 CGM 用於兒童（約 2026-06-30 報導）；CONNECT 隨機對照試驗結果於 2026 Q2 公布（第 2 型非胰島素族群）","source":"MDDI：Analysts Love Dexcom's Q2 Results, But Competition Is Heating Up（搜尋摘要）","url":"https://www.mddionline.com/diabetes/analysts-love-dexcom-s-q2-results-but-competition-is-heating-up","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-06-04 簽約收購 Nutrisense（價格未揭露、營收貢獻小）；未見大型併購，Insulet 傳聞 Dexcom 稱無 active discussions（日期未確認）","source":"搜尋摘要彙整（drugdeliverybusiness、massdevice、gurufocus）","url":null,"excerpt":null,"as_of":"2026-06-04","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"證券集體訴訟持續，2026-02-06 提第二次修正訴狀","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"On January 7, 2026, the court granted defendants’ motion for judgment on the pleadings with leave to amend. On February 6, 2026, lead plaintiff filed a second amended consolidated complaint.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"衍生訴訟（聯邦＋2025-09-25 Delaware Chancery）均暫停待證券訴訟駁回動議","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"On September 25, 2025, an additional derivative lawsuit was filed against us and certain of our current and former executive officers and directors in the Court of Chancery of the State of Delaware.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#2","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"G6/G7 使用者六件重疊集體訴訟","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm","excerpt":"Between September 29, 2025, and January 8, 2026, various plaintiffs, purported users of G6 or G7 devices, filed six overlapping putative class action complaints against us.","as_of":"2026-02-12","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"+","claim":"FDA 清除 Stelo OTC CGM 兒童適用（約 2026-06-30）；CONNECT RCT 結果 2026 Q2 公布；G7 510(k) K253737 於 2026-02-03 取得；入選 FDA TEMPO 試點（2026-07）","source":"搜尋摘要彙整（MDDI 等）","url":"https://www.mddionline.com/diabetes/analysts-love-dexcom-s-q2-results-but-competition-is-heating-up","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"DXCM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":63.42,"operating_margin_pct":23.98,"fcf_margin_pct":33.93,"rd_intensity_pct":11.91},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DXCM","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"ABT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.63,"operating_margin_pct":15.9,"fcf_margin_pct":15.66,"rd_intensity_pct":6.64},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABT","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"PODD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.08,"operating_margin_pct":16.9,"fcf_margin_pct":8.7,"rd_intensity_pct":11.33},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PODD","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MDT","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":65.01,"operating_margin_pct":19.04,"fcf_margin_pct":16.33,"rd_intensity_pct":7.77},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"TNDM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.01,"operating_margin_pct":-4.4,"fcf_margin_pct":-5.93,"rd_intensity_pct":18.03},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TNDM","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"DXCM"},"financial_history":{"ticker":"DXCM","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":2909800000.0,"revenue_yoy_pct":null,"gross_margin_pct":64.72,"operating_margin_pct":13.44,"net_income":341200000.0,"diluted_eps":0.82,"free_cash_flow":304700000.0,"fcf_margin_pct":10.47,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":3622300000.0,"revenue_yoy_pct":24.49,"gross_margin_pct":63.19,"operating_margin_pct":16.5,"net_income":541500000.0,"diluted_eps":1.3,"free_cash_flow":511900000.0,"fcf_margin_pct":14.13,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":4033000000.0,"revenue_yoy_pct":11.34,"gross_margin_pct":60.46,"operating_margin_pct":14.88,"net_income":576200000.0,"diluted_eps":1.42,"free_cash_flow":630700000.0,"fcf_margin_pct":15.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":4662000000.0,"revenue_yoy_pct":15.6,"gross_margin_pct":60.1,"operating_margin_pct":19.56,"net_income":836300000.0,"diluted_eps":2.09,"free_cash_flow":1077200000.0,"fcf_margin_pct":23.11,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/DXCM/DXCM_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**DexCom, Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Ladies and gentlemen, thank you for standing by. Welcome to the Dexcom Third Quarter 2026 Earnings Release Conference Call. My name is Abby, and I will be your operator for today's call. [Operator Instructions] As a reminder, the conference is being recorded.
I will now turn the call over to Sean Christensen, Senior Vice President of Finance and Investor Relations. Sean, you may begin.

**Sean Christensen** (Executives):
Thank you, operator, and welcome to Dexcom's Third Quarter 2026 Earnings Call. Our agenda begins with Jake Leach, Dexcom's President and CEO, who will summarize our recent highlights and ongoing strategic initiatives, followed by a financial review and outlook from Jereme Sylvain, our Chief Operating Officer and Chief Financial Officer.
Following our prepared remarks, we will open the call up for your questions. At that time, we ask analysts to limit themselves to one question each so we can provide an opportunity for everyone participating today. Please note that there are also slides available related to our third quarter 2026 performance on the Dexcom Investor Relations website on the Events and Presentations page.
With that, let's review our safe harbor statement. Some statements on today's call may constitute forward-looking statements. These statements reflect management's intentions, beliefs and expectations about future events, strategies, competition, products, operating plans and performance. These statements are made as of the date hereof based on information currently available to DexCom, are subject to various risks and uncertainties that could cause actual results to differ materially. For a discussion of these risks, please see Dexcom's annual report on Form 10-K, most recent quarterly report on Form 10-Q and other filings with the Securities and Exchange Commission. Except as required by law, we assume no obligation to update any forward-looking statement or to conform any forward-looking statements to actual results.
Additionally, during the call, we will discuss certain non-GAAP financial measures. Unless otherwise noted, all financial measures discussed on this call are presented on a non-GAAP basis. Non-GAAP measures should not be considered in isolation or as a substitute for or superior to GAAP results. Please refer to the tables in our earnings release and the slides accompanying our third quarter 2026 earnings call for reconciliations to the most directly comparable GAAP measure.
Now I will turn it over to Jake.

**Jacob Leach** (Executives):
Thank you, Sean, and thank you, everyone, for joining us. Today, we reported third quarter revenue growth of 11% compared to the third quarter of 2025 on both a reported and organic basis. Underlying our third quarter results are 4 key areas that advance our long-term vision we provided earlier this year. First, we continue to see strong momentum across the CGM category driving our stable low double-digit revenue growth with active base growth above those levels. We once again gained share in the quarter, supported by prescriber and customer preference for Dexcom CGM, positioning us well as we prepare for significant access expansion. Second, our clinical evidence continues to strengthen the case for broader access to CGM. Third, our product portfolio continues to advance, helping us deliver a more personalized and valuable experience for each customer. And fourth, our operational execution has given us upward momentum throughout the year, strengthening our scale and financial position while also driving strong product performance in the field. In the U.S., we again delivered strong revenue growth of 14% and captured share across the market. This extended a multi-quarter trend of share gains in the U.S. with our largest increase coming from customers with type 2 diabetes, including those not on insulin. We continue to see greater physician awareness of the role Dexcom CGM can play across the spectrum of diabetes. This is contributing to growth today and preparing the market for a significantly broader coverage environment in the future. Along those lines, we continue to expect CMS to announce a type 2 non-insulin coverage decision this year as the case for reimbursement is strengthening. Much of this confidence is driven by CONNECT, our Type 2 randomized controlled trial, which is now widely recognized as the landmark CGM study for this population.
As a reminder, we announced the results of CONNECT this summer at the 2026 ADA scientific sessions and could not have been happier with the results. Over a 6-month study period, we saw a 1.6% A1c improvement for the Dexcom CGM Group, which equated to a 0.9% difference in A1c between the CGM arm and the control group. These are the strongest A1c results we have generated across our historic randomized controlled trials, which have helped shape standards of care and establish broad reimbursement. We now expect CONNECT to do the same thing for the type 2 non-insulin population.
Earlier this month, CONNECT was published in the New England Journal of Medicine. This provides an important level of independent validation and gives the study a prominent platform among clinicians, advocacy organizations and reimbursement bodies around the world. This marks the first time in nearly 2 decades that the New England Journal of Medicine published clinical data on the stand-alone use of CGM. While we believe our results speak for themselves, this publication reinforces both the quality of the data and its potential to reshape clinical practice.
As a next step towards broader coverage, we provided this publication update directly to the medical directors evaluating the submission for Medicare coverage expansion. We also look forward to seeing this evidence included in upcoming clinical standards, including the ADA standards of care, which is expected to be updated in the coming weeks. CONNECT further strengthened the growing body of evidence supporting the broader benefit of CGM across metabolic health. This includes significant improvements across multiple studies in 10-year cardiovascular disease risk, blood pressure, cholesterol, triglycerides and kidney disease progression. Our expanding clinical evidence is supported by a product portfolio designed around the distinct needs of each customer.
During the third quarter, we launched a fully redesigned Stelo app. The new Stelo app experience is more intuitive and personalized with enhanced glucose insights, simplified meal logging and more detailed nutritional information. This is especially important because many Stelo customers are engaging with their glucose data for the first time, helping them understand how food and lifestyle choices affect their glucose can make the information more useful and actionable. Just as importantly, the redesigned app establishes a new software foundation from which our broader product experience can evolve. Stelo gives us a platform to introduce new capabilities, learn from customer engagement and ultimately bring the most valuable innovations across our broader product portfolio. This supports the goal we outlined at Investor Day to deliver greater personalization and engagement across every stage of the customer journey. During the quarter, we also continued to advance the rollout of our G7 15 Day system with broad pump connectivity available as of this summer; customer adoption steadily built throughout the quarter. This leaves us on track to convert nearly 50% of our U.S. customer base to G7 15 Day by year-end. Importantly, feedback from physicians and customers continues to be positive, particularly around the extended wear time, sensor performance and updated patch design. In fact, as the updated adhesive is rolling out into the field, we've already seen a 4- to 5-point improvement in 15 Day survivability. We are now preparing to bring these benefits to customers outside the United States.
Earlier this year, Health Canada became the first international regulator to clear G7 15 Day. Beginning in November, we will officially launch this product in Canada, marking the first of several planned international introductions in the coming quarters. We also received clearance in the third quarter in Japan, positioning us for a launch in that market in early 2027. I'm encouraged by the level of execution we've delivered in 2026, including the third quarter. During the quarter, we delivered further manufacturing efficiencies, improved freight costs and saw strong product performance in the field. We also reached an important milestone at our Ireland facility, which recently initiated commercial production on schedule. Ireland expands our manufacturing capacity and strengthens the resilience of our global supply network. With large-scale manufacturing plants now in the U.S., Europe and Asia Pacific, we have the capacity to support our ambitious growth plans ahead. We are also expanding our digital customer support ecosystem into select international markets, including My Dexcom Account. Building on the strong adoption we've seen in the U.S., these tools help simplify the support experience, improve efficiency and save time for our customers. This is another example of our commitment to setting the standard for customer experience. This continued progress reflects our team's focus and discipline throughout the year. Across the business, we have advanced several important strategic initiatives while continuing to deliver strong growth, margin and cash flow generation. As we look toward Dexcom's next chapter, it is critical that we have the right leadership and operating structure to scale with that same discipline. In line with that goal, we recently promoted Jereme Sylvain to Chief Operating Officer in addition to his responsibilities as Chief Financial Officer. Jereme is an exceptional leader and trusted partner with a deep understanding of every part of our business. Expanding his role to include operations, quality and customer success brings these functions even closer to our financial and strategic priorities as we work to reach millions more people around the world.
With that, I will turn it over to Jereme.

**Jereme Sylvain** (Executives):
Thank you, Jake. As a reminder, unless otherwise noted, the financial metrics presented today will be discussed on a non-GAAP basis. Reconciliations to GAAP can be found in today's earnings release as well as the slide deck on our IR website.
For the third quarter of 2026, we reported worldwide revenue of $1.34 billion compared to $1.21 billion for the third quarter of 2025, representing growth of 11% on both a reported basis and organic basis. As a reminder, our definition of organic revenue excludes the impact of foreign exchange in addition to non-CGM revenue acquired or divested in the trailing-12 months.
U.S. revenue totaled $970 million for the third quarter compared to $852 million in the third quarter of 2025, representing an increase of 14%. As Jake mentioned, we again took share in the U.S. market with strong performance across all customer segments. This helped drive a nice acceleration in our U.S. growth rate compared to the first half of the year. Global new patient starts were near record levels in Q3, consistent with our expectation as seasonality continues to evolve in the business. Relative to the prior year, new customer starts were up in the third quarter with these efforts amplified by our focused efforts on retention and utilization to maximize our growth algorithm.
International revenue grew 5% on -- both on a reported and organic basis. totaling $375 million in the third quarter. As we've discussed in previous quarters, the second half of 2025 saw multiple reimbursement wins that we are lapping as we move through the third and fourth quarters of 2026. We've seen a similar dynamic in prior years as the timing of these reimbursement decisions can create some quarterly variability in international growth rates. As usual, we expect this to be a short-term dynamic with international revenue normalizing back to higher organic growth levels at the start of next year. We are very excited about the business based on the number of drivers on the horizon, including new access wins, the rollout of G7 15 Day, Dexcom ONE+ 15 Day, Stelo, a full year of Dexcom Flex and continued go-direct opportunities. We have not seen significant changes to our pricing environment, and we are executing the access expansion and go-to-market strategy that we discussed at Investor Day.
Our third quarter gross profit was $875.3 million or 65.1% of revenue compared to 61.3% of revenue in the third quarter of 2025. We delivered another quarter of strong gross margin performance, with margins up approximately 380 basis points compared to last year. This reflected continued manufacturing efficiencies, further progress in freight and quality management and a benefit from the continued ramp-up of G7 15 Day in the U.S. market.
Operating expenses were $535.8 million for Q3 of 2026, compared to $468.4 million in Q3 of 2025. Operating income was $339.5 million or 25.3% of revenue in the third quarter of 2026, compared to $272.9 million or 22.6% of revenue in the same quarter of 2025. We again delivered solid operating margin expansion during the quarter despite increased investment in Ireland as we prepare that facility for commercial production. Excluding the Ireland facility, we would have again delivered OpEx leverage in the quarter.
Adjusted EBITDA was $435.2 million or 32.4% of revenue for the third quarter compared to $368.4 million or 30.5% of revenue for the third quarter of 2025. Net income for the third quarter was $275 million or $0.73 per share.
We remain in a great financial position, closing the quarter with approximately $1.8 billion of cash and cash equivalents. Our cash flow generation continues to stand out as we have now generated over $900 million of free cash flow through the first 3 quarters of the year. This enabled us to already execute our Investor Day goal of repurchasing $1 billion of stock in 2026. Having completed that, we are announcing another $1 billion share repurchase authorization in line with our commitment to deploy at least 50% of free cash flow generated over the course of 2027.
During Investor Day, we also spoke to our broader framework for assessing tuck-in M&A. Historically, acquiring international distributors has been 1 of our highest value uses of capital and a key part of our strategy to transition to direct operations in select markets. Today, we are announcing another international distribution deal. We recently signed a deal to acquire a business from a partner that allows us to go direct across high potential markets in Europe. As we shared at Investor Day, these decisions to go direct to help ensure that we have control and alignment as we significantly expand access to CGM in key markets.
Turning to guidance. We are updating our revenue guidance to be in the range of $5.20 billion to $5.25 billion, representing growth of 12% to 13% for the year. At the midpoint, our updated outlook passes through the third quarter revenue outperformance, partially offset by approximately $5 million of incremental foreign exchange headwinds since last quarter. This also implies midpoint fourth quarter growth of 10%. For margins, we are maintaining our full year non-GAAP gross profit margin guidance at approximately 64%. We are increasing our non-GAAP operating profit margin guidance to approximately 24% and adjusted EBITDA margin guidance to approximately 32%.
With that, we can open up the call for Q&A. Sean?

**Sean Christensen** (Executives):
Thank you, Jereme. As a reminder, we ask our audience to limit themselves to only one question at this time and then reenter the queue if necessary. Operator, please provide the Q&A instructions.

**Operator** (Operator):
[Operator Instructions] And our first question comes from the line of Matt Taylor with Jefferies.

**Matthew Taylor** (Analysts):
Congrats on the nice results. I thought maybe I'd start high level, and I wanted you to address the debate around category growth. We saw your competitor call out some pricing headwinds that you just said in the prepared remarks, you're not really seeing that. So maybe you could comment on that specifically and what you think about overall category growth today before we're getting this CMS announcement.

**Jacob Leach** (Executives):
Yes. Thanks, Matt, for the question. And I really appreciate the opportunity to be able to give you guys our perspective on this because there has been, as you mentioned, some recent noise out there about the category. I think if you look at the way that this year has played out, from our perspective, nothing has changed in our view of the opportunity in front of us. We put out our LRP at our Investor Day this summer, and we are still extremely confident in that plan that we put forward. As you look at the way we guided for this year, we looked at the current coverage environment, and we specifically mentioned that we didn't anticipate any expansions in coverage this year, at least that's how we based our plan. And we basically guided to a range of new customer starts with the bottom of our growth range and that's strong customer starts, but not record. And then the top end of our guide was -- would reflect a record year of new patient starts. As you've seen, we've continually raised our guidance, and we're now guiding to the upper range of our original guidance we issued in January. And that's because we're tracking to a record new patient year. And so as you look at that against the backdrop of current coverage, we feel very confident in our ability to grow in this environment. Our active base growth is in the upper teens, and you can see the revenue growth. And so we're confident in our ability to grow in this category.

**Jereme Sylvain** (Executives):
Yes, to your question, Matt, on pricing, I think you asked a question on pricing and can you talk to that? I think it's pretty clear. We haven't seen a degradation of pricing around the world. Certainly, as we move outside the U.S. into markets that are new for us, we have a product portfolio that we go in. I think we've matched the product portfolio to the reimbursement. And I think you've seen that be relatively stable. And so I think we haven't seen some of the references that June referenced with some pricing concerns. Certainly not in the markets we've entered into, in the markets we've been in. And I think you'll see that ultimately reflected in our gross margins as our gross margins are the highest they've been since Q4 of 2022.

**Operator** (Operator):
Our next question comes from the line of Robbie Marcus with JPMorgan.

**Robert Marcus** (Analysts):
One, I wanted to talk or ask about competition outside the U.S. Your competitors spoke to seeing pretty sharp pricing, mostly in cash pay. I know, you and them overlap, but not exactly some markets that are more exposed to than you. So what are you seeing outside the U.S.? How do you feel about volume growth right now? And anything new on the competitive front? Appreciate it.

**Jereme Sylvain** (Executives):
Yes, certainly, I can take that. Certainly, as we think about markets outside the U.S. and monitoring pricing, it's been stable. And what I mean when we look at -- certainly, when it comes to reimbursement, and we'll start with reimbursement because typically, that's how we've approached markets to begin with. We've seen the reimbursement is stable and it's usually tiered based on the acuity of the condition. And so we've seen that play out. It's why we have a product portfolio to match it and to match what the need ultimately is. And again, it's been stable. We don't exactly overlap in all fairness to your point, there's a lot of markets, I would say that maybe we don't overlap in where a competitor might be and we may not. And so ultimately, if there's a degradation in the existing business for that particular incumbent, there could be some impact there. For example, if you were the only CGM offering in a country and someone came in there is a risk that the incumbent may have been overpriced into that window, and naturally, with natural pressure, you come back to more market conditions. But what I would say is as we look at our portfolio and our offerings across the world, and the market conditions that exist there from all competitors in that market, I think we're priced right. And so we haven't necessarily seen that degradation at least in our book of business. And competition, I think we compete well in those markets. Clearly, the tiered portfolio was done to compete with the right patient with the right product. And when we get into these markets and we compete with that right product in that market, you can see we're taking share in those markets.

**Operator** (Operator):
And our next question comes from the line of Travis Steed with Bank of America.

**Travis Steed** (Analysts):
This is Travis, sorry. I guess I wanted to ask about there was a CVS contract lost recently. I know you don't talk about payers too much, but maybe if you just talk about the potential when you do have contract losses that you're able to offset with revenue per patient and how you think about your ability to still be confident in 10%-plus revenue growth in '27?

**Jacob Leach** (Executives):
Travis, thank you. Yes. I think what I'll start is just talk a little bit about the landscape, particularly in the U.S., as you mentioned, payers and PBMs. And then I'll cover that. I'll cover kind of how we view it, how we think things are moving forward, and then we'll also cover what we think the impact looks like for next year. So if you look at the general access landscape in the United States, you've got -- for CGM, you got formulary access through the pharmacy and then you've also got medical benefit access. And so specifically on the formulary side, there's a lot of custom formularies. The specific contract you're talking about is a very -- it's a particular portion of a particular PBM access. And so when we look at PBM formularies across the United States, we're generally in an equal access position, co-preferred with competitors. There are some where we're advantaged and there are some where our competitors are advantaged. But one thing I want to be clear on is as we negotiate these contracts, we are always negotiating for equal access. We feel that, that is the right thing for patients. It's the right thing for prescribers. Ultimately, I think it's the right thing for employers and the plans that service them. And we think we're very confident in our position to be able to compete in that type of a scenario. And so we're always pushing for equal access. And I think when these types of decisions are made, one of the things that I think is important to consider is sometimes it may be suggested that the products are comparable. But I'll give you an example. Imagine there's a child out there with type 1 diabetes who has been using Dexcom for 4, 5 years, powering an AID system, getting fantastic results driven by the accuracy of our sensor, their ability to calibrate that sensor when they want to. And then the parent's ability to see their data through the Share/Follow system anytime they want. Now if you see -- if that individual try to switch to a competitor, it is not compatible with their insulin pump. There's multiple pumps out there that competitors are not compatible with here in the United States. They also lose the ability to use the Share/Follow system in collaboration. So I think trying to consider that as a comparable product is not even in the realm of reality. The other example I give is if you have a prescriber who's prescribing Dexcom G7 to a basal insulin user because of the smart basal feature and the ability to hit those outcomes that both the patients and the prescribers want, that's not a feature that's offered by our competitor. So I think in the realm of maybe for certain patients, those products are considered comparable, but for the vast majority, they are not. And so the good news, though, is that for patients who have potentially lost coverage through a formulary, through a pharmacy, most of them still have access through a medical benefit, and so they can still access the product through a DME. And actually, one thing I wanted to mention is that we have a plan to launch a new system called Dexcom Direct. It is a service for patients that we've been building actually with the anticipation of the expansion into Medicare. So our plan was as Medicare coverage expanded. We wanted to be able to help those folks navigate their coverage, whether it's through a Medicare Advantage plan or through a medical benefit for fee-for-service, durable medical equipment benefit. And so that system was being developed very similar to some of the other direct services that you see out there in the marketplace. And it's all about helping our patients get access to our technology. Again, we're originally planning to launch that in front of the Medicare expansion. But with that capability launching early next year, it is a perfect place where patients -- anyone, not just this example, but anyone who's having a challenge getting access to our technology can go the Dexcom Direct and we'll walk them through every step of the way to ensure that they get access to the technology they need.
Jereme, do you want to talk a little bit about how we see it moving forward?

**Jereme Sylvain** (Executives):
Yes. So I -- and thanks for the question, Travis. Maybe I'll give you guys some context to at least how we see it in the context of next year. And while we're not going to give guidance next year, I do think it helps give you confidence around LRP starting point for next year. So the PBM we're talking about represents less than 4% of our U.S. revenue results. So relatively small in the context of our overall company. And typically, when you think about an arrangement where you have exclusivity or preferred 1 of 1, even though it says 1 of 1, you typically don't get all of it. You might get 2/3 of customers and 1/3 go through various pathways, whether it's off-formulary other opportunities. Obviously, when you have that preferred status, there's differences in price tiers that you could probably imagine. And that's the way you typically negotiate these things. If you move off of preferred into the secondary, it typically comes with a pretty significant price increase. And so the expectation is while we navigate through this from a financial perspective, we'll talk about the patient perspective here in a second. The expectation is that it doesn't necessarily have that much of an impact on our next year results from a financial perspective. because we do expect to -- even though there might be a flip in terms of patients, the reality is, as we expect, obviously, the remuneration to change as a result of that. That's the financial piece of it. I think it's important to understand, it's important context to size it. The underlying reality though, and Jake alluded to it is we don't like being in these situations for our patients. And so that's one of the things, the reason why Jake alluded to Dexcom Direct and working really hard to make sure there's a limited patient disruption because at the end of the day, what we want to do is come back to our mission, which is empower people to control of their health. It means having access to product, making sure we don't disrupt their daily life. So we're going to work hard to make sure we keep every single patient, undisrupted as much as possible through this process, I mean, against the backdrop, but we don't expect to have much of a significant impact on our next year financial results.

**Operator** (Operator):
And our next question comes from the line of Larry Biegelsen with Wells Fargo.

**Lei Huang** (Analysts):
It's Lei calling in for Larry. You mentioned some impact from the from the PBM change being modest. Can you talk about any other top line, bottom line puts and takes for '27? The consensus revenue number out there is roughly 11% growth, that's near the floor that you laid out. How should we think about U.S. OUS growth just given kind of the coverage expectations?

**Jereme Sylvain** (Executives):
Yes. So the -- we'll go back to kind of what we talked about at Investor Day in terms of how to think about it. We'll give guidance at the right time. But -- in terms of how we've talked about exiting 2026, obviously, we've made some really nice progress over the course of the year on gross margin. We're going to turn on Ireland here in the fourth quarter. So I'd expect there to be a little bit of an impact of Ireland ramping up into the first part of next year. But at the end of the day, underneath it all, you're still going to see more and more progression of a move to 15 Day product here, certainly in the U.S. talked about launching it in Canada. And we have a couple of other markets that are going to be launching here 15 Day relatively soon. So you should start to see some of those tailwinds starting to play through next year. And then obviously, we won't have the start-up costs associated with Ireland. So those are some pretty some interesting puts and takes as we move into next year. We'll go ahead and give the guide for next year officially as we get to that point. But I think hopefully, that gives you some puts and takes, at least to think about it that we've historically talked about. And then, of course, we'll give you more as the right time comes.

**Operator** (Operator):
And our next question comes from the line of Jeff Johnson with Baird.

**Jeffrey Johnson** (Analysts):
Maybe if I could just ask a follow-up question on the CVS question that was already asked. But Jereme, as you explained some of those patients who might no longer have preferred access might be willing to pay the higher price to come off that preferred. Typically, what would that price increase look like? If I'm a patient who no longer has preferred access, what would I be paying per month as an increase to stay on Dexcom, number one? And number two, I know you're working with a group to try to move some of these patients, as you talked about from pharmacy to medical. Can you just help us understand the mechanics of that? If I'm a Dexcom G7 wearer, can I just call that group that you're working with and say, "Hey, move me to my medical, do I even know as a patient what that means? And typically, what is my DME co-pay relative to my pharmacy co-pay?

**Jereme Sylvain** (Executives):
Sure. Thanks, Jeff. I can take you through -- while we won't get into specific pricing because there's obviously some competitive reasons behind that. It would typically be pretty sizably higher. And the reason is, is obviously, exclusive is very different than nonpreferred. And that's always embedded in contracts. And so it goes up by a pretty significant amount. In terms -- so that at least gives you some context. It's not like a 5% increase. It's much, much, much higher than that.
In terms of then what do I do? How do I navigate through this? What we're going to do is -- typically what you would have to do is you have to have the script. And so you'd write the script, and the script would go to either the DME or the pharmacy. In this case, you'd write the script to the DME provider and the DME provider then go ahead and check against you medical benefit, your prior authorization as needed and/or if you want to go through the prior authorization route with the actual PBM, which you also have that opportunity as well, that would go through. This is where Jake referred to Dexcom Direct comes directly into play there. That's where you can send a script there. We'll do the work for you. And so it makes it much easier for folks to understand, okay, where do I have access? What are my opportunities? Can I -- can you canvass the landscape for -- do I want to go cash pay? Do I want to go DME? Do I want to try for a prior authorization. Again, we'll do that work for you. So hopefully, that makes it much easier for the patient. I think it's a good opportunity for us to make sure that we're doing that work for them. The co-pay, it varies. It really depends on your individual insurance. And so what's happened typically is the DME will have a contract with the payer or in this case, the medical benefit payer. Sometimes it a percentage of the total list price. Sometimes it's a flat rate. It really depends. Typically, it's -- we typically see it in that 10% to 20% of total pay range per month. In high deductible health plans, you have the upfront cost, but then you get to full coverage going forward. So we've kind of talked about this historically as we had a DME business. It depends on the individual payer contracts. But obviously, we'll work best using that Dexcom Direct portal to try to maximize the opportunity for the individual. Hope that helps you, Jeff.

**Operator** (Operator):
And our next question comes from the line of Matthew O'Brien with Piper Sandler.

**Anna Runci** (Analysts):
This is Anna on for Matt. Just wanted to ask on the CONNECT data, now that that's fully out, wondering how much of a contributor NI type 2 patients were to the U.S. new patient start number in the quarter. I know it's still pretty early days, but just given that commercial coverage still exists for a pretty sizable chunk of the market, are there any signs that CONNECT is starting to shift that mix? And to the extent possible, is there -- how much of the improvement in the quarter reflects the growth of the category versus share gains?

**Jacob Leach** (Executives):
Yes. Thanks, Anna. So when we think about CONNECT, we're very excited to see it published in such a prominent journal, which really changes the conversation out there, and it makes the data very accessible to a large population of physicians and clinicians who read that journal. And so what I'd say is it's additional evidence. We already had a pretty significant amount of evidence, but this now being kind of the landmark irrefutable evidence of how Dexcom CGM can drive improvements in this population. It's really around helping our team that's out in the field raise awareness to the fact that we have these outcomes. And so it's really changing the conversation out there more towards very broad coverage expansion as we prepare for that.
When you think about new patients, to your question, the -- we are seeing a good number of non-insulin users in our new patient numbers. The insulin users are still the largest group, but the non-insulin users are not too far behind when you look at new patient numbers per quarter. And so as we continue to see coverage -- awareness of the coverage, I think that's been what we've been working on is making sure people are aware of that coverage because it wasn't very long ago that we got that commercial coverage for non-insulin users. And we're basically priming the pump for when the Medicare expansion occurs in that way, it will be much easier for prescribers because you get to the point where when Medicare moves, then you'll see some of the commercial plans move, and we get to the point where anybody who has diabetes should have access to CGM because of the benefits that we can provide across that broad spectrum of patients. So the CONNECT data is extremely helpful in carrying that message to all those prescribers.

**Jereme Sylvain** (Executives):
And then to your question on the overall market, you kind of look at the overall market, it is -- it remains stable. I think you've got 2 of the 3 largest CGM players out there, and you've got -- you combine the 2 and you're still in the low double digits, specifically in the U.S. in terms of revenue growth. And so it's still a stable market. Obviously, if you look at the results, you can see -- and you can see it in various other forms, I think we're doing a nice job taking share. And so a good chunk of that is us taking share there. But it is a stable market. I think we're excited to see it continue.

**Operator** (Operator):
And our next question comes from the line of Joanne Wuensch with Citi.

**Joanne Wuensch** (Analysts):
Did you update on the timing of expectations for non-intensive type 2 either the proposal and/or the implementation? And can you please update us on the time line or expectations for GA?

**Jacob Leach** (Executives):
Thanks, Joanne. We haven't changed our perspective on the Medicare timing. We still anticipate hearing back from Medicare around the coverage decision this year. And then our current plan has that coverage taking effect middle of next year. So nothing has changed there, very consistent. And it's consistent with the conversations we've been having. I've been spending quite a bit of time in Washington, talking to lots of different stakeholders. We've got our advocacy groups, lots of discussions going on around this coverage. And as I mentioned in my prepared remarks, we made sure that the Medicare directors who're making this decision had access to the CONNECT data. It was actually funny. They were very aware of the data even before it was published in the New England Journal, which I think is helpful, but we did make sure they have the official notice of that. And so yes, nothing has changed on that front at all.
And then on GA, the teams are continuing to make fantastic progress on that technology. We're seeing amazing results in the clinical studies that we're running around the accuracy and performance of that platform. It's a whole new platform for us with the -- with a new electronics sensor, everything kind of built into a 50% smaller volume with more capability than we have in the G7 platform. So making fantastic progress on that. And so nothing has changed in that timing either. We're still targeting depending on regulatory review time lines, either launching at the end of next year or early '28, kind of dependent on those time lines, but everything is very much on track.

**Operator** (Operator):
And our next question comes from the line of Jayson Bedford with Raymond James.

**Jayson Bedford** (Analysts):
Congrats on the progress. I wanted to ask about the distributor deal that you announced and see if we can get a bit more detail. What percent of the international -- your international business is covered by this distributor? And was there any impact in 3Q or an anticipated impact in the 4Q?

**Jereme Sylvain** (Executives):
Yes. So it's a good question. We'll have more specific details on it as we come up. We've signed the deal, it has not closed yet. So it's not going to impact this year. It's going to close next year, Jayson. So I think -- so in short, no impact in Q3, no impact in Q4. It certainly is a growth lever as we move into next year, as we lean into that market. It is essentially our largest remaining distributor market in Europe. So we'll be doing some work about taking that direct. So very excited about that opportunity here soon. But we are in the kind of sign-to-close phase. So in the close it will take while just because there's a lot of conditions that we have to go ahead and address. So thanks for the question. Probably have a little bit more about it as we get closer. And certainly, as we close the deal, we'll kind of give you a feel for what that size looks like, what the impact looks like. Ultimately, we'd expect, as you might expect, as we take these distributors direct as a growth lever, we are willing to invest in our business in a way that obviously others may not be.

**Operator** (Operator):
And our next question comes from the line of Steve Lichtman with William Blair.

**Steven Lichtman** (Analysts):
Jake, you mentioned the upcoming ADA standards of care update. Where do you hope that lands now with CONNECT in hand and published? And do the potential changes there give you more confidence in the ultimate coverage decision by CMS?

**Jacob Leach** (Executives):
Yes. Thanks, Steve. Yes, we anticipate that the CONNECT data is going to influence those -- the standards of care. And what it really is, it's all about the level of evidence. So when you -- the CONNECT study is Level A evidence. And so when you have Level A evidence, it is a strong recommendation for use of the technology in that population. So we very much believe that, that will have a significant impact on those standards of care, basically making the CGM standard of care for anybody with diabetes that we're rounding out the broad NIT group. So everything from type 1 through the different stages of type 2, CGM can have a significant benefit. So we do anticipate that.
And when it comes to confidence, yes, as standards of care change around the world, coverage also changes. And so as some paying -- payer systems recognize it sooner than others, but I think the important thing that we do is just keep the volume up on the noise around the benefits and make sure that everyone is aware of this new evidence that we've generated. And we're going to continue to generate evidence. We're not done here. I mean, we basically -- this is NIT, but as we look to the future, there's still lots of opportunity. If you think about the prediabetes population being able to screen that population and help them either prevent diabetes, reverse their pre-diabetes or significantly slow that progression of diabetes and all of the complications that I mentioned that come along with that. So we're very, very excited about that publication and it being out, our ability to talk about it and do feel like it's going to change standards of care around the world.

**Operator** (Operator):
And our next question comes from the line of Bill Plovanic with Canaccord Genuity.

**William Plovanic** (Analysts):
Yes. It's really -- mine is around G7 15 Day and the exit rate in 2026, I think is your commentary changing? I think you said nearly 50%. [ As I said ], you thought 50% in the past. I know it's a nuance.
And then just secondly, how much will Ireland impact this year? I mean, based on the guidance, it's like 130 to 150 bps sequentially. Is that how we should be thinking it and then it gets better as you get into Q1 and Q2 of next year as you're absorbing that overhead?

**Jereme Sylvain** (Executives):
Yes. So I think the 50% has always been nearly 50%. And so when we kind of gave a read coming into the year, I think the question was, where -- are you going to get to half? And I think we said nearly 50%. And by the way, it's tracking great towards that. So we're continuing to make good progress. And again, when we say nearly 50%, again, you're kind of making an estimation 12 months from now. And I got to say, we're pretty darn close. So certainly happy to see that, and that's been pretty consistent. And so that will be the thoughts there.
In terms of the jump-off point into next year, look, you can see some of the underlying improvement in 15 Day, obviously, over the course of this year. But a lot of that ultimately is also the work we've done around working on scrap and freight and some of the challenges that we had in the prior year, and you guys are paying close attention to it. You've seen our inventory levels stabilize on our books. And I think that's really important. That's allowed us to be more efficient as we've navigated through kind of how we're going to get product around the world. So all of that has contributed. What I think is great as you can see what happens in our gross margin with the existing facilities that we have. And so that's great. It's a starting point. Now obviously, we're guiding to a bit of a step back here in the fourth quarter. that's just going to be some of the turn on of Ireland and as we took a step back, it usually takes a few quarters for a facility to get up to kind of a normal volume ramp where you start to get back to normal. So we'll have some of those -- that drag into the first and to a lesser extent, the second and third quarter. And remember, these variances, they do amortize. And so even as you're getting more and more efficient, it does take time for when you make it to when you ultimately then distribute into the system. So I would expect us to take a little step back from Ireland, obviously in the fourth quarter as we move into next year. But underneath it all, I think the most important part of this is you can see where our exit rate is prior to Ireland. And obviously, as Ireland gets up to speed where our opportunity is, and that's prior to having 15 day as a majority of our product. Obviously, if we're getting to nearly 50% in the U.S exiting this year, next year, we would expect a majority of our product, obviously, to be on G7 15 Day. So I think there's some real opportunities here. We laid out some of kind of the progression drivers at Investor Day. Those are absolutely intact. And so I think that continued progression, I'd expect to see into next year, give you a little bit more color when we give official guidance, but I'd expect us to continue to make progress into next year's gross margin.

**Operator** (Operator):
And our next question comes from the line of Mike Kratky with Leerink Partners.

**Michael Kratky** (Analysts):
You mentioned your focus on utilization and retention metrics. So to what extent are you seeing those having a detectable impact in terms of your U.S. growth in 3Q? And can you help frame that magnitude?

**Jereme Sylvain** (Executives):
Yes. Thanks, Mike. One of the things we've been really, really focused on, and I encourage you to -- as you pay attention to all the work we're doing around customer success and the work we're doing around obviously, the product and doing all we can around the -- enhancing the product experience. What we would -- what we're seeing is a very stable retention and utilization, and that's across a base that's growing more and more in the type 2 NIT space. And so I think that's a positive thing. And so we are doing some of that work. While we don't necessarily break out, this is the bps from this, and this is the bips from that, I think what's important is the question often comes up, well, do you expect your retention and utilization to wane over time, especially as more and more folks come into the category. And I think the answer is, it's holding steady based on all the work we're doing around it. I think that's just an important thing to hold in the back of your mind. We're moving to more and more folks. Those folks, I think, are seeing the value where there's an opportunity to improve the customer experience, we're absolutely taking advantage of it, and we're not done. There's a lot of things we're going to roll out here in the fourth quarter and into next year that we're really excited about, something that we launched in the third quarter. We talked about my Dexcom account and a new platform that we rolled out in the U.S. in the past. Well, that rolled out in Europe already at this point, it is rolling out in APAC shortly after that. That really starts to enhance that customer experience so that someone once they get on the product, if they do have an issue, how do we help them? How do we help them in an efficient manner? How do we make sure we meet their needs. And then what we hope to do is how do we make it an excellent experience where they continue to come back and they see it as a differentiator. We're going to continue to work on that. So more to come on all the initiatives, and you'll start to see them coming up time after time. But I think the most important part is those concerns that folks may have had around retention utilization as we expand deeper into the population. I think the work we're doing is holding those steady, which is a great thing.

**Operator** (Operator):
And our next question comes from the line of Daniel Markowitz with Evercore ISI.

**Daniel Markowitz** (Analysts):
I wanted to talk a little bit about the basal opportunity. you talk about where we are in terms of contribution from Smart Basal? And if we could really see that step up? And if so, when?

**Jacob Leach** (Executives):
Yes. Thanks, Daniel. Yes, the Smart basal technology, we've been continuing to expand our pilot launch of that technology, and we're seeing really good results, both when it comes to patient and prescriber satisfaction with the system as well as the outcomes it's driving. What we're seeing is most of these patients are getting to their optimum basal dose in about 3 weeks, and that's with no hypoglycemia, which is one of the things that folks could be challenged with if they don't have a system like this. So it's getting -- rapidly getting folks to their optimum dose, driving the outcomes. The thing that prescribers love about it is the patients are actually taking their insulin and they're seeing the A1c levels come down. And so we continue to broaden the pilot there. One of the things we've learned is -- and we made a bunch of adoptions to the system around the workflow. So one of the things that we knew was that we designed the system for both patients and prescribers and the different user interfaces. And what we've learned over time is that based on some of the variability we see in the different setup of the clinics, we've needed to make changes to the way we manage counts, the way we make connections. The other thing too, is that many of these prescribers want to see this capability in the EHR. So we've been using all this time to basically optimize the system to be able to roll it out even more broadly. One of the things we're working on, too, is right now, the system is compatible with the most popular basal insulin glargine that's out there. But we're also now working to expand its -- the algorithms capability to do degludec and some of the higher consultation insulins. And so what we've learned is that to really make this an impactful feature, we want to have more compatibility with insulins. I feel that this is a very strong capability that's going to help drive our share in basal even higher because when a prescriber is thinking about basal insulin for a patient, this is the type of system you can put them on and ensure that they're going to get to that dose and ensure that they get the outcomes they're looking for in an easy and efficient way. And the -- because the patients love it so much, they're going to take their insulin. They're going to hit that outcome. So it has an opportunity to really expand the share that we are taking in that basal market. We'll -- more to come on exactly when we're going to roll it out more broadly, but we do ultimately intend to launch it, of course, here in the U.S. broadly as well as internationally because there are basal users all over the world that could benefit from those technology.

**Operator** (Operator):
And our next question comes from the line of Kieran Ryan with Deutsche Bank.

**Kieran Ryan** (Analysts):
Just kind of ties into the last question there, but I wanted to ask kind of about a PCP prescriber growth and productivity. Maybe you could talk a little bit about kind of how that's trending, where you're at on the sales force coverage penetration of that broader type 2 PCP market? And then kind of within that, anything you're learning on the non-insulin side as far as turning that coverage into starts ahead of Medicare, which I know is what really moves the needle there.

**Jereme Sylvain** (Executives):
Yes. Thanks for the question. This is Jereme. What we've seen in that space and we -- and maybe I'll start with the sales force and then kind of the learnings that are coming out of it. In terms of the sales force, we made the decision to expand the sales force a few years ago. It was with basal but ultimately with NIT in mind. And so we did that work and what we found over the years is there might be groups in areas that pop up and we might slightly modify sizes of territories because new prescribers are popping up. And so I think we're doing a nice job tweaking it without making massive changes to the sales force. So that's the first start. I think we have a pretty stable sales force. I would say, a stable and efficient sales force which is great, and we're seeing great results from that team. One of the things that we've learned is we've learned that, one, it's important to find the right prescribers that have the right patient group, obviously, if it's an NIT group with all Medicare patients,, ahead of Medicare expansion, it doesn't make sense to go and push non-insulin there. And so it's one of those things where as we learn more and more about the prescribers and ultimately, how they're prescribing, what they're prescribing. I think the team is getting ever more efficient about making sure they customize the approach as they get to the physician's office. Because you know this, I know this. We've all talked about this. You only get so much time with a physician in a primary care office. They're very, very busy. They're seeing patients all day long. And so it's making sure we're maximizing those touch points wherever we can. And we're using all sorts of tools to do it. And I think that's the other piece as well we've learned is making sure we're using tools internally that make us more efficient on those call points, but also using tools and creating tools that we bring into the physician's office like coverage calculators and ways that they can understand who and who does not have coverage, make sure they're efficient and who they prescribe for and how often they prescribe. So the learnings continue, I think we're getting better and better at it. But of course, there's always opportunities to continue to learn.

**Operator** (Operator):
And our next question comes from the line of Richard Newitter with Truist.

**Ravi Misra** (Analysts):
It's actually Ravi here for Rich. Just I want to turn back to the payer comments with the CVS. Just trying to understand how you size the risk of potential other payers that you're with going to exclusive peer platforms?
And then on Dexcom Direct, can you just walk through the impact that would have on maybe the back end and profitability per patient, DME used to require a little bit more investment. How does that kind of compare to what they should offer today?

**Jacob Leach** (Executives):
Yes. Thanks for the question, Ravi. As we look at it, most payers -- most of these -- the formularies are, as I mentioned, co-preferred, and I think they're like that for a reason. It's about ensuring that their customers, ultimately, they're in the business of serving beneficiaries and at this point in time, their beneficiaries want the choice of the systems they use and as do the prescribers and as do the employers. That's why when you look at these employer plans and the custom formularies that many folks operate off of, they have choice. And I think that's because that's what the customers want. Now the 2027 formularies are already kind of locked in, so there's no near-term issue there. And as we continue to have conversations throughout the market, we're going to make sure people understand the benefits of our technology as well as our push to ensure that there's equal access for patients so that they can get the technology that they need.

**Jereme Sylvain** (Executives):
Yes. And to your question on Dexcom Direct and how that works from an economics perspective, I mean, certainly, we've talked about this other times in the past where there are certain channels that tend to be higher reimbursed DME. There's kind of the middle, which we'll call government, and then there's kind of pharmacy commercial. And all those incur whatever the underlying OpEx burden is associated with it. So you're 100% right there. As more folks move, for example, from one location to the other, certainly, the costs associated with rightsizing and we've kind of got a pretty good structure to navigate through those right now. So I don't expect there to be a significant underlying cost structure for us because we've already kind of invested in high-volume capabilities across both. There'll be a little bit of a cost of handholding that goes through. So you're absolutely right. There will be a cost underneath it to support the benefits check, the white glove service that we expect to provide for folks. But that would all be embedded in kind of sort of the run rate and investment areas that we make as an organization. And so in the context, you are right, there's a little bit of an incremental cost associated with it, but we'll ultimately be able to assume that into what I'd say is our growth algorithm because we do make investments. I mean every year, we make investments in the business. And this is one we intended to make irrespective of this announcement. We wanted folks, especially as you had CMS expansion to know what their options were. Because if you remember, CMS expansion is one side on the fee-for-service side, but then you've got to navigate to the Medicare Advantage side. And so making sure that we're helping the population navigate through what's a pretty complicated environment. That was always part of the plan, and it'd be part of what of our long-term plans were when we set our LRP out, quite frankly. This is something we've been thinking about for a long, long time.

**Operator** (Operator):
And our final question comes from the line of Marie Thibault with BTIG.

**Marie Thibault** (Analysts):
And I wanted to ask a little bit about operating expenses. You've been exceeding expectations on operating margin. And I know you raised the target here for the full year. How should we be thinking about Q4 exiting 2026? I know, obviously, some dynamics with Ireland and shifting spend there. And you've answered the question on not needing to expand the sales force. But what else should we be looking for on OpEx and investments needed there, whether that's G8 or other priorities like that?

**Jereme Sylvain** (Executives):
Sure. Yes. I mean I think -- at least as we think about OpEx for the remainder of this year into next year, you're 100% correct. We are going to make sure we invest in G8. We've got some clinical work to do for G8 as we get ready for submission to the FDA. And so there'll be some investment there. I would expect to see us continue to invest in obviously expansion, and we talked earlier about Dexcom Direct and some investment there. At the same time, remember, we are not investing in an Ireland expansion next year. And so there's an opportunity to gain leverage there. So we'll make the right investments in the business to drive growth. But I think you've seen our LRP expectations, and you've seen us historically be able to do it. We can invest in the organization, and we do invest in the organization. Every year, we add a couple of hundred million dollars to OpEx. And so we'll continue to do that, but we can do that while gaining leverage as we're going through the process. And I would expect us to make the investments we need to make, but also continue to be able to get the leverage we need to over time in 2027 and quite frankly, beyond. And we laid it out in the LRP, nothing's changed from our thoughts on how we can track towards that. So thank you for the question, and thank you for the acknowledgment over time. It's been a lot of work and great work by the organization in getting that leverage.

**Operator** (Operator):
And that concludes our question-and-answer session. I would now like to turn the call back over to Mr. Jake Leach for closing remarks.

**Jacob Leach** (Executives):
Thank you, Abby. I just want to close the call by saying how proud I am of the execution we delivered this quarter and throughout the year. The progress really reflects the commitment of our employees around the world. And I do want to thank them all for everything they do for Dexcom and for the people we serve. We're confident in our plan. We're energized by the opportunities we see ahead of us, and we're focused on execution.
And as we head in November, which is National Diabetes Awareness month, it's a meaningful reminder of why the work we do matters and the positive impact we can have on the lives of millions of people living with diabetes. Thank you all for joining us.

**Operator** (Operator):
And ladies and gentlemen, this concludes today's call, and we thank you for your participation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### DXCM_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO｜guidance：全年營收財測上調中點，區間 $5.18–5.25B（原話："an updated range of $5.18 billion to $5.25 billion"）
- 2026-07-30｜CFO｜guidance：匯率對下半年國際營收約 $15M 影響（原話："about a $15 million impact to international revenue"）
- 2026-07-30｜CFO｜guidance：排除匯率後有機成長預期較前次財測上調（原話："an increase in organic growth by more than 50 basis points"）
- 2026-07-30｜CFO｜guidance：全年 non-GAAP 毛利率財測約 64%（原話："gross profit margin guidance to approximately 64%"）
- 2026-07-30｜CFO｜margin：全年 non-GAAP 營業利益率財測 23.5%–24%（原話："operating profit margin guidance to a range of 23.5% to 24%"）
- 2026-07-30｜CFO｜margin：Q2 毛利率較去年同期改善約 400bp（原話："margins improving approximately 400 basis points"）
- 2026-07-30｜CFO｜margin：管理層說明毛利率高點預期在 Q3，Ireland 投產後下降（原話："The expectation was always a peak into Q3 in gross margin"）
- 2026-07-30｜CFO｜margin：毛利率財測上調歸因於產線表現而非油價（原話："the raise is really on underlying performance improvements"）
- 2026-07-30｜CFO｜margin：管理層稱 15 Day 對毛利的幫助為多年期、無單一季度見頂（原話："there's not really 1 quarter where it plateaus"）
- 2026-07-30｜CFO｜margin：營業費用槓桿優於計畫（原話："We've had some operating leverage really ahead of plan"）
- 2026-07-30｜CFO｜margin：Ireland 投產前將有招聘與折舊，Q3 繼續投資（原話："we'll start some depreciation as well"）
- 2026-07-30｜CFO｜guidance：有機營收定義（排除匯率及近12個月併購/出售的非CGM營收）（原話："our definition of organic revenue excludes the impact"）
- 2026-07-30｜CEO｜product：美國客戶 G7 15 Day 年底轉換目標近 50%（原話："convert nearly 50% of our U.S. customer base"）
- 2026-07-30｜CFO｜product：15 Day 全年平均滲透率約 20–25%，明年起點近 50%（原話："you're at 20%, 25%"）
- 2026-07-30｜CEO｜product：Health Canada 為首個核准 G7 15 Day 的海外監管機構（原話："Health Canada became the first international regulator"）
- 2026-07-30｜CEO｜commitment：承諾 2026 下半年將 G7 15 Day 帶到加拿大（原話："bringing G7 15 Day to Canada in the second half of 2026"）
- 2026-07-30｜CEO｜product：G8 時程仍維持，2027 年底至 2028 年初視法規時程（原話："very much on track for that end of 2027, early 2028"）
- 2026-07-30｜CEO｜product：Smart Basal 試點使客戶 3 週達最佳基礎胰島素劑量（原話："reach an optimal basal dose in only 3 weeks on average"）
- 2026-07-30｜CEO｜product：Dexcom 為 FDA TEMPO 試點首家入選公司（原話："first company chosen to participate in the TEMPO"）
- 2026-07-30｜CEO｜product：CONNECT 試驗 A1c 改善 1.6%（原話："1.6% A1c improvement for the Dexcom CGM group"）
- 2026-07-30｜CEO｜customer：四大商業 PBM 已涵蓋所有糖尿病患（原話："across the 4 largest commercial PBMs"）
- 2026-07-30｜CEO｜customer：美國有保險覆蓋但未使用 CGM 者約 900 萬人（原話："approximately 9 million people in the United States"）
- 2026-07-30｜CEO｜guidance：CMS 非胰島素第二型涵蓋決定預計年底前回覆（原話："We do expect to hear back from CMS on that decision"）
- 2026-07-30｜CEO｜commitment：公司計畫中 CMS 涵蓋生效時點為 2027 年中（原話："we've got it taking effect in the middle of 2027"）
- 2026-07-30｜CFO｜capital_allocation：2026 年承諾回購 $10 億股票（原話："a commitment to repurchase $1 billion of stock in 2026"）
- 2026-07-30｜CFO｜capital_allocation：Q2 已回購約 $6 億（原話："repurchased approximately $600 million in the second quarter"）
- 2026-07-30｜CFO｜capital_allocation：上半年自由現金流逾 $6 億（原話："more than $600 million in free cash flow"）
- 2026-07-30｜CFO｜capital_allocation：完成 Nutrisense 收購（原話："we completed the acquisition of Nutrisense"）
- 2026-07-30｜CFO｜capital_allocation：Nutrisense 非 CGM 營收極小（原話："you can count the millions for the year on one hand"）
- 2026-07-30｜CFO｜capital_allocation：資本配置框架含小型併購評估（原話："ongoing assessment of tuck-in M&A"）
- 2026-07-30｜CFO｜customer：新客戶數 Q2 與 Q1 全球紀錄持平（原話："Q2 is in line with the record globally"）
- 2026-07-30｜CFO｜customer：新客戶中美國環比增加、海外下降（原話："This means the OUS patients came down a bit"）
- 2026-07-30｜CEO｜risk：去年 out-of-box 失效率問題曾使客戶不滿（原話："out-of-box failure rates that disrupted things"）
- 2026-07-30｜CEO｜risk：下半年國際比較基期變高（原話："the comps get a little tougher"）
- 2026-07-30｜CFO｜risk：匯率假設：6/30 為 1.14（原話："As of June 30, when we're thinking about it's $1.14"）
- 2026-07-30｜CEO｜customer：真實世界非胰島素第二型使用率逾 80%（原話："not quite at 97%, but well above 80% in this population"）
- 2026-07-30｜CEO｜competition：管理層否認 CMS 將設 A1c 門檻之說（原話："that's not consistent at all with what we hear"）
- 2026-07-30｜CEO｜commitment：長期目標：現金流與利潤率輪廓（原話："one of the more compelling cash flow and margin profiles"）
- 2026-07-30｜CFO｜product：Dexcom Flex 在德國上市（原話："launch of Dexcom Flex in Germany"）

### DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 表示長期計畫（LRP）至 2030 年每年營收成長 10% 以上（原話："10% plus every year, each year in our LRP through 2030"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 澄清 10% 以上不是 CAGR 或平均，而是逐年（原話："It's 10% plus each year every year."）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 說 LRP 已納入 2028 年起的競標假設（原話："competitive bidding assumptions starting in 2028"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 說 LRP 已納入競爭對手新品上市假設（原話："competitor product launches over the course of time"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 回答價量組合：價格假設每年約 2% 至 3%（各年不同）（原話："we've typically thought about 2% to 3% price"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 對競標的假設：納入名目價格影響（原話："some nominal price impacts associated with it"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 說 LRP 中 Medicare 涵蓋時點假設為 2027 年中（原話："for LRP purposes, we put it in the middle of 2027"）
- 2026-05-14｜Jacob Leach｜guidance：CEO 表示公司規劃假設 CMS 涵蓋於明年年中生效（原話："coverage will come the middle of next year"）
- 2026-05-14｜Jon Coleman｜guidance：Coleman 在 Q&A 說 CMS 非胰島素型涵蓋從未預期在 2026 年發生（原話："we never anticipated that to happen in '26"）
- 2026-05-14｜Jon Coleman｜guidance：Coleman 說若 CMS 涵蓋提早，屬上行空間（原話："mid-'27 is when the coverage will actually kick in"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 預期全球涵蓋人數 2030 年底約 5200 萬（目前約 2300 萬）（原話："We expect to exit around 52 million"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 假設 2030 年第二型滲透率 10% 至 15%（原話："type 2 in the 10% to 15% range"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 假設 CMS 涵蓋後滲透速度為 basal 的一半（原話："CMS penetration goes at half the rate of basal"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 說明配戴使用率假設沿用網站所列 75% 至 80%（原話："the 75% to 80% utilization"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 說留存與使用率提升的上行未放進 LRP（原話："we haven't put any of this into our LRP"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 預期 LRP 結束時毛利率升至 60% 後段（原話："We expect gross margin to grow into the high 60s"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 預期 LRP 結束時非 GAAP 營業利益率 29% 至 30%（原話："get to 29% to 30% by the end of the end of the LRP"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 說營業利益率每年約擴張 150 bp，主要來自毛利率（原話："about 150 basis points a year"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 預期調整後 EBITDA 利益率升至 36% 至 37%（原話："adjusted EBITDA margin to grow to 36% to 37%"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 預期 G8 製造成本較 G7 至少低 10%（原話："it costs at least 10% less than it cost to make G7"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 提及 15 日款保固率可能小幅上升（管理層認為可接受）（原話："the warranty rate may go up a little bit"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 說近期毛利率機會：今年底美國約近半數用戶轉 15 日款，次年起點更高（原話："approaching 50% of our population moved over"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 說去年營運費用改善 300 bp，來自 cost to execute 框架（原話："300 basis points of operating expense improvement"）
- 2026-05-14｜Jacob Leach｜margin：CEO 說公司目前營業利益率已超過 20% 且仍有空間（原話："operating at margins of over 20% with additional room to go"）
- 2026-05-14｜Jereme Sylvain｜capital_allocation：CFO 表示 10 億美元回購授權將於 2026 年執行完畢（原話："It will be fully executed in 2026."）
- 2026-05-14｜Jereme Sylvain｜capital_allocation：CFO 提出未來每年至少 50% 自由現金流用於回購（原話："at least 50% of our annual free cash flow to repurchases"）
- 2026-05-14｜Jereme Sylvain｜capital_allocation：CFO 稱股價有落差時要回購（原話："And boy, we see a big one today."）
- 2026-05-14｜Jereme Sylvain｜capital_allocation：CFO 列出支持小型併購為資本配置用途之一（原話："We want to be able to support tuck-in M&A."）
- 2026-05-14｜Jacob Leach｜commitment：CEO 說 G8 預計明年送件，2027 年底或 2028 年初上市（原話："a launch either at the end of '27 or early '28"）
- 2026-05-14｜Jacob Leach｜commitment：CEO 說今年底前轉換近半美國用戶至 G7 15 日款（原話："convert nearly half of our U.S. base over to this product"）
- 2026-05-14｜Jacob Leach｜commitment：CEO 說明年推出醫院連續血糖監測產品（原話："We want to be able to support tuck-in M&A."）
- 2026-05-14｜Jacob Leach｜commitment：CEO 說酮體感測會納入 G8 平台但時程在後（原話："Ketones, it will be part of the G8 platform."）
- 2026-05-14｜Jacob Leach｜commitment：CEO 說 G8 之後將有多分析物版本（原話："right behind that product is a multi-analyte version of G8"）
- 2026-05-14｜Jon Coleman｜commitment：Coleman 表示國際收入願景：LRP 結束時達數十億美元（原話："you'll see multibillions of dollars in international"）
- 2026-05-14｜Jacob Leach｜product：CEO 說 Smart Basal 把達到合適劑量的時間從 12 週以上縮短到 30 天內（原話："from over 12 weeks to fewer than 30 days"）
- 2026-05-14｜Jacob Leach｜product：CEO 說 EHR 直接整合已有逾 320 家醫療系統整合或導入中（原話："We have over 320 health systems"）
- 2026-05-14｜Jacob Leach｜product：CEO 說 G7 產線可改裝生產 G8，支援產能（原話："retrofit the G7 lines to manufacture these G8 systems"）
- 2026-05-14｜Jacob Leach｜product：CEO 承認貼片黏著問題尚未完全解決（原話："the code is definitely not cracked"）
- 2026-05-14｜Jon Coleman｜product：CEO 說 Flex 美國是否推出（另一產品或 App）尚未決定（Coleman 回答）（原話："We've not yet made that decision"）
- 2026-05-14｜Jon Coleman｜competition：Coleman 稱公司相對競爭對手已有留存優勢，並預期差距擴大（原話："We've already got a retention advantage"）
- 2026-05-14｜Jeffrey Johnson｜competition：分析師提到最大競爭對手在酮體上有進展，詢問 Dexcom 路徑（原話："your biggest competitor is still making progress"）
- 2026-05-14｜Jon Coleman｜customer：Coleman 說基層醫療處方份額從 2023 年約 30% 升到 2025 年近 40%（原話："2025 has grown close to 40%"）
- 2026-05-14｜Jon Coleman｜customer：Coleman 說先前擴編美國銷售團隊 40%（原話："expand the sales force in the United States by 40%"）
- 2026-05-14｜Jacob Leach｜customer：CEO 說使用者停用 CGM 的首要原因之一是認為數據不夠可靠（原話："they don't feel that the glucose data is reliable enough"）
- 2026-05-14｜Jacob Leach｜customer：CEO 說非胰島素型第二型患者目前僅 25% 有涵蓋（原話："we're only 25% covered"）
- 2026-05-14｜Jacob Leach｜customer：CEO 說第一季國際成長多數來自新開通涵蓋的市場（原話："most of that growth came from new markets"）
- 2026-05-14｜Jacob Leach｜customer：CEO 提到另一家 PBM 今年起涵蓋所有糖尿病人（原話："another PBM, the next largest, starting to cover CGM"）
- 2026-05-14｜Jacob Leach｜risk：CEO 宣布與 Elliott 合作新增 2 名董事（原話："recruit 2 new Board directors to our Board"）
- 2026-05-14｜Jacob Leach｜risk：CEO 說正在招聘新設的 Chief Product Officer（原話："a brand-new role at Dexcom, a Chief Product Officer"）
- 2026-05-14｜Jacob Leach｜risk：CEO 說董事會目前沒有獨立的醫材董事（原話："We don't have independent med tech directors on our Board"）
- 2026-05-14｜Jereme Sylvain｜risk：CFO 說 CMS 關注點在詐欺性帳單，競標影響有限（原話："CMS is heavily focused on fraud"）

### 問答異常語氣（迴避／改口／保留）
- DXCM_Q2_2026_Earnings_Call_20260730.md｜問：Polark 請管理層就產品表現給具體指標（報廢、保固、退貨、客訴）｜答法：CEO 以 NPS 連三季上升及客訴下降作答，未給報廢/保固/退貨數字；CFO 指向毛利率改善為佐證
- DXCM_Q2_2026_Earnings_Call_20260730.md｜問：Block 詢問毛利率財測上調是否含油價緩衝｜答法：CFO 解釋樹脂成本遞延流入並稱與上季指引大致一致，未明確回答是否仍有油價緩衝
- DXCM_Q2_2026_Earnings_Call_20260730.md｜問：Wuensch 詢問 Nutrisense 收購金額｜答法：CFO 未公開金額，指向 10-Q 現金流量表
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Jeffrey Johnson（Baird）追問酮體感測的時程與路徑｜答法：CEO 說酮體會納入 G8 平台，但明說不給任何確切時間表（"I'm not going to give any exact time lines"），改談 G8 準確度優先、臨床工作仍待完成
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Larry Biegelsen（Wells Fargo）問銷售與利潤率假設的逐年節奏｜答法：CFO 未給逐年數字，表示 "We don't have a cadence to provide"，留待年度財測
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Joanne Wuensch（Citi）問 10% 以上各年哪年較強｜答法：CFO 不分年度給數字，只說 10% 以上是基礎情境，逐年細節留給年度財測，僅提供各年催化劑
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Matt O'Brien（Piper Sandler）問 LRP 中美國與國際成長的相對關係｜答法：CEO 以存取擴張時點難控制回答，CFO 說「兩者都不輕忽」，未給美國與國際的成長拆分數字
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Rich Newitter（Truist）問國際成長是否高於美國、美國是否需要第二型非胰島素型才能維持雙位數｜答法：CFO 表示未拆分美國與國際，改談涵蓋是成長演算法核心，未直接回答美國單獨是否雙位數
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Joanne Wuensch（Citi）問 Flex 是否會帶到美國｜答法：Coleman 表示尚未決定是否為不同產品或 App，不願多談
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Chris Pasquale（Nephron）問 G8 上市後的轉換策略｜答法：CEO 說「沒有具體轉換計畫」，只表示希望快速轉換

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
{"status":"no_prior_dd"}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DXCM_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
