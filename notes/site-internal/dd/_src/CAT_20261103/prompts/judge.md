你是 stock-analyst **v20 判斷 agent**，標的 CAT（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CAT","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAT_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAT_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_sales_and_revenues_gaap","label":"營收（Sales and revenues, GAAP）","value":20682,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 caterpillar.com 3Q26 results／8-K Ex.99.1"}},{"id":"f_kpi1_adjusted","label":"Adjusted 營業利益／利益率（排除重組成本）","value":20.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 caterpillar.com 3Q26 results／8-K Ex.99.1"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":20.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 caterpillar.com 3Q26 results／8-K Ex.99.1"}},{"id":"f_kpi3_eps_gaap_adjusted","label":"EPS（GAAP／Adjusted）","value":7.13,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司新聞稿 caterpillar.com 3Q26 results／8-K Ex.99.1"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_cat_gross_margin_pct","label":"CAT 毛利率","value":32.65,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cat_operating_margin_pct","label":"CAT 營業利益率","value":17.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cat_fcf_margin_pct","label":"CAT FCF 利潤率","value":11.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_de_gross_margin_pct","label":"DE 毛利率","value":34.64,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DE.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_de_operating_margin_pct","label":"DE 營業利益率","value":17.59,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DE.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_de_fcf_margin_pct","label":"DE FCF 利潤率","value":6.89,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DE.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_6301_t_gross_margin_pct","label":"6301.T 毛利率","value":30.48,"period":"TTM ending 2026-03-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6301.T.gross_margin_pct","as_of":"TTM ending 2026-03-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_6301_t_operating_margin_pct","label":"6301.T 營業利益率","value":13.82,"period":"TTM ending 2026-03-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6301.T.operating_margin_pct","as_of":"TTM ending 2026-03-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_6301_t_fcf_margin_pct","label":"6301.T FCF 利潤率","value":5.73,"period":"TTM ending 2026-03-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6301.T.fcf_margin_pct","as_of":"TTM ending 2026-03-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_uri_gross_margin_pct","label":"URI 毛利率","value":39.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.URI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_uri_operating_margin_pct","label":"URI 營業利益率","value":25.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.URI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_uri_fcf_margin_pct","label":"URI FCF 利潤率","value":5.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.URI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cnh_gross_margin_pct","label":"CNH 毛利率","value":30.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CNH.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cnh_operating_margin_pct","label":"CNH 營業利益率","value":13.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CNH.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cnh_fcf_margin_pct","label":"CNH FCF 利潤率","value":3.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CNH.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_me_t_me_t_me_t_me_t_9m_6","label":"ME&T 自由現金流（自算：ME&T 營業現金流 − ME&T 資本支出 − ME&T 租賃設備支出，由 9M 累計減 6M 累計）","value":3827,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"8-K Ex.99.1 現金流量表 ME&T 欄：9M 營業現金流 11,534、資本支出 1,993、租賃設備 16；6M（Q2 8-K Ex.99.1）7,011、1,302、11。新聞稿未直接給單季 FCF，此為自算，非公司揭露口徑"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":620.38,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-28.78,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":23.72,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.62,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（27.33 → 27.5）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.86,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（32.59 → 32.31）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.87,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（39.21 → 38.87）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":27.5,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":32.31,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":38.87,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":11.25,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 24.72 → 27.5（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":24.36,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝59.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":59.5,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.67,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝76.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":76.6,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.16,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝76.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":76.5,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":22.57,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 27.5，分子＝快照價 620.62","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.012,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":38099.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 45201.0、現金 7102.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":459.67,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":323382.42,"period":"2026-11-03","unit":"USD m","basis":"市值 285283.42 ＋ 淨負債 38099.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":79548.42,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（11 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":88185.58,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.07,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 619.57 / W52 759.92 / W104 572.89 / W250 385.38 / W250 13週斜率 1.96%"},{"id":"f_ma_w52","label":"52 週均線","value":759.92,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":572.89,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":385.38,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.96,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K FY2025 列出全球與中國區域競爭者（Komatsu、Sany、XCMG、LiuGong、SDLG、Shantui 等），並稱競爭強度有時造成特定產業或地區價格折扣、壓縮利潤。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/18230/000001823026000008/cat-20251231.htm","excerpt":"Our global surface competitors include Deere Construction & Forestry (part of Deere & Company), Epiroc AB, Hitachi Construction Machinery Co., Ltd., Komatsu Ltd., Liebherr-International AG, Sandvik AB, and Volvo Construction Equipment.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：競爭者積極定價等可能降低公司產業銷售份額。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/18230/000001823026000008/cat-20251231.htm","excerpt":"Thus, our share of industry sales could be reduced due to aggressive pricing or product strategies pursued by competitors, unanticipated product or manufacturing difficulties, our failure to price our products competitively","as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"CAT FY2025 10-K 披露：金融應收款與經銷商存貨應收款中，無單一客戶或經銷商構成重大信用集中風險。","source":"SEC EDGAR 10-K FY2025 Item 8 Concentration of Credit Risk","url":"https://www.sec.gov/Archives/edgar/data/18230/000001823026000008/cat-20251231.htm","excerpt":"No single customer or dealer represented a significant concentration of credit risk.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2019 至 FY2024 各年 10-K 皆為同一結論（無單一客戶或經銷商構成重大信用集中），屬一貫表述；該段針對應收款信用風險，未涉營收占比。","source":"SEC EDGAR CAT 10-K FY2024 與歷年（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/18230/000001823025000008/cat-20241231.htm","excerpt":null,"as_of":"2025-02-14","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"CAT Q2 2026 backlog 約 $72B、年增 92%；59% 排定 12 個月內出貨，部分 Power & Energy 訂單排到 2029–2030。","source":"GuruFocus, Caterpillar Q2 2026 Earnings Call Highlights: Record $20.5B Quarter, Backlog Soars 92% to $72B","url":"https://gurufocus.com/news/9002976/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"風險面：成長高度依賴資料中心客群，AI 建設暫停會衝擊；長期 backlog 可能被改期或取消。","source":"TIKR, Caterpillar's backlog hits a record $72 billion","url":"https://www.tikr.com/blog/caterpillars-backlog-hits-a-record-72-billion-is-the-stock-still-undervalued","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"設備業產能擴張：Sany India 董事稱主要建機廠產能近 2–3 年已滿載，各家都在擴產；CNH 印度 Pithampur 擴產 20–25%。","source":"Autocar Pro, Sany India to invest Rs 1000 crore in next 3 years","url":"https://autocarpro.in/news/sany-india-to-invest-rs-1000-crore-in-next-3-years-117689?amp=1","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"需求展望：BofA 預期多數營建相關股票 2027 年獲利成長快於 2026；ICRA 預估印度 FY2027 設備量 +8–10%。未找到 2028 共識。","source":"BofA, Green shoots on machinery's horizon; ICRA Construction Equipment","url":"https://business.bofa.com/en-us/content/improving-machinery-stock-mike-feniger.html","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Caterpillar 子公司 Progress Rail 於 2026 年 2 月撤回對 Wabtec 的反壟斷訴訟（Caterpillar 為原告，非被調查方）。","source":"Law360｜Caterpillar Unit Drops Antitrust Suit Against Wabtec","url":"https://www.law360.com/articles/2444346","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Bobcat 於 2025-12-02 向美國 ITC 提出申訴，指 Caterpillar 違反裝載機、推土機、挖掘機等進口規則（Federal Register 摘要）；尚未讀到頁面，狀態未核。","source":"policyrisk.com 彙整 Federal Register｜Caterpillar Files ITC Complaint Over Heavy Equipment Imports","url":"https://policyrisk.com/federal-register/2026-10673","excerpt":null,"as_of":"2026-05-29","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Baird 於 2026 年 7 月下旬將 CAT 降至 Neutral，理由為各州對資料中心建設的政策阻力（含紐約州新建大型資料中心暫停令，7-14 生效）可能自 2027 年起影響發電業務。","source":"Barchart｜Baird just downgraded Caterpillar stock, here's why","url":"https://www.barchart.com/story/news/3531384/baird-just-downgraded-caterpillar-stock-here-s-why","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Caterpillar 2026 年 10-Q 稱未決法律訴訟預期不具重大性。","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0000018230/000001823026000046/cat-20260630.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"CAT 預期 2026 年關稅衝擊約 26 億美元，較 2025 年實際高 8 億；若無緩解措施約再高 20%。2025 年營業利潤減少主因為製造成本不利，主要反映關稅上升。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/18230/000001823026000008/cat-20251231.htm","excerpt":"Based on the incremental tariffs announced in 2025 and in place by January 29, 2026, we expect the impact from tariffs to be around $2.6 billion in 2026, which is $800 million higher than incurred in 2025. If we do not take the mitigating actions we plan to take in 2026, the impact from tariffs could be around 20 percent higher.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026 年增量關稅成本約 50% 落在 Construction Industries、20% Resource Industries、30% Power & Energy；Q1 2026 預期約 8 億美元。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/18230/000001823026000008/cat-20251231.htm","excerpt":"We expect the impact from incremental tariffs to be around $800 million in the first quarter of 2026, which is similar to the fourth quarter of 2025. We anticipate around 50 percent of the incremental tariff costs will be in Construction Industries, 20 percent in Resource Industries and 30 percent in Power & Energy.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子揭露受 BIS、OFAC、DDTC 等進出口與制裁法規約束，貿易限制可能影響需求、競爭地位或使其無法在特定國家銷售。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/18230/000001823026000008/cat-20251231.htm","excerpt":"Government policies on international trade and investment such as import quotas, capital controls or tariffs, whether adopted by individual governments or addressed by regional trade blocs, can affect the demand for our products and services, impact the competitive position of our products or prevent us from being able to sell products in certain countries.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"CAT Q2 2026 10-Q：2026 年關稅成本約 22 億美元（扣除回收前），IEEPA 關稅 2026-02-20 遭最高法院裁定未授權，認列 3.92 億美元預期 IEEPA 關稅回收。","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0000018230/000001823026000046/cat-20260630.htm","excerpt":"IEEPA tariffs in 2026, the company's total IEEPA tariff costs were approximately $1.0 billion. 11 Table of Contents During the second quarter of 2026, CBP launched the Consolidated Administration and Processing of Entries (CAPE) system, which enabled the submission of certain IEEPA refund claims. For both the three and six months ended June 30, 2026, the company recorded $392 million of","as_of":"2026-08-05","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"2026 年 6 月公告將推土機、堆高機、農機之 Section 232 關稅由 25% 降至 15%（6/8 生效至 2027 年底）。","source":"Barchart: Trump just gave Caterpillar stock a boost","url":"https://www.barchart.com/story/news/2308052/trump-just-gave-caterpillar-stock-a-boost-what-to-know","excerpt":null,"as_of":"2026-06-10","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"CAT Q2 2026 10-Q：排除預期 IEEPA 關稅回收，2026 年關稅成本預估約 22 億美元；IEEPA 關稅成本 2025 起至 CBP 停徵累計約 10 億美元；供應鏈關注重點為運輸、部分零組件與原物料。","source":"Caterpillar Form 10-Q (quarter ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0000018230/000001823026000046/cat-20260630.htm","excerpt":"Excluding the expected IEEPA tariff recoveries in the second quarter of 2026, we now expect 2026 tariff costs of around $2.2 billion.","as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"CAT 供應基礎為全球性：超過 600 家海外供應商、約 50 家為關鍵供應商，關稅與貿易爭端被列為零組件流動風險（二手 SWOT 文章轉述 Reuters，2024 年底）。","source":"Investing.com Caterpillar SWOT analysis","url":"https://investing.com/news/swot-analysis/caterpillars-swot-analysis-global-supply-chain-autonomy-drive-stock-outlook-93CH-3775953","excerpt":null,"as_of":"2024-12-31","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"次級分析：CAT 中國曝險與美中貿易關係及中國市場疲弱相關。","source":"Kavout market lens","url":"https://www.kavout.com/market-lens/is-caterpillar-s-china-exposure-a-blessing-or-a-curse-amid-trade-tensions","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"CAT 2026Q3 總營收 206.82 億美元，年增 17%；Power & Energy 營收 +18% 至 87.84 億，其中發電（Power Generation）+30%，主因資料中心用渦輪與大型引擎；Construction Industries +18% 至 79.83 億（北美帶動）；Resource Industries 46.15 億，對用戶銷售僅 +4%，管理層稱採礦設備出貨/試車延遲屬暫時；積壓訂單創高 780 億美元","source":"Caterpillar 3Q2026 earnings release (SEC 8-K ex99.1)；分段數字部分來自二手摘要，待核","url":"https://www.sec.gov/Archives/edgar/data/0000018230/000001823026000052/ex991toformcat3q2026earnin.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"公司 2026 全年指引：三大主要分部皆強勁成長，主要由銷量與有利價格實現（price realization）驅動；2025 年價格實現約 -8 億美元拖累；2026 預計關稅成本約 22 億美元（不含 IEEPA 退稅）","source":"Caterpillar 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0000018230/000001823026000046/cat-20260630.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Power & Energy 對用戶銷售 +36%、發電 +75%，資料中心訂單延伸至 2029–2030；計畫將大型往復式引擎產能較 2024 年擴三倍；2024–2030 營收 CAGR 目標 6–9%；經銷商年底庫存預期高於 2025 以備 2027 用戶銷售；風險：紐約州 7 月對新超大型資料中心設暫停令","source":"Manufacturing Dive／MarketBeat Q3 2026 call 摘要","url":"https://www.marketbeat.com/instant-alerts/transcript-caterpillar-q3-earnings-call-highlights-2026-10-30/","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"CAT 10-K FY2025 風險因子：能源、運輸、採礦客戶的購買決策取決於未來商品動態，包含商品替代（commodity substitutions）造成的價格波動；未提及以替代設備技術取代 CAT 核心產品。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/18230/000001823026000008/cat-20251231.htm","excerpt":"Commodity price volatility may be abrupt and unpredictable in response to global economic conditions, government actions, regulatory changes, supply/demand dynamics, innovation, and commodity substitutions among others.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"中國挖機出口 2026 上半年成長 33%，三一、中聯、徐工逐步侵蝕 Hitachi、Komatsu、Caterpillar 等國際大廠市占（KHL Yellow Table），產業轉向電動。","source":"SCMP: China's excavator exports surge 33% in first half as industry pivots to electric power","url":"https://www.scmp.com/economy/china-economy/article/3359726/chinas-excavator-exports-surge-33-in-first-half-as-industry-pivots-to-electric-power","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"CAT 於 CES 2026 說明將自動化延伸至挖掘機、裝載機、推土機、壓路機，未提供商業化時程。","source":"Heavy Equipment Magazine: Caterpillar Heads to Conexpo 2026 with Automation, AI and New Service Options","url":"https://www.heavyquipmag.com/2026/02/10/caterpillar-heads-to-conexpo-con-agg-2026-with-automation-ai-and-new-service-options/","excerpt":null,"as_of":"2026-02-10","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：Caterpillar 機械主要仍經全球經銷商網路銷售（美國 41、美國以外 109，服務 190 國）；Perkins 另有 86 家經銷商、FG Wilson 108 家經銷商。經查一手文件未見轉向直營／D2C 的描述。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/18230/000001823026000008/cat-20251231.htm","excerpt":"We distribute our machines principally through a worldwide organization of dealers (dealer network), 41 located in the United States and 109 located outside the United States, serving 190 countries.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Trefis：2026 Q2 營建部門經銷商庫存增加 4 億美元，管理層預期 Q4 減少逾 10 億美元；營建 sales to users 增 22%，租賃車隊補貨計入。","source":"Trefis, Is Caterpillar Stock Relying on an Artificial Demand Story?","url":"https://www.trefis.com/articles/613531/is-caterpillar-stock-relying-on-an-artificial-demand-story/2026-08-28","excerpt":"Industries outpacing the global industry on 5% full-year sales to users growth. On the second-quarter 2026 call the term surfaced exactly once, in reply to an analyst question and not at all in the prepared remarks, and in that same answer the CEO still credited the programs for outperformance carried through the first half of 2026. Rental Fleet Loading Is A Bigger Piece Of The Segment’s Growth","as_of":"2026-08-28","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Digital Commerce 360：Caterpillar 目標 2026 年服務營收 280 億美元，Helios 平台連結逾 150 萬台機器，服務與設備經既有經銷商通路銷售。","source":"Digital Commerce 360, Caterpillar digital $28 billion services revenue","url":"https://www.digitalcommerce360.com/2025/07/18/caterpillar-digital-28-billion-services-revenue/","excerpt":"Caterpillar aims for $28 billion in services revenue by using digital technologies Share This Story: News Caterpillar aims for $28 billion in services revenue by using digital technologies Mark Brohan | Jul 18, 2025 Share: Time to Read: 2.5 minutes The role of ecommerce is also expanding, with Caterpillar’s online parts platform, in partnership with its dealer network, processing more","as_of":"2025-07-18","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 10-Q 將 2026 關稅成本預期降至約 22 億美元（不含 Q2 預期 IEEPA 關稅退還），展望未納入下半年額外 IEEPA 退還；搜尋摘要稱 Q1 後公司將全年銷售成長指引由 5-7% 上調至低雙位數，Q2 後再上調至中高十位數（%）。","source":"SEC 10-Q FY2026 (cat-20260630) / TIKR 'Caterpillar raises guidance after Q1 revenue jumps 22% to $17.4B'","url":"https://www.sec.gov/Archives/edgar/data/0000018230/000001823026000046/cat-20260630.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Walnut（2026-08 資料）：26 位分析師，目標價區間 $575–$1,218、均值約 $959；評等 14 買進、12 持有、2 賣出，買進占比近三個月下降。","source":"Walnut Invest — Caterpillar (CAT) Stock Forecast and Price Target (2026)","url":"https://walnutinvest.com/stocks/cat/forecast","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"ChartMill：FY2026 共識 EPS 27.89（截至 2026-10-17，33 位分析師），Q3 2026 共識 EPS $7.15，財報預計 10-29。","source":"ChartMill CAT Earnings & Revenue Estimates, Forecasts & Revisions","url":"https://www.chartmill.com/stock/quote/CAT/estimates","excerpt":null,"as_of":"2026-10-17","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Evercore ISI 2026-05 將目標價由 $878 升至 $1,103","source":"Yahoo Finance — Evercore Turns More Bullish on Caterpillar","url":"https://finance.yahoo.com/markets/stocks/articles/evercore-turns-more-bullish-caterpillar-143636746.html","excerpt":"with $1,103 Price Target Vardah Gill May 22, 2026 2 min read CAT -0.28% Caterpillar Inc. (NYSE:CAT) is included among the 10 High Quality Stocks to Buy According to Hedge Funds. Wells Fargo Sees Caterpillar (CAT) Benefiting From Data Center and Energy Demand On May 11, Evercore ISI analyst David Raso raised the price recommendation on Caterpillar Inc. (NYSE:CAT) to $1,103 from $878.","as_of":"2026-05-22","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 營收創紀錄 $20.5B、積壓訂單 $72B，並上調全年展望","source":"GuruFocus Q2 2026 Earnings Call Highlights","url":"https://gurufocus.com/news/9002976/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Caterpillar 於 2026-02-04 完成收購 RPMGlobal（ASX:RUL），早期報導交易價值約 7.28 億美元；另 2026-07-07 完成收購 Skycatch，2026-09-29 同意收購經銷商 John Fabick Tractor（條款未揭露，待監管核准）。","source":"WebSearch 摘要（聚合彙整，含 RPM 公司公告頁、Option Finance 2026-09-29 報導）","url":"https://rpmglobal.com/company-update-caterpillar-cat-and-rpm-have-signed-a-binding-scheme-implementation-deed/","excerpt":null,"as_of":"2026-09-29","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"SEC EDGAR 近 12 個月 11 份 8-K，含重大項目者 4 份；清單中無 Item 4.02（財報不可信賴／重編）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000018230&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Escorts Kubota 於 2026-08-19 在北方邦動土 154 英畝新廠，第一期增加最多 6 萬台曳引機與 1.5 萬台工程機械年產能，投資逾 ₹2,000 億盧比（約 200 億）；現有年產能約 17 萬台曳引機、1 萬台工程機械；完工日期未載明。","source":"themachinemaker.com - Escorts Kubota announces investment plan for new plant","url":"https://themachinemaker.com/news/escorts-kubota-announces-investment-plan-for-new-plant/","excerpt":null,"as_of":"2026-08-19","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"CNH 預期 2026 年零售需求較 2025 年下滑約 5%，並維持低產量；預期農機產業需求 2027 年恢復成長（同業減產屬供給紀律訊號）。","source":"ttnews.com - CNH expects farm equipment demand to revive in 2027","url":"https://www.ttnews.com/articles/cnh-farm-machine-rebound-2027","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R","triggers"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Caterpillar 自身擴產：Q1 2026 財報會上將大型往復式引擎產能目標由 2024 年的 2 倍上調至近 3 倍，追加投資主要在 2027–2029，預期年底前現金回收轉正；Q2 10-Q 稱擴產進行中，預期 2026 下半年產出提升。搜尋未找到同業具體擴產公告（僅 Terex 回補訂單 69 億美元，屬需求指標）。","source":"Caterpillar Q1 2026 Earnings Call Transcript (MarketBeat); CAT 10-Q FY2026 Q2","url":"https://www.sec.gov/Archives/edgar/data/0000018230/000001823026000046/cat-20260630.htm","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"CAT 經銷商庫存 2026 上半年回補 $26 億（去年同期增 $2 億），其中 Construction Industries 增 $19 億（去年同期減 $4 億）","source":"Caterpillar Form 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0000018230/000001823026000046/cat-20260630.htm","excerpt":"Dealer inventory increased $2.6 billion during the six months ended June 30, 2026, compared with an increase of $200 million during the six months ended June 30, 2025.","as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation","triggers","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"Q1 2026 經銷商庫存增 $20 億（去年同期增 $1 億），Construction Industries 增 $15 億","source":"Caterpillar Form 10-Q (period ended 2026-03-31)","url":"https://www.sec.gov/Archives/edgar/data/0000018230/000001823026000021/cat-20260331.htm","excerpt":"Total dealer inventory increased $2.0 billion during the first quarter of 2026, compared with an increase of $100 million during the first quarter of 2025.","as_of":"2026-05-01","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"二手營建設備價值因庫存上升而下滑；農機市場處於長期下行但價格仍維持高檔（次級來源摘要）","source":"equipmentfinancenews.com 'Used construction equipment values fall amid rising inventories'","url":"https://equipmentfinancenews.com/tag/skid-steers/","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"管理層預期 Q4 Construction Industries 經銷商庫存下降逾 $10 億","source":"Insider Monkey 'Caterpillar (CAT): Can Earnings Keep Growing After Dealers Stop Restocking?'","url":"https://www.insidermonkey.com/news/caterpillar-cat-can-earnings-keep-growing-after-dealers-stop-restocking-1848714/","excerpt":"Management expects Construction Industries dealer inventories to decline by more than $1 billion in the fourth quarter. Dealers can satisfy customers by selling machines already on hand, reducing factory shipments even when retail activity remains healthy.","as_of":"2026-10-12","retrieved_at":"20261103","affects":["triggers","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"CAT 2016 營業利益 $498M，對比 2015 年 $3.785B，主因銷量下滑與產品組合不利，另含 Resource Industries 商譽減損與退休金 MTM 損失","source":"Caterpillar FY2016 10-K / Q3 2016 8-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000018230/000001823017000041/cat_10-kx12312016.htm","excerpt":"Operating profit for 2016 was $498 million, compared with $3.785 billion in 2015.","as_of":"2017-02-15","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"CAT 2020 全年營業利益率 10.9%，2019 年為 15.4%；2020 銷售約下滑 22%","source":"Caterpillar 4Q20 financial results","url":"https://www.caterpillar.com/content/dam/caterpillarDotCom/releases/4q20/4q20-caterpillar-inc-financial-results.pdf","excerpt":"Operating profit as a percent of sales and revenues was 10.9 percent in 2020, compared with 15.4 percent in 2019.","as_of":"2021-01-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"CAT 2015 營收約 $47.0B，較 2014 年降 15%，獲利降 43% 至 $2.1B；Q4 2015 虧損 $87M（去年同期獲利 $757M）","source":"Caterpillar FY2015 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000018230/000001823016000410/cat10k2015.pdf","excerpt":null,"as_of":"2016-02-15","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Motley Fool 稱 CAT 股價 2015 年下跌約 25%","source":"Motley Fool, Will 2016 be Caterpillar Inc's best year yet","url":"https://www.fool.com/investing/general/2016/01/02/will-2016-be-caterpillar-incs-best-year-yet.aspx","excerpt":null,"as_of":"2016-01-02","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-02-04 完成收購 RPMGlobal；2026-07-07 完成收購 Skycatch；2026-09-29 同意收購 John Fabick Tractor（待核准，條款未揭露）。Monarch Tractor 為 Bloomberg Law 2026-04 報導、未見公司證實。","source":"WebSearch 摘要；RPMGlobal 公司更新頁；Option Finance 2026-09-29","url":"https://rpmglobal.com/company-update-caterpillar-cat-and-rpm-have-signed-a-binding-scheme-implementation-deed/","excerpt":null,"as_of":"2026-09-29","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 清單中未列 Item 4.02（重編）項目；搜尋所得 SEC／大陪審團調查皆為 2013–2017 舊事。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000018230&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"CAT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":32.65,"operating_margin_pct":17.59,"fcf_margin_pct":11.08,"rd_intensity_pct":3.0},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAT","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"DE","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":34.64,"operating_margin_pct":17.59,"fcf_margin_pct":6.89,"rd_intensity_pct":5.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DE","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"6301.T","period":"TTM ending 2026-03-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":30.48,"operating_margin_pct":13.82,"fcf_margin_pct":5.73,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6301.T","as_of":"TTM ending 2026-03-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"URI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":39.08,"operating_margin_pct":25.91,"fcf_margin_pct":5.1,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.URI","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CNH","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":30.55,"operating_margin_pct":13.75,"fcf_margin_pct":3.36,"rd_intensity_pct":5.97},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CNH","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"CAT"},"financial_history":{"ticker":"CAT","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":59427000000.0,"revenue_yoy_pct":null,"gross_margin_pct":29.47,"operating_margin_pct":14.86,"net_income":6705000000.0,"diluted_eps":12.64,"free_cash_flow":5167000000.0,"fcf_margin_pct":8.69,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":67060000000.0,"revenue_yoy_pct":12.84,"gross_margin_pct":34.69,"operating_margin_pct":19.33,"net_income":10335000000.0,"diluted_eps":20.12,"free_cash_flow":9793000000.0,"fcf_margin_pct":14.6,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":64809000000.0,"revenue_yoy_pct":-3.36,"gross_margin_pct":35.99,"operating_margin_pct":20.17,"net_income":10792000000.0,"diluted_eps":22.05,"free_cash_flow":8820000000.0,"fcf_margin_pct":13.61,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":67589000000.0,"revenue_yoy_pct":4.29,"gross_margin_pct":31.78,"operating_margin_pct":16.5,"net_income":8884000000.0,"diluted_eps":18.81,"free_cash_flow":7453000000.0,"fcf_margin_pct":11.03,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CAT/CAT_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Caterpillar Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Welcome to the Third Quarter 2026 Caterpillar Earnings Conference Call. Please be advised that today's conference is being recorded. [Operator Instructions] I would now like to hand the conference over to your speaker today, Alex Kapper. Thank you. Please go ahead.

**Alex Kapper** (Executives):
Thank you, Audra. Good morning, everyone, and welcome to Caterpillar's Third Quarter of 2026 Earnings Call. I'm Alex Kapper, Vice President of Investor Relations. Joining me today are Joe Creed, Chairman and CEO; Kyle Epley, Chief Financial Officer; Stephanie Baughman, Senior Vice President of the Global Finance Services Division; and Ryan Coleman, Senior Director of IR. During our call, we'll be discussing third quarter earnings release we issued earlier today. You can find our slides, the news release and a webcast recap at investors.caterpillar.com under Events and Presentations. The content of this call is protected by U.S. and international copyright law. Any rebroadcast, retransmission, reproduction or distribution of all or part of this content without Caterpillar's prior written permission is prohibited.
Moving to Slide 2. During our call today, we'll make forward-looking statements, which are subject to risks and uncertainties. We'll also make assumptions that could cause our actual results to be different than the information we're sharing with you on this call. Please refer to our recent SEC filings and the forward-looking statements reminder in the news release for details on factors that individually or in aggregate could cause our actual results to vary materially from our forecast. A detailed discussion of the many factors that we believe may have a material effect on our business on an ongoing basis is contained in our SEC filings.
On today's call, we'll also refer to non-GAAP numbers. For any reconciliation of any non-GAAP numbers to the appropriate U.S. GAAP numbers, please see the appendix of the earnings call slides. For today's agenda, Joe will begin by sharing his perspectives about our results, and he will highlight key initiatives across our segments. Then he'll discuss our full year outlook and insights about our end markets. Kyle will provide a detailed overview of results and share key assumptions looking forward. We will conclude by taking your questions. Now let's advance to Slide 3 and turn the call over to Joe Creed.

**Joseph Creed** (Executives):
All right. Good morning, and thanks, Alex. I appreciate everyone joining us today. Our third quarter results reflect the durability of our end markets with our highest sales quarter ever, strong order rates and a record backlog. Our team continues to execute our strategic priorities in a dynamic environment, positioning us for a strong year. Sales and revenues were $20.7 billion, up 17% versus the prior year, driven by strong end market demand. We delivered adjusted profit per share of $7.20, an increase of 45% versus last year.
Strong order rates across all 3 of our primary segments drove backlog to a record $78 billion. That's an increase of approximately $38 billion or 96% from the third quarter last year and marks the fourth consecutive quarter of sequential backlog growth in all 3 of our primary segments. The quarter demonstrated the team's ability to execute in a high-growth environment. Specifically, our Power & Energy team continued to increase production of large reciprocating engines and turbines while simultaneously expanding capacity to meet demand. The team is effectively managing the operational challenges that come with this rapid growth. Bringing additional capacity online is still the top pacing factor for growth in Power & Energy, so working diligently to execute our plans and meet our customers' needs. 
As I mentioned, sales and revenues were $20.7 billion, and they were in line with our expectations. The increase from the prior year was primarily driven by strong growth in sales volume and favorable price realization in all 3 of our primary segments. Third quarter adjusted operating profit margin was 20.6%. Excluding IEEPA tariff recoveries, adjusted operating profit margin was in line with our expectations. In the third quarter, we generated MP&E free cash flow of $3.8 billion and deployed $2 billion to shareholders through share repurchases and dividends.
Now I'll review third quarter retail statistics. In Power & Energy, sales to users grew a robust 36%. Power generation grew 75%, driven by continued very strong demand for turbines and large reciprocating engines used in data center applications. Sales to users in oil and gas increased 5% and were driven by turbines and turbine-related services. Industrial sales to users were down due to softness in the EAME region.
Now for Construction Industries. We have one of the broadest ranges of products, technology and services to support customers, whether they prefer to own, lease or rent equipment. Combined with healthy construction activity, our unique position has allowed us to outpace the industry throughout the year. In the third quarter, total sales to users increased 20%, marking the seventh consecutive quarter of year-over-year growth. In North America, sales to users grew a robust 27%, in line with expectations. Dealer rental revenue in North America continued to grow, driving increased investment in their equipment fleets.
We also saw strong customer interest in the Cat dealer-owned rental joint venture called Major Projects, which was launched last quarter. As a reminder, Major Projects will serve customers developing large-scale infrastructure across North America, including transportation, energy, manufacturing and data center builds. It's a supplemental national rental solution to help deliver larger size class construction equipment and capabilities where existing individual dealer rental fleets aren't sufficient to execute at scale.
As a result, rental fleet loading was exceptionally strong in the third quarter, contributing significantly to sales to users growth compared with prior year when fleet loading was a slight headwind. Even excluding the positive impact from the rental fleet loading, sales to users growth was strong, driven by residential and nonresidential construction activity. Sales to users in EAME were above expectations, with growth driven by strength in Europe and Africa, partially offset by softness in the Middle East. In Asia Pacific, sales to users outside of China were lower than we anticipated and declined slightly due to timing. China, however, continued to grow from a low base as we expected. Latin America continued to grow but at a lower rate than we anticipated.
For Resource Industries, third quarter sales to users increased 4%, which is below our expectations. Sales to users were higher in heavy construction and quarry and aggregates, but lower in mining due to delays in shipping and commissioning. The rail decrease was driven by lower international locomotive deliveries. 
Turning to Slide 4. I'll cover a few highlights since our last earnings call, starting with Power & Energy. We serve customers across the Power & Energy value chain and demand for our solutions remains strong. To ensure we can meet their needs and maintain operational excellence, we're continually evaluating opportunities to repurpose underutilized facilities across our footprint. In line with that approach, we plan to use a portion of our Winston-Salem, North Carolina facility, which currently produces locomotive engines, as a second assembly and test location for the 3600 Series large reciprocating engine. The footprint will support our oil and gas customers to meet the growing need for natural gas compression. The initiative directly supports previously announced plans to increase large reciprocating engine capacity to nearly 3x the '24 level by 2030. Utilizing our existing footprint and workforce is the most cost-effective and quickest way for us to bring additional capacity online.
In Construction Industries, we launched Cat Compact earlier this year, a key part of our strategy to reach more small contractors in the growing compact construction equipment industry. To support that growth and meet increasing customer demand, we announced a $1 billion investment to expand manufacturing capacity in Sanford, North Carolina. The investment will create a modern, technology-enabled manufacturing environment designed to improve safety, quality and operational performance while supporting long-term growth. The facility will incorporate advanced manufacturing technologies, automation, digital production systems and integrated logistics capabilities to create a more connected and efficient operation. This demonstrates how we're aligning our investments to meet our 2030 targets and positioning Caterpillar for long-term profitable growth. 
And in Resource Industries, we announced last month that we're working with Luck Stone to expand autonomous hauling technology across 2 additional Virginia operations. The expansion follows a highly successful pilot at the Bull Run Quarry, where autonomous trucks have hauled more than 3.5 million tons since going live in November of 2024. These deployments also mark the first use of Caterpillar's autonomous technology on a Cat 775 truck, expanding our advanced autonomy capabilities beyond large mining applications and into quarry and aggregates. Through this customer collaboration, we gained insights that are helping us refine and scale our autonomous hauling solutions that deliver measurable value for operations at job sites around the world. This expansion marks another important step towards our goal of tripling the number of Cat autonomous trucks by 2030 compared with 2024.
Now on Slide 5, I'll provide an update on our outlook. Our strong execution through the first 9 months positions us well to meet our full year outlook. We continue to expect our full year 2026 sales and revenues to grow in the mid- to high teens. Strong order rates and a growing backlog reflect continued broad-based momentum across our business, despite ongoing geopolitical uncertainty. Excluding the favorable impact from IEEPA tariff recoveries, we continue to expect full year adjusted operating profit margin to be near the bottom of the target range.
Our full year margin expectation reflects the strategic investments we're making to execute our growth strategy as well as the ongoing impact of tariffs and higher freight costs due to elevated energy prices. We remain focused on delivering long-term OPACC growth, and we aim to operate around the midpoint of our adjusted operating profit margin target range over time. We're also maintaining our MP&E free cash flow expectations to be in the top half of our annual target range. Kyle will provide additional details to you shortly.
And now I'll discuss our key end markets, starting with Power & Energy. We continue to work closely with our customers, which allows us to understand and respond to their evolving needs. Customers' view of demand for both oil and gas and power generation remains strong. As I mentioned, backlog continues to grow due to strong order rates, and we're now taking some large reciprocating orders as far out as 2029 and turbine orders into 2030. We continue to anticipate full year growth in power generation for both Cat reciprocating engines and Solar Turbines, driven by increasing energy demand to support the data center build-out related to cloud computing and generative AI. 
Additionally, prime power demand continues to trend higher as customers look to Caterpillar's turbine and reciprocating engine products to support their need for power solutions. After a record year for sales in 2025, oil and gas is expected to grow moderately again this year. Reciprocating engine sales are anticipated to increase driven by strong demand in gas compression applications. We also see continued momentum in demand for reciprocating engine aftermarket parts. Solar Turbines oil and gas sales are expected to grow and the backlog remains healthy with solid order and inquiry activity. Demand for products in industrial applications is expected to grow moderately in 2026 as well. 
For Construction Industries, we expect strong fourth quarter and full year sales to users growth supported by healthy end markets. The outlook for North America remains positive with construction spending at healthy levels. Nonresidential construction investment continues to be supported by the IIJA, critical infrastructure programs and data centers. We expect fourth quarter dealer rental fleet loading to remain strong. However, it will contribute less to sales to users growth than in the third quarter due to lapping strong rental loading in the fourth quarter of last year. 
In EAME, Europe is expected to remain stable, supported by nonresidential construction, while construction activity in Africa is projected to remain strong. The Middle East continues to face challenges, and we currently anticipate only a limited impact on EAME sales to users. In Asia Pacific, outside of China, stable economic conditions are expected. In China, we anticipate moderate conditions with full year growth in the above 10-ton excavator industry off low levels of activity. We expect full year growth in Latin America. 
We're seeing continued positive momentum in Resource Industries with robust order rates driving strong backlog growth. Customer product utilization is high and the age of the fleet remains elevated. Most key commodities remain above investment thresholds, and customers are focused on the long term. For full year 2026, we expect strong sales to users growth, primarily driven by rising demand for copper and gold, increasing activity in the Canadian oil sands and positive dynamics in heavy construction and quarry and aggregates. We expect commissioning delays from the third quarter to catch up, which will contribute to strong sales to users growth in the fourth quarter. We continue to expect rebuild activity to increase moderately compared with last year. Rail services are anticipated to grow for the year, and we now see -- we now expect locomotive deliveries to be slightly lower year-over-year due to timing of deliveries. 
And finally, earlier this month, we announced that Derrick York will succeed Denise Johnson as Group President of Resource Industries. I want to congratulate Denise on a remarkable career. Under her leadership, Resource Industries returned to profitability and positioned Caterpillar as an industry leader in mining autonomy and technology. I'm deeply grateful for all she's done to strengthen our relationships with customers, develop our people and shape the future of our company. Her impact and influence will be remembered long after her retirement. I've worked closely with Derrick for well over a decade, and I'm confident in his ability to lead the RI team into its next chapter of innovation, growth and customer success. He's a highly respected leader who understands our customers, our strategy and the industries that we serve. With that, I'll turn it over to Kyle.

**Kyle Epley** (Executives):
Thank you, Joe. Good morning, everyone. I'm going to take a few minutes to walk you through our third quarter results, including details about segment performance as well as the balance sheet and cash flow. I will finish with remarks on our expectations for the fourth quarter and current full year assumptions. Beginning on Slide 6. Sales and revenues were $20.7 billion, up 17% versus the prior year, which was in line with our expectations. Adjusted operating profit was $4.3 billion, and our adjusted operating profit margin was 20.6%. Excluding the IEEPA tariff recoveries, both were in line with our expectations.
Moving to Slide 7. The 17% increase in sales and revenues compared to the third quarter of 2025 was primarily driven by strong growth in sales volume and favorable price realization. The stronger sales volume was mainly driven by higher sales of equipment to end users, supported by healthy end market demand and strong execution by our team. Dealer inventory increased by $300 million in Construction Industries compared to an increase of $600 million in the third quarter of 2025. This created a modest headwind to sales volume in the quarter and was in line with our expectations. Sales and revenues, both at a consolidated level and across all 3 primary segments, were in line with our expectations. 
Moving to operating profit on Slide 8. Operating profit in the third quarter increased by 38% to $4.2 billion. Adjusted operating profit of $4.3 billion also increased by 38% versus the prior year. The adjusted operating profit margin was 20.6%, which was an increase of 310 basis points compared to the prior year. Margin benefited from the profit impact of higher sales volume and favorable price realization. This was partially offset by higher manufacturing costs, mainly driven by higher freight and higher expenses related to our capacity expansions. In the quarter, we recognized $128 million in IEEPA tariff recoveries. Nearly all this amount is reflected in corporate items. For tariffs introduced since the beginning of 2025 and excluding IEEPA recoveries, our third quarter tariff costs were approximately $600 million and about flat year-over-year, as we anticipated.
Moving to Slide 9. Profit per share was $7.13 in the quarter. Adjusted profit per share was $7.20. Excluding discrete items, the provision for income taxes in the third quarter of 2026 reflected a global estimated annual effective tax rate of 23%. Finally, the year-over-year impact from the reduction in the average number of shares outstanding due to share repurchases resulted in a favorable impact on adjusted profit per share of approximately $0.15 compared to the third quarter of 2025.
On Slide 10, I will now review the third quarter results of our segments, starting with Power & Energy. For Power & Energy, sales of $8.8 billion increased by 18% versus the prior year, which was in line with our expectations. The sales increase versus the prior year was mainly due to higher sales volume and favorable price realization. Services revenues were also strong in the quarter, especially for sales into oil and gas applications.
Third quarter profit for Power & Energy increased by 31% versus the prior year to $2.1 billion. The segment's margin of 24.4% was an increase of 250 basis points versus the prior year. The increase was mainly due to the profit impact of higher sales volume. Favorable price realization was mostly offset by unfavorable manufacturing costs driven by spend related to our capacity expansions, including higher depreciation along with higher freight and material costs. Segment margin matched our expectations.
Now moving to Slide 11. Construction Industries sales increased by 18% in the third quarter to $8 billion, as we anticipated. The sales increase versus the prior year was primarily due to the higher sales volume and favorable price realization. Higher sales volume was mainly driven by sales of equipment to end users, which included strong contributions from both retail sales and rental fleet loading. Both residential and nonresidential industries contributed to the growth. Third quarter profit for Construction Industries was $1.8 billion, a 33% increase versus the prior year. 
The segment's margin of 22.9% was an increase of 250 basis points versus the prior year, mainly driven by favorable price realization and the profit impact of higher sales volume. This was partially offset by unfavorable manufacturing costs, including the impact of freight and tariff costs. SG&A and R&D expenses related to our digital and technology investments also increased compared to the prior year. Segment margin was also consistent with our expectations.
Turning to Slide 12. Resource Industries sales, which were broadly in line with our expectations, increased by 15% in the third quarter to $4.6 billion, primarily driven by higher sales volume. Price realization was also favorable versus the prior year and slightly better than our expectations, primarily driven by positive geographic mix. Third quarter profit for Resource Industries increased by 14% versus the prior year to $622 million. The segment's margin of 13.5% was roughly unchanged versus the prior year. This was mainly driven by unfavorable manufacturing costs, primarily due to higher material costs, including tariffs, offset by the profit impact of higher sales volume and favorable price realization. Overall, the segment margin was about in line with our expectations. 
Moving to Slide 13. Financial Products revenues increased by 9% versus the prior year to $1.2 billion, mainly due to higher average earning assets across all regions. Segment profit increased by 10% to $264 million. This increase was primarily due to a favorable impact from higher average earning assets, partially offset by a higher provision for credit losses. Our customers' financial health remains strong. Past dues were 1.31% in the quarter, down 16 basis points versus the prior year and remains the lowest level we have recorded since 1998.
The allowance rate was 0.91% at the end of the third quarter. Business activity within Cat Financial remains healthy. Retail new business volume grew by 6% versus the prior year. In addition, used equipment inventory levels continue to remain low and conversion rates remain above historical averages as customers continue to choose to purchase their equipment at the end of their lease term.
Moving on to Slide 14. MP&E free cash flow was $3.8 billion in the quarter. This was an increase of roughly $600 million versus the prior year, mainly driven by stronger profit. CapEx spend was about $700 million in the quarter. We deployed $2 billion to shareholders in the third quarter, of which share repurchases accounted for $1.2 billion and nearly $750 million for our quarterly dividend payment. Earlier this year, we announced our sixth consecutive year of high single-digit quarterly dividend increase, and this year will mark 33 consecutive years of paying higher annual dividends to our shareholders. Our balance sheet remains strong. We have ample liquidity with an enterprise cash balance of $7.9 billion. In addition, there is $1.6 billion in slightly longer-dated liquid marketable securities to improve yields on our cash.
Now for outlook assumptions. Turning to Slide 15. I will start with the fourth quarter. End user demand remains favorable across all 3 primary segments, and the team is working diligently to deliver on our commitments for the year. At the same time, we are aware of potential headwinds presented by higher cost inflation, which we continue to monitor closely. For the fourth quarter, we anticipate moderate sales growth versus the prior year. As a reminder, we are lapping a strong quarter last year, which creates a tougher comparison this year.
Now let me walk you through each of our 3 primary segments. In Power & Energy, we anticipate moderate sales growth in the fourth quarter versus the prior year, as we lap a strong prior year fourth quarter and continue to ramp capacity. Volume growth is expected to be driven by continued strength in power generation, modest growth in oil and gas and moderate growth in industrial applications as it continues to recover. We also expect favorable price realization. 
In Construction Industries, we expect sales to be similar to the prior year. We anticipate the typical seasonal dealer inventory reduction to be roughly $1.6 billion, which compares to the decline of $600 million in the fourth quarter of 2025. As a result, we expect the year-over-year impact to be about a $1 billion headwind to sales volume in the fourth quarter against a backdrop of continued strong sales to users and industry growth. As a result, we expect sales volume in Construction Industries to be down modestly versus the prior year. 
However, we continue to expect favorable price realization in the fourth quarter. Despite the drawdown, we continue to expect dealer inventories at the end of the year to be higher than the prior year in anticipation of strong sales to users in 2027. In Resource Industries, we expect strong sales growth in the fourth quarter versus the prior year. Volume is expected to be driven by higher sales to users and services growth. We also anticipate favorable price realization. 
I will now provide some color on our fourth quarter margin expectations versus the prior year. At the enterprise level, we expect higher adjusted operating profit margin versus the prior year. This is primarily due to favorable price realization and the profit impact of higher sales volume. Excluding the impact of lower tariffs, we expect unfavorable manufacturing costs driven by higher freight as well as expenses related to our capacity expansions. SG&A and R&D expenses are also expected to be higher, driven by our continued investment in the strategic initiatives aligned with our 2030 goals. We anticipate tariff costs excluding IEEPA recoveries of around $600 million, which is similar to what we incurred in the third quarter, but roughly $200 million lower than what we incurred in the fourth quarter of 2025. We continue to expect about 50% of the tariffs to be incurred in Construction Industries and 25% in both Power & Energy and Resource Industries. 
Now for our fourth quarter margin expectations in our 3 primary segments. In Power & Energy, we anticipate favorable price realization and stronger volume to drive a higher margin percentage compared to the prior year. The higher margin compared to the prior year is expected to be partially offset by unfavorable manufacturing costs, including depreciation and expenses related to our capacity expansions, along with higher material and freight costs. We expect fourth quarter margin to be similar to the third quarter. 
In Construction Industries, we anticipate a higher margin percentage compared to the prior year, primarily due to the favorable price realization, which is partially offset by lower sales volume. Excluding the impact of lower tariffs, manufacturing costs are expected to be higher, driven by freight. We also expect higher SG&A and R&D related to our technology investments. Also, as a reminder, our Construction Industries' fourth quarter margin typically has a sequential step down from the third quarter. We expect this seasonality change to be slightly more than our typical average step down due to the expected lower sales volume, higher SG&A and R&D related to our technology and digital investments as well as higher freight costs.
In Resource Industries, we anticipate a higher margin percentage compared to the prior year, driven by favorable price realization and the profit impact of higher sales volume, partially offset by unfavorable manufacturing cost including freight and material. 
Now on Slide 16. Let me provide a few comments on the full year. As Joe mentioned, we continue to anticipate sales and revenues growth in the mid- to high teens for the full year 2026. Our strong full year sales and revenues expectations is supported by strong sales to users growth across all 3 primary segments driven by healthy end markets, strong order rates across all 3 primary segments driving our backlog growth, increased output from our capacity expansion plans which remain on schedule and a strong year of services growth.
Now for our adjusted operating profit margin for the full year. Compared to last year, we expect a higher adjusted operating profit margin, which reflects profit impact of higher sales and favorable price realization, partially offset by unfavorable manufacturing costs, including spend related to our capacity expansion, which includes higher depreciation expense as well as higher freight. We also expect higher SG&A and R&D. Excluding IEEPA tariff recoveries, our full year adjusted operating profit margin is expected to be near the bottom of our target range.
Excluding our reported year-to-date IEEPA tariff recoveries of about $520 million, we continue to expect full year 2026 tariff costs of around $2.2 billion. Our outlook does not include any additional IEEPA tariff recoveries in the fourth quarter. We now expect restructuring costs of about $300 million in 2026, which is on the low end of our prior range. Our estimated global annual effective tax rate remains approximately 23% for 2026, excluding discrete items. We also continue to expect MP&E free cash flow to be in the top half of our annual target range of $6 billion to $15 billion. Our CapEx spend for 2026 is now anticipated to be about $3.3 billion, which is slightly below our prior expectations of $3.5 billion. 
Now turning to Slide 17 to summarize. We delivered another very strong quarter, with year-to-date financial results tracking toward another record year for Caterpillar. Our end markets remain healthy with strong order rates and a growing backlog. We continue to drive improved profitability in a dynamic operating environment. We will remain disciplined and committed to operational excellence and the O&E model. We will continue to look for ways to invest efficiently. We will maintain a strong balance sheet and continue to return substantially all of our MP&E free cash flow to our shareholders through dividends and share repurchases over time. And finally, we will continue to execute our strategy for profitable growth. With that, we will take your questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Tami Zakaria from JPMorgan. Hearing no response, we'll go next to Rob Wertheimer with Melius Research.

**Robert Wertheimer** (Analysts):
I had a couple questions around power gen. And 2 quarters ago, you detailed some of the prime power projects you've done. I think you gave gigawatt numbers. Do you have any update there? Is prime power still expanding for you, either in general, if you have any update on gigawatts? And then you mentioned you're taking orders into '29. Does that imply that '28 is sold out? Are you selling out current capacity but leaving future capacity for future orders? Can you just sort of talk about how you manage backlog there?

**Joseph Creed** (Executives):
Rob, we still continue to see trending higher prime power, both turbines and reciprocating gen sets. I've had a handful of discussions with customers for prime power just in this last quarter. So a lot of quoting activity continuing to go on. And I think we'll continue to see that trend as we move into the future. We're not seeing anything different in that space. When it comes to orders and sort of backlog, if it's significant order in gas prime power, we're probably looking at 2029. 
I mean maybe some -- we'll probably still roll some diesel backup orders into 2028. We're not completely full. But we're still -- we have frame agreements in the pipeline that kind of convert to orders as we move over time. So again, we continue to have extended backlog. I'm happy that the backlog grew in all 3 segments. And what we're hearing from our customers is they still want more from us if we can get them more power. So we're trying to ramp as quickly as we can and still hit our customers' needs.

**Operator** (Operator):
We'll go next to Tami Zakaria at JPMorgan.

**Tami Zakaria** (Analysts):
Can you hear me?

**Joseph Creed** (Executives):
We can.

**Tami Zakaria** (Analysts):
So just wanted to touch on that backlog comment. I think I heard Jill say that the engines and turbine orders are now going as far out as 2029, 2030. So is it that the total orders you receive in the quarter are primarily for the out years? Or are the majority of the orders booked still for the next 12 months? And given the new capacity that will be coming online, when would you expect this record backlog to start stepping down? Or is it the new normal for the backlog magnitude?

**Joseph Creed** (Executives):
Tami, thanks for the question. So I want to be clear. I mean we're taking our orders into '29. We have some in '29 and 2030. We still have more to fill. And this is a bit of a complicated question because it's going to depend on the product, right? So for a large reciprocating engines and turbines we're definitely extended out into late '28, into '29. Smaller gen sets, smaller engines, obviously lead times are much shorter than that. And on the machine side of the business, the backlog grew in all 3 segments, aside from a couple of products where we're ramping production and operationally trying to ramp production and even in those, we're not extended near as far.
I would like to produce and get our production ramp closer to STU. So when we look at the backlog, we want to make sure we're looking at the backlog in the context of sales to users and order rates and the entire system and how it works. So if we can -- sales to users stay healthy, which is what we're expecting, and we can produce more product, we'll continue to take orders, but I would like to see the backlog. I mean if we can get it to even come in on the machine side because we can keep up, that would be a good thing.
And I also think if you -- when you look at, we've had a few quarters of backlog growth. I think we'll continue to see some backlog growth, but it's going to really depend. I mean customers have time to place orders and sort of digest what we have. And so I don't know that quarter-to-quarter, it's going to be something we look at as the singular metric as we start to move out, especially as we get extended. We're continuing to do long-term planning with our big data center customers and prime power customers.
We're seeing demand for cloud compute and our backup power continue to be strong. And then AI obviously comes in on top of that in the prime power numbers. So with those frame agreements, we have a line of sight past the backlog, and we continue to talk to our customers. And then on prime power, those are big projects, and I think they get negotiated individually and those can come in lumpy in the backlog, as can mining orders. So I'm really pleased with the backlog growth we saw in this quarter. It was broad-based. Oil and gas, power gen, RI and CI. So we have good momentum.

**Kyle Epley** (Executives):
And just for a reference, we expect 58% of our backlog is expected to be sold within the next 12 months. That's comparative to 59% last quarter.

**Operator** (Operator):
We'll move next to Jamie Cook at Truist Securities.

**Jamie Cook** (Analysts):
I guess my question, Joe, is just around your longer-term margin framework that you guys have put out there. You guys have done an exceptional job, but the margins have been pushing towards the lower end. Obviously, we have tariffs and inflationary pressures, et cetera. But like what do you think with sort of capacity coming online and price costs in your backlog, what's like a reasonable time for us to assume we can get back towards like the mid- to high end of your longer-term target range, and what would be the major drivers behind that? And then last, is there any way you can help us frame how much incremental capacity is coming online in 2027 on a dollar basis if -- or any way you could frame it?

**Joseph Creed** (Executives):
Jamie, as far as the margin target range, we -- I've said many times I want to operate towards the middle of that range. The sales are growing at a really good clip, which is a good thing, and we've been able to, as best we can, keep up with customer demand, and it's a progressive target. So as our margins are going up, the target continues to increase, so we're kind of skipping along the bottom. I would expect, and we'll talk to you a lot more about 2027 in the next quarter, that we start to claw our way off the bottom of that margin target range as we go forward while we still try to keep up with demand.
We also are trying to do this with the tariff headwind, in a smart way where we're not slowing down investments that would impact the growth and the momentum we have in the business. So I'm happy with the progress we've made. Our margins continue to go up as our volume goes up. And over the next couple of years, we want to try to work our way back to the midpoint.

**Operator** (Operator):
Next, we'll move to David Raso at Evercore ISI.

**David Raso** (Analysts):
I'm trying to figure out the revenue sequentially and what it means when we think about '27 revenue. If you look at the sequential revenue 3Q to 4Q, let's use the guide for the full year, mid- to high teens, right, let's call it, 17%. It implies that the fourth quarter, even if I give you back the extra $1 billion, right, the headwind of the dealer inventory, it implies the revenue is barely up sequentially. And over a long period of time, fourth quarter is up 5% to 10%. 
I mean it moves around, but a year where you're adding capacity, it's a big focus. And I mean demand is there. You speak to it in retail, even the backlog is still pretty solid. Just trying to understand, is there some capacity issue, supplier issue? Why is the revenue growth so modest sequentially, especially given the capacity adds? And any implications on how to think about '27 top line would be appreciated as well.

**Joseph Creed** (Executives):
As we said in the prepared remarks, I mean, on Power & Energy, it's really paced by capacity and timing of customer deliveries. So we're not seeing anything different in the business that we would say would impact the fourth quarter, but it is hand to mouth, right? The teams are working really hard. We had a test cell go down for a little bit in the third quarter, that we were able to overcome, but there's no slack in the system. And then as you mentioned, and we've kind of said we're going to have the inventory drawdown in CI, which seasonally isn't unusual. It's going to be a little different than the patterns that we had last year.
And then RI, we are, as we mentioned, we think operationally we're trying to ramp. So we're going to obviously get as much product out as we can on large mining trucks and some of those products. But I don't think there's, other than typical seasonality and things that we've talked about on trying to ramp production, we're pretty confident. And this is in line -- our third quarter results came in line as we expected. We haven't really changed our view for what we plan to do in the fourth quarter.
And as you think about how we're going to finish the year, again, we'll talk to you more about 2027 in January, but our backlog continues to increase, we have longer line of sight. We are drawing down CI inventory, $1.6 billion. We're going to finish the year with almost $700 million more of inventory in place than we finished 2025 heading into 2026. So we feel good about where we sit right now.

**Kyle Epley** (Executives):
And David, I just -- this is Kyle. Just to remind you, and I said in my prepared remarks, when we talk about the growth, it's off a really tough comparison versus 4Q last year, just from a consolidated level and then especially from a Power & Energy standpoint. But going into 2027, the dealer inventory increase in CI, we still expect really strong STUs across all 3 primary segments in 4Q going into 2027.

**Operator** (Operator):
We'll take our next question from Michael Feniger at Bank of America.

**Michael Feniger** (Analysts):
And just kind of following up on David Raso's question. The Q4 implying the moderate sales growth, you guys talked about the dealer destock. I know your target is 6% to 9% CAGR, on the revenue growth side, some years higher, some years lower to get to that average. Just with the backlog, with where it is, the framework agreements, and I understand there's a quarter dynamic with destocking. But why would the setup for '27, should we be thinking that we're above that 6% to 9% CAGR at the higher end based on where retail sales are and where we're seeing it? What would hold us back to be in that line? I'm just kind of curious what the setup and the building blocks would look like for next year on that.

**Joseph Creed** (Executives):
Yes. So 2027, again, we don't have much different than how I answered David's question, right? I mean we're finishing the year strong. We had, as Kyle mentioned, a really strong fourth quarter last year. So when we say moderate growth year-over-year, some of that's a comp issue. We're paced on capacity on Power & Energy. We think we'll continue to increase capacity. It's not a cliff event, as we've said. So every quarter, we try to get more and more product out. We expect to continue that. When it comes to the dealer inventory drawdown, one, dealers are independent businesses, just to remind you, we do work with them. And we want to make sure we have the right inventory in the right place in the right regions of the world with the right products. 
And we do feel like we're in a good positioning heading into 2027, finishing the year with more dealer inventory in CI than we finished last year. So RI orders continue to go up. We've had 3 really strong quarters in a row of orders in RI. Having some operational challenges and inefficiencies as we ramp, but I think we'll continue to work those and get those behind us. So we're pretty confident and bullish in where we sit right now as we watch things. We're focused on delivering a strong fourth quarter and a strong finish to the year, and we'll talk to you guys more about '27 in January.

**Operator** (Operator):
Next, we'll go to Chad Dillard at Bernstein.

**Charles Albert Dillard** (Analysts):
Just wanted to spend some time on the mining business. I recall from, beginning of this year, you talked about orders being the highest, I think, since 2012. So I was wondering if you could give an update on how that's trending. Talk about what's driving it, more refurbishment versus replacement. And if you can just give a little bit more color on some of the ramping challenges that you're seeing. And do you have a line of sight to seeing that being resolved in the next quarter or so?

**Joseph Creed** (Executives):
We've had 3 really good order quarters in a row for RI, which we're really happy about. As we mentioned in prepared remarks, driven a lot by mining and both heavy construction. But in mining, in particular, copper and gold, we're starting to see activity in the Canadian oil sands. Services are continuing to grow, so customers are using the fleet, and we're seeing aftermarket rebuilds continue to happen and customers are starting to order equipment. So that's all a really good sign. We've -- as we try to ramp, particularly in large mining trucks, is where we've been actually increasing capacity at some of our factories where we can inside our 4 walls and working with the supply base to get ramped up. 
They're just sort of, I would say, as normal growing pains and operational challenges when you're increasing capacity and trying to get product out the door. So we'll continue to work those. I think we'll get them behind us as we move forward. But it's a great sign that we've had this strength in orders as we've been waiting for orders to kind of pick up in mining for quite a while. So we're really happy with what we've seen in the first 3 months of -- or the first 3 quarters of this year.

**Operator** (Operator):
We'll go next to Jerry Revich at Wells Fargo Securities.

**Jerry Revich** (Analysts):
Congratulations to Denise and Derrick. Joe, Kyle, I wanted to ask in terms of as you think about the production slots and lead times out to '29, '30 for turbines and large reciprocating engines. As you folks look at the permit requirements out that far and the counterparty has given some angst about credit in the market, can you just talk about if you've seen any shifts in timing in backlog? And I don't know if you can share what proportion of those production slots are backed by hyperscalers, just to build comfort around the moving pieces, given all of the news on the permitting side.

**Joseph Creed** (Executives):
Yes. I mean I don't think we would quantify hyperscalers versus colos versus others or IPPs, but we work with all of them. Typically, when we roll orders from pipeline into backlog and working with other customers, we generally have line of sight to the project that they're working on. Our teams are working closely with customers. We continue to see strong oil and gas activity as well for large engines. So as we think of this, we've always tend to move, if we can, some slots around, to meet customer needs to deliver on their projects. And we've been doing that the last couple of years because we want to make sure we meet our customers' time line, but also no need to get product there early. It allows us to meet more customer demand if we're getting it when they need it. And we haven't seen really any significant change in how we're working with our customers to deliver projects so -- and product to get their project time lines.
So we continue to talk to our customers. We stay close to them. We'll follow their lead, but we're not seeing significant changes. But as I said earlier, as we're extended pretty far out, I mean this is going to be -- this is unusual for us. Typically, we've only had 12 months or less line of sight to our backlog. And now in particularly this situation, customers are placing orders pretty far out there. We have a lot of quoting activity in '29, '30. We've got some quoting activity even beyond as we talk to customers. But I think they have time to firm up those orders and place the firm orders and move them into our backlog. So we'll see our backlog kind of move in a lumpy way moving forward. But we'll continue to watch sales to users, we'll continue to watch order rates, our backlog, all in conjunction together and stay close to our customers as we move into the end of this year and into next year.

**Operator** (Operator):
We'll move to our next question from Mig Dobre at Baird.

**Mircea Dobre** (Analysts):
Yes. And just to follow up on these last comments, if we're kind of looking at backlog progression or maybe looking at it from the perspective of book-to-bill, it was as high as 1.7 earlier this year decelerated to about 1.3 in a quarter here. As you look at the fourth quarter, based on what you know, how should we think about book-to-bill here? And given that you're taking now orders into '29, maybe even '30 for solar, is there some kind of slippage in terms of bookings given how constrained from a capacity we seem to be?

**Joseph Creed** (Executives):
Yes. I mean one of the things you have to look at book-to-bill as we continue to increase production as well. So our sales are continuing to go up. And as I mentioned, for certain products, when you look at our backlog, all 3 segments are in there and all 3 have been growing. There are some of them we'd like to actually bring in and increase production. And so as we continue to ramp book-to-bill, we'll sort of move around.
And then in Power & Energy, again, we're extended way longer than we've ever been, so we continue to talk to our customers. That's why it's great to have the frame agreements and sort of the pipeline view beyond what's in the backlog. That's what we're using to plan with customers and those orders will roll into the backlog at different times as we continue to move forward. RI and prime power projects, as I mentioned earlier, will also probably come in, in not a smooth sequential fashion, they'll be lumpy depending on when those orders get placed because they're typically big orders.
So I think we'll continue to talk to our customers. And again, you can't just look at one metric like backlog growth in a quarter or book-to-bill in a quarter. It has to be taken into context with continued momentum in sales to users, our ability to produce more and get more product out the door. There's a lot of things that we're watching on the health of the business more than just book-to-bill and a singular backlog number.

**Operator** (Operator):
Our next question comes from Kyle Menges at Citi.

**Kyle Menges** (Analysts):
Great. I would love to hear from you guys how the landscape might be changing a little bit as far as the demand you're seeing in the data center market. Maybe you can talk a little bit about how you're seeing things evolve in demand for turbines versus nat gas recips and then for diesel backup. And then also, just as you're booking into the latter part of this decade and having a lot of discussions, it sounds like a lot of quoting activity to 2030 and even beyond, would love to get just some sense of how you could see your mix shifting, maybe that mix of prime versus backup, where you've been versus maybe where that mix is heading as you look to 2030.

**Joseph Creed** (Executives):
Yes. As we talk to our customers, we've not seen really any change since the last quarter in our discussions with customers. We continue to see momentum in standby diesel backup, which has been the growing base of our business for quite a while, before even really AI started to accelerate the growth even more, driven by a lot of demand for cloud compute. AI has obviously accelerated that. When it comes to prime power versus diesel, that's one of the things that's good about the capacity we've put in place. It's pretty fungible as long as we have line of sight to those orders. If you get the largest 3520, that one, they're probably a little more extended on the gas 3520K. But keep in mind as well, the capacity we have in place and the momentum we have, it's more than just power generation.
We continue to see the momentum there, oil and gas, and I think we're going to move a lot of natural gas in the next few years and are really strong in gas compression, both at Solar Turbines and in our reciprocating engine business. Demand is there for that. It's for marine and large engines also go into our mining products as well. So as the mining picks up, we're excited about making sure that we can serve those customers. And really, when you talk about aside from diesel standby, all these other applications, we -- as the field population grows, we need to be able to support customers in the aftermarket and grow services. So the capacity is all aligned to what we plan to have in place to meet our goals in 2030.

**Operator** (Operator):
We'll go next to Kristen Owen at Oppenheimer.

**Kristen Owen** (Analysts):
We've talked a lot about the synchronous growth within the portfolio, but I'm hoping you can maybe double click for us on the construction side. You called out the tough comps here in the fourth quarter, but backlog growth in construction, can you maybe help us understand or give us some color on the underlying demand? How much of that growth is going into rental for your own fleet versus third parties and maybe some of those other sources of demand outside of rental and mega projects?

**Joseph Creed** (Executives):
Yes, we've seen really strong order rates, strong STUs continue in construction. So we're really excited about the progress we have there and the initiatives that we've announced. I think it's the seventh consecutive STU growth quarter. And we'll see as we move forward, but our goal and our strategy really is to get customers in the cabs of Cat machines, whether they want to rent or lease or buy, and we're seeing customers do all 3. We're really excited, and we were heavy in the fleet load in the Major Projects fleet in the third quarter.
And basically, as soon as we can get fleet on the ground, they're moving to projects. So I think that's going to be a great initiative for us to continue to drive rental. And the point of that is to supplement. If you think about that strategy, the Major Projects JV, it supplements the local dealer where they wouldn't be able to get on -- have the scale to get to projects before. So it drives not only Major Projects, but allows each of the individual dealers to be in more rental deals as they move forward as well.
So we're seeing great progress there. We're excited about Cat Compact and how we're taking care of customers in the growing compact equipment industry. And in particular, we've seen it's large infrastructure projects, high IIJA spending still has a lot of money left to be spent and projects left to be completed. I'm confident we'll continue to prioritize critical infrastructure as we move forward. Data centers obviously have a little bit of a rollover into CI as well. And so we're seeing really good momentum with the CI team. We're getting closer to customers than we ever have, and it's showing in their results. We're seeing strength in all 3 of our segments right now, which is really exciting.

**Operator** (Operator):
And today's final question comes from the line of Stephen Volkmann from Jefferies.

**Stephen Volkmann** (Analysts):
Joe, I'm just wondering, any update on the 10-megawatt MaK restart that you're doing? And how we should think about that kind of ramping going forward?

**Joseph Creed** (Executives):
Yes, we plan to ship our first units here in the fourth quarter, and we'll continue to ramp as we go through next year on restarting the 10-megawatt MaK engine and using it in power generation. I think that's going to be a great opportunity for us as we move into -- we'll get started here in the fourth quarter, but as we move into 2027, so everything is on track with that program. 
All right. Well, that was the last question. So I just want to say thanks for joining us today. We really appreciate your questions. And I'm really proud of our team, the Caterpillar team's strong performance in what's been a pretty dynamic environment as we try to ramp production, add capacity and take care of our customers. We're well positioned to deliver a strong year, and we'll continue creating long-term value for our customers and shareholders. So thank you. I'll turn it back over to Alex.

**Alex Kapper** (Executives):
Thank you, Joe, Kyle, Stephanie and everyone who joined us today. A replay of our call will be available online later this morning. We'll also post a transcript on our Investor Relations website as soon as it's available. You'll also find a third quarter results video with our CFO and an SEC filing with our sales to users data. Visit investors.caterpillar.com and then click on Financials to view those materials. If you have any questions, please reach out to me or Ryan Coleman. The Investor Relations general phone number is (309) 675-4549. Now let's turn it back to Audra to conclude our call.

**Operator** (Operator):
Thank you. And that concludes our call. Thank you for joining. You may all now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CAT_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜CFO｜guidance：全年銷售與營收成長預期上調至中高十幾%（原話："sales and revenues growth in the mid- to high teens for the"）
- 2026-08-04｜CEO｜guidance：全年調整後營業利益率高於四月預期；排除 IEEPA 退稅後接近目標區間底部（原話："we expect full year adjusted operating profit margin to be"）
- 2026-08-04｜CFO｜guidance：全年關稅成本預估約 22 億美元，在先前區間低端（原話："of around $2.2 billion or at the low end of the range we"）
- 2026-08-04｜CFO｜guidance：Q3 關稅成本預估約 6 億美元（原話："We anticipate tariff costs of around $600 million"）
- 2026-08-04｜CFO｜guidance：財測不含下半年任何額外 IEEPA 退稅（原話："Our outlook does not include any additional IEEPA tariff"）
- 2026-08-04｜CFO｜guidance：MP&E 自由現金流預期上調至年度目標區間（60–150 億）上半部（原話："expect MP&E free cash flow to be in the top half of our"）
- 2026-08-04｜CFO｜guidance：2026 年資本支出約 35 億美元，與先前預期相近（原話："Our CapEx spend for 2026 is anticipated to be approximately"）
- 2026-08-04｜CEO｜guidance：全年服務營收成長率高於先前展望（原話："Services revenues are also expected to grow at a higher rate"）
- 2026-08-04｜CEO｜guidance：下半年產能擴充將提高產出（原話："we expect to increase our throughput in the second half of"）
- 2026-08-04｜CFO｜guidance：Q4 預期 CI 經銷商庫存較典型地下降逾 10 億美元，年底庫存高於去年（原話："We plan to end the year higher than last year"）
- 2026-08-04｜CFO｜guidance：Resource Industries Q3 利潤率預期與去年相近（原話："we anticipate a similar margin percentage"）
- 2026-08-04｜CFO｜margin：Q2 認列 3.92 億美元預期 IEEPA 退稅，多數在 corporate items（原話："we recognized $392 million in expected IEEPA tariff"）
- 2026-08-04｜CFO｜margin：Q2 關稅成本約 4 億，低於四月提供的 7 億估計；原因為先前已發生關稅的計算調整（原話："favorable compared to the $700 million estimate we provided"）
- 2026-08-04｜CFO｜margin：Q2 各 segment 受關稅影響的利潤率bp 拆解（P&E 90bp）（原話："Segment margins were impacted by 90 basis points in Power &"）
- 2026-08-04｜CFO｜margin：P&E Q2 利潤率 24.6%，年增 250bp（原話："margin of 24.6% was an increase of 250 basis points"）
- 2026-08-04｜CFO｜margin：P&E 製造成本受產能擴充支出（含折舊）影響（原話："Higher manufacturing costs were impacted by spend related"）
- 2026-08-04｜CEO｜margin：下半年運費與折舊面臨壓力的說法（原話："We might see a little pressure on freight in the back half"）
- 2026-08-04｜CEO｜commitment：管理層表示有信心長期處理關稅衝擊，目標在利潤率目標區間中點附近運作（原話："I'm confident that we'll manage the impact of tariffs over"）
- 2026-08-04｜CFO｜commitment：承諾持續將幾乎全部 MP&E 自由現金流透過股息與買回還給股東（原話："substantially all of our MP&E free cash flow to our"）
- 2026-08-04｜CFO｜capital_allocation：Q2 買回約 15 億美元，其餘為股息，合計回饋 22 億（原話："Share repurchases accounted for about $1.5 billion"）
- 2026-08-04｜CFO｜capital_allocation：6 月宣布股息增加 8%（原話："In June, we announced an 8% dividend increase,"）
- 2026-08-04｜CEO｜product：重啟 10 MW 中速燃氣往復式引擎，約 1.5 GW 產能，預計 Q4 開始出貨（原話："We plan to bring about 1.5 gigawatts of capacity back online"）
- 2026-08-04｜CEO｜product：該產品 2022 年曾停產，重啟敘事不同於前期（原話："In 2022, we stopped manufacturing this product"）
- 2026-08-04｜CEO｜product：回答分析師：10 MW 機型未計入 2030 年 65 GW 目標（原話："included in the 65. But again, it's a lower volume."）
- 2026-08-04｜CEO｜product：Wamego 工廠改造為渦輪機產能，12 個月內完成（原話："converted the facility in under 12 months"）
- 2026-08-04｜CEO｜product：部分客戶詢問將柴油備用電源改用較小 C32 平台（原話："moving down to the C32 platform"）
- 2026-08-04｜CEO｜customer：管理層稱 AI／資料中心需求無客戶放緩（原話："no one is slowing down at the moment"）
- 2026-08-04｜CEO｜customer：管理層稱未見客戶退出需求（原話："we haven't seen any customers back off of demand"）
- 2026-08-04｜CEO｜customer：開始接受 2029、2030 年訂單（原話："we're starting to take orders into '29 and '30 already."）
- 2026-08-04｜CEO｜customer：油氣積壓訂單年增接近 2 倍（原話："nearly 2x bigger"）
- 2026-08-04｜CEO｜customer：燃氣 prime 與大型引擎交期已排到 2028 後段（原話："we're into '28 in gas prime, late '28 for sure"）
- 2026-08-04｜CEO｜customer：交期延長的說法（原話："We've seen, obviously, lead times start to extend here."）
- 2026-08-04｜CEO｜customer：遠期訂單通常附價格調整條款（原話："we do typically have price escalators on those"）
- 2026-08-04｜CFO｜customer：Cat Financial 逾期率 1.31%（原話："Past dues were 1.31% in the quarter"）
- 2026-08-04｜CEO｜customer：租賃載入成為 CI 銷售給用戶成長的較大部分（原話："rental loading has definitely become a bigger piece"）
- 2026-08-04｜CEO｜competition：Major Projects 為經銷商持有的全國性租賃合資公司（原話："a specialized fully Cat dealer-owned rental joint venture"）
- 2026-08-04｜CEO｜risk：地緣政治不確定性（原話："despite ongoing uncertainty due to geopolitical events"）
- 2026-08-04｜CEO｜risk：中東持續受挑戰，但預期對 EAME 銷售給用戶影響有限（原話："While the Middle East continues to be challenged"）
- 2026-08-04｜CEO｜capital_allocation：新渦輪產能提供者回收期說法：本十年底前現金回收（原話："We said last time we'll have cash payback by the"）
- 2026-08-04｜CEO｜customer：CI 積壓非供給受限，部分取決於產出追上需求（原話："somewhat of a function of us being able to produce to demand"）
- 2026-08-04｜CEO｜customer：住宅等其他 CI 領域疲弱，被視為潛在上行空間（原話："that provide some potential upside for us"）
- 2026-08-04｜CEO｜product：P&E 服務成長多數在 2030 年之後（原話："There will be some between now and 2030"）

### 問答異常語氣（迴避／改口／保留）
- CAT_Q2_2026_Earnings_Call_20260804.md｜問：Jamie Cook：積壓成長中大型專案（如 PROPWR）與廣泛訂單的組成，及 P&E 增量利潤率來源｜答法：未給拆解數字，稱「we don't really kind of talk about the specifics」，改談各 segment 訂單特性與關稅、運費、折舊因素
- CAT_Q2_2026_Earnings_Call_20260804.md｜問：Angel Castillo：10 MW 引擎首批訂單規模與增量成本，及遠期訂單定價｜答法：確認已有首批訂單但未給規模；稱投資「minimal」，定價回答僅提及價格調整條款，未給幅度
- CAT_Q2_2026_Earnings_Call_20260804.md｜問：Rob Wertheimer：2027、2028 是否已售罄、是否保留產能檔期｜答法：未直接說是否售罄，改述交期（gas prime 2028 下半至 2029）及會優先照顧長期油氣客戶、調整排程
- CAT_Q2_2026_Earnings_Call_20260804.md｜問：Mig Dobre：P&E 服務與售後市場的目前規模與占比｜答法：未給規模或占比，只談定性成長機會，主要在 2030 年後

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
{"date":"20260805","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"資料中心自備發電需求在 2029 年前不中斷，且 CAT 能把它轉成 P&amp;E 分部 2026-2029 年化 ≥ 15% 的營收成長"},{"id":"H2","text":"非住宅營建與礦業資本支出在 2027-2028 不同時反轉——CI＋RI 合計約佔營收 55%，需要至少一邊撐住"},{"id":"H3","text":"CAT 能把 2026 年約 20-21% 的調整後營益率，在產能爬坡、折舊上升與 $2.2B 關稅成本下維持到 2028"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"資料中心監理的州級收緊（但聯邦在鬆綁，方向相反）：紐約州 2026-07-14 通過全美首個資料中心建設暫停令（Responsible Data Center Development Act，20MW 以上州級許可暫停一年，參院 44-16、眾院 102-39；州長另以行政命令針對 50MW 以上超大規模，最長一年，待通用環評完成），六週內 30 多州提出 300+ 件相關法案。反向抵銷項：聯邦層級同期在降低燃氣渦輪的空氣許可負擔（2026-01 新版 NSPS；2025-09 與 2026-05 指引允許動工先於許可核發）。故本風險的正確形狀是「州與聯邦方向相反的監理拉鋸」，不是單向利空"},{"id":"R2","text":"全行業產能同步落地壓垮定價權（分層：往復引擎風險高、渦輪風險低）：CAT 大型往復引擎產能 2030 擴至 2024 近 3 倍、渦輪 2.5 倍；GE Vernova 目標 2030 年產 30GW（現 backlog 116GW、自稱「大致賣光到 2030」）；Cummins 投資 $450M 增 20GW 至 2030 年 55GW 高馬力產能，並訂下 2030 年 $9B 資料中心營收目標；Mitsubishi Power 產能翻倍；INNIO、Wärtsilä 同步擴產。分層依據：重型渦輪的真瓶頸在轉子鍛件與熱端葉片鑄件（全球僅少數幾家供應，製程無法快速擴產，交期已達 5-7 年），故渦輪線的緊缺較持久；而 CAT 的 P&amp;E 成長主體是往復引擎，該線的邊際供給成本由 CAT 自己證明極低（MaK 平台以「幾乎四捨五入等於零的投資」復產 1.5GW、Wamego 廠 12 個月改建完成）"},{"id":"R4","text":"替代技術在超大規模客戶端滲透：Bloom Energy 與 Oracle 於 2026-04 把合作擴大至 2.8GW 固態氧化物燃料電池（部署期 &lt;1 年、效率較燃氣渦輪高 10-30%）——單一合作案規模已超過 CAT 在行為表後 prime power 已公告專案的全部 3.6GW。另有天然氣供應與管線瓶頸（已申報的資料中心天然氣需求約 125GW，2026-01 一次 20% 需求衝擊使 Henry Hub 價格暴漲），可能把部分客戶推向非燃氣方案"},{"id":"R3","text":"CI／RI 雙循環同時反轉：IIJA 授權於 2026-09-30 到期且再授權延宕；美國非住宅營建支出 2026 年 6 月 $745.3B SAAR、已「大致持平」；礦業資本支出對銅金價格高度敏感"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"價格 ≤ $700（FY27E 我方 build 21x，Base 年化 IRR 回到約 9%）且 backlog 未連 2 季 QoQ 淨下滑；或 FY27E 共識升至 ≥$36 而股價未過 $950（倍數自然消化）","irr_base_pct":4.3,"ev5y_pct":7.3,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":0.75,"ev5y_pct":7.3,"irr_base_pct":4.3,"max_dd_pct":-60.0,"bull_5y_price":1276.0,"bear_5y_price":392.0,"p_bull_pct":23.0,"p_bear_pct":30.0,"rearm_trigger":"價格 ≤ $700（FY27E 我方 build 21x，Base 年化 IRR 回到約 9%）且 backlog 未連 2 季 QoQ 淨下滑；或 FY27E 共識升至 ≥$36 而股價未過 $950（倍數自然消化）","price_at_dd":876.54,"archetype":"循環/商品","cycle_position":"晚循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAT_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
