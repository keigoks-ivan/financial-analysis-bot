你是 stock-analyst **v20 判斷 agent**，標的 GRAB（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"GRAB","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_ifrs","label":"Revenue（IFRS）","value":1112,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Grab Q3 2026 IR 新聞稿（q4cdn）／SEC 6-K Ex.99.1"}},{"id":"f_kpi1_adjusted_ebitda_ifrs_gra","label":"Adjusted EBITDA（公司非 IFRS 口徑，Grab 不報 non-GAAP 營業利益）","value":237,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD m（利益率 21.3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Grab Q3 2026 IR 新聞稿；排除 SBC、折舊攤銷、併購成本、重組、法律和解準備"}},{"id":"f_kpi2_ifrs_operating_profit","label":"IFRS 營業利益（Operating profit）","value":108,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD m（利益率 9.7%，自算 108÷1112）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Grab Q3 2026 IR 新聞稿損益表"}},{"id":"f_kpi3_adjusted_free_cash_flow","label":"Adjusted Free Cash Flow（公司定義）","value":286,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Grab Q3 2026 IR 新聞稿；TTM 533。公司口徑含金融服務放款應收變動 +445、客戶存款 −184、處分資產 +4 等調整"}},{"id":"f_kpi6_fy2026","label":"管理層指引：FY2026 營收","value":"4,150–4,200","period":"Q3 2026 公告（2026-11-03），本季上修","unit":"USD m（YoY +23%～+25%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026 公告（2026-11-03），本季上修","citation":"Grab Q3 2026 IR 新聞稿 Business Outlook"},"note":"對照 dd_numbers_extra.py capital_structure：FY1 營收共識均值 4,211.6（18 位分析師，查詢日 2026-11-08），指引上緣略低於共識均值"},{"id":"f_kpi7_fy2026_adjusted_ebitda","label":"管理層指引：FY2026 Adjusted EBITDA","value":"790–800","period":"Q3 2026 公告（2026-11-03），本季上修","unit":"USD m（YoY +58%～+60%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026 公告（2026-11-03），本季上修","citation":"Grab Q3 2026 IR 新聞稿 Business Outlook；Q4 費用另有 60 百萬美元違約金（台灣公平會否決 foodpanda Taiwan 收購），計入 IFRS 但不計入 Adjusted EBITDA，不影響指引"}},{"id":"f_kpi8_mtu","label":"MTU（月活交易用戶）","value":57.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Grab Q3 2026 IR 新聞稿"}},{"id":"f_kpi9_on_demand_gmv","label":"On-Demand GMV","value":6.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD bn（YoY +18%，固定匯率 +22%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Grab Q3 2026 IR 新聞稿；外送 GMV 4,500（+21%），出行 GMV 2,335（+14%）"}},{"id":"f_kpi10","label":"金融服務（放款與營收）","value":201,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD m 營收（YoY +124%）；當季放款發放 1.9bn（+115%）；放款組合 2,711（YoY +200%，不含 Superbank +115%）；90 天以上逾期 2.6%；首次轉正 Adjusted EBITDA 12","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Grab Q3 2026 IR 新聞稿"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-02","period":"2026-11-02","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-02"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_grab_gross_margin_pct","label":"GRAB 毛利率","value":44.45,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GRAB.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_grab_operating_margin_pct","label":"GRAB 營業利益率","value":10.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GRAB.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_grab_fcf_margin_pct","label":"GRAB FCF 利潤率","value":-0.45,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GRAB.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_se_gross_margin_pct","label":"SE 毛利率","value":44.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SE.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_se_operating_margin_pct","label":"SE 營業利益率","value":8.24,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SE.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_se_fcf_margin_pct","label":"SE FCF 利潤率","value":16.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SE.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_uber_gross_margin_pct","label":"UBER 毛利率","value":43.21,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UBER.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_uber_operating_margin_pct","label":"UBER 營業利益率","value":12.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UBER.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_uber_fcf_margin_pct","label":"UBER FCF 利潤率","value":18.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UBER.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_dash_gross_margin_pct","label":"DASH 毛利率","value":51.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DASH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_dash_operating_margin_pct","label":"DASH 營業利益率","value":5.55,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DASH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_dash_fcf_margin_pct","label":"DASH FCF 利潤率","value":12.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DASH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_meli_gross_margin_pct","label":"MELI 毛利率","value":42.02,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MELI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_meli_operating_margin_pct","label":"MELI 營業利益率","value":7.42,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MELI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_meli_fcf_margin_pct","label":"MELI FCF 利潤率","value":31.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MELI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_ocf_fcf_ocf","label":"營業現金流（OCF）與簡單 FCF（OCF−資本支出＋處分收入）","value":-12,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD m（OCF 55；資本支出 71；處分收入 4；簡單 FCF＝55−71＋4，自算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Grab Q3 2026 IR 新聞稿 Adjusted FCF 調節表；簡單 FCF 為本報告自算，非公司口徑"}},{"id":"f_kpi5_sbc","label":"SBC（股權報酬費用）","value":49,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","unit":"USD m（占營業利益 45%、占營收 4.4%，皆自算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-03）","citation":"Grab Q3 2026 IR 新聞稿 Adjusted EBITDA 調節表"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":3.41,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-8.33,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":66.31,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（0.14 → 0.14）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（0.14 → 0.14）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（0.21 → 0.21）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":0.14,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":0.14,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":0.21,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":7.69,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 0.13 → 0.14（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":34.1,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"1 個年度端點內的分位＝50.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":50.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.47,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.5,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":24.36,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 0.14，分子＝快照價 3.41","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-3827.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 2070.0、現金 5897.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":4037.0,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":9939.17,"period":"2026-11-08","unit":"USD m","basis":"市值 13766.17 ＋ 淨負債 -3827.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":4211.6,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":5246.56,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（18 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.36,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 3.41 / W52 3.87 / W104 4.44 / W250 3.79 / W250 13週斜率 -1.43%"},{"id":"f_ma_w52","label":"52 週均線","value":3.87,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":4.44,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":3.79,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-1.43,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"20-F 列出各板塊競爭者：外送有 Foodpanda、ShopeeFood、Gojek（主要印尼）、Line Man Wongnai；叫車有 Gojek、Be、Bolt、Tada、Ryde、Xanh SM、Maxim、InDrive 等；支付有 ShopeePay、Google Pay、Dana、GoPay 等。","source":"SEC EDGAR 20-F FY2025 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"In our deliveries segment, we face competition from regional players such as Foodpanda, ShopeeFood and Gojek (primarily in Indonesia) and single market players in Southeast Asia, including Line Man Wongnai in Thailand.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"20-F 指出競爭者包含新進入者，且法規變動可能便利本地與外國競爭者進入。","source":"SEC EDGAR 20-F FY2025 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"These competitors may be well-established or new entrants and focused on providing low-cost alternatives or higher quality offerings, or any combination thereof.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"新加坡 CCS 初步認定 Grab 收購 Trans-cab 會強化其叫車市場支配地位，Grab 於 2024 年 7 月終止收購。","source":"SEC EDGAR 20-F FY2025 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"in July 2024, following a provisional decision by the CCS that our proposed acquisition of Trans-cab Holdings Ltd was likely to entrench and strengthen our dominant position in the ride-hailing market, and result in a substantial lessening of competition in the ride-hailing market, we terminated the acquisition and withdrew our application for merger approval.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["moat_trend","triggers"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Xanh SM 為越南唯一主要替代者，GoTo 2024 年起退出越南；報導 Grab 與 GoTo 洽談約 70 億美元併購。","source":"Tuoi Tre News","url":"https://news.tuoitre.vn/vietnam-might-be-last-trench-against-grabs-regional-dominance-103250814152412042.htm","excerpt":"While GoTo once operated in Vietnam under the GoViet brand, it exited the market in 2024, leaving Xanh SM as the sole major alternative to Grab. Now, that already-fragile market balance faces a serious threat. Grab is reportedly in advanced discussions to acquire GoTo in a transaction valued at approximately US$7 billion, in what could become one of Southeast","as_of":"2025-08-15","retrieved_at":"20261108","affects":["moat_trend","triggers"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Grab FY2025 20-F: 貿易應收款主要來自 Deliveries 與 Mobility 的商家、司機夥伴等，無重大客戶信用集中度。","source":"SEC EDGAR 20-F FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"There is no significant concentration of customer credit risk. In monitoring customer credit risk, customers are grouped according to their credit characteristics which includes geographic location and operating segment.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Moody's 將 Grab CFR 由 Ba3 升至 Ba2，展望穩定。","source":"TechNode Global","url":"https://technode.global/2026/04/27/moodys-upgrades-grabs-cfr-to-ba2-with-stable-outlook/","excerpt":null,"as_of":"2026-04-27","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Grab Q3 2026 營收年增27%、月交易用戶創高5700萬；全年2026營收指引上調至41.5–42.0億美元、調整後EBITDA 7.9–8.0億美元；管理層稱東南亞滲透率仍低。2027無公司指引。","source":"Grab Holdings Form 6-K Q3 2026 earnings press release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001855612/000185561226000148/a2026q3-earningspressrelea.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"S&P 將 Grab 升至BB、展望正面，預期未來12–18個月維持行動出行與外送主導地位，2026–2027 on-demand 抽成率維持13–15%（2025為13.6%）。","source":"S&P rating action as cited in search summary of Grab 2026 results/coverage","url":"https://www.sec.gov/Archives/edgar/data/0001855612/000185561226000148/a2026q3-earningspressrelea.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Q1 2026 誘因占 On-Demand GMV 10.5%，Q1 與 Q3 管理層提及燃油價格波動、印尼法規變動與總體逆風。","source":"Grab Q1 2026 earnings summary (Quartr) / Q3 6-K","url":"https://quartr.com/events/grab-holdings-limited-grab-q1-2026_ofH5oDwn","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Grab 2026-03 報導稱目前未推進與 GoTo 合併；印尼反壟斷機構對市場集中度表達關注。Euromonitor估合併後東南亞叫車GMV占85%。","source":"Stocktwits news, Grab cools off merger talks with GoTo","url":"https://stocktwits.com/news-articles/markets/equity/southeast-asia-ride-hailing-giant-grab-cools-off-talks-with-go-to/chlEQZZRby4","excerpt":null,"as_of":"2026-03-05","retrieved_at":"20261108","affects":["moat_trend","triggers"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"印尼競爭監理機關 KPPU 於 2024、2025 年調查 Grab 與司機夥伴的合作安排（GrabExpress／GrabFood 及特殊租賃運輸），並另就印尼 P2P 借貸協會利率的卡特爾指控啟動程序（Grab 子公司為會員），程序仍在進行。","source":"SEC EDGAR 20-F FY2025 Item 8 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"In 2024 and 2025, KPPU investigated our partnership arrangements with driver-partners for (i) GrabExpress and GrabFood delivery and (ii) special rental transportation with other ride-hailing applicators. In addition, KPPU has initiated proceedings regarding a cartel allegation involving the determination of P2P interest rates by the Indonesian Fintech Peer-to-Peer Funding Association,of which our relevant subsidiary is a member. The proceedings are still ongoing.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"20-F 風險因子指出東南亞反壟斷機關對大型科技公司濫用市場地位、反競爭協議與併購的關注升高，Grab 受競爭主管機關嚴密審視，可能面臨罰款或交易受阻；亦列出零工經濟、數位平台、AI 等法規風險。","source":"SEC EDGAR 20-F FY2025 Item 3.D Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"Competition authorities closely scrutinize us. Antitrust regulators in Southeast Asia and elsewhere are taking a greater interest in potential abuses of market power, anti-competitive agreements, and transactions that lead to substantial lessening of competition or entrenching or strengthening a dominant position, involving big technology companies.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"印尼反壟斷法下罰款最高可達相關市場該違規期間淨利的 50%（其他轄區最高約營業額 10%）。","source":"SEC EDGAR 20-F FY2025 Item 4 Antitrust and Competition Laws","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"In many jurisdictions, these penalties can reach up to 10% of total domestic or worldwide turnovers, and in the case of Indonesia, it can reach up to 50% of the net profit in the relevant market for the non-compliant period.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"KPPU 表示未收到 Grab、GoTo 合併的正式資訊，將持續監控；2025 年 5 月已就潛在合併啟動初步調查。","source":"Indonesia Business Post: KPPU warns of law violation in potential Grab-GoTo merger","url":"https://indonesiabusinesspost.com/4353/policy/kppu-warns-of-law-violation-in-potential-grab-goto-merger","excerpt":"KPPU warns of law violation in potential Grab-GoTo merger Published on 22/05/2025 GMT+7 Reading time 2 minutes Author: Gusty Da Costa Editor: Imanuddin Razak","as_of":"2025-05-22","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"regulatory_antitrust#4","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"馬來西亞零工工作者法 2026 年 3 月底前施行，設仲裁庭與三方諮詢理事會；2026-10 預算案政府與 Grab 共同出資 RM160 百萬零工福利方案。","source":"Business Today: Budget 2027 Government, Grab To Fund RM160 Million Gig Worker Package","url":"https://www.businesstoday.com.my/2026/10/09/budget-2027-government-grab-to-fund-rm160-million-gig-worker-package/","excerpt":null,"as_of":"2026-10-09","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"20-F 列出在東南亞營運的風險包含新增或更繁重的法規、稅負或關稅；另揭露受緬甸相關制裁（含敏感品項出口／再出口限制），緬甸營運占營收不到 1%。","source":"SEC EDGAR 20-F FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"While our operations in Myanmar represent less than one percent of our revenue, our future prospects there could be adversely affected, potentially necessitating a market exit involving significant costs and the loss of our investment.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"20-F 風險因子列「new or more burdensome regulations, taxes, or tariffs」為東南亞營運風險之一。","source":"SEC EDGAR 20-F FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"•new or more burdensome regulations, taxes, or tariffs;","as_of":"2026-03-06","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 20-F：幾乎全部營收與資產在東南亞；提示區域政治波動與地緣不確定性外溢風險","source":"Grab Holdings Form 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"Corporate Structure and Doing Business in Southeast Asia •In certain jurisdictions, we are subject to restrictions on foreign ownership. •We are subject to risks associated with operating in the rapidly evolving Southeast Asia. •Our businesses may be materially and adversely affected by any changes or negative developments in the economic and political environments in any regions of Southeast","as_of":"2026-03-31","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2024 20-F：曾因雲端供應商技術故障或中斷而遺失訂單或交易，平台可靠度隨擴張更難確保","source":"Grab Holdings Form 20-F FY2024","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561225000013/ck0001855612-20241231.htm","excerpt":"Third-party cloud infrastructure services providers and SaaS providers are vulnerable to damage or interruptions from factors beyond our or their control, including but not limited to computer viruses and other malicious code, denial-of-service attacks, cyber","as_of":"2025-03-31","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026：Deliveries 營收 +21% 至 $561M（GMV $4.5B +21%）；Mobility 營收 +10% 至 $349M（GMV +14%）；Financial Services 營收 +124% 至 $201M，segment adj. EBITDA 首度轉正；集團營收 $1,112M +27%。","source":"Grab Q3 2026 earnings 6-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001855612/000185561226000150/a2026q3-earningspressrelea.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Grab 於 Q3 2026 將 2026 營收指引上調至 $4.15–4.20B、EBITDA $790–800M；月交易用戶 57M；管理層提到燃油成本與通膨壓力；結果中未見 2027 展望。","source":"Reuters syndicated via NST: Singapore's Grab lifts 2026 forecasts","url":"https://www.nst.com.my/amp/business/corporate/2026/11/1569533/singapores-grab-lifts-2026-forecasts-strong-ride-hailing","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"市占／定價：搜尋僅見 2025 年 Euromonitor 估計 Grab+GoTo 合計印尼逾 91%、區域叫車 GMV 約 85%；分析稱與 GoTo 在印尼打補貼價格戰、定價權有限；Grab 近期據報未積極推動合併。無 2026 實際市占與價格數據。","source":"Euromonitor: three key implications of the Grab and GoTo merger","url":"https://www.euromonitor.com/article/three-key-implications-of-the-grab-and-goto-merger","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"20-F 風險因素：Grab 自述競爭者含新進者與提供低價替代品者；數位支付與 ShopeePay、Google Pay、Dana、GoPay 等競爭，數位銀行主要對手為新興數位銀行。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"These competitors may be well-established or new entrants and focused on providing low-cost alternatives or higher quality offerings, or any combination thereof.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"20-F 風險因素：AI 採用加深使第三方侵權主張風險上升，可能被迫停用某些技術。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"As our business grows, competition increases and adoption of AI deepens, we face a higher risk of receiving notices claiming we have infringed upon third-party rights","as_of":"2026-03-06","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"DBS 研究報告：Grab 認為東南亞 AV 採用將緩慢、分階段，新加坡有 11 輛 AV，近期為人車混合車隊。","source":"DBS Group Research, Grab Holdings Ltd (2026-03-12)","url":"https://www.dbs.com/insightsdirect/api/s3/dbs-buffer/article_attachment/20260312/07-57-09_20260312%20Grab%20Holdings%20Ltd.pdf","excerpt":"from agentic AI, citing its strong driver and merchant supply network, and control over platform APIs and sees AI as an efficiency driver. Fintech breakeven is targeted for 2H26, with long-term EBITDA margins potentially reaching 30–40%, supported by lending scale and operating leverage. Autonomous vehicle deployment in early-stage, with 11 AVs in Singapore.","as_of":"2026-03-12","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Grab Q2 2026 財報說明稿：GrabUnlimited 訂閱制擴至五國，訂閱者占外送 GMV 約 35%，訂閱者成長 20% YoY；金融服務預期 2026 下半年達調整後 EBITDA 獲利","source":"Grab Q2 2026 Earnings Remarks","url":"https://s205.q4cdn.com/179588156/files/doc_financials/2026/q2/Grab-Q2-2026-Earnings-Remarks.pdf","excerpt":"loyalty program, GrabUnlimited. GrabUnlimited subscribers grew 20% YoY during the quarter, with these power users now contributing 35% of total Deliveries GMV.","as_of":"2026-08-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 財報（2026-11-03）公司將 FY2026 營收 guidance 上調至 $4.15–4.20B、Adjusted EBITDA 上調至 $790–800M；搜尋未見 2026 年下調。","source":"Grab Form 6-K Q3 2026 earnings press release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001855612/000185561226000148/a2026q3-earningspressrelea.htm","excerpt":"Full-year 2026 Group Revenue and Adjusted EBITDA guidance raised to $4.15 - $4.20 billion and $790 - $800 million, respectively.","as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026（8月）公司把 FY2026 guidance 上調至營收 $4.10–4.15B、Adj. EBITDA $720–740M；Q1（5/5）維持 $4.04–4.10B／$700–720M。","source":"Grab Form 6-K Q2 2026 earnings press release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001855612/000185561226000123/a2026q2-earningspressrelea.htm","excerpt":"We are raising our full-year 2026 guidance to $4.10 billion to $4.15 billion in Group revenue and $720 million to $740 million in Adjusted EBITDA","as_of":"2026-08-03","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"MarketBeat 10 月底：分析師共識評級 Buy、共識目標價 $6.01；同文股價約 $2.79，接近一年低點 $2.74（價格僅為來源字面，現價以 numbers.price_at_dd 為準）。","source":"MarketBeat, Upcoming: Grab expected to post earnings on Monday","url":"https://www.marketbeat.com/instant-alerts/upcoming-grab-grab-expected-to-post-earnings-on-monday-2026-10-26/","excerpt":"analysts maintain a consensus \"Buy\" rating and a $6.01 price target","as_of":"2026-10-26","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Investing.com 目標價分布：平均 5.82 美元、高 8 美元、低 4.6 美元（日期未標，as_of 為估計）。","source":"Investing.com Grab Holdings Ltd (GRAB)","url":"https://uk.investing.com/equities/grab-holdings","excerpt":"average 12-month price target for Grab Holdings is 5.820 USD, with a high estimate of 8 USD and a low estimate of 4.6 USD","as_of":"2026-10-31","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"個別券商 5 月調降目標價：Mizuho $7→$6（outperform）、JPMorgan 降至 $5.80（overweight）；StoneX 2026-09-16 維持 $7 買進。","source":"MarketBeat Mizuho/JPMorgan price target articles 2026-05-05","url":"https://www.marketbeat.com/instant-alerts/grab-nasdaqgrab-price-target-cut-to-600-by-analysts-at-mizuho-2026-05-05/","excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2022 年起的美國證券集體訴訟（In re Grab Holdings Limited Securities Litigation）已和解，20-F 載明 2024 年與 2022 年集體訴訟和解應計 8,000 萬美元，並於 2025 年結清；20-F 法律程序章節未列新的證券集體訴訟。","source":"SEC EDGAR 20-F FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"These amounts include $80 million related to a settlement in 2024 with regard to class action lawsuits filed against the Company and certain of its officers in 2022. The associated accrual was settled in 2025.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"20-F 列印尼 KPPU 對司機夥伴合作安排（GrabExpress、GrabFood、特殊租賃運輸）的調查，以及 P2P 利率卡特爾指控程序，仍在進行。","source":"SEC EDGAR 20-F FY2025 Item 8 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"In 2024 and 2025, KPPU investigated our partnership arrangements with driver-partners for (i) GrabExpress and GrabFood delivery and (ii) special rental transportation with other ride-hailing applicators. In addition, KPPU has initiated proceedings regarding a cartel allegation involving the determination of P2P interest rates by the Indonesian Fintech Peer-to-Peer Funding Association,of which our relevant subsidiary is a member. The proceedings are still ongoing.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"菲律賓競爭委員會因 Grab 與 Uber 在併購審查期間違反臨時措施，合計罰 1,600 萬披索，Grab 分攤 800 萬披索（2026-02-03 報導）。","source":"Carmudi Philippines：PCC Fines Grab, Uber PHP16 Million for Violating Order","url":"https://www.carmudi.com.ph/journal/pcc-fines-grab-uber-php16-million-violating-interim-measures-order/","excerpt":null,"as_of":"2026-02-03","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"Bloomberg 報導 Grab 推進收購 GoTo 並開始盡職調查；GoTo 回應稱尚無決定或協議。","source":"Stocktwits：Grab Stock Rises Premarket On Report Of Moving Ahead With GoTo Deal","url":"https://stocktwits.com/news-articles/markets/equity/grab-stock-rises-premarket-on-report-of-moving-ahead-with-goto-deal/ch7KI4qRbcN","excerpt":null,"as_of":"2026-03-10","retrieved_at":"20261108","affects":["valuation","thesis.R","triggers"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"Kontan 報導 Grab 收購 Foodpanda 台灣業務，並提到與 GoTo 合併疑問。","source":"Kontan：Grab akuisisi bisnis Foodpanda di Taiwan","url":"https://investasi.kontan.co.id/news/grab-akuisisi-bisnis-foodpanda-di-taiwan-akankah-merger-dengan-goto-terjadi","excerpt":"Grab Akuisisi Bisnis Foodpanda di Taiwan, Akankah Merger dengan GOTO Terjadi? Rabu, 15 April 2026 / 19:17 WIB INDEKS BERITA ILUSTRASI.","as_of":"2026-04-15","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"2022 年證券集體訴訟 8,000 萬美元和解，應計已於 2025 年結清；搜尋未見 2026 年新的 Grab 證券集體訴訟。","source":"SEC EDGAR 20-F FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"These amounts include $80 million related to a settlement in 2024 with regard to class action lawsuits filed against the Company and certain of its officers in 2022. The associated accrual was settled in 2025.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"印度班加羅爾法院的 IP 侵權訴訟（2021 年起）：2023-05-31 駁回，原告已提覆審請求，尚待裁定。","source":"SEC EDGAR 20-F FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm","excerpt":"The case was dismissed on May 31, 2023 but the plaintiffs have since filed a petition to review the dismissal and the petition is pending.","as_of":"2026-03-06","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"搜尋未見 Grab 產品召回；僅見菲律賓競爭委員會因違反併購審查臨時措施的罰款（Grab 800 萬披索）。","source":"Carmudi Philippines：PCC Fines Grab, Uber PHP16 Million for Violating Order","url":"https://www.carmudi.com.ph/journal/pcc-fines-grab-uber-php16-million-violating-interim-measures-order/","excerpt":null,"as_of":"2026-02-03","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"GRAB","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":44.45,"operating_margin_pct":10.95,"fcf_margin_pct":-0.45,"rd_intensity_pct":10.4},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GRAB","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"SE","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":44.34,"operating_margin_pct":8.24,"fcf_margin_pct":16.92,"rd_intensity_pct":4.24},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SE","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"UBER","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":43.21,"operating_margin_pct":12.44,"fcf_margin_pct":18.44,"rd_intensity_pct":7.35},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UBER","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"DASH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":51.91,"operating_margin_pct":5.55,"fcf_margin_pct":12.91,"rd_intensity_pct":10.85},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DASH","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"MELI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":42.02,"operating_margin_pct":7.42,"fcf_margin_pct":31.81,"rd_intensity_pct":7.16},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MELI","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"GRAB"},"financial_history":{"ticker":"GRAB","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":1433000000.0,"revenue_yoy_pct":null,"gross_margin_pct":5.37,"operating_margin_pct":-90.37,"net_income":-1683000000.0,"diluted_eps":-0.44,"free_cash_flow":-872000000.0,"fcf_margin_pct":-60.85,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":2359000000.0,"revenue_yoy_pct":64.62,"gross_margin_pct":36.46,"operating_margin_pct":-16.41,"net_income":-434000000.0,"diluted_eps":-0.11,"free_cash_flow":-6000000.0,"fcf_margin_pct":-0.25,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2797000000.0,"revenue_yoy_pct":18.57,"gross_margin_pct":41.97,"operating_margin_pct":-1.97,"net_income":-105000000.0,"diluted_eps":-0.03,"free_cash_flow":739000000.0,"fcf_margin_pct":26.42,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":3370000000.0,"revenue_yoy_pct":20.49,"gross_margin_pct":43.2,"operating_margin_pct":6.59,"net_income":268000000.0,"diluted_eps":0.06,"free_cash_flow":-44000000.0,"fcf_margin_pct":-1.31,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2026_Earnings_Call_20261103.md）

# Q3 2026 Earnings Call
**Grab Holdings Limited** | Earnings Calls | 2026-11-03

**Douglas Eu** (Executives):
Good day, everyone, and welcome to Grab's Third Quarter 2026 Earnings Call. I'm Douglas Eu, Director of Strategic Finance and Investor Relations at Grab. And joining me today are Anthony Tan, Chief Executive Officer; Alex Hungate, President and Chief Operating Officer; and Peter Oey, Chief Financial Officer.
During this call, we will be making forward-looking statements regarding future events, including our business and financial performance. These statements are based on our current beliefs and expectations. Actual results could differ materially due to a number of risks and uncertainties as described in this earnings call and earnings release and in our Form 20-F and other filings with the SEC. We do not undertake any duty to update any forward-looking statements. We will also be discussing non-IFRS financial measures on this call, and these measures supplement but do not replace IFRS financial measures. Please refer to the earnings materials for a reconciliation of non-IFRS to IFRS financial measures. And for more information, please refer to our earnings release, remarks and supplemental presentation available on our IR website.
So for today's call, Anthony will deliver opening remarks, after which we will open the floor for questions. And as a reminder, we accept questions via our IR email at investor.relations@grab.com. So please do submit your questions ahead of time, and we'll add them to the Q&A queue.
And with that, I'll hand it over to Anthony.

**Ping Yeow Tan** (Executives):
Thanks so much, Doug. Good day, everyone, and thank you for joining us. The third quarter of 2026 was a quarter of several milestones. For the first time, all 3 of our core segments are profitable with Financial Services achieving segment adjusted EBITDA profitability, including the contributions from Stash and Superbank. Adjusted EBITDA reached a record $237 million, up 73% year-on-year, our 19th consecutive quarter of adjusted EBITDA expansion. On-demand GMV grew 22% on a constant currency basis and monthly transacting users reached a record 57 million. We have a clear line of sight to the fourth quarter. We are raising our full year guidance for both group revenue and adjusted EBITDA for the second time this year. We also reiterate our 2028 expectations of our group revenue compounded annual growth rate of over 30% and adjusted EBITDA of $1.7 billion. These expectations include the proposed acquisition of Atome, which remains subject to completion.
Now, we delivered this in a challenging environment. Elevated fuel prices continued to pressure driver operating costs, persistent inflation generated tightened household spending and Indonesia's new 2-wheeler commission framework took effect in July. We leveraged our ecosystem advantages to grow revenue while expanding profitability and our Mobility and Deliveries margins both expanded quarter-on-quarter to 8.9% and 2.7%, respectively. This is what we mean when we say our ecosystem compounds with more users, more services per user and more of each dollar reaching the bottom line. That strength is also what allows us to stand with our driver partners. We know elevated fuel costs have weighed directly on their take-home earnings, and we continue to support them through this period.
Beyond immediate relief, we are also equipping partners with tools that help them earn more on every hour they spend on Grab. AI now powers every layer of the Grab ecosystem, and we are building AI-First with Heart to simplify experiences for our users and drive tangible earnings growth for our partners.
As AI agents become a new way for consumers to transact, every order they place still needs to be fulfilled on the ground through the drivers, merchants and logistics and licenses we have built for over more than a decade. With over 20 billion cumulative transactions on our platform, our models have a deep real-world understanding of how Southeast Asia moves, eats, shops and borrows. We're doing this while structurally lowering our compute cost with cost per AI interaction down 42% quarter-on-quarter as AI interactions grew 60%. In September, we also announced a partnership with OpenAI to equip 30,000 driver and merchant partners with practical AI skills over the next 2 years starting in Singapore and then Thailand and expanding to Indonesia and the Philippines later this year, followed by Malaysia and Vietnam in 2027.
Southeast Asia has been our home for nearly 15 years, and our conviction in the region has never been stronger. It's one of the world's fastest-growing economies and is projected to expand well above the global average in 2026, according to the latest IMF forecast. With all 3 core segments now profitable and our outlook raised for the second time this year, Grab has more engines contributing to profit than at any point in our history. I share that conviction personally, and I have purchased additional shares in Grab. 
Our mission to drive Southeast Asia forward by empowering millions across the region remains central to our strategy and every capability we build serves our triple bottom line of delivering long-term shareholder value, creating meaningful impact for the communities and partners in our ecosystem and operating responsibly across Southeast Asia.
Thank you so much, and let's open it up for questions.

**Douglas Eu** (Executives):
Great. Thank you, Anthony. [Operator Instructions]. So we received some questions coming in. So the first question is on guidance upgrade, and this is a question for Peter, and the question comes from several analysts, Ranjan of JPMorgan, Piyush at HSBC, Jiong at Barclays and Wei from Mizuho. So the question is, pleased to see the guidance upgrade, but why not raise the 2026 EBITDA guidance higher as the current guidance indicates that the fourth quarter EBITDA may be stable relative to the third quarter? Question then goes on to ask, what are you assuming for fuel support FX and the festive season investments for the fourth quarter? So it's a question for Peter.

**Peter Oey** (Executives):
Yes, sure. It's a great question to open up. Look, when you look at our guidance revision today, so what are we? We're at $790 million to $800 million. And this is from our previous range just to reset from $720 million to $740 million. So that's roughly about a 58% to a 16% year-over-year expansion on our EBITDA. Now in context, we are now operating at the highest margins level in Grab's history. If you look at the year-over-year, it was a 560 basis points improvement in terms of EBITDA margin that we are continuing to demonstrate as our business continues to perform.
Now the progression from Q3 to Q4, which is at the heart of the questions, there are a couple of deliberate strategic choices that we as a management team going into Q4, feel that it's really important. Now if you look at the fourth quarter, so fourth quarter is a high-return investment window. It's one of our busiest seasons for Southeast Asia itself. It's the festive season and a very high-volume tourist travel also at the same time. And we saw some snippets of that in October with a lot of the events and also coming up also in December itself.
Now Anthony just spoke about driver supply and some of the challenges that we've got here also. The elevated fuel prices has continued. We saw it in the second quarter. We saw it in the third quarter, and we're expecting the same in the fourth quarter. Now we need more drivers on the platform. Actually, if you look at the third quarter, our active driver base was the highest ever on the Grab ecosystem itself. We increased the driver base by 20% on a year-over-year basis, and we need more drivers out there. So securing driver partner capacity is really critical as for us going to the Q4. So we're leaning in, in Q4 to make sure our driver community continues to be strong and also to help our passengers also to have access to rides reliably as well as affordable at the same time.
Now we're also deliberately deploying targeted marketplace investments across the board, both on the driver side also and also having -- making sure they have access to vehicles at the same time. Because if we fail to have drivers on the platform, it will just be leading to higher prices, high consumer waiting time, which is not a great customer experience. So that's one part, which is really important how we think about Q4, especially around the mobility.
Now the second part, going into this very busy season is also supporting the high-growth product launches. And if you read in the earnings remarks today, what did we launch? We launched GrabMall in the Q3, and we're also rolling out several digital banking initiatives, the GXS Credit Card in Singapore and also in Indonesia, we launched, in conjunction with our collaboration with Atome, OVO Pinjaman, which is a lending product for our consumers with Kredit Pintar. And these are very exciting both delivery products as well as financial services products. So we're allocating marketing and also leaning in to make sure these products continue to pick up the traction in Q4 and also as we get into 2027.
Now on the cost structure itself, we see that regional corporate costs to be fairly stable in the second half to the first half. So that is really the package of how we think about the Q4 itself. Now my guidance philosophy has always been to be on the prudent side and also be transparent with our shareholders, but also be grounded in what we're seeing on the ground. And we are seeing some of the challenges on our driver community that we talked about earlier. So we are setting expectations to ensure that we can reinvest with agility, but also capture the seasonal market share. We want to finish the fourth quarter strong and we're on track to do so, profitably at the same time, also deliver a great customer experience for our customers, while also for making sure our drivers and our merchants are also increasing their earnings at the same time.

**Douglas Eu** (Executives):
Thank you, Peter. So we received this next question set that came from several analysts. It's all pertaining to the Deliveries segment. So we've segmented it into 3 parts. The questions came from several analysts like Divya of Morgan Stanley, Alicia of Citi, Piyush of HSBC, Ranjan of JPMorgan and Thomas at Jefferies as well. There's a question pack for Alex. So the 3-part questions. First is on margins. Second is on ads. And then third is on clarification on GrabMall. So I'll read basically each of the 3 components. And the first component is on the Deliveries segment. Is the 2.7% EBITDA margin a new structural baseline? And what drove the outperformance and how much of this was enabled by AI-driven unit cost efficiencies? And should we expect a 2.7% segment margin to be a new base? 
The second part of your question is then on advertising. Can you update us on advertising penetration relative to Deliveries GMV and what outperformed in the quarter? And the third part is on clarification on GrabMall. Could you expand more on the GrabMall strategy? So this is a question pack for Alex.

**Alexander Charles Hungate** (Executives):
Well, thank you all. I guess this is the most popular question so far. So let me try and go in a bit detailed in those 3 parts. You're right, Deliveries margin performed very strongly, 2.7%, up from 2.1% in the prior year, so very strong in the quarter. That does reflect primarily the operating leverage that we're getting from the scale because Deliveries is growing fast, so 21% GMV growth year-on-year. As Peter said earlier, our control of the corporate costs, the regional corporate costs has been good, so pretty much flat in the second half versus the first half. And that gives us strong operating leverage enhanced by very widespread deployment of AI, both in terms of the productivity that we as Grabbers benefit from. But more importantly, if you think about our central purpose, it's driven by continued improvements in the performance of the marketplace that we run, increasingly using AI to do the optimization that we need to make sure we get the best combination of reliability of service and affordability for our users. So that is going very strongly.
The other driver of the improvement in margin is ads. Ads are growing strongly as our scale attracts more of the endemic advertisers who sell food on the platform and increasingly also brings in new FMCG advertisers who start to get attracted by that growing reach and are now very engaged also in partnering with us to grow GrabMart and GrabMall. So we've been able to do this at the same time as we increase driver incentives. As Peter mentioned, we're leaning in to help drivers during these difficult times. So you do see increased incentives, both for Mobility and for Deliveries for drivers. So the operating leverage is even bigger than the increase in incentives that we've given out to drivers. So that shows the strength and the overall reach that we're getting now with that scale.
So we still see plenty of opportunities to invest, though, in the Deliveries segment using product-driven growth, which has been a key factor in our success over the last couple of years. So we are expecting, as you remember from the last quarter, to invest in product growth in the GrabMall marketplace area. So something like $160 million we set aside in the 2028 adjusted EBITDA guidance to fund those investments. It's driving better affordability in groceries and driving further growth in both GrabMall and GrabMart. But in spite of these investments, we expect Deliveries margins to improve progressively year-by-year as we make progress towards our longer-term margin target of 4% plus, which you'll recall, we've been guiding towards over the last couple of years.
And then the last part of the strategy, I believe, was the GrabMall -- question was the GrabMall strategy. So let me talk about that. We launched GrabMall this quarter. It's a branded retail commerce channel within the Deliveries ecosystem. It's been inspired by the FMCG advertisers who have been working with us on advertising. They're now keen to partner to do closed loop endemic advertising where we actually fulfill the transaction as well. And because of our very strong last-mile quick commerce capabilities, we're able to do that probably better than any other partner in the region. So it's a good combination. We tap on our ecosystem advantage, and then we have that very large high-frequency user base and proven fulfillment network. And then we also know how to work well with merchants in terms of making sure that we tap into understanding their inventory so we can get a very good online fulfillment rates for customers as well.
The additional benefit here, once Atome is approved, of course, that we'll be able to then have better monetization capabilities via lending as well on this new base. So we'll get not just the advertising improvement in margin as we grow GrabMall and GrabMart, but we'll start to get stronger lending monetization as well with those highly developed Atome consumer lending models. So we'll continue to pilot GrabMall, which we just launched across select markets, and we are seeing good uplifts right away from these pilots, and we'll start to expand that across the region.

**Douglas Eu** (Executives):
Thank you, Alex. So next question is on AI and specifically on AI proof points. Question came from Alicia of Citi and John of Daiwa. Those are questions for Anthony. So Anthony, could you elaborate on how AI agents and Gen AI's features are currently driving user engagement and transaction velocity across the platform? Specifically, what early trends are you observing in terms of cross-sell, in-app time spent and basket size uplift? And additionally, on the supply side, how are merchant partners leveraging AI tools to drive demand, improve sell-through and how are drivers partners utilizing AI to optimize their earnings and manage the workload and rest cycle? So that is a question for Anthony.

**Ping Yeow Tan** (Executives):
Thanks so much, Alicia, and John. Let me take the AI proof points. So on engagement, I want to be straight about what we measure. We do not optimize for time spent in the app. For every AI feature, we ask whether people transact more often, more loyal, do they come back because that is what you can model. Three numbers from this quarter answer it, users who shop both GrabFood and GrabMart now account for 43% of food GMV and their baskets are about 10% larger. Groceries GMV is growing 1.8x faster than Food. GrabUnlimited subscribers transact almost 3x as often as nonsubscribers. AI sits behind each of those in search, in recommendations and offers we show, but we report the outcome rather than the model, and we will keep reporting the same metrics every quarter so you can track them.
On the supply side, the tools are now at scale. The driver AI assistant is with nearly 500,000 drivers. It shows them where demand will be before it peaks and drivers who actively use it, earn over 10% more per online hour. The same information helps them plan their day, their breaks because they no longer need to stay online just waiting for the next job. 
I want to be clear on how we see that. These are tools drivers choose to use, and they decide when and how long they want to drive. On the merchant side, merchants on our merchant AI assistant, MAI, earn about 20% more on average. Average merchant earnings grew 15% year-on-year and active advertisers grew 39%.
Look, I'll be honest, adoption still has a long way to go, and that's why we continue to lean in on AI as a core part of our company's DNA.

**Douglas Eu** (Executives):
All right. Thank you, Anthony. So continuing on to that thread, additional questions as well on OpenAI and Muse, which are our recent partnership collaborations. Questions as well coming from John of Daiwa and Wei of Mizuho. So once again, another question set for Anthony. So these are 2 separate questions on these partnerships as well and their broader AI benefits. So the first component is what tangible benefits do you expect the OpenAI partnership and your broader AI investments to deliver to Grab? And the second component is then on Muse. Grab was announced last week as an early connector partner for Meta Muse in Singapore across GrabMart and Grab Dine Out. Can you discuss the early use cases you're exploring? And where do you see AI agents becoming a meaningful incremental customer acquisition channel for Grab over time? So questions for Anthony.

**Ping Yeow Tan** (Executives):
Thanks, John and Wei. On OpenAI specifically, our OpenAI partnership delivers tangible benefits because we put the tools in our partners' hands and we teach them how to use them and how to make more money with them. The results are already measurable. As I shared just now on merchants using our AI assistant see about 20% uplift, drivers who use it earn over 10% more per online hour.
Now to scale, in September, we launched Go Forward with OpenAI under Grab Academy. Over the next 2 years, we will equip 30,000 drivers and merchant partners across Southeast Asia with very practical AI skills. I actually met many of them, and I saw how they're using even [indiscernible] to help them become even greater creators, social media creators to help them boost their income. We started in Singapore, launched in Thailand in October and are expanding to several other countries, including Indonesia and the Philippines this year-end. Partners who use AI sell more, earn more and stay longer and more loyal to our platform. That gives us stronger supply, as Peter talked about, and better service quality.
Now on Muse, Meta chose us as a launch partner when they brought Muse to Singapore last week. And we deliberately chose GrabMart and Dine Out. Groceries are habitual. People buy much the same basket every week, and that's exactly the kind of task an agent does very well. Dining out is the other everyday use case. Here's how it works. A user asks Muse in chat, Muse will build a basket from a GrabMart store and a basket shows up in the Grab app where the user approves the purchase. Our merchant, our inventory and the transaction data all stay with Grab. This is our pilot in one market, so it's too early to size the impact on customer acquisition or GMV. We see it first as incremental demand, just a new front door into Grab. 
We'll go partner by partner with platforms that bring real scale and utility and add services and markets when the time is right. Over time, I do expect agent-originated orders to become a growing channel, and we will share updates as the partnership progresses. What does not change is where the value sits: whichever front door an order comes through, the merchant network, real-time inventory, dispatch, payments and customer care all run on Grab. We will also keep improving our own AI experiences, so users have good reasons to come to us directly.

**Douglas Eu** (Executives):
Thank you, Anthony. So we received a few questions on Financial Services. So I think we'll take them as a different components. So the first component is on the Financial Services EBITDA breakdown for the third quarter. So this is a question for Peter coming from several analysts, including Piyush of HSBC and at Jacquelyn from CGS. So for Financial Services, Peter, can you give us a split of the EBITDA contributions from Superbank, Stash, GrabFin and the remaining business in the third quarter?

**Peter Oey** (Executives):
Yes. We don't split them out each of those components because the way we think about it, actually, Financial Services is one bucket of different components of the ecosystem working together. And hence, why we are very, very deliberate of not breaking it out, including the banks itself. And what is publicly available, obviously, we will disclose such as Superbank, which is a public company itself. 
So just stepping back here, just to remind everyone here, the EBITDA target that we are giving up for 2028 for Financial Services is $500 million. Financial Services today, third quarter, produced $12 million. So we still have some ways to go to get to $500 million. So where is it going to come from? What are the mix that we're going to see.
Now what we said was $300 million out of the $500 million will come, we believe, from Atome and Superbank, and we said that a few weeks ago. So the remaining $200 million come from all the other products, ecosystem of Financial Services, including the banks, the GXS GXB banks as well as our nonbank lending portfolio, which is coming from we call GrabFin.
Now we do expect that our banks over time, given that they are in a scaling mode to take up a larger share of the gross loan portfolio over time. And that will be a great leading indicator in terms of the profitability trajectory that we have. In addition to the Atome also once the acquisition is closed, given that their loan book also is growing at a very rapid pace at the same time. And in this quarter, actually, we gave out some additional disclosure on Financial Services regarding NPL as regarding also risk-adjusted returns, revenue-adjusted returns here to give the community a bit of a sense in terms of how we think about the unit economics of our lending portfolio to help you be able to model actually how we get to the $500 million.

**Douglas Eu** (Executives):
Thanks, Peter. So for the second component on the Financial Services question, this is more in terms of the building blocks to get to the $500 million. So the question comes from Alicia of Citi and Piyush of HSBC. So I'll turn the question now to Alex to explain this. So the question is, as you work towards the 2028 Financial Services targets of $500 million EBITDA and the above $6 billion loan book target, where do you believe you are today relative to that journey? What are the building blocks required over the next few years in terms of customer acquisition, lending penetration, product expansion, funding costs and credit performance that's required to get you there? And which assumptions do you believe is the most critical in achieving these targets? And wonder what scenarios could the business meaningfully outperform or fall short of your current ambitions?

**Alexander Charles Hungate** (Executives):
Thanks, Doug. Yes, we're very proud that it's the first profitable quarter for Financial Services. I think it was September 2022 when I stood up in front of you and said that we could break even by the end of this year. But here we are in the third quarter, and it's a strong contribution also $12 million of segment adjusted EBITDA, so up $40 million year-on-year. So we're at a very good trajectory in terms of the time at which we're breaking even. Then we have some, as you know, some significant advantages in terms of how we think about the strategy.
So just to summarize what those are for those of you who haven't been following our strategy closely on Financial Services. First of all, the acquisition costs are very low. We have daily interactions through the Superapp to 57 million monthly transacting users, and we have annual transacting users of far north of 100 million, so it's a very big significant reach. We have 647 million repayment touch points through which we can feed the AI-driven underwriting model. So that's a significant advantage, too. We can pre-collect many of the repayments from revenues which are flowing through the platform. And then on the funding side, the reason why we have the banks is that we expect them to be able to give us access to lower cost of funds over time. And so we have 2.7 billion of digital bank deposits already. And of course, we're building syndicated facilities that we can do in cooperation with Atome over time also, which will give us access to wholesale bank funding. So we're doing a lot more on funding than we were in the past where we were just relying upon the equity that we hold on the balance sheet.
So moving forward, as Peter was just saying, the banks continue to grow their share of the gross loan portfolio. It's a bank group which is structured with a lead regulator in Singapore. So international investors can feel confident of the compliance and the strength of that -- the strength of that structure for the banks. Gross loan portfolio growth, obviously, is outpacing cost structure significantly. We're coming through that breakeven point now. So this is where the operating leverage really kicks in and the returns from the Financial Services segment will start to accelerate from here. 
The proposed acquisition of Atome adds consumer lending on a massive scale. So most of our lending so far has been to drivers and merchants, but now with Atome coming in, these more mature consumer lending models like open loop BNPL, which would have taken us many years to develop and now available to us to distribute immediately and the network of 30,000 retail brands that they work with already also available to our platform, not just for Financial Services but also for advertising and partnering on e-commerce. 
So very well positioned for future growth. We're focused on the partners, as I said historically, but now this addition of this very large TAM for consumer lending comes into sight. That gives us confidence in line of sight of the $500 million EBITDA target for 2028. So Financial Services already becoming a major driver of our growth in EBITDA to that total group number of $1.7 billion in 2028. At that point, the loan book will be above $6 billion, including Atome, obviously, subject to completion. But that's still just a medium-term milestone. In my view, as we mentioned at the time that we announced Atome, the consumer TAM here is much, much larger. And so we could be 10x higher than we are in terms of consumer penetration than where we will end this year 2026 with our $3 billion loan book. So lots and lots of runway for us to grow this business and make significant contribution to Grab's future growth and future market cap.

**Douglas Eu** (Executives):
Thanks, Alex. So we move on to the next question, which is on Indonesia, a question also from several analysts, including Navin of UBS, Piyush of HSBC, Thomas at Jefferies and John from Daiwa. This is a question for Alex. In Indonesia, can you share if there's any update on potential regulatory intervention in the Deliveries segment? And what could be the likely impact of the regulations?

**Alexander Charles Hungate** (Executives):
Yes. As I mentioned in my remarks, the written remarks accompanying the release, we are very concerned about the plight of the drivers faced with the high fuel costs that we're seeing globally. And so we have been leaning in heavily to make sure that their income keeps pace. And in addition, we've been leaning in with additional driver incentives as well to support them during these difficult times. We are working closely with governments also. So in the case of Indonesia, the Indonesian ministries, including Komdigi, the Ministry of Transport, the Ministry of Manpower as the government evaluates the regulatory frameworks for on-demand logistics and food delivery.
I think our counterparts in the government truly appreciate that our platform and the other delivery platforms provide earning opportunities for those millions of everyday entrepreneurs in Indonesia. And so any regulation that is implemented must not damage those earning opportunities. So we have to proceed carefully and in partnership with government. So our understanding is these guidelines will focus on helping the driver earnings and fee transparency. And so we'll focus on that with them. We'll continue the constructive dialogue. We're not in a position to reveal any new details, but the details are starting to emerge. And as we hear about those, we'll let you know as soon as possible. But we don't expect any of the business implications of those new guidelines to materially impact our guidance outlook.

**Douglas Eu** (Executives):
Thanks, Alex. So next question is on capital allocation. Also a question from several analysts, including Divya at Morgan Stanley, Jiong at Barclays, Hussaini of Maybank, Sachin of Bank of America and Jacquelyn of CGS. This is a question for Peter. So Peter, following the rejection of the foodpanda Taiwan acquisition, are you exploring alternative acquisition opportunities? How would you weigh these against further share buybacks? And how much incremental -- in addition to that, with regard to the Financial Services segment, how much incremental corporate capital do you need to scale the loan book?

**Peter Oey** (Executives):
Yes. Look, we are disappointed with the outcome of foodpanda Taiwan acquisition, we were anticipating it. But at the same time, also, we respect the decision made by the TFTC in Taiwan. It also adds another $550 million of additional cash to the balance sheet. So from an M&A and capital allocation perspective, let me just frame it this way. When it comes to M&A discipline, we're very anchored on investing first in our core Mobility, Deliveries and Financial Services business. And you've seen that track record that we've been doing. We couldn't get there in terms of Taiwan, but hopefully, with Atome, which Alex spoke about is the next one that we feel very, very passionate about. It really opens up a great opportunity into our ecosystem. It is also a sizable acquisition that we're doing. At the same time also, we're working with the regulators just to make sure also that this one has the comfort that we want to get through by the time of next year. 
Now at the same time also, we have to invest on our organic business. And that's what we've been doing. You saw that in the Q3 results. We talked a little bit about the guidance for Q4 and how we think about the fiscal year also. Alex spoke about GrabMall and GrabMart, how we're investing that also at the same time. We are going to continue to lean in around affordability which is really important. When you see the MTU growing at 20% year-over-year basis, reaching 57 million MTUs. We added 3 million Southeast Asians into the platform itself shows that we have to continue to lean in, in giving access to Southeast Asians to use our products. And it has to be affordable and reliable and accessible at the same time. 
At the same time also, we have to lean in and invest organically on our partners' earnings. And Alex spoke about that, Anthony spoke about whether it's related to AI or whether it's related to fuel subsidies or whether it's related to the way they are able to earn also in working with our regulators, that is really critical. And we're not going to stop. We're going to continue to lean in to make sure our merchants and our drivers continue to earn more on the platform. 
We are also continuing to make sure that our products, when it comes to lending, is accessible to our public as well as to our partners at the same time. And Atome will unlock that at greater scale for us. And that's indeed a very perfect example where scale can multiply. Alex is so dead on. We're just scratching the surface with consumer credit. The TAM of consumer credit is 10x what Alex just spoke about, and we think it's more than that. So we are very, very eager and keen to actually unlock that box in consumer credit in a prudent way in Southeast Asia, and we'll continue to invest in that. 
Now we are also always looking at long term. Part of my capital allocation strategy in working with Anthony and Alex here is to think long term for the business. And we're continuing to see where can the business continue to grow and evolve over the next 5 to 10 years. And we have been making those bets. You see them in autonomous vehicles, for example. We're increasing cars in Singapore in anticipation of the introduction of a widely more usage of autonomous vehicles. We're adding another 40 cars of autonomous vehicles. We're making those investments. We're making investments in robotics also at the same time. We're making investments in AI also at the same time. So those are more longer-term bets that we will use our balance sheet to make sure that those long-term bets are also important, but also prudent at the same time.
Now excess capital will always be there, and we know that. And all of you are watching the balance sheet all the time. So we are very focused on shareholders' value. So what do we do? September, October, we accelerated the share buyback, and we repurchased $400 million in those last 2 months. I'm committed, so is Anthony and Alex, to make sure that we complete the remaining $500 million of our $900 million program over the next 12 months. If we can do it earlier, we'll do it earlier, but we intend to make sure that, that $900 million gets done by September of next year, and we intend to cancel all those repurchase shares also as part of that program. 
We do generate cash in the business. You see it in the numbers, $553 million. We almost doubled the free cash flow, and we will continue to use that cash to good use. I can assure you to our shareholders that I am very conscious that the balance sheet that we have is a privilege. We will make sure also that our shareholders' return when it comes to the balance sheet itself, and we will make sure that balance sheet also continues to be very healthy in a net cash position.

**Douglas Eu** (Executives):
Thank you, Peter. So the next question is from Venu of Bernstein, and this is a question for Anthony. So question here is, would Grab be willing to partner with global firms such as Uber to minimize long-term risk?

**Ping Yeow Tan** (Executives):
Thanks, Venu. Let me say what I take the longer-term risk to be, so I answer the right question. The risks that matter globally over the next 10, 20 years are technology shifts. So we talked about AI agents, AI agents changing how people transact, autonomous vehicles changing how people get around. Our answer to both is the same. We partner with the best in the world. We bring their technology, we localize it in Southeast Asia on our platform. 
Now on Uber specifically, you called out, Uber has been a shareholder since 2018 and Dara and I speak regularly. Today, an Uber user traveling in Southeast Asia can book a Grab ride inside the Uber app and a Grab user traveling into the U.S. can book Uber inside ours. That works for travelers and brings demand to both platforms. We take the same approach with others. In AI, as I shared earlier, we work with OpenAI across the region and Meta's Muse in Singapore. 
In autonomous vehicles, we have invested in WeRide and Momenta to bring robotaxis to the region and A-I-R, AIR, our public autonomous ride service in Punggol, Singapore, is already carrying passengers with commercial service on the Grab app to come. So we have partnered for years, and we will continue to do so. What we bring with each of these partnerships is our on the ground network, the biggest driver army, merchants, maps, licenses across 900-plus cities across Southeast Asia. We are all in on Southeast Asia, and I'm convinced that this region will continue to grow strongly in the years to come with Grab as its key enabler. And that is why we see today global companies come to us when they want to reach the real Southeast Asia across the region and it's why new technology here continues to arrive on Grab.

**Douglas Eu** (Executives):
Thank you, Anthony. So the next question is on autonomous vehicle strategy. This question is from Divya of Morgan Stanley and Venu of Bernstein. This is a question for Alex. So can you share your latest thoughts on what does the eventual autonomous vehicle business model look like between Grab, the fleet owner and AV technology provider? Could AVs ultimately disintermediate Grab? Or do you think Grab's demand aggregation, payments and fleet orchestration mean AV operators will still need Grab as a distribution layer? It's a question for Alex.

**Alexander Charles Hungate** (Executives):
Thanks, Divya. Yes, you started to -- even in the question, you started to kind of outline how we feel about this. So first of all, AVs are still in the early stages in Singapore. So we've already clocked over 100,000 kilometers in local trials, and we have plans to expand our fleet here in Singapore by fivefold. Currently, we're growing it to 50 vehicles, and we're preparing to launch the commercial autonomous ride hailing on the Grab app in the coming months. 
So the steady state model divides into basically 3 specialized layers. There's the AV OEM, the technology provider, and they develop and license the autonomous driving stack with the remote guidance software that's necessary to make that run. Then there's a fleet owner or financier. They fund the capital expenditure. They take the capital -- they take the depreciation through their P&L and balance sheet. And then they manage the depot charging, the cleaning, the maintenance. And then there's the orchestrator. So that's primarily Grab, platform orchestrator, demand aggregator. In some cases, Grab can also get involved in depot management where necessary to get things running.
Now the -- our track record in Southeast Asia has been to develop relationships with those fleet owners and fleet operators, okay? So we can continue that model. So we ourselves remain primarily asset-light under that model. But the fleet operators who in -- who currently are using conventional vehicles, so not AV, but the standard driver-driven vehicles. We will work with them to transition into this new world. In some cases, with our banks, we can help them with financing as well. And so we can add capacity as demand grows. 
So although at the start, where AV is currently a very young technology, and we are developing the capabilities to understand how they interact with the ride-hail platform, what kind of depot management and fleet management capabilities are needed as we scale to massive asset deployment, hundreds of billions or maybe trillions of dollars of AV asset deployment in the long run. Then we will combine a ride-hailing technology with its new hands-on AV experience. And then we'll be able to optimize the integration with the OEM to get the optimum integration of demand and fleet management, working with regulators, those technology partners and the communities on the ground as we always have. 
Now let's focus specifically on Southeast Asia because AVs cannot handle Southeast Asia transportation alone at the moment with a lot of weather, huge extreme tropical monsoons, et cetera. So there are lots of operational edge cases where the technology is still developing. And then more -- probably more significantly, even once the technology can overcome those, the cost displacement curve for human drivers in Southeast Asia is going to be many, many years. So it's not like North America where the driver cost per hour is much higher than it is here. In most of our markets, it's going to be a very long transition, probably a decade, something like that, where there's drivers and AVs working side by side. And that's obviously where the platform orchestration is critical. 
So we'll have a hybrid dispatch orchestration, load balancing between AVs, human drivers, some passengers will need assistance. So they'll have preferences for human drivers. Other passengers might have preferences for AVs, but that's all going to be orchestrated through the app. And those passengers, of course, are not just using mobility. In the Grab app, the Superapp, they're using all our other services as well. And you can see from our numbers that the intensity of cross-sell between food, Mobility, Financial Services and now GrabMart and GrabMall as well is very intense. So the customer relationship is very much intact with Grab. So we're confident that our goal of scaling AVs with fleet partners across Southeast Asia in the coming years in this asset-light model in complement with the human driver fleet is something where -- which will just enhance the position of our platform as the orchestration layer across all of those partnerships.

**Douglas Eu** (Executives):
Thanks, Alex. So we have time for 1 last question. So the final question is on GrabUnlimited, and this is a question from Wei of Mizuho. A question for Alex. Subscribers are now over 20% of Deliveries MTUs, but they generate 35% of Deliveries GMV and to transact nearly 3x as frequently as nonsubscribers. So this scale is a larger economic benefit coming from higher order frequency, lower acquisition and retention costs? Or is it greater cross-sell into Mobility and Financial Services?

**Alexander Charles Hungate** (Executives):
Yes. Thanks, Wei. You're right to highlight GrabUnlimited. It's a critical relationship-building tool for us, which drives primarily frequency and retention. So GrabUnlimited users transact over 3x more than nonusers and have significantly higher retention rate. So that's the key benefit from the program. They also allow us to reduce promotions. So consumer incentives outside of GrabUnlimited can come down from where they were before GrabUnlimited had such high penetration, and that also helps to fund the program. 
The benefits today concentrate primarily in Deliveries, but we've begun to extend it to Mobility benefits in those markets, in particular, where we've got very healthy supply situations. And that is working very well and has improved our cross-sell and retention on the Mobility side as well. And then merchants are very interested in this universe of GU users. They know that those are the ones with the high spend and the high frequency. So they're very important customers for our merchants to have access. So a lot of spend on the platform is from merchant-funded promotions. And you can see that, that's gone up 48% year-on-year and a meaningful portion of that increase is driven by merchants wanting to reach the GrabUnlimited user base with their exclusive offers. 
So a great time to join GrabUnlimited with all those exclusive offers, but also a very attractive magnet for merchants to drive their success as well. So you should expect us to continue to expand GrabUnlimited for Deliveries, continue to drive penetration into the other verticals. And you can also expect us to use GrabUnlimited to extend benefits beyond the ecosystem. We are leveraging, for example, there's a partnership with OpenAI to offer free ChatGPT Plus and Trip.com booking discounts. So that's going to be an avenue that you see more and more of also. So we can bring new benefits for our loyal GrabUnlimited customers.

**Douglas Eu** (Executives):
Thanks very much, everyone. So that brings us to the end of our Q&A session. I will now turn the time over to Peter for the closing remarks.

**Peter Oey** (Executives):
Thanks, Doug. Look, before we wrap up, I just want to take a moment to acknowledge what this year, the last 9 months, has delivered. Adjusted EBITDA reached new record levels in every quarter. Our Financial Services business crossed into profitability, and we have nearly doubled the trailing 12 months adjusted free cash flow. That reflects the durability of the Grab platform itself.
Now in addition also, we back that with capital. So we've repurchased $400 million of shares in September and October, and we reflected it in our guidance, raising both revenue and also adjusted EBITDA for the full year for the second time this year. As I always remind the Grab team, this is not a one-quarter story. It's the trajectory where it counts. These milestones would not be possible without the trust of everyone who relies on Grab. Our drivers and our merchant partners, thank you. It's what has been a rough quarter for a lot of you, given the weather as well as the fuel prices. 
So thank you for our merchant partners also for the restaurants. Thank you for supporting us. And to the millions of consumers who use the Grab services every day. Thank you for trusting Grab. Thank you for opening up the app, ordering a ride, ordering a book, ordering a restaurant for delivery, or a Mart, or a Mart. Thank you for doing that. And also to all our Grabbers who worked tirelessly in the third quarter and all through this year. Thank you very much.
So, Anthony, Alex and I also want to thank our shareholders also for your continued support. As usual, the IR team will be on the road over the next few weeks, so do reach out. We will be in a few countries, including Singapore also, so feel free to reach out. We'd love to have a dialogue with you or even sit down and have a coffee with you. Thanks, everyone, for joining us today and see you in the next quarter.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GRAB_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜CEO｜guidance：CEO 表示因上半年表現加上 Superbank 合併與 Stash 收購，上調 2026 全年財測（原話："we are raising our full year 2026 guidance,"）
- 2026-08-04｜President and COO｜guidance：COO 說明財測上調區間為由 7 億至 7.2 億美元，並計入司機燃油補貼（原話："$700 million to $720 million does reflect the factors in"）
- 2026-08-04｜President and COO｜guidance：COO 表示新財測含 2% 至 3% 的匯率逆風（原話："includes the FX headwinds of between 2% to"）
- 2026-08-04｜President and COO｜guidance：COO 表示核心業務表現符合先前財測，新增部分來自 Superbank 與 Stash 合併及匯率（原話："the core business is performing well"）
- 2026-08-04｜President and COO｜guidance：COO 表示全年財測假設 Ojol 佣金結構維持現行（原話："does assume that the commission structure remains"）
- 2026-08-04｜CEO｜margin：CEO 報告第二季調整後 EBITDA 利潤率由 13.3% 升至 16.9%（原話："margin expanding to 16.9% of revenue from 13.3%"）
- 2026-08-04｜President and COO｜margin：COO 重申下半年集團出行利潤率維持歷史區間 8.5% 至 9%（原話："within the historical range of between 8.5% and 9%."）
- 2026-08-04｜President and COO｜margin：COO 給出本季出行利潤率數字（原話："mobility margins this quarter were 8.6%."）
- 2026-08-04｜President and COO｜commitment：COO 承諾下半年出行利潤率留在區間內，不論燃油價格如何（原話："We expect to stay within that range during the second half"）
- 2026-08-04｜CFO｜margin：CFO 說明出行 take rate 受司機補貼以外的夥伴獎勵加碼影響（原話："We're also leaning over and above that around partner"）
- 2026-08-04｜CFO｜product：CFO 稱平均客單價下降來自推出 saver 產品（原話："while the average ticket size went down because we did implement"）
- 2026-08-04｜President and COO｜risk：COO 說明已承諾的燃油補貼金額，自三月油價飆升起（原話："we have committed $7 million already to build support"）
- 2026-08-04｜President and COO｜risk：COO 說明印尼兩輪 Ojol 占出行 GMV 比重（原話："Ojol in Indonesia represents 6% of our"）
- 2026-08-04｜CEO｜risk：CEO 披露董事 Dara 於 7 月 6 日卸任，與收購 Foodpanda 台灣的治理強化有關（原話："Dara stepped down from our Board effective that date"）
- 2026-08-04｜President and COO｜commitment：COO 重申金融服務下半年達到獲利的承諾（原話："we are on track to achieve profitability for Financial Services"）
- 2026-08-04｜President and COO｜guidance：COO 給出年底放款餘額目標，含 Superbank（原話："book to exceed $3 billion by the end of this year"）
- 2026-08-04｜President and COO｜margin：COO 提供 Superbank 稅前股東權益報酬率數字（原話："pretax return on equity already hitting 5.7% in this quarter."）
- 2026-08-04｜President and COO｜guidance：COO 預期 Superbank 成本收入比年底前降至 50% 以下（原話："probably hitting below 50% by the end of the"）
- 2026-08-04｜CEO｜competition：CEO 回應 Uber 問題時引用 Uber 出售 Grab 持股後的競業限制（原話："competing with Grab in our core markets under 1 year"）
- 2026-08-04｜CEO｜customer：CEO 稱成長品質由交易量與用戶帶動而非價格（原話："What stands out is the health of that growth"）
- 2026-08-04｜President and COO｜customer：COO 說明 GrabMart 用戶僅占外送用戶的比例（原話："Mart still only consists of about 14% of our food user base"）
- 2026-08-04｜President and COO｜commitment：COO 表示擴大雜貨業務同時承諾外送利潤率逐年成長（原話："within our commitment to grow Deliveries margins year-on-"）
- 2026-08-04｜President and COO｜guidance：COO 預期雜貨成長快於整體外送，年底占外送 GMV 比重略升（原話："we expect this kind of growth to outpace the overall"）
- 2026-08-04｜President and COO｜product：COO 說明外送業務以固定匯率計成長加速（原話："accelerated again this time to 24% year-on-year growth"）
- 2026-08-04｜CFO｜capital_allocation：CFO 說明新增 7.5 億美元後累計庫藏股授權額度（原話："up to $1.75 billion of cumulative buyback"）
- 2026-08-04｜CFO｜capital_allocation：CFO 說明二月 5 億美元買回已執行的規模（原話："executed roughly about $400 million off that $500 million"）
- 2026-08-04｜CFO｜capital_allocation：CFO 表示買回視股價是否出現失衡而執行（原話："we'll execute where we continue to see a"）
- 2026-08-04｜CFO｜capital_allocation：CFO 稱併購門檻維持很高（原話："M&A, which we keep a very high bar"）
- 2026-08-04｜CFO｜commitment：CFO 稱 Foodpanda 台灣交易進度符合預期並預期年底前完成（原話："we remain on track with the progress on this transaction itself"）
- 2026-08-04｜CEO｜product：CEO 說明東南亞多數交易為低於一美元的兩輪車，使電動車商業化不經濟（原話："50% of all transactions in Southeast Asia are 2-wheel"）
- 2026-08-04｜CEO｜product：CEO 說明新加坡 Punggol 自駕服務預計第四季開始收取商業車資（原話："public in Q4 when we start charging commercial fares"）
- 2026-08-04｜CEO｜product：CEO 把 AI 視為利潤率槓桿（原話："why we can continue to treat AI as a margin lever."）
- 2026-08-04｜CFO｜commitment：CFO 結語稱金融服務轉盈是下一個催化劑（原話："is the next real catalyst for us"）

### 問答異常語氣（迴避／改口／保留）
- GRAB_Q2_2026_Earnings_Call_20260804.md｜問：Foodpanda 台灣的整合前期成本是多少？是否已計入 2026 財測？｜答法：CFO 只說進度符合預期、與監管機關密切討論、預期年底前完成，未回答整合成本金額，也未說明是否計入財測
- GRAB_Q2_2026_Earnings_Call_20260804.md｜問：出行 GMV、交易量與營收成長差距，take rate 下半年是否穩定或回升，出行營收如何展望？｜答法：CFO 解釋補貼與 saver 產品原因及出行利潤率 8.6%，未給 take rate 下半年走向或出行營收成長展望
- GRAB_Q2_2026_Earnings_Call_20260804.md｜問：燃油價格展望，以及出行利潤率何時回到區間高端？｜答法：COO 表示不預測油價，未給利潤率回到高端的時點，只說留在 8.5% 至 9% 區間內
- GRAB_Q2_2026_Earnings_Call_20260804.md｜問：Uber 擬收購 Delivery Hero 對東南亞競爭格局（經 Foodpanda）的影響？｜答法：CEO 談與 Uber 的股東對話、競業限制與結構優勢，未直接評論 Delivery Hero 交易的影響
- GRAB_Q2_2026_Earnings_Call_20260804.md｜問：一年後 Mart 占總 GMV 的比重與成長軌跡？｜答法：COO 只說年底占外送 GMV 比重略升、長期目標更高，未給具體百分比

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
{"date":"20260905","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":13.6,"ev5y_pct":93.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"❌","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":5.17,"ev5y_pct":93.7,"irr_base_pct":13.6,"max_dd_pct":-48,"bull_5y_price":12.5,"bear_5y_price":2.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":null,"price_at_dd":3.42,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
