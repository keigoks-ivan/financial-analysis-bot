你是 stock-analyst **v20 判斷 agent**，標的 TER（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TER","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TER_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TER_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1306.0,"period":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","citation":"公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益","value":412.9,"period":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","citation":"公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm"}},{"id":"f_kpi2_non_gaap","label":"Non-GAAP 營業利益率","value":31.6,"period":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","citation":"公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm"}},{"id":"f_kpi3_gaap","label":"GAAP 營業利益","value":402.0,"period":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","citation":"公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm"}},{"id":"f_kpi4_gaap","label":"GAAP 營業利益率","value":30.8,"period":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","citation":"公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm"}},{"id":"f_kpi8_q4_fy2026_1_300","label":"管理層 Q4 FY2026 指引：營收區間（中值 1,300）","value":"1,250–1,350","period":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","citation":"公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ter_gross_margin_pct","label":"TER 毛利率","value":59.41,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TER.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ter_operating_margin_pct","label":"TER 營業利益率","value":33.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TER.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ter_fcf_margin_pct","label":"TER FCF 利潤率","value":21.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TER.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_6857_t_gross_margin_pct","label":"6857.T 毛利率","value":65.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6857.T.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_6857_t_operating_margin_pct","label":"6857.T 營業利益率","value":45.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6857.T.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_6857_t_fcf_margin_pct","label":"6857.T FCF 利潤率","value":31.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6857.T.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_form_gross_margin_pct","label":"FORM 毛利率","value":44.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FORM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_form_operating_margin_pct","label":"FORM 營業利益率","value":15.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FORM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_form_fcf_margin_pct","label":"FORM FCF 利潤率","value":16.67,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FORM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cohu_gross_margin_pct","label":"COHU 毛利率","value":43.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHU.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cohu_operating_margin_pct","label":"COHU 營業利益率","value":-6.19,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHU.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cohu_fcf_margin_pct","label":"COHU FCF 利潤率","value":6.68,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHU.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_keys_gross_margin_pct","label":"KEYS 毛利率","value":64.69,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KEYS.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_keys_operating_margin_pct","label":"KEYS 營業利益率","value":20.25,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KEYS.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_keys_fcf_margin_pct","label":"KEYS FCF 利潤率","value":22.32,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KEYS.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_313_6_86_3_agent","label":"自由現金流（營業現金流 313.6 − 資本支出 86.3，本 agent 自算）","value":227.3,"period":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","citation":"公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm"}},{"id":"f_kpi6_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":5.4,"period":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","citation":"公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm"}},{"id":"f_kpi7_non_gaap_eps","label":"Non-GAAP 稀釋 EPS","value":2.29,"period":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）","citation":"公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":274.37,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-20.51,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":28.85,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.44 → 9.44）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.25,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.87 → 11.9）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.7,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（15.81 → 15.92）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":9.44,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":11.9,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":15.92,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":10.28,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 8.56 → 9.44（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":31.54,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝26.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":26.6,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":8.57,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝67.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":67.3,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":8.5,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝67.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":67.4,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":29.06,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 9.44，分子＝快照價 274.37","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.186,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-329.47,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 137.12、現金 466.59（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":156.12,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":42506.48,"period":"2026-11-02","unit":"USD m","basis":"市值 42835.95 ＋ 淨負債 -329.47","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":5230.16,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（16 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":6518.41,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":8.13,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 274.37 / W52 316.39 / W104 211.64 / W250 149.55 / W250 13週斜率 1.83%"},{"id":"f_ma_w52","label":"52 週均線","value":316.39,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":211.64,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":149.55,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.83,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列名半導體測試對手為 Advantest、SPEA、Cohu，並指出面臨新興亞洲公司與客戶內部自製供應的競爭","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"Competitors in the Semiconductor Test segment include, among others, Advantest Corporation, SPEA S.p.A., and Cohu, Inc.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：面臨新興亞洲公司及數家客戶內部開發的競爭，且美國貿易法規未必約束部分對手","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"We also face competition from emerging Asian companies and internal development at several of our customers.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 稱貿易限制使其在部分市場競爭力受限，因部分對手不受同樣限制","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"current trade restrictions are limiting our ability to be competitive, particularly in certain markets, where some competitors are not subjected to the same restrictions.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Futurum：Q2 FY2026 Teradyne 出貨首筆 merchant GPU 訂單，並在第二家超大型雲端客戶完成 correlation，為 2027 年份額提升鋪路","source":"Futurum Group, Teradyne Q2 FY 2026 Doubles Semiconductor Test Revenue","url":"https://futurumgroup.com/insights/teradyne-q2-fy-2026-doubles-semiconductor-test-revenue-on-ai-compute-and-memory-demand/","excerpt":"Teradyne shipped its first merchant GPU order and completed correlation at a second hyperscaler, steps that widen its compute customer base and set up share gains in 2027.","as_of":"2026-08-03","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Seeking Alpha：Advantest 與 Teradyne 雙寡占份額消長，稱 Advantest 2025 年取得顯著份額","source":"Seeking Alpha, Advantest/Teradyne: Market Share Shifts In This Duopoly","url":"https://seekingalpha.com/article/4837312-advantest-teradyne-market-share-shifts-in-this-duopoly","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2025 10-K：前五大直接客戶占營收 44%（2024 為 36%、2023 為 32%）；一家半導體測試客戶占 19%（含他人指定的營收）；失去或大幅減少大客戶需求可能造成重大不利影響。","source":"SEC EDGAR 10-K FY2025（經 WebSearch 摘要轉述，未逐字取得原文）","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":null,"as_of":"2026-02-19","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"第三方分析稱 Teradyne 正爭取成為 Nvidia GPU 測試的第二供應商（UBS 分析師亦有此看法），非公司官方揭露；Futurum 摘要稱 Q2 2026 出貨首張 merchant GPU 訂單並完成第二家 hyperscaler 的 correlation。本次搜尋未找到任何最大客戶導入 TER 之外第二供應商或自製測試機的 2026 來源。","source":"WebSearch 摘要（dcf-analysis.com / Futurum Q2 FY2026）","url":"https://futurumgroup.com/insights/teradyne-q2-fy-2026-doubles-semiconductor-test-revenue-on-ai-compute-and-memory-demand/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 前五大直接客戶占營收 44%（2024: 36%、2023: 32%）；兩家指定客戶驅動 12%、10%，另一家直接客戶占 19%（含他人指定）；失去重要客戶可能有重大不利影響，且幾乎無合約追索權。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"In each of the years, 2025, 2024 and 2023, our five largest direct customers in aggregate accounted for 44%, 36% and 32% of consolidated revenues, respectively.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025/12/31 應收帳款中兩家客戶分別占約 22% 與 20%（2024 年底各 10%）；公司稱持續做客戶信用評估，必要時要求信用狀。","source":"SEC EDGAR 10-K FY2025 Item 7A","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"As of December 31, 2025, two customers primarily of our Semiconductor Test segment accounted for approximately 22% and 20%, respectively, of our accounts receivable balance. As of December 31, 2024, two customers of our Semiconductor Test segment each accounted for 10% of our accounts receivable balance.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"搜尋未發現 2026 年主要客戶信用降級、破產或下修財測的報導；Teradyne 預告 Q3 2026 營收 12–13 億美元，高於分析師預期。","source":"WebSearch 摘要（Teradyne Q2 2026 相關報導）","url":null,"excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SEMI 2026 年中預測：全球半導體設備銷售 2026 年 1,659 億美元（+23%），2028 年達 2,295 億美元，連續第五年成長；測試設備 2027 年預估 +18.1%、2028 年 +13.6%（測試設備金額數字來源有疑義）","source":"SEMI press release: Global Semiconductor Equipment Sales Forecast to Reach a Record $229 Billion in 2028","url":"https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-forecast-to-reach-a-record-229-billion-dollars-in-2028-semi-reports","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Wolfe Research 分析師認為 2028 年前幾乎不可能出現半導體供過於求（TSMC 售罄、新晶圓廠需多年興建）","source":"247WallSt: Top Chip Analyst: Semiconductor Oversupply Is Nearly Impossible Before 2028","url":"https://247wallst.com/investing/2026/07/30/top-chip-analyst-semiconductor-oversupply-is-nearly-impossible-before-2028-why-hes-bullish-on-memory/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ASML 預期其規劃的晶片設備供給在 2027、2028 年仍不足以滿足客戶需求","source":"techenclave: ASML expects planned chipmaking-tool supply to fall short in 2027 and 2028","url":"https://techenclave.com/news/items/asml-expects-planned-chipmaking-tool-supply-to-fall-short-in-2027-and-2028","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"測試設備廠面臨 FPGA、CPU、GPU、驅動 IC 等關鍵零組件嚴重短缺，交期拉長（Digitimes 引 The Elec）；另 36Kr 引韓媒稱測試設備 FPGA 交期由 8–10 週拉至最長 52 週","source":"Digitimes 2026-06-01 / 36Kr","url":"https://www.digitimes.com/news/a20260601VL218.html","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Teradyne Q2 FY2026：Compute 約占 SoC 營收 70%、YoY 近 +600%；記憶體測試連續三季 >2 億美元；出貨首張 merchant GPU 訂單，並完成第二家超大規模客戶 correlation，設定 2027 年份額成長；分析師指出訂單不平均、客戶集中","source":"Futurum: Teradyne Q2 FY 2026 Doubles Semiconductor Test Revenue on AI Compute and Memory Demand","url":"https://futurumgroup.com/insights/teradyne-q2-fy-2026-doubles-semiconductor-test-revenue-on-ai-compute-and-memory-demand/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["moat_trend","thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"AI 相關需求占 Teradyne Q1 FY2026 營收近 70%，Q4 FY2025 約 60%","source":"Futurum: Teradyne Q1 FY 2026 Earnings Credit Revenue Growth to AI Test Demand","url":"https://futurumgroup.com/insights/teradyne-q1-fy-2026-earnings-credit-revenue-growth-to-ai-test-demand/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"有分析稱各主要廠商對同一需求訊號採相同多年期建廠時程，新增供給集中在 2027–2029 窗口，存在供過於求路徑風險（二手評論，未核原文）","source":"Creative Strategies / stockwirex 評論","url":"https://stockwirex.com/?p=30660","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Q3 2026 10-Q 的法律程序章節描述訴訟屬例行（專利、僱傭、商業、環境），預期無重大不利影響；未提反壟斷調查","source":"SEC EDGAR 10-Q（期末 2026-09-27）","url":"https://www.sec.gov/Archives/edgar/data/0000097210/000119312526441091/ter-20260927.htm","excerpt":"Teradyne is subject to various legal proceedings and claims which have arisen in the ordinary course of business such as, but not limited to, patent, employment, commercial and environmental matters.","as_of":"2026-10-30","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Q1 2026 10-Q 揭露美國出口管制合規已限制公司在部分地區的競爭能力，未來規則變動可能帶來重大成本","source":"SEC EDGAR 10-Q（期末 2026-03-29）","url":"https://www.sec.gov/Archives/edgar/data/0000097210/000119312526201058/ter-20260329.htm","excerpt":"regulations relating to import-export control, technology transfer restrictions, and other laws and regulations. Additionally, U.S. and foreign governmental authorities have taken, and may continue to take, administrative, legislative or regulatory action that could impact our operations. We believe that our operations are in material compliance with applicable trade regulations.","as_of":"2026-05-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K FY2025：關稅與出口管制（含商務部對中國客戶限制）已限制公司在部分市場的競爭力；近期關稅變動至今未造成重大不利影響，但未來新增關稅可能有重大影響。","source":"SEC EDGAR 10-K FY2025 Item 1/1A","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"We are subject to tariffs and restrictions from the dynamically changing global trade environment. While it is difficult to quantify the exact impact, current trade restrictions are limiting our ability to be competitive, particularly in certain markets, where some competitors are not subjected to the same restrictions.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：部分中國半導體公司被列入實體清單，對公司與這些客戶的業務已有且將持續有不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"The addition of certain of these companies to the Entity List has had and will continue to have an adverse impact on our business with these customers.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：供應商受關稅與出口限制規範，可能影響零組件供應或提高價格。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"Our suppliers are subject to trade regulations, including tariffs and export restrictions imposed by the United States Government and by the governments of other countries. These regulations could impact our suppliers’ ability to provide us with components for our products or could increase the price of those components.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K MD&A：FY2025 貿易法規遵循成本不重大。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"The costs we incurred in complying with applicable trade regulations for the year ended December 31, 2025 were not material, however, compliance with these laws has limited our ability to compete in certain regions.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Section 232 對半導體及半導體製造設備課徵關稅，2026-01-15 生效，25% 稅率（有特定用途豁免）。","source":"Baker Donelson","url":"https://www.bakerdonelson.com/new-section-232-tariffs-on-semiconductors-and-a-new-plan-of-action-regarding-critical-minerals","excerpt":"President Trump has imposed tariffs on semiconductors, semiconductor manufacturing equipment, and their derivative products under Section 232 of the Trade Expansion Act of 1962, effective January 15, 2026. Imports of semiconductors and certain derivative products are subject to a 25 percent tariff, unless the products are for use in certain applications that are deemed","as_of":"2026-01-15","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Teradyne 的 FY2025 10-K 指出供應商受美國及他國關稅與出口限制約束，可能影響零件供應或價格","source":"Teradyne 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"Our suppliers are subject to trade regulations, including tariffs and export restrictions imposed by the United States Government and by the governments of other countries. These regulations could impact our suppliers' ability to provide us with components for our products or could increase the price of those components.","as_of":"2026-02-27","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Teradyne 10-K（FY2014/2007 版）表示部分零件為單一來源，單一來源供應商延遲或停供會造成暫時衝擊","source":"Teradyne 10-K FY2014 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000097210/000119312515067671/d829718d10k.htm","excerpt":"While the majority of our components are available from multiple suppliers, certain items are obtained from sole sources.","as_of":"2015-02-27","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2018 10-K：產品及供應商零件越來越多在中國與馬來西亞生產","source":"Teradyne 10-K FY2018 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312519059974/d652525d10k.htm","excerpt":"an increasing portion of our products and the products we purchase from our suppliers are sourced or manufactured in foreign locations, including China and Malaysia","as_of":"2019-02-28","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2024 10-K：新出口管制已影響對部分中國客戶的銷售","source":"Teradyne 10-K FY2024 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/97210/000095017025023784/ter-20241231.htm","excerpt":"Compliance with the new export controls has impacted our ability to sell products to certain customers in China.","as_of":"2025-02-28","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"Teradyne 將半導體製造自中國遷出（蘇州）","source":"The Machine Maker","url":"https://themachinemaker.com/news/teradyne-relocates-semiconductor-manufacturing-from-china/","excerpt":null,"as_of":"2025-01-01","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#5","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"測試業務製造仰賴合約製造商，主要在馬來西亞","source":"PolicyRisk","url":"https://policyrisk.com/world/company/TER","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"TER Q3 2026 營收 $1,306M（Q3'25 為 $769M）；Semiconductor Test $1,072M，較 Q2 的 $1,122M 下降 4.5%（自 2025 Q2 以來首次季減），Memory 與 Integrated Systems Test 創紀錄；Robotics $96M（Q2 $100M）首次獲利；Product Test $138M；Q4 指引 $1,250–1,350M","source":"Teradyne Form 8-K Ex.99.1 Q3 2026 results（SEC）","url":"https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"1H26 Semiconductor Test 營收 $2,232.6M 對去年同期 $1,034.4M；Robotics $191.2M 對 $143.9M","source":"Teradyne Form 10-Q (quarter ended 2026-06-28)","url":"https://www.sec.gov/Archives/edgar/data/0000097210/000119312526327715/ter-20260628.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"管理層預期 2027 年續成長（記憶體、compute 專案、產能擴張）；AI 相關營收占總營收逾 60%；主要 compute 客戶雙供應商策略可能自 2027 起逐步提升 TER 市占；ATE 市場 2030 年前達 $20B 以上；實體 AI 較大規模採用約 2028；compute 訂單時點與行動裝置疲弱為下半年風險","source":"Zacks, Teradyne Q3 Earnings Call Highlights AI Demand and 2027 Growth Plans","url":"https://www.zacks.com/stock/news/3018941/teradyne-q3-earnings-call-highlights-ai-demand-and-2027-growth-plans","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"Advantest 在 SoC 測試機市占：2024 報導稱 2023 年 Advantest 約 50% 對 TER 約 30%；第三方電子報稱 CY25 Advantest SoC 市占由 56% 升至 66%（未經核實）；TER Q2 2026 call 稱 fast follower 階段市占預期從零增至約 30%。未找到 2026 明確定價/ASP 資料","source":"Nasdaq/Zacks 與 datagravity、earningswhispers Q2 2026 transcript（搜尋摘要）","url":"https://earningswhispers.com/transcript/TER/Q22026","excerpt":"during the fast follower phase, we expect market share to grow incrementally from zero up to about 30%","as_of":"2026-07-29","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"SEMI 2026 年中預測：全球設備銷售 2026 年 $165.9B（+23.2%），2028 年 $229.5B；測試設備 2026 年 $15.3B（2025 年 +55.3%），2028 年 $20.8B。前版（2025-12）預測測試設備 2026 +12.0%、2027 +7.1%，已被上修取代","source":"SEMI press release via controleng / emsnow / iconnect007","url":"https://www.controleng.com/?p=135339","excerpt":null,"as_of":"2026-07-14","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"SEMI 2026 年中預測測試設備 $15.3B","source":"SEMI via emsnow","url":"https://www.emsnow.com/?p=55265","excerpt":"After surging 55.3% in 2025, semiconductor test equipment sales are projected to increase 31.0% to $15.3 billion in 2026, marking a strong upward revision from SEMI’s 2025 year-end forecast.","as_of":"2026-07-14","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Teradyne 10-K 風險因子：電子、半導體與機器人產業的產品常被技術更先進的替代品取代，舊技術需求下降時售價下滑；若無法推出新技術，營收與財務狀況可能受不利影響。未點名具體替代技術。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"In the electronics, semiconductor, and robotics industries, products are often replaced by more technologically advanced substitutes and, as demand for older technology falls, the price at which such products can be sold drops. If we cannot advance new technologies to meet our customers’ demands, our revenues and financial condition may be adversely impacted.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"第三方文章稱傳統 ATE 無法抓到 AI 工作負載所有重要缺陷，催生系統級測試等相鄰測試層；Advantest 與 Teradyne 在高階 ATE 合計約 90% 份額（第三方估計）。","source":"Wing VC, The Chip Testing Bottleneck","url":"https://wing.vc/content/the-chip-testing-bottleneck","excerpt":"in short supply, the financial fingerprint of a duopoly with a captive AI accelerator customer base. Where the next leg of growth comes from The interesting part of the story isn’t ATE itself. It’s the adjacent test layers that have emerged because traditional ATE no longer catches every defect that matters in an AI workload. System-Level Test (SLT).","as_of":"2026-06-01","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：Teradyne 以直銷為主，僅 Robotics 產品主要經經銷商與 OEM 銷售；未見通路結構性轉變敘述。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"We sell in these areas predominantly through a direct sales force, except for Robotics products, which are sold principally through distributors and OEMs.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-28 Q3 指引 EPS $1.85–2.15、營收 $1.2–1.3B，高於當時共識 EPS $1.43、營收約 $1.0B；營收區間自前次 $1.15–1.25B 上調","source":"MarketBeat: Teradyne issues Q3 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/teradyne-nasdaqter-issues-q3-2026-earnings-guidance-2026-07-28/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 EPS $2.47 vs 共識 $2.04（+21.1%），營收 $1.3B vs 預估 $1.2B；近 8 季皆優於共識（Chartmill/聚合站，日期未明）","source":"Chartmill TER estimates","url":"https://www.chartmill.com/stock/quote/TER/estimates","excerpt":null,"as_of":"2026-10-17","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Chartmill 顯示 FY2026 EPS 共識 9.18 美元（19 位分析師，2026-10-17）；各站 FY26 EPS 數字差異大（TIKR 6.24、Barchart 5.75、MarketBeat 7.2），口徑/日期不一","source":"Chartmill TER estimates","url":"https://www.chartmill.com/stock/quote/TER/estimates","excerpt":null,"as_of":"2026-10-17","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"目標價分布：Bullstory 2026-08-26 為 15 位分析師 Buy、均價 $449.80、區間 $350–$550；JPMorgan 2026-07-30 將目標價由 $450 升至 $465（Overweight）；其他聚合站均價 $348–$437 不一，as-of 不一致","source":"Bullstory TER forecast; MarketBeat 7/28","url":"https://bullstory.io/en/stocks/ter/forecast","excerpt":null,"as_of":"2026-08-26","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"+","claim":"2026-04-16 Teradyne 收購半導體測試開發與驗證軟體公司 TestInsight，金額未揭露；2026-04 為 MLTP 成立與 TestInsight 收購合計支付 1.667 億美元（來自 10-Q 摘要）。","source":"Business Wire：Teradyne Acquires TestInsight Accelerating Time to Market for AI and Data Center Devices；10-Q FY2026 Q1","url":"https://secure.businesswire.com/news/home/20260416215846/en/Teradyne-Acquires-TestInsight-Accelerating-Time-to-Market-for-AI-and-Data-Center-Devices","excerpt":null,"as_of":"2026-04-16","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-08-07 簽訂 10 億美元五年期擔保循環信用額度（PNC 為行政代理），申報時未動用。","source":"SEC EDGAR 8-K（2026-08-10）Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526342367/ter-20260807.htm","excerpt":"The Credit Agreement provides for a five-year, senior secured revolving credit facility of $1.0 billion (the “Credit Facility”).","as_of":"2026-08-10","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共6份，僅1份含重大項目（為信用額度 Item 1.01），其餘為財報、股東投票。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000097210&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"+","claim":"2026-04-16 Teradyne 收購 TestInsight（測試軟體），金額未揭露。","source":"Business Wire：Teradyne Acquires TestInsight","url":"https://secure.businesswire.com/news/home/20260416215846/en/Teradyne-Acquires-TestInsight-Accelerating-Time-to-Market-for-AI-and-Data-Center-Devices","excerpt":null,"as_of":"2026-04-16","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K 風險因子以假設語氣寫「若涉入證券訴訟」，搜尋亦只找到 2001–2004 年舊案，近12個月未見集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm","excerpt":"If we were to become involved in securities litigation, it could subject us to substantial costs, divert resources and the attention of management from our business, and adversely affect our business, results of operations, financial condition, and cash flows.","as_of":"2026-02-19","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K清單中僅1份重大項目（Item 1.01 信用額度），無 Item 4.02（重編）項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000097210&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"TER","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":59.41,"operating_margin_pct":33.17,"fcf_margin_pct":21.59,"rd_intensity_pct":11.78},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TER","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"6857.T","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":65.73,"operating_margin_pct":45.86,"fcf_margin_pct":31.21,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6857.T","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"FORM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":44.1,"operating_margin_pct":15.95,"fcf_margin_pct":16.67,"rd_intensity_pct":13.19},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FORM","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"COHU","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":43.95,"operating_margin_pct":-6.19,"fcf_margin_pct":6.68,"rd_intensity_pct":18.6},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHU","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"KEYS","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.69,"operating_margin_pct":20.25,"fcf_margin_pct":22.32,"rd_intensity_pct":18.13},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KEYS","as_of":"TTM ending 2026-07-31（4季加總）"}}],"subject":"TER"},"financial_history":{"ticker":"TER","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":3155045000.0,"revenue_yoy_pct":null,"gross_margin_pct":59.18,"operating_margin_pct":26.91,"net_income":715501000.0,"diluted_eps":4.22,"free_cash_flow":414674000.0,"fcf_margin_pct":13.14,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":2676298000.0,"revenue_yoy_pct":-15.17,"gross_margin_pct":57.42,"operating_margin_pct":19.52,"net_income":448752000.0,"diluted_eps":2.73,"free_cash_flow":425589000.0,"fcf_margin_pct":15.9,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2819880000.0,"revenue_yoy_pct":5.36,"gross_margin_pct":58.48,"operating_margin_pct":19.58,"net_income":542372000.0,"diluted_eps":3.32,"free_cash_flow":474081000.0,"fcf_margin_pct":16.81,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":3190024000.0,"revenue_yoy_pct":13.13,"gross_margin_pct":58.22,"operating_margin_pct":21.59,"net_income":554047000.0,"diluted_eps":3.47,"free_cash_flow":450406000.0,"fcf_margin_pct":14.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TER/TER_Q3_2026_Earnings_Call_20261028.md）

# Q3 2026 Earnings Call
**Teradyne, Inc.** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Ladies and gentlemen, good morning, and welcome to the Teradyne Third Quarter 2026 Earnings Conference Call. [Operator Instructions] As a reminder, today's call is being recorded.
I would now like to turn the call over to Amy McAndrews, Vice President of Corporate Relations for Teradyne. Please go ahead.

**Amy McAndrews** (Executives):
Thank you, operator. Good morning, everyone, and welcome to our discussion of Teradyne's most recent financial results. I'm joined this morning by our CEO, Greg Smith; and our CFO, Michelle Turner.
Following our opening remarks, we'll provide details of our performance for the third quarter of 2026 and our outlook for the fourth quarter. The press release containing our third quarter results was issued last evening. We are providing slides as well as a copy of these prepared remarks on the Teradyne Investor website that may be helpful in following the discussion. Replay of this call will be available via the same page after the call ends.
The matters that we discuss today will include forward-looking statements that involve risks that could cause Teradyne's results to differ materially from management's current expectations. We caution listeners not to place undue reliance on any forward-looking statements included in this presentation. We encourage you to review the safe harbor statement contained in the slides accompanying this presentation as well as the risk factors described in our annual report on Form 10-K for the fiscal year ended December 31, 2025, on file with the SEC. Additionally, these forward-looking statements are made only as of today.
During today's call, we will refer to non-GAAP financial measures. We have posted additional information concerning these non-GAAP financial measures, including reconciliation to the most directly comparable GAAP financial measures, where available, on our Investor website.
Looking ahead between now and our next earnings call, Teradyne expects to participate in a technology-focused investor conference hosted by UBS. Our quiet period will begin at the close of business on December 18, 2026. Following Greg and Michelle's comments this morning, we'll open up the call for questions. This call is scheduled for 1 hour. Greg?

**Gregory Smith** (Executives):
Thanks, Amy. Good morning. AI was the driver again this quarter. Total company revenue topped $1.3 billion, up 70% year-over-year and consistent quarter-over-quarter, with non-GAAP EPS of $2.29, up over 150% year-over-year. All 3 of our business groups, Semi Test, Product Test, and Robotics, grew versus the prior year, highlighting AI demand across all parts of the business.
AI-driven revenue represents more than 60% of total revenue, a key proof point that our wafer to data center strategy is delivering results. From wafers to modules to trays to racks and into full data centers, Teradyne equipment is used to build and test the high-performance computing that underpins the growth of agentic AI.
We've previously discussed our long-term perspective on the AI transformation of the semiconductor industry and global economy. The first wave started back in 2024 with the build-out of general-purpose data centers, which were used for both model training and inference. In 2026, we are in the early stages of the second wave where data centers are optimized to serve these models to support agentic AI and inference on a global scale. The third wave is physical and edge AI.
While there are already compelling examples of physical and edge AI in automotive, robotics and wearables, the full impact of AI on these segments is still to come. The strength of these waves gives us great confidence in our mid-term growth plans.
Let's start with Semiconductor Test. The demand for compute is far greater than supply, and the semiconductor industry is seeing dramatic expansion in capacity to meet this burgeoning demand. The portion of semi CapEx associated with test is increasing as well, from 6.4% in 2025 to 8.1% for the first 8 months of 2026. With forecasts for semiconductor CapEx being revised upward for '27, '28, and beyond, we believe that the conditions are ripe for prolonged expansion of the ATE TAM.
CPUs and AI accelerators are key drivers of the expansion. Through our accelerated investments, Teradyne is positioned for continued growth in both the overall ATE market and share gains, driven by customers adopting dual vendor strategies. Dual vendor provides greater assurance of getting capacity when needed, minimizes the risk of supply chain disruptions, and ensures that the test capability in -- that the test capability arrives in time for new device technologies. Dual vendor programs progress through several phases over multiple quarters, including initial qualification, fast follower, and mature dual sourcing.
We have multiple customers at different stages of this process. Our first hyperscaler customer is in the mature phase, and we expect our next major ramp in the middle of 2027. Our merchant GPU customer is in the fast follower phase with multiple devices in development, and we expect to see additional revenue in 2027. Our second hyperscaler customer has passed qualification and is now in fast follower with an expectation of capacity buys in the second half of 2027. We also have a third hyperscaler in initial qualification.
Networking devices, both copper and optical, are growing proportionately with compute. The majority of this TAM is in switches. However, retimers and DSPs are driving significant business. The majority of the networking market is currently copper and optical pluggables. Over the next few years, we believe the NPO and CPO markets will grow strongly from a small base.
We are working with leaders in this segment on solutions across all test insertions, and it is clear that there are many different approaches and technologies being tried by different customers. As a result, the types of tests and the handling and alignment techniques are in flux. The key to our strategy here is to develop strong open-ecosystem -- to develop strong open-ecosystem partnerships for instrumentation, handling, and alignment.
We have spoken before about our partnerships with Technoprobe and ficonTEC, and we have just announced a partnership with FormFactor to address optical tests amongst other opportunities. Our open, non-exclusive ecosystem of probing, handling, and interface partners allows us to validate complete test cell solutions before they reach our customers' floors, giving them more interoperability, full control over their supply chains and lead times. This provides a faster path to high-volume production.
The pace of innovation in compute and networking has accelerated, and we have been investing in R&D to ensure that our product road map is aligned with those needs. We've discussed before that there is no current ATE solution for the most complex next-generation AI and data center devices that are coming to market in 2027. The trio of new UltraFLEXplus instruments that we just introduced address that need.
The first is the UltraPin5000-EM. The EM stands for extended memory. This instrument has up to 80x deeper memories than our current instrument for intensive device characterization work. The second instrument is the UltraVS64-HP. The HP stands for high power. This instrument enables testing accelerators that consume up to 15,000 amps. And finally, the UltraPort-PCIe6. This is the industry's first ATE solution for PCIe Gen6.
We also introduced the Iris 100, a solution for optical test of microLED and VCSEL emitters. This instrument serves both mobile applications and optical networking. To assure data center reliability and uptime, customers are increasingly turning to system-level test and burn-in. In the third quarter, we introduced new burn-in capabilities for the Titan HP platform, which enables full system test coverage across burn-in temperature ranges.
As AI moves out of the data center and into cars, robots, and wearables as part of the third wave of AI, mobile processors and microcontrollers are adding neural processing units and other AI features. To address that coming market, in the third quarter, we launched the UltraFLEXplus S, a small footprint system that covers both engineering and production insertion for edge AI devices.
Moving on now to memory. Memory manufacturers are bringing on more capacity for HBM, DDR, LPDDR, and flash memories. More capacity means more wafers, more wafers means more bits and more units, which means more -- which means more to test in memory. In the past 2 quarters, it has become clear that the constraints on memory supply are so severe that AI accelerators are turning to lower stack heights of HBM memory to get a larger number of stacks out of the same volume of DRAM wafers.
This will tend to increase the TAM for HBM performance test, an area where we have higher share. The HBM, DDR, LPDDR, and GDR (sic) [ GDDR ] markets are moving quickly from generation to generation with higher data rates and new encoding approaches. To support these new technologies, in the third quarter, we introduced the Magnum E2, our next-generation DRAM tester with the signal integrity and throughput needed to keep pace with our memory customers.
Linear and power segments, which were previously driven mainly by automotive and industrial verticals, are adding capacity to deliver data center power distribution and regulation components. Our product revenue in the automotive and industrial space has grown from less than $400 million in 2025 to over $600 million in 2026. This trend will accelerate with new 800-volt standards and new technologies like IVR.
The demand for AI accelerated compute goes beyond the semiconductor market. The need for nearline storage in data centers has accelerated the annual exabyte growth for HDD to over 20% in 2026. Since the test time for HDD is more closely related to the capacity than the unit volume, this, as well as adding a third major customer, is driving expansion of our HDD test revenue.
Scale-up networking to support large GPU clusters is predominantly served by copper connections via backplanes and cable spines running at unprecedented data rates. This has turned backplanes and cables from commodities to highly engineered and tested elements of the HPC system, which is driving significant growth in TDR and BERT test equipment served by our MLTP joint venture. In addition, we have seen strong demand for our Omnyx board test products. Together, these contributed to almost 30% quarter-over-quarter growth for the entire Product Test Group.
Increasingly, exotic packaging and materials are being used in data center tray assemblies. These trays demand superhuman accuracy and stamina to build. ODMs and CMs are increasingly turning to flexible physical AI-based robots to assist in assembly and test processes. As a result, electronics and semiconductor is now our largest vertical for Robotics.
In the third quarter, we introduced the Universal Robots Gen 7 cobot platform. The features of this platform and PolyScope X have been tailored precisely to bring physical AI to electronics assembly workcells and provide a platform for UR+ partners to plug into, to support the diverse requirements of server and rack build.
To sum up, our wafer to AI data center strategy is delivering. Within the third quarter, outside of compute, the rest of our portfolio delivered close to 80% of our overall sales. The R&D that we have been investing has yielded next-generation products. These products allow us to capture opportunity along the entire value chain from wafers to modules to trays to racks. Our continued investment reflects our optimism about the near- and medium-term opportunities in front of us.
This was another strong quarter where AI was the driver across our business groups. We are riding a rising tide. AI has driven the semiconductor and electronics industry into a new era, and our wafer to data center strategy has positioned us to benefit from these positive changes.
With that, I'll turn the call over to Michelle.

**Michelle Turner** (Executives):
Thanks, Greg, and good morning, everyone. Let's get into the quarter, beginning with the total company. Both revenue and non-GAAP EPS came in above the high end of our guidance range, as our wafer to data center strategy and the breadth of our portfolio sustained positive momentum.
For the third consecutive quarter, total company sales remained at the high watermark of $1.3 billion. For the first 9 months of 2026, we delivered $3.9 billion in revenue and $7.31 of non-GAAP EPS, up over 85% and 235% year-over-year, respectively, driven by all things AI. Building on that, let's take a deeper look at revenue, starting with Semi Test.
Our Semi Test team once again cleared $1 billion in revenue, up 77% from Q3 2025. The revenue breakdown within Semi Test was SoC at $676 million, memory at $301 million, and IST at $95 million. As expected, compute order timing was predominantly offset by strength across the rest of the Semi Test portfolio.
Starting with SoC, compute revenue grew nearly 50% year-over-year on continued AI-related demand. As Greg mentioned, our customers' dual vendor strategies are opening up more opportunities for us in compute, and we expect healthy growth in 2027. Auto and industrial continued to strengthen, up nearly 90% year-over-year, driven primarily by power management demand increases for AI data center build-outs. Mobile was up 60% year-over-year from a low base, but remains below historical levels and a muted part of the overall SoC portfolio.
Now turning to memory. Our memory business delivered another record quarter at $301 million in revenue, up from the previous record set just last quarter. This represents our fourth consecutive quarter of revenue over $200 million, driven by continued robust HBM and DRAM test solutions demand and the resurgence in NAND.
Finally, turning to IST. Revenue in the quarter reached a new record at $95 million, up approximately 150% from the prior year with continued strength in AI-related HDD storage demand from all 3 major suppliers in this space.
Now on to the Product Test Group. Revenue was $138 million, up 56% year-over-year. The group experienced broad-based growth tied to AI infrastructure build-outs, from production board test to optical to high-speed interconnect. Book-to-bill for the quarter was 1.4x with particular strength in the newest addition to the group, MultiLane Test Products JV, as the need for data center interconnect test solutions increases. Robotics revenue was $96 million, up 28% year-over-year. Our Robotics group delivered its highest third quarter revenue ever and also achieved profitability within the quarter. AI-related revenue remains elevated with robot-assisted test and assembly across the data center value chain in high demand.
In the first 9 months of the year, AI-related revenue was roughly 20%. Aligned with the third wave of AI Greg mentioned, the physical and edge AI ecosystem is in early innings and building momentum. Our Robotics group has announced partnerships with industry leaders such as NVIDIA and Analog Devices as well as innovative start-ups, including Scale AI, Generalist, Bright Machines, and Sereact. These partnerships reflect growing interest in physical AI.
Now moving down the P&L. Gross margins for the quarter were 59.1%, up 60 basis points year-over-year, driven by strong volume and product mix, while sequentially gross margins were down 70 basis points, driven primarily by product mix. As expected, OpEx increased, driven by more R&D and go-to-market investment in support of future growth. Finally, non-GAAP operating income was $413 million with an operating margin of 31.6%.
Now moving to capital allocation. Reinvesting in the business remains our top priority. In 2026, we will invest close to $1 billion across R&D and CapEx with R&D investments representing a double-digit percentage of our sales. Beyond that, our strategy is to maintain the cash reserves to grow the business, return capital to shareholders through both dividends and share repurchases, and keep dry powder available for accretive M&A.
Each pillar of our capital allocation strategy is focused on innovating from wafer to data center, positioning us well over the near and midterm. We ended the quarter with cash and investments of $625 million, up 21% from last quarter. We had free cash flow of $227 million in the quarter. For the first 9 months of 2026, free cash flow was $806 million, up nearly 250% from the prior year period. Additionally, from a working capital perspective, we increased our inventory in support of future revenue growth. We paid $20 million in dividends in the quarter, and our share buybacks were $99 million.
Now looking ahead to our fourth quarter guidance. For the quarter, we expect revenue in the range of $1.25 billion to $1.35 billion and non-GAAP EPS of $1.95 to $2.25. Gross margins are expected to be in the range of 57.5% to 58.5%, reflective of product mix and new product launches. Operating expenses are expected to run at 28.5% to 29.5% of fourth quarter sales, driven by continued investments in R&D and go-to-market. The non-GAAP operating profit rate is expected to be between 28% and 30%. Our Q4 guidance midpoint of $1.3 billion represents growth of approximately 20% over last year's fourth quarter, which would bring full year revenue to approximately $5.2 billion, up over 60%.
We expect Q4 will be our fourth consecutive quarter of revenue above $1.25 billion, representing a sustained step change in the business from a year ago. As we said last quarter, we expect 2027 to be another year of healthy growth. Our strengthening backlog and the growth in compute give us momentum, and we expect to carry and build throughout the year.
For your modeling purposes, we expect the FormFactor investment to close in the fourth quarter, subject to regulatory approval and customary closing conditions. The breadth of our portfolio is in full effect in the second half as memory, auto and industrial, IST, Product Test, and Robotics grow, offsetting second-half program timing in compute.
In closing, Q3 was another quarter of strong execution. AI demand continued to pull through every part of our portfolio from the chips that power it to the systems, interconnects, and robots that build it. This is what our wafer to data center strategy is designed to capture.
As we look to the fourth quarter and into 2027, the demand signals across our end markets remain strong, and we look forward to sharing an updated target earnings model on our Q4 call.
I'll close by thanking all of our Teradyne team members around the world for the hard work and dedication that drives our results and positions us well for the opportunities ahead. 
With that, operator, we're ready for questions.

**Operator** (Operator):
[Operator Instructions] We'll take our first question from C.J. Muse with Cantor Fitzgerald.

**Christopher Muse** (Analysts):
I guess first question on memory. You obviously put up a record number for September. I'm curious how we should think about the trajectory of that business into December. And then moreover, as you think bigger picture into '27, I know it's early, you're going to save that for February, your outlook. But as you sit here today and as you look at your book-to-bill, how are you thinking about maybe the rank order of growth between HBM, traditional DRAM, and NAND?

**Gregory Smith** (Executives):
Hi C.J., it's Greg. So looking out to Q4, we think memory is going to continue at a really strong level. And going into '27, given all of the fab expansion that is coming online in '27, we're expecting significant growth for the memory business year-on-year. And you were asking in terms of like what segment is going to drive most of the growth. We would say that like this year, HBM was probably the biggest thing that drove the growth of the memory TAM. Flash came back pretty strong and DRAM was surprisingly strong based on what we were thinking at the beginning of the year. Looking at next year, I think HBM is the star. There's going to be growth across all of the segments of memory, but I think the biggest impact is going to be in HBM growth.

**Christopher Muse** (Analysts):
Very helpful. And then maybe on your gross margin guide and the strength in the 1.4x book-to-bill you highlighted for Product Test. How should we think about Product Test sequentially? I'm assuming that's up. And is that what's driving gross margins lower? And as you think about that business next year, what impact does that have to what we should be thinking about as a more normalized gross margin for Teradyne?

**Michelle Turner** (Executives):
Yes. So I'll start with the gross margins, and then we can talk a little bit about Product Test. So within the quarter, gross margins came in at 51.1% (sic) [59.1%]. This is up 60 basis points from Q3 last year. Within the Q4 guide, we're also guiding up about 80 basis points in comparative to last year. And then if you extrapolate that for full year, our overall gross margins for the year will be about 59.4%, which is up about 110 basis points year-over-year.
So we're at the low end of the earnings model that we just put out in January, and we're going to expect to update that in the Q4 call. So thinking about the 3 segments, C.J., Product Test is actually accretive to the overall portfolio. So as you think about modeling for Q4 and into next year, we expect that to continue to be true. As you think about gross margins for 2027, I'd put it in a couple of buckets in terms of headwinds and tailwinds.
From an overall headwinds perspective, I would say volume, we're going to have another year of healthy growth when you think about the overall portfolio, along with some elements of mix as we think about next year. Tailwinds, though, from an overall cost perspective, we are continuing to see cost pressures, inflationary pressures just across the overall ecosystem across supply, along with potential expanded capacity next year as well.
And so as we look at second half of next year, we're continuing to see robust demand signals. So to the extent that we're continuing to build on our capacity, that will also be an expense that we would expect next year as well. I don't know if you've got anything else?

**Gregory Smith** (Executives):
You misspoken [ a bit ]. You said 51.1%. I think you meant 59.1%.

**Michelle Turner** (Executives):
59.1%, yes.

**Gregory Smith** (Executives):
I just want to make sure that, that doesn't stay out in the atmosphere.

**Michelle Turner** (Executives):
No, I [ misstated ] that.

**Gregory Smith** (Executives):
But I completely agree with what you said that there are kind of, I'd say, equal up and down forces in terms of gross margin going into 2027.

**Michelle Turner** (Executives):
Yes. And the only other thing I would add, C.J., in terms of Q4 and comparative to Q3, and Greg referenced that kind of the continued growth in memory, and we certainly expect that. We do expect, though, that Q3 was the record quarter within 2026. 
So we think there's a bit of a digestion period, although it's going to continue to grow from Q4 of last year. We expect that compute was at its lowest within Q3. And so we expect that, that's going to start to reaccelerate from a growth perspective in Q4. And then to your point, we also expect Product Test and Robotics to grow within fourth quarter as well.

**Operator** (Operator):
We'll move on now to Timothy Arcuri with UBS.

**Timothy Arcuri** (Analysts):
You're in kind of the shape of the year. So this year kind of played out, you got this big step-up in Q1, and then it was basically flat throughout the year, Greg. Inventory, though, is up like $200 million over the past 6 months. So obviously, you're portending a pretty big year next year. Can you speak to that?
And I guess, particularly, it sounds like both your first and your second hyperscale customers are a little more back-end loaded next year. So does that mean like next year is going to be a back-end loaded year? Should we think of the first half as kind of flat versus the back half of this year and then a big step-up in second half next year? I ask because people are sort of thinking that it's more of a ratable ramp for the year. So if you can help us shape that, that would be great.

**Gregory Smith** (Executives):
So I think there are 2 things that are driving the increase in inventory that you're seeing. One is you're right, we are preparing for robust growth in 2027. The other is that many of the components that we're procuring to build these testers, the lead times for those have gone out as well. So we are needing to essentially put on order and take inventory against sort of a longer lead time of our inputs. So there's sort of 2 things going on there. I don't think it's a good idea to just sort of extrapolate from that number to a pure growth number.
In terms of how next year breaks down, we'll have a lot more to say about that in our Q4 call. But I will tell you that in terms of the ASIC programs, I think you're right. I think they are going to tend to be more back-half loaded. But I don't particularly expect -- I think it's going to be a strong year all around, and we'll talk more about the phasing next quarter.

**Timothy Arcuri** (Analysts):
Okay. And I guess just, Greg, on the share gain pace, so last night, your competitor was kind of -- I mean, they keep pushing back on losing any share. And in the release last night, there were some allusions to their contract manufacturing partners adding a bunch of supply for them. So how do you see your lead times affecting the pace of the share gains? Like, are you being proactive enough about adding -- having your supply chain add enough for you to keep lead times when you need them so that your customers don't just go to them and place orders with them?

**Gregory Smith** (Executives):
Yes. So we've talked a lot about this in prior calls that we've added significant capacity already for our primary SoC test platform, the UltraFLEXplus. We're actually at like 4x the capacity that we were about 18 months ago. And we are essentially planning our next capacity step-up for that platform. In addition, we've employed a dual vendor strategy for our own supply chain. So in 2026, we qualified a second CM to build that platform.
We're in the process of doing that for our memory test platform as well. And we are aggressively adding capacity for both memory and our Eagle power test line. So we are definitely looking to increase our capacity. We are doing our best to try to hold our lead times. One thing that is a little bit different is we're holding our lead times but customers are giving us probably better forecast information about when they are going to need capacity in advance of placing those orders.
So we have a pretty good viewpoint going out further than we did before, and that's helping us map out exactly what we need to do for capacity planning. We're doing our best to try and hold our lead times. I would say that if demand comes in that we haven't heard anything about from a forecasting perspective, the drop-in place for that is probably longer than it was a year ago. But we're doing our best in terms of procuring material and expanding capacity so that we can still be very responsive to spot demand.

**Operator** (Operator):
We'll move next to Mehdi Hosseini with SIG.

**Mehdi Hosseini** (Analysts):
Two follow-ups for me. Greg, I want to go back and see if you can qualitatively give us an update on the demand vectors. I think the targeted model is now stale. And yes, we're going to have to wait till Q4 earnings to get an update. But I think it would be very helpful if you can shed some light into different demand vectors.
It seems like everything is tracking better than expected and next year could be second half weighted. But is there anything else you can provide? Because I just want to make sure that consensus is already well above your target, and we're not being too aggressive. And I have a follow-up.

**Gregory Smith** (Executives):
Yes. No. So I think we can definitely -- we're going to give you an updated model in January. And the last model was based around a $13 billion ATE TAM, $12 billion to $14 billion. And the TAM has grown very, very quickly. And when we were building that model, we were trying to give you an idea of what a larger Teradyne would look like without tying down sort of exactly when that would happen because of uncertainty about these growth rates.
Having said that, there are multiple independent parts of Teradyne that are each growing associated with their markets and our success there. And we had to make assumptions in terms of the mix that in our model, we assumed that Semiconductor Test would be 80% of the revenue and Robotics would be 10% and Product Test would be 10%. Semiconductors are growing so fast that, that mix has changed.
Also, the semiconductor TAM growth has been so concentrated in compute, an area where we have low but growing share that essentially, we need more ATE TAM in order to hit the revenue that we had in the model that we published. So as we're looking to put together the model that we'll talk about in January, we're definitely sort of retiming all of the different groups of the company.
But if you sort of run through it, compute is growing faster than we anticipated, and we're gaining share there at a modest rate because that's being driven by dual vendor strategies primarily from those customers and growth in networking. I would say that mobile is underperforming our expectations from the model as we've put it together, and we're going to be relooking at that to see whether and when we would see an edge AI-driven recovery in that space.
The automotive and industrial space, we're seeing good growth there. And I think that's tracking to sort of the model that we had before. And both Product Test and Robotics are tracking the growth that we had expected in our model, but they've been sort of -- the semiconductor growth has sort of outpaced it. So when we put it all together, I would expect to see us building an evergreen model against a much larger ATE TAM, and we'll talk about that in January. But the vector -- growth vectors are all there, and it's all positive in terms of the direction that we're going.

**Mehdi Hosseini** (Analysts):
And a follow-up, your industrial automation for me is basically physical AI and its build there. And you have also built out manufacturing capacity in the U.S. What needs to happen for a higher growth rate? Is it just a matter of timing? Or do you have to make more modifications to the model? And anything there that could help you with a higher growth rate?

**Gregory Smith** (Executives):
Yes. So -- it's a great question. So with the growth of physical AI, the capabilities of physical AI, we think that, that is going to unlock significant growth in the Robotics group. There are a couple of things that have to happen. Over this year, and Michelle talked a little bit about it in her script, we have been building partnerships with the labs that are working on physical AI models and physical AI implementations.
We are also aligning with the CMs and ODMs that are serving primarily the AI data center build-out. They're doing server builds basically. These things are really tough to build and the customers are quite sophisticated in terms of the adoption of technology. That is kind of fertile ground to be able to deploy robots.
The thing that I will warn you is that because we are working with the labs and then the labs are working to solve the problems with the end customers, it's going to have a gestation period. So I would expect us to see robust growth in terms of the transactions that we have to the labs in '27 and the beginning of end market growth. But I think it's probably more of a 2028 thing than a 2027 thing beyond our sort of major customer in Robotics.

**Operator** (Operator):
We'll move on now to Jim Schneider with Goldman Sachs.

**James Schneider** (Analysts):
I was wondering if you could maybe comment on your sort of near-term visibility heading in the next several months. And specifically, I think you've talked about visibility kind of extending beyond the current quarter. So I was wondering if you can maybe in terms of the longer-dated commentary, help us a little bit, at least directionally with your view on Q1 preliminarily directionally sort of up, flat or down? And maybe what would sort of be driving that beyond the memory drivers you talked about earlier?

**Michelle Turner** (Executives):
Jim, it's Michelle. So from a visibility perspective, we talked about this over the last couple of quarters. So coming into the year, historically, we've had about 13 weeks of visibility. Fast forward to where we are today, we have pretty good line of sight out a couple of quarters. So where we're sitting as we exit '26 is really strong backlog.
So we have pretty good line of sight to what will play out in Q1. The caution we have around putting any guidance around it right now is we do continue to see movement within any given quarter depending on how test cells are coming together for our customers. So I would say we would expect Q1 from where we sit today to be some level of growth, but we expect the year to progressively grow throughout quarter-on-quarter versus what we saw this year, which was more of a 50-50 split.

**James Schneider** (Analysts):
That's very helpful color. And then maybe as a follow-up, I was just wondering if you could sort of give us a view on the Robotics business very broadly speaking. Obviously, the momentum there is improving. And I know that you have some level of visibility on some very large customers potentially ramping next year. So maybe can you give us any update on like sort of how your visibility in Robotics compares to the broader visibility in the business you just discussed?

**Gregory Smith** (Executives):
Yes. So visibility in Robotics aside from our largest customer is pretty short term. I mean we have -- coming into a quarter, a large portion of our revenue is coming from turns. So we manage that business against sort of a pipeline of opportunities. I'll tell you that the pipeline of opportunities is expanding and our closure rates are relatively consistent, but it is essentially probabilistic.
We're -- in the Semiconductor Test space, we're kind of counting noses. We know how many testers people will need, when they'll need them. In terms of the Robotics business, a big chunk of it is essentially driven by an opportunity pipeline. Our large customer, we tripled our revenue for that large customer from 2025 to 2026. We expect to see robust growth next year.
The way that -- what's going on with that major customer is that in 2025, they were largely doing engineering work to prove out the solution they were deploying. In 2026, they deployed that solution to their sort of leading edge of distribution centers and have been working out the kinks and getting it ready and also like sort of developing the processes so that they could install these systems quickly so that they can quickly flip over a distribution center from manual to automated in these workflows. 
And that's the work that we expect to see happening in 2027, sort of a more broad deployment of these technologies, but we'll have to see exactly what pace they're going to be able to do that work.

**Michelle Turner** (Executives):
Yes. And just to follow up on that, Jim, this is an example of where we see more of the back half weighting based on that customer schedule.

**Operator** (Operator):
We'll move on now to Joseph Cardoso with JPMorgan.

**Joseph Cardoso** (Analysts):
Maybe just for the first one, I just wanted to touch on in your prepared remarks, I think you've made a couple of references around CPO and NPO. And so I was just curious if we can get an update on how you're thinking about the timing. 
It sounds like maybe anecdotally, there's a little bit of a deemphasis there in terms of how fast these opportunities could ramp relative to maybe what we're hearing across various suppliers in the broader supply chain there. And just curious whether you're thinking about that any differently as well as the content and TAM associated with the opportunity. And then I do have a quick follow-up.

**Gregory Smith** (Executives):
Hi, Joe. So I think we remain quite enthusiastic about CPO. And when we've talked about it before, we've tried to be pretty clear that we're kind of in the preseason right now, that there is an initial customer that is driving towards a significant ramp in 2027, but it is growing from a very small base. We've talked about the TAM in 2026, probably somewhere in the neighborhood of $100 million for the test equipment portion, and that could grow to $300 million to $700 million by 2028. I think that's still the right range.
As to whether we trend towards the high end or the low end of CPO, I think it really depends on how -- like whether the economics of CPO get to the point where it's practical to ramp it hard. Right now, the test times and the test intensity required to do CPO is quite high. And I think that, that is going to be somewhat of a limiter in terms of how broadly it's deployed until those -- it's part -- and test is only part of it. There are other challenges in the whole assembly flow that need to get worked out and refined.
So I think as those things get refined, this is going to turn into something big. That the $300 million to $700 million is just sort of a stop along a path of growth. This is likely to continue to be up to $1 billion market or beyond. But the exact timing, how fast we go up that ramp is something that I think is going to be a question mark.
The thing that you have to remember is these network connections have to get made. Whether they get made with CPO or NPO or pluggables or copper, the key thing is that clusters are going to get bigger and connectivity is going to be increasing. And so our strategy is to make sure that we are able to serve all of those markets and be able to serve that from both our Product Test Group for pluggables and copper and from our Semi Test market for all of the switch silicon and everything else.
So we're definitely investing towards an open ecosystem in CPO, but I think we are trying to make sure that our business strategy is resilient to any uncertainty in the timing. That's not like a lack of confidence in the end goal, it's more just knowing that the importance of these connections is so high that they're going to have multiple paths to success.

**Joseph Cardoso** (Analysts):
Got it. Appreciate the thoughts there and totally fair. And maybe on the second question, and I wanted to go back to compute, but maybe touch on it in a different angle. Obviously, you have your kind of disclosed customers that you'll be ramping through 2027. But maybe if we think about more medium term, longer term, I just want to hear your thoughts around potential engagements beyond those 3 customers, particularly just given that we're hearing more around maybe a bigger step-up or inflection around custom ASIC opportunities going into 2028 with additional hyperscalers and potentially AI labs.
So just curious how you're thinking about your opportunity or the TAM there as you guys are thinking or maybe hearing about these engagements or discussions with customers? And are you seeing maybe a similar trend as we kind of think about 2028 as well? I know I'm skipping '27 a little bit here, but it does seem like this is a big talking point around, maybe an expanding opportunity set here. So just curious how you guys are thinking about that?

**Gregory Smith** (Executives):
I think it's awesome that you're thinking about 2028, and it really reflects sort of the new reality of this market that we used to be in a world where we were like there was significant uncertainty quarter-to-quarter around how the end market would develop. Now any quarter-to-quarter uncertainty is really just around like shipment timing and how fast people can build buildings. So it's pretty cool that we have the ability to look out to 2028 and have a conversation about long-term targets.
So in our prepared remarks, I talked about hyperscaler 1 is mature. Hyperscaler 2, we're in fast follower. We expect to see stuff in the back half of '27. We're in qualification for a third. There are other X factors here in terms of what will happen with the Terafab investment, what will happen with OpenAI, with Anthropic. All of these folks are leaning hard into the -- into developing their own silicon technology for sort of a complete stack.
I will say that we are approaching all of them in the same way. In some cases, we are the first in supplier and working to maintain and maximize our share. In other cases, we are positioning ourselves as a capable dual vendor option for them that will allow them to secure their supply chain. It's essentially the same -- the same engagement process that we've used for the first 3 hyperscalers is going to be what we use on subsequent ones. And we think that the same things that are driving those early hyperscalers towards the choices they've made are going to be driving the rest of the market.
So I think it's logical to be thinking about what's going to happen in the future. I will say that our competitor has established a very powerful share position in compute. We are making significant progress in terms of share gain inside of compute in 2026. But the size of the compute market has grown so much that, that has essentially had a dilutive effect on overall share. So I'm very optimistic about what will happen with hyperscaler programs, but it is definitely something that takes time. So 2027 is going to be a good year for these programs. 2028 is going to be even better.

**Operator** (Operator):
We'll move on now to Vivek Arya with Bank of America Securities.

**Vivek Arya** (Analysts):
I had a near and then more of an intermediate-term question. So on the near term, Michelle, you mentioned that you expect sales to consistently grow over the next several quarters. If I go back to the Q1 -- the Q4 to Q1 transition in '22, '23, '24, '25, I think Q1 sales were down double digit. But in Q1 '26, they were up because I imagine compute started to become more important than mobility. So I appreciate it's a lumpy business, but I just wanted to make sure we keep everything in mind or anything in mind that could cause Q1 to be below Q4 levels?

**Michelle Turner** (Executives):
Let me clarify. So you're asking about Q4 to Q1. I was referencing sales growing throughout 2027. So we expect the quarters next year to represent growth quarter-on-quarter when you look at next year. And I also expect between Q4 and Q1 that we're also going to have growth. So just to clarify kind of and set the baseline in terms of the numbers that you quoted.
The other thing I would point out is coming into this year, when we set the 60-40 split, the visibility we had was really at 13 weeks. As the year has progressed, we have gained additional visibility that's helping better inform how we position for Q1 and as we think about next year. 
To your point, though, we do continue to see lumpiness quarter-on-quarter. And so I think that's the caution that you're hearing. We feel really strongly in terms of the demand signals, and we feel strongly that next year is going to be another year of healthy growth. But there could be variability within quarter. But where we sit today, we expect each quarter next year to grow in comparative to '26.

**Gregory Smith** (Executives):
And just like the thing I want to add is, I think we talked about this probably 2 calls ago, maybe 3 calls ago that the patterns that we saw up through 2024 are over like that. So I know it's a useful analytic technique to sort of look at historical patterns. There has been a seismic shift in the Semiconductor Test market that started in 2024 and really took hold in 2025.
So prior to that, the mobile -- sort of the mobile consumer cycle was the tick-tock of the industry. But after that, it's all around data center buildup schedules and capacity coming online in semiconductor manufacturers that are vastly underserving a market demand. So like I just -- I think it's an important thing for us to try to figure out how to give you good directional guidance about what's going on. But part of that is to like be very careful about applying patterns that existed prior to '24 to a market that's twice as big and acting very differently.

**Michelle Turner** (Executives):
Yes. And I think the other thing I caught that is it really is driven by compute order timing, right? That's what drove this year. We expect that, that's going to play out next year as well.

**Vivek Arya** (Analysts):
Very helpful. And on my follow-up, Greg, one for you. You made this very interesting point that memory constraints are pushing some accelerators towards lower HBM stack heights. I'm curious to know, is this something that you think might happen? Is it already happening? Will it become prevalent? And I think you also mentioned that your share might be higher when the wafer heights are shorter. So I was just -- would appreciate your perspective on what is the sensitivity here? And for the same amount of HBM bit, how much more test insertion or test time and intensity and opportunity does that create for you?

**Gregory Smith** (Executives):
So I'm afraid I can't give you hard numbers, but I can give you some directional guidance here. So I think it is pretty locked in that next-generation -- like there was a trend towards higher stack heights, like from '24 to '25 into '26, there was this progression that stack heights are going to go 4, 6, 8 up to 12, 16-high. And I feel like that has reversed in 2026. And I would expect to see lower stack heights across a number of different devices.
Now how is that good for us? The way to think about it is that there is -- the bottleneck is the total number of DRAM wafers that can be produced. Those DRAM wafers, if you think about it, you can build twice as many 4-high stacks as you can 8-high stacks out of the same supply of DRAM wafers. So that essentially helps deconstrain the shipments of AI accelerators that are using those HBM memories.
The other thing is that with a higher stack height, you are essentially trying to go through a -- like you're trying to get more data through a narrower pipe. So you have some data rate advantages from having more DRAM stacks versus higher stacks.
The thing that makes it an advantage to us is that our market share in DRAM wafer sort is lower than our market share in HBM performance test. So if the same number of wafers are going into more stacks, that means more stacks need to get tested, which is where we sell more testers. So I think it is a positive indicator for what our share will do going forward, but I don't have a hard number for you.

**Operator** (Operator):
We'll move on now to Krish Sankar with TD Cowen.

**Sreekrishnan Sankarnarayanan** (Analysts):
[Technical Difficulty] de-speccing argument. There's some chatter that there might be some lowering of the HBM signal or pin speed. Would that have any impact on test complexity? And along the same path, I'm curious about HBM competition, not from the Japanese competitors, but more from the Korean players like UniTest, et cetera, how is that shaping up? And then I had a follow-up.

**Gregory Smith** (Executives):
So Krish, I heard part of your question. So if I get it wrong, please feel free to clarify. I think the first part of your question was around HBM de-speccing. And honestly, like while we've heard a lot about lower stack heights, I can't say that we have heard a lot from our customers around de-speccing or how de-speccing could affect tests. So, so far, that is not a factor in the way we're looking at it.
Now in terms of share versus Korean suppliers, Korean suppliers in test for memory are primarily serving the wafer sort part of the business, not the performance test part of the business. And so we tend to have less of an impact. Given the expansion in capacity that's going on right now, I would expect that they're going to see healthy growth, that they're going to get a fair amount of business as the number of DRAM and flash wafers increase.

**Sreekrishnan Sankarnarayanan** (Analysts):
Got it. And then a quick follow-up for Michelle. Thanks for touching up on the capacity and your inventory position. I'm just wondering how much of the inventory build-out is actually for true demand versus actually building inventory of components that will be constrained, for example, I think your testers use DDR4 chips and things like that. So I'm just wondering how much of that is inventory build to prevent any constraints down the road versus true demand?

**Michelle Turner** (Executives):
Yes. I'd say it's about 50-50. The other thing I would point you to like -- and I think this is important to go back and look at is when you look at our inventory from a DIO perspective, we had actually reached unusually low levels in Q1. So part of this was we were building really fast, really quickly to meet the demand and the surge that's occurred over the last 6 to 9 months.
And so part of this is also a normalization. And I would argue the 189 that we're at, I still think that we should probably be around 200 when you think of kind of normal levels in comparative to some of our peers. And so I think there's an element of that, that has to be factored in as well and not just extrapolating on the 35% growth within the quarter.

**Operator** (Operator):
At this time, we've reached our allotted time for Q&A. I'd be happy to return the call to our host for any closing comments.

**Gregory Smith** (Executives):
Thank you, operator. It was another great quarter for us. We're looking forward to Q4 and especially looking forward to updating you all on an updated model in our next earnings call. We'll talk to you then.

**Operator** (Operator):
This concludes today's Teradyne Third Quarter 2026 Earnings Call and Webcast. You may disconnect your line at this time, and have a wonderful day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TER_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜Michelle Turner｜guidance：Q3 營收 12～13 億美元、非 GAAP EPS 1.85～2.15（營收數字在原文同句後半）（原話："$1.2 billion to $1.3 billion and non-GAAP EPS of $1.85"）
- 2026-07-29｜Michelle Turner｜guidance：上半年營收占全年比重更新為 50%～52%（原話："we are updating our first half weighted revenue to 50% to"）
- 2026-07-29｜Michelle Turner｜guidance：下半年展望轉強、區間較三個月前收窄（原話："The outlook for the second half has strengthened"）
- 2026-07-29｜Michelle Turner｜guidance：下半年對比上半年的分部成長與抵銷項目（原話："We expect this growth will be offset by softness"）
- 2026-07-29｜Michelle Turner｜guidance：預期 2027 年成長回升，來源為 ATE TAM 擴張與市占提升（原話："We anticipate a resurgence in growth in 2027"）
- 2026-07-29｜Gregory Smith｜guidance：CEO 預期 2027 為健康成長年（原話："We expect 2027 to be another year of healthy growth"）
- 2026-07-29｜Michelle Turner｜margin：Q3 毛利率指引 58%～59%，歸因產品組合與新產品（原話："Gross margins are expected to be in the"）
- 2026-07-29｜Michelle Turner｜margin：Q2 毛利率 59.8%，年增 250bp，季減 110bp（部分因 Q1 一次性利益）（原話："Gross margins for the quarter were 59.8%"）
- 2026-07-29｜Michelle Turner｜margin：Q3 營業費用占營收約 29%～30%（原話："approximately 29% to 30% of third quarter sales"）
- 2026-07-29｜Michelle Turner｜margin：Q3 非 GAAP 營業利益率指引 28%～30%（原話："operating profit rate is expected to be between 28% and 30%"）
- 2026-07-29｜Michelle Turner｜margin：Q2 非 GAAP 營業利益 4.48 億美元，營業利益率 33.7%（原話："non-GAAP operating income was $448 million,"）
- 2026-07-29｜Michelle Turner｜margin：CFO 說明毛利率季間波動幅度與全年區間的口徑（原話："you'll see about 400 basis point swing"）
- 2026-07-29｜Michelle Turner｜margin：CFO 稱上半年有不會重複的非營運有利因素（原話："some nonrecurring nonoperational"）
- 2026-07-29｜Michelle Turner｜margin：全年毛利率約 59%，略低於目標模型（原話："which is just shy of our target"）
- 2026-07-29｜Michelle Turner｜margin：CFO 稱記憶體產品對毛利率持續構成壓力，並延續至 2027（原話："memory is going to continue to be a strain from an overall"）
- 2026-07-29｜Michelle Turner｜margin：回答分析師：2027 毛利率不預期根本性變化，取決於產品組合（原話："any fundamental changes in gross margin."）
- 2026-07-29｜Michelle Turner｜margin：Q4 營業費用預期與 Q3 指引相當（原話："OpEx in Q4 to be comparable to Q3 guidance"）
- 2026-07-29｜Michelle Turner｜commitment：管理層表示有信心以更快速度達成目標獲利模型，並將於 Q4 法說更新（原話："We remain confident in achieving our target earnings model"）
- 2026-07-29｜Gregory Smith｜commitment：CEO 表示將在 Q4 法說分享更新後的目標獲利模型，更新方式與 WFE 連動（原話："which we will share in our Q4 earnings call"）
- 2026-07-29｜Gregory Smith｜commitment：CEO 稱正加碼投資，有機與併購皆在內（原話："We are leaning further into investments"）
- 2026-07-29｜Michelle Turner｜commitment：美國製造中心預計今年稍後啟用（原話："is on track for opening"）
- 2026-07-29｜Michelle Turner｜capital_allocation：資本配置首要為再投資於業務（原話："Our first priority for capital continues to be reinvesting"）
- 2026-07-29｜Michelle Turner｜capital_allocation：其次為維持營運現金並保留可做增值併購的火力（原話："keep dry powder available for accretive M&A"）
- 2026-07-29｜Michelle Turner｜capital_allocation：Q2 現金與投資 5.17 億美元，自由現金流 3.78 億美元（原話："We had free cash flow of $378 million in"）
- 2026-07-29｜Michelle Turner｜capital_allocation：Q2 股利 2,000 萬美元、買回 6,900 萬美元（原話："We paid $20 million in dividends in the"）
- 2026-07-29｜Michelle Turner｜capital_allocation：營運資金主要為存貨增加，資本支出較上季增加 2,600 萬美元（原話："predominantly inventory investment, increased in support"）
- 2026-07-29｜Gregory Smith｜customer：Q2 營收破 13 億美元，年增逾 100%；AI 營收占比逾 60%（原話："At more than 60%, AI-driven revenue is the key proof point"）
- 2026-07-29｜Michelle Turner｜customer：Semi Test 拆解：SOC 8.43 億、記憶體 2.12 億、IST 6,700 萬美元（原話："SOC of $843"）
- 2026-07-29｜Michelle Turner｜customer：運算占 SOC 產品營收 70%，年增近 600%（原話："compute remains the largest portion of our SOC product"）
- 2026-07-29｜Michelle Turner｜customer：運算訂單時點被記憶體與 IST 成長抵銷（原話："compute order timing was more"）
- 2026-07-29｜Michelle Turner｜customer：記憶體廠規劃更遠期擴產；Q2 記憶體 book-to-bill 超過 2（原話："planning capacity additions further out in time"）
- 2026-07-29｜Michelle Turner｜customer：手機相關 SOC 季增雙位數但仍低於歷史水準（原話："though it remains below historical"）
- 2026-07-29｜Michelle Turner｜customer：Product Test 營收 1.07 億，年增 26%、季增 33%；Robotics 1 億，年增 33%（原話："Revenue was $107 million, up 26% year-over-year"）
- 2026-07-29｜Gregory Smith｜customer：IST 營收季增 2.5 倍，來自 AI 帶動的 HDD（原話："Our IST business grew revenue 2.5x quarter-over-quarter"）
- 2026-07-29｜Gregory Smith｜customer：運算客戶下一波高峰預期在 2027 上半年（原話："The next surge for these customers is expected"）
- 2026-07-29｜Gregory Smith｜competition：第一筆 merchant GPU 客戶訂單 Q1 收到、Q2 出貨（原話："we received our first order from -- for a merchant GPU"）
- 2026-07-29｜Gregory Smith｜competition：管理層描述雙供應商資格認證流程，從啟動到量產 9～12 個月（原話："it takes 9 to 12 months from the start to the ramp"）
- 2026-07-29｜Gregory Smith｜competition：fast follower 階段市占預期由 0 增至約 30%（原話："market share to grow incrementally from 0 up to about 30%"）
- 2026-07-29｜Gregory Smith｜competition：三個運算客戶所處階段：成熟雙供應商 1、fast follower 1、量產前資格認證 1（原話："we have 1 compute customer in the mature dual vendor phase"）
- 2026-07-29｜Gregory Smith｜competition：CEO 同意競爭對手 Advantest 對記憶體市占下滑的說法，並預期 SOC 市占約持平、略增（原話："I have to say I agree with their commentary about memory."）
- 2026-07-29｜Gregory Smith｜competition：運算市占今年趨穩並開始上揚，市占變化 2027 起逐步顯現（原話："stabilizing and starting to inflect upward"）
- 2026-07-29｜Gregory Smith｜competition：伺服器 CPU 轉向 ARM 對 Teradyne 市占有利，同時也在 x86 爭取（原話："as the share mix of server CPU shifts towards ARM"）
- 2026-07-29｜Gregory Smith｜competition：客戶擅長逐階段挑選最佳方案，Teradyne 須逐項競爭（原話："we have to really compete for everything that we're getting"）
- 2026-07-29｜Gregory Smith｜competition：中國功率市場有在地競爭者，Teradyne 的中國功率占比與前高相近（原話："There is some local competition"）
- 2026-07-29｜Gregory Smith｜product：測試設備占半導體資本支出比重由 2023 年約 4% 升至 2026 前 5 個月 8%（原話："it's 8% of total semi CapEx has been on test equipment"）
- 2026-07-29｜Gregory Smith｜product：CEO 預期該比重落在 7%～9%，不會再持續上升（原話："it's going to settle somewhere in the 7% to 9% range"）
- 2026-07-29｜Gregory Smith｜product：WFE 增加代表需測電晶體與位元增加；管理層看到 ATE TAM 路徑達 200 億美元以上（原話："reach or exceed $20 billion"）
- 2026-07-29｜Gregory Smith｜product：2026 記憶體 TAM 預期較 2025 大逾 40%（原話："The 2026 memory TAM is likely to be more than 40% larger"）
- 2026-07-29｜Gregory Smith｜product：DDR 市場比 1 月預期更強；NAND 開始出現客戶拉貨（原話："the DDR market is stronger now than we thought it would be"）
- 2026-07-29｜Gregory Smith｜product：不預期 2027 記憶體出現特別的波動（原話："we are looking at particular lumpiness in memory"）
- 2026-07-29｜Gregory Smith｜product：預期 2028 年 CPO 市場規模 3 億～7 億美元（原話："We expect CPO alone will be a $300"）
- 2026-07-29｜Gregory Smith｜product：2027 年 CPO 偏向低端，約 2 億美元（原話："the low end would be in the $200 million range"）
- 2026-07-29｜Michelle Turner｜product：Omnyx 初期客戶動能強，管理層預期下半年持續成長（原話："continued growth expected in the second half"）
- 2026-07-29｜Gregory Smith｜product：預期 2027 年汽車與工業可能達到或超越前高（CEO 自稱憑直覺、尚未完整分析）（原話："'27 is going to be up to or exceeding prior peaks"）
- 2026-07-29｜Gregory Smith｜risk：CEO 稱 WFE 與 ATE 的關聯在單季層級不相關，且有約一年時間落差（原話："it's not at all correlated when you're down to a quarter"）
- 2026-07-29｜Gregory Smith｜risk：2027 年測試設備占半導體資本支出比重可能回落至約 7%（原話："It's possible that next year, that could revert down to 7%"）
- 2026-07-29｜Gregory Smith｜risk：良率或品質問題可能造成 ATE 超買，測試時間縮短也可能影響需求（原話："there's significant over buying in ATE"）
- 2026-07-29｜Michelle Turner｜risk：指引區間納入訂單時點可能使營收在季度或年度間位移（原話："timing of orders that could impact revenue"）
- 2026-07-29｜Gregory Smith｜risk：CEO 指出供應鏈中斷是此領域所有人關心的事項，並驅動雙供應商策略（原話："as strong as the weakest link in our whole supply chain"）

### 問答異常語氣（迴避／改口／保留）
- TER_Q2_2026_Earnings_Call_20260729.md｜問：Morgan Stanley 的 Shane Brett 追問記憶體測試成長 vs 位元成長（投影片第 6 頁）及記憶體測試成長 2 倍位元成長如何解讀｜答法：CEO 先說要離線再談，表示分析師過度解讀圖表、並非要預測記憶體 ATE TAM，之後才給一般性原則說明，未直接回答數字
- TER_Q2_2026_Earnings_Call_20260729.md｜問：UBS 的 Timothy Arcuri 追問長期市占目標（40%？42%？）及新認證何時反映市占｜答法：CEO 未給長期市占目標數字，僅稱 2027 起逐步顯現、逐 socket 進行
- TER_Q2_2026_Earnings_Call_20260729.md｜問：Bank of America 的 Vivek Arya 追問 2027 年 WFE 成長 30% 時 Teradyne 相對成長快慢的情境｜答法：CEO 未給 2027 成長率對照，僅稱 TAM 預期增加、測試占資本支出比重可能回落至 7% 但仍在釐清

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
{"date":"20260626","verdict":"觀望","role":"條件式衛星持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 測試強度結構提升 → SoC compute（custom ASIC + merchant GPU）持續為 SoC 測試主引擎","columns":{"2Y 驗證點":"FY27 SoC compute 維持 ≥ 50% of SoC 營收 + AI 佔總營收 ≥ 70%","5Y 驗證點":"FY30 ATE 市場達 mgmt 目標 $12-14B（vs $9B 2025）；TER 營收 ~$6B","10Y 驗證點":"FY36 AI/HPC 測試成為 SoC 測試主流（vs mobile）","Sourced Floor / 漂移觸發":"Floor：Q1'26 compute ~half of SoC、FY25 compute +90%（CEO Greg Smith 法說公開）。漂移：連 2 季 SoC compute 訂單環比下滑 = 循環鬆動"}},{"id":"H2","text":"突破 Advantest 在 merchant GPU 的主場：從 design-in → 量產（custom ASIC 已 ~50% 份額是既有強項，merchant GPU 才是新增量）","columns":{"2Y 驗證點":"FY27 merchant GPU 量產營收上量 + Rubin 認證落地","5Y 驗證點":"FY30 merchant GPU + custom ASIC 雙引擎","10Y 驗證點":"FY36 互連（MultiLane）/ 先進封裝（TEL）/ 矽光子 CPO（Photon 100）測試成獨立成長軸","Sourced Floor / 漂移觸發":"Floor：FY26 merchant GPU 指引僅 ~$50M（初期）、H1'26 認證、H2'26 初步營收；NVIDIA Blackwell 最終測試仍由 Advantest 近乎 sole-source，TER 為第二供應商候選（Rubin 預期最高 ~40% 份額，未落地）。漂移：H2'26 量產未實現或 Rubin 認證落空 = H2 thesis 受傷"}},{"id":"H3","text":"市場願維持 forward PE 在 28-40x（AI 測試溢價）而非回落至循環中樞 20-25x","columns":{"2Y 驗證點":"FY27 FPE 維持 ≥ 28x（不單季崩至 18-20x）","5Y 驗證點":"循環反轉後 normalized EPS $9-11、PE 擴張至 25-30x（mid-cycle）","10Y 驗證點":"長期合理 PE 趨向 22-28x","Sourced Floor / 漂移觸發":"Floor：5Y forward 中位 ~28-30x（macrotrends/finbox）。漂移：連續 4w FPE 50x（cycle peak 透支警戒，現值 49x 已逼近上緣）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Advantest 守住 merchant GPU 主場（Blackwell sole-source，Rubin 不讓 TER 進）+ 中國 ATE（長川/華峰）高端化蠶食","columns":{"對應假設":"H1, H2","時間尺度":"🔥 中（4-6 季）","監測指標":"Rubin 測試供應商選擇、Advantest 季度 GPU 份額、中國廠高端機台發佈","警戒閾值":"Rubin 認證 TER 出局 或 連 2 季 TER custom-ASIC 份額流失 5pp"}},{"id":"R2","text":"cycle peak 後 AI capex digestion → EPS/Rev 環比下滑（peak-EPS 回落）","columns":{"對應假設":"H1, H3","時間尺度":"⚡ 短（1-2 季）","監測指標":"季度營收/EPS 環比、book-to-bill、AI 佔比","警戒閾值":"連 2 季營收環比下滑（Q2'26 guide 已環比 -6%，需觀察 Q3 是否續弱）"}},{"id":"R3","text":"估值正常化（PE de-rating）：市場不再給 AI 測試溢價","columns":{"對應假設":"H3","時間尺度":"⚡ 短（1-2 季）","監測指標":"forward PE 分位、現價 vs 分析師均值","警戒閾值":"連續 4w FPE 15%（Q1'26 已現 -17% gap down）"}},{"id":"R4","text":"出口管制再收緊（中國 ~14% 營收）；Robotics 段（UR+MiR）持續低貢獻","columns":{"對應假設":"H1, —","時間尺度":"🐢 長（2+ 年）","監測指標":"美國 BIS 規則、UR+MiR 季度營收與 OM","警戒閾值":"新增測試機出口禁令；robotics 連 4 季虧損擴大"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":-3.0,"ev5y_pct":-13.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"條件式衛星持倉","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":null,"ev5y_pct":-13.0,"irr_base_pct":-3.0,"max_dd_pct":-60.0,"bull_5y_price":665.46,"bear_5y_price":169.91,"p_bull_pct":30.0,"p_bear_pct":30.0,"rearm_trigger":null,"price_at_dd":471.96,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TER_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
