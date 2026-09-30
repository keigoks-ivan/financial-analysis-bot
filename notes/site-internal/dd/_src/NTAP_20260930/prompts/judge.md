你是 stock-analyst **v20 判斷 agent**，標的 NTAP（20260930）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
  *eps
    *bull[]: arr ≥1 num
    *base[]: arr ≥1 num
    *bear[]: arr ≥1 num
  *pe
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
- `counter_evidence.blind_spots[].view`：論點失敗｜論點成功但股東經濟變差｜價格已反映太多
- `decision_inputs.signal`：A+｜A｜B｜C｜X
- `decision_inputs.ma`：🟢｜✅｜🟡｜🟠｜❌｜-
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
{"meta":{"ticker":"NTAP","date":"2026-09-30","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NTAP_20260930/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NTAP_20260930/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":2025,"period":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","citation":"公司新聞稿 investors.netapp.com Q1 FY27 press release；YoY/QoQ 見 prepared remarks (s21.q4cdn.com)"},"note":"查無可靠共識數字；公司稱超越所有指引區間高端"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":31.9,"period":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","citation":"公司新聞稿 investors.netapp.com Q1 FY27 press release（營業利益 $645M）"},"note":"超越指引高端（共識數字查無）"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":23.9,"period":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","citation":"公司新聞稿 investors.netapp.com Q1 FY27 press release（GAAP 營業利益 $484M）"}},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":401,"period":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","citation":"公司新聞稿 investors.netapp.com Q1 FY27 press release（營運現金流 $503M，capex $102M）"}},{"id":"f_kpi5_guidance_q2_fy27","label":"Guidance: Q2 FY27","value":"營收 $2.025–2.175B；non-GAAP EPS $2.54–2.64；non-GAAP 營業利益率 30.9–31.9%；non-GAAP 毛利率 67.0–68.0%","period":"Q1 FY2027（公告於 2026-09-02）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q1 FY2027（公告於 2026-09-02）","citation":"公司新聞稿 Q1 FY27 press release"}},{"id":"f_kpi6_guidance_fy27","label":"Guidance: FY27 全年","value":"營收 $7.975–8.225B；non-GAAP EPS $9.73–10.03（本次上調）","period":"Q1 FY2027（公告於 2026-09-02）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q1 FY2027（公告於 2026-09-02）","citation":"公司新聞稿 Q1 FY27 press release；上調表述見 prepared remarks"}},{"id":"f_kpi7_remaining_performance_ob","label":"Remaining Performance Obligations (RPO)","value":5650,"period":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","citation":"公司 prepared remarks (s21.q4cdn.com Q1 FY27)；遞延收入 $4.85B（+7% YoY）"}},{"id":"f_kpi8_billings","label":"Billings","value":2057,"period":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","citation":"公司新聞稿 Q1 FY27 press release"}},{"id":"f_kpi9_product_revenue_all_flas","label":"Product revenue / All-flash array revenue","value":987,"period":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","unit":"USD million（AFA $1,309M，+47% YoY）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","citation":"公司 prepared remarks 與新聞稿 Q1 FY27"}},{"id":"f_kpi10_product_gross_margin_non","label":"Product gross margin (non-GAAP)","value":54.6,"period":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","citation":"公司 prepared remarks Q1 FY27（整體 non-GAAP 毛利率 70.6%）"}},{"id":"f_kpi11_inventory_turns","label":"Inventory turns","value":6,"period":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","unit":"x","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","citation":"公司 prepared remarks Q1 FY27"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-09-02","period":"2026-09-02","unit":"date","basis":"距今 20 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-09-02"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ntap_gross_margin_pct","label":"NTAP 毛利率","value":70.63,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NTAP.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_ntap_operating_margin_pct","label":"NTAP 營業利益率","value":26.03,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NTAP.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_ntap_fcf_margin_pct","label":"NTAP FCF 利潤率","value":22.32,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NTAP.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_sndk_gross_margin_pct","label":"SNDK 毛利率","value":71.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sndk_operating_margin_pct","label":"SNDK 營業利益率","value":61.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sndk_fcf_margin_pct","label":"SNDK FCF 利潤率","value":56.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_gross_margin_pct","label":"000660.KS 毛利率","value":76.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_operating_margin_pct","label":"000660.KS 營業利益率","value":68.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_000660_ks_fcf_margin_pct","label":"000660.KS FCF 利潤率","value":47.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_gross_margin_pct","label":"005930.KS 毛利率","value":57.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_operating_margin_pct","label":"005930.KS 營業利益率","value":36.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_fcf_margin_pct","label":"005930.KS FCF 利潤率","value":28.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_gaap","label":"SBC 占營收 / 占 GAAP 營業利益","value":4.8,"period":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","unit":"% of revenue（SBC $98M；約占 GAAP 營業利益 20.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）","citation":"公司新聞稿 Q1 FY27 press release（SBC $98M）；比率由本 agent 換算"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":209.18,"period":"2026-09-29（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-09-29（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":105.97,"period":"2026-09-29（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-09-29（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":66.22,"period":"2026-09-29（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-09-29（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.01 → 10.01）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.12 → 11.12）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.36 → 12.36）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":10.01,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":11.12,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":12.36,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":12.47,"period":"2026-06-23 → 2026-09-26","unit":"%","basis":"FY1 共識 EPS 8.9 → 10.01（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":28.89,"period":"2026-09-29（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-09-29（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-09-29（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-09-29（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.56,"period":"2026-09-29（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-09-29（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-09-29（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-09-29（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.42,"period":"2026-09-29（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-09-29（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-09-29（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-09-29（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":20.9,"period":"2026-09-26","unit":"x","basis":"分母＝FY1 EPS 10.01，分子＝快照價 209.18","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-26"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.994,"period":"2026-09-30","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-09-30"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-09-30","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-30","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 209.18 / W52 134.02 / W104 120.45 / W250 95.87 / W250 13週斜率 2.08%"},{"id":"f_ma_w52","label":"52 週均線","value":134.02,"period":"2026-09-30","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-30","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":120.45,"period":"2026-09-30","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-30","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":95.87,"period":"2026-09-30","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-30","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.08,"period":"2026-09-30","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-30","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"IDC：NetApp 2025 全年外接式企業儲存份額 8.1%、排第三，全快閃陣列表現穩健；外部 OEM 儲存市場 2025 年成長 4.3% 至 353 億美元","source":"Blocks & Files, IDC ranks Dell, NetApp, Everpure, Huawei and HPE in external storage systems market","url":"https://www.blocksandfiles.com/flash/2026/06/16/idc-ranks-dell-netapp-everpure-huawei-and-hpe-in-external-storage-systems-market/5256070","excerpt":"NetApp held third place with an 8.1% share in 2025, driven by solid results in all-flash arrays. The external OEM enterprise storage systems market grew by 4.3% in 2025 to $35.3 billion.","as_of":"2026-06-16","retrieved_at":"20260930","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"IDC：2026 年第一季 NetApp 為外接式儲存第二大供應商，僅次於 Dell；前五為 Dell、NetApp、Everpure、Huawei、HPE","source":"Blocks & Files, IDC ranks Dell, NetApp, Everpure, Huawei and HPE in external storage systems market","url":"https://www.blocksandfiles.com/flash/2026/06/16/idc-ranks-dell-netapp-everpure-huawei-and-hpe-in-external-storage-systems-market/5256070","excerpt":"NetApp was the second-largest external storage systems supplier in the first quarter of 2026, after Dell, with a top five ranking also including Everpure, Huawei, and HPE.","as_of":"2026-06-16","retrieved_at":"20260930","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"IDC 最新追蹤（2026 Q2）：NetApp 年增 35.7%、成長速度第三快，市占仍高於 Everpure","source":"Blocks & Files, IDC's latest enterprise storage tracker shows booming storage market growth","url":"https://www.blocksandfiles.com/flash/2026/09/23/idcs-latest-enterprise-storage-tracker-shows-booming-storage-market-growth/5298577","excerpt":"NetApp grew third-fastest at 35.7% year-over-year, while NetApp remained ahead of Everpure in market share trends.","as_of":"2026-09-23","retrieved_at":"20260930","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"IDC 2025 Q3：NetApp 份額 9.4% 排第三（全快閃陣列表現穩）；同期 Pure（現 Everpure）與 Huawei 為成長最快者，NetApp 非成長最快","source":"Blocks & Files / StorageNewsletter, IDC Q3 2025 tracker","url":"https://www.blocksandfiles.com/ai-ml/2025/12/12/idc-storage-tracker-shows-pure-and-huawei-growing-fastest/1720792","excerpt":"NetApp finished third with 9.4% share thanks to solid performance in all-flash arrays (AFA).","as_of":"2025-12-12","retrieved_at":"20260930","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"NetApp 財報風險揭露：對手含既有公開公司、專注快閃的新公開公司，以及鎖定 AI 商機的新進入者","source":"NetApp Form ARS FY2026 / 8-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001002047/000119312526321239/ntap-2026_ars.pdf","excerpt":"NetApp faces competition from many companies, including established public companies, newer public companies focused on flash storage, and new market entrants targeting the AI opportunity.","as_of":"2026-07-15","retrieved_at":"20260930","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"搜尋摘要稱：受供給限制的超大規模雲業者更願意認證新供應商，可能替新進入者打開取代缺口（摘要為搜尋工具轉述，未讀原頁）","source":"search summary on NetApp Q3 FY2026 (Futurum / Forbes results)","url":"https://futurumgroup.com/insights/netapp-q3-fy-2026-results-highlight-all-flash-growth-and-cloud-services/","excerpt":"hyperscalers facing supply constraints are more willing to qualify new vendors, potentially opening the door to competitive displacement.","as_of":"2026-02-28","retrieved_at":"20260930","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"NetApp FY2026 10-K: 兩家主要客戶合計占淨營收 43%（搜尋摘要稱為兩家通路商客戶，未單獨拆出最大客戶占比）。","source":"NetApp, Inc. Form 10-K FY2026 (period ended 2026-04-24)","url":"https://www.sec.gov/Archives/edgar/data/0001002047/000119312526259683/ntap-20260424.htm","excerpt":null,"as_of":"2026-04-24","retrieved_at":"20260930","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"NetApp FY2026 10-K：兩家經銷商客戶合計約占營收 43%（搜尋摘要未指名、未拆個別比重；明細在 10-K Note 14）","source":"NetApp, Inc. Form 10-K FY2026 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0001002047/000119312526259683/ntap-20260424.htm","excerpt":null,"as_of":"2026-04-24","retrieved_at":"20260930","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"StorageSwiss (2026-05-06) 標題主張記憶體與快閃價格到 2027 都不會回落；搜尋摘要稱這是結構性重新配置，而非暫時性缺貨。","source":"StorageSwiss: Memory and Flash Prices Are Not Coming Down (Through 2027)","url":"https://storageswiss.com/2026/05/06/memory-and-flash-prices-not-coming-down/","excerpt":"Memory and Flash Prices Are Not Coming Down (Through 2027)","as_of":"2026-05-06","retrieved_at":"20260930","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Micron 新加坡 NAND 廠預計 2028 下半年才開始出貨；搜尋摘要稱有意義的新產能要到 2027 或 2028 才會出現，2026 年吃緊不受影響。","source":"搜尋結果彙整 (NAND supply discipline new capacity timeline 2026)；相關來源含 NAND Research、Kioxia via IBS Electronics","url":"https://nand-research.com/memory-nand-flash-crisis-may-2026-update/","excerpt":"Micron's planned $24B Singapore NAND fab is a major capacity signal, but output is expected to begin in 2H 2028","as_of":"2026-05-01","retrieved_at":"20260930","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"NetApp 管理層稱需求橫跨各客戶類型、地區與產業，且不同於過往靠大幅漲價的週期，與 AI 及其現代化需求相關；FY26 全快閃營收創高 $4.2B、年增 11%，AI 與資料準備新單逾 1,100 件。","source":"Yahoo Finance: NetApp Q1 Earnings Call Highlights Durable AI-Led Demand；Futurum: NetApp Q4 FY 2026","url":"https://finance.yahoo.com/technology/ai/articles/netapp-q1-earnings-call-highlights-172400980.html","excerpt":"All-flash revenue reached a record $4.2 billion in FY26, up 11% year-over-year","as_of":"2026-05-28","retrieved_at":"20260930","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"NetApp FY2026 10-K 風險揭露：自進口來源國採購／製造的產品，若貿易限制、關稅或稅負變動，可能對業務與財務結果造成重大不利影響；美國關稅政策仍在變動，另有中美緊張與台海風險可能影響關鍵零組件取得。","source":"NetApp, Inc. Form 10-K FY2026 (period ended 2026-04-24), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0001002047/000119312526259683/ntap-20260424.htm","excerpt":"changes in trade restrictions, tariffs, or taxes on imports from countries where they source and/or manufacture products could have a material adverse effect on their business and financial results.","as_of":"2026-04-24","retrieved_at":"20260930","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"報導稱美中同意對 300 億美元商品降關稅並啟動 AI 對話（2026-09-27）。","source":"The National: China and US agree to tariff cuts on $30 billion in goods and AI dialogue","url":"https://www.thenationalnews.com/business/economy/2026/09/27/china-and-us-agree-to-tariff-cuts-on-30-billion-in-goods-and-ai-dialogue/","excerpt":"China and US agree to tariff cuts on $30 billion in goods and AI dialogue","as_of":"2026-09-27","retrieved_at":"20260930","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"產業層：IEEPA 關稅遭最高法院否決後，10% 全球關稅於 2026-07-24 到期，改為對 80 國課 10–12.5% 的 Section 301 關稅；IT 硬體成本 2026 年上升 15–30%。此為一般產業資料，非 NetApp 專屬。","source":"WebSearch 摘要（growrk.com 等）：data storage hardware tariff exposure supply chain 2026","url":"https://growrk.com/blog/control-global-it-hardware-costs","excerpt":"Global IT hardware costs are up 15-30% in 2026, with tariffs and AI demand creating a structural price surge.","as_of":"2026-07-24","retrieved_at":"20260930","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"NetApp 10-K 揭露：不直接控制製造環節，製造夥伴與供應商地理分散，地緣衝突等可能中斷供應鏈","source":"NetApp Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001002047/000119312526259683/ntap-20260424.htm","excerpt":"NetApp lacks direct control over manufacturing elements and has diverse international geographic locations of manufacturing partners and suppliers, which creates significant risks including geopolitical disputes, acts of terrorism, cyber attacks and hacktivism disrupting the supply chain.","as_of":"2026-04-24","retrieved_at":"20260930","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"NetApp 10-K 揭露：中台緊張升級可能影響其或代工廠取得關鍵供應鏈零組件的能力","source":"NetApp Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001002047/000119312526259683/ntap-20260424.htm","excerpt":"any increase in tensions between China and Taiwan, including threats of military actions or escalation of military activities, could adversely affect its ability, or the ability of its contract manufacturers, to source key supply chain components included in its products.","as_of":"2026-04-24","retrieved_at":"20260930","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"NetApp 依賴商品化 NVMe SSD 供應鏈（非自研快閃），加速採用新世代 NAND 並降低媒體成本","source":"Technologymatch: Pure Storage vs NetApp vs Dell PowerStore (2026)","url":"https://technologymatch.com/blog/pure-storage-vs-netapp-vs-dell-powerstore-storage-comparison-ai","excerpt":"NetApp relies on the commodity NVMe SSD supply chain, which speeds adoption of each NAND generation and lowers media cost.","as_of":"2026-01-01","retrieved_at":"20260930","affects":["moat_trend"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"NAND/DRAM 生產集中於三家廠商，產能轉向 HBM/企業級，下游議價空間有限；企業級 SSD 2026 合約價預估大漲，短缺可能延續至 2027–2028","source":"NAND Research: Memory & Flash Crisis March 2026 Update / Avnet / Microchip USA（搜尋彙整）","url":"https://nand-research.com/memory-flash-crisisc-update-march-2026/","excerpt":"The NAND shortage is likely to persist until 2027-2028, when new fab investments gradually start operations.","as_of":"2026-03-01","retrieved_at":"20260930","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY27 Q1 (季底約 2026-07)：Hybrid Cloud 營收 +30% 至 $1.82B；Public Cloud +28% 至紀錄 $206M；總營收 +30% 至 $2.03B。","source":"NetApp Reports First Quarter of Fiscal Year 2027 Results (NetApp IR)","url":"https://investors.netapp.com/news/news-details/2026/NetApp-Reports-First-Quarter-of-Fiscal-Year-2027-Results/default.aspx","excerpt":"Hybrid Cloud revenue increased 30% to $1.82 billion","as_of":"2026-09-02","retrieved_at":"20260930","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"FY27 Q1 全快閃陣列（AFA）營收年增 47% 至 $1.31B；Hybrid-Flash 及其他 $510M（前年同期 $505M，近乎持平）；Billings $2.06B、+36%。","source":"NetApp Reports First Quarter of Fiscal Year 2027 Results (via search summary)","url":"https://investors.netapp.com/news/news-details/2026/NetApp-Reports-First-Quarter-of-Fiscal-Year-2027-Results/default.aspx","excerpt":"All-Flash Array Revenue grew 47% year over year to $1.31 billion","as_of":"2026-09-02","retrieved_at":"20260930","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"IDC 2026 年第一季外部儲存系統排名：Dell、NetApp、Everpure、Huawei、HPE；NetApp 居第二。","source":"Blocks and Files: IDC ranks Dell, NetApp, Everpure, Huawei and HPE in external storage systems market","url":"https://www.blocksandfiles.com/flash/2026/06/16/idc-ranks-dell-netapp-everpure-huawei-and-hpe-in-external-storage-systems-market/5256070","excerpt":"the top five external storage systems suppliers were Dell, NetApp, Everpure, Huawei and HPE in that order","as_of":"2026-06-16","retrieved_at":"20260930","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"Dell 在 2025 年第二季重奪 AFA 市佔第一（NetApp 曾於 2025 年第一季居首）。","source":"Blocks and Files: Dell reclaims top spot in all-flash array market","url":"https://www.blocksandfiles.com/flash/2025/09/21/dell-reclaims-top-spot-in-all-flash-array-market/1608235","excerpt":"Dell reclaims top spot in all-flash array market","as_of":"2025-09-21","retrieved_at":"20260930","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"外部企業儲存市場 2026 年第一季營收 $9.2B、年增 22.7%（2025 年全年為 3.9%）；高階系統年增逾 60%。此為聚合站報導，非 IDC 原文。","source":"KAD: Enterprise Storage Market Surges to $9.2B Amid AI-Driven Demand","url":"https://www.kad8.com/news/enterprise-storage-market-surges-to-9.2-billion-amid-ai-driven-demand/","excerpt":"The global enterprise external storage systems market reached $9.2 billion in Q1 2026, representing a 22.7% year-over-year increase","as_of":"2026-06-16","retrieved_at":"20260930","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"0","claim":"TrendForce：2027 年 DRAM 供給仍緊，NAND 供給情勢趨緩（標題層級）；搜尋摘要另稱 NAND 價格高位與配置吃緊可能延續至 2027（來源為次級聚合，未取得原文）。NAND 成本走向對 AFA 毛利與定價為變數。","source":"TrendForce: Diverging Memory Market Outlook in 2027 as DRAM Supply Remains Tight While NAND Flash Supply Conditions Ease","url":"https://www.trendforce.com/presscenter/news/20260730-13158.html","excerpt":"Diverging Memory Market Outlook in 2027 as DRAM Supply Remains Tight While NAND Flash Supply Conditions Ease, Says TrendForce","as_of":"2026-07-30","retrieved_at":"20260930","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"Public Cloud：FY26 Q3 營收 $174M，第一方與 marketplace 儲存服務年增 27%；FY26 Q2 為 +32%。","source":"Enterprise Times: NetApp celebrates growth and looks forward to strong Q4 finish (via search summary)","url":"https://www.enterprisetimes.co.uk/2026/02/27/netapp-celebrates-growth-and-looks-forward-to-strong-q4-finish/","excerpt":"NetApp's Public Cloud revenue totaled $174 million in Q3 2026, supported by 27% year-over-year growth in first-party and marketplace storage services.","as_of":"2026-02-27","retrieved_at":"20260930","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"-","claim":"AWS 於 2026 年 4 月為 S3 加入檔案存取，Blocks and Files 稱其對標 NetApp 與 Qumulo。","source":"Blocks and Files: AWS adds file access to S3, taking on NetApp and Qumulo","url":"https://www.blocksandfiles.com/public-cloud/2026/04/07/aws-adds-file-access-to-s3-taking-on-netapp-and-qumulo/5214675","excerpt":"AWS adds file access to S3, taking on NetApp and Qumulo","as_of":"2026-04-07","retrieved_at":"20260930","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"NetApp FY2026 10-K risk factors: competes with established public companies, newer flash-focused public companies and new entrants targeting the AI opportunity; markets have rapidly changing technology; AI technologies evolving with significant competition.","source":"NetApp Form 10-K FY2026 (period ended 2026-04-24), SEC","url":"https://www.sec.gov/Archives/edgar/data/0001002047/000119312526259683/ntap-20260424.htm","excerpt":null,"as_of":"2026-04-24","retrieved_at":"20260930","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"NetApp risk factor: business may be harmed if it cannot keep pace with rapid technological change or manage the transition from older products to new ones (10-K language surfaced in search; the exact filing year of the surfaced text is not confirmed).","source":"SEC NetApp filings via search (10-K/10-Q)","url":"https://www.sec.gov/Archives/edgar/data/0001002047/000119312526259683/ntap-20260424.htm","excerpt":null,"as_of":"2026-04-24","retrieved_at":"20260930","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Industry commentary lists newer approaches disrupting enterprise storage: hyperconverged storage, NVMe flash, container storage, composable/disaggregated infrastructure; Gartner-cited forecast that by 2028, 20% of I&O heads will deploy agentic-AI autonomous storage infrastructure, up from under 1% in 2026.","source":"Search results for 'enterprise storage alternative technology disruption 2026 2027' (Infinidat, TechTarget, DCD, others)","url":"https://www.infinidat.com/en/blog/storage-trends-2026","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20260930","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Roadmap commentary: enterprises continue to run production workloads on flash, object storage takes on broader scale-out/analytics role; DNA and optical ultra-cold archive media confined to narrow archival use cases.","source":"Intelligent CIO North America, Storage trends for 2026","url":"https://www.intelligentcio.com/north-america/2026/01/21/storage-trends-for-2026-how-ai-cyber-resilience-and-power-efficiency-are-reshaping-enterprise-data-centres/","excerpt":null,"as_of":"2026-01-21","retrieved_at":"20260930","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Keystone（訂閱／用量計價儲存即服務）營收 FY2026 年增約 65%（搜尋摘要轉述，未讀原文頁面）","source":"NetApp 8-K FY2026 earnings release / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001002047/000119312526245196/ntap-ex99_1.htm","excerpt":"Revenue from NetApp's Keystone storage-as-a-service offering grew approximately 65% year-over-year in FY2026","as_of":"2026-05","retrieved_at":"20260930","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"NetApp 推出 Keystone Sovereign，供合資格歐洲客戶使用資料主權控制","source":"BusinessWire: NetApp Enhances Data Sovereignty Controls to Keystone","url":"https://www.businesswire.com/news/home/20260929289707/en/NetApp-Enhances-Data-Sovereignty-Controls-to-Keystone","excerpt":"NetApp announced NetApp Keystone Sovereign, which will enable qualified European customers to use data sovereignty controls in support of their compliance and data residency journeys.","as_of":"2026-09-29","retrieved_at":"20260930","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY27 起改版全球經銷夥伴計畫，簡化會員門檻；間接通路約占營收四分之三，未見通路去中介化證據","source":"NetApp Blog: Empowering distribution partners to drive growth & innovation","url":"https://www.netapp.com/blog/distribution-partner-program-fy27/","excerpt":"As NetApp entered FY27, the company built on the success of its Distribution ecosystem with enhancements to the NetApp Distribution Partner Program","as_of":"2026-05","retrieved_at":"20260930","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師共識評級為 Hold，部分券商目標價高至 $225","source":"Daily Political: NetApp, Inc. (NASDAQ:NTAP) Receives Consensus Rating of Hold from Analysts","url":"https://www.dailypolitical.com/2026/09/26/netapp-inc-nasdaqntap-receives-consensus-rating-of-hold-from-analysts.html","excerpt":"The consensus rating is \"Hold,\" although some firms have issued bullish ratings and price targets as high as $225.","as_of":"2026-09-26","retrieved_at":"20260930","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司大幅上調 FY2027 營收與 non-GAAP EPS 指引（營收 $7.975–8.225B，前為 $7.325–7.575B；EPS $9.73–10.03，前為 $8.70–9.00）","source":"NetApp 8-K ex99_1 (SEC) / Q1 FY27 results coverage","url":"https://www.sec.gov/Archives/edgar/data/0001002047/000119312526245196/ntap-ex99_1.htm","excerpt":"The company now expects full-year revenue of $7.975 billion to $8.225 billion, up from its previous $7.325 billion-$7.575 billion range. Its non-GAAP EPS outlook increased to $9.73-$10.03, compared with the previous $8.70-$9.00 range.","as_of":"2026-08-31","retrieved_at":"20260930","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q1 FY27 EPS $2.58 對共識 $2.12、營收 $2.02B 對共識 $1.84B；次季營收指引中點 $2.1B 比預期高 13.2%","source":"Yahoo Finance: NetApp Stock: Analyst Estimates & Ratings","url":"https://finance.yahoo.com/markets/stocks/articles/netapp-stock-analyst-estimates-ratings-110635504.html","excerpt":"NetApp reported $2.58 EPS for the recent quarter, beating analysts' consensus estimates of $2.12 by $0.46, with revenue of $2.02 billion during the quarter, compared to the consensus estimate of $1.84 billion.","as_of":"2026-08-31","retrieved_at":"20260930","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價共識分布依來源不同：約 $190.69–$195.79（13–28 位分析師）；Barclays 目標價由 $199 上調至 $219（Overweight）","source":"StockAnalysis / Barclays PT revision (search aggregate)","url":"https://stockanalysis.com/stocks/ntap/forecast/","excerpt":"Barclays raised the firm's price target on NetApp (NTAP) to $219 from $199 and keeps an Overweight rating on the shares.","as_of":"2026-09-30","retrieved_at":"20260930","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Zacks 共識 EPS 30 天內上修約 21.6%，八筆上修、無下修","source":"Yahoo Finance: Why NetApp (NTAP) Might be Well Poised for a Surge","url":"https://finance.yahoo.com/markets/stocks/articles/why-netapp-ntap-might-well-162002580.html","excerpt":"The Zacks Consensus Estimate for NetApp has increased 21.61% over the last 30 days, with eight estimates moving higher compared to no negative revisions.","as_of":"2026-09-30","retrieved_at":"20260930","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"NetApp 宣布擬收購英國 AI 儲存軟體公司 PEAK:AIO（元資料架構／平行檔案系統），未揭露金額，需完成慣例交割條件與監管核准。","source":"NetApp Investor Relations — NetApp Announces Intent to Acquire PEAK:AIO to Advance Scalable AI Infrastructure Architecture","url":"https://investors.netapp.com/news/news-details/2026/NetApp-Announces-Intent-to-Acquire-PEAKAIO-to-Advance-Scalable-AI-Infrastructure-Architecture/default.aspx","excerpt":"The acquisition remains subject to customary closing conditions and regulatory approvals, while NetApp did not disclose financial terms for the transaction.","as_of":"2026-09-25","retrieved_at":"20260930","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"PEAK:AIO 交易之前，NetApp 已於 2026 年 7 月收購 DataPelago、8 月收購 JetStream Software。","source":"Yahoo Finance — Can PEAK:AIO Buyout Give NetApp a Competitive Edge in AI-Scale Storage?","url":"https://finance.yahoo.com/technology/ai/articles/peak-aio-buyout-netapp-competitive-133800847.html","excerpt":"The deal follows NetApp's acquisition of DataPelago in July and JetStream Software in August as the company expands its data infrastructure portfolio for AI workloads.","as_of":"2026-09-25","retrieved_at":"20260930","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"NetApp 宣布擬收購 PEAK:AIO，未揭露金額，需監管核准。","source":"NetApp Investor Relations — NetApp Announces Intent to Acquire PEAK:AIO","url":"https://investors.netapp.com/news/news-details/2026/NetApp-Announces-Intent-to-Acquire-PEAKAIO-to-Advance-Scalable-AI-Infrastructure-Architecture/default.aspx","excerpt":"The acquisition remains subject to customary closing conditions and regulatory approvals, while NetApp did not disclose financial terms for the transaction.","as_of":"2026-09-25","retrieved_at":"20260930","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"此前已於 7 月收購 DataPelago、8 月收購 JetStream Software。","source":"Yahoo Finance — Can PEAK:AIO Buyout Give NetApp a Competitive Edge in AI-Scale Storage?","url":"https://finance.yahoo.com/technology/ai/articles/peak-aio-buyout-netapp-competitive-133800847.html","excerpt":"The deal follows NetApp's acquisition of DataPelago in July and JetStream Software in August as the company expands its data infrastructure portfolio for AI workloads.","as_of":"2026-09-25","retrieved_at":"20260930","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 12 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"NTAP","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":70.63,"operating_margin_pct":26.03,"fcf_margin_pct":22.32,"rd_intensity_pct":13.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NTAP","as_of":"TTM ending 2026-07-31（4季加總）"},"is_subject":true},{"name":"SNDK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.47,"operating_margin_pct":61.58,"fcf_margin_pct":56.77,"rd_intensity_pct":6.56},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"000660.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":76.27,"operating_margin_pct":68.04,"fcf_margin_pct":47.8,"rd_intensity_pct":4.93},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.000660.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"005930.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.48,"operating_margin_pct":36.88,"fcf_margin_pct":28.95,"rd_intensity_pct":9.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"PSTG","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PSTG"},"note":"quarterly_income_stmt 無資料"}],"subject":"NTAP"},"financial_history":{"ticker":"NTAP","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-04-30","revenue":6362000000.0,"revenue_yoy_pct":null,"gross_margin_pct":66.16,"operating_margin_pct":18.22,"net_income":1274000000.0,"diluted_eps":5.79,"free_cash_flow":868000000.0,"fcf_margin_pct":13.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-04-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-04-30","revenue":6268000000.0,"revenue_yoy_pct":-1.48,"gross_margin_pct":70.72,"operating_margin_pct":20.23,"net_income":986000000.0,"diluted_eps":4.63,"free_cash_flow":1530000000.0,"fcf_margin_pct":24.41,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-04-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-04-30","revenue":6572000000.0,"revenue_yoy_pct":4.85,"gross_margin_pct":70.19,"operating_margin_pct":21.68,"net_income":1186000000.0,"diluted_eps":5.67,"free_cash_flow":1338000000.0,"fcf_margin_pct":20.36,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-04-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-04-30","revenue":6925000000.0,"revenue_yoy_pct":5.37,"gross_margin_pct":70.74,"operating_margin_pct":24.48,"net_income":1276000000.0,"diluted_eps":6.35,"free_cash_flow":1869000000.0,"fcf_margin_pct":26.99,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-04-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/NTAP/NTAP_Q1_2027_Earnings_Call_20260902.md）

# Q1 2027 Earnings Call
**NetApp, Inc.** | Earnings Calls | 2026-09-02

**Operator** (Operator):
Good day, and welcome to the NetApp First Quarter of Fiscal Year 2027 Earnings Call. [Operator Instructions] Please note, this event is being recorded.
I would now like to turn the conference over to Kris Newton, Vice President, Investor Relations. Please go ahead.

**Kris Newton** (Executives):
Hi, everyone. Thanks for joining our Q1 FY '27 earnings call. With me today are our CEO, George Kurian; and CFO, Wissam Jabre. This call is being webcast live and will be available for replay on our website at netapp.com.
During today's call, we will make forward-looking statements and projections with respect to our financial outlook and future prospects, including, without limitation, our guidance for the second quarter and fiscal year 2027, our expectations regarding future revenue, profitability and shareholder returns, the expected benefits from our acquisitions and partnerships, and other growth initiatives and strategies. These statements are subject to various risks and uncertainties, which may cause our actual results to differ materially. For more information, please refer to the documents we file from time to time with the SEC and on our website, including our most recent Form 10-K and Form 10-Q. We disclaim any obligation to update our forward-looking statements and projections.
During the call, all financial measures presented will be non-GAAP unless otherwise indicated. Reconciliations of GAAP to non-GAAP measures are available on our website.
I'll now turn the call over to George.

**George Kurian** (Executives):
Thanks, Kris. Good afternoon, everyone. Thank you for joining us today. We delivered a stellar start to the year, exceeding our Q1 guidance on every metric and delivering a record-setting first quarter. Revenue increased 30% year-over-year to $2.03 billion. Our disciplined approach converted robust top line growth into significant profitability even in a challenging component cost environment with gross profit growing 29% to a record $1.43 billion, operating margin reaching 31.9% and EPS up 66% from Q1 a year ago. Adjusting for the additional week in Q1, our performance still stands as one of the best in the company's history.
This quarter's achievements reflect more than just strong execution. They underscore NetApp's growing leadership in a rapidly evolving environment. Our broad-based success spanned industries and geographies with multiyear agreements, expansion into new workloads and deeper customer engagement, all strong leading indicators of durable growth.
While we're seeing some accelerated purchase decisions and pricing benefits, we are also seeing a clear structural improvement in the underlying demand environment, all of which contributed to Q1 strong results and are fueling our momentum. This exceptional quarter is both a testament to our execution and a clear signal of the expanding opportunities ahead.
Given our strong start and the success we're seeing across our business, we are materially raising our outlook for the year.
AI is no longer a future aspiration. It's a business imperative. As organizations move to operationalize AI, the challenge is not just compute but data readiness. NetApp is a key partner for companies making this shift, eliminating complexity and accelerating time to value at scale. The NetApp Platform enables customers to make all data AI-ready in place, providing unified storage, robust security and a single control plane across hybrid multi-cloud environments, delivering capabilities that redefine expectations in the industry.
By removing the need for data movement, we empower enterprises to accelerate AI and analytics while maintaining governance and control, enabling them to transition from AI experimentation to production with confidence.
The strength of our platform is fueling both deeper relationships with existing customers and new customer acquisition. A recent win highlights this momentum. In a highly competitive evaluation, a major U.S. utility chose NetApp over both legacy and flash-only competitors, displacing the incumbent and standardizing on our unified AI-ready data infrastructure. Wins like this, where a customer entrusts their most demanding workloads to NetApp, are leading indicators of our expanding role in the market and set the stage for long-term growth.
Our record Q1 was fueled by robust growth in public cloud, all-flash and Keystone revenues, reflecting the momentum in our business and validating our strategy as we deliver meaningful results for customers. Driven by strong adoption of our first-party and marketplace storage services, Q1 public cloud revenue grew to $206 million, up 28% year-over-year and up 19% adjusting for the extra week. Customers choose NetApp for our secure, scalable, cloud-native storage services as they migrate workloads to the cloud. VMware workloads, in particular, are among those increasingly being moved to the cloud, opening significant opportunities for NetApp. In Q1, a U.S. hospitality company adopted NetApp technology for the first time through Amazon FSx for NetApp ONTAP, supporting its large-scale VMware migration to AWS.
FSxN delivered superior performance, lower cost and versatile workload support. Similarly, a U.S. public sector organization selected Azure NetApp Files as a part of its data modernization efforts. ANF overcame technical barriers found in other cloud services and enabled substantial cost savings. These wins highlight how NetApp's differentiated cloud storage solutions facilitate seamless, efficient VMware migrations, reinforcing our ability to drive sustained growth as organizations accelerate their cloud adoption. All-flash array revenue reached $1.31 billion in Q1, up 47% year-over-year. Customers are standardizing on NetApp for their most mission-critical workloads, including GPU-intensive AI pipelines that demand high performance, low latency and built-in cyber resilience. Our innovation and go-to-market execution continue to drive share gains in this part of the market.
In today's challenging cost environment, the breadth and flexibility of the NetApp Platform stand as strategic advantages. We empower customers to optimize performance, capacity and budget requirements without compromising cyber resilience or operational simplicity. This value proposition is driving strong customer demand across our portfolio. And notably, we are seeing accelerating interest in our hybrid flash solutions.
Let me share recent examples of how the breadth of our portfolio has enabled us to displace competitors and win new customers. In its first engagement with NetApp, a European IT service provider for pension insurance selected our unified storage to meet stringent security and resilience requirements for critical infrastructure. Our flexible architecture not only supports the availability and integrity of highly sensitive data today, but also provides a secure, efficient and sustainable foundation for future AI workloads. NetApp recently displaced a competitor at a leading transportation agency. Our solution combined all-flash arrays for high-performance processing of massive video files with hybrid flash arrays for reliable, cost-effective long-term retention. Our ability to deliver the scalability, reliability and performance required for advanced analytics and ongoing infrastructure maintenance was key to the win.
AI is powering a new wave of growth for NetApp, momentum that has been building and continues to accelerate. In Q1, we won approximately 350 AI and data lake modernization deals, up significantly from a year ago. Importantly, deal sizes are increasing as customers move from proof of concept to production. Initial wins in prior years are expanding into production-level workloads, reflecting confidence in NetApp's ability to support large-scale AI environments. Our solutions are enabling customers to activate data in place for AI, accelerate time to insight and achieve real business outcomes, putting NetApp at the center of their AI journeys.
Here are a few examples from Q1. We signed a significant agreement with Samsung Electronics to support its EDA environment and AI Center of Excellence. A public sector organization awarded NetApp a strategic deal to modernize and expand its intelligence capabilities and deliver real-time analytics, leveraging NetApp AFX integrated with NVIDIA SuperPOD. AFX's disaggregated architecture provides the flexibility and performance required for advanced AI workloads and provides a future-ready foundation, delivering the power and scalability needed to meet evolving requirements as data demands grow.
NetApp secured a significant win with an Asian neocloud provider, supplying high availability, secure and scalable storage for new customer-facing AI services. Our robust multi-tenancy and deep expertise in large-scale Kubernetes and OpenStack environments set us apart, helping the provider to modernize its infrastructure and support demanding AI inference workloads. This win displaced existing vendors and established a strong foundation for NetApp in one of the provider's most strategic AI initiatives.
We are strengthening our leadership through strategic acquisitions that expand the capabilities of the NetApp Platform and broaden our addressable market. These investments position us to stay ahead as customer needs evolve, deepening our differentiation in cloud and AI.
In Q1, we acquired DataPelago, a recognized innovator in AI data infrastructure. Their Nucleus software engine enables high-performance in-place data processing, eliminating costly data movement and streamlining AI readiness. With this technology, we believe we can unlock additional value from the vast unstructured data already managed on our platform, giving customers fresh opportunities to accelerate their AI initiatives and maximize the potential of their existing data assets. This positions NetApp as the company that makes zero-copy activation of enterprise data for AI real, helping customers drive AI initiatives, improve efficiency and unlock more value from their data.
At the start of Q2, we acquired JetStream, a leader in cloud-native disaster recovery for VMware environments. JetStream enables continuous protection and recovery of VMware workloads across diverse storage environments with seamless replication to NetApp cloud offerings like Azure NetApp Files. This acquisition will allow us to offer a simpler, more flexible path to cloud modernization and positions NetApp as the recovery destination of choice for VMware deployments, even when production data originates from competitors' infrastructure.
NetApp's strong Q1 results underscore our leadership in a transformative era shaped by accelerating AI and cloud adoption. The strength and flexibility of the NetApp Platform allow us to support a diverse and growing customer base. By winning new business, deepening partnerships and investing in innovation, we are building a durable foundation for continued leadership and long-term growth. We are executing with discipline and vision and building on our leadership to deliver sustained value for our customers and shareholders. We are excited to host our annual customer conference, NetApp INSIGHT, in September. We will showcase substantial innovation throughout the NetApp platform, delivering new value for AI and addressing the unique needs of high-growth markets like neo and sovereign clouds. We also will host an investor session to provide more detail on our strategy and solutions, and we hope you will join us.
In closing, I want to thank our employees for their dedication and focus. Our record start to the year is a testament to our team's commitment to our customers and to driving NetApp's continued success.
I'll now turn it over to Wissam.

**Wissam Jabre** (Executives):
Thanks, George, and good afternoon, everyone. In the fiscal first quarter, we delivered exceptional results exceeding the high end of all our guidance ranges. Revenue for the quarter was $2.03 billion, up 30% year-over-year and 4% sequentially. Non-GAAP earnings per share was $2.58, up 66% year-over-year. Revenue growth was driven by broad-based momentum across the business, highlighting the strength of our portfolio. This quarter's results reflect a healthier demand environment as customers invest in AI and modernization as well as some accelerated purchases and pricing benefits. As a reminder, Q1 included an additional week. Revenue was up 26% year-over-year, excluding the effect of the extra week, which contributed approximately $65 million to revenue, primarily in support and public cloud.
Looking at revenue by segment. Hybrid Cloud revenue of $1.82 billion was up 30% year-over-year and 27% adjusting for the additional week. Product revenue of $987 million was up 51% year-over-year. Support revenue of $720 million was up 11% year-over-year and up 4%, excluding the extra week, which contributed approximately $50 million. Professional Services revenue of $112 million was up 15% year-over-year, mainly driven by continued robust growth in Keystone, our storage-as-a-service offering. Q1 Public Cloud revenue of $206 million was up 28% year-over-year and up 19% adjusting for the extra week, reflecting strong demand for first-party and marketplace storage services. The additional week contributed approximately $15 million to Public Cloud. We exited Q1 with $4.85 billion in deferred revenue, an increase of 7% year-over-year. Remaining performance obligations were $5.65 billion, up 14% year-over-year.
Moving to the rest of the income statement. Please note, my comments will be related to non-GAAP results unless stated otherwise. Q1 gross margin was 70.6%, exceeding the high end of our guidance and down 50 basis points year-over-year driven by greater product revenue mix compared to a year ago. Product revenue in the quarter was 49% of total revenue compared to 42% in the same period last year. The headwind from revenue mix was partially offset by year-over-year gross margin expansion across product, support, professional services and public cloud. Gross profit was $1.43 billion, up 29% compared to Q1 2026. Hybrid Cloud gross margin was 68.8%, down 20 basis points sequentially reflecting lower product gross margin and partially offset by improvement in support and professional services gross margin.
Product gross margin was 54.6%, down 150 basis points sequentially, mainly driven by higher component costs and partially offset by better pricing. Our recurring support business continues to be highly profitable with gross margin of 93.2%. Professional Services gross margin was 36.6%, improving 4.5 percentage points sequentially. Public Cloud gross margin was 86.4%, up 70 basis points sequentially and over 6 percentage points year-over-year, benefiting slightly from the additional week. The Public Cloud business has operated above the high end of the 80% to 85% long-term target range in the past 3 quarters. Operating expenses of $784 million were up 11% year-over-year and 5% sequentially, driven primarily by variable compensation and the impact of the additional week, which added approximately $22 million. Operating income was $645 million, up 61% compared to Q1 2026, and operating margin was 31.9%, up 6.1 percentage points year-over-year.
Earnings per share exceeded the high end of the guidance range at $2.58, up 66% year-over-year, more than double the growth rate of revenue, highlighting the operating leverage and our ability to translate that into earnings power.
In Q1, cash flow from operations was $503 million and free cash flow was $401 million. During the first quarter, we returned $302 million of capital to our shareholders with $200 million in share repurchases and $102 million paid in dividends of $0.52 per share. Q1 diluted share count of 200 million decreased by 3 million shares or 1.5% year-over-year.
Our balance sheet remains very healthy. We closed the quarter with $3.6 billion in cash and short-term investments and $2.5 billion in gross debt outstanding, resulting in a net cash position of $1.1 billion. Inventory expanded both year-over-year and quarter-over-quarter as we manage supply and inventory levels to support growing demand. Inventory turns were 6, down sequentially.
Overall, Q1 was an excellent start to the fiscal year, highlighted by strong revenue growth amid heightened AI and cloud-driven storage solutions demand. Combined with our disciplined execution, our revenue growth drove meaningful operating margin and EPS outperformance and robust cash flow generation.
Now turning to non-GAAP guidance, starting with Q2. We expect revenue to be $2.1 billion, plus or minus $75 million. At the midpoint, this implies 23% year-over-year growth. We expect gross margin to be in the range of 67% to 68%, sequentially lower, primarily driven by higher product revenue mix as a percentage of total revenue. We expect operating margin to be in the range of 30.9% to 31.9%. We expect earnings per share to be in the range of $2.54 and $2.64 with a midpoint of $2.59.
Turning now to full year fiscal 2027. We remain confident in the strength of our portfolio and our ability to execute in the current environment. Strong demand and continued business momentum reinforce that confidence and support our increased outlook for the year. We are raising our fiscal year revenue and EPS guidance. We now expect fiscal year 2027 revenue to be in the range of $7.975 billion to $8.225 billion. At the $8.1 billion midpoint, this represents 17% year-over-year growth and an increase of $650 million compared to our prior guidance. We expect gross margin to be in the range of 68.1% to 69.1%. The revised range primarily reflects a higher expected mix of product revenue compared with our prior guidance. At the same time, our fiscal year 2027 product gross margin expectations have improved slightly, while the underlying gross margin outlook for the rest of the business remains largely unchanged. We are raising operating margin to be in the range of 30.3% to 31.3%. We are raising earnings per share to be in the range of $9.73 to $10.03. At the $9.88 midpoint, this represents 22% year-over-year growth.
In closing, as we look ahead to the rest of fiscal year 2027, we remain confident in our strategy and disciplined execution. Our focus stays firmly on delivering strong revenue growth and profitability, strengthening free cash flow and building long-term value for our customers and shareholders.
With that, I'll now turn the call over to Kris for Q&A.

**Kris Newton** (Executives):
Thanks, Wissam. Operator, let's begin the Q&A.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Joseph Cardoso with JPMorgan.

**Joseph Cardoso** (Analysts):
Maybe for my first, if I could. George, you called out accelerating purchase decision and pricing benefits as well as structural improvement and underlying demand at the same time. Can you maybe just walk us through the key drivers that is helping to distinguish between those dynamics? And what drives your confidence around maybe the more durable demand part of that? And just particularly in the context of the outlook, which implies a decline heading into the second half of fiscal year. And then I have a follow-up.

**George Kurian** (Executives):
Thank you for the question. We had an exceptional start to the year. The demand profile was broad-based and we saw strength across every customer type, by size, medium, small, public sector. We saw it across all the geographies, and we saw it across industry verticals, workload solutions, on-prem, Keystone, cloud. So super strong broad-based portfolio strength. I think when we distinguish the 3 buckets, clearly, what we saw in the quarter was counter to what we see typically when prices of silicon and commodity costs go up dramatically, customers generally lean into tech refresh. We saw into maintenance and non-refresh. We saw the opposite. We saw much higher than the anticipated strength across all classes of customers.
Within the largest customers, we saw some pockets of accelerated purchasing. But in many of those customers, we also saw them for less priority workloads and use cases be more moderated in their buying behavior as is typical. And then we saw clearly as commodity prices have gone up, we have adjusted our pricing, and you could see that in the outperformance in our product gross margin relative to our guidance, which is reflected in our ability to capture higher pricing.

**Joseph Cardoso** (Analysts):
No. Got it. George, I appreciate the color there. And maybe just a quick follow-up on the last comments you made. I just wanted to get an update or a clarification on how you're thinking about. I think you believe -- I believe you guys called out product gross margins troughing in the first quarter itself. Is that playing out? And then maybe more specifically, are you realizing the full benefits of the flow-through of the pricing actions you've taken and whether that's already playing now in 2Q? Or should we expect that to still be a tailwind going out into the 3Q or one of the subsequent quarters?

**Wissam Jabre** (Executives):
Yes, great question. And so in Q1, we did outperform our expectations with respect to the product gross margin, as George mentioned. We did have a bit of a favorable product mix associated with the various customer types and the geos that we serve. And so it did help us a little bit.
As we think and we look forward to Q2 and the rest of the year, the outlook very much on product margin has improved slightly relative to our prior guidance that we've provided 90 days ago. And so that's sort of an incremental positive, which basically says we have a bit more confidence in our ability to recoup the incremental costs that we're paying, albeit probably won't be at the same levels we saw in Q1, but I would stress that it would be -- we're anticipating or -- and projecting it to be better than we thought it would be 90 days ago for the rest of the year.

**Operator** (Operator):
Your next question comes from the line of Mehdi Hosseini with Susquehanna Financial Group.

**Mehdi Hosseini** (Analysts):
Yes. I also have a question with 2 parts. George, help me understand how would you break up your customers' investment and splitting modernization, upgrade of existing installed base of a storage from incremental capacity added due to AI inferencing?
And my second question is for Wissam. I'm a little bit confused with the product gross margin trajectory. I think expectation was for gross margin -- product gross margin to be troughing in the mid-50% and improve from there. But your Q2 guide implies that we actually may see a Q-on-Q decline. If you could clarify, it would be appreciated.

**George Kurian** (Executives):
With regard to your first question, Mehdi, we have seen super strong growth in our product portfolio as well as offerings like our all-flash array, Keystone and our cloud storage. Pretty much across the board, we were well ahead of our expectations. And we continue to see that strength durable for multiple quarters, which is why 1 quarter into the year, we have raised the full year materially, including the second half, right? So really, really strong momentum in the business.
With regard to what we saw, there are AI-specific buildouts, which are, for example, GPU as a service cloud, GPU environment within enterprises and data lakes and modern data lake type environment being built, particularly for GPU usage and for AI analytics. There is, however, also as other people have noted, including the hyperscalers, a broad-based modernization of a variety of adjacent workloads and infrastructures, right? So when you use AI, you also want to modernize your databases, you also want to modernize your unstructured data environment to get them ready, and we saw that happening pretty much across all the industries and all the customer segments. So really strong momentum. We're excited for the year, super confident about our position in the market and the alignment to where customers are prioritizing spending.

**Wissam Jabre** (Executives):
And to the second part of the question, Mehdi. Look, we did anticipate -- so maybe I'll explain how we anticipated the product gross margin to be shaped throughout the year 90 days ago. We said that we would see a trough in Q1, and we anticipate a slight improvement for the rest of the year or gradual improvement for the rest of the year.
Now fast forward to today, we did manage Q1 product gross margin in a really great way. I think we did a great job in execution and we outperformed our expectations for Q1. So that's sort of the first point I want to make.
The second point is when we compare now Q2 to Q4 for the rest of the year to where it was 90 days ago, we're now expecting it to be slightly better. So if you think of the prior guidance had product gross margin in sort of the low 50% range if you sort of -- even though we don't guide every number, but that's what was implied in the guidance, what's implied now in the updated guidance for the rest of the year in product gross margin is slightly better than that. That's really the -- hopefully, that clarifies and answers your question.

**Operator** (Operator):
Your next question comes from the line of Amit Daryanani with Evercore.

**Amit Daryanani** (Analysts):
I guess just 2 questions from my side as well. I think one of the big things that investors are trying to figure out is just the durability of growth that you and everyone else is seeing. And if I think about your fiscal year guide, you folks are going to do 26% growth in Q1, ex extra week, it's going to be 23% in Q2. And I think it's like 9% or 10% in the back half of the year. Can you just talk like what is driving that sort of deceleration? And is that exit rate in the back half of 9%, 10%, sort of the right way to think about what the long-term growth should be for the company?
And then, George, you sort of talked about you're seeing clear structural improvement in the underlying demand environment. Can you maybe just help us appreciate like what metrics are you looking at or tracking that give you confidence that this is a structural shift versus perhaps prebuying given all the price increases?

**George Kurian** (Executives):
I think, first of all, we are 1 quarter into our fiscal year and our approach has been to provide guidance that we feel confident about. We have raised the year materially to reflect the strength of our position and have raised the second half of the year right at the start of the year, right? And so I would not say that we are being cautious about the year. We feel really strongly about the performance. I think, as I noted, with regard to what gives us confidence, it is the fact that all of our product lines, all of our customer segments by size, all of the types of commercial vehicles we use multiyear agreements, storage as a service, traditional CapEx transactions as well as the performance through all of our routes to market have outperformed materially and the outlook for the year is very strong. So we feel really, really good about our position both in terms of alignment to customer spend, the overall customer discussions we're having and the expanding opportunities we see across all kinds of customers.

**Operator** (Operator):
Your next question comes from the line of Krish Sankar with TD Cowen.

**Sreekrishnan Sankarnarayanan** (Analysts):
Congrats on the good results. George, my first question is that you kind of closed like 350 AI and data lake deals this quarter. Last quarter is more like 500. I understand the deal sizes are getting bigger. Is there a way you can quantify how much was the deal size and revenue dollars in the July versus April quarter? And from a bigger picture perspective, how much of your revenues is driven by AI? And then I had a quick follow-up for Wissam after that.

**George Kurian** (Executives):
I think it's hard to quantify specifically what percentage of the revenue is driven by AI for 2 reasons. One is there are customer-specific AI-specific environment, right, which is what the 350 deals that we said count toward. These are typically GPU connected AI stack connected deals.
That being said, as we and others have noted, AI is now driving a broad-based modernization and replatforming of the data infrastructure stack so that you can support the needs of high-performance, inferencing use cases, the ability to build cross-application kind of data infrastructures and that is reflected across the strength of our business. So 350 were AI stack-specific use cases, but the overall performance of the business reflects the influence of AI to modernize the entire data infrastructure. And we had signaled many years ago that we had started to see that momentum acceleration. We saw that in Q4. We are off to a super start in Q1. Our outlook for the year is very positive, and we see really good momentum across our entire portfolio.

**Sreekrishnan Sankarnarayanan** (Analysts):
Got it. And then Wissam, a quick question. Your component costs are going up. So is your inventory levels. I'm just wondering, when you look at your products, you kind of spoke about the product gross margin, what is the equation you're solving for? Is it managing product mix or price capture to generate more gross profit dollars? And where are most of the inventory dollars spent on?

**Wissam Jabre** (Executives):
Yes. So Krish, we did exit Q1 with a slightly higher inventory, but that's because, obviously, we continue to manage our supply and secured supply to be able to secure product for the demand growth that we're seeing. What we're basically focused on is the total gross profit for the company. We managed the total gross margin, but also the total gross profit dollars. And as you can see, as the top line grows, we're seeing gross profit dollars growing almost at a similar pace. That's because this is what drives really the earnings power of the business. The -- I think this is best demonstrated when you also sort of take it down to the operating margin line. And you can see how basically any time where we upsided gross profit and gross margin, we tend to generate quite a bit of operating margin leverage. So I don't know if this answers your question.

**George Kurian** (Executives):
I think one of the things we have also -- one of the things we've also worked on to provide customers with the right solution for their use cases, I think we have started to see again the resurgence of hybrid flash in our portfolio and we anticipate a much stronger contribution from hybrid flash. So we're -- as Wissam said, we're trying to solve as many customer problems with the right mix of portfolio and manage the overall business for gross profit dollar growth.

**Operator** (Operator):
Your next question comes from the line of Asiya Merchant with Citigroup.

**Michael Cadiz** (Analysts):
It's Mike Cadiz for Asiya Merchant at Citi. So my first question is regarding pricing. So as pricing actions begin to flow through and materialize in the quarter -- in quarters, how much of the expected pricing benefit do you think has been realized? And are you seeing any change in demand elasticity, albeit early on?

**George Kurian** (Executives):
I think with -- I'll take the demand question and Wissam can address the pricing capture. I think with regard to demand, listen, we have always believed and continue to believe that customers budget in dollars. What we are seeing reflected in the market is that the overall budget priority for data infrastructure and storage has gone up significantly in our customers. Within customers, for example, there are use cases where even at a higher price, they will be prioritizing spending on that. But within the same customer, they may defer till a future quarter a less priority use case. And we have seen that in our customer base.
In some of those customers, they have also decided to go from a flash-based solution to a hybrid flash-based solution for the lower value use case, right? And so I would say that the most important thing that we have seen is unlike in prior cycles with the significant increase in pricing, we are actually seeing broad-based infrastructure spending, and we believe that it is correlated with AI and the modernization requirements of AI.

**Wissam Jabre** (Executives):
Yes. And with respect to the delay between the pricing actions and when we start seeing it. Look, we've taken actions to be more agile in this environment. So the impact of price increases should materialize sooner than in the past. In the past, for instance, it would take probably 2 to 3 quarters to start seeing it. But now we're seeing it much earlier.

**Operator** (Operator):
Your next question comes from the line of Erik Woodring with Morgan Stanley.

**Erik Woodring** (Analysts):
George, I just want to maybe press it as a follow-up to Amit's question earlier, which is I realize we're just 1 quarter into the year, it's early, but your second half revenue is usually up like high single digits versus your first half. And you're guiding it down. And so I understand the desire to remain conservative and provide a guide that you can hit. But given your qualitative commentary about demand, like why couldn't you beat those expectations by 10%, 20%? I just want to make sure we're not missing anything, just as we think about seasonality from the first half to the second half and anything that could be maybe an offset the way that -- the way that we're thinking about normal seasonality. And then a quick follow-up, please.

**Wissam Jabre** (Executives):
Yes. So Erik, this is Wissam. When we think of the seasonality, if you adjust for the extra week in Q1, we are now roughly seeing -- looking at 50-50, maybe a little bit -- when we're talking rounding here, maybe a little bit more than 50% in the second half, a little bit less than 50% in the first half. I mean you can do the math. But that's just basically based on our visibility at this time. We do, however, see as George mentioned in his prepared remarks, really strong structural improvements in the demand. It's broad-based. It's driven by AI workloads. It's driven by modernization, and we basically are looking at that being the driver of revenue for the rest of the year.

**George Kurian** (Executives):
We are 1 quarter in, Erik. We feel really good about business. We've raised Q2 guidance. We've raised the full year guide. We'll tell you more as we play through the year. We are super confident about our position in the market, and we'll tell you more as we play through the year.

**Erik Woodring** (Analysts):
Awesome. Thank you, George. I can hear it in your voice. So I appreciate that, guys. And then Wissam, just one clarification point. The comments that you make about product gross margins and your ability to maybe get a little bit better capture here in the first quarter, is that purely a function of pricing and pricing confidence and kind of confidence in the demand inelasticity response there? I just want to make sure that when we think about your ability to maybe capture slightly better product gross margins, it's because it's a function of price and not necessarily the other side, obviously being the BOM inflation.

**Wissam Jabre** (Executives):
Yes. Look, I mean, my comment is based on everything we see. As we look at -- as we form our outlook and we look -- and we project the business, we put everything that we know in our numbers. And that's really what my comment is about. It has to do with pricing. It has to do with mix. It has to do with multiple factors that basically go -- and of course, the cost side of the equation, that basically goes into forming the final, basically product margin.

**Operator** (Operator):
Your next question comes from the line of Param Singh with Oppenheimer & Co.

**Paramveer Singh** (Analysts):
So you've done a couple of acquisitions -- niche acquisitions recently. And I wanted to understand where do you see gaps in your technology portfolio today? And where does this make sense to buy versus build? And then I had a follow-up.

**George Kurian** (Executives):
I think we are disciplined in our approach to acquisitions. The 2 that we have talked about are tied to cloud and AI. And they provide us with differentiated offerings to accelerate our position in each of those use cases.
With regard to DataPelago, it is really about AI-driven analytics and inferencing where we can accelerate the application processing adjacent to storage, providing customers a better inferencing solution top to bottom.
With regard to JetStream, which we acquired at the start of Q2, it really strengthens our already strong position in VMware migrations to the cloud. We have really good solutions for customers that want to use NetApp to migrate. But for customers that are non-NetApp on-prem, we have a really good starting point with a DR in the cloud solution. So those are the 2 areas, AI and cloud, that we're focused on, and we feel good about the technology portfolio that we have and we are doing tuck-ins to enhance the overall solution value to customers.

**Paramveer Singh** (Analysts):
Understood, George. And then as my follow-up, your guidance implies that OpEx would go up as a percentage of revenue from the 2Q level in the back half. So I want to understand why there is an increase in investment in the back half? And then where would that actually go, whether it's R&D or sales and marketing? So if you could give some color on the investments that you're thinking about for the rest of the year, that would be great.

**Wissam Jabre** (Executives):
Yes, Param, this is Wissam. So the increase is driven really by a couple of areas. One, as we outperform, we're getting -- we have slightly higher variable compensation accruals. And then the second is really continuing to invest in our AI solutions. But when you look at the overall OpEx for the year and you sort of look what is implied in the guidance year-over-year is still -- year-over-year increase for the full year, it still shows basically that the increase is less -- much less than the half of the revenue -- projected revenue growth. So we continue to be very disciplined in how we invest and how we look at our OpEx. That's, of course, because operating leverage and driving operating margin is a key element of our business model.

**Operator** (Operator):
Your next question comes from the line of Wamsi Mohan with BofA.

**Wamsi Mohan** (Analysts):
I have a couple of clarifying questions. I think as you sort of think about the full year, a, would you say that your expectation of hybrid versus all-flash is similar versus your prior expectations? Would you say that given what you're seeing with supply that the upside that you're guiding to would be more driven by one versus other? And I have a quick follow-up, too.

**George Kurian** (Executives):
Listen, I think that if you look at the overall business, all-flash performed exceptionally strongly in Q1, right? It was up 47% year-on-year. So when we look at the overall year, all-flash still blows out our prior expectations. Hybrid flash, when we had planned the year, we were cautious about customers spending on non-mission-critical workloads. That is typically what they do, right? When you see price increases, customers pull back on capital equipment spending. We are seeing broad-based acceleration in capital spending across the board. And we are -- which is a sign of the AI super cycle. But then we are also seeing customers buying more hybrid flash. I would say if you look at the relative comparison. Listen, all-flash is super strong and will still be the predominant part of the acceleration in our business.

**Wamsi Mohan** (Analysts):
Okay. And as my follow-up, just is there any way you could give us some sense of this magnitude of these accelerated purchases? Going back to Erik's question on half over half seasonality, you guys obviously sound very confident on the outlook over here. But could you just help us through -- think through mathematically, how large was the accelerated purchases or the contribution there, which we should factor in as pull forward? Or is that just acceleration of demand that is coming not necessarily from the second half?

**George Kurian** (Executives):
I think first of all, we're not going to break it out, right? Wamsi, I think what I would tell you is the number of customers and the percentage of our customer base that have the financial flexibility to do accelerated spending is very small, right? These are very large private companies usually. Not even public sector organizations have the flexibility to do accelerated purchasing. So it is a much smaller percentage of customers than you would imagine, right? Very small percentage.
What we saw in the results in Q1 was certain transactions that we expected to be built out over multiple quarters happening within a quarter. That doesn't mean that those same customers didn't defer other projects to accommodate these projects, right? And so I would tell you that it's a percentage of our business, we did not see it in Q4, but we saw it in Q1, and we felt like it was appropriate for us to acknowledge it. But it is not a material part of the overall business. In certain clients, as we talk about, they are kitting out multiple data centers. They wanted to kit out. They said, let's do 2 of the 4 that we want to do faster this calendar year and we'll come back for the other 2. We had expected kind of a more gradual build-out of those. That is not common and widespread across the customer base.

**Operator** (Operator):
Your next question comes from the line of Steven Fox with Fox Advisors.

**Steven Fox** (Analysts):
I was curious if you could talk a little bit more about new customer wins. You mentioned that that was also contributed to growth this quarter. I was curious from the standpoint of what maybe you're leading with and whether it's -- what kind of products, et cetera, and whether you're having success in certain verticals that we should be aware of?

**George Kurian** (Executives):
Thank you for your question. We saw strength, as we said in our prepared remarks, in new customer acquisition, in new workload expansion within existing customers and stronger-than-expected tech refresh in our business. With new customers, we typically attack from 2 different vectors. One is our kind of cloud-based solutions or our purpose-built block optimized solutions for the corporate and mid-market customers and with our unified sort of simplify your infrastructure, unify it on one platform solution for the enterprise. And we feel really good about our position with both new customer counts, new customer dollars as well as expansion within existing customers were all well ahead of our internal forecast.

**Operator** (Operator):
Your next question comes from the line of Katherine Murphy with Goldman Sachs.

**Katherine Murphy** (Analysts):
In line with the following question regarding new customer acquisition through new workloads and new product categories, can you talk more about the success you're seeing in the AFX platform? I know you highlighted a public sector win in the quarter, but anything to share just on the momentum there and how that may be contributing to outlook for the full year?

**George Kurian** (Executives):
AFX is built for the very high end of the performance and scale environment. So the number of transactions are not as many but the size of the transactions are material. We have really focused it on the AI GPU-as-a-service category, and we're seeing good progress. We talked about neoclouds. We talked about the government agency that's building a private AI cloud. And so good progress. It is being certified across a large number of customers, and we're excited to continue to make progress on the solution.

**Operator** (Operator):
Your next question comes from the line of Tim Long with Barclays.

**Timothy Long** (Analysts):
Yes, maybe a follow-on, and then the second one. On the public cloud business, 19% growth ex the extra week is still very good growth rate. We've seen it kind of around that number for the last 1.5 years or so. So just curious, is there anything in the pipeline or new solutions or customer bases or anything that could maybe accelerate that number?
And then second, on Keystone, I did want to touch on that, you talked about growth and strength there. Looking at the professional services line and backing out an extra week, it doesn't look like it grew that much and we're kind of seeing or hearing about more as-a-service purchases in that area instead of paying up for more expensive hardware-based solutions because of the NAND price increases. So just talk about what you're seeing with those as-a-service solutions. I'm surprised we're not seeing a little bit more acceleration in that.

**George Kurian** (Executives):
I think with regard to the public cloud business, listen, it stayed in the high teens as we have scaled the business. So I'm encouraged by the sustained momentum of the business. Obviously, the cloud storage business performed at a much higher level than that. And so we continue to see strength in the 1P or the first-party and marketplace storage services.
With regard to the things that we're bringing out, please come to INSIGHT. We have more AI solutions with the hyperscalers. We have more use cases combining data on-prem with hyperscale cloud and we have brought block storage and lower cost price points in multiple clouds, including Google and Amazon. So really good progress across the portfolio in cloud.
With regard to Keystone, without giving you a specific number, I will just say our Keystone business grew roughly in the same ballpark as prior quarters and in the same ballpark as our overall flash business, which is a really strong number. So we're excited about the progress of the business. We are seeing more new customers that we are targeting with Keystone, and we are bringing more capabilities to that part of our portfolio.

**Wissam Jabre** (Executives):
And Tim, just to add to what George said on Keystone, keep in mind, Keystone didn't really benefit much from the extra week, it benefited a very, very minimal amount.

**Operator** (Operator):
Your next question comes from the line of Victor Chiu with Raymond James.

**W. Chiu** (Analysts):
So inventory nearly doubled sequentially. Just kind of wondering, is that a function of trying to secure NAND and other components against expected demand? And maybe how much you have the inventory increases earmarked to specific customer orders and backlog? And a follow-up there is, does the inventory buildup kind of give you better visibility into the remaining year and into next year?

**Wissam Jabre** (Executives):
Yes. I didn't get the second part of the question. But on the first part of the question, most of the inventory buildout was some strategic purchases and basically us managing inventory to be able to ship to our customers based on the strength of demand. So I wouldn't say -- in my mind, this is a positive. We're really making sure that we have the supply to continue to drive the growth in the business. I'm sorry, could you please repeat the second part of the question? I didn't get...

**W. Chiu** (Analysts):
Yes. Does the inventory buildup kind of give you better supply and cost visibility, I guess, throughout this year and into next year?

**Wissam Jabre** (Executives):
Yes, it typically does.

**W. Chiu** (Analysts):
Pricing is going to be less of a function for growth now, I guess.

**Wissam Jabre** (Executives):
You're correct. It typically does.

**Operator** (Operator):
Your final question today comes from the line of David Vogt with UBS.

**David Vogt** (Analysts):
Great. So I'm going to keep it brief, George. You've answered a lot of questions. But just a question on demand as we think about the next couple of quarters, is there any sort of seasonality that you saw in the most recent quarter, particularly as we go into subsequent quarters from industry verticals? I know if we go into the October quarter, obviously, there are customers that have different fiscal year-end. Did you see any sort of demand maybe slightly different seasonal demand patterns in the quarter? Because I know I think Wissam mentioned that there was a little bit of a pull-in. I'm just trying to get a sense for how do we think about sort of the normal seasonality? Maybe this isn't normal, but how do we think about the seasonality of demand as we move through the back half of this year?

**George Kurian** (Executives):
Listen, I think our Q2 outlook, if you adjust for the extra week in Q1 is roughly in line with typical seasonality. And as Wissam mentioned, second half and first half are within spitting distance of our typical seasonality, right? I think we have a really broad book of business, David. And so the movement of any one customer is not going to affect the broad book of business. I think the one exception to that is typical U.S. public sector seasonality, right? And that you are quite aware of. So we feel really good about the momentum in the business.
Listen, as we said, exceptional start to the year, we had strength across pretty much every part of our portfolio, across every customer type, on-prem and cloud, every geography, we've raised the full year guide. We've raised Q2 guide. We feel really good about the momentum in the business, and we'll tell you more as we get through the year. So super excited.

**Kris Newton** (Executives):
Thank you, David. I'll pass it over to George for closing comments.

**George Kurian** (Executives):
Thanks, Kris. With broad-based momentum, we delivered an exceptional start to fiscal year '27, exceeding our guidance on every metric, strengthening our conviction in the durability of demand and underpinning our confidence in our materially higher expectations for the year. The NetApp Platform addresses a wide range of customer requirements, helping to operationalize AI workflow and accelerating cloud journey, driving new customer wins and deepening existing relationships. Our ongoing innovation continues to strengthen the value of the NetApp Platform and at our upcoming INSIGHT conference, we'll showcase new solutions that unlock value for AI and in high-growth markets. We're building a durable foundation for long-term success, delivering sustained value for our customers and shareholders.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NTAP_Q4_2026_Earnings_Call_20260528.md
- 2026-05-28｜CFO｜guidance：FY27 毛利率財測區間 68.5%–69.5%（FY27 營收財測 $7.325B–$7.575B、中點 $7.45B）（原話："expect gross margin to be in the range of 68.5% to 69.5%"）
- 2026-05-28｜CFO｜guidance：FY27 營收中點對應年增 8%，前一年為 5%（原話："this implies 8% year-over-year growth"）
- 2026-05-28｜CFO｜guidance：FY27 營業利益率財測 29.1%–30.1%（原話："operating margin to be in the range of 29.1% to 30.1%"）
- 2026-05-28｜CFO｜guidance：FY27 EPS 財測 $8.70–$9（原話："We expect EPS to be in the range of $8.70 to $9."）
- 2026-05-28｜CFO｜guidance：Q1 營收財測 $1.75B–$1.9B（含額外一週）（原話："We expect revenue to be in the range of $1.75 billion"）
- 2026-05-28｜CFO｜guidance：Q1 含額外一週，約貢獻 $65M 營收（原話："Q1 includes an extra week, which is expected to contribute"）
- 2026-05-28｜CFO｜guidance：FY27 指引納入可能出現加速採購的需求（原話："we recognize the potential for pockets of"）
- 2026-05-28｜CFO｜guidance：上下半年季節性：扣除 Q1 額外一週後類似（原話："roughly similar type of seasonality first half, second half"）
- 2026-05-28｜CFO｜guidance：Q2–Q4 相較 FY26 同期為中個位數成長（原話："it gets you still in the sort of mid-single-digit"）
- 2026-05-28｜CFO｜commitment：FY27 打算把最高 100% 自由現金流還給股東（原話："intend to return up to 100% of free cash flow"）
- 2026-05-28｜CFO｜commitment：FY27 股數預計年減低個位數百分比（原話："expect to reduce share count by low-single-digit percentage"）
- 2026-05-28｜CFO｜capital_allocation：宣布回購額度增加 $10 億（原話："announcing an increase in that authorization by $1 billion"）
- 2026-05-28｜CEO｜capital_allocation：M&A：持續評估，不排除也不排除不做（原話："we won't rule anything in"）
- 2026-05-28｜CFO｜margin：產品毛利率 7 月季為底部，之後逐步改善（原話："For us, July quarter is more or less the trough."）
- 2026-05-28｜CFO｜margin：靠調價回應零組件成本上升，效果逐步顯現（原話："price adjustments as we see component costs increase"）
- 2026-05-28｜CFO｜margin：產品毛利率長期目標未調整（mid-50s 到 high-50s）（原話："we're not really moving from our long-term goal or target"）
- 2026-05-28｜CFO｜margin：Public Cloud 毛利率長期目標區間 80–85%，近兩季高於區間上緣（原話："operated within the 80% to 85% long-term target range"）
- 2026-05-28｜CFO｜margin：Public Cloud 成長較快被描述為毛利率順風（原話："it does give us a bit of a nice tailwind to the margin line"）
- 2026-05-28｜CFO｜margin：NAND 價格主要反映在產品毛利率（原話："NAND prices would manifest themselves in"）
- 2026-05-28｜CFO｜margin：Q4 產品毛利率 56.1%，季增 80bp（原話："Product gross margin was 56.1%, up 80 basis points"）
- 2026-05-28｜CFO｜margin：Google 協議抵銷較高零組件成本（原話："offsetting higher component costs."）
- 2026-05-28｜CFO｜margin：管理層也以毛利額年增作為目標（原話："we look at gross profit growth year-over-year as well"）
- 2026-05-28｜CEO｜margin：FY26 營業利益率達 30% 目標（原話："Achieving our full year target of a 30% operating margin"）
- 2026-05-28｜CEO｜risk：坦承可能有部分拉貨（原話："there are probably some amounts of pull forward"）
- 2026-05-28｜CEO｜risk：稱 Q4 損益表上拉貨影響極小，另有看到決策加速（原話："We have seen some accelerated decision-making"）
- 2026-05-28｜CEO｜risk：稱財測已納入拉貨風險（原話："the risks of pull-ins and the dynamics it creates"）
- 2026-05-28｜CEO｜risk：稱可取得足夠供給達成全年展望（原話："can source adequate supply to meet our outlook for the year"）
- 2026-05-28｜CEO｜risk：記憶體與零組件成本上升，以調價平衡成長與毛利（原話："We're managing rising memory and component costs"）
- 2026-05-28｜CEO｜risk：客戶以美元編預算、價格彈性小（原話："customers budget in dollars"）
- 2026-05-28｜CFO｜risk：存貨增加、週轉降至 12（原話："Inventories expanded both year-over-year and quarter-over"）
- 2026-05-28｜CFO｜risk：Q4 支援營收年增部分來自一次性項目（原話："partly driven by a onetime item"）
- 2026-05-28｜CFO｜customer：Q4 大型交易兌現，先前已預告（原話："we mentioned the potential for large deals to materialize"）
- 2026-05-28｜CEO｜customer：Q4 約 500 筆 AI 與資料準備訂單（原話："We had approximately 500 AI and data preparation wins"）
- 2026-05-28｜CEO｜customer：500 筆 AI 訂單全為地端（原話："All of the 500 AI wins are on-prem wins"）
- 2026-05-28｜CEO｜customer：AI 用例分布約 50/25/25（原話："So it's roughly 50%, 25%, 25%, roughly speaking."）
- 2026-05-28｜CEO｜customer：Google Distributed Cloud 協議，NetApp 為資料基礎設施大宗（原話："NetApp was chosen by Google to be a"）
- 2026-05-28｜CEO｜customer：大型 neo cloud 客戶為美國前五（原話："meaning top 5, U.S. neo cloud"）
- 2026-05-28｜CFO｜customer：Unbilled RPO 年增 88%（原話："$807 million, up 88% year-over-year"）
- 2026-05-28｜CEO｜product：Keystone 營收較 FY25 成長約 65%（原話："grew approximately 65% from FY '25"）
- 2026-05-28｜CEO｜product：第一方與 marketplace 雲端服務 FY26 成長 30%（原話："which increased 30% in FY '26"）
- 2026-05-28｜CEO｜product：AFX 為新架構，需要時間（原話："It's a new architecture"）
- 2026-05-28｜CEO｜product：AIDE 可單獨以軟體訂閱變現（原話："monetize that as either stand-alone software"）
- 2026-05-28｜CEO｜product：全快閃占裝機基礎升至 48%（原話："it picked up another 1% to 48% of the installed"）
- 2026-05-28｜CEO｜competition：歐洲航太客戶綠地案取代競爭對手（原話："chose NetApp displacing competitors in a greenfield win"）
- 2026-05-28｜CEO｜competition：調價尚未明顯反映在交易，預期未來一到兩季傳導（原話："We raised prices during the quarter"）
- 2026-05-28｜CEO｜competition：已收緊客戶合約，調價傳導預期一到兩季（原話："We have tightened up our agreements with customers"）
- 2026-05-28｜CEO｜customer：部分客戶可能因通膨環境選擇 Keystone（原話："customers who bought Keystone because they felt that it"）
- 2026-05-28｜CEO｜guidance：預期雲端明年成長快於今年（原話："which should cause cloud to grow faster next"）
- 2026-05-28｜CEO｜commitment：增加銷售資源以支撐展望，如去年（原話："some additional sales resources just like we did last year"）

### NTAP_Citi_s_2026_Global_TMT_Conference_20260908.md
- 2026-09-08｜CFO｜guidance：CFO 說 FY27 全年財測已上調（原話："we basically increased the guidance for fiscal year '27"）
- 2026-09-08｜CFO｜guidance：CFO 說下半年財測也比 90 天前高（原話："the guidance for the second half also is higher"）
- 2026-09-08｜CFO｜guidance：CFO 拆解上下半年營收中點約五五對分（Q1 含多一週）（原話："roughly the revenue is split almost 50-50"）
- 2026-09-08｜CFO｜guidance：被問財測高低端風險，CFO 表示等本季結束再更新（原話："we'll wait until the end of this quarter"）
- 2026-09-08｜CFO｜guidance：CFO 說營運利益率財測中點上調約 120 個基點（原話："increased the operating margin guidance at the midpoint"）
- 2026-09-08｜CFO｜risk：CFO 說分銷通路沒有塞貨的動態（原話："there is no stocking the channel for this type of dynamics"）
- 2026-09-08｜CFO｜customer：CFO 說 Q1 需求跨區域、客戶類型與產業皆成長（原話："we experienced broad-based demand"）
- 2026-09-08｜CFO｜risk：被問供給，CFO 表示對交付財測的供給有把握（部分 LTA、部分承諾）（原話："we feel comfortable about the supply we have"）
- 2026-09-08｜CFO｜margin：CFO 說漲價因素屬通膨環境下正常現象，並把成長歸因於 AI 與基礎設施現代化（原話："pretty normal and understandable and inflationary environment"）
- 2026-09-08｜CFO｜margin：CFO 說 Q2–Q4 產品毛利率預期比 90 天前略好（原話："slightly better product gross margin than we had expected"）
- 2026-09-08｜CFO｜margin：CFO 說全年毛利率財測略低，原因是產品營收占比較高（原話："that's solely driven by the richer product revenue mix"）
- 2026-09-08｜CFO｜margin：被問零組件通膨何時緩和，CFO 說現在下判斷太早（原話："too early to sort of make a call on the component pricing"）
- 2026-09-08｜CFO｜margin：CFO 說零組件成本漲價已轉嫁數季（原話："pass through the component cost inflation"）
- 2026-09-08｜CFO｜margin：CFO 說全快閃與混合快閃的毛利差異不大（原話："we don't have much of a differential on the margin side"）
- 2026-09-08｜VP IR｜margin：IR 提醒不要假設歷來各產品類別的相對毛利在現況下仍成立（原話："I wouldn't necessarily assume that the historical"）
- 2026-09-08｜CFO｜product：CFO 說 AI 案件平均規模變大，從概念驗證走向量產部署（原話："the average size of the deal is now bigger than before"）
- 2026-09-08｜CFO｜product：CFO 說 Q1 全快閃陣列營收年增 47%（原話："the all-flash array business grew by 47%"）
- 2026-09-08｜CFO｜product：CFO 說混合快閃營收連兩季小幅年增，前面是多季下滑（原話："a small uptick in the hybrid flash revenue year-on-year"）
- 2026-09-08｜CFO｜product：CFO 說 CPU 伺服器部署後需要儲存，但規模現在難判斷（原話："It's a bit too early to tell the magnitude"）
- 2026-09-08｜CFO｜product：被問 AI 占營收比重，CFO 說未來 AI 與非 AI 界線會模糊（原話："the line between AI and non-AI could become blurry"）
- 2026-09-08｜CFO｜product：被問儲存 TAM 未來兩三年規模，CFO 說現在判斷太早（原話："it is too early for us to tell where this could be"）
- 2026-09-08｜CFO｜competition：被問 AFX 與 Vast／WEKA 等的差異，CFO 說有客戶處於 AFX 認證階段（原話："some customers that are in certification phase on AFX"）
- 2026-09-08｜CFO｜competition：CFO 稱統一平台是差異化關鍵（原話："which is really the key differentiator for us"）
- 2026-09-08｜CFO｜product：CFO 說公有雲 Q1 剔除多出一週後約成長 19%（原話："for the extra week that we had in Q1, it was around 19%"）
- 2026-09-08｜CFO｜commitment：CFO 說公有雲高個位數以上（high-teens）成長率可持續（原話："the high teens growth rates are sustainable"）
- 2026-09-08｜CFO｜customer：CFO 說對公有雲內 AI 工作負載的能見度有限，因為是客戶的客戶（原話："the visibility isn't as great"）
- 2026-09-08｜CFO｜margin：CFO 說公有雲長期毛利率區間為 80–85%（原話："The long-term range for us is 80% to 85%"）
- 2026-09-08｜CFO｜commitment：CFO 說公有雲毛利率區間暫不調整，但承認有上行偏向（原話："We think there's potentially some upward bias"）
- 2026-09-08｜CFO｜margin：CFO 說 Keystone 對整體毛利與營業利益率有正貢獻（原話："It's accretive to our overall gross margin"）
- 2026-09-08｜CFO｜commitment：CFO 說費用成長不超過營收成長的一半，並稱 FY27 財測仍在此框架內（原話："not to have OpEx grow faster than half of the growth rate"）
- 2026-09-08｜CFO｜capital_allocation：CFO 說資本配置不變，最高將 100% 自由現金流還給股東（原話："return up to 100% of our free cash flow to our shareholders"）
- 2026-09-08｜CFO｜capital_allocation：CFO 說 DataPelago 與 JetStream 是小型技術補強併購（原話："both of these are small tuck-ins"）
- 2026-09-08｜CFO｜customer：被問客戶如何調整預算，CFO 說客戶依業務優先順序編預算（原話："customers budget based on their business priorities"）

### NTAP_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260908.md
- 2026-09-08｜George Kurian｜guidance：CEO 描述新財年開局強勁，並稱各產品線、地區皆優於計畫（原話："It was a super strong start to the quarter, to the year."）
- 2026-09-08｜George Kurian｜product：全快閃陣列營收創紀錄、年增 47%（原話："All-flash array revenue was a record, up 47% year-on-year."）
- 2026-09-08｜George Kurian｜guidance：全年產品毛利率展望每季都比年初給的數字逐步上修（原話："product gross margins, it's incrementally up every quarter"）
- 2026-09-08｜George Kurian｜margin：產品毛利率靠提價轉嫁成本，管理層承認無法一對一完全轉嫁（原話："we can't match them always one for one"）
- 2026-09-08｜George Kurian｜margin：公司整體毛利率受產品與服務組合影響，產品成長遠快於服務（原話："product is growing much faster than service"）
- 2026-09-08｜George Kurian｜margin：產品毛利率比 90 天前的預期更好（原話："better than we thought 90 days ago"）
- 2026-09-08｜George Kurian｜margin：AI 專屬配置與一般企業業務的毛利率結構無實質差異（原話："the margin profile, there's no material difference"）
- 2026-09-08｜George Kurian｜risk：被問到 NAND／硬碟供給與定價，管理層表示存貨增加是為了備足供給，並提到現貨與長約並用（原話："inventory was up because we want to make sure"）
- 2026-09-08｜George Kurian｜risk：向供應商採購方式包含公開市場與長期合約（原話："buying in the open market as well as through long-term"）
- 2026-09-08｜George Kurian｜product：快閃成本升高下，磁碟式系統已開始出現成長（原話："our disk-based systems have started to show growth"）
- 2026-09-08｜George Kurian｜risk：管理層給出快閃與磁碟的成本倍數（原話："as the cost of flash becomes 15 to 20x the cost of disk"）
- 2026-09-08｜George Kurian｜product：Keystone（儲存即服務）Q1 表現高於內部目標（原話："were above our internal targets"）
- 2026-09-08｜George Kurian｜commitment：預告在 INSIGHT 大會發布針對高階 neocloud 訓練場景的新進展（原話："We are going to be announcing even more advancements"）
- 2026-09-08｜George Kurian｜customer：AFX 平台客戶需經認證流程（原話："They go through a certification process"）
- 2026-09-08｜George Kurian｜competition：對 neocloud 的銷售模式是夥伴多於供應商（原話："we are more partner than vendor"）
- 2026-09-08｜George Kurian｜customer：主權雲端：法國前八大雲端業者中六家以 NetApp 為基礎設施（原話："6 of the 8 largest cloud providers in France have NetApp"）
- 2026-09-08｜George Kurian｜competition：面對全堆疊綑綁廠商，管理層稱與六個月前相比無根本改變（原話："No fundamental changes from 6 months ago."）
- 2026-09-08｜George Kurian｜competition：管理層點名 NetApp、Pure、Dell 為持平或增加份額的專注型廠商（原話："it's probably us, Pure and Dell"）
- 2026-09-08｜George Kurian｜customer：美國公部門採購干擾已緩解（原話："the disruption from a procurement side has mitigated"）
- 2026-09-08｜George Kurian｜competition：公部門市場管理層稱是與 Dell 的兩強競爭（原話："it's a 2-horse race between us and Dell"）
- 2026-09-08｜George Kurian｜product：公有雲長期以來維持高十位數到低二十位數成長（原話："public cloud has grown in the high teens, low 20s"）
- 2026-09-08｜George Kurian｜commitment：CEO 表示正在向銷售團隊施壓要求雲端更快成長（原話："I'm pushing for faster growth."）
- 2026-09-08｜George Kurian｜customer：舉例：剛把一家大型競爭對手客戶的 AI 資料湖搬上公有雲（原話："moved a large competitive customer to the public cloud"）
- 2026-09-08｜George Kurian｜customer：銷售模式：不直接賣給超大型雲端業者，而是透過它們賣給企業（原話："We sell through them to the enterprise."）
- 2026-09-08｜George Kurian｜product：對儲存而言推論的重要性遠大於訓練（原話："inference is the much bigger part of the overall business"）
- 2026-09-08｜George Kurian｜risk：面對元件漲價，基礎設施升級需求高於正常型態（原話："We are seeing infrastructure upgrades way above normal"）
- 2026-09-08｜George Kurian｜customer：新use case 需求同樣高於正常型態（原話："We are seeing new use cases also way above normal pattern"）
- 2026-09-08｜George Kurian｜capital_allocation：內部 AI 專案由約 400 件收斂，其中 13 件已在損益表貢獻正報酬（原話："that are contributing to positive returns in the P&L"）

### 問答異常語氣（迴避／改口／保留）
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Fox：NAND 漲價推升的營收占比｜答法：CFO 表示 too early，不願量化；CEO 稱這是特殊領域，難以精確告知
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Sankar／Chokshi：AI 相關占產品營收或訂單比重｜答法：CFO 兩次表示不拆分，只給筆數；被問每筆金額是否上升，回答範圍很廣、不願推測
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Mohan：為何 Q4 沒看到拉貨、後續調價節奏｜答法：重申 Q4 損益表拉貨影響極小，未回答調價節奏；後段又承認可能有部分拉貨
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Woodring：FY27 財測有多少來自已取得的 AI 訂單｜答法：未給占比，改談廣泛動能、裝機基礎與銷售投資
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Sankar：neo cloud 大單是否為唯一供應商｜答法：CEO 表示不評論對方環境，只說對方為美國前五 neo cloud
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Wilhelm：AFX 何時成為較大營收來源｜答法：只說需要時間，未給時程或數字
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Singh：AIDE 定價與 ASP 提升幅度｜答法：回答取決於資料量與服務，未給百分比
- NTAP_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：漲價（P×Q）在財測中占多少、持續漲價是否為財測上行空間｜答法：未給任何數字，改談 AI 採用與基礎設施現代化是成長的底層驅動
- NTAP_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：除供給外還有哪些上行因素，以及財測低端的風險｜答法：未回答上行因素或低端風險，只說財測已納入當時所有資訊、等本季結束再更新
- NTAP_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：快閃占比上升對產品毛利率的影響｜答法：確認 Q1 快閃占比較高，但前瞻不拆分；IR 補充不要假設歷來各產品毛利關係仍成立
- NTAP_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：AI 案件未來兩三年可占營收多少｜答法：不給比例，改說 AI 與非 AI 界線會變模糊
- NTAP_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260908.md｜問：FY27 財測有多少 NAND／硬碟已由長約鎖定、多少要以浮動價採購，以及財測內含的元件價格假設｜答法：未給長約占比或價格假設，改談需求可見度、供應商合作與存貨增加

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

`scenario_inputs`（EPS路徑五年、終端倍數、機率、yield、second_stage、Max DD範圍與依據）——你不寫`scenario.json`，那份由程式跑`dd_scenario.py`產生。Bear機率5Y不應<20%(多數25-30%；極強護城河+短期已兌現才壓15-20%)；Bull/Bear散布5Y應比1Y/2Y寬≥50%；Base機率不應>50%；bear機率須註明依據，sourced結構性durability仍硬套bear需說明「為何不採信」否則不得高於base [§3]。
- 內生天花板sanity check：Base情境EPS CAGR貢獻vs§5.R內生天花板(同組數字不重算)→天花板內✅/超出⚠(⚠→Bear機率強制≥30%)。成長熄火：3年後成長率降至15%/10%/5%三情境×Forward P/E壓縮→估值跌幅，作Bear PE錨。三分量拆解(≤80字，Base IRR多少來自EPS複利/re-rate/股息淨回購)：re-rate貢獻≥Base合計IRR的40%→標記「估值依賴型」(`decision_inputs.valuation_dependent=true`) [§3]。
- IRR落點：<8%/yr弱、8-12%中、>12%強、>15%罕見，不作跨檔排序依據。AR=`(P_bull×|Bull5Y%|)÷(P_bear×|Bear5Y%|)`，<2平庸/2-4偏正/≥4顯著，非放鬆機率防線理由。年期硬規則：①表頭終端年=主時距終端年②終端倍數EPS分母年期與現價倍數同源③終端倍數必附≥1個同業現值comp對照 [§3]。10Y二段延伸(`runway_post_y5`=🟢且終端倍數承重，或Base IRR實質來自Y5後)：Y5→Y10 EPS CAGR/10Y累積倍數/IRR。R:R數學假象：下行>15%正常使用；5-15%警示「已接近定價」；<5%失效標「數學假象」禁引用進場判定，改極端Bear(Bear PE×0.8+Bear EPS×0.85)重算(Bear EPS=FY+1 EPS×0.9；Bear PE=成長熄火「降至10%」情境) [§3]。

**Max DD**(`premortem.max_dd`)：填範圍`lo`/`hi`(禁單點，寬度≥10pp)+`path_risk`(🟢0～−30%/🟡−30～−50%/🔴<−50%)；推導依據須寫`reasoning.premortem`。硬接線：🔴且thesis脆弱(`moat.trend`↓或`runway_post_y5`🔴或估值依賴型)→倉位上限下修(6%→≤3%)；🔴但thesis完整→不因波動砍倉，註記「深回撤心理準備」[§2問六]。

**必答項**：`scenario_inputs`三支EPS路徑、終端倍數、Bear/Base/Bull機率、`premortem.max_dd.lo/hi`、`path_risk`。

---

## ④反證裁定

**`premortem.blind_spots[]`（反證唯一居所，違例即無效輸出）**：每條`view`(擇一)｜`evidence`｜`assumption`｜`consequence`｜`ruling`(採納或反駁+理由)｜`watch`(＋`evidence_refs`)。三視角(enum)至少各一條：`論點失敗`(5年後虧50%最可能的故事)／`論點成功但股東經濟變差`／`價格已反映太多`；不適用寫`not_applicable_reason`。steelman、自我攻擊(寫檔前一次inner monologue「最強3個反駁點」，觸及核心論據者併進本紀錄)、trap判斷依據一律引用本紀錄不重寫(`trap_analysis`本欄只交`verdict`🟢/🟡/🔴+`label`，`evidence_for/against`不要填)。視角①與Single Thing對帳(撞上不動/部分重疊回補/獨立則重寫)。**降位不得安靜刪門檻**：前份反證帶指標門檻，本輪降位仍須保留「指標＋門檻＋資料來源」，取不到值標「資料缺口」，確實不成立才退休並在`contradictions[]`寫理由 [§0.5(一)][§2問六]。

**`contradictions[]`**：先列一致判斷，再列矛盾(矛盾點/A側/B側/性質：可調和=程度差異、不可調和=方向相反)；⚖不可調和矛盾必填裁決：選哪邊/依據(非「直覺」)/硬數據點/執行路徑(≥1 if-then＋1反向條件，動作具體如加碼至X%/清倉，禁「再評估」)；Steelman義務：觀望迴避寫「現在就買的最強論證」，進場寫「現在就賣的最強論證」。前份漂移歸因：`drift_watch`20欄按`cause`三選一(`價格變動`/`新證據`/`方法變動`)分組，`prior_field`填涵蓋欄名陣列，漏一欄＝FAIL；門檻或Single Thing與前份不同須歸因「舊→新＋理由」，`rearm_trigger`不得寫「相同」；觀望須點名binding constraint，`rearm_trigger`=該約束的否定，多因素模糊觀望=重寫 [§5]；前次觀望/迴避且報酬>+30%須明寫翻面理由；前份在90天內：`decision_inputs.qc49_inherit_prior`答一題——前份觸發器全部沒發火填`true`，有任一條已發火填`false`並在contradictions引用那條；`prior_verdict`／`prior_role`由程式帶入，不要填 [§4]。

**負向證據強制處置（硬擋）**：`findings_digest[]`每條`direction="-"`的finding必落於`contradictions[]`/`blind_spots[]`/`triggers[]`/`moat.threats[]`/`thesis.R[]`之`evidence_refs`，或寫進`evidence_dismissed[]`(`{"ref":…,"reason":…}`，理由需指出證據本身問題，禁「影響不大」)。`triggers[]`每列`n`/`text`/`type`/`maps_to`/`metric`/`threshold`/`action`/`source_freq`/`date`；type僅八值(假設驗證/風險/Single Thing/估值rearm/加碼/減碼/清倉/複審日期)，H1-H3或R1-R3寫`maps_to`不塞`type`。`kill_metrics[]`陣列，每條`metric`/`bear_threshold`/`window`＋`source`；`rearm_trigger`=估值rearm/進場首倉列；`catalysts[]`type英文六值`product`/`regulatory`/`capacity`/`guidance`/`macro`/`other`(禁中文)。QC-39產業態勢三軸(必填一句)：A競爭惡化/B結構轉好與durability/C其他結構變數(法規/關稅/反壟斷/通路/商模/替代技術/客戶結構)→裁決=競爭惡化中/結構性轉好中/其他結構變動中(指名哪軸)/雙向拉鋸/靜態＋一句sourced依據，禁只報單向 [§6]。重大事件：M&A(>市值5%)/集體訴訟/臨床或FDA讀數/CEO或CFO離職或SEC調查/客戶流失皆🔴，涉核心假設或護城河須入`thesis.R`或`moat.threats` [§5][§6]。

**必答項**：三視角blind_spots各至少一條、不可調和矛盾的⚖裁決、`evidence_dismissed[]`(若有負向finding未落點)、`kill_metrics[]`、`rearm_trigger`。

---

## ⑤決策輸入與行動條件

**`decision_inputs`**（值可`null`，`dd_decision.py`機械路由裁決）七欄：`thesis_irreconcilable`(§4不可調和)｜`valuation_dependent`(re-rate貢獻≥Base IRR 40%；程式依你的情境算後覆寫，你填的僅供對照)｜`market_wrong_reason_given`(市場錯在哪的具體理由)｜`week26_return_pct`(26週漲幅)｜`momentum_overheated`(RSI 14d>70或4週漂移>+10%)｜`cycle_gates_pass`(反動能五閘全過，循環股)｜`consensus_rev_3m_pct`(FY1/FY2共識近3月上修%)，缺值`null`。覆寫層：`val_denominator_disputed`/`qc49_inherit_prior`+`prior_verdict`+`prior_role`/`held_now`(bool三態不可`"unknown"`代`null`)；`asym_ratio`/`irr_base_pct`/`ev5y_pct`一律`null` [§5]。

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
{"date":"20260518","verdict":"B 觀望偏進場·thesis 完整等估值或時機修復（Q4 5/28 法說催化）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Keystone STaaS 成為主要成長引擎，從目前約 5% 占比擴大至 15%+ 並進入穩定 ~30% YoY 成長","columns":{"2Y 驗證點（2026-28）":"Q4 FY26 ~ Q4 FY28：YoY 從 +65% 收斂至 +35%（穩態前奏）；占營收 ≥ 10%","5Y 驗證點（2028-31）":"FY29-31：穩態 ~30% YoY；占營收 ≥ 18%；ARR sourced floor $1.5B","10Y 驗證點（2031-36）":"FY31-36：穩態 +20% YoY；占營收 ≥ 30%；成熟期","驗證指標":"Keystone billings YoY%，unbilled RPO 季度增長","資料來源":"2Y: §6 / 5Y: §8 A / 10Y: §8 A + §9 趨勢"}},{"id":"H2","text":"All-Flash + AI 引擎建立第二曲線，AFF + AFX 取代傳統 hybrid array 並進入 NVIDIA AI factory standard architecture","columns":{"2Y 驗證點（2026-28）":"FY26 末：All-Flash 占系統安裝基數 ≥ 50%（目前 45%）；NVIDIA DGX SuperPOD 部署數 ≥ 30 個","5Y 驗證點（2028-31）":"FY30：All-Flash 占系統安裝基數 ≥ 70%；AFX disaggregated 在 hyperscaler reference design 中 ≥ 50% 共享","10Y 驗證點（2031-36）":"FY35：傳統 hybrid 業務","驗證指標":"All-Flash 占比，NVIDIA 認證系統部署數，AFX Rev","資料來源":"2Y: §6 / 5Y: §8 A 路線圖 / 10Y: §9 護城河趨勢"}},{"id":"H3","text":"估值重新評價，從「成熟 storage」（Fwd PE 14-15x）→「AI 數據基礎設施 + hybrid cloud 平台」（Fwd PE 18-22x）","columns":{"2Y 驗證點（2026-28）":"FY27：Fwd PE 進入 16-18x（修復至 5Y 均 19.36x 的 85-95%）","5Y 驗證點（2028-31）":"FY30：Fwd PE 進入 20-22x（PSTG 與 NTAP 折溢價收斂）","10Y 驗證點（2031-36）":"—","驗證指標":"Fwd PE 5Y 分位、PEG 比、與 PSTG fwd PE 折溢價","資料來源":"2Y/5Y: §13"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"PSTG 持續搶 hyperscaler 大單（Meta Mar 2026 已得手）；若 AWS/Azure/GCP 中任一將 NTAP 從 first-party 降為 second-party，moat 結構性受損","columns":{"對應假設":"H2","時間尺度":"🔥 中期（2-3 年）","監測指標":"三大雲 first-party status；hyperscaler RPO 占比","警戒閾值":"連 2 季 NetApp first-party Rev YoY"}},{"id":"R2","text":"Public Cloud services GM 結構性壓縮。目前 83%，目標 80-85%；hyperscaler 拆分搶 margin 後可能下行至 70-75%","columns":{"對應假設":"H3 + H2","時間尺度":"⚡ 短期（12 月）","監測指標":"Public Cloud GM","警戒閾值":"連 2 季 GM"}},{"id":"R3","text":"傳統 Hybrid Cloud 業務（佔 90%）成長失速 + 替代品（VAST Data、WEKA、DDN）侵蝕 AI 訓練 reference design","columns":{"對應假設":"H1 + H2","時間尺度":"🐢 長期結構（5+ 年）","監測指標":"Hybrid Cloud Rev YoY；VAST/WEKA/DDN AI training 部署數","警戒閾值":"Hybrid Cloud 連 4 季 YoY"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":119.93,"archetype":null,"cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名的每一個**（含程式稍後才會算的 asym_ratio／bull_5y_price／bear_5y_price／p_bull_pct／p_bear_pct／ev5y_pct／irr_base_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NTAP_20260930/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
