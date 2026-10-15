你是 stock-analyst **v20 判斷 agent**，標的 MRVL（20261012）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MRVL","date":"2026-10-12","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRVL_20261012/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRVL_20261012/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":2739.3,"period":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","citation":"公司新聞稿 investor.marvell.com Q2 FY27 press release"},"note":"新聞稿稱高於自家指引中點 $39.0M；分析師共識未取得"},{"id":"f_kpi1","label":"資料中心營收","value":2171.5,"period":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","citation":"公司新聞稿 investor.marvell.com Q2 FY27 press release"},"note":"未取得"},{"id":"f_kpi2_non_gaap","label":"Non-GAAP 營業利益／利益率","value":36.6,"period":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","unit":"%（營業利益 1,003.2M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","citation":"公司新聞稿 investor.marvell.com Q2 FY27 press release"},"note":"未取得"},{"id":"f_kpi3_gaap","label":"GAAP 營業利益／利益率","value":16.8,"period":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","unit":"%（營業利益 459.7M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","citation":"公司新聞稿 investor.marvell.com Q2 FY27 press release"},"note":"未取得"},{"id":"f_kpi6_gaap_non_gaap","label":"GAAP／Non-GAAP 毛利率","value":58.9,"period":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","unit":"% Non-GAAP（GAAP 53.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","citation":"公司新聞稿 investor.marvell.com Q2 FY27 press release"},"note":"未取得"},{"id":"f_kpi7_q3_fy2027_2026_10_31","label":"管理層指引：Q3 FY2027（季末 2026-10-31）","value":"營收 3.150B ±5%（約 2.99–3.31B）；Non-GAAP 毛利率 57.5–58.5%；Non-GAAP 營業費用約 655M；Non-GAAP EPS 1.10±0.05；GAAP EPS 0.53±0.05","period":"Q2 FY2027（公告於 2026-08-27）","unit":"指引","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2027（公告於 2026-08-27）","citation":"公司新聞稿 investor.marvell.com Q2 FY27 press release"},"note":"未取得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-27","period":"2026-08-27","unit":"date","basis":"距今 32 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mrvl_gross_margin_pct","label":"MRVL 毛利率","value":52.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_operating_margin_pct","label":"MRVL 營業利益率","value":16.81,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_fcf_margin_pct","label":"MRVL FCF 利潤率","value":18.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_gross_margin_pct","label":"NVDA 毛利率","value":74.67,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_operating_margin_pct","label":"NVDA 營業利益率","value":65.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_fcf_margin_pct","label":"NVDA FCF 利潤率","value":41.92,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amd_gross_margin_pct","label":"AMD 毛利率","value":53.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amd_operating_margin_pct","label":"AMD 營業利益率","value":15.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amd_fcf_margin_pct","label":"AMD FCF 利潤率","value":20.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3661_tw_gross_margin_pct","label":"3661.TW 毛利率","value":37.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3661_tw_operating_margin_pct","label":"3661.TW 營業利益率","value":24.0,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3661_tw_fcf_margin_pct","label":"3661.TW FCF 利潤率","value":-10.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_605_5m_capex_126_7m","label":"自由現金流（營業現金流 605.5M − capex 126.7M，自算，公司未列示）","value":478.8,"period":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","citation":"公司新聞稿現金流量表 investor.marvell.com Q2 FY27 press release；FCF 為自算"},"note":"未取得"},{"id":"f_kpi5_sbc_gaap","label":"SBC 占營收／占 GAAP 營業利益","value":11.9,"period":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","unit":"% 占營收（SBC 326.2M；占 GAAP 營業利益約 71%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）","citation":"公司新聞稿 investor.marvell.com Q2 FY27 press release；比率自算"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":275.28,"period":"2026-10-09（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":114.34,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":61.52,"period":"2026-10-09（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.24,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.21 → 4.22）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":7.25,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.76 → 7.25）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":17.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.41 → 12.18）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":4.22,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":7.25,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":12.18,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.2,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 4.05 → 4.22（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":90.55,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"1 個年度端點內的分位＝50.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":50.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":26.18,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":26.32,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":65.23,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 4.22，分子＝快照價 275.28","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.087,"period":"2026-10-12","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-12"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Futurum 估計 Marvell 仍為 XPU 第二大業者，但 Alchip、GUC 與 Broadcom 的既有優勢是主要逆風","source":"Futurum Group, Marvell Q2 FY 2026 Earnings: Data Center Growth Healthy but Overshadowed by Rising Competition","url":"https://futurumgroup.com/insights/marvell-q2-fy-2026-earnings-data-center-growth-healthy-but-overshadowed-by-rising-competition/","excerpt":"Futurum's estimates continue to place Marvell as the second-largest player in XPUs this year and over the coming years. However, competition from Alchip, GUC, and Broadcom's entrenched dominance remains a key headwind","as_of":"2025-08-29","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Marvell 的 XPU 專案面臨台灣設計服務業者（Alchip、GUC）競爭而有毛利壓力；有未證實的二手報導稱 Trainium 3/4 轉向 Alchip","source":"Dolphin Research 筆記（經搜尋摘要轉述，Marvell FY26 Q2 後）","url":"https://longportapp.cn/topics/33455225","excerpt":null,"as_of":"2025-09-01","retrieved_at":"20261012","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"JPMorgan 稱依一手研究與財報電話會議，Microsoft 與 AWS 現世代及下一世代 AI XPU ASIC 專案均無份額流失","source":"搜尋摘要轉述 JPMorgan 評論（日期未能確認）","url":null,"excerpt":null,"as_of":"2025-09-01","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Benzinga 引 JPMorgan：自訂 AI 加速器份額 Broadcom 55–60%、Marvell 約 15%；另有部落格稱 Broadcom 約 70%（無來源）","source":"Benzinga 引 JPMorgan Harlan Sur / heygotrade 部落格","url":"https://www.heygotrade.com/en/blog/broadcom-vs-marvell-custom-ai-silicon-battle-2026/","excerpt":"Broadcom, the market leader with 55%-60% share; Marvell, trailing with a 15% share","as_of":"2026-03-01","retrieved_at":"20261012","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Digitimes 2026-01-30 標題顯示 MediaTek、Alchip、Marvell 爭奪 ASIC 第二名；內文未取得","source":"Digitimes, MediaTek, Alchip, Marvell clash for ASIC runner-up spot","url":"https://www.digitimes.com/tag/marvell/002898.html","excerpt":"MediaTek, Alchip, Marvell clash for ASIC runner-up spot","as_of":"2026-01-30","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"光 DSP：Marvell 與 Broadcom 合計近 90% 份額；2025 年 5 月研究稱 Broadcom 與 MaxLinear 開始送 800G DSP 認證，報價 Marvell $90–100 對 $50–60","source":"Dolphin Research (2025-01)；Global Technology Research Substack (2025-05)","url":"https://globaltechresearch.substack.com/p/whats-going-on-with-marvell-mrvl","excerpt":"the main players in the market are Marvell and Broadcom, with a combined market share of nearly 90%","as_of":"2025-05-01","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#6","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Cignal AI：相干 DSP 400G 由 Acacia 與 Marvell 主導，800G 可插拔份額之爭將更競爭","source":"Cignal AI, Tracking the coherent DSP supply chain 2026","url":"https://cignal.ai/2026/04/tracking-the-coherent-dsp-supply-chain-2026/","excerpt":"At 400G, two vendors (Acacia and Marvell) dominated the DSP market. The battle for 800G pluggable market share will be much more competitive.","as_of":"2026-04-01","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#7","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Nvidia 於 3/31 宣布 20 億美元投資 Marvell，並將 NVLink Fusion 與 Marvell XPU 服務整合","source":"Digitimes (Marvell tag page)","url":"https://www.digitimes.com/tag/marvell/002898.html","excerpt":"On March 31, Nvidia announced a US$2 billion investment in Marvell","as_of":"2026-03-31","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-Q 風險揭露：AWS 為 Marvell 最大客戶且差距顯著；Trainium 放緩或轉向其他設計夥伴將對營收造成重大影響。","source":"Marvell 10-Q FY2026 (quarter ended 2026-05-02), via search summary","url":"https://www.sec.gov/Archives/edgar/data/0001835632/000183563226000019/mrvl-20260502.htm","excerpt":"AWS is Marvell's largest customer by a significant margin. A slowdown in the Trainium program or a shift to a different design partner would have a material impact on revenue.","as_of":"2026-05-02","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Marvell 風險揭露警告部分大客戶可能自行開發並製造半導體方案，導致 Marvell 失去業務。","source":"Marvell 10-Q FY2026 (quarter ended 2026-05-02), via search summary","url":"https://www.sec.gov/Archives/edgar/data/0001835632/000183563226000019/mrvl-20260502.htm","excerpt":"some large customers may begin developing and making their own semiconductor solutions which could result in a loss of business for Marvell","as_of":"2026-05-02","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Benchmark 降評稱 Marvell 將 Trainium 3 與 4 設計輸給台灣 Alchip；未經公司證實。","source":"AOL/Barron's-type coverage: Will Customer Defections Crumble Marvell Technology's AI Empire?","url":"https://www.aol.com/articles/customer-defections-crumble-marvell-technology-165123515.html","excerpt":"sources indicated Marvell lost the designs for the Trainium 3 and 4 AI chips to Taiwan-based rival Alchip Technologies","as_of":"2026-03-08","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#3","axis":"customer_second_source","section":"coverage","direction":"-","claim":"The Information 報導 Microsoft 正評估 Broadcom 作為晶片設計夥伴（Maia）。","source":"AOL: Will Customer Defections Crumble Marvell Technology's AI Empire?","url":"https://www.aol.com/articles/customer-defections-crumble-marvell-technology-165123515.html","excerpt":"Microsoft is exploring Broadcom as a potential chip design partner","as_of":"2026-03-08","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#4","axis":"customer_second_source","section":"coverage","direction":"+","claim":"Marvell 管理層稱 FY2026 看不到來自 Amazon 的營收中斷；CEO 否認失去 Microsoft 或 Amazon 業務。","source":"24/7 Wall St: Wall Street's Worry About Marvell Losing Customers Was Overblown","url":"https://247wallst.com/investing/2026/03/08/wall-streets-worry-about-marvell-losing-customers-was-overblown/","excerpt":"Marvell executives stated they see no revenue disruptions from Amazon in fiscal 2026.","as_of":"2026-03-08","retrieved_at":"20261012","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 10-K：兩家客戶占營收 10% 以上（一家經銷商、一家直接客戶）；前十大客戶（含經銷商與直接客戶）占 FY2026 淨營收 82%。","source":"Marvell Form 10-K FY2026 (mrvl-20260131)","url":"https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"第三方彙整稱 FY2026 經銷商 A 占淨營收 37%、一家直接客戶 14%（未對照 10-K 原文確認）；經銷商 A 占比 FY2024 24%→FY2025 34%，FY2025 直接客戶 13%。","source":"autobound.ai / policyrisk.com 彙整；FY2025 10-K","url":"https://www.autobound.ai/companies/marvell/10-k","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2024 年底四家客戶占應收帳款毛額 72%；公司稱信用風險由信用評估、短收款期與客戶高信用品質大幅緩解。","source":"Marvell Form 10-K FY2025/FY2024 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1835632/000183563225000057/mrvl-20250201.htm","excerpt":null,"as_of":"2025-03-01","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"超大型雲端業者資本支出與舉債升高：S&P 預估 2026 年五大業者 capex 約 7,500 億美元；Q1 美國超大型業者直接發債 1,150 億美元（2025 全年 700 億）；PIMCO 預估 capex 吃掉 94% 營運現金流。搜尋結果未見 Amazon／Microsoft／Google 的評等調降事件。","source":"FactSet Insight 2026-07-23 及 fi-desk 等彙整","url":"https://insight.factset.com/hyperscalers-tap-external-financing-as-ai-capex-outruns-cash-flow","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"光互連與矽光子產能被點名為 AI 資料中心建置的新瓶頸（2026-06 報導）","source":"Seeking Alpha: AI data centers hit a new bottleneck: Optical interconnects","url":"https://seekingalpha.com/news/4606321-ai-data-centers-hit-a-new-bottleneck-optical-interconnects","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261012","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"S&P：聯發科瞄準 2027 年客製 AI 加速器可服務市場最高 20%，首顆 ASIC Q4 2026 量產（客製 ASIC 競爭者增加）","source":"S&P Global Market Intelligence: MediaTek's AI ASICs growth to offset smartphone weakness","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/08/mediatek-s-ai-asics-growth-to-offset-smartphone-weakness","excerpt":"MediaTek is targeting as much as 20% of the serviceable available market for customized AI accelerators by 2027.","as_of":"2026-08-26","retrieved_at":"20261012","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"CoWoS 產能估 2026 年底約 12.5–13 萬片/月；KGI 預估 2027 年底 170k wpm，擴產多落在 2H27；Nvidia 約佔 2026 CoWoS 60%、Broadcom 約 15%、AMD 約 11%（Morgan Stanley 估）","source":"KGI Securities TSMC report (2026-03-09) / aiweekly / tipranks 彙整","url":"https://www.kgi.com.hk/en/-/media/files/kgishk/research-reports/tw-reports/tsmc_2330-tt_09032026e.pdf","excerpt":null,"as_of":"2026-03-09","retrieved_at":"20261012","affects":["thesis.R","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Moody's：美國超大型雲端業者 2026 年 capex 約 7,850 億美元、2027 年逼近 1 兆美元；Goldman 估 2027 年 1.14 兆；Moody's 指新增約 7,000 億美元 RPO 支撐多年軌跡，但投資人擔憂過度建置與報酬偏弱","source":"DatacenterDynamics: Moody's hyperscaler capex forecasts marked up by $85bn to close in on $1trn by 2027","url":"https://datacenterdynamics.com/en/news/moodys-hyperscaler-capex-forecasts-marked-up-by-85bn-to-close-in-on-1trn-by-2027/","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Bank of America 預估超大型雲端業者合計自由現金流 2026 約 -640 億美元、2027 約 -1,440 億、2028 約 -1,860 億；Goldman 預期債務涵蓋 2027 年 AI capex 約三分之一；市場共識傾向 2027 年 capex 見頂後持平","source":"TFTC: AI capex cash flow negative 2027 peak hyperscalers","url":"https://www.tftc.io/ai-capex-cash-flow-negative-2027-peak-hyperscalers","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Marvell FQ2 FY2026（2025-08）營收 20.06 億美元年增 58%；管理層稱客製矽業績起伏大、由電光產品抵銷；超過 10 家客戶、50+ 客製 AI 設計機會；18 個 XPU/XPU attach 設計案已量產或爬坡（此為一年前資料，非最新季）","source":"Converge Digest: Marvell doubles down on AI with record $2B quarter","url":"https://convergedigest.com/marvell-doubles-down-on-ai-with-record-2b-quarter-and-optical-milestones/","excerpt":null,"as_of":"2025-08-28","retrieved_at":"20261012","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2026 10-K 揭露：MRVL 目前不是中國對美國科技公司反壟斷調查的對象（中國曾宣布對特定美國科技公司展開反壟斷調查）。","source":"Marvell Technology, Inc. Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm","excerpt":"While we are not currently the subject of such an antitrust probe","as_of":"2026-01-31","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2026 10-K 揭露：部分對中國客戶銷售需出口許可，過去部分許可曾被延遲或拒絕，未來核准無保證；10-Q（2026-05）重複此語。","source":"Marvell Technology, Inc. Form 10-K FY2026 / Form 10-Q (quarter ended 2026-05-02)","url":"https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm","excerpt":"sales to some customers require licenses for us to export our products; however, in the past some of these licenses have been delayed or denied","as_of":"2026-01-31","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2026 年報（ARS）討論美國商務部對半導體進口的 Section 232 國安調查，可能導致額外關稅與貿易限制（貿易事項，非反壟斷）。","source":"Marvell Technology, Inc. Form ARS FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001835632/000110465926060265/tm261486d6_ars.pdf","excerpt":null,"as_of":"2026-01-31","retrieved_at":"20261012","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2026 10-K 稱出口限制已降低且未來可能降低對中國銷售，部分對中國銷售需美國出口許可，過去曾有許可被延遲或拒發，現有許可可能因政策變動被撤銷；Entity List 新增曾壓抑需求。","source":"Marvell Form 10-K FY2026 (fiscal year ended 2026-01-31), SEC","url":"https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm","excerpt":"export restrictions reducing our sales of products to China have in the past and may in the future adversely impact our revenues, profits and results of operations.","as_of":"2026-01-31","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Marvell 財報稱 Section 232 半導體調查（BIS 2025 年 4 月啟動）可能導致額外關稅與貿易限制；FY2026 年報仍列為開放風險，未量化影響。","source":"Marvell Form ARS FY2026 / 10-Q filings, SEC","url":"https://www.sec.gov/Archives/edgar/data/0001835632/000110465926060265/tm261486d6_ars.pdf","excerpt":"may result in additional tariffs and trade restrictions, which may adversely impact our business.","as_of":"2026-01-31","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-01-14 總統公告對一小群先進晶片課 25% Section 232 關稅（1/15 生效），適用不供美國使用者；美國資料中心、美國境內維修與研發等有豁免；第二階段可能擴大。搜尋結果未載明 Marvell 產品是否在涵蓋範圍。","source":"Thomson Reuters OneSource, Trump administration imposes tariffs on advanced AI chips under Section 232 authority","url":"https://www.thomsonreuters.com/en-us/help/onesource-global-trade/regulatory-insights/2026/january-15th/trump-admin-tariffs-advanced-ai-chips-232.html","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美台協議：台灣半導體與科技業承諾至少 2,500 億美元對美直接投資，美國對台灣商品互惠關稅上限 15%，未來 Section 232 關稅將獎勵在美新增產能的台灣生產商（Marvell 主要晶圓由台灣代工）。","source":"Polsinelli, Trump adopts dual track approach to restore semiconductor leadership","url":"https://www.polsinelli.com/publications/trump-adopts-dual-track-approach-restore-semiconductor-leadership","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261012","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Marvell 產品多數由台灣第三方晶圓代工；封裝測試分布於中國、馬來西亞、新加坡、台灣、加拿大。未找到 2026 年點名 Marvell 的 Entity List 行動。","source":"policyrisk.com MRVL profile (summarising Marvell SEC disclosures)","url":"https://policyrisk.com/world/company/MRVL","excerpt":null,"as_of":"2026-01-31","retrieved_at":"20261012","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Marvell FY2026 10-K（會計年度止 2026-01-31）：多數合格晶圓代工廠位於台灣同一區域；台灣政治、軍事或天災中斷會損及業務（搜尋摘要轉述10-K，未讀全文頁面）。","source":"Marvell Technology, Inc. Form 10-K FY2026 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm","excerpt":"Most of our current qualified integrated circuit foundries are located in the same region within Taiwan.","as_of":"2026-01-31","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"封裝與測試分包商集中於泛太平洋地區（中國、馬來西亞、新加坡、台灣、加拿大）；FY2026 10-K 並列地緣緊張與衝突為中斷風險（搜尋摘要轉述）。","source":"Marvell Technology, Inc. Form 10-K FY2026 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm","excerpt":null,"as_of":"2026-01-31","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"歷史 10-K（FY2013）揭露多數產品同一時間不在超過一家晶圓廠生產，轉換晶圓廠困難；FY2020 10-K 稱替代晶圓廠有限、導入需時。為舊年度文件，現行單源程度未於本軸確認。","source":"Marvell Technology Group 10-K FY2013 / FY2020 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0001058057/000119312513134707/d469362d10k.htm","excerpt":"most of our products are not manufactured at more than one foundry at any given time","as_of":"2013-03-01","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026年產業分析：自研晶片（Google TPU、Amazon Trainium）仍與其他客戶競爭同一批先進製程與先進封裝產能（TSMC）；CoWoS 與 HBM 為產業瓶頸，非 TSMC 的 CoWoS 產能很小。屬產業層次二手分析，非針對 MRVL。","source":"enkiai.com / softwareseni.com 等產業分析（搜尋摘要）","url":"https://enkiai.com/data-center/ai-manufacturing-constraint-2026-the-real-ai-choke-point/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Marvell FY27 Q2 資料中心營收 $2.17B、年增 46%、占總營收 79%；報導稱全年資料中心成長預期由約 50% 上修至約 60%、全年營收約 $12B（各報導數字不一，未見公司原始公告）","source":"Futurum Group, Marvell Q2 FY 2027: Connectivity and Custom Silicon Fuel AI Growth / Pulse2","url":"https://futurumgroup.com/insights/marvell-q2-fy-2027-connectivity-and-custom-silicon-fuel-ai-growth/","excerpt":null,"as_of":"2026-08-28","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Marvell 稱 FY2028 客製化營收將超過倍增，並重申 FY2029 客製化矽營收目標逾 $100 億","source":"Futurum Group, Marvell Q1/Q2 FY 2027 coverage","url":"https://futurumgroup.com/insights/marvell-q1-fy-2027-raises-full-year-outlook-on-ai-data-center-demand/","excerpt":null,"as_of":"2026-05-29","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Interconnect 業務 FY2027 預期成長逾 70%（原約 50%）；1.6T 方案已量產並於 FY2027 快速放量","source":"Futurum Group, Marvell Q1 FY 2027 Raises Full-Year Outlook","url":"https://futurumgroup.com/insights/marvell-q1-fy-2027-raises-full-year-outlook-on-ai-data-center-demand/","excerpt":"Marvell expects its interconnect business to grow more than 70% YoY in FY 2027","as_of":"2026-05-29","retrieved_at":"20261012","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"Counterpoint 預估 Marvell 在客製 AI ASIC 的份額 2027 年降至約 8%（出貨量 2024–2027 約倍增）；JPMorgan 估 Broadcom 占高階 ASIC 80–85%、Marvell 約 10–12%；Motley Fool 引 Broadcom 約 70%","source":"Counterpoint Research / JPMorgan via KuCoin / Motley Fool","url":"https://www.fool.com/investing/2026/06/30/better-custom-asic-stock-marvell-vs-broadcom/","excerpt":"Broadcom is the bigger player in custom AI chips with an estimated market share of 70%.","as_of":"2026-06-30","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"自 FY26 Q4 起，企業網路、電信基礎設施、消費、車用/工業合併為單一 communications and other 終端市場；車用乙太網路事業以 $2.5B 售予 Infineon，2025-08-14 完成","source":"Marvell Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm","excerpt":"Beginning in the fourth quarter of fiscal 2026, the Company consolidated revenue previously reported separately as enterprise networking, carrier infrastructure, consumer and automotive/industrial end markets into a new communications and other end market","as_of":"2026-03-01","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"分析師指 Marvell PAM4 DSP 在可插拔光學相對領先（定性，無量化份額）；較早的疑慮含 Trainium 份額流失、1.6T DSP 放量時程、Broadcom 競爭","source":"Investing.com, Marvell SWOT analysis: stock surges on optical growth","url":"https://uk.investing.com/news/-4759933","excerpt":"Marvell's PAM4 DSP is relatively leading in pluggable optics.","as_of":"2026-05-29","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"HSBC 以 Hold、目標價 $85 啟動 MRVL 評等，認為其 ASIC 業務至 2027 年可能落後同業，並稱 Broadcom ASIC 路線圖能見度較高。","source":"Yahoo Finance: Marvell started at Hold as weak ASIC outlook offsets strength in AI optical","url":"https://finance.yahoo.com/news/marvell-started-hold-weak-asic-154522224.html","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Digitimes 2026 年 1 月標題：MediaTek、Alchip、Marvell 爭奪 ASIC 第二名；另有分析稱台系 IP 廠 Alchip、GUC 對 Marvell XPU 專案造成毛利壓力。","source":"Digitimes: MediaTek, Alchip, Marvell clash for ASIC runner-up spot","url":"https://www.digitimes.com/tag/marvell/001898.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Dell'Oro：1.6T ZR/ZR+ 可插拔廠商（1Finity、Ciena、Marvell、Nokia）採 2nm DSP；預計 2027 年底前普遍供貨，樣品最早 2026Q4；Cisco Acacia 等另有自家 DSP 的 100G ZR/ZR+ 2026 年中出貨。","source":"Dell'Oro Group: OFC 2026 scaling up optical network density","url":"https://www.delloro.com/ofc-2026-scaling-up-optical-network-density/","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261012","affects":["moat_trend","valuation"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Marvell FY2026 10-K 將 LPO 晶片組（TIA、雷射驅動）與 CPO 列為產品線，並列有 AEC DSP；LPO 為無 DSP 模組，是對模組 DSP 需求的潛在替代路徑，採用面仍有訊號完整性與互通性挑戰（OFC workshop）。","source":"Marvell 10-K FY2026; OFC workshop: Will LPO have a future","url":"https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm","excerpt":null,"as_of":"2026-01-31","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Semtech OFC 2026 摘要：scale-up 目前以銅為最實用，光學與銅並行進入而非取代；Broadcom Taurus BCM83640（3nm、400G/lane 光 DSP）為 1.6T/3.2T 模組關鍵件，競爭 Marvell DSP。","source":"Semtech blog OFC 2026; Digitimes 2026-04-21","url":"https://blog.semtech.com/ofc-2026-semtech-advances-the-future-of-ai-data-center-optical-and-active-copper-interconnects","excerpt":null,"as_of":"2026-04-21","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 價目頁（約 2026-08-28 擷取）：26 位分析師、共識 Buy（23 Buy／3 Hold），平均目標價 $261；近期動作含 Craig-Hallum 調升至 $300、B. Riley 下調至 $315。","source":"Benzinga MRVL price-targets page","url":"https://kr.benzinga.com/quote/MRVL/price-targets","excerpt":"lists 26 analysts with a consensus \"Buy\" rating and an average target of $261, about 20.6% above the price at the time.","as_of":"2026-08-28","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"各聚合站目標價分布（2026-07）：MarketBeat 平均 $245.45、37 位分析師、區間 $105–$400（07-21）；Investing.com UK 平均 $252.94、40 位（07-14）；Public.com $243.71、28 位。","source":"Capital.com MRVL stock forecast (citing MarketBeat/Investing.com/Public.com)","url":"https://capital.com/en-ae/analysis/marvell-technology-stock-forecast","excerpt":"MarketBeat reported an average 12-month target of $245.45, based on 37 analyst estimates ranging from $105 to $400 as of July 21, 2026.","as_of":"2026-07-21","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ2'27 財報（2026-08-27）公司 FQ3 指引：營收約 $3.15B ±5%、non-GAAP EPS $1.10 ±$0.05，高於當時 Street 預期（營收 $3.03B、EPS $1.07）；non-GAAP 毛利率指引 57.5%–58.5%，低於 Q2 的 58.9%。","source":"Marvell 8-K Q2 FY27 press release exhibit 99.1; search summary of Benzinga/StockTwits","url":"https://www.sec.gov/Archives/edgar/data/0001835632/000183563226000022/q227_8kx812026ex-991.htm","excerpt":"Net revenue is expected to be $3.150 billion +/- 5%. Non-GAAP diluted net income per share is expected to be $1.10 +/- $0.05 per share.","as_of":"2026-08-27","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"財報後盤後股價約下跌 2%，市場關注 Q2 小幅優於預期與 Q3 毛利率指引走低，儘管多年展望上調。","source":"StockTwits: MRVL Stock Slips After-Hours Despite Raised Multi-Year Outlook","url":"https://stocktwits.com/news-articles/markets/equity/mrvl-stock-slips-after-hours-despite-raised-multi-year-outlook-investors-weigh-thin-q2-beat-lower-q3-margin-outlook/cZYoXteRJqV","excerpt":"MRVL Stock Slips After-Hours Despite Raised Multi-Year Outlook — Investors Weigh Thin Q2 Beat, Lower Q3 Margin Outlook","as_of":"2026-08-27","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Marvell 於 2025-12 宣布以 32.5 億美元收購光子 AI 新創 Celestial AI；搜尋結果未能確認是否已交割。","source":"Seeking Alpha: Marvell slumps as Q3 results, guidance meet estimates; announces $3.3B Celestial AI deal","url":"https://seekingalpha.com/news/4527755-marvell-slumps-as-q3-results-guidance-meet-estimates-announces-33b-celestial-ai-deal","excerpt":null,"as_of":"2025-12-02","retrieved_at":"20261012","affects":["moat_trend","valuation","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"Marvell 於 2026-02-10 完成收購 XConn Technologies（PCIe/CXL 交換晶片），交割時付現金約 2.8 億美元並發行約 210 萬股。","source":"Marvell newsroom: Marvell completes acquisition of XConn Technologies","url":"https://cn.marvell.com/company/newsroom/marvell-completes-acquisition-of-xconn-technologies.html","excerpt":null,"as_of":"2026-02-10","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"Infineon 於 2025-08-14 完成收購 Marvell 的車用乙太網路事業（協議 2025-04 宣布）。","source":"搜尋摘要（Infineon／Marvell 交易公告）","url":null,"excerpt":null,"as_of":"2025-08-14","retrieved_at":"20261012","affects":["thesis.H"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"2026 年 4 月 Marvell 取消對 Celestial AI 的全部採購訂單，引發 POET Technologies 集體訴訟（被告為 POET，非 Marvell）。","source":"ts2.tech: POET Technologies Stock Faces Marvell Fallout as Investor Lawsuit Deadline Nears","url":"https://ts2.tech/en/poet-technologies-stock-faces-marvell-fallout-as-investor-lawsuit-deadline-nears/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2025-12 宣布以約 32.5 億美元收購 Celestial AI；交割狀態未確認。","source":"Seeking Alpha","url":"https://seekingalpha.com/news/4527755-marvell-slumps-as-q3-results-guidance-meet-estimates-announces-33b-celestial-ai-deal","excerpt":null,"as_of":"2025-12-02","retrieved_at":"20261012","affects":["valuation","moat_trend","thesis.R"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"+","claim":"2026-02-10 完成收購 XConn Technologies，現金約 2.8 億美元加約 210 萬股。","source":"Marvell newsroom","url":"https://cn.marvell.com/company/newsroom/marvell-completes-acquisition-of-xconn-technologies.html","excerpt":null,"as_of":"2026-02-10","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"ma_merger#2","axis":"ma_merger","section":"events","direction":"0","claim":"2025-08-14 Infineon 完成收購 Marvell 車用乙太網路事業（出售方為 Marvell）。","source":"搜尋摘要","url":null,"excerpt":null,"as_of":"2025-08-14","retrieved_at":"20261012","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 11 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MRVL","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":52.21,"operating_margin_pct":16.81,"fcf_margin_pct":18.23,"rd_intensity_pct":25.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL","as_of":"TTM ending 2026-07-31（4季加總）"},"is_subject":true},{"name":"NVDA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.67,"operating_margin_pct":65.21,"fcf_margin_pct":41.92,"rd_intensity_pct":7.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AMD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":53.2,"operating_margin_pct":15.71,"fcf_margin_pct":20.34,"rd_intensity_pct":22.74},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"3661.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.2,"operating_margin_pct":24.0,"fcf_margin_pct":-10.46,"rd_intensity_pct":9.17},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"MRVL"},"financial_history":{"ticker":"MRVL","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-01-31","revenue":5919600000.0,"revenue_yoy_pct":null,"gross_margin_pct":50.47,"operating_margin_pct":6.07,"net_income":-163500000.0,"diluted_eps":-0.19,"free_cash_flow":1071500000.0,"fcf_margin_pct":18.1,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-01-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-01-31","revenue":5507700000.0,"revenue_yoy_pct":-6.96,"gross_margin_pct":41.64,"operating_margin_pct":-7.93,"net_income":-933400000.0,"diluted_eps":-1.08,"free_cash_flow":1020300000.0,"fcf_margin_pct":18.52,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-01-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-01-31","revenue":5767300000.0,"revenue_yoy_pct":4.71,"gross_margin_pct":41.31,"operating_margin_pct":-6.35,"net_income":-885000000.0,"diluted_eps":-1.02,"free_cash_flow":1389600000.0,"fcf_margin_pct":24.09,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-01-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-01-31","revenue":8194600000.0,"revenue_yoy_pct":42.09,"gross_margin_pct":51.02,"operating_margin_pct":16.33,"net_income":2670100000.0,"diluted_eps":3.07,"free_cash_flow":1391900000.0,"fcf_margin_pct":16.99,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-01-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MRVL/MRVL_Q2_2027_Earnings_Call_20260827.md）

# Q2 2027 Earnings Call
**Marvell Technology, Inc.** | Earnings Calls | 2026-08-27

**Operator** (Operator):
Good afternoon, and welcome to Marvell Technology Inc. Second Quarter of Fiscal Year 2027 Earnings Conference Call. [Operator Instructions] Please note, this event is being recorded.  
I will now turn the conference over to Mr. Ross Seymore, Senior Vice President of Investor Relations. Thank you. You may begin.

**Ross Seymore** (Executives):
Thank you, and good afternoon, everyone. Welcome to Marvell's Second Fiscal Quarter 2027 Earnings Call. Joining me today are Matt Murphy, Marvell's Chairman and CEO; Dan Durn, CFO; Chris Koopmans, President and COO; and Sandeep Bharathi, President of our Data Center Group. Let me remind everyone that certain comments made today include forward-looking statements, which are subject to significant risks and uncertainties that could cause our actual results to differ materially from management's current expectations.  
Please review the cautionary statements and risk factors contained in our earnings press release, which we filed with the SEC today and posted on our website as well as our most recent 8-K, 10-K, 10-Q and other documents that we file from time to time with the SEC. We do not intend to update our forward-looking statements. During our call today, we will refer to certain non-GAAP financial measures. A reconciliation between our GAAP and non-GAAP financial measures is available in our earnings press release.  
Let me now turn the call over to Matt for his comments on the quarter. Matt?

**Matthew Murphy** (Executives):
Thanks, Ross, and good afternoon, everyone. Before I discuss our results and outlook, I want to briefly highlight 2 management transitions that occurred during our last quarter. First,  Willem Meintjes stepped down as Marvell's CFO in mid-June. I deeply appreciate Willem's steady hand, leadership and tireless commitment to transforming Marvell over his decade with the company, and I greatly respect his desire to spend more time with his family. To ensure a seamless transition, we simultaneously welcome Dan Durn as our new CFO. Dan brings more than 3 decades of experience in senior finance roles across semiconductor and enterprise technology companies. And having most recently served on Marvell's Board of Directors, Dan comes into the role with a deep understanding of our business and strategy as well as a unique appreciation for the significant growth opportunities at Marvell ahead. 
Second, in July, we began a transition in our Investor Relations leadership. After 8 years with Marvell, Ashish Saran will retire from the company in April 2027. I want to personally thank Ashish for his leadership, partnership and countless contributions to Marvell. I also appreciate the thoughtfulness and care he has brought to planning this transition, including helping us identify the right successor. On that front, I'm very pleased to welcome Ross Seymore, who comes to us from Deutsche Bank, where he covered the semiconductor industry for more than 25 years. A warm welcome to you, Dan and Ross. 
Now let me move on to our results and outlook. For the second quarter of fiscal 2027, Marvell delivered record revenue of $2.739 billion, reflecting 13% sequential and 37% year-over-year growth. Revenue and non-GAAP earnings per share of $0.94 both exceeded the midpoint of guidance. On our last earnings call, we increased our sequential revenue growth expectation for the third and fourth quarters of this fiscal year to double-digit percentage growth, up from our prior outlook of high single-digit growth. Since then, our outlook has continued to strengthen, and we now expect revenue growth to further accelerate in the second half. The strength is reflected in our guidance for the third quarter of fiscal 2027, where we expect total company revenue of $3.15 billion at the midpoint, representing growth of 15% sequentially and more than 50% year-over-year. 
We expect growth to further accelerate in the fourth quarter, both sequentially and year-over-year. As a result, we now expect overall Marvell revenue in fiscal 2027 to grow approximately 45% year-over-year to roughly $12 billion, up from our prior outlook of approximately $11.5 billion just 1 quarter ago. The increase in our revenue outlook continues to be driven by our Data Center business, which we now expect to grow by approximately 60% this fiscal year, up from our prior expectation of approximately 50%. Importantly, this growth remains broad-based. Interconnect continues to lead the way, while our custom business is expected to ramp significantly in the second half. For our communications and other end markets, the trajectory remains largely as expected. Despite typical quarter-to-quarter lumpiness in these businesses, we currently expect fiscal 2027 growth to approach our 10% target.  
Looking ahead to fiscal 2028, aggregate demand continues to accelerate, and our operations team is doing an outstanding job securing additional supply despite pervasive industry-wide constraints. As a result, we now expect Marvell's Data Center revenue to grow more than 60% year-over-year in fiscal 2028, driven by strong growth across all of our key data center businesses. This includes custom more than doubling as we indicated last quarter. We look forward to providing a deeper dive into the specific drivers of our longer-term growth at our Investor Day in New York City on October 6, but the key takeaway for today is clear. The strength of our data center business continues to exceed our prior expectations. 
Putting it all together, we now expect fiscal 2028 revenue of approximately $18 billion, up $1.5 billion from the $16.5 billion outlook we provided just 1 quarter ago. And importantly, even as our revenue base becomes significantly larger, our growth rate is accelerating. We now expect fiscal 2028 revenue to grow approximately 50% year-over-year compared with approximately 45% in our prior outlook. 
With that, let me provide color on our current business, beginning with Data Center. In our Data Center end market, we delivered record second quarter revenue of $2.17 billion, representing 18% sequential growth and 46% year-over-year growth. Both sequential and year-over-year growth accelerated from the first fiscal quarter when Data Center revenue increased 11% sequentially and 27% year-over-year.  
Now looking ahead to the third fiscal quarter, we expect this acceleration to continue with data center revenue forecasted to grow more than 20% sequentially and roughly 75% year-over-year. The drivers of this growth remain very broad-based as AI demand for our products continues to rise. We are seeing strong tailwinds across each of our data center businesses, including interconnect, switching and custom. Connectivity continues to be a critical enabler of AI performance driven by robust demand for both our interconnect and switching products. Thus far, the largest driver of growth for these businesses has been for scale-out applications. 
Here, Marvell's market-leading franchises in optical DSPs, switching and broadband analog components continue to see significant demand. On the optical DSP side, 800 gig demand remains strong, while our 1.6T business is ramping rapidly, a trend we expect to accelerate further in fiscal 2028. Within scale-out switching, our business remains on track to more than double this year driven by a strong ramp in our 51.2T products across a broadening array of customers. And within broadband analog, demand for our industry-leading TIAs and drivers continues to exceed expectations.
Now moving beyond scale-out, we expect this connectivity strength to broaden as hyperscalers build significantly larger AI clusters that increasingly span multiple data centers. As we have discussed on prior calls, aggregate bandwidth requirements for these scale across networks are projected to be more than 10x greater than those of current front-end DCI Networks. Marvell is ideally positioned to address this opportunity through our leadership in coherent enabled DSP -- coherent DSP enabled 1.6T ZR and ZR+ DCI modules.  
Finally, we continue to expect the adoption of scale-up networking and AI infrastructure to create a massive new TAM for Marvell. Scale-up domains are expected to become significantly larger, requiring high bandwidth interconnects closely coupled with high radix low-latency switches. Now while customers are initially deploying copper interconnect for scale-up networking, as cluster sizes grow, the reach and bandwidth limitations of copper are increasingly driving customers towards optical interconnects as well as purpose-built UALink ESUN and NVLink scale-up switches. As a result, we are investing aggressively to lead the industry in next-generation scale-up optical interconnect and switching technologies.  
On the interconnect side, pluggable modules remain the primary form factor for scale-out networks, and we do not expect that to change. However, the significantly higher bandwidth density required by scale-up networks is best served by bringing optics much closer to XPUs and switches. While the transition and scale-up networks from copper to optics is expected to take several years with both technologies coexisting, customers are aggressively planning scale-up optics deployment starting as early as next year.  
Given how early we are in this transition, customers are evaluating a broad range of potential solutions with multiple technologies under consideration, including NPO and CPO packaging options, with both leveraging advanced silicon photonics as well as 3 different modulator technologies, MZM, EAM and MRM. Each of these choices has different considerations around cost, power and technology maturity. Importantly, given the breadth of our optical portfolio across modulation technologies fully supported by our broadband analog TIAs and drivers, Marvell is uniquely positioned to help customers move towards the optical scale of architecture that best meets their needs. The full spectrum of Marvell developed solutions is reflected in accelerating design activity with a broad set of customers. In addition to our ongoing success in CPO, we are also seeing a strong adoption of our NPO solutions at multiple customers. As a result, our fiscal 2028 revenue outlook for scale-up optics has increased meaningfully compared to prior expectations, positioning Marvell to be one of the largest enabler of NPO in AI infrastructure.  
Moving to scale-up switching, we are seeing similar momentum. Marvell is uniquely positioned to support all 3 purpose-built scale-up protocols through our internally developed UAL and ESUN switches as well as our partnership with NVIDIA around NVLink Fusion. Our scale-up switches leverage decades of experience developing large reticle-size switch silicon combined with our in-house best-in-class high-performance SerDes technology. The close coupling of optics and switching in scale-up networks provides another important differentiator for Marvell, given our market-leading positions in both technologies. This allows us to deliver highly optimized scale-up solutions designed to provide customers with exceptional performance and reliability while accelerating time to market. 
As a result, we are engaged in multiple deep discussions with Tier 1 customers across our scale-up switch portfolio, with each engagement representing a multibillion-dollar lifetime revenue opportunity given the expected size of the scale-up TAM. Taken together, we are extremely excited about the continued acceleration and broadening of networking demand as AI architectures require ever-increasing performance across scale-out, scale-across and scale-up domains.  
Now let's turn to the custom business within our data center end market. As I mentioned earlier, we are seeing a significant acceleration in custom demand in the second half of this year. We remain confident that this business will more than double year-over-year in fiscal 2028 and accelerate significantly in fiscal 2029. We expect this growth to be driven by both our XPU and XPU attach products. In XPUs, we continue to make strong progress across current and next-generation programs at multiple hyperscalers.  
And in XPU attach, we are benefiting from increasing demand for both CXL and custom NIC. Looking further ahead, we expect our custom business to continue to deliver strong revenue growth as we see ongoing robust design activity with hyperscale customers. The most recent example of this momentum is the 8-K we filed last week, disclosing an expanded commercial agreement and associated warrant with a key hyperscaler, one of the largest adopters of custom silicon. The warrant agreement encompasses custom programs already in execution that were awarded to Marvell over the past several years, new design wins and future potential programs.
The warrant structure reflects the scale and long-term potential of the relationship and further aligns common interest as our work together expands, expands a broad range of custom silicon programs, including those that attached to the TPU ecosystem such as AI inference accelerators, storage controllers, network interface controllers, memory interface controllers and near-memory compute. We look forward to continue working closely with this customer to enable the next generation of AI infrastructure.
This expanding range of attached products and the scale of this agreement provides significant validation of the XPU attached category that Marvell has pioneered. We are excited to see both the use cases and attach rates for this category of products continue to broaden. These products are built upon a rich portfolio of Marvell IP and perform specialized functions designed to significantly improve the performance and efficiency of the overall AI data center. This is another strong confirmation of Marvell's leadership in connectivity, compute and memory technologies and the increasingly important role they play in enabling our customers to design more advanced AI infrastructure.
In terms of the impact of the new warrant agreement, revenue from programs covered by the agreement through fiscal 2028 is already reflected in the overall custom revenue target we have previously provided. Looking at fiscal '29 and beyond, this agreement, along with several additional programs gives us even greater confidence in our ability to grow the custom business to a significantly larger scale in that time frame. We look forward to sharing more details on the long-term trajectory of our custom business at our upcoming Investor Day.  
Turning to our communications and other end markets. We delivered second quarter revenue of $568 million, down 3% sequentially and up 10% year-over-year. Going forward, we expect to remain -- revenue to remain somewhat lumpy on a quarterly basis, given the mix of businesses in this segment. For the third fiscal quarter, we expect revenue to decline in the low to mid-teens percentage range both sequentially and year-over-year, followed by a solid sequential recovery in the fourth quarter.
To summarize, the momentum across our business remains exceedingly strong. In the near term, that strength is reflected in the significant increases to our outlook. Compared with the expectations we provided just 1 quarter ago, we have increased our fiscal 2027 revenue outlook by approximately $500 million and our fiscal 2028 outlook by approximately $1.5 billion. The center of this higher outlook is our data center business, where growth continues to both accelerate and broaden. We've increased our forecast for data center revenue growth in fiscal 2027 from our prior expectation of 50% to approximately 60%, and we see potential for further acceleration in fiscal 2028. 
Within connectivity, we continue to see strength established in areas such as optical DSPs, while also seeing significant growth across broadband analog TIAs and drivers, scale-across DCI modules and scale-out switching. Each of these 3 businesses is on or ahead of the trajectory towards the $1 billion annualized revenue run rate we highlighted last quarter. Scale-up opportunity remains massive and is still largely ahead of us. Marvell is ideally positioned for the transition toward NPO and CPO optical interconnects as well as the adoption of purpose-built scale-up switches. 
Our custom business, including both XPU and XPU attach is also on a strong growth trajectory, both near term and longer term. The 8-K we filed last week highlights the expanded scope of our relationship with a key hyperscaler and reinforces our confidence in the increasingly important role custom silicon will play in the ongoing AI infrastructure build-out. We look forward to sharing more about the longer-term growth opportunities we see for Marvell at our Investor Day on October 6 in New York City, and we hope to see many of you there.  
Now with that, I'll turn the call over to Dan for more details on our recent results and outlook.

**Daniel Durn** (Executives):
Thank you, Matt. Good afternoon, everyone. Before I get into the financials, since this is my first earnings call as Marvell's CFO, I want to spend a moment on 3 things: Why I joined Marvell? What I hope to accomplish as CFO? And what I believe that should ultimately mean for our stockholders? First, I joined Marvell because I believe the company has incredible growth potential. I believe Marvell is at a unique inflection point with a broad and diverse set of capabilities that have been intentionally built and are ideally aligned to enable the future of AI infrastructure.
Second, my goal as CFO is to help Marvell scale efficiently and effectively to capture what I expect to be a tremendous opportunity. The company has a strong history of disciplined execution and maintaining that rigor will remain paramount as we strategically allocate capital to fuel our growth. And third, I expect that growth to translate into significant value creation for our stockholders. I recognize that the growth opportunity ahead must be matched by its quality, and I plan to remain intensely focused on expanding operating margins, growing cash flow and driving attractive stockholder returns.
With that, let me turn to our financial results for the second quarter of fiscal 2027. Revenue was $2.739 billion, growing 37% year-over-year and 13% sequentially. Data center was our largest end market, contributing 79% of total revenue and growing 46% year-over-year. GAAP gross margin was 53.1%. Non-GAAP gross margin was 58.9%, slightly above the midpoint of our guidance. 
Moving to operating expenses. GAAP operating expenses were $996 million, including stock-based comp, amortization of acquired intangible assets, restructuring costs and acquisition-related costs. Non-GAAP operating expenses were $611 million, slightly above our guidance. GAAP operating margin was 16.8%, while non-GAAP operating margin was 36.6%. Non-GAAP operating margin expanded 180 basis points year-over-year and 160 basis points sequentially, demonstrating the significant operating leverage in our model. For the second quarter, GAAP earnings per diluted share were $0.33. Non-GAAP earnings per diluted share were $0.94, a penny above the midpoint of our guidance and up 40% year-over-year.  
Now turning to cash flow and the balance sheet. Cash flow from operations was $606 million in the second quarter, down slightly quarter-over-quarter, primarily reflecting the higher capacity prepayments to suppliers in support of Marvell's future growth. Inventory at the end of the second quarter was $1.36 billion, down just slightly from the prior quarter. During the quarter, we repurchased $200 million of our common stock through our ongoing capital return program and returned $54 million to stockholders through cash dividends. At the end of the second quarter, total debt was $4.96 billion, with gross debt-to-EBITDA ratio of 1.32x and net debt-to-EBITDA ratio of 0.27x. 
Turning to our guidance for the third quarter of fiscal 2027. We are forecasting revenue of $3.15 billion, plus or minus 5%. We expect GAAP gross margin to be between 52.9% and 53.9%. We expect our non-GAAP gross margin to be between 57.5% and 58.5%. Revenue levels and product mix remain key determinants of gross margin in any given quarter with the forecasted acceleration of our custom business creating the sequential headroom in the fiscal third quarter -- the sequential headwind in the fiscal third quarter. We currently expect to maintain gross margin in this range in the fourth fiscal quarter.
We project GAAP operating expense of approximately $1.015 billion in fiscal Q3 and non-GAAP operating expenses of approximately $655 million. We expect GAAP other income and expense, including interest on our debt to be an expense of approximately $86 million. On a non-GAAP basis, we expect other income and expense, including interest on our debt to be an expense of approximately $36 million. We expect a non-GAAP tax rate of 11%. Looking ahead, given the significant increase in our revenue and earnings outlook, we expect non-GAAP tax rate of approximately 13% in fiscal 2028. We expect basic weighted average shares outstanding of approximately $900 million and diluted weighted average shares outstanding of approximately $921 million, both roughly flat with the second quarter. 
We anticipate GAAP earnings per diluted share of $0.48 to $0.58. We expect non-GAAP earnings per diluted share of $1.05 to $1.15. As we look ahead, we intend to continue investing in our business to drive substantial revenue growth in the years ahead while delivering operating leverage. For fiscal 2027, we expect non-GAAP operating expenses of approximately $2.55 billion, slightly above our prior expectation of $2.45 billion, reflecting the significantly larger revenue opportunity we now see. Importantly, we expect revenue to continue growing substantially faster than operating expenses. As a result, we expect significant operating leverage with non-GAAP operating margin likely to enter our 38% to 40% long-term target range in Q4 of this fiscal year.  
Looking ahead to fiscal 2028. We currently expect non-GAAP operating expenses to grow at roughly half the rate of revenue growth in percentage terms. This reflects continued investment against an expanding opportunity set while yielding continued operating leverage to achieve the upper end of our target non-GAAP operating model of 38% to 40% as we progress through the year. Moving to cash usage. Based on the design wins we've secured and our confidence in the sustained customer demand, we're aggressively securing additional capacity to support our growth. We remain on pace to make approximately $1 billion of capacity prepayments to suppliers in fiscal 2027. Consistent with the guidance we provided last quarter, as a reminder, these prepayments will be applied against future material purchases and will be funded through our strong balance sheet, and robust operating cash flow. In parallel, we intend to continue repurchasing shares to manage dilution. 
Now let me come back to where I started. I joined Marvell because I believe the company has an exceptional opportunity ahead of it. Having now stepped into the CFO role, I'm even more convinced of the incredible strength of our technology portfolio, our deep customer relationships and the substantial long-term growth potential. Our job from here is to execute with discipline as we efficiently scale the company to capture that opportunity, and ensure that our growth translates into expanding margins, strong cash flow and compelling returns for our stockholders. I'm honored to be Marvell's CFO at such an important point in the company's evolution, and I look forward to working with Matt and the rest of the team to deliver on the incredible opportunity we see ahead.  
With that, ready to start Q&A. Operator, please open the line and announce the instructions.

**Operator** (Operator):
[Operator Instructions] And our first question Tom O'Malley with Barclays.

**Thomas O'Malley** (Analysts):
Appreciate it, good results. I wanted to ask first on the warrants with Google. Obviously, a very robust relationship over a multiyear period of time. I would love if you could give a color on what's contributing to that revenue? Obviously, you have an inference accelerator, but you talked a lot about XPU attach, which you guys did kind of start the industry standard on in terms of defining. So maybe what XPU attach are you excited about there? And like any sort of color you can give us on the percentage of contribution between the inference accelerator and some of the attach that you're seeing there?

**Matthew Murphy** (Executives):
Yes. Great. Thanks, Tom. Good to hear from you. So I think you captured it well. It's a very exciting time for Marvell. This engagement and warrant is significant. You can see that in the scale of the opportunity we have. And as you pointed out, a couple of things I would just validate. The first is it's very broad-based. It's a number of products and product lines, which is very exciting. It includes inference accelerators as you mentioned, also storage controllers, NICs, memory interface controllers, near-memory compute, a whole bunch of different products. And you're right, we did define the -- what we call the XPU attach category a couple of years back, and actually we gave quite a detailed view of that in our June 2025 custom silicon event. 
And I think all of our projections to date have been under called, meaning that opportunity continues to get more and more significant. So, it's a broad set of products, Tom, that are covered here, and it's very broad-based in terms of where we can engage and where we're going to contribute. And I wouldn't call out any one of them at the moment specifically, but all of them in total, you can see represent -- if you look at the total envelope of the opportunity, it's just massive for Marvell and game changing at the sort of peak performance of what could be achieved now over the next 6, 6.5 years.

**Operator** (Operator):
And your next question comes from Harlan Sur with JPMorgan.

**Harlan Sur** (Analysts):
Welcome to the team, Dan and Ross. Matt, given the Google commercial program you signed back in late July, a $120 billion in cumulative revs over 6 years, if you hit all of your milestones, right, that puts you if you just annualize it at about $18.5 billion per year in revenues just in Google XPU attach custom ASICs, right? I actually thought that, that would start to show up in fiscal '28 or your calendar '27, but given your guidance, it looks like custom is still going to be around $5 billion to $6 billion in calendar '27. 
But maybe some of the big programs associated with this commercial agreement more back-end loaded. So maybe the better question is, the team has previously targeted $10 billion to $11 billion in custom revenues in fiscal '29 or calendar '28. What does that number look like now based on the Google commercial agreement and some of the new programs associated with the agreement?

**Matthew Murphy** (Executives):
Yes. Yes. Great question, Harlan. Thank you. So first, you're right. If you look out to next year, we have comprehended already revenue that would come as part of this warrant in our numbers now. Now that's because some of these programs, obviously, are already in flight or have already started, but the programs ahead of us that are either in execution or just starting production, those will contribute much more significantly in fiscal '29. And for next year, all I've said, by the way, is that custom is going to over double. So I haven't capped it. I haven't sized it exactly, but it is going to overdouble next year. 
And then -- so then you look out to fiscal '29 where in our last call, I talked about a $10 billion kind of plus number for custom in fiscal '29, which isn't a new number, by the way. That was something that we outlined back in June '25 and even back in April '24, we were talking about custom revenues in the $8 billion to $10 billion range. So we've had a consistent view of what that can look like. This opportunity with this customer greatly increases the revenue opportunity for us in custom with some of that potentially starting in '29. I'm not going to size it on the call here today, but you should assume with our Investor Day coming up Harlan, the Marvell team, we always do a thorough job in our investor -- in our analyst/investor days.
And so you should expect a very robust detailed review of how we step through the revenue, not just through fiscal '29, but really out until the end of the decade. And so we're excited to present that to everybody, which will then really help us contextualize the scale of the warrant that we just signed, along with all the other exciting programs we have in custom. So if you don't mind, hold tight on that one, there will be more to come. But clearly, there's a lot of upside bias in those numbers in fiscal '29 and beyond in custom.

**Harlan Sur** (Analysts):
Yes, absolutely. Absolutely. Looking forward to it.

**Operator** (Operator):
Your next question comes from Vivek Arya with Bank of America Securities.

**Vivek Arya** (Analysts):
Best wishes to Dan and Ross. Matt, I was hoping you could give us an update on the other large XPU program that you're planning to start in the next year. I think the assumptions there are quite modest for next year, $600 million or $700 million or so, and I was hoping you could give us an update on that? And then what is the opportunity for that program over time? Because that hyperscaler is just getting started on their XPU type like every one of their competitors, I imagine they want to make that XPU program much larger than what it is. So give us maybe an update on what the progress is? Can this be a really meaningful program, right, for you over time?

**Matthew Murphy** (Executives):
Yes. Thanks, Vivek. So yes, we're very encouraged by our custom setup for next year on the double plus. That new program is clearly part of that. And we've been judging that, I think, in a very conservative and practical manner as we've made progress, but we make -- we continue to make progress every quarter, not only on design execution, but also supply commercials and figuring out the -- sort of the envelope of that opportunity. And that's only gotten better. So without quantifying it, exactly what I would say is from the last call, if you look at the $1.5 billion raise we're doing for next year, just at a high level, it's broad-based. 
So some of that is from custom next year. There's also -- actually get another question on this one, probably the most meaningful part of the next year raise is actually from the scale-up optics switching in other areas, but customs definitely part of it, Vivek. So even when we size that opportunity, which goes back to a couple of years, we've always said that, that is probably one of Marvell's largest revenue opportunity opportunities we have, and that's still the case. So we're very encouraged by the project -- the prospects of this project. And there'll be more to come, but it certainly is tracking, and we feel very good about next year and that layering in the year after and beyond.

**Operator** (Operator):
Your next question comes from Aaron Rakers with Wells Fargo.

**Aaron Rakers** (Analysts):
And welcome Dan and Ross. Maybe kind of building on that last question a little bit. Matt, if you can maybe talk a little bit about what you're architecturally seeing in CXL and how that's evolving, obviously, with the Structera product, and it seems to be a broadening ecosystem around that. And then similar on an architectural perspective, any update on -- you just touched on scale-up optics, the Celestial AI numbers that you've previously outlined. How have those progressed relative to your initial targets?

**Matthew Murphy** (Executives):
Sure. So let me start with CXL and then we'll talk about scale-up optics. So with respect to CXL, I mean this investment we made organically over the years has really evolved and is turning out to be a home run for a couple of reasons. As you might recall, this started off as a server-centric traditional compute-centric memory architecture. It turns out all that investment we've made is just ideal for memory expansion and inferencing. 
And so we're seeing this technology now getting deployed at multiple hyperscalers with varying architectures by the way, in extremely high volumes. One is just the demand of inferencing require it. The other is what we're seeing is as a result of the scarcity that's out there in memory. Customers are modifying and adjusting their plans to actually use more of this type of technology. So this has continued to have a strong upward bias. We've actually secured additional design wins in this area in the last couple of quarters. we're going to outline all of that at the Investor Day. But that opportunity, Aaron, turns out to be massive. 
And I think it's a case where the pivot we made about 5 years ago where we really put the pedal to the metal on organic internal investment on a number of new technologies. This is one that's really bearing fruit. So very exciting, and you'll -- you should expect to see a very comprehensive memory expansion section in our Investor Day presentation. 
On scale-up optics, this is turning out to be, I think, one of the most exciting areas for us. Last quarter, the way we framed it was we had the Celestial AI CPO photonic fabric solution, which for reference, was about $150 million for next year. We had actually said that overall scale-up optics inclusive of that was about $300 million as a category, that includes NPO, by the way. And as I said in my prepared remarks, all of that together, scale-up optics is accelerating even further from the number I gave you last quarter. And so, a significant driver of the $1.5 billion raise we have for next year, Aaron, is coming from that area. And it's not just a one-trick pony. I think that's the thing I want to stress to you is the CPO is absolutely a key part of it. It will be for next year and certainly the year after. But if I look at the opportunity set that's happening now at a much faster pace in parallel with the CPO programs we have is for NPO.
And in NPO, we participate through a wide variety of design wins we have and partners, some of those are with our broadband analog products in silicon germanium, both TIAs and drivers, which we have a significant market share and content and also on our own organically developed NPO solution, which we call our light engine, which we've been in development on for several years, and we've shown it off at OFC for several years.
So all of that is a category, Aaron, is really how we think about the business. Certainly, Celestial and Photonic Fabric is a key part of that. But what I want to stress is that this is not an or, it's an and. And it's a little bit analogous to when people thought, well, there's 800-gig DSPs and then they're going to move to 1.6T and it's all going to just cut over. That's not how this works anymore. Our customers have varying architectures that they're pursuing. They have a number of different solutions that they're going to implement simultaneously. So we see this as an and, not an or. And I think the magnitude of our scale-up optics opportunity next year is much larger than we thought just a quarter ago. The year after is going to be, I think, way larger than I sort of could have ever comprehended back even last year when we were looking at Celestial. 
And if you look at the solution we're providing, which you heard on my last comment, we are pedal to the metal on our switching road map and coupling those optical solutions with our switches, both UAL and ESUN, as well as being able to seamlessly integrate and architect with our customers on the XPU/GPU side. 
So all of that together and having the end-to-end length that we're able to provide and the entire solution and the scale in manufacturing, R&D, the diversity of all the technologies we have in terms of packaging, modulator technologies, silicon photonics, a decade of experience there. It's a massive opportunity and Marvell is very uniquely positioned to participate in it. And we couldn't be happier with the Celestial team. They've integrated well. They're a key part of the program. But this thing is going to be a much bigger overall business for Marvell.

**Operator** (Operator):
Your next question comes from Joe Moore with Morgan Stanley.

**Joseph Moore** (Analysts):
Along the same lines, can you talk about your progress in copper scale-up, and you mentioned the sort of success across the 3 protocols. How do you think about copper scale-up as it transitions to optical? Is it -- are those initial successes foundational to what you do in optical? Or are those sort of 2 separate decisions?

**Matthew Murphy** (Executives):
Yes. Thanks, Joe. I think you're talking about from a switching perspective, right, as we implement those electrical/copper solutions and then how does that success translate when we move to optical? So a couple of things. One is, on the Ethernet side, we've seen great traction and success with our Teralynx architecture, which came from the acquisition we did of a company called Innovium back in 2021. That business has a significant head of steam on it. We've expanded the customer base. We're driving significant revenue there, and we've proven to the market that we can deliver these solutions in volume. 
So that translates itself, Joe, very seamlessly to scale-out. And in fact, we're seeing even at 100T, our scale-out solutions be applicable to scale-up as well. So we're driving that independently of the optics or not. Same thing on UAL. We're aggressively investing in UAL switching, that product development is coming along nicely, and we certainly can intercept any electrical or copper-based solution there. What customers really want to see though, and that's why I'm spending time on it, is, that's all great. And at this point, they trust us that we can deliver these very complex switching products because we've done it already, which by the way, is no small feat. There's been a lot of companies that have tried and failed to do these radical size very complex Ethernet switches, and it's only getting harder with the SerDes performance and the speeds. 
But the next level of that, Joe, is that you then need to show a compelling clear roadmap that you can execute with credibility on the optics side, both NPO and then all the way to full integration on CPO. And so our additions while certainly there's opportunities in the next few years that are going to come and we're going to have on the copper side, I think why we really win long term is because we convince our customers we can execute on the full end-to-end, which really is what our customers are looking for at the end of the day, especially in scale-up, they need to bookend the link, and they need to trust it on both sides of it and everything in between. They've got a partner that can handle that job.
And point solutions at this juncture, we believe are not going to get it done. You really have to have the end-to-end portfolio. And that's what we're hearing from our customers, by the way. So the existing silicon will do fine, and it will do great, but I'm even more excited about the optics attach once that gets going over the next few years, because it just effectively almost doubles the SAM of the switching in terms of the attach you can get. Thanks.

**Operator** (Operator):
Your next question comes from Ben Reitzes with Melius Research.

**Benjamin Reitzes** (Analysts):
Matt, so I want to go back to the Google deal. I think people are just wrestling with this. And I realize that you have a great Analyst Day coming. So I -- don't shoot me. But for FY, if you look at the $120 billion over the course of the years, that's about $18 billion a year, and at the $120 billion divided by 6.5. And that's like adding an FY '28, Marvell every year. And I realize that we don't know how much is incremental versus what's already in your guide. 
But, are we talking like FY '29 and FY '30 big step-ups as a result of this incrementally, because these numbers are huge. And I know you're going to tell us at the Analyst Day, but I think we're all just trying to figure out how high to go in those out years? And is it at the comparable margin? And -- just any more color if you're in our shoes, how we should handle it into Analyst Day or just wait, that would be great.

**Matthew Murphy** (Executives):
Yes, Ben, thanks. And by the way, fully valid question. I mean, when you look at the scale of this, your math is not wrong. And what you can conclude from what I'm saying is, because most of this is comprehended already in next year, the big impact would be in '29 and beyond. So it's -- if you took the full performance and the full opportunity, then you're right, it's just -- it's just a monster number.
What I would say -- and so we do need the Analyst Day, though, I think you guys understand to contextualize it and probably show some ranges of outcomes. But you should assume in that time frame that on the custom side, these numbers would be a lot larger than -- overall custom than anybody has been modeling so far. I mean, I think there's been doubt for years that we could even do the $8 billion to $10 billion. This should give, I think, investors comfort that we secured a pretty big set of programs, not just here, but across the broad range of our customer set.
On the margins, just in general, this is a custom business, and we've got a financial model for custom. We've got a financial model for our standard and merchant products. It would be in line with that, but it's significant. And I'm not able to quantify it today for you, but you should assume starting in FY '29 and beyond whatever you've modeled previously prior to the warrant for custom numbers definitely goes higher. How big, we'll be happy to show the range of outcomes. 
But in the context of where Marvell was, Ben, I mean, we were an $8 billion company last year. We just took everybody to $12 billion this year. We haven't even finished that year and $18 next year. And the rough math you do at full performance provides an incredible step up to the scale of the company. If all those programs that come to fruition at their max performance, which -- but I think what this is helpful to show is just the scale of the opportunity in general that Marvell is participating in. Because we have significant engagements across the customer base. This one is a little unique because of the warrants that given the magnitude and the equity side, we needed to disclose it. 
But I think you've seen over the last couple of years, we've entered into very strategic partnerships with other big players in the AI market. And some of that we've done publicly and some of that we're doing just on our own. So I think one takeaway I would have right now is just a significant validation of where Marvell sits in the market today, and we're very honored to be a part of the ecosystem, the TPU ecosystem. We'll see how it plays out. But I hope that's enough for now. I want to save a little bit of firepower for my Investor Day.

**Benjamin Reitzes** (Analysts):
And I appreciate that and congrats on that deal. I'll see you soon.

**Operator** (Operator):
Your next question comes from CJ Muse with Cantor Fitzgerald.

**Christopher Muse** (Analysts):
I think one of the more interesting takeaways from NVIDIA's report last night is Jensen's view of the fungibility of compute, networking and memory to deliver performance in the AI data center in a cost-constrained world. And considering your vast experience and expertise across all these 3 areas, how is this backdrop, particularly in light of where memory pricing is today, support your new design wins? And is it really focused on the memory controllers, custom HBM to increase shoreline? Or is it also driving strength on the XPU side as well? Would love to hear your thoughts there.

**Matthew Murphy** (Executives):
Yes. Thanks, CJ. No -- first of all, I see the same thing. I'm very mind-melded with what they talked about. I think at the broadest level to start, it definitely -- this fungibility requirement, given the dynamic nature of the market and some of the constraints we're seeing. Some are supply constraints, some are power constraints, some are architectural constraints, having our ability to very quickly execute custom and semi-custom designs or modify our products or adapt to shifting architectures at Marvell. It's a key capability, the flexibility that the company has, because we've built a business around being able to customize quickly, and it's been in our DNA even from 2021 Investor Day. We talked about how every hop in the network at some point was going to get some level of customization, it wasn't going to just be the accelerator. And here we are 5 years later, and that's playing out. 
CXL and memory expansion is one example, where very quickly customers are adapting, but there's also other opportunities where to optimize for inference as an example, and this is one of the things that was in the warrant, but it's a trend in the market. AI inference accelerators, that's another trend in the market you see. So I think companies are all looking at how they can maximize their performance, how they can maximize the cost and performance relative to the tokens generated.
And we're in a monetization era. So this stuff really matters. It went from training very, very quickly to inference and to companies now monetizing this. And so we're seeing a big pickup in activity. And it's not just on the custom side. I mean this discussion we had earlier about CPO and NPO and optics and copper, that's all moving very, very fast because, again, companies are architecting at a speed we really haven't seen to make sure that they have the most competitive solutions. 
So Marvell fits right in there, CJ, on a number of fronts. It's not just "our custom" revenue, but it's the solutions underneath we provide including our networking and our storage and -- storage and memory in our compute.

**Operator** (Operator):
Your next question comes from Jim Schneider with Goldman Sachs.

**James Schneider** (Analysts):
I was wondering if you could maybe just give us a little bit of update in terms of the growth rate for connectivity, you expect. I think, Matt, you outlined those growth rates for both this fiscal year, next fiscal year last quarter. Can you maybe just give us an update on where those are landing, given the incremental strength. It sounds like most of that's being driven by that subsegment right now?

**Matthew Murphy** (Executives):
Well, yes, thanks, Jim. As I said, the way to think about it is the $500 million raise for this year and the $1.5 billion for next year is broad-based. Connectivity clearly is a driver, and I say connectivity at a broader level because underneath that, we spent time talking about scale-up optics, that's one, which is our NPO and CPO and SiGe products. But it's also just the transceiver market for scale-out and optical DSPs going into that segment, that's upsized versus the prior growth rates we talked about. So that's in the $500 million and the $1.5 billion, that business continues to be absolutely on fire, and we're executing well there.
And then within connectivity as well as a broader segment, you also have our switching, which is biasing higher this year, but also from our last quarter update, again next year. So you really have those 3, plus, I'd say, custom that are all floating up versus our prior expectations. But Jim, we're really seeing broad-based strength. There's -- I think it's across almost all of our product lines when we look out, but those are a few of the ones I'd highlight. And you're right. The connectivity is a bigger bucket, it is probably the largest driver net-net of the $1.5 billion raise. If I just look at all those pieces I mentioned underneath, scale-out, scale-up and switching.

**Operator** (Operator):
And our last question for today comes from Quinn Bolton with Needham & Company.

**Quinn Bolton** (Analysts):
I guess, Matt, just wanted to come back to the sort of the near-term guidance. Within data center, I think you guided up greater than 20% sequentially. But with margins coming down 90 basis points quarter-on-quarter, is custom the fastest-growing segment within data center that drives that lower margin? Or is there some other mix going on within data center kind of driving the lower 90 -- or sorry, that 90 basis point lower guidance for the October quarter?

**Matthew Murphy** (Executives):
Yes, sure. Thanks. Let me -- I'll tee it up, but I'm going to have Dan comment because you guys are sparing him too much on this call. I mean, he's the new CFO. You're supposed to be asking him questions and you're asking me all the questions. So joking aside, you can clearly see it in the numbers. I mean, stronger Q3 guide implied a much stronger Q4 guide. We did say custom was ramping meaningfully in the second half. I said that, Dan said that. But Dan, maybe why don't you make a few comments on the margins and how you see that playing out and also through next year as well as we grow.

**Daniel Durn** (Executives):
Sure. So just jumping in, we clearly see the performance of the company doing well. You see the acceleration in Q2, followed with acceleration in Q3, followed with acceleration in Q4. Part of the acceleration story in Q3, as you point out, mix is the primary driver. We've got a strong ramp in custom. And so you can see that play out in the profiling of the margins. Not a surprise. We've been signaling that custom ramp for quite some time as we window into Q4, that strength, we're signaling a bigger step-up, much larger step-up from a revenue standpoint, if you roll in the $12 billion annual target. 
And that step up in Q4 is broad-based. You see it not only in custom, you see it in connectivity. You see it in a rebound in comm and other. So broad-based performance. Net it all out, we see gross -- Q4 gross margins in the same target range as Q3. If we use the back half of the year as a jumping-off point and think about how that looks going into FY '28, that broad-based strength continues. We take the momentum exiting this year and we push that forward into next year, and it's across custom, it's across connectivity. All parts of the business are higher. They're up. 
Gross margin depends on ultimate mix. My preliminary view is gross margins next year are going to be in a similar range, same range as we're exiting this year. So back half of this year, same range for FY '28. So we feel good about the performance of the company. We're going to drive growth at this company. We're going to do it with discipline, and we're going to deliver strong margins. But when we think about that margin profile, operating margin still has significant leverage embedded in it. You're going to see it up in Q3. You're going to see us entering our target long-term model range, 38% to 40% exiting this year. You'll see us achieve the high end of that range as we progress through FY '28, and we're going to reset that long-term target model here in the coming weeks at the Analyst Day. So we feel good about the performance of the company and the broad-based strength.

**Operator** (Operator):
Thank you. And ladies and gentlemen, thank you all for your participation. This does conclude today's teleconference. You may disconnect and have a wonderful day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MRVL_Q1_2027_Earnings_Call_20260527.md
- 2026-05-27｜CEO｜guidance：CEO 說明 Q3、Q4 營收各季對季成長至少 10%。（原話："to also grow by at least 10% sequentially."）
- 2026-05-27｜CEO｜guidance：CEO 回顧上一季說法：自 Q2 起各季對季成長為高個位數。（原話："trend in the high single-digit range sequentially"）
- 2026-05-27｜CEO｜guidance：CEO 表示本次再度上調展望（FY27 營收預測增加逾 5 億美元，FY28 增加約 15 億美元）。（原話："we are again raising our outlook"）
- 2026-05-27｜CEO｜guidance：CEO 給 FY27 全公司營收約年增 40%、近 115 億美元。（原話："year to nearly $11.5 billion."）
- 2026-05-27｜CEO｜guidance：CEO 給 FY28 營收約 165 億美元，並稱較上季展望高約 15 億美元。（原話："fiscal 2028 revenue to reach approximately $16.5 billion"）
- 2026-05-27｜CEO｜guidance：CEO 預期 FY28 資料中心營收約年增 55%，快於 FY27 預期成長率。（原話："revenue in fiscal 2028 to grow approximately 55%"）
- 2026-05-27｜CEO｜guidance：CEO 說明 FY28 規劃假設雲端 CapEx 成長率放緩至 30% 以上區間。（原話："planning for the rate of cloud CapEx growth to moderate"）
- 2026-05-27｜CEO｜guidance：CEO 給 Q2 資料中心營收對季成長預期（中高十位數百分比）。（原話："data center revenue growth to accelerate into the mid-"）
- 2026-05-27｜CEO｜guidance：CEO 給 Q2 通訊及其他市場營收對季下滑中個位數。（原話："expect revenue to decline in the mid-single-digit range"）
- 2026-05-27｜CFO｜guidance：CFO 給 Q2 營收區間：27 億美元正負 5%。（原話："$2.7 billion, plus or minus 5%"）
- 2026-05-27｜CFO｜guidance：CFO 給 Q2 non-GAAP EPS 區間 0.88–0.98 美元。（原話："in the range of $0.88 to $0.98"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY28 165 億美元之下，互連業務仍有向上偏誤。（原話："there's upward bias for sure"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY27 互連業務年增逾 70%。（原話："our interconnect business to grow more than 70%"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY28 客製化業務預期年增超過一倍，高於先前展望。（原話："our custom business to more than double year-over-year"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY27 客製化業務維持年增逾 20%。（原話："Custom revenue remains on track to grow more than 20%"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY28 1.6T 營收將再顯著墊高。（原話："We expect 1.6T revenue to take another substantial step up"）
- 2026-05-27｜CEO｜guidance：CEO 稱 TIA 與驅動器季營收數季內將超過年化 10 億美元。（原話："exceed a $1 billion annualized run rate"）
- 2026-05-27｜CEO｜guidance：CEO 稱 DCI 模組業務對 FY28 年化營收 10 億美元有可見度。（原話："line of sight to a $1 billion annualized revenue"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY27 scale-out 交換器營收將超過 6 億美元。（原話："scale-out switch revenue in fiscal 2027 to exceed $600"）
- 2026-05-27｜CEO｜guidance：CEO 稱交換器業務在 FY28 年化營收追蹤超過 10 億美元。（原話："see the business tracking to more than $1 billion"）
- 2026-05-27｜CEO｜guidance：CEO 稱 AEC 與 retimer 合併營收 FY27 將成長逾一倍。（原話："combined revenue to more than double year-over-year"）
- 2026-05-27｜CEO｜guidance：CEO 稱 scale-up 光學業務 FY28 營收將大幅躍升，較先前僅含 Celestial AI 的約 1.5 億美元展望增逾一倍。（原話："we expect our scale-up optics business to ramp significantly"）
- 2026-05-27｜CEO｜guidance：Q&A 中 CEO 稱 scale-up 光學目前估計約 3 億美元。（原話："effectively calling at this point to be about $300 million"）
- 2026-05-27｜CEO｜guidance：CEO 稱 scale-up 網路與交換器幾乎未計入 165 億美元（逐字稿原文如此）。（原話："that's not very little or nothing in the $16.5 billion"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY28 客製化成長三大來源比例與上季相近。（原話："it's roughly the same ratio"）
- 2026-05-27｜CFO｜margin：CFO 報 Q1 non-GAAP 毛利率。（原話："non-GAAP gross margin was 58.9%"）
- 2026-05-27｜CFO｜margin：CFO 給 Q2 non-GAAP 毛利率區間。（原話："non-GAAP gross margin to be between 58.25% and 59.25%"）
- 2026-05-27｜CFO｜margin：CFO 說明毛利率取決於營收水準與產品組合。（原話："revenue and product mix will remain key determinants"）
- 2026-05-27｜CFO｜margin：CFO 解釋 Q1 GAAP EPS 低於財測，來自 Celestial AI 與 XConn 購併會計及 earn-out。（原話："$0.04 lower than our guidance"）
- 2026-05-27｜CFO｜margin：CFO 稱 FY28 non-GAAP 營業費用成長遠低於營收成長。（原話："we expect non-GAAP operating expense to grow year-over-year"）
- 2026-05-27｜CFO｜margin：CFO 給 FY27 non-GAAP 營業費用約 24.5 億美元，含兩項購併（逐字稿誤植為 earnings expense）。（原話："expense of approximately $2.45 billion"）
- 2026-05-27｜CFO｜commitment：CFO 承諾 FY28 營業利益率達目標模型上緣。（原話："operating margin model of 38% to 40%"）
- 2026-05-27｜CEO｜commitment：CEO 重申對客製化業務 FY29 逾 100 億美元的目標有信心。（原話："deliver on over $10 billion in revenue in fiscal 2029"）
- 2026-05-27｜CEO｜commitment：CEO 稱新 Tier 1 XPU 專案已有涵蓋下一整個財年的明確需求。（原話："we already have firm requirements in place for all of next"）
- 2026-05-27｜CEO｜commitment：CEO 稱新斬獲設計的典型開發週期約兩年才貢獻增量營收。（原話："typical development cycle of approximately 2 years"）
- 2026-05-27｜CFO｜capital_allocation：CFO 預計本財年約 10 億美元供應商預付款，自 Q2 起。（原話："approximately $1 billion in prepayments"）
- 2026-05-27｜CFO｜capital_allocation：CFO 報 Q1 買回 2 億美元股票。（原話："we repurchased $200 million of our stock"）
- 2026-05-27｜CFO｜capital_allocation：CFO 說明後續持續買回股票以管理稀釋。（原話："we plan to continue to repurchase shares to manage"）
- 2026-05-27｜CEO｜capital_allocation：CEO 宣布收購 Polariton（電漿子矽光子元件）。（原話："the acquisition of Polariton, a developer of high-speed"）
- 2026-05-27｜COO｜risk：COO 說明 AI 相關供應自 2020–2021 起持續受限。（原話："I don't think we've been in an unconstrained environment"）
- 2026-05-27｜COO｜risk：COO 說明確保產能的做法：向少數關鍵供應商提供五年預測。（原話："giving them a 5-year forecast of what we need"）
- 2026-05-27｜CEO｜customer：CEO 稱 DCI 方案已出貨給全部五大美國超大規模業者。（原話："we shipped DCI solutions to all 5"）
- 2026-05-27｜CEO｜customer：CEO 稱 Celestial AI 方案已被一家 Tier 1 超大規模業者選用於下一代 XPU scale-up。（原話："The solution has already been selected by a Tier 1"）
- 2026-05-27｜CEO｜customer：CEO 稱 AEC 已取得三家 Tier 1 美國超大規模業者設計案。（原話："design wins with 3 Tier 1 U.S. hyperscalers"）
- 2026-05-27｜CEO｜customer：CEO 稱新 Tier 1 XPU 專案約占明年客製化總成長的三分之一。（原話："probably still about 1/3 of the total growth"）
- 2026-05-27｜CEO｜customer：CEO 稱近期新設計案不是既有預測所需，視為保險。（原話："Think of that as like an insurance policy."）
- 2026-05-27｜CEO｜customer：CEO 稱客製化預測不需要任何增量。（原話："it's not requiring anything incremental"）
- 2026-05-27｜CEO｜product：CEO 說明與 NVIDIA 的 NVLink Fusion 整合內容。（原話："This allows Marvell to build custom chips and networking"）
- 2026-05-27｜CFO｜product：（逐字稿標示為 Willem Meintjes 回答）稱 XPU（原文為 XPO）attach 單一項目數年內營收將逾 10 億美元。（原話："attach alone over $1 billion in revenue"）
- 2026-05-27｜CFO｜competition：（同上段發言者）稱記憶體週期的疑慮正推動 CXL 設計採用。（原話："driving additional adoption of CXL-based design"）

### MRVL_Citi_s_2026_Global_TMT_Conference_20260909.md
- 2026-09-09｜CEO｜guidance：CEO 說明營收口徑已從一年前的兩年 $20B 拉到本財年 $12B、下財年 $18B（原話："we can do $12 billion this year and $18 billion next year"）
- 2026-09-09｜CEO｜guidance：CEO 稱資料中心營收從 2023 曆年約 $2.2B 到明年約 $15–16B（原話："next year, we're looking at $15 billion, $16 billion"）
- 2026-09-09｜CEO｜guidance：CEO 稱連接業務今年成長 70% 以上，明年維持高成長但未給具體數字（原話："that business this year is growing like 70% plus"）
- 2026-09-09｜CEO｜guidance：CEO 提到供應鏈一年內彈性上調約 50%（原話："our supply chain has been able to flex up 50%"）
- 2026-09-09｜CEO｜guidance：CEO 回溯上一季對 NPO/CPO 明年營收的說法為 0 至 $300M（原話："we said it was going to be 0 to $300 million"）
- 2026-09-09｜CEO｜guidance：CEO 稱上一季已說該數字會高得多（原話："This past quarter, I said that was going to be much higher"）
- 2026-09-09｜CFO｜guidance：CFO 給營業利益率路徑：本年底進入長期目標區間（原話："exit this year entering the long-term target model"）
- 2026-09-09｜CFO｜guidance：CFO 稱明年底觸及該區間上緣（原話："We will exit next year touching the top end of that range."）
- 2026-09-09｜CFO｜margin：CFO 稱 Q3、Q4 營業利益率連續季增（原話："increase in operating margin in Q3 and again in Q4"）
- 2026-09-09｜CFO｜margin：CFO 稱客製化占比上升時毛利率會逐步下降（原話："you will see incremental step down"）
- 2026-09-09｜CEO｜margin：CEO 說明客製化 NRE 以 contra R&D 入帳（原話："an offset or contra R&D"）
- 2026-09-09｜CEO｜margin：CEO 稱明年毛利率可在客製化翻倍下大致持平並伴隨營業利益率擴張（原話："gross margin flattish with OM expansion"）
- 2026-09-09｜CEO｜margin：CEO 拆解 $13.5B 到 $18B 的上調來源，多數來自互連、交換器與儲存（原話："most of that raise has come from interconnect and switching"）
- 2026-09-09｜CFO｜margin：CFO 稱營運費用成長約為營收成長的一半（原話："your OpEx will grow roughly half the rate of revenue"）
- 2026-09-09｜CFO｜commitment：CFO 承諾分析師日重設長期營業利益率目標（原話："we'll reset what we think the new long-term target is"）
- 2026-09-09｜CEO｜commitment：CEO 稱客製化 FY29 目標軌道正常，並預告分析師日將給區間（原話："we probably need to give a range for the future"）
- 2026-09-09｜CEO｜commitment：CEO 預告 10/6 投資人日（原話："We got an Investor Day coming up on October 6."）
- 2026-09-09｜CEO｜commitment：CEO 稱到目前為止拿到足夠供給以兌現承諾（原話："we're getting what we need, I think, to deliver"）
- 2026-09-09｜CEO｜product：CEO 稱 Teralynx 交換器業務預計達 $1B 以上（原話："on track to do $1 billion plus"）
- 2026-09-09｜CEO｜product：CEO 稱 scale-up 目前尚屬綠地市場（原話："sort of greenfield at the moment"）
- 2026-09-09｜CEO｜product：CEO 稱 NPO 與 CPO 並存而非二選一（原話："this is not an or. This is going to be an and"）
- 2026-09-09｜CEO｜product：CEO 稱 1.6T 的 2nm DSP 率先宣布（原話："We were first to market on announcing our 2-nanometer DSPs"）
- 2026-09-09｜CEO｜product：CEO 稱 scale across 可能使 DCI 市場放大數倍（原話："that could 2, 3, 4, 5x the size of the DCI market"）
- 2026-09-09｜CEO｜product：CEO 稱現有業務仍以每年 50% 以上成長（原話："the existing businesses growing at 50% a year plus"）
- 2026-09-09｜CEO｜product：CEO 稱交換器加光學為下一個大型成長引擎（原話："switching plus optics is going to be very big"）
- 2026-09-09｜CEO｜competition：CEO 稱 1.6T 地位與以往同樣強（原話："we're as well positioned as we've ever been at 1.6T"）
- 2026-09-09｜CEO｜competition：CEO 預期多家公司將推出 XPU attach 策略（原話："a whole bunch of companies are going to come out"）
- 2026-09-09｜CEO｜competition：CEO 稱競爭對手多只有一塊拼圖（原話："A lot of our competitors don't have that."）
- 2026-09-09｜CEO｜customer：CEO 稱涵蓋四大美系雲端業者的設計案已逾 20 件（原話："20-plus design wins across all the 4 U.S. hyperscalers"）
- 2026-09-09｜CEO｜customer：CEO 說明 Google 的 8-K 認股權屬 XPU attach 關係（原話："that is really an XPU attach relationship"）
- 2026-09-09｜CEO｜customer：CEO 稱客製化業務將多元而非單一插槽（原話："there's no one trick pony in there"）
- 2026-09-09｜CEO｜customer：CEO 稱與 NVIDIA 的關係是反向於緊張（原話："I would say it's the opposite of tension."）
- 2026-09-09｜CEO｜risk：CEO 稱供給自疫情以來持續吃緊（原話："It's been constrained since the pandemic."）
- 2026-09-09｜CEO｜risk：CEO 稱部分領域目前特別吃緊（原話："It's very acute right now in some areas."）
- 2026-09-09｜CEO｜risk：CEO 提到社會對資料中心的反彈（原話："societal pushback"）
- 2026-09-09｜CEO｜risk：CEO 稱若供給無限則產業總會過度擴張（原話："the industry always overdoes it"）
- 2026-09-09｜CFO｜capital_allocation：CFO 稱資本配置第一支柱為讓公司成長（原話："pillar 1 of capital allocation is grow the company"）
- 2026-09-09｜CFO｜capital_allocation：CFO 稱保留彈性以供應鏈下單（原話："preserve the flexibility to put order in the supply chain"）
- 2026-09-09｜CEO｜capital_allocation：CEO 稱已提高 CapEx 與預付款規模（原話："We've upped the CapEx and the prepays"）

### MRVL_Analyst_Investor_Day_Marvell_Technology_Inc_20261006.md
- 2026-10-06｜CEO Matt Murphy｜guidance：FY28 總營收展望由八月的約 180 億美元再上調至約 200 億美元。（原話："approximately $20 billion in total company revenue"）
- 2026-10-06｜CEO Matt Murphy｜guidance：FY28 資料中心營收預期成長約 80%。（原話："we expect data center revenue to grow approximately 80%"）
- 2026-10-06｜CEO Matt Murphy｜guidance：FY29 客製化（custom）營收目標由逾 100 億上調為 FY28 的三倍以上、逾 120 億美元。（原話："custom revenue in FY '29 to more than triple from FY '28"）
- 2026-10-06｜CEO Matt Murphy｜guidance：FY31 長期營收目標區間為 700 億至 900 億美元，中點 800 億。（原話："a range of $70 billion to $90 billion in revenue"）
- 2026-10-06｜CEO Matt Murphy｜guidance：FY31 資料中心營收對應 55%–70% 成長區間，約 675 億至 875 億美元。（原話："approximately $67.5 billion to $87.5 billion"）
- 2026-10-06｜CEO Matt Murphy｜guidance：CEO 稱自下而上的路徑是資料中心營收 FY28 後年增約 70% 至 FY31，CapEx 假設趨緩。（原話："growing our data center revenue at roughly 70% annually"）
- 2026-10-06｜SVP Xi Wang｜guidance：FY31 互連（interconnect）中點目標約 375 億美元。（原話："approximately $37.5 billion in FY '31 at the midpoint"）
- 2026-10-06｜CEO Matt Murphy｜guidance：FY31 交換器與儲存中點約 100 億美元。（原話："approximately $10 billion in switching and storage revenue"）
- 2026-10-06｜CEO Matt Murphy｜guidance：FY31 客製化中點約 300 億美元。（原話："approximately $30 billion at the midpoint in FY '31"）
- 2026-10-06｜CEO Matt Murphy｜guidance：通訊及其他業務假設僅維持位置、成長極小。（原話："maintain our position with very modest growth"）
- 2026-10-06｜CFO Dan Durn｜guidance：CFO 稱 FY31 資料中心 CAGR 中點為 65%，與 CEO 口述的約 70%／55–70% 區間口徑並陳。（原話："a 65% CAGR at the midpoint of our long-term model"）
- 2026-10-06｜CFO Dan Durn｜guidance：CFO 給三條產品線中點 CAGR：客製化約 80%。（原話："We see a revenue CAGR of approximately 80% at the midpoint"）
- 2026-10-06｜CFO Dan Durn｜guidance：CFO 給互連中點 CAGR 約 65%。（原話："we forecast a revenue CAGR of about 65% at the midpoint"）
- 2026-10-06｜CFO Dan Durn｜guidance：CFO 給長期模型 FY31 non-GAAP EPS 中點大於 30 美元（「$30 in '30」）。（原話："non-GAAP EPS of greater than $30 a share in FY '31"）
- 2026-10-06｜SVP Russ Esmacher｜guidance：Russ 稱其相干（coherent）業務由 FY26 約 5 億美元成長至 FY28 逾 10 億美元。（原話："$500 million in fiscal '26 to safely over $1 billion"）
- 2026-10-06｜EVP David Lazovsky｜guidance：Teralynx 交換器業務（51T 放量）明年預期超過 10 億美元。（原話："exceed north of $1 billion and significantly so"）
- 2026-10-06｜CFO Dan Durn｜margin：FY31 毛利率目標 56%–59%，依產品組合而定。（原話："We expect a gross margin of 56% to 59%"）
- 2026-10-06｜CFO Dan Durn｜margin：CFO 說明客製化毛利率相對較低，但因客戶出資 NRE 與規模，營業利益率仍具吸引力。（原話："Custom silicon carrying a relatively lower gross margin"）
- 2026-10-06｜CFO Dan Durn｜margin：CFO 說毛利率區間低端需要客製化營收大幅優於基本預測，連接業務超預期則趨向高端。（原話："it likely requires a significant upside to the base case"）
- 2026-10-06｜CFO Dan Durn｜margin：FY31 營業利益率目標 44%–46%。（原話："We expect an operating margin of 44% to 46%"）
- 2026-10-06｜CFO Dan Durn｜margin：營業費用成長速度約為營收成長的一半，是營業槓桿假設的來源。（原話："grow operating expenses at roughly half the rate of revenue"）
- 2026-10-06｜CFO Dan Durn｜margin：稅率 15%、自由現金流利潤率長期大於 36%。（原話："a free cash flow margin of greater than 36% over time"）
- 2026-10-06｜CEO Matt Murphy｜margin：CEO 重申去年說法：XPU attach 毛利率高於 XPU，原因含 IP 差異化與量。（原話："you should expect that the XPU attach side is more margin"）
- 2026-10-06｜President/COO Chris Koopmans｜commitment：COO 表示達成目標不需要新的大型設計案或新 socket。（原話："We don't need any new home run design wins"）
- 2026-10-06｜President/COO Chris Koopmans｜commitment：COO 對交付預測作出明確承諾。（原話："my team and I are going to deliver that forecast"）
- 2026-10-06｜President/COO Chris Koopmans｜commitment：COO 稱明年 200 億美元所需的供給已備妥。（原話："the supply I need to hit the $20 billion next year"）
- 2026-10-06｜President/COO Chris Koopmans｜commitment：COO 稱靠前四大美國超大規模客戶即可達成 Murphy 所述目標的絕大部分。（原話："we can hit the vast majority of the goals that Matt laid out"）
- 2026-10-06｜EVP Will Chu｜commitment：客製化負責人表示不需新增勝案即可達成客製化目標。（原話："we don't need new wins to achieve our target."）
- 2026-10-06｜CFO Dan Durn｜commitment：CFO 稱長期目標不依賴單一大型 socket。（原話："no mega socket is needed to deliver on our long-term targets"）
- 2026-10-06｜CEO Matt Murphy｜commitment：Murphy 表示在互連的 scale-out 與 scale-across 不打算流失市占。（原話："We don't intend to lose any market share there"）
- 2026-10-06｜CFO Dan Durn｜commitment：CFO 承諾平均長期返還超過 50% 自由現金流。（原話："returning greater than 50% of our free cash flow on average"）
- 2026-10-06｜CFO Dan Durn｜capital_allocation：CFO 回顧 FY21–FY26：有機研發約 80 億美元，併購約 110 億美元。（原話："$11 billion of inorganic investments"）
- 2026-10-06｜CFO Dan Durn｜capital_allocation：同期以股利與買回返還股東約 40 億美元。（原話："returning about $4 billion to shareholders via dividends"）
- 2026-10-06｜President/COO Chris Koopmans｜capital_allocation：COO 稱公司已投入資本預付產能以鎖定供應鏈，並給供應商五年預測。（原話："we are investing ahead of our growth to reserve the capacity"）
- 2026-10-06｜President/COO Chris Koopmans｜capital_allocation：COO 說明 FY24 研發投入占資料中心營收超過一半。（原話："investing well north of 50% of our revenue back into R&D"）
- 2026-10-06｜CEO Matt Murphy｜customer：客製化矽已出貨給全部四家美國超大規模雲端業者。（原話："we're shipping custom silicon to all 4 U.S. hyperscalers"）
- 2026-10-06｜President/COO Chris Koopmans｜customer：COO 揭露與 Google 的協議：6.5 年 1,200 億美元的 TPU 生態系客製化機會。（原話："$120 billion opportunity over 6.5 years for custom products"）
- 2026-10-06｜President/COO Chris Koopmans｜customer：COO 列出與 NVIDIA 的策略協議（光學、NVLink Fusion 等）。（原話："we announced a strategic agreement with NVIDIA"）
- 2026-10-06｜President/COO Chris Koopmans｜customer：前四大美國超大規模客戶占去年資料中心 CapEx 過半。（原話："the top 4 U.S. hyperscalers alone were more than half"）
- 2026-10-06｜CEO Matt Murphy｜customer：Murphy 稱預測成長高度集中於四大客戶，但產品面分散。（原話："highly leveraged to the Big 4, but very diversified"）
- 2026-10-06｜CEO Matt Murphy｜customer：Murphy 稱客製化專案皆為 Marvell 獨家（sole source）。（原話："are all proprietary sole source"）
- 2026-10-06｜CEO Matt Murphy｜customer：Murphy 稱 AI 實驗室屬於模型之外的潛在上行選項，未納入目標。（原話："I think it's a real call option"）
- 2026-10-06｜SVP Xi Wang｜competition：Xi Wang 稱沒有其他公司涵蓋整條連接堆疊。（原話："No other companies cover this entire stack."）
- 2026-10-06｜SVP Xi Wang｜competition：Xi Wang 稱 1.6T DSP 領先競爭對手約兩年。（原話："leading our competitors by 2 years and continuing"）
- 2026-10-06｜EVP David Lazovsky｜competition：Lazovsky 稱 T100 交換器延遲與功耗優於任一領先競爭對手。（原話："on the order of 20% or more lower latency"）
- 2026-10-06｜President/COO Chris Koopmans｜competition：COO 劃清定位：不是單純 ASIC 供應商。（原話："We're not an ASIC vendor."）
- 2026-10-06｜CEO Matt Murphy｜competition：Murphy 以客製化 TAM 的演變說明市場超出當年辯論的預期（2024 年為 400 億美元 XPU 客製化 TAM）。（原話："we called out a $40 billion XPU custom TAM"）
- 2026-10-06｜CEO Matt Murphy｜competition：Murphy 以 300 億美元對 2,350 億美元客製化 TAM 推算約 13% 占比，稱並非不合理。（原話："You get 13% share, okay?"）
- 2026-10-06｜CEO Matt Murphy｜product：TAM 總量：2030 曆年約 4,000 億美元可定址市場。（原話："approximately $400 billion total addressable market"）
- 2026-10-06｜CEO Matt Murphy｜product：TAM 與前次相比放大約四倍。（原話："So this is a 4x increase to our TAM opportunity"）
- 2026-10-06｜CEO Matt Murphy｜product：TAM 的 CapEx 前提：2030 年資料中心 CapEx 約 3 兆美元。（原話："total data center CapEx to reach roughly $3 trillion"）
- 2026-10-06｜CEO Matt Murphy｜product：XPU attach 的可定址市場一年前約 150 億美元，現在已放大數倍。（原話："We said it was about $15 billion a year ago."）
- 2026-10-06｜CEO Matt Murphy｜product：FY28 資料中心 180 億美元目標比原訂 FY29 提早近一年達成。（原話："the $18 billion data center target we set for FY '29"）
- 2026-10-06｜CEO Matt Murphy｜product：scale-up 光學目前幾乎沒有營收，明年開始放量。（原話："multi-hundred million starting next year"）
- 2026-10-06｜CEO Matt Murphy｜product：scale-out 業務近年大致每年翻倍，模型假設成長率會趨緩。（原話："that business has been roughly doubling each year"）
- 2026-10-06｜EVP David Lazovsky｜product：Teralynx T100 為單晶 102.4T 交換器，主打 scale-out 與 scale-up 雙用。（原話："the first and only monolithic full reticle-limited die"）
- 2026-10-06｜EVP David Lazovsky｜product：預期 100T 交換器本身可新增數十億美元年營收。（原話："multiple billions of dollars of annual revenue"）
- 2026-10-06｜EVP David Lazovsky｜product：UALink U115 交換器預計明年推出，已有一家超大規模客戶部署。（原話："we'll be releasing next year, a UALink U115 switch"）
- 2026-10-06｜EVP David Lazovsky｜product：每顆 XPU 的 scale-up 光學內容約為數千美元。（原話："thousands of dollars of scale-up optics per XPU"）
- 2026-10-06｜EVP David Lazovsky｜product：Photonic Fabric 記憶體模組已完成 tape-out，明年向多家客戶送樣。（原話："we'll be sampling with multiple customers"）
- 2026-10-06｜SVP Xi Wang｜product：3.2T 路線轉向 coherent-lite：管理層稱 PAM4 在 400G/lane 有物理極限。（原話："3-nanometer alone wasn't the optimal answer"）
- 2026-10-06｜SVP Xi Wang｜product：類比（TIA／driver）業務年營收正朝 10 億美元以上邁進。（原話："rapidly headed towards $1 billion plus annually"）
- 2026-10-06｜SVP Xi Wang｜product：scale-in（光學進封裝）被稱為可能再成就數十億美元事業。（原話："yet another multibillion-dollar business for Marvell"）
- 2026-10-06｜CEO Matt Murphy｜product：Murphy 稱 scale-in 在 FY31 數字中並不重大，視為選擇權。（原話："not really material at that point in FY '31"）
- 2026-10-06｜CEO Matt Murphy｜product：Murphy 稱 scale-in 可能在目標期內起步，但屬未來投資人日的主題。（原話："which could start in the period"）
- 2026-10-06｜SVP Russ Esmacher｜product：相干可插拔模組的資料中心間需求預估到 FY31 超過 300 萬顆。（原話："grows to over 3 million units"）
- 2026-10-06｜EVP Will Chu｜product：XPU attach 新增兩個先前未談過的類別之一：AI 基礎設施管理矽。（原話："Today, we're introducing an entirely new XPU attach category"）
- 2026-10-06｜EVP Will Chu｜product：Chu 給 XPU attach 單價與機會量級：每類可達 10 億美元，部分達數十億。（原話："with some reaching several billions"）
- 2026-10-06｜EVP Will Chu｜product：Chu 以每 XPU 一至兩個 attach socket、ASP 約 1,000 美元作示範算式。（原話："sockets attaching to each XPU with ASPs around $1,000"）
- 2026-10-06｜EVP Will Chu｜product：Chu 稱 XPU attach 的 socket 黏性高、可跨多代 XPU。（原話："these sockets are very sticky"）
- 2026-10-06｜CEO Matt Murphy｜risk：Murphy 承認外部衝擊下公司同樣暴露。（原話："We're all exposed if the world turns upside down"）
- 2026-10-06｜CEO Matt Murphy｜risk：Murphy 稱此預測實質上是三年而非五年的押注。（原話："it is a 3-year kind of a pick, not a 5-year"）
- 2026-10-06｜CEO Matt Murphy｜risk：CapEx 假設：模型假設 CapEx 成長由目前的高速放緩，尾端約 20%。（原話："it's probably growing more like 20%"）
- 2026-10-06｜CEO Matt Murphy｜risk：對分析師詢問的供電與廠房（powered shell）限制，Murphy 稱客戶討論中未見此限制。（原話："we don't see that as any kind of constraint"）
- 2026-10-06｜CEO Matt Murphy｜risk：Murphy 稱 Google 大型策略協議在 FY31 中只計入部分 warrant 價值。（原話："that comprehends not the full value of the warrant"）
- 2026-10-06｜CEO Matt Murphy｜risk：Murphy 說明其預測哲學：取最可能結果，不偏保守也不偏積極。（原話："I'm not conservative, and I'm not aggressive. I'm pragmatic."）

### 問答異常語氣（迴避／改口／保留）
- MRVL_Q1_2027_Earnings_Call_20260527.md｜問：Arya：新 Tier 1 XPU 客戶何時揭露、是否獨家。｜答法：CEO 確認 10 億美元目標，但未回答客戶名稱與是否獨家，僅稱進度符合預期、隨年度推進信心增加。
- MRVL_Q1_2027_Earnings_Call_20260527.md｜問：Arcuri：是否進入運算 TAM、是否含於預測。｜答法：CEO 未直接回答是否進入運算 TAM，改述既有設計案，稱預測不需任何增量。
- MRVL_Q1_2027_Earnings_Call_20260527.md｜問：Wells Fargo：新增客製化插槽的 XPU 類型細節。｜答法：CEO 明確表示目前不提供額外細節，稱適當時機再做回顧。
- MRVL_Q1_2027_Earnings_Call_20260527.md｜問：Seymore：互連成長率 30%→50%→70% 逐步上調，為何 FY28 回落至略高於 CapEx，是否保守。｜答法：CEO 以「這是我們目前所在位置」帶過，未解釋減速原因，只稱有向上偏誤與選擇權。
- MRVL_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：Google 認股權協議的營收何時開始貢獻｜答法：CEO 先談歷史與 XPU attach 範疇，未給時點或金額，改指分析師日再說明
- MRVL_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：對同業與金融夥伴合資建資料中心的風險看法｜答法：CFO 表示不評論其他公司，回到技術領先與客戶成功；CEO 補充 Marvell 不參與
- MRVL_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：客戶對土地、電力、廠房（LPS）的疑慮｜答法：CEO 稱沒有太多新資訊，轉談限制反而健康
- MRVL_Analyst_Investor_Day_Marvell_Technology_Inc_20261006.md｜問：Vivek Arya 問客製化多重來源程度，以及 300 億美元目標與八月大型策略協議（warrant）規模的關係。｜答法：Murphy 回答 sole source 並說 FY31 模型只計入「部分」warrant 價值，未給出被納入的具體金額或比例。
- MRVL_Analyst_Investor_Day_Marvell_Technology_Inc_20261006.md｜問：Tom O'Malley 要求拆解 2030 年互連 TAM（DSP 占比、量、NPO／CPO）。｜答法：Murphy 只給定性分桶（scale-out、scale-across、scale-up、scale-in），並說「we're not going to give a lot more precision than that」，未給數字拆解。
- MRVL_Analyst_Investor_Day_Marvell_Technology_Inc_20261006.md｜問：Mark Lipacis 問客戶超額下單（double ordering）風險與本輪與過往超級週期的差異。｜答法：Murphy 未直接回應超額下單機制，改以「看得到明年 200 億」「實質是三年的押注」框架回答；CFO Durn 被點名後表示無補充。
- MRVL_Analyst_Investor_Day_Marvell_Technology_Inc_20261006.md｜問：Chris Rolland 問 scale-in 市場規模、客戶接觸現況與時程（傳聞最早曆年 2029）。｜答法：Murphy 表示有多家客戶接洽、正在投入研發，但稱「today is not the day」，未給規模或時程。

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
{"date":"20260831","verdict":"觀望","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"客製運算業務藉多客戶分散化抵銷單一旗艦社羣的執行風險——Google／Microsoft／新一線雲端商上線速度快於 AWS 旗艦社羣份額流失速度"},{"id":"H2","text":"互連端首發技術優勢持續轉化為超越資本支出的成長（1.6T PAM4、規模化光學 NPO/CPO、DCI）"},{"id":"H3","text":"AI 資料中心資本支出多年結構性不反轉，且 Marvell 毛利率結構在客製組合上升後仍能靠營運槓桿撐住 EPS"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AWS／Microsoft 旗艦 custom 社羣世代交接持續失利，且 Google/新客戶放量不如預期補位"},{"id":"R2","text":"非 GAAP 毛利率結構性跌破 57.5-58.5% 目標區間——除客製組合佔比上升外，記憶體（DRAM/HBM）成本通膨是本次新增查證的成本側變數：DRAM 價格 2025→2027 累計漲幅估計 ~275-300%，TrendForce（2026-06-02）預期 HBM 合約價 2027 年倍數級上漲且短缺延續至 2027 年後，Goldman 估 custom ASIC 用 HBM 需求 +82%；Google 協議本身涵蓋 memory interface controllers/near-memory compute，成本與客戶系統預算兩條路徑都通向毛利率"},{"id":"R3","text":"CPO（共同封裝光學）在規模化網路加速取代可插拔 DSP 模組，侵蝕互連端長期經濟性（Broadcom Tomahawk 6 已具第三代 CPO、NVIDIA 承諾於未來 Spectrum-X 導入）"},{"id":"R4","text":"AI 資本支出消化／融資結構風險（前份報告原有、本次恢復）：主流預估 hyperscaler capex 增速由 2026 年 +51% 降至 2027 年 +13%、2028 年約 +5%；增量負債占 capex 比重由 FY24 的 9% 升至 2026 年中 LTM 32%，五大雲端商自 2024 年底起舉債逾 $137.5B；另有折舊年限（會計 5-6 年 vs 估計經濟壽命 2-3 年）爭議，估計 2026-28 少認列約 $1,760 億，FASB 新揭露要求要到 FY2027 才上路——資訊最不透明期與折舊壓力最集中期重疊"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"三旗艦socket任一正面確認＋GM守57.5-58.5%","irr_base_pct":10.9,"ev5y_pct":64.6,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"衛星","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":4.3,"ev5y_pct":64.6,"irr_base_pct":10.9,"max_dd_pct":-48.0,"bull_5y_price":570.3,"bear_5y_price":134.1,"p_bull_pct":30.0,"p_bear_pct":30.0,"rearm_trigger":"三旗艦socket任一正面確認＋GM守57.5-58.5%","price_at_dd":216.62,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRVL_20261012/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
