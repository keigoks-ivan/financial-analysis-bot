你是 stock-analyst **v20 判斷 agent**，標的 TSM（20261017）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TSM","date":"2026-10-17","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSM_20261017/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSM_20261017/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP，合併）","value":40.2,"period":"Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）","unit":"US$ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）","citation":"公司新聞稿 investor.tsmc.com 2Q26 Earnings Release（https://investor.tsmc.com/english/quarterly-results/2026/q2；同文件 SEC 6-K https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000451/a2q26e_withguidancexfinal.htm）"},"note":"consensus 約 US$39.5–40.04B（來源：web_search 綜合媒體報導，非單一權威資料庫），實際 $40.20B 落在自結指引上緣、beat consensus 約 1.4%"},{"id":"f_kpi1_tsm_taiwan_ifrs_gaap_non","label":"營業利益率（TSM 採 Taiwan-IFRS 單一口徑，未如美股公司分列 GAAP／Non-GAAP——此為結構性差異，不強行拆成兩筆數字）","value":60.3,"period":"Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）","citation":"公司新聞稿 2Q26 Earnings Release（同上 URL），創歷史新高"},"note":"毛利率 consensus 67.1% vs 實際 67.7%（beat）；營業利益率未查到明確 sell-side consensus 數字"},{"id":"f_kpi4_guidance_q3_2026_2026","label":"管理層 guidance（下一季 Q3 2026 ＋ 全年 2026）","value":"Q3'26 營收 $44.6–45.8B／毛利率 65–67%／營業利益率 56–58%；FY26 營收成長上修至「40%以上」YoY（前次為 30%以上）；FY26 capex 上修至 $60–64B（另加碼美國亞利桑那 $100B 投資）","period":"公告於 2026-07-16 法說會","unit":"guidance range（text）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"公告於 2026-07-16 法說會","citation":"公司新聞稿 2Q26 Earnings Release ＋ 法說會逐字稿（web_search 綜合多家媒體轉引，非官方逐字稿原文）"},"note":"N/A"},{"id":"f_kpi5_archetype","label":"產能利用率（archetype=硬體/設備 追加項；定性描述，公司未揭露具體利用率百分比）","value":null,"period":"Q2 2026 法說會（2026-07-16）","unit":"qualitative","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 2026 法說會（2026-07-16）","citation":"web_search 法說會逐字稿摘要：管理層表示毛利率 QoQ +150bp 部分來自成本改善與「整體產能利用率提高」，未給出具體利用率數字"},"note":"N/A","needs_sonnet":true},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-15","period":"2026-10-15","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-15"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_tsm_gross_margin_pct","label":"TSM 毛利率","value":64.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tsm_operating_margin_pct","label":"TSM 營業利益率","value":56.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tsm_fcf_margin_pct","label":"TSM FCF 利潤率","value":25.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvda_gross_margin_pct","label":"NVDA 毛利率","value":74.67,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_operating_margin_pct","label":"NVDA 營業利益率","value":65.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_fcf_margin_pct","label":"NVDA FCF 利潤率","value":41.92,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amd_gross_margin_pct","label":"AMD 毛利率","value":53.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amd_operating_margin_pct","label":"AMD 營業利益率","value":15.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amd_fcf_margin_pct","label":"AMD FCF 利潤率","value":20.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mu_gross_margin_pct","label":"MU 毛利率","value":72.57,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.gross_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_mu_operating_margin_pct","label":"MU 營業利益率","value":65.67,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.operating_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_mu_fcf_margin_pct","label":"MU FCF 利潤率","value":28.99,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.fcf_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi2_fcf","label":"自由現金流（FCF）","value":287.36,"period":"Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）","unit":"NT$ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）","citation":"web_search 綜合法說會揭露：營運現金流 NT$783B － 資本支出 NT$496B"},"note":"無明確 sell-side FCF consensus 可查"},{"id":"f_kpi3_tsm_sbc_sbc","label":"員工酬勞性現金紅利占營收%（TSM 依台灣公司法走員工利潤分配現金紅利，非美式股權 SBC，口徑不同、不可直接類比美股公司 SBC%）","value":2.93,"period":"H1 2026 累計（非單季，查無單季拆分數字）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"H1 2026 累計（非單季，查無單季拆分數字）","citation":"web_search／SEC 6-K：H1 2026 員工酬勞金 NT$70.35B（YoY +54.3%）÷ H1 2026 營收 NT$2,404.48B"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":412.61,"period":"2026-10-16（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":11.93,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":34.3,"period":"2026-10-16（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.29,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（17.0 → 16.95）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.67,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（22.5 → 22.65）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":1.05,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（28.6 → 28.9）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":16.95,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；已依 data/adr_ratios.json 換算為 adr-usd (koyfin ordinary ×5)","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":22.65,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；已依 data/adr_ratios.json 換算為 adr-usd (koyfin ordinary ×5)","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":28.9,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；已依 data/adr_ratios.json 換算為 adr-usd (koyfin ordinary ×5)","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":7.96,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 15.7 → 16.95（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":26.74,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.43,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":-0.21,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":26.74,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 16.95，分子＝快照價 453.31","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.934,"period":"2026-10-17","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-17"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-3198600.09,"period":"2026-10-17","unit":"TWD m","basis":"yfinance 最新一季：總債務 818380.01、現金 4016980.1（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-17"},"note":"財報幣別 TWD ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 TWD，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":5186.47,"period":"2026-10-17","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-17"},"note":"財報幣別 TWD ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 TWD，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":5561413.97,"period":"2026-10-17","unit":"TWD m","basis":"yfinance revenue_estimate 0y 平均（41 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-17"},"note":"財報幣別 TWD ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 TWD，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":7647456.61,"period":"2026-10-17","unit":"TWD m","basis":"yfinance revenue_estimate +1y 平均（41 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-17"},"note":"財報幣別 TWD ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 TWD，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"TrendForce 資料顯示 TSMC 全球晶圓代工市佔率在 2026 Q2 攀升至歷史新高 72.5%（Q1 為 72.3%），三星以 5.9% 居次，兩者差距擴大至 12.3 倍；2nm 首季貢獻營收，帶動出貨量與 ASP 同步上升。","source":"techsoda substack, \"Global Market Watch: TSMC's Global Foundry Market Share Inches Up to 72.5%\", https://techsoda.substack.com/p/global-market-watch-tsmcs-global","url":null,"excerpt":null,"as_of":"2026-09-10","retrieved_at":"20261017","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"英特爾在川普政府公開表態支持其代工野心後，被視為對三星代工復甦計畫的新威脅；三大廠（台積電、三星、英特爾）皆已進入 2nm 量產階段，先進製程需求量已達台積電可供產能的 110–120%，代表三星與英特爾不需搶下台積電客戶即可受惠，只要能承接台積電產能不足的溢出需求。","source":"Semiwiki, \"TSMC vs Intel Foundry vs Samsung Foundry 2026\", https://semiwiki.com/semiconductor-manufacturers/tsmc/366523-tsmc-vs-intel-foundry-vs-samsung-foundry-2026/","url":null,"excerpt":null,"as_of":"2026-06-19","retrieved_at":"20261017","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"華爾街日報於 2026 年 5 月報導，Apple 與 Intel Foundry Services 已達成初步協議，Apple 將以 Intel 18A 製程（電晶體密度與電性可比台積電 2nm 級製程）生產部分 Apple Silicon 晶片，可能結束 Apple 近乎完全依賴台積電代工的局面；Apple 仍自行設計晶片，Intel 僅負責製造。","source":"Investing.com, \"Apple-Intel Chip Manufacturing Deal Reshapes Foundry Race\", https://www.investing.com/analysis/appleintel-chip-manufacturing-deal-reshapes-foundry-race-200682398","url":null,"excerpt":null,"as_of":"2026-06-18","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Apple(蘋果，TSM 長期最大單一客戶)正探索讓部分低階處理器改由 TSMC 以外廠商生產，與 Intel、Samsung 進行早期洽談；Intel 18A-P 製程(預計 2026 年底量產)被視為 2016 年 Apple 離開 Samsung 以來第一個理論上可行的替代方案，但分析師認為 Intel 短期內較可能是策略備援或低量次要供應商，而非主力代工廠。","source":"MacRumors, 'Apple May Break a 10-Year Chip Strategy' (引述 Wall Street Journal 報導)","url":null,"excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261017","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Apple 近年持續擴大自研晶片(insourcing)範圍，含 M 系列處理器與自製 C1/C1X 蜂巢數據機，晶片設計團隊擴增至數千工程師；但這是 Apple 把設計從第三方晶片商(如 Qualcomm)收回自研，成品仍需委外晶圓代工，未見明確跡象顯示 Apple 打算自建先進製程晶圓廠取代 TSMC 的代工角色。","source":"CNBC, 'Apple's elevation of silicon head Johny Srouji signals sprint to build in-house chips for all devices'","url":null,"excerpt":null,"as_of":"2026-04-21","retrieved_at":"20261017","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"TSMC's ten largest customers accounted for 78% of FY2025 net revenue, up from 76% in FY2024; the single largest customer accounted for roughly 19% of FY2025 revenue (up from 12% in FY2024).","source":"TSMC 2025 Annual Report (20-F) customer concentration disclosure, summarized by StockTitan (https://www.stocktitan.net/sec-filings/TSM/20-f-taiwan-semiconductor-manufacturing-co-ltd-files-annual-report-fo-e7792df70159.html) and ExploreSemis (https://exploresemis.substack.com/p/tsmcs-top-10203040-customers-who)","url":null,"excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261017","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Nvidia overtook Apple to become TSMC's largest customer in FY2025 (~19% of revenue, up from 12% in FY2024), while Apple's share fell to ~17% from 22%.","source":"MacRumors, \"Nvidia Overtakes Apple as TSMC's Biggest Customer\" (https://www.macrumors.com/2026/01/28/nvidia-replaces-apple-as-biggest-tsmc-customer/); CNBC (https://www.cnbc.com/2026/01/26/nvidia-set-to-supplant-apple-as-tsmcs-largest-customer.html)","url":null,"excerpt":null,"as_of":"2026-01-26","retrieved_at":"20261017","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"S&P Global Ratings upgraded Nvidia's credit rating from 'AA-' to 'AA', citing strong AI-driven growth; this follows an earlier upgrade from 'A+' to 'AA-' on 2024-04-30. TSM's largest customer's credit profile is strengthening, not deteriorating.","source":"S&P Global Ratings, \"Nvidia Corp. Upgraded To 'AA' On Strong AI-Driven...\" (https://www.spglobal.com/ratings/en/regulatory/article/-/view/type/HTML/id/3579353); Yahoo Finance (https://finance.yahoo.com/markets/stocks/articles/p-global-ratings-upgrades-nvidia-211417548.html)","url":null,"excerpt":null,"as_of":"2026-06-11","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TSMC執行長C.C. Wei表示，AI晶片短缺可能持續到2027年及更後期；他指出新建晶圓廠需要2-3年，擴建產能還要再1-2年，沒有捷徑，顯示此為結構性而非短期週期性缺口","source":"TweakTown, 'TSMC can't keep up with AI chip demand, with shortages projected to last beyond 2027' (引用 eetimes.itmedia.co.jp)","url":null,"excerpt":null,"as_of":"2026-04-21","retrieved_at":"20261017","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Broadcom警示2026年晶片供應吃緊，TSMC先進封裝(CoWoS)產能為次要瓶頸，2025年底排定的產能擴充恐無法在短期內緩解壓力，分析師建議客戶重新檢視長期供應合約，暗示屬中期結構性問題而非單純週期性","source":"Astute Group, 'Broadcom flags 2026 chip supply squeeze as TSMC capacity tightens under AI demand'","url":null,"excerpt":null,"as_of":"2026-03-24","retrieved_at":"20261017","affects":["moat_trend","thesis.H","triggers"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Nvidia約佔TSMC CoWoS先進封裝產能近60%，已鎖定TSMC 2026-2027年CoWoS擴產計畫的一半以上；前三大客戶(Nvidia、Broadcom、AMD)合計控制超過85%產能，3奈米製程為業界最搶手的稀缺資源，三星與Intel在3奈米進度上明顯落後","source":"Sanie Institute, 'The Wafer Allocation Decision No Foundry Customer Can Postpone'","url":null,"excerpt":null,"as_of":"2026-01","retrieved_at":"20261017","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"全球晶片投資過去多年集中投向先進製程(3奈米、2奈米、未來1奈米)，成熟製程投資相對不足，但電動車、再生能源、醫療、國防等領域對成熟製程晶片的依賴仍在上升，形成結構性錯配而非單純景氣循環","source":"SemiWiki forum, 'Global semiconductor market faces shortages as AI demand strains supply chains'","url":null,"excerpt":null,"as_of":"2026","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美國對特定先進邏輯半導體課徵 25% Section 232 關稅，2026-01-15 生效；同日美台框架協議約定，台灣廠商在美新建產能可豁免此關稅，直接惠及 TSMC 亞利桑那擴廠（12 座廠、1650 億美元投資承諾）。","source":"EY Global Tax News, 'US Section 232 proclamation imposes 25% tariff on certain semiconductors'; Global Policy Watch, 'A Month in Semiconductor Policy'","url":null,"excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"美國商務部核發 TSMC 南京廠一年期年度出口許可（取代 2025-12-31 到期的 VEU 資格），允許美製晶片製造設備持續供應南京廠，免逐案審批；南京廠為成熟製程（16nm 及以上），約占 TSMC 整體營收 2.4%。","source":"CNBC, 'U.S. grants TSMC annual licence to import U.S. chipmaking tools into China'; Benzinga, 'TSMC Secures One-Year US Export License'","url":null,"excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"台灣政府於 2026 年 6 月研議收緊 AI 晶片對中國出口管制，擬將限制範圍從僅涵蓋華為等受制裁對象擴大至所有中國客戶，並首度賦予刑事追訴權；若定案將限縮 TSMC 對中國先進製程客戶的銷售，尚未拍板。","source":"Bloomberg, 'Taiwan Weighs Tighter AI Chip Export Controls Targeting China to Align with US'; UPI, 'Taiwan weighs tighter rules for AI chip exports to China'","url":null,"excerpt":null,"as_of":"2026-06-09","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"台灣生產全球約92%的最先進邏輯晶片（5奈米以下），台積電先進製程產能高度集中在台灣本島，海外廠（美國亞利桑那、日本、歐洲）尚無法承接同等先進製程規模。","source":"Simply Wall St News, 'Blockade Risk Puts TSMC's Taiwan Hub And Tech Supply Chain In Focus'","url":null,"excerpt":null,"as_of":"2026-05-20","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"台積電亞利桑那廠在2027年前是其海外唯一具備先進邏輯製程（5奈米以下）量產能力的據點，海外產能達到有意義規模預計要到2028年以後才會出現，短中期地緣風險仍高度集中於台灣。","source":"Simply Wall St News（彙整報導，同上主題）","url":null,"excerpt":null,"as_of":"2026-05-20","retrieved_at":"20261017","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"晶片製造耗電量約占台灣全國總發電量18%，台灣本地電力供應若不穩定，可能直接影響在製晶圓批次良率與交期，成為供應鏈單點失效的具體傳導管道之一。","source":"Simply Wall St News, 'Taiwan Semiconductor Puts Global Tech Supply Chains Under Geopolitical Scrutiny'","url":null,"excerpt":null,"as_of":"2026-05-20","retrieved_at":"20261017","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"美、歐、日政府正合計規劃約2000億美元投資以分散半導體供應鏈地理集中度，但進度緩慢，市場評估風險與韌性之間的落差至少要到2028年才會顯著收斂。","source":"Simply Wall St News（彙整報導，同上主題）","url":null,"excerpt":null,"as_of":"2026-05-20","retrieved_at":"20261017","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"TSMC HPC (High Performance Computing) platform grew 20% QoQ in Q2 2026 to reach 66% of total revenue ($40.20B quarterly revenue), driven by AI/cloud accelerator demand.","source":"Investing.com, 'TSMC Q2 2026 slides: AI demand drives record margins, HPC surges 20%'","url":null,"excerpt":null,"as_of":"2026-07-17","retrieved_at":"20261017","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"TSMC raised FY2026 revenue growth guidance to 'slightly above 40%' YoY in USD terms (up from prior guidance of 'more than 30%'), and raised 2026 capex target to $60-64B, citing sustained AI accelerator demand and faster advanced-node ramps.","source":"Bloomberg, 'TSMC Hikes Sales, Spending Outlook to Catch AI Megatrend'","url":null,"excerpt":null,"as_of":"2026-07-16","retrieved_at":"20261017","affects":["thesis.H","valuation","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Smartphone platform revenue rose 11% QoQ in Q4 2025 to 32% of quarterly revenue; full-year 2025 smartphone platform revenue grew 11% YoY.","source":"TSMC 4Q2025 earnings management report / transcript (investor.tsmc.com)","url":null,"excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261017","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"IoT platform revenue rose 3% QoQ in Q4 2025 to 5% of quarterly revenue; full-year 2025 IoT platform revenue grew 15% YoY.","source":"TSMC 4Q2025 earnings management report / transcript (investor.tsmc.com)","url":null,"excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261017","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"Automotive chip demand is showing a 2026 recovery across smart cockpit, ADAS, analog IC and display-driver IC segments among Taiwan IC design firms and foundry customers, but near-term recovery pace is being constrained by macro headwinds (tariffs, interest rates, energy costs); long-term automotive semiconductor outlook remains positive.","source":"Digitimes, 'Taiwan chip designers see automotive demand rebound'","url":null,"excerpt":null,"as_of":"2026-08-20","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#none","axis":"substitute_technology","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"台積電首度將部分 CoWoS 先進封裝製程委外給專業封測廠（OSAT，日月光投控、矽品等），因 CoWoS 產能仍追不上 AI 晶片需求缺口；此前 CoWoS 幾乎全數自製，屬供應/生產模式的結構性轉變。","source":"壹蘋新聞網《CoWoS擴產仍追不上需求！台積電歡迎替代方案 OSAT喜迎外溢商機》 https://news.nextapple.com/finance/20260816/9A442EB83257B351C3CEF24B8EC35606","url":null,"excerpt":null,"as_of":"2026-08-16","retrieved_at":"20261017","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026年CoWoS市場需求估達約100萬片，台積電最多可供應約60至70萬片，缺口延續至2027年底，帶動日月光等OSAT廠承接外溢訂單（含CPO、Fan-out、SiP等技術）。","source":"TechNews 科技新報《台積電 CoWoS 先進封裝擴產仍難滿足市場，OSAT 業者持續受惠外溢訂單》 https://finance.technews.tw/2026/01/29/tsmcs-cowos-advanced-packaging-capacity-expansion-still-falls-short-of-market-demand/","url":null,"excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261017","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"台積電正將先進封裝技術從單一 CoWoS 擴展為多技術陣列（2.5D CoWoS、扇出型 InFO、3D SoIC），公司角色從純晶圓代工延伸至封裝平台整合商；CoWoS 產能至2026年底將擴增至月產13萬片規模，訂單已全數售罄至2026年底。","source":"Troy Technical《TSMC CoWoS Advanced Packaging Becomes Critical Bottleneck in AI Chip Supply, Sold Out Through 2026》 https://troy-technical.com/2026/08/09/tsmc-cowos-advanced-packaging-becomes-critical-bottleneck-in-ai-chip-supply-sold-out-through-2026/","url":null,"excerpt":null,"as_of":"2026-08-09","retrieved_at":"20261017","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"TSMC 3Q26 營收 46.72B 美元（年增 41.2%），高於自家指引 44.6–45.8B 上緣；毛利率 66.4%，落在 65–67% 指引內","source":"TSMC 3Q26 Earnings Release / HL share research","url":"https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-10/526b65af7305df2dde6b9ece6812b1fdf1e49f9b/3Q26%20EarningsRelease.pdf","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261017","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"TSMC 對 4Q26 營收指引 52.3–54.3B 美元（匯率假設 31.8 NTD/USD）","source":"TSMC 3Q26 Earnings Release (SEC 6-K)","url":"https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000726/a3q26e_withguidancexfinal.htm","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261017","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"7 月 2Q26 法說：全年 2026 營收成長指引由 >30% 上調至略高於 40%，資本支出上調至 60–64B 美元，明顯高於法說前共識 53.6B；S&P 稱高 capex 壓抑市場情緒","source":"S&P Global Market Intelligence, Research — July 21, 2026","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/07/tsmc-postq-ai-drives-beat-outlook-raised-higher-capex-weighs-on-sentiment","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261017","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Hudson Labs 3Q26 預覽：共識營收約 45.8B vs 指引 44.6–45.8B（指引中點略低於共識）；毛利率指引 65–67% vs 共識 66.5%；單一來源，另有來源稱 3Q 指引高於共識，方向互相矛盾","source":"Hudson Labs, TSMC (TSM) Earnings Preview: Q3 2026","url":"https://www.hudson-labs.com/research/tsmc-q3-2026-earnings-preview-tsm-revenue-and-margins","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"目標價聚合：TickerLeague 共識目標價約 $586（中位 $600，區間 $480–$700，4 位分析師）；TickFlow 平均 $520（區間 $450–$700，僅 2 位）；樣本很少、兩站不一致、日期約 8 月","source":"TickerLeague / TickFlow 聚合頁","url":"https://tickerleague.com/companies/TSM/estimates","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"路透2025-04報導：TSMC 因一顆晶片流入華為 AI 處理器（涉 Sophgo），可能面臨 US$10 億以上的美國出口管制罰款；消息來自匿名人士。TSMC 表示自2020年9月中旬起未供貨華為並配合商務部。搜尋未找到 2026 年後續（無正式指控或罰款）。發布日早於近12個月窗口，列為仍未結案的監管事項。","source":"Reuters via SCMP/Yahoo Finance/Business Today：TSMC could face $1b or more fine in US export control probe","url":"https://finance.yahoo.com/news/tsmc-could-face-1b-us-193911645.html","excerpt":null,"as_of":"2025-04-09","retrieved_at":"20261017","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2025-08 TSMC 表示已對涉及潛在營業秘密外洩的員工啟動法律程序並採取懲處（二手來源摘要，未取得原文）。","source":"搜尋摘要（Nasdaq／二手站）","url":null,"excerpt":null,"as_of":"2025-08-01","retrieved_at":"20261017","affects":["moat_trend"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"TSM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.23,"operating_margin_pct":56.1,"fcf_margin_pct":25.33,"rd_intensity_pct":6.07},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSM","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"NVDA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.67,"operating_margin_pct":65.21,"fcf_margin_pct":41.92,"rd_intensity_pct":7.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AMD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":53.2,"operating_margin_pct":15.71,"fcf_margin_pct":20.34,"rd_intensity_pct":22.74},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MU","period":"TTM ending 2026-05-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.57,"operating_margin_pct":65.67,"fcf_margin_pct":28.99,"rd_intensity_pct":5.3},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU","as_of":"TTM ending 2026-05-31（4季加總）"}}],"subject":"TSM"},"financial_history":{"ticker":"TSM","currency":"TWD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":2263891300000.0,"revenue_yoy_pct":null,"gross_margin_pct":59.56,"operating_margin_pct":49.53,"net_income":992923400000.0,"diluted_eps":196.0,"free_cash_flow":520972800000.0,"fcf_margin_pct":23.01,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":2161735800000.0,"revenue_yoy_pct":-4.51,"gross_margin_pct":54.36,"operating_margin_pct":42.62,"net_income":851740000000.0,"diluted_eps":161.7,"free_cash_flow":286568900000.0,"fcf_margin_pct":13.26,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2894307700000.0,"revenue_yoy_pct":33.89,"gross_margin_pct":56.12,"operating_margin_pct":45.68,"net_income":1158380200000.0,"diluted_eps":226.25,"free_cash_flow":861195500000.0,"fcf_margin_pct":29.75,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":3809054300000.0,"revenue_yoy_pct":31.61,"gross_margin_pct":59.89,"operating_margin_pct":50.83,"net_income":1697604000000.0,"diluted_eps":331.25,"free_cash_flow":992378400000.0,"fcf_margin_pct":26.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TSM/TSM_Q3_2026_Earnings_Call_20261015.md）

# Q3 2026 Earnings Call
**Taiwan Semiconductor Manufacturing Company Limited** | Earnings Calls | 2026-10-15

**Jeff Su** (Executives):
Good afternoon, everyone, and welcome to TSMC's Third Quarter 2026 Earnings Conference Call. This is Jeff Su, TSMC's Director of Investor Relations and your host for today. TSMC is hosting our earnings conference call via live audio webcast through the company's website at www.tsmc.com, where you can also download the earnings release materials. [Operator Instructions] The format for today's event will be as follows: First, TSMC's Senior Vice President and CFO, Mr. Wendell Huang, will summarize our operations in the third quarter 2026, followed by our guidance for the fourth quarter 2026. 
Then Mr. Huang and TSMC's Chairman and CEO, Dr. C.C. Wei, will jointly provide the company's key messages. That will be followed -- then we will open the line for the Q&A session. As usual, I would like to remind everybody that today's discussions may contain forward-looking statements that are subject to significant risks and uncertainties, which could cause the actual results to differ materially from those contained in the forward-looking statements. Please refer to the safe harbor notice that appears in our press release. And now I would like to turn the call over to TSMC's CFO, Mr. Wendell Huang, for the summary of operations and the current quarter guidance.

**Jen-Chau Huang** (Executives):
Thank you, Jeff. Good afternoon, everyone. Thank you for joining us today. My presentation will start with financial highlights for the third quarter of 2026. After that, I will provide the guidance for the fourth quarter of 2026. Third quarter revenue increased 17.6% sequentially in TWD, supported by strong demand for our leading-edge process technologies. In U.S. dollar terms, revenue increased 16.2% sequentially to $46.7 billion, above the high end of our third quarter guidance. Gross margin decreased by 1.3 percentage points sequentially to 66.4%, primarily due to margin dilution from 2-nanometer ramp. 
Total operating expenses accounted for 7.8% of net revenue. Operating margin was 58.7%. Overall, our third quarter EPS reached TWD 29.43 and ROE was 45.5%. Now let's move on to revenue by technology. 2-nanometer process technology contributed 8% of wafer revenue in the third quarter, while 3-nanometer, 5-nanometer and 7-nanometer accounted for 33%, 28% and 10%, respectively. Advanced technologies, defined as 7-nanometer and below, accounted for 79% of wafer revenue. 
Moving on to revenue contribution by platform. HPC increased 22% quarter-over-quarter to account for 68% of our third quarter revenue. Smartphone increased 10% to account for 21%. IoT increased 5% to account for 4%. Automotive increased 23% to account for 4%, while DCE declined 12% to account for 1%. Moving on to the balance sheet. We ended the third quarter with cash and marketable securities of TWD 4 trillion or USD 126 billion. On the liability side, current liabilities increased by TWD 110 billion quarter-over-quarter, mainly due to the increase of TWD 46 billion in current portions of bond payable and bank loans and TWD 26 billion in dividend payable. 
In terms of financial ratios, accounts receivable turnover days decreased by 1 day to 28 days. Inventory days decreased by 5 days to 82 days, primarily due to the increase in wafer shipment. Regarding cash flow and CapEx. During the third quarter, we generated about TWD 920 billion in cash from operations, spent TWD 443 billion in CapEx and distributed TWD 156 billion for fourth quarter 2025 cash dividends. 
Overall, our cash balance increased TWD 488 billion to TWD 3.6 trillion at the end of the quarter. In U.S. dollar terms, our third quarter capital expenditures totaled $13.8 billion. I have finished my financial summary. Now let's turn to our current quarter guidance. Based on the current business outlook, we expect our fourth quarter revenue to be between USD 52.3 billion and USD 54.3 billion, which represents a 14% sequential increase or a 58% year-over-year increase at the midpoint. 
Based on the exchange rate assumption of USD 1 to TWD 31.8, gross margin is expected to be between 65% and 67%, operating margin between 56.5% and 58.5%. This concludes my financial presentation. Now let me turn to our key messages. I will start by talking about our third quarter '26 and fourth quarter of '26 profitability. Compared to second quarter, our third quarter gross margin decreased by 130 basis points sequentially to 66.4%, primarily due to the margin dilution from the initial ramp-up of our 2-nanometer technology. 
We have just guided our fourth quarter gross margin to decrease by 40 basis points to 66% at the midpoint, primarily due to the continued margin dilution from the steep ramp-up of our 2-nanometer technology as well as dilution from overseas fabs. These impacts are expected to be partially offset by cost improvement efforts, including productivity gains and across node capacity optimization. While the cost of overseas fabs remain higher, thanks to the company's overall larger scale and cost improvement efforts, we now expect the gross margin dilution from the ramp-up of our overseas fabs to be closer to 2% for the full year 2026. 
As we put more effort to support the strong structural demand from our customers, more fabs will be ramping up in the U.S. Thus, we expect the dilution from our overseas fabs to widen to 3% to 4% in the next few years. We will leverage our increasing size in Arizona and work on our operations to improve the cost structure. We will also continue to work closely with our customers and suppliers to manage the impact. Overall, with our fundamental competitive advantages of manufacturing technology leadership and large-scale production base, we are confident that TSMC continues to be the most cost-efficient manufacturer in every region that we operate. 
Next, let me make some comments on our 2026 capital budget. At TSMC, a higher level of capital expenditures is always correlated with higher growth opportunities in the following years. Given the continued robust multiyear demand from our customers, including the emerging Agentic AI market, we reiterate our full year 2026 capital budget to be between USD 60 billion and USD 64 billion. We continue to expect our CapEx dollars investment from 2026 to 2028 to be even more significantly higher than the past 3 years as we continue to invest heavily to support our customers' growth. 
Additionally, while the tool supply is tight, we always collaborate closely with our tool suppliers well in advance to prepare the capacity, just like our customers collaborate with us well in advance to plan our capacity. Even as we invest for the future growth with this level of CapEx spending in the next few years, we remain committed to delivering profitable growth to our shareholders. We also remain committed to a sustainable and steadily increasing cash dividend per share on both an annual and quarterly basis. Now let me turn the microphone over to C.C.

**C.C. Wei** (Executives):
Thank you, Wendell. Good afternoon, everyone. First, let me start with our near-term demand outlook. We concluded our third quarter with a revenue of USD 46.7 billion higher than our guidance in U.S. dollar terms, driven by strong demand for our leading-edge process technologies. Moving into fourth quarter 2026, we expect our business to be supported by continued strong demand for our leading-edge process technologies, including the steep ramp-up of our 2-nanometer technology. 
Looking ahead, we continue to observe consumer and price-sensitive end market segment are being challenged due to the impact of rising component prices and macroeconomic uncertainties. As such, we are being prudent in our business planning going into 2027, while focusing on the fundamentals of our business to further strengthen our competitive position. Having said that, demand for our leading-edge technologies continue to be extremely robust, supported by our strong technology differentiation and broad customer base. Therefore, we now expect our full year 2026 revenue growth to be around 44% year-over-year in U.S. dollar terms. 
Next, let me talk about the AI-related demand outlook. The AI market continues to be very strong. Recent developments are very positive to AI's long-term demand outlook. We observe increasing AI demand fueled by the rising adoption of Agentic AI as we transition from chatbot to AI assistants. In addition, we are observing great adoption of open source AI models. This will drive greater efficiency and help lower the barrier to future AI usage and result in more and more demand for leading-edge silicon. 
AI-related demand is being supported by strong underlying demand for AI accelerators. In addition, the emergence of Agentic AI, CPUs and the continued demand for networking chips are driving further silicon demand. Therefore, semiconductor will remain essential in the AI megatrend. The value of semiconductors in the global supply chain is set to continue to increase in our view. This will create more value opportunities for our customers to capture and more value opportunities for TSMC as well. 
No matter which approach is taken, it will require use of the most advanced semiconductor process technology. With our technology leadership, manufacturing excellence, global capacity expansion and customer trust, we are well positioned to capture the full multiyear structural AI-related demand. Therefore, all the AI players are working with TSMC. 
Next, let me talk about TSMC's capacity expansion strategy. As a foundry, our first responsibility is to provide our customers with the best technologies and effective capacity support to unleash their innovations. To address the structural increase in the long-term semiconductor market demand profile, TSMC collaborated closely with our customers and our customers' customers to plan for our capacity. In addition, we are now going one step further and sending our own teams of people to check on the data center build-out progress and power supply situation in the U.S. 
The feedback is so far so good, and the CSPs has been well prepared. Internally, TSMC employed a disciplined capacity planning system to assess the market demand from both a top-down and bottom-up approach. This is a continuous and ongoing process. Given the fundamental complexity of leading-edge technologies and the design-in and lead time involved, we already have a very good idea of customers' multiyear product road map and production plans. Thus, we continue to hold strong conviction in the AI megatrend. 
We are moving full speed ahead to increase our capacity to meet our assesses demand and stepping up our CapEx investment to support our customers' future growth. TSMC is expanding at an unprecedented pace with a near 20 fabs worldwide in progress. We are building 13 leading edge and advanced packaging fab in Taiwan over the next several years and another 5 to 6 fabs overseas. Our new node, N2 has already entered high-volume manufacturing in the fourth quarter of 2025 with good yield. N2 is ramping successfully in multiple phases at both Hsinchu and Kaohsiung site. 
We expect our N2 family technologies annual capacity to more than double in 2027, supported by strong demand from both smartphone and HPC AI applications. We are also leveraging our manufacturing excellence to generate more N2 wafer output, further increasing our capacity support to customers. In addition, we have already begun preparing the capacity for our A14 technology. Risk production is well on track for 2027 and volume production will start in 2028. Thus, TSMC's semiconductor technologies and manufacturing will continue to play a pivotal role in supporting the global semiconductor industry while unleashing our customers' innovation. 
Now let me talk about TSMC's global N3 capacity expansion update. As we said before, historically, we do not add additional capacity to a node once it reaches its targeted capacity. However, based on our assessment, we are executing well on our global capacity plan to add 3 new fabs to support a robust multiyear pipeline of demand for 3-nanometer technologies. In Taiwan, volume production for our new 3-nanometer fab in Tainan Science Park is well on track to begin the first half of 2027. 
In addition, driven by the strong demand from our customer, we have decided to add one additional 3-nanometer fab in Tainan. Volume production is scheduled for the first half of 2028. In Arizona, we have completed the construction of our second fab and are in the process of tool moving and installation. Volume production will begin in third quarter '27, slightly ahead of our previous schedule. In Japan, we are progressing well to our plan to utilize 3-nanometer in our second fab and volume production is scheduled in 2028. In addition to all the new fabs, we continue to convert 5-nanometer tool to support 3-nanometer capacity in Taiwan. We are also leveraging our manufacturing excellence to greater productivity across our fab in all locations to generate more wafer output. 
We are also focusing on capacity optimization across nodes, which including flexible capacity support among N7, N5 and N3 node. Thus, we are using multiple levers to do everything we can whenever we can, as fast as we can to maximize the support to our customers. We have no intention to leave food on the table for others, and we want to capture every piece of business possible. This is concluding our key message, and thank you for your attention.

**Jeff Su** (Executives):
Thank you, C.C. This concludes our prepared statements. [Operator Instructions] Now let's begin the Q&A session. Operator, can we proceed with the first caller on the line, please?

**Operator** (Operator):
Yes. First one, Laura Chen, Citi.

**Chia Yi Chen** (Analysts):
I appreciate C.C. for sharing with us the TSMC capacity expansion strategy. So may I follow up more on that given the increasing aggressive AI semiconductor demand, how does TSMC now see the AI revenue CAGR growth? And how does TSMC reconcile customers' capacity requirements with some of the potential concern on the data center power availability and also maybe funding recently and other critical components such as HBM, ABF advanced packaging and also in the networking side, we see the tightness of laser as well. So if these kind trends create a mismatch between semiconductor supply and also actual AI development, how would TSMC adjust your capacity allocation and also the strategy to minimize the potential overbuilding in the supply chain? That's my first question.

**Jeff Su** (Executives):
Okay, Laura. Laura has a very involved first question. I think she's asking how do we see the AI demand outlook? The AI demand, as C.C. said, seems to be very strong, but she's worried or concerned. How do we reconcile the strong demand of chips, AI chips versus risks related to whether it be power supply, I think also like different bottlenecks within the supply chain, et cetera. How do we make our assessment of what is the appropriate CapEx and capacity we need to prepare? Is that correct, Laura?

**Chia Yi Chen** (Analysts):
Yes. Thank you.

**C.C. Wei** (Executives):
That's a long, long question. Laura, let me share with you. We have a very sophisticated capacity planning process, and we also have a very disciplined on our consideration. And let me share with you, we put every possibility we can talking about the CSP's CapEx, data centers build-out, financial, power supply and also other component supply, et cetera, into our consideration. And so we make our own judgment. And then based on our assessment the demand, we still think the demand is higher than the supply, and we are working very hard to narrow the gap. Did I answer your question, Laura?

**Chia Yi Chen** (Analysts):
Sure. Thank you very much. So far from our -- like a comprehensive study in the supply chain, we are still quite positive on the demand in the longer term, right? So in that case, can you also give us like more color about that what -- any update on your AI CAGR growth? I recall previously, we're talking about like high 50%.

**Jeff Su** (Executives):
Yes. So part of Laura's question is then based on our assessment, we had previously guided our AI CAGR -- AI accelerator CAGR, which is a narrow definition to grow mid- to high 50s percentage from 2024 to 2029. So Laura wants to know, do we have any update to that number today?

**C.C. Wei** (Executives):
Laura, all I can say right now is the demand is very extremely robust, okay? And we did not see any sign of slowdown. Whether it's a high 50 CAGR, it doesn't matter. It probably will be higher.

**Chia Yi Chen** (Analysts):
Okay. Thank you very much. Yes. And my second question is also about like the -- given the very strong demand, the CapEx cycles, we see that definitely this round will be much higher than before. And TSMC also announced that earlier, you will adopt a High-NA EUV around 2030. So should we think about that, that will be further improved the productivity that will be more meaningful for further like accelerating revenue growth in the longer term? And also given that the CapEx intensity are also getting much higher. So how should we think about that the pricing power and also the long-term gross margin and the capital efficiency returns? That's my...

**Jeff Su** (Executives):
Okay. That's actually 2 questions, but okay, just very quickly. So part of it is on with the strong demand and our CapEx cycle, how do we view the adoption of High-NA, which we said we will in 2030? And then her question is on profitability, long-term outlook.

**C.C. Wei** (Executives):
Okay. Let me answer that question. Yes, for the long-term productivity, we continue to improve it and High NA definitely is a very good tool. And so far, I think our plan is to use it in 2030. Again, our CapEx will be much higher than today. And so you're talking about the gross margin or the profitability can be increased or not. Let me say that. There's no ceiling for TSMC's profitability, but a dramatic increase will not happen overnight either. So our philosophy or our strategy always working with our customer, and we want to make them be successful and then we can get our value.

**Jeff Su** (Executives):
Operator, can we move on to the next participant, please?

**Operator** (Operator):
Next one, Gokul Hariharan, JPMorgan.

**Gokul Hariharan** (Analysts):
My first question, again, on capacity addition. It looks like the shortage situation next year could be even more than 2026. Just wanted to hear C.C. your view on this. And I think it's been quite some time since we have seen TSMC add capacity at more than 10% every year. I think if you look at your annual report, you see like about 10 years that you have added capacity at more than 10%. Given this accelerated build-out, can we start getting wafer capacity growth closer to 10% or even higher than 10% in the next couple of years? Any comment on like what is your planned wafer capacity growth in the next couple of years? That's my first question.

**Jeff Su** (Executives):
Okay. So Gokul's first question is regarding the capacity addition and the demand. So -- his question first is the tightness in the wafer supply, do we think that will be even more or greater in 2027 than 2026? And then along with that, how do we see our overall capacity addition? Although you say 10%, I think every year we disclosed in the annual report, it's been about mid- to high single digit and sometimes even lower. But anyways, regardless, those are the 2 questions. So first, on just the demand outlook and then the supply, will next year be even more tight than this year?

**C.C. Wei** (Executives):
I guess I mentioned the demand is extremely robust and getting higher and higher. Of course, we have our own judgment, and we look at every angle. As I said, we talk to customer, customers and customer, and then we do our own one more step to check the data centers build-out. All the results we put into our judgment and our assessment, the result is the demand is very, very high. And so the gap between demand and supply are still quite big, and that's why we put all our strengths to increase the capacity, as I just mentioned. Whether it's bigger or the gap become bigger or the gap become narrower, we are working very hard. I cannot answer this question right now because my customers continue to increase their demand.

**Jen-Chau Huang** (Executives):
Okay. Gokul, I think it's a bit too early to talk about capital capacity increase percentage going forward. But let me just remind you that the increase every year, although the number is -- even though the number may be small, but the increase in advanced packaging -- sorry, advanced nodes are really the main driver for the capacity increase, okay?

**Gokul Hariharan** (Analysts):
Fair enough. Okay. Secondly, could you -- I think you alluded to more aggressive overseas expansion plans in the U.S., especially. And I think recently, there's been a lot of discussion with potentially a new fab cluster in Texas as well as I think one of your customers also talked about discussions with TSMC as well. So C.C., could you talk a little bit about your overseas plans, like the more accelerated kind of capacity build-out? And also any engagement with SpaceX or Tesla, given your customer did call you out last week in terms of some engagements you have? Like what are the broad contours of this kind of engagement likely to be? Is it similar to what you've done with some of the customers in Japan and ESMC as well?

**Jeff Su** (Executives):
Okay. Thank you, Gokul. So Gokul's second question, he notes that C.C. said, we're expanding at an unprecedented place, doing everything we can as fast as we can to increase the capacity. So this question is particularly to the U.S. What is the status or update? There's been reports that we are looking to expand in Texas. There's been reports that one of our customers, we are engaging in discussions. He wants to know what kind of framework or parameters of any cooperation may be or any comment on either of those 2 things?

**C.C. Wei** (Executives):
Okay. Gokul, -- we work very hard to expand our capacity in U.S. This is necessary because of all our customers, most of our large customer in U.S. and they requested TSMC to increase the capacity. And also U.S. government are very helpful. So that's a place we want to expand. So recently, we did expand our capacity consideration to see outside Arizona, whether we can get another chance to expand our capacity. And Texas is one. So we send the teams to Texas to do all the evaluation. And we also talked to one of our customers who try to build a fab, Terafab, let me be more specific. And we discuss with them to see whether that we can be utilizing that actual capacity also. So we joint discussion, if we have any solid conclusion, we'll share with you. But today, and that's it, yes, from Arizona to Texas, yes.

**Gokul Hariharan** (Analysts):
Okay. But all these are going to be TSMC run fabs, right? I think you're not becoming part of the fab project or anything like that. Could you just help us understand what are the principles that you're using here? Is it the similar principles that you use for JASM or ESMC?

**Jeff Su** (Executives):
Okay. So Gokul's question is in particular to the potential cooperation with this customer. Would it be [ TSMC own? ] What's the principles that we have, if anything?

**C.C. Wei** (Executives):
We are still in discussion. Let me say that. It's not either way, it will be possible, but the fab got to be run by TSMC.

**Jeff Su** (Executives):
Operator, can we move on to the next participant, please?

**Operator** (Operator):
Yes. Next one, Krish Sankar, TD Cowen.

**Sreekrishnan Sankarnarayanan** (Analysts):
I have 2 of them. First one, C.C. some customers talk about a secondary wafer market where one customer passes their wafer allocation to another. Is this like a very small portion of the business? Is it customer specific? Or do you see that as an emerging trend where customers whose demand is we pass some of the allocation to stronger customers? And then I had a quick follow-up.

**Jeff Su** (Executives):
All right, Krish. Thank you. So Krish's first question is asking some of our customers are talking about a resell a secondary wafer market where they can pass their allocation on. So is this a very small portion of our business? Or is this more of a trend for us to do? And is this something that we allow our customers to do?

**C.C. Wei** (Executives):
Well, let me answer that. To say whether this is a new strategy, new methodology, the answer is no. The principle of TSMC is we do not allow our customer to sublet or auction of the capacity. But in certain cases, customers can collaborate through a mask licensing agreement, but this is not our common practice. And the amount is very, very small. Krish, did I answer your question?

**Sreekrishnan Sankarnarayanan** (Analysts):
Yes. And then a quick follow-up. You did touch upon it the High-NA agreement with ASML from 2030 onwards. I'm just curious, historically, TSMC was more ahead of the curve with the EUV adoption. It looks like by the time you adopt High-NA EUV will be 2030, 2031, but some of your competitors have already been using it by then. So do you see that as a disadvantage? Or you're not worried about competition getting ahead with High-NA EUV?

**Jeff Su** (Executives):
Okay. So Krish's second question is looking at High-NA. He notes some of our competitors are both using -- already adopted or will adopt High-NA earlier than TSMC. So his question, does this put us at a competitive disadvantage or risk compared to our competitors in terms of technology leadership?

**C.C. Wei** (Executives):
Krish? Let me answer that. We always evaluate a new tool. And if we want to put into the mass production, it got to be the best technology with a very reasonable cost and most important is the best maturity, okay? So we say in 2030, we'll start to use it because we also think at that time, High-NA will be mature. And we're also working very closely with ASML to establish a 12-inch photomask by 2031. And at that time, we think that the high cost will be reasonable and for TSMC to make it into the mass production. 
And this is a very good tool. Let me emphasize that. And in the smaller geometry, it definitely has some advantage. Whether that our technology because we are using it later than our competitor, so disadvantage to TSMC, no, because we are confident that we are still the best company to offer the most advanced technology to our customers.

**Jeff Su** (Executives):
Krish, does that answer your question? Operator, can we move on to the next participant, please?

**Operator** (Operator):
Charlie Chen, Morgan Stanley.

**Charlie Chan** (Analysts):
Also to hear very strong AI semi demand amid some recent stock market correction. So my first question is really about your leading-edge capacity expansion strategy. As far as I know, one of your IDM customers is expanding CapEx very aggressively. So there are some concern about this customer may in-source more and outsource to you, right? So first of all, I'm not sure how you're going to deal with this sort of business opportunity? And secondly, I remember last time that C.C., you mentioned about A14 could be a bigger node than N2. May I know whether that assume the big IDM company will outsource more CPU like server CPU at A14?

**Jeff Su** (Executives):
Okay. So Charlie's first question is around IDM competitor. He wants to know very specifically if we see this competitor moving to in-source more. So his question is then our prior comment of A14 being a larger, bigger node than N2 has even been -- does this include the server CPU from this IDM competitor, which...

**C.C. Wei** (Executives):
Well, Charlie, we treat every customer fairly. So whether it's IDM or it is purely fabless, we treat them the same. But of course, we take into consideration of the internal capacity. So we calculate our support, we calculate our capacity buildup according to our own judgment. Actually, in our A14, we have seen more and more customers actually higher than the 2-nanometer activities so far. And we expect that the A14 will be a bigger node than our current N2 technologies.

**Charlie Chan** (Analysts):
I see. So it doesn't need to consider this IDM will also outsource more. We can still have A14 to be a bigger node than N2. Is that the right understanding?

**Jeff Su** (Executives):
Well, again, Charlie wants to know very specifically this customer outsourcing plan, which you probably may need to ask them, but...

**C.C. Wei** (Executives):
Well, Charlie, as I said, to be frank with you, I don't comment on a specific customer, but let me guarantee you that we take everything into consideration.

**Jeff Su** (Executives):
Do you have a second question, Charlie?

**Charlie Chan** (Analysts):
Yes, I do. Thanks Jeff. So the second question is kind of follow-up about your advanced packaging. From where we've seen that the retail size is getting much bigger C.C., you said last time or even 2 quarters ago about your response, Sow, 3.5D. So lots of initiatives is going on. So my question is that do you think those are kind of a proposed SoW, 3.5D can really catch customers' very rapid development of their larger reticle size chip, like 14 reticle? And secondly, if some customer, they initially choose to use Intel's EMIB-T, and for some reason, cannot get to sufficient demand (sic) [ supply ]. Are you okay to bail out or support customers for the CoWoS version or capacity?

**Jeff Su** (Executives):
All right. So Charlie's second question is focused on the advanced packaging. I guess, Charlie, if I understand your question, summarize it, is, of course, customers are moving to larger and larger reticle size 14x. So he wants to know TSMC's road map and solutions and how competitive we can be against -- I think he mentioned specifically our competitors' EMIB-T. So how do we view our solution? Is it as competitive as our competitor? That's the first part of this question.

**C.C. Wei** (Executives):
All right, Charlie. Actually, I still think that TSMC's advanced assembly or they say, packaging technology are very, very competitive. But the most important thing is that we're using that one to help us help our customers product can be introduced in the market smoothly. That's our #1 priority. And so we have to offer them the best technology with enough capacity. So far, let me share with you today's situation. We are in the real-world production of 5x reticle size. I don't believe that anybody can do that today, except at TSMC. And the yield is excellent. So our customers are very satisfied with the result. And then we are working on the 9x reticle size and moving into the 14x reticle size. 
Of course, we are also working on the CoWoS and to make sure that in the future, we can offer a reasonable cost reduction. But so far, the CoWoS is still the #1 choice for our customer. As time goes by, yes, our competitors offer a very competitive solution. Still, I want to say that today's situation, we are the only one that make sure that the advanced packaging is a 5x reticle size and still, we are very competitive. I want to emphasize that.

**Jeff Su** (Executives):
And then Charlie's question, if the competitor cannot deliver on their solution, Charlie, I think you're saying we will need to be something like a backup plan.

**C.C. Wei** (Executives):
I try to avoid to answer it directly, but let me say that. Yes, we will be #1 priority. I already indicated that TSMC's customers product can be introduced into the market smoothly. That's the #1 priority, okay? And that gives you enough hint.

**Charlie Chan** (Analysts):
Yes, indeed. I hope you don't give any food to others, including the advanced packaging.

**Jeff Su** (Executives):
All right, operator, let's move on to the next participant, please.

**Operator** (Operator):
Next one is Sunny Lin, UBS.

**Sunny Lin** (Analysts):
So my first question is to have a bit more color on how we should think about CapEx beyond 2026. Recall a few quarters ago, you mentioned if you are doing your job well, then you may be able to drive CapEx to grow a bit less than top line. But now obviously, the overall cloud demand has further strengthened and you're also willing to support your clients with more substantial expansion. And therefore, I wonder, at this point, when you look at maybe the coming 2 years, would you expect maybe CapEx to grow a bit faster, maybe in line with sales or even a bit faster just like for 2026? And then meanwhile, obviously, the tool price is also increasing given a very tight supply. And therefore, going to 2027, would the higher tool price also be a driver for high CapEx as well?

**Jeff Su** (Executives):
Higher -- sorry. What was the last part of your question, Sunny? Higher tool price, higher what?

**Sunny Lin** (Analysts):
So yes, I wonder when we think about 2027 CapEx, should we also consider tool price inflation to be a meaningful variable for a lot higher CapEx compared with this year.

**Jeff Su** (Executives):
Understood. Okay. Sorry. Okay. So Sunny's first question is about our CapEx beyond '26. really, she's asking '27, '28, the next 2 years. With the strong extremely robust demand that C.C. indicated, question is around our capital intensity in the next 2 years. How do we see the capital intensity trending revenue growth versus the CapEx growth, part one. And then also the impact of tool inflation on the CapEx outlook as well.

**Jen-Chau Huang** (Executives):
Okay. Sunny, this is Wendell. It's a bit too early to share the CapEx number beyond this year. But as we said in the prepared remarks, we have very strong conviction in the AI megatrend. Therefore, our CapEx from 2026 to 2028 is expected to be significantly higher than the past 3 years. And this is a step-up of our investment to support the customers' growth. We have no intention to leave any food on the table for others. The tool price inflation is real. The tool price, material, labor costs, et cetera. However, the majority of the CapEx is always related to the long-term demand. So that will be the composition going forward. And capital intensity-wise, as we always said, if we do our job right, the increase in revenue will outpace the increase in CapEx, and that is still the case from what we are looking at.

**Sunny Lin** (Analysts):
Got it. If I may have a very quick follow-up on the CapEx side. Earlier, Wendell, you raised the margin dilution from overseas to, I think, 3% to 4% starting from 2027, given faster overseas expansion. But for the U.S., you're still so far focused on Arizona. So does that imply for Arizona, the expansion for the second phase will happen very quickly or you are actually accelerating the expansion for the third phase or even the other phases as well? Is that therefore the reason for higher margin dilution for next year?

**Jeff Su** (Executives):
Okay. So Sunny's question is kind of about the puts and takes to next year's margin. She does note, as Wendell said in our prepared remarks, that the overseas fabs will widen a bit to 3% to 4% in the next few years. So she wonders what's driving that wider dilution. C.C. did say we are pulling in the schedule for the second fab for 3-nanometer. Her question is, are we also pulling in third fab? What's leading to this wider dilution? And maybe -- yes.

**Jen-Chau Huang** (Executives):
Okay. Sunny, as we mentioned, we are doing everything we can, wherever we can to increase our capacity to meet the strong demand from the customers. And we are also accelerating everywhere, including in the U.S. We did mention before that the later part of the 5-year period, the dilution -- margin dilution from overseas fab will be 3 to 4 percentage points, and that still remains the case. So it's 3 to 4 percentage points in the second part of the 5-year period.

**Sunny Lin** (Analysts):
I see. My second question, I want to follow up.

**Jeff Su** (Executives):
That was 2 questions, Sunny. So there's already 2 questions. Can we -- sorry, but we probably just to accommodate as many as we can, we're going to move on. Thank you for your understanding. Operator, can we move to the next participant, please?

**Operator** (Operator):
Next one, Haas Liu, Bank of America.

**Haas Liu** (Analysts):
Congrats on the great results. My first question would be on your view regarding the potential shift in AI demand mix. You mentioned in the prepared remarks that the AI accelerator chipset demand is proliferating into generative AI demand, including CPUs and networking switches. We understand the overall AI investment is still pretty strong and even trending stronger across the board. But can we get more clarity that are you seeing your customers' demand shifting towards more efficient compute solutions, especially monetization gets more important? And how should we think about the incremental opportunity for your manufacturing and packaging business?

**Jeff Su** (Executives):
So Haas's first question is on the AI-related demand. His question is, are we seeing a shift in the AI-related demand more and more to CPU or networking switches and away from AI accelerators? Or any type of comment?

**C.C. Wei** (Executives):
Well, all I can say is AI demand is extremely robust, okay? Whether it's come from accelerator or more from the CPU side, it's not for me to make a comment. Although we did see the demand from Agentic AI, CPUs continue to increase. Yes, that is a trend today. But other than that, everything is very robust. And I want to emphasize again, in our judgment, we consider all the parameters and the demand actually is still far above our capability today to supply, and we are working very hard to narrow the gap. That's all I can say.

**Haas Liu** (Analysts):
Okay. That's very clear. And my second question is just regarding the yield learning curve going forward for your dual technology tracks strategy going forward. So historically, I think you have been ramping up the yield of a new node through producing the chipsets with smaller die size and simpler design to improve the learning curve of a new node. But for the future node families supporting both conventional power delivery for the applications like mobile and consumer applications and Super Power Rail technology for HPC and AI chipsets, would operating two process architectures at the same time make the learning curve more challenging or increase the manufacturing complexity? And how should we think about the implication to your gross margins from the yield and also cost control perspective?

**Jeff Su** (Executives):
Okay. So Haas's second question is -- his question is really about ramping a new node, the learning curve of yield and cost and therefore, the implication to gross margin, really, I think, is what he's driving at. And his question is that in the past, a new node is mostly ramped with smaller die size and simpler design. But -- so today, we have both the smartphone and also with the AI and HPC applications coming in. Does that increase the complexity of the node process architecture, make the learning curve more challenging or difficult and therefore, the implication to the margin?

**C.C. Wei** (Executives):
Well, today's situation actually is a little bit different from previous year. Yes, we now have a very strong demand from smartphone and also AI HPC applications. And so the smaller die size per se or the big die size in the accelerator, they happen at the same time. And this is to TSMC's advantage, let me say that, because we are good. We have been prepared for this kind of thing. And our results are very excellent and customers are very happy to work with us. And so the learning curve, yes, but we are doing a reasonable job. And so all the customers are very happy today.

**Jeff Su** (Executives):
Okay. Operator, let's move on to the next participant, please.

**Operator** (Operator):
On the line Macquarie.

**Yu Jang Lai** (Analysts):
I have a question on the power as gating factor. So I want to understand have power grid constraints led you reduce your customer forecast in Q3? And also, could this tighter and tighter power grid surprise your customer actually accelerating adoption of your Super Power Rail products for the better performance per watt?

**Jeff Su** (Executives):
Okay. So Arthur's first question is about the power supply or electricity supply. Is it a gating factor? And have we seen that lead to a reduction in customers' forecast? And with the tighter -- on the other side or on the other hand, with the tighter power electricity supply, have we seen more customers' adoption of Super Power Rail technologies?

**C.C. Wei** (Executives):
Well, let me update that. Definitely, the power supply situation is one of the consideration factor that we are looking into. And that's why also we do one more step to double check whether the power supply situation in the U.S. And we have done all the study and so far, so good, let me say that. And whether this kind of situation change our customers' behavior and move more into the backside power rail? The answer is no. Whether you use the backside power, those kind of metallization scheme is based on your need for your product, okay? So some of the accelerator might be using it, some of the products like mobile phones, they don't use it. So it depends on customers' product. Did I answer the question?

**Yu Jang Lai** (Analysts):
Yes.

**Jeff Su** (Executives):
Do you have a second question?

**Yu Jang Lai** (Analysts):
So just to recall the previous discussion on the Agentic AI demand on the CPU. So I wonder according to our previous framework, demand forecast framework, the mid- to high teens growth, included the CPU or not? And if we hear our clients increase the CPU forecast significantly, when is the next time we refresh our AI demand growth numbers?

**Jeff Su** (Executives):
Okay. So Arthur second question is on -- his question is really on our -- we already stated by anyway, our AI accelerator definition. He wants to know with the emergence of Agentic AI and CPU, does that AI accelerator definition include CPUs or not? And if when we will provide inclusion for him?

**C.C. Wei** (Executives):
Let me answer the question. It's not included in our AI demand calculation. The reason is very simple because we cannot identify which CPU user in the conventional server CPU or AI server CPU. And also that it depends on our customers' application and their own allocation also. So no. So far today, we stick to our initial very narrow definition on the AI demand.

**Yu Jang Lai** (Analysts):
Understand. And so if we have seen a really strong CPU-driven demand, when we will revise up the...

**Jeff Su** (Executives):
Arthur, I think we already said very clearly, it's not part of the AI accelerator definition. It's a narrow definition, but it is certainly part of our business, okay?
Okay. Operator, in the interest of time, can we take question from the last participant on the line, please?

**Operator** (Operator):
Sahej Singh, Stifel Financial.

**Sahej Singh** (Analysts):
Thank you for the question. Into 2027, you have N3 turning accretive and now that's crossed over, N2 is still in its dilutive ramp and the overseas dilution is widening. So on the offset side, there have been reports of significant price increases across your mature and advanced nodes. Could you provide some color into perhaps some of that conversation and where pricing does move, does it typically apply across the existing contracted book? Or is it mainly being applied to incremental capacity above what customers have already committed to?

**Jeff Su** (Executives):
Yes. Okay. So the first question is talking about -- I guess you're asking about the potential puts and takes for next year? Or you're asking specifically on pricing, sorry? For pricing.

**Sahej Singh** (Analysts):
Specifically on pricing.

**Jeff Su** (Executives):
Okay. So it's a very specific question that there's reports that we are increasing the price. He wants to know, does it apply across the existing contracted commitments from customers? Or is it mainly for the incremental capacity?

**C.C. Wei** (Executives):
Well, we have discussed this kind of thing before that our pricing strategy is very strategic. It also depends on the market segment, depending on the location and depends on the technology and something. Once we offer the flexibility of the physical location like in the U.S., it will be a little bit different from the one we produce in Taiwan. So no matter what, well, we try to get our value to be recognized, and we will give our shareholders the maximum value of our technology.

**Sahej Singh** (Analysts):
Understood. For the second question, something you said in your prepared remarks, stuck out to me was we will not be leaving food on the table. And earlier, I think it was maybe 1 or 2 weeks ago, there was the announcement via GlobalFoundries that they would be providing silicon interposers to TSMC. And so would love some color into how are you thinking through these strategic decisions in terms of procuring from some of the specialty foundries versus providing in-house?

**Jeff Su** (Executives):
Okay. So his second question is, again, he notes that recently, we had an announcement with GlobalFoundries and interposers. So how do we view these partnerships? And what is our approach strategically?

**C.C. Wei** (Executives):
Let me answer the question. We designed a deal with GlobalFoundries -- and this is part of our overall strategy in the back-end supply. Actually, our #1 priority is to help our customers to be successful in their market. We want them to be fully supported by all the supply, including the front end and back end. Definitely, we have a little bit shortage on the back end, and we'd like to work with our so-called partner with GlobalFoundries so that we can both TSMC and GlobalFoundries can support TSMC's customer for their product to be introduced with enough support on the capacity.

**Jeff Su** (Executives):
Okay. Thank you for your questions. Thank you for all the participants. This does conclude our question-and-answer session. Before we conclude today's conference, please be advised that the replay of the conference will be accessible within 30 minutes from now. The transcript will become available 24 hours from now, and you can find both will be available through TSMC's website at www.tsmc.com. So again, thank you for joining us today. We hope everyone continues to stay well. Have a good autumn, and we hope you will join us again next quarter. Thank you, and have a good day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TSM_Q2_2026_Earnings_Call_20260716.md
- 2026-07-16｜CFO｜guidance：CFO 給第三季營收指引區間（446–458 億美元，中點季增 12%）（原話："our third quarter revenue to be between USD 44.6 billion"）
- 2026-07-16｜CFO｜guidance：第三季毛利率與營業利益率指引（匯率假設 32）（原話："gross margin is expected to be between 65% and 67%"）
- 2026-07-16｜CEO｜guidance：CEO 上調 2026 全年美元營收成長預期（原話："slightly above 40% year-over-"）
- 2026-07-16｜CFO｜margin：第二季毛利率季增 150bp 至 67.7% 的原因（原話："primarily due to cost"）
- 2026-07-16｜CFO｜margin：管理層說明 2 奈米陡峭放量對毛利率的稀釋幅度（約 3–4 個百分點）（原話："dilute our gross margin by about 3 to 4"）
- 2026-07-16｜CFO｜margin：海外晶圓廠毛利率稀釋的區間口徑（初期 2–3%、後期 3–4%）（原話："to be 2% to 3% in the early stages"）
- 2026-07-16｜CFO｜capital_allocation：全年資本支出上調至 600–640 億美元（原話："raise our full year 2026 capital budget to be between USD 60"）
- 2026-07-16｜CFO｜capital_allocation：資本支出分配比例（原話："About 70% to 80% of the 2026 capital budget will be"）
- 2026-07-16｜CFO｜commitment：管理層重申股利承諾：2026 每股 24 元、2027 持續增加（原話："we expect a continued and increasing cash dividends"）
- 2026-07-16｜CFO｜commitment：未來三年資本支出相對過去三年的說法升級（先前為「明顯高於」）（原話："the CapEx in the next 3 years will be even more"）
- 2026-07-16｜CEO｜capital_allocation：宣布亞利桑那再增 1000 億美元投資（原話："we would like to announce an additional USD 100 billion"）
- 2026-07-16｜CEO｜capital_allocation：被問及亞利桑那時程，CEO 稱視市況而定，並說明新增約 4 座廠（含前後段）（原話："the schedule will depend on the market situation."）
- 2026-07-16｜CEO｜risk：消費性與價格敏感市場受零組件漲價與總經不確定性挑戰，公司規劃趨於審慎（原話："consumer and price-sensitive end market segments are being"）
- 2026-07-16｜CEO｜customer：CEO 指雲端服務商給出強烈正向訊號，對多年 AI 趨勢信心很高（原話："our conviction in the multi-year AI"）
- 2026-07-16｜CEO｜product：Agentic AI 使 CPU 在 AI 資料中心角色回升，CEO 稱各種 CPU 架構幾乎都是客戶（原話："they are almost all"）
- 2026-07-16｜CEO｜product：A14 進度：2027 試產、2028 量產（原話："Pre-production will start in 2027 and volume production"）
- 2026-07-16｜CEO｜product：A13、A12 為 A14 延伸，預定 2029 量產（原話："Both A13 and A12 are scheduled for"）
- 2026-07-16｜CEO｜product：N3 擴產：台灣、亞利桑那、日本各一座新廠，並轉換 5 奈米機台（原話："we continue to convert 5-nanometer tools"）
- 2026-07-16｜CEO｜product：成熟製程策略：高附加價值領域增加而非減少產能，其他商品化領域需求不強（原話："mature node demand in other commodity area is not that"）
- 2026-07-16｜CEO｜competition：回應三星／英特爾競爭：強調技術、製造與客戶信任三項基本功（原話："the technology, manufacturing, and customer"）
- 2026-07-16｜CEO｜competition：CEO 表示先進封裝產能吃緊，歡迎 EMIB-T 等替代方案分擔（原話："our packaging capacity is so tight that now it's limited by"）
- 2026-07-16｜CEO｜competition：CEO 區分前段晶圓與後段封裝為兩種不同業務（原話："The front-end's wafer business and the back-end's business"）
- 2026-07-16｜CEO｜guidance：被問 AI 半導體五年 CAGR 更新，CEO 不給數字，只稱比先前說法更強（原話："but stronger than what we said before."）
- 2026-07-16｜CEO｜risk：CEO 談需求預測方法：各客戶說法加總未必是真相，需自行判斷（原話："You put all the truths"）
- 2026-07-16｜CEO｜risk：被問供給不足會否持續，CEO 稱需求強勁至約 2029–2030，但不確定中間是否有回檔（原話："Whether in between there's a dip or not, I'm not very"）
- 2026-07-16｜CEO｜margin：定價哲學：不大幅漲價以免擠壓客戶，毛利以支撐長期擴張為目標（原話："I don't want to squeeze them out from the market."）
- 2026-07-16｜CEO｜customer：被問前五大客戶集中度風險，CEO 稱不是顧慮（原話："No, that's not our concern."）
- 2026-07-16｜CEO｜capital_allocation：CEO 表示公司目前不做對客戶的客戶提供融資或投資（原話："So far, no, TSMC don't do this kind of financial arrangement"）
- 2026-07-16｜CEO｜product：COUPE 已開始生產，預期未來幾年重要性提升（未給時程數字）（原話："We start the production right now, and it will be ramped up."）
- 2026-07-16｜CEO｜product：玻璃基板等替代方案仍在建置試產線，約再一年成熟（原話："it takes about another 1 year to be mature"）
- 2026-07-16｜CEO｜capital_allocation：資本支出上調原因之二：設備價格通膨（之一為客戶需求持續增加）（原話："The second reason is inflation."）
- 2026-07-16｜CEO｜customer：成熟製程僅與 AI 相關者短缺（電源管理 IC、感測器），消費性需求不強（原話："Only the one which related to AI is in"）
- 2026-07-16｜CEO｜risk：被問先進製程需求超出供給的幅度，CEO 不給數字，只稱缺口很大（原話："the gap is very big."）

### 問答異常語氣（迴避／改口／保留）
- TSM_Q2_2026_Earnings_Call_20260716.md｜問：是否提供未來三年資本支出指引（比照 2021 年做法）｜答法：CFO 明說沒有數字可提供，改以定性說法（未來三年資本支出會更顯著高於過去三年）回應
- TSM_Q2_2026_Earnings_Call_20260716.md｜問：是否上調 AI 半導體五年營收 CAGR（1 月為中高 50% 區間）｜答法：CEO 拒絕給數字，只說「越來越強」、比先前說法更強
- TSM_Q2_2026_Earnings_Call_20260716.md｜問：亞利桑那新增 1000 億美元的投入時程｜答法：CEO 稱有計畫但視市況與客戶需求，拒絕給確定時程
- TSM_Q2_2026_Earnings_Call_20260716.md｜問：未來幾年營收成長是否可量化｜答法：CEO 只答「接下來幾年對台積電會是很好的生意」，未給數字
- TSM_Q2_2026_Earnings_Call_20260716.md｜問：3 奈米以下無限制需求超出供給的比例是否遠高於 30–50%｜答法：CEO 不給數字，僅稱缺口「很大」，並提及不想評論記憶體
- TSM_Q2_2026_Earnings_Call_20260716.md｜問：先進封裝資本支出可否單獨拆出、佔比多少｜答法：CEO 稱前後段彈性調度無法具體拆分，維持 10–20% 區間

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
{"date":"20260916","verdict":"進場","role":"核心","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"FY2027 共識 EPS 22.55 × 16x ≈ $361 以下，或 250 週均線斜率回到 +3% 以上且毛利率連兩季 ≥66%","irr_base_pct":13.0,"ev5y_pct":81.4,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"🟡","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":6.3,"ev5y_pct":81.4,"irr_base_pct":13.0,"max_dd_pct":-50,"bull_5y_price":1222.0,"bear_5y_price":294.0,"p_bull_pct":28,"p_bear_pct":30,"rearm_trigger":"FY2027 共識 EPS 22.55 × 16x ≈ $361 以下，或 250 週均線斜率回到 +3% 以上且毛利率連兩季 ≥66%","price_at_dd":413.75,"archetype":"品質複利成長","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSM_20261017/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
