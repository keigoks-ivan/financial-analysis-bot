你是 stock-analyst **v20 判斷 agent**，標的 GFS（20261012）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"GFS","date":"2026-10-12","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261012/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261012/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1786,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"},"note":"高於公司自家指引區間上緣（CEO 說法）；Earnings Whispers 共識約 $1.76B（二手來源，未經 IR 驗證）"},{"id":"f_kpi1_non_ifrs","label":"Non-IFRS 營業利益率","value":16.7,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益率","value":9.7,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"}},{"id":"f_kpi6_q3_2026","label":"下一季（Q3 2026）指引：營收","value":1885,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-05","period":"2026-08-05","unit":"date","basis":"距今 48 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_gfs_gross_margin_pct","label":"GFS 毛利率","value":27.14,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GFS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_gfs_operating_margin_pct","label":"GFS 營業利益率","value":11.59,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GFS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_gfs_fcf_margin_pct","label":"GFS FCF 利潤率","value":11.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GFS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2330_tw_gross_margin_pct","label":"2330.TW 毛利率","value":64.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2330_tw_operating_margin_pct","label":"2330.TW 營業利益率","value":56.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2330_tw_fcf_margin_pct","label":"2330.TW FCF 利潤率","value":25.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_intc_gross_margin_pct","label":"INTC 毛利率","value":38.6,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INTC.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_intc_operating_margin_pct","label":"INTC 營業利益率","value":7.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INTC.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_intc_fcf_margin_pct","label":"INTC FCF 利潤率","value":4.96,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INTC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_gross_margin_pct","label":"005930.KS 毛利率","value":57.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_operating_margin_pct","label":"005930.KS 營業利益率","value":36.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_005930_ks_fcf_margin_pct","label":"005930.KS FCF 利潤率","value":28.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2303_tw_gross_margin_pct","label":"2303.TW 毛利率","value":30.6,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2303.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2303_tw_operating_margin_pct","label":"2303.TW 營業利益率","value":20.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2303.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2303_tw_fcf_margin_pct","label":"2303.TW FCF 利潤率","value":23.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2303.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3","label":"營業現金流","value":405,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"}},{"id":"f_kpi4_non_ifrs","label":"調整後自由現金流（Non-IFRS）","value":-3,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"}},{"id":"f_kpi5_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":49.4,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-05）","citation":"GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":48.24,"period":"2026-10-09（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-1.02,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":50.83,"period":"2026-10-09（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.96 → 1.96）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.38,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.62 → 2.63）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.28,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.55 → 3.56）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.96,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.63,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.56,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":3.16,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 1.9 → 1.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":37.69,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.88,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝72.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":72.5,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.78,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝62.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":62.2,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":24.61,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 1.96，分子＝快照價 48.24","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.498,"period":"2026-10-12","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-12"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Counterpoint 純晶圓代工季度份額：GFS 由 2024Q4 約 5% 降至 2025 年 4%，2026Q1 為 3%；TSMC 2026Q1 佔 73%，產業年增 30%（AI GPU/ASIC 驅動）。","source":"Counterpoint Research, Global Pure Foundry Market Share: Quarterly","url":"https://www.counterpointresearch.com/en/insights/global-semiconductor-foundry-market-share","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"TrendForce 稱 GFS 2025 年晶圓代工營收排名第五、份額 3.87%；Tower 第七、0.89%；GFS 與 Tower 在 RF、矽光子等利基競爭。","source":"TrendForce News via Reuters (搜尋摘要轉述)","url":"https://www.trendforce.com/news/?p=55236","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2026Q1 管理層稱 design wins 年增約 50%，四大終端市場皆有；車用嵌入式 MRAM 客戶已 tape-out，與 Bosch 等一級供應商接觸增加。","source":"GlobalFoundries Q1 2026 earnings call transcript (Motley Fool)","url":"https://www.fool.com/earnings/call-transcripts/2026/05/05/globalfoundries-gfs-q1-2026-earnings-transcript/","excerpt":"In the first quarter, we saw a 50% increase in design wins compared to the same period a year ago, with excellent representation across all 4 major end markets.","as_of":"2026-05-05","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2026Q2：GFS 取得七項光網路（AI 資料中心）design wins，涵蓋收發器廠、超大規模業者與網通公司；另有一項 SCALE 平台 CPO 相關設計 tape-out，預期 Q3 再一項（二手摘要）。","source":"MarketBeat, GlobalFoundries Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/globalfoundries-q2-earnings-call-highlights-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"TrendForce 2Q26：前十大代工營收季增 11.5% 至近 534.9 億美元，SMIC 縮小與 Samsung 的份額差距；摘要未提 GFS 當季數字。","source":"TrendForce press center, 2026-09-09","url":"https://www.trendforce.com/presscenter/news/20260909-13225.html","excerpt":null,"as_of":"2026-09-09","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Simply Wall St 社群敘事（非公司/機構資料）主張 GFS 先進製程落後 TSMC/Samsung，且在地化要求與客戶垂直整合為風險；未找到 2026 針對 GFS 的具名新進入者報導。","source":"Simply Wall St community narrative","url":"https://simplywall.st/community/narratives/us/semiconductors/nasdaq-gfs/globalfoundries/w0hqa7cr-legacy-fabs-will-suffer-as-tsmc-and-samsung-lead","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2024 20-F：兩個匿名客戶各超過營收 10%，Customer A 2024 年占 16%（$1,061M）、Customer B 占 11%（$722M）；客戶名稱未揭露。","source":"GLOBALFOUNDRIES Form 20-F FY2024 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904825000024/gfs-20241231.htm","excerpt":"Customer A accounted for $1,061 million, or 16%, in 2024, and Customer B $722 million, or 11%.","as_of":"2024-12-31","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2021 20-F：前十大客戶占晶圓出貨量 2019/2020/2021 年約 73%/73%/67%；公司預期營收仍將集中在少數客戶。","source":"GLOBALFOUNDRIES Form 20-F FY2021 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904822000008/gfs-20211231.htm","excerpt":"Our ten largest customers in 2019, 2020 and 2021 accounted for approximately 73%, 73% and 67% of our wafer shipment volume, respectively.","as_of":"2021-12-31","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TrendForce 預估 2026 年前十大晶圓代工 8 吋平均稼動率近 90%（2025 約 80%），全球 8 吋產能至 2027 上半年續呈負成長","source":"TrendForce／iconnect007 mature-node foundry price increases","url":"https://evertiq.com/news/2026-05-07-mature-node-foundry-prices-set-to-rise-as-ai-demand-tightens-capacity","excerpt":"The average 8-inch capacity utilisation rate among the world's ten largest foundries is projected to approach 90% in 2026, up from around 80% in 2025; TrendForce expects global 8-inch capacity to remain in negative growth through the first half of 2027.","as_of":"2026-05-07","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"成熟製程晶圓代工 2026 Q1→Q2 全面漲價 5–15%，第三輪漲價可能從 2026 下半年延續到 2027","source":"TrendForce／evertiq","url":"https://evertiq.com/news/2026-05-07-mature-node-foundry-prices-set-to-rise-as-ai-demand-tightens-capacity","excerpt":"The industry is also preparing a third round of price increases that could extend from the second half of 2026 into 2027.","as_of":"2026-05-07","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"12 吋擴產近 70% 來自中國晶圓廠，其餘地區擴產溫和；TSMC 縮減 12 吋成熟產能預期將轉單給其他代工廠","source":"TrendForce／iconnect007","url":"https://iconnect007.com/article/150606/ai-chip-shortage-foundry-cuts-to-extend-maturenode-price-hikes-in-2027/150603/smt","excerpt":"Nearly 70% of capacity expansion in this segment is being driven by Chinese foundries, while expansion elsewhere remains moderate.","as_of":"2026-06-30","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"TrendForce 2023 年預測中國成熟製程產能占比 2027 年達 39%，並警告 CIS、DDI、PMIC、功率離散元件可能價格競爭（舊預測，早於 2026 年緊俏）","source":"TrendForce press 2023-12-14","url":"https://www.trendforce.com/presscenter/news/20231214-11959.html","excerpt":null,"as_of":"2023-12-14","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"GF 管理層：通訊基礎建設與資料中心營收年增 62%，預期 2026 年該區塊成長 50–60%，矽光子營收翻倍以上；SiGe 產能至 2027 已超額訂購並擴產","source":"GlobalFoundries Q2 2026 earnings call highlights (MarketBeat)","url":"https://www.marketbeat.com/instant-alerts/globalfoundries-q2-earnings-call-highlights-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"GF 2026 Q2 財報電話會議：車用與智慧行動營收轉弱，家用與工業 IoT 改善","source":"GlobalFoundries Q2 2026 earnings call highlights (MarketBeat)","url":"https://www.marketbeat.com/instant-alerts/globalfoundries-q2-earnings-call-highlights-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"UBS 逆市場共識認為成熟製程晶圓代工進入上行週期（供給重分配驅動），預期 2027–2028 獲利更有上檔","source":"UBS view via Webull news","url":"https://www.webull.com/news/15654887556711424","excerpt":"Earlier, UBS put forward the opposite view from market consensus, that the mature process foundry industry will usher in an upward cycle, which is driven by the reallocation of supply and resources throughout the industry.","as_of":"2026-06-30","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#7","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"消費性電子受記憶體漲價與零組件成本拖累，2026 下半年出貨承壓，部分客戶希望延後漲價","source":"TrendForce DRAMeXchange weekly research","url":"https://dramexchange.com/WeeklyResearch/Post/2/12752.html","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"新加坡競爭及消費者委員會（CCCS）於 2026-04-13 裁定 GFS 已完成的 Advanced Micro Foundry 收購未造成實質減損競爭（審查範圍限於可插拔收發器代工服務）；屬結構性放行，非調查。","source":"CCCS public register: Acquisition by GlobalFoundries Singapore Pte. Ltd. of Advanced Micro Foundry Pte. Ltd.","url":"https://www.ccs.gov.sg/case-register/public-register/mergers-and-acquisitions/acquisition-by-globalfoundries-singapore-pte--ltd--of-advanced-micro-foundry-pte--ltd-/","excerpt":null,"as_of":"2026-04-13","retrieved_at":"20261012","affects":["moat_trend","triggers"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"GFS 向 ITC 提出專利侵權申訴，ITC 於 2026-04-27 對 Tower 製造的晶片立案調查，GFS 請求有限排除令與停止令；屬 IP 案件，非反壟斷，尚無裁決。","source":"Federal Register via policyrisk.com: ITC Investigates Imported Chips for Patent Sneakiness in Tech Wars","url":"https://policyrisk.com/federal-register/2026-08439","excerpt":null,"as_of":"2026-04-27","retrieved_at":"20261012","affects":["moat_trend","triggers"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2024-11 美國商務部 BIS 就 GFS 2021-02 至 2022-10 間向實體清單中國公司出口晶圓的違規予以處罰（GFS 承認違反 EAR）；屬過往出口管制執法。","source":"Linklaters: Due Diligence in China's Semiconductor Value Chain - Lessons from the GlobalFoundries Enforcement Case","url":"https://www.linklaters.com/knowledge/publications/alerts-newsletters-and-guides/2024/november/07/due-diligence-in-chinas-semiconductor-value-chainlessons-from-the-global-foundries-enforcement-cas","excerpt":null,"as_of":"2024-11-07","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"GFS FY2025 20-F：2026年1月總統公告對有限的先進運算晶片及部分衍生產品加徵25%關稅；公司稱不認為其業務目前受此關稅牽涉，但仍可能有進一步關稅（含歐洲）。","source":"GLOBALFOUNDRIES Inc. Form 20-F FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904826000022/gfs-20251231.htm","excerpt":"Although we do not believe our business is currently implicated by the new tariffs","as_of":"2026-01-15","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026年1月Section 232公告：對窄範圍先進半導體加徵25%關稅，生效2026-01-15；美國資料中心用晶片等用途豁免；後續可能擴大並設投資美國產能的關稅抵減機制。","source":"White & Case / EY Global Tax News：Section 232 semiconductor proclamation","url":"https://taxnews.ey.com/news/2026-0209-us-section-232-proclamation-imposes-25-percent-tariff-on-certain-semiconductors","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261012","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2024-11-01 BIS 對 GFS 處以50萬美元和解罰款：2021–2022年向實體清單公司 SJ Semiconductor 出貨約1,710萬美元晶圓未取得許可；GFS自行揭露並合作，歸因於交易篩查系統資料輸入錯誤。","source":"Manufacturing Dive / BIS 執法案","url":"https://www.manufacturingdive.com/news/commerce-department-globalfoundries-500k-fine-sj-semiconductor-entity-list/733768/","excerpt":null,"as_of":"2024-11-01","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Yahoo Finance 報導（Wedbush 降評）稱聯邦指引顯示對中國半導體關稅要到2027年6月才生效，更激進的Section 232措施近期較不可能；未對照政府原文確認。","source":"Yahoo Finance: Wedbush downgrades GlobalFoundries","url":"https://finance.yahoo.com/news/wedbush-downgrades-globalfoundries-sees-more-132056656.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"據 policyrisk.com 對 SEC 申報的摘要，GF 對單一 SOI 晶圓供應商（摘要指為 Soitec）的採購占比為 2025 年 71.4%、2024 年 60.9%、2023 年 63.0%；替換該供應商需時甚長。部分原料（稀土、天然氣）亦有單一來源，價格與供應受美中貿易緊張及烏克蘭、中東衝突影響。（二手摘要，未核對申報原文）","source":"policyrisk.com GFS company page（SEC 申報摘要）","url":"https://policyrisk.com/world/company/GFS","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"GF 申報文件的風險語言提及其業務可能受地緣政治狀況影響，例如與中國的政治與貿易緊張（2024 年 6-K 與投資人文件；非 2026 專屬揭露）。","source":"GLOBALFOUNDRIES Form 6-K 3Q2024 earnings","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904824000061/globalfoundries3q2024earni.htm","excerpt":null,"as_of":"2024-11-12","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2025 年 4 月有報導稱 GF 與台灣聯電（UMC）洽談合併，背景為台灣風險與中國成熟製程擴張；UMC 財務長否認有此案。","source":"Electronics360 / GlobalSpec: Report: GF and UMC mull chip foundry merger","url":"https://electronics360.globalspec.com/article/22133/report-gf-and-umc-mull-chip-foundry-merger","excerpt":null,"as_of":"2025-04-01","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"第三方評論稱 GF 紐約 Malta 廠具美國國防部 Trusted Foundry 認證，並獲最高 15.75 億美元聯邦 CHIPS 補助及紐約州 5.5 億美元，被視為降低對台灣產能依賴的緩衝（TradingView 使用者文章，屬意見而非公司揭露，未核實）。","source":"TradingView GFS 使用者文章","url":"https://pl.tradingview.com/chart/GFS/fWfqAsxk/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"產業層面：Fusion 2026 Q1 報告指台灣中斷將立即觸發全球「Level 1」供應危機；Design News 指 AI 需求把產能拉向先進製程，類比與混合訊號晶片廠在成熟製程晶圓配額上競爭縮水的分配。","source":"Fusion Worldwide MILT 26Q1; Design News","url":"https://info.fusionww.com/hubfs/Q1%202026%20Industry%20and%20Intelligence%20Reports/Fusion%20MILT%20-%2026Q1.pdf?hsLang=en","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 通訊基建與資料中心段營收年增 62%（上半年 +47%），來自 SiPh 與 SiGe 需求；管理層將 2026 全年該段成長展望上調至 50–60%（原高 30% 區間）。","source":"GLOBALFOUNDRIES Form 6-K (Q2 2026); MarketBeat Q2 call highlights","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000219/gfs-20260630_d2.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q2 2026 車用營收年減 9.5%（客戶出貨遞延至下半年），上半年仍 +5.6%；Q1 車用年增 24%，管理層當時預期全年低雙位數成長。","source":"GLOBALFOUNDRIES Form 6-K (Q2 2026); Motley Fool Q1 2026 transcript","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000219/gfs-20260630_d2.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261012","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Q2 2026 智慧行動裝置段營收年減 5.7%（上半年 -5.3%），歸因記憶體價格導致智慧手機疲弱；居家與工業 IoT 段 Q2 +10.3%、上半年 -6.7%，管理層上調 IoT 展望。","source":"GLOBALFOUNDRIES Form 6-K (Q2 2026); MarketBeat Q2 call highlights","url":"https://www.marketbeat.com/instant-alerts/globalfoundries-q2-earnings-call-highlights-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 營收 $1.786B（季增 9%、年增 6%）；Q3 指引 $1.885B ±$25M，非 IFRS 毛利率 30.5% ±100bps。","source":"MarketBeat / Quartr Q2 2026 summary","url":"https://quartr.com/events/globalfoundries-inc-gfs-q2-2026_ojFuZzVo","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"GF 預期矽光營收 2026 年超過倍增，目標 2028 年底矽光年化營收達 $10 億，長期 $20 億；共封裝光學拐點在 2028 年底至 2029 年；GF 估計 2030 年可服務市場約 $110 億。","source":"Nasdaq/Yahoo: GlobalFoundries maps path to 40% margins; iAmsterdam summary; TrendForce 2026-05-07","url":"https://www.nasdaq.com/articles/globalfoundries-maps-path-40-margins-silicon-photonics-demand-builds","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"成熟製程晶圓代工報價走升：分析師預期 UMC 2026 下半年漲價 5–10%、2027 再 5–10%；TrendForce 預估 2026 年 8 吋前十大廠平均稼動率近 90%（2025 約 80%）；TrendForce 2026 年 9 月稱消費 IC 客戶 Q3 晶圓價格可能上漲。無 GF 自身調價資料。","source":"Evertiq 2026-05-07 Mature node foundry prices set to rise; TrendForce press release 20260909; StreetInsider UMC pricing report","url":"https://evertiq.com/news/2026-05-07-mature-node-foundry-prices-set-to-rise-as-ai-demand-tightens-capacity","excerpt":null,"as_of":"2026-09-09","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"-","claim":"Counterpoint 純代工市佔表：GF 2026 Q1 約 3%，2024 Q4 為 5%；TSMC 73%。","source":"Counterpoint Research Global Pure Foundry Market Share: Quarterly","url":"https://www.counterpointresearch.com/en/insights/global-semiconductor-foundry-market-share","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"-","claim":"IDC 2026 年 2 月預測 2026 智慧手機出貨年減 12.9% 至約 11.2 億支、2027 年 +2%；後續（約 2026 年 6 月，二手報導）修正為 2026 年 -13.9% 至約 10.9 億支、2027 年 -1.1%、2028 年 +5.5%。IDC 預期記憶體晶片價格 2027 年中趨穩。","source":"eeNews Europe / Gigazine (IDC Feb 2026); IT Brief (IDC revision, secondary)","url":"https://www.eenewseurope.com/en/smartphone-memory-shortage-2026-idc/","excerpt":null,"as_of":"2026-02-27","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#8","axis":"end_markets","section":"coverage","direction":"0","claim":"S&P Global 2026 年 3 月車用半導體需求報告：記憶體恐成瓶頸；功率半導體隨電動化成長，MCU 與類比仍關鍵且與產量連動。Meticulous Research（2026 年 5 月）估車用半導體 2025 年 $638 億、2026 年 $724 億，2026–2036 CAGR 7.4%。無主要機構的當期 2027 預測。","source":"S&P Global Inside automotive semiconductor demand 2026; Meticulous Research","url":"https://autotechinsight.spglobal.com/shop/product/5003699/inside-automotive-semiconductor-demand-2026","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261012","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"GFS FY2025 20-F 風險揭露未見專門的技術替代/過時風險條款；最接近者為提前投產致庫存/過時成本，及技術在廠間轉移時若需求驟降會衝擊整廠稼動率。","source":"SEC GLOBALFOUNDRIES Form 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904826000022/gfs-20251231.htm","excerpt":"This exposes us to the risk that our operations, including our utilization rate for entire fabs, may be severely impacted if demand for those technologies drops suddenly or for an extended period.","as_of":"2026-03-01","retrieved_at":"20261012","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"FY2023 20-F 載明技術與服務價格隨時間下滑，未推出新技術可能迫使既有技術降價。","source":"SEC GLOBALFOUNDRIES Form 20-F FY2023","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904824000013/gfs-20231231.htm","excerpt":"the market prices for technology and services tend to fall over time, except in times of extreme supply shortage.","as_of":"2024-03-01","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"矽光子被報導為特殊製程晶圓廠的成長線：GFS 管理層預期 2026 年矽光子營收約倍增、2028 年可能超過 10 億美元（為 GFS 自有技術的成長面，非替代威脅）。","source":"TrendForce News 2026-05-07 GlobalFoundries silicon photonics revenue","url":"https://www.trendforce.com/news/2026/05/07/news-globalfoundries-reportedly-sees-silicon-photonics-revenue-doubling-in-2026-passing-1b-by-2028/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"中國成熟製程晶圓廠持續擴張：Nexchip 28nm 邏輯平台於 2026-03-11 完成開發，Silan、Hua Hong 亦擴產與製程升級（競爭壓力，非替代技術）。","source":"TrendForce News 2026-03-26 Nexchip, Silan and Hua Hong mature node","url":"https://www.trendforce.com/news/2026/03/26/news-nexchip-silan-and-hua-hong-step-up-efforts-in-advancing-mature-node-foundry/","excerpt":null,"as_of":"2026-03-26","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"+","claim":"IDC 預期 2026 年全球 8 吋產能下滑約 3%，部分晶圓廠漲價最高 10%，成熟製程供需轉向。","source":"IDC press release Foundry 2.0 market 360B 2026","url":"https://www.idc.com/resource-center/press-releases/foundry-2-0-market-360b-2026/","excerpt":null,"as_of":"2026-03-30","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"GF 2026 年 6 月收購 Synopsys ARC 處理器 IP 業務，公司稱此使其成為提供「軟體到矽」能力的整體技術夥伴（由純代工往解決方案延伸）。","source":"GLOBALFOUNDRIES Form 6-K, Q2 2026 earnings","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm","excerpt":"holistic technology partner, offering customers a software-to-silicon capability for Physical AI and beyond","as_of":"2026-08","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2026 年 5 月 GF 推出 Quantum Technology Solutions，預期獲美國商務部 3.75 億美元補助。","source":"GLOBALFOUNDRIES Form 6-K, Q2 2026 earnings","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm","excerpt":null,"as_of":"2026-08","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"GM 與 GF 簽直接長約（繞過晶片設計商），為專屬產能協議；屬 2023 年舊事，非 2026 新變化。","source":"eeNews Europe: GM signs first long term supply deal direct with GlobalFoundries","url":"https://www.eenewseurope.com/en/gm-signs-first-long-term-supply-deal-direct-with-globalfoundries/","excerpt":null,"as_of":"2023-02-09","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026 指引（2026-08-05）：營收約 18.85 億美元（±0.25 億）、non-IFRS 稀釋 EPS 0.51（±0.05）、non-IFRS 營業利益率 16.7%±170bps；EPS 指引區間 0.46–0.56 對比共識約 0.47（另一來源 0.49／營收 18.7 億），大致貼近共識","source":"MarketBeat: GlobalFoundries issues Q3 2026 earnings guidance; SEC 6-K Q2 2026","url":"https://www.marketbeat.com/instant-alerts/globalfoundries-nasdaqgfs-issues-q3-2026-earnings-guidance-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261012","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 營收指引發布後 Chartmill 報導盤前約下跌 5.5%，稱 Q3 營收預測略低於市場預期；Benzinga 則稱營收預測較前次區間 17.4–17.8 億上調，兩來源對「上調或略低」解讀不一","source":"Chartmill: GlobalFoundries Dips After Q3 Revenue Forecast Trails Estimates; Benzinga earnings forecasts","url":"https://www.chartmill.com/news/GFS/Chartmill-52785-GlobalFoundries-NASDAQGFS-Dips-After-Q3-Revenue-Forecast-Trails-Estimates","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 調整後 EPS 0.46 vs 共識 0.43，營收 17.9 億美元（年增 5.8%）；管理層稱營收與 non-IFRS 獲利指標達或高於指引區間高端；資料中心與通訊營收 2026 預期成長 50–60%，矽光子營收將翻倍以上","source":"MarketBeat: posts quarterly earnings results beats estimates by $0.03 EPS; Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/globalfoundries-nasdaqgfs-posts-quarterly-earnings-results-beats-estimates-by-003-eps-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 統計 2022-11 至 2026-08 間公司上調展望 7 次、下調 4 次","source":"Benzinga GFS earnings forecasts","url":"https://www.benzinga.com/quote/GFS/earnings-forecasts","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布最新快照（Investing.com，約 2026-10）：21 位分析師，12 買／9 持有／1 賣，平均目標價 80.24 美元，高 125、低 60；Arete 升至 95 為最近動作。較早快照：MarketBeat 2026-08-05 共識 Hold、平均 74.12；Benzinga 2026-08-14 平均 63（19 位分析師，中性）；StockAnalysis 2026-06 為 78.95；Fintel 平均 79.38、高 147。各聚合站快照日期不一，分布不一致","source":"Investing.com GlobalFoundries consensus estimates; MarketBeat; Benzinga sentiment; StockAnalysis; Fintel","url":"https://uk.investing.com/equities/globalfoundries-consensus-estimates","excerpt":null,"as_of":"2026-10-12","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"賣方個別調整：2026-02 UBS 目標價 45→50（Neutral）、TD Cowen 42→56（Buy）、Baird 40→60（Outperform）；JPMorgan Harlan Sur 維持 Neutral、目標價 40→35 並稱 2026 市場預期可能過於樂觀（該則日期未標示，可能為 2025 年）","source":"Yahoo Finance: UBS Raises its Price Target on GLOBALFOUNDRIES to $50; Benzinga","url":"https://finance.yahoo.com/news/ubs-raises-price-target-globalfoundries-110743438.html","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#6","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Axelrod Research 2026-10-07 筆記評級 HOLD，稱 2026-10-06 收盤 48.63 美元，對比 2026-05-09 的 74.12 美元（該筆記依 5 月營運快照，非新財報修正）","source":"Axelrod Research: GFS the foundry thesis survives","url":"https://buttondown.com/user75/archive/axelrod-research-gfs-the-foundry-thesis-survives/","excerpt":null,"as_of":"2026-10-07","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"GF 於 2026-01-14 簽約、2026-06-01 完成收購 Synopsys ARC Processor IP Solutions 業務，對價 $455M（含現金 $440M），與已持有的 MIPS 合併強化 RISC-V IP。","source":"GLOBALFOUNDRIES Form 6-K (2026-06-30) / MarketScreener","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000219/gfs-20260630_d2.htm","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261012","affects":["moat_trend","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"TrendForce 報導：12 吋成熟製程擴產約 70% 由中國晶圓廠驅動；SMIC、華虹、晶合（Nexchip）新廠陸續投產，Nexchip 合肥四期 51 億美元擴 28nm。","source":"TrendForce News / Tom's Hardware（搜尋摘要轉述）","url":"https://tomshardware.com/tech-industry/semiconductors/the-trailing-edge-foundry-roadmap-examined","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"TrendForce 預期全球 8 吋產能至 2027 上半年續負成長，漲價趨勢延伸至 2027；TSMC 6 吋 Fab 2 與 8 吋 Fab 5 預計 2027 年底前關閉。","source":"TrendForce Press Center 2026-06-30","url":"https://www.trendforce.com/presscenter/news/20260630-13127.html","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"IDC 預期 2026 全球 8 吋產能約降 3%，TSMC 與 Samsung 開始削減 8 吋；TSMC 預計 2028 前將 Fab14 12 吋成熟製程產能削減 15–20%；2026 Q1→Q2 晶圓代工價格約漲 5–15%。","source":"IDC / iconnect007 / finviz（搜尋摘要轉述）","url":"https://iconnect007.com/article/150606/ai-chip-shortage-foundry-cuts-to-extend-maturenode-price-hikes-in-2027/150603/ein","excerpt":null,"as_of":"2026-03-30","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"GF 2026 capex 指引為營收 15–20%（2025 為 8%）；宣布德勒斯登廠產能倍增（目標 2032 完成）；華虹無錫專案約 67 億美元、月增約 3 萬片；SMIC 2026 資本支出預測 80 億美元以上；UMC capex 持平、新加坡投產延至 2026。","source":"Fab Tracker February 2026 (GF IR) / Tom's Hardware（搜尋摘要轉述）","url":"https://s29.q4cdn.com/619069826/files/doc_financials/2025/q4/Fab-Tracker-February-2026.pdf","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261012","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"TrendForce 3 月晶圓代工簡報：華虹 capex 高峰已過；SMIC 擴產步調趨緩（消費需求逆風）；GF 為美歐在地化提高 capex。","source":"TrendForce Foundry Market Bulletin 2026-03-02","url":"https://www.trendforce.com/research/download/RP260302TJ3","excerpt":null,"as_of":"2026-03-02","retrieved_at":"20261012","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"TrendForce 2026年6月分析：消費電子庫存回補、AI需求、地緣因素與TSMC逐步退出成熟製程，正在重塑成熟製程供需；另警告電視與筆電提前備貨使2H26庫存有疑慮。","source":"TrendForce, Mature Node Repricing: AI Squeeze Reshapes Foundry Landscape","url":"https://www.trendforce.com/research/download/RP260629VB3","excerpt":null,"as_of":"2026-06-29","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"TrendForce 2026年4月：成熟製程價格或在2026回升，但庫存過剩與中國同業競爭仍構成壓力。","source":"TrendForce News, Mature node prices may rebound in 2026 but inventory overhang and China competition weigh","url":"https://www.trendforce.com/news/2026/04/03/news-mature-node-prices-may-rebound-in-2026-but-inventory-overhang-and-china-competition-weigh/","excerpt":null,"as_of":"2026-04-03","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"TrendForce：2026年Q1至Q2晶圓代工價格普遍上漲約5%至15%，第三輪漲價可能自2026年底延續至2027；8吋稼動率2026年達88%、2H26預估90%，TSMC與Samsung縮減8吋產能。","source":"TrendForce press release 2026-06-30 (via iconnect007 / trendforce.com presscenter)","url":"https://www.trendforce.com/presscenter/news/20260630-13127.html","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"GF自身存貨2026-06-30為16.22億美元（2025-12-31為15.77億；2026-03-31為16.86億），存貨備抵由9,000萬增至1.4億美元。未找到GF 2026年客戶/通路庫存水位的揭露。","source":"GlobalFoundries Form 6-K (quarter ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000219/gfs-20260630_d2.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"FY2024 營收 67.5 億美元，較 FY2023 的 73.92 億下降 9%（-6.42 億）","source":"GlobalFoundries Reports Fourth Quarter 2024 and Fiscal Year 2024 Financial Results","url":"https://investors.gf.com/news-releases/news-release-details/globalfoundries-reports-fourth-quarter-2024-and-fiscal-year-2024/","excerpt":"Net revenue was $6,750 million in FY2024 versus $7,392 million in FY2023, a $642 million or 9% decline.","as_of":"2025-02-11","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"FY2024 GAAP 毛利率 24.5%，較 FY2023 的 28.4% 下滑 390bp；非 IFRS 毛利率 25.3% vs 29.1%（搜尋摘要之轉述，未取得逐字原文）","source":"GlobalFoundries Q4/FY2024 earnings release (6-K)","url":"https://www.sec.gov/Archives/edgar/data/1709048/000170904825000017/globalfoundries4q2024earni.htm","excerpt":null,"as_of":"2025-02-11","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2024 年季度調整後毛利率：Q2 25.2%（年減 440bp）、Q3 24.7%、Q4 25.4%；去庫存壓力來自客戶庫存偏高，Q2 營收年減 12%","source":"Benzinga: GlobalFoundries Exceeds Q2 Projections, Navigates High Inventory Levels In Chip Market","url":"https://www.benzinga.com/news/earnings/24/08/40192110/globalfoundries-exceeds-q2-projections-navigates-high-inventory-levels-in-chip-market","excerpt":"the adjusted gross margin declined by 440 bps to 25.2%","as_of":"2024-08-06","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2024 年 9 月 GFS 股價單月下跌 13.8%，年初至 9 月累計約 -36%，同期 TSMC +73%","source":"Motley Fool: Why GlobalFoundries Stock Fell 14% Last Month","url":"https://www.fool.com/investing/2024/10/04/why-globalfoundries-stock-fell-14-last-month","excerpt":"the stock has slid 36% lower in 2024 while larger rival Taiwan Semiconductor Manufacturing posted a 73% price gain","as_of":"2024-10-04","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#4","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Q4 2024 另認列 9.35 億美元與 Malta, NY 產能相關減損，毛利率收縮、展望低於市場預期","source":"Benzinga: GlobalFoundries Q4 Earnings: Revenue And EPS Beat, Margins Shrink, Revenue Outlook Disappoints Street","url":"https://www.benzinga.com/25/02/43623967/globalfoundries-beats-q4-estimates-margins-shrink-935-million-impairment-charge","excerpt":null,"as_of":"2025-02-11","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#5","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"產業週期長度：TechInsights 統計 1963 年以來 14 次衰退期，平均約每 4.4 年一次；另有分析指 Micron 前兩輪下行持續 7 與 9 季（以 EBITDA 毛利峰谷計，非 GFS 專屬）","source":"TechInsights: The Chip Insider – Cyclical History of the Semiconductor Industry; Seeking Alpha: Micron: How Low Will It Go?","url":"https://www.techinsights.com/blog/chip-insiderr-cyclical-history-semiconductor-industry","excerpt":null,"as_of":"2023-01-01","retrieved_at":"20261012","affects":["thesis.R","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"GF 於 2026-01-14 簽約、2026-06-01 完成收購 Synopsys ARC Processor IP Solutions 業務，對價 $455M（含現金 $440M）。","source":"GLOBALFOUNDRIES Form 6-K (2026-06-30) / MarketScreener","url":"https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000219/gfs-20260630_d2.htm","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261012","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"Bloomberg 報導 GF 探索與聯電（UMC）合併；未見達成協議，報導日期未確認；中國監管核准為障礙。","source":"The Edge Singapore: GlobalFoundries explores merger with Taiwan's UMC","url":"https://alfi.dev.theedgesingapore.com/news/semiconductor/globalfoundries-explores-merger-taiwans-umc","excerpt":null,"as_of":"2025-03-01","retrieved_at":"20261012","affects":["thesis.R","triggers"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 12 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"GFS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":27.14,"operating_margin_pct":11.59,"fcf_margin_pct":11.47,"rd_intensity_pct":8.11},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GFS","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"2330.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.23,"operating_margin_pct":56.1,"fcf_margin_pct":25.33,"rd_intensity_pct":6.07},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"INTC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.6,"operating_margin_pct":7.55,"fcf_margin_pct":4.96,"rd_intensity_pct":23.13},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.INTC","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"005930.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.48,"operating_margin_pct":36.88,"fcf_margin_pct":28.95,"rd_intensity_pct":9.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.005930.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"2303.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":30.6,"operating_margin_pct":20.13,"fcf_margin_pct":23.64,"rd_intensity_pct":7.53},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2303.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"GFS"},"financial_history":{"ticker":"GFS","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":8108000000.0,"revenue_yoy_pct":null,"gross_margin_pct":27.61,"operating_margin_pct":15.55,"net_income":1448000000.0,"diluted_eps":2.62,"free_cash_flow":-435000000.0,"fcf_margin_pct":-5.37,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":7392000000.0,"revenue_yoy_pct":-8.83,"gross_margin_pct":28.42,"operating_margin_pct":16.23,"net_income":1020000000.0,"diluted_eps":1.83,"free_cash_flow":321000000.0,"fcf_margin_pct":4.34,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":6750000000.0,"revenue_yoy_pct":-8.69,"gross_margin_pct":24.46,"operating_margin_pct":10.79,"net_income":-265000000.0,"diluted_eps":-0.48,"free_cash_flow":1097000000.0,"fcf_margin_pct":16.25,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":6791000000.0,"revenue_yoy_pct":0.61,"gross_margin_pct":24.89,"operating_margin_pct":11.74,"net_income":885000000.0,"diluted_eps":1.59,"free_cash_flow":1009000000.0,"fcf_margin_pct":14.86,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GFS/GFS_Q2_2026_Earnings_Call_20260805.md）

# Q2 2026 Earnings Call
2026-08-05

Q2 2026 Earnings Call
GLOBALFOUNDRIES Inc. | Earnings Calls | 2026-08-05
Operator (Operator)
Thank you for standing by, and welcome to the GlobalFoundries Inc. Second Quarter Fiscal Year 2026
Financial Results. [Operator Instructions] As a reminder, today's program is being recorded. And now
I'd like to introduce your host for today's program, Eric Chow, Head of Investor Relations. Please go
ahead, sir.
Eric Chow (Executives)
Thank you, operator. Good morning, everyone, and welcome to GlobalFoundries' Second Quarter 2026
Earnings Call. On the call with me today are Tim Breen, CEO; and Sam Franklin, CFO. A short while
ago, we released GF's second quarter 2026 financial results, which are available on our website at
investors.gf.com, along with today's accompanying slide presentation. This call is being recorded, and a
replay will be made available on our Investor Relations web page.
During this call, we will present both IFRS and non-IFRS financial measures. The most directly
comparable IFRS measures and reconciliations for non-IFRS measures are made available in today's
press release and accompanying slides. Please note that these financial results are unaudited and
subject to change. Certain statements on today's call may be deemed to be forward-looking statements.
Such statements can be identified by terms such as believe, expect, intend, anticipate and may or by the
use of the future tense. You should not place undue reliance on forward-looking statements. Actual
results may differ materially from these forward-looking statements, and we do not undertake any
obligation to update any forward-looking statements we make today.
For more information about factors that may cause actual results to differ materially from forward-
looking statements, please refer to the press release we issued today as well as risks and uncertainties
described in our SEC filings, including in sections under the caption Risk Factors in our annual report
on Form 20-F and in any current reports on Form 6-K furnished with the SEC. In terms of upcoming
events, we will be participating in a fireside chat at the Goldman Sachs Communacopia & Technology
Conference in San Francisco on September 8. We will begin today's call with Tim providing a summary
update on the business environment and technologies, followed by Sam, who will provide details on our
second quarter results and third quarter guidance.
We will then open the call for questions with Tim and Sam. We request that you please limit your
questions to one with one follow-up. I'll now turn the call over to Tim.
Timothy Breen (Executives)
Thank you, Eric, and welcome, everyone, to our second quarter 2026 earnings call. GF delivered strong
results in the second quarter with revenue and non-IFRS profitability metrics at or above the high end
of our guidance ranges. The team continued its rigorous execution, ramping critical technology
corridors where we see accelerating customer demand and the opportunity to create and capture value.
In particular, our comms infrastructure and data center end market delivered over 60% year-over-year
growth in Q2, driven by continued demand for optical networking applications across our silicon

photonics and silicon germanium platforms. This marked one of the fastest quarters of year-over-year
revenue growth for an end market in our company history.
We believe our value proposition has never been more in demand. Our differentiated technology
portfolio and resilient global manufacturing footprint continue to strengthen our position with
customers. We are seeing meaningful momentum as we execute our strategy and drive towards the
long-term targets we shared at this year's Investor Day. Let me now update you on 3 key developments
in the quarter that are accelerating our strategic path: one, Quantum Technology Solutions; two, optical
networking and power opportunities in the AI data center; and three, IP, software, and custom silicon.
Starting with Quantum, a paradigm shift that will define the next chapter of high-performance
computing over the coming decade and beyond. In May, we launched Quantum Technology Solutions, a
new dedicated team and set of capabilities within GF that will enable the quantum industry to move
from prototypes to high-volume production. Just as CPUs, GPUs and AI ASICs define today's compute
paradigm, we believe quantum processor units, or QPUs, will be an essential part of tomorrow's.
Advanced semiconductor manufacturing built securely here in the U.S. will be essential for the scaling
of this technology. Establishing the right production capability is now the critical enabler. The ability to
manufacture and integrate complex quantum devices with consistency, yield and scale.
This is precisely where GF wins. Our Quantum strategy is Qubit-Agnostic, meaning our manufacturing
platforms are expected to support a broad range of leading modalities, including superconducting,
trapped ion, photonic, topological and spin. Our proven platforms like FDX provide the cryogenic
CMOS foundation, and we are extending our advanced packaging capabilities into the cryogenic regime
to enable the 3D heterogeneous integration that these systems require. As highlighted in our recent
announcements, we are working closely with 8 of the world's leading quantum computing players,
including partnerships with PsiQuantum, Quantinuum and Quantum Motion as well as new
endorsements from the quantum arms of large hyperscalers. Since launching just 3 months ago, we
have already embarked on 4 new customer-specific quantum engagements with accelerating
commercial momentum ahead.
Advancing our quantum capabilities is anchored by an expected $375 million grant from the U.S.
Department of Commerce to accelerate the research, development and build-out of quantum
manufacturing capacity in the U.S. This critical partnership with the U.S. government underscores why
Quantum is not only a business opportunity, but also a national priority. We are only in the early stages
of the nascent quantum opportunity. Over the next 1 to 3 years, we expect to generate quantum-related
revenue largely through engineering engagements with customers reported within our technology
services revenue. As customer platforms qualify and move into volume production, we expect
quantum-related revenue from manufacturing services to ramp towards the end of the decade.
Ultimately, our early momentum and customer proof points in this emerging area perfectly encapsulate
the outsized value GF provides a strongly differentiated technology, deep customer partnerships and a
global secure manufacturing footprint.
Let me turn to AI data center, where we continue to build momentum through new customer design
wins and increasing engagement across the ecosystem. In the second quarter alone, we secured 7 new
optical networking design wins with customers across both pluggable transceiver suppliers as well as
major hyperscaler and networking players. Silicon photonics and silicon germanium each play critical
roles in optical networking systems and combined with data center power represent 3 high-quality

long-term secular growth drivers, which underscore our conviction in the ability to grow in the data
center for years to come. I will walk through an update on each of these.
For silicon photonics, let's start with pluggables, which contributes the vast majority of our silicon
photonics revenue today. Thanks to our differentiated technology and advanced 300-millimeter
photonics manufacturing footprint, we are actively engaged with 4 of the top 5 optical transceiver
players. Given our strong capabilities and robust capacity ramp, we now expect our silicon photonics
revenue as reported within the comms infrastructure and data center end market to more than double
in 2026 compared with the year prior. Beyond just this year, we are progressing well on our multiyear
road map to advance the enablement of modules delivering 1.6T, 3.2T and beyond. High-volume
manufacturing of our 200-gig per lane technology is underway.
We have already demonstrated 400-gig capability and solutions for even greater bandwidth are in
development. In addition to our robust pluggable offerings today, we see significant customer interest
in our SCALE platform, the industry's first OCI MSA compatible solution for near and co-packaged
optics. We currently have 7 active engagements with leading companies on our SCALE platform and
customer feedback on the merits of our technology and manufacturing capabilities has been very
positive. We are already delivering tangible results for our customers today, having taped out a SCALE-
related design win in Q2, and we expect to tape out another in Q3. Specifically for near-packaged
optics, we see NPO as an important application and exciting opportunity ahead of the broader adoption
of co-packaged solutions. Because near and co-packaged optics are built on a common photonic IC and
because many components of GF SCALE solution support both near and co-packaged optics, our
customers benefit from the same underlying platform.
As a result, we expect GF to benefit from the silicon photonics opportunity regardless of the rate and
pace of various form factor adoptions by our customers. As we increase investments into our silicon
photonics capabilities, the importance of government partnerships continues to grow. Last week, GF
entered into a letter of intent with the U.S. Department of Commerce for a $300 million award to
accelerate the development of next-generation silicon photonics technologies in the U.S.
The funding will support advanced optical materials, modulated technologies and packaging
innovations that will enable next-generation near and co-packaged optics architectures, building
directly on GF SCALE platform. The endorsement from our partners across the industry has reinforced
our strategic conviction, including the world's top XPU providers, hyperscalers, AI connectivity leaders
and ecosystem partners. We are pleased to take a central role in advancing optical innovation and
development in the U.S. and believe this recognition validates the strategic importance of silicon
photonics, the excellent relationship we enjoy with our partners and GF leadership in these
technologies.
Another driver of data center momentum is high-performance silicon germanium, which powers the
analog and mixed signal electronics at the heart of optical interconnects for AI and cloud infrastructure.
Our differentiated SiGe platform delivers the bandwidth, signal integrity and power efficiency required
for increasingly demanding optical networking applications, making it strongly complementary to our
silicon photonics portfolio. During the quarter, we secured multiple new SiGe TIA and driver design
wins across networking customers. Demand for SiGe remains strong, and we are oversubscribed
throughout 2027. We are actively expanding capacity in our Vermont facility to support this demand.
We believe SiGe represents another key growth opportunity for GF.

Combined with our leadership in silicon photonics, GF offers a uniquely differentiated set of
technologies that help address the bandwidth, power efficiency and signal integrity requirements of
next-generation AI systems. The momentum we are seeing today reinforces our belief that we will be a
key leader in optical networking for years to come. The third strong opportunity we see in the AI data
center relates to power. In July, we closed a strategic acquihire of the custom power team from Photon
Technologies in Europe, bringing an experienced design team focused on integrated voltage regulators,
or IVRs. Together with our BCD, GaN and integrated inductor capabilities, IVR further strengthens our
road map depth in power technologies and expands our serviceable market in one of the fastest-
growing opportunities within AI data centers.
Our goal is to help enable a new power architecture for AI infrastructure, one that brings power
conversion closer to the processor and addresses the increasing efficiency, power density, bandwidth,
high current and transient response requirements of next-generation XPUs. As AI workloads continue
to scale, XPUs are consuming more power than ever before, increasing the need for solutions that can
reduce power losses and deliver higher performance within increasingly constrained thermal and
physical footprints. Closed in Q2, this transaction brings new differentiated IVR technology specialized
engineering talent and additional R&D capabilities that strongly complement our power portfolio,
allowing us to capture a larger share of the growing power opportunity in AI data centers.
Finally, moving to another key element of our long-term strategy, our IP, software, and custom silicon
capabilities. In June, we completed our previously announced acquisition of Synopsys ARC processor
IP Solutions business, an important milestone in advancing our strategy in physical AI and a notable
step change in expanding GF's serviceable addressable market. As a recap, the strategic rationale is
multifold. As AI increasingly moves beyond the data center into the physical world around us, it is
transforming automotive, industrial automation, robotics and intelligent edge devices. In that context,
customers are looking for partners that can help them navigate the growing complexity of software,
compute architectures and semiconductor design.
Together with MIPS, this acquisition bolsters GF's capabilities across RISC-V processor IP, software
development tools and custom silicon design, enabling us to support customers from architecture and
software through high-volume silicon production. We acquired a broad set of CPU, DSP, NPU and
broader RISC-V technologies as well as a proven software development toolkit and application-specific
processor design capabilities. With over 150 patents, 300 existing customers and 400 R&D engineers
around the world, this acquisition meaningfully expands our ecosystem reach and depth. Importantly,
we are already seeing significant strategic benefits from our acquisition. By combining MIPS and
Synopsys ARC under one roof, we are engaging with more customers earlier in the design cycle,
shaping application-specific compute architectures and creating deeper, longer-lasting customer
partnerships.
To accelerate customer enablement, we are increasing investment in a number of R&D initiatives.
These are focused high-return programs that position us to capitalize on expanding opportunities while
helping our customers innovate faster. Over time, we believe this creates a pathway to greater custom
silicon opportunities and enabling physical AI customers to run their AI inference workloads on GF and
MIPS-based processing platforms. In summary, we made meaningful progress across several strategic
growth areas this quarter.

We delivered a record quarter for design wins across both communications infrastructure and data
center and smart mobile devices in differentiated areas such as display backplanes for AI glasses,
PMICs for premium smartphones and smart power stage gate drivers for data center power. Our
differentiated capabilities are helping customers solve increasingly complex challenges while
positioning GF as a trusted technology partner. We are making critical investments and integrating
strategic acquisitions that strengthen our competitive position, diversify our growth drivers and
provide a durable foundation for long-term profitable growth. I am proud of the team's diligent
execution this quarter and excited about the opportunities ahead.
I'll now pass the call over to Sam for a deeper dive on second quarter 2026 financials.
Sam Franklin (Executives)
Thank you, Tim. For the remainder of the call, including guidance other than revenue, cash flow and
net interest income, I will reference non-IFRS metrics. GF delivered strong results in the second
quarter with revenue and non-IFRS gross margin exceeding the high end of our guidance ranges.
Thanks to the efforts from our teams around the world to improve structural costs, raise manufacturing
productivity and accelerate growth in value-accretive secular end markets, we grew our gross margin by
nearly 500 basis points year-over-year.
Not only did this represent a second quarter record, we delivered on our expectation to reach
approximately 30% gross margin well before the end of 2026 driven by a richer mix of revenue, this
quarter's results demonstrated a meaningful step towards our long-term objectives to achieve. Now on
to the results. We delivered second quarter revenue of $1.786 billion, up 9% sequentially and 6% year-
over-year. We shipped approximately 625,000 300-millimeter equivalent wafers in the quarter, up 8%
sequentially and 8% from the prior year period. Revenue from manufacturing services accounted for
approximately 89% of total revenue.
Revenue from technology services, which includes revenue from IP, licensing, software, reticles,
nonrecurring engineering, expedite fees and other items, accounted for approximately 11% of total
revenue for the second quarter. Following the acquisitions of MIPS and the Synopsys IP business, we
expect revenue contribution of approximately $100 million to $120 million towards our full year 2026
technology services revenue, up from our prior expectation of $60 million to $100 million as these
acquisitions continue to drive new opportunities with our customers. In addition, driven by strong
conversion of our design win pipeline and an expanding scope of partnerships with customers, we
expect sustained momentum in our revenue contribution from technology services. As a result, we
expect technology services revenue towards the high end of the 10% to 12% range of total revenue in
2026 with a gross margin profile significantly higher than our corporate targets.
Let me now provide an update on our revenue and outlook by end market. Communications
infrastructure and data center represented approximately 16% of second quarter total revenue.
Revenue increased 20% sequentially and 62% year-over-year. This marked the seventh consecutive
quarter of double-digit percentage year-over-year growth for communications infrastructure and data
center and the fastest quarterly year-on-year growth since 2022. Within this end market, we saw strong
customer demand for our silicon photonics and silicon germanium offerings. In both of these high-
margin technologies, we're ramping capacity and making the necessary investments to unlock increases
in demand indicated by our customers.

Beyond optical networking, we saw strong double-digit year-over-year growth in applications across
both wireless and -- Given the accelerating demand outlook from our customers, we now expect to
achieve full year 2026 revenue growth in the range of 50% to 60% for our communications
infrastructure and data center end market, up from our prior expectations of high 30s percentage year-
over-year growth, which we believe is an early indication of the long-term growth opportunities ahead
for GF in this end market. Beyond the growth opportunities across silicon photonics and SiGe outlined
by Tim, we also closed a first-of-a-kind design win for smart power stage gate drivers on our BCD
platform.
We see this as just one notable step forward in the rapidly evolving market for data center power
applications. Automotive represented approximately 19% of second quarter total revenue. Automotive
revenue decreased 13% sequentially and 10% year-over-year, principally driven by customer-led
shipment timings. However, for the full year, we continue to expect low double-digit percentage
revenue growth for our automotive end market with a higher weighting towards the fourth quarter. As
automotive semiconductor content continues to grow, we're encouraged by our design win momentum
with customers and the long-term growth opportunities these present. In the second quarter, we
secured a significant automotive power design win for 5-volt and 10-volt power management integrated
circuits built on our BCD platform. In addition, we also taped out an ADAS radar built on our FDX
platform for Bosch, a notable milestone and the culmination of years of close partnership.
These highlights reflect the strong momentum we continue to see across automotive power, processing,
sensing and safety applications. Smart mobile devices represented approximately 36% of second
quarter total revenue. Revenue increased 15% sequentially and decreased 6% from the prior year
period. As noted by peers and customers across the industry, 2026 smart mobile handset forecasts have
reduced meaningfully over the last quarter, principally due to the continued impact from memory
pricing and associated shortages. As a result, we currently expect smart mobile devices to decline by a
low teens percentage year-over-year in 2026. Customer design win momentum for new generations of
smart mobile devices continues to be positive.
In the second quarter, we secured a notable design win on GF's BCD platform with MediaTek, further
validating our expanding power platform. This marked GF's first-ever power management integrated
circuit design win with our long-standing customer. In addition, we continue to strengthen our position
with next-generation augmented reality wearables at a leading hyperscaler, winning a new design for
microLED display backplanes. Finally, home and industrial IoT represented approximately 19% of
second quarter total revenue. Revenue increased 30% sequentially and 10% year-over-year. In the
second quarter, IoT revenue growth marked the fastest year-over-year growth since 2022, driven by a
breadth of demand for applications across AI-enabled image processing, health care wearables and
next-generation MCUs for edge AI compute.
As inventory normalizes, customer demand signals improve and the next generation of production
ramps commence in the second half of the year, we expect our revenue for the home and industrial IoT
end market to grow in the range of 10% to 15% in 2026, up notably from our prior expectations for mid-
single-digit percentage growth. In the second quarter, we secured 3 strategic chiplet design wins with
Lockheed Martin on our FinFET and FDX platforms, creating a foundational aerospace and defense
chiplet ecosystem that further extends GF leadership as a trusted U.S. foundry. We also expanded our
relationship with Microchip with a meaningful design win on our FinFET platform, another notable
proof point for the growth of our embedded compute and edge AI offerings.

Moving now to other key financial performance metrics in the quarter. In the second quarter, we
delivered gross profit of $534 million, which translates into approximately 29.9% gross margin, above
the high end of the guidance range and up 470 basis points year-over-year. A richer mix of
manufacturing and technology services revenue, structural improvements in manufacturing costs and
improved utilization all contributed to favorable year-over-year margin expansion. R&D for the quarter
was $144 million and SG&A was $92 million. Total operating expenses of $236 million were up 16%
quarter-over-quarter and represented approximately 13% of total revenue.
We delivered operating profit of $298 million for the quarter at an operating margin of 16.7%, above
the midpoint of our guided range and up 140 basis points from the prior year period. Second quarter
net interest income was $9 million. Other expense was $12 million, and we incurred tax expense of $39
million in the quarter. We delivered second quarter net income of approximately $256 million, an
increase of approximately $22 million from the prior year period. Diluted earnings of $0.46 per share
was at the high end of the guidance range based on a fully diluted share count of approximately 556
million shares. Let me now provide some key cash flow and balance sheet metrics.
Cash flow from operations in the second quarter was $405 million. Second quarter CapEx, net of
proceeds from government grants was $408 million or roughly 23% of revenue. Adjusted free cash flow
for the quarter was negative $3 million as indicated in our prior quarter's guidance. At the end of the
second quarter, our combined total of cash, cash equivalents and marketable securities stood at
approximately $3.3 billion. Our total debt was $1.1 billion, and we also have a $1 billion revolving credit
facility, which remains undrawn. On July 14, we paid GF's first-ever quarterly cash dividend of $0.12
per share, an important milestone that reflects both the progress we have made in strengthening the
business and our confidence in its future cash generating capacity.
Supported by a strong balance sheet and disciplined capital allocation framework, we remain
committed to investing in profitable growth while returning excess cash to shareholders. As outlined at
our Investor Day, our objective is to return up to 50% of trailing 12-month non-IFRS adjusted free cash
flow after investments through a combination of dividends and share repurchases over time. Pursuant
to this strategic objective, I'm pleased to announce that our Board of Directors approved a quarterly
cash dividend of $0.12 per share payable on October 9, 2026, to shareholders of record as of September
23, 2026. In addition, approximately $100 million remains under the share repurchase authorization
approved by our Board of Directors, and we expect to be flexible with the deployment of the remaining
authorized amount.
Next let me provide you with our outlook for the third quarter of 2026. We expect total GF revenue to
be $1.885 billion, plus or minus $25 million. We expect gross margin to be approximately 30.5%, plus
or minus 100 basis points, which at the midpoint reflects approximately 450 basis points of year-over-
year expansion. Excluding share-based compensation, we expect total operating expenses to be $260
million, plus or minus $10 million. We expect operating margin in the range of 16.7%, plus or minus
170 basis points. At the midpoint of our guidance, we expect share-based compensation to be
approximately $76 million, of which roughly $18 million is related to cost of goods sold. We expect net
interest and other income for the quarter to be between $3 million and $11 million and income tax
expense to be between $28 million and $52 million.
Based on a fully diluted share count of approximately 556 million shares, we expect diluted earnings
per share for the third quarter to be $0.51, plus or minus $0.05. Now let me provide an update on some

broader financial drivers as we evolve the mix of our business and aim to deliver the growth model set
out at our recent Investor Day. With respect to pricing, we're encouraged by the improving industry
dynamics as well as the evolving mix of our business towards highly accretive technologies. In addition
to these positive mix shifts in the second quarter, we implemented pricing increases in partnership with
our customers across several technology corridors. Following the satisfactory conclusion of these
customer conversations, we expect the pricing adjustments to be reflected in revenue commencing in
2027.
The magnitude of these pricing increases varies by end market and technology and contemplates the
differentiated value we provide, the ongoing supply and demand dynamics and the inflationary
absorption across our industry in recent years. Conversations with our customers have been very
constructive, and we'll continue to assess pricing for 2027 through the second half of 2026. With
respect to operating expenses, consistent with the strategic updates we set out at our Investor Day in
May, we believe that R&D will rise as a percentage of revenue as we integrate recent acquisitions and
accelerate our R&D capabilities to support key growth opportunities.
We've strengthened our portfolio capabilities through the acquisitions of the Synopsys ARC IP business
in June as well as the IVR business from Photon Technologies in early July, adding critical R&D, IP and
engineering resources. Following these acquisitions, we now expect quarterly operating expenses in the
second half of 2026 to be consistent with our third quarter guidance as we accelerate critical R&D
investments while ramping talent and capabilities intended to support key growth opportunities across
the AI data center, physical AI, quantum computing and advanced packaging.
These timely and necessary investments are targeted to accelerate our technology road map, deepen
our customer engagements and expand future growth opportunities in the years ahead. Moving now to
tax, where we expect an effective tax rate in the mid-teens percentage range for the full year of 2026,
principally due to the expected geographical mix of wafers shipped in the second half of this year.
Finally, for the full year 2026, we continue to expect an adjusted free cash flow margin of
approximately 10%. In conclusion, I'd like to thank our global teams for their continued commitment
and diligent execution towards our strategic goals.
GF drove another quarter of meaningful year-over-year margin expansion and achieved new second
quarter records across a range of growth and profitability metrics. Our strategic initiatives and
investments executed over the last year are demonstrating good momentum across the end markets
that we serve and the continued mix shift in our business is driving improved diversification across our
end market portfolio. Looking ahead, we intend to continue executing towards a richer mix of business,
targeting continued structural cost improvements and improved manufacturing productivity, all of
which we believe are forming a strong foundation for increasing shareholder value in the years ahead.
With that, let's open the call to Q&A. Operator?
Operator (Operator)
And our first question comes from the line of Chris Caso from Wolfe Research.
Christopher Caso (Analysts)
I guess the first question is about the comms data center growth and some of the capacity expansion
that's occurring in that segment. And I know while it's growing strongly, you're capacity constrained.
Can you help us with to the extent you can, timing and magnitude of that capacity expansion?

When does the additional capacity come online? And I did also notice that you received, I think it was a
$300 million CHIPS Act grant for the silicon photonics expansion. Can you speak to how that helps to
defray some of the net CapEx for that?
Timothy Breen (Executives)
Yes. Thank you, Chris. So I'll kick us off on that. So in terms of capacity, as you say, demand has been
strengthening across basically all data center applications. We're feeling that very strongly in the optical
networking space that particularly pulls on silicon photonics and silicon germanium. But we're also
seeing it in other parts of the business starting to pick up, including areas like power. So our strategy
will be to add capacity in those areas. One advantage for us is we're building that capacity out within
our existing fab footprint, and we have, let's say, ample fab footprint today to ramp capacity relatively
quickly. By the way, one of the contributors to us upping our full year view about our CID end market is
actually our confidence about bringing that capacity on and driving factory level productivity
improvements to be able to get basically wafers out through the back half of this year and even further
into 2027.
So we feel good about the ability to meet that growth with additional capacity expansion. Maybe I'll
turn to the $300 million partnership with the U.S. government. We couldn't be more excited about this.
I think it's really important to bear in mind that the shift to optical networking is very much a secular
shift, and we see this only at the very early innings of penetrating the data center. We've spoken in the
past about 70% of data center links being optical by 2030. I think every piece of evidence today points
to that being perhaps even conservative relative to what's happening, including the penetration, not
just to scale out, but also scale-up networking. And so look, we're very excited about the prospects of
optical networking and within that silicon photonics. But a lot of what that will require is higher
performance technologies in the future. And so what we announced really has 3 components:
continuous innovation at the PIC level, right, so improved modulated technology so we can go to 400-
gig per lane and beyond.
New materials. At some point, we will introduce new materials into the system. Think about barium
titanate, thin film lithium niobate, think about indium phosphide, all areas of technological innovation
to produce higher-performing systems and more integrated systems going forward. And then the last
piece, which is extraordinarily important, particularly for near and co-packaged optics is packaging.
And so being able to build those integrated optical engines for both those applications using our SCALE
solution also requires continued capability and capacity. So that partnership allows us to accelerate
that, and we're very grateful to have the U.S. government as a strong, let's say, partner in our corner
supporting that innovation happen right here in the U.S.
Sam Franklin (Executives)
Do you have a follow-up question?
Christopher Caso (Analysts)
I do. A follow-up, I'll ask on gross margins. And can you speak to what's the driver of the gross margin
expansion as you go into the third quarter in terms of utilization mix and pricing and perhaps give us
some color on the trajectory of gross margins into next year, particularly in light of some of your
comments with regard to pricing?

Sam Franklin (Executives)
Yes, very happy to, Chris. And look, I will start by saying that we're very encouraged by the continued
progression and expansion in our gross margins. And I think it's a continued reflection of the progress
that we've seen during the course of this year. We had almost 500 basis points of margin expansion in
the second quarter. We had over 500 basis points of margin expansion in the first quarter. And as I said
in my prepared remarks, if you take the midpoint of our inferred guide, that implies about another 450
basis points of margin expansion. So this is really playing to the thesis and the levers that we discussed
at our Investor Day just a couple of months ago now.
And frankly, it's falling through on a relatively healthy basis when you look at the revenue. Take
revenue a year ago and compare it to the same period this year, about $100 million of revenue growth.
Look at that adjusted gross profit and you see about $100 million of gross profit falling through as well.
So we're very encouraged by that relative fall-through to the underlying gross margins as it relates to
our revenue growth. And you sort of touched on it a little bit in your question, Chris. Mix has been a big
and continues to be a big driver of that. And the way to think about mix is twofold. It's mix from a
manufacturing services point of view, and it's mix from a technology services point of view as well.
Both of those have been encouraging tailwinds for us, particularly when you look at the relative
strength and growth within some of those end markets, which I touched on around comms infra and
data center being highly accretive to those targets. You take our technology services revenue up a little
under $40 million year-over-year. That's about a point of benefit that comes through there. So the
combination of the mix across manufacturing and technology services has been encouraging. We expect
that to continue. As I said previously, productivity within our manufacturing sites and driving
structural cost improvements has been a big driver as well. Utilization, we were in the second quarter
sort of high 80s from a utilization point of view.
So we still feel we've got a good amount of our existing capacity to be able to grow into and see positive
margin movements over time. And frankly, all of that is against some of the benefits we had in the year
ago period. We had things like liquidated damages in early 2025, which have fallen out. So again, it sort
of reflects the strong growth we've seen from a margin point of view. We bumped up on that 30% target
margin that we said we were looking to solve for at the exit of 2026 in our second quarter, we're above
that in the third quarter guidance. So expectation now for the full year is that we should be at about 30
points of gross margin for the full year rather than just that exit target that we had at the beginning of
the year. I hope that helps, Chris.
Operator (Operator)
And our next question comes from the line of Krish Sankar from TD Cowen.
Sreekrishnan Sankarnarayanan (Analysts)
Congrats on nice results. I just wanted to first follow up on the silicon photonics CID year-over-year
growth, almost doubling from your prior outlook. I'm just kind of curious what changed in the last 3
months that the outlook has been revised almost materially higher? And any color you can give on your
PIC solutions compared to your two competing foundries? Then I had a quick follow-up on Quantum,
too.
Timothy Breen (Executives)

Yes. Great. Thank you very much, Krish. Look, photonics remains a very strong driver for us. I think
every customer meeting is all about what more can we do, how much faster can we go. There is clearly
strong demand today. And by the way, in a market like this, we don't just validate that demand with our
direct customers. We spend time throughout the ecosystem, including with the big hyperscalers, and
you've seen many of them are supporting a lot of what we're doing here in the U.S. and around the
world. So we're validating the demand, and we believe it's very real today and durable going forward.
That's giving us confidence to continue to invest. We'll increase our investments in photonics capacity.
And as I mentioned earlier, there's nothing our factories love more than being challenged to get more
output literally every single week. We're calling in from Malta, New York, right now, and the factory is
hard at work producing more wafers every day for these oversold corridors. So I think very strong
conviction about continuing to grow silicon photonics. But yet, we're still at the very beginning of this
and that those growth targets we set for kind of end of '28 and through 2030, I'd say today, we are very
much on track and potentially ahead of those targets in terms of our silicon photonics growth.
Sreekrishnan Sankarnarayanan (Analysts)
Got it. Very helpful, Tim. And then a quick follow-up on Quantum. You recently got a $375 million
grant. Can you talk a little bit about the opportunity set there? And where are we in the Quantum
commercialization curve? And have you seen more interest or share gains given IonQ just recently
closed acquisition of SkyWater?
Timothy Breen (Executives)
Yes. So thank you for that question. I mean Quantum is extremely exciting, and there's a few reasons
behind that. I think one is talking to now basically all the players in the sector, everyone is facing the
same kind of transition. This is not a, can I prove it in a lab discussion? This is can I scale to high-
volume manufacturing. And so the conversations we have and in our announcement, we had both
dedicated quantum players, but also hyperscalers and others comment and support that initiative.
The conversations are similar because it's all about transitioning to that high-volume scale and cracking
different problems that they've proven at lab scale, but need to prove now as they transition to high
volume. Since that announcement, we've launched 4 significant new engagements with some -- a subset
of the players that are supporting us in that announcement, and we see that ramp continuing. Those
engagements have some common features.
For example, some of the stuff we're doing around cryogenic CMOS for readout ICs for different
modalities. That's very exciting because it builds on existing platforms that we have. But also there are
those who have very specific requirements. And that's where also I'm quite excited about the technology
benefits of us investing in Quantum. And so I'll give you an example, a couple of -- actually more than
2, 3 or 4 players are doing things linked to the photonics side in their quantum solution. That has
excellent read across for us in our long-term silicon photonics road map. So think of that as very
synergetic with what we're doing in that space.
And so Quantum is actually reinvigorating a number of our long-term technology road maps even
further and faster than otherwise it would be happening. So that's very positive. As Sam mentioned in
the prepared remarks, we'll see the financial profile of Quantum in our technology services revenue this
year and definitely into next year. Think of it more medium term as a kind of call option on the scale to
high-volume module manufacturing. Too early to call exactly when those ramps will happen. But

clearly, that is the objective of these players that are engaging with us is develop and crack the solutions
and then scale them to high volume together.
Operator (Operator)
And our next question comes from the line of Karl Ackerman from BNP Paribas.
Karl Ackerman (Analysts)
Two, if I may. Tim, you spoke about the 3 pillars of growth, including Photonics, Quantum, IP and
custom silicon. But could you speak to the revenue and OpEx contribution of the ARC and Photon
Technologies IVR team in the September outlook? And also, if you zoom out, could you double-click on
the rationale for these deals and maybe any early customer design engagements you've seen to date?
Timothy Breen (Executives)
Yes. So let's -- I'll talk about rationale, and then I'll let Sam comment on how we're thinking about
revenue for this year. So we've been very focused in our acquisition strategy on identifying capabilities
that our customers value, and that links to our manufacturing road map, but also links to what they tell
us around gaps that the industry today is not meeting. So let me take kind of the MIPS and Synopsys
story first, and I'll come back to Photon, both very exciting in their own ways. Customer feedback on
MIPS and then ARC has been excellent. I spent a lot of time personally with customers, especially since
we've closed the ARC deal. And by the way, with that came 300 customers. Some of those were not GF
customers before.
So it gives us also new customers to engage with on those road maps. And these are very strategic
discussions because these are about future architectures for their processor solutions. How can they
add AI at the edge? How can they do on-device inference in the automotive space, the industrial space,
the robotics space. And so it's bringing some really interesting discussions to bear. And it allows us as
GF to engage much earlier in that design conversation than we would if it was just a conversation about
manufacturing capacity and manufacturing process technology. It has another benefit, which is that it's
also giving us very, very early input into our manufacturing road map.
And so now you have this, let's say, symbiosis internally that we have an internal customer for what
we're doing that is actually challenging us to push performance of next-generation technologies,
particularly in our CMOS business to the next level. So you're thinking about how do you do lower
power inference at the edge and so on. So I'd say early, of course, for both of these, but very
encouraging. We've talked about some of the early wins and partnerships in spaces like defense with
Lockheed Martin in automotive with players like Infineon, but there are many, many more in the
pipeline. So very encouraging for our IP software and custom silicon strategy. To talk briefly about IVR
and Photon, we've had the chance to work with the Photon team for many years now as the IVR
category has started to become more and more important.
The way you should think about that is IVR is to power, what CPO is to photonics, right? Think about
how do you build a much more wafer-level integrated solution to deliver power closer to the chip and to
be able to do things that today exist in much more kind of traditional power modules, much more like
the industrial and automotive power modules of today. This is moving to a much more kind of, let's say,
wafer level solution that is higher and higher performance. That is essential for next-generation data
center power, given how hungry these XPUs, GPUs, CPUs are all for power. Photon team, very engaged

with a number of our existing customers. So it's a very natural transition to bring that team on board,
accelerate those engagements. And again, early feedback from the likes of existing kind of fabless and
IDMs, but also hyperscalers who are engaged there, very, very positive bringing that capability into GF.
Sam Franklin (Executives)
And Karl, maybe if I just jump on the second part of your question as it relates to some of the financial
profile. And for all the reasons that Tim outlined, these investments are incremental, they're strategic.
And actually, in the case of the MIPS acquisition as well as the ARC IP business from Synopsys, they are
revenue generative from day 1. At the outset of this year, we expected that we'd be seeing about $60
million to $100 million of incremental revenue through from that MIPS acquisition during the course
of 2026. That remains the expectation. But what's changed over the course of the last quarter is that we
closed the acquisition of the Synopsys ARC IP business.
So the midpoint of that range, as you can kind of infer from my prepared remarks, has moved up from
$60 million to $100 million to $100 million to $120 million, call it, $30 million of revenue growth. Our
expectation in terms of the skew of that incremental revenue from that recent acquisition is sort of 1/3,
2/3 skewed from third quarter and fourth quarter perspective. As it relates to the R&D and the fall-
through ultimately through to EPS, look, these are R&D-intensive businesses. They're also highly
accretive from a gross margin point of view. Overall, we expect that the increase in OpEx and
particularly the acceleration from an R&D point of view to largely be covered by that incremental
revenue we see coming through from both of those acquisitions. So we feel quite good about it from
that perspective.
Karl Ackerman (Analysts)
Very clear. For my follow-up, if I may, could you discuss what portion of those 7 customers on your
SCALE platform are working on NPO or near-packaged optics -- and I guess how should we think about
the timing of your NPO opportunity?
Timothy Breen (Executives)
Yes. Maybe just to take a step back, and I think there's obviously a year ago, the industry wasn't talking
a lot about NPO -- now it's talking a lot about it. I think the reason is that you see a comfort level for a
number of players moving from, let's say, traditional pluggable infrastructure to NPO, and that's
because they have synergies in terms of things like the SerDes. So the system is, let's say, a smaller
transition versus moving to the full co-package optics. We think both those form factors as well as
pluggables will continue to exist in the data center. Obviously, as you get more into scale-up
networking, that's where you need to move to smaller form factors like NPO and CPO and to really
address all of those linkages within a scale-up network. So we think all of those will continue to exist.
Scale supports NPO and CPO. So a lot of the dimensions that go into putting a SCALE solution
together, an EIC bonded to a PIC with a micro-optic with a fiber attached unit are necessary for both
NPO and for CPO. Fundamentally, the mechanical difference is that the NPO is bonded to the board,
whereas the CPO sits within the package, right? And there are differences, therefore, to, let's say, more
the things like the SerDes architecture, as I mentioned, but less to the mechanics of how things are
done. So look, we see very good momentum on NPO. I'd say the scale engagements we have cut across

both. And actually, I'd say even many of the customers are doing both because they have both an NPO
that they're ramping sooner and a CPO that they're ramping a little bit later.
We still maintain the view that '27 we will see the beginning of NPO ramp and '28, we'll see the
beginning of CPO ramp, and that's been quite consistent over the last few quarters.
Operator (Operator)
And our next question comes from the line of Mehdi Hosseini from Susquehanna International Group.
Mehdi Hosseini (Analysts)
I also have a couple of follow-ups on comm infrastructure. Tim, can you help me understand what is
the contribution of SiGe into your overall optical revenue mix? And as we migrate to NPO and
assuming the PIC itself becomes a catalyst, to what extent should I expect some synergy between the
SiPho and SiGe? And I do have a follow-up.
Timothy Breen (Executives)
Yes, it's a great question. And let me talk about SiGe just for a little bit since you picked it out. Just to
wind the clock back, right, how do we have such an important position in SiGe? IBM Microelectronics, I
think, is on record for inventing SiGe. IBM Microelectronics is part of GF today. And so we've had team
members building SiGe solutions for a long time now. And so that's always been an important part of
our portfolio. What you're seeing in SiGe is that the acceleration is driven by, let's say, 2 trends
happening at the same time. One is the shift to optical networking means you are moving more data
through a different kind of link.
But as you push to higher and higher bandwidth, what you could do previously in CMOS at, say, 50 gig
per lane, 100 gig per lane at 200 gig per lane and definitely at 400 gig per lane, you cannot do. And so
what we're seeing is people are breaking out those TIAs, those transimpedance amplifiers and also
incrementally also breaking out the drivers and doing them in high-performance analog solutions like
SiGe. And so in a way, what we're seeing in our SiGe business is actually growth driven by both the
switch to optical, but also the increased bandwidth requirements within those optical solutions.
That's driving significant growth within the space. Just to give you a dimension, our SiGe business is
actually larger than our silicon photonics business today. So it's actually a meaningful part of our data
center business overall. And like silicon photonics has very strong growth trajectories because it serves
the same underlying trend and perhaps with even that multiplier effect playing out even more so as
we're expanding the performance of those pluggable technologies. You'll also find high-performance
analog solutions in near and co-packaged optics as well. So those will also have components of those
depending on the architecture. Our SiGe solutions, we build them today in Burlington, Vermont. We're
expanding capacity there. That's part of what is also increasing our output within '26 and definitely into
'27. But we're also qualifying 300-millimeter SiGe in Singapore, which will bring additional capacity,
the economics of 300-millimeter, which obviously is very good, but also higher performance.
And so as you move to new platforms, you improve your fT, your fMAX performance. And so we think
we can continue that great tradition started by IBM of leading the industry in terms of our SiGe
solutions for the market.
Mehdi Hosseini (Analysts)

Okay. Great. I feel like we can spend an hour just focusing on optical, but I'm going to move on. Within
the comm infrastructure, there's also satellite comm and SpaceX had their first quarterly call last night.
So help us understand, right now, we're just focused on a transceiver and optical solution. But I see
there's also a synergy. So what kind of a substrate is used for satellite comm? And remind us on Analyst
Day, how satellite comm could also drive double-digit growth here. Hopefully, I'm in line with my
assumptions.
Timothy Breen (Executives)
Yes. So SATCOM, look, continues to be a strong growth business for us. And the reasons for that, I
think, are fairly clear. The transition to LEO deployment really driven by SpaceX originally and a couple
of other players now ramping as well. It's very clear to see. And as a consumer, once you take a flight
and you Starlink on the flight, you kind of don't want to go back to how it used to be. So I think it's clear
why those solutions are taking effect. Remember, you're beaming a signal 300 miles into space, a signal
that normally would have gone 2 or 3 miles to a base station or a cell tower. And so you need higher
performance RF, you need beam forming, you need other kind of wireless technologies -- these are very
core strength areas for GF. Some of those technologies are in SOI today.
Some of them have SOI-like characteristics but are done without SOI as well. And we're seeing more
and more trajectory of new RF technologies playing into SATCOM going forward. Even areas like RF
GaN, we think will play a very important role in SATCOM going forward because you're not just
increasing the number of units deployed, but you're talking about faster and faster bandwidth. And by
the way, this is not just for consumers, you're hearing about industrial deployment, corporate
deployment and so on. And there, I say, when you put data centers in space, you're going to need a lot
more bandwidth to bring that capability back to Earth for people to use. So I think very strong secular
driver of growth for us. Obviously, we're starting from a relatively small base compared to other
markets, given this is relatively new, but we definitely see it growing very well long term.
Operator (Operator)
And our next question comes from the line of Timothy Arcuri from UBS.
Timothy Arcuri (Analysts)
So Sam, I had a multipart question. So the segment guidance implies like December is up sort of in the
10% range. So my question is, a, is that right? And then can you give us any sense for September of how
the guidance shakes out by segment, even if you just give qualitative comments on that?
Sam Franklin (Executives)
Yes. Happy to, Tim. And look, you're right in terms of your overall inference. We said that certainly for
the remaining part of this year, just given some of the dynamics around mobile, we think that's sort of
down low teens for the full year. Meanwhile, automotive, despite having a slight softer in 2Q, that was
really a function of some of the customer shipment timing. Our expectation is that comes back in the
second half. So sort of low double-digit growth on auto is very consistent with what we've been guiding
throughout this year. IoT has actually been an interesting update from our perspective.
And what we're seeing is that where there has been some softness in smart mobile, some of those
customers within mobile have actually reallocated their demand into IoT, a lot of commonality between

some of those connectivity applications that you see between the 2. So that's what's driving the pickup
in IoT to sort of the 10% to 15% level that I indicated year-over-year. And then obviously, we spent quite
a bit of time on comms infra and data center. So I won't reiterate that, but that's really the change
quarter-on-quarter, that movement to kind of 50% to 60% year-over-year growth. So you can sort of
infer from that, Tim, what that means for third quarter into fourth quarter.
I think your math is about right in terms of that implied pickup into the fourth quarter. And then, look,
as it relates to some of the dynamics within 3Q and 4Q, it's largely consistent with, I think, what we're
expecting to see from a trend perspective and what I just outlined on the end market split as well.
Timothy Breen (Executives)
And maybe, Tim, if I can just add, if we zoom out for a second and think about kind of are we seeing
more and more traction in those end markets? I think we haven't spoken a lot about design wins across
the board, but we continue to see record design win momentum entering into 2026. versus '25. So
again, that traction remains really strong. I think the other thing that's very important, we've worked
very hard to make our manufacturing footprint as flexible as possible because there are always going to
be perturbations between different end markets in terms of timing.
You see obviously a very strong story in the data center. You see mobile is obviously going in a different
direction given the memory shortage. We've been able to reuse capacity very well this year to enable us
to capture some of those upsides given the flexibility of our manufacturing footprint.
Timothy Arcuri (Analysts)
Great. And then just as a quick follow-up. So on SiPho, we do hear about some competitors are getting
aggressive in going after that business as well. And the customer base is fairly concentrated. So how to
think about that? Like can customers multisource across different suppliers? How feasible is that?
Timothy Breen (Executives)
Yes. I think, look, the fact that there's competition is a sign that there's strong support for this secular
trend, and I think that's not a bad thing from our point of view. What I can say is customers are also
coming to us and saying, I don't have enough secured, I need to secure more and how can I help? And
some of that is also mitigating geopolitical risk that they see as well. And look, our strategy in any
platform is try to work as broadly as we can across the industry so that we're not betting on the success
of player A over player B, but we're mitigated if different people win different sockets.
Actually, we have more than 40 customers today in SiPho, and that, of course, includes some early-
stage companies, but some of those early-stage companies are really doing great things in terms of
ramping new solutions. So I don't think we have a customer concentration concern at this stage, and
you're going to see even new entrants. Look at all of the, let's say, I would say, smaller fabless
companies that historically were saying copper will last for a long time. All of them to a T have done a
photonic strategy, made a photonics acquisition, and they're entering into that space quite aggressively.
So I don't think we have a customer concentration concern. And I just think we have durable demand.
And like I mentioned earlier, our conversations with the hyperscalers are very helpful to vet what they
see kind of as an end consumer of those applications. And again, that reinforces the durability of the
demand.

Operator (Operator)
And our next question comes from the line of C.J. Muse from Cantor Fitzgerald.
Christopher Muse (Analysts)
I guess first question on CID. Implicit in your guide is roughly an exit rate of $350 million for this
segment. And so curious, based on what you see today in terms of design wins, how do you see kind of
the growth into calendar '27? I know you don't want to give specific guidance, but should we be
thinking about very strong growth off of that kind of new level? Or is there kind of a digested period?
Sam Franklin (Executives)
Yes. Happy to take that, C.J. And look, I think you're kind of getting to the right rough numbers going
out of this year. The commentary that we provided as part of our Investor Day and Analyst Day a couple
of months ago still stands as we see the opportunities for comms infra and data center. Obviously, it's
expected to come in stronger during 2026, but there was a good reason we indicated that 30-plus
percentage year-over-year growth that we're targeting through our long-term model.
The plus is sort of ties into what Tim said earlier around some of the growth that we're seeing in
demand, the increases that we're making to support that demand into our capacity and just the
continued ramp in customer expansion as well. So look, I would still stand by our long-term model that
we shared a couple of months back in terms of that 30-plus point percentage growth going into 2027
and beyond.
Timothy Breen (Executives)
CJ, if I could. Demand is clearly very strong. And so the question is more about the rate and pace of
manufacturing productivity and capacity expansion. That's obviously a conversation we continue to
have with customers. One of the advantages for us is that we can meaningfully inflect our capacity
within our existing fab footprint. We don't need to build other fabs and some of our other players in the
industry are building other fabs, which obviously is a longer lead time to bring that capacity online. So
we're bringing within our 4 walls.
And just to give you a sense, if we think of our long-term plan, just take for Photonics, we could 10x our
photonics capacity within our current 4 walls plan on a global basis. And so we have a lot of flexibility
about when we do that based on the demand and the partnerships we have with customers.
Christopher Muse (Analysts)
Very helpful. And then a follow-up on gross margins. It sounds like the story here in calendar '26 is
really all about mix. And so curious, given your commentary around selective price increases and how
you're going to continue to look at that into calendar '27, how are you thinking about the prioritization
of drivers between kind of mix, pricing and utilization? And is there a framework for us to think about
incremental gross margins from here?
Sam Franklin (Executives)
Yes. Look, maybe I'll start with the mix point, CJ, because it remains the single biggest driver. And in
actual fact, we're still at some of the early innings of those mix shifts that we talked about from a
capacity point of view. Clearly, the demand has been pulling through well during the course of 2026.

But when you think about the CapEx that we indicated for this year, that sort of 15% to 20% range, my
expectation is that we'll be up to the higher end of that range. One of the single biggest drivers just to
support incremental investments into capacity to meet that growing demand.
Now as you'd expect, the time lag between when you incur those CapEx dollars to when you install a
tool, qualify it, ramp it, there's a lag to be able to then support that demand. My point being is that mix
will continue to be a significant driver as we outlook within the model over the course of the next couple
of years. And then really the 2 to 3 other factors I'd point to. One, yes, utilization, but somewhat
impacted. If you think about where things are at from a cycle point of view, we've still got about 10
points of utilization to be able to grow into just with our installed capacity today. So that's one dynamic.
And then the other is really around continued improvements from a cost and a productivity point of
view. We have been focusing maniacally on our structural cost improvements. We've seen that come
through in terms of our relative cash cost per mask layer. It's an area of continued focus for the teams
as well. So really across that range of metrics is where we see the opportunity to continue expanding
margin and get towards that 40% exit run rate that we indicated in the 2028 time frame.
Then beyond that, to Tim's earlier comments, is where we expect to see continued ramps in custom
silicon and activities under our IP, software, custom silicon business as well as the increased ramp from
co-packaged optics and the broader silicon photonics offerings as well. So that's how we think about it
over the next couple of years around some of those margin ramp drivers.
Operator (Operator)
This does conclude the question-and-answer session of today's program. I'd like to hand the program
back to Eric Chow for any further remarks.
Eric Chow (Executives)
Thank you, Jonathan. Thank you, everyone, for joining today. We're very glad to see you, and we will
see you at the Goldman Sachs Conference on September 8. Thank you.
Operator (Operator)
Thank you, ladies and gentlemen, for your participation in today's conference. This does conclude the
program. You may now disconnect. Good day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GFS_Q1_2026_Earnings_Call_20260505.md
- 2026-05-05｜Sam Franklin (CFO)｜guidance：Q2 營收指引 17.6 億美元 ±2,500 萬（原話："to be $1.76 billion, plus or minus $25 million."）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：Q2 毛利率指引約 28.5%（原話："We expect gross margin to be approximately 28.5%, plus"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：Q2 營業利益率指引 15.7%（±180bp）（原話："operating margin to be in the range of 15.7%"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：下半年季度營業費用維持與 Q2 指引相近水準（原話："operating expense run rate in the second half of 2026"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：CID 全年成長由約 30% 上調至高 30%（原話："achieve high 30s percent year-over-year revenue growth"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：車用 2026 年營收低雙位數成長（原話："deliver low double-digit growth in 2026"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：智慧行動裝置 2026 年預期高個位數衰退，略優於智慧手機大盤（原話："slightly outperform the overall smartphone market"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：IoT 2026 年預期為成長年（Q1 下滑屬出貨時點、Q2 回補）（原話："we continue to expect 2026 to be a growth year for"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：技術服務佔 2026 年營收比重趨近原 10–12% 區間高端（原話："comprise a greater proportion of our total 2026 revenue"）
- 2026-05-05｜Timothy Breen (CEO)｜guidance：矽光子 2026 年營收約翻倍（原話："roughly double our silicon photonics revenue in '26"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：全年淨資本支出佔營收 15–20% 維持不變（原話："CapEx to be in the range of 15% to 20% of revenue."）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：2026 全年調整後自由現金流率約 10%，下半年偏重（原話："adjusted free cash flow margin of approximately 10%"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：MIPS 2026 年營收貢獻 6,000 萬至 1 億美元區間維持（原話："That range still holds."）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：MIPS 預訂趨勢高於區間中點（未含 Synopsys ARC）（原話："trending towards above the midpoint of"）
- 2026-05-05｜Timothy Breen (CEO)｜guidance：短期定價部位將調價，預期落在 2026 下半年尾端並延續至 2027（原話："price adjustments on that part of the portfolio."）
- 2026-05-05｜Sam Franklin (CFO)｜commitment：承諾 2026 年底毛利率達 30% 以上（原話："still to exit 2026 at or above a 30% gross margin."）
- 2026-05-05｜Timothy Breen (CEO)｜commitment：矽光子營收運行率目標：2028 年底超過 10 億美元（原話："photonics revenue run rate exiting 2028."）
- 2026-05-05｜Sam Franklin (CFO)｜margin：Q1 毛利率創第一季紀錄，年增逾 500bp（原話："our gross margin achieved a first quarter record"）
- 2026-05-05｜Sam Franklin (CFO)｜margin：管理層稱 Q1 毛利率年增的最大來源為產品組合（原話："driver there was mix and mix falls into 2 categories."）
- 2026-05-05｜Sam Franklin (CFO)｜margin：Q1 毛利率優於指引中點 200bp 中，約 1 點來自 AMF 成本綜效（原話："about 1 point of that came through cost synergies that"）
- 2026-05-05｜Sam Franklin (CFO)｜margin：中東衝突相關氣體與化學品備貨成本，預期每季約影響 0.5 點毛利率（原話："has about 0.5 point of margin impact for each quarter"）
- 2026-05-05｜Sam Franklin (CFO)｜margin：Q1 自由現金流受有利營運資金變動推升，管理層預期 Q2 回轉（原話："favorable working capital movements in the first quarter"）
- 2026-05-05｜Sam Franklin (CFO)｜margin：Q1 非智慧行動裝置終端市場加技術服務佔比創歷史高點約 2/3（原話："that came in at the highest level"）
- 2026-05-05｜Sam Franklin (CFO)｜margin：定價以對毛利結構的貢獻衡量，而非單看 ASP；舊閒置費用已大致結束（原話："That is largely in the rearview mirror."）
- 2026-05-05｜Timothy Breen (CEO)｜capital_allocation：針對吃緊產能談客戶預付款，搭配資本支出加速（原話："advanced payments to secure capacity"）
- 2026-05-05｜Sam Franklin (CFO)｜capital_allocation：下一波產能投資預期伴隨客戶預付款與政府補助（原話："capacity investments will be accompanied by customer"）
- 2026-05-05｜Sam Franklin (CFO)｜capital_allocation：Q1 回購 4 億美元，授權額度剩約 1 億美元（原話："we repurchased $400 million of our shares"）
- 2026-05-05｜Timothy Breen (CEO)｜capital_allocation：資本支出主要加裝工具於既有廠區，並有政府支持（原話："the ROI is very strong because we're adding tools"）
- 2026-05-05｜Sam Franklin (CFO)｜capital_allocation：下半年加碼 R&D 方案（原話："We are ramping R&D programs in the second half of 2026 to"）
- 2026-05-05｜Timothy Breen (CEO)｜competition：被問 CID 成長是否落後同業，答稱各子市場未見流失、多處有份額增加（原話："we don't see share loss. In fact, we see share gain"）
- 2026-05-05｜Timothy Breen (CEO)｜competition：矽光子設計導入前四大可插拔光模組廠中的三家（原話："GF is now designed in at 3 of the top 4 pluggable optical"）
- 2026-05-05｜Sam Franklin (CFO)｜competition：管理層稱此前定價環境較 2025 更具建設性（原話："GF is now designed in at 3 of the top 4 pluggable"）
- 2026-05-05｜Timothy Breen (CEO)｜product：SCALE 稱為業界首個符合 OCI MSA 的平台（原話："the industry's first OCI MSA capable platform"）
- 2026-05-05｜Timothy Breen (CEO)｜product：共封裝光學仍視為 2028 年的故事（原話："co-packaged optics is a 2028 story."）
- 2026-05-05｜Timothy Breen (CEO)｜product：SiGe 於 Vermont 廠產能超額認購至 2027（原話："the industry's first OCI MSA capable platform"）
- 2026-05-05｜Timothy Breen (CEO)｜customer：Q1 設計案較去年同期增加 50%（原話："co-packaged optics is a 2028 story."）
- 2026-05-05｜Timothy Breen (CEO)｜customer：Renesas 多十億美元策略合作（原話："announced a multibillion-dollar strategic partnership"）
- 2026-05-05｜Timothy Breen (CEO)｜customer：Apple 與 Cirrus Logic 合作將新製程帶至 Malta 廠（原話："bring new process technologies to our Malta, New York fab."）
- 2026-05-05｜Timothy Breen (CEO)｜customer：在地化帶動客戶接洽與設計案增加（原話："a meaningful increase in customer engagements"）
- 2026-05-05｜Sam Franklin (CFO)｜risk：中東衝突影響供應鏈，已提前備貨關鍵氣體與化學品（原話："how the conflict in the Middle East impacts supply chain"）
- 2026-05-05｜Sam Franklin (CFO)｜product：營收類別更名：晶圓營收改稱製造服務（原話："revenue previously referred to as wafer revenue"）

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

### GFS_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260908.md
- 2026-09-08｜Timothy Breen (CEO)｜capital_allocation：CEO says company is in a supply-chasing phase; capex rising this year and again next year, gated by tool install/qualification.（原話："We are clearly in a chasing supply moment today."）
- 2026-09-08｜Timothy Breen (CEO)｜capital_allocation：Capex increases this year vs last and further next year; pace depends on tool readiness.（原話："We'll be increasing further again next year"）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：Next year's growth is gated by supply (tool installation/qualification), not demand.（原話："We don't see a demand-based reason"）
- 2026-09-08｜Timothy Breen (CEO)｜customer：Customers co-invest financially alongside GF in some capacity ramps.（原話："they're also co-investing alongside us"）
- 2026-09-08｜Timothy Breen (CEO)｜product：Silicon photonics customer count.（原話："We have more than 40 customers in photonics today"）
- 2026-09-08｜Timothy Breen (CEO)｜commitment：States ability to scale photonics capacity 10x inside existing US and Singapore fabs.（原話："10x our photonic capacity within our existing 4-wall"）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：On the $1B (2028) / $2B (2030) photonics targets, says industry adoption needed is already in place.（原話："the industry adoption needed to reach those targets"）
- 2026-09-08｜Timothy Breen (CEO)｜risk：Photonics demand exceeds supply from current installed base; mentions balancing capacity lead against long-term profitability.（原話："much more demand than we can supply"）
- 2026-09-08｜Timothy Breen (CEO)｜product：Pluggables alone reach the first photonics milestone; co-packaged optics would be upside beyond targets.（原話："Pluggables gets you pretty much all the way there."）
- 2026-09-08｜Timothy Breen (CEO)｜competition：Notes former copper proponents have entered optical, so participants in optical have broadened.（原話："everyone who was touting copper 2 years ago"）
- 2026-09-08｜Timothy Breen (CEO)｜product：GaN products already shipping to data center; BCD 55nm in new conversion stages.（原話："We're shipping GaN products to the data center today."）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：Power/BCD pull-through to business not yet seen; expected in 2027 and more in 2028, with capacity added then.（原話："We have yet to see the real pull-through for the business"）
- 2026-09-08｜Timothy Breen (CEO)｜margin：Mobile share of revenue defined: from >50% to mid-30s, long-term model mid-20s.（原話："that's down to the mid-30s today"）
- 2026-09-08｜Timothy Breen (CEO)｜commitment：Medium-term plan does not depend on mobile growth.（原話："we do not rely on it growing to achieve our medium-term plan"）
- 2026-09-08｜Timothy Breen (CEO)｜risk：Describes mobile as a tough year, especially at the low end; GF more exposed to higher-end handsets.（原話："It is indeed a tough year."）
- 2026-09-08｜Timothy Breen (CEO)｜customer：Mobile customers are asking to secure 2027 and 2028 supply even if units are down low double digits.（原話："I need my supply for '27, I need my supply for '28"）
- 2026-09-08｜Timothy Breen (CEO)｜customer：Automotive share of revenue went from 2% five years ago to the 20s today.（原話："We were, sort of 5 years ago, 2%. It's now in the 20s."）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：Auto double-digit growth expected to continue this year, next year and beyond, driven by content not units.（原話："will continue this year, next year and beyond"）
- 2026-09-08｜Timothy Breen (CEO)｜customer：GM cited as having secured capacity itself with GF as part of NCNT/US-for-US sourcing push in auto.（原話："securing that capacity themselves as GM did with us"）
- 2026-09-08｜Timothy Breen (CEO)｜customer：Reshoring: NCNT now the rule in procurement, whereas footprint was previously not a differentiator.（原話："NCNT is the rule, not a nice-to-have, right?"）
- 2026-09-08｜Timothy Breen (CEO)｜product：Physical AI described as early stage, not yet materially hitting the business.（原話："We haven't seen that really materially hit the business yet."）
- 2026-09-08｜Timothy Breen (CEO)｜capital_allocation：About six acquisitions in two years; IP acquisitions (MIPS, RISC-V, Synopsys ARC) framed by customer reaction test.（原話："We've done about 6 acquisitions in the last 2 years."）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：IP/software/custom silicon revenue stated at $100–120M this year with $1B exit run-rate target by end of decade.（原話："between $100 million and $120 million of revenue this year"）
- 2026-09-08｜Timothy Breen (CEO)｜commitment：Expresses confidence in the $1B end-of-decade IP run-rate.（原話："very confident for that end of decade kind of $1 billion"）
- 2026-09-08｜Timothy Breen (CEO)｜margin：Describes IP acquisitions as accretive revenue with very good margins.（原話："accretive revenue, very good margins, very good growth"）
- 2026-09-08｜Timothy Breen (CEO)｜competition：Claims position as second-largest processor IP supplier after the incumbent.（原話："probably the second largest processor IP supplier"）
- 2026-09-08｜Timothy Breen (CEO)｜customer：Synopsys ARC acquisition brought a 300-customer base GF is now engaging.（原話："it came with 300 customers"）
- 2026-09-08｜Timothy Breen (CEO)｜customer：Names Lockheed Martin (defense) as an IP-related engagement.（原話："we had an announcement with Lockheed Martin about that"）
- 2026-09-08｜Timothy Breen (CEO)｜product：Quantum: bottleneck framed as high-volume manufacturing.（原話："the bottleneck is not quantum science, it's high-volume manufacturing"）
- 2026-09-08｜Timothy Breen (CEO)｜capital_allocation：US government quantum deal completed; accelerates investment in tooling and infrastructure.（原話："we completed the deal that we announced earlier in the year"）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：Comm infrastructure/data center end-market running 60% in Q2 vs long-term target in the 30s; auto in line, IoT slightly ahead.（原話："We're doing 60% in Q2."）
- 2026-09-08｜Timothy Breen (CEO)｜commitment：Says no demand constraint to meeting and exceeding the long-term plan.（原話："I don't see a demand constraint to meeting and exceeding"）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：Next couple of years described as supply-constrained rather than demand-constrained, barring environment changes.（原話："supply-constrained, not demand-constrained"）
- 2026-09-08｜Timothy Breen (CEO)｜capital_allocation：Government partnerships provide capex acceleration tools with significant recovery rates.（原話："accelerate CapEx at significant recovery rates"）
- 2026-09-08｜Timothy Breen (CEO)｜commitment：Says diversification gives confidence; long-term plan numbers may look conservative.（原話："may even make those numbers look a bit conservative"）

### 問答異常語氣（迴避／改口／保留）
- GFS_Q1_2026_Earnings_Call_20260505.md｜問：Harlan Sur 問年底毛利率是否可接近 33–35%｜答法：未回應該區間，改談年增表現、營收增量對應毛利增量，並重申年底 30% 以上目標
- GFS_Q1_2026_Earnings_Call_20260505.md｜問：Vivek Arya 問 CID 成長相對同業 50–100% 是否在流失份額｜答法：未給份額數字，以三大子市場分述並稱未見流失
- GFS_Q1_2026_Earnings_Call_20260505.md｜問：Vivek Arya 問年初與現在的定價假設及每片營收持續下滑｜答法：未給定價數字，改談混合與毛利貢獻，稱以毛利結構為重
- GFS_Q1_2026_Earnings_Call_20260505.md｜問：Krish Sankar 問 SCALE 與 TSMC COUPE／Tower 的比較與製程節點｜答法：未給節點或規格比較，延後至 Investor Day
- GFS_Q1_2026_Earnings_Call_20260505.md｜問：Ross Seymore 問 2Q 各終端市場與子類別方向性指引｜答法：僅給年增方向與 IoT 回補，未給各市場 Q2 數字
- GFS_Q1_2026_Earnings_Call_20260505.md｜問：Ross Seymore 問智慧行動裝置相對大盤的長期差距｜答法：未回答，延後至 Investor Day，僅談新形態裝置的順風
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
{"date":"20260710","verdict":"觀望","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"成熟製程週期復甦真實，稼動率與 Non-IFRS GM 結構性回升","columns":{"2Y 驗證點":"FY26-27 Non-IFRS GM 達 30%+、稼動率近 90%","5Y 驗證點":"through-cycle GM 站穩 28-32%（vs 谷底 22%）","10Y 驗證點":"長期 GM 目標 40% 可達性","具體數字門檻":"Non-IFRS GM 30%+（Q1'26 29%、Q2 guide 28.5%）；稼動率 8 吋 80%→90%","信息來源":"公司 4Q25/1Q26 法說、TrendForce 成熟製程漲價報告","漂移觸發條件":"連 2 季 TTM GM &lt; 27% 或稼動率回落 → 削弱（TTM 季節性過濾）"}},{"id":"H2","text":"特殊製程第二曲線（車用/矽光子/功率）成長引擎兌現","columns":{"2Y 驗證點":"矽光子 2026 翻倍、車用 +low-double、Comms/DC +25%+","5Y 驗證點":"矽光子 $1B run-rate（2028）、功率 $1B 增量軌道（2030）","10Y 驗證點":"特殊製程營收占比由 ~30% 升向 50%+","具體數字門檻":"矽光子 FY26 +100%（$200M→$400M+）；車用 FY25 $1.4B +17%","信息來源":"公司 Investor Day 2026、SiPh Cisco/Sivers 合作、AMF 收購","漂移觸發條件":"矽光子連 2 季 &lt; +50% 或車用 &lt; +8% → 削弱"}},{"id":"H3","text":"ROIC 隨稼動率回升結構性改善、資本效率提升","columns":{"2Y 驗證點":"FY26-27 ROIC 由 ~7% 升向 9-10%（周轉率改善）","5Y 驗證點":"ROIC 持續站上 WACC（~9-10%）","10Y 驗證點":"through-cycle ROIC &gt; WACC 的複利可維持性","具體數字門檻":"投入資本周轉率由 0.52x 升；Capex/Rev 控制在 ≤12%","信息來源":"yfinance 三表自算、公司 capex 指引","漂移觸發條件":"FY26-28 連 3 年 ROIC &lt; 9% → 結構性低 ROIC 確認、H3 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"成熟製程循環二次反轉：中國新產能（Nexchip/CanSemi）壓低 ASP + 車用/工業庫存二次修正 → 稼動率回落、GM 壓回","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"季度稼動率、wafer 出貨 YoY、同業 UMC/VIS/SMIC 成熟製程價量","警戒閾值":"連 2 季稼動率 &lt; 80% 且 GM YoY 下滑 &gt; 3pp"}},{"id":"R2","text":"客戶集中 + 中國本地化侵蝕：前二大客戶占晶圓收入 ~30.3%（2025 20-F）；China-for-China 車用授權策略稀釋自身產能訂單；2028 Qualcomm LTA 重議","columns":{"對應假設":"H1+H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"客戶 IR、中國本土代工拿單、LTA 續約條件、全球代工市佔","警戒閾值":"市佔跌破 3.0%，或任一大客戶轉單 &gt; 30% 訂單，或 LTA 重議量縮"}},{"id":"R3","text":"ROIC 結構性低於 WACC：capital-intensive foundry 投入資本周轉率長期壓 ROIC → 多年複利價值毀滅","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"年度 ROIC、Capex/Rev、投入資本周轉率、同業資本效率","警戒閾值":"FY26-28 連 3 年 ROIC &lt; 9%（WACC 之下）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE(FY+2) 回落至 ≤22x（約 $55-58）；或連 2 季 Non-IFRS GM ≥30% 且 SiPh 全年翻倍兌現；Section 232 Phase 2 若對進口類比/RF/功率 IC 課稅為額外上行催化","irr_base_pct":6.3,"ev5y_pct":31.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"衛星","signal":"B","val":"🟠","ma":"-","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.3,"ev5y_pct":31.0,"irr_base_pct":6.3,"max_dd_pct":-60.0,"bull_5y_price":143.0,"bear_5y_price":43.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE(FY+2) 回落至 ≤22x（約 $55-58）；或連 2 季 Non-IFRS GM ≥30% 且 SiPh 全年翻倍兌現；Section 232 Phase 2 若對進口類比/RF/功率 IC 課稅為額外上行催化","price_at_dd":69.71,"archetype":"循環/商品","cycle_position":"早循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261012/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
