你是 stock-analyst **v20 判斷 agent**，標的 NVT（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"NVT","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVT_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVT_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":1514.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）"},"note":"未採集"},{"id":"f_kpi1_non_gaap_adjusted_operat","label":"Non-GAAP (adjusted) operating income / return on sales","value":22.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","unit":"%（調整後營業利益 335.4M，YoY +57%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）"},"note":"未採集"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":18.6,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","unit":"%（GAAP 營業利益 282.3M，YoY +70%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）"},"note":"未採集"},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":267.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）"},"note":"未採集"},{"id":"f_kpi4_stock_based_compensation","label":"Stock-based compensation（前九個月累計，新聞稿未單列 Q3）","value":30.9,"period":"前九個月至 2026-09-30，公告於 2026-10-30","unit":"USD M（9M 2026）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"前九個月至 2026-09-30，公告於 2026-10-30","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）"},"note":"不適用"},{"id":"f_kpi5_guidance_q4_fy2026","label":"Guidance: Q4 FY2026","value":"adjusted EPS 1.30–1.33；GAAP EPS 1.13–1.16","period":"公告於 2026-10-30","unit":"USD/share","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"公告於 2026-10-30","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）"},"note":"未採集（本檔 consensus_revision 為財報前快照）"},{"id":"f_kpi6_guidance_fy2026","label":"Guidance: FY2026（上調）","value":"adjusted EPS 5.36–5.39；GAAP EPS 4.54–4.57","period":"公告於 2026-10-30","unit":"USD/share","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"公告於 2026-10-30","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）"},"note":"未採集"},{"id":"f_kpi7_systems_protection_sales","label":"Systems Protection sales / adj. return on sales","value":1098.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD M（YoY +53%；adj. ROS 23.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）"},"note":"未採集"},{"id":"f_kpi8_electrical_connections_s","label":"Electrical Connections sales / adj. return on sales","value":416.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD M（YoY +23%；adj. ROS 28.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）"},"note":"未採集"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-30","period":"2026-10-30","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-30"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_nvt_gross_margin_pct","label":"NVT 毛利率","value":36.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvt_operating_margin_pct","label":"NVT 營業利益率","value":17.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvt_fcf_margin_pct","label":"NVT FCF 利潤率","value":11.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hubb_gross_margin_pct","label":"HUBB 毛利率","value":35.36,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HUBB.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hubb_operating_margin_pct","label":"HUBB 營業利益率","value":20.21,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HUBB.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hubb_fcf_margin_pct","label":"HUBB FCF 利潤率","value":14.07,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HUBB.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_etn_gross_margin_pct","label":"ETN 毛利率","value":35.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_etn_operating_margin_pct","label":"ETN 營業利益率","value":17.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_etn_fcf_margin_pct","label":"ETN FCF 利潤率","value":13.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_vrt_gross_margin_pct","label":"VRT 毛利率","value":38.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_operating_margin_pct","label":"VRT 營業利益率","value":20.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_fcf_margin_pct","label":"VRT FCF 利潤率","value":23.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":125.19,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-22.82,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":34.62,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.17 → 5.17）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.78 → 6.78）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.05 → 8.05）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.17,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.78,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":8.05,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":12.15,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 4.61 → 5.17（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":30.39,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝75.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":75.3,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.82,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝62.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":62.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.05,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝54.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":54.1,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":24.21,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 5.17，分子＝快照價 125.19","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.671,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1224.1,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 2345.9、現金 1121.8（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":161.6,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":21454.56,"period":"2026-11-03","unit":"USD m","basis":"市值 20230.46 ＋ 淨負債 1224.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":5809.28,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（8 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":7537.62,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（10 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.69,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 122.23 / W52 136.36 / W104 105.32 / W250 72.52 / W250 13週斜率 2.13%"},{"id":"f_ma_w52","label":"52 週均線","value":136.36,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":105.32,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":72.52,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.13,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：公司面對大型全球對手、區域／在地廠商與低成本製造商，並明言新進入者可能提供競爭產品，可能壓縮利潤並限制維持或提高份額的能力。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm","excerpt":"Competition may also result from new entrants into the markets we serve offering products and/or services that compete with ours.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 業務章節：各產品線對手數量與規模差異大，部分較小對手以價格、在地專長與關係競爭；公司不依賴單一專利、客戶關係或品牌。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm","excerpt":"Some of our competitors, in particular smaller companies, attempt to compete based primarily on price, localized expertise and local relationships. The number and size of competitors vary considerably depending on the product line.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Vertiv 2026-04 完成收購 Strategic Thermal Labs 以強化液冷工程能力（對手動作）；nVent 稱已部署逾 2GW 液冷容量。","source":"Zacks／Nasdaq: Can AI Data Center Demand Keep Driving nVent Electric's Growth?","url":"https://www.nasdaq.com/articles/can-ai-data-center-demand-keep-driving-nvent-electrics-growth","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"nVent 2026 Q2 銷售 +53%、有機 +47%、資料中心 2026 年銷售預期逾 $20 億（成長快於產業的間接線索，非份額數據）。","source":"Benzinga: nVent Raises 2026 Outlook as Liquid Cooling Demand Accelerates","url":"https://www.benzinga.com/markets/earnings/26/07/60845239","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K FY2025 揭露最大客戶約占 2025 合併淨銷售 11%，無其他客戶超過 10%；公司稱無法保證留住最大客戶，部分客戶未來可能轉向競爭對手。搜尋未找到最大客戶導入第二供應商或自製的具體來源。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm","excerpt":"Our net sales to our largest customer represented approximately 11% of our consolidated net sales in 2025. While we do not have any other customers that accounted for more than 10% of our consolidated net sales in 2025, we have other customers that are key to the success of our business.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 最大客戶（Systems Protection 分部）占合併淨銷售約 11%，無其他客戶超過 10%；2024、2023 無客戶超過 10%。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm","excerpt":"Our net sales to our largest customer represented approximately 11% of our consolidated net sales in 2025. While we do not have any other customers that accounted for more than 10% of our consolidated net sales in 2025, we have other customers that are key to the success of our business.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"單一客戶占2025年底應收帳款約11%；2024年底無客戶超過10%。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm","excerpt":"Accounts receivable from one customer represented approximately 11% of total accounts receivable as of December 31, 2025. No customer receivable balance exceeded 10% of total net receivable balance as of December 31, 2024.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Rystad 2026年5月底白皮書：設備價格與交期短期仍高，歐美製造商的變壓器與高壓斷路器交期至少2～3年；Wood Mackenzie 2025年調查顯示電力變壓器平均交期128週。","source":"pv magazine USA: U.S. transformer market faces severe supply constraints as lead times extend to four years","url":"https://pv-magazine-usa.com/2026/05/11/u-s-transformer-market-faces-severe-supply-constraints-as-lead-times-extend-to-four-years/","excerpt":null,"as_of":"2026-05-11","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"新產能多在2027～2028年後才投產（Eaton南卡廠2027、Siemens Energy北卡廠約2027初）；Goldman（二手轉述）預估美國變壓器需求2027-28年增9～12%、國內產能僅增2～4%；Citi（二手轉述）估全球高壓變壓器供給2026～2028年低於需求。","source":"搜尋結果彙整：powerpeakdigest / longbridge / GreentechLead（二手轉述，未核原文）","url":"https://powerpeakdigest.com/global-transformer-supply-constraints-ease-rystad/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"nVent 2026 Q2財報電話會：$25億在手訂單提供2026年餘下及2027年能見度；2026年資料中心銷售預期超過$20億、為前一年兩倍以上；第三座明尼蘇達液冷廠Blaine 2預計2027上半年開出，支撐需求至2027及2028；CEO稱液冷僅占資料中心散熱10～15%；訂單大且不均；關稅增量約$1億。","source":"MarketBeat: nVent Electric Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/nvent-electric-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.H","decision_inputs.bear","triggers"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Wood Mackenzie 2025年9月摘要：GSU與電力變壓器交期出現改善跡象但仍在2～3年；另有報導指低壓桿上變壓器可能轉為過剩。","source":"Wood Mackenzie: Making the connection executive summary (Sept 2025) / powerpeakdigest","url":"https://www.powermag.com/wp-content/uploads/2026/01/making-the-connection-executive-summary-september-2025.pdf","excerpt":null,"as_of":"2025-09-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3 列示的法律程序為一般商業糾紛、產品責任、石棉、環境、專利與僱傭事項及環境 PRP 案，未列反壟斷調查或拆分事項；搜尋亦未見 2026 年針對 nVent 的 DOJ/FTC/EU 競爭調查報導。","source":"SEC EDGAR 10-K FY2025 Item 3. Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm","excerpt":"We have been made parties to a number of actions filed or have been given notice of potential claims relating to the conduct of our business, including those pertaining to commercial disputes, product liability, asbestos, environmental, safety and health, patent infringement and employment matters.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：公司列出對鋼、鋁、銅及中國、加拿大、墨西哥製品關稅的暴露；2025 年第二季起新關稅（含中國、墨西哥、歐盟）已公布，後續仍可能調整，最終影響不確定。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm","excerpt":"particularly tariffs on steel, aluminum and copper and products manufactured in China, Canada and Mexico, and adverse responses by foreign governments to U.S. trade policies","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"MD&A：2025 年新關稅因緩解措施對財務無重大影響，但預期 2026 年起通膨成本（含關稅）持續，可能衝擊營運結果；2025 年毛利率下滑 2.5 個百分點部分源於含關稅的通膨。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm","excerpt":"The effects from new tariffs imposed in 2025 did not have a material impact on our financial results in 2025 due to mitigating actions.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：部分產品屬兩用（dual use）產品，受較嚴格出口管制。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm","excerpt":"Certain of the products we manufacture are “dual use” products, which are products that may have both civil and military applications, or may otherwise be involved in weapons proliferation, and are often subject to more stringent export controls.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"nVent 揭露依賴美國以外生產的零組件與成品，點名墨西哥與中國，並提及政治或貿易不穩定風險","source":"nVent Electric 10-K FY2025 ARS","url":"https://www.sec.gov/Archives/edgar/data/1720635/000110465926037785/tm267209d3_ars.pdf","excerpt":"agreements, greater restrictions on free trade generally, the imposition of or significant increases in tariffs on goods imported into the U.S. particularly tariffs on steel, aluminum and copper and products manufactured in China, Canada and Mexico, and","as_of":"2026-03-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026 年 10-Q 稱關稅帶來原料、人工、運輸通膨，供應鏈限制可能中斷關鍵零組件取得","source":"nVent Electric 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001720635/000162828026068596/nvt-20260930.htm","excerpt":"the impacts related to tariffs, primarily related to raw materials, labor and transportation costs. Although we regularly monitor the financial health and operations of companies in our supply chain, and use alternative suppliers when necessary and available, supply chain constraints could cause a disruption in our ability to obtain raw materials or critical components required to manufacture","as_of":"2026-10-31","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 淨銷售 $1,515M，年增 44%（有機 44%）；10-Q 稱有機成長 43.7% 中約 35.0 個百分點來自 infrastructure（資料中心）業務。","source":"nVent 10-Q (period 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001720635/000162828026068596/nvt-20260930.htm","excerpt":"organic sales growth contribution of approximately 35.0% and 37.0% from our infrastructure business in the third quarter and first nine months of 2026 from 2025","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"公司上修 FY2026 報告銷售成長至 48–49%（前次指引較低），Q4 報告銷售成長指引 45–48%。","source":"nVent Q3 2026 press release (8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001720635/000162828026068391/q32026nvtpressrelease.htm","excerpt":"The company now estimates reported sales growth for full-year 2026 of 48 to 49 percent versus prior guidance","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 時管理層預期 2026 資料中心銷售逾 $20 億（超過去年兩倍）；Q2 backlog $25 億，有機訂單低雙位數成長；液冷僅占資料中心冷卻 10–15%；Blaine 2 液冷廠預計 2027 上半年開出。","source":"Benzinga / Nasdaq-Zacks 摘要（Q2 2026 財報）","url":"https://www.benzinga.com/markets/earnings/26/07/60845239","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"管理層稱刻意消化 backlog 以維持客戶交期，backlog 自 Q1 $26 億降至 Q2 $25 億。","source":"Nasdaq/Zacks 摘要","url":"https://www.nasdaq.com/articles/can-ai-data-center-demand-keep-driving-nvent-electrics-growth","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 分部：Systems Protection 銷售 +53% 至 $1.1B、Electrical Connections +23% 至 $417M。","source":"nVent Q3 2026 press release","url":"https://s22.q4cdn.com/268397047/files/content_files/Q3-2026-NVT-Press-Release.pdf","excerpt":"Systems Protection Three months ended September 30, September 30, % / point 2026 2025 change $1,098 $716 53% Net Sales Organic Adjusted ROS 23.0% 20.4% 54% 260 bps Electrical Connections Three months ended September 30, September 30, % / point 2026 2025 change $417 $338 23% Net Sales Organic Adjusted ROS 28.2% (1) Certain figures presented in the tables are rounded. (more) 30.0% 23%","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"NVIDIA 800 VDC 機架架構預計 2026 下半年量產，開放規格有 80 多家廠商支持（含 ABB、Eaton、Schneider、Vertiv）；資料中心電力配電由 415V AC 轉向 800V DC 為產業技術轉向（搜尋摘要未提及 nVent 本身是否受影響）","source":"StorageReview：NVIDIA moves 800 VDC power architecture from concept to production","url":"https://storagereview.com/news/nvidia-moves-800-vdc-power-architecture-from-concept-to-production-just-dont-turn-off-ac-power-yet","excerpt":"An open specification is backed by more than 80 manufacturers, including ABB, Eaton, Schneider Electric, and Vertiv","as_of":"2026-08-26","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"nVent 搜尋結果中未見浸沒式或其他冷卻替代技術被列為對 nVent 的威脅；報導多為液冷需求與產能擴張（液冷僅占資料中心冷卻 10-15%）","source":"Zacks/Nasdaq 等對 nVent 液冷與 Q2 財報報導（搜尋摘要）","url":"https://www.nasdaq.com/articles/can-ai-data-center-demand-keep-driving-nvent-electrics-growth","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K 仍描述產品主要經電氣經銷商、零售、承包商與OEM銷售，成功取決於強大通路與經銷網絡；未見訂閱化／D2C／平台化的結構性轉變描述。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm","excerpt":"As many of our products sell through electrical distributors, retail, contractors and original equipment manufacturers, our success also depends on building and partnering with a strong channel and distribution network.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q4 2025 財報分析：基礎設施占營收約45%，組合轉向資料中心（第三方趨勢媒體報導）。","source":"HVACR Trends: nVent Q4 2025 earnings portfolio transformation","url":"https://hvacrtrends.com/nvent-q4-2025-earnings-portfolio-transformation/","excerpt":"Infrastructure, which now represents 45% of nVent’s total revenue, drove organic growth of 50 to 70% in Q4. Data center sales alone hit roughly $1 billion for the year, up more than 50% and about 40% organically.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 財報（8-K）將 FY2026 調整後 EPS 指引由 $5.00–5.10 上調至 $5.36–5.39，報告營收成長 48%–49%；Q4 調整後 EPS 指引 $1.30–1.33。2026 年每季皆上修、無下修。","source":"nVent Q3 2026 press release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001720635/000162828026068391/q32026nvtpressrelease.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 財報（2026-07-31）時 FY 調整後 EPS 指引由 $4.45–4.55 升至 $5.00–5.10，對比分析師預期 $4.60；營收指引 $5.3–5.4B 對比共識 $5.0B；Q3 EPS 指引 $1.35–1.38 對比預期 $1.18。指引高於當時共識。","source":"MarketBeat: nVent Electric updates FY 2026 earnings guidance (2026-07-31)","url":"https://www.marketbeat.com/instant-alerts/nvent-electric-nysenvt-updates-fy-2026-earnings-guidance-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"目標價共識（約 8 月底）：Bullstory 平均 $204.07（15 位分析師，低 $136、高 $240）；Investing.com 12 個月平均 $202.13；TickFlow 8/1 平均 $188.22（17 位）。各聚合站數字不一，MarketBeat/TipRanks 部分數字疑過期。尚未找到 11 月更新。","source":"Bullstory / Investing.com / TickFlow（搜尋摘要）","url":"https://bullstory.io/en/stocks/nvt/forecast/analyst-rating","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Seeking Alpha 修正頁（無日期）顯示營收 12 次上修 0 次下修、EPS 2 次下修；日期不明僅供參考。","source":"Seeking Alpha NVT earnings revisions","url":"https://seekingalpha.com/symbol/NVT/earnings/revisions","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"nVent 於 2026-10-01 完成收購 Maverick Power, LLC，現金約 17.5 億美元，另有 2027–2028 績效條件下最多 5.5 億美元額外對價；協議簽於 2026-08-21（搜尋摘要轉述自 10-Q）。","source":"SEC EDGAR 10-Q (period 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001720635/000162828026068596/nvt-20260930.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共12份，含重大項目者4份；2026-09 有 8 億美元 6.150% 2036 年到期優先債發行（Hoffman Schroff 發行）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001720635&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 12 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K 法律程序僅列商業糾紛、產品責任、石棉、環境等例行事項，未列證券集體訴訟、SEC 調查。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm","excerpt":"We have been made parties to a number of actions filed or have been given notice of potential claims relating to the conduct of our business, including those pertaining to commercial disputes, product liability, asbestos, environmental, safety and health, patent infringement and employment matters.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"nVent 於 2026-10-01 完成收購 Maverick Power, LLC，現金約 17.5 億美元，另有最多 5.5 億美元績效對價（搜尋摘要轉述自 10-Q）。","source":"SEC EDGAR 10-Q (period 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001720635/000162828026068596/nvt-20260930.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"經查一手紀錄，FY2025 10-K 法律程序僅列例行商業/產品責任/環境等事項，無證券集體訴訟；搜尋亦未見相關案件。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm","excerpt":"We have been made parties to a number of actions filed or have been given notice of potential claims relating to the conduct of our business, including those pertaining to commercial disputes, product liability, asbestos, environmental, safety and health, patent infringement and employment matters.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單中未見 Item 4.02（財報不可信賴）；搜尋亦未見 SEC 調查或重編。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001720635&type=8-K","excerpt":"2026-10-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 13 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"NVT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.97,"operating_margin_pct":17.1,"fcf_margin_pct":11.95,"rd_intensity_pct":1.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVT","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"HUBB","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.36,"operating_margin_pct":20.21,"fcf_margin_pct":14.07,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HUBB","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ETN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.9,"operating_margin_pct":17.71,"fcf_margin_pct":13.1,"rd_intensity_pct":2.81},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"VRT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.12,"operating_margin_pct":20.35,"fcf_margin_pct":23.74,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SU.PA","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SU.PA"},"note":"quarterly_income_stmt 無資料"}],"subject":"NVT"},"financial_history":{"ticker":"NVT","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":2295100000.0,"revenue_yoy_pct":null,"gross_margin_pct":35.85,"operating_margin_pct":13.46,"net_income":399800000.0,"diluted_eps":2.38,"free_cash_flow":354100000.0,"fcf_margin_pct":15.43,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":2668900000.0,"revenue_yoy_pct":16.29,"gross_margin_pct":40.29,"operating_margin_pct":17.34,"net_income":567100000.0,"diluted_eps":3.37,"free_cash_flow":462500000.0,"fcf_margin_pct":17.33,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":3006100000.0,"revenue_yoy_pct":12.63,"gross_margin_pct":40.22,"operating_margin_pct":17.53,"net_income":331800000.0,"diluted_eps":1.97,"free_cash_flow":569100000.0,"fcf_margin_pct":18.93,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":3893100000.0,"revenue_yoy_pct":29.51,"gross_margin_pct":37.74,"operating_margin_pct":15.84,"net_income":710200000.0,"diluted_eps":4.31,"free_cash_flow":371900000.0,"fcf_margin_pct":9.55,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/NVT/NVT_Q3_2026_Earnings_Call_20261030.md）

# Q3 2026 Earnings Call
**nVent Electric plc** | Earnings Calls | 2026-10-30

**Operator** (Operator):
Good day, and welcome to the nVent Electric Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please note this event is being recorded. I would now like to turn the conference over to Tony Riter, Vice President of Investor Relations. Please go ahead.

**Tony Riter** (Executives):
Thank you, and welcome to nVent's Third Quarter 2026 Earnings Call. On the call with me are Beth Wozniak, our Chair and Chief Executive Officer; and Gary Corona, our Chief Financial Officer. Today, we'll provide details on our third quarter performance and outlook for the fourth quarter and an update to our full year outlook. 
All results referenced throughout this presentation are on a continuing operations basis unless otherwise stated. Before we begin, let me remind you that any statements made about the company's anticipated financial results are forward-looking statements subject to future risks and uncertainties, such as the risks outlined in today's press release and nVent's filings with the Securities and Exchange Commission. 
Forward-looking statements are made as of today, and the company undertakes no obligation to update publicly such statements to reflect subsequent events or circumstances. Actual results could differ materially from anticipated results. Today's webcast is accompanied by a presentation, which you can find in the Investors section of nVent's website. 
References to non-GAAP financials are reconciled in the appendix of the presentation. We'll have time for questions after our prepared remarks. With that, please turn to Slide 3, and I will now turn the call over to Beth.

**Beth Wozniak** (Executives):
Good morning, everyone. I am pleased to share with you our outstanding third quarter results and cover some key business highlights. We had another tremendous quarter with record sales, orders and earnings, well ahead of our guidance. The better-than-expected sales were broad-based with double-digit growth across all verticals and geographies. In Q3, for total nVent, we continue to have strong orders and backlog. 
Organic orders grew low double digits on top of 65% growth a year ago. In addition, backlog remained healthy and grew sequentially to $2.6 billion. We also closed on the Maverick Power acquisition on October 1. Maverick brings to nVent a new power distribution platform and increases our offerings in data centers. 
We are raising our full year sales and EPS guidance to reflect our outstanding third quarter performance and continued broad-based growth led by data centers. Our guidance also incorporates the Maverick Power acquisition. Now on to Slide 4 for a summary of our third quarter performance. 
Sales were up 44%, both on a reported and organic basis, led by the infrastructure vertical. New products contributed approximately 30 points to our sales growth, and we launched 24 new products in the quarter. Adjusted operating income grew 57% year-over-year with return on sales up 190 basis points. Adjusted EPS grew 67%, and we had robust free cash flow. Sales grew double digits across all verticals. 
Infrastructure led the way with organic sales up over 70%, primarily driven by outstanding growth in data centers. Industrial grew in the high teens and commercial resi grew mid-teens. Turning to organic sales by geography. All geographies grew double digits, led by the Americas growing approximately 50%. Europe was up low double digits and Asia Pacific grew double digits. 
Infrastructure represents our largest long-term growth opportunity, driven by the powerful secular trends of electrification, sustainability and digitalization. We expect the infrastructure vertical to deliver record double-digit organic growth this year with data center expansion and the need for power. We also forecast continued strong growth in 2027. 
We have been investing in new capacity for liquid cooling, engineered building solutions, power connections and cable management. This week, we announced a new 400,000 square foot facility in Arizona for engineered buildings that will expand our capacity to support growing demand in data centers and power utilities with production expected to begin in mid-2027. 
In our high-growth areas within infrastructure, our suppliers are working to keep pace with our growth and are also investing in capacity expansions. It is a lot of work to increase volumes with the velocity required. We are partnering closely with our suppliers to help ensure we are scaling rapidly together. 
Turning to industrial and commercial resi. We expect each to grow organic sales high single digits for the year versus mid-single digits previously. We see industrial growth as broad-based and see improving demand trends across our short-cycle portfolio. I want to thank our nVent team for focusing on our customers and achieving record performance levels. 
This wraps up my opening remarks. I will now turn the call over to Gary for further details on our third quarter results as well as our updated outlook. Gary, please go ahead.

**Gary Corona** (Executives):
Thank you, Beth. We had another excellent quarter, exceeding our guidance with record sales and adjusted EPS. Let's turn to Slide 5 to review our results. Sales of $1.515 billion were up 44%, both on a reported and organic basis as compared to last year. This was well ahead of our guidance, driven by broad-based growth led by very strong data center sales. 
Adjusted operating income was $335 million, up 57%. Return on sales came in ahead of expectations at 22.1%, up 190 basis points versus last year. Price plus productivity offset inflation of nearly $60 million, including approximately $20 million in tariff impact. We also continued to make investments for growth in data centers and power utilities. 
We had record adjusted earnings, well ahead of the high end of our guidance, driven by exceptional sales growth and execution by the team. Adjusted EPS grew 67% year-over-year to $1.52. We generated robust free cash flow of $268 million. 
Now please turn to Slide 6 for a discussion on the third quarter segment performance. Starting with Systems Protection. Sales of $1.098 billion increased 53%. Organic sales grew 54%. Sales growth was broad-based with double-digit increases across all verticals and geographies. 
Infrastructure led the way, growing approximately 90%, driven by continued strength in data centers. Industrial and commercial resi each grew in the teens. Geographically, the Americas delivered very strong double-digit growth, while Europe grew low double digits. 
Asia Pacific also delivered double-digit growth in the quarter. Third quarter segment income was $253 million, up 73%. Return on sales of 23% increased 260 basis points year-over-year on strong volume, price and productivity. 
Moving on to Electrical Connections. Growth exceeded expectations, reflecting continued momentum on our growth initiatives in infrastructure and industrial and stronger demand in commercial resi. 
Sales of $417 million increased 23% on both a reported and organic basis. Growth was broad-based across all verticals and geographies, all growing double digits. From a vertical perspective, infrastructure and industrial each grew strong double digits. Commercial resi was up high teens. 
Geographically, Americas grew strong double digits, while Europe was up mid-teens. Asia Pacific also grew double digits in the quarter. Segment income was $118 million, up 16% versus last year. Return on sales of 28.2% was down 180 basis points year-over-year. 
The margin performance was impacted by inflation and investments for growth, partially offset by strong volume, price and productivity. Importantly, margins improved sequentially as expected. 
Turning to the balance sheet and cash flow on Slide 7. In addition to our strong free cash flow on the quarter, we issued $800 million of 10-year senior notes near quarter end to help fund the Maverick Power acquisition. As a result, we ended the quarter with more than $1.1 billion in cash on hand and total debt of $2.2 billion. 
We also had $600 million available on our revolver. Including the Maverick Power acquisition, we expect our leverage to be well within our target range of 2 to 2.5x by the end of the year. Our healthy balance sheet and strong liquidity provide financial flexibility to support our disciplined capital allocation strategy. 
Turning to Slide 8 on capital allocation, where we outline how we deploy capital to drive growth and sustain financial outperformance. Our framework has been consistent and is centered on disciplined growth investments and rigorous execution of our M&A strategy while maintaining the balance sheet flexibility to consistently return capital to shareholders. Our capital allocation priority is growth. This starts with reinvesting in the business by funding capacity expansion, innovation and the capabilities required to win in high-growth verticals. This year, we expect to invest approximately $140 million in CapEx, up 50%, inclusive of the Maverick Power acquisition. 
We have spent $95 million year-to-date. Most of this increased investment is for new capacity to support growth in data centers, power utilities and supply chain resiliency. Year-to-date, we returned $202 million to shareholders, including share repurchases of $100 million, and we have increased our quarterly dividend by 5% compared to last year. 
Overall, our disciplined capital allocation approach positions us to prioritize growth and create long-term shareholder value. 
Moving to Slide 9. As Beth shared earlier, we are significantly raising our full year sales and EPS guidance again due to our strong performance in Q3, momentum across our portfolio and the addition of Maverick Power. 
We now forecast reported sales growth of 48% to 49%, up from 37% to 39% previously. We are increasing our organic sales growth guidance. We now expect to grow 38% to 39% versus our prior guidance of 32% to 34%. We are raising our full year adjusted EPS range to $5.36 to $5.39 versus our prior guidance of $5 to $5.10. 
At the midpoint, adjusted EPS is expected to grow 60% versus last year. A few updated assumptions for modeling purposes. Acquisitions are expected to add approximately 10 points to sales growth, now including Maverick Power. Please note, Maverick Power will be reported as part of our Systems Protection segment. 
Tariff impact is expected to be approximately $105 million, up from $100 million previously. Corporate costs are expected to be approximately $145 million compared to $140 million previously. And adjusted net interest is now expected to be approximately $88 million for the year. 
Looking at our fourth quarter outlook on Slide 10, we forecast reported sales growth of 45% to 48%, with Maverick Power contributing approximately 19 points to sales growth and foreign exchange roughly flat. Organic sales growth is expected to be up 26% to 29%. We continue to see very strong demand, particularly in data centers and power utilities. 
As Beth mentioned, we are working closely with our suppliers to support the pace of growth and have reflected the current environment in our guidance. Price and productivity are expected to offset the impact of inflation, including tariffs, and we continue to invest for growth, particularly in data centers and power utilities. 
We expect Maverick to contribute a few cents to adjusted EPS in the quarter, inclusive of the higher interest expense associated with the financing of the acquisition. For the fourth quarter, we forecast net interest expense of approximately $39 million. 
And adjusted EPS to be between $1.30 and $1.33, which at the midpoint reflects more than 45% growth versus last year. Overall, we expect a strong finish to an outstanding year. I will now turn the call back over to Beth.

**Beth Wozniak** (Executives):
Thank you, Gary. Please turn to Slide 11. Our portfolio transformation to become a more focused, higher-growth electrical connection and protection company is showing up in our results. We have intentionally increased our exposure to the high-growth infrastructure vertical through both organic investments and M&A. 
Infrastructure made up 12% of sales at spin, expanded to 45% last year and is nearly 60% year-to-date. Including Maverick Power, our 2026 sales are expected to be approximately 3x what they were at spin and nearly 50% higher than last year. Overall, our total opportunity is now over $150 billion.
Turning to Slide 12 and an overview of Maverick Power. Maverick Power is a leading manufacturer of engineered power distribution and infrastructure solutions for data centers. The acquisition broadens our exposure to the high-growth infrastructure vertical and adds a new power distribution platform that is highly complementary to our existing data center offerings. Maverick's portfolio includes low and medium voltage switchgear and switchboards, integrated modular solutions and services. 
Maverick also brings significant scale and capabilities to nVent with more than 1,000 employees with key sites in Texas and Arizona and approximately 1.5 million square feet of manufacturing footprint. 
Looking ahead, Maverick's strong engineering capabilities expand our offerings into new power architectures and strengthens our ability to provide more system-level solutions and services for data center customers. 
We plan to show Maverick's new 800-volt DC power rack at Supercomputing next month. Positioned alongside the IT rack, it integrates power conversion, protection and controls to convert existing AC power to 800-volt DC supporting high-density AI computing without a facility-wide power redesign. And importantly, Maverick meaningfully expands our offerings in data centers. With Maverick, we estimate nVent's total data center opportunity expands to approximately $2 million per megawatt. We believe the combination of our complementary portfolios, engineering capabilities and customer relationships create significant opportunities to grow together and deliver even more value for our data center customers. 
Wrapping up on Slide 13, we had another tremendous quarter with record sales, orders and adjusted EPS. We continue to deliver broad-based growth with infrastructure leading the way and expect another record year, having significantly raised our full year sales and adjusted EPS guidance. We remain very well positioned for the powerful trends of electrification, sustainability and digitalization. 
And are excited about the significant growth opportunities ahead. Our future is bright. With that, I will now turn the call over to the operator to start Q&A.

**Operator** (Operator):
[Operator Instructions] The first question today comes from Julian Mitchell with JPMorgan.

**Julian Mitchell** (Analysts):
Just wanted to start off on the top line outlook. Maybe just give us a little bit of context around the planning behind the latest capacity addition you've announced and when you might sort of open up the order book for that. And when you're thinking about orders, it was a good result of a very difficult comp. Is it natural to assume that, that rate accelerates given the demand backdrop?

**Beth Wozniak** (Executives):
Well, Julian, thank you for the question. So to start, we just announced a new facility in Arizona, which will start to begin production, as I said in my prepared remarks, midway through 2027. We also announced Blaine 2, which is another site for liquid cooling and data center solutions. And so again, that also will be into production going into mid first half 2027. 
So we're looking ahead as we see order rates and some of our backlog as to where we need capacity. And with respect to orders, we are absolutely have a difficult comp that we had to overlap in Q3. But I will say this, starting off Q4, orders are very -- in October, orders are very strong.

**Julian Mitchell** (Analysts):
Got it. That's helpful. And then just my second question would be around the operating margins. So it looks like they're pegged at about 20% in the fourth quarter in the guidance. So sort of flattish year-on-year. Maybe just unpack that a little bit. Are you seeing maybe bigger cost headwinds? Is it something to do with the margin that Maverick Power is coming in at of about $200 million of revenue? Any thoughts around that, please?

**Gary Corona** (Executives):
Yes, sure. Julian, this is Gary. I'll start by saying we are pleased with the margin performance in the third quarter. Margin up almost 200 basis points, incrementals well into the mid-20s. In the fourth quarter, we do expect margins to be up year-on-year approximately 60 basis points at the midpoint. And you put your finger on a bit of a headwind in the fourth quarter. 
Excluding Maverick, we'll have incrementals well in the mid-20s, which is our target. But Q4 will be an investment quarter for Maverick as we prepare to grow strongly in 2027. And that will put margin incrementals more into the low 20s. So approximately 60% margin -- 60 points of margin growth -- basis points of margin growth in the fourth quarter, and the core business has nice incrementals.

**Operator** (Operator):
The next question comes from Nigel Coe with Wolfe Research.

**Nigel Coe** (Analysts):
So Maverick, stick with Maverick. So the Arizona expansion, is that more Maverick products than core nVent? And then maybe if you could just give us a few more details on Maverick. Can you disclose the backlog acquired with Maverick and this investment spending, how does that profile look through 2027?

**Beth Wozniak** (Executives):
Okay. So to start with, the new Arizona facility is actually for our engineered building solutions. So recall, that is the combination of Trachte and Avail EPG. So this is to create those solutions that support both utilities and data centers and a lot of integration work. 
So that's what that facility is about. With respect to Maverick, we have not included a backlog yet. That is something that we will do, but I will say this, it is very healthy backlog. And some of the investments that are being made is we mentioned that they have 1.5 million square feet. And so they are fitting that out currently as they start to see this nice trajectory as we go into 2027 of growth and the backlog in the orders. So we're investing in that capacity there to bring them up to speed and online.

**Nigel Coe** (Analysts):
Great. And then Maverick, if you look at some of their competitors, the growth profile is, in many cases, 50% plus and in some cases, as high as 100% for 2027. Is that the kind of growth profile you expect to see for Maverick next year?

**Beth Wozniak** (Executives):
Well, we're not -- we're focused on our current integration. I'll just remind you, it's only been 30 days, but we do expect strong double-digit growth in Maverick as we go forward.

**Operator** (Operator):
The next question comes from Steve Tusa with Wells Fargo.

**Charles Stephen Tusa** (Analysts):
The -- just to put a finer point on that, I guess, when you say well into the mid-20s incrementals, I know we're talking about like tens of basis points here sometimes, but that would suggest Maverick kind of in the mid-teens from a margin perspective, like an operating margin perspective?

**Gary Corona** (Executives):
That's exactly right, Steve. That's what we're expecting in the fourth quarter for Maverick.

**Charles Stephen Tusa** (Analysts):
Okay. And then just into next year, I know there's a bit of inflation out there to say the least. How are you looking at -- what was -- what do you expect price to be for this year? And then how do you think about more actions? Do you need more actions to drive price cost next year?

**Gary Corona** (Executives):
Yes. So Steve, in the third quarter, price and productivity more than offset the $60 million of inflation that we saw and price nearly covered it on its own. Our investments behind capacity and capability were significant. We've had a long track record of leveraging price to offset inflation as well as productivity and the teams are working diligently to ensure that we forecast that's the case for Q4 and next year.

**Operator** (Operator):
The next question comes from Jeff Hammond with KeyBanc Capital Markets.

**Jeffrey Hammond** (Analysts):
So I know we've had a lot of questions on this new modular liquid cooling product, but there seems to be some confusion on when you start taking orders? Did you start taking orders in the third quarter? Or what's the timing around that? And then just kind of the uptake and interest. I know maybe it was initially for distribution, but the initial interest seems to be broader than that.

**Beth Wozniak** (Executives):
Yes. So we have been taking orders for our new modular cooling products and platforms. We'll also be showcasing that at Supercompute. There is a lot of interest in this product. And we have said before, we wanted to make it modular because it allows us to configure it to various types of customers and sell through distribution. But certainly, there is significant interest in this product from all types of data center companies. So it really is a broad-based platform with a lot of flexibility, and we're very excited that it gets to launch here in the back half of the year.

**Jeffrey Hammond** (Analysts):
Okay. Great. And then you mentioned the Maverick 800-volt DC. And I guess we keep hearing, one, next-gen chips, needing more liquid cooling intensity, but also 800-volt DC having a lot more liquid cooling intensity. So I'm just wondering kind of your approach and what you're seeing from early ops, both with maybe incorporating your liquid cooling into Maverick and other customers around 800-volt DC and just give us some parameters around that opportunity.

**Beth Wozniak** (Executives):
Okay. So as we know, the chips require more power, more power means more heat, more heat means more cooling. So as we think about the future, the demand for liquid cooling is only going to increase. And as we think about these higher voltages, we're positioned well to think about our modular platform, how we can convert it and meet those needs. 
Similarly, on the power side, now having Maverick in our portfolio, they have an 800-volt DC offering. We're going to showcase that at Supercompute. I think as we think about cooling and power now having that in our portfolio, it gives us more opportunities to provide system solutions and different architectures. 
So we're excited. We're going to showcase some of this, like I said, at Supercompute and we'll be working on the road map, and we'll have more to share in the future.

**Operator** (Operator):
The next question comes from Jacob Levinson with Melius.

**Jacob Levinson** (Analysts):
Maverick seems like a nice add for you folks. But can you give us a sense of -- are there other assets out there of that scale? Or maybe said a different way, are there gaps in the portfolio that you're still looking to fill through M&A?

**Beth Wozniak** (Executives):
Well, we have -- and we've always said this, we have a very healthy M&A pipeline. And we have a flywheel that we've been very -- that we've had in place for a while because we're very disciplined about this and it is very strategic. I never say we have gaps in the portfolio, but more so, we have opportunities to extend what we do. 
And if you think about our portfolio transformation, we have intentionally focused on infrastructure. So you've seen us do deals in the last little while in the data center space, in power utilities. And I think there are opportunities out there. We're also very disciplined in how we think about that value creation because we buy companies that we can invest in to grow and scale and then want to ensure that we can get good returns. 
So I feel we have lots of opportunity there. And we certainly, at our Investor Day earlier in the year, said we're going to see acquisitions contribute several points to our growth year-over-year. And I'd expect us to do some deals every year, and we have a good integration playbook.

**Gary Corona** (Executives):
Jacob, I would just add, as I mentioned in my prepared remarks, the balance sheet is healthy, and we expect to end the year within our targeted leverage range.

**Jacob Levinson** (Analysts):
Okay. That's helpful. And just on a different topic, it seems like there's been a notable pickup overseas. Is that -- how much of that is just the data center build-out starting to really come through in Europe and Asia? Or is that your more traditional industrial commercial markets recovering from depressed levels?

**Beth Wozniak** (Executives):
Well, when we look at Europe and Asia, actually, our growth is very broad-based. Certainly, we see the data center space growing and those opportunities are increasing there. But we're very pleased to say that industrial and our commercial resi and infrastructure and power utilities, we just saw a nice broad-based growth.

**Operator** (Operator):
The next question comes from Joe O'Dea with Vertical Research.

**Joseph O'Dea** (Analysts):
Could you just add a little bit of perspective on the capacity ramps, talking about the timing of the production volume ramp at Blaine 1 and 2 as well as kind of Arizona and what you'll see through the first half of next year. Really looking for any detail on the time line to reach scale efficiency and then ultimately, what it means for revenue capacity versus your current footprint?

**Beth Wozniak** (Executives):
Okay. So Blaine 1, we are in production, and it's been ramping up, and we're actually very pleased. And earlier in the year, we said even -- it was 100 days from when we -- business days to get that factory up and going. And I think that was like a record for us. And so it's off to a great start and improving and improving efficiencies. 
Blaine 2 will not come online until about midway through next year. And similarly, this new Arizona site for engineering building solutions, that also is mid-2027. And then we expect those take time to ramp up. But when we look at our backlog and opportunity, we plan those investments to allow us to start meeting the capacity demand in 2027.

**Joseph O'Dea** (Analysts):
And then just on the product launches that you highlighted in the prepared remarks, any common denominators around kind of capabilities or solutions that you're adding in terms of serving particular kind of customer needs?

**Beth Wozniak** (Executives):
Well, when we look at our product opportunities, we actually prioritize all of our new products in those high-growth verticals. So it's an array of things from our Systems Protection group, where we're developing new solutions in power and cooling, for example. It's also in our Electrical Connections group, where we look at some of our power connections and some of our other products aligned to the needs of utilities or data centers. So overall, we always think about how do we differentiate, how do we innovate because new products not only drive growth, but they're always margin accretive as well.

**Operator** (Operator):
The next question comes from Vlad Bystricky with Citi.

**Vladimir Bystricky** (Analysts):
So just sticking with Maverick for a second and maybe a little more broadly. You mentioned that Maverick, in addition to their product portfolio, brings some service capabilities. So can you talk about your overall service offering for data center customers today and how that's evolving and sort of where you see the service opportunities going in '27 and beyond?

**Beth Wozniak** (Executives):
Yes. So Maverick does have a service capability to support their offerings. We also have been building a service capability around our liquid cooling portfolio. And as we launch our new modular platform, we believe because that will serve a wide array of customers, that ability to help install, help in commission, help provide regular support is critical. 
So we have this opportunity, as I said, that this now expands our service opportunity with Maverick between what we do in liquid cooling and what we have in Maverick, I think we're going to be able to provide further solutions for our data center customers. So we're building out a strong service capability. And I think it's important, especially with more new products and with the breadth of the portfolio.

**Vladimir Bystricky** (Analysts):
That's helpful. Appreciate that, Beth. And then just on the capacity side, I know you talked about Blaine and Arizona. You mentioned that Maverick was still sort of outfitting or building out their 1.5 million feet -- square feet of capacity. So can you just talk about sort of the time line to Maverick's capacity ramp and when you see that coming more available?

**Beth Wozniak** (Executives):
Well, they've opened a lot of facilities over the last little while. And I would say, much like we have with these new facilities, it's ramping and it's going to provide capacity that is needed in 2027. So I think that continues to ramp through the first half of next year.

**Operator** (Operator):
The next question comes from Alexander Virgo with Evercore ISI.

**Alexander Virgo** (Analysts):
A little bit to the new product introductions. Contribution of growth in the quarter was 30% or so. I guess the lapping tougher comps as we go into Q4. But just wondering if you could give us a sense of that cadence into the end of the year. And then I guess, thinking about what that does as it wraps around into 2027. I appreciate you haven't given us any guidance for '27 yet, but obviously, starting to think about the order momentum, the backlog and that new product -- those new product dynamics sort of building into the model in the '27 numbers.

**Beth Wozniak** (Executives):
Well, one of the things that we said at our Investor Day is that we wanted to have our new product vitality at around 30%. And we're effectively at that level. And to be able to do that, it means you have to innovate faster, you have to come up with new things. And certainly, as we focus our portfolio on to these high-growth verticals, we see that ability to do so. 
And certainly, with data center growth, a lot of our new products are focused there. And so that's where we're seeing that tremendous uplift. And that's what will be our continued focus as we go into 2027. And it's important, new products are -- have been a key driver of our growth. As we think about our strategy, high-growth verticals, it's new products, it's growing globally and then it's growth through M&A. 
So I think we've got a good pipeline of what we're working on, some good innovation, and we expect it to be a significant contributor to our overall performance of our portfolio.

**Operator** (Operator):
The next question comes from Neal Burk with UBS.

**Neal Burk** (Analysts):
So another question about Maverick. So just trying to think about the implications of Maverick doubling your content in data centers to $2 million per megawatt. I mean this is probably simplistic, but does that mean that over time, your data center revenues could double from what they were before the acquisition? Maverick revenues started around $700 million. So clearly, that isn't the impact right out of the gate, but just trying to think about the growth opportunity over time.

**Beth Wozniak** (Executives):
Well, it certainly allows us as we bid on new projects or new data center opportunities, we have more content and more capability. And not to mention, as I said previously, the ability for us to think about cooling and power and everything that we bring together, we certainly have greater opportunity. 
And I think it's -- it really for us is about just ensuring that as we see into the future about 800-volt DC and other needed solutions, having power and cooling, we think, is very complementary.

**Neal Burk** (Analysts):
And one follow-up on orders. You clearly had a really tough 3Q comp of last year. Orders were very strong. Are those now fully recognized in revenue at this point? I ask because you've had 2 quarters now organic sales grew well above orders, which are sort of low double digits. So I'm just trying to understand like conceptually, I know you don't like to talk about future orders. 
But just conceptually, can we continue to see the sort of 30 to 40 plus top line growth that we've been seeing when orders are sort of growing well below that? Or would you expect these to sort of converge over time?

**Gary Corona** (Executives):
So this is Gary. I'll take that. And what I -- what's important to remember is that we've talked about orders being lumpy and the timing of those orders being lumpy. But I'll look at the 2-year stack of orders for us just this quarter, and it's very strong. And you look at what Beth's comments were about October, as our business continues to evolve to more long cycle, we expect that backlog to build, especially as Maverick Power comes into our portfolio and we report them with the broader business.

**Operator** (Operator):
The next question comes from Varun Govindaraj from Bernstein.

**Varun Govindaraj** (Analysts):
I wanted to understand how you think about opening new facilities and what you sort of look for before making that decision? Is it more just broader demand trends? Or do you need to see some level of customer commitment before breaking ground?

**Beth Wozniak** (Executives):
Well, it's a combination of many things when we look at a new facility. We look at, in some cases, the orders that we have on hand or orders that we can't fulfill, so to speak. We look at just what we see our customers telling us, and it's multiple factors there that we then decide to make that investment. So it's very prudent. 
We have a good sense of direction of where the market is headed, what our customers are saying, what the opportunities are. And then we are very disciplined, as you can expect, in terms of how we think about those returns. And I think Gary always likes to say those returns are very good every time that we've invested in new capacity expansion.

**Gary Corona** (Executives):
Yes. Just to build on the discipline, we go back and take a look at our significant investments and ensure that they're delivering the returns that we expected. And many times, they have over-delivered our initial expectations from an ROI perspective.

**Varun Govindaraj** (Analysts):
Absolutely. And then just as a quick follow-up. Can you talk about any of the actions you're taking right now on supply chain resilience? Obviously, at this level of growth, your suppliers are probably stretched as well. So anything you can share there would be helpful.

**Beth Wozniak** (Executives):
Yes. Certainly, as we see this growth rate and the velocity and the demand and the ability to respond, I mentioned 100 days for us, many of our suppliers, they too are having to add capacity. Sometimes that is new lines, sometimes that's new facilities. So we're trying to work hand-in-hand with them to ensure that they understand our forecast, that we're working through bringing new capacity online together because we're only going to be successful if they're successful with us. 
So it's a lot of work. We always say that. We try to be very prudent when we give our guidance given that there's a lot going on from our own capacity expansion to our suppliers as well.

**Operator** (Operator):
The next question comes from Nicole DeBlase from Deutsche Bank.

**Nicole DeBlase** (Analysts):
Just wanted to ask one on 4Q. Gary, the revenue guidance kind of implies flattish total revenue sequentially, which is a bit of a head scratcher just because like Maverick is coming into the mix. And we've obviously seen how strong the backlog and order growth is plus you guys continue to work to add capacity. So just curious if that's like prudence and conservatism, which we've come to expect from nVent or if there's any other reasons we should be thinking about?

**Gary Corona** (Executives):
Yes. Thanks, Nicole. Our Q4 organic guide is still quite healthy and the 2-year stack is still over 50%. So great growth for us. It is a tick down. Some of that is seasonality in our business that we normally see a bit of a step back. And look, in Q4, we could have -- we could maybe have delivered more. But as Beth talked about, we're navigating and being prudent with our -- how we manage the supply chain, and that's something that is incorporated into our guidance. 
I will say we're really pleased with the year. We're going to grow almost $2 billion year-over-year on a revenue basis and $2 of additional EPS. So we feel really good about the growth that we're delivering in '26.

**Nicole DeBlase** (Analysts):
Understood. And then just coming back on Maverick. I think you said in response to a prior question that it's like mid-teens margins in the fourth quarter. Does that incorporate some of the growth investments that you're making? And I guess the question is, like as you look out over the next several years and integrate Maverick, do you think it has the potential to get to Systems Protection or nVent average margins?

**Gary Corona** (Executives):
Yes, Nicole, exactly. Significant ramp happening in Maverick, and we've incorporated those investments into our guide. We expect those margins to improve both from the growth and fully utilizing those facilities that Beth talked about. It's only 30 days, so I'm not ready to strike the exact expectations for Maverick margins, but we do expect them to certainly improve as we get into '27 and beyond.

**Operator** (Operator):
The next question comes from Luke Junk with Baird.

**Luke Junk** (Analysts):
Beth, another Maverick question, but I want to take it in a little different direction in terms of a strategic question. Just be curious to get your color on initial engagement with customers, either after announcing the deal or now that you've owned it for about a month here, just in terms of walking them into your current relationships and starting to lay the groundwork for selling thermal and power as a system-level solution.

**Beth Wozniak** (Executives):
Well, certainly, we had very favorable reaction to the acquisition, both from our nVent customers and from Maverick's customers because they know that just the capabilities that each company has, there's more that we can bring together. And as we think about the opportunity, certainly, there -- as in anything, we look at these synergies around growth about -- if you think about we have developed over the last several years, a very strong commercial organization, which we believe with Maverick's offering, we're going to have the opportunity to drive their reach beyond what they had today. 
So overall, I think these are -- it's a great new platform for us and very complementary to what we do, and it kind of follows our flywheel of we find companies that have great products that we can invest in and scale to grow.

**Luke Junk** (Analysts):
Got it. And then for my follow-up, I'll ask on Electrical Connections. Not sure if we got the question in Q&A yet. I'm just curious, were you surprised to see the growth accelerate sequentially there? I think it's maybe a bit better than expectations and kind of unpacking that any of the upside drivers on that low 20s plus kind of growth rate.

**Gary Corona** (Executives):
Luke, you were cutting in and out. We could not understand that question. Not sure if it's on your end or...

**Luke Junk** (Analysts):
Yes. Let me try it again here. Yes, let's go...

**Gary Corona** (Executives):
Much better.

**Luke Junk** (Analysts):
Yes, growth accelerating there. I think that was a bit better than your expectations in the low 20-plus range here. Just kind of -- can you unpack what was better than expected there? And any particular drivers that we should be focused on?

**Beth Wozniak** (Executives):
And sorry, you meant the growth rate for -- compared to what?

**Gary Corona** (Executives):
Connections...

**Luke Junk** (Analysts):
Electrical Connection versus expectations and accelerating sequentially.

**Beth Wozniak** (Executives):
Yes. We had another great quarter for Electrical Connections. And I think it speaks to our focus on our growth initiatives. So as you know, that has always been a very strong segment focused on commercial. And we've had the product portfolio there, we focused it on infrastructure and industrial as well as some of our commercial actions. 
So we've seen significant growth opportunities. New products are contributing to this. And I would also say one of the things -- and this is not just Electrical Connections, but the nVent portfolio, we are seeing very strong growth through our distribution channel, and that speaks to the broad-based growth that we're seeing across industrial, infrastructure and commercial for that matter.

**Operator** (Operator):
The next question comes from Scott Graham with Seaport Research Partners.

**Scott Graham** (Analysts):
I wanted to first ask about just 40,000 feet data centers. You see what's going on out there with there's pockets of suppliers saying a little slower, a little pause and what have you. Obviously, you're not seeing that. But I'm just wondering your customer conversations, I know it's kind of 2 step, but nevertheless, you get good visibility on sales there reading through to the OEM. 
I'm just wondering, are you seeing any less urgency in that market? I know for a while there is really having trouble keeping up with things and you're adding capacity, I get all of that. But is there a tenor of maybe less urgency for orders in that market?

**Beth Wozniak** (Executives):
So Scott, I will say that we also have direct relationships with those end customers. So we get a lot of feedback that way as well. And no, I would say there is a sense of urgency in terms of are we able to do more. I mean that's more -- do we have more output we respond faster, bring in lead times. 
So we're not seeing that slow at all. If anything, it's just -- I talked earlier in my prepared remarks about the pace of growth and the velocity needed. It's a lot of hard work, and that's continuing.

**Scott Graham** (Analysts):
I appreciate that. I just wanted to maybe ask a follow-up question about the Electrical Connections margin, which has been declining for some time. And historically, I remember with Pentair and even in the early days with you a spinout that pricing was always one of the strengths of this business. 
And I'm just wondering, I know acquisitions were a factor last year, but the continued decline in that segment's margins. Can you kind of give us some color on what -- where that's coming from, again, another 40,000 footer in that way?

**Gary Corona** (Executives):
Yes, Scott, it's Gary, and I appreciate the question. And I'll start with what we're focused on in Electrical Connections right now, which is growth. And to deliver a couple of quarters in a row around 20%, it is breakthrough growth for that business. And a lot of it has to do with the strategy change with focus more on industrial and infrastructure, repositioning the portfolio, and that's really driving that nice growth. 
With that repositioning, we have some mix that is impacting the portfolio. But I will say the team has done a nice job to price away the inflation. And we've been very consistent in kind of what we expected from that business, which is sequential improvement in margins. And I'll take that high 20s margin with approximately 20% growth. So it's been a nice acceleration for that business this year and a bit different than what we had seen in the past.

**Operator** (Operator):
This concludes our question-and-answer session. I would like to turn the conference back over to Beth Wozniak for any closing remarks.

**Beth Wozniak** (Executives):
Thank you for joining us today. We are confident in our strategy and our ability to execute. We have significant growth opportunities ahead and multiple levers to drive continued margin expansion. I'm very proud of our outstanding performance in the third quarter and the continued progress we're making across nVent. We remain focused on delivering for our customers, employees and shareholders. nVent is a top-tier high-performance electrical company, well positioned to win with the powerful trends of electrification, sustainability and digitalization. We're excited about the opportunities ahead. 
Thank you again for joining us today. This concludes our call.

**Operator** (Operator):
The conference has now concluded. Thank you for attending today's presentation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NVT_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜CFO｜guidance：全年報告營收成長財測自 26%–28% 上調至 37%–39%。（原話："reported sales growth of 37% to 39%, up from 26% to 28% previously."）
- 2026-07-31｜CFO｜guidance：全年有機營收成長財測為 32%–34%，前次為 21%–23%。（原話："We now expect to grow 32% to 34% versus our prior"）
- 2026-07-31｜CFO｜guidance：全年調整後 EPS 區間上調至 $5–$5.10（原 $4.45–$4.55）。（原話："raising our full year adjusted EPS range to $5 to $5.10"）
- 2026-07-31｜CFO｜guidance：第三季報告與有機營收成長財測 32%–35%。（原話："we forecast reported and organic sales growth of 32%"）
- 2026-07-31｜CFO｜guidance：第三季調整後 EPS 財測 $1.35–$1.38，中點成長約 50%。（原話："between $1.35 and $1.38, which at the midpoint reflects 50%"）
- 2026-07-31｜CFO｜guidance：全年自由現金流轉換率維持 90%–95%。（原話："we still expect conversion of 90% to 95%"）
- 2026-07-31｜CFO｜guidance：全年關稅衝擊預估由 $80M 增至約 $100M，管理層稱主因為量大幅成長。（原話："tariff impact is expected to be approximately $100 million"）
- 2026-07-31｜CEO｜guidance：2026 年資料中心總銷售預期超過 $20 億，為去年兩倍以上。（原話："center sales to be more than $2 billion in 2026"）
- 2026-07-31｜CFO｜margin：下半年財測內含的增量利潤率假設為 20% 中段。（原話："which is assuming mid-20s incrementals in the second half"）
- 2026-07-31｜CFO｜margin：CFO 說明中期增量利潤率目標為 20% 中段，目的是留空間投資成長。（原話："our midterm target was mid-20s for incrementals"）
- 2026-07-31｜CFO｜margin：公司整體調整後營業利益率 21.9%，較去年 +110bp；價格加生產力抵銷超過 $50M 通膨（含超過 $30M 關稅）。（原話："Return on sales came in ahead of expectations at 21.9%"）
- 2026-07-31｜CFO｜margin：Electrical Connections 利潤率 27.3%，年減 140bp。（原話："Return on sales of 27.3% was down 140 basis points"）
- 2026-07-31｜CFO｜margin：管理層將 EC 利潤率年減歸因於通膨與產品組合，部分被價格與量抵銷。（原話："performance was impacted by inflation and mix"）
- 2026-07-31｜CFO｜commitment：CFO 表示預期 EC 今年利潤率落在 20% 後段（high 20s）。（原話："that's where I expect it to be this year."）
- 2026-07-31｜CFO｜commitment：管理層持續預期以定價、供應鏈生產力與營運措施抵銷通膨（含關稅）。（原話："impact of inflation, including tariffs through pricing"）
- 2026-07-31｜CFO｜commitment：第三季財測稱定價將抵銷通膨衝擊。（原話："Pricing is expected to offset the impact of inflation"）
- 2026-07-31｜CFO｜capital_allocation：全年資本支出維持約 $1.3 億、年增 40%，多用於資料中心、電力公用事業與供應鏈韌性的新產能。（原話："invest approximately $130 million in CapEx, up 40%"）
- 2026-07-31｜CFO｜capital_allocation：上半年回饋股東 $1.18 億，含回購 $5,000 萬。（原話："we returned $118 million to shareholders"）
- 2026-07-31｜CFO｜capital_allocation：淨槓桿 1.2 倍，低於 2–2.5 倍的目標區間。（原話："net leverage of 1.2x, well below our target range"）
- 2026-07-31｜CEO｜capital_allocation：CEO 稱併購管線良好、維持紀律，目標進一步強化基礎設施布局。（原話："on M&A, we have a very good pipeline"）
- 2026-07-31｜CEO｜capital_allocation：宣布第三個明尼蘇達液冷擴產據點 Blaine 2，預計 2027 上半年啟用。（原話："This facility is expected to open in the first half of 2027"）
- 2026-07-31｜CEO｜capital_allocation：Blaine 1 從簽約到開廠約 100 個工作天。（原話："Blaine site within approximately 100 working days"）
- 2026-07-31｜CEO｜capital_allocation：被問 Blaine 2 能否同樣 100 天內開張，CEO 說太積極。（原話："I think that's too aggressive"）
- 2026-07-31｜CEO｜capital_allocation：CEO 說新增產能可支撐需求至 2027 並進入 2028。（原話："that takes us through '27 and into '28 at this time"）
- 2026-07-31｜CEO｜customer：管理層稱基礎設施方面客戶涵蓋超大規模雲端、neo-cloud、多租戶與經銷夥伴。（原話："a wide range of customers from hyperscalers to neo-clouds"）
- 2026-07-31｜CEO｜customer：客戶採購方式有整套購買，也有只買液冷系統一部分；公司表示可在整條價值鏈彈性供應。（原話："we're working with hyperscalers, we're working with colos"）
- 2026-07-31｜CEO｜customer：本季有機訂單成長為低雙位數，積壓訂單 $25 億。（原話："backlog remained healthy at $2.5 billion"）
- 2026-07-31｜CEO｜customer：CEO 稱資料中心訂單大且不均，第三季至今資料中心訂單強勁。（原話："In fact, we've had strong data center"）
- 2026-07-31｜CFO｜customer：CFO 稱積壓訂單多數在 12 個月以內，期限未拉長。（原話："mostly 12 months or less, and that hasn't extended out."）
- 2026-07-31｜CEO｜customer：CEO 稱客戶未必以更長前置期下單，但公司有取得客戶未來需求能見度。（原話："that not necessarily for the -- in the product portfolios"）
- 2026-07-31｜CEO｜customer：CEO 稱經銷商 sell-in 與 sell-out 平衡，短週期需求為實際需求。（原話："it's actually been well balanced"）
- 2026-07-31｜CEO｜customer：CEO 稱 EC 短週期（經銷通路）訂單為轉折點。（原話："it was just a nice inflection point"）
- 2026-07-31｜CEO｜customer：電力公用事業本季成長雙位數。（原話："power utilities grew double digits for us in the quarter"）
- 2026-07-31｜CEO｜customer：資料中心與電力公用事業產能若有取捨，管理層稱會做審慎決策。（原話："we make prudent decisions if there has to be trade-offs"）
- 2026-07-31｜CEO｜customer：管理層稱資料中心正在歐洲與亞洲擴張，公司正投資當地商務與製造。（原話："data centers are expanding in both Europe and Asia"）
- 2026-07-31｜CEO｜product：新產品貢獻銷售成長超過 30 個百分點。（原話："New products contributed over 30 points to our sales"）
- 2026-07-31｜CEO｜product：新一代模組化液冷平台預計今年秋季推出。（原話："modular platform is going to launch later this fall"）
- 2026-07-31｜CEO｜product：CEO 稱正投入液冷產品的服務能力建設。（原話："And as we are also investing in a service capability to"）
- 2026-07-31｜CEO｜product：管理層對 800V DC 的看法：認為有一定應用，但仍有低壓需求，視為延伸機會。（原話："is going to have some application in data centers"）
- 2026-07-31｜CEO｜competition：CEO 稱液冷目前僅占資料中心冷卻的 10%–15%。（原話："maybe it's now 10% to 15% of cooling in"）
- 2026-07-31｜CEO｜risk：對 Q3 財測，CEO 說因產能爬坡需配置設備、人力與供應商，規劃上採審慎。（原話："But as we look forward, we're just being prudent."）
- 2026-07-31｜CFO｜risk：CFO 稱財測保持審慎以保留執行與投資彈性。（原話："it's important that we're prudent in our guidance"）
- 2026-07-31｜CFO｜risk：CFO 指下半年面對的基期：有機約 20%、EPS 成長約 50%。（原話："we're going to be lapping 20% organic and 50% EPS growth"）
- 2026-07-31｜CEO｜risk：CEO 談長期能見度：與 NVIDIA 等合作至 2030 路線圖，並稱資料中心建置放緩時液冷仍有汰換週期。（原話："NVIDIA and others on their road maps out through 2030"）
- 2026-07-31｜CEO｜risk：CEO 稱客戶能見度達數年。（原話："we've got a visibility several years out"）
- 2026-07-31｜CEO｜risk：分析師問積壓訂單是否為合適水位，CEO 稱約在合適水準。（原話："it's around the right level"）
- 2026-07-31｜CFO｜customer：被問近 12 個月訂單成長是否高於本季低雙位數，CFO 回答是，未給數字。（原話："Yes, Brian, they are."）
- 2026-07-31｜CEO｜commitment：結語稱有多種槓桿可擴大利潤率。（原話："multiple levers to expand margins"）
- 2026-07-31｜CEO｜customer：基礎設施占銷售比重：分拆時 12%、去年 45%、今年上半年近 60%。（原話："expanded to 45% last year and was nearly 60% in the first"）

### NVT_Analyst_Investor_Day_nVent_Electric_plc_20260318.md
- 2026-03-18｜Gary Corona (CFO)｜guidance：CFO 提出三年期（至2028）新目標：有機成長10%–13%（原話："now expect organic sales growth of 10% to 13%"）
- 2026-03-18｜Gary Corona (CFO)｜guidance：三年目標：併購每年貢獻超過3個百分點營收，原為約1點（原話："acquisitions to be more than 3 points of sales annually, up"）
- 2026-03-18｜Gary Corona (CFO)｜guidance：三年目標：調整後EPS成長17%–20%（原話："We now expect adjusted EPS growth of 17% to 20%"）
- 2026-03-18｜Gary Corona (CFO)｜guidance：三年目標：自由現金流轉換率約95%（原話："expect to convert approximately 95% of our earnings into"）
- 2026-03-18｜Gary Corona (CFO)｜guidance：2026年資本支出計畫約1.3億美元（原話："Looking ahead to 2026, we plan to invest approximately $130"）
- 2026-03-18｜Sara Zawoyski｜guidance：Systems Protection 2025年銷售報酬率逾20%，管理層預期2026年再有好表現（原話："Return on sales was over 20%, and we expect another great"）
- 2026-03-18｜Gary Corona (CFO)｜guidance：ROIC目標：2028年前超過15%（原話："investments with ROIC exceeding 15%, an additional 2-point"）
- 2026-03-18｜Aravind Padmanabhan｜guidance：新產品活力長期目標30%，每年貢獻逾3點銷售成長（原話："expect new products to deliver 30% vitality"）
- 2026-03-18｜Gary Corona (CFO)｜margin：營業利潤率目標：三年約擴張2點至約22%（原話："From a margin perspective, we're targeting approximately 2"）
- 2026-03-18｜Gary Corona (CFO)｜margin：口徑：22%利潤率預測與EPS目標都不含併購（原話："the margin forecast does not include M&A nor did the EPS, as"）
- 2026-03-18｜Gary Corona (CFO)｜margin：利潤率擴張來源：定價、高毛利新產品、成長帶來的規模槓桿（原話："driven by disciplined pricing, margin-accretive new products"）
- 2026-03-18｜Gary Corona (CFO)｜margin：增量利潤率口徑：約中段20%（mid-20s）（原話："That's approximately mid-20s from an"）
- 2026-03-18｜Gary Corona (CFO)｜margin：兩個事業部都預期擴張利潤率（原話："Both segments have nice margin improvement plans, and we"）
- 2026-03-18｜Gary Corona (CFO)｜margin：Trachte與EPG利潤率預期向事業部平均靠攏（原話："we're applying our integration playbook, and we expect their"）
- 2026-03-18｜Gary Corona (CFO)｜margin：管理層承認部分逆風會持續（原話："Looking ahead, while some of these headwinds will persist"）
- 2026-03-18｜Brian Coleman｜margin：Electrical Connections 2025年利潤率逾28%、銷售13億美元（原話："Electrical Connections had record sales of $1.3 billion and"）
- 2026-03-18｜Gary Corona (CFO)｜margin：口徑：2025年自由現金流金額與年增（原話："$561 million of free cash flow, up 31% year-over-year"）
- 2026-03-18｜Gary Corona (CFO)｜margin：口徑：2023–2025併購貢獻4點（扣除熱管理出售後）（原話："Organic sales growth of 8% exceeded our targets."）
- 2026-03-18｜Gary Corona (CFO)｜margin：2023年舊框架的有機成長目標為中個位數（原話："calling for mid-single-digit organic growth, 1 point"）
- 2026-03-18｜Gary Corona (CFO)｜commitment：CFO稱自2023年投資人日以來達成或超過每個中期目標（原話："have met or exceeded every midterm target we set"）
- 2026-03-18｜Gary Corona (CFO)｜commitment：管理層對持續擴張利潤率表示有信心（原話："healthy, and we're confident in our ability to continue to"）
- 2026-03-18｜Gary Corona (CFO)｜commitment：併購須三年內報酬率超過資本成本（原話："requirement that acquisitions align with our strategy and"）
- 2026-03-18｜Gary Corona (CFO)｜commitment：CFO表示約六週後會就通膨與關稅提供更多說明（原話："We'll be together in about six weeks,"）
- 2026-03-18｜Beth Wozniak (CEO)｜commitment：管理層表示一向希望成長快於市場（原話："we always want to grow ahead of those targets"）
- 2026-03-18｜Gary Corona (CFO)｜capital_allocation：2023–2025年共部署53億美元資本（原話："From 2023 to 2025, we deployed $5.3 billion of"）
- 2026-03-18｜Gary Corona (CFO)｜capital_allocation：淨槓桿1.6倍，低於2–2.5倍目標區間（原話："we ended 2025 with net leverage of 1.6x, well below our"）
- 2026-03-18｜Gary Corona (CFO)｜capital_allocation：股利自2023年投資人日起增加約20%，並以回購抵銷稀釋（原話："We're committed to a competitive dividend, which has"）
- 2026-03-18｜Gary Corona (CFO)｜capital_allocation：2025年ROIC約13%（原話："ROIC of approximately 13%, up from 2022"）
- 2026-03-18｜Gary Corona (CFO)｜capital_allocation：近期併購成果：部分標的進場時利潤率低於預期（原話："Some of these businesses came into nVent with margins below"）
- 2026-03-18｜Gary Corona (CFO)｜capital_allocation：CFO稱近期併購皆達到報酬目標（原話："and all of the recent deals have met those expectations."）
- 2026-03-18｜Beth Wozniak (CEO)｜capital_allocation：CEO談併購：未來可為較大型的補強併購（原話："can be larger bolt-on deals"）
- 2026-03-18｜Sara Zawoyski｜product：液冷滲透率預估：現約10–15%，2028年逾30%（原話："utilize liquid cooling, which we expect to be over 30% by"）
- 2026-03-18｜Beth Wozniak (CEO)｜product：管理層引用的液冷市場成長率（原話："is expected to grow more than 35%"）
- 2026-03-18｜Sara Zawoyski｜product：液冷產能自2023年中增加逾八倍（原話："liquid cooling production capacity more than eightfold"）
- 2026-03-18｜Beth Wozniak (CEO)｜product：Blaine新廠預計年底前使液冷產能約增一倍（原話："approximately double our liquid cooling capacity by year-end"）
- 2026-03-18｜Aravind Padmanabhan｜product：新CDU宣稱單台可支援多個機櫃（原話："whereas competitors need multiple CDUs to achieve the same"）
- 2026-03-18｜Beth Wozniak (CEO)｜product：首次揭露每百萬瓦約100萬美元的資料中心內容量機會（原話："approximately $1 million per megawatt."）
- 2026-03-18｜Beth Wozniak (CEO)｜product：CEO說明該數字為首次公開（原話："but this is the first time that we've shared that"）
- 2026-03-18｜Sara Zawoyski｜product：資料中心銷售（Systems Protection）逾8億美元、三年成長約40%（原話："million and have grown roughly 40% over the last three years"）
- 2026-03-18｜Beth Wozniak (CEO)｜product：口徑：公司層級白空間約75%、灰空間25%（原話："75% of sales. And the gray space makes up 25%."）
- 2026-03-18｜Sara Zawoyski｜product：口徑：Systems Protection 白空間占比（原話："Systems Protection sales in the white space."）
- 2026-03-18｜Brian Coleman｜product：線槽（WBT）產品線成長率與液冷相當（原話："at rates comparable to liquid cooling"）
- 2026-03-18｜Sara Zawoyski｜product：服務收入預期隨時間累積（原話："service revenue to kind of build over time"）
- 2026-03-18｜Beth Wozniak (CEO)｜product：800V DC：電力連接產品已達800V DC額定（原話："power connections that are already rated to 800-volt DC"）
- 2026-03-18｜Beth Wozniak (CEO)｜product：800V DC：仍需AC系統（原話："there's still going to be a need for AC systems"）
- 2026-03-18｜Beth Wozniak (CEO)｜competition：對液冷標準的看法：避免任何人都可自稱有CDU（原話："that they have a CDU, but you may not know for what"）
- 2026-03-18｜Beth Wozniak (CEO)｜competition：回應Vertiv、Eaton、Schneider：不須有HVAC才能做液冷（原話："no one has ever said, oh, you're not in HVAC"）
- 2026-03-18｜Beth Wozniak (CEO)｜competition：回應Envicool問題：業界在尋找更多供應商（原話："companies are just looking for more and more suppliers"）
- 2026-03-18｜Beth Wozniak (CEO)｜competition：對冷板/浸沒技術保持中立（原話："we are agnostic to whether it is a cold plate or immersion"）
- 2026-03-18｜Beth Wozniak (CEO)｜competition：定位在白空間技術冷卻系統而非設施冷卻（原話："we talk about the technology cooling system that is in the"）
- 2026-03-18｜Aravind Padmanabhan｜customer：與NVIDIA夥伴網路關係（原話："companies who are part of NVIDIA's partner network."）
- 2026-03-18｜Beth Wozniak (CEO)｜customer：資料中心需求能見度來自超大規模客戶（原話："we're getting good visibility because we're working with"）
- 2026-03-18｜Beth Wozniak (CEO)｜customer：積壓訂單23億美元，約為一年前3倍（原話："a backlog of $2.3 billion, 3x"）
- 2026-03-18｜Gary Corona (CFO)｜risk：關稅：232金屬為主要關稅影響（原話："232 metals are the primary tariff impact for us"）
- 2026-03-18｜Gary Corona (CFO)｜risk：通膨：年初預估全部含關稅約中個位數（原話："the year, we estimated about mid-single digits all in"）
- 2026-03-18｜Gary Corona (CFO)｜risk：價格轉嫁靠經銷商漲價（原話："delivering the price increases that we need to cover"）
- 2026-03-18｜Sara Zawoyski｜risk：液冷換機週期長度尚未定義（原話："I think it's too early just in terms of where we're at"）

### 問答異常語氣（迴避／改口／保留）
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Jeff Sprague：Systems Protection 財測似乎 Q3、Q4 營收較 Q2 持平或略降，是否有供應鏈問題？｜答法：CFO 轉談 2 年疊加成長加速；CEO 回答為「規劃審慎」，未直接說明 Q3 是否有供應鏈限制，也未回應序列走勢。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Joe Ritchie／Nicole DeBlase：積壓訂單年底是否會成長、$25 億是否合適水位？｜答法：CEO 回「hard to say」「probably around the right level」，並自問自答式確認，未給方向。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Nicole DeBlase：Q3 訂單強勁開局是否代表訂單成長較 Q2 加速？｜答法：CEO 未答加速與否，只說有短週期強勢與一些大型不均訂單。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Scott Graham：Q3 有機財測是否有上檔空間、是否由液冷積壓出貨驅動？｜答法：CFO 未回答上檔空間或液冷出貨占比，改談 2 年疊加 50% 與財測審慎。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Scott Graham：下半年增量利潤率 20% 中段，過去提過的 30% 是否仍是延伸目標？｜答法：CFO 未回應 30%，重申 Investor Day 中期目標為 20% 中段，並改談 EPS 為 2024 年兩倍以上。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Jeff Hammond：$20 億資料中心營收中液冷與其他的占比？｜答法：CEO 稱尚未拆分，僅稱液冷為顯著貢獻；CFO 改談整體組合廣泛。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Jeff Hammond／Joe Ritchie：EC 利潤率後續軌跡是否更高？｜答法：CFO 兩次皆只答預期持續進步、落在 20% 後段，未給具體數字或時點。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Brian Drab：近 12 個月訂單成長率是否明顯高於本季低雙位數？｜答法：CFO 僅答「是」，未提供數字。
- NVT_Analyst_Investor_Day_nVent_Electric_plc_20260318.md｜問：Q1財測/訂單趨勢：新聞稿稱第一季優於預期，是什麼意思？｜答法：CEO表示不想評論該季，只說進展順利，未給數字或訂單更新
- NVT_Analyst_Investor_Day_nVent_Electric_plc_20260318.md｜問：資料中心營收中電力管理與冷卻的比重｜答法：CEO稱未拆分、也未更新，只說液冷最大
- NVT_Analyst_Investor_Day_nVent_Electric_plc_20260318.md｜問：10%–13%有機成長如何拆到資料中心與公用事業｜答法：CEO指向簡報圖表，只說資料中心最高、公用事業次之，未給拆分數字
- NVT_Analyst_Investor_Day_nVent_Electric_plc_20260318.md｜問：Engineered Building Solutions 的產業成長率與資料中心/公用事業占比｜答法：未給產業成長率；稱成長率與公用事業相近，占比只說多數為公用事業
- NVT_Analyst_Investor_Day_nVent_Electric_plc_20260318.md｜問：Google與Envicool洽談，中國競爭者在美國是否更具威脅｜答法：未直接回答威脅程度，改談需求龐大與廠商尋找更多供應商

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
{"date":"20260524","verdict":"B 衛星候選：thesis 完整（A 級執行 9/10、AI 數據中心液冷超級週期、Trachte/EPG systems integrator 轉型）但估值 🟡 + MA stretched + 短期 R:R 負值 + 4 週 +25.5% 漂移 = 時機不到。等回測 BB 中軌 $127 區 或 Fwd PE 28x $140 區 + Q2/Q3 26 backlog 維持 +100%+ YoY 後分批進場 3-5% 衛星倉。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"液冷超級週期持續 5+ 年，NVT systems integrator 角色拿到 SAM 15-20%","columns":{"2Y 驗證點":"FY26 sales ≥ guide $4.9-5.0B + Q3/Q4 26 backlog YoY 維持 &gt; +100%","5Y 驗證點":"FY28 sales ≥ $6.5B（含液冷 + 模組化 DC）+ data center 占比 ≥ 40%","10Y 驗證點":"FY30 sales ≥ $8.5B + 全球液冷 SAM 滲透 15-20%","具體數字門檻":"FY26 公司 guide / FY27 +20% 共識 / FY30 公司 long-term target","信息來源":"公司 guidance + sell-side consensus + Yole / GMI 液冷市場報告","漂移觸發條件":"連 2 季 TTM revenue &lt; consensus −5% → H1 削弱"}},{"id":"H2","text":"Trachte + EPG 收購整合 18-24 個月後 synergy 兌現至 EPS +$0.50-0.80","columns":{"2Y 驗證點":"Q2-Q4 26 quarterly synergy 揭露 + EPG cross-sell 案例","5Y 驗證點":"2027-28 systems integrator 角色帶 customer lock-in 顯化在 GM / OPM 提升","10Y 驗證點":"合併 entity FY30 OPM ≥ 22%（vs FY25 ~17.5%）","具體數字門檻":"EPG 收購時管理層宣示 $80M synergy / 24 個月；FY30 OPM 22% 為管理層 long-term target","信息來源":"5/1 Q1 26 法說 + 後續法說會跟進","漂移觸發條件":"連 2 季 OPM 增速 &lt; +0.5pp QoQ → H2 削弱"}},{"id":"H3","text":"估值倍數 Fwd PE 33-35x 維持在 28-30x 區間（不再大幅向上）","columns":{"2Y 驗證點":"2026H2 股價回測 $135-150 區，Fwd PE 28-30x","5Y 驗證點":"2027-28 隨 EPS 成長自然 PE 下降至 24-26x","10Y 驗證點":"2030 估值 reset 至 GARP 標準 PE 20-22x","具體數字門檻":"PE 28-30x 是 NVT 結構性高成長期合理上限；&gt; 35x 不可持續","信息來源":"5Y 歷史 Fwd PE band + 同業 VRT / ETN / SU 估值對比","漂移觸發條件":"連 2 季 Fwd PE &gt; 38x → 估值倍數脫鉤"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI hyperscaler capex 2027 提前放緩","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"NVT backlog YoY + hyperscaler capex guidance（MSFT / META / GOOG / AMZN）","警戒閾值":"連 2 季 backlog YoY &lt; +50% + 2 家 hyperscaler 下修 capex → R1 觸發"}},{"id":"R2","text":"Trachte + EPG synergy 不如預期 / 整合失敗 / goodwill impairment","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"EPG 揭露的 cross-sell 案例 + OPM 改善速度 + goodwill 帳面值","警戒閾值":"FY27 OPM 仍卡在 17-18% 未進到 19-20% → H2 削弱"}},{"id":"R3","text":"Vertiv / Schneider 等同業在液冷市場拿走更多 share","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"液冷市場 share 報告（Yole / GMI 年度更新）+ 大型 hyperscaler 訂單揭露","警戒閾值":"2028 全球液冷 NVT share &lt; 8% → R3 觸發 + 估值倍數 reset"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟡","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":164.66,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVT_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
