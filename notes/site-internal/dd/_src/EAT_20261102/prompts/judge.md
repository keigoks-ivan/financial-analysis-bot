你是 stock-analyst **v20 判斷 agent**，標的 EAT（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"EAT","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EAT_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EAT_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenues_gaap","label":"Total revenues (GAAP)","value":1475.6,"period":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","citation":"公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm"},"note":"未查得共識，省略比較"},{"id":"f_kpi1_operating_income_gaap","label":"Operating income (GAAP)","value":151.0,"period":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","citation":"公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm"},"note":"未查得共識，省略比較"},{"id":"f_kpi2_operating_margin_excl_ot","label":"Operating margin excl. other gains & charges（衍生值：GAAP OI 151.0＋other gains and charges 2.4＝153.4，/1,475.6）","value":10.4,"period":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","citation":"公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm"},"note":"未查得共識，省略比較"},{"id":"f_kpi3_restaurant_operating_mar","label":"Restaurant operating margin (non-GAAP)","value":17.7,"period":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","citation":"公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm"},"note":"未查得共識，省略比較"},{"id":"f_kpi4_adjusted_diluted_eps_non","label":"Adjusted diluted EPS (non-GAAP, excl. special items)","value":2.77,"period":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","unit":"US$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","citation":"公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm"},"note":"未查得共識，省略比較"},{"id":"f_kpi5_free_cash_flow_non_gaap","label":"Free cash flow (non-GAAP)","value":105.7,"period":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","citation":"公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm"},"note":"未查得共識，省略比較"},{"id":"f_kpi6_stock_based_compensation","label":"Stock-based compensation（占 GAAP 營業利益 5.5%、占營收 0.56%）","value":8.3,"period":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","citation":"公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm"},"note":"未查得共識，省略比較"},{"id":"f_kpi7_comparable_restaurant_sa","label":"Comparable restaurant sales — Brinker／Chili's","value":9.1,"period":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","citation":"公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm"},"note":"未查得共識，省略比較"},{"id":"f_kpi8_guidance_fy2027_total_re","label":"Guidance FY2027 total revenues","value":"6230～6330","period":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","citation":"公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm"},"note":"未查得共識，省略比較"},{"id":"f_kpi9_guidance_fy2027_adjusted","label":"Guidance FY2027 adjusted EPS (non-GAAP)","value":"13.3～13.9","period":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","unit":"US$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）","citation":"公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm"},"note":"dd_numbers_extra consensus_revision：FY1 13.68（2026-10-31 快照，已含財報後修正）；指引中點 13.60"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_eat_gross_margin_pct","label":"EAT 毛利率","value":19.14,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EAT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eat_operating_margin_pct","label":"EAT 營業利益率","value":11.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EAT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_eat_fcf_margin_pct","label":"EAT FCF 利潤率","value":11.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EAT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mcd_gross_margin_pct","label":"MCD 毛利率","value":57.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mcd_operating_margin_pct","label":"MCD 營業利益率","value":45.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mcd_fcf_margin_pct","label":"MCD FCF 利潤率","value":28.02,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_txrh_gross_margin_pct","label":"TXRH 毛利率","value":15.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXRH.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_txrh_operating_margin_pct","label":"TXRH 營業利益率","value":7.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXRH.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_txrh_fcf_margin_pct","label":"TXRH FCF 利潤率","value":6.43,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXRH.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dri_gross_margin_pct","label":"DRI 毛利率","value":21.66,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DRI.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dri_operating_margin_pct","label":"DRI 營業利益率","value":12.18,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DRI.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dri_fcf_margin_pct","label":"DRI FCF 利潤率","value":7.64,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DRI.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cmg_gross_margin_pct","label":"CMG 毛利率","value":23.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMG.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cmg_operating_margin_pct","label":"CMG 營業利益率","value":14.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMG.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cmg_fcf_margin_pct","label":"CMG FCF 利潤率","value":11.88,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMG.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":212.18,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":43.23,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":56.61,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.22,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.65 → 13.68）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.61,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（14.71 → 14.8）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":1.79,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.16 → 16.45）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":13.68,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":14.8,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":16.45,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":27.14,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 10.76 → 13.68（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":18.71,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝45.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":45.9,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.49,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝93.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":93.6,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.78,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝90.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":90.1,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":15.51,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 13.68，分子＝快照價 212.18","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1768.4,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 1799.1、現金 30.7（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":41.54,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":10582.93,"period":"2026-11-02","unit":"USD m","basis":"市值 8814.53 ＋ 淨負債 1768.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6308.76,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":6494.11,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.68,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 212.18 / W52 167.86 / W104 157.58 / W250 90.31 / W250 13週斜率 2.94%"},{"id":"f_ma_w52","label":"52 週均線","value":167.86,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":157.58,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":90.31,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.94,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K FY2026 風險因子：休閒餐飲整體近年客流無顯著成長，EAT 要成長客流須靠提高休閒餐飲板塊內市占；另面對速食、快休閒、雜貨熟食及外送/餐盒業者競爭。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/703351/000070335126000029/eat-20260624.htm","excerpt":"The casual dining segment of the restaurant industry has not seen significant growth in customer traffic in recent years. If these trends continue, our ability to grow customer traffic at our restaurants (including through off-premise) will depend on our ability to increase our market share within the casual dining segment.","as_of":"2026-08-19","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Chili's 同店銷售與客流超越休閒餐飲產業，持續搶份額（管理層框架）","source":"Zacks EAT report","url":"https://advisortools.zacks.com/proxy/ResearchReport/EAT/report?d=20251216","excerpt":null,"as_of":"2025-12-16","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"FY26 Q3 Chili's 同店+4%、超越產業420bps，但受風暴影響客流-1.2%；Maggiano's 拖累","source":"VectorShift EAT 2026 Q3 summary","url":"https://vectorshift.ai/research/companies/brinker-international/earnings/2026-q3-summary","excerpt":"quarter of same-store sales growth and outpaced the casual dining industry by 420 basis points. While our competitors ramp up limited time offers, we spent the quarter investing time in operations, training, and culinary resources into everyday capability that more closely correlates with long-term sustainable traffic growth.","as_of":"2026-04-29","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Black Box：休閒餐飲自2022年以來淨店數 -3.3%，同期速食 +5.8%、快休閒 +15.5%；約9%全服務餐廳2026有倒閉風險（供給收縮、非緊缺）","source":"Black Box Intelligence / Restaurant Dive","url":"https://www.restaurantdive.com/news/black-box-intelligence-data-restaurant-closures-2026/814042/","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Brinker FY27 Q1：Chili's可比銷售 +10.1%、客流 +6.4%、價格 +3.7%；全年EPS指引上調至$13.30–13.90；FY27含第53週（約$0.70 EPS），不會重複","source":"Brinker FY27 Q1 press release (franchising.com) / Zacks","url":"https://www.franchising.com/news/20261028_brinker_international_reports_first_quarter_fiscal_2027_results_and_updates.html","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Maggiano's FY26可比銷售 -3.9%、客流 -9.3%（集團內弱項）","source":"Brinker earnings coverage (Zacks/Nasdaq)","url":"https://www.nasdaq.com/articles/brinker-international-q4-earnings-call-highlights","excerpt":null,"as_of":"2026-08-12","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"NRA中期更新：2026經通膨調整餐飲銷售成長預測由1.3%下調至0.8%（油價>$4拖累）；未見官方2027/2028銷售預測；2027僅有總經GDP +2.5%","source":"National Restaurant Association midyear update","url":"https://restaurant.org/research-and-media/research/restaurant-economic-insights/analysis-commentary/restaurants-remain-resilient-despite-challenging-business-conditions/","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Black Box 2027預測：銷售溫和成長、客流大致持平；休閒餐飲因速食漲價縮小價差而受惠於價值定位","source":"Black Box Intelligence Q3 2026 webinar / Modern Restaurant Management","url":"https://blackboxintelligence.com/event/webinar-state-of-the-restaurant-industry-q3-2026/","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261102","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因素僅列一般性的特許經營法規與國際反壟斷等合規義務，未指稱有進行中的反壟斷調查；三次搜尋亦未見 2026 年 DOJ／FTC／EU 對 Brinker 的調查報導","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/703351/000070335126000029/eat-20260624.htm","excerpt":"These include antitrust and tax requirements, anti-boycott regulations, import/export/customs and other international trade regulations, the USA Patriot Act and the Foreign Corrupt Practices Act. Failure to comply with any such legal requirements could subject us to monetary liabilities and other sanctions, which could adversely impact our business and financial performance.","as_of":"2026-08-19","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"2026-09 季度 10-Q 稱風險因素自 FY2026 10-K 後無重大變動","source":"SEC EDGAR 10-Q（季度結束 2026-09-23）","url":"https://www.sec.gov/Archives/edgar/data/0000703351/000070335126000040/eat-20260923.htm","excerpt":"There have been no material changes in the risk factors set forth in Part I, Item 1A","as_of":"2026-09-23","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"EAT 10-K FY2026 風險因子：美國或全球貿易政策變動（如新增或加徵食品／進口品關稅）可能持續推高成本、擾亂供應，並限制以定價保護利潤率的能力。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/703351/000070335126000029/eat-20260624.htm","excerpt":"Changes in U.S. or global trade policy, such as new or increased tariffs on certain food products or other imported goods could continue to elevate costs, disrupt supply availability, and constrain our ability to protect operating margins through pricing strategies or adjustments in purchasing practices.","as_of":"2026-08-19","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"EAT 10-K FY2026 MD&A：地緣緊張與總體壓力導致產品成本通膨（含關稅）與供應鏈中斷。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/703351/000070335126000029/eat-20260624.htm","excerpt":"Geopolitical tensions and broader macroeconomic pressures have led, and in the future may lead, to wage inflation, staffing challenges, product cost inflation (inclusive of tariffs), and/or supply chain disruptions.","as_of":"2026-08-19","retrieved_at":"20261102","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"搜尋摘要：Q2 FY2026 財報電話會議稱，因家禽與乳製品價格下降及巴西牛肉關稅減免，全年商品通膨維持低個位數，下半年預期中個位數。","source":"AOL, Brinker EAT Q2 2026 Earnings Call Transcript（搜尋摘要）","url":"https://www.aol.com/articles/brinker-eat-q2-2026-earnings-170450015.html","excerpt":null,"as_of":"2026-01-28","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K 風險因子：貿易政策變動（如對某些食品或進口商品新增或加徵關稅）可能推高成本、干擾供應；未能有效管理供應鏈風險會增加成本或減少營收。未見單一地緣區域或單點供應商集中度的量化揭露。","source":"Brinker International Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000703351/000070335126000029/eat-20260624.htm","excerpt":"Changes in U.S. or global trade policy, such as new or increased tariffs on certain food products or other imported goods could continue to elevate costs, disrupt supply availability","as_of":"2026-06-24","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Chili's 2026Q1(FY27 Q1) 可比店銷售 +10.1%，客流 +6%；FY27 指引營收 $6.15–6.27B、調整後 EPS $12.60–13.40，預期定價落在 3–5% 區間低端","source":"Brinker Q1 FY27 earnings release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0000703351/000070335126000036/fy27q1ex991-earningsrelease.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"Maggiano's FY2026 可比店銷售 -3.9%、客流 -9.3%；Q2 FY26 Maggiano's 可比 -2.4% 對 Chili's +8.6%，公司稱因客流下降","source":"Brinker FY2026 results / Q2 FY26 release (franchising.com) 及 Q1 FY27 摘要","url":"https://www.franchising.com/news/20260128_brinker_international_reports_second_quarter_of_fiscal_2026_results_and_upd.html","excerpt":null,"as_of":"2026-01-28","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Black Box Intelligence Q3 2026 預期 2027 產業銷售小幅成長、客流大致持平；Fitch 預期 2026 餐飲低個位數成長，休閒餐飲客流表現優於整體","source":"Black Box Intelligence webinar Q3 2026; NRN Fitch Ratings","url":"https://blackboxintelligence.com/event/webinar-state-of-the-restaurant-industry-q3-2026/","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261102","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#none","axis":"substitute_technology","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY26 Q4 財報電話會議摘要：off-premise 約占業務 25%，管理層列為改善 app 速度、取餐便利與訂單正確性的項目","source":"Nasdaq - Brinker International Q4 Earnings Call Highlights","url":"https://www.nasdaq.com/articles/brinker-international-q4-earnings-call-highlights","excerpt":null,"as_of":"2026-08-12","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Brinker 於 2026-10-28 隨 FQ1'27 財報上調 FY2027 指引：營收 $6.23–6.33B（前 $6.15–6.27B）、調整後 EPS $13.30–13.90（前 $12.60–13.40）；53 週效應約 +2.0% 營收、+$0.70 EPS。","source":"franchising.com — Brinker International Reports First Quarter Fiscal 2027 Results and Updates Fiscal 2027 Guidance","url":"https://www.franchising.com/news/20261028_brinker_international_reports_first_quarter_fiscal_2027_results_and_updates.html","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"TIKR 稱新指引中位 $13.60 高於分析師預期 $13.28，股價當日約漲 13%；Earnings Whispers 則稱上調與市場預期一致（兩來源口徑不同）。","source":"TIKR — Brinker Soars 13% on Guidance Raise; Earnings Whispers","url":"https://www.tikr.com/blog/brinker-soars-13-on-guidance-raise-as-chilis-flywheel-of-sustainable-growth-keeps-spinning","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill：FY2027 EPS 共識 $13.39（24 位分析師，2026-10-17），3 個月內上修約 6.00%；Q1 預估 EPS $2.44、營收 $1.465B。","source":"Chartmill — EAT Earnings & Revenue Estimates, Forecasts & Revisions","url":"https://www.chartmill.com/stock/quote/EAT/estimates","excerpt":null,"as_of":"2026-10-17","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FMP：Jefferies 於 2026-10-14 設目標價 $255；過去一年更新之券商平均目標價 $243.38，24 家中 17 買進、2 強買、5 持有（Moderate Buy）。","source":"Financial Modeling Prep — Brinker International (NYSE:EAT) Stock Gains Momentum with Strong Analyst Ratings","url":"https://site.financialmodelingprep.com/market-news/brinker-international-eat-stock-analyst-ratings","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布隨時間差異大：Walnut 2026-08 均值 $198.67/中位 $204（21 位）；MarketBeat 2026-07 末均值 $191.20（22 位）；Benzinga 價目頁 8/28 為 $232（21 位）。口徑與日期不一。","source":"Walnut Invest; MarketBeat; Benzinga","url":"https://walnutinvest.com/stocks/eat/forecast","excerpt":null,"as_of":"2026-08-28","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY2027 指引上調與 53 週貢獻","source":"Zacks — EAT's Fiscal 2027 Guidance Gets a Boost from the 53rd Operating Week","url":"https://www.zacks.com/stock/news/2975243/eats-fiscal-2027-guidance-gets-a-boost-from-the-53rd-operating-week","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月8-K共8份，含重大項目者2份（8.01：新增$718.0M庫藏股授權、贖回8.250%優先票據）；無併購合併、重編（4.02）項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000703351&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"董事會2026-08-10授權再增$718.0M庫藏股，總可用授權$750.0M。","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/703351/000070335126000026/eat-20260810.htm","excerpt":"the Board of Directors of the Company authorized the repurchase of up to an additional $718.0 million in shares of the Company’s common stock under the Company’s share repurchase program (the “Repurchase Program”), allowing for a total available authority of $750.0 million under the Repurchase Program.","as_of":"2026-08-12","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06-16發出贖回通知，全數贖回2030到期8.250%優先票據，贖回價104.125%。","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/703351/000070335126000022/eat-20260616.htm","excerpt":"On June 16, 2026, Brinker International, Inc. issued a notice of redemption for all of its outstanding 8.250% Senior Notes due July 15, 2030 (the “Notes”).","as_of":"2026-06-17","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"Brinker 同意向加盟商收購阿拉巴馬與密西西比12家Chili's餐廳（預計2026年8月底交割），含6處不動產。","source":"SEC 8-K FY26Q4 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000703351/000070335126000026/fy26q4ex991-earningsrelease.htm","excerpt":"During the fourth quarter of fiscal 2026, the Company executed an agreement with a franchisee for the acquisition of 12 Chili’s restaurants located in Alabama and Mississippi, including the real estate for six of the locations, and the transaction is expected to close on August 27, 2026.","as_of":"2026-08-12","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"turnaround_catalyst_timeline#0","axis":"turnaround_catalyst_timeline","section":"coverage","direction":"0","claim":"FY2026 10-K: 6/1/2026 簽約收購 Alabama/Mississippi 加盟商 12 家 Chili's（含 6 處不動產），預計 2026-08-27 交割，價約 $27.5M；搜尋未見 2026 重整計畫或品牌處分","source":"Brinker FY2026 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000703351/000070335126000029/eat-20260624.htm","excerpt":null,"as_of":"2026-08-12","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"turnaround_catalyst_timeline#1","axis":"turnaround_catalyst_timeline","section":"coverage","direction":"+","claim":"Q1 FY2027 10-Q（2026-09-23）顯示 8.25% 票據歸零、循環信貸餘額 $375.0M、長期債務合計 $484.8M；次級來源稱 $350M 8.25% 票據於 2026-07-15 贖回（未經 SEC 原文核對）","source":"Brinker Form 10-Q period ending 2026-09-23 (SEC); panabee.com","url":"https://www.sec.gov/Archives/edgar/data/0000703351/000070335126000040/eat-20260923.htm","excerpt":null,"as_of":"2026-09-23","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"turnaround_liquidation_floor#0","axis":"turnaround_liquidation_floor","section":"coverage","direction":"+","claim":"FY2026 10-K：FY2024–FY2026 無商譽減損；商譽約 $194.5M（2026-06-24）。其他減損列在 Other (gains) and charges（Note 13），金額未讀到。","source":"Brinker 10-K FY2026 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0000703351/000070335126000029/eat-20260624.htm","excerpt":"There have been noimpairments of Goodwill for the fiscal years ended June 24, 2026, June 25, 2025 and June 26, 2024.","as_of":"2026-08-12","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"turnaround_liquidation_floor#1","axis":"turnaround_liquidation_floor","section":"coverage","direction":"0","claim":"FY2026 年底資產負債表：總資產約 $2.8B、權益約 $443.7M、遞延稅資產約 $634.5M、商譽約 $194.5M（聚合站）","source":"OpenCapital Q4 2026 earnings","url":"https://www.opencapital.sh/stocks/eat/earnings/q4-2026","excerpt":null,"as_of":"2026-08-12","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K無1.01/2.01等併購類重大項目；搜尋亦未見合併，僅有小型加盟店收購（見coverage clues）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000703351&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K風險因素僅泛稱可能遭證券集體訴訟，未載明已發生；搜尋未見近12個月證券集體訴訟。","source":"SEC 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/703351/000070335126000029/eat-20260624.htm","excerpt":"Following periods of volatility in the market price of a company’s securities, it is not uncommon for securities class action litigation to be brought against a company.","as_of":"2026-08-19","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"因轉租承租人未付租金，公司被通知違約並列為訴訟當事人；FY2026未認列費用，FY2025 $1.7M、FY2024 $0.8M。","source":"SEC 10-K FY2026 Item 8","url":"https://www.sec.gov/Archives/edgar/data/703351/000070335126000029/eat-20260624.htm","excerpt":"We recorded no charge related to these leases and lawsuits in fiscal 2026 and recorded charges of $1.7 million and $0.8 million in fiscal 2025 and fiscal 2024 respectively","as_of":"2026-08-19","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K無Item 4.02（財報不可信賴）項目；搜尋僅見2004年舊重編，無SEC調查。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000703351&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 11 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"EAT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.14,"operating_margin_pct":11.43,"fcf_margin_pct":11.11,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EAT","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MCD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.38,"operating_margin_pct":45.71,"fcf_margin_pct":28.02,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCD","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"TXRH","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":15.69,"operating_margin_pct":7.86,"fcf_margin_pct":6.43,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXRH","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"DRI","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":21.66,"operating_margin_pct":12.18,"fcf_margin_pct":7.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DRI","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CMG","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.84,"operating_margin_pct":14.95,"fcf_margin_pct":11.88,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CMG","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"EAT"},"financial_history":{"ticker":"EAT","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":4133200000.0,"revenue_yoy_pct":null,"gross_margin_pct":12.1,"operating_margin_pct":4.28,"net_income":102600000.0,"diluted_eps":2.28,"free_cash_flow":71400000.0,"fcf_margin_pct":1.73,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":4415100000.0,"revenue_yoy_pct":6.82,"gross_margin_pct":14.21,"operating_margin_pct":6.18,"net_income":155300000.0,"diluted_eps":3.4,"free_cash_flow":223000000.0,"fcf_margin_pct":5.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":5384200000.0,"revenue_yoy_pct":21.95,"gross_margin_pct":18.25,"operating_margin_pct":10.29,"net_income":383100000.0,"diluted_eps":8.32,"free_cash_flow":413700000.0,"fcf_margin_pct":7.68,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":5807400000.0,"revenue_yoy_pct":7.86,"gross_margin_pct":18.65,"operating_margin_pct":10.82,"net_income":487000000.0,"diluted_eps":10.87,"free_cash_flow":557500000.0,"fcf_margin_pct":9.6,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/EAT/EAT_Q1_2027_Earnings_Call_20261028.md）

# Q1 2027 Earnings Call
**Brinker International, Inc.** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Good morning, and welcome to the Brinker International First Quarter Fiscal 2027 Conference Call. [Operator Instructions]
It is now my pleasure to turn the floor over to your host, Kim Sanders, Vice President of Investor Relations. The floor is yours.

**Kim Sanders** (Executives):
Thank you, Joanna, and good morning, everyone, and thank you for joining us on today's call. Here with me today are Kevin Hochman, Chief Executive Officer and President of Brinker International and President of Chili's; and Michaela Ware, Chief Financial Officer. 
Results for our first quarter were released earlier this morning and are available on our website at brinker.com. As usual, Kevin and Michaela will first make prepared comments related to our strategic initiatives and operating performance. Then we will open the call for your questions. Before beginning our comments, I would like to remind everyone of our safe harbor regarding forward-looking statements. 
During our call, management may discuss certain items which are not based entirely on historical facts. Any such items should be considered forward-looking statements within the meaning of the Private Securities Litigation Reform Act of 1995. All such statements are subject to risks and uncertainties, which could cause actual results to differ materially from those anticipated. 
Such risks and uncertainties include factors more completely described in this morning's press release and the company's filings with the SEC. And of course, on the call, we may refer to certain non-GAAP financial measures that management uses in its review of the business and believes will provide insight into the company's ongoing operations. 
And with that said, I will turn the call over to Kevin.

**Kevin Hochman** (Executives):
Thank you, Kim, and good morning, everyone. Thank you for joining us as we share insights from our first quarter and our outlook for the remainder of fiscal '27. Q1 Chili's same-store sales were plus 10%, outperforming the casual dining industry by 720 basis points. This strong result was lapping a plus 21% in Q1 fiscal '26 and a plus 14% in Q1 fiscal '25 for a 3-year cumulative comp of plus 52%. 
Our Q1 sales result was driven by traffic increases of 6% versus a year ago. Chili's traffic has now beat the industry in the past 12 quarters. I'm proud of our Chili's team rolling industry-leading comps from Q1 last year and two years ago with even more very strong comps in Q1 this year. 
Our guest experience improvements and our everyday value leadership continue to support a powerful flywheel of traffic, sales growth, margin expansion and reinvestment in our business. And this steady approach is why the business will continue to win. Some have repeatedly said we cannot possibly continue to comp on top of big comp numbers. Our Q1 result putting three consecutive years of double-digit comp growth, driven by traffic gains provides ample support that our strategy is sustainable even with a difficult macro. 
And in Q2, we feel good about our ability to not only comp positive, but deliver a mid-single-digit comp for two reasons. We continue to convert new guests into regular guests, which means sustainable growth regardless of the prior year comp and we have very strong commercial and operational plans to keep the flywheel going. While it's clear the consumer is challenged, we feel we are positioned to continue to win in this environment through market share growth. 
Our experience improvements, combined with our everyday value leadership position us to win trips, a sustainable traffic-led strategy based on the fundamentals of why a consumer goes out to eat will continue to win the day. 
Now let's talk about the specific food and hospitality initiatives in Q1 that helped keep the momentum going. We continued our advertising and operations focus on the Big Crispy Chicken sandwich, and it was a key driver of incremental traffic throughout the quarter. Customers are responding to the size and quality of the sandwich versus fast food, as well as the price certainty of $10.99 for a large and abundant complete meal. 
Customer reception to the Big Crispy has been very positive, and our traffic momentum is proving the sandwich reception has been great. In Q1, we maintained the 55 sandwiches sold per restaurant per day we saw in Q4. Customer social media comments tell the story. Quotes include "Those commercials weren't lying. This thing is the bomb," and, "Chili's is making it affordable to go out to eat again."
In addition to continued focus on the Big Crispy, we also completed the upgrade of several lower mixing menu items during the quarter. During our Investor Day, we outlined plans to renovate most of the remaining 40% of the menu that has not been touched over the next few years. Recent menu changes included upgraded ice cream to the famous Blue Bell premium brand, the addition of sausage as a new protein to our high mixing pasta menu, the return of Cheesecake, a highly requested non-chocolate dessert, and a newly renovated Kids Pepper Pals menu with the addition of Ice Cream floats, Shirley Temples as well as the return of Grilled Chicken Bites, Cheese Quesadillas, and Mini Molten. 
On the hospitality side, ongoing simplification, removing friction for our team members and managers and North of 6 initiatives are continuing to improve the guest experience. Q1 was the first quarter we removed GWAP from our General Manager bonus. But as planned, this does not stop our customer experience improvements. Chili's Google ratings hit an all-time best in Q1 of 4.3. 
Key operational initiatives this quarter focused on the fundamentals of making our existing menu items more consistently. We had another full court press on Big Crispy execution, focusing on scratch-made batter and hand-breading perfection as well as ensuring filets go out freshly cooked hot and fresh every time. With the sausage addition to our pasta menu, we took the opportunity to retrain teams on pasta perfection, which includes how to cook the pasta for optimal taste and texture as well as retraining on all pasta menu item recipes. 
And our last big ops swing for the quarter was the initiative called Staff to Grow Your Business. With all the incremental traffic coming in, we believe it was the perfect time to roll out North of 6 best practices on staffing so restaurants can continue to take on more guests without sacrificing the customer experience. As part of this big swing, we also retrained all above restaurant leaders and managers on how to write perfect labor schedules based on North of 6 learnings, which is one of the most difficult tasks for our restaurant managers. 
So while our competitors were hard at work launching new items and new offers, we continue to keep operations focused on the fundamentals of delivering a great restaurant experience. We believe this focus will allow us to spend more time on what is important versus free limited time offers that will not have a lasting impact on the business. Marketing continues to bring guests in, and our restaurant operations continues to bring them back. 
Now I want to give an update on Maggiano's. I'm pleased to report the successful rollout of our new banquet operations program in Q1, where we have, one, restaffed our banquet sales managers removed during COVID; two, streamlined banquet execution; and three, created single point ownership of the entire process to ensure guests receive great service through the entire banquet planning and event day experience. 
This cross-functional banquet team was formed back in January, and we are now seeing great results from these efforts. Banquet sales were up 11% for the quarter versus a year ago. And while Banquets are only 15% of the Maggiano's business, this initiative is important for two key reasons. 
One, it shows that we can turn around Maggiano's results with focus on deploying cross-functional resources at a single-minded goal; and two, Banquets are Maggiano's #1 marketing vehicle to introduce guests to the brand as the vast majority of Banquets have never eaten Maggiano's. 
Big congratulations to the Maggiano's team for rebuilding our banquet capability, an important part of the brand's DNA. 
Before I close out my prepared remarks, I also want to provide an update on the industry check averages we shared at Investor Day. We were recently informed by our third-party data aggregator, Black Box Intelligence, that there were errors in the industry benchmarks for casual dining per person average. Importantly, they confirmed our PPA remains below the competition, but the differential is now narrower than we previously have quoted. The new data is expected to be included in the November update. We are confident our overall experience and price point provides the best value to guests. 
One last piece of quick recognition before I close out. A big thank you to our Bedford, Chili's GM, Nikky Castro, and our Pinnacle Park Chili's GM, Kara Miller, and their restaurant teams for allowing me to work hourly team member roles for a week in October. I learned some really important things, including while it's easier to work in a Chili's today than it was five years ago, there's still lots of opportunity to make it a whole lot easier. So thank you, Nikky, and thank you, Kara, and thank you to your team. 
As we discussed during our September Investor Day, the Chili's business has been rebuilt for the long-term sustainable growth, and our focus is on playing offense to keep this exceptional performance going. The powerful flywheel of traffic, sales growth, margin expansion and reinvestment in our business supports all of the investment needed to maintain the momentum, create a new layer of growth through new restaurant development and reimages as well as return significant capital to shareholders. And this quarter of comping double-digit sales over the past two years with double-digit growth this year is proof positive this sustainable strategy is working. 
Now I'll hand the call over to Mika to walk you through fiscal '27 first quarter numbers. Go ahead, Mika.

**Mika Ware** (Executives):
Thank you, Kevin. Good morning. Brinker started the year strong with its 22nd consecutive quarter of same-store sales growth. Our momentum and consistent focus on the fundamentals continue to support sustainable long-term growth. This momentum drove strong year-over-year revenue growth, positive traffic at Chili's that meaningfully outpaced the industry and restaurant margin expansion. Brinker reported total revenues of $1.476 billion with consolidated comp sales of positive 9.1%. Our adjusted diluted EPS for the quarter was $2.77, up from $1.93 last year, a 44% increase. 
Chili's comps were positive 10.1% in the quarter, building on double-digit comp growth in both fiscal '26 and 2025. This was driven by traffic of 6.4% and price of 3.7% with mix coming in flat. This represents cumulative traffic growth of over 28% over the last three years, demonstrating our ability to build on the increasingly strong foundation of our business bringing in new guests and keeping existing ones coming back. 
Chili's strong everyday value platform continues to resonate with guests, led by the success of the Big Smasher, Big QP and now the Big Crispy Chicken Sandwich. We are also focused on increasing throughput in our restaurants, allowing us to bring more guests through our doors as we reduce bottlenecks and streamline operations. We continue to have confidence in sustaining positive growth as we move through the year with our marketing brings guests in and operations brings them back approach. 
For Maggiano's, the brand reported comp sales for the quarter of negative 3.4% with negative 5.1% traffic, negative 0.3% of mix, partially offset by price of 2%. At the Brinker level, restaurant operating margins were 17.7% 150 basis points improvement year-over-year, primarily driven by sales leverage, partially offset by unfavorable commodity costs as well as higher hourly labor costs. 
Food and beverage costs for the quarter were unfavorable by 10 basis points year-over-year due to 3.3% of commodity inflation and unfavorable menu mix, partially offset by price. Labor for the quarter was favorable 90 basis points year-over-year. Top line sales growth and productivity offset wage rate inflation of approximately 2.6% and additional investments in labor. 
Restaurant expenses were favorable by 70 basis points compared with last year. Sales leverage offset higher costs for repairs and maintenance, advertising, insurance, rent and other inflation-related expenses. Advertising expenses for the first quarter were flat to the prior year at 2.5% of sales due to sales leverage offsetting slightly higher spend. 
G&A for the quarter came in at 4.3% of total revenues, 10 basis points higher than prior year due to higher performance-based compensation and additional restaurant support center resources, partially offset by sales leverage. 
Depreciation and amortization for the quarter came in at 3.8% of total revenues and decreased 20 basis points year-over-year due to sales leverage, offset by increased depreciation on capital spend. 
First quarter adjusted EBITDA was approximately $209.1 million, a 21.3% increase from prior year. The adjusted tax rate for the quarter increased to 19%, mainly driven by the increase in income, which was partially offset by a higher FICA tax tip credit. Capital expenditures for the quarter were approximately $63.4 million, driven primarily by capital maintenance spend. 
Regarding our Chili's reimage program, we have completed a total of 20 reimages to date. We have another 13 currently under construction and expect to complete a total of 60 to 80 during fiscal 2027. In fiscal '28, we will start a planned cadence of 10% of the fleet annually. 
While it is still early in the program, and we will continue to evaluate and read the results as more time passes, we anticipate the cost of each remodel to be in the $500,000 to $600,000 range with sales lift of approximately 3% to 5%. We are pleased with these early results as we know it's important to preserve the fun, welcoming and relevant atmosphere that we're known for. As we continue to refine the program, we will look for additional opportunities for cost efficiencies while retaining the quality of the reimage package. 
Turning to new unit growth plans. As we announced at our recent Investor Day, we'll be targeting 2% to 3% annual unit growth by fiscal 2029, supported by AUV growth from $3 million to $5 million and improved four-wall unit economics. We have visibility into a decade of new development with over 300 potential trade areas identified. The growth opportunities include capturing underpenetrated markets like Washington and the Pacific Northwest, executing infill strategies in core strongholds like Texas and Florida, expanding in high-growth secondary markets like the Carolinas and leaning into a small town strategy. 
That said, our growth will be modest in fiscal '27, but we already have ample sites in the pipeline and will ramp up significantly in fiscal '28 with expectations for our new run rate to be in place for fiscal '29. 
Our strong free cash flow provides sufficient liquidity to maintain our disciplined capital allocation strategy, allowing us to invest in our restaurants, keep debt levels low and return excess cash to shareholders. We continue to support this approach by repurchasing $125 million of common stock under our share repurchase program during the quarter. 
In this morning's press release, we shared that we are updating the fiscal '27 targets provided on our last earnings call due to our first quarter outperformance and continued business momentum. We expect to significantly outperform the industry in sales and traffic while delivering another year of same-store sales growth in fiscal '27. 
Regarding the updated targets, we expect F '27 annual revenues in the range of $6.23 billion to $6.33 billion, adjusted diluted EPS in the range of $13.30 to $13.90, weighted average shares in the range of $42 million to $43 million and capital expenditures in the range of $265 million to $285 million. 
The assumptions underlying our targets remain unchanged, including the expected impact of the 53rd operating week in the fourth quarter of approximately 2% increase in total revenues and $0.70 in incremental earnings per share. We anticipate the first quarter will be our strongest on a year-over-year same-store sales basis with more moderate gains in subsequent quarters as we lap higher prior year comparisons. 
Despite these tougher comparisons, Q2 is also off to a strong start with high mid-single-digit same-store sales growth, primarily led by positive traffic that continues to meaningfully outpace the industry. While consumer sentiment is creating some pressure on check and mix, the underlying strength of the business gives us confidence in our outlook. We are optimistic about our ability to continue growing sales and traffic while maintaining a disciplined approach to our full year expectations.
As we look to the rest of the year, I am confident in the direction of the business and our ability to drive consistent long-term growth. We are executing on the fundamentals of operational improvements, marketing and value across the menu while adding incremental growth through reimages and new units. These initiatives will continue to generate new and repeat visits and deliver solid traffic and sales growth. 
With our comments now complete, I will turn the call back to Joanna to moderate questions.

**Operator** (Operator):
[Operator Instructions] 
First question comes from David Palmer with Evercore ISI.

**David Palmer** (Analysts):
Thanks for your comments on the quarter today because I know people are going to be focused on any changes that you're seeing in the industry. Maybe I could ask you a question about it since you talked about your sales in particular. What insights can you give us about what's going on out there with the consumer? We've heard that perhaps there was a little bit of wobbliness with $100,000 and over consumer and maybe you could speak to what you've seen even on a weekly basis and looking into your demographics and any other insights we'd love to hear from you on that. And then I know that also, if I throw in another one, it would be on inflation. A lot of focus on freight and other costs kind of getting into the cost picture by what would be the end of your fiscal year? And I'll pass it on.

**Kevin Hochman** (Executives):
So let me handle the consumer question, David, and then I'll have Mika do the inflation question. So we are seeing what most of you guys are all seeing, which is a consumer that is under pressure with what's happening with gas prices and the interest rates. So what we've seen, and we talked about this on the prepared comments, is we still see very strong same-store sales, primarily driven by traffic. We have seen a little bit of mix slippage, which we think is the consumer being under pressure. So it's very similar to what we've talked about in the past, which is if trips do pull back because of the macro, that consumer is going to pick places they trust and the stronger are going to get stronger and the weaker are going to get weaker. 
I think that's what you're seeing with us growing market share and driven by traffic. So we launched the chicken sandwich at $10.99 as a traffic-driving strategy for just this. This is exactly how it's playing out in the way we had hoped in terms of growing market share. So we believe as long as we continue to improve food service and atmosphere and make us an obvious choice for consumers that may be going out a little bit less, but they know they're going to get a great value and a consistent experience. We believe we're going to continue to grow enough market share to continue to win, and that's what's reflected in our guidance.

**Mika Ware** (Executives):
Yes. And David, on your inflation question, specifically around the oil prices and freight, yes, no, we've had that pressure. The good news is all of that is built into the guidance that I gave. So we probably have about $7 million built into our numbers and our expectations. Most of that for us is going to hit in restaurant expense. So that's where that lies. It's not necessarily in food and beverage costs. But yes, we are feeling those pressures and the inflation kind of I spoke about in the prepared comments, that is built through. Luckily, our sales are helping us to still have great margins and flow-through. 
That's kind of been job one from this whole -- from the start of the turnaround has been, we are going to grow faster and grow enough volume to improve our margins and to overcome any inflationary pressures, and that's exactly what's happening in the business right now.

**Operator** (Operator):
Next question comes from John Ivankoe with JPMorgan.

**John Ivankoe** (Analysts):
I'm going to ask a tactical question, if I can. In terms of the promotion awareness trial repeat of the Chicken Parm Big Crispy, Hopefully, I'm getting that right. Do you expect to kind of go back to kind of traditional media and really drive awareness of it? Do you think enough people know what the product is, appreciate how it's differentiated? And just talk about, at least from your perspective, how you think that product could or should build as we move throughout the second quarter?

**Kevin Hochman** (Executives):
Yes. So let me just give you a little context of like what we're trying to accomplish with that. And then I'll give you a status update of where we think it is right now versus where it could be. So this is what we call a big swing. So this is swings that we take in marketing. Some of them hit, some of them don't hit. 
In Q1, I think the swings that we took, they all pretty much landed. That's, I think, why we were plus 10 and more. This one is a big swing, similar to the one that we had done when we launched Nashville Hot Mozz. So this was a quote unquote "secret menu item." We had trained our teams on how to make Nashville Hot Mozz. We released that via social media, and we had no POP and we had no menu presence until a few months later, and it obviously worked incredibly well. 
On this one, we're applying that same playbook. But the one thing I think we're learning in the first week of it being available nationwide is, it's much easier to order that Nashville Hot Mozz even if it's not on the menu because you order like a Triple Dipper or you order Mozzarella sticks, so you can just ask for it in this other flavor versus this is an entirely new sandwich. And so some guests are more forceful and say, "Hey, do you have the sandwich I saw on social media?" Other guests are kind of like, "Hey, I do not see it on POP or on the menu. I am not going to order it." 
 Now that's all going to change the first of the year. Our table tents for the next three months, we'll all have…

**Mika Ware** (Executives):
First of the month.

**Kevin Hochman** (Executives):
I'm sorry, first of the month.

**Mika Ware** (Executives):
Yes, not year November 1.

**Kevin Hochman** (Executives):
1st of November. Sorry, with the Table tent merch. So I think we're going to learn a lot more in the next coming week or two about how much it takes off because it's going to be something that people can point to and say, "I want to order that."
So right now, it's being a little over two a day, which is a little short of what we expected it to do. But I think the difference on this one that we're learning is it's not an easy thing to order. And so once we have that merchandising in the restaurant, we would expect it to pick up again. So let me answer that in a few weeks when we see what's going on once we have some merchandising in the restaurant.

**Operator** (Operator):
Next question comes from Dennis Geiger with UBS.

**Dennis Geiger** (Analysts):
I wanted to ask a little more on the '27 guidance. I know we can back into some of the items. But after the strong 1Q same-store sales, very good momentum still into 2Q, anything more specific on your assumption for Chili's same-store sales for the year, I guess, really for the back half of the year in particular?

**Mika Ware** (Executives):
Yes. So Dennis, what I would say is for the back half of the year, two, three and four, we're back to the mid-single-digit same-store sales expectation with positive traffic. October, again, we are thrilled with the start to October. We do have, we're just aware of, and you guys remember, we had a huge November last year. So we do have a big lap right in the middle of the quarter. We feel very confident in our ability to lap that with positive sales and traffic. But right now, we're in that same mid-single-digit same-store sales. We have a lot of momentum, and we're really excited about it.

**Dennis Geiger** (Analysts):
Awesome. And then just as far as value goes, can you just give us the latest update considering the backdrop in particular, on where the 3 for Me mix is, where that $10.99 is? And if anything incremental on the check management maybe that you're suggesting, I think we heard a QSR a couple of weeks ago, we talked about number of items per order. So it sounds like you're not the only one that's seen that. But just if anything incremental as we think about value and where the consumer is.

**Mika Ware** (Executives):
So for Q1, when we think about the 3 for Me platform and specifically the $10.99, the 3 for Me platform, it's pretty similar to what it has been. It ticked up a little bit, maybe 50 basis points. So I always say we're in that 20%, 21% range. So we're a little over 21%. So really right where we expect it to be, so a little bit of an uptick. As far as the check management goes, in Q1, like we said, our mix was flat. Kevin alluded to this, we did see in October, our mix has gone a little bit negative, but our traffic has more than made up for that. Our traffic is 2/3 of our same-store sales right now. So our traffic is accelerating. So we're seeing those guests maybe do a little check management in alcohol and desserts, but they're seeing more guests come to Chili's as that's where they think the affordable choice is. So that's really working out for us.

**Operator** (Operator):
Next question from Chris O'Cull with Baird.

**Christopher O'Cull** (Analysts):
Kevin, I'm just curious what you believe is driving the quarter-to-date strength? Because I believe that's happening during a period where you weren't particularly heavy on national advertising, at least until very recently. And if that's correct, what potential is there maybe for further acceleration as you do get back into some more heavier media?

**Kevin Hochman** (Executives):
Well, I don't think it's anything different than what we've been doing year after year now. So this idea of marketing brings them in and then ops brings them back. We shared at Investor Day, Chris, the token data where we said, hey, we have anywhere from 3 million to 3.5 million new tokens come in and then we track their frequency as a monthly cohort to see do we maintain that frequency as we continue to fill the bucket with new guests. 
We don't have the data for this past quarter yet in terms of repeat from new guests, but like there's no reason to believe that's changing based on the guest metrics that we have. So I don't think it's anything new or different. I think we have great marketing. So we had some big swings. We had a really good July Margarita of the Month. We had the Big Crispy advertising going with a direct comparison to a large QSRs chicken sandwich, which is really before your eyes, how much value you get with $10.99 in Chili's. 
Then we had a great Rhoback, Chili's golf merch thing, which is another big thing just to get into the zeitgeist and be relevant with our guests. And then we've continued to have operational improvements. We talked about the Google scores, which is an external measure. That's not something we even measure. That's just we get from Google being an all-time high at 4.3. So it's just kind of more of the same. I know that sounds a little boring. I wish it was more of a Merlin act where we pulled out some LTO and it did it. It's really just about the fundamentals of casual dining, delivering great everyday value for our guests and then executing like crazy. And the guest is seeing that and they are coming more often. I think that's why we're seeing traffic accelerate as the consumer is becoming under more pressure.

**Christopher O'Cull** (Analysts):
Okay. Fair enough. And Mika, can you provide some additional color on the returns you're seeing on the remodels as you ramp them up? I mean, just in terms of flow-through, I understand you've given the comp list, but I'm curious what the flow-through looks like, especially as relative to the investment.

**Mika Ware** (Executives):
Yes. So Chris, really, what they're doing now is covering the cost of capital. Early on, right now, we're at the $600,000 investment. We talked about 20% of the fleet is going to need that higher investment. The other 80%, it will probably get closer to $500,000. And again, we're so early in this program. We think we can continue to get some costs out of those reimages while just maintaining the quality of the reimage. So I think we're going to see some efficiency there.
Also remember, these are fairly new. We need to read them over time. Again, we're getting that 3% to 5% lift even as we continue to add on new restaurants. And again, that is above and beyond all the incredible momentum that we're seeing in the business. So we're still really pleased with this because we know the reimages need to be -- they need to happen. They need to keep as part of our pillars on the atmosphere. We've got to stay relevant, and we think it's part of the overall program. But more to come on specifics on returns as we continue to refine it over time, but it's just really early right now.

**Operator** (Operator):
Next question comes from Jeff Farmer with Gordon Haskett.

**Jeffrey Farmer** (Analysts):
Mika, can you update us on the restaurant level margin expectation for the year in the backdrop of sort of the stronger same-store sales numbers you're seeing?

**Mika Ware** (Executives):
Sure. Absolutely. I'm happy to. So taking a step back. So if we look at the full year, what I'm expecting in restaurant-level margin improvement is about 70 to 90 basis points improvement year-over-year now, especially with the strong first quarter that we've had. Now I do want to say I need to maybe smooth out the quarters a little bit, just thinking about some of the lapse that we had in prior year. So what I would expect in the second quarter, I would expect restaurant level margins to be roughly flattish year, year-over-year with maybe a little pressure on labor because, as Kevin said, we are really leaning into labor. 
We kind of do opposite what everybody else does. Labor is one of our secret sauces where when those guests comes in, we want to make sure that we're taking care of them and capturing all those guests. So we don't shy away from that. Quarter 3, I think you're going to see a return to the 20 to 40 basis points that I always talk about with mid-single-digit same-store sales. 
Then quarter 4, there's more upside there, particularly in the food and beverage line because we're going to be lapping from a year ago, the tomatoes and the lettuce. We talked about that last year. So we have a little bit more upside there. So again, full year, and that does include the 53rd week, that 70 to 90. The 53rd week is worth about 30 basis points. So hopefully, that helps everyone to kind of get those quarters in line and a little more visibility on how we expect restaurant level margins to progress throughout the year.

**Jeffrey Farmer** (Analysts):
Very helpful. And just same sort of topic area, at least on the margin front. Updated G&A guidance, I think it stood at approximately 4% of sales on the last call. Where does G&A stand right now?

**Mika Ware** (Executives):
Yes. So it's going to hover around that for the full year. It may be 4%, 4.1%. We do have some incremental performance-based compensation there, especially after the first quarter. It will smooth out over time, but it's going to still be in that 4% to 4.1% range for the full year.

**Operator** (Operator):
Next question comes from Andrew Strelzik with BMO.

**Andrew Strelzik** (Analysts):
My first one is about the throughput initiatives. But I'm curious, as you talk to the traffic strength, if you're seeing any measurable benefit from those throughput initiatives in the first quarter or even the quarter-to-date period? And maybe just looking for an update on where the rollout of some of those drivers stand today.

**Kevin Hochman** (Executives):
Yes. So we've seen a slight decrease in ticket time, but it's not worth, it wasn't worth, it wasn't significant enough to worth reporting. I think if we see it over a few quarters and it continues to track, then we'd probably share that. But we feel very good about what's happening. So number one, as I talked about in our prepared comments, we rolled out really the best practices on how the North of 6 restaurants manage labor cards and labor productivity at peak. And so we retrained all of our above restaurant leaders on how to write proper labor schedules and have incorporated all the best thinking and best practices in the North of 6 restaurants into the business. So that's kind of point one.
Point two, we have a quarterly rollout going on right now on host stand. That's a pretty big initiative for us because just top per day is almost a point in sales. So it's a pretty big opportunity for us. And we have nothing baked in the guidance. So anything that we can get here is upside. We did four things this quarter. 
One, we reestablished talent standards for the host position as well as staffing appropriately for the volume. So five years ago, there are a lot of restaurants didn't even have a host done. Now we're talking about three, four hosts in some of the restaurants. 
Number two, we trained on what we call Aces in Places. So defining multiple host stand roles. We call it Meeter, Seater And Greeter and then making sure that managers are at the floor for large parties. That tends to be a bottleneck when a party of like 8 or 12 come in and they all want to sit together. And so making sure managers get involved there. 
Three was retraining on our iPad training for host stand. So this is all about how to properly use the software with the end goal of making sure that we quote zero false waits. False waits, I think I talked about this in an earlier earnings call. False waits are a very common thing in casual dining where through improper preparation or lack of labor scheduling, the restaurant gets backed up. So the servers are kind of pushed to put people on false waits. We want zero false waits in our restaurants, meaning we want them quote in the exact quote time that the system is quoting. 
So all these things are rolling out right now. So I would expect by November, December to start seeing some progress on host stand. And then we are currently rolling out. We've talked about this for a while. It should be done by the end of the calendar year of rolling out the new team member handheld interface, which eliminates over half of the tasks that are required in order to ingest an order from a table, which would help with ordering time. 
So we have a lot going on in terms of throughput. There's a whole host of another initiatives on to-go that we have yet to share, that is just getting started now. And as we get updates, we'll share them. But feel very, very good about what we're attacking. I hope in future calls to be able to share metrics like what we talked about at Investor Day like dine-in times and ticket times and things that would give you some sense of in-process metrics that would let you know that productivity is happening.
I will say when we look at North of 6 restaurants, who have mailed throughput, everything is better. Food grade scores are better, GWAP is better, productivity is better. They save on the labor line and ticket times are lower despite having way more volume. So certainly, if we can crack the net on this productivity thing, I would expect there to be upside from it.

**Mika Ware** (Executives):
And I'd like to note on North of 6, they also continue to comp at the same rate or higher than the brand. So their ability to get even more traffic in continues to amaze us.

**Andrew Strelzik** (Analysts):
Okay. All right. That was super helpful. And I just wanted to quickly ask, with the change to the manager bonus structure going into place, have you seen any changes in behaviors? I know you're leaning into labor more certainly. But I guess I'm just curious if you're seeing any changes to maximize throughput or anything like that since that's gone into place.

**Kevin Hochman** (Executives):
Yes. There's a couple of things that are going on. One is there's just a lot less like distraction about the guest score. So we don't see as much like for lack of a better term, obsession about the Ziosk scoring and the scores going up, and it's no longer a motivator for our hours when folks are posting these scores. So I think the biggest thing that I've seen so far is just a lack of a distraction or wasted time on worrying about a score versus worrying about the behaviors. So that's kind of point one. 
The second thing that I think has come out of this is we rolled out a vastly simpler reporting structure in terms of like the key operational metrics that we look at on a daily basis. the focus on a few ones that are incredibly important. So I feel like when I go to restaurants and we have discussions with the general managers and the above restaurant leaders, I feel like they're more focused on the more important things, and we get to the fewer, bigger things faster. 
So I think over time, I would hope to see just continued operational improvement because of the simplification. But those are the two big areas that I've seen is a focus on what's important, and then the elimination of distraction of looking at these metrics on a daily basis by individual basis and really just focusing on the behaviors that are going to be required to deliver improved operations over time.

**Operator** (Operator):
Next question comes from Andrew Charles with TD Cowen.

**Andrew Charles** (Analysts):
Kevin, I wanted to ask on the marketing side. We've seen you guys partner celebrity brand fans, including Snooki most recently and then Lizzo about five months ago. Should we think about this as a pattern that you have the opportunity to run these collaborations every six months or so? Or do you expect future collapse to be further apart?

**Kevin Hochman** (Executives):
Well, I can just share with you how the marketers think about this. So typically, we sit down with the calendar or they sit down with the calendar and they look at, "Okay, when are we launching things, where are consumers seasonality-wise, what's happening in the restaurants." They typically make the plan to try to always be on with some type of interesting thing happening in the business. So, if the food is leading the way because we're launching the Big Crispy, they let that thing. But if we have times where it's been three or four months into the Big Crispy launch, and we feel like we got to get new news to make sure that we continue to build relevancy for this brand, they'll come up with ideas based on some specific strategy, right? 
So the example of the Lizzo example that you gave was, "Hey, we have these new improved ribs. There is 50% more bones from the portion size. They are fattier and meatier than the old rib that we had, so they are much better value." How do we create excitement to get people to come into the ribs given it's not the biggest segment that we're going to go put on TV. And that's where the team came up with like, "Hey, let's reboot the rib single. " That's something that's really part of our history, and let's get a bid performer to sing that. So that's where Lizzo came in. 
On the Snooki one that you're referring to that's most recently, that was in innovation kitchen, we tasted a lot of different chicken sandwiches to see which ones could really stand out given how big that fleet is. We talk about it's over 80% bigger than the leading QSRs chicken sandwich and handmade, the batter is from scratch. So this is a vastly superior chicken sandwich. And so we're looking for ways to create some excitement by it. The team saw Chili's way of doing Chicken Parm with the cheese pull. So that's where that piece of sandwich was invented, right? 
And then we say, how do we create excitement in social media, and that's where Snooki came from. So it's not necessarily like on a cadence of every six months. It has to do with what is the priority for the quarter that we want to drive. In this case, how do we continue to launch and sustain our chicken sandwich launch. So how do we create new news virally. And so that was the idea behind it. So it really just starts with what's the priority and what we want to drive with the guest and then the marketers then use their creatives to figure out what are we going to apply to that.

**Andrew Charles** (Analysts):
That's very helpful. And then, Mika, I know you gave the commodity inflation by quarter for the year, the expect for food inflation. Can you give that for labor inflation as well?

**Mika Ware** (Executives):
Yes. Labor is just going to be in that 3% to 5%. It was a little bit less than 3% this quarter. Closer to 3% all year.

**Operator** (Operator):
Next question comes from Sara Senatore with Bank of America.

**Sara Senatore** (Analysts):
I guess I wanted to ask just broadly about the casual dining segment. I know it's something we've talked about before, in particular, younger users. I think when you and I chatted, you suggested that maybe having more casual dining brands on social media gives younger consumers maybe permission to go. Could you just talk about that cohort in particular? And I'm trying to, I guess, figure out why it seems like just casual dining, the contrast between the comps and casual diners we're seeing, you're obviously leading, but just broadly speaking, much greater than QSR or others. 
I know you talked about the relative value. But maybe you could just talk about that younger cohort in particular as a potential longer-term maybe structural driver.

**Kevin Hochman** (Executives):
Yes. I mean I think we see that in our business. I think you're probably referring to one of our competitors that have done this successfully, too. What I would tell you is I think maybe we brought some of the more modern marketing techniques to casual dining, but they're not, I mean, I think within restaurants, they're pretty well known, like in QSR, I came from QSR. And if you actually look at the reports that come out about social media impressions, QSR tends to have more social media impressions than casual dining. 
I think the difference is what's happening is, one, it's new to casual dining. So as George and team have brought social media to our business and people see the success that we've had, they're saying, "Hey, I could probably apply this to my casual dining concept. " But I think the second thing, which I think is different than QSR is there are several casual diners that operate very, very well. 
When you have a good product and it shows up in social media and then people go to replicate it, if you have that experience, that's what grows and that's what grows your business, right? Like I always talk about when we had the first kind of spark in social media, this was April of '24, so about 2.5 years ago, if people came in for the cheese pool and the cheese didn't pull and the restaurant wasn't clean and the experience wasn't good, I don't think that would have lasted more than two or three weeks, and we wouldn't be talking about this 30 months later, comping a 10 on top of a 22% on top of a 14%, right?
So I think that's the other thing that I think, Sara, I'm not sure everybody quite understands is like it's not just about going viral. I think lots of brands go viral. But like what you saw with us, I think what you're seeing with one of our competitors in casual dining that's having some really good success with it is you go into their restaurant, you go into our restaurant, you have a pretty good experience. 
Like it feels like that social media experience that you saw online, and that causes you then to repost and share your experience and then that's when it has that more. So I would anticipate that everybody trying to do this. I think the better operators are the ones that are going to really win out in this environment because you can't take a social media post, right? Like that person is going to post whatever they see an experience. If it's great, you're going to feel really good about that post. And if it's not great, you're going to feel the exact opposite. And as long as the brands that do this are operating well like Chili's is, I think they're going to also win too.

**Sara Senatore** (Analysts):
Yes. And then just quickly on Maggiano's. The banquet business, that's encouraging. And to your point, that's the real opportunity to market. Anything that else that maybe has changed in the operating environment, whether in the Italian segment or anything that you've seen that might also be contributing? Or this is really very specific to Maggiano's?

**Kevin Hochman** (Executives):
Well, I mean, there's macro factors. I always tell our team, we've got to just focus on what we can control. And what we can control is speeding up service and making it more consistent. And so Banquet is a great example. And the reason why I shared it, even though it's only 15% of the business, it's up double digits, and it was like kind of a big swing that we started nine months ago, and now we're seeing the fruits of our labor and our bank of bookings are ahead of a year ago now when we look heading into the holiday season. So to me, it was two things. One, it's a marketing tool because that's the way a lot of people are introduced to the brand. But two, I think it showed, hey, if this cross-functional team gets together, they focus on something that's important, they work together, they're going to have big results, right? 
And so the next big thing that we're working on right now, we have it now live in one restaurant is taking the Chili's KDS technology, which is the back-of-house system that tells cooks what to cook and QA what to send out to tables. And we're taking that state-of-the-art system and putting it into Maggiano's. The current system they have today is it's just not doing Maggiano's a service in terms of temperature of food and how fast food goes out and how it coordinates across stations. 
So that's an example where I think if we get that done, it's probably going to take at least another quarter to get all the kinks out. If we get that done successfully. I would expect to see ticket times come down, total dining times come down, improved productivity on the weekends, which is where we need it. So that's the next big swing, I think, cross-functional projects that we're working on. And I hope by next earnings call to be able to update that it's either been rolled out or is in process of the majority of the system and soon to be fully rolled out because I think that's going to be the next big push in improving throughput at that concept.

**Operator** (Operator):
Next question comes from Brian Harbour with Morgan Stanley.

**Brian Harbour** (Analysts):
Could you just talk about both pieces of the off-premise business maybe? And I know you talked a little bit about kind of leveling that up at your Investor Day. When do you expect that would happen?

**Kevin Hochman** (Executives):
So delivery and carryout are about each about 12.5% of the business roughly. So it's about 1/4 of our business is off-premise. We are in process of a major cross-functional effort that's going to take several years to, we think, strengthen our off-premise business. And we're not really focused on delivery per se. We're just focused on all those things that impact carryout and delivery. So even though delivery obviously has been growing from an industry standpoint, we're more focused on how do we make it easier for customers to order, how do we make it easier for both customers and drivers to pick up the food and then how do we ensure that the food is as accurate to the order as possible and arrives in the best possible condition given it's got to travel for a period of time. 
So the first things that we're working on this year are our promise time calculator. So essentially, as we've sped up our operations, the promise time calculator is a bit antiquated. So it quotes longer times than actually the food would be prepared. So you get a text that, "Hey, your food is going to be ready in 25 minutes," and then 10 minutes later, you get a text that your food is ready. We think we've got that solved with an interim solution now that's in restaurant. We're working on a longer-term solution that's going to be more reflective of ticket times and how fast the food can be ready to be ordered. 
The second thing that we're working on right now is improving the ease of ordering. So the first project that's on the docket that hopefully will roll out soon is just making the reorder button a whole lot easier to use. So there's a decent percentage of people that just want to be able to either reorder or reorder with minor modifications on their order. And the bold goal for that team is to get people's order time to less than a minute in order to make it kind of a routine. When you look at the better players in off-premise. They have apps that are very easy to reorder food from and makes the small items too. So we're trying to copy that. And then longer term, we're looking at things like the pickup experience with order boards, additional packaging upgrades to make the food present better and hold better as well as some improvements in terms of accuracy. But it's going to be a multiple. 
Brian, it's going to be a multiple year initiative. We're still working on dine-in, and we're in year five. So I wouldn't expect some magic wand in Q3, all of a sudden to go is fixed. I think it's going to be a long slug of looking at things in a very deep way and then improving things over time so that when you add it all up a couple of years later, we can be the leaders in casual dining to go. 
But I will tell you, it's a big opportunity for us because when we think about the better than fast food campaign, and that food tends to travel better. So the bold goal is we want to be as easy as fast food, but have a better value than fast food. And if we can do that, I think you'd see our off-premise business start growing a little bit faster than our dine-in business.

**Brian Harbour** (Analysts):
Okay. Kevin, I guess, since you teased it, what, based on your time working in a restaurant, what do you think can still get better on the back of the house?

**Kevin Hochman** (Executives):
Everything. So that it's encouraging. I know that sounded like it was, but it's encouraging. So one of the things that, one of the biggest things, I spent about 1.5 hours debriefing our leadership team on kind of my experience there. And the big umbrella was even though I think everybody, all the managers told me and all of the hours told me, it's so much easy to work here, Kevin. Thanks for your continued partnership on this. 
My observation was it's still not easy to run at Chili's. I don't think that's unique to Chili's in casual dining. I think it's probably hard to run complex venues with table service pretty much anywhere, especially when you have a giant concept with over 1,000 restaurants. So I have two main observations on that. 
One was we have to be continuously improving and making this restaurant easier to run. And so we think about things like the Heart of House project, which is going to be fueled by AI. So we think about almost like a completely new system that's an integrated kind of like an ERP system for the Heart of House. That is going to make forecasting, ordering, inventory, prep, labor scheduling, it's going to make everything easier. Now that is a two- to three-year project. So it's not like it's going to come this fiscal. But like that example, there's so much institutional knowledge that you need to have to run at Chili's because none of the systems are naturally connected. 
We've created some integrations, but most of them are manual integrations that the managers have to do, and it requires a lot of institutional knowledge. So point one, there's still a lot of upside to make it a whole lot easier, especially with technology. The second thing is even when we get all this stuff installed, it's still not going to be the easiest thing to run. So it instilled me the importance of retention in this ownership model because when you look at like North of 6 restaurants, they have longer tenured managers. It's such a clear like data point. 
Then having like done it firsthand, I can see why. Because regardless of how much automation we can put in the business with technology, it's still going to be a difficult job. And so the longer we can retain our managers and have them have big careers at Brinker and at Chili's, I think the better they operate, which is why the majority of North of 6 restaurants have long-tenured general managers. So I mean, it was like I have like 60 slides of all the improvements that we can make. So Brian, so a lot came out of that. 
But the two big ahas were we still have so much low-hanging fruit that we can focus on to make this operation more seamless and a better guest experience. And then two, how do we really take this ownership and retention and take it to a whole another level. And probably the guys that everybody is chasing in casual dining, that second part, they know like the back of their hand. I think now I see firsthand why that is so valuable to our business.

**Operator** (Operator):
Next question comes from Margaret-May Binshtok with Wolfe Research.

**Margaret-May Binshtok** (Analysts):
I just wanted to follow up. I know you mentioned that there is some check management that's impacting desserts. But last quarter, you guys did talk a little bit about some of the dessert innovation that's coming and also moving up desserts in that kitchen screen to help servers sell more. I guess, how do you think about leaning into desserts while seeing the check management that's going on right now?

**Kevin Hochman** (Executives):
Yes. So we saw some virality with the Molten being served on top of a cookie. I think that's what drove incidents that quarter, the mix decline has really been more recent. So this dessert incidence is more of a recent trend post the morality of that molten cookie initiative. I will say we're in test right now with bumping the desserts to the top of the screen. We want to make sure that we're not inadvertently slowing down other dishes. So I mean it's more important to turn tables than to create dessert add-ons. So that's why we're testing it versus just doing it. I will say from my last three restaurant visits floating the idea that we're testing it, that everybody got really excited by it. So my guess is it's probably going to work. But we don't really have any updates on that because it's still being tested right now. Still early.

**Margaret-May Binshtok** (Analysts):
Got it. And then just a follow-up on the Big Crispy. I know you mentioned marketing earlier and the pace of it. But just on the Big Crispy, I know you have the Chicken Parm one coming up. But should we think about more innovation opportunity on the Big Crispy platform? And is there a cadence we should be thinking about from here?

**Kevin Hochman** (Executives):
Well, so right now, we're focused on just advertising the Big Crispy on $10.99 with the majority of our marketing dollars are spent on whether linear TV or connected TV and then digital. So the majority of our marketing spend is on this value message find the Big Crispy. The Big Crispy Chicken Parm sandwich is mostly a PR and digital social media play, which is not that it's not important. It's just that investments are a lot less than when we talk about broad-based message about value. We are continuing to look at different innovations on the Big Crispy. We have seven variants right now that we haven't talked about them all. So that's the other opportunity is we have some very unique things like the Honey-Chipotle sandwich and the Nashville Hot sandwich. 
These are all very unique sandwiches within casual dining. So we're going to evaluate whether we think we need to update the Big Crispy message next May, like do we need to bring new product news or do we continue to see more traffic being built with just the $10.99 message. 
What we talk about here is if it's not broken, we don't fix it. So if we see that the traffic lifts are the same, call it, in Q3 as they were in Q1 and Q2 from the Big Crispy advertising, I don't anticipate us moving off that message. If we see that starting to wane in terms of the traffic response to the advertising, then I think we'd likely see some type of new product news either on chicken or on hamburger depending on what we think is more topical for the moment. But it's more the business results are going to drive whether we bring additional innovation. We're going to be preparing for innovation, but we're not going to like be hard and fast that we are absolutely going to have to have a new chicken sandwich next May because if the business continues to rock and roll, we would not move off that.

**Operator** (Operator):
Next question comes from Chris Carril with KeyBanc Capital Markets.

**Christopher Carril** (Analysts):
So Kevin, you mentioned big swings a few times on this call. Can you maybe talk a little bit more about the efficiency of these big swings, maybe why you think they're landing more frequently? Is this a function of the overall momentum the business is seeing? Or has something changed in the process to ensure the success here?

**Kevin Hochman** (Executives):
Yes. So just to be clear, we use big swings in two ways, maybe because I always talk about fewer bigger with our teams, so everybody attached to the word big swings. So I think you're referring to big swings in marketing. We use think swings for two things. Big swings in marketing, meaning take a couple of big swings every quarter to see what we can have takeoff into the culture and drive relevance to the brand. Then we also talk about big swings in operations. We pick about three big swings every quarter that we do a rollout on. They're typically based on the fundamentals of casual dining and typically tied to something commercially that we're driving so that the business is hearing one message from us. 
So I think your question is about marketing. We are constantly learning about what works and what doesn't work, and we're adjusting our plans based on that. So like the best example I can give you, so it's not really formulaic. It's more -- we think about it on a value offer, we have large amounts of out-of-store advertising to drive the value message because that's broadly appealing. 
Then we use social and digital and PR to kind of try to go after specific groups of people that we think would have interest in learning more about Chili's than about whatever that item is. And then based on what we see in market, we adjust. So things hit, we try to understand what are the things that made it sticky and go. When things don't hit, we try to learn from them and say, what do we miss out on that we could have improved more? Like, for example, on the chicken parm that we just launched, realizing not having something to point to in the restaurant maybe limits the amount of business that we can have on that, but we're going to find out very quickly on November 1 when we have merchandising in the restaurant. 
But the best example I can share with you so you can understand at least how we approach it is when we launched the Big Smasher in May of '24, we primarily did that with TV advertising. And next year, we layered on a bunch of social advertising behind it because we had all this great success from the social and the Triple Dipper. And that social advertising was squarely on having people compare our burger versus a fast food burger, which is way more compelling when it's coming from a third party than it is from a company that's advertising on TV. And then in year three, when we launched the Big Crispy, we had all of the PR we had in year two and the social, but then we had three bouts of social. So we didn't just stop with the launch in social. 
We had a second hit with new messaging that was fed to the influencers a few months later. And now we have the Big Crispy Parm, which is our third hit of social. So I would tell you it's just every year, we're learning how to be more effective. And that's one of the things I really appreciate about our marketing team. So like George Felix and Jesse Johnson, they're very hungry to like just how do we get better. So even though I would say they're probably the best in advertising in restaurants right now, like every year, they're doing a debrief on like what could we have done better. 
So I just feel like every year, they just get stronger, right? And that's why we're able to continue to bring new guests in and then operations does their amazing job, and that's why we have the sustainable flywheel going. So that's the best way I can describe it is they're constantly looking at how they can make these things better. But like there's no formula of like add another 30% and get another three big swings. That's just not the way they look at it.

**Operator** (Operator):
At this time, I will turn the call back over to Kim Sanders for closing comments.

**Kim Sanders** (Executives):
And that concludes our call for today. We appreciate everyone joining us and look forward to presenting our update on our long-term growth on our second quarter fiscal year 2027 results in January. Have a wonderful day.

**Kevin Hochman** (Executives):
Thanks, everyone.

**Mika Ware** (Executives):
Thanks, everyone.

**Operator** (Operator):
Thank you. This does conclude today's conference call. You may disconnect your phone lines at this time, and have a wonderful day. Thank you for your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### EAT_Q4_2026_Earnings_Call_20260812.md
- 2026-08-12｜CFO Mika Ware｜guidance：FY27 營收財測區間 $6.15B–$6.27B（原話："we expect F '27 annual revenues in the range of $6.15 billion to $6.27 billion,"）
- 2026-08-12｜CFO Mika Ware｜guidance：FY27 調整後稀釋 EPS 財測 $12.60–$13.40（原話："adjusted diluted EPS in the range of $12.60 to $13.40,"）
- 2026-08-12｜CFO Mika Ware｜guidance：FY27 資本支出財測 $265M–$285M（原話："and capital expenditures in the range of $265 million to $285 million."）
- 2026-08-12｜CFO Mika Ware｜guidance：FY27 第四季含第 53 週，估計增加約 2% 營收與 $0.70 EPS（原話："approximately 2% in total revenues and $0.70 in incremental earnings per share."）
- 2026-08-12｜CFO Mika Ware｜guidance：財測假設：7 月加一點上檔後，其餘時間 Chili's 同店中個位數、客流為正（原話："for the remainder of the year, we have assumed mid-single digit same-store sales and"）
- 2026-08-12｜CFO Mika Ware｜guidance：財測含收購阿拉巴馬與密西西比 12 家 Chili's 加盟店（原話："Guidance also contemplates the planned acquisition of 12 Chili's franchise restaurants located in"）
- 2026-08-12｜CFO Mika Ware｜guidance：12 家收購店對 EPS 影響約持平，增量營收約 $30M（原話："it's going to have a flat impact to EPS basically because it's a very small acquisition."）
- 2026-08-12｜CFO Mika Ware｜guidance：財測假設 Maggiano's 營收與獲利與去年持平（原話："Maggiano's is going to have flat revenues and flat profits"）
- 2026-08-12｜CFO Mika Ware｜guidance：全年定價約略高於 3%，組合（mix）假設持平，其餘成長來自客流（原話："flattish mix for the year. You got the price just over 3%"）
- 2026-08-12｜CFO Mika Ware｜margin：FY27 以 52 週計，餐廳層級利潤率預期改善 20–40bp（原話："I'm going to expect 20 to 40 basis points of margin improvement."）
- 2026-08-12｜CFO Mika Ware｜margin：第 53 週可讓利潤率改善最高到 50bp（原話："Depending on where it falls in that range, the 53rd week could get you"）
- 2026-08-12｜CFO Mika Ware｜margin：各季商品通膨建模路徑：Q1 4%、Q2 3%、Q3 2%、Q4 1%（原話："Q1, 3% inflation in Q2, 2% inflation in Q3 and 1% in Q4."）
- 2026-08-12｜CFO Mika Ware｜margin：管理層說利潤率成長在轉型後會趨緩（對比轉型期累積逾 600bp 改善）（原話："you're going to see the margin growth moderate a little bit."）
- 2026-08-12｜CFO Mika Ware｜margin：回答利潤率有無天花板：仍可擴張，但幅度不會像轉型期那麼大（原話："It's just not going to be as material as it has been during this turnaround."）
- 2026-08-12｜CEO Kevin Hochman｜margin：CEO 表示每年起始的利潤率財測偏合理，歷來都被超越（原話："then we've blown through it"）
- 2026-08-12｜CFO Mika Ware｜margin：Q4 Brinker 餐廳營業利潤率 18%，年增 20bp（原話："restaurant operating margins were 18%, a 20 basis points improvement"）
- 2026-08-12｜CFO Mika Ware｜margin：Q4 食材與飲料成本增加 80bp，商品通膨 4.4%（原話："Food and beverage costs for the quarter increased by 80 basis points, driven by 4.4% commodity"）
- 2026-08-12｜CFO Mika Ware｜margin：番茄價格飆升比預期久，已正常化且不影響 Q1 成本（原話："Tomato costs remained elevated longer than expected, but have since normalized and will"）
- 2026-08-12｜CFO Mika Ware｜margin：Q4 人力成本占比年減 90bp（原話："Labor for the quarter was favorable 90 basis points year-over-year."）
- 2026-08-12｜CFO Mika Ware｜margin：管理層要求營運端依想要的銷量排班，人力效率未達預期（原話："We have been telling our operators to staff for the sales they want."）
- 2026-08-12｜CFO Mika Ware｜margin：Q4 Chili's 同店 +5.6%：價格 4.3%、客流 +1.5%、組合 -0.2%（原話："driven by price of 4.3% and positive traffic of 1.5%, partially offset by negative mix of 0.2%."）
- 2026-08-12｜CFO Mika Ware｜margin：定價策略原為 3–5%，FY27 落在低端（原話："3% to 5%. We're on the lower end of that."）
- 2026-08-12｜CFO Mika Ware｜margin：管理層提到餐廳仍有客流容量（為歷史客數的 80%）（原話："Our restaurants are only at 80% capacity of"）
- 2026-08-12｜CEO Kevin Hochman｜competition：CEO 稱 Chili's 每人均消費比競爭對手低 $3–4（原話："average spend that is $3 to $4 below competition"）
- 2026-08-12｜CFO Mika Ware｜competition：CFO 稱同業也有不想現在過度提價的心態，因此自身保守看待定價（原話："You've heard a lot of our competitors have that same mindset"）
- 2026-08-12｜CEO Kevin Hochman｜product：Big Crispy 每店每日雞肉三明治銷量由 20 個升到 55 個（原話："By the end of Q4, we were selling 55 sandwiches per restaurant per day"）
- 2026-08-12｜CEO Kevin Hochman｜product：CEO 稱 Big Crispy 規模大於前兩次 Big Smasher 與 Big QP 的上市（原話："the Big Crispy is bigger than the '24 Big Smasher launch"）
- 2026-08-12｜CEO Kevin Hochman｜product：FY27 菜單優先順序調整，沙拉延到 FY28 上半年（原話："We have shuffled a little bit of our priorities in '27"）
- 2026-08-12｜CEO Kevin Hochman｜product：沙拉改在 FY28 上半年推出（原話："front half, we're going to launch salads."）
- 2026-08-12｜CEO Kevin Hochman｜product：外帶占營收 25%，被稱為尚未開發的下一個前沿（原話："which we haven't even scratched the surface on is to-go."）
- 2026-08-12｜CEO Kevin Hochman｜product：用餐室循環時間改善至少還有 3 年跑道（原話："we've got at least 3 years of runway on that"）
- 2026-08-12｜CFO Mika Ware｜product：3 For Me 參與率穩定，Q4 略高於 21%（原話："So in Q3, it was just under 21%. And in Q4, it's just over 21%"）
- 2026-08-12｜CEO Kevin Hochman｜customer：每月近一半以上的 token（會員代碼）為新客（原話："a little bit more than half of the tokens that we see each month"）
- 2026-08-12｜CFO Mika Ware｜customer：客流成長涵蓋各收入層級（原話："We're growing all income levels, low,"）
- 2026-08-12｜CFO Mika Ware｜risk：酒類品類整體承受壓力（原話："look at the whole alcohol category, we're feeling a little pressure"）
- 2026-08-12｜CEO Kevin Hochman｜risk：CEO 提到產業面臨的總體逆風仍在（原話："The macro headwinds the industry is experiencing are still there"）
- 2026-08-12｜CEO Kevin Hochman｜risk：Maggiano's 轉型進度比計畫慢（原話："the turnaround is happening slower than we had planned."）
- 2026-08-12｜CFO Mika Ware｜risk：Q4 Maggiano's 同店 -2.5%、客流 -5.3%（原話："comp sales for the quarter of negative 2.5% with negative"）
- 2026-08-12｜CFO Mika Ware｜capital_allocation：Q4 回購 $100M 普通股（原話："repurchasing $100 million of common stock"）
- 2026-08-12｜CFO Mika Ware｜capital_allocation：董事會 8 月增加回購授權，可用總額達 $750M（原話："program in August, bringing the total amount available to"）
- 2026-08-12｜CFO Mika Ware｜capital_allocation：年度結束後以循環信貸額度贖回 $350M 8.25% 債券（原話："we redeemed our outstanding $350 million, 8.25% bonds"）
- 2026-08-12｜CFO Mika Ware｜capital_allocation：資本支出上調的大宗來自店面改裝（reimage）（原話："The majority of that increase year-over-year is due to the reimages"）
- 2026-08-12｜CFO Mika Ware｜capital_allocation：FY27 計畫再完成 60–80 家改裝（FY26 為 11 家）（原話："we plan to complete another 60 to 80 during fiscal '27."）
- 2026-08-12｜CFO Mika Ware｜capital_allocation：管理層偏好持有不動產，不傾向賣回租回（原話："We prefer probably just to hold the real estate."）
- 2026-08-12｜CFO Mika Ware｜commitment：FY28 起改裝步調為每年 10% 店數（原話："we will start a planned cadence of 10% of the fleet annually."）
- 2026-08-12｜CFO Mika Ware｜commitment：新店成長 FY27 溫和，FY28 顯著加速，細節留待 9/17 投資人日（原話："the pipeline to ramp up significantly in fiscal '28"）
- 2026-08-12｜CFO Mika Ware｜commitment：CFO 稱有信心達成先前承諾的雙位數 EPS 成長（原話："So we feel good about delivering the results in the double-digit EPS"）
- 2026-08-12｜CEO Kevin Hochman｜commitment：管理層承諾維持價值領先與改善客人體驗（原話："we will work hard for our guests to maintain both our value leadership"）
- 2026-08-12｜CEO Kevin Hochman｜commitment：廣告與 $10.99 輪替的做法不打算改變（原話："So we don't plan on changing that formula."）
- 2026-08-12｜CEO Kevin Hochman｜commitment：營運副總的 FY27 執著指標：客流第三年，新增獲利改善（原話："have chosen traffic for a third year in a row"）
- 2026-08-12｜CEO Kevin Hochman｜commitment：店經理獎金改為完全聚焦銷售與獲利，GWOP 移出獎金（原話："We removed that from the bonus."）
- 2026-08-12｜CFO Mika Ware｜guidance：CFO 稱 7、8 月顯著加速，Q1 同店高於 Q4 的 6%，未給具體數字（原話："if Chili's was 6% in Q4, that means it's higher than that in Q1."）
- 2026-08-12｜CFO Mika Ware｜guidance：CFO 說 7 月營收與客流較 Q4 顯著加速（原話："significantly accelerated versus the fourth quarter,"）

### EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md
- 2026-09-17｜Mika Ware｜guidance：CFO 給出 3 年新目標：年營收成長 4%–6%（原話："deliver 4% to 6% annual revenue growth"）
- 2026-09-17｜Mika Ware｜guidance：3 年目標含雙位數 EPS 成長（原話："deliver double-digit EPS growth"）
- 2026-09-17｜Mika Ware｜guidance：新目標隱含假設：新店 2–3%、買回 3–5%（原話："Underlying these assumptions are the 2% to 3% new unit"）
- 2026-09-17｜Mika Ware｜guidance：CFO 對同店銷售的基本情境假設為 2%–3%，並稱有機會超標（原話："2% to 3% same-store sales, that seems highly achievable"）
- 2026-09-17｜Mika Ware｜guidance：價格／組合：mix 預期持平到略正（原話："flat to slightly positive moving forward"）
- 2026-09-17｜Mika Ware｜margin：餐廳利潤率每年 20–40 bps 的常態化擴張，維持舊說法（原話："still going to stick with my 20 to 40 basis points per year"）
- 2026-09-17｜Mika Ware｜margin：被問 North of 6 的 400 bps 差距能實現多少，CFO 稱不一定走到 400（原話："are we going to get all the way to 400? Maybe not."）
- 2026-09-17｜Kevin Hochman｜margin：North of 6 餐廳的餐廳營業利潤率比系統高 400 bps（原話："400 basis points better than the system"）
- 2026-09-17｜Kevin Hochman｜margin：North of 6 占比僅 20%，管理層以此論述利潤率上升空間（原話："only 20% of our estate are north of 6"）
- 2026-09-17｜Kevin Hochman｜margin：管理層稱利潤率擴張的主因是 AUV 而非砍成本（原話："the main driver of our margin expansion has been AUVs"）
- 2026-09-17｜Mika Ware｜margin：Chili's 品牌營業利潤率超過 18%（原話："the Chili's operating margins are over 18%"）
- 2026-09-17｜Mika Ware｜margin：G&A 約占營收 4%，無具體下調指引（原話："you guys see us stay around that 4% of revenues"）
- 2026-09-17｜Kevin Hochman｜margin：10.99 美元價位僅占 9% 的帳單（原話："it's only like 9% of checks"）
- 2026-09-17｜Kevin Hochman｜margin：EDLP 使人均客單低於 CDR 同業 3–4 美元（原話："$3 to $4 less on a per person average than our competitors"）
- 2026-09-17｜Mika Ware｜commitment：資本支出路徑：今年中位 2.75 億，後續 3.5 億再 4 億（原話："I would ramp that up to $350 million and then $400 million"）
- 2026-09-17｜Mika Ware｜capital_allocation：年度股數減少目標 3%–5%，由超額自由現金流支應（原話："our goal will be to reduce our shares by 3% to 5% annually"）
- 2026-09-17｜Mika Ware｜capital_allocation：槓桿目標：租賃調整後槓桿維持 2 倍以下（原話："our target is to keep it at less than 2x"）
- 2026-09-17｜Mika Ware｜capital_allocation：股利：現在不做，未來會再討論（原話："I'm not saying never. I'm just saying not right now."）
- 2026-09-17｜Mika Ware｜capital_allocation：租賃調整後槓桿由 3.7 倍降至 1.4 倍（原話："we took our lease adjusted leverage from 3.7x to 1.4x"）
- 2026-09-17｜Mika Ware｜capital_allocation：去年自由現金流 5.58 億美元（原話："last year, we delivered $558 million"）
- 2026-09-17｜Kevin Hochman｜capital_allocation：資本配置重心由還債轉為投資與買回（原話："our capital allocation will shift from paying down debt"）
- 2026-09-17｜Kevin Hochman｜capital_allocation：每年 reimage 資本支出超過 6,000 萬美元（原話："spending over $60 million a year in capital on reimages"）
- 2026-09-17｜Mika Ware｜commitment：新店節奏：2029 財年達每年 30 家（原話："ramp up to 30 units per year by F '29"）
- 2026-09-17｜Mika Ware｜commitment：新店成長率目標 2%–3%／年（原話："the pace that we want to go is 2% to 3% new units per year"）
- 2026-09-17｜Mika Ware｜commitment：新店單位投資額 500–600 萬美元（原話："going to be between $5 million and $6 million"）
- 2026-09-17｜Mika Ware｜commitment：F28 已核准 15 家新店（原話："we already have 15 units approved and ready to go for F '28"）
- 2026-09-17｜Mika Ware｜commitment：Reimage 目標 F28 達系統 10%（原話："our plan is to ramp up to 10% of the system in F '28"）
- 2026-09-17｜Mika Ware｜commitment：轉 reimage 到 F28 預計每年約 110 家，歷史最高 125 家（原話："125 is the most we've been able to get done in a year"）
- 2026-09-17｜Mika Ware｜commitment：管理層表示不縮小新店面積，新原型反而更大（原話："no plans for smaller ones. Not this time."）
- 2026-09-17｜Aaron White｜commitment：擬在 12–24 個月內推出股票薪酬計畫（原話："we are looking and evaluating a stock comp program"）
- 2026-09-17｜Mika Ware｜commitment：新店審慎擴張，不為追量核准次級地點（原話："not feel pressured to approve any subpar sites"）
- 2026-09-17｜Mika Ware｜product：早期 16 家 reimage 店銷售提升 3%–5%（原話："we are getting a 3% to 5% sales lift"）
- 2026-09-17｜Mika Ware｜product：Reimage 平均每家花費約 60 萬美元（原話："the average spend is $600,000 per unit"）
- 2026-09-17｜George Felix｜product：Triple Dipper 占 Chili's 總銷售 16%（原話："that one item alone now makes up 16% of Chili's total sales"）
- 2026-09-17｜George Felix｜product：管理層稱 Triple Dipper 未見退燒（原話："We have seen no signs of the triple dipper fading"）
- 2026-09-17｜George Felix｜product：Big Crispy 年化後預期成為 2.2 億美元以上品類（原話："going to be over $220 million category"）
- 2026-09-17｜George Felix｜product：Mexican QSR 為下一個目標品類，預計約 2 年後（原話："We're probably not even doing this in the next 12 months."）
- 2026-09-17｜Kevin Hochman｜product：菜單約 40% 尚待翻新（原話："We have 40% left."）
- 2026-09-17｜Kevin Hochman｜product：Maggiano's 義大利麵份量增加 20%（原話："20% more portions to all of our pasta dishes"）
- 2026-09-17｜Kevin Hochman｜product：Maggiano's 份量調整已納入現行財測（原話："That's all baked into the current guidance that you have."）
- 2026-09-17｜Kevin Hochman｜customer：新 token 約占 60%，管理層以此說明可持續 comp（原話："That represents about 60% of the tokens that we see are new."）
- 2026-09-17｜Kevin Hochman｜customer：新客在 9–12 個月內行為近似既有客（原話："they look a lot like existing guests"）
- 2026-09-17｜George Felix｜customer：Gen Z 占客群約 25%（原話："Gen Z is now making up about 25% of our total guest mix"）
- 2026-09-17｜Aaron White｜customer：每店每週客數目標 4,300（原話："Our goal is at 4,300."）
- 2026-09-17｜Aaron White｜customer：客數由 4,300 的目標對應約 2% 同店銷售（原話："and that's an additional 2% in same-store sales"）
- 2026-09-17｜Aaron White｜customer：2000 年代初同棟建築歷史高峰每週 5,200 人（原話："Our largest guests per week was an average of 5,200."）
- 2026-09-17｜Aaron White｜customer：出餐時間達標店僅 40%，目標 65%（原話："Only 40% of our system today are actually at our goals"）
- 2026-09-17｜Aaron White｜customer：小時工離職率降至 84%，首次回到業界平均（原話："declined to 84%"）
- 2026-09-17｜George Felix｜competition：管理層稱價格下殺未拖慢 Chili's（原話："It hasn't slowed Chili's down."）
- 2026-09-17｜Kevin Hochman｜competition：競爭對手開店只造成短期分流（原話："it's going to all snap back and it does."）
- 2026-09-17｜Kevin Hochman｜competition：管理層稱休閒餐飲價值感首度追平 QSR（原話："people think casual dining is as good a value as QSR"）
- 2026-09-17｜Kevin Hochman｜competition：管理層稱獨立餐廳目前在搶市占（原話："right now, I think independents are winning"）
- 2026-09-17｜George Felix｜competition：酒類份額為產業第一（原話："we are now the #1 alcohol share brand in the entire industry"）
- 2026-09-17｜Kevin Hochman｜competition：Maggiano's 約占獲利 3%（原話："It's about 3% of profitability."）
- 2026-09-17｜Kevin Hochman｜competition：Maggiano's 營運指標改善，財務與客流尚未反映（原話："not seeing it necessarily in the financials"）
- 2026-09-17｜Kevin Hochman｜competition：近 2–3 年聚焦 Chili's，之後可能重新看組合／併購（原話："that can change 2 to 3 years from now."）
- 2026-09-17｜Kevin Hochman｜risk：管理層稱體驗改善仍在中段（原話："we're still middle innings on improving this experience"）
- 2026-09-17｜George Felix｜risk：管理層承認消費者承壓、油價偏高（原話："We know the gas prices are high."）
- 2026-09-17｜Mika Ware｜risk：FY27 營收成長與 3 年目標的關係，CFO 稱因同店基準尚在摸索（原話："we're just trying to figure out, does this thing ever settle"）
- 2026-09-17｜Aaron White｜risk：只有 50% 餐廳（原文寫 15%）達歷史客流高峰，管理層仍視為成長空間（原話："only 50% of our restaurants, so 15% that are actually"）

### 問答異常語氣（迴避／改口／保留）
- EAT_Q4_2026_Earnings_Call_20260812.md｜問：Brian Vaccaro（Raymond James）：請提供 Q1 迄今 Chili's 同店或給個護欄｜答法：未給數字，僅說比 Q4 的 6% 高，並稱待季末再談 Q1 結果
- EAT_Q4_2026_Earnings_Call_20260812.md｜問：John Ivankoe（JPMorgan）：FY27 每間改裝的單店成本落在哪｜答法：稱數字仍在定案，只重申整體 $60–80M 與資本支出上調，細節延到投資人日
- EAT_Q4_2026_Earnings_Call_20260812.md｜問：Andrew Charles（TD Cowen）：12 家加盟店收購價格是多少｜答法：未給收購價，只說拿到很好的價格，細節之後再說
- EAT_Q4_2026_Earnings_Call_20260812.md｜問：Andrew Strelzik（BMO）：若薪酬改制能帶來更多流通，為何利潤率起點仍是 20–40bp｜答法：回答以通膨、低端定價與保守假設為由，並說明年中若銷售超預期可能優於財測，未接受流通提升的說法
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：Fadem：是否估算過獨立餐廳市場規模／從獨立餐廳取得份額｜答法：答「We have not. We don't look at it that way.」，未給數字
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：Binshtok：家庭客群目前占比與成長速度｜答法：CEO 稱不追蹤該區塊、沒有數據，改談社群與 Gen Z
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：Chris O'Cull：Chili's 是否出現更多用餐情境｜答法：CMO 稱沒有硬數據，僅以質化的社群例子回答
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：未具名分析師：快 5–10 分鐘出餐對同店／AUV 的貢獻｜答法：CEO 稱難以量化，改以經理刷卡等例子說明
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：Vaccaro：用餐時長過長的訪客占比｜答法：COO 稱沒有占比數字，只給平均約 50 分鐘
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：Carril：FY27 營收成長 6–8% 對比 3 年目標 4–6% 是否保守｜答法：CFO 未直接確認保守與否，改說仍在摸索新的同店常態值、2–3% 為基本情境
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：Andrew Charles：North of 6 的 400 bps 差距會實現多少｜答法：CFO 未給比例，稱不一定走到 400、不知天花板

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

## ⑥ 條件附卡（archetype_hint='轉機/特殊情境' 命中）：judge_addendum_archetype.md

<!-- source: .claude/skills/stock-analyst/references/archetype-gatesets.md sha256:d173785f92087f36 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary ∈ {金融，未獲利高成長，轉機/特殊情境，受監管公用/穩定內需} -->

# archetype 換尺 gate-set 附卡（QC-44/45/46）

## QC-44 金融（bank／insurer／broker）
archetype=金融時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：ROTCE(替FCF Margin) >15%穿越循環｜ROE且>COE~10%(替ROIC) ROE>12-15%｜跨信用循環ROTCE穩定含2008/2020壓力年(替10Y ROIC穩定) 壓力年仍正/不破底｜NIM趨勢+效率比cost/income(替毛利率定價) 效率比<~60%｜Capex/Rev不適用→operating leverage/效率比改善｜EPS+TBVPS複合+股息總回報(替EPS CAGR>20%) ~10-12%即優｜P/TBV vs ROTCE(替PEG)：Warranted P/TBV=(ROTCE−g)/(COE−g)，實際P/TBV≤warranted｜CET1 ratio(替D/E<0.7) >監管要求+緩衝(~11-13%)｜NPL/NCO趨勢+撥備覆蓋+CET1緩衝(替負債安全性)：信用品質穩、撥備足。[§QC-44]
§10估值主錨：P/TBV分位+P/E，用Warranted P/TBV判貴賤；EV/EBITDA拿掉。QC-31 signal：X改ROTCE跨循環<COE／CET1跌破監管／NPL·NCO結構惡化／重大舞弊，移除FCF·NI、EV-EBITDA、Capex觸發。§6跑道：放款·存款·AUM成長+費收業務+市佔，非TAM滲透。[§QC-44]
子型：bank＝CET1/NIM/效率比/NPL·NCO/ROTCE/P-TBV｜insurer(注意US掛牌ALV=Autoliv汽車安全件循環工業，非保險，勿誤歸)＝combined ratio<100%/float/Solvency II ratio/book value/ROE，不看NIM/CET1｜broker·交易所＝ARPU/AUC/take rate/活躍戶，常與未獲利高成長blend｜支付網絡不歸金融，走品質複利。[§子型]
batch補搜：`[ticker] CET1 ratio NIM efficiency ratio ROTCE`(bank)／`[ticker] combined ratio Solvency II book value`(insurer)；yfinance .info 給不出 CET1/NIM/效率比/NPL/ROTCE/TBV。[§batch]

## QC-45 未獲利高成長
archetype=未獲利高成長時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：Rule-of-40(營收成長%+FCF margin%，替EPS CAGR>20%) ≥40｜EV/S÷營收成長growth-adjusted或EV/gross-profit(替PEG<2)｜NRR+毛利率+增量OI margin改善軌跡(替ROIC>15%，GAAP負無意義) NRR>110%/GM>65-70%｜FCF margin+轉正軌跡(替FCF Margin>15%；已正看margin升，未正看跑道+轉正路徑)｜NI負時FCF/NI比無意義→改看FCF margin絕對值+淨現金+跑道，FCF正或跑道>12個月。[§QC-45]
§10估值主錨：EV/S(+EV/gross-profit)+Rule-of-40-adjusted，轉正後接forward P/E；trailing PE/PEG拿掉。**情境樹同步改走EV/S（2026-10-12）**：FY1共識EPS≤0時程式自動切`valuation_basis=sales_multiple`，`scenario_inputs`填營收路徑×終端EV/S×終端淨負債×終端股數（形狀見尾段），不再用EPS×本益比；負債重者(淨負債/EV>30%)Bear的`net_debt_y5`須如實反映融資缺口，股權價值為負即歸零。QC-31 signal：不因GAAP NI負觸發X；X改NRR跌破100%／Rule-of-40<20連2季／毛利結構崩／現金跑道<12個月無轉正路徑／SBC稀釋失控(股數>10%/yr無營收槓桿)。§6跑道：NRR+淨增客戶+TAM滲透+SBC-adjusted轉正時程。blend：fintech broker常＝金融×未獲利，兩套都跑、標背離。[§QC-45]

## QC-46 轉機／受監管公用（輕量尺，不展開大表）
轉機/特殊情境：§4/§10主錨→資產重估/SOTP/normalized earning power/P-TBV，非成長外推；EPS-CAGR/PEG不適用。Single Thing→轉機觸發(債務重組完成/出售虧損部門/新管理層/catalyst里程碑)，非「moat擴張」。§6/§5→「為何現在會轉」catalyst+下行保護(資產底/清算價值)。QC-31 X→流動性危機(跑道<12個月+無再融資)/重整失敗/治理舞弊。[§QC-46轉機]
受監管公用/穩定內需：§4/§10主錨→DDM/殖利率+股息成長/regulated ROE(rate base×allowed ROE)/P/B；PEG/高成長門檻不適用。§6成長→rate base成長+費率案(rate case)+准許ROE，非TAM滲透。§5護城河→監管特許/天然獨佔(single-axis)。QC-31 X→准許ROE結構下調/費率案連敗/監管轉敵/過度槓桿(利率敏感)。[§QC-46受監管]
此兩類不強制長表，但換尺與catalyst/下行保護須sourced。[§QC-46]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260711","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Chili's 份額增益是結構性（營運＋價值架構搶市），非純 lapping 的數學回歸","columns":{"2Y 驗證點":"同店續守 ≥ MSD 且跑贏產業","5Y 驗證點":"穿越一次消費放緩仍守正同店","10Y 驗證點":"Chili's 維持休閒正餐份額領先地位","具體數字門檻":"FY26-28 每季同店 ≥ +2%、vs 產業價差 ≥ +200bps","來源":"公司 Q3 FY26 8-K／法說（跑贏產業 420bps）","漂移觸發":"連 2 季同店 &lt; +2% → 削弱"}},{"id":"H2","text":"margin 恢復可守——OM ~10%＋餐廳層利潤率不因價值促銷回吐","columns":{"2Y 驗證點":"合併 OM 守 ≥ 9.5%","5Y 驗證點":"through-cycle OM ≥ 8%","10Y 驗證點":"規模＋供應鏈使 margin 結構性高於轉機前","具體數字門檻":"餐廳層 flow-through ≥ 10%；合併 OM FY26 ~10%","來源":"公司財報（FY25 OM 10.3%；Q3 flow-through ~14%）","漂移觸發":"flow-through 連 2 季 &lt; 10% → 削弱"}},{"id":"H3","text":"去債＋回購把 EPS 往上頂，估值對 DRI/TXRH 折價溫和收斂","columns":{"2Y 驗證點":"FY27 EPS ≥ $12、股數續縮","5Y 驗證點":"forward PE 站穩 14-16x","10Y 驗證點":"股東總回報（回購＋潛在復股息）持續","具體數字門檻":"年淨回購 ≥ 2%、FY27 共識 ≥ $12；折價由 ~40% 收至 ~30%","來源":"公司回購揭露（FY26 前三季 $343M）＋同業倍數","漂移觸發":"FY27 共識連 3 月 &lt; $11.50 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"同店大幅減速／轉負（消費放緩＋lapping tough comp）","columns":{"對應假設":"H1+H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Chili's 季度同店、量/價拆分","警戒閾值":"任一季轉負 ＝ 撤退；連 2 季 &lt; +2% ＝ 減碼／重評"}},{"id":"R2","text":"TXRH/DRI/Fast-casual 持續搶流量，Chili's vs 產業價差縮窄；價值促銷侵蝕餐廳層 margin","columns":{"對應假設":"H1/H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Black Box 月度流量、TXRH/DRI 季度同店、Chili's flow-through","警戒閾值":"價差連 3 月 &lt; +200bps ＝ 護城河侵蝕；flow-through 連 2 季 &lt; 10%"}},{"id":"R3","text":"牛肉超級週期／勞動通膨壓制餐廳層 margin；單一品牌集中風險（Chili's ~88%）","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"牛肉現貨/期貨、最低工資立法、餐廳層 OM 趨勢","警戒閾值":"餐廳層 OM 自高位回落 &gt; 200bps 且無定價對沖"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"starter 1/3；帽 3%；加碼＝Q4 FY26 comp ≥ +3% 且 FY27 guide 不下修；撤退＝Chili's 任一季 comp 轉負","irr_base_pct":7.0,"ev5y_pct":22.8,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.4,"ev5y_pct":22.8,"irr_base_pct":7.0,"max_dd_pct":-46.0,"bull_5y_price":319.0,"bear_5y_price":104.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"starter 1/3；帽 3%；加碼＝Q4 FY26 comp ≥ +3% 且 FY27 guide 不下修；撤退＝Chili's 任一季 comp 轉負","price_at_dd":185.26,"archetype":"轉機/特殊情境","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EAT_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
