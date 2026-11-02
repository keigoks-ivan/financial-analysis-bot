你是 stock-analyst **v20 判斷 agent**，標的 MSFT（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MSFT","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSFT_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSFT_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":92279,"period":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m (YoY +19%)","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast"}},{"id":"f_kpi1_gaap_operating_income","label":"GAAP operating income","value":45915,"period":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m (YoY +21%)","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast"}},{"id":"f_kpi2_gaap_operating_margin","label":"GAAP operating margin","value":49.8,"period":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast（營業利益÷營收自行換算；CFO 稱約 50%）"}},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":18633,"period":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast（營業現金流 58,000 − PP&E 增加 39,367，自行換算；CFO 稱 $18.6B）"}},{"id":"f_kpi5_guidance_q2_fy27","label":"Guidance Q2 FY27","value":"Revenue $96.0–97.1B（+18–19%）；Azure +49–50% cc；營業利益率 YoY 微降；Capex >$50B；FY27 維持 FCF 為正，CY 資本支出約 $170B","period":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","citation":"Q1 FY27 earnings call，CFO Amy Hood（新聞稿本身無指引）；https://finance.yahoo.com/markets/stocks/articles/microsoft-msft-q1-2027-earnings-052921146.html"}},{"id":"f_kpi6_microsoft_cloud_revenue","label":"Microsoft Cloud revenue","value":63.9,"period":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn (YoY +30%)","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast"}},{"id":"f_kpi7_azure_revenue_growth","label":"Azure revenue growth","value":48,"period":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast"}},{"id":"f_kpi8_commercial_rpo","label":"Commercial RPO","value":677,"period":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn (YoY +73%)","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast"}},{"id":"f_kpi9_capex_pp_e_cash_addition","label":"Capex (PP&E cash additions)","value":39367,"period":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","unit":"USD m (去年同期 19,394)","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_msft_gross_margin_pct","label":"MSFT 毛利率","value":67.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_operating_margin_pct","label":"MSFT 營業利益率","value":47.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_fcf_margin_pct","label":"MSFT FCF 利潤率","value":17.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_gross_margin_pct","label":"GOOGL 毛利率","value":60.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_operating_margin_pct","label":"GOOGL 營業利益率","value":33.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_fcf_margin_pct","label":"GOOGL FCF 利潤率","value":4.19,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_crm_gross_margin_pct","label":"CRM 毛利率","value":77.28,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crm_operating_margin_pct","label":"CRM 營業利益率","value":21.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crm_fcf_margin_pct","label":"CRM FCF 利潤率","value":34.49,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_adbe_gross_margin_pct","label":"ADBE 毛利率","value":89.25,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADBE.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_adbe_operating_margin_pct","label":"ADBE 營業利益率","value":35.7,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADBE.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_adbe_fcf_margin_pct","label":"ADBE FCF 利潤率","value":40.79,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADBE.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_team_gross_margin_pct","label":"TEAM 毛利率","value":84.83,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TEAM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_team_operating_margin_pct","label":"TEAM 營業利益率","value":0.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TEAM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_team_fcf_margin_pct","label":"TEAM FCF 利潤率","value":20.07,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TEAM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc","label":"SBC 占營業利益","value":6.8,"period":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"FY2027 Q1（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 IR 新聞稿 https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast（SBC $3,134m ÷ 營業利益；占營收 3.4%）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":521.91,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":26.44,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":49.03,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":1.32,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.76 → 20.02）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":1.9,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.69 → 24.14）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":3.19,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（29.16 → 30.09）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":20.02,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":24.14,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":30.09,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.38,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 19.18 → 20.02（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":27.24,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝32.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":32.1,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":11.19,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝46.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":46.4,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":11.39,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝47.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":47.3,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":26.07,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 20.02，分子＝快照價 521.91","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.697,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":69422.0,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 133931.0、現金 64509.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":7426.19,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":3945226.81,"period":"2026-11-02","unit":"USD m","basis":"市值 3875804.81 ＋ 淨負債 69422.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":395873.32,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（40 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":475270.33,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（53 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":9.97,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 521.91 / W52 445.89 / W104 447.7 / W250 374.01 / W250 13週斜率 0.93%"},{"id":"f_ma_w52","label":"52 週均線","value":445.89,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":447.7,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":374.01,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.93,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"MSFT FY2026 10-K 自述：AI 市場競爭激烈且有新進入者持續加入，AI 產品與超大規模雲商、開源及前沿模型供應商競爭（部分同時是夥伴）；多數業務進入門檻低。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm","excerpt":"AI technology and services are a highly competitive and rapidly evolving market, and new competitors continue to enter the market. Our AI offerings compete with AI products from hyperscalers, open-source offerings, and frontier model providers, some of which are also current or potential partners.","as_of":"2026-07-29","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Synergy 資料：2025Q3 AWS 29%、Microsoft 20%、Google 13% 雲支出份額","source":"The Register, AWS under pressure as big three battle to eat the cloud market","url":"https://www.theregister.com/2025/11/20/aws_loses_market_share_azure_google/","excerpt":"AWS still has a comfortable lead, with 29 percent of global market spend in Q3, but Microsoft and Google, the junior pair in the cloud triumvirate, are steadily increasing their market shares, accounting for 20 percent and 13 percent respectively.","as_of":"2025-11-20","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Ramp 資料：Anthropic 企業支出份額 37% 對 OpenAI 33%，資料集不含 Microsoft","source":"Sherwood News, Microsoft is pushing Copilot but everyone just wants ChatGPT","url":"https://sherwood.news/tech/microsoft-is-pushing-copilot-but-everyone-just-wants-chatgpt/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Microsoft 在 365 Copilot 加入 Anthropic 模型，降低對 OpenAI 依賴","source":"eMarketer, Microsoft adds Anthropic to 365","url":"https://www.emarketer.com/content/microsoft-adds-anthropic-365-loosening-openai-grip-on-enterprise-ai","excerpt":null,"as_of":"2025-09-25","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2026 10-K：無客戶占營收超過 10%；與 OpenAI 商業安排營收約 $24.1B（約 7%）","source":"Microsoft Form 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0000789019/000119312526323660/msft-20260630.htm","excerpt":"investee, OpenAI is a related party as defined in Accounting Standards Codification Topic 850, Related Party Disclosures (“ASC 850”). In accordance with ASC 850, we are disclosing revenue and accounts receivable balances from transactions with OpenAI. For fiscal year 2026, we recorded revenue from commercial arrangements with OpenAI, inclusive of revenue-sharing payments, of $24.1 billion,","as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 10-K 揭露來自 OpenAI 商業安排的營收約 241 億美元，約占 FY2026 營收 3318 億美元的 7%；據二手報導，10-K 未點名其他客戶。","source":"aiweekly: Microsoft Booked $24.1B From OpenAI, Filings Reveal AI Reliance","url":"https://aiweekly.co/alerts/microsoft-booked-241b-from-openai-filings-reveal-ai-reliance","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"二手報導：OpenAI 約占微軟商業 RPO（FY26 末 6780 億美元）的三成多；FY26 Q2 財報電話會 CFO 稱約 45% 的商業 RPO 來自 OpenAI（當時 6250 億美元）。兩者日期與基準不同。","source":"The Register: Microsoft investors sweat cloud giant's OpenAI exposure","url":"https://www.theregister.com/2026/01/29/microsoft_earnings_q2_2026/","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"二手報導：FY27 Q1（截至 9 月）OpenAI 未收款餘額 72 億美元，6 月底為 60 億美元；搜尋未見 OpenAI 或微軟的評等調降、破產或財測下修；微軟維持 AAA 評等（TIKR 評論）。","source":"aiweekly FR: Microsoft encaisse 10 Md$ d'OpenAI au T1 FY27","url":"https://aiweekly.co/fr/alerts/microsoft-encaisse-10-md-dopenai-au-t1-fy27-11-de-son-chiffre-et-72-md-de","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"10-K 中 OpenAI 營收占比與應收","source":"SEC FY2026 10-K","url":"https://www.sec.gov/Archives/edgar/data/0000789019/000119312526323660/msft-20260630.htm","excerpt":"OpenAI is a related party as defined in Accounting Standards Codification Topic 850, Related Party Disclosures (“ASC 850”). In accordance with ASC 850, we are disclosing revenue and accounts receivable balances from transactions with OpenAI. For fiscal year 2026, we recorded revenue from commercial arrangements with OpenAI, inclusive of revenue-sharing payments, of $24.1 billion, and","as_of":"2026-07-29","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FY26 Q4 財報電話會（2026-07）：需求仍超過供給，CFO Hood 未給出何時改善的預估；Q4 新增約 1GW 容量，新增容量『immediately monetized』。","source":"Directions on Microsoft / 財報報導 (July 30, 2026)","url":"https://www.directionsonmicrosoft.com/microsoft-expect-capacity-constraints-capex-acceleration-to-continue/?ref=wheresyoured.at","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"FY27 Q1（2026-10）：本季 capex $45.2B 低於預期 $50.7B，原因是部分 AI 雲合作夥伴未能如期交付資料中心容量；FY27 capex 指引由 $175B 微降至 $170B。","source":"TechNews 微軟 FY27 Q1 法說報導","url":"https://finance.technews.tw/2026/10/30/microsoft-earnings-report-data-center-lifespan-extended/","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"商業 RPO 在 FY26 Q2 約 $625B（+110%），其中約 45% 來自 OpenAI；管理層稱其餘 55% 來自廣泛客戶；管理層當時稱容量受限至少到財年底，需求超過基建。","source":"Fierce Network: OpenAI in focus as Microsoft's $625B backlog faces scrutiny","url":"https://www.fierce-network.com/cloud/microsoft-livin-ai-prayer","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FY27 Q1 Azure 成長 48%；指引 12 月季 Azure 成長 49%–50%（固定匯率），高於分析師預期；Oppenheimer 認為 Azure 擴張主要受基建可得性而非終端需求限制。","source":"Runtimewire / Tradingpedia (Oppenheimer) / Reuters 引述","url":"https://runtimewire.com/article/microsoft-revenue-hits-92-3-billion-as-azure-growth-accelerates-to-48","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Introl 二手分析：電力與資料中心空間（非晶片）為瓶頸；資料中心殼體建置 18–24 個月、電網接入主要市場可達 4 年以上、變壓器交期 128 週；文中引用緩解時間約 2026 年底/2027（未獨立證實）。","source":"Introl blog: Hyperscaler CapEx Hits $690B in 2026","url":"https://introl.com/blog/hyperscaler-capex-690-billion-microsoft-azure-power-bottleneck-2026","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261102","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2026 10-K 揭露：各國政府機關嚴格審視公司競爭行為，美英歐中均積極執法並制定數位市場新規，可能導致罰款或限制產品提供。","source":"SEC EDGAR 10-K FY2026 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm","excerpt":"Government agencies closely scrutinize us under U.S. and foreign competition laws. Governments are actively enforcing competition laws and regulations and enacting new regulations to intervene in digital markets, and this includes markets such as the EU, the United Kingdom, the U.S., and China.","as_of":"2026-07-29","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FTC 向微軟競爭對手問訊，強化對微軟捆綁與雲端授權的反壟斷調查","source":"PYMNTS: FTC Grills Microsoft Rivals to Bolster Antitrust Probe","url":"https://www.pymnts.com/antitrust/2026/ftc-grills-microsoft-rivals-to-bolster-antitrust-probe/","excerpt":"FTC Grills Microsoft Rivals to Bolster Antitrust Probe By PYMNTS | February 13, 2026 | Listen to Article Listen The Federal Trade Commission (FTC) has been asking several of Microsoft’s competitors about the company’s business practices as part of an ongoing antitrust probe","as_of":"2026-02-13","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"英國 CMA 對微軟啟動 SMS（策略市場地位）調查","source":"SDxCentral: UK's competition watchdog launches SMS investigation into Microsoft","url":"https://www.sdxcentral.com/tags/antitrust_1/","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"MSFT FY2026 10-K 揭露：美國關稅、AI 出口管制政策變動已且可能持續增加營運成本、造成產品持續性不確定，關稅波動可能影響雲端與裝置供應鏈成本競爭力。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm","excerpt":"U.S. tariffs, shifting AI export controls policies, and disagreements among governments on sanctions policies toward third countries, has and may continue to increase operational costs, create uncertainty in the continuity of our products, and accelerate sovereignty initiatives among international partners and customers.","as_of":"2026-07-29","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 載明美國出口管制限制 Microsoft 向特定國家實體提供許多產品與服務，且資料中心關鍵零組件供應有限、短缺。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm","excerpt":"U.S. export controls restrict Microsoft from offering many of its products and services to, or making investments in, certain entities in specified countries.","as_of":"2026-07-29","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K 稱certain critical device and datacenter components 供應商有限且短缺，競爭者共用同批供應商；列半導體、網通、電力、冷卻設備短缺風險","source":"Microsoft FY2026 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000789019/000119312526323660/msft-20260630.htm","excerpt":"There are limited suppliers for certain critical device and datacenter components, and those items are in short supply.","as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Nikkei報導（TechCrunch轉述）：Microsoft 欲最快2026年將Surface與資料中心所需元件最多80%移出中國製造；微軟未置評","source":"TechCrunch","url":"https://techcrunch.com/2025/10/16/microsoft-aws-and-google-are-trying-to-drastically-reduce-chinas-role-in-their-supply-chains","excerpt":"tech giants Microsoft, Amazon, and Google are ramping up efforts to move production of their products and data centers outside of China, Nikkei reported, citing supply chain sources. In particular, Microsoft wants to have up to 80% of the components needed to make its Surface notebooks and tablets, as well as its data centers, manufactured outside of China as soon as 2026, the report said.","as_of":"2025-10-16","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Taipei Times：Microsoft 計畫將台灣資料中心由2座增至4座，以降低單一事件造成營運中斷風險","source":"Taipei Times","url":"https://www.taipeitimes.com/News/biz/archives/2026/09/22/2003864650","excerpt":"Microsoft to double data centers in Taiwan MORE DATA CENTERS: Microsoft’s Taiwan-area general manager said the corporation is looking to add two more data centers in northern Taiwan over the next few years By Meryl Kao / Staff Reporter Add TT as Preferred Source Microsoft Corp plans to double its data centers in Taiwan from two facilities to four, Microsoft Taiwan general manager","as_of":"2026-09-22","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY26 Q1（2025-09 季）三段營收：Intelligent Cloud $30.9B +28%、Productivity & Business Processes 約$33.0B +17%、More Personal Computing 約$13.8B +4%；Microsoft Cloud $49.1B +26%","source":"Finviz / licenseq 摘要 (Microsoft FY26 Q1)","url":"https://licenseq.com/?p=21252","excerpt":null,"as_of":"2025-10-29","retrieved_at":"20261102","affects":["valuation","moat_trend"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"FY26 Q4 Intelligent Cloud 營收 +32% 至$39.3B；FY2026 全年 Intelligent Cloud $137.8B（FY2025 $106.3B）","source":"Microsoft FY2026 ARS / 二手報導","url":"https://www.sec.gov/Archives/edgar/data/0000789019/000119312526427876/d62902dars.pdf","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261102","affects":["valuation","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Synergy 2026 Q1 估計雲基礎設施份額：AWS 28%、Azure 21%、Google 14%（來源間數字不一，另有站台稱 Azure 23–25%、AWS 31%，未對照 Synergy 原文）；Q1 2026 全球雲基礎設施支出約$128.6B +35% YoY","source":"tech-insider.org / macmyths.com 引述 Synergy（二手）","url":"https://tech-insider.org/?p=8617","excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Microsoft 365 商用方案自 2026-07-01 漲價（Business Basic $72→$84、Business Standard $150→$168、E3 $36→$39/user/月，依來源）；獨立 Copilot $30/user/月不變；既有客戶於下次續約適用","source":"Office Watch / Directions on Microsoft / The Register","url":"https://www.theregister.com/2025/12/05/microsoft_365_prices_up_2026","excerpt":null,"as_of":"2025-12-05","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"MSFT FY2026 10-K 自述：多數業務進入門檻低、技術快速且具顛覆性演進；AI 產品與超大規模雲、開源及前沿模型供應商競爭（其中部分同時是夥伴），並點名 agentic computing 的重要性快速上升。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm","excerpt":"Barriers to entry in many of our businesses are low and many of the areas in which we compete evolve rapidly with changing and disruptive technologies, shifting user needs, and frequent introductions of new products and services.","as_of":"2026-07-29","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 述及 AI 產品與 hyperscalers、開源產品及前沿模型供應商競爭，部分為現有或潛在夥伴。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm","excerpt":"Our AI offerings compete with AI products from hyperscalers, open-source offerings, and frontier model providers, some of which are also current or potential partners.","as_of":"2026-07-29","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"部落格稱 AI agents（含 Copilot）壓縮 M365 生態 per-seat 收入。","source":"Collab365 blog","url":"https://collab365.com/blog/copilot-gutted-our-business-now-ai-agents-are-eyeing-saas-se","excerpt":"Could AI Agents Break Per-Seat SaaS Pricing? A founder's view of how AI agents could change software interfaces, usage and pricing, grounded in what Microsoft is already doing with Copilot licensing.","as_of":"2026-04-30","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2026 稱銷售與分銷模式持續演進以支援雲端、訂閱與用量計費產品，並同時保留多種取得管道（直銷＋間接通路）。","source":"SEC EDGAR 10-K FY2026 Item 1 Distribution, Sales, and Marketing","url":"https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm","excerpt":"Sales and distribution models continue to evolve to support cloud-based, subscription-based, and consumption-based offerings while maintaining multiple options through which customers may acquire and manage our products and services.","as_of":"2026-07-29","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q3 FY26 財報：Nadella 稱按人頭業務將成為按人頭加用量業務；GitHub Copilot 2026-06-01 轉全用量計費。","source":"Directions on Microsoft, Q3 FY26 take-aways: consumption pricing is coming sooner rather than later","url":"https://www.directionsonmicrosoft.com/microsofts-q3-fy26-take-aways-consumption-pricing-is-coming-sooner-rather-than-later/","excerpt":"But during Microsoft’s Q3 FY26 earnings call on April 29, Microsoft’s leaders made it clear that consumption-based pricing isn’t a distant goal; it’s on the near-term horizon. “Any per-user business of ours, whether it’s productivity, coding, security, will become a per-user and usage business,” CEO Satya Nadella told analysts on the call.","as_of":"2026-04-30","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Microsoft 將更多夥伴業務導向經銷商，直接帳單夥伴門檻提高。","source":"SoftwareOne, Microsoft partner offboarding explained","url":"https://www.softwareone.com/en/channel-partner/articles/2026/05/21/microsoft-partner-offboarding-explained","excerpt":null,"as_of":"2026-05-21","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Investing.com 列示分析師 12 個月目標價平均約 569.45 美元，高 870、低 400（日期不一，為聚合站快照）","source":"Investing.com Microsoft Corporation (MSFT)","url":"https://www.investing.com/equities/microsoft-corp","excerpt":"The average 12-month price target for Microsoft is 569.45 USD, with a high estimate of 870 USD and a low estimate of 400 USD.","as_of":"2026-08-12","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Oppenheimer 於財報前將目標價由 570 上調至 625 美元，其預估 FQ1 營收 900 億、EPS 4.69，低於市場預期 907.5 億／4.72；並提示 FY2027 資本支出為重大風險","source":"Tradingpedia, Oppenheimer lifts Microsoft target on cloud AI growth","url":"https://www.tradingpedia.com/2026/10/26/oppenheimer-lifts-microsoft-target-on-cloud-ai-growth/","excerpt":null,"as_of":"2026-10-26","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ1 FY2027 指引中位數 904 億美元，高於 LSEG 平均分析師預估 896.6 億（7 月財報時）","source":"搜尋摘要彙整（Microsoft 7 月財報報導）","url":"https://www.marketbeat.com/instant-alerts/microsoft-fy2027-eps-forecast-increased-by-erste-group-bank-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"證券集體訴訟待審：City of St. Clair Shores Police and Fire Retirement System v. Microsoft（W.D. Wash., No. 26-cv-02071），指 Microsoft 誇大 Copilot 能力與採用；class period 2025-05-01 至 2026-01-28；原告律所新聞稿，指控未經證實。","source":"Pomerantz LLP 新聞稿（newswire.com）","url":"https://www.newswire.com/news/pomerantz-llp-highlights-class-action-filing-against-microsoft-corporation-msft","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-28 8-K Item 8.01：因 2026-09 公告之分部報告變更（新增 Agents and Infra、Devices and Consumer 分部）而重編（recast）FY2026 10-K 金額；為分部列報調整，非財報重編錯誤更正。","source":"SEC EDGAR 8-K 2026-10-28 Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/789019/000119312526436149/msft-20261028.htm","excerpt":"Microsoft Corporation (the “Company”) is filing this Current Report on Form 8-K to recast certain previously reported amounts to conform with segment reporting changes made to align our segments with how we manage our business","as_of":"2026-10-28","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 9 份 8-K 中僅 1 份含重大項目（為上述分部 recast 之 8.01），其餘為財報、董事異動、Reg FD。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["triggers"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"證券集體訴訟待審：City of St. Clair Shores Police and Fire Retirement System v. Microsoft（W.D. Wash., No. 26-cv-02071），class period 2025-05-01 至 2026-01-28，指控涉及 Copilot；1/29 股價跌約 10%（$481.63→$433.50）。原告律所稿，指控未經證實。","source":"Pomerantz LLP 新聞稿（newswire.com）","url":"https://www.newswire.com/news/pomerantz-llp-highlights-class-action-filing-against-microsoft-corporation-msft","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"未見 SEC 調查或財報重編；2026-10-28 8-K 僅為分部報告變更之 recast。","source":"SEC EDGAR 8-K 2026-10-28 Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/789019/000119312526436149/msft-20261028.htm","excerpt":"Microsoft Corporation (the “Company”) is filing this Current Report on Form 8-K to recast certain previously reported amounts to conform with segment reporting changes made to align our segments with how we manage our business","as_of":"2026-10-28","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"sec_investigation_restatement#1","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 中無 Item 4.02（非可信賴財報）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MSFT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.66,"operating_margin_pct":47.1,"fcf_margin_pct":17.31,"rd_intensity_pct":10.52},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"GOOGL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.86,"operating_margin_pct":33.32,"fcf_margin_pct":4.19,"rd_intensity_pct":15.81},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"CRM","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":77.28,"operating_margin_pct":21.52,"fcf_margin_pct":34.49,"rd_intensity_pct":14.49},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRM","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"ADBE","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":89.25,"operating_margin_pct":35.7,"fcf_margin_pct":40.79,"rd_intensity_pct":18.07},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADBE","as_of":"TTM ending 2026-08-31（4季加總）"}},{"name":"TEAM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":84.83,"operating_margin_pct":0.16,"fcf_margin_pct":20.07,"rd_intensity_pct":49.74},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TEAM","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"MSFT"},"financial_history":{"ticker":"MSFT","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":211915000000.0,"revenue_yoy_pct":null,"gross_margin_pct":68.92,"operating_margin_pct":41.77,"net_income":72361000000.0,"diluted_eps":9.68,"free_cash_flow":59475000000.0,"fcf_margin_pct":28.07,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":245122000000.0,"revenue_yoy_pct":15.67,"gross_margin_pct":69.76,"operating_margin_pct":44.64,"net_income":88136000000.0,"diluted_eps":11.8,"free_cash_flow":74071000000.0,"fcf_margin_pct":30.22,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":281724000000.0,"revenue_yoy_pct":14.93,"gross_margin_pct":68.82,"operating_margin_pct":45.62,"net_income":101832000000.0,"diluted_eps":13.64,"free_cash_flow":71611000000.0,"fcf_margin_pct":25.42,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":331839000000.0,"revenue_yoy_pct":17.79,"gross_margin_pct":67.94,"operating_margin_pct":46.78,"net_income":133749000000.0,"diluted_eps":17.95,"free_cash_flow":66987000000.0,"fcf_margin_pct":20.19,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MSFT/MSFT_Q1_2027_Earnings_Call_20261028.md）

# Q1 2027 Earnings Call
**Microsoft Corporation** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Greetings, and welcome to the Microsoft Fiscal Year 2027 First Quarter Earnings Conference Call. [Operator Instructions] As a reminder, this conference is being recorded. It is now my pleasure to introduce Jonathan Neilson, Vice President, Investor Relations.

**Jonathan Neilson** (Executives):
Good afternoon, and thank you for joining us today. On the call with me are Satya Nadella, Chairman and Chief Executive Officer; Amy Hood, Chief Financial Officer; Alice Jolla, Chief Accounting Officer; and Brian DeFoe, Deputy General Counsel and Corporate Secretary.
On the Microsoft Investor Relations website, you can find our earnings press release and financial summary slide deck, which is intended to supplement our prepared remarks during today's call and provides the reconciliation of differences between GAAP and non-GAAP financial measures. More detailed outlook slides will be available on the Microsoft Investor Relations website when we provide outlook commentary on today's call.
On this call, we will discuss certain non-GAAP items. The non-GAAP financial measures provided should not be considered as a substitute for or superior to the measures of financial performance prepared in accordance with GAAP. They are included as additional clarifying items to aid investors in further understanding the company's first quarter performance in addition to the impact these items and events have on the financial results.
All growth comparisons we make on the call today relate to the corresponding period of last year, unless otherwise noted. We will also provide growth rates in constant currency when available as a framework for assessing how our underlying business performed, excluding the effect of foreign currency rate fluctuations. Where growth rates are the same in constant currency, we will refer to the growth rate only.
We will post our prepared remarks to our website immediately following the call until the complete transcript is available. Today's call is being webcast live and recorded. If you ask a question, it will be included in our live transmission, in the transcript and in any future use of the recording. You can replay the call and view the transcript on the Microsoft Investor Relations website.
During this call, we will be making forward-looking statements, which are predictions, projections or other statements about future events. These statements are based on current expectations and assumptions that are subject to risks and uncertainties. Actual results could materially differ because of factors discussed in today's earnings press release, in the comments made during this conference call and in the Risk Factors section of our Form 10-K, Forms 10-Q and other reports and filings with the Securities and Exchange Commission. We do not undertake any duty to update any forward-looking statements.
And with that, I'll turn the call over to Satya.

**Satya Nadella** (Executives):
Thank you very much, Jonathan. It was a fast start to our fiscal year. Microsoft Cloud revenue surpassed $63 billion with growth accelerating to 30% year-over-year. We are focused on 3 things: designing AI to empower people, ensuring every organization has sovereignty over its own learning and building trust with controls that ensure agent safety and security.
Now let's talk about how we are making progress on those goals as we build a new tech stack, starting with Copilot. We announced our biggest update to Copilot to date this quarter, bringing together Chat, Cowork, Autopilot and Code into one unified experience. It's one product experience across commercial and consumer and comes with all of Office built in. We think of Copilot as the new OS for work.
Customers are increasingly turning to Copilot to get real work done. Automated tasks have nearly doubled since July. Daily users are up nearly 50% quarter-over-quarter and over 5x year-over-year. User satisfaction improved nearly 20% quarter-over-quarter to another all-time high. And 90% of Copilot queries use Auto mode, which dynamically routes tasks across models optimizing for quality, speed and cost. These improvements are translating into larger purchases. The number of customers with more than 50,000 Copilot seats increased over 8x year-over-year, including Capgemini, HCLTech, Hitachi Group, Truist Financial and U.K. Revenue and Customs Department. And just last week, Volkswagen announced plans to deploy Copilot to more than 330,000 employees, one of the largest deployments to date in Europe.
We're also seeing strong momentum with E7, which brings together Copilot, E5, Entra and Agent 365. Thousands of customers in every industry have purchased the suite to date, including Amadeus, BlackRock, Fiserv and New South Wales Health Department and ZEISS.
Our business model is expanding from per seat subscriptions to include consumption, expanding our TAM and ARPU. The subscription brings increasingly capable everyday intelligence to every user. Typically, IT funds this, consolidating frontier advances for everyone across the organization. And as agents take on higher-value work, consumption opens up business funded demand with spending tied directly to the value these agents deliver. The number of Copilot customers actively consuming credits through usage-based billing grew over 75% over the quarter.
When it comes to software development, all major coding agents have shown up to work on GitHub. Agent-generated PRs have increased 6x over the past 6 months, and agents now open more than 1/3 of all PRs on the platform. We are very hard at work on reliability as agentic activity on GitHub soars. At GitHub Universe this morning, we shared how we are expanding capacity and rebuilding the core Git architecture for the Agentic wave. Also at Universe, we announced broad availability of Copilot Fusion, which is all about bringing multi-model orchestration to software development. It delivers frontier-level quality up to 40% faster and at up to 77% lower cost.
Credit consumption from Agentic features on GitHub has more than doubled since usage-based billing went into effect. And we're also helping developers secure their code and turn AI-generated code into high-quality software. GitHub Advanced Security revenue increased over 50% year-over-year as customers use its AI capabilities to scan entire repos and fix vulnerabilities in real time.
In the business application space, we are extending this vision of Copilot as the new OS for work, bringing the business logic and capabilities of Dynamics 365 directly into Copilot and helping every organization stand up their own infinite SaaS factory. This quarter, we introduced 30 new Copilot skills across Dynamics 365, which enables customers to access CRM and ERP capabilities directly in the flow of work.
In recruiting, more than 10 million LinkedIn members use our LinkedIn AI-powered job search daily and 25,000 customers are using our agentic hiring solutions. Recruiters using Hiring Assistant are finding interview quality applicants 33% faster while reviewing 83% fewer profiles to find qualified match.
In healthcare, we automated 30 million patient encounters this quarter, up 70% year-over-year, helping clinicians spend less time on administrative work and more time with patients. 10 providers, including Advocate Health, Mass General Brigham, Mercy, Intermountain Health and others have used our solutions to document over 1 million encounters each since the beginning of the calendar year. And in Science, our FDE teams are working with customers to use Discovery to accelerate scientific progress. A great example is Saint-Gobain, which used Discovery to accelerate the development of low-carbon construction materials.
Underneath our first-party agentic experience is a common platform. It starts with Foundry, which is becoming an increasingly important driver of our growth. Foundry helps organizations build learning loops grounded in their business context and deploy agents safely at scale. We now have over 120,000 Foundry customers with revenue more than tripling year-over-year.
Foundry's model choice and feature set, coupled with its deep integration across our stack is driving differentiation. Azure OpenAI directly benefited in the last quarter with big advances in OpenAI models. And when you couple this with our model choice built into Foundry, customers are able to build solutions optimizing across quality, cost and performance. In fact, the number of customers building agentic solutions with multiple models increased 5x year-over-year and revenue from open source models on Foundry increased 10x. We also continue to make rapid progress with our first-party models. Our goal is to advance the cost-to-outcome frontier, which means delivering capabilities comparable to leading models within 3 to 6 months of their release at a fraction of the training cost, thereby allowing us to transfer those cost benefits to customers. And you see this in our products today.
MAI-Cyber now powers over 40% of the scans in our Agentic MDASH code scanner at 18% lower cost per scan. MAI-Transcribe is the most accurate and cheapest transcription model in the world, supporting Dragon Copilot's multilingual workflow. MAI Code Flash has 3 million users in GitHub Copilot last month alone, helping developers get more out of their AI credits. Microsoft-Decision-1 is our new model for structured decision-making, outperforming both LLMs and other decision models in latency and quality. Over 4,000 customers, including Atos Group, Equinor and RBI have already used it in the first month since its release.
And we recently completed pretraining MAI-Base-2, which outperforms other open weight models we tested with 4 to 12x greater training compute efficiency. This base model will be used in the upcoming MAI models across thinking, code and cyber.
Beyond models, we are making the harness behind our own Copilot experience available to customers in Foundry. It gives customers a Microsoft managed way to build agents that reason, use tools, complete complex, long-running work while preserving their choice of model.
Another critical layer is data. We now have 44,000 paid Fabric customers, up more than 50% year-over-year. We are bringing Foundry and Fabric closer together so you can build your own agents right next to data. Over 19,000 customers now use Foundry and Fabric as enterprises connect and operate agents over real-time operational, analytical and unstructured data.
Customers are also rapidly deploying our AI optimized databases, including PostgreSQL, SQL DB Hyperscale, Cosmos DB to give agents fast, secure access to the data and context they need. PostgreSQL growth accelerated for the fourth consecutive quarter, and the number of PostgreSQL customers also using Foundry accelerated to 90% year-over-year.
We also have one of the most important databases for any enterprise, which is the knowledge underneath Microsoft 365 spanning people, their relationships, documents, e-mails, meetings, chats, projects and other artifacts. Work IQ makes this context available to every Agentic workload. And with Microsoft IQ, we are bringing together Work IQ, Fabric IQ and Foundry IQ as a unified context for Agentic systems.
Nearly 60,000 customers are accessing context across Microsoft IQ, up 25% quarter-over-quarter. As enterprises deploy more agents, they also need to govern them at scale. With Agent 365, we provide a platform for AI observability, enabling customers to manage, secure and optimize the performance and cost of their agents. Over 50 million agents are now in the registry, up over 30% quarter-over-quarter. And finally, as agents gain greater access to enterprise data and systems, security becomes even more critical.
Our approach is to separate intelligence from authority, enforcing identity, permissions, monitoring and containment outside the model itself. Last week, we expanded Perception with new capabilities to help customers secure and contain agentic insiders, including expanded agent discovery across local and cloud environments, dynamic permissions that enforce least privileged access for each task and continuous risk assessment.
We also introduced Teams of Guardian agents that continuously monitor agent activity to help prevent unsafe actions before they occur. And we are seeing encouraging feedback on Perception overall from preview customers, including KPMG, Nationwide Building Society, Northern Trust, Stellantis. More broadly, we are helping customers secure and govern AI use across the enterprise. Customers have used Microsoft Purview to audit over 7.6 billion agent activities to date, up 5x quarter-over-quarter.
Underlying everything I've talked about so far is our infrastructure. We are building against a growing book of business with a fungible fleet that allows us to dynamically allocate capacity to the highest value opportunities across compute, data, Foundry and Copilot. Accelerating demand led to us adding 24 new data centers across 5 continents this quarter. And we are bringing capacity online faster, reducing dock-to-live times by about 20% quarter-over-quarter for new GB300s in our biggest regions, which make up the majority of the GPU deployments. At the same time, we continue to get more from the infrastructure we already have by optimizing across the data center design, silicon systems, software and models. For example, we increased the throughput for Copilot workloads by over 50% quarter-over-quarter.
We continue to scale our fleet with the latest innovations from NVIDIA and AMD alongside our own Maia systems. We have docked our first NVIDIA Vera Rubin GPUs and are very excited about it. Maia 200 is already delivering up to 1.7x more tokens per watt across the AI experiences in Teams and Copilot, and Maia 300 will drive further gains, delivering 40% more tokens per watt compared to the leading GPU-based systems.
Our growth extends beyond GPUs. We continue to see strong adoption of our cloud-native Cobalt CPUs, improving price performance for general-purpose cloud workloads. All up, Azure growth was broad-based across both enterprises and small and medium business segments and spanning both core cloud services and AI infrastructure.
Finally, let me turn to devices and consumer. In Windows, we are executing on our vision to bring hybrid intelligence to every desk and every home, making every PC the secure agent box. As more capable models run locally, we see an opportunity to make it more intelligence effectively unmetered. We are working with the broader hardware ecosystem to bring these capabilities to a new generation of PCs across AMD's Ryzen AI 400 Series, Intel Core Ultra Series 3, Qualcomm's Snapdragon X2 series. And earlier this month, we also announced new PCs powered by NVIDIA's RTX Spark and DGX Station for Windows. With these new devices, you can run last year's Frontier models on your laptop and last quarter's model at your desk.
We are bringing together Windows and Agent 365, so agents can work with secure boundaries on device. We introduced Microsoft Execution Containers, a policy-driven execution layer that governs and contains agents across Windows and other platforms integrated with Agent 365 for governance and observability. Agents like OpenAI Codex, Anthropic Claude Code, Meta Muse are adopting MXC and customers like Meta are starting to deploy it across their enterprise environments.
In search and advertising, Bing and Edge once again took share. In LinkedIn, engagement continues to deepen across our more than 1.4 billion members with time spent viewing content in the feed up 15% year-over-year.
And finally, in gaming, we remain focused on building great games and reaching players wherever they choose to play across console, PC, mobile and cloud. Minecraft delivered a record quarter, reaching all-time highs in both engagement and revenue, while World of Warcraft had its largest beta in franchise history.
We entered the holiday season with one of our strongest first- and third-party lineups in years, including Modern Warfare 4, which launched last week to the best reviews for a Call of Duty game in more than a decade and Grand Theft Auto VI, which is coming to Xbox next month.
In closing, based on the demand we see, the strength of our products and the efficiency we are driving across the stack, I've never been more confident in the long-term returns for our investments.
With that, let me turn it over to Amy.

**Amy Hood** (Executives):
Thank you, Satya, and good afternoon, everyone. Our results exceeded expectations across revenue, operating income and earnings per share, driven by strong demand across the Microsoft Cloud. This quarter, revenue was $92.3 billion, up 19%. Gross margin dollars increased 17% and gross margin percentage was 68%. Operating income increased 21% and 22% in constant currency. Earnings per share was $4.89, an increase of 18% and 19% in constant currency when adjusted for the impact from our investment in OpenAI. And FX was roughly in line with guidance.
Operating expenses increased 6%, driven by continued investments in R&D compute, capacity and talent. Operating margins increased slightly year-over-year to 50%, driven by strong revenue growth, platform efficiency gains and focused investments across our portfolio, partially offset by sales mix shift to Azure.
When adjusted for the impact from our investments in OpenAI, other income and expense was negative $234 million, slightly lower than expected. Capital expenditures were $45.2 billion as some third-party capacity deliveries we expected in Q1 were delayed. Roughly 3/4 of our CapEx was for short-lived assets, primarily CPUs and GPUs, including higher memory and storage costs as we continue to invest in the infrastructure required for our customers to build and scale AI applications.
The remaining spend was for long-lived assets. This quarter, finance leases were $7.4 billion. As a reminder, we recognize the full principal value of finance leases and CapEx at the time of lease commencement. And cash paid for PP&E was $39.4 billion. Cash flow from operations was $58 billion, up 29%, driven by strong cloud billings and collections. And free cash flow was $18.6 billion, reflecting higher capital expenditures. And finally, we returned $10.2 billion to shareholders through dividends and share repurchases.
Now to our segment results reported under the updated segment structure announced in September. Revenue from Agents and Infra was $76.8 billion and grew 25%, reflecting strength across the connected layers of our platform. Commercial bookings decreased 12% and 11% in constant currency, driven by the impact from large Azure commitments in the prior year, partially offset by healthy growth in our commercial sales motions, including a large Azure commitment this quarter.
Commercial remaining performance obligation grew 73% to $677 billion, with a smaller sequential decline relative to historical seasonality due to the large Azure commitment this quarter. Our RPO has a weighted average duration of 2.3 years and roughly 30% will be recognized in revenue in the next 12 months, up 29% year-over-year. The remaining portion recognized beyond the next 12 months increased 98%.
Now to Microsoft Cloud. Revenue was $63.9 billion and growth accelerated to 30% and 31% in constant currency with sequential dollars added nearly doubling year-over-year, reflecting strong demand across Azure and M365 Commercial Cloud. Azure revenue was ahead of expectations and increased 48%, even with the 3P capacity delays noted earlier, driven by Foundry and improved CPU monetization.
Foundry revenue more than tripled year-over-year with upside driven by efficiency gains across our GPU fleet that allowed us to allocate additional capacity to customers as well as higher revenue per token that we benefited from in the quarter. Across our CPU fleet, engineering work enabled us to identify and monetize underutilized capacity this quarter, helping us serve more of the growing demand with our existing capacity. The timing of engineering efficiencies like these as well as 3P GPU lease deliveries, our own capacity build-outs and ARPU changes from model mix can create quarterly variability in the year-over-year growth rate.
M365 Commercial Cloud revenue increased 18% and 19% in constant currency when adjusted for the prior year comparable that benefited from 1 point of in-period revenue recognition. On a reported basis, revenue growth was 17% and 18% in constant currency. Results were ahead of expectations, driven by stronger GitHub Copilot adoption and usage, partially offset by weaker sales execution in our M365 E3 and stand-alone SKUs.
We continue to evolve our sales motions to balance those more traditional SKU per-seat rhythms with the newer premium E7, M365 Copilot and usage-based productivity offerings. Year-over-year growth was driven by both ARPU and seats. ARPU growth was led by our premium seat-based offerings, including M365 Copilot, E5 and E7, which has already reached millions of paid seats with additional contribution from usage-based offerings, primarily GitHub Copilot. And Copilot revenue growth accelerated quarter-over-quarter with continued adoption across M365, GitHub and Security.
Paid M365 Commercial seats grew 5% with some impact from the weaker sales execution noted earlier. Growth was driven by installed base expansion across all customer segments, though primarily in our SMB and frontline worker offerings. M365 Consumer Cloud revenue increased 17% and 16% in constant currency, down sequentially as we begin to lap the benefit from the price increase in the prior year.
Productivity and server licensing revenue decreased 3% and 2% in constant currency, primarily driven by a decrease in transactional purchasing as we lap the benefit from product launches in the prior year, partially offset by a greater mix of contracts that carry higher in-period revenue recognition.
Industry Solutions Cloud revenue increased 10% with growth in Dynamics 365 and LinkedIn Talent Solutions, though booking trends continued to moderate. And in Frontier and Support Services, revenue increased 4% and 5% in constant currency, driven by support.
Microsoft Cloud gross margin percentage declined year-over-year to 66%, driven by sales mix shift to Azure, partially offset by product level margin improvements, primarily in Azure. And for this segment, gross margin dollars increased 20% and 21% in constant currency. Operating expenses increased 10%, driven by the R&D investments noted earlier. Operating income grew 24% and 25% in constant currency, and operating margins decreased slightly year-over-year to 53% as strong revenue growth, platform efficiency gains and focused investments across our portfolio were more than offset by sales mix shift to Azure.
Now to Devices and Consumer. Revenue was $15.5 billion and declined 3%. Search and advertising revenue ex-TAC increased 12% and was ahead of expectations, driven by higher volume and rate across LinkedIn, Edge and Bing. Xbox revenue decreased 2% and Xbox content and services revenue decreased 2% and 1% in constant currency, driven by declines in third-party content and Xbox Game Pass, partially offset by growth in first-party content. And Windows OEM and devices revenue decreased 22%. Windows OEM revenue was below expectations and decreased 27% and 28% in constant currency, driven by the Windows 10 end of support demand in the prior year, inventory drawdowns by OEM and channel partners and weaker PC market demand. Inventory levels remain elevated.
Segment gross margin dollars were relatively unchanged year-over-year and operating expenses decreased 3%, driven by Xbox, partially offset by the continued investments in R&D noted earlier. Operating income increased 2% and 3% in constant currency, and operating margins increased year-over-year to 35%, driven by lower amortization of intangible assets from the Activision acquisition, partially offset by the impact from a lower mix of Windows OEM revenue.
Now moving to the outlook for our second quarter, which unless specifically noted otherwise, is on a U.S. dollar basis. Based on current rates, we expect FX to have no meaningful impact on total revenue, COGS or operating expense growth, or on revenue growth in either segment. Starting with segment guidance. We expect revenue from Agents and Infra of USD 80.1 billion to USD 80.7 billion or growth of 24% to 25%. In commercial bookings, we expect healthy growth in our commercial sales motions, the results will be impacted by the significant Azure commitments signed in the prior year. Timing related to significant Azure commitments like these will result in material volatility in bookings, making quarterly growth rates less indicative of underlying sales execution. In Azure, we expect revenue growth of 49% to 50% in constant currency with continued efficiency gains across our CPU and GPU fleet, helping to offset some 3P GPU-as-a-Service contracts that have been delayed to H2.
Customer demand continues to exceed available supply. And looking beyond Q2, year-over-year growth will continue to reflect the timing and scale of engineering efficiencies delivered in the quarter and new capacity adds as well as a strong prior year comparable that included accelerating growth in the second half.
In M365 Commercial Cloud, we expect growth of approximately 19% in constant currency with FX expected to reduce reported growth by less than 1 point. We expect continued momentum across our premium per seat offerings and usage-based offerings, along with some improvement in execution across E3 and our stand-alone SKUs. Growth will be driven primarily by ARPU with additional contribution from seats, and we continue to expect revenue growth to accelerate through the year. M365 Consumer Cloud revenue should grow in the low teens, down sequentially as we lap the price impact noted earlier.
Productivity and server licensing revenue should decline in the mid-to-high single digits, down sequentially due to a lower expected mix of contracts that carry higher in-period revenue recognition. Quarterly growth can vary materially based on contract mix, product launch timing and other transactional purchasing trends.
In Industry Solutions Cloud, we expect revenue growth to be in the mid-to-high single digits with continued impact from the bookings trends noted earlier. And in Frontier and Support Services, we expect revenue to grow in the low to mid-single digits. Microsoft Cloud gross margin percentage should be roughly 65%, down year-over-year as continued improvement in product level margins is more than offset by sales mix shift to Azure.
In Devices and Consumer, we expect revenue to be USD 15.9 billion to USD 16.4 billion. Search and advertising revenue ex-TAC growth should be in the low double digits, driven by consistent trends in rate and volume with overall search and advertising revenue expected to grow at a similar rate. And in Xbox Content and Services, we expect revenue growth to be in the mid-to-high single digits, up sequentially, driven by the timing of content launches across both third and first party.
With content launch patterns through the year, we expect growth to be the strongest in the second quarter with some deceleration in Q3 and further moderation in Q4. Hardware revenue in Q2 should decline year-over-year. Windows OEM and devices revenue should decline in the mid-30s. Growth will continue to be impacted by elevated inventory levels, PC market demand and a prior year comparable that benefited from Windows 10 end of support. As in prior quarters, the range of potential outcomes remains wider than normal. We expect these trends to continue through the rest of the fiscal year. Therefore, at a total company level, revenue should be between USD 96 billion and USD 97.1 billion or growth of 18% to 19%. We expect COGS of USD 32.7 billion to USD 32.9 billion or growth of 26% to 27% and operating expense of USD 18.5 billion to USD 18.6 billion or growth of 9%, driven by continued investment in R&D compute capacity and talent.
Our cost guidance across both COGS and OpEx includes an estimate for the recently announced employee voluntary exit offer. Operating margins should be down slightly year-over-year. Excluding any impact from our investments in OpenAI, other income and expense is expected to be roughly negative $300 million as interest income will be more than offset by interest expense, which includes the interest payments related to data center finance leases. And we expect our Q2 effective tax rate to be approximately 20%.
Next, capital expenditures. In Q2, we expect CapEx spend will be over $50 billion. Therefore, for the calendar year, spend should be approximately $170 billion due to the 3P capacity delays noted earlier. In the second half of the fiscal year, we currently expect CapEx spend to accelerate primarily from CPUs, inclusive of higher memory and storage costs and GPUs as well as the 3P capacity deliveries that shifted to H2. And as we continue to improve the efficiencies of our infrastructure, each dollar of CapEx has the potential to support more revenue and higher returns over time.
Given our strong business performance, we expect to continue to remain free cash flow positive in FY '27. To complement cash generated by the business and preserve financial flexibility, we will access additional sources of funding when we believe it is attractive to do so.
In closing, we are off to a strong start to FY '27 with accelerated growth across the Microsoft Cloud. Product improvements, along with efficiency gains across our data center infrastructure and our first-party apps and agents are increasing the value and improving the outcomes we deliver to our customers. Delivering that value to our customers positions us for durable long-term growth.
With that, let's go to Q&A, Jonathan.

**Jonathan Neilson** (Executives):
Thanks, Amy. We'll now move over to Q&A. [Operator Instructions] Operator, can you please repeat your instructions?

**Operator** (Operator):
[Operator Instructions] And our first question comes from the line of Adam Wood with Morgan Stanley.

**Adam Wood** (Analysts):
[Technical Difficulty] alongside lower expected CapEx and those better cloud gross margins sequentially. Can I ask, as incremental AI capacity comes online, what do you see as likely to be the more important driver of returns over the next few years, improving utilization and unit costs within Azure, or your ability to monetize more layers of each workload across Fabric, Foundry and Copilot?

**Satya Nadella** (Executives):
Thanks for the question, Adam. I'd say all of the above. But I think the way we're coming at this is we have one pool, and we want to get the pool to be as efficient and fungible, right? That's sort of the place where if I sort of think about all of the physics of how we're building out the data centers, all of the operational rigor with which we can bring up the capacity. And then, of course, how do we run the workloads that are optimized on that infrastructure. And once you do that, then it's just a function of how we allocate it by looking at the demand signal.
And even there, even in our new segment reporting, I think you kind of see it, which is Copilot, Copilot stateful database underneath it is Work IQ. That gets used in Foundry, which is where people will build, let's say, a multi-agent system for supply chain that spans both unstructured and structured. Of course, it uses a Postgres database in Azure. And so -- and then, by the way, all the agentic work is registered in the Agent 365 and Perception manages the security of it, right?
So to us, at least we look at all of this as the same infrastructure. Of course, we report to you in a variety of different products. But your core question of where is the margin going to come from, where the leverage is going to come from. It's not going to come from any -- it's going to come from every one of them, and it compounds when we work them across.

**Amy Hood** (Executives):
I think that's -- and Adam, I probably missed the front half of your question. I think we at least caught the back half.

**Operator** (Operator):
The next question comes from the line of Karl Keirstead with UBS.

**Karl Keirstead** (Analysts):
Amy and Satya, I'm wondering if you could unpack what I thought was one of the key metrics from this call, and that is the guidance for Azure growth of 49% to 50% constant currency in December. I can imagine there's a number of variables, the capacity you're putting up, the allocation to third-party customers, probably OpenAI strength. But perhaps you could comment a little bit on what some of the key drivers are given how good that number seems at least to me.

**Amy Hood** (Executives):
Thanks, Karl, for the question. Maybe I'll start by talking a little bit about Q1, and I think that will help to think through Q2 and even going forward. And it's not unrelated really to Adam's question at some level as well.
In Q1, I would say the engineering teams have really delivered very, very good work in terms of improving efficiency at the platform layer. That is not just a statement around the efficiency of GPUs. It's a statement around the efficiency of every layer, how the app utilizes the platform and how Foundry utilizes the platform as well as the Azure platform itself. Those efficiencies -- they're sort of ground out every week, and you have good ideas, a lot of work, some don't, and you stay at it. So they're not maybe as predictable in terms of how much impact we'll get in quarter. Q1, they did a very good job. And you saw some of that result in us being able to put more allocation into Foundry in the quarter. That's a great thing because we're -- as I said in the call, we still have demand that exceeds supply. So where we can have our engineering teams deliver those efficiencies, we do really try to put it into Foundry when we can because it's so important, as Satya talked about, into how customers broadly are building what I would call against the new stack.
Secondly, and you mentioned it, token pricing will create a little bit of variability. We had higher token pricing than we expected in the quarter. Listen, high-quality models that we're able to take advantage of and see good margins on do benefit us in the quarter, and that did happen in Q1. And I think also in that number in Q1 was the efficiencies I talked about applied not just to our GPU fleet. But I think people sort of underestimated when the example Satya gave for Adam's question that the GPU, CPU storage memory workload. I mean it takes all of the pieces. And so our ability to also create additional capacity within our existing fleet gave us some room to be able to convert that actually pretty quickly as well in Q1.
So in Q2, we've got those efficiency gains, which is great, and those will continue into Q2. We need to find some more, which we're counting on, enable to get to that guidance that I gave because I have faith in the team's work in Q1 continuing into Q2. But we also need that work to be able to help us a little bit because we had some supply we were counting on Q2 move out into H2. And so I think -- and to your point, there's also some unknown on some token pricing through the quarter, that stuff can change. So I think I feel good in terms of the efficiency gains that we saw we were able and when I'm able to see those and put them in, I feel good about guiding to that. But as other things are less predictable, I mean I hope that's helpful on the levers, Karl.

**Operator** (Operator):
The next question comes from the line of Mark Moerdler with Bernstein Research.

**Mark Moerdler** (Analysts):
Congratulations on the solid quarter and the solid guidance. It's really nice to see how well you guys are executing. I'd like to get a sense on the drivers of the AI strength in Azure being from enterprise versus digitally native in general or AI native. With inferencing starting to ramp and Microsoft the go-to for enterprises, how should we think Amy about the mix of enterprise customer workloads within overall workloads at this point? And Satya, with the strong growth of the Azure AI platform offering, can you give us color on what's driving that? Is it, again, enterprise? Is it digitally native? Obviously, it's a mix of both. But any color that shows the ramp of that enterprise, I think, would be valuable.

**Satya Nadella** (Executives):
Yes. Thanks for the question, Mark. Maybe I'll start and Amy, you can add to it. I was even here in Europe just last week, and it was great to see the qualities of the Agentic systems, right, that are just broadly getting deployed, right, where Unilever deploys what is their automated order taking and trade coupon dispute management stuff, all as a fully agentic touchless system. Rolls-Royce deploys a system to really manage all of their maintenance or whatever their jet engines with 30,000 parts, a pretty complex supply chain, both planning, execution, inventory management systems, all built on Foundry, Agentic systems.
RBI, which is an Austrian bank, showed me 20-plus business processes end-to-end. And they were talking about like whether it's in for credit or what have you, how they are able to now do that so much more optimally, right? So the breadth, the quality, their ability -- by the way, the multimodel nature of it, right? And they look -- they start with a Frontier model. Many of them -- in fact, the Unilever one, they just dropped an MAI model trained using our traces. So even the degree of sophistication of what I think of as model optimization, workload optimization, token optimization was just great to see. So the breadth is starting. Finally, it does feel like the enterprise workloads. They feel like to me, like the database applications enterprises built in the past that I grew up with is happening now when it comes to AI.
And in fact, maybe in some of the shiny object stuff is waning, right, which is not about the next big thing. They're really more about, wow, can I build the system? Can I own the weight? Can I manage my costs? Can I have reliability? What about security? And so in that sense, the enterprise breadth motion is starting. But like everything else, the enterprise stuff is not like a quarter-over-quarter. It's a decade-long thing, and that's what I've been waiting for as opposed to like 4 customers who buy a lot of capacity from you and you can show a few quarters of growth. And that's not a business as far as I'm concerned. So I want the breadth. We are well positioned on the breadth. And we have large customers who want to buy from us, and we're open for business with it. And as long as the pricing is right, we may sell them some. If not, we will be patient about building the breadth of business.

**Operator** (Operator):
The next question comes from the line of Gabriela Borges with Goldman Sachs.

**Gabriela Borges** (Analysts):
Satya, I want to stay on the topic of breadth because you had a comment in the prepared remarks talking about how MAI can now be comparable to leading models within 3 to 6 months of their release. At the same time, you have OpenAI at 11% of revenue in the quarter. So maybe just take a step back, can you give us your latest thinking on how you think token mix and token value is going to evolve between the Frontier MAI and maybe what some of your more sophisticated enterprise customers are doing from a proprietary AI strategy standpoint?

**Satya Nadella** (Executives):
Yes. So I think, in fact, I would say that you should think of 3 things perhaps as in the toolbox for any workload. The first is a new model drops and it's got some great performance and you want -- you can eval Max on whatever that matters to you, i.e., the outcome that matters to you by using it, people should use it. We saw that with some of the OpenAI models in the last quarter. They were fantastic models. And we're obviously very thrilled about the progress OpenAI has made with Astra and also what's to come. And I thought we saw some good demand on that.
Then the next thing people do is, hey, can I actually put multiple of the Frontier models because these -- these are very different prices. In fact, this morning, Artificial Analysis has the -- what I think is the real benchmark, which is the coding agents using our Fusion, and I think we were #2 or #3 there, which is awesome to see, right, which is you can now get Frontier performance 45% faster, 75% cheaper. Like why -- who would want to not take that, right, which is like if you're a coding agent user, you want, in fact, Anthropic and OpenAI, by the way, to compete for your workload, not like once a quarter, but for every task. And that, to me, is what the value of these routers and auto Fusion stuff routing does, and we are very excited about it.
And then the last thing is another important one. A lot of customers are saying, hey, look, take the Unilever one, right? It's their system. They will ultimately take even the traces after having done even a bunch with Frontier models, and they just want to train their own model. So it could be open-weight or in this case, it was MAI model. And so I think all of that needs to be as options that are available. And then depending on pricing, depending on the need of the customer, they will exercise it. And there's a temporality to it. It's never like, oh, I start one place and that's where I stop, right? It's like I may start at the Frontier, I may go to an open-weight, I may go to an MAI model. I may go back to the Frontier for the next drop for a few months, come out. Like that's how I think -- how dynamic these workloads are. And that's where when we think about Foundry or when we think about Fabric or when we think about Copilot and GitHub Copilot, we really want to build a model system that delivers customers' value continuously versus them being stuck in any one thing.

**Operator** (Operator):
The next question comes from the line of Brent Thill with Jefferies.

**Brent Thill** (Analysts):
Amy, good to see Azure approaching 50%. You have another line item approaching 50%, and that's your operating margin. I think many ask how can you sustain this level of growth with a 50% in the top and a 50% in the bottom? Maybe you can discuss the operational improvements you continue to put forward to maintain that high level on the bottom line.

**Amy Hood** (Executives):
Thanks, Brent. Let me first say, the best solution here is revenue growth. And so I would say I tend to start and focus there, even though I think many people seem to think I start at the bottom of the P&L and work up. The right answer is you always start at the top of the P&L and work down. And so what we've been focused on, and I think really, it's almost inherent in all of the commentary is we changed segments because we're changing how we deliver products and services to customers. We're changing it because we're delivering new and different products with a lot, a lot of value in them. And those products are far more integrated than they were before.
I think when you see that revenue accelerate at the top line, of course, it does, in a pretty healthy way, contribute to positive margin. And part of the positive margin dollars, which I think I need people to also focus on.
The second piece is this real focus on efficiency because efficiency, when we say the word, I think people believe it's cost related. The outcome is cost related. But the real benefit of efficiency is stability, it's security, it's reliability, is that it delivers the highest quality unit at the lowest possible cost. And so it's operational excellence. And so I think when you think about you can deliver product excellence, which is what we're really focused on, I think we did a very good job on product quality in the past quarter, which I think team should be proud of in lots of places. I think then you have this sort of operational focus on improvement. And then it is a real focus in terms of operating expense to make sure it's going towards building the new thing or providing security and quality. And I think that's -- we've made, I think, a very active choice to be really focused on those 2 things, especially in this environment and how important it is.
And I think when you do those things and you happen to be in a good market with breadth and breadth in customers and a global business, we've seen a good result. This quarter, in particular, when you're delivering a lot of efficiency gains in a quarter and you can deliver revenue growth without spending additional costs, you, of course, see a benefit, which we did. But I feel good about what's behind that number, which is, I think, a focus on the right levers.

**Operator** (Operator):
Our next question comes from the line of Brad Reback with Stifel.

**Brad Reback** (Analysts):
Great. Sorry about that. I did not hear my name. On M365 consumption, when you all shifted GitHub from a per-seat model to a consumption model, it unlocked a ton of revenue growth for you all. As you think about the tools in place now unlocked on the consumption side for the core M365 customer, do you think the unlocks as fast and without sales effort? Or is it going to take a fair amount of effort to get those meters spinning?

**Satya Nadella** (Executives):
Yes. Thanks for the question. I think on the coding side, it will be faster just because I think people are used to paying on this PayGo as the sort of the general market and how it works. And if anything, hopefully, some of the things that we announced even at GitHub Universe today with Fusion are a more attractive way, right? Because you even -- if you think about it, right, you buy a bunch of credits and you want to use those credits most efficiently. That's the promise of GitHub Copilot Fusion. So we are very optimistic about making progress on that.
And then when it comes to Copilot itself, right, we are trying to make sure that we, in some sense, are driving more and more value into the subscription with every model drop and essentially consolidating the frontier gains for broad deployment. And in many instances, as my remarks said, IT funds this, right? That's the thing that you want to have standard issue across the board. And at the same time, you have your Pay-As-You-Go or consumption meters for places where you need it. And so both of those options are open. And I think that's why the -- in the Copilot, as Amy referenced, which is we are trying to make sure that customers understand both options. They're able to use the 2 options in the optimal way that benefits them. We don't want them to overbuy one thing and then feel like they're token maxing because that doesn't serve anybody's purpose. We want to make sure that they understand the value of the subscription and how it's a continually improving value. It's not even static. And at the same time, you can exercise this consumption meter. And so that's a little bit of the degree of sophistication in both in our sales motions, even customers' understanding that's, I think, coming together. We feel very good about the progress, but a lot more to do.

**Amy Hood** (Executives):
And I think I would say it's also why we've made the investment into the frontier company here, coupled with changes in our sales motion, which I talked a little bit about. We need both of those things to make sure customers are -- because what I think Satya is saying, we want them to utilize both the Copilot license to its fullest and understand when the consumption meter is delivering value to them. The investment in the FDE organization or the Frontier Co., as well as new motions within our modern work and Microsoft 365 sales teams are both meant to do that. And I think to Satya's point, it will be a slower move outside of coding. But I also still think we're still seeing encouraging signs, and I feel positive about that.

**Jonathan Neilson** (Executives):
Operator, we have time for one last question.

**Operator** (Operator):
The next question will come from the line of Tal Liani with Bank of America.

**Tal Liani** (Analysts):
Just a clarification on something you just said. Did you disclose the Copilot numbers this quarter? But my question is more about the capital commitment or the capital strategy. You said in the prepared remarks that you will approach raising capital if need be in the future. Can you discuss your strategy around it between debt and equity and other sources? How do you intend to raise capital if need be?

**Amy Hood** (Executives):
Great. I'll take that. Look, I think what I said is that if it's attractive and makes sense, we're lucky. We have a lot of flexibility in terms of our capacity to raise financing. I've talked about this before. There's a form of financing called leasing, and we've been using that one as a vehicle. There's also -- we're fortunate to have access in the debt markets given that where our ratings are and sort of we haven't been able to -- we haven't yet, I would say, tapped that. And then, of course, there's other options. But I think the way I see it is we're feeling good that we're free cash flow positive. We feel good that the return on every dollar of CapEx we're spending, we're confident in that. And therefore, we feel like we have lots of options to be able to tap the financing markets when they make sense and they're attractive. And we did not disclose to answer your direct question, an update on the Copilot number this quarter. We talked about momentum in revenue and usage.

**Jonathan Neilson** (Executives):
Thanks, Tal. That wraps up the Q&A portion of today's earnings call. Thank you for joining us today, and we look forward to speaking with all of you soon.

**Satya Nadella** (Executives):
Thank you all.

**Operator** (Operator):
Thank you. This concludes today's conference. You may disconnect your lines at this time, and we thank you for your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MSFT_Q4_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：FY27 全公司營收與營業利益預期維持雙位數成長（原話："double-digit revenue and operating income growth."）
- 2026-07-29｜CFO｜margin：FY27 全年營業利益率預期下降不到 1 個百分點（原話："full fiscal year operating margins should be down less than"）
- 2026-07-29｜CFO｜guidance：FY27 預期維持自由現金流為正（原話："we expect to remain free cash flow positive in FY '27."）
- 2026-07-29｜CFO｜guidance：FY27 資本支出預期年增（原話："we expect FY '27 capital expenditures will grow"）
- 2026-07-29｜CFO｜guidance：FY27 營業費用成長預期為中到高個位數（原話："Operating expenses should grow in the mid- to high single"）
- 2026-07-29｜CFO｜guidance：2026 曆年 CapEx 預期除租賃重分類外不變（原話："our calendar year 2026 CapEx investment expectations remain"）
- 2026-07-29｜CFO｜guidance：租賃由融資轉營業後，曆年 CapEx 預期調整至約 1750 億美元（原話："finance to operating leases adjust our expectation to"）
- 2026-07-29｜CFO｜guidance：FY27 Q1 CapEx 預期（含租賃重分類影響）（原話："We expect CapEx spend will be over $50 billion"）
- 2026-07-29｜CFO｜guidance：FY27 Q1 Azure 固定匯率成長預期約 45%（原話："In Azure, we expect revenue growth of approximately 45% in"）
- 2026-07-29｜CFO｜guidance：上半年成長預期加速（原話："Even with the strong close to Q4, we continue to expect H1"）
- 2026-07-29｜CFO｜guidance：FY27 Q1 全公司營收區間（原話："between USD 89.85 billion and USD 90.95 billion or growth"）
- 2026-07-29｜CFO｜margin：Q1 COGS 成長預期（原話："We expect COGS of USD 29.6 billion to USD 29.8 billion or"）
- 2026-07-29｜CFO｜margin：Q1 營業利益率預期年持平（原話："Operating margins should be relatively flat year-over-year."）
- 2026-07-29｜CFO｜margin：Q1 Microsoft Cloud 毛利率預期季持平（原話："Microsoft Cloud gross margin percentage should be"）
- 2026-07-29｜CFO｜margin：本季公司毛利率 67%，年減，管理層歸因於 Azure 組合與 AI 基建投資（原話："Company gross margin percentage was 67%, down year-over-year"）
- 2026-07-29｜CFO｜margin：本季 CapEx 含元件漲價影響（原話："including the impact from higher component pricing"）
- 2026-07-29｜CFO｜margin：資料中心與辦公大樓估計耐用年限由 15 年延至 25 年（原話："of our data centers and office buildings from 15 to 25 years"）
- 2026-07-29｜CFO｜margin：本季一次性項目對 EPS 的影響（原話："resulting in a benefit of $0.27 on diluted earnings"）
- 2026-07-29｜CFO｜capital_allocation：本季約 2/3 CapEx 為短期資產（原話："Roughly 2/3 of our CapEx was for short-lived assets"）
- 2026-07-29｜CFO｜capital_allocation：本季股利與買回金額（原話："we returned $10.2 billion to shareholders through dividends"）
- 2026-07-29｜CFO｜capital_allocation：本季自由現金流（原話："And free cash flow was $19.6 billion,"）
- 2026-07-29｜CFO｜customer：RPO 成長剔除 OpenAI 後數字（原話："RPO increased 25% when excluding OpenAI."）
- 2026-07-29｜CFO｜customer：全年雲端營收來自 frontier 模型公司以外客戶的占比（原話："with nearly 90% from customers outside of frontier model"）
- 2026-07-29｜CFO｜customer：商業預訂剔除 OpenAI 成長 18%（原話："Commercial bookings grew 18% when excluding the impact from"）
- 2026-07-29｜CEO｜customer：EY 部署 E7 為最大單（原話："EY deployed E7 to 400,000 employees in our largest win to"）
- 2026-07-29｜CEO｜customer：HSBC 承諾 200,000 席 Copilot（原話："HSBC committed to 200,000 seats"）
- 2026-07-29｜CFO｜risk：需求超過可用容量（原話："Customer demand continues to exceed available capacity."）
- 2026-07-29｜CFO｜risk：現貨市場定價作為供需失衡訊號（原話："pricing that's occurring in the spot market for"）
- 2026-07-29｜CFO｜risk：Dynamics CRM 銷售週期拉長、ERP 預訂健康（原話："Bookings growth in ERP remains healthy, while CRM continued"）
- 2026-07-29｜CFO｜guidance：Windows OEM 與 Devices FY27 全年營收預期高十位數衰退（原話："we expect revenue to decline in the high teens for the"）
- 2026-07-29｜CFO｜guidance：Q1 Windows OEM 與 Devices 營收預期降低 20 幾%（原話："Windows OEM and Devices revenue should decline in the low"）
- 2026-07-29｜CFO｜risk：MPC 結果區間較正常寬（原話："the range of potential outcomes remains wider than normal."）
- 2026-07-29｜CFO｜guidance：M365 Commercial cloud 全年成長預期加速（原話："we expect to see acceleration in M365 Commercial cloud"）
- 2026-07-29｜CFO｜product：付費 M365 Copilot 席次超過 3,000 萬（原話："with paid seats now over 30 million."）
- 2026-07-29｜CEO｜product：商業模式由每席擴展為每席加用量（原話："we are also evolving our business model beyond per seat to"）
- 2026-07-29｜CEO｜product：GitHub Copilot 營收季增加速（原話："Copilot revenue accelerated over 60%"）
- 2026-07-29｜CEO｜competition：模型目錄廣度定位（原話："We offer the broadest model catalog in the cloud"）
- 2026-07-29｜CEO｜competition：架構主張：harness 與模型分離，模型可替換（原話："you've got to keep your harness separate from the model."）
- 2026-07-29｜CEO｜commitment：Xbox 預期 FY27 回到成長（原話："expect to return the business to growth in fiscal 2027."）
- 2026-07-29｜CEO｜commitment：容量預計兩年內約翻倍（原話："remain on track to roughly double our overall capacity in"）
- 2026-07-29｜CFO｜capital_allocation：Amy 談需求變動時 CapEx 彈性（原話："And so if the demand environment changes, you just slow down"）
- 2026-07-29｜CFO｜capital_allocation：Amy 談 ROI 計算方式在過去一年的變化（原話："quite frankly, my math has changed in terms of how I do it"）

### 問答異常語氣（迴避／改口／保留）
- MSFT_Q4_2026_Earnings_Call_20260729.md｜問：Gabriela Borges（Goldman Sachs）問今天 CapEx 決策的 ROI 與一年前相比如何｜答法：Amy Hood 未給 ROI 數字或與去年的比較，改談 TAM 擴張信心、毛利槓桿與矽、模型多元化等效率項目
- MSFT_Q4_2026_Earnings_Call_20260729.md｜問：Mark Moerdler（Bernstein）問若出現產能過剩如何自保、元件漲價如何不傷毛利或不大幅漲價｜答法：Amy Hood 以短期資產可放緩、客戶組合分散、新合約反映定價作答，未給元件漲價對毛利的量化影響
- MSFT_Q4_2026_Earnings_Call_20260729.md｜問：Karl Keirstead（UBS）問開源與自訂模型的實質貢獻幅度，以及在 frontier 實驗室曝險下 Microsoft 如何受益｜答法：Satya Nadella 談企業自建學習系統與 harness 架構，未量化開源/自訂模型的營收貢獻；Amy Hood 補充基礎設施可替代

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
{"date":"20260730","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Azure 維持 30%+ 成長，且 Copilot／企業代理由席位制走向「席位＋用量」後持續放量變現，雲＋AI 是結構性長跑道"},{"id":"H2","text":"FY26-FY28 的巨額 AI 資本支出最終轉為可衡量的報酬（雲／AI 變現上升、增量資本報酬率高於資金成本），而非永久的自由現金流黑洞、亦非折舊錯配掩蓋的假獲利"},{"id":"H3","text":"市場對資本支出的恐慌折價（Fwd P/E 20.4x vs 五年中位約 28.5x、分位約 13%）隨報酬能見度回升而部分修復"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"元件成本通膨傳導至雲毛利（本次新增）：CY2026 資本支出中約 $25B 直接歸因於元件價格上漲；記憶體占超大規模業者資本支出的比重由 2023 年約 8% 升至 2026 年約 30%，2027 年可能逼近 48%。DRAM 合約價在 2026 年可能翻倍。這筆成本先進資產、再由折舊分年吃進毛利。Q4 FY26 公司毛利率 67%、Microsoft Cloud 毛利率 65%，皆已 YoY 下滑。"},{"id":"R2","text":"折舊爬坡吞噬營運槓桿與自由現金流：D&amp;A 由 FY25 $34.2B 升至 FY26 約 $46B（＋52.7%），FY28 前將續升。自由現金流／淨利已達 0.50。若營收成長無法在折舊全額落地前追上，營業利益率與自由現金流會同時轉向。"},{"id":"R3","text":"前沿模型實驗室的運算採購結構性繞開 Azure ＋ 應用層價格戰：OpenAI 2026-04 結束 Azure 獨家（Microsoft 保留 IP 非獨家授權至 2032、營收分成至 2030 且設上限），新增巨額算力承諾落在 AWS 與 Oracle；Anthropic 的主要新增算力落在 AWS 與 Google。應用層則有 Google 把 Gemini 免費綑綁進 Workspace（Gemini Enterprise 每席 $21 vs Copilot $30 ＋ M365 底座）。"},{"id":"R4","text":"反壟斷監管（已升級，非假設）：FTC 對 Microsoft 的調查被外部媒體定性為「1990 年代以來對 Microsoft 最廣泛的反壟斷調查」，已向對手發出逾 70 份傳票，焦點正是 Azure Hybrid Benefit 授權折扣、身分管理與資安服務的深度整合是否構成綁定。歐盟《雲端與 AI 發展法》引入主權風險評分，歐洲主權雲 IaaS 支出預估由 2025 年 $6.9B 增至 2027 年約 $23.1B。此風險直接命中 §7 論證定價權的機制本身。資訊缺口：本案自 2026-02 以來檢索不到公開進展更新，狀態已 5 個月未刷新。"},{"id":"R5","text":"證券集體訴訟（已發生）：2026-06-12 提起，類別期間 2025-05-01 至 2026-01-28，被告含 Nadella、Hood 及兩位事業群主管，指控就 Copilot 採用與 Azure 整合的實際狀況作出重大不實陳述；訴狀並指 CEO 於類別期間以 &gt;$500 價位賣出逾 $7,500 萬股票。首席原告申請期限 2026-08-11。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已進場；加碼觸發＝FY27 任兩季 FCF/淨利 ≥0.6，或股價回檔 $365 以下且 Azure cc ≥35%","irr_base_pct":11.2,"ev5y_pct":61.9,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":5.8,"ev5y_pct":61.9,"irr_base_pct":11.2,"max_dd_pct":-50.0,"bull_5y_price":912.0,"bear_5y_price":286.0,"p_bull_pct":25.0,"p_bear_pct":28.0,"rearm_trigger":"已進場；加碼觸發＝FY27 任兩季 FCF/淨利 ≥0.6，或股價回檔 $365 以下且 Azure cc ≥35%","price_at_dd":390.54,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSFT_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
