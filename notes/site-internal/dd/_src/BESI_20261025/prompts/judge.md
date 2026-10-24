你是 stock-analyst **v20 判斷 agent**，標的 BESI（20261025）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"BESI","date":"2026-10-25","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BESI_20261025/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BESI_20261025/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_ifrs","label":"營收（IFRS）","value":283.4,"period":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","unit":"€M（YoY +113.6%、QoQ +13.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/"}},{"id":"f_kpi1_orders","label":"訂單 orders","value":342.6,"period":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","unit":"€M（YoY +96.1%、QoQ +17.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/"}},{"id":"f_kpi2","label":"毛利率","value":65.2,"period":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/"}},{"id":"f_kpi3","label":"淨利","value":107.2,"period":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","unit":"€M（YoY +323.7%、QoQ +20.4%；淨利率 37.8%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/"}},{"id":"f_kpi4","label":"營業費用","value":55.1,"period":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","unit":"€M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/"}},{"id":"f_kpi5","label":"期末淨現金","value":246.6,"period":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","unit":"€M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/"}},{"id":"f_kpi6_q4_26","label":"Q4-26 指引","value":"營收 持平±5%（相對 Q3 €283.4M）；毛利率 63–65%；營業費用 +5–10%（相對 €55.1M）","period":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","unit":"文字","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/"}},{"id":"f_kpi7_hybrid_bonding","label":"hybrid bonding 累計需求／訂單","value":"累計單位需求 >215 台；YTD-26 hybrid bonding 訂單較 FY2025 翻倍以上","period":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","unit":"文字","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3-2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-22","period":"2026-10-22","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-22"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_besi_gross_margin_pct","label":"BESI 毛利率","value":64.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BESI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_besi_operating_margin_pct","label":"BESI 營業利益率","value":36.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BESI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_besi_fcf_margin_pct","label":"BESI FCF 利潤率","value":23.08,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BESI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_klic_gross_margin_pct","label":"KLIC 毛利率","value":48.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLIC.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_klic_operating_margin_pct","label":"KLIC 營業利益率","value":13.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLIC.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_klic_fcf_margin_pct","label":"KLIC FCF 利潤率","value":4.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLIC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_042700_ks_gross_margin_pct","label":"042700.KS 毛利率","value":57.35,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.042700.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_042700_ks_operating_margin_pct","label":"042700.KS 營業利益率","value":42.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.042700.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_042700_ks_fcf_margin_pct","label":"042700.KS FCF 利潤率","value":18.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.042700.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amat_gross_margin_pct","label":"AMAT 毛利率","value":49.4,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amat_operating_margin_pct","label":"AMAT 營業利益率","value":31.09,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amat_fcf_margin_pct","label":"AMAT FCF 利潤率","value":18.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":145.1,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-42.1,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_rsi14","label":"RSI(14)","value":30.44,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":2.27,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.85 → 4.96）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.55,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.31 → 7.27）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-1.59,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.46 → 9.31）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":4.96,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":7.27,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":9.31,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-07-30 → 2026-10-24","unit":"%","basis":"FY1 共識 EPS 4.96 → 4.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":29.25,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 4.96，分子＝快照價 145.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.089,"period":"2026-10-25","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-25"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-10-25","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 145.1 / W52 197.59 / W104 156.63 / W250 116.99 / W250 13週斜率 1.49%"},{"id":"f_ma_w52","label":"52 週均線","value":197.59,"period":"2026-10-25","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":156.63,"period":"2026-10-25","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":116.99,"period":"2026-10-25","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.49,"period":"2026-10-25","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"TrendForce 2026-03：BESI 仍居混合鍵合機台首位，但 Hanmi、Hanwha Semitek、LG、SEMES、ASMPT 皆在建立混合鍵合能力，競爭開始浮現；未見任何對手 2026 年取得具名客戶混合鍵合訂單。","source":"TrendForce News 2026-03-13 Hybrid bonding leader BESI reportedly draws takeover interest","url":"https://www.trendforce.com/news/2026/03/13/news-hybrid-bonding-leader-besi-reportedly-draws-takeover-interest/","excerpt":null,"as_of":"2026-03-13","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Bits&Chips：BESI 執行長表示全球有約二十款鍵合機在開發，並出現數家中國業者；Canon 目標 2026 推出、LG 目標 2028。","source":"Bits&Chips: Besi leads hybrid bonding race with twenty players chasing","url":"https://bits-chips.com/article/besi-leads-hybrid-bonding-race-with-twenty-players-chasing/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261025","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"報導稱 ASML 正開發混合鍵合機台，挑戰 BESI；BofA 認為不會假設其取得顯著份額；ASML 未公布產品或時程。","source":"The Next Web: ASML's chip packaging move threatens Besi shares, Bank of America says; Dealroom 轉載","url":"https://thenextweb.com/news/besi-asml-hybrid-bonding-dutch","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"BESI 2026 Q1 訂單 2.697 億歐元，年增逾一倍，營收 1.849 億歐元年增 28.3%，主因混合鍵合需求；Yole 分析師稱 Besi 為該領域領先者。","source":"Bits&Chips: Besi sees orders double on hybrid bonding demand","url":"https://bits-chips.com/article/besi-sees-orders-double-on-hybrid-bonding-demand/","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261025","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Hanmi 在 HBM 熱壓(TC)鍵合機約占 71.2%（36Kr），並規劃混合鍵合產線；ASMPT 稱在 TCB 市場約 35–40% 份額。此為 TCB 非混合鍵合。","source":"36Kr / Tech Investments HBM die bonding semicap outlook","url":"https://www.techinvestments.io/p/hbmdie-bonding-semicap-outlook","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"某次要網站估 BESI 高階混合鍵合份額約 75%（2025-12），但中階高量 die attach 份額低於 10%；另有來源稱 die attach 份額 42%／49%，各來源互相矛盾，無可靠對手份額數據。","source":"dcf-analysis.com BESI SWOT; tspasemiconductor substack","url":"https://dcf-analysis.com/products/besias-swot-analysis","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Bits&Chips 評論：TSMC 為 Besi 目前最重要客戶，預期將導入第二家 hybrid bonding 供應商（評論，非確認報導）；ASMPT、Süss、Shibaura 已出貨 hybrid bonding 設備","source":"Bits&Chips - Besi's blue ocean is slowly turning redder","url":"https://bits-chips.com/article/besis-blue-ocean-is-slowly-turning-redder/","excerpt":"Serious players like ASMPT, Süss and Shibaura are already shipping hybrid bonding systems there. On top of that, four companies in Korea alone are competing for the favor of SK Hynix and Samsung in particular.","as_of":"2026-06-01","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"TrendForce：韓國 LG Electronics、SEMES、Hanmi、Hanwha Semitech 與 ASMPT 正建立競爭性 hybrid bonding 能力；SK hynix 於 2026-03 訂購 Kinex 系統","source":"TrendForce News 2026-03-13","url":"https://www.trendforce.com/news/2026/03/13/news-hybrid-bonding-leader-besi-reportedly-draws-takeover-interest/","excerpt":"The report notes that several Korean companies including LG Electronics, SEMES, Hanmi Semiconductor and Hanwha Semitech are developing related systems, while Singapore-based ASMPT is also working to build capabilities in the technology.","as_of":"2026-03-13","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"BESI 混合鍵合客戶數由 2025 年底 15 家增至 2026 Q2 底 21 家，應用擴及邏輯、記憶體、CPO（客戶數，非營收集中度）","source":"BESI Q2-26 and H1-26 Results (GlobeNewswire via datacentremagazine)","url":"https://datacentremagazine.com/globenewswire/3331898","excerpt":"Hybrid bonding customer adoption increased from 15 at year end 2025 to 21 at the end of Q2-26.","as_of":"2026-07-23","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2026 Q1 混合鍵合成長主要來自單一客戶超預期的產能建置，顯示單一客戶訂單可左右單季","source":"debelegger.nl 分析（引述 BESI Q1-26 說明）","url":"https://www.debelegger.nl/post/besi-aandeel-hybrid-bonding-orders-marges-waardering-2026","excerpt":"larger-than-anticipated capacity build this quarter by a customer","as_of":"2026-04-30","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Besi 2026年6月將長期年營收目標區間上調至€1.7–2.2B（原€1.5–1.9B），理由為AI資料中心、光子與邏輯／記憶體／CPO的混合鍵合新用途","source":"Bits&Chips: Besi raises long-term targets on AI packaging and hybrid bonding demand","url":"https://bits-chips.com/article/besi-raises-long-term-targets-on-ai-packaging-and-hybrid-bonding-demand/","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261025","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q2-26上半年訂單€562.6M，年增116.5%；混合鍵合客戶數由2025年底15家增至Q2-26底21家；Q3-26指引營收較Q2的€249.9M成長10–15%，毛利率63–65%","source":"Besi Q2-26 and H1-26 Results press release","url":"https://datacentremagazine.com/globenewswire/3331898","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261025","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"執行長將混合鍵合採用率上升連結到2027–2030年間預期的AI產品發布；Morningstar指訂單前置期6–9個月，為觀察重點","source":"Bits&Chips: Besi sees orders double on hybrid bonding demand","url":"https://bits-chips.com/article/besi-sees-orders-double-on-hybrid-bonding-demand/","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261025","affects":["thesis.R","triggers"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"SK Hynix將混合鍵合推遲至HBM5，可能延後Besi記憶體機會","source":"Bits&Chips","url":"https://bits-chips.com/?p=232321","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"荷蘭媒體稱美方收購 Besi 將面臨荷蘭國安審查等障礙（報導預期，非正式程序）","source":"De Belegger: Amerikaanse overname van Besi lijkt dichtbij, maar er is één groot obstakel","url":"https://www.debelegger.nl/post/amerikaanse-overname-van-besi-lijkt-dichtbij-maar-er-is-één-groot-obstakel","excerpt":"de overheid nodig zijn, juist omdat Besi actief is in een sector die van groot belang is voor Europa en voor de technologische zelfstandigheid van Nederland. Sinds 2023 moeten bedrijven in deze sector overnames, fusies en investeringen voorleggen aan het ministerie van Economische Zaken voor een toetsing op mogelijke risico’s voor de nationale veiligheid.","as_of":"2026-03-13","retrieved_at":"20261025","affects":["triggers","valuation"],"status":"ok"},{"id":"reg_tariff_export#none","axis":"reg_tariff_export","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"荷蘭投資網站指出地緣政治、出口規範、客戶集中與匯率可能影響 BESI 2026 年的可預測性與利潤率","source":"debelegger.nl 'Hybrid bonding maakt Besi kansrijk, maar dit zijn de valkuilen in 2026'","url":"https://www.debelegger.nl/post/hybrid-bonding-maakt-besi-kansrijk-maar-dit-zijn-de-valkuilen-in-2026","excerpt":"Geopolitiek, exportregels, klantconcentratie en valuta kunnen de voorspelbaarheid en marges raken, terwijl hoge AI-verwachtingen het aandeel extra gevoelig maken.","as_of":"2026-01-29","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Bits&Chips 報導 Besi 混合鍵合領先但約二十個平台競爭，包含數家中國業者","source":"bits-chips.com 'Besi leads hybrid bonding race with twenty players chasing'","url":"https://bits-chips.com/article/besi-leads-hybrid-bonding-race-with-twenty-players-chasing/","excerpt":"Besi leads hybrid-bonding race, with twenty players chasing 7 July 2026 René Raaijmakers Founder of Bits&Chips and High Tech Institute | Tech writer Reading time: 4 minutes Everyone is piling into hybrid bonding, the holy grail for stacking chips.","as_of":"2026-04-01","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2-26 訂單€562.6M(H1)、Q2訂單€292.9M、Q2營收€249.9M；光子、混合鍵合、資料中心驅動；混合鍵合客戶由15增至21；Q3-26營收指引較Q2+10–15%，毛利率63–65%","source":"BESI Q2-26 and H1-26 results press release","url":"https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q2-26-and-h1-26-results/","excerpt":"Q2-26 Revenue and Net Income of € 249.9 Million and € 89.0 Million, Respectively, Up 68.7% and 177.3%, Respectively, vs. Q2-25. Orders of € 292.9 million Up 128.8% vs. Q2-25. H1-26 Revenue and Net Income of € 434.7 Million and € 140.6 Million, Respectively, Up 48.8% and 121.1%, Respectively, vs. H1-25. Orders of € 562.6 million Up 116.5% vs.","as_of":"2026-07-23","retrieved_at":"20261025","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年6月BESI上調長期年營收預期至€1.7–2.2B（原€1.5–1.9B），2.5D AI資料中心與光子、CPO為依據","source":"Bits&Chips: Besi raises long term targets on AI packaging and hybrid bonding demand","url":"https://bits-chips.com/article/besi-raises-long-term-targets-on-ai-packaging-and-hybrid-bonding-demand/","excerpt":"Besi raises long-term targets on AI packaging and hybrid bonding demand 18 June 2026 Paul van Gerven Editor at Bits&Chips Reading time: 1 minute BE Semiconductor Industries (Besi) has raised long-term annual revenue expectations from 1.5-1.9 billion euros to 1.7-2.2 billion euros.","as_of":"2026-06-15","retrieved_at":"20261025","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"BofA稱ASML進入混合鍵合支援可能對Besi構成壓力，但分析師未假設其取得顯著市佔","source":"TheNextWeb: ASML's chip packaging move threatens Besi shares, Bank of America says","url":"https://thenextweb.com/news/besi-asml-hybrid-bonding-dutch","excerpt":"in the Stoxx 600 last quarter before Bank of America halved its price target October 6, 2026 - 3:35 pm ASML air freight containers in Tainan, May 2025 Credit: 4300streetcar Bank of America cut BE Semiconductor Industries to neutral and nearly halved its price target, saying the share price does not reflect the threat of ASML entering hybrid bonding, the market Besi depends on for growth.","as_of":"2026-10-06","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"ASMPT、Süss、Shibaura 已出貨混合鍵合設備，韓國四家業者追逐 SK Hynix／Samsung；Bits&Chips 認為混合鍵合不再是 BESI 的藍海","source":"Bits&Chips, BESI's blue ocean is slowly turning redder","url":"https://bits-chips.com/article/besis-blue-ocean-is-slowly-turning-redder/","excerpt":"Serious players like ASMPT, Süss and Shibaura are already shipping hybrid bonding systems there.","as_of":"2026-07-01","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"SK hynix 評估 HBM4 16 層採無助焊劑鍵合後仍保留 MR-MUF，認為技術尚早；HBM4 與 HBM4E 16 層維持現行製程","source":"TrendForce, SK hynix may stick with MR-MUF for HBM4 16-high","url":"https://www.trendforce.com/news/2026/01/13/news-sk-hynix-may-stick-with-mr-muf-for-hbm4-16-high-despite-asmpt-tc-bonder-orders/","excerpt":"evaluated adopting fluxless bonding for HBM4 16-high but ultimately opted to retain its existing advanced MR-MUF process","as_of":"2026-01-13","retrieved_at":"20261025","affects":["thesis.H","triggers"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"全球約二十個混合鍵合平台在開發，BESI CEO 承認設備商大量進入、中國業者出現","source":"Bits&Chips, BESI leads hybrid bonding race with twenty players chasing","url":"https://bits-chips.com/article/besi-leads-hybrid-bonding-race-with-twenty-players-chasing/","excerpt":"race, with twenty players chasing 7 July 2026 René Raaijmakers Founder of Bits&Chips and High Tech Institute | Tech writer Reading time: 4 minutes Everyone is piling into hybrid bonding, the holy grail for stacking chips. Twenty platforms are now in development worldwide. Yet, Besi remains confident about its lead. At Besi’s annual investor day, CEO Richard Blickman was unusually","as_of":"2026-07-01","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"韓國業者 LG、SEMES、Hanmi、Hanwha Semitech 開發混合鍵合機，ASMPT 也在建立能力，BESI 仍領先","source":"TrendForce, Hybrid bonding leader BESI reportedly draws takeover interest","url":"https://www.trendforce.com/news/2026/03/13/news-hybrid-bonding-leader-besi-reportedly-draws-takeover-interest/","excerpt":"The report notes that several Korean companies including LG Electronics, SEMES, Hanmi Semiconductor and Hanwha Semitech are developing related systems, while Singapore-based ASMPT is also working to build capabilities in the technology.","as_of":"2026-03-13","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Besi 與 Applied Materials 推出完整整合的 die-to-wafer 混合鍵合平台（合作模式，非通路轉移）","source":"Bits&Chips: Besi sees orders double on hybrid bonding demand","url":"https://bits-chips.com/article/besi-sees-orders-double-on-hybrid-bonding-demand/","excerpt":"Applied Materials and Besi launched a fully integrated die-to-wafer hybrid bonding platform at Semicon West. Credit: Besi","as_of":"2026-04-01","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2-26 後 22 位分析師預估 2026 營收 €987.8m、EPS €4.23；財報前為 €954.8m／€4.04","source":"Simply Wall St: BESI Second-Quarter Results Are Out And Analysts Have Published New Forecasts","url":"https://simplywall.st/stocks/nl/semiconductors/ams-besi/be-semiconductor-industries-shares/news/the-be-semiconductor-industries-nv-amsbesi-second-quarter-re","excerpt":"BE Semiconductor Industries' 22 analysts are now forecasting revenues of €987.8m in 2026. This would be a huge 35% improvement in revenue compared to the last 12 months. Statutory earnings per share are predicted to bounce 64% to €4.23. Yet prior to the latest earnings, the analysts had been anticipated revenues of €954.8m and earnings per share (EPS) of €4.04 in 2026.","as_of":"2026-07-26","retrieved_at":"20261025","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Investing.com 共識 Buy，23 位分析師，平均目標價約 €296.57，區間 €173–€401","source":"Investing.com BESI consensus estimates","url":"https://www.investing.com/equities/be-semicond-consensus-estimates","excerpt":null,"as_of":"2026-08-15","retrieved_at":"20261025","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2-26 財報給 Q3-26 營收季增 10–15%、毛利率 63–65%、營業費用持平至 +5%","source":"Quartr: BESI Q2 2026 earnings summary","url":"https://quartr.com/events/be-semiconductor-industries-n-v-besi-q2-2026_3eFihPPL","excerpt":"Q3-26 revenue is expected to increase 10-15% sequentially from Q2-26, driven by continued AI and mainstream market demand. Gross margin is projected to be 63-65% in Q3-26, slightly lower due to a less favorable product mix.","as_of":"2026-07-23","retrieved_at":"20261025","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026 年 6 月 Oddo BHF 目標價由 €375 升至 €400；公司上調長期目標（營業利益率 45–55%、營收 €1.7–2.2bn），市場反應有限","source":"Boursorama: Besi en hausse limitée après un relèvement d'objectifs sans grande surprise","url":"https://www.boursorama.com/bourse/actualites-amp/besi-en-hausse-limitee-apres-un-relevement-d-objectifs-sans-grande-surprise-18acc5d31adccb377381eaa3413b6ce3","excerpt":"Besi a relevé ses objectifs financiers à long terme, tablant désormais sur une marge opérationnelle comprise entre 45% et 55%, pour un chiffre d'affaires compris entre 1,7 et 2,2 MdsEUR, à comparer à des fourchettes cibles de respectivement 40% à 55% et de 1,5 à 1,9 MdEUR il y a un an.","as_of":"2026-06-18","retrieved_at":"20261025","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-03-13 路透報導 Lam Research 與 Applied Materials 對收購 BESI 有興趣（Applied Materials 已持股約 9%）；BESI 表示不回應市場傳聞，專注以獨立公司執行策略計畫；已聘 Morgan Stanley 評估；未見簽署協議。","source":"搜尋摘要彙整（Reuters 報導經 digitaltoday.co.kr／HL 轉述）","url":"https://www.digitaltoday.co.kr/cn/view/36927/lam-research-applied-materials-consider-acquiring-dutch-chip-equipment-maker-besi","excerpt":"The Company is fully committed to the execution of its strategic plan to enhance shareholder value as an independent company.","as_of":"2026-03-13","retrieved_at":"20261025","affects":["valuation","triggers","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Besi 2026 Investor Day 摘要：產能擴張進行中，越南廠爬坡以支應目前每年 300 台 bonder 以外的未來需求。","source":"Quartr, BESI Investor Day 2026 summary","url":"https://quartr.com/events/be-semiconductor-industries-n-v-besi-investor-day-2026_3eFihPox","excerpt":"Capacity expansion underway, with Vietnam ramping up to support future demand beyond current 300 bonders/year.","as_of":"2026-06-30","retrieved_at":"20261025","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Hanmi 於仁川興建混合鍵合機工廠，投資 1000 億韓元，目標 2026 下半年完工、2027 年底前推出設備（同業新進入者，不同來源投資額不一致）。","source":"Asiae, Hanmi Semiconductor Invests 100 Billion KRW in Hybrid Bonder Development","url":"https://view.asiae.co.kr/en/article/2025072510360750859","excerpt":null,"as_of":"2025-07-25","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"BESI H1-26 訂單 €562.6M，年增 116.5%，由光子、混合鍵合、資料中心運算帶動的廣泛成長；Q3-26 營收指引較 Q2 的 €249.9M 增 10-15%","source":"Press Release: be Semiconductor Industries N.V. Announces Q2-26 and H1-26 Results","url":"https://www.itiger.com/news/2653743637","excerpt":"Orders of EUR 562.6 million rose 116.5% vs. H1-25 due to broad based growth across end-user markets with strength in photonics, hybrid bonding and datacenter computing applications.","as_of":"2026-07-23","retrieved_at":"20261025","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"Yole：後段設備營收 2026Q1 季增 6.2%，預估 Q2 再增 3.8%，由 AI、HBM、先進封裝領動，傳統封裝緩步復甦","source":"Yole Group Semiconductor Back-end Equipment Market Monitor","url":"https://www.yolegroup.com/product/quarterly-monitor/semiconductor-back-end-equipment-market-monitor/","excerpt":"Back-end equipment revenue increased by 6.2% QoQ from Q4 2025 to Q1 2026 and is projected to increase further by 3.8% QoQ in Q2 2026 as growth is led by AI, HBM and Advanced Packaging while mainstream assembly recovers more gradually.","as_of":"2026-06-30","retrieved_at":"20261025","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2019 下行：H1-19 營收年減 44.9%，但毛利率 55.9%（H1-18 為 56.5%），毛利率僅小幅下滑","source":"Besi Q2-19 and H1-19 results press release","url":"https://www.plantautomation-technology.com/pressreleases/be-semiconductor-industries-nv-announces-q2-19-and-h1-19-results","excerpt":"Revenue of € 174.1 million, down 44.9% vs. H1-18 consistent with ongoing weakness in assembly equipment market.","as_of":"2019-07-25","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"2019 前九個月毛利率 55.7%（2018 同期 56.9%），淨利年減 58.1%","source":"Besi Q3-19 results press release","url":"https://www.besi.com/investor-relations/press-releases/2019/details/be-semiconductor-industries-nv-announces-q3-19-results-q3-19-revenue-and-net-income-of-eur-897-million-and-eur-192-million-respectively-results-exceed-expectations/","excerpt":"Gross margin reached 55.7% vs. 56.9% in YTD-18.","as_of":"2019-10-24","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"2023 下行：全年營收 €578.9M 年減 19.9%、訂單 €548.3M 年減 17.4%；Q2-23 訂單 €112.6M 為單季低點；全年毛利率 64.9%（2022 為 61.3%），毛利率未隨下行下滑","source":"Besi Q4-23 and full-year 2023 results press release","url":"https://besi.com/events/events-shows/details/be-semiconductor-industries-nv-announces-q4-23-and-full-year-2023-results","excerpt":"Revenue of € 578.9 million decreased 19.9% due to adverse market conditions and reduced demand for mainstream computing and, to a lesser extent, automotive applications","as_of":"2024-02-08","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-03-13 路透報導 Lam Research 與 Applied Materials 對收購 BESI 有興趣；BESI 未確認、無簽署協議；荷蘭法下需國安審查。","source":"digitaltoday.co.kr 轉述 Reuters","url":"https://www.digitaltoday.co.kr/cn/view/36927/lam-research-applied-materials-consider-acquiring-dutch-chip-equipment-maker-besi","excerpt":"The Company is fully committed to the execution of its strategic plan to enhance shareholder value as an independent company.","as_of":"2026-03-13","retrieved_at":"20261025","affects":["valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 8 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"BESI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.25,"operating_margin_pct":36.36,"fcf_margin_pct":23.08,"rd_intensity_pct":11.71},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BESI","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"KLIC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":48.18,"operating_margin_pct":13.21,"fcf_margin_pct":4.21,"rd_intensity_pct":17.0},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KLIC","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ASMPT","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASMPT"},"note":"quarterly_income_stmt 無資料"},{"name":"042700.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.35,"operating_margin_pct":42.49,"fcf_margin_pct":18.69,"rd_intensity_pct":3.44},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.042700.KS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"AMAT","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.4,"operating_margin_pct":31.09,"fcf_margin_pct":18.23,"rd_intensity_pct":12.88},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT","as_of":"TTM ending 2026-07-31（4季加總）"}}],"subject":"BESI"},"financial_history":{"ticker":"BESI","currency":null,"method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":722870000.0,"revenue_yoy_pct":null,"gross_margin_pct":61.29,"operating_margin_pct":40.69,"net_income":240647000.0,"diluted_eps":2.9,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":578862000.0,"revenue_yoy_pct":-19.92,"gross_margin_pct":64.92,"operating_margin_pct":36.86,"net_income":177084000.0,"diluted_eps":2.23,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":607473000.0,"revenue_yoy_pct":4.94,"gross_margin_pct":65.18,"operating_margin_pct":32.2,"net_income":181992000.0,"diluted_eps":2.3,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":591331000.0,"revenue_yoy_pct":-2.66,"gross_margin_pct":63.29,"operating_margin_pct":29.27,"net_income":131641000.0,"diluted_eps":1.66,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/BESI/BESI_Q3_2026_Earnings_Call_20261022.md）

# Q3 2026 Earnings Call
**BE Semiconductor Industries N.V.** | Earnings Calls | 2026-10-22

**Operator** (Operator):
Good morning, good afternoon, ladies and gentlemen, and welcome to Besi's quarterly conference call and audio webcast to discuss the company's 2026 third quarter results. You can register for the conference call or log into the audio webcast via Besi's website, www.besi.com.
Joining us today are Mr. Richard Blickman, Chief Executive Officer; and Mrs. Andrea Kopp, Senior Vice President, Finance. [Operator Instructions] As a reminder, ladies and gentlemen, this conference is being recorded and cannot be reproduced in whole or in part without written permission from the company.
I would now like to turn the call over to Mr. Richard Blickman. Go ahead.

**Richard Blickman** (Executives):
Thank you. I'd like to remind everyone that on today's call, management will be making forward-looking statements. All statements other than statements of historical facts may be forward-looking statements. Forward-looking statements reflect Besi's current views and assumptions regarding future events, many of which are, by nature, inherently uncertain and beyond Besi's control. Actual results may differ materially from those in the forward-looking statements due to various risks and uncertainties, including, but not limited to, factors that are discussed in the company's most recent periodic and current reports filed with the AFM. Such forward-looking statements, including guidance provided during today's call, speak only as of this date. Besi does not intend to update them in light of new information or future developments nor does Besi undertake any obligation to update the forward-looking statements.
For today's call, we'd like to review the key highlights for our third quarter and 9 months ended September 30 of this year and update you on the market, our strategy and the outlook. First, some overall thoughts on the third quarter. Besi reported strong third quarter and year-to-date 2026 results as favorable order momentum continued for both our traditional and wafer-level assembly systems.
For the quarter, revenue of EUR 283.4 million increased by 13.4% and 113.6% versus the second quarter of this year and the third quarter of 2025, respectively. Year-over-year revenue growth was primarily due to increased demand for computing end markets with strength in hybrid bonding, photonics and data center applications. Similarly, orders of EUR 342.6 million increased by 17% versus the second quarter of this year and 96.1% versus the third quarter of last year, primarily due to increased orders for hybrid bonding, data center and AI-related mainstream computing applications, including power management. Besi's orders for the last 12 months increased to EUR 1.2 billion as the expansion of digital infrastructure capacity significantly increased demand for our advanced packaging portfolio.
In the third quarter of this year, net income of EUR 107.2 million increased by 20.4% versus the second quarter of this year and 323.7% versus the third quarter of last year. Strong profit growth versus the third quarter of last year was principally due to higher revenue, improving gross margins and disciplined expense management, which has significantly limited overhead development in the current revenue ramp. In fact, baseline operating expenses as a percentage of revenue decreased from 32% in the third quarter of last year to 16.4% in the third quarter of this year, underscoring the operating leverage in our business model. As a result, net margins increased from (sic) [ to ] 37.8% in the third quarter '26, double the level of Q3 '25.
Year-to-date results also confirm the strength of Besi's advanced packaging portfolio in the present AI CapEx up cycle. Revenue of EUR 718.1 million increased by 69% versus year-to-date '25, primarily due to broad-based growth in computing end markets and to a lesser extent, an increase in mobile shipments. Some modest recovery in more traditional automotive, industrial and non-AI computing markets has also been experienced. Year-to-date '26 orders of EUR 905.2 million more than doubled versus year-to-date '25 due to growth across all end-user markets with strength in hybrid bonding, photonics and data center applications.
Further, net income of EUR 247.8 million increased by 179.1% versus the year-to-date '25, primarily due to significantly higher revenue and gross margins, primarily due to a more favorable product mix and the pass-through of price increases to help offset higher supply chain costs. Combined with ongoing cost control efforts, net margins increased to 34.5% versus the 20.9% a year ago.
Our results also indicate significant market share gains in our addressable markets, particularly for Besi's flip chip, multi-module die attach and hybrid bonding systems. Increased profitability and careful working capital management have contributed to steady improvement in our liquidity position this year.
Net cash reached EUR 246.6 million at September 30, up EUR 254.4 million versus September 30 last year. As a result, we will increase our share buyback program to EUR 100 million for the annual period starting October 27 of this year.
Next, I'd like to discuss the current market environment and an update on our strategy. TechInsights recently upgraded its 2026 assembly equipment forecast to growth of 37%, almost double their last forecast. They now expect the market to reach $12 billion by 2028, an increase of 122% compared to their last estimate of 53% growth. We expect to grow more than double their underlying market growth rate.
We can report significant progress this quarter and this year on our wafer-level assembly agenda. Year-to-date, hybrid bonding orders have more than doubled versus fiscal '25 as orders increased for HBM applications, more logic chiplet programs entered production, co-packaged optics use cases expanded faster than anticipated and edge AI device production began. To date, in 2026, hybrid bonding customer adoption grew to 23 customers and total cumulative unit demand exceeded 215 systems.
In the third quarter of this year, orders were received from customers for logic, co-packaged optics and memory end markets. Of note, we received orders for both hybrid bonding and TC Next systems from a leading memory customer as they focus on the development of current and next-generation HBM device structures. Our competitive position in wafer-level assembly is very strong, further underscored by the progress we've made -- excuse me, this year and inclusion recently of an innovation partner at Applied Materials EPIC Center, showcasing both Besi's hybrid bonding and TC Next solutions.
We do not view ASML as a competitor, contrary to recent analyst reports. To the best of our knowledge, ASML is interested in a road map for 3D transistor stacking inside the chip over the next decade and is not competing with Besi in the area of die-to-wafer bonding. In fact, ASML and Besi are jointly working together on die stress programs to improve placement accuracy and consequently throughput as well as other mutually beneficial areas of collaboration.
Now a few words about our guidance. The favorable year-to-date order momentum should continue in the fourth quarter as the multiyear AI capacity build-out progresses. We see strong demand continuing for data center and photonics applications from Asian subcontractors and market share gains in our addressable markets, particularly for Besi's flip chip and multi-module attach systems.
Our results also indicate ongoing hybrid bonding capacity expansion planned by the leading industry players for logic, CPO and edge AI devices. Severe memory shortages this year have extended the use of lower stack heights in current HBM production beyond prior expectations. However, the need for higher power efficiency -- energy efficiency performance, bandwidth interconnect density and speed has only increased interest in the use of hybrid bonding for HBM as the year has progressed. We anticipate that hybrid bonding will be adopted in a range of stack heights over the next 2 years and in new innovative stacks combining HBM, custom advanced logic base dies and the direct bonding of DRAM onto accelerator chips by decade end.
Based on our current backlog and feedback from customers, we anticipate that Besi's Q4 revenue will be flat plus/minus 5% as certain customers request delivery dates for third quarter '26 received orders in alignment with H1 production capacity plans. In addition, gross margins are anticipated to range between 63% and 65%, and operating expenses are expected to increase between 5% and 10% versus the third quarter due primarily to increased strategic consulting costs.
That ends my prepared remarks. I would like to open the call for questions.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Didier Scemama from Bank of America.

**Didier Scemama** (Analysts):
First, I wanted to ask your views on essentially the adoption of hybrid bonding in HBM because I think clearly, expectations were for that adoption to be delayed. But at the same time, you clearly mentioned that you've had orders on TCB and hybrid bonding from one customer. So how should we think about the adoption curve now for that particular customer and for hybrid bonding in general in HBM for your business? Is that more of a 2028, 2029 story? Or should we have some meaningful revenues already next year?

**Richard Blickman** (Executives):
Well, what can we add here? I mean the opinions are as they have been expressed by you. But anyway, let me give a response to that. As I mentioned, the development activity to use hybrid bonding for HBM stacking has only continued. And despite some noise about despeccing, that only relates to satisfying current demand in current end application. But the next generation, future demand is being evaluated using the benefits of hybrid bonding, as very well known, less energy, higher performance and that road map development is continuing at full speed with all 3 memory manufacturers.
The precise dates of when certain applications will hit mainstream volume is not known by us. It's determined by the end customer of those customers mentioned. And we are only further preparing the equipment processes with windows, which can be used in those end applications. But again, the activity and the focus and the commitments also illustrated by the orders received are in full speed continuing.

**Didier Scemama** (Analysts):
Okay. Maybe my follow-up question would be on the hybrid bonding ramp at your leading-edge logic and foundry customers. I think in the past, you had mentioned that your leading customer have about maybe 60 tools installed at their facilities and ambitions were for that AP7 factory to have at least 100 tools or something like 100 tools by '27. I just wondered if you could maybe give us an update on progress of that ramp? And also related to that, there's been press reports that another customer is planning to open an additional 3 advanced packaging fabs. Just wondered if you've got any updated thoughts on the magnitude of those particular opportunities.

**Richard Blickman** (Executives):
Well, the precise volume of equipment orders is always unknown at the start. It depends on end customers and their applications. But the news is certainly a very good one that tells you that they expect a significant further increase in demand of devices, and that's ever broader range in logic, but also co-packaged optics involved.
And your earlier question, we reported we received so far twice as many orders as the whole year '25 for hybrid bonders. That tells you that the expansion is continuing.

**Operator** (Operator):
The next question comes from Harry Blaiklock from UBS.

**Harry Blaiklock** (Analysts):
The first is just a follow-up on Didier's question on memory adoption. I appreciate that there are multiple reasons why hybrid bonding is attractive in memory, which you outlined in your answer. But I guess you could say that, that's been true for some time now in terms of the benefits of adopting hybrid bonding. So when you look over the next kind of 2 years, is there a key bandwidth requirement or I/O density milestone or anything else that you think will make adoption particularly compelling to the memory industry?

**Richard Blickman** (Executives):
Well, let me answer it in this way. As I said earlier, the current demand is satisfied as much as possible with existing technologies. And the consequence of that is that adopting superior technologies has been somewhat delayed. But that does not mean that, that results in a showstopper for adopting hybrid bonding for those applications. And that's the message. If that would be the case, all 3 of them would have stopped the development of adoption of hybrid bonding at some point in time. But as I mentioned earlier, it is only continuing and increasing and orders for systems are being placed.

**Harry Blaiklock** (Analysts):
Got it. That's very helpful, Richard. And then maybe second question is on co-packaged optics. You mentioned that demand is increasing there. Is that predominantly from the co-packaged optics switches that are ramping? Or is it early capacity build for optical I/O for GPUs in co-packaged optics?

**Richard Blickman** (Executives):
It can be for both. We're not fully, let's say, informed about for which applications. But as we mentioned earlier, we had a quite substantial order in the first quarter for those applications. And also, we have received several in the last quarter.

**Operator** (Operator):
[Operator Instructions] The next question comes from Charles Shi from Needham & Company.

**Yu Shi** (Analysts):
Maybe my first question, yesterday, Micron said that they are still going to hybrid bonding and other than well understood the benefit of thermal, they see there is also bandwidth benefit because of a smaller bond pad pitch, which ultimately determines bandwidth. But I mean, throughout my conversations with average investors, they still kind of associate hybrid bonding with HBM stack height thickness and really -- people are really obsessed about what's the timing of 16 high, 20 high. So maybe I understand that despeccing, there's some temporary near-term cross currents there, but what should we be looking at right now to really understand the timing of hybrid bonding adoption in HBM? And related to that, can you give a little bit of color on this particular customer, why are they buying more hybrid bonders over the last quarter? Because I would assume all the top 3 HBM suppliers already have hybrid bonders from Besi. Why are they buying more?

**Richard Blickman** (Executives):
Well, we have not disclosed the customer ordering the systems. But in general, let me respond in that way. It precisely explains that it's not a matter of stack height, which determines the adoption of hybrid bonding. One should simply imagine a hybrid bonded interconnect is superior for the reasons as was just repeated, energy, latency, bandwidth, in other words, and heat. And those are the issues which they face to create whatever new structures. And whether that is 16 or 20 or 12, and we've mentioned that earlier in the call, end of July, I think also end of April. So there's a whole road map, which has the simple decision to make. Do we use a conventional reflow process, TC process? Or is the performance improvement and some released data about that performance improvement, 20%, 30%, also about the heat, temperature reduction. And those are the developments those customers are working on, driven by their customer, the big end customer, we all know, is dictating at some point "I want devices to be hybrid bonded because of better performance." Does that answer your question?

**Yu Shi** (Analysts):
Yes. Yes, Richard. And maybe a quick follow-up. Richard, what do you hear so far from your customers' customers who are already testing hybrid bonded HBM cells from one of your leading HBM customers right now? What do you hear from them?

**Richard Blickman** (Executives):
A very positive feedback. We hear simply, and as I said to an earlier question, why would more hybrid bonders be needed to test, to qualify preproduction if there is not a high-volume production somewhere inside. But I'm sorry, we have to answer it in this way because we are not involved or we don't have any knowledge of end customer demand and decisions. But what we do know is that the activity and the pressure on making this high volume ready is only increasing.

**Operator** (Operator):
The next question comes from Lee Simpson from Morgan Stanley.

**Lee Simpson** (Analysts):
I really just wanted to go back to the delay in deliverables for Q4. I think as I understood things, there's a pushout with capacity expansion plan at 1 or 2 of your customers from Q4 into the first half. So just trying to understand, is it a multi-customer issue? Is this maybe something that relates to the AP7 that you talked about or something more broadly? And then I've got a follow-up.

**Richard Blickman** (Executives):
No, no, no. Then we have presented this message incorrectly. It's not a customer pushout. It is simply customers order equipment. And we are in a whole line, a certain range and sometimes only bonder in a production line. The timing of delivery depends on the readiness of all equipment for that process and at the same time for the infrastructure. So although we have received last quarter, 340-something million in orders, that doesn't mean that they are all shipped in the next week. So some are shipped in Q4. Some are shipped in Q1 and also some are shipped in Q2. So that's a normal pattern. But in order to explain that, that results in a more or less flat revenue has nothing to do with any delays. That's just how the orders have been placed.

**Lee Simpson** (Analysts):
Great. Okay. Very clear. And maybe just a quick follow-up. It does seem as though with the margin guide that there is some ongoing, let's say, that may have one-off feature in Q4. I wonder if those one-offs would result in future savings. And if indeed, you could actually give us a quant on what those savings.

**Richard Blickman** (Executives):
Please repeat where are you referring to?

**Lee Simpson** (Analysts):
We're just looking at the margin guides for Q4, under the impression that there is some one-off in there. We just wondered if there was a resulting savings to come from that.

**Richard Blickman** (Executives):
No, there's no one-offs in that. To explain to you, and I understood you are new in covering our stock, our margin guide, 63% to 65% is the same guide we had for Q3. It depends ultimately on the mix of the orders totaling the revenue. Sometimes, it is a bit more and sometimes it's a bit less. But there's no one-off effect. There is in the OpEx, we have a one-off extra cost because of consultancy. And we highlighted that and why the OpEx is slightly higher, 5% to 10% compared to the third quarter. But on margins, it is purely a guidance, which was the same as for the last quarter. But the mix may result in a somewhat in that range margin. Is that clear?

**Lee Simpson** (Analysts):
All clear.

**Operator** (Operator):
The next question comes from Sandeep Deshpande from JPMorgan.

**Sandeep Deshpande** (Analysts):
My question is regarding your TC Next tools. You've got this order in the current quarter as well in Q3 for TC Next tools as well as hybrid bonding. Is there any -- is the customer ordering for TC Next and hybrid bonding going to make a decision between one or the other? Or is these separate kinds of products they're going to use these tools for? And I have a quick follow-up.

**Richard Blickman** (Executives):
Sandeep, that is for 2 different product road maps of that customer. But they are all involved in memory. So that explains also there's not one end product. But the fact that we received this order, this is also, by the way, a repeat order for TC. That also shows that we have an excellent workhorse for the next generation in TC Next to our hybrid bonding road map.

**Sandeep Deshpande** (Analysts):
Understood. And when you look at the TC Next road map, I mean, how do you see this? I mean, clearly, hybrid bonding has already become a major product line for Besi in terms of revenue generation. Is TC Next going to become this major product line next year or the following year? Or is the -- is the timing still being worked out with the customer in terms of adoption?

**Richard Blickman** (Executives):
Well, we have now in total 7 customers. And this tool is developed for bond pad pitches below what is currently the market standard, and that is in the 20s, this is below 20. And at the same time, it's developed for fluxless processes. And the expectation is that for the next generation, so somewhere between 10 and 20 micron bond pad pitch, that this will be, let's say, excellent for not only memory stacking, but also logic. So most customers ordered so far logic. We shared data produced at Imec last year on this machine, right even below 10-micron bond pad pitch and that comes very close to hybrid bonding. This machine gives the option to the customer to use either a reflow process or hybrid bonding if needed. And that is where it's intended for. And that segment is opening up. And in the next couple of years, it could be a very sizable product range.

**Operator** (Operator):
The next question comes from Robert Sanders from Deutsche Bank.

**Robert Sanders** (Analysts):
I guess just following up from the comments about ASML. I know you can't talk too much about this, but can you just sort of talk a little bit about the IP you have around handling and the uniqueness of it? I think there's still this idea that even if they go into something like wafer-to-wafer, they'll ultimately transition to die-to-wafer. So it seems like there's quite a lot of misunderstanding. So if you could just clarify that and how secure your position is in the die side?

**Richard Blickman** (Executives):
Well, first of all, what we've tried to make clear, we have a very good relationship with ASML. And what we understood is their strategy, as they explained to the market, is to focus on 3D integration using a hybrid bonding process once that becomes a mainstream market requirement. They are not interested, as we stated, in the current market for 2 reasons. One is simply the size of the market and also the current situation in this market. Together, we are developing programs to further understand die stress. What is die stress? Every die has stress for the reason that it is built in layers. And once it's cut, it has another stress introduced. And that stress determines the placement accuracy and also other technology you need for the placement process.
So other than a quick conclusion, ASML, because of its size, will, in the next couple of weeks, take over Besi's market position. The situation is entirely different. One could argue this stacking of transistors into dies, the 3D development continuation of Moore's Law, that will require accuracy placements below 10 nanometers. We are today shipping this quarter the first 50 nano, which is by far ahead of the current curve. So 100 is more or less the standard. That's all the 215 machines sold so far is on that generation, Generation 1 and Generation 1 plus, 50 is Generation 2. But then next to 50, which will be sufficient for the next 4 or 5 years is 25. And 25 is currently under development, which we are definitely able to reach.
And then the next step beyond that is going down to 10. But that's all still chip-to-wafer bonding. And that is not chip-in-wafer bonding. That's a step beyond that. So there's still many years ahead of us on further development of this technology in line with further shrink in chip design.

**Robert Sanders** (Analysts):
Could I just quickly ask a follow-up just on automotive and industrial? In the past, you had quite a strong order from that back in '21, '22. It seems like the mature side is getting very tight now. Have you seen the beginnings of a sort of cycle on the mature side? Do you think that's sustainable?

**Richard Blickman** (Executives):
Well, whether that's sustainable, that will probably follow the same cyclical pattern as the industry has done forever. So there are certain signs of pickup. We see that in orders from subcontractors. We see that in orders more broadly. But the key is, of course, and we try to explain that in the press release, our business is driven by the high end of all of the applications, whether that is submicron or whether that is in the industrial market, and you always have new developments. Power today is hot because that power is also used for data centers. And that's older, you could say, technology in brackets. But it's also across the board. It's picking up. That's reflected in the updated TechInsights' forecast for '26. And that should continue in '27 if the cyclical pattern is similar to that, which we experienced in the past. So that then explains that they expect a continuation of this growth cycle in the next year.

**Unknown Analyst** (Analysts):
Just as a follow-up on your comments regarding ASML. I was just wondering if you could provide some more color on your nature of the partnership with ASML. It sounds like you're working together to solve some of the problems that you're seeing on in die-to-wafer bonding. So like where is the R&D taking place? How does the relationship function in practice?

**Richard Blickman** (Executives):
This is an, let's say, ongoing dialogue for many, many years on different programs, which have to do with -- and in this case, understanding die stress. So the whole critical nature of manipulating die, so to speak, you have to pick up a die, you have to place it and you have to place it ever more accurately, is to understand what are the reasons for the behavior of that process. It takes place inside our development, inside their development, also at other locations here in Europe. So you should see that on a program basis and an alignment regularly on road maps.

**Unknown Analyst** (Analysts):
That's very clear. And then a follow-up, I think you mentioned they're targeting different applications, more intra-die 3D transistor formation. Could you talk about what's fundamentally different between bonding or hybrid bonding or intra-die 3D transistor formation and the die stacking that Besi currently looks at? Like what -- are there fundamental challenges that are different that you and ASML are looking to solve here?

**Richard Blickman** (Executives):
We connect dies. So our job forever is to connect dies, chips, which are coming out of front end and are ready to be connected to something. We are not engaged yet in the chip manufacturing process. And the angle we understand ASML is looking at is how to continue the road map in chip design and manufacturing. So we are at the end. We connect the dies so far. You can connect 2 dies with a wire. You can do that with a mass reflow flip chip. You can do that with a TC process, a bit helping with a bit of pressure. You can do it with hybrid bonding. And that's all manipulating individual dies. Is that more clear?

**Unknown Analyst** (Analysts):
Yes, very clear.

**Richard Blickman** (Executives):
I should also add, we have this angle with Applied Materials. So simply imagine Applied's process front end, how to make those dies are running into the same challenge in ever smaller design geometries than finally connecting those dies into end products. So the foundation behind our relationship with Applied already for 7 years and now in the EPIC center, where the first program we will set up is both for hybrid bonding and TC for a major U.S. customer. And that is the reason why we come ever closer.

**Operator** (Operator):
The next question comes from Martin Jungfleisch from BNP Paribas.

**Martin Jungfleisch** (Analysts):
Just have 2 quick ones. First one is on the order trends. In the press release this morning, you mentioned that you would expect the order momentum to continue into Q4. Is this primarily driven by the OSATs demand for 2.5D in photonics? Or is this also driven by hybrid bonding demand of the leading foundry? And is there any reason to think that there's some digestion period now for hybrid bonding at the leading foundry at levels in the first 9 months? Or would you not agree that?

**Richard Blickman** (Executives):
No, that's an excellent question. And the answer is that we don't expect the momentum to decline. So the momentum should continue. We are not in control of exact order timing placements. But as we said in our press release and also in the comments now, the momentum is still very strong.

**Martin Jungfleisch** (Analysts):
Okay. And that's in both, right, classical and then hybrid.

**Richard Blickman** (Executives):
Yes.

**Martin Jungfleisch** (Analysts):
Okay. Interesting. And my follow-up is really on the new tool release in photonics. I think you had an initial target of submicron photonics tool for Q4. Is that still expected in Q4? And then maybe also if you got some initial customer interest or orders for the tools?

**Richard Blickman** (Executives):
Well, as we said, in general terms, there is increased activity all the time for hybrid bonding and certainly for those applications. As we highlighted so far, twice as many orders as what we had in the whole year '25. And a part of that is also the co-packaged optics part.

**Martin Jungfleisch** (Analysts):
Yes. I was also referring not to the hybrid side of it. I was referring to this -- I think it's called the Evo1.

**Richard Blickman** (Executives):
For the pluggables...

**Martin Jungfleisch** (Analysts):
Yes, yes, exactly, exactly.

**Richard Blickman** (Executives):
Yes. Well, for the pluggables, the same, continued momentum. So that is directly related to data centers. And it's also a very good question because if you would start to see a digestion or a slowdown, you should ask the question, is this a first sign of an overall overcapacity? Or is this a sign of a timing issue? Those are the critical signals to understand. But so far, until October 22, the order momentum continues.

**Operator** (Operator):
The next question comes from Simon Coles from Barclays.

**Simon Coles** (Analysts):
It's just on the strategic review. The last you did one, I think, was in '25, and then we got a nice upgrade to the hybrid bonding targets. Could you just give us a bit more color on where this one is focused? Is it on some of your other tools that are maybe not getting as much attention as they perhaps could get in this market?

**Richard Blickman** (Executives):
Sorry, the line was very difficult. Can you repeat it one more time?

**Simon Coles** (Analysts):
Sure. Can you hear me better now?

**Richard Blickman** (Executives):
Yes. Try again. Yes, please.

**Simon Coles** (Analysts):
Just on the strategic review, the last time you gave us a strategic review, we saw some upgrades to hybrid bonding TAM numbers. Could you just give us some color on where strategic review is focused? Is it around some other areas of the business that could be getting some more attention?

**Richard Blickman** (Executives):
Perfect. Why do we do this review? And your question is also very important. And we did the last review beginning of last year, which we then shared with the market. So much is happening in this industry in this last 1.5 years that we are engaged to get in the 16 weeks deep dive with our key customers on understanding even better their road maps and being prepared to serve them not only on the short term, but on the longer term. And one of the questions is, of course, hybrid bonding, TC and mass reflow. How -- which road maps and timing is going to be determining the demand in the next 3 to 5 years. And that focus has always helped us. It helped us for several reasons.
One is, of course, to understand better what is the market requirements. But at the same time, the customer engagement always increases when you do this kind of process. Also involved is, of course, Applied Materials and simply to understand on this whole advanced packaging, what can we do more, what is missing, what can we do in partnership and better development? So those are the key deliverables to be expected in the next, let's say, 16 weeks. We're already 4 weeks down the road. So early January, we should come to a conclusion.

**Operator** (Operator):
The next question comes from Marc Hesselink from ING.

**Marc Hesselink** (Analysts):
First question is on -- a lot of Europeans are talking about increasing longer visibility, longer lead times with the clients. Is that something that you're also seeing? For example, the element that you have very good order intake in this quarter, but some of it will be for the first half next year? Or is that just not directly linked to that longer lead times?

**Richard Blickman** (Executives):
Yes. Well, it's inevitable with this enormous demand, we are able to grow nearly 70% year-on-year, which is a lot more machines. Also customers, because of longer lead times of other tools in the process, and that's the reason we explained also earlier that you can't ship immediately what you ordered in Q3 and Q4 because also of that reason. But that's a natural development. If you look at the front-end companies, supposedly, their lead times have gone much further down the road, even 2 years. We are able with our operating model to increase the capacity rapidly, as mentioned, to 70%, is simply because of the supply chain model and operating model, which allows that.
The question could also be, could you do more if you can deliver more? For some cases, it may be. But overall, we are more because the industry needs to increase the infrastructure. Also, as mentioned earlier, the supply of a complete line, and there's a bit of longer visibility. The visibility in lesser years behind us was about a quarter, 1.5 quarters. Now the visibility is longer. It's a quarter, 2 quarters, 6 months and for some programs, even longer.

**Marc Hesselink** (Analysts):
Okay. Very clear. And my second question is on the power management business opportunity. You highlighted for the second time, I think you also did it the previous quarter. This seems like a quite sizable opportunity given that it's quite a big change towards the higher voltage. So can you maybe explain a bit more like where exactly does Besi come in and how big can that addressable market be from the perspective of Besi?

**Richard Blickman** (Executives):
Well, I can explain it in this way. Power has always been part of our business and especially for automotive. That was for ever and still today, it is a reasonable segment. And we always said between 15% and 20% of our revenue is related to automotive. That has declined because of the enormous increase in AI data centers. So somewhere around 10%. But if you look at power increase, so part of that AI data center modules, that certainly brings that back to the levels which overall automotive was, including automotive then. So the equipment used for that is typically copper frames and power devices soldered to those frames, packaged and in all shapes and sizes. So next time you visit Duiven, we will show you some examples.

**Operator** (Operator):
The next question comes from Martin Marandon-Carlhian from ODDO BHF.

**Martin Marandon-Carlhian** (Analysts):
My first question on hybrid bonding adoption in logic and specifically on your U.S. logic customer because he didn't order at least at a significant level for some time now. I think he's facing a CPU shortage. So I was wondering if -- how do you see this customer potentially increasing its capacity for hybrid bonding in the following quarters on that CPU demand? And I have a quick follow-up.

**Richard Blickman** (Executives):
Excellent, Martin. Thank you. You're absolutely right. That customer ordered a large volume order in '24, it was even, and that they shipped in '25 and installed and full preparation now for mass volume production. And the question is, when is that filled and is extra capacity needed?
Well, with the success of that company regained, one can expect further expansion in next year. And what will be interesting to see, their original plan was to set up also operations in Asia, which is very close to our manufacturing facility. So there are certainly plans to further expand.

**Martin Marandon-Carlhian** (Analysts):
Okay. Very clear. And the second one is more on the GPU opportunity. So I think you previously described GPUs as potentially an inflection point for hybrid bonding demand in logic with the leading customer, the leading GPU player, sorry, adopting it. I think qualification was supposed to be this year, possibly orders next year and volume the following year in '28. Is that time line still valid? And how big do you think that opportunity could be?

**Richard Blickman** (Executives):
Well, the time line is still more or less as you have remembered. The volume is hard to predict. If we would mention an indication, it would be a guess.

**Unknown Analyst** (Analysts):
I just -- I was curious around your Applied partnership, right, with the announcement a few weeks ago, talking about a bit more TCB scaling to die on panel, and some new hybrid platforms. Should we expect that to turn into new, let's say, jointly offered systems, something like the Kinex type integrated lines for TCB specifically or die to panel? And if so, like could you roughly talk about time line when you think commercial product could be offered here?

**Richard Blickman** (Executives):
Well, let me explain it as follows. The Applied Kinex you need for achieving the maximum cleanliness, so particle-free process is guaranteed. And that is hybrid bonding. Of course, you need a certain cleanliness with a reflow process, a TC process, but that's far less critical than with hybrid bonding. It's not aimed at developing Kinex type of solutions. It's aimed at developing bonding processes. So how can we create, and that's a question of material and also the preparation for that, the most superior TC bonded device.
There's TC in several ways. There's also copper-to-copper bonding using a TC process. So those type of developments is expected to take place in the EPIC Center in Sunnyvale for U.S. customers directly. On top of the development, we have the TC development in Imec in Belgium. We have TC development in Radfeld. We have TC development in the center of excellence in Singapore. So supporting the development of next generation and that's all smaller bond pad, is all related to fluxless, developing superior processes to the processes used today.
And Applied has immense material knowledge, Applied Materials, also enormous experience in preparation and cleaning. And those type of processes are vital not only to hybrid bonding, but also to other interconnects like TC processes. I hope that answers your question.

**Unknown Analyst** (Analysts):
Yes, very helpful. Just a final one on China. It went to 40% orders and it drove the majority of the sequential increase, I think. So what are Chinese customers mainly buying now? And how confident are you that it's sort of tied to end demand rather than maybe a capacity build ahead of demand coming in?

**Richard Blickman** (Executives):
Well, there's a whole broad spectrum of Chinese subcontractors. Don't forget a lot of the high-end smartphone infrastructure is built in China. So that business is very much the Foxconn's and many others. So it's not just one application. There's also development in TC, development in hybrid bonding. But to your question, is that something which we expect a limited future? No, the answer is it will be -- will have a long-term future. There are many devices built in China and evermore. Also, by the way, for the pluggables.

**Operator** (Operator):
Okay. Thank you. Thank you, everyone.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### BESI_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜Richard Blickman｜guidance：管理層預告 Q3 營收較 Q2 成長 10%–15%。（原話："will increase by 10% to 15% versus the second quarter"）
- 2026-07-23｜Richard Blickman｜margin：Q3 毛利率預期降至 63%–65%，管理層歸因於產品組合較不有利。（原話："anticipated to decrease to a range between 63% and 65%"）
- 2026-07-23｜Richard Blickman｜guidance：Q3 營業費用預期持平至增加 5%，主因研發支出增加。（原話："Operating expenses are anticipated to be flat to up 5%"）
- 2026-07-23｜Richard Blickman｜guidance：管理層表示 Q3 訂單動能持續。（原話："order momentum continuing in the third quarter of this year"）
- 2026-07-23｜Richard Blickman｜margin：管理層拆解營業槓桿：基線營業費用占營收比由去年 Q2 的 30% 降至 Q2'26 的 18.9%。（原話："operating expenses reduced from 30% of revenue in Q2 last"）
- 2026-07-23｜Richard Blickman｜product：管理層估計 AI 應用占系統訂單比重上半年約 60%，去年同期約 50%。（原話："Overall, we estimate that system orders for AI"）
- 2026-07-23｜Richard Blickman｜customer：Q2 新增混合鍵合訂單，來自 2 個既有客戶與 1 個新的超大規模客戶。（原話："Additional hybrid orders were received in the second quarter"）
- 2026-07-23｜Richard Blickman｜customer：混合鍵合客戶數由 2025 年底 15 家增至 Q2'26 底 21 家。（原話："Hybrid bonding customers adoption increased from 15 at"）
- 2026-07-23｜Richard Blickman｜customer：答分析師：超大規模客戶的訂單可能用於穿戴式（眼鏡）；另兩家一為 CPO、一為邏輯。（原話："the hyperscaler is probably for wearables."）
- 2026-07-23｜Richard Blickman｜competition：HBM 混合鍵合：三大記憶體廠之一正在評估，另一家剛開始評估。（原話："Also, we've indicated that another one is starting the"）
- 2026-07-23｜Richard Blickman｜competition：管理層轉述業界對 HBM 採用混合鍵合時程的不同看法（延後 vs. 近在眼前）。（原話："Some are voicing that it may delay."）
- 2026-07-23｜Richard Blickman｜competition：針對 JEDEC 放寬 HBM4E 厚度限制，管理層表示高度放寬不改變混合鍵合的效能與散熱優勢。（原話："heat or the height does not change that characteristic."）
- 2026-07-23｜Richard Blickman｜risk：管理層指出 HBM 混合鍵合量產的主要障礙是成本與良率。（原話："The major hurdles are simply cost and yield."）
- 2026-07-23｜Richard Blickman｜risk：以台灣邏輯大客戶為參照，管理層說明驗證歷時超過三年。（原話："It took us over 3 years."）
- 2026-07-23｜Richard Blickman｜risk：管理層談產能過剩：過往上行週期約 6–8 季後出現過剩。（原話："cycle last 6 quarters, maybe 8 and then you are bound to"）
- 2026-07-23｜Richard Blickman｜risk：被問是否走向產能過剩，管理層答以時間會證明。（原話："So are we heading into an overcapacity? Time will tell."）
- 2026-07-23｜Richard Blickman｜guidance：解釋 Q3 營收逆季節性成長：下游由智慧型手機轉為 AI 資料中心，訂單動能延續但組合不同。（原話："we have continued order momentum, but with a different mix."）
- 2026-07-23｜Richard Blickman｜commitment：AP7 擴產：管理層稱若按計畫，下半年可能再有一輪訂單，交期約 6 個月。（原話："we don't know, with a lead time of about 6 months"）
- 2026-07-23｜Richard Blickman｜commitment：管理層預期表現將顯著優於 Tech Insights 的市場成長預測（2025–2028 年 53%）。（原話："significantly exceed such projected growth rates"）
- 2026-07-23｜Richard Blickman｜commitment：管理層轉述客戶說法：處於多年期 AI 資本支出週期。（原話："Customers indicate that we are in a multiyear AI CapEx cycle"）
- 2026-07-23｜Richard Blickman｜capital_allocation：Q2 末淨現金增至 1.64 億歐元，可轉債轉股並支付年度股利。（原話："Our net cash position at the end of the second quarter '26"）
- 2026-07-23｜Richard Blickman｜capital_allocation：Q2 支付年度股利 1.254 億歐元。（原話："payment of EUR 125.4 million for the annual dividend"）
- 2026-07-23｜Richard Blickman｜product：TC Next 目前為單台訂單，尚未大量。（原話："single systems, not yet major volume."）
- 2026-07-23｜Richard Blickman｜product：CoWoS-like 已是訂單的重要部分，自 Q4 起持續。（原話："That's already a significant part of the orders."）
- 2026-07-23｜Richard Blickman｜product：IDM 訂單增加屬非混合鍵合的主流產品，車用仍未改善。（原話："still not very much improving is automotive."）
- 2026-07-23｜Richard Blickman｜product：混合鍵合用於高階手機的訂單尚未出現。（原話："Not yet we have seen those orders."）
- 2026-07-23｜Richard Blickman｜customer：被問台灣大客戶是否放緩，管理層稱未見放緩。（原話："but we don't see any slowdown in that."）

### BESI_Analyst_Investor_Day_BE_Semiconductor_Industries_N_V_20260618.md
- 2026-06-18｜Richard Blickman｜guidance：管理層說當天上午公布的目標模型區間由 EUR 1.5–1.9 billion 上調為 EUR 1.7–2.2 billion。（原話："up from EUR 1.5 billion to EUR 1.9 billion"）
- 2026-06-18｜Richard Blickman｜guidance：管理層提到部分分析師在第一時間的評論中對新模型略感失望。（原話："several of you, I won't call names, are a bit"）
- 2026-06-18｜Richard Blickman｜guidance：新模型 EUR 1.7–2.2 billion 中，Engine 1 部分約 EUR 1.1 billion,其餘為 Sub Micron。（原話："About EUR 1.1 billion is the Engine 1 part of that."）
- 2026-06-18｜Richard Blickman｜guidance：Sub Micron 目標由 EUR 0.5–0.9 billion 調為 EUR 0.6–1.1 billion,理由是邏輯晶片持續導入，區間差異取決於 HBM 導入。（原話："Submicron up from EUR 0.5 billion to EUR 0.9 billion"）
- 2026-06-18｜Richard Blickman｜guidance：管理層稱目標相較上次 Investor Day 提高約 15%,且對應已識別的客戶與業務。（原話："increased by about 15% versus last Investor Day"）
- 2026-06-18｜Richard Blickman｜guidance：管理層說明 HBM 導入速度會讓 Sub Micron 區間偏上緣的時點快或慢約 1–2 年。（原話："in a somewhat 1, 2 years slower trend"）
- 2026-06-18｜Peter Wiedner｜guidance：Peter Wiedner 說混合鍵合低情境(邏輯加 CPO)的機台數假設較去年模型增加 18%。（原話："we can increase that for 18% versus our last year model"）
- 2026-06-18｜Peter Wiedner｜guidance：加入手機與智慧眼鏡等邊緣裝置的高情境，整體較去年增加 12%。（原話："which then increases overall by 12%"）
- 2026-06-18｜Peter Wiedner｜guidance：混合鍵合機台累計需求的高情境上調至 2,200 台。（原話："up to a cumulative 2,200 machines"）
- 2026-06-18｜Peter Wiedner｜guidance：混合鍵合機台累計需求的低情境上調至 1,150 台。（原話："to 1,150 machines"）
- 2026-06-18｜Christoph Scheiring｜guidance：Mainstream die attach 的可及市場模型更新為 EUR 1.6 billion 水準，較上次約增 8%。（原話："addressable market model to a EUR 1.6 billion level"）
- 2026-06-18｜Christoph Scheiring｜guidance：Christoph 稱到 2030 年可及市場成長約 2 倍，並說相較去年模型上修。（原話："addressable market growing by a factor of 2 until 2030"）
- 2026-06-18｜Richard Blickman｜guidance：管理層形容目前處於 AI 帶動的大型上行循環的起點。（原話："We are at the very beginning of a significant up cycle"）
- 2026-06-18｜Richard Blickman｜guidance：舉去年例子說明模型偏保守：2025 年營收中約 40% 是年初預算之外的業務。（原話："about 40% of that EUR 600 million"）
- 2026-06-18｜Richard Blickman｜margin：管理層回顧毛利率在下行期往 62%、63% 靠。（原話："it was a bit trending towards 62%, 63%."）
- 2026-06-18｜Richard Blickman｜margin：管理層拆解口徑：淨利率低點 21%,依 Q2 毛利率與營業費用指引，淨利率會回到 30% 以上。（原話："it should move well again"）
- 2026-06-18｜Richard Blickman｜margin：管理層解釋調高營業利益率目標的理由：產品轉向更複雜的先進封裝。（原話："if you do your homework right, you have higher margins"）
- 2026-06-18｜Richard Blickman｜margin：管理層對市占率的口徑：市占是結果，先看毛利潛力。（原話："market share is an end result"）
- 2026-06-18｜Peter Wiedner｜margin：回應定價問題：每提高一級精度，機台價格都會上升，沒有給出具體數字。（原話："the price level is definitely going up with each increased"）
- 2026-06-18｜Richard Blickman｜margin：產能口徑：以每年 300 台、平均單價 2.5 million 概算混合鍵合機台產出。（原話："multiply that by 2.5 million as an average price"）
- 2026-06-18｜Christoph Scheiring｜margin：管理層稱低端製程轉向中國競爭者的業務因價格敏感、毛利不如預期而不追。（原話："we are not interested in as it is very, very price sensitive"）
- 2026-06-18｜Richard Blickman｜commitment：Richard 說明目前產能約每年 300 台混合鍵合機，下一階段已備妥。（原話："we are now at a level of building 300"）
- 2026-06-18｜Richard Blickman｜commitment：管理層承諾今年底前越南開始組裝首批鍵合機，自馬來西亞遷出部分產線。（原話："we will build the first bonders in Vietnam"）
- 2026-06-18｜Richard Blickman｜commitment：管理層說調整營運模型的方法是每次把產能加倍，這次打算準備得比加倍更多。（原話："we have always used the simple method, doubling each time"）
- 2026-06-18｜Richard Blickman｜commitment：管理層承認內部仍有改善空間，並以此說明目標調高屬自然管理。（原話："wrong in our company, there's still a lot to improve"）
- 2026-06-18｜Richard Blickman｜capital_allocation：管理層說明研發支出逐步增加。（原話："you see a gradual increase in R&D spends"）
- 2026-06-18｜Richard Blickman｜capital_allocation：對併購傳聞不回應，並稱產業併購近乎不存在，夥伴關係為主要路線。（原話："partnerships is the way to go"）
- 2026-06-18｜Peter Wiedner｜competition：Peter 稱 Besi 的混合鍵合機台路線圖與產品線沒有競爭對手能比。（原話："no other competitor of us is matching"）
- 2026-06-18｜Richard Blickman｜competition：Richard 提到市場上已宣布的混合鍵合機供應商超過 10 家，包含中國廠商。（原話："somebody counted there are over 10 Hybrid"）
- 2026-06-18｜Richard Blickman｜competition：Richard 承認是否擁有最佳鍵合機仍是挑戰。（原話："Whether we have the best bonder is still the challenge."）
- 2026-06-18｜Richard Blickman｜competition：Richard 回答領先期限：現行 100nm 為業界標準，競爭者將在下一輪切入。（原話："Competition will get in with the next round."）
- 2026-06-18｜Chris Scanlan｜competition：Chris 回應晶圓對晶圓鍵合的威脅問題：不認為對邏輯與記憶體堆疊構成威脅。（原話："we don't see a threat coming from wafer-to-wafer bonding"）
- 2026-06-18｜Peter Wiedner｜product：下一代 N50 機台(50nm 精度)的定位。（原話："which we call the N50, N50 for 50-nanometer"）
- 2026-06-18｜Peter Wiedner｜product：N50 今年開始在客戶端進行 beta 測試。（原話："start actually the beta test at the customer site this year"）
- 2026-06-18｜Peter Wiedner｜product：Peter 稱第一家 HBM 廠商將在 2027 年的 HBM4e 導入混合鍵合。（原話："will adopt the hybrid interconnect in HBM 4e in '27"）
- 2026-06-18｜Chris Scanlan｜product：Chris 重申 HBM 混合鍵合的首次導入點為 HBM4e,之後 HBM5 擴大。（原話："the intercept for hybrid bonding for HBM memory"）
- 2026-06-18｜Peter Wiedner｜product：Peter 稱 HBM5 世代時機台市場將以混合鍵合為主，而非 TCB。（原話："definitely far more than 50% will be hybrid"）
- 2026-06-18｜Peter Wiedner｜product：Peter 稱 CPO 在一年內從研發走到量產，是去年最令人興奮的發展，並放入低情境。（原話："the CPO has developed in one year into volume manufacturing"）
- 2026-06-18｜Peter Wiedner｜product：Peter 說明 HBM 仍留在中情境：為了與歷史圖表一致，而非不確定其會發生。（原話："not because we are not convinced it's not coming"）
- 2026-06-18｜Chris Scanlan｜product：Chris 稱 Arm 架構 CPU 供應商目前尚無採用混合鍵合者。（原話："for all the ARM CPU suppliers, none of them yet are using"）
- 2026-06-18｜Richard Blickman｜customer：Richard 稱已有超過 20 家客戶購買混合鍵合機。（原話："over 20 customers who have bought hybrid bonders"）
- 2026-06-18｜Peter Wiedner｜customer：Peter 稱三大 HBM 供應商都在評估混合鍵合，且都使用 Besi 機台。（原話："And by the way, they all do it with our machines."）
- 2026-06-18｜Christoph Scheiring｜customer：Christoph 稱 Chameo Flex 已完成一家客戶驗證，正等首張採購單。（原話："I'm expecting the first purchase order any moment"）
- 2026-06-18｜Christoph Scheiring｜customer：Christoph 稱 TSMC 將部分晶片對晶圓作業外包給 OSAT。（原話："TSMC decided to outsource their internal chip-to-"）
- 2026-06-18｜Peter Wiedner｜customer：Peter 稱已與美國 Terafab 團隊開始討論，對方確認會含封裝。（原話："also for us a large opportunity, the Terafab"）
- 2026-06-18｜Christoph Scheiring｜customer：Christoph 稱 Engine 1 中光子(收發器)占比將提高，部分取代過去較大的手機占比。（原話："the Photonics portion is seeing an increase"）
- 2026-06-18｜Peter Wiedner｜customer：Peter 稱手機應用處理器導入混合鍵合最大推力來自中國。（原話："I see the biggest drive for that coming out of China"）
- 2026-06-18｜Peter Wiedner｜customer：Peter 稱服務收入正加速，因混合鍵合裝在客戶前段廠，有常駐與服務合約。（原話："the service part is accelerating as we speak"）
- 2026-06-18｜Richard Blickman｜risk：Richard 提醒歷史上產業會出現高峰，表示不預測時點。（原話："if history repeats itself, that is what you should be"）
- 2026-06-18｜Richard Blickman｜risk：Richard 說產業發展從來不是直線。（原話："it's never a straight line"）
- 2026-06-18｜Christoph Scheiring｜risk：Christoph 稱中國市場競爭強度很高，受當地廠商與政策推動。（原話："the competitive intensity there is very high"）
- 2026-06-18｜Richard Blickman｜risk：Richard 稱為因應地緣政治，正檢視機台中的美國零件以減少使用。（原話："that we have less U.S. components in our"）

### 問答異常語氣（迴避／改口／保留）
- BESI_Q2_2026_Earnings_Call_20260723.md｜問：Robert Sanders（Deutsche Bank）問 2.5D 產能過剩風險最擔心什麼。｜答法：未直接指出擔憂來源，引用歷史週期統計，結尾稱『Nobody knows』並向提問者致歉無法給更好答案。
- BESI_Q2_2026_Earnings_Call_20260723.md｜問：Robert Sanders 問 Q2 混合鍵合出貨與訂單台數。｜答法：明確不揭露台數，只改報客戶數 21 家。
- BESI_Q2_2026_Earnings_Call_20260723.md｜問：Didier Scemama（BofA）與 Charles Shi（Needham）問 HBM 混合鍵合各客戶驗證進度與採用時程。｜答法：不給各家進度與時程，稱『下半年會更清楚』、『拭目以待』，僅說有一家進展最快。
- BESI_Analyst_Investor_Day_BE_Semiconductor_Industries_N_V_20260618.md｜問：Ruben Devos 追問：HBM 為何仍只放中情境、去年提的 AI 邏輯 500 台目標為何不再重複。｜答法：Peter 以保持圖表與歷史一致為由回答 HBM 的情境位置，對 500 台目標未重述數字，改談 NVIDIA 已含在先前預測中、變動主要來自 CPO。
- BESI_Analyst_Investor_Day_BE_Semiconductor_Industries_N_V_20260618.md｜問：François-Xavier Bouvignies(UBS)問下一代工具何時出現、5–10 年精度路線圖、以及機台定價空間。｜答法：定價只答價格會隨精度上升，未給數字;精度路線圖答客戶目標約 1 micron 以下，在本十年結束前，未給 N50 以外的具體時點。
- BESI_Analyst_Investor_Day_BE_Semiconductor_Industries_N_V_20260618.md｜問：Michael Roeg 追問：過去 5 年已售出逾 EUR 2 billion 設備，服務收入卻持平，為什麼。｜答法：Peter 以保固期延遲與早年混合鍵合出貨量小回答，分析師再度追問時，Peter 轉為說明覆晶機台不賣服務合約，未提供服務收入的數字。
- BESI_Analyst_Investor_Day_BE_Semiconductor_Industries_N_V_20260618.md｜問：分析師問市場對 Besi 被收購的傳聞，是否還需要夥伴。｜答法：Richard 未直接回答，只稱不回應傳聞，轉而強調對自身策略的信心與 Applied Materials 夥伴關係。
- BESI_Analyst_Investor_Day_BE_Semiconductor_Industries_N_V_20260618.md｜問：Martin Marandon(ODDO BHF)問 Besi 相對競爭者的領先幅度，以及是否有僅 Besi 進入驗證的 15nm 級產品。｜答法：Richard 未舉出具體客戶或產品例子，也說領先期限難以回答，改談 5 年後低精度段市場將出現競爭、但毛利較低。

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
{"date":"20260710","verdict":"觀望","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"混合鍵合成為 HBM4／HBM4e 與先進邏輯封裝的主流鍵合技術，BESI 維持 60%+ 份額","columns":{"2Y 驗證點":"≥2 家記憶體廠 HBM 產線導入混合鍵合量產","5Y 驗證點":"混合鍵合佔先進封裝鍵合 &gt; 30%","10Y 驗證點":"混合鍵合成為 2.5D／3D 標準製程","數字門檻":"混合鍵合份額 ≥ 60%；HBM4/4E 世代開始導入","來源":"公司法說、TrendForce、SemiEngineering","漂移觸發":"連 4 季（5Y 假設）記憶體廠明示 16-high 前不導入 → 削弱"}},{"id":"H2","text":"先進封裝 capex 上行循環延續，BESI 營收 FY2025 €591M → FY2027E €1.3B","columns":{"2Y 驗證點":"季度訂單 YoY 保持正、Q2-26 guide 兌現（+30-40%）","5Y 驗證點":"營收較 2025 谷底翻倍以上、OM 回到 35%+","10Y 驗證點":"穿越 1-2 個 capex 週期仍結構性增長","數字門檻":"FY2027E 營收 €1,309M（共識）；OM &gt; 32%","來源":"yfinance 共識、公司 guidance","漂移觸發":"連 2 季（2Y 假設）訂單 YoY &lt; 0 → 削弱"}},{"id":"H3","text":"高估值（Fwd PE 40x／P/B 43x／EV·EBITDA 96x）由獨佔性支撐、不因循環或競爭崩解","columns":{"2Y 驗證點":"Fwd PE 不跌破 25x（護城河下限）","5Y 驗證點":"ROIC（剔現金）維持 &gt; 25%、GM &gt; 60%","10Y 驗證點":"混合鍵合定價權維持、無有效第二供給","數字門檻":"GM &gt; 60%；混合鍵合份額不流失","來源":"財報、產業份額報告","漂移觸發":"連 4 季 GM &lt; 58% 或份額掉出 60% → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"先進封裝 capex 循環見頂／消化（客戶砍單）","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"季度訂單 YoY、book-to-bill","警戒閾值":"訂單 YoY 連 2 季 &lt; 0"}},{"id":"R2","text":"HBM4／HBM4E 沿用微凸塊／TCB，混合鍵合放量遞延至 HBM5（2028-2029）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"記憶體廠世代路線公告、Hanmi／K&amp;S TCB 訂單","警戒閾值":"16-high 前明示不導入混合鍵合"}},{"id":"R3","text":"韓廠（Hanmi／Hanwha／LG／SEMES）＋ ASMPT 縮小精度差距、客戶扶植第二供應源侵蝕份額","columns":{"對應假設":"H1／H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"混合鍵合份額、客戶 second-source design win","警戒閾值":"份額掉出 60%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"價格回落至 Fwd PE FY2027 ~28-32x（約 €180-210）；且／或 HBM4 混合鍵合 design-win 確認（≥2 家記憶體廠量產）化解 7/7 遞延疑慮","irr_base_pct":8.4,"ev5y_pct":43.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"核心","signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":2.7,"ev5y_pct":43.0,"irr_base_pct":8.4,"max_dd_pct":-60.0,"bull_5y_price":578.0,"bear_5y_price":146.0,"p_bull_pct":28.0,"p_bear_pct":32.0,"rearm_trigger":"價格回落至 Fwd PE FY2027 ~28-32x（約 €180-210）；且／或 HBM4 混合鍵合 design-win 確認（≥2 家記憶體廠量產）化解 7/7 遞延疑慮","price_at_dd":251.4,"archetype":"循環/商品","cycle_position":"早循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BESI_20261025/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
