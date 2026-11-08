你是 stock-analyst **v20 判斷 agent**，標的 CMI（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CMI","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":9438,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99 (cmi2026q38-kex99.htm)"},"note":"未查證"},{"id":"f_kpi1_ebitda_margin_non_gaap","label":"EBITDA margin（公司主要口徑；公司不報 Non-GAAP 營業利益）","value":18.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99；EBITDA 1,786 USD m"},"note":"未查證"},{"id":"f_kpi2_gaap_operating_income","label":"GAAP operating income","value":1444,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m（利益率 15.3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99"},"note":"未查證"},{"id":"f_kpi4_guidance_fy2026_revenue_","label":"Guidance: FY2026 revenue growth","value":"約 +10%","period":"Q3 FY2026 公告（2026-11-05）","unit":"YoY","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026 公告（2026-11-05）","citation":"公司新聞稿 8-K Ex.99"},"note":"FY1 營收共識 37,168 USD m（yfinance，見 capital_structure）；未對照指引隱含值"},{"id":"f_kpi5_guidance_fy2026_ebitda_m","label":"Guidance: FY2026 EBITDA margin","value":"約 18.2%","period":"Q3 FY2026 公告（2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026 公告（2026-11-05）","citation":"公司新聞稿 8-K Ex.99（不含 Q1 低壓燃料電池事業出售 199 USD m 損失）"},"note":"未查證"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_cmi_gross_margin_pct","label":"CMI 毛利率","value":25.88,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cmi_operating_margin_pct","label":"CMI 營業利益率","value":11.79,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cmi_fcf_margin_pct","label":"CMI FCF 利潤率","value":9.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cat_gross_margin_pct","label":"CAT 毛利率","value":32.92,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cat_operating_margin_pct","label":"CAT 營業利益率","value":18.33,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cat_fcf_margin_pct","label":"CAT FCF 利潤率","value":12.36,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pcar_gross_margin_pct","label":"PCAR 毛利率","value":16.85,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PCAR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pcar_operating_margin_pct","label":"PCAR 營業利益率","value":10.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PCAR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pcar_fcf_margin_pct","label":"PCAR FCF 利潤率","value":7.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PCAR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_alsn_gross_margin_pct","label":"ALSN 毛利率","value":33.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALSN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_alsn_operating_margin_pct","label":"ALSN 營業利益率","value":18.88,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALSN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_alsn_fcf_margin_pct","label":"ALSN FCF 利潤率","value":15.85,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALSN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gnrc_gross_margin_pct","label":"GNRC 毛利率","value":39.92,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GNRC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gnrc_operating_margin_pct","label":"GNRC 營業利益率","value":10.37,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GNRC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gnrc_fcf_margin_pct","label":"GNRC FCF 利潤率","value":8.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GNRC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_free_cash_flow","label":"Free cash flow（營業現金流減資本支出，自算；公司未報）","value":1102,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）","citation":"公司新聞稿 8-K Ex.99：營業現金流 1,405、資本支出 303"},"note":"未查證"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":450.07,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-33.31,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":23.81,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（29.59 → 29.59）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（34.81 → 34.81）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（40.69 → 40.69）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":29.59,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":34.81,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":40.69,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-0.24,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 29.66 → 29.59（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":18.78,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝21.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":21.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.72,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝65.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":65.4,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.81,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝60.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":60.4,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":15.21,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 29.59，分子＝快照價 450.07","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.822,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":3334.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 7519.0、現金 4185.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":137.08,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":65028.64,"period":"2026-11-08","unit":"USD m","basis":"市值 61694.64 ＋ 淨負債 3334.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":37167.88,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":40741.03,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（18 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.75,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 450.07 / W52 577.57 / W104 464.79 / W250 327.19 / W250 13週斜率 1.46%"},{"id":"f_ma_w52","label":"52 週均線","value":577.57,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":464.79,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":327.19,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.46,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列出 Power Systems 主要對手為 Caterpillar、MTU、Kohler/SDMO，另有 INNIO、Generac、三菱重工；Engine 段獨立引擎對手為 Weichai、Yuchai、Deutz。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"Our primary competitors are Caterpillar, Inc., MTU (Rolls Royce Power Systems Group) and Kohler/SDMO (Kohler Group), but we also compete with INNIO, Generac, Mitsubishi Heavy Industries and numerous regional generator set assemblers.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：替代技術（天然氣、氫、電動）持續發展，公司將面對這些新技術帶來的新競爭；新興市場客戶出口後可能與公司既有客戶競爭。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"We primarily compete with diesel engines and related diesel products; however, new technologies continue to be developed for gasoline, natural gas, hydrogen, electrification and other technologies, and we will continue to face new competition from these expanding technologies.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"搜尋摘要：資料中心發電機市場研究稱 Caterpillar 2025 年占比逾 19%；未找到 Cummins 2026 年份額增減的一手數據。","source":"GM Insights data center generator market（經搜尋摘要）","url":"https://gminsights.com/industry-analysis/data-center-generator-market/market-share","excerpt":"Caterpillar Inc. led with over 19% market share in 2025.","as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Cummins 預期新 X10 引擎將提升重型卡車引擎份額","source":"pulse.bot","url":"https://www.pulse.bot/manufacturing/news/cummins-expects-x10-to-lift-heavy-duty-truck-engine-share-81957435-dfac-46aa-9584-1e189c35ea6c/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"PACCAR為最大客戶，占2025合併銷售13%（2024、2023為16%）；長約不保證特定數量；失去該客戶或PACCAR產量大降會有不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"PACCAR is our largest customer, accounting for 13 percent of our consolidated net sales in 2025, 16 percent in 2024 and 16 percent in 2023.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K風險因素載明部分現有客戶可能自行開發或改向其他製造商採購（電動化動力系統情境）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"Some of our existing customers could choose to develop their own or source from other manufacturers.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"PACCAR 為 CMI 最大客戶，2025 年占合併淨銷售 13%（2024、2023 各 16%），是唯一超過 10% 的客戶；供應協議不保證特定數量，失去該客戶或其車款產量大減將對營運與財務產生不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"PACCAR is our largest customer, accounting for 13 percent of our consolidated net sales in 2025, 16 percent in 2024 and 16 percent in 2023.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"對 PACCAR 的銷售額約 44 億美元（2025）、54 億（2024）、55 億（2023）；無其他客戶超過 10%。","source":"SEC EDGAR 10-K FY2025 Item 8 Financial Statements","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"Worldwide sales to this customer were approximately $4.4 billion, $5.4 billion and $5.5 billion for the years ended December 31, 2025, 2024 and 2023, representing 13 percent, 16 percent and 16 percent, respectively, of our consolidated net sales. No other customer accounted for more than 10 percent of consolidated net sales.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Cummins 管理層在 Q4 2025 財報會議稱訂單進帳創紀錄、已接單到 2028 年，發電積壓訂單創新高，形容為「multi-year strength」","source":"Motley Fool, Cummins Q4 2025 earnings call transcript","url":"https://www.fool.com/earnings/call-transcripts/2026/02/05/cummins-cmi-q4-2025-earnings-call-transcript/","excerpt":null,"as_of":"2026-02-05","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Cummins Q2 2026 創紀錄，資料中心備援電力訂單強勁，Power Systems 營收年增 19% 至 23 億美元，並上調 2026 展望","source":"SEC 8-K Cummins Q2 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000026172/000002617226000026/cmi2026q28-kex99.htm","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026 年 2 月 Barclays 會議摘要：管理層預期資料中心發電需求整個十年強勁、至少未來五年能見度高；長期情境較不確定；積壓集中於大型超大規模業者","source":"Quartr, Cummins Barclays 43rd Annual Industrial Select Conference summary","url":"https://quartr.com/events/cummins-inc-cmi-barclays-43rd-annual-industrial-select-conference_3ehQviHi","excerpt":null,"as_of":"2026-02-18","retrieved_at":"20261108","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"風險面：分析師點出重/中型卡車週期長期低迷、競爭加劇（Caterpillar 發電銷售增 72%、Generac 資料中心積壓約 16 億美元）、EPA27 與關稅不確定","source":"rallies.ai / Nasdaq (Generac backlog) 摘要","url":"https://rallies.ai/news/cummins-jumps-3-as-data-center-power-backlog-and-bullish-targets-lift-sentiment","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"RSM 2026 年 6 月報告：資料中心熱潮下工業需要為多年交期投資產能與人力；供應鏈已自行擴產但集中於資料中心需求","source":"RSM US, Data center boom reshaping industrial ecosystem","url":"https://www.rsmus.com/insights/industries/manufacturing/data-center-boom-reshaping-industrial-ecosystem","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Cummins 2023 年 12 月與 EPA、CARB、DOJ、加州檢察長就皮卡引擎排放認證達成和解，2024 年 4 月生效，2024 Q2 付 19 億美元；10-K 稱仍可能有額外監管行動與附帶訴訟。屬環保執法，非反壟斷。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"we have incurred, and likely will incur, other additional claims, costs and expenses in connection with the matters covered by the Settlement Agreements and other matters related to our compliance with emission standards for our engines, including with respect to additional regulatory action and collateral litigation related to these matters.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：Cummins 依賴全球供應鏈，關稅與貿易中斷（禁運、制裁、出口管制）可能衝擊生產成本、需求與客戶／供應商關係；美中出口管制與制裁變動可能影響應收帳款回收、中國現金調回、售後與保固支援及銷售。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"Embargoes, sanctions and export control laws are changing rapidly for certain geographies, including with respect to China. In particular, changing U.S. export controls and sanctions on China, as well as other restrictions affecting transactions involving China and Chinese parties, could affect our ability to collect receivables, access cash generated in China, provide aftermarket and warranty support for our products, sell products and otherwise impact our reputation and business","as_of":"2026-02-10","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2025 年關稅淨財務影響（扣除緩解措施）對獲利與營運現金流不重大；公司透過供應商協商、替代採購與客戶成本回收緩解。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"The financial impact of tariffs, net of mitigation actions, was immaterial to our profitability and operating cash flows during 2025.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"MD&A 展望：關稅、出口管制與地緣緊張帶來不確定性，成本與關稅上升可能衝擊獲利，貿易中斷可能造成生產中斷。","source":"SEC EDGAR 10-K FY2025 Item 7 Outlook","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"Increases in costs, tariffs, as well as other inflationary pressures, could negatively impact earnings.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Q3 2025 財報電話會議：關稅成本於第三季上升，接近完全回收先前公布的關稅；單季淨衝擊為數千萬美元級。","source":"Motley Fool Q3 2025 earnings call transcript","url":"https://www.fool.com/earnings/call-transcripts/2025/11/06/cummins-cmi-q3-2025-earnings-call-transcript","excerpt":null,"as_of":"2025-11-06","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Q3 2026 10-Q：主要風險含全球貨運減少、供應商與終端成本上升、供應可得性不確定；稱關稅淨影響 Q1 不重大；並稱 single source 多項關鍵零件與原料","source":"Cummins 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0000026172/000002617226000037/cmi-20260930.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 歷年風險因子：易受單一來源供應商短缺影響","source":"Cummins 10-K FY2020","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617221000012/cmi-20201231.htm","excerpt":"We are vulnerable to supply shortages from single-sourced suppliers, including suppliers that may be impacted by the COVID-19 pandemic, and any delay in receiving critical supplies could have a material adverse effect on our results of operations, financial condition and cash flows. We single source a significant number of parts and raw materials","as_of":"2021-02-15","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收 $9.4B（+13% YoY）；Engine $3.1B +20%、Components $2.9B +23%、Distribution $3.3B +4%、Power Systems $2.3B +15%（EBITDA 率 25.4%，資料中心發電需求驅動）、Accelera $103M -15%。","source":"Cummins Q3 2026 8-K Ex.99 / 新聞稿彙整","url":"https://www.sec.gov/Archives/edgar/data/0000026172/000002617226000035/cmi2026q38-kex99.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"全年營收成長指引由 10–13% 下修至約 10%，主因北美皮卡需求疲弱；發電與重型卡車需求仍強。","source":"Cummins Q3 2026 新聞稿彙整（investingnews）","url":"https://investingnews.com/cummins-reports-strong-third-quarter-2026-results/","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026：Power Systems 營收 +19% 至 $2.255B，EBITDA 率 24.5%（前年 22.8%）；公司稱資料中心發電需求強勁；Texas 資料中心天然氣發電機組合約涵蓋 2026–2030；X10/X15 新引擎 2027 分階段放量（EPA 擬議排放規則）。","source":"Cummins Q2 2026 8-K Ex.99 / IVT International","url":"https://www.sec.gov/Archives/edgar/data/0000026172/000002617226000026/cmi2026q28-kex99.htm","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Cummins 於 2026 Q1 出售低壓燃料電池業務，淨付款 1.75 億美元、淨費用 1.99 億美元；Accelera 零排放事業 Q2 銷售 1.45 億美元、EBITDA 虧損 6,900 萬美元，公司稱將放慢並聚焦零排放投資節奏","source":"Cummins 8-K Ex.99 Q2 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000026172/000002617226000026/cmi2026q28-kex99.htm","excerpt":"In the first quarter of 2026, we sold our low pressure fuel cell business to a customer","as_of":"2026-08-04","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Cummins 10-K 指出資料中心產品需求延伸六至八季，積壓訂單看似強；一手文件未見替代技術取代核心引擎的描述","source":"Cummins 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"We also have strong demand for our data center products extending out six to eight quarters.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Caterpillar 發電銷售成長 72%，大型發電機組與渦輪用於資料中心，競爭壓力增加","source":"Equipment World: Caterpillar, Cummins, Rehlko generators power data center boom","url":"https://www.equipmentworld.com/business/article/15826765/caterpillar-cummins-rehlko-generators-power-data-center-boom","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025: Distribution segment is Cummins' primary sales, service and support channel (30% of 2025 consolidated sales, 34% of EBITDA, up from 25%/24% in 2023); 一手紀錄未顯示訂閱化/D2C 等通路結構轉移，通路仍為經銷網路","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"The Distribution segment is our primary sales, service and support channel. The segment serves our customers and certified dealers through a worldwide network of wholly-owned, joint venture and independent distribution locations.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q1 2026 10-Q: Components drivetrain and braking sales decreased partly due to a changed business model in India","source":"SEC EDGAR 10-Q Q1 2026","url":"https://www.sec.gov/Archives/edgar/data/0000026172/000002617226000016/cmi-20260331.htm","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026-11-05 Q3 後公司把全年營收成長指引由 10–13% 收窄為約 10%（北美皮卡需求弱），EBITDA margin 約 18.2% 仍在原 18–18.5% 區間；Q3 營收約 $9.44B 低於市場預期約 $9.87B，EPS $8.25 與共識 $8.28 約當（聚合摘要，未逐字核對 8-K）。5 月、8 月曾兩度上修。","source":"SEC 8-K Q3 2026 exhibit 99 / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0000026172/000002617226000035/cmi2026q38-kex99.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 後分析師目標價共識：StockAnalysis 21 位平均目標約 $756.52、評級 Buy；Truist 目標 $894 由 $901 下修，JPMorgan $690 由 $725 下調（Neutral）。為 Q3 前資料，Q3 後修正未見。","source":"StockAnalysis CMI ratings","url":"https://stockanalysis.com/stocks/cmi/ratings/","excerpt":"The 12-month stock price target is $756.52.","as_of":"2026-08-23","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat：16 位分析師平均目標約 $745.64，區間 $500–$894，共識評級 Moderate Buy（最新評級日 2026-08-23）。","source":"MarketBeat CMI forecast","url":"https://www.marketbeat.com/stocks/NASDAQ/CMI/forecast/","excerpt":"the average price target is $745.64. The highest price target for CMI is $894.00, while the lowest price target for CMI is $500.00.","as_of":"2026-08-23","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 SEC 8-K 共5份，無併購/重編/下市等重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01）。","source":"SEC EDGAR 8-K 申報清單 2025-11-08~2026-11-08","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000026172&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 5 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"NHTSA 對 Cummins 召回 campaign 26E066（L9 燃油濾清器油管可能鬆脫漏油）發出受理函，約39,052件；車主通知預計2026-11-20寄出。為召回受理函，非 warning letter。","source":"NHTSA RCAK-26E066 acknowledgment letter","url":"https://static.nhtsa.gov/odi/rcl/2026/RCAK-26E066-6960.pdf","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2026年3月 NHTSA 召回 26E011000：Cummins PD7000 電驅單元軟體錯誤可能造成非預期移動（約411~413台）。","source":"vehiclesafetyrecalls.com NHTSA 26E011000","url":"https://vehiclesafetyrecalls.com/recall/26E011000","excerpt":null,"as_of":"2026-03-13","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2024年起的證券集體訴訟 Baker v. Cummins（C.D. Cal.），涉及排放認證／defeat device，期間2019-04-30至2023-12-21；搜尋所見為2024年律所公告，目前進度未核實。","source":"Kessler Topaz Meltzer Check notice (BusinessWire)","url":"https://www.businesswire.com/news/home/20240304811825/en/Kessler-Topaz-Meltzer-Check-LLP-Reminds-Investors-of-Securities-Fraud-Class-Action-Against-Cummins-Inc.-CMI-and-Urges-CMI-Investors-with-Substantial-Losses-to-Contact-the-Firm/","excerpt":null,"as_of":"2024-03-04","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Cummins Q2 2026：北美重卡需求預測上調至 24–25 萬輛（原 23–25 萬）；公司稱卡車廠即使訂單轉強也不太可能提高產量；Q2 業界重卡產量 6 萬輛、年減 4%。","source":"Transport Topics, Replacement demand drives Cummins HD truck guidance hike","url":"https://www.ttnews.com/articles/cummins-earnings-q2-2026","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Cummins 2026 年 6 月 Wells Fargo 會議摘要：發電產能擴充約 20 GW、投資 $4.5 億，主要在既有廠區（Seymour、Daventry 等），訂單排到 2028；Q2 財報稱 2026 成長仍受大型發電機組產能限制。","source":"Quartr, Cummins 16th Annual Wells Fargo Industrials & Materials Conference summary","url":"https://quartr.com/events/cummins-inc-cmi-16th-annual-wells-fargo-industrials-materials-conference_3ehQvq9r","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Cummins Rocky Mount 引擎廠 $5.8 億升級預計 2027 完成；另有 Jamestown $4.52 億升級進行中；PACCAR 在 Columbus, Mississippi 投資逾 $2 億擴引擎產能（2024 Q2 公布）。","source":"Manufacturing Dive / Benzinga search results","url":"https://www.manufacturingdive.com/news/cummins-plans-580-investment-to-upgrade-rocky-mount-engine-plant-whitakers-north-carolina-plant/704844/","excerpt":null,"as_of":"2026-01-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Cummins 8-K Q2 2026 新聞稿：Power Systems 營收創高、產能限制說明","source":"SEC 8-K FY2026 Q2 ex99","url":"https://www.sec.gov/Archives/edgar/data/0000026172/000002617226000026/cmi2026q28-kex99.htm","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"Class 8 orders rebounded sharply in 2026: ACT May 2026 preliminary orders up 103% y/y; FTR YTD order intake +112%; while Class 8 sales Jan-May 2026 were 73,419 units, down 16% y/y (Omdia).","source":"carrieratlas.com / truckpartsandservice.com (ACT/FTR/Omdia data)","url":"https://carrieratlas.com/class-8-orders-double-year-over-year-in-may-2026","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"ACT January 2026 outlook said manufacturers carried production restraint into early 2026 to work down excess inventory (destocking phase early 2026).","source":"ACT Research Class 8 Truck Market 2026","url":"https://www.actresearch.net/resources/blog/class-8-truck-sales-forecast-2026","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Cummins 10-Q: finished products inventory rose from $3,091M (2025-12-31) to $3,215M (2026-03-31) to $3,560M (2026-09-30); filings do not break out distributor vs company-held inventory.","source":"Cummins Form 10-Q for period ended 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0000026172/000002617226000037/cmi-20260930.htm","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"Q2 2026 Cummins results tied partly to OEM inventory stocking to mitigate logistics risks in the Middle East; Distribution segment sales up 9% to $3.3B.","source":"Truck Parts & Service: Cummins raises 2026 outlook in Q2 earnings report","url":"https://www.truckpartsandservice.com/business/outlook-and-benchmarking/article/15831613/strong-onhighway-demand-and-data-centers-drive-cummins-secondquarter-revenues-up-9","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#4","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"US PPI for special industry machinery rose Dec 2025 299.081 -> Jan 2026 301.619 -> Feb 2026 303.624 (price trend firming; not a spot/contract series for CMI end-markets).","source":"FRED WPS116","url":"https://fred.stlouisfed.org/series/WPS116","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2008Q4（上一輪衰退起點）EBIT 率由 9.2% 降到 3.9%（排除重整費用 5.0%）；公司 2009 年初指引銷售降約 20%、EBIT 率 6.5%","source":"Cummins press release 2009-02-03 (8-K)","url":"https://www.sec.gov/Archives/edgar/data/0000026172/000002617209000008/escumminspressrelease020309.htm","excerpt":"EBIT decreased to $129 million, or 3.9 percent of sales, from $324 million, or 9.2 percent of sales a year ago. Excluding the restructuring charge, EBIT was $166 million, or 5.0 percent of sales.","as_of":"2009-02-03","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"2020Q1 營收年減 17%，合併 EBITDA 率 16.9%（去年同期 17.2%），顯示 2019-20 下行初期利潤率僅小幅下滑","source":"Cummins Revenue Drops 17 Percent in First Quarter (RER Magazine)","url":"https://www.rermag.com/news-analysis/wall-street-beat/article/21130168/cummins-revenue-drops-17-percent-in-first-quarter","excerpt":"consolidated EBITDA was 16.9 percent of sales, compared to 17.2 percent a year ago","as_of":"2020-05-05","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2019 年 Class 8 產量九個月內下降 55%，高階主管稱 18 年來未見；ACT 稱高峰通常持續約 13-15 個月","source":"ACT Research / trucknews.com","url":"https://www.trucknews.com/business-management/heavy-duty-vehicle-market-on-edge-of-precipice-act-research/1003093170","excerpt":null,"as_of":"2019-06-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K中無併購類重大項目（2.01等）；搜尋亦未見2026年新併購，僅見舊案（Meritor 2022）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000026172&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 5 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"證券集體訴訟 Baker v. Cummins（C.D. Cal.）針對排放認證事件，為2024年提起之舊案，現況未核實；10-K 稱公司面臨日常訴訟。","source":"Kessler Topaz Meltzer Check notice (BusinessWire)","url":"https://www.businesswire.com/news/home/20240304811825/en/Kessler-Topaz-Meltzer-Check-LLP-Reminds-Investors-of-Securities-Fraud-Class-Action-Against-Cummins-Inc.-CMI-and-Urges-CMI-Investors-with-Substantial-Losses-to-Contact-the-Firm/","excerpt":null,"as_of":"2024-03-04","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K FY2025 Item 3 併入 Note 14 訴訟說明；EPA/CARB/DOJ 和解2024-04生效，2024Q2支付19億美元。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm","excerpt":"In the second quarter of 2024, we made $1.9 billion of payments required by the Settlement Agreements.","as_of":"2026-02-10","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"NHTSA campaign 26E066：L9 燃油濾清器油管可能鬆脫漏油，約39,052件，受理函日期2026-09-30。","source":"NHTSA RCAK-26E066 acknowledgment letter","url":"https://static.nhtsa.gov/odi/rcl/2026/RCAK-26E066-6960.pdf","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"product_recall_warning#1","axis":"product_recall_warning","section":"events","direction":"-","claim":"NHTSA campaign 26E011000：PD7000 電驅單元軟體錯誤可能造成非預期移動。","source":"vehiclesafetyrecalls.com NHTSA 26E011000","url":"https://vehiclesafetyrecalls.com/recall/26E011000","excerpt":null,"as_of":"2026-03-13","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K無 Item 4.02（財報不可依賴）項目；搜尋僅見2006年舊案SEC和解（2003年應付帳款重編）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000026172&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 5 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 11 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"CMI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":25.88,"operating_margin_pct":11.79,"fcf_margin_pct":9.66,"rd_intensity_pct":4.17},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMI","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"CAT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":32.92,"operating_margin_pct":18.33,"fcf_margin_pct":12.36,"rd_intensity_pct":2.97},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAT","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"PCAR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":16.85,"operating_margin_pct":10.75,"fcf_margin_pct":7.44,"rd_intensity_pct":1.51},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PCAR","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"ALSN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":33.95,"operating_margin_pct":18.88,"fcf_margin_pct":15.85,"rd_intensity_pct":4.06},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALSN","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"GNRC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":39.92,"operating_margin_pct":10.37,"fcf_margin_pct":8.97,"rd_intensity_pct":5.48},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GNRC","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"CMI"},"financial_history":{"ticker":"CMI","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":28074000000.0,"revenue_yoy_pct":null,"gross_margin_pct":23.93,"operating_margin_pct":9.19,"net_income":2151000000.0,"diluted_eps":15.12,"free_cash_flow":1046000000.0,"fcf_margin_pct":3.73,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":34065000000.0,"revenue_yoy_pct":21.34,"gross_margin_pct":24.22,"operating_margin_pct":3.75,"net_income":735000000.0,"diluted_eps":5.15,"free_cash_flow":2753000000.0,"fcf_margin_pct":8.08,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":34102000000.0,"revenue_yoy_pct":0.11,"gross_margin_pct":24.75,"operating_margin_pct":9.89,"net_income":3946000000.0,"diluted_eps":28.37,"free_cash_flow":279000000.0,"fcf_margin_pct":0.82,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":33670000000.0,"revenue_yoy_pct":-1.27,"gross_margin_pct":25.29,"operating_margin_pct":11.48,"net_income":2843000000.0,"diluted_eps":20.5,"free_cash_flow":2386000000.0,"fcf_margin_pct":7.09,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CMI/CMI_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**Cummins Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Greetings, and welcome to Cummins Inc. Third Quarter 2026 Earnings Conference Call. [Operator Instructions] As a reminder, this conference is being recorded. It is now my pleasure to introduce your host, James Hopkins, Vice President, Financial Planning, Capital Management and Investor Relations. Please go ahead.

**James Hopkins** (Executives):
Thank you, Donna. Good morning, everyone, and welcome to our teleconference today to discuss Cummins' results for the third quarter of 2026. Participating with me today are Jennifer Rumsey, our Chair and Chief Executive Officer; and Mark Smith, our Chief Financial Officer. We will all be available to answer questions at the end of the teleconference. 
Before we start, please note that some of the information you will hear or be given today will consist of forward-looking statements within the meaning of the Securities Exchange Act of 1934. Such statements express our forecasts, expectations, hopes, beliefs and intentions on strategies regarding the future. Our actual future results could differ materially from these projected in such forward-looking statements because of several risks and uncertainties. 
More information regarding such risks and uncertainties is available in the forward-looking disclosure statement in the slide deck and our filings with the Securities and Exchange Commission, particularly the Risk Factors section of our most recently filed annual report on Form 10-K and any subsequently filed quarterly reports on Form 10-Q. During this call, we'll be discussing certain non-GAAP financial measures, and we will refer you to our website for the reconciliation of those measures to GAAP financial measures. Our press release with a copy of the financial statements and a copy of today's webcast presentation are available on the website within the Investor Relations section of cummins.com. 
With that out of the way, I wanted to share that I look forward to reconnecting with the investment community in my previously announced role overseeing Investor Relations as the Vice President of Financial Planning, Capital Management and Investor Relations and continue our dialogue about Cummins' performance and future prospects for profitable growth. I look forward to speaking with many of you in our follow-up conversations after today's call. 
With that, I will turn it over to our Chair and CEO, Jennifer Rumsey, to kick us off.

**Jennifer Rumsey** (Executives):
Thank you, James. It's great to have you back on our earnings calls as a part of your new role. Good morning, everyone. I'll start with a few highlights from the third quarter and an overview of our financial results. I'll then discuss key trends across our markets and provide an update on our outlook for the remainder of 2026. Mark will follow with additional details on our third quarter results and full year forecast. 
Before turning to our financial performance, I want to highlight a few important milestones from the quarter. In August, we announced that our Power Systems business was selected to supply battery energy storage systems for a large U.S. data center project. These systems will help manage AI-driven fluctuations in power demand, improve grid stability and enhance power reliability. This will be our largest battery energy storage system deployment to date and an important milestone as we expand our capabilities to meet the evolving power needs of data center customers. 
We continue to make meaningful progress and remain on track with the power generation capacity expansion plans we outlined at our recent Analyst Day. This includes strengthening our global supply chain, which remains a key pacing item as we bring additional capacity online to meet exceptionally strong demand in power generation, particularly from data center customers. Recently, we celebrated the opening of a 500,000-square-foot manufacturing facility for our IEA cooling systems business in Somers, Wisconsin. 
This approximately $100 million investment will more than double IEA's production capacity and strengthen our ability to supply critical cooling systems for our generator sets. We also made important progress preparing for the upcoming launch of our HELM engine platforms. During the quarter, we completed our 2026 Forever Rising Tour, giving more than 500 customers and dealers the opportunity to experience our 2027 X15 engine, alongside our X10 and natural gas X15N engines. 
Customer feedback has been very positive, particularly around performance, drivability and confidence in Cummins reliability and support network. Hearing directly from customers is an important part of our launch preparations, and reinforces our confidence in these products as we prepare to bring them to market. Together, these milestones demonstrate the progress we're making against our strategic priorities, strengthening our core business, expanding our capabilities and investing in technologies and capacity needed to support our customers and drive long-term growth. 
Now let me turn to our third quarter financial performance in key markets. We delivered third quarter revenues of $9.4 billion, an increase of 13% compared to the third quarter of 2025. Growth was driven primarily by improved demand in North America heavy and medium-duty truck markets, and continued strength in global power generation, particularly from data center customers, contributing to record sales in our Power Systems segment. We achieved record quarterly EBITDA of $1.8 billion or 18.9% of sales, compared to $1.2 billion or 14.3% of sales a year ago. 
Last year's results include a $240 million goodwill impairment charge and inventory write-down related to our Accelera business. Excluding these charges, EBITDA margin improved approximately 170 basis points year-over-year, primarily reflecting higher volumes, partially offset by increased variable compensation expenses associated with our expectations for a full year record earnings.
Turning to our key markets. Third quarter revenues in North America increased 15% compared to third quarter of 2025. Industry production of heavy-duty trucks in the third quarter was in line with our expectations at 70,000 units, up 62% from 2025 levels, while our heavy-duty unit sales were 24,000, up 68% year-over-year. In the medium-duty truck market, industry production increased 77% to 36,000 units while our unit sales were up 33,000, up 88% year-over-year. 
Despite the strong year-over-year growth, demand was below our expectations as regulatory uncertainty and the anticipated phased transition to EPA '27 products continued to delay some customer purchasing decisions. We shipped 34,000 engines for pickup trucks in the third quarter of 2026, down 16% from a year ago. Demand was weaker than anticipated amid elevated diesel prices and interest rates. North America Power Generation revenues increased 22%, driven primarily by continued strong data center demand and supported by the additional manufacturing capacity we brought online at the end of 2025. 
While we achieved record power generation sales this quarter, revenues were below our expectations as supply chain constraints limited shipments across both Power Systems and Distribution, which we expect to largely catch up in the fourth quarter. We continue to see robust order intake and engaged in multiyear strategic planning discussions with large data center customers. 
Turning to our International markets. Revenues increased 11% compared to the third quarter of last year. In China, third quarter revenues, including joint ventures, increased 9% to $1.9 billion, supported by accelerating data center demand. Industry demand for medium- and heavy-duty trucks in China was 297,000 units, a decrease of 5% compared to last year. Domestic demand remained challenged by elevated fuel costs, partially offset by strong export demand, particularly in Africa and Southeast Asia. 
Our sales in units, including joint ventures, were 42,000, a decrease of 15%, reflecting increased adoption of battery electric trucks in the domestic market. Industry demand for excavators in China in the third quarter was 62,000 units, an increase of 15% from 2025 levels. We sold 12,000 units, up 28%, driven by export demand associated with mining investments in Africa and Indonesia as well as domestic demand for rural development. Sales of power generation equipment in China increased 42% in the third quarter due to accelerating data center demand. In India, third quarter revenues, including joint ventures, were $803 million, an increase of 13% from a year ago. Industry truck production increased 30% from 2025, driven by increased freight, infrastructure and mining activity. 
Now let me provide our outlook for 2026, including comments on several of our key markets. We have updated our full year 2026 outlook and now expect revenue growth of approximately 10% and an EBITDA margin of approximately 18.2% compared to our prior guidance ranges of 10% to 13% revenue growth and 18% to 18.5% EBITDA margin. In North America, we are maintaining our 2026 heavy-duty truck market forecast of 240,000 to 250,000 units. For medium-duty trucks, we are lowering our forecast to 125,000 to 130,000 units, compared to our prior outlook of 130,000 to 140,000 units, reflecting weaker-than-expected third quarter demand as regulatory uncertainty delayed customer purchasing decisions.
Looking ahead, we expect fourth quarter production in both markets to remain strong near third quarter levels, with supply chain constraints limiting the potential for additional upside. For our North America pickup truck engine business, we are now lowering our 2026 shipment forecast to 118,000 to 122,000 units compared to our prior guidance of 125,000 to 140,000 units. We expect demand to moderate further in the fourth quarter, reflecting continued pressure from elevated diesel prices and interest rates. 
In China, we continue to expect total revenue, including joint ventures, to increase approximately 15% in 2026, consistent with our prior outlook, primarily driven by strong demand in power generation, particularly from data center customers. For China heavy and medium-duty truck demand, we continue to expect industry demand to range from a decline of 5% to an increase of 5%. As we saw in the third quarter, elevated fuel prices have contributed to a shift toward battery electric trucks, while export demand for diesel-powered trucks remain strong, particularly in Africa and Southeast Asia. 
In India, we expect total revenue, including joint ventures, to increase approximately 5% in 2026. We continue to expect full year industry truck demand to be approximately flat at the midpoint of our forecasted range, supported by recent tax rate reduction. For global construction markets, we are maintaining our outlook for demand to increase 10% to 20%. In China, we expect export demand to remain strong, while demand in North America is expected to remain relatively flat amid elevated interest rates. 
In Power Generation, we continue to expect global revenue to increase 15% to 25% this year, consistent with our prior guidance. We expect to recover most of the shipments delayed by third quarter supply constraints in the fourth quarter, and demand remains exceptionally strong across North America, China and the broader Asia Pacific region. We're expanding our manufacturing capacity and demand continues to grow with customers increasingly ordering smaller displacement generator sets as availability of larger configurations remains constrained. 
In mining, we continue to expect engine sales to range from a decline of 5% to an increase of 5% for the year, consistent with our prior guidance. Fleet replacement activity remains supportive in several markets, although elevated inventory levels and others are expected to moderate demand through the remainder of the year. For aftermarket, we are maintaining our outlook for revenue growth of 3% to 8% in 2026, supported by aging fleets and increased parts consumption. 
In summary, we delivered a strong third quarter with record profitability and continued growth across several of our key markets. Our updated full year outlook reflects continued strength across most of our business, tempered by lower-than-expected pickup truck demand. As we enter the fourth quarter, we remain focused on executing our strategy and delivering our commitments to customers and shareholders. We remain on track with the commitments outlined at our recent Analyst Day, including expanding our production capacity and investing in new products and technologies to strengthen our product portfolio.
Finally, I want to thank our employees and leaders around the world for their continued commitment to our customers and to each other through a dynamic time. Their dedication, teamwork and focus on execution continue to differentiate Cummins and position us to deliver for our customers while creating long-term value for our shareholders. 
Now I'll turn it over to Mark.

**Mark Smith** (Executives):
Thank you, Jen, and good morning, everyone. Before reviewing our third quarter financial results in detail, I'd like to summarize 5 key takeaways. First, we delivered record profitability and strong operating cash flow, putting us on track to extend our record of raising performance cycle over cycle. Second, our year-over-year revenue growth rate continues to accelerate. After reporting a 3% growth in Q1 and 9% in Q2, we reported 13% top line increase in the third quarter and implied in our updated full year guidance is 15% growth in the fourth quarter. 
Third quarter growth was underpinned by exceptionally strong demand for power generation equipment, particularly among global data center customers, along with improving orders for North America medium- and heavy-duty trucks. Our fourth key takeaway is that we returned $661 million to shareholders through share repurchases and cash dividends. And as we enter the fourth quarter and expect to generate record full year operating cash flow, returning excess cash to shareholders remains an important priority.
Finally, we've updated our full year 2026 outlook. We now expect revenue growth of approximately 10% at the lower end of the prior range and an EBITDA margin of approximately 18.2%, consistent with our prior range of 18% to 18.5%. Lower-than-expected pickup truck volumes in North America are the primary reason for the downward revision to revenue guidance. 
Let me now walk through the financials in a little more detail. Third quarter revenues were $9.4 billion, up 13% from a year ago. Sales in North America increased 15%, while international revenues grew 11%. EBITDA was a record $1.8 billion or 18.9% of sales, compared with $1.2 billion or 14.3% of sales a year ago. Excluding the $240 million in Accelera goodwill impairment and inventory charges recorded in the prior year, EBITDA margin improved 170 basis points from 17.2% to 18.9%. 
Higher volumes contributed to the improved profitability, partially offset by increased variable compensation expense, reflecting our outlook for record full year earnings. The net impact of tariffs, if we're still asking about that, was immaterial in the quarter. Gross margin was $2.6 billion or a record 27.7% of sales compared with $2.1 billion or 25.6% of sales a year ago. The prior year included a $30 million noncash inventory write-down related to our electrolyzer business, included in the Accelera charges discussed earlier. 
Excluding the inventory charge, gross margin improved from 26% to 27.7%. Higher volumes and favorable pricing, particularly in power generation, drove the improvement, partially offset by higher freight cost, some material costs and increased variable compensation expense. Selling, administrative and research expenses were $1.3 billion or 13.4% of sales compared with $1.1 billion or 13.6% of sales a year ago. The increase in dollars was driven primarily by higher development spending for upcoming North America on-highway platform launches as well as the new mining and natural gas power generation platforms. 
Higher variable compensation expense affected both cost of sales and operating expenses across our segments in the year-over-year comparisons. And I won't repeat that driver in each segment discussion, unless it's the principal driver of the variation in results. Joint venture income was $127 million, up $23 million from the prior year, primarily driven by a stronger performance in our Chongqing joint venture within Power Systems in China. Other income was positive $27 million compared with a loss of $186 million in the prior year. Excluding the prior year $210 million noncash goodwill impairment charge, other income was roughly flat year-over-year. Interest expense was $81 million, down $2 million from a year ago.
The all-in effective tax rate was 17.7%, including $75 million of favorable discrete tax items or $0.54 per diluted share. All-in net earnings were $1.1 billion or $8.25 per diluted share compared with $536 million or $3.86 per diluted share a year ago. The prior year included $240 million in noncash Accelera charges equivalent to $1.73 per diluted share. All-in operating cash flow was $1.4 billion compared with $1.3 billion a year ago. 
During the quarter, we returned $661 million to shareholders, consistent with our long-standing commitment to return approximately 50% of operating cash flow to shareholders. The quarterly returns included $359 million in share repurchases and $300 million in cash dividends. I will now review segment performance briefly and our guidance for 2026. Engine business third quarter revenues were $3.1 billion, up 20% from a year ago. EBITDA margin improved 350 basis points to 13.5% from 10% a year ago, primarily due to higher North America heavy and medium-duty truck volumes more than offsetting weakness in the pickup truck market.
For 2026, we now expect revenue growth of 8% to 11% compared to our prior guide of 9% to 14% and EBITDA margins of 12.25% to 12.75% compared with 12.5% to 13.25% previously. This updated outlook primarily reflects lower pickup truck demand. Components revenues were $2.9 billion, up 23% from a year ago. EBITDA margin improved 180 basis points to 14.3% from 12.5%, primarily driven by higher North American heavy- and medium-duty truck volumes. For 2026, we now expect Components revenue growth of 8% to 11% compared with our prior guide of 8% to 13%. We have updated our EBITDA margin outlook to 13.25% to 13.75% compared with 13.5% to 14.25% previously. 
These revisions primarily reflect lower-than-expected pickup demand as well as weaker domestic on-highway demand in China. Distribution revenues increased 4% from a year ago to $3.3 billion, and EBITDA margin declined to 13.9% from 15.5% a year ago, driven by a lower mix of aftermarket revenues. For 2026, we now expect revenue growth of 10% to 13% compared with our prior guidance of 9% to 14% and EBITDA margins of 13.6% to 14.1%, a tightening of the prior range of 13.5% to 14.25%.
Power Systems revenues were a record $2.3 billion, up 15% year-over-year, and EBITDA margin increased 250 basis points to 25.4% from 22.9% a year ago, driven primarily by stronger power generation demand globally and favorable pricing. For 2026, we now expect Power Systems revenue growth 15% to 18% compared with our prior range of 14% to 19% and EBITDA margins at 25.1% to 25.6% which is a slight tightening compared to the prior range of 25% to 25.75%, unchanged.
For both Power Systems and Distribution, the outlook reflects the anticipated fourth quarter recovery of most of the shipments that were delayed from the third quarter. Accelera revenues were $103 million compared with $121 million a year ago, mainly due to lower electrolyzer sales. EBITDA was a loss of $56 million compared with a loss of $96 million a year ago, excluding the noncash charges described earlier. This improvement reflects the benefits of previously implemented cost reduction actions. For 2026, we now expect Accelera revenues of $350 million to $400 million and net losses -- net EBITDA loss of $260 million to $290 million, consistent with our prior guidance. 
I also want to highlight an update on our HyLYZER electrolyzer products. During the third quarter, 2 wholly-owned subsidiaries, Hydrogenics and Hydrogenics Europe N.V., issued a stop-use recommendation to customers of HyLYZER electrolyzer products following a planned review of operational data from the installed fleet. At this time, Hydrogenics has not initiated a recall campaign and continues to evaluate whether any modifications are required to return the electrolyzers to service. The potential financial impact of this remains under evaluation and is not reflected in our guidance. 
In summary, we've updated our full year 2026 outlook for the company. We now expect revenue growth of approximately 10% at the lower end of the prior range, an EBITDA margin of approximately 18.2% within the prior range of 18% to 18.5%. Our effective tax rate is expected to be approximately 23% in '26, excluding any discrete items. Our outlook for capital investments is unchanged between $1.35 billion and $1.45 billion, as we continue to make critical investments to support future growth. 
Overall, we delivered a strong third quarter with record profitability, solid cash generation and continued growth across several key markets, demonstrating progress to our 2030 Analyst Day targets. Revenues in Q3 were a little below our own expectations. Implied in our guidance is stronger fourth quarter revenue with a key step-up in distribution revenues, an important driver tied to power generation products, especially data centers. 
Our strong balance sheet and record cash flow generation give us the financial flexibility to fund long-term growth investments while continuing to prioritize returning excess cash to shareholders. So far this year, we returned a total of $1.681 billion in the form of cash dividends and share repurchases reflecting our confidence in our future prospects. I want to thank our employees around the world for their continued dedication and commitment to customers. 
Now let me turn it back over to James, who assures me his greatly missed earnings day and all the callbacks he's looking forward to after this call. Thank you.

**James Hopkins** (Executives):
Thanks, Mark. [Operator Instructions] Donna, with that, we're ready for our first question.

**Operator** (Operator):
[Operator Instructions] Today's first question is coming from Angel Castillo of Morgan Stanley.

**Oliver Z Jiang** (Analysts):
This is Oliver on for Angel this morning. I know you guys talked about fully passing through NCPs next year. I guess 2-part question. One, is that predicated on a disciplined OEM market? And then two, is there a chance that the EPA won't make its final ruling until after 2027? Any color there would be helpful.

**Jennifer Rumsey** (Executives):
So we currently anticipate that the EPA will come out with their final rule. As you are well aware, they initiated the draft rule in July, comment period closed at the end of August, and they're making their way through those comments and our understanding is we'll likely see that in December. And we anticipate that NCPs will be included in the final rule. The question and what's driving some underlying market uncertainty is, will they change the amount of those NCPs from the draft rule. 
We have been working closely with all of our OEM customers around product availability and plans, and we anticipate largely in the next year, we'll sell more of the current products, but we have a phased transition that we've announced over the course of the year, launching limited production of X10 and X15 in January and then transitioning in the third and fourth quarter to full production of the new product. And then we'll move to the new product at the beginning of '28.

**Mark Smith** (Executives):
And our comments about recovering NCPs are from our customers, right, where those apply on the older products.

**Oliver Z Jiang** (Analysts):
Understood. And then maybe just a follow-up on the supply chain constraints you mentioned. Can you just share some color on the nature of those bottlenecks? And then as they're resolved, I mean, which kind of -- which products do you see or which segments do you think should see the most benefit there?

**Mark Smith** (Executives):
Yes. We experienced -- we identified a challenge with one of our suppliers in the third quarter in Power Systems, but that's been worked on. We expect to recover most of those -- the production engine production, which then flows into distribution for installation to our customers in the fourth quarter. So that's the primary one. It is fair to say demand is tight, given the -- demand is high. And so increasing supply, investing in capacity, along with our suppliers is a key focus going forward, not just for the fourth quarter. 
But generally, I would say supply is tight, both in Power Systems and in some of the on-highway markets. But specifically for the third quarter, the impact was within Power Systems, which had a knock-on impact for distribution. And that's why you've seen such a step-up in revenue in the fourth quarter in distribution. We would have expected, let's say, about $200 million more of that revenue to incur in the third quarter that's rolled into the fourth quarter. The other part of our revenue miss in the third quarter was market-driven, which we tried to be clear, was tied to the North American pickup truck -- heavy-duty part of the pickup truck market.

**Operator** (Operator):
The next question is coming from Jerry Revich of Wells Fargo Securities.

**Jerry Revich** (Analysts):
I'm wondering if you could just talk about, within Power Systems, if you've seen any movement in the backlog given the election news and otherwise? And if you could just comment on the ability to ship production and deliver more into other regions if we do see movement in the backlog. Just would love you to comment on the broader puts and takes as you look at the production plan.

**Jennifer Rumsey** (Executives):
Yes, Jerry, sure. I understand the question. I think a lot of people have that question. And we, of course, recognize the conversation that's happening in the U.S. right now around energy use and environmental impact of data centers. Our focus remains on meeting our customers' demands. And what I can tell you is those demands continue to grow. Our order intake in the third quarter exceeded what we thought it would be. We continue to see exceptionally strong demand on our larger engine gensets with orders extending out into the second half of 2028 as well as interest in the next size down from those where we can't meet customer needs with the larger gensets. 
We have multi-year strategic conversations to plan expectations with our customers, and those remain very strong, and we have contractual commitments with some of our big hyperscaler customers that extend beyond when we have firm order board. So what I'll tell you is we continue to see strong demand. And recall that, that demand is global. We've seen significant rise in China and Asia Pacific this year in addition to the already growing demand in North America. And our investments are in existing plants and assets that have a lot of flexibility to meet various customer global needs in industrial markets as well as various power generation markets.

**Mark Smith** (Executives):
And that's one of the other advantages of having a global in-house distribution system that our global customers have that confidence of the support they're going to get wherever they operate.

**Jerry Revich** (Analysts):
Super. And can I ask you on the capacity expansion, obviously, super CapEx-efficient plan to add capacity. Can you just update us on how additional production is coming online, how that's going? And Mark, I believe if I've got the math right, fourth quarter implies potentially a step down in Power Systems margins. I want to make sure that's right. It looks like that's about 22.5%, but maybe there are moving pieces to think about.

**Jennifer Rumsey** (Executives):
So I'll talk just about the investments we're making. We're really making good progress, pleased on track with those investments, really 2 key areas, the capacity investment that we're making, and we will see -- start to see a step-up in capacity next year and then further step up most of that coming in, in the 2028 time frame that we can use for both backup power as well as prime power applications. 
And then we're also making good progress with the development of our new 130-liter natural gas engine. So you've seen announcements of selling some of our existing natural gas products in the prime power applications as well as BESS, and then we'll have some key development milestones and start to have pilot product in the market for the larger engine in 2028. So that revenue really doesn't start to come in, in a more meaningful way until 2029. But all of that is tracking to the plans that we had. And as I said, we feel we're well on track for what we committed for 2030 at our May Analyst Day.

**Mark Smith** (Executives):
Yes. And then on the margin question, yes, of course, your math is right, Jerry. I think Q4 is not going to be a forward-looking run rate. There's always a bit of natural variation when you're investing in new products, bringing on capacity, you've got a few shorter production days in the fourth quarter. So yes, the Q4 margins could be a little bit lower, but that's not the run rate going forward. There's no fundamental change in the underlying trajectory of the Power Systems profitability. It's been a great story, and we're very confident on global demand and the prospects for that business.

**Operator** (Operator):
The next question is coming from Jamie Cook of Truist Securities.

**Jamie Cook** (Analysts):
I guess my first question, just, Mark, there's a lot of debate in 2027 and 2028 with just complications around EPA 2027 and phasing in and your investments on your ability to put up the targeted 25% incremental margins that you guys talked about at your Analyst Day this year. So just trying to understand your confidence level with Cummins' ability to do that? And is it more back-end loaded? So just thoughts there. 
And then I guess just my second question, I guess what struck me about the quarter, as we miss on revenues, the margin performance, you mean, was very strong. So was there anything unusual that allowed you to put up good margins on a softer revenue base? And then the margins implied in the fourth quarter are pretty strong, too. So I'm just wondering if the back half of 2026 margins is a good way to think about a starting point for 2027.

**Mark Smith** (Executives):
Yes, so good. That's a wide range of related comments. So what I'd say is, number one, when we had our Analyst Day, best of my recollection, I tried to paint a picture across the different segments. The Power Systems and Distribution were a bit more of a continuous story that there would be part of a transition to new products on the engine business and components story. And it's possible people are misinterpreting some of the comments we've tried to make about migrating to the new products. We are making great progress on revenues. We're making great progress on margins, set aside the individual quarter nuances towards our 2030 Analyst Day. 
And any comments I've tried to make about this transition in product on the engine business, I tried to flag that early at the Analyst Day and our comments remain consistent with that. We knew we didn't have the EPA rulings when we had Analyst Day. We still don't have the final rulings now, and we're just trying to provide you with an ongoing description of what we expect to happen given more information but still incomplete information. 
So the key takeaway overall is that 2030, we're making great progress towards those targets, and we're not in any way trying to signal anything other than strong progress towards them. We'll get to the very specifics next year. There is nothing significant in the Q3 results, which is why Q4 also looks strong. I mentioned in Q2, we'd have to update our incentive compensation plan expenses, which happens every single quarter. It just stood out more because of the year-over-year comparison. 
But the trajectory of that incentive compensation is the same as I mentioned 3 months ago. The absolute expense was up year-over-year, consistent with record profitability this year. It was down sequentially because we had to true up the full year view. But in the grand scheme of things, not material. The underlying story is very strong performance. We didn't get quite out as much revenue as we'd hoped. Our expectations were similar to consensus for what we thought our revenues would be, half of it is supply chain issues, which we believe will catch up in the fourth quarter, and roughly half of it market conditions primarily related to lower pickup trucks. 
So we feel very good about the profitability and the progress. We feel very confident that we can do better as we continue to expand our revenues over the next few years. And also, as the CFO, particularly excited about generating record operating cash flow and returning that back on a disciplined basis. So I hope that is as clear as I can make it. Next year, we'll get into details -- next year. Of course, there are other complexities, but you should feel like we're entering with a very strong underlying margin base as we exit this year.

**Operator** (Operator):
The next question is coming from Kyle Menges of Citigroup.

**Kyle Menges** (Analysts):
Great. I was hoping if we could dig into Power Systems margins and maybe a framework to think about it exiting 2026 and the incrementals. I think you've talked about maybe 25% to 30% incrementals for that segment going forward and understand there's a lot of moving pieces around the capacity ramp, maybe some incremental demand for smaller products and then this battery opportunity coming in. But just any color you can provide on how to think about the incrementals in that business moving forward with all the puts and takes, seemingly.

**Mark Smith** (Executives):
I would say that all those smaller comments are exactly the same. We -- when we've taken the range by fractions of a percent, that to us, that's the same guidance. We just got 1 quarter left. So we're just tightening up the range with 2.5 months to go. But nothing's changed, stand by all of those comments. We'll give you the very specific guidance. It will be -- if you ask me today, do I expect revenues of Power Systems and Distribution next year to be higher, lower or the same than this year, they're going to be higher with what we know today. 
And we expect over time that those businesses are going to deliver more earnings. There's going to be variation in individual quarters given the balance of investment and other things, but we're very excited about the prospects of Power Systems and Distribution. We will give you very specific guidance in February when we get there. Nothing's changed. If anything, demand has gone up.

**Kyle Menges** (Analysts):
Got it. That's good to hear. And then just a follow-up on -- maybe on North America, on the highway. Curious what -- how you're thinking about any potential prebuy or pre-build of inventory in the back half of 2026 and managing through a potential air pocket in 1Q '27 in production. I'm curious how you're thinking about that.

**Jennifer Rumsey** (Executives):
Yes. Really, what we've seen this year has been, we believe, pretty limited prebuy in the U.S. truck market and actual growing underlying demand off a cyclical low. Of course, it stepped up year-over-year significantly in the third quarter. And the industry and we are managing through some supply hiccups and challenges through that. So in the fourth quarter, in Jamestown, where we build X15, we're really building at the capacity, we believe that this year is largely sold out. 
We're navigating some of our own supply challenges in components and axles in particular and really focused on trying to deliver to customers through the end of this year and into next. And so we anticipate there'll be continued underlying demand as we go into 2027. But of course, the uncertainty around where NCPs will be is causing some customers to wait. We believe the fundamentals have improved and the demand out there is real and will continue and are really just focused on trying to execute through the big step-up we've seen.

**Operator** (Operator):
The next question is coming from David Raso of Evercore ISI.

**David Raso** (Analysts):
I was curious, can you help us with your power demand today, the domestic versus international? And any color around the profitability? And if you can incorporate the China JV in that answer. Because back in the day, the geographic color was usually minority U.S., Canada for power. But just given the recent trends and there's obviously more in the business than just power. Can you help us with that mix? And obviously, any sense of the profitability domestic versus international would be interesting.

**Jennifer Rumsey** (Executives):
I'll just start with how we see the global business and demand. So we've seen really strong demand here in the U.S. and also in China and Asia Pacific. And of course, that's where you see a lot of the AI model development happening that's driving that strong demand. One of the benefits of Cummins is with our global product and manufacturing footprint and the distribution network, we can support those big customers wherever they go in the world. 
And we have projects happening around the world. In fact, I was in Spain in September and visiting a couple of our data center customers there. So they really are global, but a larger percentage of them sit in U.S., China and Asia Pacific, and the demand continues to grow. And as AI use grows in application, we think globally, we'll see growing data center demand. Mark, you can talk a little bit more about how you think about margins.

**Mark Smith** (Executives):
Yes. I think we definitely have strong margins, whether that's domestically or internationally. We're not a company that makes only margins in one particular region. It depends what the application is. If it's a data center then the -- typically the EBITDA dollars are greater than another application because we get all the extra installation in our Distribution business. But I would say there's no significant difference. 
And the order intake has been very strong in North America for quite some time. It is picking up at a faster pace outside of the U.S. such that the orders are almost on at par now between international and domestic. That's not going to be a discussion point in our earnings calls in terms of the Power Systems performance on margins. That's not going to be the principal driver. But we share some of that engine margin depending on which engines we're talking about in the genset in China, if it's made in the joint venture, and anything through our distribution, of course, is 100% Cummins' extra slice of the pie. No big variation.

**David Raso** (Analysts):
What you just said about international versus domestic on the orders? Were you talking about magnitude of growth? Or the absolute dollars now international as big as domestic?

**Mark Smith** (Executives):
I would say the absolute dollars on data centers, I'm not talking about other power gen, it's probably even bigger internationally. But on data centers, it's now reached at par across all International market.

**Jennifer Rumsey** (Executives):
U.S. versus international.

**Mark Smith** (Executives):
In which China -- Southeast Asia is the most fastest accelerating piece, and we're in a very strong position there.

**Operator** (Operator):
The next question is coming from Rob Wertheimer of Melius Research.

**Robert Wertheimer** (Analysts):
I had a couple of questions around evolving capabilities for data center. And specifically, on the battery backup announcement, how repeatable is that? Is there a big pipeline for that? And does that, in any way, intersect with your potential JV to make cells? And then just more generally, Jennifer, I think you touched on the rollout of the 130-liter. Any early indications? I don't know if you're taking indications of demand at this point? I know you're doing pilot production not this year and into '28, but how are you thinking about the commercial gathering of orders and when you start that?

**Jennifer Rumsey** (Executives):
Yes. So on the question around stationery energy storage, obviously, early days for us. We have a big announcement. What I would say is the conversations and the interest in how to bridge the grid, grid availability as well as grid and reliability continue to only strengthen, especially here in the U.S., we think there's a real demand there. And so the places that we get a lot of interest, of course, is that the stationary energy storage battery system. 
And to your question on the Amplify joint venture, that joint venture is planning to make a cell for commercial vehicle on-highway that's different than what we're using in those. So we're sourcing that cell elsewhere. And on the natural gas product, you've seen a couple of announcements that we've already made around multiyear agreements and use of some of our natural gas product. That's largely the 78-liter that we have in production today. 
So yes, there remains a lot of interest in the 130-liter, the larger version of genset that will better meet that market need. And we're not taking specific orders at this point, really just talking about customer interest and where we want to pilot and build confidence in that product. We're excited to be growing there. It's really going to be late this decade that we'll see that start to ramp up.

**Operator** (Operator):
The next question is coming from Tami Zakaria of JPMorgan.

**Tami Zakaria** (Analysts):
I wanted to ask you about the BESS contract you recently won, which seems exciting. Was this BESS opportunity embedded in your multiyear target? And if not, what kind of incremental revenue lift should we expect over that time frame that you have? And then would incremental margins on this type of revenues be similar to the enterprise target of over 25% through 2030?

**Mark Smith** (Executives):
I think that's an exciting project. Obviously, there are different forms of these projects evolving over time, but I would just say that's likely to grow, but not be the most significant factor in our Power Systems guidance. So that we're just -- by communicating that, we're just letting you know we'll continue to expand our participation in meeting the power -- flexible power needs of our customers, but it's not a fundamental change to the direction of Power Systems or changing in our outlook, which is very bullish for the top line and margin expansion going forward in aggregate.

**Tami Zakaria** (Analysts):
Got it. That's helpful. And then I wanted to ask you about the price cost dynamic in the quarter? And has it changed versus the first half of the year, especially as it relates to the engine segment?

**Mark Smith** (Executives):
I would say, generally, we're starting to see some creeping cost increases, right? Freight's gone up. There's various bottlenecks around the world or areas of conflict or shortages. I would just say, generally, there's a little bit more creeping cost. There's positive pricing for the company in total, but I would say between price, cost, tariffs in an environment where we significantly improve gross margins, that was not a significant dive. All of that washed out to a slight negative. And really, it's the volumes and the execution of our operations that's driven the margin improvement. It is more of a slight headwind on price costs in the second half for now.

**Operator** (Operator):
The next question is coming from Kristen Owen of Oppenheimer.

**Kristen Owen** (Analysts):
And forgive me if I'm asking you to repeat yourself here. But I did want to start with the updated guidance for Distribution. That midpoint assumes sequential growth 3Q to 4Q of 23%. Can you just help us unpack what supports that increase? Is that generator deliveries, installation milestones, service activity? Just a little additional color there, please.

**Mark Smith** (Executives):
Yes. It's -- the step-up is really driven by the distribution didn't receive all of the large engines expected at the end of the third quarter. And so a lot of their installation -- some of the installations were pushed into the fourth quarter. So you're right, it is an outsized number. I've tried to call that out. So it's really just catching up the slight delays in the third quarter. The full year outlook has not changed. It is not a demand issue. The demand is there.

**Jennifer Rumsey** (Executives):
And I think it's important when you think about our distribution business, there's a few things that this business does. Of course, we have aftermarket and parts and service that happens through that business. And then they're also doing projects, and they're doing a growing number of these large data center power generation projects. And broadly, we see higher margins in the aftermarket parts part of that business versus the power generation part of that business, which, of course, has been growing and very attractive, but just a way to think about that business and margin.

**Kristen Owen** (Analysts):
Great. And then my follow-up relates to the Circe order, the 2 gigawatts there in Texas. Just what milestones determine the delivery schedule there? And what needs to be in place at the customer level before that equipment shifts?

**Jennifer Rumsey** (Executives):
Yes. So those -- that order is existing products. So we're really working with them in terms of their installation plans and providing that product to them and then potential for that to continue to grow and evolve as we bring the new product into the market over time.

**Mark Smith** (Executives):
Just overall project schedule, nothing particularly unique about the delivery of that. Exciting, but not unique.

**Operator** (Operator):
At this time, I'd like to turn the floor back over to Mr. Hopkins for closing comments.

**James Hopkins** (Executives):
Thanks, Donna. I want to summarize 5 key points as we think now about 2027 and themes that we're anticipating, many of which we've discussed throughout the teleconference. Number one, we expect continued strength in power generation related to data center customers that will positively impact both Power Systems and Distribution revenue next year as we bring incremental capacity online and is consistent with our data center revenue targets for 2030. 
Number two, industry expectations are for truck production in North America to be flattish in 2027 versus 2026, supported by increased freight rates in the second half of this year and improved fleet profitability. Number three, the vast majority of our North America truck engine production next year will be on our legacy platforms. Number four, we plan to pass on NCPs to our customers. And number five, we expect another year of strong operating cash flow and returning 50% of that operating cash flow to investors as we are on track to do this year. 
We'll give more detailed guidance, as Mark mentioned, when we get to our Q4 earnings call in next February, but those are some of the key themes that we're anticipating that will drive profitable growth as we head into 2027. That concludes our teleconference for the day. I want to thank you all for participating and your continued interest as well as the Investor Relations team will be available for questions after the call.

**Operator** (Operator):
Thank you. Ladies and gentlemen, this concludes today's event. You may disconnect your lines or log off the webcast at this time, and enjoy the rest of your day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CMI_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜Jennifer Rumsey (CEO)｜guidance：全年營收財測上調至 +10%~13%（前次 8%~11%）（原話："total company revenues to increase 10% to 13% in 2026"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜guidance：全年 EBITDA 率財測中點上調至 18%~18.5%（原話："midpoint of our EBITDA guidance to a range of 18% to 18.5%."）
- 2026-08-04｜Jennifer Rumsey (CEO)｜guidance：北美重型卡車 2026 預測 24~25 萬輛（前次 23~25 萬）（原話："up from our prior guidance of 230,000 to 250,000"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜guidance：全球發電營收維持 +15%~25%，成長受產能限制（原話："growth in 2026 will continue to be constrained by capacity."）
- 2026-08-04｜Jennifer Rumsey (CEO)｜guidance：中國營收（含合資）預期約 +15%（前次 +10%）（原話："to increase approximately 15% in 2026"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜guidance：採礦引擎銷售預期下修至 -5%~+5%（前次持平~+10%）（原話："engine sales to range from down 5% to up 5% for the year"）
- 2026-08-04｜Mark Smith (CFO)｜guidance：Accelera 2026 淨損預期 2.6~2.9 億美元（前次 2.7~3.0 億）（原話："prior guide of a negative $270 million to $300 million."）
- 2026-08-04｜Mark Smith (CFO)｜guidance：年度資本支出區間（原話："range of $1.35 billion to $1.45 billion"）
- 2026-08-04｜Mark Smith (CFO)｜guidance：全年有效稅率約 23%（不含離散項）（原話："effective tax rate is expected to be approximately 23%"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜margin：Q2 EBITDA 率 17.5%，去年同期 18.4%（原話："EBITDA for the quarter was a record $1.7 billion or 17.5%"）
- 2026-08-04｜Mark Smith (CFO)｜margin：Q2 毛利率 26.1%（去年 26.4%）（原話："Gross margin for the quarter was $2.5 billion or 26.1%"）
- 2026-08-04｜Mark Smith (CFO)｜margin：Q2 關稅淨影響對 EBITDA 金額不重大（原話："The net impact of tariffs was immaterial to EBITDA dollars"）
- 2026-08-04｜Mark Smith (CFO)｜margin：獎金提列：下半年每季較 Q2 低約 2,500 萬美元（原話："a quarter lower in Q3 and Q4 than the Q2 expense."）
- 2026-08-04｜Mark Smith (CFO)｜margin：明年獎金重設至目標，規模約 2 億美元（原話："next year, it could be in the order of like $200 million."）
- 2026-08-04｜Mark Smith (CFO)｜margin：Components 分部 EBITDA 率財測區間下限不變、上限下調（原話："compared to our prior guide of 13.5% to 14.5%."）
- 2026-08-04｜Mark Smith (CFO)｜margin：Distribution 分部 EBITDA 率財測較前次中點下調（原話："range of 13.5% to 14.25% compared to our previous"）
- 2026-08-04｜Mark Smith (CFO)｜margin：Power Systems EBITDA 率財測中點較前次 25.5% 上移但含下半年投資（原話："compared to our previous guide of 25.5% at the midpoint,"）
- 2026-08-04｜Mark Smith (CFO)｜margin：Distribution 利潤率受獎金影響較大的原因之一為零件業務成長較慢（原話："the parts business isn't growing at the same rate"）
- 2026-08-04｜Mark Smith (CFO)｜margin：下半年無一次性項目、EBITDA 率預期高於上半年（原話："there's no onetime or anything"）
- 2026-08-04｜Mark Smith (CFO)｜margin：Power 增量利潤率優於預期的主因（原話："stronger demand in China, which helps on the JV earnings"）
- 2026-08-04｜Mark Smith (CFO)｜margin：保固成本目前約佔營收低 2%（原話："warranty costs are running in the low 2% of sales range"）
- 2026-08-04｜Mark Smith (CFO)｜margin：新平台上市通常伴隨較高保固提列（原話："those come with a higher warranty accrual"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜product：EPA 2027 草案下 X15 量產時程（原話："production expected to begin in the fourth quarter of 2027."）
- 2026-08-04｜Jennifer Rumsey (CEO)｜product：X10 限量生產與量產時程（原話："with full production expected by the third quarter of 2027"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜product：新一代 B 平台 2028 年 1 月上市（原話："B platform is expected to launch in January 2028"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜product：宣布開發 130 公升天然氣發電機組，切入主電力市場（原話："development of 130-liter natural gas genset"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜product：較長的限量生產過渡期是過去沒有過的（原話："is something that we've not had in the past."）
- 2026-08-04｜Jennifer Rumsey (CEO)｜commitment：與超大規模雲端客戶簽多年協議，涵蓋數 GW 備援發電機需求（原話："several gigawatts of future backup power genset demand"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜commitment：分析師日宣布新增 20 GW 產能，明年部分上線、2028 年大幅增加（原話："investment in capacity, 20 gigawatt incremental"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜commitment：產能增幅預期：2028 年為較大一步（原話："the bigger step-up happening in '28"）
- 2026-08-04｜Mark Smith (CFO)｜capital_allocation：Q2 回饋股東約營運現金流 50% 的長期承諾（原話："commitment to return approximately 50% of operating"）
- 2026-08-04｜Mark Smith (CFO)｜capital_allocation：Q2 買回與股息金額（原話："$225 million of share repurchases and $276 million in cash"）
- 2026-08-04｜Mark Smith (CFO)｜capital_allocation：董事會批准季度股息增加 10%（原話："approved a 10% increase in our quarterly cash dividend"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜customer：Q2 中國發電設備銷售 +88%，資料中心需求加速（原話："Sales of power generation equipment in China increased 88%"）
- 2026-08-04｜Mark Smith (CFO)｜customer：發電機組訂單已排到 2028 下半年（原話："it's going to be the second half of 2028."）
- 2026-08-04｜Mark Smith (CFO)｜customer：管理層稱需求無暫停（原話："absolutely no pausing or blinking in demand"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜customer：積壓訂單描述（原話："So backlog is very strong."）
- 2026-08-04｜Jennifer Rumsey (CEO)｜competition：本十年發電營收仍以柴油備援為主（原話："predominant revenue for power gen this decade"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜competition：對 NCP 與排放額度的看法：預期不會大量用額度抵 NCP（原話："there's going to be a kind of a big use of credits"）
- 2026-08-04｜Mark Smith (CFO)｜competition：Mark 稱能同時提供產品、服務與安裝的全球業者不多（原話："there are not many players in this segment"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：北美工程機械需求預期持平，理由為關稅與利率不確定（原話："given ongoing tariffs and"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：採礦：庫存偏高預期壓抑需求（原話："inventory levels and others are expected to moderate"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：中國下半年預期正常季節性放緩（原話："we expect normal seasonal moderation during the second half"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：中國挖掘機 Q2 受 OEM 備貨影響（原話："OEM inventory stocking to mitigate potential logistics risks"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：2027 年需求預期溫和回落，但不會像先前預期那麼劇烈（原話："it will not be as abrupt as we might have previously"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：2027 年不給具體財測（原話："we won't give specific guidance"）
- 2026-08-04｜Mark Smith (CFO)｜risk：研發費用因分階段轉換將維持較高更久（原話："our R&D costs will stay elevated for a little bit longer"）
- 2026-08-04｜Mark Smith (CFO)｜risk：2027 年保固與產品涵蓋成本低於全面 1/1 上市情境（原話："product coverage costs for next year would be lower than we"）
- 2026-08-04｜Mark Smith (CFO)｜risk：NCP 預期轉嫁市場（原話："we don't expect a significant financial impact from those"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：預購需求：預期持續到明年（原話："some prebuy is coming in"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：中型卡車財測納入略高的預購（原話："modestly higher prebuy following the recent regulatory"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：行業景氣描述為謹慎樂觀（原話："I would describe it as cautious optimism"）

### CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md
- 2026-05-21｜CEO｜guidance：CEO 宣布 2030 營收目標區間上調為 $45–50B（原話："revenue to be in the range of $45 billion to $50 billion"）
- 2026-05-21｜CEO｜guidance：2030 EBITDA margin 目標為超過 20%（原話："EBITDA to exceed 20%."）
- 2026-05-21｜CEO｜guidance：前次 2030 目標為 17–18% margin（逐字稿營收寫成 $43 million to $48 million）（原話："and 17% to 18% margin."）
- 2026-05-21｜CFO｜guidance：CFO：目標對應 6–9% 複合年增率（原話："translate into 6% to 9% compound"）
- 2026-05-21｜CFO｜guidance：資料中心貢獻 2–3% CAGR（原話："That delivers 2% to 3% of the compound annual growth rate"）
- 2026-05-21｜CFO｜margin：CFO：未來至少再 250bp 的 margin 改善（原話："a further at least 250 basis points of margin improvement."）
- 2026-05-21｜CFO｜margin：20% EBITDA 目標對應 25% 以上增量 margin（原話："that implies 25% plus incremental margins over time."）
- 2026-05-21｜CFO｜margin：Power Systems 與 Distribution 的 EBITDA% 預期持續改善，Engine/Components 隨新產品成熟（原話："we should see more continuous improvement in the EBITDA"）
- 2026-05-21｜CFO｜margin：公司不給各分部目標（原話："We didn't give individual segment guidance"）
- 2026-05-21｜CFO｜margin：2030 年 Power Systems 加 Distribution 約占總獲利不低於 50%（原話："you're probably not looking at less than 50% of the"）
- 2026-05-21｜CFO｜margin：2025 年 Power Systems 與 Distribution 合計占 EBITDA 60%（原話："exactly 60% of the total in 2025"）
- 2026-05-21｜CEO｜margin：2025 年營收與 EBITDA margin（原話："$33.7 billion in revenue and a record 17.4% EBITDA"）
- 2026-05-21｜CFO｜margin：兩年來 EBITDA margin 改善 250bp（原話："You've seen 250 basis points of margin"）
- 2026-05-21｜Power Systems president｜margin：Power Systems 過去數年 margin 改善逾 1,000bp（原話："driving over 1,000 basis points improvement in margin."）
- 2026-05-21｜CFO｜margin：管理層稱投資不會造成 margin 大幅下挫（原話："any big bathtub in margins"）
- 2026-05-21｜Engine president｜margin：新平台上市品質應計約 18 個月，完整 margin 效果要到 2028 後段（原話："quality accruals, and those will for sure take 18-ish"）
- 2026-05-21｜Engine president｜margin：多數產品要到 2028 後段才看到真正 EBITDA 表現（原話："you're in the late '28 before seeing where they are truly"）
- 2026-05-21｜CFO｜margin：Distribution margin 還有擴張空間（原話："excited about more margin expansion to come in Distribution"）
- 2026-05-21｜CEO｜margin：研發占營收比預期過 2027 後下降（原話："going to start to come down a little bit"）
- 2026-05-21｜CEO｜margin：Power Systems 研發投入增加（原話："some of the R&D investment in Power Systems"）
- 2026-05-21｜Distribution president｜margin：大型引擎市場競爭者少，定價有彈性空間但競爭仍強（原話："there's probably some ability to price more in that space"）
- 2026-05-21｜Distribution president｜margin：同上：定價競爭（原話："competition is tough in that space"）
- 2026-05-21｜Power Systems president｜guidance：資料中心營收由約 $5B 增至 2030 年 $9B 以上（原話："billion today to above $9 billion by 2030."）
- 2026-05-21｜Engine president｜guidance：美國 EPA 規則尚未定案，Q3/Q4 預期強於明年 Q1（原話："Q3, Q4 are going to be stronger than what Q1 will be next"）
- 2026-05-21｜Engine president｜guidance：預期明年第一季出現量的停頓（原話："pause or a lag in volume in the first quarter of next year"）
- 2026-05-21｜Engine president｜guidance：北美重型引擎日產量由約 250 升至 6 月底 400（原話："by the end of June, we'll be up to 400."）
- 2026-05-21｜Engine president｜guidance：北美重型引擎年初日產量（原話："we started the year making 250, 240 engines a day"）
- 2026-05-21｜CFO｜guidance：資本支出框架維持占營收 3–4%（原話："framework of 3% to 4% of revenue for the overall company"）
- 2026-05-21｜Power Systems president｜capital_allocation：新增 $450M 產能投資（原話："we're announcing an additional $450 million of"）
- 2026-05-21｜Power Systems president｜capital_allocation：高馬力引擎／發電機組產能 2030 年達 55GW（原話："20 gigawatts, reaching a total of 55 gigawatts by 2030."）
- 2026-05-21｜CFO｜capital_allocation：FCF：至少 50% 返還股東為起點（原話："at least 50% is the starting point"）
- 2026-05-21｜CFO｜capital_allocation：股利與回購承諾（原話："excess capital to shareholders in the form of share"）
- 2026-05-21｜CFO｜capital_allocation：已重啟股票回購（原話："we restarted our share repurchase activity"）
- 2026-05-21｜CEO｜capital_allocation：M&A：無大型項目在管線（原話："there's no big things that are really in the pipeline right"）
- 2026-05-21｜Engine president｜capital_allocation：Engine 投資高峰已過（原話："peak investment period is largely behind us"）
- 2026-05-21｜CFO｜capital_allocation：CFO：接近投資高峰（原話："we are getting to the point of peak investment"）
- 2026-05-21｜Components/Accelera president｜capital_allocation：Amplify 合資不再於該廠設產線、放慢投資（原話："put lines in that facility and slow the investment"）
- 2026-05-21｜CEO｜commitment：CEO：對 2030 承諾有能見度（原話："line of sight to what we're committing to you today"）
- 2026-05-21｜CFO｜commitment：CFO：對 6–9% 成長有高信心（原話："we have high confidence in the numbers going forward."）
- 2026-05-21｜CFO｜commitment：Accelera 方向為降低虧損（原話："loss improvement is the trend that we're aiming for"）
- 2026-05-21｜Power Systems president｜commitment：Accelera 已調降今年虧損預期（原話："we revised our guidance to lower losses even this year"）
- 2026-05-21｜Power Systems president｜commitment：不給 Accelera 2030 分部目標（原話："we aren't giving a segment-specific 2030 target for Accelera"）
- 2026-05-21｜Power Systems president｜commitment：第一台大型天然氣引擎 2028 年交付（原話："The launch of a natural gas large engine will be in '28."）
- 2026-05-21｜Power Systems president｜commitment：新產能 2027 年開始逐步貢獻（原話："You won't see big step changes"）
- 2026-05-21｜Engine president｜commitment：新 7 公升引擎 2028 年 1 月 1 日上市（原話："we're launching the 7-liter in Jan 1 2028"）
- 2026-05-21｜CEO｜commitment：prime 產品尚不接受正式訂單（原話："we're not taking firm orders"）
- 2026-05-21｜CFO｜commitment：prime 業務未來可達 $200M 的數倍（原話："We would expect multiples of $200 million"）
- 2026-05-21｜Power Systems president｜product：天然氣大型引擎最高 4MW prime power（原話："it extends up to 4 megawatts of prime power"）
- 2026-05-21｜Engine president｜product：L9 到 X10：馬力與扭力提升（原話："70 additional horsepower, 400-foot pounds of torque"）
- 2026-05-21｜Engine president｜product：X10 納入 Mack Granite（原話："We've already announced the X10 for Mack's Granite platform."）
- 2026-05-21｜Engine president｜product：EPA 2027 每台卡車成本增加約 $10,000，多在動力系統（原話："EPA 2027 could add roughly $10,000 to the cost of a truck"）
- 2026-05-21｜Power Systems president｜product：Cummins 自稱唯一整合供應商（原話："Cummins is the only integrated offering in the market"）
- 2026-05-21｜Components president｜product：Components 受法規驅動：EPA27 以某種形式必然發生（原話："EPA27 in some form is going to happen."）
- 2026-05-21｜CFO｜competition：大型引擎競爭者數量有限（原話："very limited number of players in large engines"）
- 2026-05-21｜Engine president｜competition：年產約 130 萬具引擎，為最近對手兩倍以上（原話："well over double our nearest competitor"）
- 2026-05-21｜Engine president｜competition：X10 預期帶動重型市占成長（原話："you will see market share growth in heavy-duty via the X10."）
- 2026-05-21｜Engine president｜competition：OEM 推動轉向終端用戶拉動（原話："More and more, we are increasingly pull led"）
- 2026-05-21｜CEO｜customer：PACCAR 為最大客戶（原話："PACCAR has been a partner of Cummins for 80 years"）
- 2026-05-21｜Engine president｜customer：北美活躍引擎保有量至少 220 萬具（原話："at least 2.2 million active on-highway engines"）
- 2026-05-21｜Engine president｜customer：售後需求高峰在 7–11 年（原話："peak somewhere between 7 and 11 years"）
- 2026-05-21｜Power Systems president｜customer：中國資料中心成長 84%（Q1）（原話："we delivered 84% growth in China, in our data center"）
- 2026-05-21｜Power Systems president｜customer：美國為 $9B 資料中心營收最大部分（原話："is the largest part of the 9"）
- 2026-05-21｜Power Systems president｜customer：中國資料中心恆為備用電源市場（原話："China will always be a backup"）
- 2026-05-21｜Power Systems president｜customer：目前 prime 訂單已在 backlog（原話："there are prime orders and customers in the backlog"）
- 2026-05-21｜Power Systems president｜customer：2030 年美國未滿足電力需求 20–50GW（原話："we think it's somewhere in that 20 to 50 gigawatts of"）
- 2026-05-21｜Power Systems president｜customer：目前 95% 為備用電源（原話："95% of our business today is standby"）
- 2026-05-21｜Power Systems president｜customer：prime 產品預期 2030 年底才進來（原話："you'll see the prime stuff come in towards the end of"）
- 2026-05-21｜Power Systems president｜customer：訂單能見度延伸至 2030 年後（原話："we see a pipeline of orders out beyond"）
- 2026-05-21｜CEO｜risk：零排放技術採用速度較慢（原話："we've seen slower adoption of 0 emissions technologies"）
- 2026-05-21｜Power Systems president｜risk：氫能投資縮減（原話："namely in hydrogen, where we stepped away from some"）
- 2026-05-21｜Engine president｜risk：車隊獲利困難（原話："it's difficult right now for a lot of the fleets to"）
- 2026-05-21｜Engine president｜risk：中型車排放法規草案未出，公司尚待釐清（原話："we can't get this draft rule fast enough to be quite honest"）
- 2026-05-21｜Power Systems president｜risk：採礦市場偏軟（原話："That market has been a little soft."）
- 2026-05-21｜CEO｜risk：預期 EPA 提前採購起點（原話："we originally thought it would start second half of last"）
- 2026-05-21｜CEO｜risk：全年 70 多項關稅政策（原話："more than 70 tariff policies that impacted our business"）

### 問答異常語氣（迴避／改口／保留）
- CMI_Q2_2026_Earnings_Call_20260804.md｜問：Jamie Cook 問下半年 EPS 約 $16-17 能否作為 2027 基期，以及 2027 上半年走勢｜答法：Rumsey 稱不給 2027 具體指引、僅說需求會有些回落但較平緩；Smith 說 'Too early to say'，未回答 $16-17 是否為基期
- CMI_Q2_2026_Earnings_Call_20260804.md｜問：David Raso 問明年發電產能相對今年的量｜答法：Smith 回 'punt that one until later in the year'，只說會更高，未給數字
- CMI_Q2_2026_Earnings_Call_20260804.md｜問：Angel Castillo 問新引擎定價與分階段轉換對利潤率、市占的影響｜答法：Smith 稱 'still working through all of the pricing'，未給定價或利潤率數字
- CMI_Q2_2026_Earnings_Call_20260804.md｜問：Kyle Menges 問簽新合約時定價有無實際改變｜答法：Smith 改談長期提升利潤率的意圖與市場競爭者少，未直接回答新合約定價是否變動
- CMI_Q2_2026_Earnings_Call_20260804.md｜問：Kristen Owen 指出自然需求改善與中型卡車預購上調之說法難以對齊｜答法：Rumsey 重申基本面改善為主、部分預購；分析師表示稍後場外再問，未當場釐清
- CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md｜問：Jamie Cook：後處理與電池的增量內容金額，以及 20% EBITDA「greater than」可高出多少｜答法：CEO 改談資料中心營收規模與廠房彈性，CFO 談分部節奏並重述 25% 增量 margin，兩者均未給金額或上限
- CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md｜問：Robert Wertheimer：新增 20GW 產能有多少已售出、占指引的比例｜答法：CFO 打斷，表示只談已給的營收數字；Bush 僅答訂單已排到 2028 並有 2030 後管線，未給比例
- CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md｜問：KC Parker：prime 機組售後市場相對成本的規模，並要求不要回答不知道｜答法：Bush 以使用時數與大修頻率定性說明，未給金額或比例
- CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md｜問：Michael Feniger：中型車排放法規情境與 2027 引擎 margin 爬坡｜答法：Merritt 稱等待草案，不談更多細節，表示會再回報
- CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md｜問：Tami Zakaria：天然氣引擎 2028 交付是否已有大型 prime 訂單在 backlog｜答法：Bush 答 HSK78 已有 prime 訂單；稍後 Rumsey 補充新 prime 引擎未接正式訂單，請勿每季追問訂單
- CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md｜問：David Raso：2030 年 Power Systems 與 Distribution 占獲利比例｜答法：CFO 稱難以給確切百分比，被追問後才說不低於 50%，並稱 Really a big number

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
{"date":"20260518","verdict":"衛星候選 / 觀望 — Power Systems data center super-cycle + EPA 2027 prebuy thesis 真實但估值已透支；建議等 Fwd PE 分位回 60% 區（~$580-620 區）或 NA Class 8 prebuy 真實流入 FY27 EPS 共識上修後再進場","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"數據中心 backup gen 結構性需求支撐 Power Systems 段 +15% YoY 成長 + EBITDA margin &gt; 25%","columns":{"2Y 驗證點":"FY26-FY27 Power Systems Rev &gt; $9-11B（FY25 ~$7B）；EBITDA margin 平均 ≥ 26%","5Y 驗證點":"FY30 Power Systems Rev &gt; $14B、占總 Rev ≥ 32%","10Y 驗證點":"數據中心 backup gen 市場至 $19.7B 2030 + CMI 維持 30%+ NA 高功率市佔","具體數字門檻":"2026 guidance global power generation revenues +15-25% YoY；market $8.4B 2024 → $19.7B 2030E (Grand View Research, 15.2% CAGR)","信息來源":"Grand View Research data center generator market 2030 forecast；CMI Q1 2026 earnings call","漂移觸發條件":"連 2 季 Power Systems YoY &lt; +10% 或 EBITDA margin &lt; 25% → 削弱"}},{"id":"H2","text":"EPA 2027 prebuy 驅動 NA Class 8 訂單 2026 H2 +30-50% YoY，2027 拓展為「2027 規範下 HELM 提早合規」競爭優勢","columns":{"2Y 驗證點":"2026 NA Class 8 production ≥ 320,000 units；HELM X15 量產 ramp Q3-Q4 26 上線且無 quality issue","5Y 驗證點":"FY27-FY28 even after pre-buy crash，CMI Engine 段 Rev 仍能維持 FY24 水平（受惠 HELM 市佔擴張）","10Y 驗證點":"EPA 2027 / CARB 規範執行至 2030+，CMI Engine 段每 1pp 市佔加分對應 $400M Rev 增量","具體數字門檻":"NA Class 8 訂單 Feb 26 +159% YoY 至 47,200 units；ACT Research 2026 Class 8 tractor sales forecast 140,000 units (truck-only)；X15 EPA 2027 認證 / X10 75% lower NOx","信息來源":"ACT Research Class 8 2026 forecast；Cummins HELM platform announcement 2024-02-29","漂移觸發條件":"2027 H1 月訂單 &lt; 15,000 = pull-forward 反噬已現 → 削弱；連 2 季 HELM ramp issue → 反轉"}},{"id":"H3","text":"EBITDA margin 結構性升至 17.75-18.50%（FY26 mid-point 18.1%）並 sustainable，反映 Power Systems mix shift 結構性效益","columns":{"2Y 驗證點":"FY26 EBITDA margin 達 guidance mid-point 18.1%；FY27 持續 17-18%","5Y 驗證點":"FY30 EBITDA margin &gt; 18% sustainable，含 Power Systems mix shift 持續貢獻","10Y 驗證點":"長期 EBITDA margin baseline 從歷史 13-14% 升至 17-18%（結構性 reset）","具體數字門檻":"FY26 guidance EBITDA margin 17.75-18.50%（raised from prior 17.0-18.0%）；Power Systems Q1 26 EBITDA margin 29.5% × Rev mix 24% 占整體 EBITDA &gt; 35%","信息來源":"Cummins Q1 2026 earnings release 2026-05-05；Power Systems segment EBITDA breakdown","漂移觸發條件":"連 2 季 全公司 EBITDA margin &lt; 16.5% 或 Power Systems &lt; 24% → 削弱；連 4 季 &lt; 15% 或 Power Systems &lt; 22% → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"EPA 2027 prebuy 反噬（pull-forward demand 提早結束）","columns":{"對應假設":"H2","時間尺度標記":"🔥 中期（4-6 季）","監測指標":"NA Class 8 訂單月度（ACT Research）+ CMI Engine 段季度 Rev YoY","警戒閾值":"2026 H2 月訂單 &lt; 25,000（peak 預期 ~30,000）→ 警示；2027 H1 月訂單 &lt; 15,000 → 結構性反噬，Engine 段 EBITDA margin 連 2 季 &lt; 8% 觸發減倉"}},{"id":"R2","text":"數據中心 capex pause / Power Systems 訂單 plateau","columns":{"對應假設":"H1","時間尺度標記":"🔥 中期（4-6 季）","監測指標":"Hyperscaler capex guidance（Microsoft / Google / Meta）+ Power Systems backlog 變化","警戒閾值":"連 2 季 Power Systems YoY &lt; +10% 或 EBITDA margin &lt; 25% → thesis 削弱；連 4 季 &lt; +5% → thesis 反轉，估值倍數 reset 至 17-18x"}},{"id":"R3","text":"BEV / HFC truck 滲透率突破 + ICE TAM 萎縮（結構性慢變數）","columns":{"對應假設":"H1 H2 H3","時間尺度標記":"🐢 長期（2+ 年慢變數）","監測指標":"BEV Class 8 NA 銷售滲透率（當前 &lt;2%）+ CMI Accelera ROIC + 加氫 / 充電基建擴張節奏","警戒閾值":"BEV Class 8 滲透率 &gt; 10% (3-5 年內) = 結構性威脅升級；需 ≥ 50% 機率才砍倉（避免短期新聞驚嚇）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":696.53,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
