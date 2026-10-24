你是 stock-analyst **v20 判斷 agent**，標的 TTMI（20261025）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TTMI","date":"2026-10-25","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TTMI_20261025/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TTMI_20261025/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1203.855,"period":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","unit":"USD M；YoY +60%（Q3 2025 752.7）；QoQ 約 +20%（Q2 約 1,005，由 adj. EBITDA 166.8÷16.6% 反推）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","citation":"公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm"},"note":"公司 Q3 指引 1,100–1,140，實績高於區間上緣"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":208.996,"period":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","unit":"USD M；利益率 17.4%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","citation":"公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":162.253,"period":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","unit":"USD M；利益率 13.5%（Q3 2025: 71.9）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","citation":"公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm"}},{"id":"f_kpi5_q4_2026","label":"管理層指引：Q4 2026","value":"net_sales_B 1.42–1.44；non_gaap_eps 1.77–1.83","period":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","citation":"公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm"}},{"id":"f_kpi6_fy2026","label":"管理層指引：FY2026","value":"net_sales_B 4.47–4.49；non_gaap_eps 4.97–5.03","period":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","citation":"公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm"},"note":"yfinance FY1 營收共識 4,474M（落在指引區間內）"},{"id":"f_kpi7_fy2027","label":"管理層初步 FY2027 預測","value":"net_sales_B 6.5–6.75；non_gaap_eps 8.10–8.90","period":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","citation":"公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm"},"note":"yfinance FY2 營收共識 6,587M（落在區間內）"},{"id":"f_kpi8_book_to_bill","label":"Book-to-bill","value":2.13,"period":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","unit":"倍","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","citation":"公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm"}},{"id":"f_kpi9_a_d_backlog","label":"A&D 專案 backlog","value":2.0,"period":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","citation":"公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm"}},{"id":"f_kpi10","label":"終端市場占比：資料中心與網通","value":41,"period":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","unit":"%（Q3 2025: 30%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","citation":"公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-22","period":"2026-10-22","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-22"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ttmi_gross_margin_pct","label":"TTMI 毛利率","value":21.19,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTMI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ttmi_operating_margin_pct","label":"TTMI 營業利益率","value":9.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTMI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ttmi_fcf_margin_pct","label":"TTMI FCF 利潤率","value":-0.45,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTMI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sanm_gross_margin_pct","label":"SANM 毛利率","value":9.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sanm_operating_margin_pct","label":"SANM 營業利益率","value":5.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sanm_fcf_margin_pct","label":"SANM FCF 利潤率","value":4.66,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2368_tw_gross_margin_pct","label":"2368.TW 毛利率","value":34.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2368.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2368_tw_operating_margin_pct","label":"2368.TW 營業利益率","value":26.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2368.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2368_tw_fcf_margin_pct","label":"2368.TW FCF 利潤率","value":0.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2368.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3037_tw_gross_margin_pct","label":"3037.TW 毛利率","value":19.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3037.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3037_tw_operating_margin_pct","label":"3037.TW 營業利益率","value":10.24,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3037.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3037_tw_fcf_margin_pct","label":"3037.TW FCF 利潤率","value":-0.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3037.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":74.79,"period":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","unit":"USD M（營業現金流 154.7 − 淨資本支出 79.9）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","citation":"公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm"}},{"id":"f_kpi4_sbc","label":"SBC","value":24.09,"period":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","unit":"USD M；占營收 2.0%、占 GAAP 營業利益 14.8%（由 SBC÷數值自算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）","citation":"公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":80.11,"period":"2026-10-23（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-46.24,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":33.07,"period":"2026-10-23（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":4.42,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.75 → 4.96）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":11.05,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.51 → 8.34）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":7.02,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.4 → 10.06）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":4.96,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":8.34,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":10.06,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":22.77,"period":"2026-07-30 → 2026-10-24","unit":"%","basis":"FY1 共識 EPS 4.04 → 4.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":32.04,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝50.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":50.8,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":2.2,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝81.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":81.3,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.41,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝82.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":82.0,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":16.15,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 4.96，分子＝快照價 80.11","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":767.52,"period":"2026-10-25","unit":"USD m","basis":"yfinance 最新一季：總債務 1643.87、現金 876.35（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-25"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":105.35,"period":"2026-10-25","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-25"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":9207.02,"period":"2026-10-25","unit":"USD m","basis":"市值 8439.5 ＋ 淨負債 767.52","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-25"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":4474.05,"period":"2026-10-25","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（5 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-25"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":6586.72,"period":"2026-10-25","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（5 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-25"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.06,"period":"2026-10-25","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-25"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟢","period":"2026-10-25","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 80.11 / W52 116.38 / W104 74.77 / W250 39.88 / W250 13週斜率 3.83%"},{"id":"f_ma_w52","label":"52 週均線","value":116.38,"period":"2026-10-25","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":74.77,"period":"2026-10-25","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":39.88,"period":"2026-10-25","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":3.83,"period":"2026-10-25","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-25","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列示主要對手：商用段多為中國與台灣 PCB 廠（AT&S、Unimicron、Victory Giant、WUS 等），PCB 產業高度分散、競爭激烈。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm","excerpt":"For PCBs, our competitors are mostly based in China and Taiwan. For engineered products such as RF subassemblies and systems, we compete with a different set of competitors largely based in the U.S. and Europe. The PCB industry remains highly fragmented and characterized by intense competition.","as_of":"2026-02-17","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：公司承認可能因競爭失去份額，且新興技術可能帶來新進入者。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm","excerpt":"In addition, we increasingly compete on an international basis, and new and emerging technologies may result in new competitors entering our markets.","as_of":"2026-02-17","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Zacks 稱 Sanmina 以其北美、歐洲、亞洲製造足跡，對 TTMI 的歐洲擴張構成直接挑戰。","source":"Zacks：TTMI's Europe expansion adds capabilities, can it drive growth","url":"https://www.zacks.com/stock/news/2984643/ttmis-europe-expansion-adds-capabilities-can-it-drive-growth","excerpt":"directly challenges TTMI's European expansion through an established manufacturing footprint spanning North America, Europe and Asia.","as_of":"2026-01-01","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Lumen Alpha 分析：TTM 為美國唯一在 ASIC 領域有相當產能的 PCB 廠；並提及產業過剩產能與競爭加劇風險。","source":"Lumen Alpha Substack：TTM Technologies (TTMI US): A Capable PCB Fast-Follower","url":"https://lumenalpha.substack.com/p/ttm-technologies-ttmius-a-capable","excerpt":"hyperscalers toward non-China PCB suppliers, offering near-term upside from accelerating ASIC demand and longer-term margin expansion potential. While industry-wide overcapacity and intensifying competition present risks, TTM’s distinctive U.S.-based footprint may provide a degree of insulation over the medium term.","as_of":"2025-07-20","retrieved_at":"20261025","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Zacks 稱 Sanmina 擴充高階 PCB 產能（AI、航太國防），為 TTMI 在先進應用更直接的 PCB 對手；Amphenol 透過 Wilder Technologies 強化高速電子。","source":"Zacks：TTMI 競爭相關文章","url":"https://www.zacks.com/stock/news/2885793/ttmi-s-pcb-demand-trends-remain-strong-can-it-support-further-upside","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"TTM 10-K FY2025 states sales are diversified across over 1,300 customers, with long-term relationships exceeding ten years with its ten largest customers; no second-source or in-house event disclosed in the excerpt.","source":"SEC EDGAR 10-K FY2025, Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm","excerpt":"Our sales are diversified across end markets with over 1,300 customers and long-term relationships exceeding ten years with our ten largest customers, which reduces our exposure to any single end market or customer.","as_of":"2026-02-17","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Third-party summary of TTM filings: for FY2025 two customers collectively accounted for approximately 23% of net sales.","source":"policyrisk.com TTMI summary of SEC filings","url":"https://policyrisk.com/world/company/TTMI","excerpt":null,"as_of":"2026-02-17","retrieved_at":"20261025","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 前五大 OEM 客戶占淨銷售約 44%（2024 年 42%、2023 年 41%），兩家客戶合計占 23%。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm","excerpt":"Our five largest OEM customers collectively accounted for approximately 44%, 42%, and 41% of our net sales for the years ended December 29, 2025, December 30, 2024, and January 1, 2024, respectively, and two customers collectively represented 23% of our net sales for the year ended December 29, 2025.","as_of":"2026-02-17","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"前十大客戶占淨銷售 55%（2025），高於 2024 年 42% 與 2023 年 41%。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm","excerpt":"Sales to our ten largest customers collectively accounted for 55%, 42%, and 41% of our net sales in 2025, 2024, and 2023, respectively.","as_of":"2026-02-17","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025 年底有一家客戶占應收帳款 14%；2024 年底無客戶達 10%。公司不要求擔保品。","source":"SEC EDGAR 10-K FY2025 附註3","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm","excerpt":"As of December 29, 2025, one customer accounted for 14% of the Company's accounts receivable. There were no customers that accounted for 10% or more of the Company's accounts receivable as of December 30, 2024.","as_of":"2026-02-17","retrieved_at":"20261025","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"公司稱客戶逾 1,300 家，前十大客戶合作關係均逾十年。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm","excerpt":"Our sales are diversified across end markets with over 1,300 customers and long-term relationships exceeding ten years with our ten largest customers, which reduces our exposure to any single end market or customer.","as_of":"2026-02-17","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Evertiq 報導：中國 AI 導向 PCB 廠對客戶表示 7 月 10 日後下的訂單 2028 年前無法交貨（交期拉長）","source":"Evertiq: AI data centres are consuming PCBs – Chinese lead times stretch to 2028","url":"https://evertiq.com/news/2026-07-28-ai-data-centres-are-consuming-pcbs-chinese-lead-times-stretch-to-2028","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261025","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Globalsources：台灣業界預期 AI 帶動的 PCB 與載板供給吃緊至少延續到 2027，新產能難以快速追上訂單；新增產能多在 2027–2029 開出","source":"Global Sources: AI demand surge causes PCB and substrate supply shortage until 2027","url":"https://www.globalsources.com/sourcing-digest/ai-demand-surge-causes-pcb-and-substrate-supply-shortage-until-2027/","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261025","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Evertiq：玻纖布等上游材料預期 2028 年前無明顯緩解；Nittobo 計畫產能約三倍但 2027 後才到位；層壓設備交期約兩年（2026 年 4 月）","source":"Evertiq: PCB material shortages intensify as AI infrastructure absorbs laminate capacity","url":"https://evertiq.com/news/2026-09-08-pcb-material-shortages-intensify-as-ai-infrastructure-absorbs-laminate-capacity","excerpt":null,"as_of":"2026-09-08","retrieved_at":"20261025","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Goldman Sachs（TechFlow 轉述）預期 PCB 供需緊俏未來兩年持續、稼動率維持高檔；有效產能不會隨宣布擴產線性增加（高層數產品耗產能、良率低）","source":"TechFlow: Goldman Sachs on AI server PCB/CCL","url":"https://techflowpost.com/en-US/article/33066","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261025","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Citi 分析（AtlasPCB 轉述）估中國 PCB 廠綠地建廠到量產 13–15 個月，現在宣布的新產能最快 2027 年底至 2028 年初才緩解壓力","source":"AtlasPCB: Citi AI PCB market forecast","url":"https://atlaspcb.com/news/news-citi-ai-pcb-market-forecast-google-tpu-562b-2028","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"二手來源整理：TTM 兩大客戶占 2025 年營收 23%、前五大 44%；Penang 與 Syracuse 擴產需數億美元資本支出，需求若放緩（資料中心建置趨緩或 AI 硬體架構改變）則產能利用率與毛利有風險（Simply Wall St 敘事，未對照公司文件）","source":"Simply Wall St: Is AI Infrastructure Demand Quietly Reshaping TTM Technologies' Long-Term Competitive Moat?","url":"https://simplywall.st/stocks/us/tech/nasdaq-ttmi/ttm-technologies/news/is-ai-infrastructure-demand-quietly-reshaping-ttm-technologi/amp","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TTM 航太國防積壓訂單約 $1.6B、book-to-bill 1.35（二手來源，另一來源為 $1.46B）","source":"Yahoo Finance","url":"https://finance.yahoo.com/markets/stocks/articles/unknown-stock-600-1-6b-141536132.html","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261025","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"TTM 與 STG、ILFA 的兩筆收購案預計 2026 年第三季交割，仍待監管機關核准；搜尋未見針對 TTM 的反壟斷調查或執法行動。","source":"SEC EDGAR 10-Q（期間 2026-06-29）","url":"https://www.sec.gov/Archives/edgar/data/0001116942/000119312526335107/ttmi-20260629.htm","excerpt":"On June 17, 2026, we announced that we had entered into definitive stock purchase agreements to acquire STG and ILFA in separate transactions. These proposed transactions are expected to close in the third quarter of 2026, subject to the satisfaction of regulatory approvals and other customary closing conditions.","as_of":"2026-06-29","retrieved_at":"20261025","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"TTM 10-K 披露約 50% 淨銷售來自非美國營運，大量製造材料來自國際供應商；美中兩國均已將 PCB 列入進口關稅項目，可能影響營收與獲利。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm","excerpt":"Both the U.S. and Chinese governments have included PCBs among items subjected to tariffs imposed on imports from such countries, which may negatively impact our revenue and profitability.","as_of":"2026-02-17","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"TTM 部分產品受美國商務部 BIS 依 EAR 管制出口，並須遵守 ITAR/EAR 與制裁法規；違規可能被罰款或喪失出口權限。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm","excerpt":"Some items we manufacture are controlled for export by the U.S. Department of Commerce’s Bureau of Industry and Security under EAR.","as_of":"2026-02-17","retrieved_at":"20261025","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"TTM 在中國有重大製造據點，面臨美中地緣風險；已透過擴充馬來西亞與美國產能部分緩解","source":"CB Insights TTM profile","url":"https://www.cbinsights.com/company/ttm-technologies-1","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261025","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"部分背板與 PCB 組裝零件為有限或單一供應來源，有時因客戶指定；覆銅板為主要原料且多數材料有多家供應商","source":"TTM FY2018 10-K","url":"https://www.sec.gov/Archives/edgar/data/1116942/000156459019004520/ttmi-10k_20181231.htm","excerpt":"These components for backplane assemblies and other PCB assemblies in some cases have limited or sole sources of supply.","as_of":"2019-03-01","retrieved_at":"20261025","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 net sales up 37% y/y to about $1.0B; Data Center and Networking +91% y/y (40% of sales), Aerospace and Defense 37% of sales +14% y/y, Medical/Industrial/Instrumentation +33%; backlog over $1.7B; book-to-bill 1.49","source":"iconnect007 - TTM Technologies Reports Q2 2026 Results","url":"https://iconnect007.com/article/151085/ttm-technologies-reports-q2-2026-results-new-sales-up-37/151082/pcb","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261025","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 net sales about $1.2B, up 60% y/y, record quarter; adjusted EBITDA $242.3M (20.1% of net sales); segment split not found in snippet","source":"SEC 8-K Exhibit 99.1 (TTM Q3 2026 earnings release)","url":"https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261025","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Third-party Substack estimate: TTM share of hyperscaler PCB supply 10-15% in 2025, expected above 15% in 2026; limited pricing power due to customer concentration; no company disclosure of PCB ASP trend found","source":"Lumen Alpha Substack - TTM Technologies (TTMI US): A Capable PCB Fast-Follower","url":"https://lumenalpha.substack.com/p/ttm-technologies-ttmius-a-capable","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"TTM 10-K 風險因素自述：PCB 產業競爭激烈、高度分散且快速變動；新興技術可能帶來新競爭者；製程技術通常不受重大專利保護；若無法因應快速技術變化，可能無法有效競爭。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm","excerpt":"The PCB industry is intensely competitive, highly fragmented, and rapidly changing.","as_of":"2026-02-17","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"二手轉述（LinkedIn 引 DIGITIMES 與 5 月 TTM CEO Roks 訪談）：供應鏈來源否認 CPO 可使用較低階板材，CPO 目前滲透率極低，光整合由板邊移到板上。","source":"LinkedIn 貼文（Jeffrey Lee）轉述 DIGITIMES","url":"https://tw.linkedin.com/in/jeffrey-lee-33503216","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261025","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"IDTechEx：玻璃基板進入商業化，但尚無公司確定量產上線日期。","source":"IDTechEx Glass in Semiconductors 2026-2036","url":"https://www.idtechex.com/GlassinSC","excerpt":"These pressures have turned glass core substrates and large-panel glass interposers from a niche curiosity into commercialization.","as_of":"2025-08-20","retrieved_at":"20261025","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-05 Q2 財報：Q3 非GAAP EPS 指引 $1.21–1.27，高於 MarketBeat 所載共識 $1.09；Q3 營收指引約 $1.10–1.14B，與預期大致一致；全年指引約 $4.4B、非GAAP EPS 接近 $5.00。Benzinga 另列 Q3 共識 $1.22，各來源共識口徑不一。","source":"MarketBeat: TTM Technologies updates Q3 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/ttm-technologies-nasdaqttmi-updates-q3-2026-earnings-guidance-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261025","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Benzinga 2026-09-25 快照：4 位分析師皆 Buy，平均目標價 $167；最近動作為 Needham 於 2026-09-21 將目標價由 $220 降至 $175。","source":"Benzinga TTMI price targets","url":"https://kr.benzinga.com/quote/TTMI/price-targets","excerpt":null,"as_of":"2026-09-25","retrieved_at":"20261025","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布隨來源與日期差異大：Simply Wall St（2026 年 9 月初）平均約 $214、高 $224、低 $205（4 位）；MarketBeat（2026-08）平均 $212、6 位中 4 買 2 持有。","source":"Simply Wall St valuation; MarketBeat consensus","url":"https://www.simplywall.st/stocks/us/tech/nasdaq-ttmi/ttm-technologies/valuation","excerpt":null,"as_of":"2026-09-05","retrieved_at":"20261025","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"後續 8-K（日期未顯示）：Q4 指引營收 $1.42–1.44B、非GAAP EPS $1.77–1.83；隱含全年營收 $4.47–4.49B、EPS $4.97–5.03；並宣布擬議 $650M 收購（不含於指引）。","source":"SEC 8-K Exhibit 99.1","url":"https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261025","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-08-15 簽約以 11 億美元現金收購 Epiq Solutions（EDS Intermediate Holding），董事會一致通過；2026-09-30 完成收購並簽第三次修訂信貸協議（增貸 TLA 3 億＋TLB 8 億）。","source":"SEC EDGAR 8-K（2026-08-17，Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526353148/d375900d8k.htm","excerpt":"for a purchase price of $1,100,000,000 in cash (the “Purchase Price”), subject to customary working capital and certain other adjustments (the “Acquisition”). The Acquisition has been unanimously approved by the board of directors of the Company.","as_of":"2026-08-17","retrieved_at":"20261025","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026-09-24 完成 5 億美元 6.750% 2034 年到期優先票據私募，併同增貸用於支付 Epiq 收購價，並可能還循環信貸以支付 Swiss Technology Group AG 收購。","source":"SEC EDGAR 8-K（2026-09-24，Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526401013/d186334d8k.htm","excerpt":"completed its previously announced private offering (the “Offering”) of $500 million in aggregate principal amount of its 6.750% senior notes due 2034 (the “Notes”).","as_of":"2026-09-24","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 20 份 8-K，其中 7 份含重大項目；未見 4.02（財報不可信賴）項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001116942&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-10-25 至 2026-10-25 共 20 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 7 份。","as_of":"2026-10-25","retrieved_at":"20261025","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"TTM 於 2026-10-12 宣布追加 4 億美元 AI 產能投資（中國四廠與馬來西亞檳城，棕地快速擴產），疊加原先 2025–2029 年 12 億美元承諾，合計約 16 億美元；未揭露各廠分配、時程與產能數字，預計 Q3 財報電話會議說明。","source":"Evertiq: TTM to invest $400 million in AI PCB capacity in China and Malaysia","url":"https://evertiq.com/news/2026-10-13-ttm-to-invest-400-million-in-ai-pcb-capacity-in-china-and-malaysia","excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261025","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"TTM Syracuse 超高密度互連（Ultra-HDI）廠房建築完工、設備進場安裝測試，預計 2026 下半年開始量產；另有報導稱全產能目標 2028。","source":"TTM 10-Q 季度報告（期間 2026-06-29）","url":"https://www.sec.gov/Archives/edgar/data/0001116942/000119312526335107/ttmi-20260629.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261025","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"同業大幅擴產：勝宏科技 2026 Q1 資本支出約 RMB 36 億（去年同期 7.3 億）；中國逾 20 家 PCB 廠於 2026 上半年宣布積極擴產計畫。","source":"TrendForce: China's PCB Makers Post Record-High Investment on AI Demand","url":"https://www.trendforce.com/news/?p=60548","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"臻鼎董事長稱 2026 年資本支出將超過 NT$800 億，13 座新廠興建中、16 座規劃中，產能 2026–2030 分階段開出；並主張高階產能需超前投資。","source":"Technews: Zhen Ding invests 80 billion in major capacity expansion","url":"https://finance.technews.tw/2026/08/16/zhen-ding-invests-80-billion-in-major-capacity-expansion/","excerpt":null,"as_of":"2026-08-16","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Kingboard 2026 年已調漲層壓板價格八次，最近一次 10 月 13 日對 2116 以下薄玻纖布層壓板與膠片加價 15%；Panasonic、Nan Ya 秋季亦漲價（來源為 PCB 廠商部落格，未核 Kingboard 原始公告）","source":"NextPCB blog, PCB laminate price increase quote impact","url":"https://www.nextpcb.com/blog/pcb-laminate-price-increase-quote-impact","excerpt":"What happened: Kingboard has issued 8 notices in 2026. The latest raises laminate and prepreg made with 2116-or-thinner glass cloth by 15% (Sina Finance).","as_of":"2026-10-21","retrieved_at":"20261025","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"TTM 毛利率由 2008 年 20.2% 降至 2009 年 17.7%（庫存沖銷、固定成本吸收下降）","source":"TTM Technologies Form 10-K FY2009","url":"https://www.sec.gov/Archives/edgar/data/0001116942/000095012310024773/p17097e10vk.htm","excerpt":"Our gross margin decreased from 20.2% for the year ended December 31, 2008 to 17.7% for the year ended December 31, 2009. The decrease in 42 Table of Contents","as_of":"2010-03-01","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"TTM 2019 全年毛利率 14.9%，低於 2018 年 16.1%","source":"TTM Technologies Form 10-K FY2019","url":"https://www.sec.gov/Archives/edgar/data/1116942/000156459020006477/ttmi-10k_20191230.htm","excerpt":"Gross Margin Overall gross margin decreased to 14.9% for the year ended December 30, 2019 from 16.1% for the year ended December 31, 2018.","as_of":"2020-02-28","retrieved_at":"20261025","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-08-15 簽約以 11 億美元現金收購 Epiq Solutions，2026-09-30 完成並簽訂增貸；另有已公告的 Swiss Technology Group AG 收購（完成與否搜尋未見）。","source":"SEC EDGAR 8-K（2026-08-17，Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526353148/d375900d8k.htm","excerpt":"for a purchase price of $1,100,000,000 in cash (the “Purchase Price”), subject to customary working capital and certain other adjustments (the “Acquisition”).","as_of":"2026-08-17","retrieved_at":"20261025","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"-","claim":"Epiq 收購資金來自 5 億美元 6.750% 優先票據加 3 億 TLA、8 億 TLB 增貸。","source":"SEC EDGAR 8-K（2026-09-24，Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/1116942/000119312526401013/d186334d8k.htm","excerpt":"to fund the purchase price for the previously announced proposed acquisition of EDS Intermediate Holding, LLC (the “Acquisition”)","as_of":"2026-09-24","retrieved_at":"20261025","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"TTMI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":21.19,"operating_margin_pct":9.94,"fcf_margin_pct":-0.45,"rd_intensity_pct":0.88},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TTMI","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"SANM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.01,"operating_margin_pct":5.49,"fcf_margin_pct":4.66,"rd_intensity_pct":0.26},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"2368.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":34.69,"operating_margin_pct":26.05,"fcf_margin_pct":0.64,"rd_intensity_pct":1.87},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2368.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"3037.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.85,"operating_margin_pct":10.24,"fcf_margin_pct":-0.4,"rd_intensity_pct":3.92},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3037.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"TTMI"},"financial_history":{"ticker":"TTMI","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":2495046000.0,"revenue_yoy_pct":null,"gross_margin_pct":18.35,"operating_margin_pct":6.52,"net_income":94583000.0,"diluted_eps":0.91,"free_cash_flow":169989000.0,"fcf_margin_pct":6.81,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":2232567000.0,"revenue_yoy_pct":-10.52,"gross_margin_pct":18.51,"operating_margin_pct":4.96,"net_income":-18718000.0,"diluted_eps":-0.18,"free_cash_flow":27042000.0,"fcf_margin_pct":1.21,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2442753000.0,"revenue_yoy_pct":9.41,"gross_margin_pct":19.54,"operating_margin_pct":6.54,"net_income":56299000.0,"diluted_eps":0.54,"free_cash_flow":51155000.0,"fcf_margin_pct":2.09,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":2906345000.0,"revenue_yoy_pct":18.98,"gross_margin_pct":20.7,"operating_margin_pct":9.21,"net_income":177448000.0,"diluted_eps":1.68,"free_cash_flow":-683000.0,"fcf_margin_pct":-0.02,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TTMI/TTMI_Q3_2026_Earnings_Call_20261022.md）

# Q3 2026 Earnings Call
**TTM Technologies, Inc.** | Earnings Calls | 2026-10-22

**Operator** (Operator):
Good day, and welcome to TTM Technologies Third Quarter 2026 Earnings Call. [Operator Instructions] Please be advised that today's conference is being recorded.
I would now like to hand the conference over to your speaker, Mr. Sean Hannan, Vice President of Investor Relations. Please go ahead.

**Sean Kilian Hannan** (Executives):
Greetings, everyone. Welcome, and thank you for joining us today. I'm Sean Hannan, Vice President of Investor Relations for TTM. With me on the call are Edwin Roks, our President and Chief Executive Officer; and Dan Boehle, our Executive Vice President and Chief Financial Officer.
Before we get started, I'd like to remind everyone today that the call contains forward-looking statements, including statements related to TTM's future business outlook. Actual results could differ materially from these forward-looking statements due to one or more risks and uncertainties, including the risk factors we provide in our filings with the Securities and Exchange Commission, which we encourage you to review.
These forward-looking statements represent management's expectations and assumptions based on currently available information. TTM does not undertake any obligation to publicly update or revise any of these forward-looking statements, whether as a result of new information, future events or other circumstances, except as required by law.
We will also discuss on this call certain non-GAAP financial measures such as adjusted EBITDA. Such measures should not be considered as a substitute for the measures prepared and presented in accordance with GAAP, and we direct you to the reconciliations between GAAP and non-GAAP measures included in the company's earnings release, which is available on the Investor Relations section of TTM's website at investors.ttm.com. We have also posted on the website an earnings presentation that we will refer to during the call.
Here is Edwin.

**Edwin Roks** (Executives):
Thank you, Sean. Good afternoon, everyone, and thank you for joining us for our third quarter 2026 conference call. At TTM Technologies, we are focused on designing and manufacturing complex advanced interconnect products and printed circuit boards in addition to what we term as Up-the-Chain products and solutions such as sophisticated RF modules, resulting in subsystems and fully integrated mission systems for communications and sensing purposes.
Core to the design of all our products and solutions as well as the strategy of our business is the innovative focus to safely next-generation needs for our customers and end markets, particularly regarding SWaP or size, weight and power. We believe the future of electronics lies in speed to market, high reliability and efficient technology integration, and we consequently engage early with our customers, often multiple times -- multiple years in advance as part of their program road maps to ensure this alignment while also enabling optimal management of their complex supply chains.
It continues to be a very successful year for TTM so far. Our third quarter set another new record with over $1.2 billion in revenue, and we expect to close out the year strong, aided by increased shipments of our N+M product offerings for data center and networking end market in addition to continuing strong demand for TTM's aerospace and defense business and product offerings.
Proposal activity in our aerospace and defense business remained at all-time highs with a record backlog of $2 billion. We already have visibility into roughly 65% of our projected A&D revenue for 2027. Our medical, industrial and instrumentation and automotive end markets also outperformed our expectations year-to-date. With all our business performing well in 2026 to date, we are increasing our full year 2026 revenue guidance from $4.47 billion to $4.49 billion.
Since our last quarterly earnings call, we have had many exciting developments here at TTM, and we continue to execute our long-term business strategy focused on projected value creation for our customers and shareholders.
As we framed at our Investor Day in May, TTM continues to invest in organic growth opportunities and technological advancements across our product offerings for all our end markets in addition to strategic M&A to enhance our capabilities and add diversification and longer-term structural enhancements.
To that end, we discussed three key strategic directives. First, investment in capacity and innovative technology for advanced interconnect. As previously disclosed in this area, we have invested or committed to invest over $1.3 billion in capacity expansion in the 2025 to 2029 time frame across both our data center and networking and aerospace and defense end markets.
While our commercial segment is currently the primary target for these investments, our model has proven over time that our investments in our commercial technology advances provide critical value to leverage into our A&D offerings as that end market continues to modernize.
Last week, we announced an additional $400 million planned investment that is expected to begin in the fourth quarter of 2026 and continue into early 2028. And this would primarily support revenue production focused on the 2028 period.
The basis of this additional investment provides critical commercial data center and networking end market customer support in their strong demand and road map requirements to utilize our unique N+M product approach. Recall, the majority of our customer business in this market currently is with our industry-leading innovative established and critical AI players.
We remind investors that our fundamental business model has been -- continues to be what we discussed at the Investor Day, and that is to pursue a very disciplined risk-reduced brownfield expansion approach for internal organic investments with the expectations to fund these efforts from operating cash without any anticipated need to access our borrowing facilities.
These investments have been given substantial forethought, are purposeful, aligned with our customers and not simply reactive to the strong demand environment. Our commitment to these investments is driven by our confidence in our projected cash flows supported by our visibility to the anticipated strong demand requirements of our differentiated and advancing technologies.
We are also in the early stages of investing in a new innovation center in the Eau Claire, Wisconsin facility, very close to our existing technology center in Chippewa Falls, Wisconsin. This facility will spearhead our intensified R&D activities focused on pioneering technological advances such as mSAP, SAP, [indiscernible] and embedded optics, among other technologies.
Second, recall that we are extremely focused on our diversified business model and that as part of this, we've pursued our initial geographic expansion in the European region. In June, we announced our intention to acquire two well-established European companies, Swiss Technology Group and ILFA to begin this effort. We've since closed the Swiss Technology Group acquisition now called TTM GS Swiss, and we believe we're nearing the close of ILFA. On Monday, we announced the planned acquisition of Ophir Optics, which would establish a presence in Israel and Romania. I'll share some additional comments on Ophir Optics in a few moments.
Additionally, we engaged last week in plans to acquire two small but strategic printed circuit board companies under the Merlin PCB Group Holding Company in the United Kingdom. We are excited that all these transactions are both strategic from a technology and capability standpoint and also in terms of adding international diversification to our business and financial model.
Finally, our third strategic directive is investment in what we call Up-the-Chain of vertical product solutions with focus on communication and sensing. In line with this directive, we acquired Epiq Solutions, which is closed on September 30. We are excited to welcome the Epiq team members into TTM as we continue the integration activities. The announced plan to acquire Ophir Optics also supports the theme of Up-the-Chain, and both these companies bring a unique set of competencies that will deliver differentiated and high-value solutions to our end markets.
I'll now provide a few additional comments on the proposed acquisition of Ophir Optics before we move on to discuss our operating results of the quarter. Ophir Optics is a global leader in precision infrared thermal imaging and laser optics solutions for defense, homeland security and industrial applications with locations in Israel and Romania. With Ophir's market-leading advanced infrared and laser optical components, we can offer our customers solutions where -- and we can combine these optics with our other in-house modalities and our interconnect capabilities.
This applies for both A&D and industrial applications. In A&D, we expect to have the opportunity to combine infrared optics and RF radar systems to offer customers a highly integrated and very small form factor mission subsystem for unmanned and counter-unmanned aerial systems, both difficult to modernize defense priorities. On top of that, Epiq will add processing capabilities. Optics and processing are the key differentiators in any optical sensing system.
Consequently, we expect the potential combined offerings of Epiq Solutions and Ophir Optics can advance a common strategy, moving up the defense value chain and bringing together complementary software-defined radios and infrared capabilities. Both are keys to expanding our role in mission-critical sensing modalities such as surveillance, reconnaissance, communications and electronic warfare.
In Industrial, this proposed acquisition provides laser optical subsystems used for shaping laser beams in industrial cutting, welding and PCB drilling machines. We are very excited for the opportunities ahead. From a financial perspective, the proposed acquisition of Ophir Optics is projected to incrementally benefit our financial model by adding more high-margin, long-cycle business to our mix.
Let me go through the financial highlights with you. We are acquiring Ophir Optics business for an all-cash purchase of $650 million as a carve-out from MKS. The transaction is expected to be funded through a combination of cash on hand and borrowings under TTM's existing revolving credit facility. And at this time, we believe it's important to convey to all our shareholders that we do not have any current incremental needs or plans to come to the financial markets to access capital.
On timing, we expect to close this in the second quarter of 2027, subject to regulatory approvals and other customary closing conditions. Ophir Optics is experiencing strong revenue growth and margin expansion, and the transaction is expected to be immediately accretive to our adjusted EBITDA margins and our non-GAAP diluted EPS.
The transaction multiple is estimated to be roughly 10x the expected Ophir Optics full year 2027 adjusted EBITDA without synergies. TTM's net leverage at closing is expected to be less than 2x adjusted last 12 months EBITDA and therefore, within our targeted leverage range.
I'll now move on to an overview of our business highlights from the quarter. Dan will follow up with a summary on our Q3 2026 financial performance, our Q4 and full year 2026 guidance and our initial preliminary guidance for 2027.
From a demand standpoint, product development with our partners, bookings and backlog and broader signals in both AI and defense remain strong and are expected to provide very healthy growth momentum for the remainder of this year and as we look in 2027.
We interact very closely with our customers and strategic partners and jointly engage in very diligent conversations to plan for the future, make thoughtful investments and take a disciplined approach to vet our outlook, which we believe provides us with a lot of optimism as will be evidenced in the guidance that Dan will share shortly.
We delivered an excellent third quarter of 2026. And as always, I would like to thank our employees for delivering these results. We achieved sales of $1.2 billion and non-GAAP EPS of $1.46 per diluted share, both above our guidance and both all-time quarterly highs.
Sales for consolidated TTM grew 60% year-on-year, reflecting demand strength in our data center and networking end markets driven by AI, while our medical, industrial and instrumentation sales almost doubled from a year ago. And aerospace and defense end markets experienced very strong double-digit growth.
The company's adjusted EBITDA margin was 20.1% in the third quarter of 2026, up an impressive 400 basis points year-on-year and over 350 basis points sequentially, reflecting positive mix impact and operational excellence. Non-GAAP EPS of $1.46 per diluted share was 118% improvement year-on-year.
The aerospace and defense end market represented 34% of third quarter 2026 sales. Sales in the aerospace and defense market grew 21% year-on-year in the third quarter with the vast majority of our facilities performing at strong levels. The sales growth in the defense market continues to be the result of positive tailwinds in defense budgets, our strong strategic program alignment and key bookings for new and ongoing programs.
Our ability to support sustained long-term growth is also very encouraging and further enabled by our recent strategic acquisitions. Our focus on product innovation is tracking well against our internal road maps for many new capabilities, including unique advancements in printed circuit board technologies for materials that enable high frequency in support of all our applications.
During the third quarter of 2026, our A&D team's effective execution continued in securing another strong bookings quarter, capturing business related to the surface ship surveillance SPY-6 radar, the APS-143 maritime surveillance radar, Golden Dome and a number of projected priority restricted programs. A&D's book-to-bill ratio was roughly 1.6 for the quarter, which led to total program backlog of $2 billion, a record level, up from just under $1.5 billion a year ago.
Within our backlog, we are excited to report that we have strong momentum in securing new business from new primes as well as restricted programs. Restricted programs are incredibly sticky and very difficult for competitors to try and displace. For the fourth quarter of 2026, we expect this end market to represent approximately 31% of our total sales and continue to deliver both year-on-year and sequential growth.
For the full year 2026, we now expect this end market to deliver approximately 20% growth compared to 2025, including contributions from acquired businesses of roughly 80% on an organic basis.
Sales in the data center and networking end market represented 41% of third quarter 2026 sales. This end market experienced 115% year-on-year growth in the third quarter, reflecting the strong ramp of our high-technology N+M asymmetrical printed circuit boards and continued demand strength from data center and networking customers.
For the fourth quarter of 2026, we expect this end market to represent approximately 49% of net sales as our N+M boards continue to experience strong uptake at customers. For the full year 2026, we continue to expect sales in this end market to be more than double year-on-year.
The medical, industrial and instrumentation end market represented 18% of the third quarter 2026 sales. This end market saw year-on-year growth of 97% during the third quarter, aided by price adjustments to fully capture the value add of our technology in addition to particular demand strength in instrumentation for automotive test equipment supporting AI solutions.
For the fourth quarter of 2026, we expect the medical, industrial and instrumentation end market to represent approximately 14% of total sales, growing roughly 90% year-on-year. For the full 2026, we now expect sales in this end market to grow nearly 70% year-on-year. Automotive sales represented 7% of third quarter 2026 sales and was up 11% year-on-year. We continue to be very selective in this market to focus on the higher value-add products that carry margin profiles consistent with our financial goals.
Given conversations with customers, we are seeing additional share opportunities as some competitors reduce their market participation while long-term business cycles are showing signs of migrating back towards our advanced capabilities. For the fourth quarter of 2026, we expect the automotive end market to represent about 6% of total sales, which reflects a quite encouraging double-digit growth as we diligently push out the challenge of supply chain materials availability discussed last quarter.
For the full year 2026, we now expect sales in this end market to improve mid-single digits versus our prior expectations for a mid-single-digit decline year-on-year. The overall book-to-bill was a remarkable 2.1 for the third quarter of 2026, with Commercial reporting segment at 2.5 and the A&D reporting segment at 1.6. At the end of the third quarter of 2026, the 90-day backlog, which is subject to cancellations, was $1.3 billion compared to $610 million a year ago, a 111% increase year-on-year.
Now Dan will summarize the financial performance in more detail. Dan?

**Daniel Boehle** (Executives):
Thanks, Edwin, and good afternoon, everyone. I'll review our financial results for the third quarter of 2026 that were included in the press release distributed today. Key financial highlights are also summarized in the earnings presentation posted on our website. For the third quarter, net sales were $1.2 billion compared to $753 million in the third quarter of 2025. The 60% year-over-year increase was due to growth across all our end markets and most notably continued strength in data center and networking, medical, industrial and instrumentation and aerospace and defense.
GAAP operating income for the third quarter of 2026 was $162.3 million compared to GAAP operating income for the third quarter of 2025 of $71.9 million. On a GAAP basis, net income in the third quarter of 2026 was $84.8 million or $0.79 per diluted share. This compares to GAAP net income for the third quarter of 2025 of $53.1 million or $0.50 per diluted share.
The remainder of my comments will focus on our non-GAAP financial performance. Our non-GAAP performance excludes M&A-related costs, restructuring costs, certain noncash expense items such as amortization of intangibles, impairment of goodwill, stock-based compensation, gains on the sale of property, unrealized gains or losses on foreign exchange and other unusual or infrequent items. We present non-GAAP financial information to enable investors to see the company through the eyes of management and to facilitate comparisons with expectations and prior periods.
Gross margin in the third quarter of 2026 was 24.8%, an increase of 330 basis points from 21.5% in the third quarter of 2025. The year-on-year increase was due primarily to higher sales volume and favorable product mix, particularly in the data center and networking and aerospace and defense end markets, in addition to execution improvements at our facility in Penang, which we continue to expect to approach breakeven in the fourth quarter of 2026.
Selling and marketing expense was $23.2 million in the third quarter or 1.9% of net sales versus $20.5 million or 2.7% of net sales a year ago. Third quarter general and administrative expense was $57.3 million or 4.8% of net sales compared to $42.1 million or 5.6% of net sales a year ago. Third quarter research and development expense was $9.5 million or just under 1% of net sales compared to $6.9 million or just under 1% of net sales in the prior year.
Our operating margin in the third quarter of 2026 was 17.4%, a 510 basis point improvement from 12.3% in the same quarter last year. The increase in the period was due both to the improvement in gross margin as well as operating leverage resulting from selling, general and administrative expense discipline.
Adjusted EBITDA was $242.3 million in the third quarter of 2026, a record quarterly adjusted EBITDA margin of 20.1% and up 400 basis points year-over-year. This compares to adjusted EBITDA of $120.9 million in the third quarter of 2025 with an associated adjusted EBITDA margin of 16.1%.
Interest expense was $12.1 million in the third quarter of 2026 compared to $9.9 million in the same quarter last year. Interest and other income was $3.1 million in the third quarter of 2026 compared to $2.5 million in the same quarter of last year. Realized foreign exchange loss in the third quarter of 2026 totaled $4.1 million as compared to $1.8 million in the same quarter last year, driven by the weakening of the U.S. dollar.
Our effective tax rate was 19.5% in the third quarter of 2026, resulting in tax expense of $38.2 million. This compares to an effective tax rate of 15% or a tax expense of $12.5 million in the same quarter last year. Third quarter 2026 non-GAAP net income was $157.8 million or $1.46 per diluted share. This compares to third quarter 2025 non-GAAP net income of $71 million or $0.67 per diluted share.
Cash flow provided by operating activities was $154.7 million in the third quarter of 2026, which compares to cash flow provided by operating activities of $141.8 million in the same quarter last year. Free cash flow in the third quarter of 2026 was $74.8 million as compared to free cash flow of $42.6 million in the third quarter of last year.
Now I'll provide our financial guidance for the fourth quarter of 2026, an update to our outlook for the full year of 2026 and an initial preliminary expectation for full year 2027. We project net sales for the fourth quarter of 2026 to be in the range of $1.42 billion to $1.44 billion and non-GAAP earnings to be in the range of $1.77 to $1.83 per diluted share. These projected results include the contributions of recently closed transactions and associated financing. However, they exclude any contribution or impact from pending acquisitions.
Consequently, we now expect full year 2026 sales of approximately $4.47 billion to $4.49 billion and non-GAAP earnings in the range of $4.97 to $5.03 per diluted share. These full year 2026 projections also include the contributions of recently closed transactions and associated financing, but exclude any contribution or impact from pending acquisitions.
The fourth quarter 2026 non-GAAP diluted EPS forecast is based on a diluted share count of approximately 107.8 million shares, which includes the dilutive effect of outstanding stock options and other stock awards. Our expected full year 2026 non-GAAP EPS forecast is based on a diluted share count of 107.5 million shares, similarly including the effect of outstanding stock options and other stock awards.
We expect SG&A expense to be approximately 6.7% of net sales in the fourth quarter and R&D expenditures to be approximately 1% of net sales. We expect interest expense of approximately $33.9 million, interest income of approximately $3.0 million and realized foreign exchange and other nonoperating expenses of approximately $4.7 million. We estimate our effective tax rate will be between 15% and 19%.
Further, we expect to record depreciation of approximately $39.7 million, amortization of intangibles of approximately $12.1 million, stock-based compensation expense of approximately $18.7 million and noncash interest expense of approximately $0.9 million.
Looking to the preliminary full year 2027 forecast, we are providing our initial net sales forecast to be in the range of approximately $6.5 billion to $6.75 billion, and non-GAAP net income is expected to be in the range of $8.10 to $8.90 per diluted share based on a diluted share count of 108.1 million shares, including the effect of outstanding stock options and other stock awards.
Our initial 2027 full year forecast includes contributions from recently closed acquisitions and associated financing costs, while excluding any contribution or impact from pending acquisitions. And finally, I'd like to announce that we are scheduled to participate in the Bank of America Leveraged Finance Conference in Boca Raton, Florida on December 1 and the UBS TMT Conference in Scottsdale, Arizona on December 2.
That concludes our prepared remarks. So I'll turn it back to you, Sherry, for the Q&A session.

**Operator** (Operator):
[Operator Instructions] And our first question will come from the line of Steven Fox with Fox Advisors.

**Steven Fox** (Analysts):
I guess for my first question, I was wondering if we could sort of dig into the N+M results to date and expectations going forward. And can you give us a sense for how much of the quarter was driven by the new product, where you think you are in terms of ramping yields, et cetera? And then how broad-based the product is expected to be used? I'm just trying to understand like how dominant this is becoming within your traditional PCB sales. And I had a follow-up.

**Edwin Roks** (Executives):
Yes, Steve, yes, happy to do that. Our N+M program is -- will be a substantial part of our data center and networking group, as you know. Ramp-ups are going really well. It's currently about 30% of the data center and networking activities. And it will grow next year to about 50% of that group.
The ramp-up is going really well. We have three major programs. Two of them are doing really well. One of them is, let's say, a bit moving to the right. This has nothing to do, by the way, with any technical issue, has nothing to do with our performance. It basically has to do with the program schedule of that customer, which is a normal thing with these big programs.
So far, we're getting very, very positive feedback on our N+M program. There are more N+M programs coming. I mentioned before, this will be 5 to 10 programs all around. So that's going well.
Yes, Steve, there will always be a bit of fluctuation in these programs. These programs are so big. So there will always be a bit of fluctuation. There is also a bit of pull forward to Q3. I can tell you, some of the things are even enhanced. So that will be a fact. But again, currently about 30% of the data center and networking business going into next year to about 50%. So that technology is working really well.

**Steven Fox** (Analysts):
Great. That's helpful. And then just to be crystal clear on all the M&A you've done and how you're planning to finance it. Can you sort of talk about where this leaves you? Like what's the potential for more M&A once you close all these deals? And just big picture thoughts on balance sheet since you've been pretty active in the acquisition market the last few months.

**Daniel Boehle** (Executives):
Yes, Steve, this is Dan. I'll take that. Thanks for the question. Yes, I think this will be the end of the big stuff for a while. There may be a few little things that we've announced a few that we need to close. And they're one of those kind of medium sized, the other is smaller. So we'll focus on strengthening our balance sheet, getting our leverage back down now. We've got a lot of strong cash flow coming in next year. We'll have positive free cash flow to continue to fund our capital expenditures as well as start paying down that debt.
But in our Q4 guide, so the difference between where we were last quarter and this quarter, we do have two of the businesses that have closed or expected to close in this period or close right at the end of Q3 into Q4 will impact positively on our EBITDA, but we did raise significant debt for the purchase of Epiq as well as to finance the Ophir project that we just announced.
So that has an increase of interest expense of about $20 million a quarter. So that drags on our EPS. And so if you look at the change in EPS guidance from last quarter to where we are now, up from the transactions, but then offset by the debt.

**Operator** (Operator):
One moment for our next question. That will come from the line of Will Stein with Truist.

**William Stein** (Analysts):
First, I want to recognize and say congratulations on the great results overall. But I want to also recognize that the data center networking end market came about 10% below your prior guidance in Q3. And so I'm hoping you can help us understand what happened there? Was it supply or like material availability or yield or something else?

**Edwin Roks** (Executives):
No, none of these things. These things basically have to do with project timing on the customer side. Again, these large customers, these big customers we have, they have multiple programs, and there are always fluctuations in these programs. Some of them move to the left, some of them move a bit to the right. Again, there are no technical issues. Ramp is going well. Yield numbers are where they should be.
Again, they have always multiple suppliers. So there's always a bit of, let's say, everybody has to be in that same window technology-wise. So that's sometimes hurting us also a bit. But again, two out of these three programs we initially had are doing really well. The third one is ramping up now. That will be in ramp-up in the second half of Q4, fully in production in Q1. So that's going smooth. And it's like I said before, there are more N+M programs coming. But again, there will always be a fluctuation, and we always try to be as accurate as possible in our guidance. But again, there are no major issues there.

**William Stein** (Analysts):
Appreciate that. As a follow-up, and last quarter, I believe you told us that N+M would be approximately $200 million in Q3 and approximately $400 million in Q4. It sounds like in Q3, that might have been a little light, but not entirely sure. Maybe you can update these numbers for us, please?

**Edwin Roks** (Executives):
Yes, sure. In Q3, of the full data center networking business, it was about 30% of our business was based on N+M. So call it, let's say, 31% or $400 million, something like that. In Q4, we expect about the same percentage, about 30% out of, let's say, a $700 million data center networking forecast. So these are about the numbers. So the ramp-up is going well.
Is it exactly the $200 million and the $400 million? No, probably not. It will be slightly more than $200 million and slightly below the $400 million. But again, like I said, next year, it's about 50% of the full data center networking business. So things are just fluctuating a bit. But again, no big deal there.

**Operator** (Operator):
One moment for our next question. And that will come from the line of Mike Crawford with B. Riley Securities.

**Michael Crawford** (Analysts):
Can you give some color on supply availability of key materials like CCL and T-glass and also how you match any increasing prices with quotes?

**Edwin Roks** (Executives):
Yes. Sure, Mike. Lead times, let's say, are, let's say, in the order of, let's say, 12 weeks, sometimes a bit longer, sometimes 24 weeks, sometimes even a bit longer depending on the materials. So far, I think we are handling this very well. On the A&D side, I think everything is solid. On the data center and networking side, it's an ongoing activity. Yes, lead times are going up, but we are also, let's say, these programs are getting bigger. So we have much more visibility on these things.
If you look at the cost, yes, the costs are going up. But so far, let's say, we are very transparent with our customers and the customers will take these price increases. And it's like I said, the N+M is having higher ASPs. So that's helping us a lot. So price increases, yes, the customers will absorb that.

**Michael Crawford** (Analysts):
Okay. And then just to follow up related, the higher ASPs for the N+M, we understand that, but would you say that's higher than corporate average gross margin? And I guess related, where do you see gross and EBITDA margins progressing throughout 2027?

**Edwin Roks** (Executives):
Yes, yes, yes. These ASPs are going faster than our cost, and that has to do with the complexity of the boards. The complexity is increasing a lot for these boards. So basically, it's all about the value. I rather don't talk about cost and ASP. I rather think about the value. We're taking much more value in these data centers and networking configurations. So that's helping us a lot. It's about a factor 4 if you compare it with, let's say, conventional architectures, N+M is really adding a lot, let's say, in complexity. And of course, the customers are willing to pay for that.

**Daniel Boehle** (Executives):
Mike, maybe I'll just add. You mentioned about EBITDA, right? So yes, our EBITDA margins will be increasing our gross margin on that N+M product is significantly higher than our corporate average. And so as that becomes more of the mix, our gross margin as well as our EBITDA margins will be increasing more than 200 basis points in the next year.

**Operator** (Operator):
One moment for our next question. And that will come from the line of Ruben Roy with Stifel.

**Ruben Roy** (Analysts):
Edwin, I wanted to first follow up on Will's question on the N+M shift. If you think about Q4 and the guide there was $700 million of revenue for DC, how much is that coming from acceleration in customer demand versus maybe recovering some of the push to the right N+M? So maybe, you could start there.

**Edwin Roks** (Executives):
Yes, Ruben, these are indeed programs. And like I said, they move a bit. It's like I said, it's about 32% of the $670 million in commercial -- sorry, in C&C, what we call C&C data centers and networking is coming from N+M. Again, these programs are ramping up. These programs are doing well. And again, the feedback is very, very positive from these larger customers that basically that more N+M programs are coming in.

**Ruben Roy** (Analysts):
Okay. And then on the $400 million capacity expansion, it sounds like that will be fully operational in '28. Can you talk about what kind of customer volume visibility you have against that increased commitment? And are customers committing to programs against that spend?

**Edwin Roks** (Executives):
Yes, happy to do that. The $400 million is going on top of something we addressed earlier, a $1.2 billion expansion, let's say, over multiple years till 2029. The $400 million is, I would say, is more allocated to N+M. So I would say the $400 million is pure N+M rounding numbers here, yes. You have to think about our brownfield approach. So basically, what we're very good at, and you see it in China, and I gave several examples during the investor meetings is that we love brownfield.
So basically, buildings close to our existing plants, we are going to utilize for additional capacity. We do that very, very fast, and we can follow the market much, much more accurate. So that's basically all of that. It's a lot of equipment, Ruben, which we are installing there to grow our N+M. It's like I said, C&C, our data center networking business, 50% of that will be N+M. So that's going really well. The technology is really doing what it should do.

**Operator** (Operator):
One moment for our next question. And that will come from the line of Jim Ricchiuti with Needham.

**James Ricchiuti** (Analysts):
Great. So I wanted to just ask you about the preliminary 2027 guidance. Relative to your earlier expectations, the growth that you're expecting now for 2027, how much of that is due to perhaps higher N+M expectations for data center or possibly how much is due to higher organic growth in the A&D business?

**Edwin Roks** (Executives):
Yes. So if you look at -- starting Jim, with the numbers, let's say, for this year, the $4.4 billion, $4.5 billion, let's say, is a 48% growth year-over-year. This is a number we're going to repeat next year. And again, next year, we will grow 50%. A substantial part of that growth will be N+M. The interesting thing, Jim, is that all the different end markets are growing.
So if you look at our medical, industrial instrumentation business, it's growing a lot, and it will continue to grow in next year. Even if you look at our automotive business is growing year-over-year. And of course, our aerospace and defense business is growing a lot next year.
So that's -- it is just a matter that data center network is growing so fast that it doesn't look like the others are growing. But I can tell you, it's growing over 20%. Yes, that is -- these are big, big, big numbers. So yes, we are confident with the numbers we predicted for 2027.

**James Ricchiuti** (Analysts):
Got it. Follow-up question relates to the M&A activity. So we have Epiq, other smaller M&A that you've done and the pending Ophir acquisition. If we look out to next year after Ophir closes, how much of the A&D business is going to be non-PCB in nature now?

**Edwin Roks** (Executives):
At the moment, if you look at our aerospace and defense business, about half of them is what we call up the chain. So our, let's say, sensing and communication activities. If we look at Epiq and Ophir -- by the way, they are very complementary. If you look at Epiq, let's say, that's more the processing and Ophir, we're very happy with that one as well. That's more the optical side.
If you have the optical side and, let's say, the processing under control and you're sensor agnostic, you basically can make full sensing systems, which are very consistently used in -- complementary to our radar activities. So that's going well.
If you look at the numbers, all of our acquisitions and of course, Ophir will only add, let's say, the second part of the year because we only closed it, let's say, hopefully in Q2, at the end of Q2. So we have only one half year of that -- of Ophir. Then I would say, if you add up all these acquisitions, it's about $0.5 billion in sales of the $6.75 billion, $6.5 billion for next year. So that's about the ratio.

**Operator** (Operator):
And we do have a follow-up question from Will Stein with Truist.

**William Stein** (Analysts):
I wanted to ask about Ophir. When we look at the EBITDA multiples cited in your press release and in the seller's press release, one conclusion is that EBITDA is growing very significantly or you expect it to grow very significantly from '26 to '27. What's driving that? Is that backlog that's already in place? Or is that stuff that you expect to get design wins after the close? Any color to sort of explain this?

**Edwin Roks** (Executives):
Yes, it's a very good question. And yes, you gave the answer yourself. The thing is if we look at the bookings for 2027, Ophir is over 85% booked with new things coming in. By the way, they have a tendency that they always beat that forecast, by the way. So '27, 85% booked. The 10.3x we addressed as being the multiple EBITDA over the price we pay is probably even a bit more conservative.
We did -- I think it was a very, very, very nice deal for us around 10x. So we're very happy with that. And it's like I said, the synergies are not taken into the business case at all, but the synergies will be huge because this is giving us the optical system. We have the processing. We can be sensor agnostic. That basically means we can make a full optical system. So it's a very nice acquisition for us.

**William Stein** (Analysts):
And then as a follow-up, you've now given us preliminary view on 2027. Normally, when you have guided revenue, you've given us some breakdown by end market. I wonder if you're willing to do that, in this case, for '27, how we should think about each end market as a percentage of revenues?

**Edwin Roks** (Executives):
It's a bit early for that, Will. But of course, we will provide more color. Again, we -- again, only a few quarters ago, we give only, let's say, forecast for the next quarter. Now let's say, we are giving a bit more guidance for the full year. You have an idea what our data center networking business is doing, how that will grow.
Our aerospace and defense business will do better and better, let's say, looking at the munition side, looking at the Golden Dome side, a lot of radar. So that will do better and better. It's a bit early to give that exact split, but we wanted to give some guidance for '27 and showing that we are maintaining that growth.

**Daniel Boehle** (Executives):
Yes. Well, I think we've done that in the past in the fourth quarter call. And so we'll strive to give that. We will be able to get that in the next call.

**Operator** (Operator):
I'm showing no further questions in the queue at this time. I'll turn the call back over to Mr. Edwin Roks for any closing remarks.

**Edwin Roks** (Executives):
Yes. Thank you. This has been a good call. So I thank you, operator. And now let's say, summarize with a few items. First of all, we are seeing strong -- very strong growth. We delivered very strong sales growth in Q3 of about 60% year-on-year, resulting in an all-time high of $1.2 billion for quarterly revenue, driven by increase in our data center networking, medical, industrial, instrumentation, aerospace and defense markets, basically all the markets helped there.
Second, our adjusted EBITDA for the second quarter of 20.1% reflected strong operating improvements and overall performance, leading to another all-time high record in non-GAAP EPS. As a result, $1.46 per diluted share, and we expect to continue building on this operating performance in the coming quarters.
And third, we continue to generate solid cash flows from operations, which is used to our source to invest in our organic operations as it supports projected or continued growth.
In closing, and I said it before, I would like to thank all our employees of TTM, our customers, our suppliers and our shareholders for continued support, and thank you very much. Goodbye.

**Operator** (Operator):
Thank you all for participating. This concludes today's program. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TTMI_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO Daniel Boehle｜guidance：Q3 2026 non-GAAP EPS 指引區間（營收 $1.10–1.14 billion）（原話："a range of $1.21 to $1.27 per diluted share"）
- 2026-08-05｜CFO Daniel Boehle｜guidance：全年 2026 營收指引上調至約 $4.4 billion（原話："full year 2026 sales of approximately $4.4 billion"）
- 2026-08-05｜CFO Daniel Boehle｜guidance：全年 2026 non-GAAP EPS 預期逼近 $5（原話："non-GAAP earnings to approach $5 per diluted share."）
- 2026-08-05｜CFO Daniel Boehle｜guidance：Q4 預期營收較 Q3 再往上（原話："net sales growth should continue with a sequential uptick"）
- 2026-08-05｜CFO Daniel Boehle｜guidance：財測口徑：指引不含待完成併購的貢獻或影響（原話："exclude any contribution or impact from pending"）
- 2026-08-05｜CFO Daniel Boehle｜guidance：Q3 SG&A 佔營收比重指引（原話："SG&A expense to be approximately 7% of net sales"）
- 2026-08-05｜CEO Edwin Roks｜guidance：Q3 資料中心與網通佔營收比重指引（原話："we expect this end market to represent 49% of net sales"）
- 2026-08-05｜CEO Edwin Roks｜guidance：全年資料中心與網通市場營收預期（原話："sales in this end market to more than double year-on-year"）
- 2026-08-05｜CEO Edwin Roks｜guidance：全年航太國防營收成長預期（原話："sales in this end market to grow in the low to mid-teens year-on-year."）
- 2026-08-05｜CEO Edwin Roks｜guidance：全年醫療／工業／儀器市場成長預期（原話："sales in this end market to grow 35% to 40% year-on-year"）
- 2026-08-05｜CEO Edwin Roks｜guidance：全年車用市場預期仍為中個位數衰退（原話："we continue to expect sales in this end market to decrease in"）
- 2026-08-05｜CEO Edwin Roks｜commitment：管理層重申 2027、2028 年有機營收成長目標（原話："achieve 15% to 20% organic revenue growth for 2027 and 2028"）
- 2026-08-05｜CEO Edwin Roks｜commitment：下一季將就遠期年度提供更新的長期計畫說明（原話："further clarity on these out years next quarter"）
- 2026-08-05｜CEO Edwin Roks｜commitment：明年也會繼續提供全年 EPS 指引（原話："We plan to do that next year as well."）
- 2026-08-05｜CEO Edwin Roks｜commitment：2026 營收預計明顯高於先前承諾的 $4 billion 門檻（原話："plan to achieve at least $4 billion in net sales in 2026"）
- 2026-08-05｜CEO Edwin Roks｜commitment：Syracuse 超高密度互連（Ultra-HDI）廠 Q3 起爬坡，2028 達滿產（原話："to reach full capacity run rate at 2028."）
- 2026-08-05｜CEO Edwin Roks｜commitment：Penang 預計接近損益兩平的時點（原話："breakeven number, which we hope to get, let's say, late Q3, Q4"）
- 2026-08-05｜CEO Edwin Roks｜product：N+M 不對稱互連板下半年約 $600 million 的出貨量（原話："$600 million of that technology, which is a really nice technology"）
- 2026-08-05｜CFO Daniel Boehle｜product：N+M 下半年 $600 million 在 Q3、Q4 的拆分（原話："About 1/3 of that's in Q3 and then 2/3 in Q4"）
- 2026-08-05｜CEO Edwin Roks｜product：N+M 良率比預期好（原話："Yields are much better than we thought"）
- 2026-08-05｜CEO Edwin Roks｜product：Penang 也在做 N+M，支援資料中心客戶（原話："doing N+M and indeed, supporting some of our data center and networking customers"）
- 2026-08-05｜CEO Edwin Roks｜product：Syracuse 廠 Ultra-HDI 產品 Q3 開始初期爬坡（原話："begin the initial stages of ramping up volume for Ultra-HDI"）
- 2026-08-05｜CFO Daniel Boehle｜margin：N+M 良率改善帶動 Q3、Q4 毛利率／EBITDA 利潤率改善，但不量化（原話："I won't quantify exactly what it will have."）
- 2026-08-05｜CFO Daniel Boehle｜margin：管理層稱 Q3、Q4 利潤率皆會改善（口徑為 adjusted EBITDA margin）（原話："it will improve the margins in both the third quarter and"）
- 2026-08-05｜CEO Edwin Roks｜margin：Adjusted EBITDA margin 16.6% 的年增／季增歸因於產品組合（原話："largely reflecting positive mix impacts"）
- 2026-08-05｜CFO Daniel Boehle｜margin：毛利率年增 100bp 的拆解：量與組合，點名資料中心與航太國防（原話："favorable product mix, particularly in the data center and networking"）
- 2026-08-05｜CFO Daniel Boehle｜margin：營業利益率改善歸因於毛利率與營運槓桿（原話："gross margin as well as operating leverage"）
- 2026-08-05｜CFO Daniel Boehle｜margin：Q2 自由現金流數字（原話："Free cash flow in the second quarter of 2026 was $46.0 million"）
- 2026-08-05｜CFO Daniel Boehle｜margin：GAAP 含 $14 million 非現金未實現匯率交換損失（因併購未完成無法適用避險會計）（原話："recognized a noncash pretax unrealized loss in the amount of $14 million"）
- 2026-08-05｜CEO Edwin Roks｜customer：資料中心與網通 Q2 年增 91%（原話："experienced 91% year-on-year growth in the second quarter"）
- 2026-08-05｜CEO Edwin Roks｜customer：商用端除既有 10% 客戶外，另有一家接近 10%（原話："it's getting a bit crowded, so there is another one"）
- 2026-08-05｜CEO Edwin Roks｜customer：前五大醫療客戶表現超出內部預期一倍以上（原話："top 5 medical customers' performance have more than doubled"）
- 2026-08-05｜CEO Edwin Roks｜customer：航太國防 Q2 book-to-bill 與在手訂單（原話："which led to a total program backlog of $1.7 billion"）
- 2026-08-05｜CEO Edwin Roks｜customer：航太國防合格潛在商機管道規模（原話："over $7 billion of potential business currently qualified"）
- 2026-08-05｜CEO Edwin Roks｜customer：90 天訂單積壓金額（可取消）（原話："backlog, which is subject to cancellations, was $901 million"）
- 2026-08-05｜CEO Edwin Roks｜competition：CEO 稱在美國航太國防部分有時是唯一供應商（原話："And it looks like sometimes we are the only"）
- 2026-08-05｜CEO Edwin Roks｜risk：車用業務因 CCL 供應商轉向高階材料而面臨材料供應壓力（原話："which reflects slight pressure in supply chain materials availability"）
- 2026-08-05｜CEO Edwin Roks｜risk：供應鏈問題僅出現在較低階業務，管理層稱高階不受影響（原話："if we are suffering a bit with our supply chain"）
- 2026-08-05｜CEO Edwin Roks｜capital_allocation：STG 與 ILFA 併購預計貢獻低於 5% 增量營收（原話："expected to contribute less than 5% of incremental sales"）
- 2026-08-05｜CEO Edwin Roks｜capital_allocation：管理層表示未來仍會機會性尋找歐洲併購標的（原話："to continue to be opportunistic in the future for businesses"）
- 2026-08-05｜CEO Edwin Roks｜capital_allocation：董事會剛核准另一筆擴產資本投資（原話："we approved another capital investment"）
- 2026-08-05｜CFO Daniel Boehle｜capital_allocation：全年資本支出區間上下限各上調約 $45 million（原話："went up around $45 million at the top and bottom end"）
- 2026-08-05｜CEO Edwin Roks｜capital_allocation：威斯康辛 Eau Claire 廠不急著投入，取得成本低於 $20 million（原話："We only paid less than $20 million for"）
- 2026-08-05｜CEO Edwin Roks｜capital_allocation：淨槓桿比率 0.9x（原話："net leverage ratio of 0.9x"）

### TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md
- 2026-05-27｜Daniel Boehle (CFO)｜guidance：CFO 說 2026 全年營收可達約 40 億美元（原話："revenue for 2026 could reach about $4 billion"）
- 2026-05-27｜Daniel Boehle (CFO)｜guidance：CFO 說 Q1、Q2 約成長 30%，全年隱含 38% 成長（原話："we're growing at about 30%. So that implies 38%"）
- 2026-05-27｜Daniel Boehle (CFO)｜guidance：CFO 說明全年成長偏下半年加速（原話："expectation of accelerated growth in the second half"）
- 2026-05-27｜Daniel Boehle (CFO)｜guidance：2026 營業利益率指引由 11.7% 升到 13%–15%，並說比先前長期目標 11%–13% 高（原話："from 11.7% last year to a range of 13% to 15%"）
- 2026-05-27｜Daniel Boehle (CFO)｜guidance：2026 調整後 EBITDA 利益率指引 16%–18%（先前 15%–17%）（原話："adjusted EBITDA margin, 16% to 18%"）
- 2026-05-27｜Daniel Boehle (CFO)｜margin：管理層把 EBITDA 利益率只升 100bps（營業利益率升 200bps）的差距歸因於美元走弱的匯損，約 100bps（原話："driven this year by the weakening of the U.S. dollar"）
- 2026-05-27｜Daniel Boehle (CFO)｜margin：CFO 指 N+M 技術帶動較高 ASP，進而帶動較高毛利率（原話："that will result in higher gross margins for us"）
- 2026-05-27｜Daniel Boehle (CFO)｜margin：CFO 說 Penang 的毛利拖累全年少於 80bps（原話："That should be less than 80 bps for the year"）
- 2026-05-27｜Daniel Boehle (CFO)｜margin：回答分析師對增量利潤率的提問，CFO 說下半年良率仍待執行（原話："We do have yield expectations or yield performance we still"）
- 2026-05-27｜Daniel Boehle (CFO)｜margin：CFO 說利潤率區間的高低端取決於 N+M 良率，主要驅動為營收組合（原話："Revenue mix is what's going to drive the majority of it"）
- 2026-05-27｜Rob Farrell｜margin：Rob Farrell 說新一代程式的 ASP 是前代的 2–3 倍（原話："replacements are 2 or 3x what they were in past generations"）
- 2026-05-27｜Catherine Gridley｜margin：Gridley 說 A&D 2025 EBITDA 利益率 17.2%，年增 120bps（原話："17.2% EBITDA margin, which was 120 basis points growth"）
- 2026-05-27｜Catherine Gridley｜margin：Gridley 說多數合約以固定價格投標（原話："largely bid in a firm fixed"）
- 2026-05-27｜Gregory Fortier｜margin：Fortier 說新採購方式（市集式）利潤較好，但部分專案仍受認證成本與定價規範（原話："subject to certified cost and pricing"）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 重申未來三年營收年複合成長 15%–20%（原話："The 15% to 20% is still pretty accurate."）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 重申 2025 到 2027 年獲利翻倍的目標仍然適用（原話："doubling the earnings from 25 to 27"）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 說公司近幾個月才改為提供全年指引，過去只給下一季（原話："we decided now to give full guidance for the year"）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 說 A&D 成長預期為高個位數（原話："in the foreseeable future, high single digit"）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 說資料中心與網路業務今年可能翻倍（原話："to double that business."）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 說醫療、工業、儀器業務預期成長約 25%–30%（原話："we expect to grow about 25% to 30% going"）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 說車用預期年減約 10%（Q1 僅減 2%）（原話："we expect a decline of, let's say, 10% year-over-year"）
- 2026-05-27｜Catherine Gridley｜guidance：Gridley 說四座北美廠擴產讓 2028 年前可增加約 5 億美元營收的產能（原話："for $500 million in additional revenue growth"）
- 2026-05-27｜Douglas Soder｜guidance：Doug Soder 估計 N+M 長期營收機會為 45 億美元（原話："revenue opportunity over the future for N+M at $4.5 billion"）
- 2026-05-27｜Rob Farrell｜guidance：Farrell 說 N+M 量產爬坡在今年夏天與下半年（原話："place this summer and into the second half of the year"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 說 2026 資本支出 3 億至 3.2 億美元，並預期現金流略為正（原話："increased the capital expenditures for the current year"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 預期今年自由現金流為小幅正值（原話："continue to get slightly positive in the current year"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 說 2027、2028 資本支出占營收約 6%–7%（原話："between 6% and 7% of revenue, with growing revenue"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 與歷史資本支出占比（約 4%–5%）相比較高（原話："higher than our historical, which is about 4% to 5%"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 說正在擴大並重新定價 Term Loan B，約 3.4 億增至 4 億美元（原話："$340 million to $400 million on upsize"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 說以多幣別循環信貸取代現有 ABL，額度最高 10 億美元（原話："commitments on that up to $1 billion"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 說擴大的借款額度預期主要用在併購（原話："is most likely going to be used for M&A"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 提到地理擴張與小型策略併購機會，並說 CEO 想去歐洲（原話："my boss seems to want to be there"）
- 2026-05-27｜Edwin Roks (CEO)｜capital_allocation：Roks 說歐洲 A&D 要求至少 60% 歐洲在地含量，是併購切入角度（原話："there needs to be 60-plus percent European content"）
- 2026-05-27｜Douglas Soder｜capital_allocation：Soder 說近年已在商用部門投入 10 億美元擴廠（原話："invested $1 billion in this commercial sector footprint"）
- 2026-05-27｜Douglas Soder｜capital_allocation：Soder 說 N+M 在 2025–2027 預計投入 4.5 億美元資本支出（原話："anticipating $450 million of capital investments in N+M"）
- 2026-05-27｜Douglas Soder｜capital_allocation：Soder 說在既有廠區旁擴產（棕地）比新建（綠地）快一倍以上（原話："to market for our customers in half the time or less"）
- 2026-05-27｜Douglas Soder｜capital_allocation：Soder 說已在檳城附近取得土地，適當時可建第二座廠（原話："land nearby so that we have the opportunity"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 說 N+M 這 4.5 億美元約換來 45 億營收（10 倍），並稱不是所有資本支出的基準（原話："gave basically a 10x on that $450 million"）
- 2026-05-27｜Rob Farrell｜commitment：Farrell 說已承諾專案到明年中約有近 100% 產能覆蓋（原話："almost 100% coverage by probably the middle of next year"）
- 2026-05-27｜Rob Farrell｜commitment：Farrell 說保留部分產能給非策略夥伴的新客戶（原話："I would say we are holding some capacity"）
- 2026-05-27｜Douglas Soder｜commitment：Soder 說正與大客戶討論長約，內容含產能保證與工程合作（原話："agreements for capacity guarantees, engineering engagement"）
- 2026-05-27｜Edwin Roks (CEO)｜commitment：Roks 說歐洲擴張在規劃管線中（原話："So that's in the pipeline."）
- 2026-05-27｜Catherine Gridley｜competition：Gridley 說 A&D 最大的競爭來自主承包商自行內製（原話："our biggest competition really is the primes"）
- 2026-05-27｜Rob Farrell｜competition：Farrell 說 N+M 的競爭格局受限，僅少數業者（原話："the competition landscape is it's restricted"）
- 2026-05-27｜Rob Farrell｜competition：Farrell 說目前 N+M 受到一定程度的保護（原話："we're somewhat protected at this point"）
- 2026-05-27｜Douglas Soder｜competition：Soder 說資料中心 SAM 中有大量商品化業務，公司不想做，所以市占只有 9%（原話："There's a lot of commodity business in that number"）
- 2026-05-27｜Douglas Soder｜competition：Soder 說資料中心網路可服務市場約 100 億美元，公司市占約 9%（原話："about $10 billion, and we're at about 9% market"）
- 2026-05-27｜Daniel Boehle (CFO)｜competition：CFO 說 9% 是回頭看的數字，未來視所選技術可能上升或下降（原話："looking at the 9%, you're looking in the rear"）
- 2026-05-27｜Douglas Soder｜customer：Doug Soder 說資料中心與網路 2025 年約 9 億美元，年增 40%（原話："up 40% year-on-year"）
- 2026-05-27｜Catherine Gridley｜customer：Gridley 說 A&D 在手訂單 16 億美元，管線 72 億美元（原話："the $7.2 billion pipeline, and that pipeline is growing"）
- 2026-05-27｜Catherine Gridley｜customer：Gridley 說 72 億美元管線到 5 月已顯著成長（原話："has already significantly grown just up through May"）
- 2026-05-27｜Catherine Gridley｜customer：Gridley 說已接到再製造回流（onshoring）訂單（原話："we are already fielding orders for onshoring and reshoring"）
- 2026-05-27｜Catherine Gridley｜customer：Gridley 說新創主承包商（neo primes）興趣顯著加速（原話："we're now seeing a significant acceleration in that interest"）
- 2026-05-27｜Catherine Gridley｜customer：Gridley 說商用太空快速加速（原話："We are seeing a rapid acceleration in commercial space"）
- 2026-05-27｜Gregory Fortier｜customer：Fortier 說已收到 Golden Dome 的首張訂單（原話："received our first order very, very quickly"）
- 2026-05-27｜Gregory Fortier｜customer：Fortier 說已收到感知與迴避雷達（先進空中運輸）的首張訂單（原話："we've received the first order here in this market as well"）
- 2026-05-27｜Gregory Fortier｜customer：Fortier 引述總統 2027 預算七條預算線共 2350 億美元（原話："$235 billion dedicated to just 7 budget lines"）
- 2026-05-27｜Gregory Fortier｜customer：Fortier 說國防合約授標由 600 天縮到 30–45 天（原話："a 600-day process to award a contract"）
- 2026-05-27｜Rob Farrell｜customer：Farrell 說愈來愈多客戶要求中國以外的方案（原話："more and more of them want solutions outside of China"）
- 2026-05-27｜Catherine Gridley｜customer：Gridley 說商業太空客戶的採購決策尚待定，直接影響 ramp 時程（原話："that will directly impact what our ramp-up"）
- 2026-05-27｜Douglas Soder｜product：Soder 說公司的板子與晶片種類無關（晶片中立）（原話："processing unit agnostic or chip agnostic"）
- 2026-05-27｜Douglas Soder｜product：Soder 說 N+M 正進入量產（原話："now entering into mass production with N+M technology"）
- 2026-05-27｜Rob Farrell｜product：Farrell 說早期 3.2T 設計尚未納入光學（原話："the early 3.2 designs we have do not include optics yet"）
- 2026-05-27｜Edwin Roks (CEO)｜product：Roks 說銅不會很快消失，光學是補充（原話："copper is not going away, okay? It's not going away soon."）
- 2026-05-27｜Edwin Roks (CEO)｜product：Roks 被問光學方向時承認目前沒有太多資訊（原話："Do we have a lot of color right now"）
- 2026-05-27｜Edwin Roks (CEO)｜risk：Roks 承認 AI 浪潮終將下滑，時點不知（原話："When it will come down, we don't know."）
- 2026-05-27｜Edwin Roks (CEO)｜risk：Roks 說波浪會下來，要做好準備（原話："we better be prepared for that"）
- 2026-05-27｜Catherine Gridley｜risk：Gridley 說國防端成長時程取決於採購核准時程（原話："it takes time to qualify these products"）
- 2026-05-27｜Edwin Roks (CEO)｜risk：Roks 說 80% 的業務由 AI 與國防兩大趨勢驅動（原話："80% of our business is basically driven by these megatrends"）

### 問答異常語氣（迴避／改口／保留）
- TTMI_Q2_2026_Earnings_Call_20260805.md｜問：Truist 的 William Stein 問明年 N+M 增量營收是否約 $1 billion、利潤率影響為何｜答法：未確認數字，稱明年規模仍為規劃中（'a work in progress'），僅說 'it could be in the ballpark you mentioned'，利潤率影響未正面回答
- TTMI_Q2_2026_Earnings_Call_20260805.md｜問：B. Riley 的 Mike Crawford 問 STG／ILFA 收購價格、年化營收貢獻與擴充空間｜答法：CEO 明說無法談營收與價格（'I cannot do that'），僅重述低於 5%，CFO 表示 '交割時再提供'，改談興奮與監管流程
- TTMI_Q2_2026_Earnings_Call_20260805.md｜問：Needham 的 Jim Ricchiuti 問 N+M 爬坡對 Q3 營收與利潤率的影響｜答法：給了下半年 $600 million 與 1/3、2/3 拆分，但利潤率影響明說不量化（'I won't quantify'），僅稱 Q3、Q4 都會改善
- TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md｜問：Steven Fox 問為何指引隱含的增量利潤率只有約 20%，是否過於保守｜答法：CFO 未給出增量利潤率數字，改談匯率逆風與下半年良率仍待執行，再補充營收組合與 N+M 良率
- TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md｜問：Steven Fox 問 A&D 為何只講高個位數成長，哪裡有雙位數上行空間｜答法：Gridley 沒給成長數字，改談資格認證時間、國防部採購時程與商用太空客戶採購決策尚待定
- TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md｜問：William Stein 問 2027、2028 年營收成長與利潤率擴張的方向｜答法：Roks 只重申 15%–20% 與 EPS 翻倍，未給新數字，並說 'So we'll see. We'll see.' 以及有變化會通知分析師
- TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md｜問：James Ricchiuti 問 72 億美元管線一年前的規模與主要組成｜答法：Gridley 說無法提供對比，也不談管線細項，只說已顯著成長且偏向國防
- TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md｜問：Remington Johnson 問 5 億美元增量營收潛力在四座廠間如何分配｜答法：Gridley 拒絕按廠拆分，只說 Syracuse 最大
- TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md｜問：James Ricchiuti 問 Eau Claire 何時裝機、如何放量｜答法：管理層回說沒有明確時程，只談客戶區域分散與中國加一等需求驅動

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
{"date":"20260518","verdict":"觀望偏進場","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Penang + Syracuse ramp 順利 → 公司 Gross Margin 從 21.4% 擴至 26%+，OI Margin 從 12.8% 擴至 16%+","columns":{"2Y 驗證（28 年內）":"Penang 達 OCF breakeven (Q3 26)；Syracuse 啟動量產 (late 26)；FY26 全年 GM 22%+","5Y 驗證（28-30 年）":"FY29 全年 GM 26%+；OI Margin 16-18%；TTMI 整體 OCF $700M+","10Y 驗證（30-35 年）":"FY32 維持 GM 26%+ 並繼續往 28% 邁進；單站 ROIC > 15%","驗證指標":"Quarterly GM / OI Margin、Penang quarterly revenue (target $30-35M Q3, $80M Q4)","來源":"§8.A Runway, §6 quarterly"}},{"id":"H2","text":"A&amp;D 段持續 +12-15% YoY 至 2028，backlog 維持 1.4-1.6x book-to-bill","columns":{"2Y 驗證（28 年內）":"2026 A&amp;D 段 +11-13%（Q1 已驗證 +11%）；backlog $1.6B → $1.9B","5Y 驗證（28-30 年）":"FY29 A&amp;D revenue $1.6B+（vs 2025 ~$1B）；占比維持 38-42%","10Y 驗證（30-35 年）":"FY32 A&amp;D $2.5B；Syracuse + Telephonics + 既有產線 三引擎","驗證指標":"季度 A&amp;D revenue、book-to-bill、backlog 絕對額","來源":"§11 議價權, §8 路線圖"}},{"id":"H3","text":"市場給予 forward PE 25-30x（vs 商用 EMS 同業 18-22x）的 premium，反映 A&amp;D moat + AI 結構性成長","columns":{"2Y 驗證（28 年內）":"FY26 Fwd PE 維持 25-30x（不破 20x），股價區間 $90-180","5Y 驗證（28-30 年）":"FY29 PE 25x，EPS $7.5+，股價 $185+","10Y 驗證（30-35 年）":"FY32 進入成熟期 PE 20x，EPS $10+，股價 $200+","驗證指標":"Fwd PE 5Y rolling、PEG、vs Sanmina/Jabil 同業溢價幅度","來源":"§13.1/§13.4"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"🔥 Penang ramp 延後 + Capex 失控：若 Q4 26 Penang 仍未達 OCF breakeven、且 FY27 Capex 拉到 $350M+，FCF 連續 3 年負，市場開始質疑 capital allocation","columns":{"對應假設":"H1","時間尺度":"🔥 中期（2-3 年）","監測指標":"Penang quarterly revenue + OCF；FY27 Capex guidance","警戒閾值":"Q3 26 Penang revenue FY27 Capex guidance > $350M（連續第三年增加）"}},{"id":"R2","text":"⚡ A&amp;D backlog 萎縮 + 國防預算延後：美國 CR (continuing resolution) 延長 / 債限政治 → DoD 凍結 program timing；backlog QoQ 連續兩季下滑","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（12 月內）","監測指標":"季度 A&amp;D revenue、backlog、book-to-bill；DoD FY27/28 budget 進度","警戒閾值":"book-to-bill A&amp;D backlog QoQ"}},{"id":"R3","text":"⚡ 估值倍數壓縮 + 內部人賣壓擴大：FPE 從 33x 修正至 25x（即使 EPS 未變，股價 −24%）；Tom Edman 從 10b5-1 schedule 切換至「機會式賣股」or 新 CEO 加入賣方","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（12 月內）","監測指標":"Fwd PE 5Y 分位（baseline 92%）、SPX 整體 P/E 收斂、Form 4 揭露","警戒閾值":"Fwd PE > 40x（超越 5Y 高）OR Fwd PE OR 6 個月內部人賣股 > $20M"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":167.35,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TTMI_20261025/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
