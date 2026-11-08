你是 stock-analyst **v20 判斷 agent**，標的 CW（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CW","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CW_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CW_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":952.59,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP（調整後）營業利益","value":189.29,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm"}},{"id":"f_kpi2_non_gaap","label":"Non-GAAP（調整後）營業利益率","value":19.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm"}},{"id":"f_kpi3_gaap","label":"GAAP 營業利益","value":187.92,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm"}},{"id":"f_kpi4_gaap","label":"GAAP 營業利益率","value":19.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm"}},{"id":"f_kpi6","label":"新訂單","value":1100,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm"}},{"id":"f_kpi7_backlog","label":"Backlog","value":4600,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm"}},{"id":"f_kpi8_fy2026_11_04","label":"FY2026 指引（11-04 上修）","value":"銷售 3,795–3,840M（+8–10%）；營業利益 731–744M；營業利益率 19.2–19.4%；稀釋 EPS 15.40–15.60；FCF 595–615M","period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"guidance","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_cw_gross_margin_pct","label":"CW 毛利率","value":38.07,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cw_operating_margin_pct","label":"CW 營業利益率","value":19.06,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cw_fcf_margin_pct","label":"CW FCF 利潤率","value":15.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hei_gross_margin_pct","label":"HEI 毛利率","value":40.4,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HEI.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hei_operating_margin_pct","label":"HEI 營業利益率","value":24.04,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HEI.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hei_fcf_margin_pct","label":"HEI FCF 利潤率","value":19.9,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HEI.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tdg_gross_margin_pct","label":"TDG 毛利率","value":59.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDG.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tdg_operating_margin_pct","label":"TDG 營業利益率","value":46.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDG.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tdg_fcf_margin_pct","label":"TDG FCF 利潤率","value":19.26,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDG.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tdy_gross_margin_pct","label":"TDY 毛利率","value":43.6,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_tdy_operating_margin_pct","label":"TDY 營業利益率","value":20.0,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_tdy_fcf_margin_pct","label":"TDY FCF 利潤率","value":17.6,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hwm_gross_margin_pct","label":"HWM 毛利率","value":36.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hwm_operating_margin_pct","label":"HWM 營業利益率","value":28.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hwm_fcf_margin_pct","label":"HWM FCF 利潤率","value":19.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_q3","label":"自由現金流（Q3）","value":157.37,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-04）","citation":"Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":463.47,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-36.39,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":40.51,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（15.35 → 15.35）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（17.24 → 17.24）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.5 → 19.5）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":15.35,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":17.24,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":19.5,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.39,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 15.29 → 15.35（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":30.92,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝3.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":3.5,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.5,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝54.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":54.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.73,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝51.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":51.3,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":30.19,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 15.35，分子＝快照價 463.47","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.216,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":863.19,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 1144.3、現金 281.11（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":36.27,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":17674.29,"period":"2026-11-08","unit":"USD m","basis":"市值 16811.1 ＋ 淨負債 863.19","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":3819.63,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":4138.6,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（9 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.63,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 463.47 / W52 642.96 / W104 531.12 / W250 338.15 / W250 13週斜率 1.64%"},{"id":"f_ma_w52","label":"52 週均線","value":642.96,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":531.12,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":338.15,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.64,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"10-K 自述：公司在多數 A&D 與商用終端市場靠工程與技術領先、精密製造及深度嵌入客戶工作流程的長期關係維持競爭地位，主要以技術與價格競爭。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"we maintain competitive positions in the majority of our key A&D and commercial end markets through engineering and technological leadership, precision manufacturing, and long-standing customer relationships where we are deeply embedded in our customers' workflows.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：對手常有更大規模與資源、可能降價；最大客戶可能自製；國際競爭與跨國對手整併增加。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"some of our largest customers could develop the capability to manufacture products or provide services similar to products that we manufacture or services that we provide. This would result in these customers supplying their own products or services and competing directly with us","as_of":"2026-02-12","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"10-K 揭露無單一客戶占2025、2024、2023年淨銷售超過10%，客戶為數百家。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"We have hundreds of customers in the various industries that we serve. No customer accounted for more than 10% of our total net sales during 2025, 2024, or 2023.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"商用航太主要客戶為Boeing與Airbus；10-K風險因素提到部分最大客戶可能自製而與公司競爭。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"Our primary focus is OEM products and services for commercial jets, which represent approximately 90% of our sales in this market and are highly dependent on new aircraft production from our primary customers, Boeing and Airbus.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"CW Q3 2026：新訂單 $1.1B、在手訂單 $4.6B，全年 2026 營收成長指引上調至 8–10%、EPS $15.40–15.60","source":"CW Q3 2026 8-K earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"CW 2026 Q2 財報電話會議：CEO 預期今年有 AP1000 訂單；核能近期營收以售後市場為主，2026 預期中高十位數成長；Q2 海軍訂單因潛艦訂單時點延後而年減；宣布 $80M 多年期專案擴充賓州海軍與商用核能產能","source":"Curtiss-Wright Q2 2026 Earnings Call Transcript (MarketBeat/Webull)","url":"https://www.marketbeat.com/earnings/reports/2026-8-6-curtiss-wright-co-stock/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["thesis.H","triggers"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"美國潛艦產業基礎產能約每年 1.2 艘，低於最低目標 2.3 艘；供應鏈（單一來源大型複雜零組件）為瓶頸；SSN(X) 時程由 2031 延至 2040；國會推動 Block VI 多年合約以給供應商長期需求訊號","source":"ShipUniverse / SAMSearch / Exchange Monitor 2026 coverage","url":"https://samsearch.co/government-contracting-news/navy-submarine-production-goals-put-industrial-base-capacity-in-focus-226708","excerpt":null,"as_of":"2026-03-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"經查 FY2025 10-K Item 3，公司法律程序僅列附帶性訴訟（石綿、環境、智財、政府合約等），管理層認為個別或合計均不會對財務造成重大不利影響；未列反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 3. Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"we do not believe that the disposition of any of these matters, individually or in the aggregate, will have a material adverse effect on our consolidated financial condition, results of operations, and cash flows.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：部分產品已被關稅涵蓋，新增或提高關稅可能提高材料成本，漲價未必能完全抵銷而壓低毛利；2025 年約 27% 銷售來自美國以外客戶。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"Some of our products are included in these tariffs. The imposition of new or increased tariffs, duties, border adjustment taxes, or other trade restrictions by the United States could also result in the adoption of new or increased tariffs or other trade restrictions by other countries.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K 風險因子：公司受 ITAR、OFAC、EAR 等進出口管制，曾對美國國務院、能源部、商務部、財政部提交自願揭露，至今未造成重大罰款或出口特權被拒。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"To date, our voluntary disclosures have not resulted in a fine, penalty, or export privilege denial or restriction that has had a material adverse impact on our financial condition or ability to export.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"搜尋摘要：2026 年 5 月 Q1 簡報稱 Aerospace & Industrial 的營運效率與重組節省超過中國關稅衝擊；FY2026 銷售成長上調至 7%–8%。","source":"Curtiss-Wright Q1 2026 Earnings Conf Call Slides","url":"https://curtisswright.com/sites/default/files/press-releases/Q1%202026%20Earnings%20Conf%20Call%20Slides%20Final.pdf","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"美國對中國核能出口許可暫緩，CW 有五件申請待 NRC 審理","source":"Energy Intelligence","url":"https://www.energyintel.com/0000017b-a7d5-de4c-a17b-e7d7688a0000","excerpt":"The US government's decision to delay authorization for nuclear exports to China appears to heavily impact Curtiss-Wright, which has five applications pending before the US Nuclear Regulatory Commission (NRC), including one explicitly covering reactor coolant pumps (RCPs) while at least some others involve equipment used in RCPs.","as_of":"2018-07-26","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因素：供應鏈受供應商產能、制裁與貿易限制、關稅及地緣事件影響，點名俄烏戰爭與中美台關係","source":"Curtiss-Wright FY2025 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"Our supply chain has been and may continue to be impacted by a wide variety of factors, including supplier capacity constraints, sanctions and trade restrictions and other governmental regulatory actions or inactions, labor and material shortages as well as tariffs and other geopolitical events, such as the Russia-Ukraine war and China's relationship with the United States and Taiwan.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2023 10-K：部分零組件有唯一供應商，若延遲或無法供貨可能無法及時生產","source":"Curtiss-Wright FY2023 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/26324/000002632424000004/cw-20231231.htm","excerpt":"If a sole-source supplier is delayed or should cease or otherwise be unable to deliver such components, we may not be able to produce the related product in a timely manner or in sufficient quantities, if at all, which could adversely affect our operating results.","as_of":"2024-02-14","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Q2 2026 法說：上半年供應鏈壓力上升，特別是表面處理用稀土材料與化合物","source":"Curtiss-Wright Q2 2026 Earnings Call Transcript (Webull)","url":"https://www.webull.com/news/15393402860938240","excerpt":"supply chain pressures have increased in the first half of this year, especially for rare earth materials and compounds used in surface treatment.","as_of":"2026-08-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Q1 2026 法說：供應鏈關注記憶體與儲存晶片、PCB、稀土礦物，並與客戶及供應商合作認證替代來源","source":"Barchart / MarketBeat Q1 2026 call summary","url":"https://www.barchart.com/story/news/1782243/cw-q1-deep-dive-backlog-expansion-and-defense-demand-shape-outlook","excerpt":"the company is focused on memory and storage chips, printed circuit board-related issues and rare earth minerals.","as_of":"2026-05-07","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 銷售約9.53億美元(+10%)；Aerospace & Industrial 2.82億(+14%)、Defense Electronics 2.59億(+2%，商用航空OEM航電出貨時點偏低)、Naval & Power 4.12億(+12%)；全年銷售成長指引上調至8-10%","source":"Curtiss-Wright Q3 2026 earnings release (SEC 8-K ex99.1)","url":"https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm","excerpt":"Aerospace & Industrial $ 281,750 $ — $ 281,750 $ 247,985 $ — $ 247,985 14 % 14 % Defense Electronics 258,988 — 258,988 253,159 — 253,159 2 % 2 % Naval & Power 411,852 — 411,852 368,026 — 368,026 12 % 12 %","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 簡報：海軍國防銷售成長指引上調至9-11%(2月為5-7%、5月為6-8%)，因潛艦與航母計畫加速及航母大修售後；商用核能受國際售後、SMR、政府核能帶動；AP1000訂單未納入指引","source":"Curtiss-Wright Q3 2026 earnings presentation (SEC 8-K ex99.2)","url":"https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex992_cwxq326.htm","excerpt":"Accelerated global defense spending driving overall strong A&D market growth Power & Process 13 - 15% 13 - 15% 19% ▪ Commercial Nuclear growth driven by aftermarket demand (esp. international markets), next-generation advanced reactors (SMRs) and increased govt. nuclear; AP1000 order excluded from targets ▪ Growth in Process driven by increased sales of valves (MRO and large capital projects)","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素指出：公司所處商業與政府市場技術快速變動，需持續投資研發、併購或合作才能維持競爭力；並提到商用核電（含 SMR）發展延遲可能影響業績。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"The commercial and government markets in which we operate are characterized by rapidly changing technologies. In addition, product and program needs of our government and commercial customers change and evolve regularly.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：商用核電產業的任何重大中斷（含 SMR 開發延遲）可能影響營運結果或展望。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"Any significant disruption in the commercial nuclear power industry, including delays in the development of small modular reactors, could adversely affect our results of operations or future outlook.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"搜尋摘要顯示 CW 為多家 SMR 的指定供應商（Rolls-Royce SMR 反應爐保護系統、X-energy Xe-100 氦氣循環器與燃料處理、NuScale 控制棒驅動），搜尋未發現取代其產品的替代技術。","source":"WebSearch 摘要（power-eng.com／X-energy／Rolls-Royce SMR 公告）","url":"https://www.power-eng.com/nuclear/x-energy-picks-curtiss-wright-as-preferred-supplier-for-xe-100-small-modular-reactor/","excerpt":null,"as_of":"2025-08-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 描述 CW 銷售對象為 OEM、美國政府／海軍、核電廠與設備商，屬直接銷售的專案／平台型模式；經查未見通路中斷、訂閱化或 D2C 轉型的一手揭露。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"The commercial aerospace business is primarily impacted by OEM production rates of new aircraft, while the defense business is primarily impacted by government funding and spending on new programs, primarily driven by the U.S. Government.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-11-04 Q3 公布並上調全年指引：調整後 EPS 由 15.10–15.40 升至 15.40–15.60，FCF 595–615 百萬美元；Q3 營收 9.53 億美元、調整後 EPS 3.94。","source":"Curtiss-Wright Q3 2026 results (finviz/SEC 8-K ex99.1)","url":"https://finviz.com/news/416130/curtiss-wright-reports-third-quarter-2026-financial-results-and-raises-full-year-2026-guidance","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"ChartMill 顯示 FY2026 EPS 共識 15.77（13 位分析師，2026-10-25），高於 Q3 前的公司指引 15.10–15.40，亦略高於 11-04 新指引上緣前之區間；共識與指引有落差（共識在上方）。","source":"ChartMill CW estimates","url":"https://www.chartmill.com/stock/quote/CW/estimates","excerpt":"Latest recorded estimate: 15.77 USD · Oct 25, 2026 · 13 analysts","as_of":"2026-10-25","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat：2026-08-05 指引 EPS 15.10–15.40 vs 共識 15.21，大致符合；Q2 EPS 3.72 勝共識 3.61；共識評級 Moderate Buy，均價目標 773.67；財報後股價跌至 748.10。","source":"MarketBeat 2026-08-05","url":"https://www.marketbeat.com/instant-alerts/curtiss-wright-nysecw-issues-fy-2026-earnings-guidance-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布因來源而異：Tickflow（as of 2026-08-01）7 位分析師 Hold、均價 741；MarketBeat 6 位均價 746.67（高 870／低 603）；ChartMill 17 位均價 713.41（高 808.50／低 611.43，未標日期）；Stifel Hold 目標 768（2026-07-20）。","source":"Tickflow／MarketBeat／ChartMill／Investing.com 聚合","url":"https://www.tickflow.io/stock/CW/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Morgan Stanley 認為 CW 有望超越三年框架目標（國防、核能需求加速）。","source":"itiger news","url":"https://www.itiger.com/news/2611041166","excerpt":"Curtiss-Wright Poised to Beat 3-Year Framework as Defense, Nuclear Demand Accelerate, Morgan Stanley Says","as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：公司稱涉及石綿等附帶訴訟，認為不會對財務狀況、經營成果或現金流產生重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"We do not believe that the disposition of any of these matters, individually or in the aggregate, will have a material adverse effect on our consolidated financial condition, results of operations, and cash flows.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月8-K共12份，含重大項目者5份；其中2026-05-20 Item 1.01為新的10億美元循環信貸（取代7.5億），非併購。","source":"SEC EDGAR 8-K 2026-05-20 Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026036955/cw-20260519.htm","excerpt":"On May 19, 2026, Curtiss-Wright Corporation (the “Company”) entered into a Credit Agreement (the “Credit Agreement”) evidencing a new syndicated $1 billion revolving credit facility (the “Credit Facility”).","as_of":"2026-05-20","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"2026-09-10董事會追加5.1億美元庫藏股授權，總可用額度7億美元。","source":"SEC EDGAR 8-K 2026-09-14 Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026061788/cw-20260910.htm","excerpt":"On September 10, 2026, Curtiss-Wright Corporation’s (the “Company”) Board of Directors authorized the Company to repurchase up to an additional $510 million of its common stock. The total available authorization is $700 million","as_of":"2026-09-14","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"RTTNews標題稱CW將以約4億美元收購Pacific Star Communications（PacStar）；日期與是否為近12個月事件未核。","source":"RTTNews","url":"https://www.rttnews.com/3131242/curtiss-wright-to-acquire-pacific-star-communications-for-400-mln-quick-facts.aspx","excerpt":"For $400 Mln - Quick Facts By RTTNews Staff Writer ✉ | Published: 9/24/2020 7:51 AM ET | Follow Us | Join Us Add as your preferred news source on Google Add Now Curtiss-Wright Corp. (CW), a manufacturer of precision components, and engineered products, said Thursday that it has agreed to acquire the stock of Pacific Star Communications, Inc. for $400 million in cash. PacStar, a private","as_of":"2020-09-24","retrieved_at":"20261108","affects":["valuation","moat_trend"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K稱涉及石綿等附帶訴訟，預期無重大不利影響；搜尋未見證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm","excerpt":"We have been named in pending lawsuits that allege injury from exposure to asbestos. To date, we have not been found liable or paid any material sum of money in settlement in any asbestos-related case.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"CW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.07,"operating_margin_pct":19.06,"fcf_margin_pct":15.78,"rd_intensity_pct":2.65},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CW","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"HEI","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":40.4,"operating_margin_pct":24.04,"fcf_margin_pct":19.9,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HEI","as_of":"TTM ending 2026-07-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TDG","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":59.57,"operating_margin_pct":46.47,"fcf_margin_pct":19.26,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDG","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TDY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":43.6,"operating_margin_pct":20.0,"fcf_margin_pct":17.6,"rd_intensity_pct":5.07},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TDY","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"HWM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.63,"operating_margin_pct":28.01,"fcf_margin_pct":19.83,"rd_intensity_pct":0.39},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"CW"},"financial_history":{"ticker":"CW","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":2557025000.0,"revenue_yoy_pct":null,"gross_margin_pct":37.33,"operating_margin_pct":16.74,"net_income":294348000.0,"diluted_eps":7.62,"free_cash_flow":256559000.0,"fcf_margin_pct":10.03,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":2845373000.0,"revenue_yoy_pct":11.28,"gross_margin_pct":37.51,"operating_margin_pct":17.03,"net_income":354509000.0,"diluted_eps":0.79,"free_cash_flow":403423000.0,"fcf_margin_pct":14.18,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":3121189000.0,"revenue_yoy_pct":9.69,"gross_margin_pct":36.96,"operating_margin_pct":17.4,"net_income":404978000.0,"diluted_eps":10.55,"free_cash_flow":483301000.0,"fcf_margin_pct":15.48,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":3498372000.0,"revenue_yoy_pct":12.08,"gross_margin_pct":37.2,"operating_margin_pct":18.24,"net_income":484228000.0,"diluted_eps":12.87,"free_cash_flow":553710000.0,"fcf_margin_pct":15.83,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CW/CW_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**Curtiss-Wright Corporation** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Welcome to the Curtiss-Wright Third Quarter 2026 Earnings Conference Call. [Operator Instructions] I would now like to turn the call over to Jim Ryan, Vice President of Investor Relations.

**James Ryan** (Executives):
Thank you, Madison, and good morning, everyone. Welcome to Curtiss-Wright Third Quarter 2026 Earnings Conference Call. Joining me on the call today are Lynn Bamford, Chair and Chief Executive Officer; Kevin Rayment, Executive Vice President and Chief Operating Officer; and Gary Ogilby, Senior Vice President, Interim Chief Financial Officer and Corporate Controller. A copy of today's financial presentation and the press release are available in the Investor Relations section of our website. A replay of this webcast will also be available on our website. 
Our discussion today includes certain projections and forward-looking statements that are based on management's current expectations and are not guarantees of future performance. We detail those risks and uncertainties associated with our forward-looking statements in our public filings with the SEC. As a reminder, the company's results and guidance include an adjusted non-GAAP view that excludes certain costs in order to provide greater transparency into Curtiss-Wright's ongoing operating and financial performance. GAAP to non-GAAP reconciliations are available in the earnings release and on our website. Now I'd like to turn the call over to Lynn to get things started.

**Lynn Bamford** (Executives):
Thank you, Jim, and good morning, everyone. Today, I'm pleased to be joined by Kevin Rayment and Gary Ogilby, both of whom are long-tenured executives at Curtiss-Wright, who have each played a critical role in driving our Pivot to Growth Strategy and long-term financial performance. You will have an opportunity to hear from each of them shortly. 
Momentum continues to accelerate at Curtiss-Wright as strong execution drove third quarter results that exceeded our expectations. The team continues to excel in aligning with customers, winning new business, growing our backlog to record levels and expanding margins through operational excellence. Our business fundamentals are strong. 
Based on our solid first quarter performance and our continued optimism heading into year-end, we confidently raised our full year guidance across all major financial metrics, and we remain committed to delivering exceptional results for our shareholders. 
With that, and turning to the highlights of our third quarter results. Sales of $953 million increased 10% year-over-year, reflecting overall strong growth across our A&D and commercial markets. Operating income once again exceeded our sales growth and resulted in 30 basis points of operating margin expansion to 19.9%. Diluted earnings per share of $3.94 increased 16% and was slightly ahead of our expectations, primarily driven by our strong operational performance. We generated nearly $160 million of free cash flow, achieving a strong cash conversion rate of 108% while continuing to accelerate investments across our organization to support our long-term objectives. 
New orders increased 15%, resulting in a book-to-bill of 1.1x, reflecting continued positive momentum across the portfolio, particularly in our A&D and general industrial markets. To give you more color, I'll start in Defense Electronics, which once again delivered a strong performance with orders up 27% year-over-year following our record second quarter bookings. We experienced higher orders supporting fighter jet and helicopter programs, various modernization programs as well as several development contracts supporting next-generation programs such as CCA.
We also received solid tactical communications equipment orders supporting U.S. Air Force programs as well as rugged small form factor mission computers for the IFPC program. The substantial growth in our order book this year underscores Curtiss-Wright's broad product portfolio ranging from MOSA-aligned embedded computing modules to advanced software solutions supporting soldiers in the battlefield, including tactical networks. We remain well aligned with the strategic growth priorities of the U.S. and its allies. 
Within the A&I segment, we experienced strong demand for commercial aerospace products supporting the long-term production ramp across the major OEM platforms. Building on that, we continue to experience solid demand in our general industrial order book, contributing to our more positive outlook in this market as we enter 2027. Lastly, within the Naval & Power segment, in Naval Defense, we saw higher orders for nuclear propulsion equipment on U.S. Navy aircraft carriers and solid demand for aircraft handling equipment supporting various international programs.
Within our commercial nuclear market, we experienced solid demand for aftermarket equipment supporting plants globally in addition to development and prototype contracts supporting leading SMRs. Overall, Curtiss-Wright's robust and strengthening pipeline of new orders adds to an already strong backlog, which is now up 12% year-to-date to a new record of approximately $4.6 billion. Our team continues to generate meaningful growth opportunities that position our businesses for success well into the next decade. 
Turning to our full year guidance. We now project sales to increase 8% to 10%, driven by continued favorability and strong demand in our defense and industrial markets. We continue to expect year-over-year margin expansion across all 3 segments in pursuit of an overall record operating margin of 19.2% to 19.4%. Based on those increases, diluted EPS is now projected to grow 16% to 18%. We also raised our free cash flow guidance and continue to expect strong cash conversion in excess of 105%.
Lastly, following our increased second half share repurchase activity, we are on pace to complete a near-record $460 million in share buybacks under our disciplined and strategic capital allocation strategy. Now I would like to turn to the recent leadership transitions, and I want to begin by congratulating Kevin on being named Curtiss-Wright's next Chief Executive Officer. As we announced last month, Kevin will become CEO effective January 1, and I will move into the role of Executive Chair. 
Kevin's appointment is incredibly well deserved. It reflects the culmination of our robust succession planning process that's taken place throughout the past year with our Board to ensure a successful transition. Since joining Curtiss-Wright in 2004, Kevin has established himself as a respected leader with a long-standing track record of execution and success. 
In recent years, he has played a significant role in shaping Curtiss-Wright's Pivot to Growth Strategy. He has been a driving force behind our accelerated organic growth as well as our pursuit of commercial and operational excellence, resulting in continued operating margin expansion and substantial value to shareholders. We expect Kevin's transition to CEO to be seamless and provide stability for our employees, customers, investors and all stakeholders as we maintain our operational momentum. 
Next, I would like to thank, Chris Farkas, who stepped down from his role as CFO last month and will retire from the company at year-end. During his tenure, Chris was a key contributor to our strong financial performance while also supporting our disciplined approach to capital allocation to help create value for our shareholders. I value his partnership in executing the Pivot to Growth Strategy and in our engagement with the investment community. We wish him well in his retirement. 
I would also like to thank Gary Ogilby, a 17-year veteran of the company, who is serving as Interim Chief Financial Officer. He previously served as VP of Finance in one of our divisions where he led numerous operating margin improvement initiatives before being named in his current role as Corporate VP and Controller. Gary has been an integral part of our finance organization and has been closely aligned with the management team in delivering on the Pivot to Growth Strategy. He continues to be a key partner to Kevin and our leadership team in advancing the company's financial discipline and performance. We are grateful for his leadership and for the continuity that Gary brings to our finance team. 
Overall, these recent announcements highlight one of the company's greatest strengths, our deep bench of talent in leadership and our commitment to developing and promoting leaders from within. Now I would like to turn the call over to Kevin to provide some additional color on this leadership transition.

**Kevin Rayment** (Executives):
Thank you, Lynn, and good morning, everyone. I'm privileged to be named Curtiss-Wright's next Chief Executive Officer. It is an exciting time to step into the CEO role based on the strength of our fundamentals, record backlog and the momentum that we're experiencing across our end markets. Since we launched the Pivot to Growth Strategy back in 2021, I've had the opportunity to work very closely with Jim, our senior leadership team and our Board to help steer Curtiss-Wright's operational journey and deliver profitable growth in excess of our expectations. 
I would very much like to thank Lynn for her leadership, guidance and partnership over the years, and I look forward to continuing to work closely with her as she steps into a new role as Executive Chair. Earlier this week, we announced the new structure for our operational leadership team by naming 3 new presidents to manage our Aerospace & Industrial, Defense Electronics, and our Naval & Power segments. 
This seasoned leadership team brings deep rooted knowledge of our customers, operations and industry, and I have the utmost trust and confidence that these leaders will continue to advance our strategy, capture significant future growth opportunities and deliver strong operational results. Together with the announcement of appointing Gary Ogilby as our interim CFO, we have a reshaped corporate leadership team that's excited to build upon our established growth strategy and drive the next phase of Curtiss-Wright's journey. 
Since being named CEO, I've engaged with our leadership team to discuss my strategic vision for Curtiss-Wright's future and our long-range financial objectives. Several key priorities will help sustain our strong momentum, including continuing to drive execution velocity by streamlining our processes and increasing our market responsiveness and utilizing our strong free cash flow position to fuel the expansion of our operations globally across both existing and new facilities to enhance alignment with customers. I'll share more specific details during our Q4 earnings call and provide a more comprehensive overview at our next Investor Day in May 2027. 
I look forward to building a Curtiss-Wright's successful strategy, sustained profitable growth in 2027 and beyond and continuing to deliver long-term value for our shareholders. Before I turn the call over, I want to thank Gary for stepping in as Interim CFO. I've appreciated his support over the years and look forward to continue to work closely with him. With that, I'll turn it over to Gary to provide more in-depth review of our financials.

**Gary Ogilby** (Executives):
Thank you, Kevin. Before we dive into the financials, I just wanted to take a moment to say how honored I am to be named Interim CFO for Curtiss-Wright. I appreciate the opportunity to lead our finance organization and to continue to work closely with our leadership team and the Board to ensure a seamless transition of our strategy as we deliver strong profitable growth. 
I'll begin on Slide 4 by reviewing the key drivers of our third quarter 2026 performance by segment. Starting in Aerospace & Industrial, sales increased 14%, which exceeded our expectations. Beginning with the Aerospace Defense market, we experienced higher-than-anticipated sales of actuation and sensors equipment supporting various U.S. fighter jet programs which were partially offset by the timing of EM actuation equipment sales supporting ground-based mobile launcher systems. 
Within the commercial aerospace market, we experienced solid OEM sales growth supporting increased production on both narrow-body and wide-body platforms. And in the general industrial market, our results reflected the continued positive inflection in our order book, which contributed to strong double-digit growth in sales. Regarding the segment's operating performance, a combination of favorable absorption and mix of products from higher revenues as well as restructuring savings drove operating income and operating margin growth of 19% and 80 basis points, respectively. We continue to experience improved profitability in this segment while maintaining sound investments in development programs. 
Next, in the Defense Electronics segment, sales increased 2%, exceeding our expectations due to the timing of tactical communications equipment revenues within ground defense as some revenues accelerated into the third quarter. We're pleased to see stability in tactical communications equipment sales and anticipate sequential growth into the fourth quarter. 
Growth in the Aerospace Defense market was driven by higher sales of embedded computing equipment supporting various domestic helicopter programs and international fighter jet production. We also experienced higher revenues supporting next-generation development programs. Regarding the segment's operating performance, operating margin of 27% was lower year-over-year as expected as favorable absorption on higher revenues was more than offset by unfavorable mix. 
Moving to the Naval & Power segment. Sales growth of 12% was driven by strong growth in our Naval Defense market associated with the timing of production on submarine programs, along with steady growth in aftermarket revenue supporting the CVN-75 overhaul project. In Power & Process, we experienced double-digit revenue growth, primarily driven by increased revenues in the commercial nuclear market supporting advanced small modular reactors. Operating income grew 25%, generating 200 basis points in operating margin expansion, reflecting favorable absorption and mix of products on higher revenues. 
To sum up, Curtiss-Wright's third quarter results, double-digit growth in both revenue and operating income resulted in strong operating margin of 19.9%, driving 30 basis points in year-over-year operating margin expansion. 
Turning to our full year 2026 guidance. I'll begin on Slide 5 with our end market sales outlook. Our continued improvement in expectations for both our overall Defense and General Industrial markets has enabled us to confidently raise the upper end of our guidance. As a result, we now anticipate total sales to grow 8% to 10%. 
Starting in Aerospace Defense. We raised our full year outlook to a new range of 14% to 16%, reflecting improved expectations for sales of actuation and sensors equipment, supporting both domestic and international fighter jet programs. Our outlook is supported by our continued alignment to Department of War priorities, including next-generation platforms and aircraft modernization, which is a catalyst for fourth quarter sequential growth in Defense Electronics. 
Within Ground Defense, strength in the pipeline and growth in the 2026 order book for our tactical communications equipment provided us with confidence to modestly increase our full year outlook. In Naval Defense, we now project full year sales growth of 9% to 11% due to expectations for higher production revenue on submarine programs and increased aftermarket revenues, while we continue to expect solid revenue growth on the CVN-81 carrier program. Based on these updates, we now expect total Aerospace & Defense sales to increase 8% to 10%. 
Moving to our commercial markets. In Power & Process, we maintained our full year outlook for sales growth of 13% to 15%, primarily driven by strong growth in commercial nuclear. Lastly, in the General Industrial, we now anticipate full year sales growth of 3% to 5%, driven by the continued market improvements and steady growth in our industrial vehicles order book. Wrapping up our commercial markets, we continue to project that total sales in these markets will increase 8% to 10%.
Moving on to our updated full year 2026 financial outlook by segment on Slide 6. I'll begin in Aerospace & Industrial, where we increased our revenue guidance to a new range of 10% to 11%, driven by the improved outlook in this segment's Aerospace Defense market and continued optimism in the General Industrial. Operating income is now projected to grow 17% to 19%, while we continue to expect operating margin expansion 110 to 130 basis points, ranging from 18.5% to 18.7% based on more favorable absorption and mix on higher sales, balanced by increased R&D investments. 
Moving to Defense Electronics, where we continue to anticipate sales growth of 4% to 6%. We expect a strong finish to the year, driven by the strength of our order book as well as the team's advanced planning and exceptional management of the supply chain to deliver continued operational efficiency. We continue to expect operating income growth of 5% to 7% and operating margin expansion of 20 to 40 basis points as we deliver industry-leading margins, reflecting a range of 27.5% to 27.7%. 
Lastly, in Naval & Power, we now expect sales to grow 11% to 12%, reflecting our increased Naval Defense market outlook and overall strong backlog, which provides long-term visibility and overall solid growth across the segment's commercial markets. We now expect operating income growth of 16% to 18% and operating margin expansion of 70 to 90 basis points, driven by the stronger revenue outlook and more favorable naval aftermarket mix. So to summarize our 2026 outlook, we now anticipate total Curtiss-Wright operating income to grow 12% to 14%, driving operating margin expansion of 60 to 80 basis points to a record range of 19.2% to 19.4%. 
Continuing with our financial outlook on Slide 7. We increased our full year 2026 adjusted diluted EPS guidance to a new range of $15.40 to $15.60, up 16% to 18%, driven by the strong third quarter performance. Also note that the ramp-up in share repurchase activity resulted in a reduction in other income with a lower year-over-year interest income and a lower share count. Overall, we continue to compound earnings at a mid-teens pace over time. 
Lastly, turning to free cash flow. We raised our full year outlook by $10 million to a new range of $595 million to $615 million. As a reminder, our confidence in achieving record free cash flow incorporates increased capital expenditures to support ongoing growth investments, particularly within our Naval & Power segment. And as we maintain throughout the year, we expect to deliver a free cash flow conversion rate in excess of 105%. Now I would like to turn the call back over to Lynn.

**Lynn Bamford** (Executives):
Thank you, Gary. And turning to Slide 8. As we demonstrated today, Curtiss-Wright continues to build momentum across the portfolio, and we remain well positioned for a strong finish in 2026, providing confidence to deliver record financial results across all major metrics. In addition, we remain on track to exceed the 3-year objectives provided at our 2024 Investor Day as shown at the bottom of the slide. As a reminder, since the launch of the Pivot to Growth Strategy in 2021, one of our primary commitments has been accelerating Curtiss-Wright's top line growth organically, supplemented by strategic acquisitions. 
Our focus and execution on driving strategic investments, innovation and collaboration have fueled our success by further elevating growth opportunities across our markets. As we've grown, we have leveraged the company's increased scale in many ways, providing better value to our customers by enhancing our sales channels and technologies and driving internal investments to advance our talent, maximize shop floor efficiency and expand our infrastructure. We have a strong track record of operational and commercial excellence and are on track to deliver nearly 200 basis points in overall margin expansion since 2023, while growing R&D at a faster pace than sales. 
Lastly, we are driving record levels of free cash flow and expect to generate 110% average free cash flow conversion over the 3-year period. Our team continues to do an exceptional job in executing our Pivot to Growth Strategy. Next, looking across the A&D and commercial markets, our teams remain relentlessly focused on strengthening the backlog and building durable revenue growth. We are accomplishing this through thoughtful and targeted investments in capital equipment and capacity expansion aligned with the strongest medium- and long-term growth vectors globally. 
Organic growth continues to accelerate across our markets, and I'll highlight 2 key growth opportunities in greater detail, beginning with Defense. Curtiss-Wright is well aligned with the strategic Department of War funding priorities highlighted within both FY '26 and FY '27 base budgets, where we typically generate the majority of our Defense revenue. 
Some key examples include naval shipbuilding, legacy fleet modernization, enhancing capabilities at the tactical edge and advancing next-generation platforms, all of which are expected to receive increased funding and support Curtiss-Wright's long-term growth. More broadly, in addition to the U.S., we expect the trends supporting increased spending by NATO allies to continue providing strong tailwinds for Curtiss-Wright in the broader industry. 
Within commercial nuclear market, we maintain a comprehensive portfolio of technologies supporting the entire life cycle from the development and construction of new large reactors and SMRs to the aftermarket. The momentum and increased pace of global investments continue to accelerate, reinforcing our confidence in the future growth of our business. 
Last week, we announced a $30 million expansion of our Round Rock, Texas facility, part of our instrumentation and controls business acquired in 2024. This expansion positions us to satisfy growing customer demand for our critical temperature and pressure sensors supporting existing and new build commercial nuclear reactors. This announcement follows the $80 million expansion of our Cheswick, Pennsylvania facility announced in July, which further demonstrates our commitment to invest alongside industry to solidify our positions as a critical long-term commercial nuclear supplier. 
Regarding the AP1000, Westinghouse continues to generate strong interest across the U.S., Poland and other countries for new nuclear power plants. They are requesting supply chain readiness to support a potential global pipeline of 91 reactors and our recent investments are part of Curtiss-Wright's response to that challenge. We remain aligned and confident that we will receive an order for our reactor coolant pump supporting AP1000 plants in 2026. 
Meanwhile, SMR developments continue to evolve globally as we work to enhance our relationships and solidify our content across the leading 300-megawatt plus SMR designs. In recent news, we are excited to continue our partnership with Rolls-Royce SMR by announcing the award of a significant contract and signing of a design services framework agreement to design, qualify and manufacture the specialized nuclear valve package for the global fleet of Rolls-Royce SMR plants. As a result, we now estimate our current content on the Rolls-Royce SMR plant to be in excess of $100 million of revenue. These active valves perform safety critical functions within the power station and require proven nuclear capability and qualification. 
Curtiss-Wright will be providing these critical function valves and other equipment from our global operations within the U.K. and U.S. in support of this SMR technology. The expansion of this and other partnerships reinforces the strategic alignment of our technologies with the considerable opportunities ahead in this market. Overall, as we've shared throughout the year, we continue to see strong tailwinds across all our markets and have significant momentum as we head into 2027. 
As I wrap up my prepared remarks and reflect upon my career at Curtiss-Wright, I'm reminded of how fortunate I am to have been part of such an iconic institution only a few years away from its 100th anniversary. It has truly been a rewarding experience for me over the last 22 years to be part of Curtiss-Wright's transformation into a stronger high-growth company. I'm particularly proud of the team's perseverance and success under the Pivot to Growth Strategy to deliver consistent results and record financial performance. 
The relationships that I have built with the investment community during my tenure as CEO have been extremely rewarding to me personally. I would like to thank our analysts and shareholders for your confidence and trust in our leadership team and for your consideration of Curtiss-Wright as an investment. I look forward to serving as Curtiss-Wright's Executive Chair, and I am excited for the opportunities that are still ahead of this historic organization. On behalf of the Board, I'm confident that we are in great hands with Kevin as our next CEO to guide the organization to new heights and continue to deliver on long-term value for Curtiss-Wright's shareholders. 
At this time, we would like to open up today's conference call for questions.

**Operator** (Operator):
[Operator Instructions] Our first question is coming from Peter Arment with Baird.

**Peter Arment** (Analysts):
Nice results and congrats to Chris on his retirement. Thanks for all the help over the years. Maybe just to start within Defense Electronics. The growth was a little stronger than we had modeled for this quarter. And the fourth quarter kind of implies another big step up. Just confidence levels around that, what you're maybe seeing and any specific drivers that you would call out?

**Lynn Bamford** (Executives):
So I'll just kick it off, Peter, and it's always been wonderful engaging with you and appreciate your support over the years for starters. Defense Electronics is in a great position. And we do look -- we did pull some revenues out of Q4 into Q3, and so that was good. I'll ask Gary to speak to the Q4 specifics. But overall, this business is in great shape. I mean I think the order book reflects a lot of the strength of what we've brought to market over the past several years, the breadth of our product offering. We monitor the pipeline of new opportunities and bookings in this business and the future is just outstanding for this business. So with that, I'll turn it over to Gary, maybe just put a little more color specifically on Q4.

**Gary Ogilby** (Executives):
Sure. Thanks, Lynn, and thanks for the question, Peter. I'll start with a reminder of our prior sales guide where we said that Q3 operating income and margin were expected to be down sequentially from Q2 as favorable H1 mix would normalize into year-end, and we expected a higher level of second half R&D investments. That would be followed by a strong finish to the year here in Q4, which is what you're seeing. And so by and large, the second half of 2026 is largely playing out how we expected it. 
On the top line, it's really supported by our order book. In Q2, we had record orders, Q3 near record orders. And with regards to Q4, when you step back and look at this, we've experienced this type of ramp before, particularly in 2022 and 2023. So overall, we're really confident in our ability to execute and expect a strong sequential growth, both in Aerospace and Ground Defense into the fourth quarter. 
If you look at it from the supply chain side, we saw early warning signs of component shortages last year and quickly took action to secure component parts. So as we head into the fourth quarter, we feel that situation is well in hand for 2026, and these challenges are not expected to impact our Q4 revenue or margins. 
On the margin side, as mentioned, H2 is largely playing out as we anticipated it. That's really due to that favorable mix in H1, which drove higher profitability in the first half of the year and the investments in R&D were a little more weighted to H2. So both of those items are weighing on the second half margins, particularly in Q3. Overall, if you step back and look at the year, we're guiding 30 basis points of operating margin expansion at the midpoint, adding to our industry-leading margins and sales -- and solid sales growth in this tough macro environment. So overall, we feel really good about the year and really proud of the team's execution.

**Kevin Rayment** (Executives):
Continuing on this point, I would add is just that we're also very confident from a Q4 point of view from a bookings perspective. We certainly started the Q very strong as well, which is encouraging as we push towards the end of the year.

**Peter Arment** (Analysts):
Appreciate all the color and those details. And just as a follow-up, I'll ask a question you probably never got before, AP1000. Just we've seen -- obviously, we're tracking the construction permits in Poland and IHI has kind of started on the long lead. How are you seeing kind of progressing kind of the timing? You're kind of near the end of your kind of 3-year objective of expecting an order. What can you say on that, Lynn, thanks.

**Lynn Bamford** (Executives):
So I'm trying to figure out how that's a follow-up to Defense Electronics. But setting that aside...

**Peter Arment** (Analysts):
I said it was a question you never got before.

**Lynn Bamford** (Executives):
That's true. No, we have said the same thing consistently, and we do still expect an order in 2026. And we surely realize where we are in November and that, that runway is getting shorter. But we are so deeply engaged with Westinghouse who we take our guide from, and that is our expectations in the year. And you're right. I mean you can see some of the press that's out there and a lot of questions with midterm elections and different things, but Poland has been marching at a very steady rate. And we do anticipate that will be the leader at this point for a while, we thought it would be DOE. DOE does continue just to keep making progress, and we don't see any disruption to that in spite of everything going on in Washington and feel that we will have an order this year.

**Operator** (Operator):
And we will move next to Myles Walton with Wolfe Research.

**Myles Walton** (Analysts):
Congratulations on a great 10-year Lynn, and Chris, you moving, and welcome, Kevin and Gary. We focus maybe on the Defense Electronics for a moment. You're sounding really confident about where you're going to end up at a fourth quarter run rate. I think, Kevin, you alluded to orders remaining here in the fourth quarter. Sometimes with continuing resolutions, we encounter air pockets. I just want to clarify, it doesn't seem like you're signaling a prospect of an air pocket given you are in a CR. And I'm also curious what you expect for the resolution of the fiscal '27 budget?

**Kevin Rayment** (Executives):
Sure. Let me take that question. I think just to add to what Gary said in terms of our Q4, our bookings have been strong Q2, Q3, we're running into sort of Q4 with the CR at the 11th of December, that sort of gets us into a good position in the sense of we're getting towards the end of the year and bookings are continuing to be strong. 
As I said, the beginning of Q4 has been good for us. So we're pretty confident of our position from a bookings perspective into this year. The other thing I would sort of add is, if you look back over last year in '25, where we had CR and a government shutdown and some changes in the administration, that caused us a bit of a sort of slowdown at the beginning of this year. And I think in this situation with the CR at the 11th of December and sort of where we've seen our bookings, it's setting us up nicely for '27.

**Myles Walton** (Analysts):
And on that, you opened can of worms for '27, how well do you think it is setting up? Do you expect that you could have as good of an organic growth profile in '27 that you do in '26 with maybe Defense Electronics acceleration playing out?

**Lynn Bamford** (Executives):
So you know we're not going to give any specifics on 2027. But in my prepared remarks, I talked about the strong tailwinds across our businesses and the prospects for '27 are very good. And I think these 2 gentlemen sitting next to me are going to have a great opportunity to share that guidance in February and then move towards Investor Day and share even the bigger picture. But things are very good.

**Myles Walton** (Analysts):
Sounds good. I just want to give Kevin an early deadline, that's all.

**Operator** (Operator):
And we will move next to Justin Lang with Morgan Stanley.

**Justin Lang** (Analysts):
And Lynn, I just want to say it's been a pleasure interacting with you over the past few years. And Kevin and Gary, congrats on your new appointments. I wanted to ask one, maybe broader just on the political regulatory environment. Clearly, some shifts here in the landscape at the midterms, as Lynn, you alluded to, and you're obviously operating in a number of highly regulated industries. So just curious if you're thinking any differently about the backdrop for Defense and Commercial Nuclear end markets given some of the more recent changes of foot.

**Kevin Rayment** (Executives):
Sure. I think we all sort of feel to the point where it's a little bit difficult at this stage to determine what's going to come out. But I think earlier comments around sort of certainly our Defense business from a CR perspective, as I mentioned earlier, I think we feel in a reasonable position as we go into the end of this year. I think the other piece, too, is if you think about a lot of our sort of main drivers across the organization, there's a great level of support from a Navy shipbuilding perspective, as you can see into '27, that sort of growth in budget to $66 billion. And with the MIB funding sort of increasing up to nearly $9 billion, we've been very successful moving from $10 million up to nearly $100 million of MIB funding. 
So I think we feel like the underlying sort of main part of the business is very strong, and we're part of that main base budget. So I think that's encouraging. If I think about the nuclear side, you know, Lynn and I were on the hill this year, spending quite a bit of time talking around sort of the nuclear side of the business, and it broadly has bipartisan support, both from a sort of an energy security point of view and obviously from an environmental perspective. So we're encouraged by that. And I think both parties are very supportive of the nuclear industry.

**Justin Lang** (Analysts):
That's great. And then maybe a quick one for Gary. At Naval & Power, the margins this quarter were up over 100 bps sequentially, but on a pretty comparable level of sales. So just curious if you could talk a little bit about the drivers of the margin performance at the segment this quarter and where you saw some of those mix benefits.

**Gary Ogilby** (Executives):
Yes. On the mix side, we did see some really nice mix in the naval aftermarket as well as on the valve side, particularly on the MRO side. And overall, we're really happy with those results.

**Operator** (Operator):
And we will move next to Michael Ciarmoli with Guggenheim Securities.

**Michael Ciarmoli** (Analysts):
Nice results, and congrats to all. Lynn, it's certainly been a long time, and Kevin, Gary, looking forward to it.

**Lynn Bamford** (Executives):
Thanks, Mike.

**Michael Ciarmoli** (Analysts):
Just maybe to stay on Defense and kind of the budget situation. I mean, how are you guys thinking -- I know you talked about the base budget, but if we don't get any reconciliation funding, as you guys look at the portfolio, maybe thoughts on how some of those tough decisions, which programs or platforms or branches might be bill payers and how that might impact you? And I guess what I'm asking, can you accomplish your growth plans with just a base budget?

**Kevin Rayment** (Executives):
Yes. I think that's a good question. Yes, I think that, as I said earlier, I do believe from a sort of an Electronics perspective, we're into a lot of the major existing sort of base programs. And I think we feel confident in that from a continuous resolution perspective. And then obviously, from a reconciliation point of view, there are pieces in that, which are sort of associated with things like Golden Dome investments. But underlying it, I think we still continue to supply into many sort of ground programs like our IFPC project, which mentioned in our opening remarks. I think, again, we feel pretty confident that we got orders this year moving into next year. And we mustn't forget too, is, obviously, we have a great sort of centralization around sort of where we are in the U.S., but we have good foreign sales -- direct foreign sales, roughly about 10% of our portfolio. So that's encouraging as well from a Defense point of view.

**Michael Ciarmoli** (Analysts):
And then just maybe back to the AP1000. I mean if you do get this order before year-end, how should we be thinking about how long that translates into hitting the P&L from long lead materials? And then I guess one maybe outlier we get from investors, is there a scenario where some of these international AP1000s, the reactor coolant pumps can be purchased from China since they are manufacturing their own pumps?

**Gary Ogilby** (Executives):
Mike, I'll start with the first one. This is Gary here on as to the 2027 revenue profile. We've mentioned in the past that the revenue profile here follows a bell curve. And we would expect to see revenues here in 2027 on that order. Obviously, we won't -- I can't give you the specifics just yet. A lot of that will kind of come down to the timing here. But we do expect based on receiving the order in the fourth quarter here that we will have revenues associated with it in 2027.

**Kevin Rayment** (Executives):
I think just following up on the China question, obviously knew we supply the pumps with AP1000 into China. I think we feel very confident with the relationship we have with Westinghouse, again, sort of from a U.S. supply perspective. And we're scaling and sort of making sure we have the capacity to meet those respective sort of demands. But obviously, the regulatory issues associated with that, as I'm sure you've heard from Westinghouse, they very much want to make sure that the design stays exactly as it is going forward, which I think obviously is very good for us.

**Operator** (Operator):
And we will move next to Pete Skibitski with Alembic Global.

**Peter Skibitski** (Analysts):
Nice quarter and congrats to all. I'll echo that. Maybe this F-35 agreement guys that Lockheed announced obviously has to be finalized, but a 10-year agreement will provide a lot of visibility for your F-35 exposure. Can you maybe walk us through kind of revenue-wise, OE versus aftermarket on F-35 for you guys and then kind of what this agreement might allow you to do? Would it be helpful to margins? Would you have to give up some price? Just your thoughts on that.

**Kevin Rayment** (Executives):
Sure. I mean I think we end up going through sort of multi-lot agreements and sort of negotiations as we go through that sort of process. But the sort of recent press that was out there for that sort of 10-year profile, we very much agreed that it was sort of in line with our sort of plans of 156 aircraft a year, which incorporates both foreign sales as well as U.S. sales. We always go through a negotiation perspective as part of that exercise. But again, I'm not anticipating any significant sort of deviation from that. We do a lot directly with them on the F-35, and I feel good that we're in a good position.

**Peter Skibitski** (Analysts):
Okay. Sounds good. And just one follow-up. I'd just be interested to learn how much -- how CW can play into this Army NGC2 program. I know it's fairly new, but Anduril seems like it has a pretty big role on it. I don't know if you guys have already booked a position on that project, but I'd like to know specifically kind of how you guys think you could play a role there in terms of the tactical communications.

**Kevin Rayment** (Executives):
Yes. That actually fits quite well with us. In fact, on the 2 programs that are in the sort of trial process, we actually have hardware that we've worked with on NGC2 out of our PacStar business. And so it fits into both of those 2 respective programs. And we work closely with Anduril on that sort of deployment. So I think we're in that program.

**Operator** (Operator):
And we'll move next to Scott Deuschle with Deutsche Bank.

**Scott Deuschle** (Analysts):
Lynn or Kevin, is Curtiss-Wright's content on the APR1400 reactor the same as it is on the AP1000?

**Kevin Rayment** (Executives):
For the APR1400, it's different. It's a different size as the 1,400 versus the AP1000.

**Scott Deuschle** (Analysts):
So is the content higher? Or is it less?

**Kevin Rayment** (Executives):
No, we're on the AP1000.

**Lynn Bamford** (Executives):
Yes. I mean we have content on the APR1400, but it's lower around $20 million per plant. So it's -- we'll have content and we continue to engage on it, but it's not in the ballpark of the AP1000, which we always mentioned 110 plus for the RCPs and again, reiterate that on top of the RCPs, we have been awarded other work. And I think on top of the RCPs, we'll have $50 million, $60 million, $70 million of incremental content, which is quite meaningful on top of the RCPs.

**Scott Deuschle** (Analysts):
Okay. So I mean, just given that Korea is funding, I guess, some of these reactors in the U.S. is that a bit of a threat to how much content you ultimately can get on the build-out? Or do you think you guys still get a very strong share position here?

**Lynn Bamford** (Executives):
Yes. I mean our content -- I mean, as Kevin just said, Westinghouse has said, I mean, you can find it in very many places that they are determined to build a stable react plant design and not change things to help assure that end-of-a-kind cost down that is what the nuclear industry seeks. And with that, our content on the AP1000, we don't take it for granted. We have to earn it every day and be a great supplier to Westinghouse. 
But we have engaged -- I mentioned things like the $80 million investment in our Cheswick facility to make sure we're ready to ramp. Like we're doing our part. I had comments on supply chain readiness in the prepared remarks. And we engage very -- every day with Westinghouse to be a great supplier. And so I think the AP1000 will be the winner in the U.S. and as a U.S. design, and I think we are well positioned to support Westinghouse on that. So if an AP1400 gets built, so be it. But it's -- the AP1000, the Gen 3+ safety profile that I think is what people are going to want.

**Kevin Rayment** (Executives):
Yes. And the only other thing I would add is just to reiterate, both Cameco and Brookfield are still signaling nearly 91. So that's a pretty significant piece of work.

**Scott Deuschle** (Analysts):
And then just, Kevin, can you provide an update on what you're seeing across your own supply chain, both in terms of availability of supply, any constraints you're still facing? And just broadly, like what are you seeing in terms of supply chain inflation these days?

**Kevin Rayment** (Executives):
Yes, very good. I can answer that. I think sort of the area on the sort of supply chain side, if I sort of just take our Electronics piece, which is where we've seen sort of similar types of issues surrounding sort of electronic components. And that sort of dates back to like we did when we had sort of -- we were coming out of COVID. So when we went through that process last time, we learned a lot from that sort of exercise. So as we started to see some issues in our supply chain this year, certainly around memory and some sort of allocation for processes, we got ahead of the curve. We had a Tiger team put together. 
We've been advanced buying, obviously, those materials to overcome that. We've also been doing things like pushing forward with our DPAS ratings, which actually get sort of guarantee of secure for us. And we've been looking at second sourcing. And again, a number of initiatives to really make sure that we're getting ahead of the cycle. And some of that sort of flowed over a little bit into our industrial piece, which was a gain on the memory side. But in that sort of industry, it's a lot easier for us to sort of look at sort of dual sourcing. But again, I feel like in a good position as we go to the fourth quarter that we've sort of built up around that sort of experience and knowledge to basically manage that process. Yes, we've seen some pressure from, obviously, as everybody knows, the memory prices have been going up, but we're managing that with our suppliers and managing that with our customers.

**Operator** (Operator):
And we'll move next to Louie DiPalma with William Blair.

**Louie Dipalma** (Analysts):
Lynn, Kevin, Gary, and Jim it was a pleasure working with you, and congrats on your tremendous success. And Chris, I'm sure you're listening. It was great working with you as well. And Kevin, congrats on the big appointment. My question for Defense Electronics, you guys discussed the negative mix in the quarter. But over the long term and putting aside the quarter-to-quarter lumpiness, should the margin consistently increase further on an annual basis? Or should investors expect the margin to stabilize here in the high like 29% range?

**Gary Ogilby** (Executives):
Yes. So I'll comment on that, Louie. We are obviously very happy with the margins. They're industry-leading margins. When we think about the margin profile and we look out to the next few years, we do balance that and the investments that we need to make to grow the business for the medium and the long term. So that's something we have a lot of internal discussion about reviewing the R&D pipeline and where we want to make those strategic investments to be successful 5 years out from now. So it's top of mind for us. And overall, it's a really, really healthy margin profile.

**Louie Dipalma** (Analysts):
For the mix headwind that you discussed in the quarter, are you able to share what products within Defense Electronics have a lower margin than the overall portfolio? And like should this be a long-term headwind? Or is it something that was just temporary?

**Gary Ogilby** (Executives):
No, it's temporary. I would say when you span the year, it tends to wash out. It was a little bit more than it normally was in Q3. But 2 things. So one of the main things that we see in the Defense Electronics portfolio is something we've mentioned in the past, it's the margin profile on the cost versus the systems that can impact the quarterly lumpiness. But also, it wasn't just the mix. It's also some of those investments we mentioned in CRAD that really help us on the next-generation aircraft modernization platforms that we're looking to continue to gain content and gain share over the long term. So it was a combination of mix as well as some of those CRAD investments.

**Louie Dipalma** (Analysts):
Great. And for those next-generation aircraft platforms, does that include the CCA as well as like the 2 next-gen fighters that were awarded to Boeing?

**Kevin Rayment** (Executives):
Yes, I'll take that. Just yes, I mean, we do -- we're working closely on F-47 and F/A-XX. Obviously, we don't declare sort of where we are in our content, but that, again, is fueled by both our Defense Electronics businesses and also our aerospace group and sensors and actuation. So we're working on those specific platforms. Also MV-75, again, we actually have content on that platform, which is obviously our accident crash recorders with our sort of program there. 
And from a CCA perspective, yes, we're on both Increment 1 with both the Anduril and the General Atomics, both platforms. And again, we have content in our Defense Electronics piece in both of those particular pieces. We're working hard because as you know, Increment 2 is coming, and there are a number of other sort of additional players in that, and we're working very closely with them to ensure that we get positioned in the U.S. and around the world. There are other CCA type programs that are going into Europe, which we're again actively pursuing.

**Louie Dipalma** (Analysts):
Thanks, everyone. And yes, we also cover some Defense Electronics companies that have margins as high as 45%. And so I just wanted to get clarity on the continued margin expansion. And it seems like you guys are heading in the right direction. So thanks, everyone. Look forward to talking on the next quarter on the Analyst Day.

**Operator** (Operator):
[Operator Instructions] And we will move next to John Godyn with Citi.

**Bradley Eyster** (Analysts):
This is Bradley Eyster on for John Godyn. So I just want to touch base on the SMR side of the equation for commercial nuclear. Just curious what your thoughts are on demand expectations. So like how you need power, you see businesses trying to generate or capture power as possible through like any means necessary it seems. So I'm just curious if you can kind of level set expectations, how you see this market evolving and the opportunity you see here for Curtiss-Wright and maybe provide some color and thoughts on the speed of market for SMRs to meet these power needs.

**Lynn Bamford** (Executives):
So just maybe I'll talk a little bit on big picture. I think one of the strengths, which we say over and over is the strength of seeing Curtiss-Wright as an investment is we play across the nuclear power industry, whether it's keeping the current plants online, doing restarts, bringing back old plants that have been shuttered to building AP1000 to building the SMRs. 
And as you know, but just to reiterate it for anybody on the phone, we're not trying to pick winners and losers across the SMR landscape. Our goal has been mostly focused on the 300-plus megawatt reactors and targeting meaningful content. It was fun to be able to announce $100 million of content plus with Rolls-Royce so far with the awards we have, and we're not necessarily stopping there. And so -- you know where we are in AP1000. We've said we're above the $120 million mark with X-energy and continuing to work across the landscape. 
And we do work below the 300 megawatts. We're working with targeted micro reactors that where our value proposition matches how the plants are going to be built. And so how the SMRs are going to be folded into the overall picture for providing energy in the company. I mean that continues to evolve. But I think there really is broad understanding, not just here in the U.S., but overseas that there are places for the large gigawatt reactors, and there's a place for the small modular reactors in more remote communities and such. And so I think just broadly speaking, this is such an exciting part of our portfolio that is going to provide growth through the next decade for Curtiss-Wright in really a meaningful way.

**Bradley Eyster** (Analysts):
I also want to touch base on possibly the M&A side. You guys have pretty strong free cash flow generation. Just to get your latest thoughts on M&A. Is there any kind of opportunities you guys are looking at expansion of capabilities, content on existing platforms, securing the supply chain? Just any color here that can provide would be appreciated.

**Kevin Rayment** (Executives):
Sure. I can cover that. And then if Gary wants to add anything else in addition, you can. Just I would say is, again, the pipeline remains healthy. We're obviously always looking at multiple different books that are coming in across the organization. So it is certainly for me, again, and to reiterate, it has been for a while, is it is our #1 sort of priority from a capital deployment perspective. And again, across our sort of core markets. So we constantly look at that. 
I think you'll also see back from sort of Curtiss-Wright's view is that we take a very disciplined approach in which we've done that. The entire team are involved is right down to the business unit levels. We have a specific property, we do a lot of diligence, a lot of work on it. And we're also comfortable in that disciplined approach and saying no if it doesn't fit either strategically or financially. But we're still very much wanting to drive that forward. I'm going to talk a little bit more about Investor Day, some sort of evolution in some of our M&A piece to sort of assist us going forward. But I think that's a good position. Gary?

**Gary Ogilby** (Executives):
Sure. Thank you, Kevin. So I'll just kind of add in, as you mentioned, we do generate a lot of free cash flow, and we have a very healthy balance sheet. When we approach acquisitions from a financial lens, we are looking at those targets to see if they're going to be accretive to some of our core KPIs over time. So revenue, op margin, EPS and ROIC. And so we look at that, and we are evaluating that through that financial lens to see and make sure they're going to be accretive to our key KPIs over time. And as Kevin mentioned, it is one of our top capital allocation priorities.

**Operator** (Operator):
There are no further questions in queue at this time. I will now turn the meeting back to Lynn Bamford, Chair and Chief Executive Officer, for any additional or closing remarks.

**Lynn Bamford** (Executives):
I'd say thank you to everybody for joining us today, and we look forward to speaking with some of you on the road in the coming weeks and the release of our fourth quarter results. Have a great day.

**Kevin Rayment** (Executives):
Thank you.

**Operator** (Operator):
Thank you. This concludes today's Curtiss-Wright earnings conference call. Please disconnect your line at this time, and have a wonderful day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CW_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Lynn Bamford (CEO)｜guidance：全年銷售財測上調至 8%–9%（原話："Overall sales are now projected to increase 8% to 9%"）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：全年 EPS 財測上調至 $15.10–$15.40（原話："our full year 2026 diluted EPS guidance to a new range of"）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：全年自由現金流財測上調至 $585–605M（原話："record free cash flow of $585 million to $605 million."）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：第四季營益率預期超過 20%（原話："operating margin in excess of 20% to conclude the year."）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：第三季整體營收小幅成長、營益與利潤率與 Q2 持平（原話："sales to reflect modest growth relative to our second"）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：Defense Electronics 第三季營益與利潤率預期季減（原話："In addition, third quarter operating income and margin are"）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：地面防務全年展望維持不變，依戰術通訊產出時點（原話："the pipeline and growing strength in the 2026 order book"）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：商用核能第三季預期與上季持平（原話："Of note, we anticipate sales in this market to be flat"）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：一般工業全年成長指引 1%–3%，管理層稱仍偏保守（原話："conservative given the order book and the macro environment."）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：DE 第三季營收預期持平至下滑，第四季量大（原話："we will see relatively flat revenues to down in"）
- 2026-08-06｜Lynn Bamford (CEO)｜margin：Q2 營業利益成長快於銷售（原話："Operating income increased 12% year-over-year, exceeding"）
- 2026-08-06｜Chris Farkas (CFO)｜margin：A&I 利潤率擴張來源：吸收、組合（原話："180 basis points, respectively, driven by favorable"）
- 2026-08-06｜Chris Farkas (CFO)｜margin：DE Q2 利潤率 28%，來自組合與成本控制（原話："operating margin of 28%, up 120 basis points"）
- 2026-08-06｜Chris Farkas (CFO)｜margin：A&I 銷量吸收率口徑與有利產品組合（原話："levels, 20% to 25% on the higher sales, but favorable mix"）
- 2026-08-06｜Lynn Bamford (CEO)｜customer：DE 訂單年增近 50%（原話："orders grew nearly 50% year-over-year and are"）
- 2026-08-06｜Lynn Bamford (CEO)｜customer：Naval & Power Q2 訂單年減，歸因潛艦訂單時點（原話："orders were down year-over-year, principally due to the"）
- 2026-08-06｜Lynn Bamford (CEO)｜customer：IFPC 計畫預期獲 FY27 預算增資（原話："on track to receive another sizable increase in funding"）
- 2026-08-06｜Chris Farkas (CFO)｜customer：CFO 稱 Q3 訂單看來也不錯（原話："I think Q3 is shaping up to look pretty good as well."）
- 2026-08-06｜Lynn Bamford (CEO)｜customer：管理層稱 DE 延遲屬時點而非需求消失（原話："I do not believe there's any demand destruction."）
- 2026-08-06｜Chris Farkas (CFO)｜customer：工業車輛 on-highway 預期高個位數成長（原話："highway is going to be up high single digits for the year"）
- 2026-08-06｜Lynn Bamford (CEO)｜customer：潛艦大單對訂單流非劇烈改變（原話："but it isn't a dramatic change in our order flow or how our"）
- 2026-08-06｜Lynn Bamford (CEO)｜risk：供應鏈壓力上半年明顯增加（原話："definitely increased in the first half of this year."）
- 2026-08-06｜Lynn Bamford (CEO)｜risk：2026 營收所需供應大致已確保，重心轉 2027（原話："we're largely secured for our 2026 revenue and the real"）
- 2026-08-06｜Lynn Bamford (CEO)｜risk：對無法替代的材料以調價反映供應鏈壓力（原話："making sure we're adjusting our prices to reflect the"）
- 2026-08-06｜Lynn Bamford (CEO)｜risk：管理層稱獲 Micron 優先配貨（原話："we have been assured that we have priority allocation out"）
- 2026-08-06｜Lynn Bamford (CEO)｜risk：M&A 市場估值偏熱（原話："The market is a bit frothy right now"）
- 2026-08-06｜Lynn Bamford (CEO)｜competition：新創國防科技公司被視為成長機會，不聚焦 Tier 2/3（原話："it's a great growth opportunity for Curtiss-Wright."）
- 2026-08-06｜Lynn Bamford (CEO)｜competition：公司定位為 Tier 2 與 Tier 3 供應商（原話："We are a Tier 2 and the Tier 3 supplier, and that's"）
- 2026-08-06｜Lynn Bamford (CEO)｜product：Golden Dome 相關計畫尚未達量（原話："program that we have not seen reach volume yet,"）
- 2026-08-06｜Lynn Bamford (CEO)｜product：彈藥相關內容占比小（原話："not that we have no content, but it's relatively minor"）
- 2026-08-06｜Lynn Bamford (CEO)｜capital_allocation：M&A 仍是資本運用首要優先（原話："it is still our top priority for our use of CapEx"）
- 2026-08-06｜Lynn Bamford (CEO)｜capital_allocation：Cheswick 設施 $80M 多年期擴建（原話："multiyear investment to expand our Cheswick, Pennsylvania"）
- 2026-08-06｜Lynn Bamford (CEO)｜capital_allocation：MIB 資金累計獲授約 $95M，3 月底為 $70M（原話："Note, this award value was $70 million as of the end"）
- 2026-08-06｜Chris Farkas (CFO)｜capital_allocation：資本支出預計年增近 30%（原話："Please note that this guidance includes a nearly 30%"）
- 2026-08-06｜Lynn Bamford (CEO)｜commitment：預期今年取得 AP1000 訂單（原話："Overall, we continue to expect an AP1000 order this year."）
- 2026-08-06｜Lynn Bamford (CEO)｜commitment：研發投入成長快於銷售的承諾（原話："investing in R&D at a pace faster than sales for the"）
- 2026-08-06｜Lynn Bamford (CEO)｜commitment：預計 2027 Q2 投資人日公布新長期目標（原話："expect to share updated long-term financial targets during"）
- 2026-08-06｜Lynn Bamford (CEO)｜commitment：持續以中段十位數速度複利盈餘（原話："compound our earnings at a mid-teens pace over time."）
- 2026-08-06｜Lynn Bamford (CEO)｜commitment：預期超越 2024 投資人日全部主要財務指標（原話："We can confidently state that we are on track to exceed all"）
- 2026-08-06｜Lynn Bamford (CEO)｜commitment：長期目標細節留待投資人日（原話："And so we will hold the thunder until"）

### 問答異常語氣（迴避／改口／保留）
- CW_Q2_2026_Earnings_Call_20260806.md｜問：Baird 追問 DE 下半年營收有多少已在 backlog、需補多少 book-and-ship｜答法：CFO 明言不提供backlog 占比數字，改談 Q2 創紀錄與第四季量大
- CW_Q2_2026_Earnings_Call_20260806.md｜問：Baird 追問商用航空下半年隱含季減約 8% 的原因｜答法：CFO 未直接解釋商航季減，改談整體 A&I 財測上調、組合與重組效益
- CW_Q2_2026_Earnings_Call_20260806.md｜問：Morgan Stanley 問未來三年是否能支撐雙位數甚至中段十位數營收成長｜答法：CEO 未給數字，改談需求順風與 R&D 投入，並稱留待 2027 Q2 投資人日公布

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
{"date":"20260529","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"國防（尤其核海軍）需求結構性成長，訂單動能維持","columns":{"2Y 驗證點":"book-to-bill ≥ 1.1x；naval 段雙位數成長","5Y 驗證點":"Columbia-class 進入全速生產，潛艇含量倍增","10Y 驗證點":"潛艇建造節奏（Virginia 2+/yr、Columbia 1/yr）維持","具體數字門檻":"Naval 段營收 YoY ≥ +8%；book-to-bill ≥ 1.0x","信息來源":"公司法說 Q1'26（B2B 1.3x、backlog $4.3B）","漂移觸發條件":"連 2 季 TTM book-to-bill &lt; 1.0x → 削弱（2Y 假設）"}},{"id":"H2","text":"商業核電 renaissance 兌現：AP1000 RCP 訂單 + SMR 放量","columns":{"2Y 驗證點":"2026 內取得 ≥ 1 筆 AP1000 RCP 訂單；SMR 占商業核電 ≥ 12%","5Y 驗證點":"多座 AP1000 + 首批 SMR 進入交付（~$110M/AP1000）","10Y 驗證點":"SMR 成為商業核電主力，CW 跨設計商獨家位置變現","具體數字門檻":"SMR 占商業核電比重 2025 10% → 2026 12% → 2028 ≥ 20%","信息來源":"公司法說（SMR design→prototype shift）；Ultra Energy 整合","漂移觸發條件":"2026 無 AP1000 訂單 + SMR 占比未升 → 連 4 季偏離削弱（5Y 假設）"}},{"id":"H3","text":"Margin 擴張 + 高 FCF 轉換持續，支撐 EPS 複利","columns":{"2Y 驗證點":"Adj OPM ≥ 18%（FY26 guide 19-19.2%）；FCF 轉換 &gt; 100%","5Y 驗證點":"OPM 朝 20%+ 邁進，營運槓桿 + mix 升級","10Y 驗證點":"ROIC 維持 &gt; 15% 且 &gt; WACC","具體數字門檻":"Adj OPM TTM ≥ 17%；FCF/NI ≥ 1.0","信息來源":"FY26 guide（OPM 19-19.2%、FCF $580-600M &gt;105% 轉換）","漂移觸發條件":"連 2 季 TTM Adj OPM &lt; 17% → 削弱（2Y 假設）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"國防預算僵局 / CR 延後潛艇撥款，訂單動能放緩","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"book-to-bill、naval 段 YoY、國防授權法案進度","警戒閾值":"連 2 季 B2B &lt; 1.0x"}},{"id":"R2","text":"AP1000 RCP 訂單 2026 落空 / 大幅延後，核電敘事 air-pocket","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Westinghouse AP1000 客戶決策、CW 季度法說對訂單時點措辭","警戒閾值":"2026 全年無 AP1000 RCP 訂單公告"}},{"id":"R3","text":"估值倍數系統性壓縮（成長正常化或 sub-sector de-rating）","columns":{"對應假設":"H3 / 市場","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Fwd PE 5Y 分位、同業（HEI/HWM）倍數趨勢","警戒閾值":"Fwd PE 自高位回落但 EPS 未同步 → 股價 de-rate；需 ≥ 50% 機率才砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":747.73,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CW_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
