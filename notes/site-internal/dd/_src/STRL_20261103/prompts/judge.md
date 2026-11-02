你是 stock-analyst **v20 判斷 agent**，標的 STRL（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"STRL","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STRL_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STRL_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":1563.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿 Q3 2026 earnings release（SEC 8-K Ex.99.1）"},"note":"未查證"},{"id":"f_kpi1_non_gaap_adjusted_operat","label":"Non-GAAP (adjusted) operating income / margin","value":332.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m（利益率 21.3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿 non-GAAP 表 Total Adjusted Operating Income"},"note":"未查證"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":306.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m（利益率 19.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿；10-Q strl-20260930"},"note":"未查證"},{"id":"f_kpi5_combined_backlog","label":"Combined backlog","value":6140,"period":"Q3 2026（2026-09-30，公告於 2026-10-28）","unit":"USD m（signed 4,140＋unsigned awards 2,000）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿；combined +78% YoY、signed +61% YoY；Q3 book-to-burn 0.9x（backlog）／1.4x（combined）"},"note":"不適用"},{"id":"f_kpi6_2026","label":"2026 全年指引（上調）","value":"Revenue 4.63–4.73B；GAAP EPS 19.16–19.42；adj. EPS 21.70–21.96","period":"Q3 2026 新聞稿（公告於 2026-10-28）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026 新聞稿（公告於 2026-10-28）","citation":"公司新聞稿；另 EBITDA 905–916m、adj. EBITDA 970–981m、net income 596–604m、adj. net income 675–683m；未提供 FCF 指引"},"note":"未查證（yfinance FY1 營收共識 4,688m 為 numbers_extra 舊值，可能含新指引前）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_strl_gross_margin_pct","label":"STRL 毛利率","value":23.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STRL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_strl_operating_margin_pct","label":"STRL 營業利益率","value":18.62,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STRL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_strl_fcf_margin_pct","label":"STRL FCF 利潤率","value":10.93,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STRL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eme_gross_margin_pct","label":"EME 毛利率","value":19.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eme_operating_margin_pct","label":"EME 營業利益率","value":9.88,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eme_fcf_margin_pct","label":"EME FCF 利潤率","value":7.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_gross_margin_pct","label":"FIX 毛利率","value":25.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_operating_margin_pct","label":"FIX 營業利益率","value":16.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_fcf_margin_pct","label":"FIX FCF 利潤率","value":19.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_gross_margin_pct","label":"PWR 毛利率","value":15.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_operating_margin_pct","label":"PWR 營業利益率","value":6.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_fcf_margin_pct","label":"PWR FCF 利潤率","value":8.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mtz_gross_margin_pct","label":"MTZ 毛利率","value":12.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTZ.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mtz_operating_margin_pct","label":"MTZ 營業利益率","value":4.85,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTZ.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mtz_fcf_margin_pct","label":"MTZ FCF 利潤率","value":2.34,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTZ.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_free_cash_flow_ocf_capex","label":"Free cash flow（OCF − capex，公司未報 FCF，自算單季）","value":53.2,"period":"Q3 2026（9M 累計減 H1 累計；季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（9M 累計減 H1 累計；季末 2026-09-30，公告於 2026-10-28）","citation":"自算：9M OCF 427.1 − H1 OCF 328.0 = 99.1；9M capex 115.5 − H1 capex 69.6 = 45.9（公司新聞稿 Q3 與 Q2）"},"note":"未查證"},{"id":"f_kpi4_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":3.7,"period":"Q3 2026（SBC 11.2 ÷ GAAP 營業利益 306.8；公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（SBC 11.2 ÷ GAAP 營業利益 306.8；公告於 2026-10-28）","citation":"公司新聞稿現金流量／調節表，比率自算"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":346.42,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-34.56,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":28.84,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.6,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.03 → 20.15）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.23,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（25.84 → 25.78）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（31.14 → 31.14）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":20.15,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":25.78,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":31.14,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":5.5,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 19.1 → 20.15（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":19.43,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝41.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":41.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":2.45,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝55.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":55.5,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.44,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝53.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":53.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":17.2,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 20.15，分子＝快照價 346.52","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-51.13,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 165.81、現金 216.94（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":30.5,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":10515.56,"period":"2026-11-03","unit":"USD m","basis":"市值 10566.69 ＋ 淨負債 -51.13","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":4688.45,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（4 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":5433.87,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（8 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.24,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 346.38 / W52 504.95 / W104 361.4 / W250 187.97 / W250 13週斜率 2.99%"},{"id":"f_ma_w52","label":"52 週均線","value":504.95,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":361.4,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":187.97,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.99,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 稱公司定位中階市場；若市況轉差，預期小型本地承包商與大型國際營造商會向公司目標中階市場靠攏，可能提高競標壓力並壓低營收成長與利潤率。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm","excerpt":"However, should market conditions become less favorable, we would expect to see a convergence from both the small local contractors and large international construction companies into our targeted mid-level market. This convergence could increase competitive bidding pressure and reduce both revenue growth and margins.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：運輸解決方案（重型公路）競爭激烈，且有更大的國際／全國性公司目前在公司地理市場無顯著據點，但若願意可進入並競爭。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm","excerpt":"a number of international and national companies in the heavy highway construction industry that are larger than we are and that currently do not have a significant presence in our geographic markets, if they so desire, could establish a presence in our geographic markets and compete with us for contracts.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Qz／Nasdaq 文章稱客戶因公司較快較安全交付大型專案而將其帶入新州（相對本地對手），屬競爭優勢敘述，非份額數據。","source":"Qz: can sterling s cross selling strategy unlock bigger ai contracts","url":"https://qz.com/can-sterling-s-cross-selling-strategy-unlock-bigger-ai-contracts","excerpt":null,"as_of":"2026-08-10","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K：2025 年無單一客戶占合併營收逾 10%，但公司常態為最大客戶承建專案，失去任一者可能有重大不利影響；一手文件未提及客戶導入第二供應商或 in-house。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm","excerpt":"In 2025, no individual customer accounted for more than 10% of our consolidated revenues; however we routinely construct projects for our largest customers mentioned above. The loss of any of these customers could have a material adverse effect on our business and financial results.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K：無單一客戶占合併營收逾10%；E-Infrastructure 前四大客戶占該部門營收27%（2024:31%、2023:40%），Building Solutions 前四大45%（36%、42%），Transportation 前四大州DOT 58%。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm","excerpt":"The top four customers in each year, accounted for 27% of the segment’s revenue in 2025, 31% in 2024 and 40% in 2023.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"10-K Note 18：2023-2025 無客戶占合併營收逾10%，2024與2025年底也無客戶占應收帳款逾10%。","source":"SEC EDGAR 10-K FY2025 Note 18","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm","excerpt":"No customers accounted for more than 10% of the Company’s consolidated revenues from continuing operations in 2025, 2024 or 2023. At December 31, 2025 and 2024, there were no customers that accounted for over 10% of the Company’s outstanding contract receivables.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"ABC 2026 estimate: 349,000 net new construction workers needed in 2026 (lower than recent years); ENR frames it as cyclical demand cooling layered on structural workforce limits (retirements, demographics); ABC 2027 projection ~456,000 workers.","source":"ENR 'Construction's Labor Relief Masks Structural Risk as Demand Cools'; ABC via Hardware Retailing","url":"https://www.enr.com/articles/62348-constructions-labor-relief-masks-structural-risk-as-demand-cools","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Linesight Americas report (June 2026): new or expanded supplier capacity may ease supply pressure in 2H 2026 into 2027, though vendor prioritization and production slots remain critical.","source":"Linesight Construction Market Insights Americas, 24 June 2026","url":"https://www.linesight.com/insights/construction-market-insights-construction-industry-trends-and-supply-chain-dynamics-americas/","excerpt":null,"as_of":"2026-06-24","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"STRL raised 2026 guidance to revenue $4.0-4.15B, adj EPS $19.70-20.30; signed backlog $4.33B; growth driven by data center and semiconductor projects; Cantor view that the constraint is capacity not demand; residential remains soft.","source":"Quartr STRL Q2 2026 earnings summary; Nasdaq/Zacks articles","url":"https://quartr.com/events/sterling-infrastructure-inc-strl-q2-2026_on6oHjMG","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"AIA 2026 consensus forecast: nonresidential building spending up ~3% in 2027; data center strong while many traditional sectors flag. Commentary notes caution on 2027 from late-2026 deceleration with multi-year rebound optimism from 2028.","source":"AIA Consensus Construction Forecast; ECM 'Navigating Construction Growth in 2027'","url":"https://www.aia.org/resource-center/consensus-construction-forecast","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261103","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：管理層稱目前無預期會對合併經營結果、財務狀況或現金流造成重大不利影響的未決或可能的法律事項；搜尋三次亦未見 DOJ／FTC／EU 反壟斷調查報導。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm","excerpt":"In the opinion of management, after consultation with legal counsel, there are currently no threatened or pending legal matters that would reasonably be expected to have a material adverse impact on the Company’s Consolidated Results of Operations, Financial Position or Cash Flows.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：聯邦政府近期對專案所用進口材料與商品課徵新增或提高的關稅，墊高公司成本；中國、加拿大、墨西哥與歐盟已回應性加徵關稅或貿易限制，進一步貿易衝突可能增加成本、造成供應鏈中斷或短缺，並對業務與營運結果造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm","excerpt":"In the recent past, the federal government imposed new or increased tariffs or duties on an array of imported materials and goods used in connection with our projects, which raised our costs for these items (or products made with them).","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"搜尋未發現 STRL 被列入出口管制／實體清單，或與 Section 232 直接相關的公司別報導；產業層面 Deloitte 2026 E&C 展望將關稅列為關鍵議題。","source":"Deloitte 2026 engineering and construction industry outlook","url":"https://www.deloitte.com/us/en/insights/industry/engineering-and-construction/engineering-and-construction-industry-outlook.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因素：貿易衝突導致的額外關稅、稅負或貿易限制可能提高成本並造成供應鏈中斷或短缺；未見具名的台灣／中國單點依賴揭露（搜尋摘要層級）","source":"Sterling Infrastructure Form 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm","excerpt":"Any trading conflicts and related escalating governmental actions that result in additional tariffs, duties and/or trade restrictions could increase our costs further, cause disruptions or shortages in our supply chains.","as_of":"2025-12-31","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 revenue $1.56B (+127%); E-Infrastructure Solutions revenue $1.30B (+212%), CEC contributed $425.6M; combined backlog $6.14B (+78%) at 2026-09-30","source":"Sterling Q3 2026 release (syndicated, trivano.com)","url":"https://www.trivano.com/persbericht/771233-771233.html","excerpt":"E-Infrastructure Solutions revenues of $1.30 billion, an increase of 212%. Revenues from Site Development operations increased 133%. The CEC electrical business, which was acquired on September 1, 2025, contributed $425.6 million of revenues in the quarter, compared with $41.4 million during the partial ownership period of the third quarter of","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Management expects data center demand to continue beyond 2026; projects larger and longer; E-Infrastructure revenue expected to grow more than 100% in 2026; JPMorgan est. ~60% of 2027 data center capacity not yet broken ground","source":"Nasdaq/Zacks: STRL's Backlog Visibility: What It Means for 2026-2027 Growth","url":"https://www.nasdaq.com/articles/strls-backlog-visibility-what-it-means-2026-2027-growth","excerpt":null,"as_of":"2026-08-15","retrieved_at":"20261103","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"資料中心預製/模組化施工成為主流（SemiAnalysis 摘要：工期減36%、成本減8%）；未針對場地開發承包商","source":"Longport 轉述 SemiAnalysis","url":"https://longportapp.cn/news/294323779","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"模組化施工縮短資料中心交付時間約40%（廠商來源）","source":"Datacentres.com Research","url":"https://www.datacentres.com/news/factory-built-and-fast-modular-construction-cuts-data-centre-delivery-times-by-4-slot1-2026-09-02","excerpt":"Modular construction: Cost: $8-12M/MW (comparable or slightly lower than traditional) Timeline: 6-10 months (order to powered rack) Customisation: Limited to manufacturer's configurations and options Quality: Factory-controlled environment produces more consistent builds Where modular saves money: Labour: Factory labour is 20-40% less expensive than skilled","as_of":"2026-09-02","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 描述 E-Infrastructure 直接服務大型藍籌終端客戶（資料中心、製造等），前四大客戶占該部門營收 2025年27%、2024年31%、2023年40%；未見訂閱化／D2C／平台化等通路轉移描述。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm","excerpt":"E-Infrastructure Solutions—Our E-Infrastructure Solutions segment serves large, blue-chip end users in the data center, manufacturing, e-commerce distribution center, warehousing, power generation sectors and more.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"分析稿稱 CEC 收購使 Sterling 能提供資料中心園區 turnkey 整合式場整＋電氣交付，並稱 Q1 2026 電話會議兩個園區提前6–8個月轉入整合執行（二手分析稿）","source":"Nasdaq/Zacks: Sterling Ramps Up Mission-Critical Projects","url":"https://www.nasdaq.com/articles/sterling-ramps-mission-critical-projects-visibility-strengthens","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-03 Q2 發布時，公司 FY2026 EPS guidance 19.70–20.30 高於事前共識 18.81；營收 guidance $4.0–4.2B 對共識約 $4.0B（約持平）","source":"MarketBeat: Sterling Infrastructure releases FY 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/sterling-infrastructure-nasdaqstrl-releases-fy-2026-earnings-guidance-2026-08-03/","excerpt":"The company provided EPS guidance of 19.700-20.300 for the period, compared to the consensus EPS estimate of 18.810. The company issued revenue guidance of $4.0 billion-$4.2 billion, compared to the consensus revenue estimate of $4.0 billion.","as_of":"2026-08-03","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 彙整共識評級 Buy、平均目標價約 $720.67；分析師 FY2026 EPS 平均約 18.24，低於新 guidance 區間（目標價日期未標，為聚合站數字）","source":"MarketBeat STRL coverage (Aug 2026)","url":"https://www.marketbeat.com/instant-alerts/sterling-infrastructure-nasdaqstrl-shares-gap-down-time-to-sell-2026-08-04/","excerpt":"analysts anticipate that Sterling Infrastructure will post 18.24 earnings per share for the current fiscal year","as_of":"2026-08-04","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"目標價分布隨來源分歧：Bullstory（2026-08-22）6 位分析師均值約 $905、高 $1,000、低 $754；Walnut Invest（2026-08）均值約 $947；Tickflow（2026-08-01）5 位均值約 $656；Fintel（2026-05-14）均值約 $758、範圍 $485–1,050","source":"Bullstory / Walnut Invest / Tickflow / Nasdaq-Fintel 聚合","url":"https://bullstory.io/en/stocks/strl/forecast/analyst-rating","excerpt":null,"as_of":"2026-08-22","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026 年兩度上修：Q1（5月）營收 guidance 由 $3.05–3.20B 升至 $3.70–3.80B；Q2（8月）調整後 EPS 由 18.40–19.05 升至 19.70–20.30；無下修紀錄。8月公告後股價曾單日跌約 9.45%，Weiss 歸因為 guidance 隱含的利潤率路徑與營收增速不符","source":"Benzinga/Reuters via search summary; Weiss Ratings","url":"https://weissratings.com/en/instant-news-alerts/sterling-infrastructure-inc-strl-down-9-4-is-this-the-moment-to-unload","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Seeking Alpha 2026-04 快照：EPS 近三個月 3 次上修、0 次下修；次一財報預計 2026-11-04 盤後","source":"Seeking Alpha STRL earnings revisions","url":"https://seekingalpha.com/symbol/STRL/earnings/revisions","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["triggers","valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：管理層認為目前無預期對經營結果、財務狀況或現金流有重大不利影響的受威脅或未決法律事項。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm","excerpt":"In the opinion of management, after consultation with legal counsel, there are currently no threatened or pending legal matters that would reasonably be expected to have a material adverse impact on the Company’s Consolidated Results of Operations, Financial Position or Cash Flows.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月14份8-K中，無 Item 4.02（財報不可信賴）；重大項目為2026-07-08 Item 1.01 信貸協議重訂（循環額度$15億）與2025-11-12 Item 8.01 $4億回購計畫。","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000874238&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 14 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-07-02 簽訂第二次修訂重訂信貸協議，借款能力增加$10.5億、循環額度$15億，用途含 permitted acquisitions。","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000093/strl-20260702.htm","excerpt":"The Amended Credit Agreement increases borrowing capacity by $1.05 billion and will initially provide for revolving borrowings up to an aggregate principal amount of $1.5 billion","as_of":"2026-07-08","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"+","claim":"Sterling 於2026-06-09公告完成收購 Stone Ridge Contracting, LLC（愛達荷州 Pocatello 場地開發承包商），併入 E-Infrastructure Solutions，對價為現金加普通股。","source":"PR Newswire／Trivano 轉載 Sterling 公告","url":"https://www.trivano.com/persbericht/sterling-announces-acquisition-of-stone-ridge-contracting-llc-737000.html","excerpt":"(NasdaqGS: STRL) (\"Sterling\" or \"the Company\") today announced that it has closed on the acquisition of Stone Ridge Contracting, LLC. (Stone Ridge), a Pocatello, Idaho-based site development contractor. Stone Ridge will join Sterling's E-Infrastructure Solutions segment.","as_of":"2026-06-09","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-07-02 信貸協議重訂，額度用途含 permitted acquisitions；另 Stone Ridge Contracting 收購於2026-06-09宣布完成（搜尋摘要，未讀原文）。","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000093/strl-20260702.htm","excerpt":"which will be used for, among other things, refinancing and prepaying existing indebtedness, capital expenditures, permitted acquisitions and other general corporate purposes.","as_of":"2026-07-08","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K 無重大未決訴訟；搜尋未見針對 STRL 的證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm","excerpt":"there are currently no threatened or pending legal matters that would reasonably be expected to have a material adverse impact on the Company’s Consolidated Results of Operations, Financial Position or Cash Flows.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月14份8-K清單未見 Item 4.02，搜尋亦未見 SEC 調查或重編報導。","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000874238&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 14 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"STRL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.78,"operating_margin_pct":18.62,"fcf_margin_pct":10.93,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STRL","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"EME","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.59,"operating_margin_pct":9.88,"fcf_margin_pct":7.47,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"FIX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.57,"operating_margin_pct":16.66,"fcf_margin_pct":19.46,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PWR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.76,"operating_margin_pct":6.81,"fcf_margin_pct":8.46,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MTZ","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":12.74,"operating_margin_pct":4.85,"fcf_margin_pct":2.34,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTZ","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"STRL"},"financial_history":{"ticker":"STRL","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":1769436000.0,"revenue_yoy_pct":null,"gross_margin_pct":15.52,"operating_margin_pct":9.08,"net_income":106461000.0,"diluted_eps":3.48,"free_cash_flow":158207000.0,"fcf_margin_pct":8.94,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":1972229000.0,"revenue_yoy_pct":11.46,"gross_margin_pct":17.12,"operating_margin_pct":10.44,"net_income":138655000.0,"diluted_eps":4.44,"free_cash_flow":414205000.0,"fcf_margin_pct":21.0,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2115756000.0,"revenue_yoy_pct":7.28,"gross_margin_pct":20.14,"operating_margin_pct":12.75,"net_income":257461000.0,"diluted_eps":8.27,"free_cash_flow":416150000.0,"fcf_margin_pct":19.67,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":2490049000.0,"revenue_yoy_pct":17.69,"gross_margin_pct":22.98,"operating_margin_pct":16.61,"net_income":290153000.0,"diluted_eps":9.38,"free_cash_flow":362676000.0,"fcf_margin_pct":14.57,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Sterling Infrastructure, Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good morning, ladies and gentlemen, and welcome to the Sterling Infrastructure Third Quarter Webcast and Conference Call. [Operator Instructions] As a reminder, this call is being recorded on Thursday, October 29, 2026. I would now like to turn the conference over to Noelle Dilts, Vice President, Investor Relations and Corporate Strategy. Please go ahead.

**Noelle Dilts** (Executives):
Good morning, and welcome to Sterling Infrastructure's Third Quarter 2026 Earnings Conference Call and Webcast. I'm pleased to be here today to discuss our results with Joe Cutillo, Sterling's Chief Executive Officer; Nick Grindstaff, Sterling's Chief Financial Officer; and Dan Govin, Sterling's Chief Operating Officer. As a reminder, accompanying slides are available in the Investor Relations section of our website and include additional information regarding our full year 2026 financial guidance.
Our discussion today may include forward-looking statements. Actual results could differ materially from the statements made today. Please refer to Sterling's most recent 10-K and 10-Q filings for a more complete description of risk factors that could affect these projections and assumptions. The company assumes no obligation to update forward-looking statements as a result of new information, future events or otherwise. Please note that management may reference certain historical forward-looking and non-GAAP financial measures. Reconciliations of these non-GAAP financial measures to their most directly comparable GAAP financial measures are included in our earnings release and posted in the Investor Relations section of our website. Please refer to the press release for additional information regarding our forward-looking statements and non-GAAP financial measures. Throughout today's discussion, all third quarter 2026 comparisons are to the third quarter of 2025, unless otherwise noted. 
I'll now turn the call over to our CEO, Joe Cutillo.

**Joseph Cutillo** (Executives):
Thanks, Noelle, and good morning, everyone. Sterling delivered another outstanding quarter as adjusted diluted EPS grew 118% to reach $7.58. Revenue increased 127% and adjusted EBITDA more than doubled. On top of this, our visibility continues to expand. Our total scoped work, which includes signed backlog, unsigned awards and the next phases being designed on our current projects now totals nearly $8 billion, up approximately 90% year-over-year. These results demonstrate the strength of our market, the great execution of our teams and the continued success of our strategy.
While the quarterly performance was exceptional, what's even more important is what these results tell us about the opportunity ahead. Throughout 2026, it has become increasingly clear to us that we are in the early stages of significant multiyear investment in large-scale mission-critical infrastructure across the U.S. Data centers remain a powerful growth driver, but the opportunity is much broader, spanning semiconductors, advanced manufacturing, energy infrastructure and the broader build-out supporting the next generation of U.S. industrial growth.
The magnitude of this opportunity is driving us to think even bigger about how we position Sterling for long-term growth. We are focused on building the capacity, services, geographic reach and customer relationships required to capture more share of this investment. Importantly, the $8 billion of scope work does not capture the full development potential of the campuses we are already working on today. Many of these projects span hundreds or even thousands of acres and are being developed in multiple phases over several years.
These are tangible opportunities backed by land, permits and power commitments and is on top of what we already have scoped. In total, these opportunities provide more than 5 years of additional work. Sterling has never been in a better position. We have significant visibility into future growth, deep relationships with our customers and the financial and operational resources to capitalize on the opportunities ahead. We are excited about Sterling's future and confident in our ability to compound strong profitable growth for years to come. 
Now I'd like to hand the call over to Dan to discuss our segment results in more detail. Dan?

**Daniel Govin** (Executives):
Thanks, Joe. I'll begin with E-Infrastructure Solutions, where mission-critical demand, accelerating project activity and outstanding execution drove another excellent quarter. Revenue increased 212% year-over-year, led by continued strength across data center and semiconductor campus projects. Within E-Infrastructure, site development operations more than doubled revenue organically with strong growth across each of our geographies. In the Southeast, customer demand remains robust and projects continue to expand in acreage, number of phases and complexity. This trend plays directly to our strengths, allowing us to leverage our broad self-perform capabilities and proven execution model.
In the Northeast, we continue to make excellent progress on our large semiconductor campus and remain ahead of schedule. Our execution on this large-scale project is strengthening our position and reputation in the semiconductor market. Momentum is building in the Rocky Mountain region, where accelerating activity on recently awarded large projects fueled another quarter of exceptional growth. Our teams are delivering strong execution and are successfully redeploying transportation resources to capitalize on the expanding mission-critical opportunities. Key customers are increasingly engaging us to support their capital plans in Texas, driving significant demand for our site development capabilities. Based on the opportunities we see today, we expect Texas to be a meaningful driver of growth over the next several years.
Turning to CEC. The Electrical business delivered $426 million of revenue in the quarter, more than quadrupling its pro forma full quarter revenue in the third quarter of 2025. Accelerating work on major hyperscaler and large colocation projects drove growth. CEC is scaling rapidly and maintaining strong execution. Year-to-date growth has significantly exceeded our initial expectations, and we now believe full year revenue could exceed $1 billion. This momentum is extending beyond 2026 as CEC continues to build high-quality, longer duration backlog with established customers, positioning the business for continued growth in 2027.
The strong demand and execution across both CEC and site development are translating to significant profit growth for the segment. In the quarter, E-Infrastructure Solutions adjusted operating income increased 171% with adjusted operating margins of 23%. Margins declined year-over-year, reflecting the significantly higher revenue contribution from CEC as it represented 1/3 of the segment revenue in the quarter versus 10% in the prior year period. Within the segment, site development operating margins remained strong at first half 2026 levels, even though several of our large mission-critical projects are still in the early stages of construction. Margins typically expand as these multiphase campuses move into later construction phases over the coming months and years.
CEC operating margins improved both year-over-year and sequentially, and we are encouraged by the margin improvement we are seeing in the core business. As we have previously discussed, we are in the process of winding down some noncore business lines identified during diligence, a process we expect to complete by year-end 2027. We estimate that these noncore operations will be a drag of approximately 160 basis points on full year 2026 CEC margins, masking the roughly equivalent improvement in the core business. At the time of the CEC acquisition, we committed to achieving 300 to 500 basis points of run rate margin improvement at CEC over 18 to 24 months. Progress in the core business and our planned exit from noncore work gives us confidence that we can deliver on this commitment.
Looking ahead, the opportunity in front of E-Infrastructure continues to strengthen. In aggregate, our scope work now approaches $7 billion, an increase of more than 130% year-over-year. The vast majority of these opportunities are tied to mission-critical work, providing substantial visibility into continued growth.
Turning to Transportation Solutions. Revenue declined 3%, reflecting the redeployment of resources from transportation into higher-margin E-Infrastructure work. This transition continues to accelerate as E-Infrastructure activity builds in the Rocky Mountain and Texas regions. This was the second consecutive quarter in which our Rocky Mountain operation generated more revenue from E-Infrastructure than transportation. Despite the lower revenue, Transportation Solutions adjusted operating income grew 22% and adjusted operating margins reached 19.7%. This demonstrates the discipline we are applying to project selection. Transportation Solutions backlog ended the quarter at $964 million, up 31% year-over-year, largely driven by the conversion of unsigned backlog to signed. On the combined backlog basis, the segment declined 22%, again, reflecting the shift in resource allocation.
In Building Solutions, segment revenue declined 5% as homebuilder activity slowed and adjusted operating margin was 8%. We expect residential market conditions to remain under pressure through the balance of 2026 and into 2027. We are managing the business carefully through the current environment while positioning the business to capture more market share when conditions improve. Stepping back, the quarter provides clear evidence of Sterling's strategy in action. We are benefiting from exceptional demand in our highest return markets, becoming more selective about where we are deploying our resources and building the foundation for multiyear growth. With that, I'd like to turn it over to Nick to give you more details on some of our financial metrics and 2026 guidance. Nick?

**Nicholas Grindstaff** (Executives):
Thanks, Dan, and good morning. I'll begin with our cash flow and balance sheet. For the first 9 months of 2026, cash flow from operating activities was $427 million, an increase of 68% compared with the prior year period. One item to note is the increase in accounts receivable at the end of the quarter. Receivables were higher at the end of the quarter due to substantial growth in E-Infrastructure activity, combined with the timing of collections. However, we have already secured a major portion of these outstanding funds in early October, setting us up for robust operating cash flow in the fourth quarter.
Investing activities resulted in a $276 million outflow, including $115 million of capital expenditures. We now anticipate full year CapEx of approximately $140 million. Financing activities resulted in a $325 million outflow year-to-date. On July 2, we closed on the extension and expansion of our revolving credit facilities to $1.5 billion and extended the maturity to July 2031. We used this facility and cash on hand to pay off our existing term loan. The expanded facility further strengthens our financial flexibility and provides additional capacity to support both organic growth and M&A. Financing activities included share repurchases of $107 million. At quarter end, $267 million remained available under our existing repurchase authorization. We will continue to take an opportunistic and disciplined approach to share repurchases as part of our broader capital allocation strategy.
Turning to the balance sheet. We ended the quarter with $217 million of cash and debt of $95 million for a cash net of debt balance of $122 million. Combined with our expanded revolving credit facility and strong cash generation, our balance sheet provides significant capacity to continue investing in the business and pursuing acquisitions.
Moving to guidance. Our performance through the first 9 months and improved visibility into the fourth quarter give us greater confidence in our full year outlook. We're raising our 2026 guidance ranges as follows: revenue of $4.63 billion to $4.73 billion, diluted EPS of $19.16 to $19.42, adjusted diluted EPS of $21.70 to $21.96, EBITDA of $905 million to $916 million, adjusted EBITDA of $970 million to $981 million. Now I will turn the call back to Joe.

**Joseph Cutillo** (Executives):
Thanks, Nick. The trends we've highlighted over the past several quarters have not only continued, they have accelerated. Projects are becoming larger, more technically complex and longer in duration. Our execution continues to build trust and loyalty with our customers, and that is creating opportunities for Sterling to enter new markets, take on more responsibility and have greater participation in our customers' long-term capital planning. The opportunity in front of us is larger than ever. Increasingly, the question is not whether the opportunity is there, but how quickly we can add capacity to capture. We are investing in our people, equipment and our capabilities while maintaining the execution discipline and focus on returns that have driven our success.
As we look to the remainder of 2026, we are confident that we will deliver another record year. The midpoints of our revised guidance ranges would represent 88% revenue growth year-over-year, 101% adjusted EPS growth and 94% adjusted EBITDA growth. Our guidance continues to assume a more pronounced weather impact in the fourth quarter than we experienced in 2025.
Stepping back, our multiyear growth strategy is built around 2 complementary drivers, strong organic growth and disciplined strategic acquisitions. We are targeting annual organic profitability growth of 20% to 30% over the next several years with M&A providing an additional opportunity to accelerate that growth. Together, these drivers support an aspiration to grow earnings by approximately 50% per year. We believe 2027 is shaping up to be another year that meets or exceeds this organic framework.
On the acquisition front, we remain very active and encouraged by the quality of opportunities in the market. We will continue to pursue acquisitions that expand our capacity and geographic presence and enhance the value we can bring to our customers. Our strong balance sheet, significant cash generation and disciplined approach to capital allocation give us the flexibility to fund organic growth and pursue strategic acquisitions supporting our multiyear growth ambition. We're confident in Sterling's ability to deliver sustained profitable growth and long-term value to our shareholders. With that, I'd like to turn it over for questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from Manish Somaiya with Cantor.

**Manish Somaiya** (Analysts):
Joe, when I look at the margin guidance for the full year, it implies 19% or so in the fourth quarter. And clearly, that's down from 21.6% that you had in 3Q. So I was just hoping if you can just help us bridge that. I know you talked about the CEC shedding of noncore businesses that's going to impact the margins. And then just staying on this topic, more specifically, would fourth quarter represent the trough in margins? And how should we sort of think about 2027 as we enter 2027 with strong backlog and obviously, to your point, 20% to 30% organic growth.

**Joseph Cutillo** (Executives):
Yes. I appreciate it, Manish. Yes. So we have -- in the fourth quarter, we have a couple of dynamics. We have the natural seasonality that we go through, and we've done that every year. As we've said, we're being a little conservative on weather for the quarter compared to 2025. Just to remind everybody, 2025 was about the easiest softest winter we've had since I've been here. We basically didn't shut down anything and we're able to run through the entire winter. We don't anticipate that happening again. If it does happen again, that's good. We'll have upside. We'll all be happy. So we have margin erosion just from the seasonality in that.
But we also have the growth of CEC, which I want to step back and talk about for a second here because everybody is looking at this as a negative, and it's really baffling to me and some people have called it mix. And I wouldn't call it mix. We have an electrical business, which is very different than our site civil business. It requires a heck of a lot more -- less capital and we've been able to grow it significantly faster than we ever imagined. That is a great thing. We've more than doubled the business. Yet everybody is looking at it as a negative because it's bringing down the total margins. We have invested almost very little to zero capital in the business to double it. We've been much more successful in hiring electricians than we ever anticipated, which is a great sign. We've got the next phases and next levels of projects from our customers. So we've been successful in executing and delivering, yet we're beat up for it. It makes no sense to me.
So as we grow that business, look, we've had great growth in our site civil business. But as we grow that at a much greater rate, the bottom line is those margins are less. They will always be less, a significant piece of their business is material, and you're not going to be able to get the margins on material that you get in executing the work. Now another positive thing is we've made great progress. And what we said early on is we were going to improve margins in that business 300 to 500 basis points in 18 to 24 months. I will tell you, we're a long way on that path. We're ahead of schedule. And if you remove the legacy business, which we know we have until the end of '27, and hopefully, we're able to do some things to get out of that a little quicker, -- if you remove that, we're on track, and we've seen over 150 basis points of improvement in CEC already. So that's -- I just want to use this opportunity to talk a little bit about that because I think people are really confusing kind of the goodness that's come out of the position and as a result, are penalizing us for really no reason whatsoever. The second question...

**Manish Somaiya** (Analysts):
Yes. No, Joe, the second question I had was just on the trajectory of margins. Would 4Q sort of represent a trough in margins? And how should we sort of think about margin trajectory as we enter 2027? And I guess while I have the mic, if you can also just touch on backlog, how much of that unsigned backlog that you have, which is quite significant, can move into signed backlog? What's sort of the cadence for that?

**Joseph Cutillo** (Executives):
Yes. So let me start with the trough. We certainly have seasonality in our margins. That will continue. Now as we grow the business and we grow in other regions, could that soften it a little bit or change it? Sure. But we will have seasonality. So we don't have a flat margin across 4 quarters. I will also say we have pretty high expectations for the site civil growth in 2027. But we also think Electrical has the opportunity to continue some of these growth rates. And if that happens, again, the blended margin will be the blended margin. I can't predict it because I don't know what the revenue is going to be. But theoretically, and I say theoretically, in reality, the margins of site will continue to improve and the margins in Electrical will continue to improve. Now whatever those revenues come out will determine the end margin, but we're very positive on the margin trajectory in each piece of our E-Infrastructure segment.
On the backlog, I wish somehow we could get out of backlog altogether because it's really a meaningless number for us. We have to look at what we have in backlog, that's jobs that we're actively working on. we have what we call unsigned awarded contracts. That's predominantly in transportation and some in electrical. And what those are is those are jobs that we have been given. We're negotiating final pricing or negotiating final terms and contracts. So those will roll into backlog. They could roll in the quarter. If there's some design work involved, it may take a couple of quarters. But those have -- we have won those jobs. We're in the final negotiations. So those will happen. We have what we're calling the next phase or Phases in design, I guess, is what we're calling it. I apologize. But that's work that's really in the site civil side. That is work that we are in the design phase or in the pricing phase to customers that we know is coming right after these existing phases end.
But there's another piece that everybody is missing. And for those that were on the tour and they're on the call, we literally have thousands of acres of land that is permitted, powered and ready to go. And when the existing phases end, they will design, build out those next phases. Those represent over 5 years of work for us. So when we talk about backlog, backlog represents a very small piece of work that we have sitting in front of us. And as we're talking about building capacity, I'm sure somebody say, well, your backlog is not growing at the rate that your capacity build needs are saying. It's because of that future land and that longevity of these projects that we know we're required to build this capacity to handle these new projects that are coming. I hope that helps, Manish.

**Operator** (Operator):
Your next question comes from Brent Thielman with Oppenheimer.

**Brent Thielman** (Analysts):
Great quarter. Joe, maybe just a follow-up on that last point on E-Infrastructure and maybe to address some of the other concerns out there. I mean you've got all these campuses with phases going on for years. Presumably, those have power. When you look at everything else out there, I guess, just in terms of new campuses that could be potentially in your pipeline to work on, do those have power connections figured out as well? Just trying to address that concern.

**Joseph Cutillo** (Executives):
Yes. Yes. We -- I'm not aware that we've ever started a campus that wasn't -- didn't already have power on it. So these are all permitted, all powered, all ready to go. And as we're looking at the ones coming, they are obviously working on the permitting the power. And as soon as that's released, they generally turn it over to us and we start working. The incremental land that we're talking about is part of that package. And what we've seen in a lot of cases, where they were able to get more power associated with the project, they're buying up incremental land around that area. So a lot of these jobs are actually continuing to get bigger than they originally started when we started on the project. So that's not uncommon at all.

**Brent Thielman** (Analysts):
Okay. And then maybe on CEC, obviously, massive growth here this year. Joe, given some of the constraints out there, kind of help us think about how you get more out of this business, whether it's capacity investments, et cetera. And I think ultimately, what I'm trying to get to is, look, what's sort of a realistic growth assumption when you think about that 20 to 30 you threw out there for a business like this, just given the demand environment and supply side constraints?

**Joseph Cutillo** (Executives):
I'll tell you a couple of things, Brent. We've been very happy with the ability of CEC to obtain electricians. The last number I saw, we were hiring roughly 80 a week just in the state of Texas. We think we can continue to be successful at that into 2027. I will tell you, we have some pretty aggressive growth opportunities with CEC in '27. But in addition, we're looking for small to midsize. And if we found a large, that would be great acquisitions that we can convert their labor force what they're working on existingly and maybe working on small commercial projects or small industrial projects where we can convert those labor forces to our mission-critical customers and add capacity there. In addition, we talked about we tripled the size and we're building out our IMS facility, which does prefab and modules. Every time we can do prefabs for modules, it takes a significant amount of the work required out of the project, which in turn turns into capacity for us. So those are the things that we're really focused on. We're happy with the progress. I think CEC will have great growth numbers in '27.

**Brent Thielman** (Analysts):
Great. Last quick one, just on site development. I think you mentioned maybe you didn't see the step-up in margin in 3Q from preceding quarters, just kind of given project timing, early-stage projects. Could you talk about maybe the other elements like new geographies you're ramping up on? Are those a margin drag? Are they approaching kind of core legacy margins? And just talk through that.

**Joseph Cutillo** (Executives):
Yes. We're -- so the new geographies we're certainly not near what I'll call our most established geographies margins, but we saw -- we're seeing nice improvement in them. The other thing to keep in mind, we talked about the Micron project and the high burn in the quarter. And I don't know, Brad, if we talked about this specifically with you, but one of the uniquenesses of that particular project is the first $600 million or so at 4 million cubic yards of rock that we had to buy and put on that. So it was a large material purchase and the margins are lower on the material side. So their margins on that job are not at the levels of our traditional job.
Now as we get into future phases, that turns into a more traditional job for us. So that definitely was lower as a blended margin. But we're very happy with the progress of all the margins because we were able, even with that, even with the new geographies to keep the site civil margins flat quarter-over-quarter. So it says we're making a lot of progress in a lot of areas. We would have thought based on that burn of Micron that the margins could have gone down for the quarter.

**Operator** (Operator):
Your next question comes from Noah Levitz with William Blair.

**Noah Levitz** (Analysts):
To start off, last quarter, you alluded to the softness in Q3 bookings and then kind of a resurgence in Q4 and early 2027. And I'm sorry if I missed it, but can you give us some color on those potential bookings? Are they still expected to occur this quarter or early next year? And then given that different customers award phases different sizes, are you confident that these potential expected bookings are going to be like as large? Or is it just more confidence that they will occur in this time frame?

**Joseph Cutillo** (Executives):
Well, here's what I'll tell you, and this is again why we don't like backlog. I could theoretically book a $1 billion project and put $10 million in backlog and you wouldn't see the $900 and whatever million left, okay? What I can tell you is all the projects that we've talked about coming out in the fourth quarter and first quarter are still there. They're still coming out. We will see timing. I always hate timing because if something moves 1 week, it can miss a quarter and be in the next quarter, but those projects are still progressing and moving forward. Those projects are bigger than projects that we've seen in the past and will last longer than projects have in the past. 
We're extremely optimistic that they will be contributors in 2027. How fast they start and everything, it's the same typical thing, right? They're working through permits. They're working through all that. And as soon as they get everything done, they're going to pull the trigger and get us going as fast as possible. So nothing's changed on the outlook there. Nothing changed on the project types or size, and we're still moving forward. So we feel very good about the prospects that are in front of us and the impact that's going to have on '27.

**Noah Levitz** (Analysts):
Great. That makes a ton of sense. And then can you give us just like drill down on the geographic expansion? Specifically, like how has your penetration of Texas been going in light of the ERCOT audit and then like differentiate between West Texas exposure with your Rocky Mountains business as well as, I guess, Stone Ridge has exposure there. And then your East Texas exposure with Plateau. And then also like have you already started to expand into the Pacific Northwest? Or is that more of a 2027 event? You've talked about customers dragging you into that geography as well as other geographies. So just an update on specifically Texas and then the Pacific Northwest and then other ancillary geographies.

**Joseph Cutillo** (Executives):
Yes. Well, Texas is going to be the biggest data center state in the next 5 years. So the magnitude of projects coming out are huge. They're in what I'll call the early phases of a lot of these projects, and that's what we see coming out potentially fourth quarter, first quarter of next year, some of those, both in West Texas and what we call East Texas, which is really North Central Texas. And we've made great progress on the ones we're on. The CEC business has got the second phases. We continue with the site developments. We've got the total packages on those. 
And we continue to get asked by our customers to do more. So we're very bullish on Texas. Our bigger challenge right now is how do we grow capacity fast enough to capture as much of Texas is being thrown at us, right? So we've got more -- I guess the simple way to put it is we got more opportunity than we have capacity right now, and we're trying to figure out how to get more capacity to take that.
The Upper Northwest or Pacific Northwest, we're up there. We're doing work. One of the first jobs we're doing work on happens to be a Micron chip plant up there. We got pulled into the Micron chip plant because of the work we've done in New York. We see that as the beginning. The data centers we're talking about haven't come out yet. We think that's going to be late '27 or '28 before we start seeing that activity. But the good news is we're positioned with Stone Ridge, positioned with our RLW business and the work we're doing up in Idaho, and we'll be ready for that when it comes.

**Noah Levitz** (Analysts):
Great. And then just a final quick question. You guided to CapEx of $140 million for 2026, which implies $20 million sequential step down. And given we're having a lot of conversations today about capacity, and then in the past, you've alluded to some of the heavy machinery providers having some supply tightness. Is that kind of the contributor to why CapEx is stepping down sequentially? Or how are you kind of looking at growth CapEx and kind of your ability to build capacity to meet all of this tremendous demand?

**Joseph Cutillo** (Executives):
Yes. I'll let Nick give you some color on it, but it's just timing. It's -- I wouldn't look at it stepping down. I think as we go into next year, we'll need more CapEx to help with our growth rates. But Nick, do you want to give some color...

**Nicholas Grindstaff** (Executives):
So look, we have other things in our toolbox here, too, as far as procuring equipment. We've got a leasing program. Obviously, we've got rentals, too. But even -- so it's just -- it's not all captured in the CapEx number. And so we'll supplement that CapEx with our leasing program.

**Operator** (Operator):
Your next question comes from Kurt Yinger with D.A. Davidson.

**Kurt Yinger** (Analysts):
Just quickly on CEC. I think kind of year-to-date, that's a little bit over $800 million in revenue. I know you have kind of that $1 billion number out there. I guess, is there any reason to believe that like Q3 kind of burn is maybe something that couldn't be repeated? Or is that maybe just a little bit of conservatism thinking about kind of the end of the year?

**Joseph Cutillo** (Executives):
Yes. As we said, no, there's no reason that we can't do Q3 and other quarters. We have factored in some conservativeness on weather. The other thing that people tend to forget is in Q4, we have a couple of big holidays both Thanksgiving and Christmas. And our guys work all year long and don't get vacation and we try to force schedule vacations around those holidays, it's a lot easier for us to manage. So part of the seasonality is just labor management and resource management. It's a lot easier, frankly, for us to say we're going to shut down these 2 weeks or reduce crews these 2 weeks and reduce crews these 2 weeks, so everybody gets their vacation in and can hit the ground running in the next year. So nothing unique about Q3. What you're seeing is CECs continue to have very strong bookings and growth. They got the next buildings of several projects within Texas, and you're just seeing that revenue kick in.

**Kurt Yinger** (Analysts):
Understood. Okay. And then second on just kind of the competitive environment more broadly in the site development side. You've talked about the desire to plant the flag on those projects that are longer in duration, making sure that you're aligned with the right customers. I guess is there any trade-off you have to make from a margin perspective to extend that visibility and ensure you're partnered with those right customers? Or is the service speed, execution, all of those things still showing up in terms of the margin profile of the work that you're bidding or new work, so to speak?

**Joseph Cutillo** (Executives):
A couple of things to keep in mind. First of all, our first phase is always the lowest margin phase. And as these projects advance and we get further in phases, our margins go up over time, okay? And a lot of that, everybody thinks it's pricing. It's really about productivity and things we can do along the line in earlier phases, which either help us or eliminates things we have to do in future phases. That's one. The other piece of it is if we plant a flag in Texas, where we're not 100% vertically integrated, those initial margins will be lower than in the Southeast where we're vertically integrated and we perform everything. However, we've talked strategically that once we get enough critical mass and we're getting there very quickly, we will begin vertical integration in Texas or in new geographies that we are and continue to ramp up that margin profile. 
So you get a double ramp. We've got the natural progression of the phases over that 5-year period or 7 years, whatever that project takes. And then you've got an incremental ramp, which is around as we continue to vertically integrate the other ancillary services and stuff required on that project, you get another pickup. So you look at it is this is the best way for us to have not only long-term growth, but also long-term margin expansion opportunities because the margins will go up on those projects over time.

**Kurt Yinger** (Analysts):
Got it. And maybe just one quick follow-up on that. I mean you've talked about a lot of these new geographies in Texas, in particular. Like when you think about the time line for kind of vertically integrating some of those new areas, is that something that you would kind of think about as a 2027 type timing or probably think further out in terms of when that happens?

**Joseph Cutillo** (Executives):
Yes, it's -- unfortunately, it's not a toggle switch. It's kind of a duration time. It took us -- well, I would tell you, we're still not finished in the Southeast. We continue to look at other services we could add that are parts of the project. But it's really a 24- to 36-month kind of runway, if I was going to give kind of a ballpark or average. What we have to do just to kind of understand it is we got to have enough critical mass that when we buy a company, we can keep them busy 100% of the time on projects. Otherwise, we'll have underutilization, negative productivity and it will actually drag down the margin. So -- and what we like to do, which makes -- it take a little more time, but it's a much more successful model is we like to partner with subcontractors and test run. 
And the ones that we think are the best -- we then continue to grow until the point that they can't keep up with us and then it's a logical time to buy them, right? And it's good for them and it's good for us. And we have great success rate not only on acquiring them, but we double or triple them in 12 to 18 months by putting more revenue and volume on. So it's worked out really well. So as soon as we get enough critical mass, whether that's in blasting or soil stabilization or I can name 10 other things, we'll start looking on how to vertically integrate that or in some cases, we may organically try to put a small business together to support that.

**Operator** (Operator):
Your next question comes from Brian Brophy with Stifel.

**Quinten Helmer** (Analysts):
This is Quinten Helmer on for Brian Brophy. So Stone Ridge outperformed quite meaningfully, it seems. You touched a bit on the drivers already. Is this kind of a one-off because of the large project that you mentioned earlier? Or what's kind of the trajectory we should be thinking about as you continue to execute on tuck-ins on the site development side? Like what are some things you're seeing there? Any color would be appreciated.

**Noelle Dilts** (Executives):
And I'm sorry, what was the question around Stone Ridge you mentioned?

**Quinten Helmer** (Analysts):
Yes. And just kind of how it outperformed. Obviously, the Micron plan is part of it. I'm kind of trying to see what's the trajectory we should be thinking about as you kind of continue to execute on these tuck-ins? And yes, any color there would be appreciated.

**Joseph Cutillo** (Executives):
Yes, yes. So the Micron job really isn't related to Stone Ridge. The Micron job is related to -- the reason we got that and how we got that is the performance that we have on the New York job. If you guys remember, we delivered the September package in July and we delivered the January, February package back in September. So we're several months ahead on that project. Not only was Micron impressed, but the GCs on there so impressed on how far ahead we were. We were asked to go take a look at the job that's taking place in Idaho and since have started doing some work on that job. We're actually using our RLW business on that. They were doing another data center up in that region in area. So we just moved them over there on that. What was the next question?

**Quinten Helmer** (Analysts):
No, that was pretty much it.

**Joseph Cutillo** (Executives):
Yes. I think the important takeaway of that is exactly what we did in data centers, we're doing in semiconductors and the semiconductor tidal wave hits around 2030. So for us, to have this much work today in semiconductors is a huge bonus, but more of a credit to our teams on the value they can bring to customers, and we believe we will be the go-to company on the big semiconductor jobs when they come.

**Operator** (Operator):
Your next question comes from Sangita Jain with KeyBanc Capital Markets.

**Sangita Jain** (Analysts):
Joe, can I ask you a bigger picture question on the dynamics that you're seeing in the market right now with reference to the pushback to rural data center activity? And if that is changing in any way how you manage risks as you consider terms and conditions for these large bookings?

**Joseph Cutillo** (Executives):
Yes. So a couple of things. There is so much noise out there, and I can't wait for next week to be over on permitting and everything else. And in fairness to our customers, we've got these projects. They've got them sitting there. They're ready to get going. But they're trying to figure out like is something going to change, right? And my answer is I don't know, and they don't know. Right now, in some instances, I'll give you a perfect example in Texas, there is all the buzz around permitting and having to go back through everything. And one of the things that was happening is TCEQ, who hands out all the water permits for the state of Texas has an automated process for permits. Well, guess what? Data centers were still submitting applications for permits through the automated system, and they were getting permits. 
Some group stepped in and said, "Wait a second, this isn't what the governor said, you have to manually review the permits." And TCEQ said, well, we don't really have a process to manually review. The customer said, I got permits, are they valid or not valid? I will tell you, they're debating back and forth right now on whether they are. So it's a little bit of limbo. So are those projects going to go? Absolutely, are they going to go? Is there confusion in the system right now for things like that? Absolutely, there is. 
I think after the election, a lot of this goes away, and it will become very clear. But we're not seeing anybody backing off projects. We're not seeing anybody change strategies or anything else. But let's just say we're all wrong. Worst-case scenario, something like that happens. here's what's going to happen as a result. That 1,000 acres that I have left on the job that has power and permitting is going to -- they are going to figure out how to either build that out faster or buy more land around it until they get the other stuff worked out. So we are sitting here looking at it with 5-plus years of work in our grasp on projects we're working on, saying, could there be some noise? Probably. Do we hear anything about the work slowing down or getting smaller? The answer is absolutely not. So we'll get through it, and it will be fine.

**Sangita Jain** (Analysts):
Got it. And then if I can ask one on the entire margin discussions that have happened so far. You spoke about [indiscernible] margins, the puts and takes. You're in early stages on several jobs and those stages tend to be a little bit margin dilutive. You're also moving into new geographies. So can you tell us how you're thinking about which one goes first, whether the existing jobs go into advanced stages and show more margin or whether the geographic expansion takes over and we continue to see margins in this flattish range for a while?

**Joseph Cutillo** (Executives):
Well, I'd have to do a pretty deep analysis on it. Here's what I would tell you is in the quarter, you would have thought our margins would have gone down on site and they didn't, which says the combination of the advancements in margins in the new geographic expansions are improving very nicely. We're in the early phases of a lot of projects. I would have thought that would have brought it down and that Micron project, which is a unique one. We know that shifts into a different set of phases as we get into 2027, probably around the second quarter. We know we'll continue to make advancements. So I don't see us having site margins going backwards. The question is how fast do they go forward, right? And as those kick in, they're all positive tailwinds, not negative tailwinds as we move...

**Operator** (Operator):
Your next question comes from Adam Thalhimer with Thompson Davis.

**Adam Thalhimer** (Analysts):
Joe, you talked about growing earnings 50% plus with acquisitions. Was that a multiyear comment or a 2027 comment?

**Joseph Cutillo** (Executives):
Well, Adam, over the last 6 years, we've grown at 48% on the bottom. I don't like to go backwards. And I think we have a multiyear opportunity here to continue to grow based on what we're seeing coming out of the marketplace. Everybody talks about data centers. We feel very bullish on what we're seeing over the next 3 to 5 years coming out of data centers. We feel like we are positioning ourselves extremely well for the semiconductor wave that starts coming out around 2030. So you start putting those together, plus all the -- nobody is talking about the one-off manufacturing plants here and there. We've got the Rivian plant, they just announced the Saudi plant, they just announced 4 or 5 others. We don't have those, but we'll see where they fall and if we don't. 
We're passing on the pharma plants right now just because we don't have the capacity to go after them. So we have plenty of opportunity to do that. The biggest wildcard is the acquisition. I feel very good about our organic side. The acquisitions are always a wildcard. Can we find the right ones in the right place at the right price? I feel very good about the market today. We've seen some high-quality businesses out there, both in site and electrical and excited about 2027. So it's not '27. This is what we think we can do over a multiyear.

**Adam Thalhimer** (Analysts):
Okay. Good color. And then to what extent were margins negatively impacted in Q3 by diesel or other inflation?

**Joseph Cutillo** (Executives):
Yes. It's really interesting. Nobody has heard us talk about diesel. Nobody has heard us talk about inflation. And the reality is what we love about our contract structure and the way these things are phased is that really mitigates a big part of that risk. If we won $1 billion -- a 7-year $1 billion project and we put that all in backlog, we'd be winding and crying on every one of these calls about diesel prices, about concrete prices, about something else. So is it's a negative to the outside world because no one believes we have $1 billion, but we know we do. It's a positive because the contract structure really mitigates the risk on that stuff. So I won't tell you that we've had 0 impact that would be false. But we're not going to talk about it because our job is to overcome it and it's such a small impact, we're moving forward.

**Operator** (Operator):
Your next question comes from Julio Romero with Sidoti & Company.

**Julio Romero** (Analysts):
Joe, Nick, and Daniel. A lot of good questions about capacity today. Just over the next 4 to 5 years, how would you have us think about the pace of capacity adds and what kind of visibility you have to that pace? Joe, you said that you've been very successful at hiring and adding electricians. You said CEC is a great returns business, relatively less fleet needed, more about adding headcount. So clearly, with the demand outlook being very strong in multiyear, it sounds more and more like the pace of capacity adds is increasingly important to the growth runway in, say, '28, '29 and the next decade. So if you could speak to the pace and visibility of that.

**Joseph Cutillo** (Executives):
Yes. Yes, Julio, it's a good question. The question no one's asked, and I'm glad because it's kind of a delusional question is we've grown it much -- we said over the next several years, we can grow 20% to 30% organically and feel comfortable with that. We've grown a hell of a lot more than that organically over the last couple of years. Now you can only keep that sort of pace for so long. We feel good on the 20% to 30% organic pace over the next several years. Certainly, internally, we're going to try to do a hell of a lot more than that. But you really start getting stretched on some of the internal resources and some of the capabilities. To beat that pace, it's really going to require us to do more on the acquisition front and really add more capacity, whether that's in new geographies or within geographies that we're in. For us to even come close to keeping up with the pace of stuff coming out in Texas we're going to have to make those acquisitions.
Now as we talked about in the site tour a couple of weeks ago, there are things we can do with acquisitions that are not even in Texas that can help us with capacity in Texas. And what I mean by that is we have 2 types of crews. We have traveling crews and we have local crews. And for us, a traveling crew, it doesn't matter if they're in Virginia or Texas or Ohio or wherever you want to pick, okay? They travel and they do work. So one of the things we're looking at is if we have a concentration of either a traveling crew that's on a mega project and it's going to be there for a long period of time or multiple traveling crews in a geography, does it make sense for us to make an acquisition within that geography of which we can then lever to do the work of a traveling crew and grow that business quite substantially very quickly, and that then frees up the capacity of that traveling crew. 
So I can make an acquisition in an area, grow the business very rapidly, double it probably 3 years, free up a traveling crew that now frees up $500-plus million of capacity for me and put them in a new geography. So those are some of the things we're looking at to increase the pace of growth beyond that 20% to 30%.

**Julio Romero** (Analysts):
Very helpful. And then have you seen any changes in how customers are financing or committing to future phases or negotiating payment terms? And just talk about more broadly how customer financial quality influences your customer selection process.

**Joseph Cutillo** (Executives):
Yes. No, we haven't seen anything. Look, the lion's share of our customers are the top-tier guys, one tier down that are all financially very stable. I know everybody panics when a Meta or Amazon or somebody goes and gets financing. I look at that as that's more money they're going to spend on us to build more stuff, right? That's the greatest thing that can happen every time I see that happen. So we have not seen anything along those lines. The step-up in receivables in the quarter really is more timing and starting the first phase of a lot of these projects. And as you can imagine, you start a project you get going, even if you have a 30-day billing cycle, by the time you get everything done, but and in, it's 60 days minimum before you're going to get your first payment. So unless you start those right at the beginning of the quarter, you're not going to see them. And we had a pretty strong first couple of weeks in October. So just kind of laying out with what we've seen in the past.

**Operator** (Operator):
There are no further questions on the phone line. I'll turn it back to Joe for some closing comments.

**Joseph Cutillo** (Executives):
Great. Thanks, Bob. I want to thank everybody again for joining the call today. If you have any follow-up questions, please contact Noelle Dilts. Her contact information is in the press release. I hope everybody has a great day. We'll be talking to a lot of you this afternoon. Thanks.

**Operator** (Operator):
Ladies and gentlemen, this concludes your conference call for today. We thank you for participating and ask that you please disconnect your lines. Have a great day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### STRL_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜CFO｜guidance：CFO 上調 2026 全年營收財測區間為 40 億至 41.5 億美元（含 Stone Ridge）（原話："$4 billion to $4.15 billion"）
- 2026-08-04｜CFO｜guidance：CFO 給出調整後稀釋 EPS 財測區間 19.70–20.30 美元（原話："adjusted diluted EPS of $19.70 to $20.30"）
- 2026-08-04｜CFO｜guidance：CFO 給出調整後 EBITDA 財測區間 8.91–9.16 億美元（原話："adjusted EBITDA of $891 million to $916 million."）
- 2026-08-04｜CEO｜guidance：CEO 說明財測中點相對去年的成長幅度（營收 64%、調整後 EPS 84%、調整後 EBITDA 79%）（原話："an 84% adjusted EPS growth and a 79% adjusted EBITDA growth"）
- 2026-08-04｜CEO｜guidance：CEO 預期傳統場地開發業務 2026 年成長率接近 70% 或更高（原話："will grow at rates approaching 70% or higher"）
- 2026-08-04｜CEO｜guidance：CEO 給 E-Infrastructure 全年調整後營業利益率預期落在 20% 中段（原話："expected to be in the mid-20%"）
- 2026-08-04｜CEO｜guidance：CEO 預期 Transportation Solutions 2026 營收下滑 7%–10%（原話："revenue in the 7% to 10% range"）
- 2026-08-04｜CEO｜guidance：CEO 預期 Building Solutions 全年調整後營業利益率為高個位數至低雙位數（原話："operating margin will be in the high single to low double di"）
- 2026-08-04｜CEO｜guidance：CEO 預告第三季接單可能偏弱、與強勁營收消化合併可能使第三季在手訂單環比下降，稱屬接單時點（原話："a sequential backlog decline in the third quarter"）
- 2026-08-04｜CEO｜guidance：CEO 回答分析師關於下半年營收增幅時，稱第四季預測刻意保守（原話："we're being very conservative in the fourth quarter right no"）
- 2026-08-04｜CEO｜guidance：CEO 預期東北部半導體專案第四季受天氣影響放緩（原話："with a weather-related slowdown in the fourth quarter"）
- 2026-08-04｜CEO｜guidance：CEO 說明 Transportation Solutions 已累積超過兩年在手訂單，且處於聯邦資金週期最後一年（原話："We have built over 2 years of backlog"）
- 2026-08-04｜CFO｜guidance：CFO 報告 Q2 簽約在手訂單與合併在手訂單的訂單出貨比（排除 Stone Ridge）（原話："Second quarter 2026 book-to-burn ratios were 1.4x for"）
- 2026-08-04｜CEO｜margin：CEO 說明 E-Infrastructure 各分項毛利率皆上升，利潤率差異完全來自組合（原話："margins were up in every single piece of it"）
- 2026-08-04｜CEO｜margin：CEO 拆解本季利潤率：場地開發約高 20% 段、CEC 約 12%（原話："you're in upper 20s and the CEC side, roughly 12%"）
- 2026-08-04｜CEO｜margin：CEO 說明下半年利潤率因 CEC 成長更快而被稀釋，稱純屬組合效應（原話："this is purely mix, we're not losing margin"）
- 2026-08-04｜CEO｜margin：CEO 表示 CEC 利潤率改善來自更好的專案組合，區間 300–500 基點，原稱 12–18 個月（原話："we see 300 to 500 basis points"）
- 2026-08-04｜CEO｜margin：CEO 表示不預期電氣業務利潤率達到場地開發的高點（原話："We don't ever expect electrical margins to be"）
- 2026-08-04｜CEO｜margin：CEO 提出 3–5 年電氣業務 EBITDA 利潤率可接近 20% 的目標（目前業界約 10%–12%）（原話："I don't know why we can't get that close to 20%."）
- 2026-08-04｜CEO｜margin：CEO 解釋場地開發利潤率成長趨緩的原因：新專案早期階段較低，以及落基山區（設備較小、未垂直整合）成長更快（原話："new projects where the beginning phases of new projects are"）
- 2026-08-04｜CEO｜margin：CEO 指 CEC 利潤率提升的兩大驅動：退出低毛利舊業務及專案規模變大（原話："we're getting out of some legacy business segments that"）
- 2026-08-04｜CEO｜margin：CEO 稱 Plateau 利潤率已接近高峰，僅剩小幅增量空間（原話："they're getting close to peak"）
- 2026-08-04｜CEO｜commitment：CEO 承諾持續擴增產能，並認為需要加速擴張速度以跟上專案規模（原話："we've got to really accelerate the rate"）
- 2026-08-04｜CEO｜commitment：CEO 表示公司需要進行更多併購以補足產能（原話："we are going to have to make more acquisitions"）
- 2026-08-04｜CEO｜commitment：CEO 說明當前條件下德州可再增加 2–3 個 CEC 規模的電氣業務（與去年 Q3 的看法相比轉變）（原話："I would add 2 or 3 more CECs to the Texas market"）
- 2026-08-04｜CEO｜commitment：CEO 表示公司傾向保守，並稱要重新思考如何更好地對外溝通未納入的專案規模（原話："we're thinking about how we"）
- 2026-08-04｜CFO｜capital_allocation：CFO 將 2026 資本支出財測上調至 1.3–1.4 億美元，較先前增加 3,000 萬（原話："$130 million to $140 million, which is a $30 million"）
- 2026-08-04｜CFO｜capital_allocation：CFO 說明上半年以平均每股 511.18 美元買回 3,500 萬美元股票（原話："share repurchases of $35 million at an average price of"）
- 2026-08-04｜CFO｜capital_allocation：CFO 稱買回態度為機會導向（原話："opportunistic in our approach to share repurchases"）
- 2026-08-04｜CFO｜capital_allocation：CFO 說明循環信貸擴增至 15 億美元的用途為把握併購機會（原話："certainly to take advantage of opportunities for acquisition"）
- 2026-08-04｜CEO｜capital_allocation：CEO 說明市場上高品質併購標的比一年前更多（原話："We are seeing more high-quality acquisition targets"）
- 2026-08-04｜CEO｜capital_allocation：CEO 說明併購目標偏向規模較小的公司，並以公司資源補強，Stone Ridge 屬此類（原話："we're starting to look at a little bit smaller players"）
- 2026-08-04｜CEO｜customer：CEO 說明 CEC 已取得資料中心的第二棟建築工程，作為執行品質的佐證（原話："CEC is now getting the second buildings on data centers"）
- 2026-08-04｜CEO｜customer：CEO 說明部分專案可能持續 5 至 12 年，而公司目前只對外講 3 年（原話："projects we're going to be on for 5 to 8 to 12 years"）
- 2026-08-04｜CEO｜customer：CEO 說明未來階段工作簿未納入客戶在既有專案旁追加購地的擴張（原話："So we don't put any of that into right now our future phase"）
- 2026-08-04｜CEO｜customer：CEO 說明資料中心既有專案超出原範圍的增量機會尚未反映在在手訂單（原話："Much of this incremental opportunity is not yet reflected"）
- 2026-08-04｜CEO｜customer：CEO 說明 CEC 約 90 天填滿產能，遠快於收購時預期的一年（原話："We filled their capacity up in about 90 days."）
- 2026-08-04｜CEO｜customer：CEO 說明本季取得亞特蘭大電動車廠初期工作範圍（原話："we were awarded the initial scope of work on an electric veh"）
- 2026-08-04｜CEO｜risk：CEO 回應德州暫停資料中心核准的新聞：目前未見對公司工程時程的影響（原話："we haven't seen anything that's impacted any of our schedule"）
- 2026-08-04｜CEO｜risk：CEO 承認未來施工啟動後可能出現供應鏈延遲（原話："could there be other supply chain delays"）
- 2026-08-04｜CEO｜risk：CEO 稱電工是最緊的產能環節，已限制公司承接更多案子（原話："the tightest is around electricians"）
- 2026-08-04｜CEO｜risk：CEO 稱場地開發端產能首度變得相當緊（原話："getting really tight on the capacity piece"）
- 2026-08-04｜CEO｜risk：CEO 說明住宅市場全年將面臨強烈逆風（原話："the residential market will face strong headwinds throughout"）
- 2026-08-04｜CEO｜competition：CEO 說明未來階段多採議價而非競標，除非範圍大幅變動（原話："We generally are negotiating those prices with the customer"）
- 2026-08-04｜CEO｜competition：CEO 說明未見大型新競爭者湧入（原話："we have not seen an influx of major new players"）
- 2026-08-04｜CEO｜competition：CEO 說明定價與條款無根本性轉變，但電氣端有人試圖加入公司拒絕的條款（原話："We're not seeing anything fundamentally shift."）
- 2026-08-04｜CEO｜competition：CEO 說明進入新市場時第一個案子最難拿，之後本地競爭變少（原話："The first one is always the hardest one for us to get"）
- 2026-08-04｜CEO｜product：CEO 說明半導體與製藥的預期時程（製藥約 2028、半導體約 2030）（原話："We think pharma is '28. Semis are around 2030."）
- 2026-08-04｜CEO｜product：CEO 說明東北部半導體專案進度超前（原話："running ahead of schedule"）
- 2026-08-04｜CEO｜product：CEO 說明 Transportation 資源正加速轉向 E-Infrastructure，落基山區首度 E-Infra 營收高於交通（原話："This was the first quarter that our Rocky Mountain"）
- 2026-08-04｜CEO｜product：CEO 說明 Q2 簽約在手訂單與增幅（原話："Signed backlog at quarter end totaled $4.3 billion"）
- 2026-08-04｜CEO｜product：CEO 說明 CEC 與場地開發聯合承接專案數量已達 3–4 個，受限於電氣產能（原話："We're on 3 or 4 now. It's just pure capacity."）

### 問答異常語氣（迴避／改口／保留）
- STRL_Q2_2026_Earnings_Call_20260804.md｜問：Brent Thielman (Oppenheimer)：在手訂單翻倍加上 Stone Ridge，為何下半年營收增幅沒有更大？是否有較長前置時間？｜答法：未給下半年具體數字，改以「第四季預測刻意保守、天氣、已多次上調財測」回應，否認放緩但未量化
- STRL_Q2_2026_Earnings_Call_20260804.md｜問：Manish Somaiya (Cantor)：2026 與 2027 正常化 E-Infra 利潤率，以及 Stone Ridge（中段 teens 利潤率）的改善路徑｜答法：未給 2027 利潤率數字，也未回應 Stone Ridge 利潤率路徑；改談 Plateau、Petillo、落基山區與 CEC 的組合邏輯，追問後只給本季場地開發高 20% 段 vs CEC 約 12%
- STRL_Q2_2026_Earnings_Call_20260804.md｜問：Sangita Jain (KeyBanc)：下半年利潤率指引是否因 CEC 成長快於幾個月前的預期｜答法：CEO 先以「純屬組合」回應，未直接確認是否高於先前預期；由 IR 主管 Noelle Dilts 補充確認 CEC 成長與新專案爬坡比先前預期更快
- STRL_Q2_2026_Earnings_Call_20260804.md｜問：Adam Thalhimer (Thompson Davis)：第三季接單偏弱的原因與投標活動細節｜答法：以「純屬時點、客戶發包週期」回應，未給第三季接單的量化範圍；語氣含「Don't panic」式安撫

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
{"date":"20260905","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼第二階：股價 <$420（FY26 21x）或 FY27 指引 E-Infrastructure ≥+20% 且分部利潤率 ≥25%","irr_base_pct":6.9,"ev5y_pct":32.5,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"-","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":1.85,"ev5y_pct":32.5,"irr_base_pct":6.9,"max_dd_pct":-58,"bull_5y_price":1104.0,"bear_5y_price":208.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"加碼第二階：股價 <$420（FY26 21x）或 FY27 指引 E-Infrastructure ≥+20% 且分部利潤率 ≥25%","price_at_dd":486.49,"archetype":"品質複利成長","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STRL_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
