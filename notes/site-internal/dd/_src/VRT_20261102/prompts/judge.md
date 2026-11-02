你是 stock-analyst **v20 判斷 agent**，標的 VRT（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"VRT","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VRT_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VRT_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":4312.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M（YoY +61.2%，QoQ +31.7%；有機 +55%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Third-Quarter-2026-with-Net-Sales-Growth-of-61-Organic-Orders-Growth-over-100-and-Diluted-EPS-Growth-of-91-Adjusted-Diluted-EPS-Growth-of-78-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/"}},{"id":"f_kpi1_adjusted_non_gaap_operat","label":"Adjusted (non-GAAP) operating profit / margin","value":1086.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M，margin 25.2%（YoY +290bp）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Third-Quarter-2026-with-Net-Sales-Growth-of-61-Organic-Orders-Growth-over-100-and-Diluted-EPS-Growth-of-91-Adjusted-Diluted-EPS-Growth-of-78-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/"}},{"id":"f_kpi2_gaap_operating_profit_ma","label":"GAAP operating profit / margin","value":983.8,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M，margin 22.8%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Third-Quarter-2026-with-Net-Sales-Growth-of-61-Organic-Orders-Growth-over-100-and-Diluted-EPS-Growth-of-91-Adjusted-Diluted-EPS-Growth-of-78-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/"}},{"id":"f_kpi3_free_cash_flow_ocf_794_0","label":"Free cash flow (OCF 794.0 − capex 139.1)","value":654.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M；公司定義 adjusted FCF 652.2","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Third-Quarter-2026-with-Net-Sales-Growth-of-61-Organic-Orders-Growth-over-100-and-Diluted-EPS-Growth-of-91-Adjusted-Diluted-EPS-Growth-of-78-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/"}},{"id":"f_kpi4_stock_based_compensation","label":"Stock-based compensation","value":19.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M；占 GAAP 營業利益 2.0%、占營收 0.5%（自算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Third-Quarter-2026-with-Net-Sales-Growth-of-61-Organic-Orders-Growth-over-100-and-Diluted-EPS-Growth-of-91-Adjusted-Diluted-EPS-Growth-of-78-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/"}},{"id":"f_kpi5_organic_orders_growth","label":"Organic orders growth","value":">100","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"% YoY（標題披露；公司已停報季度 backlog／訂單絕對值，backlog 末次 2025-12-31 為 15.0B）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Third-Quarter-2026-with-Net-Sales-Growth-of-61-Organic-Orders-Growth-over-100-and-Diluted-EPS-Growth-of-91-Adjusted-Diluted-EPS-Growth-of-78-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/"}},{"id":"f_kpi6_guidance_q4_fy2026","label":"Guidance Q4 FY2026","value":"net sales 4,313–4,513；adj op profit 1,118–1,158；adj EPS 2.22–2.28","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M / USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Third-Quarter-2026-with-Net-Sales-Growth-of-61-Organic-Orders-Growth-over-100-and-Diluted-EPS-Growth-of-91-Adjusted-Diluted-EPS-Growth-of-78-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/"}},{"id":"f_kpi7_guidance_fy2026","label":"Guidance FY2026（上調）","value":"net sales 14,450–14,850；adj op profit 3,475–3,555；adj EPS 7.10–7.20；adj FCF 2,600–2,800","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M / USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Third-Quarter-2026-with-Net-Sales-Growth-of-61-Organic-Orders-Growth-over-100-and-Diluted-EPS-Growth-of-91-Adjusted-Diluted-EPS-Growth-of-78-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_vrt_gross_margin_pct","label":"VRT 毛利率","value":38.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_operating_margin_pct","label":"VRT 營業利益率","value":20.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_fcf_margin_pct","label":"VRT FCF 利潤率","value":23.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_etn_gross_margin_pct","label":"ETN 毛利率","value":35.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_etn_operating_margin_pct","label":"ETN 營業利益率","value":17.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_etn_fcf_margin_pct","label":"ETN FCF 利潤率","value":13.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_gev_gross_margin_pct","label":"GEV 毛利率","value":21.73,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GEV.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gev_operating_margin_pct","label":"GEV 營業利益率","value":6.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GEV.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gev_fcf_margin_pct","label":"GEV FCF 利潤率","value":38.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GEV.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pwr_gross_margin_pct","label":"PWR 毛利率","value":15.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_operating_margin_pct","label":"PWR 營業利益率","value":6.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_fcf_margin_pct","label":"PWR FCF 利潤率","value":8.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_enr_de_gross_margin_pct","label":"ENR.DE 毛利率","value":20.76,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ENR.DE.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_enr_de_operating_margin_pct","label":"ENR.DE 營業利益率","value":8.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ENR.DE.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_enr_de_fcf_margin_pct","label":"ENR.DE FCF 利潤率","value":18.62,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ENR.DE.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":232.5,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-29.15,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":51.46,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.14,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.18 → 7.19）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":3.07,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.45 → 9.74）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":3.55,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.11 → 12.54）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":7.19,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":9.74,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":12.54,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":9.27,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 6.58 → 7.19（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":43.46,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝1.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":1.5,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.83,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.8,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝99.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":99.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":32.34,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 7.19，分子＝快照價 232.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.108,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-354.8,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 3356.9、現金 3711.7（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":385.06,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":89171.75,"period":"2026-11-02","unit":"USD m","basis":"市值 89526.55 ＋ 淨負債 -354.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":14712.44,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":19415.09,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（30 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":6.06,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟢","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 232.5 / W52 249.78 / W104 185.33 / W250 99.81 / W250 13週斜率 3.23%"},{"id":"f_ma_w52","label":"52 週均線","value":249.78,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":185.33,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":99.81,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":3.23,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 列出兩類主要對手：利基型（Delta、Stulz、Johnson Controls、Socomec）與大型全球型（Schneider、Eaton、Legrand、Huawei）；並警示中國、印度低成本製造商可能成為新興市場競爭者，衝擊價格與份額。","source":"SEC EDGAR 10-K FY2025 Item 1 / 1A","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":"Manufacturers in countries that have lower production costs, such as China and 21 Table of contents India, may become competitors in key emerging markets and could offer their products in established markets. These actions may have a negative effect on our pricing, market share and operating results in these markets.","as_of":"2026-02-13","retrieved_at":"2026-11-02","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"CSIMarket 以營收估算，VRT 市佔升至約 27.74%（同業集合與方法未明，僅供參考）。","source":"CSIMarket VRT Competitors","url":"https://csimarket.com/stocks/VRT-Competitors","excerpt":"due to strong revenue growth of 24.12 % in Overall company Vertiv Holdings Co improved its market share, to approximately 27.74 %.","as_of":"2026-07-29","retrieved_at":"2026-11-02","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"評論指 Schneider（併 Motivair）為主要對手，Super Micro 預整合液冷機櫃可能繞過分件採購，構成替代威脅；另有 TradingView 貼文將液冷新進入者列為中度風險。","source":"Shareholdersunite Substack, A Primer on Vertiv；TradingView ideas VRT","url":"https://shareholdersunite.substack.com/p/a-primer-on-vertiv","excerpt":"SMCI is a real competitive threat, especially in AI buildouts where customers may buy a pre-integrated liquid-cooled rack solution instead of assembling the stack from separate vendors.","as_of":"2026-01-01","retrieved_at":"2026-11-02","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因素：大型通訊、雲端/超大規模、neocloud 與主機代管業者占客戶基礎重要比重，可要求更有利合約條件","source":"SEC EDGAR 10-K FY2025 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":null,"as_of":"2026-02-13","retrieved_at":"2026-11-02","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 可能含客戶集中度／主要客戶揭露","source":"Vertiv Holdings Co Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":null,"as_of":"2026-02-25","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Vertiv Q4 2025 backlog about $15.0B, up 109% y/y, book-to-bill ~2.9x, TTM organic orders up ~81%; 2026 organic sales growth guided 27-29%.","source":"Vertiv Form 8-K exhibit 99.1 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000006/exhibit991vrt02112026.htm","excerpt":null,"as_of":"2026-02-11","retrieved_at":"2026-11-02","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Eaton $340M SC transformer plant production expected 2027; Siemens Energy Charlotte plant early 2027; GE Vernova Vietnam April 2027; Hitachi Energy South Boston 2028; analysts say meaningful relief not until after 2027; one view (Power Magazine) argues procurement practices, not capacity, are the bottleneck.","source":"Search summary of grid equipment shortage articles (Power Magazine, ecmag, greentechlead)","url":"https://www.powermag.com/transformers-in-2026-shortage-scramble-or-self-inflicted-crisis","excerpt":null,"as_of":"2026-05-11","retrieved_at":"2026-11-02","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Omdia: data center cooling growth constrained by production capacity (e.g. CDUs) rather than lack of demand; Bloomberg Intelligence projects DC infrastructure equipment from $46B (2024) to $73B (2028).","source":"Omdia via Data Center Knowledge; Bloomberg Intelligence","url":"https://www.datacenterknowledge.com/cooling/data-center-cooling-market-to-top-16b-in-2028-research-indicates","excerpt":null,"as_of":"2024-06-18","retrieved_at":"2026-11-02","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Simply Wall St flags rising customer concentration and possible in-house data center builds by large customers at Vertiv.","source":"Simply Wall St","url":"https://simplywall.st/stocks/us/capital-goods/nyse-vrt/vertiv-holdings-co/news/how-raised-2026-guidance-and-ai-data-center-demand-at-vertiv","excerpt":null,"as_of":"2026-03-01","retrieved_at":"2026-11-02","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Vertiv and Eaton posted record backlogs and raised guidance on Q2 2026 calls; Vertiv deferred revenue rose; Electrical Americas DC orders ~+65%.","source":"TIKR","url":"https://www.tikr.com/blog/vertiv-eaton-data-center-power-cooling-picks-shovels-stocks","excerpt":null,"as_of":"2026-08-01","retrieved_at":"2026-11-02","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"經查 10-K FY2025 Item 3，除 2022 年證券集體訴訟外無重大未決法律程序；SEC 執法部門 2025-12-30 告知已結束對公司調查、不建議採取執法行動。無反壟斷事項。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":"On December 30, 2025, the SEC’s Division of Enforcement informed the Company that it had concluded its investigation as to the Company and did not intend to recommend any enforcement action against the Company at this time.","as_of":"2026-02-13","retrieved_at":"2026-11-02","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋未見 2026 年針對 Vertiv 的 DOJ／FTC／歐盟競爭機關調查、訴訟或併購審查；2026 年可見調查皆為律所發起的證券詐欺調查（非政府機關），與反壟斷無關。","source":"WebSearch 摘要（DOJ/FTC/EU 與 antitrust 查詢）","url":null,"excerpt":null,"as_of":"2026-11-02","retrieved_at":"2026-11-02","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露：過去關稅曾推升美國製、輸入美國的產品成本；進出口管制變動、報復性關稅及中國可能管制稀土，可能增加成本並限制業務。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":"Changes in import and export control or trade sanctions laws, the imposition of tariffs on certain U.S. trading partners, the potential for or imposition of retaliatory tariffs, or the potential for or imposition of additional tariffs or other trade restrictions, including potential control from China on rare earth elements, may increase our costs, and may restrict our business practices","as_of":"2026-02-13","retrieved_at":"2026-11-02","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K MD&A：公司以供應商與地理韌性因應，增加區域採購與製造產能，強化美國與其他策略地區供應基礎；稱關稅可能顯著影響財務表現。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":"The imposition of U.S. tariffs and foreign country retaliatory tariffs, or the proposed imposition of additional or similar tariffs, in jurisdictions where we have manufacturing facilities or where our customers operate could increase our cost of doing business and could significantly impact our financial performance.","as_of":"2026-02-13","retrieved_at":"2026-11-02","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Q3 2026 10-Q：最高法院 2026-02 判 IEEPA 關稅無效，公司已啟動退稅申請，金額與時點不確定","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001674101/000162828026067893/vrt-20260930.htm","excerpt":"International Emergency Economic Power Act (\"IEEPA\") In February 2026, the Supreme Court issued a decision invalidating tariffs imposed under IEEPA. The U.S. Court of International Trade ordered U.S. Customs and Border Protection (“CBP”) to refund such tariffs.","as_of":"2026-10-29","retrieved_at":"2026-11-02","affects":["valuation","thesis.H"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-Q 稱美國關稅與外國報復措施已並將持續影響供應鏈與投入成本","source":"Vertiv Form 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001674101/000162828026050609/vrt-20260630.htm","excerpt":"These factors have affected, and are likely to continue to impact, supply chains, input costs","as_of":"2026-06-30","retrieved_at":"2026-11-02","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Q1 2026 財報會議：管理層擴大美國與墨西哥產能、以供應鏈重整降低關稅衝擊，最大逆風在 Q2","source":"Vertiv Q1 2026 earnings call (MarketBeat/Finviz)","url":"https://finviz.com/news/33675/vrt-q1-earnings-call-vertiv-lifts-full-year-outlook-amid-data-center-demand-tariff-management","excerpt":"supply chain realignment and pricing actions will gradually reduce the impact of tariffs throughout the year, with the largest headwinds occurring in the second quarter.","as_of":"2026-04-22","retrieved_at":"2026-11-02","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因素：部分物料來自單一來源供應商，更換可能延誤生產","source":"Vertiv Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":"Replacing a single-source supplier could delay production of some products because replacement suppliers, if available, may be subject to capacity constraints or other output limitations.","as_of":"2026-02-28","retrieved_at":"2026-11-02","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026Q3 淨銷售 $4,313M、年增 61%（有機 55%）；Americas +75%（有機 66%）、APAC +50%（有機 48%）、EMEA +23%（有機 19%）；有機訂單年增逾 100%","source":"Vertiv Q3 2026 earnings release / 8-K","url":"https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Third-Quarter-2026-with-Net-Sales-Growth-of-61-Organic-Orders-Growth-over-100-and-Diluted-EPS-Growth-of-91-Adjusted-Diluted-EPS-Growth-of-78-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/","excerpt":null,"as_of":"2026-10-28","retrieved_at":"2026-11-02","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"全年 2026 銷售指引中值上調 $650M 至 $14.65B；Q4 指引中值 $4,413M、有機約 +50%","source":"Vertiv Q3 2026 earnings release / 8-K","url":"https://www.sec.gov/Archives/edgar/data/0001674101/000162828026067707/q32026exhibit991vrt10282026.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"2026-11-02","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"法說會：Americas 管線季增為年內最快；EMEA 管線年增約一倍；APAC 有機訂單大增（澳洲、印度帶動）。公司不揭露訂單金額","source":"Q3 2026 earnings call transcript (tradingkey)","url":"https://www.tradingkey.com/news/transcripts/262248257-tradingkey","excerpt":null,"as_of":"2026-10-28","retrieved_at":"2026-11-02","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"2025 年底 book-to-bill 積壓訂單約 $15B、年增 109%；2026Q1 Americas 有機銷售 +44%，EMEA 有機 -29%","source":"Motley Fool, Data Center Demand Drove Vertiv's Earnings up 83%","url":"https://fool.com/investing/2026/05/01/data-center-demand-drove-vertivs-earnings-up-83-bu/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"2026-11-02","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"管理層預期 800V sidecar 產品需求 2027 下半年加速，原生 800V 動力系統 2027 年底商用、2028 放量","source":"thecerbatgem 報導 Vertiv 管線擴張","url":"https://www.thecerbatgem.com/?p=10390153","excerpt":null,"as_of":"2026-07-01","retrieved_at":"2026-11-02","affects":["thesis.H","triggers"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"Global Market Insights 預期資料中心液冷市場年複合成長逾 18% 至 2035，液冷滲透率低於 10%","source":"Motley Fool / Nasdaq","url":"https://www.fool.com/investing/2026/07/21/ai-chips-need-liquid-cooling-thats-why-vertivs-sto/?.tsrc=rss","excerpt":null,"as_of":"2026-07-21","retrieved_at":"2026-11-02","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Vertiv 10-K 風險因子自述：競爭者（Schneider、Eaton、Legrand、Huawei）可能推出顛覆其重要市場的新技術或商業模式，使客戶將相當部分業務移離；若未能預見技術轉變，競爭力與營收將受損。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":"Our competitors, any of which could introduce new technologies or business models that disrupt significant portions of our markets and cause our customers to move a material portion of their business away from us, primarily include:","as_of":"2026-02-13","retrieved_at":"2026-11-02","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"NVIDIA 2025年10月800V白皮書將固態變壓器(SST)列為800V DC供電的終極方案，現階段SST未成熟時可用工業整流器；Vertiv自身規劃2026下半年推出800VDC產品組合。","source":"iTiger 新聞：從800V終極架構到千億市場 SST商業化前夜","url":"https://www.itiger.com/hant/news/2645092828","excerpt":"中信建投發布研報稱，2026年以來關於SST固態變壓器進展層出不窮，SST強趨勢全球範圍形成共識。國內多家企業紛紛推出樣機產品；海外創業公司密集孖展，商業化加速推進；海外電力設備龍頭加速推進SST產品落地。數據中心用電架構的終局方案為SST已形成共識，預計將在商業化之後，SST的滲透率將快速提升，預計在2030年達到千億級市場。SST產業鏈機會將共振向上。 中信建投證券主要觀點如下： 一、 SST強趨勢全球範圍形成共識 2025年10月，英偉達發布的800V白皮書中提出，固態變壓器(Solid-State Transformer, SST)是提供800V直流的終極解決方案，能夠將中壓交流電網提供的13.8/35kV交流電一步直降800V直流。在SST技術尚不成熟的當前階段，也可以使用7.5MW級別的工業級整流器，實現一步將中壓交流電整流至直流，可以省去大部分中間轉換步驟","as_of":"2026-06-01","retrieved_at":"2026-11-02","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"液冷占全球新建AI資料中心34%（2024年12%），預測2028年達50%。","source":"Datacentres.com Research 2026-07-15","url":"https://www.datacentres.com/news/liquid-cooling-reaches-34-of-new-ai-data-centres-as-power-densities-hit-150kw-ra-slot1-2026-07-15","excerpt":null,"as_of":"2026-07-15","retrieved_at":"2026-11-02","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：主要銷售方式仍為直銷（約3,000名業務），另以通路夥伴、經銷商、IT轉售商補充；未見訂閱化或D2C的結構性轉變描述。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":"Our primary selling method is direct sales, and we have approximately 3,000 salespeople located around the world. We also utilize a robust network of channel partners, distributors, IT resellers, and value-added retailers.","as_of":"2026-02-13","retrieved_at":"2026-11-02","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q2 2026財報解讀稱公司由元件供應商轉向系統整合商（二手聚合來源）","source":"Panabee Vertiv Q2 2026 earnings write-up","url":"https://www.panabee.com/news/vertiv-earnings-q2-2026-report","excerpt":"The company is effectively shifting its business model from a component vendor to a systems integrator, evidenced by the rollout of factory-integrated modular solutions designed to reduce deployment timelines for hyperscale customers.","as_of":"2026-07-29","retrieved_at":"2026-11-02","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill 顯示 FY2026 EPS 共識 6.81 美元（38 位分析師，2026-10-17），下一季營收預估 3 個月上修約 1.3%、FY2027 EPS 上修約 3.9%","source":"Chartmill VRT estimates","url":"https://www.chartmill.com/stock/quote/VRT/estimates","excerpt":"Latest recorded estimate: 6.81 USD · Oct 17, 2026 · 38 analysts","as_of":"2026-10-17","retrieved_at":"2026-11-02","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"TickFlow 列分析師共識為 Buy，平均目標價 375.08 美元（25 位分析師，約 2026-08）","source":"TickFlow VRT forecast","url":"https://www.tickflow.io/stock/VRT/forecast","excerpt":"The consensus among 25 analysts covering Vertiv Holdings Co (VRT) is Buy with an average price target of $375.08.","as_of":"2026-08-04","retrieved_at":"2026-11-02","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga 列 23 位分析師、22 買 1 持有、平均目標價約 324 美元（約 2026-08 下旬）；目標價分布各站不一（Walnut 8 月：平均 339.35、區間 236–416，24 買 4 持有 0 賣）","source":"Benzinga VRT price targets; Walnut VRT forecast","url":"https://jp.benzinga.com/quote/VRT/price-targets","excerpt":"Analyst Consensus — 23 Analysts 22Buy 1Hold Consensus RatingBuy# Analysts23Avg.","as_of":"2026-08-28","retrieved_at":"2026-11-02","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Vertiv 於 2026-10-28（Q3）再度調升全年指引：全年淨銷售指引上調 6.5 億美元，調整後稀釋 EPS 中位數 7.15 美元；今年 4 月、7 月已各調升一次，搜尋未見下修","source":"Vertiv Q3 2026 8-K Exhibit 99.1","url":"https://www.sec.gov/Archives/edgar/data/0001674101/000162828026067707/q32026exhibit991vrt10282026.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"2026-11-02","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2（2026-07-29）：調整後 EPS 1.52 美元優於共識約 1.43，營收 32.7 億低於預估 33.8 億；全年調整後 EPS 指引 6.65–6.75 高於共識 6.47","source":"MarketBeat Vertiv Q2 results","url":"https://www.marketbeat.com/instant-alerts/vertiv-nysevrt-posts-quarterly-earnings-results-beats-estimates-by-009-eps-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"2026-11-02","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026-10-16 MarketBeat 報導 VRT 因分析師降評跌 4%，10 月多家目標價下調，平均目標價約 335.67 美元","source":"MarketBeat 2026-10-16 downgrade alert","url":"https://www.marketbeat.com/instant-alerts/price-vertiv-nyse-vrt-stock-falls-4-on-analyst-downgrade-2026-10-16/","excerpt":null,"as_of":"2026-10-16","retrieved_at":"2026-11-02","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#6","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"TIKR：Vertiv 今年兩度調升指引，市場預估仍落後","source":"TIKR blog","url":"https://www.tikr.com/blog/vertiv-raised-guidance-twice-this-year-the-street-is-still-behind","excerpt":"Vertiv Raised Guidance Twice This Year. The Street Is Still Behind. Gian Estrada • 5 minute read Reviewed by: David Hanson Last updated Jul 21, 2026 @gettyimages and @pexels","as_of":"2026-07-21","retrieved_at":"2026-11-02","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-27 完成收購 Utility Innovation Holdings（UIG），預付現金約 $1.45B，另有最高 $1.15B 盈利對賭（EBITDA 目標、分 2 期）。","source":"SEC EDGAR 8-K Item 2.01 (2026-10-27)","url":"https://www.sec.gov/Archives/edgar/data/1674101/000162828026067393/vrt-20261027.htm","excerpt":"completed the acquisition (the “Acquisition”) of Utility Innovation Holdings, Inc., a Delaware corporation (“UIG”)","as_of":"2026-10-27","retrieved_at":"2026-11-02","affects":["valuation","moat_trend","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2025-12-04 完成收購 PurgeRite，預付現金約 $1.0B，另有最高 $250M 績效對價。","source":"SEC EDGAR 8-K Item 2.01 (2025-12-05)","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410125000031/vrt-20251204.htm","excerpt":"completed the acquisition (the “Acquisition”) of all of the outstanding interests in Purge Rite Intermediate, LLC, a Delaware limited liability company (“PurgeRite”), for approximately $1.0 billion in upfront cash consideration","as_of":"2025-12-05","retrieved_at":"2026-11-02","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2022 年提起的證券集體訴訟 In re Vertiv Holdings Co Securities Litigation 仍在 SDNY 待決；Securities Act 部分 2024-01-31 已駁回，Exchange Act 部分駁回動議仍待裁定。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":"The motion to dismiss the claims under Sections 10(b) and 20(a) of the Exchange Act remains pending.","as_of":"2026-02-13","retrieved_at":"2026-11-02","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"股東衍生訴訟（Sullivan／Hanna）已合併，於 Delaware Chancery 待決。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":"The Sullivan Action has been stayed since August 10, 2023 pending the outcome of the motion to dismiss in the securities class action.","as_of":"2026-02-13","retrieved_at":"2026-11-02","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"+","claim":"SEC 執法處 2025-12-30 告知已結束調查、不擬建議執法行動（據搜尋摘要轉述 10-K FY2025，未取得逐字原文）。","source":"SEC EDGAR 10-K FY2025（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":null,"as_of":"2026-02-13","retrieved_at":"2026-11-02","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-10-27 完成收購 UIG，預付約 $1.45B，另有最高 $1.15B 盈利對賭。","source":"SEC EDGAR 8-K Item 2.01","url":"https://www.sec.gov/Archives/edgar/data/1674101/000162828026067393/vrt-20261027.htm","excerpt":"approximately $1.45 billion in upfront cash at closing","as_of":"2026-10-27","retrieved_at":"20261102","affects":["valuation","thesis.R"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"2025-12-04 完成收購 PurgeRite，預付約 $1.0B。","source":"SEC EDGAR 8-K Item 2.01","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410125000031/vrt-20251204.htm","excerpt":"for approximately $1.0 billion in upfront cash consideration","as_of":"2025-12-05","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2022 證券集體訴訟仍待決（SDNY），Exchange Act 部分駁回動議未決；另有合併後衍生訴訟。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":"The motion to dismiss the claims under Sections 10(b) and 20(a) of the Exchange Act remains pending.","as_of":"2026-02-13","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"+","claim":"2023-11 起收到 SEC 傳票；SEC 執法處 2025-12-30 告知結案、不擬建議執法行動（搜尋摘要轉述）。未見重編財報。","source":"SEC EDGAR 10-K FY2025（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm","excerpt":null,"as_of":"2026-02-13","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"VRT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.12,"operating_margin_pct":20.35,"fcf_margin_pct":23.74,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ETN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.9,"operating_margin_pct":17.71,"fcf_margin_pct":13.1,"rd_intensity_pct":2.81},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"GEV","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":21.73,"operating_margin_pct":6.43,"fcf_margin_pct":38.86,"rd_intensity_pct":3.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GEV","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"PWR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.76,"operating_margin_pct":6.81,"fcf_margin_pct":8.46,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ENR.DE","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":20.76,"operating_margin_pct":8.81,"fcf_margin_pct":18.62,"rd_intensity_pct":2.77},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ENR.DE","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"VRT"},"financial_history":{"ticker":"VRT","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":5691500000.0,"revenue_yoy_pct":null,"gross_margin_pct":28.39,"operating_margin_pct":4.0,"net_income":76600000.0,"diluted_eps":0.04,"free_cash_flow":-263800000.0,"fcf_margin_pct":-4.63,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":6863200000.0,"revenue_yoy_pct":20.59,"gross_margin_pct":34.98,"operating_margin_pct":13.36,"net_income":460200000.0,"diluted_eps":1.19,"free_cash_flow":765900000.0,"fcf_margin_pct":11.16,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":8011800000.0,"revenue_yoy_pct":16.74,"gross_margin_pct":36.62,"operating_margin_pct":17.25,"net_income":495800000.0,"diluted_eps":1.28,"free_cash_flow":1135200000.0,"fcf_margin_pct":14.17,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":10229900000.0,"revenue_yoy_pct":27.69,"gross_margin_pct":36.32,"operating_margin_pct":18.54,"net_income":1332800000.0,"diluted_eps":3.41,"free_cash_flow":1887400000.0,"fcf_margin_pct":18.45,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/VRT/VRT_Q3_2026_Earnings_Call_20261028.md）

# Q3 2026 Earnings Call
**Vertiv Holdings Co** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Good morning. My name is Warren, and I will be your conference operator today. At this time, I would like to welcome everyone to Vertiv's Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please note that this call is being recorded. I would now like to turn the program over to your host for today's conference call, Lynne Maxeiner, Vice President of Investor Relations.

**Lynne Maxeiner** (Executives):
Good morning, and welcome to Vertiv's Third Quarter 2026 Earnings Conference Call. During the course of this call, we will make forward-looking statements regarding future events, including the future financial and operating performance of Vertiv. These statements are subject to material risks and uncertainties that could cause actual results to differ materially from those in the forward-looking statements. 
We undertake no obligation to update these statements as a result of new information or future events. Please refer to the cautionary language included in today's earnings release and the risks disclosed in our annual and quarterly reports and other filings made with the SEC. Additionally, non-GAAP measures referenced today are defined and reconciled in our earnings press release and in the investor slide deck found on our website at investors.vertiv.com. [Operator Instructions] With that, I'll turn the call over to Executive Chairman, Dave Cote.

**David Cote** (Executives):
Well, to paraphrase Mark Twain, the rumors of our demise have been greatly exaggerated. I'm really pleased with the third quarter and our year-to-date performance. This performance is testament to how customers look at Vertiv, our thought leader, with leading technology and reliability, undeniable ability to scale and superior service performance and capabilities. This is reflected, among other things, in our strong Q3 organic orders on top of very strong first half organic orders, as Gio will mention. Q3 organic orders are not only strong, but also very balanced across customer types. Orders are strong no matter how you look at them with or without neoclouds. 
Our customers clearly believe in us. By the way, to be clear, we're not planning to share orders data going forward. This order strength and financial performance notwithstanding, Gio will be the first to say that we are relentlessly focused on further improving our customer and financial performance across the board. We can still be a lot better. Gio is never satisfied. What you're seeing in these results isn't something that happened overnight. This is a payoff from years of seed planting, years of investing in technology, capacity, service and all capabilities because we believe this opportunity was going to be big. It turns out, it's even bigger than most people imagined, and we believe it's going to stay big for a long time. 
We are just at the beginning of the digital age, and we anticipate it has decades left to run. The foundation for it is data storage and processing, which means data centers. No data centers, no digital age. And Vertiv supplies the picks and shovels. We are at the forefront of the technology change in those picks and shovels and intend to stay there. As you know, I've always believed it's important to have a great position in a good industry, preferably with technology differentiation and then develop a high-performance culture so you then perform well for customers and investors. 
Vertiv is doing that. I'm pleased with how rapidly the high-performance culture is developing at Vertiv. And the more technology changes, the better it is for us. It's exciting stuff. Like that famous book says, we're accomplishing 2 seemingly conflicting things at the same time. We're delivering very strong results today while investing aggressively for tomorrow. That's generally hard to do. Most companies choose one or the other. Gio and his team are doing both. And I believe the gap between us and everyone else just keeps getting wider. And the fact is we're still early. We aren't done yet, not even close. As you've heard me say in the past, buy now while supplies last. So let me hand it over to Gio to take you through it all. Gio?

**Giordano Albertazzi** (Executives):
Well, thank you very much, Dave, and let us go to Slide 3. A very strong quarter indeed. Net sales up 61% versus Q3 2025 with broad-based strength across all regions. Americas up 75%, APAC up 50% and EMEA back to convincing growth at 23%. Organic net sales grew approximately 55% with an additional 6% from acquisitions. Disciplined execution drove adjusted operating margin to 25.2%, up 290 basis points year-on-year, exceeding our guidance. Adjusted operating profit was over $1 billion, up 83% year-over-year. Adjusted diluted EPS of $2.21 were up 78%, primarily driven by higher volume and continued operational productivity. Adjusted free cash flow was up 50% year-on-year at $652 million. 
Our net cash position continued with negative leverage of 0.2x at quarter end. The balance sheet remains very strong. We are raising our full year guidance across all key metrics. Net sales expected at $14.65 billion, $650 million up on July guidance and approximately 38% organic growth. Adjusted diluted EPS now expected at $7.15, up 70% from '25. And adjusted operating profit guidance raised to more than $3.5 billion, up 68% year-on-year. Full year adjusted operating margin expected to be 24%, approximately 360 basis points higher than 2025 and adjusted free cash flow guidance raised to $2.7 billion. 
And with that, let's move to Slide 4, and I'll start with the market environment. Our pipeline remains very strong globally. Demand signals are clear and broad-based across technologies, customer types and regions. We expect another year of robust orders growth. You know we do not disclose orders and we will continue not to. But it is worth sharing that our Q3 orders were more than 100% up year-on-year organically. This to give a sense of what this strength practically translates into. Also important to share that our customer mix called hyper-enterprise, neocloud, et cetera, very much represents the market mix. Let's now talk regionally. Americas pipeline sequential quarter-to-quarter growth is the fastest we have seen all year, translating into very strong organic Q3 orders. Yes, power availability, permitting, general sentiment and construction site, skilled labor availability are pacing items, but not slowing down growth. 
We've been talking about the EMEA spring uncoiling. In Q3, the pipeline in EMEA has approximately doubled year-on-year and organic orders grew even more. Momentum is now in the market, and we see these dynamics carrying well into 2027 and beyond. When it comes to APAC, it's a broad-based strength, particularly in Australia and India. Organic orders were up substantially in the quarter in APAC. China is showing encouraging green shoots. Commercial execution continues to be favorable, and we expect positive price/cost in '26, including the current impact of tariffs and countermeasures. And now to the right of the slide, and let's talk about operations and supply chain. The sequential and year-on-year revenue growth you saw in the quarter reflects the combination of ongoing capacity expansion, improving utilization, Vertiv operating system adoption and overall disciplined backlog execution. 
It also reflects increasingly mature execution for complex converged infrastructure projects. We are making significant capacity investments globally to be well positioned to serve our customers and execute on a robust backlog. In the Americas, we announced several new or expanded facilities for infrastructure solutions, power management, thermal management and rack systems. In EMEA, we are expanding our Slovakia campus for power and thermal management and infrastructure solutions, scaling up our power facilities in India -- in Ireland, sorry. We are also on track to doubling chiller production capacity by year-end. In Asia Pacific, our new Johor, Malaysia factory is now operational, strengthening our ability to serve customers across Southeast Asia and Australia. 
These capacity additions are already contributing to our Q3 and Q4 growth. And it's not just our own capacity. We keep on proactively securing and expanding long-term capacity agreements with key suppliers to ensure they scale in lockstep with our growth. Let me also welcome Mike Resha, our new EVP of Manufacturing and Logistics. Mike brings very strong operational experience and capabilities and very strong lean expertise. Anders remains with us in a senior advisory capacity focused on a successful handover and on special projects. And let us now go to Slide 5. Time to first token matters a lot to our customers. It indicates how quickly an investment in AI data center and compute becomes revenue generating. 
I want to highlight the work we're doing with NVIDIA, the  Dassault Systemes and Polar Data Center to significantly reduce time to first token, accelerating every phase of the cycle. The design phase, for example, pre-engineered reference designs are configured and validated in a digital twin. This reduces the design time by a factor of 10. And the deployment phase, factory built and modularly deployed infrastructure significantly removes complexity from site. It happens in parallel with site preparation. This cuts deployment time by up to half. The result is up to 30% more cumulative AI token output in the first 12 months from project kickoff. Same installed capacity, just productive much sooner for our customers. Polar Data Centers is already applying this at the first 41 megawatt phase of its Heroya campus in Norway and is scalable to 100 megawatts. And with that, over to you, Craig.

**Craig Chamberlin** (Executives):
Thanks, Gio. Let's move to Slide 6 and talk through our third quarter financial results in more detail. Our adjusted diluted EPS was $2.21, up $0.97 or 78% versus prior year, and $0.41 above the midpoint of our guidance. The year-over-year improvement was driven by higher after-tax adjusted operating profit, primarily from increased revenue and operating profit rate expansion. On the top line, net sales were approximately $4.3 billion. That's up approximately $1.6 billion or 61% versus prior year. Organic sales growth was approximately 55% with an additional 6% from acquisitions. 
By region, Americas grew 66% organically. APAC grew 48% organically and EMEA grew 19% organically. All regions were above the 3Q revenue guidance. Moving to adjusted operating profit. We delivered approximately $1.1 billion. That's up $491 million or 83% versus prior year and $169 million above the midpoint of our guidance. Adjusted operating margins of 25.2% expanded 290 basis points year-over-year and came in 70 basis points above guidance. The margin expansion was driven by strong sales volume increase, operating leverage and continued productivity. The business teams continue to show the ability to scale operations while expanding margins. As we have mentioned in prior calls, we're continuing to invest in capacity and engineering R&D to support future business growth. 
To round out the quarter, adjusted free cash flow was $652 million, up $216 million or 50% from prior year. The improvement was driven by higher adjusted operating profit, partially offset by working capital usage and higher net CapEx. Net leverage at quarter end was negative 0.2x, providing significant strategic flexibility. Flipping to Slide 7, let's look at segment performance by region. Americas delivered an outstanding quarter. Net sales were approximately $3 billion, up 75% with organic growth of 66%. Organic sales growth remained robust in the quarter. Adjusted operating margin came in at 29.4%, driven by strong operational leverage. 
Moving to APAC. The region had strong results with net sales of $779 million, up 50% with organic growth of 48%. Full year outlook remains positive, driven by strong end market demand and continued commercial execution. Adjusted operating margin of 17% expanded 380 basis points year-over-year, primarily attributed to operating leverage. In EMEA, net sales were $545 million, up 23% with organic growth of 19%. The market continues to strengthen with accelerating pipeline conversion, positioning the region well for continued organic sales growth. Adjusted operating margin of 28% expanded 920 basis points year-over-year, driven by improved operational leverage and commercial execution. It was a very strong performance across all 3 regions in the third quarter. Turning to Slide 8. Let's walk through our fourth quarter 2026 guidance. For Q4, we're projecting adjusted diluted EPS of $2.25 at the midpoint. That represents 65% growth versus prior year. 
The year-over-year improvement is driven by higher after-tax adjusted operating profit, primarily from increased revenue and operating profit rate expansion. On net sales, we expect approximately $4.4 billion at the midpoint. That's up approximately $1.5 billion or 53% versus prior year. Organic sales growth is expected to be approximately 50% with an additional 3% from acquisitions. We expect continued strong organic growth across all regions with Americas in the mid-50s, APAC in the mid-50s and EMEA in the low 20s. Adjusted operating profit is expected to be approximately $1.1 billion at the midpoint. That's up approximately $470 million or 70% versus prior year. Adjusted operating margin rate is expected to be 25.8% at the midpoint. That's up 260 basis points year-over-year, and that's driven by strong organic sales growth and operating leverage, which is offsetting some small mix impact. 
As you can see, we expect another strong quarter, reflecting the ongoing excellent operational performance of our business teams. Now on to Slide 9. Let's talk about updated full year 2026 guidance. We're raising our guidance across all key metrics. Starting with the adjusted diluted EPS. We now expect $7.15 at the midpoint. That's up approximately $2.95 or 70% versus 2025 and an increase of $0.45 versus our prior guidance. The year-over-year improvement is driven by higher after-tax adjusted operating profit, primarily from increased revenue and operating profit rate expansion. For net sales, we now expect $14.65 billion at the midpoint. That's up approximately $4.4 billion or 43% versus 2025 and an increase of $650 million versus our prior guidance. 
Organic sales growth is expected to be approximately 38% with an additional 4% from acquisitions and 1% from favorable currency. By region, we expect Americas organic growth in the high 40s, APAC in the mid-30s and EMEA in the low to mid-single digits. Moving to adjusted operating profit. We now expect approximately $3.5 billion at the midpoint. That's up approximately $1.4 billion or 68% versus 2025 and an increase of $190 million versus our prior guidance. Adjusted operating margin is expected to be 24% at the midpoint. That's approximately 360 basis points of expansion from 2025 and 20 basis points above our prior guidance. 
The margin expansion is driven by strong organic sales growth, continued operating leverage and ongoing productivity realization. Finally, adjusted free cash flow is expected to be $2.7 billion at the midpoint. That's up $813 million or 43% versus 2025. The year-over-year improvement is driven by higher adjusted operating profit and cash interest favorability, partially offset by higher net CapEx as we continue to invest in capacity expansion and operating capability. We're delivering strong results, raising our outlook and executing with discipline. With that, I'll hand it back to you, Gio.

**Giordano Albertazzi** (Executives):
Well, thank you, Craig. And let's go to Slide 10 for some initial thoughts on 2027. Data center demand is accelerating despite pacing items like power availability, permitting some data center sentiment headwinds, shortage of skilled labor for site activity. Many of these pacing items are not headwinds for us. They play directly to Vertiv's strengths as we help the industry solve them. With a robust backlog and strong pipeline visibility, we expect continued significant above-market organic sales growth in 2027. We will continue investing in engineering and R&D for the next-generation technology, expanding capacity and scaling our supply chain and services to widen our competitive lead and stay ahead of our customers' evolving needs and time lines. 
Growing at this pace is a lot of work and not always orderly, but we are clearly demonstrating the operational strength to deliver on this challenge. Despite an ongoing inflationary environment, we expect continued margin expansion powered by productivity, strong commercial execution, operational rigor and increasingly deep Vertiv operating system adoption. We expect to continue generating significant adjusted free cash flow, enabling strategic reinvestment in engineering and R&D while expanding capacity and pursuing targeted acquisitions that drive shareholder value. The demand environment remains strong heading into 2027, and we believe we are well positioned to capture it and gain market share. We expect strong growth across all financial metrics. 
And let us go to Slide 11 and wrap up. A strong Q3 performance exceeded guidance, the team continues to raise the bar. We raised our 2026 guidance across all key metrics and feel good about how we will end the year and the momentum we carry into 2027. We closed the acquisition of UtilityInnovation Group, adding microgrid solution, advanced power controls and behind-the-meter power design capabilities. We also closed the acquisition of King Environmental Services, expanding our fluid management and load-testing services in Europe. I also want to provide further evidence of the strength of our execution through a couple of examples. First, our long-tenured partnership with EdgeConneX and the design engineering and construction management firm, BCEI. They continue to expand globally with Vertiv as their preferred end-to-end powertrain, thermal chain and services partner. 
Vertiv's innovation, quality, scale and reliability are enabling the deployment of gigawatt scale facilities across multiple locations. We are proud of the trust this customer has in Vertiv to deliver at scale. Next, our collaboration with SGC Energy and KT Cloud on the Gunsan AI data center project in South Korea, designed to enable scalable high-density AI data centers. The project is utilizing our converged infrastructure to accelerate time to token and deliver at scale. Global reach, technical depth, quality and reliability, scale and industrial-leading services define Vertiv's value proposition. And with that, I think it's time to go to the Q&A part.

**Operator** (Operator):
[Operator Instructions] The first question comes from Amit Daryanani with Evercore.

**Amit Daryanani** (Analysts):
Gio, extremely impressive set of numbers for September quarter, and you're seeing 100% plus order growth right now, which I think is well in excess of the underlying gigawatts of capacity addition the AI ecosystem would do going forward. This would almost imply that Vertiv is actually picking up market share at this point, which I think is very different from the investor concerns that are around -- throughout the quarter around product quality and potential share loss. Perhaps if you think about the strength in September, the 100% plus order growth, can you just talk about how much of this was catch-up versus underlying demand getting better? And to the extent you can focus in on your share within these AI deployments and how that's evolving, that would be really helpful.

**Giordano Albertazzi** (Executives):
Well, thank you, Amit. And as you're saying, we strongly believe that this growth is above the market growth. If you go back to the market model that we shared with you in May, and we believe that's pretty intact in terms of outlook of the market, that is squarely there. So if we continue to talk about orders and our orders trajectory and specifically talk about Q3 here. But as you heard, we're pretty positive about kind of orders more broadly speaking. But it is, I think, a way to demonstrate that the industry believes in Vertiv and that our technology, our execution, our customer -- strength of our customer relationships and our ability to deliver are certainly serving our customers very, very well. Is it a catch-up? And I'm not talking about catch-up here. We're talking about orders. So orders are a reflection of strength in the market.

**Operator** (Operator):
Your next question comes from the line of Scott Davis with Melius Research.

**Scott Davis** (Analysts):
Congrats on the very strong snapback in numbers here. Gio, I want to just follow on a little bit on Amit's question there. As it relates to some of the chatter out there of supply chain issues and such and also product quality issues. There's been chatter of compressors that have been burning out and heat levels and UPS machines or UPS systems that are overheating. And would you -- I mean, could you give us a little bit of color? I mean one could characterize as kind of normal product development challenges and one could characterize it as a door opening for competitors. So how do you guys think about it? And should we have confidence given the numbers you just provided that these issues are all seemingly overblown, and we should just look onward? And I'll pass it on after that.

**Giordano Albertazzi** (Executives):
Well, thank you, Scott. Well, again, best answer is our performance. Certainly, we operate at high levels of growth and a very vibrant environment when it comes to new products being launched. Many of these new products are new to the industry, if you will. So this growth and this new product situation is always creating acceleration across the portfolio. But when we see -- we look at the quality data, we are optimistic about what we see. We are -- we feel good about the trajectory. We feel good about the direction. When it comes to new products, it's true that if the new product mix is higher, then there is a kind of a higher, let's say, statistically distributed curve in the initial phase of new products. 
So there might be a mix there. But when we look at the way, the infant phase of a new product quality evolves, how it evolves, we see improvements, constant improvements. So we feel good about that. And it is a complicated industry. It is a complicated set of products, and that's true across the entire industry. It's not just a Vertiv thing. So I feel pretty good at where we are. We are not perfect. Absolutely, we're not perfect, but we believe that we continue to reinforce and focus on quality and reliability as one of the competitive advantages for us.

**Operator** (Operator):
Your next question comes from the line of Steve Tusa with Wells Fargo.

**Charles Stephen Tusa** (Analysts):
Can we just get an update on the supply chain issues from the second quarter, how those played out and whether you are actually, kind of, like, capturing that revenue into this year? And then just CapEx, maybe a preview of CapEx for 2027.

**Craig Chamberlin** (Executives):
Yes. So I'd say -- thanks, Steve. On the kind of a recap of the 2Q, some of that revenue, the delayed revenue did filter into the third quarter numbers. So I think we capped it somewhere around $100 million to $150 million. I think that was some of the recovery we felt in the third quarter. In terms of our feeling of where we sit right now, again, we're continuing to build up those resiliencies in those factories and ensuring that they can deliver the project level outcomes that we expect to. So we said before that it was going to be an ongoing thing that we're continuing to improve at. 
We saw some definite improvements in third quarter. So that was what you felt come through, and we saw some recovery of that in the revenue basis. But we're going to continue to work on making sure that we can deliver at a steady pace and an ongoing pace around those project level outcomes. So I think for us, it's continued effort there. And we did put the capacity in place, as you saw. A little bit of that capacity does drive some of the margin things that we've talked about, but definitely put the capacity in place. And on your question, we won't highlight 2027 now from an outlook on what our percentage of CapEx would be. Again, we've given a guide for that in the long-term guidance, so we'd update any of that as we got through fourth quarter.

**Operator** (Operator):
Your next question comes from Joe O'Dea with Vertical Research.

**Joseph O'Dea** (Analysts):
Can you just talk about the mix dynamics in Americas and some of the margin spread there, even if not quantified, just trying to think through the opportunities moving forward as you sort of gain some efficiencies on new products and thinking about what that could mean for margin expansion as you see a narrowing spread between some of these buckets?

**Craig Chamberlin** (Executives):
Yes. Yes, I would say you're exactly right. So some of the margin you're seeing in Americas, again, the incrementals are a little bit lower in the second half than they were in the first half because of some favorable comps. But you also see there, Joe, in the second half that Americas had a large ramp in capacity, which would drive some inefficiency there. So -- and then on the point of the mix, the mix would be that the product side of that had more output than normal in terms of services. So you got a little bit of a mix factor there. So as that balances back out, you might have a little bit of a pickup on the mix there. 
And as we got better in terms of bringing our capacity online and getting through that learning curve, you have some potential there as well to continue to work through your margins. I would say, as we think about growing this business and the level we're growing it and bringing on capacity, we're always being prudent about how we do that and creating capabilities. So we'll continue to do that. And I think the 30% to 35% that we put out there is the right way to think about it, 30% always being when we're kind of in the ramp mode and trying to make sure we stay there and the high end of that being 35%.

**Operator** (Operator):
Your next question comes from the line of Andrew Obin with Bank of America.

**Andrew Obin** (Analysts):
Just maybe can we talk about your service organization? It seems like a big differentiator in the market. Can you share some KPIs and particularly, we're getting quite a few questions about any difference in attachment rates on electrical and thermal, and how should we think about the opportunity there going forward?

**Giordano Albertazzi** (Executives):
Well, thank you for your question. Of course, services is a very important differentiator for us. We've been vocal and we continue to believe and we have proof of the fact that it is making a difference. And it's making a difference, especially when the industry is complex and when there are a lot of new technology being deployed, so particularly in these times. We will not go into details of attach rates, but let's talk directionally. We're pleased by the direction in which our attach rates are evolving. That's a metric that we obsessively, and obsessively and very granularly measure regionally product line, everything. I would say that the -- they're not necessarily a dramatic difference between the electrical and mechanical part, is more specific maybe to some product lines within the larger groups of technologies. But again, you heard us talk about converged infrastructure, we talked about system level, all things that create even further opportunities for attachment on a broader installed base. So we are pleased with where we are going.

**Operator** (Operator):
Your next question comes from the line of Andy Kaplowitz with Citigroup.

**Andrew Kaplowitz** (Analysts):
Gio, maybe you could further characterize the order pipeline for us. I think you suggest it continues to grow, but does it continue to maybe widen out by geography as you go into '27? Obviously, the biggest opportunity seems to continue to be in the U.S., but how big of an opportunity is Europe these days or interestingly, India as you go into '27 and beyond?

**Giordano Albertazzi** (Executives):
I go back to what I was saying in terms of pipeline and strength, the broad-based strength. Of course, we start from the Americas for us, which, of course, the central gravity of the Americas for us is -- and for the market is the U.S. that is intrinsically, absolutely, unequivocally the largest market in the world. So I was very explicit about the fact that we are very pleased about pipeline growth in the Americas. Very pleased in terms of an absolute acceleration of pipeline in the Americas in the third quarter. 
The situation is certainly very, very convincing also outside. So I think it's very widespread geographically, though, of course, in some markets, the starting point is smaller, sometimes very much smaller than the Americas. But that's okay. It's relative growth that matters. We were talking about the strength in EMEA and the acceleration in EMEA. When it comes specifically to India, as you were asking, an extremely convincing landscape, an extremely convincing landscape in terms of the combination of the pipeline and our strength in the market. So please don't think that it's only the Americas, but please be convinced with us that the Americas is an absolutely strong market for us.

**Operator** (Operator):
Your next question comes from Mark Delaney with Goldman Sachs.

**Mark Delaney** (Analysts):
Congratulations on the strong results. Gio, I was hoping you could give us a bit more of an update on the 800-volt momentum. I know a number of different products that Vertiv is bringing to market with respect to 800 volt. Can you share a bit more around how that customer momentum is progressing and how impactful 800-volt products may be for revenue in 2027?

**Giordano Albertazzi** (Executives):
Thank you for the question. Certainly, a very important one. We were pretty explicit about our road map and what we see in the market when in July, we dedicated one page of our earnings deck to the evolution of power infrastructure, including the 800-volt DC. Remember, we talked about 3 model configurations. It's probably more complex than that, but from the current infrastructure to the 800-volt DC, to the rack and the row all the way to an end-to-end 800-volt DC. I'd say that the situation continues to be consistent with that. 
We are pleased with the direction of travel as Vertiv and the demand in the market is evolving in the same direction that we described pretty much 3 months ago with a -- let's say, initial 800 volt to the rack with medium voltage AC or low-voltage AC with BESS as an intermediate, if you will, configuration when going to the full 800-volt DC being in the validation part as we speak and starting to be revenue generating during 2027, and 2027 being the validation -- customer validation phase of the full native 800-volt DC and then the deployment into the market in '28. So pretty much the same picture we saw back then, pretty pleased about our trajectory and very consistent with what we shared in May and in July.

**Operator** (Operator):
Your next question comes from Amit Mehrotra with UBS.

**Amit Mehrotra** (Analysts):
I guess I wanted to ask about maybe just overly tactical first. Usually, you see a pretty nice step-up in revenue 3Q to 4Q. The guidance implies sort of more sequentially flat. Obviously, 3Q was much better. So maybe you can just address that. And then as all this capacity is coming online and the pipeline is great and orders are great, is that jump-off point in 4Q in terms of organic growth sort of the right way to think about growth in '27? And maybe if you don't want to answer it that precisely, is there any reason why organic growth doesn't accelerate in '27 in light of capacity and order momentum sort of moving in the right direction?

**Craig Chamberlin** (Executives):
Thanks, Amit. I'll start with the second quarter to third quarter kind of delay that kind of raised up third quarter a little bit there. So we had that delay in second quarter of revenue recognition came in, in third quarter. So brought third quarter up a little bit more than would have historically been there. So if you adjust for that $100 million to $150 million, you're more in a sequential nature that we've seen in the past from the third quarter to fourth quarter number, if you look at that for the guide. 
So I think that's a little bit of a normalization there. And again, as Gio and I have said, as we walk through these things, there's always some prudence in the way that we look at our guide. So our fourth quarter guide would be assessing for that as well. In terms of kind of where does it sit as going into 2027, again, we feel good about where we are right now in exiting the year. We won't comment on 2027 of where it's going to go. But just to point back to the fact of pipelines look good. As Gio mentioned, the order book looks good, and we feel confident about our ability to execute given the third quarter and what we have in front of us here in the fourth quarter.

**David Cote** (Executives):
By the way, Amit, while I got you, I loved your headline today, too. Well done.

**Operator** (Operator):
Your next question comes from Toby Okwara with Morgan Stanley.

**Tobenna Okwara** (Analysts):
I wanted to talk about the inventory dynamic into the quarter. It was a pretty sizable ramp up over 100% year-over-year. Is that kind of just a reset of your normal operating positioning? Or is that part of a transitional phase as you start to readjust supply chains to support modular?

**Craig Chamberlin** (Executives):
I mean I think it's a little bit of both. It's definitely the ramp to support the growth that we have and ensuring that we have the right level of resiliency in the factory as well as we talked about last quarter. So you're getting kind of a feed through on both of those, Toby, that's causing that ramp in inventory. So it's definitely to support the go-forward growth, but it's also to ensure that we have the right level of resiliency as we get more into this pattern of delivering the projects like a product level business.

**Tobenna Okwara** (Analysts):
And then if I could follow up on any commentary on mix of liquid cooling. Have you started to see that take greater share of your order book and revenues? And how should we think about the potential margin impact there?

**Giordano Albertazzi** (Executives):
We will not be specific. We've never been specific, but we've been, in other occasions, vocal about our found, let's say, satisfaction with the direction of travel, if you will, of our liquid cooling business. So not only liquid cooling is becoming a much -- taking a much bigger share of the, let's say, first level heat extraction. So the mix is definitely moving towards liquid cooling in the market, but we're also very, very satisfied about our role in the industry and our win rates and dare I say, leadership in this part of the business. It doesn't mean that air cooling is going away, as we said several times, even if it's a small portion -- a smaller portion of, let's say, the total heat extracted from individual high-density rack. There's still a lot of air being extracted. But I'd say that as this evolves, what I think is extremely -- becomes even more important and prominent is the system level. 
So the coordination between the liquid cooling, the air cooling and the heat rejection, so the power -- sorry, the total thermal chain system. You were talking about what direction is it mixing us from a margin standpoint, I'd say we're pretty pleased and fully factored in, of course, the numbers that you see and the numbers that we guide for the rest of the year, but we feel good about liquid cooling across the board, including the service attached side.

**Operator** (Operator):
Your next question comes from Nigel Coe with Wolfe Research.

**Nigel Coe** (Analysts):
Gio, maybe talk about -- there's obviously been a lot of noise around your internal supply chain. Maybe just talk about what kind of -- what measures you took to enable obviously, the incredible ramp-up kind of in the third quarter. And then maybe just kind of touch on your sort of degree of satisfaction right now and where you are right now and where you can improve. And then just that leads into my question around the hire of the new EVP of Manufacturing Supply Chain. What are you hoping that Mike brings to your organization? And any problems that you're hoping he can solve?

**Giordano Albertazzi** (Executives):
When it comes to dynamics, Craig explained a little bit the dynamics in terms of revenue recognition in Q2, Q3, et cetera. We were very transparent and explicit about the fact that what we are doing in terms of bringing it into a factory, the incredible complexity that you have on site requires building processes, building, maturing a modus operandi that is first to the market. And I would say unique still in our industry. We progressed well. I'm pleased with the progress on our learning curve that is a combination of how we execute and how we really architect the entire system, how it works. So pretty pleased about that. Are we done? Not yet, but not in terms of feeling nervous about the future, but feeling fully kind of satisfied about having developed the perfect and having matured across the perfect process. That is something that will continue to evolve. 
And that is something that will continue to create a competitive advantage for us. I think we are ahead in the industry and still work to do, but pleased with the direction we're going. Your question about Mike, and I have an opportunity to welcome again, Mike, and a big thank you for what -- everything that Anders have done. We continue to expand. We continue to take the operational execution to the next level. So there's nothing specific that I would say that's the one thing that will be addressed. This is a very convincing and broad-reaching evolution towards operational excellence, towards a fully mature Vertiv operating system, and that's the direction Mike will continue to drive towards, and he is extremely qualified for that.

**Operator** (Operator):
Your next question comes from the line of Nicole DeBlase with Deutsche Bank.

**Nicole DeBlase** (Analysts):
Gio, you highlighted a number of times some of the pacing factors, power availability, permitting, moratoriums, et cetera. Just curious, like if you look from a higher level of, like, how the cadence of your shipments is coming together and when customers are asking for shipments, are you seeing any evidence of data center construction projects pushing to the right because of these pacing items?

**Giordano Albertazzi** (Executives):
What we see in terms of movements at project level is nothing out of the ordinary from what we have seen in the industry over the years. So it's a construction activity. So sometimes there are slippages. There are complexities on site. Some of the complexity, of course, we are addressing changing the name of the game with our converged infrastructure. But we do not see those dynamics translating into meaningful or, let's say, material out of the ordinary shifts. Clearly, customers and the customers we work with are pretty savvy. And I know that when they start the project, they start procuring material and technology for that project when they know that the project can be taken to completion.

**Operator** (Operator):
Your next question comes from the line of Luke Junk with Baird.

**Luke Junk** (Analysts):
Gio, maybe a little bigger picture question. I think you had previously said you were planning portfolio launches for 800 volt in the second half of this year. Can you just comment on where that stands from an industrialization standpoint right now? And then secondarily, maybe if there's any color you could share on the scope of that opportunity in terms of your relationship with chip makers versus hyperscalers and maybe where you're most engaged right now or even what's animating what might be going into backlog?

**Giordano Albertazzi** (Executives):
As I was saying, we're pleased with the progress right now. When it comes to the way we think about product launches today, we cannot think in terms of product launches separate from having the right capacity, dedicated production line, dedicated supply chains with us. So that's an increase -- sorry, it's part of a new product and new technology launch. So certainly, 800-volt DC in its various guises, as I explained earlier when answering to a previous question, be it 800-volt DC to the rack or the pod or the entire 800-volt DC is no exception to that. 
If anything, it's certainly, let's say, a pinnacle of where we have to match supply chain footprint, capacity and technology all at the same time, and that's what we're doing. So the industrialization is an intrinsic part of the product launch. When it comes to who are we working with on the customer and customer validation standpoint, it's really a combination of customers, hyperscalers and partners on the silicon side. But I will not be much more specific than that.

**Operator** (Operator):
Your next question comes from the line of Ananda Baruah with Loop Capital.

**Ananda Baruah** (Analysts):
Gio, would just love to get your thoughts on the DSX POD that NVIDIA announced last week, which is intended to, as you well know, because you're partners, speed up kind of time to stand up. And they also have this broader, as you're aware, DSX AI factory platform. If that gains any real momentum, does that help you guys faster to revenue? Or is that -- is it more like the data center takes sort of a set amount of time to set up and it's more time to first token for them, but not necessarily an impact to you? But just wondering if it can increase your velocity of orders to revenue.

**Giordano Albertazzi** (Executives):
Well, clearly, very much involved in everything DSX, be it the DSX POD or the broader DSX AI factory data center design, very, very involved, and that's public information, as you know. As you correctly say, the fundamental driver is time to token, and the value, as I mentioned in one of the early slides, the value is -- can be billions of dollars for our customers. So clearly, there is an acceleration of -- very strong appetite for acceleration across the entire industry. We were explicit and we've been very explicit about our converged infrastructure, modular converged infrastructure, where you have reference designs that then gets configured more and more, as I mentioned, using simulation and digital twin to compress not only the deployment time, but also the design time so that we do not design snowflakes, but we go about deploying things that have already been engineered and are just tailored on a specific data center. 
So what we're doing with the converged infrastructure, OneCore, SmartRun and what we are doing together with NVIDIA on the DSX, be it the pod or the broader, it's exactly going in the same direction. So we shared that ambition. We shared that vision. And I was talking about us accelerating the learning curve of being operationally excellent in everything execution of those complex, let's say, delivery processes that is exactly going into the direction of creating a competitive advantage. Acceleration? Well, certainly, we believe that this will continue to expand our -- goes in the direction of us expanding market share and certainly works very well as a very strong technology pull-through vehicle for us.

**Operator** (Operator):
Your next question comes from Varun Govindaraj with Bernstein.

**Varun Govindaraj** (Analysts):
Congratulations on the strong quarter. I had a quick question on orders/backlog. Do you continue to see customers essentially widening the aperture to which they're willing to put in orders for? I mean said another way, are they just placing orders further down the time line? And is that having any impact on the backlog? Because in the past, you've said 12 to 18 months. Is that still the range? Or has it shifted around a little bit?

**Giordano Albertazzi** (Executives):
Well, thank you for the question. It is an important question for us, and it's around what is the -- what is backlog coverage here. The dynamics of orders in terms of how far out orders are placed, that has not changed dramatically. I would say not changed a lot quarter-to-quarter in the last few quarters. We're talking about that 12, 18 months and can be very, very much true right now. And it is -- that's certainly one of the aspects that we analyze a lot. Clearly, as you all very well remember, we are very strict in what we call backlog. We don't call a capacity agreement backlog. We only call backlog what is squarely a purchase order. So no, I would say the shape of the backlog has not changed dramatically, of course. Orders are very strong news as we were saying. So you can imagine that reflect in our backlog.

**Operator** (Operator):
Your next question comes from Andrew Buscaglia with BNP Paribas.

**Andrew Buscaglia** (Analysts):
Just wondering as we look into '27, anything you'd like to set us up with in terms of margins? And I say that's because we have some noise in the back half of this year, but it seems like the setup with incremental volume and better mix and capacity going away should set you up for, I think, what should be a really strong starting point. Do we see these kind of exit margins as the starting point for next year?

**Craig Chamberlin** (Executives):
No, we won't specifically talk about 2027 in terms of where we sit on incrementals. I'd say historically, what we've said and kind of go forward of what we laid out in the long-term planning is we aim to be at the 30% to 35%. A lot of things can influence that, especially when you're going through growth. And if you go through growth, you tend to see a little bit lower of that. If you are more of a steady state, you see a little bit of a higher of that based on where your volume is. So I'd say that's still the right framework to look at it through. We wouldn't change our framework at all, but I won't specifically comment on 2027 until we provide guidance for that at the end of next quarter.

**Operator** (Operator):
Your next question comes from Noah Kaye with Oppenheimer.

**Noah Kaye** (Analysts):
And just a follow-up there. Incremental margins sequentially from 3Q to 4Q are above the historical average. And I guess in the absence of any other factors, that would imply you are getting more efficient as you ramp these new offerings. So maybe you can comment on if that's the right read or if there are any kind of timing expense-related benefits in the quarter. And the corollary to that is really the EMEA margins, which continue to step up. Are these levels sustainable?

**Craig Chamberlin** (Executives):
Yes. I mean, again, I think you do see a little bit of a pickup on the third quarter to fourth quarter incremental margins. I wouldn't say it's significant. You are feeling a little bit of a pickup there from APAC getting -- when I say they're [ facilitated ] online more, you see that a little bit. And then again, you still see some good pull-through on EMEA. So again, I don't think it's materially different from third quarter to fourth quarter, but definitely, you're feeling the positive impacts of EMEA and you're feeling the positive impacts of APAC getting more, let's say, their facility running at a more standard basis.

**Operator** (Operator):
Your next question comes from David Tarantino with KeyBanc Capital Markets.

**David Tarantino** (Analysts):
Maybe just on capital allocation and UtilityInnovation Group specifically. Can you talk about the opportunities about moving up to the grid interconnect part of the market as behind-the-meter power is increasingly leveraged? And then maybe more broadly on capital allocation, even incorporating these deals, the balance sheet is still pristine. How should we think about capital allocation moving forward? And would you consider doing opportunistic buybacks in this kind of choppy market?

**Craig Chamberlin** (Executives):
I'll start with the capital allocation question first. Again, I don't think our strategy will change there. We have cash on the balance sheet. We like to have the dry powder to be able to do investments in both ourselves and investments in inorganic plays that we believe are scalable, and we believe those are the right levels of returns we'd like. We'll continuously look at things like buybacks and dividends and stuff like that. But in terms of where we see the most value-accretive nature is investing in our own capabilities and capacity and/or inorganic plays. 
On your question on UIG, I think it was a strategic play that allows us to get at the table sooner, allows us to get into the conversation of the architecture sooner. And so that was a unique position where we could go up further the value chain and start the conversation of how do you architect all the way back to the data center with Vertiv products. And we think it's a great hit for us to be able to do that, and it will be very synergistic to start the conversation earlier of what architecture is in the data center and what architecture is at the microgrid. So I don't know, Gio, if you wanted to add anything.

**Giordano Albertazzi** (Executives):
No, I think you explained it very well. So I'm very pleased about that and looking forward to adding this segment to our powertrain.

**Operator** (Operator):
There are no further questions at this time. Thank you. This concludes our question-and-answer session. I would like to turn the conference back over to Gio Albertazzi for any closing remarks.

**Giordano Albertazzi** (Executives):
Well, thank you, Warren, and thank you all for the questions and for your time today. This was a quarter where the organization showed what it's made of. The opportunity in front of us is significant and it is durable. Our customers are building at scale and complexity that this industry has never seen. And they need partners who can scale technology, execution, quality, reliability and services. That is where the Vertiv team -- that's what the Vertiv team does. I am proud of what we accomplished this quarter, proud and pleased, but certainly never satisfied. There is more ahead, and we are ready for it. With that, thank you all.

**Operator** (Operator):
The conference has now concluded. Thank you for attending today's presentation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### VRT_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO Craig Chamberlin｜guidance：全年淨銷售上調至 140 億美元中點，較前次加 2.5 億（原話："For net sales, we now expect $14 billion at the midpoint."）
- 2026-07-29｜CFO Craig Chamberlin｜guidance：全年調整後 EPS 中點 6.70 美元，區間 6.65–6.75，較前次中點加 0.35（原話："we now expect $6.70 at the midpoint. That's up $2.50"）
- 2026-07-29｜CFO Craig Chamberlin｜guidance：全年調整後營業利益率中點 23.8%，較前次指引加 50bp（原話："Adjusted operating margin is expected to be 23.8% at the mid"）
- 2026-07-29｜CFO Craig Chamberlin｜guidance：全年自由現金流指引中點 25 億美元（原話："adjusted free cash flow is expected to be $2.5 billion at th"）
- 2026-07-29｜CFO Craig Chamberlin｜guidance：Q3 指引：EPS 中點 1.80，銷售 37.5 億（原話："we're projecting adjusted diluted EPS of $1.80 at the midpoi"）
- 2026-07-29｜CFO Craig Chamberlin｜guidance：Q3 營業利益率指引中點 24.5%（原話："Adjusted operating margin is expected to be 24.5% at the mid"）
- 2026-07-29｜CFO Craig Chamberlin｜guidance：Q3 分區有機成長指引：美洲與亞太高 30%、EMEA 中段十幾%（原話："By region, we expect Americas organic growth in the high 30s"）
- 2026-07-29｜CEO Giordano Albertazzi｜guidance：全年預期正的價格成本，含關稅及反制措施影響（原話："We expect positive price cost in '26, including the current"）
- 2026-07-29｜CEO Giordano Albertazzi｜guidance：CapEx 預計落在占 2026 年銷售 4% 區間的高端（原話："we now expect to be at the high end of our range, 4% of '26"）
- 2026-07-29｜CEO Giordano Albertazzi｜guidance：管理層預期下半年成長 45%（原話："not just for the 45% growth we expect in the second half"）
- 2026-07-29｜CFO Craig Chamberlin｜margin：Q2 調整後營業利益率 22.6%，年增 410bp，高於指引 140bp；拆解為營運執行、生產力、價格成本，被關稅部分抵銷（原話："The margin expansion was driven by strong operational execut"）
- 2026-07-29｜CEO Giordano Albertazzi｜margin：Q2 營收成長拆解：有機 18%、併購 5%、匯率 1%（原話："On an organic basis, net sales grew 18% with additional 5% f"）
- 2026-07-29｜CFO Craig Chamberlin｜margin：EMEA 利益率年增 380bp 部分來自去年愛爾蘭問題造成的低基期（原話："the gain that you saw in margin was a favorable comp too."）
- 2026-07-29｜CFO Craig Chamberlin｜margin：Q2 自由現金流 9.25 億，來源含專案里程碑收款（含初期預付款）；遞延收入增加來自預付款與里程碑（原話："including project milestone collections, which is inclusive"）
- 2026-07-29｜CFO Craig Chamberlin｜margin：遞延收入結構與前幾季同口徑，無結構性變化；差異來自 Q4 大量專案訂單（原話："But no structural change in the way that we would recognize"）
- 2026-07-29｜CEO Giordano Albertazzi｜risk：Q2 營收出現時間差，歸因多階段專案執行與暫時性供應鏈因素（原話："primarily driven by multiphase project execution and tempora"）
- 2026-07-29｜CFO Craig Chamberlin｜risk：CFO 稱美洲的時間延遲預期在 2026 下半年化解（原話："we expect the associated timing delay to resolve in the seco"）
- 2026-07-29｜CEO Giordano Albertazzi｜risk：供應鏈互相依賴也來自 Vertiv 內部工廠，非僅外部供應商（原話："this supply chain is not necessarily an external supply chai"）
- 2026-07-29｜CFO Craig Chamberlin｜risk：CFO 說明大型專案的供應鏈延遲有放大效應（原話："when it becomes a larger supply chain, it becomes"）
- 2026-07-29｜CEO Giordano Albertazzi｜risk：分析師問是否為持續性問題，CEO 承認複雜度上升且有學習曲線（原話："complexity is increasing. Some of the projects"）
- 2026-07-29｜CEO Giordano Albertazzi｜commitment：管理層稱下半年指引留有緩衝，不假設一切順利（原話："we're not assuming all stars aligned."）
- 2026-07-29｜CFO Craig Chamberlin｜commitment：CFO 稱下半年指引已假設供應鏈壅塞持續，專案上可能比平常更多（原話："we've also assumed some of that congestion continues as we n"）
- 2026-07-29｜CEO Giordano Albertazzi｜commitment：CEO 以三層說明下半年達成依據：營運加速、產能釋出、backlog 覆蓋（原話："The operational acceleration in the complex projects, the ca"）
- 2026-07-29｜CFO Craig Chamberlin｜commitment：EMEA 預期下半年回到有機成長（原話："our position for the region to return to organic sales growt"）
- 2026-07-29｜CEO Giordano Albertazzi｜commitment：CEO 稱今年將有另一年強勁訂單成長（原話："we expect another year of robust orders growth."）
- 2026-07-29｜CEO Giordano Albertazzi｜competition：被問準時交貨受損是否讓競爭者有機會，CEO 稱整體表現在改善、市場觀感不變（原話："our overall performance is, if anything, improving."）
- 2026-07-29｜CEO Giordano Albertazzi｜competition：CEO 稱 PurgeRite NearZero 為他人無法在同規模複製的能力（原話："a capability we believe no one else can replicate at our sca"）
- 2026-07-29｜CEO Giordano Albertazzi｜product：固態變壓器（SST）仍在專案開發階段（原話："the solid state is currently a matter of project development"）
- 2026-07-29｜CEO Giordano Albertazzi｜product：800V DC 路線圖：機架/pod 級 2026 客戶驗證、2027 部署；機房級 2027 驗證、2028 部署（原話："This is under customer validation in '26 with deployments pl"）
- 2026-07-29｜CEO Giordano Albertazzi｜product：CEO 稱未來多種電力架構並存，非單一架構（原話："Multiple power architectures will coexist in the future."）
- 2026-07-29｜CEO Giordano Albertazzi｜product：被問 800V 採用遞延的傳言，CEO 不評論傳言，稱採用將是漸進，並指 400V DC 也有參與（原話："we believe that the adoption of 800-volt will be gradual, wo"）
- 2026-07-29｜CEO Giordano Albertazzi｜product：對 800V 時程若較慢，CEO 稱其他架構會取得份額、公司有彈性（原話："we will be flexible."）
- 2026-07-29｜CEO Giordano Albertazzi｜product：每 MW 內容價值隨 800V DC 擴大，CEO 稱與 Investor Day 說法一致（原話："an expansion of revenue per TAM -- per megawatt."）
- 2026-07-29｜CEO Giordano Albertazzi｜customer：管道加速指銷售週期變快，且規模成長，涵蓋 hyperscaler、企業、colo、neocloud（原話："So we noticed an acceleration. So becoming faster sales cycl"）
- 2026-07-29｜CEO Giordano Albertazzi｜customer：與 NVIDIA、Foxconn 旗下 VisionBay AI 合作，奪得台灣首座 GB300 AI 資料中心的電力、散熱與服務（原話："VisionBay AI awarded the power, thermal and services busines"）
- 2026-07-29｜CFO Craig Chamberlin｜customer：客戶在 Q4 去年有大量專案型（OneCore、SmartRun）訂單（原話："we had a large order intake in the fourth quarter of last ye"）
- 2026-07-29｜CFO Craig Chamberlin｜customer：CFO 補充 hyperscaler 有時部署在 colo，客戶分類會有混合（原話："hyperscalers are sometimes deploying to colos."）
- 2026-07-29｜CFO Craig Chamberlin｜capital_allocation：被問股價下跌時是否加大回購，CFO 稱一貫機會主義評估並稱現在是值得看的時機（原話："Given today, it is a good time to look at it"）
- 2026-07-29｜CFO Craig Chamberlin｜capital_allocation：M&A 觀點與 Investor Day 相同，市場活躍並正在評估多個標的，先投資自己再看外部（原話："I've always talked about we invest in ourselves first"）
- 2026-07-29｜CFO Craig Chamberlin｜capital_allocation：Q2 末達淨現金部位，淨槓桿負 0.1 倍（原話："our net leverage is at negative 0.1x, providing even more fl"）
- 2026-07-29｜CEO Giordano Albertazzi｜capital_allocation：已完成 ThermoKey（6 月）與 Strategic Thermal Labs（4 月）收購（原話："we closed the ThermoKey in June, strengthening our heat reje"）
- 2026-07-29｜CEO Giordano Albertazzi｜capital_allocation：垂直整合：無重大缺口，但會調整自製或外購；前季收購 BMarko 為框架垂直整合（原話："We do not think there are any major gaps in vertical integra"）

### 問答異常語氣（迴避／改口／保留）
- VRT_Q2_2026_Earnings_Call_20260729.md｜問：Amit Daryanani 問 Q2 因供應鏈被推遲的營收金額有多大、是 Vertiv 自身還是客戶端問題｜答法：CEO 稱不會給具體金額（we will not be too specific），CFO 也稱不定義具體數字，只說集中在大型專案部署
- VRT_Q2_2026_Earnings_Call_20260729.md｜問：Chris Snyder 問 Q2 逐月是否改善、7 月節奏如何｜答法：CEO 先糾正不用 disruption 一詞，未給逐月節奏，改談複雜度與學習曲線；CFO 稱 good signs 但未給數字
- VRT_Q2_2026_Earnings_Call_20260729.md｜問：Nicole DeBlase 問下半年成長有多少來自 Q2 遞延營收釋出 vs 產能擴張｜答法：CEO 未給比重，改用三層框架（營運加速、產能、backlog）並重申指引非 all-star aligned
- VRT_Q2_2026_Earnings_Call_20260729.md｜問：Nigel Coe 問有進度收款的營收占比多少｜答法：CFO 說明收款階段結構，未給占營收百分比
- VRT_Q2_2026_Earnings_Call_20260729.md｜問：Ananda Baruah 問 800V 若有大客戶遞延到 2029 的傳言與 450V 影響｜答法：CEO 稱不評論傳言，未回答遞延的財務影響，改談採用漸進與彈性
- VRT_Q2_2026_Earnings_Call_20260729.md｜問：Andrew Kaplowitz 問 800V 內容價值是否落在每 MW 3.25–3.75 百萬美元高端｜答法：CEO 稱相當確信內容增加，但未回應是否落在該區間高端

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
{"date":"20260710","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI DC capex 超級週期延續至 2028+，Vertiv 為主要受益整合商","columns":{"2Y 驗證點":"hyperscaler 2026-27 合計 capex ≥ $1.5T；VRT backlog 季底 ≥ $15B","5Y 驗證點":"液冷+800VDC 滲透率翻倍、backlog 穩定轉營收","10Y 驗證點":"資料中心電力散熱 TAM 持續擴張、Vertiv 份額不流失","具體門檻 + 來源":"門檻：4 大 hyperscaler 2026 capex ~$725-785B、2027 ~$1T+（Moody's/Evercore/BofA 2026-04）；Goldman FY25-30 累計 $5.3T。VRT Q4 25 backlog $15.0B（+109%，book-to-bill 2.9x）。來源：DCD/CNBC 2026-04；VRT Q4 25/Q1 26 earnings。","漂移觸發":"連 2 季任二家 capex YoY &lt;+10%（TTM）→ 削弱"}},{"id":"H2","text":"Adj OP margin FY26 達 23.3% 中值、FY27 續擴至 24-25%（液冷+800VDC mix-shift + 營運槓桿）","columns":{"2Y 驗證點":"FY26 全年 ≥ 23.0%","5Y 驗證點":"FY27-28 ≥ 24%","10Y 驗證點":"mix-shift 結構性鎖定高毛利","具體門檻 + 來源":"門檻：FY26 guide Adj OP margin ~23.3%、EPS $6.30-6.40（VRT Q1 26 raise）；Q1 26 actual 20.8%（+430bp YoY）。來源：VRT Q1 26 press release / earnings call 2026-04-22。","漂移觸發":"連 2 季 Adj OP margin YoY 下滑 &gt;100bp → 削弱；連 4 季 → 反轉"}},{"id":"H3","text":"NTM Fwd PE 在 40-55x 維持動態合理（EPS 上修速度 ≥ 倍數擴張），不出現多殺多 reset","columns":{"2Y 驗證點":"NTM PE 40-55x（當前 ~46x，5Y 分位 ~62%）","5Y 驗證點":"成長兌現使 PE 自然沉降至 30-40x 而股價仍漲","10Y 驗證點":"成熟後 PE 落 20-25x、EPS 已放大 3-4x","具體門檻 + 來源":"門檻：NTM PE ~46x（GuruFocus 2026-07-03）；90d EPS 上修 FY26 +5.7%、FY27 +9.9%（yfinance eps_trend）。來源：yfinance forwardPE / eps_trend。","漂移觸發":"NTM PE 連 2 季 &gt;60x + 90d EPS 上修停滯 → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Hyperscaler capex 2027-2028 進入 digestion（capex 已陸續超過 OCF：Oracle 已跨、Amazon 現正跨越、Alphabet ~2027Q1、Meta ~2027Q3、MSFT ~2028Q3）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"4 大 hyperscaler 季度 capex YoY（TTM）","警戒閾值":"連 2 季任二家 &lt;+10%"}},{"id":"R2","text":"液冷/800VDC margin 擴張失敗（mix-shift 不成或價格戰）","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"季度 Adj OP margin YoY","警戒閾值":"連 2 季 YoY 下滑 &gt;100bp"}},{"id":"R3","text":"NTM PE 突破 60x → 多殺多 multiple compression","columns":{"對應假設":"H3","時間尺度":"⚡ 短期","監測指標":"NTM Fwd PE + 90d EPS 上修","警戒閾值":"PE &gt;60x 且上修停滯"}},{"id":"R4","text":"競爭升級：Eaton（Boyd $1.7B）/Schneider（Motivair）/Ecolab（CoolIT $4.75B）取得同階 NVIDIA reference 或價格戰","columns":{"對應假設":"H1/H2","時間尺度":"🔥 中期","監測指標":"NVIDIA partner 生態升等公告 + 液冷 ASP 趨勢","警戒閾值":"對手取得同階 reference 且份額實際流失"}},{"id":"R5","text":"電網併網/變壓器瓶頸拖慢 $15B backlog 認列（併網排隊 4-7 年、變壓器交期 128-144 週、30-50% 2026 計畫容量遞延至 2028 後）","columns":{"對應假設":"H1","時間尺度":"🔥 中期","監測指標":"gross backlog 增 vs revenue 認列速度","警戒閾值":"backlog 增但 revenue 認列連 2 季 miss guidance"}},{"id":"R6","text":"ODM 白牌化 / 架構替代：Foxconn 等自製冷板/manifold 向上整合；或 NVIDIA/hyperscaler 電力散熱 in-house","columns":{"對應假設":"H1/H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"NVIDIA reference 是否仍納 Vertiv + ODM 自製公告","警戒閾值":"NVIDIA 公告自製液冷/800VDC &gt;$500M 或移除 Vertiv reference 階級"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"回檔至 $260-280（Bollinger 中軌／NTM PE ~38x）分批加碼；或 2027 hyperscaler capex 指引續強（≥+20% YoY）確認超級週期延續","irr_base_pct":6.5,"ev5y_pct":35.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.6,"ev5y_pct":35.0,"irr_base_pct":6.5,"max_dd_pct":-60.0,"bull_5y_price":640.0,"bear_5y_price":176.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"回檔至 $260-280（Bollinger 中軌／NTM PE ~38x）分批加碼；或 2027 hyperscaler capex 指引續強（≥+20% YoY）確認超級週期延續","price_at_dd":323.92,"archetype":"品質複利成長","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VRT_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
