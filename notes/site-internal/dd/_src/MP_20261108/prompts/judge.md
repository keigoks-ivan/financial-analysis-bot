你是 stock-analyst **v20 判斷 agent**，標的 MP（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MP","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MP_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MP_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_ppa_income","label":"營收（GAAP，不含 PPA Income）","value":147.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 investors.mpmaterials.com Q3 2026 results"},"note":"未取得單季共識"},{"id":"f_kpi1_ppa_income","label":"營收＋PPA Income","value":155.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q3 2026 results"},"note":"未取得"},{"id":"f_kpi2_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（公司未揭露 Non-GAAP 營業利益，以此代）","value":41.1,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q3 2026 results"},"note":"未取得"},{"id":"f_kpi3_gaap","label":"GAAP 營業利益（損失）","value":-22.1,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q3 2026 results"},"note":"未取得"},{"id":"f_kpi7_ndpr","label":"NdPr 產量／銷量","value":1018,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"MT（銷量 1,020 MT）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q3 2026 results"},"note":"未取得"},{"id":"f_kpi8","label":"期末現金與短期投資","value":1337.9,"period":"Q3 2026（2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q3 2026 results"},"note":"n/a"},{"id":"f_kpi9","label":"管理層指引","value":null,"period":"Q3 2026（公告於 2026-11-05）","unit":"定性","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q3 2026 results"},"note":"n/a","needs_sonnet":true},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mp_gross_margin_pct","label":"MP 毛利率","value":-16.15,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MP.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mp_operating_margin_pct","label":"MP 營業利益率","value":-34.06,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MP.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mp_fcf_margin_pct","label":"MP FCF 利潤率","value":-165.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MP.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_alb_gross_margin_pct","label":"ALB 毛利率","value":25.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALB.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_alb_operating_margin_pct","label":"ALB 營業利益率","value":16.27,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALB.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_alb_fcf_margin_pct","label":"ALB FCF 利潤率","value":23.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALB.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_usar_gross_margin_pct","label":"USAR 毛利率","value":-11.22,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.USAR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_usar_operating_margin_pct","label":"USAR 營業利益率","value":-946.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.USAR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_usar_fcf_margin_pct","label":"USAR FCF 利潤率","value":-1865.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.USAR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_uuuu_gross_margin_pct","label":"UUUU 毛利率","value":47.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UUUU.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_uuuu_operating_margin_pct","label":"UUUU 營業利益率","value":-62.09,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UUUU.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_uuuu_fcf_margin_pct","label":"UUUU FCF 利潤率","value":-95.79,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UUUU.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_gaap_eps","label":"GAAP 淨損／稀釋 EPS","value":-20.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m（EPS -0.12；Adjusted EPS 0.04）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q3 2026 results"},"note":"未取得"},{"id":"f_kpi5","label":"自由現金流（單季，由九個月累計減上半年推算）","value":-125.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"推算：九個月 OCF -7.8、capex 420.3（Q3 新聞稿）減上半年 OCF +4.9、capex 307.7（Q2 8-K 2026-08-06）；公司未直接報 FCF"},"note":"未取得"},{"id":"f_kpi6_sbc","label":"SBC 占營收","value":7.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q3 2026 results（SBC 11.3m ÷ 營收 147.7m；營業利益為負故不以營業利益為分母）"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":35.41,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-47.49,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":34.19,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（-0.01 → -0.01）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（0.74 → 0.74）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.31 → 1.31）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":-0.01,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":0.74,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":1.31,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":12.17,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝7.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":7.7,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":11.49,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝2.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":2.5,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":3830.0,"period":"2026-10-22","unit":"x","basis":"分母＝FY1 EPS 0.01，分子＝快照價 38.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-22"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-354.29,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 983.62、現金 1337.91（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":178.23,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":5957.01,"period":"2026-11-08","unit":"USD m","basis":"市值 6311.3 ＋ 淨負債 -354.29","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":453.16,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（13 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":786.15,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（13 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":13.15,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 35.41 / W52 54.95 / W104 46.82 / W250 34.12 / W250 13週斜率 -0.28%"},{"id":"f_ma_w52","label":"52 週均線","value":54.95,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":46.82,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":34.12,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-0.28,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 稱中國兩大集團控制幾乎全部中國精煉與濃縮配額，2025 年進一步集中；中國以外僅一家大型整合營運商（澳洲／馬來西亞），NdFeB 磁鐵亦由中國主導。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"Outside of China, there are few producers operating at scale, with only one other major integrated operator across Australia and Malaysia. China also maintains a dominant position in the supply of NdFeB permanent magnets due to its vast rare earth reserves, advanced processing capabilities, and vertically integrated production infrastructure.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子明言新進入者可能透過併購、合作進入市場，且產業整併可能使對手具更強產品或定價彈性。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"In addition, new entrants not currently considered competitors may enter our market through acquisitions, partnerships, or strategic relationships. We expect these trends to continue as demand for rare earth materials increases.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"USA Rare Earth 在奧克拉荷馬州 Stillwater 磁鐵廠調機，目標 2026 Q4 達 600 MT/年，為美國本土磁鐵直接新進入者。","source":"Motley Fool: MP Materials vs USA Rare Earth","url":"https://www.fool.com/investing/2026/02/14/mp-materials-vs-usa-rare-earth-which-stock","excerpt":null,"as_of":"2026-02-14","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"報導稱 Stillwater 磁鐵廠出現主要競爭對手。","source":"OK Energy Today: Major rival emerges for Stillwater rare earth magnet firm","url":"https://www.okenergytoday.com/2026/02/major-rival-stillwater-rare-earth-magnet-firm","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K 披露客戶集中度：Materials 客戶 A、B 占總營收 30%、23%，Magnetics 客戶 C 占 31%","source":"MP Materials FY2025 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"Customer C, primarily in the Magnetics segment, accounted for 31% of the Company’s total revenue. For the year ended December 31, 2024, Customers B and A in the Materials segment accounted for 78% and 20% of the Company’s total revenue, respectively. For the year ended December 31, 2023, Customer B in the Materials segment accounted for 96% of","as_of":"2026-02-28","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025：客戶 A（材料）30%、B（材料）23%、C（主要磁材）31%，前三大合計約84%；2024 年 B 78%、A 20%；2023 年 B 96%。","source":"SEC EDGAR 10-K FY2025 Item 8 Concentration of Customer Risk","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"For the year ended December 31, 2025, Customers A and B in the Materials segment accounted for 30% and 23% of the Company’s total revenue, respectively; Customer C, primarily in the Magnetics segment, accounted for 31% of the Company’s total revenue.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"公司稱預期 DoW 可能成為最大磁材客戶，且高度依賴 DoW 資金撥款（需國會撥款）；撥款延遲或受限可能需另尋融資。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"we anticipate that the DoW may become our largest customer of magnets and that the obligations of the DoW under the Price Protection Agreement and DoW Offtake Agreement may represent a significant source of our revenue.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"公司自評信用風險有限，現有合約對象有可靠付款紀錄；未揭露客戶信用惡化事件。","source":"SEC EDGAR 10-K FY2025 Item 8 Concentration of Credit Risk","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"The Company believes that its credit risk is limited because the Company’s current contracts are with companies that have a reliable payment history.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2026 Q3 10-Q：客戶A（材料）單季33%／前九月37%，客戶B（材料）23%／26%，客戶C（磁材）12%／16%。","source":"SEC EDGAR 10-Q Q3 2026 Note 2 Concentration of Customer Risk","url":"https://www.sec.gov/Archives/edgar/data/0001801368/000180136826000057/mp-20260930.htm","excerpt":"Customer A in the Materials segment accounted for 33% and 37%, respectively","as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"美國業者向 Reuters 表示 2027-01-01 對中國來源材料的國防供應鏈禁令前，無法建足夠加工與磁體產能；政府考慮延長部分取用","source":"Oilprice.com: Pentagon Suppliers Warn U.S. Won't Have Magnet Capacity By 2027","url":"https://oilprice.com/Metals/Commodities/Pentagon-Suppliers-Warn-US-Wont-Have-Magnet-Capacity-By-2027.amp.html","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.H","triggers"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"IDTechEx 預期全球稀土磁體產能擴張將大幅超過需求成長，2037 年全球產能利用率降至 59%","source":"IDTechEx (經 Skillings/搜尋摘要引用)","url":"https://www.skillings.net/rare-earths-supply-chain-2026-magnet-capacity-reaches-300000-tonnes/","excerpt":"IDTechEx expects the expansion of global rare earth magnet production capacity to significantly outstrip demand growth, resulting in worldwide capacity utilization falling to 59% in 2037.","as_of":"2026-06-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"美國磁體產能擴張時程：USA Rare Earth 奧克拉荷馬廠 2027 年達 1,200 噸/年、南卡廠 2028-04 首產 6,400 噸/年；JS Link 喬治亞廠 3,000 噸/年預計 2027 年底商業生產","source":"搜尋摘要（Skillings／SMM／ProjectBlue）","url":"https://projectblue.com/blue/news-analysis/1304/js-link-america-announces-construction-of-ndfeb-magnet-facility-in-georgia,-usa","excerpt":"The new facility is targeted to produce 3ktpy of rare-earth permanent magnets, with commercial production scheduled for late 2027.","as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"DoD 與 MP 協議：10 年 NdPr $110/kg 價格底、10X 磁體廠 10 年 100% 包銷、保證年 EBITDA 至少 1.4 億美元；風險在於價格底補貼須國會年度撥款（FY26 DPA 基金請求 2.66 億美元，低於以現價估算的年付款）","source":"The Deep Dive / FAS 摘要","url":"https://thedeepdive.ca/would-trumps-110-kg-rare-earth-floor-work/","excerpt":null,"as_of":"2025-09-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"SMM 2026-10 分析：2027 年 NEV NdFeB 需求由 76,954 噸增至 79,832 噸（+3.74%），成長慢於下游產出；電腦裝置 -12.76%、電動工具 -10.89%","source":"SMM Analysis: Pr-Nd Retreats: NdFeB Demand in 2027 - 2026 Q4 Scenario","url":"https://news.metal.com/newscontent/104188901-pr-nd-retreats-ndfeb-demand-in-2027%E2%80%8B-2026-q4-scenario-smm-analysis","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K風險因素指出，因DoW交易協議，公司可能面臨更嚴格審查、政府稽核／調查、國會關注及司法部執法（含False Claims Act）等；未見反壟斷調查之陳述。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"The Company may be subject to heightened scrutiny of our business activities with both government and non-government customers, government audits, investigations, congressional scrutiny, inquiries about conflicts of interest, civil or criminal enforcement by the Department of Justice (including actions under the False Claims Act)","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"2026年搜尋未見針對MP的DOJ／FTC／EU反壟斷調查或拆分報導；所見爭議為對USA Rare Earth的營業秘密訴訟，屬非競爭法案件。","source":"WebSearch 結果摘要（pulse.bot: MP Materials Accuses USA Rare Earth of Magnet Tech Theft）","url":"https://www.pulse.bot/mining/news/mp-materials-accuses-usa-rare-earth-of-magnet-tech-theft-02f9bce2-a5c5-4aaa-880c-31992e5ce2d6/","excerpt":"MP alleges that a former employee handed over its proprietary \"grain boundary diffusion\" formulations to USA Rare Earth","as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：公司在全球銷售，美國關稅政策、出口管制或其他貿易限制的變動難以預測，可能對公司造成重大不利影響；現任政府已對中國、加拿大、墨西哥進口品加稅。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"Significant political, trade, or regulatory developments in the jurisdictions in which we sell our products, including changes in tariff policies by the U.S. administration, export controls, or other trade restrictions, are difficult to predict and may have a material adverse effect on us.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K MD&A：2025 年中國擴大稀土出口管制；2025 年 11 月美中協議中國同意暫停擴大管制與報復性關稅；此情勢帶來供應鏈波動與對非中國供應鏈的需求增加，可能對公司產品需求有重大影響。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"While in November 2025 the U.S. reached a trade and economic deal in which China agreed to suspend implementation of the expanded export controls and to suspend retaliatory tariffs and non-tariff measures imposed since March 2025, these developments have led and continue to lead to several market trends","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","thesis.H","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K MD&A：精礦售價以扣除稅、關稅後的暫定市價計；DoW 協議與 Apple、GM 供應協議提供需求確定性，但美中等國貿易政策變動（新增或調整關稅）仍可能影響流動性。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"further changes in trade policies in the United States, China or other countries, including the implementation of new tariffs, increases in or reductions of existing tariffs, or the taking of other actions.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"中國商務部 2026-06-22 將 MP Materials 與 USA Rare Earth 等美國實體列入出口管制清單，禁止向其出口兩用物項","source":"Mining Weekly: China places two US rare earths producers on export control list","url":"https://www.miningweekly.com/article/china-places-two-us-rare-earths-producers-on-export-control-list-2026-06-22","excerpt":null,"as_of":"2026-06-22","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"2026 年 Section 232 關鍵礦物公告：採納 Commerce 認定，指示談判協議；聚焦稀土永磁加工依賴外國","source":"Recycling Today: Trump proclamation critical minerals","url":"https://www.recyclingtoday.com/news/usa-trump-proclamation-critical-minerals-nickel-cobalt-rare-earths-import-negotiations-tariffs","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中國商務部於 2026-06-22 將 MP Materials 與 USA Rare Earth 列入出口管制清單，禁止中國原產雙用途物項轉移給這些公司","source":"Mining Weekly: China places two US rare earths producers on export control list","url":"https://www.miningweekly.com/article/china-places-two-us-rare-earths-producers-on-export-control-list-2026-06-22","excerpt":null,"as_of":"2026-06-22","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"MP 2020 年 SEC 說明書稱中國是全球稀土供應鏈的單點失效，MP 定位為國內替代","source":"MP Materials S-1 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1801368/000119312520313937/d48477ds1.htm","excerpt":null,"as_of":"2020-11-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 Q3 合併營收 $147.7M、年增 176%；Materials 段營收 $133.5M（年增 322%），其中 NdPr 氧化物與金屬 $101.0M、其他 $32.6M（主要為 $31.6M 一次性 SEG+ 銷售給美國航太國防客戶）；PPA 收入 $8.1M；磁材前驅物營收因 Independence 磁材投產略降。","source":"MP Materials 8-K Q3 2026 earnings release / 10-Q (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001801368/000180136826000056/mpmcq32026er.htm","excerpt":null,"as_of":"2026-11-06","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"稀土精礦營收因 2025 年 7 月起停止對中國銷售，預期未來期間將大幅偏低。","source":"MP Materials 10-Q Q3 2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001801368/000180136826000057/mp-20260930.htm","excerpt":null,"as_of":"2026-11-06","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Visible Alpha 共識：MP Magnetics 營收 2026 年約 $75M（2025 年 $67M），2027 年升至 $208M；S&P 指 NdPr 需求成長。","source":"S&P Global Market Intelligence, MP Materials magnetics revenue poised to surge as NdPr demand grows","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/09/mp-materials-magnetics-revenue-poised-to-surge-as-ndpr-demand-grows","excerpt":null,"as_of":"2026-09-10","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"BMI 預期全球 NdPr 氧化物需求成長 7.7%，2026 年 NdPr 價格約 $90,000/t（2026-01-15 觸及 $97,969/t 多年高點）。","source":"Engineering News / Mining Weekly, NdPr oxide price forecast to rise to $90 000/t this year","url":"https://www.engineeringnews.co.za/article/ndpr-oxide-price-forecast-to-rise-to-90-000t-this-year-report-2026-02-02","excerpt":null,"as_of":"2026-02-02","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"SMM：2027 年 NdFeB 需求不會收縮，但成長將落後下游產出；消費端為支撐而非價格上漲動能。","source":"SMM (news.metal.com) 2026 demand model analysis","url":"https://news.metal.com/newscontent/103818093-smm-analysis-march-pr-nd-drop-likely-due-to-weak-demand-outlook-2026-demand-model-part-1","excerpt":null,"as_of":"2026-03-15","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"DoD 與 MP 的 10 年協議：NdPr 價格下限 $110/kg，低於則政府補差額，高於部分政府分 30%；僅適用 MP 產出。Q2 2026 實現價指引為 $90 出頭至中段。","source":"Mining.com / Barchart, DoD backs MP Materials in $110/kg rare earth pricing deal","url":"https://www.nasdaq.com/articles/dod-backs-mp-materials-mp-110-kg-rare-earth-pricing-deal","excerpt":null,"as_of":"2025-07-10","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"0","claim":"Argus：美國至少 56,000t 新稀土磁材產能在開發中","source":"Argus Media US rare earth magnet capacity","url":"https://www.argusmedia.com/en/news-and-insights/market-insight-papers/us-rare-earth-magnet-capacity","excerpt":null,"as_of":"2026-09-09","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"MP 在 FY2025 10-K 風險因子自陳：若下游產業採用不需稀土或 NdFeB 磁鐵的新技術，或出現合適替代品，需求會下降並對業務造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"Technology changes rapidly in the industries and end-markets that utilize our materials. If these industries introduce new technologies or products that no longer require the rare earth materials or NdFeB magnets we produce or may produce in the future, or suitable substitutes become available, this could result in a decline in demand for our rare earth materials or NdFeB magnets.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"IDTechEx 預測 2035 年近 30% 電動車市場將使用無稀土馬達（含外激磁同步馬達）。","source":"IDTechEx via electricvehiclesresearch.com","url":"https://www.electricvehiclesresearch.com/articles/32237/magnetic-materials-that-could-replace-rare-earths-in-ev-motors","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"公司自 2023 起由賣濃縮礦（經經銷）轉向中游分離產品，直接賣給終端用戶並經經銷商，營收主要來自磁材供應鏈；Sumitomo 為日本 NdPr 獨家經銷至 2030 年底。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"In 2023, the Company commenced midstream operations, consisting of the latter three primary process steps, to produce separated rare earth products that are marketed directly to end users and indirectly through distributors, with revenue generated primarily from the magnet supply chain.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"搜尋摘要指 Q3 2026 10-Q 稱 NdPr 營收主要來自 Sumitomo 銷售及 2026 年 Q1 與美國大型科技／工業公司簽的 offtake；2025 年 7 月起停止對中國銷售；獨立工廠量產後預期以永久磁鐵為主。","source":"SEC EDGAR 10-Q（2026-09-30）搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001801368/000180136826000057/mp-20260930.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"10X 磁材廠：DoW 承諾十年購買全部磁鐵（除非商業轉售），預期 2028 年試車、年產約 7,000 噸","source":"Magnetics Magazine","url":"https://magneticsmag.com/mp-materials-to-build-10x-magnet-manufacturing-campus-in-texas-disengages-business-dealings-in-china/","excerpt":"Off on MP Materials to Build “10X” Magnet Manufacturing Campus in Texas; Disengages Business Dealings in China MP Materials will invest more than $1.25 billion to develop the largest and most strategic U.S. rare earth magnet manufacturing asset in history. February 26, 2026 — MP Materials Corp. today announced it has selected a 120acre site in Northlake, Texas, to develop “10X,” the","as_of":"2026-03-02","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 2026-09-25 頁面：分析師平均目標價 $76.29、共識 Moderate Buy；JPMorgan、Barclays 近期下調目標價（Barclays 7/16 由 $69 降至 $65，overweight）。未讀原頁，原文未核。","source":"MarketBeat instant alert 2026-09-25","url":"https://www.marketbeat.com/instant-alerts/price-mp-materials-nyse-mp-stock-price-down-1-time-to-sell-2026-09-25/","excerpt":null,"as_of":"2026-09-25","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Chartmill（2026-10 資料）：EPS 預估 23 位分析師；下一財年 EPS 預估 1 個月降 17.56%、3 個月降 57.21%；Q3 2026 共識 EPS -$0.01、營收約 $120.18M，預定 2026-11-05 公布（未查到實際結果）。原文未核。","source":"Chartmill MP estimates page","url":"https://www.chartmill.com/stock/quote/MP/estimates","excerpt":null,"as_of":"2026-10-18","retrieved_at":"20261108","affects":["valuation","triggers","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"公司僅重申 FY2026 資本支出指引 $500–600M，未見正式營收／EPS 數字指引；搜尋未見指引上修或下修的直接報導。原文未核。","source":"MP Materials Q1 2026 earnings call transcript (Motley Fool) / Q1 2026 8-K","url":"https://www.fool.com/earnings/call-transcripts/2026/05/07/mp-materials-mp-q1-2026-earnings-transcript/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 2026 營收 $108.5M 高於共識約 $99.18M，調整後 EPS -$0.01 低於共識 $0.01（Zacks 版本為共識 -$0.02）；該季共識 EPS 30 天內下修 14.3%。原文未核。","source":"Chartmill news: MP Materials Q2 loss, beats revenue estimates","url":"https://www.chartmill.com/news/external/113184/mp-materials-corp-mp-reports-q2-loss-beats-revenue-estimates","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Walnut Invest：2026-08 平均目標價 $77.78（16 位分析師）、中位 $80、區間 $60–$100","source":"Walnut Invest MP forecast","url":"https://walnutinvest.com/stocks/mp/forecast","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"+","claim":"2025-11-19 8-K Item 8.01：MP 與美國戰爭部合作，和沙烏地 Maaden 成立策略合資，在沙烏地興建稀土精煉廠。","source":"SEC EDGAR 8-K (2025-11-19) Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1801368/000119312525287046/d39340d8k.htm","excerpt":"On November 19, 2025, MP Materials Corp. (the “Company”) issued a press release that it has partnered with the U.S. Department of War (“DOW”) to establish a strategic joint venture with Maaden, Saudi Arabia’s flagship mining company, to develop a rare earth refinery in the Kingdom of Saudi Arabia.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月6份8-K中僅1份含重大項目（即上述Item 8.01）；其餘為財報、股東投票，無1.03/4.02/5.01等事件。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001801368&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露與一家營建總包商的仲裁爭議，已估列損失；若不利結果可能對財報有重大影響。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm","excerpt":"The Company is currently in a dispute with a general contractor for a construction project, which is in binding arbitration.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Argus Media 2026-09 報導：美國至少有 56,000 噸新稀土磁鐵產能在開發中（同業擴產，未見紀律性克制的證據）","source":"Argus Media market insight paper: US rare earth magnet capacity","url":"https://www.argusmedia.com/en/news-and-insights/market-insight-papers/us-rare-earth-magnet-capacity","excerpt":null,"as_of":"2026-09-09","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"USA Rare Earth Stillwater Phase 1a 磁鐵線 2026-03 投產，目標 2026 年底 600 mtpa、2027 Q1 Phase 1b 後合計 1,200 mtpa","source":"Barchart / Metal.com (SMM) USAR 報導","url":"https://news.metal.com/en/newscontent/103837340-USA-Rare-Earth-to-Start-Commercial-Magnet-Shipments-in-April-Aiming-for-1200-mt-Annual-Capacity-by-2027","excerpt":null,"as_of":"2026-03-30","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"MP Materials 10X 廠（德州 Northlake）預計 2028 開始生產，完工後磁鐵總產能 10,000 mt/年；資本支出約 $1.25–1.3B（二手彙整）","source":"Metal.com (SMM): MP Materials Eyes Northlake, Texas for 10X Plant","url":"https://news.metal.com/newscontent/103713047/mp-materials-eyes-northlake-texas-for-new-10x-plant-to-boost-us-rare-earth-magnet-capacity","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Evolution Metals & Technologies：13 台 ULVAC 燒結磁鐵設備預計 2026-11 交機安裝，完成後韓國浦項年磁鐵產能逾 10,000 噸（約 6,000 噸高性能燒結）；FY2027 營收指引 $400–460mm 為公司自述","source":"Investegate / FinanceWire EMAT press release","url":"https://www.investegate.co.uk/announcement/fnw/financewire-news--fnews/evolution-metals-technologies-provides-init-/9766058","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"JS Link America 投資約 $223M 在喬治亞州 Columbus 建稀土磁鐵廠，預計 2027 開始營運","source":"Mining.com","url":"https://www.mining.com/js-link-america-to-invest-223m-in-rare-earth-magnet-manufacturing-plant-in-georgia","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#5","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Energy Fuels 整合平台目標年產約 15,700 噸磁鐵，並有 $725M 美國有條件融資（20 年貸款，待盡調與正式協議）","source":"Pulse2: Energy Fuels mine-to-magnet platform","url":"https://pulse2.com/energy-fuels-mine-to-magnet-platform-targets-15700-tons-of-annual-magnets-as-725-million-u-s-financing-advances/amp/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#6","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Lynas FY2026 Q3（至 2026-03-31）NdPr 產量 1,996 噸、年增 32%，2026-03 首次產出氧化釤，預期重稀土初期年產約 400 噸並待新增分離產能","source":"Zacks / Metal.com 彙整 Lynas","url":"https://www.zacks.com/stock/news/3002904/can-mp-materials-deliver-another-year-of-production-growth","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"MP 2026-09-30 總存貨約 $293.2M，高於 2026-06-30 的 $279.5M 與 2025 年底 $252.1M；Q3 認列 $6.4M 非核心產品 LCNRV 減損，存貨增加原因未查到","source":"MP Materials Form 10-Q (Q3 2026)","url":"https://www.sec.gov/Archives/edgar/data/0001801368/000180136826000057/mp-20260930.htm","excerpt":null,"as_of":"2026-11-06","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"MP Q3 2026 營收年增 176% 至 $147.7M，主因 NdPr 氧化物與金屬銷量及市場價格較高；調整後 EBITDA $41.1M","source":"MP Materials Form 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001801368/000180136826000056/mpmcq32026er.htm","excerpt":null,"as_of":"2026-11-06","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"2026 年初 NdPr 價格大幅上漲，約 $104/kg(2026-03)，另有來源稱達約 $123/kg；近期 SMM 日評顯示 Pr-Nd 氧化物下跌 3,500 元/噸（日期未確認）","source":"rallies.ai / SMM daily review（搜尋摘要）","url":"https://news.metal.com/newscontent/104056087-rare-earth-prices-show-divergence-pr-nd-is-weaker-while-medium-heavy-rare-earth-holds-steady-smm-rare-earth-daily-review","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"SMM：2026 年中磁材廠以補庫為主；2026-03 Pr-Nd 下跌與需求展望偏弱、經銷去庫有關；SMM 預期中國 2026 磁材出口可能超過 67,500 噸","source":"SMM Analysis（搜尋摘要）","url":"https://news.metal.com/newscontent/103820368/smm-analysis-march-pr-nd-drop-likely-due-to-weak-demand-outlook-2026-demand-model-part-2","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"MP FY2023 10-K：2023年稀土精礦營收年減51%，實現價格每REO公噸年減43%；定價高峰在2022年2月；全年調整後EBITDA margin約40%。","source":"MP Materials Form 10-K FY2023 / Q4 2023 8-K","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136824000014/mp-20231231.htm","excerpt":null,"as_of":"2024-02-29","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"MP Q1 2024：營收年增20%至$62.9M，REO實現價年減23%，調整後EBITDA為$(11.2)M（年減$26.7M），為上輪下行期EBITDA轉負。","source":"MP Materials Q1 2024 earnings 8-K（經搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/1801368/000180136824000085/mpmcq32024er.htm","excerpt":null,"as_of":"2024-05-09","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"SMM 報導：PrNd氧化物2022上半年約81萬至110萬人民幣/噸；2024年5月下旬約37.5萬至37.7萬人民幣/噸，自高點下跌約三分之二、歷時約兩年（跌幅為搜尋摘要所算，未見單一來源明載谷底日）。","source":"SMM metal.com / SunSirs 價格報導","url":"https://news.metal.com/newscontent/102782361/Pr-Nd-oxide-prices-continued-to-drop-but-the-decline-slowed-down","excerpt":null,"as_of":"2024-05-31","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Ex-China NdPr價格跌破MP與DoD協議的$110/kg底價，約$95,000/噸","source":"Benchmark Source","url":"https://source.benchmarkminerals.com/article/ex-china-ndpr-prices-slip-below-110-kg-price-floor-as-oversupply-builds","excerpt":"Ex-China NdPr prices slip below $110/kg price floor as oversupply builds","as_of":"2026-08-21","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"+","claim":"2025-11-19 與美國戰爭部、Maaden 成立沙烏地稀土精煉合資（合資，非併購MP本身）。搜尋未見MP為買方或標的的2026年併購。","source":"SEC EDGAR 8-K (2025-11-19) Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1801368/000119312525287046/d39340d8k.htm","excerpt":"partnered with the U.S. Department of War (“DOW”) to establish a strategic joint venture with Maaden, Saudi Arabia’s flagship mining company, to develop a rare earth refinery in the Kingdom of Saudi Arabia.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MP","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":-16.15,"operating_margin_pct":-34.06,"fcf_margin_pct":-165.23,"rd_intensity_pct":8.0},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MP","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"LYC.AX","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LYC.AX"},"note":"quarterly_income_stmt 無資料"},{"name":"ALB","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.84,"operating_margin_pct":16.27,"fcf_margin_pct":23.47,"rd_intensity_pct":0.54},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALB","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"USAR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":-11.22,"operating_margin_pct":-946.09,"fcf_margin_pct":-1865.38,"rd_intensity_pct":278.35},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.USAR","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"UUUU","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":47.9,"operating_margin_pct":-62.09,"fcf_margin_pct":-95.79,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UUUU","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"MP"},"financial_history":{"ticker":"MP","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":527510000.0,"revenue_yoy_pct":null,"gross_margin_pct":79.04,"operating_margin_pct":63.5,"net_income":289004000.0,"diluted_eps":1.52,"free_cash_flow":16919000.0,"fcf_margin_pct":3.21,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":253445000.0,"revenue_yoy_pct":-51.95,"gross_margin_pct":41.44,"operating_margin_pct":1.42,"net_income":24307000.0,"diluted_eps":0.14,"free_cash_flow":-199198000.0,"fcf_margin_pct":-78.6,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":203855000.0,"revenue_yoy_pct":-19.57,"gross_margin_pct":-32.76,"operating_margin_pct":-80.32,"net_income":-65424000.0,"diluted_eps":-0.57,"free_cash_flow":-173069000.0,"fcf_margin_pct":-84.9,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":224441000.0,"revenue_yoy_pct":10.1,"gross_margin_pct":-25.67,"operating_margin_pct":-64.64,"net_income":-85874000.0,"diluted_eps":-0.5,"free_cash_flow":-328130000.0,"fcf_margin_pct":-146.2,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MP/MP_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**MP Materials Corp.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Hello, and welcome to the MP Materials Third Quarter 2026 Earnings Call. [Operator Instructions] Also as a reminder, this conference is being recorded. If you have any objections, please disconnect at this time. 
With that, I'd like to turn the call over to Martin Sheehan, Head of Investor Relations. Mr. Sheehan, you may begin.

**Martin Sheehan** (Executives):
Thank you, operator, and good afternoon, everyone. Welcome to the MP Materials Third Quarter 2026 Earnings Conference Call. With me today from MP Materials are Jim Litinsky, Founder, Chairman and Chief Executive Officer; Michael Rosenthal, Founder and Chief Operating Officer; and Ryan Corbett, Chief Financial Officer. 
As a reminder, today's discussion will contain forward-looking statements relating to future events and expectations that are subject to various assumptions and caveats. Factors that may cause the company's actual results to differ materially from these statements are included in today's presentation, earnings release and in our SEC filings. In addition, we have included some non-GAAP financial measures in this presentation. Reconciliations to the most directly comparable GAAP financial measures can be found in today's earnings release and the appendix to today's slide presentation. Any reference in our discussion to EBITDA means adjusted EBITDA and tons means metric tons. Finally, the earnings release and slide presentation are available on our website. 
With that, I'll turn the call over to Jim. 
Jim?

**James Litinsky** (Executives):
Thank you, Martin. Good afternoon, everyone. MP delivered another strong quarter across the business with continued growth in NdPr production and sales volumes and solid execution on several important strategic initiatives. In our Materials segment, third quarter NdPr production increased 41% year-over-year to 1,018 metric tons, in line with the outlook we provided in August. And demand for our product remains very strong with NdPr sales volumes reaching 1,020 metric tons, up 94% year-over-year. 
Michael and the team also made strong progress on our heavy rare earth separation circuit during the quarter, and I am pleased to say that the commercial scale production of dysprosium and terbium will begin this quarter, Q4. This will support our heavy rare earth needs for EV traction motor magnets produced at Independence. We also benefited from the strategic value of the inventory we have built through our separation operations. Since we began commercial scale light rare earth separation a couple of years ago, we have stockpiled a heavy rare earth fraction of our production while developing our heavy rare earth separation capabilities. 
We often refer to this fraction as SEG+. Amid geopolitically driven supply constraints, particularly in heavy rare earths, we sold a modest portion of our SEG+ inventory to support an important strategic customer. The sale generated attractive economics, and we retained several hundred tons of feedstock to support our own future production. Altogether, we generated $141.6 million of revenue and PPA income and $47.8 million of adjusted EBITDA for the Materials segment in the quarter. 
In our Magnetics segment, we have completed qualification and will begin shipping salable magnets to GM this quarter. Ryan will provide additional detail on what to expect over the next several quarters, but I want to recognize our incredible magnetics team. We built this business from scratch, and I believe we are on our way to becoming the most advanced, most profitable and best scaled magnetics platform in the world. 10X remains on schedule for commissioning in late 2028. 
As we work to ramp up magnet deliveries to GM and expand Independence to begin deliveries to Apple in 2027, we continue to improve our production processes from precursor products all the way through finished magnets. We are still in the early stages of our ramp and expansion, but we are already generating solid financial results. This quarter was another good one with segment revenue of $18.6 million and adjusted EBITDA of $5.3 million. 
With that, I'll turn the call over to Ryan to walk through our financial results, and then Michael will provide additional details on our operations. 
Ryan?

**Ryan Corbett** (Executives):
Thank you, Jim. Consolidated revenue plus PPA income totaled $155.8 million in the quarter, an increase of 23.6% sequentially, reflecting strong operating performance across the business. The year-over-year improvement was broad-based, driven by a nearly doubling of NdPr sales volumes, higher realized market prices, a onetime SEG+ sale and the addition of PPA income, which, as you'll recall, we began earning in the fourth quarter of 2025. The combination of higher revenue and PPA income drove a $53.7 million year-over-year improvement in adjusted EBITDA. And finally, our substantial improvement in adjusted EBITDA, both sequentially and year-over-year flowed through to meaningful improvements in adjusted diluted EPS compares. 
Looking ahead to the fourth quarter, we expect the strong operating performance in our Materials segment to continue. NdPr oxide volumes and realized prices are expected to remain broadly consistent with Q3 at approximately 1,000 metric tons and $100 per kilogram, respectively. At that level of realized pricing and with our expected product mix, we expect to earn approximately $8 per kilogram of PPA income on sold NdPr. Similar to Q3, we do not expect to recognize any PPA income associated with NdPr contained in stockpiled concentrate. 
Looking forward to 2027, we expect to continue to see leverage in our cost structure as production volumes of NdPr increase and cost optimization projects bear fruit. We may see some lumpiness during the start-up of chlor-alkali early in the year, but we ultimately remain very confident in our ability to see strong progress in reducing our cost per NdPr kilogram produced, particularly in the back half of the year as operations across heavy rare earth separation and chlor-alkali stabilize. 
Switching to magnetics. At the end of the third quarter, we had approximately $28 million of deferred revenue remaining related to magnetic precursor products. We expect to recognize that revenue over the next several quarters at a declining rate as we work down the remaining balance and ramp up magnet production. I'll also note the lumpiness in margins we flagged last quarter. This is driven primarily by the transition from precursor production to the initial ramp of magnet production, while we also invest significantly in our team, capabilities, R&D and start-up operations to position the business for strong future growth. 
As part of that transition, a growing share of our manufacturing costs, particularly depreciation, is now allocated to magnet production rather than solely to precursor products. Because of how our precursor contracts are priced, this reduces precursor revenue in the near term. Ultimately, these costs will earn an attractive margin within our magnet products as magnet sales ramp. On that ramp, we remain in the very early stages of production scale-up. So magnet sales are likely to be lumpy quarter-to-quarter. 
In addition to a measured scale-up of production volumes, magnet revenues will ultimately be dictated by a deliberate phase-in by our foundational customer. As is typical in automotive supply transitions, they will work through existing supply and incorporate our magnets into specific programs and plants over time. As with any complex manufacturing ramp, progress is unlikely to be perfectly linear as we increase throughput, extend production runs and optimize the process. 
We, therefore, expect magnet volumes to build gradually, starting quite modestly over the next couple of quarters before increasing in the back half of 2027, when we also expect production for Apple to begin contributing. Putting this together, while we expect magnet sales to generate positive adjusted EBITDA from the outset, we expect the overall adjusted EBITDA contribution from magnetics to continue to be modest in 2027, particularly in the first half as declining precursor revenue offsets the early ramp in magnet sales. We expect the full earnings power of this segment to become visible in 2028. 
Moving on to the balance sheet and cash flow. Year-to-date capital expenditures totaled $413.8 million across the business. Approximately 60% of that spend was related to magnetics, primarily for construction of 10X and the associated land purchase. We continue to expect full year capital expenditures of $500 million to $600 million. In addition, during the quarter, we earned another $8 million of prepayments from Apple as we continue to progress towards start of production for them next year. We expect to earn an additional $120 million in prepayments over the next 1 to 2 years as we achieve various magnet and recycling-related milestones. Finally, we ended the quarter with a strong liquidity position of $1.34 billion in cash, cash equivalents and short-term investments on the balance sheet. 
With that, let me turn it over to Michael. 
Michael?

**Michael Rosenthal** (Executives):
Thanks, Ryan. Operationally, it was another solid quarter for both the Materials and Magnetics divisions as we increased production while advancing a number of initiatives designed to improve efficiency, expand capabilities and support future growth. At Mountain Pass, results were generally in line with our expectations. In our upstream operations, concentrate production remained strong despite ongoing pilot testing, investments in future growth and optimization and efforts to better utilize the reserve base. 
Encouragingly, these initiatives are demonstrating the potential to unlock further improvements in operational efficiency and flexibility while sustaining strong production performance. In our midstream operations, performance continued to improve. We delivered our highest quarterly NdPr oxide production to date, in line with our outlook. For portions of the third quarter, we operated at a production rate of over 450 tons per month, providing further confidence in our long-term production objectives. 
Most circuits are performing quite well, and we are seeing the benefits of the equipment upgrades and process enhancements discussed last quarter. During the period, a small number of circuits experienced unplanned maintenance activities and equipment-related interruptions associated with the introduction of new capabilities. As previously indicated, addressing the remaining reliability constraints will be an iterative process over the next several quarters as we add redundancy and implement targeted debottlenecking efforts. Despite these occasional disruptions, overall throughput, reliability and operating consistency continue to trend in the right direction. 
Our midstream expansion initiatives also made important progress during the quarter. Most notably, we began operations in our first heavy rare earth separation circuits designed to separate terbium and dysprosium from the broader medium and heavy rare earth stream. We are pleased with the startup to date with both process and equipment performance meeting the expectations. Commissioning has progressed largely as planned, benefiting from the experience the team has accumulated through years of operating and optimizing our light rare earth separation facilities. 
Since separation circuits are susceptible to unexpected operating challenges and minor upsets can have multi-week impacts, the team has approached the start-up deliberately and methodically. But we have navigated these risks very well and remain on track to begin on-spec production of finished terbium and dysprosium in short order. As a reminder, this circuit is primarily intended to support our downstream Magnetics division and its strategic customers. As we progress towards full production, our focus remains on establishing sustainable production and ensuring product quality. 
The commissioning of terbium and dysprosium separation capability is also producing 2 high-purity intermediate streams that we have the option and ability to precipitate and finish. These are SEG, samarium, europium and gadolinium, as well as a mixture of yttrium and holmium to lutetium. Given the supply chain challenges currently impacting the marketplace, both products are attracting significant customer interest. We are eager to capitalize on these opportunities, particularly because doing so allows us to support the near-term requirements of our strategic long-term customers while benefiting from a uniquely favorable market environment for these materials. 
To support the start-up and accelerate near-term production of our medium and heavy rare earths, we also began a process to prudently reintroduce our SEG+ inventory back into the system. Our broader heavy rare earth expansion strategy continues to advance as well. Samarium and gadolinium projects remain on track for first production in the first half of 2028, processing feed from the SEG intermediate stream referenced above. While current market conditions for a number of medium and heavy rare earth products are unusually strong, we do not believe today's elevated prices will persist indefinitely. 
Many of these remain relatively small markets that have been significantly affected by export restrictions and artificial supply constraints. Nevertheless, we see compelling opportunities to create value through targeted investments, commercial partnerships and long-term offtake arrangements that support the development of a broader market. The gadolinium agreement we announced last quarter is an example of the type of opportunity we are pursuing. Attractive project economics, combined with the ability to bring additional supply to market in relatively short order. 
Importantly, we believe these added capabilities will improve our ability to secure and process third-party feedstocks and increase production volumes over time. The successful start-up of our terbium and dysprosium circuits further strengthens our confidence in pursuing those opportunities. Elsewhere at Mountain Pass, progress continued across several initiatives. Early in Q4, we successfully and safely completed our scheduled maintenance outage, largely on schedule. 
As always, the approximately 10 to 14 days required for de-inventorying, maintenance activities and reinventoring will impact sequential comparisons. However, we expect improvements in sustained production rates and relatively stable year-over-year growth in total NdPr oxide production during Q4. 
Turning to our Magnetics division. Teams at Independence made substantial progress technically, operationally and commercially, culminating in what I believe was a transformative quarter for the business. Attention during the period was focused on increasing strip cast alloy production, expanding throughput across powder processing operations, significantly increasing machining, bonding and finishing capabilities and capacity and achieving higher magnetic performance from existing chemistries. 
As expected, our focus is increasingly shifting from demonstrating production capability and advancing through the qualification process to ramping volumes and improving efficiency. Now that we have established the ability to produce qualified salable magnets at scale, we are accelerating efforts around material handling, process optimization and automation. Over time, these initiatives will drive increased throughput, improved operating leverage and the extraction of additional value from the manufacturing platform. 
We also continue to invest heavily in expanding our technical capabilities. In support of our Apple partnership, 10X and broader market opportunities, our engineering teams are expanding the portfolio of magnet grades and specifications on our product road map. Consistent with what we have discussed in prior quarters, reducing heavy rare earth utilization remains a central focus. Through further advancements in our approach to grain boundary diffusion, improved process control and ongoing materials innovation, we expect to further reduce heavy rare earth intensity across our product portfolio while maintaining performance requirements. We remain encouraged by the progress. 
Finally, development of 10X remains on schedule. Learnings from both Independence and Mountain Pass, together with the hard-earned experience gained executing large-scale projects across the company for much of our history are being incorporated into detailed engineering and commissioning plans. Stepping back, this is another solid quarter across the business. From continued progress in our Materials division to important milestones in magnetics, we are seeing the benefit of years of investment, operational learning and technical development increasingly compounding across the platform. That gives me confidence not only in our ability to finish 2026 strongly, but also in the opportunities ahead as we expand our capabilities, grow production and execute against our long-term objectives. 
With that, I'll hand it back to Jim.

**James Litinsky** (Executives):
Thanks, Michael. This was another outstanding quarter of execution. I'm very proud of the MP team. The progress you hear about each quarter reflects years of difficult work. On our August call, before the recent market stress, I questioned whether the enormous sums flowing into computing infrastructure would earn attractive returns. At the same time, I emphasized that the transformational economic opportunity would emerge as intelligence moved into the physical economy. 
I believe we are living through a second Gilded Age. Like the first, it combines extraordinary technological progress with enormous capital formation, considerable financial speculation and anxiety about the distribution of wealth and the future of work. The railroads transformed America even as many of the companies behind them went bankrupt. Being right about the future then did not guarantee a return. The financing stress emerging in computing infrastructure is a reminder of that distinction. Demand can grow spectacularly while the economics disappoint. 
Capital still has a cost and investors need both a return on it and a return of it. But even as capital markets grow more volatile, the building blocks of the next industrial era are coming into view. Superintelligence is moving into the physical economy. Robots need motors. These motors need high-performance magnets and those magnets require an industrial supply chain that takes years to build. President Trump's recent proclamation on robotics and industrial machinery, together with the FCC's restrictions on foreign-produced advanced robotics devices underscores the national security importance of these supply chains. 
In the competition with China, American leadership will require American production from the robots themselves to the magnets that make them move. For context, the global NdFeB magnet market is roughly 250,000 metric tons a year with well over 90% of production concentrated in China. Precise requirements depend on final design, but at 3 to 5 kilograms of magnets per humanoid, annual production of 50 million robots would create additional demand equivalent to most or all of today's global market. 
That demand would come on top of cars, electronics, factory automation, drones, data centers and defense systems that are already depending on these magnets. A single manufacturer hoping to produce just 1 million humanoids per year without relying on China would need magnet volume equivalent to roughly 40% to 70% of 10X's planned annual capacity. And those existing markets will continue to grow. China is competing to win across all of them and especially in robotics, where its own downstream manufacturers have global ambitions. 
Consider the capital being committed to this opportunity. Venture investors, major technology companies and Chinese competitors are investing billions. Private robotics valuations already reach into the tens of billions of dollars. Those valuations reflect bets on which companies will capture a share of a potentially multitrillion dollar market. The timing and the ultimate winners remain uncertain and near-term expectations may very well disappoint. But put that capital alongside the supply-demand math and the competition with China and one takeaway becomes clear. 
If you believe physical intelligence will transform the world, access to the MP platform could determine which companies get to compete in this multitrillion dollar opportunity. I'm not exactly sure what that is worth, but I believe our current valuation materially understates it. That does not mean that every rare earth or magnetics business will succeed. To the contrary, I expect a very difficult year ahead for parts of the industry. Some projects will stop, some businesses will fail because of capital constraints, inadequate feedstock, flawed M&A or some combination of the 3. 
A compelling demand forecast cannot rescue poor assets or substitute for sound execution and strategy. Our growth is supported by contracted cash flows, committed customers and long-term partnerships across industry and government. That foundation allows us to pursue the robotics opportunity patiently. We do not need the most aggressive forecast to materialize to build an exceptional business. As we deliver on the commitments we have already made, we are building the best and most vertically integrated magnetics company in the world. 
With that, let's open it up for questions. 
Operator?

**Operator** (Operator):
[Operator Instructions] Our first question comes from the line of Brian Lee with Goldman Sachs & Co.

**Brian Lee** (Analysts):
I appreciate all the overview on some of the medium to longer-term opportunities, Jim. But curious on the maybe near- to medium-term opportunity as it stands for you guys on NdPr magnets for the automotive market, particularly GM, your anchor customer. Can you just give us a sense of kind of the general demand backdrop for NdPr magnets in the U.S.? 
I know GM has had sort of this very publicized dispute with another supplier that you might consider a peer of yours. Is that a reflection of the demand for EV applications in the U.S.? Or is there maybe a chance that demand comes to you and you can actually upsize your commitments to GM? Just curious maybe broader backdrop of EV demand for magnets in North America.

**Ryan Corbett** (Executives):
Brian, it's Ryan. Thanks for the question. I won't comment specifically on your specific question there. But I think broadly, what we see from a foundational customer and broadly across the automotive space is continued very strong demand for our products. We remain very enthusiastic and pleased with what we see as the demand backdrop from our foundational customer. And importantly, what we continue to see is with GM being very early in their strategy of localizing, there are many, many more OEMs behind them that are really starting to catch up. 
And so from the perspective of automotive as a percentage of the market, obviously, it's very, very significant. And the demand that we see both directly from OEMs and in addition from Tier 1s and Tier 2s that supply them remains incredibly strong. So I think automotive for us, to the extent we want to continue to invest in that area is absolutely still a big upside opportunity for us.

**Brian Lee** (Analysts):
Okay. Great. That's helpful. And then maybe just one more bigger picture question. I'll pass it on. I know it's early days, but any initial thoughts on kind of critical minerals and the policy response, if any, that the recent midterm election results from this week could impact for the U.S. rare earth sector as well as MP specifically?

**James Litinsky** (Executives):
Brian, sure, it's Jim. I'll take that. Basically, we really see no change. I mean, we're a nonpartisan national security company. Our deal was really driven out of the Pentagon. We operate in red states, blue states, purple states. And we've really had strong bipartisan support since the beginning, and we've obviously been operating in quite a few different government regimes. So we feel very good that there's no change on our front. As far as some of the others, obviously, I wouldn't begin to speculate what might be happening there. But my guess is there'll be certainly be a lot of media and action on that front.

**Operator** (Operator):
Our next question comes from Lawson Winder with Bank of America Securities.

**Lawson Winder** (Analysts):
Nice quarter. And once again, thank you for the update. Ryan, thank you for the guidance that you've provided looking into '27, '28 on the magnet ramp-up. Hear you loud and clear. When you describe 2028 as a year in which the earnings potential of Independence will become clear, would that suggest that Independence will be operating at the design rate of around 3,000 tons per annum?

**Ryan Corbett** (Executives):
Yes. Lawson, we're not going to give specific volume guidance at this point, particularly given the nature of our customer contracts, I think there are 2 that are very high profile and others potentially behind it. And so we won't get into the specifics there. But I think given what we see with our expected ramp-up in production as well as sort of the feathering in of our products into our customers' supply chains, that's when I do think you'll sort of start to see the positive flywheel become very clear from a financial perspective.

**Lawson Winder** (Analysts):
Okay. And then looking at it from another angle, and that would be just of commercial production. So '26 year-to-date has had some material start-up costs. You'll start recognizing those in COGS once you hit commercial production. So considering the ramp-up in 2027 that you described for Independence, what would you expect commercial production to look like in terms of when it will be achieved? And then how will you actually define what commercial production looks like?

**Ryan Corbett** (Executives):
Yes, Lawson, it's a great question. As we mentioned, we will begin shipments of salable products this quarter in Q4. That will involve a continued ramp-up to what we view as sort of a more normalized volume level. And some of that will depend, as I mentioned, on how our parts find their way into the specific programs and specific plants of our foundational customer. 
And then, of course, very quickly behind that, in 2027, we have the start-up of production of Apple. And so taking that all into account, I would expect us to continue to see from a start-up cost perspective, continued costs in that category for at least the first half of next year, and then that will start to taper off as we get into higher volume production.

**Operator** (Operator):
Our next question comes from Neal Dingmann with William Blair.

**Neal Dingmann** (Analysts):
My question is a bit on what you just touched on, and that's really around your numerous offtake agreements and price floors. Specifically, Jim, are there any part -- I assume not, but I figured I would ask, are there any parts of your contracts or floors able to be reexamined or restructured potentially by the new representatives?

**James Litinsky** (Executives):
No, we have a binding contract.

**Neal Dingmann** (Analysts):
That's what I thought. All right. That's simple enough. And then secondly, just can you remind me just maybe the 10X, you keep advancing. I love to hear the progress of that. Could you talk a bit about how conversations around this, maybe such as price structure has changed in recent months, which to me, given seems to be a very strong pricing sort of environment despite the volatility seen in the group. So just wondering if your contracts continue to advance as you expect them to?

**James Litinsky** (Executives):
Sure. I mean, I think what -- it's a great question. What's really interesting on this front is I think if we look back historically over the last year or so, you may have heard me say that our expectation is multiples of demand for 10X and just given the growth in all of the growth vehicles and the onshoring. And interestingly, what I would say, is in recent months, really in this quarter, I think it started to accelerate. We have seen actually specific, what I would call, RFQs or specific customer sizings that well exceed the 10X capacity that we are bringing online now. 
And so I think what was sort of theoretical has become specific. And what I would remind you is that our 10X, as we know, is 100% contracted. We can bring that online in '28, and we can be thoughtful about how we ramp, how we contract. We don't have any sort of financial gun to our head, so to speak. And so what that really enables us to do is focus on what we believe are going to be materially higher margin opportunities. 
And as I referenced in the script, and I try to be thoughtful about the words that I put out there, Neal. But we do believe that we will be somewhat of a kingmaker in some of these new multitrillion dollar opportunities. If you look at our platform, we're going to be able to enable a company or companies to be a number of years ahead of competitors. And so it's a very unique position that we're in. And obviously, we're going to make sure that our shareholders are rewarded for that strategic value.

**Operator** (Operator):
Our next question comes from Max Yerrill with BMO Capital Markets.

**Max Yerrill** (Analysts):
I'm sure at this date, you've tested many different magnet formulations to finish the qualification process with GM. But just wondering if during this process, how your views have changed on the market or supply and demand balance for NdPr or some of the other rare earth elements?

**James Litinsky** (Executives):
Well, I mean, kind of referencing back to my prior answer, what I would say, and we've said this for a couple of quarters now, but we have dramatically lowered the heavy needs to hit grade on automotive magnets. So we really believe that we've created a lot of IP value on that front. And then when you move to some of the other categories, which we believe are going to be materially higher margin, higher growth, our expectation is that when 10X comes online that we're going to need likely no. I mean, maybe we'll have certain verticals where we'll have a little bit. 
But we believe that we could -- from what we're seeing today, we believe we could fit more than the supply of 10X with 0 heavy formulations. And so again, I go back to what you've heard me say for a quarter or 2 now, which is NdPr is the binding constraint. We do not believe that for the major growth and margin opportunity that you're going to see ahead that heavies are going to be a factor. And frankly, we are creating that reality with the extraordinary IP advancements that our team are making at Independence today.

**Max Yerrill** (Analysts):
And then maybe a follow-up on that. Do you see the GBD and the advancements in drifting out some of the heavies? Could that get to a point where you could start to see more of heavy rare earth sales to third parties like we saw in this quarter?

**Ryan Corbett** (Executives):
Yes, I can take that. I think at this point, Max, it's Ryan. Our focus is ensuring that we have security of supply for our existing customers in the magnetics business. But there is absolutely a world where you take what Jim said and we look at some of the performance applications that we have right now that do demand heavy rare earths through GBD where we may not need them. And that's actually much closer to reality today than I even thought 3 months ago. And so there is a world where that becomes a reality from a dysprosium and terbium perspective. 
Certainly, what you've seen us do is be thoughtful on the other heavy rare earth markets where there are a wide variety of needs, particularly the gadolinium announcement that we made last quarter. And so I think that the sale that you saw this quarter in a lot of ways is emblematic of the embedded value that we have on our balance sheet right now that I don't think is being properly understood. And it's not just heavy rare earth concentrate and it's not, frankly, including light rare earth concentrate that we have on the balance sheet that's worth hundreds of millions of dollars of potential value, same with the heavy rare earth concentrate. 
And I think that the results that you saw this quarter, while the sale of SEG+ in particular, is a bit of a one-off to support a strategic customer, if you think about the margin potential of the products that we are going to bring to market shortly, I think it speaks to the value -- the incremental value we'll be able to create out of Mountain Pass and why we've been investing so thoughtfully in this heavy rare earth capability.

**Operator** (Operator):
Our next question comes from Carlos De Alba with MS.

**James Litinsky** (Executives):
Carlos. You there?

**Carlos de Alba** (Analysts):
Yes, sorry. Can you hear me?

**James Litinsky** (Executives):
Yes, go ahead.

**Carlos de Alba** (Analysts):
So the question is on -- given how the share has performed recently, are you considering maybe some share buybacks as you did a great program in 2024. And look, I know that you're growing, you're investing, but also there might be value -- there is value at these levels in your share price. So I wanted to get your thoughts there.

**James Litinsky** (Executives):
Yes. Sure. It's a great question. Obviously, we're very surprised. There's a lot of -- as I referenced in the opening remarks, there's a lot of currents going on in this market, I think, that are in general, unrelated to us. I think you're seeing, if I had to guess, a lot of pods and tax arbitrage strategies pressuring certain sectors, ours being one of them. And so you really have sort of these macro level quantitative things that are hitting our sector connected to some others. 
What I would say is I think what differentiates us is that we have contracted cash flows and then obviously, we have this material upside strategic value given the niche that we're in. And if you -- I think we sort of seem to be correlated with some peers that need to raise enormous amounts of capital that don't have balance sheets that are commensurate with survival, that don't necessarily have assets that even if they had the time that represent sort of the value. And so I think there's sort of this overall macro downdraft on the sector. And obviously, then there's some political considerations that may be happening with some of the others. 
And so I don't think that, that reflects on us. I think if you look, all we have to do, and we don't take this lightly, but all we have to do is execute and our cash flows, you can do the math on that and the upside. And so we do believe that there's -- as I said, there's material upside. But I think what's really important is that we have to make sure that we maintain our fortress balance sheet to continue so that we have the runway to be opportunistic through. And although I feel really great about our strategic positioning, our business, our ability to execute, the niche that we're in, I will say, and I think probably -- again, my remarks probably referenced this, but I do expect the sort of the months and year ahead are going to be significantly challenging financially. 
There's a lot of disarray in the market right now. It would not surprise me if we see some of the credit issues to continue to play out across private credit and maybe the insurance industry that's loaded up with a lot of that. I think there's an entire rethinking around the returns on capital happening. And I think there's -- for those of us who've been in the markets a long time, these things are never sort of up and to the right. And so it would not surprise me to see a real sort of global macro financial setback. 
And so I would say for most of this quarter or 2, internally at MP, we've been very focused on that as a possibility. We've said it on the calls, and so we've been kind of batten down the hatches, making sure that we're being really thoughtful about every dollar that we spend and also as we look at opportunities out there, not being wasteful with capital because I think there's going to be some excellent opportunities for us to, for lack of a better analogy, kind of clean up the garbage, so to speak, in the time ahead. 
That's a long-winded way of kind of laying out my perspective on the environment right now. And then obviously, lastly, with respect to specific capital actions, as you know, we never telegraph these things. We will obviously do things and then tell you. But hopefully, you can expect us to continue to be opportunistic as we have been.

**Carlos de Alba** (Analysts):
I appreciate that. And then just exploring a little bit more on the SEG+ sale that you had. What was the cost associated with that revenue, if you can share that? But also maybe more importantly, did you deliver those tons or perhaps you sold them, you monetize them or you will monetize them, but you are going to use them to produce magnet for that customer down the road?

**Ryan Corbett** (Executives):
Yes. Carlos, it's Ryan. We're not going to get into the contract specifics. I think you'll probably be able to deduce from our filings that this was a sale to an existing strategic customer of ours. I would note that this product has been sold. We have no intention of -- or ability to reuse it. This is a use case that is not focused on magnets. And so I think, again, it sort of speaks to the broader opportunity set of the heavy rare earth business that we're building. 
Obviously, at this point, as we're entering production of the initial set of separated heavy rare earths that the team is working on and then expanding into gadolinium and samarium. And I think we've made clear that there are probably some further opportunities of other separated heavies for us to look at. This is sort of an early sign of the potential of that business.

**Operator** (Operator):
[Operator Instructions] Our next question comes from Corinne Blanchard with Deutsche Bank.

**Corinne Blanchard** (Analysts):
I think actually, most of my questions have been asked and answered, but maybe we can touch on -- maybe a little bit of recycling. Any update you can share here? And then maybe the second question would be on the Project Swarm that you announced a few months ago. Like is there any update there that we could be expecting maybe for next year or like in the coming months?

**Michael Rosenthal** (Executives):
Corinne, it's Michael. Related to recycling, good progress at both of our sites. So engineering is moving along at Mountain Pass and construction is underway. All long lead equipment has been procured. On the actual magnet production side from recycled materials, equipment is starting to be delivered and installed. Our teams are working closely with our customer on developing the magnet grades and prototypes and specifications to start deliveries next year. So it's been a great collaboration so far, and we're very excited about it.

**James Litinsky** (Executives):
And then, Corinne, on Swarm, given that that's defense supply chain, we'll try to be delicate and thoughtful here. But what I would say is that the reception has been overwhelming. It's great to see. I think that -- just to give some background, the purpose of Swarm is when we looked across, obviously, drones being the future of warfare. When we looked across the American defense supply chain, what we were finding is that many of the producers would have magnet specs where they didn't even really know why they had those specs. They were buying motors out of China, whether it was through another location or not. 
And so what we view our role here is to help standardize the domestic industry on specific grade and work with some of the downstream producers to help them do what they do best and make sure that they have the supply chain available to them so that they don't need to think about procuring or spending capital on getting capacity that they may or may not never -- may or may not need. And so I think we're serving a really important role in the defense supply chain for the country on this front, and the reception has been outstanding, and we're happy to do it. And so I doubt we'll give you much many updates beyond that, but that's the general gist of it.

**Corinne Blanchard** (Analysts):
Great. And maybe if I can squeeze actually one more. I think you spent a few minutes, actually probably a little bit more time than you usually do on robotics and how much you could really tilt the demand balance there? I'm actually wondering if some of your customer conversations are already going to that direction? Do you already have some customers approaching you for your magnets for robotics purposes? And maybe just more strategic view here, do you have a preference? Do you see a difference in terms of strategy for maybe in terms of pricing, defense versus robotics? Or are you pretty much agnostic?

**James Litinsky** (Executives):
Yes. So it's a great question. And that was what was in my head when I earlier in the call when I referenced sort of the theoretical becoming the real, Corinne. We're having conversations with the names you would think and know. And there's obviously a lot of those names and then there's sort of some world-class global big tech and other types of companies that are getting into the space. And what we're seeing across the board is an enormous amount of investment and focus and recognition that this is sort of the cutting-edge landscape of economic opportunity as superintelligence moves into the physical world. 
And so we're having those conversations. And in fact, if you look last night, the Chinese government blocked SoftBank's acquisition of ABB, that robotics business. And so I know, obviously, we're all in this country distracted with a lot of politics this week, but we can't forget that there's global competition going on out there, and this supply chain is absolutely critical. And so we are seeing -- it is getting more specific. 
And to your question on the business, that's why I referenced, I do believe that because we have a very unique platform that we -- this is going to be very high-margin business for us. And we have the balance sheet, the structural -- contracted structural benefit for 10X to be thoughtful about how we think about bringing online that factory for this sector and others. And so we do expect it to be really economically attractive, and we will be patient and thoughtful about it, but we're really encouraged by what we're seeing.

**Operator** (Operator):
Our next question comes from Bill Peterson with JPMorgan.

**James Litinsky** (Executives):
Bill. You there?

**William Peterson** (Analysts):
Yes, sorry. Can you hear me now?

**James Litinsky** (Executives):
Yes.

**William Peterson** (Analysts):
Great. Sorry about that. I want to actually ask about NdPr production and basically how we should think about the ramp into next year, taking into consideration any -- if there's any downtime that you typically have. Effectively, when should we reach nameplate capacity, but also thinking about what can drive it beyond nameplate, whether it be further efficiency or incremental investments? And then maybe speak to how the -- on the cost side, how -- when you might reach normalized cost and how the chlor-alkali facility could impact that?

**Michael Rosenthal** (Executives):
Great. Thanks, Bill. It's Michael. I'll start and turn it to Ryan. As I mentioned in my remarks, for a portion of the third quarter, we were able to run at over 450 tons per month run rate. And so I think that sort of cements in my mind, our ability to hit that kind of targeted run rate with our existing assets. And we still have some optimization and debottlenecking to do in order to sustain that for a full month or quarter. But it's clear that we can. And I would expect over the next several quarters, we will get to that point where we're able to do so. 
As of -- in terms of 2027, we have a number of projects commissioning next year, in particular, the chlor-alkali facility, where we'll start the first phase of that in the first quarter or so. This is a really important project for us that increases resilience, hopefully lowers cost structure, improves our environmental footprint, reduces reliance on third parties and some kind of pipe chemical reagents that represent a very significant portion of our cost structure. 
So bringing that online will be a significant endeavor and have significant implications for our overall site infrastructure. So we would expect from that as well as recycling some of the additional heavy rare earth investments to have some additional downtime next year, and that's incorporated into our expectations already. But we would expect to operate at sort of over 5,000 tons per annum production rate for the year.

**Ryan Corbett** (Executives):
To hit your question on cost structure, I think all the things that Michael just laid out, I mean, you kind of answered my portion of the question, too. The reality is that once we are through some of these debottlenecking initiatives, keep in mind that debottlenecking isn't free and neither is the start-up of chlor-alkali and heavies. And so I think 2027, particularly as we get to the back half of the year when we've got our initial train of chlor-alkali online, we've made progress on heavies, and we're consistently producing on a normalized basis at that 500 ton a month production level, that is when you will really start to see the leverage in the cost structure. 
I think that in some ways, we're starting to see it now as well. If you think about the scale of Mountain Pass and the fact that NdPr has been really the only revenue product absorbing the vast, vast, vast majority of all shared infrastructure, and we'll be at the point where we have dysprosium and terbium, we have other heavy rare earth products that will share in some of that shared infrastructure costs, you really look at the full true NdPr production cost with all of these optimizations and growth in throughput that we expect, I'm extremely confident in our ability to continue to drive down the cost structure.

**William Peterson** (Analysts):
Yes. I wanted to ask a question on the magnet ramp a little bit differently than some of the prior questions. First of all, congrats on the qualification. But I guess when we think about the path to the sort of nameplate 1,000 tons for your lead customer and then layer on top of that the next tranche for the second customer. 
I guess, my question is, is this gated by your own output or ability or yield or the demand cadence from these customers? And if it's the former, I guess, what areas are you looking to debottleneck or work to improve yields? Or -- and then if it's the latter and you have the capacity, are there ways to ship these magnets to other -- is there demand basically from other players that can absorb the capacity?

**Ryan Corbett** (Executives):
Yes, sure. I can start on that. I think the way to think about this is that magnets are highly customized engineered products. And our focus is ensuring that we are ready to meet the demand of our foundational customers as we continue to get placed into the specific programs and plants that we are targeted to be, which is not an overnight process. And so we are focused on ensuring that each of the areas of the plant are reaching sort of the throughputs that are necessary to meet a forecast that we are planning to, we have visibility, of course, into these various programs and various additions to the plants. 
And so it's not one or the other. It's really feathering into the automotive supply chain is a relatively complex process. And then at the same time, there is significant expansion ongoing at Independence to support our next major customer there. And so the focus really is on executing for the 2 of them, first and foremost, getting those programs well ramped and well optimized and then taking further opportunities as they come.

**James Litinsky** (Executives):
Yes. And I would just reiterate, as we bring online our foundational customer and then Apple next year, from a risk management standpoint, we are fully focused on those 2 customers, they are critical. And we want to get that right for them. And so I think we have been methodical about how we've built this business. If we wanted to sign a bunch of business and just sort of take a lot of stuff that comes, we could certainly do that. That has not been our philosophy. So it is fully about executing properly, thoughtfully. And then obviously, as 10X comes online, we'll do the same thing.

**Operator** (Operator):
Our next question comes from Ben Kallo with Baird.

**Ben Kallo** (Analysts):
Maybe just on heavy, and I know you guys talked about this a bit. You talked, Jim, about having heavies on site. And I also understand that you're going to use less heavy, but I'm just wondering how much of Independence you're covered for with what's in inventory? And then just on your own production, if you could just talk about how we can think about that in terms of ramp and potential revenue contribution going forward?

**Ryan Corbett** (Executives):
Ben, it's Ryan. On that front, what we've consistently said is, for Independence, where obviously, we're starting out production with EV traction motor magnets and then expanding into other products with our next customer set. We believe that we are fully covered for everything that we need at Independence from just the production from our own ore body. And obviously, we've also talked about the fact that the heavy rare earth separation facility is designed to take in third-party feedstocks where we are actively in the market sourcing those as we speak. 
And so from that perspective, we remain very, very confident. As it relates to 10X, I think we've talked about in the past as well that we have a partnership with the Department of War on that front that protects us there, and that's made excellent progress.

**Ben Kallo** (Analysts):
Just following up on the heavy production at Mountain Pass, how we think about that just in terms of any kind of revenue contribution?

**Ryan Corbett** (Executives):
I think, Ben, what you will see is given the fact that for the foreseeable future, we will be using those products internally is, in the early days, it will be intercompany revenue that gets eliminated in consolidation. And then ultimately, we will recognize the revenue for the heavies that make their way into magnets through the magnetics business over time. There also is a consideration of, in early production at Mountain Pass, I think we've been very thoughtful in positioning our inventory of heavy rare earths for magnets. 
And so there may be a period of time where we are producing for our own inventory before that finds its way into a magnet and gets sold. And so we aren't really guiding to specific dysprosium, terbium revenue numbers at this point. And as we have more to update you on, we will. I think what you will start to see is, I think Michael made mention in his prepared remarks of the fact that we will make some interesting intermediate product streams that will come off of the heavy separation process ahead of us going into finished samarium oxide and gadolinium oxide production. Those are potential very significant margin opportunities for us. 
Again, we're not giving a ton of specifics there at the moment, but it is, I think, a very significant opportunity for the Materials segment. And then, of course, we've talked about 2028 being the time frame where our gadolinium contract comes online, and we're looking at other opportunities as well.

**Operator** (Operator):
Our last question comes from Richard Garchitorena of Barclays.

**Martin Sheehan** (Executives):
Richard, make sure you unmute. We can't hear you. You there?

**Richard Garchitorena** (Analysts):
Sorry, can you hear me now?

**Martin Sheehan** (Executives):
Yes.

**James Litinsky** (Executives):
Yes.

**Richard Garchitorena** (Analysts):
Oh, I lost you again.

**James Litinsky** (Executives):
I'm sorry, Richard. You're breaking up. Try again.

**Richard Garchitorena** (Analysts):
Can you hear me now?

**James Litinsky** (Executives):
Yes.

**Richard Garchitorena** (Analysts):
Okay. Let's try this last time. Just curious, as you went through the qualification process, was there anything that surprised you? And were there any best practices, I think, that you may have taken away that can help improve the process, whether it's procurement, whether it's how do you basically set up the lines that -- where we could see incremental improvements in margin and optimization as you move ramping up in 2027?

**Ryan Corbett** (Executives):
Yes, Richard, it's Ryan. It's a great question. And the answer is absolutely yes. And I think that this is one of the great facets of the partnership that we have with General Motors. We decided to enter the magnet business and start with automotive for multiple reasons. Obviously, it's a significant portion of the market, but it happens to be one of the toughest from a technical perspective and absolutely the hardest from a quality perspective. 
When we talk about qualification, it is not about, do you make a product to our spec? Does it just meet performance specifications? It is down to every piece of equipment, how do you run it? What are the standard work instructions that are present? What are the safety attributes of it? How does material flow on the floor? It is incredibly thorough. And so I would probably give another plug to our magnetics team for how hard they have worked in pushing this process forward and frankly, to the General Motors team for how thorough and helpful they've been having started this business from scratch in 2021 to get to this point is something that I think this entire team is incredibly proud of. And so it has absolutely made us better, and we have a lot more to do.

**Operator** (Operator):
That concludes the question-and-answer portion of today's call. I'll now hand the call back to Mr. Litinsky for closing remarks.

**James Litinsky** (Executives):
All right. Well, thank you, everyone. It was an outstanding quarter. And obviously, there is a lot of interesting currents and chaos out there. And so we wish everyone well and look forward to seeing you again next quarter.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MP_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Michael Rosenthal｜guidance：Q3 NdPr 產量預期超過 1,000 公噸（原話："I expect Q3 NdPr production to exceed 1,000"）
- 2026-08-06｜Ryan Corbett｜guidance：Q3 NdPr 氧化物實現價格預期在每公斤 90 多元高段，PPA 收入約每公斤 10 元（原話："will be in the high 90s per kilogram, leaving PPA income"）
- 2026-08-06｜Ryan Corbett｜guidance：Q3 材料部門銷量預期持平（原話："sales volumes in the Materials segment to be flattish"）
- 2026-08-06｜Ryan Corbett｜guidance：全年 CapEx 預期維持 5 到 6 億美元（原話："CapEx spend to be in the $500 million to $600 million range."）
- 2026-08-06｜Ryan Corbett｜guidance：上半年累計 CapEx 為 3.08 億美元（原話："year-to-date spend to $308 million as of June 30."）
- 2026-08-06｜James Litinsky｜guidance：磁鐵商業出貨預計在第四季開始，之後穩定爬坡（原話："expect to begin commercial shipments in the fourth quarter"）
- 2026-08-06｜Ryan Corbett｜guidance：磁鐵銷量為小幅爬坡，且不會線性（原話："There'll be a modest ramp of volume over time."）
- 2026-08-06｜Ryan Corbett｜guidance：預付款約 4,600 萬美元的前驅物營收將在未來 3 到 4 季認列（原話："$46 million of prepaid revenue to be earned for magnetic"）
- 2026-08-06｜James Litinsky｜margin：材料部門營收加 PPA 收入 1.132 億美元、調整後 EBITDA 3,250 萬美元（原話："$113.2 million of revenue plus PPA income and $32.5 million"）
- 2026-08-06｜Ryan Corbett｜margin：合併營收加 PPA 收入 1.261 億美元（原話："$126.1 million of revenue and PPA income, more than doubling"）
- 2026-08-06｜James Litinsky｜margin：前驅物產品調整後 EBITDA 利潤率超過 40%（原話："Precursor production generated adjusted EBITDA margins"）
- 2026-08-06｜Ryan Corbett｜margin：磁鐵部門營收小降，因成本更多歸入磁鐵量產起步而非前驅物（原話："much higher proportion of costs being attributable to the"）
- 2026-08-06｜Ryan Corbett｜margin：降成本的前提是穩定在目標產量運轉（固定成本攤提）（原話："we need to be operating consistently at our target"）
- 2026-08-06｜Ryan Corbett｜margin：氯鹼等降本效益預計到 2027 年逐步堆疊（原話："we expect those benefits to build progressively through '27"）
- 2026-08-06｜Michael Rosenthal｜margin：新試劑直接成本略高於舊產品，管理層認為整體效益較大（原話："The direct cost of the reagent is somewhat higher than our"）
- 2026-08-06｜Michael Rosenthal｜commitment：Dy/Tb 分離線預計今年稍後產出鋱與鏑（原話："we remain on track to produce terbium and dysprosium"）
- 2026-08-06｜Michael Rosenthal｜commitment：釤計畫預計 2028 年首度生產（原話："planning first production in 2028."）
- 2026-08-06｜Michael Rosenthal｜commitment：預浮選製程預計 2028 年前規模化導入（原話："pre-flot process that we now anticipate implementing"）
- 2026-08-06｜Ryan Corbett｜commitment：不急於為宣布而宣布合約，只在準備好時才公布（原話："We are in no rush to announce a deal to announce a deal."）
- 2026-08-06｜James Litinsky｜customer：7 月簽下對美國航太國防廠商的釓氧化物長約，預期多年累計 9 位數美元（原話："9-figure deal in total over multiple years"）
- 2026-08-06｜Ryan Corbett｜customer：釓合約經濟條件已鎖定，不受現貨價影響（原話："we've locked in economics on this contract."）
- 2026-08-06｜James Litinsky｜customer：Independence 已被 GM 與 Apple 訂滿，可能再塞一兩家客戶（原話："sold out between GM and Apple, it's possible that we'll"）
- 2026-08-06｜James Litinsky｜customer：10X 目前 100% 由戰爭部合約涵蓋，之後預期多數轉給產業客戶（原話："is 100% contracted with the Department of War."）
- 2026-08-06｜James Litinsky｜customer：Project Swarm 用來彙整並標準化未來無人機磁鐵需求（原話："initiative designed to aggregate and standardize future"）
- 2026-08-06｜Michael Rosenthal｜product：持續降低產品的重稀土用量（原話："aggregate and standardize future magnet demand"）
- 2026-08-06｜James Litinsky｜product：預期 10X 開出時大多數產能為無重稀土或極少重稀土的磁鐵（原話："the vast majority of that facility will be no"）
- 2026-08-06｜James Litinsky｜competition：管理層稱 NdPr 是可預見未來的限制性資源（原話："But I remain convicted in the view that NdPr is the"）
- 2026-08-06｜James Litinsky｜competition：管理層描述目前為「管制性稀缺」體制（中國出口管制）（原話："And we are in a regime right now of controlled scarcity."）
- 2026-08-06｜Ryan Corbett｜risk：中國出口禁令對試劑與成本預期影響極小（原話："we expect minimal impact given everything you know about us"）
- 2026-08-06｜Michael Rosenthal｜risk：Mountain Pass 停機被與計畫無關的專案延長（原話："Unrelated projects extended the downtime"）
- 2026-08-06｜Ryan Corbett｜capital_allocation：現金 14.5 億美元，稱可完全支應長期資本計畫（原話："This fully funds our long-term capital plan and"）
- 2026-08-06｜Michael Rosenthal｜capital_allocation：回收業務目前主力為自家製程廢料與 Apple，規模依市況擴張（原話："but we are looking at scaling that business in line"）

### 問答異常語氣（迴避／改口／保留）
- MP_Q2_2026_Earnings_Call_20260806.md｜問：Garchitorena 問下半年成本能改善多少、Dy/Tb 調機是否增加成本｜答法：未給下半年數字，改談存貨資本化與成本效益到 2027 年逐步出現
- MP_Q2_2026_Earnings_Call_20260806.md｜問：Peterson 要求 GBD/低重稀土磁鐵與傳統磁鐵的績效數據｜答法：未提供比較數據，只說符合並超過客戶規格
- MP_Q2_2026_Earnings_Call_20260806.md｜問：Summerville 問 2027 磁鐵爬坡到 1,000 噸/年的節奏與下半年磁鐵營收/EBITDA 組成｜答法：只說會不規則、非線性，2027 節奏留待年底再說，未給數字
- MP_Q2_2026_Earnings_Call_20260806.md｜問：Ma 問為何磁鐵新合約沒有加速｜答法：質疑問題前提，改稱已訂滿且不急於簽約
- MP_Q2_2026_Earnings_Call_20260806.md｜問：de Alba 問 GM 資格驗證的早期回饋｜答法：只談驗證流程，說結果「極鼓舞」，未給 GM 具體反饋

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
{"date":"20260525","verdict":"觀望偏進場","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"NdPr 商品價格維持 $110+ 且 DOD floor 可信（最關鍵的結構性假設）","columns":{"2Y 驗證點":"2026-2027 NdPr 季均價 ≥ $110","5Y 驗證點":"2028-2030 五年均價 ≥ $115（不含 floor 補貼）","10Y 驗證點":"2035 全球 ex-China 供給達 30% market share，價格可獨立形成","具體數字門檻":"NdPr ≥ $110/kg（CRU + Argus weekly）+ DOD floor 撥款 trigger（Pentagon FY 預算 line item ≥ $200M for MP offtake）","信息來源":"CRU Group / Argus Media / DOD FY2026 budget","漂移觸發條件":"連 2 季 TTM 均價偏離"}},{"id":"H2","text":"10X facility 按時 ramp + Magnetics 段 GM 轉正（成長兌現的操作性假設）","columns":{"2Y 驗證點":"2027 末 Magnetics 段年化營收 ≥ $200M，GM 由負轉 0","5Y 驗證點":"2030 達 10,000 MT 磁鐵年產能、Magnetics GM ≥ 20%（規模經濟）","10Y 驗證點":"2035 magnetics segment 達 50% 公司 OI","具體數字門檻":"季度報出 magnet 出貨量（MT/quarter）+ Magnetics revenue/MT 單價","信息來源":"MP 季報 + 8-K 公告","漂移觸發條件":"連 2 季 magnet 出貨量"}},{"id":"H3","text":"估值倍數收斂至成長股區間（normalized PE 35x）（估值修復的市場假設）","columns":{"2Y 驗證點":"FY 2027 EPS 共識穩定 ≥ $1.10，Forward PE 收斂至 50-55x","5Y 驗證點":"FY 2030 EPS ≥ $2.50，PE 收斂至 30-35x","10Y 驗證點":"FY 2035 EPS ≥ $4，PE 25-30x","具體數字門檻":"EPS 共識穩定（90d trend 標準差","信息來源":"yfinance EPS estimate + analyst rating distribution","漂移觸發條件":"FY 2027 EPS 共識 90d trend 連 2 季下修 > 15% → 削弱；連 4 季下修 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"NdPr spot 連續走弱（China 反向補貼出口或全球需求疲軟）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期","監測指標":"NdPr 月均價（CRU/Argus）+ China REE 出口量","警戒閾值":"連 2 月均價"}},{"id":"R2","text":"10X facility ramp 失敗（成本超支或良率不達標）","columns":{"對應假設":"H2","時間尺度":"🔥 中期","監測指標":"季度 magnet shipment + Magnetics 段 GM","警戒閾值":"連 4 季 magnet 出貨量"}},{"id":"R3","text":"政治結構變化（2028 大選後 DOD 預算重排或中美和解）","columns":{"對應假設":"H1+H3","時間尺度":"🐢 長期","監測指標":"DOD FY 預算 line item for MP + 中美關係溫度（CSIS / RAND 評估）","警戒閾值":"2028-2029 DOD MP 撥款"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":64.46,"archetype":null,"cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名中除程式欄以外的每一個**（程式稍後才會算的 p_bull_pct／p_bear_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；`asym_ratio`／`ev5y_pct`／`irr_base_pct`／`bull_5y_price`／`bear_5y_price` 的漂移歸因同樣由程式生成條目（程式用本次情境、依先換情境後換股價的順序拆量），你不要為它們開條目；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

**給讀者看的文字欄不准出現內部代號**：`thesis.H[]`／`thesis.R[]` 的各欄（信息來源／漂移觸發條件等）、`triggers[].text`、`counter_evidence.contradictions[]` 各欄、`answers.*.verdict`／`answers.*.reasoning` 這類文字，一律不得出現事實表 id（`f_` 開頭，如 `f_consensus_rev_3m_fy1_pct`）或軸／finding id（`軸名#n`，如 `competitive_share_entrants#0`）——這些是程式內部代號，不是給讀者的話。要引用哪個事實或哪個軸，寫進對應的 `fact_refs[]`／`evidence_refs[]` 陣列，文字欄本身只寫人話。

---

## 尾段：scenario_inputs 形狀與回覆格式

**本檔 FY1 共識 EPS ≤ 0（虧損），程式已把估值口徑定為 `sales_multiple`：情境樹用營收路徑 × 終端 EV/S，不用 EPS × 本益比。** 口徑由程式決定，你填什麼 `valuation_basis` 都會被覆寫。`scenario_inputs` 的鍵名與形狀必須完全照下面這份（不得增刪改名；程式據此產生 `dd_scenario.py` 的輸入檔，寫錯鍵名就是整段判斷失效）：

```json
{
  "valuation_basis": "sales_multiple",
  "terminal_label": "FY20XXE",
  "start": {"rev": <FY+1 共識營收，百萬，報告幣別；抄事實表 f_rev_consensus_fy1_m>, "ev_s": <目前 EV/S（EV÷FY+1 共識營收）；抄事實表 f_ev_s_fwd>, "basis": "<起點口徑一句話：營收取哪一年、EV/S 的分母是哪一年，須與終端 EV/S 分母同口徑>"},
  "rev": {"bull": [<Y1>, <Y2>, <Y3>, <Y4>, <Y5>], "base": [五個數], "bear": [五個數]},
  "ev_s": {"bull": <終端 EV/S>, "base": <倍數>, "bear": <倍數>},
  "net_debt_y5": {"bull": <終端年淨負債，百萬，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "shares_y5": {"bull": <終端年稀釋股數，百萬股，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "p": {"bull": <機率整數>, "base": <整數>, "bear": <整數>},
  "yield_pct": {"dividend": <股息殖利率 %>, "net_buyback": <淨回購殖利率 %>},
  "max_dd": {"lo": <負數 %>, "hi": <負數 %>, "basis": "<範圍怎麼推出來的，見判斷卡③情境樹假設段>", "trigger_time": null},
  "basis": {"bull": "<這支路徑的假設一句>", "base": "…", "bear": "…"},
  "endo_ceiling_exceeded": <true|false，共識 CAGR 是否超過 §5.R 內生天花板>
}
```

（**不要**填 `eps`、`pe`、`second_stage`、`peer_max_fpe`；`eps_meta` 仍照常寫共識三年 EPS。現價、目前淨負債（`f_net_debt_m`）、目前股數（`f_shares_diluted_m`）由程式從事實表帶進 `scenario.json`。）

**終端每股價＝max(0, (終端營收 × 終端 EV/S − 終端淨負債) ÷ 終端股數)**，股權價值為負就是 0（Bear 情境債務吃光股權時，要如實寫出讓它歸零，不要為了好看調高倍數）。`net_debt_y5` 要反映該情境下的現金流與融資（虧損公司的淨負債通常會變大，不是沿用目前值）；`shares_y5` 要反映該情境下的增資與稀釋；兩者填 null 才是沿用目前值，不是預設答案。`ev_s` 是終端年 EV ÷ 終端年營收，須與 `start.ev_s` 同口徑（前瞻 vs trailing 不可混）。

`dd_scenario.py` 會擋：`rev` 各路徑長度 ≠ 5、終端營收非 Bear＜Base＜Bull、三機率加總 ≠ 100、`p.bear` ＜ 20、`endo_ceiling_exceeded=true` 且 `p.bear` ＜ 30、`p.base` ＞ 50。另有機械閘：Bull 前兩年營收不得與 Base 相同（情境退化）、`|max_dd.lo|` 不得小於任一情境終點跌幅。機率與路徑是你的判斷，算術（IRR／倍數貢獻／AR）全由腳本算，不要自己填結果欄。

**回覆全文即 `judgment.json` 內容**：緊湊 JSON（`json.dumps(obj, separators=(",", ":"))` 等效格式），陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）。不寫 `scenario.json`（程式從 `scenario_inputs` 產生）。不填不歸你的欄（`decision_inputs` 的機械欄、`reasoning`／`plain` 頂層、`moat.spread_table`／`competitors`、`contradictions`／`triggers` 等舊形狀頂層欄）——填了機械閘會擋。`decision_inputs.asym_ratio`／`irr_base_pct`／`ev5y_pct` 一律填 `null`，由腳本從 scenario 機械算回。

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MP_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
