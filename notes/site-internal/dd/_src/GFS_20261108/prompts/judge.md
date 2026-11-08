你是 stock-analyst **v20 判斷 agent**，標的 GFS（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"GFS","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1786,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"},"note":"高於公司自家指引區間上緣（CEO 說法）；Earnings Whispers 共識約 $1.76B（二手來源，未經 IR 驗證）"},{"id":"f_kpi1_non_ifrs","label":"Non-IFRS 營業利益率","value":16.7,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益率","value":9.7,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"}},{"id":"f_kpi6_q3_2026","label":"下一季（Q3 2026）指引：營收","value":1885,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_gfs_gross_margin_pct","label":"GFS 毛利率","value":28.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GFS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gfs_operating_margin_pct","label":"GFS 營業利益率","value":11.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GFS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gfs_fcf_margin_pct","label":"GFS FCF 利潤率","value":6.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GFS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_2330_tw_gross_margin_pct","label":"2330.TW 毛利率","value":65.85,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_2330_tw_operating_margin_pct","label":"2330.TW 營業利益率","value":57.98,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_2330_tw_fcf_margin_pct","label":"2330.TW FCF 利潤率","value":29.58,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_intc_gross_margin_pct","label":"INTC 毛利率","value":39.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INTC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_intc_operating_margin_pct","label":"INTC 營業利益率","value":10.06,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INTC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_intc_fcf_margin_pct","label":"INTC FCF 利潤率","value":6.29,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INTC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_005930_ks_gross_margin_pct","label":"005930.KS 毛利率","value":57.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_operating_margin_pct","label":"005930.KS 營業利益率","value":36.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_fcf_margin_pct","label":"005930.KS FCF 利潤率","value":28.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2303_tw_gross_margin_pct","label":"2303.TW 毛利率","value":31.71,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2303.TW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_2303_tw_operating_margin_pct","label":"2303.TW 營業利益率","value":21.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2303.TW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_2303_tw_fcf_margin_pct","label":"2303.TW FCF 利潤率","value":25.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2303.TW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3","label":"營業現金流","value":405,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"}},{"id":"f_kpi4_non_ifrs","label":"調整後自由現金流（Non-IFRS）","value":-3,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"}},{"id":"f_kpi5_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":49.4,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":38.62,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-47.69,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":35.66,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.96 → 1.96）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.63 → 2.63）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.61 → 3.61）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.96,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.63,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.61,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 1.96 → 1.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":110.34,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.01,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.94,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":19.7,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 1.96，分子＝快照價 38.62","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.621,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-539.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 1716.0、現金 2255.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":557.45,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":20989.67,"period":"2026-11-08","unit":"USD m","basis":"市值 21528.67 ＋ 淨負債 -539.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":7323.06,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":8294.54,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（22 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.87,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 38.62 / W52 51.45 / W104 44.58 / W250 50.57 / W250 13週斜率 -0.5%"},{"id":"f_ma_w52","label":"52 週均線","value":51.45,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":44.58,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":50.57,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-0.5,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Counterpoint 純晶圓代工季度份額：GFS 由 2024Q4 約 5% 降至 2025 年 4%，2026Q1 為 3%；TSMC 2026Q1 佔 73%，產業年增 30%（AI GPU/ASIC 驅動）。","source":"Counterpoint Research, Global Pure Foundry Market Share: Quarterly","url":"https://www.counterpointresearch.com/en/insights/global-semiconductor-foundry-market-share","excerpt":null,"as_of":"2026-03-31","retrieved_at":"2026-10-12","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"TrendForce 稱 GFS 2025 年晶圓代工營收排名第五、份額 3.87%；Tower 第七、0.89%；GFS 與 Tower 在 RF、矽光子等利基競爭。","source":"TrendForce News via Reuters (搜尋摘要轉述)","url":"https://www.trendforce.com/news/?p=55236","excerpt":null,"as_of":"2026-03-01","retrieved_at":"2026-10-12","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2026Q1 管理層稱 design wins 年增約 50%，四大終端市場皆有；車用嵌入式 MRAM 客戶已 tape-out，與 Bosch 等一級供應商接觸增加。","source":"GlobalFoundries Q1 2026 earnings call transcript (Motley Fool)","url":"https://www.fool.com/earnings/call-transcripts/2026/05/05/globalfoundries-gfs-q1-2026-earnings-transcript/","excerpt":"In the first quarter, we saw a 50% increase in design wins compared to the same period a year ago, with excellent representation across all 4 major end markets.","as_of":"2026-05-05","retrieved_at":"2026-10-12","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2026Q2：GFS 取得七項光網路（AI 資料中心）design wins，涵蓋收發器廠、超大規模業者與網通公司；另有一項 SCALE 平台 CPO 相關設計 tape-out，預期 Q3 再一項（二手摘要）。","source":"MarketBeat, GlobalFoundries Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/globalfoundries-q2-earnings-call-highlights-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-12","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"TrendForce 2Q26：前十大代工營收季增 11.5% 至近 534.9 億美元，SMIC 縮小與 Samsung 的份額差距；摘要未提 GFS 當季數字。","source":"TrendForce press center, 2026-09-09","url":"https://www.trendforce.com/presscenter/news/20260909-13225.html","excerpt":null,"as_of":"2026-09-09","retrieved_at":"2026-10-12","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Simply Wall St 社群敘事（非公司/機構資料）主張 GFS 先進製程落後 TSMC/Samsung，且在地化要求與客戶垂直整合為風險；未找到 2026 針對 GFS 的具名新進入者報導。","source":"Simply Wall St community narrative","url":"https://simplywall.st/community/narratives/us/semiconductors/nasdaq-gfs/globalfoundries/w0hqa7cr-legacy-fabs-will-suffer-as-tsmc-and-samsung-lead","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-12","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"GF 20-F 風險因素：部分 OEM 可能自行開發 in-house ASIC、繞過 fabless 的 GF 客戶並改採其他晶圓代工策略；幾乎所有客戶都有自家設計能力。","source":"SEC EDGAR 20-F FY2025 Item 3.D Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904826000022/gfs-20251231.htm","excerpt":"Some original equipment manufacturers may develop their own in-house application-specific ICs, cut out the fabless GF customer and adopt a different foundry strategy. Nearly all of our customers already maintain their own semiconductor design capability, and they may choose to leverage those design resources instead of utilizing our services.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"2025 年 Smart Mobile Devices 營收年減 12.1%，部分原因是客戶雙供應來源（dual sourced）處的價格調整；單一來源產品約占晶圓出貨量 63%。","source":"SEC EDGAR 20-F FY2025 Item 5","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904826000022/gfs-20251231.htm","excerpt":"Smart Mobile Devices decreased by 12.1% year-over-year, primarily due to lower underutilization payments from customers and pricing adjustments where customers are dual sourced.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2024 20-F：兩個匿名客戶各超過營收 10%，Customer A 2024 年占 16%（$1,061M）、Customer B 占 11%（$722M）；客戶名稱未揭露。","source":"GLOBALFOUNDRIES Form 20-F FY2024 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904825000024/gfs-20241231.htm","excerpt":"Customer A accounted for $1,061 million, or 16%, in 2024, and Customer B $722 million, or 11%.","as_of":"2024-12-31","retrieved_at":"2026-10-12","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2021 20-F：前十大客戶占晶圓出貨量 2019/2020/2021 年約 73%/73%/67%；公司預期營收仍將集中在少數客戶。","source":"GLOBALFOUNDRIES Form 20-F FY2021 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904822000008/gfs-20211231.htm","excerpt":"Our ten largest customers in 2019, 2020 and 2021 accounted for approximately 73%, 73% and 67% of our wafer shipment volume, respectively.","as_of":"2021-12-31","retrieved_at":"2026-10-12","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TrendForce 預估 2026 年前十大晶圓代工 8 吋平均稼動率近 90%（2025 約 80%），全球 8 吋產能至 2027 上半年續呈負成長","source":"TrendForce／iconnect007 mature-node foundry price increases","url":"https://evertiq.com/news/2026-05-07-mature-node-foundry-prices-set-to-rise-as-ai-demand-tightens-capacity","excerpt":"The average 8-inch capacity utilisation rate among the world's ten largest foundries is projected to approach 90% in 2026, up from around 80% in 2025; TrendForce expects global 8-inch capacity to remain in negative growth through the first half of 2027.","as_of":"2026-05-07","retrieved_at":"2026-10-12","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"成熟製程晶圓代工 2026 Q1→Q2 全面漲價 5–15%，第三輪漲價可能從 2026 下半年延續到 2027","source":"TrendForce／evertiq","url":"https://evertiq.com/news/2026-05-07-mature-node-foundry-prices-set-to-rise-as-ai-demand-tightens-capacity","excerpt":"The industry is also preparing a third round of price increases that could extend from the second half of 2026 into 2027.","as_of":"2026-05-07","retrieved_at":"2026-10-12","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"12 吋擴產近 70% 來自中國晶圓廠，其餘地區擴產溫和；TSMC 縮減 12 吋成熟產能預期將轉單給其他代工廠","source":"TrendForce／iconnect007","url":"https://iconnect007.com/article/150606/ai-chip-shortage-foundry-cuts-to-extend-maturenode-price-hikes-in-2027/150603/smt","excerpt":"Nearly 70% of capacity expansion in this segment is being driven by Chinese foundries, while expansion elsewhere remains moderate.","as_of":"2026-06-30","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"TrendForce 2023 年預測中國成熟製程產能占比 2027 年達 39%，並警告 CIS、DDI、PMIC、功率離散元件可能價格競爭（舊預測，早於 2026 年緊俏）","source":"TrendForce press 2023-12-14","url":"https://www.trendforce.com/presscenter/news/20231214-11959.html","excerpt":null,"as_of":"2023-12-14","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"GF 管理層：通訊基礎建設與資料中心營收年增 62%，預期 2026 年該區塊成長 50–60%，矽光子營收翻倍以上；SiGe 產能至 2027 已超額訂購並擴產","source":"GlobalFoundries Q2 2026 earnings call highlights (MarketBeat)","url":"https://www.marketbeat.com/instant-alerts/globalfoundries-q2-earnings-call-highlights-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-12","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"GF 2026 Q2 財報電話會議：車用與智慧行動營收轉弱，家用與工業 IoT 改善","source":"GlobalFoundries Q2 2026 earnings call highlights (MarketBeat)","url":"https://www.marketbeat.com/instant-alerts/globalfoundries-q2-earnings-call-highlights-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"UBS 逆市場共識認為成熟製程晶圓代工進入上行週期（供給重分配驅動），預期 2027–2028 獲利更有上檔","source":"UBS view via Webull news","url":"https://www.webull.com/news/15654887556711424","excerpt":"Earlier, UBS put forward the opposite view from market consensus, that the mature process foundry industry will usher in an upward cycle, which is driven by the reallocation of supply and resources throughout the industry.","as_of":"2026-06-30","retrieved_at":"2026-10-12","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#7","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"消費性電子受記憶體漲價與零組件成本拖累，2026 下半年出貨承壓，部分客戶希望延後漲價","source":"TrendForce DRAMeXchange weekly research","url":"https://dramexchange.com/WeeklyResearch/Post/2/12752.html","excerpt":null,"as_of":"2026-06-30","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"新加坡競爭及消費者委員會（CCCS）於 2026-04-13 裁定 GFS 已完成的 Advanced Micro Foundry 收購未造成實質減損競爭（審查範圍限於可插拔收發器代工服務）；屬結構性放行，非調查。","source":"CCCS public register: Acquisition by GlobalFoundries Singapore Pte. Ltd. of Advanced Micro Foundry Pte. Ltd.","url":"https://www.ccs.gov.sg/case-register/public-register/mergers-and-acquisitions/acquisition-by-globalfoundries-singapore-pte--ltd--of-advanced-micro-foundry-pte--ltd-/","excerpt":null,"as_of":"2026-04-13","retrieved_at":"2026-10-12","affects":["moat_trend","triggers"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"GFS 向 ITC 提出專利侵權申訴，ITC 於 2026-04-27 對 Tower 製造的晶片立案調查，GFS 請求有限排除令與停止令；屬 IP 案件，非反壟斷，尚無裁決。","source":"Federal Register via policyrisk.com: ITC Investigates Imported Chips for Patent Sneakiness in Tech Wars","url":"https://policyrisk.com/federal-register/2026-08439","excerpt":null,"as_of":"2026-04-27","retrieved_at":"2026-10-12","affects":["moat_trend","triggers"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2024-11 美國商務部 BIS 就 GFS 2021-02 至 2022-10 間向實體清單中國公司出口晶圓的違規予以處罰（GFS 承認違反 EAR）；屬過往出口管制執法。","source":"Linklaters: Due Diligence in China's Semiconductor Value Chain - Lessons from the GlobalFoundries Enforcement Case","url":"https://www.linklaters.com/knowledge/publications/alerts-newsletters-and-guides/2024/november/07/due-diligence-in-chinas-semiconductor-value-chainlessons-from-the-global-foundries-enforcement-cas","excerpt":null,"as_of":"2024-11-07","retrieved_at":"2026-10-12","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"GFS FY2025 20-F：2026年1月總統公告對有限的先進運算晶片及部分衍生產品加徵25%關稅；公司稱不認為其業務目前受此關稅牽涉，但仍可能有進一步關稅（含歐洲）。","source":"GLOBALFOUNDRIES Inc. Form 20-F FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904826000022/gfs-20251231.htm","excerpt":"Although we do not believe our business is currently implicated by the new tariffs","as_of":"2026-01-15","retrieved_at":"2026-10-12","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026年1月Section 232公告：對窄範圍先進半導體加徵25%關稅，生效2026-01-15；美國資料中心用晶片等用途豁免；後續可能擴大並設投資美國產能的關稅抵減機制。","source":"White & Case / EY Global Tax News：Section 232 semiconductor proclamation","url":"https://taxnews.ey.com/news/2026-0209-us-section-232-proclamation-imposes-25-percent-tariff-on-certain-semiconductors","excerpt":null,"as_of":"2026-01-15","retrieved_at":"2026-10-12","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2024-11-01 BIS 對 GFS 處以50萬美元和解罰款：2021–2022年向實體清單公司 SJ Semiconductor 出貨約1,710萬美元晶圓未取得許可；GFS自行揭露並合作，歸因於交易篩查系統資料輸入錯誤。","source":"Manufacturing Dive / BIS 執法案","url":"https://www.manufacturingdive.com/news/commerce-department-globalfoundries-500k-fine-sj-semiconductor-entity-list/733768/","excerpt":null,"as_of":"2024-11-01","retrieved_at":"2026-10-12","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Yahoo Finance 報導（Wedbush 降評）稱聯邦指引顯示對中國半導體關稅要到2027年6月才生效，更激進的Section 232措施近期較不可能；未對照政府原文確認。","source":"Yahoo Finance: Wedbush downgrades GlobalFoundries","url":"https://finance.yahoo.com/news/wedbush-downgrades-globalfoundries-sees-more-132056656.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-12","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"據 policyrisk.com 對 SEC 申報的摘要，GF 對單一 SOI 晶圓供應商（摘要指為 Soitec）的採購占比為 2025 年 71.4%、2024 年 60.9%、2023 年 63.0%；替換該供應商需時甚長。部分原料（稀土、天然氣）亦有單一來源，價格與供應受美中貿易緊張及烏克蘭、中東衝突影響。（二手摘要，未核對申報原文）","source":"policyrisk.com GFS company page（SEC 申報摘要）","url":"https://policyrisk.com/world/company/GFS","excerpt":null,"as_of":"2026-02-01","retrieved_at":"2026-10-12","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"GF 申報文件的風險語言提及其業務可能受地緣政治狀況影響，例如與中國的政治與貿易緊張（2024 年 6-K 與投資人文件；非 2026 專屬揭露）。","source":"GLOBALFOUNDRIES Form 6-K 3Q2024 earnings","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904824000061/globalfoundries3q2024earni.htm","excerpt":null,"as_of":"2024-11-12","retrieved_at":"2026-10-12","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2025 年 4 月有報導稱 GF 與台灣聯電（UMC）洽談合併，背景為台灣風險與中國成熟製程擴張；UMC 財務長否認有此案。","source":"Electronics360 / GlobalSpec: Report: GF and UMC mull chip foundry merger","url":"https://electronics360.globalspec.com/article/22133/report-gf-and-umc-mull-chip-foundry-merger","excerpt":null,"as_of":"2025-04-01","retrieved_at":"2026-10-12","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"第三方評論稱 GF 紐約 Malta 廠具美國國防部 Trusted Foundry 認證，並獲最高 15.75 億美元聯邦 CHIPS 補助及紐約州 5.5 億美元，被視為降低對台灣產能依賴的緩衝（TradingView 使用者文章，屬意見而非公司揭露，未核實）。","source":"TradingView GFS 使用者文章","url":"https://pl.tradingview.com/chart/GFS/fWfqAsxk/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-12","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"產業層面：Fusion 2026 Q1 報告指台灣中斷將立即觸發全球「Level 1」供應危機；Design News 指 AI 需求把產能拉向先進製程，類比與混合訊號晶片廠在成熟製程晶圓配額上競爭縮水的分配。","source":"Fusion Worldwide MILT 26Q1; Design News","url":"https://info.fusionww.com/hubfs/Q1%202026%20Industry%20and%20Intelligence%20Reports/Fusion%20MILT%20-%2026Q1.pdf?hsLang=en","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-12","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 通訊基建與資料中心段營收年增 62%（上半年 +47%），來自 SiPh 與 SiGe 需求；管理層將 2026 全年該段成長展望上調至 50–60%（原高 30% 區間）。","source":"GLOBALFOUNDRIES Form 6-K (Q2 2026); MarketBeat Q2 call highlights","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000219/gfs-20260630_d2.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-12","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q2 2026 車用營收年減 9.5%（客戶出貨遞延至下半年），上半年仍 +5.6%；Q1 車用年增 24%，管理層當時預期全年低雙位數成長。","source":"GLOBALFOUNDRIES Form 6-K (Q2 2026); Motley Fool Q1 2026 transcript","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000219/gfs-20260630_d2.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-12","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Q2 2026 智慧行動裝置段營收年減 5.7%（上半年 -5.3%），歸因記憶體價格導致智慧手機疲弱；居家與工業 IoT 段 Q2 +10.3%、上半年 -6.7%，管理層上調 IoT 展望。","source":"GLOBALFOUNDRIES Form 6-K (Q2 2026); MarketBeat Q2 call highlights","url":"https://www.marketbeat.com/instant-alerts/globalfoundries-q2-earnings-call-highlights-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 營收 $1.786B（季增 9%、年增 6%）；Q3 指引 $1.885B ±$25M，非 IFRS 毛利率 30.5% ±100bps。","source":"MarketBeat / Quartr Q2 2026 summary","url":"https://quartr.com/events/globalfoundries-inc-gfs-q2-2026_ojFuZzVo","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-12","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"GF 預期矽光營收 2026 年超過倍增，目標 2028 年底矽光年化營收達 $10 億，長期 $20 億；共封裝光學拐點在 2028 年底至 2029 年；GF 估計 2030 年可服務市場約 $110 億。","source":"Nasdaq/Yahoo: GlobalFoundries maps path to 40% margins; iAmsterdam summary; TrendForce 2026-05-07","url":"https://www.nasdaq.com/articles/globalfoundries-maps-path-40-margins-silicon-photonics-demand-builds","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-12","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"成熟製程晶圓代工報價走升：分析師預期 UMC 2026 下半年漲價 5–10%、2027 再 5–10%；TrendForce 預估 2026 年 8 吋前十大廠平均稼動率近 90%（2025 約 80%）；TrendForce 2026 年 9 月稱消費 IC 客戶 Q3 晶圓價格可能上漲。無 GF 自身調價資料。","source":"Evertiq 2026-05-07 Mature node foundry prices set to rise; TrendForce press release 20260909; StreetInsider UMC pricing report","url":"https://evertiq.com/news/2026-05-07-mature-node-foundry-prices-set-to-rise-as-ai-demand-tightens-capacity","excerpt":null,"as_of":"2026-09-09","retrieved_at":"2026-10-12","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"-","claim":"Counterpoint 純代工市佔表：GF 2026 Q1 約 3%，2024 Q4 為 5%；TSMC 73%。","source":"Counterpoint Research Global Pure Foundry Market Share: Quarterly","url":"https://www.counterpointresearch.com/en/insights/global-semiconductor-foundry-market-share","excerpt":null,"as_of":"2026-06-01","retrieved_at":"2026-10-12","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"-","claim":"IDC 2026 年 2 月預測 2026 智慧手機出貨年減 12.9% 至約 11.2 億支、2027 年 +2%；後續（約 2026 年 6 月，二手報導）修正為 2026 年 -13.9% 至約 10.9 億支、2027 年 -1.1%、2028 年 +5.5%。IDC 預期記憶體晶片價格 2027 年中趨穩。","source":"eeNews Europe / Gigazine (IDC Feb 2026); IT Brief (IDC revision, secondary)","url":"https://www.eenewseurope.com/en/smartphone-memory-shortage-2026-idc/","excerpt":null,"as_of":"2026-02-27","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#8","axis":"end_markets","section":"coverage","direction":"0","claim":"S&P Global 2026 年 3 月車用半導體需求報告：記憶體恐成瓶頸；功率半導體隨電動化成長，MCU 與類比仍關鍵且與產量連動。Meticulous Research（2026 年 5 月）估車用半導體 2025 年 $638 億、2026 年 $724 億，2026–2036 CAGR 7.4%。無主要機構的當期 2027 預測。","source":"S&P Global Inside automotive semiconductor demand 2026; Meticulous Research","url":"https://autotechinsight.spglobal.com/shop/product/5003699/inside-automotive-semiconductor-demand-2026","excerpt":null,"as_of":"2026-05-01","retrieved_at":"2026-10-12","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"GFS FY2025 20-F 風險揭露未見專門的技術替代/過時風險條款；最接近者為提前投產致庫存/過時成本，及技術在廠間轉移時若需求驟降會衝擊整廠稼動率。","source":"SEC GLOBALFOUNDRIES Form 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904826000022/gfs-20251231.htm","excerpt":"This exposes us to the risk that our operations, including our utilization rate for entire fabs, may be severely impacted if demand for those technologies drops suddenly or for an extended period.","as_of":"2026-03-01","retrieved_at":"2026-10-12","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"FY2023 20-F 載明技術與服務價格隨時間下滑，未推出新技術可能迫使既有技術降價。","source":"SEC GLOBALFOUNDRIES Form 20-F FY2023","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904824000013/gfs-20231231.htm","excerpt":"the market prices for technology and services tend to fall over time, except in times of extreme supply shortage.","as_of":"2024-03-01","retrieved_at":"2026-10-12","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"矽光子被報導為特殊製程晶圓廠的成長線：GFS 管理層預期 2026 年矽光子營收約倍增、2028 年可能超過 10 億美元（為 GFS 自有技術的成長面，非替代威脅）。","source":"TrendForce News 2026-05-07 GlobalFoundries silicon photonics revenue","url":"https://www.trendforce.com/news/2026/05/07/news-globalfoundries-reportedly-sees-silicon-photonics-revenue-doubling-in-2026-passing-1b-by-2028/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"2026-10-12","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"中國成熟製程晶圓廠持續擴張：Nexchip 28nm 邏輯平台於 2026-03-11 完成開發，Silan、Hua Hong 亦擴產與製程升級（競爭壓力，非替代技術）。","source":"TrendForce News 2026-03-26 Nexchip, Silan and Hua Hong mature node","url":"https://www.trendforce.com/news/2026/03/26/news-nexchip-silan-and-hua-hong-step-up-efforts-in-advancing-mature-node-foundry/","excerpt":null,"as_of":"2026-03-26","retrieved_at":"2026-10-12","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"+","claim":"IDC 預期 2026 年全球 8 吋產能下滑約 3%，部分晶圓廠漲價最高 10%，成熟製程供需轉向。","source":"IDC press release Foundry 2.0 market 360B 2026","url":"https://www.idc.com/resource-center/press-releases/foundry-2-0-market-360b-2026/","excerpt":null,"as_of":"2026-03-30","retrieved_at":"2026-10-12","affects":["valuation","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"GF 2026 年 6 月收購 Synopsys ARC 處理器 IP 業務，公司稱此使其成為提供「軟體到矽」能力的整體技術夥伴（由純代工往解決方案延伸）。","source":"GLOBALFOUNDRIES Form 6-K, Q2 2026 earnings","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm","excerpt":"holistic technology partner, offering customers a software-to-silicon capability for Physical AI and beyond","as_of":"2026-08","retrieved_at":"2026-10-12","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2026 年 5 月 GF 推出 Quantum Technology Solutions，預期獲美國商務部 3.75 億美元補助。","source":"GLOBALFOUNDRIES Form 6-K, Q2 2026 earnings","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm","excerpt":null,"as_of":"2026-08","retrieved_at":"2026-10-12","affects":["thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"GM 與 GF 簽直接長約（繞過晶片設計商），為專屬產能協議；屬 2023 年舊事，非 2026 新變化。","source":"eeNews Europe: GM signs first long term supply deal direct with GlobalFoundries","url":"https://www.eenewseurope.com/en/gm-signs-first-long-term-supply-deal-direct-with-globalfoundries/","excerpt":null,"as_of":"2023-02-09","retrieved_at":"2026-10-12","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026 指引（2026-08-05）：營收約 18.85 億美元（±0.25 億）、non-IFRS 稀釋 EPS 0.51（±0.05）、non-IFRS 營業利益率 16.7%±170bps；EPS 指引區間 0.46–0.56 對比共識約 0.47（另一來源 0.49／營收 18.7 億），大致貼近共識","source":"MarketBeat: GlobalFoundries issues Q3 2026 earnings guidance; SEC 6-K Q2 2026","url":"https://www.marketbeat.com/instant-alerts/globalfoundries-nasdaqgfs-issues-q3-2026-earnings-guidance-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-12","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 營收指引發布後 Chartmill 報導盤前約下跌 5.5%，稱 Q3 營收預測略低於市場預期；Benzinga 則稱營收預測較前次區間 17.4–17.8 億上調，兩來源對「上調或略低」解讀不一","source":"Chartmill: GlobalFoundries Dips After Q3 Revenue Forecast Trails Estimates; Benzinga earnings forecasts","url":"https://www.chartmill.com/news/GFS/Chartmill-52785-GlobalFoundries-NASDAQGFS-Dips-After-Q3-Revenue-Forecast-Trails-Estimates","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-12","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 調整後 EPS 0.46 vs 共識 0.43，營收 17.9 億美元（年增 5.8%）；管理層稱營收與 non-IFRS 獲利指標達或高於指引區間高端；資料中心與通訊營收 2026 預期成長 50–60%，矽光子營收將翻倍以上","source":"MarketBeat: posts quarterly earnings results beats estimates by $0.03 EPS; Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/globalfoundries-nasdaqgfs-posts-quarterly-earnings-results-beats-estimates-by-003-eps-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-12","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 統計 2022-11 至 2026-08 間公司上調展望 7 次、下調 4 次","source":"Benzinga GFS earnings forecasts","url":"https://www.benzinga.com/quote/GFS/earnings-forecasts","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-12","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布最新快照（Investing.com，約 2026-10）：21 位分析師，12 買／9 持有／1 賣，平均目標價 80.24 美元，高 125、低 60；Arete 升至 95 為最近動作。較早快照：MarketBeat 2026-08-05 共識 Hold、平均 74.12；Benzinga 2026-08-14 平均 63（19 位分析師，中性）；StockAnalysis 2026-06 為 78.95；Fintel 平均 79.38、高 147。各聚合站快照日期不一，分布不一致","source":"Investing.com GlobalFoundries consensus estimates; MarketBeat; Benzinga sentiment; StockAnalysis; Fintel","url":"https://uk.investing.com/equities/globalfoundries-consensus-estimates","excerpt":null,"as_of":"2026-10-12","retrieved_at":"2026-10-12","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"賣方個別調整：2026-02 UBS 目標價 45→50（Neutral）、TD Cowen 42→56（Buy）、Baird 40→60（Outperform）；JPMorgan Harlan Sur 維持 Neutral、目標價 40→35 並稱 2026 市場預期可能過於樂觀（該則日期未標示，可能為 2025 年）","source":"Yahoo Finance: UBS Raises its Price Target on GLOBALFOUNDRIES to $50; Benzinga","url":"https://finance.yahoo.com/news/ubs-raises-price-target-globalfoundries-110743438.html","excerpt":null,"as_of":"2026-02-28","retrieved_at":"2026-10-12","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#6","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Axelrod Research 2026-10-07 筆記評級 HOLD，稱 2026-10-06 收盤 48.63 美元，對比 2026-05-09 的 74.12 美元（該筆記依 5 月營運快照，非新財報修正）","source":"Axelrod Research: GFS the foundry thesis survives","url":"https://buttondown.com/user75/archive/axelrod-research-gfs-the-foundry-thesis-survives/","excerpt":null,"as_of":"2026-10-07","retrieved_at":"2026-10-12","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"GF 於 2026-01-14 簽約收購 Synopsys ARC 處理器 IP 業務，2026-06 初完成；總對價 4.55 億美元（含現金 4.4 億）。","source":"SEC EDGAR 6-K（期間至 2026-06-30）；MarketScreener 收購完成報導","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000219/gfs-20260630_d2.htm","excerpt":null,"as_of":"2026-06-02","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 20-F：法律程序屬一般營運範圍，公司認為結果不會對營運、財務重大影響。","source":"SEC EDGAR 20-F FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904826000022/gfs-20251231.htm","excerpt":"Based on the information currently available to us, we believe that the outcome of these proceedings would not have a material impact on our results of operations, financial condition, business and prospects.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"TrendForce 報導：12 吋成熟製程擴產約 70% 由中國晶圓廠驅動；SMIC、華虹、晶合（Nexchip）新廠陸續投產，Nexchip 合肥四期 51 億美元擴 28nm。","source":"TrendForce News / Tom's Hardware（搜尋摘要轉述）","url":"https://tomshardware.com/tech-industry/semiconductors/the-trailing-edge-foundry-roadmap-examined","excerpt":null,"as_of":"2026-06-30","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"TrendForce 預期全球 8 吋產能至 2027 上半年續負成長，漲價趨勢延伸至 2027；TSMC 6 吋 Fab 2 與 8 吋 Fab 5 預計 2027 年底前關閉。","source":"TrendForce Press Center 2026-06-30","url":"https://www.trendforce.com/presscenter/news/20260630-13127.html","excerpt":null,"as_of":"2026-06-30","retrieved_at":"2026-10-12","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"IDC 預期 2026 全球 8 吋產能約降 3%，TSMC 與 Samsung 開始削減 8 吋；TSMC 預計 2028 前將 Fab14 12 吋成熟製程產能削減 15–20%；2026 Q1→Q2 晶圓代工價格約漲 5–15%。","source":"IDC / iconnect007 / finviz（搜尋摘要轉述）","url":"https://iconnect007.com/article/150606/ai-chip-shortage-foundry-cuts-to-extend-maturenode-price-hikes-in-2027/150603/ein","excerpt":null,"as_of":"2026-03-30","retrieved_at":"2026-10-12","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"GF 2026 capex 指引為營收 15–20%（2025 為 8%）；宣布德勒斯登廠產能倍增（目標 2032 完成）；華虹無錫專案約 67 億美元、月增約 3 萬片；SMIC 2026 資本支出預測 80 億美元以上；UMC capex 持平、新加坡投產延至 2026。","source":"Fab Tracker February 2026 (GF IR) / Tom's Hardware（搜尋摘要轉述）","url":"https://s29.q4cdn.com/619069826/files/doc_financials/2025/q4/Fab-Tracker-February-2026.pdf","excerpt":null,"as_of":"2026-02-28","retrieved_at":"2026-10-12","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"TrendForce 3 月晶圓代工簡報：華虹 capex 高峰已過；SMIC 擴產步調趨緩（消費需求逆風）；GF 為美歐在地化提高 capex。","source":"TrendForce Foundry Market Bulletin 2026-03-02","url":"https://www.trendforce.com/research/download/RP260302TJ3","excerpt":null,"as_of":"2026-03-02","retrieved_at":"2026-10-12","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"TrendForce 2026年6月分析：消費電子庫存回補、AI需求、地緣因素與TSMC逐步退出成熟製程，正在重塑成熟製程供需；另警告電視與筆電提前備貨使2H26庫存有疑慮。","source":"TrendForce, Mature Node Repricing: AI Squeeze Reshapes Foundry Landscape","url":"https://www.trendforce.com/research/download/RP260629VB3","excerpt":null,"as_of":"2026-06-29","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"TrendForce 2026年4月：成熟製程價格或在2026回升，但庫存過剩與中國同業競爭仍構成壓力。","source":"TrendForce News, Mature node prices may rebound in 2026 but inventory overhang and China competition weigh","url":"https://www.trendforce.com/news/2026/04/03/news-mature-node-prices-may-rebound-in-2026-but-inventory-overhang-and-china-competition-weigh/","excerpt":null,"as_of":"2026-04-03","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"TrendForce：2026年Q1至Q2晶圓代工價格普遍上漲約5%至15%，第三輪漲價可能自2026年底延續至2027；8吋稼動率2026年達88%、2H26預估90%，TSMC與Samsung縮減8吋產能。","source":"TrendForce press release 2026-06-30 (via iconnect007 / trendforce.com presscenter)","url":"https://www.trendforce.com/presscenter/news/20260630-13127.html","excerpt":null,"as_of":"2026-06-30","retrieved_at":"2026-10-12","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"GF自身存貨2026-06-30為16.22億美元（2025-12-31為15.77億；2026-03-31為16.86億），存貨備抵由9,000萬增至1.4億美元。未找到GF 2026年客戶/通路庫存水位的揭露。","source":"GlobalFoundries Form 6-K (quarter ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000219/gfs-20260630_d2.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"2026-10-12","affects":["valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"FY2024 營收 67.5 億美元，較 FY2023 的 73.92 億下降 9%（-6.42 億）","source":"GlobalFoundries Reports Fourth Quarter 2024 and Fiscal Year 2024 Financial Results","url":"https://investors.gf.com/news-releases/news-release-details/globalfoundries-reports-fourth-quarter-2024-and-fiscal-year-2024/","excerpt":"Net revenue was $6,750 million in FY2024 versus $7,392 million in FY2023, a $642 million or 9% decline.","as_of":"2025-02-11","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"FY2024 GAAP 毛利率 24.5%，較 FY2023 的 28.4% 下滑 390bp；非 IFRS 毛利率 25.3% vs 29.1%（搜尋摘要之轉述，未取得逐字原文）","source":"GlobalFoundries Q4/FY2024 earnings release (6-K)","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904825000017/globalfoundries4q2024earni.htm","excerpt":null,"as_of":"2025-02-11","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2024 年季度調整後毛利率：Q2 25.2%（年減 440bp）、Q3 24.7%、Q4 25.4%；去庫存壓力來自客戶庫存偏高，Q2 營收年減 12%","source":"Benzinga: GlobalFoundries Exceeds Q2 Projections, Navigates High Inventory Levels In Chip Market","url":"https://www.benzinga.com/news/earnings/24/08/40192110/globalfoundries-exceeds-q2-projections-navigates-high-inventory-levels-in-chip-market","excerpt":"the adjusted gross margin declined by 440 bps to 25.2%","as_of":"2024-08-06","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2024 年 9 月 GFS 股價單月下跌 13.8%，年初至 9 月累計約 -36%，同期 TSMC +73%","source":"Motley Fool: Why GlobalFoundries Stock Fell 14% Last Month","url":"https://www.fool.com/investing/2024/10/04/why-globalfoundries-stock-fell-14-last-month","excerpt":"the stock has slid 36% lower in 2024 while larger rival Taiwan Semiconductor Manufacturing posted a 73% price gain","as_of":"2024-10-04","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#4","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Q4 2024 另認列 9.35 億美元與 Malta, NY 產能相關減損，毛利率收縮、展望低於市場預期","source":"Benzinga: GlobalFoundries Q4 Earnings: Revenue And EPS Beat, Margins Shrink, Revenue Outlook Disappoints Street","url":"https://www.benzinga.com/25/02/43623967/globalfoundries-beats-q4-estimates-margins-shrink-935-million-impairment-charge","excerpt":null,"as_of":"2025-02-11","retrieved_at":"2026-10-12","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#5","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"產業週期長度：TechInsights 統計 1963 年以來 14 次衰退期，平均約每 4.4 年一次；另有分析指 Micron 前兩輪下行持續 7 與 9 季（以 EBITDA 毛利峰谷計，非 GFS 專屬）","source":"TechInsights: The Chip Insider – Cyclical History of the Semiconductor Industry; Seeking Alpha: Micron: How Low Will It Go?","url":"https://www.techinsights.com/blog/chip-insiderr-cyclical-history-semiconductor-industry","excerpt":null,"as_of":"2023-01-01","retrieved_at":"2026-10-12","affects":["thesis.R","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"GF 2026-01-14 簽約、2026-06 初完成收購 Synopsys ARC 處理器 IP 業務；總對價 4.55 億美元（含現金 4.4 億）。","source":"SEC EDGAR 6-K（期間至 2026-06-30）","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000219/gfs-20260630_d2.htm","excerpt":null,"as_of":"2026-06-02","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"20-F 稱 Cayman 律師不知有向開曼法院提起的集體訴訟；搜尋亦未見針對 GF 的證券集體訴訟。","source":"SEC EDGAR 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904826000022/gfs-20251231.htm","excerpt":"Maples and Calder (Cayman) LLP, our Cayman Islands counsel, is not aware of any reported class action suits having been brought in a Cayman Islands court.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"2026-03-26 向 ITC 提出 337 條款專利侵權申訴，申請人為 GlobalFoundries U.S. Inc.（GF 為原告）。","source":"Federal Register 2026-08439","url":"https://open-gov.usebase.io/federal-register/2026-08439","excerpt":null,"as_of":"2026-03-26","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"GFS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":28.47,"operating_margin_pct":11.74,"fcf_margin_pct":6.01,"rd_intensity_pct":8.71},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GFS","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"2330.TW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":65.85,"operating_margin_pct":57.98,"fcf_margin_pct":29.58,"rd_intensity_pct":5.96},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"INTC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":39.9,"operating_margin_pct":10.06,"fcf_margin_pct":6.29,"rd_intensity_pct":22.46},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INTC","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"005930.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.48,"operating_margin_pct":36.88,"fcf_margin_pct":28.95,"rd_intensity_pct":9.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"2303.TW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":31.71,"operating_margin_pct":21.83,"fcf_margin_pct":25.76,"rd_intensity_pct":7.07},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2303.TW","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"GFS"},"financial_history":{"ticker":"GFS","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":8108000000.0,"revenue_yoy_pct":null,"gross_margin_pct":27.61,"operating_margin_pct":15.55,"net_income":1448000000.0,"diluted_eps":2.62,"free_cash_flow":-435000000.0,"fcf_margin_pct":-5.37,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":7392000000.0,"revenue_yoy_pct":-8.83,"gross_margin_pct":28.42,"operating_margin_pct":16.23,"net_income":1020000000.0,"diluted_eps":1.83,"free_cash_flow":321000000.0,"fcf_margin_pct":4.34,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":6750000000.0,"revenue_yoy_pct":-8.69,"gross_margin_pct":24.46,"operating_margin_pct":10.79,"net_income":-265000000.0,"diluted_eps":-0.48,"free_cash_flow":1097000000.0,"fcf_margin_pct":16.25,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":6791000000.0,"revenue_yoy_pct":0.61,"gross_margin_pct":24.89,"operating_margin_pct":11.74,"net_income":885000000.0,"diluted_eps":1.59,"free_cash_flow":1009000000.0,"fcf_margin_pct":14.86,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GFS/GFS_Q3_2026_Earnings_Call_20261104.md）

# Q3 2026 Earnings Call
**GLOBALFOUNDRIES Inc.** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Thank you for standing by, and welcome to the GlobalFoundries Third Quarter Fiscal Year 2026 Financial Results Conference Call. [Operator Instructions] As a reminder, today's program is being recorded.
And now I'd like to introduce your host for today's program, Eric Chow, Head of Investor Relations. Please go ahead, sir.

**Eric Chow** (Executives):
Thank you, operator. Good morning, everyone, and welcome to GlobalFoundries Third Quarter 2026 Earnings Call. On the call with me today are Tim Breen, CEO; and Sam Franklin, CFO. A short while ago, we released GF's third quarter 2026 financial results, which are available on our website at investors.gf.com, along with today's accompanying slide presentation. This call is being recorded, and a replay will be made available on our Investor Relations web page.
During this call, we will present both IFRS and non-IFRS financial measures. The most directly comparable IFRS measures and reconciliations for non-IFRS measures are made available in today's press release and accompanying slides. Please note that these financial results are unaudited and subject to change. Certain statements on today's call may be deemed to be forward-looking statements. Such statements can be identified by terms such as believe, expect, intend, anticipate and may or by the use of the future tense. You should not place undue reliance on forward-looking statements. Actual results may differ materially from these forward-looking statements, and we do not undertake any obligation to update any forward-looking statements we make today. For more information about factors that may cause actual results to differ materially from forward-looking statements, please refer to the press release we issued today as well as risks and uncertainties described in our SEC filings, including in sections under the caption Risk Factors in our annual report on Form 20-F and in any current reports on Form 6-K furnished with the SEC.
In terms of upcoming events, we will be participating in a fireside chat at the UBS Global Technology and AI Conference in Scottsdale, Arizona, on December 1.
We will begin today's call with Tim providing a summary update on the business environment and technologies, followed by Sam, who will provide details on our third quarter results and fourth quarter guidance. We will then open the call for questions with Tim and Sam. We request that you please limit your questions to one with one follow-up.
I'll now turn the call over to Tim.

**Timothy Breen** (Executives):
Thank you, Eric, and welcome, everyone, to our third quarter 2026 earnings call. GF delivered strong results in the third quarter with revenue and non-IFRS profitability metrics at the high end of our guidance ranges. We delivered record non-IFRS gross margin, which demonstrates the meaningful progress we are making to enhance the mix of our business by ramping our differentiated technologies in high-value, high-growth applications. Our communications infrastructure and data center end market saw record levels of growth, led by accelerating demand in optical networking across our silicon photonics and silicon germanium platforms. We also delivered strong growth in automotive and home and industrial IoT, reflecting broad-based secular momentum across our key markets.
Thanks to the accelerated growth across several end markets, the proportion of revenue outside of smart mobile devices was the highest level in our company's history and is driving a richer, more diversified, more resilient revenue base. Thanks to the team's excellent efforts and execution, we are ahead of plans to deliver the strategic and financial targets we set out at our Investor Day earlier in the year.
We will look back at 2026 being a pivotal year for GF. In recent weeks, we have made several significant announcements that meaningfully advance our strategy, support our financial objectives and reinforce our foundation for durable long-term growth. We are proud to have announced a significant number of new customer and investment partnerships such as our agreements with Marvell to accelerate capacity for our industry-leading high-performance SiGe, with Monolithic Power for critical power management solutions, with TSMC to establish a U.S.-based supply of silicon interposers for the CoWoS ecosystem and the landmark U.S.-Japan fab expansion plan that will transform our Malta, New York, site.
These milestones firmly position GF as a diversified holistic technology provider critical to governments and partners around the world. Let me cover these areas in more detail, beginning with our strong investment partnerships. As announced last month, the U.S.-Japan initiative provides a new and innovative model for GF to expand our critical U.S. semiconductor manufacturing capacity at accretive economic returns. This initiative will unlock substantial capacity growth, support significant future customer demand and bring the scale of our U.S. operations in Malta, New York, to mega fab level. The unique and innovative partnership structure allows GF to expand capacity faster without investing capital with an economic model that is accretive to our long-range plans. Through a robust structure of technology, construction and operations fees, cost reimbursements and EBITDA sharing, the initiative is designed to generate the profit per wafer comparable to if we had built and owned the capacity ourselves.
As another indicator of our deepening partnership with the U.S. government, GF reached an agreement with the U.S. Department of Commerce to reallocate USD 955 million of our existing CHIPS and Science Act award to accelerate investments at our Malta, New York and Burlington, Vermont, facilities. The amended award will accelerate CapEx and R&D investments in our highest value differentiated technologies that our customers demand, such as silicon photonics, silicon germanium and advanced packaging, including the first U.S.-based source of silicon interposers. In recognition of the growing role that GF is playing in the U.S. semiconductor ecosystem, a separate agreement will be entered into to issue 4% equity to the U.S. government, which provides a vehicle for the American people to share in GF's future success.
Combined with previous announcements across our Quantum, silicon photonics and advanced packaging investments, we anticipate the total equity ownership of the U.S. government to be approximately 7% when all agreements are finalized. Having attained a meaningful position in GF, our Board of Directors and our U.S. government partners do not plan on any further government equity position beyond these announced equity stakes. In summary, this landmark agreement represents a strong vote of confidence in GF and underscores our critical role in advancing U.S. semiconductor leadership.
Let me now turn to our significant and expanding opportunity in the AI data center. We see significant momentum with customers for our optical networking solutions where customers value GF's unique combination of high-performance photonic devices, advanced fiber coupling, RF integration and advanced packaging. Backed by more than a decade of investment and substantial clean room space within our modern, highly automated 300-millimeter footprint, GF can deliver differentiated performance and scale capacity rapidly as customer demand grows. Our competitive advantages are translating into strong design win momentum and robust customer demand. We are actively engaged with more than 50 silicon photonics customers, including 7 of the top 10 optical transceiver suppliers with active designs slotted to ramp in 2027 and 2028 to scale across, scale-out and scale-up networks.
In 2026, we expect to deliver $0.5 billion of revenue from silicon photonics. And on the back of the strength of customer demand, order visibility and our capacity growth plans, we now expect to exit 2027 at an annualized silicon photonics revenue run rate of approximately USD 1 billion, a full year ahead of prior expectations. To support the ramping demand for optical networking in 2028 and beyond, we plan to approximately triple our silicon photonics capacity over the course of next year, which Sam will cover in more detail.
In addition to silicon photonics, silicon germanium is another important and complementary driver of GF growth in optical networking. Our SiGe technology enables high-speed optical transceivers through transmit drivers and receipt amplifiers, key interface elements between the electrical and optical domains. Customer demand for our SiGe technology continues to increase beyond current capacity. And supported by customer prepayments, we are accelerating our capacity investments to ensure that we can meet this demand. Our recently announced multiyear strategic partnership with Marvell will help support significant SiGe capacity expansion in our Burlington fab to enable next-generation optical solutions. Together with the reallocated U.S. government funding from our prior CHIPS grant awards, this gives us additional resources and strong customer alignment to scale a highly differentiated platform, meaningfully accretive to GF's long-term margin targets.
Lastly, advanced packaging is another key enabler of our AI data center strategy. Under our 5-year, USD 2 billion manufacturing agreement with TSMC, GF will establish a U.S.-based supply of silicon interposers for the CoWoS ecosystem with volume production expected to ramp at our Malta site in the first half of 2028, and with a framework to expand the agreement over time. The economics of this arrangement are attractive for GF and the strategic benefits are clear. This agreement establishes a new multiyear revenue stream for GF with gross margins above our long-term targets and with co-investment from TSMC that will help fund the necessary capital associated with this project.
The silicon interposers are yet another way GF can serve growing AI and high-performance computing infrastructure demand. By combining GF's trusted U.S. manufacturing capabilities with a leading advanced packaging ecosystem globally, we are expanding into another essential layer of AI infrastructure and supporting the tighter integration of compute, memory and connectivity. We believe we are in the early innings of GF's AI data center opportunity, underpinned by the critical needs of our customers for higher bandwidth connectivity, tighter integration of compute and memory, greater power efficiency and secure scalable supply. The result for GF, more avenues to win greater content and value in each system and a clear path to growth and a structurally richer business mix.
Let me turn to physical AI as well as the meaningful progress we are making across IP, software and custom silicon or ISC. GF's physical AI opportunity spans a wide variety of applications across connectivity, compute, power, actuation and sensing and our IP software and custom silicon capabilities unlock even more ways for GF to win. We believe the deployment of intelligence into vehicles, factories, robots, drones, satellites, medical devices and other edge systems represents a significant and long-duration demand vector for GF. Together with the Synopsys ARC processor IP business we acquired earlier this year, MIPS expands our role into that of an holistic technology partner servicing a broader set of customers with our custom silicon platforms. MIPS recently announced 3 physical AI native reference platforms focusing on compute, AI inference and real-time control, and we are now working with several customers designing systems focused on physical AI, leveraging our expanded capabilities.
The combination of RISC-V compute and AI IP design capability and AI native platforms based on GF's broad manufacturing capabilities puts us in a unique position to accelerate share gain in this area. Just over 1 year after we initially acquired MIPS, we are very encouraged by the strong customer traction, which is now driving several platform level wins.
During the third quarter alone, we secured custom silicon design wins that totaled nearly $1 billion of lifetime revenue. These included platform wins for a radar system on chip and a RISC-V-based processor core designed for real-time control.
In addition, we secured a win with a leading provider of high-performance data center computing solutions to design their custom board management controller system-on-chip, integrating our processor technology with third-party IP. We also secured a notable aerospace and defense win to support the engine control processor for a leading global aerospace and propulsion company.
Ultimately, these wins demonstrate how GF can capture more opportunities and support our customers across the semiconductor value chain, deepen our relationships with industry partners and convert initial design engagements into concrete long-duration growth opportunities.
In summary, the multifaceted progress we demonstrated this quarter shows our strategy in action. We are scaling differentiated technologies into high-growth AI markets and driving meaningful customer value with our capabilities in IP, software and custom silicon. We are transforming GF into a more diversified, more durable and more profitable business, propelled by the defining megatrends of our time.
I'll now pass the call over to Sam for a deeper dive on third quarter 2026 financials.

**Sam Franklin** (Executives):
Thank you, Tim. For the remainder of the call, including guidance other than revenue, cash flow and net interest income, I'll reference non-IFRS metrics. The third quarter was a significant milestone for GF, not only for the continued progression in our profitability metrics, but also for the continued mix shift in our portfolio. For the first time in our history, more than 2/3 of our Q3 revenue came from outside smart mobile devices, a record for GF and further evidence of our increasingly diversified and margin-accretive mix. We delivered record non-IFRS gross margin while continuing to fund the strategic investments that will drive GF's next phase of growth. Our strategic decisions are already enhancing our earnings power, and we believe that we're only in the early innings of this evolution.
Now on to the results. We delivered third quarter revenue of $1.899 billion, up 6% sequentially and 13% year-over-year. We shipped approximately 647,000 of 300-millimeter equivalent wafers in the quarter, up 4% sequentially and 7% from the prior year period. Revenue from manufacturing services accounted for approximately 88% of total revenue. Revenue from technology services, which includes revenue from IP licensing, software, reticles, nonrecurring engineering, expedite fees and other items, accounted for approximately 12% of total revenue for the third quarter.
As we continue to invest in a broader range of capabilities for our customers, we expect technology services revenue will represent approximately 12% of total revenue in 2026, which is at the upper end of the range we indicated and with a gross margin profile that continues to be above our long-term target. Beyond 2026, we expect that the growth of revenue from technology services associated with IP licensing and software, combined with strong momentum in customer design wins and tape-outs will be important drivers of GF revenue growth and gross margin appreciation.
Let me now provide an update on our revenue and outlook by end markets. Communications infrastructure and data center represented approximately 17% of third quarter total revenue. Revenue increased 14% sequentially and 81% year-over-year, driven by robust growth in optical networking, which includes silicon photonics and silicon germanium. Not only did Q3 represent record year-over-year growth for this end market, it also marked the eighth consecutive quarter of double-digit percentage year-over-year growth for communications infrastructure and data center.
With accelerating customer demand and improved manufacturing productivity, our expectation is that revenue from communications infrastructure and data center will grow in the range of 60% to 70% in 2026. Furthermore, our design win momentum across this end market has continued to strengthen. In the third quarter, we secured design wins for both silicon photonics and SiGe and a new optical transceiver customer for hyperscaler demand. In data center power, we taped out a smart power stage gate driver on our BCD platform and secured a design win on our 650-volt GaN platform. Automotive represented approximately 19% of third quarter total revenue. Automotive revenue increased 11% sequentially and 20% year-over-year.
Consistent with our prior commentary, our expectation is that automotive revenue will grow low double-digit percentage in 2026, marking another strong year of growth for this end market, and GF continues to win with our customers to support the expansion of automotive semiconductor content. Smart mobile devices represented approximately 32% of third quarter total revenue, the lowest proportion in our history and a step forward to our long-term strategic goal to enhance the diversification of mix.
Revenue decreased 5% sequentially and 19% from the prior year period. Consistent with the commentary from our customers, we continue to expect smart mobile devices to decline by a low teens percentage year-over-year in 2026. We continue to have a skew towards the premium end of the smart mobile market, and we expect to largely track the broader demand dynamics as the market adjusts to the challenges associated with memory-related supply constraints.
The long-term demand indicators continue to be positive. In the third quarter, we secured new design wins across form factors spanning both smartphones and smart glasses. These included additional content wins in mobile power and a first-ever design win for fuel gauge ICs in premium tier handsets. Customer engagement continues to be strong for GF differentiated and high-performance RF power, audio, display and imaging capabilities to service the demand for smart and connected mobile devices.
Finally, home and industrial IoT represented approximately 20% of third quarter total revenue. Revenue increased 16% sequentially and 49% year-over-year on broad-based strength across connectivity, tracking and sensing applications. As workloads for edge AI applications continue to grow alongside the requirement for Bluetooth, wireless, cellular and power management components to perform at higher standards, we have seen strong traction with our customers in this end market for GF's highly differentiated platforms. As a result, we continue to expect home and industrial IoT to grow in the range of 10% to 15% in 2026.
Looking ahead to the future growth opportunities, the design win momentum has continued. In the third quarter, we taped out next-generation cellular IoT and Bluetooth products on our FDX platform for wireless connectivity. We're encouraged by the momentum we're seeing across the end markets we serve and believe keep us on track with the strategic diversification objectives that we set out during our Investor Day this year.
Moving now to other key financial performance metrics in the quarter. In the third quarter, we delivered gross profit of $597 million, which translates into approximately 31.4% gross margin, up 540 basis points year-over-year. Q3 gross margin achieved a company record and was at the high end of our guidance range. R&D for the quarter was $164 million and SG&A was $93 million. Total operating expenses of $257 million represented approximately 14% of total revenue and were up 9% quarter-over-quarter, reflecting recent acquisitions. We delivered operating profit of $340 million for the quarter at an operating margin of 17.9% at the high end of our guided range and up 250 basis points from the prior year period. Third quarter net interest income was $9 million and other expense was $6 million, and we incurred tax expense of $45 million in the quarter. We delivered third quarter net income of approximately $298 million, an increase of approximately $66 million from the prior year period. Diluted earnings of $0.53 per share was at the high end of the guidance range based on a fully diluted share count of approximately 558 million shares.
Let me now provide some key cash flow and balance sheet metrics. Cash flow from operations in the third quarter was $341 million. Third quarter CapEx, net of proceeds from government grants was $205 million or roughly 11% of revenue. Adjusted free cash flow for the quarter was $136 million. Free cash flow in the third quarter benefited from approximately $150 million of customer prepayments and government grants received.
At the end of the third quarter, our combined total of cash and cash equivalents and marketable securities stood approximately $3.2 billion. Our total debt was $1.1 billion, and we also have a $1.5 billion revolving credit facility, which remains undrawn. On October 9, we paid a quarterly cash dividend of $0.12 per share. On October 27, the Board of Directors approved a dividend of $0.12 per share payable on January 14, 2027, to shareholders of record as of December 22, 2026. In the third quarter, we also repurchased $100 million of our shares.
Let me now provide you with our outlook for the fourth quarter of 2026. We expect total GF revenue to be $2 billion, plus or minus $25 million. We expect gross margin to be approximately 31.5%, plus or minus 100 basis points, which at the midpoint reflects approximately 250 basis points of year-over-year expansion. Excluding share-based compensation, we expect total operating expenses to be $235 million, plus or minus $10 million. We expect operating margin to be in the range of 19.8%, plus or minus 170 basis points. At the midpoint of our guidance, we expect share-based compensation to be approximately $68 million, of which roughly $16 million is related to cost of goods sold. We expect net interest and other income for the quarter to be between negative $5 million and $1 million, and income tax expense to be between $44 million and $68 million.
Based on a fully diluted share count of approximately 575 million shares, which reflects the expected issuance of equity to the U.S. government, we expect diluted earnings per share to be $0.59, plus or minus $0.05. Subject to the timing of the closures associated with the remaining equity issuances to the U.S. government, we expect that our fully diluted share count will be approximately 600 million shares commencing 2027.
Now let me provide an update on some broader financial drivers, milestones and outlook. With respect to pricing, the third quarter saw meaningful blended ASP growth, both sequentially and year-over-year. This marked the first quarter of year-over-year blended pricing improvement since 2023 and is consistent with the commentary we provided on our last earnings call, especially as we execute the continued mix shift of our business. With respect to tax, we continue to expect a non-IFRS effective tax rate in the mid-teens percentage range for the full year 2026. Net CapEx for 2026 is expected to be approximately 15% to 20% of revenue, which remains below our long-term model, and we continue to expect free cash flow margin of approximately 10% in 2026.
Touching briefly on the CapEx outlook for the year ahead. We expect 2027 to represent a year of accelerated investment for GF. Throughout the second half of this year, our customers have substantially increased their demand for our differentiated solutions across critical technologies such as silicon photonics, silicon germanium, FDX and advanced packaging. Importantly, we have the ability to grow our capacity quickly and efficiently within our existing 4 walls manufacturing footprint, resulting in a strong return on investment for new CapEx spending. Robust demand and customer commitments form the foundation of our capacity investment principles. As these signals strengthen, we expect approximately 1/3 of our net CapEx in 2027 to be supported by customer prepayments for incremental capacity agreements. In parallel, we also expect to secure CapEx offsets from investment tax credits and government grant frameworks, including a proportion of the recently announced $955 million repurposing from our previously awarded CHIPS grants.
Against this backdrop of customer demand, prepayments and government support, we now expect net CapEx investments of approximately $4 billion into our manufacturing footprint in 2027, while continuing to deliver our free cash generation targets. These critical investments will unlock capacity constraints, accelerate future growth and continue to evolve our business into a more diversified, resilient and accretive portfolio. Our third quarter results demonstrate that GF strategy is translating into stronger financial performance. Importantly, we believe these improvements are structural.
Our revenue mix continues to shift towards differentiated high-value technologies and services, while our government and customer partnerships are enabling us to make capital-efficient investments to scale and accelerate key technologies with favorable economics. All of these drivers reinforce our confidence in the long-term financial targets we presented at our Investor Day. GF today is more diversified and better positioned to capture more value than it ever has been. In closing, I want to thank our employees around the world for their continued focus and execution. Their work made this quarter's performance possible and gives us confidence in what GF can achieve next.
With that, let's open the call to Q&A. Operator?

**Operator** (Operator):
Certainly. And our first question for today comes from the line of C.J. Muse from Cantor Fitzgerald.

**Christopher Muse** (Analysts):
I think one of the key themes from this call is you guys moving to a structurally richer business mix, particularly as I think about silicon photonics pulled in by a year. And so I'm curious, you laid out targets of exiting '27 at 35% gross margins. 40% exiting '28. You're raising pricing starting Jan 1. How, I guess, is that portfolio of changes impacting your thinking about your gross margin trajectory into '27 and '28?

**Sam Franklin** (Executives):
Yes. C.J., I'll take that one and then Tim probably overlay some of the strategic dynamics as well. Look, we're really pleased with the margin trajectory. And I think you've seen from us consistently this year, and a near on 500 basis points of year-over-year margin growth. So if you go back to what we said we were going to do at the Investor Day back in May, we feel like we're doing exactly that mix has been a key component of it. We've also seen some gradual pickup in utilization as well through this year. But fundamentally, it's been driven by those strategic decisions that we've taken over the last couple of years. And technology services as a percentage of revenue clearly falls through as a richer mix and margin driver as well. That's continued to grow during the course of this year.
So, On balance, we feel like we're actually hitting that target, and we're well on track to the target that we set out in May. Remember, at the start of this year, we said we wanted to exit the fourth quarter of 2026 with a 30% gross margin handle. We were bumping up on that in our 2Q results. Our 3Q results, obviously, we've gone through that target. We're quite pleased with even where the guide is for fourth quarter. It shows about 1.5 points of growth relative to that original target we have.
So, very much feel at this point that we are on track to those gross margin goals that we set out earlier on this year. Obviously, there's still some way to bridge from, call it, the 31.4% in 3Q up to the 40% that we want to exit the fourth quarter of 2028 with. But that mix dynamic and where we're continuing to invest in those corridors, where we're seeing very strong demand signals from customers is continuing to push us in the right direction as it relates to that margin accretion. So, no change to the goals that we laid out just a few months ago, but maybe I'll pass it to Tim for some of the other structural and strategic dynamics.

**Timothy Breen** (Executives):
Yes. Thank you, Sam. C.J., I think the right way to think about this is we're delivering what we said earlier this year, right? We're winning in those secular growth markets, and we're winning with leading customers who, in many cases, are new to GF. And so the announcements we made just this quarter, customers like MPS, customers like TSMC, expanded business with Marvell. By the way, there are many others that supported our several announcements over the quarter, just tell you kind of the breadth of engagement we have. And that's giving us a lot of confidence to bring those technologies to market, accelerate those ramps, accelerate the capacity investments and obviously unlock even more growth through the partnership we struck with the U.S. and Japan. So look, it's been a great period of accelerating our business model and look, we're very confident in the trajectory ahead.

**Christopher Muse** (Analysts):
I guess as a follow-up question, could you speak to, I guess, your early look to Q1 seasonality? If I look at it, the implied SMD, you're talking down 22% year-on-year for Q4 and down 40% from your prior peak. And at the same time, CID is tracking 80% implied in Q4. So would love to hear how you're thinking about the March quarter.

**Sam Franklin** (Executives):
Yes. Happy to give you a little bit of color, C.J. Obviously, just mindful that we're going to guide one quarter at a time. But the way you've characterized it is the right way. And we think that relative to where we said earlier on this year, we're broadly on track with several of those end markets, right? We expected that mobile would be down in the low teens percentage, no change to that for the full year '26. We expected that IoT would be in that 10% to 15% range full year. Again, no change in automotive, low double-digit percentage growth. That's been a consistent theme for us.
So, really, the step change has been the accelerated growth that we're seeing in comms infrastructure and data center and the way you thought about it for the fourth quarter is the right way. Looking out to 2027, obviously, we'll put more color on that when we get to the next call. But just going back to what we said as part of our Investor Day in May, look, I think the general trends are very constructive as it relates to automotive. IoT, remember in that space, we said low double-digit growth is our long-term goal for automotive and sort of mid-teens for IoT. Comms and data center is where we think that there's very strong momentum to continue growing. The target that we put out previously in our long-term model was 30-plus percentage points. You can infer from where we've reported in Q3 and the direction of travel for Q4 that we're seeing that continued momentum in that space.
So, I'd say that, that is probably a tailwind going into 2027. And then look, mobile, we've been consistent on the commentary there and largely tracking where we see the rest of the market. So, I don't think any surprises on that front. But hopefully, that gives you a little bit of color as we're thinking about it for the full year and obviously, happy to give you more color on Q1 when we get to the next quarter.

**Operator** (Operator):
And our next question comes from the line of Sahej Singh from Stifel.

**Sahej Singh** (Analysts):
Congrats, by the way, on the partnerships you've lined up this quarter. I think they say a lot about where Global sits in the AI supply chain. Tim, I guess, thanks for the color that customer prepayments will support roughly 1/3 of 2027 net CapEx, I think I heard. And since May, you've sort of talked about customers discussing advanced payments to secure FDX, SiPho and silicon germanium capacity. And you've had CPO tape-outs in the first quarter and a scale tape-out in the second. So, I guess, even directionally, could you give some color into how much of your 2027, 2028 SiPho and SiGe capacity is now under signed commitments? And are those agreements even reaching into 2029 as NPO and CPO potentially come in?

**Timothy Breen** (Executives):
Yes. No, thank you, Sahej. So, I think the picture is as follows. The acceleration of optical communication is very clear. And I think we're still at the very early innings of that as you see just optical links replacing copper in all aspects of the data center, just demand is truly skyrocketing. And so, we're having those discussions with our customers and lining up the supply they need. We are absolutely booked out through '27, increasingly booked out through '28. And the question for us is how fast we can add more capacity to meet their requirements in '28. And many of them are seeking capacity assurance through '29 and even some cases, beyond. And I think in every single case, they're willing to put their balance sheet to work to support us in those investments as well.
So, it's a very constructive environment in terms of visibility, in terms of demand. And it's really now down to us in terms of execution, right, installing tools, driving productivity. And that's really what you're seeing accelerate our own trajectory even within '26, we're doing better than we expected based on our acceleration of investments and the ability to ramp those tools to production quickly. And that's true across all those corridors you mentioned. And I'd say increasing that will also be true in advanced packaging with some of the interposer work we've also announced.

**Sahej Singh** (Analysts):
Yes. I guess interposers work is topical as well. And Sam, thank you for the color on the blended ASPs. I guess I'd like to build on CJ's question on the margin drivers, particularly to help us price -- frame pricing specifically. At the Investor Day, you were pretty clear that the bridge to the 40% exiting '28 doesn't embed significant price increases from supply and demand.
So, now with ASPs up year-over-year for the first time since 2023, should we think of pricing as additive to that to the 40%, I mean? And then on the TSMC interposers agreement, -- thanks for the color that margins sit above your long-term targets. And at roughly $400 million a year or about 4% of revenue against 28 consensus. Is it fair to think of that as adding on the magnitude of 50 basis points to corporate gross margins at run rate alongside the 100 to 200 basis points from the U.S.-Japan program?

**Sam Franklin** (Executives):
A little bit to unpack there. So, maybe I'll start with the pricing point, and then we can talk more broadly around margins. And look, it's encouraging what we've seen in the third quarter, but also not surprising. We gave you color on this in prior quarterly earnings updates where we said we expected the second half of 2026 to be the point where we lapped some of those pricing headwinds, if you like, that we've seen over the course of the last few years, and that was certainly the case in the third quarter, quarter-over-quarter, blended ASPs were up about 2.5%. And for the year-over-year period, they were up almost 5%.
So, we feel that across all of the end markets that we operate in now that pricing is a much more constructive dynamic. But obviously, mix is a key component of that as well. We are servicing a richer mix of demand within the end market portfolio that we have. And so, looking out to 2027, look, I'd say this combination of richer mix and blended ASP mix improvements points us towards probably about a 10% uplift in blended ASP mix for 2027, which I think is consistent more broadly with the market and consistent with what we said we were going to do as it relates to pricing actions as well that we took towards the end of the first half of 2026. So naturally, that serves as a tailwind. But I would say, in the same way that we -- when we've seen pricing going the other way in prior years, pricing is only one component from the margin perspective. And it's actually a far less impactful component than even the broader mix dynamics are concerned, the utilization, the depreciation, the productivity within our manufacturing footprint.
So, like I said to C.J., we're not looking to change the targets that we put out there from the perspective of our gross margin accretion over the course of the next couple of years. But you can infer that these decisions, these announcements that we've made over the course of the last couple of months really give us more clarity, more certainty on our ability to hit those targets. So, I'd say no major change on that front, but we're encouraged by the momentum. And naturally, as you would expect, the announcement for the silicon interposers with TSMC, when that starts to ramp in the first half of 2028, we would expect that to be margin accretive as well to our overall objective. So, the change to the targets, greater visibility, and we think a high degree of momentum to get to those targets.

**Operator** (Operator):
And our next question comes from the line of Jim Schneider from Goldman Sachs.

**James Schneider** (Analysts):
Maybe just sort of building on the theme that's been asked for the last few questions. I want to maybe clarify more tactically where you see the various moving parts of utilization, pricing and mix going in the first half of '27. It seems like, if anything, mix is improving, pricing, as you said, is getting better. And then I guess the question is about utilization. And so like do you think you're going to be able to maintain sort of at least flattish utilization? Because it seems like given everything that's going on with the smartphone market and its relatively dilutive margins, that mix or gross margins could actually at least stay flat in the first half, if not go up?

**Sam Franklin** (Executives):
Happy to take that one, Jim. And look, I think I'll echo what I said around some of the structural drivers that we see across those end markets. And naturally, from a mobile point of view, we think we largely track that market. But the offset that we're seeing in terms of mix benefits from the other end markets are a tailwind from our point of view going into next year. I will say that naturally, there's a degree of seasonality from the fourth quarter into the first quarter. You can see that in prior years. But given some of the structural shifts that we're seeing within those end markets, we do think that there should be a slightly less pronounced impact from a seasonality point of view, fourth quarter into the first quarter. And obviously, I'll give more color around that when we get to the next call. But hopefully, that helps give you a little bit of insight from a tactical point of view.
And then, look, as it relates to 2027 more broadly and into 2028, like Tim said and like I said, we think we're increasing our visibility on getting to those objectives that we set out from a margin point of view and really have our eyes set on getting to that 40% gross margin. We think we're making good progress towards that.

**Timothy Breen** (Executives):
Maybe, Jim, one comment I'll add is about just thinking about utilization and it's also about flexibility. We spent a lot of time over the last 3 years really investing in our manufacturing footprint to make it as flexible as possible so that we can respond when one market is weaker and one market is stronger, we can respond and use that capacity across where there's growth. Obviously, there are always limitations to that, but that's definitely a factor that's helping us overall improve utilization this year and picking up into next year as well.

**James Schneider** (Analysts):
That's fine. And then maybe just to clarify, on the smart mobile device market, clearly, there's been some correction there for all the reasons that we understand. But I just wanted to clarify, your outlook is unchanged on the full year. So can you maybe characterize where you think the downstream inventory levels stand with respect to component inventories in smart mobile devices and just kind of making sure that you're sort of aligned with inventory levels you can go in terms of unit demand tracking from there?

**Timothy Breen** (Executives):
Yes. Thanks, Jim. I think the broader topic on SMD is just how the market is quite bifurcated. I think the high end is not that bad, right, all things considered. Obviously, you can weather the memory impacts much more. The low end is much, much worse. Our exposure is much more to the high end of the market. And I'd even say in this current environment, some of the capacity in the industry more broadly is being taken up by other end markets, which actually in turn leads mobile customers to come back to us and look for more supply to make sure they have enough to build what they need to build. So, I'd say, overall, we're not seeing any kind of concerns from an inventory point of view. Like I said, overall, we're going to track the market going into 2027, but the situation is perhaps not as bad as people might think.

**Operator** (Operator):
And our next question comes from the line of Mehdi Hosseini from Susquehanna Financial.

**Mehdi Hosseini** (Analysts):
I want to dive into communication infrastructure. And Tim, can you please update us on how you see the mix between SiPho and SiGe changing into 2027, 2028? And I ask the question in this context because last time, you highlighted that in '26, SiGe mix is higher than SiPho. And again, I want to see how that mix is changing over the next couple of years? And I do have a follow-up.

**Timothy Breen** (Executives):
No. Thanks, Mehdi. I think the story I'd say is very simple. The optical transition is pulling both of them very strongly. And I'd say SiGe is getting a particular pickup because of the transition to 200 gig per lane speeds, and I think that's going to continue going forward. We're sold out effectively of both. We're adding capacity for both. We have an excellent road map for both, right? And I think our strategy will continue to operate on that basis. I think both are going to see very strong growth going into '27 and beyond. And like I said, customers are now willing to put their balance sheets to work to help us invest and add capacity again in both those end markets are very strong.
And you didn't ask it, but I'll answer it anyway. The transition to technologies like NPO are going to accelerate that story even further because that requires even higher performance photonics, but also extra SiGe content as well. So those are tailwinds for the business going forward.

**Mehdi Hosseini** (Analysts):
I was actually going to follow up on NPO, which is kind of a black box. In my opinion, NPO is more about integration, heterogeneous integration, you have PIC and EIC, which is quite different than discrete components associated with a pluggable transceiver. And my follow-up question for you is, how do you see GlobalFoundries' content changing from pluggable to NPO transceivers?

**Timothy Breen** (Executives):
Yes. It's a great question. I'd say overall, the transition from pluggables to NPO and to CPO, by the way, which we still believe will continue to happen. All of that creates a growing content opportunity for us because obviously, as you go forward in high performance, the PIC has to do more, right, in different applications. You have more sticky content in each of those applications. And then as you get closer to the XPU, you have some of the packaging components, be that fiber attach, die-to-wafer bonding and so on also play an important role. So I'd say, the opportunity increases as you get closer to the ultimate chip. And therefore, our investments in R&D, building the scale platform and others have really begun to pay off very well in terms of customer interest and traction for long-term road map in those areas.

**Operator** (Operator):
And our next question comes from the line of Harlan Sur from JPMorgan.

**Harlan Sur** (Analysts):
Great job on the quarterly execution. June quarter utilizations were in the high 80% range. Did that increase in the September quarter maybe towards the 90% range? That would imply -- the team still has another 8 to 10 percentage points of utilization increases ahead. If that's the case, I mean, by my calculations, you still have roughly about 400 basis points of gross margin improvement in front of you just from utilizations, right? How much of that potentially gets unlocked in 2027 as manufacturing activity and utilizations continue to increase?

**Sam Franklin** (Executives):
Harlan, maybe just to pick up on that, you're right, utilization in the high 80s in the second quarter. Utilization in the third quarter was also in the high 80s. One of the reasons for that is that we've been investing CapEx through this year. We've been adding to the capacity, which in effect adds to that denominator for the purposes of calculating utilization. So you're right, we do still see utilization upside as an opportunity from a margin point of view. But as you heard on the call, we're going to be continuing to invest in that capacity and really sort of grow the overall corridors where we see strong demand to be able to expand margins from a mix point of view, but also from a utilization point of view into 2027. So, at this point, headwinds to certainly grow into from a utilization point of view. And we think we're going to keep growing that denominator as we invest CapEx dollars to grow our capacity.

**Harlan Sur** (Analysts):
I appreciate that. And then for Tim, on the Photonics front, lasers are also in tight supply, right? In high-quality lasers, very, very tight supply situation. I mean, Marvell is paying a healthy premium to acquire Lumentum, right partly for their indium phosphide laser portfolio. The GF team has done a very good job in compound semiconductors, right? Silicon germanium, you talked about quite a bit, targeted for high-quality TIAs and drivers is a good example. Indium phosphide lasers will also add to your SiPho capabilities and portfolio. Is the team considering adding indium phosphide manufacturing to your technology offerings?

**Timothy Breen** (Executives):
No, it's a great question, Harlan. You're definitely seeing a strong interest in that part of the value chain expressed by the transaction you mentioned, but also other investments that we're hearing about in the industry. We're focusing on integration of indium phosphide into our technologies, right? And I think part of the road map is about having integrated lasers, integrated SOAs for future optical applications. By the way, just like we're also investing in novel materials for future enhanced modulation to go to 400 gig per lane. So part of our road map we can invest at the silicon level. Discrete laser manufacturing, not on our current road map, but obviously, we'll continue to be open to opportunities going forward.

**Operator** (Operator):
And our next question comes from the line of Joseph Moore from Morgan Stanley.

**Joseph Moore** (Analysts):
Great. In the last cycle, it seemed like a lot of the focus on wafer securing was coming from automotive, and you had big automotive OEM deals that were working with GlobalFoundries. And obviously, we had a shortage of cars that was driven by all of this. And as I look at things now, I mean, your automotive business is doing fine. But I worry about looking at all the capacity going to interposers and silicon photonics and AI. These fabs are getting full. Like do you think we could be looking at another capacity crunch in the automotive space? And I guess, how are you thinking about that? And how are your customers thinking about that? Are you seeing people start to focus on those supply chains in the way that they did a couple of years ago?

**Timothy Breen** (Executives):
Yes. Thank you, Joe. It doesn't get as much of the limelight, but I think the sector continues to be advancing forward in terms of the automotive sector, that is in terms of its thinking on supply security. We have a lot of conversations with automotive players, not just for like the next 12 months, but the next kind of 3 to 5 years. And so, a lot of them, they're very keen also to see that geographic supply diversification as well. And that plays particularly well for us given our U.S. footprint and our European footprint.
So, I would expect continuous investments, more engagement, more direct business opportunities in auto as well. Many of them are doing that, both OEMs and Tier 1s. And that also plays, by the way, into our custom business where a part of what we've announced in our prepared remarks was progress in things like custom radar, which is another area we're developing further within the platform. So, I'd say automotive continues to be in line with what we talked about at our Investor Day, strong consistent growth opportunity and where GF is really very well positioned to play across multiple technologies and with multiple end customers.

**Sam Franklin** (Executives):
And Joe, maybe just more broadly, as you think about some of the CapEx that we've guided to today for 2027, as you'd expect, a lot of that is going into both the silicon photonics, SiGe, data center applications, but we're not leaving our other end markets behind and automotive is a key component of that. So, as we think about driving towards that low double-digit percentage growth, investing into some of our automotive capacity corridors across the footprint will also feature within that overall $4 billion net CapEx that we indicated for next year.

**Joseph Moore** (Analysts):
Yes. That's helpful. And in terms of the OEMs, you mentioned that those relationships are direct. I mean I feel like that's what's been unique about the last few years is that you're getting automotive OEMs showing awareness of foundry supply chains and things. Is it still -- I guess, are they emphasizing it enough, do you think? And is it still very much a focus on the geographic sourcing? Is that coming from the Tier 1s? Or is that coming from the OEMs?

**Timothy Breen** (Executives):
I think it's both. And I think part of it also is increased differentiation. I mean if you look at today's car, the content growth is just tremendously increased over the last years, and all of them have road maps to do more, right, as you move to different architectures. Some of that's linked to electrification, but some of it is just linked to performance and feature sets of the cars. I think it's also being led by the more, kind of, silicon native OEMs. By the way, I would cite obviously Tesla, but I would also cite the Chinese players that are increasingly setting the tone globally for what the automotive industry needs to do in terms of performance. So, I just think you've got a much more aware end market, and that creates a lot of opportunities for players like us.

**Operator** (Operator):
And our next question comes from the line of Krish Sankar from TD Cowen.

**Sreekrishnan Sankarnarayanan** (Analysts):
I've two of them. First one, Tim or Sam, can you give us an update on the silicon photonics competitor landscape? Obviously, there is TSMC, Tower, STMicro, now UMC. And also along the same path, I think the Marvell Lumentum merger highlighted one of the bear aspects, which people worry that you could be into optical transceiver overbuild in 2028. I'm just, kind of, curious if you have any thoughts around that? And I had a quick follow-up.

**Timothy Breen** (Executives):
Yes. No, great question, Krish. Look, overall, it's great to see other players believe in the same thing. We believe that the optical transition is just getting started, and that's why you're obviously seeing people enter the space who previously weren't very engaged in photonics. We've been doing this for 10 years. We've got a very strong technology road map and positioning today. We've also got a lot of investments beyond the PIC level into the packaging side, which I think will play more and more into those new applications we talked about earlier like NPO and CPO. But I think perhaps even more important right now is we've got the scalable fab footprint to invest and grow with our customers without adding fab space for it, particularly for Photonics and SiGe where they need that capacity rapidly. And that's one thing they're betting on in terms of coming to GF for more of their capacity.
So, I think we feel very confident in our competitive position within that landscape. Look, I view the recent announcement, the Marvell Lumentum announcement, again, as a really strong endorsement of that optical transition, both are betting a bit, if you like, their future on optical, which I think is reassuring. Both, by the way, are our close partners with GF have been public about that as well. So, we think this is a great opportunity for all of us to do more to innovate faster and to grow the business. So, I think it's a tailwind.

**Sreekrishnan Sankarnarayanan** (Analysts):
Great. And then a quick follow-up on the TSMC CoWoS interposers agreement. It's like a $2 billion manufacturing agreement. Is any of this flowing through CapEx next year? And will the wafer supply there be dedicated to TSM for the first 5 years? Or do you have flexibility over that?

**Timothy Breen** (Executives):
Yes. So it's part of the CapEx that Sam has talked about. So definitely, that's included within the $4 billion number that we shared. Look, our strategy in interposers is a critical technology for all forms of high-performance compute where you're integrating multiple die with HBM and so on. So, we've had a road map for some time in that. The TSMC agreement stands on its own, and that's accretive in its own right. But we're also engaging with a number of other customers for future interposer requirements. And these are getting increasingly sophisticated with integration of deep trench capacitors and so on. So, I think it's actually a very interesting area that we're spending R&D money and efforts to actually build more for the future because it fills our sweet spot in terms of technology mix.

**Operator** (Operator):
And our next question comes from the line of Atif Malik from Citi.

**Atif Malik** (Analysts):
You guys have been busy with the partnership announcements with TSMC, Marvell, Monolithic Power. To what extent are these partnerships incremental to the long-term model shared at the Investor Day?

**Timothy Breen** (Executives):
I think Sam you've commented on that a bit earlier. The way I think about it, Atif, is that we set out early 6 months ago a set of strategic goals, which I think are both appropriate for the business and very much strategically aligned with where we have a right to win. And these are evidence points that we are winning in those directions with those customers. So too early to update the numbers of our strategic goals. But as Sam said, all of these give us increased confidence that we're on the right track to deliver and exceed those goals over time.

**Atif Malik** (Analysts):
Great. And then, Sam, what is the satellite communications exposure within CID? And what's the gross margin profile?

**Sam Franklin** (Executives):
Look, we don't break out the individual components. I will say that in 2025, we gave a little bit of color around SATCOM. We delivered about $100 million of revenue within that component of the end market from a relative standing start in the prior year. You've seen publicly, we've made some announcements that associate ourselves with some of those key players within the satellite communications market more broadly. You've only got to look at low earth orbit satellite launches and the continued momentum within that end market to see that it's an important growth vector within comms and data center for us. And look, more broadly, this is a technology that we're servicing that demand, which is accretive to the long-term goals that we've set out.

**Timothy Breen** (Executives):
Maybe just to add on my side. I mean I think one of the reasons we're seeing strong long-term momentum in technologies like SiGe beyond the data center is actually things like satellite communications, right? When you want to launch satellite 300 miles in space and have a high-performance, high-bandwidth solution, bringing that bandwidth back to us, you need high-performance RF technologies. We've been doing that for a very long time, and SiGe is getting also traction from those areas as well. So, very encouraging.

**Operator** (Operator):
And our final question for today comes from the line of Chris Caso from Wolfe Research.

**Christopher Caso** (Analysts):
My first question is with regard to the CapEx. And the $4 billion number you mentioned, it's a big number relative to what you guys have spent in the past. So, a few questions on that. One is if you could discuss given some of the prepayments and credits in that, how much of that is cash out the door from GlobalFoundries that would affect your cash flow for next year, just kind of separating out what's supported by others and what you're putting out yourself? And then, in terms of when that turns into revenue and kind of the timing of that? And I guess what I'd really like you to answer, which you probably won't, is how much revenue gets generated by $4 billion CapEx, but I'll settle for the when.

**Sam Franklin** (Executives):
Yes, Chris, I think that we've been relatively underinvesting from a CapEx point of view over the last, call it, 3 years. If you look at the aggregate over the last 3 years, it's only been a little north of 10% of revenue versus what we said previously was targeting a 20% net CapEx to revenue and what we reiterated earlier this year. So, the principal reason for that is the foundation of our investment decisions into capacity is demand. And we've seen a step change function in that demand outlook as we go through this year. It's the technologies across photonics, FDX, advanced packaging, SiGe, more recently, what we announced with TSMC on interposers. So, this has been the single biggest change in terms of how we think about that investment into the footprint.
Now our customers recognize that as well. And actually, to Tim's earlier comments, they've been very, very constructive conversations in terms of the prepayment capacity reservation for incremental capacity discussions that we've been having. We expect those largely to close in, call it, the fourth quarter and into early 2027 as well. And so that $4 billion net number that I gave you, obviously, we don't net customer prepayments from that in terms of how we calculate net CapEx. So, think of that as $4 billion net CapEx for GF. But within that $4 billion, we expect that we'll get about, call it, 1/3 of that supported by customer prepayments. You won't see that flow through as the net CapEx, but you will effectively see it flow through towards our free cash flow. And so that's why we feel good about still remaining the targets around our free cash flow margin for 2027.
And then the other dynamic, as you said, is around government grants and broader support framework. If I take the ITC as an example, that's now 35%. Now, we don't get all of that 35% in year. In fact, some of what we'll get as a net to CapEx next year will be from ITC that was accrued in, call it, the 2025 time frame. We will, however, get as an offset to CapEx next year, the government grants that we've announced during the course of this year. Some of that is in relation to quantum computing. We've also got the $955 million repurposing from the original CHIPS office grant. About 80% of that $955 million we expect will allocate towards CapEx. Not all of that will be allocated in 2027 as an offset, but we'll probably get the majority of that coming through in 2027 as well. So, all points towards good indicators from a free cash point of view.
And then look, the way we think about the ROI is really a function of payback. And when you take that combination of the government grants, the ITC, the offset to our overall CapEx burden, we see strong paybacks inside a sort of 2-year time horizon for most of those technologies that we outlined. So, it forms an important part of our investment decision-making. And given the margin profile and the mix associated with these corridors, we see a strong ROI and a relatively quick ramp to demand and revenue. Obviously, it's really a function of how quickly you can get those tools installed, qualified and ramped. But the beauty of our expansion footprint is that we can do it within our existing 4 walls. So, we're not reliant like some others are around building incremental capacity to do it. We can do it within our existing 4 walls. So, that accelerates the time to revenue as well.

**Timothy Breen** (Executives):
And maybe I'll just add. I mean, the way we've been thinking about this is it's a unique moment for us to accelerate our business with the participation of our customers, with the participation of government, maintaining a very strong balance sheet, maintaining our free cash flow generation objectives. It's the right way to navigate the current situation that we're in.

**Operator** (Operator):
This does conclude the question-and-answer session of today's program. I'd like to hand the program back to Eric Chow for any further remarks.

**Eric Chow** (Executives):
Thank you very much for joining today. We look forward to seeing you at the UBS Conference on December 1. Thanks again.

**Operator** (Operator):
Thank you, ladies and gentlemen, for your participation in today's conference. This does conclude the program. You may now disconnect. Good day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GFS_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜guidance：Q3 營收財測 18.85 億美元±2,500 萬（原話："We expect total GF revenue to be $1.885 billion, plus or"）
- 2026-08-05｜CFO｜guidance：Q3 毛利率財測約 30.5%±100bp（原話："We expect gross margin to be approximately 30.5%, plus or"）
- 2026-08-05｜CFO｜guidance：Q3 EPS 財測 0.51±0.05（原話："we expect diluted earnings per share for the third quarter"）
- 2026-08-05｜CFO｜guidance：CID 全年成長預期由高 30% 上調至 50–60%（原話："we now expect to achieve full year 2026 revenue growth in"）
- 2026-08-05｜CEO｜guidance：矽光子 2026 營收預期至少翻倍（原話："we now expect our silicon photonics revenue as reported"）
- 2026-08-05｜CFO｜guidance：智慧行動裝置全年預期衰退低十位數百分比，原因為記憶體價格與短缺（原話："we currently expect smart mobile devices to decline by a"）
- 2026-08-05｜CFO｜guidance：IoT 全年成長預期由中個位數上調至 10–15%（原話："we expect our revenue for the home and industrial IoT end"）
- 2026-08-05｜CFO｜guidance：車用全年仍預期低雙位數成長，下半年（Q4）權重較高（原話："we continue to expect low double-digit percentage revenue"）
- 2026-08-05｜CFO｜guidance：技術服務營收全年貢獻上調至 1–1.2 億美元（原 6000 萬–1 億）（原話："we expect revenue contribution of approximately $100"）
- 2026-08-05｜CFO｜guidance：全年自由現金流率維持約 10%（原話："we continue to expect an adjusted free cash flow margin of"）
- 2026-08-05｜CFO｜guidance：下半年每季營運費用與 Q3 財測一致（原話："we now expect quarterly operating expenses in the second"）
- 2026-08-05｜CFO｜guidance：全年有效稅率中段十幾%（原話："we expect an effective tax rate in the mid-teens percentage"）
- 2026-08-05｜CFO｜margin：Q2 毛利率 29.9%，年增 470bp（原話："approximately 29.9% gross margin, above the high end of the"）
- 2026-08-05｜CFO｜margin：毛利率全年預期由年底 30% 目標改為全年約 30%（原話："we should be at about 30 points of gross margin for the"）
- 2026-08-05｜CFO｜margin：營收年增約 1 億美元對應毛利約增 1 億美元（落差口徑）（原話："about $100 million of revenue growth. Look at that adjusted"）
- 2026-08-05｜CFO｜margin：技術服務營收年增不到 4,000 萬，貢獻約 1 個百分點毛利率（原話："You take our technology services revenue up a little under"）
- 2026-08-05｜CFO｜margin：Q2 稼動率高 80%，仍有約 10 個百分點可成長空間（原話："we've still got about 10 points of utilization to be able"）
- 2026-08-05｜CFO｜margin：產品組合為毛利率單一最大驅動，仍處早期（原話："mix point, CJ, because it remains the single biggest driver."）
- 2026-08-05｜CFO｜margin：去年同期含 liquidated damages 一次性效益（原話："We had things like liquidated damages in early 2025, which"）
- 2026-08-05｜CFO｜margin：Q2 營業利益率 16.7%、營運費用 2.36 億（季增 16%）（原話："Total operating expenses of $236 million were up 16%"）
- 2026-08-05｜CFO｜commitment：2028 年毛利率退出率目標 40%（原話："get towards that 40% exit run rate that we indicated in the"）
- 2026-08-05｜CFO｜commitment：長期模型 CID 成長 30%+ 維持不變（原話："I would still stand by our long-term model that"）
- 2026-08-05｜CFO｜commitment：股東回饋目標：追蹤 12 個月調整後自由現金流之最多 50%（原話："our objective is to return up to 50% of trailing 12-month"）
- 2026-08-05｜CFO｜capital_allocation：首次季度現金股利 0.12 美元已發放，並宣布下一季同額股利（原話："we paid GF's first-ever quarterly cash dividend of $0.12"）
- 2026-08-05｜CFO｜capital_allocation：買回授權剩約 1 億美元，部署彈性（原話："approximately $100 million remains under the share"）
- 2026-08-05｜CFO｜capital_allocation：Q2 淨資本支出 4.08 億（約 23% 營收），自由現金流 −300 萬（原話："Adjusted free cash flow for the quarter was negative $3"）
- 2026-08-05｜CFO｜capital_allocation：全年 CapEx 預期落在 15–20% 區間的高端（原話："my expectation is that we'll be up to the higher end of"）
- 2026-08-05｜CFO｜capital_allocation：現金及有價證券約 33 億、負債 11 億、10 億循環額度未動用（原話："approximately $3.3 billion. Our total debt was $1.1 billion"）
- 2026-08-05｜CEO｜capital_allocation：7 月完成 Photon Technologies IVR 團隊 acquihire；6 月完成 Synopsys ARC 收購（原話："we completed our previously announced acquisition of"）
- 2026-08-05｜CFO｜product：Q2 CID 營收年增 62%、季增 20%（原話："Revenue increased 20% sequentially and 62% year-over-year."）
- 2026-08-05｜CEO｜product：SiGe 2027 年全年超額認購，擴充佛蒙特產能（原話："Demand for SiGe remains strong, and we are oversubscribed"）
- 2026-08-05｜CEO｜product：SiGe 業務目前大於矽光子業務（原話："our SiGe business is actually larger than our silicon"）
- 2026-08-05｜CEO｜product：矽光子 SCALE 平台 7 個進行中合作；Q2 tape-out 一個、Q3 預計再一個（原話："We currently have 7 active engagements with leading"）
- 2026-08-05｜CEO｜product：NPO 2027 起量、CPO 2028 起量，說法與前幾季一致（原話："We still maintain the view that '27 we will see the"）
- 2026-08-05｜CEO｜product：現有廠區內矽光子產能可擴 10 倍（原話："we could 10x our photonics capacity within our current 4"）
- 2026-08-05｜CEO｜product：矽光子成長目標（2028–2030）進度符合並可能超前（原話："very much on track and potentially ahead of those targets"）
- 2026-08-05｜CEO｜product：量子：預期 3.75 億美元商務部補助；1–3 年營收主要來自工程服務，製造服務營收年底前後才放量（原話："we expect to generate quantum-related revenue largely"）
- 2026-08-05｜CEO｜product：量子視為長期『買權』，放量時點太早無法判斷（原話："Think of it more medium term as a kind of call option on"）
- 2026-08-05｜CEO｜product：矽光子取得美國商務部 3 億美元意向書補助（原話："entered into a letter of intent with the U.S. Department of"）
- 2026-08-05｜CFO｜product：MIPS 與 ARC 收購貢獻營收首日起、營運費用上升預期大致被增量營收覆蓋（原話："largely be covered by that incremental revenue we see"）
- 2026-08-05｜CEO｜customer：矽光子客戶逾 40 家，管理層稱無客戶集中疑慮（原話："we have more than 40 customers today in SiPho"）
- 2026-08-05｜CEO｜customer：與前五大光收發模組廠中 4 家有接洽（原話："we are actively engaged with 4 of the top 5 optical"）
- 2026-08-05｜CFO｜customer：IoT 上調部分來自行動客戶將需求轉入 IoT（原話："some of those customers within mobile have actually"）
- 2026-08-05｜CFO｜customer：首次取得 MediaTek PMIC 設計案（原話："This marked GF's first-ever power management integrated"）
- 2026-08-05｜CEO｜customer：Q2 新增 7 個光網路設計案（原話："we secured 7 new"）
- 2026-08-05｜CFO｜customer：Bosch ADAS 雷達於 FDX 平台 tape-out（原話："we also taped out an ADAS radar built on our FDX"）
- 2026-08-05｜CEO｜competition：面對矽光子競爭者變積極，管理層視競爭為需求佐證（原話："the fact that there's competition is a sign that there's"）
- 2026-08-05｜CEO｜competition：客戶多源採購風險與地緣政治考量，客戶表示要確保更多供給（原話："customers are also coming to us and saying, I don't have"）
- 2026-08-05｜CEO｜competition：管理層稱無需新建晶圓廠即可擴產，對比同業新建廠（原話："We don't need to build other fabs and some of our other"）
- 2026-08-05｜CFO｜risk：手機預測因記憶體價格與短缺而下修（原話："principally due to the continued impact from memory"）
- 2026-08-05｜CFO｜risk：車用 Q2 衰退 13% 季減、10% 年減，歸因客戶出貨時點（原話："principally driven by customer-led"）
- 2026-08-05｜CFO｜risk：定價調整預期自 2027 年起反映於營收（原話："we expect the pricing adjustments to be reflected in"）
- 2026-08-05｜CFO｜risk：R&D 占營收比重預期上升（原話："we believe that R&D will rise as a percentage of revenue"）
- 2026-08-05｜CEO｜risk：管理層稱產能有限：CID 成長受限於製造生產力與擴產速度（原話："the question is more about the rate and pace of"）

### GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20260310.md
- 2026-03-10｜Michael Hogan｜guidance：矽光子營收 2025 年翻倍、2026 年再近乎翻倍（原話："revenue doubled in 2025 is set to nearly double again in"）
- 2026-03-10｜Michael Hogan｜guidance：矽光子 2028 年底年化營收達 10 億美元以上（原話："a clear line of sight to a $1 billion-plus run rate"）
- 2026-03-10｜Michael Hogan｜commitment：10 億美元年化目標有實際營收客戶支撐、稱產能超額認購（原話："is actually supported by real revenue customers"）
- 2026-03-10｜Michael Hogan｜margin：目標營收口徑：2028 年約 1/3 來自 CPO，其餘為可插拔（原話："we model about maybe 1/3 of that"）
- 2026-03-10｜Michael Hogan｜guidance：CPO 若較慢，目標不變、改出更多可插拔（原話："We'll just ship more pluggables as CPO catches up."）
- 2026-03-10｜Michael Hogan｜risk：管理層承認 CPO 放量時程可能較晚（原話："if CPO takes a little longer, we still stick by that"）
- 2026-03-10｜Michael Hogan｜guidance：2030 年 GF 通訊基建與資料中心可服務市場約 110 億美元（原話："than doubles to approximately $11 billion."）
- 2026-03-10｜Michael Hogan｜guidance：光網路 SAM 同期放大逾五倍（原話："the optical networking SAM more than quintuples"）
- 2026-03-10｜Michael Hogan｜guidance：光網路 SAM 至 2030 年約 40% CAGR（原話："optical networking SAM will grow something like 40% CAGR"）
- 2026-03-10｜Michael Hogan｜competition：自稱矽光子代工最大業者（原話："we think we're the largest player in silicon photonics"）
- 2026-03-10｜Michael Hogan｜competition：併入 AMF 後自稱市佔第一，現今 SAM 約 10 億美元（原話："we're the #1 guy in the market"）
- 2026-03-10｜Michael Hogan｜commitment：預期市佔將持續提高（原話："our share will actually continue to grow"）
- 2026-03-10｜Kevin Soukup｜customer：前五大可插拔收發器廠中四家與 GF 合作（原話："4 out of 5 of the top pluggable transceiver players are"）
- 2026-03-10｜Gregg Bartlett｜competition：對 TSMC COUPE 的回應：主張開放生態、雙向相容（原話："We are very much in support of an open ecosystem."）
- 2026-03-10｜Michael Hogan｜capital_allocation：在既有無塵室空間內擴產，由美國與新加坡政府夥伴支持（原話："GlobalFoundries is scaling within existing clean room space"）
- 2026-03-10｜Michael Hogan｜capital_allocation：矽光子每增加一美元資本支出的營收效率提高（原話："revenue per dollar of incremental CapEx is meaningfully"）
- 2026-03-10｜Gregg Bartlett｜capital_allocation：Malta 矽光子與先進封裝廠預期提供整合流程至良品光模組（原話："expected to deliver a fully integrated silicon"）
- 2026-03-10｜Kevin Soukup｜capital_allocation：AMF 併購預期帶來營收與成本綜效（原話："we expect to unlock further revenue and cost"）
- 2026-03-10｜Michael Hogan｜product：銅線於每通道 200G 以上面臨根本挑戰（原話："Using copper becomes fundamentally challenged"）
- 2026-03-10｜Michael Hogan｜product：光互連使 XPU 使用率由十幾趴升至 80% 以上（原話："from as low as mid-teens to north of 80%"）
- 2026-03-10｜Gregg Bartlett｜product：晶圓對晶圓鍵合可縮小 RF 開關晶粒面積（原話："reduce the effective die size by as much as 45%."）
- 2026-03-10｜Michael Hogan｜guidance：前述 10 億美元目標由 2030 年提前至 2028 年底前年化（原話："we pulled in the expectation of sort of $1 billion-plus"）
- 2026-03-10｜Michael Hogan｜customer：稱 10 億美元年化目標已有客戶爭搶產能（原話："this is an oversubscribed corridor, right?"）
- 2026-03-10｜Gregg Bartlett｜product：非光學先進封裝各線暫無個別 TAM（原話："here's what the TAM is going to be for each of these."）
- 2026-03-10｜Gregg Bartlett｜product：各非光學封裝應用成長不及 CPO 光模組（原話："None of these are likely to grow at the rate that"）
- 2026-03-10｜Michael Hogan｜risk：管理層明說暫不提供先進封裝 TAM（原話："we're not ready to put a particular TAM on that"）
- 2026-03-10｜Eric Chow｜commitment：將於 2026 年 5 月 7 日在紐約舉辦投資人日（原話："we will be hosting an Investor Day on Thursday, May 7"）
- 2026-03-10｜Eric Chow｜guidance：近期營運問題延後到 Q1 財報後再答（原話："We will be happy to address near-term questions"）

### GFS_Analyst_Investor_Day_GLOBALFOUNDRIES_Inc_20260507.md
- 2026-05-07｜Sam Franklin (CFO)｜guidance：CI&D 市場長期成長目標 30% 以上（原話："we feel very comfortable with the target of 30-plus percent"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2025 CI&D 營收年增 29%（原話："We delivered 29% year-over-year revenue growth"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：車用目標：低雙位數成長（原話："our target to deliver low double-digit percentage growth"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：IoT 目標：中段十幾%成長（原話："we believe that a target growth rate of mid-teens"）
- 2026-05-07｜Michael Hogan｜guidance：智慧手機（SMD）預期大致持平（原話："we'll probably look to stay relatively flat in SMD"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：矽光子營收目標：2028 年底年化 10 億美元（原話："$1 billion run rate by the exit of 2028"）
- 2026-05-07｜Gregg Bartlett｜guidance：矽光子 2030 營收可達 20 億美元（原話："we can actually achieve $2 billion in revenue by 2030"）
- 2026-05-07｜Gregg Bartlett｜guidance：電源業務 2030 前增量營收 10 億美元（原話："targeting an incremental $1 billion of revenue in our power"）
- 2026-05-07｜Gregg Bartlett｜guidance：MIPS／客製矽業務 2030 年化營收 10 億美元（原話："we see an opportunity to achieve a $1 billion run rate"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2026 年底毛利率目標約 30%（原話："with a 30% gross margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2028 年底毛利率目標 40%（原話："we expect to achieve a 40% gross margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：長期毛利率目標 45%（原話："a line of sight to a 45% gross margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2028 年底營業利益率約 25%（原話："delivering approximately 25% operating margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：長期營業利益率約 35%（原話："support an operating margin of approximately 35% longer term"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2028 年底 EPS 約 4 美元、長期 6 美元（原話："approximately $4 of EPS exiting 2028, and $6 of longer-term"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：自由現金流率目標約 10%（原話："to target approximately 10% free cash margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2026 年資本支出占營收 15% 至 20%（原話："We're targeting about 15% to 20%"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：長期資本支出強度約 20%，且為淨額目標（原話："we think of that as a net target"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：技術服務占比 2026 全年預期靠近 12%（原話："we're going to be closer to that 12% end of the"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：毛利率 40% 橋接：組合貢獻 5 至 6 點（原話："6 points of margin opportunity over the next 3 years"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：製造成本與每層光罩現金成本改善貢獻 1 至 2 點（原話："can deliver 1 to 2 points of margin growth as well"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：折舊上升在未來幾年約構成一點左右的逆風（原話："probably is a point or so of headwind"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：模型未預設大幅漲價，毛利改善來自組合（原話："price increases just associated with supply and demand"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：毛利率與營業利益率差距維持約 15 點，2028 後才縮至 10 點（原話："that sort of 15-point delta to the gross margin"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：OpEx 成長速度約為營收 CAGR 的一半（原話："we expect our OpEx to grow at roughly half the"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：2026 Q1 毛利率年增 510 bps（原話："gross margin, up 510 basis points year-over-year"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：不按終端市場拆毛利，因產線設備可互換（原話："we don't break out the gross margin by end market"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：上市以來毛利率擴張超過 1,000 bps（原話："over 1,000 basis points of margin expansion"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：宣布首次季度現金股息（原話："initiation of a quarterly cash dividend of $0.12 per share"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：資本配置框架：回饋最多 50% 投資後自由現金流（原話："returning up to 50% of free cash flow after investments"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：預期可回收 30% 至 50% 的合格支出（原話："recover anywhere between 30% and 50% of eligible spending"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：第四筆併購預計未來幾個月內完成（原話："We have a fourth, which we expect to close in the next"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：10 億美元軟體與服務目標已含 ARC（原話："That's included."）
- 2026-05-07｜Sam Franklin (CFO)｜capital_allocation：最近五年資本支出強度約 22%，略高於前一版模型（原話："marginally higher than the prior model we shared"）
- 2026-05-07｜Sam Franklin (CFO)｜capital_allocation：未來自由現金流預期維持 10% 以上區間（原話："over the next 5 years in the 10-plus percent range"）
- 2026-05-07｜Timothy Breen (CEO)｜capital_allocation：美國將占成長投資的大宗（原話："that will be the lion's share of our growth investments"）
- 2026-05-07｜Sam Franklin (CFO)｜capital_allocation：正式併購 ARC IP 業務（原話："we're seeking to acquire the ARC IP business"）
- 2026-05-07｜Gregg Bartlett｜product：SCALE 為業界首個支援 OCI 的方案（原話："solution is the industry's first OCI capable solution"）
- 2026-05-07｜Gregg Bartlett｜product：CPO 材料級放量預期 2028 開始（原話："material volume in co-packaged optics will start"）
- 2026-05-07｜Gregg Bartlett｜product：CPO 顯著放量時點預估 2028 下半年（原話："probably the second half of '28"）
- 2026-05-07｜Sam Franklin (CFO)｜product：2028 前矽光子成長主要來自可插拔（原話："principally pluggables revenue growth focused"）
- 2026-05-07｜Michael Hogan｜product：車用毫米波雷達：FDX 靈敏度較 bulk CMOS 高 75%（原話："FDX is 75% more sensitive than the same solution"）
- 2026-05-07｜Gregg Bartlett｜product：量子運算目前為 NRE 型業務（原話："This is an NRE business for the foreseeable future"）
- 2026-05-07｜Sam Franklin (CFO)｜product：新增營收分類：製造服務與技術服務（原話："manufacturing services and revenue from technology services"）
- 2026-05-07｜Gregg Bartlett｜competition：可插拔光學方案低插入損耗光纖貼合（原話："We have a very elegant solution that has the lowest loss"）
- 2026-05-07｜Timothy Breen (CEO)｜competition：CEO 對 CPO 地位：預期為前二（原話："GF will be one of the top 2."）
- 2026-05-07｜Timothy Breen (CEO)｜competition：管理層預期車用小幅取得市占（原話："net-net, probably will gain a little bit of share"）
- 2026-05-07｜Timothy Breen (CEO)｜customer：2025 設計案 500 件，95% 為單一來源（原話："95% of those wins were awarded to GF on a sole-source"）
- 2026-05-07｜Timothy Breen (CEO)｜customer：2025 年再在岸化帶來 30 億美元設計案（原話："We had $3 billion of design wins in 2025 alone"）
- 2026-05-07｜Michael Hogan｜customer：車用營收由期初 1 億美元增至期中 14 億美元（原話："$100 million at the beginning of the decade, $1.4"）
- 2026-05-07｜Michael Hogan｜customer：IoT 優於市場主要來自市占提升（原話："I think it's mostly share gain."）
- 2026-05-07｜Timothy Breen (CEO)｜customer：與現代汽車集團簽署合作（原話："we announced a partnership with Hyundai Motor Group"）
- 2026-05-07｜Timothy Breen (CEO)｜customer：CSP 預計計畫後段轉向更直接參與（原話："the latter part of the plan into more direct work"）
- 2026-05-07｜Sam Franklin (CFO)｜risk：高效能 SiGe 產能超額認購至 2027 上半年（原話："seeing oversubscription in high-performance SiGe"）
- 2026-05-07｜Sam Franklin (CFO)｜risk：手機市場成長受限，管理層不倚賴其成長（原話："no longer reliant on the growth of smart mobile devices"）
- 2026-05-07｜Timothy Breen (CEO)｜risk：全球一半關鍵半導體產能在中國與台灣（原話："50% of essential semiconductor capacity"）

### GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20261014.md
- 2026-10-14｜CEO｜customer：GF 被選為日本出資至多 210 億美元、Malta 兩座 300mm 新廠的技術提供者與營運者（原話："GF has been selected as the technology provider and operator"）
- 2026-10-14｜CFO｜capital_allocation：由 SPV 出資並擁有廠房與設備，GF 不直接承擔資本支出（原話："without directly incurring the associated capital investment"）
- 2026-10-14｜CFO｜margin：數字口徑：費用組成為建廠與營運管理費、技術費及 SPV 的 EBITDA 分成（原話："GF will earn construction and operations management fees"）
- 2026-10-14｜CFO｜guidance：待最終協議簽署後，預期 2027 年營收貢獻約 5,000 萬美元（原話："expect revenue contribution of approximately $50 million"）
- 2026-10-14｜CFO｜guidance：毛利率增益 2027 年 30–50bp，長期 100–200bp（原話："annual accretion of 30 to 50 basis points in 2027"）
- 2026-10-14｜CFO｜guidance：營益率增益 2027 年 100–200bp，長期 200–300bp（原話："annual accretion of 100 to 200 basis points in 2027"）
- 2026-10-14｜CFO｜margin：營益率增幅高於毛利率增幅，管理層說明主因是建廠管理費的損益表認列（初步看法）（原話："our preliminary views on the income statement recognition"）
- 2026-10-14｜CFO｜guidance：EPS 增益 2027 年 0.10–0.15 美元，長期 0.50–0.75 美元（原話："annual accretion of $0.10 to $0.15 in 2027"）
- 2026-10-14｜CFO｜guidance：技術與廠務管理服務模式預期 10 年累計自由現金流約 30 億美元（原話："approximately $3 billion of cumulative free cash flow"）
- 2026-10-14｜CFO｜margin：數字口徑：10 年內每片晶圓利潤設計為與自建產能相當，但無對應固定成本（原話："target profit per wafer without incurring the associated"）
- 2026-10-14｜CEO｜commitment：時程：本季動工、2028 年可進機台、2029 年首批晶圓（原話："We expect to break ground during this quarter"）
- 2026-10-14｜CEO｜commitment：第二座廠須在 2028 年底前由利害關係人做 go/no-go 決定（原話："go/no-go decision between the stakeholders before the end"）
- 2026-10-14｜CFO｜risk：財務數字以簽署最終協議為前提，且僅反映第一座廠（原話："subject to the signing of definitive agreements"）
- 2026-10-14｜CEO｜product：新廠技術範圍為 FDX、BCD、UX 平台（原話："highly differentiated and sought-after FDX, BCD and UX"）
- 2026-10-14｜CEO｜capital_allocation：管理層稱此計畫與 GF 自有成長計畫並行、完全是額外增量（原話："does not displace or replace what GF is doing on its own"）
- 2026-10-14｜CEO｜customer：點名日美既有客戶與供應商，並稱與更多客戶處於進階洽談（原話："We are in advanced discussion with many more customers"）
- 2026-10-14｜Unknown Executive｜capital_allocation：CHIPS 辦公室同意將先前核定的 9.55 億美元資金改用於 2027 年起的研發與資本支出（原話："repurpose $955 million of our previously awarded CHIPS"）
- 2026-10-14｜Unknown Executive｜capital_allocation：美國商務部將取得 GF 約 4% 股權（原話："will receive an equity stake in GF of approximately 4%"）
- 2026-10-14｜Unknown Executive｜commitment：預期今日公告後美國政府不再有進一步股權參與（原話："we do not expect any further equity participation"）
- 2026-10-14｜CEO｜competition：管理層稱 GF 是少數在美國本土有規模產能與擴產能力的晶圓代工廠（原話："one of the only at-scale foundries with meaningful capacity"）
- 2026-10-14｜CEO｜product：每期滿載約新增 90 萬片年產能（300mm 約當）（原話："add approximately 900,000 wafers of annual capacity"）

### 問答異常語氣（迴避／改口／保留）
- GFS_Q2_2026_Earnings_Call_20260805.md｜問：Arcuri：SiPho 競爭者積極、客戶集中，客戶能否多源採購？｜答法：未直接說明多源採購可行性，改談競爭代表需求強、客戶超過40家、客戶要確保更多供給
- GFS_Q2_2026_Earnings_Call_20260805.md｜問：Muse：CID 2026 退出率約 3.5 億，2027 成長是大幅成長或消化期？｜答法：不給 2027 具體數字，重申長期模型 30%+ 成長，CEO 改談產能與生產力步調
- GFS_Q2_2026_Earnings_Call_20260805.md｜問：Caso：矽光子補助如何沖抵淨 CapEx？｜答法：CEO 回答補助的技術內容與戰略意義，未回答對淨 CapEx 的沖抵幅度
- GFS_Q2_2026_Earnings_Call_20260805.md｜問：Karl Ackerman：ARC 與 IVR 對 9 月財測的營收與費用貢獻｜答法：CFO 給全年營收區間與 Q3/Q4 1/3、2/3 分佈，未給 Q3 單季營收與費用絕對數字
- GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20260310.md｜問：Bryson：競爭對手稱握有逾 80% 矽光子市佔、營收與 GF 相近，如何解釋落差｜答法：Hogan 回「You can talk to the Tower about what they think」，未回應落差，改談自身十年投資與三大支柱
- GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20260310.md｜問：Garrigan：目前與 3 至 5 年後的市佔為何｜答法：未給市佔百分比，只講自身為第一、SAM 約 10 億美元、預期市佔續升
- GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20260310.md｜問：Hosseini：光學以外先進封裝機會與 TAM 數字｜答法：Bartlett 與 Hogan 皆明說暫不給 TAM，改談產品組合與「stay tuned」
- GFS_Analyst_Investor_Day_GLOBALFOUNDRIES_Inc_20260507.md｜問：Ted Kang（Craig Group）請按事業別拆分 2030 毛利率，並問何以營業利益率槓桿不如毛利率｜答法：管理層明確不拆毛利率（理由為產線設備可互換），改以組合與成本層次回覆；營業利益率差距以技術服務 R&D 密集解釋。
- GFS_Analyst_Investor_Day_GLOBALFOUNDRIES_Inc_20260507.md｜問：Charles Shi（Needham）請拆分毛利率改善中組合與效率占比，以及基礎晶圓代工毛利目標與補貼貢獻｜答法：CFO 給組合 5 至 6 點、成本 1 至 2 點等區間，但未提供基礎晶圓代工的毛利目標，也未量化補貼對毛利的貢獻。
- GFS_Analyst_Investor_Day_GLOBALFOUNDRIES_Inc_20260507.md｜問：Matt Bryson（Wedbush）問 1 百萬量子位元系統的含量或 TAM，及 IonQ 收購 SkyWater 的影響｜答法：Gregg 未給含量或 TAM 數字，改說之後有網路研討會，對 IonQ 事件僅說不評論；Tim 補充當日市場在找數字。

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

## ⑥ 條件附卡（archetype_hint='循環/商品' 命中）：judge_addendum_cyclical.md

<!-- source: .claude/skills/stock-analyst/references/cyclical-lens.md sha256:b13d95972edd47ea git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary 或 secondary ∈ {循環/商品，EMS/ODM}（QC-43 判定，含 capex 建設循環／需求量循環子型） -->

# QC-42 循環交易讀數（附錄 B）附卡

循環股的錢在 Game 2（投降買、延伸賣）。本附卡是平行、明標投機的交易讀數，不改長抱裁決。[§WHY]

## 一、觸發與子型判定
無循環 sleeve（純成長 mis-route）→ 整段省略。[§①]
商品子型（下列≥2命中→用商品 through-cycle 錶）：近5-7年≥1個GAAP虧損年｜peak-to-trough毛利率擺動>~20pp｜營收主由商品ASP驅動(price-taker)｜產業∈{記憶體/DRAM/NAND、礦業/材料/稀土、化工、航運、鋼鐵、太陽能、油氣E&P、部分晶圓/設備}｜capex/rev結構性>15%且ROIC高度擺動。未達≥2仍判循環→依驅動來源選capex建設循環錶或需求量循環錶。[§商品子型]

## 二、循環位置錶族（三選一，錨自身 through-cycle 區間非動能；位置落 深谷投降/早循環/中循環/晚循環/過熱頂部，多數決+sourced 裁決）
商品 through-cycle（MU 型，6 訊號）：P/B vs 自身區間(近1x/下緣=買，>中位2x/上緣=賣)｜量 vs 價(量增領先=買，ASP-only量平降=賣)｜GM vs自身區間(近谷/負=買，近峰=賣)｜供給紀律(減產=買，新產能洪水=賣)｜庫存(去化乾淨=買，通路+公司堆積=賣)｜情緒/部位(投降PT>價=買，狂熱PT<價=賣)。[§B.1商品]
capex 建設循環（ORCL 型，6 訊號）：capex/折舊比(低/正常化=買，遠高於1=賣)｜產能利用率爬坡(低基期回升=買，滿載見頂=賣)｜RPO(backlog)vs capex覆蓋(backlog領先=買，capex超前需求=賣)｜交易對手信用(客戶分散信用強=買，集中燒錢客戶=賣)｜情緒/部位(同上)｜量vs價(量增領先=買，ASP承壓量見頂=賣)。[§B.1capex]
需求量循環（EMS/ODM，JBL 型，5 訊號）：book-to-bill/需求量拐點(>1拐點向上=買，<1量見頂=賣)｜客戶庫存去化(去化乾淨=買，通路+客戶堆積=賣)｜倍數vs自身歷史re-rate均值回歸(近下緣=買，>5Y中位×1.5/貼峰=賣)｜終端·hyperscaler capex週期位置(早週期=買，晚週期見頂=賣)｜情緒/部位(同上)。[§B.1需求量]

## 三、交易姿態 + 反動能硬閘（跨子型通用，逐條檢查，觸發即 override 向保守）
位置→姿態：深谷投降→積極分批建立｜早→分批建立｜中→持有不加｜晚→分批了結｜頂→清光不碰。[§B.2]
閘1 位置=晚/頂→姿態不得為任何「建立」。閘2 成長=ASP-only+量持平/降→最多「持有」。閘3 P/B>自身中位2x→禁新建立。閘4 訊號矛盾→標「位置不明，觀望」不硬給姿態。閘5 TTM/Fwd本益比或EV倍數>自身歷史高區(>5Y中位×1.5、或貼/破歷史峰)→禁新建立。[§閘1-5]

## 四、落欄與 §13 row 8b 接線
`cycle_position`(深谷投降｜早循環｜中循環｜晚循環｜過熱頂部)＋`cycle_verdict`(右側可追蹤｜等回踩｜頂部觀望｜未觸發)；非循環 archetype 不填，整欄省略。[§落欄]
接 §13 row 8b：位置∈{深谷投降，早循環}+五閘全過+moat底線+獨立critic冷讀通過→落「進場・條件式(循環衛星)」(倉位上限3%)；任一不成立→只落研究提名，§13維持觀望。驗證失敗不得升級，只能降回觀望。`trade_stance`僅進HTML不入dd-meta。[§row8b]

## 五、雙制度與兩軌背離
有 secular sleeve + commodity sleeve → 循環鏡頭只套 commodity sleeve，secular sleeve 一句話另計(不隨循環賣)。[§⑤]
投資軌(§13長抱視角) vs 交易軌(本鏡頭位置)：底部背離(長抱視角迴避 + 循環位置深谷投降/早循環)是本鏡頭獨門訊號；頂部多收斂(皆遠離)。[§B.3]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20261012","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"2026 Q3 實績 Non-IFRS 毛利率 ≥30% 且 Q4 指引 ≥31%、通訊基建與資料中心全年年增 50% 以上維持 → 重跑判斷後進場首倉","irr_base_pct":6.9,"ev5y_pct":41.5,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"❌","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.0,"ev5y_pct":41.5,"irr_base_pct":6.9,"max_dd_pct":-60,"bull_5y_price":117.6,"bear_5y_price":28.8,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"2026 Q3 實績 Non-IFRS 毛利率 ≥30% 且 Q4 指引 ≥31%、通訊基建與資料中心全年年增 50% 以上維持 → 重跑判斷後進場首倉","price_at_dd":48.24,"archetype":"循環/商品","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
