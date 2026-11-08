你是 stock-analyst **v20 判斷 agent**，標的 OSCR（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"OSCR","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/OSCR_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/OSCR_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenue_gaap","label":"Total revenue (GAAP)","value":5139.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 8-K Q3 2026（SEC URL 同 quarter 欄）"},"note":"新聞稿未列共識；媒體稱優於預期（未驗證）"},{"id":"f_kpi1_non_gaap_adjusted_ebitda","label":"Non-GAAP: Adjusted EBITDA","value":206.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 8-K Q3 2026"},"note":"新聞稿未列共識"},{"id":"f_kpi2_gaap_earnings_from_opera","label":"GAAP earnings from operations","value":178.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M（利益率 3.46%，自算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 8-K Q3 2026"},"note":"新聞稿未列共識"},{"id":"f_kpi3_net_income_attributable_","label":"Net income attributable to Oscar / diluted EPS","value":167.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M；EPS $0.49","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 8-K Q3 2026"},"note":"新聞稿未列共識"},{"id":"f_kpi4_medical_loss_ratio_sg_a_","label":"Medical loss ratio / SG&A ratio","value":"MLR 84.0%；SG&A 14.0%","period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 8-K Q3 2026"},"note":"新聞稿未列共識"},{"id":"f_kpi5_free_cash_flow","label":"Free cash flow（前九個月，自算）","value":3478.9,"period":"前九個月至 2026-09-30（公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"前九個月至 2026-09-30（公告於 2026-11-05）","citation":"新聞稿營運現金流 3,510.7M 減資本支出（含資本化軟體）31.9M，自算；公司未報 FCF，Q3 單季現金流未揭露"},"note":"n/a"},{"id":"f_kpi7_effectuated_membership","label":"Effectuated membership","value":2691885,"period":"2026-09-30（公告於 2026-11-05）","unit":"members","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"2026-09-30（公告於 2026-11-05）","citation":"公司新聞稿 8-K Q3 2026"},"note":"n/a"},{"id":"f_kpi8_fy2026_guidance","label":"FY2026 guidance（上修）","value":"營收 19.0–19.3B；MLR 80.5–81.5%；SG&A 15.1–15.6%；營業利益 850–950M","period":"Q3 2026 公告（2026-11-05）","unit":"USD / %","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026 公告（2026-11-05）","citation":"公司新聞稿 8-K Q3 2026"},"note":"yfinance FY1 營收共識均值約 18.99B（財報前快照，見 capital_structure）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_oscr_fcf_margin_pct","label":"OSCR FCF 利潤率","value":43.41,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.OSCR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cnc_gross_margin_pct","label":"CNC 毛利率","value":7.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CNC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cnc_operating_margin_pct","label":"CNC 營業利益率","value":0.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CNC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cnc_fcf_margin_pct","label":"CNC FCF 利潤率","value":1.93,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CNC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_moh_gross_margin_pct","label":"MOH 毛利率","value":7.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MOH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_moh_operating_margin_pct","label":"MOH 營業利益率","value":0.6,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MOH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_moh_fcf_margin_pct","label":"MOH FCF 利潤率","value":0.54,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MOH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_elv_fcf_margin_pct","label":"ELV FCF 利潤率","value":3.23,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ELV.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_clov_gross_margin_pct","label":"CLOV 毛利率","value":19.53,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLOV.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_clov_operating_margin_pct","label":"CLOV 營業利益率","value":0.3,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLOV.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_clov_fcf_margin_pct","label":"CLOV FCF 利潤率","value":3.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLOV.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi6_sbc","label":"SBC 占營業利益 / 營收","value":12.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"% of earnings from operations（占營收 0.43%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"新聞稿 SBC 22.3M ÷ 營業利益 178.0M，自算"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":30.65,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":43.83,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":44.97,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.94 → 1.94）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.22 → 2.22）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.84 → 2.84）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.94,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.22,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":2.84,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":7.78,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 1.8 → 1.94（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":13.62,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"1 個年度端點內的分位＝50.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":50.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.55,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.14,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝69.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":69.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":15.8,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 1.94，分子＝快照價 30.65","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-7006.86,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 481.73、現金 7488.59（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":310.69,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":2515.67,"period":"2026-11-08","unit":"USD m","basis":"市值 9522.53 ＋ 淨負債 -7006.86","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":18990.59,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（8 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":20796.33,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（10 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.13,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 30.65 / W52 22.28 / W104 19.03 / W250 13.36 / W250 13週斜率 2.95%"},{"id":"f_ma_w52","label":"52 週均線","value":22.28,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":19.03,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":13.36,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.95,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K FY2025：主要對手為全國性carrier、區域carrier、Medicaid型保險公司及地方Blue Cross；HHS 2027 NBPP提案部分條款可能引來新進入者或造成市場不穩。","source":"SEC EDGAR 10-K FY2025 Item 1/1A","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm","excerpt":"Our principal competitors in the individual market primarily consist of plans offered by national carriers, regional carriers, Medicaid-focused insurers offering Health Insurance Marketplaces products, and local Blue Cross plans.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Oscar自報其footprint市佔由2025年17%升至2026年30%；2026年市場enrollment縮減","source":"Oscar Q4 2025 earnings call（經 roic.ai 轉錄）","url":"https://www.roic.ai/quote/OSCR/transcripts/2025-year/4-quarter","excerpt":null,"as_of":"2026-02-10","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2027年Oscar擴入南卡、縣數+24%；多家保險公司退出ACA、另有Centene、AmeriHealth Caritas等新增縣市／州","source":"Healthcare Dive / Becker's 2027 ACA footprint","url":"https://www.beckerspayer.com/payer/aca/how-insurers-aca-footprints-are-changing-in-2027/","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"2026年ACA enrollment由24.3M降至約22.8M，UNH預期流失約50萬ACA會員","source":"acasignups.net","url":"https://acasignups.net/node/9787","excerpt":"United Healthcare told investors that it will lose millions of consumers this year across most of its products, including 500,000 fewer ACA marketplace enrollees.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2022 10-K：2022 年約 85%、2021 年約 73% 的會員保費由 APTC 補貼（對聯邦補貼依賴度，非單一客戶占比；無單一客戶營收占比數字）","source":"Oscar Health 10-K FY2022 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865123000017/oscr-20221231.htm","excerpt":"During the years ended December 31, 2022 and 2021, the direct policy premiums of approximately 85% and 73%, respectively, of our members were subsidized by APTCs.","as_of":"2023-02-28","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K 將 eAPTC 到期與 CMS program integrity rules 列為影響估計的法規變動","source":"Oscar Health 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm","excerpt":"changes in legislation and regulations (including the expiration of the eAPTCs and the CMS program integrity rules)","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Oscar Health 與 Centene 公布 2027 ACA 市場布局（擴張縣數；競爭者如 Cigna/Aetna 退出視為成長機會）","source":"Fierce Healthcare","url":"https://www.fiercehealthcare.com/payers/centene-oscar-health-outline-2027-aca-marketplace-plans","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Oscar Q2 2026：營收年增70%至$4.9B、會員2.96M、MLR 79.2%、2026營運獲利指引上調至$500–700M；管理層預期月流失率約為先前估計兩倍","source":"MarketBeat Oscar Health Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/oscar-health-q2-earnings-call-highlights-2026-08-08/","excerpt":null,"as_of":"2026-08-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因素：Oscar 因收取聯邦付款，受 DOJ／HHS-OIG／CMS 的詐欺、浪費與濫用法規（含 FCA）管轄，預期持續受審查；10-K 未點名具體反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm","excerpt":"We anticipate continued scrutiny by the HHS-OIG and the DOJ in the areas of fraud, waste, and abuse, including the use of telehealth and telemedicine-based treatment, and we may be subject to audits, reviews and investigations of our telehealth coverage and payment practices and arrangements by government agencies.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因素：部分市場的醫院或醫師團體具near monopoly地位，削弱 Oscar 議價力（供給端集中，非 Oscar 自身被調查）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm","excerpt":"In some markets and geographies, certain healthcare providers, particularly hospitals, physician/hospital organizations, or multi-specialty physician groups, may have significant positions or near monopolies that could result in diminished bargaining power on our part during contract negotiations.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"搜尋未發現 2026 年針對 Oscar 的 DOJ／FTC／EU 反壟斷調查或拆分風險；產業監管面向為 eAPTC 補貼 2025 年底到期、CMS 2025 年 Program Integrity 規則（部分條款遭 Maryland 聯邦地院 2025-08-22 暫停）。依 Q2 2026 10-Q 摘要，公司業務受州與聯邦監管機關審查。","source":"SEC EDGAR 10-Q（截至 2026-06-30）搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001568651/000156865126000069/oscr-20260630.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"2019 年 Oscar 為原告控告 Florida Blue 排他經紀人政策，DOJ 提出支持 Oscar 的利益聲明；地院判 Oscar 敗訴後上訴第 11 巡迴法院。","source":"Fierce Healthcare: DOJ sides with Oscar Health in ongoing spat with Florida Blue","url":"https://www.fiercehealthcare.com/payer/doj-sides-oscar-health-ongoing-spat-florida-blue-over-broker-agreements","excerpt":null,"as_of":"2019-05-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K：公司表示川普政府可能對藥品、原料、醫療器材與耗材課關稅，可能推高醫療院所成本、藥價與醫療器材成本，並造成藥品與醫療用品短缺，進而影響醫療成本估計。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm","excerpt":"The Trump administration has indicated that tariffs may be imposed on a variety of products relevant to our business, including certain pharmaceutical products and ingredients and medical devices and supplies imported into the United States. Any such tariffs could result in higher costs for medical providers and facilities, higher pharmaceutical prices, higher costs of medical devices, and shortages of certain medicines and medical supplies.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K MD&A 列「Proposed Tariffs」：關稅的不確定性可能影響公司估計與管理醫療費用的能力。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm","excerpt":"The unprecedented nature of these types of tariffs, as well as uncertainty around their implementation, could impact our ability to accurately estimate and effectively manage the impact on our medical expenses, which in turn could adversely affect our results of operations and financial position.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026-04 Section 232 公告對專利藥及藥品原料課 100% 關稅；Oscar 後續 10-Q 稱關稅生效後藥品回扣可能同步或更大幅下降。","source":"Oscar Health 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001568651/000156865126000086/oscr-20260930.htm","excerpt":"April 2, 2026, the Trump administration issued a proclamation under Section 232 of the Trade Expansion Act imposing 100% tariffs on patented pharmaceuticals and associated pharmaceutical ingredients, imported into the United States, which took effect on July 31, 2026 for certain enumerated companies, and on September 29, 2026 for all other companies, unless manufacturers agreed to specific","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Mayer Brown：川普政府依 Section 232 對進口專利藥與藥品原料課關稅（2026-04）。","source":"Mayer Brown 文章","url":"https://www.mayerbrown.com/ja/insights/publications/2026/04/trump-administration-implements-tariffs-on-imported-patented-medication-and-pharmaceutical-ingredients-under-section-232-of-the-trade-expansion-act-of-1962","excerpt":"This Proclamation, issued pursuant to Section 232 of the Trade Expansion Act of 1962,1 establishes a 100% ad valorem duty on products of companies that have not secured “Most-Favored-Nation” (“MFN”) pricing agreements, while providing tiered lower rates for companies committed to onshoring production to the United States and countries that","as_of":"2026-04-03","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Oscar 10-K（FY2025）揭露依賴第三方供應商營運多數通訊、網路與電腦軟硬體；失去供應商可能造成重大中斷。未見地緣（台灣/中國）暴露的搜尋摘要。","source":"Oscar Health Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm","excerpt":"Some of these third-parties have direct access to our systems in order to provide their services to us and operate the majority of our communications, network, and computer hardware and software.","as_of":"2026-02-28","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Oscar 將藥局理賠與網絡管理委外給單一 PBM（CVS/Caremark），並用 AWS、Google Cloud 託管（FY2021 10-K）。","source":"Oscar Health Form 10-K FY2021","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865122000011/oscr-20211231.htm","excerpt":"Oscar delegates pharmacy claims and network management to a Pharmacy Benefit manager (PBM), CVS/Caremark.","as_of":"2022-03-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026（2026-11-05 公布）：總營收約 $51 億（去年同期 $30 億，含 $2.5 億風險調整估計更新利益）；有效會員 2,691,885，年增約 27%，來自 2026 開放投保期高於市場的成長與高續保；MLR 84.0% 對 88.5%；全年營收指引上調至 $190–193 億。","source":"Oscar Health 8-K Q3 2026 earnings release（SEC）；搜尋摘要含 Becker's/Fierce","url":"https://www.sec.gov/Archives/edgar/data/0001568651/000156865126000082/oscarhealththirdquarter202.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"2027 逆風：KFF 資料顯示個人市場 2026 年 6 月約 2,050 萬人，年減約 18%；保險公司 2027 提案保費中位數漲約 15%，Oscar 喬治亞州申請約 29%。UBS 降評 Sell，預估 2027 營收 $122 億、EPS $1.25（低於共識 $1.46），指定價能力有限；Piper 認為即使加強補貼失效 Oscar 仍可能拿下份額。","source":"Weiss Ratings 引 KFF；AllMind（UBS）；Asianet Newsable（Piper/Jefferies）","url":"https://weissratings.com/en/instant-news-alerts/oscar-health-inc-oscr-down-5-2-is-it-smart-to-take-money-off-the-table","excerpt":null,"as_of":"2026-10-31","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Oscar 目標全國 ACA 份額 >18%，可服務市場由約 960 萬人擴至 1,600 萬人；UnitedHealthcare 2027 退出喬治亞 ACA 市場；Oscar 約 290 萬 ACA 會員、持續擴張版圖。","source":"BeInsure；Healthcare Dive","url":"https://www.healthcaredive.com/news/centene-oscar-unitedhealthcare-new-counties-aca-2027/833442/","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Oscar 10-K 稱 ICHRA 將顛覆雇主團體保險並擴張個人保險市場；公司以 2025 年收購的 Lucie、IHC Specialty Benefits 作為 ICHRA 策略基礎（替代模式同時是公司自身的佈局）。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm","excerpt":"We continue to believe ICHRA will disrupt employer group coverage and expand individual insurance beyond the traditional ACA market. Our goal is to position Oscar as the preferred carrier for employees enrolling in health insurance through an ICHRA program.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：公司核心技術與基礎設施為自建，關鍵技術人員流失可能干擾營運；且未申請專利保護其專有技術。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm","excerpt":"we have registered, or applied to register, those trademarks that we believe are important to our business, but to date we have not filed patent applications to protect our innovations and proprietary technology.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025：絕大多數會員經經紀人通路取得，經紀人多用EDE平台於交易所投保，Oscar以佣金與獎金結構競爭；ICHRA員工亦可購買其方案，多數在交易所外購買。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm","excerpt":"The vast majority of our membership is acquired through the broker channel, and brokers typically use an EDE platform to enroll the members in plans offered on the Health Insurance Marketplace. As such, we compete through the commissions and bonus structures we pay these partners.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Oscar贊助之SureCo 2026 ICHRA報告：56%經紀人推薦ICHRA，移轉至少一客戶至ICHRA的經紀人比例由2024年15%升至2026年37%。","source":"Fierce Healthcare: Study: Brokers increasingly recommending ICHRA to employers","url":"https://www.fiercehealthcare.com/payers/study-brokers-increasingly-recommending-ichra-employers","excerpt":null,"as_of":"2026-05-21","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Oscar Investor Day：目標成為消費者偏好的AI原生保險商，拓展至ACA以外族群；Lucie市集為payer-agnostic。","source":"Quartr: Oscar Health Investor Day 2026 summary","url":"https://quartr.com/events/oscar-health-inc-oscr-investor-day-2026_369vXoKU","excerpt":"Plans to expand beyond ACA, targeting gig workers, part-time employees, public program participants, and the broader individual market, with a goal to serve all 350 million Americans. Lucie Health Marketplace will be payer-agnostic, enabling all carriers to compete and offering a broad range of health and wellness products, aiming","as_of":"2026-09-22","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Oscar 2026-08-06 Q2 發布並上調全年 2026 展望（營運盈餘區間上調、MLR 區間收窄）；搜尋摘要稱 11-05 Q3 再度上調營運盈餘展望（第三次），Q3 具體數字未取得。","source":"Business Wire: Oscar Health Announces Record Financial Results for First Half 2026 and Raises Full Year 2026 Outlook","url":"https://www.businesswire.com/news/home/20260806425955/en/Oscar-Health-Announces-Record-Financial-Results-for-First-Half-2026-and-Raises-Full-Year-2026-Outlook","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill 顯示 FY2026 EPS 共識 1.87 美元（15 位分析師，2026-10-24 記錄），Q3 EPS 共識 -0.22 美元、營收約 48.2 億美元；Q2 實際 EPS 1.10 對共識約 0.32–0.40。","source":"Chartmill OSCR estimates","url":"https://www.chartmill.com/stock/quote/OSCR/estimates","excerpt":null,"as_of":"2026-10-24","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布分歧且 as-of 不一：TickFlow 2026-08-02 共識 Hold（6 位）均值 $24.20；MarketBeat 2026-05-02 均值約 $16.78（11 位，2 sell/7 hold/2 buy）；StockAnalysis 均值 $18.25 區間 $11–25；Benzinga 於投資人日後 Barclays 目標價 $49。各聚合站數字不一致，未核原文。","source":"TickFlow / MarketBeat / StockAnalysis / Benzinga 搜尋摘要","url":"https://tickflow.io/stock/OSCR/forecast","excerpt":null,"as_of":"2026-08-02","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 8-K 載明再度上調全年展望","source":"SEC 8-K Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0001568651/000156865126000082/oscarhealththirdquarter202.htm","excerpt":"Prior Full Year 2026 Outlook Updated Full Year 2026 Outlook (in thousands, except percentages) Low High Low High Total revenue (1) $18.7 billion $19.0 billion $19.0 billion $19.3 billion Medical loss ratio (2) 81.0% 82.0% 80.5% 81.5% SG&A expense ratio (3) 15.6% 16.1% 15.1% 15.6% Earnings from operations (4)","as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月8-K共11份，僅1份含重大項目（2026-02-10 Item 1.01，4.75億美元三年期擔保循環信貸）；無併購、重編（4.02）類8-K。","source":"SEC EDGAR 8-K 申報清單（2025-11-08至2026-11-08）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001568651&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"2022年IPO證券集體訴訟（Carpenter v. Oscar Health）列於FY2025 10-K；另CSR集體訴訟（Common Ground）和解經法院2025-11-06最終核准，2025年底認列約4,800萬美元淨回收（對公司為受益方）。","source":"SEC EDGAR 10-K FY2025 Note 18","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm","excerpt":"On November 6, 2025, the Court of Federal Claims granted final settlement approval and ordered the distribution of 95% of the settlement funds, with the remaining 5% held until the attorneys’ fees award is determined. The estimated net recovery recorded as of December 31, 2025 was approximately $48 million.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"unprofitable_nrr_rule40_band#none","axis":"unprofitable_nrr_rule40_band","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"unprofitable_dilution_trajectory#0","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"聚合站顯示 OSCR 2026 Q1 稀釋加權股數 329.8M，年增 7.8%（305.9M→329.8M）；來源未對照 10-Q 原文","source":"opencapital.sh weighted shares diluted / stockanalysis.com OSCR financials","url":"https://www.opencapital.sh/stocks/oscr/metrics/weighted_shares_diluted","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#1","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"稀釋股數年度序列（聚合站）：FY2021 179M、FY2022 212M、FY2023 222M、FY2024 266M、FY2025 262M；各站數字有出入","source":"stockanalysis.com OSCR financials / alphaquery annual diluted weighted shares","url":"https://stockanalysis.com/stocks/OSCR/financials/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#2","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"0","claim":"2025-09 發行 $355M 2.25% 可轉債（2030 到期），轉換價約 $24.82、每千美元 40.2946 股，並買 capped call（上限初始 $37.46）以抵銷稀釋","source":"Business Wire: Oscar Health Prices Upsized $355,000,000 Convertible Senior Subordinated Notes Offering","url":"https://www.businesswire.com/news/home/20250916911961/en/Oscar-Health-Prices-Upsized-355000000-Convertible-Senior-Subordinated-Notes-Offering-to-Scale-Long-Term-Growth-and-Consumer-and-Employer-Adoption-of-the-Individual-Market","excerpt":null,"as_of":"2025-09-16","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#3","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"0","claim":"聚合站（Digrin）列 2026 Q1 SBC 約 $16.0M，同季營收約 $4.65B；FY2025 SBC 約 $87.65M（AlphaQuery，期間標示存疑）","source":"digrin.com OSCR financials / alphaquery quarterly stock-based compensation","url":"https://www.digrin.com/stocks/detail/OSCR/financials","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"unprofitable_path_to_profitability#0","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"+","claim":"Oscar 已轉正：2026 全年 earnings from operations 指引於 11/5 第三度上修至 8.5–9.5 億美元（原 6–8 億），MLR 80.5–81.5%，營收 190–193 億；前九個月歸屬淨利 12.1 億美元","source":"Oscar Health 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001568651/000156865126000082/oscarhealththirdquarter202.htm","excerpt":"\"Oscar Health is on track to deliver the strongest year of financial performance in our history\"","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"unprofitable_path_to_profitability#1","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"+","claim":"前九個月營運現金流 +35.1 億美元（去年同期 4.2 億）；現金 44.7 億、短投 30.2 億、長投 14.4 億（2026-09-30）","source":"Oscar Health 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001568651/000156865126000082/oscarhealththirdquarter202.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_path_to_profitability#2","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"0","claim":"Q1 2026 10-Q：現金與投資足以支應至少未來十二個月營運需求；未見公司正式 FCF 指引","source":"Oscar Health 10-Q Q1 2026","url":"https://www.sec.gov/Archives/edgar/data/0001568651/000156865126000040/oscr-20260331.htm","excerpt":"cash, cash equivalents, and investments, not including restricted cash, will be sufficient to fund our operating requirements for at least the next twelve months","as_of":"2026-05-07","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K清單無Item 1.01併購協議／2.01完成收購；唯一重大項目為2026-02信貸額度。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001568651&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K揭露2022年IPO證券集體訴訟（SDNY, Carpenter v. Oscar Health）；搜尋摘要稱該案2025-04-22已被法院以不得重訴駁回（未讀原文）；未見2026新增證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 Note 18","url":"https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm","excerpt":"In addition, on May 12, 2022, a securities class action lawsuit against the Company, certain of its directors and officers, and the underwriters that participated in the Company’s IPO was commenced in the United States District Court for the Southern District of New York (the “Court”), captioned Carpenter v. Oscar Health, Inc., et al., Case No. 1:22-CV-03885 (S.D.N.Y.) (the “Securities Action”).","as_of":"2026-02-13","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K清單中無Item 4.02（財報不可信賴／重編）；僅1份含重大項目（信貸額度）。搜尋未見SEC調查。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001568651&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"OSCR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":43.41,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.OSCR","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CNC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":7.78,"operating_margin_pct":0.75,"fcf_margin_pct":1.93,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CNC","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MOH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":7.97,"operating_margin_pct":0.6,"fcf_margin_pct":0.54,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MOH","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ELV","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":3.23,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ELV","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CLOV","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.53,"operating_margin_pct":0.3,"fcf_margin_pct":3.17,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLOV","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"OSCR"},"financial_history":{"ticker":"OSCR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":4125584000.0,"revenue_yoy_pct":null,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":-606275000.0,"diluted_eps":-2.85,"free_cash_flow":351337000.0,"fcf_margin_pct":8.52,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":5862869000.0,"revenue_yoy_pct":42.11,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":-270728000.0,"diluted_eps":-1.22,"free_cash_flow":-297736000.0,"fcf_margin_pct":-5.08,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":9177941000.0,"revenue_yoy_pct":56.54,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":25432000.0,"diluted_eps":0.1,"free_cash_flow":950296000.0,"fcf_margin_pct":10.35,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":11701427000.0,"revenue_yoy_pct":27.5,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":-443151000.0,"diluted_eps":-1.69,"free_cash_flow":1058482000.0,"fcf_margin_pct":9.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/OSCR/OSCR_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**Oscar Health, Inc.** | Earnings Calls | 2026-11-05

**Mark Bertolini** (Executives):
[Audio Gap] address consumer needs, including opportunities created by competitor exits. These strengths, combined with our medical cost management, operating efficiency and superior technology will drive sustainable financial performance in 2027 and beyond. 
Now I will review our business highlights. Oscar Insurance ended the third quarter with 2.7 million members, up 27% year-over-year. We are entering open enrollment with a 24% larger footprint spanning 713 counties. We are also expanding into South Carolina. Our expansion increases our total addressable market to approximately 10 million consumers across 21 states. 
Oscar is launching a new wave of consumer lifestyle products. Our newest product, RetireEase, is live in select markets and serves a growing segment of 2.5 million early retirees in the ACA. Members keep their trusted doctors and receive set prices for preventative services, physical therapy and heart, bone and joint care. We are also addressing affordability through bundled benefits. Hundreds of Oscar plans now include dental and vision coverage. 
In addition, our new Allstate Health Solutions partnership pairs Oscar plans with low-cost supplemental coverage to help bronze members manage out-of-pocket costs. Each product meets a distinct consumer need and extends our reach into high-value underserved segments. 
Our Oscar team is also scaling CHOICE. Our Hy-Vee Health with Oscar product is expanding from Iowa into Nebraska, Missouri and Kansas. This product's concierge care model earns a 92% satisfaction rate and can now serve more small businesses, part-time employees and gig workers. 
We are also launching HelloMeno off-exchange to better serve women across the workforce. Employer demand is building. CHOICE adoption is growing fastest in health care, technology, construction and manufacturing sectors across Oscar states. Oscar's health technology puts consumer in control of their health care decisions across 2 platforms. 
The Oscar platform now includes new AI capabilities that make our product suite easy to understand. The Lucie platform serves the broader market, personalizing the health care shopping experience at scale. Lucie instantly matches consumers with plans from major ACA carriers and select supplemental carriers and guides broker through CMS eligibility. No other platform brings these capabilities together in one place. Lucie is on track to sell approximately 800,000 new policies in 2027, driven by growing broker and consumer demand. 
Oscar Health's third quarter performance puts us on track to deliver strong results 1 year ahead of plan. Our disciplined pricing, product innovation and technology-powered support are delivering superior member experiences and efficiency across the company. The individual market opportunity is growing. People expect health care to work like the best consumer products, simple, transparent and personalized. We are building a consumer health care company that meets those expectations and serves a much larger market. The team is positioned to grow market share [Technical Difficulty].

**Richard Blackley** (Executives):
Some technical difficulties with the call. Some of the audience was only able to hear the call after we had started. So we're going to go ahead and start over. I apologize for the challenges, but please bear with us, and we're going to start the call from this point forward.

**Chris Potochar** (Executives):
Good morning, everyone. Thank you for joining us for our third quarter 2026 earnings call. Mark Bertolini, Oscar Health's Chief Executive Officer; and Scott Blackley, Oscar Health's Chief Financial Officer, will host this morning's call. 
This call can also be accessed through our Investor Relations website at ir.oscarhealth.com. Full details of our results and additional management commentary are available in our earnings release, which can be found on our Investor Relations website at ir.oscarhealth.com.
Any remarks that Oscar makes about the future constitute forward-looking statements within the meaning of safe harbor provisions under the Private Securities Litigation Reform Act of 1995. Actual results may differ materially from those indicated by those forward-looking statements as a result of various important factors, including those discussed in our annual report on Form 10-K for the period ended December 31, 2025, and the quarterly report on Form 10-Q for the period ended June 30, 2026, each as filed with the Securities and Exchange Commission and other filings with the SEC, including our quarterly report on Form 10-Q for the period ended September 30, 2026, to be filed with the SEC. 
Such forward-looking statements are based on current expectations as of today. Oscar anticipates that subsequent events and developments may cause estimates to change. While the company may elect to update these forward-looking statements at some point in the future, we specifically disclaim any obligation to do so. The call will also refer to certain non-GAAP measures. A reconciliation of these measures to the most directly comparable GAAP measures can be found in the third quarter earnings press release available on the company's Investor Relations website at ir.oscarhealth.com. 
We have not provided a quantitative reconciliation of estimated full year 2026 adjusted EBITDA as described in this call to GAAP net income because Oscar is unable without making unreasonable efforts to calculate certain reconciling items with confidence. 
With that, I will turn the call over to our CEO, Mark Bertolini.

**Mark Bertolini** (Executives):
Good morning. Thank you, Chris, and thank you all for joining us. 2026 is the strongest year in Oscar Health's history. We delivered record profitability for the first 9 months of the year, reporting earnings from operations of $1.3 billion and net income of $1.2 billion. We also expect to achieve several of our 2024 Investor Day commitments 1 year ahead of plan. 
Based on our performance year-to-date, we are raising 2026 earnings from operations guidance for a third time to a range of $850 million to $950 million. Our strong third quarter performance exceeded our expectations with improvement across all core metrics. Revenue grew roughly 70% year-over-year to $5.1 billion. Our SG&A expense ratio improved 350 basis points year-over-year to 14%, another record low, reflecting the disciplined execution, greater fixed cost leverage and AI-driven efficiencies. 
MLR improved 450 basis points over the prior year period to 84%. Earnings from operations increased $307 million year-over-year to $178 million and adjusted EBITDA increased $308 million to $207 million. 
Before I turn to our business highlights, I will share our perspective on current market trends. The ACA is the foundation of a rapidly developing individual market. Americans are building careers on their own terms. They are starting businesses, combining part-time work, participating in the gig economy and retiring early. More than 19 million people rely on the ACA, yet 28 million American workers remain uninsured. 
Affordable coverage gives people greater financial security to pursue new opportunities and helps employers build a more stable workforce. Both parties understand health care is a priority for the American people. We have a significant opportunity to expand the ACA into a competitive marketplace that improves affordability and supports a resilient economy. Our 2026 performance demonstrates the strength of our operating model. We remain focused on growing market share and expanding margin in 2027. 
Our weighted average rate increase of approximately 14% for 2027 open enrollment period reflects elevated trend and higher market morbidity. Pricing is one lever of our growth model. We also target markets where our products and distribution network address consumer needs, including opportunities created by competitor exits. These strengths, combined with our medical cost management, operating efficiency and superior technology will drive sustainable financial performance in 2027 and beyond. 
Now I will review our business highlights. Oscar Insurance ended the third quarter with 2.7 million members, up 27% year-over-year. We are entering open enrollment with a 24% larger footprint spanning 713 counties. We are also expanding into South Carolina. Our expansion increases our total addressable market to approximately 10 million consumers across 21 states. Oscar is launching a new wave of consumer lifestyle products. Our newest product, RetireEase, is live in select markets and serves a growing segment of 2.5 million early retirees in the ACA. 
Members keep their trusted doctors and receive set prices for preventative services, physical therapy and heart, bone and joint care. We are also addressing affordability through bundled benefits. Hundreds of Oscar plans now include dental and vision coverage. 
In addition, our new Allstate Health Solutions partnership pairs Oscar plans with low-cost supplemental coverage to help bronze members manage out-of-pocket costs. Each product meets a distinct consumer need and extends our reach into high-value underserved segments. 
Our Oscar team is also scaling CHOICE. Our Hy-Vee Health with Oscar product is expanding from Iowa into Nebraska, Missouri and Kansas. This product's concierge care model earns a 92% satisfaction rate and can now serve more small businesses, part-time employees and gig workers. 
We are also launching HelloMeno off-exchange to better serve women across the workforce. Employer demand is building. CHOICE adoption is growing fastest in health care, technology, construction and manufacturing sectors across Oscar states. Oscar's health technology puts consumer in control of their health care decisions across 2 platforms. 
The Oscar platform now includes new AI capabilities that make our product suite easy to understand. The Lucie platform serves the broader market, personalizing the health care shopping experience at scale. Lucie instantly matches consumers with plans from major ACA carriers and select supplemental carriers and guides broker through CMS eligibility. No other platform brings these capabilities together in one place. Lucie is on track to sell approximately 800,000 new policies in 2027, driven by growing broker and consumer demand. 
Oscar Health's third quarter performance puts us on track to deliver strong results 1 year ahead of plan. Our disciplined pricing, product innovation and technology-powered support are delivering superior member experiences and efficiency across the company. The individual market opportunity is growing. People expect health care to work like the best consumer products, simple, transparent and personalized. We are building a consumer health care company that meets those expectations and serves a much larger market. The team is positioned to grow market share and expand margin in 2027. 
We are also on track to deliver our long-term targets, including at least $4 earnings per share by 2029. Thank you to the Oscar Health team for giving people power over their health care. 
With that, I will turn the call over to Scott. Scott?

**Richard Blackley** (Executives):
Thank you, Mark, and good morning, everyone. Sorry for the voice. I'm recovering from a cold today. Through the first 9 months of 2026, we delivered net income of approximately $1.2 billion or $3.59 per diluted share. Earnings from operations were approximately $1.3 billion. Based on these strong results and underlying trends, we are raising our full year 2026 outlook. 
Turning now to third quarter results. We ended the quarter with approximately 2.7 million members, an increase of 27% year-over-year. Sequential decline in membership primarily reflects disenrollments from CMS' industry-wide eligibility review, which was in line with expectations. From a second smaller CMS review, we expect a small number of additional disenrollments in the fourth quarter. 
Total revenue increased approximately 70% year-over-year to $5.1 billion, driven by rate increases and higher membership. During the quarter, we received updated risk adjustment data. We saw significant improvement in Oscar's risk relative to the market and market morbidity was modestly favorable to our expectations. 
These factors drove a $250 million revenue benefit in the quarter. Risk adjustment as a percentage of premiums was 11.8% in the third quarter and 17.2% through the first 9 months. While the additional data gives us greater visibility and more confidence in our risk adjustment accruals, we continue to take a cautious approach to our risk adjustment reserves. The third quarter medical loss ratio was 84%, an improvement of 450 basis points year-over-year. 
Improvement was primarily driven by our disciplined pricing strategy. Overall, year-to-date utilization was moderately favorable to our expectations. By category, inpatient, professional and pharmacy utilization were favorable, while outpatient was elevated. We believe some of the elevated outpatient utilization reflects a rotation from inpatient to outpatient care, driven in part by our affordability initiatives. 
Switching to administrative costs. The third quarter SG&A expense ratio was 14%, the lowest in the company's history. The approximately 350 basis point year-over-year improvement was driven by lower risk adjustment as a percentage of premium, higher fixed cost leverage and disciplined expense management, including an increasing impact from technology and AI initiatives. 
We reported earnings from operations of $178 million in the third quarter, a $307 million year-over-year improvement. Operating margin was 3.5%, an improvement of approximately 780 basis points year-over-year. Net income was $167 million, a $305 million increase year-over-year. Adjusted EBITDA was $207 million in the quarter, an increase of $308 million year-over-year. 
Shifting to the balance sheet. We ended the third quarter with approximately $9 billion of cash and investments, including $360 million of cash and investments at the parent. The sequential decline in cash and investments primarily reflect the payment of our 2025 risk adjustment payable during the third quarter. As of September 30, our Insurance subsidiaries had approximately $2.3 billion of capital and surplus, including $1.4 billion of excess capital, which was driven by our strong operating performance. 
Turning now to our 2026 full year guidance. Based on our results through the first 9 months, we are raising our full year earnings from operations guidance to a range of $850 million to $950 million. At the midpoint, this is $200 million above our prior outlook and $550 million above our original guidance. Our improved outlook reflects favorable risk adjustment and utilization that was moderately favorable to our expectations. We now expect total revenue in the range of $19 billion to $19.3 billion, an increase of $300 million from our prior outlook. 
We expect to end the year with approximately 2.5 million members, which reflect the additional disenrollments from the second CMS review. We expect risk adjustment as a percentage of premiums to be between 17% and 18% compared with our prior expectation of 20%, which is based on year-to-date risk adjustment experience. 
Turning to the medical loss ratio. We now expect a full year MLR in the range of 80.5% to 81.5%. On administrative expenses, we expect our SG&A expense ratio to be in the range of 15.1% to 15.6%. We expect adjusted EBITDA to be roughly $110 million higher than earnings from operations. 
Our performance this year positions us well for 2027. We will provide formal guidance on the fourth quarter earnings call, but let me spend a moment on our buying assumptions. We expect overall ACA marketplace membership to be stable compared with year-end 2026, and we are positioned to gain market share. We continue to take a disciplined approach into pricing, balancing growth and profitability. As Mark mentioned, our weighted average rate increase for 2027 is approximately 14%. Our pricing reflects an incremental increase in medical cost trends and higher market morbidity from ongoing program integrity initiatives. 
Our competitive positioning, differentiated products and strong member experience gives us confidence as we head into 2027. We expect improved medical cost performance and administrative efficiency to drive further margin expansion next year. 
In closing, we are on track to deliver a strong financial performance in 2026, and we remain focused on driving sustainable earnings growth and achieving our long-term target of at least $4 of earnings per share by 2029. 
With that, I'll turn the call over to the operator for the Q&A portion of our call.

**Operator** (Operator):
[Operator Instructions] And we'll take our first question from Andrew Mok with Barclays.

**Andrew Mok** (Analysts):
G&A came in meaningfully better in the quarter, but updated guidance appears to imply a 400 basis point sequential increase. Can you elaborate on the drivers of the strong 3Q outperformance? And what's driving the higher-than-normal step-up for 4Q?

**Richard Blackley** (Executives):
So on SG&A, I think that in Q3, you're seeing the benefit of our continuous disciplined expense management, growing impact of AI that we're deploying across the business and those are the themes that I would call out. We're also picking up a pretty healthy amount of fixed cost leverage. So that -- those are the drivers of Q3 performance. As you think about Q4, there is a step-up in the Q4 SG&A ratio. A portion of that is being driven by things like -- I would say these are Q4 specific spend, things like OE ramp, some of our risk adjustment operations where we do a lot of our chart collection activity in the fourth quarter. And then we've got some typical investments that we make for '27 growth in the fourth quarter. So I would say these are kind of seasonally expected spend, but we like the trajectory of SG&A.

**Andrew Mok** (Analysts):
Great. And I think I heard you say membership is expected to be stable with year-end 2026 results while you take market share. Can you flesh out a little bit more how you're thinking about your share gains in the context of how market growth might play out for 2027?

**Mark Bertolini** (Executives):
Sure. Thanks, Andrew. This is Mark. So we'll start with the market growth that both Scott and I highlighted, where we've -- we're now going to be 713 markets. We've added South Carolina. Secondly, I would offer new program extensions and products into the marketplace like RetireEase, where we tend to have very high retention and opportunistic growth in those marketplaces. 
And then finally, there's about 850,000 lives coming to market as a result of competitor exits. So all of that, as we add that into our mix and our ability to price appropriately disciplined and competitively in the marketplace, we believe that we'll pick up share.

**Operator** (Operator):
And our next question comes from Jessica Tassan with Piper Sandler.

**Jessica Tassan** (Analysts):
Congratulations on the phenomenal results. So our estimates imply, I think, that year-over-year MedEx PMPM increased 19.9% in 3Q from down 1.5% in 2Q. So can you maybe just give us some color on the utilization behavior you're observing by metal level? Curious to know how MLR seasonality is evolving both for bronze members and then also whether you're observing any changes in silver member to your historical -- relative to historicals or relative to expectations and why that might be?

**Richard Blackley** (Executives):
Yes, Jess. Let me start with the claims PMPM. So one of the challenges that you guys have this year in looking at claims PMPM is that we do have our member months because of some of these CMS-driven disenrollments. Member months are -- reported are a little bit different than those that are actually generating claims. So there is a little bit of a skew in that. So when I unpack that and kind of put Humpty Dumpty back together, what I see is that from Q1 to Q2, there's a meaningful step-up in claims PMPM. 
We see another step-up in Q3 from there. And in Q4, we're anticipating, and this has historically been the case that there's less movement, a fairly stable Q3 to Q4 PMPM support. When I look at utilization, we're seeing utilization across the metals, which is consistent with the risk that we see there. We're not seeing any specific thing that I would call out from one metal to the next. I think that the risk that we have in the book is being supported by the claims that we're seeing. And we're -- as you think about the MLR that we've got embedded for our fourth quarter, we are expecting a normal seasonal uptick in MLR into the fourth quarter from where we are in Q3.

**Jessica Tassan** (Analysts):
Got it. That's really helpful. And then I appreciate that the midterm has changed the eAPTC outlook considerably for '28, but maybe hoping you can help us better understand just the membership outlook for 2027. Where are we in terms of CMS' fraud and marketplace integrity efforts? And how do you expect those efforts to evolve in '27? And then can you just clarify that despite the expectation for flat enrollment year-over-year in 2027, you all are priced for an increase in market morbidity within that 14%.

**Mark Bertolini** (Executives):
Yes, Jess, I'll start, and then I'll turn it over to -- I'll turn it over to Scott on market morbidity. So we do expect stable membership year-over-year. We do still see more program integrity programs coming through. We believe that will have an impact on the marketplace. Obviously, as I said before, it's going to be offset by some of the other things, new markets entered, new products and other competitors leaving. 
So overall, we see the whole market being relatively stable. I don't think the midterms are going to have much of an effect, if anything, in the near term because there's a lot of bargaining that would need to go on given that the administration still will hold the veto pen. And so getting the kind of things we would need to get done to, for example, reintroduce enhanced subsidies and others would have to be part of a grander deal, and we're not quite sure how the dynamics of that will move forward. We always plan for these things in our operating plans and risks and opportunities. And we always see what we would need to do should these things begin to happen. But right now, I don't know that much of anything is going to happen over the next year at least. Scott?

**Richard Blackley** (Executives):
Yes. So Jess, with respect to market morbidity, I have a couple of thoughts there. One is, we are seeing and expecting to see a stable ACA in '27. A lot of the big change events happened in '26, and we expect fewer going into '27. We are expecting that program integrity will have an impact, and we have built that into our pricing. So I would comment that on our average 14% rate increase, the 3 things that are really driving that 14% kind of in rank order of impact, number one is trend, which is in the, call it, high single digits and then market morbidity coverage is second. 
And then we also have built in a little bit of margin expansion into pricing. So we feel like we've got a very competitive price and some really terrific products in markets. So we're optimistic about our ability to grow share next year.

**Operator** (Operator):
And we'll take our next question from Parker Snure with Raymond James.

**Parker Snure** (Analysts):
Yes. So just kind of piggybacking on the previous few questions. Just curious on your view for this annual enrollment period. There's some additional friction that's being added to the enrollment process, some enhanced social security verification, broker consent, tax verification, things like that. I understand that you think the market will be flat, but just curious if you view these procedural measures as being a material driver in this year's annual enrollment process? And could this lead to some people being thrown off? And I guess just kind of general expectations in terms of market morbidity. I know you touched on that, but just related to that specific dynamic.

**Mark Bertolini** (Executives):
Parker, I'll start by describing -- obviously, we've had a lot of preparation to try and get in front of the things for brokers in the enrollment program this year. So it will slow down the start. These systems are new to them. We did a lot of training over the summer. We even built our own capabilities on our own platform to help them as they navigate through this. But there will be a learning curve. It will be something new for them, and it will have an impact on their productivity. 
But I think that is something that they will pick up quickly enough. We're watching it every day and watching how it evolves. And obviously, we only have 4 or 5 days under our belt anyway from the standpoint of enrollment. Scott, do you want to talk about market morbidity?

**Richard Blackley** (Executives):
Yes. I would maybe call out 2 things. So first of all, just to reiterate, we're expecting that '27 will be flat to year-end '26. We do expect that some of these enhanced eligibility checks will result in some of the membership from '26 not being able to continue into '27. But we also anticipate that we're going to see a continuation of new people coming into the marketplace. We saw that in '26. We expect to see similar types of drivers for '27. So net-net, we expect the market overall to be flat to the '26 standpoint.

**Parker Snure** (Analysts):
Okay. That's super helpful. And if I can just get one more. Just curious on the fourth quarter guidance as it pertains to medical costs and MLR, it appears that it implies actually a decline in actual medical costs sequentially. I understand you'll have fewer members in the fourth quarter. But if I look back over the last 5 years or so, I don't know if 4Q medical costs have actually declined sequentially ever. 
So just curious if you can give more color on that dynamic, if there were some onetime items in the third quarter or fourth quarter? Or is it just simply lower enrollment that's driving that?

**Richard Blackley** (Executives):
Yes. I think you and I probably don't have the same math because when I look at implied fourth quarter MLR, it's in the range of, let's call it, low 90s. And we finished the third quarter with an MLR of 84%. If you add back PPD, that gets you to something like 84.8%. I think it's important when you think about the $250 million benefit of risk adjustment, all of that doesn't fall to the bottom line. 
It comes with claims. And so the -- you really -- you shouldn't be taking the risk adjustment out of the numbers. Like I think that's fundamental to the business, and it is offsetting the actual claims volumes that we're getting. So I think of -- if you want to think of a comparison, I would say I would start with an MLR in the third quarter of roughly 84.8%. And you can add a couple of points, if you want to kind of say some of that favorable risk adjustment related to the first half of the year. But from there, it is still a step-up into Q4 based on everything we're seeing around people reaching their maximum out-of-pockets, utilization, that continues to be favorable to our expectations. We feel like the step-up in Q4 MLR makes sense to us and is consistent with the trends we're seeing through this part of the year.

**Operator** (Operator):
And we'll take our next question from Stephen Baxter with Wells Fargo.

**Stephen Baxter** (Analysts):
Kind of a similar theme question. So you're lowering the risk adjustment payable expectation by 200 or 300 basis points. You're improving the MLR by 50 basis points. And then you're pointing to medical costs that I think that you're saying are modestly favorable to your expectations. So it seems like there's a pretty big difference there. And I know that you're a conservative company. But just thinking about the difference between those 2 items, if you could maybe help us bridge that, that would be super helpful.

**Richard Blackley** (Executives):
Yes. So Steve, I would say a few things. So we have $250 million of favorable risk adjustment. And then we've got $45 million of PPD. As I talked about, not all of that favorable risk adjustment drops to the bottom line. There's a portion that's being offset by claims, which are appropriate given the risk of the book but are creating higher claims costs for us. 
When I think about full year guidance that we just put out, I would say we're being -- we've only got Wakely through July. We're being prudent in making sure that we are thoughtful about the continued morbidity risk that's inherent in this marketplace. We feel like we have more than adequately covered for that in the guidance, and we're walking into good news. So we feel like we've got a very balanced target for full year operating earnings.

**Stephen Baxter** (Analysts):
Got it. Okay. And then, yes, I'd just be curious on your latest thinking on the latest CMS regulation governing 2028 open enrollment. I mean I think this was mostly codifying changes that were already made by OB3. But I would just love your feedback on that potential dynamic around maybe having less of an ability to utilize auto enrollments in 2028.

**Mark Bertolini** (Executives):
Yes. Steve, we're working on that for our 2027 plan, and we'll prepare ourselves to handle those new provisions and believe it's in the guidance that -- it will be in the guidance that we provide going forward. But it's just -- from our perspective, program integrity is really important because it stabilizes the risk pool. And we want to keep those programs moving forward. 
Our biggest fear is that we make sure that the people who should be excluded are excluded and that the people who need coverage get coverage. And so that work with CMS, because the sort of eligibility and enrollment responsibilities are split between CMS and the plans, we have to make sure that our data synchronizes. And so in our latest review of this information, we have information going back and forth between CMS and us, and I'm sure our competitors as well and say, well, wait a minute, let's look at this population and talk about what you see versus what we see and what we need to do to make sure these people, if they are eligible, get access to coverage. 
So that's an ongoing, I would call it, a flaw in the system is that we have dispersed eligibility too far between plans and CMS. You don't see that much anywhere else. And so we're working through those changes as we go through program integrity. But we support program integrity and we believe it's important.

**Operator** (Operator):
And our next question will come from Scott Fidel with Goldman Sachs.

**Scott Fidel** (Analysts):
Mark, I thought it might be helpful just given the midterm elections results yesterday. If you want to, one, talk us through like in terms of as -- now as you go to the hill and sort of speak with members and the expanded Blue Caucus, from a policy perspective, what, in particular, you'll maybe be advocating for the ACA? I know that in the prepared comments, you talked about opportunity to expand the ACA. But just curious in terms of -- is it -- I don't think it's probably as simple as you'll just advocate for sort of renewing the enhanced subsidies. 
I would assume that there's probably suggestions that you want to make as well around strengthening the foundation of the program longer term. And then from a timing perspective, do you think that '28 would be possible in terms of potentially getting the subsidies restored? Or curious just on your thoughts on timing as the Congress sort of start to '27.

**Mark Bertolini** (Executives):
So I think the first thing, Scott, you should know is that we have been working both at the state level and at the federal level. And we've actually made a lot of progress at the state level around things like CHOICE, and -- I mean, at the state level versus federal. And at the federal level, we've been pushing through CMS and through the administration ideas about how do we best support the changes that we need to make to make the ACA TAM bigger. 
And part of that is this whole eligibility issue. How do we get that right? And one of our suggestions has been that we create wallets, enhanced HSAs, if you will, that will allow people by having KYC criteria will allow them to be more sure of eligibility as people come into the program. 
We can stabilize that piece of the business that does great things for the risk pool and for growth and for our distribution channel that has to work through all these issues. Piecemeal every so often, as it has happened over the last couple of years is difficult. On the enhanced subsidies, we shall see. That's a financial discussion. We shall see how much of that comes back in. 
Will it change in form? It's going to have to be a deal before '28 between the administration and the new caucus. And we don't know how that's going to work. The President has made comments that he can work with the caucus. We have -- the caucus has been talking about the things that they want to have happen. We need to see how that relationship is actually going to work and evolve into legislation and then regulation. So I'm not holding out a whole lot in '27 toward '28 at this moment other than we will keep going forward. 
We continue to work with the administration on working on the eligibility piece. And on regulations like tax treatment for HSA purchases and defined contribution for employers, where we see a huge opportunity if we can clear some of that road blockage out of the way for them in the future. That makes the TAM bigger. That makes the ACA framework work. And we've also been talking to the Democrats as well while we've been talking to the administration about what we could do to make CHOICE a reality. 
In a lot of ways, my point of view is that what we are talking about in making a bigger individual market is very much what some of the aims of the ACA were in its initial construction. So I think we have a lot of common ground there. It could be a great place for both parties to get together and actually do something that could advantage the American public and more importantly, our economy.

**Scott Fidel** (Analysts):
That's helpful. And for my follow-up question, I wanted to toggle just over to pricing and it sounds like the average rate increases that you talked about are right in line with the market. I'm curious just from the average perspective, obviously, every pricing MSA is going to be different. But sort of a general sort of breakdown as you think about those sort of mid-teens, 14% or so sort of pricing, how are you -- how would you say that sort of breaks down between like underlying cost trend versus morbidity versus any other sort of key actuarial underwriting factors? And that's it for me.

**Mark Bertolini** (Executives):
I'll start off and then I'll pass it to Scott on the morbidity stuff. So the very basis of our network -- of our pricing structure and our plan design in every market starts with the network. And so where we have a great network relationship, and where we can -- again, all the most successful players in the ACA use narrow networks. And so you get a discount and that passes through to the customer, number one. 
Number two, what are your distribution relationships like? And what can you rely on in getting distribution done? Those are the 2 first most important requirements we assess when we go into the market. And then we look at the competitive framework, the pricing tolerance in the marketplace and then we build our models. But think of it as us underwriting that network and distribution model first as a way of deciding where our price points need to be in the market. Relative to morbidity and the intricacies of pricing, Scott, I'll just toss it over to you to add anything that you would.

**Richard Blackley** (Executives):
Yes. Scott, a few other thoughts. So first off, we are starting from a position of strength in '26. Our relative price increase this year was probably a bit lower than some of our competitors. So we've already got a very advantaged price position, then you go to a 14% price increase from there. So we think that from a competitive position, our pricing looks -- as you said, it's an MSA by MSA game, but we like how we look on the book in aggregate. 
When you think about the buildup of that 14%, again, it's in rank order starts with trend, which we've built in something that's in the high single digits for trend. Then you've got that impact from market morbidity related to some of the PI initiatives that we've discussed. And then on top of that, we've got a bit of margin enhancement that we also built into price. So those are the building blocks on the pricing.

**Operator** (Operator):
[Operator Instructions] And we'll go next to the line of Jonathan Yong with UBS.

**Jonathan Yong** (Analysts):
I guess just based on the landscape file, it does look like one of your competitors has gotten a little bit more, I'll call it, aggressive in terms of how they're pricing and coming in as the cheapest option in the market. I guess from your perspective, how do you consider your pricing relative to that? And is it most important to be at the cheapest end of the market? Or how are you viewing that alongside metal tier mix for 2027?

**Richard Blackley** (Executives):
I'll start on price.

**Mark Bertolini** (Executives):
Go ahead, Scott.

**Richard Blackley** (Executives):
Okay, go ahead, Mark.

**Mark Bertolini** (Executives):
I was just going to say that, obviously, metal mix that matters very much, number one. Number two, we believe that it's not just price, it's the quality of the product, quality of customer service. We tend to have higher retention than our competitors do as a result. We have higher NPS scores. So as we look at all of that, it's a mix of capability and our relationship with our customers and our distribution channel that matter. It's not just a price point. Scott?

**Richard Blackley** (Executives):
Yes, I think you hit on it. The point I was going to make, Mark, is that it's really a question of -- you have to be within a relatively reasonable range of the lowest. We feel like we've got really strong price positions in our markets and Mark talked about the distribution and the right products. And we feel like we've got great relationships with our distribution partners, and we have a product that -- we're a member-centric company. We've got a very good brand when it comes to supporting members, and that's a big part of our selling package. And that -- we think that matters beyond just price.

**Jonathan Yong** (Analysts):
Okay. Great. And then just going back to the proposed rules for payment year or for 2028. I guess in relation to the pre-verification open enrollment period that is being proposed, do you see this as kind of a benefit in terms of making sure members get enrolled given the pressure on auto enrollment? And then similarly, does this create pressure on G&A from your perspective where brokers may ask for more in terms of commissions, et cetera? Just curious how you're thinking about that.

**Mark Bertolini** (Executives):
We solve that problem first, Jonathan, by going after -- I always like to say brokers like to maximize revenue per joule of energy expended. And so if we can provide tools to them, which we have through Lucie and our EDE, the opportunity is for them to be able to keep their productivity while being able to go through each of these steps. And so that's part of what we've been doing all along. That's what we did when the enhanced subsidies went away. 
We made it easy for them to move people to new products. And they moved some of our competitors' people to our new products as a result. So I think you have to look at it from the -- again, from the perspective of what do they need to do, how can we help them with tools. And it doesn't necessarily mean that we have to have the highest commissions. As a matter of fact, and Scott, I check with you on this. I believe we are not the highest commission program in the country.

**Richard Blackley** (Executives):
That's right. I mean our commission strategy generally is to be competitive, but we don't feel like we need to be the highest. I think that the products and the service sells itself.

**Operator** (Operator):
And we'll take our next question from Michael Ha with Baird.

**Hua Ha** (Analysts):
As you look at '27, I know you're expecting stabilizing metal mix next year. But I wanted to ask your thoughts on like a potential scenario where bronze members could trade up into gold, meaning like could there be an environment where bronze members, maybe they deferred care this past year because of the higher deductibles? Could that have worsened their health or acuity? And so next year, then they shift to gold, lower deductibles, unlock care for members that previously deferred. 
Like how are you thinking about the possibility of that happening? How much of that migration have you assumed? Like what allowance would you build in your '27 pricing that has some sort of catch-up utilization beyond your normal gold plan assumptions?

**Richard Blackley** (Executives):
Well, I will start off by saying you are correct. We do expect a similar metal mix. We're not seeing any kind of thematic things that would suggest that there's some delay in utilization, right? It's not like 2026 where we were worried, and then we built in an expectation of higher fourth quarter utilization because people knew they were losing their subsidy. I don't think that's quite what we're seeing. 
And on the MOOP side, at maximum out-of-pockets, we are seeing a progression there, which looks to us like behavior that we have seen over a longer period. So again, it doesn't look like people are not using care because they've got a deductible that they have to cover a portion of those costs. So when I kind of pull back and I look at the pricing build that we did for '27, we think we've done the appropriate amount of risk analysis of where in the metals do we see people growing, what does utilization look like? And we're excited about the products we've got out in the market and about our opportunity for the year.

**Mark Bertolini** (Executives):
Michael, I would add just one thing about Lucie. So Lucie helps people find the right plan in the ACA, not necessarily an Oscar plan, but also connects them to a thing called Allstate Health Solutions that offer coverage for higher deductibles on a premium basis. So people can actually buy protection based on that underlying cover. So they have more than an option of just going up to gold, they could consider a plan like Allstate Health Solutions that helps cover some of those expenses when they occur.

**Hua Ha** (Analysts):
Interesting. Helpful. And my next question, just the one key remaining question to me after your ID was really the latest Wakely data that confirms the stabilizing risk pool even after all these CMS lives were removed, identified lives. I just wanted to ask if you could provide a bit more detail on what that Wakely file showed about market morbidity relative to your assumptions. 
And also of all the new integrity measures, all the verification checks, everything new happening next year, curious, which one do you think has the biggest range of uncertainty and how it could impact membership into next year?

**Richard Blackley** (Executives):
Yes. Well, a lot to unpack there. I would say that with respect to Wakely, latest Wakely white paper shows market morbidity moving as we would have anticipated. And I think that it just reaffirms the estimates that we've been making are appropriate, slightly favorable to our pricing expectations. 
I do think it's important to note that the first Wakely risk report we got in the first quarter was quite favorable. We got that in the second quarter. And then the report that we received in the third quarter is now moderately favorable. We think that is the effect of the CMS program integrity efforts and removing some lives and those are mainly non-utilizers. So we still believe, though, that market morbidity continues to be moderately favorable to where we priced and we're -- we think that gives us a good position for closing out '26.

**Operator** (Operator):
And we'd like to take our next question from Kevin Fischbeck with Bank of America.

**Joaquin Eduardo Martinez** (Analysts):
This is Joaquin Arriagada Martinez on for Kevin. I just wanted to ask about on the 17% to 18% risk adjustment range that you guys gave, is this something that will continue in 2027? Or does that reset back to the 20% range?

**Richard Blackley** (Executives):
Yes. I would say that the 17% to 18% for this year is specific to the risk of the book. And so we'll give you guidance on where we think next year is going to come out. And it really depends on the books and the markets and the metal mix. So I wouldn't want to get ahead of our full year guidance.

**Joaquin Eduardo Martinez** (Analysts):
All right. And could you give us some more color on the trend commentary? What specifically in outpatient is higher? And how are you translating that to your initiatives?

**Richard Blackley** (Executives):
Yes. We do see a bit of a trade-off between inpatient and outpatient, which is honestly beneficial for the cost of the member. It's beneficial to us. It's a lower -- typically a lower cost of care. And this is really doing things that are -- some of it is being driven by affordability initiatives that we're executing, which is really kind of just the fundamental blocking and tackling of how you run a health plan. 
It's things like making sure that we're doing clinical reviews that are looking at distinguishing observation from inpatient admissions, things like discharge planning, making sure that, that is done in appropriate time frames. So nothing that I think is out of the ordinary in terms of what we see with the health plan. We're just -- as Mark likes to say, we're constantly trying to progressively eliminate failure. 
And we're seeing the benefits of that strong operating cadence in both the results on the MLR side, on lower DCPs. So overall, I think that you can see the evidence that we're running a very effective health plan in the numbers.

**Operator** (Operator):
At this time, we have reached our allotted time for questions. We'd like to thank everybody for joining today's conference call. Please feel free to disconnect at any time.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### OSCR_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：全年營運盈餘財測上調至 5 億～7 億美元，較先前上調 2.5 億（原話："an increase of $250 million from our prior outlook."）
- 2026-08-06｜CFO｜guidance：全年營收財測維持 187 億～190 億美元（原話："to expect total revenues of $18.7 billion to $19 billion."）
- 2026-08-06｜CFO｜guidance：全年 MLR 財測 81.5%–82.5%,中點改善 90bp（原話："an improvement of 90 basis points at the midpoint"）
- 2026-08-06｜CFO｜guidance：SG&A 費用率財測中點改善 20bp（原話："an improvement of 20 basis points at the midpoint."）
- 2026-08-06｜CFO｜guidance：調整後 EBITDA 約高於營運盈餘 1.15 億（原話："run roughly $115 million above earnings from operations."）
- 2026-08-06｜CFO｜guidance：財測未全額計入 Wakely 早期有利數據（原話："we have not taken full credit for that"）
- 2026-08-06｜CFO｜guidance：若有利趨勢持續，可能是全年財測順風（原話："that could present a tailwind to our full year outlook."）
- 2026-08-06｜CEO｜guidance：下半年預期會員流失(churn)約為先前 1–2% 的兩倍，屬時間遞延（原話："It's probably going to be closer to twice that amount."）
- 2026-08-06｜CFO｜guidance：Q4 SG&A 費用率預期為全年最高（原話："the fourth quarter will be the highest SG&A ratio"）
- 2026-08-06｜CEO｜guidance：管理層預期 MLR 隨季節性逐季走高（原話："as members burn through their deductibles."）
- 2026-08-06｜CFO｜margin：Q2 MLR 79.2%（原話："The second quarter medical loss ratio was 79.2%"）
- 2026-08-06｜CFO｜margin：前六個月風險調整占直接保費約 20%,與全年預期一致（原話："approximately 20%, consistent with our expectations"）
- 2026-08-06｜CFO｜margin：2025 年 CMS 最終風險調整報告較 Q1 應計有利約 1.6 億，Q2 全額認列（原話："approximately $160 million favorable to our first"）
- 2026-08-06｜CFO｜margin：Q2 有利前期準備金發展 1.64 億，上半年累計 2.32 億，為調整 MLR 時應剔除的數字（原話："Year-to-date, that's $232 million."）
- 2026-08-06｜CFO｜margin：上半年門診利用率偏高，其餘類別有利（原話："we're basically getting there a year ahead of plan."）
- 2026-08-06｜CEO｜margin：Q2 SG&A 費用率創歷史新低 14.2%,稅與交易所費用上升被變動成本效率抵銷（原話："we're basically getting there a year ahead of plan."）
- 2026-08-06｜CFO｜margin：風險調整付款方屬性來自會員較年輕健康、偏都會（原話："we're a risk adjustment payer because"）
- 2026-08-06｜CEO｜competition：管理層稱單一平台單一資料集，AI 規模化部署領先同業（原話："we have one platform, we have one data set."）
- 2026-08-06｜CEO｜competition：2027 費率環境至今被管理層描述為理性（原話："We believe the market so far has been rational."）
- 2026-08-06｜CEO｜product：Oswell 放射科試點：會員選推薦院所比例與節省金額（原話："1 in 4 members choose Oswell's recommended site of care and"）
- 2026-08-06｜CEO｜product：ICHRAx 提供 ICHRA 運行軌道（原話："which has not been the case in the past."）
- 2026-08-06｜CEO｜product：AI 藥局醫務經濟方案預期年節省數千萬美元（原話："We expect these capabilities to generate tens of millions"）
- 2026-08-06｜CEO｜product：銅級/金級新產品，會員由銀級轉移（原話："from silver into higher deductible Bronze"）
- 2026-08-06｜CFO｜risk：CMS 計畫完整性相關影響已納入全年財測（原話："I don't think this is an area that we see as a risk to"）
- 2026-08-06｜CEO｜risk：IDR 不是成本趨勢驅動因素（原話："IDR is not a trend driver."）
- 2026-08-06｜CEO｜risk：預期會被取消註冊的會員不認列營收（原話："we don't recognize revenue for members that we"）
- 2026-08-06｜CEO｜customer：Q2 末 296 萬有效會員，季增約持平（原話："which is basically flat in the second quarter."）
- 2026-08-06｜CEO｜customer：Wakely 首份 2026 理賠型市場罹病率報告有利於預期（原話："market morbidity is also favorable to our expectations,"）
- 2026-08-06｜CFO｜capital_allocation：現金與投資約 102 億美元（原話："approximately $10.2 billion of cash and investments"）
- 2026-08-06｜CFO｜capital_allocation：保險子公司超額資本 9.94 億（原話："including $994 million of excess capital"）
- 2026-08-06｜CEO｜commitment：將於 9/16 投資人日說明持久成長與長期價值（原話："We will outline how we translate that performance into"）
- 2026-08-06｜CEO｜commitment：管理層稱 2027 若有 NBPP 變動，有能力調整產品與定價（原話："we have an opportunity to change product and pricing"）
- 2026-08-06｜CEO｜commitment：管理層稱 2026 稅收抵免影響已過（原話："We think we're through all the enhanced premium tax credits"）

### OSCR_Analyst_Investor_Day_Oscar_Health_Inc_20260916.md
- 2026-09-16｜CEO Mark Bertolini｜guidance：2026 營業盈餘財測上修（原話："guidance is up $600 million to $800 million"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2026 全年 MLR 財測上修 50bp 至 81–82%（原話："50 basis points to 81% to 82%"）
- 2026-09-16｜CFO Scott Blackley｜guidance：營業盈餘新區間為原財測的兩倍（原話："which is double our original guidance"）
- 2026-09-16｜CFO Scott Blackley｜guidance：其餘 2026 財測不變（原話："guidance that we have for the year remains unchanged"）
- 2026-09-16｜CEO Mark Bertolini｜guidance：2026 SG&A 比率區間不變、營收 187–190 億（原話："$18.7 billion to $19 billion in revenue"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2027 營業利益率預期高於 5%（原話："our 2027 operating margin will be greater than 5% next year"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2027 EPS 預期高於 2.25 美元（原話："our 2027 EPS will be greater than $2.25 a share"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2027 有效稅率預期維持個位數中段（原話："continue to be in the mid-single digits"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2027 正式財測留待明年二月法說（原話："specific guidance on 2027 at our investor call next February"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2029 目標：營業利益率 5–7%（原話："5% to 7% operating margin by 2029"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2029 目標：EPS 大於 4 美元（原話："EPS of greater than $4 per share by 2029"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2029 假設稅率與股數（原話："diluted share count will grow at around 2% to 3% per year"）
- 2026-09-16｜CFO Scott Blackley｜guidance：投資收益 2029 前年增 10–15%（原話："at a rate of around 10% to 15% per year"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2026 底 ACA 市場約 1,700 萬人並持平至 2027（原話："around 17 million lives in the total ACA"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2027 費率調幅與全國平均大致相當（原話："rate increases are largely in line with national averages"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜guidance：2027 Oscar 調幅 14%，競爭者平均 15%（原話："14% rate increase and the competitors are on average of 15%"）
- 2026-09-16｜CFO Scott Blackley｜guidance：CMS 100 萬人清查已處理並反映於 Q3；另有約 50 萬人第二輪（原話："a second smaller CMS program later this year"）
- 2026-09-16｜CFO Scott Blackley｜guidance：CMS 清查影響已完整反映於財測（原話："we have fully reflected the impact of these programs"）
- 2026-09-16｜CFO Scott Blackley｜margin：MLR 目標接近 80%（原話："approaching 80% is our target"）
- 2026-09-16｜CFO Scott Blackley｜margin：管理層說明 2029 利潤率區間高於歷史 3–5%（原話："higher than what we've seen historically in the 3% to 5%"）
- 2026-09-16｜CFO Scott Blackley｜margin：固定成本占比 2024 年 30% 降至今年約 25%（原話："gone from 30% back in 2024 to around 25% this year"）
- 2026-09-16｜CFO Scott Blackley｜margin：約 10% 的 SG&A 屬 ACA 結構性成本（原話："about 10% of our SG&A is structural to the ACA"）
- 2026-09-16｜CFO Scott Blackley｜margin：Lucie 規模化後利潤率為核心保險的 5–6 倍（原話："5 to 6x greater than our core insurance business"）
- 2026-09-16｜CEO Mark Bertolini｜margin：每 10 萬會員的 Lucie 利潤率假設（原話："35% on the first 2 and 80% in Consumer Health Products"）
- 2026-09-16｜CFO Scott Blackley｜margin：每 10 萬會員 Lucie 營收機會 1.5 億美元（原話："$150 million revenue opportunity per 100,000 members"）
- 2026-09-16｜CEO Mark Bertolini｜margin：AI 同時影響成本與營收（風險調整、再保回收）（原話："It's a revenue enhancer because now we have the ability"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜margin：網路與技術在兩年內帶來 30 億美元的可負擔性（原話："$3 billion in affordability"）
- 2026-09-16｜CEO Mark Bertolini｜margin：AI 累計醫療成本節省（原話："$3-plus billion in total medical cost savings"）
- 2026-09-16｜Mario Schlosser｜margin：藥局理賠 agent 揪出約 2,800 萬美元藥費（原話："$28 million or so in drug costs that we probably shouldn't"）
- 2026-09-16｜CEO Mark Bertolini｜commitment：重申 2027 營業利益率至少 5%（原話："a commitment which we are reaffirming of at least 5% in 2027"）
- 2026-09-16｜CEO Mark Bertolini｜commitment：2029 營收 CAGR 20%+、利潤率 5–7%、EPS 4 美元以上（原話："continue to deliver on our 20% plus revenue CAGR"）
- 2026-09-16｜CFO Scott Blackley｜commitment：不論 Lucie 成敗，2029 EPS 目標不變（原話："deliver more than $4 of EPS in 2029"）
- 2026-09-16｜CEO Mark Bertolini｜commitment：Lucie 未納入數字（原話："We don't have Lucie in the numbers"）
- 2026-09-16｜CFO Scott Blackley｜commitment：Lucie 預期支出已計入計畫（原話："significant amount of expected spend there"）
- 2026-09-16｜CEO Mark Bertolini｜commitment：規劃流程：風險機會各配對槓桿，2025 年未撤回財測（原話："So we didn't withdraw guidance."）
- 2026-09-16｜CFO Scott Blackley｜capital_allocation：母公司現金（原話："$460 million of parent cash"）
- 2026-09-16｜CFO Scott Blackley｜capital_allocation：計畫期間預計產生 40–45 億美元資本（原話："$4 billion to $4.5 billion across the parent"）
- 2026-09-16｜CFO Scott Blackley｜capital_allocation：約 60% 資本留在保險子公司（原話："60% of our capital generation will stay within"）
- 2026-09-16｜CFO Scott Blackley｜capital_allocation：上繳母公司資金用途（原話："pursue opportunistic M&A and manage share dilution"）
- 2026-09-16｜CFO Scott Blackley｜capital_allocation：再保（quota share）日後預期減少使用（原話："over time, we will use them to a lesser extent"）
- 2026-09-16｜CFO Scott Blackley｜capital_allocation：資本優先順序首項為有機成長（原話："capital priorities start with organic growth"）
- 2026-09-16｜CEO Mark Bertolini｜competition：稱 ACA 不是終點，因 TAM 與競爭（原話："the competition would be too fierce"）
- 2026-09-16｜CEO Mark Bertolini｜competition：競爭對手將付費使用 Oscar 技術平台（原話："they will pay rents on that capability"）
- 2026-09-16｜CEO Mark Bertolini｜competition：ICHRAx 以成本加成收費，對比他家 4 美元（原話："cost-plus unlike the $4 they're paying"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜competition：Oscar 在現有區域市占約 30%，目標 35%（原話："mature our market share from 30% to 35%"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜competition：2029 全國市占目標 18%（原話："national share by 2029 of 18%"）
- 2026-09-16｜CEO Mark Bertolini｜competition：網路為 ACA 原生建構，對比同業改造（原話："retrofit those networks for ACA"）
- 2026-09-16｜CEO Mark Bertolini｜competition：價差本身不足以搶走客戶（原話："the price differential in and of itself is not enough"）
- 2026-09-16｜CFO Scott Blackley｜competition：收入成長拆解：現有區域 17–19%（原話："between 17% and 19% growth per year"）
- 2026-09-16｜CFO Scott Blackley｜competition：新市場以 5–7% 市占進入，貢獻 2–4% 成長（原話："2% to 4% revenue growth through 2029"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜competition：每年擴張 400–600 個新縣（原話："roughly 400 to 600 new counties"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜product：生活型產品 NPS 71 vs 產業 12（原話："Net Promoter Score of 71 versus an industry average of 12"）
- 2026-09-16｜CEO Mark Bertolini｜product：同場另一說法：產業 NPS 平均為 0（原話："in an industry that averages 0"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜product：生活型產品占會員不到 10%（原話："just under 10% of our total membership"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜product：HelloMeno 直接報名提升 2.5 倍（原話："2.5x increase in direct enrollment"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜product：與 Allstate 合作，2027 年銷售（原話："about 30,000 new brokers who have not written Oscar medical"）
- 2026-09-16｜CEO Mark Bertolini｜product：補充險 2027 開放投保期已有 80 萬張保單（原話："We already have 800,000 policies for open enrollment"）
- 2026-09-16｜CEO Mark Bertolini｜product：CHOICE 2026 約 50 萬人，2029 預期 250 萬（原話："We think it's 2.5 million lives by 2029."）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜product：CHOICE 2029 市占預期 3 倍（原話："we will be at 3x market share in CHOICE"）
- 2026-09-16｜CEO Mark Bertolini｜product：CHOICE 已納入數字有限，轉折點時間未知（原話："We haven't put a lot in the numbers other than these"）
- 2026-09-16｜CEO Mark Bertolini｜product：Lucie 平台 70 家以上承保人（原話："over 70 other carriers"）
- 2026-09-16｜Mario Schlosser｜product：AI 撰寫程式碼占比由 16% 升至近三分之二（原話："almost up to 2/3s of all the lines of code"）
- 2026-09-16｜Mario Schlosser｜product：Oswell 直接處理 30–40% 會員訊息（原話："solves about 30% to 40% of all member messages"）
- 2026-09-16｜Mario Schlosser｜product：事前授權：只自動核准，不自動拒絕（原話："We don't do automated disapprovals ever"）
- 2026-09-16｜Mario Schlosser｜product：AI 在稀疏資料上表現不佳（原話："They're not very good at sparse data and making that up."）
- 2026-09-16｜CEO Mark Bertolini｜risk：Medicaid 示範計畫仍在早期（原話："we're still early in that process"）
- 2026-09-16｜CEO Mark Bertolini｜risk：顧問端預期出現長期對抗（原話："is going to be a fight over time"）
- 2026-09-16｜CFO Scott Blackley｜risk：2026 定價已假設市場萎縮 30%（原話："We priced for a market that we expected to contract by 30%."）
- 2026-09-16｜CFO Scott Blackley｜risk：成員自付額進度符合預期（原話："are in line with our expectations"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜customer：2025 年營收與會員各成長 60%、利潤率擴 7 點（原話："60% membership growth, 60% revenue growth and 7 points"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜customer：經紀分銷成長 60%（原話："we grew our distribution by 60%"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜customer：生活型產品每年為會員省近 1,000 美元（原話："saved nearly $1,000 on average each year"）
- 2026-09-16｜CEO Mark Bertolini｜customer：2029 ACA 約 2,300 萬人（原話："a total of 23 million lives in the ACA in 2029"）

### 問答異常語氣（迴避／改口／保留）
- OSCR_Q2_2026_Earnings_Call_20260806.md｜問：Justin Lake(Wolfe):CMS 100 萬名單中有多少為 Oscar 會員、能留住多少、財務影響｜答法：未給會員數或比例，改談 CMS 重視資格驗證、正在逐檔審查、影響已在財測內
- OSCR_Q2_2026_Earnings_Call_20260806.md｜問：Michael Ha(Baird):剔除 PPD 後 Q2 底層 MLR 是否約 85.2%｜答法：CFO 稱自己算約 82%,未確認 85.2%,表示會後再對帳
- OSCR_Q2_2026_Earnings_Call_20260806.md｜問：Michael Ha:下半年隱含風險調整比例與 Wakely 上行空間幅度、哪些情境會威脅全年｜答法：CEO 僅重申上半年 20% 與全年 20% 預期，未量化上行空間也未談威脅情境
- OSCR_Analyst_Investor_Day_Oscar_Health_Inc_20260916.md｜問：Goldman：投影片 45/46 的利潤率與 MLR 150bp 改善如何對應｜答法：CFO 稱想不起投影片 45 內容，改以泛稱的負擔能力措施與 2029 年 80% MLR 目標回答，未逐項拆解 150bp
- OSCR_Analyst_Investor_Day_Oscar_Health_Inc_20260916.md｜問：UBS：2029 年 G&A 降至 15% 以下需要什麼｜答法：CEO 只答「Scale, AI」，未給 SG&A 拆解或數字
- OSCR_Analyst_Investor_Day_Oscar_Health_Inc_20260916.md｜問：BofA：CHOICE 方案是否承受立法/費率風險｜答法：CEO 答以「依預期組合定價」並描述雇主定額做法，未直接回應立法風險；CFO 改談 ACA 長期趨勢
- OSCR_Analyst_Investor_Day_Oscar_Health_Inc_20260916.md｜問：Jefferies：市場由 2,300 萬降到 1,700 萬、逾 900 萬人流失對風險組合的影響｜答法：CFO 回以事前假設市場收縮 30% 與定價準備，未回應流失者與留存者 MLR 差異的具體數字

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

## ⑥ 條件附卡（archetype_hint='未獲利高成長' 命中）：judge_addendum_archetype.md

<!-- source: .claude/skills/stock-analyst/references/archetype-gatesets.md sha256:d173785f92087f36 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary ∈ {金融，未獲利高成長，轉機/特殊情境，受監管公用/穩定內需} -->

# archetype 換尺 gate-set 附卡（QC-44/45/46）

## QC-44 金融（bank／insurer／broker）
archetype=金融時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：ROTCE(替FCF Margin) >15%穿越循環｜ROE且>COE~10%(替ROIC) ROE>12-15%｜跨信用循環ROTCE穩定含2008/2020壓力年(替10Y ROIC穩定) 壓力年仍正/不破底｜NIM趨勢+效率比cost/income(替毛利率定價) 效率比<~60%｜Capex/Rev不適用→operating leverage/效率比改善｜EPS+TBVPS複合+股息總回報(替EPS CAGR>20%) ~10-12%即優｜P/TBV vs ROTCE(替PEG)：Warranted P/TBV=(ROTCE−g)/(COE−g)，實際P/TBV≤warranted｜CET1 ratio(替D/E<0.7) >監管要求+緩衝(~11-13%)｜NPL/NCO趨勢+撥備覆蓋+CET1緩衝(替負債安全性)：信用品質穩、撥備足。[§QC-44]
§10估值主錨：P/TBV分位+P/E，用Warranted P/TBV判貴賤；EV/EBITDA拿掉。QC-31 signal：X改ROTCE跨循環<COE／CET1跌破監管／NPL·NCO結構惡化／重大舞弊，移除FCF·NI、EV-EBITDA、Capex觸發。§6跑道：放款·存款·AUM成長+費收業務+市佔，非TAM滲透。[§QC-44]
子型：bank＝CET1/NIM/效率比/NPL·NCO/ROTCE/P-TBV｜insurer(注意US掛牌ALV=Autoliv汽車安全件循環工業，非保險，勿誤歸)＝combined ratio<100%/float/Solvency II ratio/book value/ROE，不看NIM/CET1｜broker·交易所＝ARPU/AUC/take rate/活躍戶，常與未獲利高成長blend｜支付網絡不歸金融，走品質複利。[§子型]
batch補搜：`[ticker] CET1 ratio NIM efficiency ratio ROTCE`(bank)／`[ticker] combined ratio Solvency II book value`(insurer)；yfinance .info 給不出 CET1/NIM/效率比/NPL/ROTCE/TBV。[§batch]

## QC-45 未獲利高成長
archetype=未獲利高成長時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：Rule-of-40(營收成長%+FCF margin%，替EPS CAGR>20%) ≥40｜EV/S÷營收成長growth-adjusted或EV/gross-profit(替PEG<2)｜NRR+毛利率+增量OI margin改善軌跡(替ROIC>15%，GAAP負無意義) NRR>110%/GM>65-70%｜FCF margin+轉正軌跡(替FCF Margin>15%；已正看margin升，未正看跑道+轉正路徑)｜NI負時FCF/NI比無意義→改看FCF margin絕對值+淨現金+跑道，FCF正或跑道>12個月。[§QC-45]
§10估值主錨：EV/S(+EV/gross-profit)+Rule-of-40-adjusted，轉正後接forward P/E；trailing PE/PEG拿掉。**情境樹同步改走EV/S（2026-10-12）**：FY1共識EPS≤0時程式自動切`valuation_basis=sales_multiple`，`scenario_inputs`填營收路徑×終端EV/S×終端淨負債×終端股數（形狀見尾段），不再用EPS×本益比；負債重者(淨負債/EV>30%)Bear的`net_debt_y5`須如實反映融資缺口，股權價值為負即歸零。QC-31 signal：不因GAAP NI負觸發X；X改NRR跌破100%／Rule-of-40<20連2季／毛利結構崩／現金跑道<12個月無轉正路徑／SBC稀釋失控(股數>10%/yr無營收槓桿)。§6跑道：NRR+淨增客戶+TAM滲透+SBC-adjusted轉正時程。blend：fintech broker常＝金融×未獲利，兩套都跑、標背離。[§QC-45]

## QC-46 轉機／受監管公用（輕量尺，不展開大表）
轉機/特殊情境：§4/§10主錨→資產重估/SOTP/normalized earning power/P-TBV，非成長外推；EPS-CAGR/PEG不適用。Single Thing→轉機觸發(債務重組完成/出售虧損部門/新管理層/catalyst里程碑)，非「moat擴張」。§6/§5→「為何現在會轉」catalyst+下行保護(資產底/清算價值)。QC-31 X→流動性危機(跑道<12個月+無再融資)/重整失敗/治理舞弊。[§QC-46轉機]
受監管公用/穩定內需：§4/§10主錨→DDM/殖利率+股息成長/regulated ROE(rate base×allowed ROE)/P/B；PEG/高成長門檻不適用。§6成長→rate base成長+費率案(rate case)+准許ROE，非TAM滲透。§5護城河→監管特許/天然獨佔(single-axis)。QC-31 X→准許ROE結構下調/費率案連敗/監管轉敵/過度槓桿(利率敏感)。[§QC-46受監管]
此兩類不強制長表，但換尺與catalyst/下行保護須sourced。[§QC-46]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260518","verdict":"觀察池 — C 級護城河 5.5 (execution 7 / pricing power 4) + ACA 補貼到期 binary 風險 + Pure MA 🟠 暫不（盲點 2 救援失效）+ 4 週 +66% 動能透支；等 2025-Q4 PTC 立法 + H2 MLR ≤84% 雙信號明朗化再評估","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"ACA Marketplace 在政策層面持續存在（無 repeal、無 single-payer）","columns":{"2Y 驗證點":"2025-Q4 enhanced PTC 立法延長 ≥ 1 年","5Y 驗證點":"2030 前無重大 ACA 結構改革","10Y 驗證點":"2035 前無 single-payer transition","具體數字門檻":"marketplace enrollment ≥ 22M（CBO 基準），OSCR 市占維持 8-12%","信息來源":"CBO / KFF 估算、CMS 月報；公司法說","漂移觸發條件":"連 2 季 OSCR 會員 YoY 下滑 ≥ 10% → 削弱"}},{"id":"H2","text":"underwriting discipline 持續，全年 MLR 落在 82-84% 區間","columns":{"2Y 驗證點":"FY2026 全年 MLR ≤ 84%","5Y 驗證點":"3 年滾動均 MLR ≤ 83%（保險業 best-in-class）","10Y 驗證點":"10 年累積 underwriting 信心建立","具體數字門檻":"全年 MLR 82.4-83.4%（管理層指引上下緣）","信息來源":"公司季報 + Earnings Call 數字","漂移觸發條件":"連 2 季 MLR 偏離指引上緣 ≥ 2pp → 削弱；連 3 季 → 反轉"}},{"id":"H3","text":"規模優勢轉化為 unit economics，SG&A 比率持續壓縮，FCF/Rev ≥ 5% 可持續","columns":{"2Y 驗證點":"FY2026 SG&A ratio ≤ 16%；FCF ≥ $1.2B","5Y 驗證點":"3 年滾動均 OIM > 2.5%（FY26 指引 1.5-2.4%）","10Y 驗證點":"10 年 ROIC 平均 > 15%","具體數字門檻":"SG&A 15.8-16.3% 指引；EBIT $250-450M","信息來源":"公司指引 / 同業對比 ELV ROIC 12-15%","漂移觸發條件":"SG&A ratio 連 2 季 > 17% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"2025 Q4 enhanced PTC 立法失敗 / 僅延 6 個月","columns":{"對應假設":"H1","時間尺度":"⚡ 短期","監測指標":"國會表決結果、CBO/Pres release","警戒閾值":"未通過 → 立即觸發；僅延 6 個月 → 部分削弱"}},{"id":"R2","text":"2026 H2 MLR 結構性超指引（utilization 飆升）","columns":{"對應假設":"H2","時間尺度":"🔥 中期","監測指標":"季度 MLR、Earnings Call utilization 描述","警戒閾值":"任一季 MLR > 86% → 削弱；> 88% → 反轉"}},{"id":"R3","text":"UNH / ELV / CNC 戰術性回歸高 OSCR 市占州","columns":{"對應假設":"H1 + H3","時間尺度":"🐢 長期","監測指標":"競爭對手 2027 ACA 計畫宣告、CMS 州別 enrollment 數據","警戒閾值":"UNH 或 ELV 宣告重返 FL/TX 任一州 → 觸發"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"C","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":23.32,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/OSCR_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
