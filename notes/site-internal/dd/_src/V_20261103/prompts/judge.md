你是 stock-analyst **v20 判斷 agent**，標的 V（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"V","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/V_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/V_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_revenue_gaap","label":"Net revenue (GAAP)","value":12139,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001403161/000140316126000126/q42026earningsrelease.htm"},"note":"未查"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin（淨營收 − non-GAAP 營業費用 4,051，自算）","value":8088,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m；利益率 66.6%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001403161/000140316126000126/q42026earningsrelease.htm（non-GAAP opex 4,051、+12% YoY）"},"note":"未查"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":7262,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD m；利益率 59.8%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001403161/000140316126000126/q42026earningsrelease.htm"},"note":"未查"},{"id":"f_kpi5_guidance_fy2027_q1_fy27","label":"Guidance：FY2027 與 Q1 FY27（二手來源，未見於新聞稿本文）","value":"FY27 調整後固定匯率淨營收成長 low double digits；營業費用成長 low double digits 略低於營收；EPS 成長 low double digits 至 low teens；VAS 成長 low-to-mid 20s。Q1 FY27 淨營收 low double digits（較 Q4 約低 1 點）、EPS 成長 low end of mid-teens","period":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）；財測於 earnings call 說明","unit":"文字","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）；財測於 earnings call 說明","citation":"二手：kucoin / zacks 對 2026-10-27 call 之整理（新聞稿無財測）；官方逐字稿待核"},"note":"未查"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_v_gross_margin_pct","label":"V 毛利率","value":79.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_v_operating_margin_pct","label":"V 營業利益率","value":65.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_v_fcf_margin_pct","label":"V FCF 利潤率","value":44.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ma_gross_margin_pct","label":"MA 毛利率","value":78.42,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MA.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ma_operating_margin_pct","label":"MA 營業利益率","value":60.07,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MA.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ma_fcf_margin_pct","label":"MA FCF 利潤率","value":42.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MA.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_axp_fcf_margin_pct","label":"AXP FCF 利潤率","value":19.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AXP.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cof_fcf_margin_pct","label":"COF FCF 利潤率","value":45.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COF.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pypl_gross_margin_pct","label":"PYPL 毛利率","value":45.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pypl_operating_margin_pct","label":"PYPL 營業利益率","value":18.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pypl_fcf_margin_pct","label":"PYPL FCF 利潤率","value":18.37,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_free_cash_flow_fy2026_23","label":"Free cash flow（FY2026 全年＝營業現金流 23,728 − 資本支出 1,671；新聞稿現金流量表僅提供全年）","value":22057,"period":"FY2026 全年（截至 2026-09-30，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"FY2026 全年（截至 2026-09-30，公告於 2026-10-27）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001403161/000140316126000126/q42026earningsrelease.htm"},"note":"不適用"},{"id":"f_kpi4_sbc_gaap_fy2026_sbc_928_","label":"SBC 占 GAAP 營業利益（FY2026 全年 SBC 928 ÷ 營業利益 28,110）","value":3.3,"period":"FY2026 全年（公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"FY2026 全年（公告於 2026-10-27）","citation":"公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001403161/000140316126000126/q42026earningsrelease.htm"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":426.3,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":30.95,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":75.41,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（15.03 → 15.03）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（17.13 → 17.13）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.05,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.52 → 19.51）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":15.03,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":17.13,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":19.51,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":13.95,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 13.19 → 15.03（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":34.6,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":17.36,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝51.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":51.7,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":17.53,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝50.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":50.5,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":28.36,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 15.03，分子＝快照價 426.32","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.629,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":7988.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 22071.0、現金 14083.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1869.01,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":804633.06,"period":"2026-11-03","unit":"USD m","basis":"市值 796645.06 ＋ 淨負債 7988.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":51023.94,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（32 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":56478.33,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（29 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":15.77,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 425.93 / W52 342.76 / W104 339.24 / W250 276.88 / W250 13週斜率 1.21%"},{"id":"f_ma_w52","label":"52 週均線","value":342.76,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":339.24,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":276.88,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.21,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Visa 10-K FY2025 指出新科技與創新正催生許多偏離傳統網路支付模式的新進入者（GenAI 代理商務、區塊鏈、穩定幣等），且部分國家監管環境正在催生本地網路或額外的處理端競爭。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm","excerpt":"These advances are enabling new entrants, many of which depart from traditional network payment models. In certain countries, the evolving regulatory landscape is creating local networks or enabling additional processing competition.","as_of":"2025-11-06","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 指出即時支付（RTP）網路已在至少 80 國上線，由政府推動（FedNow、PIX、UPI），成為卡組織的替代方案，跨境 RTP 連結亦將與 Visa 跨境業務競爭。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm","excerpt":"RTP networks have launched in at least 80 countries and continue to be driven by strong government sponsorship and regulatory initiatives to enable and drive adoption (e.g., FedNow in the U.S., PIX in Brazil and United Payments Interface (UPI) in India), increasing their position as an alternative to payment card schemes.","as_of":"2025-11-06","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Visa 高層表示穩定幣需求在美歐偏弱，但在跨境、匯款與 B2B 強勁。","source":"paymentexpert.com Visa stablecoins strong Q1 results","url":"https://paymentexpert.com/2026/01/30/visa-stablecoins-strong-q1-results/","excerpt":null,"as_of":"2026-01-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Capital One 已完成借記卡轉 Discover 網路，正測試信用卡遷移，後續依測試結果決定規模與時程（聚合站摘要，2026-07）","source":"Pluang news feed: Capital One uji pindahkan kartu kredit ke jaringan Discover","url":"https://pluang.com/en/news-feed/capital-one-uji-pindahkan-kartu-kredit-ke-jaringan-discover","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Visa FY2022 10-K：一個客戶占淨營收10%（FY2021為11%）；FY2020有兩個客戶分別占11%與10%；FY2018–19無客戶超過10%。未取得FY2023–26數字。","source":"Visa Inc. Form 10-K FY2022 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316122000081/v-20220930.htm","excerpt":"In fiscal 2022 and fiscal 2021, the Company had one client that accounted for 10% and 11% of its total net revenues, respectively.","as_of":"2022-11-18","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"S&P於2018年11月將Visa長短期發行人評級升至AA-/A-1+，展望穩定；2025年4月S&P給予歐元優先無擔保債AA-。搜尋未見2026年評級調整。","source":"S&P Global Ratings via Alacra: Visa Inc.'s Proposed Euro-Denominated Senior Unsecured Debt Rated 'AA-'","url":"https://www.alacrastore.com/s-and-p-credit-research/Visa-Inc-s-Proposed-Euro-Denominated-Senior-Unsecured-Debt-Rated-AA-3361601","excerpt":null,"as_of":"2025-04-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Visa FY26 Q4：恆定匯率支付量 +9%（全年 +9%）、跨境量 Q4 +14%、全年 +13%；處理交易數全年 2,813 億筆 +9%。","source":"Visa 4Q26 earnings release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001403161/000140316126000126/q42026earningsrelease.htm","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Visa 初步 FY27 指引：調整後淨營收低雙位數成長、EPS 低雙位數至低十位數；前提為總經大致穩定、消費韌性。Morgan Stanley FY27 淨營收成長估 11.5%；Seaport 指客戶獎勵金高於預期。","source":"Zacks／Reuters 轉載 Visa Q4 call 摘要與報導","url":"https://www.zacks.com/stock/news/3017664/visa-q4-earnings-call-highlights-fy27-outlook-and-growth-priorities","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FXC Intelligence：跨境旅遊量 Q4 +13%（Q3 +10%）、跨境電商 +17%。","source":"FXC Intelligence ct visa q4 2026 earnings","url":"https://www.fxcintel.com/research/analysis/ct-visa-q4-2026-earnings","excerpt":"Visa grows cross-border volumes with ecommerce and travel gains. Source: FXC Intelligence analysis, company financials. Visa’s reported Q4 2026 is equivalent to calendar Q3 2026. Quarter Cross-border volume Cross-border volume excluding intra-Europe Payments volume Q1 22 40% 51% 20% Q2 22 38% 47% 17%","as_of":"2026-10-28","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K FY2025 風險因素：歐盟 IFR 對消費信用/金融卡跨境與境內交換費設 30/20 bps 有效上限，歐盟執委會宣布將再做影響評估，可能降低上限並擴大管制範圍；Visa 2019 與歐委會和解的跨境交換費限制已延長至 2029。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm","excerpt":"The European Commission has announced its intention to conduct another impact assessment of the IFR, which could result in even lower caps on interchange rates and the expansion of regulation to other types of products, services and fees.","as_of":"2025-11-06","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K FY2025 風險因素：Visa 受多項涉及競爭/反壟斷法的訴訟與調查，反壟斷集體訴訟可能涉及三倍賠償，詳見 Note 20。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm","excerpt":"We are subject to numerous litigation matters, investigations, claims, examinations, information gathering requests, subpoenas, government and regulatory proceedings asserted by civil litigants, governments and enforcement bodies investigating or alleging, among other things, violations of competition and antitrust law","as_of":"2025-11-06","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"加州北區法官駁回投資人就 DOJ 反壟斷訴訟指控 Visa 未揭露的集體訴訟；DOJ 借記卡壟斷案仍在進行","source":"Bloomberg Law: Visa Escapes Shareholder Class Suit Over DOJ Antitrust Complaint","url":"https://news.bloomberglaw.com/litigation/visa-escapes-shareholder-class-suit-over-doj-antitrust-complaint","excerpt":"Visa Escapes Shareholder Class Suit Over DOJ Antitrust Complaint June 30, 2026, 2:24 PM UTC Mallory Culhane Reporter Visa Inc. defeated a shareholder lawsuit claiming it failed to disclose its allegedly anticompetitive practices as the company faced an investigation by the Justice Department. The investor who led the proposed class action failed to plausibly connect","as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"DOJ 持續推進對 Visa 的反壟斷案","source":"Payments Dive: DOJ presses Visa antitrust case","url":"https://www.paymentsdive.com/news/doj-presses-visa-antitrust-case/808859/","excerpt":"DOJ presses Visa antitrust case The Justice Department is pressing ahead with the debit card market case brought against the network during the Biden administration.","as_of":"2026-01-06","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Visa 10-K 風險因素：關稅提高、貿易報復、全球貿易放緩屬總體風險，限制跨國企業活動或全球貿易中斷可能實質不利支付量與淨營收；超過半數淨營收來自美國以外。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm","excerpt":"Adverse macroeconomic conditions within the U.S. or internationally, including but not limited to recessions, inflation, rising interest rates, increase in tariff rates, high unemployment, currency fluctuations, actual or anticipated large-scale defaults or failures, rising energy prices, a slowdown or disruption of global trade, trade retaliation, government shutdowns, and reduced consumer, small business, government, and corporate spending, have a direct impact on international commerce.","as_of":"2025-11-06","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Visa 受 OFAC 制裁約束，不允許位於全面制裁地區（古巴、伊朗、北韓、克里米亞等）或 SDN 名單的機構發卡或交易；2022 年 3 月已因制裁暫停俄羅斯業務。","source":"SEC EDGAR 10-K FY2025 Item 1 / Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm","excerpt":"In March 2022, we suspended our operations in Russia due to economic sanctions imposed on Russia, impacting Visa and its clients. As a result, we are no longer generating revenue from domestic and cross-border activities related to Russia.","as_of":"2025-11-06","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2018 年 Visa 歐洲主資料中心交換器故障致約 520 萬筆交易失敗，備援交換器未啟動（單點失效舊案）","source":"DatacenterDynamics: Visa details cause of widespread outage, blames data center switch failure","url":"https://www.datacenterdynamics.com/en/news/visa-details-cause-of-widespread-outage-blames-data-center-switch-failure/","excerpt":null,"as_of":"2018-06-25","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY26 Q4 淨營收 $12.1B +13%；全年 $45.9B +15%（固定匯率 +14%）；支付量 Q4 +9%、跨境量 Q4 +14%（全年 +13%）、處理筆數 74.2B +10%；國際交易營收 +8% 至 $4.1B，落後跨境量成長（波動度較低與組合）","source":"Visa 4Q26 Earnings Release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0001403161/000140316126000126/q42026earningsrelease.htm","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"FY27 指引：調整後固定匯率淨營收成長低雙位數、營運費用低雙位數、調整後 EPS 低雙位數至低十位數；加值服務成長低至中 20%（FY26 約 30%）；FY27 約 25% 支付量合約到期續約（FY26 為 20%），客戶誘因可能壓抑淨營收；摩根士丹利模型 FY27 調整後淨營收 +11.5%","source":"Zacks: Visa Q4 earnings call highlights FY27 outlook and growth priorities","url":"https://www.zacks.com/stock/news/3017664/visa-q4-earnings-call-highlights-fy27-outlook-and-growth-priorities","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"美國信用卡 interchange 和解修訂版於 2026-06 獲法院初步核准：公告信用卡 interchange 上限 1.25%、平均有效信用費率降 10bp 為期五年；Durbin/Marshall 於 2026-01 重新提出 CCCA，尚未立法；Durbin 引用 Visa+Mastercard 約占美國通用信用卡流通張數 84%；未找到 2026 Visa 單獨市佔數字","source":"America's Credit Unions / Payment Expert / Digital Transactions","url":"https://www.americascreditunions.org/node/27531","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear","triggers"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Visa 10-K 自述：穩定幣在法規明朗後可運作全球 24/7、支援跨境，B2B 區塊鏈/穩定幣支付為 CMS（如 Visa Direct）的替代競爭來源；ACH、RTP、電匯亦為替代方案。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm","excerpt":"We compete with alternative solutions to our CMS (e.g., Visa Direct) such as ACH, RTP and wires.","as_of":"2025-11-06","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Visa 10-K 風險因子：2025 年 7 月美國 GENIUS Act 建立穩定幣監管框架，穩定幣可能顛覆現有支付網路，尤其跨境與 B2B。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm","excerpt":"With more regulatory certainty and permissive or favorable regulations, stablecoins could potentially disrupt existing payment networks, including in cross-border and B2B transactions.","as_of":"2025-11-06","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Visa 10-K 指出 GenAI/agentic commerce 對 Visa 既是創新機會，也帶來競爭與新的資安風險。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm","excerpt":"GenAI and agentic commerce solutions have emerged as an opportunity for Visa, its clients, suppliers, sellers and partners to innovate more quickly and better serve consumers.","as_of":"2025-11-06","retrieved_at":"20261103","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"分析師觀點：穩定幣被廣泛視為 Visa/Mastercard 最大長期威脅，但缺乏消費者保護與詐欺管理層，短期難全面取代。","source":"Third Bridge perspectives: Disruption or distraction? Why stablecoins haven't shaken the card networks","url":"https://www.thirdbridge.com/en-us/about-us/media/perspectives/disruption-or-distraction-why-stablecoins-haven-t-shaken-the-card-networks","excerpt":"Why stablecoins haven't shaken the card networks Disruption or distraction? Financial 27 Jan 2026 Jonathan King, Analyst US Stablecoins are widely seen as the biggest long-term threat to Visa and Mastercard.","as_of":"2026-03-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"-","claim":"A2A/open banking 對卡量構成雙刃劍；Visa 購入 Tink（$2.15 billion）以布局非卡支付。","source":"American Banker: How Visa and Mastercard are bolstering non-card payments","url":"https://americanbanker.com/payments/news/how-visa-and-mastercard-are-bolstering-non-card-payments","excerpt":"Account-to-account payments are a double-edged sword for Visa and Mastercard.","as_of":"2024-05-28","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 說明 Visa Acceptance Platform（Cybersource、Authorize.net）為雲端架構，提供與電商平台的全通路整合；並列出封閉商務生態、BNPL、加密貨幣（含穩定幣）等另類支付業者，可能同時是夥伴與競爭者。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm","excerpt":"Alternative Payments Providers: These providers, such as closed commerce ecosystems, BNPL solutions and cryptocurrency platforms (including stablecoins), often have a primary focus of enabling payments through ecommerce and mobile channels; however, they are expanding or may expand their offerings to the physical point of sale.","as_of":"2025-11-06","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Hospitality Net 專家評論：Visa Destinations 被視為探索而非分銷，尚未構成飯店分銷結構轉變，是訊號而非轉移。","source":"Hospitality Net Expert Views","url":"https://www.hospitalitynet.org/viewpoint/125000322/is-the-new-visa-destinations-the-beginning-of-a-major-shift-in-hotel-distribution","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Visa FY26 Q2 增值服務約占淨營收 30%、年增 27%；Visa Intelligent Commerce Connect 為 agentic commerce 入口。","source":"TIKR: Visa Just Told the Market Where It Thinks Payments Are Headed Next","url":"https://www.tikr.com/blog/visa-just-told-the-market-where-it-thinks-payments-are-headed-next","excerpt":"Per TIKR’s earlier coverage of the latest quarter, Visa Direct transactions grew 23% year-over-year and value-added services grew 27% in constant dollars, now near 30% of net revenue.","as_of":"2026-06-15","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"FY27 首次 guidance（2026-10-27 隨 FQ4 公布）：調整後淨營收低雙位數成長、調整後 EPS 低雙位數至低十位數成長；FQ4 EPS $3.48 高於共識 $3.43；財測前市場共識 FY27 EPS 約 +14% 至 $15.02，guide 低於該共識成長率。","source":"Zacks/Finimize 搜尋摘要：Visa Q4 earnings call highlights FY27 outlook","url":"https://www.zacks.com/stock/news/3017664/visa-q4-earnings-call-highlights-fy27-outlook-and-growth-priorities","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ4 2026 調整後 EPS $3.48 勝共識 $3.43、營收 $12.14B 小幅勝出；Zacks 列示下季共識 EPS $3.63／營收 $12.23B，當前財年共識 EPS $14.99／營收 $50.66B；Zacks Rank #2。","source":"Zacks: Visa (V) Beats Q4 Earnings and Revenue Estimates","url":"https://www.zacks.com/stock/news/3016446/visa-(v)-beats-q4-earnings-and-revenue-estimates","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價共識：MarketBeat 共識 Buy、均值約 $416.62（2026-09-04）；2026-07-29 為 $405.12，JPMorgan 目標價由 $400 調至 $450。valueinvesting.io 48 位分析師：低 327.46／均 406.19／中位 408／高 472.50（無明確日期）。屬 FQ4 財報前資料，未見財報後目標價分布。","source":"MarketBeat 2026-09-04 / 2026-07-29 alerts；valueinvesting.io","url":"https://www.marketbeat.com/instant-alerts/price-visa-nyse-v-trading-down-11-time-to-sell-2026-09-04/","excerpt":null,"as_of":"2026-09-04","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Visa 2026-08 宣布以 24 億美元現金收購詐欺情報業者 BioCatch（Reuters 報導）；2026-02 宣布向 Advent 買下阿根廷 Prisma 與 Newpay。","source":"Reuters via galvnews：Visa to buy fraud intelligence provider BioCatch for $2.4 billion","url":"https://www.galvnews.com/news_reuters/business/visa-to-buy-fraud-intelligence-provider-biocatch-for-2-4-billion/article_2a115d98-ff2b-5cf2-bbc4-1b498e7f954f.html","excerpt":"Card giant Visa said on Monday it will buy fraud intelligence provider BioCatch for $2.4 billion in cash","as_of":"2026-08-03","retrieved_at":"20261103","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"Cai v. Visa 證券集體訴訟（涉 DOJ 反壟斷）2026-06 遭法院駁回，Bloomberg Law 稱原告未能證明約 7% 股價跌幅與不實陳述的因果關係。","source":"Bloomberg Law：Visa Escapes Shareholder Class Suit Over DOJ Antitrust Complaint","url":"https://news.bloomberglaw.com/litigation/visa-escapes-shareholder-class-suit-over-doj-antitrust-complaint","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"DOJ 於 2024-09 起訴 Visa 借記卡市場壟斷，案件仍在證據開示階段（2026）。","source":"Payments Dive：Visa, DOJ lawyers clash ahead of trial","url":"https://www.paymentsdive.com/news/visa-doj-lawyers-clash-ahead-of-trial/828378/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2026-09-18 Visa 對美國訴訟託管帳戶存入 4.05 億美元，B 類股轉換率下調。","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316126000121/v-20260918.htm","excerpt":"On September 18, 2026, Visa Inc. (the “Company”) authorized the deposit of $405 million into the U.S. litigation escrow account previously established under the Company’s U.S. retrospective responsibility plan (the “Plan”).","as_of":"2026-09-23","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Visa 2026-08 宣布以 24 億美元現金收購 BioCatch。","source":"Reuters via galvnews","url":"https://www.galvnews.com/news_reuters/business/visa-to-buy-fraud-intelligence-provider-biocatch-for-2-4-billion/article_2a115d98-ff2b-5cf2-bbc4-1b498e7f954f.html","excerpt":"Card giant Visa said on Monday it will buy fraud intelligence provider BioCatch for $2.4 billion in cash","as_of":"2026-08-03","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"+","claim":"證券集體訴訟 Cai v. Visa 於 2026-06 被駁回。","source":"Bloomberg Law","url":"https://news.bloomberglaw.com/litigation/visa-escapes-shareholder-class-suit-over-doj-antitrust-complaint","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"Mackmin 集體和解：2025-06-23 法院終局核准 Visa 與 Mastercard 的和解並駁回。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm","excerpt":"On June 23, 2025, the district court in Mackmin granted plaintiffs’ motion for final approval of a class action settlement and entered final judgments of dismissal as to Visa and Mastercard.","as_of":"2025-11-06","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"V","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":79.75,"operating_margin_pct":65.57,"fcf_margin_pct":44.91,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.V","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MA","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":78.42,"operating_margin_pct":60.07,"fcf_margin_pct":42.52,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MA","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"AXP","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":19.82,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AXP","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"COF","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":45.04,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COF","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PYPL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.76,"operating_margin_pct":18.52,"fcf_margin_pct":18.37,"rd_intensity_pct":9.56},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PYPL","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"V"},"financial_history":{"ticker":"V","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-09-30","revenue":29310000000.0,"revenue_yoy_pct":null,"gross_margin_pct":80.44,"operating_margin_pct":67.15,"net_income":14957000000.0,"diluted_eps":7.0,"free_cash_flow":17879000000.0,"fcf_margin_pct":61.0,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-09-30","revenue":32653000000.0,"revenue_yoy_pct":11.41,"gross_margin_pct":79.89,"operating_margin_pct":67.15,"net_income":17273000000.0,"diluted_eps":8.28,"free_cash_flow":19696000000.0,"fcf_margin_pct":60.32,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-09-30","revenue":35926000000.0,"revenue_yoy_pct":10.02,"gross_margin_pct":80.4,"operating_margin_pct":66.96,"net_income":19743000000.0,"diluted_eps":9.73,"free_cash_flow":18693000000.0,"fcf_margin_pct":52.03,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-09-30","revenue":40000000000.0,"revenue_yoy_pct":11.34,"gross_margin_pct":80.36,"operating_margin_pct":66.39,"net_income":20058000000.0,"diluted_eps":10.2,"free_cash_flow":21577000000.0,"fcf_margin_pct":53.94,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/V/V_Q4_2026_Earnings_Call_20261027.md）

# Q4 2026 Earnings Call
**Visa Inc.** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Welcome to Visa's Fourth Quarter and Full Year 2026 Earnings Conference Call. [Operator Instructions] Today's conference is being recorded. If you have any objections, you may disconnect at this time. I would now like to turn the conference over to your host, Ms. Jennifer Como, Senior Vice President and Global Head of Investor Relations. Ms. Como, you may begin.

**Jennifer Como** (Executives):
Thank you. Good afternoon, everyone, and welcome to Visa's Fiscal Fourth Quarter and Full Year 2026 Earnings Call. Joining us today are Ryan McInerney, Visa's Chief Executive Officer; and Chris Suh, Visa's Chief Financial Officer.
This call is being webcast on the Investor Relations section of our website at investor.visa.com. A replay will be archived on our site for 30 days. A slide deck containing financial and statistical highlights has been posted on our IR website.
Let me also remind you that this presentation includes forward-looking statements. These statements are not guarantees of future performance, and our actual results, outcomes or timing could differ materially as a result of many factors. Additional information concerning those factors is available in our most recent annual report on Form 10-K and any subsequent reports on Forms 10-Q and 8-K, which you can find on the SEC's website and the Investor Relations section of our website. Except as required by law, we do not undertake any responsibility to update these forward-looking statements.
Our comments today regarding our financial results will reflect revenue on a GAAP basis and all other results on a non-GAAP nominal basis unless otherwise noted. The related GAAP measures and reconciliation are available in today's earnings release and related materials available on our IR website.
And with that, let me turn the call over to Ryan.

**Ryan McInerney** (Executives):
Thanks, Jennifer. 2026 was a milestone year for Visa. We finished the year with fourth quarter net revenue of $12.1 billion, up 13% year-over-year. This resulted in full year record net revenue of $46 billion, up 15%, the strongest net revenue growth in over 15 years, excluding the post-pandemic recovery and acquisitions. CMS revenue grew 19%, and VAS revenue grew 30%, both in constant dollars and their revenue collectively represents more than 40% of our total net revenue. Our drivers for the year were strong. Payments volume was up 9% year-over-year in constant dollars. Commercial payments volume grew 12% for the year in constant dollars, faster than consumer and the fastest annual growth rate in 8 years, excluding the post-pandemic recovery. Total cross-border volumes, excluding intra-Europe, rose 12% year-over-year with travel up 11% and e-commerce up 15%, all in constant dollars.
We processed 281 billion transactions, up 9% year-over-year and with approximately 80% processing penetration globally. And Visa Direct topped 15 billion transactions, representing about $1.5 trillion in payments volume. While these numbers speak to our strength, in 2026, we also demonstrated that whenever technology changes commerce, we move with it. We anticipate what's next, and we enable its growth as the leading hyperscaler of payments globally. The foundation of all of this is trust. Visa brings trust with our scale, our network and infrastructure, and our products, all delivered through our Visa-as-a-Service stack.
Starting with scale. We have scale in issuance and acceptance. In 2026, we had 5.2 billion credentials, up 6% year-over-year with Latin America crossing the billionth credential milestone, and we continued to grow our credentials globally in a number of ways. We signed new co-brand agreements and expanded existing relationships with marquee brands around the world. In the hotel industry, this included Marriott in CEMEA, Asia Pacific, Latin America and North America. And in the airline industry, this included Air India in Asia Pacific, Copa Airlines in Latin America, Qatar Airways and Ethiopian Airlines in CEMEA. We also had the launch of debit portfolios for Alaska Airlines and Southwest Airlines in the U.S. in addition to our existing credit portfolios with these brands.
In the U.S., we added the new Samsung Galaxy Card and maintained our leadership position with 7 of the top 10 U.S. co-brands. In the affluent space, we recently launched our new Visa Infinite card series, signing with more than 70 issuers in over 40 countries in Q4 alone with more than 15 issuers in Latin America, including Santander in Mexico as part of an expanded relationship with Visa.
Our Flex Credentials have tripled since last year with continued strength from existing players as well as growth from new partners such as Cash App and Chime. We will also soon be launching the world's first stablecoin-linked Visa Flex Credential with Norwegian Block Exchange, or NBX, in Europe. Visa Pay, which connects wallets to any Visa-accepting seller worldwide, has nearly tripled its presence since last year to 11 countries.
In commercial, we have over 15 new fleet clients this year across our 5 regions. We recently renewed our global agreement with WEX to enable B2B travel and solutions for their corporate clients. We also expanded our relationship from Europe to the U.S. with Adyen for their travel clients. And through Visa's multinational program, Newline by Fifth Third will be enabling U.S.-based fintechs to offer Visa corporate cards in 46 countries. Across all of this credential growth, we continue to drive adoption of tokens. Today, over 50% of all available credentials are tokenized, more than doubling from 5 years ago. In 2026, we processed a tokenized transaction in 200 countries and territories for the first time, and now more than 60% of all e-commerce transactions are tokenized.
On acceptance, we have well over 200 million seller locations driven by a more than 40% increase in Brazil, a more than 60% increase in Mexico and a more than 15% increase in India seller locations year-over-year. When we incorporate digital wallets, Visa credentials can be used at more than 200 million additional seller locations. So in total, Visa credentials can be used at more than 400 million seller locations. With this increased acceptance, Visa empowers buyers and sellers with secure ways to pay, such as with Tap to Pay, reaching nearly 85% penetration of face-to-face transactions globally.
And with the final top 100 seller enabling Tap to Pay in 2026, we reached 75% penetration in the U.S., well on our way to the global total. Tap to Phone has driven new small business acceptance with more than 25 million active Visa-accepting mobile devices across more than 100 markets, surpassing more than 1 billion transactions in 2026, with 30% of Tap to Phone sellers new to our ecosystem this year. And for micro sellers in more emerging markets, we have Visa Accept, which has grown to 15 markets in just 1 year.
Throughout all of these efforts, we are expanding our reach to power all types of payments, C2B, B2B, P2P, B2C, G2C and more. In fact, we have the largest money movement platform on the planet with Visa Direct as measured by transactions, volumes and accounts with more than 18 billion endpoints across cards, accounts and wallets, up from 12 billion in 2025. Clients value the trust that this brings, and we have over 40 clients who each used more than 5 different Visa Direct use cases this year.
A recent example of a client adding new use cases is Navy Federal, who we have already partnered with on cross-border remittances, and as part of a broader renewal across consumer and commercial portfolios and VAS, including DPS, they are positioning Visa Direct to support a number of new domestic money movement use cases over time. In addition, Wells Fargo has enabled Visa Direct for cross-border payroll, accounts payable and disbursement payments.
With our credentials, acceptance and our reach, Visa has and will continue to bring scale to the ecosystem. You see this play out across our more than 200 countries and territories. For example, in Asia Pacific in 2026, we renewed and expanded with 3 of the top 4 Australian banks, 3 of the top 4 Indian banks, 2 of the top 4 Chinese banks, initiated new relationships with Japanese clients such as PayPay and Travel Wallet Japan.
Visa also delivers trust through our network and infrastructure. Over the last 5 years, we have invested $15 billion in our network security and resilience, all to provide that 99.9999% of reliability, always-on capability that you expect from Visa. And this year, we tested and strengthened our defenses through our Visa Vulnerability Agentic Harness, which we then open-source to the world. 
We also made progress this year building the next generation of VisaNet to enable the future of commerce through a cloud-native, micro-services-distributed modular architecture that uses open languages and technologies enabling easier scaling and configuration and faster feature deployment. Today, this supports live authorization traffic in production across markets in Latin America and CEMEA, and powers additional payment processing workloads at a global scale.
An important area of future development will be Mainland China as Visa has received approval of our application to prepare from the People's Bank of China. This significant milestone now marks the beginning of our formal preparations to ultimately process domestically on the Visa network.
Another core aspect of our network and infrastructure is enabling new capabilities including blockchain. In 2026, we gained even greater conviction in the opportunity and benefits of extending our network on-chain. Our vision is simple: one network combining fiat, stablecoins and tokenized deposits with interoperability and utility across our infrastructure, bringing the same ease and trust clients expect from Visa. It requires key capabilities across the full on-chain stack, which we have made significant progress on this year.
Specific highlights this quarter include: for the blockchain layer, we were invited to the founding validator cohort for Circle's Arc, adding to our roles on Tempo as a validator and Canton as a super-validator; for the issuance layer, Open USD went live on September 30, with total supply in circulation surpassing $800 million so far through October 15; in the orchestration layer, Visa Direct's stablecoin prefunding and cross-border money movement has moved from pilot to commercial production, and we have our first live partner, Inyo Global, a U.S.-based payments infrastructure provider; in the application layer, our Visa Stablecoin Platform is now available in the U.S., Mexico, Puerto Rico, Colombia, Switzerland and the U.K. with additional countries to follow and the pipeline has more than 300 partners.
And the engagement we are seeing with our more established stablecoin offerings is significant. In stablecoin settlement, our run rate has surpassed $25 billion in annualized volume, up 10x year-over-year. We can now support 10 blockchains, more than doubling from last year and are operating in all 5 regions.
In consulting, with over 60 unique engagements, stablecoin advisory was our fastest-growing Visa Consulting and Analytics practice this year, with nearly half of these projects in Q4 alone. And it continues to be among the top 3 focus areas for our clients alongside AI and cybersecurity.
We now have over 225 stablecoin-linked card programs, up more than 70% year-over-year with 150% plus growth in volume across 5 million cards in more than 50 countries with issuers across crypto exchanges, neobanks, wallets and remitters. That is trust at scale. And the trust that the Visa network and infrastructure represent is only amplified by the products we provide on top of it.
I spoke last quarter about the fundamental changes to the way that we build and ship products enabled by utilizing our agentic toolchain. For example, the Visa Stablecoin Platform enablement for OUSD was designed, built and shipped in 7 weeks with 12 people. This would have taken much, much longer and required many more people without utilizing our agentic toolchain. Today, more than 60% of our global product development and engineering teams have adopted this new way of working with the intent of reaching 100% this year.
One of the key areas of innovation for Visa has been empowering agentic commerce. It is clear that in agentic, trust is the biggest barrier to scale. We believe the best way to break through that barrier is with one simple but powerful idea. Every time someone pays or gets paid, it's with a Visa credential. And as we look at the albeit limited number of agentic transactions today, Visa credentials are being used by consumers, businesses and agents. We have nearly 50 AI partners live and in production including more recently Shopify's Shop Pay, with that number expected to double in the coming months. We are also collaborating with Anthropic to bring their commerce blueprints to our merchant network, combining the intelligence of Claude with the trust, security and global reach of the Visa network.
One of the areas we have identified for fast adoption of agentic has been B2B, and we have had several partners launch and expand offerings. Ramp's agentic bill pay use case is now generally available, and as Ramp businesses use Visa Intelligent Commerce to automate bill payments, payments volume is growing. Airwallex is testing Visa Intelligent Commerce-enabled credentials and integrating them into their native wallet, Airi. BILL's payment agent is piloting Visa Intelligent Commerce to pay invoices, and Billtrust's supplier portal will identify the agent and accept payment.
Our Visa Intelligent Commerce solution is enabling all of this. It provides trust for the user with credentials, agentic tokens and transaction identifiers; trust for the agent with the Trusted Agent Protocol and Agent Directory; and trust for the transaction. Once we have verified the user and agent identity, we need to make sure that the purchase instructions are clear by capturing consumer authenticated intent. And of course, like on any Visa transaction, our rules clarify the roles and responsibilities and processes should something go wrong. It is clear that agentic commerce is here, and Visa's role is clear, delivering trust. 
Another important area of product development has been in our value-added services. In fiscal 2026, our VAS business grew revenue 30% in constant dollars to $14 billion, essentially double our 2023 VAS revenue. Our issuing, acceptance, and risk and security portfolios collectively grew more than 20% in constant dollars this year, a growth rate we believe is sustainable in 2027 for 2 primary reasons: the underlying drivers of revenue and demand from clients. I'll go deeper into each one.
First, transactions, cards and accounts had driven the vast majority of our VAS revenue, more than 80% over the last 5 years, and that will continue as our clients grow, we expand to new clients and develop new products, and we were able to price those products to value. For example, Pismo signed clients in Sweden, Belgium and Guatemala this quarter, bringing the total for the year to 28 countries, almost doubling from last year. Our success has enabled us to sell more products fueled by these underlying drivers.
Now to demand. Cyber-related products are a top priority for our clients. We offer many end-to-end cyber solutions, including several launched this year, and we will continue to invest more over time. The associated revenue spans across the VAS portfolios and represents a meaningful amount of total VAS revenue. We delivered these cyber solutions in 4 areas, all bringing trust to the ecosystem: one, helping our clients collect threat intelligence and detect cyber problems early; two, protecting our client's security perimeter with identity access and behavioral trust solutions; three, ensuring every transaction on and off the Visa network is safe with transaction intelligence solutions; and four, when an active threat does emerge, enabling our clients to maintain service resilience and recover as quickly as possible.
In threat intelligence, our Visa Threat Intelligence Platform combines cyber, fraud, brand, identity and financial crime insights through high-fidelity feeds. We connect these indicators to potential fraud outcomes to help our clients defend against would-be attackers. We also recently invested in Overwatch Data, a financial threat intelligence company whose solutions we will soon be offering to our clients globally.
In identity access and behavioral trust, our authentication and tokenization platforms protect consumer credentials, payment transactions, and merchants' and acquirers' sensitive data. And we are excited about our pending acquisition of BioCatch, a leading provider of behavioral first multi-signal fraud intelligence. With over 1.8 billion devices and 760 million users protected around the world, and serving more than 100 of the largest banks globally, we see the opportunity and need to move further upstream, protecting where most of the fraud occurs today at the account level.
In transaction intelligence, we are enhancing our scaled transaction risk services like Visa Advanced Authorization and Visa Decision Manager with our large transaction model. And our Featurespace solution offers clients a flexible platform to integrate a wide range of risk signals to enrich risk decisions throughout the consumer journey.
And in recovery and resilience, Smarter Stand-In Processing enables clients to deliver seamless, resilient transaction authorization services. And the newly launched Visa Intelligent Authorization empowers acquirers with advanced processing, payment orchestration, risk settings and real-time data across multiple local and global payment methods.
Of course, this list is not exhaustive, and with all of this, we offer our Visa Cybersecurity Advisory Practice to help clients review, design and select the best solutions for them. Our advisory and other capabilities had significant revenue growth this year with successful activation around the Olympics and FIFA and also around other sponsorships in sports and music and our other highly valued consulting engagements. These underlying set of assets and capabilities in this portfolio will drive strong revenue growth well into the future.
Across all our value-added services, we have the people, technology, data, brand assets and reach that our customers are looking for. That is what drove the 30% VAS constant dollar revenue growth in 2026 and is why we expect strong VAS growth in the low to mid-20s in 2027.
2026 was a historic year for payments, and Visa only strengthened our positioning in the ecosystem as the leading hyperscaler of payments globally. We demonstrated our ability to significantly accelerate product development, with the true birth of tokenized agentic commerce transactions powered by Visa, with blockchain infrastructure and platforms designed for payments, with the increased utilization of AI across our business to deliver over 350 product releases, up 25% year-over-year.
We reached new customers with Tap to Phone, Pismo, our B2B travel and fleet offerings, new affluent solutions, and cyber and risk capabilities like Featurespace and A2A Protect and with the first transaction in Syria in well over a decade. We delivered secure, reliable payments, nearly 9,000 transactions per second in over 200 countries and territories every day, up 9% year-over-year. We brought the best of Visa technology to the world for free with the Visa Vulnerability Agentic Harness.
All of this was possible because of what Visa and our brands stand for. Every day, across more than 200 countries and territories, over 18 billion endpoints and more than 400 million seller and wallet locations across consumers, businesses, governments and agents, trust enables all of this. We've seen meaningful growth acceleration this year. And as I look ahead to 2027, one thing is clear. Trust is the next growth vector for Visa. Trust fuels everything we do at Visa every day, and trust will fuel our future.
For more on our 2026 performance and our thoughts on 2027, I will hand it over to Chris.

**Christopher Suh** (Executives):
Thanks, Ryan, and good afternoon, everyone. We closed out our strong fiscal year 2026 with another impressive quarter for Visa. Fiscal fourth quarter net revenue was up 13% year-over-year in nominal and constant dollars, in line with our expectations, reflecting broad-based strength across all our key drivers. In constant dollars, global payments volume was up 9% year-over-year. Cross-border volume, excluding intra-Europe, was up 14%. And total processed transactions grew 10%. EPS was up 17% year-over-year in nominal and constant dollars, better than expected, primarily due to a lower-than-expected tax rate.
Now let's go into the details. U.S. payments volume grew 10% year-over-year, generally consistent with Q3 as we saw several factors from Q3 continuing to play a role, including the cost of fuel, retail, strong Visa Direct growth and FIFA-related spend. From the FIFA World Cup round of 32 matches on July 1 through the final on July 19, we continued to see both U.S. host cities as well as destination cities benefit from the influx of FIFA fans with total U.S. card-present spend payments volume growth elevated above pre and post tournament levels. For the quarter, both the U.S. discretionary and nondiscretionary spend growth remained strong.
Fourth quarter U.S. credit grew 11% year-over-year and debit grew 9%. Growth across consumer spend bands remained relatively consistent with prior quarters with the highest spend band continuing to grow the fastest. We did not see signs of the lower-spend consumer weakening in our volumes. Fourth quarter total international payments volume was up 9% year-over-year in constant dollars, generally consistent with the growth we've seen all year.
Now to cross-border volume, which I'll speak to in constant dollars and excluding intra-Europe transactions. Q4 total cross-border volume was up 14% year-over-year, more than 2 points above Q3, primarily due to travel. Travel-related cross-border volume was up 13%, 3 points of acceleration from Q3, primarily driven by improvements in both CEMEA inbound and outbound. Overall, U.S. inbound cross-border growth for July remained elevated following strong growth in June, reflecting in part the demand around the FIFA World Cup.
Focusing on inbound cross-border card-present spend, U.S. host cities increased by over 20% year-over-year from July 1 to July 19, with the most significant increases driven by fans from Argentina and Colombia. Cross-border e-commerce volume was up 17%, more than 1 point above Q3, primarily driven by retail, including spending on AI platforms.
With that as a backdrop, I'll move to discuss our financial results. Starting first with the revenue components. Service revenue grew 14% year-over-year, above the 10% growth in Q3 constant dollar payments volume primarily due to pricing. Data processing revenue grew 16%, above the 10% growth in processed transactions, primarily due to pricing, higher cross-border transaction mix and value-added services. International transaction revenue was up 8%, below that 14% increase in constant dollar cross-border volume growth, excluding intra-Europe, primarily due to lower volatility levels than last year and mix.
Other revenue grew 40%, primarily driven by growth in advisory and other value-added services, especially marketing services revenue as well as pricing. Client incentives grew 21%, a step-up of nearly 3 points from Q3, primarily due to new deals that were signed in Q3 and early in Q4.
Now to our 3 growth engines. Consumer payments revenue was driven by strong payments volume, cross-border volume and processed transactions growth. Commercial and money movement solutions revenue grew 16% year-over-year in constant dollars with strong growth in the underlying drivers. Commercial payments volume grew 13% in constant dollars, consistent with Q3 and faster than Visa's overall payments volume growth.
Visa Direct transactions grew 23% year-over-year, up nearly 2 points from Q3, primarily due to strength in the U.S. and LAC. Value-added services revenue grew 31% year-over-year in constant dollars to $4 billion, driven by 3 factors: one, underlying business drivers, which included strength in marketing services engagements related to FIFA; two, pricing; and three, the acquisition of Prisma.
Operating expenses grew 12%, consistent with our expectations, driven primarily by marketing and personnel expenses. Nonoperating expense was $57 million, better than expected, primarily due to higher average cash balances. Our tax rate for the quarter was 18.4%, lower than our expectations due to claim of right tax benefits related to recent legal settlements. EPS was $3.48, up 17% year-over-year, better than expected with minimal impact from exchange rates. For our non-GAAP results, Prisma and Newpay added approximately 1 point to net revenue growth, approximately 2 points to operating expense growth and approximately 0.5 point to EPS growth.
In Q4, we bought back $4 billion in stock and distributed $1.3 billion in dividends to our shareholders. We also funded the litigation escrow account by $405 million, which has the same effect as a stock buyback. At the end of September, we had $24.4 billion remaining in our buyback authorization.
Looking at the full year 2026. Net revenue grew 15% to $46 billion, and EPS grew 16% to $13.27. Full year 2026 CMS revenue growth was 19%, and value-added services revenue growth was 30% on a constant dollar basis. This foundation of strong growth will continue in 2027.
So let's get into the guidance details. And a quick note, when I reference 2026 and 2027, I'm referring to our fiscal years. And remember that our guidance is on an adjusted basis defined as non-GAAP results in constant dollars and excluding acquisition impacts. You can review these disclosures in our earnings presentation for more detail. We are still working through regulatory approvals on BioCatch and expect to close no later than the end of the fiscal second quarter, upon which we will provide the expected financial impact.
Now let's cover our underlying assumptions for net revenue growth. As we regularly say, we're not economic forecasters, so we're assuming the macroeconomic environment stays generally where it is today and consumer spending remains resilient. The Middle East conflict brings continued near-term uncertainty, in particular, to CEMEA cross-border travel spend, and our assumptions are that those volumes remain generally indexed to where they were in Q4. This implies key business drivers will be strong and improve modestly from 2026 as we lap the impact of the conflict in the Middle East from last year.
On pricing, for 2027, we expect the benefits of new pricing to be similar in magnitude and timing as in 2026, with the majority going into effect in the back half even more so than in 2026.
On volatility, we expect volatility throughout the year to be generally consistent with Q4 of 2026, which implies a drag for the full year. Q1 is expected to have a slight benefit, and Q2 is expected to have the largest drag followed by Q3.
On incentives, 2027 will be an important year in securing our long-term client relationships to drive long-term success, as we're expecting around 25% of our payments volume to be renewed, including renewals with several large clients. This implies a step-up in the year-over-year growth rate from 2026.
Pulling this all together, with strength across our growth pillars of consumer, CMS and VAS, we expect full year adjusted net revenue growth to be in the low double digits, with Q2 being the growth low point as a result of lapping the very strong performance last year. 
Now moving to expenses. As Ryan highlighted, Visa brings trust with our scale, our network and infrastructure, and our products, all delivered through our Visa-as-a-Service stack. In 2027, we will continue to invest across each of these areas focused on driving sustainable long-term growth. Let me share a few examples. On scale, we will continue investing to grow credentials, drive token adoption, expand acceptance, increase our reach in money movement and enhance our affluent and cross-border offerings while deepening our presence in key markets around the world.
On network and infrastructure, we will continue investing to strengthen the security and resilience of VisaNet and further develop our on-chain infrastructure across fiat, stablecoins and tokenized deposits. And for our products, we'll continue investing to advance agentic commerce, expand our offerings for small and lower middle market businesses, and accelerate product development across value-added services. By driving operational efficiency in our business, we're able to make these important investments and can sustain industry-leading operating margins.
For 2027, we currently expect to grow adjusted operating expense in the low double digits, modestly below net revenue growth. As we think about the cadence of spend, we expect adjusted operating expense growth to be relatively consistent each quarter with a moderation in the fourth quarter as we lap FIFA-related spending.
Now moving to nonoperating expense, which is expected to be between $250 million and $300 million, primarily as a result of lower cash balances. Our tax rate is expected to be about 19%, consistent with our long-term tax rate range of 19% to 20%, up from 2026, primarily due to the lack of claim of right benefits. On capital return, the Board has declared an increase in our quarterly dividend of 16%, and we intend to return excess free cash flow to shareholders through buybacks. All of this results in our adjusted EPS growth to be in the low double digits to low teens.
Moving to Q1. But first to comment on monthly drivers. You may recall that we began providing intra-quarter driver data during the pandemic to give greater visibility into the trends during a period of significant volatility. As the environment has largely normalized for some time now, we believe quarterly trends provide a more meaningful view of the underlying performance of our business. As a result, we will continue to provide monthly drivers data in our earnings presentation through fiscal Q1, after which we will transition back to quarterly reporting. We will, of course, continue to highlight meaningful intra-quarter trends in a Reg FD-compliant manner when we believe prudent to do so.
Now let's look at the drivers through October 21, with volume growth in constant dollars. U.S. payments volume was up 10%, with credit up 11% and debit up 9% year-over-year. For constant dollar cross-border volume, excluding transactions within Europe, total volume grew 15% year-over-year with e-commerce up 17% and travel up 13%. Processed transactions grew 10% year-over-year.
Now moving to Q1 financial expectations, which again are on an adjusted basis. We expect Q1 net revenue growth in the low double digits, just under 1 point below Q4 adjusted net revenue growth, primarily due to a lack of FIFA-related revenue and pricing. We expect Q1 operating expense growth also in the low double digits, modestly below net revenue growth. Nonoperating expense is expected to be about $60 million, and our tax rate in the first quarter is expected to be between 18.5% and 19%. As a result, we expect first quarter EPS growth to be in the low end of mid-teens. As always, if the environment changes and there are events that impact our business, we will remain flexible and thoughtful on balancing short- and long-term considerations.
As Ryan said earlier, trust has always been at the core of Visa, and trust will be key to our growth going forward. As we look to 2027, we remain focused on driving top line performance, executing with discipline and investing in our strategic priorities to capture the significant opportunities ahead.
And now, Jennifer, I'll hand it back to you.

**Jennifer Como** (Executives):
Thanks, Chris. And with that, we're ready to take questions. [Operator Instructions]

**Operator** (Operator):
[Operator Instructions] Our first question comes from Sanjay Sakhrani with KBW.

**Sanjay Sakhrani** (Analysts):
I guess one of the big topics this quarter was the launch of initiatives like Muse and Instinct, and it seems like the pace of adoption of agentic experiences seem to have accelerated. I'm just curious what, Ryan, you guys are seeing in terms of merchant and consumer adoption. And like when do you expect it to actually affect your results in terms of these token initiatives, et cetera?

**Ryan McInerney** (Executives):
I agree, Sanjay, that the quarter was a bit of a tipping point on users being able to experience the type of things we've been talking about on calls like this in other forums for a while now, where you can actually have an agent who can go out on your behalf and execute not just shopping but real transactions and do it either with or without a human in the loop. And I think both Muse and Instinct experiences are good examples of that.
I think it's still very early. If you just look at just even the user numbers that are public for Muse, it's still very early in terms of the number of consumers that are doing this. And certainly, in the big scheme of things in our overall business, it's a very small amount. Having said that, we remain very excited and have deep conviction about agentic commerce and the promise that it offers not just for buyers and sellers but for Visa. Second, we still have high conviction that Visa and our credentials will play an extraordinarily important role in enabling these experiences. And we're glad that during the quarter, people who don't study the industry, Sanjay, like you and others on the call and we do, are starting to see the very early use cases and examples of how powerful this can be both for buyers and sellers.
So we're continuing to invest. We continue to have conviction. We'll continue to work hard across the ecosystem to enable these experiences. And over time, we're optimistic about the impact that it will have.

**Operator** (Operator):
James Faucette with Morgan Stanley.

**James Faucette** (Analysts):
Wanted to ask kind of a follow-on question related to how you're investing in agentic commerce and all the new money movement capabilities. As these flows continue to develop, how much of an opportunity do you expect to genuinely be incremental to Visa versus potentially a migration of existing card volumes? And as we look at '27, do we expect any of these to start to have a meaningful impact on growth or the total P&L?

**Ryan McInerney** (Executives):
I think I'll kind of come back to where I was with Sanjay. It's still very early. So we do have conviction that the opportunity is significant. We do have conviction that there's real incremental opportunities. But as we think about the next 4 quarters in '27, it all remains very small in the big scheme of the enormous size of our business.
The -- a couple other notes in terms of where we see incremental opportunities. One, you mentioned some of the work we've been doing on Visa Direct and things like that. Those are big incremental opportunities. Two, when you think about machine-to-machine payments and the CLI as a commerce interface, there's a lot of incremental opportunities there. And then just more broadly, in the big scheme of things with agentic commerce, are agents finding more buying opportunities for us, are agents making more purchases at more seller locations because they're optimizing based on value, speed, delivery like whatever it is important to the user. Those are opportunities. So I think we remain very excited and have conviction about the opportunities, but I think we all just need to realize that the development of all of this is still quite early.

**Operator** (Operator):
Ken Suchoski with Autonomous Research.

**Kenneth Suchoski** (Analysts):
I wanted to ask just on token pricing. It's very high margin revenue building in fiscal year '27. The guide has a sort of low double-digit revenue growth, low double-digit OpEx growth, EPS sort of low double digits to low teens. I was just curious, like how much token pricing are you embedding in the guide? We're just getting to some questions as to why there's not more EPS growth. If you could just comment on that. And just is the -- is that pricing being reinvested? Or are there offsets on incentives or anything else we should be aware of?

**Christopher Suh** (Executives):
Yes, there's a few different things there. Let me try to address each of them or at least cover your main points. In terms of pricing, I outlined our assumptions on pricing in our guide, the low double-digit adjusted net revenue guide for FY '27. It assumes that the contribution to growth from pricing in '27 is consistent with what we saw in '26. That does include all the pricing plans that we have in motion today. And also, I did note that in terms of the timing that it's slightly more back half loaded in '27 as well. So that's one.
I think you touched on a couple of other things, which ultimately sort of laddered up to an EPS point. On incentives, you brought that one up as well. Incentives, we are anticipating a higher volume of incentives in '27. About 25% of our PV will be renewed versus the 20% we saw in '26. As we said many times, we manage our business to drive net revenue growth, and we have a strong plan for '27. And so as you think about incentives, remember, incentives are a tool. They're a tool that lets us align with a common set of goals and priorities with our partners as we work together to continue to grow the shared business. And in fact, when we have higher incentive volumes and growth, it does lead -- it does ensure that we're securing these client relationships over the long period and is a key ingredient to our long-term growth.
And then finally, you touched on a little bit of the EPS point. Yes, we continue to drive productivity growth. We've been focused. As you know, as we said many times, we're focused on driving both strong top line growth and profit growth as we did in '26, delivering 15% net revenue growth and 16% EPS growth. In order to continue to do that, to grow in our consumer payments business and accelerate the growth in VAS and CMS, we -- it is necessary that we continue to invest in those growth opportunities. And so as you've noticed in our guide for next year, we are continuing to become more efficient, and we're continuing to invest in these growth opportunities. And when we do that, I think we can continue to drive top line and bottom line growth.

**Operator** (Operator):
Bill Carcache with Piper Sandler.

**Bill Carcache** (Analysts):
Following up on your commentary around the significant renewals expected in 2027. As more of your clients leverage your VAS offerings, what are the areas, as you look to the new year, in particular, that you're most excited about beyond your core capabilities? And are you seeing your strength in VAS translate into a deepening of the stickiness in your client relationships?

**Ryan McInerney** (Executives):
Yes. Bill, it's Ryan. In short, yes. Our -- and I would kind of expand it to include both VAS and our CMS offerings. The nature of the client agreements that we are engaged in as we kind of migrated into our 2027 fiscal year, they're much broader, they're much deeper, and they include a much more comprehensive set of both value-added services and CMS services such as Visa Direct, some of the commercial and small business offerings I mentioned in our prepared remarks, all in addition to, of course, our consumer payments capabilities. And what these broader agreements do is they create a stronger, tighter, deeper, hopefully, longer-lasting and more comprehensive client relationship with our clients all around the world. So yes.
And then I think, finally, you asked about some of the specific things in VAS that we're excited about in that context. Well, I would point to a lot of the cyber capabilities that I mentioned on my -- in my prepared remarks. I would point to capabilities like Pismo, which are new areas where we can support our clients, both in core banking and issuer processing. I would point to the advisory work that we've talked about several times in these areas. So all of it are very, very important parts of the types of renewals that you asked about and Chris mentioned.

**Operator** (Operator):
Timothy Chiodo with UBS.

**Timothy Chiodo** (Analysts):
I want to dig in a little bit -- and Ryan, you hit on this. But I want to hit on this a little bit more on the agentic network token. So our understanding is that this token is sort of a bolstered version of the network token. It's more of a scoped network token if you will. It will have all the programmatic aspects, meaning a time window, merchant category code, dollar amount. It will have the upfront intent, as you mentioned in your prepared remarks. All of that gets kind of bundled up into the agentic network token.
The question is how ready are the issuing banks and what do they need to do in order to say, yes, I'm willing to have an agent issue a agentic network token for one of my customers? And related, what about the merchant acquirers that are out there, the PSPs? Are they ready to accept the tokenization handshake, if you will? I know you mentioned Shop Pay is doing this, but I'm wondering about the others.

**Ryan McInerney** (Executives):
First of all, that was a great summary of a lot of the objectives of Visa Intelligent Commerce and our agentic tokens. In short, we are doing the work across the ecosystem to ensure that issuers, acquirers and other ecosystem participants are not only ready but are ready to enable these transactions at scale, and we know how to do this work.
If you look at our history, even just with tokenization pre-agentic commerce, this is the work that we did broadly across the world. I think I mentioned in my prepared remarks now that we have tokenized e-commerce transactions in 200 countries and territories around the world. We know how to do this work to enable the ecosystem.
I also just want to come back and build on your points around these agentic tokens and just put it in context of what we are delivering through Visa Intelligent Commerce. First, we want to make sure that there's an identifiable user behind every agent. So these are -- this is why the identity verification and the tokenization is so important. The second thing we're trying to do is make sure that your agent is your agent, and this is why we've built the agent registration and identification capabilities. The third is that we want to make sure your agent is buying according to your instructions. So these are a lot of the data payloads that you mentioned that ladder up to the intent capture and ultimately, the biometric signature. We want to make sure that there's a clear path to resolution in the event of a problem. So disputes, rules and processes and things like that. And then finally, we want to make sure that this all works securely everywhere in the world for billions of users at scale.
And that is the work that we're doing. We've announced dozens of partners that are utilizing Visa Intelligent Commerce. We're engaged with many dozens more across the ecosystem that are enablers of all this as well as all of our issuing partners and acquiring partners around the world to try to enable it at scale.

**Operator** (Operator):
Bryan Keane with Citi.

**Bryan Keane** (Analysts):
Solid results here. Just wanted to ask about cross-border. We've seen a little bit of stronger cross-border volumes both in travel and then in e-comm, in particular, has kind of jumped into the -- I think it was 17%. Just curious on any details on both travel and e-comm as we head into next year, how we should think about those growth rates and some of the drivers there.

**Christopher Suh** (Executives):
Bryan, yes, total cross-border volume, as you noted, it was 14% with 2 points above Q3. And that difference, as I noted in my prepared comments, was due to travel, which was up 3 points from Q3. Now that improvement was primarily due to improvements in both inbound and outbound in CEMEA. That's the primary driver, but also U.S. inbound remained strong as well in the third quarter. And then, of course, I won't repeat it, but you noted the strength in cross-border, which was up 1 point from Q3.
Yes, I mean, when we look across the cross-border volumes in total, both travel and e-commerce, they are strong. They've been strong throughout the course of FY '26. And when we look at the history of cross-border, they're above the historical levels. I think it is reflective of strong consumer sentiment, strong demand for travel experiences and the fact that e-commerce has also just expanded, and e-commerce now encompasses both discretionary and nondiscretionary things.
So we're seeing strength there. Obviously, when we look out, we're assuming stable drivers, in fact, maybe a slight improvement, depending on the speed of the resolution -- potential resolution of the conflict in CEMEA, but this is something that we'll continue to be very watchful of. But yes, we agree with you. Cross-border in total has continued to be a strength, and that's a good thing for Visa.

**Operator** (Operator):
Darrin Peller with Wolfe Research.

**Darrin Peller** (Analysts):
You mentioned you're going to be doing about 25% of the portfolio in terms of renewals in '27, and I think you did, correct me if I'm wrong, 20% in 2026, so a lot of the portfolio being renewed over a couple of years versus the typical 15% or so per year, but you're still able to grow low double digits. I know we often see pricing pressure on renewals. You're still guiding low double digits. So maybe just touch on the dynamics of these contracts. Is it fair to say you're seeing 2 big years of renewals that normally would be 15% to 20% for the years ahead? And what's driving that pricing power despite the renewals we're seeing?

**Christopher Suh** (Executives):
Yes. I'm glad you said that, actually. First of all, your facts are exactly right. We're looking at about 25% of our payments volume, which is a bigger year than we saw in 2026, which is around the 20% mark. But the key point there, which you pointed out, is we manage the business to net revenue growth, and we have a strong plan for '27 for net revenue growth in the low double digits, inclusive of all the renewal activity that we're seeing -- that we're anticipating seeing in '27.
So I think that's exactly the right way to think about it. And as I said earlier in my previous answer, when we have renewal activity and we're successful in renewing it, it is a great thing for Visa over the long term. It ensures that we have long-term relationships with these very important clients, and that will help us continue to deliver strong revenue growth well into the future.

**Operator** (Operator):
Jason Kupferberg with Wells Fargo.

**Jason Kupferberg** (Analysts):
I wanted to talk about U.S. volume growth. I mean a couple of years ago, we were down in the 5%, 6% range, and now we're trending up in the 8% to 10% neighborhood over the past few quarters. I mean, clearly, inflation has helped. There's been probably a little bit of World Cup tailwind. But how much of this acceleration do you guys feel is more transitory versus being structural and sustainable? And just to the extent it's the latter, what do you really see as the main drivers there?

**Ryan McInerney** (Executives):
It's Ryan. Maybe I'll try to take a crack at this. First of all, I think it's tough to say. We just back -- like zoom out a bit and put it in the context of the macro U.S. economy. We've seen strong growth, as you said, kind of an acceleration from 6%, 7%, 8% 6, 12, 18 months ago to 10% that you referenced.
I think the foundation underlying that more than anything is employment. Anyone in this country who wants a job for the most part has a job. And that strength of employment, despite consumer uncertainty, is delivering the strength that you're asking about and ultimately, I think, driving the strength in spending.
The -- as I said, the uncertainty remains elevated, but in the context of strong employment, people have jobs. They have real wage growth. They are spending. And by the way, we see the resilience across the spending bands on our network. So we've seen stability in that sense. But in terms of like how strong for how long and what the new normal is, I just think it's just too hard to tell.

**Operator** (Operator):
Rayna Kumar with Oppenheimer.

**Rayna Kumar** (Analysts):
Can you touch on the progress you're making with geographic expansion of Pismo and whether you think Pismo can make progress in core bank processing in the U.S.?

**Ryan McInerney** (Executives):
Well, I gave, I believe, some remarks in my prepared comments about the number of new countries and some examples of countries that we're entering with Pismo, and I would say our geographic expansion opportunities have exceeded my expectations, going back to when we bought Pismo. We're having strong demand around the world from clients, both for the core banking offerings that Pismo offers but also the issuer processing capabilities. So I think, in general, our thesis on the global expansion for Pismo and having Pismo as part of the Visa network is proving out to be quite strong.
In the U.S., I think I spent a fair bit of time on the last earnings call kind of going through the market, the segments, the client types. We see opportunity in the medium and low end for the combined offering that we've brought to market across DPS and Pismo. For the more sophisticated clients at the larger end, the largest banks in the United States, we do see opportunities for core banking, but those clients manage core banking very separate from their other capabilities. So it tends to be more of a distinct discussion about core banking. But you asked, do we think it's possible for us to make progress in the U.S. Of course. And we've had some great proof points with Wells Fargo and others that we've talked about on this call in the U.S.

**Operator** (Operator):
Harshita Rawat with Bernstein.

**Harshita Rawat** (Analysts):
Ryan, I want to follow up on your comments on Visa cyber-related services. In the current environment, what kind of demand are you seeing on both your Visa transaction-related services and also for cyber and risk beyond Visa transactions and A2A or even in areas like KYC, identity, et cetera? And also, this feels like a fragmented space beyond kind of Visa transactions. So what is Visa's right to win here?

**Ryan McInerney** (Executives):
Well, Harshita, I think our right to win is very significant. We bring strong client relationships. We've delivered some great products to the market. I think it's -- it is a somewhat fragmented competitive space around the world with a lot of different players. And this is a top 3 issue for our clients, especially our financial services clients around the world, and they're turning to Visa and looking for help. And so in our risk and security value-added services businesses, we have a vast array of these solutions that we've been bringing to market, both new and existing solutions, whether it's Visa Threat Intelligence program, obviously, I mentioned BioCatch, which we're excited about, Visa Advanced Authorization, Visa Decision Manager, those types of things.
But if you broaden it to our other areas, as I alluded to and mentioned on my prepared remarks, we're having success deploying and delivering revenue from these services in our acceptance business with our authentication and tokenization platforms, with Visa Intelligent Authorization, which, as I think I mentioned in my prepared remarks, empowers acquirers with advanced processing and payment orchestration and risk settings and real-time data across a bunch of different capabilities. So -- as well as our advisory business in terms of our kind of Visa Cybersecurity Advisory Practice and even in our issuing business with examples like Smarter Stand-in Processing.
So it's become a really important set of service lines and services across our entire suite of VAS services. I think our right to win is high, our progress to date is good, and we'll continue to invest in this space going forward.

**Operator** (Operator):
Andrew Jeffrey with William Blair.

**Andrew Jeffrey** (Analysts):
Ryan, I read with some interest the Visa Direct stablecoin launch. I know you mentioned it in your prepared remarks. It -- the press release notes that you're going to prefund cross-border payouts with USDC, at least for starters, and I know you're part of the Open Standard consortium. Can you talk a little bit about some of your thoughts around whether -- just how stablecoin agnostic you're going to be, thoughts on liquidity factors that might impact the incorporation of other stablecoins and so forth? Just some high level thoughts there would be helpful.

**Ryan McInerney** (Executives):
Sure. We're very excited about the Visa Direct product that you mentioned, but just trying to get to the core of your question, we are stablecoin agnostic. We are blockchain agnostic. We serve a vast array of clients with different preferences and different needs around the world. And so in that particular example, while we started with USDC, we plan to activate other stablecoins as we push forward.
I mean if you just look at maybe our settlement as an example, I think I mentioned in our prepared remarks, we now support 10 blockchains in settlement. We now support 5 stablecoins in settlement, USDC, USDG, EURC, PYUSD and SBC. We have lots of clients who have them for different needs around the world.
So we will be agnostic. We think that's the right approach. But we also, as you noted, we are part of the open consortium. We are part of OUSD. OUSD will also, and you should assume, will be an integrated offering into all these other products, not just settlement but Visa Direct and others going forward.

**Operator** (Operator):
Tien-Tsin Huang with JPMorgan Chase.

**Tien-Tsin Huang** (Analysts):
I'll close it out with my favorite question on visibility, if you don't mind. So '26 was a pretty special year for growth, Ryan and Chris. Thinking about '27, how would you characterize visibility on growth versus this time last year? Where is visibility higher? Where is it weaker? Where might you be more cautious?

**Christopher Suh** (Executives):
Listen, the approach that we've taken to sharing our initial guide for '27 is very similar to that that we took at the start of FY '26. We shared the initial guidance. We also shared with you a set of planning assumptions that underlie that. Some of those assumptions are macro, like assuming consumer resiliency and the drivers remain stable and healthy. Others are dependent on our strong execution, like securing the large volume of client contracts that are up for renewal this year.
And so you think about those things. And of course, like with any plan, there are risks and opportunities, but the plan we shared with you, I think, reflects a balance point of view that takes all that into account. And when you put it together, we feel really good about our plan going into FY '27.

**Jennifer Como** (Executives):
And with that, we'd like to thank you for joining us today. If you have additional questions, please feel free to call or e-mail our Investor Relations team. Thanks again, and have a great day.

**Operator** (Operator):
Thank you all for participating in the Visa Fourth Quarter and Full Year 2026 Earnings Conference Call. That concludes today's conference. You may now disconnect at this time, and please enjoy the rest of your day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### V_Q3_2026_Earnings_Call_20260728.md
- 2026-07-28｜CFO｜guidance：CFO 給 Q4 淨營收成長指引，與 Q3 調整後口徑相近（原話："similar to Q3 on an adjusted basis"）
- 2026-07-28｜CFO｜guidance：Q4 EPS 成長指引（原話："we expect fourth quarter EPS growth to be in the low end"）
- 2026-07-28｜CFO｜guidance：全年營收與 EPS 指引（用語為「now」）（原話："full year net revenue growth to now be in the low end"）
- 2026-07-28｜CFO｜guidance：全年 EPS 成長指引（原話："full year EPS growth to now be in the low end of mid-teens"）
- 2026-07-28｜CFO｜guidance：Q4 指引假設波動率維持目前水準，管理層稱比先前假設有更多拖累（原話："implying more of a drag than was incorporated previously"）
- 2026-07-28｜CFO｜guidance：Q4 客戶獎勵金成長預期略高於 Q3，並說明續約比重（原話："we expect to have renewed about 20% of our payments volume"）
- 2026-07-28｜CFO｜guidance：Q4 營業費用成長指引，含 Q3 費用遞延至 Q4（原話："We expect Q4 operating expense growth in the low-double"）
- 2026-07-28｜CFO｜guidance：截至 7/21 的季中驅動指標：美國付款量 9%，跨境（不含歐洲內部）14%（原話："total volume grew 14% year-over-year, with e-commerce up 18%"）
- 2026-07-28｜CFO｜guidance：FY27 指引留到下一季提供，目前正在跑情境（原話："All of this will result"）
- 2026-07-28｜CFO｜margin：營業費用成長 17%，高於預期；原因為匯兌重估與遞延薪酬市價調整（管理層稱 EPS 中性）（原話："which, as a reminder, is EPS neutral"）
- 2026-07-28｜CFO｜margin：GAAP 含 5.63 億美元資遣成本（原話："we had $563 million in severance costs related to"）
- 2026-07-28｜CFO｜margin：國際交易營收成長 6% 低於跨境量 12%，管理層歸因於去年波動高峰與組合（原話："primarily due to lapping the currency volatility peak"）
- 2026-07-28｜CFO｜margin：客戶獎勵金成長 18%，較 Q2 加快 4 個百分點（原話："Client incentives grew 18%, a step-up of 4"）
- 2026-07-28｜CFO｜margin：CMS 營收較 Q2 降速，管理層列舉兩個原因（原話："CMS revenue stepped down from Q2 due to the"）
- 2026-07-28｜CFO｜product：VAS 營收固定匯率成長 34%、達 38 億美元，並拆解三項來源（含 Prisma 併購）（原話："primarily due to 3 factors:"）
- 2026-07-28｜CFO｜product：管理層稱 VAS 四大組合過去 12 個月成長皆快於投資人日揭露的歷史成長率（原話："all 4 of our VAS"）
- 2026-07-28｜CEO｜product：宣布裁減職位，多數在技術與產品團隊；並說明產品團隊縮編為 2 至 4 人的 agentic 小隊（原話："we are eliminating roles, with the majority being in our"）
- 2026-07-28｜CEO｜product：推出 Visa Stablecoin Platform，並加入 Open Standard（Open USD）（原話："we launched the Visa Stablecoin Platform for stablecoin"）
- 2026-07-28｜CEO｜product：與 OpenAI 合作，在 agentic commerce 中提供 Visa 支付（原話："We are excited to
be partnering with OpenAI"）
- 2026-07-28｜CEO｜product：管理層對 agentic commerce 的定調與時程態度（原話："Agentic commerce is a when, not an if."）
- 2026-07-28｜CEO｜product：DPS 完整信用發卡處理方案，Q4 試行、明年全面上市（原話："We will be piloting it in Q4"）
- 2026-07-28｜CEO｜competition：歐洲憑證成長與贏得業務，含 NatWest 整個零售銀行消費信用卡組合（原話："we have won the entire consumer credit portfolio of their"）
- 2026-07-28｜CEO｜competition：被問及對歐洲本地卡組織的市占，CEO 稱仍在贏得業務（原話："it's hard to keep up, I think, for many domestic schemes"）
- 2026-07-28｜CEO｜competition：穩定幣策略：多幣種多鏈，不選邊；並稱穩定幣尚未規模化（原話："Visa going forward will remain multi-coin, multi-chain."）
- 2026-07-28｜CFO｜customer：美國付款量成長 10%，較 Q2 加快約 2 點，並列出驅動因素（原話："a growth rate not seen since fiscal 2019"）
- 2026-07-28｜CFO｜customer：CFO 稱未在量中看到低消費客群轉弱（原話："We do not see signs of the lower spend"）
- 2026-07-28｜CFO｜customer：跨境電商 6 月與 7 月被管理層描述為異常偏高，預期回到較典型關係（原話："I do think June and July are unusually high"）
- 2026-07-28｜CFO｜risk：旅遊跨境中，衝突仍為抵銷因素（原話："While the conflict continued to be an offsetting factor"）
- 2026-07-28｜CFO｜capital_allocation：Q3 買回 49 億美元股票、發放 13 億美元股利（原話："In Q3, we bought back $4.9 billion in stock and distributed"）
- 2026-07-28｜CFO｜capital_allocation：6 月底剩餘買回授權額度；7 月商業本票容量擴至 70 億美元（原話："we expanded our commercial paper capacity to $7 billion"）
- 2026-07-28｜CEO｜commitment：裁員節省的成本將再投資，CEO 稱投資機會巨大（原話："The investments that we
have in front of us are enormous."）
- 2026-07-28｜CFO｜commitment：CFO 對未來營業利益率的表述（未給數字）（原話："The investments that we"）
- 2026-07-28｜CFO｜commitment：對 FY27 規劃的表述：續約、產品管線與定價貢獻可見度（原話："we do expect that we'll continue to be able to deliver"）

### 問答異常語氣（迴避／改口／保留）
- V_Q3_2026_Earnings_Call_20260728.md｜問：Fahed Kunwar（Redburn）：營收演算（消費支付 5–7%、CMS 與 VAS 15–17%、整體 9–11%）近兩年已明顯偏離，長期是否可持續？｜答法：CFO 未回答演算是否改變，改談 VAS 近 1/3 營收成長 34%、執行策略與專注 FY26 收尾，未給長期口徑。
- V_Q3_2026_Earnings_Call_20260728.md｜問：Will Nance（Goldman）：FIFA 對 6、7 月跨境旅遊數字的量化貢獻，以及如何正常化？｜答法：CFO 未給量化貢獻，改談跨境分布均勻（單一區域不超過 25%）與底層健康。
- V_Q3_2026_Earnings_Call_20260728.md｜問：Sanjay Sakhrani（KBW）：裁員節省是全數再投資還是部分落到損益底線？多久見到回報？｜答法：CEO 與 CFO 未直接回答比例或回收期，改談投資機會巨大、持續進行與過往紀錄，CFO 僅稱預期維持強勁利潤率。
- V_Q3_2026_Earnings_Call_20260728.md｜問：Andrew Schmidt（KeyBanc）：VAS 未來成長路徑與行銷服務相關費用的連動？｜答法：CFO 重申四大組合皆快於投資人日，稱不談 FY27，僅說「預期維持強勁」；未回答費用連動問題。

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
{"date":"20260729","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"卡片軌道在可預見期間仍是唯一可規模化的信任層——穩定幣與帳戶對帳戶軌道在爭議處理、詐欺保護與全球互通性上無法在十年內取得同等能力，故繞道占比維持在個位數以下"},{"id":"H2","text":"網路的定價權在監管壓力下仍能維持——交換費上限與司法部訴訟壓縮的是發卡行與生態系的經濟，不是 Visa 的網路與資料處理費；Visa 仍能每年以定價貢獻 4-7pp 的營收成長"},{"id":"H3","text":"加值服務成為與交易量脫鉤的第二成長引擎——由「隨交易量附帶」升級為「按能力訂價的獨立服務業」，其成長率長期高於支付金額成長率"}],"extra_text":"# | 具體數字門檻（floor） | 信息來源 | 漂移觸發條件\nH1 | 穩定幣結算占 Visa 支付金額 &lt; 1%（現約 0.04%）；憑證數年增 ≥ +6%（本季 +8%）；季支付金額 ≥ $4 兆 | Visa 多鏈結算試點年化約 $70 億（2026-04 揭露，季增 50%）：產業媒體報導（2026）；憑證 +8%、代幣化近 60%、季支付金額首破 $4 兆：Visa FY2026 Q3 法說（2026-07-28）；GENIUS 法案與 Open USD 零手續費設計：多家法律與產業分析（2026） | 連 4 季繞道占比累計上升 ≥ 2pp（5Y 假設）→ 削弱；達 5% → 反轉。單季試點規模擴張不觸發。\nH2 | 資料處理收入成長 − 交易筆數成長 ≥ +4pp；服務收入成長 − 支付金額成長 ≥ +3pp；營業利益率 ≥ 63% | 本季資料處理 +17% vs 交易筆數 +10%、服務收入 +14% vs Q2 固定匯率支付金額 +9%（管理層明言差額「主要來自定價」）：Visa FY2026 Q3 法說；營業利益率 66.4%（FY2025）：yfinance 財報三表；司法部案程序時程（事實證據開示 2026-10-16、專家 2027-04-08、駁回動議 2025-06 被否決）：法律事務所與產業媒體整理（2026） | 連 2 季定價差額 ≤ +2pp（2Y 假設）→ 削弱；出現結構性救濟裁定 → 立即反轉。\nH3 | 加值服務營收年增 ≥ +20%（固定匯率）；底層三組合（發卡、受理、風險與安全）合計 ≥ +15% | 本季加值服務 +34% 至 $38 億、四個子組合全部快於投資人日（2025-02）揭露之歷史成長率、底層三組合連 12 個月每季 &gt; +20%：Visa FY2026 Q3 法說；Pismo 與 Featurespace 併購貢獻約 1.5pp 營收成長：同上 | 連 4 季低於 +15%（5Y 假設）→ 削弱；連 6 季低於 +10% → 反轉。剔除 FIFA 行銷服務高基期後判定。"},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"營業費用結構性快於營收。本季營業費用 +17% 對照淨收入 +14%，為本財年首度反向；GAAP 另認列 $5.63 億資遣費用、裁撤 2,600 個職位。若「投資以維持成長」的需求持續上升，67% 的營業利益率就不是結構性而是週期性。"},{"id":"R2","text":"司法部借記卡案朝結構性救濟發展。駁回動議已被否決，案件進入實質訴訟；美國借記業務是 Visa 規模優勢最集中之處。結構性救濟（強制開放路由、拆分借記處理）與金錢和解對估值的含義完全不同。"},{"id":"R3","text":"穩定幣與帳戶對帳戶軌道取得爭議處理能力後開始承接主流商戶流量。GENIUS 法案提供制度基礎；Open USD 零手續費 ＋ 儲備收益回饋設計直接對準卡片經濟；商戶動機從未消失。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已進場；加碼觸發＝回檔至 $340-350（W52 上緣）或 DOJ 事實證據開示結束無結構性不利發展","irr_base_pct":10.7,"ev5y_pct":49.8,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"🟡","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":3.5,"ev5y_pct":49.8,"irr_base_pct":10.7,"max_dd_pct":-50.0,"bull_5y_price":784.0,"bear_5y_price":248.0,"p_bull_pct":27.0,"p_bear_pct":27.0,"rearm_trigger":"已進場；加碼觸發＝回檔至 $340-350（W52 上緣）或 DOJ 事實證據開示結束無結構性不利發展","price_at_dd":366.59,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/V_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
