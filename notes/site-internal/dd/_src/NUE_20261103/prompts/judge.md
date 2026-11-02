你是 stock-analyst **v20 判斷 agent**，標的 NUE（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"NUE","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NUE_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NUE_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_net_sales","label":"營收（GAAP net sales）","value":11249,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","unit":"USD百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","citation":"Nucor Q3 2026 新聞稿（IR q4cdn，2026-10-26）https://s202.q4cdn.com/531038915/files/doc_news/Nucor-Reports-Results-for-the-Third-Quarter-of-2026-2026.pdf"},"note":"查無可驗證共識（未填）"},{"id":"f_kpi2_non_gaap_nucor_q3","label":"Non-GAAP 營業利益率（Nucor 無營業利益科目；以稅前盈餘＋淨利息推算，Q3 無調整項）","value":16.7,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","citation":"Nucor Q3 2026 新聞稿（IR q4cdn，2026-10-26）https://s202.q4cdn.com/531038915/files/doc_news/Nucor-Reports-Results-for-the-Third-Quarter-of-2026-2026.pdf"},"note":"查無共識"},{"id":"f_kpi3_gaap_1_867_7","label":"GAAP 營業利益（推算＝稅前盈餘 1,867＋淨利息 7）","value":1874,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","unit":"USD百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","citation":"Nucor Q3 2026 新聞稿（IR q4cdn，2026-10-26）https://s202.q4cdn.com/531038915/files/doc_news/Nucor-Reports-Results-for-the-Third-Quarter-of-2026-2026.pdf"},"note":"查無共識"},{"id":"f_kpi4_ebitda","label":"EBITDA（公司披露）","value":2279,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","unit":"USD百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","citation":"Nucor Q3 2026 新聞稿（IR q4cdn，2026-10-26）https://s202.q4cdn.com/531038915/files/doc_news/Nucor-Reports-Results-for-the-Third-Quarter-of-2026-2026.pdf"},"note":"查無共識"},{"id":"f_kpi7_q4_2026","label":"管理層指引（Q4 2026）","value":"Q4 盈餘大致持平至小幅高於 Q3（Q3 EPS 5.80）","period":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","unit":"定性","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","citation":"Nucor Q3 2026 新聞稿（IR q4cdn，2026-10-26）https://s202.q4cdn.com/531038915/files/doc_news/Nucor-Reports-Results-for-the-Third-Quarter-of-2026-2026.pdf"},"note":"無數值區間；Nucor 通常於季末前約兩週另發 Q4 EPS guidance（尚未發布）"},{"id":"f_kpi8","label":"鋼廠產能利用率","value":89,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","citation":"Nucor Q3 2026 新聞稿（IR q4cdn，2026-10-26）https://s202.q4cdn.com/531038915/files/doc_news/Nucor-Reports-Results-for-the-Third-Quarter-of-2026-2026.pdf"},"note":"不適用"},{"id":"f_kpi9_asp","label":"外部平均售價（ASP，合併）","value":1493,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","unit":"USD/短噸","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","citation":"Nucor Q3 2026 新聞稿（IR q4cdn，2026-10-26）https://s202.q4cdn.com/531038915/files/doc_news/Nucor-Reports-Results-for-the-Third-Quarter-of-2026-2026.pdf"},"note":"不適用"},{"id":"f_kpi10","label":"外部銷售噸數","value":7533,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","unit":"千短噸","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","citation":"Nucor Q3 2026 新聞稿（IR q4cdn，2026-10-26）https://s202.q4cdn.com/531038915/files/doc_news/Nucor-Reports-Results-for-the-Third-Quarter-of-2026-2026.pdf"},"note":"不適用"},{"id":"f_kpi11_6_020_8_923_91","label":"庫存天數（推算＝庫存 6,020 / 銷貨成本 8,923 × 91 天）","value":61.4,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","unit":"天","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","citation":"Nucor Q3 2026 新聞稿（IR q4cdn，2026-10-26）https://s202.q4cdn.com/531038915/files/doc_news/Nucor-Reports-Results-for-the-Third-Quarter-of-2026-2026.pdf"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-26","period":"2026-10-26","unit":"date","basis":"距今 6 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-26"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_nue_gross_margin_pct","label":"NUE 毛利率","value":15.94,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NUE.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nue_operating_margin_pct","label":"NUE 營業利益率","value":11.89,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NUE.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nue_fcf_margin_pct","label":"NUE FCF 利潤率","value":3.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NUE.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_stld_gross_margin_pct","label":"STLD 毛利率","value":14.33,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STLD.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_stld_operating_margin_pct","label":"STLD 營業利益率","value":10.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STLD.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_stld_fcf_margin_pct","label":"STLD FCF 利潤率","value":2.54,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STLD.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cmc_gross_margin_pct","label":"CMC 毛利率","value":18.65,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMC.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cmc_operating_margin_pct","label":"CMC 營業利益率","value":9.26,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMC.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cmc_fcf_margin_pct","label":"CMC FCF 利潤率","value":5.1,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMC.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_clf_gross_margin_pct","label":"CLF 毛利率","value":1.54,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLF.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_clf_operating_margin_pct","label":"CLF 營業利益率","value":-1.41,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLF.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_clf_fcf_margin_pct","label":"CLF FCF 利潤率","value":-2.42,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLF.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rs_gross_margin_pct","label":"RS 毛利率","value":28.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rs_operating_margin_pct","label":"RS 營業利益率","value":8.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rs_fcf_margin_pct","label":"RS FCF 利潤率","value":2.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi1_non_gaap_eps_q3_gaap","label":"Non-GAAP 稀釋 EPS（Q3 無調整項，等於 GAAP）","value":5.8,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","unit":"USD/股","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","citation":"Nucor Q3 2026 新聞稿（IR q4cdn，2026-10-26）https://s202.q4cdn.com/531038915/files/doc_news/Nucor-Reports-Results-for-the-Third-Quarter-of-2026-2026.pdf"},"note":"公司 9 月 guidance 5.55–5.65，實際高於區間（來源：Nucor Q3 guidance 新聞稿 q4cdn）"},{"id":"f_kpi5_fcf","label":"自由現金流（FCF）— 僅公司披露前九個月累計；單季未披露","value":2661,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","unit":"USD百萬（9M 累計，2026 前三季）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","citation":"Nucor Q3 2026 新聞稿（IR q4cdn，2026-10-26）https://s202.q4cdn.com/531038915/files/doc_news/Nucor-Reports-Results-for-the-Third-Quarter-of-2026-2026.pdf"},"note":"查無共識"},{"id":"f_kpi6_sbc_9m","label":"SBC 占稅前盈餘（9M 累計）","value":2.8,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-26）","citation":"Nucor Q3 2026 新聞稿（IR q4cdn，2026-10-26）https://s202.q4cdn.com/531038915/files/doc_news/Nucor-Reports-Results-for-the-Third-Quarter-of-2026-2026.pdf"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":284.71,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":26.69,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":73.45,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.61,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.53 → 19.65）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":1.86,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（21.02 → 21.41）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":2.94,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.38 → 19.95）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":19.65,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":21.41,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":19.95,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":6.45,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 18.46 → 19.65（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":18.13,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝76.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":76.1,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.66,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.75,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":14.49,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 19.65，分子＝快照價 284.71","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.787,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":3453.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 7093.0、現金 3640.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":226.88,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":68046.77,"period":"2026-11-03","unit":"USD m","basis":"市值 64593.77 ＋ 淨負債 3453.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":41525.17,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（11 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":42833.59,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（13 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.64,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 278.8 / W52 212.41 / W104 170.38 / W250 155.3 / W250 13週斜率 1.74%"},{"id":"f_ma_w52","label":"52 週均線","value":212.41,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":170.38,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":155.3,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.74,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K FY2025 稱鋼鐵市場高度競爭，內外國業者眾多，Nucor 主要以價格與服務競爭；外國對手多受國家補貼","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"These markets are highly competitive with many domestic and foreign firms participating, and, as a result of this highly competitive environment, we find that we primarily compete on price and service.","as_of":"2026-02-25","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K FY2025 風險因素：持續面對其他鋼廠與進口品在價格、品質、服務上的競爭","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"We face ongoing competition from other steel producers and imports that compete with our products on price, quality and service.","as_of":"2026-02-25","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Nucor 10-Q（Q1 2026）稱進口占美國成品鋼市場比重由 2025 Q1 逾 22% 降至 2026 Q1 約 15%","source":"SEC EDGAR 10-Q 2026-04-04","url":"https://www.sec.gov/Archives/edgar/data/0000073309/000119312526220778/nue-20260404.htm","excerpt":"laws in combination with Section 232 national security tariffs, are continuing to reduce the flood of unfairly traded imports into the United States. Imports' share of the U.S. finished steel market declined from over 22% in the first quarter of 2025 to approximately 15% in the first quarter of 2026.","as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Nucor Q3 2026 投資人資料：進口市占由 4Q25 約 14% 升至 3Q26 約 17%，南韓進口前三季 +57%","source":"SEC EDGAR 8-K Ex.99.2 (Q3 2026)","url":"https://www.sec.gov/Archives/edgar/data/0000073309/000119312526318190/d468854dex992.htm","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Hyundai Steel 與 POSCO 於路易斯安那 Donaldsonville 啟動 58 億美元 EAF 鋼廠合資，目標 2029 商轉，主打車用","source":"Asia News Network","url":"https://asianews.network/?p=299162","excerpt":"From White House pledge to Louisiana, South Korean firm Hyundai’s US$5.8 billion bet takes shape From White House pledge to Louisiana, South Korean firm Hyundai’s US$5.8 billion bet takes shape","as_of":"2026-09-15","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Nucor 10-Q 揭露 2026 Q2 最大單一客戶約占銷售 5%，客戶集中度低；搜尋未見任何客戶導入第二供應商或自製的報導。","source":"SEC EDGAR｜Nucor 10-Q（季度結束 2026-07-04）","url":"https://www.sec.gov/Archives/edgar/data/0000073309/000119312526345891/nue-20260704.htm","excerpt":"Our largest single customer in the second quarter of 2026 represented approximately 5% of sales and has consistently paid within terms.","as_of":"2026-07-04","retrieved_at":"2026-11-03","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K：最大單一客戶約占 2025 年銷售 5%，且一貫在期限內付款；公司表示不依賴單一客戶。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"We have a diverse customer base and are not dependent on any single customer. Our largest single customer in 2025 represented approximately 5% of sales and consistently pays within terms.","as_of":"2026-02-25","retrieved_at":"2026-11-03","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K MD&A 市場風險：最大客戶約 5% 銷售、準時付款；鋼廠與鋼製品段為最大市場風險暴露。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"Our largest single customer in 2025 represented approximately 5% of sales and consistently pays within terms.","as_of":"2026-02-25","retrieved_at":"2026-11-03","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"2026 年信用評等 A-（S&P）、A-（Fitch）、A3（Moody's），展望穩定；搜尋未見 2026 年任何升降評或展望變動（摘要來自搜尋結果對 Q2 2026 10-Q 的描述）。","source":"Nucor 10-Q Q2 2026（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0000073309/000119312526345891/nue-20260704.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"OECD Steel Outlook 2026 projects global steel excess capacity reaching 745 million tonnes by 2028, utilization falling to 74% or lower from 76% in 2025; most expansion outside OECD, with growing circumvention of trade measures.","source":"OECD Steel Outlook 2026 / eurometal.net","url":"https://eurometal.net/oecd-global-steel-excess-capacity-set-to-reach-745-million-mt-by-2028/","excerpt":null,"as_of":"2026-06-04","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"worldsteel Oct 2026 cut forecast: global demand flat in 2026 and +1.7% in 2027 (was 2.2%); China demand to fall 2% in 2026 and 1% in 2027. April worldsteel forecast had US demand +1.7% in 2026 and +2.0% in 2027.","source":"Engineering News, Global steel demand to remain flat this year on China slowdown","url":"https://www.engineeringnews.co.za/article/global-steel-demand-to-remain-flat-this-year-on-china-slowdown-2026-10-12","excerpt":null,"as_of":"2026-10-12","retrieved_at":"2026-11-03","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Fastmarkets: Nucor execs say robust demand driving shipments and higher earnings likely to extend into 2027; Q2 call cited demand strength in energy, data centers, automotive, consumer durables, est. US steel demand +2% in 2026.","source":"Fastmarkets / MarketBeat Q2 call highlights","url":"https://www.fastmarkets.com/insights/robust-demand-driving-nucor-shipments-earnings-higher-likely-to-extend-into-2027-execs/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"2026-11-03","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Nucor Q3 2026 (reported Oct 26): net earnings about $1.32B, $5.80/share; Q4 guided in line with or modestly higher than Q3; West Virginia sheet mill first heat in September.","source":"SteelOrbis, Nucor's net income up 14.1 percent in Q3 2026","url":"https://www.steelorbis.com/steel-news/latest-news/nucors-net-income-up-141-percent-in-q3-2026-1486602.htm","excerpt":null,"as_of":"2026-10-26","retrieved_at":"2026-11-03","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"US new capacity pipeline: ArcelorMittal Calvert EAF expected at full capacity 2H 2026 with second EAF under consideration; U.S. Steel Gary Tin Mill restart early 2027; Big River DRI plant completion 2027; Hyundai Louisiana ~2.7-2.8Mtpa DRI-EAF sheet timeline unclear.","source":"gmk.center / SMM / Industrial Info","url":"https://news.metal.com/newscontent/103869875-smm-steelus-steel-plans-to-reactivate-gary-tin-mill-in-early-2027","excerpt":null,"as_of":"2026-08-04","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"OECD Steel Outlook 2026 executive summary on excess capacity","source":"OECD","url":"https://www.oecd.org/en/publications/oecd-steel-outlook-2026_99ab9b0c-en/full-report/executive-summary_4410f4cc","excerpt":null,"as_of":"2026-06-04","retrieved_at":"2026-11-03","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：Nucor 稱其訴訟與程序單獨或合計預期不會對經營結果、財務狀況或現金流造成重大不利影響；未揭露反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"We do not believe that any of these proceedings, individually or in the aggregate, would be expected to have a material adverse effect on our results of operations, financial condition or cash flows.","as_of":"2026-02-25","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Nucor Steel Louisiana（DRI 廠）自2022年起被EPA指控違反清潔空氣法，與DOJ、EPA、路易斯安那州DEQ的合併和解協商中，公司預期不重大。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"A combined settlement is currently being negotiated with the U.S. Department of Justice, the EPA and the Louisiana Department of Environmental Quality. We do not believe that any aggregate settlement for these allegations will be material to Nucor.","as_of":"2026-02-25","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"JSW Steel 對Nucor等的鋼板反壟斷訴訟，第五巡迴上訴法院2025年4月維持駁回。","source":"Arnold & Porter 新聞稿","url":"https://www.arnoldporter.com/en/perspectives/news/2025/04/arnold-porter-secures-appellate-victory-for-nucor-in-steel-antitrust-case","excerpt":"JSW alleged that the defendants’ objections misrepresented the domestic industry’s ability to supply equivalent slab and that some of them later refused sale of the material, impairing JSW’s ability to compete in downstream steel markets. The Fifth Circuit panel unanimously affirmed dismissal of the claims, holding that Nucor and its fellow defendants’","as_of":"2025-04-01","retrieved_at":"2026-11-03","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Section 232 鋼鐵關稅 2025 年無豁免全面恢復並擴及約 600 項加工鋼製品；2025 年成品碳鋼與合金鋼進口較 2024 年減 17.4%，約占美國需求 18%；公司表示關稅未來可能被修改或終止。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"In 2025, vigorous enforcement of U.S. trade remedy laws and the full reinstatement of the Section 232 steel tariffs without exemptions or exclusions resulted in a lower volume of steel 9 imports compared to 2024. Imports of finished carbon and alloy steel products decreased 17.4% from 2024, supplying approximately 18% of U.S. demand in 2025.","as_of":"2026-02-25","retrieved_at":"2026-11-03","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"風險因子：若 Section 232 等進口關稅到期、放寬或廢止，大量外國鋼材進口可能對美國鋼價形成下行壓力。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"There can be no assurance as to when or if the Section 232 or other import tariffs, quotas or other duties may be enacted, enforced, extended, modified or terminated in the future.","as_of":"2026-02-25","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Q2 2026 法說會：管理層稱成品鋼進口年減 25%，歸因於強化的 232 計畫與反傾銷／反補貼稅；並呼籲 USMCA 續約要求鋼材於北美熔煉澆鑄。","source":"Nucor Q2 2026 earnings call transcript (Webull)","url":"https://www.webull.com/news/15661328036856832","excerpt":"finished steel imports are down 25% year-over-year due to the strengthening of the 232 program, along with antidumping and countervailing duties on corrosion-resistant steel and other steel products.","as_of":"2026-07-28","retrieved_at":"2026-11-03","affects":["moat_trend","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Nucor 把 USMCA 檢討（2026-07 起）視為主要北美貿易風險，主張處理經墨西哥、加拿大轉運的海外鋼材與加拿大鋼業補貼，並要求「熔煉澆鑄於北美」規則","source":"Argus / steel-technology.com 轉述 Nucor Q4 2025 財報電話會","url":"https://www.steel-technology.com/index.php/news/nucor-forecasts-strong-2026-outlook-driven-by-tariffs-surging-demand-and-new-sheet-mill-investments","excerpt":"One important change we hope to see is a requirement that all steel used in any steel or steel intensive products must be melted and poured in North America to qualify as USMCA compliant.","as_of":"2026-02-01","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"Section 232 關稅 50% 自 2025-06 起，進口鋼占美國消費比重由 2025 初 25% 降至 11 月 14%，Nucor 預期 2026 維持在此水準或更低","source":"Argus / steel-technology.com 轉述 Nucor Q4 2025 財報電話會","url":"https://www.argusmedia.com/news-and-insights/latest-market-news/2781160-tariffs-demand-boost-us-steel-outlook-nucor","excerpt":"Nucor projects that imports will remain at or below these suppressed levels throughout 2026","as_of":"2026-02-01","retrieved_at":"2026-11-03","affects":["thesis.H","valuation"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2022 10-K：2022 俄烏戰爭後 Nucor 停止自俄羅斯採購生鐵，生鐵供應集中俄烏致全球價格波動","source":"Nucor 10-K FY2022","url":"https://www.sec.gov/Archives/edgar/data/73309/000156459023002793/nue-10k_20221231.htm","excerpt":"For example, when Russia invaded the eastern regions of Ukraine in February of 2022, we stopped all ordering of pig iron (a scrap substitute) from Russia and the supply of global pig iron was severely disrupted due to the concentration of pig iron supply in Russia and","as_of":"2023-02-24","retrieved_at":"2026-11-03","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：仍須外購大部分主要原料（廢鋼、替代品），部分來自政治動盪地區","source":"Nucor 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"scrap substitutes (e.g., prime scrap, pig iron and DRI) that are critical to the manufacture of our steel products. The raw material required to produce DRI is pelletized iron ore. Although we have vertically integrated our business by constructing our DRI facilities in Trinidad and Louisiana and also by acquiring our scrap processing and brokerage operations, DJJ, in 2008, we still must purchase","as_of":"2026-02-27","retrieved_at":"2026-11-03","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Nucor Q3 2026 (ended 2026-10-03): net sales約$11.25B(+32% YoY)；鋼廠段稅前獲利$1.79B（去年同期$793M），外部鋼廠均價$1,233/短噸（Q2 $1,145），開工率89%（Q2 91%）；鋼品段獲利$465M（Q2 $353M、去年同期$319M）；原料段獲利降至$105M。","source":"Nucor Q3 2026 earnings release / SEC 8-K Ex.99.1","url":"https://www.sec.gov/Archives/edgar/data/0000073309/000119312526432117/d129328dex991.htm","excerpt":null,"as_of":"2026-10-26","retrieved_at":"2026-11-03","affects":["valuation","moat_trend"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Nucor 對Q4 2026指引：整體獲利與Q3持平或小幅上升；鋼廠段因實現價格較高，被季節性較低出貨量與較高成本抵銷，獲利穩定。","source":"Metal.com: Nucor Q3 steel shipments up 11.2% YoY, sees Q4 earnings in line to modestly higher","url":"https://news.metal.com/newscontent/104182160-nucor-q3-steel-shipments-up-112-yoy-sees-q4-earnings-in-line-to-modestly-higher","excerpt":null,"as_of":"2026-10-26","retrieved_at":"2026-11-03","affects":["valuation","triggers"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"管理層預期2026年美國鋼需約+2%；Nucor 2026出貨成長預估落在先前5–10%區間高端；預期需求強勁延續到2027，主要由能源、先進製造、資料中心帶動；汽車與住宅等利率敏感市場改善有限；進口成品鋼年減約25%（歸因232條款與反傾銷/反補貼稅）；訂單積壓延伸至2027。","source":"Fastmarkets: Robust demand driving Nucor shipments, earnings higher likely to extend into 2027: execs","url":"https://www.fastmarkets.com/insights/robust-demand-driving-nucor-shipments-earnings-higher-likely-to-extend-into-2027-execs/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"2026-11-03","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Nucor熱軋捲CSP 2026年夏季續升：7/28報導+$10/t，美國HRC均價約$1,165/短噸(7/21)；8/11報導再+$5/t，均價約$1,180(8/4)，並提及季節性放緩可能限制進一步大漲；6/29信函曾持平，稱留意進口量。","source":"GMK Center","url":"https://gmk.center/en/news/nucor-has-once-again-raised-hrc-price-by-5-t/","excerpt":null,"as_of":"2026-08-11","retrieved_at":"2026-11-03","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Nucor Q2 2026：片材與板材市場多年期強勁（SMU）","source":"Steel Market Update","url":"https://www.steelmarketupdate.com/2026/07/28/nucor-sees-multi-year-strength-in-sheet-and-plate-markets/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"2026-11-03","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Nucor 10-K 自述鋼材在許多應用上與混凝土、鋁、塑膠、複合材料、木材競爭，替代材料用量增加可能對鋼價與需求造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"In many applications, steel competes with other materials, such as concrete, aluminum, plastics, composites and wood. Increased use or availability of these materials in substitution for steel products could have a material adverse effect on prices and demand for our steel products.","as_of":"2026-02-25","retrieved_at":"2026-11-03","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Nucor 以電弧爐（EAF）為主、以廢鋼及替代原料（含自有 DRI）煉鋼；2025 年兩座 DRI 廠供應約 330 萬公噸。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"Nucor manufactures steel principally from scrap steel and scrap steel substitutes using electric arc furnaces (“EAFs”) along with continuous casting and automated rolling mills.","as_of":"2026-02-25","retrieved_at":"2026-11-03","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"搜尋摘要：美國氫基綠鋼進展停滯，業界會議指美國買家不願付綠鋼溢價，低價高碳進口鋼被視為更大威脅；ICCT 2026-08 工作論文估 H2-DRI-EAF 綠鋼約 $812/噸，綠地廠比改造高爐-轉爐成本高約 34%。","source":"ICCT working paper Aug 2026; Fastmarkets; Canary Media（搜尋摘要）","url":"https://theicct.org/publication/estimating-green-steel-production-costs-us-aug26/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"2026-11-03","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K 描述金屬建築產品主要經獨立建商經銷網路銷售，沿用既有通路模式。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"The buildings are sold primarily through independent builder distribution networks in order to provide fast-track, customized solutions for building owners.","as_of":"2026-02-25","retrieved_at":"2026-11-03","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 2026 10-Q：最大單一客戶約占銷售 5%，客戶集中度低。","source":"SEC EDGAR 10-Q (Q2 2026)","url":"https://www.sec.gov/Archives/edgar/data/0000073309/000119312526345891/nue-20260704.htm","excerpt":"Our largest single customer in the second quarter of 2026 represented approximately 5% of sales","as_of":"2026-07-04","retrieved_at":"2026-11-03","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Nucor Q3 2026 release (late Oct 2026): management expects Q4 2026 earnings generally in line with or modestly higher than Q3; steel mills stable, steel products flat, raw materials slightly lower. Q3 revenue $11.25B vs consensus $10.79B, adj EPS $5.80 vs $5.83 est; stock rose ~6%.","source":"TIKR blog: Nucor soars 6% on Q3 revenue beat, sees Q4 in line with or modestly higher","url":"https://www.tikr.com/de/blog/nucor-soars-6-on-q3-revenue-beat-sees-q4-in-line-with-or-modestly-higher","excerpt":null,"as_of":"2026-10-27","retrieved_at":"2026-11-03","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026 guidance issued 2026-09-17 was EPS $5.55-$5.65 (raised from $4.5-$4.6), vs consensus EPS $6.17 at that time (guided below consensus); Q4 2026 EPS consensus ~$5.07-$5.14 on revenue ~$9.75-9.80B per Benzinga snapshots (undated).","source":"Benzinga NUE earnings forecasts","url":"https://www.benzinga.com/quote/NUE/earnings-forecasts","excerpt":null,"as_of":"2026-09-17","retrieved_at":"2026-11-03","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Analyst price targets vary by source/date: Bullstory avg $282.81 from 16 analysts as of 2026-08-30 (Buy); Walnut avg $280.31 (16 analysts, Aug 2026); Tickflow avg $253.63 (22 analysts, 2026-07-31); StreetInsider 12-month range high $297 (Wells Fargo) to low $190 (Jefferies), avg $264.90. No snapshot dated after late Aug 2026 found.","source":"Bullstory NUE analyst forecast; Tickflow; StreetInsider","url":"https://bullstory.io/en/stocks/nue/forecast","excerpt":null,"as_of":"2026-08-30","retrieved_at":"2026-11-03","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Nucor 8-K Q3 2026 earnings release with Q4 outlook","source":"SEC EDGAR 8-K ex99.1","url":"https://www.sec.gov/Archives/edgar/data/0000073309/000119312526432117/d129328dex991.htm","excerpt":"Fourth Quarter of 2026 Outlook Compared to the Third Quarter of 2026 We expect earnings in the fourth quarter of 2026 to be generally in-line with or modestly higher than the third quarter.","as_of":"2026-10-27","retrieved_at":"2026-11-03","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月（2025-11-03至2026-11-03）11份8-K中，含重大項目（1.01/1.02/1.03/2.01/2.05/2.06/3.01/4.02/5.01/8.01等）者0份。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000073309&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K：Nucor Steel Louisiana（DRI廠）自2022年起收到EPA清潔空氣法違規指控，正與DOJ/EPA/LDEQ協商合併和解；公司認為不重大。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"During 2022, Nucor Steel Louisiana, our DRI facility located in St. James Parish, Louisiana, received allegations of violations of the Clean Air Act from the EPA. A combined settlement is currently being negotiated with the U.S. Department of Justice, the EPA and the Louisiana Department of Environmental Quality. We do not believe that any aggregate settlement for these allegations will be material to Nucor.","as_of":"2026-02-25","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Nucor 2026 capex target約25億美元，約60%用於成長專案（含西維吉尼亞新薄板廠）","source":"chartmill: NUE Q2 Earnings Call Highlights Growth Projects And Demand","url":"https://www.chartmill.com/news/external/97849/nue-q2-earnings-call-highlights-growth-projects-and-demand","excerpt":null,"as_of":"2026-07-30","retrieved_at":"2026-11-03","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Nucor Berkeley（南卡 Huger）50萬短噸/年連續鍍鋅線預計2026年中投產","source":"Steel Market Update: Nucor gives updates on new capacity coming online","url":"https://www.steelmarketupdate.com/2025/05/01/nucor-gives-updates-on-new-capacity-coming-online/","excerpt":null,"as_of":"2025-05-01","retrieved_at":"2026-11-03","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"北美鋼業近五年資本支出專案近500億美元；日本製鐵旗下U.S. Steel計畫至2028年資本支出140億美元","source":"IndustrialInfo: AISTech 2026 U.S. Steel Industry Healthy Riding $50 Billion Capital Spending Wave","url":"https://www.industrialinfo.com/iirenergy/industry-news/article/aistech-2026-us-steel-industry-healthy-riding-50-billion-capital-spending-wave--357467","excerpt":null,"as_of":"2026-04-01","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"U.S. Steel計畫2027年初重啟Gary鍍錫廠（非新EAF）","source":"SMM Steel","url":"https://news.metal.com/newscontent/103869875-smm-steelus-steel-plans-to-reactivate-gary-tin-mill-in-early-2027","excerpt":null,"as_of":"2026-06-01","retrieved_at":"2026-11-03","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Cleveland-Cliffs 9/28宣布因關稅與市況裁員最多500人（產能收縮訊號，搜尋結果摘要）","source":"WebSearch result summary on Nucor peers","url":null,"excerpt":null,"as_of":"2026-09-28","retrieved_at":"2026-11-03","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"GMK Center 2026-10-20 報導 Nucor 再度上調熱軋卷 CSP 至約 $1,255/short ton，並引 Fastmarkets 稱熱軋卷價格一年內上漲 52%","source":"GMK Center: Nucor has increased prices for hot-rolled coils by $15/t","url":"https://gmk.center/en/news/nucor-has-increased-prices-for-hot-rolled-coils-by-15-t/?category=industry%2F","excerpt":"According to Fastmarkets, the price of hot-rolled coil has risen by 52 per cent over the past year, reaching $1,255 per short tonne. This figure was last recorded in May 2022.","as_of":"2026-10-20","retrieved_at":"2026-11-03","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"Nucor 2026 Q3 業績：淨利 $1.32B、EPS $5.80、平均售價 $1,493/short ton，Q4 預期與 Q3 持平或略高","source":"Nucor Reports Results for the Third Quarter of 2026 (SteelOrbis/Metal.com)","url":"https://news.metal.com/newscontent/104182160-nucor-q3-steel-shipments-up-112-yoy-sees-q4-earnings-in-line-to-modestly-higher","excerpt":"For the fourth quarter of 2026, Nucor expects earnings generally in line with or modestly higher than third-quarter levels, with Steel Mills segment earnings projected to remain stable as higher realized pricing is offset by seasonally lower volumes","as_of":"2026-10-28","retrieved_at":"2026-11-03","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Nucor 2015 full-year net earnings約$80.7M（$0.25/股），2016為$796.3M（$2.48/股）；2015 ROE 1.0%","source":"Nucor FY2016 10-K Exhibit 13","url":"https://www.sec.gov/Archives/edgar/data/0000073309/000119312517062124/d298801dex13.htm","excerpt":null,"as_of":"2017-02-24","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2016 Q1 Nucor鋼廠部門平均售價每噸由$732降至$538（-27% YoY）","source":"Nucor 10-Q 2016","url":"https://www.sec.gov/Archives/edgar/data/0000073309/000119312516586874/d152409d10q.htm","excerpt":null,"as_of":"2016-05-01","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2024 Q2 Nucor預告EPS年減逾60%，主因鋼廠平均售價下降；另一來源稱HRC基準價自2024年初約$1,200/short ton跌逾40%（與另一來源『自4月高點跌約17%』不一致）","source":"Steel Market Update / GMK Center","url":"https://steelmarketupdate.com/2024/06/14/nucor-warns-of-weaker-q2-earnings-on-lower-prices-volumes","excerpt":null,"as_of":"2024-06-14","retrieved_at":"2026-11-03","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2024全年Nucor EBITDA $4.36B，較2023年$7.41B低41%；Q4 2024淨利$345M對比去年同期$873M","source":"GMK Center","url":"https://gmk.center/en/news/nucor-expects-financial-results-to-deteriorate-in-q3/","excerpt":null,"as_of":"2025-01-29","retrieved_at":"2026-11-03","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#4","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Steel Market Update價格資料：2014–2015跌勢延續約83週至紀錄低點；2011年一波下跌33週","source":"Steel Market Update, Dead cat bounces are not unusual in down cycles","url":"https://www.steelmarketupdate.com/2019/09/19/dead-cat-bounces-are-not-unusual-in-down-cycles/","excerpt":null,"as_of":"2019-09-19","retrieved_at":"2026-11-03","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#5","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Metinvest執行長稱2000年代初鋼鐵下行不到1.5年、2008–09僅數月，2022起的下行為20年來最長（至2024已逾3年）","source":"GMK Center, Metinvest CEO","url":"https://gmk.center/en/news/steel-market-is-experiencing-the-longest-downturn-in-20-years-metinvest-ceo/","excerpt":null,"as_of":"2024-12-01","retrieved_at":"2026-11-03","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K中無含1.01/2.01等重大項目者。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000073309&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K稱各項訴訟個別或合計預期不致對經營、財務或現金流有重大不利影響；僅EPA清潔空氣法指控正和解協商中，未見證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm","excerpt":"We do not believe that any of these proceedings, individually or in the aggregate, would be expected to have a material adverse effect on our results of operations, financial condition or cash flows.","as_of":"2026-02-25","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K中無Item 4.02（財報不可信賴/重編）等重大項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000073309&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"NUE","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.94,"operating_margin_pct":11.89,"fcf_margin_pct":3.81,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NUE","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"STLD","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":14.33,"operating_margin_pct":10.66,"fcf_margin_pct":2.54,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STLD","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CMC","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":18.65,"operating_margin_pct":9.26,"fcf_margin_pct":5.1,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMC","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CLF","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":1.54,"operating_margin_pct":-1.41,"fcf_margin_pct":-2.42,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLF","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"RS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":28.1,"operating_margin_pct":8.76,"fcf_margin_pct":2.83,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RS","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"NUE"},"financial_history":{"ticker":"NUE","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":41512000000.0,"revenue_yoy_pct":null,"gross_margin_pct":30.12,"operating_margin_pct":25.31,"net_income":7607000000.0,"diluted_eps":28.79,"free_cash_flow":8124000000.0,"fcf_margin_pct":19.57,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":34714000000.0,"revenue_yoy_pct":-16.38,"gross_margin_pct":22.51,"operating_margin_pct":17.95,"net_income":4525000000.0,"diluted_eps":18.0,"free_cash_flow":4898000000.0,"fcf_margin_pct":14.11,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":30734000000.0,"revenue_yoy_pct":-11.47,"gross_margin_pct":13.35,"operating_margin_pct":9.69,"net_income":2027000000.0,"diluted_eps":8.46,"free_cash_flow":806000000.0,"fcf_margin_pct":2.62,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":32494000000.0,"revenue_yoy_pct":5.73,"gross_margin_pct":11.93,"operating_margin_pct":8.18,"net_income":1744000000.0,"diluted_eps":7.52,"free_cash_flow":-188000000.0,"fcf_margin_pct":-0.58,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/NUE/NUE_Q3_2026_Earnings_Call_20261027.md）

# Q3 2026 Earnings Call
**Nucor Corporation** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Good morning, and welcome to Nucor's Third Quarter 2026 Earnings Call. [Operator Instructions] Today's call is being recorded. [Operator Instructions] I would now like to introduce Chris Jacobi, Director of Investor Relations. You may begin your call.

**Chris Jacobi** (Executives):
Thank you, and good morning, everyone. Welcome to Nucor's Third Quarter Earnings Review and Business Update. Leading our call today is Leon Topalian, Chair and CEO; along with Steve Laxton, President and COO; and Jack Sullivan, CFO. Other members of Nucor's executive team are also here with us today and may participate during the Q&A portion of the call. Yesterday, we posted our third quarter earnings release and investor presentation to Nucor's IR website. We encourage you to access these materials as we'll cover portions of them during the call.
Today's discussion will include the use of non-GAAP financial measures and forward-looking information within the meaning of securities laws. Actual results may be different than forward-looking statements and involve risks outlined in our safe harbor statement and disclosed in Nucor's SEC filings. The appendix of today's presentation includes supplemental information and disclosures, along with a reconciliation of non-GAAP financial measures. 
So with that, let's turn the call over to Leon.

**Leon Topalian** (Executives):
Thanks, Chris. I want to begin by recognizing our 33,000 teammates for making the summer of 2026 our safest summer ever. Summer brings added safety challenges, and our team met them with focus and determination. That's something to be proud of, and it reflects our commitment to the most important value we have, safety. And as we finish the year, let's keep looking out for one another and make sure every one of our team members goes home safely at the end of every shift.
Turning to our third quarter financial results. Nucor delivered its strongest quarter in more than 3 years with approximately $2.3 billion of EBITDA and earnings of $5.80 per share. Jack is going to unpack our results in more detail, but many of the themes we've highlighted throughout the year continue this quarter: strong demand across key end markets, growing contributions from recent investments and federal policies that support a healthy domestic steel sector. And with the capital spending moderating as major projects near completion, that strength is increasingly showing up in Nucor's free cash flow. We also remain committed to meaningful shareholder returns, returning $629 million in dividends and buybacks during the quarter, bringing our year-to-date total to nearly $1.4 billion.
Operationally, the Nucor team is executing exceptionally well across each of our business segments. In our steel mills, quarterly shipments exceeded 7.2 million tons, setting another shipment record for the third consecutive quarter. This would not be possible without the investments we've made over the past 6 years, many of which are now online and contributing to our results. For example, the plate group set another quarterly shipment record. Brandenburg shipped approximately 240,000 tons, or roughly 1/3 of the group's total shipments. The team has done an amazing job bringing the mill's full capabilities online and advancing customer qualifications. The bar group also set another quarterly shipment record. 
Our Lexington micro mill has had a very successful ramp-up since coming online last year. The team became EBITDA positive in March and has built on that progress, reaching a utilization rate of nearly 80% in the third quarter. We've also seen very strong results from Kingman, Arizona, and our micro mills at Frostproof and Sedalia, as well as our upgraded Kankakee mill, helped to deliver our best merchant bar quarter in several years. In steel products, we saw a significant improvement in quarterly earnings. Higher shipments and a notable inflection in pricing led to margin expansion across most of our major product groups. Joist and deck had a standout quarter with shipments up about 20% and realized pricing increasing by $110 a ton.
In raw materials, our Louisiana DRI plant has begun capturing CO2 emissions for transport and storage through a project with ExxonMobil. The project is designed to capture and store up to 800,000 tons of CO2 annually, supporting our greenhouse gas emissions reduction goals and strengthening Nucor's position as one of the world's cleanest steel producers. Congratulations to our entire team in Louisiana on this achievement.
The strength we are seeing in today's domestic steel market is being driven by healthy economic conditions and broad-based investment across key end markets. Nucor is benefiting from these conditions because trade policy improvements over the past decade have created a more level playing field. In particular, vigorous trade law enforcements and strengthening Section 232 measures are allowing us to realize a greater share of the strong demand environment in the U.S. Finished steel imports are down more than 13% year-over-year and down 24% compared to 2024. Fair trade supports strong markets, unfair trade distorts them. However, import volumes have been increasing in recent months, including a massive surge from South Korea despite the Section 232 tariffs.
From decades of experience fighting for a level playing field, we know we must always stay vigilant. Therefore, we will work closely with the administration to ensure trade measures remain robust and effective. But make no mistake, demand is very healthy. Even as imports have crept higher this year, domestic shipments have risen in each of the past 3 quarters. Strong market fundamentals and favorable trade policies will continue to support a positive outlook for the domestic steel industry. 
With that, I'll turn it over to Steve for an update on our growth initiatives and market outlook. Steve?

**Stephen Laxton** (Executives):
Thank you, Leon, and thank you all for joining us this morning. We're in the final stages of construction at our new sheet mill project in West Virginia, and we're commissioning equipment across the site. I want to thank the team in West Virginia for their hard work and excellent safety performance throughout the multiyear construction phase. They've kept the project on time and on budget while reaching several important milestones. In September, the melt shop produced its first heat. And in October, we started shipping coils from the pickle line to our downstream Nucor divisions. And by December, we expect to run our first coils through the hot mill, cold mill and construction-grade galv lines. 
As we complete commissioning, the team is preparing to ramp production in early 2027. Our priority will be to operate safely and reliably while steadily increasing production toward our 50% utilization target by the end of 2027. Our sheet mill network provides an important advantage as production begins. By gradually shifting baseload tons from other Nucor sheet mills to West Virginia, we can provide the new mill a steady base of orders to support a successful ramp through 2027 and '28. As with any project of this scale and complexity, we expect start-up costs to remain elevated in 2027 at levels similar to or higher to those in 2026. 
Turning to our Berkeley, South Carolina sheet mill, our new automotive-grade galvanizing line began production early this month. We expect utilization rates for the new galv line to reach 50% in the second quarter of next year, on its way to full run rate by the end of 2027. At full production, this new line will add 500,000 tons of annual galvanizing capacity. Taken together, our investments in West Virginia and South Carolina enhance Nucor's ability to serve the automotive market, where we are relatively underweighted today. As both projects ramp and complete customer qualifications, we will build on the strong relationships we already have in place with many of North America's leading automakers.
But we are not simply waiting for these investments to ramp. While North American automotive production is essentially unchanged year-to-date, Nucor's flat-rolled shipments to automotive customers are up 4%. And as we grow our automotive shipments, we're expanding what we can offer with the capabilities we have in place today. Recently, we commercialized exposed-quality galvanized steel for the exterior panel of an SUV platform. We accomplished this using thin slab casting, demonstrating Nucor's innovation in EAF steelmaking. And as new growth projects come online, we'll have even more opportunities to expand our position in the automotive market.
Moving to our Towers & Structures business. We're encouraged by how each of our facilities is progressing and the strength of our customer demand. Our Decatur, Alabama facility is on track to be EBITDA positive this month, while our Crawfordsville, Indiana facility began full production in the third quarter and is expected to follow a similar path toward profitability. Our Brigham City, Utah facility remains on track to reach full production by mid-2027. We are now qualified with more than 30 utilities with additional customer qualifications underway. And we've entered into multiyear agreements with several of the largest utilities in the United States. That momentum is reflected in our order backlog, which has more than doubled since the start of the year and extends into early 2028.
Based on the strength of customer demand, we recently announced a combined $165 million of investments to increase the capacity of our Indiana and Alabama facilities by about 50%. As a result, we now expect our long-term annual EBITDA contribution from our Towers & Structures business to reach approximately $200 million, up from the $150 million previously forecast.
Turning to our demand outlook. Nucor continues to expect steel mill shipments growth to finish closer to the higher end of our 5% to 10% range for 2026, supported by several durable underlying drivers. Let me touch on a few of these. First, infrastructure. While the IIJA was passed about 5 years ago, the infrastructure investment activity it was meant to spur is still accelerating. State-level decision-making and permitting have, in many cases, taken years to complete, extending construction activity over a longer period of time. Today, many projects are underway, but new ones are still being approved, and over $135 billion of funding has yet to be spent as of August. In addition, steel requirements for the border wall are substantial, and stadium construction shows no signs of slowing.
Second, reshoring and digital infrastructure. The COVID pandemic highlighted the fragility of our domestic supply chain and underscored the need to manufacture more in the U.S. And supportive federal actions on tax, trade and regulatory fronts have helped stimulate considerably higher levels of manufacturing construction. This is broader than the chip fab activity first encouraged by the CHIPS Act and now includes sectors like pharmaceuticals, automotive, appliance and electrical components. And data center construction activity has gone from a small niche to a significant driver of nonresidential building construction activity. 
Finally, energy. Rising demand, aging infrastructure and the need to strengthen the grid are driving substantial investment in the power sector. Utilities plan to spend nearly $1.4 trillion over the next 5 years, with steel-intensive investments ranging from generation and substations to transmission upgrades. Beyond power, we're seeing strong demand across the oil and gas sector, including LNG terminals and pipeline construction and growing domestic production of oil country tubular goods. We see these trends as durable, and we believe Nucor is incredibly well positioned with our world-class manufacturing team and broad portfolio to meet the needs of our customers across these diverse applications. 
With that, let me turn the call over to Jack. Jack?

**Jack Sullivan** (Executives):
Thanks, Steve, and good morning, everyone. In the third quarter, Nucor generated net earnings of $1.3 billion, or $5.80 per share. This exceeded the midpoint of our guidance range by roughly 3.5%, primarily due to higher-than-expected shipments and higher average selling prices in our steel mills segment. 
Let me now review our third quarter performance by segment. The steel mills segment generated $1.8 billion of pretax earnings, an increase of $232 million from the prior quarter. As Leon mentioned, we set another quarterly shipment record with volumes up 2%. Average selling prices rose across the segment, led by our sheet and structural groups. These increases were partially offset by higher costs. As a reminder, the second quarter benefited from $130 million in cash refunds that reduced cost of goods sold, and that benefit did not recur in the third quarter.
Turning to steel products. We generated pretax earnings of $465 million, an increase of $112 million from the prior quarter. Volumes increased 6%, and average selling prices rose 7%. The improvement in pricing was particularly encouraging as realized pricing in our downstream businesses is catching up with the higher steel input costs that compressed margins earlier this year. As a result, the EBITDA margin for our steel products segment increased approximately 200 basis points from the second quarter. And in our raw materials segment, we generated pretax earnings of $105 million compared to $146 million in the prior quarter, reflecting lower pricing and shipments. Preoperating and start-up costs totaled $124 million compared to $120 million in the prior quarter.
Turning to capital allocation and the balance sheet. We generated $1.6 billion of free cash flow in the third quarter, bringing our year-to-date total to nearly $2.7 billion. Cash from operations has grown from $900 million in the first quarter to over $2.2 billion in the third, as we benefit from healthy market conditions and growing contributions from our recent investments. At the same time, capital spending is moderating as our major projects near completion. We've deployed just under $1.9 billion in CapEx year-to-date, with the majority going toward growth projects. For the full year, we expect our capital expenditures to finish at or slightly below our original $2.5 billion estimate.
Our free cash flow supports meaningful returns to shareholders. During the quarter, we returned $629 million through dividends and share repurchases, up approximately $150 million from the second quarter. Year-to-date, we've returned nearly $1.4 billion, or 42% of net earnings. We remain committed to returning at least 40% of net earnings to shareholders on an annual basis. 
All of this is underpinned by our strong balance sheet and investment-grade credit profile. We ended the quarter with approximately $3.6 billion in cash and liquidity of $4.3 billion. Total debt as a percentage of capital was 23%, and our credit ratings remain the highest of any North American steel producer. Looking ahead, we expect our CapEx to decline further in 2027, extending the step down from peak spending in '24 and '25. We'll share more detail on our 2027 capital allocation plans on our year-end call in January.
Turning to our fourth quarter outlook. We expect consolidated earnings to be in line with or modestly higher than the third quarter results. In steel mills, we expect stable earnings as higher average pricing across all product groups is offset by seasonally lower volumes and higher costs. The cost increase reflects lower fixed cost absorption and higher start-up spending at West Virginia as we add teammates and prepare to ramp production. In steel products, higher pricing is expected to offset the impact of lower volumes, resulting in stable earnings for the segment. In raw materials, we expect slightly lower earnings, primarily due to lower realized DRI pricing. Finally, we expect to benefit from lower intersegment profit eliminations that should reduce corporate and elimination expense relative to the third quarter.
And as 2026 draws to a close, we're excited about Nucor's earnings prospects for 2027. Healthy durable demand across key end markets, another step-up in contributions from new growth projects and supportive federal policy, all position us for another strong year. And with the broadest range of capabilities in the North American steel market, we're confident the Nucor team will deliver on that opportunity for our customers and shareholders. 
And with that, we'd like to hear from you and answer any questions you may have. Operator, please open the line for questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Nick Cash with Goldman Sachs & Co.

**Nicklaus Cash** (Analysts):
The first question I have is, you've been running at record shipment levels this year and suggesting it will be closer to the 10% range, driven by strength in demand over the past few quarters as well as backlog visibility. I just wanted to know, as you think into '27, how much further organic volume growth do you think Nucor's existing system can generate before considering contribution from West Virginia? And then which end markets give you the most confidence in another year of growth?

**Leon Topalian** (Executives):
Nick, it's Leon. I'll kick us off, and I want to begin with something I shared in the opening. Nucor has just come through the safest summer ever. And if we look back at our history, the months of June, July and August have historically been the most dangerous and the most opportunity for injuries across our entire enterprise. Our team set out a very audacious goal to target no injuries for those 3 months. And while we didn't meet that, we ended up with the safest 3 months in the history of Nucor and now are putting those efforts towards the safest fall. The thing to really remember in all of that is every one of those numbers that we track has a name, every name has a family, and every family deserves to be complete. Our greatest responsibility as leaders in this company is to the men and women of this amazing company of ours. And so thank you, team, for what you do and how you take care of our customers and for working safe each and every day.
And Nick, as you talk, look, as we came off the highs of '21 and '22, '23 was an okay year. '24 and '25 were very tepid, but look, our investment strategies, our capital allocation philosophy has been to invest for the long term. And so over the last 6.5 years, you've seen Nucor deploy about $19 billion worth of capital, half in organic growth and the other half in M&A. And so it's the ultimate strategy of playing to where the puck is going to be, not where it's at, understanding our customer demand, understanding the capability sets that are needed by our customers and building and creating those opportunities to win. And that is exactly what you're seeing Nucor do today: executing on an incredibly strategic plan to grow the core, expand beyond and live our culture. And so we've had the best quarter in 3 years. We're on the track to have the safest year in all of our entire history. 
'26 is shaping up to be the third best financial year in the history of our company, and we fully expect that '27 will be even stronger. But where is that coming from? And the end market probably that gets more attention in the entire economy is data centers. And while that's a major part in some of our product groups, it represents about 15%, 1-5 percent, of our entire backlog and as an enterprise. But it's a strong end market, but so is chips and technology and hardware, natural gas and gas power plants, LNG export terminals, nuclear, utilities, pharma, heavy equipment is coming back in gangbusters, shipbuilding, military and defense spending, appliance and HVAC.
And so I would tell you, in my 31 years in Nucor, Nick, we are seeing -- I am seeing early, the strongest demand environment across the breadth of Nucor's products, couple that with the investments that we've made in West Virginia, Brandenburg, Lexington, our micro mill in Lexington, Kingman, Arizona, Crawfordsville's paint line, Berkeley's galvanizing line and Brandenburg's plate mill are all now firing where, again, as Steve mentioned just a minute ago, West Virginia will fully commission this year and begin its full ramp in 2027. We are at the tip of the spear of the greatest economic growth in our nation, and I couldn't be more optimistic about what 2027 and beyond is going to bring. 
Finally, I would tell you with the last part of all of that, as that CapEx unwinds of our spend, into 2027, it skyrockets the free cash flow on top of the margins that we're earning, on top of the contributions that the new investments are already having and will continue to ramp into '27. It means we're fueled for growth, disciplined growth, just like we have over the last 6 years. That money is not burning a hole in our pocket, and if we don't have a great use for it, you're going to get it back. 
Over the last 16 years, we've returned nearly $15 billion to our shareholders through dividends or share buybacks, and we will continue to focus on that. However, I can tell you there are massive areas of growth for our company that we're targeting now, mostly in the Expand Beyond categories. But we are just getting warmed up. I couldn't be more optimistic about 2027 and beyond and the future of Nucor.

**Nicklaus Cash** (Analysts):
That is all really fantastic color. I really appreciate it. And then just one quick follow-up. I mean you mentioned, just on the cost side, costs were a little bit higher than expected. I think mills' margins were a little bit lighter than expected, acknowledging the $130 million tailwind from last quarter. Could you provide any further color on any inflationary pressures you might be experiencing? I know you mentioned some lower fixed cost absorption, but any other impacts experienced in the quarter? And then for the 4Q guide of flat earnings, can you provide any additional color on how these impacts -- or how these costs could impact margin trajectory in the year-end?

**Jack Sullivan** (Executives):
Yes, Nick, this is Jack. You're right, conversion costs did tick up some in Q3, but I think we need to put a few things into perspective here. Nucor's EBITDA margin expanded to over 20%, and that's our highest level in the past 3 years. So we continue to see margin expansion even with some of that conversion cost per ton creep. But in terms of specifics and where we saw that, I'd point you to certain consumables, freight, certainly energy and just some other services. But keep in mind, when you're running at high utilization rates, particularly in hot demand environments like we're seeing right now, you do tend to see some costs creep up just to keep operations running. Maybe that's overtime pay or some higher energy costs when, in softer markets, we may have chosen to curtail in higher energy cost environments. 
But -- and you pointed out correctly, we also didn't benefit from the tariff refunds that occurred in Q2. The other thing unique to Q3, when you're comparing it to Q2, we did have more planned outages in the quarter. And of course, that led to some lower fixed cost absorption. So I'd say -- your last question about looking ahead to Q4, I think you could expect a modest uptick in conversion costs Q-over-Q. And again, we do have some outages in Q4. We've got -- we've pointed to some gradual increase in preoperating start-up costs as we get West Virginia closer to ramp up. And yes, those would be the -- I think those would be the things I'd point to.

**Operator** (Operator):
Your next question comes from the line of Bill Peterson with JPMorgan.

**William Peterson** (Analysts):
Congrats on the quarter. I would like to unpack the shipment guide in 4Q. You're still planning on being towards the high end of the range, which would be like 10% year-on-year growth. But I guess if you run it through, it would imply around down 10% quarter-on-quarter, which would be more like 2021, 2022 as compared to the last few years, which were below that in terms of seasonality. I believe you have 2 less shipping days. Are you taking into account other things like holidays and maybe you can characterize how much downtime you're expecting? Or just trying to get a sense, can there be upside to this number?

**Jack Sullivan** (Executives):
Yes. Bill, it's Jack. All good questions. You're right, we do have 2 fewer fiscal days in Q4 compared to Q3, 89 versus 91. But also, to your point, there are 4 additional nonshipping days really just due to Q4 holidays when you think of Veterans Day, Thanksgiving, a few days around Christmas Eve and New Year's. So in aggregate, you're talking 5 or 6 fewer days of shipping compared to the prior quarter, plus the added risk of some winter weather in certain regions.
Q4 planned outages, I just mentioned, some of those outages are at our largest mills. And so planned downtime relative to Q3 actually has a few more days. So keep that in mind. But I think it's also important to recognize we're coming into Q4 off of record high Q3 shipment quarter. So I think sometimes it's easier to ship through outage season during softer markets, a little bit harder to do so when the mills are already operating at such a high level. There's just less slack in the system. But I think if you looked historically, quarterly shipments, Q3 to Q4 have trended down about 7%. And so that may be a useful planning assumption as you're looking to fine-tune your models. 
I think the silver lining here, though, Bill, is we've guided you to steel mills earnings having relatively flat quarter-over-quarter. And really, that's just for all the obvious reasons, we're going to see some volume softness due to seasonality and the outages, but stronger pricing outlook sort of neutralizes that impact. But rest assured, our goal is to ship every ton possible.

**William Peterson** (Analysts):
Yes. No, that's a terrific color. Earlier, I think you said that your data center was something around 15%. I'm not sure if that's a mill statement or a product statement, but I'm trying to get a sense for how big that opportunity, I guess, is for you as we think about 2026, and do you expect that to grow? And then the second one you called out was the border wall, and you characterized it as tons per mile. I was trying to figure out how much border wall needs to get built, but I'd like to get a sense, too, on how you see the border wall opportunity this year and also for next year. Would you expect that to grow again?

**Leon Topalian** (Executives):
Yes, Bill, I'll touch on, and if you can remember now, I got the second part of your question. The first part was on data centers, right? Look, if we step back, most of the forecasts and analysts are talking massive numbers, multitrillion dollars worth of spend over the next 5, 6, 7 years. And so Nucor's entrance into this isn't like weeks or months old. This is something going back 2 or 3 years that we have been, again, readying ourselves to be where the puck is going to be at.
And so today, with the acquisitions of Southwest Data Products, our Nucor Warehouse Systems, our capability set in our buildings, plate, structural, tube group, all are now combining where today, Nucor can make or supply roughly 95% of all the steel required inside and outside of a data center today. So we are really, really capable of providing most of what the hyperscalers need today. Our relationship build with them over the last 4, 5, 6 years has been incredible. There's a high level of trust there. We earn a lot of that business. And so to your question, do we anticipate that growing into 2027? Yes. 
And again, as we think about growth and fueling Nucor's Expand Beyond growth, you can expect that some of those areas of growth will be in that space and the continued build-out of our data center offering to our customers. As we get to the border wall, I'll ask John Hollatz maybe to comment on that. It's been a lightning rod for us. And again, another end market that we've been really very well prepared and capable to supply that need. But John, maybe giving some framing around the volumes.

**John Hollatz** (Executives):
Bill, on the border wall, we estimate there's about 1,400 miles of new wall to be built. That's primary and secondary wall. And there's around 1,500 tons of steel in there per mile. And we have been shipping thousands of tons every week to the border. You can see it in the increased volumes in our tubular group, and that's going to continue all the way through 2027 and well into 2028. And again, we're the only company with the raw materials, the sheet supply, the tube capacity and the logistics team to keep up with the demand for the border. And for the tube group, it's not just border. 
On top of that, you've got a really strong demand for structural on the HSS side. We're seeing incredible performance from our conduit team. Our sprinkler pipe team is having a great year. And all of that has played a role in leading to our steel products group having the best quarter on the earnings side that we've had since the beginning of 2024. So we see a really good outlook well past the end of '26 and into '27 for the border fence.

**William Peterson** (Analysts):
Congrats again.

**Leon Topalian** (Executives):
Thank you, Bill.

**Operator** (Operator):
Your next question comes from the line of Lawson Winder with BofA Securities.

**Lawson Winder** (Analysts):
Nice results. If I could ask on your comments around merchant bar. Could you just discuss a bit more as to what end markets are primarily driving that? And then how do the market dynamics vary regionally on merchant bar? And then is there any merchant bar replacement of rebar capacity at the current moment or to any extent at all?

**Leon Topalian** (Executives):
Say that last part of your question again, Lawson.

**Lawson Winder** (Analysts):
Just in terms of the strength in shipments from merchant bar, is that causing any displacement of rebar shipping capacity?

**Leon Topalian** (Executives):
Look, I'm going to ask Randy Spicer to jump in on this. But just a bit of framing. Our rebar strategy and our -- that end market has been incredibly strong for us. Our long products groups are some of the most profitable and have been through the entire cycle. There's a lot of questions, right, of the flattening of this cost curve, but our ability to maintain margins, our ability and how our teams executed in remaining the low-cost producer, building these facilities where there's a high level of scrap inventory as well as the customers that are in proximity gives Nucor a unique, differentiated advantage in this marketplace.
And quite frankly, ADC is growing. And so again, I remain very optimistic knowing that there's some competitors coming into the space, and that will continue. But we've been in this business for 60 years now. We know this market incredibly well. Our teams are executing at a high level. But Randy, why don't you share a little more on what we're doing with merchant bar in particular and that growth?

**Randy Spicer** (Executives):
Yes. Thanks, Leon. Lawson, thank you for the question. Yes, certainly seeing tremendous growth in both, quite frankly, merchant and rebar, as evidenced by the record shipments that we've seen that's in place. What I would tell you specifically around merchant bar is it's got exposure to some of the hottest markets that we've seen right now, specifically, as Leon had just talked about, data centers. We're in the middle of what we call the AI Super Bowl. The hyperscalers have committed an enormous amount of capital to these data center build-outs. And those structures require these larger sections that we're able to produce at Nucor, and that's showing up directly in our order book. As you can look and see, we're at record levels to be able to take advantage of both here in '26 as well as the growth as we go forward into '27.
With that, you're also spot on as you see the margins increase in that space, you're also seeing some of the rebar producers out there, right, that are capable of making flexible products, of which Nucor is one of the largest in that space, that you're actually able to move into the merchant bar space as well. So with that growth, we've continued to see strong performance, and we would expect to see that as we go forward into future years.

**Lawson Winder** (Analysts):
Okay. That's very helpful. And then maybe just to put a finer point on my last question. I mean given the way your capacity is kind of set up between Kankakee and Missouri, is there some displacement of rebar as a result of that merchant bar capacity, i.e., is the rebar market in the U.S. getting tighter as a result of what you're seeing in merchant bar?

**Leon Topalian** (Executives):
Well, look, you're seeing ADC actually grow. If you look back a year or 2, it's at roughly 9 million, 9.5 million tons. We're predicting that to be upwards of 10.5 million or possibly 11 million. And so the market is growing. And so that just bodes very well, again, for our capability set and where we're going. But very specifically to your displacement question. One of the unique advantages in what Randy and his groups have done, again, this is over years, is when we put Frostproof and Sedalia in, our first 2 micro mills, we looked at the overall mix and how do we supply that. 
We took Darlington from rebar, some MBQ into no more rebar and all MBQ and now higher end SBQ and wire rod. And so Darlington's capabilities has expanded tremendously. Kankakee's investment in their growth, and they've moved out of a lot of rebar into heavy MBQ and beyond. And so again, the breadth of our footprint enables us to shift and modify where we meet the geographic needs and the capability sets that, again, our customers need from us in the regions where we're located. So yes, there's been a lot of that that's happened, Lawson, over the last 5, 6, 7 years that really kind of catapulted with the investment of the rod mill at Darlington and now continues on.

**Operator** (Operator):
Your next question comes from the line of Tristan Gresser with BNP Paribas.

**Tristan Gresser** (Analysts):
I have 2. The first one is on your auto strategy. You had a slide in your presentation, and I think a couple of years ago, you mentioned your goal to double auto shipments. So could you provide maybe an update tonnage-wise, how much you expect to achieve this year and the next? Also, I was curious if you're -- I don't think you've done this in the past, but are you entering into annual contracts with OEMs? Do you have everything you need from a raw material standpoint, or you need to make some adjustments? And lastly, from a quality perspective, it would be interesting to have your view if you're confident that you can fully replicate the products that customers usually get from an integrated producer. I'll leave it there.

**Leon Topalian** (Executives):
Tristan, I'm going to go ahead and jump in here. And while I'm going to tell you Noah Hanners will answer the question in a minute, I may not leave him anything to answer because I really appreciate the question, and I want to fully blow apart any notion that EAFs do not have the technical and quality capabilities to provide and make exposed automotive panels. It has been the last bastion of the integrated competition. And the only thing they have left, think about it, left in America, there's not a single integrated producer making a long product in America. All EAFs do all of that today. So the last piece of that pie has been the exposed automotive panels. And I'm really pleased to report on behalf of Noah and the entire sheet group that Nucor has been awarded an entire platform with General Motors for exposed automotive sheet.
And you're going to couple that work, that time, that effort, those resources, the process engineering and process and quality control, the PPAPs, all that work is now shifting into West Virginia. So as they begin ramping up, that mill will produce 30% automotive steels capable of making the highest end. So you can fully dismantle any notion that the EAF producers cannot make the most complex, high-quality and exposed pieces of that vehicle. It's over. We're on it. We're doing it, and we're going to continue to do it, and we're going to continue to take that market share away from the integrated producers, period, full stop. So Noah, anything to add on that? I'll leave the rest for you.

**Noah Hanners** (Executives):
I love Leon's energy around this because we're so proud of what our team has accomplished, and we can produce the full suite of what auto demands from us. And I'll tell you, our customers are pumped about doing more business with us. And the capabilities that we're bringing to the market are perfectly timed for meeting their demands. I mean you talk about West Virginia, the first phase of West Virginia is largely volume and proving the mill. And then we get out to 2028, and that's when we'll start to put auto tons through qualifications on West Virginia. So it's coming soon.
The second thing is at Berkeley. We already do a lot of auto out of Berkeley. They were the substrate mill for that qualification Leon just mentioned. They just galvanized their first coil on the new galv line last week, awesome accomplishment from that team, on time, on budget, and we're just really well positioned to take substantial share in the automotive market, continue to grow, exercise our capabilities there. We're at about 10% this year. We'll do about 1 million tons at West Virginia as we're ramped up there. A significant portion of that, probably 10%, goes into auto exposed. So awesome, awesome story about our growth in automotive. Really proud of our team.

**Jack Sullivan** (Executives):
Yes. And the other thing I'd add there, Noah, on automotive, I think a big testament goes to the amount of time and energy and frankly, patience that's taken our team and our investors on helping us along this journey. As Leon mentioned, we are now on a platform. Aspirationally, we'd like to get a bigger chunk of that platform, but starting out with certain parts and look forward to continuing to chip away at that.

**Operator** (Operator):
[Operator Instructions] Your next question comes from the line of Matt Dushkin with Wells Fargo.

**Matthew Dushkin** (Analysts):
So on the data centers that you all said it's 15% of backlog. I just kind of want to unpack what's the breakout of that between your different products? Like how much is structural versus how much is sheet versus downstream? Just any color there would be helpful.

**Leon Topalian** (Executives):
Yes. Look, the 15% is the entire enterprise. And obviously, in the long products, particularly structural, much higher, Matt. It's in the 30% to 35% range. And so those teams continue to operate in one of the strongest demand environment -- well, the strongest demand environment we've ever had. Nucor-Yamato and Berkeley Beam are running rates with backlogs that are unprecedented. We've never seen in the history of those mills, in the 35-year history at NYS. So again, robust doesn't really put justice to the demand drivers fueling that. And a big piece of that for structural is the data centers.

**Stephen Laxton** (Executives):
Matt, maybe if I could just add a little bit there, too. Some of our downstream businesses are seeing a lot of volume from the data center space, too, particularly Vulcraft, but also it might surprise you, our metal buildings group has picked up a fair amount of volume as well. And really that's just a testament to our team's ability, the breadth of the portfolio and solutions that we offer and the range of end market capabilities we have and the willingness to work with customers to find the right outcome.
So it's really -- Leon correctly highlighted, it's pronounced in beams. That's not surprising to anybody. Randy highlighted earlier, it's having an impact on MBQ and bar and of course, in Vulcraft, you wouldn't be surprised. But some of the other areas, because of Nucor's breadth, we're seeing volume pick up as well.

**Matthew Dushkin** (Analysts):
That's all super helpful. And then I just want to pivot to piggyback on Tristan's question. And sorry, when you all cut off, you all may have been answering this. But just curious about the commercial approach to the exposed auto qualifications. How are you all thinking about the contract structure for that, whether it's fixed, maybe you take it with the spot market, which I assume would be tough? But just curious on that.

**Leon Topalian** (Executives):
Matt, where did we cut off? What did you hear? How far into the answer before you lost us?

**Matthew Dushkin** (Analysts):
We got to how you all won with GM, and then it kind of just cut off a little bit after that, so I didn't...

**Leon Topalian** (Executives):
Okay. Well, look, it gives me a wonderful opportunity to make sure everyone understands the dispelling nature that EAF producers cannot make the most stringent grades of exposed automotive. Again, we're on the General Motors platform for that. The Berkeley start-up of their second galv line is in play, and West Virginia will continue to ramp. And look, this is also not a new story. While it's the first platform we've been given, we've been in the automotive space for more than 10 years, right? So we've learned and worked with the major OEMs in this country for a long time, not just GM, but Ford and BMW and Mercedes and many others. And I'll let Noah speak more to that.
But look, with General Motors, we've had a great relationship. We're 6-time recipient of the Supplier of the Year Award with them. And so we understand their needs. We've worked closely with them. Our engineers, metallurgists and commercial teams have built incredible relationships. Our technical teams in Detroit provide an incredible avenue for those OEMs to understand how we're doing it and for us to link in those PPAPs and process control side to have that full offering. And so Noah, I'll let you answer maybe if you want to add any more detail on the commercial and how we're thinking about that. I just wanted to provide the backdrop that these are not new orders or new customers for us. It's a new platform, new grades, but not new relationships.

**Noah Hanners** (Executives):
Yes. Thanks for the question, Matt. Sorry, you missed my answer the first time. I assure you it was brilliant. But to give you more color, I guess, specifically to the contract side, it's one thing to have the capabilities, and we're at a point where we're very confident in our capabilities. It's built on decades of work by our team to learn how to make the grades and meet our customers' requirements. And this proof of our ability to get on platform that we talked about here is really a testament to that.
But then getting set up contractually and qualified takes a number of years. And we have a leg up on our growth because we have an auto exposed galv line in Mexico, where we do extensive automotive of a variety of different grades that will match up nicely with the suite of capabilities at Berkeley and at West Virginia. And then we have a broad book of capabilities and qualifications that we've worked through. So our team is very experienced with the qualification process, and we're able to lean into those qualifications at some of our other locations to really set West Virginia up for success. 
West Virginia is by volume our biggest growth opportunity for automotive. We'll do 1 million tons of automotive out of West Virginia. About 100,000 of that will eventually be auto exposed. So we're able to lean into that know-how across our team and those other resources to start to fast track those qualifications.

**Matthew Dushkin** (Analysts):
I think the answer is probably even better the second time.

**Operator** (Operator):
Your next question comes from the line of Richard Garchitorena with Barclays.

**Richard Garchitorena** (Analysts):
If I could just ask quickly in terms of pricing, obviously, the market has been able to withstand pricing moving higher. Can you provide some color in terms of what you're hearing from customers? And when it comes to fixed price contracts resetting next year, how should we think about that impacting your results?

**Leon Topalian** (Executives):
Richard, I want to make sure I understand the question. Are you asking how pricing in the structural side moving into '27 is impacting our customers?

**Richard Garchitorena** (Analysts):
No. [ Do you have any color ] on the market? Yes. How the market -- yes, yes.

**Noah Hanners** (Executives):
Richard, this is Noah. Let me just step in and talk maybe about where we are with our sheet contracts and how we work through resetting those contracts as we step into 2027. And we come into this market, you've heard the demand drivers we've talked about, really robust demand picture across the sheet group and an expectation of continued growth in demand. And then we're bringing these new capabilities to the fold as well.
So West Virginia will start to come online, Berkeley. Indiana just painted their first coil. So our goal through contract season is to match up these new capabilities, this really strong demand picture to meet the needs of especially our long-term customers. And we've never been, I would tell you, more deliberate about that plan. And we have a strategy that feels good because it's very coherent across our mills. So some mills are going to have to give up volume to get West Virginia online, they're able to go out and we're able to back those replacement tons up contractually. So I think we have a very coherent plan in the face of a lot of strong demand picture out there. 
To maybe talk about the terms, we're not going to get into specifics, but they're significantly better as we step into 2027. We've improved the overall quality of the agreements, lower discounts, higher extras, and our volume variances are tighter than they were in 2026. If you look back historically, we've been about 80% to 85% contracted. We'll be a little heavier than that this year. And overall, I think our commercial team has done an outstanding job positioning us for 2027.

**Jack Sullivan** (Executives):
And Tristan (sic) [ Richard ], you had also asked about the composition of our contracts that are fixed that may be resetting at a different price as we go into 2027. Nucor really doesn't have a very large percentage of contracts that are fixed.

**Noah Hanners** (Executives):
Yes, the majority of our fixed are going to be in auto, and I would call that just loosely 5% to maybe it's 7% of our fixed contracts, but the majority will reset at year-end.

**John Hollatz** (Executives):
It's 5% to 7% of sheet.

**Noah Hanners** (Executives):
Of sheet, thank you. Thanks.

**Jack Sullivan** (Executives):
So very low single-digit percentage of sheet overall.

**Operator** (Operator):
Your next question comes from the line of Tristan Gresser with BNP Paribas.

**Tristan Gresser** (Analysts):
It's me again. Sorry, I got disconnected. I just have another question on the strong performance of the steel products division. If you could dive a little bit into that, the main driver behind it, maybe the contribution of towers, panels, doors, anything standing out or anything really behind the strong performance?
And also when we look past that, looking into Q4 and Q1 next year, should we expect some similar scale of ASP increase? Or would you expect some moderation of that? And even with lower volumes, how do you think about margins? Are they going to continue to expand every quarter? Or you're going to feel a bit the pressure from those higher substrate costs in general?

**Leon Topalian** (Executives):
Well, look, that's a lot to unpack here, and I'm going to let John Hollatz take most of it. But look, as we sort of answered earlier as well, Tristan, as we came out of '25 into '26, the demand environment has continued to become more and more and more robust. And with that, pricing is flowing through the enterprise as well. So you're seeing higher realized pricing in our downstream products groups that are now hitting the balance sheet and will continue to do so well into 2027. Again, at a very high level, the products group now in Nucor is such a wide and diverse set of businesses and generates great returns. But again, there's a lot of different business segments in that. So John, why don't you just walk through to Tristan's question, some of those highlights and what we're most excited about as we head into '27?

**John Hollatz** (Executives):
Yes. Tristan, I appreciate that question and the recognition that our steel products earnings were the best earnings in Q3 that we've had since the beginning of 2024. And this is not just one specific product. This is a variety of different products that are contributing to this. We talked earlier about the tubular group and their performance related to border wall overall construction. On the Vulcraft joist and deck side, we had noted previously that we were seeing higher prices and new order entry, and that is now being realized in our earnings. And new orders continue to exceed our current backlog pricing. And that backlog carries us well into 2027. 
It was mentioned earlier, our buildings group and their participation in the data center market. They had a really strong third quarter. It's setting the stage for a great year in 2027. And again, we're the only company, as Steve mentioned, that has the ability to support data centers through conventional construction with joist and deck and structural steel or the alternative of supplying a pre-engineered metal building. And then I also want to recognize our insulated panel group, one of our Expand Beyond businesses that had record earnings in the third quarter, and that, again, will carry us well into 2027. Overall, our backlogs are up about 25%. Pricing continues to improve, and it's going to -- we're going to have a good Q4 and a really strong 2027.

**Leon Topalian** (Executives):
Maybe the other thing, too, and you mentioned it, Tristan, but look, we're excited -- we love our door business. We love what C.H.I. and Rytec are doing. But think about the build-out, what we've done in Towers, right? We've been pretty public that we made some runs in the M&A side that didn't work out. We love the space and have for a lot of years. And so we made the decision a couple of years ago that we're going to do it organically. We bought a small company in Summit to kind of begin and get some in-house knowledge. That now has expanded to 3 greenfield towers plants, 2 of which are online and the third that will be up and running by mid next year. But think about what -- and I think it was Steve's opening comments, we -- that team is already qualified at 30 different utilities. 
So not unlike the robust excitement and demand picture from OEMs into the sheet group to provide the higher end and automotive exposed grades, we're finding and feeling the very same relationship build and networking within the utility side to grow that space. And so the order books are getting filled very, very quickly. And again, it's a space that not only do we feel really well poised to provide, but the build-out of those facilities is so automated. We truly believe we're going to have a cost -- significant cost advantage in a differentiated position in that market. 
So again, I'm really proud of what the downstream products group's teams are doing across the board and including the Expand Beyond businesses. So I appreciate the question, Tristan.

**Operator** (Operator):
This concludes our Q&A portion. I will now turn the call back to Leon Topalian, Chair and CEO, for closing remarks.

**Leon Topalian** (Executives):
Well, team, as we close, I want to thank our 33,000 teammates for another strong quarter and for your continued unwavering commitment to our most important value: the health, safety and well-being of every one of our team members. Thank you to our customers for the place -- trust you place in us with each and every order. We want to continue to work hard and earn your business every day. And lastly, to our shareholders, thank you for trusting us with your valuable shareholder capital. '26 is shaping up to be a really, really good year, and we believe '27 will be even stronger. Our best days are definitely in front of us. Thank you for your interest in Nucor, and have a great day.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NUE_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜Stephen Laxton｜guidance：2026 鋼廠出貨成長預期調至先前 5%–10% 區間的高端（原話："higher end of our previously suggested 5% to 10% range"）
- 2026-07-28｜Jack Sullivan｜guidance：第三季整體獲利預期較高（原話："We expect higher consolidated earnings."）
- 2026-07-28｜Jack Sullivan｜guidance：Q3 鋼廠不再有原料退款貢獻，但金屬價差擴大（原話："we do not expect any further cash refunds to materially"）
- 2026-07-28｜Jack Sullivan｜guidance：Q3 鋼廠獲利預期較高（排除退款後）（原話："Even without that benefit, we expect higher third quarter"）
- 2026-07-28｜Jack Sullivan｜guidance：Q3 原料部門獲利預期下降（原話："In Raw Materials, we expect lower earnings"）
- 2026-07-28｜Jack Sullivan｜guidance：2026 資本支出維持 25 億美元（原話："Earlier this year, we guided to $2.5 billion for 2026,"）
- 2026-07-28｜Stephen Laxton｜guidance：西維吉尼亞新薄板廠 2027 年初開始商業出貨爬坡（原話："commercial shipments begin to ramp in early 2027."）
- 2026-07-28｜Noah Hanners｜guidance：西維吉尼亞廠第一年底稼動率約 50%（原話："we expect to be at about 50% utilization by the end of"）
- 2026-07-28｜Stephen Laxton｜guidance：2026 全產品美國鋼材需求約成長 2%（原話："an estimate somewhere around 2% up on demand overall."）
- 2026-07-28｜Jack Sullivan｜guidance：下半年營運資金預期趨緩，可能小幅釋出現金（原話："likely expect some moderation in working capital"）
- 2026-07-28｜Jack Sullivan｜guidance：自由現金流預期隨專案上線、資本支出降低而上升（原話："inflect higher as these growth projects come online"）
- 2026-07-28｜Jack Sullivan｜margin：Q2 鋼廠部門稅前獲利季增逾 35%（原話："an increase of more than 35% from the prior quarter"）
- 2026-07-28｜Jack Sullivan｜margin：Q2 鋼廠數字含 1.3 億美元前期原料採購退款（主要生鐵）（原話："$130 million of cash refunds associated with prior period"）
- 2026-07-28｜Jack Sullivan｜margin：Q2 EPS 5.04 美元含 Helion 投資非現金利益 0.20 美元，調整後 4.84（原話："noncash benefit of $0.20 related to an increase in the value"）
- 2026-07-28｜Jack Sullivan｜margin：Q2 EPS 高於自家中點財測 0.29 美元（原話："exceeding the midpoint of our guidance range by $0.29."）
- 2026-07-28｜Jack Sullivan｜margin：DRI 內部轉撥價隨生鐵價格上升而提高，推升原料部門（原話："benefited from a higher transfer price"）
- 2026-07-28｜Jack Sullivan｜margin：開辦與啟動成本 Q2 為 1.2 億美元，預期 2026 下半年與 2027 持續偏高（原話："these costs to remain elevated through the rest of 2026"）
- 2026-07-28｜Stephen Laxton｜margin：鋼製品部門預期隨實現價格上升而擴大利潤率（原話："further margin expansion over time"）
- 2026-07-28｜Jack Sullivan｜commitment：承諾每年至少將淨利 40% 回饋股東（原話："we remain committed to returning at least 40% of net"）
- 2026-07-28｜Leon Topalian｜commitment：塔架與結構事業先前承諾貢獻 1.5 億美元 EBITDA（原話："we were going to generate $150 million of EBITDA"）
- 2026-07-28｜Leon Topalian｜commitment：管理層稱 1.5 億美元的數字可能偏低（原話："I hope that's a really low number."）
- 2026-07-28｜Leon Topalian｜capital_allocation：現金用途主攻 Expand Beyond（下游、巨型趨勢相關）（原話："it's going to go into the Expand Beyond bucket."）
- 2026-07-28｜Leon Topalian｜capital_allocation：併購門檻：報酬須遠高於資金成本，否則回饋股東（原話："if not double our cost to capital, we're just not going to"）
- 2026-07-28｜Leon Topalian｜capital_allocation：2026 資本支出約 60% 用於成長專案（原話："$2.5 billion for the year, with about 60% of"）
- 2026-07-28｜Leon Topalian｜competition：製成鋼品進口年減 25%，歸因於 232 條款強化與反傾銷/反補貼稅（原話："finished steel imports are down 25% year-over-year"）
- 2026-07-28｜Leon Topalian｜competition：Q2 H 型鋼進口季增 50 個百分點以上（原話："spike of about 50-plus percentage points in beams"）
- 2026-07-28｜Leon Topalian｜competition：管理層稱進口上升並非價差驅動（原話："it's not a pricing delta that's driving that."）
- 2026-07-28｜Noah Hanners｜competition：薄板進口 2024 年 900 萬噸，今年預估約 450 萬噸（原話："we see probably 4.5 million tons this year."）
- 2026-07-28｜Noah Hanners｜competition：CSP 透明定價被稱為改變市場波動（原話："our discipline and our approach around CSP"）
- 2026-07-28｜Noah Hanners｜customer：客戶採購反映供需而非投機（原話："we do not see the speculation we typically would have seen"）
- 2026-07-28｜Noah Hanners｜customer：服務中心需求回升（原話："Service center shipments were up 10% in June"）
- 2026-07-28｜John Hollatz｜customer：邊境圍牆需求每週出貨數千噸，預期延續至 2028（原話："thousands of tons every week to multiple locations"）
- 2026-07-28｜Brad Ford｜product：Brandenburg 約三分之一出貨為過去 Nucor 板材無法供應的品級與尺寸（原話："Nearly 1/3 of the shipments out of Brandenburg in Q2"）
- 2026-07-28｜Brad Ford｜product：API 管線鋼板已完成認證並出貨（原話："we're fully qualified, we're producing that and shipping"）
- 2026-07-28｜Leon Topalian｜risk：川普政府選擇不續約 USMCA，除非有修改，觸發年度檢討（原話："opted not to renew the USMCA trade agreement"）
- 2026-07-28｜Jack Sullivan｜risk：Q3 原料部門成本風險：中東球團產能閒置推高鐵礦成本（原話："elevated iron ore costs due to the idling of some pellet"）
- 2026-07-28｜Leon Topalian｜risk：西維吉尼亞廠 2027 年被定位為爬坡年，管理層不確定是否貢獻獲利（原話："'27 will be that ramp-up year. I'm not sure"）
- 2026-07-28｜Stephen Laxton｜guidance：全年需求成長維持約 2%（分析師稱上季為 2%–2.5%）（原話："we're at about 2% growth probably this year"）

### 問答異常語氣（迴避／改口／保留）
- NUE_Q2_2026_Earnings_Call_20260728.md｜問：Carlos de Alba 追問 DRI 轉撥價參考哪個生鐵指數及落後多久｜答法：Al Behr 稱有落後但不願量化，也不指明指數，僅重複「受生鐵價格影響」
- NUE_Q2_2026_Earnings_Call_20260728.md｜問：Timna Tanners 要求量化新專案對 Q3/Q4 的貢獻及是否抵銷季節性｜答法：Leon 逐項講專案狀態並稱 1.5 億美元可能偏低，未給 Q3/Q4 量化數字
- NUE_Q2_2026_Earnings_Call_20260728.md｜問：Lawson Winder 問 Brandenburg 稼動率 75% 模型假設是否合理｜答法：Brad Ford 未確認或否認 75%，只說數字會持續「creep up」
- NUE_Q2_2026_Earnings_Call_20260728.md｜問：Nick Cash 問 Q2 薄板出貨季減是否為訂單疲弱、停機或進口回流，及長材市占｜答法：Noah 以生產創紀錄與庫存出貨作答，未直接回應訂單簿；Randy Spicer 未直接說明長材市占原因
- NUE_Q2_2026_Earnings_Call_20260728.md｜問：Bill Peterson 問 Q4 季節性與邊境圍牆 2028 出貨量及市占｜答法：Laxton 只說有季節性、相對下降，未給數字；Hollatz 未給圍牆噸數或市占

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
{"date":"20260525","verdict":"B 觀望偏進場；等回測 $180-200 (W52 + BB 中軌) 或 WV mill 2027 commissioning + Section 232 維持 50% 確認後分批","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Section 232 50% tariff 維持，美國鋼鐵 floor pricing 結構性墊高 $200-300/ton","columns":{"2Y 驗證點":"2026-2028 Trump 任內維持 50%；HRC spot 維持 &gt; $750/ton 多數時間","5Y 驗證點":"2029-2030 即使政權變動仍維持 25%+ tariff（兩黨共識某種形式）","10Y 驗證點":"2031-2035 美國本土鋼鐵生產 share 維持 90%+，imports &lt; 10%","具體門檻":"HRC 月均 &gt; $750/ton 6 月以上","信息來源":"White House Fact Sheets + AISI monthly","漂移觸發":"連 2 季 HRC 月均 &lt; $700 → 削弱"}},{"id":"H2","text":"WV 新產能成功 ramp + data center 段持續加碼","columns":{"2Y 驗證點":"2027 WV 50% utilization；data center steel revenue +30% YoY","5Y 驗證點":"2028-2029 WV 100% utilization；data center vertical 達 $3-5B 年化 revenue","10Y 驗證點":"2030+ data center vertical 達 $5-10B + Nucor 維持 95% market share","具體門檻":"WV 2028 末 utilization ≥ 80%","信息來源":"Nucor 法說 + Investor Day","漂移觸發":"連 2 quarter WV utilization 進度 &lt; plan 20% → 削弱"}},{"id":"H3","text":"估值倍數維持合理 cyclical 區間：Fwd PE 12-16x normalized","columns":{"2Y 驗證點":"2026-2027 Fwd PE 13-17x；EPS &gt; $13","5Y 驗證點":"2028-2029 Fwd PE 13-15x；EPS $14-18 normalized","10Y 驗證點":"2030+ 進入「premium cyclical」估值區 14-18x","具體門檻":"Fwd PE 不超 18x 不低於 10x","信息來源":"sell-side + Bloomberg","漂移觸發":"連 2 quarter EPS 共識下修 &gt; 15% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"2028 大選政策變動：新政府降至 25% 或廢除 Section 232","columns":{"對應假設":"H1 / H3","時間尺度":"🐢 長期（2028+）","監測指標":"2028 大選結果；新政府 trade rep 公開立場","警戒閾值":"新政府 100 天內公開降至 25% → 砍倉 30%；半年公開廢除 → 大砍 50%"}},{"id":"R2","text":"HRC spot price 重設：cyclical softening 或 capacity oversupply","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（2026-2027）","監測指標":"AISI 月度 HRC index；mill shipments YoY；competitor capacity additions","警戒閾值":"HRC 連 6 週 &lt; $700/ton OR mill shipments YoY -5% 連 3 月 → 連 2 季觸發即減倉 1/3"}},{"id":"R3","text":"data center demand plateau：AI capex 不如預期","columns":{"對應假設":"H2","時間尺度":"🔥 中期（2027-2028）","監測指標":"hyperscaler capex guidance；data center construction start data","警戒閾值":"4 大 hyperscaler 連 2Q 下修 capex guide &gt; 15% → 連 4 季觸發大砍 thesis"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":232.0,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NUE_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
