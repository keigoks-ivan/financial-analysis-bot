你是 stock-analyst **v20 判斷 agent**，標的 AMD（20260923）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"AMD","date":"2026-09-23","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMD_20260923/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMD_20260923/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":11536,"period":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","citation":"公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results, https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results"},"note":"Street 共識約 $11.31B，實際 $11.536B（beat）（來源：web_search 彙整多家財經媒體引述 LSEG/Wall St. 共識，非公司原始揭露）"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":27,"period":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","citation":"公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results"},"note":"未查得明確 Street 共識營業利益率數字；EPS 端可比對：non-GAAP EPS $1.66 vs 共識 $1.62（beat，來源：web_search 多家財經媒體）"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":17,"period":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","citation":"公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results"},"note":"N/A（Street 通常僅追蹤 non-GAAP 口徑，未查得 GAAP 營業利益率共識）"},{"id":"f_kpi5_q3_fy2026_guidance","label":"管理層 Q3 FY2026 財測 guidance","value":"營收約 $13.0B ± $300M；non-GAAP 毛利率約 56%","period":"發布於 2026-08-04，指引對象為 Q3 FY2026","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"發布於 2026-08-04，指引對象為 Q3 FY2026","citation":"公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results"},"note":"公司指引中值 $13.0B 高於彼時 LSEG 共識 $12.52B（來源：web_search 財經媒體引述）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-04","period":"2026-08-04","unit":"date","basis":"距今 36 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_amd_gross_margin_pct","label":"AMD 毛利率","value":53.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amd_operating_margin_pct","label":"AMD 營業利益率","value":15.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amd_fcf_margin_pct","label":"AMD FCF 利潤率","value":20.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvda_gross_margin_pct","label":"NVDA 毛利率","value":74.67,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_operating_margin_pct","label":"NVDA 營業利益率","value":65.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_fcf_margin_pct","label":"NVDA FCF 利潤率","value":41.92,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_gross_margin_pct","label":"MRVL 毛利率","value":52.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_operating_margin_pct","label":"MRVL 營業利益率","value":16.81,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_fcf_margin_pct","label":"MRVL FCF 利潤率","value":18.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_3661_tw_gross_margin_pct","label":"3661.TW 毛利率","value":37.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3661_tw_operating_margin_pct","label":"3661.TW 營業利益率","value":24.0,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3661_tw_fcf_margin_pct","label":"3661.TW FCF 利潤率","value":-10.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":1558,"period":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","citation":"公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results"},"note":"未查得 Street FCF 共識數字"},{"id":"f_kpi4_sbc","label":"SBC 占營收 %","value":4.36,"period":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）","citation":"公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results"},"note":"N/A（無此項共識追蹤）"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":623.77,"period":"2026-09-22（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-09-22（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":203.69,"period":"2026-09-22（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-09-22（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":72.96,"period":"2026-09-22（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-09-22（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.58 → 7.58）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（15.57 → 15.57）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（22.27 → 22.27）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":7.58,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":15.57,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":22.27,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":2.85,"period":"2026-06-23 → 2026-09-19","unit":"%","basis":"FY1 共識 EPS 7.37 → 7.58（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":156.33,"period":"2026-09-22（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝43.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-09-22（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":43.3,"period":"2026-09-22（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-09-22（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":24.65,"period":"2026-09-22（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-09-22（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-09-22（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-09-22（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":24.44,"period":"2026-09-22（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-09-22（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-09-22（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-09-22（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":82.29,"period":"2026-09-19","unit":"x","basis":"分母＝FY1 EPS 7.58，分子＝快照價 623.77","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-19"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"✅","period":"2026-09-23","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-23","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 623.77 / W52 339.87 / W104 235.31 / W250 165.31 / W250 13週斜率 3.99%"},{"id":"f_ma_w52","label":"52 週均線","value":339.87,"period":"2026-09-23","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-23","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":235.31,"period":"2026-09-23","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-23","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":165.31,"period":"2026-09-23","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-23","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":3.99,"period":"2026-09-23","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-23","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMD reached a record 34.1% x86 CPU market share in Q2 2026 (Mercury Research data), up 4.7 percentage points YoY, with Intel losing share across every major client/server segment.","source":"digitalcitizen.life, \"AMD Reaches Record 34.1 Percent x86 CPU Share as Intel Loses Ground Across Every Major Segment\"","as_of":"2026-06-30","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMD's desktop x86 CPU unit share climbed to 34.9% in Q2 2026, up 1.8 percentage points quarter-over-quarter.","source":"The Register, \"AMD grabs more CPU share while pricier PCs punish desktop demand\"","as_of":"2026-08-21","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMD's server CPU revenue share hit a record 46.2% in Q1 2026 while shipping roughly one-third of x86 server units; Intel still shipped ~66.8% of units but its revenue share fell to ~53.8%, reflecting AMD's higher-ASP premium EPYC configs.","source":"wccftech, \"AMD's EPYC Steamrolls the Server Market With Record 46.2% Revenue Share\"; TechPowerUp, \"Intel's Server Share Slips to 67%\"","as_of":"2026-03-31","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMD's EPYC CPUs were reported sold out in 2026, with delivery lead times stretching more than 30 weeks due to hyperscaler demand.","source":"io-fund, \"AMD, Nvidia, Arm, Intel: Inside the $120 Billion CPU Gold Rush\"","as_of":"2026-01-01","affects":["moat_trend","triggers"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"In AI accelerators, AMD's share has grown from under 1% to an estimated 5-7% (~$7-8B Instinct revenue), but Nvidia still holds roughly 80% of AI accelerator revenue share, meaning the absolute gap is widening even as AMD's relative share grows.","source":"siliconanalysts.com, \"AMD vs NVIDIA AI GPU Market Share 2026: MI350X vs B200 Competitive Analysis\"","as_of":"2026-06-30","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Custom ASIC silicon from hyperscalers (Broadcom AI ASIC revenue $20B+ in FY2025, Google TPU, AWS Trainium) is characterized as a larger and faster-growing competitive threat to Nvidia's AI accelerator dominance than AMD is, positioning custom silicon rather than AMD as the more significant new-entrant pressure in AI accelerators.","source":"SemiAnalysis, \"Can AMD break the CUDA Moat? AMD Advancing AI 2026\" (cited via siliconanalysts.com search summary)","as_of":"2026-01-01","affects":["thesis.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#6","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMD Instinct MI300X/MI350 accelerators have secured adoption from Microsoft Azure, Meta, Dell Technologies, HPE and Lenovo, including use by Microsoft Azure for Azure OpenAI services; MI350 began shipping to partners and hyperscale data centers in Q3 2025.","source":"AMD FY2025 Annual Report to Shareholders (Form ARS), SEC EDGAR filing","as_of":"2025-12-27","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#7","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMD confirmed the Instinct MI400 series for 2026 with 432GB HBM4 memory, doubling MI355's throughput (40 PFLOPS FP4 / 20 PFLOPS FP8 vs 20/10), as part of AMD's plan to release a new data center GPU every year.","source":"VideoCardz, \"AMD launches Instinct MI350 series, confirms MI400 in 2026 with 432GB HBM4 memory\"","as_of":"2025-06-12","affects":["moat_trend","thesis.H","triggers"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Meta（AMD 6GW Instinct GPU 合約的客戶）在簽下輝達與 AMD 大單數週後，宣布擴大自研 AI 晶片 MTIA（in-house）部署","source":"CNBC, \"Meta rolls out in-house AI chips weeks after massive Nvidia, AMD deals\", https://www.cnbc.com/2026/03/11/meta-ai-mtia-chip-data-center.html","as_of":"2026-03-11","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Broadcom 被證實是 Google TPU、Meta MTIA、Microsoft Maia，以及 2026 年初起 OpenAI／Anthropic Titan 自研 AI 晶片專案的設計夥伴——顯示 AMD 多個大型 AI 客戶同時在推進自製晶片路線","source":"Tom's Hardware, \"The custom AI ASIC state of play (May 2026)\", https://www.tomshardware.com/tech-industry/semiconductors/custom-ai-asics-examined-from-broadcom-to-mtia","as_of":"2026-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Microsoft 自研 AI 晶片 Maia 200 於 2026 年 1 月開始部署（台積電 3nm 製程），號稱比現有機隊每美元效能高 30%——微軟同時也是 AMD Instinct 的客戶之一","source":"Windows News, \"AI Compute Crunch: How Meta and Microsoft's Chip Deals Shape the 2026 Race\", https://windowsnews.ai/article/ai-compute-crunch-how-meta-and-microsofts-chip-deals-shape-the-2026-race.411832","as_of":"2026-01","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"AMD 10-K (FY2025, filed 2026-02-04) discloses no single customer accounted for 10% or more of consolidated net revenue in fiscal 2025 or fiscal 2024, an improvement from FY2023 when one customer accounted for 18% of consolidated net revenue.","source":"AMD Form 10-K for fiscal year ended 2025-12-27, SEC EDGAR (amd-20251227.htm)","as_of":"2026-02-04","affects":["moat_trend","decision_inputs.bear","triggers"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"AMD's forward customer base is concentrating around a small number of AI hyperscalers: AMD and Meta signed a 5-year, up-to-$60B, 6GW Instinct GPU supply agreement (with AMD issuing Meta a performance-based warrant for 160M shares), and combined with the OpenAI 6GW agreement AMD has ~12GW of committed deployments; these agreements are multi-year and milestone-based, meaning most of the associated revenue is not yet contracted, shipped, or paid.","source":"CNBC / Tom's Hardware / AMD IR press release on AMD-Meta strategic partnership","as_of":"2026-02-24","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"OpenAI, a counterparty to AMD's Instinct GPU supply agreement, reported a Q1 2026 net loss of $21.3B, carries roughly $665B in long-term compute purchase commitments not reflected as balance-sheet debt, and faces a projected financing gap of about $130B over the next two years.","source":"TradingKey / IFR (International Financing Review) reporting on OpenAI Q1 2026 financials","as_of":"2026-05","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Despite tripling its debt load in a single month (including $26B in debt financing from Blue Owl/PIMCO for a Louisiana AI data center), Moody's (2026-07-24) said Meta still retains one of the strongest corporate balance sheets and its investment-grade rating is not under imminent threat, even as Moody's flagged 'unprecedented' AI spending as a broader credit-quality risk across hyperscalers.","source":"CNBC, citing Moody's commentary","as_of":"2026-07-24","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#4","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"S&P Global downgraded Oracle's credit rating from BBB to BBB- (one notch above junk), explicitly naming OpenAI as a 'key credit risk' for Oracle due to Oracle's large compute-supply exposure to OpenAI — illustrating rating-agency concern about OpenAI's counterparty credit quality that is also relevant to AMD's own OpenAI compute agreement.","source":"the-decoder.com / TradingKey reporting on S&P Global Oracle downgrade","as_of":"2026","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"記憶體晶片（DRAM/NAND，含 HBM 上游）短缺預期持續到 2027 年，SK海力士高層警告短缺可能延續到 2030 年之後，因 AI 資料中心需求排擠傳統記憶體供給","source":"CNBC, \"Memory chip shortage to last through 2027, semiconductor boss says\", https://www.cnbc.com/2026/01/26/memory-chip-shortage-synopsys-lenovo-ai-data-centers.html","as_of":"2026-01-26","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Gartner 預測 2026 年全球半導體營收將突破 1.3 兆美元，反映 AI 相關晶片需求持續強勁","source":"Gartner 新聞稿, \"Gartner Forecasts Worldwide Semiconductor Revenue to Exceed $1.3 Trillion in 2026\", https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026","as_of":"2026-04-08","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"NVIDIA 執行長黃仁勳在 GTC 大會上將公司 AI 晶片訂單預測倍增至 1 兆美元、預計 2027 年達成，理由是產業正進入由推論（inference）工作負載主導的新階段","source":"MLQ News, \"NVIDIA Doubles Its AI Chip Order Forecast to $1 Trillion by 2027, Citing Inference Demand Surge\", https://mlq.ai/news/nvidia-doubles-its-ai-chip-order-forecast-to-1-trillion-by-2027-citing-inference-demand-surge/","as_of":"2026-03-17","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"AMD 在 AI 加速器市場的營收份額約 5-7%（NVIDIA 約 80%），但 AMD Instinct GPU 系列 2025 會計年度營收估計 $6-8B，較 2024 年最初約 $2B 的原始指引歷經四次上修至『超過 $5B』的實際成果","source":"Silicon Analysts, \"AMD vs NVIDIA AI GPU Market Share 2026: MI350X vs B200 Competitive Analysis\", https://siliconanalysts.com/analysis/amd-vs-nvidia-ai-gpu-market-share-2026","as_of":"2026-04-13","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"美國商務部工業與安全局(BIS)於2026年1月13日發布最終規則、1月15日生效，將輝達H200與AMD MI325X等同等級先進AI晶片對中國(含澳門)出口的審查標準，從『推定拒絕』改為『逐案審查』；出口商須證明輸往中國/澳門的總處理效能(TPP)低於輸美客戶總量的50%。","source":"Mayer Brown, 'Administration Policies on Advanced AI Chips Codified' (引述BIS最終規則) https://www.mayerbrown.com/en/insights/publications/2026/01/administration-policies-on-advanced-ai-chips-codified","as_of":"2026-01-15","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"美國總統於2026年1月14日簽署行政公告，對輸往中國、非用於美國供應鏈之先進AI晶片(含AMD MI325X等級產品)課徵25%從價關稅，作為前述放行規則的配套限制。","source":"Mayer Brown, 'Administration Policies on Advanced AI Chips Codified' https://www.mayerbrown.com/en/insights/publications/2026/01/administration-policies-on-advanced-ai-chips-codified","as_of":"2026-01-14","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"President Trump's Proclamation 11002 imposed a 25% Section 232 tariff on advanced semiconductors and derivative products effective January 15, 2026; AMD's Instinct MI325X is specifically named in the annex. Exemptions apply to products supporting US data centers, R&D, startups, repairs, and non-data-center consumer/industrial uses.","source":"President Trump Announces Section 232 Tariffs on Semiconductors and their Derivative Products, International Trade & Supply Chain Insights (internationaltradeinsights.com/2026/01/president-trump-announces-section-232-tariffs-on-semiconductors-and-their-derivative-products/)","as_of":"2026-01-15","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"BIS published a final rule on January 15, 2026 shifting export license review policy for NVIDIA H200 and AMD MI325X exports to China/Macau from 'presumption of denial' to 'case-by-case review', subject to a 25% tariff on those exports, a 50% volume cap, third-party testing, and KYC requirements.","source":"Revision to License Review Policy for Advanced Computing Commodities, Federal Register (federalregister.gov/documents/2026/01/15/2026-00789); BIS press release (bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china)","as_of":"2026-01-15","affects":["thesis.H","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"AMD CEO Lisa Su stated China represents roughly 20% of AMD's total revenue, and characterized China as a 'very important market' despite ongoing US export restrictions on advanced AI GPUs.","source":"AMD CEO Lisa Su says China still accounts for about 20% of revenue despite GPU export controls, cryptobriefing.com (cryptobriefing.com/amd-china-revenue-export-restrictions/)","as_of":"2026-05-22","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"AMD planned to ship an additional $100 million of MI308 chips to China in the quarter ending March 2026, but was not counting on further China AI-chip revenue beyond that due to market/regulatory uncertainty.","source":"AMD 1Q Sales to Slip Despite $100M MI308 China Boost, Next-Gen AI Chips Set for 2H Ramp, TrendForce (trendforce.com/news/2026/02/04/news-amd-1q-sales-to-slip-despite-100m-mi308-china-boost-next-gen-ai-chips-set-for-2h-ramp/)","as_of":"2026-02-04","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"TSMC controls roughly 90% of the world's most advanced-node chip production (3nm/5nm) and is AMD's main foundry for leading-edge chiplet processors; this production is concentrated in Taiwan, ~100 miles from mainland China.","source":"Mapshock, \"TSMC Taiwan Geopolitical Risk: Concentration and Resilience Planning\" (mapshock.com); FourWeekMBA, \"AMD and TSMC: What a Reported Foundry Cost Rise Reveals About the Fabless Supply Layer\"","as_of":"2026-01-01","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"On 2026-01-14, the US administration signed a proclamation imposing a 25% duty/revenue-share on advanced computing chips (e.g. H200, MI325X) shipped to China, with mandatory third-party testing and a volume cap; AMD CEO Lisa Su stated China still accounts for about 20% of AMD's revenue despite export controls.","source":"Introl Blog, \"BIS Export Policy Shift\" (introl.com/blog/bis-export-policy-h200-mi325x-china-case-by-case-2026); Cryptobriefing, \"AMD CEO Lisa Su says China still accounts for about 20% of revenue despite GPU export controls\"","as_of":"2026-01-14","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"AMD had previously forecast about $1.5 billion in 2025 revenue loss and taken an $800 million charge tied to halted AI-chip shipments to China (inventory write-downs, cancelled purchases) due to tightened US export restrictions.","source":"Astute Group, \"AMD Flags $1.5 Billion Revenue Blow from Tightened Export Curbs\"; Motley Fool, \"AMD Stock Declines as Earnings Drop 30% on Government Restricting Advanced AI Chip Sales to China\"","as_of":"2025-08-06","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"TSMC's second Arizona fab (Fab 21 Phase 2, 3nm) is reportedly targeting 2H27 mass production, with all four announced US fabs said to be fully booked; AMD is among the AI chip designers allocated capacity at TSMC's advanced nodes including its overseas (non-Taiwan) fabs, offering AMD partial future geographic diversification, though no advanced-node output outside Taiwan is yet in volume production for AMD's chiplets.","source":"TrendForce, \"TSMC Reportedly Eyes 2H27 3nm Mass Production at Arizona Fab 2; Four U.S. Fabs Said to Be Fully Booked\" (trendforce.com/news/2026/03/24)","as_of":"2026-03-24","affects":["thesis.R","triggers"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Data Center segment revenue $6.7B in Q2 2026, up 107% YoY, driven by EPYC CPU and Instinct GPU sales","source":"AMD Q2 2026 press release (ir.amd.com); CNBC https://www.cnbc.com/2026/08/04/amd-earnings-report-q2-2026.html","as_of":"2026-08-04","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"AMD guided Q3 2026 data center + embedded revenue to grow double-digit sequentially, and server CPU revenue to grow >80% YoY in H2 2026","source":"AMD Q2 2026 earnings slides via Investing.com https://www.investing.com/news/company-news/amd-q2-2026-slides-data-center-revenue-doubles-ai-partnerships-expand-93CH-4836256","as_of":"2026-08-04","affects":["thesis.H","triggers"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"AMD stated data center segment revenue should more than double in 2027, supported by ramp of Helios (MI400-series) platform","source":"AMD Q2 2026 earnings call/slides via Investing.com https://www.investing.com/news/company-news/amd-q2-2026-slides-data-center-revenue-doubles-ai-partnerships-expand-93CH-4836256","as_of":"2026-08-04","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"AMD data center revenue reached $5.8B in Q1 2026; company reiterated a long-term target of $120B server CPU-related revenue by 2030","source":"DataCenterDynamics https://www.datacenterdynamics.com/en/news/amd-posts-q1-2026-data-center-revenue-of-58bn-forecasts-120bn-server-cpu-income-by-2030/","as_of":"2026-05-05","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"AMD reached record 46.2% server x86 CPU revenue share in Q1 2026 (unit share ~30% of entire x86 CPU market)","source":"Wccftech https://wccftech.com/amd-posts-record-server-cpu-revenue-in-q1-2026-red-team-commands-30-percent-market/; Tom's Hardware https://www.tomshardware.com/pc-components/cpus/amd-reaches-46-percent-of-server-x86-cpu-revenue-intel-still-controls-70-percent-of-the-consumer-pc-market-share","as_of":"2026-05-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"NVIDIA holds an estimated 70-75% of data-center AI accelerator market revenue vs. AMD's estimated 6-8%; hyperscaler custom silicon collectively ~15-20%","source":"Silicon Analysts https://siliconanalysts.com/analysis/nvidia-ai-accelerator-market-share-2024-2026","as_of":"2026-08-01","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"AMD Instinct GPU line generated an estimated $7-8B in 2025 (~5-7% of AI accelerator revenue); MI400 series (CDNA5, 2nm, 432GB HBM4) launched July 2026 as first-to-market 2nm AI accelerator","source":"Silicon Analysts https://siliconanalysts.com/analysis/amd-vs-nvidia-ai-gpu-market-share-2026","as_of":"2026-07-01","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"+","claim":"Third-party analyst scenario projects AMD AI accelerator share could reach 15-20% by 2027 (vs. NVIDIA 75-80%), citing OpenAI 6GW compute commitment and Meta multi-year deals as catalysts; this is a market-analyst projection, not AMD guidance","source":"Silicon Analysts https://siliconanalysts.com/analysis/amd-vs-nvidia-ai-gpu-market-share-2026","as_of":"2026-08-01","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#8","axis":"end_markets","section":"coverage","direction":"+","claim":"AI data center GPU market projected to grow from $11.12B (2025) to $32.3B by 2030, a 23.8% CAGR","source":"GlobeNewswire market report https://www.globenewswire.com/news-release/2026/04/14/3273676/0/en/AI-Data-Center-Graphics-Processing-Units-GPUs-Market-Report-2026-32-3-Bn-Opportunities-Trends-Competitive-Landscape-Strategies-and-Forecasts-2020-2025-2025-2030F-2035F.html","as_of":"2026-04-14","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#9","axis":"end_markets","section":"coverage","direction":"+","claim":"Client segment (PC CPU) unit market share reached 30.3% in Q2 2026 (first time above 30%), up from 29.6% in Q1 2026 and 24.1% a year earlier; Intel share fell to 69.7%","source":"XenoSpectrum https://xenospectrum.com/en/amd-x86-client-share-q2-2026/; pbxscience https://pbxscience.com/amds-x86-client-processor-share-tops-30-for-the-first-time-as-intels-lead-keeps-shrinking/","as_of":"2026-08-04","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#10","axis":"end_markets","section":"coverage","direction":"+","claim":"Client segment revenue was $3.1B in Q2 2026, up 23% YoY (from $2.5B); Q1 2026 client revenue was $2.9B, up 26% YoY, driven by Ryzen demand and share gains","source":"AMD Q1/Q2 2026 press releases (ir.amd.com)","as_of":"2026-08-04","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#11","axis":"end_markets","section":"coverage","direction":"-","claim":"Gaming segment revenue was $779M in Q2 2026, down 31% YoY, primarily due to lower semi-custom (console) revenue and higher component costs weighing on GPU demand at this late stage of the console cycle; AMD guided H2 2026 gaming revenue to be >20% lower than H1 2026","source":"Tom's Hardware https://www.tomshardware.com/tech-industry/amd-doubles-data-center-revenue-year-over-year-but-gaming-revenue-plunged-by-31-percent-ceo-lisa-su-says-prices-have-weighed-on-consumer-demand-but-is-optimistic-about-client-market","as_of":"2026-08-04","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#12","axis":"end_markets","section":"coverage","direction":"0","claim":"Gaming revenue was $720M in Q1 2026, up 11% YoY on higher Radeon GPU demand, partially offset by lower semi-custom revenue; customer demand for next-gen console platforms described as encouraging even as current-gen console sales decline late in the cycle","source":"TweakTown https://www.tweaktown.com/news/111459/amd-gaming-revenue-increased-in-q1-2026-thanks-to-solid-demand-for-radeon-gpus/index.html","as_of":"2026-05-05","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#13","axis":"end_markets","section":"coverage","direction":"+","claim":"Embedded segment revenue was $977M in Q2 2026, up 19% YoY (strongest embedded growth in 3+ years), with operating margin at 40% (up from 33% a year earlier); segment tracking toward a record year with over $18B in new design wins, following a prolonged industrial inventory correction","source":"AMD Q2 2026 press release (ir.amd.com)","as_of":"2026-08-04","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#14","axis":"end_markets","section":"coverage","direction":"+","claim":"Embedded segment revenue was $873M in Q1 2026, up 6% YoY, as industrial and edge demand began improving","source":"AMD Q1 2026 press release https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results","as_of":"2026-05-05","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"AMD 2026 SWOT 分析指出，AMD 部分大客戶正自行開發內部處理器與加速器（客製化晶片/ASIC），可能壓縮 AMD 的可觸及市場（addressable market）。","source":"AMD SWOT Analysis 2026 - The Strategy Story (https://thestrategystory.com/blog/amd-swot-analysis-2026/)","as_of":"2026-09-21","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"AMD 於 2026-08-10 收購 AI 加速新創 Taalas（由 Tenstorrent 共同創辦人 Ljubisa Bajic 創立）。Taalas 技術將模型「硬編碼」進晶片（predefined logic tiles + mask-programmed ROM），宣稱推論階段 token 速率達最接近競品的 8 倍、耗電更低，屬於犧牲彈性換取速度的專用硬體路線，被視為對通用型 GPU（如 AMD 自家 MI455X）的替代/互補技術，AMD 藉收購提前佈局以防被此類專用晶片路線邊緣化。","source":"xpu.pub, \"Taalas Technology to Boost AMD AI Performance and Efficiency\" (https://xpu.pub/2026/08/10/amd-taalas-ai-acceleration/)","as_of":"2026-08-10","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"55 analysts polled by S&P Global give AMD a 'Strong Buy' consensus rating with an average price target of $616.51","source":"S&P Global consensus data cited via ts2.tech, 'AMD Stock Jumps 8.8% to a Record as Consensus Upside Shrinks to 1%'","as_of":"2026-09-21","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat's consensus price target for AMD stands at $565.13, characterized as a 'Moderate Buy' rating — lower than the S&P Global figure, showing dispersion across target-price aggregators","source":"MarketBeat, 'Advanced Micro Devices (AMD) Stock Forecast and Price Target 2026'","as_of":"2026-09-19","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"AMD guided Q3 2026 revenue to $13.0B ± $300M (≈41% YoY growth), above the $12.52B LSEG analyst consensus estimate, but kept non-GAAP gross margin guidance flat at ~56%; stock fell despite the beat-and-raise because investors focused on the flat-margin guidance after a 20.7% run-up in the prior four sessions","source":"TradingKey, 'AMD Beat on Revenue, Profit, and Guidance — So Why Did the Stock Drop 7%?'","as_of":"2026-08-05","affects":["thesis.H","thesis.R","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Some sell-side analysts have raised their 2026 revenue estimates for AMD by $2B and gross profit estimates by $1.5B, putting both materially above both Wall Street consensus and AMD's own official guidance — a divergence between the most bullish analyst models and management's stated outlook","source":"Simply Wall St, 'Advanced Micro Devices (NasdaqGS:AMD) Stock Forecast & Analyst Predictions'","as_of":"2026-09-10","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"In the trailing 30 days, sell-side analysts made 33 upward FY2027 EPS revisions against only 3 downward revisions, and consensus fair value/price target estimates rose (e.g., one model's fair value from $213.89 to $225.00, consensus price target from $291 to $312 in an earlier framework), reflecting broad-based upward revision momentum tied to AI/data-center demand and recent large GPU deals (Meta, OpenAI)","source":"Simply Wall St, 'Advanced Micro Devices (NasdaqGS:AMD) Stock Forecast & Analyst Predictions'","as_of":"2026-09-10","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"+","claim":"AMD 於 2025-03-31 完成收購 ZT Systems（AI/通用運算基礎設施供應商），強化端到端 AI 機架系統能力；其製造業務隨後於 2025-10 出售給 Sanmina。","source":"AMD Newsroom - AMD Completes Acquisition of ZT Systems (https://www.amd.com/en/newsroom/press-releases/2025-3-31-amd-completes-acquisition-of-zt-systems.html)","as_of":"2025-03-31","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"AMD 於 2025 年收購 MK1，強化 AI 推論效能與效率。","source":"AMD Blog - AMD Acquires MK1 to Advance AI Inference Performance and Efficiency (https://www.amd.com/en/blogs/2025/amd-acquires-mk1-to-advance-ai-inference-performance.html)","as_of":"2025-01-01","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"AMD 於 2026-07 完成收購 FastFlowLM，專攻 NPU 上大型語言模型推論運行時軟體優化。","source":"Tracxn - List of 18 Acquisitions by AMD (https://tracxn.com/d/acquisitions/acquisitions-by-amd/__fwyiOptL3Stsxv1-fiN0X0QBNAymC3ylFvabx6tLFRk)","as_of":"2026-07-01","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"查無 AMD 近 12 個月遭 SEC 調查或重大財報重編；2026-02-04 提交之 10-K 與 2026 年各季 10-Q 均未勾選涉及錯誤更正/重編需追回高管薪酬之欄位，僅見一項屬 ASP/單位揭露的非重大文字校正。","source":"AMD 10-K SEC filing, 2026-02-04 (https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000018/amd-20251227.htm)","as_of":"2026-02-04","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"+","claim":"AMD 於 2025-03-31 完成收購 ZT Systems（AI/通用運算基礎設施供應商）。","source":"AMD Newsroom - AMD Completes Acquisition of ZT Systems (https://www.amd.com/en/newsroom/press-releases/2025-3-31-amd-completes-acquisition-of-zt-systems.html)","as_of":"2025-03-31","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"+","claim":"AMD 於 2025 年收購 AI 推論新創 MK1。","source":"AMD Blog - AMD Acquires MK1 (https://www.amd.com/en/blogs/2025/amd-acquires-mk1-to-advance-ai-inference-performance.html)","as_of":"2025-01-01","affects":["moat_trend"],"status":"ok"},{"id":"ma_merger#2","axis":"ma_merger","section":"events","direction":"+","claim":"AMD 於 2026-07 完成收購 FastFlowLM（NPU LLM 推論運行時軟體）。","source":"Tracxn - Acquisitions by AMD (https://tracxn.com/d/acquisitions/acquisitions-by-amd/__fwyiOptL3Stsxv1-fiN0X0QBNAymC3ylFvabx6tLFRk)","as_of":"2026-07-01","affects":["moat_trend"],"status":"ok"},{"id":"ma_merger#3","axis":"ma_merger","section":"events","direction":"0","claim":"AMD 於 2025-10 將 ZT Systems 之製造業務出售予 Sanmina。","source":"Sanmina IR - Sanmina Announces Acquisition of Data Center Infrastructure Manufacturing Business of ZT Systems from AMD (https://ir.sanmina.com/news/news-details/2025/SANMINA-ANNOUNCES-ACQUISITION-OF-DATA-CENTER-INFRASTRUCTURE-MANUFACTURING-BUSINESS-OF-ZT-SYSTEMS-FROM-AMD/default.aspx)","as_of":"2025-10-01","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"AMD 2026-02-04 提交之 10-K（FY2025）及後續 2026 年各季 10-Q 均未勾選涉及錯誤更正/財報重編需追回高管薪酬之欄位；僅揭露一項屬 MD&A 中 ASP／出貨量年增率呈現方式之非重大文字校正，非重大財報重編。","source":"AMD 10-K SEC filing, 2026-02-04 (https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000018/amd-20251227.htm)","as_of":"2026-02-04","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"AMD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":53.2,"operating_margin_pct":15.71,"fcf_margin_pct":20.34,"rd_intensity_pct":22.74},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"NVDA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.67,"operating_margin_pct":65.21,"fcf_margin_pct":41.92,"rd_intensity_pct":7.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"MRVL","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":52.21,"operating_margin_pct":16.81,"fcf_margin_pct":18.23,"rd_intensity_pct":25.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"3661.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.2,"operating_margin_pct":24.0,"fcf_margin_pct":-10.46,"rd_intensity_pct":9.17},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"AMD"}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/AMD/AMD_Q2_2026_Earnings_Call_20260804.md）

# Q2 2026 Earnings Call
2026-08-04

Q2 2026 Earnings Call
Advanced Micro Devices, Inc. | Earnings Calls | 2026-08-04
Operator (Operator)
Greetings, and welcome to the AMD Second Quarter 2026 Conference Call. [Operator Instructions]
And please note that this conference is being recorded.
I will now turn the conference over to Matt Ramsey, VP, Financial Strategy and IR. Thank you, Matt.
You may begin.
Matthew Ramsay (Executives)
Thank you, and welcome to AMD's Second Quarter 2026 Financial Results Conference Call. By now,
you should have had the opportunity to review a copy of our earnings press release and the
accompanying slides. If you have not had the chance to review these materials, they can be found on the
Investor Relations page of amd.com. Today, we will refer primarily to non-GAAP financial measures
during the call. The full non-GAAP to GAAP reconciliations are available in today's press release and
slides posted on our website.
As a reminder, our second quarter 2025 results included approximately $800 million of inventory and
related charges associated with U.S. export control restrictions on MI308 shipments to China. Unless
otherwise noted, comments making year-over-year comparisons exclude the impact of those charges to
provide a more comparable and meaningful view of our underlying business performance. Participants
on today's conference call are Dr. Lisa Su, our Chair and CEO and Jean Hu, our Executive Vice
President, CFO and Treasurer. This is a live call and will be replayed via webcast on our website.
Before we begin, I would like to note that AMD will participate in the following events for the financial
community. KeyBanc's Technology Leadership Forum on Tuesday, August 11; Citi's 2026 Global TMT
Conference on Tuesday, September 8; and the Goldman Sachs Communacopia and Technology
Conference on Friday, September 11. Today's discussions contain forward-looking statements based on
the current beliefs, assumptions, expectations including forward-looking statements regarding
financial projections, business and industry trends that speak only as of today and as such, involve risks
and uncertainties that could cause actual results to differ materially from our current expectations.
Please refer to the cautionary statement in our press release for more information on these factors that
could cause actual results to differ materially.
With that, I will hand the call over to Lisa.
Lisa Su (Executives)
Thank you, Matt, and good afternoon to all those listening today. We delivered another outstanding
quarter with record revenue and profitability as adoption of our leadership products continued to
expand. Revenue increased 50% year-over-year to $11.5 billion, driven by significantly higher sales of
EPYC, Instinct, Ryzen and embedded processors. Data center revenue more than doubled year-over-
year and now represents 58% of total revenue, up from 42% a year ago, reflecting the rapidly expanding
scale of our server and data center AI businesses.

Our record results mark another clear step up in AMD's financial performance and demonstrates the
strength of our product portfolio and execution. We are still in the early stages of a multiyear AI
adoption cycle as deployments grow across a broad set of markets and workloads, driving demand for
more compute and creating a clear path to significant revenue growth and earnings power in the years
ahead.
Turning to our segments. Data center revenue grew 107% year-over-year to a record $6.7 billion, driven
by strong demand for EPYC processors and Instinct accelerators. In server, we delivered our fifth
consecutive quarter of record server CPU revenue with cloud and enterprise sales each growing more
than 70% year-over-year, exceeding the outlook we provided last quarter. We gained x86 server
revenue share year-over-year as customers expanded deployments of both fifth-gen EPYC Turin and
fourth-gen EPYC Genoa families.
In cloud, hyperscalers continued expanding EPYC across their internal infrastructure and public cloud
offerings, including AWS, Microsoft, Google, Oracle and others. Fifth-gen EPYC Turin now powers
nearly 1/3 of the more than 1,600 EPYC public cloud instance types available globally as providers
broaden their offerings with new database storage and AI workloads. That expanding footprint is
translating into growing adoption of EPYC in the cloud with health care, financial services, media and
technology companies adding tens of millions of instances last quarter.
In enterprise, we delivered record sales in our fourth consecutive quarter of record sell-through as on-
prem adoption accelerated driven by the leadership performance and TCO advantages of our EPYC
portfolio. Growth was broad-based as we won large deployments with leading financial services,
manufacturing, telecom, retail, and technology companies. More than 230 fifth-gen EPYC platforms
are now in market from HPE, Dell, Lenovo, Supermicro and others, our broadest enterprise portfolio to
date. Looking ahead, agentic AI is creating a new growth vector for server CPUs, spanning high-
frequency AI host nodes, high-density agentic servers and general-purpose cloud and enterprise
workloads.
Our sixth-gen EPYC Venice family is purpose-built for this expanding range of workloads and delivers
one of the largest generational performance gains in EPYC history. Built on our all-new Zen 6 core and
2-nanometer technology, Venice extends EPYC leadership in performance and efficiency, delivering
more than twice performance per watt of leading x86 CPUs, and up to 3.3x the performance per watt of
leading ARM-based CPUs. The Venice family includes more than 30 processors that combine
leadership per core and per-socket performance with a broad range of memory and I/O configurations,
giving customers greater flexibility to optimize performance, efficiency, and TCO across the most
widely used cloud, enterprise, and HPC workloads. Venice is in production now with every major OEM
on track to launch platforms and the leading cloud providers planning deployments beginning later this
year. Customer demand for Venice is stronger than for any prior EPYC generation, and we expect to
continue growing market share across cloud and enterprise in the coming quarters.
Turning to our data center AI business. Revenue more than doubled over year driven by strong demand
for Instinct accelerators. MI355x adoption continued to broaden as leading AI companies scale
deployments across a growing range of inferencing and training workloads and cloud providers
expanded MI350-series availability. At our advancing AI event, we launched Helios, our rackscale AI
platform combining EPYC Venice CPUs, MI450-Series GPUs, Pensando networking and ROCm
software. Across a broad range of inferencing workloads, Helios delivers up to 15% more throughput at

the same rack power and up to 30% more tokens per dollar than the competition. Customer pull for
Helios is very strong and tracking ahead of our initial forecast.
In addition to our multi-generation gigawatt scale deployments with OpenAI and Meta, we announced
a new strategic partnership with Anthropic. Anthropic will deploy up to 2 gigawatts of MI450 series
GPUs in Helios with deployment of the first gigawatt beginning in the first half of 2027. The
partnership includes a multiyear joint engineering collaboration using Claude to optimize workloads
for Instinct GPUs and accelerate ROCm software development. We also expanded our long-standing
partnership with Microsoft. Microsoft will deploy Helios at scale on Azure for frontier model
inferencing across Microsoft, its AI customers and Azure AI services. Together, these commitments
broaden the group of leading AI companies and cloud providers building their next-generation
infrastructure on AMD.
Helios is now in production with initial shipments on track to begin later this quarter and ramp
through the fourth quarter and into 2027 to meet very strong customer demand. Looking beyond
Helios, we plan to launch a new rack scale AI platform every year with each generation delivering
significant performance, efficiency and TCO gains. In 2027, our next-generation platform combines
MI500 series GPUs, Verano CPUs and Pensando networking with expanded scale-up domains in both
copper and optical-based interconnects. Customer engagement on MI500 is very strong with multiple
customers working closely with us as they plan their next-generation AI infrastructure. We expect
MI500 to deliver the largest generational leap in instinct history putting us on track to increase
inferencing performance more than 2,000 times in just 4 years.
Turning to our AI software stack. ROCm has reached an important inflection point with the
performance, capabilities and developer experience customers need to deploy AI in production at scale.
The breadth of the ecosystem also continues to expand. More than 3 million models now run out of the
box on AMD, the leading open models launched with day 0 support for Instinct and open source
contributions to ROCm have increased more than tenfold over the past year. We introduced ROCm.ai,
our new AI-assisted development platform for AMD GPUs last month. ROCm.ai let developers use
today's leading coding agents, including Claude, Codex and Cursor to create, port and optimize code for
Instinct, making it significantly faster and easier to bring new models and workloads to AMD. ROCm.ai
delivers more than twice the training performance and won 3x the inferencing performance of ROCm 7
across a broad range of models. We are also working closely with the leading AI labs, including OpenAI,
Anthropic, Meta and others to co-optimize ROCm for their models with the improvements benefiting
the entire AMD ecosystem.
Taking a step back, the overall data center market opportunity is expanding far more rapidly than we
projected just 6 months ago. As AI moves into production across a broader range of applications and
workloads demand for both accelerators and CPUs is growing well above our prior expectations. We
now expect the data center AI accelerator market to grow more than 45% annually to approximately
$1.4 trillion by 2030. And we expect the server CPU market to grow more than 50% annually to
approximately $220 billion by 2030. For AMD, this larger opportunity, combined with the strength of
our portfolio and growing customer visibility is creating a steeper growth trajectory for our data center
business.
In data center AI, the growing number and scale of Helios and MI450 Series Instinct deployments
position the business for significant growth in the second half of the year with growth accelerating in

2027. In server CPUs with very strong customer demand and improved supply, we now expect server
revenue to grow more than 80% year-over-year in the second half of 2026 and more than 70% for the
full year 2027, off a much higher base. Taken together, we now expect data center segment revenue to
more than double year-over-year in 2027.
Turning to Client and Gaming. Segment revenue grew 6% year-over-year to $3.8 billion. In client,
revenue increased 23% year-over-year to $3.1 billion, driven by record mobile processor revenue and
continued share gains. Commercial adoption continued to expand in the quarter, with Ryzen Pro sales
growing more than 50% year-over-year as we close new wins with large health care, technology,
automotive, and financial services companies. To build on this momentum, Dell, HP, Lenovo, Asus and
others launched a broad portfolio of new commercial PCs powered by our latest generation Ryzen AI
Pro 400 series processors. Demand was also strong for our Ryzen AI Halo developer systems, which
went on sale in the quarter. In July, we introduced our next-generation Ryzen AI Halo platform
powered by our new Gorgon Halo processor, featuring an industry-leading 192 gigabytes of unified
memory and can run models with up to 300 billion parameters. And to make it even easier for
developers to build and test large AI models locally, we are partnering with Hugging Face to include 1
year of Hugging Face Pro with every Ryzen AI Halo system beginning later this year.
Looking to the second half of the year, we are planning for a softer PC market as higher memory and
component costs weigh on demand. Against this backdrop, we expect our client business to perform
better than the market, driven by the strength of our Ryzen portfolio and growing commercial
adoption. In gaming, revenue declined 31% year-over-year to $779 million, primarily due to lower
semi-custom sales at this stage of the console cycle. Gaming graphics revenue also declined year-over-
year as higher industry-wide component costs contributed to higher graphics card prices and weighed
on overall demand.
Turning to our Embedded segment. Revenue increased 19% year-over-year to $977 million, our
strongest growth in more than 3 years. Demand was broad-based with strength across networking,
aerospace and defense, test measurement and emulation and communication customers. Our
embedded x86 business grew significantly in the quarter as hyperscalers and networking customers
increasingly adopted our CPUs to power critical networking and control plane functions in the data
center. We also continued to expand our portfolio, introducing Ryzen AI embedded x100 processors for
demanding real-time edge AI workloads and the Kria AI robotics platform for physical AI. Looking
more broadly, the strategy we have been executing over the last few years is now delivering strong
results. Embedded x86 is becoming a significant growth driver for the segment. Our overall embedded
portfolio is outgrowing the market and gaining share, and our embedded semi-custom engagements are
expanding. Design win momentum also remains very strong. We are tracking towards another record
year with more than $18 billion of new design wins, led by major wins with networking, data center,
communications, tests, and aerospace and defense customers.
In summary, we delivered record revenue and profitability in the second quarter, reflecting our strong
execution and the growing adoption of our leadership products. We entered the second half with strong
momentum across our businesses. With Venice and MI455X now in production, initial Helios
shipments set to begin this quarter, Ryzen Pro CPUs driving continued commercial share gains and our
embedded segment returning to strong year-over-year growth.

More than a decade of focused investment has given us the strongest and broadest product portfolio in
the industry, deep strategic relationships with the companies driving the future of computing and a
proven ability to deliver multi-generation road maps and ramp complex products at scale. At the same
time, AI is driving demand for dramatically more compute across all of our markets. We now see the
overall market for high performance in AI computing growing approximately 40% annually over the
next several years, approaching $2 trillion by 2030, and we expect to grow well above the market. As a
result, we are tracking materially ahead of the long-term financial model we shared at our Financial
Analyst Day last November.
We now expect revenue to grow substantially above our prior target of greater than 35%, and we expect
to significantly exceed our $20 annual EPS target within our strategic timeframe. We are still in the
early innings of a multiyear AI adoption cycle and the opportunity ahead is enormous. We are
exceptionally well positioned to capitalize on this opportunity and deliver significant growth in the
coming years.
Now I will turn the call over to Jean to provide additional color on our second quarter results. Jean?
Jean Hu (Executives)
Thank you, Lisa, and good afternoon, everyone. I'll start with a review of our second quarter financial
results and then provide our current outlook for the third quarter of fiscal 2026. We had an outstanding
second quarter, marking our sixth consecutive quarter of greater than 30% year-over-year revenue
growth. Revenue increased 50% year-over-year and 13% sequentially to a record $11.5 billion, driven by
continued momentum across our businesses. Importantly, data center accounted for approximately
58% of total revenue, underscoring the continued shift in our business mix and its increasing
contribution to AMD's growth. On comparable basis, diluted earnings per share increased
approximately 82% year-over-year, significantly outpacing our revenue growth and demonstrating our
earnings power as we scale our business.
Gross margin for the quarter expanded to 56%, up over 200 basis points year-over-year and 80 basis
points sequentially, reflecting a favorable product mix and a growing contribution from our data center
business. Operating expenses were $3.4 billion, an increase of 40% year-over-year as we continue to
invest in R&D to expand our AI silicon systems and software capabilities to support our long-term
growth opportunities. Operating income was $3.1 billion, representing a 27% operating margin.
Now turning to our reportable segment, starting with the data center segment. Revenue was a record
$6.7 billion, more than doubling year-over-year and up 16% sequentially. Growth was driven by greater
than 70% year-over-year increase in EPYC sales with record enterprise sell-through and robust demand
across our cloud customer base. Both unit shipments and ASP increased significantly year-over-year
reflecting the continued mix shift powered to our latest Zen 5 generation processors. Instinct sales
more than doubled year-over-year with the continued ramp of our MI350 Series product as adoption
broadened across the largest AI labs, cloud providers, leading AI start-ups, national labs and the
sovereign AI deployment. Data center segment operating income was $2.1 billion or 31% of revenue.
Client and Gaming segment revenue was $3.8 billion, up 6% year-over-year and 7% sequentially. The
client business revenue was $3.1 billion, up 23% year-over-year and 6% sequentially, led by record
mobile revenue. The gaming business revenue was $779 million, down 31% year-over-year, primarily
due to lower semi customer revenue. Sequentially, gaming revenue increased 8%, driven by higher semi

customer sales, partially offset by lower Radeon shipments. Client and Gaming segment operating
income was $582 million or 15% of revenue compared to $767 million or 21% a year ago, reflecting
continued investment in go-to-market activities and expanding product road map.
Embedded segment revenue was $977 million, up 19% year-over-year and 12% sequentially as demand
continued to improve across end markets and the new design wins began ramping. Embedded segment,
operating income was $386 million or 40% of revenue, compared to $275 million or 33% a year ago,
driven by higher revenue and favorable product mix. Turning to the balance sheet and the cash flow.
During the quarter, we generated $2.4 billion in cash from continuing operations and $1.6 billion in
free cash flow. Inventory increased sequentially to approximately $8.5 billion to support strong data
center demand. At the end of the quarter, cash, cash equivalents and short-term investments were $13.1
billion.
Now turning to our third quarter 2026 outlook. We expect revenue to be approximately $13 billion plus
or minus $300 million. At the middle point of our guidance, revenue is expected to be up 41% year-
over-year, driven by very strong double-digit growth in our data center segment. Strong double-digit
growth in our embedded segment and the decline in the client gaming segment with growth in our
client business more than offset by significant double-digit decline in gaming. Sequentially expect
revenue to be up approximately 13%, driven by strong double-digit growth in both our data center and
embedded segments and a modest decline in our client gaming segment with a slight growth in client
offset by strong double-digit decline in gaming.
In addition, we expect third quarter non-GAAP gross margin to be approximately 56%. Non-GAAP
operating expenses to be approximately $3.65 billion, non-GAAP other income and expense to be again
of approximately $55 million. Non-GAAP effective tax rate to be 13% and the diluted share count is
expected to be approximately 1.66 billion shares. In closing, we delivered another outstanding quarter
of revenue growth and the significant earnings expansion, reflecting the strength of our execution and
the strong momentum across the business. As data center growth continue to accelerate, we entered the
second half of the year, very well positioned to deliver continued profitable growth.
With that, I'll turn it back to Matt for the Q&A session.
Matthew Ramsay (Executives)
Thank you very much, Jean. John, we'd like to go ahead and start the Q&A session now. Please do poll
the audience for questions. We ask that each caller ask 1 question with 1 brief follow-up. Thank you.
Operator (Operator)
Thank you, Matt. [Operator Instructions] And the first question comes from the line of Tom O'Malley
with Barclays.
Thomas O'Malley (Analysts)
Lisa, you laid out the Analyst Day $1.4 trillion TAM on the accelerator side. You laid out the $220
billion on the CPU side. But the share dynamics within those are very different. So I think the genesis of
the question here is when do you see that crossover point happening in the data center GPU business
and the CPU business. Is that something that comes this calendar year? And when you look at the
relative contributions between those 2 buckets, into calendar year '27 from a dollars perspective, where
are you seeing the most strength?

Lisa Su (Executives)
Yes. Tom, thanks for the question. So look, we are certainly seeing a very, very strong compute market
demand over both the data center accelerator as well as the server CPU. I think the server CPU is a little
bit newer, and so we've been giving updates on that. As we go forward, certainly, looking at our Q3
guide our Q4 guide, we see very strong growth across both server and data center AI. So we're seeing
server grow over 80% in the second half of the year-over-year. We're seeing very strong data center AI
growth and that reflects into our 2027. The way to think about it is both businesses are going to grow a
lot. The data center AI TAM is certainly larger. And as a result, as we ramp the large strategic customers
that we have on Helios in 2027, you would expect substantial growth in that business in 2027. But both
businesses are very significant drivers of our 2027 growth and beyond.
Thomas O'Malley (Analysts)
And then maybe under that framework with both growing very strongly into next year. Maybe this one
is for you, Jean. You obviously have some headwinds in the -- on the GPU side as you're ramping
Helios. But also on the server processor side, you would imagine that you're getting above corporate
gross margins there. Maybe as you look at the trade-offs to gross margins into next year, is one kind of
offsetting the other? Or could you maybe think that directionally, just given some of the tailwinds
you're seeing with pricing directionally with the mix shift to more CPUs, could you see a tailwind more
so than a headwind into calendar year '27?
Jean Hu (Executives)
Yes, Tom, that's a great question. Thank you for that. I think as we talked before, our gross margin is
primarily driven by the mix -- business mix. We're actually very pleased with our gross margin progress
in the first half of 2026 and our guidance for Q3 2026. I think the way to think about the 2027 is there
are a few puts and takes. The first thing is, right, as Lisa just mentioned, our server business is
expanding very significantly with the increased TAM and the pace of our business continue to grow,
which from a gross margin perspective is accretive to our overall gross margin. .
On the other side, you are right, the pace of data center AI ramp is also very important because from a
revenue opportunity perspective, we see large incremental revenue opportunity from data center AI
once it ramps not only added tremendous revenue for the company, but also gross profit. The gross
margin is slightly below copper average. I think the mix will determine how we go through 2027. But
overall, we actually feel good about how we can really navigate through the transition of the business
and continue to improve our gross margin to manage the balance of the gross margin plus our
Embedded business is recovering significantly. We actually think the Embedded business will give us
additional tailwind on the gross margin side in 2027. So I feel really good about that.
Operator (Operator)
And the next question comes from the line of Timothy Arcuri with UBS.
Timothy Arcuri (Analysts)
Lisa, I wonder if you could give us any color just what's embedded in the guidance in terms of data
center. So the question really is like of the growth between Q2 and Q3, which will grow more on a dollar
basis CPU or GPU? And I ask because if I take your up 80% half-on-half number, it sort of implies that

server CPU might not grow that much in Q4. So I'm not sure if I'm doing that wrong. Can you just give
us some color there?
Lisa Su (Executives)
I'm just looking at that, Tim. Look, I think we believe that the server CPU is going to grow substantially
in Q3 and Q4. The way I would describe it in terms of dynamics is we have been -- we have very strong
demand across all of our customers in hyperscale and enterprise. And we have been adding additional
supply as we've increased supply throughout the year. So we would -- we're guiding the Q3 segment to
grow sequentially double digits. Both server and the data center AI will grow nicely within that. And
then we should expect more growth for each of those businesses in Q4 with more supply coming on for
server as well as for data center AI, the Helios ramp is just starting at the end of Q3, and it will be much
more substantial in Q4, so that should sort of give you the picture of -- we think Q3 is certainly a strong
quarter as we look at the strong -- very strong double-digit growth going into in data center segment.
And in Q4, it will be higher than that.
Timothy Arcuri (Analysts)
Okay. And then just as a follow-up. So relative to the TAM that you laid out Analyst Day. I think it's a
40% CAGR out through 2030. So -- and do you think you can outgrow that CAGR out through 2030. So
is your plan to grow your revenue more than 40% during that period?
Lisa Su (Executives)
Yes. So as we look at the overall TAM, first of all, it's a very exciting time in the compute market. When
you look at every part of our business, whether it's server CPU, data center AI or our embedded
business and our PC business we see them all benefiting from the AI tailwinds. And beneath that, I
think in each one of the segments, we see an opportunity to grow above the market. So from that
standpoint, with our view of the TAM being greater than 40%. We are also saying that we will grow
greater than from an overall revenue standpoint for the company.
Operator (Operator)
And the next question comes from the line of Vivek Arya with Bank of America Securities.
Vivek Arya (Analysts)
Lisa, I'm curious with all the announcements that you have made, how many gigawatt of compute does
AMD have line of sight into for 2027 and what is AMD's monetization per gigawatt. I think the current
assumption from everything you've announced is about 3 gigawatts and I think from some of the
warrant numbers that you had mentioned before, right? It seems to be at least $15 billion per gigawatt.
But so I'm just curious if you agree with those views and then what is the upside or downside to either
the gigawatt or the content assumption?
Lisa Su (Executives)
Yes. So Vivek, there are lots of pieces to that question. So maybe let me take them one at a time. From
an overall data center standpoint, I think we have given a little bit of color on 2027, we believe that the
server CPU portion of our data center business will grow by over 70% year-over-year off of a higher
base. And we believe the overall segment will grow by over 100%, so we'll more than double due to the

data center AI ramping. So we do see a very significant ramp into 2027. We are very happy with our
strategic anchor customers in OpenAI, Meta, and Anthropic. They are all in the process of ramping
compute demand is high, and this is very much aligning their data center build-outs and their work
with their cloud service providers together with our ramp.
The way I would describe it is we have supply to more than meet the guidance that we've talked about
and the upside potential is there. The key thing is to work very closely with our customers as they're
planning their build-outs overall. So I think from a Helios ramp standpoint, we're expecting a very
significant ramp over the next couple of quarters. We've said Q3 is the very beginning of the ramp. Q4
is a step-up, and then Q1 will be a further step up and we'll ramp as we go through 2027. So hopefully,
that gives you a little bit of color on how that data center AI will play out.
And in terms of the revenue per gigawatt, I think we've said double-digit billions. We're still in that
range. I think there's -- that looks like that's pretty much where it will be. And the key here will be
continuing to work with our partners as they ramp because there's a demand for a lot more compute,
and we would like to satisfy that demand.
Vivek Arya (Analysts)
And for my follow-up, a little of a technical question. When we look at the specs of Helios, it has, I
think, almost 50% more HBM than the competition. And I think you have always had more HBM in
your products. So how much of the benefit is because of having 50% more HBM and then doesn't that
expose AMD more to memory cost inflation. So I'm just curious how are you ensuring that you're able
to maintain margins, right, and get this memory allocation? And I think Jean already suggested you are
comfortable with the gross margin range. But I'm curious how much of the benefit is just because of the
use of more HBM? And does that still enable you to meet your profitability targets and allocation
requirements over time?
Lisa Su (Executives)
So look, Vivek, we're working very, very closely with our memory partners across the board on both our
GPU, HBM memory as well as just the general memory for the systems across our data center business.
And what I would say is we've worked with our memory partners for multiple years to ensure that we
have a strong ramp in our business. There is very good visibility into HBM allocation for what we
expect to deliver in 2027. And the other piece of it is in terms of the memory bandwidth and the
memory capacity, it is one of the advantages of the AMD solutions, when you think about the larger
model sizes, they really benefit from the larger memory footprint, and that goes into the total cost of
ownership.
We do recognize in this memory environment though, every customer is looking at how to optimize
their memory footprint. And we have the opportunity, if desired to also modify that memory footprint if
the total cost of ownership is not as significant in certain workloads. So think about it as the benefit of
the memory is workload-dependent. And we know a bunch of our customers are very, very happy with
what that returns in terms of performance. But there are some workloads, let's call it, medium-sized
models that may not get as much of a benefit. And in that case, we would address the memory footprint
as you might expect.
Operator (Operator)

The next question comes from the line of Joshua Buchalter with TD Cowen.
Joshua Buchalter (Analysts)
Congrats on the very strong results. I wanted to also follow up on the server CPU assumptions for 2027.
So it sounds like the supply for that is locked up, and you have ability to service higher demand if it
continues to track that way. But I guess any help you can give us on sort of the unit and ASP
assumptions that are baked in there? Like I think investors are struggling to model the CPU market
overall. So like how should we think about, I guess, core count growth or whatever is the right proxy as
we think about modeling this business?
Lisa Su (Executives)
Yes. Sure, Josh. So let me maybe start with a little bit of grounding on the growth that we have seen so
far. There are certainly both unit and ASP growth. So if you just look at our Q2 performance, when we
said we grew over 70% in both cloud and enterprise, we actually had double-digit growth in both units
and ASPs, but it was actually more unit. The unit growth was higher. That is very much the nature of
our business. I mean we're seeing just very strong demand from an overall market standpoint.
On the ASP growth, we have ASP growth as we go to higher core counts, for certainly. But as we go
forward, you should expect both unit and ASP growth. And what we have been working on very
diligently over the past couple of quarters is as soon as we saw the significant inflection point in server
demand, we've been working across our supply chain. That's wafers, that's back-end capacity, that's
substrates, that's all of the components to raise the overall capacity for servers. And we're seeing that
play out through this year. That's one of the reasons we can raise the second half guidance. And we're
seeing much more capacity coming in line in 2027 that supports the growth that we've been talking
about. So you should think about both units and ASP in this framework.
Joshua Buchalter (Analysts)
And Lisa, in your prepared remarks, you mentioned that Helios was ahead of your original forecast.
Can we unpack that comment a little bit? Was that a comment on volumes? Was it yields? And then if it
yields, how should we think about sort of the first quarter or 2 of Helios gross margins compared to as
it gets later into its ramp, should we expect gross margins to improve as it ramps?
Lisa Su (Executives)
Yes. So Josh, when I was talking about Helios was ahead of our initial forecast, it was as it relates to the
overall volumes. So the -- let's call it, the amount of demand there is for Helios in 2027. It's like an
outstanding product. So what we're seeing from every one of our customers who's had a chance to not
only spend time with Helios, but also spend time in our overall ecosystem. There is a high confidence
that Helios will be a great addition to the AI portfolio, particularly around inference, and that was my
comment about higher than our initial expectations.
As it relates to your comments about yields and performance and what do we expect as we go through
the ramp. One would expect that the overall yields will improve as we go through the next few quarters,
the starting quarter is this quarter here in Q3, and we will be ramping over the next couple of quarters
and we always would expect that the yields will continue to improve as we go through the first few
quarters, especially on a product like this, which is highly complex.

Operator (Operator)
And the next question comes from the line of Aaron Rakers with Wells Fargo.
Aaron Rakers (Analysts)
As you can imagine, I'll stick with the server piece of the business as well. At your recent event, you
highlighted the server market, the new $220 billion TAM that you're throwing out there as kind of in 3
buckets, right? General purpose, I think you called it or defined it as sandbox servers, and then kind of
the AI front end node. So as we think about the growth that you're talking about, I'm wondering if you
could help us conceptualize the sizing of those buckets at all? And how big is that kind of middle
category, that sandbox AI market as we think about growing 80% plus this back half of the year and
70% plus. How big of that opportunity do you see that becoming?
Lisa Su (Executives)
Yes. So Aaron, what I would say is -- maybe let me start from the end points. So when you think about
the $220 billion TAM in 2030, we actually see this agentic AI or these agentic sandboxes being the
largest piece of the TAM. It's the fastest-growing piece. It's also the smallest piece today. So in the near
term, I would say that there is certainly growth in that area. But as we go out over the next 3, 4, 5 years,
we think that's the largest growth in the server market. And I think the thing that is very strong about
our portfolios. We believe we can grow in every one of those segments. So when you think about the
types of CPUs you need for each of these workloads, you need sort of different optimization points.
That's one of the things that we've really tried to point out. It's not just 1 CPU. It's actually a real family
of CPUs that you need. From our standpoint, Venice is absolutely leadership in all of the categories.
So whether you're talking about per core performance or you're talking about overall socket
performance and that gives us a very strong position across general purpose agentic-AI and also the
head nodes for the AI accelerator business. So from our standpoint, when we look at our customer
traction and our customer momentum going from Turin into Venice, Turin was already extremely
widely used, especially amongst the hyperscalers. What we're seeing is when we go into Venice, the
workloads actually expand. So there are more workloads that are going to be run on the next generation
of EPYC than are run on the previous generation. And that's what gives us the confidence to say that we
can grow substantially ahead of the market given the product positioning.
Aaron Rakers (Analysts)
That's very helpful. And as a quick follow-up. I know it's probably lower on the radar for a lot of people.
But I think in the past, you've talked about the client business even with some pressures in the PC
market growing this year for you guys on a year-over-year basis. Do you still see that? And are you
willing to any kind of give any thoughts on what you might think of 2027 on the client CPU side?
Lisa Su (Executives)
Yes. Well, let me say, first of all, the client CPU business, we have continued to -- I think it's a very
important business. I particularly think that local AI will continue to become a larger and larger piece
of how people experience AI. So I think AI PCs will become more important. As it relates to our client
business in 2026, I think our first half performance has been very strong. And although we are

expecting that the market will decline in the second half, the market has actually held up better than
most people would have thought.
So our view is we will -- we see the growth in 2026 on a year-over-year basis certainly there. And as we
go into 2027, I think we have a strong product portfolio that is coming on board to address not just the
traditional notebook and desktop markets, but also as you think about a more AI-centric PC experience
like what we have been talking about with the Ryzen AI Halo. So I remain optimistic about the PC
market as an important way for us to reach a broader set of users and our ability to grow ahead of the
market. The market itself will depend a bit on some of the components. We're all watching the
component costs and how that will -- how that will play out over the next couple of quarters. But I think
our portfolio and our rising content in enterprise are very positive for our client mix.
Operator (Operator)
And the next question comes from the line of Stacy Rasgon with Bernstein Research.
Stacy Rasgon (Analysts)
First thing, I wanted to pick on something in some of the press release. It tells you that data center
accelerates in the second half. So it grew 107% year-over-year in Q2, you're guiding it up like in the 80s,
though, like in Q3. So how do I interpret which is not acceleration, how do I interpret that statement? Is
like the second half collectively higher than 107% that you see in Q2? Or were you just sort of -- like
how should I be interpreting what you guys wrote in the press release around data center accelerating
in the second half?
Jean Hu (Executives)
Yes. Stacy, this is Jean. Good question. I think when we talk about the acceleration, we are talking
about the second half versus the first half. If you look at the first half, our data center business year-
over-year growth versus the second half, we do think there's an acceleration. That's the reflection there.
Stacy Rasgon (Analysts)
And then I think for my follow-up, I want to dig in a little more into the data center targets for next
year. So you said like more -- I think servers more than 70%, the total more than doubling. I guess what
I'm asking is how much work is the more in that statement doing? Like is -- like you seem to be on a
trajectory that would take you like well above those numbers. I guess, just how should I be interpreting
the more in the statement? understanding that we're only in August of '26, I get it, but what's on your
mind there?
Lisa Su (Executives)
Stacy, you bring a smile to my face. So I would say, we're trying to give you a way to think about 2027.
And yes, the server CPU we're saying is more than 70%, which we think at this point is a very strong
statement just given where the business is. And we do expect the overall data center business to be well
over 100%. And the well over 100% comes because the data center AI business is going to be well over
100% just given the strength of our strategic customers, the ramp of Helios and all of the things that
we've talked about. So hopefully, that answers your more question.
Operator (Operator)

And the next question comes from the line of Jim Schneider with Goldman Sachs.
James Schneider (Analysts)
As you think about the early days of your MI400 series ramp over the next few quarters, can you maybe
talk about the customer diversity you expect in the early stages. I think you've noted 4 or 5 large
customers that you've announced publicly. Can you maybe talk about how many of the customers will
be contributing, let's say, in Q4 and how many in the first half of '27?
Lisa Su (Executives)
Let's see. So Jim, I guess, the way to say it is we've talked about the large frontier model companies,
OpenAI, Anthropic, Meta they will be consuming through a number of CSPs, both hyperscalers and
others. So the diversity of the business -- and there are additional customers. There are lots of
customers who are interested in Helios at, let's call it, a more regular scale than gigawatt scale. So I
think we'll have a good diversity of customers as we go through the next couple of quarters. And what
we're really doing is matching to when the larger data center build-outs are ready. And so we are
working with each of our customers on their data center plans and ensuring that we are meeting their
data center plans. But yes, I think there's a good diversity, especially as we get into the Q4, Q1
timeframe.
James Schneider (Analysts)
And maybe as a follow-up, you mentioned data center readiness. And so I wanted to sort of test how
you're seeing your various customers and their ability to accept your products into their data centers,
whether that's land power shell or anything else? Any constraints that you see heading into the first half
of '27 or even the back half of '27 that would give you pause about hitting your targets?
Lisa Su (Executives)
Well, Jim, I don't think we see anything that would give us pause about hitting the targets. I mean we
feel very good about the targets. Now when you ask me what the range could be? There is a range, and
the range will depend on the ability to bring on more capacity in a timely fashion. So the way I view it is
we are building sort of the entire supply chain. So ensuring that we have the entire -- our silicon CPU,
GPU networking components that go into it, all of the Helios components, I think we feel very, very
good about that part of the supply chain.
We are working very closely on the data center operators and ensuring that we have good visibility into
what's going on there. And that gives us, let's call it, strong confidence in what we've guided for the data
center AI business so far. And we're going to be continuing to look at how to accelerate some of those
bills. And I think there's a clear desire on the part of everyone in the ecosystem to bring on more AI
compute faster. We are seeing every day more opportunities with operators to accelerate some of that
capacity, and that's much of the work that we're doing together with our customers and partners.
Operator (Operator)
And the next question comes from the line of C.J. Muse with Cantor.
Christopher Muse (Analysts)

If I take your data center guide, Lisa, it sort of implies Instinct revenues of $30 billion, give or take. And
so curious, 2 parts on this. How do you see kind of the revenue cadence first half, second half and then
if we isolate to instinct only and start thinking about 455X and Helios, how should we think about the
underlying gross margins for that business starting in Q1 and then exiting in Q4?
Lisa Su (Executives)
I think, C.J. you're saying $30 billion. Are you talking about the server? Or are you talking about which
one are you -- you're talking about 2027, right?
Christopher Muse (Analysts)
I mean, it's '27 instinct yes.
Lisa Su (Executives)
Yes. 2027, maybe let me help. CJ, I think what you're hearing from us is that your data center AI
number is probably too low. And maybe back to Stacy's question without going into exact numbers, I
think this notion of over 100% should consider be well over 100%. And look, as we look at this, it's a
progression over the next couple of quarters. And as we go through the next couple of quarters, we
expect to continue growing Helios quarter-by-quarter. But yes, that's the best way of thinking about it.
And I'm sure Jean can work on if you have further questions on that. But Jean, does that...
Jean Hu (Executives)
yes, yes, yes.
Christopher Muse (Analysts)
And on the gross margin side, if we isolate to instinct, how should we think about beginning 2027 and
then exiting?
Jean Hu (Executives)
Yes. I think overall, when we think about the gross margin for 2027, as I said earlier, it's really
determined by both the pace of server CPU business ramp and the data center AI ramp. So I actually
think overall, quarter-over-quarter, it could be a different mix. It could change differently. But overall,
when we think about this, we are actually very optimistic about how we manage the ramp of the MI450.
At the same time, with the server business continue to improve and grow significantly in 2027.
Overall, I think they have a good offset in general overall. But I do think it's important to remember we
have multiple other levers from the company perspective, not only embedded business, but also client
business, we continue to improve gross margin and operation team continued to do a great job. So we'll
give you more color when we get there to guide the 2027.
Operator (Operator)
And the next question comes from the line of Joe Moore with Morgan Stanley.
Joseph Moore (Analysts)
Great. In the server CPU business, are you supply constrained now? It seems like the market is very
tight. And do you anticipate that tightness persisting? And when you sort of think about next year, just

the general ability of the supply chain to support the level of growth that you're talking about
specifically in CPU?
Lisa Su (Executives)
Sure, Joe. I would say the server CPU supply chain is tight right now, and it has been tight for the first
half of the year because much of this demand was unforecasted. As we get into 2027, the demand is
better forecasted. And so we would expect that the 2027 server supply situation should be better than
'26. We feel very good about being able to satisfy what we just talked about, which was over 70% year-
over-year growth. And I believe depending on how things play out, there may be opportunities for that
growth to go higher as we get through the next few quarters.
Joseph Moore (Analysts)
Okay. And is it -- you guys are ramping a lot on 2-nanometer, and there's been a lot of focus on 3-
nanometer being in short supply. Is that helping? Or is it still challenging to bring up new capacity on
the new node that way?
Lisa Su (Executives)
Yes. I think, Joe, it's always challenging to bring up new capacity on new node. I think what makes our
approach a little bit special and different is that because we're using the chiplet technology, we actually
ramp in fewer wafers in the new node. And so that gives us the opportunity to -- again, we're working
very hard on ensuring that we get the supply necessary to meet the very strong customer demand. So
from my perspective, I think all of that is work that's being done. We're certainly looking at the overall
supply chain, not just wafers, so that includes back-end capacity, packing capacity, substrates, all of
those things. But we feel good about where we are to satisfy both the strong ramp in servers as well as
the strong ramp in the data center AI business.
Matthew Ramsay (Executives)
John, I think we have time for one more caller before we close out the call, please.
Operator (Operator)
Our final question comes from the line of Atif Malik with Citi.
Atif Malik (Analysts)
Lisa, you guys announced a partnership with Cerebras at your Advanced AI Day on disaggregate
compute. Can you talk about just qualitatively, how do you expect the sales to grow in the fast inference
market this year into next year?
Lisa Su (Executives)
Yes, absolutely. So I think the inference market overall is growing very substantially over this year into
next year. The fast inference in particular, is an area which is, let's call it, starting to become more and
more relevant. And so with our partnership with Cerebras, I think they have great technology together
with Helios Plus their wafer scale engine, we get a very good solution for customers. And we would
expect that solution to be start becoming available in Q4 in the Cerebras cloud and extend into 2027.
But from our view, this is an important part of the market, and we continue to look at ways to, I would

say, customize and optimize our technologies for the various workloads out there. So we view this as
just more of what we do in an open ecosystem.
Atif Malik (Analysts)
Great. And one for Jean. How should we think about OpEx growth relative to that overall 40% market
growth that you talked about in the next few years?
Jean Hu (Executives)
Yes. I think Lisa talked about the TAM growth at 40%, and we'll be growing faster than TAM. From an
OpEx perspective, we'll continue to invest given the large opportunities we have ahead of us. But you
should expect us to manage this OpEx increase less than the top line revenue growth. That's what our
business model is designed for so we can drive in more operating leverage to deliver earnings per share.
That is also consistent with Lisa said, our EPS will be significantly higher than $20 we outlined at our
Financial Analyst Day.
Matthew Ramsay (Executives)
Thank you very much for all the analysts and investors that joined our call today. John, you can go
ahead and wrap up the call. Thank you.
Operator (Operator)
Thank you. Ladies and gentlemen, that does conclude the question-and-answer session, and that also
concludes today's teleconference. We thank you for your participation. You may disconnect your lines
at this time.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AMD_Q1_2026_Earnings_Call_20260505.md
- 2026-05-05｜Lisa Su｜guidance：Lisa Su 表示 server CPU TAM 現預期年增率大於 35%，2030 年前規模超過 1,200 億美元。（原話："TAM to grow at greater than 35% annually"）
- 2026-05-05｜Lisa Su｜guidance：Lisa Su 回顧去年 11 月分析師日的 server CPU 市場預期：未來 3 至 5 年年增約 18%。（原話："18% annually over the next 3 to 5 years"）
- 2026-05-05｜Lisa Su｜guidance：Lisa Su 表示 server CPU 營收第二季預期年增超過 70%，並持續到下半年與 2027 年。（原話："more than 70% year-over-year in the second quarter"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 說明正與供應鏈夥伴合作，大幅擴充晶圓與後段產能以支應 CPU 需求。（原話："we are working closely with our supply chain partners"）
- 2026-05-05｜Jean Hu｜guidance：Jean Hu 給第二季營收指引約 112 億美元，正負 3 億美元。（原話："We expect revenue to be approximately $11.2 billion"）
- 2026-05-05｜Jean Hu｜guidance：Jean Hu 表示第二季營收預期季增約 9%，由 Data Center 與 Embedded 雙位數成長帶動，Client and Gaming 小幅成長。（原話："9% driven by double-digit growth in both our Data Center"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 給第二季 non-GAAP 毛利率指引約 56%。（原話："gross margin to be approximately 56%"）
- 2026-05-05｜Jean Hu｜guidance：Jean Hu 給第二季 non-GAAP 營業費用指引約 33 億美元，其他損益為約 6,000 萬美元收益。（原話："non-GAAP operating expenses to be approximately $3.3"）
- 2026-05-05｜Jean Hu｜guidance：Jean Hu 給第二季 non-GAAP 有效稅率 13%，稀釋股數約 16.6 億股。（原話："effective tax rate to be 13%"）
- 2026-05-05｜Jean Hu｜guidance：Jean Hu 表示第一季營收 103 億美元，高於指引上緣。（原話："First quarter revenue was $10.3 billion, exceeding"）
- 2026-05-05｜Lisa Su｜customer：Lisa Su 說明與 Meta 擴大策略合作，將部署最多 6 GW 的 AMD Instinct GPU，橫跨數個產品世代。（原話："Meta to deploy up to 6 gigawatts of AMD Instinct GPUs"）
- 2026-05-05｜Lisa Su｜customer：Lisa Su 將 Meta 與先前公布的 OpenAI 合作並列，稱 AMD 是大型 AI 基礎設施建置商的核心夥伴。（原話："Together with our previously announced OpenAI partnership"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 表示 MI450 系列已開始送樣，Helios 量產出貨仍維持下半年的時程。（原話："remain on track to ramp Helios production shipments"）
- 2026-05-05｜Lisa Su｜customer：Lisa Su 表示主要客戶對 MI450 系列的預測已超過 AMD 原先規劃，且有更多新客戶洽談大規模部署。（原話："lead customer forecasts now exceeding our initial plans"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 表示對 2027 年 Data Center AI 年營收達數百億美元的信心增強。（原話："annual Data Center AI revenue in 2027 and to exceed our"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 在問答中表示看到路徑可超越原先大於 80% 的 CAGR 目標，時間框為 2027 年。（原話："exceed our original targets of greater than 80% CAGR"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 表示在策略時間框內每股盈餘目標為超過 20 美元，並稱有路徑超越長期財務目標。（原話："than $20 in EPS over the strategic time frame."）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 表示第 6 代 EPYC Venice 仍預定今年稍晚推出。（原話："remain on track to launch Venice later this year."）
- 2026-05-05｜Lisa Su｜competition：Lisa Su 表示 Venice 每插槽吞吐量相較領先的 ARM 架構 AI 方案超過 2 倍。（原話："and more than 2x throughput"）
- 2026-05-05｜Lisa Su｜guidance：Lisa Su 表示第二季 Ryzen 需求預期穩健，但規劃下半年 PC 出貨較低。（原話："we are planning for second half PC shipments to be"）
- 2026-05-05｜Lisa Su｜risk：Lisa Su 將下半年 PC 出貨走低歸因於記憶體與零組件成本上升，同時仍預期 Client 營收年增並優於市場。（原話："lower due to higher memory and component costs"）
- 2026-05-05｜Jean Hu｜guidance：Jean Hu 表示下半年 Gaming 營收預期較上半年下滑超過 20%（上一句稱因記憶體與零組件成本）。（原話："second half gaming revenue to decline more than"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示第一季毛利率 55%，較去年同期增加 170 個基點，原因為產品組合有利（含 Data Center 營收占比提高）。（原話："Gross margin was 55%, up 170 basis"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示第一季營業費用 31 億美元，年增 42%。（原話："Operating expenses were $3.1 billion, an increase of 42%"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示第一季營業利益 25 億美元，營業利益率 25%。（原話："representing a 25% operating margin"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示第一季稀釋後每股盈餘 1.37 美元，年增 43%。（原話："diluted earnings per share was $1.37, up 43%"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示 Data Center 部門第一季營業利益 16 億美元、占營收 28%，去年同期為 9.32 億美元、25%。（原話："Data Center segment operating income was $1.6 billion"）
- 2026-05-05｜Jean Hu｜capital_allocation：Jean Hu 表示第一季自由現金流創紀錄的 26 億美元，占營收 25%。（原話："a record $2.6 billion in free cash flow or 25% of revenue"）
- 2026-05-05｜Jean Hu｜capital_allocation：Jean Hu 表示第一季買回 110 萬股，回饋股東 2.21 億美元。（原話："repurchased 1.1 million shares and returned $221 million"）
- 2026-05-05｜Jean Hu｜capital_allocation：Jean Hu 表示季底股票買回授權額度剩 92 億美元。（原話："$9.2 billion authorization remaining"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 表示 Data Center AI 營收年增為「顯著的雙位數百分比」，逐字稿中未給美元金額或確切百分比。（原話："Revenue grew by a significant double-digit percentage"）
- 2026-05-05｜Lisa Su｜risk：Lisa Su 表示 Data Center AI 第一季環比小幅下滑，她歸因於 China 的轉換（第四季 China 收入較多）。（原話："Data Center AI was actually down modestly"）
- 2026-05-05｜Lisa Su｜guidance：Lisa Su 說明 Helios 放量節奏：下半年起步，第三季有初期量，第四季顯著放量。（原話："starting with initial volume in Q3, with a significant ramp"）
- 2026-05-05｜Lisa Su｜guidance：Lisa Su 表示第二季 Data Center 指引為環比雙位數成長，server 與 Data Center AI 兩者都是雙位數。（原話："double digits in both server as well as Data Center AI"）
- 2026-05-05｜Lisa Su｜risk：Lisa Su 承認供應鏈吃緊，Data Center 建置也吃緊。（原話："We feel that there is tightness in the supply chain."）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 表示有信心供應所述成長水準，甚至超過該水準。（原話："we are confident in our ability to supply to the levels of"）
- 2026-05-05｜Lisa Su｜customer：Lisa Su 表示對 2027 年部署已有精細能見度，細到 GPU 會裝進哪些資料中心。（原話："it's visibility down to which Data Centers are the GPUs"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 被問到 server CPU 市占大於 50% 的目標時，回答對達成該市占的機會有信心。（原話："than 50% share of that market."）
- 2026-05-05｜Lisa Su｜competition：Lisa Su 談 ARM 競爭：稱 ARM 是好架構，但 AMD 視其為點狀產品，相對於 AMD 的完整產品組合。（原話："We view it as more point products relative to a portfolio"）
- 2026-05-05｜Lisa Su｜competition：Lisa Su 回應 ARM 與 x86 競爭時表示，大型超大規模業者會同時使用 x86 與 ARM。（原話："I think you're going to see people actually use x86"）
- 2026-05-05｜Lisa Su｜competition：Lisa Su 談低延遲等專用推論架構：預期會出現不同變體，AMD 稱已準備好因應。（原話："we should expect that there will be different variants"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 表示 Data Center GPU 仍將是絕大部分 TAM 的主要加速器。（原話："Data Center GPUs as the primary accelerator"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 表示 CPU 對 GPU 的配比正從過去的 1:4 或 1:8 主機節點，朝接近 1:1 移動。（原話："getting closer to a 1:1 configuration"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 回答 Vivek Arya 時表示 agentic CPU 需求對整體 AI TAM 大致是加項。（原話："it's largely additive to the TAM"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 把 CPU TAM 拆三類：傳統通用型（低雙位數成長）、AI 主機節點、agentic AI；並稱成長最大的一塊是 agentic AI。（原話："the largest piece of the growth is this agentic AI piece"）
- 2026-05-05｜Lisa Su｜margin：Lisa Su 說明第一季 server 成長中，ASP 與出貨量都年增，但主要由出貨量帶動。（原話："it was actually much more unit-driven."）
- 2026-05-05｜Lisa Su｜margin：Lisa Su 表示第二季與下半年 server 成長多數來自出貨量，ASP 漲幅用來覆蓋通膨壓力。（原話："growth is unit-driven and the ASPs are just really to help"）
- 2026-05-05｜Lisa Su｜margin：Lisa Su 表示供應鏈吃緊帶來成本上升，AMD 與客戶分攤部分成本。（原話："we are sharing some of that with our customers"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示 MI450 第三季開始放量、第四季大幅放量，其毛利率低於公司平均。（原話："That is below corporate average."）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示對 2026 年毛利率的整體架構有信心，順風因素可抵銷部分 MI450 的稀釋。（原話："feel really good about the setup of the gross margin"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 重申分析師日訂的長期毛利率區間為 55% 至 58%，並說第一年進展良好。（原話："long-term gross margin in the range of 55% to 58%"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 被問 Instinct 毛利率時，表示目前聚焦營收成長，營收放量後在 ASP 與成本面有改善空間。（原話："we'll have a lot of opportunities to improve gross margin"）
- 2026-05-05｜Jean Hu｜commitment：Jean Hu 表示今年 R&D 的成長會明顯快於 SG&A。（原話："you should expect us to grow R&D much faster than SG&A."）
- 2026-05-05｜Lisa Su｜capital_allocation：Lisa Su 說明銷售與行銷投資投向企業級 server、商用 PC 與中小企業市場。（原話："the investments are going into enterprise servers"）
- 2026-05-05｜Jean Hu｜capital_allocation：Jean Hu 回應費用一再超出指引的提問時，表示公司正積極投資。（原話："we actually are investing aggressively"）
- 2026-05-05｜Lisa Su｜risk：Lisa Su 表示已確保足夠記憶體供應可達成並超越目標，但也說明記憶體環境吃緊。（原話："we have secured enough supply to certainly meet"）
- 2026-05-05｜Lisa Su｜risk：Lisa Su 表示 Client 第一季桌機較軟，因桌機偏消費市場，較受記憶體與零組件漲價影響。（原話："We did see desktops a little bit softer"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 表示 Turin 本季占營收已超過 50%，Milan 出貨已隨時間下降。（原話："crossed over 50% of our revenue being Turin this quarter"）
- 2026-05-05｜Lisa Su｜customer：Lisa Su 表示 Embedded 的設計案動能年增雙位數百分比，新增設計案價值達數十億美元。（原話："with billions of dollars in new wins across markets"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 表示 AMD 大幅加快 ROCm 開發節奏，做法包括增加軟體投資與 agent 式程式開發流程。（原話："we have significantly accelerated our ROCm"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 預告將在七月的 Advancing AI 活動分享下一代 Instinct、EPYC、Helios 與客戶合作進展。（原話："our Advancing AI event in July"）
- 2026-05-05｜Jean Hu｜risk：Jean Hu 被追問時表示 China 在第一季收入不重大。（原話："the China revenue in Q1 is not material."）

### AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md
- 2025-11-11｜Matthew Ramsay｜margin：開場聲明：當天幾乎所有數字都是 non-GAAP，GAAP 對帳表在簡報附錄與 SEC 文件。（原話："pretty much every number that we're going to talk about"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱資料中心 AI 營收未來 3 到 5 年的年複合成長率超過 80%。（原話："over 80% AI revenue CAGR over the next 3 to 5 years"）
- 2025-11-11｜Jean Hu｜guidance：Jean 稱 2027 年資料中心 AI 營收軌跡為數百億美元（tens of billion）。（原話："tens of billion dollars of data center AI revenue in 2027"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 提到先前講過 2027 年營收目標為 tens of billions of dollars，並稱進度符合。（原話："So I can say that we're on track to that."）
- 2025-11-11｜Lisa Su｜guidance：全公司營收成長目標以 2025 年約 340 億美元為基期。（原話："a baseline in 2025 of $34 billion"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱全公司營收年複合成長率超過 35%（3 到 5 年框架）。（原話："over 35% CAGR at the total company level"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱核心業務（Client 與 Embedded）年複合成長率超過 10%；資料中心超過 60%。（原話："growing also well ahead of the market at over 10% CAGR"）
- 2025-11-11｜Forrest Norrod｜guidance：Forrest 稱 AMD 資料中心事業未來 3 到 5 年有明確路徑達 60% 年複合成長率。（原話："clear line of sight to 60% CAGR over the next 3 to 5 years"）
- 2025-11-11｜Forrest Norrod｜guidance：Forrest 把 60% 年複合成長率換算為資料中心年營收超過 1000 億美元。（原話："over $100 billion in annual AMD data center revenue"）
- 2025-11-11｜Jean Hu｜guidance：Jean 給長期財務模型：3 到 5 年毛利率區間 55% 到 58%。（原話："expect our gross margin to be in the range of 55% to 58%"）
- 2025-11-11｜Jean Hu｜guidance：Jean 給長期模型：營業利益率超過 35%、稅率 13% 到 15%（同句接續給自由現金流利潤率超過 25%）。（原話："operating margin to be more than 35%, the tax rate of 13%"）
- 2025-11-11｜Jean Hu｜guidance：Jean 稱預測期間每股盈餘超過 20 美元。（原話："per share to be more than $20 in the forecast period"）
- 2025-11-11｜Jean Hu｜guidance：Jean 答毛利問題時提到 Q4 毛利率指引為 54.5%。（原話："We guided Q4 at 54.5%."）
- 2025-11-11｜Jean Hu｜guidance：Jean 稱 MI450 預期 2026 下半年開始放量。（原話："we expect MI450 to start to ramp in second half of 2026"）
- 2025-11-11｜Jean Hu｜guidance：Jean 對 2026 年給的唯一方向：營收成長會高於 OpEx 成長。（原話："one thing I can tell you is revenue growth next"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 回應 Stacy：近年成長率預期高於 80%，且稱對 tens of billions 落在市場想法附近感到 comfortable。（原話："faster than 80%, so greater than greater than 80%."）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱伺服器營收市占目標為 3 到 5 年內超過 50%（目前約 40%）。（原話："path to over 50% revenue share of the server market"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱 Client 營收市占目標為 3 到 5 年內超過 40%（目前高 20% 區間）。（原話："a clear path to over 40% client revenue market share"）
- 2025-11-11｜Jack Huynh｜guidance：Jack 稱 Client 營收成長將達市場的 3 倍以上，並把市占推到 40% 以上。（原話："revenue growth at more than 3x the market rate while"）
- 2025-11-11｜Jack Huynh｜guidance：Jack 被問 TAM 時：Client TAM 3 到 5 年預估低到中個位數成長。（原話："we're projecting low to mid-single digit"）
- 2025-11-11｜Salil Raje｜guidance：Salil 稱 Embedded 近期營收成長為市場的 2 倍。（原話："we'll grow our revenue at 2x the market rate"）
- 2025-11-11｜Salil Raje｜guidance：Salil 稱長期隨 semi-custom 與 physical AI 放量，Embedded 成長升到市場的 3 倍。（原話："up to 3x the market rate over the long-term horizon"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱 Embedded adaptive 營收市占目標為 3 到 5 年內超過 70%。（原話："over 70% of the embedded adaptive revenue market share"）
- 2025-11-11｜Salil Raje｜guidance：Salil 稱核心 FPGA 業務市占正朝 70% 走（Lisa 講的是 3 到 5 年 embedded adaptive 超過 70%，用詞不同）。（原話："We're also tracking to 70% market share in our core FPGA"）
- 2025-11-11｜Jean Hu｜guidance：Jean 稱資料中心 TAM 從今年 2000 億美元成長到 2030 年超過 1 兆美元。（原話："go from $200 billion this year to over $1 trillion in 2030"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱 2030 年 TAM 超過 1 兆美元；此為新口徑（延伸到 2030 年）。（原話："greater than $1 trillion by 2030."）
- 2025-11-11｜Lisa Su｜guidance：Lisa 說明 TAM 口徑擴大：除加速器外，也納入 CPU 與部分網路內容。（原話："but also include CPUs and some of the"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱先前 2028 年 TAM 預測（超過 5000 億美元）現在被大幅上修。（原話："we're seeing that number come up significantly"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 回顧 AI TAM 歷次上修：3000 億、4000 億、再到 5000 億美元。（原話："we updated it to $400 billion and then $500 billion."）
- 2025-11-11｜Daniel McNamara｜guidance：Dan 稱到 2030 年 CPU TAM 增加 300 億美元，約為目前的兩倍。（原話："we're going to add $30 billion in CPU TAM"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱 2025 年資料中心營收預估超過 160 億美元、成長率超過 50%。（原話："estimated over $16 billion, over 50% growth rate"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱 2025 年全公司營收預估約 340 億美元。（原話："We're now projecting to be about $34 billion this year"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱混合（mix）仍是毛利率的主要驅動因素。（原話："Third is mix, which remain to be the primary driver"）
- 2025-11-11｜Jean Hu｜margin：Jean 談資料中心整體（近半營收）時稱其毛利率較高；後段講 Data Center AI 時口徑不同（見下條）。（原話："what's really most exciting, it has a higher gross margin"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 Data Center AI 業務目前毛利率略低於公司平均。（原話："our gross margin is slightly below corporate average"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱在快速成長的市場，毛利金額最大化是第一優先。（原話："maximizing gross margin dollars is our #1 priority"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 Data Center AI 賣的是 GPU、CPU、有時 DPU，不賣整櫃系統，毛利結構與現在相同。（原話："Our business model is not going to change."）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 Client 毛利率仍遠低於公司平均，有續升空間。（原話："it's still very much lower than corporate average"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱企業市場每多一個百分點的市占，對整體毛利率都明顯加分。（原話："is significantly accretive to our overall gross margin"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 2025 年預期毛利率達 54%。（原話："expect to deliver gross margin of 54% this year"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 2025 下半年 MI350 大量放量，毛利率仍持續擴張。（原話："we are able to continue to expand the gross margin"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 2025 年營運獲利水準超過 33%（稿中原文措辭為 of operating income，未寫 margin）。（原話："deliver over 33% of operating income"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 2027 年 Data Center AI 放量，若量很大，毛利率可能落在 55% 區間下緣。（原話："it could be closer to the 55% range"）
- 2025-11-11｜Lisa Su｜margin：Lisa 談 HBM：自家主導設計的部分預期有健康毛利，但代為搭載的 HBM 不預期同等毛利。（原話："same margin on HBM. And I think that's fair"）
- 2025-11-11｜Lisa Su｜margin：Lisa 澄清 1 兆美元 TAM 為矽（silicon）TAM，含隨 GPU 搭載的 HBM。（原話："includes the HBMs that go with the GPUs."）
- 2025-11-11｜Forrest Norrod｜margin：Forrest 強調 1 兆美元是矽 TAM，不宜與他人整體方案 TAM 比較。（原話："That's not to be compared to some others"）
- 2025-11-11｜Jean Hu｜margin：Jean 回答 MI450 初期是否稀釋毛利率時稱目前還不知道。（原話："Right now, actually, I don't know yet."）
- 2025-11-11｜Jean Hu｜capital_allocation：Jean 稱 2021 年起已透過買回股票回饋股東 86 億美元。（原話："Since 2021, we have returned $8.6 billion cash to"）
- 2025-11-11｜Jean Hu｜capital_allocation：Jean 稱買回股票先抵銷員工股權稀釋，有機會再做額外買回。（原話："offset the employee stock dilution first"）
- 2025-11-11｜Jean Hu｜capital_allocation：Jean 稱 2025 年自由現金流預期較去年成長逾一倍。（原話："we expect to more than double our free cash flow"）
- 2025-11-11｜Jean Hu｜capital_allocation：Jean 以 ZT Systems 為例：收購設計團隊、同時剝離製造業務。（原話："We acquired the ZT design team."）
- 2025-11-11｜Lisa Su｜capital_allocation：Lisa 稱 AMD 現在有更積極的創投投資部門（幾年前沒這麼做）。（原話："a much more active venture investments arm"）
- 2025-11-11｜Jean Hu｜capital_allocation：Jean 稱過去累計透過有機投資與併購投入超過 1000 億美元。（原話："we have invested over $100 billion through organic"）
- 2025-11-11｜Jean Hu｜capital_allocation：Jean 稱 2025 年是加碼投資的一年（硬體路線圖、系統軟體、ZT 與軟體併購）。（原話："2025 is an important year for us to invest."）
- 2025-11-11｜Jean Hu｜commitment：Jean 承諾營收成長速度要快於營運費用成長。（原話："But we are very committed to drive revenue"）
- 2025-11-11｜Forrest Norrod｜commitment：Forrest 稱機櫃層級系統也將維持每年一代的節奏（元件同樣維持年度節奏）。（原話："we will continue on annual cadence for the components"）
- 2025-11-11｜Forrest Norrod｜commitment：Forrest 稱 AMD 自己不賣機櫃系統，透過 OEM、ODM 與 ZT 夥伴（Sanmina）推向市場。（原話："AMD is not selling the rack systems."）
- 2025-11-11｜Lisa Su｜commitment：Lisa 談執行力：稱說了要做的事就會做到。（原話："that we're going to do something, we're going to do it."）
- 2025-11-11｜Mark Papermaster｜commitment：Mark 稱 AMD 持續投入開放軟體與開放硬體的 AI 生態系。（原話："commitment to open software and open hardware"）
- 2025-11-11｜Lisa Su｜commitment：Lisa 稱與 OpenAI 的第一個 gigawatt 已說過會在 2026 下半年開始、延續到 2027。（原話："the first gigawatt will start in the second half of '26"）
- 2025-11-11｜Lisa Su｜commitment：Lisa 稱與 Oracle 的合作以 2026 第三季為 MI450 公有雲執行個體的放量目標。（原話："targeting third quarter and '26 as the ramp"）
- 2025-11-11｜Forrest Norrod｜commitment：Forrest 稱 Helios 預計 2026 年 Q3 上市。（原話："when it comes to the market in Q3 of next"）
- 2025-11-11｜Daniel McNamara｜commitment：Dan 稱 Venice 明年上市，採台積電 2 奈米製程。（原話："It's on 2-nanometer TSMC process."）
- 2025-11-11｜Mark Papermaster｜competition：Mark 稱競爭對手在 AI 上走較封閉的專有（walled garden）方案，AMD 走開放。（原話："more proprietary walled garden solutions."）
- 2025-11-11｜Forrest Norrod｜competition：Forrest 稱資料中心現在面對的是另一個不同的主導對手（相對於早年 CPU 市場的對手）。（原話："a new dominant competitor, a different dominant competitor"）
- 2025-11-11｜Lisa Su｜competition：Lisa 估計 ASIC 佔加速器 TAM 約 20% 到 25%，其餘為 GPU。（原話："So ASICs, maybe 20% to 25% of"）
- 2025-11-11｜Lisa Su｜competition：Lisa 說明 ASIC 適用情境：模型與演算法較穩定、下一步可預期時。（原話："ASICs tend to be good if your models -- if your algorithms"）
- 2025-11-11｜Lisa Su｜competition：Lisa 稱標準款 GPU 仍會是最大成長動能，但也可能做客製化 GPU。（原話："I still believe that standard product GPU will be"）
- 2025-11-11｜Forrest Norrod｜competition：Forrest 稱伺服器 CPU 除了對 Intel，也在與 ARM 比 TCO 與效能。（原話："not just with Intel, but also with ARM"）
- 2025-11-11｜Lisa Su｜competition：Lisa 稱 AMD 在伺服器 CPU 已是現任者（incumbent），不把任何市占視為理所當然。（原話："we don't take any share for granted"）
- 2025-11-11｜Daniel McNamara｜competition：Dan 稱市場上有 CPU 被 GPU 蠶食的論點，他說實際看到的是相反。（原話："that CPUs have been cannibalized."）
- 2025-11-11｜Lisa Su｜competition：Lisa 稱今年前曾有 GPU 會吃掉 CPU 工作負載的說法，實際看到相反的情況。（原話："We've actually seen the opposite be true."）
- 2025-11-11｜Lisa Su｜competition：Lisa 稱雲端對通用伺服器的需求增幅出乎 AMD 意料。（原話："demand has actually surprised us."）
- 2025-11-11｜Lisa Su｜competition：Lisa 稱通用運算需求上升是可持續的趨勢（過去兩年 TAM 大致持平）。（原話："This feels like a real durable trend."）
- 2025-11-11｜Daniel McNamara｜competition：Dan 稱伺服器 CPU 營收市占約 40%。（原話："we're hovering around 40% share"）
- 2025-11-11｜Vamsi Boppana｜product：Vamsi 給 MI455X 規格：432 GB HBM、19.6 TB/s（同段稱最高 40 petaflops FP4）。（原話："It has 432 gigabytes of HBM memory running at 19.6"）
- 2025-11-11｜Vamsi Boppana｜product：Vamsi 引用 InferenceMAX 基準：MI355 在 GPT OSS 上單位 token 服務成本最多較前代降至 1/10 水準（稿中原文 up to 10x benefits）。（原話："MI355 on the GPT OSS model deliver up to 10x benefits"）
- 2025-11-11｜Vamsi Boppana｜product：Vamsi 稱 MI500 系列不是漸進式改版，是下一次重大突破。（原話："this is not an incremental step on our road map."）
- 2025-11-11｜Vamsi Boppana｜product：Vamsi 介紹新增的 MI430，針對科學運算與主權需求，強調雙精度浮點。（原話："we have built the MI430 product."）
- 2025-11-11｜Vamsi Boppana｜product：Vamsi 談 AI 寫 GPU kernel：稱未來會移除採用 AMD 平台的最後障礙（同段稱目前尚未完全到位）。（原話："and it will take down with it any last remaining barriers"）
- 2025-11-11｜Forrest Norrod｜product：Forrest 稱光學互連預計 2027 到 2029 年間開始轉換，先從機櫃級 scale-up 開始。（原話："we believe in the '27, '28, '29 time frame"）
- 2025-11-11｜Forrest Norrod｜product：Forrest 稱長期走向光學，銅與 SerDes 只會短期並存。（原話："but it's all going optics long term."）
- 2025-11-11｜Lisa Su｜product：Lisa 稱 AMD 已贏得數個資料中心 semi-custom 案。（原話："we have won several data center semi-custom"）
- 2025-11-11｜Lisa Su｜product：Lisa 稱這些資料中心 semi-custom 案偏向系統周邊（含部分網路元件），不是運算單元本身。（原話："not the compute unit itself, but some of the attach"）
- 2025-11-11｜Lisa Su｜product：Lisa 稱 2025 年 AMD 選擇不推機櫃級方案，把資源放在新資料格式與時程，MI450 才備齊各項元件。（原話："We chose not to do Rack Scale solutions"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱與 OpenAI 簽下 5 年 6 gigawatt 合作（準備稿口徑：over 5 years）。（原話："announce a 6-gigawatt deal over 5 years"）
- 2025-11-11｜Lisa Su｜customer：Lisa 在 Q&A 把同一合約期間說成 4 或 5 年（準備稿說 5 年）。（原話："6 gigawatts over 4 or 5 years"）
- 2025-11-11｜Lisa Su｜customer：Lisa 回答客戶集中度：OpenAI 是重要基礎，但稱同期會有多家超大規模客戶。（原話："OpenAI is an important foundation, but we will have"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱 OpenAI 合約結構是逐年檢視需求與供應的紀律式安排。（原話："it's a very disciplined engagement."）
- 2025-11-11｜Lisa Su｜customer：Lisa 承認 OpenAI 是算力預測最積極的客戶之一。（原話："one of the most aggressive when it comes to their compute"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱 MI450 世代預期有多家規模相近（gigawatt 等級）的客戶，供應鏈依此規劃。（原話："We expect to have multiple similar-sized customers"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱首度公開展示與 Meta 合作的 Helios 機櫃方案。（原話："showed for the first time our Helios Rack scale solution"）
- 2025-11-11｜Vamsi Boppana｜customer：Vamsi 舉例：某超大規模客戶一年內在 Instinct 上跑的工作負載超過 70 個。（原話："within 12 months, within 1 year, they now have over 70"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱 MI450 完全放量並通過驗證後，預期轉換多個 gigawatt 等級機會。（原話："we would expect to convert a number of those opportunities"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱客戶說法改變：去年說投資會趨緩，現在說不會趨緩、需要加速。（原話："no, it's actually not going to level off."）
- 2025-11-11｜Lisa Su｜customer：Lisa 回應 OpenAI 資金能力疑慮：稱不會押注反方。（原話："I wouldn't bet against that. I really wouldn't."）
- 2025-11-11｜Jack Huynh｜customer：Jack 稱 Client 營收占比達 28% 的紀錄高點，ASP 兩年成長 50%。（原話："our ASPs to a record 28% revenue share"）
- 2025-11-11｜Jack Huynh｜customer：Jack 稱 Client and Gaming 營收由 96 億美元成長到超過 140 億美元。（原話："50% year-on-year increase in revenue from $9.6 billion to"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱 Embedded 設計訂單 2025 年將超過 160 億美元（2024 年為 140 億美元）。（原話："We're on a path to exceed $16 billion this year."）
- 2025-11-11｜Salil Raje｜customer：Salil 稱 Embedded 累計設計訂單超過 360 億美元（與 Lisa 講的另一組設計訂單數字並列，稿中未說明兩者關係）。（原話："We won thousands of designs totaling $36 billion plus."）
- 2025-11-11｜Salil Raje｜customer：Salil 稱 semi-custom 設計訂單 150 億美元，涵蓋車用、資料中心、航太國防、無線。（原話："$15 billion across automotive, data center"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱近 12 到 18 個月新簽 semi-custom 設計訂單合計超過 450 億美元（與 Salil 的 150 億美元數字並列，稿中未說明差異）。（原話："now totaling over $45"）
- 2025-11-11｜Salil Raje｜customer：Salil 稱 semi-custom 長期可占 Embedded 事業近三分之一。（原話："scaling up to almost 1/3 of our business"）
- 2025-11-11｜Salil Raje｜customer：Salil 稱 physical AI 市場 2035 年預期超過 2000 億美元。（原話："expected to be $200 billion plus by 2035"）
- 2025-11-11｜Salil Raje｜customer：Salil 稱擴大後的 Embedded 產品線可觸及 300 億美元 TAM。（原話："tap into $30 billion of TAM"）
- 2025-11-11｜Salil Raje｜risk：Salil 稱 Embedded 過去兩年的疲軟來自庫存調整，現已過去、成長回來。（原話："Now that phase is behind us, and growth is returning"）
- 2025-11-11｜Lisa Su｜risk：Lisa 稱最近財報電話會議已把中國從營收預測中拿掉。（原話："China out of our revenue forecast because it's too hard"）
- 2025-11-11｜Lisa Su｜risk：Lisa 稱中國在她所說的 TAM 中占比很小。（原話："it's also a small piece of our TAM"）
- 2025-11-11｜Lisa Su｜risk：Lisa 承認供應環境正在趨緊。（原話："the supply environment is getting tighter"）
- 2025-11-11｜Lisa Su｜risk：Lisa 稱有信心整體供應鏈能支撐所提的成長模型。（原話："feel very confident that we have the overall supply chain"）
- 2025-11-11｜Lisa Su｜risk：Lisa 稱花不少時間研究客戶與全球的電力路線圖，以對照預測。（原話："spending quite a bit of time looking at the power road map"）
- 2025-11-11｜Lisa Su｜risk：Lisa 回應融資疑慮：稱若 AI 使用量如預期成長，會有足夠的融資。（原話："I think there's going to be plenty of financing"）

### 問答異常語氣（迴避／改口／保留）
- AMD_Q1_2026_Earnings_Call_20260505.md｜問：Stacy Rasgon：Q1 Data Center AI 排除 China 後，環比是否仍成長？｜答法：Jean Hu 先重複「DC AI 環比小幅下滑、主因 China 收入較低」，Rasgon 指出未回答後，她只說 China 在 Q1 不重大，仍未回答排除 China 後是否成長。Lisa Su 稍早對 Tom O'Malley 則說 DC AI 下滑是因為 China 轉換、Q4 China 收入較多。
- AMD_Q1_2026_Earnings_Call_20260505.md｜問：Stacy Rasgon：營業費用一再超出 AMD 自己給的指引，為何難預測、今年剩餘時間如何看？｜答法：Jean Hu 改談「積極投資、投資帶動營收動能、營收超標拉高部分費用、支援 DC AI 客戶」，未解釋預測為何偏低，也未給全年費用數字。
- AMD_Q1_2026_Earnings_Call_20260505.md｜問：C.J. Muse：Instinct 產能吃緊，毛利率是否可在 1-3 年內拉近公司平均？｜答法：Jean Hu 回答目前聚焦營收成長，只說「over time」營收放量後在 ASP 與成本面有改善機會，未給目標、時程或數字。
- AMD_Q1_2026_Earnings_Call_20260505.md｜問：Aaron Rakers：為 AI 工作負載優化的 CPU，ASP 是否結構性高於通用 server CPU？｜答法：Lisa Su 明說沒有可提供的相對 ASP 數字，稱取決於工作負載，只說核心數增加時 ASP 會上升。
- AMD_Q1_2026_Earnings_Call_20260505.md｜問：Vivek Arya：AMD 是否已確保足夠記憶體供應，相較對手已揭露大量預付款？｜答法：Lisa Su 答稱與記憶體廠商關係深、已確保足夠供應以達成並超越目標，同時說明記憶體環境吃緊；未回應預付款，也未給數字。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Timothy Arcuri 問零組件成本上漲（記憶體等）如何計入模型，可能傷及 PC 與伺服器 TAM。｜答法：Jean 回答營運團隊與 Forrest 在管控零組件供應與成本可見度，未說明是否或如何計入財務模型，未給數字。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Vivek Arya 與 Joseph Moore 追問 80% 成長對應的資料中心 AI 市占願景（Vivek 自算約中段十幾％）。｜答法：Lisa 說明近期為 bottoms-up、遠期為策略對話，並稱目標為 meaningful double-digit percentage，兩題都未給具體市占數字。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Stacy Rasgon 指出以 80% 成長從約 65 億美元推算 2027 年只有約 200 到 210 億美元，低於市場約 290 到 300 億美元。｜答法：Lisa 稱近年成長會高於 80%，只說對 tens of billions 落在市場想法附近感到 comfortable，未確認或否認市場共識數字。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Joshua Buchalter 問多個 gigawatt 級專案要轉換需要跨過哪些門檻，以及規模與 OpenAI 相比如何。｜答法：Lisa 談與超大規模客戶的關係、供應鏈準備與軟體工作，未列出具體門檻，也未比較與 OpenAI 的規模。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Christopher Rolland 問營運費用成長是否前置、是否高於約 25%，以及市場預期的 2026 年營收成長（中高十幾％）方向是否應上調。｜答法：Jean 說 2026 年度營運計畫仍在制定、沒有明確路徑，只給營收成長會高於 OpEx 成長；未回答是否前置與 2026 營收預期方向。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Benjamin Reitzes 問近期有什麼事讓 AMD 對 OpenAI 6 gigawatt 更有信心。｜答法：Lisa 描述合約為逐年檢視的紀律式結構、首個 gigawatt 時程與多客戶佈局，稱 quite comfortable，未點名新增的具體事件。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：William Stein 問客戶能否取得資金與電力，以及是否預期出現更多類似 OpenAI 的非典型融資交易。｜答法：Lisa 詳談電力路線圖、超大規模客戶資產負債表穩健與 OpenAI 用量成長，稱融資足夠；未直接回答是否還會有其他非典型融資交易。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Christopher Caso 問既然近期優先最大化毛利金額，如何看 55% 到 58% 長期區間，以及 MI450 初期是否稀釋毛利率。｜答法：Jean 稱近期毛利率與現在相近、55% 到 58% 取決於 mix 與量，MI450 放量期的毛利影響答稱取決於量與節奏並說目前還不知道；未給稀釋幅度。

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

**`contradictions[]`**：先列一致判斷，再列矛盾(矛盾點/A側/B側/性質：可調和=程度差異、不可調和=方向相反)；⚖不可調和矛盾必填裁決：選哪邊/依據(非「直覺」)/硬數據點/執行路徑(≥1 if-then＋1反向條件，動作具體如加碼至X%/清倉，禁「再評估」)；Steelman義務：觀望迴避寫「現在就買的最強論證」，進場寫「現在就賣的最強論證」。前份漂移歸因：`drift_watch`20欄按`cause`三選一(`價格變動`/`新證據`/`方法變動`)分組，`prior_field`填涵蓋欄名陣列，漏一欄＝FAIL；門檻或Single Thing與前份不同須歸因「舊→新＋理由」，`rearm_trigger`不得寫「相同」；觀望須點名binding constraint，`rearm_trigger`=該約束的否定，多因素模糊觀望=重寫 [§5]；前次觀望/迴避且報酬>+30%須明寫翻面理由；90天內翻面須引用前次觸發器已發火，引不出填`qc49_inherit_prior=true`+`prior_verdict`+`prior_role` [§4]。

**負向證據強制處置（硬擋）**：`findings_digest[]`每條`direction="-"`的finding必落於`contradictions[]`/`blind_spots[]`/`triggers[]`/`moat.threats[]`/`thesis.R[]`之`evidence_refs`，或寫進`evidence_dismissed[]`(`{"ref":…,"reason":…}`，理由需指出證據本身問題，禁「影響不大」)。`triggers[]`每列`n`/`text`/`type`/`maps_to`/`metric`/`threshold`/`action`/`source_freq`/`date`；type僅八值(假設驗證/風險/Single Thing/估值rearm/加碼/減碼/清倉/複審日期)，H1-H3或R1-R3寫`maps_to`不塞`type`。`kill_metrics[]`陣列，每條`metric`/`bear_threshold`/`window`＋`source`；`rearm_trigger`=估值rearm/進場首倉列；`catalysts[]`type英文六值`product`/`regulatory`/`capacity`/`guidance`/`macro`/`other`(禁中文)。QC-39產業態勢三軸(必填一句)：A競爭惡化/B結構轉好與durability/C其他結構變數(法規/關稅/反壟斷/通路/商模/替代技術/客戶結構)→裁決=競爭惡化中/結構性轉好中/其他結構變動中(指名哪軸)/雙向拉鋸/靜態＋一句sourced依據，禁只報單向 [§6]。重大事件：M&A(>市值5%)/集體訴訟/臨床或FDA讀數/CEO或CFO離職或SEC調查/客戶流失皆🔴，涉核心假設或護城河須入`thesis.R`或`moat.threats` [§5][§6]。

**必答項**：三視角blind_spots各至少一條、不可調和矛盾的⚖裁決、`evidence_dismissed[]`(若有負向finding未落點)、`kill_metrics[]`、`rearm_trigger`。

---

## ⑤決策輸入與行動條件

**`decision_inputs`**（值可`null`，`dd_decision.py`機械路由裁決）七欄：`thesis_irreconcilable`(§4不可調和)｜`valuation_dependent`(re-rate貢獻≥Base IRR 40%)｜`market_wrong_reason_given`(市場錯在哪的具體理由)｜`week26_return_pct`(26週漲幅)｜`momentum_overheated`(RSI 14d>70或4週漂移>+10%)｜`cycle_gates_pass`(反動能五閘全過，循環股)｜`consensus_rev_3m_pct`(FY1/FY2共識近3月上修%)，缺值`null`。覆寫層：`val_denominator_disputed`/`qc49_inherit_prior`+`prior_verdict`+`prior_role`/`held_now`(bool三態不可`"unknown"`代`null`)；`asym_ratio`/`irr_base_pct`/`ev5y_pct`一律`null` [§5]。

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
{"date":"20260805","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Instinct 自個位數份額爬向雙位數，MI450／Helios 的 GW 級承諾轉為實際營收","columns":{"2Y 驗證點":"2027 年資料中心 AI 營收落在 $33B 以上；Meta 首個 GW 的認股權證第一批如期 vest","5Y 驗證點":"AI 加速器份額達雙位數；Helios 成為超大規模第二供應的機櫃級標配","10Y 驗證點":"MI500／Verano 世代維持效能與 TCO 競爭力，份額不回落","具體數字門檻":"2027 年 DC AI 營收 ≥ $35B（管理層對分析師 ~$30B 模型明言「大概太低了」）。品質限定：其中由 AMD 自身股權投資所支撐的 Anthropic 分項須單獨揭露，不計入「純需求」驗證","信息來源":"2026-08-04 法說；2026-02-24 特別法說（Meta 6GW 條款）","漂移觸發條件":"連 2 季 GPU 營收 TTM 偏離指引 ≥ 10% → 削弱"}},{"id":"H2","text":"EPYC 伺服器份額續創高，Intel 製程與產品持續弱勢","columns":{"2Y 驗證點":"營收市佔守住 46%；Venice（Zen 6，2nm）於各大雲端如期部署","5Y 驗證點":"x86 伺服器穩居領先，ARM 侵蝕限於自研範圍","10Y 驗證點":"資料中心 CPU TAM 內維持 &gt;50% 增量份額","具體數字門檻":"EPYC 營收市佔維持 ≥ 45%（現 46.2%）","信息來源":"Mercury Research 2026Q1；公司法說","漂移觸發條件":"連 2 季份額回落 ≥ 3pp → 削弱"}},{"id":"H3","text":"市場願為「AI 第二供應商」付溢價，且激進的 EPS 上修真的兌現","columns":{"2Y 驗證點":"FY2026 EPS ~$7.45 兌現；FY2027 共識 $13.9 不下修","5Y 驗證點":"FY2028 EPS ~$20 量級兌現，倍數隨之自然壓回 24–28x","10Y 驗證點":"盈餘力撐起 $768B+ 市值不靠 re-rate","具體數字門檻":"FY2027 共識 EPS 維持 ≥ $12（含權證稀釋路徑）","信息來源":"買方共識 Excel snapshot 2026-07-30（FY26 $7.45／FY27 $13.78／FY28 $20.02）；yfinance 財報後刷新 n=45–46","漂移觸發條件":"連 2 月共識下修 → 估值假設反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"混合稀釋壓過營運槓桿：MI450／Helios 的毛利率低於公司平均，且 Helios 的 HBM 含量高於對手約 50%，正撞上 SK 海力士執行長口中「史上最差」的 2027 記憶體供給年。管理層兩度拒絕指引 2027 毛利率。","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1–2 季可觸發）","監測指標":"單季毛利率 vs 資料中心營收占比的斜率；FY2027 首次毛利率指引","警戒閾值":"資料中心占比 +5pp 而合併毛利率 −50bp 以上；或 FY2027 指引 &lt; 55%"}},{"id":"R2","text":"對手方信用與循環融資：早期 Helios 客戶名單中的 Oracle 據報處於投機等級邊緣（$1,300 億債務、自 2025-09 高點下跌逾六成、並有退休基金就其 2025 年債券發行前隱匿 OpenAI 交易風險提起證券訴訟）；AMD 自身於 2026-07 對 Anthropic 承諾最高 $50 億里程碑條件股權投資，同時取得其最高 2GW 承諾——AMD 已在用自己的資產負債表補貼一部分 2027 指引裡的需求。","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4–6 季）","監測指標":"Oracle 信用評等與 AMD 相關採購揭露；AMD 對 Anthropic 投資的實際撥付進度與其對應營收占比","警戒閾值":"任一早期 Helios 客戶被降至投機等級或公開延後採購；或自身投資支撐的營收占 2027 DC AI 逾 15%"}},{"id":"R3","text":"產業級 AI 資本支出報酬重定價：2026-07 中下旬四篇獨立報導在同一週窗口記錄同一敘事——AI 資本支出報酬遭質疑、資金窄化回 NVIDIA 一家、AMD／Marvell／Intel 同步下跌。AMD 於 7/23 發表會後五日跌 22%、8/4 財報後再跌 9.2%，兩次都不是公司特定利空。","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"四大超大規模業者 2027 資本支出指引方向；產業前瞻倍數帶","警戒閾值":"任兩家 2027 資本支出指引年增率跌破 +20%；或半導體板塊前瞻倍數帶再下移一個標準差"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":10.6,"ev5y_pct":48.6,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.1,"ev5y_pct":48.6,"irr_base_pct":10.6,"max_dd_pct":-68.0,"bull_5y_price":1260.0,"bear_5y_price":216.0,"p_bull_pct":22.0,"p_bear_pct":33.0,"rearm_trigger":null,"price_at_dd":470.79,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMD_20260923/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
