你是 stock-analyst **v20 判斷 agent**，標的 BSX（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"BSX","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BSX_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BSX_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":5138,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿 8-K earningsrelease_live.htm"},"note":"未取得營收共識；adjusted EPS 低於共識（媒體報導，未逐字核對）"},{"id":"f_kpi1_gaap_operating_income_ma","label":"GAAP operating income / margin","value":828,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m（利益率 16.1%，為自算 828/5138）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿 8-K earningsrelease_live.htm"},"note":"n/a"},{"id":"f_kpi2_non_gaap_adjusted_operat","label":"Non-GAAP (adjusted) operating income / margin","value":1364,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m（利益率 26.5%，為自算 1364/5138）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司新聞稿 8-K earningsrelease_live.htm"},"note":"n/a"},{"id":"f_kpi3_adjusted_eps","label":"Adjusted EPS","value":0.73,"period":"Q3 2026（公告於 2026-10-28）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（公告於 2026-10-28）","citation":"公司新聞稿 8-K earningsrelease_live.htm"},"note":"低於共識（Grafa 報導，數字未取得）"},{"id":"f_kpi4_guidance_q4_2026","label":"Guidance: Q4 2026","value":"net sales -3.0% 至 -1.0%（reported 與 organic）；adjusted EPS 0.77–0.79","period":"Q3 2026 新聞稿（公告於 2026-10-28）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026 新聞稿（公告於 2026-10-28）","citation":"公司新聞稿 8-K earningsrelease_live.htm"},"note":"n/a"},{"id":"f_kpi5_guidance_fy2026","label":"Guidance: FY2026","value":"net sales 約 +4.25% reported／約 +3.75% organic；adjusted EPS 3.16–3.18","period":"Q3 2026 新聞稿（公告於 2026-10-28）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026 新聞稿（公告於 2026-10-28）","citation":"公司新聞稿 8-K earningsrelease_live.htm"},"note":"FY1 EPS 共識 3.18（consensus_revision 2026-10-31 快照）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_bsx_gross_margin_pct","label":"BSX 毛利率","value":69.92,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BSX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bsx_operating_margin_pct","label":"BSX 營業利益率","value":21.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BSX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bsx_fcf_margin_pct","label":"BSX FCF 利潤率","value":4.14,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BSX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mdt_gross_margin_pct","label":"MDT 毛利率","value":65.01,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mdt_operating_margin_pct","label":"MDT 營業利益率","value":19.04,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mdt_fcf_margin_pct","label":"MDT FCF 利潤率","value":16.33,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_syk_gross_margin_pct","label":"SYK 毛利率","value":64.98,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SYK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_syk_operating_margin_pct","label":"SYK 營業利益率","value":21.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SYK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_syk_fcf_margin_pct","label":"SYK FCF 利潤率","value":18.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SYK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abt_gross_margin_pct","label":"ABT 毛利率","value":56.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abt_operating_margin_pct","label":"ABT 營業利益率","value":15.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abt_fcf_margin_pct","label":"ABT FCF 利潤率","value":15.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ew_gross_margin_pct","label":"EW 毛利率","value":77.84,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ew_operating_margin_pct","label":"EW 營業利益率","value":28.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ew_fcf_margin_pct","label":"EW FCF 利潤率","value":22.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":44.15,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-22.45,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":49.91,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.31,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.19 → 3.18）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-1.54,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.24 → 3.19）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-3.67,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.54 → 3.41）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.18,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.19,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.41,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-4.22,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 3.32 → 3.18（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":18.6,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.03,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.61,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":13.86,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 3.18，分子＝快照價 44.08","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":12085.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 12624.0、現金 539.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1449.23,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":75974.29,"period":"2026-11-03","unit":"USD m","basis":"市值 63889.29 ＋ 淨負債 12085.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":20966.85,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（28 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":21026.61,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（29 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.62,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 43.99 / W52 63.44 / W104 81.58 / W250 66.19 / W250 13週斜率 0.02%"},{"id":"f_ma_w52","label":"52 週均線","value":63.44,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":81.58,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":66.19,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.02,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K FY2025 揭露：面臨全球與本地競爭者，包含低成本製造商進入造成價格壓力，中國有本土廠商優勢。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm","excerpt":"We also encounter competition from the entry of low-cost manufacturers, which may lead to increased pricing pressure. In certain countries, and particularly in China, we face competition from domestic medical device companies that may benefit from their status as local suppliers.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：新競爭者可能出現（新銷售模式、機器人、導航、自動化技術），次世代產品延遲可能導致市占下滑。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm","excerpt":"New competitors may emerge in the future, potentially including companies introducing new sales or distribution models to our industry or leveraging genomic, robotic, navigation, and/or other automation technologies.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"BTIG 醫師調查：預期 BSX PFA 份額由 2025 年 58% 降至 2026 年 48%，Medtronic、J&J 上升","source":"MedTech Dive BTIG PFA market share survey","url":"https://www.medtechdive.com/news/PFA-market-share-BTIG-doctor-survey/738367/","excerpt":"weighted average basis, projected market share in 2025 would be divided between Boston Scientific (58%), Medtronic (28%), J&J (11%), and Abbott (3%). In 2026, the survey predicted Boston Scientific would lose share and J&J would gain it, with an expected PFA share split of Boston Scientific (48%), Medtronic (29%), J&J (20%) and Abbott (3%).","as_of":"2025-01-27","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Abbott Amulet 360 LAA 封堵器取得 CE mark，與 Watchman 競爭","source":"MedTech Dive Abbott wins CE mark for new LAA closure device","url":"https://www.medtechdive.com/news/abbott-wins-ce-mark-for-new-laa-closure-device/829072/","excerpt":"Europe’s CE mark for the next-generation version of its Amulet device. The implant seals the heart’s left atrial appendage, or LAA, to help reduce the risk of stroke in people with atrial fibrillation. The device has been designed to improve how the implant conforms to and seals the LAA, the company said Thursday. Abbott plans to expand use of the new device, called Amulet 360, across","as_of":"2026-08-28","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K：客戶包含經銷商、醫院、醫療機構等多元對象，付款條件美國通常30天、國際可能更長，一般不要求擔保品；金融工具交易對手為投資級大型金融機構。","source":"SEC EDGAR 10-K FY2025 Item 8 Concentrations of Credit Risk","url":"https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm","excerpt":"In the normal course, our payment terms with customers, including distributors, hospitals, health care agencies, clinics, doctors' offices and other private and governmental institutions, are typically 30 days in the U.S. but may be longer in international markets and generally do not require collateral.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2024 10-K：2024/2023/2022 無單一客戶占淨銷售逾10%；GPO、醫院網絡、國際經銷商為重要買方群。","source":"SEC EDGAR 10-K FY2024","url":"https://www.sec.gov/Archives/edgar/data/885725/000088572525000011/bsx-20241231.htm","excerpt":null,"as_of":"2025-02-18","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"BSX cut 2026 guidance; CEO called 2027 the 'trough in the cycle', expects return to growth in 2028; Watchman not assumed to improve in 2027; further China price headwinds in 2027","source":"MDDI - Boston Scientific Cuts 2026 Guidance as Watchman and Electrophysiology Headwinds Intensify","url":"https://www.mddionline.com/business/boston-scientific-cuts-2026-guidance-as-watchman-and-electrophysiology-headwinds-intensify","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Wells Fargo conference: U.S. Watchman market expected mid-to-high single-digit declines in 2H and similar trends in 2027","source":"Quartr - BSX Wells Fargo 21st Annual Healthcare Conference summary","url":"https://quartr.com/events/boston-scientific-corporation-bsx-wells-fargo-21st-annual-healthcare-conference_3YK5rfio","excerpt":"WATCHMAN and LAAC market outlook U.S. WATCHMAN market expected to see mid to high single-digit declines in the second half and similar trends in 2027, with growth below market due to new competition.","as_of":"2026-09-10","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"BSX 與 Penumbra 於 2026-01-14 簽訂收購協議；雙方於 3-16 收到 FTC Second Request，雙方在栓塞器材直接競爭，外界推測此重疊為 FTC 關注主因。","source":"Goodwin, Life Sciences Antitrust Quarterly Update Q3 2026","url":"https://www.goodwinlaw.com/en/insights/publications/2026/10/insights-lifesciences-antc-antitrust-life-sciences-q3-update-2026","excerpt":"each received an FTC Second Request on March 16.","as_of":"2026-10-16","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因素揭露 BSX 曾收到 DOJ、SEC、HHS OIG 等傳票，涉及醫療人員財務安排、法規遵循與銷售促銷作法；不可預測結果。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm","excerpt":"We have received, and in the future may receive, subpoenas and other requests for information from Congress and state and federal governmental agencies, including, among others, the U.S. Department of Justice (DOJ), the U.S. Securities and Exchange Commission (SEC), the Office of Inspector General of the Department of Health and Human Services (HHS) and the Department of Defense","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"EU MDR 過渡期延長至 2027（高風險類）與 2028（較低風險類），需持續投資轉換產品。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm","excerpt":"In 2023, the European Commission extended the transitional period to 2027 for certain high risk class devices and 2028 for lower risk class medical devices. The MDR has required significant investment and will continue to require ongoing investment over the next couple of years to transition all products.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"BSX FY2025 10-K: 公司目前受制於仍在美國最高法院受審的美國關稅；已繳關稅可能退款但無保證，且關稅調整或以其他授權重新課徵、他國報復性關稅可能對財務造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm","excerpt":"We are subject to certain U.S. tariffs that are currently subject to legal challenge before the U.S. Supreme Court. The timing and outcome of this litigation are uncertain, and the Court’s decision could result in the modification, invalidation, or continuation of such tariffs.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"BSX 10-K MD&A: 公司預期在現行美國進口關稅下持續產生增額成本，並可能面臨中國對美製產品加徵關稅。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm","excerpt":"We continue to anticipate incurring incremental costs under the current schedule of tariffs on U.S. imports announced by the U.S. government, as well as any potential increases in tariffs introduced by China on U.S. manufactured products.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"BSX 10-K 風險因素：國際銷售占 36%，並提及進出口管制與許可、貿易保護措施，及在中國面對本土廠商競爭。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm","excerpt":"International net sales accounted for 36 percent of our global net sales in 2025.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"BSX 請求美國將哥斯大黎加排除於醫材關稅之外（Section 232 調查）","source":"MDDI: Costa Rica Seeks U.S. Tariff Exemption for Medical Devices","url":"https://www.mddionline.com/manufacturing/costa-rica-seeks-u-s-tariff-exemption-for-medical-devices","excerpt":null,"as_of":"2025-11-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險因子稱任一特定產品的製造集中在一或少數地點；主要廠區含美國/波多黎各、愛爾蘭、哥斯大黎加、馬來西亞、中國（聚合站彙整，需對 10-K 核實）；風險因子點名台海、俄烏、中東為潛在供應鏈干擾來源","source":"policyrisk.com BSX 彙整 / BSX 10-K（搜尋摘要）","url":"https://policyrisk.com/world/company/BSX","excerpt":"the manufacturing of any specific product is concentrated in one or a few locations","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"BSX 部分材料為單一來源採購；FDA 要求材料與零件使用前須驗證，更換供應商耗時；PFAS 主要製造商宣布停供相關材料","source":"BSX FY2022 ARS / 10-K 系列（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/885725/000119312523076690/d429871dars.pdf","excerpt":"Some materials are purchased from single sources due to quality considerations, expertise, costs or other reasons","as_of":"2023-03-01","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2026 年啟動 7–8 億美元全球重組計畫（至 2029），含生產線在全球廠區間轉移（Kalkine 報導，未對主要文件核實）","source":"Kalkine","url":"https://kalkine.com/news/announcements/boston-scientific-launches-700-million-to-800-million-global-restructuring-program-through-2029","excerpt":"transfer of production lines among Boston Scientific's facilities worldwide","as_of":"2026-01-01","retrieved_at":"20261103","affects":["triggers","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"BSX 2026Q3 淨銷售 $5.138B，reported/operational/organic 皆 +1.5%；MedSurg +0.6%（operational +0.7%），Cardiovascular +1.9%；美國 +0.5%、EMEA +4.4%、APAC -0.6%、LACA +16.0%。","source":"BSX Q3 2026 earnings release (SEC 8-K) / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0000885725/000088572526000066/earningsrelease_live.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","valuation","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"BSX 指引 2026Q4 銷售年減 1%～3%，調整後 EPS $0.77～0.79，全年調整後 EPS $3.16～3.18（Q2 時為 $3.28～3.32）。","source":"BSX Q3 2026 earnings release / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0000885725/000088572526000066/earningsrelease_live.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"分析摘要稱 Farapulse 在 PFA 市佔約 50% 且流失快於預期，J&J、Abbott、Medtronic 擴張；管理層稱仍是 PFA 領導者但份額下降；分析師認為 PFA 定價仍穩定。","source":"Wells Fargo 21st Annual Healthcare Conference summary (Quartr)","url":"https://quartr.com/events/boston-scientific-corporation-bsx-wells-fargo-21st-annual-healthcare-conference_3YK5rfio","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"美國 Watchman 市場急遽放緩，預期 2026 下半年呈中高個位數衰退；CHAMPION-AF 若獲一線標籤擴張尚未計入共識。","source":"搜尋摘要彙整（Quartr/MedTech Dive 等二手來源）","url":"https://www.medtechdive.com/news/boston-scientific-again-cuts-2026-guidance/826473/","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子載明：他公司的產品、製程或技術（含低成本替代品）可能使 BSX 產品過時或較缺競爭力；次世代產品上市延遲可能導致市占下滑。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm","excerpt":"Developments by other companies of products and/or services, processes or technologies, including low-cost alternatives, may make our products or proposed products obsolete or less competitive and may negatively impact our net sales.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"MD+DI 報導：BSX 電生理部門在 PFA 領域受 Medtronic、J&J、Abbott 競爭，營收低於預期約 3,300 萬美元。","source":"MD+DI: Boston Scientific's Electrophysiology Segment Earnings Confirm Investor Fears","url":"https://www.mddionline.com/cardiovascular/boston-scientific-s-electrophysiology-segment-earnings-confirm-investor-fears","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"MD+DI 報導：Medtronic Sphere-9 取得進展並在歐洲推出 Sphere-360，BSX PFA 主導地位流失快於預期。","source":"MD+DI: PFA Wars","url":"https://www.mddionline.com/cardiovascular/pfa-wars-the-battle-for-dominance-in-cardiac-ablation-s-fastest-growing-market","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"+","claim":"CHAMPION-AF 達全部主要與次要終點：Watchman FLX 對 NOAC 之出血較低（15.1% vs 21.8%），為 LAAC 取代長期抗凝血藥的臨床證據。","source":"Boston Scientific press release via Nasdaq/Barchart: CHAMPION-AF","url":"https://www.nasdaq.com/press-release/champion-af-study-watchman-flxtm-left-atrial-appendage-closure-device-first-line","excerpt":"CHAMPION-AF study of the WATCHMAN FLX™ Left Atrial Appendage Closure Device as a first-line therapy for stroke risk reduction meets all primary and secondary safety and efficacy endpoints Published Mar 28, 2026 10:55am EDT linkedin facebook x email reddit Data highlights the WATCHMAN FLX device provided statistically superior protection from bleeding, demonstrated similar","as_of":"2026-03-28","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 載明多數淨銷售來自直銷組織的國家，並以經銷商網路補充；預期在經濟或策略上不適合設直銷的市場使用第三方經銷商，未見通路結構性轉變的表述。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm","excerpt":"The majority of our net sales are derived from countries in which we have direct sales organizations. We also have a network of distributors and dealers who offer our products in certain countries and markets.","as_of":"2026-02-17","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026-07-21 董事會核准全球重組計畫，聚焦供應鏈最佳化，預估稅前費用 7–8 億美元（屬供應鏈而非銷售通路）。","source":"TipRanks: Boston Scientific launches 2026 global restructuring plan","url":"https://www.tipranks.com/news/company-announcements/boston-scientific-launches-2026-global-restructuring-plan","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 report (2026-07-29): FY2026 adjusted EPS guidance $3.28–$3.32 vs consensus $3.36; revenue guidance $21.2–$21.4B vs consensus $21.6B; Q3 guide EPS $0.80–$0.82 and revenue $5.2–$5.3B vs consensus $0.84 / $5.4B. Guidance below consensus.","source":"MarketBeat, Boston Scientific updates FY 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/boston-scientific-nysebsx-updates-fy-2026-earnings-guidance-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Company cut 2026 guidance twice: Q1 (Apr 22) organic growth to 6.5–8% from 10–11% and EPS to $3.34–3.41; Q2 (Jul 29) cut again, citing WATCHMAN and US EP. No raise found in 2026.","source":"MassDevice, Boston Scientific Q2 2026 cuts guidance","url":"https://www.massdevice.com/boston-scientific-q2-2026-cuts-guidance/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 2026 (reported 2026-10-28): net sales $5.138B, +1.5% organic; adjusted EPS $0.73, below July Q3 guide of 3–5% growth and $0.80–$0.82 EPS. Updated FY/Q4 guidance not retrieved.","source":"Finviz/PR Newswire, Boston Scientific announces results for third quarter 2026","url":"https://finviz.com/news/409766/boston-scientific-announces-results-for-third-quarter-2026","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.R","triggers","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Analyst target distribution varies by aggregator: Bullstory (2026-08-19) avg ~$62.69, 29 analysts, range $44–$94; MarketBeat (undated) avg $71.62, 31 analysts, high $118, low $50; Tickflow (Aug 1) avg $82.40. Targets cut after guidance (e.g. Needham to $57 from $77). Ratings still mostly Buy.","source":"Bullstory BSX analyst forecast; MarketBeat BSX forecast; Tickflow","url":"https://bullstory.io/en/stocks/bsx/forecast","excerpt":null,"as_of":"2026-08-19","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-01-14 BSX 與 Penumbra 簽訂併購協議（約 $374/股、EV 約 $145 億）；搜尋結果僅見公告期報導，未見完成交割的來源","source":"SEC EDGAR 8-K Item 1.01（2026-01-15）","url":"https://www.sec.gov/Archives/edgar/data/885725/000094787126000037/ss5822815_8k.htm","excerpt":"On January 14, 2026, Boston Scientific Corporation, a Delaware corporation (the “Company”), entered into an Agreement and Plan of Merger (the “Merger Agreement”) with Pinehurst Merger Sub, Inc., a Delaware corporation and wholly owned subsidiary of the Company (“Merger Sub”), and Penumbra, Inc.","as_of":"2026-01-15","retrieved_at":"20261103","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026-03-05 起有證券集體訴訟（D. Mass.），指控與美國電生理業務財測／成長陳述有關；2026-05-20 指定首席原告，2026-07-20 提出修正訴狀；另有衍生訴訟","source":"BSX 10-Q（期間 2026-06-30）","url":"https://www.sec.gov/Archives/edgar/data/0000885725/000088572526000053/bsx-20260630.htm","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-07-21 董事會核准全球重組計畫，預估稅前費用約 $7–8 億，年化節省約 $5 億，2029 年底前完成","source":"SEC EDGAR 8-K Item 2.05（2026-07-27）","url":"https://www.sec.gov/Archives/edgar/data/885725/000088572526000049/bsx-20260721.htm","excerpt":"The implementation of the 2026 Restructuring Plan is estimated to result in total pre-tax charges of approximately $700 million to $800 million, of which approximately $600 million to $700 million is expected to result in future cash outlays, and reduce gross annual pre-tax expenses by approximately $500 million as program benefits are realized.","as_of":"2026-07-27","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2026-09-07 8-K Item 1.05：網路攻擊造成網路中斷，影響製造及訂單處理／出貨；調查仍在進行","source":"SEC EDGAR 8-K（2026-09-07 事件）","url":"https://www.sec.gov/Archives/edgar/data/0000885725/000088572526000059/bsx-20260907.htm","excerpt":"As of the date of this Current Report on Form 8-K, the Company has not identified evidence of ongoing unauthorized access to its systems. The Company’s investigation of the incident remains ongoing.","as_of":"2026-09-08","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"-","claim":"FDA 對 BSX 心律調節器 Class I 召回更正（2026-05-07 報導）；AXIOS 支架、Infinion CX 脊髓刺激導線、EnRoute 頸動脈神經保護系統亦有召回／停用通知","source":"搜尋結果：MassDevice／MDDI／FDA 公告彙整","url":"https://www.mddionline.com/cardiovascular/boston-scientific-pulls-select-stents-electrocautery-enhanced-delivery-systems","excerpt":null,"as_of":"2026-05-27","retrieved_at":"20261103","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-01-14 BSX 與 Penumbra 簽訂併購協議；搜尋僅見公告期報導，未見完成交割來源","source":"SEC EDGAR 8-K Item 1.01（2026-01-15）","url":"https://www.sec.gov/Archives/edgar/data/885725/000094787126000037/ss5822815_8k.htm","excerpt":"On January 14, 2026, Boston Scientific Corporation, a Delaware corporation (the “Company”), entered into an Agreement and Plan of Merger (the “Merger Agreement”) with Pinehurst Merger Sub, Inc., a Delaware corporation and wholly owned subsidiary of the Company (“Merger Sub”), and Penumbra, Inc.","as_of":"2026-01-15","retrieved_at":"20261103","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026-03-05 起證券集體訴訟（D. Mass.，案號 1:26-cv-40075-JEK），涉及 2026-02-04 股價跌逾 17%；2026-07-20 提出修正訴狀；衍生訴訟已合併並暫停","source":"BSX 10-Q（期間 2026-06-30）","url":"https://www.sec.gov/Archives/edgar/data/0000885725/000088572526000053/bsx-20260630.htm","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"+","claim":"FARAPOINT PFA 導管取得 FDA 核准與 CE mark（Q4 2025 財報稿、BioWorld 2026-01 報導）；2026-03-30 Asurys 液體管理系統取得 FDA 510(k)","source":"BSX Q4 2025 財報新聞稿／BioWorld","url":"https://news.bostonscientific.com/2026-02-04-Boston-Scientific-announces-results-for-fourth-quarter-and-full-year-2025","excerpt":"Received U.S. Food and Drug Administration (FDA) approval and CE mark for the FARAPOINT™ Pulsed Field Ablation (PFA) Catheter","as_of":"2026-02-04","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"2026 年多起召回：AXIOS 支架及輸送系統（1,660 批、167 起嚴重傷害、3 死亡）、Infinion CX 脊髓刺激導線（1,081 起嚴重傷害）、EnRoute 神經保護系統（2026-07-09 通知）；心律調節器 Class I 更正（2026-05-07 報導）","source":"MDDI／MassDevice／FDA 公告彙整","url":"https://www.mddionline.com/cardiovascular/boston-scientific-pulls-select-stents-electrocautery-enhanced-delivery-systems","excerpt":null,"as_of":"2026-07-09","retrieved_at":"20261103","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"BSX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":69.92,"operating_margin_pct":21.08,"fcf_margin_pct":4.14,"rd_intensity_pct":10.29},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BSX","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"MDT","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":65.01,"operating_margin_pct":19.04,"fcf_margin_pct":16.33,"rd_intensity_pct":7.77},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MDT","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"SYK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.98,"operating_margin_pct":21.73,"fcf_margin_pct":18.2,"rd_intensity_pct":6.42},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SYK","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ABT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.63,"operating_margin_pct":15.9,"fcf_margin_pct":15.66,"rd_intensity_pct":6.64},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABT","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"EW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":77.84,"operating_margin_pct":28.09,"fcf_margin_pct":22.01,"rd_intensity_pct":16.75},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"BSX"},"financial_history":{"ticker":"BSX","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":12682000000.0,"revenue_yoy_pct":null,"gross_margin_pct":68.81,"operating_margin_pct":16.04,"net_income":698000000.0,"diluted_eps":0.45,"free_cash_flow":914000000.0,"fcf_margin_pct":7.21,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":14240000000.0,"revenue_yoy_pct":12.29,"gross_margin_pct":69.49,"operating_margin_pct":16.97,"net_income":1593000000.0,"diluted_eps":1.07,"free_cash_flow":1703000000.0,"fcf_margin_pct":11.96,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":16747000000.0,"revenue_yoy_pct":17.61,"gross_margin_pct":68.61,"operating_margin_pct":17.93,"net_income":1854000000.0,"diluted_eps":1.25,"free_cash_flow":2365000000.0,"fcf_margin_pct":14.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":20074000000.0,"revenue_yoy_pct":19.87,"gross_margin_pct":69.01,"operating_margin_pct":19.78,"net_income":2898000000.0,"diluted_eps":1.94,"free_cash_flow":3404000000.0,"fcf_margin_pct":16.96,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/BSX/BSX_Q3_2026_Earnings_Call_20261028.md）

# Q3 2026 Earnings Call
**Boston Scientific Corporation** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Good morning, and welcome to the Boston Scientific Third Quarter 2026 Earnings Call. [Operator Instructions] Please note this event is being recorded. 
I would now like to turn the conference over to Lauren Tengler, Vice President, Investor Relations. Please go ahead.

**Lauren Tengler** (Executives):
Thank you, Drew, and thanks to everyone for joining us. With me today are Mike Mahoney, Chairman and Chief Executive Officer; and Jon Monson, Executive Vice President and Chief Financial Officer. During the Q&A session, Mike and Jon will be joined by Joe Fitzgerald, Executive Vice President and Group President, Cardiology; and our Chief Medical Officer, Dr. Ken Stein.
We issued a press release earlier this morning announcing our Q3 2026 results, which included reconciliations of the non-GAAP measures used in this release. The release as well as reconciliations of the non-GAAP measures used in today's call can be found on the Investor Relations section of our website.
Please note that on the call, operational revenue excludes the impact of foreign currency fluctuations, and organic revenue further excludes certain acquisitions and divestitures for which there is less than a full period of comparable net sales. Guidance excludes our previously announced agreement to acquire Penumbra, which we expect to close in early 2027.
For more information, please refer to the Q3 financial and operating highlights deck, which may be found on the Investor Relations section of our website. On this call, all references to sales and revenue are organic and relative growth is compared to the same quarter of prior year, unless otherwise specified.
This call contains forward-looking statements regarding, among other things, our financial performance, business plans, market expectations and product performance and development. These statements are based on our current beliefs using information available to us as of today's date and not intended to be guarantees of future events or performance. If our underlying assumptions turn out to be incorrect or certain risks or uncertainties materialize, actual results could vary materially from those projected by the forward-looking statements. Factors that may cause such differences are discussed in the earnings release we issued earlier this morning and our periodic reports and other filings with the SEC, including the Risk Factors section of our most recent annual report on the Form 10-K. Boston Scientific disclaims any intention or obligation to update these forward-looking statements, except as required by law.
In addition, this call does not constitute an offer to sell or the solicitation of an offer to buy any securities or solicitation of any vote or approval in connection with the proposed transaction with Penumbra. Boston Scientific has filed with the SEC a registration statement on Form S-4 containing a proxy statement of Penumbra and a prospectus of Boston Scientific that contains important information about Penumbra, Boston Scientific, the proposed transaction and related matters.
At this point, I'll turn it over to Mike.

**Michael Mahoney** (Executives):
Thanks, Lauren. Thank you, everyone, for joining us today. I want to begin by walking through our third quarter results, provide some fourth quarter outlook and then assumptions behind our updated view of 2027. I'll then provide more details on both the region and business unit performance and outlook.
Q3 total company organic sales grew 1.5% versus a guide -- versus our original guide of 3% to 5%. Q3 adjusted EPS of $0.73 declined 3% versus our guidance range of $0.80 to $0.82. Our Q3 results were impacted by our previously reported cybersecurity incident, which we estimate reduced our sales growth by approximately 300 basis points and adjusted EPS by $0.07 in the quarter. Importantly, after a 2-week outage as a result of the cyber incident, all operations are back up and running as of September 8. I'm very proud of our team's resiliency and the efforts they made to help us return as quickly as possible to supporting physicians and their patients with our products.
Turning to Q4, we anticipate that there will be a 200 to 300 basis points of impact from the cyber incident as we work through elevated customer orders at the end of Q3 to replenish inventory levels. Additionally, since our second quarter earnings call, EP share pressure has intensified, further accelerated by the cyber incident. We have also seen pricing dynamics in China become more challenging.
To that end, we are guiding to organic revenue declines of minus 1% to minus 3% for fourth quarter '26 and adjusted EPS of $0.77 to $0.79. This results in a full year '26 organic revenue growth guide of approximately 4% and EPS of $3.16 to $3.18.
Boston Scientific has enjoyed several years of exceptional growth, driven by strategic investments and strong execution globally, particularly within our EP and WATCHMAN franchises. In '26, we've seen that cycle turn, and those 2 businesses are now weighing on our total company growth as we navigate competition and market dynamics. We believe that 2027 will be the trough in this cycle, and we have several investments and new innovations coming over the course of the next 3 years that we expect will support stabilization and growth for both the EP and WATCHMAN businesses.
And while the remaining 75% of our business has grown consistently, we anticipate there will be additional price headwinds in China in '27 and the growth likely won't be enough to offset the pressure from EP and WATCHMAN next year. As a result, we believe we'll be challenged to grow sales and adjusted EPS in '27, excluding our pending acquisition of Penumbra.
Having said all that, we are taking immediate actions to prepare for the future, including through our previously announced restructuring program and the evolution of our operating structure while ensuring that we continue to make the right strategic investments across a number of growth platforms. We have a very strong cadence of launches in '27 and '28, and anticipate entering several new markets over the next few years that will unlock $25 billion in new market opportunity by 2030. Importantly, we expect these actions to drive meaningful improvement in both our revenue and adjusted EPS performance as we aim to exit the cycle in '27 and return to delivering high performance in '28 with further improvement expected in '29.
I'll now provide some more details on Q3 and full year '26. Turning to our regional performance. The U.S. was flat year-over-year on an operational basis, driven by ICVT, IO&E and Neuromodulation. Europe, Middle East and Africa grew 6% on an operational basis with strong performance across many of our businesses. But within the quarter, there was some impact from cyber, offset by a transient headwind in third quarter '25 from our ERP platform go-live. 
Asia Pacific declined 1% operationally with growth impacted by the cyber incident as well as price pressure in China. Pricing dynamics in China continue to evolve with a number of our businesses seeing VBP and other pricing impacts as a result. We expect growth in this market will moderate to single-digit growth.
Turning to our business units. I'll start with Neuromodulation. Sales grew 13%. In Pain, growth was broad-based across the portfolio with exceptional performance with our Nalu PNS technology. But within the quarter, data was presented from the IMPROVE study evaluating our Intracept technology with real-world outcomes showing improvements in pain function and quality of life at 3 months. In Brain, growth was driven by our Cartesia X lead and Illumina 3D software, which enable more precise placement and programming.
Urology declined 3% this quarter with impact from the cyber incident as well as expanding pricing pressure in China. In stone management, we have received a number of approvals for key products, including FDA clearance of our Navigator Flex suction sheath, CE Mark and FDA clearance for distribution of the 7.5 Slim scope and FDA clearance of our LithoVue Elite single-use ureteroscope. As we look forward, we expect these new stone launches as well as stabilization and productivity from our S&M commercial organization to help our Urology improve its growth profile over the course of 2027.
Endoscopy sales declined 1% versus Q3 '25, inclusive of an impact from China VBP and cyber. Importantly, the underlying performance of this business continues to be strong, led by AXIOS, our differentiated technology, and as we look ahead, we expect our Endoscopy performance to be slightly pressured closer to mid-single-digit market growth until we annualize the impact from the China VBP in fourth quarter '27.
Cardiovascular sales delivered growth of 2% and Interventional Cardiology & Vascular Therapies sales grew 12%. Our Interventional Cardiology business had another exceptional quarter, growing 19% with continued strength in our global imaging franchise and drug-eluting technologies. We had another outstanding quarter of our AGENT DCB, which is backed by strong clinical evidence and now has been used to treat over 400,000 patients to date. We remain focused on both the near- and longer-term growth opportunities for this business.
And last quarter, we received IDE approval of the VITAL-PCI trial that is studying our VITALYST circulatory support technology in the high-risk PCI population. However, considering the evolving clinical evidence in this space, we've made the decision to shift our strategy and focus our development and clinical efforts on the AMI cardiogenic shock indication. We believe that our device design has the potential to be well suited to treat patients experiencing cardiogenic shock and look forward to initiating clinical efforts in '27.
Our VITALYST program is one of the largest internal R&D programs and an important long-term growth driver. To solidify funding for the AMI shock program, we have entered an agreement with Blackstone Life Sciences and aim to bring this important technology to market in 2030.
Our Vascular Therapies business grew 1% with some impact from cyber as well as TCAR supply constraints. Importantly, we anticipate that our TCAR supply to improve throughout fourth quarter with full resolution by early next year.
Our SEISMIQ launch continues to go well. And within the quarter, we received FDA clearance for SEISMIQ IVL -- sorry, SEISMIQ IVL to treat patients with severely calcified peripheral artery disease in small vessel, expanding our size matrix to now treat above the knee and below the knee. We also received FDA approval for the Ranger 035 drug-coated balloon, offering an expanded size and providing a highly complementary offering as most IVL procedures that are performed in lower limbs are also followed by drug-eluting technologies.
We remain excited about the opportunity to add Penumbra team to the -- we are excited about the opportunity to add the Penumbra team and their highly differentiated and complementary portfolio to Boston Scientific. We continue to work with the regulators and now expect to close in early '27, subject to the receipt of the remaining regulatory clearances.
Our Interventional Oncology & Embolization business grew 5% driven by strong performance in our cancer therapies franchise, partially offset by some supply constraints that we anticipate will be resolved in early 2027. We continue to see strong adoption of any-day dosing on TheraSphere 360 as well as momentum with our Hepatic Artery Infusion technology, providing a portfolio of options for cancer treatment.
Cardiac Rhythm Management sales declined minus 2% with some impact from the cyber incident as we navigated usage and activation of technologies that leverage remote monitoring while our systems were down. In Q3, our Diagnostics franchise grew high single digits. Our low-voltage business declined mid-single digits and high-voltage business declined low single digits. We anticipate that our performance will improve over the course of '27 with new launches and ongoing momentum.
Before I turn to WATCHMAN and EP, I want to acknowledge the pressures in these 2 businesses and the impact that it has on our overall growth. We are acting now to strengthen the LAAC market and focus our EP resources where we can compete most effectively while investing in innovation that we believe can improve over time.
On WATCHMAN, sales declined minus 6%, declining 7% in the U.S. and growing 4% internationally. Within the U.S., concomitant procedures grew approximately 35% and stand-alone procedures declined high teens versus third quarter '25. We continue to believe that the overall LAAC market slowdown primarily reflects changes in patient identification and referral patterns as physicians assess the clinical evidence published over the last year.
Importantly, we are executing against our investment priorities that we laid out in our 2Q call. We held over 200 med ed events in second quarter and third quarter, providing an opportunity for more than 2,000 referrers and implanters to gain a deeper understanding of the clinical evidence available. We've added more dedicated commercial resources to WATCHMAN to support both concomitant and stand-alone procedures and support the referral pathway. 
In the third quarter, we saw increased patient engagement, further reinforcing the strong demand for alternatives to oral anticoagulation and highlighting the significant unmet need among patients who can't, shouldn't or won't take lifelong OAC. We continue to believe that focusing on these priorities will support improvement in the LAAC market over time.
With our third quarter performance largely in line with expectations despite the cyber incident, we are maintaining our previous outlook for our WATCHMAN business. In fourth quarter, within the U.S., we anticipate no improvement in the year-over-year stand-alone procedure performance and continued deceleration in concomitant procedure growth against a very high baseline. Internationally, we anticipate similar performance in Q3 and Q4, resulting in sequential flat, low single-digit declines versus Q3 '26 globally. 
Turning to '27, we believe our investments along with the potential label change will improve the market over time. However, until we see the market improve, we are assuming that the market performance will be similar to Q4 with additional pressure due to a new competitive launch.
We believe in the benefit of this therapy and continue to innovate and invest for the future. And within the quarter, we commenced enrollment in the Elite AF clinical trial to evaluate the safety and effectiveness of the next-generation WATCHMAN Elite platform. We anticipate bringing this fourth-generation technology to market in '29. And additionally, we look forward to the late-breaking data presentation of our SIMPLAAFY trial at TCT, studying post-implant drug therapy using WATCHMAN FLX Pro and assessing whether a less intensive drug regimen may help mitigate post-implant bleeding risk.
Turning to EP, sales declined 5% with a decline of 8% in the U.S. and 2% growth internationally. We estimate that the cyber incident contributed to roughly half our miss primarily within our international region. But within the quarter, we continue to expand our OPAL footprint and drive more utilization of our mapping systems with our FARAWAVE and FARAPOINT catheters.
The EP market has transformed over the past few years, led by our differentiated FARAPULSE platform. We have seen our strong market share position erode as new technologies are introduced and adoption of these different PFA form factors has been highly dynamic. While the cyber incident has accelerated some of the share shift, we do expect continued erosion of our PFA share position until we launch FARAWAVE Ultra, now expected in early '28. We expect our EP performance to meaningfully improve in '28 as we expand our PFA ecosystem with 2D ICE in the second half of '27 and FARAWAVE Ultra in '28 and FARAFLEX, our wide-area focal catheter in '29.
In the near term, we're focusing our teams where we know we can win. We have the most utilized and studied technology for de novo atrial fibrillation procedures with our FARAWAVE catheters. We have a differentiated portfolio available, including our VersaCross transseptal needle and WATCHMAN technology, and we continue to invest to bring differentiated innovation to this large and fast-growing market.
In closing, I want to restate that I remain very confident in Boston Scientific's long-term outlook. We operate in attractive markets with approximately 75% of our business, historically growing approximately 6% for many quarters. We have an impactful cadence of future growth catalysts anticipated in '27 and '28 that we expect to drive meaningful improvement to our growth profile in '28 and beyond. We remain focused on execution and delivering our updated '26 guidance, taking appropriate action to evolve our organization that will create greater focus, speed and accountability, while ensuring we are continuing to invest in our long-term growth drivers.
I'm incredibly grateful to our global employees for their resiliency and winning spirit. And across all of our businesses and regions, I've seen our colleagues step up in extraordinary ways, adapting quickly and supporting one another and doing what it takes to ensure we are focused on what matters, improving patient lives through a relentless pursuit of innovation.
With that in hand, I'll hand over to Jon to provide more details.

**Jonathan Monson** (Executives):
Thanks, Mike. Before I provide details on our third quarter financial performance, I want to express my gratitude to our customers, physicians and employees for their patience and partnership as we work through the recent cyber incident. I'm very proud of our global teams who have worked diligently to restore operations and continue to support our customers and the patients that they serve. The cyber incident caused significant disruption to our business operations, and it materially impacted our third quarter financial results. Despite these challenges, we remain focused on taking the necessary actions to drive improved financial performance.
So turning now to the quarter. Third quarter consolidated revenue of $5.138 billion represents 1.5% reported growth versus third quarter 2025 and includes a neutral impact from foreign exchange which was in line with expectations. As a result, operational and organic revenue growth were also 1.5% in the quarter, below our third quarter guidance range of 3% to 5%.
We estimate the cyber incident had a net negative impact of approximately 300 basis points on third quarter organic revenue growth. This impact reflects the 8 business day disruption to our global network during which we were unable to manufacture or ship product, partially offset by revenue recovered as operations resumed.
Third quarter 2026 adjusted earnings per share of $0.73 declined 3% versus 2025, below our third quarter guidance range of $0.80 to $0.82. As Mike mentioned, third quarter results include an approximate $0.07 unfavorable impact from the cyber incident, primarily driven by lower-than-expected sales and the additional manufacturing and operation -- operating costs associated with the cyber incident.
Adjusted gross margin for the third quarter was 68.0%, representing a 300 basis point decrease versus the third quarter of 2025, primarily driven by unfavorable manufacturing absorption during the cyber-related disruption. Third quarter adjusted operating margin was 26.5%, contracting 150 basis points versus the third quarter of 2025, primarily driven by the impact of the cyber incident on gross margin. On a GAAP basis, third quarter operating margin was 16.1%. These results include an approximate $80 million charge primarily related to certain product liability cases.
Moving to below the line. Third quarter adjusted interest and other expenses totaled $124 million, which was in line with expectations. On an adjusted basis, our tax rate for the third quarter was 14.3%, which was higher than expected due to certain discrete tax items.
Fully diluted weighted average shares outstanding ended at 1.452 billion in the third quarter, and free cash flow for the third quarter was $867 million, with $1.047 billion from operating activities, less $180 million in net capital expenditures. As of September 30, 2026, we had cash on hand of $609 million, and our gross debt leverage ratio was 1.9x.
Our capital allocation approach remains disciplined and growth-oriented. Our top priorities remain strategic tuck-in M&A and opportunistic share repurchases while we continue to evaluate and fund the opportunities that we believe will create the greatest long-term value for our shareholders. We look forward to closing our acquisition of Penumbra, which we believe will strengthen our long-term growth profile through its innovative portfolio and strong strategic fit within our cardiovascular business.
In addition to tuck-in M&A, we're leveraging strategic partnerships to advance innovation, ensuring we're directing capital towards high-growth opportunities. Consistent with this approach, we recently entered into an agreement with Blackstone Life Sciences to co-fund the development of our VITALYST circulatory support system for the treatment of patients with cardiogenic shock.
Under the agreement, Boston Scientific will receive funding from Blackstone, which will be recognized as a reduction to R&D expense as the related costs are incurred. Upon achievement of certain milestones, expected starting in 2030, Blackstone will be eligible to receive a return on the actual amount funded for the program plus royalties on sales of VITALYST. This agreement allows us to continue advancing VITALYST while accelerating investments in other high-growth opportunities.
Before I discuss guidance, I want to acknowledge that we need to rebuild confidence in our forecast. We've implemented meaningful enhancements to our forecasting process, which we believe provide a stronger foundation for more accurate forecasting going forward. And so now I'll walk through our guidance for the fourth quarter and full year 2026.
We now expect full year 2026 reported revenue growth to be approximately 4.25% versus 2025. Excluding an approximate 50 basis point tailwind from foreign exchange based on current rates, we expect full year 2026 operational and organic growth to be approximately 3.75%. We expect fourth quarter 2026 reported revenue to decline in a range of down 3% to down 1% versus fourth quarter 2025. We anticipate no impact from foreign exchange based on current rates and therefore, expect fourth quarter 2026 operational and organic revenue to also decline in a range of down 3% to down 1%. As Mike mentioned, our fourth quarter guidance contemplates a headwind from the cyber incident, reflecting elevated customer ordering at the end of the third quarter, which we expect to normalize over the course of the fourth quarter.
We expect full year 2026 adjusted gross margin to be below full year 2025, reflecting a less favorable product mix, investment in our global supply chain and quality systems and the additional impact of the cyber incident. We now expect full year 2026 adjusted operating margin to be approximately 27.6%, reflective of gross margin pressures. We continue to expect full year 2026 adjusted below-the-line expense to be approximately $485 million.
Under current legislation, including enacted laws and issued guidance, we now expect a full year 2026 adjusted tax rate of approximately 12%. We expect full year 2026 free cash flow to be approximately $3.6 billion, reflecting a reduced operating income outlook. We expect full year 2026 adjusted earnings per share to be in a range of $3.16 to $3.18, representing growth of 3% to 4% versus 2025, including an approximate $0.06 headwind from foreign exchange, and we expect fourth quarter adjusted earnings per share to be in the range of $0.77 to $0.79.
As Mike outlined, we anticipate continued top line pressure into 2027, which we expect will make it challenging to grow revenue and adjusted earnings per share, excluding Penumbra. We expect our underlying business dynamics in Q4 to persist into 2027 and believe our fourth quarter guidance provides a reasonable baseline for next year's revenue and adjusted earnings per share outlook.
Importantly, we're taking decisive actions to drive greater focus, speed and accountability, most notably through our company-wide restructuring program. This comprehensive initiative is focused on org structure evolution, supply chain optimization, back-office transformation and reductions in other categories of spend. We expect these efforts to deliver sustained cost efficiencies while allowing us to prioritize investments that support long-term growth.
In closing, we believe we're well positioned in attractive markets. We're making the right investments and taking the necessary steps to strengthen our financial performance. I'm confident that these actions will position us to stabilize Boston Scientific in 2027 and then drive improved revenue and adjusted earnings per share growth in 2028 and then further acceleration in 2029. For more information, please check our Investor Relations website for third quarter 2026 financial and operational highlights, which outlines more details on third quarter results and 2026 guidance.
And so Lauren, with that, I'll turn it back to you to moderate the Q&A.

**Lauren Tengler** (Executives):
Thanks, Jon. Drew, let's open it up for questions for the next 30 minutes or so. [Operator Instructions] Drew, please go ahead.

**Operator** (Operator):
[Operator Instructions] The first question comes from Robbie Marcus with JPMorgan.

**Robert Marcus** (Analysts):
A lot to dig into. I'll stick with one here and focus on guidance. Maybe you could -- and there's a lot of questions I'm getting from investors. So hopefully, this will help clarify. How do we think about sort of the actual underlying impact from the hack disruption in third quarter? It sounds like there was some order benefits. What's the actual impact and why bleeding into fourth quarter? And with the no growth comment on 2027, how much of that is conservatism related to the hack? And how much is new information of end market and product timing?

**Michael Mahoney** (Executives):
Jon, do you want to take the cyber question?

**Jonathan Monson** (Executives):
Sure. Yes. Thanks, Robbie. So let me lay out the impacts of cyber. So in Q3, we estimate a roughly 300 basis point headwind to our revenue from cyber, so call it roughly $150 million of headwind on the top line and then bottom-line impact to EPS of $0.07. So the impact of the lost sales, we did have unfavorable manufacturing absorption that contributed to the $0.07 of EPS as well as other direct costs, expedited shipping, cost of experts that impacted Q3 cyber. For the fourth quarter, we expect an ongoing impact of approximately 200 to 300 basis points.
And so what we saw, Robbie, coming out of the cyber incident is a level of stocking of -- from customers. And over the fourth quarter, we'll burn off some of those inventory levels. So that's why you see the ongoing impact into the fourth quarter of that 200 bps to 300 bps. And that drops through down to EPS, roughly $0.04 to $0.05 of impact in the fourth quarter.

**Michael Mahoney** (Executives):
Yes. Maybe just some comments on the '27 question. When we think about it, we obviously aim to exceed these expectations. But just to frame and we'll give our guidance, obviously, in January. We really do expect some of the underlying business dynamics that we see in the fourth quarter to persist in 2027.
So if you look at that, you've got a number of our businesses doing extremely well, Interventional Cardiology, Vascular, IO&E, Endoscopy's underlying business is doing quite well despite the pressures in China. So the overall base business, we feel is consistently growing about 6%. We expect about 1 point of impact due to the comprehensive China pricing issues, and that represents about 75% of the business.
So the 2 key areas -- questions are, what will be the impact of WATCHMAN and EP in 2027? So for the basis of our early framing of guidance, we wanted to be appropriately conservative. So we're assuming that the WATCHMAN market dynamics do not improve over current state. And we're obviously doing a lot to turn that around. But those underlying markets today are growing at about negative 7%, negative 8-ish percent, in that area. And we do have a competitive launch coming in 2027. So the error bars around on the market -- around the WATCHMAN assumptions are quite wide, given that we are assuming no improvement in the market despite some of our efforts and an anticipated label change, where we're assuming that the market baseline stays similar to Q4 with competitive entry in '27.
Similarly, in EP, EP will be a challenging year for us in '27, and we're very optimistic about '28 and '29 based on our product launch cadence. But in '27, we are lacking new product launches. The market continues to be fairly healthy, but we expect to continue to cede share in 2027 in EP, similar to the rates that we've seen in the second half of 2026. Until we successfully launch ICE program in second half of '27, an excellent platform upgrade with FARAPULSE Ultra, ideally late fourth quarter, early first quarter '27 (sic) [ '28. ] And as you know, we've initiated our clinical trial of our FARAFLEX platform, which will be an early '29 launch. So hopefully, that gives you some context for 2027.

**Operator** (Operator):
The next question comes from Larry Biegelsen with Wells Fargo.

**Larry Biegelsen** (Analysts):
So super helpful color on 2026 and 2027. Mike, just talk about your confidence in improving sales and EPS growth in '28. I'm not looking for specifics, obviously, but what are the drivers? It looks like FARAFLEX, the launch was pushed out to 2029 in the slides, if I'm reading that correctly. And I think there are some concerns about new PFA competition coming in '28, with a novel waveform. And so how are you factoring that in?

**Michael Mahoney** (Executives):
Yes. Thank you. Just a backdrop a bit and maybe not new news. '23 to '25, we experienced a very high growth cycle, much on the heels of our base business being strong and the tremendous growth of our WATCHMAN and EP. We also had a decent first half despite some of our forecasting challenges, growing 8% in the first half of 2026. We are clearly in the middle of a down cycle, which is a short-term phenomenon for Boston Scientific that you will see -- that we predicted in the fourth quarter based on our guide in 2027. We are very confident about the return to growth and kind of pushing off the bottom in '27 as we enter '28.
And a high-level formula for growth in '28, potentially below our WAMGR, but solid growth and growth above our WAMGR in '29 really are the -- if you look at our 3 segments.
Our biggest segment, as you look at 2028, will be our Interventional Cardiology, Vascular and Penumbra business. We expect that collection of businesses to comfortably grow above their market WAMGR as Penumbra goes organic and they continue to drive excellent momentum with a very strong portfolio cadence in that business with our IVL platforms in peripheral and vascular, potentially hypertension in 2028 and a strong cadence of imaging capabilities as well as launches within our VT, IO&E platform. So that will represent our biggest segment, very much on offense, growing above WAMGR and propelling the growth of the company.
Our MedSurg business, with a number of key launches, you saw a couple of key approvals just this quarter in our Urology business. We expect our MedSurg segment businesses to essentially grow at our market WAMGR or grow at their market WAMGR, call it, mid-single digits. So then it really comes down to what happens to EP and WATCHMAN and CRM. The good news in CRM is we'll be launching a significant platform launch with Denali, our defibrillator platform, which we expect CRM will comfortably return to growth in 2028 to help that segment.
And then in WATCHMAN, we will anniversary a competitive launch in 2028. We'll be in the midst of a trial of our fourth-generation platform. As you know, we've got a very, very strong share in WATCHMAN, and we expect to maintain that strong leadership position during this case. And we'll also aim to have an approved label change ideally by 2028. So we see the WATCHMAN business kind of maximum down is in 2027, and will return to a healthier position in 2028.
Similar with our EP business, again, it's driven by portfolio and cadence. And as I mentioned before, we'll have our ICE platform launch, our full year of FARAPULSE Ultra and pending approval of our FLEX business. So we expect the overall Rhythm Solutions business with a stronger growth in CRM and improving cadence of effective launches in EP and WATCHMAN to significantly improve the growth profile of Rhythm in '28, whereas 2027, that segment is driving the challenges.

**Operator** (Operator):
The next question comes from Joanne Wuensch with Citi.

**Joanne Wuensch** (Analysts):
Two parts. One part is, internally, it sounds like you're doing quite a bit to build the bridge between today and 2028, which could include any number of things such as sales force realignment, expense reduction, et cetera, et cetera. Could you please address what you're doing internally to build that bridge? And then second of all, the Penumbra delay, is there a way to share the steps to that resolution?

**Michael Mahoney** (Executives):
Sure. We're certainly -- and Jon, you can comment a bit more. As you would expect, we're aligning our cost structure to a reality of what we see in fourth quarter in 2027. So the team has gotten ahead of that about 6 months ago and are implementing a pretty meaningful restructuring program, both in terms of where we -- our discretionary spend, head count. We want to delayer the company a bit more, increase some of the spans and layers in the organization and get after some SG&A offsets. So that program is very much in flight. 
Importantly, we maintain the really important cultural values of Boston Scientific that makes it a special place to work and focus on advancing science for life and our winning spirit. So we believe we will continue to drive an important culture within Boston Scientific focused on the future despite the needed restructuring initiatives.
Importantly, while we're doing that, we're also continuing to invest in these big growth platforms that will drive the company's growth back to a decent growth in '28 and above-market WAMGR and entering all these new markets that we're taking on. So I think it's important that we show the discipline to drive those cost savings and invest in our growth drivers at the same time.

**Jonathan Monson** (Executives):
And Joanne, I'd just add with the restructuring program, I'll fill in a couple of pieces there. So anticipate to achieve over $500 million of savings from the program over the next 3 years, been some tough decisions, but I've been very pleased with how we've been tracking. We're a little ahead of where I thought we'd be at this point in the program. I expect to achieve over half of those savings exiting 2027. So back to Larry's question, that contributes to our confidence in 2028. Mike went through the top line, but from an EPS perspective as well.
Program itself, focused on streamlining org structures, back-office transformation to streamline our processes, leverage shared services. There's a supply chain optimization looking across our global supply network, to better leverage technology, AI and streamline across supply chain and then a broader initiative just looking at other pools of spend like T&E and meetings, like use of external vendors to reduce our spend there. So it's a very broad initiative, but very focused. And again, I've been pleased with how we've been tracking. We're a little ahead of our schedule there.

**Michael Mahoney** (Executives):
And sorry, Joanne, on the Penumbra comments, maybe some good and bad news. Overall, we're super impressed with the Penumbra results for 2026. And the good news is with a bit of an extended closing period, we've continued to get to know the Penumbra team extremely well, how they run the business, the synergies that are very obvious on growth side and some on the cost side when you combine 2 powerful businesses with Interventional Cardiology, Vascular and the Penumbra business. So we're very bullish on the Penumbra team, the progress, the innovation pipeline they have and how they will work very seamlessly within Boston Scientific to drive ongoing strength in Penumbra and our ICVT business.
On the regulatory process, it has taken a bit of time. We're still very confident in closing the transaction. But based on some of the discussions with the regulatory authorities, we anticipate an early first quarter close.

**Operator** (Operator):
The next question comes from Rick Wise with Stifel.

**Frederick Wise** (Analysts):
Mike, I was hoping maybe you could further unpack the MedSurg outlook a little bit. You said, I think, just a moment ago, you expected the combined business to grow mid-single digits, sort of in line with the WAMGR market growth. But maybe talk us through each piece. Historically, these are businesses that in totality grew 7% or 8%. Why can't we dream or aspire for you to get back to that kind of range? And maybe what needs to happen in Urology, Endoscopy and Neuro to get back there? And what are the key drivers here as we look ahead to the next year or 2?

**Michael Mahoney** (Executives):
Yes, I would agree. 5% to 6%, mid-single-digit growth is not what we want MedSurg to be and not what it's been and not what the potential is. Just to break through the 3 of them really quickly. Neuromodulation is doing very well. Our Brain franchise is doing well. We've really diversified our Pain business into more minimally invasive alternatives in addition to spinal cord stim. And we continue to have additional growth drivers in that business with a whole new SCS launch that will happen in 2028. So overall, I would assume kind of over a period of time, the Neuromod business will continue to be accretive to the MedSurg growth profile.
Our Endo business is very strong. We've got a list of quite a few product launches in that area with scopes and our Versatile platform and a number of others. The headwind in 2027 for Endo is China. Significant pricing erosion we will see in our China business in 2027. So the Endo business will anniversary that China pricing impact in fourth quarter 2027. So we expect kind of our Endo business to be at that mid-single-digit growth range in '27, accelerate in '28 based on launching and getting -- lapping that China piece.
The challenge, quite frankly, has been Urology. And we've been wrong on calling the growth trend in Urology. Obviously, a lot of efforts are going on in that area. So we expect the Urology business to improve in 2027, not back to its previous levels, but certainly not at a negative growth profile that we see in 2026. And this business is all about people and portfolio. We just announced in our script there, we've got 3 Stone launches that -- or 3 Stone approvals, which has been the one segment that's been lagging the growth for that franchise. So we expect our core Stone business to improve in 2027.
And as you know, you've heard for many quarters now, we've struggled a bit with the Axonics integration. We've done great with the Silk Road integration, with Nalu integration, but we struggled with Axonics. Based on significant commercial turnover, we've done a lot to hire a lot of new reps and clinical people in that area. It takes a bit of time for them to get seasoned in their territories, but we expect to see improvement in that in 2027. 
So in short, '27, we think Endo and Uro will be in that kind of lower to mid-single-digit range and Neuro slightly higher. And Endo and Uro both lapping significant China VBP pricing in fourth quarter '27 to have a stronger '28. But we -- overall, we do aim to get back to kind of that 7% to 8%-ish numbers that we used to see.

**Operator** (Operator):
The next question comes from Travis Steed with Bank of America.

**Travis Steed** (Analysts):
I wanted to ask on the pipeline. There was a lot of things kind of across the board pushed out. Is there something bigger picture going on, on the pipeline -- of the derisking of the pipeline? And also, Jon, you mentioned better forecasting abilities. So just curious if you could elaborate on that as well?

**Jonathan Monson** (Executives):
Yes, Travis, I'll start on the forecasting question and then turn to Mike and Joe is in the room here to go through the pipeline. 2026 has been a challenging year for us, as Mike said, after several years of exceptional growth, driven in large part by EP and WATCHMAN, we've seen that cycle turn. So we're in a tough business cycle now because of the dynamics predominantly within those 2 businesses. And we've struggled to forecast that this year, and we need to be better. I recognize that, Mike knows that, Joe knows that. The whole team here knows that.
We feel we've got a clear picture of the business dynamics now. We've laid that out. We're taking action with the restructuring program. We have our new operating model, which will drive greater focus, greater speed, greater accountability. And from a forecasting process perspective, we've made a number of enhancements, implemented more sensitivity and scenario analysis, more objective models, more third-party data that we pull in. 
So we feel with all of that together, you'll see improved forecasting accuracy from us on a go-forward basis. And with the guidance that we put forth for the fourth quarter here and the framework for 2027, very, very focused on delivering on that.
Mike, Joe, pipeline?

**Michael Mahoney** (Executives):
Maybe just quick things. We pride ourselves in executing. '26 has not been the year we've executed so well. So we're -- we've done a lot to tighten our performance. Jon just went through some of our forecasting areas. In terms of the overall business, the business has gotten larger. So one of the reasons for the -- for Joe now becoming COO and breaking up the sectors is to have even more focus on these sectors. So we improve our efficiency and reliability in terms of the dates that we give you for these big launches.
We do have a very impressive pipeline that's coming for the company. We're down for a bit, but we're far from out and these pipeline products will come through and return Boston Scientific to its high-performance reputation that we want to earn back with you. Some of these products are complicated with clinical trials and regulatory processes.
So we've kind of seen about a 6-month delay in some of these big platforms. We want to make sure we launch them at that high scale with high quality and we aim to do that, but the pipeline is very rich, and we can go through some of those elements and Joe can provide more detail. But we're not happy with some of the slips. We've put a lot of focus on it, and we know the impact it has on the business.

**Operator** (Operator):
The next question comes from Josh Jennings with TD Cowen.

**Joshua Jennings** (Analysts):
Mike, I was hoping to just clarify just the outlook for the WAMGR as you've given, strong -- good high color -- high-level color on '27 and '28. 2026 WAMGR is 7% is -- you got some pipeline products, potentially could expand. But is the assumption baked into some of your high-level color in the out years that, that WAMGR is sustainable at that 7% level? And then just a side question, maybe just hoping to get an updated outlook on your view of the market, the U.S. EP market and growth there as we move into '27 and '28?

**Michael Mahoney** (Executives):
Yes. On the WAMGR, we don't -- we're not used to growing below our WAMGR. We think it's still about 7%. We've seen some pressure overall in maybe the Uro market and Endo markets that have pushed it down a bit to that 7% level. EP market continues to remain very strong. Obviously, the WATCHMAN market has pulled that WAMGR to that 7% range, but the WATCHMAN market is about a $2 billion market overall.
Importantly, as you look at the LRP, we're entering markets that grow faster than our WAMGR. The IVL market, potentially the hypertension market and some big launches in EP and segments that we don't play in today with ICE and also with FARAFLEX. So I think overall, kind of that 7% WAMGR today, and in that 7% but maybe -- and then you're adding Penumbra, which is at scale, an accretive WAMGR to the business or at least in line.
So I think that kind of 7% range now and maybe 7% to 8% over the next 3 years is about the right way to call it. When we look at '27 based on the comments that we made -- I'm sorry, when we look at '27, obviously growing below the WAMGR based on the comments that we made. And in '28, we aim to get back to closer to those WAMGR numbers and beyond.

**Operator** (Operator):
The next question comes from Marie Thibault with U.S. Bank BTIG.

**Marie Thibault** (Analysts):
I wanted to circle back to the commentary on no growth for 2027 when it comes to EPS. We heard Jon talk about some of the restructuring efforts that are being put in place. I know this quarter, you were able to offset things like expedited shipping costs related to the cyberattack, you were able to offset some of that with a better OpEx control.
So thinking about all of this, when we think about no growth in adjusted EPS next year, is it really about product mix and some of those less profitable products being the contributors to sales growth? Or why else shouldn't we expect some adjusted EPS growth given some of the efforts you're putting in place?

**Jonathan Monson** (Executives):
Mix is the biggest factor, Marie. So as we talked about, do you see pressure on the top line, that pressure predominantly is with WATCHMAN and EP. So we'll feel the mix impact of that within gross margin. And then with the China pricing pressure that we see escalating, that will also impact gross margin in 2027 as well. And we do have some investment that we continue to make across supply chain, our quality systems.
So as you look ahead to 2027, and we'll give the guide in all the detail on the Q4 earnings call, but expect significant pressure in gross margin next year. And we'll continue to invest in the portfolio. We have a lot that we're excited about in the portfolio and want to make sure we're fully funding those initiatives.
Now again, we will have restructuring that will help to offset some of those costs. We'll continue to be very disciplined with spend in 2027. But as you put that all together, I would expect our EPS next year to be roughly in line with revenue. And again, on our commentary, expect to be challenged to grow next year.

**Operator** (Operator):
The next question comes from Pito Chickering with Deutsche Bank.

**Pito Chickering** (Analysts):
Can you talk about what's causing the delay of the THRIVE data and therefore, the TIVUS launch? And on VITALYST, I think you said you weren't looking at high-risk PCI. Can you talk about what you're seeing with the product? And do you think the market is still attractive with just shock?

**Ken Stein** (Executives):
Yes, Pito, it's Ken. Maybe let me start with VITALYST. So there was data from a competitor released last year that I think called into question the broad use of mechanical circulatory support for high-risk PCI. We still believe that there is a role for that therapy there. But we do, I think, as a field, need to figure out better patient selection.
The pivot to first studying cardiogenic shock, it's very important to realize just how much of an unmet medical need there is in AMI cardiogenic shock. There is still mortality approaching 50% patients who present with acute MI and shock, and it occurs in up to 10% of patients who are having an ST-elevation MI. 
Data was presented a couple of years ago. The DanGer Shock trial showed beyond a doubt that mechanical circulatory support can reduce mortality in those patients. So this is both an area of major need and an area where we know that mechanical circulatory support can improve outcomes.
And we believe that with our VITALYST platform, we have differentiated advantages over the current incumbent in terms of dealing with shock. VITALYST has a novel catheter design that improves positional stability, that's particularly important in dealing with shock patients, where the catheter needs to stay in place in the CCU for a longer period of time, along with strategies aimed at just minimizing the complexity of managing these patients and minimizing vascular complications. And so that's why we're so excited about the potential for the VITALYST platform and well, actually we like the move into AMI shock as the first trial.

**Lauren Tengler** (Executives):
And then on THRIVE?

**Ken Stein** (Executives):
THRIVE, really, again, it's just a matter of continuing to execute on enrollment in the clinical trial. Enrollment, I think, frankly, has been a little bit slower than we would have hoped as we navigated the transition and the integration of the SoniVie team into the Boston Scientific ecosystem. But again, are confident that we can get that on track and that we will eventually finish enrollment in the trial. I believe in the technology. We do believe that ultrasound is the best for the energy sources that we can use for doing renal denervation. And we continue to believe that the THRIVE platform has differentiated advantages over the 2 current approved devices for renal denervation for hypertension.

**Operator** (Operator):
The next question comes from Matthew O'Brien with Piper Sandler.

**Matthew O'Brien** (Analysts):
Just a follow up on the pushback on the pipeline because that's what we're all kind of banking on at this point. Is the pipeline coming through? You just mentioned TIVUS and what's happening there. But with Ultra and with FLEX, is it product related? Is it enrollment? Is it manufacturing? What's slowing things down in terms of getting those to market? And then just anything more you can provide on Penumbra and a modest push on the timing there? Is it more regulatory questions, specific product-related questions, just anything on those things.

**Michael Mahoney** (Executives):
Yes, we won't provide any more updates on Penumbra other than what I commented on. We're very bullish on the transaction, and we're aiming to close that as early as we can. Likely, it will be pushing into early '27. In terms of the -- some of the product delays, Joe's here. Joe, any additional comments...

**Joseph Fitzgerald** (Executives):
I'll take Ultra first. As you know, Ultra is a PMA supplement, does not require a clinical study. So most of the issues we have there are just on getting through what we call design verification and validation. And if you look at Ultra, that's a hardware, software and a catheter project. So the, let's call it, one-quarter delay that you see is just a summary of issues that we have to work through with DV, it has nothing to do with anything on the clinical trial because we don't need clinical data to get Ultra approved.
On FARAFLEX, I would call it 3 things. It is related to our negotiations with FDA on getting the actual IDE approved. We've had slight delays with CMS full approval. And there are some operational challenges getting everything that's needed to complete a FARAFLEX case done to expand the number of sites. So we believe we will have that largely -- we just got CMS, and we believe our supply chain to support the study will be pretty robust by end of year. So I think when we get on the Q4 call, a good question for us will be how is enrollment going in the FARAFLEX study, which we expect that to ramp each successive week and month going forward.

**Operator** (Operator):
I understand there is time for one last question, that would be from Matt Taylor with Jefferies.

**Matthew Taylor** (Analysts):
I wanted to follow up on the Penumbra, not on the timing. But could you talk about the kind of growth that you expect from that platform? And before you had said in the first year, it could be $0.06 to $0.08 dilutive, but some of the math there has changed. I was wondering if you could update us on that. It's decelerated a little bit in the last couple of quarters. So I just wanted to get an update.

**Jonathan Monson** (Executives):
Yes. Thanks, Matt. I'll take the dilution piece and then Mike and Joe can give quick comments on the growth profile. But we're excited to add Penumbra. You can see from their results, they're performing very well, high growth, would be a great addition to our cardiovascular portfolio.
So we announced Penumbra in mid-January. We Anticipate closing in early 2027 at this point. At the time of announcement, we had said we expected $0.06 to $0.08 of dilution and that assumes no divestitures, that assumes interest rates that were in place at that time. We have seen increases in interest rates since then, so that will drive incremental financing costs and I think will put additional pressure on the EPS dilution that we'd expect. But once we close the deal, we'll provide much more detail.

**Lauren Tengler** (Executives):
Thanks so much, Jon. Thank you for joining us today. We appreciate your interest in Boston Scientific. If we were unable to get to your question or if you have any follow-ups, please don't hesitate to reach out to investor -- the Investor Relations team. Before you disconnect, Drew will give you all of the pertinent details for the replay. Thanks, everyone.

**Operator** (Operator):
Thank you. Please note, a recording will be available in 1 hour by dialing either 1 (877) 344-7529 or 1 (412) 317-0088 using replay code 8506317 until November 11, 2026, at 11:59 p.m. Eastern Time.
The conference has now concluded. Thank you for attending today's presentation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### BSX_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CEO Mike Mahoney｜guidance：CEO 下修 2026 全年有機營收與調整後 EPS 指引（原話："updating our full year 2026 guidance for organic revenue"）
- 2026-07-29｜CEO Mike Mahoney｜guidance：第三季有機營收成長與調整後 EPS 指引（原話："guiding to organic revenue growth of 3% to 5%"）
- 2026-07-29｜CEO Mike Mahoney｜guidance：CEO 說明下修集中在 WATCHMAN 與 EP 兩處（原話："Our guidance reduction is concentrated in 2 areas"）
- 2026-07-29｜CEO Mike Mahoney｜guidance：管理層對 2027 的假設：營收成長低於 WAMGR、EPS 成長有限（原話："revenue growth below our WAMGR and limited adjusted EPS"）
- 2026-07-29｜CFO Jon Monson｜guidance：CFO 拆解下半年指引：EP 持平、WATCHMAN 中高個位數衰退、其餘約 6%（原話："approximately flat growth in our global Electrophysiology"）
- 2026-07-29｜CFO Jon Monson｜guidance：CFO 給 2026 全年調整後營業利益率擴張幅度（原話："expand full year 2026 adjusted operating margin by 0 to"）
- 2026-07-29｜CEO Mike Mahoney｜guidance：WATCHMAN 全球全年與下半年指引（原話："global WATCHMAN growth to be flat to low-single digits"）
- 2026-07-29｜CEO Mike Mahoney｜guidance：美國 EP 第三季較第二季季減，全年持平至低個位數（原話："our Q3 sales will sequentially decline mid-single digits"）
- 2026-07-29｜CEO Mike Mahoney｜guidance：Urology 全年成長指引下修至持平至低個位數（原話："our CRM growth will be flat on a full year basis"）
- 2026-07-29｜CEO Mike Mahoney｜guidance：CRM 全年預期持平，EluPro 貢獻下半年小幅改善（原話："We now expect full year 2026 free cash flow"）
- 2026-07-29｜CFO Jon Monson｜guidance：全年自由現金流指引（原話："We now expect full year 2026 free"）
- 2026-07-29｜IR Lauren Tengler｜guidance：指引不含 Penumbra 收購（原話："Guidance excludes the previously announced agreement"）
- 2026-07-29｜CFO Jon Monson｜margin：第二季調整後毛利率與年增幅度（原話："Adjusted gross margin for the second quarter was 70.3%"）
- 2026-07-29｜CFO Jon Monson｜margin：2026 全年調整後毛利率預期低於 2025，原因為產品組合（原話："adjusted gross margin to be below full year 2025"）
- 2026-07-29｜CFO Jon Monson｜margin：第二季 EPS 優於指引主因為有利的一次性稅項（原話："primarily driven by favorable discrete tax items"）
- 2026-07-29｜CFO Jon Monson｜margin：GAAP 營業利益率包含產品責任費用與 IEEPA 關稅退款（原話："approximate $75 million charge related to certain product"）
- 2026-07-29｜CFO Jon Monson｜margin：CFO 說明 2027 EPS 成長有限、營業利益率改善有難度的原因（原話："improving op margins will be a challenge"）
- 2026-07-29｜CFO Jon Monson｜margin：Penumbra 預期對 2026 營業利益率與 EPS 小幅稀釋（原話："improving op margins will be a challenge"）
- 2026-07-29｜CFO Jon Monson｜margin：重組節省將先反映在 SG&A，之後才是 COGS（原話："I'd expect to see them materialize in SG&A"）
- 2026-07-29｜CEO Mike Mahoney｜commitment：CEO 公開承擔下修責任（原話："I do take responsibility for the guidance reduction"）
- 2026-07-29｜CEO Mike Mahoney｜commitment：管理層承諾 2028 回到營收與 EPS 顯著改善（原話："We expect our revenue and EPS growth"）
- 2026-07-29｜CEO Mike Mahoney｜commitment：重組方案目標：2029 年底前年化節省約 5 億美元（原話："approximately $500"）
- 2026-07-29｜CFO Jon Monson｜commitment：CFO 給重組節省與支出的時程：2027 年底前實現過半（原話："over half of our run rate savings and incur over half"）
- 2026-07-29｜CEO Mike Mahoney｜commitment：2027 不給精確指引，僅給框架：目標優於 2026 下半年指引（原話："we aim to improve 2027 versus"）
- 2026-07-29｜CEO Mike Mahoney｜commitment：EP 目標 2028 回到市場或以上成長（原話："at market or above market growth in EP in '28"）
- 2026-07-29｜CEO Mike Mahoney｜commitment：Urology 2027 預期改善、接近市場成長率（原話："We expect to get closer to at-market growth in 2027"）
- 2026-07-29｜CEO Mike Mahoney｜commitment：管理層表示將改進預測流程（原話："we are sharpening our forecasting processes"）
- 2026-07-29｜CEO Mike Mahoney｜risk：WATCHMAN 美國市場急遽放緩，歸因於累積的臨床證據影響轉診（原話："the U.S. market has slowed sharply and unexpectedly"）
- 2026-07-29｜CEO Mike Mahoney｜risk：WATCHMAN 單獨手術（非併行）年減低十位數百分比（原話："we saw low-teens declines versus"）
- 2026-07-29｜CEO Mike Mahoney｜risk：預期 2027 年有新競爭者進入 LAAC，WATCHMAN 可能流失份額（原話："likely we'll have some share erosion in"）
- 2026-07-29｜CEO Mike Mahoney｜risk：指引不假設 2027 年 WATCHMAN 改善，直到動態實際改變（原話："we are not assuming improved"）
- 2026-07-29｜CMO Ken Stein｜risk：CMO 指出 OCEAN／closure 等試驗的影響大於預期，且 wait-and-wait 策略使用增加（原話："much greater use of the so-called wait-and-wait strategy"）
- 2026-07-29｜CEO Mike Mahoney｜risk：Urology 第二季僅成長 1%，薦骨神經調節復甦比預期久（原話："much greater use of the so-called wait-and-wait strategy"）
- 2026-07-29｜CEO Mike Mahoney｜competition：EP：管理層承認低估美國競爭對手搶份額（原話："recovery in that business taking longer than we had"）
- 2026-07-29｜CEO Mike Mahoney｜competition：管理層稱美國 PFA 已占 AFib 市場約 80%，限制抵銷競爭壓力的空間（原話："which does limit our ability to offset some"）
- 2026-07-29｜CEO Mike Mahoney｜competition：已調整市占假設以求更務實（原話："we have adjusted our market share assumptions to ensure a"）
- 2026-07-29｜CEO Mike Mahoney｜competition：EP 美國份額下滑趨勢預期延續至 2027 上半年（原話："We have lost some share in the U.S."）
- 2026-07-29｜CEO Mike Mahoney｜competition：CRM 面臨競爭壓力與產品組合缺口，PRECEDENT 預計 2027 下半年上市（原話："we are seeing competitive pressure with some portfolio gaps"）
- 2026-07-29｜CEO Mike Mahoney｜competition：WATCHMAN 在 LAAC 市場份額約 91%（原話："we're about 91% share of the market"）
- 2026-07-29｜CEO Mike Mahoney｜product：EP 管線：FARAWAVE Ultra 與 ICE 市場進入時程（2027 下半年），FARAFLEX 2028（原話："We have lost some share in the U.S."）
- 2026-07-29｜CEO Mike Mahoney｜product：FARADIGM 關鍵試驗開始收案（FARAFLEX）（原話："we commenced enrollment in"）
- 2026-07-29｜CMO Ken Stein｜product：WATCHMAN 後續證據：SIMPLAAFY 預計下半年公布，並提到 CHAMPION 標示更新與 CMS 覆蓋決定（原話："I'd highlight our SIMPLAAFY trial"）
- 2026-07-29｜CEO Mike Mahoney｜product：WATCHMAN 三項重啟成長優先事項之一：直接面向病患投資（原話："we are seeing competitive pressure with some portfolio gaps"）
- 2026-07-29｜CEO Mike Mahoney｜product：SEISMIQ 4CE 冠狀動脈 IVL 預計 2027 上半年上市（原話："we're about 91% share of the market"）
- 2026-07-29｜CEO Mike Mahoney｜product：腎臟去神經 THRIVE 試驗，預期 2028 上市（原話："continue to anticipate bringing our"）
- 2026-07-29｜CEO Mike Mahoney｜product：WATCHMAN 併行手術占美國手術約三分之一（原話："improve in the second half of 2027 after the introduction of"）
- 2026-07-29｜CMO Ken Stein｜customer：CMO 指出單獨 WATCHMAN 手術的轉診流失集中在軟性適應症（原話："we commenced enrollment in"）
- 2026-07-29｜CEO Mike Mahoney｜customer：第二季區域與事業單位表現：Neuromod 成長 12%、IC 成長 15%（原話："I'd highlight our SIMPLAAFY trial"）
- 2026-07-29｜CEO Mike Mahoney｜customer：管理層估計 WAMGR 為 7%-8%，較先前下調約 1 個百分點（原話："accelerating direct-to-patient investments to stimulate"）
- 2026-07-29｜CFO Jon Monson｜capital_allocation：CFO 陳述資本配置優先順序（原話："bringing SEISMIQ 4CE to market in the first half of '27"）
- 2026-07-29｜CFO Jon Monson｜capital_allocation：宣布對 MiRus 投資 15 億美元（含收購 TAVR 事業的獨家選擇權），並完成 20 億美元加速股票回購（原話："we announced a $1.5 billion investment in MiRus"）
- 2026-07-29｜CFO Jon Monson｜capital_allocation：全年調整後利息及其他費用上調，反映 MiRus 與 ASR 融資影響（原話："1/3 of WATCHMAN procedures in the U.S. are done"）
- 2026-07-29｜CFO Jon Monson｜capital_allocation：期末現金與毛負債槓桿比（原話："our gross debt leverage ratio was 2.0x"）
- 2026-07-29｜CEO Mike Mahoney｜capital_allocation：Penumbra 預計 2026 下半年交割，待剩餘監管許可（原話："We anticipate the deal will close in the second half of '26"）

### 問答異常語氣（迴避／改口／保留）
- BSX_Q2_2026_Earnings_Call_20260729.md｜問：Robbie Marcus（JPMorgan）：此次下修是否已保守到可排除未來負向修正？以及 2027 買方預期約 5% 有機成長是否合理｜答法：未直接確認買方 5% 預期，改談 75% 業務成長 6%、EP/WATCHMAN 為下修主因；僅稱 2027「aim to do better than our guide for the second half of 2026」，未給數字
- BSX_Q2_2026_Earnings_Call_20260729.md｜問：Joanne Wuensch（Citi）：2026 年 5%-6% 是否可作為 2027 起點｜答法：未確認該區間，稱 2027 精確指引要到 1 月才給，只給「aim to improve 2027 versus our second half 2026 guidance」框架
- BSX_Q2_2026_Earnings_Call_20260729.md｜問：Travis Steed（BofA）：2027「limited EPS growth」是持平、與營收同步，還是仍有槓桿；2028 是否回到雙位數｜答法：未回答具體數字或 2028 是否雙位數，改談 Q4 財報會再說明、重組方案與成長催化劑，僅稱 2028 起 'strong EPS growth'
- BSX_Q2_2026_Earnings_Call_20260729.md｜問：Larry Biegelsen（Wells Fargo）：是否仍預期依 CHAMPION 3 年數據取得一線適應症標示｜答法：未正面回答標示時程，改談市場假設與競爭者進入；另一場 Q&A 中僅稱 'if labeling occurs in 2027, there obviously could be some upside'

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
{"date":"20260710","verdict":"迴避","role":"不持有","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"PFA 領導地位可守（成長引擎不崩）","columns":{"2Y 驗證點":"US EP 有機成長回正且份額止跌","5Y 驗證點":"PFA 品類仍擴張、BSX 維持 ≥ 前二","10Y 驗證點":"次世代 PFA（Farawave Ultra）延續代次領先","數字門檻":"PFA spend-share ≥ 40%；US EP 有機 ≥ +8%","來源":"Citi/Guidepoint 調查、BSX 法說（管理層自稱 mid-2027 leadership）","漂移觸發":"連 2 季 TTM EP 成長偏離 ≥ 5% → 削弱"}},{"id":"H2","text":"多元化醫材（心血管/內視鏡/泌尿/神調＋Penumbra）可補 EP/Watchman 放緩","columns":{"2Y 驗證點":"非 EP 分部有機成長維持 mid-single＋","5Y 驗證點":"Penumbra 整合達 synergy、增量 ROIC &gt; WACC","10Y 驗證點":"資本配置飛輪維持 &gt; WACC 報酬","數字門檻":"公司整體有機成長守 6.5-8%（2026 guidance 下緣）","來源":"Q1 FY2026 法說（泌尿僅 +1%）、Penumbra 8-K","漂移觸發":"連 2 季有機 &lt; 6% → 削弱"}},{"id":"H3","text":"12x 遠期本益比是估值底（下行有限）","columns":{"2Y 驗證點":"倍數不再壓縮、共識停止下修","5Y 驗證點":"成長止穩後 re-rate 回 mid-teens","10Y 驗證點":"—","數字門檻":"Fwd PE ≥ 12x 維持；共識 EPS 不再下修","來源":"yfinance/財報；MDT 對照（現 12.2x）","漂移觸發":"共識連 2 季下修 或 倍數破 11x → 反轉（H3 高度不確定，見 §11）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"US EP 份額續流失（MDT/JNJ/ABT 四強混戰，spend-share 已被反超）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"US EP 有機成長、獨立調查 spend-share","警戒閾值":"連 2 季有機 &lt; +5% 或 share &lt; 38%"}},{"id":"R2","text":"Watchman 撞 CMS 給付砍（2026 ~19%、2027 完整 ~35%）＋競品上市","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Watchman 美國量 YoY、2027 CMS 最終規則","警戒閾值":"連 2 季量負 或 2027 完整砍確認"}},{"id":"R3","text":"$14.5B Penumbra 整合減損／過度槓桿／FTC 拖延；聯邦調查與集體訴訟裁罰","columns":{"對應假設":"H2/H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"淨負債/EBITDA、synergy 兌現、docket 進度","警戒閾值":"淨負債/EBITDA &gt; 3.5x 且 synergy 落後、或不利和解"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"3-of-3 AND 全數成立方重跑 DD：① US EP 有機成長連 2 季止穩且份額止跌；② Penumbra 整合無減損、槓桿回落；③ 證券集體訴訟/聯邦調查落地無重大裁罰或給付風險。任一未過即維持迴避。","irr_base_pct":7.6,"ev5y_pct":29.0,"drift_watch_prior":{"dca_verdict":"迴避","dca_role":"不持有","signal":"C","val":"🟢","ma":"❌","trap":"🔴","moat_trend":"↓","runway_post_y5":"🟡","asym_ratio":null,"ev5y_pct":29.0,"irr_base_pct":7.6,"max_dd_pct":-40.0,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":"3-of-3 AND 全數成立方重跑 DD：① US EP 有機成長連 2 季止穩且份額止跌；② Penumbra 整合無減損、槓桿回落；③ 證券集體訴訟/聯邦調查落地無重大裁罰或給付風險。任一未過即維持迴避。","price_at_dd":44.99,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BSX_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
