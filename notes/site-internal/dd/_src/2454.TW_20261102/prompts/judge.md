你是 stock-analyst **v20 判斷 agent**，標的 2454.TW（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"2454.TW","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2454.TW_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2454.TW_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_tifrs","label":"營收（GAAP/TIFRS）","value":168058,"period":"3Q26（季末 2026-09-30，公告於 2026-10-30）","unit":"NT$百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-30）","citation":"聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）"},"note":"查無（IR 新聞稿不含共識；未另查證）"},{"id":"f_kpi1_gaap","label":"毛利率（GAAP）","value":46.3,"period":"3Q26（季末 2026-09-30，公告於 2026-10-30）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-30）","citation":"聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）"},"note":"查無（IR 新聞稿不含共識；未另查證）"},{"id":"f_kpi2_non_tifrs","label":"Non-TIFRS 營業利益／利益率","value":27923,"period":"3Q26（季末 2026-09-30，公告於 2026-10-30）","unit":"NT$百萬（利益率 16.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-30）","citation":"聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf），調節項＝SBC＋收購資產攤銷"},"note":"查無（IR 新聞稿不含共識；未另查證）"},{"id":"f_kpi3_gaap_tifrs","label":"GAAP（TIFRS）營業利益／利益率","value":27102,"period":"3Q26（季末 2026-09-30，公告於 2026-10-30）","unit":"NT$百萬（利益率 16.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-30）","citation":"聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）"},"note":"查無（IR 新聞稿不含共識；未另查證）"},{"id":"f_kpi4_eps_tifrs","label":"淨利／EPS（TIFRS，歸屬母公司）","value":17.5,"period":"3Q26（季末 2026-09-30，公告於 2026-10-30）","unit":"NT$／股（淨利 28,199 百萬，其中非營業收入 6,471 百萬占營收 3.9%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-30）","citation":"聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）"},"note":"查無（IR 新聞稿不含共識；未另查證）"},{"id":"f_kpi7_archetype","label":"存貨週轉天數（硬體 archetype）","value":127,"period":"3Q26（季末 2026-09-30，公告於 2026-10-30）","unit":"天","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-30）","citation":"聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）；期末存貨 153,531 百萬"},"note":"n/a"},{"id":"f_kpi8","label":"現金及流動金融資產","value":278320,"period":"3Q26（季末 2026-09-30，公告於 2026-10-30）","unit":"NT$百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-30）","citation":"聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）"},"note":"n/a"},{"id":"f_kpi9_4q26","label":"管理層指引：4Q26 營收","value":"NT$210.1–221.8 十億（約 YoY +40–48%）；毛利率 45% ±1.5pp；2027 全年營業利益率目標約 20% 或略高","period":"4Q26 指引（法說會 2026-10-30）","unit":"NT$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"4Q26 指引（法說會 2026-10-30）","citation":"二手來源（IR 新聞稿不含指引，指引在法說簡報／逐字稿）：MarketScreener、Investing.com、BigGo 摘要；採用前宜對照 IR 法說簡報"},"note":"查無（IR 新聞稿不含共識；未另查證）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-30","period":"2026-10-30","unit":"date","basis":"距今 1 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-30"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_2454_tw_gross_margin_pct","label":"2454.TW 毛利率","value":46.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2454.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2454_tw_operating_margin_pct","label":"2454.TW 營業利益率","value":15.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2454.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2454_tw_fcf_margin_pct","label":"2454.TW FCF 利潤率","value":13.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2454.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qcom_gross_margin_pct","label":"QCOM 毛利率","value":54.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qcom_operating_margin_pct","label":"QCOM 營業利益率","value":23.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_qcom_fcf_margin_pct","label":"QCOM FCF 利潤率","value":23.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_3661_tw_gross_margin_pct","label":"3661.TW 毛利率","value":37.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3661_tw_operating_margin_pct","label":"3661.TW 營業利益率","value":24.0,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3661_tw_fcf_margin_pct","label":"3661.TW FCF 利潤率","value":-10.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3443_tw_gross_margin_pct","label":"3443.TW 毛利率","value":23.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3443.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3443_tw_operating_margin_pct","label":"3443.TW 營業利益率","value":13.0,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3443.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3443_tw_fcf_margin_pct","label":"3443.TW FCF 利潤率","value":7.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3443.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_ocf","label":"營業活動現金流（OCF）","value":-4256,"period":"3Q26（季末 2026-09-30，公告於 2026-10-30）","unit":"NT$百萬","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-30）","citation":"聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）（現金流量摘要）。單季資本支出新聞稿未揭露（財報 PDF 僅有前九個月累計，PP&E 21,846 百萬），故單季 FCF 不推算"},"note":"查無（IR 新聞稿不含共識；未另查證）"},{"id":"f_kpi6_sbc","label":"SBC 占營業利益","value":2.89,"period":"3Q26（季末 2026-09-30，公告於 2026-10-30）","unit":"%（783 ÷ GAAP 營業利益 27,102；占營收 0.47%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-30）","citation":"聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）（Non-TIFRS 調節表 SBC 783 百萬）；占比為自行換算"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":3915.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"TWD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":50.9,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^TWII","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":36.23,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":1.88,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（69.69 → 71.0）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.66,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（149.48 → 150.46）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.34,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（286.26 → 285.29）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":71.0,"period":"2026-10-31","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":150.46,"period":"2026-10-31","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":285.29,"period":"2026-10-31","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":6.03,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 66.96 → 71.0（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":64.65,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":10.09,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":9.71,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":55.14,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 71.0，分子＝快照價 3915.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.367,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-236369.99,"period":"2026-11-02","unit":"TWD m","basis":"yfinance 最新一季：總債務 41950.0、現金 278319.99（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1597.13,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":6016393.56,"period":"2026-11-02","unit":"TWD m","basis":"市值 6252763.55 ＋ 淨負債 -236369.99","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":678630.33,"period":"2026-11-02","unit":"TWD m","basis":"yfinance revenue_estimate 0y 平均（19 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":1199125.91,"period":"2026-11-02","unit":"TWD m","basis":"yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":8.87,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"✅","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 3915.0 / W52 2869.02 / W104 2094.86 / W250 1316.5 / W250 13週斜率 4.3%"},{"id":"f_ma_w52","label":"52 週均線","value":2869.02,"period":"2026-11-02","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":2094.86,"period":"2026-11-02","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":1316.5,"period":"2026-11-02","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":4.3,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Counterpoint：2026Q1 全球智慧手機 SoC 聯發科市占 32%（去年同期 38%），高通 23%（27%），蘋果 19%（15%），紫光展銳 14%（10%），三星 7%（5%）；聯發科仍第一但份額下滑，搶份額者為蘋果、紫光展銳、三星","source":"工商時報 2026-06-12／malaysianwireless（Counterpoint Q1 2026）","url":"https://www.ctee.com.tw/news/20260612701159-430503","excerpt":null,"as_of":"2026-06-12","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"2026-06 高通宣布與 Meta 策略性多世代合作進軍 AI ASIC，聯發科盤中股價一度跌停；聯發科稱目標搶攻 10%～15% 市占（以 2027 年 700～800 億美元潛在市場估算）","source":"自由時報 對手高通搶進AI ASIC市場! 聯發科「嚇」跌摜至跌停","url":"https://ec.ltn.com.tw/article/breakingnews/5484649","excerpt":null,"as_of":"2026-06-26","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"市場傳 Marvell 可能成為 Google 第三家 ASIC 夥伴，對博通與聯發科形成競爭疑慮；法人稱聯發科已取得 Google 下一代 ASIC 訂單、地位穩固，KGI 認為疑慮被過度放大","source":"工商時報 2026-04-26／KGI 報告 2026-04-21","url":"https://www.ctee.com.tw/news/20260426700386-430201","excerpt":null,"as_of":"2026-04-26","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"亞系券商指出聯發科中低階市場報價與市占承壓，紫光展銳在 4G、高通在 5G 競爭激烈，預期 2026 年 5G SoC 平均售價年減約 10%（發布日期搜尋結果未明確，as_of 為估計）","source":"經濟日報","url":"https://money.udn.com/money/story/5607/9023568","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"2026年9月底傳聞 Google 新一代 TPU 供應鏈有變數，TPU v9 可能由邁威爾（Marvell）分食訂單、v8 樣品可能延至2027年Q2；聯發科股價一度重挫逾7%（媒體傳聞，未經公司證實）。","source":"ETtoday 財經／搜尋結果摘要：聯發科發了!搶到Google「TPU大單」 博通重挫12%（同批結果另有 Google TPU 訂單疑慮報導）","url":"https://finance.ettoday.net/news/3177980","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"聯發科於2026-10-30 Q3法說會表示已取得第二家客製AI晶片（ASIC）客戶，預計2028年量產，未揭露客戶身分，並稱非中國公司；市場傳為Meta但未證實。","source":"cryptobriefing: MediaTek confirms second AI ASIC customer for 2028 production","url":"https://cryptobriefing.com/mediatek-second-ai-asic-customer-2028/","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"0","claim":"本軸搜尋未找到任何報導指出聯發科主要客戶（手機品牌或ASIC客戶）將此環節自製（in-house）；僅有一般性風險評論。","source":"搜尋摘要（2454.TW MediaTek largest customer second source OR in-house 2026）","url":null,"excerpt":null,"as_of":"2026-11-02","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#3","axis":"customer_second_source","section":"coverage","direction":"+","claim":"博通大客戶傳轉單，市場盯上聯發科","source":"數位時代 bnext","url":"https://www.bnext.com.tw/article/91243/mediatek-broadcom-ai-asic-tpu","excerpt":"博通大客戶傳轉單，市場盯上聯發科！AI ASIC成台灣IC設計廠下一階段成長主軸 博通於財報會議中首度透露，大客戶正尋找其他供應商，引發市場對聯發科大啖更多谷歌客製化TPU的想像空間。 ＃英特爾 ＃IC設計 ＃聯發科 ＃google tpu ＃台積電（tsmc） 工商時報 博通大客戶傳轉單，市場盯上聯發科！","as_of":"2026-06-13","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"114年度（2025）占銷貨10%以上客戶共3家：客戶A 15.49%（923.1億元）、客戶B 12.07%、客戶C 11.38%，合計約38.9%；其餘客戶占61.06%；皆非關係人。113年度為客戶D 14.92%、客戶C 12.20%、客戶B 12.15%（客戶A當年未達10%）。","source":"公開資訊觀測站電子書件 114年股東會年報 主要銷貨客戶表（PDF第75頁）","url":"https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id=2454&year=115&seamon=&mtype=F&dtype=","excerpt":"客戶 A  92,314,595  15.49%  非關係人  客戶 B  71,933,222  12.07%  非關係人  客戶 C  67,798,735  11.38%  非關係人  客戶 D  不適用  不適用  非關係人  其他  363,919,130  61.06%","as_of":"2026-05-08","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026-07-31 法說會上，執行長蔡力行把 2027 年 AI ASIC 市占率目標由 10%~15% 上調至 15%~20%","source":"鉅亨網","url":"https://news.cnyes.com/news/id/6554849","excerpt":"聯發科 (2454-TW) 近年積極搶攻 AI ASIC 商機，執行長蔡力行今 (31) 日於法說會中宣布，將 2027 年 AI ASIC 市占率目標，由原先的 10% 至 15%，上調至 15% 至 20%。","as_of":"2026-07-31","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"管理層稱 CoWoS 產能吃緊，但 2026、2027 年產能需求已確保；外資指 TPU 量產與 T-Glass 及載板供應相關，載板為產業瓶頸","source":"搜尋摘要（富果研究／uanalyze 等）","url":"https://blog.fugle.tw/post/earnings-call-2454-2026-03-11","excerpt":"儘管目前先進封裝(CoWoS)產能吃緊，但聯發科表示，2026 年與 2027 年的產能需求已獲得確保，足以達成既定目標。","as_of":"2026-03-11","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"記憶體缺貨：聯發科高層傳出拜會三星與SK海力士爭取產能，手機業務占比高受影響較大（媒體傳聞，公司未回應）","source":"technews 搜尋摘要","url":"https://finance.technews.tw/2026/01/27/rising-memory-prices-impact-mediateks-operations/","excerpt":"業界傳出，聯發科高層罕見親拜會三星電子與SK海力士，希望換取更多產能。","as_of":"2026-01-27","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"台積電 CEO 表示供應短缺可能延續到 2027 年甚至更久（上游代工產能）","source":"longportapp 搜尋摘要","url":"https://longportapp.cn/news/283506138","excerpt":"despite the massive investment, the company still expects supply shortages to continue until 2027 or even longer","as_of":"2026-01-01","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"公平會處分書資料庫以「聯發科技」全文搜尋共2筆，皆為2014年東陽行動／威寶電信廣告案僅文內提及，聯發科本身未被處分","source":"公平交易委員會 處分書及決議書全文搜尋","url":"https://www.ftc.gov.tw/internet/main/decision/decisionList.aspx?mid=11","excerpt":"以關鍵字「聯發科技」全文搜尋（查詢日 2026-11-02）共 2 筆。命中只代表處分書或決議書全文提到該名稱，不代表該公司被處分","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"證交所ESG彙總：報告年度114反競爭行為法律訴訟金錢損失為0","source":"證交所 OpenAPI t187ap46_L_20","url":"https://openapi.twse.com.tw/v1/opendata/t187ap46_L_20","excerpt":"報告年度 114，因與反競爭行為條例相關的法律訴訟而造成的金錢損失總額(仟元)＝0.000。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"瑞昱在美國對聯發科提私人反壟斷訴訟（賞金協議），2026-02法院駁回簡易判決動議；2026-07瑞昱撤告（Bloomberg Law報導）。非主管機關調查，未查到DOJ正式調查","source":"Bloomberg Law: Realtek Drops Suit Against MediaTek Targeting Patent Bounty Deal","url":"https://news.bloomberglaw.com/ip-law/realtek-drops-suit-against-mediatek-targeting-patent-bounty-deal","excerpt":null,"as_of":"2026-07-16","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"聯發科表示出口美國營收約占一成，關稅影響相對有限，客戶未見訂單調整，暫難提供全年展望（搜尋摘要轉述，未核原文）","source":"自由時報 美關稅衝擊》聯發科︰未見訂單調整 暫難提供全年展望","url":"https://ec.ltn.com.tw/article/paper/1704554","excerpt":null,"as_of":"2025-04-30","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2018年聯發科曾因國貿局公文要求出口前申請許可而暫停對中興出貨，後取得許可恢復；2025年6月經濟部擴充出口管制實體名單（新增華為、中芯等），搜尋結果未顯示聯發科本身被列入（搜尋摘要轉述，未核原文）","source":"techbang／technews 報導（2018中興案）；worldecr 2025-06 名單擴充","url":"https://finance.technews.tw/2018/05/04/mtk-zte/","excerpt":null,"as_of":"2018-05-04","retrieved_at":"20261102","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"玉山投顧2025年4月報告：台灣IC設計業需分攤部分關稅，中國營收比重高的聯發科受衝擊最低","source":"玉山證券 esunsec 文章","url":"https://www.esunsec.com.tw/article/post/260","excerpt":"關稅影響程度為最大，究竟台灣各個主要股票的美國營收比重為多少，又川普關稅政策會如何影響台灣各大產業及個股，詳見以下文章：（以下文章資訊皆整理自玉山投顧） IC設計 晶圓代工 封裝測試 記憶體 光學/砷化鎵 伺服器零組件 電子代工 電子品牌 網通 工業電腦 成衣/製鞋 汽車零組件 重電/工具機 結論 <延伸閱讀：全面解析川普對等關稅影響，股債ETF投資組合應如何調整？> <延伸閱讀：川普對等關稅橫掃 美股科技七巨頭影響分析一表秒看懂> IC設計產業：可能須分攤部分關稅成本 產業 主要評析 相關個股 IC設計產業：可能須分攤部分關稅成本 受衝擊程度低 台灣IC設計公司主要投片於晶圓代工廠，再按各產品別如手機、電視、筆電、網通、伺服器銷往全球，實際上受到對等關稅的衝擊程度較低，但由於品牌客戶與代工廠都會面臨關稅成本壓力，因此IC設計業者勢必需要分攤部分關稅成本，現階段中國營收比重高的公司如聯發科","as_of":"2025-04-15","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"聯發科執行長稱正模擬美國關稅情境，預期當年影響可控（manageable）","source":"PhoneArena","url":"https://www.phonearena.com/news/mediatek-running-simulations_id167401","excerpt":null,"as_of":"2025-04-10","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"聯發科 2026-05 供應商大會：導入 AI 預測與數位自動化，整合需求、供應、庫存資訊以提早辨識供應鏈風險（搜尋摘要轉述，未核原文）","source":"technews 財經頻道 mediatek announces supply chain resilience at supplier conference","url":"https://finance.technews.tw/2026/05/25/mediatek-announces-supply-chain-resilience-at-supplier-conference/","excerpt":null,"as_of":"2026-05-25","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"聯發科副董事長蔡力行於2026年股東會表示台積電是長期合作晶圓代工夥伴，合作涵蓋12奈米到2奈米及先進封裝","source":"中時 wantrich","url":"https://wantrich.chinatimes.com/news/20260529900231-420101","excerpt":null,"as_of":"2026-05-29","retrieved_at":"20261102","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"2026Q3 手機營收占比37%，季減1%、年減17%","source":"TechNews 聯發科Q3 EPS 17.5元、毛利率46.3%","url":"https://finance.technews.tw/2026/10/30/mediateks-third-quarter-eps-reached-nt17-5-with-a-gross-margin-of-46-3/","excerpt":"手機業務（Mobile）營收占比為 37%，季減 1%、年減 17%。","as_of":"2026-10-30","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"2026Q3 智慧裝置平台占比58%，季增20%、年增63%","source":"TechNews 聯發科Q3 EPS 17.5元、毛利率46.3%","url":"https://finance.technews.tw/2026/10/30/mediateks-third-quarter-eps-reached-nt17-5-with-a-gross-margin-of-46-3/","excerpt":"智慧裝置平台（Smart Edge）營收占比達 58%，較前一季成長 20%，更較2025年同期大增 63%。","as_of":"2026-10-30","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"PMIC占比5%，年增18%，來自資料中心市占提升","source":"TechNews 聯發科Q3 EPS 17.5元、毛利率46.3%","url":"https://finance.technews.tw/2026/10/30/mediateks-third-quarter-eps-reached-nt17-5-with-a-gross-margin-of-46-3/","excerpt":"電源管理 IC（PMIC）營收占比為 5%，季增 1%、年增 18%，年成長主要來自資料中心業務市占率顯著提升。","as_of":"2026-10-30","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"首款AI加速器ASIC 9月小量出貨，Q4預估貢獻25億美元；Q4合併營收指引2,101～2,218億元，季增25%～32%","source":"TechNews 聯發科Q3 EPS 17.5元、毛利率46.3%","url":"https://finance.technews.tw/2026/10/30/mediateks-third-quarter-eps-reached-nt17-5-with-a-gross-margin-of-46-3/","excerpt":"首款 AI 加速器 ASIC 於 9 月開始小量出貨，預估第四季將貢獻 25 億美元營收","as_of":"2026-10-30","retrieved_at":"20261102","affects":["thesis.H","valuation","triggers"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年8月營收641.83億元，月增32.41%、年增44.08%，創單月新高","source":"優分析轉載鉅亨網 聯發科8月營收","url":"https://uanalyze.com.tw/articles/4277055080","excerpt":null,"as_of":"2026-09-10","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"2027年資料中心ASIC營收比重可望達約兩成","source":"優分析 〈聯發科法說〉Q1營收拚持平上季 2027年ASIC營收比重衝2成","url":"https://uanalyze.com.tw/articles/5844147329","excerpt":"2027年資料中心 ASIC 營收比重可望達到約兩成。","as_of":"2026-04-30","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"大摩報告提到聯發科 3 奈米 TPU 尚未完成所有工程驗證測試，TPU 出貨量與 T-Glass/基板供應高度相關（搜尋摘要轉述，未讀原頁）","source":"中時 wantrich：大摩、富邦投顧看好聯發科2027年（搜尋摘要）","url":"https://wantrich.chinatimes.com/news/20260127900273-420101","excerpt":null,"as_of":"2026-01-27","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"外資指受記憶體成本上升影響，2026 全球智慧機晶片出貨預估年減約 7%，中國 Android 手機 SoC 2026Q1 出貨可能季減 10%～20%（搜尋摘要轉述）","source":"technews.tw 大摩看好聯發科 AI ASIC（搜尋摘要）","url":"https://technews.tw/2026/01/26/morgan-stanley-see-mediatek-ai-asic/","excerpt":null,"as_of":"2026-01-26","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"報導：摩根士丹利與高盛示警聯發科毛利率面臨結構性下修風險（台積電先進製程漲價、車用與 AI ASIC 初期毛利低）","source":"經濟日報 聯發科靠ASIC翻轉景氣循環宿命","url":"https://money.udn.com/money/amp/story/5607/9773650","excerpt":"智慧裝置平台，涵蓋聯網、WiFi 8、PC運算（與Nvidia合作的RTX Spark），以及最重要的ASIC。隨著與谷歌合作的ＴＰＵ進展順利，聯發科在四月及七月法說會上，將全年ASIC的營收展望上修倍增到突破二○億美元（約六三二億台幣）。 與ＴＰＵ的合作晶片預計會如期在第四季進入量產並貢獻營收，成為拉動聯發科營收率創新高的主引擎。聯發科透過將原本在手機端累積的ＩＰ（CPU/GPU/NPU、通訊、低功耗設計），重複利用並延伸到路由器、車用與資料中心。不僅大幅攤提昂貴先進製程的研發費用，帶來邊際成本遞減的效果，直接推升智慧裝置平台的整體毛利率。","as_of":"2026-09-23","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"聯發科由手機晶片商轉向資料中心 ASIC／系統級設計夥伴；目標 2026 年 ASIC 營收超過 10 億美元，長期占整體營收 20%（搜尋摘要轉述，未讀原頁）","source":"民報 peoplenews.tw 聯發科轉型2》揭ASIC營收大餅","url":"https://www.peoplenews.tw/?p=15503","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Futurum 描述聯發科由 mobile-first B2C 轉為多引擎 B2B 夥伴，Analyst Day 明列資料中心為最高優先與最大成長機會；手機占營收 49%，季減與年減各 15%（搜尋摘要轉述）","source":"Futurum Group：MediaTek Analyst Day 2026","url":"https://futurumgroup.com/insights/mediatek-analyst-day-2026-is-the-new-mediatek-ready-to-move-upmarket-to-ai-pcs-and-data-center","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"S&P Global：AI ASIC 成長抵銷智慧手機疲弱","source":"S&P Global Market Intelligence 2026-08-26","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/08/mediatek-s-ai-asics-growth-to-offset-smartphone-weakness","excerpt":null,"as_of":"2026-08-26","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"凱基預期 2027 年手機占比可能首次降至 50% 以下","source":"中時 wantrich","url":"https://wantrich.chinatimes.com/news/20260529900583-420101","excerpt":null,"as_of":"2026-05-29","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"亞系外資6月底將聯發科目標價由5850元上修至10000元，為外資圈最高；2028年ASIC營收預估由180億美元上調至400億美元","source":"自由時報 焦點股》聯發科：外資送暖 訂出10000元驚天目標價","url":"https://ec.ltn.com.tw/article/breakingnews/5487324","excerpt":"焦點股》聯發科：外資送暖 訂出10000元驚天目標價 2026/06/29 09:35 加入Google首選 留言 聯發科AI ASIC業務前景備受外資看好。（記者卓怡君攝） 〔記者卓怡君／台北報導〕IC設計龍頭聯發科（2454）上週五因對手高通搶進AI ASIC市場，拿下Meta大客戶，引發市場緊張，聯發科股價被摜至跌停，不過，亞系外資出具最新報告，看好聯發科受惠於下一代TPU與市占率提升，ASIC業務的營收表現明顯優於先前預期，將2028年ASIC營收預估由原先的180億美元，大幅上修至400億美元，同時也有望接到新的大型CSP（雲端服務供應商）客戶，目標價從5850元上修至10000元，調升幅度高達71%，創下外資圈最高目標價。","as_of":"2026-06-29","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"瑞銀將目標價調升至6500元，為法人圈最高；大摩上修至5588元","source":"財報狗 聯發科獲外資調升目標價至 6500 元","url":"https://statementdog.com/news/16874","excerpt":"聯發科獲外資調升目標價至 6500 元 蔡明介高喊迎接「史普尼克時刻」 發佈時間：2026/06/24 · 編輯整理 Celine 聯發科 AI TPU ASIC 目標價上調 AI晶片 半導體 手機晶片 智慧型手機 HPC 衛星通訊 ABF載板 先進製程 先進封裝 6G NTN 5G AI伺服器 矽智財 光通訊 更多題材 外資密集調升目標價 大摩列首選股 IC 設計龍頭聯發科（2454）近期成為外資圈追捧焦點，在手機晶片需求回穩之際，人工智慧（AI）特殊應用晶片（ASIC）、Google TPU 專案以及產品漲價效應，被視為未來幾季的成長新動能。 瑞銀證券最新將聯發科目標價大幅調升至 6500 元，創下目前法人圈的最高水準；摩根士丹利則在一個月內兩度上修目標價至 5588 元，並將聯發科列為大中華半導體的首選股，顯示市場對其 AI","as_of":"2026-06-24","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"聯發科2025年12月營收512.66億元，月增9.32%、年增22.99%","source":"TechNews 聯發科12月營收","url":"https://finance.technews.tw/2025/12/10/mtk-2454-202511-financial-report/","excerpt":"聯發科11月營收468.96 億元 作者 TechNews 財報助手 | 發布日期 2025 年 12 月 10 日 17:10 | 分類 財報快訊 Loading... 聯發科（2454）今（10）日公布 11 月營收，達 468.96 億元，較 10 月成長 -9.9%，較去年同期成長 3.7%，累計前 11 月營收為 5,447.00 億元，年增 11.4%。","as_of":"2025-12-10","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"MOPS近12個月122則重訊中，標題含併購／訴訟／停工／裁罰／重編等關鍵字者僅7則，皆為子公司內部合併（翔發投資與聚星電子簡易合併，皆間接100%持股）或轉投資匯頂股份處分，無對外併購、訴訟、裁罰、重編標題。","source":"公開資訊觀測站 歷史重大訊息清單（近12個月）","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2454","excerpt":"【程式統計】公開資訊觀測站「歷史重大訊息」（t05st01），2025-11-02 至 2026-11-02 共 122 則；標題含關鍵字（併購、合併、收購、處分、訴訟、仲裁、停工、工安、裁罰、重編、異常、更正等）者 7 則，未含者 115 則。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026年5月上旬聯發科被列為處置股（分盤交易），金管會表示將督導交易所檢討注意股制度並評估縮短處置期間；屬交易制度事件，非公司財報或裁罰。","source":"經濟日報／聯合理財網 避免聯發科變處置股重演 金管會將縮短處置時間","url":"https://money.udn.com/money/story/5607/9558192","excerpt":null,"as_of":"2026-06-10","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-05-29重訊：子公司翔發投資與聚星電子（皆間接100%持股）簡易合併，屬集團內部組織調整；無對外併購或公開收購紀錄。","source":"公開資訊觀測站 重大訊息：翔發投資公司公告與聚星電子公司之簡易合併案","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2454","excerpt":"翔發投資(股)公司及聚星電子(股)公司皆為本公司間接持股100%之子公司，依企業併購‎法第19條進行簡易合併，係為集團內部組織架構調整","as_of":"2026-05-29","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"近12個月MOPS重訊標題無訴訟、仲裁類；搜尋亦未見投保中心團體訴訟。","source":"公開資訊觀測站 歷史重大訊息清單（近12個月）","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2454","excerpt":"標題含關鍵字（併購、合併、收購、處分、訴訟、仲裁、停工、工安、裁罰、重編、異常、更正等）者 7 則，未含者 115 則。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月MOPS重訊標題無裁罰、重編類；搜尋未見財報重編或非無保留意見。","source":"公開資訊觀測站 歷史重大訊息清單（近12個月）","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2454","excerpt":"標題含關鍵字（併購、合併、收購、處分、訴訟、仲裁、停工、工安、裁罰、重編、異常、更正等）者 7 則，未含者 115 則。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"2454.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":46.28,"operating_margin_pct":15.13,"fcf_margin_pct":13.34,"rd_intensity_pct":25.83},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2454.TW","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"QCOM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":54.23,"operating_margin_pct":23.28,"fcf_margin_pct":23.64,"rd_intensity_pct":22.45},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.QCOM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"3661.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.2,"operating_margin_pct":24.0,"fcf_margin_pct":-10.46,"rd_intensity_pct":9.17},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3661.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"3443.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.95,"operating_margin_pct":13.0,"fcf_margin_pct":7.38,"rd_intensity_pct":8.61},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3443.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"2454.TW"},"financial_history":{"ticker":"2454.TW","currency":"TWD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":548796030000.0,"revenue_yoy_pct":null,"gross_margin_pct":49.36,"operating_margin_pct":23.1,"net_income":118141106000.0,"diluted_eps":74.23,"free_cash_flow":125668297000.0,"fcf_margin_pct":22.9,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":433446330000.0,"revenue_yoy_pct":-21.02,"gross_margin_pct":47.84,"operating_margin_pct":16.58,"net_income":76978637000.0,"diluted_eps":48.34,"free_cash_flow":149264141000.0,"fcf_margin_pct":34.44,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":530585886000.0,"revenue_yoy_pct":22.41,"gross_margin_pct":49.64,"operating_margin_pct":19.29,"net_income":106386578000.0,"diluted_eps":66.78,"free_cash_flow":133541821000.0,"fcf_margin_pct":25.17,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":595965682000.0,"revenue_yoy_pct":12.32,"gross_margin_pct":47.5,"operating_margin_pct":17.36,"net_income":105319255000.0,"diluted_eps":66.03,"free_cash_flow":137373283000.0,"fcf_margin_pct":23.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/2454.TW/2454.TW_Q3_2026_Earnings_Call_20261030.md）

# Q3 2026 Earnings Call
**MediaTek Inc.** | Earnings Calls | 2026-10-30

**Operator** (Operator):
Welcome to the MediaTek 2026 Third Quarter Investors Conference Call. Financial results and presentations for today's call are available on the Investors section of the company website at www.mediatek.com. 
And now I would like to turn the call over to Ms. Jessie Wang, Deputy Director of Investor Relations. Ms. Wang, please go ahead.

**Jessie Wang** (Executives):
Good afternoon, everyone. Joining us today are Dr. Rick Tsai, MediaTek's CEO; and Mr. David Ku, MediaTek's CFO. Mr. Ku will report our third quarter results, and then Dr. Tsai will provide our prepared remarks. After that, we will open for Q&A.
As a reminder, today's presentation will provide forward-looking statements based on our current expectations. The statements are subject to various risks and factors, which may cause actual results to differ materially from the statements. The presentation material supplement non-TIFRS financial measures. Earnings distribution will be made in accordance with financial statements based on TIFRS. For details, please refer to the safe harbor statement in our presentation slides. 
In addition, all contents provided in this teleconference are for your reference only, not intended for investment advice. Neither MediaTek nor any of independent providers is responsible for any actions taken in reliance on content provided in today's call. 
Now I would like to turn the call to our CFO, Mr. David Ku for the third quarter financial results.

**David Ku** (Executives):
Thank you, Jessie. Good afternoon, everyone. Now let's start with the 2026 third quarter financial results. The currency used here is NT dollar and the average exchange rate for this quarter was TWD 31.99 to USD 1. Revenue for the quarter was TWD 168.1 billion, up 10.4% sequentially and up 18.3% year-over-year. Gross margin for the quarter was 46.3%, up 0.1 percentage points from the previous quarter and down 0.2 percentage points from the year ago quarter. 
Operating expense for the quarter were TWD 50.7 billion compared with TWD 47.4 billion in the previous quarter and TWD 43.9 billion in the year ago quarter. Operating income for the quarter was TWD 27.1 billion, up 18.5% sequentially and up 22.2% year-over-year. Non-TIFRS operating income for this quarter was TWD 27.9 billion. Operating margin for the quarter was 16.1%, up 1.1 percentage points in the previous quarter and up 0.5 percentage points year-over-year. Non-TIFRS operating margin for the quarter was 16.6%. 
Net income for the quarter was TWD 28.2 billion, up 14.6% sequentially and up 10.8% year-over-year. Non-TIFRS net income for the quarter was TWD 28.9 billion. Net profit margin for the quarter was 16.8%, up 0.6 percentage points from the previous quarter and down 1.1 percentage points year-over-year. Non-TIFRS net margin for the quarter was 17.2%. EPS for the quarter was TWD 17.5, up from TWD 15.28 in the previous quarter and up from TWD 15.84 in the year ago quarter. Non-TIFRS EPS for the quarter was TWD 17.92. A reconciliation table for our TIFRS and non-TIFRS financial measures is attached in our press release for your information.
And that concludes my comments. Thank you.

**Jessie Wang** (Executives):
Thank you, David. And now I would like to turn the call to our CEO, Dr. Rick Tsai, for prepared remarks.

**Lih Shyng L. Tsai** (Executives):
Good afternoon, everyone. Thank you for joining us today. MediaTek third quarter revenue exceeded our guidance range again, achieving TWD 168 billion with an 18% year-over-year growth. This was primarily driven by the better-than-expected customer demand and improving supply. Gross margin for the quarter was in line with our prior expectations. 
During the quarter, we successfully completed an overseas convertible bond offering of USD 3.9 billion with participation from NVIDIA and Alphabet. This not only strengthened our partnership with key AI infrastructure partners, but also enhanced our ability to secure capacity for critical components for business expansion. In addition, we continue to drive solid progress in our data center and edge device businesses.
For Data Center, demand for our first AI accelerator remains very strong. We have already commenced initial shipments in September and are confident of delivering USD 2.5 billion revenue in the fourth quarter. For 2027, we expect this program to achieve the high end of our revenue target range of approximately USD 16 billion, representing around 20% of the total AI Accelerator ASIC market. This confidence is underpinned by our solid supply outlook. We are working closely with our supply chain partners for additional capacity to meet the strong customer demand. The successful ramp of our first AI accelerator marked an important milestone, demonstrating our ability to integrate industry-leading interconnect IPs, advanced process and advanced packaging technologies, together with our capabilities to orchestrate global supply chain. We are now able to deliver a highly competitive custom silicon for data centers.
For our second AI accelerator project, the development is progressing well, and we are on track for high-volume production in the first quarter of 2028. This chip is purpose-built to power our customers' next-generation AI infrastructure. MediaTek incorporates cutting-edge technologies across every critical aspect of the design to deliver multiple times higher performance per watt with significantly lower TCO. We expect this project to further strengthen our market position and contribute substantially to our revenue growth. Meanwhile, we continue to make solid progress across key enabling technologies, including 448 gig SerDes, 3.5D advanced packaging and co-packaged optics. We are also broadening our customer base as we expand our business scope beyond silicon to offer more comprehensive system and rack solutions.
We connect custom XPUs to the NVLink ecosystem through our NVLink Fusion partnership with NVIDIA, and we also support UALink for Ethernet-based rack architecture. This creates significant value to our customers by greatly reducing the complexity of deploying AI infrastructure for different architectures and substantially accelerating customers' time to market and time to revenue. We continue to expand engagements with several customers and deepen our collaborations with major industry players across the AI ecosystem. With our proven track record and the substantial value we offer, we believe we will be a trusted long-term partner for data center customers in years to come. 
On the edge computing side, RTX Spark AI PC powered by the N1X chip integrating NVIDIA GPUs with MediaTek SoCs became commercially available in mid-October through major PC OEM partners. RTX Box brings powerful on-device Agentic AI capabilities to users and has received strong market interest. Building on this momentum, development of our second-generation SoC is already underway, further expanding our long-term collaboration with NVIDIA. 
In addition, our flagship Dimensity 9500 is featured in the latest Samsung Galaxy Tab S12 series AI tablets. This marks the third consecutive generation of Samsung AI tablets powered by MediaTek's flagship SoCs. All of these developments underscore the strength of MediaTek's comprehensive AI compute stack from edge to cloud. With our established technology portfolio and strong market presence, we aim to capture the exciting growth opportunities across advanced AI compute, physical AI, automotive and AI infrastructure markets in the future. 
With that, I will now talk about the recent business performance for our 3 revenue groups. In the third quarter, Mobile Phone declined 1% quarter-over-quarter and declined 17% year-over-year, accounting for 37% of total revenue. Flagship outperformed in the third quarter as our customers began to introduce new AI flagship smartphones, powered by MediaTek SoCs, including our first 2-nanometer Dimensity 9600 Pro.
Moving on to Smart Edge platform. This group grew 20% quarter-over-quarter and grew 63% year-over-year in the third quarter, accounting for 58% of total revenue. The significant year-over-year growth was partially driven by the volume production of several new projects, including 5G SIM modem for new smartphone customer, new AI tablets, AI PCs and automotive cockpit. Our TV SoC revenue also increased, reflecting higher DRAM content than a year ago.
Moving on to Power IC. This group grew 1% quarter-over-quarter and 18% year-over-year in the third quarter, accounting for 5% of total revenue. The year-over-year growth was mainly driven by share gains in data center-related business. Moving to guidance, driven by the ramp of our AI accelerator business, we expect strong sequential revenue growth in the fourth quarter despite a high base in the third quarter. Our underlying growth would have been even stronger without the seasonal softness in consumer electronics. Quarterly gross margin is expected to be within the current range. We expect our fourth quarter revenue to be in the range of TWD 210.1 billion to TWD 221.8 billion, grew 25% to 32% sequentially and up 40% to 48% year-over-year at a forecasted exchange rate of TWD 31.7 to USD 1.
Gross margin is forecasted at 45%, plus or minus 1.5 percentage points. And operating expense ratio is forecasted at 26%, plus or minus 2 percentage points. Based on our fourth quarter guidance, we now expect our full year revenue growth to exceed our previous target of high single-digit percentage growth in U.S. dollars. This again showcases the solid foundation MediaTek has built for the AI era, including our diversified edge AI portfolio and our strong capability to deliver value in data centers. We believe our expanding presence across edge and cloud will pave the way for MediaTek's sustainable growth in the era of ubiquitous AI.
This concludes my prepared remarks. Thank you.

**Jessie Wang** (Executives):
Thank you, Rick. Operator, we are now ready for Q&A session. May we please have the first question.

**Operator** (Operator):
[Operator Instructions]  First one to ask questions, Gokul Hariharan from JPMorgan.

**Gokul Hariharan** (Analysts):
Congrats on your start of your data center ASIC shipments as well. My first question is actually on your second-generation data center ASIC. There's been a lot of talk in the market about potential delays in design and tapeout. So you just reaffirmed your previous guidance that you are ready for HBM in early 2028 or Q1 2028. Could you talk a little bit about any changes in schedule you have seen? And what exactly are the potential kind of milestones that you're watching for here? And could you also take a quick stab at what your revenue and the market share or TAM and market share potential is going to be in 2028 as you ramp this second generation ASIC, which is definitely higher ASP and higher performance?

**Lih Shyng L. Tsai** (Executives):
Thank you for the question. Let me first address the second ASIC product accelerator. As I said in my remarks, it is on track, on schedule. We understand there's some noise about the tapeout schedule. What I want to say, clearly, I cannot say how many dies are on the chip for these very, very advanced HPUs, you all know there are multiple dies on the chip. And I can say, clearly, also a couple of dies have been taped out already. The big, obviously, much more complex die will tape out also on schedule. Because it's big and complex, it will take a couple or 3 weeks longer than the other dies. So we are very happy with the progress. I think both our partners, our customers and our team are performing tremendously well, and they have been collaborating tremendously well so that these tapeouts of such complex dies are very challenging. And those dies -- my hats off for them, they are making their schedules. About...

**Gokul Hariharan** (Analysts):
The revenue guidance actually for second quarter?

**David Ku** (Executives):
Maybe I'll take that. Gokul, normally actually we don't give out the detail for '28. But I think the better way to think about that actually is -- I think we're kind of talking about for '27, like risk guidance. Right now, we are aiming for the higher end of the TWD 16 billion range. And for year 2028, we're looking for another year of strong growth, okay? So I think probably the better way to think about that because the reason we don't want to give out the detail is actually '28, there are so many moving pieces on the supply chain situation. We are still in the process of finalizing the supply chain situation. But overall, it's going to be another year of strong growth for '28 versus '27 based on the demand profile.

**Gokul Hariharan** (Analysts):
Got it. Maybe also on the second generation, I think there have been so many discussions about the packaging choices you are making with the U.S. IDM vendor. How confident are you now in terms of the packaging choice? Or do you think that you will still need to hedge your bets a little bit given the supply chain situation that you mentioned? And do you think that is the primary limiting factor in terms of your ability to service the demand from your customers given in that second generation chip, you will be the primary vendor for that customer when you need AI shipment?

**Lih Shyng L. Tsai** (Executives):
Gokul, right now, we are working on this U.S. IDM packaging process. That's our absolute priority. Actually, we now have a very strong manufacturing team within MediaTek team, led by actually some very experienced staff operating executives, I would say, retired. And we are working very closely with the IDM partner and substrate suppliers, first and foremost, on the yield improvement. I'm glad to say that -- many of you know my background, I came from manufacturing. I have seen the progress. I have witnessed the clear identification of the key difficulties and also the way people are working together to resolve the problem and implement them in the factory. I have very high confidence that the yield will go up very quickly because once we figure out a couple of 2 or 3 key problems, once they are implemented, the yield will go up quite quickly, and we will continue to explore the next level of sources of effects. But these are the things that we have seen before, we have done before. I'm very happy that our own team, we're working with the Japanese supplier, we're working with Taiwanese supplier and we're going to make the second generation of ASICs a great success.

**Operator** (Operator):
Next one to ask questions is Sunny Lin from UBS.

**Sunny Lin** (Analysts):
Congrats on the very good progress for your key ASIC programs. so my first question is on maybe the -- even the third-generation ASIC. I know it's a bit far away, but it's also pretty essential for us to think about your ASIC revenue sustainability in the coming few years. So for that one, maybe ramping in late 2029, any progress that you could share with us? How is MediaTek positioned against the competition? And how should we think about the overall TAM for MediaTek to continue to grow into '29 and '30?

**Lih Shyng L. Tsai** (Executives):
We certainly cannot speak for our customers. But we can say we are working very closely with them on the next-generation ASIC. Again, our customer is very aggressive in moving forward and upward in the performance -- downwards for the TCO, I guess. So this is going to be another challenging chip. So I think it takes some time to define, to finalize the definition.
So right now, as you said, we are very busy in getting our first one right now in mass production and second one into production. And we will be happy to discuss with you about the next one when time is right. But as I said, I'd like to remind you, as I said in my remarks, the second-generation ASIC is a very powerful chip from both performance per watt point of view and also from the lower TCO point of view.

**Sunny Lin** (Analysts):
Very helpful. So my second question is, earlier, you talked about potential for new clients and several engagements for cloud ASIC. So any color you could share with us in terms of the progress that you're making for new projects? And how should we think about maybe the combined addressable market for new projects and the potential sales that you could recognize maybe in '27?

**David Ku** (Executives):
Sunny, I think we just confirmed. We do have the second customer, okay? The new project right now is kicking off and working on right now. We're talking about going to see the first revenue coming in, in 2028. Again, normally actually [indiscernible] disclose more detail later on, but this is just to confirm. We do have a second customer and [indiscernible] revenue coming in 2028.

**Sunny Lin** (Analysts):
Got it. So second customer is different customer from the key projects that you are referring to, right?

**David Ku** (Executives):
Yes, second customer, so a different customer.

**Operator** (Operator):
Now we have Haas Liu from Bank of America.

**Haas Liu** (Analysts):
Congrats on the great results. I would like to start with your near-term ASIC outlook. You provided new USD 2.5 billion guidance for cloud ASIC contribution for this year, which is better than your previous guidance of slightly higher than $2 billion. I was just wondering, what drives the incremental strength? Is it because the smooth production ramp driving the unit upside or the chipset pricing upside reflecting the cost hike?
And relatedly, with cloud ASIC reaching 30% of your quarterly revenue in fourth quarter this year, I was just wondering, it is, of course, very encouraging to see that your gross margin is still kept at 44% to 46% range. But just wondering if you could provide more detail on the factors keeping your margins resilient during the quarter.

**Lih Shyng L. Tsai** (Executives):
Well, our latest -- today's guidance for fourth quarter $2.5 billion indeed comes from a very robust customer demand. And with a robust customer demand, actually, we have been working very hard with our supply chain partners. And I'm also very glad to say that although -- you probably understand how hard nowadays to get the right amount of supply in order to meet the demand. And I'm very happy that our team has been successful in rounding up multiple various suppliers such as, for instance, substrates, which is usually one of the most difficult things to do. So we continue to perform. Our team and I would certainly hope and expect we do that going forward.

**David Ku** (Executives):
Yes. For the gross margin, actually, we kind of give out the guidance early on for the blended gross margin. On the data center side, currently is still below the corporate average. So that's why you see for our guidance, actually, we guide down a notch, 1 percentage point. And on top of that side of that, we also have some price adjustment in order to reflect about the cost increase for the whole supply chain. So on a blended basis, actually, that's actually the guidance we give out. And again, we want to highlight the focus for the new data center business. I think we really see this as very accretive on the operating margin side. And as you can see, starting from fourth quarter and likewise starting from next year, I think that will be the focus.

**Haas Liu** (Analysts):
Okay. Got it. So just a quick follow-up on that commentary that your operating margin for the ASIC business is already going to be accretive as compared to your corporate average starting from fourth quarter. Is that the correct understanding?

**David Ku** (Executives):
Yes. Starting from fourth quarter, the operating margin will become accretive to the overall company.

**Haas Liu** (Analysts):
Okay. Got it. And my second question is just a follow-up on the second customer for the ASIC business that you mentioned that the mass production timing or the revenue contribution from production for that project, new project, new customer is going to pick up in 2028. Does that suggest that the chipset is already under design milestone? Or how should we read it?

**David Ku** (Executives):
Yes. Actually, I think the [indiscernible] side kicked off already. Again, we will provide more detail later on.

**Operator** (Operator):
Next one to ask question, Charlie Chan from Morgan Stanley.

**Charlie Chan** (Analysts):
I actually have several follow-ups, if I may. So first of all, on the operating margin implication, right? I mean the guidance implied fourth quarter operating margin to be around 19%. So if I think about the data center revenue like 30% of your total revenue, then it seems to be like your AI data center operating margin is like 10% above corporate average. Is that the right way to think about it? Or you'll be even more accretive when the project goes for a higher scale?

**David Ku** (Executives):
I'm sorry, Charlie, can you repeat. You say -- I didn't hear it clearly. You said our operating margin for data center was 10% or 10% higher?

**Charlie Chan** (Analysts):
10% higher than corporate average based on your first quarter revenue mix and your fourth quarter operating margin guidance.

**David Ku** (Executives):
Okay. First of all, I think it's higher. We probably won't be able to quantify that because actually as I explained in fourth quarter, we also have the effect of our price adjustment starting from third quarter for non-data center business as well. But overall, it's higher, it's higher, but we will not be able to comment on the magnitude of the operating margin for the intangible other segment.

**Charlie Chan** (Analysts):
Okay. And can I say my next two questions because I love to know the answer for both. One is also a clarification about your second customer. Can you give a little bit color? Is that kind of AI lab type of customer? Is that kind of related to your recent NVLink Fusion progression? Can you give us a little bit more color about this second customer?
And also a question to Rick, right? So I think the recent capital market seems to be very concerned about Neocloud financing ARR deceleration. So there is some concern about AI infrastructure slowdown, right? So I want to get management's view about if CSPs CapEx will slow down or cut? Do you think customers will prioritize GPU, which is more general purpose or they should prioritize their own ASIC for the future spending in a better market?

**David Ku** (Executives):
So Charlie, maybe the first customer, again, currently, we probably won't be able to provide more detail. But yes, I think in general, maybe the easy way to think about it. I understand there are some rumors out there, at least one can say the second customer is not coming from China, okay? Maybe that market, we can talk about that. For any more detail, please bear with us. Actually, we'll provide more detail later on.

**Charlie Chan** (Analysts):
Got you. And can I get management's view about what would be prioritized? Is that ASIC or GPU if the CSPs budget is going to shrink?

**Lih Shyng L. Tsai** (Executives):
Well, Charlie, Yes, there's certainly quite a bit of a market movement, there's no question about it, during the last several weeks almost. But my view is if we look at it 1 year, 2 years out, maybe even up to 3 years out, the demand growth for AI, which means the demand growth for compute will continue, absolutely sure. The rate of which may vary somewhat. But if you look at from a TAM point of view, it's a huge TAM. It's a huge TAM. And what we definitely focus on is to ensure we are working with the first-class customer -- first-class products that will stand the test to usage criteria and the test of time, but it's very accurate, I think. As I said again in my remarks, the chips we're designing and making together with our customers, really powerful chip.
So especially during the tough time, those chips will win out. Of course, I'm absolutely sure also GPU will -- they will also have very great chips too. But I cannot say every other chip will be successful. I'm very sure the chips we are making is already very successful and will be very, very competitive in this kind of a rocky market in the next year maybe. But I'm actually -- I've been thinking about that. And I'm quite confident that the MediaTek will come out better and stronger.

**Operator** (Operator):
Next one to ask questions, Robert Sanders from Deutsche Bank.

**Robert Sanders** (Analysts):
I guess you seem pretty dependent on [indiscernible] right now. If I was working at Intel, I would probably tell Google in the future that there are only packaging deals if you use our foundry, which would obviously have implications for you because it would force you to work with Intel's front-end foundry, which is obviously more dangerous given their execution. Would that be something that concerns you about your dependency on [indiscernible]?

**Lih Shyng L. Tsai** (Executives):
First of all, we are not dependent on one supplier. It is critical to make it clear. We continue -- I mean, [indiscernible] TSMC is our most important partner. So we definitely -- what we are doing is the market is expanding so fast, the customer's requirement becoming so -- or they change also so fast. And we actually -- as a very capable supplier, we are -- how should I say, we are adapting those challenges to make good powerful chips for our customers whatever they would like to choose. I think -- I would really credit that as a major capability for MediaTek. However, we also understand clearly TSMC is our most important partner. And we are working with them closely in every part of the, I should say, technology chain. So packaging has become a major redefining technology for this AI era and MediaTek is investing in money, especially in people and in our ecosystem partners relationship.

**Robert Sanders** (Analysts):
Just as a follow-up. In terms of these frontier model custom silicon projects, your major competitor is using financing, a very aggressive financing, buy now, pay later type terms. I know you have a small financing and you raised this debt. But is it worth even engaging with these loss-making frontier model companies given the sort of scale of the balance sheet support that your competitor is using? Or do you think it's still worth engaging with these companies given the smaller relative size?

**David Ku** (Executives):
Well, Robert, I think the market is so dynamic right now. You're talking about all of -- depends on somebody call vendor financing or support by chipset vendors. I think if it's necessary, I think we will consider as well because actually right now, especially due to the new frontier models, at least one of the new frontier model is actually about to file IPO. We're going to see more and more [indiscernible] information coming out. We actually see quite a few positive signals. For example, for the revenue return versus the CapEx investment, obviously, we see quite a big improvement quarter-over-quarter in the last 6 quarters. So with that trend, I mean, we still strongly believe for the CapEx invest regards of CSP or frontier model, you will generate enough revenue and cash flow to fulfill that. But actually, there's a transition period to support that CapEx spending in order to reach the final stage or stable stage of our cash generating.
So again, just to go long way to answer your question is if the market required and more importantly, if we have the right customer, okay, and actually, we will consider as well.

**Operator** (Operator):
And right now we have Arthur Lai from Macquarie.

**Yu Jang Lai** (Analysts):
Congrats on strong fourth quarter OP margin bit. And question number one is on the OP margin discussion. Number two is on the technology learning curve. So starting from number one, if you look at the Q3 OP margin and Q4 OP margin, can you give us a long-term OP margin guidance? Or how we think of the Q4 OP margin is sustainable? How should we forecast?

**David Ku** (Executives):
I think, first of all, long answer short, I think Q4 operating margin -- Q4 should be the starting point people to see improving operating margin, okay? So it's not going to be just sustainable. I think we are looking for continuing to enhance given that we're going to ship more on the top line, okay? And so it is sustainable and also we're looking for continuing to improve.
And if we talk about next year guidance for the operating margin, I think overall, we are looking for 20% plus, okay, if not slightly higher. Again, the reason we probably wanted to give out the detailed guidance because there are still some moving pieces. But overall, we feel comfortable for the full year basis. Next year, the operating margin should be above 20%. So from a year-over-year perspective, we're going to see a pretty good [indiscernible]. That's on the operating margin side. And again, that's all in line with what we talked about, right now, probably almost like 1.5 years ago, we say the business model or the new business model, if you like, we're adopting right now is actually the gross margins compared to what we have right now may be slightly dilutive, but operating margin will be impressive. I think that's the strategy of the business model.

**Yu Jang Lai** (Analysts):
Yes. That's great. Second question is a follow-up on Rick's opening remarks. You mentioned that we are doing the leading tech. And I think the investor actually asking about the [indiscernible] technology and also HBM5. And if we think about maybe 2 years later, your company probably will believe only one who have wherewithal to handle these 2 technologies with a track record. So [indiscernible], how is the entry barrier investors should think if you already handle this tough technology and how many years you will be ahead of your major competitor?

**Lih Shyng L. Tsai** (Executives):
It's a good and tough question. I want to be careful in responding to your question. We are quite excited about our progress in the multiple fronts of the technology capability required for such complex and dynamic AI era. And you mentioned the packaging capability, the HBM5, and I think we have the world-class state-of-the-art 448 gig, a tremendous power consumption -- low power consumption capability, for instance. But I think on top of those things, the capability to integrate all those technology capabilities and make them into highly manufacturable, scalable products for our customers, for them to be successful, that is and will continue to be the barrier, the competitive barrier. It's many things together, not just one thing or 2 things. And we also recognize we have very strong, competitive competitors. So we will not think that we will be very much ahead of our competitors. We always have a very tough fight against our competitors. And I'm very sure we will win our part of the business.

**Operator** (Operator):
Now we have Gokul Hariharan from JPMorgan.

**Gokul Hariharan** (Analysts):
First of all, on the NVLink Fusion partnership, Rick, could you -- I know that you cannot talk about the specific ASIC yet. But could you give us a little bit more pointers in terms of how you are integrating NVLink Fusion? And what are the benefits your customers could be getting? I think one of the factors that your competitor has is definitely their scale-up technology based on Ethernet. So does this completely kind of balance out the potential kind of networking-related edge that your competitor has when it comes to new customer engagement?
And maybe also talk a little bit about the customer interest levels for this NVLink Fusion-enabled ASIC offering that you're bringing to the market.

**Lih Shyng L. Tsai** (Executives):
Gokul, first, NVLink Fusion model, of course, it's a business model, but with a very, very high and strong technical content. So let's talk about technical content first. I think you mentioned the credentials. I can say, I think, clearly that with NVIDIA and MediaTek together, I think our credentials can match anybody in the business, in the market. That I think I can say in confidence.
So secondly, I think the thing we're doing -- the value of the model, as I said in the remarks and also actually back in the announcement of the collaboration in one of the interviews, I always stress that we can accelerate, we can enable customers' time to market and time to revenue, time to money. And so we work together with NVIDIA first to build a chassis with which the customer can really -- I wouldn't call that plug in, but it will be much more easily putting their design, either XPU or CPU or some other Us and fit into a rack and sell the rack for instance. So that's the essence, I think, of this business model. There are a lot of other things we must do together to convince the various potential customers to adopt such model.

**Gokul Hariharan** (Analysts):
Got it. Any initial feedback that you're hearing from the customers on this model now?

**David Ku** (Executives):
Yes. Gokul, right now, we are in discussion together with NVIDIA with several potential customers. I think overall, some of the customers like it. I think one of the key advantage about having the NVLink switch or NVLink Fusion model is for potential customers, I think their time to computation power is actually much, much faster. Because traditionally, they've been working on the chipsets first, what we call the packaging, then talk about the system. So it sometimes takes a long time for an idea to computation power online. But with NVLink fusion that provides a great advantage for time to computation power. And given the strong demand on the end market side, I think that provides a lot of opportunity. So we got a pretty good positive feedback. I think it's hopefully in the near term, we can officially announce some case, okay.

**Gokul Hariharan** (Analysts):
Got it. That's very [indiscernible]. Maybe second question, just wanted to address, again, the second-generation ASIC as a much more powerful, much better TCO kind of chip. What does it do to your competitive position within this customer? Like do you think that you will kind of become like the majority source when it comes to 2028 because there's a lot of discussions around this, as you can imagine. So this generation, obviously, you've proven with the ramp in Q4. But could you talk a little bit about your competitive position within this lead customer when it comes to the second generation?

**David Ku** (Executives):
Sure. Gokul, I think the key is really just like Rick talked about during the opening remarks for the second generation or the second project, I think the performance is multiple times better on the performance per gigawatt, which also mean much better TCO. And to be honest, actually, based on what we see on the so-called competing projects, they're actually not even close from the overall performance perspective. On that one, actually, we feel very comfortable, very comfortable. Because by the end of the day, the market is looking for the performance and TCO. And as long as our product can win from that front, I think we feel comfortable.

**Operator** (Operator):
With the interest of time, we are going to take the last question and also returning to Q&A, Charlie Chan, Morgan Stanley.

**Charlie Chan** (Analysts):
So I want to ask about the 448 gigabit SerDes. And we know is that for the third-generation project with major customer or it will be applied for this circular second customer? Can you clarify your progress for 448 gigabit SerDes adoption.

**Lih Shyng L. Tsai** (Executives):
Yes. Well, first of all, we certainly serve our current customer first and 448 is a must going forward with a very stringent [indiscernible] design with a very stringent power consumption requirements that we have taped out already. So we are quite [indiscernible] takes measurement, verification, all those things, but we -- our service team is very, very capable, and they have done this multiple generations. They know what they're doing. And I'm very confident that we will deliver 448 gigabit SerDes. It will not be on the critical path. And in addition, we will work on -- we will use this IP to put in some extra work so that it has the right interoperability for the broader customer base going forward.

**Charlie Chan** (Analysts):
And we are also looking forward to your more projects, not just the NVLink Fusion that you just mentioned, but we believe you have a great opportunity with other U.S. CSP or AI Lab customers. But for this already announced second customer win, maybe get a rough kind of revenue size or margin profile. For example, compared to your ASIC revenue this year is around USD 2 billion in the first year, right? So if you think about the second customer in 2028, would there be a bigger revenue size? And would the margin profile be similar?

**David Ku** (Executives):
Right now, it's a little bit too early to talk the detail. But in general, I guess, actually the demand that the customer would like actually is pretty strong. But again, for 2028, we are still in the process about finalizing the supply. So we probably will provide some more detail later on. But so far, as you can see from the marketplace, everyone is talking about further increase the CapEx and demand.
So if we only judge from demand side, that looks good, but we also need to take into consideration about the other half as well. So give us some more time, we will come back with some more clarification. But right now, the key is really '26, we delivered a great result of $2.5 billion for just -- mainly for fourth quarter. Next year, we actually talking about the high end of the guidance. And once we can deliver that, we're going to be based on a pretty solid ground to deliver the new revenue for 2028 and beyond.

**Charlie Chan** (Analysts):
Yes, David, you mentioned about substrate several times that is a key factor, right? So just in case, if TSMC supply cannot fulfill customers' demand, do you think your current sort of first-generation project will extend the life cycle or the demand will go to your competitor in the U.S. using TSMC cohorts?

**David Ku** (Executives):
I think for current generation, the demand looks good and also like with the guidance we gave out, actually, we should feel fairly comfortable to deliver what the customer want for Gen 1. For Gen 2, based on the current yield profile and also tied to market, I think we still feel comfortable to deliver what the customer want basically. In the meantime, as you can guess, the customers actually for the second generation, they are looking for the upside. So we are still working with our supply chain partner to provide upside.
But I think overall, the key is really go back to my earlier comment, the performance we can deliver together with our customers right now, you can't really find some kind of replacement or the substitute of it. I think that's the key.

**Operator** (Operator):
Ladies and gentlemen, we thank you for all your questions. Now I'll hand it over to Ms. Jessie Wang for closing comments. Ms. Wang, please proceed.

**Jessie Wang** (Executives):
Ladies and gentlemen, this concludes MediaTek 2026 Third Quarter Conference Call. An audio replay will be available in 1 hour after the call at the Investors section of MediaTek's website. We would like to thank you for your participation, and you may now disconnect.

**Operator** (Operator):
Yes. We thank you again for your participation in today's conference. You may disconnect now. Thank you, and goodbye.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 2454.TW_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜CEO｜guidance：Q3 營收財測區間（匯率 32）（原話："in the range of TWD 152.2 billion to TWD 159.8 billion"）
- 2026-07-31｜CEO｜guidance：Q3 毛利率財測 46% ±1.5pp（原話："Gross margin is forecasted at 46% plus or minus 1.5"）
- 2026-07-31｜CEO｜guidance：全年營收目標改為區間高標（原話："achieve the high end of our full year revenue target range"）
- 2026-07-31｜CEO｜guidance：全年毛利率落在當季財測區間內（原話："we aim to deliver our full year gross"）
- 2026-07-31｜CEO｜guidance：Q3 手機營收預期（原話："flat to decline mid-single-digit percentages sequentially"）
- 2026-07-31｜CEO｜guidance：Q3 Smart Edge 營收預期（原話："Smart Edge Platforms revenue to grow mid- to high"）
- 2026-07-31｜CEO｜guidance：Q3 Power IC 營收預期（原話："Power IC revenue to be flattish sequentially"）
- 2026-07-31｜CEO｜guidance：資料中心 2026 營收預期（原話："data center revenue to exceed $2 billion in 2026"）
- 2026-07-31｜CEO｜guidance：2027 SAM 估計與市占目標上調（原話："we now believe the 2027 SAM to be USD 80 billion"）
- 2026-07-31｜CEO｜guidance：全年智慧手機出貨預期不變（原話："expect the market to decline by about 15% in units this year"）
- 2026-07-31｜CFO｜margin：Q2 毛利率年減原因：去年同期一次性利益（原話："mainly due to a one-time benefit in the year-ago quarter"）
- 2026-07-31｜CEO｜margin：Q2 營收超出財測高標（原話："exceeding the high end of our guidance range"）
- 2026-07-31｜CFO｜margin：漲價目的是轉嫁成本（原話："not trying to actually increase the price to increase"）
- 2026-07-31｜CFO｜margin：毛利率目標為維持而非提高（原話："trying to maintain the gross margin rather than increase the"）
- 2026-07-31｜CFO｜margin：ASIC 各世代毛利率相近（原話："the gross margin generation after generation will be similar"）
- 2026-07-31｜CFO｜margin：ASIC 毛利率對公司平均略稀釋（原話："will be slightly dilutive compared to the current corporate"）
- 2026-07-31｜CFO｜margin：營業利益率規模化後增益（原話："once we start to scale, I think it will be accretive"）
- 2026-07-31｜CFO｜margin：費用金額小幅增加、費用率大降（原話："It will increase slightly. But the ratio will come down"）
- 2026-07-31｜CEO｜margin：費用金額成長但費用率下降（原話："It will grow higher, but the ratio will come down."）
- 2026-07-31｜CEO｜commitment：第二顆 ASIC 2028 年量產（原話："the yield and reliability of the second ASIC are on track"）
- 2026-07-31｜CEO｜commitment：第二顆 ASIC 約 2028 年初量產（原話："you can assume early 2028 for early production"）
- 2026-07-31｜CEO｜commitment：第一顆 ASIC 2026 Q4 量產（原話："scheduled to begin in the fourth quarter of this year"）
- 2026-07-31｜CEO｜commitment：2028 SAM 尚未給數字但稱會更高（原話："our 2028 SAM will be quite a bit higher than 2027"）
- 2026-07-31｜CEO｜commitment：2028 營收區間尚未指引（原話："while we are not ready today to guide the 2028 revenue range"）
- 2026-07-31｜CEO｜commitment：448G SerDes 預計明年下半年就緒（原話："next year, maybe second half of next year"）
- 2026-07-31｜CFO｜commitment：營業利益率增益僅給方向（原話："we probably only provide the directional guidance"）
- 2026-07-31｜CFO｜commitment：供應鏈對今明年營收目標有信心（原話："for next year, I think we feel very comfortable"）
- 2026-07-31｜CEO｜commitment：2nm 旗艦 SoC 第三季推出（原話："we will launch our 2-nanometer SoC in the third quarter"）
- 2026-07-31｜CEO｜capital_allocation：董事會核准 50 億美元融資額度（原話："approved a discretionary USD 5 billion financing budget"）
- 2026-07-31｜CFO｜capital_allocation：CFO 說明為備用彈性（原話："really just optionality, a flexing plan"）
- 2026-07-31｜CFO｜capital_allocation：帳上現金 70 億美元以上（原話："ample cash, $7 billion plus on our balance"）
- 2026-07-31｜CFO｜capital_allocation：確認可用於支持供應商擴產（原話："Yes, yes."）
- 2026-07-31｜CEO｜product：SAM 僅含加速器（原話："Right now, it's accelerator only for now."）
- 2026-07-31｜CEO｜product：SAM 不含 HBM（原話："And no HBM."）
- 2026-07-31｜CEO｜product：與 NVIDIA 合作 RTX Spark（原話："collaboration with NVIDIA on RTX Spark"）
- 2026-07-31｜CEO｜product：子系統整合 NVLink Fusion（原話："incorporating NVLink Fusion connectivity onto the subsystem"）
- 2026-07-31｜CEO｜product：由 IP 供應走向機櫃式整合（原話："moving to not only provide very competitive IPs"）
- 2026-07-31｜CFO｜product：CFO 稱 448G 之後需走光學（原話："for beyond that, most likely we need to go on the optical"）
- 2026-07-31｜CFO｜competition：HBM 仍是主流（回應 LPDDR 替代路線）（原話："I think HBM is still a must"）
- 2026-07-31｜CFO｜competition：超大型客戶要求高效能（原話："hyperscalers who actually require absolutely"）
- 2026-07-31｜CEO｜competition：稱目標為優於公平份額（原話："we will get our hopefully, better than"）
- 2026-07-31｜CEO｜risk：封裝技術具高度挑戰（原話："those technologies are very challenging, we all understand"）
- 2026-07-31｜CEO｜risk：手機需求弱因 BOM 成本上升（原話："weak demand as a result of increasing smartphone BOM costs"）
- 2026-07-31｜CEO｜risk：EMIB-T 良率進展獲確認（原話："Yes, in short, yes, you can."）
- 2026-07-31｜CFO｜risk：封裝交期良率準時交付（原話："we're going to deliver this on time"）
- 2026-07-31｜CEO｜risk：邊緣裝置形態未定（原話："the jury definitely is out, still out"）
- 2026-07-31｜CEO｜customer：深化多家資料中心 ASIC 客戶接觸（原話："deepen our engagement with several customers"）
- 2026-07-31｜CEO｜customer：Smart Edge 季增含 TV SoC 的 DRAM 內容（原話："contribution from DRAM content in TV SoC"）
- 2026-07-31｜CEO｜customer：漲價行動反映供應鏈成本（原話："we are taking pricing actions to ensure these increases are"）
- 2026-07-31｜CFO｜customer：不揭露第三代專案（原話："third generation, actually, we won't be able"）
- 2026-07-31｜CEO｜customer：不揭露新技術會用於哪個客戶（原話："I'm afraid we cannot disclose those details."）

### 問答異常語氣（迴避／改口／保留）
- 2454.TW_Q2_2026_Earnings_Call_20260731.md｜問：JPMorgan：第二顆 ASIC 與 2028 SAM/市占，是否可能成為該客戶多數供應商｜答法：CEO 拒絕正面回答是否成為多數來源，改談專注執行與『better than fair share』
- 2454.TW_Q2_2026_Earnings_Call_20260731.md｜問：BofA：資料中心洽談客戶是否含 Tier 2 與企業客戶｜答法：CFO 稱無法提供細節，待可揭露時再說
- 2454.TW_Q2_2026_Earnings_Call_20260731.md｜問：KGI：三大事業群漲價幅度排序｜答法：CFO 表示無法評論，僅稱各事業群大致公平
- 2454.TW_Q2_2026_Earnings_Call_20260731.md｜問：Morgan Stanley：第三代專案是否回 TSMC CoWoS／大光罩｜答法：CFO 稱無法評論第三代，轉談前兩個專案
- 2454.TW_Q2_2026_Earnings_Call_20260731.md｜問：Goldman：營業利益率增益幅度｜答法：CFO 只給方向，不給數字，稱第三季後再說
- 2454.TW_Q2_2026_Earnings_Call_20260731.md｜問：Citi：新技術用於第二顆 ASIC 或其他客戶、明年市占／營收｜答法：CEO 稱無法揭露，明年市占未給數字，僅稱會滿足需求

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
{"date":"20260711","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"ASIC（雲端資料中心）成為第二成長引擎，且不嚴重稀釋整體毛利","columns":{"2Y 驗證點":"2026 Q4 ASIC 單季 ~$2B、2027 資料中心 ~$3.2B","5Y 驗證點":"雲端 ASIC 份額 10-15% 站穩、整體毛利率守 45%+","10Y 驗證點":"ASIC 成第二個 &gt;30% 營收支柱且回報 &gt; WACC","具體數字門檻":"ASIC 2027 營收 ≥ $3B 且合併 GP% ≥ 45%","來源":"公司 Q1 FY26 法說；TrendForce 2026-02；Digitimes 2026-04","漂移觸發":"連 2 季 TTM GP% 偏離 −5% → 削弱"}},{"id":"H2","text":"MediaTek 在 Google TPU 供應鏈的份額不被結構性稀釋","columns":{"2Y 驗證點":"TPU 8i/v7e 量產如期、v9 SerDes 訂單維持","5Y 驗證點":"推論變體 design win 延續到 v8/v9 世代","10Y 驗證點":"成為 Google 長期推論 ASIC 主力之一（非一次性設計費）","具體數字門檻":"2027-28 未出現第三家分食其推論變體份額","來源":"Digitimes 2026-06；TheNextWeb；SemiWiki","漂移觸發":"確認第三家分單 → 反轉"}},{"id":"H3","text":"手機核心業務不硬著陸，旗艦（Dimensity 9500）中國高階份額維持","columns":{"2Y 驗證點":"手機營收年降幅個位數、中國超高階份額 &gt;40%","5Y 驗證點":"手機提供穩定現金流資助 R&D，不拖累整體","10Y 驗證點":"手機成熟但不萎縮，作為 ASIC 的現金牛","具體數字門檻":"手機營收年 YoY 不低於 −10%、中國高階份額不跌破 35%","來源":"Counterpoint Q1 2026；Digitimes 2025-09","漂移觸發":"連 4 季手機營收 YoY &lt; −10% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"ASIC 毛利率稀釋整體獲利——為衝營收接低毛利客製案","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"合併 GP% 趨勢、資料中心 blended 毛利","警戒閾值":"合併 GP% 連 2 季 &lt; 45%"}},{"id":"R2","text":"Google 多元化供應鏈，MediaTek 推論份額被第三家（Marvell）分食","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Google TPU 分單新聞、design win 世代延續性","警戒閾值":"確認第三家取得推論 TPU 分單"}},{"id":"R3","text":"中國高階手機需求走弱或補貼退場，旗艦 SoC 量價齊縮","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"中國超高階份額、Dimensity 9500 出貨、手機營收 YoY","警戒閾值":"連 2 季手機營收 YoY &lt; −15%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"回檔至 FY27 30x（約 $3,150）或 ASIC 量產＋毛利率能見度兌現","irr_base_pct":8.0,"ev5y_pct":36.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.4,"ev5y_pct":36.0,"irr_base_pct":8.0,"max_dd_pct":-60.0,"bull_5y_price":8800,"bear_5y_price":2250,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"回檔至 FY27 30x（約 $3,150）或 ASIC 量產＋毛利率能見度兌現","price_at_dd":3925,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2454.TW_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
