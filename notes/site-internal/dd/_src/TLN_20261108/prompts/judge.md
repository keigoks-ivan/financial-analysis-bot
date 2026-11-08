你是 stock-analyst **v20 判斷 agent**，標的 TLN（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TLN","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TLN_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TLN_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1327,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm"}},{"id":"f_kpi1_gaap","label":"營業利益（GAAP）","value":255,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm"}},{"id":"f_kpi2_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（公司定義，無 non-GAAP 營業利益揭露）","value":669,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm"}},{"id":"f_kpi3_gaap","label":"歸屬股東淨利（GAAP）","value":138,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm"}},{"id":"f_kpi4_adjusted_free_cash_flow","label":"Adjusted Free Cash Flow（公司定義）","value":433,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm"}},{"id":"f_kpi7","label":"發電量／容量因數","value":23.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"TWh","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm"}},{"id":"f_kpi8","label":"對沖比例（占預期發電量）","value":80,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"%（2026 Q4）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-03","period":"2026-11-03","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-03"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_tln_gross_margin_pct","label":"TLN 毛利率","value":42.67,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TLN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tln_operating_margin_pct","label":"TLN 營業利益率","value":15.33,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TLN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tln_fcf_margin_pct","label":"TLN FCF 利潤率","value":6.27,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TLN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ceg_gross_margin_pct","label":"CEG 毛利率","value":21.43,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CEG.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ceg_operating_margin_pct","label":"CEG 營業利益率","value":14.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CEG.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ceg_fcf_margin_pct","label":"CEG FCF 利潤率","value":0.99,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CEG.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vst_gross_margin_pct","label":"VST 毛利率","value":37.99,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VST.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vst_operating_margin_pct","label":"VST 營業利益率","value":19.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VST.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vst_fcf_margin_pct","label":"VST FCF 利潤率","value":11.74,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VST.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nrg_gross_margin_pct","label":"NRG 毛利率","value":18.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NRG.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nrg_operating_margin_pct","label":"NRG 營業利益率","value":6.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NRG.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nrg_fcf_margin_pct","label":"NRG FCF 利潤率","value":0.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NRG.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc_g_a","label":"SBC（損益表 G&A）","value":51,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm"}},{"id":"f_kpi6_2026_adjusted_ebitda_adj","label":"管理層指引：2026 全年 Adjusted EBITDA／Adj FCF","value":null,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm"},"needs_sonnet":true}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":338.64,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-12.35,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":49.79,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.99 → 16.99）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（27.7 → 27.7）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（39.62 → 39.62）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":16.99,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":27.7,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":39.62,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-20.38,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 21.34 → 16.99（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.29,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝47.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":47.6,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.35,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝57.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":57.9,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":19.93,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 16.99，分子＝快照價 338.64","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":9230.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 9569.0、現金 339.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":43.51,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":23962.64,"period":"2026-11-08","unit":"USD m","basis":"市值 14732.64 ＋ 淨負債 9230.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":4363.61,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（13 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":5056.96,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（15 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":5.49,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"-","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 338.64 / W52 353.96 / W104 317.07 / W250 None / W250 13週斜率 None%"},{"id":"f_ma_w52","label":"52 週均線","value":353.96,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":317.07,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 稱競爭受新進入者、新建電廠、補貼等影響；PJM 為競爭市場，部分州考慮重新管制，可能限縮競爭供應商機會。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000017/tln-20251231.htm","excerpt":"Competition is affected by electricity and fuel prices, grid congestion, government subsidies for new and certain existing generation facilities (including some which might otherwise retire), new market entrants, construction of new generation assets, technological advances in power generation, environmental and regulatory matters, and various other factors.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：競爭對手可能擁有更多資源、較新機組或較低成本；州或聯邦干預（補貼、公用事業電廠納入費率基礎）可能壓低容量與能源價格。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000017/tln-20251231.htm","excerpt":"Some of our competitors may have advantages over us through access to greater resources, newer generation facilities, lower costs, or more experience.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"PJM 市場監視者稱 Talen 收購 ECP 2.6GW 後控制約 13.1GW、為 PJM 第四大容量持有者；Constellation 收購 Calpine、Vistra 擬收購 Cogentrix，同業亦在擴張（摘自搜尋彙整，未讀原頁）。","source":"Utility Dive via Yahoo Finance: Reject Talen-Energy Capital power plant deal, PJM market monitor tells FERC","url":"https://finance.yahoo.com/sectors/energy/articles/reject-talen-energy-capital-power-093618488.html","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"10-K FY2025 風險因子：Talen 揭露對 RTO/ISO、PPA 交易對手、電力公用事業、金融機構、行銷交易公司與美國政府有信用集中度；未在此段列出單一客戶占營收百分比。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000017/tln-20251231.htm","excerpt":"Additionally, we are exposed to concentrations of credit risk from suppliers and customers among electric utilities, financial institutions, marketing and trading companies, and the U.S. Government.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Moody's 2026-04-20 將 Talen Energy Supply 無擔保債評等由 B2 升至 B1、擔保債由 Ba2 升至 Baa3；2026-04-01 展望由負面轉穩定、維持 Ba3 CFR。","source":"Moody's Ratings via researchpool","url":"https://app.researchpool.com/provider/moodys-investors-service/moodys-ratings-upgrades-talen-energys-debt-ratings-following-senior-un-ncaZAZfhJ5","excerpt":null,"as_of":"2026-04-20","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Talen 與 AWS 簽約約 1.92 GW Susquehanna 電力至 2042 年。","source":"thesis-lab TLN page","url":"https://thesis-lab.pages.dev/tickers/TLN/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"PJM 2028/2029 容量拍賣（2026年7月）再短缺約 6,831 MW；2027/2028 為首次全 RTO 未達可靠度要求（短缺約 6,623 MW，僅 774 MW UCAP 新增/擴容出清，價格達上限 $333.44/MW-day）","source":"PJM news release 2026-07-14; publicpower.org; renewableenergyworld","url":"https://www.pjm.com/-/media/DotCom/about-pjm/newsroom/2026-releases/20260714-pjm-capacity-auction-procures-138318-mw-of-generation-resources.pdf","excerpt":null,"as_of":"2026-07-14","retrieved_at":"20261108","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Talen–AWS 合約：Susquehanna 核電最高 1,920 MW 供應至 2042，約 17 年、名目約 $180 億；2026年7月投資人更新稱 2028 年後最低承諾階梯式增加，支撐 2029–2032 每股 FCF 年增 20%","source":"Talen investor update summary (Quartr); letsdatascience","url":"https://quartr.com/events/talen-energy-tlne-investor-update_FLNL3zFe","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"相反觀點：有來源指公用事業承諾約 100 GW 新容量至 2030，第三方估計實際需求僅約 50 GW，指向可能過度建設；渦輪機訂單可能 2028 才交付","source":"CreditSights podcast 'utilities the great data center overbuild'; DCD","url":"https://creditsights.podbean.com/e/utilities-the-great-data-center-overbuild","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 披露多件 FERC 共站（co-location）程序將形塑 FERC/PJM 對共站負載的政策；Susquehanna ISA 修正案上訴已於 2026-01 自願撤回、該案結案。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000017/tln-20251231.htm","excerpt":"FERC Co-Location Proceedings. Several consolidation matters before the FERC are likely to shape FERC and PJM policy around co-located load.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因素：Cornerstone 收購交割條件為無禁止性法令；公司目前未知有反壟斷訴訟，但不保證；協議終止日 2027-01-15，反壟斷／監管未決時可自動延至 2027-07-15。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000017/tln-20251231.htm","excerpt":"Although we are not currently aware of any, legal actions relating to the proposed Cornerstone Acquisition could be filed under antitrust, securities, or other laws.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"Talen 宣布 Lawrenceburg、Waterford、Darby 收購取得其餘監管核准：印第安納州委員會 5/27、FERC 6/1。","source":"Talen Energy IR 新聞稿","url":"https://ir.talenenergy.com/news-releases/news-release-details/talen-energy-receives-regulatory-clearances-lawrenceburg","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"PJM 市場監督人要求 FERC 駁回 Talen–Capital Power 電廠交易案，或附市場力承諾後重送。","source":"pulse.bot：Reject Talen-Energy Capital Power Plant Deal, PJM Market Monitor Tells FERC","url":"https://www.pulse.bot/energy/news/reject-talen-energy-capital-power-plant-deal-pjm-market-monitor-tells-ferc-873ec24b-0b72-4d5b-88f7-1aed644cf751","excerpt":null,"as_of":"2026-04-02","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#4","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"Freedom 與 Guernsey 收購取得 FERC 與 DOJ（HSR 等待期屆滿）許可。","source":"Talen 新聞稿：Regulatory Clearance for Freedom and Guernsey Acquisitions","url":"https://business.mammothtimes.com/mammothtimes/article/gnwcq-2025-11-18-talen-energy-receives-regulatory-clearance-for-freedom-and-guernsey-acquisitions","excerpt":null,"as_of":"2025-11-18","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Talen 10-K 風險因子：新增或提高的關稅、貿易限制可能實質墊高燃料、材料、設備、零件成本或影響取得，未量化；無出口管制／Entity List 相關內容。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000017/tln-20251231.htm","excerpt":"Any new or increased trade tariffs, restrictions, or controls, as well as any resulting delays or disruptions in global supply chains or shipping channels, could materially increase the prices we pay for, or negatively impact our ability to obtain, on a timely basis or at all, fuel, materials, supplies, equipment, parts, and (or) other products critical to our operations.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Talen 在 2025 Q1 法說會稱新建複循環電廠設備多自歐洲採購，關稅與供應緊張使新建更貴（利於既有電廠稀缺性）。","source":"Talen Q1 2025 earnings call (allmind.ai 摘要)","url":"https://allmind.ai/earnings/event/bt_TLN_2025_Q1","excerpt":null,"as_of":"2025-05-08","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因素：核燃料及其部分原料／零組件供應商數量有限，供應中斷可能造成非計畫停機或燃料成本上升；Susquehanna 燃料循環已簽約至 2028 換料，2029 年超過 50%、2030 年超過 20%。","source":"Talen Energy Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000017/tln-20251231.htm","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Talen 在 Q1 2025 法說會表示供應鏈吃緊與關稅（尤其歐洲採購設備）使新建電廠更貴、近期更難交付；產業面大型燃氣渦輪交期逾五年、大型變壓器交期可達四年。","source":"TLN Q1 2025 Earnings Call (allmind.ai); Utility Dive 5-year waits gas turbine","url":"https://allmind.ai/earnings/event/bt_TLN_2025_Q1","excerpt":null,"as_of":"2025-05-08","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Talen Q3 2026（2026-11-03 公布）：Adjusted EBITDA $669M、Adjusted FCF $433M，重申 2026 指引，2027 指引 Adj. EBITDA $2,500–2,850M、Adj. FCF $1,500–1,750M；ASR $1.5B，買回計畫上調至 $3.0B（至 2028-12-31）。分段營收 Q3 未取得；Q2 2026 能源及其他營收 $722M、容量營收 $237M。","source":"Talen Energy 8-K Q3 2026 earnings release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"PJM 2027/2028 容量拍賣（2025-12）連續第三年以價格上限結算，全 RTO 首度未達可靠度要求（缺口約 5.2%）；若無上限價格約 $530/MW-day（高約 60%）。2027/28 預測尖峰負載比上期高約 5,250 MW，其中近 5,100 MW 來自資料中心。","source":"Utility Dive / Power Engineering / NRDC 報導 PJM 2027/28 BRA","url":"https://www.power-eng.com/business/pjm-capacity-auction-hits-price-cap-again-as-region-falls-short-of-reliability-target/","excerpt":null,"as_of":"2025-12-17","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"2028/29 拍賣報導同樣達聯邦核准上限 $325/MW-day，並連續第二次未籌足所需容量（價格上限限制上行空間）。","source":"mychesco 報導 PJM capacity auction","url":"https://www.mychesco.com/a/news/business/pjm-capacity-auction-hits-price-cap-as-data-center-demand-strains-grid/","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"+","claim":"10-K 稱 PJM 新建發電排隊以間歇性電源為主、非可調度，且煤電持續退役；需求成長與供給增加不匹配（未提及替代技術取代 TLN 產品）。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000017/tln-20251231.htm","excerpt":"This demand growth is not currently well matched with increases in supply, as the PJM queue for new-build generation is predominately intermittent rather than dispatchable in nature.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Q2 2026 財報會議摘要：管理層主張併網（front-of-the-meter）供電長期優於表後（BTM）或新建氣電；Talen 不以表後為長期模式。","source":"GuruFocus 對 TLN Q2 2026 earnings call 摘要","url":"https://www.gurufocus.com/news/9009707/talen-energy-corp-tln-q2-2026-earnings-call-highlights-strong-cash-flow-raised-guidance-and-strategic-growth-in-data-center-pipeline","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"2026 年業界報導：Bloom 固態氧化物燃料電池（如 AEP 約 26.5 億美元、至多 1GW）與 SMR 被推為資料中心自備電力替代方案；多為聚合站/商業媒體，部分為框架協議，SMR 商轉多在 2030 後，未見直接指名 TLN。","source":"enkiai.com / cleaner-energy-solutions 等聚合報導（低權威）","url":"https://enkiai.com/data-center/fuel-cell-energy-sofc-off/","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Talen與Amazon的Susquehanna供電由behind-the-meter改為front-of-the-meter，Talen擔任Amazon的零售電力供應商，PPL負責輸配電；合約最高1,920MW至2042年。","source":"World Nuclear News｜New supply agreement expands Talen-Amazon partnership","url":"https://world-nuclear-news.org/articles/new-supply-agreement-expands-talen-amazon-partnership","excerpt":null,"as_of":"2025-06-11","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 2026法說：CEO稱持續持有低成本基載發電並轉為長約，強調彈性結構而非策略方向改變；除AWS外尚無新長約簽訂。","source":"Nasdaq/Zacks｜TLN Q2 Earnings Call Emphasizes Cash Flow and Data Center Strategy","url":"https://www.nasdaq.com/articles/tln-q2-earnings-call-emphasizes-cash-flow-and-data-center-strategy","excerpt":null,"as_of":"2026-08-08","retrieved_at":"20261108","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Talen 2026-11-03 Q3 8-K：Q3 Adjusted EBITDA $669M；2026 guidance 維持中點、區間各縮 $25M（Adj. EBITDA $2,050–2,200M、Adj. FCF $1,225–1,325M）；首度給 2027 guidance（Adj. EBITDA $2,500–2,850M、Adj. FCF $1,500–1,750M）；回購upsize至$3.0B（至2028-12-31）。","source":"SEC 8-K Talen Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 2026-07-31：共識評級 Moderate Buy，共識目標價 $476.45（9 Buy／4 Hold 為 07-29 預覽）；04-21 時平均目標價 $436.75；Intrinsic Alpha 頁共識 476.60、區間 411–510（日期不明）。","source":"MarketBeat 2026-07-31 / 2026-04-21 instant alerts","url":"https://www.marketbeat.com/instant-alerts/talen-energy-nasdaqtln-upgraded-to-strong-buy-at-zacks-research-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 2026-10-06 提示：8 Buy／3 Hold／1 Sell，平均目標價 $460.08；2026-08 Mizuho 以 Outperform、目標價 $405 首次覆蓋，當時共識約 $466.86。尚未找到 Q3 後（11-03 起）目標價調整。","source":"MarketBeat 2026-10-06 與 2026-08-24 alerts","url":"https://www.marketbeat.com/instant-alerts/price-talen-energy-nasdaq-tln-shares-gap-up-heres-why-2026-10-06/","excerpt":null,"as_of":"2026-10-06","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06-15 完成收購（Merger Agreement），現金約 25.5 億美元加 2,399,998 股普通股，以 2026-04 發行的 2031／2033 年到期優先無擔保票據資金支應","source":"SEC EDGAR 8-K Item 2.01 (2026-06-15)","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000048/tln-20260615.htm","excerpt":"On the Closing Date, the Company completed the previously announced Acquisition contemplated by the Merger Agreement. As a result of the Acquisition, the Acquired Companies became indirect, wholly owned subsidiaries of the Company.","as_of":"2026-06-15","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2025-11-25 完成收購 Freedom（約 15 億美元）與 Guernsey（約 23 億美元）電廠，以發行與新定期貸款 B 資金支應","source":"SEC EDGAR 8-K Item 2.01 (2025-11-25)","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253625000037/tln-20251125.htm","excerpt":"the Company paid approximately $1.5 billion in connection with the Freedom Acquisition and approximately $2.3 billion in connection with the Guernsey Acquisition.","as_of":"2025-11-25","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"10-K 法律程序：Susquehanna ISA 修正案上訴於 2026-01 自願撤回並結案；Winter Storm Uri 訴訟損失上限限於保險給付","source":"SEC EDGAR 10-K FY2025 Item 3 / Item 8","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000017/tln-20251231.htm","excerpt":"In January 2026, following approval of the CIR waiver request, the ISA Amendment appeal was voluntarily dismissed by Talen. This matter is now closed.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"CoBank 報告：燃氣渦輪 OEM 訂單積壓年底 2025 約 80 GW，未來兩年製造產能預期約 24 GW，新增氣電供給受設備瓶頸限制。","source":"CoBank, Waiting on Watts: The Gas Turbine Backlog Straining the Grid","url":"https://cobank.com/knowledge-exchange/power-plays/power-plays-s6e03","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Wood Mackenzie：2025 年渦輪製造產能利用率約 90%，部分美國開發商最早的新複循環併網時間可能到 2030 年或更晚；2026–2030 年氣電新增需求約 63 GW。","source":"Wood Mackenzie via search summary (gas turbine prices/backlog coverage)","url":"https://www.woodmac.com/press-releases/gas-turbine-prices-soar-195-as-market-faces-supply-demand-crisis","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"EIA 資料：開發商預計 2026 年併網 3.3 GW（過半已在建），2027 年 3.3 GW 多數尚未開工；2026 初在建氣電超過 29 GW。","source":"EIA Today in Energy (via ajot.com), Preliminary Monthly Electric Generator Inventory","url":"https://www.ajot.com/news/today-in-energy-electric-generators-plan-more-natural-gas-fired-capacity-after-few-additions-in-2024","excerpt":null,"as_of":"2025-05-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Talen 2026-01-15 宣布以 34.5 億美元向 ECP 收購 Waterford、Darby（俄亥俄）與 Lawrenceburg（印第安納）三座氣電廠約 2.6 GW，預計 2026 下半年初交割；屬購併擴張而非新建。","source":"Talen Energy 8-K / IR press release","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000004/a20260115pressreleasetalen.htm","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"PJM 2026/2027 容量拍賣價達上限 $329.17/MW-day（前一年 $269.92），Talen 清出 6,702 MW、約 $8.05 億容量收入","source":"Talen Energy IR / 搜尋摘要：PJM auction results 2026/2027","url":"https://ir.talenenergy.com/news-releases/news-release-details/talen-energy-reports-pjm-auction-results-20262027-planning-year","excerpt":null,"as_of":"2025-07-22","retrieved_at":"20261108","affects":["valuation","moat_trend"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Talen 10-Q：2026-09-30 煤炭庫存 $71M（2025 年底 $94M）、燃料庫存（發電用）$143M（年底 $151M）、總存貨淨額 $316M（年底 $278M）","source":"Talen Energy Form 10-Q (period 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000086/tln-20260930.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"Talen 2028/2029 PJM 拍賣結果","source":"Talen Energy reports PJM auction results for the 2028/2029 planning year","url":"https://www.barchart.com/story/news/3283997/talen-energy-reports-pjm-auction-results-for-the-2028-2029-planning-year","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"IEEFA 分析師指 AES、Calpine、Dynegy、NRG、Talen 在 2015 年股價下跌約 30%～66%（2014–2020 IPP 下行期）","source":"IEEFA, Independent power producers after tough 2015 will seek ways to stick ratepayers in new year","url":"https://ieefa.org/resources/independent-power-producers-after-tough-2015-will-seek-ways-stick-ratepayers-new-year","excerpt":null,"as_of":"2016-01-01","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Utility Dive 2019 稱 IPP 處境約三年前轉壞、之後幾無改善；投資等級最早在 2020 下半年或 2021 初才可考慮（下行期持續數年）","source":"Utility Dive, The cold truth: today's market conditions are hurting independent power producers","url":"https://utilitydive.com/news/the-cold-truth-todays-market-conditions-are-hurting-independent-power-pro/564592","excerpt":null,"as_of":"2019-12-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"TLN 自 2024 年上市以來最深回撤為較前高低 33.8%，2025-03-10 落底（回撤追蹤站數據）；本公司無 2014–2020 週期的獨立上市價格史","source":"ChartRow TLN drawdown / Trefis TLN","url":"https://chartrow.com/quote/tln/drawdown","excerpt":null,"as_of":"2026-11-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-06-15 完成收購，現金約 25.5 億美元加 2,399,998 股普通股","source":"SEC EDGAR 8-K Item 2.01 (2026-06-15)","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000048/tln-20260615.htm","excerpt":"the purchase price for the Acquisition consisted of (a) the Cash Consideration of approximately $2.55 billion, subject to customary adjustments for net working capital, cash, indebtedness, certain casualty losses and transaction expenses, and (b) the Stock Consideration of 2,399,998 shares","as_of":"2026-06-15","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"2025-11-25 完成 Freedom 與 Guernsey 收購，合計約 38 億美元","source":"SEC EDGAR 8-K Item 2.01 (2025-11-25)","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253625000037/tln-20251125.htm","excerpt":"the Company paid approximately $1.5 billion in connection with the Freedom Acquisition and approximately $2.3 billion in connection with the Guernsey Acquisition.","as_of":"2025-11-25","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K 列示 Winter Storm Uri 訴訟（前德州子公司）；最高賠償限於保險給付；搜尋未見證券集體訴訟","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1622536/000162253626000017/tln-20251231.htm","excerpt":"Pursuant to the Plan of Reorganization, Talen’s maximum potential damages on prepetition Uri claims are expressly limited to payments from Talen’s insurers.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"TLN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":42.67,"operating_margin_pct":15.33,"fcf_margin_pct":6.27,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TLN","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CEG","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":21.43,"operating_margin_pct":14.34,"fcf_margin_pct":0.99,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CEG","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"VST","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.99,"operating_margin_pct":19.38,"fcf_margin_pct":11.74,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VST","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"NRG","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":18.8,"operating_margin_pct":6.28,"fcf_margin_pct":0.95,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NRG","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"TLN"},"financial_history":{"ticker":"TLN","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2021-12-31","revenue":1775000000.0,"revenue_yoy_pct":null,"gross_margin_pct":13.58,"operating_margin_pct":-25.13,"net_income":-989000000.0,"diluted_eps":-2198.06,"free_cash_flow":-541000000.0,"fcf_margin_pct":-30.48,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2021-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2022-12-31","revenue":2412000000.0,"revenue_yoy_pct":35.89,"gross_margin_pct":31.92,"operating_margin_pct":4.31,"net_income":-1289000000.0,"diluted_eps":-2864.444444,"free_cash_flow":-125000000.0,"fcf_margin_pct":-5.18,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2073000000.0,"revenue_yoy_pct":-14.05,"gross_margin_pct":32.03,"operating_margin_pct":7.96,"net_income":998000000.0,"diluted_eps":17.67,"free_cash_flow":67000000.0,"fcf_margin_pct":3.23,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":2626000000.0,"revenue_yoy_pct":26.68,"gross_margin_pct":38.12,"operating_margin_pct":0.61,"net_income":-219000000.0,"diluted_eps":-4.79,"free_cash_flow":498000000.0,"fcf_margin_pct":18.96,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TLN/TLN_Q3_2026_Earnings_Call_20261103.md）

# Q3 2026 Earnings Call
**Talen Energy Corporation** | Earnings Calls | 2026-11-03

**Operator** (Operator):
Good day, and thank you for standing by. Welcome to the Talen Energy Corporation Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please be advised that today's conference is being recorded.
I would now like to turn the conference over to your speaker for today, Bill Appicelli.
Please go ahead.

**William Appicelli** (Executives):
Thank you, Lisa. Welcome to Talen Energy's Third Quarter 2026 Conference Call. Speaking today are Chief Executive Officer, Mac McFarland; President, Terry Nutt; and Chief Financial Officer, Cole Muller. They are joined by other Talen senior executives to address questions during the second part of today's call as necessary.
We issued our earnings release this morning, along with the presentation, all of which can be found on the Investor Relations section of Talen's website, talenenergy.com.
Today, we are making some forward-looking statements based on current expectations and assumptions. Actual results could differ due to risk factors and other considerations described in our financial disclosures and other SEC filings. Today's discussion also includes references to certain non-GAAP financial measures. We have provided information reconciling our non-GAAP measures to the most directly comparable GAAP measures in our earnings release and the appendix of our presentation.
With that, I will turn the call over to Mac.

**Mark McFarland** (Executives):
Thanks, Bill. Good morning, everyone, and thank you for joining us. Before we get into the quarterly results, I want to spend a few minutes on what we're seeing in the market, how we're thinking about the business and a few topics on investors' minds.
Talen is in a fundamentally stronger position today than at any point since we began rebuilding this company. Our financial outlook continues to improve. Our cash flows are becoming more durable, and we have more ways to create value than ever before. We own advantaged assets and advantaged locations in markets where demand is growing, supply remains constrained and the value of our reliable generation continues to increase. These assets would be extraordinarily difficult, expensive and time-consuming to replicate today.
Across PJM, we've seen a significant move in forward power prices and spark spreads this year. I know there's a debate about whether those levels are sustainable. Our view is straightforward. We don't expect markets to move in a straight line. There will be volatility, but we don't believe this is simply another commodity cycle. The underlying fundamentals have changed. Demand is growing, new supply is difficult and expensive to build and the timeline for bringing new generation online continues to stretch. The demand is here, the supply isn't, and we already own the assets the market needs. Now basis matters, congestion matters and how we hedge and manage our portfolio matters.
Our commercial team remains focused on managing those exposures and converting stronger market conditions into realized financial performance. We're seeing that translate directly into our financial outlook. Today, we're providing 2027 guidance, updating our '28 outlook and initiating our 2029 outlook. Focusing on the '29 outlook, our adjusted free cash flow is in the range of $56 to $60 per share. That outlook assumes no additional large load transactions. That's the cash-generating power of the business we've built, supported by our capital allocation strategy.
Additional large load contracting and powered land monetization represent upside. While the magnitude of the cash flow is important, so is its quality. Our objective is to generate more durable cash flow and grow that cash flow on a per share basis. That's what the Talen flywheel is all about. Strong assets in attractive markets generate significant cash flow. That gives us the flexibility to make high-return investments, pursue attractive long-term contracts, optimize our portfolio and return capital to shareholders, all while maintaining our balance sheet discipline.
Contracting can lock in attractive economics and reduce risk. Strategic investments can expand our earnings base and disciplined share repurchases can drive further growth and free cash flow per share. We're not dependent on any single lever to create value. We have several and they reinforce one another.
That's the power of the flywheel and it's working, which brings me to large load contracting and powered land monetization. I know there's a lot of interest in when we're going to announce our next data center transaction. So let me address that directly. We're actively engaged with customers across our footprint, evaluating a variety of commercial structures and working to bring additional transactions to fruition. We have existing generation infrastructure, interconnections and strategically located land. Those are all real advantages for customers trying to solve increasingly difficult power challenges.
Some need speed to power, some need reliability. Some need long-term price certainty. Increasingly, they need all 3. We can provide solutions ranging from long-term power contracts to powered land development and monetization. We don't have to build a position in these markets. We already have one, and we're going to be disciplined about how we monetize it. We are focused on creating value, not headlines. The objective is to lock in attractive economics, increase the durability of our cash flows and create lasting value for our shareholders.
We know what we own, we know what it's worth, and we're not going to compromise that value to meet someone else's timeline. That's not a lack of urgency. That's just discipline. Every attractive transaction we execute creates an opportunity to build on an already compelling financial outlook. We're negotiating from a power -- position of strength, not necessity, and that matters.
That same conviction is reflected in our capital allocation decisions. The $1.5 billion ASR is a tangible example. We believe in the value of the business and the ASR puts capital behind that conviction. Our cash generation gives us the flexibility to invest in the business and return capital to shareholders. We can advance large load contracting, monetize powered land, optimize our portfolio and repurchase shares. These opportunities aren't mutually exclusive. We're focused on maximizing value per share period.
All of this is happening against the backdrop of a continued regulatory and market design reform in PJM. There's considerable discussion around large load interconnections, reliability requirements, capacity market design, price caps and how the cost of serving new demand should be allocated.
We support reforms that facilitate load growth, maintain reliability, protect existing customers from inappropriate cost shifts and provide the economic incentives necessary to retain and build new generation.
But I'd make two points. First, the changing market rules doesn't change the underlying physics of the system. PJM needs more reliable generation to meet growing demand. That generation takes time and capital to develop, and the existing fleet needs to be maintained economically viable. Whatever market structure ultimately emerges has to recognize those realities. You can't regulate your way out of a physical supply shortage. You can change how the market compensates generation. You can't change the fact that the system needs it.
Second, we're not waiting for every regulatory issue to be resolved before moving our business forward. We're continuing to engage with customers, advance development opportunities and evaluate commercial structures in parallel with the regulatory process. Because we have multiple ways to serve large load customers, we believe we're well positioned to adapt as those rules evolve.
Regulatory uncertainty may change the path. It doesn't change the fundamental need for power or the value of the assets we own. Capacity market design matters and auction outcomes matter, and we'll continue to engage constructively in that process.
So let me close with this. We have attractive market fundamentals, an advantaged portfolio and a strategy focused on generating increasingly durable cash flows and growing adjusted free cash flow per share. And we're not done. We're working to capture additional value through large load contracting, optimizing our portfolio and returning capital to shareholders. We've built a company with multiple paths to create value and the financial strength to pursue them.
The strategy is working. The flywheel is working and the opportunity in front of Talen is substantial. As I look ahead to the leadership transition, I have tremendous confidence in Talen's future. Terry and the entire management team know these assets, understand these markets and have the experience and discipline to take this business forward.
One of the things that I'm most proud of is that we've built a company whose success isn't dependent on any one individual. We have the strategy, the culture and the leadership team to keep moving forward and creating value. I believe the best days for Talen are still ahead of us.
And with that, I'll turn the call over to Terry.

**Terry Nutt** (Executives):
Thank you, Mac, and good morning, everyone. Turning to our key highlights for the quarter. Our plants performed well during periods of strong demand, and I'm pleased to report that we delivered $669 million of adjusted EBITDA and $433 million of adjusted free cash flow in the quarter.
In September, we announced an increase in our share repurchase program to $3 billion through the end of 2028, including the $1.5 billion accelerated share repurchase previously announced. And when that transaction is completed, we expect to have repurchased approximately 1/3 of our shares outstanding since emergence just 3 years ago. That's a significant return of capital and a clear demonstration of our commitment to creating value for our shareholders.
PJM fundamentals remain strong. We saw continued improvement in forward spark spreads across ADHUB and PPL zones, where we have significant generation exposure. During the quarter, strong demand, tightening reserve margins and elevated outages across PJM drove increased run hours across our fleet. The market increasingly needs reliable generation. We own it, and we're seeing that value reflected in both our operating performance and our financial outlook. With 9 months behind us, we're reaffirming our 2026 guidance and introducing formal 2027 guidance. We're also increasing our 2028 outlook and initiating our 2029 outlook.
We expect to generate approximately $6 billion of cumulative adjusted free cash flow through 2029. And with continued disciplined capital allocation, we expect adjusted free cash flow per share to reach $56 to $60 per share in 2029, representing nearly a 30% annual growth rate from our original 2026 base. We have multiple opportunities to create additional value beyond that. The strategy is working, and we're executing.
Turning to Slide 3. For the 9 months ended September 30, 2026, we are reporting $1.516 billion of adjusted EBITDA and $995 million of adjusted free cash flow, numbers that validate the continued growth trajectory over the past several years.
Turning to our operational metrics. Our fleet achieved strong levels of safety and reliability during the year, including during the record-setting demand that PJM experienced during the third quarter. We generated approximately 53 terawatt hours of power with a capacity factor of 64% so far this year. Our intermediate dispatch assets continue to have increased run times to support the higher demand in PJM. We took time in September and October during the seasonal outage period for additional maintenance to ensure the fleet is ready for the winter.
We continue to make investments in our assets to ensure that our fleet meets the level of reliability and performance standards we expect. This will continue to be a focus for us through the coming years, especially as the market backdrop continues to point to tightening supply and demand for several years to come.
Safety remains our first priority across the fleet, and our year-to-date recordable incident rate was 0.31. I would like to thank the men and women of Talen who continue to demonstrate strong operational and safety performance. The team's commitment to operate in a safe and reliable manner is an important part of Talen's value proposition.
Turning to Slide 4. We have seen a continued appreciation in the forward curves through the next several years. While not as pronounced as the moves in PJM and West Hub, 2028 ADHUB and PPL spark spreads rose 19% and 11%, respectively, over the quarter, as you can see from the graph on the bottom right-hand side of the slide. On a year-to-date basis, 2028 ADHUB and PPL zone spark spreads both increased by nearly 30%.
Our views on PPL zonal basis remain unchanged. We continue to see this as an upside lever to our financial outlook as the combination of load ramping in the zone and completion of transmission network upgrades drive a narrowing of the zonal spread over time. In the meantime, our commercial team continues to deploy a hedging strategy around zonal basis that mitigates short- and near-term risk associated with price volatility. While larger macro factors like transmission build-out, line upgrades and load growth within the zones will impact the longer-term outlook.
Moving to Slide 5. The power demand outlook continues to remain strong. The 2 charts on the top of the slide show cumulative load additions for AEP and PPL zones. By 2031, AEP is estimated to have an additional 31 gigawatts of contracted large load additions. And PPL will have an additional 10.7 gigawatts. In the PPL zone, this includes 6 gigawatts of data centers currently under construction. We have assets and locations that are able to support the coming increase in load.
The increase in demand is illustrated in the lower left of the slide, where you can see the Q3 average electricity demand in PJM. 2026 demand was significantly above both 2025 and the 5-year average. Increased demand and higher prices result in higher run times for our intermediate fleet, as you can see on the bottom right. Compared to Q3 2025, the capacity factor for our intermediate fleet increased from approximately 36% to 52%. This continues the trend that we have seen over the past several years.
All of this validates our driving thesis: that large load growth is here and more is coming. It's notable demand and the desire for more long-term certainty has not been slowed by regulatory rulings as shown by recent transactions in the market. On the regulatory front, we view the Pennsylvania executive order as setting balanced standards for project development, and we are working with stakeholders to ensure future projects have a fair and measured approach.
We have a track record of working well with the state, as evidenced by the Susquehanna AWS transaction and intend to continue working to bring large loads and the related economic benefits to Pennsylvania. In addition, recent regulatory progress from PJM and FERC has been helpful, and we continue to see opportunities in the bilateral market as counterparties look for energy and capacity.
Turning now to our long-term contracting solutions. As Mac noted, we continue to work with customers to find the right solutions for their needs. We believe these offerings will continue to translate into value-enhancing contracts that leverage our assets. We have 6 gigawatts of baseload generation length across our portfolio that can support customers who desire price certainty and/or physical capacity commitments.
We have 4 gigawatts of powered land sites with significant speed to power advantages. These sites can be grid connected in the 2028, 2029 window and continue to advance. Sites with this timing and scale are very attractive to hyperscalers and large developers.
We also have a 3-plus gigawatt pipeline of new capacity projects under development, including uprates, batteries and peakers. Some customers specifically desire these types of projects to help either meet their ratepayer protection pledge or other corporate commitments. Additionally, Talen can offer both existing generation such as the 300 megawatts of uncontracted nuclear power from Susquehanna or one of the lowest carbon intensity combined cycle portfolios in the PJM fleet as well as new capacity options like multiple battery projects under development.
With that, I'll turn the call over to Cole to discuss our financial performance and outlook.

**Cole Muller** (Executives):
Thanks, Terry, and good morning. Terry described how stronger demand is driving higher dispatch across our fleet and outline the commercial opportunities ahead. And I'll focus on how these dynamics translate into cash generation, our financial outlook and value per share.
On Slide 7, third quarter adjusted EBITDA was $669 million and adjusted free cash flow was $433 million, nearly double what it was for the same period just a year ago. Year-over-year improvement reflects contributions from Freedom and Guernsey and beginning fully this quarter, Lawrenceburg, Waterford and Darby. We also benefited from higher settled power prices, greater generation volumes and increased cleared capacity revenues.
Realized hedge results partially offset these gains while acquisition financing increased cash interest payments. Our expanded fleet and stronger market conditions are translating into higher cash generation. That is the financial foundation for the per share growth Mac described earlier.
On Slide 8, we are reaffirming our 2026 guidance midpoint of $2.125 billion in adjusted EBITDA and $1.275 billion in adjusted free cash flow, and we have narrowed each range by $25 million on either side. We are also introducing our 2027 guidance, adjusted EBITDA with a $2.675 billion midpoint and adjusted free cash flow with a $1.625 billion midpoint. At these midpoints, this represents more than 25% growth over the 2026 adjusted EBITDA and adjusted free cash flow. This guidance reflects our larger portfolio and September 30 forward curves and that we are approximately 70% hedged for expected 2027 generation. For 2028, we are approximately 35% hedged. And in 2029, we remain largely open, except for the impact of the AWS contract.
Our commercial desk continues to manage zonal basis exposure as we approach the delivery year. As Mac emphasized, the investing case does not depend on another large load agreement. This guidance is grounded in the portfolio that we own today. Please see updated modeling assumptions and hedge disclosures in the appendix for more detail.
Slide 9 goes to our central measure of value creation, adjusted free cash flow per share. The bar shading distinguishes underlying cash generation from the incremental per share effect of future repurchases. Holding our share count constant at approximately 42.9 million shares following the completion of the ASR, our base guidance is approximately $38 per share of adjusted free cash flow in 2027, and our 2028 outlook has a midpoint of $48 per share. This 2028 base outlook has increased approximately 20% since just last quarter.
In 2029, we introduced an outlook range of $46 to $50 per share. We provide a range given we are still 3 years out. Our 2029 range midpoint is flat to 2028, overcoming Brunner Island shift to gas only and the backwardation in current forward curves, which declined by more than $2 per megawatt hour year-over-year. We mark our outlook to these curves rather than assuming a recovery in power prices. Applying our capital allocation assumptions, including repurchases funded with roughly 70% of annual adjusted free cash flow, our 2028 outlook grows to $53 per share and 2029 increases to a range of $56 to $60 per share.
This more than doubles our 2026 baseline of $26.60 per share outlined last quarter. At today's share price, our free cash flow yield is approximately 17% when looking out to 2029. Importantly, this outlook is just executing on the base business and does not require us to capture additional opportunities in front of us. These incremental opportunities represent upside to this outlook, and that is the distinction Mac made earlier. The base outlook can stand on its own with new contracting and powered land opportunities providing potential upside.
Slide 10 shows the magnitude of these potential upside levers on a free cash flow per share basis. The M&A and new data center contract upsides are illustrative impacts based on our recently announced transactions. Accelerating the AWS campus load ramp by 1 year would add approximately $2 of incremental adjusted free cash flow per share. We remain encouraged by the pace of development and see potential for the load ramp to exceed the existing contractual schedule, perhaps by multiple years.
Turning to the market sensitivities. Our outlook incorporates backward dated forward curves, as I mentioned earlier. A move to flat curves would represent approximately $2 to $3 per share of additional adjusted free cash flow with further potential if curves move contango. These are upside sensitivities, not assumptions embedded in our outlook. This also holds true for zonal basis. Every $5 per megawatt hour improvement in zonal basis across the portfolio corresponds to approximately $5 of an annual adjusted free cash flow per share.
These are illustrative and depends on transaction terms, timing and execution, but illustrate the additional growth potential of the business. Our test for every opportunity remains the same. Does it improve risk-adjusted value per share, relative to the alternative?
On Slide 11, we show how we are putting our capital discipline to work. In September, we expanded our share repurchase authorization to $3 billion through December 2028, including the announced $1.5 billion accelerated share repurchase.
The ASR is supported by our capacity monetization transaction, which brings forward contracted cash flows through May 2029. Approximately 3.8 million shares were retired upfront, and we expect to complete the ASR by the end of the first quarter of 2027 with the final share count subject to the discounted VWAP over the duration of the program. We continue to target returning approximately 70% of adjusted free cash flow to shareholders. Repurchasing our own shares remains the benchmark against which we evaluate other uses of capital, not a reason to pass on investments that offer superior risk-adjusted returns.
Across our outlook through 2029, we expect to generate approximately $6 billion of adjusted free cash flow. $6 billion to enable significant value creation opportunities for shareholders over the next few years. At our targeted allocation rate that supports more than $4 billion of aggregate repurchases, including the ASR, while retaining flexibility for strategic investments and balance sheet priorities. Balance sheet strength remains core to our framework, and we continue to target net leverage of 3.5x over the long term. Following the capacity monetization, we expect this obligation to amortize between June 2027 through May '29. Together with expected growth in the business, this supports our objective of returning to approximately 3.5x net leverage in the second half of 2027.
Slide 12 illustrates another part of the flywheel, the opportunity to improve cash flow durability through long-term contracting while retaining participation in attractive power markets. The objective is not simply to contract more megawatts. It is to lock in attractive risk-adjusted economics. The existing AWS agreement continues to ramp towards its full contracted level, which gets us to approximately 35% contracted gross margin.
Additional contracts could increase the contracted portion of gross margin and reduce reliance on future market conditions. We show the impact of another 2 gigawatts of premium data center deals, which would take us to 60% plus contracted with potential to meaningfully go further. These incremental opportunities are illustrative and not included in our base outlook. The overall combination, higher underlying cash generation, disciplined capital allocation and opportunities to contract at attractive economics is how we intend to compound value per share.
With that, I'll turn it back to Mac.

**Mark McFarland** (Executives):
Great. Thanks, Cole, and we're going to turn it back to the operator to open the line for questions at this point.

**Operator** (Operator):
[Operator Instructions] Our first question today will be coming from the line of Shahriar Pourreza of Wells Fargo.

**Shahriar Pourreza** (Analysts):
So Mac, Terry, just on the negative zonal basis in PJM, I mean, we do continue to see even further widening, especially after you guys marked on September 30. I guess what are you assuming is the normalization path there? And has that kind of been incorporated into the free cash flow figures for '27 and '28?

**Mark McFarland** (Executives):
Yes, Shahr, let me start on this, and then I'll turn it over to Cole to give you some details of what's in our numbers. We continue to think that the -- believe that the zonal basis is going to narrow over the next couple of years. And we think there's two primary drivers to that. One, obviously, we see load growing inside of PPL zone. We can see that very clearly with respect to the AWS Susquehanna campus that's going up today as well as other projects in the zone.
And then secondly, there's a significant amount of transmission upgrade work that's getting done. It's been -- that work started at the end of last year and continues into this year and goes into the next year. So we're confident that, that basis will narrow.
With respect to the numbers, let me turn it over to Cole, and he can give you some details on what's included.

**Cole Muller** (Executives):
So in terms of the impact for '27, '28, as I said earlier, our free cash flow guidance and outlook looks at just whatever the marks are. So for basis, we mark to our zonal pricing for all of our assets. And so that's already incorporated that widening basis as of 9/30, right? And so again, all these numbers are reflective of the 9/30 curve. And just as a reminder, as I said in the script, we're hedged 70% in '27 and 35% in '28, and our commercial desk is always actively working to minimize any exposure that we have on the zonal basis.

**Shahriar Pourreza** (Analysts):
Got it. Okay. Perfect. And then just on the 4 gigawatts opportunity, I know you noted that powered land is kind of the higher-value solution that you are marketing. I guess what's the right benchmark in terms of return on invested capital, especially relative to new build options and off-grid solutions?
So maybe another way to ask is how much margin above current market prices, which are obviously up significantly, does that solution require? And is it still kind of competitive?

**Mark McFarland** (Executives):
Shahr, it's Mac. Look, I think the monetization of powered land for us is a means to an end. The end being long-term capacity and energy contracts and how we service those off of a combination of what sometimes we describe as a hybrid model, which is bringing some new capacity from these additions that we have in a pipeline or selling our existing capacity and energy in combo or discretely against those powered land opportunities.
So we're not necessarily -- obviously, when we -- if we invest in acquiring land, we want to get a fair return for that acquisition. But that is a means to an end. We're not looking to create premium out of that. What we're looking to do is facilitate the ability to locate data centers, principally in the PPL zone for a lot of those that we've -- that we're advancing. And so our goal is to take those, combine them into a transaction with a long-term PPA, if you will, and create value off of our existing fleet plus potential capacity additions in a hybrid model.
So when we think about what a fair return for that hold is, we're -- first of all, we're not investing a lot of dollars in that. Let's just be clear. It's not like we're going out and investing hundreds of millions of dollars in these assets or billions of dollars in these assets. We're acquiring land that we hope to just get a fair sort of equity-type return on for the hold period. So I hope that answers your question. If you have a follow-up, it would be please let us know.

**Shahriar Pourreza** (Analysts):
No, no, that actually did touch it. I appreciate it, guys. That's all I had and terrific execution.

**Operator** (Operator):
Our next question is coming from the line of Matt Petitt of Barclays.

**Nicholas Campanella** (Analysts):
It's actually Nick Campanella on for Matt. Maybe just to dovetail off that last question, just with the end of the bilateral contracting window now being in February, I believe, can you just talk about your interest in participating that as an avenue? And just given the fact that you're talking about you can get people connected as soon as '28 now. I'm just curious, why would that not be the window to do deals now and net down this RBP requirement? Are there reasons we could be waiting past February? Could you talk to that a little?

**Cole Muller** (Executives):
Sure, Nick. It's Cole. As we've said before, we're not beholden to a specific timeline for our deals. And so obviously, the RBP window has been extended here. So as deals get done between now and when that auction is run, of course, there may be some additional netting. But we don't see the RBP timing as kind of driving hyperscaler decisions and our timeline necessarily. If deals get done within that time frame, great. We're obviously working on a bunch of opportunities, as Mac and Terry outlined. And when we've got something to talk about, we'll talk about it.

**Nicholas Campanella** (Analysts):
Okay. Great. And then maybe just with the BRA still on track for December, seemingly, this is the last one that's capped, I believe. Just what are stakeholders or yourselves advocating for as we kind of look forward to the spring in terms of keeping the cap or reevaluating this?

**Terry Nutt** (Executives):
Nick, I'll respond to that. Obviously, we've got the December auction coming up. Parameters are out there. I think most everybody has got a similar view that that's going to clear at a pretty high level all the way up to the cap at the end of the day. I think when we look towards the May auction, a couple of things from our vantage point.
One, we need to make sure that auctions continue to get executed on time, continue to move forward. I think that's one of the challenges that the market experienced several years ago when we got to the delay is -- we had a delay and then we had a price clear that was fairly high. There's discussion out there, rumors that maybe there's another price cap in the spring. We'll obviously participate in that discussion as it comes around.
But our biggest drive is we need to continue to have the auctions execute because at the end of the day, we think that's the primary the primary function of the market is to have sort of durability and certainty around those capacity revenues because that's ultimately going to be what helps finance new build and new generation.

**Operator** (Operator):
Our next question is coming from the line of Michael Sullivan of Wolfe.

**Michael Sullivan** (Analysts):
I wanted to ask maybe just -- hey, Terry, on Slide 10, when you list out the incremental value drivers, what would you say is your highest conviction one of being realized over the kind of near medium term?

**Cole Muller** (Executives):
Michael, this is Cole. Great question. Look, we outlined levers there that we think they're all great opportunities for them or else we wouldn't be talking about them. Obviously, some of them, we control more than others. The bottom 3 for sure, dependent on other parties, right, the market on the bottom 2 on sparks and zonal basis, data center build-out, which we don't control, but we -- as I said in the script, we see great progress. It continues to progress more than linear. I wish folks could get out there and see the site.
So that's a upside that we see that's tangible. But again, we don't control it. Obviously, deals, the top two, M&A and data center deals -- sorry, I got them flipped to the second and third one, but you get the point. Data center deals and M&A, there are stuff we can control somewhat, but obviously depend on good deals and willing counterparties. So all are good upsides. I know I'm not answering your question directly, but we see them all as potential here.

**Michael Sullivan** (Analysts):
Okay. Great. No, that makes sense. And just a follow-up on the acceleration of the AWS contract, I think you've got here going to 480 megawatts in the '28 guide. What is embedded in the '29 outlook?

**Cole Muller** (Executives):
Yes. So we don't embed any acceleration within the range. Obviously, as we accelerates and as we outlined for every year of acceleration, you can see a couple of dollars per share increase. So to get to the higher end of the range in '29 for sure, some of that acceleration could be helpful. But to get into that range, we're not dependent on any acceleration.

**Mark McFarland** (Executives):
It's the minimum commits basically of the contract, Michael.

**Michael Sullivan** (Analysts):
Okay. So I just want to make sure because I think there's a step function change there, if I remember correctly, like the original slides had 840 to 1,200 megawatts. So is 840 the right number to use there basically?

**Cole Muller** (Executives):
Yes. So the PPA does start to ramp faster once you get out to '29 because of the revamped deal that we did. And so they start moving from 120-megawatt increments to 360-megawatt. So the minimum commits out in '29, as we outlined a little over a year ago, do ramp to 840-megawatt in 2029.

**Operator** (Operator):
Our question will be coming from the line of Jeremy Tonet of JPMorgan Securities.

**Jeremy Tonet** (Analysts):
Just wanted to come back to Power land, if I could, and specifically for time to power. Just wondering if you could talk a bit, I guess, about the different types of solutions for resource there, battery, solar, fuel cell, smaller gen assets, where do you see, I guess, the best opportunities right now when focused on speed?

**Terry Nutt** (Executives):
Yes, Jeremy, I'll start and then Mac and Cole can chime in. I think, first of all, the interconnection to the grid in the 2028 time frame is really key for a number of customers, right? When you talk about large-scale reliability and what they want, getting that interconnection and getting it in a short amount of time is one of the highest priorities when we talk to hyperscalers and other developers.
The additional capacity resource, whether, as I mentioned in the script, to meet their ratepayer protection commitment or other sort of corporate commitments, it varies. There are some customers who are really keen on battery technology and storage technology. And that has been a topic of conversation that we've had with a number of counterparties. And then some are more interested in maybe a combination. I think one of the interesting things that we've noted and we'll reiterate here is at the end of the day, the solution matters, but the cost also matters.
I think that's been a misnomer in the market is that these hyperscalers or some of these large entities will pay any price whatsoever. You take a look at some of the inflation on large-scale generation technology, and it's been pretty sizable the last several years. And so we still think cost matters because ultimately it impacts what they pay for and what the affordability is. And so those solutions make a ton of sense as we're talking to customers.

**Mark McFarland** (Executives):
Jeremy, it's Mac. Let me tack on there a little bit. First of all, I think that the focus over the past year has been on land opportunities or data center sites that could be electrified '27, '28. And I think '29 is becoming the new '28 as we roll into next year. And so I think you'll see a focus, and we sit squarely with our land opportunities in that sort of '29 development time frame, which is what we've been trying to do in the background for the past years is to advance those.
I think the other thing that sometimes -- and I'll throw this a little nugget out there. I think one of the things that's a growing trend isn't that it's just new capacity additions in addition to existing contracting for capacity and energy off of existing assets, but also the opportunity to look at curtailment in terms of a PPA off of existing that can then satisfy the requirements.
Because if you think about it, if you can curtail, aka demand response, you can provide effectively something that looks like a peaker or a battery. It's just by having net negative load at that time or negative or 0 load at that time, providing that resource that then satisfies the hours that you're effectively developing a reserve margin across all of PJM 4. I think that's going to become a growing trend, and I think that's going to become -- the other growing trend is that '29 is going to be the new focus of data center development.

**Jeremy Tonet** (Analysts):
Got it. That's very helpful there. And then maybe just, I guess, pivoting when you talk about new deals, we've only seen nuclear so far. Just wondering how you think about the potential for other resources coming forward here in the future?

**Mark McFarland** (Executives):
They're coming. That's how we see it. They're coming, trust me.

**Operator** (Operator):
Our next question is coming from the line of Julien Dumoulin-Smith of Jefferies.

**Julien Dumoulin-Smith** (Analysts):
Look, maybe, Mac, you just said it yourself a second ago. Why don't we take it up a little bit on that curtailment subject because that's certainly a burgeoning subject. I'm glad to hear you talk about it. How do you think about cultivating that yourself as a business?
A, we have some of your peers that have these DR businesses embedded. But what I hear you saying is this is the curtailment of the actual load site. You don't need to develop a full DR suite of capabilities, I presume. How do you think about pivoting your business to enable that kind of contracting?
And when you say they're coming a second ago, is that sort of the principal vector for addressing additionality that you're thinking through today? Is that, that lens for it to be that pledge?

**Mark McFarland** (Executives):
Look, Julien, I would tell you that in addition to capacity additions, whether it be batteries, peakers, combined cycles that helps solve some of the so-called additionality requirement, which is really ill defined, by the way. But there are ratepayer protection pledges and people are thinking about how to meet some of these obligations. I think we've been talking for at least I've been mentioning this for a year that load management on the data center on the demand side needs to get better.
And in the past, it was -- you pop down a data center, you took power when you needed it, you didn't take power when you didn't need it and you didn't worry about any of the rest of it. But now when you're developing gigawatt or more than in Susquehanna's case, 1.9 gigs of data center development, you need to think about your load management. And I think that, that's a growing concern. And so we are advocating, and I think we would all take the position that PJM needs to come out with a new large load demand response product that's different than what I think you were mentioning with C&I.
The C&I type demand response stuff is stacking nickels and dimes to make a dollar. These things are dollars themselves and need to be -- need to have a different construct. They need to be paid for it. So that's the carrot as opposed to the stick of like an IRAS. You know that we were never supporters of IRAS. We talked about that. and we think that it's discriminatory and all the other pieces. But if you could voluntarily subscribe to a demand response that was equitable and fair and paid appropriately and then, I'll call it, dispatched appropriately within the response by PJM, that is a solution that can be one of the most economic to solve some of these issues with respect to reliability and the capacity market.
So when Terry was talking about the capacity market reforms, one of the things we'd like to see is how does demand response fit in there. I think we started to see a rationalization of load forecast. You saw that most recently going into this auction about what the load forecast will be, what will be the requirements of the RBP, et cetera. So we're starting to get real sort of rationalized supply -- demand forecast. Now let's add load management to those demand forecasts and get real about what is the right solution there. And I think there's a growing consensus that demand response is going to solve some of these issues.
But I don't think it's akin to the C&I that you described there. I think it's something different because it's much larger. It needs to be managed not real time, somewhat longer in advance. So it's either a day ahead DR or a week ahead type DR response because people need to know how to shut down a gigawatt.
So I can give you an example, like Terry and I, when we were working in ERCOT, there's a big assembly line in Fort Worth that was a big 50 megawatt. That was a big demand response asset that provided optionality. That's 50 megawatts. That was huge. Okay? We're talking gigs here and people that are managing the gigawatts or greater than gigawatts of load need to have a signal further in advance. So we're out pushing and advocating for a demand response product to be incorporated in long-term capacity reform.

**Julien Dumoulin-Smith** (Analysts):
Yes. No, thank you for elucidating on that point because I think that's what I was trying to tease out is the difference from the new versus the old DR paradigm. If I can, just to follow up a little bit, like I'm trying to read between the lines on the leverage target. You say an ability to achieve 3.5 net leverage target by the back half of '27. I don't know if that's an incremental take on your prior commitment.
And really, what I'm trying to get at there is how do you think about deploying the balance sheet? Obviously, we see the ASR here. But how do you think about deploying strategically? You went back to this contract by philosophy earlier. Where are we in potentially going back in and diversifying the portfolio further? And again, maybe I'm trying to read too much into some of the credit commentary here, but it would seem as if there's a litany of different permutations that you could evaluate here that would diversify you in different directions from what you have today?

**Terry Nutt** (Executives):
Julien, yes, it's a good question. It's a good point. Obviously, we view the balance sheet as a key part of our strategic options, right? We've -- as we've done in the past, we've taken the opportunity to take leverage up slightly to do really accretive transactions for the business, and we'll continue to focus on it.
Our 3.5x net leverage target is a target. Obviously, we went up a little bit above that to do this most recent acquisition. And the idea is, okay, let's get back to a level to where we can sort of redeploy it again. I think we'll always look at how to utilize that in any part of our strategic alternatives, whether it's in the M&A space or the share repurchase space or other ways to grow the business and ultimately grow free cash flow per share.

**Cole Muller** (Executives):
And Julien, just as Terry said, when we've done these -- the last 2 acquisitions, we've temporarily gone above the target, but with line of sight to get back down. And we meaningfully did that this quarter post the Cornerstone acquisition. The comment in the script around second half '27 is reflective of a lot of folks are going to treat the capacity monetization as short-term debt. And so as that amortizes, we'll get right back down to 3.5x this time next year going forward.

**Mark McFarland** (Executives):
Yes, you just -- you were asking a question about diversification. I mean, look, we like the position we're in. Let's not forget that we sold the ERCOT assets a couple of years ago, recycled that capital into share repurchases at a time that now in hindsight, that doubled up the value that we sold those assets for. We are more than doubled, as I'm reminded here in the room.
So I was being conservative there. But look, that -- we like the position that we've concentrated in PJM. We like the exposure to PJM. We diversified through 2 acquisitions of over $7 billion and toggled the balance sheet to do so, toggled equity issuance to do so. So we remain flexible across all of those things, and I think we remain disciplined with respect to maintaining our balance sheet. But at the same time, we're willing to lean in and toggle those different aspects when we find the right opportunities. And so we'll do that in the future if we find a new one, too.

**Operator** (Operator):
Our next question is coming from the line of Angie Storozynski of Seaport.

**Agnieszka Storozynski** (Analysts):
So my first question is we're hearing a lot about the return on investment for data centers and how sensitive the hyperscalers are becoming to the cost of these investments and how big a component of that is power. So we're just wondering how that is reflected in your discussions about what type of power source hyperscalers want. I mean we've all been waiting for announcements about contracts for combined cycles. Those are not coming seemingly or at least they haven't come yet.
And just wonder how you're positioned vis-a-vis this new increased sensitivity on the cost side for hyperscalers?

**Mark McFarland** (Executives):
Angie, it's Mac. That's a great question. We've always said, I think, that there's price sensitivity by the hyperscalers. A lot of people have said, well, they'll just pay anything because it's irrelevant. But we've always said that they're price sensitive. Cole has been saying that for years. And we're very much attuned to that.
And I think that's why when you look at some of the solutions, and I'll just go through a couple quickly. First of all, you're looking north of $120 all in a megawatt hour for a combined cycle, new combined cycle. And that -- those costs aren't going down. They keep going up anytime you read them. And so I do think -- and maybe just to mention it quickly, the demand response piece that I was articulating earlier or batteries or some other new capacity with existing gen is a much more economic solution. So we remain focused there.
I think a lot of people have talked about the behind-the-meter solutions, which I do think that because of speed to power and sort of '27, '28 delivery, there's been a move into the behind the meter. But all -- every time we talk to people, there's a reason why to be grid connected. It's much more reliable. It in the long run is lower cost. And so we're focused on grid-connected front-of-the-meter solutions, providing some form of additionality either through our backlog and new capacity or in figuring out this demand response aspect of things.
So I do agree with you that there's price sensitive. We've always been in that price-sensitive camp and attuned to it. And so the solutions we're providing, we think, fit within that, and that's why we've targeted them.

**Agnieszka Storozynski** (Analysts):
Great. And a little bit of a different topic. So if you're looking at power flows like exports and imports within PJM, it's pretty clear that the load growth is primarily in the Dominion zone, at least for now, and that is a zone that continues to attract more and more imports from outside of Virginia.
So I mean, is it just that we are still waiting for these data centers to be energized in Pennsylvania and Ohio, those two states that seem to attract most debates about the power position? Or what is driving that? Again, it just feels like the import of -- into Virginia continues to grow at a pace which is just not comparable to any other state.

**Mark McFarland** (Executives):
Well, yes, I think you're right with respect to Northern Virginia, okay, or Dominion zone. And that's where a lot of this transmission that we think is going to get built over the next couple of years will help. In fact, there's one particular line. I can't remember the name of it, Chris probably knows. But -- so -- but those projects have been started. When you drive through Loudoun County, which I did within the past year, when you go through, you'll see projects that are being completed. Those things were started a long time ago. And so that's why you see those energized.
But I do think that those projects are being built in Pennsylvania. I know that when we recently -- Terry and I and Brad, our Chief Operating Officer, were recently on the road, and we went to all of our sites in Ohio. And as we drove into Columbus, you can see the data centers being built there live on the ground, just like if you look -- if you come up to Susquehanna, you can see in Berwick, you can see what's going on there. And there was just another site approved in Salem Township recently, I think last week on the 28th or something like that.
So they're coming. It's just that I think Northern Virginia had a head start and they're just completing projects. I think Columbus and the surrounding areas in Ohio have a head start and they're completing projects. And so those will be energized just like the AWS contract. So I think that you're right with respect to Loudoun County, but I also think they're coming in Ohio, and I think they're coming in Pennsylvania.

**Terry Nutt** (Executives):
Yes. And Angie, maybe to add to Mac's comments on that. I think the other thing that we see is when you look at interconnection, which once again goes back to a key that the hyperscalers and the developers want, you get into some zones like Dominion where the transmission build-out is there's just not a lot of ability to do anymore.
But then you take a look at PPL and different zones like AEP, and they've got the ability to build out more transmission PPL, for example, already has done that, which is why you see a lot more focus in that market because there is the ability to get connected to the grid faster for reliability. So we think that, that advantages the grid and advantages the assets that we have there, and that's why we expect to see more load growth. And obviously, we've got materials in the slides that show the projections for those two zones over the next several years, and we continue to have a strong belief that it will accelerate.

**Agnieszka Storozynski** (Analysts):
Yes. And just one other question, completely unrelated. If you guys could explain to us what are -- how do we actually understand the uprates of gas plants? Because I think we're all used to like very small capacity increases like anywhere between 3% to 5%. We see them being pursued, for example, by Capital Power on some of the assets that they recently acquired. So when you guys talk about upgrades of your assets, what kind of a percentage of the installed capacity are we talking about as a potential increase? And what do they entail?

**Cole Muller** (Executives):
Angie, it's Cole. Look, as you said, there's a lot of different upgrade opportunities across the asset base, not just ours. Obviously, there's nuclear upgrades. We've said we've done the larger ones. And so we have a relatively small number of upgrades at -- on the gas side, combined cycles, depending on the vintage, have different upgrade capabilities, and they're all in different stages of that. So there's not one percentage.
There's also opportunities to convert simple cycle to combined cycle. Those have meaningful larger percentages because you're kind of, let's call it, just doubling the size there, rough numbers. So we're evaluating all those opportunities and think that there's attractive opportunities to do those on a cost-effective basis relative to new build and also from a time frame standpoint on the execution front. So...

**Mark McFarland** (Executives):
Look, Angie, we have a couple of hundred megawatts or more across our fleet. And you're right, when it comes to the gas plants, particularly when you go back to the F frames, you're talking about doing these -- I think we're 0.04s right now, and there's a 0.05 upgrade and you get those smaller percentages. But those come around like every 3 to 5 years from GE to upgrade and squeeze more megawatts out. So those are the kind of upgrades that you're looking at. That's absolutely right.

**Operator** (Operator):
This does conclude today's Q&A session. I would like to turn the call back to Mac for closing remarks. Please go ahead.

**Mark McFarland** (Executives):
Great. Thank you. Thanks, everyone, for joining us, and I appreciate your interest in Talen. We've got a bright future ahead of us, and we look forward to continue to execute. Thanks again. Take care.

**Operator** (Operator):
Thank you. This concludes today's program. Thank you so much for joining. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TLN_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜guidance：2026 調整後 EBITDA 財測區間上調（含 Cornerstone、市場更新、Keystone 出售抵減）（原話："EBITDA range for 2026 has increased to $2.025 billion to"）
- 2026-08-05｜CFO｜guidance：2026 調整後自由現金流財測區間上調為 12 億至 13.5 億美元（原話："free cash flow range to $1.2 billion to $1.35 billion"）
- 2026-08-05｜CFO｜guidance：2027 基準情境 FCF/股維持 34 美元，2028 升至 40 美元（原話："outlook remains $34 per share, increasing to $40 per share"）
- 2026-08-05｜CFO｜guidance：計入買回後，2027 FCF/股約 37 美元（原話："forecast 2027 cash flow at approximately $37 a share"）
- 2026-08-05｜CFO｜guidance：Cornerstone 交易宣布時給的 2027 pro forma EBITDA 約 26 億，本次表示已超過（原話："pro forma 2027 EBITDA of approximately $2.6 billion"）
- 2026-08-05｜CEO｜guidance：財測節奏：每年秋季給下一年度財測與後兩年展望（原話："provide guidance for the upcoming year each fall"）
- 2026-08-05｜President｜guidance：2028 PPL 與 ADHUB 遠期 spark spread 較 2025 年 7 月投資人日價格上升（原話："2028 PPL spark spreads are up 28%,"）
- 2026-08-05｜President｜guidance：管理層指出 PPL 基差擴大原因之一為南向輸電工程停電（原話："Two main drivers will work to compress that basis"）
- 2026-08-05｜President｜margin：PPL 相對 West Hub 折價由約 9 美元擴大到約 20 美元/MWh（原話："we have seen the basis grow to approximately $20 per"）
- 2026-08-05｜CFO｜margin：基差敏感度經驗法則：每改善 1 美元約增加 1 美元 FCF/股（原話："every $1 improvement in zonal basis across our portfolio"）
- 2026-08-05｜CFO｜margin：財測已採用反映擴大基差的 PPL 現行遠期價（原話："recent PPL marks that reflect the widened basis"）
- 2026-08-05｜CFO｜margin：AWS 滿載後長約毛利占比由 10% 升至 35%（原話："our long-term contracted margin increases from 10% to 35%"）
- 2026-08-05｜CFO｜margin：假設再增約 2GW 同類長約，示意毛利組合長約占比可達 60%（原話："60% of our gross margin mix under long-term contracts"）
- 2026-08-05｜President｜margin：年初至今 FCF 轉換率落在 60% 中段（原話："free cash flow conversion rate in the mid-60% range"）
- 2026-08-05｜CFO｜margin：Cornerstone 資產位於 ADHUB 而非 PPL，說明 2028 展望上調需同時看兩區（原話："those Cornerstone assets are in ADHUB and not PPL"）
- 2026-08-05｜CEO｜margin：本季調整後 EBITDA 3.74 億美元（原話："we delivered $374 million of adjusted"）
- 2026-08-05｜CEO｜capital_allocation：Q2 回購 55 萬股，維持把 70% 調整後 FCF 回饋股東的目標（原話："committed to our target of returning 70% of adjusted"）
- 2026-08-05｜CFO｜capital_allocation：預計至 2028 年底回饋股東至少 70% 的 FCF，共 28 億美元（原話："returning at least 70% of this cash, $2.8"）
- 2026-08-05｜CFO｜capital_allocation：現有買回授權剩 17 億美元，後續需董事會核准（原話："has $1.7 billion remaining"）
- 2026-08-05｜CFO｜capital_allocation：買回後仍有逾 13 億美元超額現金供其他用途（原話："This leaves more than $1.3 billion of excess cash"）
- 2026-08-05｜CFO｜capital_allocation：淨槓桿目標維持 3.5 倍（原話："continuing to target our net leverage ratio at 3.5x"）
- 2026-08-05｜President｜capital_allocation：併購以股票回購為門檻比較基準（原話："the share repurchase program is our hurdle"）
- 2026-08-05｜CEO｜capital_allocation：管理層稱曾用發股、舉債等工具做併購（原話："we've been flexible. We've issued shares to do deals."）
- 2026-08-05｜CEO｜capital_allocation：6 月完成 Waterford、Darby、Lawrenceburg 收購（原話："we closed on the Waterford, Darby and Lawrenceburg plants"）
- 2026-08-05｜CFO｜capital_allocation：Keystone 權益出售待完成，已反映於財測（原話："offset due to the pending sale of our interest in Keystone"）
- 2026-08-05｜CFO｜commitment：管理層承諾資本紀律，聚焦增加每股 FCF 的槓桿（原話："we will continue to maintain capital discipline"）
- 2026-08-05｜President｜commitment：新增容量專案須先達門檻報酬才會推進（原話："we'll have to clear the right hurdle"）
- 2026-08-05｜CEO｜commitment：不做 behind-the-meter 方案（原話："The one we're not doing is behind the meter."）
- 2026-08-05｜CEO｜commitment：管理層表示不預期未來頻繁更新多年展望，除非有重大業務變化（原話："provide guidance for the upcoming year each fall"）
- 2026-08-05｜CEO｜competition：管理層主張前表（front-of-the-meter）混合方案成本低於 behind-the-meter（原話："less expensive than any behind-the-meter solution"）
- 2026-08-05｜CEO｜competition：管理層稱 IRAS 實質上是 Connect and Manage（原話："IRAS is just Connect and Manage"）
- 2026-08-05｜CEO｜competition：管理層稱混合策略可作為 Connect and Manage 的安全港（原話："provides a safe harbor to"）
- 2026-08-05｜CEO｜competition：555 美元上限為平均值形成的軟上限（原話："the 555 cap, which is sort of a soft cap because"）
- 2026-08-05｜CEO｜risk：PPL 基差難以避險：交易不深、成本可能偏高（原話："It might become expensive to do it."）
- 2026-08-05｜CEO｜risk：雙邊市場長天期容量報價為薄量（原話："these are thinly traded"）
- 2026-08-05｜CEO｜risk：IRAS 細節未出，管理層稱影響難評估（原話："It's a bit of a hypothetical until we get proposal"）
- 2026-08-05｜President｜risk：PPL 區無資源充足性問題，發電過剩是基差原因（原話："PPL zone does not have a resource adequacy problem"）
- 2026-08-05｜CEO｜product：新增容量管線聚焦電池、尖峰機組與增容（原話："batteries, peakers and uprates"）
- 2026-08-05｜President｜product：設備供給可得，問題在價格（原話："The supply is there. It's available."）
- 2026-08-05｜President｜product：併購後新增燃氣廠增容項目納入新建容量管線（原話："we do have some upgrades that we're looking at"）
- 2026-08-05｜CFO｜customer：約 4GW 具電網負載承諾的資料中心站點（原話："advantaged data center sites with utility load commitments"）
- 2026-08-05｜CFO｜customer：潛在客戶擴及 co-locator、neo-cloud 與大型 C&I（原話："beyond hyperscalers to include Co-locators, Neo-clouds"）
- 2026-08-05｜CEO｜customer：管理層稱超大規模客戶決策時程為何時而非是否（原話："it's a matter of when, not if is the real point here"）
- 2026-08-05｜CEO｜customer：管理層稱無單一 gating 事項（原話："I don't know that there's any one particular gating item."）
- 2026-08-05｜CEO｜customer：超大規模客戶尋求 2028 年即可交付的容量（原話："all looking for something that can be done exactly in '28"）
- 2026-08-05｜CEO｜customer：長約遠期價已逼近先前與超大規模客戶討論的約 80 美元水準（原話："forwards have finally caught a bid"）
- 2026-08-05｜CEO｜customer：PJM 近三次容量拍賣均以價格上限結清（原話："the last 3 base residual capacity auctions clearing at"）
- 2026-08-05｜CEO｜customer：管理層稱遠期曲線開始反映供給緊俏（原話："we have seen bids at the cap level for the early"）
- 2026-08-05｜CEO｜guidance：避險：2028 年避險比率季增約 5% 至 25–30%（原話："quarter-over-quarter, 25% to 30%"）
- 2026-08-05｜President｜guidance：避險使用將結果區間圍起來的工具，並保留部分上行參與（原話："some instruments that allow us to fence in outcomes"）
- 2026-08-05｜CEO｜capital_allocation：收購動機：認為能量與容量被低估（原話："we felt as though energy and capacity was underpriced"）
- 2026-08-05｜President｜product：車隊容量因子 51%，較去年高 14 個百分點（原話："achieving a 51% fleet-wide capacity factor"）

### 問答異常語氣（迴避／改口／保留）
- TLN_Q2_2026_Earnings_Call_20260805.md｜問：Storozynski 問氣電資產長約價差相對遠期的溢價是否壓縮｜答法：未給數字，以玩笑帶過並稱 willing buyer/willing seller，改談混合方案價值
- TLN_Q2_2026_Earnings_Call_20260805.md｜問：Moses Sutton 追問 2028 FCF/股由 36 升至 40 的橋接項目（OpEx、協同、發電量）｜答法：未拆解各項貢獻，回答為整體企業模型與遠期價更新，僅 CFO 補充 ADHUB 影響
- TLN_Q2_2026_Earnings_Call_20260805.md｜問：Constantine Lednev 問 4GW 是否與前一季相比有變動｜答法：CFO 稱不評論專案數量，只說持續推進與擴充
- TLN_Q2_2026_Earnings_Call_20260805.md｜問：Carly Davenport 問是否參與 RBP 中央採購或雙邊流程｜答法：稱計畫參與但不保證，並說仍在研讀 695 頁文件
- TLN_Q2_2026_Earnings_Call_20260805.md｜問：Michael Sullivan 問 IRAS 對未來容量拍賣的影響｜答法：稱未聽清並表示須等內容出來再判斷，未直接回答

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
{"date":"20260612","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"PJM 結構性缺電使容量價 + spark spread 維持高位（非曇花一現）","columns":{"2Y 驗證點":"2028/29 BRA 清算價守在高檔","5Y 驗證點":"容量價在去上限後仍 &gt;$200/MW-day","10Y 驗證點":"PJM 負載成長持續 &gt; 新供給","具體數字門檻":"27/28 BRA $333/MW-day（cap）；目標 2028/29 &gt;$200","信息來源":"PJM BRA 報告 / 法說","漂移觸發條件":"連 1 次 BRA &lt;$150 → 削弱（容量週期屬慢變數）"}},{"id":"H2","text":"AWS 1,920 MW PPA 如期爬坡 + FTM 結構規避 FERC 風險","columns":{"2Y 驗證點":"2026H1 co-lo 轉 FTM 完成（傳輸升級後）","5Y 驗證點":"2029 爬坡達 840-1,200 MW","10Y 驗證點":"2032 達 1,680-1,920 MW，~$18B 收入兌現","具體數字門檻":"2029 ≥ 840 MW；契約至 2042","信息來源":"Talen 6/11/25 PR；AWS PPA","漂移觸發條件":"FTM 結構遭新監管挑戰 或 爬坡延後 &gt;12 月 → 削弱"}},{"id":"H3","text":"三併購（~5.4 GW）以增值倍數整合，FCF/share 持續累積 + 槓桿可控","columns":{"2Y 驗證點":"2027 FCF/share ~$34 兌現；淨槓桿 &lt;3.5x","5Y 驗證點":"2028 FCF/share $36→$41（含回購）","10Y 驗證點":"併購資產 ROIIC &gt; WACC 經週期驗證","具體數字門檻":"2027 FCF/share ≥$30；淨槓桿 ≤3.5x","信息來源":"Q1'26 法說 guidance","漂移觸發條件":"淨槓桿 &gt;3.5x 連 2 季，或 FCF/share 下修 &gt;15% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"PJM 容量價上限鬆綁 / 回落（新供給回應 + 行政上限到期）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"BRA 清算價","警戒閾值":"2028/29 BRA &lt;$200/MW-day"}},{"id":"R2","text":"Spark spread 隨新氣電產能 + 天然氣價波動回落","columns":{"對應假設":"H1/H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"前向 spark spread 曲線 vs guidance","警戒閾值":"實現 spread 連 2 季低於 guidance &gt;10%"}},{"id":"R3","text":"監管/政治：FERC 對 co-location 與資料中心併網的限制擴大（電費轉嫁公眾爭議）","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"FERC/PJM 規則制定、州 PUC 動向","警戒閾值":"FTM 結構被新規則納管 或 新增 ISA 全面凍結"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟢","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":360.54,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TLN_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
