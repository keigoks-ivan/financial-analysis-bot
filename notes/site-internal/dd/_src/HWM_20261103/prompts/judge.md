你是 stock-analyst **v20 判斷 agent**，標的 HWM（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"HWM","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HWM_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HWM_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":2703,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.howmet.com/press-release/2026-10-29/howmet-aerospace-reports-third-quarter-2026-results/"},"note":"未取得（新聞稿未載；未另查）"},{"id":"f_kpi1_non_gaap_adjusted_operat","label":"Non-GAAP (adjusted) operating margin","value":29.1,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.howmet.com/press-release/2026-10-29/howmet-aerospace-reports-third-quarter-2026-results/"},"note":"未取得（新聞稿未載；未另查）"},{"id":"f_kpi2_gaap_operating_margin","label":"GAAP operating margin","value":28.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.howmet.com/press-release/2026-10-29/howmet-aerospace-reports-third-quarter-2026-results/"},"note":"未取得（新聞稿未載；未另查）"},{"id":"f_kpi3_adjusted_ebitda_margin","label":"Adjusted EBITDA margin","value":32.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.howmet.com/press-release/2026-10-29/howmet-aerospace-reports-third-quarter-2026-results/"},"note":"未取得（新聞稿未載；未另查）"},{"id":"f_kpi4_free_cash_flow","label":"Free cash flow","value":562,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.howmet.com/press-release/2026-10-29/howmet-aerospace-reports-third-quarter-2026-results/"},"note":"未取得（新聞稿未載；未另查）"},{"id":"f_kpi5_stock_based_compensation","label":"Stock-based compensation (9M YTD)","value":80,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.howmet.com/press-release/2026-10-29/howmet-aerospace-reports-third-quarter-2026-results/"},"note":"未取得（新聞稿未載；未另查）"},{"id":"f_kpi6_guidance_fy2026_revenue","label":"Guidance FY2026 revenue","value":10300,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（區間 10,290–10,310）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.howmet.com/press-release/2026-10-29/howmet-aerospace-reports-third-quarter-2026-results/"},"note":"未取得（新聞稿未載；未另查）"},{"id":"f_kpi7_guidance_q4_2026_revenue","label":"Guidance Q4 2026 revenue","value":2750,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M（區間 2,740–2,760）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 IR 新聞稿 https://www.howmet.com/press-release/2026-10-29/howmet-aerospace-reports-third-quarter-2026-results/"},"note":"未取得（新聞稿未載；未另查）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_hwm_gross_margin_pct","label":"HWM 毛利率","value":36.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hwm_operating_margin_pct","label":"HWM 營業利益率","value":28.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hwm_fcf_margin_pct","label":"HWM FCF 利潤率","value":19.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ati_gross_margin_pct","label":"ATI 毛利率","value":24.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ati_operating_margin_pct","label":"ATI 營業利益率","value":16.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ati_fcf_margin_pct","label":"ATI FCF 利潤率","value":8.4,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crs_gross_margin_pct","label":"CRS 毛利率","value":31.21,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crs_operating_margin_pct","label":"CRS 營業利益率","value":23.36,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crs_fcf_margin_pct","label":"CRS FCF 利潤率","value":10.69,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tdg_gross_margin_pct","label":"TDG 毛利率","value":59.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDG.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tdg_operating_margin_pct","label":"TDG 營業利益率","value":46.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDG.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tdg_fcf_margin_pct","label":"TDG FCF 利潤率","value":19.26,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDG.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":211.44,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-11.73,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":48.24,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":1.5,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.34 → 5.42）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.77,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.5 → 6.55）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.68 → 7.68）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.42,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.55,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":7.68,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":7.11,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 5.06 → 5.42（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":41.46,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝44.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":44.1,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":8.64,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝76.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":76.3,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":9.06,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝77.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":77.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":39.01,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 5.42，分子＝快照價 211.44","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.236,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":4114.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 4621.0、現金 507.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":397.66,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":88195.34,"period":"2026-11-03","unit":"USD m","basis":"市值 84081.34 ＋ 淨負債 4114.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":10290.59,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":11677.21,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（18 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":8.57,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 211.84 / W52 239.78 / W104 196.6 / W250 112.37 / W250 13週斜率 2.5%"},{"id":"f_ma_w52","label":"52 週均線","value":239.78,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":196.6,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":112.37,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.5,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出主要對手（PCC/Berkshire、VSMPO、ATI、Lisi、Aubert & Duval 等），並稱最大客戶部分自有超合金熔爐生產葉片精密鑄件；新進入者、客戶換供應商為風險因子","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm","excerpt":"Several of Howmet’s largest customers have captive superalloy furnaces for producing airfoil investment castings for their own use.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：新進入者可能與 Howmet 產品競爭或取代之；產業整併可能使客戶改用對手","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm","excerpt":"New entrants in our markets, new product offerings, new and/or emerging technologies in the marketplace, or new facilities may compete with or replace Howmet products.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"TIKR 報導：GE Aerospace 同意以 117.5 億美元收購鑄件對手 Consolidated Precision Products，預計 2027 下半年完成（二手來源，未見一手公告）","source":"TIKR blog：Howmet Aerospace stock dropped nearly 11% after GE bought a rival casting supplier","url":"https://www.tikr.com/blog/howmet-aerospace-stock-dropped-nearly-11-after-ge-bought-a-rival-casting-supplier-heres-whether-the-selloff-is-an-overreaction","excerpt":"GE Aerospace agreed to buy Consolidated Precision Products, a rival casting maker, for $11.75 billion","as_of":"2026-09-09","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Howmet 10-K 披露：多家最大客戶擁有自有高溫合金爐，自製翼型熔模鑄件供自用；其他公司亦生產並可能與 Howmet 競爭。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm","excerpt":"Several of Howmet’s largest customers have captive superalloy furnaces for producing airfoil investment castings for their own use.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因素：客戶整併可能使合併後實體以 Howmet 競爭對手取代 Howmet，減少需求。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm","excerpt":"Consolidation within Howmet’s customer base may result in customers who are better able to exert leverage in negotiating prices and other terms of sale, or may lead to reduced demand for Howmet’s products if a combined entity replaces Howmet with a Howmet competitor with which it had prior relationships.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"GE Aerospace 同意以約 117.5 億美元收購鑄件供應商 CPP（Howmet 競爭對手），Howmet 股價下跌；市場解讀為 GE 增加自製關鍵件控制。","source":"Stockopedia/Reuters: Howmet falls after GE Aerospace agrees to buy CPP for nearly $12 billion","url":"https://www.stockopedia.com/share-prices/general-electric-NYQ:GE/news/howmet-falls-after-ge-aerospace-agrees-to-buy-cpp-for-nearly-12-billion-01a08152-09c1-7034-8b01-22bab9f38cca/","excerpt":null,"as_of":"2026-09-08","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K：RTX 與 GE Aerospace 各約占第三方銷售 11%；失去任一重要客戶可能對相關業務造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm","excerpt":"In 2025, RTX Corporation and GE Aerospace each represented approximately 11% of the Company’s third-party sales. The loss of any such significant customer could have a material adverse effect on such businesses.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K：部分最大客戶自有超合金鑄造爐，自行生產翼型精密鑄件，另有多家同業可能競爭。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm","excerpt":"Several of Howmet’s largest customers have captive superalloy furnaces for producing airfoil investment castings for their own use.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"GE Aerospace：Moody's 2026-02-02 由 A3 升 A2；S&P 2026-04-16 展望由穩定轉正面，長期 A-。","source":"GE 10-Q FY2026 (Q2)","url":"https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000049/ge-20260630.htm","excerpt":"On February 2, 2026, Moody's upgraded our long-term rating from A3 to A2, our short-term rating from P-2 to P-1 and maintained our positive outlook. On April 16, 2026, S&P revised our outlook from stable to positive, and affirmed our short-term rating of A-2 and our long-term rating of A-.","as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"GE Aerospace 2026-07 稱引擎維修與備品需求撐住，供給限制而非客戶需求才是延至 2027 的較大挑戰","source":"CP24/Reuters: GE Aerospace sees repair demand holding up despite aviation fuel shock","url":"https://www.cp24.com/news/money/2026/07/16/ge-aerospace-sees-repair-demand-holding-up-despite-aviation-fuel-shock/","excerpt":"GE Aerospace raised its 2026 profit forecast on Thursday as demand for engine repairs and spare parts held up despite high fuel prices and airline schedule cuts, leaving supply constraints, rather than customer demand, as the bigger challenge into 2027.","as_of":"2026-07-16","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Aviation Week 預測交機量 2026 1,686、2027 1,860、2028 約 2,000、2032 高峰約 2,250","source":"Aviation Week: 2026 Airliner Deliveries To Be Short Of 2018","url":"https://aviationweek.com/air-transport/aircraft-propulsion/2026-airliner-deliveries-be-short-2018-aviation-week-forecasts","excerpt":"In 2027, according to the Aviation Week forecast, the tally should hit 1,860. It could reach 2,000 deliveries in 2028 and peak in 2032 with around 2,250","as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"供應鏈限制預期持續至 2027（Deloitte 2026 展望／產業分析）","source":"Deloitte midyear update aerospace and defense industry outlook / marketscreener","url":"https://www.deloitte.com/us/en/insights/industry/aerospace-defense/midyear-update-aerospace-and-defense-industry-outlook.html","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261103","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Howmet 新承諾的資本支出因設備交期，約 2028-08 才產出產能；2026 資本支出預計逾 5 億美元；管理層稱部分客戶視 2031 產能已訂滿","source":"MarketBeat: Howmet Aerospace Q2 earnings call highlights; Finimize","url":"https://www.marketbeat.com/instant-alerts/howmet-aerospace-q2-earnings-call-highlights-2026-08-08/","excerpt":null,"as_of":"2026-08-08","retrieved_at":"20261103","affects":["thesis.H","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"GE Aerospace 以 117.5 億美元收購鑄件供應商 CPP 以擴充鑄件產能，顯示 OEM 垂直整合競爭","source":"Manufacturing Digital: GE Aerospace's $12bn Plan to Acquire Castings Supplier CPP","url":"https://manufacturingdigital.com/news/ge-aerospaces-12bn-plan-to-acquire-castings-supplier-cpp","excerpt":"The acquisition aims to expand GE Aerospace's mission-critical castings capacity amid a growing demand for commercial and defence engines.","as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因子僅以一般性條文列示反壟斷與競爭法遵循風險（含產品責任可能引發政府調查），未描述具體反壟斷調查；三次搜尋亦未找到 2026 年針對 Howmet 的 DOJ／FTC／EU 反壟斷調查報導。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm","excerpt":"These risks include, among other things, potential claims, class action lawsuits or compliance issues, including those relating to securities laws, employment laws, intellectual property rights, cyber, security and privacy, insurance, commercial matters, antitrust and competition, human rights","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：關稅、出口限制、制裁等政府限制影響原料與製造成本；2025 及 2026 初美國新關稅行政命令與他國報復使貿易環境更不穩，後續關稅不可預測。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm","excerpt":"Governmental constraints, including export restrictions, sanctions, new or increased import duties or tariffs, and countervailing or anti-dumping duties, also impact the cost of raw materials and other manufacturing and operating costs. The global trade landscape is growing more volatile, including as a result of 2025 and early 2026 executive orders in the U.S. for the imposition of new tariffs, the retaliatory counter measures by other countries and the likelihood and unpredictability of further tariffs and related countermeasures.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K MD&A：2025 年出貨地北美 72%、歐洲 22%；營運含日本、中國；關稅的時點、範圍與能否回收具不確定性；商用運輸（鍛造輪）需求受關稅相關不確定性壓抑，預期 2026 下半年起復甦。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm","excerpt":"The timing, extent, application, and level of tariffs by various governments and our ability to recover tariffs are subject to changes and uncertainties.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-07 Section 232 商用航空器、發動機及零件調查結果：未課新關稅，開啟 180 天談判期並保留日後課稅選項。","source":"Expeditors Newsflash: Section 232 Aerospace Investigation Results in No Tariffs","url":"https://info.expeditors.com/newsflash/section-232-aerospace-investigation-results-in-no-tariffs","excerpt":"Section 232 Aerospace Investigation Results in No Tariffs Posted by Timothy Miller on 7/13/26, 5:00 PM Tweet On July 9, 2026, the President of the United States issued a Proclamation announcing that no additional tariffs would result from the Section 232 investigation into imports on commercial aircraft, jet engines, and associated aircraft and engine","as_of":"2026-07-14","retrieved_at":"20261103","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2024 10-K 風險因子：部分原料與服務依賴有限來源或單一來源供應商（如海綿鈦、特殊合金），且因認證要求替代來源不易取得","source":"Howmet FY2024 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428125000011/hwm-20241231.htm","excerpt":"For certain raw materials and services, we depend on a number of limited source or sole source suppliers, such as for titanium sponge and specialized metal alloys.","as_of":"2025-02-28","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K：在歐洲、墨西哥、中國、日本等多國有營運；風險因子列示關稅、制裁、徵收、戰爭（含烏克蘭、中東）可能衝擊業務","source":"Howmet FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm","excerpt":"Howmet Aerospace has operations or activities in numerous countries and regions outside the United States, including Europe, Mexico, China, and Japan.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 10-K：多數供應以年度或長約採購，其餘靠現貨；原料可得性可能受出口國政治不穩影響","source":"Howmet FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm","excerpt":"We maintain annual or long-term contracts for a majority of our supply requirements, and, for the remainder, we depend on spot purchases.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收 $2.70B，年增 29%、內生 25%；Engine Products 第三方銷售 $1,451M（vs $1,087M，+33%，商用航太與燃氣渦輪驅動）；Fastening Systems $630M（vs $448M，+41%，含 CAM、Brunner 併購）；Forged Wheels $327M（vs $247M，+32%，鋁成本轉嫁）。Engineered Structures 未查到乾淨數字。","source":"Howmet Q3 2026 earnings release (SEC 8-K ex99-1) / finviz","url":"https://finviz.com/news/411256/howmet-aerospace-reports-third-quarter-2026-results","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 稿：管理層稱商用市場強勁，飛機訂單積壓支撐 2027 年及之後產量提升；預期中東衝突不會對備品需求造成重大影響（引擎維修入廠積壓、新一代窄體引擎需求）。","source":"Howmet Q3 2026 earnings release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0000004281/000110465926119857/tm2628456d1_ex99-1.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H","triggers"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"商用航太營收 Q1 2026 年增 20%、Q2 年增 28%；Q1 商用引擎備品 +48%，管理層提及產量上調、引擎建造庫存有限及部分市占提升。","source":"Barchart/Nasdaq: Howmet Aerospace Q1 earnings call highlights; Zacks","url":"https://www.nasdaq.com/articles/howmet-aerospace-q1-earnings-call-highlights","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"CEO 於財報電話會議稱工業燃氣渦輪（IGT）葉片全球市占逾 50%（TIKR 轉述，非公司文件）；GE 收購一家競爭鑄件供應商引發定價權與長期份額疑慮，Howmet 股價當時跌近 11%。","source":"TIKR: Howmet stock dropped nearly 11% after GE bought a rival casting supplier","url":"https://www.tikr.com/blog/howmet-aerospace-stock-dropped-nearly-11-after-ge-bought-a-rival-casting-supplier-heres-whether-the-selloff-is-an-overreaction","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"2025 年報稱銷售成長含有利產品定價與成本轉嫁，且產品漲價高於材料與通膨成本轉嫁；資本支出持續偏高以擴產支撐航太與燃氣渦輪成長及市占提升。","source":"Howmet 8-K (2026-05-28) / FY2025 filing via search","url":"https://www.sec.gov/Archives/edgar/data/0000004281/000110465926067497/hwm-20260528_d2.htm","excerpt":null,"as_of":"2026-05-28","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素稱新進入者、新產品、新興技術可能與 Howmet 產品競爭或取代之，客戶接受替代方案的意願與 AI 等技術進展可能不利業務；未指名具體替代技術。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm","excerpt":"New entrants in our markets, new product offerings, new and/or emerging technologies in the marketplace, or new facilities may compete with or replace Howmet products. The willingness of customers to accept alternative solutions for the products sold by Howmet, pricing pressure from competitors, and technological advancements or other developments, including the use of AI, by or affecting Howmet's competitors or customers could adversely affect Howmet's business, financial condition, or results of operations.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q1 2026 spares 占總營收 23%，高於 2025 全年 21%、2019 年 11%","source":"Barchart: Howmet Aerospace Q1 Earnings Call Highlights","url":"https://www.barchart.com/story/news/1861333/howmet-aerospace-q1-earnings-call-highlights","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026（2026-10-29 公布）營收 27.0 億美元、年增 29%，調整後 EPS 1.46；FY2026 指引第四度上調至營收約 103 億、調整後 EPS 5.50（2 月為 91 億／4.45）；2027 初步營收展望約 115 億（約 +12%）；回購授權增加 50 億。","source":"Stocktwits／Finviz 轉載 Howmet Q3 2026 新聞稿","url":"https://stocktwits.com/news-articles/markets/equity/howmet-aerospace-announces-5-b-buyback-raises-2026-guidance-as-q3-earnings-beat-estimates/cZUQmE7R9bA","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill 顯示 FY2026 EPS 共識 5.39（24 位分析師，截至 2026-10-17），Q3 共識 EPS 1.38／營收 26.16 億；實際 Q3 EPS 1.46 高於該共識，且新指引 5.50 高於 10 月中旬共識 5.39。","source":"Chartmill HWM estimates","url":"https://www.chartmill.com/stock/quote/HWM/estimates","excerpt":null,"as_of":"2026-10-17","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026（2026-08-06）調整後 EPS 1.33 vs 共識約 1.23–1.25；當時 FY26 指引上調至營收 100.0–100.5 億、EPS 5.23–5.27，高於先前共識約 97.6 億／5.06。","source":"Barchart／Tradestie／搜尋彙整","url":"https://www.barchart.com/story/news/3223371/howmet-aerospace-s-q2-2026-earnings-what-to-expect","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"目標價共識（財報前、非 Q3 後）：Walnut Invest 2026-08 平均 312.93（20 位，19 買 3 持有 0 賣）；Tickflow 截至 2026-07-31 平均 297.36；JP Morgan 目標 350（2026-08-10）。各站分布不一，Q3 後更新值未查到。","source":"Walnut Invest／Tickflow／Benzinga","url":"https://walnutinvest.com/stocks/hwm/forecast","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"有報導稱股價較 8 月水位低約 35%，投資人質疑 2026 年後成長；2027 展望 +12% 不到目前有機成長率的一半。","source":"Stocktwits／搜尋彙整","url":"https://stocktwits.com/news-articles/markets/equity/howmet-aerospace-announces-5-b-buyback-raises-2026-guidance-as-q3-earnings-beat-estimates/cZUQmE7R9bA","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Howmet Q3 2026 新聞稿（調整後 EPS、全年指引）","source":"Finviz 轉載新聞稿","url":"https://finviz.com/news/411256/howmet-aerospace-reports-third-quarter-2026-results","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Howmet 於 2026-04-06 完成以約 18 億美元現金收購 Stanley Black & Decker 旗下 Consolidated Aerospace Manufacturing。","source":"SEC EDGAR 8-K Item 2.01 (2026-04-06)","url":"https://www.sec.gov/Archives/edgar/data/4281/000110465926039791/tm2611168d1_8k.htm","excerpt":"On April 6, 2026, Howmet Aerospace Inc., a Delaware corporation (“Howmet Aerospace”), completed its previously announced purchase of Consolidated Aerospace Manufacturing, LLC (“Consolidated Aerospace Manufacturing”), a wholly owned subsidiary of Stanley Black & Decker, Inc., a Connecticut corporation (“Stanley Black & Decker”), for a cash purchase price of approximately $1.8 billion, subject to customary adjustments.","as_of":"2026-04-06","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-05-28 的 8-K 為分部重編（將 Whitehall 鈦合金廠從 Engine Products 移至 Engineered Structures），不影響合併損益、財務狀況或現金流；非財報錯誤重編。","source":"SEC EDGAR 8-K Item 8.01 (2026-05-28)","url":"https://www.sec.gov/Archives/edgar/data/4281/000110465926067497/hwm-20260528.htm","excerpt":"The recasting had no impact on the Company’s consolidated results, financial position or cash flows. The titanium alloy location is one of the Company’s facilities at Whitehall, Michigan.","as_of":"2026-05-28","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"搜尋未發現 Howmet 本身的新證券集體訴訟、FDA/臨床事項或近期召回/警告信；FDA 不適用其航太業務。","source":"WebSearch 多組查詢（見 queries_run）","url":null,"excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Howmet 於 2026-04-06 完成以約 18 億美元現金收購 Consolidated Aerospace Manufacturing。","source":"SEC EDGAR 8-K Item 2.01 (2026-04-06)","url":"https://www.sec.gov/Archives/edgar/data/4281/000110465926039791/tm2611168d1_8k.htm","excerpt":"On April 6, 2026, Howmet Aerospace Inc., a Delaware corporation (“Howmet Aerospace”), completed its previously announced purchase of Consolidated Aerospace Manufacturing, LLC (“Consolidated Aerospace Manufacturing”), a wholly owned subsidiary of Stanley Black & Decker, Inc., a Connecticut corporation (“Stanley Black & Decker”), for a cash purchase price of approximately $1.8 billion, subject to customary adjustments.","as_of":"2026-04-06","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"HWM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.63,"operating_margin_pct":28.01,"fcf_margin_pct":19.83,"rd_intensity_pct":0.39},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"ATI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":24.46,"operating_margin_pct":16.52,"fcf_margin_pct":8.4,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CRS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":31.21,"operating_margin_pct":23.36,"fcf_margin_pct":10.69,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TDG","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":59.57,"operating_margin_pct":46.47,"fcf_margin_pct":19.26,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDG","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SAF.PA","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SAF.PA"},"note":"quarterly_income_stmt 無資料"}],"subject":"HWM"},"financial_history":{"ticker":"HWM","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":5663000000.0,"revenue_yoy_pct":null,"gross_margin_pct":27.55,"operating_margin_pct":17.22,"net_income":469000000.0,"diluted_eps":1.11,"free_cash_flow":540000000.0,"fcf_margin_pct":9.54,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":6640000000.0,"revenue_yoy_pct":17.25,"gross_margin_pct":28.12,"operating_margin_pct":18.46,"net_income":765000000.0,"diluted_eps":1.83,"free_cash_flow":682000000.0,"fcf_margin_pct":10.27,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":7430000000.0,"revenue_yoy_pct":11.9,"gross_margin_pct":31.1,"operating_margin_pct":22.26,"net_income":1155000000.0,"diluted_eps":2.81,"free_cash_flow":977000000.0,"fcf_margin_pct":13.15,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":8252000000.0,"revenue_yoy_pct":11.06,"gross_margin_pct":34.17,"operating_margin_pct":25.81,"net_income":1508000000.0,"diluted_eps":3.71,"free_cash_flow":1431000000.0,"fcf_margin_pct":17.34,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HWM/HWM_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Howmet Aerospace Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good day, and welcome to the Q3 2026 Howmet Aerospace Earnings Conference Call. [Operator Instructions] Please note, this event is being recorded. I would now like to turn the conference over to Paul Luther, Vice President, Investor Relations. Thank you, and over to you, Paul.

**Paul Luther** (Executives):
Thank you, Danish. Good morning, and welcome to the Howmet Aerospace Third Quarter 2026 Results Conference Call. I'm joined by John Plant, Executive Chairman and Chief Executive Officer; and Patrick Winterlich, Executive Vice President and Chief Financial Officer. After comments by John and Patrick, we will have a question-and-answer session. I would like to remind you that today's discussion will contain forward-looking statements relating to future events and expectations. You can find the factors that could cause actual results to differ materially from these projections listed in today's presentation and earnings press release and in our most recent SEC filings. 
In today's presentation, references to EBITDA, operating income and EPS mean adjusted EBITDA, adjusted operating income and adjusted EPS. These measures are among the non-GAAP financial measures that we've included in our discussion. Reconciliations to the most directly comparable GAAP measures can be found in today's press release and in the appendix in today's presentation. In addition, unless otherwise noted, all comparisons are on a year-over-year basis. 
With that, I'd like to turn the call over to John.

**John Plant** (Executives):
Good morning, everybody, and welcome to Howmet's Q3 earnings call. Let's start with the highlights on Slide 4. Howmet's performance in Q3 was solid in all dimensions. Revenues at $2.7 billion were up 29% year-over-year and up 25% through organic growth. EBITDA was $879 million and was up 43% with a margin rate of 32.5%. Margins were up 40 basis points from the second quarter and year-over-year incrementals were 43% after the dampening effect of the CAM acquisition. Free cash flow in the quarter was $562 million after capital expenditure of $147 million, which was a quarterly record. The strong cash flow supported by -- share buybacks of $500 million. And in addition, gross debt was reduced by $60 million in the quarter, and we ended with approximately 1.3x net debt to EBITDA. 
We have repurchased $1.1 billion of shares to date, which is $400 million more than the total repurchases in 2025. I would like to note that our diluted share count fell to just below 400 million outstanding shares at 399.5 million at the end of Q3. Over the last 8 years, the share count has been reduced by in excess of 100 million shares. Earnings per share were $1.46, a 54% increase year-over-year, and this sets us up well to achieve the remainder of our 2026 objectives. Good progress was made on several fronts with new business being booked in line with our outlook expectations in commercial aerospace, defense aerospace and industrial gas turbines. 
Of particular note in the quarter was the 45% gas turbine revenue growth, which demonstrates both the extraordinary addition to output and even more importantly, the increased market share. Further commentary will be provided during the outlook section of the call. I'll now turn the call over to Patrick, who will provide further commentary on end market growth and segment performance.

**Patrick Winterlich** (Executives):
Thank you, John. Good morning, everyone. Please move to Slide 5. Howmet delivered another strong quarter with all end markets growing. We are well positioned for the future and continue to invest for growth. Total revenue was up 29% in the third quarter, excluding the net impact of the 3 transactions we completed this year, revenue was up 25% year-over-year, an acceleration from the 21% organic growth rate in the second quarter and 19% in the first quarter. Commercial aerospace growth was very healthy at 32%, with organic growth of 27%, driven by demand for both OE and spares. Commercial aerospace spares demand continues to increase significantly, driven by both legacy and next-generation engine programs. 
Defense aerospace growth was 10%, with organic growth of 3%, driven by spares demand, particularly on legacy fighter platforms. Commercial transport revenue was up 28%, reflecting both volume increases as the North America market recovery continued and the pass-through of higher aluminum costs. Gas turbine growth was very strong at 45% as end market demand remains robust. Growth in other markets of 48% was largely driven by the Brunner Fastening acquisition completed in February. Spares growth remained robust across Howmet's markets. Total spares revenue was up 30% to approximately $570 million and represented approximately 21% of total revenue in the quarter. In summary, continued strong performance in commercial aerospace, defense aerospace, gas turbines and commercial transportation. Moving to Slide 6, starting with the P&L. Third quarter revenue, EBITDA, EBITDA margin and earnings per share all exceeded the high end of guidance. 
On a year-over-year basis, revenue was up 29% and 25% organically, the strongest quarterly growth rate on record for Howmet. EBITDA continued to outpace revenue growth, up 43%. EBITDA margin increased 310 basis points to 32.5%. Incremental flow-through of revenue to EBITDA was solid at 43% year-over-year. Earnings per share were $1.46, up 54% compared to Q3 2025. Now let's cover the balance sheet and cash flow. The balance sheet remains a source of strength for Howmet. The quarter end cash balance was $508 million with quarterly free cash flow of $562 million. Net debt to trailing EBITDA improved to 1.3x. During the quarter, we paid down $60 million of commercial paper. Liquidity remains strong with an undrawn $1 billion revolver complemented by a $1 billion commercial paper program with $390 million outstanding from the $450 million that was drawn to support the CAM acquisition. 
Turning to capital deployment. CapEx was $147 million. The majority of our capital spend continues to be in the Engine Products segment as we continue to invest for growth in both aerospace and gas turbines markets. Investments are backed by long-term customer contracts. In the quarter, we repurchased $500 million of common stock at an average price of $265 per share. This brings year-to-date repurchases to $1.1 billion at an average price of $251 per share. We continue to be confident in strong future free cash flow. We increased the quarterly stock dividend in Q3 by 17% from $0.12 per share to $0.14 per share. Now let's move to Slide 7 to cover the segment results for the third quarter. The Engine Products team delivered exceptional performance again across revenue, EBITDA and EBITDA margin. Revenue grew 33% to $1.45 billion. Commercial aerospace was up 39% and gas turbines was up 44%. Demand continues to be strong across both original equipment and spares. EBITDA outpaced revenue growth with an increase of 57% to $567 million.
EBITDA margin increased 580 basis points to 39.1%, while absorbing approximately 520 net new employees in the quarter, positioning us well for future growth. Please move to Slide 8. Fastening Systems delivered another solid quarter. Revenue increased 41% to $630 million, including the impact from the CAM and Brunner acquisitions. Commercial Aerospace was up 42% and Defense Aerospace was up 66%. Commercial Transportation was up 6% year-over-year. Excluding the impact from acquisitions, total Fastening growth was up 10%. EBITDA increased 34% to $185 million. EBITDA margin declined 140 basis points year-over-year and 70 points sequentially, reflecting the increased revenues from CAM, which we acquired in April. Moving to Slide 9. The Engineered Structures team continues to drive improvement in the business. Revenue declined 4% to $295 million due to the divestiture of the Savannah disk forging facility. Excluding the impact of Savannah, revenue growth was 8%. We continue to focus on higher margin and stronger return opportunities in the business. 
Sequentially, revenue was up 10% from the second quarter, driven by increased commercial aerospace OE demand. EBITDA increased 9% year-over-year despite the revenue decline and EBITDA margin expanded 290 basis points to 23.7% as we continue to focus and optimize the Structures segment to maximize profitability. Please turn to Slide 10. Forged Wheels delivered another solid quarter. Revenue was up 32%, driven by higher volumes in addition to increased aluminum cost pass-through. Volumes also increased sequentially from Q2 as the North American market recovery continued. EBITDA was $86 million, an 18% increase year-over-year. EBITDA margins declined year-over-year and sequentially, reflecting the significant dilutive effect of sharply higher aluminum cost pass-through. We continue to outperform the market, driven by our premium products. Now let me turn the call back to John.

**John Plant** (Executives):
Thanks, Patrick, and let's move to Slide 11 and turn the call to the outlook. Firstly, of course, we provided guidance for Q4. Our glide path continues towards the conclusion of another good year for Howmet. The specific numbers will be commented upon in a few moments, plus our initial [ exciting ] chart of 2027. Regarding commercial aerospace, the flight schedules and load factors held up well during the summer months, both for domestic and international travel. Naturally, the Middle East was lower given the Iran conflict and its fallout. Oil prices, notably jet fuel and diesel are especially high and with the resultant effect on ticket prices, overall travel will potentially impact some schedules as we go through the winter into 2027. 
Having said that, we do not expect there to be any impact on our spares deliveries during this period and indeed throughout 2027. In fact, we expect solid demand given the [indiscernible] issues experienced by the new generation of narrow-body engines and also the backlog of aircraft engines, which are scheduled for shop visits and the ongoing underbuild of aircraft compared to plans. And also, this means that spares demand will continue to be very robust. The current extraordinary aircraft OE order backlog will ensure that new aircraft production continues and increases throughout 2027 and beyond. We expect volume increases for the 737, the A320, the 787 and the A350 to be healthy, and they help to underpin our commercial aerospace business outlook. Defense sales continue to be strong with further increases likely in legacy aircraft build and spares.
Notably, F-35 spares continue to be healthy with an expanding fleet of aircraft. We have not yet assumed in our forward look the replenishment of inventories, which have been depleted as a result of the Iran conflict. The most important growth factor as a percent of sales is of the one sector of defense sales is that of missile parts. We are being asked to increase production significantly, albeit final agreements have yet to be concluded. We believe that Howmet's technological and operational leadership position in the industry, coupled with our ability to develop the most sophisticated turbine blades at scale in both commercial and the defense aerospace sectors will ensure that Howmet's market position and strong financial performance will continue well into the middle of the next decade and beyond. Industrial gas turbines growth and the growth we continue to look forward to with customers will strengthen, and we look forward to further increases in volumes into the future beyond the previous expectations. This impact is likely to be felt in the outer years beyond 2028 since the new capacity currently being installed is totally sold out. 
More recently, we've seen major gas turbine customers state that 2031 is now also sold out and indeed, 2032 will likely be sold out in the next 1 or 2 quarters. This growing level of demand continues into the 2030s and combined with the need for significant increases in future gas turbine spares provides us with even greater confidence. Further capacity is likely to be considered for addition, albeit within the framework of maintaining a high level of free cash flow conversion. Most importantly, the whole of the IGT growth serving broad-based demand across industrial, oil and gas as well as data centers will be completed without adding any debt to the company. Indeed, this year, we will have completed 2 acquisitions for approximately $2 billion, spent $0.5 billion on CapEx and bought back shares in excess of $1 billion. And yet our leverage level at the end of 2026 is expected to be similar to the exit level of 2025. The commercial transportation sector continues to experience North American market recovery. Production volumes continue to climb after the Q1 low point with truck OEM build slots largely full in the second half and now into the first part of 2027. The more gradual phase-in of the 2027 NOx emissions regulations should also be supportive of industry volumes going into 2027. 
While I will comment on specific Q4 numbers in a moment, the new guide has been raised from the prior outlook. But perhaps the most important view is the initial growth outlook for 2027, which is seen at 12%, plus or minus 0.5%, resulting in revenues of approximately $11.5 billion. Further refinement and underlying aircraft volume build assumptions will be provided during our February 2027 earnings call. Finally, the share buyback authorization has also been addressed by the Board and has been increased by a further $5 billion. Now moving to specific numbers for Q4. We envisage revenues to be approximately $2.75 billion, plus or minus $10 million, EBITDA at $900 million, plus or minus $5 million, earnings per share at $1.50, plus or minus $0.01. For the full year, the guidance is increased again across the board to revenues of $10.3 billion, plus or minus $10 million, EBITDA at $3.33 billion, plus or minus $5 million and earnings per share of $5.50, plus or minus $0.01. And free cash flow has been increased to $2 billion, plus or minus $50 million. 
In terms of the full year commentary, we're pleased with our sales growth of 25%, including a 22% organic growth so far this year and an earnings per share growth of over 45%. We note that free cash flow of around $2 billion represents a very healthy cash flow to revenue and the margin, a cash [indiscernible] margin of over 19%, which is at a very high level. We can now move to Q&A.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Kristine Liwag with Morgan Stanley.

**Kristine Liwag** (Analysts):
John, Patrick, PT. I guess blades and vanes remain a critical bottleneck in aerospace supply chain, which seems to be driving OEMs to take greater control of their manufacturing capabilities. We saw this with Pratt when they invested in the Asheville facility and GE announced its acquisition of CPP. John, you previously highlighted the difficulty of replicating Howmet's technology, your manufacturing yields and scale. But how do you view these vertical integration initiatives reshaping the competitive dynamics in this aerospace blades and vanes market? And what implications could they have for Howmet's future market share? And how do you think about pricing power?

**John Plant** (Executives):
Thanks, Kristine. I think the first comment I would like to make is that we have excellent relationships with all of our engine customers, so namely GE, Safran, Pratt & Whitney, Rolls-Royce to name just a few. Our investments in technology, quality and ability to invest in capacity have been fundamental to the increase in volume of modern jet engines and indeed support of the airline fleets worldwide. This capability has taken years, if not decades, to achieve. And right now, we're actually poised to further increase capacity for GE, which will take 2 years to install and then there will be a multiyear runway after that. In fact, regarding this particular capacity for GE, I was reviewing it yesterday for one of our sites, and it is a significant investment. 
We're also in dialogue with what's been called the Blue First Blade and its future industrialization in the 2030s. I know that this audience, though, likes to have quantification and numbers rather than just words. And of course, it's difficult to give dollar values since I also recognize that our competitors are listening. So I thought I'd try to provide some view, some scale, some quantification of the central thrust of your question, which was the GE acquisition of CPP. And I think it was thinking about so how do we move into the 2030s and beyond, especially given the investments I've talked about in commercial aerospace, but also you've seen us make a lot of investments in this year and already talked to the planned increase in investment in 2027 and beyond in the IGT space. And so I thought maybe I could give some quantification of this by just think about the fleet of turbines that we are enabling to be built from like 2025 through 2030 and the large increase in the fleet of turbines, which will produce for us spares demand into the 2030s.
And when we have done our modeling, we think about that increase in spares demand and just pick, let's say, 1 year. So I just picked at random like 2031 and what our expectations are in our planning assumptions is that we see the sales value increase in spares revenues from IGT in that 1 year that would exceed the total value of the sales of the first blade of our largest narrow-body engine blade to any of our customers. So -- and if you think about it, we don't expect to lose any of that business anyway. But just to try to provide and put the context, should we lose a first blade to a narrow-body engine is -- that would be more than compensated by just one thing, which would be the spares increases in the IGT segment in one year. And then, of course, we're expecting similar values of increases in 2032, 2033, 2034 and beyond, given the continued build-out that we envisage.
So let me just turn back from a quantification to back to some more, I'll say, thoughts around CPP. And when we consider their capabilities, we see them to be probably a higher order in structural castings. And that's probably augmented recently by the acquisition of Precicast from Switzerland that they closed in the last month or so. And when I think about the industry, we've heard a lot about forgings and castings, which seems to be the word that people reach for immediately. And in fact, structural castings have probably been the main pain point of the industry that commercial aerospace has suffered in recent years. And therefore, I consider the capabilities that maybe CPP has in structural castings to be possibly of a more important relevance. And when I think about it, even though Howmet has been increasing our market share, and we're actually currently considering a further build-out of another manufacturing plant in this area, maybe it will affect the scale of the plant that we're considering and indeed where we'll place that investment. But -- so we expect that we'll continue to grow even in this segment with the relative strength that CPP may have in the future. 
And then I think just turning the call into like a broader perspective for what Howmet is going to do over the next few years. I think I'd just like to return to that IGT theme. And I think it's may be worthy of updating our guide regarding growth that I provided, I think, during last year, especially in the light of our growth in 2026. And as you know, it's been above expectations. In fact, growth accelerated in the third quarter from the 30% plus revenue increases in the first and second quarters to a 45% level. And as I commented earlier, that level of growth is clearly well in excess of the land-based gas turbine industry and a result of further market share increments that we've achieved during the course of the negotiations that I referred to in recent calls. 
So what I see now is that whereas our prior commentary had been around a doubling of IGT sales from 2025 as the base year within a 3- to 5-year period. We now see this as being achieved in 3 years, so 2 years right at the front end of that. And maybe it will rise to 2.5x inside 5 years, which would take those sales to about $2.5 billion by the end of the decade. So hopefully, I've covered the perspective of the investments we're making in commercial aero, the investments that we're anticipating making right now for GE and the way that those investments will bring additional capacities on towards the end of this decade and into the 2030s. And also the impact should something like a first blade have a different destination, albeit we don't think it does. And we see growth in both commercial aero and IGT as we go into the next decade.

**Operator** (Operator):
Our next question comes from the line of Seth Seifman with JPMorgan.

**Seth Seifman** (Analysts):
Maybe just to round that out, and this might be kind of a quick one in light of your prior comments, but it might be a good time to round out. You kind of addressed fairly directly the potential impact from CPP on your plans in Aero. When you think about the IGT plans, how do you think about the role of potentially in-sourcing at SpaceX and what that might mean for the IGT market?

**John Plant** (Executives):
Thanks, Seth. I mean, first, maybe the comment I should make is that SpaceX is indeed an extraordinary company, which has almost limitless access to capital. And I guess, fundamental to their current plans as a company indeed is the build out of their data center business, I think referred to as Colossus 1 and 2. And if you study that part of SpaceX in detail, then it's clear that they sold capacity of those, let's say, ultra-modern data centers with the latest, say, custom silicon in them to other frontier AI companies such as Google and Anthropic to name a couple. I think it's important again to note that for those cutting-edge data centers, the gross margins on the tokens that you use like AI tokens is exceptional. And I'm sure you're aware of how high those are. 
And hence, the uptime and keeping those data centers going is fundamental. And indeed, you can't have interruption of service to that really important revenue stream with that level of margin. And I'm sure it's in their contracts with those frontier AI companies. Specific to that is on their recent earnings call at SpaceX, they talked about power and specifically behind the meter power and its acquisition, which is so fundamental to achieving that compute increase and switching the compute capabilities on. So to solve those power issues and to get to today's level of compute power, which is using about approximately 1 gigawatt, then SpaceX bought the APR company and its fleet of mobile gas turbines to solve the problem. And so these 69 mobile gas turbines were installed and are situated just across the state line to support Colossus. And that power is needed in addition to what power was available from the grid. And then I guess you know that by the middle of next year, those mobile turbines have to be relocated. And therefore, replacement is required. 
And I think currently to approximately 1.2 gigawatts of power level to support the Colossus center. And so my understanding from scouring the Internet and knowing a little bit about the inside of the industry, there are some 33, I'll say, fully fledged Titan turbines from Solar or Caterpillar being installed and a further 10 PROENERGY 6000 series turbines. And you're probably not surprised when I say that Howmet does supply those turbine blades to both Titan and to the LM6000 series of aeroderivative turbines. Getting a bit deeper into it. And on the recent call, Elon Musk talked about his plans going forward for 2027. And he talked about the plans to get to 20 gigawatts of power capabilities to provide the ability to turn on further compute capabilities. And this is by various means, obviously, IGT, wind, solar, the grid, et cetera, et cetera. So it's not coming from one singular source. But part of this was that gas turbines were fundamental to it. 
And if it's not 20 gigawatts, then maybe the thought was at least 10 gigawatts of power could be achieved on top of getting to 3 gigawatts capability by the midyear and to be able to turn on that additional compute capacity and then earn those high profits. And he did comment that to do this, new turbines were required, but he realized the problem is that the availability of those turbines was restricted in the industry by the availability of turbine blades. And it was commented on the call by SpaceX that these might take another 18 months to 2 years to achieve and therefore, maybe that SpaceX could accelerate the ability of power by providing the blades to those turbines, which turbine could be built, but the availability of the blades wasn't there. And my understanding is that one Asian turbine manufacturing company has agreed to supply turbines without the blades. And I assume that those are central to the capability of casting that SpaceX talks about with their special casting capabilities. 
So I think the SpaceX can take that step. And maybe even if those blades are not quite at the level that would have been for the original equipment, they can operate at a power rating maybe below the full power rating of the turbine and its full durability. But the important thing, it gets power. And if you think about it, this is all about power acquisition. And what we see generally, both for SpaceX and across the industry, that data centers are and constructors are reaching out to get power from any source. And whether it's buying power generations of turbines, I think going back to like an E-Series turbine, not today's F-Series or the more modern H-Series, just got a Series E -- and in addition to that, you've probably read about several start-ups, venture companies they're looking to get into this segment and launch new companies to provide power using aeroderivative engines, which are really at the end of life or aero engines and repurpose them off, let's say, old 737s as an example. 
And our thought is that [indiscernible] power of those companies will exist and they will start, but maybe they'll become less necessary when additional turbine capacity is brought on stream towards the end of the decade and into next decade. So I'm trying to give like a specific SpaceX answer to your question and then broaden it out into the needs of power to achieve the compute levels, which are being planned. And then I took note and you probably took note from the GE Vernova call yesterday, their earnings call, which said that now they see that their 2032 order book is largely filled. And that obviously, if you think about it, we've talked about being good through '28, good through 2030. Now it's looking at 2031, 2032 looks to be pretty booked. And so our views are now turning towards the middle of the next decade for this level of capacity. And my thought is as we see each of those then today's level of investment that we're envisaging is probably not enough. So I don't know whether that covers your specific question, Seth, and then broaden it out into a wider...

**Seth Seifman** (Analysts):
Yes, John...

**John Plant** (Executives):
What's going on for data centers...

**Operator** (Operator):
[Operator Instructions] Our next question comes from the line of Sheila Kahyaoglu.

**Sheila  Kahyaoglu** (Analysts):
John, you mentioned the Blue Blade coming in the 2030s. That's the first time we've talked about that. Obviously, your technology edge is what provides you additional content on the LEAP and GTF, and I'm sure you're first in line for the next-gen LEAP blade. Maybe can you quantify for folks how much of your growth is coming from that technology edge content increases versus just volume and price? And perhaps to that kind of question, as you think about the industry players perhaps starting from a more square one, how do you think about what supply-demand looks like today versus 2030 and 2035 and 2040?

**John Plant** (Executives):
Okay. So I guess, thematically, what we've been trying to do is step up to the needs for fuel efficiency in the industry and providing a level of capability, particularly at the front end of the hot section of the turbine, which can achieve performances at considerably higher temperatures and indeed, the pressure those turbine blades are under and therefore, the structural integrity of them. And we've been doing that and increasing it with each generation or part generations and updates during the course of the life of the engines. And everybody is familiar with the upgrades currently going on in the -- for the LEAP part of the hot section for CFM led by GE. And that's already been launched for the LEAP-1A engine for Airbus last year. And we are currently now building in considerable volumes for the LEAP-1B, albeit those volumes are, I think, going through the normal processing, which will probably lead to a launch in -- sometime during the first quarter of 2027. 
At the same time, we are also building and increasing our levels of production for the Geared Turbofan Advantage. And again, with a similar theme of increasing the thermal performance capabilities for the turbine blades for that engine. And because that has to operate at even a higher temperature level. And I've already described on previous calls about how we're approaching that. And indeed, when you think about what's going to drive the economics of aircraft going over the next, let's say, decade, given the fact that inside the decade, it's probably unlikely that we're going to see totally new aircraft from Boeing or Airbus is that further improvements to fuel efficiency will be required and hence, the need to continue to upgrade those parts of the turbines to provide that increased fuel efficiency given the -- especially today, given the cost of jet fuel and maybe what it will cost during that period of time. 
So thematically, it's just the same. What we envisage is that further OE production will be required over the next few years with the increases envisaged by the airframe manufacturers and the engines to be supplied to them, whether it's for Boeing or indeed Airbus. And if you think about it, those things are not going to stand still. There are going to be further content increases. And so I expect that we'll see during the next decade, the further capacity that's been going to be required for OE, further capacity that's going to be required to service these new, I'll say, new fleet of engines and the improvements. And I also think that fundamentally, when you put higher temperature, higher pressure into engines is that the replacement cycles actually become more frequent. And so we do envisage a very healthy spares demand over that same period of time. 
And you can see that by the build-out of further MRO shop capabilities by -- in fact, by all of the engine manufacturers. You can look at GE, Safran in particular and also Pratt & Whitney. Everybody is building that capacity for further MRO refurb capabilities. So the broad view is we're going to increase capacity, increase revenues into the Aero segment during the next 5 years and 10 years and just keep the same thing going and continue to develop our technology. And here we are, again, having already recruited in the last 5 years, probably several hundred engineers, we're going to increase our engineering staffing again in 2027 by a similar number than we did in 2025 and 2026 as an example, to keep ourselves at the forefront of all the developments.

**Operator** (Operator):
Next question comes from the line of John Godyn with Citi.

**John Godyn** (Analysts):
A follow-up on the outlook for the defense portfolio. John, you flagged that you don't have any replenishment of inventories kind of in your outlook, but the demand signals are very strong. It feels like not long ago, we were talking about IGT in a similar way. Maybe you can talk about the scale of the opportunity there and just give us whatever color you're sort of willing to offer.

**John Plant** (Executives):
Yes. Right now, defense is difficult to really give absolute clarity on in terms of expectation. Apart from thematically, what we're seeing is both the need for replenishment of inventories and parts. Of course, to some degree, we're not clear on the numbers of missions, which have been flown over the last 3 months. But I think you could assume that they've been extensive and are going to require us to provide and provision for a replenishment of spares as we go through 2027, the degree to which will probably be also guided by the defense budget rather than the current situation where we have a continuing resolution of the existing level of expenditure. So I expect that sometime after the midterm that might become more clear. At the same time, there's a lot of other questions that have to be answered in terms of truly definitizing all of the missile work that's there. It's there before us.
We've been spending a lot of time with the existing large primes and indeed some of the, I'll say, newer defense companies getting ready for really putting that into production, albeit, again, waiting for final definitization of every aspect of the contract as we do that. So again, probably my thought is that given the situation regarding missiles is that at some point after the midterms, then that will get resolved as Congress comes back and the bipartisan agreement is achieved to give us a clarity regarding the defense budget for 2027. 
And indeed, going forward, given we're now talking about not individual lots, but multiyear contracts, which are also critical to investment in this area. So while I sort of -- I'm optimistic. I think it's going to be good for us in our planning rounds. We see the opportunity. It's difficult to be precise about it, but we do expect our defense sales to be up in 2027 from what we already know. But with an agreed budget, it may become more robust for us.

**Operator** (Operator):
Our next question comes from the line of Doug  Harned with Bernstein.

**Douglas Harned** (Analysts):
So John, when you talk about IGT demand, and it's really -- it seems like a pretty extraordinary profile going forward. You're up 45% in the quarter, which suggests you've already built ahead of some of this demand, a substantial amount of capacity. And yet I think these 7 contracts that you said with the one in Japan being first, that's not even kicked in yet. So I guess, looking forward to this demand profile, can you give us a sense of sort of when these next tranches would come in? But I think more importantly, given your position and the supply-demand imbalance, how should we expect margins to trend on IGT going forward relative to the rest of the business and particularly the aero engine side?

**John Plant** (Executives):
I've talked about margins in the past, Douglas, seeing really that our IGT margins and our aerospace margins are roughly similar. I mean, should the rate of growth continue in the IGT space, then we probably would have a little bit of leverage to that volume just against the fixed costs associated with that segment. But I see it more of a continuing, I'll say, a continuum of development looking for revenue growth with healthy profitability because we really look to have long-term relationships with our customers, never seek to take advantage and because there's always tomorrow to think about. And we try to be really good partners, not only with the aero engine customers I listed earlier in response to the first call, but also for our IGT customers, and that's whether it is, as you mentioned, Mitsubishi for Japan or whether it's GE Vernova or Siemens or is it Solar, Baker Hughes and Doosan. 
We try to work with all of them in a very consistent way. And in terms of growth rates, it's also -- it's been trying to pin something on what's been a moving target -- and in fact, we're already in discussions for the willingness to capacitize for additional demand and indeed also introduce new product developments for the industry as we go through the end of the decade into the early 2030s. And so in fact, this week, it was looking at a new product introduction for a particularly sophisticated type of large IGT blade for a customer that doesn't start until 2031. And so we're looking at all of that and trying to capacitize for it, recognizing that no matter what we do, it seems like we're not going to be able to totally satisfy what the demands appear to be for 2027, as an example. So we're going to be investing -- we've invested this year. 
We're going to invest again at a higher level in 2027. And the way things are shaping is that I sense that we're going to have a very continuing high level of capital expenditure into 2028. And we keep reevaluating it. But for ourselves is that given we try to take a very clear-eyed view of capacitization is that for every year, we see an elevated CapEx then gives us a little bit of confidence about that future growth and its solidity going into the next decade. And so clearly, we're not going to invest at the sort of levels in '28 and '29 if we're not sure about those revenue increases that are going to happen in the 2030s.

**Operator** (Operator):
Next question comes from the line of Ron Epstein with Bank of America.

**Ronald Epstein** (Analysts):
Just a follow-up on Doug's question. How do you get comfortable? I mean, I think you've talked about this in the past with -- when you try to think about where the market could be in 2030 or whatever, and you have to make investments upfront here. How do you get comfortable that it's still going to be there in 2030? You know what I mean when you actually execute a decision?

**John Plant** (Executives):
Yes. I really do. I mean something that we've tried to think about a lot and the security of that demand and think about it in relation to both what we see the fundamental demand in terms of construction of data centers, permitting. We saw a few months ago, there's a lot of questions around data centers in space and what would that do and try to understand that part of the demand. I'm also spending time thinking about the future generations of chips and for example, the degree to which they'll require the same amount of cooling and therefore, electricity consumption and indeed, what's the growth rate that's anticipated by the likes of an Anthropic or an OpenAI or Grok or any of the other, I'll say, frontier models. And it's -- obviously, it's complicated in terms of kind of put it all together. 
And then we fall back on, okay, so given the need for power, what other segments could be there for us if it should stutter. And then we go to look at, for example, liquefied natural gas and the U.S. providing energy security to Europe and all the shipping of gas across the ocean. But of course, it has to be liquefied. And so compressors used for liquefaction of gas, then it's also -- you've got to get the liquefied gas from the source through pipelines to the ports and terminals. And then indeed, what's going to be the demand in Europe as we see not in the likes of short-term El Nino, but also fundamental say, changes that might be going on in climate and hotter experiences in the summer and need for air conditioning and therefore, what does that do to electricity demand and therefore, additional turbines, which are the only realistic means of addressing them in the next decade to any substantial degree. And so it's a very big picture involving many different aspects to try to bring together.
And then finally, okay, under -- what are the customer contracts that we'd like to see to make sure that we have it feel secure in providing that capacity with underpins around corridors of volumes, et cetera, while also being responsive to our customers' needs. So I'm trying to give you like all the things we think about without being like fastened on about any one of them because the assumptions do move. And the -- I will say, just the picture has been emerging for all of us over the last couple of years. But it's also something that we feel absolutely justify we should play in this sector, and we have the capabilities, in fact, some quite unique capabilities to achieve the performance required of turbine blades of this scale and this size. And also, as you can imagine, what are the turbines being considered for the future even beyond the current version of the current H-class turbines and what -- how big do they become? And are they all going air cooled blades and how sophisticated they are and the critical change of technology, which needs to be brought to bear to achieve that. So there's a lot going on, on this one, Ron.

**Ronald Epstein** (Analysts):
Yes. And then maybe just one quick follow-on. When you look at the end markets that you're confronted with today, I mean just at a very high level, how strong are they? Do you ever expect to have so much demand out of all the end markets you're in between aero, IGT, defense? I mean it seems like everything is just ripping right now.

**John Plant** (Executives):
No, we did not. I used to think to myself, well, we're sort of fortunate in one sense that airframe manufacturers weren't able to build everything because we were able to continue to drive our company forward and let's say, improve our level of earnings capability when times are really tough, and demand was going to be more robust in the future because of the lack of build of aircraft. So I used to turn that negative into a positive about where I thought. And so I'm always looking for like how can this be better for us in the future? And how do we maximize that technology buildout combined with the volume build-out. I never thought that IGT would look like it is. And so I think sometimes in life, you get lucky. And this is one of the things where I feel as though we've had some good luck. But on the other hand, I temper that with all of the things that go against you and you have to power through them. 
And so maybe I got to take a bit of the smooth and a bit of the rough. And so I quite like it. But I just don't -- at the same time, I don't want to get giddy about it and certainly overcapacitized. And that's why I spent a long time talking about the factors that I need to think about in terms of that capacitization. And some of that was exactly the conversation that I led our Board through, I'd say, 10 months ago and try to say to them, these are all the potentials, these are the issues, these are the risks. And this is what I think we need to do. And we've all coalesced into this is something that we can do, should do, and it's good for us. But you're right, I never thought that we would be seeing, I'll say, defense land-based gas turbines and aerospace all moving in a positive way, and it's straining us. I mean if you think about hundreds of engineers, thousands of production operatives. We're probably now at 7 new manufacturing plants and considering 3 more. So there's a lot going on. I mean, growth can be tough as well.

**Operator** (Operator):
Ladies and gentlemen, that was the last question for today. The conference has now concluded. Thank you for attending today's presentation. You may now disconnect. Goodbye.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### HWM_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜John Plant｜guidance：CEO 給 Q3 EBITDA 財測 8.3 億美元±500 萬。（原話："EBITDA of $830 million, plus or minus $5 million;"）
- 2026-08-06｜John Plant｜guidance：CEO 給全年 EBITDA 財測 32.3 億美元±2000 萬（全年財測再度上調）。（原話："EBITDA of $3.23 billion, plus or minus $20 million,"）
- 2026-08-06｜John Plant｜guidance：CEO 表示自由現金流對淨利轉換率維持 90% 目標。（原話："is maintained at our 90% target conversion"）
- 2026-08-06｜John Plant｜guidance：CEO 預告 11 月 Q3 法說首度提供 2027 營收展望，預期高於 2026。（原話："which we expect will be an increase over 2026"）
- 2026-08-06｜John Plant｜guidance：CEO 預期年底槓桿回到約 1 倍淨負債/EBITDA。（原話："1x net debt-to-EBITDA by year-end"）
- 2026-08-06｜John Plant｜margin：CEO 報告 Q2 EBITDA 利潤率 32.1%，年增 340bp（含 CAM 併入）。（原話："EBITDA margin in Q2 was 32.1%, an increase of 340"）
- 2026-08-06｜Patrick Winterlich｜margin：CFO 說明 Engine Products 利潤率年增 470bp 至 37.7%。（原話："EBITDA margin
increased 470 basis points to 37.7%"）
- 2026-08-06｜Patrick Winterlich｜margin：CFO 拆解 Forged Wheels：鋁價轉嫁稀釋利潤率約 360bp，但 EBITDA 金額無實質影響。（原話："diluted margins by approximately 360 basis points"）
- 2026-08-06｜Patrick Winterlich｜margin：CFO 表示 Wheels 利潤率被稀釋的情況預期至少再持續幾季。（原話："likely to continue at least for the next couple of quarters"）
- 2026-08-06｜John Plant｜margin：CEO 以 CAM 約 20%、自家約 30% 的利潤率說明併購稀釋被原有業務提升所抵銷。（原話："they were a 20% company, so we were at 30%"）
- 2026-08-06｜John Plant｜commitment：CEO 說 CAM 綜效大部分落在 2027。（原話："the majority of it comes in 2027"）
- 2026-08-06｜John Plant｜commitment：CEO 表示 CAM 對 EPS 今年約持平，2027 起轉為正貢獻。（原話："starting to see positive EPS effect in 2027 and beyond"）
- 2026-08-06｜John Plant｜commitment：CEO 將 2027 定為 CAM 最佳化計畫的重點年。（原話："to begin to drive noticeable synergies"）
- 2026-08-06｜John Plant｜capital_allocation：CEO 說今年資本支出將超過 5 億美元，2027 還要再增加。（原話："already seeing the need to further increase this in 2027"）
- 2026-08-06｜Patrick Winterlich｜capital_allocation：CFO 說明資本支出有客戶合約支持。（原話："Investments are backed by customer contracts."）
- 2026-08-06｜John Plant｜capital_allocation：CEO 預期 2027 回購金額多於 2026。（原話："we'll probably buy back more stock than we"）
- 2026-08-06｜John Plant｜capital_allocation：CEO 預期未來 12 個月股利不會再大幅調整（剛調升 17%）。（原話："I doubt we'll do much by way of change on the dividend"）
- 2026-08-06｜John Plant｜capital_allocation：CEO 表示願意考慮進一步併購。（原話："I think we have a willingness to examine further M&A"）
- 2026-08-06｜John Plant｜capital_allocation：CEO 表示目前不預期超大型併購。（原話："I'm not envisaging at this point anything mega large"）
- 2026-08-06｜John Plant｜competition：CEO 說 Howmet 在工業燃氣輪機（IGT）葉片全球市占逾 50%。（原話："market share in excess of 50% globally for turbine blades"）
- 2026-08-06｜John Plant｜competition：CEO 認為新應用與新產品導入將使市占進一步提高。（原話："leads us to believe that our market share will"）
- 2026-08-06｜John Plant｜customer：CEO 說已與 7 大 IGT 客戶中最後一家完成談判。（原話："completed negotiations with the last of our 7 major customers"）
- 2026-08-06｜John Plant｜customer：CEO 說 IGT 營收成長超出他原先預期，主因是既有資產良率改善。（原話："exceeded what I thought we would possibly do"）
- 2026-08-06｜John Plant｜customer：CEO 說日本新廠產能幾乎已被預訂完。（原話："fully spoken for. We have one casting pit left"）
- 2026-08-06｜John Plant｜customer：CEO 預期 IGT 成長將持續未來 4–5 年。（原話："we will see growth throughout the next 4 or 5 years"）
- 2026-08-06｜John Plant｜customer：CEO 說商用航空需求未因中東衝突改變。（原話："Howmet has not experienced any changes in customer demand."）
- 2026-08-06｜Patrick Winterlich｜customer：CFO 指出備件占營收比重高於歷史水準。（原話："a greater portion of our total revenue than historically"）
- 2026-08-06｜Patrick Winterlich｜customer：CFO 指出北美商用卡車輪圈量較上季回升 7%。（原話："on a sequential basis, wheels volumes were up 7%"）
- 2026-08-06｜John Plant｜customer：CEO 說緊固件已開始看到 787 等寬體機的拉貨。（原話："We are beginning to see the pull."）
- 2026-08-06｜John Plant｜product：CEO 說 LEAP-1A/1B 新技術葉片切換預期較可能在 2027 年第一季，日期未定。（原話："first quarter of 2027. But again, date not fixed"）
- 2026-08-06｜John Plant｜product：CEO 說今年下半年 GTF Advantage 仍以舊版葉片全量供應。（原話："the legacy blade at pretty full volumes"）
- 2026-08-06｜John Plant｜product：CEO 說多化學成分塗層擴產，並傾向擴建 Whitehall 廠區。（原話："it's probably more likely than not"）
- 2026-08-06｜John Plant｜product：CEO 說上週簽核商用航空新廠興建。（原話："the building of a new plant in that area as well."）
- 2026-08-06｜John Plant｜risk：CEO 表示不願為單一年度高峰而投資，需持續監控需求的可持續性。（原話："we don't want to certainly invest for a singular year peak"）
- 2026-08-06｜John Plant｜risk：CEO 說國防備件需求增加預期在 2027，尚無具體訂單。（原話："a 2027 items that is anticipated but not assured"）
- 2026-08-06｜John Plant｜risk：CEO 說飛彈增產目前尚無正式同意的增加訂單。（原話："we have nothing formally agreed by way of increased orders"）
- 2026-08-06｜John Plant｜risk：CEO 評論太空資料中心的威脅預計落在 2040–2050 年代。（原話："sometime in the 2040s or maybe in 2050s"）
- 2026-08-06｜John Plant｜commitment：CEO 對商用卡車輪圈說外部預測機構預期 2027 更強。（原話："envisaging an even stronger 2027"）

### 問答異常語氣（迴避／改口／保留）
- HWM_Q2_2026_Earnings_Call_20260806.md｜問：Ken Herbert：3–4 年後產業能否支撐比疫情前高 25–30% 的生產速率、是否投資產能。｜答法：未給具體產能或速率數字，改談新機種時程不確定與需求可持續性，稱需增產的程度「yet to be determined」。
- HWM_Q2_2026_Earnings_Call_20260806.md｜問：Seth Seifman：新產能目前利用率到哪、後續季增軌跡如何。｜答法：未提供利用率數字或季增指引，只說部分機台仍在爬升、還有設備待進。

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
{"date":"20260710","verdict":"觀望","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"商航 build-rate 爬坡 + 售後年金共振，Engine Products 2026-2029 營收 CAGR ≥ 12%","columns":{"2Y 驗證點":"737 月產 47→52、A320 向 70-75 續爬；Engine 季 YoY ≥ +12%","5Y 驗證點":"在役機隊擴大帶動售後備件 &gt; 25% 營收占比","10Y 驗證點":"2030 年代 LEAP/GTF 機隊進入 shop visit 高峰","具體數字門檻":"地板：Engine 季 TTM YoY ≥ +10%（Q1 2026 +29%、備件 +48%）","信息來源":"公司 10-K/法說；GE Aerospace/CFM LEAP 交付；Boeing 737 rate 公告","漂移觸發":"連 2 季 Engine TTM YoY &lt; +10% → 削弱；連 4 季 &lt; +5% → 反轉（QC 季節性以 TTM）"}},{"id":"H2","text":"引擎 EBITDA margin 33%→35%+，CAM（$1.8B 扣件收購）整合使 Fastening margin 續擴","columns":{"2Y 驗證點":"Engine margin ≥ 33%、Fastening ≥ 30%；CAM 綜效兌現","5Y 驗證點":"合併調整後 EBITDA margin 站穩 32%+","10Y 驗證點":"售後 mix 提升結構性抬升 margin 天花板","具體數字門檻":"地板：Engine 分部 EBITDA margin ≥ 32%（FY25 33.3% record）","信息來源":"公司分部 EBITDA；CAM pre-synergy margin &gt;20%（2026-04 完成）","漂移觸發":"連 2 季 Engine margin YoY 壓縮 &gt;100bps → 削弱；連 4 季 &lt; 30% → 反轉"}},{"id":"H3","text":"IGT/電力需求驅動 gas turbine 基礎 $1B 向 $2B 翻倍（3-5 年）","columns":{"2Y 驗證點":"Gas turbine 營收 YoY &gt; +25%（Q1 2026 +39%）","5Y 驗證點":"IGT 營收接近 $2B、佔比升","10Y 驗證點":"電力結構性缺口延續（資料中心 + 傳統公用事業）","具體數字門檻":"地板：Gas turbine 年 YoY ≥ +20%","信息來源":"公司法說（$1B→$2B 3-5 年）；GE Vernova backlog ~110GW（惟僅 ~20% 綁資料中心，80% 傳統電力 → 更抗跌）","漂移觸發":"連 4 季 &lt; +15% → 削弱；push-out 至傳統電力周期 → 重估"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Boeing 737 再爆生產/品質事件（FAA 再降速、罷工、door plug 2.0）→ OEM 訂單能見度斷點","columns":{"對應假設":"H1","時間尺度":"737 月產（現 42，目標 47→52）；FAA production rate 公告","監測指標":"⚡ 短期 ｜ 連 3 月 YoY 負或月產跌破 38 → 立即重估"}},{"id":"R2","text":"關稅（Section 232 鋁/鋼/銅 50%）轉嫁落差壓縮 margin；且商用運輸循環（Forged Wheels）已在轉弱","columns":{"對應假設":"H2","時間尺度":"合併 EBITDA margin；Forged Wheels 量 YoY（Q1 −11%）；毛利率轉嫁落差","監測指標":"🔥 中期 ｜ 合併 EBITDA margin 連 2 季 YoY 壓縮 &gt;100bps 或 Forged Wheels 拖累擴散至核心段 → 重估"}},{"id":"R3","text":"客戶垂直整合/insourcing（RTX P&amp;W $285M 先進鑄造廠 2028、GE $1B 美製產能、PCC Ravenswood $500M 鈦熔煉）+ 單晶 3D 列印良率突破 + 成長股倍數系統性壓縮","columns":{"對應假設":"H1, H3","時間尺度":"P&amp;W Asheville 鑄造廠上線進度；單晶 AM 良率（現 &lt;20%）；10Y UST；HWM/SPX Fwd PE 比","監測指標":"🐢 長期 ｜ P&amp;W 自製佔其鑄件 &gt;20% 或單晶 AM 良率 &gt;50% 或 HWM/SPX PE 比 &lt;1.8x（現 ~2.4x）→ 慢變數觸發"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"NTM Fwd P/E 回落 ≤ 35x（約 $175-195）或航太類股回檔 20%+；或售後/IGT 加速使共識 FY27 EPS 上修 >15% 重錨倍數","irr_base_pct":5.7,"ev5y_pct":22.5,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"核心","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.6,"ev5y_pct":22.5,"irr_base_pct":5.7,"max_dd_pct":-58.0,"bull_5y_price":456.0,"bear_5y_price":148.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"NTM Fwd P/E 回落 ≤ 35x（約 $175-195）或航太類股回檔 20%+；或售後/IGT 加速使共識 FY27 EPS 上修 >15% 重錨倍數","price_at_dd":273.77,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HWM_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
