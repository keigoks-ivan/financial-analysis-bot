你是 stock-analyst **v20 判斷 agent**，標的 SHOP（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"SHOP","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SHOP_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SHOP_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":3742,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001594805/000159480526000067/exhibit991pressreleaseq320.htm"},"note":"未取得"},{"id":"f_kpi1_non_gaap_gaap_149","label":"Non-GAAP 營業利益（新聞稿未單列，GAAP 營業利益＋調整項 149 自算）","value":717,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元（利益率約19.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿 8-K Ex.99.1；717＝568＋149 為自算，非公司揭露"},"note":"未取得"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益","value":568,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元（利益率15.2%，自算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未取得"},{"id":"f_kpi5_q4_fy2026","label":"管理層指引（Q4 FY2026）","value":"營收年增低30%段；毛利金額年增高20%段；營業費用占營收29%–30%；SBC 155百萬美元；FCF 利益率與2025Q4相當","period":"Q3 FY2026（公告於 2026-11-03）","unit":"文字區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（公告於 2026-11-03）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未取得"},{"id":"f_kpi6_gmv","label":"GMV","value":119145,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元（YoY +29%，固定匯率+30%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未取得"},{"id":"f_kpi7_mrr","label":"MRR","value":230,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未取得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-03","period":"2026-11-03","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-03"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_shop_gross_margin_pct","label":"SHOP 毛利率","value":47.49,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SHOP.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_shop_operating_margin_pct","label":"SHOP 營業利益率","value":18.07,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SHOP.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_shop_fcf_margin_pct","label":"SHOP FCF 利潤率","value":18.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SHOP.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_wix_gross_margin_pct","label":"WIX 毛利率","value":66.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WIX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_wix_operating_margin_pct","label":"WIX 營業利益率","value":-8.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WIX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_wix_fcf_margin_pct","label":"WIX FCF 利潤率","value":19.24,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WIX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amzn_gross_margin_pct","label":"AMZN 毛利率","value":51.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_operating_margin_pct","label":"AMZN 營業利益率","value":12.89,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_fcf_margin_pct","label":"AMZN FCF 利潤率","value":-6.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gddy_gross_margin_pct","label":"GDDY 毛利率","value":63.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GDDY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gddy_operating_margin_pct","label":"GDDY 營業利益率","value":26.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GDDY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_gddy_fcf_margin_pct","label":"GDDY FCF 利潤率","value":33.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GDDY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":816,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"百萬美元（FCF 利益率22%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿 8-K Ex.99.1"},"note":"未取得"},{"id":"f_kpi4_sbc_gaap","label":"SBC（含相關稅）占 GAAP 營業利益","value":25.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"%（SBC 及相關稅147；占營收約3.9%；現金流量表 SBC 140）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司新聞稿 8-K Ex.99.1；比率自算"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":148.91,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":34.87,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":42.76,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.89 → 1.89）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.41,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.45 → 2.44）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.63,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.19 → 3.17）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.89,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.44,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.17,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-0.53,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 1.9 → 1.89（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":91.36,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝3.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":3.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":13.52,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝55.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":55.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":13.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝52.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":52.7,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":78.79,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 1.89，分子＝快照價 148.91","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-4539.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 188.0、現金 4727.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1286.52,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":187037.0,"period":"2026-11-08","unit":"USD m","basis":"市值 191576.0 ＋ 淨負債 -4539.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":15314.83,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（44 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":19374.41,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（51 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":12.21,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 148.91 / W52 135.07 / W104 127.21 / W250 86.4 / W250 13週斜率 0.91%"},{"id":"f_ma_w52","label":"52 週均線","value":135.07,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":127.21,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":86.4,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.91,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 自述：電商市場高度分散，成長可能吸引新進入者或既有對手的新產品；商家也可能改選支付處理商、CMS、市集等整合或單點方案。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm","excerpt":"The growth of ecommerce may attract new entrants or new offerings from existing competitors. Additionally, some merchants may select one or more integrated or standalone offerings from other providers such as: •ecommerce software vendors; •content management systems; •payment processors; •point of sale providers;","as_of":"2026-02-11","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：對手有更長歷史、更大客群與資源，可能以更積極定價或整合競爭平台；定價決策可能導致失去市占。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm","excerpt":"Some of our larger competitors may be able to leverage a larger installed customer base and distribution network to adopt more aggressive pricing policies and offer more attractive sales terms, which could cause us to lose potential sales or to sell our solutions at lower prices.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2026 年行銷公司爬蟲報告稱 Shopify 占電商店家 42.6%（2022 年 31.8%），WooCommerce 24.6%（2022 年 32.4%）；單一非獨立來源，口徑不一。","source":"tenten.co The 2026 Ecommerce Platform Landscape","url":"https://tenten.co/shopify/ecommerce-platform-market-share-2026/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"評論稱 AI 平台（OpenAI／Google）若接管結帳，Shopify 商家關係護城河可能受挑戰；OpenAI 於 2026-03 撤下 ChatGPT Instant Checkout。","source":"fudge.ai State of Shopify AI 2026","url":"https://www.fudge.ai/blog/state-of-shopify-ai-2026/","excerpt":"OpenAI pulled ChatGPT Instant Checkout in March 2026, while Google and Shopify pushed the Universal Commerce Protocol.34 The hype gap is in trust, not capability.","as_of":"2026-06-24","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"FY2024 10-K：沒有單一商家在任一報告期間占總營收超過 5%","source":"Shopify FY2024 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480525000012/shop-20241231.htm","excerpt":"Our merchants represent a wide array of retail verticals and business sizes and no single merchant has ever represented more than five percent of our total revenues in a single reporting period.","as_of":"2025-02-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"FY2025 10-K：因商家基礎多元，應收款、貸款、商家現金墊款無特定信用風險集中","source":"Shopify FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm","excerpt":"Due to the Company’s diversified merchant base, there is no particular concentration of credit risk related to the Company’s trade and other receivables, loans receivable and merchant cash advances.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"SHOP 2026Q3 營收年增32%至37.42億美元，GMV 1191億美元；GMV年增29%，為近五季最慢；訂閱營收年增20%（前期22%）；Q4指引營收低30%段成長、毛利高20%段成長","source":"Shopify Q3 2026 press release (SEC 8-K ex99.1) / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001594805/000159480526000067/exhibit991pressreleaseq320.htm","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Bloomberg Intelligence：應用軟體市場2035年達1.8兆美元（2025起CAGR 10.7%），但AI推動定價由席位制轉向成果制，利潤率可能壓縮100–900bps","source":"Bloomberg Intelligence Agentic AI Deep Dive（搜尋摘要轉述）","url":"https://assets.bbhub.io/professional/sites/41/Bloomberg-Intelligence-Agentic-AI-Deep-Dive.pdf","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Sezzle 私人反壟斷訴訟（D. Minn. 25-cv-2395）：2026-05 法院部分駁回 Shopify 撤案動議，Sherman Act 第 2 條壟斷與意圖壟斷主張繼續審理，搭售主張無損害駁回；非責任認定。","source":"Sezzle 新聞稿轉載 / Finviz：Sezzle Provides Update on Antitrust Case Against Shopify","url":"https://finviz.com/news/353620/sezzle-provides-update-on-antitrust-case-against-shopify","excerpt":null,"as_of":"2026-05-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋未見 DOJ、FTC 或歐盟對 Shopify 的 2026 年反壟斷調查；僅有私人訴訟。","source":"WebSearch 結果彙整（SHOP DOJ OR FTC OR EU competition 2026）","url":null,"excerpt":null,"as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Sezzle 反壟斷案獲法官准許核心壟斷主張進入審理","source":"Shopifreaks","url":"https://www.shopifreaks.com/?p=17766","excerpt":"Sezzle’s antitrust case against Shopify clears first hurdle as judge advances monopolization claims over BNPL favoritism by Paul Drecksler | May 13, 2026 | Latest E-commerce News & Updates","as_of":"2026-05-13","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：Shopify 的中小商家客戶易受關稅、進出口許可與管制要求等貿易保護措施影響，進而可能衝擊 Shopify 業務（間接暴露，非自身供應鏈）","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm","excerpt":"These businesses may be particularly susceptible to changes in economic conditions, including pressure from inflation, declines in consumer spending, international trade risks and/or the imposition of trade protection measures (such as the imposition of or an increase in tariffs or import and export licensing 14 Table of Contents and control requirements)","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 提及關稅等總經因素過去已影響買家信心與消費，可能使商家倒閉或停用服務、減少平台交易量","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm","excerpt":"Economic downturns, financial market volatility or other negative macroeconomic factors such as tariffs or inflation, have in the past and may in the future impact buyer confidence and spending, and adversely impact consumer spending","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Shopify 自身受美國 OFAC 制裁及 BIS、DDTC 與加拿大出口管制法規約束（合規義務，未見具體管制事件）","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm","excerpt":"the export control laws administered by the U.S. Commerce Department’s Bureau of Industry and Security, the U.S. State Department’s Directorate of Defense Trade Controls and the Canadian Export and Import Controls Bureau","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Shopify 公開支持 de minimis 豁免，反對美國取消","source":"TechCrunch: Shopify pushes for open trade as Trump delays import exemption","url":"https://techcrunch.com/2025/02/07/shopify-pushes-for-open-trade-as-trump-delays-import-exemption","excerpt":null,"as_of":"2025-02-07","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K risk factors cite reliance on third parties for key services including cloud hosting and Shopify Payments","source":"SEC EDGAR Shopify Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm","excerpt":"on the development and maintenance of internet infrastructure by third parties, including by our cloud service provider. Such development and maintenance includes the maintenance of reliable networks with the necessary speed, data capacity and bandwidth. If one of these third parties suffers from capacity constraints, our business may be adversely affected.","as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收年增32%至約37.4億美元；Merchant Solutions 營收年增35%至29.06億美元（Payments 滲透率68%，去年同期65%）；Subscription Solutions 營收8.36億美元、年增約20%，MRR 2.30億美元（+19%）；GMV 1191億美元、+29%（定幣+30%），低於分析師約1200億預期。Q4 指引營收年增低30%區間。","source":"SEC 8-K Q3 2026 press release; sec-api.io Q3 2026 analysis","url":"https://www.sec.gov/Archives/edgar/data/0001594805/000159480526000067/exhibit991pressreleaseq320.htm","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Shopify 自揭美國電商市佔「大於14%」（Census 與內部 GMV 估計）；平台使用率口徑約29-30%（第三方部落格，口徑不同）。RBC 2026-04-21 維持 Outperform，指美國電商成長數據顯示持續搶佔份額。","source":"RBC Capital via Yahoo Finance; Shopify statistics aggregators","url":"https://finance.yahoo.com/markets/stocks/articles/shopify-shop-continue-growing-ahead-160330913.html","excerpt":null,"as_of":"2026-04-21","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"定價：追蹤站稱2026-10-15年繳 Grow 由$79升至$89、Advanced 由$299升至$359，10-16 回復；10-22/23 比對無牌價上調。無持續性漲價。","source":"PricingSaaS Shopify pricing tracker","url":"https://pricingsaas.com/companies/shopify","excerpt":null,"as_of":"2026-10-23","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"全球電商需求：二手彙整引 EMARKETER，2026約6.88兆美元(+7.2%)、2027約7.375兆(+7.2%)；各來源2027區間約7.1–8.0兆。非一手頁面。","source":"fungies.io / affmaven 等彙整引 EMARKETER (2025-02預測)","url":"https://fungies.io/ecommerce-statistics/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 GMV/Merchant Solutions 數字","source":"ppc.land","url":"https://ppc.land/shopify-revenue-gains-32-to-3-7bn-as-ai-referred-orders-rise-3-3x/","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Shopify 10-K 列示可能的替代/競爭方案（電商軟體、CMS、支付、POS、市集等），並稱正以 Sidekick 與 Agentic Storefronts（跨 AI 平台的代理式商品發現與結帳）納入新興 AI 技術。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm","excerpt":"Shopify provides a suite of AI-enabled features integrated across the Shopify platform, including Sidekick, our AI-enabled commerce assistant, and Agentic Storefronts, which enables agent-assisted product discovery and checkout across a number of AI platforms.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：大型科技平台可能整合競爭功能或限制第三方存取其用戶資料，影響商家行銷與銷售及平台需求。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm","excerpt":"large technology platforms have imposed and are considering imposing, or may provide their users the ability to impose, restrictions on the ability of other parties to access or use data from their customers and users.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Baillie Gifford 評論：AI 代理接手搜尋比較購買時，靠發現與客戶旅程變現的平台面臨被顛覆風險，對他者則是機會。","source":"Baillie Gifford Monthly commentary 2026 Q1","url":"https://www.bailliegifford.com/en/uk/intermediaries/insights/ic-article/2026-q1-global-alpha-insights-agentic-commerce-10061584/","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FY2025 10-K 揭露 Shopify 定位為多通路商務平台，銷售通路含線上店、實體零售、AI 平台、社群；營收由訂閱方案與商家成功型（merchant solutions）兩部分構成","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm","excerpt":"Shopify offers them the tools to seamlessly manage, market and sell their products across various sales channels, including online storefronts, physical retail spaces, AI platforms, social media and more.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K MD&A 將「提供更多銷售通路」及運用 AI 等新技術列為未來成功要素","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm","excerpt":"offer more sales channels that connect merchants with potential customers; develop new solutions to extend our platform’s functionality and catalyze merchants’ sales growth; leverage emerging technologies, including AI;","as_of":"2026-02-11","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Shopify 2026-03-24 讓美國商家可透過 ChatGPT 等 AI 通路銷售（Agentic Storefronts）","source":"roic.ai news","url":"https://www.roic.ai/news/shopify-expands-ai-commerce-reach-enabling-millions-of-merchants-to-sell-via-chatgpt-03-24-2026","excerpt":null,"as_of":"2026-03-24","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Shopify 總裁稱 AI 購物不會繞過 Shopify 結帳","source":"Retail Brew","url":"https://www.retailbrew.com/stories/2026/02/23/shopify-says-ai-shopping-will-not-bypass-its-checkout","excerpt":null,"as_of":"2026-02-23","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#4","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q3 2026 訂閱營收 836M（約+20%），merchant solutions 2.91B（+35%），Payments 滲透率 68%","source":"Shopify 8-K Q3 2026 press release","url":"https://www.sec.gov/Archives/edgar/data/0001594805/000159480526000067/exhibit991pressreleaseq320.htm","excerpt":"Subscription solutions 836 699 Merchant solutions 2,906 2,145 3,742 2,844 Cost of revenues Subscription solutions 175 128 Merchant solutions 1,786 1,325","as_of":"2026-11-03","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026 公司 8/5 guidance 營收 $3.73B–$3.78B；Benzinga 財報前共識營收 $3.74B、非 GAAP EPS $0.43（他源 $0.44）；有報導稱實際營收 $3.74B（+32% YoY）、調整後 EPS $0.49 對共識 $0.47，僅單一二手來源，未核對公司原始公告","source":"Benzinga earnings forecasts; Grafa 'Shopify Q3 2026 revenue rises 32 percent, earnings beat'","url":"https://grafa.com/en/news/united-states/shopify-q3-2026-revenue-rises-32-percent-earnings-beat","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價分布：Fintel 2026-08-27 平均 $174.57、最高 $231；MarketBeat 共識 $157.58（45 位，高 $200、低 $120）；10 月 Citi $196→$216（10/28）、Oppenheimer $205（10/23）、RBC $200、Baird $190、Cantor $158（中立）；一源稱 51 位分析師中 38 位 Buy/Outperform。各源 as-of 不一","source":"Fintel; MarketBeat price-target page; TIKR","url":"https://www.marketbeat.com/stocks/NASDAQ/SHOP/price-target/","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"聚合站列出 Shopify 於 2026-09-29 買下 Shop.com 網域（Market America 出售），價格未揭露；未見大型併購。","source":"Autobound 聚合頁（引 thedomains.com）","url":"https://www.autobound.ai/companies/shopify/acquisitions","excerpt":null,"as_of":"2026-09-29","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"加州聯邦法官駁回 Shopify 對 Briskin v. Shopify（結帳頁蒐集個資的消費者集體訴訟）的駁回動議，案件續行。","source":"Top Class Actions，Shopify class action lawsuit survives motion to dismiss","url":"https://topclassactions.com/lawsuit-settlements/lawsuit-news/shopify-class-action-lawsuit-survives-motion-to-dismiss/","excerpt":null,"as_of":"2026-08-17","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 9 份 8-K 中無 Item 4.02（財報不可信賴／重編）；重大項目 3 份為股東會相關 8.01／5.07 與 5.02 等。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001594805&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"聚合站列出 Shopify 於 2026-09-29 買下 Shop.com 網域，價格未揭露；另有未證實的 Tailwind Labs 收購說法（無日期）。","source":"Autobound 聚合頁","url":"https://www.autobound.ai/companies/shopify/acquisitions","excerpt":null,"as_of":"2026-09-29","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Briskin v. Shopify（N.D. Cal., 21-cv-06269）隱私集體訴訟經駁回動議後續行；未查到 2026 年證券詐欺集體訴訟。","source":"Top Class Actions","url":"https://topclassactions.com/lawsuit-settlements/lawsuit-news/shopify-class-action-lawsuit-survives-motion-to-dismiss/","excerpt":null,"as_of":"2026-08-17","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"FY2025 10-K 風險因素稱 CIPA／CCPA 允許集體訴訟，且訴訟數量與重要性隨規模增加。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm","excerpt":"The number and significance of legal disputes have increased as we have grown larger, as our business has expanded in scope and geographic reach, and as our platform and solutions have increased in complexity, and we expect we will continue to face additional legal disputes.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單無 Item 4.02；搜尋未見 SEC 調查或重編報導。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001594805&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"SHOP","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":47.49,"operating_margin_pct":18.07,"fcf_margin_pct":18.08,"rd_intensity_pct":12.49},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SHOP","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"WIX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":66.64,"operating_margin_pct":-8.5,"fcf_margin_pct":19.24,"rd_intensity_pct":34.55},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WIX","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"BIGC","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BIGC"},"note":"quarterly_income_stmt 無資料"},{"name":"AMZN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":51.08,"operating_margin_pct":12.89,"fcf_margin_pct":-6.38,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"GDDY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":63.75,"operating_margin_pct":26.05,"fcf_margin_pct":33.66,"rd_intensity_pct":16.34},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GDDY","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"SHOP"},"financial_history":{"ticker":"SHOP","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":5600000000.0,"revenue_yoy_pct":null,"gross_margin_pct":49.18,"operating_margin_pct":-12.27,"net_income":-3460000000.0,"diluted_eps":-2.73,"free_cash_flow":-186000000.0,"fcf_margin_pct":-3.32,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":7060000000.0,"revenue_yoy_pct":26.07,"gross_margin_pct":49.79,"operating_margin_pct":1.05,"net_income":132000000.0,"diluted_eps":0.1,"free_cash_flow":905000000.0,"fcf_margin_pct":12.82,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":8880000000.0,"revenue_yoy_pct":25.78,"gross_margin_pct":50.36,"operating_margin_pct":14.66,"net_income":2019000000.0,"diluted_eps":1.559579,"free_cash_flow":1597000000.0,"fcf_margin_pct":17.98,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":11556000000.0,"revenue_yoy_pct":30.14,"gross_margin_pct":48.07,"operating_margin_pct":16.31,"net_income":1231000000.0,"diluted_eps":0.944088,"free_cash_flow":2007000000.0,"fcf_margin_pct":17.37,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/SHOP/SHOP_Q3_2026_Earnings_Call_20261103.md）

# Q3 2026 Earnings Call
**Shopify Inc.** | Earnings Calls | 2026-11-03

**Shane Kleinstein** (Executives):
Good morning, and thank you for joining Shopify's Third Quarter 2026 Conference Call. I'm Shane Kleinstein, Director of Investor Relations. And joining us today are Harley Finkelstein, Shopify's President; and Jeff Hoffmeister, our CFO. After their prepared remarks, we will open it up for your questions. Today's call will include certain forward-looking statements that are based on assumptions and therefore, subject to risks and uncertainties that could cause actual results to differ materially from those projected. Undue reliance should not be placed on these forward-looking statements. We undertake no obligation to update or revise these statements, except as required by law. You can read about these assumptions, risks and uncertainties in our press release this morning as well as in our filings with U.S. and Canadian regulators.
We will also speak to adjusted financial measures and other non-GAAP measures, which are not a substitute for GAAP financial measures. Reconciliations between the 2 are provided in our press release. And finally, we're reporting U.S. dollars so all amounts discussed today are in U.S. dollars unless otherwise noted. And with that, I'll turn the call over to Harley.

**Harley Finkelstein** (Executives):
Good morning, everyone. And as always, thank you for joining this call. It has been an incredible quarter for commerce. The velocity of development we are seeing across the entire industry is nothing short of remarkable. From the adoption of personal agents to the start of delegated purchasing to new tools that help entrepreneurs turn any idea into a business overnight. We've seen an avalanche of new interfaces, but it's all powered by the same load bearing commerce operating system, and that is Shopify. I'll get into the numbers shortly, but I want to take a moment at the top of the call to really land the significance of all of this and why it matters so much for merchants.
Imagine for a moment that you are a retail business owner in 2026. Here are just a few things that might be on your mind today. How is your online store performing? Is ChatGPT servicing your products correctly? How can you drive up conversion in your physical retail stores? Is it time to start thinking about expanding into new markets. Now don't get me wrong, these are all very good problems to have. This is truly the greatest time in history to be a founder. There is opportunity everywhere. And the more opportunity there is, the more complexity there is. And the more complexity there is, the more our value goes up.
The value of one unified commerce operating system connected to every surface area that customers want to shop on and every tool that teams want to build with. That is the real story behind this moment. For Shopify, that is what matters most. As the world is finding its feet in this new era, there is simply no better place to be than where we are, and that is everywhere. Okay. Let's talk about the numbers. Q3 was another signature Shopify quarter. GMV was up 29.5% to $119 billion. Revenue was up 32% to $3.7 billion, and our free cash flow margin was 22%. And we saw more of the biggest names in retail from Balmain to MAC to Clinique to Lululemon all go live on Shopify. So we delivered exactly what we said we would, consistent, durable growth yet again.
But the real story is hiding in between the numbers, and it is this. Shopify is uncommonly good at operating in 2 realities at the same time. The agentic future we're building towards and that everyone on this call is excited about and the current reality for most of our merchants today. And here's what that looks like in practice. Since our last earnings call, personal agents hit the mainstream, Muse, Instinct, Claude Duet, Grok Bot, all partner with Shopify. So our merchants checkouts are supported and buyers can use Shop Pay as their wallet. And we're powering product discovery across all major AI channels from ChatGPT to Microsoft to Muse. These are the things that could drive real merchant success in the future.
At the same time, we also rolled out an incredible range of new products and features across Shopify, growing our presence internationally, strengthening our offline business and making our online store builder even more powerful. Those are the things that drive merchant success today. And importantly, we balance both of these realities while running an exceptionally strong business. 32% revenue growth, 22% free cash flow margin at our scale. That is not common. And yet I get to repeat numbers like this every quarter. So I mentioned merchant success in the future and merchant success today.
Let's start by talking about the future first, specifically, agentic shopping. Now while the volume is still small here, adoption is growing and the early signals show this is the potential to become a very powerful surface area. Here's what we're seeing. AI traffic is up 2.6x year-over-year. Orders are growing even faster at 3.3x, AI channels are sending shoppers straight to product pages at 3x the rate of organic search and shoppers are converting 64% more often.
So the numbers are certainly encouraging. But what's even more interesting is what products are being surfaced and it's not the obvious categories. AI channels are surfacing highly specific products that fit specific customers with a specific need. Here is where Shopify Catalog comes in. Catalog powered searches are converting at 2x the rate of general AI search. That is because catalog is quite literally written for agents. It turns over 1 billion product pages into structured data set translating details like size, color and material into numerical values that an agent can read and understand. And it is not just a linear product feed, it is live, cross-merchant map for what is available across all of Shopify, with current pricing and inventory that helps AI channels make more accurate recommendations and that makes it insanely powerful.
And here's what is really exciting. AI is no longer just Discovery channel. As I mentioned earlier, Q3 was the first time we saw shoppers experimenting with delegated purchasing through personal agents who can also act on behalf of their users with their permission. And in order to do that, they must earn their trust, does it know what I like. Will it get my size right? Can I trust it with my personal information. For Muse, Instinct, Claude Duet and Grok Bot, the answer is yes. Thanks to Shop.  
Through your shop account, the agent knows your preferences and shopping history. Through the Shop app, you can track all your orders placed by your agent listed right next to your other orders. And with Shop Pay as your wallet, your payment details are already saved. You stay in control of your purchases and your agent never sees your card details. And with Claude Duet, Instinct and Grok Bot that reach even extends beyond stores built on Shopify. Shoppers can now use Shop Pay as their chosen wallet for any merchant, no extra setup required, it just works.
For merchants, this means reach, a huge new pool of customers with 0 lift for them. For buyers, this means trust, a familiar way to buy in an unfamiliar channel. And for developers and AI companies, this means access to world-class infrastructure. Now all the tools they need to build a shopping experience, including catalog, checkout and the shop network are in 1 place. We call it shop.dev, one-stop all commerce complexity handled.
Okay, switching gears. Now let's talk about how we're helping merchants to build and operate more effectively with AI. As we predicted in previous quarters, commerce is fragmenting. AI is not just creating new ways for buyers to shop, it is also creating new ways for merchants to operate. And that is what Shopify was built for. We have always been an open ecosystem, and that now extends to agentic tools. We have connectors with agents like Muse, ChatGPT, Claude, Google Gemini, giving merchants complete optionality over how and where they run their business. Now this doesn't just give our current merchants optionality, it is also becoming an on-ramp for new merchants.
Imagine an aspiring entrepreneur talking to ChatGPT or Claude or Muse about starting a retail business. The agents suggest they start building with Shopify. And then it helps them build their store inside the chat. And once they're ready to start selling, they sign up for Shopify account. Agents can effectively become ambassadors for Shopify connecting new entrepreneurs to the platform at precisely the right moment. Now of course, this is still a small source of new merchants today relative to our scale.
But as more people use more tools to turn ideas into businesses, Shopify is part of that journey right from the start. Now talking about turning ideas into businesses. This quarter, we launched the biggest update to our online store builder in our 20-year history. It's called Canvas. Canvas lets merchants build a fully bespoke online store simply by describing what they want to Sidekick, no coding or design expertise required. Now the store you can picture is the store you can build. It's only been live for about a month, but here is what we are seeing.
Merchants are launching stores that are more personalized and they're doing it 20% faster. Anecdotally, this has been one of the most exciting things for me to watch rollout in a while. I ask merchants to tag me on X with what they built using Canvas. And the quality and the sheer variety has been truly remarkable from handmade pottery, to pet treats to band merch to vintage comic books. This is the Shopify that Tobi and I imagined almost 2 decades ago. Anyone selling anything from anywhere gets their own beautiful functional home on the Internet.
Now I want to talk a bit more about Sidekick, which is still overwhelmingly the most widely used tool for our merchants to run their business. And usage continues to grow at an even faster clip in Q3. Daily active merchants are up 3.7x year-over-year and daily sessions are up 4.2x, but there's an even more important story here than adoption. And it is just how capable Sidekick is becoming. In Q3, Sidekick created around 2/3 of all Shopify flows. Now remember, flows are those automations merchants used to take repetitive tasks off their plates. And here's how that shows up in practice.
I recently met a large furniture retailer who has built custom Sidekick flows for everything from warehouse inventory snapshots to delivery fee analysis to regional pricing checks. This is what makes Sidekick so powerful. It can be completely tailored to power a merchant's particular business. And now these flows extend beyond the admin into supported apps that merchants use to run their business. Sidekick is the only AI tool that can connect to them without the merchant having to set up manual integrations. We want merchants getting the benefits of AI, not spending their time figuring out how to get those benefits. This is what makes Sidekick truly feel like an extension of their team.
So there are obviously a lot of tools in the market. And there's a lot of noise about which ones will come up on top. But here's what really matters. Shopify's critical advantage is that we do not have to choose because all of them connect back to our platform. And that is what makes our incredible growth durable in the long term. Now I want to bring us right back to what merchants are focused on today. I recently hosted a forum for some of our largest and most active merchants alongside some of Shopify's leadership team. And guess what? The merchants did not spend much time talking about personal agents or even AI-powered discovery or even delegating purchasing. They talked about the fundamentals, trust, growth and simplicity, and we never lose sight of that.
Let's first talk about how we're building trust. I mentioned earlier that Shop Pay is bringing trust to an unfamiliar surface with agentic shopping. That trust is built on 20 years of commerce experience. And it is also why we continue to see incredible brands bringing Shop Pay into their ecosystem, including one of my favorite brands, as I mentioned earlier, Lululemon, who just selected Shop Pay for their North American online store. And as history has proven, once we have a toe in the door, the upside is clear.
More broadly, in Q3, GMV accelerated with Shop Pay grew over 50% year-over-year. Both the number of buyers and the number of purchases per buyer keeps growing with Shop Pay, and Shop Pay installments expanded beyond the U.S., Canada and the U.K. into Australia. Now trust also comes from the work we do in enhancing fraud detection. It is not sexy, but it is the stuff that really matters to merchants. We drawn signals across millions of businesses to help merchants spot risks. And in Q3, we added tools to automatically cancel high-risk orders even before checkout and explain why an order looks suspicious, helping merchants protect their inventory and their revenue.
And of course, trust comes from the connected shopping experience that Shop has become known for. So whether you're shopping on a merchant's website, the Shop app or the newly announced shop.com your preferences, your payment and shipping information and even carts and viewed items all come together to make the shopping experience feel seamless and personalized. Now speaking of Shop, GMV in Q3 more than doubled year-on-year. This is shops network effect at play, more shop buyers, more seamless shopping experiences, more benefits for merchants. And we continue to invest to make the experience even better. The second thing I mentioned that our merchants really care about is growth. These merchants are growing across channels. And as they grow, so do we.
Let's start with our off-line business. we hit a key milestone crossing $200 billion in lifetime offline GMV this quarter. In this past quarter alone, Canada Goose, The Body Shop, BevMo!, all launch retail locations powered by Shopify. SKIMS launched its first international flagship in London with us. And MAC Cosmetics launched 84 locations, just 120 days after signing with us. That is remarkable speed. And in Q3, we made real progress on one of the oldest problems for physical retailers, not knowing their customers. We're changing that.
Now when a customer taps their card in a Shopify powered store and opts in to receive a digital receipt, a customer profile has been created, so the merchant has a record of the shopper and their purchase history. They can get to know them, understand what they like and they can even reach out to eligible customers to bring them back and the payoff is real. In fact, a known in-store customer has a meaningfully higher lifetime value than an unknown one. This is Shopify turning point of sale from a sales channel into a growth engine, and that is a very powerful advantage for merchants. Now let's talk about growth internationally. Our goal there is simple, to make global and cross-border selling possible, simple and localized. And the impact is clear.
International GMV grew 32% in the quarter. And the work here continues. In Q3, we launched mobile-first solutions like sign-in with WhatsApp and WhatsApp marketing and messaging, which will be huge unlocks globally. We also launched a localized version of the Shop app in Japan, which became the #1 shopping app in the Japan app store, the week after full rollout, which I think is really cool. And we launched new payment offerings globally that reflect important global nuances like the rollout of OXXO as another local payment method across Mexico allowing shoppers to place an order online and pay for it in cash at an OXXO convenience store. There'll be a lot more of this to come in 2027.
The last point I'll make on growth is about discovery. As I talked about at the top of the call, shopping is spreading across more channels, more opportunity, more complexity, more ways for Shopify to help our merchants. Shopify Campaigns offers a risk-free way to reach customers across 10 channels from shop to Instagram to ChatGPT. That means full optionality for merchants. We're not biased towards any 1 particular channel and they only pay when a sale happens. And the momentum there is really building. Year-to-date orders through Shop Campaigns more than doubled year-over-year, accelerating in the third quarter. That means more merchants getting discovered without needing to become advertising experts. It also means more traffic coming to the Shop app.
Finally, I said our merchants really care about simplicity. And whether you're looking at the present reality of most merchants or the direction of travel we're heading in, in both cases, one thing becomes very clear. Our simple connected unifying operating system is the moat. No one merchant can manage the increasing volume of surface areas to build and sell across and nor should they. And that is true for merchants of all sizes, including larger merchants.
These businesses want their online stores and their physical locations to work together. They want their team spending more time improving the customer experience and less time maintaining the technology behind it. And as AI creates new ways to shop, they want a platform that keeps them ready for what comes next. And that is why we continue to see large merchants join and scale across the platform like Balmain, Givenchy, Jacquemus, Chaumet and Acne Studios, these iconic names in luxury retail that all chose Shopify in Q3 or Alice + Olivia, who scaled from a single founder to a globally recognized fashion label and who just decided to fully replatform onto Shopify after starting with Shop Pay and seeing it become their most used payment method or Omaha Steaks. I love the story.
This is a 109-year old company that was running on a custom stack built by their own CEO. They wanted a platform that can keep up with the pace of technology and allow them to focus on their business. So of course, Omaha Steaks is coming to us as well. Okay. I'll end on this note. There is a very special energy inside of Shopify right now. Tobi talks about it openly. We're giving people the tools and the room to tinker to try an idea to turn it into something useful for merchants. AI is changing what our teams can build and how quickly they can get an idea into someone's hands.
Small teams can try more things, learn from what works and build again. That makes taste and judgment even more valuable, seeing a problem we're solving, knowing what a great solution looks like and then having the curiosity to go after it. And that mindset extends well beyond engineering. All across Shopify, our team is rethinking how they work and what they can accomplish with these amazing tools. Tobi put it this way in a recent note. The early answer to how we make commerce common turned out to be simple, just build great products for them. This is what we continue to do every damn day.
And with that, I'll turn the call over to Jeff.

**Jeff Hoffmeister** (Executives):
Thanks, Harley. Q3 was another quarter of strong, consistent execution. Before turning to the results, I'm going to step back and provide some perspectives on our addressable market as we've not discussed that in a while, and I believe that agentic commerce will expand our market. Commerce continues to grow globally. But in addition to that, there are 2 important things to keep in mind regarding Shopify's role and our future opportunity. First, we continue to power a larger share of commerce overall. And second, we are expanding commerce itself by helping more merchants survive and thrive, helping them discover new buyers and lowering barriers to entrepreneurship.
To my first point, the quality and capabilities of our solutions help our merchants drive a disproportionate share of global commerce growth. Over the last 3 years, our U.S. merchants online sales grew at a compound annual growth rate of 23% compared to 8% for U.S. e-commerce overall. In Europe, we saw a similar pattern. Our merchants grew online GMV at a compound annual growth rate of 37% compared to a market growth of 8%, doubling their share of e-commerce in just 3 years. And these trends have accelerated.
Three years ago, Shopify merchants drove nearly 1/5 of incremental e-commerce sales in the U.S. and nearly 1/4 in Europe. Since the start of 2025, they now capture nearly half in the U.S. and more than 40% in Europe. To illustrate the platform scale today, in the third quarter alone, our merchants sold over $119 billion through Shopify, almost as much as they sold in all of 2020, the year everything went online due to COVID. An entire year of Shopify GMV has now become a single quarter and not even the holiday shopping quarter.
And to my second point, measuring our opportunity against the market potential that exists today, this is a critical component. Our products do more than help merchants compete for existing commerce. We help create newcomers. AI is an accelerant for our market, simultaneously making entrepreneurship easier to try, but also raising the stakes for what success requires. In that context, Shopify is a merchant's not-so-secret weapon. We make the complex simple so that our merchants can focus on what matters, building strong businesses. We have always and will continue to change the economics of entrepreneurship.
When your niche passion products can more easily find the customers are meant for, you're more likely to build that business. Smaller niche markets are now not only addressable. They're not so small anymore. With Shopify Catalog and how it is optimized for LLMs, more long-tail merchants succeed by matching buyers specific needs, however unique with our merchants tailored solutions extending the long tail of commerce is helping create new commerce. In Q3, 3/4 of AI referred sales yet again came from product categories outside our top 100. And as entrepreneurship has become more accessible, that access has manifested inside our platform.
Since 2018, the number of first-time sellers on Shopify has increased 7 times. Moreover, we help new entrepreneurs reach that milestone faster than ever before. Last year, compared to just 3 years ago, 43% more stores made their first sale within a single day of signing up. We're not just finding high intent entrepreneurs. We're bending the curve for how quickly they reach early success. AI, and the AI products that we build are a rising tide lifting all boats. And we saw that wave coming a long time ago. It's why we started building catalog 3 years ago before agentic was ever in the lexicon of commerce to make our merchants product data reachable across all AI channels with high fidelity and high consistency.
It's why we co-led the creation of the universal commerce protocol because we knew that in order for our merchants to take advantage of the opportunities inside agentic commerce, agentic commerce needed a shared language across the Internet. It's also why we're actively driving other standards like the personal agent protocol, alongside other technology and retail partners and why we have embedded Shopify into personal agents like Instinct, Muse and more. We also recently released Shop.dev and the SHOP MCP, giving developers one easy connection to add Shopify's AI tooling, sign-ins and check out into their apps or agents.
We are embedding commerce across more channels and more surfaces. Our growing buyer network extends this leadership. With Shop Pay, customers can explore new merchants through new channels while maintaining the safety of the wallet, they already know and trust and businesses of all sizes benefit from the complex commerce ecosystem Shopify has built at scale. You may have seen our latest Editions themes was exponential. Apt when you reflect on the compounding return of our massive network of both merchants and buyers. These examples are all different expressions of the same underlying business model. We build more of what merchants need, expand what they can accomplish with Shopify and participate in their success alongside them.
Wherever commerce happens, however, complex it becomes, we will continue to be the force behind it. Ultimately, the thesis is simple. To believe in Shopify, you really just need to believe in commerce. Now let's take a closer look at our third quarter results. Q3 GMV was $119 billion up 30% in constant currency, our sixth consecutive quarter at these levels of growth. The trends across all vantage points are very consistent with recent quarters. Growth was broad-based across merchant sizes and geographies and remained evenly split among new and same-store sales, starting with merchant size. The $2 million to $25 million cohort contributed the most incremental GMV and is the largest slice.
Growth in this band was mostly from existing shops growing into the size. The $25 million and greater band is the fastest growing, albeit off of a smaller base. North America continues to deliver strong growth at scale with GMV growing 28% in constant currency for the third consecutive quarter. GMV in Europe grew 33% in constant currency, aided by our continued addition of local payment offerings across several markets. Similarly, we continue to build our presence in Asia and Latin America with more tailored local offerings like those Harley mentioned. We also launched local currency billing in 10 new countries over the past few months. Merchants in these markets can now pay for their Shopify subscription in their local currency, making it easier for merchants to get started on our platform.
Finally, looking by channel, beyond just online. Off-line GMV grew 30% year-over-year, consistent with last quarter's constant currency growth. Large, complex multi-location merchants continue to be our fastest-growing segment with our total locations on Shopify up 52% year-over-year. Importantly, we are having greater success expanding our point-of-sale merchant base beyond just those merchants that started with us online and then adopted our off-line solutions. In Q3, 55% of merchants that added our point-of-sale were new to Shopify. And of those already selling, half are selling only in-store. B2B GMV grew 74%. We consider B2B a significant opportunity to expand the verticals that Shopify addresses. Interestingly, B2B GMV is much more distributed by industry vertical than online, and the fastest-growing verticals include home improvement and hardware, electronics and business supplies for verticals such as retail stores, laboratories and medical, food service and agriculture. These are categories that take us beyond our most prevalent online categories.
Turning to revenue. Q3 revenue grew 32%, both reported and in constant currency, delivering on the expectations we laid out and accelerating on top of last year's strong 31% constant currency growth rate. Merchant Solutions revenue grew 35%, driven substantially by the strength in GMV and increased payments penetration. Our FX revenue contributed nicely this quarter again, commensurate with our increasing international scale and has consistently been a source of growth within payments. Payments penetration surpassed 68%, up 3 points year-over-year, and Shop Pay GMV grew 50% year-over-year. We also saw growth in the broader set of services merchants use on Shopify, most notably this quarter in advertising.
Subscription Solutions revenue grew 20% led by standard plan subscriptions. Equivalent size increases in Plus subscriptions and variable platform fees rounded out the growth in subscription solutions with the variable platform fees growth balance between more merchants exceeding their minimum volume thresholds and continued sales growth among merchants already above them. Q3 MRR grew 19% year-over-year. Plus MRR represented 34% of MRR, growing 18% year-over-year. As a reminder, MRR comparatively underrepresents the impact we're seeing from larger GMV merchants.
Turning to profitability. Gross profit grew 28%, in line with our guidance and gross margins came in at 47.6%, consistent with the second quarter. Merchant Solutions gross profit grew 37% with gross margins expanding year-over-year for the third consecutive quarter. Our year-over-year and sequential margin improvements were driven by margin expansion in Shopify payments from savings negotiated with partners across the full payments ecosystem. We also saw a margin uplift from increased FX activity in our advertising products. Subscription Solutions gross profit grew 16%. Gross margins were 79%. 
On a year-over-year basis, Subscription Solutions gross margins compressed primarily from incremental AI spend on Sidekick, partially offset by efficiencies and support. On a sequential basis, our margin declined mainly due to higher hosting costs as we added capacity ahead of BFCM and some enhancements to our storefront resiliency and global search capabilities. Although Sidekick drove year-over-year pressure on margins, on a sequential basis, we've been able to offset that pressure with efficiencies we've built into how we deliver Sidekick. We've made improvements in model selection, distillation and caching to support more usage at a lower cost.
From Q2 to Q3, merchant conversations increased 14% while cost per conversation declined 28%, and total Sidekick cost fell 18%. The cost is only one part of the Sidekick story. The more important measure is what merchants accomplish with it. That is our focus. But that, of course, also translates into our financials. Sidekick attracts more merchants to Shopify, which manifests in the financials and subscription solutions, and it propels more merchant success, which materializes in merchant solutions.
Last quarter, we shared that using Sidekick's onboarding guide results in an 8% lift in merchants reaching 5 sales within 15 days. This quarter, we can demonstrate benefits beyond that. After their first sales, Sidekick offers merchants a dynamic conversion guide to prompt additional conversion tactics in those critical early months as a business is launching. Examples include help with answering customers' questions reaching out to customers with abandoned carts and more. This resulted in a 3% lift in merchants reaching their next 5 orders in 60 days after using the guide, incrementally small, but off large cohorts. That benefit makes a difference and shows the value Sidekick can bring in targeted, proactive merchant communication.
Our gross margins in the third quarter reflect our deliberate work. We maintain discipline in the quality of our spend and discipline in the long-term value that we believe will accrue to Shopify. Now turning to operating expenses. We continue to deliver operating leverage with operating expenses at 32% of revenue in the third quarter, down from 37% last year. Throughout the year, gross profit growth has outpaced operating expense growth by approximately 12 points each quarter. That consistency reflects our ability to scale efficiently while continuing to invest in the platform. The year-over-year dollar increase in R&D expense this quarter reflects continued investment in AI in our infrastructure and employee costs. Sales and Marketing grew 14% year-over-year. The slightly slower Q3 growth rate resulted from testing that we did in the U.S.
We paused spending for a couple of weeks in some channels and geographies in order to test the incrementality of our marketing efforts, which allows us to drive even greater precision into how we deploy the spend. Some of the reduced spend will effectively shift to Q4, but nothing has changed about our marketing approach. Our free cash flow was $816 million, a 22% margin. I should point out that approximately 150 basis points of the year-over-year improvement in free cash flow margins stems from the structural operating discipline and expense leverage that we've been delivering.
The remainder of the improvement results from items that are more temporary. The marketing test that we did this past quarter, the timing of certain tax receivables and the accounting change to merchant cash advances with each of these 3 being roughly equally sized. The point remains a very strong quarter of profitability. With that, let's move to our fourth quarter outlook.
We expect Q4 revenue growth in the low 30s year-over-year. Our guidance reflects less than 1 point of FX headwind. This outlook compares to a 29% constant currency growth rate last year. We expect gross profit dollars to grow in the high 20s. We expect Q4 operating expenses to be 29% to 30% of revenue, reflecting higher marketing expenses, including some initiatives in advance of BFCM. And finally, we expect free cash flow margin for Q4 to be in line with Q4 of last year. Our free cash flow performance in the fourth quarter primarily reflects a continuation of the trends we saw in Q3, but with higher taxes from the timing of payments in certain jurisdictions that get paid in the fourth quarter.
We don't expect any meaningful impact from the accounting change in merchant cash advances in Q4. A few thoughts in closing. Our opportunity remains substantial. We are serving more merchants and building more of what they need to grow. We continue to drive a larger share of commerce. We continue to expand commerce itself. We continue delivering top line results with proven consistency, consistency of GMV growth, consistency of revenue growth and consistency in the breadth of strength across regions, merchant sizes and channels.
Lastly, we continue to demonstrate strong discipline in our expenses. Our profitability is a combination of that discipline and a thoughtful planned investment as we build for the future. It took Shopify 18 years to reach our first $1 trillion in cumulative GMV. We expect to pass the second trillion by the end of this year, less than 2.5 years later. That gives you a sense of how the scale of our merchants businesses have compounded. With that, I'll turn the call back to Shane for your questions.

**Shane Kleinstein** (Executives):
Thanks, Jeff. We'll now take your questions before turning the call back to Harley for some final words. [Operator Instructions] Our first question will come from Samad Samana from Jefferies.

**Samad Samana** (Analysts):
Congrats on another strong quarter from the team. I wanted to see Harley, if we could dig into the relationship with Meta and Muse. It's been a key investor focus. How is Shop working with Meta on development? How does it impact the payment economics depending on whether they use Shop Pay or Meta Pay or another option. And any early signals on what merchants are seeing from this channel in terms of conversion, we think it's a big focus, and it would be very helpful.

**Harley Finkelstein** (Executives):
Yes. So thanks for the question. Specifically on personal agents, I mean, as I mentioned in my remarks, certainly the last quarter, you've seen a lot of them, whether it's Muse or Instinct or Claude Duet and I think one of the things we're most excited about is this feels like a brand-new channel for merchants. It feels like a new place where they can actually find new customers. And the fact that Shop Pay is integrated as a wallet means that the agent knows your size, he knows your style, he knows your shopping history and then all orders get tracked by the Shop app as well.
So I would say it's still quite early. Momentum is certainly strong. The quality of traffic is really, really quite high, and that we think is really, really important. But the agent is really just this new front door here. We are everything beyond that. So every new interface needs this commerce infrastructure running underneath it, and that's what we're doing. And I think the value is an enormous complexity of commerce. So the millions of lines of code that give the platform its power allows these agents to have -- provide the best experience to the new consumer and I think that will only continue as well.
In terms of just agentic in general, not just the agents, I think what you're seeing is that every week or 2, you're seeing a new agent or a new personal agent show up. And hopefully, you're noticing that Shopify is the commerce infrastructure behind all of them, we're partnering with all of them. Volume again is small, but traffic we saw in the last quarter was 2.6x year-on-year. Orders were up 3.3x and then Shopify Catalog is powering discovery in almost every single major AI channel. The other thing that's really cool is conversion from catalog is actually 2x the rate of general AI search sort of what people call scraping.
Maybe the last point I'll sort of end on here is that we are seeing that these AI channels are really rewarding specificity, which is really, really important for the long tail of commerce, which is most of our merchant base. So as we said, 74% of AI attributed purchases in Q3 were from outside our top 100 categories. So we're really seeing that these more nuanced niche products are getting found and that -- we have a ton of those on Shopify.
So the way that we see it is, Q3 saw personal agents hit the mainstream and all the major ones are partnered with Shopify. Our merchants' checkouts are supported and the fact that buyers can use a very familiar paying opportunity with Shop Pay as their wallet on an uncommon surface or a new surface, we think, is going to be a huge advantage to both merchants and consumers.

**Shane Kleinstein** (Executives):
Our next question will be from Andrew Boone at Citizens.

**Andrew Boone** (Analysts):
I wanted to stay on the agentic topic. As I think about the potential, and you talked about the potential of agents at large of moving towards what is a headless version of commerce. Can you talk about how that changes maybe the moat of Shopify? What happens to Shop Pay or the infrastructure and how you guys prioritize the road map?

**Harley Finkelstein** (Executives):
Thanks for the question on that. So here's -- let me be really clear about that because I think one thing that maybe is getting missed here is that with this entrance of sort of these personal agents, and the beginning of delegated purchasing, this is where agents don't just recommend products, but they're also buying on behalf of some of the users. And again, I said this in the last answer, but this is really the newest front door into commerce. This is very new behavior. Volume is, of course, small, but it's growing.
But in the new world of personal agents, shop is not just a wallet. It is your complete buyer profile. So when you connect shop to Muse, Instinct, or Claude Duet, or Grok Bot, the agent gets 3 things. First of all, it gets your entire shopping history across any Shopify merchants who can deliver these incredibly personalized recommendations. Second, with Shop Pay gets save payment details, you can pay the way you want with confidence, the agent doesn't get that information. And then the connection to the Shop app means even afterwards, you're able to track everything you purchased. So the fact that we have 400 million shoppers already trusting Shop and Shop Pay, now that trust goes with them into every single agent. We think that's really, really important.
So we actually think in a world of agents in a world of agentic shopping, these tools, specifically the shop tool and the tool kit that comes with Shop Pay, the Shop app, even UCP so your checkout is exactly what you want it to be, what it is on your website, we think has become even more important. The one thing I wanted to zoom up just for a sec because I suspect I may get a lot of great questions about agentic on this call. The way we think about this is that agentic ultimately is this incredible new opportunity for merchants. It is a new surface area that otherwise does not exist.
As Jeff mentioned earlier, this is, we think, going to be an incremental increase to commerce. He mentioned on the call -- on his remarks, but since start of 2025, we've seen an average -- we've captured nearly half of all incremental e-comm in the U.S. despite only being 14%. Part of what you're seeing is a strategy to make sure that wherever consumers are purchasing, whether online or offline or agents on social, Shopify helps merchants connect to it. So with more opportunity becomes more complexity. And actually, that is where Shopify's value goes up by simplifying more complexity where there's more front doors that allows us to play a larger role in the lives of the merchant that use Shopify.
So we think actually with more of these channels and more of these front doors, we will actually play a larger role in the lives of the merchants that use Shopify.

**Shane Kleinstein** (Executives):
Great. Our next question will come from Mike Morton from MoffettNathanson.

**Michael Morton** (Analysts):
Thanks for the question. Maybe just a little bit a follow-up, Jeff, on the Sidekick cost. You talked about doing a good job getting some leverage there on your token expenses. It's something that comes up a fair amount in the investor base. So just would love to maybe have some kind of guidance, not like the financial rate, but just -- you've talked in the past about subscription solution trend line 80% of gross margins. It's kind of 2 quarters in a row, it's been below that and trending down. When you look forward and you think about your ability to serve merchants with Sidekick but also get leverage on the token expenses. Has your philosophy on that 80% gross margin trend line changed at all?

**Jeff Hoffmeister** (Executives):
No. I guess, Mike, from my vantage point, what I would -- and I said this a little bit in my prepared remarks, I would go back to a couple of things. Number one, on Subscription Solutions. I talked about what we saw in Sidekick costs as well as also about being a blend of some of the other things we're doing from a hosting perspective. And so I feel really good in terms of what we're doing on subscription solutions. And again, I gave some detail in terms of some of the impact we're seeing on Sidekick. I really think we're doing some interesting things, and I reflect back to my comments in terms of essentially what we're doing in cost per additional inquiry versus usage.
And we're really trying to drive usage on Sidekick because we see significant benefit not only -- and this is -- Sidekick maybe one of these few products, not the only product, but it's -- just from a pure accounting perspective, obviously, the costs sit within subscription solutions, but the impact is really felt on both sides of our business, both the Merchant Solutions as well as on subscription solutions. So -- and I tried to do some of this in my remarks earlier in the call to just speak to you kind of the benefit we're seeing and how that value is going to accrue more and more over time in terms of in terms of the success of the business.
You also saw from the outlook I gave when you look at the gross margin implications for Q4 of this year, and you think about what that trend looks like both on a quarter-over-quarter basis as well as a year-over-year basis. We feel really good about what we're doing here on the core elements of the business. Some of what we're seeing in Q4 is going to be -- again, I also alluded to this earlier as well. Some of what we're going to see in Q4 is some infrastructure spend, which really speaks to us making sure in this super important quarter, the Q4 quarter was obviously the big holiday shopping season that we have extreme resiliency. We're ready to do everything our merchants need. So some of that's factored into the margins as well. But again, I think we feel really good about where we're heading on all this.

**Shane Kleinstein** (Executives):
Our next question comes from Mark Mahaney at Evercore ISI.

**Mark Stephen Mahaney** (Analysts):
Okay. You may have just answered the question I wanted to ask, which is the -- your guidance implies this...

**Shane Kleinstein** (Executives):
Mark, if you come back in the queue, we'll get you back in. Mark, you should be able to...

**Mark Stephen Mahaney** (Analysts):
I'm back. Can you hear me now? Sorry about that. Just a little bit more on the free cash flow margin for Q4. You typically have free cash flow margins up sequentially. And maybe you just answered it with the last question about a little bit of extra infrastructure spend in Q4, and I know you had some small onetime items in the cash flow margin in Q3. But just any more clarification on why you wouldn't have your normal sequentially up free cash flow margin in Q4?

**Jeff Hoffmeister** (Executives):
Yes. I think there's a couple of things, Mark. I alluded to this in my comments earlier that there is some marketing spend that has shifted effectively from Q3 to Q4 in terms of some of the testing we did. But more importantly, when you look what we're doing on the performance marketing side, the returns have been very, very good. There are some opportunities just going into holiday shopping season, what we've already seen in terms of putting some marketing dollars to work in a highly effective way. And that's Shopify. We're going to lean into opportunities like that, and I think that's exactly what you would want us to do.
And even with that opportunity on the marketing side and some of the things I alluded to on the infrastructure side, we're still getting to those margins. So again, there's a little bit of timing differential between the two. But between some of the investments on the infrastructure side and some of the investments in the marketing side, we're still delivering these margins, right? So -- and when you look what that implies for where we will end for the full year, again, I think from an overall expense perspective, from a profitability perspective, nothing has fundamentally changed. We feel -- I feel very good about where we are with this business right now.

**Shane Kleinstein** (Executives):
Great. Our next question is coming from Ken Gawrelski from Wells Fargo.

**Kenneth Gawrelski** (Analysts):
If I could ask just 2 quick, please. First is just on the industry side. There's a fair amount of debate between horizontal kind of general purpose agents and vertical agents. With the full acknowledgment that Shop remains largely agnostic here, could you -- you have a unique vantage point and I would appreciate your perspective maybe Harley, on that one. And very quickly, just one more on the Subscription Solutions revenue. Could you talk a little bit about kind of the disconnect between subscriptions revenues decelerating while GMV remains so robust. You have -- could you talk about the outlook as you think 4Q into next year for that line item?

**Harley Finkelstein** (Executives):
I'll take the first question. Look, I mean, I think you sort of answered the question yourself, which is our job is to be channel agnostic. The fact -- I mentioned this in the early -- in my earlier remarks, but while we're all talking and excited about agentic and what's to come, it's still -- there's so much white space here. At the same time, our merchants are still selling online, they're selling offline. Our job is not necessarily to predict exactly what channel will be the next big channel. Our responsibility to the merchant is Shopify is to make sure they're everywhere.
So obviously, when there are some very large new agents that come out from some of the largest companies, we want to make sure we're front and center. That's the Muse and Instinct and Claude Duet style. But beyond that, I mean, we're also building web MCP, which enables agentic checkout, any agent can complete a checkout with any store. We also built Shop.dev, which are these -- and Shop.md, in fact, which are these are specifically for developers, 1 file that can turn any surface area into a commerce experience. Shop.md on the shopper side is 1 prompt that turns your agent into your personal shopper.
So you're seeing us ensure that whatever comes out, if there's commerce integration or there's a commerce component that Shopify is either directly integrated at day 1 or we're creating these tooling like Shop.dev and Shop.md so that any third-party developer who wants to bring commerce into their application, whether it's a vertical agent or it's a horizontal agent is able to do so very easily. The idea really here is to be too good to ignore, whether it's UCP or its catalog or it's the Shop app or Shop Pay, make it so that any type of agentic tooling that wants to incorporate commerce comes to Shopify, first and foremost.

**Jeff Hoffmeister** (Executives):
Yes. And I would just add to your question on the Subscription Solutions piece versus GMV. Obviously, most of the GMV gets manifested in the payments revenue, which ends up on the Merchant Solutions side. As I alluded to in my comments earlier, this is -- we don't try and from a pure accounting perspective, manage one piece of the business versus the other or the Subscription Solutions generally captures again, the merchants, which are being added to the platform as well as variable platform fees and then everything from a payments tax, shipping, capital, et cetera, all that ends up in Merchant Solutions.
So you see this in the MRR growth, I mentioned in my comments and you've seen in the press release that MRR was up 19% year-over-year. We talked a little bit about the marketing element of this, too. So from a merchant adds perspective, we feel really good about what we're seeing there. But this is when you look at the revenue growth in terms of what we delivered in Q3, it being 32%. The guidance we talked about low 30s. This would be -- that would mark the seventh consecutive quarter of revenue in the low 30s. We feel really good about where we are.
And then the only other thing I would add is you know for some of -- as we get some of the larger merchants want to just do more GMV, there's even a larger disproportionate share of value that comes on the payment side versus on the Subscription Solution side. So when we think about these 2 together, and we want to add great merchants to the platform. And then obviously, over time, and we've talked about cohorts in the past, over time that continues to generate more and more revenues for us. So we feel really good about where it is.

**Shane Kleinstein** (Executives):
Our next question will come from Jim Callahan from Piper Sandler.

**James Callahan** (Analysts):
Just kind of curious on the marketing tests, I understand some of this will reverse in 4Q. But curious what the conclusion of the test was and maybe could this have had any top line impact in the quarter?

**Jeff Hoffmeister** (Executives):
No, no top line impact. This is -- this was testing in some channels in some geographies. And I would just say what we're always trying to do, Jim, is just get smarter and hone even further the accuracy of our analysis, and it gives us a lot of confidence in the returns that we're seeing. No change in marketing philosophy, no change in terms of how we lean on performance marketing, we just want to always be smarter and better at what we're doing. And again, the returns have been very compelling. So every now and then you make sure you're doing your best to analyze returns and make sure that next incremental dollar of marketing spend is deployed very wisely.

**Harley Finkelstein** (Executives):
One of the things that I think is most remarkable but the business model here is that our model has this breadth of growth levers it is not a single bet on one growth curve. We have sort of this portfolio of commerce and payments, international agentic enterprise. And in any given quarter, some will be stronger than the others. But the durability, I think, of the story is the compounding strength across that set. International GMV was up 32%. B2B saw 74% growth, off-line GMV was up 30%, we crossed the $200 billion mark for off-line GMV. And then you have enterprise as well.
So what we try to think about is sort of this portfolio of bets and making sure that whatever is to come, we're front and center, but also making sure that we're able to -- Shopify ultimately is a growth company, and we want to stay focused on driving merchants growth in turn that fuels our growth. But there's never necessarily 1 particular place we put our eggs in because we have this portfolio of opportunities. And I think that actually talks to the durability of this business model.

**Shane Kleinstein** (Executives):
Our next question is from Shweta Khajuria with Wolfe Research.

**Shweta Khajuria** (Analysts):
Could I please follow up on agentic commerce. So when we think about the economics and how economics will evolve, where will the -- how will it work in your view? Will the merchants be paying a certain take rate? Or are you -- will you be sharing the economics with these agents? How does this evolve in the near term and maybe mid- to long term? And then how do the agents choose Shop Pay, if I, as a consumer, have set up Shop Pay and other forms of payment, how do these agents default to Shop Pay as the option.

**Harley Finkelstein** (Executives):
Maybe I'll take the second part of the question and then Jeff can do the first part of monetization. That's the best part of Shop Pay because we have 400 million consumers that are using it constantly across all their favorite brands. We want to make sure that when the consumer is using any agent that they want and Shop Pay is available, that's the one they select. And so that's -- ultimately, this is about ensuring that consumers have an amazing experience that they have -- that they're able to get the right credit card information, the right sizing, the right merchandising of the product they want and able to purchase it.
Part of the reason why we're beginning to talk more about Shop as the suite of products with Shop Pay with your preferences, with your order tracking is that ultimately, we think that when consumers are given a number of different options, they're going to pick the option that is best for them. That results with the highest -- the best experience, high security, it is fast, but it also knows the details of their purchase history, and that's what they get with Shop Pay. So this is about merit, and we believe that we can compete on merit to get more consumers to use it.

**Jeff Hoffmeister** (Executives):
Yes. And to Harley's point on that very -- that very point he just made. What we're trying to do is make sure, of course, more and more merchants use Shopify as their core platform. If you start to your questions whether if you start for example, on Muse. And if you, as a consumer, then do a search, which leads to a merchant, which is using Shopify then the economics are exactly the same, essentially what this is another form of discovery, they're sending you to the merchant's website and everything else that you would have done and any other form of discovery ends up to the same economics back to Shopify. And then to Harley's point, what we're trying to make sure we do is get Shop Pay out there more and more in terms of a wallet perspective and continue to expand the economics on that front as well.

**Shane Kleinstein** (Executives):
Our next question is from Paul Treiber with RBC Capital Markets.

**Paul Treiber** (Analysts):
Shopify during the quarter bought shop.com for about $100 million. It's a fairly sizable amount, how do you think about shop.com coexisting with merchant websites and other channels? And then the second question is why now, particularly in light of the rise of AI agents, what's the importance of having a centralized location?

**Harley Finkelstein** (Executives):
Yes. Look, in the physical retail world, location, location, location matters, we think the same thing that applies online as well and we think shop.com is an incredible prime address for us. I think the way you should view this is, this is a declaration that we're ready for more ambitious posture for Shop. We wanted to make a deliberate investment to Shop's credibility and discoverability as a consumer shopping destination, not just a tracking utility. And we think this is a really convenient, very easy entry point for shoppers to discover incredible brands and products. The transition required no action for merchants and shopper -- traffic to shop is growing even faster on the web than in the app.
So this was us moving basically the shop -- we were at shop.app previously we're moving to shop.com. We think this is one of the most important locations on the Internet, and that really matters to us. But I think you can sort of glean from this what our ambition is with Shop.

**Shane Kleinstein** (Executives):
Our next question is from Colin Sebastian with Baird.

**Colin Sebastian** (Analysts):
I appreciate the questions. I guess, Harley, what's helping Shopify win more of these point-of-sale merchants that didn't start with you online? And I guess, is that changing your approach to acquiring those. And then maybe a follow-up on the -- all the questions around variable economics with agentic. I guess as Sidekick takes on more merchant workflows and the product catalog is now really critical for powering agentic, are you thinking about translating that value into higher monetization? Or is it more about expanding Shopify's share of overall retail.

**Harley Finkelstein** (Executives):
I mean on the point-of-sale on the retail side, this certainly was an incredible quarter for offline. I mean, I mentioned that lifetime POS GMV crossed $200 billion in Q3. GMV was up 30%. We had Canada Goose who brought on dozens of locations, BevMo! brought over 150 locations. The Body Shop, MAC Cosmetics, added 83 locations under 90 days. So -- and what we're seeing is that offline is not a separate business. It is the same platform, the same catalog, the same buyer relationships. It's just extended into the physical world.
And I think we're seeing more businesses with very established brick-and-mortar businesses, their own come to Shopify for this unified commerce capability. It's great when we get a point-of-sale only merchant to come on first and foremost, and expand, but also what is happening is the fact that new features. We just announced something recently at our Editions, but point-of-sale now automatically recognizes customers at checkout by using Shopify payment network in the actual physical store. That's never happened before. So this brings sort of this digital style customer context to physical retail, which frankly has never been the case.
And I think ultimately, whether it's expanding customer recognition and point-of-sale or it's expanding locations, we are now becoming one of the default places that retail goes, not just for online, but also for off-line as well. I think generally around enterprise, just because a lot of these very large point-of-sale installations are coming from enterprise. Enterprise is getting some incredible momentum here. We're able to not only get some of the up and comers that are expanding sort of the home growth success stories are staying with us, but the fact that we're bringing the Lululemons of the world, for example, or Burton or Balmain or Canada Goose who all went live in Q3. 
I mean the pace of that, again, it is -- it takes longer to bring enterprise merchant to migrate on, but we've really figured out how to get them on as quickly as possible given the context and all their integrations so I think both point-of-sale and enterprise is going really, really well. And yes, what is the second part of your question? I think I missed that.

**Shane Kleinstein** (Executives):
I think you got it, Harley, I think you got it. We're now going to go to Bryan Smilek at JPMorgan for a final question.

**Bryan Smilek** (Analysts):
Great. Just curious on Sidekick, very good to see you continue to gain efficacy. Can you just talk about the product road map into '27 across analytics, cogeneration and Canvas more broadly? And then Jeff, just more near term, can you just elaborate on where you're going to allocate the incremental infrastructure spend into Black Friday, Cyber Monday? Will that be more across Sidekick or just broader platform volume?

**Harley Finkelstein** (Executives):
Yes, it is amazing. I mean, for new merchants, Sidekick is helping with the first sale much faster, continue to grow. In Q3, we saw a 3% lift in the number of merchants reaching 5 orders within 60 days after using the guide. That's on a very, very large base. So it is becoming obviously incredibly powerful for new merchants, but also for complex tasks inside the flow of running a business, whether it's these third-party apps that are now able to integrate merchants on average, use 8 apps to help them run their day-to-day business that all integrates into Sidekick.
Beyond that, you're seeing these incredible examples of power users who are pushing into this advanced design, doing SEO, product creation, and so I think, generally, you're just going to see Sidekick continue to provide more value over time, both for new merchants, but I mean, 2/3 of all Shopify flows were created by Sidekick in this past quarter. So the pattern should be very clear. More merchants are using it. And each merchant is finding more ways to use it over time, that value will only compound. Again, it's powered by 20 years of commerce experience. So there's that intelligence and it also knows the full context of everything about your particular store.

**Jeff Hoffmeister** (Executives):
Yes. And Bryan, to your question about source of the spend, some of it is Sidekick. There's also some interesting things we're doing on search capabilities. We've had search capabilities for merchants for a while. We're continuing to enhance that, make that even stronger and storefront resiliency, again, as I alluded to, as you go into the big holiday shopping season, we want to make sure we are extremely ready to let merchants do everything they can in terms of sell as much as possible. And so there's some things on the storefront infrastructure that we're doing.

**Shane Kleinstein** (Executives):
And then we'll go to Harley for some closing comments.

**Harley Finkelstein** (Executives):
Yes. Thanks, Shane. Maybe before we close, I just want to leave you all with something. First and foremost, today's results reflect decisions that we've made probably 3 years ago. And the work that we're doing right now, the new projects, new products, the new enhancements you're seeing coming out with things like additions, that's going to show over the next 3, 6, maybe even 9 years. Retail is obviously changing completely. New channels seem to keep emerging. All the channels are becoming big again. And I think I can appreciate from the outside, it may be hard to sort of keep pace of this. But through it all, I hope it is very clear that Shopify is unequivocally at the epicenter of all of this. We deeply believe this is one of the most exciting times in retail and commerce in a very long time.
And as you see new companies or new technologies or even new models launched where commerce is involved, Shopify will be integrated and that is not by accident. We work really, really hard to be the de facto partner for commerce on the Internet, whether that means partnering or building it ourselves or collaboration. And so for those listening, if you're a shareholder, this is what you should want from us to be the company, not just betting on commerce, but also helping architect for what is coming and executing on that vision. And the one that is constantly giving things hopefully that surprise you, which is how we stay ahead. I said in the press release this morning that Shopify is uncommonly good at operating in 2 realities at the same time, the world that our merchants exist in today and the ones that they are moving towards.
And we do this for both new entrepreneurs making the very first sale. You heard the call from Dell at the top of this call, who just had his first sale or the biggest brands in the world, but I think commerce of all shapes and all sizes are coming to Shopify. There is no floor, no ceiling. And the products we're building is not just to help them right now, but also to future proof them long into the future. Many of you have been betting on Shopify for almost 12 years now since the IPO. And I think in that time, I believe we've earned the right to be considered a highly trusted public company because we do what we say we're going to do, and we do that reliably and I think we do that durably, and we will absolutely keep doing that. So thanks for joining us on this call, and we will talk to you all next quarter.

**Shane Kleinstein** (Executives):
Great. Thanks, Harley. Thanks, Jeff. This wraps our third quarter 2026 conference call. Thanks, everyone, for joining, and we look forward to speaking to you all soon. Have a great day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SHOP_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜guidance：CFO 給 Q3 營收年增低 30 幾%（原話："We expect Q3 revenue growth in the low 30s year-over-year."）
- 2026-08-05｜CFO｜guidance：CFO 給 Q3 毛利金額年增中高 20%（原話："gross profit dollars to grow in the mid- to high 20s"）
- 2026-08-05｜CFO｜guidance：CFO 給 Q3 營業費用占營收 33%–34%，並對照去年 Q3 的 37%（原話："operating expenses in Q3 to be 33% to 34% of revenue"）
- 2026-08-05｜CFO｜guidance：CFO 給 Q3 自由現金流率區間，含不到 1 點商業預支款會計變更的順風（原話："cash flow margin to be in the high teens to low 20s"）
- 2026-08-05｜CFO｜guidance：CFO 表示 Q3 無重大匯率影響（原話："We do not expect any significant FX impact."）
- 2026-08-05｜CFO｜margin：Q2 營業費用占營收 34%，較去年同期改善近 4 點（原話："operating expenses, which were 34% of revenue"）
- 2026-08-05｜CFO｜margin：Q2 自由現金流率略高於 18%，高於先前展望（原話："our Q2 free cash flow margin was just over 18%"）
- 2026-08-05｜CFO｜margin：排除商業預支款會計變更後，自由現金流率年增約 1.5 點（原話："roughly 1.5 points of year-over-year margin expansion"）
- 2026-08-05｜CFO｜margin：商家解決方案毛利率微幅高於去年，支付量增加的壓力被高毛利收入抵銷（原話："Margin pressure from increased payments volume"）
- 2026-08-05｜CFO｜margin：國際市場支付毛利率通常較高，理由是簽帳卡比例高、交換費低（原話："payments gross margins are generally higher in international"）
- 2026-08-05｜CFO｜margin：訂閱解決方案毛利率略低於 80%，與 Q1 持平；Sidekick 的 AI 成本多數落在此處（原話："gross margins just under 80%"）
- 2026-08-05｜CFO｜margin：Sidekick 使用量放大的同時，訂閱毛利率季對季維持相近水準（原話："hold gross margins at a relatively consistent level"）
- 2026-08-05｜CFO｜margin：銷售與行銷費用占營收低於 14%，年減約 160 基點（原話："Sales and marketing in Q2 was less than 14% of revenue"）
- 2026-08-05｜CFO｜margin：內部 AI 支出多數歸在研發費用（原話："the majority of our internal AI spend is allocated here"）
- 2026-08-05｜CFO｜margin：交易貸款與損失占營收 3.9%，Capital 為本季較大推手（原話："Transaction loans and losses came in at 3.9% of revenue."）
- 2026-08-05｜CFO｜margin：支付與信貸損失率處於正常水準，Capital 為較大推手（原話："Capital was a larger driver this quarter"）
- 2026-08-05｜CFO｜commitment：CFO 重申毛利率若承壓，會以營業費用成效超額抵銷（原話："any pressure we see on gross margin, we'll more than"）
- 2026-08-05｜CFO｜commitment：CFO 表示 AI 策略為最大槓桿搭配成本管理（原話："Maximum leverage paired with thoughtful cost"）
- 2026-08-05｜President｜commitment：Harley 表示代理式交易沿用與網店交易相同的經濟模型，無新增費用（原話："There's no new fees. There's no separate pricing."）
- 2026-08-05｜President｜commitment：被問 Sidekick 是否直接收費時，管理層保留彈性、未承諾（原話："we reserve the right to wake up smarter every single day"）
- 2026-08-05｜CFO｜commitment：R&D 持續維持費用紀律（原話："we'll continue to be disciplined in managing the spend."）
- 2026-08-05｜CFO｜product：Q2 營收年增 34%，超出預期（原話："Q2 revenue grew 34% or 33% on a constant currency basis"）
- 2026-08-05｜CFO｜product：支付滲透率年增 3 點至 68%（原話："payments penetration, which grew 3 points year-over-year"）
- 2026-08-05｜CFO｜product：Shop Pay GMV 年增 53%（原話："Shop Pay GMV grew 53% year-over-year."）
- 2026-08-05｜CFO｜product：Q2 MRR 年增 19%（原話："Q2 MRR grew 19% year-over-year"）
- 2026-08-05｜President｜product：Sidekick 日活躍商家年增 3.6 倍（Q&A 中同一指標講成 3x）（原話："daily active merchants using Sidekick were up 3.6x"）
- 2026-08-05｜President｜product：Sidekick 建立自訂應用數從 Q1 的 12,000 增至 36,000（原話："36,000 custom apps, up from 12,000 in Q1."）
- 2026-08-05｜President｜product：Catalog 驅動的 AI 搜尋轉換率為爬取資料的兩倍（原話："AI searches powered by Catalog converted twice the rate"）
- 2026-08-05｜President｜product：Shop app 自有 GMV 年增逾 70%（原話："Shop app's native GMV grew over 70%"）
- 2026-08-05｜President｜product：內部使用蒸餾模型，大模型教小模型處理特定任務（原話："we now have a number of distilled models"）
- 2026-08-05｜President｜competition：代理式流量與訂單年增三倍（原話："AI-driven traffic and also orders to Shopify stores tripled"）
- 2026-08-05｜President｜competition：傳統搜尋工作階段仍在成長，管理層稱 AI 為搜尋的補充（原話："AI as a complement to search rather than a substitute"）
- 2026-08-05｜President｜competition：管理層回應上季關於代理式是否取代搜尋的疑問，稱搜尋成長良好（原話："but search is growing incredibly well"）
- 2026-08-05｜President｜competition：OpenAI、Google、Meta、Microsoft 為合作夥伴（原話："like OpenAI, Google, Meta, and Microsoft, have"）
- 2026-08-05｜President｜competition：AI 歸因訂單 75% 來自前 100 大品類之外（原話："with 75% of AI-attributed orders in the second quarter"）
- 2026-08-05｜CFO｜competition：CFO 引用 eMarketer，稱 Shopify 商家取得美國電商增量近半（原話："Shopify merchants have captured nearly half of all"）
- 2026-08-05｜CFO｜competition：CFO 將電商加速或長尾價值視為基本情境之外的上行因素（原話："is upside to our underlying growth story"）
- 2026-08-05｜CFO｜customer：$25M 以上級距成長最快，基期較小（原話："The $25 million in greater band is the fastest-growing"）
- 2026-08-05｜CFO｜customer：各區域固定匯率 GMV 成長：北美 28%、歐洲 34%（原話："North America GMV grew 28%, and Europe grew 34%"）
- 2026-08-05｜CFO｜customer：線下 GMV 年增 32%、B2B GMV 年增 76%（原話："Offline GMV was up 32%. B2B GMV grew 76%"）
- 2026-08-05｜CFO｜customer：年 GMV 達 100 萬美元的商家五年留存率 92%（原話："$1 million in annual GMV had a 92% retention"）
- 2026-08-05｜President｜customer：大型複雜零售商為成長最快的區塊（原話："particularly strong momentum with large complex retailers"）
- 2026-08-05｜President｜customer：國際 GMV 年增 37%（原話："International GMV grew 37% in the quarter"）
- 2026-08-05｜President｜customer：Harley 稱較大商家選擇 Shopify 的速度加快（原話："Larger merchants are now choosing"）
- 2026-08-05｜President｜customer：Harley 稱全球零售銷售占比不到 1%，國際市場滲透不足（原話："I think we've captured less than 1% of global retail sales."）
- 2026-08-05｜President｜risk：Harley 承認少數商業模式目前不適合完整遷移（原話："There are some merchants that just"）
- 2026-08-05｜President｜risk：Harley 強調代理式量體相對 GMV 仍小、仍屬早期（原話："Look, it is early and"）
- 2026-08-05｜CFO｜capital_allocation：營運槓桿提供持續投資平台與內部 AI 能力的彈性（原話："This operating leverage provides the financial flexibility"）

### 問答異常語氣（迴避／改口／保留）
- SHOP_Q2_2026_Earnings_Call_20260805.md｜問：CIBC 問自由現金流率約 20% 是否為新常態、槓桿來自哪裡｜答法：CFO 不正面回答是否為新常態，改指向 Q3 財測並說持續創造槓桿
- SHOP_Q2_2026_Earnings_Call_20260805.md｜問：Morgan Stanley 問 Sidekick 對留存、GMV 成長、產品附加率的數據，以及未來是間接或直接變現｜答法：Harley 未提供留存／GMV／附加率數字，改談使用量與案例；變現部分只說保留彈性、模式建立在商家成功上

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
{"date":"20260808","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"US／全球電商份額持續擴大（跑道未走完，SHOP 是主要收割者之一）","columns":{"可證偽門檻":"US 份額 YoY 連 2 季不再上升；或 B2B GMV YoY 增速降至 &lt;40%","本次狀態":"成立：US 份額 14%（YoY +2pp）、B2B GMV +76%（101%→84%→76% 減速軌跡，證偽門檻＜40% 尚遠）、Q2'26 GMV +32%（連 5 季 &gt;30%）"}},{"id":"H2","text":"Take rate 持續擴張（monetization 是結構性的，非一次性）","columns":{"可證偽門檻":"Take rate 連 2 季 QoQ 不再上升；或 Payments 滲透率連 2 季不再上升","本次狀態":"成立：2.84%→3.05%→3.14% 軌跡向上；Payments 滲透 68.0%（YoY +3pp）"}},{"id":"H3","text":"現價已合理反映成長減速路徑（62× 不是為「維持今天成長率不變」定價）","columns":{"可證偽門檻":"FY+2 共識 EPS 上修 ≥33%（使 PEG 回落至 1.0）；或股價回檔 ≥20%","本次狀態":"不成立：目前無跡象顯示分母端會以此速度追上；此假設是本檔判觀望的直接原因"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回檔至 $70–90 區間（$70≈PEG 1.0 對應 FY+1 共識成長 29.2%；上緣 $90 保留予國際 take rate 收斂槓桿〔Payments 僅covers~40國〕兌現空間）；或終端倍數假設站上同業現值上緣（NOW 28x）之後仍具正 EV；觸發後首階 1/3 分批建倉","irr_base_pct":-3.1,"ev5y_pct":-2.3,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"🟡","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.3,"ev5y_pct":-2.3,"irr_base_pct":-3.1,"max_dd_pct":-58.0,"bull_5y_price":243.8,"bear_5y_price":67.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"股價回檔至 $70–90 區間（$70≈PEG 1.0 對應 FY+1 共識成長 29.2%；上緣 $90 保留予國際 take rate 收斂槓桿〔Payments 僅covers~40國〕兌現空間）；或終端倍數假設站上同業現值上緣（NOW 28x）之後仍具正 EV；觸發後首階 1/3 分批建倉","price_at_dd":151.57,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SHOP_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
