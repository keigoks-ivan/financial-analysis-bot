你是 stock-analyst **v20 判斷 agent**，標的 FSLR（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"FSLR","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_net_sales","label":"營收（GAAP net sales）","value":1056.2,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","citation":"公司新聞稿 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/1274494/000127449426000169/ex991pressreleaseq2-2026.htm"},"note":"consensus 約 $1,061M（多家彙整站稱『大致符合／小幅未達』，來源：web_search，非公司原文）"},{"id":"f_kpi1_non_gaap_adjusted_ebitda","label":"Non-GAAP 獲利指標（Adjusted EBITDA；公司本季未單獨揭露 non-GAAP operating income）","value":643.6,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","unit":"US$M；margin 61%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","citation":"公司新聞稿 SEC 8-K Ex.99.1（同上）"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／營業利益率","value":450.4,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","unit":"US$M；margin 42.6%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","citation":"公司新聞稿 SEC 8-K Ex.99.1（同上）"}},{"id":"f_kpi5_fy2026_guidance_q2","label":"FY2026 全年 guidance（隨Q2財報重申，區間未變動）","value":"Net sales $4.9B–$5.2B；Gross profit $2.4B–$2.6B；Opex $610M–$635M；Adjusted EBITDA $2.6B–$2.8B；Capex $0.8B–$1.0B；年底Net cash $1.7B–$2.3B；另單獨給Q3單季 Adjusted EBITDA guide $625M–$775M","period":"公告於 2026-07-30，隨Q2財報重申（非新發guidance，與Q1財報所發一致）","unit":"US$（詳見value欄各分項）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"公告於 2026-07-30，隨Q2財報重申（非新發guidance，與Q1財報所發一致）","citation":"公司新聞稿 SEC 8-K Ex.99.1（同上）"},"note":"營收guidance中值≈$5.05B，市場彙整站稱略低於 street consensus $5.08B（來源：web_search，非公司原文）"},{"id":"f_kpi6_contracted_sales_backlog","label":"Contracted sales backlog（硬體／設備 archetype 追加項）","value":45.1,"period":"截至 2026-06-30，公告於 2026-07-30","unit":"GW；對應合約總值 $13.6B（不含技術調整項），交貨期至2030年","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"截至 2026-06-30，公告於 2026-07-30","citation":"公司新聞稿 SEC 8-K Ex.99.1（同上）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_fslr_gross_margin_pct","label":"FSLR 毛利率","value":49.25,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FSLR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_fslr_operating_margin_pct","label":"FSLR 營業利益率","value":37.69,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FSLR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_fslr_fcf_margin_pct","label":"FSLR FCF 利潤率","value":4.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FSLR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_csiq_gross_margin_pct","label":"CSIQ 毛利率","value":16.43,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSIQ.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_csiq_operating_margin_pct","label":"CSIQ 營業利益率","value":-0.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSIQ.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_csiq_fcf_margin_pct","label":"CSIQ FCF 利潤率","value":-31.42,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSIQ.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_jks_gross_margin_pct","label":"JKS 毛利率","value":4.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JKS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_jks_operating_margin_pct","label":"JKS 營業利益率","value":-6.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JKS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_enph_gross_margin_pct","label":"ENPH 毛利率","value":45.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ENPH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_enph_operating_margin_pct","label":"ENPH 營業利益率","value":4.53,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ENPH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_enph_fcf_margin_pct","label":"ENPH FCF 利潤率","value":11.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ENPH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF＝營運現金流－資本支出）","value":-306.2,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","unit":"US$M；margin -29.0%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","citation":"公司新聞稿現金流量表僅列 Six Months Ended 欄位，Q2 單季由 H1（營運現金流 -$359.8M／資本支出 -$279.8M）減去 Q1 press release 對應數字（-$214.9M／-$118.5M）反推，非公司原文直接揭露"}},{"id":"f_kpi4_sbc","label":"SBC 占營業利益（及占營收）%","value":1.56,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","unit":"%（占GAAP營業利益）；另占營收 0.67%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","citation":"公司新聞稿現金流量表 H1 股權薪酬 $13.826M 減 Q1 press release 三個月數字 $6.781M，反推 Q2 單季 SBC ≈$7.045M，非公司原文直接揭露單季數"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":184.21,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-12.86,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":54.47,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（17.48 → 17.48）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.51 → 23.51）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（29.65 → 29.65）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":17.48,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":23.51,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":29.65,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.29,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 17.43 → 17.48（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":10.65,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.95,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.69,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":10.54,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 17.48，分子＝快照價 184.21","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-1299.11,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 324.97、現金 1624.08（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":107.48,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":18499.99,"period":"2026-11-03","unit":"USD m","basis":"市值 19799.1 ＋ 淨負債 -1299.11","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":4822.75,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（32 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":5945.83,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（30 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.84,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 183.14 / W52 222.53 / W104 200.65 / W250 177.33 / W250 13週斜率 0.84%"},{"id":"f_ma_w52","label":"52 週均線","value":222.53,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":200.65,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":177.33,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.84,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"FSLR Q1 2026 淨銷售 10.4 億美元，年增 24%，主因是賣給第三方的模組出貨量增加","source":"SEC 8-K, First Solar Q1 2026 press release","url":"https://www.sec.gov/Archives/edgar/data/0001274494/000127449426000108/ex991pressreleaseq1-2026.htm","excerpt":"Net sales were $1.04 billion for the first quarter of 2026, a 24% increase compared to the first quarter of 2025, driven primarily by an increase in the volume of modules sold to third parties.","as_of":"2026-04-30","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"截至 2026年3月31日，FSLR 合約在手訂單（backlog）47.9 GW","source":"SEC 8-K, First Solar Q1 2026 press release","url":"https://www.sec.gov/Archives/edgar/data/0001274494/000127449426000108/ex991pressreleaseq1-2026.htm","excerpt":"Contracted sales backlog of 47.9 GW as of March 31, 2026","as_of":"2026-03-31","retrieved_at":"2026-09-29","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"2025年全球模組出貨量排名：LONGi 約87GW、Jinko約86GW 並列龍頭，FSLR出貨17.5GW創自身紀錄但僅佔全球約2%市佔率，量能上落後中國廠","source":"TaiyangNews / SolarQuarter，2025全球模組出貨排名報導","url":"https://taiyangnews.info/business/solar-module-shipment-2025-ranking","excerpt":null,"as_of":"2026-03-14","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"儘管出貨量僅為中國四大廠（LONGi/Jinko/JA Solar/Trina）合計的三分之一，FSLR的淨利仍高於這四家合計；差異化來自CdTe薄膜技術不依賴矽料供應鏈、美國本土製造適用45X稅收抵免（2025年認列16億美元）、以及50.1GW/150億美元的在手訂單","source":"SurgePV，Top Solar Companies by Revenue 2026","url":"https://www.surgepv.com/blog/top-solar-companies-by-revenue-2026","excerpt":null,"as_of":"2025-12-31","retrieved_at":"2026-09-29","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Lightsource bp 與 First Solar 簽署4GW模組供貨協議，2026-28年交貨，為雙方繼2021年最高4.3GW協議後第二筆同類合約，顯示既有客戶持續下單、未被競爭對手取代","source":"PV Tech，Lightsource bp and First Solar ink 4GW module supply agreement for 2026-28","url":"https://www.pv-tech.org/lightsource-bp-and-first-solar-ink-4gw-module-supply-agreement-for-2026-28/","excerpt":"Lightsource bp and First Solar have agreed a 4GW module supply deal for US projects to be delivered between 2026-28.","as_of":"2023-02-28","retrieved_at":"2026-09-29","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"同業／風險因子提及：來自矽晶（crystalline silicon）模組廠的激烈競爭可能壓低平均售價與淨銷售；FSLR 也在CdTe配方中加入鈣鈦礦(perovskite)以提升效率，屬對新興技術威脅的回應","source":"綜合搜尋摘要（PV Tech / CleanTechnica 相關報導）","url":null,"excerpt":null,"as_of":"2026-03-13","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K 披露兩家客戶各占 2025 淨銷售 11% 與 10%（未具名）；2024 年無客戶達 10%，2023 年有一家 10%。搜尋未發現最大客戶導入第二供應商或自製的報導。","source":"SEC EDGAR 10-K FY2025 note 22（經搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/1274494/000127449426000021/fslr-20251231.htm","excerpt":null,"as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"Q2 2026 財報電話會議：美國整合產能到 2028 年大致已被承諾","source":"MarketBeat Q2 2026 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/first-solar-q2-earnings-call-highlights-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K names two customers each at/above 10% of modules business net sales: Silicon Ranch Corporation and NextEra Energy.","source":"First Solar, Inc. Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1274494/000127449426000021/fslr-20251231.htm","excerpt":"During 2025, Silicon Ranch Corporation and NextEra Energy each accounted for 10% or more of our modules business net sales.","as_of":"2025-12-31","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"For FY2024, no single customer accounted for 10% or more of First Solar's net sales (an improvement in diversification versus 2023 and 2021).","source":"First Solar, Inc. Form 10-K FY2024 (aggregated search summary, not independently page-verified)","url":"https://www.sec.gov/Archives/edgar/data/1274494/000127449425000010/fslr-20241231.htm","excerpt":null,"as_of":"2024-12-31","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Historical concentration was higher in earlier years: FY2023 Customer #1 = 10%; FY2022 three customers each >=10% (14%, 10%, 10%); FY2021 Customer #1 = 12%, Customer #2 = 10%. Customers are not named in these older filings, only numbered.","source":"First Solar, Inc. Form 10-K FY2021/2022/2023 (aggregated search summary, not independently page-verified)","url":"https://www.sec.gov/Archives/edgar/data/1274494/000127449424000004/fslr-20231231.htm","excerpt":null,"as_of":"2023-12-31","retrieved_at":"2026-09-29","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"2026 US solar bankruptcy wave (100+ companies since 2023, including Freedom Forever Chapter 11 on 2026-04-15) is concentrated in residential/C&I installers; commentary frames First Solar as insulated because it sells utility-scale modules to large developers/utilities rather than to homeowners.","source":"Yahoo Finance / TheStreet: \"One company stands to gain as bankruptcy wave hits solar sector\"","url":"https://finance.yahoo.com/energy/articles/one-company-stands-gain-bankruptcy-033300453.html","excerpt":"Unlike residential solar installers, First Solar does not sell to homeowners and builds large volumes of panels for utility-scale power plants, the kind that feed electricity to the grid.","as_of":"2026-08","retrieved_at":"2026-09-29","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"全球太陽能供應鏈各環節產能相對近期需求嚴重過剩（pv magazine 用「severely overbuilt」形容）","source":"pv magazine USA","url":"https://pv-magazine-usa.com/2026/09/01/oversupply-expanding-tariffs-and-tech-shifts-reshape-u-s-solar-outlook/","excerpt":"Global manufacturing capacity across every segment of the solar value chain remains severely overbuilt relative to near-term demand","as_of":"2026-09-01","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"第三方估算：多晶矽產能約 2,034 GW 對比 2026 年預估裝機 638 GW，模組產能約 1,908 GW，過剩逾 1.2 TW；此為結構性而非暫時性短缺","source":"ICRA / SurgePV 產業分析（經搜尋摘要彙整）","url":null,"excerpt":null,"as_of":"2026-08-28","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"BNEF／pv-tech 觀點：2026 年可能是本輪供應鏈調整的谷底，2027–2029 年成長率可望回升至兩位數（受電動運輸、資料中心、汰舊換新驅動）","source":"pv magazine International / pv-tech The PV Review 2025","url":"https://www.pv-magazine.com/2025/12/23/bnef-flags-potential-global-solar-slowdown-in-2026-as-china-cools/","excerpt":null,"as_of":"2025-12-23","retrieved_at":"2026-09-29","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"中國多晶矽業者 2025 年產量年減 28.4% 至 132 萬噸，價格自 2025 年中低點回升逾 50%（RMB 50–56/kg），為行業自律限產結果；2026 上半年在產產能約 130 萬噸","source":"搜尋摘要彙整（DAQO New Energy 6-K 系列 / 產業報告）","url":null,"excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-09-29","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"中國自 2027-01-01 起實施更嚴格多晶矽單位能耗強制標準（超過 6.3 kgce/kg 須整改或面臨停產），但因高耗能產能多已閒置，對實際供給的立即影響有限","source":"pv magazine Global","url":"https://www.pv-magazine.com/2026/07/24/china-adopts-tougher-mandatory-energy-limits-for-polysilicon-plants/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"2026-09-29","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"First Solar 2026 Q2 季底合約在手訂單（backlog）達 45.1 GW，交付期涵蓋至 2030 年","source":"First Solar Q2 2026 財報摘要（wedoany 轉載）","url":"https://en.wedoany.com/shortnews/435850.html","excerpt":"As of the end of the quarter, First Solar's contracted backlog stood at 45.1 GW, covering through 2030.","as_of":"2026-08-01","retrieved_at":"2026-09-29","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"First Solar 技術調整條款（technology adjusters）在合約中最多可為 2028 年前帶來額外約 6 億美元營收，主要落在 2027–2028 年","source":"First Solar Q1 2026 財報電話會議摘要（Yahoo Finance / Motley Fool）","url":null,"excerpt":null,"as_of":"2026-04-30","retrieved_at":"2026-09-29","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#7","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"產業預估 2026 年全球 PV 模組需求將自 2025 年的 653–706 GWdc 降至 529–624 GWdc，為近十年來首次年度負成長","source":"搜尋摘要彙整（產業預估報告）","url":null,"excerpt":null,"as_of":"2026-04-30","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#8","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"中期展望（2027–2028）：全球太陽能裝機預估年增 10–20%，2028 年中位數估計達 760 GWdc；美國 EIA 預估太陽能發電 2026 年增 17%、2027 年再增 23%，主要受資料中心用電需求帶動","source":"搜尋摘要彙整（EIA / 產業預估）","url":"https://www.utilitydive.com/news/demand-growth-solar-2027-energy-information-administration/811941/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-09-29","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Section 201 進口晶矽太陽能電池／模組安全防護關稅於 2026-02-06 到期，結束長達八年的對低價進口品限制","source":"Beveridge & Diamond (bdlaw.com) - Solar's Momentum At Mid-2026 Will Help It Overcome Snags","url":"https://www.bdlaw.com/publications/solars-momentum-at-mid-2026-will-help-it-overcome-snags/","excerpt":"Most notably, the Section 201 safeguard tariffs on imported crystalline silicon photovoltaic cells and modules expired on Feb. 6, ending an eight-year effort to address low-cost imports that were found to injure U.S. manufacturers.","as_of":"2026-02-06","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"美國川普政府對多晶矽（polysilicon）進口啟動 Section 232 國安調查行動，First Solar 表示此舉有助削弱中國在該供應鏈的掌控，並藉此撤回 USITC 337 條款申訴、轉向聯邦地方法院訴訟追討專利權","source":"Yahoo Finance - First Solar Recalibrates TOPCon IP Enforcement Strategy Following Section 232 Action","url":"https://finance.yahoo.com/energy/articles/first-solar-recalibrates-topcon-ip-000100185.html","excerpt":"The decision follows the Trump Administration's recent national security action on imports of polysilicon and its derivatives under Section 232 of the Trade Expansion Act, a move aimed at loosening China's grip on a critical supply chain. ... The Trump Administration's Section 232 action helps level the playing field at the border, and we are more determined than ever to enforce our IP rights and defend the rule of law here at home.","as_of":"2026-09-16","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"美國於2026年8月6日宣布 Section 232 太陽能關稅：對成品模組設 $0.38/瓦最低進口價、對部分多晶矽衍生品課15%關稅，2026年12月4日生效；First Solar 的 CdTe 模組不含多晶矽，作為最大美國本土模組製造商公開表態支持此措施。","source":"postregister.com — 'First Solar Applauds Comprehensive Section 232 Action on Polysilicon and Derivatives'; oilprice.com — 'Solar Stocks Up 40% YTD as Section 232 Tariff Decision Looms'","url":"https://www.postregister.com/businessreport/government/first-solar-applauds-comprehensive-section-232-action-on-polysilicon-and-derivatives/article_71bfa321-364b-550c-aa94-9e008938381b.html","excerpt":null,"as_of":"2026-08-06","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"中國自2025年2月起收緊含碲（tellurium）等五項關鍵礦物的出口管制，出口商須向中國商務部申請許可；碲是 First Solar CdTe 模組的主要原料之一，中國佔2024年全球精煉碲產量約76.53%。First Solar 10-K/10-Q 揭露已組建跨部門小組監控此風險、申請出口許可並尋求替代供應商。","source":"pv-magazine-india.com — 'China adds export restrictions for minerals used in thin-film solar'; First Solar SEC filings (10-K/10-Q risk factors, 搜尋摘要)","url":"https://www.pv-magazine-india.com/2025/02/11/china-adds-export-restrictions-for-minerals-used-in-thin-film-solar/","excerpt":null,"as_of":"2025-02-11","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"2026年2月20日美國最高法院裁定2025年依 IEEPA 對中國進口加徵的10%關稅違法，川普隨即撤銷該關稅並以 Section 122 全球關稅取代；First Solar 已申請 IEEPA 關稅退款，並於截至2026年6月30日止季度開始收到部分退款款項。","source":"FIRST SOLAR, INC. Form 10-Q for the quarterly period ended June 30, 2026 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0001274494/000127449426000170/fslr-20260630.htm","excerpt":"In February 2026, the U.S. Supreme Court ruled the IEEPA tariffs unlawful.","as_of":"2026-02-20","retrieved_at":"2026-09-29","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"First Solar 用 CdTe 薄膜技術，不吃矽晶圓/多晶矽那條由中國主導的供應鏈，因此較不受中國關聯的關稅與地緣風險影響","source":"pv magazine USA - Solar Manufacturing USA 2026","url":"https://pv-magazine-usa.com/2026/04/30/solar-manufacturing-usa-2026-production-and-technology-at-the-heart-of-u-s-solar/","excerpt":"First Solar's CdTe thin-film technology is independent from the silicon-polysilicon value chain dominated by Chinese manufacturers, which insulates it from geopolitical tensions, tariffs, and logistical risks affecting crystalline silicon competitors.","as_of":"2026-04-30","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"First Solar 的關鍵原料碲(tellurium)是煉銅的副產品，供應量跟著銅需求走;公司只跟少數幾家供應商採購，換供應商要走很長的資格審查，萬一斷供不容易及時補上","source":"First Solar 10-K (FY2015) 風險因子章節","url":"https://www.sec.gov/Archives/edgar/data/0001274494/000127449416000067/fslr10-k12x31x2015.htm","excerpt":"First Solar currently purchases these raw materials from a limited number of suppliers, and because suppliers must undergo a lengthy qualification process, the company may be unable to replace a lost supplier in a timely manner and on commercially reasonable terms.","as_of":"2015-12-31","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"First Solar 產能刻意集中在美國本土(Ohio、Alabama、Louisiana),2026 Q1 美國廠稼動率 96%,出貨 3.8GW,公司稱這樣的本土集中讓自己不受全球地緣風險波動影響","source":"pv magazine USA - Solar Manufacturing USA 2026","url":"https://pv-magazine-usa.com/2026/04/30/solar-manufacturing-usa-2026-production-and-technology-at-the-heart-of-u-s-solar/","excerpt":"This deliberate concentration in Ohio, Alabama, and Louisiana creates a domestic industrial base optimized for serving large utility-scale projects and insulated from global geopolitical volatility.","as_of":"2026-04-30","retrieved_at":"2026-09-29","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"因美國政策不確定性、中國模組流入歐洲、印度關稅政策等近期逆風，First Solar 宣布 2025 年把馬來西亞、越南廠的 Series 6 模組產能下修 1GW,重心轉向美國本土擴產","source":"TaiyangNews","url":"https://taiyangnews.info/business/first-solar-lower-1-gw-malaysia-vietnam-module-output","excerpt":"These items create near-term headwinds for our international production","as_of":"2025-03-05","retrieved_at":"2026-09-29","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"截至 2025 年底前後，美國對越南(20%)、印度(25%)、馬來西亞(19%)課對等關稅;印度另以反傾銷/核准名單機制，大幅堵住中國電池模組借道東南亞轉銷印度的路","source":"SurgePV - Solar Import Duty Rates by Country","url":"https://www.surgepv.com/solar-compliance/global/import-duty-rates","excerpt":"Reciprocal tariff rates apply to Vietnam (20%), India (25%), and Malaysia (19%) as of late 2025. Additionally, India's tariff and non-tariff measures against Chinese cells and modules have largely eliminated the country as a destination from Malaysia and Vietnam product, including India's Basic Customs Duty and the Approved List of Models and Manufacturers.","as_of":"2025-12-31","retrieved_at":"2026-09-29","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"FSLR 2026 全年財測維持：模組出貨量 17.0–18.2 GW、淨銷售額 $4.90–5.20B（Q1'26 財報重申）。","source":"Gurufocus - First Solar (FSLR) Reports Record Q1 2026 Revenue and Strong Outlook","url":"https://www.gurufocus.com/news/8834541/first-solar-fslr-reports-record-q1-2026-revenue-and-strong-outlook","excerpt":"The company reaffirmed its 2026 outlook with expected module volumes of 17.0–18.2 GW and net sales of $4.90–$5.20 billion.","as_of":"2026-04-30","retrieved_at":"2026-09-29","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"美國公共事業級（utility-scale）市場：Q1'26 起累計新簽 1.9 GW，其中 1.4 GW 為美國 utility-scale，均價 $0.35/W；截至 Q1'26 末在手訂單（backlog）47.9 GW，合約總價 $14.4B（不含技術加價），交付排到 2030 年。","source":"First Solar Q1'26 Earnings Presentation / earnings coverage aggregation","url":"https://s202.q4cdn.com/499595574/files/doc_financials/2026/q1/Q1-26-Earnings-Presentation-vf-Secured.pdf","excerpt":"First Solar secured gross bookings of 1.9 gigawatts, with 1.4 gigawatts booked in the US utility scale market at an average selling price of $0.35 per watt. The company maintains a backlog of 47.9 gigawatts valued at $14.4 billion.","as_of":"2026-04-30","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"截至 2026/6/30（Q2'26 末），backlog 降為 45.1 GW、合約總價 $13.6B，交付仍排到 2030 年——較 Q1'26 末的 47.9 GW / $14.4B 略減，屬正常出貨消耗 backlog。","source":"First Solar Q2'26 10-Q / earnings coverage aggregation","url":"https://www.sec.gov/Archives/edgar/data/0001274494/000127449426000170/fslr-20260630.htm","excerpt":"More recently, as of June 30, 2026, the backlog was 45.1 GW valued at $13.6B through 2030.","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"印度市場：Q1'26 新簽 0.8 GW、均價僅 $0.20/W，明顯低於美國 utility-scale 的 $0.35/W，反映印度段定價力較弱、屬較低毛利的地區市場。","source":"First Solar Q1'26 earnings coverage aggregation","url":"https://www.theglobeandmail.com/investing/markets/markets-news/Motley%20Fool/1633246/first-solar-fslr-q1-2026-earnings-transcript/","excerpt":"During Q1 2026, First Solar achieved gross bookings of 1.7 GW during the quarter (0.9 GW U.S. at $0.34/watt average; 0.8 GW India at $0.20/watt average)","as_of":"2026-04-30","retrieved_at":"2026-09-29","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"CURE 技術加價（technology adjuster）預計 2028 年前複製到 Series 6/7 全系列產能，若達成可為 backlog 帶來最多 $600M 額外營收，主要落在 2027–2028 年。","source":"First Solar Q1'26 earnings coverage aggregation","url":"https://www.fool.com/earnings/call-transcripts/2026/04/30/first-solar-fslr-q1-2026-earnings-transcript/","excerpt":"CURE technology is scheduled to be replicated across the Series 6 and 7 fleet through 2028, which, if achieved, supports the potential realization of up to $600 million of additional revenue from technology adjusters in the backlog, with the majority anticipated in 2027 and 2028.","as_of":"2026-04-30","retrieved_at":"2026-09-29","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"美國 utility-scale 太陽能終端需求：2026 年美國公共事業級太陽能發電量預期較 2025 年成長（290 BkWh → 2027 年 424 BkWh），2026 年計劃新增 43.4 GW 公共事業級容量，較前一年增加 60%；本地含量合規模組供給短缺預期至少延續到 2027 年。","source":"EIA - Today in Energy","url":"https://www.eia.gov/todayinenergy/detail.php?id=67205","excerpt":"Utility-scale solar is the fastest-growing source of electricity generation in the United States, increasing from 290 BkWh in 2025 to 424 BkWh by 2027... developers plan to add 43.4 GW of new utility-scale solar capacity in 2026, a 60% increase in capacity additions from last year if realized. Demand for Domestic Content–eligible modules will continue to outstrip available compliant supply through at least 2027.","as_of":"2026-01-01","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"美國本土模組製造產能 2025 年底達 65.5 GW，較 2024 年底 42.5 GW 成長逾 50%，但 Section 232 關稅預期推升美國模組價格至 2027 年（因本土電池片產能多數要到 2026 年底才有意義放量）。","source":"Intertek CEA / SolarStock USA market brief aggregation","url":"https://www.solarstockusa.com/research/market-brief-2026-q2","excerpt":"Intertek CEA forecasts rising U.S. module prices through 2027, driven by potential Section 232 tariffs on polysilicon and constrained domestic cell supply, with most planned U.S. cell factories not expected to ramp meaningfully until late 2026. U.S. domestic solar module manufacturing capacity reached 65.5 GW at the end of 2025, up more than 50% from 42.5 GW at the end of 2024.","as_of":"2026-01-01","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"-","claim":"全球（非 FSLR 所在的關稅保護利基）結晶矽模組市場：2026 年預估為十餘年來全球 PV 需求首次負成長（529–624 GWdc），全球產能逾 1,100 GW 對僅約 650 GW 裝機需求，模組價格崩至約 $0.10/W，遠低於 TOPCon 約 $0.16/W 的生產成本；此為中國結晶矽產能過剩導致，與 FSLR 受美國關稅/本土含量保護的薄膜（CdTe）利基市場性質不同。","source":"InfoLink Consulting / pv magazine aggregation","url":"https://www.infolink-group.com/energy-article/solar-topic-solar-pv-supply-chain-marks-industry-trough-the-beginning-restructuring","excerpt":"2026 is projected to mark the first year of negative growth in global PV demand in over a decade, with module demand forecast to decline to 529–624 GWdc... Global module manufacturing capacity sits above 1,100 GW against roughly 650 GW of installation demand, and polysilicon spot prices have fallen 84% from the 2022 peak... global module prices collapsed to approximately USD 0.10 per watt, a figure that severely undercuts the actual production costs of even the most advanced TOPCon manufacturing lines, which hover around USD 0.16 per watt.","as_of":"2026-01-12","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#8","axis":"end_markets","section":"coverage","direction":"0","claim":"FSLR 為全球最大薄膜（CdTe）太陽能模組製造商，佔全球薄膜技術市場約 45%；薄膜技術在印度 2026 年 ALMM 掛牌模組製造產能中僅佔約 2%，印度年產模組中薄膜約估 8–12%。","source":"Statista / IndexBox aggregation","url":"https://www.statista.com/topics/2737/first-solar/","excerpt":"First Solar is the world's largest thin film PV solar module manufacturer, and the company accounts for roughly 45 percent of the market for this solar technology globally... thin-film technology represented 2% of ALMM-listed module manufacturing capacity as of June 2026.","as_of":"2026-06-01","retrieved_at":"2026-09-29","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"矽晶太陽能效率持續提升、成本下降，可能使 CdTe 與矽晶的效率差距擴大到租稅抵減也難以彌補的程度","source":"FinancialContent - The American Solar Champion: An In-Depth Research Feature on First Solar (FSLR)","url":"https://markets.financialcontent.com/stocks/article/finterra-2026-4-15-the-american-solar-champion-an-in-depth-research-feature-on-first-solar-fslr","excerpt":"If crystalline silicon efficiency continues to climb while costs fall, the \"gap\" between CdTe and silicon might become too wide for tax credits to bridge.","as_of":"2026-04-15","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"First Solar 正開發 CdTe-Perovskite 疊層電池，目標突破 25% 效率門檻；若試產成功，市場可能重新評價其為技術領先者而非單純製造商","source":"FinancialContent - The American Solar Champion: An In-Depth Research Feature on First Solar (FSLR)","url":"https://markets.financialcontent.com/stocks/article/finterra-2026-4-15-the-american-solar-champion-an-in-depth-research-feature-on-first-solar-fslr","excerpt":"By layering its traditional CdTe with a material called Perovskite, the company aims to break the 25% efficiency barrier. Any successful pilot of the CdTe-Perovskite tandem cell could trigger a re-rating of the stock as a technology leader, not just a manufacturing play.","as_of":"2026-04-15","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"First Solar 官方技術頁預告 CdTe 電池效率目標為 2025 年前達 25%、2030 年前達 28%，並規劃結合 CdTe 與 c-Si（結晶矽）半導體技術優點的疊層產品","source":"First Solar - Our Technology (CdTe)","url":"https://www.firstsolar.com/en/Technology/CadTel","excerpt":"forecast a thin film CdTe entitlement of 25% cell efficiency by 2025 and pathways to 28% cell efficiency by 2030; development of CdTe bifacial modules and tandem products that incorporate the best aspects of both CdTe and c-Si semiconductor technologies","as_of":"2026","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q3 2026 10-Q：第三方客戶為系統開發商、IPP、公用事業、C&I及大型企業買家，無住宅/消費者通路；Q3營收年減22.8%主因第三方模組量下滑及客戶合約終止","source":"First Solar Form 10-Q (quarter ended 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001274494/000127449426000212/fslr-20260930.htm","excerpt":"Third-party customers of this segment include system developers, independent power producers, utilities, commercial and industrial companies, large corporate energy buyers, and other system owners and operators.","as_of":"2026-10-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026-10-29 Q3 財報下修全年 2026 guidance：出貨量 16.0–17.0GW（原 17.0–18.2GW）、淨銷售 $4.6–4.9B（原 $4.9–5.2B）、調整後 EBITDA $2.55–2.75B（原 $2.6–2.8B）、資本支出 $0.6–0.8B（原 $0.8–1.0B）；新聞稿未明說下修原因，並稱展望假設現行美國政策環境持續","source":"First Solar 8-K Ex.99.1 Q3 2026 press release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001274494/000127449426000211/ex991pressreleaseq3-2026.htm","excerpt":"Our outlook assumes the current U.S. policy environment persists","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026 初始 guidance 營收 $4.9–5.2B 遠低於約 $6.16B 共識，多家券商降評/降目標價","source":"Finviz: First Solar 2026 Guidance Disappoints Wall Street Firms, Triggers Downgrades","url":"https://finviz.com/news/331782/first-solar-inc-fslr-2026-guidance-disappoints-wall-street-firms-triggers-downgrades","excerpt":"(FSLR) 2026 Guidance Disappoints Wall Street Firms, Triggers Downgrades By Abdul Rahman | March 06, 2026, 1:50 AM FSLR +5.07% First Solar Inc First Solar, Inc. (NASDAQ:FSLR) is one of the best solar stocks to buy now. First Solar (NASDAQ:FSLR) has a consensus rating of Moderate Buy from 24 analysts.","as_of":"2026-03-01","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Morgan Stanley 下修 2026 出貨預估至 17.6GW（原 19.7GW）、ASP 至 $0.287/W（原 $0.315）","source":"Yahoo Finance: Why Morgan Stanley Cut First Solar's Target as Pricing Recovery Slows","url":"https://finance.yahoo.com/news/why-morgan-stanley-cut-first-162903998.html","excerpt":"Public summaries of the note also said Morgan Stanley lowered its 2026 shipment forecast to 17.6 gigawatts from 19.7 gigawatts and reduced its 2026 average selling price estimate to $0.287 per watt from $0.315.","as_of":"2026-03-10","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-08 分析師目標價中位 $260，22 buy/12 hold/2 sell；7/31 多家下修 PT","source":"Walnut: First Solar FSLR Stock Forecast and Price Target","url":"https://walnutinvest.com/stocks/fslr/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2025-02 起 First Solar 在德拉瓦聯邦地方法院控告 JinkoSolar 的 TOPCon 產品侵犯其專利；PTAB 於 2025-11-20 駁回 Jinko 的 IPR 申請，Jinko 另於 2025-12-15 申請 ex parte 再審。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1274494/000127449426000021/fslr-20251231.htm","excerpt":"On November 20, 2025, the U.S. Patent Trial and Appeal Board declined the petition, ending the proceeding.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2025-09 First Solar 在紐約州最高法院控告 BP Solar Holding 及 Lightsource 違約，要求支付 3.236 億美元及其他已交付模組應收款。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1274494/000127449426000021/fslr-20251231.htm","excerpt":"in September 2025, First Solar filed a complaint in the Supreme Court of the State of New York asserting that BP Solar Holding LLC and its affiliate Lightsource Renewable Energy Trading, LLC (together, the “Defendants”) breached their contractual obligations with First Solar and demanding payment from the Defendants of $323.6 million","as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共6份，含重大項目者2份：2026-02-19 的 1.01/1.02/2.03（15 億美元循環信貸）與 2026-10-29 的 8.01（5 億美元庫藏股授權）；無 2.01（併購完成）、4.02（財報不可信賴）項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001274494&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2026年有針對 FSLR 的證券集體訴訟（Day v. First Solar，EDNY），集體期間 2025-02-26 至 2026-02-24，指控淡化關稅影響；原告律所公告，指控未經證實。","source":"Levi & Korsinsky 公告（natlawreview）","url":"https://natlawreview.com/press-releases/first-solar-inc-fslr-lawsuit-investors-urged-contact-levi-korsinsky-august-0","excerpt":null,"as_of":"2026-06-24","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"全球太陽能模組產能在2025年已達約800GW，遠超過同年約450GW的新增裝機量，供過於求局面延續","source":"TheEnergyBrief - PV Module Manufacturers' New Reality 2026","url":"https://www.theenergybrief.org/en/articles/global-solar-pv-module-manufacturing-new-reality-2026","excerpt":"total global PV module capacity reached approximately 800 GW in 2025, while global new installations that year were only about 450 GW","as_of":"2026-07-19","retrieved_at":"2026-09-29","affects":["thesis.bear","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"中國龍頭LONGi與Jinko仍持續擴大電池產能，LONGi的HPBC電池產能預計2026年底達50GW、Jinko的N型TOPCon產能超過60GW，顯示同業並未收縮新產能","source":"TheEnergyBrief - PV Module Manufacturers' New Reality 2026","url":"https://www.theenergybrief.org/en/articles/global-solar-pv-module-manufacturing-new-reality-2026","excerpt":"LONGi Green Energy's HPBC cell capacity expected to reach 50 GW by the end of 2026, and Jinko's N-type TOPCon capacity exceeding 60 GW","as_of":"2026-07-19","retrieved_at":"2026-09-29","affects":["moat_trend"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"中國多晶矽廠商推動協調性「自律」減產與整合，加上出口退稅取消，帶動模組價格在2025Q4至2026H1轉為上漲，顯示部分供給紀律正在形成","source":"搜尋摘要（surgepv／pv-magazine-india 2026年太陽能供應鏈報導）","url":null,"excerpt":"Module prices increased in Q4 2025 and continued to face upward pressure in H1 2026, driven by a combination of Chinese supply-side rationalization, production discipline, consolidation in the polysilicon sector, and the removal of China's photovoltaic export tax rebate.","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"美國同業Qcells在喬治亞州Cartersville廠已開始生產矽晶太陽能電池，3.5GW電池線預計2026年第三季達全產能，屬美國本土新增產能","source":"Solar Power World Online","url":"https://www.solarpowerworldonline.com/2026/06/qcells-starts-production-of-solar-cells-in-united-states/","excerpt":"Qcells has begun manufacturing silicon solar cells at its integrated factory in Cartersville, Georgia, and expects to reach full production of the 3.5-GW cell line by Q3 2026","as_of":"2026-06","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.bear","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"美國同業T1 Energy 2026年模組產量預計3.1-4.2GW（2025年為2.79GW），德州Milam County的2.1GW電池廠第一期預計2026年第四季開始投產，屬未來12-24個月內的新增美國本土產能","source":"pv magazine USA","url":"https://pv-magazine-usa.com/2026/05/14/how-t1-energy-is-ramping-up-multi-gigawatt-u-s-solar-manufacturing/","excerpt":"We produced 2.79 GW of modules in 2025. We expect to manufacture between 3.1 and 4.2GW of modules this year... Phase 1 will be a 2.1-gigawatt fab...we remain on track to begin cell production in the fourth quarter of 2026.","as_of":"2026-05-14","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.bear","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"中國太陽能電池庫存持續下降，產業重心轉向需求復甦與庫存去化，但模組價格在 8 月兩輪調漲後又回落","source":"EnergyTrend","url":"https://www.energytrend.com/pricequotes/20260724-51816.html","excerpt":"Cell Production Cuts Begin to Take Effect; Market Focus Shifts to Market Demand Recovery and Inventory Destocking","as_of":"2026-07-24","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"美國模組價格因反傾銷/反補貼稅及 FEOC（受關注外國實體）規定收緊，2026 Q1 中位價來到 $0.28/W，較 2025 年初 $0.25/W 上升；PERC 模組價格 2025/11–2026/2 上漲 20%","source":"pv magazine USA","url":"https://pv-magazine-usa.com/2026/04/03/u-s-solar-module-prices-face-upward-pressure-as-trade-risks-and-feoc-rules-dominate-q1-2026/","excerpt":"median solar module pricing in the United States reached $0.28 per watt as the market adjusted to intensified trade enforcement and new Foreign Entity of Concern compliance requirements","as_of":"2026-04-03","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"中國 TOPCon 模組出口基準價（CMM）2026 年 6 月底維持在 $0.113/W，Q4 2026 及 2027 年遠期交貨報價因下半年需求預期轉弱而下滑","source":"pv magazine Global","url":"https://www.pv-magazine.com/2026/07/03/china-solar-module-forward-prices-ease-amid-softer-europe-demand/","excerpt":"The Chinese Module Marker (CMM) benchmark assessment for TOPCon modules FOB China held steady at $0.113/W with spot price indications ranging between $0.110/W and $0.117/W in late June 2026","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"First Solar 合約在手訂單（backlog）截至 2026/6/30 降至 45.1GW、約 $13.6B，較 2025 年底的 50.1GW 下降；當季出貨 7.6GW、新增訂單僅 2.8GW，取消訂單多於新單","source":"PV Tech / Investing.com（First Solar Q2 2026 財報）","url":"https://www.pv-tech.org/first-solar-reaffirms-2026-outlook-as-backlog-reaches-45-1gw/","excerpt":"First Solar's contracted backlog stood at 45.1 GW valued at approximately $13.6 billion as of June 30, 2026, down from 50.1 GW at year-end 2025","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"全球太陽能模組均價在 2011-2013 這輪下行崩跌：2011 年 $1.37/Wp，2012 年跌到 $0.79/Wp（跌 42%），2013 年初再跌 18% 到 $0.65/Wp","source":"pv magazine India - Solar industry faces collapse amid surplus and plunging prices","url":"https://www.pv-magazine-india.com/2024/08/28/solar-industry-faces-collapse-amid-surplus-and-plunging-prices/","excerpt":null,"as_of":"2013-01-01","retrieved_at":"2026-09-29","affects":["cyclical_downside_scenario","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"First Solar 上一次下行谷底在 2022 年：Q1 2022 毛利率驟降到 3.1%，全年僅 2.67%；之後強力回升，2023 年回到 39.19%，2025 全年約 41%","source":"stock-analysis-on.net - First Solar Inc. Analysis of Profitability Ratios","url":"https://www.stock-analysis-on.net/NASDAQ/Company/First-Solar-Inc/Ratios/Profitability","excerpt":null,"as_of":"2022-12-31","retrieved_at":"2026-09-29","affects":["cyclical_downside_scenario","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"PV 產業上一輪製造業下行約持續 2012-2014 年（2-3 年）；目前這輪下行預期延續到 2026 年，是近 20 年來第二次大型 PV 製造業下行","source":"pv-tech.org - PV manufacturing downturn to extend into 2026","url":"https://www.pv-tech.org/pv-manufacturing-downturn-to-extend-into-2026/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-09-29","affects":["cyclical_downside_scenario","triggers"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026年有針對 FSLR 的證券集體訴訟（Day v. First Solar，EDNY），集體期間 2025-02-26 至 2026-02-24，指控淡化關稅影響；原告律所公告，指控未經證實。","source":"Levi & Korsinsky 公告（natlawreview）","url":"https://natlawreview.com/press-releases/first-solar-inc-fslr-lawsuit-investors-urged-contact-levi-korsinsky-august-0","excerpt":null,"as_of":"2026-06-24","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"First Solar 對 JinkoSolar 專利訴訟（德拉瓦），2025-11-20 PTAB 駁回 Jinko IPR。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1274494/000127449426000021/fslr-20251231.htm","excerpt":"On November 20, 2025, the U.S. Patent Trial and Appeal Board declined the petition, ending the proceeding.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#2","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2025-09 對 BP Solar/Lightsource 追討 3.236 億美元。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1274494/000127449426000021/fslr-20251231.htm","excerpt":"demanding payment from the Defendants of $323.6 million, along with certain other receivables for solar modules previously delivered to the Defendants.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"FSLR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.25,"operating_margin_pct":37.69,"fcf_margin_pct":4.64,"rd_intensity_pct":5.51},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FSLR","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"CSIQ","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":16.43,"operating_margin_pct":-0.55,"fcf_margin_pct":-31.42,"rd_intensity_pct":1.67},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSIQ","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"JKS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":4.75,"operating_margin_pct":-6.7,"fcf_margin_pct":null,"rd_intensity_pct":1.64},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JKS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ENPH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.78,"operating_margin_pct":4.53,"fcf_margin_pct":11.17,"rd_intensity_pct":15.02},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ENPH","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"FSLR"},"financial_history":{"ticker":"FSLR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":2619319000.0,"revenue_yoy_pct":null,"gross_margin_pct":2.67,"operating_margin_pct":-10.72,"net_income":-44166000.0,"diluted_eps":-0.41,"free_cash_flow":-30236000.0,"fcf_margin_pct":-1.15,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":3318602000.0,"revenue_yoy_pct":26.7,"gross_margin_pct":39.19,"operating_margin_pct":26.7,"net_income":830777000.0,"diluted_eps":7.74,"free_cash_flow":-784515000.0,"fcf_margin_pct":-23.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":4206289000.0,"revenue_yoy_pct":26.75,"gross_margin_pct":44.17,"operating_margin_pct":33.13,"net_income":1292044000.0,"diluted_eps":12.02,"free_cash_flow":-308077000.0,"fcf_margin_pct":-7.32,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":5219376000.0,"revenue_yoy_pct":24.09,"gross_margin_pct":40.62,"operating_margin_pct":30.59,"net_income":1528229000.0,"diluted_eps":14.21,"free_cash_flow":1187230000.0,"fcf_margin_pct":22.75,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/FSLR/FSLR_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**First Solar, Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good afternoon, and welcome to First Solar's Third Quarter 2026 Earnings Conference Call. This call is being webcast live on the Investors section of First Solar's website at investor.firstsolar.com. [Operator Instructions] And please note that today's call is being recorded. I would now like to turn the call over to your host, Byron Jeffers, Head of Investor Relations.

**Byron Jeffers** (Executives):
Good afternoon, and thank you for joining us. With me today are Mark Widmar, Chief Executive Officer; and Alex Bradley, Chief Financial Officer. Mark will begin with an update on the business, followed by Alex with our financial results and outlook.
Before we begin, today's discussion will include forward-looking statements that are subject to risks and uncertainties. Additional information regarding these risks and uncertainties can be found in our earnings press release, other SEC filings and the earnings material available on our Investor Relations website at investor.firstsolar.com. We undertake no obligation to update any of these forward-looking statements as a result of new information or future events.
During today's call, we will also discuss certain non-GAAP financial measures. Reconciliation of these measures to the most directly comparable GAAP measures are provided in our earnings press release and accompanying presentation. We encourage investors to review those reconciliations as non-GAAP measures should not be considered in isolation or a substitute for financial information prepared in accordance with U.S. GAAP.
With that, I'll turn it over to Mark.

**Mark Widmar** (Executives):
Thank you, and good afternoon. Getting on Slide 4. We continue to execute with discipline this past quarter, advancing our U.S. manufacturing expansion, CuRe deployment and perovskite R&D program while delivering strong financial results. We generated approximately $1.2 billion in net sales, expanded gross margin to approximately 58% and delivered adjusted EBITDA of $744 million.
Operationally, our continued CuRe deployment across the fleet is being executed through a disciplined learnings-based approach that began with our Perrysburg Series 6 conversion in Q1 of this year. That approach now extends to our first Series 7 conversion at our India facility expected to begin in the first quarter of 2027, which marks the start of Series 7 CuRe replication across the fleet.  
Beginning in India allows us to first refine the deployment process in a low earnings impact environment before replicating across our U.S. Series 7 fleet. During the subsequent U.S. conversions, assuming a supportive trade environment, India front-end output is planned to be flexed to supply U.S. facilities, supporting U.S. back-end throughput and preserving partial domestic content and Section 45X eligibility production during the transition.
Accordingly, India's finished goods production in 2027 is expected to range from 2.2 gigawatts to 2.6 gigawatts. The pace in sequencing subsequent Series 7 U.S. conversions will be informed by learnings from the India launch consistent with the disciplined learnings-based approach we have taken across all periods of technology transition.
In South Carolina, our Series 6 finishing facility is being brought online in 2 phases as part of the integrated manufacturing flow from Vietnam. The first phase started production in Q3. Second phase is expected to reach commercial launch in mid-2027. As we previously shared, we delayed the second phase by approximately 1 quarter so that the CuRe could be incorporated at commercial launch. Together, these 2 phases are expected to result in 2027 South Carolina production of 2.2 to 2.5 gigawatts.
Beyond CuRe, we continue to advance our next-generation technology road map. Our Ohio pilot line designed to produce Series 6 size perovskite modules remains on track to reach operational readiness in the first half of 2027. We expect this line will enable field deployment of modules to further capture learnings and validate the manufacturing performance and durability profile of this next-generation thin film technology before we undertake broader scaling decisions. Our licensing agreement with CubicPV announced earlier today, together with our previously announced intellectual property agreement with Oxford PV, continues to support the development road map, providing access to foundational perovskite IP as we advance our technology road map. 
Turning to the market environment on Slide 5. The Section 232 proclamation issued in August represents a meaningful shift for U.S. solar manufacturing, and we believe First Solar is well positioned to benefit as the shift takes effect. Combined with fundamentals such as continued demand strength from load growth and data center expansions, we see a long-term opportunity to translate this position into earnings growth.
Section 232 represents a structural change in how the United States approaches solar manufacturing. As the U.S. competes for global leadership in artificial intelligence and the emerging low Earth orbit economy, secure and affordable power will be foundational to both. The country cannot afford to depend on adversarial nations for technologies and supply chains increasingly central to our long-term economic prosperity and national security.
As a technology company and the only fully integrated utility-scale solar manufacturer without dependency on a Chinese crystalline silicon supply chain, we believe we are structurally positioned to benefit from this environment. Note, by 2027, nearly 80% of our global module manufacturing footprint will be located in the U.S.
Long-term demand fundamentals also remained strong. AI-related infrastructure, electrification and the onshoring of U.S. manufacturing are driving significant load growth. These customers need large-scale power quickly, and solar plus storage remains one of the fastest and lowest cost solutions. They are increasingly focused on availability, delivery certainty, bankable warranties and supply chain security, attributes we have built our business around.
As it relates to bookings, we believe the market is working through a transition following the Section 232 announcement with significant influence from other key factors. As a reminder, a substantial portion of our existing backlog is comprised of multiyear framework agreements that are intended to supply customers with projects in various stages of development. While entering into these types of agreements has historically driven significant additions to our backlog, they can also be more challenging for us to plan for and allocate against because of the inherent delivery timing uncertainty associated with projects in early stage of development.
Over the course of this year, while not closing the door on framework agreements with appropriate contractual protections, our customer engagements have shifted more towards project-specific contracting with the 5 projects and delivery schedules. From our perspective, the enhanced certainty surrounding project-specific contracts allows us to optimize module allocation and delivery with a potential trade-off of slowing the pace of an extended multiyear contracted backlog.
At the same time, customers are focused on advancing mid- and late-stage projects where modules have already been secured while deferring procurement on early-stage projects requiring delivery later in the decade. We see several factors driving this behavior, including increased NIMBYism among community residents and growing state and local government opposition.
In addition, the overall inflationary environment together with the continuously evolving tariff landscape have challenged near-term project economics and require greater strategic planning on behalf of our development customers to address system cost increases unrelated to module pricing. As one example, in certain cases, surging battery prices is challenging both projects in construction as well as projects at the PPA bid stage. 
Lastly, an incomplete regulatory picture with regards to the final FEOC guidance as well as the potential for Section 232 tariffs to continue to evolve, particularly as it relates to minimum import prices and the effectiveness of anti-stocking measures has generated volatility in the module procurement market and inhibited customer clarity as it relates to module pricing discovery.
The impact of these current dynamics on recent bookings is most pronounced from our Malaysia facility. While Vietnam is expected to supply the semi-finished product for our South Carolina finishing facility, Malaysia retains the capacity to produce fully finished international modules. We continue to evaluate demand for this product based on core unit economics, tariffs and trade conditions, and customer contracting terms. We expect the operating decision regarding our Malaysia facility to be binary, resulting in either operations at full or near full capacity of 1.8 gigawatt annually or a shutdown of production with a decision expected in the first half of 2027.
Given Malaysia's relatively small contribution to our manufacturing footprint, limited Series 6 blending opportunity in the U.S. absent of Section 45X credits and freight and tariff burdens, we do not expect either outcome to materially impact our run rate earnings profile. Against this backdrop, we remain deliberate on bookings, and we are pleased with the results of this approach. Through today in the U.S., our largest market, we have booked approximately 4.9 gigawatts at approximately $0.35 -- $0.36 per watt inclusive of adjusters. Moreover, our 44-gigawatt backlog gives us the ability to focus on contracting approaches on 2 strategic initiatives.
First, we seek to improve pricing on new module sales relative to our current backlog ASP. Note, pricing will continue to vary by product, Series 6 and Series 7, and by U.S. versus internationally made. Second, we seek to improve contract structures to further mitigate the risk of cost increases beyond our control, strengthening credit support and payment terms and firm up product delivery schedules. Our objective is to optimize across both upfront ASPs as well as long-term earnings profile through disciplined pricing, appropriate contractual protections, strong counterparties and alignment with our manufacturing and delivery strategy.
In summary, our focus on project-specific versus framework agreements, customer focus on near-term project execution versus late data procurement, evolving market price discovery and our contracting discipline have moderated recent bookings on a volume basis but on an economic basis, has generated improved pricing relative to our overall backlog. In addition, we remain focused on our ability to effect our contracting strategic initiatives and are confident in demand for our domestically produced product, particularly for 2029 and beyond when we have available supply.
With that, I turn the call over to Alex to discuss our bookings, financial results and outlook.

**Alexander Bradley** (Executives):
Thanks, Mark. Turning to our bookings and backlog on Slide 6. We ended the quarter with 44 gigawatts under contract, representing approximately $13.5 billion contracted value, exclusive of technology adjusters with scheduled deliveries extending through 2030. Since our last earnings call, we recorded approximately 1.4 gigawatts of additional U.S. gross bookings at an average selling price of approximately $0.36 per watt, inclusive of applicable technology adjusters.
Importantly, substantially all the volume was contracted or in late-stage negotiation, and pricing and terms are largely set ahead of the Section 232 announced. In addition, there remains approximately 4 gigawatts of variable volume associated with previously signed contracts, not currently part of the contracted backlog, but pricing reflective of the pre-Section 232 environment, which our customers have the ability to exercise as of the date [ start ]. Approximately half of this volume has a decision date within the next 5 months, with the other half spread across the remainder of 2027 and 2028. Should our customers elect to receive this volume, it will be recognized as incremental bookings at the time of such election.
During the quarter, we also continued customer notifications related to contractual technology adjusters, aligned with our production plan and intended deployment sequence. These notifications represent a meaningful source of incremental backlog value as CuRe deployment advances across the fleet, with the majority of the adjuster value expected to be realized in 2027 and 2028.
In respect to adjuster-eligible volume, we would note that the ultimate realization of these adjustments is subject to the achievement of the underlying technology milestones, timing of future customer notifications and module delivery schedules, and other contractual conditions. And therefore, the final value and timing may differ from the amounts and periods described.
Of that potential adjuster value, approximately 20% is currently associated with 2027 deliveries, with the remainder weighted to 2028 and beyond. As we continue to progress customer notifications associated with existing bookings tied to our CuRe deployment sequence, together with new bookings removing the adjuster concept as we sell our CuRe product with the technology embedded in the base ASP, the value of the adjusters will roll off over time.
Turning to Slide 7. Net sales for the third quarter were approximately $1.2 billion, a decrease of approximately 23% year-over-year. The decrease was primarily driven by lower module volumes sold to third parties compared to the prior year period. Gross margin was approximately 58%, up roughly 20 percentage points year-over-year. The year-over-year increase was driven primarily by a higher mix of U.S.-produced modules. Gross margin also benefited from lower sales rates and utilization costs, tariffs and duties, partially offset by lower termination-related revenue. 
Operating expenses were approximately $167 million. Research and development expense was approximately $67 million, reflecting continued investment in our technology road map, including perovskite development.  
Net income was $571 million, up approximately 25% year-over-year. Adjusted EBITDA was $744 million, near the upper end of our previously communicated Q3 preview range, with an adjusted EBITDA margin of approximately 60%. Diluted earnings per share were $5.30 compared with $4.24 in the prior year period.
Turning to our balance sheet and capital allocation on Slide 8. We ended the quarter with approximately $1.5 billion in net cash remaining within our long-term target net cash range of $1.5 billion to $2 billion. Our balance sheet and projected cash generation continues to provide substantial financial flexibility.
In February, we laid out our approach to capital structure and capital allocation. This prioritized maintaining the aforementioned $1.5 billion to $2 billion of net cash to provide resiliency to cyclicality and industry volatility and to use additional cash to focus on growth, technology deployment, innovation, R&D, technology road map advancements and M&A, especially related to complementary technology-adjacent opportunities.
We further stated that we would evaluate applying cash generation in excess of the above capital priorities to share repurchases, pending clarity around certain factors, including policy catalysts, new bookings volume and tax credit monetization. In line with this approach and following the Section 232 proclamation issued in Q3, our Board has authorized a share repurchase program of up to $500 million, effective immediately with no expiration date. This authorization reflects confidence in the long-term value of the business while preserving our disciplined approach to capital allocation and ability to continue investing in technology development and growth.
Turning to Slide 9. Our full year 2026 guidance is updated to reflect a lower range of India domestic, international Series 6 and U.S. finishing volumes sold, with an associated reduction in revenue and adjusted EBITDA. As we stated in our original guidance in February, we entered the year assuming our India facility would flex production as needed to match acceptably priced India-based demand in an inherently short book-to-bill cycle market.
We've accordingly reduced our full year India domestic volume sold forecast by approximately 0.7 gigawatts. We also stated in February that we entered the year assuming limited in-year demand for our Series 6 international product, and bookings activity for 2026 deliveries has remained consistent with that assumption.
While the low end of our total U.S. component volume sold forecast reflects a modest reduction based on reduced Series 6 WIP share products sold, our forecast range for fully domestic products sold remains unchanged. As we look forward to next year, subject to a supportive policy and trade environment, we expect to increase exports from our India facility to the U.S. market to optimize the margin potential from this factory. And as Mark discussed, we expect to make a decision on the long-term operating path for our Malaysia facility in the first half 2027.
Core operating expenses primarily increased as a function of increased legal spend associated with defending our TOPCon intellectual property position, which we believe has the potential to drive future revenue and earnings upside; and increased R&D spend on perovskite development. Note, our full year perovskite-related spend originally forecasted approximately $100 million is now expected to total approximately $120 million. This forecast increased in 2027 as we seek to advance this next-generation advanced technology.
Core OpEx increases were offset by a delay in certain start-up expenses of our South Carolina facility now expected in mid-2027, leaving our total 2026 operating expense guidance unchanged. Net cash guidance remains unchanged with reduced cash inflows from volumes sold offset by a reduction to forecasted CapEx.
In summary, we believe we remain well positioned as we close out 2026 and look forward to 2027, driven by U.S. policy framework supporting true domestic manufacturing, continued load growth as the United States competes to lead in AI and utility-scale solar ambition to meet the cost and speed to power requirements of a rapidly modernizing U.S. economy.
These drivers align well with our 44-gigawatt contracted backlog for mostly nearer-term deliveries and greater module supply availability in the 2028 and beyond time frame, which we expect further improvements in pricing and contractual terms relative to our existing backlog. We continue to invest in our future, including our staged CuRe technology replication across the fleet, and increased perovskite spend in R&D, IP partnerships and our Perrysburg pilot line. Our strong balance sheet allows us continued investment in the business while concurrently enabling capital return to shareholders.
And with that operator, please open the line for questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Moses Sutton with BNP Paribas.

**Moses Sutton** (Analysts):
Maybe you could like elaborate on what seems like literally 0 urgency for developers to book '29 volumes. I sort of get the point on there's NIMBYism. There's positive economics. There's tariffs. But we also hear from developers they expect to really do a lot of safe harbor volume in [ 2029 ]. Panel prices will structurally go up 50%. They don't have inventory that extends that far out even if they do for the next 2 years. So -- sorry for the long question, but would there be a strategy change that's necessary? Would you cut price to $0.34, $0.35 and book the rest of the decade? It would seem there's a little more urgency for '29 than there used to be. Maybe you can elaborate a little more because we do still expect at least tens of gigawatts of TAM each year in '29 and '30?

**Mark Widmar** (Executives):
Yes. Well, look, I think the first thing, I think, we just need to maybe step back and reflect on is that everyone obviously is evaluating the execution against their development pipeline. And there's near-term initiatives and areas of focus that they're concentrated on right now and disruptions at certain times, as we indicated, even as it relates to whether it's battery costs or other component costs, I mean, or the impact of tariffs that are swinging various projects around. People are all trying to work through that. They're trying to secure their financing. There's still interconnection challenges that people are working through. And then probably the biggest issue that people are continuing to struggle with right now is just the challenges that are continuing to happen in local communities even at the state level, in particular, from a government standpoint and trying to push back on deployment of data centers, as we indicated in the NIMBYism comment that we had in our prepared remarks.
So there's a lot that they got going on right now, some engagements that we are having right now with customers. And we are starting to book a pipeline of opportunities that are going out into that horizon and some even beyond '29 and going into '30 and beyond as well. But everyone is kind of like, "I got all these near-term things I'm focused on at this point in time. I've got to work through these, get everything addressed. I'm still trying to digest the implications of what happens with the full implementation around 232." People are still trying to think through the FEOC guidance is going to come out sometime either later this year or beginning of next year. And so I think there's clarity that everybody is looking for at that point in time.
So I think it's just a matter of just the timing of letting some of this work its way through and where their near-term priorities are to then think through the balance of the decade and what they still need to do. I mean everyone is really concerned now of meeting their 48 safe harbor requirements, which these projects have to be safe harbored by -- and completed and commissioned by the end of 2028. And there's not as much focus going further out into the horizon, and that's largely what we're seeing from customers.

**Alexander Bradley** (Executives):
Moses, just a couple of other comments. So we said on the call that we were seeing this year challenges in near-term book to bill on our international volume. And if that ties into what we said before, we don't want to be in the spot market. That's a challenging place for us to be. But if you look at our contracted backlog, we're still booked out a couple of years in advance. So when you talk about urgency around booking 2029, obviously, we'd like to see bookings momentum. We're open for business, but I don't think we have a desperate urgency to be booking in that horizon right now. 
And we also talked on the call in the prepared remarks around how we're thinking about contracting, and we're looking increasingly at individual projects versus large frameworks. And we're happy to take framework deals with the right set of structural protections within them, but we see more and more customers actually looking at individual project deals, and we've been looking at that. And generally speaking, that's going to give you shorter-term visibility relative to 2029. So if it's trying to book specific deals, specific projects, that the amount of clarity you have for 2029 is a lot less than if you were looking at framework horizon. So there's that piece to factor in as well.

**Mark Widmar** (Executives):
Yes. And Moses, one thing I should have mentioned, too, just I think it's just a really good example maybe to highlight kind of the dynamics that are going on, right? Now we are in negotiations with the customer for a 2-gigawatt procurement decision that was largely into final negotiations and documentation associated around the agreement and the particular state that this project was being developed put a moratorium in place. And the whole project stopped, right? And this has happened after the announcement of the 232. So customers are just uncertain and when that level of uncertainty does happen, then they're not going to be making commitments until they get better clarity.

**Operator** (Operator):
Your next question comes from the line of Joseph Osha with Guggenheim.

**Joseph Osha** (Analysts):
Following a little bit on Moses' question. Alex, you mentioned that bookings we're seeing now reflect conversations that were undertaken prior to 232. Can you maybe give us a little bit of a preview on where conversations are landing for conversations that commenced post 232?

**Mark Widmar** (Executives):
Yes, maybe I'll add a little bit color around that. Since the announcement of 232, we have revised and increased our pricing. In some cases, they were deals that were still in the early stage of negotiations. So we have increased pricing in those negotiations with customers. It -- and if it's a new opportunity that's come in our way that wasn't even in any form of conversation prior to the 232, then those prices have gone up relative to what we would have been indicating previously. 
We still have to work through all those issues, right? And I think we're -- anytime you get through here in an environment of rising prices, there's a lot of price discovery that's going to get done. Everyone wants to go out, and they want to evaluate all other options and sort of discover where they think the pricing can be for different dynamics and whether they need the domestic content or how much of the domestic content from a point standpoint do they need.
So they're going to do a lot of heavy lifting to sort of figure out and triangulate what makes the most sense, partly because they also have to, in most cases, go back and get approval through their boards. And when you see a price point in the market that was there previously and now that, that price point has increased significantly, then everybody has to then sort of do the due diligence around that.
So what I would say is the deals that -- some of the deals that we have announced in this quarter were priced before the 232. In cases where we were in earlier negotiations with customers after the 232, we have looked to try to increase that and then clearly, any new opportunities have kind of informed the more comprehensive view of what we think the pricing environment is like today. But like I said, the price discovery is going to take a while before you'll start to see that volume being executed.

**Operator** (Operator):
Your next question comes to the line of Philip Shen with ROTH Capital.

**Philip Shen** (Analysts):
In terms of price, just to continue with the conversation, the price discovery may take some time. It sounds like you are -- you have 4 gigawatts, of which maybe 2 gigawatts needs to be decided on in the next 5 months. And so just curious where -- what are we talking about now in terms of where pricing could go to in the crystalline silicon world. We've quantified it as pricing has gone up $0.10 to $0.20 a watt depending on the product and maybe timing. And so that's a big move, and I understand the price discovery patience or timing that people need because they have to process kind of this upside shock to their economics. And so I was wondering if you can share with us a little bit of where do you think -- what could you book in the next quarter and then what kind of price do you think you might get.

**Mark Widmar** (Executives):
Yes. Phil, the one thing on price, too, I just want to make sure that we've highlighted this before. It does vary by -- we have it in our prepared remarks as well. I mean the price for us -- for our Series 6 product is different than our Series 7 products. Our domestic -- high content -- domestic content product is different than a fully international imported module.
So there's going to be a distribution of what that pricing could look like. And so if I'm selling something that's being imported from Malaysia, as an example, that's going to be at the low end of that continuum. And if I'm selling our Series 7 product that's domestically manufactured here in the U.S., that's going to be at the high end. So there's going to be a continuum around pricing.
As it relates to -- we just announced, again, I think, another quarter at $0.36 or something like that is what our -- since the last call -- call to call, I think it was around $0.36. And we have deals and that's an average. We've got deals that are above that, and that's a momentum that we'd like to continue to carry on -- carry forward.
But I also want to be careful of we've got to put a marker out there with so much that still is in -- is fluid and is still evolving. I don't want to give an indication of what that price realization could be. We're just going to work to try to see how we can engage the market and capture the highest value relative to competitive alternatives. And if crystalline silicon stays in the range that you referenced and -- then that gives us quite a bit of opportunity to improve pricing dynamics for our technology. But a lot of work still to go to get there.

**Alexander Bradley** (Executives):
So maybe just 2 other comments. As it relates to the volume that we already have that may get elected by customers, that's going to range from somewhere close to the current backlog average to somewhere close to where we're pricing now. So you're going to see a variety in that. But it's going to be between what we see historically and what we're seeing currently.
And then as you think about future pricing, crystalline silicon pricing is still most likely for deals in the next 12 to 24 months. And I don't think there's a good market for that price point when you get out into the late '28, 2029, 2030 time frame, which is when we have most of our available product to sell.
So one of the reasons, I think, customers are still doing price discovery is they don't necessarily have a good benchmark that far out that's reliable or trustworthy. And so we're still working through our pricing relative to where we think the market is and customers trying to understand our pricing relative to where they think that market point will be.

**Mark Widmar** (Executives):
Yes. And I think the other point maybe I'll highlight as well, Phil, is that, look, we still have a little bit of time before we get to full implementation on the 232. And what I will say is I'm very happy to hear the kind of enforcement focus that the commerce has to address stockpiling.
The problem is there's such an aggressive posture and risk-taking that people are willing to do in order to get a module into the U.S. at some pre-232 MIP. And so we're in a lot of stories of to what extent people are going to in order to try to get product into the market, whether it's at the cell level or whether it's at the module level and just aggressively pushing the envelope. And I know Commerce is doing a great job of trying to enforce that and to prevent that from happening and stopping that, but the onslaught of this stuff is coming from every angle.
And so I think there's also that piece that people are waiting for. Let's let -- maybe there'll be a lot more product that does make it into the market somehow. And a customer may say I'm willing to take some -- wait and buy some time because maybe I can get an opportunity to get some pre-232 volume that's been imported into the market at some crazy low price. And that's informing their decision or at least creating a willingness to wait. And we obviously are there to encourage Commerce to do whatever they can to ensure that enforcement of preventing that stockpiling.
But that's not stopping the activities. People are willing to take a lot of risk, and it's very aggressive. And we'll have to see how effective Commerce could be. So far, we applaud them for their efforts. There's no doubt about that.

**Philip Shen** (Analysts):
Yes. So far, they blocked -- I think we've learned about 60 importers blocked that up until about 2 weeks ago, and that's out of an importer count of, I think, 400. Pre-232, we learned that it was 200. And then post-232, that jumped up to 400. They've blocked at least close to 60. So it looks like they're working -- the enforcement is pretty aggressive. Any thoughts on that? And then how much higher MIPs could go up and what kind of timing that could be?

**Mark Widmar** (Executives):
Yes. I think on the enforcement, I mean, I don't -- some of you may know that we did our ribbon cutting for our new factory in South Carolina and Secretary Lutnick was there and a number of the key members of his team were there. So it gives us a great opportunity to talk with them and to sort of continue to emphasize the importance of this enforcement. And they're 100% committed on the enforcement side and to do everything they can to prevent those types of things from happening.
And where we can, we are sharing insights with them and things we think could be helpful from that standpoint. And just to your point, I mean, the risk tolerance and -- that people are willing to take, knowing that there's going to be that level of enforcement is not slowing things down very much. I mean, yes, you can get 60 out of the -- if the number of importers of record went up from 200 to 400, and it's great that we caught 60 of them, but that means there's another 140 that potentially are still getting around the current enforcement levels, right?
So -- and then as it relates to the MIP, look, I think is very clear. If you haven't seen Lutnick's remarks at our ribbon cutting, I think you just ought to watch it. There's a couple of videos that are out there, and he's 100% clear of the strategic intent of what we're trying to do here, which is to create U.S. manufacturing, U.S. jobs, U.S. supply chain, U.S. technology and things that can help enable energy independence and national security. And so they're going to enforce this, and they're going to put the right requirements in place of ensuring the domestic manufacturing can thrive and then put as many incentives as possible to encourage people to manufacture more here in the U.S., which I think is great.

**Operator** (Operator):
Your next question comes from the line of Brian Lee with Goldman Sachs.

**Brian Lee** (Analysts):
I know we're kind of all dancing around the same topic, so I'll try my best as well. But it sounds like you guys are moving from being a contract go-to-market strategy to more of a spot market go-to-market strategy, which I think most of your peers do and now is the case even for First Solar a few cycles ago. So maybe, as you said, Mark, the bookings cadence moderates here with all the uncertainties, but the bookings cadence can potentially be more fluid on a quarter-to-quarter basis. I guess, is that fair? And are you equipped, I guess, from a sales force perspective to be able to manage through that?
And then, again, on the pricing entitlement side of things that you keep referring to developers and all the uncertainties that they're having to grapple with. I guess what are you tasking your sales force with in terms of this price discovery process post 232? I would imagine they're not going to go anywhere lower than what you've been booking at recently, which is $0.36. But is it a range of like $0.36 to $0.40, $0.40 plus? Like what are the puts and takes around kind of what they're going out to market with?

**Mark Widmar** (Executives):
Yes. So I think what we were trying to say, Brian, just as it relates to -- a lot of the deals that we announced going back 3 or 4 years ago when we built our contract backlog, a lot of these were multiyear framework agreements that have indicative delivery schedules associated with them. And then as we said before, they had certain rights, annual ship rights or quarterly ship rights. Things could move around from that contracted schedule, but it wasn't tied to a specific project.
And what's happened when we do that is the volatility of our customers' development pipeline for various reasons is just whipsaw stuff all over the place, right, in terms of, hey, this is what the contract was, and now this is what the current requirements are given the state of their development portfolio of projects and what have you. And what we're trying to do now a little bit -- and not that we won't get back to that. We've got a couple of very large deals where there'd be more of that legacy kind of framework agreement, strategic partnerships, and we'll clearly do those. But near term, what we're seeing more is that everybody is like, "I got a particular project, and I want to negotiate this particular project." And that gives us better clarity and certainty of, a, the project where it sits in its permitting process, where it sits in its interconnection process, where it is in its financing, if it's approaching that or at least we know what the time line and the profile looks like and gives us a better clarity of the timing of when the shipments need to occur. 
So that's where the near-term focus is on that. But what I would say is that after this price discovery kind of gets better understood, I think we may see some customers moving into that other direction to say, "I really want to lock in and secure my project pipeline going out into '29, '30." And I like I said, we have some customers that are even wanting to start having some conversations that go beyond 2030.
So as it relates to the sales force, I somewhat alluded to that. First off, from a capacity standpoint, I don't think it's an issue with our capabilities of our sales team to handle that pivot, right, to more project specific versus framework structures. But as I somewhat alluded to is we have gone and we've repriced deals that were in the early negotiation phase and any new deals that have come to us now are obviously reflected of what we believe the current market pricing should be. So I'm not going to give you an indication of what that looks like. But we have recalibrated and I think the market fully understands that. 
But I also want to continue to go back. I mean there is a continuum of what those prices are going to be in near term, and I think I've even alluded to this in prior calls. What we have right now available to book is more Malaysia finished good module coming into the U.S. or an India product coming into the U.S. And so that profile in terms of ASP entitlement is going to be on the lower end of that continuum, as I indicated. The lowest price point we would have for a module will be for that international product coming -- fully finished international product coming into the U.S., and then the highest will be kind of 100% domestically manufactured Series 7.
So it can move around. That average is reflected in the numbers that we've been giving you. But in any particular quarter, if I'm heavy on maybe international modules coming to the U.S., that would drive that average ASP down. And clearly, we'll provide color around that. But yes, I mean, pricing is reestablishing itself at a higher point than it has been historically, and we'll continue to see how price discovery works through.

**Alexander Bradley** (Executives):
Brian, just one follow-on point to that framework discussion. And one of the challenges that we've talked about over the last couple of years now is the period cost that we've been incurring around the amount of inventory we have to keep, the storage cost of that inventory, overall sales rate. If you think about when there's an ability to move volume around or when customers need to do that because the timing of their projects shift, I have to keep inventory to make sure I can service all the available contracts that I have. So that generally means my AR -- my overall inventory position as well as my working capital position is worse.
At the same time then, if that product all does move to the right from a schedule perspective, now I end up having to warehouse materially more volume than I expected. So generally speaking, it's become harder for us to plan around that, and we're seeing a significant financial impact from that. If we move to more of a project-based model where there's a certainty around an individual project, the timing of that project and delivery schedule, that allows me to plan on the operational side much more efficiently, reduce working capital, reduce storage costs as well. So it provides that operational financial efficiency that we're looking for.

**Operator** (Operator):
Your next question comes from the line of Jon Windham with UBS.

**Jonathan Windham** (Analysts):
Perfect. Mark and Alex, I appreciate you taking the questions. We'll get on to the exciting topic of filing your taxes. So in the presentation, you note there's $1.9 billion of government grant receivables. My understanding is that's payable 2 to 3 months after you file your annual returns. Can you just give us an indication of how your planning is for that cash actually going to your balance sheet and then into your bank account? And then any comments around the liquidity in the secondhand market if you were to decide to try to monetize those early?

**Alexander Bradley** (Executives):
Yes. So you're right. On the balance sheet, there's about $1.9 billion. About $100 million of that is related to India. So you got about $1.8 billion in the U.S. And then part of that $1.8 billion relates to credits that were generated last year and we have yet to file. Yet -- we have just filed our tax return but yet to receive refundability for those.
But if you look at this year's credit generation, the forecast is about $2.1 billion of credit to be generated this year. If you look at the 2024 credits, we sold most of those. We did keep a portion of them to file our 2025 tax return in October of 2025, and we received refund for what was about $120 million in about 3 months' time. And importantly, even within that 3 months, the government was actually shut down for about a month of that. So the turnaround time from filing to receiving the cash, relatively short. 
As it relates to this year, we haven't made a decision yet. We've not made any assumption around a reduction in the carrying value of those credits if we were to sell them. We've seen that the market through the first half of this year, I think, was a little softer for credit sale value. That's picked up pretty significantly towards the back end of the year as large corporates just have better position and understanding of their tax position coming into year-end and looking for tax planning strategies.
So we're seeing a lot more outreach and interest around those credits. We're in some discussions around potential sales there. But we'll look to balance how much we would like to sell to pull some liquidity forward versus how much we're comfortable filing for refundability for because then you're not taking a discount on that sale. So it's a balancing act, and we're in discussions around those at the moment.

**Operator** (Operator):
Your next question comes from the line of David Arcaro with Morgan Stanley.

**David Arcaro** (Analysts):
I was wondering, with the shift toward individual project booking, typically, what's the time frame for how far in advance you would end up getting that order into your backlog relative to, I guess, the timing of the project. And I think you had suggested that the decision on Malaysia could be made in the first half of 2027. Are you thinking that we'll get enough kind of visibility by that time, that you'll be able to make that call on what to do with that capacity?

**Mark Widmar** (Executives):
Yes, I'll take the first one, and I'll let Alex take the Malaysia comment. So yes, so basically, what happens on a -- if we're bidding specific to a project, again, module's usually at the forefront of your procurement-led decision. You want to secure that technology because it also drives your design of the factory, right, or the design of the project, excuse me. So crystalline silicon and CadTel, it will design your factory and your plant, excuse me differently. There's different string count, different voltage and other parameters, which you would want to optimize for.
Generally, we don't have the same constraints as it relates to the tracking -- backtracking requirements because we don't deal with the same adverse impact of shade or diffused light and those types of things. So there's a lot that has to be done early on. And so you're going to want to source that module and lock that up so you can be unencumbered now to figure out how do you want to design and optimize at the project level.
So it could be 18 months, 2 years before the first delivery would start to happen or at least for sure until the project would be commissioned. So it doesn't really -- it shortens your time line a little bit from a visibility standpoint, but it doesn't really significantly shorten it. But it gives you better certainty. There's no doubt about that. People would be willing to go out into 2030 in a framework kind of construct. And projects normally would be commitments that would go out into '28 or into early '29, is probably not as far out as they would want to go but still more than enough visibility to properly understand the project and price it appropriately.

**Alexander Bradley** (Executives):
And David, as it relates to Malaysia, yes, I do believe we have enough visibility going into the first half of next year. We've effectively been carrying that asset, running at very low throughput for the whole of this year. And we've done that deliberately. We thought the underutilization costs associated with that was worth the option value of having the ability to run what would be up to about 1.8 gigawatts of international volume.
As we look through the 232 announcement, as Mark said, the customer base still in transition, fully understanding what that looks like and trying to work through what their need is going to be. We want to make sure we have the optionality in Malaysia in the event that, that significant demand does materialize. We've also said that we have an order of how we want to make sure our factories sell.
So first, we look to make sure our U.S. content is sold. Secondly, we look to make sure we're selling our finishing line production out of our new facility in South Carolina and then after that, the full international product. We're also going to be bringing more volume from India over into the U.S. next year, subject to a trade and tariff environment that makes sense. So I think we'll have the understanding of the marketplace that we'll need by the first half of next year, and we're still looking at that as an option value and seeing how the effect of the 232 plays out.

**Operator** (Operator):
Your next question comes from the line of Vikram Bagri with Citi.

**Vikram Bagri** (Analysts):
Apologize for another question on pricing, but this is important. On this call itself, we've heard pricing either go down by a couple of cents or go up by $0.20. So Mark, fully appreciate the lack of clarity about the environment we are in. But for Series 7, is there a construct you can provide for pricing that we should keep in mind. So if pricing for silicon-based panels move higher, we should assume a certain discount to that, which some people will characterize as quality discount. And I imagine pricing also depends on several other factors, project and contractors. But all else being equal, is there a construct where pricing for silicon-based panels moves higher than $0.40 or $0.45, we should assume a certain fixed discount for Series 7, U.S. Series 7?
And then related to that, Mark, you talked about a number of items limiting ability of developers to make long-term plans. Is competition in panel manufacturing is also one of the factors, which is sort of like prohibiting them from committing to supply of panels? Do you think the lack of urgency to book 2029 is also a function of new capacity coming online potentially in the U.S. from other suppliers of panels? Or how do you see the competition evolve over the next couple of years in the sector?

**Mark Widmar** (Executives):
Yes. So I'll talk on the -- so if you take S7 as an example and -- just one thing to make clear, you made a comment about quality discount. I don't know if you're familiar with how energy predictions are done for crystalline silicon technology. They actually have a quality factor that they use, which would -- basically reduces the energy profile of the technology as part of the energy prediction, of which that does not apply at all to First Solar's technology.
So we don't have any quality factors that are assumed in the energy predictions that are underwritten by -- and supported by IEs and the banks, so I'm not sure what your point is around that. But crystalline silicon clearly does. They have a meaningful quality factor that is being used when they do the energy prediction for that technology.
The -- what I would say, if you take a Series 7 CuRe product and you compare it from an energy profile because, again, energy is what our customers pay for, and what the value of that product would be relative to a PERC technology, it would be advantage to PERC, so there would be no discount to PERC. It would also vary with where it is because, obviously, our technology does not have what CuRe will have better bifaciality than our QED product is. Our bifaciality is lower than crystalline silicon. So if you were to go further Northeast where you get a better impact of bifaciality, then you'll see a different outcome. If you go to the other Southwest or to the Southeast and more hot and humid -- hot climates or hot and humid climates, you're going to see a better outcome for our technology.
And then if you compare us to TOPCon, which, again, the vast majority of anyone producing or selling any TOPCon product in the U.S. is infringing on our IP, which we will stand by and completely enforce that, then you'll have a slightly different outcome. We would actually be average, slightly disadvantaged to TOPCon of a few pennies. So it depends. I mean you've got different situations, different geographies, different terrains. A lot of different things factor into that and determine the relative competitiveness of the technology. So -- but I would say general rule thumb, Series 7 CuRe is going to be advantaged against PERC and disadvantaged by pennies relative to TOPCon.
As it relates to the competition and how that all plays out, you have to think through how much are you willing to -- first off, is the competition and the manufacturing that's coming in the U.S. truly FEOC-free, truly unencumbered by any dependency from the Chinese, whether it's the supply chain, whether it's the tools and the manufacturing equipment, whether it's the IP, right?
A lot of our customers do their own subjective analysis and have concluded that there is a substantial risk still that these entities are not FEOC-free, and they don't want to take on that risk. That puts us in a much better position. There's no doubt about that, and that's also why I think you're going to find customers leaning into developing partnerships with First Solar that go longer dated.
I believe I remember reading one of the filings recently for one of the U.S. manufacturers, and I believe almost 100% of the sales that they're generating this year is to a related party. And I understand that related party to be a Chinese counterparty. So I mean it tells you, just looking at that as an example, that in certain situations, customers are not willing to take on that risk. And we still don't have full clarity around FEOC yet, and I think that's why people are being a little gun shy.

**Operator** (Operator):
Our final question comes from the line of Dimple Gosai with Piper Sandler.

**Dimple Gosai** (Analysts):
My question is regarding just December 4 in terms of outcomes and what you're hearing. I mean there's been a lot of news recently. T1 recently filed for a waiver around cell imports. We're hearing a lot about lobbying for exclusions. And we also know utilities are pretty price sensitive here. So are we -- in your view, is there a risk to the upside or downside just in terms of the outcome there?
And then separately, just kind of talking about some of the news that we're hearing about. There's also news on Swift Current lawsuit that's been in the news. Is there anything you can speak about here? Is there any merit to that? Is there a size associated with it? And any merit really?

**Mark Widmar** (Executives):
Yes. As it relates to the exclusions, look, I do believe because, again, the program incentive and motivation is to try to ensure manufacturing here, reshoring of manufacturing, true manufacturing, truly unencumbered by Chinese or adversarial countries' dependencies. Each one of those will be determined on a fact and circumstances basis and work through with Commerce to say is there true substance to this. And then in general, the focus with Commerce is to limit the period of time at which that exclusion would be provided.
I don't stay on top of it. I don't know -- my team may have better insights than I do in terms of have any exclusions been granted at this point in time. It's not clear to me that there have been any granted exclusions. I know there's been some representation of statements that have been made, but I don't believe there's any actual exclusions that have been communicated publicly at this point in time. But that's something that we're going to have to stay close to and understand.
I'm perfectly fine though competing. We've always said U.S. manufacturing on a level playing field, First Solar is more than happy to compete on our own merits and our technology and the competitiveness of our manufacturing process in our supply chain. So if some of that does happen, then it will evolve, and that will create the domestic industry that I do believe still is a strategic thread that's important for us as a country. 
Assuming we do it right, right? Assuming it truly is U.S. technology, U.S. manufacturing and U.S. supply chains, right, creating American, U.S. jobs and supporting American families. There's no doubt about that. That's absolutely critical from that standpoint.
As it relates to the lawsuit, I really can't comment much of anything around that. We actually will be filing our response here shortly for the required time line. And I think there'll be better clarity around the issues in the allegations that have been raised during that -- during the -- or part of that lawsuit.
What I will say is that we have always -- even with the engagement with Swift, as we've always said, we will stand by and we will support under the parameters of our limited liability warranty, the obligations that we have. Again, that largely is reflective and relates to the Series 7 initial product launch that we had indicated that there was a couple of issues that came out as part of that launch that resulted in an initial stabilization of that technology to be below expectations. And then underneath that program we put in place, we said we would remedy those issues with customers. And we engaged even with Swift to have that have that conversation.
I think where the challenge comes in is where people are asking for remedies that are outside the parameters of the warranty, and that's just -- that's not something that we will do. But we will be more than -- we'll stand behind the technology, and we have that conversation with Swift in this case. And they chose to try to pursue a different approach where they think they could be successful. And again, you should see our response in our filing coming out here in the next several weeks.

**Operator** (Operator):
We have reached the end of the Q&A session. This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FSLR_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Alexander Bradley (CFO)｜guidance：CFO 表示 2026 全年財測維持不變（原話："Our full year 2026 guidance remains unchanged."）
- 2026-07-30｜Alexander Bradley (CFO)｜guidance：財測現假設淨關稅影響 6,000 萬至 8,000 萬美元（含 IEEPA 淨回收與下半年 Section 301 假設）（原話："assumes a net tariff impact of $60 million to $80 million"）
- 2026-07-30｜Alexander Bradley (CFO)｜guidance：Q3 出貨量指引 3.9–4.5 GW（原話："volumes sold between 3.9 gigawatts and 4.5 gigawatts"）
- 2026-07-30｜Alexander Bradley (CFO)｜guidance：Q3 調整後 EBITDA 指引 6.25–7.75 億美元（原話："EBITDA between $625 million and $775 million"）
- 2026-07-30｜Alexander Bradley (CFO)｜guidance：印度產能假設主要在國內短週期市場銷售、高稼動率；上半年訂單約 1.1 GW（原話："totaled approximately 1.1 gigawatts"）
- 2026-07-30｜Mark Widmar (CEO)｜margin：Q2 毛利率約 57%（原話："expanded gross margin to approximately 57%"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：CFO 拆解毛利率年增原因之一：約 8,900 萬美元 IEEPA 關稅淨利益（原文金額 $89 在上一行）（原話："million net IEEPA tariff-related benefit"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：毛利率另一拆解項：符合 45X 稅額抵減的模組組合提高（原話："higher mix of modules qualifying for Section 45X tax credits"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：IEEPA 淨關稅利益為目前估計，後續可能調整（原話："remains subject to refinement as"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：Q2 調整後 EBITDA 6.44 億美元，高於先前預覽區間上緣（原話："above the high end of our previously communicated"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：部分美國境內運費已接近國際海運成本（因模組交付地點改變）（原話："domestic freight costs are now approaching"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：東南亞廠低稼動每季約 3,000 萬美元，約一半為現金、一半非現金（原話："somewhere around $30 million quarter of underutilization"）
- 2026-07-30｜Mark Widmar (CEO)｜margin：CEO 描述成本環境：大宗商品成本上升、降本空間有限（原話："a pretty challenging rising commodity cost environment"）
- 2026-07-30｜Mark Widmar (CEO)｜margin：CEO 稱當前是降成本最困難的時期之一（原話："probably one of the most challenging times that we've been in"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：研發費用含部分不再用於技術路線圖的研發設備減損（原話："impairment of certain R&D equipment"）
- 2026-07-30｜Mark Widmar (CEO)｜commitment：CEO 表示優先看價格、合約品質與風險分配，而非短期訂單量（原話："we continue to prioritize pricing, contract quality"）
- 2026-07-30｜Mark Widmar (CEO)｜commitment：南卡完工廠第一階段預計 2026 下半年開始生產（原話："first phase of the finishing facility remains on track"）
- 2026-07-30｜Mark Widmar (CEO)｜commitment：Series 6 尺寸鈣鈦礦試產線預計 2027 上半年達運作就緒（原話："operational readiness in the first half of 2027"）
- 2026-07-30｜Alexander Bradley (CFO)｜commitment：CFO 稱 232 結果出來後會盡快形成對東南亞產能的看法（原話："We would expect to evaluate that and have a view shortly thereafter."）
- 2026-07-30｜Mark Widmar (CEO)｜commitment：CEO 表示不會放棄降低投入成本（原話："we're never going to give up on the input costs"）
- 2026-07-30｜Mark Widmar (CEO)｜commitment：新訂單優先要求現金流動性擔保（原話："having cash liquid security against new bookings"）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：季末淨現金約 17 億美元，在目標區間 15–20 億內（原話："approximately $1.7 billion of net cash"）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：上半年營運現金流出 3.6 億美元（原話："Operating cash outflows year-to-date were $360 million"）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：上半年資本支出 2.8 億美元（原話："First half capital expenditures were $280 million"）
- 2026-07-30｜Mark Widmar (CEO)｜capital_allocation：CEO 表示持續投入大量資本於鈣鈦礦商業化（原話："continue to invest substantial capital in our efforts"）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：CFO 提到可運用資產負債表協助供應商擴產以換取遠期定價（原話："We could try and leverage our position of"）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：CFO 對併購表示較過去更願意、更開放，但強調紀律（原話："So we are more willing to do that."）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：東南亞可全流程完工產能約 1.8 GW，待 232 結果再決定（原話："about 1.8 gigawatts of end-to-end fully finished capacity"）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：東南亞產能決策等待 232 結果（原話："we're really waiting for the outcome of the 232"）
- 2026-07-30｜Mark Widmar (CEO)｜product：南卡第二階段完工時間改為 2027 年中，並稱可更早納入 CuRe（原話："we now expect completion in mid-2027"）
- 2026-07-30｜Mark Widmar (CEO)｜product：CEO 稱 CuRe 量產與田間表現優於預期（原話："We are pleased with the performance of CuRe"）
- 2026-07-30｜Alexander Bradley (CFO)｜product：已開始發出合約 CuRe 價格調整項的首批客戶通知（原話："initiated our first customer notifications"）
- 2026-07-30｜Alexander Bradley (CFO)｜product：2026 年 CuRe 銷售的 ASP 上行有限（原話："expect limited ASP upside from CuRe sales in 2026"）
- 2026-07-30｜Mark Widmar (CEO)｜product：Series 6 尺寸鈣鈦礦試產線進度符合時程（原話："Series 6 form factor pilot line remains on schedule"）
- 2026-07-30｜Mark Widmar (CEO)｜product：CEO 對 FCC 逆變器裁決：認為近期不會構成限制（原話："I don't see it being a constraint near term."）
- 2026-07-30｜Alexander Bradley (CFO)｜customer：在手訂單 45.1 GW（原話："our contracted backlog totaled 45.1 gigawatts"）
- 2026-07-30｜Alexander Bradley (CFO)｜customer：自上次財報新增美國毛訂單約 1.9 GW（原話："approximately 1.9 gigawatts of additional U.S. gross bookings"）
- 2026-07-30｜Alexander Bradley (CFO)｜customer：新增美國訂單平均售價約每瓦 0.36 美元（含技術調整項）（原話："average selling price of approximately $0.36 per watt"）
- 2026-07-30｜Alexander Bradley (CFO)｜customer：美國完全整合產線產能已大致被承諾至 2028 年（原話："substantially committed through 2028"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：在手訂單約 41 GW 含某種形式的本土含量要求（原話："Approximately 41 gigawatts of our 45-gigawatt"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：CEO 描述超大規模資料中心業者需求（原話："somewhat insatiable demand from hyperscalers"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：CEO 稱 7 月已簽近 2 GW 美國訂單（原話："we booked almost 2 gigawatts in the"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：另有超過 2 GW 在合約中但附帶先決條件（CP）（原話："There's about 2 more gigawatts, north of 2 gigawatts"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：另有約 2 GW 洽談中，CEO 稱年底前高機率成交（原話："we can close through by the end of the year"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：CEO 確認有客戶因等待政策而觀望（原話："customers that are sitting on the sidelines"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：CEO 說明 1.9 GW 訂單多數發生在 7 月（季末之後）（原話："So most of that happened in July"）
- 2026-07-30｜Mark Widmar (CEO)｜risk：Section 232 結果尚未公布，CEO 仍樂觀認為結果將具建設性（原話："we're still optimistic that the outcome will be constructive."）
- 2026-07-30｜Alexander Bradley (CFO)｜risk：CFO 指 Section 301 產能過剩調查仍有風險（原話："There is still risk around 301 relating to excess capacity"）
- 2026-07-30｜Mark Widmar (CEO)｜risk：CEO 反對 232 設豁免或配額（原話："we don't believe that they should be allowed"）
- 2026-07-30｜Alexander Bradley (CFO)｜competition：CFO 描述競爭格局：多數競爭對手為中國企業且規則不同（原話："the vast majority of our competitors are Chinese"）
- 2026-07-30｜Alexander Bradley (CFO)｜competition：CFO 認為國安性質的 232 設carve-out不合理（原話："doesn't make a lot of sense to have a carve-out"）

### FSLR_Shareholder_Analyst_Call_First_Solar_Inc_20260513.md
- 2026-05-13｜Mark Widmar｜commitment：CEO 確認 CuRe 技術已在 Perrysburg 完成導入，首條 Series 6 產線爬坡符合預期（原話："the CuRe launch is complete in Perrysburg"）
- 2026-05-13｜Mark Widmar｜guidance：CuRe 技術調整可望為 backlog 帶來最高 6 億美元額外營收，主要落在 2027-2028 年（原話："$0.6 billion of additional revenue from technology adjusters"）
- 2026-05-13｜Mark Widmar｜customer：CEO 重申技術策略前提：客戶買的是全生命週期發電量，不是單純名牌效率（原話："buy lifetime energy, not just nameplate efficiency"）
- 2026-05-13｜Mark Widmar｜product：Perovskite 技術可靠度已達可比業界最佳 R&D 成果的水準（原話："reliability results that we believe are comparable to"）
- 2026-05-13｜Alexander Bradley｜margin：CFO 確認 2026 年第一季毛利率明顯擴張，帶動單季每股盈餘創紀錄（原話："margin expansion and record Q1 diluted EPS of $3.22"）
- 2026-05-13｜Alexander Bradley｜commitment：CFO 確認南卡羅來納州加工產線進度符合 2026 年第四季排程（原話："Carolina finishing line remains on schedule for Q4 2026"）
- 2026-05-13｜Alexander Bradley｜commitment：CFO 確認路易斯安那州廠已完成試車並啟動商業化生產（原話："initiated commercial production at our Louisiana facility"）

### 問答異常語氣（迴避／改口／保留）
- FSLR_Q2_2026_Earnings_Call_20260730.md｜問：Brian Lee (Goldman)：Section 232 時程與 $0.40/W 以上價格下限的看法｜答法：CEO 未回應價格下限數字，表示不願給內部判斷（'I don't want to give kind of our internal read'），僅稱仍演進中、保持樂觀
- FSLR_Q2_2026_Earnings_Call_20260730.md｜問：Philip Shen (ROTH)：232 是否會在 8 月公布或延到秋季｜答法：CEO 未給時間點，稱無法提供更強的信心（'I can't really give you a strong view on that'），改談希望正確實施

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
{"date":"20260929","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"第三季財報美國新簽 ≥2 GW 且單價 ≥0.34 美元／瓦，且週收盤站回 250 週均線（約 175 美元）之上","irr_base_pct":8.8,"ev5y_pct":52.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟢","ma":"❌","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.0,"ev5y_pct":52.7,"irr_base_pct":8.8,"max_dd_pct":-55,"bull_5y_price":476.0,"bear_5y_price":88.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"第三季財報美國新簽 ≥2 GW 且單價 ≥0.34 美元／瓦，且週收盤站回 250 週均線（約 175 美元）之上","price_at_dd":172.97,"archetype":"循環/商品","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
