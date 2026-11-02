你是 stock-analyst **v20 判斷 agent**，標的 F（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"F","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/F_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/F_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":49.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_kpi1_adjusted_ebit","label":"Adjusted EBIT","value":2.658,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_kpi2_adjusted_ebit_margin","label":"Adjusted EBIT margin","value":5.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_kpi3_gaap","label":"GAAP 營業利益","value":1.454,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_kpi4_gaap","label":"GAAP 營業利益率（自算）","value":2.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_kpi6_adjusted_eps","label":"Adjusted EPS","value":0.49,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_kpi10_adjusted_ebit","label":"全年指引 Adjusted EBIT","value":"10.5～11.0","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無"},{"id":"f_kpi12_wholesales","label":"批發量 Wholesales","value":1049,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"千輛","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[12]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_kpi13_ford_pro_ebit","label":"Ford Pro EBIT","value":1.665,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[13]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_kpi14_ford_blue_ebit","label":"Ford Blue EBIT","value":1.392,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[14]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_kpi15_ford_model_e_ebit","label":"Ford Model e EBIT","value":-1.058,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[15]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_f_gross_margin_pct","label":"F 毛利率","value":2.36,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.F.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_f_operating_margin_pct","label":"F 營業利益率","value":-3.82,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.F.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_f_fcf_margin_pct","label":"F FCF 利潤率","value":2.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.F.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gm_gross_margin_pct","label":"GM 毛利率","value":7.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gm_operating_margin_pct","label":"GM 營業利益率","value":2.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gm_fcf_margin_pct","label":"GM FCF 利潤率","value":-0.19,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_stla_gross_margin_pct","label":"STLA 毛利率","value":7.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STLA.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_stla_operating_margin_pct","label":"STLA 營業利益率","value":0.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STLA.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_stla_fcf_margin_pct","label":"STLA FCF 利潤率","value":-7.18,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STLA.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_tm_gross_margin_pct","label":"TM 毛利率","value":16.76,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tm_operating_margin_pct","label":"TM 營業利益率","value":7.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tm_fcf_margin_pct","label":"TM FCF 利潤率","value":-2.35,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_eps_gaap","label":"淨利／稀釋 EPS（GAAP）","value":2.049,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn（EPS 0.50）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_kpi7","label":"營業現金流","value":5.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_kpi8_adjusted","label":"Adjusted 自由現金流","value":4.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無（新聞稿未載）"},{"id":"f_kpi9_sbc_9","label":"SBC（前9個月累計，無單季）","value":324,"period":"2026 年前九個月（公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"2026 年前九個月（公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"不適用"},{"id":"f_kpi11_adjusted_fcf_capex","label":"全年指引 Adjusted FCF／Capex","value":"fcf_low 6；fcf_high 7；capex_low 9.5；capex_high 10.5","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm"},"note":"查無"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":12.55,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":11.61,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":54.68,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":3.8,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.84 → 1.91）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.52,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.92 → 1.91）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.95,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.11 → 2.09）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.91,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":1.91,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":2.09,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":5.52,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 1.81 → 1.91（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.27,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝97.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":97.3,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.02,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝87.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":87.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":6.57,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 1.91，分子＝快照價 12.54","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":4.781,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":140345.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 165433.0、現金 25088.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":3993.22,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":190422.34,"period":"2026-11-03","unit":"USD m","basis":"市值 50077.34 ＋ 淨負債 140345.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":175943.28,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（5 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":179702.64,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（9 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.08,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 12.61 / W52 13.16 / W104 11.61 / W250 10.86 / W250 13週斜率 -0.67%"},{"id":"f_ma_w52","label":"52 週均線","value":13.16,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":11.61,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":10.86,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-0.67,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Ford 10-K 稱產業歷來競爭激烈、產能過剩，業者以折扣與促銷維持市占；EV 政策支持減弱導致該區隔供給過剩，近季已見此類行動重現。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm","excerpt":"manufacturers typically have offered price discounts and other marketing incentives to provide value for customers and maintain market share and production levels, and we saw some of these actions resume as industry production and inventories increased in recent quarters, especially with waning policy support for EVs leading to excess supply in that market segment.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Ford 10-K 風險因子指出其產品面臨汽車及數位軟體服務產業既有業者與新進入者的重大競爭，且新進入者可能加速其重組行動。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm","excerpt":"Our plans for implementing such actions may be accelerated by shifting industry dynamics and new entrants to our industries with which we must compete.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Cox Automotive 預估 GM 與 Ford 為 2026 年美國市占流失最大的主要車廠；Ford 前九月市占約 12.5%，降近一個百分點。","source":"OCBJ / Cox Automotive：Ford US share decline slowing","url":"https://www.ocbj.com/news/ford-us-share-decline-slowing/","excerpt":"Ford: U.S. Share Decline Slowing By staff-author April 11, 2006 144 Facebook Twitter Linkedin Email Print Ford Motor Co. is seeing the rate of decline in its U.S. market share slowing, the president of the automaker’s Americas unit said on Wednesday.","as_of":"2006-04-11","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Ford 2026年7月美國銷量（Ford 品牌）年減 9.1%，年初至今減 9.5%。","source":"Ford U.S. July 2026 Sales Release","url":"https://s205.q4cdn.com/882619693/files/doc_news/2026/Aug/04/Ford-U-S-July-2026-Sales-Release.pdf","excerpt":"Ford Cars 3,406 3,406 4,229 4,229 -19.5 -19.5 32,131 32,131 27,780 27,780 15.7 15.7 Ford Brand 164,851 181,354 -9.1 1,121,367 1,239,677 -9.5 Corsair Nautilus","as_of":"2026-08-04","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Farley 於 2026-07-30 員工會議表示中國車廠可能在 5–10 年內進入美國市場。","source":"GM Authority：Ford CEO tells employees Chinese automakers could arrive in the U.S. within 10 years","url":"https://gmauthority.com/blog/2026/07/ford-ceo-tells-employees-chinese-automakers-could-arrive-in-the-u-s-within-10-years/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"GlobalData/MarkLines 預測 2026 全球輕型車產量約 91.97M（-1.2%）、2027 約 92.64M；2026/2027 預測分別下修 1.7M 與 2.5M，主因中國需求疲弱","source":"MarkLines GEN-AI forecast production 202607","url":"https://www.marklines.com/en/report/forecastprod_202607","excerpt":"the more entrenched weakness in China's LV market underpins the bulk of our 1.7 mn and 2.5 mn respective downgrades to the 2026 and 2027 global LV production forecasts","as_of":"2026-07-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"美國新車庫存 2026 年初約 76 天供給，接近歷史常態，自 2025 年過剩修正；各品牌分化（Toyota 偏緊、Chrysler/VW 仍過剩）","source":"CBT News / Cox Automotive: U.S. auto inventories stabilize entering 2026","url":"https://www.cbtnews.com/u-s-auto-inventories-stabilize-entering-2026/","excerpt":"the U.S. auto industry began 2026 with an average 76-day supply","as_of":"2026-01-06","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"BCG 研究（經 Milano Finanza 引述）估歐洲約 5.4M 輛過剩產能、35 座工廠有風險、平均稼動率 59%；Mercedes 計畫 2028 年將全球產能降至 2.2M","source":"Milano Finanza (BCG study)","url":"https://www.milanofinanza.it/news/auto-di-troppo-un-sito-ue-su-tre-2710327","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"S&P 中國評級 2026 年 4 月：產能整併是緩解中國車市競爭的主要途徑，預期 2026 年競爭激烈、短期利潤率承壓","source":"S&P Global Ratings China 2026 Auto Outlook","url":"https://www.spgchinaratings.cn/upload/20260408_2026_Auto_Outlook_EN.pdf","excerpt":null,"as_of":"2026-04-08","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Ford 2026 全年指引下修為調整後 EBIT $10.5–11.0B、調整後自由現金流 $6.0–7.0B；指引不含中東重大升級或美國經濟重大下滑","source":"Ford Form 10-Q (period ended 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000191/f-20260930.htm","excerpt":"Adjusted EBIT $10.5 - $11.0 billion; Adjusted Free Cash Flow $6.0 - $7.0 billion","as_of":"2026-09-30","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Ford CFO 2026 年 6 月稱產業層級需求仍相當不錯","source":"Ford fireside transcript, UBS 2026 Auto Tech Conference","url":"https://s205.q4cdn.com/882619693/files/doc_events/2026/Jun/03/Ford-Motor-Company-Fireside-Transcript_UBS-2026-Auto-Auto-Tech-Conference_June-3-2026.pdf","excerpt":"Demand, I think at an industry level, still looks pretty good.","as_of":"2026-06-03","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3 lists only a product liability matter (Hetsler v. Ford, $103M jury verdict under appeal) as significant pending legal proceeding; no antitrust or break-up proceeding listed there.","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm","excerpt":"Individual product liability matters that have more than a remote risk of loss and such loss would likely be significant if the matter is resolved unfavorably to us would be described herein. Currently, there is one such matter to report:","as_of":"2026-02-11","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"福特 10-K 揭露：已實施的美國及他國關稅對福特、其他車廠、供應商與經銷商造成顯著干擾與成本增加","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm","excerpt":"Tariffs implemented to date in the United States and elsewhere have caused significant disruption, increased costs, and uncertainty in the automotive industry, including for Ford, other OEMs, suppliers, and dealers, as well as customers.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025 年關稅毛成本約 30 億美元，扣除抵減後對 EBIT 淨影響約 20 億美元","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm","excerpt":"In 2025, Ford’s gross costs related to tariffs implemented or revised in 2025 was about $3 billion, including the impact of tariff relief, and the net EBIT impact was about $2 billion after offsets.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"2026 年指引預期關稅成本下降約 10 億美元（全年度抵免擴大效果）；指引未納入未公布的新關稅政策","source":"SEC EDGAR 10-K FY2025 Outlook","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm","excerpt":"We expect lower tariff costs of about $1.0 billion, reflecting a full year’s worth of credit expansion","as_of":"2026-02-11","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"中國稀土及零組件出口限制已造成福特供應鏈生產中斷與成本上升，並列為出口管制風險","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm","excerpt":"instability in the supply chain exacerbated by tariffs and other industry concerns, such as China’s restriction on the export of rare earth minerals and various components, has resulted in production disruptions and increased costs","as_of":"2026-02-11","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Novelis Oswego NY 鋁廠 2025年9月火災，該廠供應美國車用鋁板約40%，Ford 為最大客戶（F-150）；Ford 暫停至少五款車型生產，預估Q4 EBIT 逆風$1.5-2B、自由現金流衝擊$2-3B；Ford 改向 Novelis 其他廠採購","source":"Deseret News: Ford stops production of multiple vehicles","url":"https://www.deseret.com/u-s-world/2025/10/14/ford-stops-production-of-multiple-vehicles","excerpt":null,"as_of":"2025-10-14","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"第三方風險彙整站轉述 Ford SEC 申報：中國稀土與零組件出口限制已造成 Ford 生產中斷與成本上升，未來中斷風險升高；鋁供應中斷拉低 F-150 批售（原文未核，需對照 10-K/10-Q）","source":"policyrisk.com Ford (F) company page","url":"https://policyrisk.com/world/company/F","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中荷 Nexperia 晶片爭端引發 GM、Ford 股價下滑與供應鏈疑慮，車廠警告可能干擾美歐生產","source":"Stocktwits: GM, Ford Stocks Slip As China-Dutch Chip Dispute Over Nexperia","url":"https://stocktwits.com/news-articles/markets/equity/gm-ford-stocks-slip-as-china-dutch-chip-dispute-over-nexperia-sparks-fresh-supply-chain-fears/ch6rH1zR3FB","excerpt":null,"as_of":"2025-10-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"2026Q3 Ford Pro 營收 $17.8B（+2%），EBIT $1,665M（前年 $1,985M）；批發 358k（前年 373k）","source":"Ford Q3 2026 Earnings Press Release","url":"https://s205.q4cdn.com/882619693/files/content_files/Ford-Motor-Company-Q3-2026-Earnings-Press-Release.pdf","excerpt":"Ford Pro Segment Wholesales (000) 373 358; Revenue ($B) $ 17.4 $ 17.8 2 %; EBIT ($M) 1,985 1,665","as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"2026Q3 Ford Model e 批發 34k（-31%）、營收 $1.2B（-31%），EBIT 虧損約 $1.06B","source":"Ford Q3 2026 Earnings Press Release","url":"https://s205.q4cdn.com/882619693/files/content_files/Ford-Motor-Company-Q3-2026-Earnings-Press-Release.pdf","excerpt":"Ford Model e Segment Wholesales (000) 50 34 (31)%; Revenue ($B) $ 1.8 $ 1.2 (31)%; EBIT ($M) (1,410) (1,058)","as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"2026Q3 Ford Blue 營收 $27.1B（-3%），因批發下降，部分被產品組合與匯率抵銷；EBIT $1,392M","source":"Ford Q3 2026 Earnings Press Release","url":"https://s205.q4cdn.com/882619693/files/content_files/Ford-Motor-Company-Q3-2026-Earnings-Press-Release.pdf","excerpt":"Third quarter 2026 revenue decreased 3%, driven by lower wholesales, offset partially by favorable mix and exchange.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"Ford 美國銷量 2026Q3 年減 7% 至 509,764 輛；1–9 月累計 -8.6% 至 1,516,279 輛","source":"Ford Authority","url":"https://fordauthority.com/2026/10/ford-motor-company-sales-numbers-figures-results-third-quarter-2026-q3/","excerpt":"Ford Motor Company sales decreased seven percent to 509,764 units during third quarter of 2026 in the United States.","as_of":"2026-10-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"-","claim":"Experian 2026Q2：Ford 在美國新車市佔排第四、11.8%","source":"Ford Authority","url":"https://fordauthority.com/2026/09/ford-market-share-ranked-fourth-in-q2-2026/","excerpt":"Ford ranked fourth in terms of new vehicle market share among all automakers in the U.S. in the second quarter, coming in at 11.8 percent.","as_of":"2026-09-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"0","claim":"Ford 財報稱業界定價預期 +0.5%，美國 2026 銷量預期 16–16.5M，與去年相當","source":"Ford Q3 2026 earnings coverage (macaubusiness)","url":"https://macaubusiness.com/ford-reports-loss-on-ev-retreat-but-lifts-2026-forecast/","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"0","claim":"Mobility Global 預測美國輕型車 2026 為 16.1M、2020 年代末 16.4M，低於疫情前約 17M；負擔能力為主要障礙","source":"Mobility Global via DBusiness","url":"https://www.dbusiness.com/daily-news/forecast-u-s-vehicle-sales-unlikely-to-regain-pre-pandemic-levels-this-decade/","excerpt":"U.S. light-vehicle sales are expected to reach 16.1 million units in 2026 and 16.4 million by the end of the decade.","as_of":"2026-07-01","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Ford FY2025 10-K：產業產能過剩壓低價格（尤其電動化車款），EV採用率低於預期，電池成本高使EV未達與燃油車價格持平","source":"SEC EDGAR Ford 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm","excerpt":"Battery costs remain high, which is detrimental to EVs reaching pricing parity with ICE vehicles and further exacerbates the pricing pressures on EVs. Furthermore, given our existing and continued investment in battery production, if we are unable to operate battery facilities at their expected capacity because EV adoption rates or the demand for such","as_of":"2026-02-11","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"報導稱Ford CEO Farley承認中國汽車技術在全球已領先／中國品牌為北美市場存亡威脅","source":"Katadata: Ford Boss Admits Chinese Car Technology Starting to Surpass US","url":"https://auto.katadata.co.id/car/ford-boss-admits-chinese-car-technology-starting-to-surpass-us-21070","excerpt":"Chinese automotive manufacturers as a more dangerous threat than Japanese manufacturers were in the past. Therefore, US automotive brands need to prepare and continue development to compete in the global market. Photo : Carnewschina “They (Chinese car factories) have capable factory capacity there with enough assembly facilities to cover the North American market,” said Jim Farley, CEO","as_of":"2025-11-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"2026北京車展：軟體定義車輛與AI成為競爭焦點，中國品牌出口擴張並往高端移動","source":"WhichEV: Auto China 2026 show report","url":"https://www.whichev.net/2026/05/05/auto-china-2026-show-report-electric-ambition-accelerates-as-beijing-becomes-the-epicentre-of-next-generation-mobility/","excerpt":"The rise of the “software-defined EV” Perhaps the most striking theme of Auto China 2026 was the integration of artificial intelligence into electric vehicles. The modern EV is no longer defined solely by its battery or drivetrain; it is increasingly a software platform on wheels.","as_of":"2026-05-05","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K 仍描述以經銷商為主的通路：車輛、零件售予經銷商再轉售零售客戶，Ford Credit 提供經銷商庫存融資；未見直營取代經銷商的描述。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm","excerpt":"In addition to the products we sell to our dealerships for retail sale, we also sell vehicles to our dealerships for sale to fleet customers, including commercial fleet customers, daily rental car companies, and governments.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Ford 2026-05 稱 Ford Pro 軟體與服務目標占 Ford Pro EBIT 25%（2023 目標為 20%）；2026 Q1 付費軟體訂閱 +30% 至 87.9 萬，毛利率逾 50%。","source":"Ford 官方新聞／搜尋摘要（Ford charges ahead in Europe；Work Truck 報導）","url":"https://www.at.ford.com/us/en/home/news-media/news/2026/5/ford-charges-ahead-in-europe.html","excerpt":null,"as_of":"2026-05-18","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Farley 表示零售端模式仍在實驗中；2023 年提出的線上直售構想受州法限制，來源稱屬願景而非正式計畫。","source":"搜尋摘要（Work Truck Online；The Drive 2023）","url":"https://www.thedrive.com/news/ford-ceo-jim-farley-says-direct-sales-no-ads-will-sell-future-evs","excerpt":null,"as_of":"2023-06-12","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Ford 在 Q3 2026 財報把 2026 全年調整後 EBIT 指引下緣上調為 $10.5–11bn（原 $10–11bn）；FCF 指引維持 $6–7bn、capex $9.5–10.5bn（Just Auto／Earnings Whispers 摘要）","source":"Just Auto: Ford raises lower end 2026 EBIT target","url":"https://www.just-auto.com/newsletters/ford-raises-lower-end-2026-ebit-target","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Ford Q2 2026 新聞稿：全年調整後 EBIT 指引上調至 $10–11bn（原 $8.5–10.5bn）","source":"Ford Q2 2026 Press Release","url":"https://s205.q4cdn.com/882619693/files/doc_financials/2026/q2/Ford-Motor-Company-Q2-2026-Press-Release.pdf","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價共識約 $14.88（25 位，Hold；區間 $12.8–$17；另一源 Benzinga 顯示 24 位、均價 $14、高 $20、Buy）；各聚合站評級與目標價不一致，最新資料約 2026-08","source":"聚合站摘要（Benzinga／Yahoo Finance／Public.com 等）","url":"https://kr.benzinga.com/quote/F/price-targets","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"RBC 於 2026-04-30 將 Ford 目標價由 $11 調高至 $13，維持 Sector Perform","source":"Placera: RBC Raises Price Target on Ford Motor to $13 From $11","url":"https://www.placera.se/telegram/ford-motor-rbc-raises-price-target-on-ford-motor-to-13-from-11-keeps-sector-perform-rating-20260430","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Ford Q3 2026 調升 EBIT 指引下緣至 $10.5–11bn","source":"SEC 8-K exhibit 99 (July 28 2026)","url":"https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000155/exhibit99tojuly282026for.htm","excerpt":"adjusted free cash flow of $2.1 billion • Company declares a third-quarter regular dividend of 15 cents per share • Company raises full-year adjusted EBIT guidance to $10 billion to $11 billion (from $8.5 billion to $10.5 billion) and adjusted free cash flow to $6.0 billion to $7.0 billion (from $5.0 billion to $6.0 billion) DEARBORN, Mich., July 28, 2026 – Ford","as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2025-12-09 Ford 與 SK On 簽 BOSK 合資處分協議：Ford 持分被贖回、Ford 子公司取得肯塔基兩座電池廠，並認列 BOSK 資產減損及剩餘投資減損（8-K Item 2.06），預計 2026 上半年交割","source":"SEC EDGAR 8-K Item 2.06 (2025-12-15)","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799625000238/f-20251209.htm","excerpt":"Pursuant to the Joint Venture Disposition Agreement, Ford’s membership interest in BOSK will be redeemed and a Ford subsidiary will acquire the two BOSK plants and related equipment in Kentucky. Closing on the transactions contemplated by the Joint Venture Disposition Agreement is expected in the first half of 2026.","as_of":"2025-12-15","retrieved_at":"20261103","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"10-K FY2025 列示 Hetsler v. Ford 產品責任案：2024 年陪審團判 Ford 賠 1.03 億美元，Ford 已上訴","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm","excerpt":"After a trial in February 2024, a jury found Ford liable and awarded plaintiff $103 million in damages. On August 22, 2024, Ford appealed the judgment to the Fifth District Court of Appeal.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-07 報導 Ford 與吉利（Geely）在西班牙 Valencia 廠成立製造合資，Ford 持 66%、Geely 34%，待主管機關核准","source":"The EV Report: Ford, Geely Form Joint Venture at Valencia Plant（經搜尋摘要）","url":"https://theevreport.com/ford-geely-joint-venture-valencia-plant","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Stellantis FaSTLAne 2030 計畫：五年投資 €60 億級（€60bn）並削減歐洲產能約 80 萬輛/年","source":"ANSA: Stellantis to invest 60 bn in next five years, scale back capacity in Europe","url":"https://www.ansa.it/amp/english/news/business/2026/05/21/stellantis-to-invest-60-bn-in-next-five-years-scale-back-capacity-in-europe_62046dbd-7a9a-4d92-9dfd-779961d58108.html","excerpt":null,"as_of":"2026-05-21","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Volkswagen 表示將再削減約 100 萬輛產能（Blume）","source":"TimesLive: Volkswagen to further cut capacity by one million cars, says Blume","url":"https://www.timeslive.co.za/motoring/2026-04-21-volkswagen-to-further-cut-capacity-by-one-million-cars-says-blume/","excerpt":null,"as_of":"2026-04-21","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"GM 於 2025 年 6 月宣布 $40 億美國投資，Orion 汽油全尺寸 SUV/皮卡 2027 年初開產；GM 預計至 2027 年每年資本支出 $100–120 億","source":"GreentechLead: EV Factory Investment in 2026","url":"https://greentechlead.com/electric-vehicle/ev-factory-investment-in-2026-hyundais-26-billion-us-plan-toyotas-battery-plant-and-global-manufacturing-leaders-55895/amp","excerpt":"Its $4 billion US manufacturing investment announcement in June 2025 included plans to begin gas-powered full-size SUV and light-duty pickup production at Orion in early 2027.","as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Hyundai 美國 2025–2028 投資由 $210 億增至 $260 億，Metaplant America 目標 2028 年年產 50 萬輛（規劃產能）","source":"GreentechLead: EV Factory Investment in 2026","url":"https://greentechlead.com/electric-vehicle/ev-factory-investment-in-2026-hyundais-26-billion-us-plan-toyotas-battery-plant-and-global-manufacturing-leaders-55895/amp","excerpt":"Hyundai Motor Group increased its planned US investment from $21 billion to $26 billion for 2025–2028, adding $5 billion to its original commitment.","as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Ford 自身 2026 年 F-Series 產量增加逾 5 萬輛（Q1 2026 起爬升）","source":"GreentechLead / Ford Oct 2025 announcement","url":"https://greentechlead.com/electric-vehicle/ev-factory-investment-in-2026-hyundais-26-billion-us-plan-toyotas-battery-plant-and-global-manufacturing-leaders-55895/amp","excerpt":"Ford aims to increase its F-Series production volume by more than 50,000 trucks in 2026, ramping from the first quarter of 2026.","as_of":"2025-10-23","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#5","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Toyota/Lexus 上海新廠預計 2027 年投產，初期產能約 10 萬輛/年（2025 年公告）","source":"CnEVPost: Toyota to build wholly-owned plant in Shanghai","url":"https://cnevpost.com/2025/02/05/toyota-to-build-wholly-owned-plant-shanghai-lexus/embed","excerpt":null,"as_of":"2025-02-05","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Ford 經銷商庫存天數（Cox）2026-08 底為 89 天，低於 7 月 91 天、5–6 月 93 天；趨勢下降但仍高於產業平均 73 天","source":"Ford Authority, new ford inventory levels shrunk again in august 2026","url":"https://fordauthority.com/2026/09/new-ford-inventory-levels-shrunk-again-in-august-2026/","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"美國新車整體庫存 2026-09 升 4.5% 至 280 萬輛，庫存天數 82 天（8 月 75 天）；J.D. Power 預估 10 月獎勵金占 MSRP 6.3%，較去年同期高 0.7pp","source":"Cox Automotive / J.D. Power via search summaries (cbtnews, beinsure)","url":"https://beinsure.com/news/us-new-vehicle-sales-forecast-to-reach-1-33-mn-in-october-2026/","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Ford 2008 全年虧損 146 億美元（上一輪金融危機下行）","source":"GoAuto: Ford books record $US14.6b. loss","url":"https://goauto.com.au/news/ford/ford-books-record-us14-6b-loss/2009-01-30/22190.html","excerpt":null,"as_of":"2009-01-30","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Trefis 稱 Ford 股價在 2008–2009 危機中跌幅 82%（同期 S&P 500 為 53%）","source":"Trefis: How Low Can F Really Go In A Market Crash?","url":"https://www.trefis.com/stock/f/articles/599597/how-low-can-f-really-go-in-a-market-crash/2026-05-16","excerpt":null,"as_of":"2026-05-16","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2020 疫情期間 Company adj. EBIT margin 全年 2.2%（2019 為 4.1%），Q2 2020 為 -10.0%，Q3 反彈至 9.7%","source":"Ford Form 10-K FY2020 / Q3 2020 8-K","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799621000012/f-20201231.htm","excerpt":null,"as_of":"2021-02-01","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"Wards：歷史上美國車市成長 5–6 年後下行約同樣長度；下行通常 2–3 年","source":"Wards Auto: Clock Ticking for Next Auto-Sales Drop","url":"https://wardsauto.com/financials/clock-ticking-for-next-auto-sales-drop","excerpt":null,"as_of":"2001-11-01","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"-","claim":"2025-12-09 BOSK 合資處分協議：Ford 子公司取得肯塔基兩座電池廠，Ford 退出 BOSK 持分","source":"SEC EDGAR 8-K Item 2.06 (2025-12-15)","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799625000238/f-20251209.htm","excerpt":"Pursuant to the Joint Venture Disposition Agreement, Ford’s membership interest in BOSK will be redeemed and a Ford subsidiary will acquire the two BOSK plants and related equipment in Kentucky.","as_of":"2025-12-15","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"2026-07 Ford–Geely Valencia 製造合資（Ford 66%／Geely 34%），待核准；搜尋結果未見 2026 年併購","source":"The EV Report（搜尋摘要）","url":"https://theevreport.com/ford-geely-joint-venture-valencia-plant","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"10-K FY2025 列示 Hetsler v. Ford 產品責任案，判賠1.03億美元，上訴中","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm","excerpt":"After a trial in February 2024, a jury found Ford liable and awarded plaintiff $103 million in damages. On August 22, 2024, Ford appealed the judgment to the Fifth District Court of Appeal.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2024 年起 E.D. Michigan 有證券集體訴訟（Guzman v. Ford，指保固準備金低估，期間至 2024-07-24）；為 2024 年案，非近12個月新案，現況未查證","source":"BFA Law／Frank R. Cruz 律所新聞稿（搜尋摘要）","url":"https://www.businesswire.com/news/home/20240924702002/en/F-CLASS-ACTION-NOTICE-The-Law-Offices-of-Frank-R.-Cruz-Files-Securities-Fraud-Lawsuit-Against-Ford-Motor-Company","excerpt":null,"as_of":"2024-09-24","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"NHTSA 2024-11 對 Ford 課 1.65 億美元民事罰款（後視鏡頭召回延遲），同意令為期三年起、季度會議與獨立第三方監督，仍在監督期內；2026-08 Ford 聘 NHTSA 資深官員任首席汽車安全官。搜尋未見 2026 新罰款","source":"NHTSA 新聞稿 Ford consent order 165 million civil penalty（搜尋摘要）／Ford Authority 2026-08","url":"https://www.nhtsa.gov/press-releases/ford-consent-order-165-million-civil-penalty","excerpt":null,"as_of":"2024-11-14","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"F","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":2.36,"operating_margin_pct":-3.82,"fcf_margin_pct":2.75,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.F","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"GM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":7.04,"operating_margin_pct":2.32,"fcf_margin_pct":-0.19,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GM","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"STLA","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":7.83,"operating_margin_pct":0.91,"fcf_margin_pct":-7.18,"rd_intensity_pct":2.53},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STLA","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"TM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":16.76,"operating_margin_pct":7.05,"fcf_margin_pct":-2.35,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TM","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"F"},"financial_history":{"ticker":"F","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":158057000000.0,"revenue_yoy_pct":null,"gross_margin_pct":10.86,"operating_margin_pct":3.97,"net_income":-1981000000.0,"diluted_eps":-0.49,"free_cash_flow":-13000000.0,"fcf_margin_pct":-0.01,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":176191000000.0,"revenue_yoy_pct":11.47,"gross_margin_pct":9.17,"operating_margin_pct":3.1,"net_income":4347000000.0,"diluted_eps":1.08,"free_cash_flow":6682000000.0,"fcf_margin_pct":3.79,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":184992000000.0,"revenue_yoy_pct":5.0,"gross_margin_pct":8.38,"operating_margin_pct":2.82,"net_income":5879000000.0,"diluted_eps":1.46,"free_cash_flow":6739000000.0,"fcf_margin_pct":3.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":187267000000.0,"revenue_yoy_pct":1.23,"gross_margin_pct":0.9,"operating_margin_pct":-4.9,"net_income":-8182000000.0,"diluted_eps":-2.06,"free_cash_flow":12467000000.0,"fcf_margin_pct":6.66,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/F/F_Q3_2026_Earnings_Call_20261028.md）

# Q3 2026 Earnings Call
**Ford Motor Company** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Good day, everyone. My name is Ronnie, and I will be your conference operator today. At this time, I would like to welcome you to the Ford Motor Company Third Quarter 2026 Earnings Conference Call. [Operator Instructions] At this time, I would like to turn the call over to Maria Ricciardone, Chief Investor Relations Officer.

**Maria Ricciardone** (Executives):
Thank you, Ronnie, and welcome to Ford Motor Company's Third Quarter 2026 Earnings Call. I'm Maria Ricciardone, Ford Chief Investor Relations Officer. With me today are Jim Farley, President and CEO; and Sherry House, CFO. Joining us for Q&A are Andrew Frick, President of Ford Blue and Model e; Alicia Boler Davis, President of Ford Pro; Kumar Galhotra, Chief Operating Officer; Cathy O'Callaghan, CEO of Ford Credit; and Dave Carroll, President of Ford Energy. 
Jim will give a high-level overview of the business, and Sherry will provide added texture on the financials and guidance. We will be referencing non-GAAP measures today. These are reconciled to the most comparable U.S. GAAP measures in the appendix of our earnings deck. You can find the deck at shareholder.ford.com. 
Our discussion also includes forward-looking statements. Our actual results may differ. The most significant risk factors are included on Page 20 of our deck. Unless otherwise noted, all comparisons are year-over-year. Company EBIT, EPS and free cash flow are on an adjusted basis. Upcoming IR engagements include Sherry House at the Barclays Global Auto and Mobility Tech Conference in New York on November 18. Now I'll turn the call over to Jim.

**James Farley** (Executives):
Thanks, Maria. Ford delivered another strong quarter, thanks to our great products, our services and execution. I want to thank our employees and our dealers, all of our suppliers for this progress and for their commitment to Ford+. In the third quarter, as you know, we generated $2.7 billion in adjusted EBIT. We're raising our low end of our previous full year adjusted EBIT guidance and now expect to earn between $10.5 billion and $11 billion. 
Our strategy is clear. Number one, grow our auto business with a whole new generation of vehicles focused on North America, focused on transforming our EV business and global products with much less capital. Number two, aggressively expand our auto adjacencies: software, services and parts, while strengthening our financing capability. And third, diversifying with Ford Energy. The objective is a more profitable, capital efficient and resilient Ford, one that achieves 8% adjusted EBIT margins by 2029 and delivers sustained earnings, cash flow and returns to our shareholders over time. 
Let's start with our vehicles. In the third quarter, we continue to focus on a portfolio that leans into our strengths: trucks, vans and utilities. Our pickup lineup gives customers an unmatched breadth of choice between vehicles, prices, trims and powertrains. In Q3, F-Series captured the highest retail share among all full-size truck brands and is on pace for the 50th straight year as America's best-selling truck.
Maverick is America's best-selling hybrid pickup. Internationally, Ranger leads in many markets, including Australia and Europe. Early demand for the Ranger Super Duty is very strong, already #1 in heavy-duty medium-sized truck market in Australia in its first year, opening a very profitable opportunity for us. Transit continues to be the best-selling van in the U.S. Ford also leads in three-row SUVs in the U.S. with the Expedition and Explorer. 
We're also expanding access to customers through Ford Blue Oval Advantage, our certified preowned program, making Ford now the #1 certified preowned brand in the U.S. This program builds customer loyalty and positions Ford for our affordable new vehicles that will be coming in the next couple of years to our showrooms, and it really helps our resale values. In fact, we found that these used customers are 50% more likely than typical used car buyers to purchase a new Ford. 
The foundation of our sustained growth is world-class quality. Of course, topping the J.D. Power's 2026 IQS study and reduction we've seen in warranty coverages is encouraging to all of us. Excluding Novelis and tariffs, we reduced warranty and material costs by $1.5 billion in '25 and are on track to reduce another $1 billion this year. But we have much more to do, especially on long-term durability and the ownership experience. We are accelerating our industrial system, including very aggressive next-generation vehicle cost reduction targets. The goal is a world-class industrial system, one that makes cost competitiveness and quality repeatable. 
Our Super Duty launch in Oakville, Ontario is an important example of this discipline. The production ramp is already exceeding planned daily volume and jobs per hour rates. We reached OK-to-Buy last week and began shipping trucks to dealerships, and the quality we're seeing is fully competitive with our existing Super Duty plant, which is #1 in J.D. Power. The added capacity will give us flexibility for future plant changeovers and support profitable growth in retail, rental and upfitter channels.
We're bringing the same discipline to the next-generation F-150. Prototypes begin, builds are beginning in first quarter of '27, just a couple of months away. We have an incredible powertrain durability testing, which is now fivefold increase to meet our bulletproof powertrain target at Ford. We're doubling endurance and strength testing and increasing full vehicle test mileage by nearly 60% to almost 4 million miles. The F-150 will be the most extensively tested truck ever at Ford, and we will apply this exact same approach across our company.
Alongside strengthening our best franchises, we're opening new paths to grow at more affordable price points. Next year, we will be launching our affordable midsize pickup for international markets. We expect the base material cost for this truck to be 20% lower than today's Ranger. Just as Maverick has done in the U.S., this truck is designed to bring new customers into the Ford truck lineup internationally at a cost structure that allows us to compete, in this case, with the Chinese.
And in Louisville, we are preparing the launch of the Fathom, our first vehicle off the UEV platform. Rigorous testing and early supplier preparation are central to that effort. The launch remains on track for fourth quarter next year. Yesterday, I had the opportunity to drive our prototype. Wow, it completely blew me away. The 0 to 60, huge room inside, and the hands-free ADAS experience was like something I've never experienced. Fathom is really a breakthrough product. It's highly capable, innovative, affordable, and that EV product will be available to more Americans way ahead of our competition. This will require high-level execution by our team to deliver on time and at cost.
And the MSRP under $30,000 and the low cost of ownership is perfect for today's market. Fathom will offer something brand new for U.S. EV customers, an advanced zonal electrical architecture, Ford's first 48-volt low-voltage system, along with a sophisticated, advanced driver-assist capability, such as hands-free driving, an incredible rear-wheel drive performance feel and a lot of fun to drive. And bidirectional charging, so you can power your home with a Fathom when rates are high or during an outage, and there's so much more to this product that we're excited to share with you. 
Switching gears to our growing auto services business, software services, parts and financing. Now these auto adjacencies deepen our customers' relationship with us and create downstream value by enabling us to earn more over the life of each vehicle. Both software services and parts businesses achieved record revenue in the third quarter at highly accretive margins. 
An important linkage exists here between software and parts. Connected services help us anticipate maintenance over time, including a whole new software product called Prognostics at Ford, bringing customers to our remote service vans, almost 5,000 of them now, and our dealer network to keep their vehicles running 24/7. We found that when a retail customer combines a software subscription with regular service, the retention of the customer, especially for parts, is about 9 points higher. 
In parts specifically, we grew our U.S. wholesale business to third-party independent repair shops, and we've expanded a lot in Europe. A broader Motorcraft catalog also allows us to serve fleet customers of competitive brands and owners of much older Ford vehicles. And Ford Credit has had a great third quarter. Notably, together with Ford Pro, Credit launched Ford Pro Leasing in the third quarter. It's a big deal for Pro. Adding commercial leasing to our fleet management software and maintenance offerings will help us grow our Pro digital fleet management portfolio, which we will expect to be over 100,000 units by year-end. Many of those are non-Ford vehicles. 
Turning to Ford Energy. The investment thesis is very clear. Ford is going to solve a meaningful customer problem, build on Ford's advantage and offer a credible path to material earnings with attractive returns in the short term. Our starting point is U.S.-manufactured grid-scale battery storage for companies building America's new power infrastructure and data centers. These customers need a domestic partner with the manufacturing know-how and scale and staying power to support them throughout the product's life. We are progressing on 2 fronts: preparing our manufacturing capacity and securing customers. 
At our battery plant in Kentucky, we have met every single operating milestone so far. We have completed trial runs of electrode mixing, the first step in producing prismatic LFP battery cells, using the exact same process as our battery plant in Marshall, Michigan. We remain on track to bring 20 gigawatt hours of annual capacity online by the end of next year. Commercial progress is encouraging and demand remains very strong. Executed contracts and late-stage negotiations together already currently account for more than 80% of Ford Energy's 2028 capacity. 
We are building a diverse customer base across solar, grid support and data centers, and we expect our 2028 capacity to be fully committed by Q1 of next year. Pricing signals remain consistent with our investment assumptions. Negotiation for '29 and '30 capacity are already advancing, with customers engaged way ahead of our initial expectations. The DC Block gives us a practical starting point to build a broader capability. We expect attractive returns with short payback period, as I said. Sherry now is going to take you through our financial performance.

**Sherry House** (Executives):
Thank you, Jim, and hello, everyone. Our third quarter results reflect the deliberate actions we're taking to improve profitability and deliver consistent financial returns. Our increasingly fit industrial system, coupled with strong vehicle sales and auto adjacency performance, enabled adjusted EBIT growth of 3%, despite 2% lower revenue as we sunset products like Escape and Corsair to transition the Louisville Assembly Plant for the all-new Fathom.
Sequentially, revenue at $49.5 billion and adjusted EBIT at $2.7 billion were both higher, despite being impacted by a short-term supplier disruption late in the quarter. We also generated $4.7 billion in company-adjusted free cash flow in Q3 and ended the quarter with $25.3 billion in cash and $46.4 billion in total liquidity, maintaining our commitment to a strong investment-grade rating and to returning capital to shareholders. 
Today, we announced a fourth quarter regular dividend of $0.15 per share. This strong performance reflects the underlying quality of the sales accomplishments Jim mentioned as well as our progress toward a leaner, more-fit industrial system. We continue to see mix strength in trucks and three-row SUVs. Our higher-margin off-road passion products accounted for about 1/4 of our U.S. sales in Q3, up almost 4 points from a year ago, and our customers have been resilient amid higher fuel prices, interest rates and inflation. 
We also continue to deliver efficiencies across the business, including the use of AI in our business segments and throughout our operations. These actions, together with our industrial improvements, have helped us absorb the vast majority of headwinds from the Middle East conflict and rising commodity costs. It is this discipline and operational rigor that is taking root across Ford. In fact, it is directly benefiting our next-generation product pipeline, where we're making real progress in improving the cost base across our products.
In addition, the traction in warranty and material cost improvement is strong again this year. Both were lower in the quarter and year-to-date, keeping us firmly on plan towards reducing these costs by $1 billion this year, excluding Novelis and tariffs. And we are leveraging these reductions to fund our investments in the Universal EV platform and Ford Energy. At Novelis, operationally, the recovery is largely behind us. Financially, we have incurred about $1 billion in Novelis-related temporary costs year-to-date, with some more to go in Q4, and we are still tracking to a net tailwind of about $1 billion in 2026.
Now let's turn to our segment results. In Ford Blue, we delivered $27.1 billion of revenue and $1.4 billion in EBIT, down 3% and 10%, respectively. Our performance primarily reflects lower volume driven by product discontinuations and the impact of the Middle East conflict within the region and higher commodity costs. Our underlying business continues to benefit from favorable mix. We saw significant year-to-date demand in the U.S. for Explorer, with the higher-margin Tremor and Platinum series increasing sales by nearly 60%. F-Series performed well as we executed a disciplined go-to-market approach that yielded the highest share of revenue and lowest incentive spend in the third quarter. Lincoln also had an impressive quarter, with both Nautilus and Aviator experiencing double-digit sales growth in the U.S.
Our stock levels are healthy. We ended the quarter slightly below our target range of 55 to 65 retail days' supply, and we increased gross stocks by about 6% versus Q2 2026. Our F-150 inventory improved quarter-over-quarter to 49 retail days' supply, though is still below our ideal range, which provides us with upside as we work to restock to target levels. Overall, we expect stocks to return within our targeted levels by year-end. 
For Model e, we improved EBIT by 25% year-over-year in the quarter. We reported an EBIT loss of $1.1 billion on revenue of $1.2 billion. These results reflect our focus on capital efficiency and structural cost reductions as we realize the benefits from rightsizing our Gen 1 volumes while we continue to invest in our UEV platform and Ford Energy. We are on track to improve Gen 1 EBIT by approximately 40% year-over-year in 2026 as we balance production and pricing with natural demand. In fact, in Q3, Mustang Mach-E had the lowest incentive spend since 2023. Importantly, we are still targeting breakeven by 2029.
Ford Pro delivered another solid quarter with $17.8 billion of revenue, up 2%, despite wholesale volumes being down 4%. Pro EBIT was $1.7 billion, down 16%, primarily due to higher commodities and temporary costs associated with the Oakville launch. Lower tariffs and favorable product mix, driven by higher truck production as we recover from Novelis, partially offset these headwinds. 2027 model year signals are favorable, as most commercial agreements are complete, with both fleet demand and pricing in line with our expectations.
Ford Credit delivered a great quarter with EBT of $803 million, up $172 million. These results reflect favorable performance on our derivatives, healthy financing margins and a supportive used vehicle pricing environment. Our high-quality portfolio of offerings across Ford Credit remains resilient, and we maintain a consistent, disciplined approach to risk management.
Jim talked earlier about the record quarter for software services and parts. I'd like to double-click on that. These auto-adjacent businesses were significant drivers of the quarter's strong performance, contributing approximately 10% of the quarter's revenue at strong margins. The largest contributors to software services revenue growth in the quarter and year-to-date were BlueCruise and Connectivity, and we continue to see momentum in Ford Pro Intelligence. 
Parts revenue growth this year has been driven by double-digit growth in our U.S. wholesale channel and the expansion of our retail and wholesale businesses in Europe. We are also increasing dealer service retention with digital and uptime tools to drive organic parts growth. We are excited about the prospects these auto adjacencies offer for continued accretive growth.
Now looking ahead to our full year 2026 outlook. We are confident in our full year trajectory and our planned investment cadence, and now expect full year adjusted EBIT between $10.5 billion to $11 billion. Adjusted free cash flow and capital expenditures are unchanged at $6 billion to $7 billion and $9.5 billion to $10.5 billion, respectively. Our guidance does not include potential impacts of a significant escalation in the Middle East or a material downturn in the U.S. economy, which, if either or both occurred, could have a substantial impact on industry demand. 
For our full year segment outlook, we expect Ford Blue EBIT of about $5.5 billion, Ford Pro EBIT of about $7 billion, Model e losses remain unchanged at about $4 billion and Ford Credit EBT updated to about $2.8 billion. Our guidance now assumes a U.S. SAAR of 16.5 million units, commodity headwinds approaching $2.5 billion year-over-year, an increase of about $500 million as we continue to see increasing pressure from input costs. 
In addition, higher fuel prices are impacting our freight and energy costs, but notably, we are not seeing it impact customer demand for trucks and fleet vehicles at this point. We now expect full year U.S. industry pricing to be about 100 basis points higher year-over-year, which is 0.5 point higher than our previous assumption. And lastly, we continue to target $1 billion in material and warranty cost reductions, excluding Novelis and tariffs.
In summary, our ability to increase profits in Q3 reflects the actions we have taken to optimize our product portfolio and create a business that is more efficient and agile in the face of increasing cost pressures, intensified global competition and an uncertain macroeconomic environment. I'll now turn it back over to Jim to provide some commentary on 2027.

**James Farley** (Executives):
Thank you, Sherry. At this point, we're targeting profitability next year to be roughly in line with this year, with an even stronger automotive business that enables us to invest in our future. Our outlook reflects 3 things: investing in future growth, substantial external cost pressures and continued operating improvements. Next year will be a foundational year on our journey to 8%, when we will have refreshed 70% of our global portfolio of vehicles by volume. We are allocating majority of that investment to North America, where we will be expanding our truck and utility lineup. 
Additionally, Ford Pro will be expanding their global lineup for Transit and Ranger with all-new price points. Additionally, we are investing in our plants for our new F-150, which will require planned production downtime next year. We expect the added Super Duty capacity at Oakville to largely offset the impact of that downtime. We will also continue to grow our investments in the Universal Electric Vehicle platform ahead of Fathom's launch and bring Ford Energy's 20 gigawatt hours of capacity online, both of which are key to the Model e turnaround by 2029. 
In auto adjacencies, we expect continued growth in software services and parts to increase the contribution from reoccurring and countercyclical revenues. This accretive growth should help offset certain macro headwinds we expect at Ford Credit. We currently expect commodities, memory and logistics costs to represent a year-over-year headwind of about $2 billion at Ford. Our current plan is that the improved reliability and capability of our industrial system, together with revenue optimization and a company-wide efficiency on cost, will allow us to offset the expected headwinds that I just walked through. We intend to finish this year strong, execute in '27, with great profitability investments and with discipline to build towards that target of 8% adjusted EBIT by '29. We'd like to take your questions now.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Rajat Gupta with JPMorgan.

**Rajat Gupta** (Analysts):
Great. And appreciate all the color on 2027. Assuming the commodities, logistics, the memory headwinds stay where they are right now at the $2 billion guide, just curious, how much of the 2027 offset stack that you've pointed to is within your control today? How much is -- how much of that do you still need to work on just because a lot of the inflation has happened in the last 3, 4 months. Just curious to get your thoughts on that, on like how comfortable you are with that '27 guide and what more needs to be done to get there. And I have a quick follow-up.

**Sherry House** (Executives):
Yes, sure. Thank you so much for your question. I would say that the areas that we see more in our control would be the areas of revenue optimization, continued software and parts growth and also continued savings as well. And I can give you a little bit more color on that, too, if that would be helpful. 
I mean on the market equation side, as you know, mix optimization is something where we have made huge progress this year, and we expect that progress to continue into next year. We have transformed our sales and operating plan and are now leveraging AI tools that are enabling us to match demand sensing to capacity planning, and that's leading to more production stability, which leads to real savings.
We also have better inventory and pricing models for both vehicles and parts, and that's leading to faster turn rates and leaner stocks and just an overall disciplined approach and management of our market equation. So that is going to be an area that's in our control. We're continuing to get better through tech modernization.
On the structural cost side, we're already working plans. We've been at this for 6 months already going into 2027, and in fact, we're already looking ahead and populating profit improvement actions for both '28 and '29 as well. And then as I said, we're going to continue to see, we believe, increased revenues in both the software and the parts growth area. And as I just mentioned in my comments here a moment ago, we've now seen those combined, representing 10% of our revenues at accretive gross margins. So this is an area that is in our control, areas that we're focused on, and we're seeing the benefits of that to stabilize our returns in the face of things like commodities in an uncertain macro environment.

**James Farley** (Executives):
I would only add that our days' supply on F-150 and Super Duty is a major accomplishment compared to our competitors. It's real -- we're going into '27, as Sherry said in her speech, in a really good situation in our truck business.

**Rajat Gupta** (Analysts):
Understood. That's very helpful color. And then just on UEV, with the deliveries expected next year, just curious what remains to be derisked between now and launch, when it comes to supplier readiness, software validation, just battery cost. How much of the path to the Model e breakeven depends on UEV hitting its volume and cost targets on schedule?

**A. Kumar Galhotra** (Executives):
This is Kumar. Let me give you some color on the status of the launch. It's progressing very well. 90% of the validation testing has been completed. We've built our first production line vehicles on -- at Louisville Assembly Plant. So we're starting to prove out our production processes. One of the key new technologies for Fathom is unicastings. We've already produced 5,000 of them, so we're proving out our capability to run at rate, and that's gone really well. 
And to be specific about your question on what risk remains to be mitigated, it's primarily in the supply base. We need to make sure that the supply base can run at rate with high-quality parts. And that's very normal at this stage of the launch, and that's what we're going to be working on for the next few months.

**James Farley** (Executives):
The other element of the Fathom launch that's critical is the revenue picture, which actually seems to be strengthening. Andrew, do you want to highlight the change in the U.S. EV market and how that relates to the profitability of Model e?

**Andrew Frick** (Executives):
Yes. I mean, the market, as we've learned over the last couple years, is definitely, in the U.S. specifically, is not acting as a monolith, especially when it comes to the affordable EVs. We've actually seen EV prices go up about 10%, which has priced a lot of new vehicles out of the affordable market. So the customer is very limited with their new vehicle options. In fact, a lot of them are looking to the used market. 
So we're now looking at the EV market as new and used, where about -- over half now of the vehicles sold under $40,000 are used vehicles. That's really important because, as you said, Jim, the Fathom starting MSRP is at $28,350. That's going to be right in the heart of the market. And it's not just the EV market. It's actually opening us up to a massive total addressable market. 
If you know that nearly 50% of the U.S. new vehicle industry transacts under $40,000. So not only do we expect Fathom, for the reasons you mentioned earlier, to attract new and used EV buyers, but also ICE hybrid customers, especially because we're going to have much lower operating costs than even a mainstream hybrid vehicle. So the customer response on what we've shared so far has been really strong. We're preparing for the launch, and we'll be launching our preorder program in the first quarter, and we'll have more to share with everyone at that time as we get closer.

**James Farley** (Executives):
We're feeling pretty good about the industrial preparation and the revenue picture. It's impressive to me to see that the used -- the EV market is above 8% of the U.S. industry now. And that's including all the issues that Andrew just highlighted and the lack of affordability options. So I think we're -- it's a lot of work to still be done. We have a year to go, but I think we're positioned really well, which will be one of the 2 big drivers turning around Model e -- the vehicle side of Model e.

**Operator** (Operator):
[Operator Instructions] Your next question will come from Emmanuel Rosner with Wolfe Research.

**Emmanuel Rosner** (Analysts):
Great. Maybe just following up here on Model e. So I know for 2027 overall for the company's stable results versus 2026, are you still looking to improve Model e within that EBIT? And maybe what are the moving pieces within that? Are you planning similar or higher investments into this UEV and BESS? And then what are the drivers of improvement on the car side of the business?

**Sherry House** (Executives):
Great. Emmanuel, thank you so much for your question. So you just heard about the Model e operational steps that we're taking and the milestones there. From a financial perspective, as I said in my comments, we're working towards our target for Model e to reach breakeven by 2029. The progress isn't going to be linear, and we're now expecting higher expenses in 2027 as the plan's coming into focus. So let me give you a little bit of what we're seeing. We think that the next step function change in profitability is going to happen in the first half of 2028 as UEV and Ford Energy both ramp with revenue on both. 
So if you break that down a bit, you're going to see Fathom launching towards the end of the year with the first derivative off the platform. Then you're going to have that full year of production in 2028. Then we're going to be escalating the Ford Energy business with investment, full year production also by 2028. And then new is the launch of the European partnership products by 2028. So there will be investment in that in 2027, and the full year of production on those will be by 2029. So you're going to have those investments that are happening through '27 with the unlock really starting to unleash as you get into 2028 and '29.

**Operator** (Operator):
Your next question comes from Tom Narayan with RBC.

**Gautam Narayan** (Analysts):
My question has to do with Ford Blue in Europe. China has about 60 million vehicles of auto production capacity. It's consuming about 20 million a year and exporting 10 million, a decent portion going to Europe, and then this has been worsened by weakening domestic sales in China. I know you have a JV with Geely in Valencia, the partnerships with Renault and VW. Are these enough to rightsize your capacity in Europe? Or do you need further actions from the EU to halt Chinese exports?

**James Farley** (Executives):
Thanks for your question. Europe is quite different than what's happening in Southeast Asia and LATAM for the China competition. So I appreciate your question specific to Europe. And the situation in Europe is very different because the EU has such a strong EV mandate, and as you said, there's a lot of overcapacity in Europe, not just to export it from China. We do feel like we know we have the right plan to right the ship in terms of our passenger car profitability, with Renault and Geely, as you mentioned. Those are very low capital investments with really great cost levels, especially for the EV portion of our lineup, that will allow us to replace unprofitable EVs with very -- with much better profit outlooks on EV. 
The commercial side is also under pressure in Europe, and we have a pretty exciting lineup, especially around the EV requirements for the commercial business, the Pro business. There's a lot of negative profit pressure, but we have a really good solution coming next year that we're really excited about. I think the combination of both will make sense. 
As far as the capacity utilization that you mentioned, your specific question at this point, I don't want to get into the details other than working through the opportunity in Valencia and Romania and Turkey. So thank you. We are completely committed to building a profitable European business with these actions. We've been on it for several years, and we have a really aggressive plan.

**Operator** (Operator):
Your next question comes from the line of Joseph Spak with UBS.

**Joseph Spak** (Analysts):
I guess I just want to start with some of your comments around the F-150 and not to sort of get -- just sort of really buckle down on this. I think you mentioned that F-150 stock, you expect to recover to target levels by the end of the year. And I want to be clear on this because you've talked about stock in terms of days historically, and I think even in your prepared remarks, but seasonally, we always see end of year, December is much lower than September. So when you say recover to correct levels, are you talking back to that days level? Because that would mean a pretty significant increase in absolute inventory.

**Andrew Frick** (Executives):
Thanks, Joe. It's Andrew. No, I think when we talk specifically to our F-150 stock, we're running at 49 days coming out of September. That is below our range. As we look at towards the year-end, we will be running probably on the low end of that. We'll continue to run on the low end of that, and as Jim mentioned, below our competitive set. 
We've seen really high days to turn on our units that we have in stock. In fact, we just came out of the third quarter where we had the fastest turn rates of the year, and they were faster than any of our competitors in the segment. And that's really helping us manage our overall market equation, as we mentioned, but we do not expect to see our stocks building to a much higher level at the end of this year.

**James Farley** (Executives):
Just want to reinforce and be specific to your question. You said dig in. I think that's great. For me, over the last many years, a normal stocking level for F-150 could have been 80 to 100 day supply in the past. I just want to reinforce what Sherry said. Our target is that 50, low 60-day supply. And I think by the end of this year, we're going to be in that range. That is substantially lower than Ford's operated, and it's really allowed us to build that disciplined full-size truck business, while we watch our competitors play a very different game. 
And our dealers are very anxious for more stock. Our mix is good, and our turn rates is really what we're focused on now, as Andrew said. So I would say, to answer your question simply, that 55- to 60-day range that Sherry talked about is historically much lower than we normally run our truck business.

**Operator** (Operator):
Your next question comes from the line of James Picariello with BNP Paribas.

**James Picariello** (Analysts):
Just to follow on Joe's question on the F-Series recovery and inventory, is the 150,000 units recovery target still cleanly intact? Or is that number lower and there's something else to favorably offset and keep that net $1 billion in the guide intact? Is it better price mix? Or is that volume target still the guide?

**Sherry House** (Executives):
So here's how I answer that. On the Novelis recovery, it has been going as planned operationally. And we're now running at rate and most -- the vast majority of the materials have been validated, and we're going to continue to run at rate in Q4 as our plan. When you get to the financial side of it, we have seen costs coming in a little bit lower and the volumes have been proportionally a little bit lower, too. And so that's going to enable us to continue to keep with the guide that we said at the outset of the year, which is $1 billion of a net tailwind by the end of 2026 as it relates to this set of products.

**Operator** (Operator):
Your next question comes from Andrew Percoco with Morgan Stanley.

**Andrew Percoco** (Analysts):
So I guess to start out, a 2-part question here. First, I want to ask a follow-up on energy storage. I think you guys provided a great update in your prepared remarks. It sounds like you're 80% contracted for 2028. So I guess that would imply about 16 gigawatt hours kind of in the backlog. But I think you also said that, that included contracted backlog as well as late-stage negotiations. So I guess, did I get that right? And is there any other information or color you can kind of provide in terms of what needs to happen to maybe get that full 16 gigawatt hours fully contracted versus late stage? Just kind of curious what the final steps are there. 
And then my second question, coming back to what Tom asked about in terms of China. Obviously, exports are continuing to increase pretty substantially out of the region. The domestic market feels fairly saturated. Can you just talk to how you expect that to impact your business at a higher level, not just in Europe, but just globally and what you think needs to be done to make sure that that's not going to create a bigger disruption for you guys going forward?

**James Farley** (Executives):
Dave, why don't you handle Ford Energy?

**David Carroll** (Executives):
Yes. So Andrew, this is Dave Carroll. First, just to cover your first question, we're actually not talking about backlog today. We were going to start disclosing that next year. And what we -- what Jim had indicated in his remarks is that we are actually ahead of expectations where we are with our customers. And we see that primarily Ford Energy is very excited about the quality of the product that we have on the market. We believe it's one of the highest quality products out there on the market that you can buy, and we're seeing that from our customers. 
And we believe that's what's bringing the customers to us as we're moving forward. In fact, last week, we had one of our customers out at our Marshall manufacturing facility, where they toured where we're producing LFP prismatic cells right now, and they toured that factory and came out saying it's top tier of all the factories they've seen globally. So we're very excited that we have the highest quality product on the market, and we believe that's what's driving the customers to us.

**James Farley** (Executives):
Yes. And I think for backlog, that'd be something we'll probably give more transparency on next year, right?

**David Carroll** (Executives):
Yes, that's correct.

**James Farley** (Executives):
Okay. So thanks for your question. And we have a lot to do with Ford Energy, but really promising start, and we're going to open the aperture for all the investors more and more as time goes on. As far as China's concerned, thank you for your question. Frankly, we've held up really well internationally as the Chinese gain more and more share in open and closed markets. Where we see the competition the most intense is LATAM and Southeast Asia, where we have a large Ranger business. And in both cases, Ranger is still doing very well because it competes at a much higher price point. And as I said, we're going to be going into their price point next year with this new affordable truck. So we'll see how that plays out, but we're confident. 
In addition, I think Ford is the #1 traditional OEM exporting from China. It's been our strategy for several years now. The Territory is our second-most profitable vehicle globally, and it is really successful for us. And I think the exports are up, I don't know, like 60%. It's a really big improvement. And we expect to continue to take advantage of that for the open markets especially. 
I kind of try to give a view on Europe, so I won't be repetitive, but that's where we -- for Ford, that's where we see the real pressure on our business with the Chinese. It's really in Europe. It's not just the Chinese. It's the EV mandates by the EU, which we expect them to address over time as well as the U.K., and all the overcapacity in Europe that's been there for many, many years. 
As far as the rest of the world, I think we're well positioned, not only now, but with our new lineup. And our global partnerships will give us a lot of opportunity. We have learned so much exporting from China. It's been really a very successful exercise for Ford with very low capital, and we've learned a lot about China cost as well as China cost in places where it needs to be localized, like Thailand, in Europe over time. So I think we're well positioned. The issue for us in the short term is really Europe.

**Operator** (Operator):
Your next question will come from Jairam Nathan with Daiwa.

**Jairam Nathan** (Analysts):
So I just wanted to understand the ability to upsell on the Fathom. The starting point of below $30,000 is pretty good, but I just wanted to understand how would you -- what ways you can upsell that.

**James Farley** (Executives):
Do you mean -- just so we understand the question, you mean how do we get to a point where it's profitable at that price point? Is that what you mean by the offset?

**Jairam Nathan** (Analysts):
No, no, not offset. Upsell the vehicle, kind of, by offering, like, getting a better mix on the vehicle beyond that $30,000 -- under $30,000.

**James Farley** (Executives):
I see. I see what you mean. Okay. Thank you. Yes. Great question. I think we're already pretty deep in a lot of intelligence. A lot of customers have shown interest in the vehicle, so we're learning a lot. There's a lot to that strategy at Ford to offer customers a lot of options beyond the $28,000. Andrew, I'll let you highlight the 3 or 4 key points.

**Andrew Frick** (Executives):
Yes. I think what, one, and we'll get more into this when we do a full reveal of the product. You'll learn a lot more about our positioning strategy. But the starting price of the $28,350 is just that. We'll have a range that goes to the high $30,000 range. And we'll have a couple different offerings within that. So I would say we will give you a lot more detail around this, the offerings themselves, as we get closer. It's probably too soon to share more at this point.

**James Farley** (Executives):
The big breakthrough conceptually for us about customers buying nicer Fathoms are really on the digital side. We put in an advanced electrical architecture, a 48-volt system, so we can offer at an incredibly low cost, very advanced ADAS, as well as digital camera dashboard. I won't go into all the details Andrew said, but the digital suite, including the embedded Apple Maps, is really a game changer for any EV, let alone at this price. I think for me personally, that is going to be the most exciting upsell opportunity, is really the long-term subscription and digital experience for the customer.

**Operator** (Operator):
Our next question will come from Mark Delaney with Goldman Sachs.

**Mark Delaney** (Analysts):
I was hoping you could give a bit more color on what Ford is seeing for pricing. The company took up its view of U.S. industry pricing by a little bit for 2026. Maybe you can share a bit more on what's driving that? And then also on this topic more broadly, any early views on pricing for 2027, including what you're seeing in Pro with the annual negotiations, which I think are now well underway.

**James Farley** (Executives):
That's a big question. Thank you for asking. So Andrew and Alicia, I think you should bring that to light.

**Andrew Frick** (Executives):
Yes, maybe I'll start with the retail side. Thanks, Mark. Yes, we're seeing a very strong pricing environment right now. We expect pricing to be up about 1 percentage point this year. And as we looked into next year, we think there's a lot of different levers that we'll be able to work with our product mix and net pricing, both the top line, but also our variable marketing as well, just very similar to how we approached this year. 
The industry remains really strong. We're seeing the segmentation remain strong. Very really big resilience with customer base, especially in trucks and utilities, which is really playing to our advantage, and we expect that to continue into next year. And Alicia, do you want to comment on what you're seeing in the early part of the commercial side?

**Alicia S. Davis** (Executives):
Yes. I can just also on pricing for fleet, we're also seeing strong pricing year-over-year over 1%. But as Sherry mentioned, our fleet demand orders for '27 model year are on target. We're excited about Oakville and that capacity because that's going to allow us to really grow our truck rental sales. We can return to our pre-pandemic levels where the economics are really favorable for us. We are also able to take a larger share of wallet for our large commercial customers.
And then we're able to supply more chassis cab units to the body modifiers, and we are very competitive in that space, and we had been constrained. And so we're excited about the ability to really meet this unmet demand, and the strong order take that we're seeing so far gives us confidence that we'll continue to grow there.

**James Farley** (Executives):
The upside for next year for Pro is pretty meaningful between Oakville and getting past Novelis. It's really a great opportunity for us at Ford.

**Operator** (Operator):
Your next question comes from the line of John Saager with Evercore ISI.

**John Saager** (Analysts):
Yes. I just wanted to take one more shot at BESS. You had mentioned the discussions for '29 and '30 advancing kind of ahead of your prior expectations. What do you need to see, in terms of commitment capacity to start to think about expanding beyond that first 20 gigawatt hours? And then what does incremental CapEx look like for that? And then maybe if I could ask a follow-up on just the impact to earnings as we go through the course of the year, as you go through the ramp to get towards the fourth quarter of 20 gigawatt hours of capacity. Could you just -- maybe give us some puts and takes there?

**David Carroll** (Executives):
Yes. So John, so obviously, the team is really -- this is Dave. The team's really focused on launching the initial 20 gigawatt hours that we have to bring online and ramp up in 2028. That being said, we are already evaluating scenarios, how we could best expand capacity, expand our offerings to our customers because we do see the real demand out there. But when we're doing so, we do consider the returns on our investment. We consider the customer demand, the tax treatment and other strategic uses of capital. So we do see upside at our Kentucky One facility. We're excited for the potential growth, but we don't have anything to announce today in that regard.

**James Farley** (Executives):
Sherry, any tips you want to give on the spending for Ford Energy next year?

**Sherry House** (Executives):
The only thing I would give is that we had talked about around $2 billion of investment, and we're going to spend about 1/3 of that this year and about 2/3 next year. So that gives you a little bit more understanding.

**Operator** (Operator):
Your next question comes from the line of Dan Levy with Barclays.

**Dan Levy** (Analysts):
Wanted to ask about the partnership with Geely. I believe part of the partnership is to establish learnings from them. So maybe you could just be a bit more concrete, what you hope to learn within supply base and designing the vehicle? And then I'll just extend that question to how you plan to achieve profitability on Fathom, which I think you've talked about sort of indexing or benchmarking against the Chinese, some of the supply chain opportunities there. So maybe you can talk about what you're doing with Geely? And maybe how some of that potentially extends to how you're going to achieve the right cost that you need on Fathom?

**A. Kumar Galhotra** (Executives):
So let me break it down into 2 pieces. It's cost and it's quality. We are already learning that they can offer a certain percentage lower cost landed in Europe for us. So we're going through part by part, understanding each system. On speed, we're learning they're a few months faster than us, and we're going through each part of the product development system to understand how they are faster than us. And a combination of both of those items is being institutionalized into our own global product development system.

**James Farley** (Executives):
On the UEV, we always set our target even 4 years ago, with imagining what a BYD could do in Mexico. Not because we knew -- not because we counted on that happening, but because we knew that ultimately that platform is going to be competitive. We had to make sure even in the U.S. would be fully competitive. So that's why we took such a big swing at the innovation because we had to. The big breakthroughs, in general, on the cost for that product is really a couple of things in general. The first is, the E-box and the whole electronics and electrical architecture and ADAS is much, much lower cost than supply chain. We did that all in-house, and the big benefit would be the cost and the design cost of that. 
Number two is we radically simplified the parts. So the 2 large unicastings that Kumar talked about derisking, the 5,000 we've already built, that is a radical enabler for much lower part count in the vehicle. And then obviously the labor content is much lower in the vehicle by intention. But there's another area that we really found to be quite advantaged relative to a BYD. And that is the efficiency of our motors, gearbox and inverters, which are about 30% more efficient than theirs and allows us to design a battery that's much less. And so that -- I think that's really critical. 
The LFP cell in Marshall is another big enabler, and I think you get the point, which is like every part of this project had to be world-class Chinese cost efficiency in order to convince ourselves we would be fully competitive. But it also introduced a lot of new technology and frankly, a lot of new suppliers. And so what we learned from UEV and what we're learning from Geely and what we want to keep strategically in the company are all getting captured at the same moment for Kumar, and his team is now curating how that all is going to work along with our AI tools that Sherry mentioned. And that's why we mentioned the heart and soul of our company is going to be this new industrial system enabled by all that benchmarking, including suppliers, manufacturing efficiency, all the way to how fast we create the vehicle. That's exciting for us because it's quite a big change for Ford.

**A. Kumar Galhotra** (Executives):
A real concrete example is the motors and efficiencies that you mentioned, Jim, are being -- now being transported into our hybrid systems for the rest of our portfolio.

**James Farley** (Executives):
And we're putting a lot of pressure on ourselves to make sure that whether it's UEV or Geely or JMC, we -- or AI tools, we are going to move that into the core part of the company as fast as we can.

**Operator** (Operator):
This concludes the Ford Motor Company Third Quarter 2026 Earnings Conference Call. Thank you for your participation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### F_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CFO｜guidance：CFO 稱全年調整後 EBIT 指引收窄至 100–110 億美元，中點上調 10 億美元，原因為定價與組合（原話："increasing the midpoint by $1 billion, driven by strong"）
- 2026-07-28｜CFO｜guidance：全年調整後自由現金流指引上調至 60–70 億美元（原話："adjusted free cash flow to $6 billion to $7 billion"）
- 2026-07-28｜CFO｜guidance：資本支出指引不變，為 95–105 億美元（原話："capital expenditures remain unchanged at $9.5"）
- 2026-07-28｜CFO｜risk：CFO 說明指引未納入的情境：中東重大升級與美國經濟顯著下滑（原話："a significant escalation in the Middle East"）
- 2026-07-28｜CFO｜guidance：Ford Blue 全年 EBIT 指引上調為 50–55 億美元（原話："Ford Blue's EBIT range to $5 billion to"）
- 2026-07-28｜CFO｜guidance：Ford Pro 全年 EBIT 指引收窄為 70–75 億美元（原話："Ford Pro's EBIT range to $7 billion to $7.5 billion"）
- 2026-07-28｜CFO｜guidance：Model e 全年虧損預期改善至約 40 億美元，含約 10 億美元 UEV 與 Ford Energy 增量投資（原話："Model e losses to about $4 billion."）
- 2026-07-28｜CFO｜guidance：Ford Credit 全年 EBT 預期高於 25 億美元（原話："expected to be above $2.5 billion."）
- 2026-07-28｜CFO｜guidance：指引假設的美國 SAAR 區間為 1,600–1,650 萬輛（原話："a U.S. SAAR of 16 million to 16.5 million units"）
- 2026-07-28｜CFO｜guidance：美國產業定價全年預期上調約 0.5 個百分點至 +50bp（原話："about 0.5 point higher at plus 50 basis points"）
- 2026-07-28｜CFO｜guidance：Novelis 鋁供應中斷全年成本影響更新為約 15 億美元（原話："expect a full year cost impact of about $1.5 billion."）
- 2026-07-28｜CFO｜commitment：CFO 重申對 Novelis 復原計畫下全年淨 10 億美元 EBIT 改善有信心（原話："confident in our net $1 billion EBIT improvement"）
- 2026-07-28｜Ford Pro 總裁｜guidance：Ford Pro 下半年 EBIT 指引區間，對照上半年 34 億美元（原話："it's $3.6 billion to $4.1 billion."）
- 2026-07-28｜Ford Pro 總裁｜guidance：Ford Pro 預期年底恢復至 2025 年營收水準（原話："full recovery to Ford Pro's 2025 revenue run rate"）
- 2026-07-28｜CFO｜margin：CFO 拆解大宗商品逆風：全年略高於 20 億美元，下半年占約 15 億美元（原話："about $1.5 billion of that to be in the second half"）
- 2026-07-28｜CFO｜margin：CFO 說明下半年大宗商品額外衝擊約 9 億美元（原話："about $900 million additional to what we've already had"）
- 2026-07-28｜CFO｜margin：管理層稱第二季 EBIT 增長主要來自組合與淨定價（原話："this quarter's EBIT strength was largely a result of strong"）
- 2026-07-28｜CFO｜margin：Ford Blue 營收與 EBIT 成長歸因於美國法規調整與較高淨定價（原話："enabled by U.S. regulatory changes and higher net pricing"）
- 2026-07-28｜CFO｜margin：CFO 稱全年有 10 億美元材料與保固成本降幅，用於再投資 UEV 與 Ford Energy（原話："on track to deliver $1 billion in material and"）
- 2026-07-28｜CEO｜margin：Farley 稱縮小成本差距是達成 8% 利潤率的重要路線（原話："is continuing to close the cost gap"）
- 2026-07-28｜CEO｜margin：Farley 稱整合服務有可能為公司貢獻 0.5 個百分點利潤率（原話："integrated services being 0.5 point of margin"）
- 2026-07-28｜CEO｜margin：Farley 說明 Ford 只強調付費訂閱，不同公司口徑不同（原話："we are focused on paid subscription."）
- 2026-07-28｜CFO｜margin：CFO 澄清 160 萬付費訂閱含零售與 Pro，其中 Pro Intelligence 為 90 萬（原話："that does include retail plus Pro."）
- 2026-07-28｜CFO｜commitment：CFO 結語重申 2029 年 8% EBIT 利潤率目標（原話："firmly on the path to our 8% EBIT margin target by 2029"）
- 2026-07-28｜CFO｜commitment：CFO 重申維持投資等級與股東回報（原話："to our investment-grade rating and returning capital"）
- 2026-07-28｜CFO｜capital_allocation：宣布第三季定期股息每股 0.15 美元（原話："a third quarter regular dividend of $0.15 per share."）
- 2026-07-28｜CFO｜capital_allocation：BlueOval SK 處分認列 36 億美元一次性特殊項目費用（原話："special item charge of $3.6 billion"）
- 2026-07-28｜CFO｜capital_allocation：12 月公告相關剩餘現金費用最多 20 億美元，預計年底前完成大部分（原話："to be completed by the end of the year."）
- 2026-07-28｜CEO｜capital_allocation：Farley 表述資本紀律原則（原話："Every dollar must earn durable returns"）
- 2026-07-28｜CEO｜capital_allocation：Farley 稱國防業務須是強勁且資本回報良好的事業（原話："It has to be a strong business with really good returns"）
- 2026-07-28｜CEO｜product：Farley 稱 Ford Energy 預計 2027 年底前達年產能 20GWh（原話："By late next year, we expect to reach 20 gigawatt"）
- 2026-07-28｜CEO｜customer：Farley 自評 2028 年 20GWh 產能的銷售進度（原話："third inning of selling out the 2028 capacity"）
- 2026-07-28｜CEO｜capital_allocation：Farley 列出 Ford Energy 是否擴產的考量之一為稅務處理（原話："Obviously, the tax treatment is very"）
- 2026-07-28｜CEO｜product：Farley 描述 Ford Energy 回收期短（原話："but one with a very short payback."）
- 2026-07-28｜CEO｜customer：Farley 稱已與美國聯邦政府簽約生產 3 台基於 Super Duty 的軍用原型車（原話："with the U.S. federal government to produce 3 prototypes"）
- 2026-07-28｜CEO｜product：Oakville 擴產預計第四季啟動，新增最多 10 萬輛 Super Duty 產能（原話："on track to launch in the fourth quarter of this year"）
- 2026-07-28｜CEO｜product：UEV 平台首款車預計明年開始交車（原話："Customer deliveries will begin next year."）
- 2026-07-28｜CEO｜product：UEV 首款車起價約 3 萬美元（原話："It starts around $30,000."）
- 2026-07-28｜CEO｜product：Apple 將為每款 UEV 平台車提供內建地圖（原話："will be the embedded map provider for every UEV platform"）
- 2026-07-28｜CEO｜product：歐洲與 Geely 的協議，管理層稱可帶來速度與資本效率（原話："our agreement with Geely, which will bring speed and"）
- 2026-07-28｜CFO｜guidance：CFO 預期 2026 年 Gen 1 EBIT 較去年改善約 40%（原話："we expect to improve Gen 1 EBIT by approximately 40%"）
- 2026-07-28｜CFO｜product：總付費訂閱成長約 50%（原話："Total paid subscriptions grew about 50% to"）
- 2026-07-28｜CEO｜product：越野車款占美國第二季銷售 25%（原話："25% of our U.S. sales in the second quarter."）
- 2026-07-28｜Ford Blue 與 Model e 總裁｜guidance：Frick 稱預期目前的產品與系列組合水準將持續至年底（原話："that level of product mix and series mix to continue"）
- 2026-07-28｜CFO｜customer：2027 車型年北美客戶合約簽訂進度較去年提前（原話："contracting in North America is off to a fast start"）
- 2026-07-28｜Ford Blue 與 Model e 總裁｜competition：Frick 對比 F-Series 與競爭對手的租賃（rental）銷量（原話："we've had really low rental volume"）
- 2026-07-28｜CEO｜product：Farley 稱 F-Series 庫存約 45 天，對批發量有上行空間（原話："F-Series is around 45-day supply, which"）
- 2026-07-28｜CEO｜competition：Farley 表述 USMCA 立場：要讓美國車廠更易與日韓競爭（原話："to compete with Japan and South Korea"）
- 2026-07-28｜CEO｜commitment：Farley 稱支持修訂 USMCA 的條件（原話："prepared to support revising the USMCA so long as it"）
- 2026-07-28｜CEO｜risk：Farley 評價 Ford 對關稅的處理（原話："has done a good job with our exposure to tariffs"）
- 2026-07-28｜COO｜risk：Galhotra 稱今年召回約 1,200 萬輛，召回件數較去年下降（原話："we've recalled about 12 million vehicles"）
- 2026-07-28｜CFO｜guidance：Sherry 被問 2027 年時稱明年的 EBIT 方向現在說太早（原話："It's too early to say at this point."）
- 2026-07-28｜CFO｜guidance：CFO 稱 2027 年大宗商品衝擊規劃為四個季度，對照 2026 年三個季度（原話："we are planning for 4 quarters of impact versus 3"）
- 2026-07-28｜CFO｜margin：Ford Credit 第二季 EBT 數字（原話："EBT of $757 million, up $112 million"）

### 問答異常語氣（迴避／改口／保留）
- F_Q2_2026_Earnings_Call_20260728.md｜問：Spak 問為何下半年 F-Series 指引的量回升在低端、是否為審慎或競爭考量｜答法：先談庫存與需求強勁，被再問後 CFO 回答「就是組合」，未直接說明量回升偏低端的原因
- F_Q2_2026_Earnings_Call_20260728.md｜問：Percoco 問是否與超大規模雲端業者洽談直接購買 Ford Energy 產能｜答法：未直接回答超大規模雲端業者，改談廣泛客戶與專案報價流程，並稱內部預測不展開
- F_Q2_2026_Earnings_Call_20260728.md｜問：Delaney 問關稅進一步緩解空間與 USMCA 美國含量要求對 Ford 的影響｜答法：談立場與原則，關稅部分稱不談細節，未回應含量要求的具體影響
- F_Q2_2026_Earnings_Call_20260728.md｜問：Levy 請管理層重述與同業的成本差距｜答法：未給數字，只稱縮小成本差距是 8% 路線的重點並談下一代產品
- F_Q2_2026_Earnings_Call_20260728.md｜問：Rosner 問 2027 年 EBIT 淨效果是否較高｜答法：列出多項正反因素後，拒絕給方向，稱現在說太早
- F_Q2_2026_Earnings_Call_20260728.md｜問：Langan 問為何下半年 EBIT 年化後呈現放緩｜答法：逐項回答大宗商品與 Novelis 金額，對年化放緩以列舉下半年成本與投資回應，IR 最後提議會後另談模型細節
- F_Q2_2026_Earnings_Call_20260728.md｜問：Yu 問 Ford Defense 未來幾年可能規模｜答法：未給規模，只談 3 台原型車合約，並稱沒有其他可補充

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
{"date":"20260524","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Ford Pro 商用車段持續 best-in-class margin（10%+）並擴大 SaaS recurring revenue","columns":{"2Y 驗證點":"2026 Ford Pro EBIT $6.5-7.5B（已 guide）；軟體訂閱破 100 萬","5Y 驗證點":"Ford Pro 占公司 EBIT > 60%；SaaS ARR > $1B","10Y 驗證點":"商用車 EV 化滲透 > 40% 時 Ford Pro 仍維持 8%+ margin（電動商用車段贏家）","具體數字門檻":"Pro EBIT margin ≥ 10%（連 2 季）；SaaS ARR 同比 +20%","信息來源":"Ford Q1 26 法說會 + 2025 10-K + Q4 25 投資者日","漂移觸發":"連 2 季 Pro margin"}},{"id":"H2","text":"Model e 段虧損漸縮 + Universal Platform $30K truck 證明可賺錢","columns":{"2Y 驗證點":"2026 Model e 虧損 $4-4.5B（已 guide）；Q4 26 季虧縮至","5Y 驗證點":"Universal Platform 首款車（2027/8）量產順利；2029 Model e 損平","10Y 驗證點":"EV 段占公司 EBIT > 0%（從虧轉盈）","具體數字門檻":"Model e 季虧 50K","信息來源":"Ford 2025/12 戰略簡報 + Kentucky $2B 投資案","漂移觸發":"季虧 > $1.3B 連 2 季 → 削弱；連 3 季 > $1.5B → 反轉"}},{"id":"H3","text":"OEM 圈估值倍數從目前 6-10x 區間 mean revert 至 10-12x（multiple re-rating）","columns":{"2Y 驗證點":"Fwd PE 從 9.2x 修復至 10x+ → 股價 +9%","5Y 驗證點":"OEM 圈整體估值結構性復甦（接近 SPX P/E）","10Y 驗證點":"—（不適用，10Y 看則 OEM 已被新 mobility 範式取代）","具體數字門檻":"同業中位 Fwd PE > 10x（Toyota 已 10.57x）","信息來源":"StockAnalysis.com / Macrotrends 5Y Fwd PE 歷史","漂移觸發":"同業中位"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Ford Pro margin 結構性壓縮（競爭 + 工資成本）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Ford Pro 季度 EBIT margin、SaaS 訂閱數","警戒閾值":"margin 連 2 季"}},{"id":"R2","text":"Model e Universal Platform 再次失敗（impairment 第二輪）","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Kentucky 廠進度、$30K EV truck 預售訂單、Model e 季虧","警戒閾值":"Q4 26 季虧 > $1.3B / Q2 27 Universal Platform 預售"}},{"id":"R3","text":"Ford Credit 槓桿放大車市下行（信用收縮 + 壞帳率）","columns":{"對應假設":"H3（間接）","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Ford Credit 60+ delinquency rate、Net charge-off、ABS spread","警戒閾值":"delinquency > 4%（vs 目前 ~2.5%）/ ABS spread + 100bp"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":"侵蝕","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":14.93,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/F_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
