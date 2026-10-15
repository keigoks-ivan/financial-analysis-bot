你是 stock-analyst **v20 判斷 agent**，標的 WDC（20261013）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"WDC","date":"2026-10-13","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261013/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261013/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":3747,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":1655,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"USD M（利益率 44.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":1563,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"USD M（利益率 41.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}},{"id":"f_kpi5_non_gaap","label":"Non-GAAP 毛利率","value":54.4,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"%（GAAP 54.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}},{"id":"f_kpi6_q1_fy2027_non_gaap","label":"管理層指引：Q1 FY2027（non-GAAP）","value":"營收 4.1B ±100M（YoY +42%~49%）；毛利率 55%~56%；營業費用 390~400M；EPS 4.00 ±0.15","period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"—","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-05","period":"2026-08-05","unit":"date","basis":"距今 49 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_wdc_gross_margin_pct","label":"WDC 毛利率","value":48.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WDC.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_wdc_operating_margin_pct","label":"WDC 營業利益率","value":35.6,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WDC.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_wdc_fcf_margin_pct","label":"WDC FCF 利潤率","value":27.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WDC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sndk_gross_margin_pct","label":"SNDK 毛利率","value":71.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sndk_operating_margin_pct","label":"SNDK 營業利益率","value":61.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sndk_fcf_margin_pct","label":"SNDK FCF 利潤率","value":56.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_gross_margin_pct","label":"000660.KS 毛利率","value":76.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_operating_margin_pct","label":"000660.KS 營業利益率","value":68.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_fcf_margin_pct","label":"000660.KS FCF 利潤率","value":47.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_gross_margin_pct","label":"005930.KS 毛利率","value":57.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_operating_margin_pct","label":"005930.KS 營業利益率","value":36.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_fcf_margin_pct","label":"005930.KS FCF 利潤率","value":28.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":1281,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"USD M（營運現金流 1,389，淨資本支出 108）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}},{"id":"f_kpi4_sbc","label":"SBC","value":45,"period":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","unit":"USD M（占 GAAP 營業利益 2.9%、占營收 1.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":386.94,"period":"2026-10-12（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":10.57,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":36.4,"period":"2026-10-12（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.15,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.09 → 20.12）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.25,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（31.75 → 31.83）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-4.37,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（44.83 → 42.87）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":20.12,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":31.83,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":42.87,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":102.21,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 9.95 → 20.12（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":14.37,"period":"2026-10-12（RTH 收盤，UTC）","unit":"x","basis":"2 個年度端點內的分位＝21.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-12（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":21.0,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":11.21,"period":"2026-10-12（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝67.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-12（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":67.3,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":11.18,"period":"2026-10-12（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝65.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-12（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":65.3,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":19.75,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 20.12，分子＝快照價 397.28","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.142,"period":"2026-10-13","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-13"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-388.0,"period":"2026-10-13","unit":"USD m","basis":"yfinance 最新一季：總債務 1191.0、現金 1579.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":374.32,"period":"2026-10-13","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":144452.64,"period":"2026-10-13","unit":"USD m","basis":"市值 144840.64 ＋ 淨負債 -388.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":19270.16,"period":"2026-10-13","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（23 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":26358.22,"period":"2026-10-13","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（22 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":7.5,"period":"2026-10-13","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Nikkei 報導 Toshiba 計畫 HDD 產能於 FY2027 前約倍增，容量份額目標由約 10% 拉到 30%；報導後 2026-10-02 WDC 約跌 10%、STX 約跌 15%，Fool 文章並指 Toshiba 可能以低價搶單壓縮 WD 毛利","source":"Motley Fool, Why Western Digital Stock Just Crashed","url":"https://www.fool.com/investing/2026/10/02/why-western-digital-stock-just-crashed/","excerpt":"Toshiba aims to lift its HDD share by storage capacity from just over 10% to 30% over the medium term, according to Nikkei.","as_of":"2026-10-02","retrieved_at":"20261013","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"2026 年 8 月報導 HDD 份額：WD 約 42%、Seagate 41%、Toshiba 17%（未見 2026 年 WD 增減份額的季度序列）","source":"Motley Fool / 搜尋彙整 (2026-08 report)","url":"https://www.fool.com/investing/2026/10/02/why-western-digital-stock-just-crashed/","excerpt":"In terms of HDD market share, WD currently represents approximately 42% of the market, followed closely by Seagate at 41% and Toshiba at 17%.","as_of":"2026-08-31","retrieved_at":"20261013","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"HAMR 進度：Seagate 已有兩家大型 hyperscaler 量產採購 Mozaic 4+；WDC 預計 2026 上半年與一家 hyperscaler 開始認證、年底擴至最多三家，量產爬坡 2027 上半年（3dnews 另稱 2026 年底開始 HAMR 生產，時間不一致）","source":"Nasdaq/Zacks, Seagate vs. Western Digital: Which Storage Stock is the Better Buy Now?","url":"https://www.nasdaq.com/articles/seagate-vs-western-digital-which-storage-stock-better-buy-now","excerpt":"WDC remains on track to begin qualification with one hyperscale customer in the first half of 2026, expanding to up to three customers by year-end.","as_of":"2026-07-29","retrieved_at":"20261013","affects":["moat_trend","triggers"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Coughlin 2025 Q1 資料：WD 單位份額 42%（179.8 EB）、Seagate 40%、Toshiba 18%，WD 自 Toshiba 取得約 1 點份額","source":"Blocks & Files (Coughlin newsletter)","url":"https://blocksandfiles.com/?p=38863","excerpt":"Western Digital at 179.8 EB and 42% of unit share, Seagate at 143.6 EB and 40%, and Toshiba at 41 EB and 18%.","as_of":"2025-06-01","retrieved_at":"20261013","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"長期替代風險為 flash（SanDisk、Samsung、Micron、Kioxia）；未找到具名的 HDD 新進入者；WD 已把 SSD 業務分出，專注 HDD","source":"Seeking Alpha, Western Digital: Watch For Technological Threats Following Post-Earnings Sell-Off","url":"https://seekingalpha.com/article/4933754-western-digital-watch-for-technological-threats-following-post-earnings-sell-off","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"WDC FY2026 10-K：三個客戶分別占 FY2026 淨營收 16%、15%、13%；前十大客戶占 73%（FY2025 68%、FY2024 55%），FY2024 無單一客戶達 10%。","source":"SEC WDC Form 10-K FY2026 (period ended 2026-07-03)","url":"https://www.sec.gov/Archives/edgar/data/0000106040/000162828026057139/wdc-20260703.htm","excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"管理層稱前七大客戶已下單至 2026 上半年、其中五家涵蓋全年 2026；一家大型超大規模客戶簽了涵蓋 2027 全年的協議（2025 年 10 月財報說明）。","source":"Blocks & Files, Western Digital extends lead over Seagate as AI drives demand tailwinds","url":"https://blocksandfiles.com/2025/10/31/western-digital-extends-lead-over-seagate-as-ai-drives-demand-tailwinds/","excerpt":null,"as_of":"2025-10-31","retrieved_at":"20261013","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Qualstar 稱 Microsoft、Amazon、OVH、Baidu 在其封存層下方使用自動化磁帶，超大規模業者已將冷儲存下層分散化（非 HDD 自製或第二供應商的直接證據）。","source":"Qualstar, How hyperscale data growth is changing the future of cold storage","url":"https://www.qualstar.com/blog/how-hyperscale-data-growth-is-changing-the-future-of-cold-storage","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261013","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"WDC FY2026 10-K：前 10 大客戶占淨營收 73%（FY2025 68%、FY2024 55%）；三家客戶各占 16%、15%、13%（合計 44%）","source":"SEC EDGAR, WESTERN DIGITAL CORP Form 10-K FY2026 (period ended 2026-07-03)（內容經搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/0000106040/000162828026057139/wdc-20260703.htm","excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"WDC 執行長於 2026 年 1 月財報會表示 2026 年 HDD 產能幾乎售罄，並有長期框架協議延伸至其後年度；多年合約涵蓋 2027、2028。","source":"Gigazine, Western Digital 2026 HDD capacity runs out (2026-02-16)","url":"https://gigazine.net/gsc_news/en/20260216-western-digital-2026-hdd-capacity-runs-out","excerpt":null,"as_of":"2026-02-16","retrieved_at":"20261013","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"WDC 與前五大客戶中三家有商業協議，兩家至 CY2027、一家至 CY2028（搜尋彙整引述 CEO 說法；日期為彙整，非原始發布日，未能核實原文日期）。","source":"WebSearch 彙整（NAND/HDD 展望，techspot 等二手來源）","url":null,"excerpt":"robust commercial agreements with three of our top five customers, two through calendar year 2027 and one through calendar year 2028","as_of":"2026-02-16","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"傳聞 Toshiba 計畫投資約 600 億日圓（約 3.8 億美元）於菲律賓，於 FY2027 前將 HDD 產出約翻倍，市佔由約 10% 朝 30% 提升；Toshiba 未證實；消息使 Seagate 跌約 10%、WDC 跌約 7%。","source":"247WallSt, Seagate Tumbles 10%, Western Digital Drops 7% as Toshiba Moves to Double Hard Disk Output (2026-10-02)","url":"https://247wallst.com/investing/2026/10/02/seagate-tumbles-10-western-digital-drops-7-as-toshiba-moves-to-double-hard-disk-output/","excerpt":null,"as_of":"2026-10-02","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Morgan Stanley 認為即使加計 Toshiba 新產能，HDD 市場至 2028 仍供不應求；Citi 認為 Toshiba 擴產對全球供給影響有限（platter 與磁頭仰賴外部供應商）。","source":"WebSearch 彙整：Tikr/Blocksandfiles/247WallSt 報導（2026-10 初）","url":"https://www.blocksandfiles.com/disk/2026/10/06/distant-third-hdd-maker-toshiba-spending-380-million-to-catch-up/5301322","excerpt":null,"as_of":"2026-10-06","retrieved_at":"20261013","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce 稱雙寡頭售罄並維持供給紀律，Toshiba 因投資到量產有時滯短期貢獻有限；隨雙寡頭轉 HAMR，供需將逐步趨近平衡，WDC 的 HAMR 進度為關鍵變數；預期 Seagate 將超越 WDC 成最大供應商。","source":"TrendForce, Seagate to Top HDD Market by 2028 on HAMR Lead (RP261007HN)","url":"https://www.trendforce.com/research/download/RP261007HN","excerpt":null,"as_of":"2026-10-07","retrieved_at":"20261013","affects":["moat_trend","thesis.R","triggers"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Seagate 稱 nearline 容量多數已分配至 2028；NAND 方面 TrendForce 預期 2026 供給缺口 4–5%，2027 下半年供給成長超過需求（NAND 非 WDC 主營 HDD，僅供背景）。","source":"WebSearch 彙整（TechSpot/DigitalCitizen NAND shortage ease 2027；pcserverandparts）","url":"https://www.techspot.com/news/113186-nand-shortages-could-finally-ease-2027-but-adata.html","excerpt":"The analyst firm says the market will remain undersupplied throughout 2026, recording a supply deficit of between 4% and 5%","as_of":"2026-10-13","retrieved_at":"20261013","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"WDC 10-Q（期間至 2026-01-02）稱截至 FY2026 第二季，營運與業績未因關稅行動受到重大影響，公司持續監控。","source":"WESTERN DIGITAL CORP Form 10-Q (quarter ended 2026-01-02)","url":"https://www.sec.gov/Archives/edgar/data/106040/000162828026004207/wdc-20260102.htm","excerpt":null,"as_of":"2026-01-02","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-01-14 總統公告依 Section 232 對一小組先進半導體及含其之衍生品課 25% 關稅（2026-01-15 生效），豁免含美國資料中心用途等；搜尋結果未顯示硬碟／NAND 是否屬涵蓋品項。","source":"White & Case, President Trump orders narrowly targeted 25% Section 232 tariff on certain advanced semiconductor articles","url":"https://www.whitecase.com/insight-alert/president-trump-orders-narrowly-targeted-25-section-232-tariff-certain-advanced","excerpt":null,"as_of":"2026-01-14","retrieved_at":"20261013","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Section 232 第二階段可能在貿易談判結束後課「顯著」關稅；商務部與 USTR 須於 2026-04-14 前提交談判更新，搜尋未找到更新內容。","source":"Baker McKenzie Global Import Blog, US President Trump issues Section 232 proclamations on semiconductors and critical minerals","url":"https://globalimportblog.bakermckenzie.com/2026/01/27/us-president-trump-issues-section-232-proclamations-on-semiconductors-and-critical-minerals/","excerpt":null,"as_of":"2026-01-27","retrieved_at":"20261013","affects":["triggers","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"DatacenterDisk 分析稱硬碟主要在泰國與馬來西亞組裝，零組件來自日本（碟片）、中國（電子件）、菲律賓（組裝）；對泰、馬、韓、中電子產品的關稅加劇 AI 驅動的缺貨，稅率多次宣布、暫停、修改再恢復。","source":"DatacenterDisk, US tariffs hard drive SSD prices 2026","url":"https://datacenterdisk.com/news/us-tariffs-hard-drive-ssd-prices-2026","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261013","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"搜尋未發現 WDC 本身被列入 Entity List 或遭 2026 年新的中國專屬出口管制；MOFCOM 2026-06-22 公告第 23 號新增的十家美國實體不含 WDC。","source":"Sinolytics Radar 241","url":"https://sinolytics.de/documents/Sinolytics-Radar-241.pdf","excerpt":null,"as_of":"2026-06-22","retrieved_at":"20261013","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"有節目簡介稱 WDC 製造足跡高度集中於泰國與馬來西亞，並受新「原產地」解釋審視（二手來源，未對照 10-K）","source":"Audible 2026Q2 Western Digital Corporation (WDC) 節目簡介","url":"https://www.audible.co.uk/pd/B0GNX9CPQ1","excerpt":"Western Digital's manufacturing footprint, heavily concentrated in Thailand and Malaysia, faces scrutiny under new \"Country of Origin\" interpretations","as_of":"2026-07-01","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"磁頭獨立供應商僅 TDK 一家，同時供應三大 HDD 廠（引 Bloomberg，經供應商部落格轉述）","source":"Fusion Worldwide blog: How China's export controls are disrupting HDD manufacturing and supply","url":"https://info.fusionww.com/blog/how-chinas-export-controls-are-disrupting-hdd-manufacturing-and-supply","excerpt":"TDK is the only independent supplier of magnetic recording heads and currently supplies all three HDD giants.","as_of":"2026-01-01","retrieved_at":"20261013","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中國稀土出口管制：中重稀土出貨仍需逐案核准，暫停期至 2026-11-10（供應商部落格轉述）","source":"Fusion Worldwide blog: Is Hard Disk Drive Supply the Next Major Infrastructure Bottleneck?","url":"https://info.fusionww.com/blog/is-hard-disk-drive-supply-the-next-major-infrastructure-bottleneck","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261013","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"WDC 10-Q 稱關稅行動截至 2026 會計年度第一季未對經營造成重大影響，持續監控","source":"WDC Form 10-Q (period ended 2025-10-03)","url":"https://www.sec.gov/Archives/edgar/data/106040/000162828025047613/wdc-20251003.htm","excerpt":"Our business and results of operations have not been materially impacted through the first quarter of 2026 as a result of the recent tariff actions, but we are actively monitoring developments.","as_of":"2025-11-01","retrieved_at":"20261013","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"法說會答覆稱已開發稀土與貴金屬替代供應來源，預期出口管制無重大影響（逐字稿日期未顯示）","source":"WDC earnings call（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0000106040/000162828026064921/wdc015705-ars.pdf","excerpt":"developed alternate sources of supply for rare earth and precious minerals, so we do not anticipate any material impact from export controls","as_of":"2026-01-01","retrieved_at":"20261013","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"WDC FY2026 Q4 營收：Cloud 約 $3.3B（占 89%，YoY +43%）、Client $225M（+61%）、Consumer $187M（+38%）；管理層將 Client/Consumer 成長歸因於定價改善。FY2026 全年營收 $12.9B（+36%）。","source":"StorageNewsletter, WD fiscal 4Q26 and FY26 financial results; Nasdaq, Western Digital Q4 earnings call highlights","url":"https://www.storagenewsletter.com/2026/08/07/wd-fiscal-4q26-and-fy26-financial-results/","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 Q3（截至 2026-04-03）10-Q：Cloud 成長主因為出貨 exabytes +36% 與每 EB 平均售價 +9%；Q3 Cloud 約 $3.0B（占 89%，YoY +48%）、Consumer $186M（+24%）、Client $179M（+31%）。（搜尋摘要另有來源給出不同 Q3 client/consumer 數字，未對 10-K 核實）","source":"SEC 10-Q WDC quarter ended 2026-04-03; Q3 FY2026 earnings call summary","url":"https://www.sec.gov/Archives/edgar/data/0000106040/000162828026029054/wdc-20260403.htm","excerpt":null,"as_of":"2026-04-03","retrieved_at":"20261013","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"WDC 執行長稱 2026 日曆年產能大致售罄；與前五大客戶中三家簽有長約，兩家至 2027 年、一家至 2028 年。Seagate 稱其 nearline 2026 產能已全數配置。","source":"heise.de, WD and Seagate confirm: Hard drives for 2026 sold out; Seagate Q2 2026 earnings call","url":"https://heise.de/-11178917","excerpt":null,"as_of":"2026-01-30","retrieved_at":"20261013","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Seagate 執行長稱隨 2027–2028 新產能上線，價格「持平至小幅上漲」是可能的（價格由供需決定）；Morgan Stanley 預測（二手轉引，未核對原報告）nearline 供給缺口今年約 300EB、2027–28 年擴大至約 400EB。","source":"Seagate Q2 2026 earnings call transcript (AOL); secondary LinkedIn post citing Morgan Stanley","url":"https://www.aol.com/finance/seagate-stx-q2-2026-earnings-143836038.html","excerpt":null,"as_of":"2026-01-30","retrieved_at":"20261013","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"TrendForce 估 2026 HDD 市佔：WDC 48%、Seagate 42%、Toshiba 10%（另一 7 月估計為 WDC/STX 各逾 40%、Toshiba 約 17%，口徑不同）。德國零售通路 HDD 價格較 2025 年中上漲約 20–50%。","source":"TrendForce projection via StockHub / newsable coverage; German retail report via heise","url":"https://stockhub.kr/en/news/news_e30078befc8b","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261013","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"2026-10-02 報導 Toshiba 計劃投資約 600 億日圓、於 FY2027 前將 HDD 產能倍增；當日 Seagate 股價跌約 10%、WDC 跌約 7%，市場擔憂長期壓抑價格。","source":"24/7 Wall St., Seagate Tumbles 10%, Western Digital Drops 7% as Toshiba Moves to Double Hard Disk Output","url":"https://247wallst.com/investing/2026/10/02/seagate-tumbles-10-western-digital-drops-7-as-toshiba-moves-to-double-hard-disk-output/","excerpt":null,"as_of":"2026-10-02","retrieved_at":"20261013","affects":["decision_inputs.bear","moat_trend","triggers"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"+","claim":"WDC 2026 年 HDD 供給已近售罄；公司稱 HDD 與 SSD 每 TB 價差約 5–10 倍（依搜尋摘要轉述，未讀原頁）","source":"Gigazine: Western Digital 2026 HDD capacity runs out (2026-02-16)","url":"https://gigazine.net/gsc_news/en/20260216-western-digital-2026-hdd-capacity-runs-out","excerpt":null,"as_of":"2026-02-16","retrieved_at":"20261013","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Western Digital Investor Day（2026-02）：HAMR 硬碟已在兩家客戶認證中，路線圖指向約 2029 年 100TB（依搜尋摘要轉述）","source":"MarketBeat: Western Digital Investor Day HAMR roadmap, AI data center shift and new $4B buyback plan","url":"https://www.marketbeat.com/instant-alerts/western-digital-investor-day-hamr-roadmap-ai-data-center-shift-and-new-4b-buyback-plan-2026-02-04/","excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261013","affects":["moat_trend","triggers"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"第三方彙整 WDC FY2026 10-K 風險因子：HAMR 轉換為高風險技術轉換，含毛利壓力與可能觸發客戶合約「epidemic failure」條款的瑕疵風險（非 10-K 原文，需對照）","source":"Autobound: What Western Digital's FY2026 10-K says: 11 signals","url":"https://www.autobound.ai/companies/western-digital/10-k","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261013","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 10-K：雲端占淨營收 89%（年增 38%），client 6%、consumer 5%；前十大客戶占淨營收 73%（FY2025 68%、FY2024 55%）。","source":"WDC Form 10-K FY2026 (SEC) 經搜尋摘要轉述","url":"https://www.sec.gov/Archives/edgar/data/0000106040/000162828026057139/wdc-20260703.htm","excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261013","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"通路誘因（經銷商／零售商價格保護與行銷補貼）占毛營收 9%（FY2026）、10%（FY2025）、11%（FY2024）。","source":"WDC Form 10-K FY2026 (SEC) 經搜尋摘要轉述","url":"https://www.sec.gov/Archives/edgar/data/0000106040/000162828026057139/wdc-20260703.htm","excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261013","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FQ2 2026 法說：前七大客戶以確定採購單涵蓋至 2026 曆年；前五大中兩家 LTA 涵蓋至 2027、一家至 2028，約定 EB 量與價格結構（二手轉述，未讀原文）。","source":"Futurum Group, Western Digital Q2 FY 2026 Results Beat on Cloud HDD Demand","url":"https://futurumgroup.com/insights/western-digital-q2-fy-2026-results-beat-on-cloud-hdd-demand/","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261013","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"產業文章描述 HDD 銷售由商品模式轉向以 LTA 為基礎的 build-to-order，小型買家較難取得硬碟（二手轉述）。","source":"Horizon Technology, hdd long term agreements","url":"https://horizontechnology.com/news/hdd-long-term-agreements/","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261013","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga（2026 年 9 月下旬快照）：20 位分析師共識為 Buy（16 Buy／4 Hold），平均目標價 $483；Citigroup 8/7 由 $800 降至 $740，TD Cowen 8/6 由 $500 升至 $540。","source":"Benzinga WDC price-targets","url":"https://kr.benzinga.com/quote/WDC/price-targets","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261013","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布極寬：Susquehanna $500（Neutral）、UBS $560、Wells Fargo $730（7/10 由 $575 上調、Overweight）、Cantor Fitzgerald $900、Melius $1,050；TickerLeague 另顯示 4 位分析師區間 $250–$660（價格資料疑為較舊）。","source":"FN2 analyst consensus; Benzinga; TickerLeague","url":"https://fn2.ai/earnings/wdc/analysts","excerpt":null,"as_of":"2026-07-10","retrieved_at":"20261013","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY26 Q4（2026-08-05 公布）營收 $3.75B（年增 44%）、EPS $3.56，優於共識 $3.27／$3.69B；FY27 Q1 指引營收 $4.1B±$0.1B、調整後 EPS 約 $4.00±$0.15，高於分析師預期（Benzinga 列共識 EPS $3.63，另列 Q1 FY27 共識 $4.03／$4.14B，兩來源口徑不一）。","source":"stock3 (德文市場報導); Benzinga earnings forecasts","url":"https://stock3.com/news/western-digital-marge-springt-auf-rekordniveau-ausblick-hebt-an-17226404","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261013","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"財報後股價下跌 5.36%，儘管數字優於預期，BingX 摘要稱因 2026 年大幅上漲後預期已被墊高。","source":"BingX: Western Digital (WDC) Q4 FY2026 Earnings Overview","url":"https://bingx.com/en/news/post/western-digital-wdc-q-fy-earnings-overview-strong-results-fail-to-impress-and-trigger-a-selloff","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261013","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Seeking Alpha 修正面：截至 2026-03-27 近三個月 EPS 上修 20 次、下修 0 次；營收上修 21 次、下修 0 次。","source":"Seeking Alpha WDC earnings revisions","url":"https://seekingalpha.com/symbol/WDC/earnings/revisions","excerpt":"EPS # of Up Revisions 20 EPS # of Down Revisions 0 Revenue # of Up Revisions 21 Revenue # of Down Revisions 0","as_of":"2026-03-27","retrieved_at":"20261013","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Barclays 2026-04-21 將目標價由 $325 上調至 $405，理由為 HDD 市場估計。","source":"Yahoo Finance: Barclays Raises its Price Target on Western Digital (WDC) to $405","url":"https://finance.yahoo.com/markets/stocks/articles/barclays-raises-price-target-western-163803561.html","excerpt":null,"as_of":"2026-04-21","retrieved_at":"20261013","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-07-09 報導稱 Western Digital 與 Kioxia 洽談合併；未揭露交易金額，搜尋結果未見簽署最終協議的確認（OCBJ 引 WSJ 稱可能逾 200 億美元、以股票支付，來源日期不一致）。","source":"Simply Wall St 公司公告摘要／OCBJ 引 WSJ『western digital advanced talks merge kioxia wsj』","url":"https://www.ocbj.com/news/weekly-news/western-digital-advanced-talks-merge-kioxia-wsj/","excerpt":null,"as_of":"2026-07-09","retrieved_at":"20261013","affects":["valuation","triggers","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-07-09 報導稱 Western Digital 與 Kioxia 洽談合併；未揭露交易金額，未見最終協議確認。","source":"Simply Wall St 公司公告摘要／OCBJ 引 WSJ","url":"https://www.ocbj.com/news/weekly-news/western-digital-advanced-talks-merge-kioxia-wsj/","excerpt":null,"as_of":"2026-07-09","retrieved_at":"20261013","affects":["valuation","triggers","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"WDC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":48.85,"operating_margin_pct":35.6,"fcf_margin_pct":27.18,"rd_intensity_pct":8.99},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WDC","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"SNDK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.47,"operating_margin_pct":61.58,"fcf_margin_pct":56.77,"rd_intensity_pct":6.56},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"000660.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":76.27,"operating_margin_pct":68.04,"fcf_margin_pct":47.8,"rd_intensity_pct":4.93},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"005930.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.48,"operating_margin_pct":36.88,"fcf_margin_pct":28.95,"rd_intensity_pct":9.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"PSTG","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PSTG"},"note":"quarterly_income_stmt 無資料"}],"subject":"WDC"},"financial_history":{"ticker":"WDC","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":6255000000.0,"revenue_yoy_pct":null,"gross_margin_pct":22.24,"operating_margin_pct":-6.43,"net_income":-1684000000.0,"diluted_eps":-5.37,"free_cash_flow":-1229000000.0,"fcf_margin_pct":-19.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":6317000000.0,"revenue_yoy_pct":0.99,"gross_margin_pct":28.07,"operating_margin_pct":1.54,"net_income":-798000000.0,"diluted_eps":-2.61,"free_cash_flow":-781000000.0,"fcf_margin_pct":-12.36,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":9520000000.0,"revenue_yoy_pct":50.7,"gross_margin_pct":38.78,"operating_margin_pct":22.37,"net_income":1861000000.0,"diluted_eps":5.12,"free_cash_flow":1279000000.0,"fcf_margin_pct":13.43,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":12919000000.0,"revenue_yoy_pct":35.7,"gross_margin_pct":48.85,"operating_margin_pct":35.6,"net_income":9298000000.0,"diluted_eps":26.92,"free_cash_flow":3511000000.0,"fcf_margin_pct":27.18,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDC/WDC_Q4_2026_Earnings_Call_20260805.md）

# Q4 2026 Earnings Call
2026-08-05

Q4 2026 Earnings Call
Western Digital Corporation | Earnings Calls | 2026-08-05
Operator (Operator)
Good afternoon, and welcome to the Western Digital's Fourth Quarter Fiscal 2026 Conference Call.
[Operator Instructions] Please note, this event is being recorded. I would now like to turn the
conference over to Mr. Ambrish Srivastava, Vice President of Investor Relations. Please go ahead.
Ambrish Srivastava (Executives)
Thank you, and good afternoon, everyone. Joining me today are Irving Tan, WD's Chief Executive
Officer; and Kris Sennesael, WD's Chief Financial Officer. Before we begin, please note that today's
discussion will contain forward-looking statements based on management's current assumptions and
expectations, which are subject to various risks and uncertainties.
These forward-looking statements include expectations for our product portfolio, our business plans
and performance, ongoing market trends and our future financial results. We assume no obligation to
update these statements. Please refer to our most recent annual report on Form 10-K and our other
filings with the SEC for more information on the risks and uncertainties that could cause actual results
to differ materially from expectations.
In our prepared remarks, our comments will be related to non-GAAP results on a continuing operations
basis, unless stated otherwise. Reconciliations between the non-GAAP and comparable GAAP financial
measures are included in the press release and other materials that are being posted in the Investor
Relations section of our website at investor.wdc.com. Lastly, I want to note that when we refer to we,
us, our or similar terms, we are referring only to Western Digital as a company and not speaking on
behalf of the industry.
With that, I will now turn the call over to Irving for introductory remarks. Irving?
Tiang Yew Tan (Executives)
Thanks, Ambrish. Good afternoon, everyone, and thank you for joining us today. Let me begin by
reflecting on our first full fiscal year of WD as a focused pure-play HDD company. We drove strong
year-on-year revenue growth of 36%, while expanding our gross and operating margins significantly.
We doubled EPS, generated $3.5 billion in free cash flow and strengthened our balance sheet to a net
positive cash position, while continuing to make significant capital returns to shareholders.
These strong financial results are an outcome of meeting our customers' growing storage demand by
focusing on innovation and driving operational excellence across the global WD organization. We enter
fiscal year 2027 with robust customer demand, increased visibility and continued confidence in the
durability of demand as well as our ability to service this demand with our industry-leading products
and technology road map. Demand for storage is being driven both by AI as well as by core cloud
services. Within the AI infrastructure market, there is a key dynamic taking shape. While compute
cycles can be reused, data compounds. Training and inference workloads share and reuse compute
resources over time. Yet the data generated by these workloads, including model inputs, outputs, logs
and retained context continues to accumulate.

As AI usage scales, this creates a growing need for storage infrastructure capable of economically
storing and managing these massive data sets. The inflection we have discussed in the past from AI
training to inference to Agentic AI has only become more pronounced. Training models create
significant initial data requirements, but inference generates and retains data continuously. Today, the
largest AI platforms process tens of billions of tokens per minute and billions of prompts per day,
creating a rapidly expanding body of data that must be stored, managed and accessed over time.
Recent disclosures show token volumes growing several fold year-over-year, underscoring the pace at
which inference is scaling. Meanwhile, AI is moving rapidly from merely answering questions to
Agentic AI that does the work, coordinating tasks, accessing data and operating continuously across
multistep workflows. This transition creates a fundamentally more data-intensive workload and one
that is increasingly persistent rather than transient.
The storage implications are significant. Agents generate data at every step of the workflow, increasing
both the volume of data created and the amount that must be stored over time. This is why we continue
to view Agentic AI as a structural and step function driver of capacity-oriented storage demand. Beyond
inference and Agentic AI, we are also seeing the emergence of physical AI, autonomous vehicles,
robotics and industrial automation systems and humanoids, where the volume of real-world data
needed to train these systems is insufficient, thereby requiring the generation and storage of synthetic
data sets, creating another driver of storage demand.
Infrastructure investment is important, but it's only the beginning. Training creates the initial data
foundation, inference generates data continuously, Agentic systems multiply the volume and frequency
of that data, and physical AI accelerates the cycle further. Together, these trends create a more durable
demand environment for data storage, driven not just by building AI infrastructure, but by the
continuous creation and retention of data once that infrastructure is deployed.
As AI workloads move from deployment to sustained use, storage demand becomes less about a
onetime infrastructure build cycle and more about the compounding of data. That is the underlying
secular demand growth driver for our business. Today, roughly 80% of data stored in a hyperscale data
center resides on hard disk drives. That is likely to continue. That reflects what HDDs do exceptionally
well, delivering the scale, economics and power efficiency required for long retention large-scale data
storage.
Let me now turn to why these secular growth drivers play to WD's strengths. WD's robust technology
road map is based on the industry-leading areal density per platter with a focus on innovation to meet
our customers' capacity needs at scale, along with our growing ability to meet their requirements by
providing cost-effective storage solutions in additional layers of the AI storage stack. We are on track to
ship our 44-terabyte HAMR product in the first half of calendar year 2027. Customer feedback on the
qualification process continues to be very positive with the capacity, performance and reliability of our
drives exceeding customer expectations.
For our next-generation 40-terabyte ePMR drives, we commenced shipments in our June quarter and
are now entering volume production with two customers. We're currently ramping our UltraSMR
technology with the third major customer, and we expect that UltraSMR will make up around 60% of
our nearline exabyte shipments as we exit fiscal 2027.
Since our last update, we have continued to broaden our customer engagement and qualification
pipeline with additional hyperscale and cloud customers advancing through qualification and

deployment planning. Beyond capacity, we are also extending innovation into new layers of the AI
storage stack. We are making progress on improving drive performance with our high-bandwidth
drives and are now sampling with 5 customers. We are targeting up to 8x the throughput of today's
drives without the corresponding increase in power draw, exactly the kind of performance AI workloads
require.
In closing, the opportunity in front of us is real. And at WD, we are well positioned to capture it. Data
creation isn't slowing, it's accelerating. And as the value of data grows, so does the infrastructure
storage requirements to store, manage and protect it. That's a durable long-term tailwind for our
business, and we intend to fully capitalize on it. Our technology road map is strong. Our customer
relationships are deep, and we have the operational discipline to translate this opportunity into
sustained earnings and free cash flow growth and long-term shareholder value.
With that, let me hand it over to Kris to walk you through the financials and our outlook for Q1.
Kris Sennesael (Executives)
Thank you, Irving, and good afternoon, everyone. Fiscal 2026 was an outstanding year for WD, driven
by broadening demand, deepening customer engagements and disciplined execution. We grew revenue
36% to $12.9 billion, while expanding gross margins 970 basis points to 49.1% and increasing operating
margins by 1,290 basis points to 37.3%. We more than doubled earnings per share to $10.22, and we
generated $3.5 billion of free cash flow, delivering a robust 27% free cash flow margin. We returned
$3.1 billion to shareholders, reflecting our confidence in the durability of the business and our
commitment to long-term value creation.
Let me now turn to our fourth quarter of fiscal '26. Revenue came in at $3.75 billion, up 44% year-over-
year on the back of strong exabyte growth and favorable pricing dynamics. Earnings per share grew
109% year-over-year to $3.56. Revenue, gross margin and EPS all came in at or above the high end of
the guidance range. We delivered 231 exabytes to our customers, up 22% year-over-year. Nearline
continued to drive our exabyte growth, complemented by solid non-nearline exabyte growth in the
quarter.
We began shipping the next-generation ePMR hard drives with capacities up to 40 terabytes in our
fiscal fourth quarter and expect a strong ramp over the next few quarters.
Cloud represented 89% of total revenue at $3.3 billion, up 43% year-over-year as demand for our high-
capacity nearline products was strong with a favorable pricing environment. Client represented 6% of
total revenue at $225 million, up 61% year-over-year. Consumer represented 5% of revenue at $187
million, up 38% year-over-year. Both segments benefited from improved pricing.
Gross margin expanded 1,310 basis points year-over-year to 54.4%, resulting in strong year-over-year
incremental gross margin. This was driven by a mix shift towards higher capacity drives, favorable
pricing across our portfolio and disciplined execution in our manufacturing operations. During the
quarter, the blended average year-over-year price increase per terabyte improved from high single
digits last quarter to high teens this quarter, reflecting the impact of our predictable and sustainable
pricing strategy as we deliver greater value to our customers.
Operating expenses were $382 million or approximately 10% of revenue, a 170 basis point sequential
improvement, demonstrating further operating leverage in the model. Strong top line growth,
expanding gross margins and leverage in the model drove operating income to $1.66 billion, up 126%

year-over-year, translating into a durable operating margin of 44.2%, up 1,610 basis points year-over-
year. Interest and other expenses were $10 million, and our effective tax rate was 16%.
Taking into account the diluted share count of 388 million shares, earnings per share was $3.56, an
increase of 109% year-over-year. Operating cash flow was $1.4 billion and CapEx was $108 million.
This resulted in free cash flow generation of $1.3 billion for the quarter and a strong free cash flow
margin of 34%. During the quarter, we completed the monetization of the remaining 1.7 million shares
of SanDisk, exchanging them for 4.8 million WD shares. Additionally, we repurchased 2.3 million
shares of our common stock for a total of $1 billion.
Our full year and fourth quarter repurchase numbers that we are describing on this call include $328
million to settle the conversion premium for some of our converts in cash rather than in stock, avoiding
the issuance of roughly 773,000 new shares. We also made $54 million of dividend payments, and we
ended the quarter with $1.1 billion of debt and $1.6 billion of cash, resulting in a net positive cash
position of $500 million. Lastly, the Board has declared a cash dividend of $0.15 per share of our
common stock, which will be paid on September 17, 2026, to our shareholders of record as of
September 8, 2026.
I will now turn to the outlook for the first quarter of fiscal 2027. We continue to operate in a strong
demand environment with improving longer-term visibility and favorable pricing dynamics across our
Cloud, Consumer and Client end markets. We expect revenue to be $4.1 billion, plus/minus $100
million. At midpoint, this reflects a growth of 45% year-over-year. Gross margin is expected to be in the
range of 55% to 56%. We anticipate operating expenses in the range of $390 million to $400 million.
Interest and other expenses are expected to be $15 million. The tax rate is expected to be 17%. As a
result, we expect diluted earnings per share to be $4, plus/minus $0.15 based on a non-GAAP diluted
share count of 388 million shares.
As we look ahead, we have high conviction in the drivers of demand, AI, cloud and the proliferation of
data-intensive workloads continue to accelerate. On the supply side, our industry-leading technology
and product road maps, combined with strong operational execution enable us to deliver substantially
more exabytes to our customers. This does not require spending CapEx to add unit capacity, but we are
making the necessary investments in our heads and media operations as well as in automation to
increase our productivity.
In summary, durable demand, disciplined supply and expanding margins position us to deliver
sustained earnings growth, strong free cash flow and long-term shareholder value.
With that, let's now begin the Q&A. Ambrish?
Ambrish Srivastava (Executives)
Thank you, Kris. Operator, you can now open the line to questions, please, and to ensure that we hear
from as many analysts as possible, please ask one question at a time. After we respond, we will give you
an opportunity to ask one follow-up question. Operator?
Operator (Operator)
[Operator Instructions] And our first question comes from C.J. Muse from Cantor Fitzgerald.
Christopher Muse (Analysts)

It's hard not to compare your results with your main competitor where they're seeing better sequential
top line growth and targeting gross margins nearly 200 bps higher than your September guide. So
curious what you make of this? Is that due to the earlier ramp of HAMR? Is it a difference in timing of
contracts, perhaps you're selling fewer bits into the open market? Would love to hear your thoughts
there and how you think about kind of gross margin acceleration from here? Do we need to kind of wait
for HAMR in calendar '27? Or are there other drivers that can allow you to push higher?
Tiang Yew Tan (Executives)
Thanks for the question, C.J. There are always quarter-to-quarter variations in terms of gross margin
because there's a whole range of factors that go into driving it. Obviously, timing of pricing in relation
to long-term agreement contracts is one. So there will always be timing differences of when existing
LTAs expire and new LTAs kick in with different pricing regimes. So that's one factor. Second will be
the introduction of next-generation platforms. So we're very excited that we started shipping in Q4
already up to 40 terabyte ePMR drives. Right now, we are very much on track to hit 50% of nearline
bits on that platform by third quarter of fiscal year '27.
So that will again will drive our ability to ship more higher capacity drives into the marketplace and
provide some additional upside opportunity from pricing as well. And obviously, we continue to work
on operational efficiencies like we normally do. So in short, there will always be quarter-to-quarter
variations, but we feel very confident with the things that I mentioned in terms of the pricing structures
that we have put in place with LTAs, the introduction of our higher cap drives coming out in the second
half of the year and our ongoing operational efficiencies that will lead to strong exabyte growth,
continuous top line growth and obviously, ongoing margin expansion.
Ambrish Srivastava (Executives)
Do you have a quick follow-up, C.J., which wouldn't be a multipart question, please.
Christopher Muse (Analysts)
Yes, of course. Marvell hosted a session at Flash Memory Summit talking about the economically
indispensable nature of HDDs in the AI data center. So curious with that as a backdrop, how is your
visibility kind of improved, and how do you think it could improve further as you start signing contracts
that renew?
Tiang Yew Tan (Executives)
Yes. Thanks for the question. Look, I think we have strong visibility and increasingly strong visibility,
it's being customer-driven to a large degree as well. The last time we reported on LTAs, we talked about
having one LTA of a large customer all the way up to calendar year '29. But we're very much in the
throes of discussions with customers to establish LTAs for calendar '29, '30 and '31 as well. So visibility
remains very strong, customer-driven demand for LTAs extending all the way out to '31 remains very
strong. So we continue to work on them. I think we have very good line of sight in terms of the exabyte
demand. What we're working through with them is more in terms of the pricing commercial construct
of what those LTAs would look like going forward.
Operator (Operator)
Our next question comes from Amit Daryanani from Evercore.

Amit Daryanani (Analysts)
I guess maybe the first one, is exabyte shipments were up about 21%, I think, year-over-year to 231.
That's below the 30% exabyte growth you folks have had in the last several quarters. Can you just talk
about, is this a temporary pause related to timing or supply? Or does this represent a more normalized
growth rate? And how should we think about exabyte growth through fiscal '27?
Tiang Yew Tan (Executives)
Yes, Amit. I think what we've guided to is that exabyte, we see demand growing at above 25%, right,
25% plus going forward. So we clearly have a road map that's designed to support that. There will,
again, as I mentioned, similar to margins, be quarter-to-quarter fluctuations in terms of exabyte growth
rates depending on the mix of products that we ship. And as we move into the second half of the year,
as we really ramp up the 40 terabyte shipments, as I mentioned, that will be over 50% of the nearline
exabytes we ship. We expect exabyte growth rate to accelerate. And then obviously, we have HAMR
coming on in the second half of the year and into calendar '27 as well at the 44 terabyte level.
Kris Sennesael (Executives)
Yes. And just to add, I think in Q4 exabyte shipments were up 22% year-over-year, and when you look
at it on a full fiscal year '26 exabytes were up 25% year-over-year.
Ambrish Srivastava (Executives)
Do you have a follow-up, Amit?
Amit Daryanani (Analysts)
I do. Just on the pricing side, right, price per terabyte went up pretty dramatically high teens year-over-
year, Kris, I think you talked about this. Can you just talk about how do you think pricing is going to
keep evolving from here? And maybe specifically the new LTAs that you folks are signing, are they
enabling this kind of high-teens pricing? Or is there more upside as we go forward?
Tiang Yew Tan (Executives)
I mean, I think we were beneficiaries of across the board pricing improvements, both in terms of our
nearline products and obviously, in the Client and Consumer space as well. In terms of the nearline,
especially with our large customers, we've been very consistent in talking about predictable pricing, and
that's a strategy we continue to adopt. This will give them visibility to ensure that they can make long-
term architectural decisions with the right economics to underpin that. So -- but even then as we
increase higher capacity drives, we provide better TCO value to them, that gives us an opportunity to
increase pricing, but you'll see that on a very predictable basis going forward. In terms of the non-
nearline space, particularly in our Client and Consumer space, we saw a higher opportunity to increase
pricing, predominantly driven by the pricing structures on alternative products that are flash-based as
well. So that resulted in a slightly higher pricing environment. Kris, do you want to -- anything you
want to add to that?
Kris Sennesael (Executives)
No, I think you summarized it well.

Operator (Operator)
The next question comes from Aaron Rakers from Wells Fargo.
Aaron Rakers (Analysts)
I guess kind of building on the prior 2 questions, it seems to me like you've got a product transition
dynamic going on with the 40-terabyte ePMR drives. If I look at your cost structure, it looks like you
saw a cost per terabyte that was more maybe flattish, down a little bit sequential. I'm curious, as we
move through this product transition, how should we think about cost per terabyte or cost of goods sold
per terabyte progressing through '27?
Kris Sennesael (Executives)
Yes. So Aaron, the cost per terabyte in Q4 of fiscal '26, the quarter that we reported was down
approximately 8% year-over-year. We've indicated before that cost per terabyte in the long term will
come down on or about 10% year-over-year. And the main driver, as Irving already explained, right, is
the move to higher capacity drives, better areal density, which gives us a substantial reduction on a cost
per terabyte. And as we execute in the near, mid and long term, execute on our technology road map,
execute on our product road map, introduce the next-generation ePMR and introduce our HAMR
products into the market, we will, over time, continue to see cost per terabyte coming down.
Ambrish Srivastava (Executives)
Do you have a followup, Aaron.
Aaron Rakers (Analysts)
I do. Maybe Kris, back to you. You've done a lot on the balance sheet, right? You've got a $1.1 billion left
on kind of the debt. You've got $1.6 billion in cash. I'm just curious, how are you thinking about the
capital structure from here? Is it pretty much 100% free cash flow return? Do you want to put more
debt on the balance sheet? I'm just curious if any updated thoughts on that.
Kris Sennesael (Executives)
Yes. No change there to our strategy and our commitment to return the free cash flow back to the
shareholders consistently with what we have been doing over the last 4 or 5 quarters through a
combination of our dividend payments as well as our share repurchases. And so we're fully committed
to those two programs.
Operator (Operator)
Our next question comes from Wamsi Mohan from Bank of America.
Wamsi Mohan (Analysts)
I was wondering, Irving, just if you could maybe drill down a little bit on the mix comment that you
made in the answer to one of the prior questions on the 22% exabyte growth because we previously
expected that there was room to deliver more exabytes in the quarter and the deceleration seems pretty
strong. So I was hoping maybe you can double-click a little bit on your mix comment. And at the same
time, you're expecting obviously an acceleration here in your comments, both on sort of a macro level
as well as from your product cadence perspective. So anything you could give us in terms of what is

changing in that mix very specifically, which caused maybe the slower growth in the quarter? I mean,
22% is pretty strong, but like definitely a deceleration and then further acceleration. Like is there a
near-term cap on that before you maybe start to ramp HAMR?
Tiang Yew Tan (Executives)
Yes. So thanks for the question, Wamsi. A lot of it, as you know well, we have very large customers. And
so different customers take different types of technology. So if there's a particular customer in a
particular quarter that takes a bit more CMR products, obviously, that will mean we ship a fewer bits
into the marketplace for the number of units that we have, right? And so in a different quarter where we
have customers that are more UltraSMR-heavy and for the same number of units, we're able to deliver
much more exabytes into the marketplace.
So there will always be variations quarter-to-quarter, and they don't buy on a very linear basis. It's a bit
lumpy. So you will see sort of quarter-to-quarter variations within that. But from a medium- to long-
term trajectory, we feel very confident about the ongoing exabyte growth, the ability to hit that 25-plus
percentage growth trajectory that we shared, both in terms of the 40-terabyte ePMR that we're ramping
up very aggressively. Then obviously, we have the 44-terabyte HAMR coming out in the first half of
calendar year '27, which will ramp. And then obviously, we've indicated in our road map, we will have
50-terabyte products coming out towards the second half of calendar year '27.
Wamsi Mohan (Analysts)
That's helpful, Irving. And then if I could just follow up. When you look at your quarter-on-quarter
gross margins from your guidance, not to beat a dead horse here, but year-on-year, you still are
suggesting pretty strong incrementals, I get that. But is there anything specific within, again, mix and
sort of pricing dynamic that is changing on a sequential basis? Or is the pricing dynamic something that
should persist and it's more about just sort of the mix that's creating maybe not further upside to the
gross margins?
Kris Sennesael (Executives)
Yes, Wamsi. So definitely, again, quarter-to-quarter, there's going to be variations. That's why I'm not
really fixated on my sequential incremental gross margins. I look more on my incremental gross
margins on a year-over-year basis. And just to put some numbers around that, right, in fiscal '25, on a
full year basis, our incremental gross margin was 60%. In fiscal '26, the fiscal year that we just ended,
incremental gross margins were 75% year-over-year, right?
Ending in Q4 with incremental gross margin year-over-year, 84%, 85%. And implied in the guide for Q1
is a year-over-year incremental gross margin of 80%, 81%. So I think we're executing really well on
driving incremental gross margins, further improving the gross margins. I have high conviction that we
will continue to improve gross margins for many quarters going forward based on everything what
we've explained. So there is very strong demand. We are moving to higher capacity drives that provides
more value to our customers, and that enables us to increase our price per terabyte, while at the same
time, driving down the cost per terabyte. And I think that's a great recipe for further gross margin
improvements.
Operator (Operator)

Our next question comes from Krish Sankar from TD Cowen.
Sreekrishnan Sankarnarayanan (Analysts)
My first one, Irving, clearly, your pricing is improving pretty well. You kind of mentioned customers
asking for LTAs into 2029, '30, '31. I'm just wondering, with 90% of your bits going into cloud and most
of them in LTAs and those LTAs extending longer, the velocity of price increases that we are seeing
going from high single digits to high teens last quarter and probably 20% in September quarter, would
that slow down because most are under LTA? Or do you think there's still flexibility where the velocity
of price increases could still increase?
Tiang Yew Tan (Executives)
Yes. Thanks for the question. As I pointed out, I think if you talk about the cloud business, as you
pointed out, quite a significant amount of it is under LTA. Obviously, not every LTA starts and ends at
the same time. So we will see price adjustments from LTAs even as we go through the fiscal year,
depending on when the contracts kick in with the new pricing. And it's obviously dictated by some of
the new platforms we introduced into the market.
And to reiterate our whole pricing strategy there, is to make sure it's predictable, and we give a lot of
visibility to our customer. Where we've seen a bit more ability to drive more rapid price increases has
been in the non-nearline space. If we fast forward that to what we are looking at in terms of what we are
discussing with customers on '29, '30, '31, we're working through the specific commercial constructs of
the LTAs, but we have a good line of sight and visibility to the volume requirements of our customers
that sort of further strengthen our conviction in that 25%-plus exabyte growth. What we're working
through is the pricing regime of how we would effect that for those years going forward.
So in short, I think there's still a lot of opportunity for us to deliver more value to our customers, deliver
better TCO and be able to benefit that through pricing as we've always stated that we would do.
Ambrish Srivastava (Executives)
Do you have a follow-up, Krish?
Sreekrishnan Sankarnarayanan (Analysts)
A quick follow-up for Kris. You kind of mentioned how the cost per terabyte downs are like probably
like high single digits right now, and you can get to like down 10% cost down. Is that in a post HAMR
qualification world? Or do you think that's something you can get to by the next few quarters?
Kris Sennesael (Executives)
So I have said in the past and repeat it today, right, that the mid- to long-term cost per terabyte decline
is on or about 10% year-over-year. If you look at it the last couple of quarters, we've been executing to
that, and I have high conviction again, over the longer term that we will be able to execute to that.
Again, there are always going to be some variations quarter-to-quarter, but mid- to longer term, and it's
all driven by our technology road map and our product transitions to higher areal density and higher
capacity drives that will bring down the cost per terabyte.
Operator (Operator)
Our next question comes from Asiya Merchant from Citi.

Michael Cadiz (Analysts)
This is Mike Cadiz for Asiya Merchant at Citi. So my first question is that given your LTA conversations
and of course, the visibility that they provide, can you perhaps talk about the types of workloads your
customers are planning to accommodate, be it Agentic or physical, et cetera? And how, if at all, the
workloads differ through time from LTAs encompassing more near term 2027 to LTAs and
conversations covering '28, '29 and even '30. Just wanted to see the progressions of workloads from
your perspective.
Tiang Yew Tan (Executives)
Sure. I think the bulk of the workloads remain the same. And there are a couple of growth drivers that
we see, and we are definitely getting visibility from customers. One, and first of all, something that's
underappreciated, core cloud services continue to grow as well, especially video-driven applications. So
a great example is the collaboration tools that many of us use each and every day. A lot of these video
meetings that we're on are getting stored at a very -- at an increasing rate that's driving a lot of more
storage demands and on core cloud services.
And obviously, in AI, the primary drivers over the last 24, 36 months have been model training and
development. And what we're seeing now and going forward is growth driven by inference, Agentic AI.
And actually, we're starting to see the early innings of growth being driven by physical AI as well. And
we are engaging with many large enterprise customers who are in the physical AI space, and we have
good visibility in terms of the growth trajectories in those areas as well.
So definitely growth coming from those vectors that I just shared. And on top of that, obviously, with
the introduction of our innovations like the high bandwidth drives that we have now sampling with 5
customers, that opens up the ability to also be able to deliver hard drive capabilities with the superior
economics that it has in higher bandwidth workloads as well. So we see that also as a future driver of
growth that we are very excited about that customers are engaging very closely with us on.
Operator (Operator)
The next question comes from Erik Woodring from Morgan Stanley.
Erik Woodring (Analysts)
Irving, last quarter, you mentioned starting to see some interest from sovereign and neocloud data
centers for nearline drives in your systems. Can you maybe just tease that out a bit more now that we're
3 months beyond that comment? Just what are they buying? How price sensitive are they? How big are
they? How big could they get, et cetera? And then a quick follow-up.
Tiang Yew Tan (Executives)
Sure, Erik. So it's a great question. I think we looked at that as an opportunity and that opportunity is
materializing today. And again, I would highlight three areas. We definitely see increasing demand
from neoclouds. Actually, even frontier AI labs are coming to us for supply. And as I just touched on to
the earlier question, physical AI companies.
So we've seen very strong demand from an autonomous vehicle company for more storage as they ramp
up their autonomous vehicle capabilities. We are seeing more demand for sovereigns, from neoclouds,
from AI frontier labs as well as they particularly see the economic benefits from hard drives and the

increasing storage demands that their business models are creating as well. In terms of pricing, I would
say they are in the very tight supply environment that we are in, that provides us an opportunity for
increased pricing leverage as well.
Ambrish Srivastava (Executives)
And Erik, you said you had a follow-up?
Erik Woodring (Analysts)
Yes. Just a quick one. Just a clarification, Irving, on your kind of pricing commentary. Is it -- am I
correct in that you have sequential pricing escalators in some of your contracted pricing? And just given
that demand has strengthened and you are adding more value to your customers now with these higher
capacity drives, is it the right way to think that these pricing escalators are accelerating? Or is that
maybe over extrapolating too much?
Tiang Yew Tan (Executives)
Yes, you're probably over extrapolating a bit too much, Erik. I would say that the LTAs obviously have a
base price associated to a base volume. And then as we're able to deliver upside to our customers, that's
subject to a different pricing construct. So that's generally what we've consistently said as a general
construct of how the LTAs are commercially organized.
Operator (Operator)
And the next question comes from Ben Reitzes from Melius.
Benjamin Reitzes (Analysts)
I wanted to ask you, given the product ramp and improving demand environment, should we expect the
first quarter fiscal to represent the low point for both sequential revenue growth and incremental
margins with acceleration as we move throughout the year with regard to FY '27.
Kris Sennesael (Executives)
Yes, Ben, as you know, we only guide one quarter at a time. And again, I think this quarter, we are
guiding to some strong sequential growth as well as year-over-year growth and some good incremental
-- strong incremental gross margins on a year-over-year basis. Again, we have -- based on the strong
demand environment that we see, based on our great execution on technology and product road map,
based on the fact that we are at the beginning of a ramp of the introduction of our new and -- new
generation of ePMR up to 40 terabytes followed then by our HAMR introduction, we have high
conviction that we can continue to ship a lot more exabytes at better pricing and driving down the cost
over time, which will lead to continuous strong revenue growth as well as further gross margin
improvement. And I'll leave it at that.
Ambrish Srivastava (Executives)
Do you have a follow-up, Ben?
Benjamin Reitzes (Analysts)

Yes. I was just wondering if you could tease out physical AI a little more. I mean I think that what might
be useful for investors is there's a ton of training video, but also synthetic video. And you're mentioning
it now more prominently than you did, I believe, in the prior quarters. And I was just wondering, did
something change? And how do you see that your tier being impacted by what's probably going to be a
surge in both synthetic and video data used to train these things?
Tiang Yew Tan (Executives)
Yes. Thanks for the question. And yes, we have highlighted it a bit more this quarter, specifically
because we're getting a lot better visibility from this space as well. I highlighted an example with
autonomous vehicle player where I would say that the increase in exabyte demand from them for this
calendar year -- or sorry, calendar year '27 has increased multiple fold, right? So we're definitely seeing
that.
And if you extrapolate that by the number of players in this space, you extend that to humanoids, you
extend that to industrial automation systems as well. And as I highlighted in the prepared remarks, in
many of these cases, they are generating new data from the tools and the vehicles that they are
collecting data from, but it's still insufficient to train their models as well. So they're also using the
existing data, feeding it into AI tools to generate synthetic data to further train the models and drive
reinforcement learning, and that's requiring a lot more storage data as well.
So the cycle that we saw in how model training development and inference was being created will
extend into what is happening into physical AI, but it's becoming very real now, and we see that being a
driver of growth '27 and beyond as well.
Operator (Operator)
And our next question comes from Karl Ackerman from BNP Paribas.
Karl Ackerman (Analysts)
I have 2 questions, if I may. First, how should we think about the gross margin delta today between
nearline versus non-nearline? I ask because given the greater ability to raise prices in the non-nearline
HDD market, I would imagine that gap closes. And then what share of these LTAs reprice for nearline
over the next 12 months?
Kris Sennesael (Executives)
So the gross margin between nearline, non-nearline, which includes Consumer and Client and all of
that, it's all in the same ballpark right now in the 5 zip code. So there's not a lot of differentiation there
anymore.
Karl Ackerman (Analysts)
Irving, obviously, hyperscale demand is robust. How large is on-prem enterprise now, and are you able
to sign LTAs with them, too?
Tiang Yew Tan (Executives)
Yes. Thanks for the question, Karl. I would say, again, that the vast majority of the nearline that we're
shipping are going to hyperscale customers. Increasingly, there's actually increased demand from
enterprise OEM players in the storage space, especially as they are pivoting to more hybrid-based

storage solutions where most recently, they were looking at all potentially 100% flash array systems.
There's a shift back towards hybrid systems that's driving more demand from us.
And so we are also factoring the forward-looking requirements into the projections that we're working
on in terms of supply that's giving us better visibility as well. And obviously, our engineering teams are
also working with them to be able to adopt our UltraSMR products and next-generation ePMR HAMR
products that will give them higher capacity drives and therefore, more exabytes faster as well.
Operator (Operator)
Question is from Ananda Baruah from Loop Capital.
Ananda Baruah (Analysts)
Irving, Kris, just was wondering what's a useful way to think about sort of the China hyperscale and the
China AI lab opportunity going forward with all the activity that's been going on there?
Tiang Yew Tan (Executives)
Yes. Thanks for the question, Ananda. I think the Asian market represents obviously a very exciting
opportunity for us. We've clearly been hearing and seeing a lot about the proliferation of AI frontier lab
models there that are open source. We think that's actually going to be good for the overall industry
because that's actually going to drive greater access to different models that will help to proliferate AI a
lot more with superior economics.
So depending on the use case, you can use different economic models to be able to drive growth and
value in the different applications. But at the heart of it, whether it's the traditional frontier models that
you've seen in the U.S. that are premium based or some of the new open source more economical
models, the underlying requirement is still that they're going to be able to require a lot of data to
support the training of these models. These models are going to generate a lot more data that requires
storage for us. So we view it as a very positive because even as compute -- maybe it drives greater
efficiency in terms of compute and memory resources, the requirement for storage is just going to
compound and grow. So we view it very positively for demand going forward.
Ambrish Srivastava (Executives)
A quick follow-up, Anand?
Ananda Baruah (Analysts)
Yes, quick one. And just dovetailing from there, the interplay between mixing up to meaningfully
higher areal density points counterbalance against we're at the front end of inference, which is the real
kind of killer use case for hard drives. And so how do you see those two things sort of impacting the
supply-demand gap in the coming years?
Tiang Yew Tan (Executives)
Well, we think the growth in inferencing will be positive in terms of the demand for higher capacity
drives because inferencing is actually going to generate even more data that's going to be required to be
stored both to support reinforcement learning and the fact that storing that context of data that's
generated is going to be more economical than rerunning it through compute and memory resources.
So we think actually as inferencing and Agentic growth is going to drive even more demand for storage

and the best way to deliver that storage with superior TCO and at the fastest rate is to deliver high
capacity drives, which is definitely something we're working towards delivering to our customers.
Operator (Operator)
This concludes our question-and-answer session. I would like to turn the conference back over to
management for any closing remarks.
Kris Sennesael (Executives)
Thank you. So at WD, as we look ahead to our new fiscal year and beyond, we do so with a very clear
sense of purpose. Our customers are counting on us to deliver storage infrastructure at scale and speed
that matches the pace and adoption of AI, and we are very much ready to that challenge. We're
confident that our technology leads, our execution is disciplined and the entire WD team remains
focused on delivering. So I want to really take this opportunity to thank the entire WD team for an
outstanding year to our investors and analysts for joining us today, and thank you for your time and
your continued confidence in Western Digital.
Operator (Operator)
The conference has now concluded. Thank you for attending today's presentation. You may now
disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### WDC_Q3_2026_Earnings_Call_20260430.md
- 2026-04-30｜CFO Kris Sennesael｜guidance：FQ4 營收指引 36.5 億美元±1 億（原話："revenue to be $3.65 billion plus/minus $100 million"）
- 2026-04-30｜CFO Kris Sennesael｜guidance：FQ4 毛利率指引 51%–52%（原話："Gross margin is expected to be in the range of 51% to 52%."）
- 2026-04-30｜CFO Kris Sennesael｜guidance：FQ4 EPS 指引 3.25 美元±0.15（原話："diluted earnings per share to be $3.25 plus/minus $0.15"）
- 2026-04-30｜CFO Kris Sennesael｜margin：FQ3 毛利率 50.5%，年增 1,040 bp、季增 440 bp（原話："Gross margin for the fiscal third quarter expanded to 50.5%."）
- 2026-04-30｜CFO Kris Sennesael｜margin：管理層用增量毛利率（約 70%–75%）說明毛利率可續升，並強調只指引一季（原話："very strong incremental gross margins in the plus 70%"）
- 2026-04-30｜CFO Kris Sennesael｜margin：毛利率超標的三大來源：定價、產品組合、成本；並稱定價並未全數鎖定（原話："not all the pricing going into the quarter is locked"）
- 2026-04-30｜CEO Irving Tan｜margin：每 EB 成本年降約 10%，並稱此為合理的看待框架（原話："we delivered 10% year-on-year"）
- 2026-04-30｜CFO Kris Sennesael｜margin：被問成本降幅是否加速，CFO 稱新產品改善將隨爬坡期分階段進入（原話："There is going to be an adoption curve, right?"）
- 2026-04-30｜CFO Kris Sennesael｜margin：FQ3 營收 33 億美元、年增 45%，營益率 38.6%（原話："revenue was $3.3 billion, up 45% year-over-year"）
- 2026-04-30｜CFO Kris Sennesael｜customer：雲端占營收 89%，年增 48%（原話："Cloud represented 89% of total revenue at $3 billion"）
- 2026-04-30｜CFO Kris Sennesael｜customer：出貨 222 EB，年增 34%（原話："We delivered 222 exabytes to our customers, up 34% year-"）
- 2026-04-30｜CEO Irving Tan｜customer：四大超大規模客戶需求型態大致相近（原話："No, I would say, in general, the profile is quite similar."）
- 2026-04-30｜CEO Irving Tan｜customer：合約年限已延伸至 2028–2029 年（原話："agreements now extending into calendar year '28 and"）
- 2026-04-30｜CEO Irving Tan｜customer：LTA 以 EB 為基礎並附一定價格；基礎量以外的量適用不同定價機制（原話："those LTAs are exabyte based with a degree of pricing"）
- 2026-04-30｜CFO Kris Sennesael｜customer：製造前置期約一年，採購單多提前一年下；一年後進入 LTA 架構、變動性較大（原話："So there is still a little bit more variability"）
- 2026-04-30｜CEO Irving Tan｜customer：UltraSMR 可擴及二線 CSP 與亞洲部分超大規模業者（原話："expand our reach into Tier 2 CSPs"）
- 2026-04-30｜CFO Kris Sennesael｜product：HAMR 目前有 4 家客戶在驗證，進度略超前原計畫（原話："Still a little bit of work to be done in terms of yield"）
- 2026-04-30｜CFO Kris Sennesael｜product：HAMR 預計 2027 年爬坡，良率與可靠度仍有工作待完成（原話："are on track to start volume production in the"）
- 2026-04-30｜CEO Irving Tan｜product：40TB ePMR 與 44TB HAMR 在驗證中；ePMR 2026 下半年量產（原話："are on track to start volume production in the"）
- 2026-04-30｜CEO Irving Tan｜product：預計 FY27 末約 60% 出貨 EB 採 UltraSMR（原話："close to about 60% of all the exabytes that we ship"）
- 2026-04-30｜CEO Irving Tan｜product：HAMR 取得主流比重的時點取決於可靠度與良率，未給目標數字（原話："We don't have a number that we are putting out there"）
- 2026-04-30｜CEO Irving Tan｜product：ePMR 良率維持在 90% 區間，目前良率與品質無變化（原話："they continue to be in the 90% range, right?"）
- 2026-04-30｜CEO Irving Tan｜product：高頻寬硬碟已送 2 家超大規模客戶試用，另有一家本季開始（原話："currently sampling with 2 hyperscale customers"）
- 2026-04-30｜CEO Irving Tan｜guidance：長期資料儲存成長率維持 25% 以上 CAGR 的信心（原話："growth will be greater than 25% CAGR."）
- 2026-04-30｜CEO Irving Tan｜guidance：每 TB 價格年增 9%，並稱 2026 下半年朝高個位數發展（原話："pricing was up 9% year-on-year."）
- 2026-04-30｜CEO Irving Tan｜competition：HDD 與快閃分工不同，目前未見重大架構轉變（原話："But we don't see any -- at this point, any"）
- 2026-04-30｜CEO Irving Tan｜competition：定價理念強調可預測性而非向上押注（原話："So we're not looking for it to be optimistic"）
- 2026-04-30｜CFO Kris Sennesael｜capital_allocation：賣出 580 萬股 SanDisk，債務減少 31 億美元，剩 16 億可轉債（原話："monetizing 5.8"）
- 2026-04-30｜CFO Kris Sennesael｜capital_allocation：FQ3 自由現金流 9.78 億美元，利潤率 29%（原話："free cash flow generation of $978 million for the quarter"）
- 2026-04-30｜CFO Kris Sennesael｜capital_allocation：股利每季由 0.125 提高 20% 至 0.15 美元（原話："free cash flow generation of $978 million"）
- 2026-04-30｜CFO Kris Sennesael｜capital_allocation：FQ3 買回 7.52 億美元（290 萬股），資本計畫啟動以來已回饋 22 億（原話："we have returned $2.2 billion to our shareholders by way"）
- 2026-04-30｜CFO Kris Sennesael｜commitment：資本配置框架不變：超額自由現金流全數回饋股東（原話："we have returned $2.2 billion to our shareholders by way"）
- 2026-04-30｜CFO Kris Sennesael｜commitment：剩餘 170 萬股 SanDisk 預計 2026 曆年底前以股換股、免稅方式處分（原話："We are returning all the excess free cash flow back"）
- 2026-04-30｜CEO Irving Tan｜commitment：目前不增加單位產能，聚焦面密度；視經濟性可能加碼磁頭與媒體投資（原話："at this juncture, we still do not see any"）
- 2026-04-30｜CEO Irving Tan｜commitment：目標在 2027 曆年底前讓所有主要客戶完成 UltraSMR 驗證（原話："We plan to have all of our major"）
- 2026-04-30｜CFO Kris Sennesael｜risk：新品導入有採用曲線，改善分階段進入，並只指引單季（原話："We plan to have all of our major"）

### WDC_Citi_s_2026_Global_TMT_Conference_20260909.md
- 2026-09-09｜CFO｜customer：CFO 表示約 90% 業務來自雲端，並稱不再是傳統週期而是長期成長業務（原話："90% of our business is with the cloud"）
- 2026-09-09｜CFO｜customer：客戶要求簽到 2030、2031 年的長約，但尚未簽署（原話："Customers are asking to sign LTAs all the way till 2030 and"）
- 2026-09-09｜CFO｜risk：被問及 AI 基建消化期，CFO 稱目前看不到消化（原話："So currently, we don't see a digestion."）
- 2026-09-09｜CFO｜guidance：CFO 稱未來 5 年 exabyte 需求年複合成長率大於 25%，目前供給無法超過 25%（原話："We can't supply more than 25% right now year-over-year"）
- 2026-09-09｜CFO｜guidance：CFO 稱營收受供給而非需求限制（原話："my revenue is not gated by the demand, my revenue is gated"）
- 2026-09-09｜CFO｜product：CFO 說明 FY26 exabyte 供給成長約 25%，其中一季為 34%，目前約 22%-23%（原話："we grew exabyte on or about 25% year-over-year"）
- 2026-09-09｜CFO｜product：CFO 稱目前處於兩個產品轉換之間，並列出 ePMR 40TB、HAMR 44TB、50TB+ 三個轉換（原話："We are now somewhat in between the next product transitions"）
- 2026-09-09｜CFO｜product：CFO 稱 80% 資料存於 HDD，並認為高效能 HDD 可侵蝕快閃記憶體領域，KV caching 是機會之一（原話："KV caching is one of the opportunities out there."）
- 2026-09-09｜CFO｜margin：CFO 稱每 TB 價格兩季前年增 9%、上季年增 18-19%，仍有上升空間（原話："Last quarter was up 18%, 19% year-over-year."）
- 2026-09-09｜CFO｜customer：CFO 稱客戶多要求提前 52 週下採購單，FY27 大部分已在長約下，FY28 部分、FY29 更少（原話："I think the vast majority of calendar or fiscal year '27 is"）
- 2026-09-09｜CFO｜customer：CFO 說明長約承諾基本量低於客戶需求，上行部分價格不同（原話："we commit to a certain base volume, which is typically less"）
- 2026-09-09｜CFO｜competition：CFO 稱 HDD 僅佔超大規模業者 capex 的 4%-5%，但為關鍵元件（原話："there is no AI without HDDs"）
- 2026-09-09｜CFO｜commitment：CFO 稱 HAMR 正與 4 家大型超大規模客戶認證，計畫 2027 年上半年開始出貨，Q1 少量、Q2 較多（原話："We're currently in qualification with 4 large hyperscale"）
- 2026-09-09｜CFO｜commitment：CFO 重申 HAMR 出貨時程：2027 曆年上半年起，Q3、Q4 持續放量（原話："we intend to start shipping in the first half of calendar"）
- 2026-09-09｜CFO｜competition：被問及競爭對手已推出 HAMR，CFO 稱客戶已熟悉 HAMR，但認證流程保守嚴謹（原話："It definitely helps a little bit that we are not the first"）
- 2026-09-09｜CFO｜product：40TB ePMR 上季少量出貨，本季開始放量（原話："we shipped a little bit last quarter. It will start ramping"）
- 2026-09-09｜CFO｜product：高頻寬硬碟已向 5 家客戶送工程樣品，目標 2 倍效能，將搭配 50TB 以上機種（原話："We are now targeting a 2x improvement on the performance"）
- 2026-09-09｜CFO｜customer：CFO 稱客戶資料中心規劃超過 5 年，因此想鎖定長達 5 年的供給（原話："This is a planned economy."）
- 2026-09-09｜CFO｜margin：CFO 稱毛利率已達 50% 中段、營業利益率達 40% 中段（原話："we are now in the mid-50s with operating margins now in the"）
- 2026-09-09｜CFO｜margin：CFO 稱看不到毛利率天花板（原話："is there a ceiling to the gross margin?"）
- 2026-09-09｜CFO｜margin：CFO 稱長期每 TB 成本年降約 10%，但並非每年每季，目前處於產品轉換間且 DRAM/NAND 等投入成本上升（原話："we will be able to reduce cost per terabyte on or about 10%"）
- 2026-09-09｜CFO｜risk：CFO 提到硬碟內使用的 DRAM 與 NAND 變貴，供應鏈整體有輸入成本上升（原話："we use a little bit of DRAM and we use a little bit of NAND"）
- 2026-09-09｜CFO｜guidance：CFO 稱近期毛利率仍將以相當快的速度提升（原話："gross margin will continue to increase at a pretty good pace"）
- 2026-09-09｜CFO｜capital_allocation：CFO 稱長期 capex 占營收 4%-6%，過去幾年低於此區間，未來幾年可能略高於（原話："the next couple of years, we might be actually slightly"）
- 2026-09-09｜CFO｜capital_allocation：CFO 稱 capex 主要投向讀寫頭、媒體碟片與自動化（原話："most of the CapEx spending goes to head and media as well"）
- 2026-09-09｜CFO｜commitment：CFO 稱自由現金流率目標為 30% 以上，且已有數季達到該水準（原話："Our target free cash flow margin is plus 30%."）
- 2026-09-09｜CFO｜capital_allocation：CFO 稱已完成 SanDisk 持股變現、清理大部分債務，仍在處理可轉債，目前為淨現金（原話："We've completed the monetization of the SanDisk shares."）
- 2026-09-09｜CFO｜commitment：CFO 稱剩餘可動用自由現金流全數回饋股東，以買回為主、股利為輔，並將持續調升股利（原話："The vast majority of the cash goes to the share buyback"）

### WDC_Special_Call_Western_Digital_Corporation_20260930.md
- 2026-09-30｜Marc Tanguay｜customer：產品行銷經理說明 HDD 是雲端資料中心的容量骨幹，且使用者互動資料很可能存在 WD 硬碟上（原話："HDDs are really the capacity backbone of everything digital"）
- 2026-09-30｜Marc Tanguay｜product：以 15 秒影片範例說明雲端 AI 產出 15MB 檔案需產生約 2GB 資料，約 125 倍（原話："So about 125x the actual output of the file size"）
- 2026-09-30｜Marc Tanguay｜product：說明本地 NAS AI 對儲存需求的影響小於 AI 資料中心（原話："You won't need as much storage at the local AI NAS level."）
- 2026-09-30｜Marc Tanguay｜competition：管理層定位本地 NAS AI 與雲端 AI 為並用而非取代（原話："you're not going to use your NAS AI to replace your cloud AI"）
- 2026-09-30｜Marc Tanguay｜product：說明 NAS 容量規劃方式因 AI 而改變，過去以 10–20% 超額配置估算，現在難以預估（原話："you don't know how much storage space you're actually going"）
- 2026-09-30｜Marc Tanguay｜product：WD Red Pro 與資料中心 Ultrastar 同產線、同硬體，僅韌體（NASware）不同（原話："the same drive that ends up being Ultrastar"）
- 2026-09-30｜Marc Tanguay｜product：Red Plus 規格：2–12TB、最多 8 bay、180TB/年工作負載、3 年保固（原話："It scales in capacity from 2 to 12 terabytes."）
- 2026-09-30｜Marc Tanguay｜product：Red Pro 規格：最高 20TB、550TB/年工作負載、250 萬小時 MTBF、7,200 RPM、5 年保固（原話："up to 2.5 million hours mean time between failure"）
- 2026-09-30｜Marc Tanguay｜customer：管理層稱高容量硬碟正被超大規模客戶大量買走，因此 Red Pro 一般可得最高容量為 20TB（原話："are buying all of our higher-capacity drives"）
- 2026-09-30｜Marc Tanguay｜guidance：對 NAS 通路容量供給的前瞻說法：20TB 將是常態可得的最高容量（原話："will be the highest regularly available capacity"）
- 2026-09-30｜Marc Tanguay｜customer：WD 與 UGREEN、QNAP、Synology 等 NAS 廠合作，並於加州 Irvine 設有 NAS 可靠性測試實驗室（原話："We operate what we call our NAS reliability and test lab."）
- 2026-09-30｜Marc Tanguay｜commitment：管理層表示將持續擴大 Red Pro 在 AI NAS 邊緣場景的使用，並維持與 Newegg 合作（原話："as we continue to grow Red Pro, its use"）

### 問答異常語氣（迴避／改口／保留）
- WDC_Q3_2026_Earnings_Call_20260430.md｜問：JPMorgan 問毛利率超標幅度為何大於營收超標、具體是什麼超預期｜答法：回答列出定價、組合、成本三項槓桿，未量化各項貢獻
- WDC_Q3_2026_Earnings_Call_20260430.md｜問：Goldman 問 2027 年底 HAMR 占出貨 EB 比重｜答法：明確表示不給數字，轉談降低客戶轉換風險的雙軌路線
- WDC_Q3_2026_Earnings_Call_20260430.md｜問：Morgan Stanley／JPMorgan 問毛利率指引是否保守、每 EB 成本降幅是否加速｜答法：兩次均重申只指引一季，以增量毛利率與三項槓桿作答，未給成本降幅加速的數字

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
{"date":"20260906","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤$350（≤11x FY2028E）且 ASP/TB 年增仍 ≥0 → 衛星首倉 1/3；或 CY2027 定價確認持平＋再有 2 家長約延至 2028 → 重跑 DD 升條件式","irr_base_pct":0.9,"ev5y_pct":7,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.23,"ev5y_pct":7,"irr_base_pct":0.9,"max_dd_pct":-65,"bull_5y_price":928,"bear_5y_price":156,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價 ≤$350（≤11x FY2028E）且 ASP/TB 年增仍 ≥0 → 衛星首倉 1/3；或 CY2027 定價確認持平＋再有 2 家長約延至 2028 → 重跑 DD 升條件式","price_at_dd":467.46,"archetype":"品質複利成長","cycle_position":"晚循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261013/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
