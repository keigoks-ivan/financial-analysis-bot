你是 stock-analyst **v20 判斷 agent**，標的 BWXT（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"BWXT","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWXT_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWXT_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":953.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）"},"note":"未查證（僅二手 Quiver 稱略低於共識，未採）"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益","value":149.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益","value":132.1,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）"}},{"id":"f_kpi5_2026","label":"管理層指引：2026 全年","value":null,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）"},"needs_sonnet":true},{"id":"f_kpi6_backlog","label":"Backlog","value":8556.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）"}},{"id":"f_kpi7_book_to_bill","label":"Book-to-bill（自算＝訂單÷營收，非公司揭露）","value":0.56,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","unit":"x","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-02","period":"2026-11-02","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-02"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_bwxt_gross_margin_pct","label":"BWXT 毛利率","value":22.61,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWXT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bwxt_operating_margin_pct","label":"BWXT 營業利益率","value":9.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWXT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bwxt_fcf_margin_pct","label":"BWXT FCF 利潤率","value":10.34,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWXT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lmt_gross_margin_pct","label":"LMT 毛利率","value":11.73,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LMT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lmt_operating_margin_pct","label":"LMT 營業利益率","value":11.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LMT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lmt_fcf_margin_pct","label":"LMT FCF 利潤率","value":10.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LMT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_rtx_gross_margin_pct","label":"RTX 毛利率","value":21.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RTX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_rtx_operating_margin_pct","label":"RTX 營業利益率","value":11.77,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RTX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_rtx_fcf_margin_pct","label":"RTX FCF 利潤率","value":9.51,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RTX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_noc_gross_margin_pct","label":"NOC 毛利率","value":20.02,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_noc_operating_margin_pct","label":"NOC 營業利益率","value":10.61,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_noc_fcf_margin_pct","label":"NOC FCF 利潤率","value":8.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gd_gross_margin_pct","label":"GD 毛利率","value":15.42,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GD.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gd_operating_margin_pct","label":"GD 營業利益率","value":10.37,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GD.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gd_fcf_margin_pct","label":"GD FCF 利潤率","value":10.22,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GD.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":150.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）"}},{"id":"f_kpi4_sbc","label":"SBC（九個月累計，季度未單獨揭露）","value":29.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-02）","citation":"公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":119.52,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-41.62,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":34.91,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.21,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.74 → 4.75）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.19,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.16 → 5.17）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.51,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.89 → 5.86）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":4.75,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":5.17,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":5.86,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.21,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 4.74 → 4.75（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":29.37,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝26.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":26.9,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.04,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝25.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":25.6,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.45,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝20.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":20.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":25.16,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 4.75，分子＝快照價 119.52","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.887,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1453.35,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 2021.88、現金 568.53（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":91.63,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":12404.39,"period":"2026-11-08","unit":"USD m","basis":"市值 10951.04 ＋ 淨負債 1453.35","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":3795.92,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":4097.34,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（15 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.27,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 119.52 / W52 182.05 / W104 158.59 / W250 107.29 / W250 13週斜率 1.25%"},{"id":"f_ma_w52","label":"52 週均線","value":182.05,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":158.59,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":107.29,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.25,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"10-K FY2025：美國政府核部件與燃料因技術、法規與資本門檻，競爭有限；主要對手列有 Bechtel、Fluor、Northrop、HII、Westinghouse 等。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1486957/000148695726000007/bwxt-20251231.htm","excerpt":"Because of the technical and regulatory standards required to meet U.S. Government contracting requirements for nuclear components and fuel and the barriers to entry present in this type of environment, competition is limited.","as_of":"2026-02-23","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K FY2025：商用部門對手含 Framatome、Cameco、Doosan、AECON、Westinghouse、AtkinsRéalis；核醫對手含 Curium、SHINE、Jubilant。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1486957/000148695726000007/bwxt-20251231.htm","excerpt":"This segment competes with a number of companies specializing in nuclear capabilities including, but not limited to, Framatome, Cameco Corporation, Doosan Heavy Industries & Construction Co., Ltd., AECON Group Inc., Westinghouse Electric Corporation and AtkinsRéalis.","as_of":"2026-02-23","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：無法保證現有技術維持競爭力或不被競爭技術顛覆。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1486957/000148695726000007/bwxt-20251231.htm","excerpt":"there can be no assurance that the current technologies that our business relies upon will remain competitive, or that competing technologies will not disrupt our business.","as_of":"2026-02-23","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K FY2025 describes BWXT as supplier of precision naval nuclear components, reactors and fuel to the DOE/NNSA Naval Nuclear Propulsion Program (the customer relationship) and as supplier of proprietary and sole-source valves, manifolds and fittings; no second-source or in-house program disclosed in the filing excerpt or searches.","source":"SEC EDGAR 10-K FY2025, Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/1486957/000148695726000007/bwxt-20251231.htm","excerpt":"Through this segment, we engineer, design and manufacture precision naval nuclear components, reactors and nuclear fuel for the U.S. Department of Energy (\"DOE\")/National Nuclear Security Administration's (\"NNSA\") Naval Nuclear Propulsion Program and we have over 100 years of experience in supplying components for defense applications.","as_of":"2026-02-23","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"美國政府占 FY2025 合併營收約 68%（FY2024 76%、FY2023 75%）；無單一非政府客戶超過 10%。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1486957/000148695726000007/bwxt-20251231.htm","excerpt":"During the years ended December 31, 2025, 2024 and 2023, the U.S. Government represented approximately 68%, 76% and 75% of our total consolidated revenues, respectively. No individual non-U.S. Government customer accounted for more than 10% of our consolidated revenues in the years ended December 31, 2025, 2024 or 2023.","as_of":"2026-02-23","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"四家大型公用事業客戶占 FY2025 營收約 17%（14%、14%）；其應收占淨應收 50%（前一年 19%）；美政府直接/間接應收占 28%（前一年 40%）。","source":"SEC EDGAR 10-K FY2025 Note 12","url":"https://www.sec.gov/Archives/edgar/data/1486957/000148695726000007/bwxt-20251231.htm","excerpt":"revenues from four large utility customers accounted for approximately 17%, 14% and 14% of our total consolidated revenues, respectively. Accounts receivable due directly from four large utility customers represented 50% and 19% of net receivables at December 31, 2025 and 2024, respectively.","as_of":"2026-02-23","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"報導稱 Moody's 於 2026-10 將 BWXT 展望由穩定調為正向、確認 Ba1 發行人評等（二手德文報導，未核 Moody's 原文）。","source":"Börse-Express：BWX Technologies Aktie: Moody's hebt Ausblick an","url":"https://www.boerse-express.com/news/articles/bwx-technologies-aktie-moodys-hebt-ausblick-an-951852","excerpt":"Medienberichten zufolge hob die Agentur am Montag den Ausblick für den US-Konzern von zuvor stabil auf positiv an.","as_of":"2026-10-09","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"A&D 供應鏈壓力預期至少持續到 2027（Deloitte 展望的二手摘要）；搜尋未見任何 2026–2027 過剩來源","source":"Deloitte midyear update aerospace and defense industry outlook","url":"https://www.deloitte.com/us/en/insights/industry/aerospace-defense/midyear-update-aerospace-and-defense-industry-outlook.html","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Bain：供應鏈限制被列為近 90% 受分析 A&D 專案提產的主要障礙；PwC/AIA 調查：3 倍提產時 33% 受訪者看不到任何時程可達成","source":"Bain Analysis: Aerospace Sourcing Faces Capacity Crisis (Procurement Magazine); PwC State of the Ramp","url":"https://procurementmag.com/news/bain-analysis-aerospace-sourcing-faces-capacity-crisis","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"國防需求：FY2027 國防預算提案 1.5 兆美元，較現水準高約 42%，但屬提案、國會路徑未定","source":"Zacks Industry Outlook (Nasdaq); Defense Daily","url":"https://www.nasdaq.com/articles/zacks-industry-outlook-highlights-ge-aerospace-rtx-and-general-dynamics","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"BWXT 2026 Q2 後合併在手訂單約 84 億美元，較前季微降（Q1 為約 87 億）；海軍反應爐合約據稱提供未來 6–8 年營收能見度；政府業務約占營收 2/3；2026 指引高個位數至十幾% 營收成長，商用 +25%","source":"Nasdaq/Zacks: How Is BWXT Strengthening Revenue Visibility Through Backlog?; Motley Fool BWXT report","url":"https://www.nasdaq.com/articles/how-bwxt-strengthening-revenue-visibility-through-backlog","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.H","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"加拿大競爭局調查 BWXT 以 5.25 億美元收購 Kinectrics 是否實質減損加拿大核醫學領域競爭；2025-11 聯邦法院核准擴大調查令，納入 Novartis 及其子公司。搜尋未見 2026 年結案或挑戰的消息；未見美國 DOJ/FTC 或歐盟行動。","source":"Law360 Canada: Competition Bureau seeks Novartis data in BWX–Kinectrics merger probe（搜尋摘要）","url":"https://www.law360.ca/ca/articles/2413932","excerpt":null,"as_of":"2025-11-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2025 年報：行政命令 EO 14372 可能限制關鍵國防承包商發放股息、買回庫藏股、調薪及激勵指標，預期以新 DFARS 條款實施。","source":"BWXT FY2025 Annual Report to Shareholders (ARS)","url":"https://www.sec.gov/Archives/edgar/data/1486957/000148695726000020/bwxtechnologiesinc2025annu.pdf","excerpt":"In addition, the President recently issued Executive Order (\"EO\") 14372 that could limit certain contractors performing work under critical defense weapons, supplies, and equipment contracts from issuing dividends or distributions, share repurchases, increasing executive salaries, and using particular metrics to determine executive incentive","as_of":"2026-03-01","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"BWXT 10-K 風險因素揭露：在加拿大有重型核能組件與醫用同位素製造，產品可能售予美國客戶，新增或提高關稅會推升產品、零組件與原料成本、壓縮毛利；最終影響取決於關稅實施與否、時點、合約條款與範圍。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1486957/000148695726000007/bwxt-20251231.htm","excerpt":"Uncertainty remains with respect to trade policies and treaties between the U.S. and other countries, including Canada, where we manufacture heavy nuclear components and products for our medical radioisotopes business that may be sold to US customers.","as_of":"2026-02-23","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K 亦揭露須遵守美國出口管制法規（涉及特定產品與技術資訊出口），不合規可能遭罰款或暫停／禁止承接美國政府合約。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1486957/000148695726000007/bwxt-20251231.htm","excerpt":"U.S. export control laws governing the export of certain products and technical information.","as_of":"2026-02-23","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"BWXT 為美國國內高濃縮鈾(HEU)/HALEU 鋁包殼板型研究及測試反應爐燃料組件的唯一國內供應商（單一來源）；搜尋摘要轉述，未取得逐字原文","source":"BWXT Advanced Fuels Brochure 05-2026 / 搜尋摘要","url":"https://www.bwxt.com/wp-content/uploads/2026/05/Advanced-Fuels-Brochure-Digital-05-2026.pdf","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"BWXT 於田納西州 Oak Ridge 開設離心機製造開發設施，目標重建完全國內的鈾濃縮能力，減少對外國來源依賴；HALEU 供應目前由俄羅斯與中國主導（評論轉述）；未取得逐字原文","source":"BusinessWire, BWXT Launches New Era of Domestic Uranium Enrichment (2026-01-26)","url":"https://www.businesswire.com/news/home/20260126595408/en/BWXT-Launches-New-Era-of-Domestic-Uranium-Enrichment-for-National-Security-in-Oak-Ridge-Tennessee/","excerpt":null,"as_of":"2026-01-26","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"BWXT 10-K/年報風險因子與廠址揭露（FY2025 ARS）可能載明供應鏈與單一來源風險","source":"BWXT FY2025 Annual Report (SEC ARS)","url":"https://www.sec.gov/Archives/edgar/data/1486957/000148695726000020/bwxtechnologiesinc2025annu.pdf","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"3Q26 營收 $953.0M；Government Operations $639.1M（去年同期 $616.7M），成長來自 special materials 與 advanced nuclear，部分被海軍推進量下降抵銷；Commercial Operations $314.2M（去年同期 $251.0M，約 +25%）。","source":"BWXT 10-Q 2026-09-30 (SEC) / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001486957/000148695726000051/bwxt-20260930.htm","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"管理層收緊 2026 non-GAAP EPS 指引至 $4.72-$4.77，並給 2027 初步展望為高個位數營收成長。","source":"BWX Technologies Reports Third Quarter 2026 Results (finviz)","url":"https://finviz.com/news/413531/bwx-technologies-reports-third-quarter-2026-results","excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q1 2026 總 backlog 約 $8.7B（年增 77%）；政府 backlog 近 $7B（含 Naval Reactors 定價協議第二部分 $1.4B）；商業 backlog 季比持平、年增 33%，支持 2026 商業電力低十位數有機成長指引。","source":"BWXT Q1 2026 earnings call 摘要 (MarketBeat/Barchart)","url":"https://www.marketbeat.com/instant-alerts/bwx-technologies-q1-earnings-call-highlights-2026-05-04/","excerpt":null,"as_of":"2026-05-04","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"BWXT 為加拿大首座 GE Hitachi BWRX-300 SMR 的反應爐壓力容器供應商；Q2 2026 合併 backlog 據 Motley Fool 較上季略降（未對主要文件核實）。","source":"搜尋摘要（Motley Fool 引述）","url":"https://www.fool.com/report/nyse-bwxt/?partner=yahoo","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"3Q26 分部營收 Government $639.1M／Commercial $314.2M","source":"BWXT 8-K ex99.1","url":"https://www.sec.gov/Archives/edgar/data/0001486957/000148695726000053/bwxt_93026xerexhibit991.htm","excerpt":"The Government Operations increase was driven by growth in special materials and advanced nuclear, partially offset by lower volume in naval propulsion. The Commercial Operations increase was driven by growth in commercial nuclear components, services and medical, partially offset by","as_of":"2026-11-02","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"BWXT 10-K 風險因素自述：無法保證現有技術維持競爭力，也無法保證競爭技術不會衝擊業務；醫用同位素領域可能出現替代技術的競爭者，且可能更早商業化或有成本優勢。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1486957/000148695726000007/bwxt-20251231.htm","excerpt":"Additionally, there can be no assurance that the current technologies that our business relies upon will remain competitive, or that competing technologies will not disrupt our business.","as_of":"2026-02-23","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"搜尋摘要：TRISO 燃料供應商少，X-energy 旗下 TRISO-X 為最接近的競爭者，Oak Ridge TX-1 於 2026-02-13 取得 NRC 許可；DOE 2025-09 同時有條件選定 TRISO-X 與 Valar Atomics 進入燃料產線試點。","source":"Sacra 分析（搜尋摘要）","url":"https://sacra.com/chat/h/4bfd2d11-7c4a-45e0-8a8f-6a10c14ffaed/","excerpt":"TRISO-X received an NRC license for its Oak Ridge TX-1 facility on February 13, 2026.","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"BWXT 獲選於 Fort Campbell 部署 20MW 微型反應爐（Army Janus），報導稱公司轉向 vendor-owned 營運模式、直接向設施售電","source":"MarketBeat: BWX Technologies army reactor win could redraw its nuclear growth story","url":"https://www.marketbeat.com/articles/bwx-technologies-army-reactor-win-could-redraw-its-nuclear-growth-story/","excerpt":"BWX Technologies was selected to deploy a 20-megawatt electric BANR microreactor at Fort Campbell under the Army’s Janus program. The Army program helps validate BWX Technologies’ commercial microreactor strategy while shifting some early deployment risk into a milestone-based federal framework.","as_of":"2026-08-28","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 7月底快照：16 位分析師（12 Buy/2 Hold/2 Sell），平均目標價 $193；JP Morgan 7/27 以 $230 初評，Seaport 6/18 升評 Buy 目標 $245。","source":"Benzinga BWXT price-targets","url":"https://kr.benzinga.com/quote/BWXT/price-targets","excerpt":"Analyst Consensus — 16 Analysts, 12 Buy, 2 Hold, 2 Sell, with an average consensus price target of $193, upside to the average price target of +14.7%.","as_of":"2026-07-28","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 5/11：共識 Moderate Buy，平均目標價 $217.96（Truist 升至 $212、Hold）。","source":"MarketBeat Truist raises BWXT PT","url":"https://www.marketbeat.com/instant-alerts/truist-financial-increases-bwx-technologies-nysebwxt-price-target-to-21200-2026-05-11/","excerpt":"the stock has an average rating of \"Moderate Buy\" and a consensus price target of $217.96.","as_of":"2026-05-11","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026 指引一路上修：Q1(5/4) EPS 4.60–4.75、Q2(8/3) 上修至 4.70–4.80（含 7/1 完成的 PCG 併購）、營收約 $3.8B；Q2 前共識 EPS $4.61，指引高於共識。","source":"MarketBeat FY2026 guidance 2026-08-03 / BusinessWire 2026-05-04","url":"https://www.marketbeat.com/instant-alerts/bwx-technologies-nysebwxt-issues-fy-2026-earnings-guidance-2026-08-03/","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"最新 8-K（期間 9/30/26，Q3）：營收指引維持約 $3.8B，調整後 EBITDA 約 $667M、non-GAAP EPS 4.72–4.77、FCF 350–360M，為縮窄區間；2026 年未見下修。發布日未確認。","source":"SEC 8-K Exhibit 99.1 (9/30/26)","url":"https://www.sec.gov/Archives/edgar/data/0001486957/000148695726000053/bwxt_93026xerexhibit991.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"+","claim":"BWXT 2026-04-20 宣布收購 Precision Components Group（PCG，2025 年營收約 1.25 億美元），新聞稿稱 2026-07-06 完成（10-Q/A 稱 7/1，日期有出入）；併入 Commercial Operations 部門。","source":"BWXT 新聞稿 Completes Acquisition of Precision Components Group（經 WebSearch 彙整）","url":"https://investors.bwxt.com/news-releases/news-release-details/bwxt-completes-acquisition-precision-components-group-expanding","excerpt":null,"as_of":"2026-07-06","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"10-Q/A 載 2026-07-31 BWXT 簽署definitive agreement，將醫療事業（BWXT Medical 與 Kinectrics 穩定醫療同位素業務）以最高 8 億美元出售給 Nordic Capital（搜尋摘要轉述，未讀原頁）。","source":"SEC EDGAR 10-Q/A（截至 2026-06-30）","url":"https://www.sec.gov/Archives/edgar/data/0001486957/000148695726000044/bwxt-20260630.htm","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共9份，含重大項目者3份：2025-11-10 發行 12.5 億美元 0% 可轉債 2030 與新信貸；2026-11-03 信貸修訂；2026-11-04 發行 5 億美元 2034 優先債並對 2028/2029 票據發動收購要約。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001486957&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-04-20 宣布收購 PCG，新聞稿稱 2026-07-06 完成；另 2026-07-31 簽約出售醫療事業予 Nordic Capital（最高 8 億美元）。","source":"BWXT 新聞稿 / SEC 10-Q/A（WebSearch 彙整）","url":"https://investors.bwxt.com/news-releases/news-release-details/bwxt-completes-acquisition-precision-components-group-expanding","excerpt":null,"as_of":"2026-07-06","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 12 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"BWXT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":22.61,"operating_margin_pct":9.83,"fcf_margin_pct":10.34,"rd_intensity_pct":0.44},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BWXT","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"LMT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":11.73,"operating_margin_pct":11.78,"fcf_margin_pct":10.59,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LMT","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"RTX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":21.1,"operating_margin_pct":11.77,"fcf_margin_pct":9.51,"rd_intensity_pct":2.97},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RTX","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"NOC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":20.02,"operating_margin_pct":10.61,"fcf_margin_pct":8.78,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NOC","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"GD","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.42,"operating_margin_pct":10.37,"fcf_margin_pct":10.22,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GD","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"BWXT"},"financial_history":{"ticker":"BWXT","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":2232834000.0,"revenue_yoy_pct":null,"gross_margin_pct":24.72,"operating_margin_pct":13.8,"net_income":238191000.0,"diluted_eps":2.6,"free_cash_flow":46392000.0,"fcf_margin_pct":2.08,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":2496309000.0,"revenue_yoy_pct":11.8,"gross_margin_pct":24.86,"operating_margin_pct":13.35,"net_income":245849000.0,"diluted_eps":2.68,"free_cash_flow":212415000.0,"fcf_margin_pct":8.51,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2703654000.0,"revenue_yoy_pct":8.31,"gross_margin_pct":24.23,"operating_margin_pct":12.17,"net_income":281941000.0,"diluted_eps":3.07,"free_cash_flow":254781000.0,"fcf_margin_pct":9.42,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":3198425000.0,"revenue_yoy_pct":18.3,"gross_margin_pct":22.91,"operating_margin_pct":10.15,"net_income":328945000.0,"diluted_eps":3.58,"free_cash_flow":295291000.0,"fcf_margin_pct":9.23,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/BWXT/BWXT_Q3_2026_Earnings_Call_20261102.md）

# Q3 2026 Earnings Call
**BWX Technologies, Inc.** | Earnings Calls | 2026-11-02

**Operator** (Operator):
Ladies and gentlemen, welcome to BWX Technologies Third Quarter 2026 Earnings Conference Call. [Operator Instructions] I would like to turn the call over to our host, Chase Jacobson, BWXT's Vice President of Investor Relations. Please go ahead.

**Chase Jacobson** (Executives):
Thank you. Good evening, and welcome to today's call. Joining me are Rex Geveden, President and CEO; and Mike Fitzgerald, Senior Vice President and CFO. 
On today's call, we will reference the third quarter 2026 earnings presentation that is available on the Investors section of the BWXT website. We will also discuss certain matters that constitute forward-looking statements. These statements involve risks and uncertainties, including those described in the safe harbor provision found in the investor materials and the company's SEC filings. 
We will frequently discuss non-GAAP financial measures, which are reconciled to GAAP measures in the appendix of the earnings presentation that can be found on the Investors section of the BWXT website. 
I would now like to turn the call over to Rex.

**Rex Geveden** (Executives):
Thank you, Chase, and good evening to all of you. Just over a month ago at Investor Day, we outlined our path to $5.5 billion to $6 billion of revenue and $1.1 billion to $1.2 billion of Adjusted EBITDA by 2030, supported by our predictable core, significant incremental organic growth opportunities, focus on operational excellence and disciplined capital allocation.
Our third quarter results reinforce that guidance with 10% revenue growth and 19% Adjusted EBITDA growth, including double-digit growth in both operating segments. Our businesses continue to execute well. We are converting opportunities into meaningful new awards, and we are expanding the industrial capabilities needed to support the next phase of nuclear growth.
The demand environment remains exceptionally strong. The need to address economic, national and energy security challenges globally is driving increased investment by our customers in nuclear national security and commercial power markets. Our national security customers are investing to reconstitute strategic deterrence capabilities that diminished after the Cold War and to radically improve energy resilience. Our commercial customers are investing in sustaining and growing their nuclear power generation fleets.
Funding is coming from public and private sources, and there is solid bipartisan political support. What differentiates BWXT is our ability to translate that demand into executable programs and sustained financial growth. Our technical capabilities, industrial scale and position in the nuclear value chain enable us to deliver integrated solutions for our customers and capture opportunities across these markets.
Turning to our segment results and outlook. The Government Operations delivered a strong quarter with good operating performance across business lines, driving Adjusted EBITDA margin of 22.6%, reflecting the continued benefit of improved efficiency, operational discipline and higher manufacturing volume. In Naval Propulsion, we booked our annual fuel contract for $189 million and are actively negotiating the next multiyear pricing agreement.
In Special Materials, our defense fuels enrichment and high-purity depleted uranium programs continue to ramp, driving the majority of Government Operations revenue growth in the quarter. For defense fuels, we are designing an HEU enrichment facility in Erwin, Tennessee, and industrializing centrifuge technology in our Oak Ridge facility. We remain on track to test a prototype centrifuge by the end of this year.
On HPDU, as part of our $1.6 billion contract to produce 300 metric tons of high-purity depleted uranium annually, we initiated construction of a new large-scale facility in Jonesborough, Tennessee, that will drive meaningful revenue growth in the fourth quarter and through 2027.
Our technical services teams once again boosted earnings in the quarter with outperformance on key programs, including Hanford and Savannah River, among others. From a business development standpoint, we were selected to provide a conceptual design for a lithium processing facility at the Y-12 National Security Complex in support of strategic deterrence. We expect the down selection for the next phase of this program in the first half of 2027.
Further, our technical services team is rapidly adopting AI to drive site performance and generate operating efficiencies. This further differentiates TSG as we develop new growth opportunities in that business to augment our base of predictable core earnings.
Moving to Advanced Nuclear. It was a busy quarter for operations and business development. We completed the core barrel assembly for Project Pele. And just a few weeks ago, we hosted Energy Secretary Chris Wright at the BWXT Innovation Campus to see our progress firsthand before we deliver the reactor to Idaho National Laboratory next year.
We also secured new wins for the BWXT advanced nuclear reactor called BANR. We were selected for the U.S. Army's Janus Program that aims to install more than 20 microreactors of various sizes across 5 military bases. We are working through the first phase of the contract, including final site selection at Fort Campbell, initiating nuclear regulatory processes and TRISO fuel production.
In parallel, we are working with our partners to fully define the program's costs, execution approach and operating plan. In addition, BANR was selected by Prodigy Clean Energy for its transportable nuclear power plant project in Belledune, New Brunswick, Canada, our first international microreactor win.
This is an excellent example of cross-segment collaboration as it brought together capabilities from our advanced nuclear teams from Lynchburg and commercial power and Kinectrics teams from Ontario, which will supply chain development and licensing services to Prodigy, highlighting the benefits of our broad capabilities across the nuclear value chain.
And lastly, we entered into a multiyear agreement to supply an initial allocation of 1 metric ton of TRISO fuel to Antares, our first large-scale commercial customer. This fuel will be manufactured in Lynchburg on the same TRISO production line used for Project Pele, the Antares Mark-0 criticality demonstration reactor and others. We will also manufacture TRISO for the Janus Program on that line.
These awards are tangible proof of BWXT's leading position in the advanced nuclear market as we uniquely combine microreactor technology, TRISO fuel manufacturing and life cycle services into a differentiated integrated offering.
Turning now to Commercial Operations. Organic revenue increased 15% and total revenue grew 25%, driven by double-digit growth in commercial power, Kinectrics and medical, along with contribution from the PCG acquisition. During the quarter, we completed the expansion of our Cambridge facility and began utilizing new sections of the plant.
The expansion increases our heavy component manufacturing capacity by about 50% and will improve operating efficiency and throughput as we execute on our deep backlog associated with CANDU life extensions and SMR projects and other new awards.
In the United States, we are finalizing design details for a new commercial manufacturing facility for large steam generators and reactor pressure vessels. The expansion will complement our existing operations and amplify our role as a super merchant supplier of critical, highly engineered nuclear components. We intend to make a final investment decision by the end of the year.
In Europe, we are also seeing high interest in nuclear power, particularly in markets where energy security is a national priority. I recently met with government officials and business leaders in Poland, where there is a strong appetite for nuclear power to address their energy security and decarbonization goals.
Specific to BWXT, there is a meaningful opportunity to deploy microreactors there and participate in the SMR supply chain. Any decision to invest in manufacturing capacity in Poland would be backed by firm orders and appropriate government partnerships. Commercial nuclear demand is precipitating rapidly on a global scale now, and we continue to expect to convert that demand into firm orders in 2027 and in the years to come as the trickle becomes a flood.
With that, I will turn the call over to Mike.

**Michael Fitzgerald** (Executives):
Thanks, Rex, and good evening, everyone. I'll begin with total company financial highlights on Slide 4 of the earnings presentation. Third quarter revenue was $953 million, up 10% year-over-year, including 7% organic growth. Strong Commercial Operations performance was complemented by steady growth in Government Operations.
Adjusted EBITDA increased 19% to $180 million, driven by double-digit growth in both operating segments, partially offset by higher corporate expense as we continue to invest for the future. Adjusted earnings per share increased 26% to $1.26, driven largely by higher operating income as nonoperating benefits from lower interest expense and a lower tax rate were partially offset by lower other income.
Third quarter free cash flow was $151 million, reflecting strong earnings, favorable advanced billings and disciplined working capital management. Given our year-to-date performance, we raised the low end of our 2026 free cash flow guidance, resulting in a revised range of $350 million to $360 million.
We continue to expect capital expenditures of approximately 6% of revenue in both 2026 and 2027. These investments are focused on expanding our manufacturing capacity, scaling fuel capabilities and supporting programs where we see significant long-term demand.
Our improving credit profile, including Fitch's inaugural investment-grade rating and Moody's positive outlook revision reinforces the strength of our financial position and provides flexibility as we execute on our disciplined capital allocation strategy.
As we discussed at Investor Day, our top capital allocation priority is investing in attractive organic growth opportunities, maintaining the capacity to pursue disciplined acquisitions and return capital to shareholders when appropriate. We continue to view balance sheet flexibility as an important competitive advantage as BWXT executes on its next phase of growth.
Moving to the segment results on Slide 6. Government Operations revenue increased 4%, driven by growth in Special Materials and Advanced Nuclear, partially offset by modestly lower Naval Propulsion revenue from reduced materials procurement compared with a strong prior year quarter.
Adjusted EBITDA was $144 million, representing a margin of 22.6% and up 22% from last year, supported by strong operational performance, productivity improvements and higher technical services equity income. As we look ahead, we remain focused on sustaining productivity improvements in our established businesses while scaling special material programs, supporting our expectation for Adjusted EBITDA growth broadly in line with revenue in 2027.
Turning to Commercial Operations. Revenue increased 25%, including 15% organic growth, driven by increases in commercial power, Kinectrics and medical plus the contribution from the PCG acquisition, which closed in early July. Growth in commercial power and Kinectrics reflected the continued strength of our Canadian components manufacturing and services businesses as well as increased engineering services revenue in the United States.
Adjusted EBITDA in the segment grew 17% to $41 million. Adjusted EBITDA margin in the quarter was 13.2% as higher volume and good execution more than offset mix and continued investments to scale the business for future growth.
Turning to our consolidated guidance for the remainder of 2026 and our preliminary outlook for 2027. In 2026, the assumptions in our operating guidance are unchanged. We anticipate Adjusted EBITDA of approximately $667 million and adjusted earnings per share to be $4.72 to $4.77, both at the midpoint of the previous guidance ranges.
Looking ahead to 2027, our preliminary outlook reinforces the financial trajectory outlined at Investor Day. We expect high single-digit to low double-digit growth in Adjusted EBITDA and adjusted earnings per share. Importantly, we expect this growth to be driven by continued expansion in our core businesses, increased contributions from Special Materials and ongoing improvements in operational execution and productivity.
2026 has been an exceptionally strong year, and we have a solid foundation for continued earnings growth in 2027, primarily supported by our existing businesses and programs with additional opportunities as new programs and commercial awards progress.
Within Government Operations, we expect high single-digit to low double-digit revenue and Adjusted EBITDA growth. Special Materials will remain a significant growth driver, complemented by increased Naval Propulsion and Advanced Nuclear activity. We expect continued productivity improvements and operational execution to help offset the margin mix effects associated with scaling new programs.
In Commercial Operations, we expect high single-digit organic revenue growth and low single-digit total revenue growth due to the planned medical divestiture, which is on track to close later this year. Organic revenue growth will be supported by our components manufacturing and services businesses.
We also expect Commercial Operations Adjusted EBITDA margins to improve by 50 to 100 basis points, reflecting higher volume, continued operational improvements and better absorption of growth investments, resulting in high single-digit Adjusted EBITDA growth.
From a cash perspective, we expect another year of solid generation in 2027 with free cash flow anticipated to be flat to slightly higher compared to 2026. While earnings growth should support increased operating cash flow, we expect continued investments in working capital and capital expenditures to support the significant growth opportunities across our business.
We remain focused on disciplined cash conversion and capital deployment as we execute our long-term growth strategy. Importantly, our preliminary 2027 outlook remains consistent with the longer-term financial framework presented at Investor Day and reinforces our confidence in achieving our 2030 targets.
Overall, we had a solid quarter. Our focus on operational excellence, converting our bid pipeline into firm awards and driving profitable growth, combined with our strong balance sheet and disciplined capital allocation strategy positions us well to deliver another strong year in 2027. 
With that, I'll turn it back to Rex for closing remarks.

**Rex Geveden** (Executives):
Thanks, Mike. To date, 2026 has been an excellent year for BWXT, and I'm excited about what lies ahead. As we close, I will leave you with 3 thoughts.
First, our core businesses continue to deliver strong predictable performance, providing the foundation for our long-term growth. Second, the opportunities we discussed at Investor Day are blossoming. We are securing new contracts, executing on strategically important programs and investing in the industrial capacity needed to grow the business.
And third, our focus remains on execution. We recognize the significant opportunities ahead of us and know that long-term value creation depends on converting those opportunities into profitable growth and strong cash generation. BWXT is exceptionally well positioned to do that, and our performance this quarter underscores our confidence in the 2030 financial targets we established at Investor Day. 
With that, we look forward to your questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Matt Akers with BNP Paribas.

**Matthew Akers** (Analysts):
I wonder if you could touch on a little bit more on the Government Operations margins. It was a really good quarter. And I know you guys -- you called out the equity income, I think even excluding that was pretty good. So if you could just kind of talk through kind of the big drivers there.

**Michael Fitzgerald** (Executives):
Yes. So thanks, Matt. Look, we're really, really proud of kind of the execution that we're performing within Government Operations. We've seen a significant increase in our overall margin from our expectations at the beginning of 2026.
I think when you get down to it and really what's happening is we're seeing a substantial increase in the efficiency of the volume of the work that we performed specifically in our naval nuclear business. So those contracts are performing very well. We're very focused on managing our volume so that it's highly efficient work. And we're seeing the results of that. So excited to see that.
I think if you look at some of the newer programs that we've talked about, no major changes there. I think that the growth on those programs, they're performing well, but they're in early stages. And as we've discussed before, we don't take large margin adjustments on those until we get further along from a progress standpoint. So what you're seeing is really excellence in the efficiencies of our core business. And certainly, it's great to see.

**Matthew Akers** (Analysts):
Yes. And then -- was there backlog acquired as part of the PCG deal? It looks like your commercial backlog is up a bit. And if so, can you talk about what that is, sort of how that runs off and how that fits in with your plan to kind of use that capacity for BWXT work?

**Michael Fitzgerald** (Executives):
Yes, that's right. I mean, so when we announced the PCG deal, what we had said at the time was that there was still -- most of that business, I think, 75% to 80% of that business was still in the kind of naval work and ultimately, the rest is commercial. We had close to $500 million in backlog associated with that transaction. So that came on to the books associated with that.
That will burn off over a period of time. I mean the thing that's encouraging is we're seeing growth in the PCG business. But as we stated before, a lot of the -- if you look at the capacity, we thought that the factories were about 50% unutilized and that we could, with some modest maybe CapEx investments, be able to get another 50% of that.
So we still want to continue to see that government work continue to be performed, and we'll see some growth in that, probably at a low single digit. But where we're able to do the commercial work is going to be in tapping into that unutilized capacity that currently exists at the site.

**Operator** (Operator):
Your next question comes from the line of Bob Labick with CJS Securities.

**Bob Labick** (Analysts):
Great. Congratulations on another strong execution and continued great outlook. I wanted to dig into your capital allocation comments between today a little bit and then some from the Analyst Day or Investor Day as well. I think to maintain the 2 to 3x leverage by 2030, you'll be spending, I think, somewhere between $3 billion and $4 billion going forward. And you just reiterated, you want to spend this on attractive organic opportunities as kind of first thing you want to spend it on.
So could you maybe tell us the top priorities, maybe 3, 4, 5 opportunities out there? And then how much of that $3 billion plus spending is necessary to reach your revenue and EBITDA numbers? Or how much is upside? How should we think about that capital allocation?

**Michael Fitzgerald** (Executives):
So one of the things that we laid out is that we had -- if you looked at kind of the slide from our Investor Day, it actually showed that amount of kind of additional capital. So the way I would think about it is the 2030 targets are really anchored to the 5% to 6% core CapEx spending that we've discussed from a target standpoint.
We also stated that we didn't need any specific M&A per se to be able to hit those 2030 targets. So I would think of that as additional deployment opportunities above and beyond the core business and what we laid out there from a 2030 target standpoint.
With that said, I think we're seeing opportunities out there. However, we've made it very clear that when there's not organic opportunities or when there's not additional M&A targets that we would return that capital to shareholders as appropriate. So I still think there's a real possibility for that.
If you look in our 2027 guidance, we'll do some modest share repurchases, consistent with our prior practice of offsetting dilution. But we are focused on kind of the -- those capital allocation priorities as stated. When you look at from a priority standpoint, we want to continue to build off the momentum that we've been seeing. So we've talked about capacity investments that we've made across the business. We certainly have talked about Special Materials, and that's been a great part of our growth story. 
And then I think you'll hear more around we're seeing a lot of some traction happening with our microreactor business with the program Janus win and BANR being selected in Canada as well. And so excited to see that market. And hopefully, there's some additional opportunities there.

**Operator** (Operator):
Your next question is from the line of Tomo Sano with JPMorgan.

**Tomohiko Sano** (Analysts):
Maybe just on Commercial Operations. Your full year guidance calls for roughly 45% growth in this business. Given where you are through Q3, that implies a pretty big step-up in Q4. Is there something specific a large order or revenue recognition event driving that acceleration, please?

**Michael Fitzgerald** (Executives):
Nothing unusual to call out. We've always experienced some ramp in the fourth quarter as we look at just kind of the timing of that overall from an execution standpoint. You are -- we are also seeing there will be contribution from PCG as well. So if you look at that on over a year-over-year basis, you're going to see some additional growth there. But I don't think anything unusual from a fourth quarter perspective.

**Tomohiko Sano** (Analysts):
And just a follow-up on PCG acquisition. It's been a few months since you closed the acquisition. How is integration tracking? Are you seeing the synergies and cost benefits you expected on schedule?

**Michael Fitzgerald** (Executives):
Yes, absolutely. Actually, the integration is going very, very well. We did not -- if you remember, the thesis around this transaction was not necessarily revenue synergies. We did see some opportunities on the cost side, but we didn't put out any specific targets related to that. However, I would say we're finding a lot of opportunities and the team has been getting very involved in how we can really address this from a U.S. commercial market standpoint. So I'm very pleased with the progress that we've made, and they've been a great addition to the overall company.

**Operator** (Operator):
Your next question comes from the line of Jeffrey Campbell with Seaport Research.

**Jeffrey Campbell** (Analysts):
Your recent press release concerning rumors of Poland investment was explicit in saying that such a decision would require firm orders of sufficient size to transact. Should we assume the same structure applies to beginning construction of a new U.S. commercial heavy component facility?

**Rex Geveden** (Executives):
No, Jeff. I don't know, that U.S. facility does not depend on firm orders. That said, there's so many things in the pipeline that we're certainly compelled to go ahead with that U.S. plant. The Poland situation had to do with some discussions around how much demand we think will precipitate for microreactors and small modular reactors in Poland. And there were certainly gigawatt scales of demand that we discussed. But no, we're going ahead with the U.S. plant regardless.

**Jeffrey Campbell** (Analysts):
Okay. Great. One of the things that impressed me in the Investor Day was the potential remuneration from your exposure to CANDU. Recently, I read that AtkinsRealis, the state of Indiana and Hoosier Energy had partnered to evaluate up to 6 gigawatts of CANDU reactors for that state. So high level, what do you think about CANDU potentially finally making inroads into the U.S.? And is it reasonable to assume BWXT could potentially be a component supplier to this project if it ever materializes?

**Rex Geveden** (Executives):
Yes. Maybe to put some things in context, Jeff, if you look back at the history of CANDU and there were about 30 CANDU units delivered globally, 20 in Canada itself. And so 10 or so that went to other places, South Korea, China, India, Romania and Argentina. So -- and that's with -- that's 30 large plants compared to a total global installed base of about 600. So let's say it captured 5% of the international market over the course of those years. And maybe that's a reasonable assumption going forward.
I certainly would hope and certainly, the Canadians hope that they can build some -- can build an international market from CANDU and have a real export capability. And I think that's feasible. And I certainly do hope that they can export into the U.S. And if they do, we will certainly be in that supply chain, probably supplying fuel, major components, feeders, all the things that we normally do, we would do for that. And that's the purpose of Canada's investment in the CANDU industrial supply base is to be able to create an industry there that's durable and has export qualities to it.

**Operator** (Operator):
Your next question comes from the line of Marc Bianchi with TD Cowen.

**Marc Bianchi** (Analysts):
I want to ask first on the '27 outlook. It looks like you upgraded the EBITDA growth expectation a little bit from the Investor Day. Could you talk a little bit about that?

**Michael Fitzgerald** (Executives):
Yes. I think, look, we're seeing some -- we've had really strong performance in the underlying margin for this year. We're seeing some continued momentum as we go into 2027. So I would think of it as kind of a refinement of our expectations, nothing material, but we feel confident in ultimately getting to high single to low double digit, both on adjusted EBITDA as well as EPS.

**Marc Bianchi** (Analysts):
Okay. Is that more coming from government side of the business, just given the beat in 3Q here?

**Michael Fitzgerald** (Executives):
I think we look at this from different scenarios. So we'll run multiple scenarios. I think it's fair to assume that our government business will continue to perform very well. As mentioned, we're kind of coming off of that -- some of those older pricing arrangements. And so we're starting to see that come into the financials as we execute successfully on those programs. But I would say we're also seeing continued momentum in commercial. So it's positive across the board.

**Marc Bianchi** (Analysts):
Okay. And then if I could just ask one more. On the potential orders for commercial, there's -- I think everybody sort of read the news around we've got this DOE long lead up program for large reactors and then there's a Department of Commerce track for 8 reactors, and there was an announcement, I guess, it's several weeks ago about the Korean program there. Like which one of those feels like we could get a quicker hit? And maybe do you think that BWXT is equally positioned for both of those programs or maybe more weighted to one than the other? Just curious for any color you can provide.

**Rex Geveden** (Executives):
Yes, Marc, I'll add some color there. I think in my opinion is that the SMR opportunity is a bit ahead of large reactor opportunity. That's just my feel for it. We're certainly in active discussions with Westinghouse and GE on all of that. So I think you'd see -- we'd see more activity in our order book. I think first from the Darlington project, units 2, 3 and 4 up there.
I think closely following that would be the TVA opportunities, the 10 reactors there, 5 at Clinch River and then 5 at Bellefonte, I think. And then with the APs to follow that would be my guess. Now all those discussions are active, and I think all of that represents opportunity for us, but that's how I see the sequencing. And I said at the beginning of this year that I expected us to have new orders for U.S. reactor plant builds in -- by the end of this year. And I still think that's a possibility for us, but certainly no later than about the first half of the next year.

**Operator** (Operator):
Your next question comes from the line of Scott Deuschle with Deutsche Bank.

**Scott Deuschle** (Analysts):
Mike, can you walk through what's been driving the relatively slow organic growth at Government Operations year-to-date? And maybe just kind of what the headwinds have been? And has the revenue cadence surprised you at all? Or is it consistent with how you thought the year would play out?

**Michael Fitzgerald** (Executives):
No, I would say it's consistent. One of the things as we came into 2026 we were going to see a larger ramp on the -- on the newer programs, but specifically on the HPDU program as we get on to the third and the fourth quarter. And so we're continuing to see that. We did discuss, I think, a little bit last quarter how we were performing actually really well on that program. And because of that, it was lower revenue just because we had really strong margin performance, which under a percent complete model actually results in lower revenue. So no surprises. I think those programs are performing well, and we'll continue to see them into '27 as well.

**Scott Deuschle** (Analysts):
Okay. And then, Rex, if the first U.S. AP1000 builds ultimately get funded by South Korea as opposed to another funding source, is that a negative as it relates to your content opportunity on those initial builds? Or is the funding source not expected to influence supplier content allocations?

**Rex Geveden** (Executives):
I think it's hard for me to say on that one, Scott. I would say that it's our expectation that we will have to go and compete with Doosan and IHI and all the usual suspects when those opportunities come up. That said, I think there's going to be plenty of opportunity for all the players there because there's actually still not that much capacity globally for these kind of components. So we'll compete and hopefully get our share and make a great business out of it.

**Scott Deuschle** (Analysts):
Is Westinghouse typically the one deciding who gets the content or someone else?

**Rex Geveden** (Executives):
No. I mean it's my expectation that Westinghouse will be making those decisions.

**Operator** (Operator):
Your next question comes from the line of Jeff Grampp with Northland Capital Markets.

**Jeffrey Grampp** (Analysts):
Rex, sticking on the new build topic. From your guys' perspective, what are kind of the main gating item or items keeping new build projects from reaching an FID? Is it predominantly finance and kind of structuring things related to that? Or are there other particular items that you guys see that kind of holding things up from getting a couple of projects across the finish line here?

**Rex Geveden** (Executives):
Yes, I'm not in those discussions, but what I'm hearing about is it has to do with the allocation of risk. How much are the hyperscalers going to take, how much of the utility is going to take, if that applies, how much is the government going to take? Are there any backstops and how much will the technology provider itself take? And so I think it's about -- we've been hearing this concept that everyone bleeds, but no one bleeds to death as it relates to any overruns or risks in the project.
So I think it's about the distribution of risk. I don't think it's so much about financing because in the case of the 10 X-300s and certainly those 10 AP1000s and then that second tranche, those are going to be funded through the sovereign investments from South Korea and Japan, as I understand it. So I think it's less about financing. It's more about allocation of risk.

**Jeffrey Grampp** (Analysts):
Got it. I appreciate those details. And for my follow-up, can you touch on BWXT's capabilities to handle multiple awards of projects for larger nuclear new builds if this accelerates into the coming years, how does your ability to scale compare to the business opportunities you guys are seeing? And maybe where does that rank in terms of, I guess, the list of worries on a given day for you guys in terms of just capacity to meet the demand that's out there?

**Rex Geveden** (Executives):
Yes. Well, good problem to have. I would say we've been trying to anticipate all that. We, of course, just increased our production capacity by about 50% at Cambridge, Ontario. We literally just completed that expansion under budget, slightly under budget and about on the original schedule. So we're prepared there.
Of course, the PCG acquisition was around that thesis. That, as Mike said in an earlier question, we think that, that asset is about 50% underutilized, and we can build some capacity there for medium reactor components. And then the U.S. plant that we've been talking about for the past couple of quarters is intended to deal with that demand. So I mean, we're stacking them up we're stacking up our capacity. We're certainly one of the largest players in the world, and I think we'll be prepared for it.

**Operator** (Operator):
Your next question is from the line of Mark Shooter with William Blair.

**Mark Shooter** (Analysts):
Congrats on the quarter. And Rex, I heard you mention that you'll have a prototype test of the DUECE centrifuge by end of the year. I was wondering if you can give us some color on the metrics you'll be judging it by. And speaking of the NNSA program, I know we also talked about the potential of widening that scope to include unobligated LEU and HALEU enrichment. So I was wondering if you could tell us how you're thinking about that now.

**Rex Geveden** (Executives):
Yes. Sure thing, Mark. What we're doing, of course, in that program is taking technology developed at Oak Ridge National Laboratory and taking it into industrializing that technology and building production capacity and ultimately, a demonstration cascade at our plant in Oak Ridge. And so I certainly can't cite the particular success criteria for that demonstration. It is just a demo.
And what we're doing, of course, is trying to reduce the complexity, exercise the supply chain and be able to build an unobligated system. So I think sort of just spinning that thing will be the proof that we're looking for, and we'll be building certainly many more units in the future. As it relates to the opportunity in between the technology transfer and the high enriched uranium scope that we have at our Erwin, Tennessee plant, we are certainly pursuing adding low-enriched uranium and high-assay, low-enriched uranium to the scope. Those discussions are ongoing. I can't offer any details on that, but it's certainly in our sights, and we hope to add it.

**Mark Shooter** (Analysts):
That's great. Switching gears on to the other fuel, TRISO. Congrats on the Antares win. And so you'll be supporting Antares, Project Pele, Project Janus and also from the Lynchburg facility. So can you remind us what capacity increases are needed today to meet those commitments? And what level of fuel contracting do you need to see to require an expansion past Lynchburg?

**Rex Geveden** (Executives):
Yes, I'll offer some details there, Mark. We were able to produce a couple of hundred kilograms a year on that Lynchburg line, and that's enough capacity for fully fueling the core of the Pele reactor and some other things that we did, the Antares demo and a couple of other customers that we actually haven't -- that we haven't disclosed. Through some technology changes and some capacity we can add and from some operational improvements, we can at least quadruple the output of that facility. That's our Lynchburg plant that I'm talking about, not the greenfield.
So that gives us quite some capacity for the near term. I think in terms of making the larger investment decision and getting to multiple megatons of -- sorry, multiple metric tons of capacity, say, at a Wyoming plant, we're going to need to see 2 things. We need to see larger demand precipitate first with our partner, Kairos, for the Hermes reactor. That one as an anchor tenant will consume a lot of TRISO and then others, right, multiple BANR orders, for example. So we need the precipitation of concrete, significant demand in the future. And we also need to see HALEU become available commercially. And those are 2 important gates, and we'll get those -- we'll get to that decision as that becomes clearer.

**Operator** (Operator):
Your next question comes from the line of Laurence Alexander with Jefferies.

**Laurence Alexander** (Analysts):
Just a simple one on Commercial Operations. The margin improvement expected for '27, how important is that? I mean, given the range of the growth opportunities you're evaluating and the incremental investments to support that, do you need that kind of -- is that sort of a flexible part of your bridge for next year?

**Michael Fitzgerald** (Executives):
Yes. Sorry, I'm not sure I follow. So from a -- we are seeing some margin improvement as we look into 2027. That's -- there's a large mix. If you kind of remember what commercial, we have kind of a services business component that we have ultimately the components margin. So that's just on the components manufacturing. And then we also will have the kind of the contribution of PCG that would continue. So different margin mix profiles.
I think we're seeing some substantial growth in the underlying revenue base for the components business. That will -- that is offsetting some of the headwinds that were associated with the divestiture of Medical, which was a higher growth -- higher kind of margin business as well. So I think when you blend all that together, I mean, we're not seeing anything unusual. The margin continues to perform well, and we're seeing a slight uptick primarily as a result of just kind of overall mix and growth in different aspects of the business.

**Operator** (Operator):
Your next question comes from the line of Andre Madrid with BTIG.

**Andre Madrid** (Analysts):
You had mentioned it before that maybe the gating factor in seeing more commercial orders convert was kind of the allocation of risk. Do you expect tomorrow's midterm elections to potentially, I guess, complicate those conversations any further? Or is that not really a concern?

**Rex Geveden** (Executives):
I don't think it's a big concern, Andre, because those deals are constructed outside the framework of congressional appropriations and authorization and they don't come through the President's budget request. So in some ways, it's outside that whole system. It obviously relates to the tariff deals that were done and the sovereign investments that were made to offset the threat of tariffs. So I think those deals go forward regardless.
And all that said, and I've said this often, I've been in the seat for 10 years and through multiple administrations and support for nuclear has only gotten stronger and stronger. It's bicameral, it's bipartisan. It makes sense for so many different reasons. And so just about everyone lines up behind nuclear now. So I don't expect a lot of impedance here.

**Andre Madrid** (Analysts):
Got it, Rex. That's helpful. And staying on that point of commercial order flow, I mean, you said that you were expecting something to start -- some of these to start picking up in the latter part of this year, but definitely no later than the first half of next year. I mean, given the back-end weighted nature of your 2030 targets, I mean, at what point does the pace of commercial order flow start to become a concern? If we don't see, I guess, a specific number of awards come in, in the first half of next year, does that kind of put risk on the long-term guidance that you guys outlined?

**Rex Geveden** (Executives):
I don't think so, Andre. I think we've got multiple ways of achieving that guidance, as we said, and we've mapped in some modest success in commercial orders for new builds. And yes, we've got multiple ways to win, and we intend to do so.

**Operator** (Operator):
Your next question comes from the line of Pete Skibitski with Alembic Global.

**Peter Skibitski** (Analysts):
Rex, I'd love to get a sense for the revenue opportunity with this New Brunswick Prodigy win, I guess, we can call it. It looks like my simplistic math, it looks like it could be maybe 2 or 3 BANR reactors. But can you give us a sense maybe for what a contract will be signed and maybe if there's a way you could size it or put a framework around it?

**Rex Geveden** (Executives):
Yes. Maybe I'll be a little bit coy here, Pete, because if you look at the way -- so just backing up a little bit, if you look at the way that Janus program is structured by the Army and DIU, what they're intending to do is create a commercial opportunity for microreactors, even though in that case, you're selling into the government market. And this one in Canada, of course, is a purely commercial endeavor. And we've got multiple other commercial opportunities around BANR.
So we're not being -- we're certainly not intending to disclose any pricing details because of competitive sensitivities. But yes, I mean, if you think about selling 3 microreactors and it is a significant revenue opportunity for us and has the potential to be an exciting business for us. But it's super early days on that one, right? We've been selected for technology. The financing has got a line up behind it. New Brunswick has committed to an MOU for a power purchase agreement. So there's some government strength behind it, but there's a long road ahead on this one. And I'd like to offer you more details, but I just can't right now.

**Peter Skibitski** (Analysts):
Understood. So time lines, so you do Fort Campbell first and then would Tata be the first kind of commercial deployment and maybe then New Brunswick?

**Rex Geveden** (Executives):
I mean, certainly, Fort Campbell's first in line. But yes, opportunities in Wyoming, opportunities in Poland, Canada, those are all kind of to me sort of running in parallel for second place.

**Peter Skibitski** (Analysts):
Okay. Okay. Got it. If I can ask one last one just because it just popped up. Obviously, Army and Janus is together, but now the Navy is talking about microreactors. I was wondering if you guys are going to do the reactor for the Navy at NSWC Crane in Indiana.

**Rex Geveden** (Executives):
No. That's a smaller microreactor and being done by one of our competitors. And by the way, Pete, if I could just add a footnote to this whole discussion. A lot of these microreactors are out there in the sort of megawatt range, let's call it. There is one 5-megawatt reactor. And what we have, of course, with our product, the BANR reactor on the Janus program and elsewhere is a 20-megawatt electrical output, 22-megawatt actually, 75 megawatts thermal.
So -- and it's a very high temperature reactor. So it's suitable for some large-scale applications, even though it's a microreactor. You can run large military bases with that. You could provide industrial heat at a large chemical plant, for example. And so we have -- we're seeing a range of opportunities that are completely unavailable to our competitors in that space because of the scale of that reactor.
That said, it still fits on a train. This is a rail shippable actually modular reactor. When we talk about small modular reactors, those are not small. And frankly, they're not modular. They're built in the field. These things are actually literally built in the factory just as our naval reactors are. And so we've got the largest scale microreactor that's capable of addressing some very big problems, and that's one of the reasons why we're bullish on it.

**Operator** (Operator):
Your next question comes from the line of David Strauss with Wells Fargo.

**Joshua Korn** (Analysts):
It's Josh Korn on for David. I wanted to ask about the free cash flow guidance. I guess, what's weighing on cash in the fourth quarter? And then you seem to be implying a pretty big working capital headwind into next year. Just kind of anything you could provide there?

**Michael Fitzgerald** (Executives):
Yes. I think -- so fourth quarter is just the timing. We had a really strong third quarter. So you're seeing some of that just on overall timing coming into the third quarter. But we feel good about where we're guiding for the year. And I think we have a great opportunity to execute on that.
When you look at 2027, there's a couple of things that are going on. One, we got about a $10 million headwind to pension contributions. This is normal course, primarily associated with the Kinectrics acquisition. We have a little bit of working capital investment for some of the growth opportunities, and there is some timing of just overall milestones, specifically on the HPDU and kind of our newer enrichment programs. But I think at the end of the day, we're seeing -- if you look at kind of the underlying true performance from an OCF perspective, we're still seeing good conversion on our core businesses. So a little bit of headwind as we invest for growth and some other kind of unique items, but we still ultimately feel good about where we're going to land for the year.

**Operator** (Operator):
Your next question comes from the line of Peter Arment with Baird.

**Peter Arment** (Analysts):
A lot of questions asked. But Rex, maybe just a quick one on the budgets. If we don't have any budgets resolved post midterms here and things linger into next year, does that have any impact on your thoughts on '27? Or is that not really an issue regarding for you guys?

**Rex Geveden** (Executives):
Peter, historically, we've been able to work through those continuing resolutions in pretty good shape because almost everything in our portfolio is program of record and those get funded at 95% of the prior year or whatever. And we typically have some uncosted carryover that's able to sustain us. We sort of got to the end of our rope on some TSG programs last year when that one ran extra long. But broadly speaking, we've been a little bit immune to CRs. And so I don't think it certainly doesn't influence how we think about the forecast right now.

**Operator** (Operator):
And our final question comes from the line of Michael Ciarmoli with Guggenheim Securities.

**Michael Ciarmoli** (Analysts):
Rex, we get this question a lot from investors on the AP1000, the Westinghouse. And you guys have, I guess, sized it already as a couple of hundred million dollars of content. But just given the comments you made, I mean, how much blood are you willing to lose on that content if risk is going to be spread around? And I guess I think about it from a margin standpoint, are there any terms or any potential content or undertaking that would be too risky for you guys?

**Rex Geveden** (Executives):
I think -- so Mike, component manufacturing is something that we understand very, very well, right? And the opportunities we'll go after would be things like RPVs and steam generators and those kind of components that we understand how to make. I think that's a very, very different category of risk than delivery risk. Project delivery risk is what it's all about.
And I've been saying of late that, that we need more innovation on the delivery side because these final investment decisions ultimately in the commercial sense are driven by the capital cost and the cost of capital. So we, the industry, have to deliver these reactors more quickly and more reliably. So it's not -- yes, I don't see that component manufacturing bears the same kind of risk as delivery. Now we'll certainly have -- we'll certainly experience price pressure. We always do that. But we know how to make steam generators, heat exchangers, control rod drive mechanisms, reactor pressure vessels, just bring it on, right? We can accept that risk, and we do every day.

**Michael Ciarmoli** (Analysts):
Got it. And presumably, that's all contemplated in your 2030 forecast in terms of a margin profile?

**Rex Geveden** (Executives):
Absolutely.

**Operator** (Operator):
And with no further questions in queue, I will now hand the call back to Chase Jacobson for closing remarks.

**Chase Jacobson** (Executives):
Thank you to everyone for joining us today. We look forward to seeing and speaking with many of you at upcoming investor events. You can all feel free to reach out to us at investors@bwxt.com, and we look forward to talking to you and seeing you soon. Thanks for the support.

**Operator** (Operator):
Thank you again for joining us today. This does conclude today's conference call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### BWXT_Q2_2026_Earnings_Call_20260803.md
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：全年自由現金流財測上調 $30M，區間 $345M–$360M（原話："to a range of $345 million to $360 million"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：全年調整後 EBITDA 財測中點上調 $10M，區間 $662M–$672M（原話："adjusted EBITDA guidance by $10 million at the midpoint"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：全年營收財測約 $3.8B，高十位數成長（原話："We now expect revenue of approximately $3.8 billion"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：政府業務營收成長財測由低十位數下修為高個位數（原話："our previous expectation of low teens growth."）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：管理層說明政府業務營收下修原因：成本表現較佳，依會計規則使認列營收較低，但經濟結果有利（原話："lower reported revenue, but an overall favorable"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：政府業務調整後 EBITDA 利潤率財測上調至約 20.5%（原為 >19%）（原話："adjusted EBITDA margin guidance to approximately 20.5% from"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：商業業務營收成長財測上調至約 45%（原約 30%）（原話："revenue growth outlook to approximately 45% from"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：商業業務 EBITDA 利潤率財測約 13%（原約 14%）（原話："adjusted EBITDA margin of approximately 13%"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：商業業務利潤率下修原因為美國產能擴張（含 PCG）與加拿大持續投資（原話："The revision reflects incremental investments in U.S."）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：2026 非 GAAP EPS 財測 $4.70–$4.80，上調全由營運獲利推動（原話："of $4.70 to $4.80. The increase from our prior guidance is"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：下半年獲利約 55% 落在第四季（原話："we expect approximately 55% of second half earnings to be"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：管理層建模口徑：出售的醫療業務 2026 年化營收約 $130M，利潤率略高於商業部門平均（原話："modestly accretive to the Commercial segment average"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：出售後保留的少數股權將以權益法收益認列、無相關營收（原話："retained minority interest through equity income"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：Q2 調整後 EBITDA 數字口徑：逐字稿本身標註 $156M 為誤，應為 $155M（原話："$156 million (sic) [ $155 million ]"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：Q2 政府業務調整後 EBITDA 利潤率 20.9%（原話："resulting in an adjusted EBITDA margin of 20.9%"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：Q2 商業業務利潤率 11.9%，量增與執行抵銷擴產投資（原話："quarter was 11.9% as higher volume and strong execution"）
- 2026-08-03｜CEO Rex Geveden｜margin：CEO 表示投資將使近期利潤率擴張趨緩（原話："will moderate near-term margin expansion"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：政府業務仍在消化舊定價安排的在手訂單（原話："working off backlog associated with older pricing"）
- 2026-08-03｜CFO Michael Fitzgerald｜commitment：CFO 預期舊定價在手訂單於 2026 年底前消化完畢（原話："that to be done by the end of '26."）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：CFO 表示目前不設定 2027 年財測（原話："I'm not setting '27 guidance at this point."）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：CFO 預期 2027 年商業業務利潤率將有較明顯提升（原話："as we go into '27, we'll see more of a"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：全年資本支出約占營收 6%，下半年美國商業產能投資增加（原話："of approximately 6% of sales with increased investment"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：未來幾年資本支出可能接近營收 7%（原話："capital expenditures could approach 7% of sales in future"）
- 2026-08-03｜CEO Rex Geveden｜commitment：CEO 稱至少有一張新建核電設備訂單有機會在年底前取得（原話："opportunity to secure at least one new build nuclear"）
- 2026-08-03｜CEO Rex Geveden｜commitment：CEO 稱預期未來數月內對美國商業製造擴產做出最終投資決定（原話："we expect to reach a final investment decision in the coming"）
- 2026-08-03｜CEO Rex Geveden｜commitment：CEO 稱擴產目前只剩選址（紐澤西、印第安納與另一處）待定，且很快決定（原話："just a matter of site selection at this point"）
- 2026-08-03｜CEO Rex Geveden｜commitment：CEO 預告 9 月投資人日（原話："our upcoming Investor Day in September"）
- 2026-08-03｜CEO Rex Geveden｜capital_allocation：宣布以最高 $800M 估值出售醫療業務給 Nordic Capital（敘事變化：聚焦核心）（原話："sale of our medical business to Nordic Capital"）
- 2026-08-03｜CEO Rex Geveden｜capital_allocation：CEO 稱該資產原本並未待售，是買方主動接洽（原話："that asset wasn't for sale"）
- 2026-08-03｜CFO Michael Fitzgerald｜capital_allocation：交易對價 $750M，另有共享經濟機制可達 $800M（原話："the deal includes $750 million of consideration"）
- 2026-08-03｜CEO Rex Geveden｜capital_allocation：BWXT 保留醫療資產 20% 股權（原話："we will maintain a 20% equity stake in"）
- 2026-08-03｜CFO Michael Fitzgerald｜capital_allocation：出售所得用途尚未確定；優先順序為內部投資（資本支出 6–7%）、併購、還債（原話："So not exactly."）
- 2026-08-03｜CFO Michael Fitzgerald｜capital_allocation：CFO 稱併購管線很充足，但篩選嚴格（原話："we have a very robust M&A pipeline"）
- 2026-08-03｜CFO Michael Fitzgerald｜capital_allocation：2026 年無計畫中的庫藏股買回（原話："we don't have any planned repurchases"）
- 2026-08-03｜CEO Rex Geveden｜capital_allocation：TRISO 商業設施資本支出規模為數億美元至最高 $500M，與夥伴分攤並有懷俄明州補助（原話："a few hundred million dollars, up to $500 million."）
- 2026-08-03｜CFO Michael Fitzgerald｜capital_allocation：CFO 稱 Janus 決標是 TRISO 投資決定的關鍵里程碑，預期今年授標（原話："expecting an award this year"）
- 2026-08-03｜CEO Rex Geveden｜risk：CEO 稱 TRISO 需求仍高度不確定，尚未準備好全面資本承諾（原話："we're not yet ready to make a full capital commitment on it"）
- 2026-08-03｜CEO Rex Geveden｜risk：CEO 解釋 AP1000 尚無確定訂單：公用事業在觀望政府主權交易結果（原話："the utilities are sort of rightly waiting to see how"）
- 2026-08-03｜CEO Rex Geveden｜risk：濃縮業務自製供應鏈須使用美國來源（無義務）設備，CEO 稱存在商業可行性疑問（原話："there's a question about the commercial viability of"）
- 2026-08-03｜CEO Rex Geveden｜risk：供應鏈目前無問題，原料（鋯管、大型鍛件）取得順利（原話："zirconium tubes, large forgings, whatever we need"）
- 2026-08-03｜CEO Rex Geveden｜risk：勞動力整體可控，加拿大鋼鐵工人略缺（原話："challenges finding steel workers in Canada right now"）
- 2026-08-03｜CEO Rex Geveden｜customer：期末在手訂單 $8.4B（原話："We ended the quarter with backlog of $8.4 billion"）
- 2026-08-03｜CEO Rex Geveden｜customer：在手訂單較上季略減，管理層歸因於大型多年期合約的授標時點（原話："Although backlog was modestly lower than last quarter"）
- 2026-08-03｜CEO Rex Geveden｜customer：近 12 個月 book-to-bill 為 1.7x（原話："our book-to-bill is a robust 1.7x"）
- 2026-08-03｜CEO Rex Geveden｜customer：海軍新造艦計畫將福特級航艦採購節奏加快為 4 年（原話："Ford-class aircraft carriers to a 4-year procurement"）
- 2026-08-03｜CEO Rex Geveden｜customer：CEO 稱福特級 4 年節奏對業務的量體影響比核動力戰艦更大（原話："actually more important to our business."）
- 2026-08-03｜CEO Rex Geveden｜customer：核動力戰艦長交期採購預期 2028 年開始進入 BWXT 工廠（原話："long lead procurements would begin in '28 as we"）
- 2026-08-03｜CEO Rex Geveden｜customer：加拿大核能策略：聯邦支持至 2040 年最多 10 座大型反應爐（原話："federal support for up to 10 large reactors by 2040"）
- 2026-08-03｜CEO Rex Geveden｜customer：加拿大大型反應爐對 BWXT 營收的影響預期落在 2030 年代初（原話："very positive way in the early 2030s."）
- 2026-08-03｜CEO Rex Geveden｜customer：DOE 宣布 $17.5B 貸款承諾，支持 AP1000 長交期設備採購（原話："$17.5 billion loan commitment"）
- 2026-08-03｜CEO Rex Geveden｜customer：CEO 預期下半年會拿到一張訂單，來源涵蓋 SMR、AP1000、X300 等（原話："second half order among the opportunities"）
- 2026-08-03｜CEO Rex Geveden｜product：濃縮專案：離心機原型機預計今年交付，進度符合時程（原話："on schedule to deliver an operational prototype centrifuge"）
- 2026-08-03｜CEO Rex Geveden｜product：高純度貧鈾（HPDU）新廠預期下半年對政府業務營收有顯著貢獻（原話："This program should contribute meaningfully to"）
- 2026-08-03｜CEO Rex Geveden｜product：mPower 授權：BWXT 保留製造權、權利金權與智慧財產（原話："exclusive manufacturing rights, royalty rights"）
- 2026-08-03｜CEO Rex Geveden｜product：CEO 稱無意自行將 mPower 推向市場，仍維持 merchant supplier 定位（原話："it's not our intention to bring"）
- 2026-08-03｜CEO Rex Geveden｜product：CEO 稱 mPower 授權等於將自家 IP 變現（原話："monetizing our IP"）
- 2026-08-03｜CEO Rex Geveden｜product：PCG 整合與產能納入需時，預期未來數季逐步展開（原話："will unfold over the next few quarters"）
- 2026-08-03｜CEO Rex Geveden｜competition：CEO 自述在供應鏈廠商中居於頂端，擁有北美最大元件製造廠（原話："we sit right at the top"）
- 2026-08-03｜CEO Rex Geveden｜competition：CEO 稱產能與能力上全球無人更佳（原話："I don't think there's any one better on the globe."）
- 2026-08-03｜CEO Rex Geveden｜competition：CEO 說明 PCG 無法生產最大型元件（如 AP1000 反應爐壓力容器）（原話："PCG is not capable of producing the largest components"）
- 2026-08-03｜CEO Rex Geveden｜competition：CEO 稱海軍核反應爐業務讓 BWXT 擁有競爭對手沒有的天然優勢（原話："natural advantages that our competitors did not"）

### BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2030 年營收目標 55~60 億美元（較 2026 年低雙位數年增）（原話："we're targeting $5.5 billion to $6 billion in 2030"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2030 年調整後 EBITDA 目標 11~12 億美元（原話："we're targeting $1.1 billion to $1.2 billion"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2030 年自由現金流目標 5.25~5.75 億美元（原話："targeting free cash flow of $525 million to $575 million"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：調整後 EBITDA 利潤率由 2026 年 17.5% 走向 2030 年約 20%（原話："approximately 20% by 2030"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜margin：CFO 說明 20% 目標不假設產品組合變好，靠執行、生產力、價值捕捉與規模（原話："20% doesn't assume that mix is going to be more favorable"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜margin：CFO 拆解利潤率改善空間約 300 個基點（營運卓越、定價、規模）（原話："This represents about 300 basis points of opportunity"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜margin：CFO 說明政府部門近年利潤率小幅受壓，原因為產品組合（原話："primarily been driven by mix"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 年初步框架：營收高個位數成長（原話："calls for high single-digit revenue growth"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 年政府部門特殊材料預期強勁雙位數成長（原話："robust double-digit special materials growth"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 年政府部門利潤率預期持平至小幅上升（原話："We expect government margins to be flat to modestly higher"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 年商業部門有機成長高個位數（原話："we expect high single-digit organic growth in 2027"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 年商業部門報告營收成長低個位數（PCG 併入、醫療出售互抵）（原話："expected to be low single digits"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 年商業部門利潤率預期擴張 50~100 基點（原話："commercial margins to expand 50 to 100 basis points"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：重申 2026 年財測（原話："we are reaffirming our 2026 guidance"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2026 年自由現金流指引 3.45~3.6 億美元（原話："$345 million to $360 million based on our current guidance"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 框架假設醫療事業 2026 年底完成出售（原話："we're assuming that Medical closes at the end of 2026"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜guidance：商業部門 2030 年前營收年複合成長高十位數百分比（原話："high teens revenue CAGR over the period to 2030"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜margin：商業部門 EBITDA 利潤率由約 13% 到 2030 年高十位數（原話："go from about 13% now into the high teens by 2030"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜guidance：政府部門 2030 年營收中至高個位數年複合成長（相較現在）（原話："mid- to high single-digit CAGR as compared to today"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜margin：政府部門 2026 年利潤率由年初 19% 升至約 20.5%（原話："raise that margin above 20% to about 20.5%"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜guidance：海軍核動力 4%~6% 年複合成長（原話："So all in all, 4% to 6% CAGR growth over this time period."）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜guidance：戰艦核心未列入預測，因海軍尚未承諾採購（原話："This isn't in our forecast"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜risk：CFO：戰艦未納入 2030 預測，仍須撥款與其他關卡（原話："has to go through appropriations and a number of hurdles"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：福特級航母採購節奏已加快並納入預測，影響約在 2030 前後（原話："that did accelerate, and we have incorporated that"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜margin：海軍核反應爐不按艘報價，因固定成本大、依總艘數定價（原話："we don't sell specific price per reactor"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：$45 億積壓訂單預計轉為營收（2027 年底前）（原話："$4.5 billion of our backlog is expected to convert"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：接單出貨比近 12 個月（至第二季）1.7 倍（原話："we're 1.7x on a trailing 12-month basis"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：營收成長中約一半多來自既有核心（原話："That represents a little over half of the growth forecast"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜commitment：CFO：成長路徑非直線，單一年度節奏可能不同（原話："I would not expect this to happen in a growth"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜commitment：CFO：不需贏下所有機會就能達標（原話："we don't need to win every opportunity discussed"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：CFO：新商業核電建設拐點在 2028、2029（原話："you're going to see that inflection in '28 and '29"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜guidance：商業大型機組訂單轉換時點：今年稍晚或 2027 年初（原話："either later this year or early in 2027"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜customer：每座 CANDU 反應爐可觸及營收 3.5~7 億美元（原話："between $350 million and $700 million per reactor of revenue"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜customer：每座 SMR 可觸及營收約 5000 萬至 1 億美元（原話："about $50 million to $100 million per reactor"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜customer：加拿大國家核能策略：10 座大型機組目標（原話："deploy 10 large reactors, 2 under construction by 2035"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜customer：預期加拿大新大型機組帶來零組件訂單於本十年結束前（原話："orders for components before the end of this decade"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜customer：Westinghouse 正在對 BWXT 做零組件資格認證（原話："working through qualifying us for all of the components"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜customer：Bruce C 與 Wesleyville 預計新機組數量（原話："probably 8 reactors at that site"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜product：蒸汽產生器產能由每月 1 台提升至 1.5 台以上（原話："operating at a pace of over 1.5 steam generators a month"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜product：服務營收由 2020 年約 7000 萬增至今年逾 6 億美元（原話："to more than $600 million this year"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜competition：BWXT 自稱技術中立的 merchant supplier（原話："we're technology agnostic"）
- 2026-09-29｜Rex Geveden (CEO)｜competition：CEO 稱 TRISO 競爭對手雜音多但出貨量小（原話："noisy competitors that are delivering very modest amounts"）
- 2026-09-29｜Rex Geveden (CEO)｜competition：CEO 指出無鈾濃縮的商業端有天然競爭劣勢（Urenco 等）（原話："a natural competitive disadvantage to that capability"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜product：特殊材料成長 24% 年複合，持續到 2030（原話："large growth, 24% CAGR"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜product：田納西州 Jonesborough 的 HPDU 設施規劃產能上限 300 公噸（原話："manufacture up to 300 metric tons of high-purity depleted"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜customer：去年 9 月取得 15 億美元濃縮鈾合約（原話："awarded the contract in September of last year for $1.5"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜capital_allocation：國防燃料設施初期投資後由政府出資（原話："Beyond that, it's been a government investment."）
- 2026-09-29｜Rex Geveden (CEO)｜customer：CEO：有機會贏下高豐度低濃縮鈾的大部分甚至全部（原話："a chance to win a good chunk of that, if not all of it"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜product：mPower 授權給 Applied Atomics 與 CORE POWER，BWXT 保留 IP 與製造權（原話："We have licensed them this technology."）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜product：微反應爐 BANR 由 BWXT 自己設計並製造整座反應爐（原話："manufacture not just the fuel, but the entire reactor"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜customer：Kairos 為 TRISO 的大型需求訊號，有 Google 支持（原話："Kairos has a big demand signal for TRISO in the near future"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：TRISO 擴產資本已含在 CapEx 目標內（原話："TRISO expansion capital within those targets"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：尚未決定 TRISO 新建全新廠房，需看 HALEU 供應（原話："we have not made a decision on a new greenfield facility"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜risk：俄羅斯鈾進口禁令即將生效（原話："an impending ban on import of Russian uranium"）
- 2026-09-29｜Rex Geveden (CEO)｜risk：CEO：核能與造艦的政治支持跨黨派，選舉結果不太影響（原話："the support for nuclear has endured"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜commitment：CFO：維持股利並持續增加，回購保留為選項（原話："maintain a consistent and growing dividend"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：CFO：沒有足夠再投資機會時將把多餘資本還給股東（原話："we will return incremental capital to shareholders"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：到 2030 年可動用資本約 55 億美元（淨槓桿 2~3 倍）（原話："$5.5 billion of available capital to deploy through 2030"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：扣除 CapEx、股利後仍有約 35 億美元額外部署能力（原話："approximately $3.5 billion of additional capital"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：淨槓桿目標區間 2~3 倍（原話："net leverage within our targeted 2 to 3x range"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：Fitch 給予投資等級評等（原話："Fitch had assigned us an investment-grade rating"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：去年 11 月發行 12.5 億美元零息可轉債（原話："we issued $1.25 billion of convertible notes at a 0% coupon"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：CapEx 目標占營收 5%~6%（原話："we are targeting CapEx at 5% to 6% of revenue"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：維護性資本支出占營收 3.5%~4%（成長性另 1.5%~2%）（原話："3.5% to 4% for maintenance capital"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2026~2030 累計自由現金流超過 20 億美元（原話："over $2 billion of cumulative free cash flow"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2030 前自由現金流低雙位數成長（原話："we're targeting low double-digit free cash flow growth"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜margin：CFO：自由現金流過去高成長來自低基期，不假設持續（原話："not assuming that, that's going to continue indefinitely"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：併購門檻：NPV 為正含可達成綜效（原話："We expect positive NPV, including achievable synergies"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：併購要求第一年 EPS 增益（排除一次性攤銷與整合成本）（原話："We target EPS accretion in year 1"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：CFO：併購規模不再受限於過去交易大小（原話："we're not anchored to the same size of transactions"）
- 2026-09-29｜Rik Geiersbach (Chief Strategy Officer)｜capital_allocation：策略長：併購範圍含小型補強、中型與可能的轉型型交易（原話："some potentially more transformative plays"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：CFO：2030 目標不依賴併購（原話："not beholden to M&A in order to hit our growth outlook"）
- 2026-09-29｜Rex Geveden (CEO)｜capital_allocation：出售多數醫療事業，保留約 20% 權益（原話："We are keeping 20% of that business"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：相較前次投資人日改為提供 2030 年具體目標而非 3~5 年成長率（原話："provide specific 2030 targets for revenue"）
- 2026-09-29｜Rex Geveden (CEO)｜guidance：CEO 說明 2024 年以來營收複合成長 15%，其中有機 8.5%（原話："a 15% revenue CAGR, of which 8.5% is organic"）
- 2026-09-29｜Rex Geveden (CEO)｜margin：CEO：新業務造成利潤率逆風，先不對利潤率達標下定論（原話："new businesses that have created some margin headwinds"）
- 2026-09-29｜Rex Geveden (CEO)｜margin：CEO：利潤率目標先不明確承諾（原話："we won't stick a spear in the ground on that one just yet"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜guidance：商業部門 EBITDA 2030 前年複合成長超過 20%（原話："greater than 20% over that period"）
- 2026-09-29｜Rex Geveden (CEO)｜risk：CEO：HEU 庫存正在消耗（原話："So we're burning that stockpile down"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜customer：政府部門積壓訂單近 70 億美元（原話："almost $7 billion of that is in Government Operations"）
- 2026-09-29｜Rex Geveden (CEO)｜product：CEO：2026 年營收預計 38 億美元（原話："we'll do $3.8 billion in sales this year"）
- 2026-09-29｜Rex Geveden (CEO)｜customer：總積壓訂單由 40 億增至 84 億美元（原話："$4 billion in backlog when I was last standing here"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜customer：技術服務幾乎贏下所有投標（原話："we've won just about every contract that we bid"）
- 2026-09-29｜Rex Geveden (CEO)｜commitment：CEO：以新機組需求類比 70~90 年代，認為未來可能蓋 1,000 座大型機組（原話："It wouldn't surprise me if we build 1,000 large reactors"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜product：太空機會：NASA SR-1 Freedom 為追蹤指標（原話："I would track that one as the space opportunity"）

### 問答異常語氣（迴避／改口／保留）
- BWXT_Q2_2026_Earnings_Call_20260803.md｜問：Ron Epstein：EBITDA 財測上調中有機與非有機各占多少？｜答法：僅回答 "It's mostly organic."，未給數字
- BWXT_Q2_2026_Earnings_Call_20260803.md｜問：Jeffrey Campbell：醫療業務出售所得是否已決定用途？｜答法：回答 "So not exactly"，列出內部投資、併購、還債、買回等可能方向，未給具體分配
- BWXT_Q2_2026_Earnings_Call_20260803.md｜問：Matt Akers：政府業務利潤率 2027 年是否可續升？｜答法：表示不設定 2027 財測，稱需持續維持績效，並說原預期 2027 的表現已提前在 2026 出現，未給 2027 數字
- BWXT_Q2_2026_Earnings_Call_20260803.md｜問：Andre Madrid：Janus 結果不同（OE 或供應商）對經濟效益與貢獻的影響？｜答法：CEO 說 "maybe I'll hold comments on that one"，待談判階段結束後再說明，未給任何經濟面資訊
- BWXT_Q2_2026_Earnings_Call_20260803.md｜問：Scott Deuschle：預期年底前的新設備訂單是吉瓦級大型還是 SMR？｜答法：未指明單一類型，列出 SMR、Darlington、AP1000、X300 等多種機會，改談政府交易與客戶動能
- BWXT_Q2_2026_Earnings_Call_20260803.md｜問：Tomo Sano：mPower 授權的變現模式與下一個里程碑？｜答法：僅提 BWXT 有權利金與製造權；對合作方的變現模式稱 "I'm not clear"，未回答里程碑
- BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md｜問：Bianchi（TD Cowen）：請說明 2030 年服務／燃料／大型零組件組成的圓餅圖會長怎樣｜答法：CFO 表示不會有太大變化，並說明刻意不量化各項機會，不想被綁在單一路徑
- BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md｜問：Ciarmoli（Guggenheim）：成長預測是否已含併購？Westinghouse 訂單金額是否已確定、是否改變成長斜率｜答法：CFO 表示併購放在額外成長機會、沒拆開；Westinghouse 訂單時點與執行未定，稱不想超前，細節留到 Q3；MacQuarrie 只講關係良好、在做資格認證，未給金額
- BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md｜問：Engelbrecht（Baird）：特殊材料（HPDU、離心機）長期利潤率與人力｜答法：Miller 說利潤率會與其他政府客戶類似，但表示現在預測太早，沒給數字
- BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md｜問：Ciarmoli：TRISO 全速量產年市場規模、每公斤成本與營收｜答法：Miller 直接說「不回答這些問題」，改談微反應爐燃料成本占比與 AP1000 比較
- BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md｜問：Chase（線上）：CapEx 2027 年是否仍高於 5~6%｜答法：CFO 表示先前曾示意可能到 7%，現在 2027 目標改為 6%，並拒絕給更細的區間；2027 正式財測幾週後公布
- BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md｜問：Madrid（BTIG）：戰艦與 AUKUS 的上緣有多大、福特級節奏是否可能加速｜答法：CFO 表示未給戰艦與 AUKUS 上緣數字，也不給單艘價格，稱合約上固定成本決定最終價格

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
{"date":"20260905","verdict":"進場·條件式（爆發候選）","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"第二階 1/3：回檔 ≤$130（前瞻本益比 ≤27 倍）或投資人日隱含 FY2028 EPS ≥$6.40／商用利潤率目標 ≥15%；第三階：Q3 政府部門年增 ≥5% 且商用利潤率 ≥12.5%","irr_base_pct":6.2,"ev5y_pct":32.6,"drift_watch_prior":{"dca_verdict":"進場·條件式（爆發候選）","dca_role":"衛星","signal":"B","val":"🔴","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.79,"ev5y_pct":32.6,"irr_base_pct":6.2,"max_dd_pct":-50,"bull_5y_price":307.2,"bear_5y_price":104.0,"p_bull_pct":25,"p_bear_pct":25,"rearm_trigger":"第二階 1/3：回檔 ≤$130（前瞻本益比 ≤27 倍）或投資人日隱含 FY2028 EPS ≥$6.40／商用利潤率目標 ≥15%；第三階：Q3 政府部門年增 ≥5% 且商用利潤率 ≥12.5%","price_at_dd":157.59,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWXT_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
