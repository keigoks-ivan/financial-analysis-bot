你是 stock-analyst **v20 判斷 agent**，標的 TSLA（20261024）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TSLA","date":"2026-10-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSLA_20261024/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSLA_20261024/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":28046,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"}},{"id":"f_kpi1_gaap","label":"GAAP 營業利益","value":718,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益率","value":2.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"}},{"id":"f_kpi3_ebitda","label":"調整後 EBITDA","value":3900,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"}},{"id":"f_kpi6_gaap","label":"汽車毛利率（GAAP）","value":18.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"}},{"id":"f_kpi7","label":"交車量","value":486532,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"輛","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"}},{"id":"f_kpi8","label":"儲能部署量","value":13.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"GWh","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"}},{"id":"f_kpi9","label":"管理層指引","value":"無量化指引","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-21","period":"2026-10-21","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-21"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_tsla_gross_margin_pct","label":"TSLA 毛利率","value":18.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSLA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tsla_operating_margin_pct","label":"TSLA 營業利益率","value":4.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSLA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tsla_fcf_margin_pct","label":"TSLA FCF 利潤率","value":5.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSLA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_gm_gross_margin_pct","label":"GM 毛利率","value":5.74,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gm_operating_margin_pct","label":"GM 營業利益率","value":0.98,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gm_fcf_margin_pct","label":"GM FCF 利潤率","value":0.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_f_gross_margin_pct","label":"F 毛利率","value":2.22,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.F.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_f_operating_margin_pct","label":"F 營業利益率","value":-3.74,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.F.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_f_fcf_margin_pct","label":"F FCF 利潤率","value":3.87,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.F.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_1211_hk_gross_margin_pct","label":"1211.HK 毛利率","value":17.76,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.1211.HK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_1211_hk_operating_margin_pct","label":"1211.HK 營業利益率","value":5.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.1211.HK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_1211_hk_fcf_margin_pct","label":"1211.HK FCF 利潤率","value":-6.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.1211.HK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rivn_gross_margin_pct","label":"RIVN 毛利率","value":7.51,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RIVN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rivn_operating_margin_pct","label":"RIVN 營業利益率","value":-60.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RIVN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rivn_fcf_margin_pct","label":"RIVN FCF 利潤率","value":-59.31,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RIVN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_gaap","label":"自由現金流（非GAAP）","value":1531,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"}},{"id":"f_kpi5_sbc","label":"SBC","value":1165,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":372.22,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-1.08,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_rsi14","label":"RSI(14)","value":51.52,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.77 → 1.77）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-1.37,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.19 → 2.16）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-2.42,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.3 → 3.22）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.77,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.16,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.22,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-0.56,"period":"2026-07-30 → 2026-10-24","unit":"%","basis":"FY1 共識 EPS 1.78 → 1.77（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":210.29,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 1.77，分子＝快照價 372.22","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 372.22 / W52 396.82 / W104 369.85 / W250 286.55 / W250 13週斜率 0.17%"},{"id":"f_ma_w52","label":"52 週均線","value":396.82,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":369.85,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":286.55,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.17,"period":"2026-10-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 自述：進入電動車與自駕市場的既有與新進車廠數量顯著且持續增加，競爭加劇可能導致銷量下降、降價與市占流失；另稱許多對手資源更多。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm","excerpt":"Increased competition could result in our lower vehicle unit sales, price reductions, revenue shortfalls, loss of customers and loss of market share, which may harm our business, financial condition and operating results.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 自述：Robotaxi 將與傳統叫車、計程車服務及 AI／機器人領域對手競爭。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm","excerpt":"As we seek to become a top provider of autonomous solutions, we also face competition in the fields of AI and robotics. We expect our Robotaxi service to compete in this developing market, along with traditional ride-hailing and taxi services","as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Counterpoint：Tesla 2026Q2 全球 BEV 份額 13%（Q1 11%），BYD 約 12%；美國銷量年減約 20%","source":"Counterpoint Research 全球 EV 份額季報","url":"https://counterpointresearch.com/de/insights/global-electric-vehicle-market-share-quarterly","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261024","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"西歐18國 Tesla 2026Q2 份額 2.6%（去年同期1.7%），中國品牌合計創 10.7% 新高","source":"SCMP：Europe's new EV power struggle","url":"https://www.scmp.com/business/china-evs/article/3362905/europes-new-ev-power-struggle-sees-chinese-giants-seize-record-market-share","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Cox 估計 Tesla 2026Q3 美國EV份額約54%（144,094／262,649），Model Y、Model 3 銷量年減；為第三方估計","source":"EVwire 引 Cox Automotive","url":"https://evwire.com/p/tesla-outsells-all-other-ev-brands-combined-us-q3-2026-cox-automotive","excerpt":"Tesla sold an estimated 144,094 EVs during the quarter, while the rest of the market combined accounted for 118,555 of the 262,649 EVs sold in the country.","as_of":"2026-10-15","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Waymo 為 robotaxi 領先者，Zoox、Uber/Lucid/Nuro 為新進入者","source":"SF Standard：Waymo has robotaxi lead","url":"https://sfstandard.com/2026/01/07/waymo-has-robotaxi-lead-tesla-zoox-uber-coming-streets/","excerpt":"Waymo has the robotaxi lead. Tesla, Zoox, and Uber are coming to the streets San Francisco is going to get more crowded with autonomous vehicles. Here’s what will be on the road in 2026.","as_of":"2026-01-07","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 的集中度附註（應收帳款無單一實體達 10%）待核","source":"Tesla, Inc. Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q3 2026 交付 486,532 輛，優於預期 461,974，年減 2%；多篇歸因高油價（週期性因素）與庫存去化，交付高於產量約 22,000 輛","source":"Electrek, Tesla Q3 2026 deliveries","url":"https://electrek.co/2026/10/02/tesla-q3-2026-deliveries-486532/","excerpt":"(TSLA) Q3 2026 deliveries slip 2% to 486,532, but beat estimates Fred Lambert | Oct 2 2026 - 6:11 am PT 66 Comments Tesla (TSLA) delivered 486,532 vehicles in the third quarter of 2026, down 2.1% from the record 497,099 it delivered in the same quarter last year. That’s still about 25,000 more than Wall Street expected, with the consensus at 461,974 deliveries.","as_of":"2026-10-02","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"分析師共識 2026 約 177 萬輛、2027 約 192 萬、2028 約 210 萬；Munster 預期 2027 成長 15% 對 Street 9%","source":"Stocktwits, Gene Munster Q3 deliveries","url":"https://stocktwits.com/news-articles/markets/equity/tsla-q3-deliveries-beat-estimates-gene-munster-sees-growth/cZDjWFIRBKa","excerpt":null,"as_of":"2026-10-02","retrieved_at":"20261024","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Tesla 表示電池產能仍是全球車輛量產的限制因素；Semi 內華達廠年產能上限 5 萬輛，產線仍在 commissioning","source":"Drive Tesla Canada, Tesla Semi high-volume production","url":"https://driveteslacanada.ca/news/tesla-semi-high-volume-production-2027/","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261024","affects":["thesis.H","triggers"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K FY2025 揭露：公司配合多項政府調查；就公司所知，沒有任何機關在進行中的調查裡認定有不當行為，但無法預測結果，若 SEC、司法部或其他機關日後採取法律行動，可能面臨責任、罰款與限制性制裁。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm","excerpt":"We are cooperating with certain government investigations as discussed in Note 13, Commitments and Contingencies, to the consolidated financial statements included elsewhere in this Annual Report on Form 10-K. To our knowledge, no government agency in any such ongoing investigation has concluded that any wrongdoing occurred.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"中國有一件反壟斷訴訟指控 Tesla 濫用市場支配地位、限制獨立維修商取得維修軟體（民間訴訟，非主管機關行動）","source":"MLex","url":"https://www.mlex.com/mlex/articles/2531117","excerpt":"Tesla faces China dominance-abuse lawsuit over EV repair-software access By MLex Staff ( September 29, 2026, 06:36 GMT | Insight) -- Tesla is facing a Chinese antitrust lawsuit accusing the US electric-vehicle maker of abusing its market dominance by restricting independent repairers’ access to software needed","as_of":"2026-09-29","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"NHTSA 對 Tesla FSD 的調查延長，回覆期限延至 2026-02-23","source":"HeyGoTrade: Tesla FSD Probe: NHTSA Grants 5-Week Breathing Room","url":"https://www.heygotrade.com/en/news/tesla-fsd-probe-nhtsa-grants-5-week-breathing-room/","excerpt":"Gotrade News - Tesla just scored a five-week extension from US regulators regarding its Full Self-Driving (FSD) investigation. This gives the EV giant much-needed breathing room to address ongoing safety concerns. Key Takeaways: NHTSA pushed the FSD response deadline to February 23.","as_of":"2026-01-19","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 稱 2025 年美國關稅調升及報復措施已影響供應鏈成本，並可能影響部分技術或零組件的取得（視關稅範圍與報復性出口管制而定）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm","excerpt":"U.S. trade policy alterations in 2025, including heightened import tariffs and subsequent retaliatory measures, have impacted our supply chain costs, and may impact the availability of certain technologies or components, depending on the exact scope of the tariffs ultimately implemented and retaliatory export controls.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K MD&A 稱現行關稅制度對儲能業務的衝擊相對大於汽車業務；進口關稅可能顯著推高電池電芯成本。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm","excerpt":"The current tariff regime will have a relatively larger impact on our energy generation and storage business compared to our automotive business.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025 年汽車銷售成本下降，部分被關稅增加抵銷。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm","excerpt":"partially offset by lower fixed cost absorption and an increase in tariffs compared to the prior year.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"公司在中國與德國設廠，以降低運輸與製造成本並限制不利關稅的影響。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm","excerpt":"Internationally, we also have manufacturing facilities in China and Germany, which allows us to increase the affordability of our vehicles for customers in local markets by reducing transportation and manufacturing costs and limiting the impact of unfavorable tariffs.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Tesla 要求供應商把顯示器、ECU、PCB 移出中國與台灣生產，供應商稱成本高且困難","source":"InsideEVs: Tesla Wants Its Suppliers To Make Parts Outside Of China And Taiwan Amid Rising Tensions","url":"https://insideevs.com/news/720893/tesla-suppliers-outside-china-taiwan/","excerpt":null,"as_of":"2024-05-01","retrieved_at":"20261024","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Musk 稱中國稀土磁鐵供應中斷延誤 Optimus 關鍵零件，北京要求出口許可","source":"The Register: Tesla's Optimus can't roll without rare earth magnets","url":"https://www.theregister.com/2025/04/23/tesla_optimus_china/","excerpt":"rare earth magnets, and Beijing ain't budging yet Officials seek assurances that bot won't be used for military applications Richard Speed Richard Speed Published wed 23 Apr 2025 // 17:32 UTC Make us preferred on Google Elon Musk says supply chain disruption in China held up delivery of a key component for Tesla's \"Optimus\" robot, with authorities reportedly demanding an export license and","as_of":"2025-04-23","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 總營收約 $28.05B，與去年同期 $28.095B 大致持平；汽車營收約 -3% 至約 $20.6B，法規積分收入降至 $113M（去年 $417M）；服務及其他營收 +33% 至約 $4.6B。","source":"Electrek, Tesla Q3 2026 financial results","url":"https://electrek.co/2026/10/21/tesla-tsla-q3-2026-financial-results/","excerpt":null,"as_of":"2026-10-21","retrieved_at":"20261024","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 能源發電與儲能營收 -16% 至約 $2.9B，儘管部署量 +10% 至 13.7 GWh（低於分析師預期約 15.9 GWh）；公司部分歸因於關稅相關客戶退款。","source":"Electrek, Tesla Q3 2026 financial results","url":"https://electrek.co/2026/10/21/tesla-tsla-q3-2026-financial-results/","excerpt":null,"as_of":"2026-10-21","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 交付 486,532 輛、生產 464,391 輛，優於公司彙整共識 462,000，但低於 2025 Q3 稅收抵免推動的高峰。","source":"autoevolution, Tesla third quarter deliveries surprise Wall Street analysts","url":"https://www.autoevolution.com/news/tesla-third-quarter-deliveries-surprise-wall-street-analysts-as-european-sales-are-booming-276474.html","excerpt":null,"as_of":"2026-10-02","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Cox Automotive 估計 Tesla Q3 2026 美國 EV 銷量約 144,094 輛、市佔約 54.0%（美國 EV 總量 262,649）；Model Y 99,037 輛；年初至今市佔 52.9%。J.D. Power 引 Reuters：聯邦稅收抵免結束後美國 EV 平均成交價升近 $6,000 至 $53,300，EV 零售佔比降 3.6 點至 6.2%。","source":"EVwire, Tesla outsells all other EV brands combined US Q3 2026 (Cox Automotive)","url":"https://evwire.com/p/tesla-outsells-all-other-ev-brands-combined-us-q3-2026-cox-automotive","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 年 Q1 儲能部署 8.8 GWh（-15% YoY），Q2 回升至 13.5 GWh（去年同期 9.6 GWh）；管理層預期 2026 全年部署量高於 2025 的 46.7 GWh；Houston Megafactory 2026 Q3 起投產；未找到官方 2027 部署目標。","source":"Nasdaq/Zacks, Tesla's Growing Energy Business; Tesla 10-Q","url":"https://www.nasdaq.com/articles/teslas-growing-energy-business-how-strong-2026-setup","excerpt":null,"as_of":"2026-10-21","retrieved_at":"20261024","affects":["thesis.H","triggers"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Waymo 以光達＋雷達＋相機路線領先 Tesla 純視覺 robotaxi 部署規模","source":"The Great Robotaxi Race: A Look at Tesla's Competition (notateslaapp)","url":"https://www.notateslaapp.com/news/3775/the-great-robotaxi-race-a-look-at-teslas-competition","excerpt":"Waymo Not a Tesla App Google (Alphabet)’s Waymo is the current market leader in the United States. Waymo is using a sensor-heavy approach to achieve Level 4 autonomy, and is now on its sixth generation of hardware. The current Waymo Driver uses an optimized array of 13 cameras, 4 lidars, and 6 radar units to cut its sensor suite costs by","as_of":"2026-03-18","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Tesla Vision 對光達策略之爭（2026）","source":"elektroquatsch: tesla vision vs lidar strategie 2026","url":"https://www.elektroquatsch.de/artikel/tesla-vision-vs-lidar-strategie-2026","excerpt":"Tesla Vision vs. Waymo: Zwei Weltanschauungen Der Vergleich mit Waymo (Google) zeigt die tiefe Spaltung der Branche. Waymo setzt auf \"Maximale Sicherheit durch Redundanz\" mit 29 Kameras, 5 LiDAR-Scannern und 6 Radarsystemen.","as_of":"2026-02-16","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025：汽車銷售通路為官網與自有門市網路，部分地區設展示廳（不交易）；能源產品另透過通路夥伴與 PPA 銷售。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm","excerpt":"Our vehicle sales channels currently include our website and a global network of company-owned stores. In some jurisdictions, we also have galleries to educate and inform customers about our products, but such locations do not transact in the sale of vehicles.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Tesla 於 2026-02-14 後停止 FSD 一次性買斷，僅剩月訂閱；Q2 2026 財報會議摘要稱 FSD 訂閱 1.48M、年增 56%（次級來源）","source":"notateslaapp Summary of Tesla's 2026 Q2 Earnings Call","url":"https://notateslaapp.com/news/4481/summary-of-teslas-2026-q2-earnings-call-cybercab-fsd-ai4-and-more","excerpt":"Active FSD subscriptions expanded to 1.48 million, reflecting a 56% YoY increase In North America, over 55 percent of new vehicle deliveries included an FSD subscription at purchase","as_of":"2026-07-22","retrieved_at":"20261024","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Tesla 於 2026 Q1 財報後把 2026 年資本支出指引上調至至少 250 億美元（1 月為 200 億），並預期本年其餘時間自由現金流為負；Morningstar 維持 400 美元公允價值。","source":"Morningstar, Tesla Earnings: Shares Fall Slightly as Management Raises Capital Expenditure Guidance","url":"https://www.morningstar.com/stocks/tesla-earnings-shares-fall-slightly-management-raises-capital-expenditure-guidance","excerpt":null,"as_of":"2026-04-23","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 25 位分析師共識評級 Buy（14 Buy／9 Hold／2 Sell），平均目標價 408 美元，區間最高 600；各聚合站平均約 404–420，MarketBeat 為 Hold、MarketScreener 為 Outperform；個股目標價最低 GLJ Sell 25 美元。資料約為 2026 年 9 月初，非最新。","source":"Benzinga TSLA price targets","url":"https://www.benzinga.com/quote/tsla/price-targets","excerpt":null,"as_of":"2026-09-06","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Tesla 公司彙編的分析師共識：2026 全年交付約 165 萬輛（3 月時約 169 萬，再早為 175 萬），共識被下修；Tesla 未提供正式交付量指引。","source":"Electrek, Tesla Q1 2026 delivery consensus; Automotive World","url":"https://electrek.co/2026/03/26/tesla-tsla-q1-2026-delivery-consensus-365000-analyst-estimates/","excerpt":null,"as_of":"2026-03-26","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q1 財報後賣方目標價調整：Mizuho 由 530 升至 540（Outperform），Goldman 由 400 升至 405（Neutral），JPMorgan 維持 Underweight 並提資本支出疑慮。","source":"Newsquawk, Sell-side on Tesla","url":"https://www.newsquawk.com/headlines/sell-side-on-tesla-tsla-shares-gain-amid-earnings-beat-but-attention-on-path-ahead-given-capex-hike","excerpt":null,"as_of":"2026-04-23","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Musk 表示 SpaceX 與 Tesla 已成立特別委員會探索合併，雙方尚未談定條款；截至 2026-10-20 報導無協議。","source":"Bloomberg Law｜Musk Says SpaceX and Tesla Have Begun Exploring a Merger","url":"https://news.bloomberglaw.com/ip-law/musk-says-spacex-tesla-have-formed-committees-to-explore-merger","excerpt":null,"as_of":"2026-10-20","retrieved_at":"20261024","affects":["valuation","thesis.R","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Tesla 於 2026-09-29 簽署 $20B 三年期延遲提款定期貸款、$8B 五年期循環、$2B 364 天循環信貸額度（8-K Item 1.01）。","source":"SEC EDGAR｜8-K 2026-09-29 Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1318605/000162828026063820/tsla-20260929.htm","excerpt":"$20.0 billion senior unsecured three-year delayed draw term loan facility (the “Term Loan Facility”)","as_of":"2026-09-29","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"美國證券集體訴訟（W.D. Texas，Autopilot／FSD／Robotaxi 陳述）：修正訴狀 2026-02-17，Tesla 於 04-20 聲請駁回，最新 10-Q 稱已完成briefing，未見裁決。","source":"Tesla 10-Q（截至 2026-09-30）","url":"https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm","excerpt":null,"as_of":"2026-10-22","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"NHTSA 正評估是否就 robotaxi 學區超速請願開正式調查（期限約 2027-01-21），並另就 Cybercab 無踏板／方向盤的自我認證發出查詢。","source":"The Star｜Tesla faces US probe over claim of robotaxis speeding in school zones","url":"https://www.thestar.com.my/tech/tech-news/2026/10/13/tesla-faces-us-probe-over-claim-ofrobotaxis-speeding-in-school-zones","excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261024","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"經查 SEC 申報清單，近12個月 10 份 8-K 中無 Item 4.02（財報不可信賴／重編）；唯一重大項目為 2026-09-29 的 1.01/1.02/2.03。","source":"SEC EDGAR｜8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001318605&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["triggers"],"status":"ok"},{"id":"major_events#5","axis":"major_events","section":"coverage","direction":"-","claim":"2026 年多起 NHTSA 召回（26V445、26V315、26V255、26V558 等）。","source":"NHTSA recall report 26V445","url":"https://static.nhtsa.gov/odi/rcl/2026/RCLRPT-26V445-3153.pdf","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"SpaceX 與 Tesla 成立特別委員會探索合併，條款未定、無協議（2026-10-20 報導）。","source":"Bloomberg Law","url":"https://news.bloomberglaw.com/ip-law/musk-says-spacex-tesla-have-formed-committees-to-explore-merger","excerpt":null,"as_of":"2026-10-20","retrieved_at":"20261024","affects":["valuation","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"W.D. Texas 證券集體訴訟（Autopilot／FSD／Robotaxi）駁回聲請已briefing完畢，未見裁決；另有 2026-06-04 N.D. Cal. 集體訴訟。","source":"Tesla 10-Q（截至 2026-09-30）","url":"https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm","excerpt":null,"as_of":"2026-10-22","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2018 CEO 績效獎勵訴訟：法院判決應撤銷，原告律師費判 $345 million。","source":"Tesla 10-K FY2025 Note 13","url":"https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm","excerpt":"On January 30, 2024, the Court issued an opinion finding that the 2018 CEO Performance Award should be rescinded.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"NHTSA 評估 robotaxi 學區超速請願是否開調查，並對 Cybercab 認證發出查詢。","source":"The Star","url":"https://www.thestar.com.my/tech/tech-news/2026/10/13/tesla-faces-us-probe-over-claim-ofrobotaxis-speeding-in-school-zones","excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261024","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單無 Item 4.02；搜尋亦未見 2026 SEC 調查或重編報導。","source":"SEC EDGAR｜8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001318605&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"TSLA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":18.85,"operating_margin_pct":4.61,"fcf_margin_pct":5.55,"rd_intensity_pct":7.46},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSLA","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"GM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":5.74,"operating_margin_pct":0.98,"fcf_margin_pct":0.33,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GM","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"F","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":2.22,"operating_margin_pct":-3.74,"fcf_margin_pct":3.87,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.F","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"1211.HK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":17.76,"operating_margin_pct":5.25,"fcf_margin_pct":-6.5,"rd_intensity_pct":6.75},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.1211.HK","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"RIVN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":7.51,"operating_margin_pct":-60.05,"fcf_margin_pct":-59.31,"rd_intensity_pct":30.61},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RIVN","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"TSLA"},"financial_history":{"ticker":"TSLA","currency":null,"method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":81462000000.0,"revenue_yoy_pct":null,"gross_margin_pct":25.6,"operating_margin_pct":16.98,"net_income":12583000000.0,"diluted_eps":3.62,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":96773000000.0,"revenue_yoy_pct":18.8,"gross_margin_pct":18.25,"operating_margin_pct":9.19,"net_income":14999000000.0,"diluted_eps":4.31,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":97690000000.0,"revenue_yoy_pct":0.95,"gross_margin_pct":17.86,"operating_margin_pct":7.94,"net_income":7130000000.0,"diluted_eps":2.04,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":94827000000.0,"revenue_yoy_pct":-2.93,"gross_margin_pct":18.03,"operating_margin_pct":5.11,"net_income":3794000000.0,"diluted_eps":1.08,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TSLA/TSLA_Q3_2026_Earnings_Call_20261021.md）

# Q3 2026 Earnings Call
**Tesla, Inc.** | Earnings Calls | 2026-10-21

**Travis Axelrod** (Executives):
Good afternoon, everyone, and welcome to Tesla's Third Quarter 2026 Q&A Webcast. My name is Travis Axelrod, Head of Investor Relations, and I'm joined today by Elon Musk, Vaibhav Taneja and a number of other executives. Our Q3 results were announced at about 3:00 p.m. Central Time in the update deck we published at the same link as this webcast. 
During this call, we will discuss our business outlook and make forward-looking statements. These comments are based on our predictions and expectations as of today. Actual events or results could differ materially due to a number of risks and uncertainties, including those mentioned in our most recent filings with the SEC. [Operator Instructions] 
Before we jump into Q&A, Elon has some opening remarks. Elon?

**Elon Musk** (Executives):
Thank you. So the third quarter was very strong, and I'd like to give a big congratulations to the whole Tesla team for working hard to make it happen. Demand is growing rapidly for our vehicles. It's exceeding our production by a significant margin. And obviously, we're going to be ramping and we are ramping production meaningfully. The biggest driver for demand is full self-driving. And today, there's really no competitor for FSD in any car that you can buy. And to be clear, we are producing and delivering as many cars as we can, and we're pushing very hard for FSD approval in additional markets. We're now approved in many countries in Europe, and we're hoping for an EU-wide approval. It's hard to predict, but maybe within a few months, but I would be surprised if it takes longer than Q1. But obviously, that's not a time frame we control, but we do anticipate being fully approved in throughout Europe and many other countries.
We also began production of the Tesla Semi truck in Q3 and did the new Roadster demo, which was, I think, one of the most exciting events. I mean, arguably, the coolest demo of any product ever, and that's a testament to amazing work by the Tesla and SpaceX teams. So we've also been like laying the groundwork for a lot more manufacturing capacity. We're, I think, aiming for 5 million vehicles a year by approximately 2030. And that's -- I think we've got a good shot of achieving that goal. And yes, so energy demand is very strong. We're actually almost sold out of all Megapacks for 2027, and we're ramping production as quickly as possible to meet demand. We also expect gross margins on that to increase meaningfully. So in a nutshell, after many years of sort of grind and things being fairly flat, I think we're now headed for a lot of fun and significant growth. 
Regarding Robotaxi, we're seeing the Robotaxi miles driven -- fully autonomous miles driven scale exponentially, meaning scaling very rapidly. And it would be hard to overstate this point. It really is an extremely fast week-over-week growth in autonomous miles. And I don't think there's any company in the world that can match our scale with autonomous vehicles as we continue to ramp. 
The Cybercab fleet in Austin, for example, has grown by a factor of 10 since launch about a month ago. And the cumulative mileage is really -- when I look at the weekly chart, it's wow. I mean it looks like a rocket going to orbit basically is growing very fast. And I recommend if you want to try it out, come into Austin and you'll see Cybercabs in use at scale in Austin, as I think a lot of people saw with the Austin City Limits concert recently. So this is really going to a very good place.
Regarding Optimus, we've started like what I'd call early production on our high-volume line in Fremont. I want to elaborate on this point because -- and I've said this before that the growth of Optimus, it's an S-curve, but the initial part of the S-curve is -- has a shallow slope and is somewhat bumpy because it is such a radically new product. So the way to think about it is there's like 10,000 things that have to go right for production of the robot, and it will move as fast as the slowest least likely of the 10,000. But we do have the vast majority of a 1 million unit per line -- production line landed in Fremont right now. But I would expect that it takes us probably at least a year, maybe a little longer to get to that annualized rate to get to 20,000 units a week. So this is just fundamentally because there's still parts of the design that are changing. 
Like a lot of people ask me about Optimus. That's why I think I've got to kind of sort of belabor this point because if people aren't -- don't sort of understand like new technology that well or volume production of complex new hardware that well, it sort of seems like, well, can't you just make a whole bunch of these things immediately and send them out. And it's like, no, you've got to basically build up an entire gigantic global supply chain and have domestically a very, very big factory and everything has got to work. And there's still some things we need to tweak about the design because you need to deliver a robot that is safe and reliable and has long duration. So it can't, like, wear out after a month. 
And there's still quite a lot of work to do with regard to the AI and the robot for it to be truly useful for open-ended tasks. But like I said, if -- I would expect that the AI, the electromechanical design and the reliability and duration -- usage duration, like the usage life of the robot, I expect -- I do expect these issues to be solved around the end of next year. So that's the time to expect when we're delivering Optimus to companies outside of Tesla. And I remain convinced that Optimus will be the biggest product on Earth and humanoid robots in general will be the biggest product on Earth. So Optimus is a very big deal, but I don't want to temper expectations that we still have a lot to get through, and it's about a year or so that will take us to get through all that stuff. But as to the best of my knowledge, there is no one that is even close to Tesla with respect to a general purpose humanoid robot. 
Regarding the Terafab, the Austin-based research fab is progressing quickly. We'll begin commissioning machinery in the first half of next year. And hopefully, if things go well, we'll make our first test chip just to see if we can make any chip at all around May or June. So that's, I think, pretty exciting. And then we're -- our aspiration is to be making some kind of useful chip at volume around Q3 of 2028. So, and as I said publicly, the Terafab, I think, will be the most valuable building in the world and will probably have an economic value that will place it in the top 20 of countries. So it's an epic project. And this will be an incredibly important asset, if not a necessary asset in order to scale, especially Optimus as we can address bottlenecks in semiconductors, whether it's memory, packaging, logic or whatever the case may be.
With regard to a potential merger with SpaceX, I think I said everything that should be said yesterday, tap-dancing through a minefield there. And yes, that's it. 
In conclusion, we're super excited about our autonomy and robotics road map. There's a lot of incredibly awesome stuff coming. And I'd like to once again thank the Tesla team for their strong execution and all of our supporters for joining us on this journey.

**Travis Axelrod** (Executives):
Great. Thanks very much, Elon, and Vaibhav has opening remarks as well. Vaibhav?

**Vaibhav Taneja** (Executives):
Thanks, Travis. We continued our progress on a lot of fronts in Q3. Elon already covered a lot of them. Additionally, which I'd like to add is we also started deliveries of Megapacks with our in-house LFP batteries. And for the first time, 2 consecutive quarters of vehicle deliveries of over 480,000. 
On the automotive business, we exited the quarter with our highest backlog in 4 years, with deliveries constrained primarily by production. We are, therefore, focused on increasing production at all our factories to meet this growing demand. While we are actively working to increase production, it does take some time to get every aspect dialed in from supply chain to manufacturing to delivery logistics. 
The Model Y continued to outperform in the quarter and set delivery records in several key markets. Based on the preliminary data which we've gathered, we believe that it was the #1 selling BEV in Europe and the #1 selling passenger car in South Korea. We also set new records in key markets, including Australia, Japan and Taiwan. 
As Elon said, FSD continues to be the key driver for demand. In Q3, over 75% of deliveries in North America included a sign-up for paid FSD subscription at the time of delivery, which is approximately 20% higher than Q2. Overall, the FSD attach rate continued to improve, reaching over 1.7 million paid customers globally, of which, for the first time, 50% is based on subscriptions. Given the strength of FSD in the U.S. We are taking extra steps to sell certain cars in Europe with some benefits to try and get more fleet out there before a broader FSD approval is obtained.
On automotive margins, excluding credits, increased sequentially from 16.3% to 18.1%. The improvement in margins is driven by a higher mix of deliveries in APAC. While commodity price increases and interest rate changes continue to add to our cost and create further headwinds, we have adjusted the vehicle financing programs to partially offset for such costs.
On the energy business, we had our second best quarter of deployments of 13.7 gigawatt hour of energy storage. Energy gross margins improved from 20.4% to 33.1%. The sequential margin improvement is primarily attributed to tariff refunds recognized in the quarter and warranty true-downs resulting from alignment with our vendor on certain cell-related costs to be reimbursed by them. As Elon said, the business is witnessing extreme demand from data centers, and we are doing our best to increase production. And accordingly, we'll see improvements in ASP and further improvements in margins as we move forward. Services and other margins improved sequentially from 14.1% to 15.9%, an all-time high. This was the result of strength across service -- across several of the businesses in services and other, including supercharging and insurance. 
The Robotaxi business, which is part of services and others, continued to grow with the launch of Cybercab's rights in Austin. Cumulative unsupervised miles 8x in the quarter, as we had weekly double-digit growth throughout the quarter. We're taking all the learnings from our Austin expansion to help us prepare for broader Cybercab launch in other markets. Our priority is progressing the density and expansion of the network through vehicles that provide the best experience like the Cybercab, we will also continue to augment the fleet with other variants over time to address the terrestrial transportation needs of the total population. 
I'd like to stress that what we are trying to do is literally take over every part of terrestrial transportation, not just getting people -- we're starting with getting people from one place to the other, but we want to basically own this transportation of any kind on Earth. 
We are in a huge investment cycle to set us up for the future. Therefore, as previously guided, operating expenses continue to increase sequentially. Most of the increase came from significant research and development-related activities, including SI development costs such as depreciation from additional compute, chip development and preproduction ramp costs for new products like the Optimus, Megapack 3 and Semi truck. This trend of growing OpEx would continue till we commercialize these new products. 
Net income was impacted from a mark-to-market reduction of our SpaceX holding of $142 million, which was offset by a Bitcoin mark-to-market gain of approximately $290 million. We continued our efforts to manage cash efficiently and responsibly. We ended the quarter with positive free cash flow of over $1.5 billion and an overall cash and investment balance of over $45 billion. We're revising our CapEx guidance to be approximately $20 billion for the current year as a result of managing our capital deployment efficiently and plan to fund it primarily from our cash flows from operations. Additionally, during the quarter, we secured capacity to borrow up to $30 billion to support the expected growth in CapEx. Our confidence in the cash generation capacity of our business and the investments we are making drove our belief to secure shorter-term financing. We don't plan to make any draws under any of the new facilities in this calendar year. 
The money that we received from the tariff refunds is being reinvested to expand production capacity in the U.S. I'd like to stress on this that we like to do a lot of hardcore, real grunt work to get production facilities up and running. And so our CapEx for the next few years would continue to expand as we add more Robotaxi fleet, we expand our production capacity for Optimus, install manufacturing capacity for solar, purchase additional SI compute infrastructure and build a semiconductor fab. This strategy will position the company for the next era of growth and disrupt many existing markets while creating new ones. 
This is by far the most exciting time to be at Tesla. The foundation being laid around autonomy, robotics and energy is setting us up for an extremely bright future. I would like to end by thanking the Tesla team, our customers, investors and suppliers for their confidence in us on this journey.

**Travis Axelrod** (Executives):
Fantastic. Thank you, Vaibhav. Now we're going to go to questions from say.com.

**Travis Axelrod** (Executives):
The first question is, how does the Cybercab fleet scale past Austin? And what's the regulatory path outside Texas given NHTSA's Open Safety Review? 
Ashok, do you want to take that?

**Ashok Elluswamy** (Executives):
Yes, I'll start here. First of all, we launched Cybercab this quarter, which is very exciting. We achieved that by mostly learning from data from the other vehicle platforms, for example, Model Y, Model 3, et cetera. All of the data helped make the Cybercab without requiring a ridiculous amount of vehicles to produce the data. 
So we are seeing very good scaling in terms of Cybercab's AI capabilities. We launched in Austin, but that's only because we had some cabs and we want to swarm Austin with Cybercabs everywhere. But there's no fundamental reason that we are limited to Austin. In fact, next month, we'll be launching in Dallas and then the same software just scaled to lots of other cities along with the Model Y Robotaxis.

**Travis Axelrod** (Executives):
Great. Thanks very much. The next question is, what are your thoughts on crowdsourcing training data for Optimus versus your internal Optimus Academy approach? Is data currently the primary bottleneck? I think you covered this quite a bit, but any other color there?

**Elon Musk** (Executives):
I mostly talked about this already, but it's not crowdsourcing is not the issue for Optimus. There's a lot of things we have to get right about the AI architecture that we're still working on. We're making good progress, but that needs to be sorted out. And really, in order for Optimus to get the training data we need, we actually need to make a lot of Optimi. So we need to make, I think, on the order of 10,000 or 20,000 bots and then have them do self-play and we're building up an Optimus Academy where Optimus can practice doing a very wide range of tasks. And then we can use that data in sort of a flywheel to make it better and better at these various tasks.
A big difference with Optimus versus the cars is we don't have this vast fleet of cars from which we can gather training data. So with Optimus, we have to bootstrap it by making the robots and having them do self-play, which is really how a human learns to navigate the world. That's -- you can see this when you have a toddler and they grow up and they -- initially, they're sort of wobbly and they don't know how to do things and eventually, they learn to wipe their own ass, which is a big milestone. As anyone's who has had kids knows. And then they learn to read and do all sorts of things and be able to do these things. And they learn this by playing. And we actually need Optimus to play at scale in order to have it be really good at tasks in the real world. 
And Ashok, you may want to add to that.

**Ashok Elluswamy** (Executives):
Yes. Like I mentioned, Elon, for the car, we actually have the data from the car's embodiment itself. But for Optimus, there's no exoskeleton for humans to get into and like make Optimus into a puppet or something like that. Like we have to learn -- Optimus has to learn by watching other people do task initially and then start practicing the task yourself. For example, you can -- if you're watching a soccer game, just because you're watching, it doesn't mean you'll be good at soccer yourself. You've got to like start practicing and get good at the game and learn from the bot's own experience. And we are setting up this huge reinforcement learning cycle with initial base training done from humans to bootstrap and then put it on Optimus and do a lot of self-play both in simulation and in the real world to learn on the embodiment of Optimus itself. I think we're pretty close to having very good results in this big loop.

**Elon Musk** (Executives):
Yes. I think we may be ready to release like an Optimus video in a month or so. I want to make sure that like when we release this video that it's not like a canned demo that -- like when you see these robot, humanoid robot demonstrations, some of them look very impressive, but they're not really using any kind of advanced AI or SI. I mean they're like preprogrammed deterministic tasks. And if you actually try to use that humanoid robot in the real world, you would have a lot of trouble. It wouldn't work basically. So I want to release a video that's where it's Optimus doing things that are not preprogrammed. And I think that would be -- it's maybe a month or 2 for that to have a demo that you can believe what you see type of thing. 
And then there's another milestone that's, I think, important we want to get to, which is to integrate our -- the Tesla AI5 chip into Optimus, which if things go according to plan, will be in approximately April of next year. And that's a giant improvement in capability with an order of magnitude more sort of more operations per second. Like it's an order of magnitude more compute, AI5 versus AI4. And that will help Optimus a lot because the degrees of freedom that a humanoid robot has to deal with are far greater than what a car has to deal with. So it is a bit of a struggle to squeeze the -- everything needed to operate with all the degrees of freedom of Optimus and the wide range of tasks. If you can think of a humanoid robot is going to do like 1,000x more things than a car would do. That's some very big number basically. 
So I think the additional compute of AI5 will make a big difference, and that comes in, hopefully in volume around April of next year. And that's why I think like all the pieces like the refinements in electromechanical dexterity, making sure Optimus can operate for long periods of time without wearing out, getting the AI software right and the AI5 chip integrated. All of these things kind of come together. That's why I think about a year from now is when it's something that would be -- that you could ship to customers. And it would also be reaching scale in production. So that's probably the right timing to think about.
In terms of the initial customers for Optimus, I think it probably would be things that are industrial applications at first, things that are like dangerous repetitive tasks, things that people really don't want to do. So -- and that you want done basically 24/7. So like around-the-clock stuff. That's going to be the highest value for Optimus in the beginning. As we scale production, of course, it would be something that people can buy for their home. But the initial high-value use will be -- the highest value use, I think, will be kind of heavy industry, dangerous tasks or things that may cause repetitive stress injuries and that you want done 24/7. So that's the way to think about it.

**Travis Axelrod** (Executives):
Great. Thank you, guys. The next question is very similar. It's about Optimus scaling, so we can go past that one.

**Elon Musk** (Executives):
I just answered that one basically.

**Travis Axelrod** (Executives):
And the next question is, when can we anticipate FSD unsupervised in customer cars? 
Ashok, do you want to kick that off?

**Ashok Elluswamy** (Executives):
Yes. Like I mentioned earlier, the software for Cybercabs and Model Y is the same, like -- and pretty soon, we'll be able to release the same software as part of the v15 release to customers. So the only additional requirement is to make sure that, for example, the customer model-wise can be part of the geofences and the fleet management that Tesla has for it to be fully autonomous. We suspect somewhere around Q2 next year is when we can turn on some of the first customer vehicles to be part of the Robotaxi fleet.

**Travis Axelrod** (Executives):
Great. Thank you, Ashok. The next question is, when will the Cybercab be available for customer purchase/ownership? 
Lars, did you want to kick this one off?

**Lars Moravy** (Executives):
Sure. Thanks, Travis. I think it builds a little bit on what Ashok just said. But in short, we're trying to get Cybercabs to customers by the end of this year, 2026. Obviously, we're producing them in our line in Texas, but all of those are currently going to our own internal Robotaxi fleet. And as Tesla grows, we'll mainly deliver fully designed autonomous vehicles to our customers. And Cybercab will be the first. And so as we start small this year, and we learn about all the things Ashok mentioned about delivery and ownership and fleet management of autonomous vehicles in customer hands, we'll continue to scale that.
Elon, I don't know if there's anything you want to add to that?

**Elon Musk** (Executives):
No. I mean Cybercab is primarily going to be something that is offered as like transport as a service whereas our other cars would be more the cars that you'd want to own like the 3 and the Y and whatnot, and Roadster, obviously. But the vast majority of the Cybercab stuff will be essentially Tesla-owned and transport as a service.

**Travis Axelrod** (Executives):
Great. Thanks, guys. The next 2 questions are quite similar around unit economic costs. The first one is on per paid Robotaxi mile. And the second one is cost per Optimus unit. And we already covered what are the first customer -- paying customer looks like. So, VT, did you want to -- Vaibhav, did you want to get into the unit economics question here?

**Vaibhav Taneja** (Executives):
Yes. So on the Robotaxi side, the main geographies where we are operating, we're already seeing utilization improving. And week by week, as Elon was talking about, we look at the miles and how many paid rides are happening. So are we at our goal of $0.30 today? No. But do we see a path to get to that? Very -- yes, we do. And it's all about scaling operations. And what you'll see over the next few months is that we -- today, Cybercab, which is the primary robotaxi product is available only in Austin. But we do plan to bring it out in some other cities before the end of this year. And as we add more Cybercabs, we are also learning from the operational experience of managing a fleet, pickup and drop off, cleaning, all those things. So all those costs are being dialed in. And that's why, like I said before, we definitely see a path to get to our $0.30 target.

**Travis Axelrod** (Executives):
And then did you want to cover the Optimus costs?

**Vaibhav Taneja** (Executives):
Yes. I mean I think Optimus cost, internally, we are tracking pretty well in terms of how the design has matured. But it would be a little too early to say that we have got there because like Elon was saying, we're still making a lot of design iterations. The good thing is when you look at it from a cost perspective, we're trending closer to where we would say our Cybercab costs would end up being.

**Elon Musk** (Executives):
Yes.

**Travis Axelrod** (Executives):
Great. Thank you very much, Vaibhav. The next question is, when do you -- we've kind of already answered this. When do you anticipate Optimus will be generating revenue? So we covered that in the prior question. 
The next one is mapping for FSD continues to be a problem. The 3 biggest issues are recognizing proper speed limits, parking and typical routes. I understand you use various third-party maps, but why not use your own maps? Authorized trusted and verified Tesla owners to provide the input. 
Ashok, did you want to kick off here?

**Ashok Elluswamy** (Executives):
Yes. Yes. You're totally right that we shouldn't be depending on external people's maps. So we are building our own maps, but not like the same way as OneMoreMap (sic) [ OpenStreetMap ]. We are building an entirely new architecture with essentially AI-based mapping and navigation. It's going to be super awesome. It's going to be integrated with voice. You can like talk to it, ask for different routes. It's going to learn your personalized preferences, plus also the fleet preferences. The collective intelligence of all the cars are going to flow into making the maps and navigation be super cool. We'll start -- you'll see the start and end of trips already use this technology pretty soon as part of the v15 release. And over the next several months, it's just going to take over all of the navigation functions, parking, destination handling. And just will know you better than you know yourself in some regard for the driving task, and then handle it fully.

**Travis Axelrod** (Executives):
Great. Thank you, Ashok. And then our last question is, what is the current production rate at your existing factories? Do you anticipate building new ones?
Lars, do you want to kick that off?

**Lars Moravy** (Executives):
Yes, sure. I think Vaibhav kind of touched a little bit on this in his opening remarks. And I'll say our factories are operating at record rates this quarter. And of course, they can only build at the rate of the least lucky process or component. And Vaibhav mentioned that we are actively managing all the aspects of production. 
As we've spoken in our past calls, we've made strategic investments globally to increase rates of our current factories over the last year plus. And this quarter, we are starting to see that, and we expect that to continue in coming quarters as those investments come to fruition. 
I mean beyond that, we've also -- are working to ramp Cybercab, obviously, in Giga Texas, and we've applied for proper permits to expand the factories in Berlin. And as also Elon mentioned, we just started our new semi factory in Reno. So in short, we are building new factories, yes, and we're aiming to hit that 5 million goal by 2030, as Elon said.

**Travis Axelrod** (Executives):
Great. Thank you very much. That's it for the say.com questions. Now we will be going to analyst questions. As a reminder, as Elon said, we will not be addressing any questions today on a potential merger with SpaceX. With that, the first question comes from Tom from RBC.

**Gautam Narayan** (Analysts):
It's on FSD. So the attach rate, I think according to my math is like 30% to 40% in North America on a paid basis. It's becoming a flywheel, as you said, for more car sales and the attach rate exceeds other automakers subscription-based autonomy by a lot. I guess in a weird way, could you guys be a victim of your own success in seeing other carmakers noting the success and trying to aggressively come up with similar L2+ type products, maybe partnering with NVIDIA or Qualcomm? And if that happens, could that be deflationary for FSD pricing?

**Vaibhav Taneja** (Executives):
I think people take this thing very simply that you can -- if the software [ can't be solved ], it's not because, I mean -- I'll let Ashok get into it. But basically, it's a very hard problem.

**Elon Musk** (Executives):
Super hard problem.

**Ashok Elluswamy** (Executives):
Yes, it's easy to get to the first 90% and make like a cool-looking demo. But when you get in the long tail of this problem, it's so long that people don't realize anyone with their sane mind should not attempt to solve this problem. It's like so difficult and so long tail. And especially to get to a safety point where you can drive safely for millions of miles with no injuries and so on, that's going to be extremely hard. As we release unsupervised FSD to the broader customer fleet, it's just going to be -- I don't think anyone can like match it in several years.

**Vaibhav Taneja** (Executives):
And one other thing which I'll say, if it wasn't clear that when -- especially in our showrooms here in the U.S., customers are now coming in and saying, "Can we get into an FSD drive?" They're not asking for 3, Y or Cybertruck. They're saying, "Can we get an FSD drive?" And that has become the key driver because what it does is it actually opens up a lot more flexibility for different parts of the population wherein they had issues driving conveniently before. Now they're getting their freedom back by being able to use FSD. And a lot of folks are just like -- I mean, it's a game changer. I mean if you haven't tried it, I keep saying it every time, if you do it, you won't be able to go back to driving any other car.

**Travis Axelrod** (Executives):
Tom, do you have a follow-up?

**Gautam Narayan** (Analysts):
Yes. Follow-up is similar to that question on China. I mean there, it seems like autonomy is like table stakes. Is it the same kind of answer as question one that they're not going to be able -- those carmakers aren't going to be able to develop similar products that you guys have had on FSD? Or do you see there that being definitely a different pricing dynamic?

**Vaibhav Taneja** (Executives):
I mean, at the beginning, like definitely, the leapfrog which we have in terms of this technology isn't there with any of the other Chinese OEMs today. And like we're working very diligently to try and get broader -- I mean, FSD approval in China. it is hard, but for certain cars, we have been able to have FSD operating. And whatever people have tried -- whoever has tried it there, they understand how much better it is as compared to any of the competition. And in fact, I don't know if you've seen this, there have been some competitor CEOs who have come and done FSD drives here in the U.S., and they themselves have been blown up as to what FSD is capable of doing. So it is a similar answer. 
And again, we're not taking it lightly. We're actively working with the regulators in China because I don't know if you saw this, but we did release our -- we've released our safety report on FSD before, but we've also released our unsupervised Robotaxi safety report. We just think this is the right way to get people into a safe environment because you know the amount of accidents which happen because of driver -- drivers not being alert. And this is the only way we can ensure that there are less casualties in the world and any regulator who looks at the data, it would be very hard for them to refute it.

**Travis Axelrod** (Executives):
Our next question comes from Emmanuel from Wolfe.

**Emmanuel Rosner** (Analysts):
So on Robotaxi, you've talked about sustaining double-digit week-over-week growth in unsupervised miles. I'm curious if there's a way you can triangulate that for us into revenue and maybe profitability of the Robotaxi business. If you sustain, let's say, 15% week-over-week growth in these miles, you'll probably cross 10 million miles by the end of the year. How many of those -- how many miles would you need to generate gross profit?

**Vaibhav Taneja** (Executives):
I mean -- so I think Elon talked about this a little bit at the beginning that using exponential math, this would become a significant part of our revenue and profitability in '27.

**Elon Musk** (Executives):
Yes. I wouldn't say it's not like going to move the needle this quarter. But if you say like maybe -- I think it starts to become noticeable probably in Q2 and then probably a big deal by Q3 or Q4 of next year.

**Vaibhav Taneja** (Executives):
Exactly.

**Emmanuel Rosner** (Analysts):
Got it. And then if I think about it in terms of fleet size, so I think your Cybercab line capacity is listed at more than 125,000 units a year. Production just recently started. How do you expect the ramp-up curve to be on the Cybercab line?

**Vaibhav Taneja** (Executives):
I mean I'll kick it off, but then I'll also let Lars chime in. But I would give kudos to the engineering team. They have designed a product because not only do I talk to the engineers, I also talk to the manufacturing guys. They think this is one of the easiest product for them to scale in terms of manufacturing. So scaling would not be that much of a challenge. I think the key thing which we're trying to make sure is that we have all the regulatory approvals where we can start deploying the Cybercabs as fast as we can produce them. 
And again, Lars, feel free to chime in.

**Lars Moravy** (Executives):
Yes. Thanks, Vaibhav. I appreciate the accolades. The team definitely crushed it on the Cybercab design and manufacturing. Just to your point, we have 50% less parts than any other vehicle we've ever built. So that's 50% less things to go wrong. We've definitely been bursting the Cybercab line to see how fast we can run it. I think the listed capacity is more of a rate at which we're capable of running today, but the actual capacity of that vehicle line is significantly higher. 
Right now, we're building at the rate that the Robotaxi service needs the vehicles. And I'll say Ashok and I are in a bit of a race of who's going to stay ahead. He's got exponential growth coming on the miles month-over-month, and we're going to look to meet that as well with the vehicle production.

**Travis Axelrod** (Executives):
Great. The next question is going to come from Andrew from Morgan Stanley.

**Andrew Percoco** (Analysts):
So I want to start on your energy business. You're clearly seeing a lot of demand on the energy storage or Megapack side, and you've got some goals to bring on your own solar manufacturing. But I was just hoping to get a little bit more insight in terms of how you're thinking about Tesla's role in enabling both distributed power, but also distributed compute. I think last quarter, you alluded to a Megapod product. So just hoping to get a little bit more insight in terms of what you're envisioning there and ultimately how big this could be for Tesla.

**Elon Musk** (Executives):
I think it's still early days on that front. We don't know the full extent of how -- what that will -- how that will unfold. I think we'll have a better sense for that probably in maybe end of Q1 or Q2. But it does have a lot of potential. It's just hard to say how much potential right now.

**Andrew Percoco** (Analysts):
Okay. Understood. And then maybe just a follow-up on Robotaxi. It does seem like you've kind of hit an inflection point here in Austin over the last month or so since you launched the Cybercab. So would you generally say that the bottlenecks at this point to growth are more regulatory driven as you think about expanding into new geographies and that you've kind of gotten through most of the hurdles on the software side. Just kind of curious how you would generally kind of categorize some of those growth hurdles in some of the incremental regions you're planning on scaling into over the next few months.

**Vaibhav Taneja** (Executives):
I think the -- I mean, there are still certain software challenges, which we are still working through. Ashok talked about it. So maybe Ashok, maybe you can...

**Ashok Elluswamy** (Executives):
I'll chime in, yes. For example, we had like initially had the Robotaxi service from 6:00 a.m. to 9:00 p.m., and then we expanded to 10:00 p.m., 11 p.m. Now it's going to be pretty soon 2:00 a.m. So we are slowly expanding the availability of Robotaxi, and that is driven by the capability of the AI software. And we just want to make sure that there's not a single safety incident. That is our operating principle. And even if there's the slightest possible risk at all, we don't, like, take on that risk. And so we are very risk averse in that sense, as in we want zero injuries or anything bad happening, and that is the driving principle. And we will see that over the rest of this year, we'll unlock 24/7 operation, go to higher speed roads. And we think all of that is necessary to sort of like scale and offer a great product to a lot of users. And that's why we wanted to both do the breadth first of doing multiple cities. 
We did -- we do 6 cities now. We are also doing the depth of like having a lot of vehicles in a single city, which is in Austin, and we'll expand to more weather conditions, day and night conditions, highways and high speeds. And all of that will be done hopefully by the end of this year, at which point you will see a lot more scaling, a lot more cities being covered by Robotaxi. So it's not purely regulatory or something like that. It is technology driven, but we do see that pretty quickly become regulatory perhaps in Q1, Q2 time frames.

**Travis Axelrod** (Executives):
Great. The next question is going to come from Edison from Deutsche Bank.

**Xin Yu** (Analysts):
First, I wanted to ask about Terafab. I know, Elon, you mentioned that you had an aspirational goal of 2Q '28. Do you have a sense on how much capital needs to be invested to get there? And also what kind of milestones we should be on the lookout for on the way there?

**Elon Musk** (Executives):
Well, it's going to be some pretty significant capital. It's certainly in the tens of billions for Terafab. Although we've got to figure out like what the sort of relative split is between SpaceX and Tesla in terms of who pays for what at Terafab. But it's not going to be less than tens of billions in capital equipment up through early 2028. And then it will be -- it will probably be north of $100 billion long term.

**Vaibhav Taneja** (Executives):
Yes. And I'll just add, the first set of equipment for the fab, which Tesla is building, we've actually already placed most of the orders. And that's why when Elon was talking about middle of next year, that is from the first fab, which...

**Elon Musk** (Executives):
The research fab.

**Vaibhav Taneja** (Executives):
Research fab.

**Elon Musk** (Executives):
Yes. That's where we're just figuring out how to work the equipment type of thing. But real production would be late '28, which is lightning fast by fab standards.

**Xin Yu** (Analysts):
Understood. Understood. And then just a quick follow-up on Optimus. I know you mentioned that we could see a video soon that there's quite a bit of progress, but you're still making some refinements. I guess just generally speaking, where do you see most of the design changes still happening going forward? Is it still the hand that's an issue? Anything you can call out there?

**Elon Musk** (Executives):
Yes, it's most of the difficulty -- I mean, Konstantinos, why don't you answer this question?

**Konstantinos Laskaris** (Executives):
So hand is one of the most challenging hardware areas actually. Most of the electromechanical system, I would say, is relatively high confidence, meaning like that it has converted to something that works decently well. The hand is, from an electromechanical point of view, more complicated than actuators for the locomotion system, for example. Also there are some bespoke gears that are carrying a lot of burden for consumption and for reliability that we are developing still. Yes, this would be the most...

**Elon Musk** (Executives):
Yes. It's mostly the hand and just kind of the fine-tuning of the hand design and the fingers, especially just -- it's a hard problem because humans have self-repair, like our hands repair -- our body repairs itself, but robots don't. So you have to -- and our fingers are kind of squishy and have lots of sensors in our skin. It's hard to make a hand that is -- that can handle lots of wear and tear, but it's still squishy enough to pick up delicate objects and has all the sensors and doesn't damage the sensors when you do repeated actions. And there's a lot of little things that you realize actually what an incredible thing the human hand is at the end of the day. So it's mostly from an electromechanical standpoint, the hands. There are other things that are improving as well throughout the robot, but that's the main thing.
And then as I mentioned, upgrading the intelligence -- the onboard intelligence of the robot with AI5, which is a big step change in intelligence that will help a lot with the capabilities of Optimus. So I've said before that like humanoid robots, biggest product on Earth and its usefulness will be -- it's a rough approximation multiple of the electromechanical dexterity, the AI software and the AI chip hardware. And all 3 of those things are improving exponentially. I think we used that word a lot, but -- and the value is roughly those 3 things multiplied by each other. And then the Optimus robots will build the future Optimus robots. So you have a recursive function. So when you have a recursive multiplicative exponential, things will really grow extremely fast. They may start from a small base, but they're going to grow to crazy levels. And I think at some point, there will be more humanoid robots on Earth than there are humans.

**Travis Axelrod** (Executives):
Great. The next question comes from Alex from Bank of America.

**Alexander Perry** (Analysts):
I guess just first on Robotaxi. So it looks like for Robotaxi, you're pricing lower than competitor rideshare and other Robotaxi players in most markets. Is that the plan to do longer term to take market share given some of your structural cost advantages?

**Vaibhav Taneja** (Executives):
Yes. I mean, remember, when you're comparing -- you're comparing us with rideshare, which has a driver in there, and we don't. Plus, we are manufacturing the car ourselves. So our cost basis overall is different. And I think I said it in my opening remarks, and I'll say it again, just don't want to be too repetitive, but basically, our goal is to take over any kind of transportation.

**Elon Musk** (Executives):
I mean I think we -- unless we are stopped by governments, which is certainly a possibility, like if they're trying to protect the domestic industry, I think Tesla will end up doing a majority of all passenger miles on Earth in any country where it is allowed to operate freely.

**Vaibhav Taneja** (Executives):
Yes.

**Elon Musk** (Executives):
And you can come back and look at this prediction, but I feel confident about this prediction.

**Alexander Perry** (Analysts):
Really helpful. And then just my follow-up question. I guess just on the key metric here, so unsupervised miles driven. So I think it grew at a high teens weekly growth rate since late July. Is it still the expectation you'll continue to grow that at double-digit weekly rate through the balance of the year? 
And then what is really enabling that type of growth? It seems like you've definitely hit a comfort level and scaling much more rapidly. How much of that is Cybercab? How much of that is better safety validation with the latest version of FSD? And then just on fleet composition, do you expect Cybercab to represent a majority of the Robotaxi fleet over time?

**Ashok Elluswamy** (Executives):
Yes. We will continue the scaling for the foreseeable future. We don't see any hurdles along the way. Obviously, there's work required, but we do see a clear path towards scaling to millions of vehicles over the next several months. 
This is happening due to like primarily the technology investments we have made over the last several years and also in v15 stack that we alluded to earlier this year. Like all of the foundations is like hard to see. It's like an iceberg. People only see the tip of the iceberg. There's a ton of work that goes into it. And like now we are starting to see the payoff of all that work of like developing end-to-end neural networks, learning from humans and so on, all of that is paying off. 
So that's what you're seeing. That -- you're seeing the result of many years of work. It didn't just like happen in the last several months. Yes. And the same technology should scale to millions of vehicles across all over -- like wherever we are allowed to operate.

**Travis Axelrod** (Executives):
Our next question is going to come from Pierre from New Street.

**Pierre Ferragu** (Analysts):
I just wanted to come back like I'm very really fascinated by 75% of, like, U.S. cars selling with FSD. And the interesting thing that if you look at the cars, they probably generate on sale the day they sell like about $7,000 of gross profit. But then, of course, FSD generates more than $1,000 a year. And so it does -- it makes like a minimal impact on numbers in the quarter the car is sold. But over the lifetime of the car, it probably at least doubles the profit per car. And so the place where I'm going -- want to get to is, am I looking at it the right way? And are you at some point going to disclose for us like the annual recurring revenues that FSD represents? And I did my own math, and I'm thinking it's probably now approaching $1 billion of ARR. Is that the right order of magnitude?

**Vaibhav Taneja** (Executives):
Yes. I think the numbers which you shared are correct. And as it scales further, we will start sharing more metrics around FSD, not just the revenue, but also other key metrics around it.

**Pierre Ferragu** (Analysts):
Okay. And as a quick follow-up, do you have like a good sense already? And can you tell us about like the retention rate? Like do -- how many people like 3 or 6 months down the line sticks to the monthly subscription if you see a percentage of drivers falling off?

**Vaibhav Taneja** (Executives):
Yes. I mean, like I said, we will share more metrics around churn rates and whatnot. But -- the reason we are not doing it at this stage is there are a lot of things which we are doing, especially with new countries being added, that we offer free trials. 
And one thing which I'd also like to make sure it's clear, when I say in North America that more than that 75% attach rate at the time of delivery, this is like every car which we're delivering comes with a month of free FSD subscription. And still people are signing up, even though they have that free available.

**Travis Axelrod** (Executives):
Great. Our next question is going to come from Colin at Oppenheimer.

**Colin Rusch** (Analysts):
Elon, can you talk about the strategy around ramping Optimus production just a little bit to start training even if the hands aren't fully baked with the final design? It seems like there's a lot that you could end up doing in terms of the training cycle and maturing some of the simulation technology even without perfected hands.

**Elon Musk** (Executives):
Well, that's what we're doing is we're building robots that do not have perfected hands, and we are making progress with Optimus training and ironing out all aspects of the supply chain and the production system. 
So that's -- we're doing all these things in parallel, like this giant production line in -- at our Fremont factory, massive supply chain and then fine-tuning the design and engineering simultaneously with the AI software. So all these things are happening simultaneously. And we're growing as fast as humanly possible here. I don't think anyone is going to have -- and in fact, I'd be stunned if anyone has a robot that is remotely competitive with Optimus when we go -- when we start delivering it to customers, which is likely to be towards the end of next year.

**Vaibhav Taneja** (Executives):
Yes. And you should know that not only the Fremont factory, we've also started constructing a factory here in Austin, which would be able to do a lot more robots as compared to the Fremont one. So going back to what Elon was saying, we're doing whatever we can. We're not stopping. We're just going at the fastest pace as we can.

**Elon Musk** (Executives):
Yes. We're definitely, as I say, in Vegas betting on the come.

**Colin Rusch** (Analysts):
Awesome. And then in terms of the semi cap -- capacity availability, can you talk about how you're navigating that with the suppliers? Obviously, seeing some deposits get put down on equipment and getting deliveries moving forward is a net positive on Terafab. But are there some more aggressive things that you can do to start getting ready for the larger ramp now? And how should we think about that flowing through the CapEx budget?

**Elon Musk** (Executives):
It's not a massive impact right now. I think CapEx is actually -- it's actually ending up being a little lower than we anticipated. But it will start to become more meaningful next year and then noticeable like in the tens of billions in '28.

**Travis Axelrod** (Executives):
All right. We are coming up on time here. We appreciate everyone's questions, and we look forward to talking to you next quarter. Thank you very much, and goodbye.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TSLA_Q2_2026_Earnings_Call_20260722.md
- 2026-07-22｜Vaibhav Taneja｜guidance：CFO 說明自由現金流本季為負，原因是資本支出季增超過一倍，且下半年預期再增加（原話："CapEx more than doubled sequentially"）
- 2026-07-22｜Vaibhav Taneja｜guidance：CFO 表示資本支出未來兩三年持續成長（全年指引為超過 250 億美元，見同段上一句）（原話："CapEx will grow for the next 2 or 3 years as we expand our"）
- 2026-07-22｜Vaibhav Taneja｜guidance：CFO 表示研發為主的營運費用 2026 年及之後會持續成長（原話："we are in a big investment cycle"）
- 2026-07-22｜Vaibhav Taneja｜guidance：CFO 說明量產成長受供應鏈限制，不只電池也包括電子零件（原話："Production growth will be limited by our supply chain."）
- 2026-07-22｜Vaibhav Taneja｜guidance：CFO 說明已取得最高可借 300 億美元的債務額度（原話："the capacity to borrow up to $30 billion"）
- 2026-07-22｜Vaibhav Taneja｜guidance：CFO 預期機器人計程車車隊成長在年內加速，並擴展到新的美國市場（原話："have expanded to a total of 7 markets in"）
- 2026-07-22｜Ashok Elluswamy｜guidance：Ashok 表示預期無人監督里程的高複利成長在今年剩餘時間持續（原話："we expect to continue growing at such a large rate"）
- 2026-07-22｜Elon Musk｜guidance：Musk 說明 Semi 自駕預計年底或明年初可運作，但未來約六個月排在次要（原話："taking a bit of a backseat for the next 6"）
- 2026-07-22｜Elon Musk｜guidance：Musk 說明 AI5 預計明年中進入量產，且最先用在 Optimus（原話："AI5, which hopefully is in volume production"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 報告汽車毛利率（不含碳權）由 19.2% 降至 16.3%（原話："declined sequentially from 19.2% to 16.3%"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 說明上季有 2.3 億美元保固回沖與關稅減免，本季未重複（原話："we had a $230 million benefit from warranty true-downs and"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 的數字口徑：扣除上季一次性效益後，汽車毛利率大致持平（原話："excluding credits, would have been approximately flat"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 指出利率上升使利息補貼成本增加，對汽車毛利率有負面影響（原話："the cost of subvention has risen along with them"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 報告儲能毛利率由 39.5% 降至 20.4%（原話："energy gross margins declined from 39.5% to 20.4%."）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 拆解儲能毛利下滑原因之一為約 2.4 億美元保固補提（供應商電芯問題）（原話："First, there was a warranty true-up in the quarter"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 給出儲能長期毛利率區間（原話："gross margin rate in the mid- to low 20% range"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 報告服務及其他毛利率創高（原話："improved sequentially from 9.2% to 14.1%, an all-time high"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 說明淨利含 SpaceX 持股約 10 億美元的市價評價利得（原話："a mark-to-market gain of $1 billion on our SpaceX holdings,"）
- 2026-07-22｜Vaibhav Taneja｜competition：CFO 提到工業儲能均價在競爭加劇下下降（先前已預告）（原話："industrial storage is coming down amidst growing competition"）
- 2026-07-22｜Ashok Elluswamy｜competition：Ashok 主張純鏡頭方案的安全紀錄可驗證其技術路線，反駁需要光達的說法（原話："and affordable autonomy with just cameras"）
- 2026-07-22｜Vaibhav Taneja｜customer：CFO 說明期末訂單積壓為 2023 年以來最大（原話："We exited Q2 with our largest order backlog since 2023."）
- 2026-07-22｜Vaibhav Taneja｜customer：CFO 揭露北美約 55% 交車在交付時已啟用 FSD 訂閱（原話："about 55% of our deliveries had FSD subscription"）
- 2026-07-22｜Vaibhav Taneja｜customer：CFO 揭露 FSD 全球付費客戶數（原話："reaching nearly 1.5 million paid customers"）
- 2026-07-22｜Vaibhav Taneja｜customer：CFO 說明 FSD 變現成長主要來自訂閱，因多數市場已移除買斷選項（原話："the growth in FSD monetization will come from subscriptions"）
- 2026-07-22｜Elon Musk｜customer：Musk 說明儲能需求預期很高，並稱電池可使美國發電量近乎翻倍（原話："demand for Megapack being very, very high in the future"）
- 2026-07-22｜Elon Musk｜capital_allocation：Musk 表示今年是大規模資本支出年（原話："this is a massive CapEx year"）
- 2026-07-22｜Elon Musk｜capital_allocation：Musk 說明資本支出寧可資本效率略低也要更快完成（原話："it's okay to be a little less capital efficient"）
- 2026-07-22｜Elon Musk｜capital_allocation：Musk 提到已下單採購 Austin 開發用晶圓廠設備（原話："We've placed equipment orders for our development fab"）
- 2026-07-22｜Brandon Ehrhart｜capital_allocation：法務長說明今年稍早與 SpaceX 透過投資與框架協議深化關係（原話："we deepened our relationship through an investment"）
- 2026-07-22｜Elon Musk｜capital_allocation：Musk 提到可在超充站部署 Megapod 分散式 AI 運算，超充站電力約 7 GW（原話："something like 7 gigawatts of power at our Superchargers"）
- 2026-07-22｜Elon Musk｜product：Musk 說明 Cybercab 已開始量產（原話："The Cybercab has started production"）
- 2026-07-22｜Elon Musk｜product：Musk 說明 Optimus 即將開始量產（原話："we will soon start production with Optimus"）
- 2026-07-22｜Elon Musk｜product：Musk 校準預期：Optimus 量產曲線前段會又平又長（原話："curve will be quite flat and long"）
- 2026-07-22｜Elon Musk｜product：Musk 稱 Optimus 是 Tesla 迄今最難量產的產品（原話："product to scale manufacturing that we've ever made at Tesla"）
- 2026-07-22｜Elon Musk｜product：Musk 說明 Optimus 4 將在 Austin 生產，垂直整合程度更高（原話："For Optimus 4, which will be built in Austin"）
- 2026-07-22｜Elon Musk｜product：Musk 給出 Optimus 4 對 Optimus 3 的產能願景（加上多項但書）（原話："aspirationally 10 million units a"）
- 2026-07-22｜Ashok Elluswamy｜product：Ashok 說明早期 v15 版本已在機器人計程車車隊上運行，七條改進主軸已併入四成（原話："40% of those tracks merged"）
- 2026-07-22｜Elon Musk｜product：Musk 說明 Cybercab 因底盤全新，需先累積專屬行駛資料才能大量上路（原話："to accumulate driving data that is specific to the Cybercab"）
- 2026-07-22｜Elon Musk｜product：Musk 說明舊款（低於 Hardware 4）車輛未來將升級，計畫以下一代 AI 板為目標（原話："upgrade all cars with that are -- have less than Hardware 4"）
- 2026-07-22｜Elon Musk｜product：Musk 說明 Semi 的自駕工作排在 Model 3/Y 與 Cybercab 之後（原話："get self-driving working on the Tesla Semi"）
- 2026-07-22｜Elon Musk｜risk：Musk 說明機器人計程車的限制是安全可靠度，並稱任何傷人事件都會招致監管收緊（原話："the march of nines of reliability is, I think, the only"）
- 2026-07-22｜Lars Moravy｜risk：Lars 對紐澤西州的州級規定表示失望（原話："the stuff in New Jersey is a little bit"）
- 2026-07-22｜Elon Musk｜risk：Musk 表示若無 Terafab，Optimus 量產會受 AI 晶片供給限制（原話："constrained in our ability to scale Optimus production"）
- 2026-07-22｜Ashok Elluswamy｜risk：Ashok 稱至今 38 萬英里無人監督行駛無重大事故（原話："0 notable incidents over 380,000 miles."）
- 2026-07-22｜Elon Musk｜risk：Musk 感謝 Micron 在記憶體價格極高下給予 Tesla 大量配額（原話："a very significant allocation on reasonable terms"）
- 2026-07-22｜Elon Musk｜commitment：Musk 承諾機器人計程車維持垂直整合、不引入第三方叫車平台（原話："We expect to be vertically integrated with robotaxi"）
- 2026-07-22｜Ashok Elluswamy｜commitment：Ashok 表示新城市上線時間預期趨近於零，目標以整州為單位營運（原話："time to launch to a new city will continue to trend"）
- 2026-07-22｜Ashok Elluswamy｜commitment：Ashok 表示 Cybercab 製造目標與無人監督里程成長率大致對齊（原話："We have aligned our manufacturing targets to roughly"）
- 2026-07-22｜Elon Musk｜commitment：Musk 表示 Terafab 地點將於日後單獨發表，不在法說會上說明（原話："we expect to announce a location soon"）

### 問答異常語氣（迴避／改口／保留）
- TSLA_Q2_2026_Earnings_Call_20260722.md｜問：Colin Langan（Wells Fargo）問 Musk 是否看到 Tesla 與 SpaceX 合併的綜效、是否合理｜答法：Musk 未正面回答合併問題，表示不能在法說會討論，轉交法務長；法務長只談現有合作與框架協議
- TSLA_Q2_2026_Earnings_Call_20260722.md｜問：William Stein（Truist）追問 Optimus 4 何時開始量產｜答法：Musk 接著只回答硬體升級與 AI5/AI6 晶片，未給 Optimus 4 的開始量產時程
- TSLA_Q2_2026_Earnings_Call_20260722.md｜問：Dan Levy（Barclays）問儲能是否長期供給受限，以及資料中心與電網調峰的需求占比｜答法：Musk 談電網平衡、資料中心電力平滑與美國發電量論述，未回答供給是否受限，也未給資料中心與調峰的占比數字
- TSLA_Q2_2026_Earnings_Call_20260722.md｜問：Colin Langan 追問為何不先在一兩個城市把車隊規模做大（媒體報導車數僅數十輛）｜答法：管理層以里程成長、跨城市驗證通用性、各城市監管不同回應，未給車隊車輛數

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
{"date":"20260705","verdict":"迴避","role":"不持有/迴避","H":{"status":"ok","format":"table","rows":[{"id":"H1｜robotaxi 規模化","text":"FSD v15（~10B 參數）在 2026 末/2027 上線後，unsupervised 車隊由現 ~20 台放大至數千台、擴至 5+ 城市，形成可營運的自駕網絡。Floor：2027 底 unsupervised 車隊 >1,000 台且營運 ≥5 城；來源：Tesla 指引 FSD v15 late-2026/early-2027（techtimes 2026-06-10）","columns":{"時間軸":"2Y：v15 上線＋Dallas/Houston 規模化5Y：多城數萬台10Y：自駕網絡貢獻 EPS 主體","驗證指標 / 漂移觸發":"車隊台數（Robotaxi Tracker）、營運城市數。漂移：v15 延至 2027H2 或上線後 6 個月車隊"}},{"id":"H2｜汽車毛利觸底回升","text":"Auto GM（ex-credit）自 2025 的 17.9% 谷底回穩，Q1'26 已回到 19.2%；新平台（低價車、Cybertruck 效率）＋規模＋軟體吸附（FSD 訂閱）讓每車毛利止跌。Floor：FY2026 Auto GM ex-credit 全年 ≥18%；來源：Q1 2026 財報 electrek 2026-04-22","columns":{"時間軸":"2Y：GM 站穩 18-20%5Y：軟體佔比拉高毛利結構10Y：混合毛利 >25%","驗證指標 / 漂移觸發":"季度 Auto GM ex-credit、FSD 訂閱轉化率。漂移：連 2 季 Auto GM ex-credit"}},{"id":"H3｜能源第二曲線","text":"能源儲存（Megapack/Powerwall）維持高速成長，成為毛利與成長的穩定貢獻者，抵銷汽車週期性。Floor：能源部署年化 ≥40 GWh、營收 YoY >25%；來源：Q2 2026 部署 13.5 GWh（IR 2026-07-02）","columns":{"時間軸":"2Y：年化 50+ GWh5Y：能源毛利佔比 >20%10Y：獨立成長引擎","驗證指標 / 漂移觸發":"季度 GWh 部署、能源毛利率。漂移：能源部署 YoY 轉負連 2 季 → H3 削弱"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE 回落至 ~80x（約 $200）＋7/22 Q2 財報 Auto GM ex-credit ≥19% 且非折價驅動＋中國重回前 10 連 2 季；三者齊備才重啟完整 DD","irr_base_pct":-2.7,"ev5y_pct":-12.0,"drift_watch_prior":{"dca_verdict":"迴避","dca_role":"不持有/迴避","signal":"B","val":"🔴","ma":"🟡","trap":"🟡","moat_trend":"↓","runway_post_y5":"🟡","asym_ratio":0.7,"ev5y_pct":-12.0,"irr_base_pct":-2.7,"max_dd_pct":-65.0,"bull_5y_price":660.0,"bear_5y_price":91.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE 回落至 ~80x（約 $200）＋7/22 Q2 財報 Auto GM ex-credit ≥19% 且非折價驅動＋中國重回前 10 連 2 季；三者齊備才重啟完整 DD","price_at_dd":393.45,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSLA_20261024/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
