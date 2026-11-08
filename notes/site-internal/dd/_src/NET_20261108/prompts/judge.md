你是 stock-analyst **v20 判斷 agent**，標的 NET（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"NET","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NET_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NET_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":782.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M（YoY +39%；QoQ +12.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 cloudflare.net Q3 2026 press release"},"note":"未取得（新聞稿無共識；不填造）"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":17.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%（$137.1M；去年同期 15.3% / $85.9M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 cloudflare.net Q3 2026 press release"},"note":"未取得"},{"id":"f_kpi2_gaap_operating_income_lo","label":"GAAP operating income (loss) / margin","value":-8.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%（營業虧損 $67.9M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 cloudflare.net Q3 2026 press release"},"note":"未取得"},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":82.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M（占營收 10%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 cloudflare.net Q3 2026 press release"},"note":"未取得"},{"id":"f_kpi5_guidance_q4_fy2026","label":"Guidance: Q4 FY2026","value":"營收 $845.0–846.0M；Non-GAAP 營業利益 $156.0–157.0M；Non-GAAP EPS $0.43（約 379M 股）","period":"Q3 FY2026（公告於 2026-11-05）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（公告於 2026-11-05）","citation":"公司 IR 新聞稿 cloudflare.net Q3 2026 press release"},"note":"未取得"},{"id":"f_kpi6_guidance_fy2026","label":"Guidance: FY2026 全年","value":"營收 $2,963.0–2,964.0M；Non-GAAP 營業利益 $462.0–463.0M；Non-GAAP EPS $1.35（約 376M 股）","period":"Q3 FY2026（公告於 2026-11-05）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（公告於 2026-11-05）","citation":"公司 IR 新聞稿 cloudflare.net Q3 2026 press release"},"note":"FY1 共識 EPS 1.26（consensus_revision，財報前快照）；與指引 $1.35 不同口徑時須註明"},{"id":"f_kpi7_dollar_based_net_retenti","label":"Dollar-based net retention (NRR)","value":122,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"Q3 2026 財報電話會議逐字稿（CFO 備詞）"},"note":"不適用"},{"id":"f_kpi8_large_customers_100k","label":"Large customers（年付 >$100K）","value":5000,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"家（約；QoQ 淨增 308；YoY +25%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"Q3 2026 財報電話會議逐字稿"},"note":"不適用"},{"id":"f_kpi9_paying_customers","label":"Paying customers 新增","value":158000,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"家（單季淨增；付費客戶 YoY +110%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"Q3 2026 財報電話會議逐字稿"},"note":"不適用"},{"id":"f_kpi10_rpo","label":"RPO","value":2877,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M（QoQ +5%；YoY +34%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"Q3 2026 財報電話會議逐字稿；新聞稿載 cRPO YoY +37%"},"note":"未取得"},{"id":"f_kpi11_current_rpo_crpo_yoy","label":"Current RPO (cRPO) YoY","value":37,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%（約占總 RPO 65%，金額約 $1.87B 為推算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 cloudflare.net Q3 2026 press release"},"note":"未取得"},{"id":"f_kpi12_non_gaap_gross_margin","label":"Non-GAAP gross margin","value":72.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%（GAAP 71.2%，去年同期 74.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[12]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"逐字稿（non-GAAP）；新聞稿（GAAP）"},"note":"未取得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_net_gross_margin_pct","label":"NET 毛利率","value":72.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NET.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_net_operating_margin_pct","label":"NET 營業利益率","value":-8.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NET.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_net_fcf_margin_pct","label":"NET FCF 利潤率","value":12.53,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NET.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_zs_gross_margin_pct","label":"ZS 毛利率","value":76.8,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ZS.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_zs_operating_margin_pct","label":"ZS 營業利益率","value":-3.61,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ZS.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_zs_fcf_margin_pct","label":"ZS FCF 利潤率","value":23.24,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ZS.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_fsly_gross_margin_pct","label":"FSLY 毛利率","value":62.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FSLY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_fsly_operating_margin_pct","label":"FSLY 營業利益率","value":-8.85,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FSLY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_fsly_fcf_margin_pct","label":"FSLY FCF 利潤率","value":5.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FSLY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_akam_gross_margin_pct","label":"AKAM 毛利率","value":57.45,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AKAM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_akam_operating_margin_pct","label":"AKAM 營業利益率","value":11.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AKAM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_akam_fcf_margin_pct","label":"AKAM FCF 利潤率","value":14.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AKAM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_crwd_gross_margin_pct","label":"CRWD 毛利率","value":75.25,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRWD.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crwd_operating_margin_pct","label":"CRWD 營業利益率","value":-2.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRWD.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crwd_fcf_margin_pct","label":"CRWD FCF 利潤率","value":28.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRWD.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc","label":"SBC（含相關雇主薪資稅）占營收","value":22.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%（$174.1M ÷ $782.5M，由兩數換算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 cloudflare.net Q3 2026 press release（SBC 金額）"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":268.75,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":37.03,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":39.35,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.26 → 1.26）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.69 → 1.69）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.27 → 2.27）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.26,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":1.69,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":2.27,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 1.26 → 1.26（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":35.24,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":35.09,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":213.29,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 1.26，分子＝快照價 268.75","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-421.23,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 4707.46、現金 5128.69（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":358.39,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":95896.69,"period":"2026-11-08","unit":"USD m","basis":"市值 96317.92 ＋ 淨負債 -421.23","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":2965.33,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（23 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":3875.43,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（29 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":32.34,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 268.75 / W52 237.13 / W104 198.95 / W250 124.31 / W250 13週斜率 2.45%"},{"id":"f_ma_w52","label":"52 週均線","value":237.13,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":198.95,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":124.31,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.45,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 自述：與公有雲廠商在儲存／運算工作負載上競爭日增，Workers 定價可與公有雲競爭；並預期新進入者與大型電信／公有雲業者會增加競爭，風險含降價與失去市占。","source":"SEC EDGAR 10-K FY2025 Item 1 / 1A","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"In addition, we believe we are increasingly competing with public cloud vendors for storage and compute workloads as more third-party developers utilize our serverless platform.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：預期更多既有與新創業者進入雲端安全／效能市場，包含運用 AI 的產品，競爭加劇可能導致降價與失去市占。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"We expect competition to increase as other established and emerging companies and start-ups enter the markets for products and solutions for security, performance, and reliability, in particular with respect to cloud-based solutions","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"聚合媒體報導 Akamai 與 Anthropic 簽七年 $1.8B LLM 合約（未經 Akamai/Anthropic 官方核實）","source":"pulse.bot: Akamai Surges on Big LLM Deal as Cloudflare Dims","url":"https://www.pulse.bot/ma/news/akamai-surges-on-big-llm-deal-as-cloudflare-dims-272348af-a726-4b3b-9472-569b66ebbe05/","excerpt":null,"as_of":"2026-11-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K 風險因素：潛在競爭者（大型電信、公有雲）可能自行開發內部解決方案或透過合作進入市場；此為一般性競爭風險，未指名最大客戶導入第二供應商或自製。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"These companies could choose to enter the markets for products and solutions for security, performance, and reliability, including by acquiring existing companies, developing their own internal solutions, or establishing cooperative relationships with businesses","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 揭露 2023、2024、2025 年皆無單一客戶占營收超過 10%。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"No single customer accounted for more than 10% of our revenue in the years ended December 31, 2023, 2024, or 2025.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2025、2024 年底無客戶占應收帳款淨額 10% 以上，2023–2025 年無客戶占營收 10% 以上。","source":"SEC EDGAR 10-K FY2025 Item 8 Financial Statements","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"For the years ended December 31, 2025, 2024, and 2023, no customer accounted for more than 10% of the Company’s revenue. No customer represented 10% or more of accounts receivable, net as of December 31, 2025 and 2024.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"部分最大客戶採「pool of funds」承諾支出模式，不要求特定產品或每期支出金額，收入認列可能不即時反映新增/續約變動。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"our subscription agreements with certain of our largest customers are structured on a \"pool of funds\" model in which the customer commits to spend at least a specified amount on our products during the subscription period.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"國際市場占營收 2025 年 51%、2024 年 49%、2023 年 48%。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"International markets represented 51%, 49%, and 48% of our revenue in the years ended December 31, 2025, 2024, and 2023, respectively","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Cloudflare 2026 年 2 月初始指引營收 27.9–28.0 億美元，高於預期 27.4 億，歸因 AI 驅動需求","source":"The Star (Reuters/LSEG)","url":"https://www.thestar.com.my/tech/tech-news/2026/02/11/cloudflare-forecasts-annual-sales-above-estimates-as-ai-drives-cloud-demand","excerpt":null,"as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Cloudflare Q2 後上調 2026 營收指引中位數至約 28.7 億美元（約 +32%），股價漲逾 16%","source":"Invezz","url":"https://invezz.com/news/2026/08/07/cloudflare-stock-jumps-16-as-ai-demand-drives-higher-2026-revenue-forecast/","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q1 2026 營收年增 34% 至 6.398 億美元，同時宣布裁員 20%","source":"TIKR","url":"https://tikr.com/blog/cloudflare-q1-2026-34-revenue-growth-but-announces-20-workforce-reduction","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"IDC 預測全球邊緣運算支出 2028 年逼近 3,800 億美元","source":"Computer Weekly","url":"https://www.computerweekly.com/news/366620991/IDC-global-edge-computing-spending-to-approach-380bn-by-2028","excerpt":null,"as_of":"2025-01-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K FY2025 Item 3：公司目前不是任何預期會對業務、經營結果或財務狀況造成重大影響的法律程序之當事方（一手紀錄無反壟斷調查）。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"We are not presently a party to any legal proceeding that we believe is likely to have a material impact on our business, results of operations, or financial condition.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因素：收購可能面臨反壟斷、競爭與其他監管審查而限制完成交易；政府採購亦有 False Claims Act 等合規風險（一般性風險揭露，非具體調查）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"If we identify companies that we would like to buy, we may also face antitrust, competition, and other regulatory scrutiny that may limit our ability to complete such acquisitions.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋未見 DOJ/FTC/EU 針對 Cloudflare 的反壟斷調查；Cloudflare 在英國 CMA 是推動者（要求 Google 拆分搜尋與 AI 爬蟲），非被調查方。另有義大利 AGCOM 就防盜版封鎖命令處罰約 1,400 萬歐元（非反壟斷）。","source":"WebSearch 摘要彙整（broadbandbreakfast／techcrunch 2025-10-21／dig.watch）","url":"https://www.techcrunch.com/2025/10/21/cloudflare-ceo-matthew-prince-is-pushing-uk-regulator-to-unbundle-googles-search-and-ai-crawlers","excerpt":null,"as_of":"2025-10-21","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Cloudflare 向少數供應商採購網路與伺服器設備，10-K 風險因子列明關稅可能推高這些設備價格。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"Our reliance on these suppliers exposes us to risks, including reduced control over production costs, increased prices due to tariffs (such as the tariffs the United States and other countries recently implemented or threatened to implement)","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"MD&A 說明部分網路設備來自美國境外供應商，或來自再向境外採購零件的美國供應商，公司與供應商評估關稅影響並調整採購來源。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"We purchase a portion of the equipment that we use to operate our network from suppliers located outside the United States and we also purchase this equipment from United States suppliers that themselves purchase components from suppliers located outside the United States.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"BIS 於 2025-09-29 發布擴大 Entity List 適用範圍的「Affiliates rule」；該規則已於 2025-11-10 暫停一年，10-K 稱若實施將大幅提高 EAR 合規門檻。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"On September 29, 2025, the U.S. Department of Commerce’s Bureau of Industry and Security (BIS) released an interim final rule that expanded export control restrictions and licensing requirements under the EAR Entity List and Military End-User List","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2019 年自揭的 OFAC 制裁合規案件，截至 10-K 仍在 OFAC 審查中。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"The voluntary self-disclosure, which we may supplement as appropriate, remains under an ongoing review by OFAC.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Q2 2026 投資人簡報的前瞻聲明風險提及中東與烏克蘭衝突及其他地緣緊張可能使結果與預期不同；網路涵蓋 335+ 城市、125+ 國家","source":"Cloudflare Q2 2026 Investor Presentation","url":"https://www.cloudflare.net/files/doc_financials/2026/q2/Q2-2026-Cloudflare-Investor-Presentation.pdf","excerpt":"the impact of the conflicts in the Middle East and Ukraine and other areas of geopolitical tension around the world","as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K：預期伺服器供應鏈出現顯著零組件短缺（記憶體、SSD、CPU、硬碟），因產能轉向 AI 基礎設施；依賴少數零組件供應商，關稅可能使供應商漲價","source":"Cloudflare Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"We rely on a limited number of suppliers for several components of the equipment we use to operate our network and provide products to our customers. Our reliance on these suppliers exposes us to risks, including reduced control over production costs, increased prices due to tariffs (such as the tariffs the United States and other countries","as_of":"2026-02-20","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 revenue $782.5M, +39% YoY, cRPO +37% YoY; CEO called it fastest revenue growth in nearly four years","source":"Cloudflare Q3 2026 8-K exhibit 99.1 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001477333/000147733326000060/q326exhibit991.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Gartner 1Q26 infrastructure software overview: spend rising from $442B (2024) to nearly $788B by 2029; Oct 2026 forecast calls sector an AI-led growth cycle; no 2027 growth figure found","source":"Gartner Insights Abstract","url":"https://www.gartner.com/en/documents/8493145","excerpt":null,"as_of":"2026-10-09","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Competition from Akamai could lead to pricing pressure or market share pressure","source":"Investing.com SWOT analysis","url":"https://ca.investing.com/news/-4722264","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K 風險因素稱所處產業技術變動快、需持續創新；未見文件點名具體替代技術已取代其產品","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"The industry in which we compete is characterized by rapid technological change, including frequent introductions of new products and services, evolving industry standards, changing regulations, and the development of novel cyber attacks by hostile parties, as well as changing customer needs, requirements, and preferences.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Q3 2026 10-Q 風險因素：提供更低價/更有效率/更安全競品的新技術可能使其網路與現有產品較不具吸引力或過時","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001477333/000147733326000061/cloud-20260930.htm","excerpt":null,"as_of":"2026-11-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"部落格主張 Anthropic 託管 agent 執行環境可能把企業 agent 工作負載從 CDN 邊緣運算拉走（作者解讀）","source":"ipcarrier blogspot 2026-04-12","url":"https://ipcarrier.blogspot.com/2026/04/now-claude-managed-agents-threaten-edge.html","excerpt":"Now Claude Managed Agents Threaten Edge Networks Add edge networks such as Akamai, Fastly and Cloudflare to the list of enterprise software of service providers that might be disrupted or helped by growing use of language models and especially agents.","as_of":"2026-04-12","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 描述銷售為 Enterprise 方案直銷加通路夥伴（MSP、經銷、分銷、GSI），並以免費方案→隨用隨付→Enterprise 的漏斗獲客；未顯示通路結構性轉變。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"We sell our products under our Enterprise plans directly to customers through our global, technically-oriented inside and field sales teams, and indirectly through our ecosystem of channel partners that includes managed service providers, resellers, distributors, and global system integrators.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Cloudflare 於 2026-07-01 宣布 Pay Per Crawl 演進為 Pay Per Use（按使用付費的內容/代理存取市集）；為次級來源報導，細節待官方確認。","source":"pasqualepillitteri.it：Cloudflare Blocks AI Crawlers by Default: From Pay Per Crawl to Pay Per Use","url":"https://pasqualepillitteri.it/en/news/7205/cloudflare-ai-crawlers-pay-per-use","excerpt":"On 1 July 2026, Cloudflare said its crawler marketplace, Pay Per Crawl, is evolving into Pay Per Use.","as_of":"2026-07-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-06 公司給 Q3 指引 EPS $0.34、營收 $736–737M，高於當時共識（MarketBeat 比對：EPS 約 $0.26、營收 $722.4M）；全年 EPS 指引 $1.25–1.26 遠高於共識 $0.96。Benzinga 則列 Q3 共識約 $0.28／$737.1M，來源間不一致。","source":"MarketBeat: Cloudflare (NYSE:NET) issues Q3 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/cloudflare-nysenet-issues-q3-2026-earnings-guidance-2026-08-06/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 財報後公司上調全年 2026 指引：營收 $2.864–2.870B、調整後 EPS $1.25–1.26；Q2 營收 $696.1M、年增 36%；盤後漲逾 18%。5 月 Q1 時曾先上調至營收中點約 $2.81B、EPS $1.19–1.20（原 $1.11–1.12）。","source":"InsiderFinance / SiliconANGLE","url":"https://www.insiderfinance.io/news/cloudflare-q2-earnings-beat-guidance-raised","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價（截至 2026-06-10）：30 位分析師，22 買／6 持有／2 賣；共識目標價 $250，區間 $136–$305。其他聚合站未標日期：TipRanks 均價 $253.14（高 318／低 135）、Benzinga 均價 $283–291，來源間分歧大；未找到 11 月最新共識。","source":"StockAlarm NET analysts","url":"https://pro.stockalarm.io/quote/NET/analysts","excerpt":null,"as_of":"2026-06-10","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Scotiabank 2026-05-14 維持 Sector Perform、目標價 $225，上調 FY2026 EPS 至 -0.04（原 -0.12）；6 月 11 日再上調 FY2027 EPS 至 0.40（原 0.17）。Cantor 維持中立、目標價 $230（原 $224）。","source":"MarketBeat: Scotiabank estimates Cloudflare's FY2027 earnings","url":"https://www.marketbeat.com/instant-alerts/scotiabank-estimates-cloudflares-fy2027-earnings-nysenet-2026-06-15/","excerpt":null,"as_of":"2026-06-15","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"單一來源稱 2026-11-05 Q3 實績調整後 EPS $0.38（共識 $0.34）、營收 $783M（共識 $738M），未有第二來源確認，待核實。","source":"247wallst: Cloudflare NET Q3 2026: 39% Revenue Growth and a Guidance Lift","url":"https://247wallst.com/cards/cloudflare-q3-2026-earnings-net-01m6psg0byw1kqkd514aq3zgkb","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-05-07 8-K Item 2.05：公司宣布重整計畫，預計裁減約 20% 員工。","source":"SEC EDGAR 8-K 2026-05-07 Item 2.05","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000035/cloud-20260507.htm","excerpt":"On May 7, 2026, the Company announced a plan (the “Plan”) designed to further accelerate its evolution to an agentic AI-first operating model. As part of the Plan, the Company expects to reduce its current workforce by approximately 20%.","as_of":"2026-05-07","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-08-13 發行 25 億美元 0% 可轉換優先票據（2031 到期），初始轉換價約 496.94 美元。","source":"SEC EDGAR 8-K 2026-08-13 Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1477333/000095010326012340/dp251721_8k.htm","excerpt":"On August 13, 2026, Cloudflare, Inc. (the “Company”) issued $2.50 billion aggregate principal amount of 0% Convertible Senior Notes due 2031 (the “Notes”)","as_of":"2026-08-13","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：公司目前不是任何預期會有重大影響之法律程序的當事方。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"We are not presently a party to any legal proceeding that we believe is likely to have a material impact on our business, results of operations, or financial condition.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-10-08 以約 2,650 萬美元現金收購 Deno Land Inc.（10-Q 期後事項）；另有 2026-01 收購 Astro 團隊與 Human Native、2026-06 收購 VoidZero（聚合站報導，未核一手）。","source":"搜尋摘要：Cloudflare 10-Q (2026-09-30) subsequent events；BusinessWire Astro 2026-01-16","url":"https://www.sec.gov/Archives/edgar/data/0001477333/000147733326000061/cloud-20260930.htm","excerpt":"On October 8, 2026, the Company acquired Deno Land Inc. which has developed an open-source JavaScript and TypeScript runtime and related developer infrastructure, for approximately $ 26.5million in cash.","as_of":"2026-10-08","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K 稱目前不是預期有重大影響之訴訟當事方；搜尋僅見原告律所調查公告（Schall，2026-05-08），未見已提起之集體訴訟、案號或原告截止日。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm","excerpt":"We are not presently a party to any legal proceeding that we believe is likely to have a material impact on our business, results of operations, or financial condition.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 8 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"NET","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.58,"operating_margin_pct":-8.11,"fcf_margin_pct":12.53,"rd_intensity_pct":22.82},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NET","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"ZS","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":76.8,"operating_margin_pct":-3.61,"fcf_margin_pct":23.24,"rd_intensity_pct":26.95},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ZS","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"FSLY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":62.64,"operating_margin_pct":-8.85,"fcf_margin_pct":5.63,"rd_intensity_pct":23.42},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FSLY","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"AKAM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.45,"operating_margin_pct":11.92,"fcf_margin_pct":14.57,"rd_intensity_pct":12.83},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AKAM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"CRWD","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":75.25,"operating_margin_pct":-2.21,"fcf_margin_pct":28.22,"rd_intensity_pct":28.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRWD","as_of":"TTM ending 2026-07-31（4季加總）"}}],"subject":"NET"},"financial_history":{"ticker":"NET","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":975241000.0,"revenue_yoy_pct":null,"gross_margin_pct":76.15,"operating_margin_pct":-20.63,"net_income":-193381000.0,"diluted_eps":-0.59,"free_cash_flow":-39769000.0,"fcf_margin_pct":-4.08,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":1296745000.0,"revenue_yoy_pct":32.97,"gross_margin_pct":76.32,"operating_margin_pct":-14.3,"net_income":-183949000.0,"diluted_eps":-0.55,"free_cash_flow":119464000.0,"fcf_margin_pct":9.21,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":1669626000.0,"revenue_yoy_pct":28.76,"gross_margin_pct":77.32,"operating_margin_pct":-9.27,"net_income":-78800000.0,"diluted_eps":-0.23,"free_cash_flow":166915000.0,"fcf_margin_pct":10.0,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":2167937000.0,"revenue_yoy_pct":29.85,"gross_margin_pct":74.51,"operating_margin_pct":-9.56,"net_income":-102267000.0,"diluted_eps":-0.29,"free_cash_flow":260562000.0,"fcf_margin_pct":12.02,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/NET/NET_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**Cloudflare, Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Welcome, ladies and gentlemen. Thank you for joining us, and welcome to Cloudflare's Third Quarter 2026 Earnings Conference Call. [Operator Instructions] I will now hand the conference over to Phil Winslow. Phil, please go ahead.

**Philip Winslow** (Executives):
Thank you for joining us today to discuss Cloudflare's financial results for the third quarter of 2026. With me on the call, we have Matthew Prince, Co-Founder and CEO; Michelle Zatlyn, Co-Founder and President; and Thomas Seifert, CFO. By now, everyone should have access to our earnings announcement. This announcement as well as our supplemental financial information may be found on our Investor Relations website.
As a reminder, we will be making forward-looking statements during today's discussion, including, but not limited to, our customers, vendors and partners, operations and future financial performance, our anticipated product launches and the timing and market potential of those products, our anticipated future financial and operating performance and our expectations regarding future macroeconomic conditions. These statements and other comments are not guarantees of future performance and are subject to risks and uncertainty, much of which is beyond our control. Our actual results may differ significantly from those projected or suggested in any of our forward-looking statements.
These forward-looking statements apply as of today, and you should not rely on them as representing our views in the future. We undertake no obligation to update these statements after this call. For a more complete discussion of the risks and uncertainties that could impact our future operating results and financial condition, please see our filings with the SEC as well as in today's earnings press release.
Unless otherwise noted, all financial numbers we talk about today, other than revenue, will be on an adjusted non-GAAP basis. You may find a reconciliation of GAAP to non-GAAP financial measures that are included in our earnings release on our Investor Relations website. For historical periods, a GAAP to non-GAAP reconciliation can be found in the supplemental financial information referenced a few moments ago. We would also like to inform you that we will be participating in RBC Capital Markets Global Technology, Internet, Media and Telecommunications Conference on November 18 and Barclays Global Technology Conference on December 9. Now with that, I'd like to turn the call over to Matthew.

**Matthew Prince** (Executives):
Thank you, Phil. There's no other way to say this. By nearly every metric, we had our best quarter ever. We again accelerated growth and became more profitable at the same time, delivering our fastest revenue growth in nearly 4 years and achieving our highest operating margin in the history of the company. We crossed $3 billion in annualized revenue, generating $782 million in the third quarter. That's up 39% year-over-year. We now have more than 5,000 customers paying us more than $100,000 per year, a 25% increase year-over-year. Our dollar-based net retention was 122%, up 2% quarter-over-quarter and up 3% year-over-year. Our gross margin was 72.4%. We delivered an operating profit of $137.1 million, representing an operating margin of 17.5% and we generated free cash flow of $82.1 million during the quarter, again exceeding expectations.
But that's just the start of what was a monster quarter. The strong momentum we've been seeing in our business continued to accelerate in the third quarter. It's like the engine was firing on all cylinders, and we found another gear. Some highlights. Sales productivity reached a new record in the third quarter and increased year-over-year for the 11th consecutive quarter. In Q3, we delivered our highest ACV growth ever and highest quota attainment in more than 5 years. 
Bookings from new customers grew faster still, beating last quarter's 5-year high. We added more than 158,000 paying customers this quarter. That's 110% growth in paying customers year-over-year and nearly double the previous record of more than 80,000 we added in Q2. We also achieved record year-over-year net additions across all our large customer annualized revenue cohorts from $100,000 to $500,000 to $1 million to $5 million. Across every one of those, we grew at a new record pace. And as we already announced at our customer conference a few weeks ago, we passed 10 million active developers on our platform, more than doubling the number we had at the start of 2026.
As I said, we seem to have found a new gear. These results speak for themselves and are the cumulative effect of our relentless focus on innovation, combined with disciplined execution. Much of that execution improvement has come from the transformation of our go-to-market engine to match our already world-class product and engineering teams. Mark Anderson deserves a huge amount of credit for shepherding us through that transition. 
With his well-earned retirement coming at the end of this year, we wanted to find a successor with a proven track record of scaling global sales organizations to turbocharge our already robust go-to-market momentum. I'm incredibly excited to welcome Christian Smith to Cloudflare as our new President of Revenue. No one will ever replace Mark, but Christian's skill set and experience building and enabling world-class go-to-market organizations match perfectly with the current stage of Cloudflare to further accelerate our next wave of growth at scale. I wanted to invite Christian to the call to say a few words. Christian?

**Christian Smith** (Executives):
Thank you, Matthew. I am thrilled to join the Cloudflare team. Look, Cloudflare has built the sheer scale of its world-class network, the company's unparalleled product innovation and the clear vision for the future of the Internet, it is truly unique. But what gets me most excited is the massive generational opportunity that's still in front of us to go and capture. I've spent my entire career scaling enterprise go-to-market engines with operational rigor, building world-class partner ecosystems and driving intense customer focus. Mark Anderson has built an incredible foundation over the past 3 years at Cloudflare. And my immediate priorities are to double down on go-to-market execution, further accelerate our enterprise momentum and ensure our customers get even more rapid compounding time to value from our platform. With the rise of the agentic Internet, Cloudflare was built for this moment. Now it's about execution and scale, and I'm ready to go get to work with the team.

**Matthew Prince** (Executives):
Thanks, Christian. Under your leadership, I know we will continue to deliver on our vision that has never just been about selling products, but rather about helping solve some of our customers' toughest challenges as only Cloudflare can. And to ensure the smooth transition, Mark Anderson has agreed to stay on as an adviser for at least the next year. I know he'll always bleed orange and be there to help close a customer if we need him.
That seems like a good segue to talk about some of Mark's team's big wins in the quarter. A rapidly growing AI company expanded their relationship with Cloudflare, signing a 1-year, $11 million pool of funds contract for our Workers Developer Platform. Tens of millions of AI-generated applications have been created on its platform and legacy hyperscalers would charge this customer for massive amounts of idle compute. With Cloudflare's Dynamic Workers, apps start in milliseconds and the customer pays only for the compute they actually use. One of their lead engineers said, "Without Cloudflare's Dynamic Workers, we wouldn't be able to build what we want to build." When the cost of creating software drops to near 0, the number of applications explodes and the most sophisticated builders are choosing to run them on Cloudflare.
A Fortune 100 cloud infrastructure provider expanded their relationship with us, signing a 13-month, $15.5 million contract for Magic Transit. As the customer aggressively scales its global footprint for AI, their legacy DDoS hardware applications simply could not keep up, failing to scale cost effectively and missing low-level attacks that were quietly draining capacity. During the evaluation, our global network stopped attacks that their appliances simply could not, and we fully displaced the incumbent. As one of their technical leaders noted, Cloudflare's threat mitigation is one of our superpowers. When the world's biggest cloud operators build next-generation AI infrastructure, they trust Cloudflare to protect it.
A cabinet level U.S. federal department signed a 5-year, $10.3 million contract for our SASE portfolio. With their legacy VPN reaching end of life, the agency needed a modern replacement that could scale on a deadline it couldn't miss. They chose Cloudflare over a first-generation Zero Trust provider for our speed, global scale and simplicity. This win positions Cloudflare as the backbone of their new cybersecurity posture and underscores that the federal government is ready to leave legacy hardware behind and that unified platforms like Cloudflare will win.
A rapidly growing multinational neobank and fintech company expanded their relationship with Cloudflare, signing a 3-year pool of funds agreement with an average annual contract value of more than $3 million. Their initial use cases focus on our SASE portfolio. The latency that employees experienced with the incumbent first-generation Zero Trust vendor was so bad that many simply turned it off, leaving the business exposed. They moved their entire workforce to Cloudflare in a single quarter. Since then, performance tickets per user have dropped 74%. It turns out the most secure Zero Trust platform inherently is the one people actually leave on. And from this customer's feedback, it seems Cloudflare may be the only vendor that has that critical feature.
A fast-growing technology company expanded their relationship with Cloudflare, signing a 39-month, $9.5 million pool of funds contract for application services and our Workers Developer Platform. For this customer, latency directly impacts their bottom line. As they prepare to expand internationally, they chose Cloudflare over a major hyperscaler for the speed and reliability of our global network. As their champion put it, there is no international expansion for them without Cloudflare's global network. When milliseconds impact users and in turn financials, the network is the business and Cloudflare runs the best network.
A leading global consulting firm expanded their relationship with Cloudflare, signing a 3-year pool of funds contract for more than $7 million for Zero Trust application services and our Workers Developer Platform. After their legacy Zero Trust provider failed to manage the complexity of securing over 10,000 custom client applications, Cloudflare's effortless deployment drove rapid company-wide adoption. The firm is now aggressively consolidating vendors onto our unified platform, including migrating their main web properties from a long-standing incumbent by the end of next year. Drawn to our forward-looking AI and developer road map that they want to standardize on, the customer is already exploring Workers AI and Cloudflare OS to build next-generation applications and agents.
A leading European media company expanded their relationship with Cloudflare, signing a 5-year, $8.1 million contract for application services and our Workers Developer Platform. Replacing a 17-year deployment with a legacy CDN vendor, they chose Cloudflare because our best-in-class bot management reliably identifies modern AI crawlers, giving this customer the control they need to protect their intellectual property, but also creating a direct on-ramp for pay-per-crawl and pay-per-use monetization. This win is a clear blueprint for how the world's largest media companies will protect and monetize their content and innovate in the agentic AI era.
I could go on and on with more wins, but we'd be here all day. To give you a sense, based on third-party data between July 1 and today, we added approximately 5% of the entire web to Cloudflare. That's wild. It's more than the total market of all our reverse proxy competitors combined added to our network in a bit over a quarter. We've been growing throughout our entire history, but recently something changed. The rate of growth inflected in October of 2025, then accelerated again in July of 2026 and then again at the beginning of this October.
So what's going on? I think it's the convergence of 2 things. First, we have built the development platform for the future of the AI-powered Internet. And second, the security landscape is getting so scary that the best viable strategy regardless of who you are is to ensure you have Cloudflare protecting you.
To the first, hyperscalers and even neoclouds were built around container technology. It was a significant improvement over bare metal or even virtual machines. Containers allow these last-generation clouds to scale during the explosion of mobile devices that defined their heyday. But now we're in the era of AI and agents. I predicted last quarter that within 5 years, agents would outnumber humans online 1,000:1. A quarter later, I'll take the under on the timing of that bet based on everything we're seeing today. The container-based architecture of the hyperscalers and neoclouds just can't keep up in a cost-effective way with the new agentic paradigms of today. 
Cloudflare's approach is different. We have based it on what we call isolates, not containers, which initially let us scale geographically to span the globe, but increasingly is allowing us to scale densely with a level of efficiency no hyperscaler or neocloud can match. The smartest developers, whether they're frontier model companies or legacy enterprises, see that the world is changing and that they need a new type of cloud in order to keep up. In other words, Cloudflare isn't a neocloud. We're also not, as some of you have called us, the fourth public cloud. We're something different. We're the first agentic cloud and developers are flocking to us to build the agentic AI future.
The second driver of our growth inflection has even broader applicability across every business. It may seem like the sky is falling with a number of new security vulnerabilities that have been reported over the last few weeks. I wish I could tell you we were through the worst, but we're not. Because of the vast percentage of the Internet that already sits behind Cloudflare, we are among the first to receive quiet disclosure of new vulnerabilities. We've partnered with nearly every major frontier AI lab and security company searching for flaws in existing software. When they find something, they notify us through a trusted reporter process, and we quietly put protection in place for all our customers, whether they pay us or not. We believe protecting everyone is important to fulfilling our mission of helping build a better Internet, and living up to that mission has ensured that we are trusted and nearly always get early warning of the worst problems researchers discover.
The bugs you read about over the last few weeks and the ones I suspect you will read about over the next few years were less impactful because Cloudflare has the Internet's back. That, of course, creates a virtuous cycle. We know what bugs are coming. We protect our customers before the bugs are publicly disclosed. Companies increasingly know that if they are behind us, they are more likely to be protected whatever the future brings. And so even legacy organizations that aren't pushing the bleeding edge of AI are signing up for Cloudflare at an accelerating rate.
And of course, as more of the Internet uses Cloudflare, it enables new opportunities. I'm proud to announce that we recorded in Q3 our first revenue for what we've called Act IV products, those where we're helping invent the new business model of the Internet. And I expect we'll talk a lot more about that in the quarters to come.
To sum up, our third quarter financial and operational results highlight the accelerating demand for Cloudflare solutions, our commitment to both innovation and operational excellence and the inherent leverage in our business model. I could not be more proud of our team. But as Michelle likes to say, we're just getting started. The opportunities ahead of us are more clear and massive than ever, and it's turning out Cloudflare was built for this moment. With that, I'll turn it over to Thomas. Thomas, take it away.

**Thomas Seifert** (Executives):
Thank you, Matthew, and thank you to everyone for joining us. I want to take a moment to also extend my personal thanks to Mark Anderson for his leadership of our go-to-market transformation over the last 3 years and congratulate him on a well-deserved retirement. I'm also incredibly excited to welcome Christian Smith to our Cloudflare team. His proven track record of scaling global sales organizations and go-to-market operations is a perfect fit for Cloudflare to further accelerate our next phase of growth at scale.
Turning to the results. We delivered an outstanding third quarter. In fact, Q3 was our best quarter as a public company to date. The strength we again drove across the major metrics we track demonstrated not only the robust demand for Cloudflare's products, but also the operational leverage inherent in our business model. Total revenue for the third quarter increased 39% year-over-year to $782.5 million, driven in particular by another quarter of rapid growth in our Workers Developer Platform and agentic workloads across our network, continued momentum with our largest customer cohorts and robust go-to-market execution. From a geographic perspective, the U.S. represented 52% of revenue and increased 44% year-over-year. EMEA represented 26% of revenue and increased 32% year-over-year. APAC represented 14% of revenue and increased 32% year-over-year.
Turning to our customer metrics. We ended the quarter with approximately 5,000 large customers. We added 308 large customers in the quarter and nearly 1,000 year-over-year, the most we have ever added both in a single quarter and in a single year. In fact, as Matthew mentioned, every one of our large customer cohorts added a record number of net new customers year-over-year in the third quarter. The higher you go among these cohorts based on the amount of spending committed to Cloudflare, the faster revenue is growing year-over-year. 
In other words, the bigger the size of the customer's annual spend with us, the faster they are growing with Cloudflare. Of particular note, we added almost as many $5 million-plus customers in the first 3 quarters of 2026 as we had $5 million-plus customers in total at the end of just last year. Revenue contribution from large customers was 75% of revenue during the quarter, up from 73% in the third quarter last year. The significant expansion with our large customers drove an acceleration in our dollar-based net retention rate to 122% in the third quarter, up from 120% last quarter and up from 119% in the same quarter last year.
Moving to gross margin. Third quarter gross margin was 72.4%, representing a decrease of 70 basis points sequentially and 290 basis points year-over-year and within our target long-term range of 70% to 77%. Our Workers Developer Platform delivered another quarter of exceptional growth, and we expect the unit economic margin of our developer products to continue to increase as evidenced by the strong operating margin we generated this quarter, which is a good segue to operating expenses.
Third quarter operating expenses as a percentage of revenue decreased by 510 basis points year-over-year to 55%. Our total headcount ended the quarter at approximately 4,700. Sales and marketing expenses were $270.2 million for the quarter. Sales and marketing as a percentage of revenue decreased to 35% from 36% in the same quarter last year. Research and development expenses were $101.7 million in the quarter. R&D as a percentage of revenue decreased to 13% from 15% in the same quarter last year. 
General and administrative expenses were $57.5 million for the quarter. G&A as a percentage of revenue decreased to 7% from 10% in the same quarter last year. Operating income was $137.1 million, an increase of 60% year-over-year compared to $85.9 million in the same period last year. Third quarter operating margin was 17.5%, an increase of 370 basis points sequentially and an increase of 220 basis points year-over-year.
Turning to net income and the balance sheet. Our net income in the quarter was $143.7 million or a diluted net income per share of $0.38. Free cash flow was $82.1 million in the quarter or 10% of revenue compared to $75 million or 13% of revenue in the same period last year. We ended the third quarter with $5.1 billion in cash, cash equivalents and available-for-sale securities. During the quarter, we issued $2.5 billion of convertible senior notes and repaid $1.3 billion of convertible senior notes. 
Network CapEx represented 15% of revenue in the third quarter. As a reminder, there can be some variability in this metric quarter-to-quarter, and we continue to expect network CapEx to be 14% to 15% of revenue for full year 2026. Remaining performance obligations, or RPO, came in at $2.877 billion, representing an increase of 5% sequentially and 34% year-over-year. Current RPO or 65% of total RPO improved 37% year-over-year.
Moving to guidance for the fourth quarter and full year 2026. For the fourth quarter, we expect revenue in the range of $845 million to $846 million, representing an increase of 38% year-over-year. We expect operating income in the range of $156 million to $157 million. We expect an effective tax rate of 20%. We expect diluted net income per share of $0.43, assuming approximately 379 million shares outstanding. We also expect to achieve GAAP profitability in the fourth quarter, significantly earlier as compared to our outlook from this year's Investor Day to reach this milestone at the latest by 2028.
For the full year 2026, we expect revenue in the range of $2.963 billion to $2.964 billion, representing an increase of 37% year-over-year. We expect operating income for the full year in the range of $462 million to $463 million. We expect an effective tax rate of 20%. We expect diluted net income per share over that period to be $1.35. We expect approximately 376 million shares outstanding.
In closing, we are consistently proving that scale, rapid innovation, profitability and growth are not trade-offs, but rather compound multipliers that provide us with meaningful competitive advantages. That is the winning formula Cloudflare continues to execute against to create significant value for both our shareholders and our customers. With our network and our developer platform at the core of the transition to the agentic Internet, we intend to capitalize on this generational opportunity with a continued focus on disciplined capital allocation, rigorous operational execution and durable efficient growth. And with that, operator, please poll for questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Matt Hedberg with RBC Capital Markets.

**Matthew Hedberg** (Analysts):
Just incredible results all around. And Christian, congrats on the new role. Excited to work with you again. I'm going to start, Matthew. You spent a lot of time talking about agents going 1,000x. And now I think you're taking the under on 5 years, which is great to hear. When we see things like news and all these consumer AI agents, with that as the sort of the paradigm in the lens, what does that mean just for the Internet as a whole when we get into that era? And specifically on Act IV, it's great to see you're starting to monetize that. But how does that start to really kick in as we move towards that paradigm?

**Matthew Prince** (Executives):
Yes. First of all, thanks, Matt. Really appreciate it and really proud of the team and also super excited to have Christian on board. As for me, I mean, first of all, if you haven't played with it yet, I mean, it's super cool as are a number of the other agents that are out there. And in the case of Muse, I mean, Meta is a customer, and it's been incredibly fun to watch them and help them scale that product and just see the explosive growth that we're seeing. So we're benefiting as that product grows directly.
I think the second bit though is, I think, more to your question, which is we're in a really interesting position because the people who are building the agents are often building them on Cloudflare. And then the things that the agents want to get to are also on Cloudflare. And so we've had examples over the last several months in the case of Meta, in the case of Google, where at times, there's been places where what they have been doing hasn't aligned exactly with what the content creators, publishers, application developers, financial services organizations, e-commerce companies, what they want to do. And Cloudflare is finding ourselves over and over and over again in the center of those questions and acting almost as a mediator between the 2 sides.
And in the process of doing that, I think what's really powerful is we're getting to set the rules of the road for what the agentic Internet is going to look like. And the reality is that if agents are going to be 1,000x human traffic online, that's going to require more bandwidth. That's going to require more servers. That's going to require more things to actually power it and someone has to pay for it. It can't be a free ride for all the agents that are out there. 
And what I'm encouraged by and what we're already seeing in terms of Act IV revenue is that the agentic companies get that they have to compensate the creators and the banks and everyone else who's providing this information in order to be able to continue to access it. And so I think we are at the cusp of figuring out what that next generation business model of the Internet is going to look like. And because of the fact that we are helping the companies that are building the agents and because of the fact that so much of the rest of the Internet sits behind us, Cloudflare is the company that's going to define what that looks like.

**Matthew Hedberg** (Analysts):
That's great. And then maybe, Thomas, just as a quick follow-up. You beat Q3 by more than 6%, and I think that was I think higher than last quarter's record beat. And now -- you grew 39%, you're guiding to 38%, so very little decel. I guess from your perspective, what are the most important drivers, not only to the quarter, but the guide as we sort of like look at the exit rate this year?

**Thomas Seifert** (Executives):
Yes. Well, we always guide to what we see. And you heard in both Matthew and my script that the demand is driven by a highly diversified momentum. The developer count, the traffic on the network, 160,000 net new customers, the largest add in every cohort we -- we count from a revenue perspective. No concentration, customers in financial verticals, government and across the globe. So we see a broad base for this momentum, and we are guiding to what we see, and this is reflected, I think, in the strong beat and raise you see for the fourth -- from the third quarter into the fourth quarter.

**Operator** (Operator):
Your next question comes from the line of Gabriela Borges with Goldman Sachs.

**Gabriela Borges** (Analysts):
Matthew, I want to stay on your point of a next-generation business model for the Internet. Maybe give us a little bit of a sense for time line on when you think that Act IV can start to be monetized in real dollar amounts and some of the key levers that could perhaps make that time line take longer or perhaps pull in relative to whatever your base case is?

**Matthew Prince** (Executives):
Yes, Gabriela, again, I'm extremely excited for this. And I think we've got to figure it out. A way of thinking of it is I'm sitting in Manhattan. And if I ask my agent, where am I going to go for dinner tonight after I'm done with earnings calls and callbacks. It might go and scour -- scour the Internet and look at 1,000 different restaurants' websites, pull down 1,000 different menus. And then I might choose to only go to one of those. The problem is that 999 of those restaurants have now had a cost that's just been applied to them, but they're not getting any benefit. And that was always true of the Internet, but the scale was different. It was, a human might look at 2 or 3 things. But in this case, the scale is so high that we're going to have to figure out some additional way to pay for it.
And so I think the ways of doing that are twofold. So one where we're already recognizing revenue and -- recognizing significant amounts of revenue is how do we make that more efficient. So we talked last quarter about how we partnered with OpenAI to make sure that as they search the Internet, they didn't do it in the kind of dumb way of just crawling everything all the time over and over again. But instead that Cloudflare could actually give them hints when a page had changed, when a menu price had updated, when anything had happened, then they could get the freshest data and they could actually crawl it. 
That helps OpenAI save money, and that actually helps the Cloudflare customers get the freshest data to them and make sure that it doesn't waste a ton of resources. And so I think that's a clear way where we're already seeing that, and that's helped -- OpenAI is paying for that and a lot of other companies in the space, I think you'll see do that as well.
Beyond that, though, I think that we're going to see some version of micro payments that exist where small payments get made when an agent comes. And I think it will be in exchange for the more that an agent is willing to tell you about why it's there, the more that you may be willing to charge it less to access the page. So if you imagine that an agent comes to a travel site and says, "Hey, I am looking for a vacation for my user and his or her family, it's family of 4, they want to go to Hawaii, what do you have for me?" 
That actually then might be something where you let the agent on for free, but it opens up all kinds of opportunities for advertising. And again, I think Cloudflare is in a perfect position to help bring both of those things together, both the agent and the places that might have whatever the agent is looking for. And so like that is coming. I don't know exactly how long it will be before it turns into major sources of revenue. But if you look out in the more distant horizon, if you look 10 years out, I would imagine that this becomes the largest part of Cloudflare's business.

**Gabriela Borges** (Analysts):
I appreciate the color. And Thomas, the follow-up is for you on pool of funds revenue. And there are 2 dynamics that I think you've talked about happening at the same time. The first is more of your business is shifting towards consumption revenue. And the second is that it sounds like customers are burning through their pool of funds contracts faster than what the original base case might have been. And so talk to us about how that informs your forecasting going forward? And any observations you can share with us on the pool of funds piece of the business in particular?

**Thomas Seifert** (Executives):
Yes. We saw continued strength in our variable revenue. It was the primary contributor to the upside. And the surprising or positive part of that was it was driven across a lot of customers either joining pool of funds or, as you said, burning to their pool of funds commitments faster and therefore, have to renew earlier and as part of the renewal process, sign up to even bigger pool of funds concepts. Because it has been driven by a long tail of customers, this, of course, influences how we build guidance for the fourth quarter that it was not a concentrated event, but a long tail of events across many customers and is part of the reason why we guided to what we guided.

**Operator** (Operator):
Your next question comes from the line of Ryan MacWilliams with Wells Fargo.

**Ryan MacWilliams** (Analysts):
So the contribution from net new customers over the last year seem to be growing strongly for Cloudflare. How are you seeing new AI native customers ramp across your acts compared to past cohorts? And are AI native driving any stronger growth in any act for the third quarter?

**Matthew Prince** (Executives):
Yes. Thanks, Ryan. I would say that we're seeing real strength across just about every different vertical that's out there. And so yes, we're seeing AI growth, but by no means would I say that this is really concentrated around AI in particular. We're seeing strong growth around financial services, government, manufacturing, health care, e-commerce across the board, that's coming on board. And it is new customers. 
And so as I talked about in the prepared remarks, I think one of the biggest drivers is the fact that it's sort of a secondary effect of AI, which is AI is finding more and more security flaws that are out there. Just last week and the week before, we had 6 of the worst Internet security bugs of all time announced over the course of fewer than 14 days. And we're not done. We have already gotten disclosures of many, many, many more extremely scary bugs, which researchers have found, have quietly disclosed to us, and we have protected our customers from.
And so at some level, I guess that's AI driving this because AI is helping find these bugs. But what else is happening is the small bank in Middle America that's like how in the world do I stay in front of all of this tsunami of threats, which is coming is getting advice from their peers, from government officials. I mean it was discussed literally in the White House the other day where a bunch of AI leaders got together with the White House officials and asked like -- and the White House was like how are we going to make sure that everyone is protected against these vulnerabilities? 
And the answer came back, Cloudflare because we sit in front of so much of the Internet and we are such a responsible player protecting the Internet. I think that's what's driving a huge amount of our growth. And so sure, AI companies are growing and they're growing across all of our different sectors. But across the board, this is really a broad-based win, not one which is entirely focused on just a small number of AI companies.

**Ryan MacWilliams** (Analysts):
Great to hear. And then love to hear at a high level how your CDN customers are evaluating significantly more of their web traffic becoming agent-based or coming from agents? Like are they happy to get more of that traffic? Or are they working with Cloudflare to make sure they receive and then pay for like the right traffic coming in?

**Matthew Prince** (Executives):
Yes. I think the answer depends on the customer. Some customers see agents as wonderful and they want to have them as many of them come to them as possible. Others see them as a bane to their business and want to keep them away. And we need to be able to serve both of those needs. And so for those customers that want more agentic traffic, we're helping them with modern we have -- there are different terms for it, but sort of the new version of SEO, sort of how do you optimize to get as much agentic traffic as possible? How do you make sure that it's being served in the most efficient way possible. And we're making that as easy as possible for them.
On the other hand, customers that want to keep those agents away that see them as a threat, then we're blocking that and then they're not getting charged for that traffic. And I think one of the things that's different from us than -- I mean, we've never been a CDN, like that's -- the fact that we do caching is only because we were afraid that our security services would slow things down and caching is an obvious computer science way of dealing with that. But we've really never been focused on charging for CDN traffic in any meaningful way. 
It's not a big driver of our business. And so when the traffic goes up or the traffic goes down, I think that more and more customers are flocking to Cloudflare because unlike some of the pure CDN players that are out there where their bills are going up, but they're not seeing the benefit, we're able to give them real control over what customers come to them and not charge them for what, frankly, I don't think they should be charged for in the beginning.

**Operator** (Operator):
Your next question comes from the line of Saket Kalia with Barclays.

**Saket Kalia** (Analysts):
Congrats on another quarter of acceleration. Absolutely. Matthew, maybe for you. There's clearly a lot of questions out there about what happens if data center construction slows. And I want to touch on the comparison that you made in your prepared remarks between container-based clouds versus Cloudflare's Isolate architecture. Now a lot can happen in terms of data center construction in the future. But hypothetically, if it were to slow, it feels like it could make your agentic cloud more valuable. But I'm curious how you think about that scenario and how it could impact Cloudflare's business, if at all?

**Matthew Prince** (Executives):
Sure. So it's -- we've gotten approached over and over again to say, would we -- would we do something like what the neoclouds are doing? And I think that what our answer has always been is we're an engineering company. We're not a financial engineering company. And so we're focused on how we can actually deliver real operational excellence and get real advantages for every CapEx dollar that we spend in order to deliver more benefit. And so we've watched a bunch of really dumb deals get done. And obviously, the market is digesting those right now. Those just aren't the sorts of deals that we would ever do.
And I think as the market gets more rational and as we actually figure out, okay, you can't sell $1 for $0.50 and be in business over the long term. What will happen is people will focus instead on where can we get more value, where can we drive more efficiency. And it turns out that we're the platform that has built that. As I said in the prepared remarks, the Isolates technology allowed us to distribute our systems globally and do that in an incredibly efficient way. 
But what we're increasingly finding is in those places where we need more density, where agents are talking to agents and they might be in 2 data centers right next to each other, that density also benefits from that same isolate architecture. And so again, my crystal ball isn't perfect, but your prediction that -- as some of the financial engineering that's driven this growth goes away, I think it will focus us more on who are the companies that have real operational excellence can deliver and have real engineering differentiation and a diversified business model. And I think that's exactly what Cloudflare has.

**Saket Kalia** (Analysts):
Makes a ton of sense. Thomas, maybe for my follow-up for you. Great to see the dollar-based net retention continue to improve. I think we're back at levels that we haven't seen in almost 4 years. So congrats. Can you just maybe dig into where the cross-sell is particularly breaking out in terms of which acts or customer segments? And could that net retention continue to improve looking forward?

**Thomas Seifert** (Executives):
Starting with your last part first. Yes, it can. We have higher ambitions when it comes to NRR than what we're currently achieving. And I think the combination of pool of funds, the largest customers growing the fastest and the friction that these concepts -- the pool of funds contracts take out of the expansion process are driving that. Where do we see that? We see that across the portfolio currently, security is playing a heavier and heavier role just following the remarks that Matthew made in his prepared statement, but also now in the Q&A session. 
So it's a broad-based expansion, especially in the large customer cohorts across all products and especially with customers that are in pool of funds relationships with us.

**Operator** (Operator):
Your next question comes from the line of Sanjit Singh with Morgan Stanley.

**Sanjit Singh** (Analysts):
And on that point of engineering differentiation, you guys have disclosed that you guys are up to 10 million developers now on the platform. So I just wanted to get a sense of how are you seeing that developer traction and that adoption translate into paid workers consumption and ultimately sort of enterprise revenue. And to that end, can you help us give us a sense of how much of agent or AI inferences contribute to workers growth today versus maybe a more traditional sort of developer use case? How quickly is that mix changing? If you can give us any sort of a high-level view on that would be great.

**Matthew Prince** (Executives):
Yes, Sanjit, I appreciate the question. Again, the rate at which developers are growing is just extraordinary. We went from 7 million to 10 million in just a quarter. And I'm just incredibly proud that when developers are looking for what the platform in the future is, they're choosing Cloudflare. The first way it's translating into it is in paying customer count. You can see that we had a record addition of new paying customers this quarter, up 158,000 paying customers, almost double our previous record from last quarter. 
And a lot of that is because that's -- those are developer customers that are there. Some of those are going to be -- are going to stay small customers forever. Some of those are folks like my EA, who's building her first app and using Cloudflare to do that. And she might pay $5 a month or something like that in order to do that.
But it's -- again, it's great and it contributes to everything. But some of those are what are new start-ups that turn into larger businesses. And increasingly, what we're seeing is large existing businesses onboarding more of their developers to the Cloudflare platform. 
And that's driving just as Thomas already talked about, faster pool of funds consumption, which is leading to earlier renewals, which is leading to better NRR and again, driving the flywheel across all of our business. So we're really proud of the fact that the developer platform business is growing as well as it is that we've, I think, hit what is critical mass and we'll continue to grow from here in terms of developer count. And I think more and more, you're seeing that people are building full applications entirely on Cloudflare Workers, and there are whole classes of start-ups. 
It was really fun at our customer conference. We actually did a little sort of mini kind of start-up competition pitch. And like the companies that pitch were incredible, and they were entirely built on Cloudflare Workers. And I think that's something you're just going to see more and more and more of over time, and the developer count is one way to measure it.

**Sanjit Singh** (Analysts):
Yes. that's super encouraging, Matt. Tom, going back to the Analyst Day, you guys called out that the developer platform carries lower gross margin today, but ultimately could have really, really compelling superior unit economics. Given the acceleration that you're seeing in this part of the business, could you remind us of what the core levers or gating levers you have to get Workers' unit economics at or above the core business?

**Thomas Seifert** (Executives):
Yes. I mean what we talked about at the Investor Day and hinted to is that our products all have very different unit economics, some with very high gross margin, longer sales cycles, but also higher cost to book like our Zero Trust products. And our Workers product falls into this category where we have slightly lower gross margins, but significantly lower cost to book, for example. And this is directly reflected in the operating margin we are achieving, and this quarter was a good testament of that. The significant expansion of our operating margin is a result of our accelerated Workers Developers Platform growth. And our guidance now to get to GAAP profitability in the fourth quarter is also a result of this.
So there are a couple of levers to even make that stronger. The engineering is working really, really hard to get more efficiency in our compute infrastructure, how compute infrastructure is utilized by workers, and we are making really good progress. So there is continued gross margin expansion, if you want to say so. And then there is improvements on the unit economic side below gross margin, if you want to say so. 
And if you remember, we said we would exit the year with momentum from a Rule of 40 moving to a Rule of 50 -- to a Rule of 50%. We are far ahead of that currently. And that is a testament to both the growth in the platform, the developer count in the business, but also the significant improvement we are already making on the engineering platform and the compute platform.

**Operator** (Operator):
Your next question comes from the line of Samik Chatterjee with JPMorgan.

**Samik Chatterjee** (Analysts):
Congrats on the strong print here. Matthew, you and Thomas both talked about the -- on the security side, that is now playing a heavier role in terms of the NDR expansion. Can you just talk about sort of what you're seeing in terms of win rates in relation to Cloudflare One, maybe against some of the first-generation Zero Trust vendors? And why are your customers choosing overall Cloudflare products over some of the legacy vendors there? And I have a follow-up.

**Matthew Prince** (Executives):
Yes. Samik, I really appreciate it. I think that we were sort of a second-generation entrant into the Zero Trust and SASE space. And so as such, a lot of what we had to do for a while was just get recognized, get in the conversation. And I think what's really helped us there is actually the developer platform that we've had, being out there talking about here's how you build agents, here's how you think about agents because it turns out those agents need identity. They need to have some way of being protected. And if you're going to turn agents loose within your organization, having the bulkheads that a Zero Trust system provides is more critical than it ever has before. And so as we were talking about the developer platform, what we found is more and more of the time, the Chief Security Officer was sitting in the room taking notes.
And the number of meetings that I've been in where people have said, "I'm way down the RFP process with a traditional kind of Gen 1 Zero Trust vendor, and I'm going to tear it up because they really aren't thinking about agents and the agentic space and how that is different than human users, whereas Cloudflare is." I think that's given us a significant leg up and it's improved our win rates. But I think even more importantly, it's improved the number of deals that we're in. And so what we're seeing more than anything is people are buying just Zero Trust. They're not just buying WAF, they're not just buying DDoS. They're not just buying the developer platform. They're buying the overall platform of Cloudflare.
And they're seeing that if you incorporate and use all of what we do that you get a much more holistic solution. And as a result, like the Zero Trust vendors effectively just become features within what is a much larger platform play. And so I think that -- the biggest recognition is that the smartest companies in the world are increasingly seeing Cloudflare as a true strategic partner to provide one of their core platforms. And that's what's driving not only our wins in Zero Trust, but our wins across the entire platform and the increased adoption that we're seeing and the faster consumption that we're seeing out of the pool fund deals that we sell.

**Samik Chatterjee** (Analysts):
And for my follow-up, if I can go back to the Workers product, and you've seen strong traction with developers on that front. In terms of the large customers that you work with and the new wins you have there, any way to sort of help us think about what portion of your new wins with large customers have Workers incorporated as part of the deal now versus maybe how that's progressed over time? And where do you see more headroom in terms of incorporating that in some of your discussions and wins with new customers?

**Matthew Prince** (Executives):
Yes. I mean I think it is increasing. I'm not -- I don't think we're disclosing exactly what percentage of deals it attaches to, but almost every pool of funds deal that we sell, Workers is a big -- is a big component of it. And it's in the toolkit that's there. And what we find is even if somebody buy -- they bought the Cloudflare platform, they signed up for a pool of funds deal, they may not have even initially thought that they were signing up for Workers. The minute their developer team hears that now they have access to Workers, all of a sudden, they're turning to it because it's such a powerful tool in their toolbox in order to get their job done. 
And so across the board, we're seeing much more adoption of Workers. We're seeing it not just from small customers, but from very large customers as well. It's not just from AI companies. It's from across the board, almost every industry that's out there. And more and more people are seeing that they need to have Workers as a tool in the toolkit of their developers. Their developers are insisting on that. And that's driving not just the sale of Workers, but then also the sale of our SASE products, the sale of our other products. Cloudflare is a platform and increasingly, our customers are recognizing us as that key strategic vendor that is providing one of their key platforms.

**Operator** (Operator):
Your next question comes from the line of Joseph Gallo with Jefferies.

**Joseph Gallo** (Analysts):
Matthew, I wanted to follow up on your earlier cyber comments. You talked about the vulnerability tsunami. Are you seeing cyber budgets inflect? Like what are CISOs doing right now or getting in terms of dollars to fix this never-ending avalanche? And then how can you attack that? Is the better market response to just offer free solutions and then cross-sell into other apps?

**Matthew Prince** (Executives):
I think right now, what CISOs are doing is panic. I mean it feels like the sky is falling. And again, I think everyone is sort of holding their breath and saying, "Hopefully, the worst of it is over." I know for a fact the worst of it is not over. There are significant vulnerabilities that are coming, and you've got to stay on top of them, and you've got to be protected by them. And again, I think that the researcher community is doing a great job disclosing those things responsibly, getting the protections in place as early as possible. But there's scary things that are happening out there. I think the good news of that is we're actually finding these vulnerabilities.
The story I keep telling is which is a more dangerous world to live in, one in which you live in a house where there are incredibly deadly monsters living under every bed and in every cabinet and in every closet, but you don't know they're there or one in which someone is relentlessly going through every closet and cabinet and under every bed, finding the monsters and killing them off. Like we had been for a long time living in that world where the monsters are out there. These vulnerabilities like the PHP vulnerabilities that were disclosed the other day had been in the wild for years. And we're going back to our logs, looking for any evidence that hackers or nation-state actors or others had been using them in the past. And I know that we're going to find examples of that.
I think it's amazing that we're getting those things cleaned up. I think it's great that Cloudflare is protecting everyone. And I think what we're seeing is every company is turning to us. And yes, sure, we're going to provide the services for free. But if you're a major bank, you're not just going to sign up for a free service and think that that's good enough. They are turning to us saying, "We need your help." They're signing major contracts, and they're relying on Cloudflare to be that trusted party that gets information before everyone else and make sure that they have protection in place for the tsunami that isn't -- hasn't hit. 
It's coming, and it's going to be bad. And it's going to be bad for, I think, 2 years. But the good news is we're finding the monsters. We're cleaning them up. And the Internet is actually getting safer, and I'm incredibly proud of our team for staying on top of it, working incredibly hard because there's a lot of new vulnerabilities that are coming out there, and we want to make sure that every single one of our customers has the protection they need.

**Joseph Gallo** (Analysts):
That's really helpful. Maybe just as a follow-up, exciting news on the appointment of Christian Smith. You highlighted doubling down on go-to-market execution. Where is the greatest opportunity to improve execution? And then do you envision a continuation of the current playbook? Or what tactical changes across enterprise sales or channel should we expect?

**Matthew Prince** (Executives):
Yes. I mean I think in the short term, and I've talked with Christian about this, and Christian, I think, has an incredibly good vision for both what's the playbook that we should continue, but also what changes in the future, given all of the changes in how sales is going to look driven in a world that is increasingly technical and increasingly -- has AI as a component of it. 
I think in the short term, it's how do we continue to hire at scale, make sure we're bringing on really great people? How do we increase our awareness, especially with our largest customers to make sure that they know that we are a significant strategic platform and a partner to them. How do we make sure that people have awareness of all of the capabilities that Cloudflare has? And how do we continue to double down on what Mark Anderson has done just such a great job of. And I think Christian is leading that.
But going forward, I think we're going to be experimenting with what's the shift, like how much are we doing what we're already doing, but at greater scale? How many forward deployed engineers do we have that are out there, which we already have at our largest customers, helping them get the most out of Cloudflare. That certainly is going to increase. What's the ratio of solutions engineers to AEs? What exactly are the specific technical overlays and how specific do we want the individual salespeople to have knowledge in all of the different products that we have. I think that's all going to redefine what sales looks like in an increasingly, again, AI-driven and an increasingly technical world. 
And I think that there will be an evolution. And as we talk to -- and we got to talk to so many incredible candidates. The thing that really stood out to me was Christian knew both how to continue to execute on what we need to deliver today, but also how do we stay malleable and adaptable to how sales is going to change and evolve over the next years to come. And I can't imagine a better partner than he is.

**Operator** (Operator):
Your next question comes from the line of Fatima Boolani with Citi.

**Fatima Boolani** (Analysts):
Matthew, I'd like to ask this of you. About 6 months ago, you made a decisive and difficult decision to restructure the organization. And certainly, the impetus was not to drive operating leverage, and that was certainly something you communicated. But with 6 months under your belt with this change, from a financial perspective, it's not like we've seen margin expansion, right? 
And just kind of reiterating my point that, that was not the impetus. I'm curious if you can talk to us about how this has fundamentally and structurally changed the way Cloudflare goes to business and showed up both in terms of your agility and some of the comments that you just made from a go-to-market perspective, how that colors your lens there. But just if you can give us some concrete examples of what the aftermath of some of those difficult restructuring moves has been in terms of your ability and your successes in operating the business at this level.

**Matthew Prince** (Executives):
Yes. So first of all, Fatima, when we made the decision to lay people off, it was an incredibly hard decision. We let go of a number of people who were extremely talented, people who I considered friends. And I'm proud of the fact that we had an incredibly generous severance package. We continue to vest people's shares, which was something that most companies haven't did -- haven't done. And also that we worked with them to figure out great places that they could work because someone who is a middle manager at Cloudflare could be a great senior manager at a fast-growing start-up. And I'm proud of the fact that we really helped place a large number of the people who we let go because they're very talented and they deserve to be treated with respect.
It really had less to do with the people. It had much more to do with what we saw as the way that organizations were going to be structured going forward. And I wrote an editorial in the Wall Street Journal about how Peter Drucker used to talk about how there are 3 types of functions within any company. There are people who build things. There are people who sell things, and there are people who measure things. And what we found with AI is that the builders are getting more efficient than ever. 
And so we're trying to hire as many great builders as we can. And again, as you said, we're not trying to cut headcount. We actually are just shifting headcount to more builders. Same thing with sellers. In the past, sellers might have spent 60% of their time getting prepared for meetings, filling out sales force reports, doing all of that. That's not what they love doing. What they love doing is being in front of customers. And we've been able to dramatically increase the amount of time that sellers are in front of customers, and you see that in sales productivity.
What's changed are the people who are the measurers. And AI is incredibly good at measuring things. 
And we have found across our business that in many cases, it's better than what humans can do. AI has biased, but the bias is not correlated to the rest of the organization, unlike what everything else has done. And so for a very specific example, which I asked if I could tweet and everybody said, not until after earnings and the person who -- I'm staring at the person who knows I'm going to tell her story right now on a screen. But Heather on our team, who for a long time was on our IR team, built an agent now that has automated pulling together all the investor materials, all the sort of statistical cheat sheets that we have that make sure that we have all the metrics right at our fingertips, giving us suggestions on kind of our earnings scripts, being able to deliver that. 
And instead of that being something that took a large team, a significant amount of time to do every single quarter. It now takes an agent less than a couple of hundred bucks in token costs to be able to put that together. And we've seen a higher quality of what gets put out, more accuracy, fewer errors, and it's just better.
And so I think what we knew we needed to do was flatten Cloudflare's organization. We needed to double down on builders. We needed to double down on sellers. And then we needed to get more efficient in those places where AI could help us be significantly more efficient. And so again, as I said at the time when we laid people off, I think our headcount is going to be larger by the end of the year than it was even before the layoffs. We're hiring like crazy. It's who we're hiring and the roles that we're hiring for that are changing. 
And frankly, I think that we were early in that, but just about every company is going to go through that transition. And as you come out the other side of it, I think our financial results show you can become a much more nimble, much more innovative, just much more successful company if you get the right people in the right functions and use technology to help those people, not replace those people, but help those people do their jobs better.

**Operator** (Operator):
We have now reached the end of this Q&A session. I would like to turn the call back to Matthew Prince for closing remarks.

**Matthew Prince** (Executives):
I want to thank the entire team and especially Mark Anderson for all of his service. We couldn't have done this without you. It's your last earnings call with us, but we're super happy to have you on board. I'm getting choked up. Thank you so much for everyone. It was an incredible quarter, a monster quarter. We'll see you back here next quarter.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NET_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：Q3 2026 營收財測區間，年增 31%（原話："range of $736 million to $737 million"）
- 2026-08-06｜CFO｜guidance：Q3 營業利益財測（原話："in the range of $129 million to $130 million"）
- 2026-08-06｜CFO｜guidance：全年營收財測（原話："in the range of $2.864 billion to $2.870 billion,"）
- 2026-08-06｜CFO｜guidance：全年營業利益財測（原話："range of $443 million to $445 million."）
- 2026-08-06｜CFO｜guidance：2026 全年網路 CapEx 佔營收比重指引（原話："we expect network CapEx to be 14% to 15% of revenue"）
- 2026-08-06｜CFO｜guidance：2026 重組費用上調至最多 1.65 億美元，其中現金最多 1.3 億（原話："up to $130 million expected to be cash related"）
- 2026-08-06｜CFO｜guidance：排除重組費用後，全年自由現金流預期不變（原話："our free cash flow expectations for 2026 remain unchanged"）
- 2026-08-06｜CFO｜guidance：毛利率預期穩定在目前水準（原話："Gross margin, I think, will stabilize around the level"）
- 2026-08-06｜CFO｜margin：Q2 毛利率 73.1%（原話："Second quarter gross margin was 73.1%"）
- 2026-08-06｜CFO｜margin：毛利率年減 320 bps，成因為付費流量佔比上升使網路成本由銷管轉入營收成本（原話："a decrease of 320 basis points year-over-year"）
- 2026-08-06｜CFO｜margin：管理層稱網路成本分攤趨勢出現趨穩跡象（原話："However, as we discussed at Investor Day, this trend is"）
- 2026-08-06｜CFO｜margin：管理層把焦點放在整體 unit economics，預期下半年續擴張（原話："we will continue to see expansion over the course of the"）
- 2026-08-06｜CFO｜margin：Q2 營業利益率 13.8%（原話："Second quarter operating margin was 13.8%"）
- 2026-08-06｜CFO｜margin：營業利益率較去年同期下滑 30 bps（原話："a decrease of 30 basis points year-over-year"）
- 2026-08-06｜CFO｜margin：銷管費用率由 36% 降至 33%（原話："decreased to 33% from 36% in the same quarter last year."）
- 2026-08-06｜CFO｜risk：重組費用高於原先預期，管理層稱優先求解決速度（原話："we prioritized speed of resolution, particularly"）
- 2026-08-06｜CFO｜risk：管理層說明 pool of funds、消耗型合約使逐季變動更難預測（原話："becomes a little bit more difficult to forecast"）
- 2026-08-06｜CFO｜risk：管理層用「更高標準差」描述客戶層面的波動（原話："a higher standard deviation"）
- 2026-08-06｜CFO｜commitment：GAAP 獲利目標（最晚 2028 年底）進度領先（原話："We are pacing ahead of that very clearly"）
- 2026-08-06｜CFO｜commitment：排除重組費用後 Q2 GAAP 淨損約 1,800 萬美元（原話："the GAAP net loss would have been around $18 million"）
- 2026-08-06｜CFO｜customer：大客戶年增 27%，較上季 25% 加速（原話："representing an increase of 27% year-over-year"）
- 2026-08-06｜CFO｜customer：NRR 120%（原話："dollar-based net retention rate to 120% in the second"）
- 2026-08-06｜CFO｜customer：RPO 為 27.32 億美元（原話："or RPO, came in at $2.732 billion"）
- 2026-08-06｜CEO｜customer：管理層稱主要 AI 公司多數為客戶（原話："over 80% of the major AI companies are Cloudflare customers"）
- 2026-08-06｜CEO｜competition：一筆媒體客戶合約提到面對整合至既有超大型雲端業者的壓力（原話："Despite competitive pressure to consolidate spend with"）
- 2026-08-06｜CEO｜competition：CEO 稱 SASE／Zero Trust 近 6 個月明顯取得份額（原話："SASE and Zero Trust platforms to actually gain share"）
- 2026-08-06｜CEO｜competition：CEO 說明不參與 AI 基建軍備競賽的理由（原話："selling commodity hardware because that, again, is bad"）
- 2026-08-06｜CEO｜capital_allocation：CEO 稱對單位 CapEx 的使用率可做到 10 倍（部分情況）（原話："get 10x as much utilization out of every CapEx dollar"）
- 2026-08-06｜CEO｜product：Workers 營收角色改口：由重採用轉為實質營收貢獻（原話："playing for adoption, we weren't playing for revenue"）
- 2026-08-06｜CEO｜product：CEO 稱 Workers 已成為營收的有意義貢獻者（原話："Workers has become a meaningful contributor to revenue"）
- 2026-08-06｜CEO｜product：Monetization Gateway 讓客戶出售 Cloudflare 後方資源（原話："Monetization Gateway allows our customers to sell any"）
- 2026-08-06｜CEO｜product：對 AI 代理流量擬收取極小額費用（原話："a very, very small fee, fractions of a penny"）
- 2026-08-06｜CEO｜product：CEO 對非人類流量長期預測（自稱每次都預測錯）（原話："traffic will be as much as 1,000x as much as human"）
- 2026-08-06｜CEO｜commitment：CEO 預期合作夥伴營收佔比續升（原話："it gets north of 50%, even maybe over 60%."）

### NET_Analyst_Investor_Day_Cloudflare_Inc_20260609.md
- 2026-06-09｜Thomas Seifert (CFO)｜guidance：CFO 稱營收年化 50 億美元目標將在 2028 年之前超越（原話："on pace to surpass the $5 billion annualized revenue target"）
- 2026-06-09｜Thomas Seifert (CFO)｜guidance：CFO 宣布 2027 年起北極星指標由 Rule of 40 上調為 Rule of 50（原話："will move our North Star up to a Rule of 50."）
- 2026-06-09｜Thomas Seifert (CFO)｜guidance：長期營運模型：營業利益率目標由 20% 升至 30%（原話："margin targets will go up from plus 20% to plus 30%"）
- 2026-06-09｜Thomas Seifert (CFO)｜guidance：長期營運模型：自由現金流率目標約 30% 至 35%（原話："increase moving forward to about 30% to 35%"）
- 2026-06-09｜Thomas Seifert (CFO)｜commitment：CFO 承諾最晚 2028 年達成 GAAP 獲利（原話："We will achieve GAAP profitability latest by '28."）
- 2026-06-09｜Thomas Seifert (CFO)｜guidance：長期毛利率區間放寬為 70% 至 77%，CFO 說明不是預期在區間內來回波動（原話："we will fluctuate between 70% and 77% all the time"）
- 2026-06-09｜Thomas Seifert (CFO)｜margin：CFO 在問答中稱第二季毛利率將看到趨穩（原話："I can say that you will see already a stabilization in"）
- 2026-06-09｜Thomas Seifert (CFO)｜margin：單位經濟毛利（unit economic margin）2025 年底升至約 44%，同時毛利率下滑（原話："we increased our unit economic margin to about 44%"）
- 2026-06-09｜Thomas Seifert (CFO)｜margin：免費轉付費造成的毛利率逆風為成本科目重分類，CFO 稱已觸底趨平（原話："I think moving forward, we've bottomed out it's"）
- 2026-06-09｜Thomas Seifert (CFO)｜margin：CFO 指出開發者平台（Act III）目前毛利率低於其他產品（原話："our developer products currently carry a lower gross margin"）
- 2026-06-09｜Thomas Seifert (CFO)｜margin：CFO 稱規模化後 Act III 單位經濟可能超越 Act I 與 Act II（原話："we think that Act III could surpass Act I and Act II"）
- 2026-06-09｜Thomas Seifert (CFO)｜margin：CFO 稱 Act IV 單位經濟曲線可能超出圖表（原話："Act IV could literally shift us off the chart"）
- 2026-06-09｜Thomas Seifert (CFO)｜margin：資金池（Pool of Funds）合約在客戶擴約期間造成營收下凹，用量不降，因此對毛利率有輕微逆風（原話："there's also a slight headwind to gross margin"）
- 2026-06-09｜Thomas Seifert (CFO)｜margin：Pool of Funds 佔 2025 年第四季新增 ACV 的 20%（口徑說明）（原話："of our new ACV was coming in, in Pool of Funds."）
- 2026-06-09｜Thomas Seifert (CFO)｜guidance：CFO 說明上限（cap）模型下營收認列落後於用量，增加預測難度（原話："the lag to revenue will come with this model"）
- 2026-06-09｜Thomas Seifert (CFO)｜customer：舉例一家大型 AI 客戶在第四季大幅提高資金池承諾（原話："a significant step-up in commitment, north of 215%"）
- 2026-06-09｜Thomas Seifert (CFO)｜margin：銷售與行銷費用佔比將較先前下降（原話："Sales and marketing will come down a bit compared"）
- 2026-06-09｜Thomas Seifert (CFO)｜margin：研發費用維持現有水準（原話："R&D will pretty much stay in the zones where we are today."）
- 2026-06-09｜Thomas Seifert (CFO)｜margin：CFO 預期 G&A 成本基準因 AI 顯著下降（原話："will significantly fall and we will be leading that charge"）
- 2026-06-09｜Thomas Seifert (CFO)｜capital_allocation：支援職能節省的費用不流向利潤，而是再投入業務承載能力（quota-carrying capacity）（原話："We will not let those dollars fall to the bottom line."）
- 2026-06-09｜Thomas Seifert (CFO)｜commitment：CFO 稱今年餘下時間業務承載能力將持續增加（原話："the sales capacity is going to continue to increase"）
- 2026-06-09｜Mark Anderson｜commitment：Mark Anderson 稱將持續投資銷售產能（原話："my plan is to continue to invest in sales capacity"）
- 2026-06-09｜Mark Anderson｜risk：銷售長 Mark Anderson 宣布年底退休（原話："end of this year, I'm going to retire."）
- 2026-06-09｜Mark Anderson｜risk：公司將立即公開徵才接任銷售長（原話："We're launching a public search right away."）
- 2026-06-09｜Thomas Seifert (CFO)｜product：總潛在市場（TAM）預估今年約 2,380 億美元，尚未納入 Act IV（原話："$238 billion for this year"）
- 2026-06-09｜Thomas Seifert (CFO)｜customer：結轉管線（carryforward pipeline）年增 40%（原話："already up 40% year-over-year."）
- 2026-06-09｜Thomas Seifert (CFO)｜product：2025 年 SASE 產品 ARR 成長 43%、開發者平台 ARR 成長 137%（原話："SASE product suite is up 43%, and developer grew 137%"）
- 2026-06-09｜Mark Anderson｜customer：百萬美元以上客戶成長斜率自 2024 下半年起轉折（原話："inflection in the slope of our $1 million-plus customers"）
- 2026-06-09｜Mark Anderson｜customer：過去一個月與 Anthropic、OpenAI、Lovable 等 AI 原生公司的合作已商業化（原話："commercialized major relationships with AI native companies"）
- 2026-06-09｜Mark Anderson｜customer：網路上代理流量（agentic traffic）過去一年成長 1,700%（原話："agentic traffic on our network, as you saw, grew 1,700%"）
- 2026-06-09｜Stephanie Cohen｜customer：受代理式網路影響最大的產業，營收成長高於 37%（原話："we're experiencing revenue growth north of 37%"）
- 2026-06-09｜Matthew Prince｜customer：OpenAI 最新平台建於 Cloudflare 之上（原話："OpenAI built their latest new platform"）
- 2026-06-09｜Matthew Prince｜product：管理層稱機器人流量已超過人類流量，且比先前預測（2027 上半年）更早（原話："bots have already exceeded human traffic online"）
- 2026-06-09｜Matthew Prince｜product：CEO 預期五年內網路流量為現在的 10 至 100 倍（原話："probably be 10 to 100x the traffic volumes that we see today"）
- 2026-06-09｜Matthew Prince｜product：CEO 設想對每月約 5 億筆交易中 1% 至 10% 做微支付（原話："and 10% of those, you can have some sort of micro payment"）
- 2026-06-09｜Stephanie Cohen｜product：x402 付款要求回應大多尚未形成實際交易（原話："they don't actually result in a transaction"）
- 2026-06-09｜Stephanie Cohen｜product：網路上每日 402 回應超過 20 億次（原話："there are more than 2 billion 402"）
- 2026-06-09｜Stephanie Cohen｜product：Stephanie 稱 Bot 管理由資安工具擴及營收分析，產品變得缺乏價格彈性（原話："commodity is now price inelastic."）
- 2026-06-09｜Rita Kozlov｜product：Rita 稱 isolates 比其他運算效率高 100 倍（原話："we can be 100x more efficient than any type of compute"）
- 2026-06-09｜Rita Kozlov｜product：Rita 提出反例：一般成長緩慢的應用跑在 Workers 上可能貴約 15%（原話："being about 15% more expensive."）
- 2026-06-09｜Rita Kozlov｜product：Rita 稱執行 100 萬個代理時，成本效益近 75%（原話："going to be nearly 75% more cost effective on Cloudflare"）
- 2026-06-09｜Stephanie Cohen｜product：Stephanie 引用 Rita 的說法：代理應用總持有成本低 60% 至 70%（原話："is 60% to 70% less expensive."）
- 2026-06-09｜Rita Kozlov｜product：Rita 稱 AI 下一個瓶頸將是 CPU 資源（原話："the next bottleneck is going to be on access to the CPU"）
- 2026-06-09｜Rita Kozlov｜risk：Rita 承認選擇 isolates 的代價是舊應用較難搬上 Cloudflare（原話："it would be harder to lift and shift"）
- 2026-06-09｜Stephanie Cohen｜risk：Stephanie 稱零售、軟體、IT、金融網站人類流量近一年顯著下降（原話："finance are all seeing meaningful declines in human traffic"）
- 2026-06-09｜Mark Anderson｜risk：Mark 稱 IT 預算大致持平、成長溫和（原話："flat budgets, IT spending is growing modestly."）
- 2026-06-09｜Matthew Prince｜competition：CEO 稱毛利率壓力並非來自競爭加劇，Cloudflare 常被視為唯一選項（原話："we are oftentimes selected as a category"）
- 2026-06-09｜Matthew Prince｜margin：CEO 稱毛利率壓力來自開發者平台成長快速（原話："just seen so much growth in our developer platform."）
- 2026-06-09｜Matthew Prince｜competition：CEO 稱其他資安公司缺乏開發者平台，講的是昨天的遊戲（原話："they sound like they're kind of talking yesterday's game"）
- 2026-06-09｜Matthew Prince｜competition：CEO 承認 Zero Trust 起步較晚，過去未必能進入採購討論（原話："The challenge was like we were late to the game."）
- 2026-06-09｜Mark Anderson｜customer：客戶諮詢委員會調查：選 Zero Trust 為年度策略機會者，兩年間由 75% 降至 65%（原話："same survey 65% of the people said Zero Trust"）
- 2026-06-09｜Matthew Prince｜competition：CEO 稱與前沿 AI 實驗室緊密合作，Cloudflare 是其程式碼預設去處（原話："Cloudflare is the default where it goes to."）
- 2026-06-09｜Matthew Prince｜risk：CEO 預期資安獨立品類只會熱絡約兩年，之後逐漸淡出（原話："will be really exciting for 2 years and then kind"）
- 2026-06-09｜Matthew Prince｜product：CEO 稱可能把 Cloudflare OS 免費送出以示範價值（原話："we may just give Cloudflare OS away for free"）
- 2026-06-09｜Matthew Prince｜product：CEO 對 10 至 100 倍流量預測的看法：寧可押超過（原話："I'd probably pick the over."）

### 問答異常語氣（迴避／改口／保留）
- NET_Q2_2026_Earnings_Call_20260806.md｜問：Citi Boolani：Workers／Workers AI 營收規模與占比｜答法：CEO 開場即說「not fully answering your question」，表示未拆分產品別營收與成長率，改談定性描述
- NET_Q2_2026_Earnings_Call_20260806.md｜問：Barclays Kalia：下半年毛利率起伏的 puts and takes｜答法：CFO 未給毛利率數字，轉談 unit economics，只說毛利率會穩定在現有水準
- NET_Q2_2026_Earnings_Call_20260806.md｜問：Morgan Stanley Singh：早期 pool of funds 續約的營收逆風是否已過｜答法：CFO 未直接回答是否已過，改談趨勢向上與模型多元化，並稱逐季預測更難、財測維持審慎
- NET_Q2_2026_Earnings_Call_20260806.md｜問：William Blair MacWilliams：下半年 NRR 建模方向｜答法：CFO 未提供 NRR 建模指引，只說各產品、客群、合約型態皆強勁
- NET_Q2_2026_Earnings_Call_20260806.md｜問：Scotiabank Colville：網路安全風險上升是否已反映在 Q2 財務模型｜答法：問題第二部分（CFO）在回答中未被正面回應，CEO 只回答 AI 基建問題後即進入結語
- NET_Analyst_Investor_Day_Cloudflare_Inc_20260609.md｜問：Gabriela Borges：Cloudflare OS 是否能長期商業化與變現｜答法：CEO 回答客戶都想要、「letting people play with it」，未回答變現方式或定價；稍後另一問答中提到可能免費提供
- NET_Analyst_Investor_Day_Cloudflare_Inc_20260609.md｜問：Fatima Boolani：Claude managed agents 與 Cloudflare 的合作／競爭界線，以及 Cloudflare 如何收費｜答法：CEO 強調與前沿實驗室緊密合作與 isolates 優勢，未直接回答競合界線與收費模式
- NET_Analyst_Investor_Day_Cloudflare_Inc_20260609.md｜問：Matthew Hedberg：毛利率短期是否承壓、之後如何走升｜答法：CFO 以「journey」回應，承認可能再度下探，未給出數字或時點，只說第二季將趨穩

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
{"date":"20260807","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Agentic AI 時代需要一個不屬於任何模型廠的中立基礎層（身分驗證、爬蟲付費、推論路由、工具呼叫的信任邊界），而超大規模雲因利益衝突無法扮演這個角色。","columns":{"目前證據":"2026-09-15 起 mixed-use 爬蟲改為預設封鎖；pay-per-crawl 已在部分出版商上線；Prince 在 Q2 財報明說「Cloudflare 位於這場典範轉移的中心——建造 agentic internet 的基礎設施、控制、開發者工具與支付軌道」。","證偽門檻":"2027 年中前仍未揭露 AI／Workers 相關年化 run-rate 絕對金額；或主要 AI 實驗室集體繞過（直接與出版商簽約）","狀態":"待驗"}},{"id":"H2","text":"非 GAAP 營益率從 FY25 的 14.0% 往 30%+ 擴張，且擴張速度快過毛利率的下滑速度——即「毛利換規模」是划算的交易。","columns":{"目前證據":"Q3 FY26 guide 營益率 17.6%（+3.6pp vs FY25）；FY26 全年 guide 15.5%。同期毛利率下滑約 3pp。營益率的擴張幅度已大於毛利率的損失。","證偽門檻":"Q3 非 GAAP 營益率未達 17.6%；或 FY26 全年低於 15.5%","狀態":"初步成立"}},{"id":"H3","text":"市場願意持續給這門生意 40x+ EV／營收的倍數，直到獲利真正兌現。","columns":{"目前證據":"NET／DDOG 的 Fwd PE 比值為 2.65x（208.4 ÷ 78.7），低於前份 DD 的 ~3.0x——但這是因為整個同業群一起再評價，不是 NET 變便宜。","證偽門檻":"NET／DDOG Fwd PE 比連二季 &gt; 4.5x；或同業群整體倍數體制下移（DDOG Fwd PE 跌破 50x）","狀態":"最脆弱一環"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE FY2 ≤122x（≈$194；分母固定用共識 FY27 EPS $1.586，對應以自建模型 FY31 終值 $260 折現的 Base IRR +6%/yr）；或 AI／Workers 相關年化 run-rate 首度揭露 ≥$400M 且非 GAAP 毛利率連二季站回 73%+（論點增強，可不等回檔）","irr_base_pct":-4.7,"ev5y_pct":-16.4,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":0.7,"ev5y_pct":-16.4,"irr_base_pct":-4.7,"max_dd_pct":-70.0,"bull_5y_price":509.0,"bear_5y_price":107.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE FY2 ≤122x（≈$194；分母固定用共識 FY27 EPS $1.586，對應以自建模型 FY31 終值 $260 折現的 Base IRR +6%/yr）；或 AI／Workers 相關年化 run-rate 首度揭露 ≥$400M 且非 GAAP 毛利率連二季站回 73%+（論點增強，可不等回檔）","price_at_dd":330.5,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NET_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
