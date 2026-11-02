你是 stock-analyst **v20 判斷 agent**，標的 3711.TW（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"3711.TW","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3711.TW_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3711.TW_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP，合併）","value":191064,"period":"2Q26（季末 2026-06-30，公告於 2026-07-30）","unit":"NT$百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"2Q26（季末 2026-06-30，公告於 2026-07-30）","citation":"日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm"},"note":"未取得"},{"id":"f_kpi1","label":"毛利率","value":21.0,"period":"2Q26（季末 2026-06-30，公告於 2026-07-30）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"2Q26（季末 2026-06-30，公告於 2026-07-30）","citation":"日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm"},"note":"未取得"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":21134,"period":"2Q26（季末 2026-06-30，公告於 2026-07-30）","unit":"NT$百萬（利益率 11.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"2Q26（季末 2026-06-30，公告於 2026-07-30）","citation":"日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm"},"note":"未取得"},{"id":"f_kpi3","label":"歸屬母公司淨利","value":21068,"period":"2Q26（季末 2026-06-30，公告於 2026-07-30）","unit":"NT$百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"2Q26（季末 2026-06-30，公告於 2026-07-30）","citation":"日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm"},"note":"未取得"},{"id":"f_kpi5","label":"設備資本支出","value":1695,"period":"2Q26（季末 2026-06-30，公告於 2026-07-30）","unit":"US$百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"2Q26（季末 2026-06-30，公告於 2026-07-30）","citation":"日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm"},"note":"未取得"},{"id":"f_kpi6_3q26","label":"管理層指引：3Q26","value":"合併營收 QoQ +21%～22%；毛利率 20.5%～21.5%；營業利益率 11.5%～12.5%；ATM 營收 QoQ +11%～13%、毛利率 28%～29%；EMS 營收 QoQ 約 +40%、營業利益率 3.2%～3.4%","period":"2Q26（季末 2026-06-30，公告於 2026-07-30）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"2Q26（季末 2026-06-30，公告於 2026-07-30）","citation":"日月光投控 2Q26 法說簡報（SEC 6-K）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011353/dp250875_6k.htm（匯率假設 US$1=NT$31.9）"},"note":"未取得"},{"id":"f_kpi7_2026","label":"管理層指引：2026 全年","value":"ATM 營收年增約 35%（美元）；一般業務年增 20%（原 13%）；LEAP 服務營收「高於先前 US$35 億指引」","period":"2Q26（季末 2026-06-30，公告於 2026-07-30）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"2Q26（季末 2026-06-30，公告於 2026-07-30）","citation":"日月光投控 2Q26 法說簡報（SEC 6-K）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011353/dp250875_6k.htm"},"note":"未取得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_3711_tw_gross_margin_pct","label":"3711.TW 毛利率","value":20.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3711.TW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_3711_tw_operating_margin_pct","label":"3711.TW 營業利益率","value":11.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3711.TW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_3711_tw_fcf_margin_pct","label":"3711.TW FCF 利潤率","value":-11.29,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3711.TW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amkr_gross_margin_pct","label":"AMKR 毛利率","value":16.56,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMKR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amkr_operating_margin_pct","label":"AMKR 營業利益率","value":9.51,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMKR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amkr_fcf_margin_pct","label":"AMKR FCF 利潤率","value":-2.09,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMKR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_6239_tw_gross_margin_pct","label":"6239.TW 毛利率","value":19.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6239.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6239_tw_operating_margin_pct","label":"6239.TW 營業利益率","value":12.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6239.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6239_tw_fcf_margin_pct","label":"6239.TW FCF 利潤率","value":-9.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6239.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2449_tw_gross_margin_pct","label":"2449.TW 毛利率","value":38.31,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2449.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2449_tw_operating_margin_pct","label":"2449.TW 營業利益率","value":26.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2449.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2449_tw_fcf_margin_pct","label":"2449.TW FCF 利潤率","value":-32.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2449.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4","label":"自由現金流（推算）","value":-32835,"period":"2Q26（季末 2026-06-30，公告於 2026-07-30）","unit":"NT$百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"2Q26（季末 2026-06-30，公告於 2026-07-30）","citation":"日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm；營業現金流 47,014 減 PP&E 淨支出 79,849，由查證者推算，公司未自報 FCF"},"note":"未取得"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":668.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"TWD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":41.03,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^TWII","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":47.73,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":21.21,"period":"2026-11-02","unit":"TWD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-02","citation":"yfinance earnings_estimate"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":33.78,"period":"2026-11-02","unit":"TWD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-02","citation":"yfinance earnings_estimate"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":40.68,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.75,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.14,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.986,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":305981.99,"period":"2026-11-02","unit":"TWD m","basis":"yfinance 最新一季：總債務 394402.99、現金 88421.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":4415.15,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":3255300.43,"period":"2026-11-02","unit":"TWD m","basis":"市值 2949318.44 ＋ 淨負債 305981.99","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":869241.07,"period":"2026-11-02","unit":"TWD m","basis":"yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":1118078.5,"period":"2026-11-02","unit":"TWD m","basis":"yfinance revenue_estimate +1y 平均（18 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.74,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"✅","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 668.0 / W52 467.26 / W104 310.42 / W250 190.54 / W250 13週斜率 5.31%"},{"id":"f_ma_w52","label":"52 週均線","value":467.26,"period":"2026-11-02","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":310.42,"period":"2026-11-02","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":190.54,"period":"2026-11-02","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":5.31,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"法人指出日月光投控為台積電以外先進封裝產能規模最大的廠商（工商時報報導，經搜尋摘要轉述）","source":"工商時報 ctee.com.tw 20251211700306-430203","url":"https://www.ctee.com.tw/news/20251211700306-430203","excerpt":null,"as_of":"2025-12-11","retrieved_at":"2026-10-19","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"瑞銀預估日月光CoWoS產能由2026年底每月約2萬片擴增至2027年底每月約5萬片，需求來自AMD新款CPU與AI加速器","source":"科技新報 瑞銀給日月光投控買進評等目標價835元","url":"https://finance.technews.tw/2026/07/02/ubs-gives-ase-technology-holding-a-buy-rating-with-a-target-price-of-nt835/","excerpt":null,"as_of":"2026-07-02","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"日月光2026年7月法說會將全年資本支出上修至105億美元（年初70億、前次85億）","source":"中國時報 wantrich.chinatimes.com 20260731900276","url":"https://wantrich.chinatimes.com/news/20260731900276-420101","excerpt":null,"as_of":"2026-07-31","retrieved_at":"2026-10-19","affects":["valuation","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"對手Amkor 2026年Q2營收創高約19億美元、年增26%，7月宣布與NVIDIA多年期15億美元美國封測合作；Intel EMIB-T在高階封裝積壓訂單增加（Zacks/Nasdaq 轉述）","source":"Nasdaq/Zacks: Can ASE Technology Sustain Its Recent Margin Expansion?","url":"https://www.nasdaq.com/articles/can-ase-technology-sustain-its-recent-margin-expansion","excerpt":null,"as_of":"2026-08-01","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"2Q26 ATM 前五大客戶約占淨營收 44%（1Q26 為 43%），單一客戶占比超過 10%；未指名客戶，也未提第二供應商或自製。","source":"ASE Technology Holding 2Q26 財報新聞稿（ycharts/PRN 轉載）","url":"https://ycharts.com/news/story/PRN-HK15751-20260730","excerpt":"Our five largest customers together accounted for approximately 44% of our total net revenues in 2Q26, compared to 43% in 1Q26. One customer accounted for more than 10% of our total net revenues in 2Q26.","as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"2Q26 EMS 口徑前五大客戶約占淨營收 58%，低於 1Q26 的 64%，單一客戶超過 10%。","source":"ASE Technology Holding 2Q26 財報新聞稿（ycharts/PRN 轉載）","url":"https://ycharts.com/news/story/PRN-HK15751-20260730","excerpt":"Our five largest customers together accounted for approximately 58% of our total net revenues in 2Q26, compared to 64% in 1Q26.","as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2Q26 法說新聞稿揭露：前五大客戶約占淨營收 44%（1Q26 為 43%）；前十大客戶占 60%（1Q26 為 58%）；有一家客戶占淨營收逾 10%，客戶未具名。搜尋摘要未明確區分該口徑為 ATM 或合併，需判斷層對照原文。","source":"ASE Technology Holding Co., Ltd. Reports Its Unaudited Consolidated Financial Results for the Second Quarter of 2026 (PR Newswire/YCharts)","url":"https://ycharts.com/news/story/PRN-HK15751-20260730","excerpt":"Our five largest customers together accounted for approximately 44% of our total net revenues in 2Q26, compared to 43% in 1Q26. One customer accounted for more than 10% of our total net revenues in 2Q26. Our top 10 customers contributed 60% of our total net revenues in 2Q26, compared to 58% in 1Q26.","as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2Q26 EMS 部門前五大客戶約占 58%（1Q26 為 64%），前十大占 69%，另有一家客戶占逾 10%；集中度較 ATM 高但單季下降。","source":"ASE Technology Holding 2Q26 results release (PR Newswire/YCharts)","url":"https://ycharts.com/news/story/PRN-HK15751-20260730","excerpt":"Our five largest customers together accounted for approximately 58% of our total net revenues in 2Q26, compared to 64% in 1Q26.","as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2022 年第3季前十大客戶占半導體封測銷售約 59%（較早期：2019 Q2 約 60%、2014 Q2 約 46%），可作歷史對照。","source":"中央社 / 工商時報 法說會報導（搜尋結果）","url":"https://www.cna.com.tw/news/afe/202210270189.aspx","excerpt":"前10大客戶占比約59%","as_of":"2022-10-27","retrieved_at":"2026-10-19","affects":["moat_trend"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026年4月法說：管理層表示2026年需求遠超原先預期，先進封裝業務營收成長預估再上修約10%，並調升2026年資本支出，看好今明兩年先進封裝需求（搜尋摘要轉述，非原文）","source":"科技新報 日月光調升 2026 年資本支出，看好今明兩年先進封裝業務需求爆發","url":"https://finance.technews.tw/2026/04/29/ase-technology-holding-is-optimistic-about-the-explosive-growth-in-demand-for-advanced-packaging-business-in-the-next-two-years/","excerpt":null,"as_of":"2026-04-29","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026年2月法說：先進封測(LEAP)營收由約16億美元倍增至32億美元，先進封裝產能供不應求，2026年資本支出上調至70億美元（搜尋摘要轉述）","source":"鉅亨/uanalyze 〈日月光法說〉先進封測供不應求 上調全年業績貢獻至32億美元；日月光投控2月營收521億元年增15.9%","url":"https://uanalyze.com.tw/articles/7561447401","excerpt":null,"as_of":"2026-02-05","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026年2月法說新聞稿：公司預期營收成長趨勢延續至2026年及以後，動能來自先進解決方案與AI普及及整體市場復甦帶動的全面性半導體需求","source":"搜尋摘要引述日月光2026年2月法說（chinatimes wantrich）","url":"https://wantrich.chinatimes.com/news/20260205900522-420101","excerpt":"日月光預計營收成長趨勢將延續至2026年及以後，主要動能來自於先進解決方案以及與AI普及和整體市場復甦所帶動之全面性半導體需求。","as_of":"2026-02-05","retrieved_at":"2026-10-19","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026年7月第二季財報時：預估先進封裝(VIP)業務營收2027年翻倍成長並追加今年資本支出20億美元；另有法人稱2027年全年維持滿載（均為搜尋摘要轉述，屬公司說法與法人推估，非確定財測）","source":"搜尋彙整 statementdog / ctee 2026-06 報導","url":"https://statementdog.com/news/16871","excerpt":null,"as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"產業層面：Wolfe Research分析師Chris Caso稱半導體供過於求最早要到2028年，因新晶圓廠建置時間長；同期SOXX自高點回落約25%（此為記憶體與整體半導體觀點，非封測專屬）","source":"247wallst Top Chip Analyst: Semiconductor Oversupply Is Nearly Impossible Before 2028","url":"https://247wallst.com/investing/2026/07/30/top-chip-analyst-semiconductor-oversupply-is-nearly-impossible-before-2028-why-hes-bullish-on-memory/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"公平會處分書及決議書資料庫以「日月光投資控股」全文搜尋，查詢日 2026-11-02 共 0 筆，無任何命中。","source":"公平交易委員會｜處分書及決議書全文搜尋","url":"https://www.ftc.gov.tw/internet/main/decision/decisionList.aspx?mid=11","excerpt":"以關鍵字「日月光投資控股」全文搜尋（查詢日 2026-11-02）共 0 筆。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"證交所 ESG 揭露：日月光投控報告年度 114 年，因反競爭行為相關法律訴訟造成的金錢損失總額為 0 仟元。","source":"證交所 OpenAPI t187ap46_L_20 反競爭行為法律訴訟","url":"https://openapi.twse.com.tw/v1/opendata/t187ap46_L_20","excerpt":"報告年度 114，因與反競爭行為條例相關的法律訴訟而造成的金錢損失總額(仟元)＝0.000。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"玉山投顧 2025 年 4 月分析：台廠中日月光美國比重最高、製造據點分布最廣；預期先進封測客戶可能以代購設備換取封測價格持穩，傳統封測則可能被要求降價以分擔客戶關稅成本（分析師預期，非公司公告）","source":"玉山證券 esunsec.com.tw 研究文章","url":"https://www.esunsec.com.tw/article/post/260","excerpt":null,"as_of":"2025-04-30","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2025 年 7 月底法說會：執行長吳田玉表示產能都在台灣且非常滿，公司支持其中一個最大客戶前往美國；美國測試廠依客戶需求規劃中，其他客戶需求續審慎評估","source":"日月光投控 2025 年 7 月法說會報導（搜尋結果摘要，來源站為公視／經濟日報系，未逐字取得）","url":"https://news.pts.org.tw/article/763494","excerpt":null,"as_of":"2025-07-31","retrieved_at":"2026-10-19","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美國商務部 BIS 擴大對中國半導體管制規則中，日月光投控列於 Approved OSAT Companies 名單（放行名單，非管制名單；報導指該名單無生產或出口豁免）；搜尋未見日月光本身被列入台灣國貿署或其他實體清單","source":"工商時報 ctee.com.tw 報導（BIS OSAT 名單）","url":"https://ctee.com.tw/news/stock/378361.html","excerpt":null,"as_of":"2024-12-03","retrieved_at":"2026-10-19","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2020年法人指出日月光投控產能在台灣比重超過6成（舊資料，非最新比重）","source":"中央社 日月光投控首季營收符預期 法人估今年獲利衝高","url":"https://www.cna.com.tw/news/firstnews/202004100215.aspx","excerpt":null,"as_of":"2020-04-10","retrieved_at":"2026-10-19","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"營運長吳田玉於2026年6月24日表示正擴大產能以滿足AI需求；報導稱2026年新建15個生產基地（日月光6、矽品7、另加4月中旬自群創收購廠房），今年資本支出85億美元（後續報導稱已上修至105億美元）","source":"時報 wantrich 日月光投控營運長吳田玉","url":"https://wantrich.chinatimes.com/news/20260624900474-420201","excerpt":null,"as_of":"2026-06-24","retrieved_at":"2026-10-19","affects":["thesis.H","valuation"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026年股東會：集團採「台灣優先」原則，先在台灣把封測整合與自動化做成熟再複製海外；2024年股東會曾稱不排除在美國、日本、墨西哥增加先進封裝產能；未找到越南、泰國的2026年產能資訊","source":"自由時報 日月光「卯足全力」擴產 今年啟動15座擴廠計畫","url":"https://ec.ltn.com.tw/article/breakingnews/5482278","excerpt":null,"as_of":"2026-06-01","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"日月光高層（黃義從）於SEMICON談話稱部分材料由少數廠商主導、甚至握有全球8、9成市占，替代供應商產能有限；部分特殊氣體與原物料集中於特定國家或地區；任一供應商出問題封裝端可能無法出貨","source":"鉅亨/UAnalyze 〈SEMICON〉日月光：材料聯盟要「築高牆」","url":"https://uanalyze.com.tw/articles/6889053842","excerpt":null,"as_of":"2025-09-01","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 年第三季法說展望：合併營收預期季增 21%～22%，封測事業毛利率上看 29%，財務長稱第四季封測毛利率很可能突破 30% 結構性上限。","source":"風傳媒 日月光法說","url":"https://www.storm.mg/article/11152966","excerpt":"展望第三季，公司預期合併營收將再季增21%至22%,半導體封裝測試事業毛利率上看29%;財務長董宏思更表示，第四季封測毛利率「很可能」突破目前30%的結構性上限。","as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 年 7 月合併營收 737.84 億元，年增 43.15%，單月歷史新高；封測及材料業務 475.24 億元，年增 49.5%。","source":"uanalyze 日月光投控7月營收738億元 年增43%飆單月新高","url":"https://uanalyze.com.tw/articles/5741253085","excerpt":"日月光投控7月營收738億元 年增43%飆單月新高","as_of":"2026-08-10","retrieved_at":"2026-10-19","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 年 5 月營收 630.33 億元，年增 28.6%，累計前 5 月年增 19.9%。","source":"TechNews 日月光投控 5 月營收","url":"https://finance.technews.tw/2026/06/09/aseh-3711-202605-financial-report/","excerpt":"日月光投控(3711)今(9)日公布 5 月營收，達 630.33 億元，較 4 月成長 1.3%,較去年同期成長 28.6%,累計前 5 月營收為 2,989.43 億元，年增 19.9%。","as_of":"2026-06-09","retrieved_at":"2026-10-19","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 年 3 月營收 615.77 億元，年增 14.6%，累計前 3 月年增 17.2%。","source":"TechNews 日月光投控 3 月營收","url":"https://finance.technews.tw/2026/04/10/aseh-3711-202603-financial-report/","excerpt":"日月光投控(3711)今(10)日公布 3 月營收，達 615.77 億元，較 2 月成長 18.2%,較去年同期成長 14.6%,累計前 3 月營收為 1,736.62 億元，年增 17.2%。","as_of":"2026-04-10","retrieved_at":"2026-10-19","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"AI 需求帶動先進封測，2026 年先進封測營收預期拚翻倍、高資本支出延續至 2027 年。","source":"財報狗 statementdog","url":"https://statementdog.com/news/16871","excerpt":"AI 需求爆發，日月光投控先進封測營收拚翻倍、高資本支出延續至 2027 年","as_of":"2026-07-31","retrieved_at":"2026-10-19","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"+","claim":"日月光投控將2026年資本支出由85億美元上調至105億美元，約70%設備資本支出投向領先尖端先進封裝（LEAP）；2027年LEAP營收目標由55億美元上修至至少75億美元（搜尋摘要轉述，未逐字取得原文）","source":"statementdog：AI 需求爆發，日月光投控先進封測營收拚翻倍、高資本支出延續至 2027 年","url":"https://statementdog.com/news/16871","excerpt":null,"as_of":"2026-07-31","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"2026年8月報導：日月光投控列出 Bridge、FOPLP、CPO 三大新技術布局；面板級封裝已進入量產準備階段（細節未取得）","source":"中時 wantrich 報導（2026-08-04）","url":"https://wantrich.chinatimes.com/news/20260804900380-420101","excerpt":null,"as_of":"2026-08-04","retrieved_at":"2026-10-19","affects":["moat_trend","triggers"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"搜尋摘要提及：客戶自建或英特爾晶圓代工加封測一條龍可能壓低封測價格、分流AI測試訂單，但短期英特爾基板良率偏低、實質影響有限（來源網址未能對應到單一篇，僅作線索）","source":"搜尋結果彙整（未對應單一網址）","url":null,"excerpt":null,"as_of":"2026-08-04","retrieved_at":"2026-10-19","affects":["decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2026年第二季法說（7/30）：營收1910.64億元、季增10%、年增26.7%創單季新高，毛利率21%為16季高點；營運長稱AI為產業典範轉移，推動先進封裝、測試新成長循環。","source":"經濟日報 ctee 2026-07-30 日月光投控法說報導","url":"https://www.ctee.com.tw/news/20260730701522-430201","excerpt":"日月光投控第2季合併營收新台幣1910.64億元，季增10%、年增26.7%，創單季新高。第2季毛利率21%","as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2025年第三季法說：Bump、FC、WLP、SiP等先進封裝占封測業務營收48%，打線26%、測試18%，先進封裝占比持續提高（產品組合由打線轉向先進封裝）。","source":"經濟日報 ctee 2025-10-30 日月光投控法說報導","url":"https://www.ctee.com.tw/news/20251030701988-430503","excerpt":null,"as_of":"2025-10-30","retrieved_at":"2026-10-19","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"法說後報導：2026全年資本支出上調至105億美元，約七成設備支出投入先進封裝（LEAP）；2026年LEAP營收將超越35億美元目標，2027年目標由55億美元上修至至少75億美元；面板級封裝預計2027上半年量產、CPO預計2026年底初期生產。（搜尋摘要彙整，非逐字）","source":"technews.tw / 搜尋摘要彙整（UBS 買進評等報導 2026-07-02、技術布局報導 2026-07-31）","url":"https://finance.technews.tw/2026/07/31/ase-technology-holding-co-ltd-has-a-comprehensive-layout-in-the-field-of-advanced-packaging/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"2026-10-19","affects":["moat_trend","valuation","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"分析稿指2026Q1 ATM 約占控股公司營收65%、卻貢獻約91%營業利潤；EMS 部門仍弱（2025Q4毛利率約9%）。","source":"Pluang 轉載分析 ASE Technology: bukan hanya OSAT","url":"https://pluang.com/en/news-feed/ase-technology-bukan-hanya-osat-kenaikan-leap-ubah-segala","excerpt":"In Q1 2026 the ATM segment was about 65 percent of holding-company revenue but roughly 91 percent of operating profit.","as_of":"2026-07-07","retrieved_at":"2026-10-19","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"野村證券2026-06-30維持買進，目標價由575元上調至730元，理由含台積電CoWoS擴產與先進封裝（LEAP）成長","source":"technews 四大因素帶動日月光投控營運動能，野村維持買進評等目標價 730 元","url":"https://finance.technews.tw/2026/06/30/four-factors-drive-the-momentum-of-ase-technology-holdings-operations/","excerpt":"四大因素帶動日月光投控營運動能，野村維持買進評等目標價 730 元","as_of":"2026-06-30","retrieved_at":"2026-10-19","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026年Q2法說（7月30日）：Q2合併營收1,910.64億元、EPS 4.80元；公司指引Q3營收季增21%至22%、封測毛利率上看29%，財務長稱Q4封測毛利率有望破30%","source":"風傳媒 日月光法說","url":"https://www.storm.mg/article/11152966","excerpt":"日月光法說》單季大賺210億元、EPS 4.8元!Q3營收季增上看22%,董宏思：Q4封測毛利率有望破30%","as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026年8月一家本土投顧維持買進、目標價685元，估2026／2027年EPS 18.72／27.33元；搜尋摘要稱7月初美系外資730元、澳系外資835元、本土法人748元（日期與機構未逐一核到原文）","source":"三立新聞 狂砸105億鎂搶先進封裝","url":"https://setn.com/news/1883173","excerpt":"狂砸105億鎂搶先進封裝!「這大廠」Q2獲利年增180% 目標價上看685元","as_of":"2026-08-01","retrieved_at":"2026-10-19","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026年7月營收737.84億元，年增43.15%，首度突破700億元；1至7月累計年增25.13%（8、9月公告未查到）","source":"鉅亨網／uanalyze 月營收","url":"https://uanalyze.com.tw/articles/5741253085","excerpt":"日月光投控7月營收738億元 年增43%飆單月新高","as_of":"2026-08-10","retrieved_at":"2026-10-19","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026年5月營收630.33億元，年增28.6%，前5月累計2,989.43億元、年增19.9%","source":"technews 日月光投控5月營收","url":"https://finance.technews.tw/2026/06/09/aseh-3711-202605-financial-report/","excerpt":"日月光投控(3711)今(9)日公布 5 月營收，達 630.33 億元，較 4 月成長 1.3%,較去年同期成長 28.6%,累計前 5 月營收為 2,989.43 億元，年增 19.9%。","as_of":"2026-06-09","retrieved_at":"2026-10-19","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"MOPS 近12個月486則重大訊息，標題含關鍵字者8則，皆為子公司資產／股權處分或子公司間簡易合併，無訴訟、停工、裁罰、重編類標題。","source":"公開資訊觀測站 歷史重大訊息清單（近12個月）","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=3711","excerpt":"【程式統計】公開資訊觀測站「歷史重大訊息」（t05st01），2025-11-02 至 2026-11-02 共 486 則；標題含關鍵字（併購、合併、收購、處分、訴訟、仲裁、停工、工安、裁罰、重編、異常、更正等）者 8 則，未含者 478 則。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"子公司USI Enterprise於2026-06-28公告擬大宗交易處分環旭電子股份不超過47,778,700股，2026-10-20公告因市場條件變化不予執行。","source":"公開資訊觀測站 重大訊息全文","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=3711","excerpt":"因市場條件變化，經審慎評估後不予執行","as_of":"2026-10-20","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"日月光2026年7月30日法說第三度上調全年資本支出至105億美元（較上季預測增加20億美元），其中40億美元用於新廠房與基礎設施、65億美元用於生產設備；13項新建工程同步進行、另有8項改建工程。","source":"自由時報／uanalyze 日月光法說報導（7/30法說）","url":"https://uanalyze.com.tw/articles/8357252477","excerpt":"日月光再度調升今年資本支出，為今年以來第三次，總金額達到105億美元，創新高，較上季預測時增加20億美元。","as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"日月光與矽品合計啟動約15個新廠或擴建計畫，目標是因應2029至2030年之後的需求；2026年規劃動工6座新廠。","source":"日月光股東會（2026年6月）報導／自由時報、uanalyze","url":"https://ec.ltn.com.tw/article/breakingnews/5482278","excerpt":"旗下日月光與矽品合計啟動約15個新廠或擴建計畫，為2029-2030年以後需求做準備。","as_of":"2026-06-30","retrieved_at":"2026-10-19","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"公司坦言近期增量成長能力受資本設備安裝及廠房建設速度限制，而非需求；2027年LEAP增量營收可望較2026年更大。","source":"technews／統計狗 日月光法說報導","url":"https://finance.technews.tw/2026/04/29/ase-technology-holding-is-optimistic-about-the-explosive-growth-in-demand-for-advanced-packaging-business-in-the-next-two-years/","excerpt":"公司坦言，近期增量成長能力已受到資本設備安裝及廠房建設速度限制。","as_of":"2026-04-29","retrieved_at":"2026-10-19","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"瑞銀估計OSAT端：日月光投控CoWoS類月產能2027年底達7萬片（2026年底2萬片），台積電18萬片、Amkor 2萬片；另一法人估OSAT端CoWoS相關月產能由2026年底約4萬片增至2027年底6.5萬片（法人估計，非公司公告）。","source":"經濟日報／UDN 瑞銀：ASIC與CPU推動CoWoS產能擴張","url":"https://money.udn.com/money/story/5607/9773857","excerpt":"瑞銀認為日月光投控(3711)的擴張更積極，在2027年底產能將達到每月7萬片，較2026年底的2萬片大幅成長。","as_of":"2026-10-08","retrieved_at":"2026-10-19","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"摩根士丹利 2026-01 預估日月光 2026 年漲價 5%~20%（媒體標題；成因含基板、貴金屬、電費成本上升，屬外資預估非公司公告報價）","source":"科技新報 finance.technews.tw","url":"https://finance.technews.tw/2026/01/08/ase-technology-holding-co-ltd-will-raise-prices-by-5-to-20-in-2026/","excerpt":"日月光 2026 年將漲價 5%~20%,大摩大調目標價至 308 元","as_of":"2026-01-08","retrieved_at":"2026-10-19","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"2026 年 10 月第三季財報報導：第三季營收優於公司原先指引；搜尋摘要稱成熟封測價格溫和上漲（摘要為二手轉述，未取得原文逐字句）","source":"科技新報 finance.technews.tw","url":"https://finance.technews.tw/2026/10/14/ase-technology-holding-co-ltd-reported-better-than-expected-results-for-the-third-quarter-of-2026/","excerpt":"ase technology holding co ltd reported better than expected results for the third quarter of 2026","as_of":"2026-10-14","retrieved_at":"2026-10-19","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"TrendForce 2026-06-08 晶圓代工快報：力積電 12 吋第二輪漲價訂於 2026 年第三季對全客戶生效，邏輯產能因 HBM 後段外包增加而吃緊（同業旁證，非日月光本身）","source":"TrendForce Foundry Market Bulletin - Jun. 8, 2026","url":"https://www.trendforce.com/research/download/RP260608SX3","excerpt":"PSMC 12-inch: Logic capacity squeezed by HBM back-end outsourcing ramp; second-round price hike set for 3Q26 across all customers","as_of":"2026-06-08","retrieved_at":"2026-10-19","affects":["valuation","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"搜尋摘要稱 2023 年第一季日月光投控毛利率降至 14.8%，為四年來低點，因客戶庫存調整、稼動率降溫；2022Q4 封裝、測試稼動率降至 75-80%（僅搜尋摘要，未讀原文頁面）","source":"鉅亨網／中央社日月光法說報導（搜尋結果）","url":"https://news.cnyes.com/news/id/4699952","excerpt":null,"as_of":"2023-04-27","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"搜尋摘要稱 2023 年全年營收 5,819.14 億元、年減 13%，全年毛利率 15.8%，較 2022 年減少 4.4 個百分點；2022 全年毛利率 20.1%；2023Q4 毛利率 16%（摘要轉述，未讀原文）","source":"TechNews 日月光投控 2023 EPS 7.39 元報導（搜尋結果）","url":"https://finance.technews.tw/2024/02/01/ase-investment-holdings-2023-eps-7-39-yuan/","excerpt":null,"as_of":"2024-02-01","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"+","claim":"搜尋摘要稱 2025Q4 毛利率回升至 19.5%、三年多新高，2025 全年毛利率 17.7%（上一輪低點回升時程，摘要轉述）","source":"uanalyze〈日月光法說〉去年Q4毛利率大增 全年EPS 9.37元創三年來新高","url":"https://uanalyze.com.tw/articles/9728447389","excerpt":null,"as_of":"2026-02-01","retrieved_at":"2026-10-19","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月唯一併購類重訊為孫公司HUNTINGTON HOLDINGS與百分百子公司UNITECH HOLDINGS簡易合併，目的為優化股權架構，不影響股東權益。","source":"公開資訊觀測站 重大訊息全文","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=3711","excerpt":"UNITECH HOLDINGS INTERNATIONAL CO. LTD.為HUNTINGTON HOLDINGS INTERNATIONAL\nCO. LTD.百分百持有之子公司，為優化股權架構進行合併，此交易並不影響股東權益。","as_of":"2025-12-22","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"3711.TW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":20.81,"operating_margin_pct":11.47,"fcf_margin_pct":-11.29,"rd_intensity_pct":5.04},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3711.TW","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"AMKR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":16.56,"operating_margin_pct":9.51,"fcf_margin_pct":-2.09,"rd_intensity_pct":2.12},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMKR","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"6239.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.12,"operating_margin_pct":12.9,"fcf_margin_pct":-9.7,"rd_intensity_pct":3.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6239.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"2449.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.31,"operating_margin_pct":26.86,"fcf_margin_pct":-32.27,"rd_intensity_pct":2.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2449.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"3711.TW"},"financial_history":{"ticker":"3711.TW","currency":"TWD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":670872643000.0,"revenue_yoy_pct":null,"gross_margin_pct":20.11,"operating_margin_pct":12.16,"net_income":61501545000.0,"diluted_eps":13.81,"free_cash_flow":37295698000.0,"fcf_margin_pct":5.56,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":581914471000.0,"revenue_yoy_pct":-13.26,"gross_margin_pct":15.77,"operating_margin_pct":7.2,"net_income":35457908000.0,"diluted_eps":7.18,"free_cash_flow":59832118000.0,"fcf_margin_pct":10.28,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":595409585000.0,"revenue_yoy_pct":2.32,"gross_margin_pct":16.28,"operating_margin_pct":6.79,"net_income":32378936000.0,"diluted_eps":7.23,"free_cash_flow":9105020000.0,"fcf_margin_pct":1.53,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":645387710000.0,"revenue_yoy_pct":8.39,"gross_margin_pct":17.69,"operating_margin_pct":7.99,"net_income":40015755000.0,"diluted_eps":8.89,"free_cash_flow":-23599076000.0,"fcf_margin_pct":-3.66,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/3711.TW/3711.TW_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**ASE Technology Holding Co., Ltd.** | Earnings Calls | 2026-10-29

**Kenneth Hsiang** (Executives):
Hello. I am Ken Hsiang, the Head of Investor Relations at ASE Technology Holdings. Welcome to our third quarter 2026 earnings release. I am joined today by Joseph Tung, our CFO. Thank you for joining us today. Please refer to our safe harbor notice on Page 2. All participants consent to having their voices and questions broadcast via participation in this event. If you do not consent, please refrain from asking questions or leave the session now. 
I would like to remind everyone that the presentation that follows may contain forward-looking statements. These forward-looking statements are subject to a high degree of risk, and our actual results may differ materially. For the purposes of this presentation, dollar figures are generally stated in New Taiwan Dollars, unless otherwise indicated. As a Taiwan-based company, our financial information is presented in accordance with Taiwan IFRS. Results presented using Taiwan IFRS may differ materially from results using other accounting standards, including those separately presented by our subsidiaries. 
For today's presentation, I'll give a brief business update and then go through the Q3 results. Joseph will close with our Q4 outlook. During the third quarter, our ATM capacities ran at or near full utilization rates. Demand for our services continues to outpace our ability to supply such services within our LEAP and much of our non-LEAP capacities. Our revenues grew faster than we had initially expected, driven primarily by faster-than-expected installations of high-demand LEAP capacities. Non-LEAP also performed slightly better than initial expectations. And even though historically speaking, third quarters tend to be driven by seasonal strength, given the increasing mix of LEAP services, seasonality related to underlying consumer buying patterns are becoming less of a factor in our overall loading patterns. 
Overall, ATM profitability also improved more than anticipated, primarily as a result of higher-than-expected LEAP loading. Our EMS business' third quarter grew slightly ahead of our expectations. The third quarter continues to exhibit strong underlying seasonal demand for our SiP-related products. Our EMS business' profitability was in line with our expectations. 
Please turn to Page 3, where you will find our third quarter consolidated results. For Q3, fully diluted EPS was TWD 5.84 and basic EPS came in at TWD 6.13. Year-to-date through Q3, our fully diluted EPS was TWD 13.40 and basic EPS was TWD 14.17. Consolidated net revenues reached a record TWD 244.2 billion, up 28% sequentially and 45% year-over-year. Gross profit was TWD 54 billion with a gross margin of 22.1%, up 1.1 percentage points sequentially and 5 percentage points year-over-year. The sequential improvement stems from higher LEAP content in our ATM business. The annual improvement reflects higher ATM revenue and a more favorable NT dollar environment. 
Operating expenses totaled TWD 20.8 billion, up TWD 1.8 billion sequentially and TWD 5.1 billion year-over-year, primarily driven by higher headcount, profit sharing expenses and further R&D spend to support LEAP initiatives. As a percentage of revenue, operating expenses declined sequentially by 1.5 percentage points and annually by 0.8 percentage points to 8.5%. Our OpEx percentage declined principally from LEAP revenue growth after previous periods of R&D investment. We currently see operating expenses continuing to rise on an absolute level, but on a percentage basis, should remain near the range demonstrated in the current year. This delivered an operating profit of TWD 33.1 billion, up 57% quarter-over-quarter and 151% year-over-year. We had an operating margin of 13.6%, expanding 2.5 percentage points sequentially and 5.8 percentage points annually. 
Rising company profitability was primarily driven by higher loading and expanding LEAP product mix. Nonoperating loss totaled TWD 0.4 billion. This amount includes net interest expenses of TWD 2.6 billion, up TWD 0.8 billion sequentially due to higher debt levels. Tax expense was TWD 4.8 billion. Our effective tax rate for the quarter was 14.8%. During the quarter, we saw beneficial changes to tax regulations and foreign currency movements, which positively affected our net deferred tax position. Given these changes, we now expect our full year effective tax rate to be between 16% to 17%. Net income for the quarter was TWD 27 billion, up 28% sequentially and 148% year-over-year. 
On Page 4 is a graphical view of our consolidated quarterly performance. For the third quarter 2026, our ATM business represented 62% of our consolidated holding company revenues, while representing 91% of our operating profits. This is compared to 59% of consolidated holding company revenues, while representing 82% of operating profit in the third quarter of last year. As our ATM LEAP business continues to outgrow our other service areas, we continue to believe that our ATM business will continue to increase as a percentage of our overall business and profitability. 
On Page 5 is our ATM P&L. For the third quarter of 2026, we recorded record revenues for our ATM business of TWD 151.5 billion, up TWD 25.3 billion sequentially and TWD 51.2 billion annually, representing an increase of 20% sequential and 51% annual growth. Gross profit for our ATM business was TWD 46.4 billion, up TWD 11.9 billion sequentially and up TWD 23.7 billion year-over-year. ATM gross profit margin was 30.6%, up 3.3 percentage points sequentially and 8 percentage points annually, driven by higher operating leverage and a more favorable revenue mix, particularly a higher mix of LEAP. 
Our gross margin has surpassed our historical structural margin ceiling. A theoretical structural margin for our ATM business would now substantially depend upon the amount of expected LEAP product mix. Given that our LEAP business continues to grow rapidly, our margin range now appears to be dynamic rather than fixed structurally. During the third quarter, operating expenses were TWD 16.2 billion, up TWD 1.5 billion sequentially and TWD 4.3 billion year-over-year. The sequential and annual increases in operating expenses are primarily related to higher overall labor costs and general R&D expenses. Our operating expense ratio was 10.7%, down 1 percentage point sequentially and 1.1 percentage points annually. We are approaching our near-term ATM OpEx percentage target as we balance cost and a more technology-led growth framework. 
During the third quarter, operating profit was TWD 30.2 billion, representing a sequential 53% increase of TWD 10.5 billion and a 178% annual increase of TWD 19.4 billion. Operating margin was 20%, up 4.3 percentage points sequentially and up 9.2 percentage points year-over-year. The NT dollar had a positive 0.5% sequential and a 3.3 annual percentage point impact to our gross and operating margins. 
On Page 6, you'll find a graphical representation of our ATM P&L. The chart currently highlights our gross profit margin. Over the displayed time frame, our margin improvement has been largely driven by improving utilization rates within traditional product lines and increasing LEAP product mix. In this time frame, from peak to trough, our gross profit margin percentage has climbed 8.7 percentage points. 
On Page 7 is our ATM revenue by communications, computing and consumer applications. LEAP services are primarily included within our computing applications with a lesser amount being included in our communications applications. As can be seen here, our computing applications percentage continues to grow steadily. With a large amount of our LEAP services coming from computing, revenues for our computing application grew by 39%. Meanwhile, automotive, industrial and consumer all grew by about 14%. Our communications application had the least amount of growth during the quarter, growing 8%. At this time, we continue to believe that our computing application will lead growth into 2027 and 2028. 
On Page 8, you will find our ATM revenue by service type. At the beginning of the year, we believe that our test business, led by rapid expansion of our wafer sort business would outpace growth of our assembly business. However, during the year, our assembly business has been showing even stronger-than-expected growth, especially as it relates to our traditional businesses. The demand for our test services continues to be robust. However, as with much of our business expansion, test capacities are awaiting new facilities. As stated during the previous quarter, we believe that both our assembly and test businesses will grow at similar rates during the year. 
On Page 9, you can see the third quarter results of our EMS business. Our EMS business has historically focused more on products closer to consumer-driven end markets. Many of these products are experiencing a higher component cost environment driven by shortages caused by the rapid AI build-out. These extra pass-through costs are increasing both our reported revenues and raw material costs. When netted, this ultimately negatively impacts our EMS business' margin performance. 
EMS revenues grew 42% sequentially and 35% annually to TWD 93.5 billion. Sequentially, our EMS business' gross margin decreased by 0.6 percentage points to 8.3%. This change was principally the result of higher pass-through component costs and product mix differences. EMS operating expenses increased by TWD 0.4 billion sequentially and by TWD 0.8 billion annually. Our third quarter EMS operating expense ratio was 5%, declining 1.5 percentage points sequentially and 0.6 percentage points annually. 
Operating margin came in at 3.3%, improving 0.9 percentage points sequentially and declining 0.4 percentage points annually. The sequential margin improvement is the result of product mix offset by a higher component cost environment. The annual decline is the result of higher component costs. Our EMS third quarter operating profit was TWD 3.1 billion, up TWD 1.5 billion sequentially and up TWD 0.6 billion annually. 
On the bottom of the page, you will find a graphical representation of our EMS revenue by application. Generally, the moves in the consumer and communication categories are related to the seasonality of the underlying products we service. And though the communications application percentage looks to have declined on an absolute dollar basis, our EMS communications application grew quarterly. Annually, the communications application percentage declined primarily due to underlying customer production timing changes. The growth in the computing application is largely driven by business related to AI accelerator products. 
From a longer-term perspective, we continue to pursue potential synergies between our ATM and EMS businesses to co-develop system-level solutions. By integrating critical EMS competencies with ATM technologies, we have the potential to optimize entire systems end to end, applying the same co-engineering disciplines that successfully scaled SiP architecture. As complexities increase at the die and package level, the system level will need to follow suit. 
On Page 10, you will find key line items from our balance sheet. At the end of the quarter, we had cash, cash equivalents and current financial assets of TWD 107.9 billion. Our total interest-bearing debt increased by TWD 100.2 billion to TWD 406.5 billion. Total unused credit lines amounted to TWD 457.3 billion. Our EBITDA for the quarter was TWD 58 billion. Our net debt-to-equity ratio this quarter was 66%. As expressed in previous quarters, the third quarter represents the near-term peak of our net debt-to-equity ratio. We expect this ratio to come down somewhat in the fourth quarter. 
On Page 11, you will find our equipment capital expenditures relative to our EBITDA. Machine and equipment capital expenditures for the third quarter in U.S. dollars totaled USD 2.1 billion, of which USD 1 billion was used in packaging operations, USD 1.1 billion in testing operations, USD 41 million in EMS operations and USD 5 million in interconnect materials operations and others. In addition to spending on machinery and equipment, during the quarter, we also spent USD 1.8 billion on facilities and land. We continue to believe that the growth of the company is highly dependent upon the execution of our various facility teams to deliver new manufacturing space and install equipment in those buildings for scaled-up mass production. 
We believe the ability to accelerate CapEx at this point to be beneficial to the company as it allows us to bring in new manufacturing capacity at a time when we are running full. Year-to-date, we have spent USD 8 billion of CapEx, USD 4.8 billion in equipment and USD 3.2 billion in facilities. We currently have 22 ongoing building projects in Taiwan. We expect more than half of these projects will start supporting some level of revenue from now through 2027. 
One final point before handing the presentation off. Our overall business outlook continues to be increasingly defined by our leading-edge capacities. And though our LEAP services are frequently tied to AI-related products, we see our LEAP capacities as the manufacturing basis for future generations of products, not just AI related. Multichip interconnectivity on leading-edge devices has become the norm. We are in the midst of an evolution of electronics production where systemization is increasingly happening at the chip level. Simply put, what we are seeing is the next evolution of miniaturization. It bears repeating the capacities we are putting in place are not specifically made for AI. AI products just so happen to need the performance benefits LEAP interconnections provide. Our investments today are laying the future groundwork for generations of products to come. 
I'll hand the presentation over to Joseph to walk through the company's Q4 outlook.

**Joseph Tung** (Executives):
Thank you, Ken. Let me give everybody a fourth quarter guidance. Based on our current business outlook and exchange rate assumption of USD 1 to TWD 31.9, which remains the same as in third quarter, management projects overall performance for the fourth quarter of 2026 to be as follows: On a consolidated basis, in NT dollar terms, our consolidated fourth quarter revenue should grow by 6% to 8% quarter-over-quarter. Our consolidated fourth quarter gross margin should be between 23% to 24%. Our consolidated fourth quarter operating margin should be between 14.5% to 15.5%. 
For our ATM business, in NT dollar terms, our ATM fourth quarter revenue should grow by 11% to 13% quarter-over-quarter. Our ATM fourth quarter gross margin should increase by 100 to 200 basis points quarter-over-quarter. For EMS, in NT dollar terms, our EMS fourth quarter revenue should be flattish quarter-over-quarter. Our EMS fourth quarter operating margin should be around 2%. 
Now with that, we will open the floor for questions.

**Kenneth Hsiang** (Executives):
[Operator Instructions]

**Operator** (Operator):
[Operator Instructions] Our first question is from Sunny Lin of UBS. Sunny?

**Sunny Lin** (Analysts):
Hello. Could you hear me okay?

**Operator** (Operator):
Yes.

**Sunny Lin** (Analysts):
My first question is on your overall LEAP sales. Given the importance and your accelerating expansion, any update on your LEAP sales for 2027? And how should we think about the split by full process, software outsourcing and test?

**Joseph Tung** (Executives):
For 2027, we're expecting to remain as we last projected to double our LEAP revenue for the year.

**Sunny Lin** (Analysts):
Well, then -- sorry, maybe just to follow up, and that will be my second question. So any update on your LEAP sales for 2026?

**Joseph Tung** (Executives):
Yes. As I said, we are upping our 2026 LEAP revenue from originally USD 3.7 billion that we mentioned last quarter to over USD 4 billion for this year.

**Sunny Lin** (Analysts):
Got it. And...

**Joseph Tung** (Executives):
Go ahead, please.

**Sunny Lin** (Analysts):
Sure. Sorry. Not sure if it's our connection issue, but I lost a part of the response, but it's okay, we will check the transcript. So my second question will be on the full process CoWoS. How's the overall ramp and yield for the key product second half of this year? And now looking into 2027 with your expansion, should we assume a more diversified customer base and product base? And how -- yes.

**Kenneth Hsiang** (Executives):
So Sunny, you're asking about our full process business and then looking for any update in terms of the full process yield and such, right? Is that correct?

**Sunny Lin** (Analysts):
Yield and then the product base going into 2027.

**Joseph Tung** (Executives):
I think for 2026, our full process revenue is on track, and we're keeping a USD 300 million revenue for the year. And I think the -- everything else is going on as planned. And for next year, we are expecting over USD 1 billion revenue coming from full process. And of course, the yield is at the level that we can get into mass production and major shipments.

**Kenneth Hsiang** (Executives):
Does that answer your question, Sunny? Thank you.

**Sunny Lin** (Analysts):
Yes.

**Operator** (Operator):
[Operator Instructions] Okay. Our next question is from Gokul Hariharan of JPMorgan.

**Gokul Hariharan** (Analysts):
Joseph and Ken...

**Operator** (Operator):
Hello, Gokul? Gokul, I cannot hear you. Okay. Next question is from Haas Liu of BoA. Haas? Can you hear me? Okay. Now we go back to Gokul Hariharan of JPMorgan.

**Gokul Hariharan** (Analysts):
Hello? Can hear me?

**Operator** (Operator):
Yes.

**Gokul Hariharan** (Analysts):
Okay. All right. My first question is on gross margins. Could you talk a little bit about where we are seeing this upside in gross margins compared to our guidance range for Q3? It looks like a very clean kind of 150, 200 basis points beat and further upside in Q4 as well. Is it pricing? Or is it your full process is ramping up better in terms of margins? 
And secondly, on the same topic, I think now that we have already exceeded our previous structural range and obviously, the product mix is also different. You're still expecting LEAP to grow faster than the overall product mix. What is the kind of gross margin range we should think about as we think about the next couple of years?

**Joseph Tung** (Executives):
Well, as we continue to ramp up our LEAP business, I think there will be further margin improvement in fourth quarter as well as going into next year. I think the -- at this point, I think the so-called structural margin no longer applies because of the significant and rapidly changing business structures that we are having today. So if we are to comment on our margin, I think the first thing we will say is that the so-called structural margin ceiling has now become the base for us. And looking into next year, I think as we continue to ramp up our overall capacity and also in a very friendly type of pricing environment, we believe that we will continue to see gross margin improvement on a quarterly basis from the base of 30% and we will continue to see sequential improvement in our margin on a quarterly basis for next year as well.

**Gokul Hariharan** (Analysts):
Got it. Just a follow-up there. If you look at the overall portfolio, maybe we leave testing aside within packaging, what would be the highest gross margin that you're able to earn in any of the lead process? Is it already like close to 40% for some of the processes or that is too ambitious?

**Joseph Tung** (Executives):
Can you repeat the question?

**Kenneth Hsiang** (Executives):
Gokul, you're looking for the potential highest-performing margin for LEAP at this point. Is that your question?

**Gokul Hariharan** (Analysts):
Yes. Within the 3 or 4 components that are there, which one is the highest performing? And what are those levels? Just to understand like what is the room for travel in terms of your overall gross margins given your mix is clearly improving quite rapidly?

**Joseph Tung** (Executives):
I don't think we need -- we want to comment on the different margins in different products or different packages. But I think the -- overall, I think the overall LEAP business, both on assembly and test are margin accretive, and we'll continue to see improvement in our margin expansion.

**Gokul Hariharan** (Analysts):
Okay. Okay. Got it. My second question is on -- just a follow-up on your LEAP full process revenues for next year. Joseph, I think you mentioned more than TWD 1 billion, but that sounds quite conservative given you're already doing TWD 300 million in the first quarter of ramp this year. Could you talk a little bit more about your engagements on the full process? And also, if you ramp up all these like 22 projects that you are currently ramping up in terms of facilities, both greenfield and brownfield, what does it mean in terms of, let's say, you ramp it up in 2028? Any indication in terms of what is the investment required from a CapEx perspective? And what does it mean for a continued growth? Does it mean that you continue to grow at similar rates even into 2028, not just for 2027?

**Kenneth Hsiang** (Executives):
Gokul, you're asking about the characterization of our full process business and in certain regards, kind of a total return outlook. Is that correct?

**Gokul Hariharan** (Analysts):
Yes. Total growth outlook given the very sharp ramp in the facilities.

**Joseph Tung** (Executives):
We do have multiple customer engagements at this point, although we are pretty much constrained by our capacity, and we're aggressively building that up. So from the business outlook that we have so far, I think our resource is quite limited. So we are -- although the demand is there, but we're still trying very hard to catch up in terms of supply. And for next year, we are expecting that the demand can be way higher than what we'll be able to deliver. So right now, we're still projecting over USD 1 billion revenue coming from full process. So I guess that's -- I think the biggest bottleneck today is really still the space, although many different areas, we do have -- find ourselves being constrained. But space is really one of the biggest constraint that we're facing today.

**Operator** (Operator):
Our next question is from Laura Chen of Citigroup.

**Chia Yi Chen** (Analysts):
Can you hear me?

**Operator** (Operator):
Yes.

**Chia Yi Chen** (Analysts):
Just want to follow that USD 1 billion like the full process. Can you give us more color about that? What type of the full process will see the contributions next year? And also for our LEAP overall revenue, so obviously, still more driven by the substrate part. But we do see that our companies have various different types of technology. So just wondering, can you give us more color about the growth breakdowns, particularly in the full process in the next 2 years?

**Kenneth Hsiang** (Executives):
Laura, this is Ken. I don't think we have a lot of characterization in terms of what types of full process. I think when we talk about full process, it's generally much more customer specific, too. I think we probably can't really comment that much on that at this point.

**Chia Yi Chen** (Analysts):
Okay. Sure. Understood. So that also seems like the growth into next year is more coming from the substrate part?

**Joseph Tung** (Executives):
Yes. But we are seeing very, very strong demand in test as well. And on assembly and test, we are both seeing a very strong momentum. Again, we are actually being constrained with the capacity buildup. So we're still trying to -- very hard to try to catch up with it. In terms of full process, I think, as I mentioned, we are moving ahead on track. And we hope that we can supply more for next year. And -- but at this point, we are conservatively looking at about over USD 1 billion revenue coming from that. And there are some other new projects that we're entering, for example, CPO, and we're expecting over USD 0.5 billion of revenue coming from CPO as well for next year. That will be included in our LEAP revenue.

**Chia Yi Chen** (Analysts):
That's actually my second question about to ask about the CPO because we see that Jensen earlier last week, he mentioned about that 30x capacity will pick up for next year. So I assume that also, yes, in the LEAP revenues. But will we like going forward to kind of split that revenues breakdown for better like investors' understanding on that part growth?

**Joseph Tung** (Executives):
I think we will -- we are kind of breaking it down already in terms of OS, in terms of full process, in terms of wafer sort and as I mentioned, CPO.

**Chia Yi Chen** (Analysts):
Okay. So if I may also check on that, do we have any expectation on the CPO revenue contributions in 2 years?

**Joseph Tung** (Executives):
In 2 to 3 years?

**Chia Yi Chen** (Analysts):
Yes.

**Joseph Tung** (Executives):
No, we have a projection for next year, but we'll see -- we'll have better clarity after we finish what we're setting up to do for now.

**Operator** (Operator):
Our next question is from Haas Liu of BoA.

**Haas Liu** (Analysts):
Yes. Can you hear me now? Sorry, I was disconnected.

**Operator** (Operator):
Yes.

**Haas Liu** (Analysts):
Congrats on the great results. I think just a quick follow-up on the structural gross margins where you already reported the third quarter ICDM gross margins up to slightly higher than 30 percentage. So with your LEAP business set to be even higher in the next couple of quarters and also your mainstream packaging and testing business utilization, pricing are actually also improving. Can we use third quarter gross margin as a base case going forward for your LEAP -- for your overall ICDM gross margin assumptions as long as the cycle holds?

**Joseph Tung** (Executives):
Yes. As I mentioned earlier that we're now using our structural margin ceiling as a base for next year.

**Haas Liu** (Analysts):
Okay. So we can use like this kind of roughly 30% of the gross margins as the base case for next year. Got it. And then...

**Joseph Tung** (Executives):
We will see quarterly improvement for next year as well.

**Haas Liu** (Analysts):
Okay. Sequential improvement. And then second thing is just on CapEx. This year, you are already spending based on what you reported just now, you have already been spending 80% to 90% of your annual budget, which has been revised up twice year-to-date to USD 10.5 billion on CapEx. Would you be able to provide some update on that since there's still like a few months to end this year? And looking into 2027, how should we think about that trajectory as one of your foundry partner also just now announced to buy another panel fab. Should we also expect similar acquisition of the fabs or the facilities by ASE as well and also more equipment procurement in the next couple of quarters to meet your customers' demand?

**Joseph Tung** (Executives):
Yes. As I said, the space continues to be a constraint -- one of the constraints that we have, and we are aggressively seeking for suitable existing plants for us to buy. But there are -- when your competition is pretty keen and there are really not that many suitable factories for us to pursue at this point. So it's an ongoing effort that we're putting in. And also for this year's CapEx, we are increasing our CapEx for the year from USD 10.5 billion to USD 11.5 billion now. We're adding USD 1 billion, another USD 1 billion. And of that USD 1 billion, half of it will be for facilities as we continue to fill up our new factories. And the other half will be for equipment and 60% of it will be for LEAP and 40% will be for the mainstream events.

**Haas Liu** (Analysts):
Got it. Got it. And just on the overall pricing environment across your LEAP versus the mainstream packaging and testing business, how should we think about -- since the supply/demand is still pretty tight and that...

**Kenneth Hsiang** (Executives):
Sorry to stop you there. You're on question #3.

**Operator** (Operator):
Our next question is from Gokul Hariharan of JPMorgan.

**Gokul Hariharan** (Analysts):
A couple of follow-ups from my side. So Joseph, I think you mentioned CapEx USD 11.5 billion, higher by USD 1 billion. Could you give an opinion on what you're thinking CapEx is going to look like next year? Are we still in an upward sloping curve for CapEx? And could you also talk a little bit about are you entering into any prepayment arrangements or anything like that with customers given a lot of this new CapEx seems to be targeted at some of the key customers itself? Yes, that's my first question.

**Kenneth Hsiang** (Executives):
Gokul, you're looking for an update on our CapEx outlook going forward?

**Gokul Hariharan** (Analysts):
Yes. And the kind of any funding arrangements that you have, repay...

**Joseph Tung** (Executives):
And the funding sources around it. Well, we'll continue to see very strong demand coming in, and we do have a very strong prospect for next year as well. So at this point, I believe the CapEx spending for next year will be even larger than this year. And as we continue to ramp up our capacity. Also in terms of R&D, we will continue to make the necessary investment to carry our missions. 
Funding-wise, we will continue to use whatever -- we do have multiple cost-effective sources for us to raise funds to support our growth. I think at this point, we are not shy -- we will not be shy from making the necessary investment to support the expansion. So I think for next year, we will continue to see negative cash flow. But I think this thing will be balanced off in due course. In terms of -- as I mentioned, multiple funding sources that will also include some of the trade financing that we can arrange with the different customers.

**Gokul Hariharan** (Analysts):
Understood. And the second question is on the test business. Could you characterize the growth of the test business going into next year, final test versus chip probing? And I think how constrained are you on test versus packaging? Like if you think about on a relative scale, is the constraints on test bigger than packaging from a facility or equipment perspective?

**Kenneth Hsiang** (Executives):
Gokul, you're looking for an update in terms of looking at the test business going into next year, and then in terms of the growth rates relative to what we're seeing in terms of the market. Is that correct?

**Gokul Hariharan** (Analysts):
Yes. Relative to packaging and relative to -- like constraints relative to packaging as well.

**Joseph Tung** (Executives):
I think same pattern will -- like in the third and fourth quarter of this year, it will repeat into next year. I think in terms of assembly, it should -- the growth rate should outpace test, given the limited resource that we have. And also for test under the current resource constraint, we will need to prioritize our investment to more on wafer probe rather than final test.

**Gokul Hariharan** (Analysts):
Okay. Would you say test is more constrained in terms of your capacity versus demand compared to packaging or it is largely similar?

**Joseph Tung** (Executives):
I think it's mostly space. I think the space that we use for assembly is more efficient than test at this point. So given the constraint, we will allocate -- we will put our priority on assembly and for test will be for wafer sort.

**Operator** (Operator):
Our next question is from Haas Liu of BoA.

**Haas Liu** (Analysts):
I think just a quick follow-up on the CapEx. A couple of your peers, including the one in Korea and also your foundry partner mentioned that they are preparing for a significant or a meaningful step-up on the CapEx for next year. Given this is the first -- the third time of CapEx upward revision for the year for ASE in 2026, do you still -- do you also expect a similar statement to hold for your CapEx for next year? You already mentioned that next year's CapEx will be higher than this year. But just wondering whether that kind of aggressiveness will be applied to ASE as well.

**Kenneth Hsiang** (Executives):
Haas, you're looking for a characterization of how we view next year's investments...

**Haas Liu** (Analysts):
Yes. in a qualitative way as compared to your peers comment for a meaningful step-up or significantly higher than this year's CapEx. Does those -- do those statements also hold for your CapEx outlook?

**Kenneth Hsiang** (Executives):
Haas, generally, we don't necessarily view our own CapEx relative to competitors or, I guess, peers in the market. In general, we do see that CapEx going into next year, we do see a lot of opportunity in terms of the business that will be available to us. And as Joseph previously mentioned, we will not be shy in terms of investing to get at that business. Does that answer your question?

**Haas Liu** (Analysts):
Okay. Yes. And just a related follow-up on the CapEx one is probably more specifically on the CPO that one of your key customers last week in its Germany event said it will hike CPO capacity by 15% next year at your facilities and then double again in 2028. Would you be able to share more detail on that? What is your role in CPO packaging and testing? What is the related CapEx you expect to spend? And how should we expect -- or try to -- or quantify the related revenue contribution from that part of the business in the next few years from CPO based on your customers' statements?

**Kenneth Hsiang** (Executives):
Haas, you're looking for a clarification in terms of the potential joint press release that we had with our customer on the CPO?

**Haas Liu** (Analysts):
Yes.

**Joseph Tung** (Executives):
Well, I don't think we will comment on specific product or specific customer. What we're saying is overall, we are the -- I think we are the most active participant in the whole CPO effort and joining with our foundry partner as well as our customer and just from the business that we are projecting to have from our customers, we're expecting to generate more than USD 0.5 billion worth of revenue coming from CPO for next year.

**Haas Liu** (Analysts):
For next year. Okay. Yes. And my second question would be just on the pricing environment across your LEAP business and also the mature -- or mainstream packaging and testing business. It seems that the supply tightness is actually happening across the board. Would you be able to share some detail on how that pricing improvement has been helping your gross margin improvement in the third quarter? And into 2027, how should we expect the pricing negotiation with your customers at this stage to help your gross margin expansion beyond the product mix improvement?

**Joseph Tung** (Executives):
Well, I will not comment on pricing, except we will continue to look for the most suitable pricing strategy depending on the situation. And all I can say is, overall, I think both for LEAP as well as for general market, I think we are in a very pricing-friendly environment at this point.

**Haas Liu** (Analysts):
Okay. Okay. And could you also just try to quantify the...

**Kenneth Hsiang** (Executives):
Haas, I think you're on question #4.

**Operator** (Operator):
Our next question is from Charlie Chen of Morgan Stanley.

**Charlie Chan** (Analysts):
So just a quick follow-up, right? Thanks for disclosing your CPO revenue. So if we may, can we know roughly is the testing part, for example, insertion 3, insertion 4, a bigger revenue contribution or the substrate is a bigger contribution for that USD 0.5 billion revenue contribution?

**Joseph Tung** (Executives):
I won't be able to comment on that, sorry.

**Charlie Chan** (Analysts):
Okay. No worries. Yes. And secondly, I think management mentioned you wouldn't hesitate to kind of invest in space capacity, whatever to gain share, right? But recently, there seems to be some industry dynamic that one of TSMC's subsidiary, they're also getting into the on-substrate business, right? Do you think there is like demand overflow or it's kind of a real competition to your on-substrate business?

**Kenneth Hsiang** (Executives):
Charlie, you're asking for commentary in terms of competition within our LEAP business.

**Charlie Chan** (Analysts):
Yes. Because now it seems like demand is not an issue. But my question is that who seems to have the space can really gain share, right? Is that a fair comment? Because one of the TSMC's subsidiaries is kind of ordering lots of equipment. So we are a little bit worried whether that's kind of gaining share at expense of ASE.

**Joseph Tung** (Executives):
It's kind of sensitive to talk about our foundry partners, subsidiary situation. And all I can say is given the scale, I think we are really the dominant player in this field. And whatever competition, I think, is out of necessity from our foundry partners as well as our customers. So I don't think -- at this point, I don't think it will move the needle that much in terms of overall market share kind of situation. As I said, we are still in a catch-up mode, trying to supply as much as we can to meet the demand. So I think that's all I can say at this point.

**Charlie Chan** (Analysts):
Got you. At least, there wouldn't be any so-called price competition, right? It's like demand is too big, whoever can squeeze more space or capacity can gain share, but don't worry about pricing and margin.

**Joseph Tung** (Executives):
I think the sheer scale difference is I don't think a price war will be created.

**Charlie Chan** (Analysts):
Makes sense. Yes. And if I may, non-AI. So we start to pick up some data points on PC and smartphone order cuts at the wafer front end. So except for iOS ecosystem, right? So Joseph or Ken, can you share your observation about non-AI part of business and how that is going to impact your kind of midterm outlook?

**Joseph Tung** (Executives):
Well, at least for this year, I think the general market growth is well ahead of our expectation in the earlier part of the year. I think we will have more than 20% growth in our general market business as well. That's largely -- we all understand that cell phone and PC is going through a very soft period given the high component prices that's kind of hurting the overall demand. But that is more than compensated by the recovery of automotive and industrial and more importantly, AI adjacent chips requirement. So we're seeing very strong growth in this year for general market, and we're expecting that to happen again in next year as well.

**Operator** (Operator):
Next question is from Sunny Lin of UBS.

**Sunny Lin** (Analysts):
I have a question on very high level, what's your view on CPO versus NPO. Besides CPO, could ASE also capture the opportunity in NPO as well? And then based on your commentary, would it be fair to say that based on the current visibility, it's fair to say that 2027 CPO will be able to ramp up even with still some technical challenges or optimization that the industry need to go through?

**Kenneth Hsiang** (Executives):
Sunny, you're looking for an update in terms of how we view the CPO versus NPO market and then our capability to ramp up to support CPO going forward. Is that correct?

**Sunny Lin** (Analysts):
Yes. Or maybe just CPO as a technology, is it mature enough to start mass production for your key clients in 2027?

**Joseph Tung** (Executives):
Yes. As I mentioned earlier on CPO, we're expecting mass production. We already started mass production in quarter 4, and that will continue into 2027. And as we are projecting at this point, we're looking at over USD 0.5 billion worth of revenue coming from CPO. In terms of NPO and CPO, I think they will both coexist. And it's just a matter of difference in terms of overall performance between the 2 different types of packages.

**Sunny Lin** (Analysts):
And for MPO, will ASE be able to capture as well?

**Joseph Tung** (Executives):
If there is real demand, yes, of course, we will be a major player in that.

**Sunny Lin** (Analysts):
Got it. And a quick question on EMS. So looking at the shared [indiscernible] is a bit different. And how should we think about the growth going to Q1? Typically, Q1 should be a down quarter as the build moderates. But this time around, the flagship smartphone clients are also launching for lower-end models going to early 2027. And so all things considered, how should we think about your EMS business maybe going to first half of 2027?

**Kenneth Hsiang** (Executives):
Sunny, you're looking for the seasonal pattern of our EMS business as potential underlying customer products change their timing of release. Is that correct?

**Sunny Lin** (Analysts):
Right.

**Joseph Tung** (Executives):
Well, we will continue to expect some growth going into 2027 as well for EMS business. I think the main focus will be on the high-performance computing. And at this point, it represents roughly mid-teens of our overall EMS revenue, and we're seeing that ramping up rapidly. And communication-wise or consumer-wise, it will be -- at this point, it's -- relative to computing, it's weaker. But all in all, I think the -- our EMS will continue to move into optical, silicon photonics and power-related type of devices. And also, of course, AI-related business that we'll be focusing on. So yes, we do expect further growth, particularly in the AI-related part of the business.

**Operator** (Operator):
Next, we have Haas Liu of BoA coming back again.

**Haas Liu** (Analysts):
It's me again. I'm just wondering if you could provide more clarity on the gross margins improvement in third quarter. How much of that is coming from the product mix improvement versus the like-for-like price hike across your LEAP versus -- and the mainstream business and your utilization improvement? Because if we look at the trend in the past 8 quarters or 7 quarters that you already have experienced 2 step-ups on the gross margins back in the second half of last year. And now in the third quarter this year, there's another step-up. So as you accelerate your LEAP business, I think -- going forward, in addition to the question I just had now on the third quarter gross margin breakdown on the -- from the relative benefits. I think just going forward, may I also check on your expectation, whether that kind of gross margin improvement will further accelerate through 2027.

**Kenneth Hsiang** (Executives):
Haas, you're looking for further clarification in terms of what has caused our margin pick up during the third quarter and then whether those types of improvements are sustainable going forward? Is that correct?

**Haas Liu** (Analysts):
That's right.

**Joseph Tung** (Executives):
Third quarter margin improvement is largely because of the LEAP ramp-up as well as overall improvement in utilization across the board, including the general market or mainstream packages and test. And going forward, as we continue to ramp up our LEAP business and having a healthy growth on the general market business as well. I think, yes, we will continue to see sequential improvement in our margin on a quarterly basis going into next year.

**Haas Liu** (Analysts):
Okay. And I think just a follow-up on the application mix. In third quarter, your computing business is seeing a nice ramp. Would you be able to share more detail on that? And what are the key applications are you targeting in that segment in the next 1 to 2 years between GPUs, CPUs, ASICs and networking switches?

**Kenneth Hsiang** (Executives):
Haas, you're looking for an answer in terms of the composition of our compute business. Is that correct?

**Haas Liu** (Analysts):
Yes. And your targeted application in the next few years between GPUs, CPUs, ASICs and networking switches.

**Kenneth Hsiang** (Executives):
I don't know if we can comment so specifically. Yes. I think from a targeting perspective, we should be targeting everything. We can't be particularly specific. But in terms of our technologies, we do hope to be able to address all applicable products within that high-performance computing section. Do you have another question, Haas?

**Haas Liu** (Analysts):
No, I am good for now.

**Kenneth Hsiang** (Executives):
Okay. I think you're the last question then. Do we have any other questions online?

**Operator** (Operator):
No, no more questions.

**Kenneth Hsiang** (Executives):
Thank you, everyone, for attending the call. Joseph, do you want to...

**Joseph Tung** (Executives):
We had a fabulous third quarter, and we'll continue to see strong momentum going into fourth and into next year. We will make the necessary investment to support the overall expansion, and we'll continue to expect good results for the fourth quarter as well as for next year. Thank you very much.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 3711.TW_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Joseph Tung｜guidance：Q3 合併營收預期季增 21%～22%（以 USD1=TWD31.9 假設）（原話："our consolidated third quarter revenue should grow by 21%"）
- 2026-07-30｜Joseph Tung｜guidance：Q3 ATM 營收季增 11%～13%（原話："our ATM third quarter revenue should grow by 11% to 13%"）
- 2026-07-30｜Joseph Tung｜margin：Q3 ATM 毛利率指引 28%～29%（Q2 實際 27.3%）（原話："Our ATM third quarter gross margin should be between 28% to"）
- 2026-07-30｜Joseph Tung｜guidance：Q3 合併毛利率與營益率指引（逐字稿原文毛利區間寫為 12.5% to 21.5%）（原話："Our consolidated third quarter gross margin should be"）
- 2026-07-30｜Joseph Tung｜guidance：Q3 EMS 營收預期季增約 40%、營益率 3.2%～3.4%（原話："our EMS third quarter revenue should grow by around 40%"）
- 2026-07-30｜Joseph Tung｜margin：管理層拆解 EMS 季增 40% 為記憶體等零組件漲價所致，剔除後為一般季節性（原話："this is largely because of the component price hikes"）
- 2026-07-30｜Joseph Tung｜margin：Q3 EMS 若剔除零組件漲價，營益率約回到 3.7%～3.8%；記憶體為轉嫁成本（原話："the operating margin will be very similar to typical"）
- 2026-07-30｜Joseph Tung｜guidance：EMS 全年成長低於 20%，ATM 全年成長 35% 以上；Q4 EMS 營收與 Q3 相近（原話："EMS at this point, I think the full year is a sub-20% kind"）
- 2026-07-30｜Tien Wu｜guidance：全年 ATM 營收預期成長 35%（美元口徑）（原話："So for the full year, we expect the ATM business revenue to"）
- 2026-07-30｜Tien Wu｜guidance：一般（非 LEAP）業務全年成長指引由 13% 上修；逐字稿該句數字有勘誤標註（30% 更正為 20%）（原話："general segment is expected to grow by 30% (sic) [ 20% ]"）
- 2026-07-30｜Joseph Tung｜guidance：今年 LEAP 營收追蹤優於先前 35 億美元指引，並以 2027 年 LEAP 營收翻倍為目標（原話："we are aiming to double our LEAP revenue in 2027"）
- 2026-07-30｜Joseph Tung｜guidance：CFO 量化今年 LEAP 超標幅度為再增數億美元（原話："we will be adding another couple of hundred million dollars"）
- 2026-07-30｜Joseph Tung｜capital_allocation：今年資本支出再加 20 億美元（廠房與設備各 10 億）（原話："So the total is adding another USD 2 billion for CapEx."）
- 2026-07-30｜Joseph Tung｜capital_allocation：全年 CapEx 總額約 105 億美元，其中廠房設施 40 億、設備 65 億（原話："$4 billion will be for new factory buildings and facilities"）
- 2026-07-30｜Joseph Tung｜capital_allocation：設備 CapEx 拆解：封裝 56%、測試 40%，且約 70% 用於先進製程（原話："it's about 56% is for assembly, 40% for test and the"）
- 2026-07-30｜Joseph Tung｜capital_allocation：目前 13 個新建案與 8 個購入舊廠改建案，足以支撐到 2028 年並可能到 2029 年部分期間（原話："I think the current projects will be sufficient for us to"）
- 2026-07-30｜Joseph Tung｜capital_allocation：CFO 承認負自由現金流將持續，並稱有多種低成本資金來源（原話："the negative cash flow situation will remain for some time"）
- 2026-07-30｜Joseph Tung｜commitment：CFO 表示不會在必要投資上卻步（原話："we are not going to be shy in making the necessary"）
- 2026-07-30｜Joseph Tung｜margin：Q4 ATM 毛利率可能超過 30% 結構性上限，屆時將檢討調整結構性區間（Q2 ATM 毛利率 27.3%）（原話："fourth quarter ATM gross margin likely to exceed our"）
- 2026-07-30｜Joseph Tung｜commitment：管理層明言若調整結構性毛利率區間，方向為向上（原話："when I say adjust, I mean upward adjustment"）
- 2026-07-30｜Joseph Tung｜margin：管理層對定價環境與成本轉嫁的說法（原話："we can definitely pass on these cost increases to our"）
- 2026-07-30｜Kenneth Hsiang｜margin：Q2 ATM 毛利率 27.3%，季增 1.3 個百分點，歸因於稼動率槓桿與 LEAP 比重提高（原話："driven by higher operating leverage and a more favorable"）
- 2026-07-30｜Kenneth Hsiang｜margin：Q2 合併毛利率 21.0%，年增拆解為結構性效率與有利匯率（原話："The annual improvement reflects both structural efficiency"）
- 2026-07-30｜Kenneth Hsiang｜margin：Q2 營業外收益 46 億元含潛在非經常性項目（評價利得 42 億、避險利得 15 億）（原話："the increase primarily reflects some potentially"）
- 2026-07-30｜Kenneth Hsiang｜margin：Q2 有效稅率 16.4%，全年仍預期 18%（原話："We continue to expect an effective tax rate of 18% for the"）
- 2026-07-30｜Kenneth Hsiang｜margin：預期下半年 ATM 營業費用率持續改善（原話："We expect our ATM operating expense ratio should continue"）
- 2026-07-30｜Kenneth Hsiang｜margin：Q2 EMS 毛利率降 0.6 個百分點至 8.9%，原因為產品組合與零組件成本（原話："The sequential margin decline is the result of product mix"）
- 2026-07-30｜Kenneth Hsiang｜risk：短期成長受限於設備安裝與廠房建置；Q2 綜合稼動率 80%～85%（原話："Our blended utilization rate for the quarter was between"）
- 2026-07-30｜Tien Wu｜risk：COO 稱需求不是疑慮，不確定性在自身執行能力（原話："So the business demand is not a concern. It's our own"）
- 2026-07-30｜Joseph Tung｜risk：同時推進約 20 個建案，管理層點出對營建夥伴的執行壓力（原話："we really need to have a very, very efficient and very"）
- 2026-07-30｜Kenneth Hsiang｜product：Q2 測試與組裝增速敘事變化：組裝（特別是傳統打線）強於年初預期，現預期兩者全年增速相近（原話："We now believe that both our assembly and test businesses"）
- 2026-07-30｜Joseph Tung｜product：自有整廠製程（full process）今年營收約 3 億（逐字稿原文為 TWD 300 million），進度符合預期並積極擴產（原話："this year, we said that we're going to have about TWD 300"）
- 2026-07-30｜Joseph Tung｜product：full process 毛利尚未完全反映，預期未來為毛利accretive業務（原話："full process will also be another margin accretive business"）
- 2026-07-30｜Tien Wu｜product：自家面板製程全自動產線 2027 Q1 開始量產，規格 310x310；玻璃基板未來 12 個月不會量產（原話："our fully automated line will start production by Q1 of"）
- 2026-07-30｜Tien Wu｜product：CPO 年底前可能小量啟動，管理層表示兩季後再提供細節（原話："somewhere along the line towards the end of the year, the"）
- 2026-07-30｜Tien Wu｜commitment：管理層承諾約兩季後提供 2027 LEAP 營收組成（OS、full process 等）細項（原話："Probably 2 quarters from now, we'll give you a better color."）
- 2026-07-30｜Joseph Tung｜guidance：2027 年 CapEx 預期仍大，但具體金額要再等約一季（原話："I know it's going to be big, but how big?"）
- 2026-07-30｜Tien Wu｜competition：對 Intel EMIB 的說法：不視為威脅，純代工定位下可相容（原話："I don't think there's a potential threat. Again, we are a"）
- 2026-07-30｜Tien Wu｜customer：與主要客戶約定先在台灣建全自動產線，之後再遷往美國或其他地區（原話："we will develop and build fully automated efficient line in"）
- 2026-07-30｜Tien Wu｜customer：Q3/Q4 客戶皆要求更多產能，COO 稱公司處於產能受限的位置（原話："all of our customers are asking for more devices for Q3 and"）
- 2026-07-30｜Tien Wu｜customer：一般元件強勁需求來自工業、電源、連接與儲存，並稱將優於整體半導體市場（原話："I believe we will outperform the general market"）
- 2026-07-30｜Tien Wu｜competition：管理層對競爭優勢的定位：純封測無利益衝突（原話："no conflict with foundry, with no conflict with substrate"）

### 問答異常語氣（迴避／改口／保留）
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Sunny Lin 追問 2027 LEAP 翻倍的拆解（full process／OS／測試）與客戶別組成｜答法：COO 與 CFO 未給拆解數字，兩度表示約兩季後再提供更多細節；CFO 僅稱組合與今年相似
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Charlie Chan 質疑 2027 LEAP 翻倍與 2.5D／測試增速、NVIDIA 與 CoWoS 擴產預期是否吻合｜答法：CFO 未回應數字對帳，改談組裝涵蓋 full process 與其他製程步驟及新封裝
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Haas Liu 追問 Q4 毛利率超過上限，成熟製程與 LEAP 各貢獻多少｜答法：CFO 未拆解貢獻比重，改列多項因素（高毛利業務、效率、自動化、營運槓桿）
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Charlie Chan 詢問客戶說下半年大幅漲價是否屬實，及是漲傳統或先進封裝｜答法：CFO 未直接確認或否認漲價幅度，僅稱定價環境友善、成本可轉嫁
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Haas Liu 要求今年 CapEx 分項及明年哪塊成長較快｜答法：CFO 先以客戶需求籠統回答，未給明年分項；總額與分項在後續追問才補出
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Gokul Hariharan 詢問 2027 CapEx 是否續升｜答法：CFO 僅稱會很大，但拒絕給幅度，請等約一季
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Sunny Lin 詢問 CPO 服務內容與營收何時有意義｜答法：COO 表示要等兩季再談 CPO 服務、營收與 2027 展望，未給時程或數字

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
{"date":"20261019","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價≤500 元（約 2027 共識 EPS 17 倍）且封測毛利率仍≥27%、LEAP 倍增指引未下修","irr_base_pct":0.1,"ev5y_pct":4.5,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":1.3,"ev5y_pct":4.5,"irr_base_pct":0.1,"max_dd_pct":-60,"bull_5y_price":1210.0,"bear_5y_price":312.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價≤500 元（約 2027 共識 EPS 17 倍）且封測毛利率仍≥27%、LEAP 倍增指引未下修","price_at_dd":670.0,"archetype":"循環/商品","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3711.TW_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
