你是 stock-analyst **v20 判斷 agent**，標的 CHEF（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CHEF","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CHEF_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CHEF_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1135.4,"period":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿 investors.chefswarehouse.com「The Chefs' Warehouse Reports Third Quarter 2026 Financial Results」（2026-10-28，SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm）"}},{"id":"f_kpi1_ebitda_non_gaap_adjusted","label":"調整後 EBITDA（公司不報 non-GAAP 營業利益，以 Adjusted EBITDA 代）","value":82.2,"period":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿 investors.chefswarehouse.com「The Chefs' Warehouse Reports Third Quarter 2026 Financial Results」（2026-10-28，SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm）"}},{"id":"f_kpi2_gaap","label":"營業利益（GAAP）","value":51.5,"period":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿 investors.chefswarehouse.com「The Chefs' Warehouse Reports Third Quarter 2026 Financial Results」（2026-10-28，SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm）"}},{"id":"f_kpi4","label":"毛利率","value":25.0,"period":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿 investors.chefswarehouse.com「The Chefs' Warehouse Reports Third Quarter 2026 Financial Results」（2026-10-28，SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm）"}},{"id":"f_kpi7_fy2026","label":"FY2026 全年指引（上修）","value":"營收 4.56–4.61B；毛利 1.130–1.140B；Adj. EBITDA 317–321m；淨利 108.5–110.0m；SBC 29–30m；利息費用 45.5–46.5m","period":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿 investors.chefswarehouse.com「The Chefs' Warehouse Reports Third Quarter 2026 Financial Results」（2026-10-28，SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm）"}},{"id":"f_kpi8_specialty_case_count_yoy","label":"有機 specialty case count YoY","value":6.1,"period":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿 investors.chefswarehouse.com「The Chefs' Warehouse Reports Third Quarter 2026 Financial Results」（2026-10-28，SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm）"}},{"id":"f_kpi9_yoy","label":"不重複客戶數 YoY","value":4.4,"period":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿 investors.chefswarehouse.com「The Chefs' Warehouse Reports Third Quarter 2026 Financial Results」（2026-10-28，SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm）"}},{"id":"f_kpi10_unique_item_placements_y","label":"Unique item placements YoY","value":7.2,"period":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿 investors.chefswarehouse.com「The Chefs' Warehouse Reports Third Quarter 2026 Financial Results」（2026-10-28，SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm）"}},{"id":"f_kpi11_center_of_the_plate_yoy","label":"Center-of-the-plate 有機磅數 YoY","value":6.6,"period":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿 investors.chefswarehouse.com「The Chefs' Warehouse Reports Third Quarter 2026 Financial Results」（2026-10-28，SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_chef_gross_margin_pct","label":"CHEF 毛利率","value":24.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHEF.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_chef_operating_margin_pct","label":"CHEF 營業利益率","value":4.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHEF.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_chef_fcf_margin_pct","label":"CHEF FCF 利潤率","value":4.03,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHEF.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_syy_gross_margin_pct","label":"SYY 毛利率","value":18.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SYY.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_syy_operating_margin_pct","label":"SYY 營業利益率","value":3.66,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SYY.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_syy_fcf_margin_pct","label":"SYY FCF 利潤率","value":2.29,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SYY.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_usfd_gross_margin_pct","label":"USFD 毛利率","value":17.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.USFD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_usfd_operating_margin_pct","label":"USFD 營業利益率","value":3.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.USFD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_usfd_fcf_margin_pct","label":"USFD FCF 利潤率","value":2.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.USFD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pfgc_gross_margin_pct","label":"PFGC 毛利率","value":11.93,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PFGC.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pfgc_operating_margin_pct","label":"PFGC 營業利益率","value":1.31,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PFGC.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_pfgc_fcf_margin_pct","label":"PFGC FCF 利潤率","value":1.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PFGC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_gaap_eps","label":"GAAP 淨利／稀釋 EPS","value":29.6,"period":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿 investors.chefswarehouse.com「The Chefs' Warehouse Reports Third Quarter 2026 Financial Results」（2026-10-28，SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm）"}},{"id":"f_kpi5_141_1_25_4","label":"自由現金流（僅有累計：營業現金流 141.1 − 資本支出 25.4，前九個月）","value":115.7,"period":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿 investors.chefswarehouse.com「The Chefs' Warehouse Reports Third Quarter 2026 Financial Results」（2026-10-28，SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm）"}},{"id":"f_kpi6_sbc_gaap_q3_sbc_9_3m","label":"SBC 占 GAAP 營業利益（Q3 SBC 9.3m）","value":18.1,"period":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿 investors.chefswarehouse.com「The Chefs' Warehouse Reports Third Quarter 2026 Financial Results」（2026-10-28，SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":105.41,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":35.16,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":43.65,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.39,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.58 → 2.57）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.65,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.09 → 3.07）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.83,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.62 → 3.65）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":2.57,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":3.07,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.65,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.98,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 2.52 → 2.57（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":45.24,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝75.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":75.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.02,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.19,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":41.02,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 2.57，分子＝快照價 105.41","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":781.05,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 945.77、現金 164.72（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":43.46,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":5362.47,"period":"2026-11-03","unit":"USD m","basis":"市值 4581.42 ＋ 淨負債 781.05","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":4607.44,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（7 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":5021.64,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（7 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.16,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 105.26 / W52 83.15 / W104 70.39 / W250 49.18 / W250 13週斜率 2.51%"},{"id":"f_ma_w52","label":"52 週均線","value":83.15,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":70.39,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":49.18,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.51,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"10-K FY2025：公司稱營收成長來自市占提升（銷售團隊、品項廣度、收購、新配送中心）。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm","excerpt":"Through these efforts, we believe that we have been able to expand our customer base, enhance and diversify our product selections, broaden our geographic penetration and increase our market share.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：客戶轉換成本極低、進入門檻低、無獨家合約，競爭可能導致降價與市占流失。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm","excerpt":"The cost of switching distributors is very low, as are the barriers to entry into the U.S. foodservice distribution industry.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K：競爭對手含大量在地小型配送商與少數全國性綜合配送商，部分資源較公司雄厚；未點名具體新進入者。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm","excerpt":"We compete with numerous smaller distributors on a local level, as well as with a limited number of national broadline foodservice distributors. Certain of these distributors have greater financial and other resources than we do.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2026 Q2（2026年7月）公司稱銷售與淨利雙位數成長，來自訂單量、新客戶與北美市占持續提升（媒體轉述公司說法，無第三方份額數據）。","source":"Distribution Strategy: Chefs' Warehouse Delivers Double-Digit Sales Growth","url":"https://distributionstrategy.com/2026/07/chefs-warehouse-delivers-double-digit-sales-growth-as-restaurant-demand-remains-strong/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"前十大客戶合計僅約占 FY2025 總淨銷售 6%，公司稱無重大客戶集中度","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm","excerpt":"We have no meaningful customer concentration as our top ten customers accounted for approximately 6% of total net sales for our 2025 fiscal year.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"應收帳款無單一重大客戶餘額；公司持續做客戶信用評估，通常不要求擔保品，部分客戶有個人保證","source":"SEC EDGAR 10-K FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm","excerpt":"The Company generally does not require collateral. However, the Company, in certain instances, has obtained personal guarantees from certain customers. There is no significant balance with any individual customer.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"CHEF 2026年Q2 specialty品類箱量年增6.0%、獨立客戶數增3.6%、產品配置數增7.2%；全年2026營收指引維持45億至46億美元（1月初始指引為43.5億至44.5億）。","source":"Distribution Strategy: Chefs' Warehouse Delivers Double-Digit Sales Growth as Restaurant Demand Remains Strong","url":"https://distributionstrategy.com/2026/07/chefs-warehouse-delivers-double-digit-sales-growth-as-restaurant-demand-remains-strong/","excerpt":"Specialty product case volume increased 6.0%, the number of unique customers grew 3.6%, and product placements increased 7.2% from a year earlier.","as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：公司大量特色食品、生鮮與肉類產品來自本地至國際第三方供應商，通常無長期供貨合約、未用金融工具對沖食品價格風險，找不到替代供應來源可能導致成本顯著上升（未具體量化關稅暴露）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm","excerpt":"We obtain a significant portion of our specialty food products, produce and center-of-the-plate products from local, regional, national and international third-party suppliers.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"UBS 會議（2026-03）：公司約 9 萬 SKU，自 40 多國進口，管理層稱採購彈性與自有品牌可因應關稅。","source":"MarketBeat：Chefs' Warehouse says demand is resilient at UBS conference","url":"https://www.marketbeat.com/instant-alerts/chefs-warehouse-says-demand-is-resilient-at-ubs-conference-highlights-ai-tariff-flexibility-2026-03-14/?.tsrc=rss","excerpt":null,"as_of":"2026-03-14","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2026-03 UBS 會議摘要：CHEF 約 90,000 SKU，配送中心在美國、加拿大與中東，自 40 多國進口；管理層稱關稅變動不致造成恐慌、目前未見中東更廣的總體供應鏈衝擊（二手摘要，未讀原頁）","source":"MarketBeat: Chefs' Warehouse says demand is resilient at UBS conference","url":"https://www.marketbeat.com/instant-alerts/chefs-warehouse-says-demand-is-resilient-at-ubs-conference-highlights-ai-tariff-flexibility-2026-03-14/?.tsrc=rss","excerpt":null,"as_of":"2026-03-14","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"公司文件揭露：食品配送業務集中於特定餐飲市場，暴露於區域經濟風險（區域集中，非地緣；二手摘要）","source":"Chefs' Warehouse IR filing (gcs-web)","url":"https://chefswarehouse.gcs-web.com/node/10561/pdf","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2026-10 報導：Dallas 營運併入新配送中心、新英格蘭合併設施增容、Las Vegas 蛋白質加工擴張；公司約 49–53 個配送中心，無單一設施單點失效的來源","source":"Distribution Strategy: Chefs' Warehouse Expands Distribution Network","url":"https://distributionstrategy.com/2026/10/chefs-warehouse-expands-distribution-network-sales-hiring-and-ai-investment/","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因素：第三方供應商未遵守食安等法規可能中斷原料或產品供應","source":"SEC 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm","excerpt":"◦the risks associated with third-party suppliers, including the risk that any failure by one or more of our third-party suppliers to comply with food safety or other laws and regulations may disrupt our supply of raw materials or certain products or injure our reputation;","as_of":"2026-02-25","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026（10/28 公布）：淨銷售約 $1.14B、+11.2%，有機 +10.3%；Specialty 有機案數約 +6.1%、獨立客戶 +4.4%、placements +7.2%；Center-of-the-plate 有機磅數約 +6.6%。","source":"Chefs' Warehouse 8-K Q3 2026 press release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 淨通膨 4.1%（Specialty 2.6%、Center-of-the-plate 6.6%）；燃料成本上升已大部分透過定價轉嫁；Q2 2026 淨通膨 4.9%（Specialty 4%、CotP 6.4%）；管理層預期 2026 通膨回到 1%-4% 常態區間。","source":"MarketBeat: Chefs' Warehouse Q3 / Q2 / Q4 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/chefs-warehouse-q2-earnings-call-highlights-2026-07-29/","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 銷售 +12.9% 至 $1.17B；FY2026 指引上修至銷售 $4.5-4.6B、adjusted EBITDA $305-315M；中東物流與 Dubai/Abu Dhabi 飯店住房率下滑為近期拖累；長期目標延至 2030。","source":"Distribution Strategy Group: Chefs' Warehouse Delivers Double-Digit Sales Growth as Restaurant Demand Remains Strong","url":"https://distributionstrategy.com/2026/07/chefs-warehouse-delivers-double-digit-sales-growth-as-restaurant-demand-remains-strong/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"業界規模代理：美國 food logistics 市場 2026 約 $240.8B、年增約 4.3% 至 2031（Mordor，非 foodservice 專屬）；未找到 2026-2027 專屬 foodservice distribution TAM 預測。","source":"Mordor Intelligence: United States Food Logistics Market","url":"https://www.mordorintelligence.com/industry-reports/united-states-food-logistics-market","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Zacks：CHEF 成長動能能否延續至 2027（廣泛需求、客戶滲透、量增）","source":"Zacks","url":"https://www.zacks.com/stock/news/2986467/can-chefs-warehouses-strong-growth-momentum-continue-into-2027","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"經查 CHEF 2026 年申報文件與搜尋結果，未找到直接指名取代 CHEF 核心產品（specialty 食品配送）的替代技術；10-K 風險因素僅列一般性的資訊系統、網路安全與 AI 使用風險。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm","excerpt":"We are continuously improving our information technology solutions, resulting in a larger technological presence and corresponding increase in exposure to cybersecurity risk.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"US Foods 擴大 AI 下單（MOXē 平台）並調整銷售模式，同業以數位/AI 下單爭奪份額；屬產業內技術競爭，非取代 CHEF 產品。","source":"Distribution Strategy: US Foods Expands AI Ordering and Reshapes Sales Model in Digital Push","url":"https://distributionstrategy.com/2026/02/us-foods-expands-ai-ordering-and-reshapes-sales-model-in-digital-push/","excerpt":"in artificial intelligence and digital tools, rolling out new AI-driven ordering capabilities while overhauling its sales compensation model and expanding rapid-delivery services as part of a broader effort to drive growth and efficiency. On its fourth-quarter earnings call, executives said the company added a new feature to its MOXē digital platform that allows customers and sales","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"新創 Pepper 募得 5,000 萬美元，把 AI 與自動化帶進獨立食品配送商，稱平台服務逾 500 家配送商、年 GMV 300 億美元。","source":"Distribution Strategy: Pepper Lands $50 Million","url":"https://archive.distributionstrategy.com/2026/02/23/","excerpt":null,"as_of":"2026-02-23","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 describes the core model as chef-focused specialty foodservice distribution via 44 distribution centers; the only direct-to-consumer channel is Allen Brothers mail/e-commerce for center-of-the-plate products, and no subscription/platform shift is described.","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm","excerpt":"Additionally, we market certain of our center-of-the-plate products directly to consumers through our Allen Brothers, Inc. (“Allen Brothers”) mail and e-commerce platform.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 2026 earnings summary cites facility and route consolidation and digital platform enhancements.","source":"Quartr CHEF Q2 2026 earnings summary","url":"https://quartr.com/events/the-chefs-warehouse-inc-chef-q2-2026_ozaCz6qZ","excerpt":"Continued focus on facility and route consolidations, digital platform enhancements, and disciplined capital allocation. Updated five-year targets now extend to 2030, reflecting accelerated growth and investment cycles.","as_of":"2026-08-06","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"FY2026 初始 guidance（2026-01）淨銷售 $4.35–4.45B、調整後 EBITDA $276–286M；後續 8-K 顯示 2026 年內多次上調，未見下調。","source":"Chefs' Warehouse 8-K / barchart: The Chefs' Warehouse announces preliminary fiscal year 2026 guidance","url":"https://www.barchart.com/story/news/36995177/the-chefs-warehouse-announces-preliminary-fiscal-year-2026-guidance","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"最新一次上調的 8-K 新聞稿（檔名指向 2026-09-25 前後）：全年淨銷售 $4.56–4.61B、毛利 $1.130–1.140B。日期以檔名推估，內文未確認。","source":"SEC 8-K press release ex99.1 (Sep 2026)","url":"https://www.sec.gov/Archives/edgar/data/0001517175/000151717526000034/pressreleaseex99109252026.htm","excerpt":null,"as_of":"2026-09-25","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026（7 月底公布）調整後 EPS $0.78 對共識 $0.59；營收 $1.17B 對 $1.12B；全年銷售 guidance 上調至 $4.5–4.6B，與當時分析師共識約 $4.5B 大致相當。","source":"Benzinga / Nasdaq-Zacks: CHEF Q2 Earnings Beat Estimates","url":"https://www.nasdaq.com/articles/chef-q2-earnings-beat-estimates-volume-and-margin-gains","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 後目標價上調：UBS、Benchmark、BTIG 各 $125（Buy），Morgan Stanley $104（Equal-weight）。MarketBeat 共識 Moderate Buy、平均目標 $104.71（另一則 $107.43）。","source":"MarketBeat: Morgan Stanley increases Chefs' Warehouse price target (2026-07-30)","url":"https://www.marketbeat.com/instant-alerts/morgan-stanley-increases-chefs-warehouse-nasdaqchef-price-target-to-10400-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價各站不一：Benzinga 平均約 $92（8–11 位分析師，區間 $58–$125，部分舊目標未更新）；Tickflow（2026-07/08 初）平均 $90.50（13 位）；Investing.com 後期頁面平均 $116.56（9 位）、$122.00（含 StoneX $125，2026-09-16）。","source":"Benzinga price-targets page; Tickflow; Investing.com","url":"https://www.benzinga.com/quote/CHEF/price-targets","excerpt":null,"as_of":"2026-09-16","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Seeking Alpha 修正頁：3 筆 EPS 下修、7 筆營收上修（期間未標示）；2026-03-30 快照全年共識 EPS 2.15、營收 $4.43B（Q2 前，已舊）。","source":"Seeking Alpha CHEF earnings revisions/estimates","url":"https://seekingalpha.com/symbol/CHEF/earnings/revisions","excerpt":null,"as_of":"2026-03-30","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-15 子公司 Dairyland 與 CW Parent 簽新定期貸款協議，本金 $675M、2033-10-15 到期，SOFR+2.00%（融資事件，非併購）；同日 8-K 另含 1.02 終止重大協議、2.03、3.02 項目","source":"SEC EDGAR 8-K Item 1.01（2026-10-19）","url":"https://www.sec.gov/Archives/edgar/data/1517175/000151717526000030/chef-20261019.htm","excerpt":"The New Term Loan Facility matures on October 15, 2033 and, at the Borrowers’ option, bears interest at a rate equal to either (i) SOFR plus 2.00% per annum or (ii) the Alternate Base Rate plus 1.00% per annum.","as_of":"2026-10-19","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月8-K共8份，僅1份含重大項目（2026-10-19，1.01/1.02/2.03/3.02），無4.02（重編）、無訴訟或併購專屬項目","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001517175&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K清單無2.01（完成收購）項目；唯一重大項目為2026-10 新$675M定期貸款（融資）。搜尋未見2026年新併購，Italco收購簽於2025-10-01（窗口外）","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001517175&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K 風險因子僅提及一般性勞資類（含集體訴訟形式）訴訟風險；搜尋未見針對CHEF的證券集體訴訟","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm","excerpt":"In the ordinary course of our business, we may become involved in various legal proceedings. The outcome of these proceedings cannot be predicted.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K清單無Item 4.02（財報不可信賴/重編）；搜尋未見SEC調查","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001517175&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"CHEF","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":24.66,"operating_margin_pct":4.32,"fcf_margin_pct":4.03,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CHEF","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SYY","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":18.5,"operating_margin_pct":3.66,"fcf_margin_pct":2.29,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SYY","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"USFD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":17.55,"operating_margin_pct":3.23,"fcf_margin_pct":2.36,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.USFD","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"PFGC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":11.93,"operating_margin_pct":1.31,"fcf_margin_pct":1.5,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PFGC","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"CHEF"},"financial_history":{"ticker":"CHEF","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":2613399000.0,"revenue_yoy_pct":null,"gross_margin_pct":23.67,"operating_margin_pct":3.28,"net_income":27750000.0,"diluted_eps":0.73,"free_cash_flow":-22714000.0,"fcf_margin_pct":-0.87,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":3433763000.0,"revenue_yoy_pct":31.39,"gross_margin_pct":23.72,"operating_margin_pct":2.94,"net_income":34590000.0,"diluted_eps":0.88,"free_cash_flow":4212000.0,"fcf_margin_pct":0.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":3794212000.0,"revenue_yoy_pct":10.5,"gross_margin_pct":24.09,"operating_margin_pct":3.38,"net_income":55479000.0,"diluted_eps":1.32,"free_cash_flow":103555000.0,"fcf_margin_pct":2.73,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":4149537000.0,"revenue_yoy_pct":9.36,"gross_margin_pct":24.2,"operating_margin_pct":3.69,"net_income":72361000.0,"diluted_eps":1.68,"free_cash_flow":87793000.0,"fcf_margin_pct":2.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CHEF/CHEF_Q3_2026_Earnings_Call_20261028.md）

# Q3 2026 Earnings Call
**The Chefs' Warehouse, Inc.** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Greetings, and welcome to The Chefs' Warehouse Third Quarter 2026 Earnings Conference Call. As a reminder, this conference is being recorded.
I would now like to turn the conference over to your host, Alex Aldous, General Counsel, Corporate Secretary and Chief Government Relations Officer. Please go ahead, sir.

**Alexandros Aldous** (Executives):
Thank you, operator. Good morning, everyone. With me on today's call are Chris Pappas, Founder, Chairman and CEO; and Jim Leddy, our CFO. By now, you should have access to our third quarter 2026 earnings press release. It can also be found at www.chefswarehouse.com under the Investor Relations section.
Throughout this conference call, we will be presenting non-GAAP financial measures, including, among others, historical and estimated EBITDA and adjusted EBITDA as well as historical adjusted net income, adjusted earnings per share, adjusted operating expenses, adjusted operating expenses as a percentage of net sales and as a percentage of gross profit, net debt, net debt leverage and free cash flow.
These measures are not calculated in accordance with GAAP and may be calculated differently in similarly titled non-GAAP financial measures used by other companies. Quantitative reconciliations of our non-GAAP financial measures to their most directly comparable GAAP financial measures appear in today's press release and third quarter 2026 earnings presentation.
Before we begin our formal remarks, I need to remind everyone that part of our discussion today will include forward-looking statements, including statements regarding our estimated financial performance. Such forward-looking statements are not guarantees of future performance, and therefore, you should not put undue reliance on them. These statements are subject to numerous risks and uncertainties that could cause actual results to differ materially from what we expect. Some of these risks are mentioned in today's release. Others are discussed in our annual report on Form 10-K and quarterly reports on Form 10-Q, which are available on the SEC website.
Today, we are going to provide a business update and go over our third quarter results in detail. For a portion of our discussion this morning, we will refer to a few slides posted on the Chefs' Warehouse website under the Investor Relations section titled Third Quarter 2026 Earnings Presentation. Please note that these slides are disclosed at this time for illustration purposes only. Then we will open up the call for questions.
With that, I will turn the call over to Chris Pappas. Chris?

**Christopher Pappas** (Executives):
Thank you, Alex, and thank you all for joining our third quarter 2026 earnings call. Revenue trends display typical seasonal cadence through the third quarter of 2026, building from the summer months into September with strong year-over-year growth. Our regional Chefs' Warehouse teams delivered excellent execution across markets and product categories, driving strong growth in revenue and gross profit dollars as well as continued progress increasing relevance with our customer base with solid year-over-year growth in unique item placements and unique customers.
Momentum continued into October. And as we head into the busy holiday season, I would like to thank all our Chefs' Warehouse teams from sales, procurement and operations to all the supporting functions for their dedication and commitment to delivering a diverse, high-quality product and service in partnership with our suppliers and customers and the communities we serve.
Our Middle East operations continue to operate effectively in a challenging environment. Revenue trends in recent weeks have been approximately 100% of prior year as food away-from-home activity is supported by local residents and expatriates returning from the summer off season. Our teams in the UAE, Qatar and Oman are doing an exceptional job of executing for our customers in the region and delivering high EBITDA margin results. We remain committed to our business and customers and to the region long term.
With that, please refer to Slide 3 of the presentation. A few highlights from the third quarter include: organic net sales grew 10.3%, organic specialty sales were up 8.4% over the prior year, which was driven primarily by unique placement growth of 7.2%, specialty case growth of 6.1% and price inflation.
Unique customers grew 4.4% year-over-year. Reported unique customer growth was impacted partially by the conflict in the Middle East. Excluding this impact, third quarter unique customer growth was approximately 5.7%. Pounds in center-of-the-plate were approximately 6.6% higher than the prior year third quarter.
Gross profit margins increased approximately 84 basis points. Gross margin in the specialty category increased approximately 63 basis points as compared to the third quarter of 2025, while gross margin in the center-of-the-plate category increased approximately 137 basis points year-over-year. Jim will provide more detail on gross profit and margins in a few moments.
For an update on certain of our operating metrics, including continued improvements in year-over-year gross profit per route and adjusted EBITDA per employee, please refer to the slides provided in the appendix of our third quarter 2026 earnings presentation.
With that, I'll turn it over to Jim to discuss more detailed financial information for the quarter and an update on our liquidity. Jim?

**James Leddy** (Executives):
Thank you, Chris, and good morning, everyone. I'll now provide a comparison of our current quarter operating results versus the prior year quarter and provide an update on our balance sheet and liquidity.
Please refer to Slide #4. Our net sales for the quarter ended September 25, 2026, increased approximately 11.2% to $1.135 billion from $1.021 billion in the third quarter of 2025. The growth in net sales was a result of an increase in organic sales of approximately 10.3% as well as the contribution of sales from acquisitions, which added approximately 0.9% to sales growth for the quarter. Net inflation was 4.1% in the third quarter, consisting of 2.6% inflation in our specialty category and 6.6% inflation in our center-of-the-plate category versus the prior year quarter.
Gross profit increased 15% to $284.3 million for the third quarter of 2026 versus $247.2 million for the third quarter of 2025. Gross profit margins increased approximately 84 basis points to 25%. Selling, general and administrative expenses increased approximately 12.1% to $233.4 million for the third quarter of 2026 from $208.1 million for the third quarter of 2025. The increase was primarily due to higher costs associated with compensation and benefits, facilities and distribution to support sales growth, fuel prices as well as higher depreciation driven by facility and fleet investments.
Adjusted operating expenses increased 11% versus the prior year third quarter. And as a percentage of net sales, adjusted operating expenses were 17.8% for the third quarter of 2026. Operating income for the third quarter of 2026 was $51.5 million compared to $38.9 million for the third quarter of 2025. The increase in operating income was driven primarily by higher gross profit, partially offset by higher selling, general and administrative expenses.
Our GAAP net income was $29.6 million or $0.67 per diluted share for the third quarter of 2026 compared to net income of $19.1 million or $0.44 per diluted share for the third quarter of 2025. On a non-GAAP basis, we had adjusted EBITDA of $82.2 million for the third quarter of 2026 compared to $65.1 million for the prior year third quarter. Adjusted net income was $29.5 million or $0.66 per diluted share for the third quarter of 2026 compared to $21.5 million or $0.50 per diluted share for the prior year third quarter.
Turning to the balance sheet and an update on our liquidity. Please refer to Slide #5 and 6. At the end of the third quarter, we had total liquidity of $348.1 million, comprised of $164.7 million in cash and $183.4 million of availability under our ABL facility.
During the third quarter, we priced and allocated a new $675 million 7-year term loan and subsequently issued a redemption notice to the holders of our 2028 convertible notes. Subsequent to the third quarter close on October 15, 2026, the new term loan closed and funded concurrent with the settlement of the convertible notes. The proceeds of the new term loan were used to prepay the term loan due in 2029 and settle the principal and a portion of the premium of the convertible notes. The remainder of the premium was settled via the issuance of approximately 2.7 million shares of common stock to noteholders.
Our objectives in executing this refinancing are as follows: to address the 2028 convertible maturity and the related springing maturities on our existing term loan and our ABL facility; to maintain net debt leverage in our target 1.5 to 2.5x range; and to reduce our fully diluted share count, aligning our capital structure with our previously announced 2030 financial targets. 
As of September 25, 2026, total net debt was approximately $448.5 million, inclusive of all cash and cash equivalents and net debt to adjusted EBITDA was approximately 1.4x. By year-end 2026, we expect net debt to be in the range of $550 million to $600 million and net debt to adjusted EBITDA to be in a range of 1.7 to 2x. For the fourth quarter of 2026, we expect interest expense to be between $15.5 million and $17.5 million. Approximately $2.7 million of estimated fourth quarter interest expense is related to onetime costs associated with the debt refinancing.
We currently expect our fully diluted share count to be in the range of 43 million to 43.5 million shares for the fourth quarter of 2026. For future modeling purposes, we currently expect the fully diluted share count for 2027 to be in the range of 42 million to 43 million shares.
Please refer to Slide 7. We are raising our full year 2026 guidance as follows: we estimate net sales for the full year 2026 will be in the range of $4.56 billion to $4.61 billion, gross profit to be between $1.13 billion and $1.14 billion and adjusted EBITDA to be between $317 million and $321 million. Thank you.
And at this point, we will open it up to questions. Operator?

**Operator** (Operator):
[Operator Instructions] Our first question is from Mark Carden with UBS.

**Mark Carden** (Analysts):
So to start, you continue to generate double-digit organic sales growth with some pretty strong results across the business. Do you think this is being driven more by market share gains from your competitors or against your competitors or by continued underlying strength from your higher-income consumers just overall? So any shift on that front? That's first. And then second, are you seeing any pockets of what we'll call it relative weakness to the rest of your portfolio?

**Christopher Pappas** (Executives):
Yes. Great question. I think it's Goldilocks. I think it's coming from a little bit from everywhere. It's really good demand. We continue to take market share, and we continue to grow new categories, new territories. I think that the team is executing to the plan that we laid out for the next few years. And you're just seeing good tailwind from the consumer. A lot of new customers in all regions for all Chefs' Warehouse businesses. And I think it's just really good execution and it's what we're counting on to continue.

**Mark Carden** (Analysts):
Okay. Great. And then as a follow-up, your implied guidance for 4Q suggests a noticeable slowdown on net sales and EBITDA growth. Have you seen anything quarter-to-date that's giving you more hesitancy on any parts of the business? Or is this just a case of being prudent given the macro?

**James Leddy** (Executives):
Yes. Thanks, Mark. No, actually, the top end of our guide for Q4 implies really consistent year-over-year revenue growth. It's pretty much all organic in Q4. We lapped the Italco acquisition. That's about 50 to 80 basis points of year-over-year that evaporates just from lapping that acquisition. We have a little bit of conservatism on the Middle East. December is a very powerful tourism month in the Middle East. And so even though they're operating a little bit above 100% right now, we are putting in a little bit of conservatism. And then we have a tougher comparison, about 1% tougher comp to last year. 
So if you looked at our organic growth, the first 3 quarters of the year was about 11%, the top end of our guide implies about 10%, and it's just very consistent throughout the year and what the guide really implies given what I just kind of went through.

**Operator** (Operator):
Our next question is from Brian Harbour with Morgan Stanley.

**Hilary Lee** (Analysts):
This is Hilary Lee on for Brian Harbour. Great quarter, guys, another quarter of strong margins. So I just wanted to know if you guys could provide some color on what drove the expansion? And do you think this sort of expansion is sustainable into 4Q and 2027?

**James Leddy** (Executives):
Hilary, are you referring to gross margin...

**Hilary Lee** (Analysts):
Adjusted EBITDA.

**James Leddy** (Executives):
In adjusted EBITDA. Yes. No, I think our guidance implies a very consistent kind of above 7% type of EBITDA margin in Q4. Our full year guidance implies getting to 7%, which was our 2028 target. And we've been seeing pretty consistent growth there. As I just mentioned, there's a little bit of conservatism in the guide, but that's just mostly driven by what I kind of just discussed.

**Hilary Lee** (Analysts):
Great. And just as a follow-up, I guess, what are you guys really seeing in terms of inflation? Anything that you can provide on diesel prices rising rapidly?

**James Leddy** (Executives):
Yes. I think one thing to point out, obviously, fuel prices have rose egregiously really since March. And so if you look at our operating leverage this quarter and last quarter as a percent of revenue, you see that most of it is coming from the gross profit margin line. And the adjusted OpEx line is relatively flat versus prior year. And the main driver of that is fuel. And then you're seeing the offset in the gross profit margin line. So I would say we're passing most of it on, not all of it. You're never really going to be able to pass all of it on, but that's been the real driver of that operating leverage gap dynamic.

**Operator** (Operator):
Our next question is from Alex Slagle with Jefferies.

**Alexander Slagle** (Analysts):
I guess following up on the fuel. I don't know if inbound freight has become any more of a challenge or sort of how you're looking at that passing through? And then just looking out 2027, I don't know if there's any initial comments at a high level just to start thinking about. I mean, should we think about that overall view for '27 to 2030 on revenue, gross profit, EBITDA, is that sort of linear? Or is there something different in '27 to think about?

**James Leddy** (Executives):
Thanks, Alex. No, look, I would say on the inbound freight, I think our teams have done a really good job of kind of managing procurement and pricing very effectively in this environment of higher fuel and higher freight costs. Obviously, you see it in our gross profit dollar growth at 15% year-over-year and strong gross profit margins. So as our smaller markets and high-growth markets start to get scale and generate the benefits of that scale on the procurement side, that flows into pricing. We're leveraging our digital platform. And as I just mentioned, we're able to pass on a good portion of that fuel cost. So I think as Chris mentioned, our teams are executing at a very high level, and it's showing through in the results.

**Christopher Pappas** (Executives):
Alex, we're running the business with the outlook of if something great happens and the world is at peace and oil comes down and there's better logistics out there and all the other things that we've kind of built into the model that the world has inflated. It's moderate at this point. I mean it's up and down. Protein can always be a little tricky, can be really high one year and down the next. We're kind of seeing -- I think we only reported in specialty only about 2%, 2%, 2.5% of inflation. So we're just -- we're trying to keep costs down. Obviously, we have to be competitive, and we want our customers to be able to get the best value of what we can provide.
But I just think the new world is higher cost and you have to fight it with technology, you have to fight it with a team operating kind of like a symphony and being able to take out some costs as much as possible as we do start to leverage our new facilities. And I think you're seeing that, and it's built into our forecast to 2030. I don't think we're going to see much different. If it does, it's a plus. If we have a little headwind, I think we've built that in. So I like where we sit, and I like where the team is taking us.

**Operator** (Operator):
Our next question is from Peter Saleh with BTIG.

**Peter Saleh** (Analysts):
Congrats on another great quarter. I did want to ask, I guess, first, if you guys could give us a little bit more color on the gross margin gains that you're seeing and really some healthy gains here for the past several quarters. Just trying to understand maybe what's driving that? And how much of that is sustainable as we head into 2027?

**James Leddy** (Executives):
Yes. Alex, I'll just revert to kind of my previous comment about -- sorry, Peter, that the operating leverage as expressed as a percent of revenue could shift around quarter-to-quarter year-over-year based on market dynamics. This quarter, it happens to be that fuel prices are causing normally with 11% or 10% type of growth in revenue, you're going to see your adjusted OpEx line be lower year-over-year, but it's relatively flat really because of fuel prices and the impact on the OpEx line. And then you're seeing that offset, and that's juicing up the gross profit margin line a little bit.
But I would say what we're really seeing is product mix as our operating companies in many of our markets are becoming more of a true Chefs' Warehouse over time as we grow categories, as our sales teams become more mature and more expert and continue to drive market share. We're selling a higher mix of higher-margin products, both on the specialty side and on the protein side.
I mentioned before that we're starting to get to leverage, really leverage our scale on the procurement and pricing side. And then behind that, we have continued improvements in digital with integrating AI-type technology that's flowing through to our pricing and to our sales teams. And so it's all of those things coming together. It's not 2 home runs. It's like we like to say, it's 20 base hits and doubles, and that's really contributing to a lot of that gross profit margin improvement.

**Christopher Pappas** (Executives):
And Peter, cautiously optimistic. We like to think there's lots of buffers going forward into 2030, '31 and beyond with just the growth into the capacity we have built, we're still running many midsized small businesses. We only have 1 or 2 really sizable businesses. And as our new facilities keep coming online where we do have the space to buy direct, buy in volume, not have LTLs, all those will contribute to better top line GP, which should result in better bottom line GP and EBITDA margins.
So we kind of look at it that we could take a few hits. There could be tailwinds, but there's a lot of -- I mean, headwinds, but there's a lot of tailwinds coming with the growth of CW family of businesses as we do grow into all these new investments and we start to get the synergies and the leverage on the enormous investments we've made in the last 12 years. So very cautiously optimistic about that.

**Peter Saleh** (Analysts):
Understood. And then just can you guys give us an update, the organic growth has been double digit all year, where are we on the sales force? Has that been growing at the same rate, maybe slower? And how are you seeing hiring trends right now?

**Christopher Pappas** (Executives):
Yes. I think no change. Really, the team is executing to -- it's always been very hard to find great people to do what we do because you have to have a lot of knowledge. You have to be able to absorb all that knowledge and talk like an adviser to the best in the world. So we find good people, we hire them. We're always -- unfortunately, there is some turnover at the bottom. It's not for everybody. It's a very expensive investment to invest 2, 3 years into somebody who doesn't make it or stay.
So we do take a lot of time and care and spend the time in the hiring process. But we're hiring still as fast as possible where we could find really good people because we still can't meet the demand that -- that's coming out of a lot of our regions, the salespeople still have way too many accounts. So we see it that we can't -- we just can't hire fast enough to meet the demand that we have for our businesses.

**Operator** (Operator):
Our next question is from Kelly Bania with BMO Capital Markets.

**Kelly Bania** (Analysts):
Just wanted to follow up on the top line. You've obviously had an incredibly strong year and not to nitpick at all, but I guess some might do some math and say if CME really accelerated and the top line did moderate just a little bit, it looks like the domestic business maybe slowed a little bit. Is there anything to note from just a seasonality standpoint or customer behavior standpoint? And as well, can you talk about the visibility you have into just the holiday season and the bookings that your customers are seeing at this stage? I think you normally have some visibility into what that looks like for the fourth quarter.

**James Leddy** (Executives):
Yes. I'll start and I'll let Chris comment more if you'd like. I'll really just go back to kind of my comments earlier. While we always build a little bit of conservatism into our guidance, we did raise it fairly significantly. And it does imply -- the top end of the guidance implies very consistent year-over-year organic growth with the prior year when you factor in a tougher comp to last year, about 1% and some conservatism around December for the Middle East, just given that there's still a lot of unknowns there.
So I don't -- there's nothing in the guidance change that we really need to expect to call out. We're not -- I would say that revenue trends, as we said in our prepared remarks, continued into October. We saw a really good October, double-digit growth consistent with what we've been seeing all year.
So I'll just -- I'll let Chris comment on the -- what we expect for the fourth quarter, but that's really what we have.

**Christopher Pappas** (Executives):
Yes. I mean, basically, Kelly, what we're hearing from all our sales meetings and obviously looking at the numbers, there's a lot of demand in the fourth quarter of private events, corporate events, celebrations. So it's really healthy at the top. Any negative that I could hear is certain conferences have 10%, 12% less people attending. I don't think that's a surprise to anybody. And from a lot of our private club businesses, what I may be hearing is the summer was a little up and down. A lot of people were traveling, but à la carte could be a little soft, but the private events are more than making up their top line -- bottom line for their budget. So it seems like a little bit goes down and then a little bit goes up.
And from our seat, we see in our forecast, obviously, we'd like to be conservative, but we don't see anything -- we've taken up guidance. So there's a little -- I think the -- the black box will tell you there's a little slowness here and there in some customer bases. And I'm sure that's true, but our investment really to grow the sales force, grow territory and categories was always designed to make up any downturn in the typical customer base and make it up by having more and more customers. We look at it again as how much -- how many dollars -- how many GP dollars can we get on trucks and fill those routes. And that's the way we run the business, and it's working pretty well.

**Kelly Bania** (Analysts):
Okay. Just had one more follow-up. Some in the industry are calling for some sizable savings from AI. Obviously, Chefs' has been at the forefront, and you've outlined many areas from pricing to sourcing, logistics, inventory that you are working on projects there. But just any -- just curious if there's any update on the size of the potential savings as you continue to work through that and feedback from the sales force as they continue to get more tools on that front?

**Christopher Pappas** (Executives):
Yes. I mean great question. We're all in on the investment. It's part of our budget to continue to invest in digital and have the best AI tools for our teams. My 20/20 vision still thinks that it's going to continue to make the sales force at every department more effective. I'm not ready to give up on people. I think people play a really important part of what we do and how we do it. But we've always been on the mindset that you're going to have to do more with less, just from the point that there's just not enough people. The birth rates aren't what they used to be across the world. So you're going to have to use AI in every piece of technology to drive your bottom line.
And I think it's an upside for us. I mean we're going to be conservative and say that our forecast that we gave you is not built with any big ahas, but would we love to see an aha? Absolutely. Can you -- if we get another point or 2 points to the bottom line because we're able to be that much more efficient, that would be truly incredible. But I think we're satisfied really with what our forecast looks like going into 2030. And just hitting that, I think it'd be a tremendous reward for shareholders.

**Operator** (Operator):
Our next question is from Todd Brooks with StoneX.

**Todd Brooks** (Analysts):
Congrats on the continued momentum in the quarter as well. Two quick questions. One, Jim, if you look at kind of where we stand in the year and the full year guidance, what inflation outlook is embedded in the Q4 guidance for specialty and center-of-the-plate?

**James Leddy** (Executives):
Nothing really out of the ordinary from what we've been seeing, Todd. Price inflation throughout the year has been pretty consistently kind of at the upper end of what we would consider the normal range of 2% to 4%. If you exclude the kind of extreme price inflation we're seeing in the Middle East, our aggregate price inflation in the quarter was closer to 3.5%. As Chris mentioned earlier, specialty was really 2.5%. So we're just assuming consistent kind of inflation through the remainder of the year. We don't expect anything other than you have a few categories that are always a little bit higher, a little bit lower, but that's normal.

**Todd Brooks** (Analysts):
Okay. Great. And then my second and final question. If we're looking out now '27, '28, how has the new facility plan shaped up? What facilities are on the come? And have you had any success? I know it's kind of a holy grail, but finding any sort of opportunity for a second facility in the New York metro market.

**James Leddy** (Executives):
Yes. Thanks, Todd. We kind of laid out at our -- when we put out our 2030 guidance kind of the markets that we'll be adding distribution capacity and consolidating facilities. We're -- many of them are in process right now, and they'll come online over the next 2, 3 years. And that's Texas to consolidate facilities in Dallas and build a state-of-the-art distribution center. New England is underway to do consolidations, add capacity. We're in the process of expanding Las Vegas, our protein processing. And then there's a couple of markets in the Midwest that are underway as well. Those are really our focus right now. And then we are working on New York. There's multiple scenarios. Nothing to announce right now.

**Operator** (Operator):
We have reached the end of the question-and-answer session. I'd like to turn the floor back over to Chris Pappas for closing comments.

**Christopher Pappas** (Executives):
Well, thank you all for joining our third quarter earnings call. It was a very strong quarter. The team continues to execute. We couldn't be more proud of how the team continues to drive forward The Chefs' Warehouse and the passion they have for selling the world's finest ingredients to the best chefs in the world. We look forward to you joining us again on our fourth quarter call. Thank you very much.

**Operator** (Operator):
This concludes today's teleconference. You may disconnect your lines at this time. Thank you for your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CHEF_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：CFO 上調 2026 全年財測，營收區間 45–46 億美元（原話："will be in the range of $4.5 billion to $4.6 billion"）
- 2026-07-29｜CFO｜guidance：全年調整後 EBITDA 財測下緣 3.05 億美元（上緣 3.15 億，毛利 11.02–11.25 億）（原話："adjusted EBITDA to be between $305 million"）
- 2026-07-29｜CEO｜guidance：CEO 表示 7 月延續動能，預期第三季開季為雙位數營收成長（原話："expect double-digit top line growth to start the third quarter."）
- 2026-07-29｜CFO｜guidance：CFO 說明財測納入保守假設，原因是中東夏季旅遊基期與第四季旅遊回流不確定（原話："we did build in some conservatism into the forward guidance"）
- 2026-07-29｜CFO｜guidance：CFO 說明下半年營收成長較慢的原因之一：第四季將滿一年的 Atelco 收購貢獻約 70bp（原話："fourth quarter, and that's about 70 basis points of year-over-year growth."）
- 2026-07-29｜CFO｜guidance：CFO 說財測燃料假設是沿用現況，不假設明顯升降（原話："Pretty conservative assumption. We just modeled forward kind of what we're experiencing now,"）
- 2026-07-29｜CEO｜guidance：2030 長期目標：營收 60–65 億美元（年增 7–10%）（原話："full year 2030 revenue of $6 billion to $6.5 billion"）
- 2026-07-29｜CEO｜guidance：2030 長期目標：調整後 EBITDA 4.5–5.2 億美元（原話："Adjusted EBITDA of $450 million to $520 million,"）
- 2026-07-29｜CEO｜margin：2030 長期目標：調整後 EBITDA margin 7.5–8%（原話："adjusted EBITDA margin of 7.5% to 8%."）
- 2026-07-29｜CFO｜margin：CFO 說明長期成長率目標已按近幾季表現做風險調整（原 4–7% 上調至 7–10%）（原話："It is risk-adjusted to what we're doing the last couple of quarters."）
- 2026-07-29｜CFO｜margin：CFO 說明全年財測隱含調整後 EBITDA margin 6.8%（原話："the full year guidance implies now 6.8% adjusted EBITDA margin."）
- 2026-07-29｜CFO｜margin：CFO 說明財測相當於 Q1 與 Q2 兩次上調合併為一次（原話："So it's really kind of 2 raises at once"）
- 2026-07-29｜CFO｜margin：CFO 提供 Q2 EBITDA margin 年增幅度（原話："Our EBITDA margin was up 120 basis points year-over-year."）
- 2026-07-29｜CEO｜margin：CEO 報告 Q2 毛利率年增約 49bp（特產 47bp、肉類 75bp）（原話："Gross profit margins increased approximately 49 basis points."）
- 2026-07-29｜CFO｜margin：CFO 報告 Q2 調整後營業費用占營收比例（原話："adjusted operating expenses were 17.5% for the second quarter of 2026."）
- 2026-07-29｜CEO｜margin：CEO 回答毛利與費用端的後續空間：兩邊都有，強調從投資中取得槓桿（原話："You're correct. All of the above."）
- 2026-07-29｜CEO｜margin：CEO 表示不為 EBITDA 率設上限（原話："teams that I'm not capping where the EBITDA can go percentage-wise."）
- 2026-07-29｜CFO｜margin：CFO 把毛利率改善歸因於定價、採購團隊與科技投資（原話："we've made a ton of investment in our pricing teams and technology"）
- 2026-07-29｜CFO｜margin：CFO 說明德州去除低毛利非核心客戶後，德州 EBITDA margin 較前幾年大幅提升（原話："We've improved our overall Texas EBITDA margin by multiple hundred basis points"）
- 2026-07-29｜CEO｜margin：數字口徑：CEO 報告 Q2 有機淨銷售成長（原話："organic net sales grew 12.2%."）
- 2026-07-29｜CFO｜margin：數字口徑：CFO 拆解 Q2 通膨 4.9%（特產 4%、肉類 6.4%）（原話："inflation was 4.9% in the second quarter, consisting"）
- 2026-07-29｜CEO｜customer：數字口徑：Q2 獨立客戶數成長 3.6%，管理層另提排除中東影響後約 4.9%（原話："Unique customers grew 3.6% year-over-year."）
- 2026-07-29｜CEO｜customer：中東業務 5–6 月約為去年同期 94%，近週大致持平（原話："located there operated at approximately 94% of prior year"）
- 2026-07-29｜CFO｜customer：CFO 回答客戶流失率：與過去相比無重大變化（原話："We see a pretty consistent attrition rate in this industry"）
- 2026-07-29｜CFO｜customer：CFO 說明德州低毛利非核心大客戶專案已滿一年，德州業務成長（原話："Our Texas business is growing really nicely."）
- 2026-07-29｜CEO｜customer：CEO 表示世界盃對公司沒有明顯影響（原話："The World Cup, we don't think had a major impact for us."）
- 2026-07-29｜CFO｜competition：CFO 承認競爭激烈，並強調關係與人才難以複製（原話："There's plenty of competition. I mean we fight every day."）
- 2026-07-29｜CFO｜competition：CFO 說明護城河中人員能力不可被電腦取代（原話："You can't just rely on computers."）
- 2026-07-29｜CEO｜product：CEO 談 AI 投資：管理層預期不是一次性大幅提升利潤（原話："expecting to get 5, 6 points to the bottom line"）
- 2026-07-29｜CEO｜product：CEO 表示公司過去未稱之為 AI，但一直投資科技（原話："We never called it AI, but we've always been investing"）
- 2026-07-29｜CFO｜risk：CFO 說明供應鏈：中東物流需改道、前置時間拉長、價格上升，北美採購未受影響（原話："we haven't seen an impact on our sourcing into North America."）
- 2026-07-29｜CFO｜risk：CFO 說明生鮮通膨主要來自物流與燃料成本，財測未假設不同於近期（原話："Still a small division."）
- 2026-07-29｜CFO｜capital_allocation：CFO：資本支出長期平均約占營收 1%（原話："We expect total Capex to average approximately 1% of revenue going forward"）
- 2026-07-29｜CFO｜capital_allocation：CFO：將增加庫藏股（原話："maintain a strong balance sheet and increase share repurchases."）
- 2026-07-29｜CFO｜capital_allocation：CFO：槓桿在目標區間（淨負債／調整後 EBITDA 1.5–2.5）內時，配置更多金額給買回（原話："we expect to allocate more dollars to share repurchases"）
- 2026-07-29｜CFO｜capital_allocation：CFO：自由現金流轉換率目標 40–60% 調整後 EBITDA（原話："we expect free cash flow conversion to be in the range of 40% to"）
- 2026-07-29｜CFO｜capital_allocation：CFO 報告 Q2 償還 ABL 並降低未償餘額（原話："ABL debt, reducing the outstanding drawn balance to $70 million."）
- 2026-07-29｜CFO｜capital_allocation：CFO 對併購環境的看法：標的價格偏熱，偏好投資人才而非收購（原話："I think it's getting frothier and frothier."）
- 2026-07-29｜CFO｜capital_allocation：CFO 稱有機成長 ROI 優於多數正在評估的收購案（原話："keep investing in people. and just keep adding talent"）
- 2026-07-29｜CEO｜commitment：CEO 承諾持續投資配送能力，列出擴建區域（原話："Current plans include New England, Texas, Las Vegas, the"）
- 2026-07-29｜CEO｜commitment：CEO 指示持續招聘有潛力人才（原話："if you find a great talent with potential hire them."）
- 2026-07-29｜CFO｜commitment：CFO 表示財測傾向保守、仍有超越空間（原話："we tend to be a little bit conservative on"）

### 問答異常語氣（迴避／改口／保留）
- CHEF_Q2_2026_Earnings_Call_20260729.md｜問：Todd Brooks（Benchmark）：EBITDA margin 從今年約 6 高段走向 7 高段，進展是階梯式還是每年 20–25bp？｜答法：CFO 未給逐年節奏，改談財測與 5 年目標皆經風險調整、有上檔可能，並稱「you never know what the cadence is going to be exactly」；CEO 改談歷史 10% 以上 EBITDA 與不設上限
- CHEF_Q2_2026_Earnings_Call_20260729.md｜問：Kelly Bania（BMO）：若下半年營收維持雙位數，EBITDA 上檔空間多大？｜答法：CFO 先釐清問的是毛利率或 EBITDA margin、一度答錯題目（以為問 Q2），最後只答「is there upside from there? Sure」，未給數字，並重申傾向保守

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
{"date":"20260518","verdict":"衛星候選 — Specialty B2B 食材分銷利基龍頭，Q1 FY26 organic +10.4% 連續第 4 季雙位數，但 Fwd PE 30.74x 溢價同業 128% 已透支；建議等回測 W52 $64 或 Sysco-Restaurant Depot 整合落地 (FY27Q1-Q2) 後再評估進場","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Specialty 食材分銷利基護城河有效保護 CHEF 對抗 Sysco-Restaurant Depot 為首的大眾化擴張","columns":{"2Y 驗證點":"Organic growth 維持 ≥ 8%","5Y 驗證點":"Adj EBITDA margin 達 6.5-7.0% 區間（不被產品 mix 稀釋）","10Y 驗證點":"市佔在 specialty 利基保持 8-12%（不被中型分銷商整合擠出）","數字門檻":"FY26-28 Organic growth ≥ 8%；FY28 Adj EBITDA margin ≥ 6.5%","信息來源":"公司 2028 EBITDA 目標 $300-350M（投資人 Day）+ Q1 FY26 法說 organic +10.4%","漂移觸發條件":"連 2 季 TTM organic"}},{"id":"H2","text":"Adj EBITDA margin 擴張 + 槓桿下降兌現「成長 + 去槓桿」雙引擎","columns":{"2Y 驗證點":"Adj EBITDA margin YoY 擴張 ≥ 30bps/年","5Y 驗證點":"Net Debt/EBITDA 維持 ≤ 2.0x","10Y 驗證點":"FCF/NI 維持 ≥ 0.8（不再 lumpy）","數字門檻":"FY26 Adj EBITDA $276-286M（公司指引）；FY28 6.5-7.0% margin","信息來源":"Q1 FY26 法說 Adj EBITDA $60.1M（+27% YoY）+ Net Debt 從 2.5x → 2.1x","漂移觸發條件":"連 4 季 TTM Adj EBITDA margin 擴張"}},{"id":"H3","text":"估值「合理」前提下，PE 透過 EPS 成長消化（並非要求倍數擴張）","columns":{"2Y 驗證點":"Fwd PE 不大幅收斂至","5Y 驗證點":"5Y EPS CAGR 17%+ 兌現 → 終端 PE 22-25x 可消化","10Y 驗證點":"同業 PE 不大幅追趕（Sysco/PFG Fwd PE 維持 14-18x 區間）","數字門檻":"Fwd PE 維持 25-35x；FY30E EPS ≥ $3.50","信息來源":"5Y Forward PE 中位 ~32x（Macrotrends）+ §13.4 同業比較","漂移觸發條件":"Fwd PE 連 4 季"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Sysco-Restaurant Depot $29.1B 併購完成後（FY26H2），Sysco 開 125+ 新 Restaurant Depot 倉，CHEF 高端小餐廳客戶部分轉自取採購 → organic growth 結構性失速","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Organic growth TTM、Top-100 餐廳客戶留存率","警戒閾值":"連 2 季 organic"}},{"id":"R2","text":"整合風險：Hardies / Greenleaf / Cambridge 3 件 specialty produce + meat 收購整合 synergy 不及預期，Adj EBITDA margin 擴張軌跡偏離 30bps/年","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Adj EBITDA margin YoY、整合 synergy 揭露","警戒閾值":"連 4 季 margin 擴張"}},{"id":"R3","text":"結構性高端餐飲萎縮：GLP-1 減重藥導致美國高端餐飲消費長期下降 + 餐廳業進入 5-10 年成熟期 → CHEF TAM 增長放緩至 3-4%（vs 目前 6-8%）","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"美國餐飲業增長率、客單價趨勢、高端餐廳開店速度","警戒閾值":"跨 2 年 organic growth 持續"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":80.34,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CHEF_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
