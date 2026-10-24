你是 stock-analyst **v20 判斷 agent**，標的 WDC（20261024）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"WDC","date":"2026-10-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261024/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261024/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":3747,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":1655,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"USD M（利益率 44.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":1563,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"USD M（利益率 41.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}},{"id":"f_kpi5_non_gaap","label":"Non-GAAP 毛利率","value":54.4,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"%（GAAP 54.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}},{"id":"f_kpi6_q1_fy2027_non_gaap","label":"管理層指引：Q1 FY2027（non-GAAP）","value":"營收 4.1B ±100M（YoY +42%~49%）；毛利率 55%~56%；營業費用 390~400M；EPS 4.00 ±0.15","period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"—","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-22","period":"2026-10-22","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-22"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_wdc_gross_margin_pct","label":"WDC 毛利率","value":48.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WDC.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_wdc_operating_margin_pct","label":"WDC 營業利益率","value":35.6,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WDC.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_wdc_fcf_margin_pct","label":"WDC FCF 利潤率","value":27.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WDC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sndk_gross_margin_pct","label":"SNDK 毛利率","value":71.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sndk_operating_margin_pct","label":"SNDK 營業利益率","value":61.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sndk_fcf_margin_pct","label":"SNDK FCF 利潤率","value":56.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_gross_margin_pct","label":"000660.KS 毛利率","value":76.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_operating_margin_pct","label":"000660.KS 營業利益率","value":68.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_fcf_margin_pct","label":"000660.KS FCF 利潤率","value":47.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_gross_margin_pct","label":"005930.KS 毛利率","value":57.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_operating_margin_pct","label":"005930.KS 營業利益率","value":36.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_fcf_margin_pct","label":"005930.KS FCF 利潤率","value":28.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":1281,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"USD M（營運現金流 1,389，淨資本支出 108）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}},{"id":"f_kpi4_sbc","label":"SBC","value":45,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"USD M（占 GAAP 營業利益 2.9%、占營收 1.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":343.67,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-14.88,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_rsi14","label":"RSI(14)","value":35.75,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":19.37,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.81 → 24.84）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":16.01,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（33.8 → 39.21）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":15.8,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（43.79 → 50.71）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":24.84,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":39.21,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":50.71,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":149.4,"period":"2026-07-30 → 2026-10-24","unit":"%","basis":"FY1 共識 EPS 9.96 → 24.84（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":13.84,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 24.84，分子＝快照價 343.67","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.16,"period":"2026-10-24","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-24"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟢","period":"2026-10-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 343.67 / W52 362.33 / W104 212.22 / W250 110.32 / W250 13週斜率 4.95%"},{"id":"f_ma_w52","label":"52 週均線","value":362.33,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":212.22,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":110.32,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":4.95,"period":"2026-10-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Nikkei 報導 Toshiba 計畫 HDD 產能於 FY2027 前約倍增，容量份額目標由約 10% 拉到 30%；報導後 2026-10-02 WDC 約跌 10%、STX 約跌 15%，Fool 文章並指 Toshiba 可能以低價搶單壓縮 WD 毛利","source":"Motley Fool, Why Western Digital Stock Just Crashed","url":"https://www.fool.com/investing/2026/10/02/why-western-digital-stock-just-crashed/","excerpt":"Toshiba aims to lift its HDD share by storage capacity from just over 10% to 30% over the medium term, according to Nikkei.","as_of":"2026-10-02","retrieved_at":"2026-10-13","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"2026 年 8 月報導 HDD 份額：WD 約 42%、Seagate 41%、Toshiba 17%（未見 2026 年 WD 增減份額的季度序列）","source":"Motley Fool / 搜尋彙整 (2026-08 report)","url":"https://www.fool.com/investing/2026/10/02/why-western-digital-stock-just-crashed/","excerpt":"In terms of HDD market share, WD currently represents approximately 42% of the market, followed closely by Seagate at 41% and Toshiba at 17%.","as_of":"2026-08-31","retrieved_at":"2026-10-13","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"HAMR 進度：Seagate 已有兩家大型 hyperscaler 量產採購 Mozaic 4+；WDC 預計 2026 上半年與一家 hyperscaler 開始認證、年底擴至最多三家，量產爬坡 2027 上半年（3dnews 另稱 2026 年底開始 HAMR 生產，時間不一致）","source":"Nasdaq/Zacks, Seagate vs. Western Digital: Which Storage Stock is the Better Buy Now?","url":"https://www.nasdaq.com/articles/seagate-vs-western-digital-which-storage-stock-better-buy-now","excerpt":"WDC remains on track to begin qualification with one hyperscale customer in the first half of 2026, expanding to up to three customers by year-end.","as_of":"2026-07-29","retrieved_at":"2026-10-13","affects":["moat_trend","triggers"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Coughlin 2025 Q1 資料：WD 單位份額 42%（179.8 EB）、Seagate 40%、Toshiba 18%，WD 自 Toshiba 取得約 1 點份額","source":"Blocks & Files (Coughlin newsletter)","url":"https://blocksandfiles.com/?p=38863","excerpt":"Western Digital at 179.8 EB and 42% of unit share, Seagate at 143.6 EB and 40%, and Toshiba at 41 EB and 18%.","as_of":"2025-06-01","retrieved_at":"2026-10-13","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"長期替代風險為 flash（SanDisk、Samsung、Micron、Kioxia）；未找到具名的 HDD 新進入者；WD 已把 SSD 業務分出，專注 HDD","source":"Seeking Alpha, Western Digital: Watch For Technological Threats Following Post-Earnings Sell-Off","url":"https://seekingalpha.com/article/4933754-western-digital-watch-for-technological-threats-following-post-earnings-sell-off","excerpt":null,"as_of":"2026-08-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"WDC FY2026 10-K：三個客戶分別占 FY2026 淨營收 16%、15%、13%；前十大客戶占 73%（FY2025 68%、FY2024 55%），FY2024 無單一客戶達 10%。","source":"SEC WDC Form 10-K FY2026 (period ended 2026-07-03)","url":"https://www.sec.gov/Archives/edgar/data/0000106040/000162828026057139/wdc-20260703.htm","excerpt":null,"as_of":"2026-07-03","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"管理層稱前七大客戶已下單至 2026 上半年、其中五家涵蓋全年 2026；一家大型超大規模客戶簽了涵蓋 2027 全年的協議（2025 年 10 月財報說明）。","source":"Blocks & Files, Western Digital extends lead over Seagate as AI drives demand tailwinds","url":"https://blocksandfiles.com/2025/10/31/western-digital-extends-lead-over-seagate-as-ai-drives-demand-tailwinds/","excerpt":null,"as_of":"2025-10-31","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Qualstar 稱 Microsoft、Amazon、OVH、Baidu 在其封存層下方使用自動化磁帶，超大規模業者已將冷儲存下層分散化（非 HDD 自製或第二供應商的直接證據）。","source":"Qualstar, How hyperscale data growth is changing the future of cold storage","url":"https://www.qualstar.com/blog/how-hyperscale-data-growth-is-changing-the-future-of-cold-storage","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"WDC FY2026 10-K：前 10 大客戶占淨營收 73%（FY2025 68%、FY2024 55%）；三家客戶各占 16%、15%、13%（合計 44%）","source":"SEC EDGAR, WESTERN DIGITAL CORP Form 10-K FY2026 (period ended 2026-07-03)（內容經搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/0000106040/000162828026057139/wdc-20260703.htm","excerpt":null,"as_of":"2026-07-03","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"WDC 執行長於 2026 年 1 月財報會表示 2026 年 HDD 產能幾乎售罄，並有長期框架協議延伸至其後年度；多年合約涵蓋 2027、2028。","source":"Gigazine, Western Digital 2026 HDD capacity runs out (2026-02-16)","url":"https://gigazine.net/gsc_news/en/20260216-western-digital-2026-hdd-capacity-runs-out","excerpt":null,"as_of":"2026-02-16","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"WDC 與前五大客戶中三家有商業協議，兩家至 CY2027、一家至 CY2028（搜尋彙整引述 CEO 說法；日期為彙整，非原始發布日，未能核實原文日期）。","source":"WebSearch 彙整（NAND/HDD 展望，techspot 等二手來源）","url":null,"excerpt":"robust commercial agreements with three of our top five customers, two through calendar year 2027 and one through calendar year 2028","as_of":"2026-02-16","retrieved_at":"2026-10-13","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"傳聞 Toshiba 計畫投資約 600 億日圓（約 3.8 億美元）於菲律賓，於 FY2027 前將 HDD 產出約翻倍，市佔由約 10% 朝 30% 提升；Toshiba 未證實；消息使 Seagate 跌約 10%、WDC 跌約 7%。","source":"247WallSt, Seagate Tumbles 10%, Western Digital Drops 7% as Toshiba Moves to Double Hard Disk Output (2026-10-02)","url":"https://247wallst.com/investing/2026/10/02/seagate-tumbles-10-western-digital-drops-7-as-toshiba-moves-to-double-hard-disk-output/","excerpt":null,"as_of":"2026-10-02","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Morgan Stanley 認為即使加計 Toshiba 新產能，HDD 市場至 2028 仍供不應求；Citi 認為 Toshiba 擴產對全球供給影響有限（platter 與磁頭仰賴外部供應商）。","source":"WebSearch 彙整：Tikr/Blocksandfiles/247WallSt 報導（2026-10 初）","url":"https://www.blocksandfiles.com/disk/2026/10/06/distant-third-hdd-maker-toshiba-spending-380-million-to-catch-up/5301322","excerpt":null,"as_of":"2026-10-06","retrieved_at":"2026-10-13","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce 稱雙寡頭售罄並維持供給紀律，Toshiba 因投資到量產有時滯短期貢獻有限；隨雙寡頭轉 HAMR，供需將逐步趨近平衡，WDC 的 HAMR 進度為關鍵變數；預期 Seagate 將超越 WDC 成最大供應商。","source":"TrendForce, Seagate to Top HDD Market by 2028 on HAMR Lead (RP261007HN)","url":"https://www.trendforce.com/research/download/RP261007HN","excerpt":null,"as_of":"2026-10-07","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.R","triggers"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Seagate 稱 nearline 容量多數已分配至 2028；NAND 方面 TrendForce 預期 2026 供給缺口 4–5%，2027 下半年供給成長超過需求（NAND 非 WDC 主營 HDD，僅供背景）。","source":"WebSearch 彙整（TechSpot/DigitalCitizen NAND shortage ease 2027；pcserverandparts）","url":"https://www.techspot.com/news/113186-nand-shortages-could-finally-ease-2027-but-adata.html","excerpt":"The analyst firm says the market will remain undersupplied throughout 2026, recording a supply deficit of between 4% and 5%","as_of":"2026-10-13","retrieved_at":"2026-10-13","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2026 10-K 風險因素僅一般性揭露：公司過去及未來可能涉及含反壟斷在內的訴訟，並可能面臨政府與監管機關的查詢、調查；未點名任何現行的具體反壟斷調查或拆分案。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/106040/000162828026057139/wdc-20260703.htm","excerpt":"We have in the past been and may in the future be the subject of inquiries, requests for information, investigations and actions by government and regulatory agencies regarding our businesses.","as_of":"2026-08-14","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"WDC 10-Q（期間至 2026-01-02）稱截至 FY2026 第二季，營運與業績未因關稅行動受到重大影響，公司持續監控。","source":"WESTERN DIGITAL CORP Form 10-Q (quarter ended 2026-01-02)","url":"https://www.sec.gov/Archives/edgar/data/106040/000162828026004207/wdc-20260102.htm","excerpt":null,"as_of":"2026-01-02","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-01-14 總統公告依 Section 232 對一小組先進半導體及含其之衍生品課 25% 關稅（2026-01-15 生效），豁免含美國資料中心用途等；搜尋結果未顯示硬碟／NAND 是否屬涵蓋品項。","source":"White & Case, President Trump orders narrowly targeted 25% Section 232 tariff on certain advanced semiconductor articles","url":"https://www.whitecase.com/insight-alert/president-trump-orders-narrowly-targeted-25-section-232-tariff-certain-advanced","excerpt":null,"as_of":"2026-01-14","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Section 232 第二階段可能在貿易談判結束後課「顯著」關稅；商務部與 USTR 須於 2026-04-14 前提交談判更新，搜尋未找到更新內容。","source":"Baker McKenzie Global Import Blog, US President Trump issues Section 232 proclamations on semiconductors and critical minerals","url":"https://globalimportblog.bakermckenzie.com/2026/01/27/us-president-trump-issues-section-232-proclamations-on-semiconductors-and-critical-minerals/","excerpt":null,"as_of":"2026-01-27","retrieved_at":"2026-10-13","affects":["triggers","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"DatacenterDisk 分析稱硬碟主要在泰國與馬來西亞組裝，零組件來自日本（碟片）、中國（電子件）、菲律賓（組裝）；對泰、馬、韓、中電子產品的關稅加劇 AI 驅動的缺貨，稅率多次宣布、暫停、修改再恢復。","source":"DatacenterDisk, US tariffs hard drive SSD prices 2026","url":"https://datacenterdisk.com/news/us-tariffs-hard-drive-ssd-prices-2026","excerpt":null,"as_of":"2026-03-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"搜尋未發現 WDC 本身被列入 Entity List 或遭 2026 年新的中國專屬出口管制；MOFCOM 2026-06-22 公告第 23 號新增的十家美國實體不含 WDC。","source":"Sinolytics Radar 241","url":"https://sinolytics.de/documents/Sinolytics-Radar-241.pdf","excerpt":null,"as_of":"2026-06-22","retrieved_at":"2026-10-13","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"有節目簡介稱 WDC 製造足跡高度集中於泰國與馬來西亞，並受新「原產地」解釋審視（二手來源，未對照 10-K）","source":"Audible 2026Q2 Western Digital Corporation (WDC) 節目簡介","url":"https://www.audible.co.uk/pd/B0GNX9CPQ1","excerpt":"Western Digital's manufacturing footprint, heavily concentrated in Thailand and Malaysia, faces scrutiny under new \"Country of Origin\" interpretations","as_of":"2026-07-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"磁頭獨立供應商僅 TDK 一家，同時供應三大 HDD 廠（引 Bloomberg，經供應商部落格轉述）","source":"Fusion Worldwide blog: How China's export controls are disrupting HDD manufacturing and supply","url":"https://info.fusionww.com/blog/how-chinas-export-controls-are-disrupting-hdd-manufacturing-and-supply","excerpt":"TDK is the only independent supplier of magnetic recording heads and currently supplies all three HDD giants.","as_of":"2026-01-01","retrieved_at":"2026-10-13","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中國稀土出口管制：中重稀土出貨仍需逐案核准，暫停期至 2026-11-10（供應商部落格轉述）","source":"Fusion Worldwide blog: Is Hard Disk Drive Supply the Next Major Infrastructure Bottleneck?","url":"https://info.fusionww.com/blog/is-hard-disk-drive-supply-the-next-major-infrastructure-bottleneck","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-13","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"WDC 10-Q 稱關稅行動截至 2026 會計年度第一季未對經營造成重大影響，持續監控","source":"WDC Form 10-Q (period ended 2025-10-03)","url":"https://www.sec.gov/Archives/edgar/data/106040/000162828025047613/wdc-20251003.htm","excerpt":"Our business and results of operations have not been materially impacted through the first quarter of 2026 as a result of the recent tariff actions, but we are actively monitoring developments.","as_of":"2025-11-01","retrieved_at":"2026-10-13","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"法說會答覆稱已開發稀土與貴金屬替代供應來源，預期出口管制無重大影響（逐字稿日期未顯示）","source":"WDC earnings call（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0000106040/000162828026064921/wdc015705-ars.pdf","excerpt":"developed alternate sources of supply for rare earth and precious minerals, so we do not anticipate any material impact from export controls","as_of":"2026-01-01","retrieved_at":"2026-10-13","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"WDC FY2026 Q4 營收：Cloud 約 $3.3B（占 89%，YoY +43%）、Client $225M（+61%）、Consumer $187M（+38%）；管理層將 Client/Consumer 成長歸因於定價改善。FY2026 全年營收 $12.9B（+36%）。","source":"StorageNewsletter, WD fiscal 4Q26 and FY26 financial results; Nasdaq, Western Digital Q4 earnings call highlights","url":"https://www.storagenewsletter.com/2026/08/07/wd-fiscal-4q26-and-fy26-financial-results/","excerpt":null,"as_of":"2026-08-07","retrieved_at":"2026-10-13","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 Q3（截至 2026-04-03）10-Q：Cloud 成長主因為出貨 exabytes +36% 與每 EB 平均售價 +9%；Q3 Cloud 約 $3.0B（占 89%，YoY +48%）、Consumer $186M（+24%）、Client $179M（+31%）。（搜尋摘要另有來源給出不同 Q3 client/consumer 數字，未對 10-K 核實）","source":"SEC 10-Q WDC quarter ended 2026-04-03; Q3 FY2026 earnings call summary","url":"https://www.sec.gov/Archives/edgar/data/0000106040/000162828026029054/wdc-20260403.htm","excerpt":null,"as_of":"2026-04-03","retrieved_at":"2026-10-13","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"WDC 執行長稱 2026 日曆年產能大致售罄；與前五大客戶中三家簽有長約，兩家至 2027 年、一家至 2028 年。Seagate 稱其 nearline 2026 產能已全數配置。","source":"heise.de, WD and Seagate confirm: Hard drives for 2026 sold out; Seagate Q2 2026 earnings call","url":"https://heise.de/-11178917","excerpt":null,"as_of":"2026-01-30","retrieved_at":"2026-10-13","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Seagate 執行長稱隨 2027–2028 新產能上線，價格「持平至小幅上漲」是可能的（價格由供需決定）；Morgan Stanley 預測（二手轉引，未核對原報告）nearline 供給缺口今年約 300EB、2027–28 年擴大至約 400EB。","source":"Seagate Q2 2026 earnings call transcript (AOL); secondary LinkedIn post citing Morgan Stanley","url":"https://www.aol.com/finance/seagate-stx-q2-2026-earnings-143836038.html","excerpt":null,"as_of":"2026-01-30","retrieved_at":"2026-10-13","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"TrendForce 估 2026 HDD 市佔：WDC 48%、Seagate 42%、Toshiba 10%（另一 7 月估計為 WDC/STX 各逾 40%、Toshiba 約 17%，口徑不同）。德國零售通路 HDD 價格較 2025 年中上漲約 20–50%。","source":"TrendForce projection via StockHub / newsable coverage; German retail report via heise","url":"https://stockhub.kr/en/news/news_e30078befc8b","excerpt":null,"as_of":"2026-07-01","retrieved_at":"2026-10-13","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"2026-10-02 報導 Toshiba 計劃投資約 600 億日圓、於 FY2027 前將 HDD 產能倍增；當日 Seagate 股價跌約 10%、WDC 跌約 7%，市場擔憂長期壓抑價格。","source":"24/7 Wall St., Seagate Tumbles 10%, Western Digital Drops 7% as Toshiba Moves to Double Hard Disk Output","url":"https://247wallst.com/investing/2026/10/02/seagate-tumbles-10-western-digital-drops-7-as-toshiba-moves-to-double-hard-disk-output/","excerpt":null,"as_of":"2026-10-02","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","moat_trend","triggers"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"+","claim":"WDC 2026 年 HDD 供給已近售罄；公司稱 HDD 與 SSD 每 TB 價差約 5–10 倍（依搜尋摘要轉述，未讀原頁）","source":"Gigazine: Western Digital 2026 HDD capacity runs out (2026-02-16)","url":"https://gigazine.net/gsc_news/en/20260216-western-digital-2026-hdd-capacity-runs-out","excerpt":null,"as_of":"2026-02-16","retrieved_at":"2026-10-13","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Western Digital Investor Day（2026-02）：HAMR 硬碟已在兩家客戶認證中，路線圖指向約 2029 年 100TB（依搜尋摘要轉述）","source":"MarketBeat: Western Digital Investor Day HAMR roadmap, AI data center shift and new $4B buyback plan","url":"https://www.marketbeat.com/instant-alerts/western-digital-investor-day-hamr-roadmap-ai-data-center-shift-and-new-4b-buyback-plan-2026-02-04/","excerpt":null,"as_of":"2026-02-04","retrieved_at":"2026-10-13","affects":["moat_trend","triggers"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"第三方彙整 WDC FY2026 10-K 風險因子：HAMR 轉換為高風險技術轉換，含毛利壓力與可能觸發客戶合約「epidemic failure」條款的瑕疵風險（非 10-K 原文，需對照）","source":"Autobound: What Western Digital's FY2026 10-K says: 11 signals","url":"https://www.autobound.ai/companies/western-digital/10-k","excerpt":null,"as_of":"2026-08-01","retrieved_at":"2026-10-13","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 10-K：雲端占淨營收 89%（年增 38%），client 6%、consumer 5%；前十大客戶占淨營收 73%（FY2025 68%、FY2024 55%）。","source":"WDC Form 10-K FY2026 (SEC) 經搜尋摘要轉述","url":"https://www.sec.gov/Archives/edgar/data/0000106040/000162828026057139/wdc-20260703.htm","excerpt":null,"as_of":"2026-07-03","retrieved_at":"2026-10-13","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"通路誘因（經銷商／零售商價格保護與行銷補貼）占毛營收 9%（FY2026）、10%（FY2025）、11%（FY2024）。","source":"WDC Form 10-K FY2026 (SEC) 經搜尋摘要轉述","url":"https://www.sec.gov/Archives/edgar/data/0000106040/000162828026057139/wdc-20260703.htm","excerpt":null,"as_of":"2026-07-03","retrieved_at":"2026-10-13","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FQ2 2026 法說：前七大客戶以確定採購單涵蓋至 2026 曆年；前五大中兩家 LTA 涵蓋至 2027、一家至 2028，約定 EB 量與價格結構（二手轉述，未讀原文）。","source":"Futurum Group, Western Digital Q2 FY 2026 Results Beat on Cloud HDD Demand","url":"https://futurumgroup.com/insights/western-digital-q2-fy-2026-results-beat-on-cloud-hdd-demand/","excerpt":null,"as_of":"2026-02-01","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"產業文章描述 HDD 銷售由商品模式轉向以 LTA 為基礎的 build-to-order，小型買家較難取得硬碟（二手轉述）。","source":"Horizon Technology, hdd long term agreements","url":"https://horizontechnology.com/news/hdd-long-term-agreements/","excerpt":null,"as_of":"2026-02-01","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga（2026 年 9 月下旬快照）：20 位分析師共識為 Buy（16 Buy／4 Hold），平均目標價 $483；Citigroup 8/7 由 $800 降至 $740，TD Cowen 8/6 由 $500 升至 $540。","source":"Benzinga WDC price-targets","url":"https://kr.benzinga.com/quote/WDC/price-targets","excerpt":null,"as_of":"2026-09-30","retrieved_at":"2026-10-13","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布極寬：Susquehanna $500（Neutral）、UBS $560、Wells Fargo $730（7/10 由 $575 上調、Overweight）、Cantor Fitzgerald $900、Melius $1,050；TickerLeague 另顯示 4 位分析師區間 $250–$660（價格資料疑為較舊）。","source":"FN2 analyst consensus; Benzinga; TickerLeague","url":"https://fn2.ai/earnings/wdc/analysts","excerpt":null,"as_of":"2026-07-10","retrieved_at":"2026-10-13","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY26 Q4（2026-08-05 公布）營收 $3.75B（年增 44%）、EPS $3.56，優於共識 $3.27／$3.69B；FY27 Q1 指引營收 $4.1B±$0.1B、調整後 EPS 約 $4.00±$0.15，高於分析師預期（Benzinga 列共識 EPS $3.63，另列 Q1 FY27 共識 $4.03／$4.14B，兩來源口徑不一）。","source":"stock3 (德文市場報導); Benzinga earnings forecasts","url":"https://stock3.com/news/western-digital-marge-springt-auf-rekordniveau-ausblick-hebt-an-17226404","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-13","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"財報後股價下跌 5.36%，儘管數字優於預期，BingX 摘要稱因 2026 年大幅上漲後預期已被墊高。","source":"BingX: Western Digital (WDC) Q4 FY2026 Earnings Overview","url":"https://bingx.com/en/news/post/western-digital-wdc-q-fy-earnings-overview-strong-results-fail-to-impress-and-trigger-a-selloff","excerpt":null,"as_of":"2026-08-06","retrieved_at":"2026-10-13","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Seeking Alpha 修正面：截至 2026-03-27 近三個月 EPS 上修 20 次、下修 0 次；營收上修 21 次、下修 0 次。","source":"Seeking Alpha WDC earnings revisions","url":"https://seekingalpha.com/symbol/WDC/earnings/revisions","excerpt":"EPS # of Up Revisions 20 EPS # of Down Revisions 0 Revenue # of Up Revisions 21 Revenue # of Down Revisions 0","as_of":"2026-03-27","retrieved_at":"2026-10-13","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Barclays 2026-04-21 將目標價由 $325 上調至 $405，理由為 HDD 市場估計。","source":"Yahoo Finance: Barclays Raises its Price Target on Western Digital (WDC) to $405","url":"https://finance.yahoo.com/markets/stocks/articles/barclays-raises-price-target-western-163803561.html","excerpt":null,"as_of":"2026-04-21","retrieved_at":"2026-10-13","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-07-09 報導稱 Western Digital 與 Kioxia 洽談合併；未揭露交易金額，搜尋結果未見簽署最終協議的確認（OCBJ 引 WSJ 稱可能逾 200 億美元、以股票支付，來源日期不一致）。","source":"Simply Wall St 公司公告摘要／OCBJ 引 WSJ『western digital advanced talks merge kioxia wsj』","url":"https://www.ocbj.com/news/weekly-news/western-digital-advanced-talks-merge-kioxia-wsj/","excerpt":null,"as_of":"2026-07-09","retrieved_at":"2026-10-13","affects":["valuation","triggers","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Toshiba (Nikkei 報導)計畫投資約 600 億日圓（約 3.8 億美元）擴建菲律賓廠，目標在 FY2027 前把 AI／雲端 HDD 產能加倍；FY2027 指到 2028 年 3 月；Toshiba 容量市占略高於 10%，中期目標約 30%。","source":"Blocks & Files, Distant third HDD maker Toshiba spending $380 million to catch up","url":"https://www.blocksandfiles.com/disk/2026/10/06/distant-third-hdd-maker-toshiba-spending-380-million-to-catch-up/5301322","excerpt":null,"as_of":"2026-10-06","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"WDC 2026 年產能已售罄，並與兩家大客戶簽定 2027 年長約、一家簽定 2028 年長約。","source":"3DTested, Western Digital is already sold out of hard drives for all of 2026","url":"https://www.3dtested.com/pc-components/hdds/western-digital-is-already-sold-out-of-hard-drives-for-all-of-2026-chief-says-some-long-term-agreements-for-2027-and-2028-already-in-place","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261024","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Seagate 執行長表示暫不擴增產能，成長僅來自更高容量硬碟而非增加出貨顆數（搜尋摘要轉述，未讀原文）。","source":"heise, WD and Seagate confirm: Hard drives for 2026 sold out","url":"https://heise.de/-11178917","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"TrendForce 預期 Toshiba 擴產因前置時間，短期供給影響有限；Citi 認為即使 Toshiba 產能加倍，產業仍供不應求（搜尋摘要轉述）。","source":"TrendForce News / TikR","url":"https://www.tikr.com/blog/seagate-sinks-12-western-digital-down-10-as-toshiba-plans-to-double-hard-disk-output","excerpt":null,"as_of":"2026-10-06","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"WD CEO 說 2026 年 HDD 產能幾乎已售罄，並已與兩家客戶簽 2027、一家簽 2028 長約。","source":"3dtested / guru3d（WD FQ2 財報後報導）","url":"https://www.3dtested.com/pc-components/hdds/western-digital-is-already-sold-out-of-hard-drives-for-all-of-2026-chief-says-some-long-term-agreements-for-2027-and-2028-already-in-place","excerpt":null,"as_of":"2026-02-16","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"TrendForce 預期 Q3 2026 NAND 合約價季增 10–15%，漲幅放緩（買方抵抗）；6 月報告稱合約價已見歷史高位、進入高價低量盤整。","source":"IgorsLab 引 TrendForce；TrendForce NAND Flash Wafer Contract Price Jun. 2026","url":"https://www.igorslab.de/en/dram-and-nand-remain-more-expensive-trendforce-sees-slowing-but-still-rising-memory-prices-q3-2026/","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261024","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"近線 HDD 交期從數週拉長到逾 52 週；Seagate 2026 年 7 月財報稱多數近線 EB 已分配至 2028 年；Resonac 新增碟片產線 2027 起分階段上線。未找到經銷商層級通路庫存數據。","source":"Touchpoint / PC Server & Parts / Xenospectrum（搜尋摘要，二手轉述）","url":"https://www.touchpoint.com.au/resources/insights/hdd-shortage-2026","excerpt":null,"as_of":"2026-08-28","retrieved_at":"20261024","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"TrendForce 6 月 NAND 晶圓合約價報告：價格見頂、高價低量盤整","source":"TrendForce","url":"https://www.trendforce.com/research/download/RP260630KM","excerpt":"Contract prices have peaked at historic highs, severely compressing margins for downstream module makers. Coupled with weak end-market demand, buyers are strongly resisting higher quotes and adopting defensive procurement strategies. Consequently, market growth has stalled, shifting into a high-price, low-volume consolidation phase.","as_of":"2026-06-30","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"FY2Q23（2023-01 公布）營收年減 36% 至 $31.07 億，GAAP 毛利率 17.0%（前年同期 32.8%），非 GAAP 17.4%（前年 33.6%），Flash 毛利率 15%（前年 36%）；FY3Q23 指引非 GAAP 毛利率 9.0%–11.0%","source":"Zacks via Nasdaq, Why Is Western Digital (WDC) Down 12% Since Last Earnings Report?","url":"https://www.nasdaq.com/articles/why-is-western-digital-wdc-down-12-since-last-earnings-report","excerpt":null,"as_of":"2023-03-01","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"FY2023 10-K：HDD 出貨 501EB（FY2022 645EB、FY2021 541EB）；HDD 營收年減 31%，主因 exabyte 約降 26% 與 ASP 下滑，雲端客戶消化庫存","source":"WDC Form 10-K FY2023 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/106040/000010604023000024/wdc-20230630.htm","excerpt":null,"as_of":"2023-08-18","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2022-09 管理層稱 NAND 環境可能是過去 10–15 年最艱困，單週股價跌 13.8%；2022-12 Goldman 降評 Sell，預估 2023 非 GAAP 毛利率由約 28% 降至約 17%、NAND ASP 降約 38%","source":"Motley Fool 2022-09-16; Benzinga 2022-12-30","url":"https://www.benzinga.com/analyst-ratings/analyst-color/22/12/30092716/memory-suppliers-are-dumping-inventory-and-these-stocks-are-paying-the-price","excerpt":null,"as_of":"2022-12-30","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-07-09 報導稱 Western Digital 與 Kioxia 洽談合併；未揭露交易金額，未見最終協議確認。","source":"Simply Wall St 公司公告摘要／OCBJ 引 WSJ","url":"https://www.ocbj.com/news/weekly-news/western-digital-advanced-talks-merge-kioxia-wsj/","excerpt":null,"as_of":"2026-07-09","retrieved_at":"20261024","affects":["valuation","triggers","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"WDC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":48.85,"operating_margin_pct":35.6,"fcf_margin_pct":27.18,"rd_intensity_pct":8.99},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WDC","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"SNDK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.47,"operating_margin_pct":61.58,"fcf_margin_pct":56.77,"rd_intensity_pct":6.56},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"000660.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":76.27,"operating_margin_pct":68.04,"fcf_margin_pct":47.8,"rd_intensity_pct":4.93},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"005930.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.48,"operating_margin_pct":36.88,"fcf_margin_pct":28.95,"rd_intensity_pct":9.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"PSTG","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PSTG"},"note":"quarterly_income_stmt 無資料"}],"subject":"WDC"},"financial_history":{"ticker":"WDC","currency":null,"method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":6255000000.0,"revenue_yoy_pct":null,"gross_margin_pct":22.24,"operating_margin_pct":-6.43,"net_income":-1684000000.0,"diluted_eps":-5.44,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":6317000000.0,"revenue_yoy_pct":0.99,"gross_margin_pct":28.07,"operating_margin_pct":1.54,"net_income":-798000000.0,"diluted_eps":-1.72,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":9520000000.0,"revenue_yoy_pct":50.7,"gross_margin_pct":38.78,"operating_margin_pct":22.37,"net_income":1861000000.0,"diluted_eps":5.139276,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":12919000000.0,"revenue_yoy_pct":35.7,"gross_margin_pct":48.85,"operating_margin_pct":35.6,"net_income":9298000000.0,"diluted_eps":26.92,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDC/WDC_Q1_2027_Earnings_Call_20261022.md）

# Q1 2027 Earnings Call
**Western Digital Corporation** | Earnings Calls | 2026-10-22

**Operator** (Operator):
Good afternoon, and thank you for standing by. Welcome to Western Digital's First Quarter Fiscal 2027 Conference Call. [Operator Instructions] As a reminder, this call is being recorded. 
Now I would like to turn the call over to Mr. Ambrish Srivastava, Vice President, Investor Relations. You may begin.

**Ambrish Srivastava** (Executives):
Thank you, and good afternoon, everyone. Joining me today are Irving Tan, WD's Chief Executive Officer, and Kris Sennesael, WD's Chief Financial Officer. 
Before we begin, please note that today's discussion will contain forward-looking statements based on management's current assumptions and expectations, which are subject to various risks and uncertainties. 
These forward-looking statements include expectations for our product portfolio, business plans and performance, ongoing market trends and future financial results. We assume no obligation to update these statements. Please refer to our most recent annual report on Form 10-K and other filings with the SEC for more information on the risks and uncertainties that could cause actual results to differ materially from expectations. Unless stated otherwise, today's remarks reflect non-GAAP results. Reconciliations to GAAP results are available in our press release and at investor.wdc.com. 
With that, I will now turn the call over to Irving.

**Tiang Yew Tan** (Executives):
Thanks, Ambrish. Good afternoon, everyone, and thank you for joining us today. Q1 marked a strong start to fiscal 2027, reflecting solid execution across the business and results ahead of our expectations. Revenue grew 55% year-over-year, while gross and operating margins expanded meaningfully to 58% and 49%, respectively. EPS grew 161% year-over-year, and we generated $1.4 billion in free cash flow. 
These results reflect ongoing robust customer demand, operational discipline and successful execution of our product and technology road map. Demand remains strong across our customer base and end markets. Our visibility is extending further and with it our conviction in the durability of demand for data storage on HDDs. 
We are increasingly seeing storage demand grow beyond our core cloud and hyperscale customers into enterprise environments and into newer end markets, such as neoclouds and AI frontier labs, resulting in a larger and more diversified customer base. Our customers are making longer-term infrastructure investments and continue to extend their planning horizons into the next decade. 
As the value of data is increasing, we are investing with confidence to support their growing needs for data storage, with the vast majority of the data being stored on HDDs. We see this firsthand in our customer conversations and in broader industry research. A recent IDC survey of more than 750 companies across several countries found that organizations are storing more data, retaining it for longer periods and increasingly putting archived data back to work. 
At the core of these trends is continued data growth, fueled by the ongoing expansion of cloud environments and the increasing storage demands from AI. While much of the conversation around AI focuses on compute, we believe the more enduring opportunity is in data. AI is fundamentally a data system. Every workload creates more data, and that data must be stored, managed and accessed in a scalable and economical manner. 
As AI adoption continues to expand across industries worldwide, data creation and storage requirements are expanding with it. Inference and agentic AI systems are generating significant volumes of logs, model outputs and system performance data that must be stored and retained. Physical AI applications such as robotics, factory automation and autonomous vehicles are further accelerating this trend with AI-generated content and video workloads that are creating and retaining data at scale. 
Let me now turn to our industry-leading technology and innovative products. We are executing well against our technology road map and remain on track transitioning our customers to higher capacity drives. As we ramp production across our next-generation ePMR and HAMR platforms, we expect our exabyte shipments to continue to increase through fiscal 2027 and beyond. 
Volume production of our latest ePMR platform, delivering up to 40 terabytes of capacity, is off to a strong start. Customer adoption is progressing ahead of prior transitions, and we expect this platform to represent close to 30% of our nearline shipments by the second quarter and 50% by the third quarter of fiscal 2027. 
On our first-generation HAMR product, we are on track to finish qualifications with 2 hyperscale customers in the first quarter of calendar year 2027 and are on schedule to begin volume shipments in the first half of calendar year 2027. We also expect to begin qualifications with 2 additional customers during the first half of calendar year 2027, further expanding customer validation and supporting broader adoption of our HAMR products. 
As AI workloads scale, customers not only need more capacity, but also greater performance from their storage infrastructure. We are expanding the role of HDDs within cloud and AI infrastructure through innovations such as our high-bandwidth drive and dual pivot technology. 
By combining the economics of HDDs with significantly higher levels of performance, we believe this technology can address a broader range of existing and emerging workloads. We are currently sampling our high-bandwidth drives with multiple customers, and the feedback has been positive with clear use cases and value creation identified. 
In summary, WD is executing with momentum. We are deepening customer relationships, extending visibility and broadening the customer base, while our product and technology road map delivers precisely what customers need. As data grows in volume and value across cloud, AI and emerging workloads, we have high confidence in the durability of long-term storage demand. 
With that, let me turn it over to Kris.

**Kris Sennesael** (Executives):
Thank you, Irving. Our first quarter results demonstrate ongoing strength of our business in combination with outstanding execution on all fronts. Customer demand remains healthy, and our visibility is extending further out. Our product transitions are progressing well, resulting in higher capacity products, solid year-over-year growth in exabytes shipped and improved pricing, all driving another quarter of strong financial performance. 
During the first quarter of fiscal year 2027, revenue was $4.4 billion, up 55% year-over-year, driven by strong exabyte growth and a favorable pricing environment. We delivered 248 exabytes in the quarter, up 22% year-over-year and up 8% sequentially. Nearline products continue to drive growth as we execute on our product transitions, starting with the ramp of our latest generation ePMR drives with capacities up to 40 terabytes and followed by the introduction of our HAMR technology in the first half of calendar year 2027, setting us up for stronger year-over-year growth in exabyte shipments. 
Cloud revenue was $3.9 billion, representing 88% of total revenue and increasing 54% year-over-year, driven by durable demand for our high-capacity nearline HDDs, including the initial ramp of our latest ePMR platform. In addition, continued pricing strength reflects the value and TCO advantages we deliver to our customers. Client represented 7% of total revenue at $320 million, up 119% year-over-year. Consumer represented 5% of revenue at $193 million, up 19% year-over-year. 
Gross margin expanded to 58.1%, up 1,420 basis points year-over-year, with incremental year-over-year gross margin above 80%. Gross margin reflects a mix shift towards higher capacity drives, disciplined operational execution and a favorable pricing environment across our portfolio as we continue to deliver greater value to our customers. Year-over-year growth in average price per terabyte further increased to 28% versus the high teens we reported in the prior quarter. 
Operating expenses were $391 million or approximately 9% of revenue, a 130 basis point sequential improvement, demonstrating continuing operating leverage in the model. Operating income of $2.2 billion increased 152% year-over-year, driven by strong revenue growth, expanding gross margin and operating leverage. Operating margin expanded to 49.1% in the quarter, demonstrating our ability to continue to drive sustainably higher levels of profitability in the business. 
Interest and other expenses were $10 million, and our effective tax rate was 17%. Taking into account a diluted share count of 383 million shares, EPS was $4.64, an increase of 161% year-over-year. We generated $1.4 billion in free cash flow during the quarter and returned $1.1 billion to shareholders through share repurchases and dividends, reflecting confidence in the durability of free cash flow generation and our ability to drive long-term shareholder value. 
Supported by the strength of the free cash flow generation and consistent with our capital allocation framework, the Board has approved a 17% increase in the quarterly cash dividend from $0.15 per share to $0.175 per share, which will be paid on December 17, 2026, to shareholders of record on December 4, 2026. 
Turning to the balance sheet. During the quarter, we took additional steps to simplify our capital structure by substantially reducing our remaining 2028 convertible notes. Our balance sheet remains strong, and we ended the quarter with a net cash position of $0.5 billion. 
Let me now turn to the outlook for the second quarter of fiscal 2027. We continue to operate in an environment of strong demand and favorable pricing in all our end markets. For the second quarter of fiscal 2027, we expect revenue to be $5.1 billion, plus/minus $100 million. At the midpoint, this reflects a 69% increase year-over-year. Gross margin is expected to be in the range of 60% to 61% as we continue to benefit from the shift to higher capacity drives along with a strong pricing environment. 
We anticipate operating expenses of $400 million to $410 million, a sequential increase driven by the project expenses related to increased product qualification activities. Interest and other expenses are expected to be $15 million. The tax rate is expected to be 17%. As a result, we expect diluted earnings per share to be $5.80 plus/minus $0.20 based on a non-GAAP diluted share count of 380 million shares. 
As we look ahead, demand remains robust. Customer engagements continue to deepen and broaden, and our visibility continues to improve. And as we execute on our technology and product transitions, we expect to accelerate exabyte supply growth throughout fiscal year 2027 and 2028. Our strong balance sheet and free cash flow generation give us the ability to make targeted investments that strengthen our technology leadership and support our customers' growing storage needs. 
While we expect capital expenditures to average 4% to 6% of revenue over a 5-year period, we anticipate that CapEx as a percentage of revenue will be modestly above that range over the next 2 years as we continue to invest in heads and media technology and factory automation, supporting our industry-leading areal density and higher capacity drives without having to spend CapEx to add unit capacity. 
In summary, accelerating exabyte growth, technology leadership, expanding margins and disciplined capital allocation provide a solid foundation for sustainable earnings, free cash flow growth and long-term shareholder value creation. 
With that, let's now begin the Q&A. Ambrish?

**Ambrish Srivastava** (Executives):
Thank you, Kris. Operator, you can now open the line to questions, please. [Operator Instructions] Operator?

**Operator** (Operator):
[Operator Instructions] Our first question today comes from Amit Daryanani from Evercore.

**Amit Daryanani** (Analysts):
I guess maybe to start with, Irving, there's always a lot of focus on HAMR, and you outlined sort of completing qualification of the 2 hyperscalers in March, volume shipments mid-'27. Can you just talk about what are the remaining milestones between those 2 steps from your perspective? And then what determines how quickly you scale from there? Is it more driven by customer deployment schedules or your manufacturing readiness? Just any help there.

**Tiang Yew Tan** (Executives):
Yes. Amit, thanks for the question. First of all, I would say I'm very pleased with the progress that we're making with HAMR. As we've highlighted in the past, feedback from our customers have been very positive, particularly around the failure rates that we've seen in our drive performance vis-a-vis what they've seen with other players within the market. As a result of that, we are very confident in terms of finishing qualifications with the 2 customers that we have for our first-generation HAMR products in Q1. 
We will be starting qualification with 2 additional customers in the first half of calendar '27 as well. We haven't had any feedback that would give us any reason for pause in terms of us translating that qual completion to volume shipments starting first half '27. Both our customer technical support teams are working very closely with customers to complete those qual schedules and get them into production. Across our global operations teams, we are working closely with our own internal manufacturing assets and vendors to get the supply chain ready to support the ramp as well. 
And then starting in the second half of calendar year '27, we will also start qualification of our second-generation HAMR drives, and this will be at 5 terabytes per platter on an 11-disk platform. So overall, very pleased with the progress. I think the engineering and operations teams across the company have done a great job in really helping us accelerate development of the products, the reliability of it, and then we're focused very much on scaling it up and getting it into customers' hands.

**Ambrish Srivastava** (Executives):
Do you have a follow-up, Amit?

**Amit Daryanani** (Analysts):
I do. Maybe just to follow up on the cost per terabyte. I realize you folks in the past have talked about some of this input cost inflation headwind. But I think cost per terabyte was down like 4%, 5% in September quarter. That's the lowest we've seen in a while. Maybe you can just touch on what's happening there and what's the right way to think about this longer term because I do realize you're guiding for some really strong gross margins in December. So just a little bit on the cost per terabyte number would be helpful.

**Kris Sennesael** (Executives):
Yes. So as Irving just indicated, we continue to execute well on our technology road map and product transitions, basically moving to higher capacity drives based on better and higher areal density. And so we are well on track in the long run to reduce our cost per terabyte approximately 10% year-over-year. 
In the near term, and I've indicated this before, this is not a surprise. We are facing some input cost increases. As most of you know, we use some DRAM and some NAND inside our hard disk drives. And the whole supply chain really operates in a very tight environment. And so we are seeing some of those input cost increases. We are addressing all of them through value engineering initiatives that we are seeing some good traction. It takes a little bit of time to implement and qualify those solutions. 
And so, in the near term, our cost per terabyte will be less than 10% down year-over-year. Taking that all into account, as you indicated as well, we are delivering very strong gross margins in the September quarter as well as a strong guide for the December quarter. Our incremental gross margins continue to be very strong, well above 80%. And so I think we're very well set up to continue to increase our gross margins over time.

**Operator** (Operator):
Our next question comes from Wamsi Mohan from Bank of America.

**Wamsi Mohan** (Analysts):
Irving, I was wondering if you could just address this angst around incremental capacity adds from the smallest player in the market, and there's been some chatter around potential consolidation in the industry. Just would love to get your high-level take on what do you think could be if there is any potential impact from that at an industry level? And is that impacting any of your price negotiations with hyperscale customers in the out years?

**Tiang Yew Tan** (Executives):
Yes. Wamsi, thanks for the question. I would say at a high level, we don't see any change in terms of the long-term fundamentals of both the industry or our business specifically, right? We continue to see demand continuing to be very strong, 25% plus CAGR as we've highlighted consistently in a very tight supply environment. And we remain committed to our strategy and our focus to meet that supply-demand growth based on delivering areal density, and that's delivered through technology, particularly through our head and media technology because that is the best way to deliver the best TCO to our customers and to also drive greatest profitability of our business -- for our business as well. And that's -- you can see that focus in terms of the investments we're making both into research and development and into capital investment into our head and media parts of the business. 
And I think the unique differentiation that we have with our own head and media development, the drive integration capability that we have gives us that confidence to be able to meet that growth trajectory through areal density and therefore, remain committed to not investing in any incremental unit capacity. There may be some other players in the market who don't have that unique ability to build their own media, build their own heads, drive that areal density improvement. And they have to compensate that by potentially maybe increasing the number of units just to maintain their share and position in the marketplace.

**Ambrish Srivastava** (Executives):
Do you have a follow-up, Wamsi?

**Wamsi Mohan** (Analysts):
Yes, Ambrish. So on the exabyte shipments, you grew 22%. And as I'm hearing you talk about sort of the trajectory here for the rest of the year, it looks like you expect that growth to improve as you execute on these product transitions and then have HAMR in the mix. Could you just give us some sense of what it is at the high level? Like, is it right to think of fiscal '27 at roughly your longer-term range for the year? Is that the right way to think about it? And maybe just if you think about unconstrained sort of demand, like how much higher is that relative to where your supply is? And do you see that widening because of just how strong the demand is over the next couple of years?

**Tiang Yew Tan** (Executives):
Yes. Thanks for the question, Wamsi. We sort of see the current quarter as being sort of the floor in terms of exabyte growth, and we see that accelerating through the rest of the fiscal year. And obviously, as Kris highlighted in the script to '28 and beyond that as well, that's really driven by the confidence that we have in the new platforms that we'll be introducing. Obviously, we have HAMR coming out in the first half of fiscal '27. And then as I highlighted, we have our second-generation HAMR drive starting qualification in the second half as well. 
So we are very quickly at the top end going from a 32-terabyte drive to 44-terabyte drive to a 55-terabyte drive and beyond. And that's the best way and the most economical way for both our customers and for us to be able to meet the demands that they have in terms of our products. 
To your question around the demand, as I said, we see that continuing to grow. We see it being very doable. There hasn't been any diminishing in demand, and we don't see the gap in supply or demand that exists today perishable in the near term as well. So we continue to focus on supporting our customers the best we can with the technology that we have.

**Operator** (Operator):
Our next question comes from Erik Woodring from Morgan Stanley.

**Erik Woodring** (Analysts):
Congrats on the quarter and the guide. Irving, can you maybe just share a bit more granular detail on your visibility comments, meaning how far out are we talking? How many customers are we talking? And for those customers that are planning that far out, just what are their exabyte needs today or in the future relative to 3 or 6 months ago? Do you see that demand kind of expanding relative to, again, 3 or 6 months ago?

**Tiang Yew Tan** (Executives):
Yes. Erik, thanks for the question. I think in terms of visibility outlook, if you take our top 7 customers as an example, we have good visibility up to 2030, 2031 for across all 7 of them, and that's something that we've highlighted that we've always really much appreciated so we can make sure we both deliver both the technology and the supply to meet that growth in demand going forward. And so we have good visibility in that. In fact, we see quarter after quarter, the demand signal actually increasing over time. And as we move forward into the '28, '29, '30 time frame, we see that demand continuing to be very durable.

**Ambrish Srivastava** (Executives):
Do you have a follow-up, Erik?

**Erik Woodring** (Analysts):
Yes. And then just as a follow-up, you obviously just grew revenue 55% year-over-year. You're guiding to 69% year-over-year revenue growth at the midpoint in December, incredibly strong. And obviously, you're referencing some exabyte growth acceleration, but that also implies that you're going to be accelerating pricing in the December quarter as well. So can you maybe just help us understand what is the source of that pricing acceleration? Is that coming from the non-nearline side? Is that the nearline side? I assume it's probably both. But just any more granular color you can provide on why we're seeing that acceleration in pricing in the December quarter and how sustainable that is?

**Kris Sennesael** (Executives):
Yes. Erik, we continue to operate in a very strong, favorable pricing environment. You saw our blended average selling price per terabyte was up 28% on a year-over-year basis. And we saw that strength across the board in nearline and non-nearline, some of our consumer and client businesses as well. The pricing environment is strong because we do execute on our technology and product road map, and we continue to deliver higher capacity drives to our customers that help our customers to reduce their total cost of ownership because you have better rack density, lower power consumption and a lot of benefits for our customers. 
As we continue to execute on that strategy and continue to deliver higher capacity drives, there is an opportunity to further enhance our price per terabyte over time. As you probably know, some of that business is under LTAs. Some of the LTAs are expiring and new agreements are being put on place. And in addition to that, of course, some of our exabytes are not under contract as well, and we do see a very strong price environment for those exabytes that are not under contract as well.

**Operator** (Operator):
Our next question comes from C.J. Muse from Cantor Fitzgerald.

**Christopher Muse** (Analysts):
I guess, Irving, you started the conversation talking about results ahead of expectations. And just to follow up on the last question. For gross margins, you initially guided kind of incremental 62% and you reported 80% and now guiding 75%. So really trying to drill down as to what is driving that incremental strength. Is it more bits that are not under contract? Is it contracts that are unwinding and repricing? And I guess, as we think beyond the near term, how should we think about the sustainability in '27 and beyond?

**Tiang Yew Tan** (Executives):
Yes. I think at a high level, C.J., first of all, we think the sustainability of gross margin expansion is absolutely there. There are 3 drivers of that. Obviously, pricing, as Kris highlighted, we have a bunch of LTAs that have contractual price increases as we move into different periods as they reach sort of their anniversary, their price adjustments as we deliver higher capacity platforms, they get better TCO values. So we're able to share in that and drive higher pricing for those contracts that we have -- customers we have LTAs with. 
We have also been able to get better spot pricing with nearline customers who aren't on LTAs given the tight supply environment. And as Kris also highlighted, across the board, we are seeing better pricing environment in our client and consumer segments of the business as well. So pricing is one key element. Second, we've also been upmixing our customers to higher capacity drives. So as we move them up to higher capacity drives, obviously, these are more profitable for us because the ASPs per drive are much higher as well. So that's the second driver of gross margin expansion that we expect to remain over a longer-term time period as well. 
And third, obviously, we'll be shipping more exabytes, right, through higher areal density. And so we are able to deliver more exabytes through areal density, you avoid the fixed cost of having to produce more units, and that's another driver of gross margin expansion. So you put the combination of those 3 factors together, we feel very optimistic about ongoing gross margin expansion.

**Ambrish Srivastava** (Executives):
Do you have a follow-up, C.J.?

**Christopher Muse** (Analysts):
I do Ambrish. You talked about a broadening breadth of customers, including enterprise and MCPs. I'm curious how is that perhaps changing the duration of LTAs pricing and deposits perhaps? Just would love to hear how your customer base is evolving and how that might impact kind of your contracts?

**Tiang Yew Tan** (Executives):
Yes. So we definitely see, I would say, a diversification of our customer base, right? And it's something that we've communicated in the past where the sort of 3-tier architecture and the critical role that HDDs play, both in terms of the scalability, reliability and the economic value that it provides to customers is truly playing out, right? And we definitely see that demand happening from the frontier AI labs, from the neocloud players and also hybrid cloud solution OEM providers as well. 
So we're factoring in the demand signal as well as we look forward and that's translating into the expanding demand signal that we've highlighted in my response to the earlier questions. And again, we're delivering -- we're building technology. We're making investments into head and media to be able to provide the areal density and the capacity to support all our customers in this more diversified customer environment.

**Operator** (Operator):
Our next question comes from Asiya Merchant from Citigroup.

**Asiya Merchant** (Analysts):
Great. Irving, I think you talked about some of the high-bandwidth drives as well and opportunity there to grow. Maybe if you could just double-click on how big is that opportunity today? How many of these are you shipping if you can elaborate on that? And how big do you think that opportunity could be for you?

**Tiang Yew Tan** (Executives):
Yes. Thanks for the question, Asiya. Look, I think the opportunity is still somewhat nascent. Today, our primary focus is obviously to get capacity into the hands of the customers. But as we move into latter part of calendar year '27, '28 and beyond, this becomes what we feel a big differentiator for us because things like high-bandwidth drives provide customers with an opportunity to use HDDs for different workloads that they may have to use alternative storage media for, which will be much more costly. 
For example, KV cache workloads in AI inferencing and in video streaming as well. So we've been actually providing samples to many of our customers in terms of this product so that they can test out different use cases. And I highlighted that's been very positively received. And so we are working through sort of the commercial structure of how we would price those high-bandwidth capabilities to customers. But from a technical capability standpoint, very positive. We are working through sort of the commercial construct of how we would price that going forward.

**Ambrish Srivastava** (Executives):
Did you have a follow-up, Asiya? Yes, go ahead.

**Asiya Merchant** (Analysts):
Yes, sure. If I can just ask about the physical AI as well. I think you talked about that as well in your script. Any early indications again of how big is that opportunity today? Are you shipping towards that? Probably still in the early innings now, but how do you think about it through calendar '27 and into calendar '28?

**Tiang Yew Tan** (Executives):
Yes. I think we're definitely seeing very promising signs from the physical AI segment of the markets. For example, some of our customers in Asia who are in the autonomous vehicle space are definitely looking for increased demand supply from us to be able to support their physical AI initiatives. A good data point of that is NVIDIA themselves have just recently highlighted the opportunity in terms of their revenue from physical AI being in the $10 billion range, right?
So if you see that happening in compute, there's obviously the demand for storage to support that compute as well. So we see it very positively. Obviously, autonomous vehicles will be one. Robotics is also becoming a key area for us. A lot of it actually is happening out in Asia, but I anticipate that will happen throughout the rest of the world over the next 2 to 3 years as well.

**Operator** (Operator):
Our next question comes from Ben Reitzes from Melius Research.

**Benjamin Reitzes** (Analysts):
I wanted to go back to one of the earlier questions on the competitive aspect of adding capacity. I think there's just some basics that would be helpful. How -- can somebody go from 10% to 30% capacity share? Is there enough materials to do media and heads to be able to do something like that? Maybe you can address the question from that. And what would be the -- is your view, that somebody could do that? And what would be the bottlenecks in doing so?

**Tiang Yew Tan** (Executives):
Yes. Ben, thanks for the question. I can't comment about somebody else doing it. I can share what we are doing to enable it. So first and foremost, it all starts with technology. Our R&D teams do a great job in terms of designing, head designs, media recipes to really enable high areal density products. Obviously, we combine that with our firmware capabilities and drive servo mechanics capability. So it's not only about the individual components, but when you integrate all of it together, do you get the optimum areal density per drive? So that's really at the engineering level, and that's one of the big differentiators that we feel versus maybe one other player in the market who is dependent on third-party suppliers. So they're not vertically integrated. 
Secondly, as you've touched on, a key element of it is not so much the unit capacity that you have. It's the availability to produce, at scale, the needed media and heads to support the higher areal density in the drives as well. And again, that's something we have been and we will continue to make investments in WD, both in terms of our R&D capability, but also in terms of our manufacturing assets, specifically to enable greater areal density to our head and media assets to drive that. 
So I think that's what we're doing, and we see the results of that. Other organizations that don't have that degree of vertical integration, I would say, will have a harder time being able to reach the same levels of growth that we are seeing.

**Benjamin Reitzes** (Analysts):
There's obviously a lot of fear out there as you guys see and well know going into this call. I was just wondering if you could give more color around how big neoclouds are for you now and in your forecast. And if there was a hiccup in demand there just due to timing of capital, how we would see it and how big a concern would that be for you?

**Tiang Yew Tan** (Executives):
Yes. I think, first of all, we need to take a step back. There are really 4 drivers of growth within the storage space, right? One is the ongoing secular growth of the cloud. And the cloud itself has been around for close to 2 decades and is still growing at a very healthy pace. In fact, accelerating really driven by a lot more storage being driven by video content. So a lot more demand because of a lot of content being stored is video and obviously, a lot of the cloud-based services are becoming AI-enabled. So that's driving greater storage requirements. So that's one key driver of growth that will continue over the foreseeable future. 
The second driver of growth has been model training and development, and we see that continuing to grow as new models get created as reinforcement learning is happening, more data needs to be stored to support reinforcement learning of existing models as well, and that's where the neoclouds do play a part in. But we don't see that being, in any way, a major hiccup if there is a bit of a slowdown in the neocloud segment. 
The third is around inferencing and agentic AI, and that's where we see a lot of opportunity going forward, and we're starting to see a tremendous amount of growth coming from that area as customers need to store logs, checkpoints, more outputs of that inferencing and sort of the agentic system decision points to support reinforcement learning as well. And then finally, physical AI that we've just touched on as well. 
So if you add those 4 things together, I think the demand remains very durable. Even if there may be a slight softness in 1 of the 4 segments, the demand will be easily picked up by any one of the other 3. So all things added together, we see a very positive outlook in terms of the demand remaining strong and remaining durable.
In terms of how we look at the neocloud segment, obviously, we are very diligent in looking at the strategic neoclouds that we want to engage with, those that we think have a very strong balance sheet, have underpinned by a very good end customer base as well. So we prioritize that over other players within the market.

**Operator** (Operator):
Our next question comes from Tom O'Malley from Barclays.

**Thomas O'Malley** (Analysts):
So if I look at kind of the CAGR of total HDD exabyte shipments over the last couple of quarters range from low 20s kind of up to the mid-30s. And I plug that in for your guide, it looks like your year-over-year pricing that's implied for the December quarter is above that 30% year-over-year mark. 
So you guys have historically kind of said high teens is the sustainable growth rate. You are now well above that for the past couple of quarters. Do you think you could give us an update about what the right way to look at that is in terms of sustainability of that pricing increases on a go-forward basis?

**Kris Sennesael** (Executives):
Yes. Tom, I think the 10% or whatever number you were referencing, we're operating well above that, right? Just in the 1 quarter ago, we were already at 18% ASP increase on an ASP per terabyte basis. And so last quarter, we did 28%. And as I indicated before, given the strong demand environment that we operate in, given the fact that we continue to move to higher capacity drives and continue to add more value to our customers, there is definitely further room for ASP per terabyte increases going forward over the next, call it, 3, 4 quarters. 
I would assume eventually that is going to slow down a little bit. But for the next 3, 4 quarters, there's definitely further room to expand our ASP per terabyte year-over-year growth.

**Operator** (Operator):
You have a follow-up, Tom?

**Thomas O'Malley** (Analysts):
Just following up on the commentary, just the CapEx on average, 4% to 6% of revs over a 5-year period, but modestly ahead of that in the next 2 years. I think like the knee-jerk reaction to that is making sure that, that is just investing in heads, and this is not something about expanding capacity or feeling like you need to take advantage of a market as it's nearing a potential peak, not saying that, just outlining what you could here. 
So maybe could you spend a little bit of time talking to us about why the investment is needed in heads? Is this around diversification efforts because of what we've heard in the media lately, or just a desire to get your internal efforts to a better spot? I would love just to hear your kind of thoughts on that.

**Kris Sennesael** (Executives):
Yes. And Tom, just to be clear, in the prepared remarks, we explicitly said that the CapEx is going to head and media and factory automation and not to expanding our unit capacity.

**Tiang Yew Tan** (Executives):
Yes. So I think Kris summarized it really well. And obviously, as we look to transition to HAMR, obviously, there are longer cycle times in terms of the steps that are involved, in terms of the heads that we need, head wafers that we need to produce, and also the media products that we need to produce.
 
So we're making the appropriate investments to support both the technology capabilities and at the same time, to recognize that there are slightly longer cycle times because there are slightly more steps that are involved to produce the head and media components that's needed for HAMR.

**Operator** (Operator):
Our next question comes from Timothy Arcuri from UBS.

**Timothy Arcuri** (Analysts):
You guys talked about an acceleration in exabyte growth. You've been undershipping your peer by about 10 points there. You're sort of mid-20s and they're sort of mid-30s. So Kris, when you mentioned that, like what is the target? Should we think that maybe over a multitude of quarters, you could get to like the mid-30s is the goal to sort of close that gap?

**Kris Sennesael** (Executives):
So yes, we did 22% last quarter, and we've talked about that. We are in between 2 product transitions. We -- the last couple of quarters, we executed really well on our up to 32 terabyte ePMR transition. We are now started to execute on our up to 44 terabyte ePMR transition.
And then we have our HAMR transitions first and second generation coming up, and that is going to drive a meaningful increase in our areal density and a meaningful increase to higher capacity drives, and that will definitely accelerate our exabyte year-over-year supply growth over the next 6, 7, 8 quarters.

**Operator** (Operator):
Do you have a follow-up, Tim?

**Timothy Arcuri** (Analysts):
I do, I do. Yes. So just to kind of double-click on that. So Kris, should we think of you in 6 quarters shipping like 35% exabyte growth? Is that the message?

**Kris Sennesael** (Executives):
So we're only guiding one quarter at a time, but you're thinking about it in the right direction.

**Operator** (Operator):
Our next question comes from Krish Sankar from TD Cowen.

**Sreekrishnan Sankarnarayanan** (Analysts):
I have two of them, too. And Kris, thanks for the color on the pricing. I'm just curious, as your first set of HAMR customers ramp in the first half, would there be any impact on the ASP growth mainly because you're helping your early customers ramp HAMR or should not have any impact?

**Tiang Yew Tan** (Executives):
No, we're not discounting our HAMR products in any way versus our ePMR products. So we price them on a dollar per terabyte basis, and we have LTAs that we -- that I mentioned that have appropriate price reviews periodically. And so whether we ship a HAMR bit or ePMR bit, the price is the price.

**Sreekrishnan Sankarnarayanan** (Analysts):
Got it. Got it. And then as a quick follow-up, I totally understand your argument about adding head capacity but not units. I'm just trying to play the devil's advocate, by adding head capacity, you are increasing the capacity per unit. So I'm just wondering, isn't that lead to the fact that you are actually adding capacity, even though if it's head, not unit, leading to more capacity increase versus the minutia between a unit or a head?

**Tiang Yew Tan** (Executives):
Yes. I think there are 2 factors there. First of all, we said we are investing into head capacity. And part of it is, as I mentioned, for example, a HAMR head does require more cycles to produce. So there's a bit of throughput loss, so we need to offset. So we do need to put in more capacity. So that does not translate into more heads and therefore, more units. 
And we have also indicated at our Innovation Day back in February of this year, we have a road map to deliver drives with up to 14 platters as well. And therefore, you will need more heads within the existing number of drives that we have as well. So we're making the investments to support that road map going forward as well.

**Ambrish Srivastava** (Executives):
And Krish, last quarter, we shared with you the platter count growth on very minimal unit growth, right? So that's one of the reasons we have to invest on the head side.

**Tiang Yew Tan** (Executives):
And that applies to media as well, same thing.

**Operator** (Operator):
Our next question comes from James Schneider from Goldman Sachs.

**James Schneider** (Analysts):
I was wondering if you can maybe just clarify with respect to your head strategy currently, whether you use external vendors for any of your products or for surge capacity? And to what extent the head investments beyond just the HAMR items you mentioned before are meant to sort of eliminate the need for any potential vendors in the future and sort of take that external off the table completely?

**Tiang Yew Tan** (Executives):
Thanks for the question. So we do use some external head capacity that we always have done. We do that for media as well. That is part of our sort of innovation approach where we build and buy. So we're able to benchmark our performance of our components with our -- the third-party suppliers as well as a great way for us to continue to drive innovation both internally and with our partners as well.
Our focus on our investment is to continue to ensure that we have the latest technology internally to support our products going forward. What we do buy from third parties are typically used in our lower capacity drives. So all the high-cap leading-edge platforms that we introduce are all on our own internal heads.

**Operator** (Operator):
Do you have a follow-up, Jim?

**James Schneider** (Analysts):
Yes. Just as a follow-up, in a hypothetical situation where one of your competitors were to meaningfully expand unit capacity, what, hypothetically, would be your response in that case?

**Tiang Yew Tan** (Executives):
Well, again, you can -- it boils down to not just unit capacity, but at what capacity point is unit shipping as well. So again, our focus is on delivering that capacity that customers need through higher capacity drive through areal density. So our response is going to be the same as we've communicated over the last year, to continue to focus on the areal density, translate that into the highest capacity drives that we can bring into the market. That's the best TCO for our customers and drives the best economics for us as well.

**Operator** (Operator):
Our next question comes from Karl Ackerman from BNP Paribas.

**Karl Ackerman** (Analysts):
Irving and Kris, you indicated that HAMR will ramp over the next couple of quarters. But do you expect non-HAMR nearline drive capacity to also expand while HAMR ramps as well?

**Tiang Yew Tan** (Executives):
So we expect -- obviously, we are looking to ramp HAMR in the first half of calendar year '27. In parallel, we will also continue to ramp and supply our latest ePMR platform. As we highlighted, it's making a very successful transition. In fact, the fastest transition of any ePMR platform that we've seen. In this quarter, Q2, we expect 30% of all the nearline bits to be on that 40 -- up to 40 terabyte platform.
 
By Q3 of calendar year -- fiscal '27, we expect 50% of all the nearline bits that we ship will be on that 40-terabyte platform as well. And then obviously, we'll continue to scale. So I think we have 2 very strong horses in the mix to deliver high cap drives to support the demand that our customers need.

**Operator** (Operator):
Our next question comes from Mark Newman from Bernstein.

**Mark Newman** (Analysts):
Congrats on numbers today. I wonder if I could just ask a bit more on the pricing. Pricing continues to be extremely strong, and this last quarter seems to be further accelerating. You talked about demand visibility all the way through 2030, 2031. I wonder if you could update us on how far out you have for price visibility such as in your purchase orders already signed or long-term agreements. 
How far out should we expect this price to remain continuing at this cadence? Or potentially, could we expect it to further accelerate from here? Any comments on price visibility from here would be great.

**Kris Sennesael** (Executives):
Yes. So the most important thing with LTAs and our customer engagements is to create that long-term visibility and making sure we are aligned from a technology and product road map. We're aligned on those product transitions that are being planned ahead for the next couple of quarters and years and making sure that we put in place the necessary exabyte capacity to support the demand. That's the most important thing that we're trying to achieve here. 
In terms of pricing, in those LTAs, we do have some pricing components. Keep in mind that there is base volume, there is upside volume. So there is definitely some flexibility. And keep in mind, of course, that not all our exabytes are covered by the LTAs. The further you go out, the less of it is covered under LTAs and for sure, under pricing component of the LTAs. 
So we think in the current environment, that's the best way to approach it. And again, as we -- for us, it's all about execution on our technology product road map, get to the higher capacity drives, deliver more value to our customers, and that's a very favorable setup for pricing and further increases in our ASP per terabyte.

**Mark Newman** (Analysts):
Can I ask one quick follow-up on the exabyte growth, 22% year-on-year? I believe you guided long-term exabyte growth for nearline at 25%. I just wanted to clarify if that is still intact, which also your competitor had also outlined. Is that 25% a good guidance long term for nearline exabyte growth?

**Kris Sennesael** (Executives):
Yes. We actually said greater than 25%, right? And again, we've indicated that currently, it's slightly below the 25% because we are in between those 2 product transitions. But as the product transitions are getting more traction, we will exceed that 25%.

**Operator** (Operator):
And at this time, we'll conclude today's question-and-answer session. I would like to turn the floor back over to Irving Tan for closing remarks.

**Tiang Yew Tan** (Executives):
Thank you, operator. I would like to leave all of you with a few thoughts. The first phase of AI investment focused on building the infrastructure to train models. Even as that continues, the next phases are about deploying AI to work at scale from inference to agents to physical AI. As that happens, data will continue to compound, driving customers to plan further ahead, adopt higher capacity products and align their infrastructure road maps more closely with our technology road map. 
For WD, this creates an opportunity that extends well beyond the initial AI infrastructure build-out. As AI scales, data creation and associated storage requirements will accelerate and compound. As always, my thanks to our customers, partners and the entire WD team, for all of you for your interest and support of WD. Thank you.

**Operator** (Operator):
The conference has now concluded. We do thank you for attending today's presentation. You may now disconnect your lines.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### WDC_Q4_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜guidance：FY27 Q1 營收財測 41 億美元±1 億（原話："We expect revenue to be $4.1 billion, plus/minus $100"）
- 2026-08-05｜CFO｜guidance：FY27 Q1 毛利率財測 55%–56%（原話："range of 55% to 56%."）
- 2026-08-05｜CFO｜guidance：FY27 Q1 EPS 財測（原話："we expect diluted earnings per share to be $4, plus/minus"）
- 2026-08-05｜CEO｜guidance：管理層稱需求年增 25% 以上的 exabyte 成長軌跡（原話："we see demand growing at above 25%, right,"）
- 2026-08-05｜CFO｜margin：Q4 毛利率 54.4%，年增 1,310 bps（原話："Gross margin expanded 1,310 basis points year-over-year"）
- 2026-08-05｜CFO｜margin：每 TB 均價年增幅由高個位數升至高十幾%（原話："digits last quarter to high teens this quarter"）
- 2026-08-05｜CFO｜margin：Q4 年增增量毛利率口徑 84–85%（原話："Ending in Q4 with incremental gross margin year-over-year,"）
- 2026-08-05｜CFO｜margin：CFO 看年增而非季增的增量毛利率（原話："I look more on my incremental gross margins"）
- 2026-08-05｜CFO｜margin：Q4 每 TB 成本年減約 8%（原話："approximately 8% year-over-year."）
- 2026-08-05｜CFO｜margin：中長期每 TB 成本年降約 10%（原話："is on or about 10% year-over-year."）
- 2026-08-05｜CFO｜margin：nearline 與非 nearline 毛利率差距不大（原話："it's all in the same ballpark right now in the 5 zip code"）
- 2026-08-05｜CFO｜margin：FY26 營收與毛利率口徑（原話："36% to $12.9 billion, while expanding gross margins"）
- 2026-08-05｜CEO｜margin：解釋季度毛利率波動來源之一（原話："There are always quarter-to-quarter variations"）
- 2026-08-05｜CFO｜customer：Q4 交付 231 EB，年增 22%（原話："We delivered 231 exabytes to our customers, up 22%"）
- 2026-08-05｜CEO｜customer：客戶採購不均導致 exabyte 季間波動（原話："they don't buy on a very linear basis."）
- 2026-08-05｜CEO｜customer：約 80% 超大規模資料中心資料存於 HDD（原話："Today, roughly 80% of data stored in a hyperscale data"）
- 2026-08-05｜CEO｜customer：新雲、前沿 AI 實驗室需求（原話："Actually, even frontier AI labs are coming to us for supply."）
- 2026-08-05｜CEO｜customer：自駕車客戶 2027 年 exabyte 需求倍增（原話："calendar year '27 has increased multiple fold, right?"）
- 2026-08-05｜CEO｜customer：企業 OEM 轉回混合式儲存（原話："There's a shift back towards hybrid systems"）
- 2026-08-05｜CEO｜competition：對中國開源模型的看法（原話："So we view it very positively for demand going forward."）
- 2026-08-05｜CEO｜product：44TB HAMR 預計 2027 上半年出貨（原話："ship our 44-terabyte HAMR product in the first half"）
- 2026-08-05｜CEO｜product：40TB ePMR 進入兩家客戶量產（原話："are now entering volume production with two customers."）
- 2026-08-05｜CEO｜product：UltraSMR 佔比目標（原話："we expect that UltraSMR will make up around 60% of"）
- 2026-08-05｜CEO｜product：高頻寬硬碟送樣（原話："We are targeting up to 8x the throughput of today's"）
- 2026-08-05｜CEO｜product：40TB 佔 nearline bits 50% 的時點（原話："Right now, we are very much on track to hit 50% of nearline"）
- 2026-08-05｜CEO｜commitment：正在談 2029–2031 長約（原話："customers to establish LTAs for calendar '29, '30 and '31"）
- 2026-08-05｜CEO｜commitment：已有一份大客戶長約到 2029（原話："one LTA of a large customer all the way up to calendar"）
- 2026-08-05｜CEO｜commitment：可預測定價策略（原話："very consistent in talking about predictable pricing"）
- 2026-08-05｜CEO｜risk：LTA 含基準價與基準量，超額部分另訂（原話："base price associated to a base volume."）
- 2026-08-05｜CEO｜risk：非 nearline 價格漲幅較快（原話："a bit more ability to drive more rapid price increases"）
- 2026-08-05｜CFO｜capital_allocation：FCF 全數回饋股東策略不變（原話："No change there to our strategy and our commitment"）
- 2026-08-05｜CFO｜capital_allocation：承諾股息與回購兩項計畫（原話："we're fully committed"）
- 2026-08-05｜CFO｜capital_allocation：Q4 回購 230 萬股共 10 億美元（原話："shares of our common stock for a total of $1 billion."）
- 2026-08-05｜CFO｜capital_allocation：回購數字含 3.28 億美元可轉債溢價現金結算（原話："describing on this call include $328"）
- 2026-08-05｜CFO｜capital_allocation：不為增加單位產能而投資 CapEx（原話："This does not require spending CapEx to add unit capacity"）

### 問答異常語氣（迴避／改口／保留）
- WDC_Q4_2026_Earnings_Call_20260805.md｜問：Reitzes 問 FY27 Q1 是否為營收與增量毛利率的低點｜答法：CFO 稱只給一季財測，未正面回答低點問題，改談需求與產品節奏
- WDC_Q4_2026_Earnings_Call_20260805.md｜問：Woodring 問長約是否有逐季價格調升條款且加速｜答法：CEO 稱『over extrapolating』，只說基準價/基準量結構，不給調升幅度
- WDC_Q4_2026_Earnings_Call_20260805.md｜問：Karl Ackerman 問未來 12 個月有多少比例 nearline 長約重新定價｜答法：CFO 只回答毛利率差距，未回答重新定價比例
- WDC_Q4_2026_Earnings_Call_20260805.md｜問：Muse 問為何財測成長與毛利率低於主要競爭對手｜答法：CEO 以季間波動、長約時點與產品換代回應，未直接對比競爭對手或給數字

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

## ⑥ 條件附卡（archetype_hint='循環/商品' 命中）：judge_addendum_cyclical.md

<!-- source: .claude/skills/stock-analyst/references/cyclical-lens.md sha256:b13d95972edd47ea git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary 或 secondary ∈ {循環/商品，EMS/ODM}（QC-43 判定，含 capex 建設循環／需求量循環子型） -->

# QC-42 循環交易讀數（附錄 B）附卡

循環股的錢在 Game 2（投降買、延伸賣）。本附卡是平行、明標投機的交易讀數，不改長抱裁決。[§WHY]

## 一、觸發與子型判定
無循環 sleeve（純成長 mis-route）→ 整段省略。[§①]
商品子型（下列≥2命中→用商品 through-cycle 錶）：近5-7年≥1個GAAP虧損年｜peak-to-trough毛利率擺動>~20pp｜營收主由商品ASP驅動(price-taker)｜產業∈{記憶體/DRAM/NAND、礦業/材料/稀土、化工、航運、鋼鐵、太陽能、油氣E&P、部分晶圓/設備}｜capex/rev結構性>15%且ROIC高度擺動。未達≥2仍判循環→依驅動來源選capex建設循環錶或需求量循環錶。[§商品子型]

## 二、循環位置錶族（三選一，錨自身 through-cycle 區間非動能；位置落 深谷投降/早循環/中循環/晚循環/過熱頂部，多數決+sourced 裁決）
商品 through-cycle（MU 型，6 訊號）：P/B vs 自身區間(近1x/下緣=買，>中位2x/上緣=賣)｜量 vs 價(量增領先=買，ASP-only量平降=賣)｜GM vs自身區間(近谷/負=買，近峰=賣)｜供給紀律(減產=買，新產能洪水=賣)｜庫存(去化乾淨=買，通路+公司堆積=賣)｜情緒/部位(投降PT>價=買，狂熱PT<價=賣)。[§B.1商品]
capex 建設循環（ORCL 型，6 訊號）：capex/折舊比(低/正常化=買，遠高於1=賣)｜產能利用率爬坡(低基期回升=買，滿載見頂=賣)｜RPO(backlog)vs capex覆蓋(backlog領先=買，capex超前需求=賣)｜交易對手信用(客戶分散信用強=買，集中燒錢客戶=賣)｜情緒/部位(同上)｜量vs價(量增領先=買，ASP承壓量見頂=賣)。[§B.1capex]
需求量循環（EMS/ODM，JBL 型，5 訊號）：book-to-bill/需求量拐點(>1拐點向上=買，<1量見頂=賣)｜客戶庫存去化(去化乾淨=買，通路+客戶堆積=賣)｜倍數vs自身歷史re-rate均值回歸(近下緣=買，>5Y中位×1.5/貼峰=賣)｜終端·hyperscaler capex週期位置(早週期=買，晚週期見頂=賣)｜情緒/部位(同上)。[§B.1需求量]

## 三、交易姿態 + 反動能硬閘（跨子型通用，逐條檢查，觸發即 override 向保守）
位置→姿態：深谷投降→積極分批建立｜早→分批建立｜中→持有不加｜晚→分批了結｜頂→清光不碰。[§B.2]
閘1 位置=晚/頂→姿態不得為任何「建立」。閘2 成長=ASP-only+量持平/降→最多「持有」。閘3 P/B>自身中位2x→禁新建立。閘4 訊號矛盾→標「位置不明，觀望」不硬給姿態。閘5 TTM/Fwd本益比或EV倍數>自身歷史高區(>5Y中位×1.5、或貼/破歷史峰)→禁新建立。[§閘1-5]

## 四、落欄與 §13 row 8b 接線
`cycle_position`(深谷投降｜早循環｜中循環｜晚循環｜過熱頂部)＋`cycle_verdict`(右側可追蹤｜等回踩｜頂部觀望｜未觸發)；非循環 archetype 不填，整欄省略。[§落欄]
接 §13 row 8b：位置∈{深谷投降，早循環}+五閘全過+moat底線+獨立critic冷讀通過→落「進場・條件式(循環衛星)」(倉位上限3%)；任一不成立→只落研究提名，§13維持觀望。驗證失敗不得升級，只能降回觀望。`trade_stance`僅進HTML不入dd-meta。[§row8b]

## 五、雙制度與兩軌背離
有 secular sleeve + commodity sleeve → 循環鏡頭只套 commodity sleeve，secular sleeve 一句話另計(不隨循環賣)。[§⑤]
投資軌(§13長抱視角) vs 交易軌(本鏡頭位置)：底部背離(長抱視角迴避 + 循環位置深谷投降/早循環)是本鏡頭獨門訊號；頂部多收斂(皆遠離)。[§B.3]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20261013","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價≤$320（約10倍FY2028E共識）且每TB價格年增仍≥0→首倉1/3；或CY2029後長約揭露鎖價且Toshiba擴產未致降價→重跑判斷","irr_base_pct":5.3,"ev5y_pct":20.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.3,"ev5y_pct":20.0,"irr_base_pct":5.3,"max_dd_pct":-72,"bull_5y_price":900.0,"bear_5y_price":137.5,"p_bull_pct":20,"p_bear_pct":32,"rearm_trigger":"股價≤$320（約10倍FY2028E共識）且每TB價格年增仍≥0→首倉1/3；或CY2029後長約揭露鎖價且Toshiba擴產未致降價→重跑判斷","price_at_dd":386.94,"archetype":"循環/商品","cycle_position":"晚循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261024/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
