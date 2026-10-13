你是 stock-analyst **v20 判斷 agent**，標的 FIX（20261013）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"FIX","date":"2026-10-13","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FIX_20261013/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FIX_20261013/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":3265.656,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"查無（未取得該季共識）"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":null,"period":"Q2 FY2026（公告於 2026-07-23）","unit":"n/a","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（公告於 2026-07-23）","citation":"公司不揭露 non-GAAP 營業利益；僅揭露 Adjusted EBITDA 600.5M（利益率 18.4%）"},"note":"查無","needs_sonnet":true},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":557.966,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）","unit":"USD M（利益率 17.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"查無"},{"id":"f_kpi5","label":"管理層指引","value":null,"period":"Q2 FY2026（公告於 2026-07-23）","unit":"n/a","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2026（公告於 2026-07-23）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"無數字指引；僅定性：optimistic about our results for the remainder of 2026 and well into 2027","needs_sonnet":true},{"id":"f_kpi6_backlog","label":"Backlog（在手訂單）","value":14060,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）","citation":"公司新聞稿 8-K Ex.99.1；same-store 13,700M"},"note":"查無"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-07-23","period":"2026-07-23","unit":"date","basis":"距今 58 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-07-23"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_fix_gross_margin_pct","label":"FIX 毛利率","value":25.66,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_operating_margin_pct","label":"FIX 營業利益率","value":16.45,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fix_fcf_margin_pct","label":"FIX FCF 利潤率","value":19.24,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eme_gross_margin_pct","label":"EME 毛利率","value":19.43,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eme_operating_margin_pct","label":"EME 營業利益率","value":9.6,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eme_fcf_margin_pct","label":"EME FCF 利潤率","value":6.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_iesc_gross_margin_pct","label":"IESC 毛利率","value":26.31,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IESC.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_iesc_operating_margin_pct","label":"IESC 營業利益率","value":12.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IESC.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_iesc_fcf_margin_pct","label":"IESC FCF 利潤率","value":5.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IESC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_gross_margin_pct","label":"PWR 毛利率","value":15.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_operating_margin_pct","label":"PWR 營業利益率","value":6.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pwr_fcf_margin_pct","label":"PWR FCF 利潤率","value":7.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":999.32,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）","citation":"公司新聞稿 8-K Ex.99.1（營業現金流 1,139.4M − 資本支出 141.4M）"},"note":"查無"},{"id":"f_kpi4_sbc","label":"SBC 占營業利益","value":1.65,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）","citation":"SBC 9.206M 取自 yfinance quarterly_cashflow（新聞稿未揭露），÷ 新聞稿 GAAP 營業利益 557.97M；占營收約 0.28%"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":1638.05,"period":"2026-10-12（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":0.72,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":46.42,"period":"2026-10-12（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（49.01 → 49.01）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（60.18 → 60.18）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（73.85 → 73.85）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":49.01,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":60.18,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":73.85,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":12.33,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 43.63 → 49.01（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":40.31,"period":"2026-10-12（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-12（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.13,"period":"2026-10-12（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-12（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.0,"period":"2026-10-12（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-12（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":35.01,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 49.01，分子＝快照價 1715.69","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.183,"period":"2026-10-13","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-13"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-1536.49,"period":"2026-10-13","unit":"USD m","basis":"yfinance 最新一季：總債務 369.91、現金 1906.4（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":35.19,"period":"2026-10-13","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":56113.58,"period":"2026-10-13","unit":"USD m","basis":"市值 57650.07 ＋ 淨負債 -1536.49","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":12982.38,"period":"2026-10-13","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（10 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":15446.4,"period":"2026-10-13","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（10 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.32,"period":"2026-10-13","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"FIX 2026-06-30 backlog 約 $14.06B，對比 2026-03-31 的 $12.45B 與一年前的 $8.12B；同店 $13.70B（搜尋摘要轉述，非直接份額數據）","source":"Comfort Systems USA Q2 2026 results (BusinessWire / SEC 8-K ex99.1)","url":"https://secure.businesswire.com/news/home/20260723227439/en/Comfort-Systems-USA-Reports-Second-Quarter-2026-Results","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261013","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Zacks 文章列出 FIX 風險包含專案延遲、勞動成本通膨、競爭加劇與執行風險；未量化份額","source":"Nasdaq/Zacks: Comfort Systems Stock Trading at a Premium: Buy, Hold or Fold?","url":"https://www.nasdaq.com/articles/comfort-systems-stock-trading-premium-buy-hold-or-fold","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"同業分析指 EMCOR 為最直接對手，規模較大、服務範圍較廣（含設施維護與更廣電氣足跡），有利爭取多據點超大規模客戶大單；Sterling Infrastructure 為次要對手（資料中心、半導體）；Quanta 偏間接對手","source":"Hudson Labs: comfort systems usa competitors fix peer comparison 2026；Chartmill: EMCOR Expands Into High-Growth End Markets","url":"https://hudson-labs.com/research/comfort-systems-usa-competitors-fix-peer-comparison-2026","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261013","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"單一未具名客戶占 2025 年合併營收約 12.8%（機械部門）；2024 為 13.3%、2023 為 13.8%。第三方風險彙整頁引用 SEC 申報，搜尋結果未將該客戶指認為超大規模雲端業者。","source":"policyrisk.com FIX company page（引用 FY2025 10-K）","url":"https://policyrisk.com/world/company/FIX","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"搜尋未找到最大客戶導入第二供應商或將機械施工自製（in-house）的報導；管理層稱與超大規模雲端業者及主要中介有直接關係，僅在客戶給出多年期承諾時才擴產。","source":"Nasdaq: Comfort Systems USA Q2 Earnings Call Highlights","url":"https://www.nasdaq.com/articles/comfort-systems-usa-q2-earnings-call-highlights","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261013","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K：最大單一客戶占 2025 合併營收 12.8%、占 2025/12/31 應收帳款 10.2%；信用風險主要來自總承包商、業主/開發商、商業與工業公司，公司對工程有留置權","source":"SEC EDGAR Comfort Systems USA Form 10-K FY2025 (concentration of credit risk note)，經搜尋摘要轉述，未讀全文","url":"https://www.sec.gov/Archives/edgar/data/1035983/000110465926017530/fix-20251231x10k.htm","excerpt":null,"as_of":"2026-02-26","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2024 10-K：最大單一客戶占 2024 營收 13.3%、占 2024/12/31 應收 17.7%；第三方摘要稱同一客戶 2023 年占 13.8%，皆在 mechanical 分部（次級來源，未對照原文）","source":"SEC EDGAR Comfort Systems USA Form 10-K FY2024 Financial_Report；policyrisk.com 摘要","url":"https://www.sec.gov/Archives/edgar/data/1035983/000155837025001222/Financial_Report.xlsx","excerpt":null,"as_of":"2025-02-27","retrieved_at":"20261013","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"科技（資料中心）相關工程占營收比重：Nasdaq/Zacks 文稱 40%（前一年 31%），另一第三方摘要稱 2025 年約 45%，兩數字口徑不一致","source":"Nasdaq/Zacks: Comfort Systems' Tech and Data Push: Growth or Concentration Risk?","url":"https://www.nasdaq.com/articles/comfort-systems-tech-and-data-push-growth-or-concentration-risk","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FIX backlog 2026-06-30 為 $14.06B，高於 3/31 的 $12.45B 與去年同期 $8.12B；管理層稱即使燃燒速度加快 backlog 仍上升","source":"Comfort Systems USA Q2 2026 earnings release (8-K ex99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001035983/000110465926086255/fix-20260723xex99d1.htm","excerpt":"Backlog as of June 30, 2026 was $14.06 billion as compared to $12.45 billion as of March 31, 2026 and $8.12 billion as of June 30, 2025.","as_of":"2026-07-23","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"管理層對 2026 剩餘期間及 2027 年表示樂觀；科技相關（資料中心）工作佔季營收過半。此為管理層自述預期，來源未給週期長度","source":"Comfort Systems USA Q2 2026 earnings call highlights (GuruFocus) / 8-K","url":"https://www.gurufocus.com/news/8978757","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261013","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"ABC 估計美國營建業 2026 需淨增約 349,000 名工人、2027 需 456,000 名，並歸因於高齡化、退休潮等結構性因素；技工缺口為產能限制","source":"ABC Carolinas / ABC workforce forecast (construction industry labor shortage data)","url":"https://abccarolinas.org/construction-industry-labor-shortage-data-drivers-and-strategic-responses/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261013","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"含資料中心工作的承包商 backlog 比其他承包商長約四個月；2026 年 4 月 backlog 增幅幾乎全來自有資料中心業務的大型承包商，其他規模公司 backlog 皆低於去年；非住宅民間營建支出已連續七個月下滑","source":"contractorplus.app Construction Backlog Indicator April 2026 / Wiss 2026 outlook","url":"https://contractorplus.app/blog/construction-backlog-indicator-april-2026","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261013","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Q1 2026 10-Q: 公司稱面臨一般營運中的法律與監管索賠（含訴訟），管理層認為個別與合計皆不會對經營結果、現金流或財務狀況造成重大影響。","source":"SEC Form 10-Q FY2026 (period 2026-03-31), Comfort Systems USA","url":"https://www.sec.gov/Archives/edgar/data/0001035983/000110465926047689/fix-20260331x10q.htm","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261013","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因子：約190個據點、27州，面臨州與地方規範（主要為承包商執照）；承做聯邦工程的子公司受稽核，違規可能導致罰款、合約終止或禁止承包。","source":"SEC Form 10-K FY2025, Comfort Systems USA","url":"https://www.sec.gov/Archives/edgar/data/1035983/000110465926017530/fix-20251231x10k.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Motley Fool 報導：FIX 在財報風險章節明確點出關稅風險（泛指關稅，非 Section 232 專指）；搜尋摘要另稱公司倚賴鋼、鋁、銅與進口零組件。","source":"Motley Fool, Why Comfort Systems USA Stock Slid 17% Last Month","url":"https://www.fool.com/investing/2025/03/07/why-comfort-systems-usa-stock-slid-17-last-month","excerpt":null,"as_of":"2025-03-07","retrieved_at":"20261013","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2025 年管理層表示大型專案成本多在早期鎖定、報價來自供應商固定報價；該輪關稅下供應商漲價在一般區間，未見專案延遲（來源為搜尋摘要轉述 Zacks，未讀原文）。","source":"Zacks 2025 results coverage (via search summary)","url":"https://www.zacks.com/stock/news/2432360/is-comfort-systems-stock-a-buy-after-a-20-ytd-dip","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261013","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"PwC（2026-02-26）：最高法院駁回 IEEPA 關稅後，政府改以其他授權宣布新全球關稅；E&C 產業核心問題是政策波動。摘要稱 2026 年 4 月時鋼鋁銅製品 50%、衍生品 25%、含此類金屬的工業電氣設備（變壓器、配電盤、導管系統）15%，全球基準 10% 至 2026 年 7 月；之後是否變動未確認。","source":"PwC, Building in uncertainty","url":"https://www.pwc.com/us/en/industries/industrial-products/engineering-construction/supreme-court-tariff-mitigate-volatility.html","excerpt":null,"as_of":"2026-02-26","retrieved_at":"20261013","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"CRS 報告（2026-08-18 更新）稱中國以關稅、出口管制部分生產投入、限制部分美企市場進入回應美國關稅；報告未點名 Comfort Systems。","source":"CRS, U.S.-China Tariff Actions Since 2018: An Overview","url":"https://www.legistorm.com/reports/view/crs/656134/U_S_China_Tariff_Actions_Since_2018_An_Overview.html","excerpt":null,"as_of":"2026-08-18","retrieved_at":"20261013","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險因素：公司、供應商與客戶自外國供應商進口部分原料、零組件與產品；貿易政策變動可能帶來關稅與貿易障礙。","source":"Comfort Systems USA Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1035983/000110465926017530/fix-20251231x10k.htm","excerpt":"We, our suppliers and our customers import certain raw materials, components and other products from foreign suppliers.","as_of":"2026-02-20","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K（FY2024）風險因素：若無法將關稅成本轉嫁客戶，經營結果可能受重大不利影響。","source":"Comfort Systems USA Form 10-K FY2024 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1035983/000155837025001222/fix-20241231x10k.htm","excerpt":"If we are unable to pass the costs of such tariffs on to our customer base or otherwise mitigate such costs, or if demand for our services decreases due to the higher cost, our results of operations could be materially adversely affected.","as_of":"2025-02-20","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"公司依賴第三方分包商與設備／材料供應商；供應商未如期履約會損及執行與獲利（一般性依賴，未點名單一供應商或地區）。","source":"Comfort Systems USA Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1035983/000110465926017530/fix-20251231x10k.htm","excerpt":"We hire third-party subcontractors to perform work and depend on third-party suppliers to provide equipment and materials necessary to complete our projects.","as_of":"2026-02-20","retrieved_at":"20261013","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"風險摘要稱商用 HVAC 設備、配電開關設備、大型發電機交期最長，常超過六個月（第三方彙整 SEC 揭露，非 10-K 原頁讀取）。","source":"policyrisk.com FIX company risk summary","url":"https://policyrisk.com/world/company/FIX","excerpt":"Orders for manufactured commercial HVAC equipment, electrical switch gear, and large application power generators have experienced the longest lead-times, and it is not uncommon for lead-times to be greater than six months.","as_of":"2026-02-20","retrieved_at":"20261013","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"2026年5月法說會：管理層稱設備端供應鏈與關稅風險已透過合約緩解（二手法說摘要）。搜尋結果未發現公司將中國／台灣列為供應鏈曝險。","source":"Comfort Systems (FIX) Earnings Call Transcript (AOL)","url":"https://www.aol.com/articles/comfort-systems-fix-earnings-call-172731925.html","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261013","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年Q2 backlog 為 $14.06B（Q1 $12.45B、去年同期 $8.12B）；同店 backlog $13.70B；同店營收成長 44%","source":"Comfort Systems USA Reports Second Quarter 2026 Results (BusinessWire)","url":"https://secure.businesswire.com/news/home/20260723227439/en/Comfort-Systems-USA-Reports-Second-Quarter-2026-Results","excerpt":"Backlog as of June 30, 2026 was $14.06 billion as compared to $12.45 billion as of March 31, 2026 and $8.12 billion as of June 30, 2025.","as_of":"2026-07-23","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Technology（資料中心）佔上半年營收 58%，去年同期 40%；管理層稱專案管線處歷史高檔、未見資料中心需求放緩；全年同店營收成長指引中高 30% 區間","source":"Comfort Systems USA Q2 Earnings Call Highlights (Nasdaq)","url":"https://www.nasdaq.com/articles/comfort-systems-usa-q2-earnings-call-highlights","excerpt":"Technology generated 58% of first-half revenues, up from 40% in the prior-year period.","as_of":"2026-07-24","retrieved_at":"20261013","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"分部營收（2025前九個月）：機械 +19.0% 至 $4.85B，電氣 +47.9% 至 $1.60B；2026年分部數字聚合站互相矛盾，未採信","source":"Nasdaq: Can Mechanical & Electrical Strength Support Comfort Systems in 2026?","url":"https://www.nasdaq.com/articles/can-mechanical-electrical-strength-support-comfort-systems-2026","excerpt":"Revenues for the mechanical segment increased 19.0% to $4.85 billion. Revenues for the electrical segment rose 47.9% to $1.60 billion.","as_of":"2026-01-01","retrieved_at":"20261013","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#none","axis":"substitute_technology","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q1 2026（4月）管理層維持 2026 年同店營收成長中至高 20% 區間的 guidance，backlog $12.5B。","source":"Seeking Alpha: Comfort Systems forecasts mid- to high 20% 2026 same-store revenue growth as backlog reaches $12.5B","url":"https://seekingalpha.com/news/4579638-comfort-systems-forecasts-mid-to-high-20-percent-2026-same-store-revenue-growth-as-backlog","excerpt":"Comfort Systems forecasts mid- to high 20% 2026 same-store revenue growth as backlog reaches $12.5B","as_of":"2026-04-23","retrieved_at":"20261013","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 後，第三方摘要（Quartr）稱全年同店成長預期上調至中至高 30%；Q2 營收 $3.27B（去年同期 $2.17B），2026-06-30 backlog $14.06B。公司原文 guidance 措辭未直接讀到，須對照財報稿/逐字稿。","source":"Quartr: Comfort Systems USA (FIX) Q2 2026 earnings summary；Barchart: Comfort Systems USA reports second quarter 2026 results","url":"https://quartr.com/events/comfort-systems-usa-inc-fix-q2-2026_3gzVJMWX","excerpt":"Full-year same-store revenue growth expected in the mid- to high-30% range, with backlog and project pipelines at historic highs.","as_of":"2026-07-24","retrieved_at":"20261013","affects":["valuation","thesis.H","triggers"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 非GAAP EPS $12.53 對共識約 $10.41–10.45、營收 $3.27B 對 $2.97B；過去四季皆優於共識。","source":"Benzinga FIX earnings 頁／fn2.ai FIX 2026 Q1 頁（聚合）","url":"https://www.benzinga.com/quote/fix/earnings","excerpt":null,"as_of":"2026-10-09","retrieved_at":"20261013","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"前瞻共識（Benzinga，10/9 頁面）：Q3'26E EPS $12.73、Q4'26E EPS $13.04、Q3 營收 $3.38B；較早快照（Q3 $11.58、Q4 $12.17）明顯上移。","source":"Benzinga FIX earnings","url":"https://www.benzinga.com/quote/fix/earnings","excerpt":null,"as_of":"2026-10-09","retrieved_at":"20261013","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Zacks：過去30天 2026 EPS 共識由 $43.08 升至 $45.48，2027 由 $52.59 升至 $57.27，無下修；營收共識 2026 +38.3%、2027 +18.4%；平均券商評等 1.33。文章發布日未顯示。","source":"Zacks via TradingView: Is Comfort Systems Stock a Buy After Wall Street Raises Estimates","url":"https://www.tradingview.com/news/zacks:811b867d4094b:0-is-comfort-systems-stock-a-buy-after-wall-street-raises-estimates/","excerpt":null,"as_of":"2026-09-11","retrieved_at":"20261013","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"目標價分布（Benzinga 約 2026-09-11）：8 位分析師、平均 $1,974、Buy 共識；最新動作 DA Davidson 8/21 初評 Buy $2,100；UBS 7/27 升至 $2,225（前 $2,125）；Stifel $1,910（7/27）；Goldman 7/9 初評 Buy $2,159；Oppenheimer $2,200（5/28）。目標價 vs 現價一律引 numbers.price_at_dd。","source":"Benzinga FIX price targets","url":"https://kr.benzinga.com/quote/FIX/price-targets","excerpt":null,"as_of":"2026-09-11","retrieved_at":"20261013","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#6","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"其他來源目標價離散：StockAnalysis 9 位平均 $2,064；Barchart（8月中）13 位平均 $2,114.30、最高 $2,400；11 Strong Buy、2 Hold。各來源 as_of 與樣本數不同。","source":"StockAnalysis FIX；Barchart/Yahoo: Do Wall Street analysts like Comfort Systems stock","url":"https://stockanalysis.com/stocks/FIX/","excerpt":null,"as_of":"2026-08-15","retrieved_at":"20261013","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2025 年 10 月 1 日收購 Feyen Zylstra Holdings 與 Meisner Electric（密西根、佛州電氣），合計預期年營收 2.0–2.4 億美元、年 EBITDA 1.5–2.0 千萬美元；全為 bolt-on，搜尋未見大型合併。","source":"Nasdaq/Zacks: Could Comfort Systems' Acquisitions Fuel a Multi-Year Rally?","url":"https://www.nasdaq.com/articles/could-comfort-systems-acquisitions-fuel-multi-year-rally","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"Q2 2026 財報摘要列出 Hunt Electric，貢獻年化營收約 2.5 億美元（交易日期與價格未揭露）。","source":"GuruFocus: FIX Q2 2026 Earnings Call Highlights","url":"https://www.gurufocus.com/news/8978757","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2025 年 10 月 1 日收購 Feyen Zylstra Holdings 與 Meisner Electric，合計預期年營收 2.0–2.4 億美元、年 EBITDA 1.5–2.0 千萬美元。","source":"Nasdaq/Zacks: Could Comfort Systems' Acquisitions Fuel a Multi-Year Rally?","url":"https://www.nasdaq.com/articles/could-comfort-systems-acquisitions-fuel-multi-year-rally","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"+","claim":"Q2 2026 財報摘要列出 Hunt Electric，年化營收約 2.5 億美元。","source":"GuruFocus: FIX Q2 2026 Earnings Call Highlights","url":"https://www.gurufocus.com/news/8978757","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261013","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 1 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"FIX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.66,"operating_margin_pct":16.45,"fcf_margin_pct":19.24,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FIX","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"EME","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.43,"operating_margin_pct":9.6,"fcf_margin_pct":6.3,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EME","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"IESC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":26.31,"operating_margin_pct":12.38,"fcf_margin_pct":5.73,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IESC","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PWR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.46,"operating_margin_pct":6.12,"fcf_margin_pct":7.27,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PWR","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"FIX"},"financial_history":{"ticker":"FIX","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":4140364000.0,"revenue_yoy_pct":null,"gross_margin_pct":17.91,"operating_margin_pct":6.09,"net_income":245947000.0,"diluted_eps":6.82,"free_cash_flow":253172000.0,"fcf_margin_pct":6.11,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":5206760000.0,"revenue_yoy_pct":25.76,"gross_margin_pct":19.02,"operating_margin_pct":7.99,"net_income":323398000.0,"diluted_eps":9.01,"free_cash_flow":544730000.0,"fcf_margin_pct":10.46,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":7027476000.0,"revenue_yoy_pct":34.97,"gross_margin_pct":21.01,"operating_margin_pct":10.62,"net_income":522433000.0,"diluted_eps":14.6,"free_cash_flow":737986000.0,"fcf_margin_pct":10.5,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":9101641000.0,"revenue_yoy_pct":29.52,"gross_margin_pct":24.13,"operating_margin_pct":14.42,"net_income":1022558000.0,"diluted_eps":28.88,"free_cash_flow":1031453000.0,"fcf_margin_pct":11.33,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/FIX/FIX_Q2_2026_Earnings_Call_20260724.md）

# Q2 2026 Earnings Call
2026-07-24

Q2 2026 Earnings Call
Comfort Systems USA, Inc. | Earnings Calls | 2026-07-24
Operator (Operator)
Thank you for standing by, and welcome to the Comfort Systems USA's Second Quarter 2026 Earnings
Conference Call. [Operator Instructions] As a reminder, today's program is being recorded. And now I'd
like to introduce your host for today's program, Julie Shaeff, Chief Accounting Officer. Please go ahead.
Julie Shaeff (Executives)
Thanks, Jonathan. Good morning. Welcome to Comfort Systems USA's Second Quarter 2026 Earnings
Call. Our comments today as well as our press releases contain forward-looking statements within the
meaning of the applicable securities laws and regulations. What we will say today is based upon the
current plans and expectations of Comfort Systems USA. Those plans and expectations include risks
and uncertainties that might cause actual future activities and results of operations to be materially
different from those set forth in our comments.
You can read a detailed listing and commentary concerning our specific risk factors in our most recent
Form 10-K and Form 10-Q as well as in our press release covering these earnings. A slide presentation
is provided as a companion to our remarks and is posted on the Investor Relations section of the
company's website on the comfortsystemsusa.com. Joining me on the call today are Brian Lane, Chief
Executive Officer; Trent McKenna, President; and Bill George, Chief Financial Officer. Brian will open
our remarks.
Brian Lane (Executives)
Okay. Thanks, Julie. Good morning, and thank you for joining us on the call today. We had a fantastic
quarter with amazing execution by our teams. This is the first time that our quarterly revenue has
exceeded $3 billion. We earned $12.53 per share this quarter, which is an increase of 92% compared to
a year ago. Our Mechanical business experienced a sharp increase in profitability, and our Electrical
segment also performed exceptionally well. Bookings continued to trend upwards, and our backlog
increased to a new high of $14.1 billion.
Demand remains strong, especially in Technology as we continue to book work with good margins and
favorable working conditions for our valuable people, and we enter the second half of 2026 with
increased sequential and year-over-year backlog. I want to welcome our newest acquisition, Hunt
Electric, a transaction we mentioned last quarter and that closed on May 1. Hunt is a great electrical
business based in Utah, and we expect Hunt will contribute about $250 million of annualized revenue.
We also increased our quarterly dividend by $0.10 to $0.90 per share.
Thanks to our amazing people, we expect strong results for the rest of 2026 and continuing success into
2027. Trent will discuss our operations and outlook in a few minutes, and I will make a few closing
comments after our Q&A. But first, I will turn the call over to Bill to review our financial performance.
Bill?
William George (Executives)

Thanks, Brian. Our results were once again extraordinary with 44% same-store revenue growth,
approximately $1 billion in free cash flow, and EBITDA that was higher than last year by 80%. Revenue
for the second quarter of 2026 was $3.3 billion, an increase of $1.1 billion compared to last year.
Electrical segment revenue grew by 81%, while Mechanical segment revenue increased by 40%.
Through 6 months, same-store revenue has grown 47%, and we estimate that 2026 same-store revenue
growth will likely finish with a full year increase that is in the mid- to high 30% range. Gross profit was
$844 million for the second quarter of 2026, $334 million higher than a year ago.
Our gross profit percentage grew to a noteworthy 25.9% this quarter compared to 23.5% for the second
quarter of 2025. Gross profit percentage ticked down by a small amount from our first quarter as it was
reported. However, absent the unique gains that we identified and quantified last quarter, our second
quarter gross profit percentage actually increased from 25.2% in the first quarter to 25.9% this quarter.
Quarterly gross profit percentage in our Mechanical segment jumped to 25.6% this year compared to
22.9% last year. Margins in our Electrical segment also increased by a full percentage point to 26.4%
compared to 25.3% in the second quarter of 2025.
We believe that gross profit margins are likely to continue in the strong ranges that we have averaged in
recent quarters. SG&A expense for the quarter was $287 million compared to $210 million in the
second quarter last year as we continue to invest in people and innovation to support our growing
business. SG&A as a percentage of revenue declined from 9.7% of revenue last year to 8.8% this
quarter. Our operating income increased by 86% from last year, from $300 million in the second
quarter of 2025 to $558 million for the second quarter of 2026. With our strong gross profit margins,
combined with our SG&A leverage, our operating income percentage surged to 17.1% this quarter from
13.8% in the prior year.
Our year-to-date effective tax rate was 22.5% and benefited from a discrete tax item in the second
quarter. We expect our full year effective tax rate to be around 23%. After considering all these factors,
net income for the second quarter of 2026 was $442 million or $12.53 per share, and that compares to
net income for the second quarter of 2025 of $231 million or $6.53 per share. So we are more than 90%
higher than the already elevated numbers we achieved a year ago. EBITDA increased to $600 million
this quarter from $334 million in the second quarter of 2025. This 80% increase reflects great
execution by our workforce and strong demand in our markets.
At the end of the second quarter, our trailing 12-month EBITDA is approximately $2 billion. Free cash
flow for the second quarter of 2026 was $999 million. We are continuing to fund expansion of our
production facilities and expect to incur additional capital expenditures through the remainder of 2026.
We estimate that full year CapEx expenditures will be approximately 5% of our revenue. Despite
funding an acquisition and big capital investments, we are in a net cash position of over $1.8 billion.
And with strong ongoing cash prospects, we are better positioned than ever to reward our shareholders
and invest in growing and adding to our business. That's what I got. Trent?
Trent McKenna (Executives)
Thanks, Bill. I'm going to discuss our operations and our outlook. Our backlog at the end of the second
quarter was a record $14.1 billion, a large sequential and year-over-year increase. Since this time last
year, our backlog has increased by $5.9 billion or 73%, and $5.6 billion of the increase was same-store.
On a sequential basis, backlog increased by $1.6 billion or 13%, of which $1.4 billion was same-store.

Second quarter bookings were especially strong in the technology sector, both in our construction
business as well as modular offerings.
We entered the third quarter with same-store backlog 69% higher than at this time last year, and our
project pipelines continue at historically high levels. Industrial customers accounted for 75% of total
revenue in the first half of 2026, and they continue to be major drivers of pipeline and backlog.
Technology, which is included in industrial, was 58% of our revenue, a substantial increase from 40%
in the prior year. Our modular operations continue to grow and thrive, and we are making progress on
expanding our customer base, including with frontier labs and colocation providers. Institutional
markets, which include education, health care, and government, remain strong and represent 17% of
our revenue. The commercial sector, now a smaller part of our business, provided 8% of our revenue.
Construction accounted for 90% of our revenue with projects for new buildings representing 75% and
existing building construction 15%. We include modular in new building construction and year-to-date,
modular was 17% of our revenue. We now have over 3.5 million square feet of building capacity
dedicated to our modular business, and we are on track to have more than 4 million square feet in
production by year-end. With ongoing orders and investments we are making to address that demand,
we expect to have approximately 5 million square feet of capacity by late summer 2027.
Service revenue was up 7% this year, and it represents 10% of our total revenue. Our service remains
very profitable and our investments to meet the future demand that will result from the current strong
construction activity remains a key element of our overall strategy. As mentioned before, we are
entering the second half of 2026 with a backlog that is 69% higher on a same-store basis than we had at
this time last year, and we have a superb team working hard for our customers every single day. Thanks
to the dedication and hard work of our employees across the country, we are optimistic about our
future. I want to close by joining Brian and Bill in thanking our over 25,000 employees for their hard
work and dedication.
And with that, I will now turn it back over to Jonathan for questions. Thank you.
Operator (Operator)
And our first question for today comes from the line of Adam Thalhimer from Thompson, Davis.
Adam Thalhimer (Analysts)
Congrats on another amazing quarter. Bill, maybe you can help us understand the puts and takes to
cash flow, how we should be looking at $1 billion of free cash flow in a single quarter and what that tells
us about your cash flow prospects?
William George (Executives)
Yes. That is a really extraordinary number, like 2.5x our earnings, right? And over time, our cash flow
will match our net income, plus a little because we do have some noncash expenses. The interesting
thing about this, there is definitely an element of advanced cash. People who know us will recall a year
or 2 ago, we received a lot of orders, and we were able to build a percentage of those orders far ahead of
when we would actually incur the cost to do the work. So we have begun to build a position of advanced
cash as well.
We also have extraordinarily good payment terms because we have extraordinarily good negotiating
power on our work overall. And then, of course, our jobs are doing very well and customers are happy

to pay when they see that the work is getting done on time and well. So it was broad-based, it wasn't
any one thing. It is certainly a good sign that our business is healthy and that our customers are happy.
But there's no like -- other than some advanced cash, there's no unique item to point out.
Adam Thalhimer (Analysts)
And then I guess the flip side of that is how do you think about capital deployment from here?
William George (Executives)
We've told you that we would spend about 5% of our increasing revenues on -- essentially, it boils down
to buildings, where we're buying them instead of leasing them because we're putting so much capital
into these buildings in the form of robots and custom paint booths and turntables and various kinds of
cutters. And then we also continue to keep a sharp eye out for opportunities to buy stock. We like our
stock better than we've ever liked it. We bought some year-to-date, but after the big purchases of last
year, we've been a little slower at the first part of the year. And of course, a patient commitment to
acquisitions is still a part of our capital allocation conviction.
Adam Thalhimer (Analysts)
Okay. Lastly, Trent, I think you made a comment on -- I think this was a modular comment, making
progress on expanding the customer base. What did you mean by that? And then I'll turn it over.
Trent McKenna (Executives)
Yes. We've been having some success with some pilot contracts, just small contracts with both frontier
labs and also with colocation providers. And the hope is that those will lead to future programs.
Operator (Operator)
And our next question comes from the line of Adam Bubes from Goldman Sachs.
Adam Bubes (Analysts)
I think you talked about potential for 5 million square foot of modular capacity at around this time next
year. How should we think about incremental CapEx associated with 1 million incremental square foot
of capacity? And is that tied to an existing customer or the new customers -- potential customers you
were referencing? And lastly, just how are you thinking about the range of outcomes for modular
capacity expansion in 2027? Could it ultimately move higher than that 5 million number?
William George (Executives)
I'll respond to the first part of that and probably Trent is a better person to respond to the second part
of that. The 5% of revenue that we talk about is our guidance on that, and we're comfortable that that's
about the right amount of money. I will say when we make new investments, we -- every time -- and
these are big buildings, right? They -- they're -- we bought one recently for $100 million. We really take
a hard look at the pros and cons of leasing or ownership. We've been tending towards ownership lately
in order to control our destiny and just liking the product that we're getting involved with. But there is
some wiggle room around that because we don't know what decisions we're making as time passes.
We'll try to make what's best for the business.

Trent McKenna (Executives)
Yes. And as far as out into the future, one thing -- we're not going to invest in buildings just on
speculation. We expand when customers provide us meaningful multiyear commitments. And so that
would justify anything, but we'll be prudent about that going forward as we've always done.
Brian Lane (Executives)
But we do love this industry. We're bullish long term about what the opportunities are in the industry
we're in.
Adam Bubes (Analysts)
Great. And then I think your 10-Q shows changes in estimates on projects positively impacted Q2
revenues by around 7.7%. I think that's close to double the impact a year ago. Two-part question.
What's driving that level of favorable revisions? Is it change orders or conservative initial estimating?
And how should we just think about the underlying margin rate given that could be reflective of in-
process work running through the portfolio at conservative margins?
William George (Executives)
So just as sort of historical context, since I became CFO in 2005 and frankly, before that, we have had
net gain in our jobs every single year ever. We have more -- and by the way, you would expect the
construction company to have that because when you're -- as you progress in these jobs, you don't know
what's going to happen when you turn the systems on. You don't know how much it's going to rain.
People who are not accruing for or considering the risks of what they're doing as they go don't last long
in this industry. They're bigger this quarter than usual. They're bigger. They've been just trending
bigger because of things like you mentioned, like excellent pricing that we're getting. And in some ways,
the risk is bigger, right?
The number of jobs we have over $40 million or $100 million counsels us to not rush to recognize
revenue on things that aren't finished too aggressively. I will also mention that in the first quarter, we
called out some incremental gains that were out of the ordinary. One resulted from a big change order
where we had a bunch of profit with no cost whatsoever. And so we identified $43 million of gains that
were kind of even outside the scope of the ordinary gains that we've had every year since 2005. That's
what -- that's the point I was making about sort of if you want to look at our margin progression over
time, you would not be getting a good picture of it if you left that out. So does that answer your
question?
Adam Bubes (Analysts)
Yes, that's helpful. I appreciate all the color.
Brian Lane (Executives)
If I could just add on one thing. When you look at an estimate and how well we do in the field, we're
really fortunate to have elite trades people that are doing this work who get out in the field and really
want to perform at a high level. So we're just very fortunate in this company to have the group of people
we have building these buildings.
William George (Executives)

There's some amazing execution.
Brian Lane (Executives)
Yes. For sure.
Operator (Operator)
And our next question comes from the line of Sangita Jain from KeyBanc.
Sangita Jain (Analysts)
Bill and Brian and Trent, can I ask if you guys are evaluating your projects any differently or with
greater scrutiny given the environment out there with the public sentiment turning against data centers
and the NIMBY issues that are coming up?
Brian Lane (Executives)
I'll take the execution part of that, and Bill probably can take the other part of it. We always spend a lot
of time scrutinizing the work at the operating level and here on the larger work. So that really hasn't
changed philosophically how we look at estimates and review the jobs. But on the front end...
William George (Executives)
Because we sell directly to the hyperscalers and to the most important intermediaries, we have really
good -- a really good view on what they're thinking, what they're planning. And there is a very deep and
calm certainty among these people that they're going to continue to build, that they absolutely need and
have to do this building. And our goal -- so we see no letdown whatsoever. And our goal is just to really
be a great partner for them in helping them achieve delivered compute. So the answer is absolutely no
sign of a letdown.
Sangita Jain (Analysts)
Got it. And then on the proposed expansion to 5 million square feet by next summer, I'm sorry if I
missed this, but is that still for your current major customers? Or are you branching some capacity out
into other industries or maybe reserving some for potential large customers coming up?
Trent McKenna (Executives)
For current customers.
Sangita Jain (Analysts)
Okay. So even that expansion from 4 to 5 is still for the existing customers, you're saying?
Trent McKenna (Executives)
Yes.
Operator (Operator)
And our next question comes from the line of Julio Romero from Sidoti & Company.
Julio Romero (Analysts)

Your full year same-store sales guidance of mid- to high 30s for the year implies second half, I think,
about high 20s range or even in the low 30s. How should we think about -- I'm really curious like kind
of the exit rate embedded in that. In other words, is the high 20s range as a run rate a reasonable
jumping off point for how to look at '27?
William George (Executives)
So it's really -- it's our best estimate. When we give this guidance and understanding we've been wrong
in the conservative direction quite a bit, we don't just make it up, right? We have people in the field who
are -- have sort of workforce loading.
Trent McKenna (Executives)
We build it from the bottom up, Julio.
William George (Executives)
And I will say also, this really -- it's an extraordinary level of growth. So we do have, in particular, in the
fourth quarter, but some really, really heavy comparables coming up. So we will show a lot of growth.
We'll continue to show a lot of growth. But it's -- this level of growth against the comparables for the
next 2 quarters and particularly in the fourth quarter is a whole different, like, proposition than what
you just saw.
Julio Romero (Analysts)
Got it. That's very helpful. And then I wanted to ask you about -- if you could speak a little about how
the first couple of months of R.C. Hunt have progressed. Can you maybe speak to the strategic fit with
the current mechanical subsidiaries you have out in Utah and how meaningful it is to go to market with
that mechanical electrical pairing and if they're pursuing work jointly?
Trent McKenna (Executives)
Yes. Hunt is exactly the kind of company that we want to be successful in joining Comfort Systems, and
they have been fantastic in early stages with the integration. They're already working on some pursuits
with our mechanical contractors in that market. That's a great market. We know it really well, and they
are the premier electrical provider in that market. So we're really excited to have them on board.
Operator (Operator)
And our next question comes from the line of Josh Chan from UBS.
Joshua Chan (Analysts)
Brian, Trent, Bill, Julie, congrats on a great quarter. I was wondering about the increase in the backlog.
I think you called out modular contributing a portion of the increase to backlog, but curious how much
of the backlog increase was modular this quarter? And is it unusual to have a larger modular order in
Q2 compared to the historical pattern? Just wanted some color around that.
William George (Executives)
So of that increase, Modular had bookings of $510 million. It's in the MD&A ahead of what they
burned. So they booked enough to cover their incredible burn rate and net an additional $500 million. I

would say nothing is unusual right now or actually, I think what I would say is everything is unusual
right now. It's an amazing time. But I don't -- there wasn't some like really special unexpected thing
that happened. It's just that -- it's the reason we're adding the square footage. There's just a very, very
consistent demand from our customers to buy as much of this as we can produce.
Joshua Chan (Analysts)
Okay. Yes. That makes a lot of sense. And then on the backlog itself, could you just talk about the
duration of the backlog? Are you stretching out the order book? How are you managing the dynamic of
the duration as you may be booking a little further out or maybe not?
William George (Executives)
Yes. I'll start with that. It's a tale of two cities, except with the difference it's the best of times and the
best of times. But on the modular side, we are getting farther and farther booked out. On the
construction side, bigger projects take longer, but some of these bigger projects move pretty fast. So I
would say we still have our sort of -- most of it burns on the construction side in the next 18 to 24
months.
Brian Lane (Executives)
But Josh, just to make sure this is clear, we only take work that we know we can perform. We do a lot of
time labor planning, looking at the extent of jobs, when the men are available. So we don't outkick our
coverage. We're very prudent and disciplined on what work we take and what it is.
Joshua Chan (Analysts)
Great. Yes. Congrats on the quarter again and good luck in the second half.
Operator (Operator)
And our next question comes from the line of Brian Brophy from Stifel.
Brian Brophy (Analysts)
Very nice quarter again. Curious, obviously, the CapEx number is quite large. You guys reiterated that.
How are you thinking about returns on that CapEx spending this year relative to your internal hurdles?
William George (Executives)
So this would meet any reasonable person's internal hurdle. What we've been experiencing in that
world is full paybacks within a year or 2. I mean it's unbelievable. So we don't -- we're not -- we're really
not a company that stares at spreadsheets a lot or sits around conference rooms a lot. But if you were
to, it's -- think about -- look at how much CapEx we've spent and then look at how much earnings we've
incrementally added for -- you can probably do a one-to-one analysis on the modular part of our
business. You have the information to do this to say, okay, how much are they spending and how much
is that business providing to them? And it's extraordinary. I mean the returns are embarrassing.
Brian Brophy (Analysts)
That's great to hear. And then there was some discussion on the advanced cash earlier. Curious to what
extent this is related to the stick-built side of the business versus the modular side?

William George (Executives)
It's all of the above. To get a number like that, everything has to be optimized in that direction for that
particular metric. But if you force me to guess, I would say it's something like 1/3, 1/3, 1/3 or so I'd say
1/3 of it might be the advanced cash that we've gotten in the past and the rest of it is -- it's really good
performance, but it's within the range of -- if you were to like do a lag 12-month -- trailing 12-month
comparison of net income to cash, we're ahead, but we've been ahead for years. And I'd say it's not
really outside sort of 1.5 standard deviations of what might have happened, setting aside the advanced
cash.
Trent McKenna (Executives)
And one of the things about the advanced cash is I think it reflects the strength of our counterparties
and also how much they value locking up our capacity right now. So it's a real good indicator from an
operations perspective.
Brian Brophy (Analysts)
That's great. And just kind of one follow-up on to that. To what extent have you guys seen any
competitive changes from a landscape perspective on the modular side recently?
William George (Executives)
There are a handful of other companies building, in most cases, the product that we codesigned with
our customers. We don't really -- I'd say some of them are so new at it that I don't think we have
feedback. But I can say this, which is our customers are not inducing other people to build this to
replace us. They're inducing other people to build this because they want more than we'll build. And
we've never really thought we'd be the only company in the world doing complex modular. We just
want to be the best and keep a lead -- keep our -- earn a lead in that.
Operator (Operator)
And our next question comes from the line of Jean Veliz from Oppenheimer.
Jean Veliz (Analysts)
Congrats on the quarter, team. Looking at the balance sheet, what was associated with the large change
in billings in excess this quarter? Was that associated with a single customer in modular or a collection
of other customers?
William George (Executives)
I'd say it's all of the factors that contributed to our cash flow. And it's emblematic of our -- really, it's
emblematic of the leverage -- I don't want to use the word leverage, of the credibility that we have with
our customers and their willingness to be a great partner for us so that we can keep working together.
Jean Veliz (Analysts)
A lot of questions have been asked about modular capacity. But just for more clarity, just roughly
speaking, what percentage of the new capacity is allocated for the legacy customers, new recent
customers and some -- and the potential leads based on the conversations you guys are having with all
the above?

William George (Executives)
I agree with Trent. I mean the capacity we're talking to you about today is overwhelmingly for existing
customers and existing orders. So if we were to begin to have serious programmatic revenue from the
new customers that we're doing pilot orders with, we would have to add space to build that. And we're
getting more and more confident in our ability in a measured way to add space and successfully.
Jean Veliz (Analysts)
And one last for me. Could you provide us an update on the service opportunities in data centers?
Trent McKenna (Executives)
Yes. So I mean, right now, we're very focused on what every project we build today, right, in the data
center world really becomes tomorrow's service opportunity. And we're building this enormous
installed base of these data centers across the country. And when you look at what it takes to properly
maintain those, there's significant technical depth and the service technicians required for it. We feel
like we're very well positioned for that, and that will develop over time. Some of that gets caught up into
warranty periods and things like that with the OEMs. So it's not an immediate opportunity, but it's
definitely a long-term opportunity for us to continue to grow our service business.
Jean Veliz (Analysts)
Are you guys having conversations about any pilot programs for the future? Or is this just based on
what you're seeing right now?
Trent McKenna (Executives)
Yes. We haven't -- we've established ourselves as a provider to one of the hyperscalers. So that provides
us an inroad to some of the data centers that they have. And we're focusing on geographies where it
makes sense for us. Some of this is -- at the end of the day, this is being able to deliver service
technicians to the location in ways that make us successful. We're not going to take something that we
can't perform. So we're being very judicious in how we approach it, but yes, we're seeing inroads.
Operator (Operator)
And our next question comes from the line of Tim Mulrooney from William Blair.
Timothy Mulrooney (Analysts)
It's going to shock you, but I have a question about your modular business. So you're adding square
feet, you're going from 4 million to 5 million now, I think it is the most recent update. Like, are you
adding projects to your backlog for that capacity today, even though that capacity isn't built out yet? Or
do you wait until the expansion is closer to finished? And then -- so that's my first question is like how
do we think about that in terms of flowing through the backlog? And then what kind of terms, I don't
know, volume guarantees or otherwise, are you getting to derisk the investments that you have to make
in these expansions?
Trent McKenna (Executives)
Yes. So some of that was in this quarter. And Bill already mentioned the over $500 million of modular
backlog that was added in the quarter, incrementally. So that's already in there to some extent. Some of

it will be coming though in future orders as well. And then as far as derisking on that stuff, I mean,
that's all about making sure that we have the volume commitments with the customer. And with the 2
hyperscalers that we work with, they have been willing to continue to provide us volume commitments.
That's why we continue to expand.
Timothy Mulrooney (Analysts)
Okay. That's really helpful. So even today, a part of the expansion from 4 to 5, you're booking some of
that today and you are getting volume commitments. That's really helpful. My other question, it's still --
it's data center related. But I mean, we saw the -- okay, we saw the news about the moratoriums on data
centers in New York. So I guess I'm curious if you have any planned projects there that might get
impacted. But also, could you just talk more about this broader idea of state moratoriums, where those
are cropping up and how that compares to the more business-friendly places where you operate in your
footprint?
Trent McKenna (Executives)
I mean a lot of what we currently have in our backlog, right, was already planned, permitted through
late cycle, right? And then with regard to moratoriums and kind of what you're hearing with certain
data centers really receiving heavy press coverage as to like we don't want them here, there. Our
position on that is these data centers as many as can be built are going to get built. There might be
reasons to move them, et cetera. With regard to our modular build-out, that doesn't impact it quite as
much because that's more of a programmatic towards certain locations that they're trying to hit.
And then with regard to the stick-built part of our business, I think these -- I'm betting on these guys to
be able to build the data centers over time. And so I think that you'll hear a lot. There's going to be some
press coverage. There's going to be this, that, and the other. And certainly, during election periods,
you're going to hear people say certain things. But I think at the end of the day, these things need to get
built. So people will figure out a place to put them and a way to get them built.
Brian Lane (Executives)
And get the power to do it.
Timothy Mulrooney (Analysts)
And get the power to do it. Got it. Okay. Congrats on a nice quarter.
Operator (Operator)
This does conclude the question-and-answer session of today's program. I'd like to hand the program
back to Brian Lane for any further remarks.
Brian Lane (Executives)
All right. In closing, I want to reiterate my gratitude for the amazing dedication and excellence of the
teams we have across our nation, serving our customers every day. Demand is strong, and our people
are rising to the challenge of addressing the unprecedented need for their unique skills. As Trent
mentioned, we feel that conditions are good for us to continue to perform. And as Bill indicated, we
have the resources and the commitment to lean into delivering for our employees, our customers, and

you, our shareholders. Thank you for your confidence, and have a great rest of your summer. Thank
you.
Operator (Operator)
Thank you, ladies and gentlemen, for your participation in today's conference. This does conclude the
program. You may now disconnect. Good day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FIX_Q1_2026_Earnings_Call_20260424.md
- 2026-04-24｜William George, CFO｜guidance：Management guided full-year 2026 same-store revenue growth to a mid-to-high 20% percentage range.（原話："in the mid to high 20% range."）
- 2026-04-24｜William George, CFO｜guidance：CFO guided full-year effective tax rate to approximately 23%.（原話："our full year effective tax rate to be around 23%."）
- 2026-04-24｜William George, CFO｜margin：CFO stated Q1 2026 gross profit percentage rose to 26.3% versus prior year.（原話："gross profit percentage grew to 26.3% this quarter"）
- 2026-04-24｜William George, CFO｜margin：CFO said gross profit margins are expected to continue at recent averaged levels.（原話："We currently expect that gross profit margins will"）
- 2026-04-24｜William George, CFO｜margin：CFO reported SG&A fell to 9.4% of revenue in Q1 2026 versus prior year.（原話："SG&A as a percentage of revenue was 9.4% this quarter"）
- 2026-04-24｜Brian Lane, CEO｜competition：CEO cited the company's traveling workforce as an advantage for serving data centers across dispersed geographies.（原話："we have a significant traveling workforce."）
- 2026-04-24｜Brian Lane, CEO｜capital_allocation：CEO announced a quarterly dividend increase to $0.80 per share.（原話："another increase to our quarterly dividend to $0.80"）
- 2026-04-24｜William George, CFO｜capital_allocation：CFO guided full-year CapEx to about 5% of revenue.（原話："CapEx will be in the range of 5% of revenue."）
- 2026-04-24｜William George, CFO｜capital_allocation：CFO described the pending electrical contractor acquisition as expected to carry EBITDA margins of 8-10%.（原話："EBITDA margins in the 8% to 10% range."）
- 2026-04-24｜Trent McKenna, President & COO｜product：COO said the company is on track to reach 4 million square feet of modular capacity by year-end.（原話："We are on track to have 4 million square feet"）
- 2026-04-24｜Samuel Kusswurm, Analyst (William Blair)｜risk：Analyst raised the risk of state-level data center bans or power access restrictions in regions the company serves.（原話："data center bans or even limiting access to power."）
- 2026-04-24｜William George, CFO｜risk：CFO identified labor availability as the persistent constraint on the company's growth.（原話："it's always and forever for us, it's labor."）
- 2026-04-24｜William George, CFO｜customer：CFO said the company now has stronger ability to select which counterparties/customers it works with.（原話："we have a much stronger ability to pick our counterparties"）
- 2026-04-24｜William George, CFO｜commitment：CFO said the company requires customers to make multiyear volume commitments as a condition of committing modular capacity.（原話："insisting as a condition of us committing our capacity"）
- 2026-04-24｜Brian Lane, CEO｜commitment：CEO reiterated commitment to consistently rewarding shareholders while maintaining balance sheet strength.（原話："remain committed to consistently rewarding our shareholders"）

### 問答異常語氣（迴避／改口／保留）
- FIX_Q1_2026_Earnings_Call_20260424.md｜問：Analyst asked for the geography and core end markets of the pending electrical acquisition.｜答法：CFO declined to give specifics, saying he 'can't get too specific' until the deal is announced because the target company's own people don't yet know.

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
{"date":"20260906","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤ $1,050（FY27 共識 EPS 17.5x）；或 Q4 FY26 訂單 ≥ $16B 且四大雲端 2028 資本支出口徑不低於 2027 → 重跑 DD、條件式上限 $1,400","irr_base_pct":0.6,"ev5y_pct":-0.9,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"-","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":0.9,"ev5y_pct":-0.9,"irr_base_pct":0.6,"max_dd_pct":-65,"bull_5y_price":2730.0,"bear_5y_price":570.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價 ≤ $1,050（FY27 共識 EPS 17.5x）；或 Q4 FY26 訂單 ≥ $16B 且四大雲端 2028 資本支出口徑不低於 2027 → 重跑 DD、條件式上限 $1,400","price_at_dd":1610.34,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FIX_20261013/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
