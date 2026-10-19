你是 stock-analyst **v20 判斷 agent**，標的 WMT（20261019）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"WMT","date":"2026-10-19","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WMT_20261019/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WMT_20261019/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenues_gaap","label":"Total revenues (GAAP)","value":187.9,"period":"Q2 FY2027（季末 2026-07-31，公告於 2026-08-20）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2027（季末 2026-07-31，公告於 2026-08-20）","citation":"Walmart Q2 FY27 earnings release（IR）"}},{"id":"f_kpi1_gaap_operating_income","label":"GAAP operating income","value":9383,"period":"Q2 FY2027（季末 2026-07-31，公告於 2026-08-20）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2027（季末 2026-07-31，公告於 2026-08-20）","citation":"Walmart Q2 FY27 earnings release（IR）"}},{"id":"f_kpi2_adjusted_operating_incom","label":"Adjusted operating income (cc)","value":9248,"period":"Q2 FY2027（季末 2026-07-31，公告於 2026-08-20）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2027（季末 2026-07-31，公告於 2026-08-20）","citation":"Walmart Q2 FY27 earnings release（IR）；cc 基準，+17.4% cc；剔除關稅退款後落在 7–10% 指引上緣"}},{"id":"f_kpi3_adjusted_eps","label":"Adjusted EPS","value":0.81,"period":"Q2 FY2027（季末 2026-07-31，公告於 2026-08-20）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2027（季末 2026-07-31，公告於 2026-08-20）","citation":"Walmart Q2 FY27 earnings release（IR）"},"note":"公司原指引 $0.72–0.74（web_search 摘要，未取得共識值）"},{"id":"f_kpi4_free_cash_flow","label":"Free cash flow（上半年累計，非單季）","value":5.5,"period":"H1 FY2027（半年至 2026-07-31，公告於 2026-08-20）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"H1 FY2027（半年至 2026-07-31，公告於 2026-08-20）","citation":"Walmart Q2 FY27 earnings release（IR）"}},{"id":"f_kpi5_global_ecommerce_sales_g","label":"Global eCommerce sales growth","value":23,"period":"Q2 FY2027（季末 2026-07-31，公告於 2026-08-20）","unit":"% YoY","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2027（季末 2026-07-31，公告於 2026-08-20）","citation":"Walmart Q2 FY27 earnings release（IR）"}},{"id":"f_kpi6_global_advertising_growt","label":"Global advertising growth","value":38,"period":"Q2 FY2027（季末 2026-07-31，公告於 2026-08-20）","unit":"% YoY","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2027（季末 2026-07-31，公告於 2026-08-20）","citation":"Walmart Q2 FY27 earnings release（IR）"}},{"id":"f_kpi7_guidance_q3_fy27","label":"Guidance: Q3 FY27","value":"net sales cc +3.0% ~ +3.75%；operating income cc +2.0% ~ +4.0%；adj EPS $0.62–0.64","period":"Q2 FY2027 公告（2026-08-20）","unit":"guidance","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2027 公告（2026-08-20）","citation":"Walmart Q2 FY27 earnings release（IR）"}},{"id":"f_kpi8_guidance_fy27","label":"Guidance: FY27 全年","value":"net sales cc +4.0% ~ +5.0%（原 3.5–4.5%）；adj operating income cc +7.0% ~ +8.5%（原 6.0–8.0%）；adj EPS $2.80–2.87","period":"Q2 FY2027 公告（2026-08-20）","unit":"guidance","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2027 公告（2026-08-20）","citation":"Walmart Q2 FY27 earnings release（IR）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-20","period":"2026-08-20","unit":"date","basis":"距今 42 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-20"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_wmt_gross_margin_pct","label":"WMT 毛利率","value":25.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMT.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wmt_operating_margin_pct","label":"WMT 營業利益率","value":4.39,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMT.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wmt_fcf_margin_pct","label":"WMT FCF 利潤率","value":1.84,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMT.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cost_gross_margin_pct","label":"COST 毛利率","value":12.88,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COST.gross_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cost_operating_margin_pct","label":"COST 營業利益率","value":3.82,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COST.operating_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cost_fcf_margin_pct","label":"COST FCF 利潤率","value":3.0,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COST.fcf_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tgt_gross_margin_pct","label":"TGT 毛利率","value":29.3,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TGT.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tgt_operating_margin_pct","label":"TGT 營業利益率","value":5.59,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TGT.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tgt_fcf_margin_pct","label":"TGT FCF 利潤率","value":4.14,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TGT.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_gross_margin_pct","label":"AMZN 毛利率","value":50.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_operating_margin_pct","label":"AMZN 營業利益率","value":11.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_fcf_margin_pct","label":"AMZN FCF 利潤率","value":-0.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dg_gross_margin_pct","label":"DG 毛利率","value":31.16,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DG.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dg_operating_margin_pct","label":"DG 營業利益率","value":5.59,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DG.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dg_fcf_margin_pct","label":"DG FCF 利潤率","value":4.61,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DG.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":118.81,"period":"2026-10-16（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-6.41,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":73.01,"period":"2026-10-16（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.89 → 2.89）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.31,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.23 → 3.22）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.63 → 3.63）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":2.89,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.22,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.63,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-0.34,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 2.9 → 2.89（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":43.05,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝75.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":75.3,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.28,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝78.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":78.5,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.37,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝79.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":79.2,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":38.53,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 2.89，分子＝快照價 111.35","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.824,"period":"2026-10-19","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-19"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":63563.0,"period":"2026-10-19","unit":"USD m","basis":"yfinance 最新一季：總債務 75092.0、現金 11529.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":7958.08,"period":"2026-10-19","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":1009062.34,"period":"2026-10-19","unit":"USD m","basis":"市值 945499.34 ＋ 淨負債 63563.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":752858.23,"period":"2026-10-19","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（37 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":785569.46,"period":"2026-10-19","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（37 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.34,"period":"2026-10-19","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Numerator 資料顯示 Walmart 在美國 CPG 市佔由 2024 年 21.1% 降至 2025 年 20.6%、2026 年 20.4%；Costco 升至 8.1%、Amazon 含 Whole Foods 升至 8%（升幅最大）","source":"Supermarket News, Walmart continues to lose grocery market share","url":"https://www.supermarketnews.com/grocery-trends-data/walmart-continues-to-lose-grocery-market-share","excerpt":"The retailer's share has dropped from 21.1% in 2024 to 20.6% in 2025 and 20.4% in 2026.","as_of":"2026-01-01","retrieved_at":"20261019","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Yonhap 報導（2026 年 7 月）：截至 6/30 的一年，Amazon 美國食品雜貨市佔增幅最大；同期 Costco、Walmart、Trader Joe's、Aldi 市佔亦擴大，Kroger 與 Albertsons 下降","source":"Yonhap item via search summary (2026-07)","url":null,"excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261019","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Zacks 報告稱 Walmart 配送服務改善帶來雜貨市佔穩定成長（as_of 為報告日期 20251202；來源為二手摘要）","source":"Zacks Research Report WMT 2025-12-02","url":"https://advisortools.zacks.com/proxy/ResearchReport/WMT/report?d=20251202","excerpt":null,"as_of":"2025-12-02","retrieved_at":"20261019","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Walmart 10-Q（截至2026-07-31）列示信評：S&P 長期債 AA／CP A-1+，Moody's Aa2／P-1，Fitch AA／F1+；FY2026 10-K 與 2026-04 10-Q 等級相同，搜尋未見 2026 年評等異動","source":"Walmart Inc. Form 10-Q (quarter ended 2026-07-31), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0000104169/000010416926000154/wmt-20260731.htm","excerpt":"As of July 31, 2026, the ratings assigned to our commercial paper and rated series of our outstanding long-term debt were as follows","as_of":"2026-07-31","retrieved_at":"20261019","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Coresight 估計 2026 年美國零售業開約 5,500 店、關約 7,900 店；Dollar General 計畫開 450 店、Aldi 180 店，折扣業者是擴張主力。","source":"ConsumerAffairs, Retail comeback? 900+ stores set to open across the U.S. in 2026","url":"https://www.consumeraffairs.com/news/retail-comeback-900-stores-set-to-open-across-the-us-in-2026-031226.html","excerpt":"Coresight Research estimates U.S. retailers will open about 5,500 new stores this year (up 4.4% year over year) and close about 7,900 stores.","as_of":"2026-03-12","retrieved_at":"20261019","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Walmart 計畫 2026 年改裝 650 間以上門市，並在 2026 年底至 2027 年初新開約 20 間，約為 2025 年（9 間）的兩倍多；公司未揭露花費。","source":"Chain Store Age / Retail TouchPoints, Walmart to Remodel 650 Stores this Year, Add 20 All-New Ones","url":"https://chainstoreage.com/walmart-remodel-650-plus-stores-2026-details-new-store-growth","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261019","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Walmart 美國部門 2026-07-31 止季淨銷售 1,252 億美元，年增 3.5%，不含油可比銷售 +2.6%，交易筆數 +1.5%，由高收入家庭帶動。","source":"搜尋摘要（Walmart 財報彙整報導）","url":null,"excerpt":"Walmart U.S. recorded net sales of $125.2 billion, representing year-over-year growth of 3.5%. Comparable sales, excluding fuel, increased 2.6%. Growth was accompanied by a 1.5% increase in transactions","as_of":"2026-08-20","retrieved_at":"20261019","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"GlobalData：2025 年約 28% 高收入消費者在折扣連鎖（如 Walmart）購物，2021 年約 20%。","source":"GlobalData Retail（經搜尋摘要轉述）","url":null,"excerpt":"Research from GlobalData Retail shows that nearly 28% of high-income consumers shopped at discount retailers such as Walmart in 2025, up from around 20% in 2021.","as_of":"2026-01-01","retrieved_at":"20261019","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"CEO 說明低收入家庭近期承受額外壓力，中等收入家庭穩定，高收入家庭更常來 Walmart。","source":"Food Business News, Walmart growth helped by higher income consumers","url":"https://www.foodbusinessnews.net/articles/29400-walmart-growth-helped-by-higher-income-consumers","excerpt":"Middle-income households have been steady, and while lower-income families have been under additional pressure of late","as_of":"2025-11-20","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Walmart FY2027 營收指引 7,347–7,417 億美元，低於共識 7,518 億美元；Q3 指引亦低於共識。","source":"MarketBeat, Walmart issues FY 2027 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/walmart-nasdaqwmt-issues-fy-2027-earnings-guidance-2026-08-20/","excerpt":"Its FY2027 revenue guidance of $734.7–$741.7 billion compares with a consensus revenue estimate of $751.8 billion","as_of":"2026-08-20","retrieved_at":"20261019","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Bank of America 預測 FY2027/28/29 調整後 EPS 為 2.90／3.20／3.53 美元，並稱美國可比銷售維持 3%–4% 區間。","source":"搜尋摘要（Bank of America 預測轉述）","url":null,"excerpt":null,"as_of":"2026-08-20","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FTC 與多州檢察長於 2026-02-26 在加州北區聯邦法院對 Walmart 提起 driver platform（配送司機平台）訴訟，列於 10-Q 法律程序","source":"Walmart Inc. Form 10-Q (period ended 2026-07-31)","url":"https://www.sec.gov/Archives/edgar/data/0000104169/000010416926000154/wmt-20260731.htm","excerpt":"Federal Trade Commission and State Attorneys General Driver Platform Litigation: Federal Trade Commission, et al. v. Walmart Inc., USDC, N.D. Cal., 2/26/26","as_of":"2026-07-31","retrieved_at":"20261019","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"墨西哥競爭主管機關（COFECE）對 Walmart de México 的調查（2023-10-06 立案）與印度 CCI 調查（2020-01-13 命令）仍列於 Walmart 備案文件；本次搜尋未見結果","source":"Walmart Inc. Form 10-Q (period ended 2026-07-31)","url":"https://www.sec.gov/Archives/edgar/data/0000104169/000010416926000154/wmt-20260731.htm","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261019","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"中國監管機構要求沃爾瑪中國（Sam's Club China 相關投訴後）加強食品安全合規與供應鏈管理","source":"China Daily, 2026-06-17","url":"https://www.chinadaily.com.cn/a/202606/17/WS6a31fa03a310986e2b4606ec.html","excerpt":null,"as_of":"2026-06-17","retrieved_at":"20261019","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"未發現 2026 年美國 DOJ 對 Walmart 的合併或行為反壟斷行動，亦未見歐盟競爭案；DOJ 相關為鴉片類藥物訴訟與 False Claims Act，非反壟斷","source":"Walmart Inc. Form 10-Q (period ended 2026-07-31) 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0000104169/000010416926000154/wmt-20260731.htm","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261019","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025-03：中國商務部約談 Walmart，因其被報導要求中國供應商吸收關稅成本；中方警告若持續可能面臨進一步後果（屬 2025 年事件，非 2026 新增）","source":"Axios: Walmart clashes with China after asking suppliers to absorb tariffs","url":"https://www.axios.com/2025/03/12/trump-tariffs-walmart-china","excerpt":null,"as_of":"2025-03-12","retrieved_at":"20261019","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-03：最高法院 6-3 裁定廢止 IEEPA 關稅；但鋼、鋁、半導體等 Section 232 國安關稅不受該裁決影響，仍在生效（一般性貿易背景，未點名 Walmart）","source":"Talk Business & Politics: The Supply Side: Consumer prices may remain elevated in 2026","url":"https://talkbusiness.net/2026/03/the-supply-side-consumer-prices-may-remain-elevated-in-2026/","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261019","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K 表示貿易政策（含關稅）的變動已對公司業務與利潤率造成影響，且 FY2026 期間因新增進口關稅已經歷這些影響。","source":"Walmart Inc. Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm","excerpt":"changes in trade policy, including tariffs, can impact, and have impacted, our business and profit margins","as_of":"2026-01-31","retrieved_at":"20261019","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"第三方對 10-K 的摘要稱：美國銷售中進口占比不到三分之一，主要來自中國、墨西哥、越南、印度與加拿大；Walmart International 約占 FY2026 合併淨銷售 19%。（二手摘要，未讀到 10-K 風險因素原文）","source":"搜尋摘要（第三方對 Walmart FY2026 10-K 的整理）","url":"https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm","excerpt":null,"as_of":"2026-01-31","retrieved_at":"20261019","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"10-K 載明美國 192 座、美國以外 179 座配銷設施，分布於非洲、加拿大、中美洲、智利、中國、印度、墨西哥（二手摘要轉述）。","source":"搜尋摘要（Walmart FY2026 10-K）","url":"https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm","excerpt":null,"as_of":"2026-01-31","retrieved_at":"20261019","affects":["moat_trend"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"報導（路透系，日期標示與內容不一致，期間需核實）稱中國占 Walmart 進口貨運量約 60%，低於 2018 年的 80%，仍為最大進口來源國；Walmart 稱提單資料僅反映部分採購；採購主管稱不能依賴單一供應商或地區。","source":"indiaseatradenews.com 轉載 Reuters 報導（Walmart shifts to India from China）","url":"https://indiaseatradenews.com/walmart-shifts-to-india-from-china-for-cheaper-imports/","excerpt":"I can't be reliant on any one supplier or geography for my product","as_of":"2026-07-05","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Mondaq 法律分析稱：2018 年第一屆川普政府 301 關稅是 Walmart 分散採購的催化劑；中國曾指控 Walmart 要求供應商吸收關稅；中國仍供應其多數電子、服飾、玩具（SAN 引路透）。","source":"Mondaq: Walmart's Diversification Of Sourcing From China","url":"https://www.mondaq.com/unitedstates/international-trade-investment/1794088/walmarts-diversification-of-sourcing-from-china-a-relationship-decades-in-the-making-so-breaking-up-is-really-hard-to-do","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261019","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 FY27：Walmart U.S. 營收約 $125.9B、年增 3.6%；可比銷售 +2.6%（含健康與保健約 80bps 拖累）；eCommerce +24%","source":"Walmart Q2 FY27 earnings release / beancount.io 分析（第三方轉述）","url":"https://corporate.walmart.com/news/2026/08/20/walmart-releases-q2-fy27-earnings","excerpt":null,"as_of":"2026-08-20","retrieved_at":"20261019","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 FY27：International 營收約 $35.6B、年增 12.8%（固定匯率 7.9%）；可比銷售 +4.4%（不含油）","source":"Walmart Q2 FY27 earnings release / beancount.io","url":"https://mms.businesswire.com/media/20260819458603/en/2879243/1/Earnings_Release_FY27_Q2.pdf?download=1","excerpt":null,"as_of":"2026-08-20","retrieved_at":"20261019","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 FY27：Sam's Club 淨銷售約 $25.71B、年增 8.8%，eCommerce +26%，營業利益 +44.3% 至 $678M；FY27 指引上調至固定匯率淨銷售成長 4.0–5.0%","source":"Retail Insight Network: Walmart raises FY27 outlook","url":"https://www.retail-insight-network.com/newsletters/walmart-raises-fy27-outlook","excerpt":null,"as_of":"2026-08-20","retrieved_at":"20261019","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"Numerator：Walmart 占美國食品雜貨 19.9%（截至 2026-03-31 之 12 個月），前兩年為 20%、20.4%；Costco 8.2% 上升；Walmart U.S. 食品雜貨 FY26 銷售約 $285B、年增 3.4%（FY25 約 4%）","source":"Grocery Dive / Supermarket News（Numerator 數據）","url":"https://www.grocerydive.com/news/walmarts-grocery-sales-growth-slows/818493/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261019","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"NRF 預測 2026 美國零售銷售成長 4.4% 至約 $5.6 兆；Moody's 預期實質消費成長放緩至約 1.5%；未找到折扣店專屬 TAM 或 2027 預測","source":"Retail Dive / Talk Business 報導 NRF 預測","url":"https://talkbusiness.net/2026/03/nrf-2026-retail-sales-forecast-to-grow-4-4-to-5-6-trillion/","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261019","affects":["thesis.R","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Walmart 與 OpenAI 合作讓消費者在 ChatGPT 內以 Instant Checkout 直接購買 Walmart 商品（代理式商務），Walmart 將其定位為成長機會而非威脅","source":"Walmart Ushers in 'Agentic Commerce' Through OpenAI Partnership（consumergoods.com）","url":"https://consumergoods.com/walmart-ushers-agentic-commerce-through-openai-partnership","excerpt":"allowing customers to shop directly through ChatGPT using Instant Checkout","as_of":"2025-10-14","retrieved_at":"20261019","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Walmart 2026-01 另與 Google 合作於 Gemini 建立商品探索與購買系統；Amazon 有 Rufus、Best Buy 2026-03 與 OpenAI 及 Google 皆有合作，AI 入口競爭同步升溫","source":"WebSearch 彙整（techradar／consumergoods 等）","url":"https://www.techradar.com/ai-platforms-assistants/chatgpt/walmart-gives-chatgpt-checkout-power","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261019","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"無人機配送競爭：Walmart 與 Wing 計畫 2027 年新增含費城在內七個城市、涵蓋 270 家門市；Amazon 亦擴張 Prime Air，Uber／DoorDash 也投入無人機配送","source":"Fortune, amazon uber doordash walmart drone delivery wars","url":"https://fortune.com/2026/08/21/amazon-uber-doordash-walmart-drone-delivery-wars/","excerpt":null,"as_of":"2026-08-21","retrieved_at":"20261019","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Walmart Q4 FY26 全球電商成長 24%，由店配取貨／配送與 marketplace 帶動；全年全球廣告業務（含 VIZIO）成長 46% 至近 64 億美元；會員費收入 Q4 全球成長 15.1%（二手摘要，數字出自 2026-02-19 財報）","source":"Walmart Q4 FY26 earnings release (Business Wire, 2026-02-19) via galvnews.com; Nasdaq/Zacks 'Walmart's Ad Business Jumps 37%'","url":"https://www.galvnews.com/walmart-reports-revenue-growth-of-5-6-up-4-9-in-constant-currency-cc/article_7296cd50-c87c-52a8-9cdc-a09b75eda9c7.html","excerpt":null,"as_of":"2026-02-19","retrieved_at":"20261019","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"廣告加會員合計占 Q4 營業利益近三分之一（Nasdaq/Zacks 分析）；Q2 FY26 marketplace 銷售成長 17%，約 44% 量經 WFS","source":"Nasdaq/Zacks, Walmart's Ad Business Jumps 37%: Margin Upside Ahead?; Zacks, Walmart's Marketplace Gains Speed","url":"https://www.nasdaq.com/articles/walmarts-ad-business-jumps-37-margin-upside-ahead","excerpt":null,"as_of":"2026-02-19","retrieved_at":"20261019","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FY26 Q1：全球廣告成長 50%（含 Vizio），不含 Vizio 為 27%，Walmart Connect 成長 31%；廣告加會員約占公司利潤四分之一；加拿大會員方案改名 Walmart+","source":"MarketingDive via 8thandwalton.com, 'Walmart's advertising business soars with Vizio integration'","url":"https://www.8thandwalton.com/?p=73315","excerpt":"Walmart's global advertising business grew 50% year over year in the retailer's fiscal Q1 2026, boosted by the integration of connected TV device maker Vizio. Stripping out Vizio, the ad segment was up 27% YoY; Walmart Connect, the retailer's U.S. retail media arm that does not yet include Vizio, increased ad sales 31% YoY in Q1.","as_of":"2025-05-15","retrieved_at":"20261019","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-20 Walmart 上調 FY27 全年指引：銷售成長 4%–5%（前 3.5%–4.5%）、營業利益成長 7%–8.5%（前 6%–8%）、EPS $2.80–$2.87（前 $2.75–$2.85）；raise 含關稅退款挹注，且燃料成本較原假設多逾 $20 億。","source":"TIKR blog；Adweek via ATDb（Walmart boosts full year guidance following 38% ads growth）","url":"https://www.theatdb.com/news/walmart-boosts-full-year-guidance-following-38-ads-growth","excerpt":null,"as_of":"2026-08-20","retrieved_at":"20261019","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-05-21 Walmart 維持 FY27 EPS 指引 $2.75–$2.85 不變；TIKR 稱當時投資人原期待上調。","source":"Benzinga earnings forecasts；TIKR（Walmart stock has gone nowhere in 2026）","url":"https://www.tikr.com/de/blog/walmart-stock-has-gone-nowhere-in-2026-heres-what-could-break-the-stall","excerpt":null,"as_of":"2026-05-21","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026 年 8 月財報：調整後 EPS $0.81 高於共識 9.3%；但下一季營收指引 $1,856 億較分析師預期低 1.4%（聚合站摘要，與全年指引上調並存；Benzinga 韓文頁另載 Q3 EPS 指引 $0.62–0.64 低於共識 $0.68，該頁文字破碎待核）。","source":"Webull 新聞摘要；Benzinga 韓國站 earnings-forecasts","url":"https://kr.benzinga.com/quote/WMT/earnings-forecasts","excerpt":null,"as_of":"2026-08-20","retrieved_at":"20261019","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"MarketBeat 2026 年 8 月初：36 位分析師共識「Moderate Buy」，平均 12 個月目標價約 $138.56（高 $155、低 $120），當時股價約 $111.85。","source":"MarketBeat WMT price-target 頁","url":"https://www.marketbeat.com/stocks/NASDAQ/WMT/price-target/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布因來源而異：Investing.com 40 位分析師平均約 $128.43（區間 $81–$155）；Benzinga 2026 年 9 月初 28 位平均約 $131；Walnut Invest 2026 年 8 月 41 位平均 $138.02。","source":"Investing.com consensus estimates；Benzinga price-targets；Walnut Invest forecast","url":"https://www.investing.com/equities/wal-mart-stores-consensus-estimates","excerpt":null,"as_of":"2026-09-05","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"個別券商：Bernstein 於 2026-07-31 將目標價降至 $142（維持 Outperform）；RBC 於 2026-07-22 維持 Outperform、目標價 $137。","source":"Walnut Invest WMT forecast","url":"https://walnutinvest.com/stocks/wmt/forecast","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#6","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Barchart 2026-07-29：39 位分析師共識「Strong Buy」（29 Strong Buy、6 Moderate Buy、4 Hold）；預期 FY27（至 2027 年 1 月）調整後 EPS 年增 9.5% 至 $2.89。","source":"Barchart: Are Wall Street analysts bullish on Walmart stock","url":"https://www.barchart.com/story/news/32179297/are-wall-street-analysts-bullish-on-walmart-stock","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#7","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Seeking Alpha 2026-03-19：下一財年 EPS 估計過去三個月 7 筆上修、26 筆下修；營收 10 筆上修、5 筆下修。","source":"Seeking Alpha WMT earnings revisions","url":"https://seekingalpha.com/symbol/WMT/earnings/revisions","excerpt":null,"as_of":"2026-03-19","retrieved_at":"20261019","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"FDA 於 2025-12-12 對 Walmart 發出警告信：已召回的 ByHeart 嬰兒配方奶在 21 州 Walmart 門市於 2025-11-12 至 11-26 期間仍上架；FDA 要求 15 個工作日內書面回覆，未回覆可能面臨查封或禁制令。","source":"FDA Warning Letters: Walmart Inc. (720400) 12/12/2025","url":"https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/walmart-inc-720400-12122025","excerpt":null,"as_of":"2025-12-12","retrieved_at":"20261019","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"Walmart 自願召回 Bettergoods 開心果醬一批（19 州），因 Florida 農業部在三罐中檢出沙門氏菌；Walmart 於 2026-07-17 得知；未通報病例。發布日期取自來源網址代碼（080426），未能獨立確認。","source":"Quartz: Walmart Bettergoods pistachio butter salmonella recall","url":"https://qz.com/walmart-bettergoods-pistachio-butter-salmonella-recall-080426","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261019","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"FDA 於 2025-12-12 對 Walmart 發出警告信：已召回的 ByHeart 嬰兒配方奶在 21 州門市仍上架約兩週；FDA 要求 15 個工作日內書面回覆。","source":"FDA Warning Letters: Walmart Inc. (720400) 12/12/2025","url":"https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/walmart-inc-720400-12122025","excerpt":null,"as_of":"2025-12-12","retrieved_at":"20261019","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"product_recall_warning#1","axis":"product_recall_warning","section":"events","direction":"-","claim":"Walmart 自有品牌 Bettergoods 開心果醬一批（19 州）因沙門氏菌召回；未通報病例。發布日期取自網址代碼，未獨立確認。另有 Bettergoods Alfredo 冷凍義大利麵因李斯特菌召回（日期未確認，未列入）。","source":"Quartz: Walmart Bettergoods pistachio butter salmonella recall","url":"https://qz.com/walmart-bettergoods-pistachio-butter-salmonella-recall-080426","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261019","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"WMT","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.23,"operating_margin_pct":4.39,"fcf_margin_pct":1.84,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMT","as_of":"TTM ending 2026-07-31（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"COST","period":"TTM ending 2026-05-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":12.88,"operating_margin_pct":3.82,"fcf_margin_pct":3.0,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COST","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TGT","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":29.3,"operating_margin_pct":5.59,"fcf_margin_pct":4.14,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TGT","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"AMZN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.25,"operating_margin_pct":11.52,"fcf_margin_pct":-0.49,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"DG","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":31.16,"operating_margin_pct":5.59,"fcf_margin_pct":4.61,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DG","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"WMT"},"financial_history":{"ticker":"WMT","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-01-31","revenue":611289000000.0,"revenue_yoy_pct":null,"gross_margin_pct":24.14,"operating_margin_pct":3.34,"net_income":11680000000.0,"diluted_eps":1.423333,"free_cash_flow":11984000000.0,"fcf_margin_pct":1.96,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-01-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-01-31","revenue":648125000000.0,"revenue_yoy_pct":6.03,"gross_margin_pct":24.38,"operating_margin_pct":4.17,"net_income":15511000000.0,"diluted_eps":1.913333,"free_cash_flow":15120000000.0,"fcf_margin_pct":2.33,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-01-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-01-31","revenue":680985000000.0,"revenue_yoy_pct":5.07,"gross_margin_pct":24.85,"operating_margin_pct":4.31,"net_income":19436000000.0,"diluted_eps":2.41,"free_cash_flow":12660000000.0,"fcf_margin_pct":1.86,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-01-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-01-31","revenue":713163000000.0,"revenue_yoy_pct":4.73,"gross_margin_pct":24.93,"operating_margin_pct":4.18,"net_income":21893000000.0,"diluted_eps":2.73,"free_cash_flow":14923000000.0,"fcf_margin_pct":2.09,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-01-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WMT/WMT_Q2_2027_Earnings_Call_20260820.md）

# Q2 2027 Earnings Call
**Walmart Inc.** | Earnings Calls | 2026-08-20

**Operator** (Operator):
Greetings. Welcome to Walmart's Second Quarter Fiscal '27 Earnings Call. [Operator Instructions]
I'll now turn the conference over to Steph Wissink, Senior Vice President, Investor Relations. Thank you, Steph. You may begin.

**Stephanie Wissink** (Executives):
Welcome, everyone. Joining me today from our home office in Bentonville are CEO, John Furner; and CFO, John David Rainey. We'll begin with highlights of the previous quarter and our outlook for the year. Then we'll open the line for your questions. During the question-and-answer portion, we've invited Seth Dallaire, our Chief Growth Officer; as well as segment leadership to join. Dave Guggina from Walmart U.S.; Chris Nicholas from Walmart International; and Latriece Watkins from Sam's Club U.S.
So we can address as many of your questions as possible, please limit yourself to one question. For additional detail on our results, including highlights by segment, please see our earnings release and supplemental presentation on our website.
Today's call is being recorded, and management may make forward-looking statements. These statements are subject to risks and uncertainties that could cause actual results to differ materially from these statements. These risks and uncertainties include, but are not limited to, the factors identified in our filings with the SEC. Please review our press release and slide presentation for a cautionary statement regarding forward-looking statements as well as our entire safe harbor statement and non-GAAP reconciliations on our website at stock.walmart.com.
That concludes my introduction. John, over to you.

**John Furner** (Executives):
Good morning, and thanks for joining us. I want to start by thanking our associates around the world. Their commitment to serving customers and members every day is what drives our business, and the results we delivered this quarter reflect their hard work. This is a good quarter for Walmart and shows once again that our strategy is proving out. We've been investing against it for years, and I'm even more bullish today as we see the pieces increasingly powering each other, a strong retail foundation alongside faster-growing businesses like marketplace, advertising and membership.
The math isn't simply 1 plus 1 equals 2. The value comes from how these businesses work together with each one strengthening the others and expanding what the company can do as a whole. And as these businesses scale, they become a more meaningful part of our mix and they're changing the shape of our business. We're accelerating growth and improving the overall economics of the company. The model is working, and we're confident in its power to drive durable long-term growth and shareholder value.
The underlying business continued to perform well in the quarter and was largely in line with our expectations, which assumed a slight moderation in sales growth from the first quarter. Overall, we continue to gain market share. We grew units and transactions and membership fee revenue was at an all-time high on growth of 17%.
We delivered another quarter of strong e-commerce growth, up 23% globally, including the 10th consecutive quarter of growth over 20% for Walmart U.S. And we also expanded the reach of platform businesses like Walmart+ and Marketplace to markets outside the United States, demonstrating how we're leveraging these for growth. And as we build and scale these capabilities across markets and begin to operate globally on the platforms we built during the last few years of transformation, we're seeing the same dynamic.
These businesses work together, deepen our relationship with customers and members, and create additional opportunities for growth and stronger economics. Our core retail business had another strong quarter with sales growth at the top end of our guidance, up 5% in constant currency. Comp sales for Walmart U.S. were 2.6%, led by transactions and Sam's Club U.S. delivered comps of 4.4%. International was up 7.9%, led by China and India.
For Walmart U.S., I feel good about how the underlying business is performing. The team delivered strong sales growth in categories like toys, pantry and fresh, and we continue to see growth from higher-income households. Changes in regulation around maximum fair pricing for certain drugs negatively impacted comp sales by 125 basis points. John David will share more about the makeup of the U.S. comp and talk to the additional color we provided in today's earnings presentation.
Turning to profits. Adjusted operating income grew 17.4% in constant currency. This includes the benefit from the receipt of tariff refunds in the quarter. And as we suggested on the last call, our intent was to deploy much of that back into price, and that's what we're doing. Importantly, our underlying profit growth was where we thought it would be, excluding this benefit. Because of our strong top and bottom line growth, we're raising our guidance for the year.
Now let me take a moment to talk about specific drivers of our growth. First, everything we do starts with serving customers and members as an omnichannel retailer. Core to that is delivering value and maintaining price leadership. As we said coming out of Q1, customers tell us they're still feeling some pressure, but it's clear. Customers are looking for value and convenience and they want things fast, and that's where Walmart shines.
Having the best prices across a basket of goods helps us continue to build trust with our customers and members by helping them save money at a time when many households are carefully managing their budgets. The Walmart U.S. team delivered more than 11,000 rollbacks during the quarter, up from 7,200 rollbacks at the end of the first quarter, demonstrating our commitment to price investment.
We're investing heavily in price because customers need us to and because we believe it drives market share gains over time. Our price gaps to conventional grocers here in the U.S. are strong, and they continue to widen. The share gains we see from this channel have persisted alongside the drug and dollar formats.
A second area I'd like to highlight is our ongoing strength in e-commerce. The sustained growth we've seen in e-commerce across the company over multiple years points to more than a digital success story. It's evident that customers and members increasingly choose Walmart because they know we combine low prices across a broad assortment with speed and convenience.
The mix of e-commerce for Walmart International is now 30% with strong growth again this quarter in China, India and Canada. Growth in Q2 was 19%. Sam's Club U.S. grew e-commerce 26% with delivery from club up triple digits following the launch of our 1-hour delivery back in April. Walmart U.S. delivered growth of 24%, Marketplace grew 52% and advertising was up 38%. We believe a factor in this growth is our ability to deliver with speed.
Customers and members around the world are getting superfast deliveries of baskets that include pharmacy, fresh, frozen, fashion and general merchandise, often in under 30 minutes. Fast delivery in the U.S. grew 48% for the quarter. Speed matters, and we have a significant competitive advantage. Our physical footprint, fulfillment infrastructure and local delivery capabilities allow us to move closer to customers while maintaining an attractive cost structure.
We've now expanded sub-30-minute delivery into 38 markets here in the U.S., giving millions of additional customers access to faster fulfillment. And speed isn't simply a fulfillment metric, it's an acquisition strategy. Customers who use fast delivery shop with us more frequently, they deepen engagement with us, and they're more likely to become Walmart+ members.
The advances we're making in speed of delivery create another reason for customers to choose Walmart for more shopping occasions. That's an important shift in how we think about growth. And as we become faster, we're not simply taking share within traditional retail categories, we're expanding the number of occasions where Walmart can serve customers like food delivery.
In the past, customers may have thought about Walmart primarily for groceries and general merchandise. Today, we're expanding beyond that. Meal solutions, prepared food partnerships like the one we announced with Subway and faster fulfillment allow us to participate in a much broader share of everyday food spending. This is an exciting opportunity, and we're just getting started.
The third area I'd like to highlight is our platform strategy. We're building capabilities that are increasingly scalable across markets. Marketplace, fulfillment services, membership, advertising and other commerce solutions are strengthening our business and they're improving the economics of the company. This quarter, we expanded our U.S. marketplace platform capabilities into both Mexico and Canada, and we launched Walmart+ in Canada.
Membership was also a highlight with double-digit growth for Walmart+ and strong growth for Sam's Club in the U.S., China and Mexico. We also gave a boost to our advertising business with the acquisition of Vibe. We believe Vibe expands our ability to help advertisers of all sizes reach customers through self-service tools while measuring results against real shopping behavior. Combined with Walmart Connect and VIZIO, this further strengthens our platform and creates value for customers, sellers, suppliers and advertisers.
These are important milestones because they demonstrate the value we're creating across the company. Rather than building entirely new capabilities market by market, we're increasingly able to build once, improve continuously and scale globally. That makes us faster and more efficient and allows customers in more markets to benefit from innovations developed anywhere across Walmart.
The fourth area is our supply chain. We've invested in automation, technology, fulfillment capacity and our physical network, and these investments are showing up in customer experience. They're allowing us to move inventory more efficiently, deliver faster, help with in-stock levels and support the growth of both our first-party and marketplace businesses. They also strengthen the economics of our omnichannel model. And as we improve density and utilization across our network, speed and profitability reinforce one another.
And you can see how these advantages build on each other. When we invest in our supply chain, it helps us get more products to our customers and members faster. When they get items faster, they shop with us more frequently, both online and in our stores. And as frequency increases, our suppliers and sellers want to be closer to the point of purchase, it's reinforcing.
Finally, let me talk about how AI is helping make Walmart faster, more convenient and personalized. We continue to take a people-led tech-powered approach. We're using AI to make our work easier and help our associates grow and be at their very best. We believe AI will improve nearly every part of our business by making shopping better and our associates work easier.
Sparky is a great example. The number of customers using Sparky is up 70% from last year, and the customers and members who use Sparky for shopping spend 40% more per order than others who don't. Someone recently shared with me that they asked Sparky for a weekly meal plan of healthy foods with high protein options. Within a few seconds, Sparky shared recipes and meal kits with the ability to add all the ingredients they need to their basket with one click.
Sparky even recognized the ingredients they had recently purchased, both online and store, so they didn't buy something they already had. It's building trust. When you step back, what encourages me the most is how these areas are increasingly connected. This isn't about any single driver. It's about building a business for each advantage reinforces the next.
With that, I'll close my comments where I began, and that's by thanking our associates. The progress we're making is possible because of the way they serve customers and members each and every day, the way they embrace new technology and the way they continue to find better ways to operate. I'm excited about the momentum we have, confident in the strategy we're executing and even more optimistic about the opportunities ahead.
With that, I'll turn it over to John David to walk through the quarter in more detail. John David?

**John Rainey** (Executives):
I'll echo John's sentiments. We're pleased with the way our business is performing, especially during the more recent operating environment that's been marked by some near-term macro crosswinds. Our business model is only getting stronger and more durable, and this gives us confidence to raise our sales and operating income growth guidance for the year.
With the tariff refunds, there are some idiosyncrasies to this quarter's results. So I'll provide a deeper view of the impacts and discuss how we're thinking about these factors looking into the second half of the year. First, I'll start with the financial and operational highlights. Enterprise net sales growth in constant currency of 5% was at the top end of our guidance of 4% to 5%, driven by growth in e-commerce, Sam's Club and China.
This quarter demonstrates the benefits of our diversified portfolio of businesses across channels, formats and markets. Global e-commerce net sales grew 23%, continuing the strong momentum of the last several years. Sam's U.S. and our International segment were both accretive to enterprise sales growth. Sam's comps were driven by a 7% increase in transactions with solid growth in unit volumes.
International constant currency sales increased nearly 8%, led by 9.7% growth in China. Walmart U.S. net sales increased 3.5%, including a comp sales increase ex fuel of 2.6%, slightly below our initial expectation due to lower health and wellness sales that were impacted by a larger headwind from maximum fair pricing. I'll talk more about this in a minute.
Enterprise adjusted operating income on a constant currency basis increased over 17% and adjusted EPS increased over 19%. This performance reflects the net benefit from the tariff refunds we received, partially offset by price investments in the quarter as well as improved incremental margins in our digital business with strength in high-margin commerce solutions.
Operating income growth included a net benefit of approximately 750 basis points related to tariff refunds received in Q2. Setting aside this benefit, underlying operating income growth was at the top end of our 7% to 10% guidance. Our outlook reflects the continued prioritization of the remaining tariff refunds in the customer experience and price investments in the second half. For this reason, I encourage you to consider Q2 and Q3 performance together to assess the underlying growth of the business.
I want to take a moment to further emphasize the positive progress we're making in our e-commerce businesses. Digital is driving our growth, customer spend and market share gains across all operating segments. As we deploy these digital capabilities outside the U.S., it allows us to move with speed from an operational perspective. From a financial perspective, this allows us to grow at a lower marginal cost.
Walmart U.S. e-commerce grew 24% in Q2 with over 40% sales growth in store fulfilled deliveries, 20% growth in average weekly customers and over 50% growth in marketplace sales. E-commerce growth was also strong at Sam's Club U.S., up 26% and our International segment up 19%, led by China, India and Canada. Sustained e-commerce momentum enables the growth of Commerce Solutions businesses, advertising, marketplace, data ventures and membership.
I'll start with global advertising, which increased 38%, driven by another strong quarter from Walmart Connect in the U.S. and Flipkart ads. Walmart U.S. advertising, including VIZIO, also increased 38%, led by strength in Walmart Connect, which was up 43%. The momentum in marketplace and fulfillment services continued this quarter with U.S. net sales up 52%. Nearly 50% of the marketplace business flowed through Walmart Fulfillment Services in Q2, an increase of nearly 400 basis points versus last year.
We're benefiting from a broader marketplace assortment that includes more of the key brands that customers want. Walmart Data Ventures continues to drive meaningful growth. Users value the platform's enhanced decision intelligence capabilities, which uncovered shared growth opportunities across Walmart's formats and markets. We announce today that we're extending the Scintilla platform to Sam's Club U.S. next year, addressing one of the top requests from our suppliers.
Rounding out our profit mix drivers, membership income grew nearly 17% globally. Sam's Club U.S. membership increased nearly 6%. This was driven by steady growth in member counts and Plus penetration. Sam's Club China hit new record highs in member counts, and we saw strong relative performance in our Sam's format in Mexico. We're especially pleased with the continued strong double-digit growth in our U.S. Walmart+ program, resulting in the best first half of membership growth in its history.
We are building what we believe can be the most essential membership program for consumers and excited for what's ahead. The thing that people sometimes overlook when reflecting on our membership program is the incrementality that we see on GMV. Our members spend approximately 4x more than nonmembers.
Turning to incremental margins. The profitability of our e-commerce business continues to improve. Our Walmart U.S. e-commerce business achieved double-digit incremental margins for the first half of the year. This was driven by continued strong ad and membership revenue, further densification of our delivery network, growth in fee-based fast deliveries, which represented an all-time high of 37% of store-fulfilled deliveries in the quarter. And lastly, the benefits of automation. 3,100 of our U.S. stores are now served with some level of automated freight, and we're processing over 50% of our e-commerce fulfillment volume through automated facilities.
Now I want to address a few areas in a little more detail. The first is the Walmart U.S. comp. To help understand the composition of our U.S. comp sales by merchandise category, we provided an additional disclosure in our supplemental slide deck, which is Slide 14. The chart on that slide shows Walmart U.S. comps, excluding the health and wellness category. Over the last 2.5 years, sales in our core categories have been extremely consistent, largely in the 3% to 4% range on a quarterly basis.
For outlier periods such as last quarter, when looking at a 2-year average, growth falls right into the middle of a similar 3% to 4% range. We expect core comps in a similar range in the second half. However, when looking at the Walmart U.S. total comps, including health and wellness, during each of FY '25 and FY '26, we realized 100 basis points of a tailwind from sales of GLP-1 branded drugs. In FY '27, the benefit from GLP-1 is expected to be roughly half that amount as script count growth is more than offset by price/mix headwinds.
New, in FY '27, we cited a 100 basis points headwind to total comp sales from deflation and brand to generic transfers under the first year of maximum fair price regulation. In Q2, this negative impact was closer to 125 basis points, and we've updated our estimate for FY '27 impact to be similar at 125 basis points.
Putting all this together, sales of core merchandise categories have been consistent. But at the total U.S. comp level, we've had nearly a 200 basis point net swing in comp sales growth from the trailing 2-year pace to this year, entirely tied to our health and wellness category. It's important to note that this unfavorable impact is to the top line only. We're pleased with the underlying performance and the profit contribution of our health and wellness business.
Next, I want to discuss in-store comps. They were down low single digits in Q2, consistent with the trend that began in late Q4 last year. This headwind is primarily driven by the negative impact from the health and wellness business, where the vast majority of the sales occur in store. The role of our stores has evolved as our model has changed. E-commerce sales now represent over 23% of our mix in Walmart U.S., which is double the level from just 5 years ago. The more omni we become, the more important our stores become, not less important, more important.
Between in-store shopping and digital fulfillment, we have more unit volumes transacted through our stores than ever before as they are the last mile fulfillment nodes for 80% of our e-commerce orders and 100% of our fast deliveries. As e-commerce profit margins continue to improve, we're becoming increasingly agnostic about channel dynamics while enabling customers to shop on their terms.
Next, I want to discuss the tariff refunds in a little more detail. As we shared with you in May, we were eligible for approximately $2.9 billion of tariff refunds, amounting to about 0.5% of annual U.S. net sales. To date, we received substantially all of these tariff refunds. As John mentioned, we've taken a disciplined approach to investing these funds back into customer experience and price leadership, prioritizing investment in grocery and general merchandise categories.
Looking forward, our Q3 guidance reflects the continued impact of pricing actions taken in Q2 alongside continued prioritization of tariff refunds and the price investment. We would encourage you to look at our operating income growth for Q2 and Q3 together to assess the underlying performance of the business.
Now I'll turn to SG&A. We leveraged wages in Q2 as we continue to improve productivity through increased usage of tech tools by associates in stores and streamlined inventory flow enabled by supply chain automation. More than offsetting these benefits were higher depreciation related to CapEx and increased self-insurance cost.
Inventory at quarter end increased 6% in constant currency, slightly higher than total enterprise sales growth. The increase reflects cost inflation as well as higher inventory to support strategic initiatives in the U.S., including the optimization of inventory across fulfillment nodes.
Turning to guidance. We have increased confidence in the long-term value drivers of our business. Our business is strong. E-commerce and related businesses offer compelling growth, and we are consistently generating strong incremental margins. We're raising our fiscal year sales guidance to 4% to 5% from 3.5% to 4.5% previously.
There are four assumptions worth highlighting. The first is this upward revision reflects the pass-through of first half performance, but also assumes slightly better second half sales versus our prior guide as price investments drive accelerated and sustained share gains. Price investments are an immediate benefit to customers that build value over time for the business.
Second, we're incorporating a larger headwind from maximum fair pricing within the Walmart U.S. business. Based on year-to-date experience, we now estimate the full year headwind to Walmart U.S. comp sales will be closer to 125 basis points.
Next, we expect Sam's Club U.S. and International to be growth accretive to the enterprise in both Q3 and Q4. Walmart U.S. sales growth is expected to improve in Q3 as the investment in customer value translates into stronger sales.
And lastly, the timing of Flipkart's Big Billion days will impact the cadence of Q3 and Q4 sales growth. This year, we expect a Q3 headwind of over 100 basis points to sales growth as we lap last year's event. We expect that Q4 sales growth will benefit by a similar amount for this year's event. Overall, for the enterprise, we expect sales growth in Q3 to be between 3% and 3.75%.
Regarding operating income, we're raising our full year guidance to 7% to 8.5% versus 6% to 8% previously. We expect the financial impact from the tariff refund receipts and reinvestment will be largely contained within the current fiscal year with the objective of driving sustained customer benefits and share gains in the second half and into future years.
Our guidance assumes that fuel costs persist at current rates. We now expect more than $2 billion of incremental fuel-related costs this year above and beyond our original guidance assumptions. We also expect costs related to the acquisition and integration of Vibe to be an approximate 20 basis points headwind to OI growth.
Inclusive of planned investment of tariff refunds, Q3 operating income growth on a constant currency basis is expected to grow 2% to 4%. Notably, a large portion of the refunds were invested at the end of Q2, so the full quarter impact of these investments is more pronounced in Q3. When looking at Q2 and Q3 reported operating income together, growth would average approximately 10% per quarter. We're raising our full year EPS guidance to $2.80 to $2.87 from $2.75 to $2.85 previously. For Q3, we expect EPS of $0.62 to $0.64.
I want to be really clear on this point. We're at the midpoint of our year, and we're raising our full year guidance to reflect confidence in our ability to sustain growth and share gains. Importantly, we're raising in the face of more than $2 billion of incremental costs tied to higher fuel prices and arguably a softer consumer environment than in February when we introduced our initial outlook.
As such, we feel it's prudent to remain cautious by only raising the guide modestly. We now expect slightly higher CapEx for the year at approximately 4% of annual net sales. Even with this increase, we expect to generate double-digit growth in free cash flow this year.
In closing, our teams continue to focus on what we do best, serving customers and members with everyday great value, exceptional convenience and speed, all while pushing our business model forward, diversifying our profit mix and leading in agentic experiences.
We're now happy to take your questions.

**Operator** (Operator):
[Operator Instructions] And our first question is from the line of Kate McShane with Goldman Sachs.

**Katharine McShane** (Analysts):
We wanted to focus our question this morning on the tariff refunds and price investment. With your most recent incremental pricing investments, I know you mentioned you're expecting a slightly better second half as a result. But have you already started to see an acceleration in units? And just given the price investment is such a focus in the market, can you talk about vendor support versus how much Walmart is investing? And how do you sustain these lower prices and lap this investment in 2027?

**John Furner** (Executives):
Kate, thanks for the question. This is John. Let me just start by saying I'm really pleased with the quarter for Walmart. This is a good quarter of 5% in sales and strong operating income growth. We've been investing, as you know, in the last few years in the strategy to drive a very powerful omni business, and we're proud of the progress. I've been a part of building the strategy for a year, and it's great to see it come together. We want to be really flexible for customers, whether they shop at the counter or at the curb or delivery to their home.
Customers are looking for value, and our team is executing that well. We had a good quarter in Walmart U.S., International and Sam's Club. And the result of that is we have seen share gains, and we're pleased with share gains across the business. There was an impact in pharmacies as we talked about from MFP. Putting that aside, the third -- the second quarter, excuse me, for Walmart U.S. is the best second quarter we've had in the last 3 years. So we're proud of the performance.
And as all these pieces come together, whether it's marketplace, advertising, our membership businesses, it's important to recognize that these businesses work together, they're reinforcing and they further develop our ability to serve customers with value. So on price specifically, as John David mentioned, we invested in price in the second quarter.
We talked about at the end of the first quarter that customers are feeling some pressure. So we're proud of our investments. We're very thoughtful about those investments, the categories they went in, the timing of those investments, and we'll manage them across the two quarters.
Our merchants have a lot of experience delivering value, mixing out. They're doing this in a way that, as I said, results in share gains. So we're really pleased with the share gains that we saw in the food categories. And those type of share gains tend to be durable over time.
So specifically, as we look forward, if you take the two quarters, you put those together, we're pleased with our forecast in terms of sales. We're pleased with the forecast in terms of operating income growth. You heard John David mention what those two are. And our purpose and mission is always to save people money and live better, and that's what we'll continue to focus on, and we'll do everything we can to keep prices as low as we can for customers throughout the rest of the year.

**Operator** (Operator):
The next question is from the line of Simeon Gutman from Morgan Stanley.

**Simeon Gutman** (Analysts):
So I guess I have two parts. The first is the lower-income consumer has faced pressures for the better part of several years. Is there anything different even about this environment with gas prices that you think has accumulated to weigh on them further?
And then it's related to the prior question, and I think some of John David's prepared remarks, the elasticity function to some of these price investments and rollbacks. I know you've mentioned you see it immediate. Can you give us some context? And then is there traditionally a little bit of a lag where you start to see a more -- I guess, more impactful response over the next, call it, 6 months?

**John Rainey** (Executives):
Simeon, this is John David. Thanks for your question. We, no doubt, and it sort of states the obvious of seeing some incremental pressure on the consumer relative to the beginning of the year with higher fuel prices. As you go through month by month in the last quarter, you can tell when fuel prices increase and got above $4, and perhaps there's a psychological impact to that, that there are choices that consumers are making. So June was a little more obvious as we look at the quarter in terms of customers making trade-offs. And it's why we have leaned so heavily into lower prices.
You're right, there is elasticity on these items that we roll out. We talked about 11,000 rollbacks. We're really proud of that, and how we're trying to be there for our customers and members during this period of time. But I think very importantly, in your question, there is a lag to this. There is a bit of a cumulative benefit that comes when you lower prices. And so you don't necessarily expect to have that offsetting benefit to the lower prices in the immediate period.
And so as you know, being very familiar with our business, we're not managing our business for one quarter. We're managing our business on a multiyear basis to play to win. We feel confident in our strategy and what we're doing here. And importantly, the market share gains that we've seen in these recent periods, they're durable. We're seeing that we're keeping those market share gains. And that's why I think we've been perhaps as bold as we have to continue to go after that.

**John Furner** (Executives):
And Simeon, with the rollbacks and the other investments, we exited the first quarter, as we mentioned earlier, at about 7,000 rollbacks. It's normally about 5,000. At the end of the quarter, we had 11,000. And when you take rollbacks in consumable categories like food, you tend to see first a unit increase, and we saw transactions and units grow in the quarter. And then that does create a temporary deflationary effect. But as the units grow over time, particularly in food, then the share gains come through. And we were really pleased with the recent share report in food. It's one of the strongest reports we've had in some time.
So we're pleased with those. But again, we'll handle this thoughtfully. Our hope and intention always is that rollbacks can become permanent price increases wherever possible. We have the line of sight to those. And for any that we see that we aren't getting return and we'll manage them carefully. We want to be thoughtful about how we invest all of our funds and all the funds available. Ultimately, we're trying to reinforce the everyday low price model and save customers' money.

**Operator** (Operator):
The next question is from the line of Greg Melich with Evercore ISI.

**Gregory Melich** (Analysts):
I'd love to follow up on where you're seeing tariff rates going forward. Are the effective rates under the new sections coming in at higher or lower than IEEPA? And then my follow-up is on the baseline into '27. Should we think about operating income still growing up to 2x sales as we see the traffic results from the price investment?

**John Rainey** (Executives):
The assumption that we have with respect to tariff rates is basically at the level that we're experiencing today, stands true for where fuel prices are as well. So if there's some improvement in fuel prices, I think that's a benefit to our forecast. On operating income for 2027 and the outer years, look, we have a lot of confidence in our ability to continue to grow the bottom line at a much faster rate than we have the top line. But I don't want to miss the top line growth, too, to have what is roughly $0.75 trillion of a revenue base and be able to grow at 4%, 5%, 6% a year, that's meaningful growth.
What's notably different, though, is how profitable that growth is. And so let's step back for a second and just think about the U.S. comp. U.S. comp is at 2.5%. I think the right way to think about that is really more 3.5% when you adjust for health and wellness. But just take at face value, a 2.5% U.S. comp. We grew operating income 10% ex tariffs. That's 4x the level of revenue growth. We haven't done that level of profit growth relative to the U.S. comp in 2 decades. Our business is fundamentally changing.
If you look at the profit drivers of our business, almost half of the growth came from areas like membership, advertising, marketplace. And we expect this to continue. In fact, I think there's line of sight to seeing improvement in incremental margins as we go forward. Right now, we're generating roughly double-digit, low double-digit incremental margins. But the growth drivers of our business are as intact as they ever have been.

**Operator** (Operator):
The next question comes from the line of Brad Thomas with KeyBanc Capital Markets.

**Bradley Thomas** (Analysts):
I want to ask about the health and wellness category and appreciate all the detail you shared this morning. It's really been an outsized contributor to growth over the last few years and still seems to have a bright outlook. I was hoping you could speak to that multiyear outlook and maybe how to think about the impact of fair pricing, particularly as we look out over a couple of years here?

**John Furner** (Executives):
Brad, as we mentioned, there definitely has been an impact in prior years. It was a tailwind and it was a headwind in the quarter. That's on Slide 14 in the supplemental materials so that we can provide the transparency we can. But we do not want to at all signal that we are unpleased with the health and wellness business. Lower prices help over the long term. We have a legacy of lowering prices in pharmacy back to the $4 generics, which has been exciting. But I'm going to have Dave talk about the business overall. We're really energetic about not only the underlying performance of health and wellness, but health and wellness customers, pharmacy customers, they spend more. And I think there's some really important detail that Dave is going to add.

**David Guggina** (Executives):
Absolutely, John. We feel very good about the underlying momentum in the health and wellness business. Prescription volumes continue to grow. We're gaining market share and customers are responding strongly to the convenience that we're building around pharmacy. I do want to highlight health and wellness, this customer cohort is incredibly important for us. When someone becomes a health and wellness customer, they spend on average 3x more than the average Walmart customer.
And when they begin using pharmacy delivery in addition to being a health and wellness customer, that almost doubles yet again. So we have a very unique opportunity to connect our pharmacy expertise, our digital capabilities and our local fulfillment network to make health care more convenient and accessible while deepening our relationship with these customers.

**Operator** (Operator):
Our next question is from the line of Michael Lasser with UBS.

**Michael Lasser** (Analysts):
You articulated a lot of confidence that the Walmart U.S. comp is going to accelerate as the lagged impact from these price investments start to gain traction. So a, have you already started to see that? And b, if that does not happen, what are you thinking about in terms of incremental price investments from here in order to drive the top line as you move not only into the back half, but also into 2027, especially as the benefit of all these tax refunds fade?

**John Furner** (Executives):
Michael, first, everyday low price is a philosophy that builds trust with customers, and we're proud to offer a value on a basket of goods that's predictable. It's consistent over time. So when we have the opportunity to lower prices, of course, that is always going to be our bias to do that. But we always need to balance our price investments relative to what we're seeing in the market and with the commitments we made on our forecast, including operating income over time. So we'll continue to work through those.
I do think it's also important to step back and just think about the business model in total. John David mentioned the growth in things like membership, advertising, data, fulfillment services. We built a much more durable and resilient model that gives us optionality over time. We're proud of our price gaps. Of course, we'll defend those. We're proud of the rollback count we have. The rollback count, as we mentioned, started really late July. July was a stronger month. In the month of June, we're pleased with the way back-to-school and back-to-college have started.
So we'll monitor over time, and we have a great merchant team that will, of course, mix out categories, and we'll look at these investments carefully one at a time. Ultimately, we want to do -- what we want to do is like what Dave said in pharmacy. We want to have a business that you can depend on whether you're shopping at the counter, you're shopping at the curb, you're shopping at home, and we want to provide the most flexibility we can for our customers.

**Operator** (Operator):
Our next question is from the line of Chris Nardone with Bank of America.

**Christopher Nardone** (Analysts):
Can you refresh us on the messaging around incremental margins coming out of your digital business given the momentum we're seeing there? And then as we think ahead to next year, how should we think about your plan to lap these rollbacks and price investments you are making today and still make sure you're driving consistent traffic to your stores?

**John Rainey** (Executives):
Chris, I'll take that. Let me start with the second part of your question. Lapping 19% EPS growth next year will be a challenge. So again, like, we're managing our business on an annual, if not a multiyear basis, but feel really good about what's in store for the next year and the years to come. But on the incremental margins, which as I noted kind of in my previous answer, I think that's a big part of the story for us. We just -- we continue to see these growth areas of our business that are driving more benefit to the bottom line.
We've not really committed to any certain number around the incremental margins in our business. But if you look back over the last, call it, 6 quarters or so, generally, U.S. e-commerce incremental margins have been in that high single-digit to low double-digit range. A couple of quarters ago, I was asked a question about the opportunity for that to improve.
And over time, I think I was maybe a little bit more guarded at that point. But when we see things like our advertising business that continues to grow at a 40% clip on a much higher base, that actually gives us confidence in the ability to maybe see incremental margins even go higher. And so like what do you have to believe to have incremental margins go higher? Well, advertising growth would need to outpace our e-commerce growth. And that's actually what we've been seeing and not by a small margin, by a large margin on a larger base.
And with the acquisition of Vibe, this gives us a new addressable market that we didn't have before in these small- and medium-sized merchants. And so we're very excited about the opportunity there. Advertising, though, is just one aspect of what we're doing. I don't want to solely point to that as the only opportunity that we have here as we continue to add businesses that complement the diversified portfolio of offerings that we have today that generate these higher margins, it's very attractive to us.
The key benefit of digital growth is being able to grow at a very low marginal cost. John has talked a lot since he's come on about this platform approach that we're taking. We're doing all the same things that we're doing in the U.S. and our other markets around the world. Mexico is a really good example. We look at Mexico today, and it's the same playbook that we implemented in the U.S. 5 years ago. And we're super excited about some of the early progress that we're seeing there. So we think we have a tremendous opportunity to continue to change and see our margins drift up over time.
Last thing I'll say on this. Obviously, I have some passion around this point. But it's not just that our incremental margins are growing, they're growing at twice the rate of the overall margin of the business. And I think that shows sort of how the earnings complexion of our business and the durability of that growth that we have will play into the future. So very excited about it.

**Operator** (Operator):
The next question is from the line of Christopher Horvers with JPMorgan.

**Christopher Horvers** (Analysts):
So if you look at the category performance relative to 1Q in the Walmart U.S. business, grocery continue to grow that mid -- strong mid-single digits, well above the market. And it was Gen Merch that actually slowed. So could you help us think about how much of that slowdown in Gen Merch was stimulus-related versus gas prices affecting that lower-end consumer? And then if you look back over the past few years, you've seen a consumer that has shown up around events. And to what extent have you seen the impact of back-to-school start to drive some lift in that Gen Merch business even considering where gas prices sit today?

**John Rainey** (Executives):
Chris, why don't I start and then maybe hand it over to Dave for a little more color. I think no doubt, the first quarter benefited from the stimulus payments related to tax refunds. And we acknowledge that on the last call. It's tough to determine how much you ascribe to what's going on in your business versus the overall macro environment, but I think we definitely benefited some from that. And then as we go into the second quarter, we saw gas prices peak at higher prices than what we saw in the first quarter. I think all of that impacts the results. But again, when you look at the core business and the fact that our value proposition, I think, is as strong as ever, we feel really good about how we're performing and what the outlook is.
Back-to-school, back-to-college. Back-to-school for much of the country is about a week later this year. So it's probably a little early to conclude anything on that. But I will say that back-to-college has gone exceedingly well. Like we're really pleased with what we're seeing there. You asked about general merchandise categories like we have right now, like one of the brands that we're selling, private brand item is Wonder Nation for kids. It's the largest kids fashion brand in the U.S. today.
So like we love our offering. We certainly recognize that the share gains that we're getting, notably from higher-income consumers are in part because of the assortment that we have. And that was part of the reason that our inventory went up. The fact that we've got more elevated brands, more expensive merchandise that appeal to a broader cohort of customers is affecting our business and our results. Dave?

**David Guggina** (Executives):
Yes. John David, what I would add is we're very pleased with the team's progress in general merchandise. We are seeing strength in style. We're seeing strength in trend. We're seeing strength in fashion and toys. In fashion, I'm really excited about some of our private brands, Scoop, Free Assembly. We're seeing triple-digit comps in those areas. When it comes to back-to-college, decor outperformed across the back-to-college home business. Areas to call out would be candles, throws, rugs, and lamps. Those all posted double-digit and triple-digit comps.
And then when it comes to back-to-school, as John David mentioned, this is where we shine. Walmart sells roughly 50% of total industry school supplies from a unit standpoint over the season. And we're very pleased with where we are at this point in the year. Customers are responding to just absolutely fantastic investments in price. We have a list of 14 key items that are priced less than what we saw in 2019. Great examples are Pen+Gear crayons for $0.25 or our Pen+Gear No. 2 pencils for $0.92. And those prices are resonating with customers, and we're seeing it in traffic, ticket and unit volume all growing.

**Operator** (Operator):
Our next question is from the line of Krisztina Katai with Deutsche Bank.

**Krisztina Katai** (Analysts):
So I also wanted to focus on the price investments from a return perspective, right? You noted 50% sequential increase in rollbacks, I believe, 11,000 items, which might be a new record for Walmart. So I wanted to ask if you could speak to the performance of the incremental rollbacks, the metrics and the payback period that determine whether an investment becomes permanent. And maybe just frame up for us just if you can, just how much of the current rollback portfolio is meeting those return thresholds?

**John Furner** (Executives):
Krisztina, throughout the year, we have stated that our intention would be to invest in price where possible and any refunds that we had, we would prioritize price investments, and that's what we did in the quarter. Categories as an example like the meat department, prices have been higher, and we know that customers have needed relief. So we invested in ground beef and other areas that were really important to the customer.
We'll watch those over the course of the time, but rollback has a start date and has an end date. We'll watch the unit movement. We'll understand the effect on the category. Importantly, the result is we're seeing share gains and share gains are ultimately the way we would judge how we're doing relative to the other businesses that are out in the market.
In terms of the quantity, I don't know if it is the highest ever, but it is a high number. It's the highest I can remember at least in recent times. And it is a reflection of the work that the merchants have done. It's a reflection of where we're in the market, and it's a reflection of the funds that we had available to be able to invest in price.
The timing of those were late in July, and they will continue into the second quarter. And that's why, as John David mentioned earlier, you should think of the second and third quarter together in terms of both sales and operating growth, and we'll measure it appropriately.
We're not investing just for the sake of doing it. We're doing this because we think it has a lasting durable impact on the way customers perceive us. And what we're trying to do ultimately with everyday low price and rollbacks is drive trust. It's probably a bit too early to call how many of these will be permanent. We'll manage that, and we'll work with our suppliers to determine where that's possible.

**Operator** (Operator):
Our next question is from the line of Bob Drbul with BTIG.

**Robert Drbul** (Analysts):
Just a couple of questions around, I think, inventory. Are there pockets of concern on your inventory levels at all? And you mentioned inflation impacting the inventory. Can you just also address like your inflationary expectations for the remainder of the year throughout the business?

**John Furner** (Executives):
Bob, generally, we've seen a pretty low inflationary environment throughout the year. We're between 1% and 2% in total. And the rollbacks, we think, can help over this quarter and the last few months. So generally not any big concerns right now on inflation. Fuel costs are probably the one thing that, of course, we're watching because of the magnitude of it. And hopefully, those can come down over time.
On inventory, it's something we watch really carefully. I've been in the company over 33 years. I've been a merchant and operator, and it can drive so many things from sales to markdowns, cash flow, as you know. When you step back and look at the categories, and I'm going to talk about Walmart U.S. just for a second because that's the majority of our inventory, the merchandise areas are in good shape. We're up anywhere from 1% to 4%. We have some investments in forward deployment. Fuel costs are a bit higher, so that's inflated, and we have some manufacturing and inventory.
But when you look at the categories, most are between 1% and 4%. The only thing that's at the high end is consumables, which is fast moving. So as we sit here today, I don't have any big concerns about inventory. If anything, there were a couple of categories, I think, in June and July where we were a bit light on inventory. We'll manage that, and we'll react appropriately based on what we're seeing from customers.

**Operator** (Operator):
The next question is from the line of Kelly Bania with BMO.

**Kelly Bania** (Analysts):
I wanted to just circle back on the topic of tariff refunds. And curious just how you are communicating this to your customers and membership base to ensure you're generating the ROI that you expect from these investments? And are you seeing others across the retail spectrum also reinvest those? Or do you expect them to also follow suit?
And if you can also include just the thought process about kind of allocating those investments between grocery and general merchandise, presumably generated on the general merchandise side, but it sounds like some going into the grocery side of the store. So just more details on the tariff refunds.

**John Furner** (Executives):
Kelly, we've invested across the business in the store today, store being the site and the physical store. You'll see a combination of rollbacks across food, general merchandise, consumables, fashion. There were some seasonal rollbacks. There are other items where there are ongoing replenishable items. So we always try to invest in a mix. We're not trying to take the investment and heavily weight it to a certain category. We know customers are looking for a variety of things across the basket.
At a time like back-to-college and back-to-school, as you heard from Dave earlier, we think about decor and upfitting a dorm, then there's the school supplies, the school lunches. And so you'll see it throughout the store. The signing in the store, we feel great about. The stores are doing a really good job signing it.
And then on our homepage, you'll see at the top left, the first -- one of the first titles right there on the top is rollbacks and more. It's always present. So we'll continue to communicate value any way that we can. We're proud of the reductions, and it's helpful for customers as we get into the back half.

**Operator** (Operator):
Our next question is from the line of Paul Lejuez with Citigroup.

**Paul Lejuez** (Analysts):
Just on the price investments, could you just talk about how that's framing your comp assumptions from a traffic versus ticket perspective in the second half? Sorry if I missed that earlier. Also curious on the OpEx growth in the U.S. was up 7%. Were there any timing shifts that impacted that? Are the liability claims coming in a bit above what you thought? Just curious how we should think about that line item and how it will grow in the second half of the year.

**John Furner** (Executives):
Sure. Let me take the first part on the composition of the comp. It was positive to see. It was great to see in the quarter that we grew in transactions. That's true at Walmart, true at Sam's Club. It's true in international. So we see customer traffic growing around the world. We also had positive unit growth. And both of those combined, that's -- they're really the two things we talked about on a weekly basis.
We start every Monday around the world in markets with something we call our trade meeting, and we talked about customer sentiment and how many customers we were able to serve, how many new customers we met, the units that we grow. So we look at both of those.
When you make investments in categories like we did across all the SBUs, you tend to see faster sales in categories like general merchandise in terms of dollars in food and consumables. You take the prices down, the prices then are lower than they were, you see units grow. And then over a few weeks or a few months, that's when you start to see the more lasting impact in food and consumables.
Your shoppers don't necessarily buy more food because they see lower prices. But over time, what we're trying to do with rollbacks and low prices is build trust with customers. We want customers to know they can trust us for a low price on a basket of goods over time, deliver the way they want, whether it's at the curb, it's at the counter or it's at their home.

**John Rainey** (Executives):
Yes. Paul, on SG&A, let me address that in a couple of parts. One of the bigger drivers was depreciation. Depreciation is related to the CapEx that we've had has really been around supply chain automation and addressing speed. And look, we are really pleased with the results that we're seeing. Just in the current quarter, the number of units that we delivered in less than 30 minutes doubled from a year ago. 70% of all of our e-commerce orders are delivered same day or better. That doesn't come without the investments that we've made. So like we're really pleased there.
We did have some pressure on what we're calling some of the self-insurance items. And the two categories that I would put in there are claims, as you asked about, but also group health. And if you take the first half of the year, about 2/3 of the increase is from group health. And what's happening there is our attrition has gone down quite appreciably in some cases. And by the way, this is a really good thing for our business. We want more seasoned, tenured associates serving our customers and members.
But with attrition going down, the number of enrollees in that plan has increased. So given the size of company we're, we've seen a little bit of pressure there. The last thing I'll say is from any quarter to one to the next, sometimes you lean in a little bit more to investments in the business. And while I did not call that out in my prepared remarks, I think this quarter falls into that category where we felt like it was prudent to make some of those investments that hopefully benefit the back half of the year.

**Operator** (Operator):
Our next question is from the line of Zhihan Ma with Bernstein.

**Zhihan Ma** (Analysts):
I wanted to follow up on the Walmart U.S. brick-and-mortar comp. And I appreciate the comment that you were saying there's a bit of a pharmacy headwind in there. Also wondering if you're seeing any impacts from higher gas prices and people may be driving less to stores and maybe the greater adoption of pharmacy delivery. Just trying to parse out how much of that is maybe some transitory impact versus a more structural shift in the channel.

**John Furner** (Executives):
So let me start with the first part on the stores. And I want to be really clear, stores are an asset. They certainly have an impact on handing back the quarter because of pharmacy, which weighs heavily on the store comp. The majority of the business is in store. But we're really pleased also with the delivery of the business. But when you step back and you think about stores and their role in the omni business, they are an asset because they position inventory, they position associates within 10 miles of 95% of the country. So the things you've heard this morning about fast delivery, accuracy, flexibility, shopping any way you want, they wouldn't come to life without our stores.
Now historically, if you go back a few years, we had a store channel, we had an e-com channel. They were independent. They were vertical. So you could look at where you sold, the cost of each, we can measure profitability of each. But as we blended those together, what we're trying to do is say, think of us in terms of the top line, the bottom line, we'll manage the middle and we'll be flexible for customers any way we can. And then the way that these get categorized, it's really where you decide to pay.
If you pay on your phone for pickup, it's an e-commerce order, and it's not a store order, but the store does the work. The store fulfills it. A fast delivery under 30 minutes, what you're actually doing is you're paying on your phone and you're having someone go shop for you and bring it to you, the store is fulfilling that inventory.
So just again, stepping back and thinking about stores, there is more volume going through stores today than there ever has been and it's growing. As a former store manager a couple of decades ago, I'm just in awe of all the things that the stores are doing to serve customers. They have so many things going on. They're executing, they're flexible, and it is a really important part of the overall business.
We'll watch all the channels. We'll make sure the store experience is great. We're investing in new stores. We're investing in remodels and are investing to ensure that the stores are omni-enabled so that they can be support and provide whatever we need for the e-commerce business.

**Operator** (Operator):
The next question is from the line of Seth Sigman with Barclays.

**Seth Sigman** (Analysts):
I wanted to follow up on the Walmart U.S. comp. So when we look at the average ticket, it does seem like it's running a little bit below inflation now, and that's been happening for the last couple of quarters. I realize a lot can contribute to ticket, but how is the composition of the basket changing? Are you seeing trade down? Are you seeing any big category mix shift? Are you seeing a shift to maybe smaller ticket items? Anything transitory? How would you sort of frame that?

**David Guggina** (Executives):
Yes. We continue to see broad-based share gains across many categories. Our strategy is working, and therefore, we're gaining share. In grocery, sales increased mid-single digits with strong unit volume growth and continued market share gains, as I noted. Areas that I'd call out in that business. One, we use some of the investments, refunds that we got to invest into the grilling basket this summer, which fed 8 people for under $40 with 13 of those items priced 16% below last year.
We're also offering incredible quality for great value with our bettergoods brand, which is now a $1 billion brand for us. And then to go back to back-to-school, we're bringing food into that play as well, including a new back-to-school lunch basket with 10 high-protein lunches for under $2. So that's just an example of a space where we're gaining traffic, we're gaining ticket size and units are going up, and those investments are driving that momentum.

**Operator** (Operator):
At this time, we've reached the end of our question-and-answer session. I'll turn the floor back to management for closing remarks.

**John Furner** (Executives):
Yes. First, again, I want to thank our associates for the work they did in the quarter and the things they do for our customers every day, and I want to thank you for taking the time and interest in the company. And I'll just close where I started. This is a good quarter for Walmart. Sales were over 5%, operating income up 17.4% without the benefit of the refunds. It was another strong quarter. I feel great about the way we're positioned.
We've been investing in a strategy that delivers an omni business model across markets. I'm really excited about the extension of platforms into the international businesses. There's a lot of progress. The teams are moving with speed. And when you just step back and look at the business that we have and the business we're building, it's very durable. It's reliable. There are a lot of things that we can do we couldn't do in years past.
Another strong quarter in e-commerce, another strong quarter in marketplace, advertising. We're seeing more and more people choose Walmart+, and it's exciting to see Walmart+ launch in Canada. So over time, I am more optimistic than I have been about the business model, and I look forward to continue to see all the pieces come together as we move forward. Thanks again for your time and interest in Walmart.

**Operator** (Operator):
Ladies and gentlemen, thank you for your participation. This does conclude today's teleconference.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### WMT_Q1_2027_Earnings_Call_20260521.md
- 2026-05-21｜CFO｜guidance：重申全年固定匯率營收成長 3.5%–4.5%，因 Q1 與 Q2 展望預期落在區間上緣（原話："we expect full year sales"）
- 2026-05-21｜CFO｜guidance：Q2 營業利益固定匯率成長 7%–10%，重申全年 6%–8%（原話："we expect growth of 7% to 10%, and we're reiterating our full year guidance of 6% to 8% growth"）
- 2026-05-21｜CFO｜guidance：Q2 EPS 與全年 EPS 指引區間（原話："For Q2, we expect EPS of $0.72 to $0.74 and full year EPS in the range of $2.75 to $2.85."）
- 2026-05-21｜CFO｜guidance：指引不含 IEEPA 關稅退款；管理層估可得最大退款不到美國年銷售的 0.5%（原話："our guidance does not assume any impact from IEEPA tariff refunds"）
- 2026-05-21｜CFO｜guidance：現行匯率下 Q2 營業利益成長有約 130bp 匯率順風（指引以固定匯率計）（原話："approximate 130 basis point benefit to operating income growth for Q2"）
- 2026-05-21｜CFO｜guidance：Q1 營業利益成長預期為全年最低，之後改善；管理層稱仍如此認為（原話："profitability would improve thereafter. We still"）
- 2026-05-21｜CFO｜margin：Q1 吸收約 1.75 億美元、約 250bp 營業利益成長的額外燃料成本，調整後營業利益成長約 5% 符合指引（原話："We absorbed approximately $175 million"）
- 2026-05-21｜CFO｜margin：Q1 品類組合 18 季以來首次對 Walmart U.S. 毛利率擴張（29bp）有正貢獻（原話："Q1 marked the first time in 18 quarters that merchandise mix contributed favorably to Walmart U.S. gross"）
- 2026-05-21｜CFO｜margin：管理層預期下一季品類組合改善幅度不會與 Q1 相同，並稱非每季都線性向上（原話："It's not directly up and"）
- 2026-05-21｜CFO｜margin：美國電商增量利潤率約 12%（原話："U.S. eCommerce incremental margins, in particular, were about 12% in the quarter."）
- 2026-05-21｜CFO｜margin：廣告與會員費合計約佔營業利益三分之一（執行長另稱廣告、會員費、約占三分之一）（原話："those 2 combined"）
- 2026-05-21｜CFO｜margin：Q2 營業利益成長有去年理賠費用墊高基期的小幅順風（原話："We're also lapping 2Q last year where we had higher claims"）
- 2026-05-21｜CFO｜margin：自有品牌滲透率下降約 40bp：食品降逾 100bp（主因雞蛋），GM 升近 200bp（原話："Overall, private brand penetration was down about 40"）
- 2026-05-21｜CFO｜margin：最高藥價（MFP）立法對 Walmart U.S. 可比銷售造成約 100bp 逆風（原話："comp sales, which were up 4.1% despite a 100 basis point"）
- 2026-05-21｜CFO｜risk：若燃料成本維持高檔，預期 Q2 與下半年零售價格通膨略高（原話："we'd expect somewhat higher retail price inflation in Q2"）
- 2026-05-21｜CFO｜risk：低所得消費者較謹慎；燃料站平均加油量 2022 年以來首次低於 10 加侖（原話："fell below 10 for the first time since 2022. That's an"）
- 2026-05-21｜CFO｜risk：承認 Q1 一般商品表現部分受較高退稅助益（原話："there were probably some tailwinds in the"）
- 2026-05-21｜CFO｜risk：管理層承認公司不免疫於總體經濟衝擊（原話："But we're not immune. We're not bulletproof to"）
- 2026-05-21｜CFO｜risk：雞蛋通縮對 like-for-like 通膨造成近 100bp 拖累，後續基期墊高將使通膨數字上行（原話："Egg deflation for us, lastly, contributed probably to about almost"）
- 2026-05-21｜CFO｜risk：關稅與燃料假設維持與目前相同環境（原話："we're generally assuming the same environment"）
- 2026-05-21｜CFO｜capital_allocation：若取得關稅退款，傾向優先用於價格投資（原話："We would definitely bias and try"）
- 2026-05-21｜CFO｜capital_allocation：管理層稱當前每 1 美元資本的最佳報酬是投資於顧客與價格（原話："We think the single best return that we can have on $1 of capital right now is to invest in the"）
- 2026-05-21｜CFO｜commitment：管理層稱不打算因短期利潤壓力而退出價格投資，並表示在燃料壓力下仍選擇進攻（原話："We continue to play offense despite the short-term pressure on"）
- 2026-05-21｜CFO｜commitment：管理層表示營業利益成長快於銷售的全年框架不變，Q2 後將提供更新（原話："our full year financial framework to grow operating income"）
- 2026-05-21｜CFO｜commitment：回應是否下調預期：投資人日多年計畫為營收約 4%、營業利益成長快於此（約 4%–8%），無需壓低預期（原話："So I don't think tamping or metering expectations is"）
- 2026-05-21｜CEO｜commitment：執行長稱將持續採每日低價策略（原話："we will continue to operate in an everyday low price strategy across our"）
- 2026-05-21｜CEO｜competition：回應競爭對手降價：稱價格競爭向來存在，對自家價差有信心，降價回調（rollback）數量加速（原話："And we are proud of our price gaps."）
- 2026-05-21｜CFO｜competition：約 7,200 項降價回調，較去年增加逾 20%；過去數年多在 5,000–5,500 區間（原話："We have approximately 7,200 rollbacks across our assortment, which is up"）
- 2026-05-21｜CFO｜competition：Q1 固定匯率銷售成長近 6%，超出指引上緣 120bp，並持續取得市占（原話："exceeding the top end of our guidance range by 120 basis points"）
- 2026-05-21｜CFO｜competition：Sam's Club 5 月加油量成長 12%，同期業界下降 5%（原話："in the month of May, our gallons are up 12%."）
- 2026-05-21｜CEO｜product：美國第三方市集銷售成長近 50%，並帶動市集賣家廣告支出（原話："sales on our marketplace in the U.S. grew almost 50% for the quarter"）
- 2026-05-21｜CFO｜product：Walmart 履約服務（WFS）當日/次日出貨單位成長近 150%（原話："Units shipped same day or next day through WFS grew nearly 150% in Q1."）
- 2026-05-21｜CFO｜product：全球廣告成長 37%、會員費收入成長逾 17%（原話："our advertising business had"）
- 2026-05-21｜CEO｜product：AI 購物代理 Sparky 週活躍用戶一季內成長逾 100%，使用者平均訂單金額約高 35%（原話："Weekly active users are up over 100% just in the last quarter"）
- 2026-05-21｜Walmart U.S. leader｜product：Sparky 購買單位較上一季成長逾 4 倍，用途從一般商品延伸到食品與日用品（原話："units purchased through Sparky have"）
- 2026-05-21｜Walmart U.S. leader｜product：快速配送銷售年增逾 50%；無人機配送累計第 100 萬單（原話："Sales in fast delivery have grown more than 50% year-over-year in Q1."）
- 2026-05-21｜CFO｜product：美國約 60% 人口可在 30 分鐘內收貨（原話："We can now reach approximately 60% of the"）
- 2026-05-21｜CEO｜product：自動化進度約走一半，後續仍有投資（原話："we're about halfway there. So we have more"）
- 2026-05-21｜CEO｜customer：Walmart U.S. 交易筆數成長為 6 季來最強（原話："Transaction growth in the U.S. was the strongest we've"）
- 2026-05-21｜CFO｜customer：高所得顧客消費有信心，低所得顧客較預算導向（原話："the high income"）
- 2026-05-21｜CFO｜customer：Walmart+ 會員支出為非會員 4 倍；Q1 淨新增創同季新高（原話："Walmart+ members generally"）
- 2026-05-21｜CFO｜customer：Sam's Club 會員費調漲於 5 月 1 日生效（原話："supported the membership fee increase that became effective on May 1"）
- 2026-05-21｜Sam's Club leader｜customer：Sam's Club 會員成長半數來自千禧與 Z 世代（原話："half of our member growth is coming from millennial and Gen Z"）

### WMT_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md
- 2026-09-09｜Ryan Mayward｜margin：管理層稱廣告業務利潤率超過 70%，核心零售約 5%（原話："over 70% margins compared to 5-ish percent"）
- 2026-09-09｜Ryan Mayward｜margin：管理層稱廣告利潤純屬增量，不靠壓縮供應商貿易投資換取（原話："purely incremental to Walmart"）
- 2026-09-09｜Ryan Mayward｜competition：管理層稱零售媒體預算集中於兩家公司，其一占不成比例的份額，且短期不會改變（原話："I don't see this dynamic changing much in the near term."）
- 2026-09-09｜Ryan Mayward｜competition：管理層描述廣告業務由出版商轉為平台，目標服務數千至數萬廣告主（原話："we've really undertaken the publisher to platform evolution"）
- 2026-09-09｜Ryan Mayward｜customer：管理層稱第三方賣家（marketplace）帶動廣告成長並分散廣告主基礎（原話："Marketplace is providing us with that diversity"）
- 2026-09-09｜Ryan Mayward｜product：Vibe 收購已於約六週前完成，定位為小型廣告主自助式 CTV 平台（原話："It closed just 6 or so weeks ago."）
- 2026-09-09｜Ryan Mayward｜product：管理層稱 VIZIO OS 上半年為美國第一大智慧電視作業系統（原話："the #1 Smart TV operating system in the U.S."）
- 2026-09-09｜Ryan Mayward｜product：今年是向 Walmart Connect 廣告主提供 VIZIO 受眾定向與衡量的第一個完整年度，大型 CPG 採用強（原話："This year is the first full year"）
- 2026-09-09｜Ryan Mayward｜product：YouTube 合作目前處於廣告主 beta 階段（原話："we're in a beta stage right now with advertisers"）
- 2026-09-09｜Ryan Mayward｜product：自家購物代理 Sparky 的週活躍客戶數季增 60%、年增一倍（原話："60% growth quarter-to-quarter"）
- 2026-09-09｜Ryan Mayward｜product：Sparky 購物訂單平均金額比非 Sparky 高 40%（原話："which is 40% higher than non-Sparky shopping trips"）
- 2026-09-09｜Ryan Mayward｜risk：管理層稱與 Google、OpenAI 的代理購物管道目前規模小、仍早期（原話："It is early and relatively small"）
- 2026-09-09｜Ryan Mayward｜risk：管理層表示對代理式購物環境下的持續數位互動不擔心（原話："we don't have any concerns about ongoing digital engagement"）
- 2026-09-09｜Ryan Mayward｜product：搜尋廣告增量（incrementality）衡量約一年前推出，用於向品牌證明 ROI（原話："launching incrementality for search about a year ago"）
- 2026-09-09｜Ryan Mayward｜product：正在部分門市測試具庫存與價格感知的走道末端螢幕（原話："we're testing in certain stores now end-of-aisle screens"）
- 2026-09-09｜Ryan Mayward｜customer：VIZIO 與 Vibe 帶來不在 Walmart 賣商品的非本業（non-endemic）廣告主，被視為新的可觸及廣告主群（原話："That's a whole new addressable advertiser universe"）
- 2026-09-09｜Ryan Mayward｜capital_allocation：正投資把 Sam's 與國際市場廣告業務統一到共同廣告技術堆疊（原話："that's a big investment that's underway now"）
- 2026-09-09｜Ryan Mayward｜commitment：管理層稱正大力投資自家購物代理（原話："we're investing heavily in our own agent"）
- 2026-09-09｜Ryan Mayward｜guidance：管理層對廣告業務長期成長空間的定性表述，未給數字目標（原話："we see a lot of headroom to grow this business"）

### WMT_Goldman_Sachs_Global_Consumer_and_Retail_Conference_20260915.md
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜guidance：對下半年各所得族群的預期：份額與單位數成長（原話："We expect to see share gains and unit gains."）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜guidance：下半年通膨預期與上半年相近（原話："we anticipate the back half to look very similar"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜guidance：上半年通膨約 1.4%（原話："we were at roughly 1.4%"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜guidance：MFP 對營收的逆風延續到明年（原話："that headwind will continue into next year"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜guidance：明年另有 15 種藥物納入 MFP（原話："15 additional drugs that will go on MFP"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜margin：關稅退款 29 億美元幾乎全數於 Q2 收到（原話："essentially all of the $2.9 billion in refunds in Q2"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜margin：退款用於降價回饋（rollback）數量（原話："we had 11,200 rollbacks within the U.S. business"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜margin：電商連續第六季獲利（原話："We are now in our sixth quarter of e-commerce profitability"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜margin：排除廣告後電商仍獲利（原話："even if you strip out advertising, our e-commerce business"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜margin：零售媒體利潤率口徑約 70%（原話："It has roughly 70% margins, which is fantastic to see."）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜margin：被問明年利潤率順逆風，答未給明年財測（原話："We haven't rolled out guidance for next year."）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜commitment：管理層稱對價差有信心（原話："right now, we feel really good about our price gaps"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜commitment：預期 AI／自動化效率改善明年延續（原話："physical AI in our supply chain for over 7 years"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜commitment：履約網路建置進度（原話："we're in the top of the fourth inning"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜commitment：強調主動搶市占（原話："There is a great opportunity right now to go after market"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜commitment：重申進攻姿態（原話："We're playing offense."）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜commitment：假期季備戰（原話："We're ready to drive everyday low cost"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜competition：價值定義擴大為省錢加省時（原話："I think we're redefining value."）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜competition：對比競爭者收取額外費用（原話："Low prices and convenience doesn't have to be an either/or"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜product：Sparky 週互動量季增（原話："weekly engagement with Sparky grow over 60%"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜product：使用 Sparky 後客單價（原話："their average order value jumps 40%"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜product：代理式引擎優化仍在早期（原話："It's early in this space, but we're leaning in."）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜customer：電商成長與連續季數（原話："That was our 10th consecutive quarter of 20%-plus growth."）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜customer：第三方市集成長，以一般商品為主（原話："So you likely saw our marketplace growth, 52% growth."）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜capital_allocation：WFS 對賣家的收費相對競爭者折價（原話："at about a 15% discount to the price of competition"）
- 2026-09-15｜David Guggina (CEO Walmart U.S.)｜risk：VIZIO 單位成長超過 150%（廣告/裝置新收入）（原話："unit growth year-over-year is over 150%"）

### WMT_Piper_Sandler_5th_Annual_Growth_Frontiers_Conference_20260916.md
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜product：Marketplace 加速成長被歸因於多年投資同時見效，而非單一改變。（原話："there's no one particular thing that we changed."）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜product：賣家庫存放在 WFS 的商品轉換率比一般高 50%。（原話："that converts at 50% higher conversion rate overall"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜customer：以 Nespresso 為例，新品類帶來沒買過咖啡的新客。（原話："never bought coffee from us before"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜customer：管理層表示高所得家庭對新品類的滲透率偏高。（原話："We're seeing high penetration of higher-income households"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜commitment：管理層形容 Marketplace 仍處早期階段，品類仍有缺口待補。（原話："it's first inning right now"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜product：品類組合仍有缺口，正在補齊品牌與賣家。（原話："we still have gaps in assortment"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜product：已開放加拿大與墨西哥消費者購買美國賣家的商品。（原話："We open up dot-com for Canadians and Mexicans"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜capital_allocation：賣家可借用既有供應鏈，沃爾瑪稱不需大額新增投資。（原話："to our sellers without significant investment"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜competition：管理層稱 4,500 家門市加品類是與他人的差異點。（原話："nobody can replicate the 4,500 stores"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜product：Marketplace 以一般商品為主，食品占比低。（原話："marketplace is predominantly general merchandise"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜margin：針對同店可比銷售，管理層表示正研究補充性指標。（原話："we are working on how do we provide complementary metrics"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜margin：Marketplace 以淨銷售額申報，GMV 是內部另看的指標。（原話："we report on net sales, [ GMV ] is another metric"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜product：電商取貨與配送上季成長 43%。（原話："e-commerce, online pickup delivery grew 43% last quarter"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜product：門市被描述為履約節點，並給出配送覆蓋範圍。（原話："95% of America is in 3 hours delivery range of stores"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜product：開始依資料把第三方庫存前置到門市後倉。（原話："forward deploying inventory into the stores in the back"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜commitment：目前前置庫存只放在後倉，尚未上貨架。（原話："we're starting with the backroom to place inventory there"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜margin：引述 CFO 說法，Marketplace 是第二損益表成長的關鍵。（原話："marketplace is a lynchpin for our second P&L growth"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜margin：賣家使用 WFS 成本低 15%。（原話："A seller sees 15% lower cost when it's in WFS."）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜product：WFS 加廣告的商品，GMV 有時成長 5 倍。（原話："we see sometimes 5x GMV growth"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜product：管理層提到也在評估 Data Ventures 作為賣家新服務。（原話："We are also looking at Data Ventures."）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜margin：測試降費時，賣家把省下的錢投回平台並讓利顧客。（原話："whenever we've dropped fees to test things out"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜product：賣家銷售中有 50% 透過 WFS。（原話："50% of our sales came through Walmart Fulfillment Services"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜product：海外延伸目前聚焦墨西哥、加拿大與智利。（原話："Mexico and Canada and then Chile"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜commitment：管理層對賣家表示願被問責並兌現成長目標。（原話："hold us accountable and we'll deliver those goals"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜commitment：對三到五年後的描述：自營與第三方的界線將淡化。（原話："the boundaries between 1P and 3P will start eroding"）
- 2026-09-16｜Manish Joneja (SVP, Global Head of Marketplace and Fulfillment Services)｜margin：管理層預期此模式對賣家、沃爾瑪與顧客都更有獲利性。（原話："We see it being a much more profitable business"）

### 問答異常語氣（迴避／改口／保留）
- WMT_Q1_2027_Earnings_Call_20260521.md｜問：Lasser：外部逆風不斷，是否該下調雙位數營業利益成長的預期｜答法：不直接承諾雙位數，改引投資人日 4%–8% 區間，稱不需壓低預期，並提醒勿過度著眼單季
- WMT_Q1_2027_Earnings_Call_20260521.md｜問：Paul Lejuez：價差現況與競爭對手降價跡象、願用多少價差守市占｜答法：未給價差具體數字，改談降價回調數量與每日低價策略，僅稱以自家價差為傲
- WMT_Q1_2027_Earnings_Call_20260521.md｜問：Krisztina Katai：市集成長拆解為賣家數、SKU、客單價及年內推展節奏｜答法：未提供賣家數、SKU、客單價拆解數字，改談品項擴充與飛輪概念
- WMT_Q1_2027_Earnings_Call_20260521.md｜問：Kate McShane：加拿大與墨西哥新平台何時對企業利潤率有貢獻｜答法：未給時間表或貢獻幅度，改談 build once scale globally 與國際電商、會員、廣告成長數字
- WMT_Goldman_Sachs_Global_Consumer_and_Retail_Conference_20260915.md｜問：明年（'27 vs '26）利潤率是順風還是逆風？｜答法：未直接回答方向，表示未發布明年財測，改談廣告／市集／會員組合改變 P&L
- WMT_Goldman_Sachs_Global_Consumer_and_Retail_Conference_20260915.md｜問：市集成長目標數字（提問未講數字）｜答法：前面稱市集成長 52%，後面稱目標「drive 51% growth」，兩處數字不一致
- WMT_Piper_Sandler_5th_Annual_Growth_Frontiers_Conference_20260916.md｜問：Marketplace 成長 52% 對整體一般商品同店可比的影響有多大？｜答法：未給 Marketplace 對一般商品同店可比的貢獻數字，改談門市已成履約節點、需要補充性指標與電商 43% 成長。

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
{"date":"20260522","verdict":"B（觀望，Q1 FY27 三大假設全 🟢 兌現 + 盤後 -7% 賣壓帶來價位修復，估值🔴→🟠 邊緣但 PEG 仍 2.84，等 PE 32x 以下 ~$95 再進場）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Walmart Connect 廣告全球 YoY ≥ +25% 至 FY29","columns":{"2Y / 5Y / 10Y 驗證點":"2Y：≥ +25% / 季5Y：營收占比達 1.5% Rev (~$15B)10Y：3-5% Rev (~$40-70B)","sourced floor":"≥ +25%（Q1 FY27 全球 +37% / US +44%；FY26 全年 +46%）","來源":"WMT IR Q1 FY27 ER；AdExchanger FY26 ($6.4B); Marketing Dive 2026 報告","漂移觸發":"連 2 季 &lt; +25% → 削弱；單季不觸發（QC-34）"}},{"id":"H2","text":"US comp ex-gas ≥ +3.5% FY27-FY29","columns":{"2Y / 5Y / 10Y 驗證點":"2Y：FY27 ≥ +3.5%5Y：FY29 ≥ +3%10Y：≥ +2%（隨成熟度下降）","sourced floor":"≥ +3.5%（Q1 FY27 +4.1%；FY26 +4.6%；FY27 公司 guidance Sales +3.5-4.5%）","來源":"WMT Q1 FY27 ER 2026/5/21；FY27 guidance 段","漂移觸發":"連 2 季 US comp &lt; +3% → 削弱"}},{"id":"H3","text":"國際 CC + Sam's 會員費雙引擎續強","columns":{"2Y / 5Y / 10Y 驗證點":"2Y：國際 CC ≥ +6% / Sam's 全球會員費 ≥ +10%5Y：mix shift 後 international + Sam's OI 占公司 OI 提升 5pp","sourced floor":"國際 CC ≥ +6%（Q1 FY27 ~+12% CC after $2.3B FX）；Sam's 會員費 ≥ +10%（Q1 FY27 全球 +17.4%）","來源":"WMT Q1 FY27 ER segment 段；Sam's ICM 2025/4 提價歷史","漂移觸發":"國際 CC &lt; +2% 連 2 季；Sam's 會費 &lt; +5% 連 1 季 → 觀察"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"廣告增速從 +37% 跌至 +20% 以下（base effect + AI agent 截流）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Walmart Connect 全球 YoY%（季）","警戒閾值":"連 2 季 &lt; +25%"}},{"id":"R2","text":"Furner 執行失誤（大型錯誤併購 / 放棄 EDLP 文化 / 自動化 ROIC miss）","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 EPS beat 幅度、大型 M&amp;A、Capex / Rev 比例","警戒閾值":"EPS miss &gt; 5% 或 M&amp;A &gt; $10B 或 Capex / Rev &gt; 5%"}},{"id":"R3","text":"10Y UST &gt; 5.5% 引發 defensive premium 重評，Fwd PE 41.6x → 28x","columns":{"對應假設":"H3 / 估值倍數","時間尺度":"🐢 長期（2+ 年）","監測指標":"10Y UST、Fwd PE","警戒閾值":"UST &gt; 5.5% 持續 6+ 個月 + Fwd PE &lt; 28x"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":121.34,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WMT_20261019/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
