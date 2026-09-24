你是 stock-analyst **v20 判斷 agent**，標的 LULU（20260924）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"LULU","date":"2026-09-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LULU_20260924/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LULU_20260924/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_revenue_gaap","label":"Net revenue（GAAP）","value":2415.6,"period":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","unit":"$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","citation":"公司新聞稿 8-K Ex.99.1 Condensed Consolidated Statements of Operations（$2,415,631K vs 去年同期 $2,525,219K）；QoQ 為自算（vs Q1 $2,471,603K）"},"note":"共識約 $2.46B、實際低約 1.6%（web_search 聚合站報導，未經第二來源核對）；公司自家 Q2 指引 $2.450–2.475B，實際低於指引下緣"},{"id":"f_kpi1_comparable_sales_total","label":"Comparable sales（total）","value":-9,"period":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","citation":"公司新聞稿 8-K Ex.99.1（constant dollar −10%；Americas −12%；International −3%，constant dollar −6%；China Mainland −2%，constant dollar −8%）"},"note":"n/a（未取得可靠的 comp 共識）"},{"id":"f_kpi2_gross_margin_gaap","label":"Gross margin（GAAP）","value":60.5,"period":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","citation":"公司新聞稿 8-K Ex.99.1（gross profit $1,461,878K；含 IEEPA 關稅退款 $134.5M＝+560bp）；扣除退款的 54.9% 為自算（60.5%−5.6pp；管理層電話會議亦說 ex-refund 較指引的 −410bp 好 50bp，即 −360bp，兩者相符）"},"note":"n/a"},{"id":"f_kpi3_gaap_operating_income_op","label":"GAAP operating income／operating margin","value":18.8,"period":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","unit":"% margin（營業利益 $453.7M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","citation":"公司新聞稿 8-K Ex.99.1（income from operations $453,653K vs $523,814K，YoY −13%；margin 18.8% vs 20.7%）"},"note":"n/a"},{"id":"f_kpi4_operating_margin_ieepa_n","label":"Operating margin 扣除 IEEPA 關稅退款（自算，非公司 non-GAAP）","value":13.2,"period":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","unit":"% margin（營業利益約 $319.2M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","citation":"自算：GAAP 營業利益 $453.653M − 公司揭露的退款 $134.5M（新聞稿註明退款使 operating margin +560bp）。公司本季不發布 non-GAAP 營業利益（新聞稿的 non-GAAP 只有 constant dollar），此數字僅供還原一次性項目"},"note":"n/a"},{"id":"f_kpi5_diluted_eps_gaap","label":"Diluted EPS（GAAP）","value":2.92,"period":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","unit":"$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","citation":"公司新聞稿 8-K Ex.99.1（vs $3.10；含關稅退款與相關利息稅後 +$0.86）；扣除退款的 $2.06 為自算（2.92−0.86）"},"note":"共識約 $1.82（web_search 聚合站報導，未經第二來源核對）；公司自家 Q2 指引 $1.76–1.81。GAAP 數字勝出全靠退款，扣除後 $2.06 仍高於指引，主因為較指引低的獎金提列與費用管控（管理層說明）"},{"id":"f_kpi6_free_cash_flow","label":"Free cash flow（單季）","value":225.2,"period":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","unit":"$M（占營收 9.3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","citation":"自算：Q2 營運現金流 $374.8M（上半年 $589,278K − Q1 $214,440K）− Q2 資本支出 $149.7M（上半年 $277,056K − Q1 $127,380K，10-Q https://www.sec.gov/Archives/edgar/data/1397187/000139718726000127/lulu-20260802.htm 與 Q1 10-Q；管理層電話會議說 capex 約 $150M）。公司新聞稿只揭露上半年累計，不揭露單季 FCF。營運現金流含已收到的關稅退款 $134.5M"},"note":"n/a"},{"id":"f_kpi7_stock_based_compensation","label":"Stock-based compensation（單季）","value":21.1,"period":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","unit":"$M（占營收 0.9%；占 GAAP 營業利益 4.6%；占扣退款營業利益 6.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","citation":"10-Q 股東權益變動表：上半年 $50,275K − Q1 $29,186K（Q1 10-Q）＝Q2 $21,089K；占比為自算"},"note":"n/a"},{"id":"f_kpi8_guidance_q3_fy2026","label":"Guidance：Q3 FY2026","value":"營收 $2.290–2.320B（YoY −10% 至 −11%）；EPS $0.93–0.98；營業利益率約 6.5%（去年 Q3 為 17%）","period":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","citation":"公司新聞稿 8-K Ex.99.1（營收與 EPS、稅率約 30%）；營業利益率、毛利率 −250bp、SG&A 去槓桿 800bp、降價 +60bp、北美中段兩位數衰退（美國同）、中國大陸與其他市場 +3–5% 來自 CFO 於 2026-09-03 電話會議的準備稿（逐字稿 LULU_Q2_2027_Earnings_Call_20260903.md）"},"note":"n/a（未取得 Q3 單季共識）"},{"id":"f_kpi9_guidance_fy2026","label":"Guidance：FY2026 全年","value":"營收 $10.350–10.500B（YoY −5% 至 −7%）；EPS $9.48–9.73（含 Q2 退款 +$0.86）；營業利益率較 FY2025 −530bp（含退款 +130bp）","period":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","citation":"公司新聞稿 8-K Ex.99.1（營收、EPS、稅率約 30%、不含任何後續退款與回購）；毛利率 −80bp、SG&A +450bp、降價 +40bp、營業利益率 −530bp、淨新店約 35 家來自電話會議準備稿"},"note":"FY1 EPS 共識 $9.39（dd_numbers_extra.py consensus_revision，2026-09-19 快照），低於新指引下緣 $9.48；90 天前（2026-06-23）為 $11.03"},{"id":"f_kpi10_inventory","label":"Inventory","value":1711.5,"period":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","unit":"$M（YoY −1%；單位數 −7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","citation":"公司新聞稿 8-K Ex.99.1（$1,711,450K vs $1,722,570K）；Q3 期末指引為金額低個位數成長、單位數略減，全年金額中個位數成長、單位數約持平（電話會議）"},"note":"n/a"},{"id":"f_kpi11_share_repurchases","label":"Share repurchases（單季）與 門市數","value":330.0,"period":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","unit":"$M（2.7M 股）；期末 825 家門市（淨增 9）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）","citation":"公司新聞稿 8-K Ex.99.1；剩餘授權約 $713M（電話會議）。期末現金 $1,389.7M、循環信用可用額度 $593.7M。回購 $330.0M 高於同季自算 FCF $225.2M，差額由現金池補（現金較 FY2025 年底 $1,807.2M 少 $417.5M）"},"note":"n/a"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-09-03","period":"2026-09-03","unit":"date","basis":"距今 15 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-09-03"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_lulu_gross_margin_pct","label":"LULU 毛利率","value":56.11,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LULU.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lulu_operating_margin_pct","label":"LULU 營業利益率","value":17.84,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LULU.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lulu_fcf_margin_pct","label":"LULU FCF 利潤率","value":12.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LULU.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nke_gross_margin_pct","label":"NKE 毛利率","value":42.91,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NKE.gross_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nke_operating_margin_pct","label":"NKE 營業利益率","value":8.18,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NKE.operating_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nke_fcf_margin_pct","label":"NKE FCF 利潤率","value":4.71,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NKE.fcf_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_onon_gross_margin_pct","label":"ONON 毛利率","value":64.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONON.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_onon_operating_margin_pct","label":"ONON 營業利益率","value":13.79,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONON.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_onon_fcf_margin_pct","label":"ONON FCF 利潤率","value":13.32,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONON.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_deck_gross_margin_pct","label":"DECK 毛利率","value":57.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DECK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_deck_operating_margin_pct","label":"DECK 營業利益率","value":22.67,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DECK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_deck_fcf_margin_pct","label":"DECK FCF 利潤率","value":20.22,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DECK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rl_gross_margin_pct","label":"RL 毛利率","value":70.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RL.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rl_operating_margin_pct","label":"RL 營業利益率","value":16.42,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RL.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rl_fcf_margin_pct","label":"RL FCF 利潤率","value":11.99,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RL.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":102.28,"period":"2026-09-23（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-35.56,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":43.04,"period":"2026-09-23（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.39 → 9.39）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.78 → 8.78）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-09-19","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.78 → 9.78）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":9.39,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":8.78,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":9.78,"period":"2026-09-19","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-14.87,"period":"2026-06-23 → 2026-09-19","unit":"%","basis":"FY1 共識 EPS 11.03 → 9.39（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-09-19","citation":"DD_universe_EPS_estimates_20260919.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":8.54,"period":"2026-09-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-09-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.02,"period":"2026-09-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-09-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.09,"period":"2026-09-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-09-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-09-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-09-23（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":10.89,"period":"2026-09-19","unit":"x","basis":"分母＝FY1 EPS 9.39，分子＝快照價 102.28","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-19"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-09-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 102.28 / W52 152.2 / W104 221.54 / W250 296.45 / W250 13週斜率 -1.82%"},{"id":"f_ma_w52","label":"52 週均線","value":152.2,"period":"2026-09-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":221.54,"period":"2026-09-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":296.45,"period":"2026-09-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-1.82,"period":"2026-09-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Earnest Analytics (交易資料)：2023-04 至 2024-04，Vuori 與 Alo Yoga 各自約取得 1% 的市占；Nike 與 Lululemon 仍主導 Active／Athleisure 市場；除 Under Armour 掉份額外，其餘品牌市占持平或略升。文中未給 Lululemon 單獨的市占百分比。資料期間為 2024 年，非 2026。","source":"Earnest Analytics, 'Athleisure shoppers lean into Vuori, Alo Yoga' — https://www.earnestanalytics.com/insights/athleisure-shoppers-lean-into-vuori-alo-yoga","as_of":"2024-04-22","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Forbes 2026-01-21 文章標題為「Lululemon Hits The Wall While Fabletics Takes Flight」，標題把 Fabletics 描述為上升中的競爭者、Lululemon 為遇到瓶頸的一方。僅見標題與搜尋摘要，內文未抓取，無法引用具體數字。","source":"Forbes (Pamela Danziger), 'Lululemon Hits The Wall While Fabletics Takes Flight' — https://www.forbes.com/sites/pamdanziger/2026/01/21/lululemon-hits-the-wall-while-fabletics-takes-flight/","as_of":"2026-01-21","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Bloomberg 2026-08-05 專題標題為「New Lululemon CEO Faces Off With Alo, Vuori and Chip Wilson」，標題把 Alo、Vuori 列為新任 CEO 面對的主要對手。付費牆，僅見標題與搜尋摘要，內文未取得。","source":"Bloomberg, 'New Lululemon CEO Faces Off With Alo, Vuori and Chip Wilson' — https://www.bloomberg.com/news/features/2026-08-05/new-lululemon-ceo-faces-off-with-alo-vuori-and-chip-wilson","as_of":"2026-08-05","affects":["moat_trend","triggers"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"搜尋摘要顯示：2025 年 9 月 Nike 與 Kim Kardashian 的 SKIMS 推出獨立女性運動服品牌 NikeSKIMS，目標是搶回被 Lululemon、Vuori、Alo 拿走的女性消費者。as_of 為月份層級（2025-09），日期以當月 1 日代填；具體出自哪一篇搜尋結果未逐篇核對（同批結果含 Retail TouchPoints 'Athleisure Faceoff' 一文）。","source":"WebSearch 結果摘要（query: 'Lululemon new entrant OR displace threat athleisure 2026 Alo Vuori'），相關文章：Retail TouchPoints, 'Athleisure Faceoff: How Lululemon, Vuori, Alo and Fabletics are Making Their Case to Consumers' — https://www.retailtouchpoints.com/topics/market-news/athleisure-faceoff-how-lululemon-vuori-alo-and-fabletics-are-making-their-case-to-consumers","as_of":"2025-09-01","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K 原文：\"We work with approximately 51 vendors, five of which produced 47% of our products in 2025, with the largest manufacturer producing 15%.\"（供應端集中度；非客戶端資料）","source":"lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm","as_of":"2026-02-01","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K 原文：2025 年產品 40% 在越南製造、18% 柬埔寨、11% 斯里蘭卡、11% 印尼、7% 孟加拉，其餘在其他地區。","source":"lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm","as_of":"2026-02-01","affects":["thesis.R"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K 原文：\"We do not own or operate any manufacturing facilities.\"（公司自身不自有工廠，製造全部委外）","source":"lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm","as_of":"2026-02-01","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#3","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 原文：\"Many of the specialty fabrics used in our products are technically advanced textile products developed and manufactured by third parties and may be available, in the short term, from only one or a limited number of sources.\"","source":"lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm","as_of":"2026-02-01","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"10-K 附註的信用風險文字：應收帳款主要來自第三方禮品卡銷售、批發帳戶、第三方線上市集、關稅退款應收、授權與供貨安排；一般不要求擔保品，必要時可要求預付款或信用狀；公司稱未發生重大損失，且目前不認為信用風險曝險重大。此段文字經搜尋摘要見於 FY2018–FY2026 多年度 10-K（FY2026 版本未能在 WebFetch 節錄中逐字核對）。","source":"lululemon athletica inc. Form 10-K, fiscal year ended 2026-02-01, https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm（搜尋結果摘要；同文字亦見於歷年 10-K）","as_of":"2026-02-01","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026 10-K 的營收通路分類為 Company-operated stores、E-commerce、Other channels；批發（Wholesale）與 Temporary locations、Outlets、Like New、License and supply arrangements 一併歸在 Other channels，WebFetch 節錄中未見單獨的批發營收金額或比重，亦未見任何單一客戶占營收 10% 以上的揭露。","source":"lululemon athletica inc. Form 10-K, fiscal year ended 2026-02-01, https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm（WebFetch 節錄，非全文）","as_of":"2026-02-01","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"公司 2026-03-18 公布的 FY2026 指引為營收 $11.35–11.50B（分析師預期 $11.52B）、EPS $12.10–12.30（預期 $12.58）。報導引述的需求面描述為「設計新鮮度不足、客戶支出轉軟、大型對手競爭」；管理層優先事項為北美重回全價銷售成長，手段為產品新鮮度、SKU 縮減與庫存再平衡。","source":"FashionNetwork USA, 'Lululemon forecasts softer 2026 amid demand strains, taps ex-CEO of Levi for board' https://us.fashionnetwork.com/news/Lululemon-forecasts-softer-2026-amid-demand-strains-taps-ex-ceo-of-levi-for-board,1816672.html","as_of":"2026-03-18","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"同一報導：FY2026 預估關稅衝擊約 $380M（2025 年為 $275M）；Q4 毛利率年減 550bps，其中 520bps 來自美國進口關稅；公司預期以減少降價與提高全價銷售抵銷「幾乎全部」關稅影響。","source":"FashionNetwork USA, 'Lululemon forecasts softer 2026 amid demand strains, taps ex-CEO of Levi for board' https://us.fashionnetwork.com/news/Lululemon-forecasts-softer-2026-amid-demand-strains-taps-ex-ceo-of-levi-for-board,1816672.html","as_of":"2026-03-18","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Q2 FY2026 財報公布前的預覽（尚非實際結果）：共識 Q2 營收 $2.45–2.475B、年減 2.7%（去年同期年增 6.5%）；共識 EPS $1.79 vs 去年 $3.10（-42.3%）；全年 EPS 指引由 $12.10–12.30 下修至 $10.95–11.15；預估毛利率年減 410bps，其中關稅約 150bps、降價再增 40–50bps；中國大陸預期 +19.5%、其他地區 +14.6%，北美走勢「疲弱」、客流「不均」。此為聚合站預覽文，實際 Q2 結果須待財報。","source":"Pomegra News, 'Lululemon Q2 2026: Athleisure Under Pressure' https://pomegra.io/news/lululemon-q2-2026-athleisure-under-pressure","as_of":"2026-09-24","affects":["moat_trend","thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Texas Attorney General Ken Paxton announced on 2026-04-13 that his office opened an investigation (civil investigative demand) into Lululemon over whether its athletic apparel contains PFAS ('forever chemicals') that health-conscious customers would not expect given the brand's marketing. Scope: review of the company's Restricted Substances List, testing protocols and supply chain practices against its stated safety standards. Framed as a consumer-protection matter.","source":"National Law Review, 'Texas AG Announces CID to Lululemon into PFAS in Athletic Apparel' https://natlawreview.com/article/texas-ag-investigates-lululemon-potential-presence-pfas-activewear ; Freeman Mathis & Gary, 'PFAS regulatory scrutiny expands to consumer apparel: What the Texas AG's Lululemon inquiry signals' https://www.fmglaw.com/environmental-law/pfas-regulatory-scrutiny-expands-to-consumer-apparel-what-the-texas-ags-lululemon-inquiry-signals/","as_of":"2026-04-13","affects":["moat_trend","decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"LULU 10-Q（季末 2026-08-02）：公司已付 IEEPA 關稅 $230M，並開始申請退款（含利息）；2026 年第二季收到 IEEPA 關稅退款 $134.5M（認列於銷貨成本）及相關利息 $4.1M。10-Q 原文另載：美國最高法院於 2026-02-20 宣告 IEEPA 關稅無效，行政部門隨後依其他法源啟動不同稅率的新關稅。","source":"SEC EDGAR, lululemon athletica inc. Form 10-Q (period ended 2026-08-02), https://www.sec.gov/Archives/edgar/data/0001397187/000139718726000127/lulu-20260802.htm（$134.5M 經全文抓取確認；$230M、$4.1M、2026-02-20 判決敘述取自搜尋摘要，未逐字核對全文）","as_of":"2026-08-28","affects":["valuation","thesis.H"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"第二季 $134.5M 關稅退款使毛利率增加 560 bps（Yahoo Finance／Zacks 報導）；同篇報導指第二季營收未達預期、需求仍有壓力。該篇未提 Section 122／232／301 或 de minimis。","source":"Yahoo Finance, 'lululemon Q2 Earnings Beat on Tariff Refunds Despite Revenue Miss', https://finance.yahoo.com/markets/stocks/articles/lululemon-q2-earnings-beat-tariff-142600388.html","as_of":"2026-09-04","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"公司 2026 年預期關稅成本毛額約 $380M，另有較高的行銷與人力支出（2026 年指引偏弱）。此為 2026-03 財測時的數字，之後是否更新未查證。","source":"Jing Daily, 'Lululemon warns of weaker 2026 as tariffs bite', https://jingdaily.com/intels/2026-03/18/lululemon-warns-of-weaker-2026-as-tariffs-bite（數字取自搜尋摘要，未抓全文）","as_of":"2026-03-18","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025（截至 2026-02-01）10-K：未緩解的關稅上升加 de minimis 豁免取消，使 2025 年毛利減少約 $275M；de minimis 取消與 IEEPA 等法源下的較高關稅對 2025、2026 年營運結果有重大不利影響。","source":"SEC EDGAR, lululemon athletica inc. Form 10-K (FY ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm（取自搜尋摘要；as_of 用會計年度結束日，未核到實際提交日）","as_of":"2026-02-01","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"LULU 自身不製造產品，依賴以亞太為主的供應商；2025 年產品製造地占比：越南約 40%、柬埔寨 18%、斯里蘭卡 11%、印尼 11%、孟加拉 7%。（Q2 10-Q 全文未再揭露此比例，此為 10-K 數字。）","source":"SEC EDGAR, lululemon athletica inc. Form 10-K (FY ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm（取自搜尋摘要；as_of 用會計年度結束日）","as_of":"2026-02-01","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#5","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"中國大陸市場營收：2026 Q2 淨營收 $407.1M（約占總營收 17%），上半年 $885.5M（約 18%）。10-Q 未討論該市場的關稅或貿易限制曝險。","source":"SEC EDGAR, lululemon athletica inc. Form 10-Q (period ended 2026-08-02), https://www.sec.gov/Archives/edgar/data/0001397187/000139718726000127/lulu-20260802.htm（經全文抓取）","as_of":"2026-08-28","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#6","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026-06-30 Hagens Berman 於美國華盛頓西區聯邦地方法院提起消費者集體訴訟，指控 LULU 自 2025-02 起以 IEEPA 關稅為由調高直營進口商品售價，向消費者多收數億美元，而該關稅其後被宣告無效；Law360 另報導有新一起消費者關稅退款訴訟。","source":"Business Wire / Hagens Berman press release, 'Hagens Berman Files Consumer Class Action Accusing Lululemon of Unlawfully Passing Tariff Costs to Consumers', https://www.businesswire.com/news/home/20260630748486/en/Hagens-Berman-Files-Consumer-Class-Action-Accusing-Lululemon-of-Unlawfully-Passing-Tariff-Costs-to-Consumers；Law360, 'Lululemon Targeted In New Shopper Tariff Refund Lawsuit', https://www.law360.com/articles/2496328/lululemon-targeted-in-new-shopper-tariff-refund-lawsuit","as_of":"2026-06-30","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 成衣產地：越南 40%、柬埔寨 18%、斯里蘭卡 11%、印尼 11%、孟加拉 7%（五國合計 87%）。","source":"lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm","as_of":"2026-02-01","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 面料產地：台灣 34%、中國大陸 29%、南韓 10%、越南 10%。","source":"lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm","as_of":"2026-02-01","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險段寫明：相當比例的技術面料來自台灣，台灣海峽軍事衝突、貿易禁運或該區中斷，可能對公司取得原料與履行客戶訂單的能力造成重大影響。","source":"lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm","as_of":"2026-02-01","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 約 51 家成衣代工廠、約 65 家面料供應商；前五大代工廠占產量 47%（最大一家約 15%）；前五大面料供應商占面料 48%（最大一家約 20%）。","source":"lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm","as_of":"2026-02-01","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 寫明：許多特殊面料是第三方開發製造的技術型紡織品，短期內可能只有一家或少數幾家來源。","source":"lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm","as_of":"2026-02-01","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#5","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險段稱公司與任何供應商或代工廠均無長期合約，且與其他公司競爭面料、原料與產能。","source":"lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm","as_of":"2026-02-01","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#6","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"lululemon 在長城辦的瑜珈活動出現日本太鼓道具，引發中國消費者反彈，公司公開道歉。","source":"CNN, 'Lululemon yoga event on Great Wall of China causes Japanese drum furor', https://www.cnn.com/2026/06/17/china/lululemon-wall-of-china-drum-japan-intl-hnk","as_of":"2026-06-17","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"FY2026 Q2（截至 2026-08-02）Americas 淨營收 $1,616.8M，年減 8%（去年同期 $1,758.2M）；Americas 可比銷售年減 12%，為各區最弱。Americas 占總營收 67%。","source":"lululemon athletica inc. Announces Second Quarter Fiscal 2026 Results (BusinessWire) https://www.businesswire.com/news/home/20260903500312/en/lululemon-athletica-inc.-Announces-Second-Quarter-Fiscal-2026-Results ；佐證 Sporting Goods Intelligence https://www.sgieurope.com/financial-results/lululemons-tough-quarter-deepens-across-key-markets/122957.article","as_of":"2026-09-03","affects":["moat_trend","thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"FY2026 Q2 China Mainland 淨營收 $407.1M，報告幣別 +4%、固定匯率 -2%；可比銷售固定匯率 -8%；占總營收 17%。SGI 稱管理層承認結果「well below」預期。","source":"Sporting Goods Intelligence, Lululemon Q2 2026 results: revenue down 4% as key markets weaken https://www.sgieurope.com/financial-results/lululemons-tough-quarter-deepens-across-key-markets/122957.article","as_of":"2026-09-03","affects":["moat_trend","thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"FY2026 Q2 Rest of World 淨營收 $391.8M，+5%（固定匯率 +6%）；可比銷售 -4%（固定匯率 -3%）；占總營收 16%。","source":"Sporting Goods Intelligence, Lululemon Q2 2026 results: revenue down 4% as key markets weaken https://www.sgieurope.com/financial-results/lululemons-tough-quarter-deepens-across-key-markets/122957.article","as_of":"2026-09-03","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"FY2026 Q2 全公司淨營收約 $2.4B，年減 4%（固定匯率 -5%）；全球可比銷售 -9%（固定匯率 -10%）；FY2026 營收指引下修至 $10.35–10.5B，SGI 標示為年減 5–7%。","source":"Sporting Goods Intelligence https://www.sgieurope.com/financial-results/lululemons-tough-quarter-deepens-across-key-markets/122957.article ；Yahoo Finance 轉載 Q2 新聞稿 https://finance.yahoo.com/markets/stocks/articles/lululemon-athletica-inc-announces-second-200500621.html","as_of":"2026-09-03","affects":["moat_trend","decision_inputs.bear","valuation","triggers"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"-","claim":"Rest of World 全年營收指引：Q1 時為「mid-teens」成長，Q2 財報後下修為「mid-single digits」成長。","source":"TradingKey, Lululemon (LULU) Fiscal Q2 2026 Earnings Call: Guidance Cut as Revenue Falls https://www.tradingkey.com/news/transcripts/262150881-tradingkey ；Investing.com Q1 2026 逐字稿 https://www.investing.com/news/transcripts/earnings-call-transcript-lululemon-q1-2026-sees-revenue-rise-stock-gains-93CH-4727636","as_of":"2026-09-03","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 Q1（截至 2026-05-03）China Mainland 營收 $478.4M，報告幣別 +30%、固定匯率 +23%；可比銷售固定匯率 +13%；占總營收 19%（去年同期 16%）。Q1 成長含約 8 個百分點的農曆新年時點位移效益。","source":"Sporting Goods Intelligence Q1 2026 https://www.sgieurope.com/financial-results/q1-lululemons-4-growth-hides-a-37-profit-collapse/121480.article ；Kungfudata https://kungfudata.com/resources/lululemon-q1-fy26-china-growth","as_of":"2026-06-04","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"-","claim":"Kungfudata 對 Q1 FY26 的標題稱 China 成長 30%，「home market」（本土市場）萎縮 3%。搜尋摘要未載明該 3% 是 Americas 還是美國，引用時以標題字面為準。","source":"Kungfudata, Lululemon's China just grew 30%. Its home market shrank 3%. https://kungfudata.com/resources/lululemon-q1-fy26-china-growth","as_of":"2026-06-04","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"lululemon 在委託書中揭露，創辦人 Chip Wilson 曾對競爭對手 Alo 與 Vuori 提供諮詢（advised）。Bloomberg 報導標題：Lululemon Says Its Founder Has Advised Rivals Alo and Vuori。","source":"Bloomberg, 'Lululemon (LULU) Discloses Founder Chip Wilson Has Advised Rivals Alo, Vuori', https://www.bloomberg.com/news/articles/2026-04-28/lululemon-says-its-founder-has-advised-rivals-alo-and-vuori","as_of":"2026-04-28","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"lululemon 的 10-K 風險因素寫明：公司的織物與製造技術通常未取得專利，可被競爭對手模仿；織物、技術與製程的智慧財產多由供應商擁有或控制，並非 lululemon 獨有；公司持有的專利與專屬智慧財產有限。若競爭對手以較低價格賣類似產品，淨營收與獲利可能受影響。","source":"lululemon athletica inc. Form 10-K（搜尋結果列出的最新一份為 FY2023 財年報，期末 2024-01-28）https://www.sec.gov/Archives/edgar/data/1397187/000139718724000010/lulu-20240128.htm；搜尋摘要未指明此句出自哪一份 10-K，as_of 取該份年報期末日","as_of":"2024-01-28","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"lululemon 宣布 2026 年進入 6 個新市場（希臘、奧地利、波蘭、匈牙利、羅馬尼亞、印度）。歐洲 5 國夥伴為 Arion Retail Group，印度夥伴為 Tata CLiQ。新聞稿寫歐洲客戶經 eu.lululemon.com 線上購買，印度客戶經 Tata CLiQ Luxury 與 Tata CLiQ Fashion 線上平台購買；門市地點與時程「將於 2026 年公布」，新聞稿未載實體門市數。","source":"lululemon corporate newsroom, press release 'lululemon to Expand International Presence in 2026 with Stores to Open in Six New Markets' https://corporate.lululemon.com/newsroom/press-releases/2025/12-18-2025-113011673","as_of":"2025-12-18","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"lululemon 於墨西哥推出電商網站 lululemon.mx，並計畫 FY2026 在墨西哥新開 8 間門市，年底墨西哥門市合計超過 30 間。文中未說明墨西哥門市是自營或夥伴經營。","source":"Retail Dive, 'Lululemon launches e-commerce in Mexico, expands brick-and-mortar presence' https://www.retaildive.com/news/lululemon-launches-mexico-e-commerce-site-opens-eight-stores/818065/","as_of":"2026-04-21","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026-09-03 公司第二度下修全年財測：FY2026 營收 $10.35–10.50B（前次 $11.0–11.15B，同比 -5% 至 -7%）、EPS $9.48–9.73（前次 $10.95–11.15）。報導同時列出事前市場共識：營收 $11.03B、EPS $10.84，新財測中點明顯低於共識。","source":"Yahoo Finance, 'Lululemon tumbles 17% after another guidance cut; Q2 tops estimates' https://finance.yahoo.com/markets/stocks/articles/lululemon-tumbles-15-weak-guidance-204337889.html ；MarketBeat 'lululemon athletica Updates FY 2026 Earnings Guidance' https://www.marketbeat.com/instant-alerts/guidance-lululemon-athletica-nasdaq-lulu-updates-fy-2026-earnings-guidance-2026-09-03/","as_of":"2026-09-03","affects":["valuation","thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 FY2026 財測：營收中點 $2.305B 對共識 $2.53B；EPS $0.93–0.98 對共識 $2.41。JPMorgan 稱 Q3 展望較共識低約 60%。","source":"Yahoo Finance 'Lululemon tumbles 17% after another guidance cut' https://finance.yahoo.com/markets/stocks/articles/lululemon-tumbles-15-weak-guidance-204337889.html（Q3 共識數字，經搜尋摘要取得）；Yahoo Finance 'Lululemon (LULU): Wall Street Keeps Cutting Targets, But Nobody's Calling It Cheap Enough to Buy' https://finance.yahoo.com/markets/stocks/articles/lululemon-lulu-wall-street-keeps-215239806.html（JPMorgan 60% 說法，2026-09-21 刊出）","as_of":"2026-09-03","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 FY2026 營收年減 4% 至 $2.42B，低於分析師預期的 $2.46B；Americas 營收 -8%、同店銷售 -9%。Yahoo 標題稱 Q2 EPS 優於預期，營收未達。報導稱此次為今年第二度下修全年財測。","source":"Yahoo Finance 'Lululemon Athletica (LULU) Cut Full Year Guidance After Q2 Revenue Decline' https://finance.yahoo.com/markets/stocks/articles/lululemon-athletica-lulu-cut-full-030922053.html ；'Lululemon Shares Fall 17% After FY2026 Guidance Cut Despite Q2 Earnings Beat' https://finance.yahoo.com/markets/stocks/articles/lululemon-shares-fall-17-fy2026-094142265.html","as_of":"2026-09-03","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"賣方目標價分布（stockanalysis.com 彙整）：35 位分析師、共識評級 Hold、平均目標價 $105.65、中位數 $100、區間 $44–$255。頁面標示最近分析師動作截至 2026-09-14。此平均值含 9 月前後不同時點的目標價，未必已反映 9/14 之後的下調。","source":"stockanalysis.com 'lululemon athletica inc. (LULU) Stock Forecast & Price Targets' https://stockanalysis.com/stocks/lulu/forecast/","as_of":"2026-09-14","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"另一彙整站 Public.com 顯示 21 位分析師共識評級 Hold（as of 2026-09-22）。","source":"Public.com 'Lululemon Athletica (LULU) Stock Forecast: Analyst Ratings, Predictions & Price Target 2026' https://public.com/stocks/lulu/forecast-price-target","as_of":"2026-09-22","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"財測下修後個別目標價調整（Yahoo 2026-09-21 彙整）：Citi $130→$117（Neutral，稱股價重挫後風險報酬『略為有利』）；Wells Fargo $105→$95（Equal Weight，稱下滑幅度『jarring』，並把下半年獲利預估下調約 30%）；JPMorgan $154→$95；Morgan Stanley $83（Underweight，分析師 Alex Straton 預期仍有進一步負向修正）；Truist $82（Sell）；BMO 新評等 Underperform、目標價 $70。stockanalysis 同期另記 Goldman Sachs $111→$95、Morgan Stanley $93→$83。","source":"Yahoo Finance 'Lululemon (LULU): Wall Street Keeps Cutting Targets, But Nobody's Calling It Cheap Enough to Buy' https://finance.yahoo.com/markets/stocks/articles/lululemon-lulu-wall-street-keeps-215239806.html ；stockanalysis.com https://stockanalysis.com/stocks/lulu/forecast/","as_of":"2026-09-21","affects":["valuation","decision_inputs.bear","triggers"],"status":"ok"},{"id":"capital_markets_pricing#6","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"stockanalysis 共識營收／EPS 欄位（2026-09-14 頁面）：標為 FY2027 的欄位營收 $10.46B、EPS $9.40；標為 FY2026 的欄位營收 $11.10B、EPS $13.26。EPS $13.26 與 Yahoo 所列 FY2025 實際 EPS 相同，欄位年度標示可能採日曆年慣例（判讀為後者對應已結束的財年、前者對應現行財年，此為讀表判斷，需判斷層再核）。公司新財測為營收 $10.35–10.50B、EPS $9.48–9.73。","source":"stockanalysis.com https://stockanalysis.com/stocks/lulu/forecast/ ；Yahoo Finance https://finance.yahoo.com/markets/stocks/articles/lululemon-lulu-wall-street-keeps-215239806.html（FY2025 EPS $13.26）","as_of":"2026-09-14","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"美國證券集體訴訟（SDNY，案號 24-cv-06033）進入證據開示階段：集體期間 2023-12-08 至 2024-07-24；2026-03-31 法院對被告駁回動議部分准許、部分駁回；2026-05-08 被告提出答辯狀。訴狀指稱公司對庫存配置、產品表現的說法有誤導，2024-07-24 Bloomberg 報導配置不一致當日股價跌 3.3%。","source":"Kessler Topaz Meltzer & Check — lululemon athletica inc. (NASDAQ: LULU) Securities Fraud Class Action, https://www.ktmc.com/new-cases/lululemon-athletica-inc/","as_of":"2026-05-08","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026-09-03 公布 FY2026 第二季財報（公司新聞稿網址日期為 2026-09-03），2026-09-04 股價單日跌 17.4%；之後 BFA Law、Levi & Korsinsky 等律所公告展開證券詐欺調查（調查公告，非已提起的新訴訟），主題為成長動能與整體業務健康度的陳述。","source":"BFA Law 新聞稿 via GlobeNewswire 2026-09-23, https://www.globenewswire.com/news-release/2026/09/23/3367258/0/en/lulu-stock-notification-lululemon-is-being-investigated-for-securities-fraud-after-growth-issues-disclosed-investors-are-alerted-to-contact-bfa-law.html ; Levi & Korsinsky 新聞稿 via PRNewswire 2026-09-16, https://www.prnewswire.com/news-releases/lululemon-athletica-inc-lulu-securities-investigation-notice---levi--korsinsky-302880124.html","as_of":"2026-09-23","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"路透報導：激進投資人 Elliott Investment Management 取得 lululemon 逾 10 億美元持股；報導提到 Elliott 與前 Ralph Lauren 高管 Jane Nielsen 接觸，評估其出任 CEO 的可能。","source":"Ecotextile News 轉載 Reuters — Activist investor acquires $1 billion stake in Lululemon, https://www.ecotextile.com/2025121861163/radar/activist-investor-acquires-1-billion-stake-in-lululemon-reuters/","as_of":"2025-12-18","affects":["triggers","thesis.H"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"公司於 2026-05-18 發布新聞稿，標題為「lululemon Highlights Strength of its Refreshed Board, with the Right Expertise to Drive the Company's Next Phase of Growth and Enhanced Shareholder Value」（僅取得標題與搜尋摘要，未讀全文）。","source":"lululemon 公司新聞室, https://corporate.lululemon.com/newsroom/press-releases/2026/05-18-2026-123025131","as_of":"2026-05-18","affects":["triggers"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"美國證券集體訴訟（SDNY，案號 24-cv-06033）：集體期間 2023-12-08 至 2024-07-24；2026-03-31 法院對被告駁回動議部分准許、部分駁回；2026-05-08 被告提出答辯狀；目前為證據開示階段。","source":"Kessler Topaz Meltzer & Check — lululemon athletica inc. (NASDAQ: LULU) Securities Fraud Class Action, https://www.ktmc.com/new-cases/lululemon-athletica-inc/","as_of":"2026-05-08","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026-09-04 股價單日跌 17.4% 後，BFA Law、Levi & Korsinsky 等律所公告證券詐欺調查（調查公告，所查來源未見新提起的訴狀）。","source":"BFA Law 新聞稿 via GlobeNewswire 2026-09-23, https://www.globenewswire.com/news-release/2026/09/23/3367258/0/en/lulu-stock-notification-lululemon-is-being-investigated-for-securities-fraud-after-growth-issues-disclosed-investors-are-alerted-to-contact-bfa-law.html","as_of":"2026-09-23","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"LULU","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.11,"operating_margin_pct":17.84,"fcf_margin_pct":12.21,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LULU","as_of":"TTM ending 2026-07-31（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"NKE","period":"TTM ending 2026-05-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":42.91,"operating_margin_pct":8.18,"fcf_margin_pct":4.71,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NKE","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ONON","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.82,"operating_margin_pct":13.79,"fcf_margin_pct":13.32,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONON","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"DECK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.8,"operating_margin_pct":22.67,"fcf_margin_pct":20.22,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DECK","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"RL","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":70.27,"operating_margin_pct":16.42,"fcf_margin_pct":11.99,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RL","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"LULU"}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/LULU/LULU_Q2_2027_Earnings_Call_20260903.md）

# Q2 2027 Earnings Call
**lululemon athletica inc.** | Earnings Calls | 2026-09-03

**Operator** (Operator):
Thank you for standing by. This is the conference operator. Welcome to the lululemon athletica inc. Second Quarter 2026 Earnings Conference Call. [Operator Instructions] The conference is being recorded. [Operator Instructions] I would now like to turn the conference over to Howard Tubin, Vice President, Investor Relations for lululemon athletica. Please go ahead.

**Howard Tubin** (Executives):
Thank you, and good afternoon. Welcome to lululemon's second quarter earnings conference call. Joining me today are Meghan Frank, Interim Co-CEO and CFO; and Andre Maestrini, Interim Co-CEO, President and Chief Commercial Officer. 
Before we get started, I'd like to take this opportunity to remind you that our remarks today will include forward-looking statements reflecting management's current forecast of certain aspects of lululemon's future. These statements are based on current information, which we have assessed, but which by its nature is dynamic and subject to rapid and even abrupt changes. Actual results may differ materially from those contained in or implied by these forward-looking statements due to risks and uncertainties associated with our business, including those we have disclosed in our most recent filings with the SEC including our annual report on Form 10-K and our quarterly reports on Form 10-Q. 
Any forward-looking statements that we make on this call are based on assumptions as of today, and we expressly disclaim any obligation or undertaking to update or revise any of these statements as a result of new information or future events. During this call, we will present both GAAP and non-GAAP financial measures. A reconciliation of GAAP to non-GAAP measures is included in our quarterly report on Form 10-Q and in our earnings press release. In addition, the comparable sales metrics given on today's call are on a constant dollar basis. The press release and accompanying quarterly report on Form 10-Q are available under the Investors section of our website at www.lululemon.com. 
On today's call, Meghan and Andre will begin by discussing recent business developments across our regions and the plans and strategies we are implementing to drive improved performance. Meghan will then discuss our detailed Q2 financials, the impact recent trends are anticipated to have on our performance for the remainder of the year and our revised guidance outlook. And then the team will be happy to take your questions. Before I turn the call over to Meghan, I'd like to remind investors to visit our investor site, where you'll find a summary of our key financial and operating statistics for the second quarter as well as our quarterly infographic. Meghan, over to you.

**Meghan Frank** (Executives):
Thanks, Howard. Welcome, everyone, and thank you for joining us. I want to start the call by taking you through our Q2 results, what we're seeing in the business today and how this is informing our decision to lower our guidance for the full year. Then Andre and I will spend most of our time discussing North America and China Mainland, what's happened since our last earnings call and the actions we are taking across these markets to improve the trajectory of the business. 
As you recall, we began the year with an action plan focused on three pillars: product creation, product activation and enterprise enablement. A key objective of our plan is to strengthen our full price sales trajectory and position the company for long-term growth. In Q1, we saw some encouraging signs indicating we were moving in the right direction to strengthen performance in North America while continuing to expand our global growth engine. 
As we moved into Q2, we faced negative commentary in the media and social channels, which impacted traffic, and softer-than-planned response to some new product launches, which contributed to a moderating sales trend. As you've seen from our press release, Q2 revenue came in below our expectations with the shortfall driven predominantly by China Mainland, where revenue grew 4%. North America finished down 8% for Q2, slightly ahead of our guidance. 
As we move into Q3, while we are seeing good guest reaction to our activations and some of our newer styles, the overall response to our product launches remains inconsistent. And we've continued to see pressure on the brand in both of our largest markets. Based on our assessment of these current trends, we've updated our guidance for the remainder of the year. At the enterprise level, we have several key actions underway to improve our performance. Andre and I will get into the regional detail in a moment. 
Our product teams are chasing into strong performers, including our Groove and Define styles, more aggressively than in the past and working with vendors to strategically manage future inventory flows. On brand, we are moving forward with our increased marketing investments in the back half of the year. We're seeing strong community engagement with our recent campaigns and activations. And while we haven't yet seen an impact on the top line trajectory, we are encouraged by the response. 
And on expenses, we've been continuing to drive efficiency across the organization. Given current trends, we've heightened that focus in the back half of the year while protecting investments in product and brand. We're excited our incoming CEO, Heidi O'Neill, joins us next week. And we expect she will take a deep dive into the business, evaluating our strategy and current action plans. And we look forward to the fresh perspective she will bring to define the path forward for lululemon's next chapter. In the near term, our teams remain focused on execution. 
As we look to the future, we remain confident in the underlying strength of lululemon's brand, the connection we have to our highly engaged community of guests and ambassadors, and the equity we have built. We believe our greatest opportunity is to build on this foundation through continued investment in product innovation, reinforcing our premium positioning, and the long-term brand health. At the same time, our strong financial position allows us to invest in near-term actions that support full price sales and top line improvement while remaining focused on the significant growth opportunities ahead. 
I'll now share an update on our action plan and then hand it over to Andre to discuss regional performance. The markets we operate in are competitive, which makes it imperative for us to focus on unique and innovative ways to inspire our guests. As you know, we've been working on this through our action plan with a focus on product and brand. We anticipated our plan would take some time to gain traction as we bring in new innovations, elevate our store and digital experience, and increase and redirect our marketing spend. But we expected a better response than we are seeing as we enter the second half of the year. 
So let me share some details, starting with product. As we've stated on prior calls, a top priority for the management team is returning to full price sales growth as we focus on restoring and protecting our brand health for the long term. Despite the headwinds we are experiencing, we are moving forward with our actions in this area, which will include bringing updates to our core franchises, introducing new styles, overall SKU reductions and tightly managing inventory levels. In addition, we are leaning into our chase capabilities. As we discussed on prior calls, faster chase times allow us to read and react to guest demand and get back into certain strong-performing styles more quickly. We're chasing approximately 20% more volume this year relative to last year. 
In Q2, while we're seeing green shoots in product, particularly within some of our newer away-from-body bottoms for women, we are also seeing an inconsistent performance in our assortment overall. This included a greater-than-expected slowdown in some of our core categories, particularly leggings. In women's tops, guests are responding well to Scuba and Steady State, now offered in our SuperLoft fabric, and our Define franchise continues to perform well. In men's, we are seeing strength in Metal Vent Tech tees and our golf tops, supported by the storytelling campaigns we developed around some of our elite ambassadors, including Lewis Hamilton and Min Woo Lee. We're also pleased with the halo effect designed-for-golf tops are having on our ABC bottoms as they pair well together and provide guests with a versatile and technical solution on the golf course. 
Let me now spend a moment on our women's bottoms business, where performance has been mixed. Leggings trends so far this year have been below our expectations, with sales declining approximately 20% in Q2. While we have been planning into lower legging sales, and we are seeing good traction in several of our away-from-body styles, we are not yet able to fully offset these declines. Leggings remain an important category for us, where we remain the market leader. The wellness trend is strong. We continue to be a leader in technical fabric development, and guests continue to purchase our leggings for their exercise and training needs, particularly yoga and Pilates. We remain committed to the category, but there are shifts occurring with guests looking for away-from-body silhouettes. 
We're happy with the performance of several new away-from-body styles we've recently introduced, including the Groove Wide-Leg, the Align Foldover Jogger, the Breezily and our updated Dance Studio Pant. All are trending well, and we expect momentum to build in the back half of the year and into 2027. As we look at the second half of the year, in addition to away-from-body bottoms, we'll continue to focus on new and updated styles across our activities. You'll see updates across run with new cold weather innovations in outerwear featuring Wunder Puff and our Featherweight Down franchise, and a new version of our popular Big Cozy, to highlight just a few. I also wanted to mention accessories, where we experienced a 13% decline in Q2. While backpacks are strong, we are seeing overall softness in bags. In addition, we are strategically editing the overall accessories assortment to better align with our go-forward vision for the brand. 
Moving now to product activations and marketing. We are working to strengthen brand relevance, desirability and demand by engaging more directly with guests through social channels and differentiated community experiences while using those platforms to tell richer stories about our brand, products and innovation. We held several successful events in Q2 and into Q3, and engagement levels are encouraging. Let me highlight 2. In June, we celebrated our foundation in yoga with the launch of our summer series. We partnered with leading yoga, Pilates and sculpt instructors to bring free classes to tens of thousands of guests across 70 cities in the U.S. and Canada. 
More recently, in August, we brought back our SeaWheeze Half Marathon and Festival for the first time since 2019. The reaction from guests, the local community and across social media was outstanding. Nearly 10,000 runners from 24 countries ran the half marathon, and approximately 14,000 attendees joined us for an evening of movement and music headlined by DJ John Summit. This event brought incredible energy to our hometown market of Vancouver, and through our virtual SeaWheeze challenge on Strava, we extended participation well beyond race weekend with more than 85,000 participants from 120 countries around the world. 
Based on the strong response, we already made the decision to bring back SeaWheeze again next summer. Guest engagement in events like this demonstrate the passion for our brand and the strength of our connections with the communities we serve. We are increasing our marketing investment in the back half of the year to drive improved brand heat, guest acquisition, traffic and overall top line performance. We are investing more heavily in mid-funnel creator and social content to build relevance, engagement and product consideration. One recent example is our YouTube series featuring some of our elite athletes. We remain confident these investments will help to reignite our sales trends over time as we continue to elevate our product and marketing execution. 
Let me now speak to our enterprise enablement and cost management initiatives. We've been reducing our expense base and working across the enterprise to operate as efficiently as possible. Given current top line trends and our expectations for the back half, we are taking an even more aggressive stance on expense management. Our ongoing initiatives continue: efficiencies across our supply chain and non-merchandise procurement, and implementation of new technologies, including AI-powered systems and automation. On discretionary spending, we are driving new efficiencies across travel, professional fees, store labor hours and head count growth moderation. 
On real estate, we continue to scrutinize every deal across all new store openings and optimizations. We're now planning approximately 35 net new store openings this year, down from our guidance of approximately 40 last quarter. And our plans call for a significant reduction in pop-up stores from 65 at the end of last year to approximately 40 by the end of 2026. We're being intentional with our cost management strategies and looking to drive enduring efficiencies beyond this year. We won't take steps that will negatively impact the brand or our long-term growth potential, but we recognize that current top line trends necessitate a smaller expense profile, and we are acting accordingly. We know there is much more work to be done. Our management team leaders and employees are focused on serving our guests and executing initiatives to drive an inflection in our business. Now let me turn it over to Andre to discuss regional performance in more detail. Andre?

**Andre Maestrini** (Executives):
Thanks, Meghan. It's good to be here with you today to discuss our results and the work underway across the business. While we are focused on improving the trajectory of the business in the short term, we are also making the appropriate decision to strengthen our foundation and drive more sustainable growth over the medium and long term. Let me provide more details about our regional performance beginning with North America. In Q2, revenue declined 8%, slightly ahead of our expectations. In the U.S., we saw a decrease of 8%, while in Canada, revenue was down 11% on a reported basis and down 9% on a constant currency basis. Meghan already spoke to our global product and brand initiatives that we expect will benefit all regions. 
So let me spend a few moments updating you on our strategies to enhance the guest experience in store and online. We are seeing good results in our store, where we are implementing new ways to elevate the guest experience through updated fixture packages, further reductions in SKU density and increased localization of assortment. We're also better organizing the guest journey by changing product adjacencies and merchandising by activity. In digital, we have a sharp focus on storytelling and driving conversion when guests visit our e-commerce sites. We recently redesigned our homepage as well as category detail page. And in the next few weeks, we will be updating also our product detail page. 
Shifting now to China Mainland. As Meghan mentioned, we have seen several issues impacting brand sentiment and product in China, which have hurt traffic and overall sales momentum. This began with spikes of negative commentary in the media and on social channels at the end of Q1 and early Q2, and was compounded by the additional commentary post our Q1 call related to an event we held on the Great Wall of China. These factors have contributed to softness in both our store and digital channels. Performance in e-commerce further impacted by a decision made by Tmall not to anniversary their 618 event in the same way as last year. In addition, we did not participate in promotions following this event. 
In Q2, revenue increased by 4% on a reported basis and declined 2% on a constant currency basis, well below our expectation. As you know, we've experienced rapid growth in China Mainland over the last several years. But while we are disappointed with the current performance in the region, we are focused across both product and brand efforts to drive inflection. And we remain confident in our teams, our strategy, the underlying strength of our brand and the opportunity China Mainland continues to hold for lululemon's future. End of Q2, we were pleased with the guest response to our Together Feels Better campaign. This featured both in-store and online moments, with the highlight being a live stream event simultaneously broadcast across 5 platforms. We featured lululemon ambassador and world champion swimmer, Wang Shun, along with other athletes to bring to life our campaign message. 
And we are building further our credibility in tennis, and we're excited to celebrate with lululemon ambassador, Guo Hanyu, the first Chinese athlete in our ambassador roster to win a Grand Slam tennis title during Wimbledon. Looking ahead, we will strengthen our brand narrative and messaging through a multilayered approach, including key new store openings with associated activations, partnering with Tmall for a Super Brand Day event, and leverage our thought leadership in the well-being space with an event for World Mental Health Day. This moment and the guest engagement we continue to see with these campaigns and activations show the underlying strength of lululemon in the market and the potential that exists for us in China Mainland. 
Next, I will spend a few minutes on our Rest of the World segment, comprised of EMEA and APAC. In total, Q2 revenue in Rest of the World increased 5% on a reported basis and 6% in constant currency. Let me share a few more details, beginning with South Korea. This market continues to be one of our strongest across the globe, and we were excited to celebrate our 10th anniversary in August. We reopened our first-ever store in this market with our new design concept and hosted a special evening event and a series of movement classes attended by guests and ambassadors. 
In Australia, our top line performance has been impacted as we've seen the market grow increasingly promotional. As we are not joining in with promotional events, we have seen a slowing in guest purchase behavior, but we continue to see strong guest engagement with our events, with a recent example being our Sydney Marathon activation. In Japan, while the market is still experiencing reduced traffic of tourism, our brand remains strong. We recently opened our largest store in APAC in Tokyo, Harajuku district, and it's seen a great response from guests. 
And lastly, in EMEA, while our Middle East franchise business continues to be impacted by the conflict in the region, as does tourism in Europe, we remain excited about our potential in the region. Beginning last week, we launched our first marketing collaboration with the online leader, Zalando, across 12 markets in Europe, and we'll be showing up in unique ways at the Berlin Marathon later this month. And we continue to expand our presence through recent franchise store openings in Athens, Greece, and in Bucharest, Romania. This market expansion speaks to the still untapped demand for our brand in new markets as we look at our longer-term plans. I will now hand it back to Meghan to share more details about our financial performance.

**Meghan Frank** (Executives):
Thanks, Andre. Let me now get into the Q2 financial review and our updated guidance outlook. For Q2, total net revenue decreased 4% or 5% in constant currency to $2.4 billion and comparable sales decreased 10%. Within our regions and channels, results were as follows. North America revenue decreased 8% with comparable sales down 12%. By country, revenue decreased 11% or 9% in constant currency in Canada and decreased 8% in the U.S. China Mainland revenue increased 4% or decreased 2% in constant currency, with comparable sales decreasing 8%. And in our Rest of World segment, revenue increased by 5% or 6% in constant currency with comparable sales decreasing 3%.
In our store channel, total sales decreased 6%, and we ended the quarter with 825 stores globally. Square footage increased 11% versus last year, driven by the addition of 41 net new lululemon stores since Q2 of 2025. During the quarter, we opened 9 net new stores and completed 12 optimizations. In our digital channel, revenues decreased 6% and contributed $0.9 billion of top line or 39% of total revenue. And by category, men's revenue decreased approximately 1% versus last year, and women's decreased 4%, while accessories and other declined by 13%.
Gross profit for the second quarter was $1.46 billion, or 60.5% of net revenue, compared to 58.5% in Q2 2025. Gross margin increased 200 basis points compared to last year and was driven primarily by the following: 560 basis points of benefit from IEEPA tariff refunds, a 150 basis point decline in overall product margin driven predominantly by tariff impact and markdowns. Tariffs, exclusive of the refund, had a gross negative impact of 160 basis points in the quarter, offset by 100 basis points related to our enterprise efficiency initiatives.
Markdowns increased 70 basis points. Deleverage on fixed costs was 230 basis points, driven by ongoing investments in our store fleet and regional mix and additional fulfillment costs as we optimize our North America DC network. Foreign exchange had 20 basis points of favorable impact. Excluding the tariff refund, gross margin was 50 basis points better than our guidance for a 410 basis point decline, driven by 40 basis points related to the reversal of an incentive compensation accrual and favorable channel and category mix, offset by slightly higher markdowns.
Moving to SG&A. Our approach continues to be grounded in prudently managing our expenses while also strategically investing to strengthen our foundation and position lululemon for future growth. SG&A expenses were approximately $1.01 billion, or 41.7% of net revenue, compared to 37.7% of net revenue for the same period last year. The increase of 400 basis points relates to fixed cost deleverage, continued investment in guest experience, including store labor hours, marketing spend and fees related to the proxy contest. These were partially offset by an incentive compensation accrual reversal and our ongoing initiatives to prudently manage costs across the enterprise.
Relative to our guidance for SG&A deleverage of 500 basis points, the improvement was driven by lower incentive compensation and additional actions to manage costs across the business. Operating income for the quarter was $454 million, or 18.8% of net revenue, compared to 20.7% of net revenue in Q2 2025. This result includes $134.5 million pretax benefit from IEEPA tariff refunds, which added 560 basis points to operating margin. Tax expense for the quarter was $138.1 million, or 29.6% of pretax earnings, compared to an effective tax rate of 30.5% a year ago. The decrease was primarily due to a decrease in nondeductible expenses in international jurisdictions partially offset by adjustments upon the filing of income tax returns. 
Net income for the quarter was $329 million, or $2.92 per diluted share, compared to $3.10 for the second quarter of 2025. Tariff refunds and associated interest, net of tax, contributed $0.86 to EPS. Capital expenditures were approximately $150 million for the quarter compared to approximately $178 million in the second quarter last year. Q2 spend relates primarily to investments to support long-term business growth including our multiyear distribution center project, store capital for new locations, relocations and renovations and technology investments.
Turning to our balance sheet highlights. We ended the quarter with $1.4 billion in cash and cash equivalents and nearly $600 million of available capacity under our committed revolving credit facility. Inventory at the end of Q2 is $1.7 billion, a decrease of 1% on a dollar basis. On a unit basis, inventory decreased approximately 7%. The difference between dollar inventory growth and unit inventory growth relates predominantly to higher tariff costs and foreign exchange. We repurchased approximately 2.7 million shares at an average price of $120.
Let me shift now to our guidance for Q3, which has gotten off to a slow start. While we are working hard to change the trajectory of the business and adapting our action plan in light of current trends, we're taking a prudent approach to our outlook for the second half of the year. At the highest level, our revenue guidance for the second half assumes a slower trend relative to Q2 in our North America business and performance relatively consistent with Q2 trends in international. And while our teams remain hard at work executing our plans across product, brand and guest experience, and we strive to do better, we have not factored this potential into our financial outlook.
For Q3, we expect revenue in the range of $2.29 billion to $2.32 billion, representing a decline of 10% to 11%. We expect to open approximately 17 net new company-operated stores and complete 15 optimizations. By region, on a reported basis, we expect North America to decline in the mid-teens, with the U.S. also in that range, and Canada lower. We expect the China Mainland and the Rest of World to increase 3% to 5%. We expect gross margin in Q3 to decrease approximately 250 basis points compared to Q3 of 2025. While we expect an improvement in product margin, this will be offset by deleverage on fixed costs and ongoing investment in store openings, optimizations and our distribution network.
When looking specifically at markdowns, we expect an increase of approximately 60 basis points versus last year. While we continue to focus on improving full price selling, the slower-than-expected top line trends will necessitate additional seasonal clearance. In Q3, we expect our SG&A rate to deleverage by 800 basis points relative to Q3 2025. This increase will be driven primarily by deleverage associated with lower sales than initially expected, increased marketing and expense timing versus last year. And we will continue to invest strategically in our growth initiatives in IT infrastructure. When looking at operating margin for Q3, we expect it to be approximately 6.5% versus 17% in Q3 2025 for the reasons I just mentioned.
Turning to EPS. We expect earnings per share in the third quarter to be in the range of $0.93 to $0.98 versus EPS of $2.59 a year ago. We expect our effective tax rate in Q3 to be approximately 30%. When looking at inventory at the end of Q3, we expect dollar growth to be in the low single-digit range with units down slightly.
Turning to our full year 2026 guidance outlook. We now expect revenue to be in the range of $10.35 billion to $10.5 billion, down 5% to 7% relative to 2025. By region, we now expect revenue in North America to be down in the low double digits, with the U.S. also in that range, and Canada slightly lower. We now expect revenue in China Mainland to be up in the high single digits. And in Rest of World, we now expect revenue to increase in the mid-single digits. Globally, we now expect to open approximately 35 net new company-operated stores in 2026 and continue to expect to complete approximately 35 optimizations. This will contribute to overall square footage growth of approximately 10%. Our new store openings in 2026 will include approximately 10 stores in North America, including 7 in Mexico and approximately 25 in our international markets.
For the full year, we now expect gross margin to decrease approximately 80 basis points relative to last year. We expect an improvement in product margin driven by a 130 basis point positive impact related to the Q2 tariff refund plus ongoing benefits from our mitigation strategies. These benefits are expected to be offset by deleverage on fixed costs and ongoing investment on our new store openings, optimizations and our distribution center network. When looking at markdowns, we expect an increase for the full year of 40 basis points. When looking at tariffs more closely for the full year, our guidance now assumes a rate of 10% to 12.5% through September, and we continue to assume a rate of 20% for the remainder of the year. In addition, while we continue to participate in the refund process, our guidance assumes no additional recovery of tariffs paid under IEEPA.
Turning now to SG&A for the full year. While we intend to realize significant savings related to the enterprise enablement pillar of our action plan, we now expect an increase of approximately 450 basis points versus 2025. This will be driven by increased deleverage associated with our updated view on top line, increased marketing spend and continued strategic investments in our business to support future growth, including market expansion and improving the guest experience by enhancing our omni capabilities. When looking at operating margin for the full year 2026, we now expect it to decrease by approximately 530 basis points versus last year, which includes the 130 basis point benefit from tariff refunds recognized in the second quarter.
For the full year 2026, we expect our effective tax rate to be approximately 30% versus our 2025 effective tax rate of 29.5%. For the fiscal year 2026, we now expect diluted earnings per share in the range of $9.48 to $9.73 versus EPS of $13.26 in 2025. This updated range includes an $0.86 benefit from tariff refunds recognized in the second quarter but does not include the impact of any potential additional refunds through the balance of the year. Our EPS guidance also excludes the impact of any future share repurchases. 
When looking at inventory, we expect dollar growth to be up in the mid-single-digit range with units approximately flat. At the end of Q2, we had approximately $713 million remaining on our share repurchase program, which we will continue to utilize. Share repurchases remain our preferred method of returning cash to shareholders, and we continue to expect our repurchase levels in 2026 to be in line with 2025. Finally, for the full year, we now expect capital expenditures to be approximately $680 million to $700 million. The spend reflects investments to support business growth, including capital for new locations, relocations and renovations, DC and technology investments.
Before we take your questions, I want to emphasize that we know there is significant work ahead for us. We're applying what we're learning this year to how we operate globally going forward. Our teams are executing against our action plan now, chasing into what's working, investing into brand and community and running a tighter expense base. Andre and I are confident in our leadership teams across every market, and we believe that with the right adjustments to our product assortment, marketing and community activations, improved revenue trends will follow. 
One thing is certain to me, our brand has real opportunity ahead of it. We've seen this with a response to SeaWheeze and engagement with our campaigns and in the strength of our teams around the world. We know our guests continue to love the brand, and we need to consistently give them the product and experience they can expect from lululemon. And as Heidi joins us next week, I'm confident that she'll help us realize this opportunity. Finally, I want to thank the leaders and employees of our company for their determination to make progress every day and for operating in a way that's consistent with our values as we innovate for our guests. Operator, we'll now take your questions.

**Operator** (Operator):
[Operator Instructions] The first question comes from Alex Straton with Morgan Stanley.

**Alexandra Straton** (Analysts):
Can you just talk about, from a strategic perspective, like where you're at in your journey with stores and reducing SKUs and making it a better experience, and any fleet rationalization considerations going forward? I know you took the targets down. But as you think about it, bigger picture and longer term.

**Meghan Frank** (Executives):
Great. Thanks, Alex. I'll give some details on just stores overall, and then Andre is going to provide a little bit of color. So in terms of stores, we were scrutinizing every deal. We're opening 35 net new stores this year. About 10 of those net new stores in North America, 7 of those are in Mexico. Of the openings, we've got in North America, about half of them are pop-up conversions where we've got evidence of strong productivity. And then the balance would be strategic presence and then key market saturation. So we'll continue to take that posture as we move throughout '27 as well, really scrutinizing every deal. And then I'll pass it to Andre to provide more color.

**Andre Maestrini** (Executives):
Yes, absolutely. And what -- to really enhance the guest experience in our stores, specifically in North America, we have made several enhancements to premiumize this experience. It includes a less dense presentation, so we decreased SKUs by 15%, and now we are rolling it out in the rest of the fleet. We'll have a sharper focus on merchandising and VM, and we've seen that organizing the store by activities on one side and lifestyle has improved the storytelling and the engagement of the guest to the range. And in addition, we have a smaller subset of doors where we are testing additional enhancements that include further SKU reductions, more curated assortment based on local taste and preferences, new fixtures packages and also using more imagery and activity mannequins. So once the formula is nailed, we will scale it to the rest of the fleet.

**Alexandra Straton** (Analysts):
Maybe just one quick follow-up on your promotion comments and how you guys not being promotional is potentially impacting you. Is that a global phenomenon or in certain markets? And also, is it in certain categories?

**Meghan Frank** (Executives):
Yes. I think what Andre was referring to was in certain markets where we're seeing them be more promotional, for example, Australia, and we are not participating in those promotions. I would say, overall, our goal has been to return to a healthy, full price penetration of business. Clearly with revenue not where we expected this year, we have more seasonal product to clear through by year-end, and that's reflected in our guide. So it's not promotions driving that. It's seasonal clearance primarily at end of season.

**Operator** (Operator):
The next question comes from Ike Boruchow with Wells Fargo.

**Irwin Boruchow** (Analysts):
I'm not sure if this is for you, Meghan, but I kind of wanted to ask a bigger picture question about the cost structure of the business. Given the underperformance on top line and the fact that it doesn't feel like that's been fully diagnosed yet, the deleverage you guys are seeing is kind of indicative of a model that is built to be comping fairly positive. How quickly can you adjust the cost structure? And I don't know if that's getting out of leases or looking at the store base. But just curious the timing of that, because if the top line trajectory doesn't turn in the next couple of quarters, it just feels like this could get a bit messier as you kind of get into next year. So just curious, your thoughts.

**Meghan Frank** (Executives):
Thanks, Ike. Yes, as I mentioned, we are in action on the cost side. We have had an active work stream in cost management throughout this year, really focused on supply chain, procurement, technology. We have taken some near-term steps to manage discretionary expense. So across some of the buckets I mentioned, like travel, professional fees, store labor hours, moderating head count growth. I would say given current trends, we are taking a deeper look to rightsize the cost base to the current business, with the -- still protecting the long-term trajectory of the business and really primarily product and brand, where we feel like we really need to move on the sentiment side as well as support our product engine moving into '27. So I think too early to share beyond the guidance that we shared for '26, but we are taking a hard look across all aspects of our business model.

**Operator** (Operator):
The next question comes from Matthew Boss with JPMorgan.

**Matthew Boss** (Analysts):
So Meghan, on the sequential softening in Mainland China and Rest of World, how much do you attribute to macro relative to product assortment? And can you elaborate on August trends? Or just what gives you confidence in the third quarter as the trough?

**Meghan Frank** (Executives):
Yes. So in terms of China, I would say we're really looking at primarily brand noise impacting brand sentiment as well as a softer 618 Tmall event that Andre mentioned. And then we are seeing across the globe, newness not perform at expectations. So I would say macro has been challenging in China for some time. We're not pointing to macro specifically as a key issue. As we look to the second half, I would say our quarter-to-date trend does support how we've looked at the international business towards the back half of the year as well as China. And maybe I'll ask Andre to add a few more details on how we're actioning China in the second half.

**Andre Maestrini** (Executives):
Yes. In China, we are really focusing on implementing continuous activations of the brand. Just in the upcoming weeks, we'll have new store openings with the associated activations in key location of top Tier 1 cities. We also are conducting a Super Brand Day around our outerwear and Wunder Puff icon, so a big activation there. And also, early October, we are leveraging our leadership in World Mental Health Day activation to keep positioning our brand on wellness. That's the underlying trend there. So all that to counter this initial negative noise that Meghan refer in Q2.

**Matthew Boss** (Analysts):
And Meghan, just as a follow-up on the 12% comp decline in the Americas in the second quarter and the inconsistency that you cited, are there any green shoots that you've seen in August with product newness now restored to your targeted levels?

**Meghan Frank** (Executives):
Yes. I would say August, as reflected in our guidance, has gotten off to a bit of a slow start. That said, we are seeing some green shoots in product, particularly in our away-from-body assortment, including our Groove Pant, Align Foldover Jogger, new Dance Studio. We're also reordering into some silhouettes of Define. We've got a new Scuba offering that's launched and Steady State that's doing well. So what we've reflected in our guidance is what we're currently seeing in the trend. But we are aggressively, as we've mentioned, reordering into what's working and any upside from that would not be reflected.

**Operator** (Operator):
The next question comes from Lorraine Hutchinson with Bank of America.

**Lorraine Maikis** (Analysts):
Understanding that most of your leases are signed for this year, as you look out into next year, are you pausing any of your store opening plans for China or store expansions in the U.S. until you can stabilize those businesses?

**Meghan Frank** (Executives):
Thanks, Lorraine. I would say we're taking a very measured approach to store expansion. So China, I would say we still see tremendous opportunity from a market expansion standpoint there in terms of square footage and store footprint, and we are taking a hard look at that, obviously, given business trends, but taking a long-term view of the opportunity in that market. 
In North America, as I mentioned, we just have a handful of new store openings this year, half of which are pop-up conversions, where we've really tested that market, and it has productivity that supports a full-time location. And then, in addition to that, we just have a handful of strategic stores where we feel we need a presence in that market, whether that's a new location or a saturation of an existing market that's performing well. I would say we're taking that approach into '27, and we're just taking a hard look at everything, given current performance of business, and we will share more about how we see square footage growth for '27 when we give guidance in March.

**Operator** (Operator):
The next question comes from Michael Binetti with Evercore.

**Michael Binetti** (Analysts):
Meghan, I think just a quick one on the model, your guidance. I think, if I got my math right, implies a slight improvement in markdowns sequentially from 2Q in each quarter. Are you -- can you just talk us through how you think the seasonal clearance mix will go? Does that roll off by the end of 3Q? And then maybe in China, if we could get a sense of the monthly cadence, given your comments around some of the Tmall event 16 -- 618, sorry. If the macro persists there, or if the brand issues persist there, is the right thing to do for the brand? Or how are you thinking about whether you'd refrain from promoting again as we get into some of those next Tmall windows, like some of the bigger ones in November?

**Meghan Frank** (Executives):
Thanks, Michael. So in terms of markdowns by quarter, we were up 70 basis points year-over-year in Q2. We're expecting 60 basis point increase in Q3, so a slight moderation. And then we are against -- up against a high water line in Q4. So we're expecting markdowns to be approximately flat in the fourth quarter and then 40 basis points up for the year. So that's the shape of that, and it is based on seasonal clearance of goods that haven't moved during '26. In terms of China, we saw some pressure in May. It subsided to some degree in June, and we also saw more pressure in July. And then I'll ask Andre to just comment on Tmall.

**Andre Maestrini** (Executives):
Yes. We're definitely with a hyperfocus on regular price increase in China, and I think we had a healthy performance there. So we continue to use Tmall. It's shop-in-shop, and it's not promotion related. When I refer to the Super Brand Day, it's a full price event on our icons, which is the Wunder Puff to launch our outerwear season. And looking for the end of the quarter and beginning Q4, the 11/11 event, we will just participate as normal to anniversary our previous year's business that we've been doing last year.

**Operator** (Operator):
The next question comes from Paul Lejuez with Citi.

**Paul Lejuez** (Analysts):
Curious, at a high level, if you think you've got a traffic problem that can be solved by increased marketing? Or would you say that you have more of a product problem that requires a little bit more adjustment and time? And how does that answer differ if you think about it region by region?

**Meghan Frank** (Executives):
Thanks, Paul. I would say, predominantly, we're seeing the pressure in traffic. We're also seeing negative year-over-year conversion, but we're not seeing that worsen. So we've really pointed to 2 opportunities. So one being we've seen some pressure on brand heat and sentiment, and we are investing into marketing, and some of the activations that we've had throughout this summer. And then we've got some things in front of us, including currently we're right now at the U.S. Open with an activation. We've got fall marathon season coming up, New York, Chicago, Toronto. We'll have a presence with those. And then we'll continue some of our social activations through new episodes on our content series there. From a conversion perspective, product, we continue to learn from what's working, not working, reordering aggressively into what is working. And so we're looking to move the needle, I would say, on both fronts with those actions.

**Paul Lejuez** (Analysts):
Was that all comment about the Americas? Or was that -- you talking globally, Meghan?

**Andre Maestrini** (Executives):
Yes, I can take for China. The main issue was more the event that impacted the brand sentiment. So the focus there is to restore the consideration of the brand at levels that were prior to these events, and that's the main driver to restore traffic -- organic traffic and bring back the demand we've been experiencing. So we'll have the swing there and the additional work on newness in products will also benefit China. But the first reason is the main focus there, definitely.

**Meghan Frank** (Executives):
I'd say, Paul, the traffic being the biggest driver is across both regions.

**Paul Lejuez** (Analysts):
Got it. And then just market growth by region. How do you view the market that you're playing in, in each region?

**Meghan Frank** (Executives):
Yes. I would say, the market continues to be competitive across all regions. We really need to be differentiated, offering new innovation. So our actions are geared towards the market we're operating in, in both North America and China, and I would say both competitive markets.

**Operator** (Operator):
The next question comes from Adrienne Yih with Barclays.

**Adrienne Yih-Tennant** (Analysts):
I guess my first question is, oftentimes when you get into sort of these trends, the first thing you go back to is sort of the customers, what do they want from you? How are they thinking about the brand? So as you do your kind of customer feedback, what are you finding out about the current customer today and what they need from the brand? My second question is, a lot of the fixes that we're talking about today, stores, are sort of at the end of the process, like what do we do about inventory today? Can you talk to us about how you're thinking about the innovation process, the development process, lead times and kind of from the origin, right, what's different about that product development process?

**Meghan Frank** (Executives):
Thanks, Adrienne. So I would say in terms of guest feedback, we certainly use that to inform our actions. So we have been doing some consumer research, and I would say what we're hearing is they're looking for new and differentiated product from us, innovation. And they are also looking for those community engagements that we offered, and some of the examples that I provided this summer really show some momentum in that engagement, including SeaWheeze, at the level of 10,000 runners -- sorry, 85,000 Strava participants, really some positive momentum in terms of engagement with the brand as well as our summer series. So I would say we are really embedding what we're hearing from our guests into that action plan. 
And then in terms of our pipeline, we have made some improvements, as we've mentioned, to our go-to-market process to reduce lead times. So that is underway. I think that will continue to improve over time as well as we've really leaned into our chase capabilities. We are reordering into about 20% more than last year. So we've really augmented our capabilities there. And then also from a fast track design perspective, looking to get back into product, with a faster lead time from a design to market perspective as well. So certainly looking at improving that over time.

**Adrienne Yih-Tennant** (Analysts):
Okay. And then my follow-up is, on the marketing, you talked about increasing some marketing investments in the back half of the year. Just wondering, if you don't know that the product is kind of really kind of resonating, are those marketing kind of higher level? Are they more social? Can you talk about like how that return on that advertising spend, how you're considering that going into that period?

**Meghan Frank** (Executives):
Yes. I would say given the challenges we've seen with -- from both the brand heat and product perspective, we do feel strongly that we need to continue to keep our investment level in marketing. I would say we're looking at more mid-funnel, top-of-funnel activations, community engagement, things such as what I've mentioned in terms of SeaWheeze, summer series, going after fall marathon season, our U.S. Open activation, the content series as well as social. So it's definitely brand building marketing efforts.

**Operator** (Operator):
The next question comes from Dana Telsey with Telsey Group.

**Dana Telsey** (Analysts):
As you talk about the product and the response to some of the new product that are out there, Meghan, you had mentioned in the prepared remarks a little about adjustments are being made. What are you seeing in response to the new product for men's, women's tops and bottoms? I know you talked about leggings for women's down 20%. What adjustments do you see need to be made? What's the time line of them being made and did pricing factor into any of it? And then I have a follow-up.

**Meghan Frank** (Executives):
Thanks, Dana. So in terms of what's working today, away-from-body, I mentioned is working, Define, Scuba are working. We did see some positive reception to our golf assortment and some attachment to our ABC Pant. We are experiencing some other new products that are not resonating as well, so we're adjusting to that and reordering what is working. And then we've also seen some decline, greater than we expected in some of our core categories, including leggings that we mentioned. And there, it's also relevant that we're shifting into away-from-body. We've really seen some positive response to that, and the shift has been happening over time but was a little more than we expected in Q2. So we're chasing into that. And overall bottoms trends are down in the mid-single digits. So we're offsetting to a degree, but not entirely. So we're looking to improve our position in away-from-body over time.

**Dana Telsey** (Analysts):
Got it. And then when you think about channels, stores and online, is there at all a difference in the performance of stores and online and traffic patterns to each for the brand?

**Meghan Frank** (Executives):
I'd say we've overall seen traffic pressure in both channels as well as some conversion pressure in both channels as well. So it's been relatively consistent, I would say, in terms of where we've seen the impact and really connects back to our priorities of getting after brand sentiment with some of the activations we have planned as well as some conversion actions we have, both in product and in improvements we're making there. And then some of the experience pieces that Andre spoke to in terms of store shopability and as well as the e-commerce enhancements we've made to the look and feel of our website.

**Operator** (Operator):
The last question comes from Mark Altschwager with Baird.

**Mark Altschwager** (Analysts):
Meghan, just one more on the shape of the year for the guide. Just backing into Q4, I think the revenue trends imply pretty similar, but you are baking in less margin pressure. Could you just help bridge that for us? I know you said you expect the promotion piece to get a little bit better, but what are the other factors we should be considering there, like with the cost actions that you outlined and other factors? And then I have a follow-up.

**Meghan Frank** (Executives):
Yes. Thanks, Mark. Yes. So for Q4, we're expecting around 250 basis points in operating margin pressure. So it is moderated from Q3. We are expecting to see gross margin slightly ahead of last year, and that's really driven by, first of all, we have a higher water line from a revenue perspective in Q4, so less fixed cost deleverage. We also have a tariff benefit. So more of our mitigation actions come into play as we move throughout this year. So we're seeing an accelerating benefit there and essentially flat markdowns and where we've got some pressure in Q2 and Q3. And then from an expense perspective, we will still have deleverage, but it will be much less, I would say, than Q3.

**Mark Altschwager** (Analysts):
Okay. And then on tariffs, the Q says you've paid about $230 million in IEEPA tariffs. You've received $135 million back. I guess, what's the process and the realistic timing on the remainder? And is there a reason you wouldn't ultimately receive the rest back?

**Meghan Frank** (Executives):
Yes. So we did receive $134 million back in Q2. We have not reflected the remaining $105 million in our forward guidance. There remains some uncertainty in the process that we are actively participating.

**Operator** (Operator):
That's all the time we have for questions today. Thank you for joining today's call, and have a nice day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LULU_Q1_2027_Earnings_Call_20260604.md
- 2026-06-04｜Meghan Frank｜guidance：CFO 給第二季營收財測 $2.45B–$2.475B，年減 2%–3%（減幅在同一句後半）。（原話："revenue in the range of $2.45 billion to $2.475 billion"）
- 2026-06-04｜Meghan Frank｜guidance：第二季 EPS 財測 $1.76–$1.81，去年同期 $3.10。（原話："in the range of $1.76 to $1.81 versus EPS of $3.10"）
- 2026-06-04｜Meghan Frank｜guidance：第二季北美預期低雙位數下滑，美國同區間。（原話："North America to decline in the low double digits"）
- 2026-06-04｜Andre Maestrini｜guidance：Andre 說第二季中國大陸銷售預期中到高十幾% 成長，全年仍約 20%。（原話："we expect sales to increase in the mid- to high teens"）
- 2026-06-04｜Meghan Frank｜guidance：全年營收財測改為 $11.00B–$11.15B（$11B 下緣在前一行），持平至年減 1%。（原話："to $11.15 billion, flat to down 1% relative to 2025"）
- 2026-06-04｜Meghan Frank｜guidance：全年北美改為高個位數下滑；後文說美國略差、加拿大較好。（原話："to be down in the high single digits"）
- 2026-06-04｜Meghan Frank｜guidance：全年中國大陸維持約 20% 成長；Rest of World 維持中十幾% 成長（在後一行）。（原話："revenue in China Mainland to be up approximately 20%"）
- 2026-06-04｜Meghan Frank｜guidance：全年新開自營店改為靠近原 40–45 家區間的低端，最佳化改裝仍約 35 間。（原話："we now expect to be closer to the low end of the"）
- 2026-06-04｜Meghan Frank｜guidance：全年毛利率財測改為年減約 90 bps。（原話："gross margin to decrease approximately 90 basis points"）
- 2026-06-04｜Meghan Frank｜guidance：答分析師時 Meghan 說全年毛利率減幅先前預期是 130 bps（現為 90）。（原話："expectation was 130"）
- 2026-06-04｜Meghan Frank｜guidance：全年 SG&A 費用率財測為年增約 290 bps 的去槓桿。（原話："we now expect deleverage of approximately 290 basis"）
- 2026-06-04｜Meghan Frank｜guidance：全年營業利益率財測改為年減約 380 bps（句首在前一行）。（原話："380 basis points versus last year"）
- 2026-06-04｜Meghan Frank｜guidance：全年 EPS 財測 $10.95–$11.15，2025 年為 $13.26。（原話："in the range of $10.95 to $11.15 versus EPS of $13.26"）
- 2026-06-04｜Meghan Frank｜guidance：口徑說明：EPS 財測不含未來任何股票買回的影響。（原話："excludes the impact of any future share repurchases"）
- 2026-06-04｜Meghan Frank｜guidance：全年存貨金額預期低至中個位數成長，件數略減。（原話："dollar growth to be in the low to mid-single-digit range"）
- 2026-06-04｜Meghan Frank｜guidance：全年關稅對毛利率的毛衝擊約 30 bps，管理層預期幾乎全數可抵銷。（原話："tariffs to have a gross impact of 30 basis points"）
- 2026-06-04｜Meghan Frank｜guidance：口徑：財測假設第二季追加關稅率為 10%，較先前假設的約 20% 下修。（原話："This is down from our prior assumption of approximately 20%"）
- 2026-06-04｜Meghan Frank｜guidance：口徑：下半年財測仍假設追加關稅率 20%。（原話："we continue to assume a 20% incremental rate"）
- 2026-06-04｜Meghan Frank｜guidance：口徑：公司參與退稅流程，但財測不計入 IEEPA 關稅的任何回收。（原話："guidance assumes no recovery of tariffs paid under IEEPA"）
- 2026-06-04｜Meghan Frank｜guidance：答北美問題時 Meghan 說財測沒有計入現行各項措施的任何實質貢獻，措施奏效則區間有上檔空間。（原話："not assuming any meaningful impact from those initiatives"）
- 2026-06-04｜Meghan Frank｜guidance：被問下半年與 90 天前相比：Meghan 說下半年趨勢相對第二季財測是小幅改善。（原話："it's a slight improvement relative to Q2 guide"）
- 2026-06-04｜Meghan Frank｜guidance：Meghan 說北美第二季低雙位數下滑，下半年大致同水準。（原話："and then generally in line in the second half of the"）
- 2026-06-04｜Meghan Frank｜guidance：第二季全價銷售預期整體中個位數下滑。（原話："overall to decrease in the mid-single digits"）
- 2026-06-04｜Meghan Frank｜guidance：全年全價銷售預期持平至略好，並預期逐季推進。（原話："flat to slightly better in terms of full price"）
- 2026-06-04｜Meghan Frank｜margin：第一季毛利率 54.2%，年減 410 bps，其中產品毛利率下降 330 bps。（原話："a 330 basis point decline in overall product margin"）
- 2026-06-04｜Meghan Frank｜margin：口徑：第一季關稅毛衝擊 280 bps，被企業效率專案約 100 bps 抵銷。（原話："Tariffs had a gross negative impact of 280 basis points"）
- 2026-06-04｜Meghan Frank｜margin：第一季固定成本去槓桿 140 bps，管理層歸因於門市投資與區域組合。（原話："Deleverage on fixed costs was 140 basis points"）
- 2026-06-04｜Meghan Frank｜margin：第一季 SG&A 費用率 42.9%（去年 39.8%），增加 310 bps。（原話："The increase of 310 basis points relates to expenses"）
- 2026-06-04｜Meghan Frank｜margin：口徑：第一季 SG&A 增加的成分包含去年砍掉、今年加回的費用（門市工時、獎金）。（原話："expenses that we've reduced last year"）
- 2026-06-04｜Meghan Frank｜margin：口徑：第一季 SG&A 增加成分另含委託書之爭（proxy contest）相關成本。（原話："activations and costs related to the proxy contest"）
- 2026-06-04｜Meghan Frank｜margin：第一季營業利益 $277M，營業利益率 11.2%（去年同期 18.5%）。（原話："Operating income for the quarter was $277 million or 11.2%"）
- 2026-06-04｜Meghan Frank｜margin：第二季毛利率財測年減約 410 bps。（原話："margin in Q2 to decrease approximately 410 basis points"）
- 2026-06-04｜Meghan Frank｜margin：口徑：第二季關稅毛衝擊約 150 bps，抵銷項約 100 bps。（原話："negative impact of approximately 150 basis points"）
- 2026-06-04｜Meghan Frank｜margin：第二季折扣（markdowns）預期年增約 50 bps。（原話："markdowns to be up approximately 50 basis points"）
- 2026-06-04｜Meghan Frank｜margin：第二季 SG&A 費用率預期去槓桿 500 bps。（原話："we expect our SG&A rate to deleverage by 500 basis points"）
- 2026-06-04｜Meghan Frank｜margin：口徑：第二季 SG&A 去槓桿部分來自銷售低於原先預期。（原話："associated with lower sales than initially expected"）
- 2026-06-04｜Meghan Frank｜margin：第二季營業利益率財測約 11.6%，去年同期 20.7%。（原話："approximately 11.6% versus 20.7% in Q2 2025"）
- 2026-06-04｜Andre Maestrini｜margin：Andre 說第二季財測納入較高的季節性清倉。（原話："our guidance assumes higher levels of seasonal clearance"）
- 2026-06-04｜Meghan Frank｜margin：被問下半年折扣假設：Meghan 說第二季是全年折扣高點。（原話："So Q2 will be our high-water mark this year"）
- 2026-06-04｜Meghan Frank｜margin：第四季折扣預期低於去年（去年為折扣高水位）；第三季較第二季逐季改善。（原話："expect markdowns in Q4 to be under last year"）
- 2026-06-04｜Meghan Frank｜margin：口徑：Meghan 說她講的 reg price 等同全價（full price）。（原話："reg price, which is the same in my mind as full price"）
- 2026-06-04｜Meghan Frank｜margin：Meghan 說第一季全球 reg price 增加高個位數。（原話："we saw a high single-digit increase in reg price"）
- 2026-06-04｜Andre Maestrini｜margin：Andre 說北美門市已大幅降低折扣活動。（原話："a significant reduction in markdowns"）
- 2026-06-04｜Meghan Frank｜margin：口徑：存貨金額增 2% 但件數減約 4%，差異主要來自較高關稅與匯率。（原話："predominantly to higher tariff rates relative to last year"）
- 2026-06-04｜Meghan Frank｜margin：被問開發週期縮短的成本取捨：Meghan 說不會把更高產品成本和上市時程掛勾，只提空運取捨。（原話："I wouldn't equate any higher product costs"）
- 2026-06-04｜Meghan Frank｜margin：被問中國毛利／營業利益率：Meghan 說中國營業利益率仍有健康擴張，公司繼續加碼投資。（原話："continue to invest behind that business"）
- 2026-06-04｜Meghan Frank｜margin：企業賦能（enterprise enablement）專案的效益預期要一段時間才會浮現。（原話："we expect to see benefits over time"）
- 2026-06-04｜Meghan Frank｜risk：Meghan 說第一季收尾與進入第二季時出現若干逆風與銷售趨勢放緩。（原話："headwinds and a moderating sales trend"）
- 2026-06-04｜Meghan Frank｜risk：管理層點出的第一個因素：媒體與社群上的負面評論暴增，影響客流與營收。（原話："spikes of negative commentary in the media and on social"）
- 2026-06-04｜Meghan Frank｜product：管理層點出的第二個因素：並非所有新品上市都達預期。（原話："not all of our product launches have met our expectations"）
- 2026-06-04｜Meghan Frank｜risk：被問社群風波成因：Meghan 列出委託書之爭。（原話："had the proxy contest during that period"）
- 2026-06-04｜Meghan Frank｜risk：被問社群風波成因：Meghan 另列四月中對部分產品成分（composition）的質疑。（原話："we had some questions around the composition of"）
- 2026-06-04｜Meghan Frank｜risk：Meghan 說負面報導已退，但趨勢尚未回到風波前水準。（原話："have not yet seen a return to our pre-disruption"）
- 2026-06-04｜Andre Maestrini｜risk：Andre 在中國段說負面評論的暴增現已消退。（原話："spikes of negative commentary, which has now subsided"）
- 2026-06-04｜Meghan Frank｜risk：Meghan 說近期表現正衝擊產品面各個區塊。（原話："recent performance is impacting all areas of our business"）
- 2026-06-04｜Andre Maestrini｜risk：Andre 說中東特許經營受衝突擾動、歐洲與日本觀光疲軟，管理層視為暫時。（原話："We view these as temporary"）
- 2026-06-04｜Meghan Frank｜competition：被問表現相對市場：Meghan 說運動品類趨勢相對穩定，公司自身掉下來。（原話："relative stability in the trend of the athletic space"）
- 2026-06-04｜Meghan Frank｜customer：Meghan 說近 6–7 週的落差主要在客流，其次是轉換率。（原話："primarily in traffic and, to a lesser degree, conversion"）
- 2026-06-04｜Meghan Frank｜customer：被問客流下滑是否集中於特定客群：Meghan 說是全客群的廣泛性減少。（原話："We really did see a broad-based traffic reduction"）
- 2026-06-04｜Meghan Frank｜customer：被問受影響區域：Meghan 說跨區域，以中國與美國受影響較大。（原話："predominantly, I would say China was impacted"）
- 2026-06-04｜Meghan Frank｜customer：Meghan 說美洲第一季下滑 4%，優於原先低到中個位數下滑的預期。（原話："we did see a negative 4% trend in Q1 overall"）
- 2026-06-04｜Meghan Frank｜customer：Meghan 說第一季二、三月最強，趨勢在四月底至五月轉軟。（原話："February and March were our strongest months"）
- 2026-06-04｜Meghan Frank｜customer：第一季北美營收 -3%（固定匯率 -4%），同店銷售下滑 6%。（原話："Comparable sales were down 6%"）
- 2026-06-04｜Andre Maestrini｜customer：Andre 說第一季北美全價銷售相對第四季有序列改善。（原話："sequential improvement in our full price sales"）
- 2026-06-04｜Meghan Frank｜customer：Meghan 說第一季美國全價銷售略為負成長，但相對第四季有實質序列改善。（原話："The U.S. was slightly negative"）
- 2026-06-04｜Meghan Frank｜customer：第一季中國大陸營收 +30%（固定匯率 +23%），同店銷售 +13%。（原話："with comparable sales increasing 13%"）
- 2026-06-04｜Meghan Frank｜customer：口徑：農曆新年移入第一季，替中國成長率加了 8 個百分點。（原話："added 8 percentage points to the growth rate"）
- 2026-06-04｜Meghan Frank｜customer：Meghan 說中國業務在負面評論後已有一定程度改善。（原話："We have seen that business improve to a degree"）
- 2026-06-04｜Meghan Frank｜commitment：Meghan 對中國全年約 20% 的財測表態維持不變。（原話："We are still holding our guide for the year at 20%"）
- 2026-06-04｜Meghan Frank｜commitment：Meghan 說中國全年同店銷售未另行拆分披露。（原話："broken out the full year comp"）
- 2026-06-04｜Meghan Frank｜product：Meghan 說「新瑜珈造型」活動未達預期的營收效果。（原話："new look of yoga campaign didn't drive top line results"）
- 2026-06-04｜Meghan Frank｜product：Meghan 說 Align、Groove 的 away-from-body 款式反應不錯，但未帶動其他品類的光環效應。（原話："the campaign hasn't had the expected halo"）
- 2026-06-04｜Meghan Frank｜product：被問設計檢討：Meghan 說顏色是光環效應不足的一個因素。（原話："think color is an aspect of that"）
- 2026-06-04｜Meghan Frank｜product：追單量今年比去年多 20%。（原話："20% more volume this year relative to last year"）
- 2026-06-04｜Meghan Frank｜product：主線產品開發週期已從 18–24 個月縮短（現為 15–16 個月，見下一行）。（原話："mainline product development process from 18 to 24 months"）
- 2026-06-04｜Meghan Frank｜commitment：管理層正進一步把開發週期縮到 12–14 個月。（原話："working to further reduce it down to 12 to 14 months"）
- 2026-06-04｜Meghan Frank｜product：新品占比目標：全年由去年 23% 拉到 35%（23% 在前一行）。（原話："year to 35% over the course of this year"）
- 2026-06-04｜Meghan Frank｜product：目前新品占比約 30%，會隨季節波動。（原話："Right now, we sit at about 30%"）
- 2026-06-04｜Andre Maestrini｜product：Andre 說北美門市改為較不密集的陳列，SKU 少 15%。（原話："presentation of products featuring 15% fewer SKUs"）
- 2026-06-04｜Andre Maestrini｜product：被問國際市場對新品的接受度：Andre 說核心系列的新色與新版本在國際市場是成長動能。（原話："bringing the core franchise to life with different colors"）
- 2026-06-04｜Meghan Frank｜capital_allocation：第一季買回約 220 萬股，均價 $165。（原話："2.2 million shares at an average price of $165"）
- 2026-06-04｜Meghan Frank｜capital_allocation：買回計畫尚餘約 $10 億額度，管理層說會持續使用。（原話："$1 billion remaining on our share repurchase program"）
- 2026-06-04｜Meghan Frank｜capital_allocation：管理層稱買回是偏好的股東回饋方式。（原話："Share repurchases remain our preferred method"）
- 2026-06-04｜Meghan Frank｜capital_allocation：2026 年買回規模預期與 2025 年相當。（原話："repurchase levels in 2026 to be in line with 2025"）
- 2026-06-04｜Meghan Frank｜capital_allocation：全年資本支出財測 $7.0 億–$7.2 億。（原話："approximately $700 million to $720 million"）
- 2026-06-04｜Meghan Frank｜capital_allocation：被問新店報酬：Meghan 說新店資本回收期 1 年（改裝 2–3 年，在下一行）。（原話："return on capital of 1 year for our new stores"）
- 2026-06-04｜Meghan Frank｜capital_allocation：Meghan 說有幾間新店延到 2027 年開。（原話："We did have a few stores push into '27"）
- 2026-06-04｜Meghan Frank｜capital_allocation：行銷投入提高到占銷售 6%–6.5%（去年 5.6%）；上一行說比去年高約 10%–15%。（原話："in the range of 6% to 6.5% of sales versus last year at"）
- 2026-06-04｜Meghan Frank｜commitment：Meghan 承諾下半年品牌活動會更大膽。（原話："You will see us be bolder in the second half of the year"）
- 2026-06-04｜Meghan Frank｜commitment：新任 CEO Heidi O'Neill 預計 9 月加入公司。（原話："welcome incoming CEO, Heidi O'Neill"）
- 2026-06-04｜Meghan Frank｜commitment：被問新 CEO 是否改變現行做法：Meghan 說目標仍是恢復全價健康度。（原話："restoring the full price health of the business"）
- 2026-06-04｜Meghan Frank｜commitment：Meghan 說公司正依現況趨勢調整（pivoting）。（原話："we're pivoting based on current trends"）

### 問答異常語氣（迴避／改口／保留）
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Dana Telsey：營收疲弱有多少來自轉向時尚款？新品占比多少？弱的是核心款還是新款？｜答法：Meghan 改談客流下降、負面評論與部分新品不如預期；核心款與新款沒有拆分，只說近期表現「影響產品面所有區塊」。
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Matthew Boss：美洲下滑幅度能否拆成產品設計、品類需求、總經幾塊？五月需求趨勢？｜答法：Meghan 說是「early analysis」，定性歸因客流與負面評論、新品表現；沒有給各因素的量化拆分，五月只說趨勢在四月底至五月轉軟、無五月數字。
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Michael Binetti：SKU 精簡的測試門市轉換率或銷售效率有無改善？哪些品類最過多？｜答法：Andre 重述少 15% SKU 與門市陳列邏輯、稱「over time」會累積成效；Meghan 補第一季 reg price 與美國序列改善；未給測試門市的轉換率／效率數字，也未指出哪類 SKU 最過多。
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Mark Altschwager：中國全年約 20% 成長中，同店與新店各占多少？｜答法：Meghan 說「haven't broken out the full year comp」，只重述第一季同店 13% 與全年 20% 財測，沒有拆分。
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Mark Altschwager：縮到 12–14 個月的卡關點？何時反映在同店？｜答法：Meghan 答技術解鎖需時間，速度效益「will build over time」，未給時程或量化。
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Aneesha Sherman：全價銷售何時轉正？第一季 reg price 高個位數增長是不是不含折扣的平均售價？｜答法：Meghan 給第二季全價銷售中個位數下滑、全年持平至略好、「progress throughout the year」，未指明哪一季轉正；ASP 之問只答「reg price 等同 full price」，未確認是 ASP 還是銷售額。
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Jay Sole：社群風波何時開始、為何結束、有無殘留影響？｜答法：Meghan 說報導「died down and subsided」，但強調尚未回到風波前趨勢、所以下修財測區間；未說明結束原因。

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
{"date":"20260516","verdict":"B 觀望（thesis 完整但時機極壞 + CEO 真空）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Americas comp 從衰退恢復至持平至小幅正成長","columns":{"2Y 驗證":"FY26-27 Americas comp 從 -3% → 0% → +2%","5Y 驗證":"FY28-FY30 Americas comp 持平 +1-3%","10Y 驗證":"Americas 占 revenue 從 70% → 55%（國際分子放大）","具體門檻":"FY26 guide Americas -1% 至 -3%；FY27 共識 0%","來源":"FY25 Q4 法說 + sell-side","漂移條件":"連 4 季 comp &lt; -3% → 反轉"}},{"id":"H2","text":"International + China 維持 +20% 增速並成為第二成長曲線","columns":{"2Y 驗證":"FY26-27 international +20-25%","5Y 驗證":"FY28-FY30 international 達 revenue 35-40%","10Y 驗證":"10Y 國際 50%+ revenue","具體門檻":"FY25 +22% / China +29%","來源":"Q4 FY25 法說","漂移條件":"連 2 季 international &lt; +15% → 削弱"}},{"id":"H3","text":"毛利率 / Op margin 在 56% / 19-21% 穩定","columns":{"2Y 驗證":"FY26-27 GM 56%、Op margin 18-20%","5Y 驗證":"FY28-30 規模 leverage 後 op margin 21-23%","10Y 驗證":"10Y 維持高 margin profile","具體門檻":"FY25 GM 56.6%、Op margin 19.9%","來源":"Q4 FY25 法說 + sell-side","漂移條件":"連 4 季 op margin &lt; 17% → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Americas brand power 永久喪失（Alo / Vuori 持續搶份）","columns":{"對應":"H1, H3","時間尺度":"🐢 長期 2+ 年","監測指標":"Americas comp 連 4 季、competitor SOM 數據","警戒":"連 8 季 Americas comp &lt; -3% → 砍倉"}},{"id":"R2","text":"新 CEO 上任後 strategy reset 不力或 brand IP 流失","columns":{"對應":"H1, H2","時間尺度":"🔥 中期 4-6 季","監測指標":"CEO 上任時程、首份 strategy update、product 創新 cycle","警戒":"2026 Q4 仍空缺 → 砍倉"}},{"id":"R3","text":"China 增速減速 + 國際擴張遇挫","columns":{"對應":"H2","時間尺度":"🔥 中期","監測指標":"China + international 各國 Rev growth","警戒":"連 2 季 international &lt; +15% → 削弱"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"❌","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":119.14,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LULU_20260924/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
